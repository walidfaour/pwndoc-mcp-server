/**
 * PwnDoc MCP Server - Native C++ Implementation
 * Entry point
 */

#include <iostream>
#include <string>
#include <vector>
#include <cstring>

#ifdef _WIN32
#include <windows.h>
#endif

#include "server.hpp"
#include "config.hpp"

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
    std::cout << "  serve            Start the MCP server" << std::endl;
    std::cout << "  version          Show version information" << std::endl;
    std::cout << std::endl;
    std::cout << "Configuration:" << std::endl;
    std::cout << "  Set environment variables:" << std::endl;
    std::cout << "    PWNDOC_URL                 PwnDoc server URL (required)" << std::endl;
    std::cout << "    PWNDOC_USERNAME            PwnDoc username" << std::endl;
    std::cout << "    PWNDOC_PASSWORD            PwnDoc password" << std::endl;
    std::cout << "    PWNDOC_TOKEN               PwnDoc JWT token" << std::endl;
    std::cout << std::endl;
    std::cout << "Examples:" << std::endl;
    std::cout << "  pwndoc-mcp-server serve" << std::endl;
    std::cout << "  pwndoc-mcp-server --version" << std::endl;
}

void print_banner() {
    std::cout << "=======================================" << std::endl;
    std::cout << "  PwnDoc MCP Server v" << PWNDOC_VERSION << " (Native)  " << std::endl;
    std::cout << "=======================================" << std::endl;
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
            std::cout << "Tools available: 89" << std::endl;
            std::cout << "Starting MCP server..." << std::endl;

            // Create and run server
            Server server(config);
            server.run();

            return 0;
        }

        // Unknown command
        std::cerr << "Error: Unknown command '" << argv[1] << "'" << std::endl;
        std::cerr << "Run 'pwndoc-mcp-server --help' for usage information." << std::endl;
        return 1;

    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
}
