#include "AlphaVantageConnection.h"
#include "CurlLibrary.h"
#include "Message.h"
#include "Periodic.h"
#include "Utilities.h"

#include <iostream>
#include <thread>
#include <chrono>


int main()
{
    std::string last_http_request = "";

    // Configure the AlphaVantage connection with the API key
    AlphaVantageConnection* connection;
    try 
    {
        connection = AlphaVantageConnection::getInstance();
        Json::Value root;
        Json::Reader reader;
        std::ifstream config_file(Files::CONFIGURATION);
        bool parsing_successful = reader.parse(config_file, root);

        if (!parsing_successful)
        {
            std::cerr << "FATAL ERROR: Could not parse the config file - " << reader.getFormattedErrorMessages() << std::endl;
            return EXIT_FAILURE;
        }
        connection->setApiKey(root.get("alpha_vantage_key", "ERR_FATAL_NO_KEY").asString());
    } 
    catch (std::exception& e)
    {
        std::cerr << "An exception occurred while trying to set the AlphaVantage API key: " << e.what() << std::endl;
        return EXIT_FAILURE;
    }

    std::vector<std::string> tickers = Utilities::parseWatchlistFile();

    std::cout << "\nTICKERS: ";
    for (auto t : tickers)
    {
        std::cout << t + " ";
    }
    std::cout << std::endl << std::endl;

    std::unique_ptr<CurlLibrary> curl = std::make_unique<CurlLibrary>();

    std::string url1 = connection->GetQueryString_INTRADAY("TSLA", "1min");
    std::string url2 = connection->GetQueryString_GLOBALQUOTE("TSLA");

    auto data1 = curl->GET(url1);
    // std::cout << data1 << std::endl;
    auto data2 = curl->GET(url2);
    // std::cout << data2 << std::endl;

    return EXIT_SUCCESS;
}