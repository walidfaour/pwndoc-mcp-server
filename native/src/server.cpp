#include "server.hpp"
#include "tools.hpp"
#include <iostream>
#include <nlohmann/json.hpp>

using json = nlohmann::json;

Server::Server(const Config& config) : config_(config) {
    client_ = std::make_unique<PwnDocClient>(config);
}

Server::~Server() = default;

std::string Server::read_line() {
    std::string line;
    std::getline(std::cin, line);
    return line;
}

void Server::write_line(const std::string& line) {
    std::cout << line << std::endl;
    std::cout.flush();
}

void Server::run() {
    while (std::cin) {
        std::string line = read_line();
        if (line.empty()) continue;
        
        try {
            std::string response = handle_request(line);
            write_line(response);
        } catch (const std::exception& e) {
            json error_response = {
                {"jsonrpc", "2.0"},
                {"error", {
                    {"code", -32603},
                    {"message", e.what()}
                }}
            };
            write_line(error_response.dump());
        }
    }
}

std::string Server::handle_request(const std::string& request) {
    json req = json::parse(request);
    
    std::string method = req.value("method", "");
    json params = req.value("params", json::object());
    auto id = req.value("id", json());
    
    json result;
    
    if (method == "initialize") {
        result = {
            {"protocolVersion", "2024-11-05"},
            {"capabilities", {
                {"tools", json::object()}
            }},
            {"serverInfo", {
                {"name", "pwndoc-mcp-server"},
                {"version", "2.0.0"}
            }}
        };
    } else if (method == "tools/list") {
        result = {{"tools", get_tool_definitions()}};
    } else if (method == "tools/call") {
        std::string name = params.value("name", "");
        json arguments = params.value("arguments", json::object());
        result = handle_call_tool(name, arguments);
    } else if (method == "notifications/initialized") {
        // No response needed for notifications
        return "";
    } else {
        return json({
            {"jsonrpc", "2.0"},
            {"id", id},
            {"error", {
                {"code", -32601},
                {"message", "Method not found: " + method}
            }}
        }).dump();
    }
    
    return json({
        {"jsonrpc", "2.0"},
        {"id", id},
        {"result", result}
    }).dump();
}

std::string Server::handle_list_tools() {
    json tools = get_tool_definitions();
    return json({{"tools", tools}}).dump();
}

std::string Server::handle_call_tool(const std::string& name, const json& arguments) {
    try {
        json result = execute_tool(*client_, name, arguments);
        return json({
            {"content", json::array({
                {{"type", "text"}, {"text", result.dump(2)}}
            })}
        }).dump();
    } catch (const std::exception& e) {
        return json({
            {"content", json::array({
                {{"type", "text"}, {"text", json({{"error", e.what()}}).dump()}}
            })},
            {"isError", true}
        }).dump();
    }
}
