#pragma once

#include "config.hpp"
#include "client.hpp"
#include <string>
#include <functional>
#include <map>

/**
 * MCP Server implementation
 */
class Server {
public:
    explicit Server(const Config& config);
    ~Server();
    
    /**
     * Run the MCP server (stdio transport)
     */
    void run();

private:
    Config config_;
    std::unique_ptr<PwnDocClient> client_;
    
    /**
     * Handle incoming JSON-RPC request
     */
    std::string handle_request(const std::string& request);
    
    /**
     * Handle tools/list request
     */
    std::string handle_list_tools();
    
    /**
     * Handle tools/call request
     */
    std::string handle_call_tool(const std::string& name, const nlohmann::json& arguments);
    
    /**
     * Read a line from stdin
     */
    std::string read_line();
    
    /**
     * Write a line to stdout
     */
    void write_line(const std::string& line);
};
