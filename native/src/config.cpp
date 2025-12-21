#include "config.hpp"
#include <cstdlib>
#include <fstream>
#include <nlohmann/json.hpp>

#ifdef _WIN32
#include <windows.h>
#include <shlobj.h>
#else
#include <unistd.h>
#include <pwd.h>
#endif

using json = nlohmann::json;

std::string Config::get_config_path() {
#ifdef _WIN32
    char path[MAX_PATH];
    if (SUCCEEDED(SHGetFolderPathA(NULL, CSIDL_PROFILE, NULL, 0, path))) {
        return std::string(path) + "\\.pwndoc-mcp\\config.json";
    }
    return "";
#else
    const char* home = std::getenv("HOME");
    if (!home) {
        struct passwd* pw = getpwuid(getuid());
        home = pw ? pw->pw_dir : "/tmp";
    }
    return std::string(home) + "/.pwndoc-mcp/config.json";
#endif
}

Config Config::from_env() {
    Config config;
    
    if (const char* url = std::getenv("PWNDOC_URL")) {
        config.url = url;
    }
    
    if (const char* token = std::getenv("PWNDOC_TOKEN")) {
        config.token = token;
    }
    
    if (const char* username = std::getenv("PWNDOC_USERNAME")) {
        config.username = username;
    }
    
    if (const char* password = std::getenv("PWNDOC_PASSWORD")) {
        config.password = password;
    }
    
    if (const char* verify = std::getenv("PWNDOC_VERIFY_SSL")) {
        config.verify_ssl = (std::string(verify) == "true" || std::string(verify) == "1");
    }
    
    if (const char* timeout = std::getenv("PWNDOC_TIMEOUT")) {
        config.timeout = std::atoi(timeout);
    }
    
    return config;
}

Config Config::from_file(const std::string& path) {
    Config config;
    
    std::ifstream file(path);
    if (!file.is_open()) {
        return config;
    }
    
    try {
        json data = json::parse(file);
        
        if (data.contains("url")) config.url = data["url"].get<std::string>();
        if (data.contains("token")) config.token = data["token"].get<std::string>();
        if (data.contains("username")) config.username = data["username"].get<std::string>();
        if (data.contains("password")) config.password = data["password"].get<std::string>();
        if (data.contains("verify_ssl")) config.verify_ssl = data["verify_ssl"].get<bool>();
        if (data.contains("timeout")) config.timeout = data["timeout"].get<int>();
    } catch (const json::exception&) {
        // Invalid JSON, return empty config
    }
    
    return config;
}

Config Config::load() {
    // Start with file config
    Config config = from_file(get_config_path());
    
    // Override with environment variables
    Config env = from_env();
    
    if (!env.url.empty()) config.url = env.url;
    if (env.token) config.token = env.token;
    if (env.username) config.username = env.username;
    if (env.password) config.password = env.password;
    
    // These are always overridden if set in env
    if (std::getenv("PWNDOC_VERIFY_SSL")) config.verify_ssl = env.verify_ssl;
    if (std::getenv("PWNDOC_TIMEOUT")) config.timeout = env.timeout;
    
    return config;
}

std::vector<std::string> Config::validate() const {
    std::vector<std::string> errors;
    
    if (url.empty()) {
        errors.push_back("PWNDOC_URL is required");
    }
    
    if (!token && !(username && password)) {
        errors.push_back("Either PWNDOC_TOKEN or PWNDOC_USERNAME/PWNDOC_PASSWORD required");
    }
    
    return errors;
}
