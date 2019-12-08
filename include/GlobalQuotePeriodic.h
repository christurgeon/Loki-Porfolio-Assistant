#pragma once 

#include "AlphaVantageConnection.h"
#include "CurlLibrary.h"
#include "Utilities.h"

#include "slacking.hpp"

#include <chrono>
#include <functional>
#include <mutex>
#include <thread>
#include <queue>

/**
 *  1. add capability to say markets closed on this day
 *  2. good morning message before markets wake up
 */

class GlobalQuotePeriodic
{
    private:
        std::unique_ptr<CurlLibrary> m_curl;
        AlphaVantageConnection* m_alpha_vantage = nullptr;
        slack::_detail::Slacking* m_slack = nullptr;
        std::queue<std::string> m_tickers;
        std::chrono::milliseconds m_interval;
        std::thread m_thread;

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
                if (!m_tickers.empty())
                {
                    std::string ticker = m_tickers.front();
                    std::string&& url = m_alpha_vantage->GetQueryString_GLOBALQUOTE(ticker);
                    std::string&& data = m_curl->GET(url);
                    std::cout << data << std::endl;
                    m_slack->chat.postMessage(data);
                    m_tickers.pop();
                    m_tickers.push(ticker);
                }
                std::this_thread::sleep_until(x);
            }
        }

    public:
        GlobalQuotePeriodic(AlphaVantageConnection*& alpha_vantage, slack::_detail::Slacking* slack, std::chrono::milliseconds interval) 
        {
            m_alpha_vantage = alpha_vantage;
            m_slack = slack;
            m_interval = interval;
            m_curl = std::make_unique<CurlLibrary>();
            if (m_alpha_vantage == nullptr || m_curl == nullptr)
            {
                throw RuntimeException("FATAL ERROR: NullPointerException - unable to start market watcher.");
            }
        }

        ~GlobalQuotePeriodic() { cleanUp(); }
        
        // Start the periodic thread
        void start(const std::vector<std::string>& tickers)
        {
            for (auto t : tickers) m_tickers.push(t);
            m_thread = std::thread([this]() { run(); });
        }
};