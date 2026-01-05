"""Tests for logging configuration."""

import json
import logging
from datetime import datetime
from pathlib import Path

import pytest

from package_name.logging import (
    SimpleConsoleFormatter,
    StructuredFileFormatter,
    get_logger,
    setup_logging,
)


class TestSimpleConsoleFormatter:
    """Tests for SimpleConsoleFormatter."""

    def test_format_basic_message(self) -> None:
        """Test basic message formatting."""
        formatter = SimpleConsoleFormatter()
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=10,
            msg="Test message",
            args=(),
            exc_info=None,
        )
        output = formatter.format(record)
        assert output == "INFO: Test message"

    def test_format_with_args(self) -> None:
        """Test message formatting with arguments."""
        formatter = SimpleConsoleFormatter()
        record = logging.LogRecord(
            name="test",
            level=logging.WARNING,
            pathname="test.py",
            lineno=10,
            msg="User %s logged in",
            args=("alice",),
            exc_info=None,
        )
        output = formatter.format(record)
        assert output == "WARNING: User alice logged in"

    def test_format_different_levels(self) -> None:
        """Test formatting with different log levels."""
        formatter = SimpleConsoleFormatter()
        levels = [
            (logging.DEBUG, "DEBUG"),
            (logging.INFO, "INFO"),
            (logging.WARNING, "WARNING"),
            (logging.ERROR, "ERROR"),
            (logging.CRITICAL, "CRITICAL"),
        ]

        for level, level_name in levels:
            record = logging.LogRecord(
                name="test",
                level=level,
                pathname="test.py",
                lineno=10,
                msg="Test",
                args=(),
                exc_info=None,
            )
            output = formatter.format(record)
            assert output == f"{level_name}: Test"


class TestStructuredFileFormatter:
    """Tests for StructuredFileFormatter."""

    def test_format_basic_message(self) -> None:
        """Test basic JSON formatting."""
        formatter = StructuredFileFormatter()
        record = logging.LogRecord(
            name="test.module",
            level=logging.INFO,
            pathname="test.py",
            lineno=42,
            msg="Test message",
            args=(),
            exc_info=None,
        )
        record.module = "test"
        record.funcName = "test_function"

        output = formatter.format(record)
        data = json.loads(output)

        assert data["level"] == "INFO"
        assert data["logger"] == "test.module"
        assert data["message"] == "Test message"
        assert data["module"] == "test"
        assert data["function"] == "test_function"
        assert data["line"] == 42

    def test_format_with_timestamp(self) -> None:
        """Test that timestamp is in ISO8601 format."""
        formatter = StructuredFileFormatter()
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=10,
            msg="Test",
            args=(),
            exc_info=None,
        )
        record.module = "test"
        record.funcName = "test_func"

        output = formatter.format(record)
        data = json.loads(output)

        # Verify ISO8601 format by parsing it
        timestamp = datetime.fromisoformat(data["timestamp"])
        assert isinstance(timestamp, datetime)
        # Should include timezone info
        assert data["timestamp"].endswith("+00:00") or data["timestamp"].endswith("Z")

    def test_format_with_exception(self) -> None:
        """Test formatting with exception information."""
        formatter = StructuredFileFormatter()

        try:
            raise ValueError("Test error")
        except ValueError:
            import sys

            exc_info = sys.exc_info()

        record = logging.LogRecord(
            name="test",
            level=logging.ERROR,
            pathname="test.py",
            lineno=10,
            msg="Error occurred",
            args=(),
            exc_info=exc_info,
        )
        record.module = "test"
        record.funcName = "test_func"

        output = formatter.format(record)
        data = json.loads(output)

        assert data["level"] == "ERROR"
        assert data["message"] == "Error occurred"
        assert "exception" in data
        assert "ValueError: Test error" in data["exception"]
        assert "Traceback" in data["exception"]


class TestSetupLogging:
    """Tests for setup_logging function."""

    def test_default_setup(self, caplog: pytest.LogCaptureFixture) -> None:
        """Test default logging setup (console only, INFO level)."""
        logger = setup_logging()

        assert logger == logging.getLogger()
        assert logger.level == logging.INFO
        assert len(logger.handlers) == 1
        assert isinstance(logger.handlers[0], logging.StreamHandler)

    def test_custom_level(self) -> None:
        """Test setting custom log level."""
        logger = setup_logging(level="DEBUG")
        assert logger.level == logging.DEBUG

        logger = setup_logging(level="WARNING")
        assert logger.level == logging.WARNING

    def test_debug_environment_variable(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test DEBUG environment variable sets debug level."""
        monkeypatch.setenv("DEBUG", "1")
        logger = setup_logging()
        assert logger.level == logging.DEBUG

    def test_console_disabled(self) -> None:
        """Test disabling console logging."""
        logger = setup_logging(console=False)
        assert len(logger.handlers) == 0

    def test_file_logging(self, tmp_path: Path) -> None:
        """Test file logging setup."""
        log_file = tmp_path / "test.log"
        logger = setup_logging(log_file=log_file)

        # Should have both console and file handlers
        assert len(logger.handlers) == 2
        file_handlers = [h for h in logger.handlers if isinstance(h, logging.FileHandler)]
        assert len(file_handlers) == 1

        # Test that file is created
        assert log_file.exists()

    def test_file_logging_creates_directories(self, tmp_path: Path) -> None:
        """Test that file logging creates parent directories."""
        log_file = tmp_path / "logs" / "app" / "test.log"
        setup_logging(log_file=log_file)

        assert log_file.parent.exists()
        assert log_file.exists()

    def test_file_only_logging(self, tmp_path: Path) -> None:
        """Test file-only logging (no console)."""
        log_file = tmp_path / "test.log"
        logger = setup_logging(console=False, log_file=log_file)

        assert len(logger.handlers) == 1
        assert isinstance(logger.handlers[0], logging.FileHandler)

    def test_logging_output_console(self, capfd: pytest.CaptureFixture[str]) -> None:
        """Test console logging output format."""
        setup_logging(level="INFO")
        logger = logging.getLogger("test")

        logger.info("Test message")

        captured = capfd.readouterr()
        assert "INFO: Test message" in captured.out

    def test_logging_output_file(self, tmp_path: Path) -> None:
        """Test file logging output format."""
        log_file = tmp_path / "test.log"
        setup_logging(level="INFO", log_file=log_file, console=False)
        logger = logging.getLogger("test.module")

        logger.info("Test file message")

        # Read and parse the log file
        content = log_file.read_text().strip()
        data = json.loads(content)

        assert data["level"] == "INFO"
        assert data["message"] == "Test file message"
        assert data["logger"] == "test.module"
        assert "timestamp" in data
        # Verify ISO8601 format
        datetime.fromisoformat(data["timestamp"])

    def test_multiple_log_entries(self, tmp_path: Path) -> None:
        """Test multiple log entries are written correctly."""
        log_file = tmp_path / "test.log"
        setup_logging(level="DEBUG", log_file=log_file, console=False)
        logger = logging.getLogger("test")

        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")

        # Read all log entries
        lines = log_file.read_text().strip().split("\n")
        assert len(lines) == 4

        # Parse each line and verify
        levels = ["DEBUG", "INFO", "WARNING", "ERROR"]
        for i, line in enumerate(lines):
            data = json.loads(line)
            assert data["level"] == levels[i]

    def test_handlers_cleared_on_setup(self) -> None:
        """Test that existing handlers are cleared when setup is called."""
        # First setup
        logger1 = setup_logging()
        handler_count_1 = len(logger1.handlers)

        # Second setup should clear previous handlers
        logger2 = setup_logging(level="DEBUG")
        handler_count_2 = len(logger2.handlers)

        # Should be same logger instance
        assert logger1 is logger2
        # Handler count should be the same (old handlers cleared)
        assert handler_count_1 == handler_count_2


class TestGetLogger:
    """Tests for get_logger function."""

    def test_get_logger_returns_logger(self) -> None:
        """Test that get_logger returns a Logger instance."""
        logger = get_logger("test.module")
        assert isinstance(logger, logging.Logger)
        assert logger.name == "test.module"

    def test_get_logger_same_instance(self) -> None:
        """Test that get_logger returns the same instance for the same name."""
        logger1 = get_logger("test.module")
        logger2 = get_logger("test.module")
        assert logger1 is logger2

    def test_get_logger_different_instances(self) -> None:
        """Test that different names return different loggers."""
        logger1 = get_logger("module1")
        logger2 = get_logger("module2")
        assert logger1 is not logger2
        assert logger1.name != logger2.name
