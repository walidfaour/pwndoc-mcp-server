"""
PwnDoc MCP Server - Model Context Protocol implementation.

This module implements the MCP server that exposes PwnDoc functionality
to AI assistants like Claude through a standardized protocol.

Supports multiple transports:
- stdio: Standard input/output (default, for Claude Desktop)
- sse: Server-Sent Events (for web clients)
- websocket: WebSocket (for real-time applications)
"""

import asyncio
import json
import logging
import sys
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Union

from .client import PwnDocClient, PwnDocError
from .config import Config, load_config
from .version import get_version

logger = logging.getLogger(__name__)


@dataclass
class Tool:
    """MCP Tool definition."""

    name: str
    description: str
    parameters: Dict[str, Any]
    handler: Callable
    required: List[str] = field(default_factory=list)


@dataclass
class MCPMessage:
    """MCP protocol message."""

    jsonrpc: str = "2.0"
    id: Optional[Union[str, int]] = None
    method: Optional[str] = None
    params: Optional[Dict[str, Any]] = None
    result: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None


class PwnDocMCPServer:
    """
    Model Context Protocol server for PwnDoc.

    Exposes PwnDoc API functionality as MCP tools that can be called
    by AI assistants like Claude.

    Example:
        >>> server = PwnDocMCPServer(config)
        >>> server.run()  # Starts stdio transport
    """

    SERVER_NAME = "pwndoc-mcp-server"
    SERVER_VERSION = get_version()
    PROTOCOL_VERSION = "2024-11-05"

    def __init__(self, config: Optional[Config] = None, transport: Optional[str] = None):
        """
        Initialize MCP server.

        Args:
            config: Configuration object (loads from environment if not provided)
            transport: Transport type (stdio, sse, websocket)
        """
        self.config = config or load_config()
        self.transport = transport or self.config.mcp_transport

        # Validate transport
        valid_transports = ["stdio", "sse", "websocket"]
        if self.transport not in valid_transports:
            raise ValueError(f"Invalid transport: {self.transport}")

        self._client: Optional[PwnDocClient] = None
        self._tools: Dict[str, Tool] = {}
        self._initialized = False

        # Register all tools
        self._register_tools()

        logger.info(f"PwnDocMCPServer initialized with {len(self._tools)} tools")

    @property
    def name(self) -> str:
        """Get server name."""
        return self.SERVER_NAME

    @property
    def version(self) -> str:
        """Get server version."""
        return self.SERVER_VERSION

    @property
    def client(self) -> PwnDocClient:
        """Get or create PwnDoc client."""
        if self._client is None:
            self._client = PwnDocClient(self.config)
            self._client.authenticate()
        return self._client

    def _register_tools(self):
        """Register all available tools."""

        # =====================================================================
        # AUDIT TOOLS
        # =====================================================================

        self._register_tool(
            name="list_audits",
            description="List all audits/pentests. Can filter by finding title.",
            parameters={
                "type": "object",
                "properties": {
                    "finding_title": {
                        "type": "string",
                        "description": "Filter audits containing findings with this title (optional)",
                    }
                },
            },
            handler=self._handle_list_audits,
        )

        self._register_tool(
            name="get_audit",
            description="Get detailed information about a specific audit including all findings, scope, sections, and metadata.",
            parameters={
                "type": "object",
                "properties": {
                    "audit_id": {"type": "string", "description": "The audit ID (MongoDB ObjectId)"}
                },
                "required": ["audit_id"],
            },
            handler=self._handle_get_audit,
        )

        self._register_tool(
            name="create_audit",
            description="Create a new audit/pentest.",
            parameters={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Audit name"},
                    "language": {"type": "string", "description": "Language code (e.g., 'en')"},
                    "audit_type": {"type": "string", "description": "Type of audit"},
                },
                "required": ["name", "language", "audit_type"],
            },
            handler=self._handle_create_audit,
        )

        self._register_tool(
            name="update_audit_general",
            description="Update general information of an audit.",
            parameters={
                "type": "object",
                "properties": {
                    "audit_id": {"type": "string", "description": "The audit ID"},
                    "name": {"type": "string", "description": "Audit name"},
                    "client": {"type": "string", "description": "Client ID"},
                    "company": {"type": "string", "description": "Company ID"},
                    "date_start": {"type": "string", "description": "Start date (ISO format)"},
                    "date_end": {"type": "string", "description": "End date (ISO format)"},
                    "scope": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Scope items",
                    },
                },
                "required": ["audit_id"],
            },
            handler=self._handle_update_audit_general,
        )

        self._register_tool(
            name="delete_audit",
            description="Delete an audit permanently.",
            parameters={
                "type": "object",
                "properties": {
                    "audit_id": {"type": "string", "description": "The audit ID to delete"}
                },
                "required": ["audit_id"],
            },
            handler=self._handle_delete_audit,
        )

        self._register_tool(
            name="generate_audit_report",
            description="Generate and download the audit report (DOCX).",
            parameters={
                "type": "object",
                "properties": {"audit_id": {"type": "string", "description": "The audit ID"}},
                "required": ["audit_id"],
            },
            handler=self._handle_generate_report,
        )

        # =====================================================================
        # FINDING TOOLS
        # =====================================================================

        self._register_tool(
            name="get_audit_findings",
            description="Get all findings/vulnerabilities from a specific audit.",
            parameters={
                "type": "object",
                "properties": {"audit_id": {"type": "string", "description": "The audit ID"}},
                "required": ["audit_id"],
            },
            handler=self._handle_get_findings,
        )

        self._register_tool(
            name="get_finding",
            description="Get details of a specific finding in an audit.",
            parameters={
                "type": "object",
                "properties": {
                    "audit_id": {"type": "string", "description": "The audit ID"},
                    "finding_id": {"type": "string", "description": "The finding ID"},
                },
                "required": ["audit_id", "finding_id"],
            },
            handler=self._handle_get_finding,
        )

        self._register_tool(
            name="create_finding",
            description="Create a new finding in an audit.",
            parameters={
                "type": "object",
                "properties": {
                    "audit_id": {"type": "string", "description": "The audit ID"},
                    "title": {"type": "string", "description": "Finding title"},
                    "description": {"type": "string", "description": "Detailed description"},
                    "observation": {"type": "string", "description": "Observation/evidence"},
                    "remediation": {"type": "string", "description": "Remediation steps"},
                    "cvssv3": {"type": "string", "description": "CVSS v3 score/vector"},
                    "priority": {"type": "integer", "description": "Priority (1-4)"},
                    "category": {"type": "string", "description": "Category"},
                    "vuln_type": {"type": "string", "description": "Vulnerability type"},
                    "poc": {"type": "string", "description": "Proof of concept"},
                    "scope": {"type": "string", "description": "Affected scope"},
                    "references": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "References",
                    },
                },
                "required": ["audit_id", "title"],
            },
            handler=self._handle_create_finding,
        )

        self._register_tool(
            name="update_finding",
            description="Update an existing finding.",
            parameters={
                "type": "object",
                "properties": {
                    "audit_id": {"type": "string", "description": "The audit ID"},
                    "finding_id": {"type": "string", "description": "The finding ID"},
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                    "observation": {"type": "string"},
                    "remediation": {"type": "string"},
                    "cvssv3": {"type": "string"},
                    "priority": {"type": "integer"},
                    "category": {"type": "string"},
                    "vuln_type": {"type": "string"},
                    "poc": {"type": "string"},
                    "scope": {"type": "string"},
                    "references": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["audit_id", "finding_id"],
            },
            handler=self._handle_update_finding,
        )

        self._register_tool(
            name="delete_finding",
            description="Delete a finding from an audit.",
            parameters={
                "type": "object",
                "properties": {
                    "audit_id": {"type": "string", "description": "The audit ID"},
                    "finding_id": {"type": "string", "description": "The finding ID to delete"},
                },
                "required": ["audit_id", "finding_id"],
            },
            handler=self._handle_delete_finding,
        )

        self._register_tool(
            name="search_findings",
            description="Search for findings across all audits by various criteria.",
            parameters={
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Search by finding title"},
                    "category": {"type": "string", "description": "Filter by category"},
                    "severity": {
                        "type": "string",
                        "description": "Filter by severity (Critical, High, Medium, Low)",
                    },
                    "status": {"type": "string", "description": "Filter by status"},
                },
            },
            handler=self._handle_search_findings,
        )

        self._register_tool(
            name="get_all_findings_with_context",
            description="Get ALL findings from ALL audits with full context (company, dates, team, scope, description, CWE, references) in a single request.",
            parameters={
                "type": "object",
                "properties": {
                    "include_failed": {
                        "type": "boolean",
                        "description": "Include 'Failed' category findings (default: false)",
                    },
                    "exclude_categories": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Categories to exclude",
                    },
                },
            },
            handler=self._handle_get_all_findings_with_context,
        )

        # =====================================================================
        # CLIENT & COMPANY TOOLS
        # =====================================================================

        self._register_tool(
            name="list_clients",
            description="List all clients.",
            parameters={"type": "object", "properties": {}},
            handler=self._handle_list_clients,
        )

        self._register_tool(
            name="create_client",
            description="Create a new client.",
            parameters={
                "type": "object",
                "properties": {
                    "firstname": {"type": "string", "description": "First name"},
                    "lastname": {"type": "string", "description": "Last name"},
                    "email": {"type": "string", "description": "Client email"},
                    "phone": {"type": "string", "description": "Phone number"},
                    "cell": {"type": "string", "description": "Cell phone"},
                    "title": {"type": "string", "description": "Job title"},
                    "company": {"type": "string", "description": "Company ID"},
                },
                "required": ["email", "firstname", "lastname"],
            },
            handler=self._handle_create_client,
        )

        self._register_tool(
            name="update_client",
            description="Update an existing client.",
            parameters={
                "type": "object",
                "properties": {
                    "client_id": {"type": "string", "description": "Client ID"},
                    "firstname": {"type": "string", "description": "First name"},
                    "lastname": {"type": "string", "description": "Last name"},
                    "email": {"type": "string", "description": "Client email"},
                    "phone": {"type": "string", "description": "Phone number"},
                    "cell": {"type": "string", "description": "Cell phone"},
                    "title": {"type": "string", "description": "Job title"},
                    "company": {"type": "string", "description": "Company ID"},
                },
                "required": ["client_id"],
            },
            handler=self._handle_update_client,
        )

        self._register_tool(
            name="delete_client",
            description="Delete a client.",
            parameters={
                "type": "object",
                "properties": {
                    "client_id": {"type": "string", "description": "Client ID to delete"}
                },
                "required": ["client_id"],
            },
            handler=self._handle_delete_client,
        )

        self._register_tool(
            name="list_companies",
            description="List all companies.",
            parameters={"type": "object", "properties": {}},
            handler=self._handle_list_companies,
        )

        self._register_tool(
            name="create_company",
            description="Create a new company.",
            parameters={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Company name"},
                    "short_name": {"type": "string", "description": "Short name/abbreviation"},
                    "logo": {"type": "string", "description": "Logo (base64)"},
                },
                "required": ["name"],
            },
            handler=self._handle_create_company,
        )

        # =====================================================================
        # VULNERABILITY TEMPLATE TOOLS
        # =====================================================================

        self._register_tool(
            name="list_vulnerabilities",
            description="List all vulnerability templates in the library.",
            parameters={"type": "object", "properties": {}},
            handler=self._handle_list_vulnerabilities,
        )

        self._register_tool(
            name="get_vulnerabilities_by_locale",
            description="Get vulnerability templates for a specific language.",
            parameters={
                "type": "object",
                "properties": {
                    "locale": {
                        "type": "string",
                        "description": "Language code (e.g., 'en', 'fr')",
                        "default": "en",
                    }
                },
            },
            handler=self._handle_get_vulnerabilities_by_locale,
        )

        self._register_tool(
            name="create_vulnerability",
            description="Create a new vulnerability template.",
            parameters={
                "type": "object",
                "properties": {
                    "details": {"type": "object", "description": "Vulnerability details by locale"},
                    "cvssv3": {"type": "string", "description": "CVSS v3 score"},
                    "priority": {"type": "integer", "description": "Priority (1-4)"},
                    "remediation_complexity": {
                        "type": "integer",
                        "description": "Complexity (1-3)",
                    },
                    "category": {"type": "string", "description": "Category"},
                },
                "required": ["details"],
            },
            handler=self._handle_create_vulnerability,
        )

        # =====================================================================
        # USER TOOLS
        # =====================================================================

        self._register_tool(
            name="list_users",
            description="List all users (admin only).",
            parameters={"type": "object", "properties": {}},
            handler=self._handle_list_users,
        )

        self._register_tool(
            name="get_current_user",
            description="Get current authenticated user's info.",
            parameters={"type": "object", "properties": {}},
            handler=self._handle_get_current_user,
        )

        # =====================================================================
        # SETTINGS & DATA TOOLS
        # =====================================================================

        self._register_tool(
            name="list_templates",
            description="List all report templates.",
            parameters={"type": "object", "properties": {}},
            handler=self._handle_list_templates,
        )

        self._register_tool(
            name="list_languages",
            description="List all configured languages.",
            parameters={"type": "object", "properties": {}},
            handler=self._handle_list_languages,
        )

        self._register_tool(
            name="list_audit_types",
            description="List all audit types.",
            parameters={"type": "object", "properties": {}},
            handler=self._handle_list_audit_types,
        )

        self._register_tool(
            name="get_statistics",
            description="Get comprehensive statistics about audits, findings, clients, and more.",
            parameters={"type": "object", "properties": {}},
            handler=self._handle_get_statistics,
        )

    def _register_tool(
        self,
        name: str,
        description: str,
        parameters: Dict[str, Any],
        handler: Callable,
        required: Optional[List[str]] = None,
    ):
        """Register a tool."""
        self._tools[name] = Tool(
            name=name,
            description=description,
            parameters=parameters,
            handler=handler,
            required=required or parameters.get("required", []),
        )

    # =========================================================================
    # TOOL HANDLERS
    # =========================================================================

    def _handle_list_audits(self, finding_title: Optional[str] = None) -> List[Dict]:
        return self.client.list_audits(finding_title)

    def _handle_get_audit(self, audit_id: str) -> Dict:
        return self.client.get_audit(audit_id)

    def _handle_create_audit(self, name: str, language: str, audit_type: str) -> Dict:
        return self.client.create_audit(name, language, audit_type)

    def _handle_update_audit_general(self, audit_id: str, **kwargs) -> Dict:
        return self.client.update_audit_general(audit_id, **kwargs)

    def _handle_delete_audit(self, audit_id: str) -> Dict:
        self.client.delete_audit(audit_id)
        return {"success": True, "message": f"Audit {audit_id} deleted"}

    def _handle_generate_report(self, audit_id: str) -> Dict:
        content = self.client.generate_report(audit_id)
        return {"success": True, "size_bytes": len(content)}

    def _handle_get_findings(self, audit_id: str) -> List[Dict]:
        return self.client.get_findings(audit_id)

    def _handle_get_finding(self, audit_id: str, finding_id: str) -> Dict:
        return self.client.get_finding(audit_id, finding_id)

    def _handle_create_finding(self, audit_id: str, **kwargs) -> Dict:
        return self.client.create_finding(audit_id, **kwargs)

    def _handle_update_finding(self, audit_id: str, finding_id: str, **kwargs) -> Dict:
        return self.client.update_finding(audit_id, finding_id, **kwargs)

    def _handle_delete_finding(self, audit_id: str, finding_id: str) -> Dict:
        self.client.delete_finding(audit_id, finding_id)
        return {"success": True, "message": f"Finding {finding_id} deleted"}

    def _handle_search_findings(self, **kwargs) -> List[Dict]:
        return self.client.search_findings(**kwargs)

    def _handle_get_all_findings_with_context(
        self, include_failed: bool = False, exclude_categories: Optional[List[str]] = None
    ) -> List[Dict]:
        return self.client.get_all_findings_with_context(include_failed, exclude_categories)

    def _handle_list_clients(self) -> List[Dict]:
        return self.client.list_clients()

    def _handle_create_client(self, **kwargs) -> Dict:
        return self.client.create_client(**kwargs)

    def _handle_update_client(self, client_id: str, **kwargs) -> Dict:
        return self.client.update_client(client_id, **kwargs)

    def _handle_delete_client(self, client_id: str) -> Dict:
        self.client.delete_client(client_id)
        return {"success": True, "message": f"Client {client_id} deleted"}

    def _handle_list_companies(self) -> List[Dict]:
        return self.client.list_companies()

    def _handle_create_company(self, **kwargs) -> Dict:
        return self.client.create_company(**kwargs)

    def _handle_list_vulnerabilities(self) -> List[Dict]:
        return self.client.list_vulnerabilities()

    def _handle_get_vulnerabilities_by_locale(self, locale: str = "en") -> List[Dict]:
        return self.client.get_vulnerabilities_by_locale(locale)

    def _handle_create_vulnerability(self, **kwargs) -> Dict:
        return self.client.create_vulnerability(**kwargs)

    def _handle_list_users(self) -> List[Dict]:
        return self.client.list_users()

    def _handle_get_current_user(self) -> Dict:
        return self.client.get_current_user()

    def _handle_list_templates(self) -> List[Dict]:
        return self.client.list_templates()

    def _handle_list_languages(self) -> List[Dict]:
        return self.client.list_languages()

    def _handle_list_audit_types(self) -> List[Dict]:
        return self.client.list_audit_types()

    def _handle_get_statistics(self) -> Dict:
        return self.client.get_statistics()

    # =========================================================================
    # PUBLIC API METHODS (for testing and direct use)
    # =========================================================================

    async def handle_initialize(self, params: Dict) -> Dict:
        """
        Handle MCP initialize request (async public method).

        Args:
            params: Initialize parameters

        Returns:
            Initialize response with capabilities
        """
        return self._handle_initialize(params)

    async def handle_list_tools(self) -> List[Dict]:
        """
        Handle list tools request (async public method).

        Returns:
            List of tool definitions
        """
        from typing import cast

        result = self._handle_list_tools({})
        return cast(List[Dict], result.get("tools", []))

    async def handle_call_tool(self, name: str, arguments: Dict) -> Any:
        """
        Handle call tool request (async public method).

        Args:
            name: Tool name
            arguments: Tool arguments

        Returns:
            Tool result

        Raises:
            ValueError: If tool is unknown
        """
        params = {"name": name, "arguments": arguments}
        return self._handle_call_tool(params)

    def _format_result(self, data: Any) -> str:
        """
        Format result data for output.

        Args:
            data: Data to format

        Returns:
            Formatted string
        """
        if isinstance(data, str):
            return data
        elif data is None:
            return "null"
        else:
            return json.dumps(data, indent=2, default=str)

    # =========================================================================
    # MCP PROTOCOL HANDLING
    # =========================================================================

    def _handle_initialize(self, params: Dict) -> Dict:
        """Handle MCP initialize request."""
        self._initialized = True
        return {
            "protocolVersion": self.PROTOCOL_VERSION,
            "capabilities": {
                "tools": {"listChanged": True},
                "logging": {},
            },
            "serverInfo": {
                "name": self.SERVER_NAME,
                "version": self.SERVER_VERSION,
            },
        }

    def _handle_list_tools(self, params: Dict) -> Dict:
        """Handle tools/list request."""
        tools = []
        for tool in self._tools.values():
            tools.append(
                {
                    "name": tool.name,
                    "description": tool.description,
                    "inputSchema": tool.parameters,
                }
            )
        return {"tools": tools}

    def _handle_call_tool(self, params: Dict) -> Dict:
        """Handle tools/call request."""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})

        if tool_name not in self._tools:
            raise ValueError(f"Unknown tool: {tool_name}")

        tool = self._tools[tool_name]

        try:
            result = tool.handler(**arguments)
            return {
                "content": [{"type": "text", "text": json.dumps(result, indent=2, default=str)}]
            }
        except PwnDocError as e:
            return {"content": [{"type": "text", "text": f"Error: {str(e)}"}], "isError": True}

    def _handle_message(self, message: Dict) -> Optional[Dict]:
        """Process an incoming MCP message."""
        method = message.get("method")
        params = message.get("params", {})
        msg_id = message.get("id")

        handlers = {
            "initialize": self._handle_initialize,
            "initialized": lambda p: None,  # Notification, no response
            "tools/list": self._handle_list_tools,
            "tools/call": self._handle_call_tool,
            "ping": lambda p: {},
        }

        if method in handlers:
            try:
                result = handlers[method](params)
                if result is None:  # Notification
                    return None
                return {"jsonrpc": "2.0", "id": msg_id, "result": result}
            except Exception as e:
                logger.exception(f"Error handling {method}")
                return {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "error": {"code": -32603, "message": str(e)},
                }
        else:
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {"code": -32601, "message": f"Method not found: {method}"},
            }

    # =========================================================================
    # TRANSPORT IMPLEMENTATIONS
    # =========================================================================

    def run_stdio(self):
        """Run server with stdio transport (for Claude Desktop)."""
        logger.info("Starting PwnDoc MCP Server (stdio transport)")

        while True:
            try:
                line = sys.stdin.readline()
                if not line:
                    break

                message = json.loads(line)
                logger.debug(f"Received: {message.get('method', 'response')}")

                response = self._handle_message(message)
                if response:
                    sys.stdout.write(json.dumps(response) + "\n")
                    sys.stdout.flush()

            except json.JSONDecodeError as e:
                logger.warning(f"Invalid JSON: {e}")
            except KeyboardInterrupt:
                logger.info("Server interrupted")
                break
            except Exception as e:
                logger.exception(f"Error: {e}")

    async def run_sse(self, host: str = "127.0.0.1", port: int = 8080):
        """Run server with SSE transport."""
        try:
            from aiohttp import web
        except ImportError:
            raise ImportError("aiohttp required for SSE transport: pip install aiohttp")

        async def handle_sse(request):
            response = web.StreamResponse(
                status=200,
                headers={
                    "Content-Type": "text/event-stream",
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                },
            )
            await response.prepare(request)

            # Read messages from POST body
            data = await request.json()
            result = self._handle_message(data)

            if result:
                await response.write(f"data: {json.dumps(result)}\n\n".encode())

            return response

        app = web.Application()
        app.router.add_post("/mcp", handle_sse)

        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, host, port)
        await site.start()

        logger.info(f"SSE server running at http://{host}:{port}/mcp")

        # Keep running
        while True:
            await asyncio.sleep(3600)

    def run(self, transport: Optional[str] = None):
        """
        Run the MCP server.

        Args:
            transport: Transport type (stdio, sse, websocket). Defaults to config value.
        """
        transport = transport or self.config.mcp_transport

        if transport == "stdio":
            self.run_stdio()
        elif transport == "sse":
            asyncio.run(self.run_sse(self.config.mcp_host, self.config.mcp_port))
        else:
            raise ValueError(f"Unsupported transport: {transport}")


# Module-level constant for tool definitions (for compatibility)
TOOL_DEFINITIONS: Optional[List[Dict]] = None


def _get_tool_definitions() -> List[Dict]:
    """
    Get tool definitions from server instance.

    Returns:
        List of tool definitions
    """
    # Create a temporary server to extract tool definitions
    config = Config(url="http://temp", token="temp")
    server = PwnDocMCPServer(config)
    tools = []
    for tool in server._tools.values():
        tools.append(
            {
                "name": tool.name,
                "description": tool.description,
                "inputSchema": tool.parameters,
            }
        )
    return tools


# Initialize TOOL_DEFINITIONS on module load
TOOL_DEFINITIONS = _get_tool_definitions()


def create_server(config: Optional[Config] = None, **kwargs) -> PwnDocMCPServer:
    """
    Create and configure a PwnDoc MCP server.

    Args:
        config: Configuration object (if provided, kwargs are ignored)
        **kwargs: Configuration parameters (url, token, etc.)

    Returns:
        Configured PwnDocMCPServer instance

    Raises:
        ValueError: If configuration is invalid

    Example:
        >>> server = create_server(url="https://pwndoc.com", token="...")
        >>> server = create_server(config)
    """
    if config is None:
        config = Config(**kwargs)

    # Validate configuration
    errors = config.validate()
    if errors:
        raise ValueError(f"Invalid configuration: {'; '.join(errors)}")

    return PwnDocMCPServer(config)


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="PwnDoc MCP Server")
    parser.add_argument("--transport", choices=["stdio", "sse"], default="stdio")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--log-level", default="INFO")
    args = parser.parse_args()

    logging.basicConfig(level=getattr(logging, args.log_level))

    config = load_config(
        mcp_transport=args.transport,
        mcp_host=args.host,
        mcp_port=args.port,
    )

    server = PwnDocMCPServer(config)
    server.run()


if __name__ == "__main__":
    main()
