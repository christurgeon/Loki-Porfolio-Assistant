#pragma once 

#include <chrono>
#include <functional>
#include <mutex>
#include <thread>


class Periodic
{
    private:
        std::chrono::milliseconds m_interval;
        std::function<void(void)> m_function;
        std::thread* m_thread;

        // Join the thread during destructing
        void cleanUp() 
        {
            if (m_thread != nullptr && m_thread->joinable())
            {
                m_thread->join();
            }
        }

        // The driving mechanism of the periodic
        void run()
        {
            while (true)
            {
                auto x = std::chrono::steady_clock::now() + m_interval;
                m_function();
                std::this_thread::sleep_until(x);
            }
        }

    public:
        Periodic(std::chrono::milliseconds interval) : m_interval(interval) {}
        ~Periodic() { cleanUp(); }
        void registerPeriodic(std::function<void(void)>& function) { m_function = function; }
        
        // Start the periodic thread
        void start()
        {
            *m_thread = std::thread([this]() { run(); });
        }
};