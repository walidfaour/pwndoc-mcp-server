#pragma once

#include "config.hpp"
#include <string>
#include <nlohmann/json.hpp>
#include <curl/curl.h>
#include <optional>
#include <deque>
#include <chrono>
#include <stdexcept>
#include <map>

/**
 * Exception classes matching Python implementation
 */
class PwnDocError : public std::runtime_error {
public:
    explicit PwnDocError(const std::string& message) : std::runtime_error(message) {}
};

class AuthenticationError : public PwnDocError {
public:
    explicit AuthenticationError(const std::string& message) : PwnDocError(message) {}
};

class RateLimitError : public PwnDocError {
public:
    explicit RateLimitError(const std::string& message) : PwnDocError(message) {}
};

class NotFoundError : public PwnDocError {
public:
    explicit NotFoundError(const std::string& message) : PwnDocError(message) {}
};

/**
 * Simple sliding window rate limiter matching Python implementation
 */
class RateLimiter {
public:
    RateLimiter(int max_requests, int period);

    /**
     * Try to acquire a request slot
     */
    bool acquire();

    /**
     * Time to wait before next request is available (in seconds)
     */
    double wait_time() const;

private:
    int max_requests_;
    int period_;
    std::deque<std::chrono::steady_clock::time_point> requests_;
};

/**
 * PwnDoc API Client with comprehensive features:
 * - Automatic authentication and token refresh
 * - Rate limiting
 * - Automatic retries with exponential backoff
 * - Comprehensive error handling
 * - Logging
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
     * Make DELETE request with optional body
     */
    nlohmann::json del(const std::string& endpoint, const nlohmann::json& data = {});

    /**
     * Test connection
     */
    nlohmann::json test_connection();

    /**
     * Check if authenticated
     */
    bool is_authenticated() const;

private:
    Config config_;
    CURL* curl_;
    std::string token_;
    std::optional<std::string> refresh_token_;
    std::optional<std::chrono::steady_clock::time_point> token_expires_;
    RateLimiter rate_limiter_;

    /**
     * Ensure we have valid authentication
     */
    void ensure_authenticated();

    /**
     * Authenticate with username/password
     * Returns true if authentication succeeded
     */
    bool authenticate();

    /**
     * Refresh the authentication token
     * Returns true if refresh succeeded
     */
    bool refresh_authentication();

    /**
     * Wait if rate limited
     */
    void wait_for_rate_limit();

    /**
     * Make HTTP request with retries and error handling
     */
    nlohmann::json request(const std::string& method,
                           const std::string& endpoint,
                           const nlohmann::json& data = {});

    /**
     * Build full URL
     */
    std::string build_url(const std::string& endpoint) const;

    /**
     * Build headers for request
     */
    struct curl_slist* build_headers(bool include_auth = true);

    /**
     * Parse cookies from CURL handle
     */
    std::map<std::string, std::string> get_cookies();

    /**
     * Log message (simple stdout logging matching Python's logger)
     */
    void log_info(const std::string& message) const;
    void log_warning(const std::string& message) const;
    void log_debug(const std::string& message) const;
};
