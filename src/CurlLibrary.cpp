#include "CurlLibrary.h"

#include <iostream>

size_t CurlLibrary::Write(void* ptr, size_t size, size_t nmemb, std::string* data)
{
    data->append((char*) ptr, size * nmemb);
    return size * nmemb;
}


std::string CurlLibrary::GET(const std::string& url)
{
    if (!m_curl) 
    {
        std::cerr << "GET call has no working curl object, creating one..." << std::endl;
        m_curl = curl_easy_init();
        if (!m_curl)
        {
            std::cerr << "After curl_easy_init() curl object still cannot be created, returning..." << std::endl;
            return nullptr;
        }
    }
    std::string header;
    std::string response;
    curl_easy_setopt(m_curl, CURLOPT_URL, url.c_str());
    curl_easy_setopt(m_curl, CURLOPT_WRITEFUNCTION, &Write);
    curl_easy_setopt(m_curl, CURLOPT_WRITEDATA, &response);

    auto rc = curl_easy_perform(m_curl);
    if (rc != CURLE_OK)
    {
        std::cerr << "The AlphaVantage server could not be reached..." << std::endl;
        return nullptr;
    }

    double elapsed_time;
    curl_easy_getinfo(m_curl, CURLINFO_RESPONSE_CODE, &m_http_code);
    curl_easy_getinfo(m_curl, CURLINFO_TOTAL_TIME, &elapsed_time);
    curl_easy_getinfo(m_curl, CURLINFO_EFFECTIVE_URL, &url);

    if (m_http_code != 200)
    {
        std::cerr << "GET request may have failed, receieved status: " << m_http_code << std::endl;
        return nullptr;
    }
    return response;
}


long CurlLibrary::getResponseCode()
{
    return m_http_code;
}