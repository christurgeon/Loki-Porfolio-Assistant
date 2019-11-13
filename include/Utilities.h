#pragma once

#include <filesystem>
#include <fstream>
#include <iostream>
#include <math.h>
#include <vector>


namespace Files 
{
    // Path to file that holds stock watchlist
    const static std::string WATCHLIST = "../watchlist.txt"; 

    // Path to file that holds configuration information
    const static std::string CONFIGURATION = "../settings.json";

}; // end namespace Files


class RuntimeException : public std::exception
{
    public:
        RuntimeException(const std::string& error_msg) : m_error_msg(error_msg) {}
        const char* what() const throw () { return m_error_msg.c_str(); }

    private:
        std::string m_error_msg = "An Exception Occurred";
}; 


class Utilities 
{
    public:
        static double delta(double open, double current)
        {
            return (current - open) / open * 100;
        }

        static std::vector<std::string> parseWatchlistFile()
        {
            std::ifstream infile(Files::WATCHLIST);
            std::vector<std::string> tickers;
            if (infile.is_open())
            {
                std::string ticker;
                while(getline(infile, ticker))
                {
                    tickers.push_back(ticker);
                }
                infile.close();
            }
            else
            {
                std::cerr << "Unable to open up file: " << Files::WATCHLIST << std::endl;
            }
            return tickers;
        }
};