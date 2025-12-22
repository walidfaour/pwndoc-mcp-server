#pragma once

#include <string>
#include <vector>
#include <optional>

/**
 * Configuration for PwnDoc MCP Server
 */
struct Config {
    std::string url;
    std::optional<std::string> token;
    std::optional<std::string> username;
    std::optional<std::string> password;
    bool verify_ssl = true;
    int timeout = 30;

    // Rate limiting
    int rate_limit_max_requests = 100;
    int rate_limit_period = 60;

    // Logging (0 = INFO, 1 = WARNING, -1 = DEBUG)
    int log_level = 0;

    // Retry configuration
    int max_retries = 3;
    double retry_delay = 1.0;
    
    /**
     * Load configuration from environment and file
     */
    static Config load();
    
    /**
     * Load from environment variables
     */
    static Config from_env();
    
    /**
     * Load from config file
     */
    static Config from_file(const std::string& path);
    
    /**
     * Get default config file path
     */
    static std::string get_config_path();
    
    /**
     * Validate configuration
     * @return vector of error messages (empty if valid)
     */
    std::vector<std::string> validate() const;
};
