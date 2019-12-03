// implement first in first out 
// for popping tickers, getting global
// computing, and sending it if it's needed

#pragma once 

#include "AlphaVantageConnection.h"
#include "CurlLibrary.h"
#include "Utilities.h"

#include <chrono>
#include <functional>
#include <mutex>
#include <thread>
#include <queue>


class GlobalQuotePeriodic
{
    private:
        AlphaVantageConnection* m_alpha_vantage = nullptr;
        std::unique_ptr<CurlLibrary> m_curl = nullptr;
        std::queue<std::string> m_tickers;
        std::chrono::milliseconds m_interval;
        // std::function<std::string(const std::string&)> m_function;
        std::thread* m_thread;

        // Join the thread during destructing
        void cleanUp() 
        {
            if (m_thread != nullptr && m_thread->joinable())
            {
                m_thread->join();
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
                    auto data = m_curl->GET(url);
                    std::cout << data << std::endl;
                    m_tickers.pop();
                    m_tickers.push(ticker);
                }
                std::this_thread::sleep_until(x);
            }
        }

    public:
        /***
         * FIGURE OUT HOW TO COPY OVER THE UNIQUE POINTERS TO THE PERIODI 
         */
        GlobalQuotePeriodic(AlphaVantageConnection* alpha_vantage, std::unique_ptr<CurlLibrary> curl, std::chrono::milliseconds interval) 
        {
            m_alpha_vantage = alpha_vantage;
            m_curl = curl;
            m_interval = interval;
            if (m_alpha_vantage == nullptr || m_curl == nullptr)
            {
                throw RuntimeException("FATAL ERROR: Unable to start market watcher [AlphaVantageConnection* == nullptr]");
            }
        }

        ~GlobalQuotePeriodic() { cleanUp(); }
        // void registerPeriodic(std::function<std::string(const std::string&)>& function) { m_function = function; }
        
        // Start the periodic thread
        void start(std::vector<std::string>& tickers)
        {
            for (auto t : tickers) m_tickers.push(t);
            *m_thread = std::thread([this]() { run(); });
        }
};