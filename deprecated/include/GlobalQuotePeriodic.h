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


class GlobalQuotePeriodic
{
    private:
        std::unique_ptr<CurlLibrary> m_curl;
        AlphaVantageConnection* m_alpha_vantage = nullptr;
        slack::_detail::Slacking* m_slack = nullptr;

        std::map<std::string, double> m_percent_change_tracker;
        std::list<std::string> m_tickers;
        std::chrono::milliseconds m_interval;
        std::mutex m_mutex;
        std::thread m_thread;

        double m_delta;

        // Join the thread during destructing
        void cleanUp();

        // Periodically queries market data
        void run();

        // NOTE: This function is assumed to be called when m_mutex is held by the calling function
        // Takes in a ticker and a recent percent change value and builds an update message
        std::string buildPercentChangeMessage(const std::string& ticker, float percent_change);

    public:
        GlobalQuotePeriodic(AlphaVantageConnection*& alpha_vantage, slack::_detail::Slacking* slack, std::chrono::milliseconds interval, double delta);

        // Stop the thread and terminate gracefully
        ~GlobalQuotePeriodic() { cleanUp(); }
        
        // Start the periodic thread
        void start(const std::vector<std::string>& tickers);

        // Add a ticker to the watchlist
        bool addTicker(const std::string& ticker);

        // Remove a ticker from the watchlist 
        bool removeTicker(const std::string& ticker);

        // Send the watchlist to the slack chat
        void sendWatchlist();

        // Update the delta value
        void updateDelta(double delta);
};