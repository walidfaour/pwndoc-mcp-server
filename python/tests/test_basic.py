"""
Basic smoke tests to ensure package imports work.
"""

import pytest


def test_import_package():
    """Test that the package can be imported."""
    import pwndoc_mcp_server
    assert pwndoc_mcp_server.__version__ is not None


def test_import_config():
    """Test that Config can be imported."""
    from pwndoc_mcp_server.config import Config
    assert Config is not None


def test_import_client():
    """Test that PwnDocClient can be imported."""
    from pwndoc_mcp_server.client import PwnDocClient
    assert PwnDocClient is not None


def test_import_server():
    """Test that PwnDocMCPServer can be imported."""
    from pwndoc_mcp_server.server import PwnDocMCPServer
    assert PwnDocMCPServer is not None


def test_config_creation():
    """Test that a Config object can be created."""
    from pwndoc_mcp_server.config import Config

    config = Config(
        url="https://test.pwndoc.com",
        username="test",
        password="test"
    )
    assert config.url == "https://test.pwndoc.com"
