#include "AlphaVantageConnection.h"
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
    std::string slack_api_key, default_channel;
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
        slack_api_key = root["slack"]["slack_private_key"].asString();
        default_channel = root["slack"]["default_channel"].asString();
        int interval = std::atoi( root["config"]["requests_interval_millis"].asString().c_str() );
        request_interval = std::chrono::milliseconds(interval);
    } 
    catch (std::exception& e)
    {
        std::cerr << "An exception occurred while trying to parse the settings.json file: " << e.what() << std::endl;
        return EXIT_FAILURE;
    }

    // Create the periodic market watcher 
    auto& slack = slack::create(slack_api_key);
    slack.chat.channel = default_channel;
    std::unique_ptr<GlobalQuotePeriodic> periodic = std::make_unique<GlobalQuotePeriodic>(connection, &slack, request_interval);

    // Parse the initial watch list and start the periodic
    std::vector<std::string> tickers = Utilities::parseWatchlistFile();
    periodic->start(tickers);

    /* Not sure how best to do this. I want this thread to stay alive
     * so the other one can keep probing market data. Maybe have it 
     * perform another function or wait for a kill signal... for now it can sleep.
     */
    while(1) { std::this_thread::sleep_for(std::chrono::seconds(1)); }

    return EXIT_SUCCESS;
}

    // Sample commands
    // std::string url1 = connection->GetQueryString_INTRADAY("TSLA", "1min");
    // std::string url2 = connection->GetQueryString_GLOBALQUOTE("TSLA");
    // auto data1 = curl->GET(url1);
    // std::cout << data1 << std::endl;
    // auto data2 = curl->GET(url2);
    // std::cout << data2 << std::endl;