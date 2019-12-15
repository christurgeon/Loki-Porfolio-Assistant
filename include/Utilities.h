#pragma once

#include "json/json.h"

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

        static Json::Value toJson(const std::string& str)
        {
            Json::CharReaderBuilder builder;
            Json::CharReader* reader = builder.newCharReader();
            Json::Value json;
            std::string errors;
            bool parsingSuccessful = reader->parse(
                str.c_str(),
                str.c_str() + str.size(),
                &json,
                &errors
            );
            delete reader;

            if (!parsingSuccessful) 
            {
                throw RuntimeException("Unable to parse the string: " + str);
            }
            return json;
        }
};