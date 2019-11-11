#pragma once

#include <fstream>
#include <iostream>
#include <math.h>

// Path to file that holds stock watchlist
const static std::string WATCHLIST = "../watchlist.txt"; 

class Utilities 
{
    public:
        static double delta(double open, double current)
        {
            return (current - open) / open * 100;
        }

        static std::vector<std::string> parseWatchlistFile()
        {
            std::ifstream infile(WATCHLIST);
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
                std::cerr << "Unable to open up file: " << WATCHLIST << std::endl;
            }
            return tickers;
        }
};