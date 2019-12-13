#include "CurlLibrary.h"
#include "Utilities.h"


size_t CurlLibrary::Write(void* ptr, size_t size, size_t nmemb, std::string* data)
{
    data->append((char*) ptr, size * nmemb);
    return size * nmemb;
}


std::string CurlLibrary::GET(const std::string& url)
{
    if (m_curl == nullptr) 
    {
        std::cerr << "GET call has no working curl object, creating one..." << std::endl;
        curl_global_init(CURL_GLOBAL_ALL);
        m_curl = curl_easy_init();
        if (m_curl == nullptr)
        {
            std::cerr << "After curl_easy_init() curl object still cannot be created, returning..." << std::endl;
            throw RuntimeException("CurlLibrary.GET : Failed to initialize a curl object");
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
        throw RuntimeException("CurlLibrary.GET : Failed to perform GET request to AlphaVantage servers");
    }

    curl_easy_getinfo(m_curl, CURLINFO_RESPONSE_CODE, &m_http_code);
    if (m_http_code != 200)
    {
        std::cerr << "GET request may have failed, receieved status: " << m_http_code << std::endl;
        throw RuntimeException("CurlLibrary.GET : HTTP status code is not OK");
    }
    return response;
}


long CurlLibrary::getResponseCode()
{
    return m_http_code;
}