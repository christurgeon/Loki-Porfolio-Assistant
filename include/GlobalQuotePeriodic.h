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
        CurlLibrary* m_curl = nullptr;
        std::queue<std::string> m_tickers;
        std::chrono::milliseconds m_interval;
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

            std::cerr << "error" << std::endl;
            // while (true)
            // {
            //     auto x = std::chrono::steady_clock::now() + m_interval;
            //     if (!m_tickers.empty())
            //     {
            //         std::string ticker = m_tickers.front();
            //         std::string&& url = m_alpha_vantage->GetQueryString_GLOBALQUOTE(ticker);
            //         auto data = m_curl->GET(url);
            //         std::cout << data << std::endl;
            //         m_tickers.pop();
            //         m_tickers.push(ticker);
            //     }
            //     std::this_thread::sleep_until(x);
            // }
        }

    public:
        GlobalQuotePeriodic(AlphaVantageConnection*& alpha_vantage, CurlLibrary* curl, std::chrono::milliseconds interval) 
        {
            m_alpha_vantage = alpha_vantage;
            m_curl = curl;
            m_interval = interval;
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
            std::thread([this]() { run(); });
        }
};