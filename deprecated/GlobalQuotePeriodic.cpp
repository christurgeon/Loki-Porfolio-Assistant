#include "GlobalQuotePeriodic.h"


GlobalQuotePeriodic::GlobalQuotePeriodic(AlphaVantageConnection*& alpha_vantage, slack::_detail::Slacking* slack, std::chrono::milliseconds interval, double delta) 
    : m_alpha_vantage{alpha_vantage}
    , m_slack{slack}
    , m_interval{interval}
    , m_delta{delta}
{
    m_curl = std::make_unique<CurlLibrary>();
    if (m_alpha_vantage == nullptr || m_slack == nullptr)
    {
        throw RuntimeException("FATAL ERROR: NullPointerException - unable to start market watcher.");
    }
}


void GlobalQuotePeriodic::cleanUp() 
{
    if (m_thread.joinable())
    {
        m_thread.join();
    }
}


void GlobalQuotePeriodic::run() 
{
    while (true)
    {
        auto x = std::chrono::steady_clock::now() + m_interval;
        {
            // Lock for exclusive access to the watchlist
            std::lock_guard<std::mutex> lock(m_mutex);
            if (!m_tickers.empty())
            {
                // Retrieve the market data from AlphaVantage servers
                std::string ticker = m_tickers.front();
                std::string&& url = m_alpha_vantage->GetQueryString_GLOBALQUOTE(ticker);
                std::string&& data = m_curl->GET(url);

                /**** DEBUG INFORMATION ****/
                std::cout << "DEBUG DATA\n" << data << std::endl;

                // Parse the data and calculate statistics
                try 
                {
                    Json::Value json = Utilities::toJson(data);
                    std::string change_percent = json["Global Quote"]["10. change percent"].asString();
                    float parsed_percent = stof( change_percent.substr(0, change_percent.length() - 1) );
                    std::string&& percent_change_message = buildPercentChangeMessage(ticker, parsed_percent);
                    if (!percent_change_message.empty())
                    {
                        std::cout << percent_change_message << std::endl;
                        m_slack->chat.postMessage(percent_change_message);
                    }
                }
                catch(RuntimeException& e)
                {
                    m_slack->chat.postMessage(ticker + ": " + e.what() + '\n' + data);
                }
                m_tickers.pop_front();
                m_tickers.push_back(ticker);
            }
        }
        std::this_thread::sleep_until(x);
    }
}


std::string GlobalQuotePeriodic::buildPercentChangeMessage(const std::string& ticker, float percent_change)
{
    // Return empty string if percent change doesn't exceed a multiple of the delta
    std::string return_string = "";
    bool up_delta_percent = percent_change > m_percent_change_tracker[ticker] + m_delta;
    bool down_delta_percent = percent_change < m_percent_change_tracker[ticker] - m_delta;

    if (percent_change > 0 && up_delta_percent) // Positive and bullish
    {
        return_string += ticker + " is up " + std::to_string(percent_change) + "%"; 
        m_percent_change_tracker[ticker] = percent_change;
    }
    else if (percent_change < 0 && down_delta_percent) // Negative and bearish
    {
        return_string += ticker + " is down " + std::to_string(percent_change) + "%";
        m_percent_change_tracker[ticker] = percent_change;
    }
    else if (up_delta_percent) // Negative but bullish
    {
        return_string += ticker + " has raised to a new daily percent change of " + std::to_string(percent_change) + "%";
        m_percent_change_tracker[ticker] = percent_change;
    }
    else if (down_delta_percent) // Positive but bearish
    {
        return_string += ticker + " has dipped to a new daily percent change of " + std::to_string(percent_change) + "%";
        m_percent_change_tracker[ticker] = percent_change;
    }
    return return_string;
}


void GlobalQuotePeriodic::start(const std::vector<std::string>& tickers)
{
    for (auto t : tickers) 
    {
        m_tickers.push_back(t);
        m_percent_change_tracker.emplace(t, 0);
    }
    m_thread = std::thread([this]() { run(); });
}


bool GlobalQuotePeriodic::addTicker(const std::string& ticker) 
{
    std::lock_guard<std::mutex> lock(m_mutex);
    auto target_ticker = std::find(m_tickers.begin(), m_tickers.end(), ticker);
    if (target_ticker == m_tickers.end())
    {
        m_tickers.push_back(ticker);
        m_percent_change_tracker.emplace(ticker, 0);
        return true;
    }
    return false;
}


bool GlobalQuotePeriodic::removeTicker(const std::string& ticker)
{
    std::lock_guard<std::mutex> lock(m_mutex);
    auto target_ticker = std::find(m_tickers.begin(), m_tickers.end(), ticker);
    if (target_ticker != m_tickers.end())
    {
        m_tickers.erase(target_ticker);
        m_percent_change_tracker.erase(ticker);
        return true;
    }
    return false;
}


void GlobalQuotePeriodic::sendWatchlist()
{
    std::lock_guard<std::mutex> lock(m_mutex);
    std::string watchlist = "WATCHLIST:\n{\n";
    for (auto t : m_tickers) 
    { 
        watchlist += "\t" + t + "\n"; 
    }
    watchlist += "}";
    m_slack->chat.postMessage(watchlist);
}


void GlobalQuotePeriodic::updateDelta(double delta) 
{
    std::lock_guard<std::mutex> lock(m_mutex); 
    m_delta = abs(delta); 
}