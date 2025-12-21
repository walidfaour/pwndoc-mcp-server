"""
PwnDoc MCP Server - Model Context Protocol server for PwnDoc pentest documentation.

A comprehensive MCP server that enables AI assistants like Claude to interact
with PwnDoc's penetration testing documentation system through natural language.

Repository: https://github.com/faour-sec/pwndoc-mcp-server
Documentation: https://walidfaour.github.io/pwndoc-mcp-server
"""

__version__ = "1.0.0"
__author__ = "Faour"
__email__ = "faour@finessedirect.com"
__license__ = "MIT"

from .server import PwnDocMCPServer
from .config import Config, load_config
from .client import PwnDocClient

__all__ = [
    "PwnDocMCPServer",
    "Config",
    "load_config",
    "PwnDocClient",
    "__version__",
]
