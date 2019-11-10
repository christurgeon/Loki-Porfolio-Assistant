#pragma once

#include <string>
#include <curl/curl.h>


class CurlLibrary
{
    private:
        CURL* m_curl;
        long m_http_code;
        static size_t Write(void* ptr, size_t size, size_t nmemb, std::string* data);

    public:
        CurlLibrary() : m_curl(curl_easy_init()), m_http_code(0) {}
        // ~CurlLibrary() { if (m_curl) curl_easy_cleanup(m_curl); } investigate this
        std::string GET(const std::string& url);
        long getResponseCode();
};