"""
Configuration management for PwnDoc MCP Server.

Supports multiple configuration sources:
1. Environment variables (highest priority)
2. Configuration file (~/.pwndoc-mcp/config.yaml or config.json)
3. Command-line arguments
4. Default values

Environment Variables:
    PWNDOC_URL          - PwnDoc server URL (e.g., https://pwndoc.example.com)
    PWNDOC_USERNAME     - PwnDoc username
    PWNDOC_PASSWORD     - PwnDoc password
    PWNDOC_TOKEN        - Pre-authenticated JWT token (alternative to user/pass)
    PWNDOC_VERIFY_SSL   - Verify SSL certificates (default: true)
    PWNDOC_TIMEOUT      - Request timeout in seconds (default: 30)
    PWNDOC_LOG_LEVEL    - Logging level (DEBUG, INFO, WARNING, ERROR)
    PWNDOC_LOG_FILE     - Path to log file (optional)
"""

import json
import logging
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional

import yaml  # type: ignore[import-untyped]

logger = logging.getLogger(__name__)

# Default configuration directory
DEFAULT_CONFIG_DIR = Path.home() / ".pwndoc-mcp"
DEFAULT_CONFIG_FILE = DEFAULT_CONFIG_DIR / "config.yaml"


@dataclass
class Config:
    """Configuration for PwnDoc MCP Server."""

    # Connection settings
    url: str = ""
    username: str = ""
    password: str = ""
    token: str = ""

    # SSL and network settings
    verify_ssl: bool = True
    timeout: int = 30
    max_retries: int = 3
    retry_delay: float = 1.0

    # Rate limiting
    rate_limit_requests: int = 100
    rate_limit_period: int = 60  # seconds

    # Logging settings
    log_level: str = "INFO"
    log_file: str = ""
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # MCP settings
    mcp_transport: str = "stdio"  # stdio, sse, websocket
    mcp_host: str = "127.0.0.1"
    mcp_port: int = 8080

    # Feature flags
    enable_caching: bool = True
    cache_ttl: int = 300  # seconds
    enable_metrics: bool = False

    # Custom fields
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate configuration after initialization."""
        self._validate()

    def _validate(self) -> None:
        """Validate configuration values."""
        if self.url and not self.url.startswith(("http://", "https://")):
            raise ValueError(f"Invalid URL format: {self.url}")

        if self.timeout < 1:
            raise ValueError(f"Timeout must be positive: {self.timeout}")

        valid_log_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if self.log_level.upper() not in valid_log_levels:
            raise ValueError(f"Invalid log level: {self.log_level}")

        valid_transports = {"stdio", "sse", "websocket"}
        if self.mcp_transport not in valid_transports:
            raise ValueError(f"Invalid MCP transport: {self.mcp_transport}")

    @property
    def is_configured(self) -> bool:
        """Check if minimum configuration is present."""
        has_url = bool(self.url)
        has_auth = bool(self.token) or (bool(self.username) and bool(self.password))
        return has_url and has_auth

    @property
    def auth_method(self) -> str:
        """Return the authentication method being used.

        Priority: username/password (preferred) > token > none
        """
        if self.username and self.password:
            return "credentials"
        elif self.token:
            return "token"
        return "none"

    def to_dict(self, include_secrets: bool = True) -> Dict[str, Any]:
        """Convert config to dictionary.

        Args:
            include_secrets: If True, include actual passwords and tokens.
                           If False, mask them with "***"

        Returns:
            Dictionary representation of config
        """
        d = {
            "url": self.url,
            "username": self.username,
            "verify_ssl": self.verify_ssl,
            "timeout": self.timeout,
            "log_level": self.log_level,
            "mcp_transport": self.mcp_transport,
            "auth_method": self.auth_method,
        }

        if include_secrets:
            d["password"] = self.password
            d["token"] = self.token
        else:
            d["password"] = "***" if self.password else ""
            d["token"] = "***" if self.token else ""

        return d

    def to_safe_string(self) -> str:
        """Return string representation without sensitive data."""
        return (
            f"Config(url={self.url!r}, username={self.username!r}, "
            f"auth_method={self.auth_method!r}, verify_ssl={self.verify_ssl})"
        )

    def validate(self) -> list:
        """Validate configuration and return list of errors.

        Returns:
            List of error messages, empty if valid
        """
        errors = []

        if not self.url:
            errors.append("PWNDOC_URL is required")
        elif not self.url.startswith(("http://", "https://")):
            errors.append(f"Invalid URL format: {self.url}")

        if not self.token and not (self.username and self.password):
            errors.append(
                "Authentication required: provide either PWNDOC_TOKEN or PWNDOC_USERNAME/PWNDOC_PASSWORD"
            )

        if self.timeout < 1:
            errors.append(f"Timeout must be positive: {self.timeout}")

        return errors

    def is_valid(self) -> bool:
        """Check if configuration is valid.

        Returns:
            True if configuration is valid
        """
        return len(self.validate()) == 0

    @classmethod
    def from_env(cls) -> "Config":
        """Create Config from environment variables.

        Returns:
            Config object populated from environment
        """
        env_config = _load_from_env()
        return cls(**env_config)


def _load_from_env() -> Dict[str, Any]:
    """Load configuration from environment variables."""
    env_mapping = {
        "PWNDOC_URL": ("url", str),
        "PWNDOC_USERNAME": ("username", str),
        "PWNDOC_PASSWORD": ("password", str),
        "PWNDOC_TOKEN": ("token", str),
        "PWNDOC_VERIFY_SSL": ("verify_ssl", lambda x: x.lower() in ("true", "1", "yes")),
        "PWNDOC_TIMEOUT": ("timeout", int),
        "PWNDOC_MAX_RETRIES": ("max_retries", int),
        "PWNDOC_LOG_LEVEL": ("log_level", str),
        "PWNDOC_LOG_FILE": ("log_file", str),
        "PWNDOC_MCP_TRANSPORT": ("mcp_transport", str),
        "PWNDOC_MCP_HOST": ("mcp_host", str),
        "PWNDOC_MCP_PORT": ("mcp_port", int),
        "PWNDOC_ENABLE_CACHING": ("enable_caching", lambda x: x.lower() in ("true", "1", "yes")),
        "PWNDOC_CACHE_TTL": ("cache_ttl", int),
    }

    config = {}
    for env_var, (key, converter) in env_mapping.items():
        value = os.environ.get(env_var)
        if value is not None:
            try:
                config[key] = converter(value)  # type: ignore[operator,misc]
            except (ValueError, TypeError) as e:
                logger.warning(f"Invalid value for {env_var}: {value} ({e})")

    return config


def _load_from_file(config_path: Path) -> Dict[str, Any]:
    """Load configuration from YAML or JSON file."""
    if not config_path.exists():
        return {}

    try:
        content = config_path.read_text()

        if config_path.suffix in (".yaml", ".yml"):
            data = yaml.safe_load(content)
            return dict(data) if data else {}
        elif config_path.suffix == ".json":
            return dict(json.loads(content))
        else:
            # Try YAML first, then JSON
            try:
                data = yaml.safe_load(content)
                return dict(data) if data else {}
            except yaml.YAMLError:
                return dict(json.loads(content))
    except Exception as e:
        logger.warning(f"Failed to load config from {config_path}: {e}")
        return {}


def load_config(config_file: Optional[Path] = None, **overrides: Any) -> Config:
    """
    Load configuration from multiple sources.

    Priority (highest to lowest):
    1. Explicit overrides passed as kwargs
    2. Environment variables
    3. Configuration file
    4. Default values

    Args:
        config_file: Path to configuration file (optional)
        **overrides: Explicit configuration overrides

    Returns:
        Config: Loaded configuration object

    Example:
        >>> config = load_config()
        >>> config = load_config(url="https://pwndoc.local")
        >>> config = load_config(config_file=Path("/etc/pwndoc-mcp/config.yaml"))
    """
    # Start with empty config dict
    config_dict: Dict[str, Any] = {}

    # Load from file (lowest priority after defaults)
    if config_file is None:
        # Check PWNDOC_CONFIG_FILE environment variable first
        config_file_env = os.getenv("PWNDOC_CONFIG_FILE")
        if config_file_env:
            config_file = Path(config_file_env).expanduser()
        else:
            # Check default locations
            for path in [DEFAULT_CONFIG_FILE, DEFAULT_CONFIG_DIR / "config.json"]:
                if path.exists():
                    config_file = path
                    break

    if config_file and Path(config_file).exists():
        file_config = _load_from_file(Path(config_file))
        config_dict.update(file_config)
        logger.debug(f"Loaded config from {config_file}")

    # Load from environment (higher priority)
    env_config = _load_from_env()
    config_dict.update(env_config)

    # Apply explicit overrides (highest priority)
    config_dict.update(overrides)

    # Create and return Config object
    return Config(**config_dict)


def save_config(config: Config, config_file: Optional[Path] = None) -> Path:
    """
    Save configuration to file.

    WARNING: This will save sensitive data. Ensure proper file permissions.

    Args:
        config: Configuration object to save
        config_file: Target file path (default: ~/.pwndoc-mcp/config.yaml)

    Returns:
        Path: Path to saved configuration file
    """
    if config_file is None:
        config_file = DEFAULT_CONFIG_FILE
    elif isinstance(config_file, str):
        config_file = Path(config_file)

    # Ensure directory exists
    config_file.parent.mkdir(parents=True, exist_ok=True)

    # Convert to dict
    data = {
        "url": config.url,
        "username": config.username,
        "password": config.password,
        "token": config.token,
        "verify_ssl": config.verify_ssl,
        "timeout": config.timeout,
        "log_level": config.log_level,
        "log_file": config.log_file,
        "mcp_transport": config.mcp_transport,
    }

    # Save based on file extension
    if config_file.suffix == ".json":
        config_file.write_text(json.dumps(data, indent=2))
    else:
        config_file.write_text(yaml.dump(data, default_flow_style=False))

    # Set restrictive permissions (owner read/write only)
    config_file.chmod(0o600)

    logger.info(f"Configuration saved to {config_file}")
    return config_file


def get_config_path() -> str:
    """
    Get the path to the configuration file.

    Checks PWNDOC_CONFIG_FILE environment variable first,
    then returns the default path.

    Returns:
        Path to configuration file as string
    """
    config_path_env = os.getenv("PWNDOC_CONFIG_FILE")
    if config_path_env:
        return str(Path(config_path_env).expanduser())
    return str(DEFAULT_CONFIG_FILE)


def init_config_interactive() -> Config:
    """
    Interactive configuration wizard.

    Prompts user for configuration values and saves to default location.
    """
    print("\n" + "=" * 60)
    print("  PwnDoc MCP Server - Configuration Wizard")
    print("=" * 60 + "\n")

    url = input("PwnDoc URL (e.g., https://pwndoc.example.com): ").strip()

    print("\nAuthentication method:")
    print("  1. Username/Password")
    print("  2. JWT Token")
    auth_choice = input("Choose (1/2): ").strip()

    username = ""
    password = ""
    token = ""

    if auth_choice == "2":
        token = input("JWT Token: ").strip()
    else:
        username = input("Username: ").strip()
        import getpass

        password = getpass.getpass("Password: ")

    verify_ssl = input("\nVerify SSL certificates? (Y/n): ").strip().lower() != "n"

    log_level = input("Log level (DEBUG/INFO/WARNING/ERROR) [INFO]: ").strip().upper()
    if not log_level:
        log_level = "INFO"

    config = Config(
        url=url,
        username=username,
        password=password,
        token=token,
        verify_ssl=verify_ssl,
        log_level=log_level,
    )

    save_choice = input("\nSave configuration? (Y/n): ").strip().lower()
    if save_choice != "n":
        save_config(config)
        print(f"\n✓ Configuration saved to {DEFAULT_CONFIG_FILE}")

    return config
