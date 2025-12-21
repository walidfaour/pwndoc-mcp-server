"""
Version helpers for PwnDoc MCP Server.

Centralizes version lookup so the CLI and server report the same value.
"""

from importlib import metadata

PACKAGE_NAME = "pwndoc-mcp-server"
_FALLBACK_VERSION = "1.0.2"


def get_version() -> str:
    """
    Return the installed package version, falling back to a bundled default.

    This ensures local source checkouts (or editable installs) still report a
    sensible version while published wheels use the package metadata.
    """
    try:
        return metadata.version(PACKAGE_NAME)
    except metadata.PackageNotFoundError:
        return _FALLBACK_VERSION


__all__ = ["get_version", "PACKAGE_NAME"]
