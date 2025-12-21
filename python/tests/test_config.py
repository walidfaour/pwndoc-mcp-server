"""
Tests for the configuration module.
"""

import json
import os

import yaml

from pwndoc_mcp_server.config import (
    Config,
    get_config_path,
    load_config,
    save_config,
)


class TestConfig:
    """Tests for Config dataclass."""

    def test_default_values(self):
        """Test default configuration values."""
        config = Config()

        assert config.url == ""
        assert config.username == ""
        assert config.password == ""
        assert config.token == ""
        assert config.verify_ssl is True
        assert config.timeout == 30
        assert config.max_retries == 3
        assert config.log_level == "INFO"
        assert config.log_file == ""

    def test_custom_values(self):
        """Test configuration with custom values."""
        config = Config(
            url="https://pwndoc.example.com",
            username="admin",
            password="secret123",
            verify_ssl=False,
            timeout=60,
            max_retries=5,
            log_level="DEBUG",
        )

        assert config.url == "https://pwndoc.example.com"
        assert config.username == "admin"
        assert config.password == "secret123"
        assert config.verify_ssl is False
        assert config.timeout == 60
        assert config.max_retries == 5
        assert config.log_level == "DEBUG"

    def test_is_valid_with_token(self):
        """Test config validation with token."""
        config = Config(url="https://pwndoc.example.com", token="jwt-token-here")
        assert config.is_valid() is True

    def test_is_valid_with_credentials(self):
        """Test config validation with username/password."""
        config = Config(url="https://pwndoc.example.com", username="admin", password="secret")
        assert config.is_valid() is True

    def test_is_invalid_no_url(self):
        """Test config validation without URL."""
        config = Config(username="admin", password="secret")
        assert config.is_valid() is False

    def test_is_invalid_no_auth(self):
        """Test config validation without auth."""
        config = Config(url="https://pwndoc.example.com")
        assert config.is_valid() is False

    def test_to_dict(self):
        """Test conversion to dictionary."""
        config = Config(url="https://pwndoc.example.com", username="admin")
        d = config.to_dict()

        assert isinstance(d, dict)
        assert d["url"] == "https://pwndoc.example.com"
        assert d["username"] == "admin"
        assert "password" in d

    def test_to_dict_exclude_secrets(self):
        """Test conversion to dict excluding secrets."""
        config = Config(
            url="https://pwndoc.example.com", username="admin", password="secret", token="jwt-token"
        )
        d = config.to_dict(include_secrets=False)

        assert d["password"] == "***"
        assert d["token"] == "***"
        assert d["url"] == "https://pwndoc.example.com"


class TestLoadConfig:
    """Tests for load_config function."""

    def test_load_from_environment(self):
        """Test loading config from environment variables."""
        os.environ["PWNDOC_URL"] = "https://env.pwndoc.com"
        os.environ["PWNDOC_USERNAME"] = "envuser"
        os.environ["PWNDOC_PASSWORD"] = "envpass"
        os.environ["PWNDOC_VERIFY_SSL"] = "false"
        os.environ["PWNDOC_TIMEOUT"] = "45"

        config = load_config()

        assert config.url == "https://env.pwndoc.com"
        assert config.username == "envuser"
        assert config.password == "envpass"
        assert config.verify_ssl is False
        assert config.timeout == 45

    def test_load_from_yaml_file(self, temp_dir):
        """Test loading config from YAML file."""
        config_data = {
            "url": "https://yaml.pwndoc.com",
            "username": "yamluser",
            "password": "yamlpass",
            "timeout": 60,
        }

        config_path = os.path.join(temp_dir, "config.yaml")
        with open(config_path, "w") as f:
            yaml.dump(config_data, f)

        os.environ["PWNDOC_CONFIG_FILE"] = config_path
        config = load_config()

        assert config.url == "https://yaml.pwndoc.com"
        assert config.username == "yamluser"
        assert config.timeout == 60

    def test_load_from_json_file(self, temp_dir):
        """Test loading config from JSON file."""
        config_data = {
            "url": "https://json.pwndoc.com",
            "username": "jsonuser",
            "password": "jsonpass",
        }

        config_path = os.path.join(temp_dir, "config.json")
        with open(config_path, "w") as f:
            json.dump(config_data, f)

        os.environ["PWNDOC_CONFIG_FILE"] = config_path
        config = load_config()

        assert config.url == "https://json.pwndoc.com"
        assert config.username == "jsonuser"

    def test_env_overrides_file(self, temp_dir):
        """Test that environment variables override file config."""
        config_data = {"url": "https://file.pwndoc.com", "username": "fileuser"}

        config_path = os.path.join(temp_dir, "config.yaml")
        with open(config_path, "w") as f:
            yaml.dump(config_data, f)

        os.environ["PWNDOC_CONFIG_FILE"] = config_path
        os.environ["PWNDOC_URL"] = "https://env.pwndoc.com"

        config = load_config()

        # Env should override file
        assert config.url == "https://env.pwndoc.com"
        # File value should still be used where env not set
        assert config.username == "fileuser"

    def test_load_nonexistent_file(self):
        """Test loading from nonexistent file returns defaults."""
        os.environ["PWNDOC_CONFIG_FILE"] = "/nonexistent/path/config.yaml"

        config = load_config()

        assert config.url == ""
        assert config.username == ""

    def test_boolean_parsing(self):
        """Test boolean value parsing from environment."""
        test_cases = [
            ("true", True),
            ("True", True),
            ("TRUE", True),
            ("1", True),
            ("yes", True),
            ("false", False),
            ("False", False),
            ("0", False),
            ("no", False),
        ]

        for value, expected in test_cases:
            os.environ["PWNDOC_VERIFY_SSL"] = value
            config = load_config()
            assert config.verify_ssl is expected, f"Failed for value: {value}"


class TestSaveConfig:
    """Tests for save_config function."""

    def test_save_yaml_config(self, temp_dir):
        """Test saving config to YAML file."""
        config = Config(url="https://save.pwndoc.com", username="saveuser", password="savepass")

        config_path = os.path.join(temp_dir, "config.yaml")
        save_config(config, config_path)

        assert os.path.exists(config_path)

        with open(config_path, "r") as f:
            saved_data = yaml.safe_load(f)

        assert saved_data["url"] == "https://save.pwndoc.com"
        assert saved_data["username"] == "saveuser"

    def test_save_json_config(self, temp_dir):
        """Test saving config to JSON file."""
        config = Config(url="https://save.pwndoc.com", username="saveuser")

        config_path = os.path.join(temp_dir, "config.json")
        save_config(config, config_path)

        assert os.path.exists(config_path)

        with open(config_path, "r") as f:
            saved_data = json.load(f)

        assert saved_data["url"] == "https://save.pwndoc.com"

    def test_save_creates_directory(self, temp_dir):
        """Test that save creates parent directories."""
        config = Config(url="https://test.com")

        nested_path = os.path.join(temp_dir, "nested", "dir", "config.yaml")
        save_config(config, nested_path)

        assert os.path.exists(nested_path)

    def test_save_file_permissions(self, temp_dir):
        """Test that saved config has secure permissions."""
        config = Config(url="https://test.com", password="secret")

        config_path = os.path.join(temp_dir, "config.yaml")
        save_config(config, config_path)

        # Check file permissions (should be 600 on Unix)
        if os.name != "nt":  # Skip on Windows
            mode = os.stat(config_path).st_mode & 0o777
            assert mode == 0o600


class TestGetConfigPath:
    """Tests for get_config_path function."""

    def test_default_path(self):
        """Test default config path."""
        path = get_config_path()

        assert ".pwndoc-mcp" in path
        assert path.endswith("config.yaml")

    def test_custom_path_from_env(self, temp_dir):
        """Test custom path from environment."""
        custom_path = os.path.join(temp_dir, "custom.yaml")
        os.environ["PWNDOC_CONFIG_FILE"] = custom_path

        path = get_config_path()

        assert path == custom_path

    def test_path_expansion(self):
        """Test that ~ is expanded in path."""
        os.environ["PWNDOC_CONFIG_FILE"] = "~/custom/config.yaml"

        path = get_config_path()

        assert "~" not in path
        assert os.path.expanduser("~") in path
