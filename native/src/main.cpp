/**
 * PwnDoc MCP Server - Native C++ Implementation
 * Entry point
 */

#include <iostream>
#include <string>
#include <vector>
#include <cstring>
#include <fstream>
#include <sstream>

#ifdef _WIN32
#include <windows.h>
#include <shlobj.h>
#else
#include <unistd.h>
#include <sys/stat.h>
#include <pwd.h>
#endif

#include "server.hpp"
#include "config.hpp"
#include "client.hpp"
#include "tools.hpp"

// Version info from CMake
#ifndef PWNDOC_VERSION
#define PWNDOC_VERSION "1.0.3"
#endif

#ifndef PWNDOC_AUTHOR
#define PWNDOC_AUTHOR "Walid Faour"
#endif

#ifndef PWNDOC_EMAIL
#define PWNDOC_EMAIL "security@walidfaour.com"
#endif

void setup_console_utf8() {
#ifdef _WIN32
    // Set console to UTF-8 on Windows
    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);
#endif
}

void print_version() {
    std::cout << "pwndoc-mcp-server version " << PWNDOC_VERSION << std::endl;
    std::cout << "Author: " << PWNDOC_AUTHOR << " <" << PWNDOC_EMAIL << ">" << std::endl;
}

void print_help() {
    std::cout << "Usage: pwndoc-mcp-server [OPTIONS] COMMAND [ARGS]..." << std::endl;
    std::cout << std::endl;
    std::cout << "PwnDoc MCP Server - Model Context Protocol for Pentest Documentation" << std::endl;
    std::cout << std::endl;
    std::cout << "Options:" << std::endl;
    std::cout << "  --version, -v    Show version and exit" << std::endl;
    std::cout << "  --help           Show this message and exit" << std::endl;
    std::cout << std::endl;
    std::cout << "Commands:" << std::endl;
    std::cout << "  serve            Start the MCP server (stdio transport)" << std::endl;
    std::cout << "  test             Test connection to PwnDoc server" << std::endl;
    std::cout << "  tools            List all available MCP tools" << std::endl;
    std::cout << "  version          Show version information" << std::endl;
    std::cout << "  config init      Interactive configuration wizard" << std::endl;
    std::cout << "  claude-install   Install MCP config for Claude Desktop" << std::endl;
    std::cout << "  claude-status    Check Claude Desktop installation status" << std::endl;
    std::cout << "  claude-uninstall Remove MCP config from Claude Desktop" << std::endl;
    std::cout << std::endl;
    std::cout << "Configuration:" << std::endl;
    std::cout << "  Set environment variables:" << std::endl;
    std::cout << "    PWNDOC_URL                 PwnDoc server URL (required)" << std::endl;
    std::cout << "    PWNDOC_USERNAME            PwnDoc username" << std::endl;
    std::cout << "    PWNDOC_PASSWORD            PwnDoc password" << std::endl;
    std::cout << "    PWNDOC_TOKEN               PwnDoc JWT token" << std::endl;
    std::cout << std::endl;
    std::cout << "Examples:" << std::endl;
    std::cout << "  pwndoc-mcp-server test" << std::endl;
    std::cout << "  pwndoc-mcp-server tools" << std::endl;
    std::cout << "  pwndoc-mcp-server config init" << std::endl;
    std::cout << "  pwndoc-mcp-server claude-install" << std::endl;
    std::cout << "  pwndoc-mcp-server serve" << std::endl;
}

void print_banner() {
    std::cout << "=======================================" << std::endl;
    std::cout << "  PwnDoc MCP Server v" << PWNDOC_VERSION << " (Native)  " << std::endl;
    std::cout << "=======================================" << std::endl;
}

// Get home directory path
std::string get_home_dir() {
#ifdef _WIN32
    char path[MAX_PATH];
    if (SUCCEEDED(SHGetFolderPathA(NULL, CSIDL_PROFILE, NULL, 0, path))) {
        return std::string(path);
    }
    return "";
#else
    const char* home = getenv("HOME");
    if (home) return std::string(home);
    struct passwd* pw = getpwuid(getuid());
    if (pw) return std::string(pw->pw_dir);
    return "";
#endif
}

// Get Claude Desktop config path
std::string get_claude_config_path() {
#ifdef _WIN32
    return get_home_dir() + "\\AppData\\Roaming\\Claude\\claude_desktop_config.json";
#elif defined(__APPLE__)
    return get_home_dir() + "/Library/Application Support/Claude/claude_desktop_config.json";
#else
    return get_home_dir() + "/.config/Claude/claude_desktop_config.json";
#endif
}

// Check if file exists
bool file_exists(const std::string& path) {
    std::ifstream file(path);
    return file.good();
}

// Test connection command
int cmd_test() {
    try {
        print_banner();
        std::cout << "Testing connection to PwnDoc server..." << std::endl;
        std::cout << std::endl;

        Config config = Config::load();
        auto errors = config.validate();
        if (!errors.empty()) {
            std::cerr << "Configuration errors:" << std::endl;
            for (const auto& error : errors) {
                std::cerr << "  ✗ " << error << std::endl;
            }
            return 1;
        }

        PwnDocClient client(config);
        auto result = client.test_connection();

        if (result.contains("status") && result["status"] == "ok") {
            std::cout << "✓ Connection successful!" << std::endl;
            std::cout << "  URL: " << config.url << std::endl;
            if (result.contains("user")) {
                std::cout << "  User: " << result["user"].get<std::string>() << std::endl;
            }
            std::cout << "  Authentication: ✓" << std::endl;
            return 0;
        } else {
            std::cerr << "✗ Connection failed!" << std::endl;
            if (result.contains("error")) {
                std::cerr << "  Error: " << result["error"].get<std::string>() << std::endl;
            }
            return 1;
        }
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
}

// List tools command
int cmd_tools() {
    try {
        print_banner();
        std::cout << "Available MCP Tools (90 total):" << std::endl;
        std::cout << std::endl;

        auto tools = get_tool_definitions();

        std::map<std::string, std::vector<nlohmann::json>> categories;
        categories["Audits"] = {};
        categories["Findings"] = {};
        categories["Clients & Companies"] = {};
        categories["Vulnerabilities"] = {};
        categories["Users"] = {};
        categories["Settings & Templates"] = {};
        categories["Languages"] = {};
        categories["Audit Types"] = {};
        categories["Vulnerability Types"] = {};
        categories["Vulnerability Categories"] = {};
        categories["Sections"] = {};
        categories["Custom Fields"] = {};
        categories["Roles"] = {};
        categories["Images"] = {};
        categories["Statistics"] = {};

        // Categorize tools
        for (const auto& tool : tools) {
            std::string name = tool["name"].get<std::string>();
            if (name.find("audit") != std::string::npos && name.find("type") == std::string::npos) {
                categories["Audits"].push_back(tool);
            } else if (name.find("finding") != std::string::npos) {
                categories["Findings"].push_back(tool);
            } else if (name.find("client") != std::string::npos || name.find("compan") != std::string::npos) {
                categories["Clients & Companies"].push_back(tool);
            } else if (name.find("vulnerabilit") != std::string::npos && name.find("type") == std::string::npos && name.find("categor") == std::string::npos) {
                categories["Vulnerabilities"].push_back(tool);
            } else if (name.find("user") != std::string::npos || name.find("totp") != std::string::npos || name.find("reviewer") != std::string::npos) {
                categories["Users"].push_back(tool);
            } else if (name.find("template") != std::string::npos || name.find("setting") != std::string::npos) {
                categories["Settings & Templates"].push_back(tool);
            } else if (name.find("language") != std::string::npos) {
                categories["Languages"].push_back(tool);
            } else if (name.find("audit_type") != std::string::npos || name == "list_audit_types" || name == "create_audit_type" || name == "update_audit_type" || name == "delete_audit_type") {
                categories["Audit Types"].push_back(tool);
            } else if (name.find("vulnerability_type") != std::string::npos) {
                categories["Vulnerability Types"].push_back(tool);
            } else if (name.find("vulnerability_categor") != std::string::npos || name.find("categor") != std::string::npos) {
                categories["Vulnerability Categories"].push_back(tool);
            } else if (name.find("section") != std::string::npos) {
                categories["Sections"].push_back(tool);
            } else if (name.find("custom_field") != std::string::npos) {
                categories["Custom Fields"].push_back(tool);
            } else if (name.find("role") != std::string::npos) {
                categories["Roles"].push_back(tool);
            } else if (name.find("image") != std::string::npos) {
                categories["Images"].push_back(tool);
            } else if (name.find("statistic") != std::string::npos) {
                categories["Statistics"].push_back(tool);
            }
        }

        // Print categorized tools
        for (const auto& [category, tool_list] : categories) {
            if (!tool_list.empty()) {
                std::cout << category << " (" << tool_list.size() << " tools):" << std::endl;
                for (const auto& tool : tool_list) {
                    std::cout << "  • " << tool["name"].get<std::string>();
                    if (tool.contains("description")) {
                        std::string desc = tool["description"].get<std::string>();
                        if (desc.length() > 60) {
                            desc = desc.substr(0, 57) + "...";
                        }
                        std::cout << " - " << desc;
                    }
                    std::cout << std::endl;
                }
                std::cout << std::endl;
            }
        }

        std::cout << "Total: " << tools.size() << " MCP tools" << std::endl;
        return 0;
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
}

// Config init command
int cmd_config_init() {
    std::cout << "=== PwnDoc MCP Server Configuration ===" << std::endl;
    std::cout << std::endl;
    std::cout << "This wizard will help you configure the PwnDoc MCP server." << std::endl;
    std::cout << std::endl;

    std::string url, username, password, token;
    std::string verify_ssl, use_token;

    std::cout << "PwnDoc Server URL: ";
    std::getline(std::cin, url);

    std::cout << "Use pre-authenticated token? (y/n) [n]: ";
    std::getline(std::cin, use_token);

    if (use_token == "y" || use_token == "Y") {
        std::cout << "JWT Token: ";
        std::getline(std::cin, token);
    } else {
        std::cout << "Username: ";
        std::getline(std::cin, username);
        std::cout << "Password: ";
        std::getline(std::cin, password);
    }

    std::cout << "Verify SSL certificates? (y/n) [y]: ";
    std::getline(std::cin, verify_ssl);

    std::cout << std::endl;
    std::cout << "Configuration Summary:" << std::endl;
    std::cout << "  URL: " << url << std::endl;
    if (!token.empty()) {
        std::cout << "  Auth: JWT Token" << std::endl;
    } else {
        std::cout << "  Auth: Username/Password" << std::endl;
        std::cout << "  Username: " << username << std::endl;
    }
    std::cout << "  Verify SSL: " << (verify_ssl == "n" || verify_ssl == "N" ? "No" : "Yes") << std::endl;
    std::cout << std::endl;
    std::cout << "Set these environment variables:" << std::endl;
    std::cout << "  export PWNDOC_URL=\"" << url << "\"" << std::endl;
    if (!token.empty()) {
        std::cout << "  export PWNDOC_TOKEN=\"" << token << "\"" << std::endl;
    } else {
        std::cout << "  export PWNDOC_USERNAME=\"" << username << "\"" << std::endl;
        std::cout << "  export PWNDOC_PASSWORD=\"" << password << "\"" << std::endl;
    }
    if (verify_ssl == "n" || verify_ssl == "N") {
        std::cout << "  export PWNDOC_VERIFY_SSL=\"false\"" << std::endl;
    }
    std::cout << std::endl;

    return 0;
}

// Claude install command
int cmd_claude_install() {
    std::cout << "=== Installing PwnDoc MCP for Claude Desktop ===" << std::endl;
    std::cout << std::endl;

    std::string config_path = get_claude_config_path();
    std::cout << "Config file: " << config_path << std::endl;
    std::cout << std::endl;

    // Get current executable path
    std::string exe_path;
#ifdef _WIN32
    char buffer[MAX_PATH];
    GetModuleFileNameA(NULL, buffer, MAX_PATH);
    exe_path = buffer;
#else
    char buffer[1024];
    ssize_t len = readlink("/proc/self/exe", buffer, sizeof(buffer) - 1);
    if (len != -1) {
        buffer[len] = '\0';
        exe_path = buffer;
    } else {
        std::cerr << "Error: Could not determine executable path" << std::endl;
        return 1;
    }
#endif

    std::cout << "Executable: " << exe_path << std::endl;
    std::cout << std::endl;
    std::cout << "Add this configuration to Claude Desktop:" << std::endl;
    std::cout << std::endl;
    std::cout << "{" << std::endl;
    std::cout << "  \"mcpServers\": {" << std::endl;
    std::cout << "    \"pwndoc\": {" << std::endl;
    std::cout << "      \"command\": \"" << exe_path << "\"," << std::endl;
    std::cout << "      \"env\": {" << std::endl;
    std::cout << "        \"PWNDOC_URL\": \"https://your-pwndoc.com\"," << std::endl;
    std::cout << "        \"PWNDOC_USERNAME\": \"your-username\"," << std::endl;
    std::cout << "        \"PWNDOC_PASSWORD\": \"your-password\"" << std::endl;
    std::cout << "      }" << std::endl;
    std::cout << "    }" << std::endl;
    std::cout << "  }" << std::endl;
    std::cout << "}" << std::endl;
    std::cout << std::endl;
    std::cout << "Manual installation:" << std::endl;
    std::cout << "1. Edit: " << config_path << std::endl;
    std::cout << "2. Add the configuration above to the mcpServers section" << std::endl;
    std::cout << "3. Update PWNDOC_URL, PWNDOC_USERNAME, and PWNDOC_PASSWORD" << std::endl;
    std::cout << "4. Restart Claude Desktop" << std::endl;
    std::cout << std::endl;

    return 0;
}

// Claude status command
int cmd_claude_status() {
    std::cout << "=== Claude Desktop Installation Status ===" << std::endl;
    std::cout << std::endl;

    std::string config_path = get_claude_config_path();
    std::cout << "Config file: " << config_path << std::endl;

    if (file_exists(config_path)) {
        std::cout << "Status: ✓ File exists" << std::endl;
        std::cout << std::endl;
        std::cout << "Check if 'pwndoc' is configured in the mcpServers section." << std::endl;
    } else {
        std::cout << "Status: ✗ File not found" << std::endl;
        std::cout << std::endl;
        std::cout << "Run 'pwndoc-mcp-server claude-install' for installation instructions." << std::endl;
    }
    std::cout << std::endl;

    return 0;
}

// Claude uninstall command
int cmd_claude_uninstall() {
    std::cout << "=== Uninstalling PwnDoc MCP from Claude Desktop ===" << std::endl;
    std::cout << std::endl;

    std::string config_path = get_claude_config_path();
    std::cout << "Config file: " << config_path << std::endl;
    std::cout << std::endl;
    std::cout << "Manual uninstallation:" << std::endl;
    std::cout << "1. Edit: " << config_path << std::endl;
    std::cout << "2. Remove the 'pwndoc' entry from mcpServers" << std::endl;
    std::cout << "3. Restart Claude Desktop" << std::endl;
    std::cout << std::endl;

    return 0;
}

int main(int argc, char* argv[]) {
    try {
        // Setup console for UTF-8
        setup_console_utf8();

        // Parse command line arguments
        std::vector<std::string> args;
        for (int i = 1; i < argc; i++) {
            args.push_back(argv[i]);
        }

        // Handle --version flag
        if (argc == 2 && (std::string(argv[1]) == "--version" || std::string(argv[1]) == "-v")) {
            print_version();
            return 0;
        }

        // Handle --help flag
        if (argc == 2 && std::string(argv[1]) == "--help") {
            print_help();
            return 0;
        }

        // Handle version command
        if (argc == 2 && std::string(argv[1]) == "version") {
            print_version();
            return 0;
        }

        // Handle test command
        if (argc == 2 && std::string(argv[1]) == "test") {
            return cmd_test();
        }

        // Handle tools command
        if (argc == 2 && std::string(argv[1]) == "tools") {
            return cmd_tools();
        }

        // Handle config init command
        if (argc == 3 && std::string(argv[1]) == "config" && std::string(argv[2]) == "init") {
            return cmd_config_init();
        }

        // Handle claude-install command
        if (argc == 2 && std::string(argv[1]) == "claude-install") {
            return cmd_claude_install();
        }

        // Handle claude-status command
        if (argc == 2 && std::string(argv[1]) == "claude-status") {
            return cmd_claude_status();
        }

        // Handle claude-uninstall command
        if (argc == 2 && std::string(argv[1]) == "claude-uninstall") {
            return cmd_claude_uninstall();
        }

        // Handle serve command (default if no args)
        if (argc == 1 || (argc == 2 && std::string(argv[1]) == "serve")) {
            print_banner();

            // Load configuration
            Config config = Config::load();

            auto errors = config.validate();
            if (!errors.empty()) {
                std::cerr << "Configuration errors:" << std::endl;
                for (const auto& error : errors) {
                    std::cerr << "  - " << error << std::endl;
                }
                std::cerr << std::endl;
                std::cerr << "Run 'pwndoc-mcp-server --help' for usage information." << std::endl;
                return 1;
            }

            std::cout << "Connecting to: " << config.url << std::endl;
            std::cout << "Tools available: 90" << std::endl;
            std::cout << "Starting MCP server..." << std::endl;

            // Create and run server
            Server server(config);
            server.run();

            return 0;
        }

        // Unknown command
        std::cerr << "Error: Unknown command";
        if (argc > 1) {
            std::cerr << " '" << argv[1];
            if (argc > 2) {
                for (int i = 2; i < argc; i++) {
                    std::cerr << " " << argv[i];
                }
            }
            std::cerr << "'";
        }
        std::cerr << std::endl;
        std::cerr << "Run 'pwndoc-mcp-server --help' for usage information." << std::endl;
        return 1;

    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
}
