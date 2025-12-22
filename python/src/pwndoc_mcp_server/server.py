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

        self._register_tool(
            name="get_audit_general",
            description="Get audit general information (dates, client, company, scope).",
            parameters={
                "type": "object",
                "properties": {"audit_id": {"type": "string", "description": "The audit ID"}},
                "required": ["audit_id"],
            },
            handler=self._handle_get_audit_general,
        )

        self._register_tool(
            name="get_audit_network",
            description="Get audit network information.",
            parameters={
                "type": "object",
                "properties": {"audit_id": {"type": "string", "description": "The audit ID"}},
                "required": ["audit_id"],
            },
            handler=self._handle_get_audit_network,
        )

        self._register_tool(
            name="update_audit_network",
            description="Update audit network information.",
            parameters={
                "type": "object",
                "properties": {
                    "audit_id": {"type": "string", "description": "The audit ID"},
                    "network_data": {"type": "object", "description": "Network configuration data"},
                },
                "required": ["audit_id", "network_data"],
            },
            handler=self._handle_update_audit_network,
        )

        self._register_tool(
            name="toggle_audit_approval",
            description="Toggle audit approval status.",
            parameters={
                "type": "object",
                "properties": {"audit_id": {"type": "string", "description": "The audit ID"}},
                "required": ["audit_id"],
            },
            handler=self._handle_toggle_audit_approval,
        )

        self._register_tool(
            name="update_review_status",
            description="Update audit ready-for-review status.",
            parameters={
                "type": "object",
                "properties": {
                    "audit_id": {"type": "string", "description": "The audit ID"},
                    "state": {"type": "boolean", "description": "Ready for review state"},
                },
                "required": ["audit_id", "state"],
            },
            handler=self._handle_update_review_status,
        )

        self._register_tool(
            name="get_audit_sections",
            description="Get audit sections content.",
            parameters={
                "type": "object",
                "properties": {"audit_id": {"type": "string", "description": "The audit ID"}},
                "required": ["audit_id"],
            },
            handler=self._handle_get_audit_sections,
        )

        self._register_tool(
            name="update_audit_sections",
            description="Update audit sections content.",
            parameters={
                "type": "object",
                "properties": {
                    "audit_id": {"type": "string", "description": "The audit ID"},
                    "sections": {"type": "object", "description": "Sections data to update"},
                },
                "required": ["audit_id", "sections"],
            },
            handler=self._handle_update_audit_sections,
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

        self._register_tool(
            name="sort_findings",
            description="Reorder findings within an audit.",
            parameters={
                "type": "object",
                "properties": {
                    "audit_id": {"type": "string", "description": "The audit ID"},
                    "finding_order": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Ordered array of finding IDs",
                    },
                },
                "required": ["audit_id", "finding_order"],
            },
            handler=self._handle_sort_findings,
        )

        self._register_tool(
            name="move_finding",
            description="Move a finding from one audit to another.",
            parameters={
                "type": "object",
                "properties": {
                    "audit_id": {"type": "string", "description": "Source audit ID"},
                    "finding_id": {"type": "string", "description": "Finding ID to move"},
                    "destination_audit_id": {
                        "type": "string",
                        "description": "Destination audit ID",
                    },
                },
                "required": ["audit_id", "finding_id", "destination_audit_id"],
            },
            handler=self._handle_move_finding,
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

        self._register_tool(
            name="update_company",
            description="Update an existing company.",
            parameters={
                "type": "object",
                "properties": {
                    "company_id": {"type": "string", "description": "Company ID"},
                    "name": {"type": "string", "description": "Company name"},
                    "short_name": {"type": "string", "description": "Short name/abbreviation"},
                    "logo": {"type": "string", "description": "Logo (base64)"},
                },
                "required": ["company_id"],
            },
            handler=self._handle_update_company,
        )

        self._register_tool(
            name="delete_company",
            description="Delete a company.",
            parameters={
                "type": "object",
                "properties": {
                    "company_id": {"type": "string", "description": "Company ID to delete"}
                },
                "required": ["company_id"],
            },
            handler=self._handle_delete_company,
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

        self._register_tool(
            name="update_vulnerability",
            description="Update an existing vulnerability template.",
            parameters={
                "type": "object",
                "properties": {
                    "vuln_id": {"type": "string", "description": "Vulnerability template ID"},
                    "details": {"type": "object", "description": "Vulnerability details by locale"},
                    "cvssv3": {"type": "string", "description": "CVSS v3 score"},
                    "priority": {"type": "integer", "description": "Priority (1-4)"},
                    "remediation_complexity": {
                        "type": "integer",
                        "description": "Complexity (1-3)",
                    },
                    "category": {"type": "string", "description": "Category"},
                },
                "required": ["vuln_id"],
            },
            handler=self._handle_update_vulnerability,
        )

        self._register_tool(
            name="delete_vulnerability",
            description="Delete a vulnerability template.",
            parameters={
                "type": "object",
                "properties": {
                    "vuln_id": {
                        "type": "string",
                        "description": "Vulnerability template ID to delete",
                    }
                },
                "required": ["vuln_id"],
            },
            handler=self._handle_delete_vulnerability,
        )

        self._register_tool(
            name="bulk_delete_vulnerabilities",
            description="Delete multiple vulnerability templates at once.",
            parameters={
                "type": "object",
                "properties": {
                    "vuln_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Array of vulnerability template IDs to delete",
                    }
                },
                "required": ["vuln_ids"],
            },
            handler=self._handle_bulk_delete_vulnerabilities,
        )

        self._register_tool(
            name="export_vulnerabilities",
            description="Export all vulnerability templates.",
            parameters={"type": "object", "properties": {}},
            handler=self._handle_export_vulnerabilities,
        )

        self._register_tool(
            name="create_vulnerability_from_finding",
            description="Create a vulnerability template from an existing finding.",
            parameters={
                "type": "object",
                "properties": {
                    "audit_id": {"type": "string", "description": "Audit ID"},
                    "finding_id": {"type": "string", "description": "Finding ID"},
                    "locale": {"type": "string", "description": "Language code (e.g., 'en')"},
                },
                "required": ["audit_id", "finding_id"],
            },
            handler=self._handle_create_vulnerability_from_finding,
        )

        self._register_tool(
            name="get_vulnerability_updates",
            description="Get available vulnerability template updates.",
            parameters={"type": "object", "properties": {}},
            handler=self._handle_get_vulnerability_updates,
        )

        self._register_tool(
            name="merge_vulnerability",
            description="Merge vulnerability template with an update.",
            parameters={
                "type": "object",
                "properties": {
                    "vuln_id": {"type": "string", "description": "Vulnerability template ID"},
                    "update_id": {"type": "string", "description": "Update ID to merge"},
                },
                "required": ["vuln_id", "update_id"],
            },
            handler=self._handle_merge_vulnerability,
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

        self._register_tool(
            name="get_user",
            description="Get user information by username.",
            parameters={
                "type": "object",
                "properties": {"username": {"type": "string", "description": "Username"}},
                "required": ["username"],
            },
            handler=self._handle_get_user,
        )

        self._register_tool(
            name="create_user",
            description="Create a new user (admin only).",
            parameters={
                "type": "object",
                "properties": {
                    "username": {"type": "string", "description": "Username"},
                    "password": {"type": "string", "description": "Password"},
                    "firstname": {"type": "string", "description": "First name"},
                    "lastname": {"type": "string", "description": "Last name"},
                    "email": {"type": "string", "description": "Email address"},
                    "role": {"type": "string", "description": "User role"},
                },
                "required": ["username", "password", "firstname", "lastname", "email", "role"],
            },
            handler=self._handle_create_user,
        )

        self._register_tool(
            name="update_user",
            description="Update a user (admin only).",
            parameters={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "User ID"},
                    "username": {"type": "string", "description": "Username"},
                    "firstname": {"type": "string", "description": "First name"},
                    "lastname": {"type": "string", "description": "Last name"},
                    "email": {"type": "string", "description": "Email address"},
                    "role": {"type": "string", "description": "User role"},
                },
                "required": ["user_id"],
            },
            handler=self._handle_update_user,
        )

        self._register_tool(
            name="update_current_user",
            description="Update current user's profile.",
            parameters={
                "type": "object",
                "properties": {
                    "firstname": {"type": "string", "description": "First name"},
                    "lastname": {"type": "string", "description": "Last name"},
                    "email": {"type": "string", "description": "Email address"},
                    "password": {"type": "string", "description": "New password"},
                },
            },
            handler=self._handle_update_current_user,
        )

        self._register_tool(
            name="list_reviewers",
            description="List all users with reviewer role.",
            parameters={"type": "object", "properties": {}},
            handler=self._handle_list_reviewers,
        )

        self._register_tool(
            name="get_totp_status",
            description="Get TOTP (2FA) status for current user.",
            parameters={"type": "object", "properties": {}},
            handler=self._handle_get_totp,
        )

        self._register_tool(
            name="setup_totp",
            description="Setup TOTP (2FA) for current user.",
            parameters={"type": "object", "properties": {}},
            handler=self._handle_setup_totp,
        )

        self._register_tool(
            name="disable_totp",
            description="Disable TOTP (2FA) for current user.",
            parameters={
                "type": "object",
                "properties": {
                    "token": {"type": "string", "description": "TOTP token for verification"}
                },
                "required": ["token"],
            },
            handler=self._handle_disable_totp,
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
            name="create_template",
            description="Create/upload a report template.",
            parameters={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Template name"},
                    "ext": {"type": "string", "description": "File extension (e.g., 'docx')"},
                    "file_content": {
                        "type": "string",
                        "description": "Base64-encoded file content",
                    },
                },
                "required": ["name", "ext", "file_content"],
            },
            handler=self._handle_create_template,
        )

        self._register_tool(
            name="update_template",
            description="Update an existing template.",
            parameters={
                "type": "object",
                "properties": {
                    "template_id": {"type": "string", "description": "Template ID"},
                    "name": {"type": "string", "description": "Template name"},
                    "ext": {"type": "string", "description": "File extension"},
                    "file_content": {
                        "type": "string",
                        "description": "Base64-encoded file content",
                    },
                },
                "required": ["template_id"],
            },
            handler=self._handle_update_template,
        )

        self._register_tool(
            name="delete_template",
            description="Delete a report template.",
            parameters={
                "type": "object",
                "properties": {
                    "template_id": {"type": "string", "description": "Template ID to delete"}
                },
                "required": ["template_id"],
            },
            handler=self._handle_delete_template,
        )

        self._register_tool(
            name="download_template",
            description="Download a template file.",
            parameters={
                "type": "object",
                "properties": {
                    "template_id": {"type": "string", "description": "Template ID to download"}
                },
                "required": ["template_id"],
            },
            handler=self._handle_download_template,
        )

        self._register_tool(
            name="get_settings",
            description="Get system settings.",
            parameters={"type": "object", "properties": {}},
            handler=self._handle_get_settings,
        )

        self._register_tool(
            name="get_public_settings",
            description="Get public settings (no authentication required).",
            parameters={"type": "object", "properties": {}},
            handler=self._handle_get_public_settings,
        )

        self._register_tool(
            name="update_settings",
            description="Update system settings (admin only).",
            parameters={
                "type": "object",
                "properties": {"settings": {"type": "object", "description": "Settings to update"}},
                "required": ["settings"],
            },
            handler=self._handle_update_settings,
        )

        self._register_tool(
            name="export_settings",
            description="Export all system settings.",
            parameters={"type": "object", "properties": {}},
            handler=self._handle_export_settings,
        )

        self._register_tool(
            name="import_settings",
            description="Import/revert system settings from export.",
            parameters={
                "type": "object",
                "properties": {"settings": {"type": "object", "description": "Settings to import"}},
                "required": ["settings"],
            },
            handler=self._handle_import_settings,
        )

        self._register_tool(
            name="list_languages",
            description="List all configured languages.",
            parameters={"type": "object", "properties": {}},
            handler=self._handle_list_languages,
        )

        self._register_tool(
            name="create_language",
            description="Create a new language.",
            parameters={
                "type": "object",
                "properties": {
                    "language": {"type": "string", "description": "Language code (e.g., 'en')"},
                    "name": {"type": "string", "description": "Language name"},
                },
                "required": ["language", "name"],
            },
            handler=self._handle_create_language,
        )

        self._register_tool(
            name="update_language",
            description="Update a language.",
            parameters={
                "type": "object",
                "properties": {
                    "language_id": {"type": "string", "description": "Language ID"},
                    "language": {"type": "string", "description": "Language code"},
                    "name": {"type": "string", "description": "Language name"},
                },
                "required": ["language_id"],
            },
            handler=self._handle_update_language,
        )

        self._register_tool(
            name="delete_language",
            description="Delete a language.",
            parameters={
                "type": "object",
                "properties": {
                    "language_id": {"type": "string", "description": "Language ID to delete"}
                },
                "required": ["language_id"],
            },
            handler=self._handle_delete_language,
        )

        self._register_tool(
            name="list_audit_types",
            description="List all audit types.",
            parameters={"type": "object", "properties": {}},
            handler=self._handle_list_audit_types,
        )

        self._register_tool(
            name="create_audit_type",
            description="Create a new audit type.",
            parameters={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Audit type name"},
                    "templates": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Template IDs",
                    },
                },
                "required": ["name"],
            },
            handler=self._handle_create_audit_type,
        )

        self._register_tool(
            name="update_audit_type",
            description="Update an audit type.",
            parameters={
                "type": "object",
                "properties": {
                    "audit_type_id": {"type": "string", "description": "Audit type ID"},
                    "name": {"type": "string", "description": "Audit type name"},
                    "templates": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["audit_type_id"],
            },
            handler=self._handle_update_audit_type,
        )

        self._register_tool(
            name="delete_audit_type",
            description="Delete an audit type.",
            parameters={
                "type": "object",
                "properties": {
                    "audit_type_id": {"type": "string", "description": "Audit type ID to delete"}
                },
                "required": ["audit_type_id"],
            },
            handler=self._handle_delete_audit_type,
        )

        self._register_tool(
            name="list_vulnerability_types",
            description="List all vulnerability types.",
            parameters={"type": "object", "properties": {}},
            handler=self._handle_list_vulnerability_types,
        )

        self._register_tool(
            name="create_vulnerability_type",
            description="Create a new vulnerability type.",
            parameters={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Vulnerability type name"}
                },
                "required": ["name"],
            },
            handler=self._handle_create_vulnerability_type,
        )

        self._register_tool(
            name="update_vulnerability_type",
            description="Update a vulnerability type.",
            parameters={
                "type": "object",
                "properties": {
                    "vuln_type_id": {"type": "string", "description": "Vulnerability type ID"},
                    "name": {"type": "string", "description": "Vulnerability type name"},
                },
                "required": ["vuln_type_id"],
            },
            handler=self._handle_update_vulnerability_type,
        )

        self._register_tool(
            name="delete_vulnerability_type",
            description="Delete a vulnerability type.",
            parameters={
                "type": "object",
                "properties": {
                    "vuln_type_id": {
                        "type": "string",
                        "description": "Vulnerability type ID to delete",
                    }
                },
                "required": ["vuln_type_id"],
            },
            handler=self._handle_delete_vulnerability_type,
        )

        self._register_tool(
            name="list_vulnerability_categories",
            description="List all vulnerability categories.",
            parameters={"type": "object", "properties": {}},
            handler=self._handle_list_vulnerability_categories,
        )

        self._register_tool(
            name="create_vulnerability_category",
            description="Create a new vulnerability category.",
            parameters={
                "type": "object",
                "properties": {"name": {"type": "string", "description": "Category name"}},
                "required": ["name"],
            },
            handler=self._handle_create_vulnerability_category,
        )

        self._register_tool(
            name="update_vulnerability_category",
            description="Update a vulnerability category.",
            parameters={
                "type": "object",
                "properties": {
                    "category_id": {"type": "string", "description": "Category ID"},
                    "name": {"type": "string", "description": "Category name"},
                },
                "required": ["category_id"],
            },
            handler=self._handle_update_vulnerability_category,
        )

        self._register_tool(
            name="delete_vulnerability_category",
            description="Delete a vulnerability category.",
            parameters={
                "type": "object",
                "properties": {
                    "category_id": {"type": "string", "description": "Category ID to delete"}
                },
                "required": ["category_id"],
            },
            handler=self._handle_delete_vulnerability_category,
        )

        self._register_tool(
            name="list_sections",
            description="List all section definitions.",
            parameters={"type": "object", "properties": {}},
            handler=self._handle_list_sections,
        )

        self._register_tool(
            name="create_section",
            description="Create a new section definition.",
            parameters={
                "type": "object",
                "properties": {
                    "field": {"type": "string", "description": "Section field name"},
                    "name": {"type": "string", "description": "Section display name"},
                },
                "required": ["field", "name"],
            },
            handler=self._handle_create_section,
        )

        self._register_tool(
            name="update_section",
            description="Update a section definition.",
            parameters={
                "type": "object",
                "properties": {
                    "section_id": {"type": "string", "description": "Section ID"},
                    "field": {"type": "string", "description": "Section field name"},
                    "name": {"type": "string", "description": "Section display name"},
                },
                "required": ["section_id"],
            },
            handler=self._handle_update_section,
        )

        self._register_tool(
            name="delete_section",
            description="Delete a section definition.",
            parameters={
                "type": "object",
                "properties": {
                    "section_id": {"type": "string", "description": "Section ID to delete"}
                },
                "required": ["section_id"],
            },
            handler=self._handle_delete_section,
        )

        self._register_tool(
            name="list_custom_fields",
            description="List all custom field definitions.",
            parameters={"type": "object", "properties": {}},
            handler=self._handle_list_custom_fields,
        )

        self._register_tool(
            name="create_custom_field",
            description="Create a new custom field definition.",
            parameters={
                "type": "object",
                "properties": {
                    "label": {"type": "string", "description": "Field label"},
                    "field_type": {
                        "type": "string",
                        "description": "Field type (text, select, etc.)",
                    },
                },
                "required": ["label", "field_type"],
            },
            handler=self._handle_create_custom_field,
        )

        self._register_tool(
            name="update_custom_field",
            description="Update a custom field definition.",
            parameters={
                "type": "object",
                "properties": {
                    "field_id": {"type": "string", "description": "Custom field ID"},
                    "label": {"type": "string", "description": "Field label"},
                    "field_type": {"type": "string", "description": "Field type"},
                },
                "required": ["field_id"],
            },
            handler=self._handle_update_custom_field,
        )

        self._register_tool(
            name="delete_custom_field",
            description="Delete a custom field definition.",
            parameters={
                "type": "object",
                "properties": {
                    "field_id": {"type": "string", "description": "Custom field ID to delete"}
                },
                "required": ["field_id"],
            },
            handler=self._handle_delete_custom_field,
        )

        self._register_tool(
            name="list_roles",
            description="List all user roles.",
            parameters={"type": "object", "properties": {}},
            handler=self._handle_list_roles,
        )

        # =====================================================================
        # IMAGE TOOLS
        # =====================================================================

        self._register_tool(
            name="get_image",
            description="Get image metadata.",
            parameters={
                "type": "object",
                "properties": {"image_id": {"type": "string", "description": "Image ID"}},
                "required": ["image_id"],
            },
            handler=self._handle_get_image,
        )

        self._register_tool(
            name="download_image",
            description="Download an image file.",
            parameters={
                "type": "object",
                "properties": {
                    "image_id": {"type": "string", "description": "Image ID to download"}
                },
                "required": ["image_id"],
            },
            handler=self._handle_download_image,
        )

        self._register_tool(
            name="upload_image",
            description="Upload an image to an audit.",
            parameters={
                "type": "object",
                "properties": {
                    "audit_id": {"type": "string", "description": "Audit ID"},
                    "name": {"type": "string", "description": "Image name"},
                    "value": {"type": "string", "description": "Base64-encoded image data"},
                },
                "required": ["audit_id", "name", "value"],
            },
            handler=self._handle_upload_image,
        )

        self._register_tool(
            name="delete_image",
            description="Delete an image.",
            parameters={
                "type": "object",
                "properties": {"image_id": {"type": "string", "description": "Image ID to delete"}},
                "required": ["image_id"],
            },
            handler=self._handle_delete_image,
        )

        # =====================================================================
        # STATISTICS
        # =====================================================================

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

    # Audit handlers
    def _handle_get_audit_general(self, audit_id: str) -> Dict:
        return self.client.get_audit_general(audit_id)

    def _handle_get_audit_network(self, audit_id: str) -> Dict:
        return self.client.get_audit_network(audit_id)

    def _handle_update_audit_network(self, audit_id: str, network_data: Dict) -> Dict:
        return self.client.update_audit_network(audit_id, network_data)

    def _handle_toggle_audit_approval(self, audit_id: str) -> Dict:
        return self.client.toggle_audit_approval(audit_id)

    def _handle_update_review_status(self, audit_id: str, state: bool) -> Dict:
        return self.client.update_review_status(audit_id, state)

    # Finding handlers
    def _handle_sort_findings(self, audit_id: str, finding_order: List[str]) -> Dict:
        return self.client.sort_findings(audit_id, finding_order)

    def _handle_move_finding(
        self, audit_id: str, finding_id: str, destination_audit_id: str
    ) -> Dict:
        return self.client.move_finding(audit_id, finding_id, destination_audit_id)

    # Company handlers
    def _handle_update_company(self, company_id: str, **kwargs) -> Dict:
        return self.client.update_company(company_id, **kwargs)

    def _handle_delete_company(self, company_id: str) -> Dict:
        self.client.delete_company(company_id)
        return {"success": True, "message": f"Company {company_id} deleted"}

    # Vulnerability handlers
    def _handle_update_vulnerability(self, vuln_id: str, **kwargs) -> Dict:
        return self.client.update_vulnerability(vuln_id, **kwargs)

    def _handle_delete_vulnerability(self, vuln_id: str) -> Dict:
        self.client.delete_vulnerability(vuln_id)
        return {"success": True, "message": f"Vulnerability {vuln_id} deleted"}

    def _handle_bulk_delete_vulnerabilities(self, vuln_ids: List[str]) -> Dict:
        self.client.bulk_delete_vulnerabilities(vuln_ids)
        return {"success": True, "message": f"Deleted {len(vuln_ids)} vulnerabilities"}

    def _handle_export_vulnerabilities(self) -> Dict:
        return self.client.export_vulnerabilities()

    def _handle_create_vulnerability_from_finding(self, **kwargs) -> Dict:
        return self.client.create_vulnerability_from_finding(**kwargs)

    # User handlers
    def _handle_get_user(self, username: str) -> Dict:
        return self.client.get_user(username)

    def _handle_create_user(self, **kwargs) -> Dict:
        return self.client.create_user(**kwargs)

    def _handle_update_user(self, user_id: str, **kwargs) -> Dict:
        return self.client.update_user(user_id, **kwargs)

    def _handle_update_current_user(self, **kwargs) -> Dict:
        return self.client.update_current_user(**kwargs)

    def _handle_list_reviewers(self) -> List[Dict]:
        return self.client.list_reviewers()

    # Template handlers
    def _handle_create_template(self, name: str, ext: str, file_content: str) -> Dict:
        return self.client.create_template(name, ext, file_content)

    def _handle_update_template(self, template_id: str, **kwargs) -> Dict:
        return self.client.update_template(template_id, **kwargs)

    def _handle_delete_template(self, template_id: str) -> Dict:
        self.client.delete_template(template_id)
        return {"success": True, "message": f"Template {template_id} deleted"}

    def _handle_download_template(self, template_id: str) -> Dict:
        content = self.client.download_template(template_id)
        return {"success": True, "size_bytes": len(content)}

    # Settings handlers
    def _handle_get_settings(self) -> Dict:
        return self.client.get_settings()

    def _handle_get_public_settings(self) -> Dict:
        return self.client.get_public_settings()

    def _handle_update_settings(self, settings: Dict) -> Dict:
        return self.client.update_settings(settings)

    # Data type handlers
    def _handle_list_vulnerability_types(self) -> List[Dict]:
        return self.client.list_vulnerability_types()

    def _handle_list_vulnerability_categories(self) -> List[Dict]:
        return self.client.list_vulnerability_categories()

    def _handle_list_sections(self) -> List[Dict]:
        return self.client.list_sections()

    def _handle_list_custom_fields(self) -> List[Dict]:
        return self.client.list_custom_fields()

    def _handle_list_roles(self) -> List[Dict]:
        return self.client.list_roles()

    # Image handlers
    def _handle_get_image(self, image_id: str) -> Dict:
        return self.client.get_image(image_id)

    def _handle_download_image(self, image_id: str) -> Dict:
        content = self.client.download_image(image_id)
        return {"success": True, "size_bytes": len(content)}

    def _handle_upload_image(self, audit_id: str, name: str, value: str) -> Dict:
        return self.client.upload_image(audit_id, name, value)

    def _handle_delete_image(self, image_id: str) -> Dict:
        self.client.delete_image(image_id)
        return {"success": True, "message": f"Image {image_id} deleted"}

    # Audit section handlers
    def _handle_get_audit_sections(self, audit_id: str) -> Dict:
        return self.client.get_audit_sections(audit_id)

    def _handle_update_audit_sections(self, audit_id: str, sections: Dict) -> Dict:
        return self.client.update_audit_sections(audit_id, sections)

    # TOTP handlers
    def _handle_get_totp(self) -> Dict:
        return self.client.get_totp()

    def _handle_setup_totp(self) -> Dict:
        return self.client.setup_totp()

    def _handle_disable_totp(self, token: str) -> Dict:
        return self.client.disable_totp(token)

    # Settings handlers
    def _handle_export_settings(self) -> Dict:
        return self.client.export_settings()

    def _handle_import_settings(self, settings: Dict) -> Dict:
        return self.client.import_settings(settings)

    # Language handlers
    def _handle_create_language(self, **kwargs) -> Dict:
        return self.client.create_language(**kwargs)

    def _handle_update_language(self, language_id: str, **kwargs) -> Dict:
        return self.client.update_language(language_id, **kwargs)

    def _handle_delete_language(self, language_id: str) -> Dict:
        self.client.delete_language(language_id)
        return {"success": True, "message": f"Language {language_id} deleted"}

    # Audit type handlers
    def _handle_create_audit_type(self, **kwargs) -> Dict:
        return self.client.create_audit_type(**kwargs)

    def _handle_update_audit_type(self, audit_type_id: str, **kwargs) -> Dict:
        return self.client.update_audit_type(audit_type_id, **kwargs)

    def _handle_delete_audit_type(self, audit_type_id: str) -> Dict:
        self.client.delete_audit_type(audit_type_id)
        return {"success": True, "message": f"Audit type {audit_type_id} deleted"}

    # Vulnerability type handlers
    def _handle_create_vulnerability_type(self, **kwargs) -> Dict:
        return self.client.create_vulnerability_type(**kwargs)

    def _handle_update_vulnerability_type(self, vuln_type_id: str, **kwargs) -> Dict:
        return self.client.update_vulnerability_type(vuln_type_id, **kwargs)

    def _handle_delete_vulnerability_type(self, vuln_type_id: str) -> Dict:
        self.client.delete_vulnerability_type(vuln_type_id)
        return {"success": True, "message": f"Vulnerability type {vuln_type_id} deleted"}

    # Vulnerability category handlers
    def _handle_create_vulnerability_category(self, **kwargs) -> Dict:
        return self.client.create_vulnerability_category(**kwargs)

    def _handle_update_vulnerability_category(self, category_id: str, **kwargs) -> Dict:
        return self.client.update_vulnerability_category(category_id, **kwargs)

    def _handle_delete_vulnerability_category(self, category_id: str) -> Dict:
        self.client.delete_vulnerability_category(category_id)
        return {"success": True, "message": f"Vulnerability category {category_id} deleted"}

    # Section handlers
    def _handle_create_section(self, **kwargs) -> Dict:
        return self.client.create_section(**kwargs)

    def _handle_update_section(self, section_id: str, **kwargs) -> Dict:
        return self.client.update_section(section_id, **kwargs)

    def _handle_delete_section(self, section_id: str) -> Dict:
        self.client.delete_section(section_id)
        return {"success": True, "message": f"Section {section_id} deleted"}

    # Custom field handlers
    def _handle_create_custom_field(self, **kwargs) -> Dict:
        return self.client.create_custom_field(**kwargs)

    def _handle_update_custom_field(self, field_id: str, **kwargs) -> Dict:
        return self.client.update_custom_field(field_id, **kwargs)

    def _handle_delete_custom_field(self, field_id: str) -> Dict:
        self.client.delete_custom_field(field_id)
        return {"success": True, "message": f"Custom field {field_id} deleted"}

    # Vulnerability update handlers
    def _handle_get_vulnerability_updates(self) -> List[Dict]:
        return self.client.get_vulnerability_updates()

    def _handle_merge_vulnerability(self, vuln_id: str, update_id: str) -> Dict:
        return self.client.merge_vulnerability(vuln_id, update_id)

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
