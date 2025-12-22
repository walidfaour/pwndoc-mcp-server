#include "client.hpp"
#include <iostream>
#include <sstream>
#include <ctime>
#include <iomanip>
#include <thread>
#include <cmath>
#include <algorithm>

using json = nlohmann::json;

// CURL write callback
static size_t write_callback(void* contents, size_t size, size_t nmemb, std::string* data) {
    size_t total = size * nmemb;
    data->append((char*)contents, total);
    return total;
}

// Helper to get current timestamp for logging
static std::string get_timestamp() {
    auto now = std::time(nullptr);
    auto tm = std::localtime(&now);
    std::ostringstream oss;
    oss << std::put_time(tm, "%Y-%m-%d %H:%M:%S");
    return oss.str();
}

// ============================================================================
// RateLimiter Implementation
// ============================================================================

RateLimiter::RateLimiter(int max_requests, int period)
    : max_requests_(max_requests), period_(period) {}

bool RateLimiter::acquire() {
    auto now = std::chrono::steady_clock::now();

    // Remove old requests outside the sliding window
    while (!requests_.empty()) {
        auto elapsed = std::chrono::duration_cast<std::chrono::seconds>(
            now - requests_.front()).count();
        if (elapsed >= period_) {
            requests_.pop_front();
        } else {
            break;
        }
    }

    // Check if we have a slot available
    if (static_cast<int>(requests_.size()) < max_requests_) {
        requests_.push_back(now);
        return true;
    }

    return false;
}

double RateLimiter::wait_time() const {
    if (requests_.empty() || static_cast<int>(requests_.size()) < max_requests_) {
        return 0.0;
    }

    auto now = std::chrono::steady_clock::now();
    auto oldest = requests_.front();
    auto elapsed = std::chrono::duration_cast<std::chrono::seconds>(now - oldest).count();

    return std::max(0.0, static_cast<double>(period_ - elapsed));
}

// ============================================================================
// PwnDocClient Implementation
// ============================================================================

PwnDocClient::PwnDocClient(const Config& config)
    : config_(config),
      curl_(nullptr),
      rate_limiter_(config.rate_limit_max_requests, config.rate_limit_period) {

    curl_global_init(CURL_GLOBAL_DEFAULT);
    curl_ = curl_easy_init();
    if (!curl_) {
        throw PwnDocError("Failed to initialize CURL");
    }

    // Set token if provided
    if (config_.token) {
        token_ = *config_.token;
        log_debug("Using provided token for authentication");
    }

    log_info("PwnDoc client initialized for " + config_.url);
}

PwnDocClient::~PwnDocClient() {
    if (curl_) {
        curl_easy_cleanup(curl_);
    }
    curl_global_cleanup();
}

// ============================================================================
// Logging Methods
// ============================================================================

void PwnDocClient::log_info(const std::string& message) const {
    if (config_.log_level <= 0) { // 0 = INFO
        std::cout << "[" << get_timestamp() << "] INFO: " << message << std::endl;
    }
}

void PwnDocClient::log_warning(const std::string& message) const {
    if (config_.log_level <= 1) { // 1 = WARNING
        std::cerr << "[" << get_timestamp() << "] WARNING: " << message << std::endl;
    }
}

void PwnDocClient::log_debug(const std::string& message) const {
    if (config_.log_level <= -1) { // -1 = DEBUG
        std::cout << "[" << get_timestamp() << "] DEBUG: " << message << std::endl;
    }
}

// ============================================================================
// Helper Methods
// ============================================================================

std::string PwnDocClient::build_url(const std::string& endpoint) const {
    std::string url = config_.url;
    if (url.back() == '/') url.pop_back();

    std::string ep = endpoint;
    if (!ep.empty() && ep.front() != '/') ep = "/" + ep;

    return url + "/api" + ep;
}

struct curl_slist* PwnDocClient::build_headers(bool include_auth) {
    struct curl_slist* headers = nullptr;
    headers = curl_slist_append(headers, "Content-Type: application/json");

    if (include_auth && !token_.empty()) {
        std::string auth_header = "Authorization: JWT " + token_;
        headers = curl_slist_append(headers, auth_header.c_str());
    }

    return headers;
}

std::map<std::string, std::string> PwnDocClient::get_cookies() {
    std::map<std::string, std::string> cookies;

    struct curl_slist* cookie_list = nullptr;
    curl_easy_getinfo(curl_, CURLINFO_COOKIELIST, &cookie_list);

    if (cookie_list) {
        struct curl_slist* current = cookie_list;
        while (current) {
            std::string cookie_line = current->data;

            // Parse cookie: domain\tTRUE\tpath\tFALSE\texpires\tname\tvalue
            std::istringstream iss(cookie_line);
            std::string domain, flag, path, secure, expires, name, value;
            iss >> domain >> flag >> path >> secure >> expires >> name >> value;

            if (!name.empty()) {
                cookies[name] = value;
            }

            current = current->next;
        }
        curl_slist_free_all(cookie_list);
    }

    return cookies;
}

// ============================================================================
// Authentication Methods
// ============================================================================

void PwnDocClient::ensure_authenticated() {
    // Check if token is expired
    if (token_expires_.has_value()) {
        auto now = std::chrono::steady_clock::now();
        if (now >= *token_expires_) {
            log_debug("Token expired, refreshing authentication");
            if (refresh_token_.has_value()) {
                if (!refresh_authentication()) {
                    log_warning("Token refresh failed, re-authenticating");
                    authenticate();
                }
            } else {
                authenticate();
            }
        }
    }

    // If no token, authenticate
    if (token_.empty()) {
        if (config_.username && config_.password) {
            log_debug("No token available, authenticating");
            authenticate();
        } else {
            throw AuthenticationError("No authentication credentials provided");
        }
    }
}

bool PwnDocClient::authenticate() {
    if (!config_.username || !config_.password) {
        throw AuthenticationError("Username and password required for authentication");
    }

    log_info("Authenticating user: " + *config_.username);

    json login_data = {
        {"username", *config_.username},
        {"password", *config_.password}
    };

    std::string url = build_url("/users/login");
    std::string response_data;

    curl_easy_reset(curl_);
    curl_easy_setopt(curl_, CURLOPT_URL, url.c_str());
    curl_easy_setopt(curl_, CURLOPT_POST, 1L);
    curl_easy_setopt(curl_, CURLOPT_COOKIEFILE, ""); // Enable cookie engine

    std::string body = login_data.dump();
    curl_easy_setopt(curl_, CURLOPT_POSTFIELDS, body.c_str());

    struct curl_slist* headers = build_headers(false);
    curl_easy_setopt(curl_, CURLOPT_HTTPHEADER, headers);

    curl_easy_setopt(curl_, CURLOPT_WRITEFUNCTION, write_callback);
    curl_easy_setopt(curl_, CURLOPT_WRITEDATA, &response_data);

    if (!config_.verify_ssl) {
        curl_easy_setopt(curl_, CURLOPT_SSL_VERIFYPEER, 0L);
        curl_easy_setopt(curl_, CURLOPT_SSL_VERIFYHOST, 0L);
    }

    curl_easy_setopt(curl_, CURLOPT_TIMEOUT, config_.timeout);

    CURLcode res = curl_easy_perform(curl_);
    curl_slist_free_all(headers);

    if (res != CURLE_OK) {
        throw AuthenticationError(std::string("Authentication request failed: ") + curl_easy_strerror(res));
    }

    long http_code = 0;
    curl_easy_getinfo(curl_, CURLINFO_RESPONSE_CODE, &http_code);

    if (http_code == 401) {
        throw AuthenticationError("Invalid username or password");
    }

    if (http_code >= 400) {
        throw AuthenticationError("Authentication failed with HTTP " + std::to_string(http_code));
    }

    json response = json::parse(response_data);
    if (response.contains("datas") && response["datas"].contains("token")) {
        token_ = response["datas"]["token"].get<std::string>();

        // Set token expiry (default 1 hour)
        auto now = std::chrono::steady_clock::now();
        token_expires_ = now + std::chrono::hours(1);

        // Extract refresh token from cookies
        auto cookies = get_cookies();
        if (cookies.find("refreshToken") != cookies.end()) {
            refresh_token_ = cookies["refreshToken"];
            log_debug("Refresh token obtained from cookies");
        }

        log_info("Authentication successful");
        return true;
    } else {
        throw AuthenticationError("Failed to get token from login response");
    }
}

bool PwnDocClient::refresh_authentication() {
    if (!refresh_token_.has_value()) {
        log_warning("No refresh token available");
        return false;
    }

    log_debug("Refreshing authentication token");

    std::string url = build_url("/users/refreshtoken");
    std::string response_data;

    curl_easy_reset(curl_);
    curl_easy_setopt(curl_, CURLOPT_URL, url.c_str());
    curl_easy_setopt(curl_, CURLOPT_POST, 1L);
    curl_easy_setopt(curl_, CURLOPT_POSTFIELDS, "");
    curl_easy_setopt(curl_, CURLOPT_COOKIEFILE, "");

    // Set refresh token cookie
    std::string cookie = "refreshToken=" + *refresh_token_;
    curl_easy_setopt(curl_, CURLOPT_COOKIE, cookie.c_str());

    struct curl_slist* headers = build_headers(false);
    curl_easy_setopt(curl_, CURLOPT_HTTPHEADER, headers);

    curl_easy_setopt(curl_, CURLOPT_WRITEFUNCTION, write_callback);
    curl_easy_setopt(curl_, CURLOPT_WRITEDATA, &response_data);

    if (!config_.verify_ssl) {
        curl_easy_setopt(curl_, CURLOPT_SSL_VERIFYPEER, 0L);
        curl_easy_setopt(curl_, CURLOPT_SSL_VERIFYHOST, 0L);
    }

    curl_easy_setopt(curl_, CURLOPT_TIMEOUT, config_.timeout);

    CURLcode res = curl_easy_perform(curl_);
    curl_slist_free_all(headers);

    if (res != CURLE_OK) {
        log_warning(std::string("Token refresh request failed: ") + curl_easy_strerror(res));
        return false;
    }

    long http_code = 0;
    curl_easy_getinfo(curl_, CURLINFO_RESPONSE_CODE, &http_code);

    if (http_code != 200) {
        log_warning("Token refresh failed with HTTP " + std::to_string(http_code));
        return false;
    }

    json response = json::parse(response_data);
    if (response.contains("datas") && response["datas"].contains("token")) {
        token_ = response["datas"]["token"].get<std::string>();

        // Update token expiry
        auto now = std::chrono::steady_clock::now();
        token_expires_ = now + std::chrono::hours(1);

        log_info("Token refreshed successfully");
        return true;
    }

    return false;
}

bool PwnDocClient::is_authenticated() const {
    return !token_.empty();
}

// ============================================================================
// Rate Limiting
// ============================================================================

void PwnDocClient::wait_for_rate_limit() {
    if (!rate_limiter_.acquire()) {
        double wait = rate_limiter_.wait_time();
        if (wait > 0) {
            log_warning("Rate limit reached, waiting " + std::to_string(wait) + " seconds");
            std::this_thread::sleep_for(std::chrono::milliseconds(static_cast<int>(wait * 1000)));
            rate_limiter_.acquire(); // Try again after waiting
        }
    }
}

// ============================================================================
// HTTP Request Methods
// ============================================================================

json PwnDocClient::request(const std::string& method,
                           const std::string& endpoint,
                           const json& data) {
    ensure_authenticated();
    wait_for_rate_limit();

    std::string url = build_url(endpoint);
    log_debug(method + " " + url);

    // Retry loop with exponential backoff
    for (int attempt = 0; attempt < config_.max_retries; ++attempt) {
        std::string response_data;

        curl_easy_reset(curl_);
        curl_easy_setopt(curl_, CURLOPT_URL, url.c_str());

        // Set method
        if (method == "POST") {
            curl_easy_setopt(curl_, CURLOPT_POST, 1L);
        } else if (method == "PUT") {
            curl_easy_setopt(curl_, CURLOPT_CUSTOMREQUEST, "PUT");
        } else if (method == "DELETE") {
            curl_easy_setopt(curl_, CURLOPT_CUSTOMREQUEST, "DELETE");
        }
        // GET is default, no need to set

        // Set body for POST/PUT/DELETE
        std::string body;
        if (!data.empty()) {
            body = data.dump();
            curl_easy_setopt(curl_, CURLOPT_POSTFIELDS, body.c_str());
        }

        // Set headers
        struct curl_slist* headers = build_headers(true);
        curl_easy_setopt(curl_, CURLOPT_HTTPHEADER, headers);

        curl_easy_setopt(curl_, CURLOPT_WRITEFUNCTION, write_callback);
        curl_easy_setopt(curl_, CURLOPT_WRITEDATA, &response_data);

        if (!config_.verify_ssl) {
            curl_easy_setopt(curl_, CURLOPT_SSL_VERIFYPEER, 0L);
            curl_easy_setopt(curl_, CURLOPT_SSL_VERIFYHOST, 0L);
        }

        curl_easy_setopt(curl_, CURLOPT_TIMEOUT, config_.timeout);

        CURLcode res = curl_easy_perform(curl_);
        curl_slist_free_all(headers);

        // Handle CURL errors with retry
        if (res != CURLE_OK) {
            std::string error_msg = std::string("Request failed: ") + curl_easy_strerror(res);

            if (attempt < config_.max_retries - 1) {
                int delay_ms = static_cast<int>(config_.retry_delay * std::pow(2, attempt) * 1000);
                log_warning(error_msg + " (attempt " + std::to_string(attempt + 1) +
                          "/" + std::to_string(config_.max_retries) + ", retrying in " +
                          std::to_string(delay_ms) + "ms)");
                std::this_thread::sleep_for(std::chrono::milliseconds(delay_ms));
                continue;
            }

            throw PwnDocError(error_msg);
        }

        long http_code = 0;
        curl_easy_getinfo(curl_, CURLINFO_RESPONSE_CODE, &http_code);

        log_debug("Response: HTTP " + std::to_string(http_code));

        // Handle 401 - try to refresh token and retry
        if (http_code == 401) {
            log_warning("Received 401 Unauthorized, attempting token refresh");

            if (refresh_token_.has_value() && refresh_authentication()) {
                log_info("Token refreshed, retrying request");
                continue; // Retry with new token
            } else if (config_.username && config_.password) {
                log_info("Re-authenticating and retrying request");
                authenticate();
                continue; // Retry with new token
            }

            throw AuthenticationError("Authentication failed (401 Unauthorized)");
        }

        // Handle 404
        if (http_code == 404) {
            throw NotFoundError("Resource not found: " + endpoint);
        }

        // Handle 429 - Rate limit
        if (http_code == 429) {
            if (attempt < config_.max_retries - 1) {
                int delay_ms = static_cast<int>(config_.retry_delay * std::pow(2, attempt) * 1000);
                log_warning("Rate limited by server (429), retrying in " + std::to_string(delay_ms) + "ms");
                std::this_thread::sleep_for(std::chrono::milliseconds(delay_ms));
                continue;
            }

            throw RateLimitError("Rate limit exceeded (429 Too Many Requests)");
        }

        // Handle other HTTP errors
        if (http_code >= 400) {
            std::string error_detail = "HTTP " + std::to_string(http_code);

            // Try to parse error message from response
            try {
                json error_response = json::parse(response_data);
                if (error_response.contains("datas")) {
                    error_detail += ": " + error_response["datas"].dump();
                } else if (error_response.contains("message")) {
                    error_detail += ": " + error_response["message"].get<std::string>();
                }
            } catch (...) {
                // If parsing fails, include raw response
                if (!response_data.empty()) {
                    error_detail += ": " + response_data;
                }
            }

            throw PwnDocError(error_detail);
        }

        // Success - parse and return response
        try {
            return json::parse(response_data);
        } catch (const json::parse_error& e) {
            // If response is empty or not JSON, return success indicator
            if (response_data.empty()) {
                return json({{"success", true}});
            }
            throw PwnDocError(std::string("Failed to parse JSON response: ") + e.what());
        }
    }

    // Should never reach here
    throw PwnDocError("Request failed after " + std::to_string(config_.max_retries) + " retries");
}

// ============================================================================
// Public HTTP Methods
// ============================================================================

json PwnDocClient::get(const std::string& endpoint) {
    return request("GET", endpoint);
}

json PwnDocClient::post(const std::string& endpoint, const json& data) {
    return request("POST", endpoint, data);
}

json PwnDocClient::put(const std::string& endpoint, const json& data) {
    return request("PUT", endpoint, data);
}

json PwnDocClient::del(const std::string& endpoint, const json& data) {
    return request("DELETE", endpoint, data);
}

json PwnDocClient::test_connection() {
    try {
        ensure_authenticated();
        json user = get("/users/me");

        std::string username = "unknown";
        if (user.contains("datas") && user["datas"].contains("username")) {
            username = user["datas"]["username"].get<std::string>();
        }

        return {
            {"status", "ok"},
            {"user", username},
            {"url", config_.url}
        };
    } catch (const std::exception& e) {
        return {
            {"status", "error"},
            {"error", e.what()},
            {"url", config_.url}
        };
    }
}
