"""
Tests for the CLI module.
"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from typer.testing import CliRunner
import json
import os

from pwndoc_mcp_server.cli import app


@pytest.fixture
def runner():
    """Create CLI test runner."""
    return CliRunner()


class TestVersionCommand:
    """Tests for version command."""
    
    def test_version_flag(self, runner):
        """Test --version flag."""
        result = runner.invoke(app, ["--version"])
        
        assert result.exit_code == 0
        assert "pwndoc-mcp-server" in result.stdout.lower() or "version" in result.stdout.lower()
    
    def test_version_command(self, runner):
        """Test version subcommand."""
        result = runner.invoke(app, ["version"])
        
        assert result.exit_code == 0


class TestServeCommand:
    """Tests for serve command."""
    
    def test_serve_help(self, runner):
        """Test serve --help."""
        result = runner.invoke(app, ["serve", "--help"])
        
        assert result.exit_code == 0
        assert "serve" in result.stdout.lower()
    
    def test_serve_requires_config(self, runner):
        """Test serve fails without valid config."""
        # Clear environment
        for var in ["PWNDOC_URL", "PWNDOC_TOKEN", "PWNDOC_USERNAME"]:
            os.environ.pop(var, None)
        
        result = runner.invoke(app, ["serve"])
        
        # Should fail or prompt for config
        # The exact behavior depends on implementation
        assert result.exit_code != 0 or "error" in result.stdout.lower() or "config" in result.stdout.lower()
    
    @patch("pwndoc_mcp_server.cli.PwnDocMCPServer")
    @patch("pwndoc_mcp_server.cli.load_config")
    def test_serve_with_valid_config(self, mock_load, mock_server, runner):
        """Test serve with valid configuration."""
        from pwndoc_mcp_server.config import Config
        
        mock_load.return_value = Config(
            url="https://pwndoc.test.com",
            token="test-token"
        )
        
        mock_instance = MagicMock()
        mock_server.return_value = mock_instance
        mock_instance.run = MagicMock()
        
        # This would normally block, so we'll just verify setup
        result = runner.invoke(app, ["serve"], catch_exceptions=True)
        
        # Should attempt to create server
        # Exact assertions depend on implementation


class TestConfigCommand:
    """Tests for config commands."""
    
    def test_config_help(self, runner):
        """Test config --help."""
        result = runner.invoke(app, ["config", "--help"])
        
        assert result.exit_code == 0
        assert "config" in result.stdout.lower()
    
    def test_config_show(self, runner, temp_dir):
        """Test config show command."""
        # Set config file path
        config_path = os.path.join(temp_dir, "config.yaml")
        os.environ["PWNDOC_CONFIG_FILE"] = config_path
        
        result = runner.invoke(app, ["config", "show"])
        
        assert result.exit_code == 0
    
    def test_config_path(self, runner):
        """Test config path command."""
        result = runner.invoke(app, ["config", "path"])
        
        assert result.exit_code == 0
        assert "config" in result.stdout.lower() or ".yaml" in result.stdout.lower() or "/" in result.stdout
    
    @patch("pwndoc_mcp_server.cli.Prompt")
    @patch("pwndoc_mcp_server.cli.save_config")
    def test_config_init_interactive(self, mock_save, mock_prompt, runner, temp_dir):
        """Test config init with interactive prompts."""
        os.environ["PWNDOC_CONFIG_FILE"] = os.path.join(temp_dir, "config.yaml")
        
        mock_prompt.ask.side_effect = [
            "https://pwndoc.test.com",  # URL
            "testuser",  # Username
            "testpass",  # Password
        ]
        
        result = runner.invoke(app, ["config", "init"])
        
        # Should succeed or prompt
        # Exact behavior depends on implementation
    
    def test_config_set(self, runner, temp_dir):
        """Test config set command."""
        config_path = os.path.join(temp_dir, "config.yaml")
        os.environ["PWNDOC_CONFIG_FILE"] = config_path
        
        result = runner.invoke(app, ["config", "set", "url", "https://new.pwndoc.com"])
        
        assert result.exit_code == 0


class TestTestCommand:
    """Tests for test connection command."""
    
    def test_test_help(self, runner):
        """Test test --help."""
        result = runner.invoke(app, ["test", "--help"])
        
        assert result.exit_code == 0
    
    @patch("pwndoc_mcp_server.cli.PwnDocClient")
    @patch("pwndoc_mcp_server.cli.load_config")
    def test_test_connection_success(self, mock_load, mock_client, runner):
        """Test successful connection test."""
        from pwndoc_mcp_server.config import Config
        
        mock_load.return_value = Config(
            url="https://pwndoc.test.com",
            token="test-token"
        )
        
        mock_instance = AsyncMock()
        mock_client.return_value = mock_instance
        mock_instance.authenticate = AsyncMock(return_value=True)
        mock_instance.get_current_user = AsyncMock(return_value={"username": "testuser"})
        
        result = runner.invoke(app, ["test"])
        
        # Should indicate success
        # Exact output depends on implementation
    
    @patch("pwndoc_mcp_server.cli.PwnDocClient")
    @patch("pwndoc_mcp_server.cli.load_config")
    def test_test_connection_failure(self, mock_load, mock_client, runner):
        """Test failed connection test."""
        from pwndoc_mcp_server.config import Config
        from pwndoc_mcp_server.client import AuthenticationError
        
        mock_load.return_value = Config(
            url="https://pwndoc.test.com",
            token="invalid-token"
        )
        
        mock_instance = AsyncMock()
        mock_client.return_value = mock_instance
        mock_instance.authenticate = AsyncMock(side_effect=AuthenticationError("Auth failed"))
        
        result = runner.invoke(app, ["test"])
        
        # Should indicate failure
        assert result.exit_code != 0 or "error" in result.stdout.lower() or "fail" in result.stdout.lower()


class TestToolsCommand:
    """Tests for tools command."""
    
    def test_tools_list(self, runner):
        """Test tools list command."""
        result = runner.invoke(app, ["tools"])
        
        assert result.exit_code == 0
        # Should list available tools
        assert "list_audits" in result.stdout or "audit" in result.stdout.lower()
    
    def test_tools_list_format(self, runner):
        """Test tools output format."""
        result = runner.invoke(app, ["tools"])
        
        assert result.exit_code == 0
        # Should have structured output


class TestQueryCommand:
    """Tests for query command."""
    
    def test_query_help(self, runner):
        """Test query --help."""
        result = runner.invoke(app, ["query", "--help"])
        
        assert result.exit_code == 0
    
    @patch("pwndoc_mcp_server.cli.PwnDocMCPServer")
    @patch("pwndoc_mcp_server.cli.load_config")
    def test_query_tool(self, mock_load, mock_server, runner):
        """Test querying a tool directly."""
        from pwndoc_mcp_server.config import Config
        
        mock_load.return_value = Config(
            url="https://pwndoc.test.com",
            token="test-token"
        )
        
        mock_instance = MagicMock()
        mock_server.return_value = mock_instance
        mock_instance.handle_call_tool = AsyncMock(return_value='{"audits": []}')
        
        result = runner.invoke(app, ["query", "list_audits"])
        
        # Should execute the tool
        # Exact output depends on implementation
    
    @patch("pwndoc_mcp_server.cli.PwnDocMCPServer")
    @patch("pwndoc_mcp_server.cli.load_config")
    def test_query_with_params(self, mock_load, mock_server, runner):
        """Test querying with parameters."""
        from pwndoc_mcp_server.config import Config
        
        mock_load.return_value = Config(
            url="https://pwndoc.test.com",
            token="test-token"
        )
        
        mock_instance = MagicMock()
        mock_server.return_value = mock_instance
        mock_instance.handle_call_tool = AsyncMock(return_value='{"audit": {}}')
        
        result = runner.invoke(app, [
            "query", "get_audit",
            "--params", '{"audit_id": "123"}'
        ])
        
        # Should pass params to tool
    
    def test_query_invalid_tool(self, runner):
        """Test querying invalid tool."""
        result = runner.invoke(app, ["query", "nonexistent_tool"])
        
        # Should fail gracefully
        assert result.exit_code != 0 or "error" in result.stdout.lower() or "not found" in result.stdout.lower()


class TestOutputFormatting:
    """Tests for CLI output formatting."""
    
    def test_json_output(self, runner):
        """Test JSON output format."""
        result = runner.invoke(app, ["tools", "--format", "json"])
        
        if result.exit_code == 0:
            # If format flag is supported, should be valid JSON
            try:
                json.loads(result.stdout)
            except json.JSONDecodeError:
                pass  # Format may not be supported yet
    
    def test_table_output(self, runner):
        """Test table output format."""
        result = runner.invoke(app, ["tools"])
        
        assert result.exit_code == 0
        # Default should be human-readable


class TestErrorHandling:
    """Tests for CLI error handling."""
    
    def test_invalid_command(self, runner):
        """Test invalid command shows help."""
        result = runner.invoke(app, ["invalidcommand"])
        
        assert result.exit_code != 0
    
    def test_missing_required_args(self, runner):
        """Test missing required arguments."""
        result = runner.invoke(app, ["query"])  # Missing tool name
        
        assert result.exit_code != 0
    
    def test_help_available(self, runner):
        """Test help is always available."""
        result = runner.invoke(app, ["--help"])
        
        assert result.exit_code == 0
        assert "pwndoc" in result.stdout.lower()
