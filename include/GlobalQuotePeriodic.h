#pragma once 

#include "AlphaVantageConnection.h"
#include "CurlLibrary.h"
#include "Utilities.h"

#include "slacking.hpp"

#include <algorithm>
#include <chrono>
#include <functional>
#include <list>
#include <map>
#include <mutex>
#include <thread>


/********************************************************************************
 * StockTrackerMap maps a ticker to a vector of booleans which                  *
 * monitors different statistics that are tracked by the bot.                   *
 *                                                                              *
 * @example                                                                     *  
 * [-DELTA, -2*DELTA, -3*DELTA, -X*DELTA, +DELTA, +2*DELTA, +3*DELTA, +X*DELTA] *
 * where X >= 4                                                                 *
 ********************************************************************************/ 
using StockTrackerMap = std::map<std::string, std::vector<bool>>;


class GlobalQuotePeriodic
{
    private:
        std::unique_ptr<CurlLibrary> m_curl;
        AlphaVantageConnection* m_alpha_vantage = nullptr;
        slack::_detail::Slacking* m_slack = nullptr;
        StockTrackerMap m_tracker;

        std::list<std::string> m_tickers;
        std::chrono::milliseconds m_interval;
        std::mutex m_mutex;
        std::thread m_thread;

        double m_delta;

        // Join the thread during destructing
        void cleanUp() 
        {
            if (m_thread.joinable())
            {
                m_thread.join();
            }
        }

        // Periodically queries market data
        void run() 
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

                        std::cout << data << std::endl;

                        // Parse the data and calculate statistics
                        std::string message = ticker + '\n';
                        try 
                        {
                            Json::Value json = Utilities::toJson(data);
                            std::string change_percent = json["Global Quote"]["10. change percent"].asString();
                            change_percent = change_percent.substr(0, change_percent.length() - 1);
                            std::cout << change_percent << std::endl;
                            // run some calculations to see if the value needs to be sent
                            // also look into opening this daily
                        }
                        catch(RuntimeException& e)
                        {
                            m_slack->chat.postMessage(message + e.what() + '\n' + data);
                        }
                        m_tickers.pop_front();
                        m_tickers.push_back(ticker);
                    }
                }
                std::this_thread::sleep_until(x);
            }
        }

    public:
        GlobalQuotePeriodic(AlphaVantageConnection*& alpha_vantage, slack::_detail::Slacking* slack, std::chrono::milliseconds interval, double delta) 
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

        // Stop the thread and terminate gracefully
        ~GlobalQuotePeriodic() { cleanUp(); }
        
        // Start the periodic thread
        void start(const std::vector<std::string>& tickers)
        {
            for (auto t : tickers) 
            {
                m_tickers.push_back(t);
                m_tracker[t] = std::vector<bool>(8, false);
            }
            m_thread = std::thread([this]() { run(); });
        }

        // Add a ticker to the watchlist
        bool addTicker(const std::string& ticker) 
        {
            std::lock_guard<std::mutex> lock(m_mutex);
            auto target_ticker = std::find(m_tickers.begin(), m_tickers.end(), ticker);
            if (target_ticker == m_tickers.end())
            {
                m_tickers.push_back(ticker);
                m_tracker[ticker] = std::vector<bool>(8, false);
                return true;
            }
            return false;
        }

        // Remove a ticker from the watchlist 
        bool removeTicker(const std::string& ticker)
        {
            std::lock_guard<std::mutex> lock(m_mutex);
            auto target_ticker = std::find(m_tickers.begin(), m_tickers.end(), ticker);
            if (target_ticker != m_tickers.end())
            {
                m_tickers.erase(target_ticker);
                m_tracker.erase(ticker);
                return true;
            }
            return false;
        }

        // Send the watchlist to the slack chat
        void sendWatchlist()
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

        // Update the delta value for percent change
        void updateDelta(double delta) 
        {
            std::lock_guard<std::mutex> lock(m_mutex); 
            m_delta = abs(delta); 
        }
};