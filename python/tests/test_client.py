"""Tests for PwnDoc MCP Server."""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from pwndoc_mcp_server.config import Config, load_config
from pwndoc_mcp_server.client import PwnDocClient


class TestConfig:
    """Tests for configuration."""
    
    def test_config_from_env(self, monkeypatch):
        """Test loading config from environment."""
        monkeypatch.setenv("PWNDOC_URL", "https://test.com")
        monkeypatch.setenv("PWNDOC_TOKEN", "test-token")
        
        config = Config.from_env()
        
        assert config.url == "https://test.com"
        assert config.token == "test-token"
    
    def test_config_validate_missing_url(self):
        """Test validation catches missing URL."""
        config = Config(token="test")
        errors = config.validate()
        
        assert "PWNDOC_URL is required" in errors
    
    def test_config_validate_missing_auth(self):
        """Test validation catches missing auth."""
        config = Config(url="https://test.com")
        errors = config.validate()
        
        assert any("PWNDOC_TOKEN" in e or "PWNDOC_USERNAME" in e for e in errors)
    
    def test_config_validate_success_with_token(self):
        """Test validation passes with token."""
        config = Config(url="https://test.com", token="test-token")
        errors = config.validate()
        
        assert len(errors) == 0
    
    def test_config_validate_success_with_password(self):
        """Test validation passes with username/password."""
        config = Config(
            url="https://test.com",
            username="user",
            password="pass"
        )
        errors = config.validate()
        
        assert len(errors) == 0


class TestClient:
    """Tests for PwnDoc client."""
    
    @pytest.fixture
    def client(self):
        """Create test client."""
        return PwnDocClient(
            url="https://test.pwndoc.com",
            token="test-token",
            verify_ssl=False,
        )
    
    @pytest.mark.asyncio
    async def test_client_from_config(self):
        """Test creating client from config."""
        config = Config(
            url="https://test.com",
            token="test-token",
        )
        client = PwnDocClient.from_config(config)
        
        assert client.url == "https://test.com"
        assert client.token == "test-token"
        await client.close()
    
    @pytest.mark.asyncio
    async def test_test_connection_success(self, client):
        """Test successful connection test."""
        with patch.object(client, 'get_current_user', new_callable=AsyncMock) as mock_get:
            mock_get.return_value = {"datas": {"username": "testuser"}}
            
            result = await client.test_connection()
            
            assert result["status"] == "ok"
            assert result["user"] == "testuser"
        
        await client.close()
    
    @pytest.mark.asyncio
    async def test_test_connection_failure(self, client):
        """Test failed connection test."""
        with patch.object(client, '_ensure_token', new_callable=AsyncMock) as mock_token:
            mock_token.side_effect = Exception("Connection failed")
            
            result = await client.test_connection()
            
            assert result["status"] == "error"
            assert "Connection failed" in result["error"]
        
        await client.close()
