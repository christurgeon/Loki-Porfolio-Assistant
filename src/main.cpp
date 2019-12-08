#include "AlphaVantageConnection.h"
#include "CurlLibrary.h"
#include "Message.h"
#include "GlobalQuotePeriodic.h"
#include "Utilities.h"

#include "slacking.hpp"

#include <iostream>
#include <thread>
#include <chrono>


int main()
{
    // Parse the app configuration settings  
    AlphaVantageConnection* connection;
    std::chrono::milliseconds request_interval;
    try 
    {
        connection = AlphaVantageConnection::getInstance();
        Json::Value root;
        Json::Reader reader;
        std::ifstream config_file(Files::CONFIGURATION, std::ifstream::binary);
        if (!reader.parse(config_file, root))
        {
            std::cerr << "FATAL ERROR: Could not parse the config file - " << reader.getFormattedErrorMessages() << std::endl;
            return EXIT_FAILURE;
        }
        connection->setApiKey(root["config"]["alpha_vantage_key"].asString());
        int interval = std::atoi( root["config"]["requests_interval_millis"].asString().c_str() );
        request_interval = std::chrono::milliseconds(interval);
    } 
    catch (std::exception& e)
    {
        std::cerr << "An exception occurred while trying to set the AlphaVantage API key: " << e.what() << std::endl;
        return EXIT_FAILURE;
    }

    CurlLibrary curl;
    std::vector<std::string> tickers = Utilities::parseWatchlistFile();
    std::unique_ptr<GlobalQuotePeriodic> periodic = std::make_unique<GlobalQuotePeriodic>(connection, &curl, request_interval);
    periodic->start(tickers);

    // while(1) { std::this_thread::sleep_for(std::chrono::seconds(1)); }

    return EXIT_SUCCESS;
}

    // std::string url1 = connection->GetQueryString_INTRADAY("TSLA", "1min");
    // std::string url2 = connection->GetQueryString_GLOBALQUOTE("TSLA");
    // auto data1 = curl->GET(url1);
    // std::cout << data1 << std::endl;
    // auto data2 = curl->GET(url2);
    // std::cout << data2 << std::endl;