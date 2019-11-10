#include "AlphaVantageConnection.h"
#include "CurlLibrary.h"
#include "Message.h"

#include <iostream>
#include <thread>
#include <chrono>


int main()
{
    std::string last_http_request = "";
    AlphaVantageConnection* connection;

    try 
    {
        connection = AlphaVantageConnection::getInstance();
    } 
    catch (RuntimeException& e)
    {
        std::cerr << "An exception occurred: " << e.what() << std::endl;
        return EXIT_FAILURE;
    }

    std::unique_ptr<CurlLibrary> curl = std::make_unique<CurlLibrary>();
    std::string url = connection->GetQueryString("TIME_SERIES_INTRADAY", "TSLA", "1min");

    auto data = curl->GET(url);
    

    return EXIT_SUCCESS;
}