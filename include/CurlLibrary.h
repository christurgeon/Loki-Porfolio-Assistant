#pragma once

#include "Utilities.h"

#include <iostream>
#include <string>
#include <curl/curl.h>


class CurlLibrary
{
    private:
        CURL* m_curl = nullptr;
        long m_http_code;
        static size_t Write(void* ptr, size_t size, size_t nmemb, std::string* data);

    public:
        CurlLibrary() 
        {         
            curl_global_init(CURL_GLOBAL_ALL);
            m_curl = curl_easy_init(); 
            m_http_code = 0;
        }
        CurlLibrary(const CurlLibrary& curl)
        {
            m_curl = curl.m_curl;
            m_http_code = curl.m_http_code;
        }
        ~CurlLibrary() { if (m_curl != nullptr) curl_easy_cleanup(m_curl); }
        std::string GET(const std::string& url);
        long getResponseCode();
};