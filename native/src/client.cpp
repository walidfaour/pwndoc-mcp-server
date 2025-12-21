#include "client.hpp"
#include <stdexcept>
#include <sstream>

using json = nlohmann::json;

// CURL write callback
static size_t write_callback(void* contents, size_t size, size_t nmemb, std::string* data) {
    size_t total = size * nmemb;
    data->append((char*)contents, total);
    return total;
}

PwnDocClient::PwnDocClient(const Config& config) : config_(config), curl_(nullptr) {
    curl_global_init(CURL_GLOBAL_DEFAULT);
    curl_ = curl_easy_init();
    if (!curl_) {
        throw std::runtime_error("Failed to initialize CURL");
    }
    
    // Set token if provided
    if (config_.token) {
        token_ = *config_.token;
    }
}

PwnDocClient::~PwnDocClient() {
    if (curl_) {
        curl_easy_cleanup(curl_);
    }
    curl_global_cleanup();
}

std::string PwnDocClient::build_url(const std::string& endpoint) const {
    std::string url = config_.url;
    if (url.back() == '/') url.pop_back();
    
    std::string ep = endpoint;
    if (!ep.empty() && ep.front() != '/') ep = "/" + ep;
    
    return url + "/api" + ep;
}

void PwnDocClient::ensure_token() {
    if (token_.empty()) {
        if (config_.username && config_.password) {
            authenticate();
        } else {
            throw std::runtime_error("No authentication credentials provided");
        }
    }
}

void PwnDocClient::authenticate() {
    json login_data = {
        {"username", *config_.username},
        {"password", *config_.password}
    };
    
    std::string url = build_url("/users/login");
    std::string response_data;
    
    curl_easy_reset(curl_);
    curl_easy_setopt(curl_, CURLOPT_URL, url.c_str());
    curl_easy_setopt(curl_, CURLOPT_POST, 1L);
    
    std::string body = login_data.dump();
    curl_easy_setopt(curl_, CURLOPT_POSTFIELDS, body.c_str());
    
    struct curl_slist* headers = nullptr;
    headers = curl_slist_append(headers, "Content-Type: application/json");
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
        throw std::runtime_error(std::string("Authentication failed: ") + curl_easy_strerror(res));
    }
    
    json response = json::parse(response_data);
    if (response.contains("datas") && response["datas"].contains("token")) {
        token_ = response["datas"]["token"].get<std::string>();
    } else {
        throw std::runtime_error("Failed to get token from login response");
    }
}

json PwnDocClient::request(const std::string& method, 
                           const std::string& endpoint,
                           const json& data) {
    ensure_token();
    
    std::string url = build_url(endpoint);
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
    
    // Set body for POST/PUT
    std::string body;
    if (!data.empty() && (method == "POST" || method == "PUT")) {
        body = data.dump();
        curl_easy_setopt(curl_, CURLOPT_POSTFIELDS, body.c_str());
    }
    
    // Set headers
    struct curl_slist* headers = nullptr;
    headers = curl_slist_append(headers, "Content-Type: application/json");
    std::string auth_header = "Authorization: JWT " + token_;
    headers = curl_slist_append(headers, auth_header.c_str());
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
        throw std::runtime_error(std::string("Request failed: ") + curl_easy_strerror(res));
    }
    
    long http_code = 0;
    curl_easy_getinfo(curl_, CURLINFO_RESPONSE_CODE, &http_code);
    
    if (http_code >= 400) {
        throw std::runtime_error("HTTP error: " + std::to_string(http_code));
    }
    
    return json::parse(response_data);
}

json PwnDocClient::get(const std::string& endpoint) {
    return request("GET", endpoint);
}

json PwnDocClient::post(const std::string& endpoint, const json& data) {
    return request("POST", endpoint, data);
}

json PwnDocClient::put(const std::string& endpoint, const json& data) {
    return request("PUT", endpoint, data);
}

json PwnDocClient::del(const std::string& endpoint) {
    return request("DELETE", endpoint);
}

json PwnDocClient::test_connection() {
    try {
        ensure_token();
        json user = get("/users/me");
        return {
            {"status", "ok"},
            {"user", user["datas"]["username"]},
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
