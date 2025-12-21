"""
PwnDoc MCP Server

Model Context Protocol server for PwnDoc penetration testing documentation.
"""

__version__ = "1.0.0"
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
from pwndoc_mcp_server.logging_config import get_logger, setup_logging
from pwndoc_mcp_server.server import PwnDocMCPServer

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
    # Logging
    "setup_logging",
    "get_logger",
]
