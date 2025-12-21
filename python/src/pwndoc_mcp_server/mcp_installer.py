"""
MCP Configuration Installer for Claude Desktop.

Automatically configures Claude Desktop to use the PwnDoc MCP server
by updating the appropriate mcp_servers.json file for each platform.
"""

import json
import logging
import os
import platform
import shutil
import sys
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


def get_claude_config_path() -> Path:
    """
    Get the Claude Desktop MCP configuration file path for the current platform.

    Returns:
        Path to Claude's mcp_servers.json file

    Raises:
        RuntimeError: If platform is not supported
    """
    system = platform.system()

    if system == "Linux":
        return Path.home() / ".config" / "claude" / "mcp_servers.json"
    elif system == "Darwin":  # macOS
        return Path.home() / "Library" / "Application Support" / "Claude" / "mcp_servers.json"
    elif system == "Windows":
        appdata = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
        return appdata / "Claude" / "mcp_servers.json"
    else:
        raise RuntimeError(f"Unsupported platform: {system}")


def is_claude_installed() -> bool:
    """
    Check if Claude Desktop appears to be installed.

    Returns:
        True if Claude Desktop installation is detected
    """
    system = platform.system()

    if system == "Linux":
        # Check for Claude Desktop in common locations
        claude_paths = [
            Path.home() / ".local" / "share" / "applications" / "claude.desktop",
            Path("/usr/share/applications/claude.desktop"),
            Path.home() / ".config" / "claude",  # Config dir exists
        ]
        return any(p.exists() for p in claude_paths)

    elif system == "Darwin":  # macOS
        # Check for Claude.app in Applications
        app_paths = [
            Path("/Applications/Claude.app"),
            Path.home() / "Applications" / "Claude.app",
            Path.home() / "Library" / "Application Support" / "Claude",  # Config dir
        ]
        return any(p.exists() for p in app_paths)

    elif system == "Windows":
        # Check for Claude in Program Files or AppData
        appdata = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
        local_appdata = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
        claude_paths = [
            Path(os.environ.get("PROGRAMFILES", "C:\\Program Files")) / "Claude",
            local_appdata / "Programs" / "Claude",
            appdata / "Claude",  # Config dir
        ]
        return any(p.exists() for p in claude_paths)

    return False


def detect_python_executable() -> str:
    """
    Detect the Python executable being used.

    Returns:
        Path to current Python executable
    """
    return sys.executable


def detect_pwndoc_mcp_path() -> Optional[str]:
    """
    Detect the path to pwndoc-mcp executable or module.

    Returns:
        Path to pwndoc-mcp command or None if not found
    """
    # Check if installed as a package with CLI entry point
    pwndoc_mcp_bin = shutil.which("pwndoc-mcp")
    if pwndoc_mcp_bin:
        return pwndoc_mcp_bin

    # Check if we're running from source
    try:
        import pwndoc_mcp_server  # noqa: F401

        # If running from source, use python -m
        return f"{sys.executable} -m pwndoc_mcp_server.server"
    except ImportError:
        pass

    return None


def create_mcp_config(
    command: Optional[str] = None,
    args: Optional[list] = None,
    env: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """
    Create MCP server configuration for PwnDoc.

    Args:
        command: Command to run (auto-detected if None)
        args: Command arguments
        env: Environment variables

    Returns:
        MCP server configuration dict
    """
    if command is None:
        detected = detect_pwndoc_mcp_path()
        if not detected:
            raise RuntimeError("Could not detect pwndoc-mcp installation")
        command = detected

    if args is None:
        args = ["serve"]

    config: Dict[str, Any] = {
        "command": command,
        "args": args,
    }

    if env:
        config["env"] = env

    return config


def load_existing_config(config_path: Path) -> Dict[str, Any]:
    """
    Load existing Claude MCP configuration.

    Args:
        config_path: Path to mcp_servers.json

    Returns:
        Existing configuration dict or empty dict
    """
    if not config_path.exists():
        return {}

    try:
        content = config_path.read_text()
        data = json.loads(content)
        return dict(data) if isinstance(data, dict) else {}
    except Exception as e:
        logger.warning(f"Failed to load existing config: {e}")
        return {}


def save_mcp_config(config: Dict[str, Any], config_path: Path, backup: bool = True) -> None:
    """
    Save MCP configuration to Claude's config file.

    Args:
        config: Full MCP configuration dict
        config_path: Path to mcp_servers.json
        backup: Create backup before saving
    """
    # Ensure directory exists
    config_path.parent.mkdir(parents=True, exist_ok=True)

    # Create backup if requested and file exists
    if backup and config_path.exists():
        backup_path = config_path.with_suffix(".json.backup")
        shutil.copy(config_path, backup_path)
        logger.info(f"Created backup at {backup_path}")

    # Write configuration
    config_path.write_text(json.dumps(config, indent=2))
    logger.info(f"Saved configuration to {config_path}")


def install_mcp_config(
    command: Optional[str] = None,
    args: Optional[list] = None,
    env: Optional[Dict[str, str]] = None,
    force: bool = False,
) -> bool:
    """
    Install PwnDoc MCP server configuration for Claude Desktop.

    Args:
        command: Command to run (auto-detected if None)
        args: Command arguments
        env: Environment variables
        force: Overwrite existing pwndoc-mcp configuration

    Returns:
        True if installation succeeded

    Raises:
        RuntimeError: If installation fails
    """
    try:
        # Get Claude config path
        config_path = get_claude_config_path()
        logger.info(f"Claude config path: {config_path}")

        # Load existing configuration
        full_config = load_existing_config(config_path)

        # Check if pwndoc-mcp already configured
        if "pwndoc-mcp" in full_config and not force:
            logger.warning("pwndoc-mcp already configured (use --force to overwrite)")
            return False

        # Create pwndoc-mcp configuration
        pwndoc_config = create_mcp_config(command=command, args=args, env=env)

        # Add to full configuration
        full_config["pwndoc-mcp"] = pwndoc_config

        # Save configuration
        save_mcp_config(full_config, config_path)

        return True

    except Exception as e:
        logger.error(f"Failed to install MCP configuration: {e}")
        raise RuntimeError(f"Installation failed: {e}")


def uninstall_mcp_config() -> bool:
    """
    Remove PwnDoc MCP server configuration from Claude Desktop.

    Returns:
        True if removal succeeded
    """
    try:
        config_path = get_claude_config_path()

        if not config_path.exists():
            logger.info("No Claude configuration found")
            return True

        full_config = load_existing_config(config_path)

        if "pwndoc-mcp" not in full_config:
            logger.info("pwndoc-mcp not configured")
            return True

        # Remove pwndoc-mcp entry
        del full_config["pwndoc-mcp"]

        # Save updated configuration
        save_mcp_config(full_config, config_path)

        logger.info("pwndoc-mcp configuration removed")
        return True

    except Exception as e:
        logger.error(f"Failed to uninstall MCP configuration: {e}")
        return False


def show_mcp_config() -> Optional[Dict[str, Any]]:
    """
    Show current PwnDoc MCP configuration in Claude Desktop.

    Returns:
        Current pwndoc-mcp configuration or None
    """
    try:
        config_path = get_claude_config_path()

        if not config_path.exists():
            logger.info("No Claude configuration found")
            return None

        full_config = load_existing_config(config_path)

        return full_config.get("pwndoc-mcp")

    except Exception as e:
        logger.error(f"Failed to read MCP configuration: {e}")
        return None
