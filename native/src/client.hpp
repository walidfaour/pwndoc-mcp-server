#pragma once

#include "config.hpp"
#include <string>
#include <nlohmann/json.hpp>
#include <curl/curl.h>
#include <optional>

/**
 * PwnDoc API Client
 */
class PwnDocClient {
public:
    explicit PwnDocClient(const Config& config);
    ~PwnDocClient();
    
    // Disable copy
    PwnDocClient(const PwnDocClient&) = delete;
    PwnDocClient& operator=(const PwnDocClient&) = delete;
    
    /**
     * Make GET request
     */
    nlohmann::json get(const std::string& endpoint);
    
    /**
     * Make POST request
     */
    nlohmann::json post(const std::string& endpoint, const nlohmann::json& data = {});
    
    /**
     * Make PUT request
     */
    nlohmann::json put(const std::string& endpoint, const nlohmann::json& data = {});
    
    /**
     * Make DELETE request
     */
    nlohmann::json del(const std::string& endpoint);
    
    /**
     * Test connection
     */
    nlohmann::json test_connection();

private:
    Config config_;
    CURL* curl_;
    std::string token_;
    
    /**
     * Ensure we have a valid token
     */
    void ensure_token();
    
    /**
     * Authenticate with username/password
     */
    void authenticate();
    
    /**
     * Make HTTP request
     */
    nlohmann::json request(const std::string& method, 
                           const std::string& endpoint,
                           const nlohmann::json& data = {});
    
    /**
     * Build full URL
     */
    std::string build_url(const std::string& endpoint) const;
};
