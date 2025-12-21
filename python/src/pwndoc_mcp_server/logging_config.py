"""
PwnDoc MCP Server - Logging Configuration.

This module provides comprehensive logging setup with support for:
- Console output with colors
- File logging with rotation
- JSON structured logging
- Log level configuration
- Performance metrics logging

Environment Variables:
    PWNDOC_LOG_LEVEL    - Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    PWNDOC_LOG_FILE     - Path to log file
    PWNDOC_LOG_FORMAT   - Log format (text, json)
    PWNDOC_LOG_MAX_SIZE - Max log file size in MB (default: 10)
    PWNDOC_LOG_BACKUPS  - Number of backup files to keep (default: 5)

Log Levels:
    DEBUG    - Detailed information for debugging
    INFO     - General operational messages
    WARNING  - Warning messages for potential issues
    ERROR    - Error messages for failures
    CRITICAL - Critical errors that may cause shutdown

Example:
    >>> from pwndoc_mcp_server.logging_config import setup_logging
    >>> setup_logging(level="DEBUG", log_file="/var/log/pwndoc-mcp.log")
"""

import json
import logging
import logging.handlers
import os
import sys
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Optional


class LogLevel(Enum):
    """Log level enumeration."""

    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


# Custom log format
DEFAULT_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DETAILED_FORMAT = (
    "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s"
)
SIMPLE_FORMAT = "%(levelname)s: %(message)s"


class ColoredFormatter(logging.Formatter):
    """Colored log formatter for console output."""

    COLORS = {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",  # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",  # Red
        "CRITICAL": "\033[35m",  # Magenta
    }
    RESET = "\033[0m"

    def format(self, record):
        color = self.COLORS.get(record.levelname, "")
        record.levelname = f"{color}{record.levelname}{self.RESET}"
        return super().format(record)


class JSONFormatter(logging.Formatter):
    """JSON log formatter for structured logging."""

    def format(self, record) -> str:
        log_obj = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add exception info if present
        if record.exc_info:
            log_obj["exception"] = self.formatException(record.exc_info)

        # Add extra fields
        if hasattr(record, "extra"):
            log_obj.update(record.extra)

        return json.dumps(log_obj)


class SafeStreamHandler(logging.StreamHandler):
    """StreamHandler that handles Unicode encoding errors gracefully on Windows."""

    def emit(self, record):
        """Emit a record, handling Unicode encoding errors."""
        try:
            super().emit(record)
        except UnicodeEncodeError:
            # If we get an encoding error, try to encode with 'replace' errors
            try:
                msg = self.format(record)
                stream = self.stream
                # Encode with errors='replace' to substitute unmappable characters
                if hasattr(stream, "encoding") and stream.encoding:
                    # Encode and decode with replace to substitute unmappable chars
                    safe_msg = msg.encode(stream.encoding, errors="replace").decode(
                        stream.encoding, errors="replace"
                    )
                    stream.write(safe_msg)
                    stream.write(self.terminator)
                    self.flush()
                else:
                    # If no encoding info, try with utf-8
                    safe_msg = msg.encode("utf-8", errors="replace").decode(
                        "utf-8", errors="replace"
                    )
                    stream.write(safe_msg)
                    stream.write(self.terminator)
                    self.flush()
            except Exception:
                self.handleError(record)


class PerformanceLogger:
    """Logger for performance metrics."""

    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self._metrics: Dict[str, Any] = {}

    def start_timer(self, name: str):
        """Start a performance timer."""
        import time

        self._metrics[name] = {"start": time.time()}

    def stop_timer(self, name: str) -> float:
        """Stop timer and log duration."""
        import time

        if name in self._metrics:
            duration: float = time.time() - float(self._metrics[name]["start"])
            self.logger.debug(f"Performance: {name} took {duration:.3f}s")
            return duration
        return 0.0

    def log_metric(self, name: str, value: Any):
        """Log a performance metric."""
        self.logger.debug(f"Metric: {name} = {value}")


def setup_logging(
    level: str = "INFO",
    log_file: Optional[str] = None,
    log_format: str = "text",
    max_size_mb: int = 10,
    max_bytes: Optional[int] = None,
    backup_count: int = 5,
    json_output: bool = False,
    colored: bool = True,
    console: bool = True,
    name: Optional[str] = None,
) -> logging.Logger:
    """
    Configure logging for the application.

    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file (optional)
        log_format: Format type ('text', 'json', 'detailed')
        max_size_mb: Maximum log file size in MB
        max_bytes: Maximum log file size in bytes (overrides max_size_mb)
        backup_count: Number of backup files to keep
        json_output: Use JSON format for all output
        colored: Use colored output for console
        console: Enable console output (default: True)
        name: Logger name (default: root logger)

    Returns:
        Logger configured for the application

    Example:
        >>> logger = setup_logging(level="DEBUG", log_file="app.log")
        >>> logger.info("Application started")
    """
    # Check environment variables for overrides
    env_level = os.environ.get("PWNDOC_LOG_LEVEL")
    if env_level:
        level = env_level

    env_file = os.environ.get("PWNDOC_LOG_FILE")
    if env_file:
        log_file = env_file

    # Get logger (root or named)
    if name:
        root_logger = logging.getLogger(name)
    else:
        root_logger = logging.getLogger()

    root_logger.setLevel(getattr(logging, level.upper()))

    # Clear existing handlers (close them first to avoid resource warnings)
    for handler in root_logger.handlers[:]:
        handler.close()
        root_logger.removeHandler(handler)
    root_logger.handlers = []

    # Select format
    formatter: logging.Formatter
    if json_output or log_format == "json":
        formatter = JSONFormatter()
    elif log_format == "detailed":
        if colored and sys.stdout.isatty():
            formatter = ColoredFormatter(DETAILED_FORMAT)
        else:
            formatter = logging.Formatter(DETAILED_FORMAT)
    else:
        if colored and sys.stdout.isatty():
            formatter = ColoredFormatter(DEFAULT_FORMAT)
        else:
            formatter = logging.Formatter(DEFAULT_FORMAT)

    # Console handler (if enabled)
    if console:
        # On Windows, use SafeStreamHandler to handle Unicode encoding errors
        if sys.platform == "win32":
            console_handler = SafeStreamHandler(sys.stderr)
        else:
            console_handler = logging.StreamHandler(sys.stderr)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)

    # File handler (if specified)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        # Calculate max bytes
        if max_bytes is None:
            max_bytes = max_size_mb * 1024 * 1024

        # Use rotating file handler with UTF-8 encoding
        file_handler = logging.handlers.RotatingFileHandler(
            log_path,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8",
        )

        # Always use non-colored formatter for files
        if json_output:
            file_handler.setFormatter(JSONFormatter())
        else:
            file_handler.setFormatter(logging.Formatter(DEFAULT_FORMAT))

        root_logger.addHandler(file_handler)

    # Configure library loggers
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)

    return root_logger


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get a logger for a specific module.

    Args:
        name: Logger name (typically __name__), if None returns root logger

    Returns:
        Configured logger instance

    Example:
        >>> logger = get_logger(__name__)
        >>> logger.info("Module initialized")
        >>> logger = get_logger()  # Get root logger
    """
    if name is None:
        return logging.getLogger()
    return logging.getLogger(name)


def log_request(logger: logging.Logger, method: str, endpoint: str, duration: float = 0):
    """Log an API request."""
    logger.debug(f"API Request: {method} {endpoint} ({duration:.3f}s)")


def log_error(logger: logging.Logger, error: Exception, context: Optional[str] = None):
    """Log an error with context."""
    msg = f"Error: {type(error).__name__}: {error}"
    if context:
        msg = f"{context} - {msg}"
    logger.error(msg, exc_info=True)


# Environment-based configuration
def setup_from_env() -> logging.Logger:
    """
    Configure logging from environment variables.

    Environment Variables:
        PWNDOC_LOG_LEVEL    - Log level
        PWNDOC_LOG_FILE     - Log file path
        PWNDOC_LOG_FORMAT   - Format (text, json, detailed)
        PWNDOC_LOG_MAX_SIZE - Max file size in MB
        PWNDOC_LOG_BACKUPS  - Backup file count
    """
    return setup_logging(
        level=os.environ.get("PWNDOC_LOG_LEVEL", "INFO"),
        log_file=os.environ.get("PWNDOC_LOG_FILE"),
        log_format=os.environ.get("PWNDOC_LOG_FORMAT", "text"),
        max_size_mb=int(os.environ.get("PWNDOC_LOG_MAX_SIZE", "10")),
        backup_count=int(os.environ.get("PWNDOC_LOG_BACKUPS", "5")),
        json_output=os.environ.get("PWNDOC_LOG_FORMAT") == "json",
    )
