/**
 * PwnDoc MCP Server - Native C++ Implementation
 * Entry point
 */

#include <iostream>
#include <string>
#include "server.hpp"
#include "config.hpp"

void print_banner() {
    std::cout << R"(
╔═══════════════════════════════════════╗
║   PwnDoc MCP Server v2.0.0 (Native)   ║
╚═══════════════════════════════════════╝
)" << std::endl;
}

int main(int argc, char* argv[]) {
    try {
        print_banner();
        
        // Load configuration
        Config config = Config::load();
        
        auto errors = config.validate();
        if (!errors.empty()) {
            std::cerr << "Configuration errors:" << std::endl;
            for (const auto& error : errors) {
                std::cerr << "  - " << error << std::endl;
            }
            return 1;
        }
        
        std::cout << "Connecting to: " << config.url << std::endl;
        std::cout << "Tools available: 89" << std::endl;
        std::cout << "Starting MCP server..." << std::endl;
        
        // Create and run server
        Server server(config);
        server.run();
        
        return 0;
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
}
