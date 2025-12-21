#pragma once

#include "client.hpp"
#include <nlohmann/json.hpp>
#include <vector>

/**
 * Get all tool definitions for MCP
 */
nlohmann::json get_tool_definitions();

/**
 * Execute a tool by name
 */
nlohmann::json execute_tool(PwnDocClient& client, 
                            const std::string& name, 
                            const nlohmann::json& arguments);
