#include "AlphaVantageConnection.h"

// Forward declare the singleton instance 
AlphaVantageConnection* AlphaVantageConnection::m_instance = nullptr;

// Default link for AlphaVantage HTTP requests
const std::string AlphaVantageConnection::DEFAULT_URL = "https://www.alphavantage.co/query?";

AlphaVantageConnection* AlphaVantageConnection::getInstance()
{
    if (!m_instance)
    {
        m_instance = new AlphaVantageConnection();
    }
    return m_instance;
}

void AlphaVantageConnection::setApiKey(const std::string& api_key)
{
    m_api_key = api_key;
}

std::string AlphaVantageConnection::getApiKey() const
{
    return m_api_key;
}

std::string AlphaVantageConnection::TimeSeriesHelper(const std::string& series, const std::string& ticker, bool all_data) const
{
    std::string size = all_data ? "full" : "compact";
    std::string url = AlphaVantageConnection::DEFAULT_URL
        + "function="   + series    + "&"
        + "symbol="     + ticker    + "&"
        + "outputsize=" + size      + "&"
        + "apikey="     + m_api_key + "&";
    return url;
}

std::string AlphaVantageConnection::GetQueryString_TIMESERIESDAILY(const std::string& ticker, bool all_data) const
{    
    return TimeSeriesHelper("TIME_SERIES_DAILY", ticker, all_data);
}

std::string AlphaVantageConnection::GetQueryString_TIMESERIESWEEKLY(const std::string& ticker, bool all_data) const
{
    return TimeSeriesHelper("TIME_SERIES_WEEKLY", ticker, all_data);
}

std::string AlphaVantageConnection::GetQueryString_TIMESERIESMONTHLY(const std::string& ticker, bool all_data) const 
{
    return TimeSeriesHelper("TIME_SERIES_MONTHLY", ticker, all_data);
}

std::string AlphaVantageConnection::GetQueryString_INTRADAY(const std::string& ticker, const std::string& interval) const
{
    std::string url = AlphaVantageConnection::DEFAULT_URL
        + "function=TIME_SERIES_INTRADAY&"
        + "symbol="   + ticker    + "&" 
        + "interval=" + interval  + "&"
        + "apikey="   + m_api_key + "&";
    return url;
}

std::string AlphaVantageConnection::GetQueryString_GLOBALQUOTE(const std::string& ticker) const 
{
    std::string url = AlphaVantageConnection::DEFAULT_URL
        + "function=GLOBAL_QUOTE&"
        + "symbol=" + ticker    + "&"
        + "apikey=" + m_api_key + "&";
    return url;
}
