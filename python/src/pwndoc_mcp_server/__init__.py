"""
PwnDoc MCP Server

Model Context Protocol server for PwnDoc penetration testing documentation.
"""

from pwndoc_mcp_server.version import get_version

__version__ = get_version()
__author__ = "Walid Faour"

# Export main classes and functions
from pwndoc_mcp_server.client import (
    AuthenticationError,
    NotFoundError,
    PwnDocClient,
    PwnDocError,
    RateLimitError,
)
from pwndoc_mcp_server.config import (
    Config,
    get_config_path,
    init_config_interactive,
    load_config,
    save_config,
)
from pwndoc_mcp_server.logging_config import LogLevel, get_logger, setup_logging
from pwndoc_mcp_server.server import (
    TOOL_DEFINITIONS,
    PwnDocMCPServer,
    create_server,
)

__all__ = [
    # Version
    "__version__",
    # Config
    "Config",
    "get_config_path",
    "init_config_interactive",
    "load_config",
    "save_config",
    # Client
    "PwnDocClient",
    "PwnDocError",
    "AuthenticationError",
    "RateLimitError",
    "NotFoundError",
    # Server
    "PwnDocMCPServer",
    "TOOL_DEFINITIONS",
    "create_server",
    # Logging
    "LogLevel",
    "setup_logging",
    "get_logger",
]
