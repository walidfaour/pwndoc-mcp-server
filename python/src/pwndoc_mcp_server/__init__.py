"""
PwnDoc MCP Server

Model Context Protocol server for PwnDoc penetration testing documentation.
"""

# CRITICAL: Suppress ALL output to stdout during module initialization
# MCP protocol requires stdout to ONLY contain JSON-RPC messages
import logging
import os
import sys
import warnings

# Suppress ALL warnings that could leak to stdout
warnings.filterwarnings("ignore")

# Configure logging to stderr BEFORE anything else
logging.basicConfig(
    level=logging.CRITICAL,  # Only CRITICAL and above (basically nothing)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
    force=True,
)

# Temporarily redirect stdout to /dev/null during imports
_original_stdout = sys.stdout
_devnull = open(os.devnull, "w")
sys.stdout = _devnull

try:
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
        get_tool_definitions,
    )
finally:
    # ALWAYS restore stdout
    sys.stdout = _original_stdout
    _devnull.close()

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
    "get_tool_definitions",
    "create_server",
    # Logging
    "LogLevel",
    "setup_logging",
    "get_logger",
]
