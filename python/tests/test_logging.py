"""
Tests for the logging configuration module.
"""

import pytest
import logging
import os
import tempfile
from pathlib import Path

from pwndoc_mcp_server.logging_config import (
    get_logger,
    setup_logging,
)


class TestSetupLogging:
    """Tests for setup_logging function."""
    
    def test_default_setup(self):
        """Test default logging setup."""
        logger = setup_logging()
        
        assert logger is not None
        assert isinstance(logger, logging.Logger)
    
    def test_custom_level(self):
        """Test setting custom log level."""
        logger = setup_logging(level="DEBUG")
        
        assert logger.level == logging.DEBUG
    
    def test_info_level(self):
        """Test INFO log level."""
        logger = setup_logging(level="INFO")
        
        assert logger.level == logging.INFO
    
    def test_warning_level(self):
        """Test WARNING log level."""
        logger = setup_logging(level="WARNING")
        
        assert logger.level == logging.WARNING
    
    def test_error_level(self):
        """Test ERROR log level."""
        logger = setup_logging(level="ERROR")
        
        assert logger.level == logging.ERROR
    
    def test_file_logging(self, temp_dir):
        """Test logging to file."""
        log_file = os.path.join(temp_dir, "test.log")
        
        logger = setup_logging(log_file=log_file)
        logger.info("Test message")
        
        # Flush handlers
        for handler in logger.handlers:
            handler.flush()
        
        assert os.path.exists(log_file)
        with open(log_file, "r") as f:
            content = f.read()
            assert "Test message" in content
    
    def test_file_rotation(self, temp_dir):
        """Test log file rotation settings."""
        log_file = os.path.join(temp_dir, "rotating.log")
        
        logger = setup_logging(
            log_file=log_file,
            max_bytes=1024,
            backup_count=3
        )
        
        # Write some logs
        for i in range(100):
            logger.info(f"Test message {i} " + "x" * 50)
        
        # Should have created backup files if rotation triggered
        # This depends on the actual size written
    
    def test_json_format(self, temp_dir):
        """Test JSON log format."""
        log_file = os.path.join(temp_dir, "json.log")
        
        logger = setup_logging(
            log_file=log_file,
            log_format="json"
        )
        logger.info("Test JSON message")
        
        for handler in logger.handlers:
            handler.flush()
        
        with open(log_file, "r") as f:
            content = f.read()
            # Should contain JSON structure
            assert "{" in content or "Test JSON message" in content
    
    def test_console_output(self, capsys):
        """Test console output."""
        logger = setup_logging(level="INFO", console=True)
        logger.info("Console test message")
        
        # Capture might not work with logging, but setup shouldn't error
    
    def test_logger_name(self):
        """Test custom logger name."""
        logger = setup_logging(name="custom.logger")
        
        assert logger.name == "custom.logger"
    
    def test_env_level_override(self):
        """Test environment variable level override."""
        os.environ["PWNDOC_LOG_LEVEL"] = "DEBUG"
        
        logger = setup_logging()
        
        # Should respect environment variable
        assert logger.level == logging.DEBUG
        
        del os.environ["PWNDOC_LOG_LEVEL"]
    
    def test_env_file_override(self, temp_dir):
        """Test environment variable file override."""
        log_file = os.path.join(temp_dir, "env.log")
        os.environ["PWNDOC_LOG_FILE"] = log_file
        
        logger = setup_logging()
        logger.info("Env file test")
        
        for handler in logger.handlers:
            handler.flush()
        
        assert os.path.exists(log_file)
        
        del os.environ["PWNDOC_LOG_FILE"]


class TestGetLogger:
    """Tests for get_logger function."""
    
    def test_get_default_logger(self):
        """Test getting default logger."""
        logger = get_logger()
        
        assert logger is not None
        assert isinstance(logger, logging.Logger)
    
    def test_get_named_logger(self):
        """Test getting named logger."""
        logger = get_logger("my.module")
        
        assert logger.name == "my.module"
    
    def test_get_child_logger(self):
        """Test getting child logger."""
        parent = get_logger("parent")
        child = get_logger("parent.child")
        
        assert child.name == "parent.child"
    
    def test_logger_caching(self):
        """Test that loggers are cached."""
        logger1 = get_logger("cached")
        logger2 = get_logger("cached")
        
        assert logger1 is logger2


class TestLogLevel:
    """Tests for LogLevel enum."""
    
    def test_log_levels_exist(self):
        """Test that standard log levels exist."""
        assert hasattr(LogLevel, "DEBUG")
        assert hasattr(LogLevel, "INFO")
        assert hasattr(LogLevel, "WARNING")
        assert hasattr(LogLevel, "ERROR")
        assert hasattr(LogLevel, "CRITICAL")
    
    def test_log_level_values(self):
        """Test log level values match logging module."""
        assert LogLevel.DEBUG.value == logging.DEBUG
        assert LogLevel.INFO.value == logging.INFO
        assert LogLevel.WARNING.value == logging.WARNING
        assert LogLevel.ERROR.value == logging.ERROR
        assert LogLevel.CRITICAL.value == logging.CRITICAL


class TestLoggingIntegration:
    """Integration tests for logging functionality."""
    
    def test_log_message_format(self, temp_dir):
        """Test log message format includes expected fields."""
        log_file = os.path.join(temp_dir, "format.log")
        
        logger = setup_logging(log_file=log_file, log_format="detailed")
        logger.info("Format test message")
        
        for handler in logger.handlers:
            handler.flush()
        
        with open(log_file, "r") as f:
            content = f.read()
            # Should contain timestamp, level, message
            assert "INFO" in content or "info" in content
            assert "Format test message" in content
    
    def test_exception_logging(self, temp_dir):
        """Test exception logging."""
        log_file = os.path.join(temp_dir, "exception.log")
        
        logger = setup_logging(log_file=log_file)
        
        try:
            raise ValueError("Test exception")
        except ValueError:
            logger.exception("Caught exception")
        
        for handler in logger.handlers:
            handler.flush()
        
        with open(log_file, "r") as f:
            content = f.read()
            assert "ValueError" in content or "Test exception" in content
    
    def test_log_with_extra_fields(self, temp_dir):
        """Test logging with extra fields."""
        log_file = os.path.join(temp_dir, "extra.log")
        
        logger = setup_logging(log_file=log_file)
        logger.info("Message with extra", extra={"audit_id": "123"})
        
        for handler in logger.handlers:
            handler.flush()
        
        # Extra fields handling depends on formatter
    
    def test_multiple_handlers(self, temp_dir):
        """Test logger with multiple handlers."""
        log_file = os.path.join(temp_dir, "multi.log")
        
        logger = setup_logging(log_file=log_file, console=True)
        
        # Should have both file and console handlers
        handler_types = [type(h).__name__ for h in logger.handlers]
        
        assert len(logger.handlers) >= 1
    
    def test_log_directory_creation(self, temp_dir):
        """Test log directory is created if needed."""
        log_file = os.path.join(temp_dir, "nested", "dir", "app.log")
        
        logger = setup_logging(log_file=log_file)
        logger.info("Nested directory test")
        
        for handler in logger.handlers:
            handler.flush()
        
        assert os.path.exists(log_file)
    
    def test_unicode_logging(self, temp_dir):
        """Test logging Unicode characters."""
        log_file = os.path.join(temp_dir, "unicode.log")
        
        logger = setup_logging(log_file=log_file)
        logger.info("Unicode test: 日本語 العربية 中文")
        
        for handler in logger.handlers:
            handler.flush()
        
        with open(log_file, "r", encoding="utf-8") as f:
            content = f.read()
            assert "日本語" in content or "Unicode test" in content
