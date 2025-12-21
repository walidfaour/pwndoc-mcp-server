"""
Tests for the MCP server module.
"""

import pytest
import json
from unittest.mock import AsyncMock, patch, MagicMock

from pwndoc_mcp_server.server import PwnDocMCPServer
from pwndoc_mcp_server.config import Config


class TestToolDefinitions:
    """Tests for tool definitions."""
    
    def test_tool_definitions_exist(self):
        """Test that tool definitions are defined."""
        assert TOOL_DEFINITIONS is not None
        assert len(TOOL_DEFINITIONS) > 0
    
    def test_tool_definition_structure(self):
        """Test tool definition structure."""
        for tool in TOOL_DEFINITIONS:
            assert "name" in tool
            assert "description" in tool
            assert "inputSchema" in tool
            
            # Check input schema structure
            schema = tool["inputSchema"]
            assert "type" in schema
            assert schema["type"] == "object"
            assert "properties" in schema
    
    def test_audit_tools_exist(self):
        """Test that audit tools are defined."""
        tool_names = [t["name"] for t in TOOL_DEFINITIONS]
        
        expected_audit_tools = [
            "list_audits",
            "get_audit",
            "create_audit",
            "update_audit_general",
            "delete_audit",
            "generate_audit_report",
        ]
        
        for tool in expected_audit_tools:
            assert tool in tool_names, f"Missing tool: {tool}"
    
    def test_finding_tools_exist(self):
        """Test that finding tools are defined."""
        tool_names = [t["name"] for t in TOOL_DEFINITIONS]
        
        expected_finding_tools = [
            "get_audit_findings",
            "get_finding",
            "create_finding",
            "update_finding",
            "delete_finding",
        ]
        
        for tool in expected_finding_tools:
            assert tool in tool_names, f"Missing tool: {tool}"
    
    def test_client_tools_exist(self):
        """Test that client tools are defined."""
        tool_names = [t["name"] for t in TOOL_DEFINITIONS]
        
        expected_client_tools = [
            "list_clients",
            "create_client",
            "update_client",
            "delete_client",
        ]
        
        for tool in expected_client_tools:
            assert tool in tool_names, f"Missing tool: {tool}"
    
    def test_special_tools_exist(self):
        """Test that special aggregate tools are defined."""
        tool_names = [t["name"] for t in TOOL_DEFINITIONS]
        
        assert "get_all_findings_with_context" in tool_names
        assert "search_findings" in tool_names
        assert "get_statistics" in tool_names


class TestPwnDocMCPServer:
    """Tests for the PwnDocMCPServer class."""
    
    @pytest.fixture
    def config(self):
        """Create test configuration."""
        return Config(
            url="https://pwndoc.test.com",
            token="test-jwt-token"
        )
    
    @pytest.fixture
    def server(self, config):
        """Create test server."""
        return PwnDocMCPServer(config)
    
    def test_server_initialization(self, server, config):
        """Test server initialization."""
        assert server.config == config
        assert server.client is not None
    
    def test_server_name(self, server):
        """Test server name."""
        assert server.name == "pwndoc-mcp-server"
    
    def test_server_version(self, server):
        """Test server version."""
        assert hasattr(server, "version")
        assert server.version is not None
    
    @pytest.mark.asyncio
    async def test_handle_list_tools(self, server):
        """Test handling list_tools request."""
        result = await server.handle_list_tools()
        
        assert isinstance(result, list)
        assert len(result) > 0
        
        # Verify structure
        for tool in result:
            assert "name" in tool
            assert "description" in tool
    
    @pytest.mark.asyncio
    async def test_handle_call_tool_list_audits(self, server, mock_audit):
        """Test calling list_audits tool."""
        with patch.object(server.client, "list_audits") as mock_list:
            mock_list.return_value = [mock_audit]
            
            result = await server.handle_call_tool("list_audits", {})
            
            assert result is not None
            mock_list.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_handle_call_tool_get_audit(self, server, mock_audit):
        """Test calling get_audit tool."""
        audit_id = mock_audit["_id"]
        
        with patch.object(server.client, "get_audit") as mock_get:
            mock_get.return_value = mock_audit
            
            result = await server.handle_call_tool("get_audit", {"audit_id": audit_id})
            
            assert result is not None
            mock_get.assert_called_once_with(audit_id)
    
    @pytest.mark.asyncio
    async def test_handle_call_tool_create_audit(self, server):
        """Test calling create_audit tool."""
        with patch.object(server.client, "create_audit") as mock_create:
            mock_create.return_value = {"_id": "new-id", "name": "New Audit"}
            
            result = await server.handle_call_tool("create_audit", {
                "name": "New Audit",
                "audit_type": "Web Application",
                "language": "en"
            })
            
            assert result is not None
            mock_create.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_handle_call_tool_get_statistics(self, server, mock_statistics):
        """Test calling get_statistics tool."""
        with patch.object(server.client, "get_statistics") as mock_stats:
            mock_stats.return_value = mock_statistics
            
            result = await server.handle_call_tool("get_statistics", {})
            
            assert result is not None
            mock_stats.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_handle_call_tool_unknown(self, server):
        """Test calling unknown tool."""
        with pytest.raises(ValueError, match="Unknown tool"):
            await server.handle_call_tool("unknown_tool", {})
    
    @pytest.mark.asyncio
    async def test_handle_call_tool_with_filter(self, server, mock_audit):
        """Test calling list_audits with filter."""
        with patch.object(server.client, "list_audits") as mock_list:
            mock_list.return_value = [mock_audit]
            
            result = await server.handle_call_tool("list_audits", {
                "finding_title": "SQL Injection"
            })
            
            assert result is not None
            mock_list.assert_called_once()


class TestCreateServer:
    """Tests for create_server factory function."""
    
    def test_create_server_with_config(self):
        """Test creating server with config object."""
        config = Config(
            url="https://pwndoc.test.com",
            token="test-token"
        )
        
        server = create_server(config)
        
        assert isinstance(server, PwnDocMCPServer)
        assert server.config == config
    
    def test_create_server_with_kwargs(self):
        """Test creating server with kwargs."""
        server = create_server(
            url="https://pwndoc.test.com",
            token="test-token"
        )
        
        assert isinstance(server, PwnDocMCPServer)
        assert server.config.url == "https://pwndoc.test.com"
    
    def test_create_server_invalid_config(self):
        """Test creating server with invalid config raises error."""
        config = Config()  # Empty config
        
        with pytest.raises(ValueError, match="Invalid configuration"):
            create_server(config)


class TestToolResultFormatting:
    """Tests for tool result formatting."""
    
    @pytest.fixture
    def server(self):
        """Create test server."""
        config = Config(
            url="https://pwndoc.test.com",
            token="test-token"
        )
        return PwnDocMCPServer(config)
    
    def test_format_result_dict(self, server):
        """Test formatting dictionary result."""
        data = {"key": "value", "count": 42}
        result = server._format_result(data)
        
        assert isinstance(result, str)
        parsed = json.loads(result)
        assert parsed["key"] == "value"
    
    def test_format_result_list(self, server):
        """Test formatting list result."""
        data = [{"id": 1}, {"id": 2}]
        result = server._format_result(data)
        
        assert isinstance(result, str)
        parsed = json.loads(result)
        assert len(parsed) == 2
    
    def test_format_result_string(self, server):
        """Test formatting string result."""
        data = "Success message"
        result = server._format_result(data)
        
        assert result == "Success message"
    
    def test_format_result_none(self, server):
        """Test formatting None result."""
        result = server._format_result(None)
        
        assert result == "null" or result is None


class TestServerTransports:
    """Tests for server transport options."""
    
    @pytest.fixture
    def config(self):
        """Create test configuration."""
        return Config(
            url="https://pwndoc.test.com",
            token="test-token"
        )
    
    def test_stdio_transport_setup(self, config):
        """Test stdio transport can be configured."""
        server = PwnDocMCPServer(config, transport="stdio")
        
        assert server.transport == "stdio"
    
    def test_sse_transport_setup(self, config):
        """Test SSE transport can be configured."""
        server = PwnDocMCPServer(config, transport="sse")
        
        assert server.transport == "sse"
    
    def test_invalid_transport(self, config):
        """Test invalid transport raises error."""
        with pytest.raises(ValueError, match="Invalid transport"):
            PwnDocMCPServer(config, transport="invalid")


class TestServerProtocol:
    """Tests for MCP protocol handling."""
    
    @pytest.fixture
    def server(self):
        """Create test server."""
        config = Config(
            url="https://pwndoc.test.com",
            token="test-token"
        )
        return PwnDocMCPServer(config)
    
    @pytest.mark.asyncio
    async def test_handle_initialize(self, server):
        """Test handling initialize request."""
        result = await server.handle_initialize({
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "test", "version": "1.0"}
        })
        
        assert "protocolVersion" in result
        assert "capabilities" in result
        assert "serverInfo" in result
    
    @pytest.mark.asyncio
    async def test_protocol_version(self, server):
        """Test protocol version compatibility."""
        result = await server.handle_initialize({
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "test", "version": "1.0"}
        })
        
        assert result["protocolVersion"] == "2024-11-05"
    
    @pytest.mark.asyncio
    async def test_server_capabilities(self, server):
        """Test server capabilities reporting."""
        result = await server.handle_initialize({
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "test", "version": "1.0"}
        })
        
        capabilities = result["capabilities"]
        assert "tools" in capabilities
