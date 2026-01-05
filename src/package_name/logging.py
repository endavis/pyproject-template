"""Logging configuration for package_name.

This module provides a centralized logging setup with:
- ISO8601 timestamps for all log entries
- Simple console output for human readability
- Structured JSON file output for machine processing
"""

import json
import logging
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal

LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class SimpleConsoleFormatter(logging.Formatter):
    """Simple formatter for console output with ISO8601 timestamps."""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record with simple output.

        Args:
            record: The log record to format

        Returns:
            Formatted log string: "LEVEL: message"
        """
        return f"{record.levelname}: {record.getMessage()}"


class StructuredFileFormatter(logging.Formatter):
    """Structured JSON formatter for file output with ISO8601 timestamps."""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON with ISO8601 timestamp.

        Args:
            record: The log record to format

        Returns:
            JSON-formatted log string with timestamp, level, message, and metadata
        """
        log_data: dict[str, Any] = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        # Add extra fields if present
        if hasattr(record, "extra_fields"):
            log_data["extra"] = record.extra_fields

        return json.dumps(log_data)


def setup_logging(
    level: LogLevel | None = None,
    log_file: str | Path | None = None,
    console: bool = True,
) -> logging.Logger:
    """Configure logging for the application.

    Sets up logging with:
    - Simple console output (if enabled)
    - Structured JSON file output (if log_file specified)
    - ISO8601 timestamps for all entries

    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
               Defaults to INFO, or DEBUG if DEBUG environment variable is set.
        log_file: Optional file path for structured JSON logging.
                  If provided, creates parent directories if needed.
        console: Enable console logging. Defaults to True.

    Returns:
        Configured root logger

    Examples:
        Basic console logging:
        >>> setup_logging()
        <Logger root (INFO)>

        Console and file logging:
        >>> setup_logging(level="DEBUG", log_file="app.log")
        <Logger root (DEBUG)>

        File logging only:
        >>> setup_logging(console=False, log_file="app.log")
        <Logger root (INFO)>
    """
    # Determine log level - ensure it's never None
    resolved_level: LogLevel = (
        level if level is not None else ("DEBUG" if os.getenv("DEBUG") else "INFO")
    )

    # Get root logger and clear existing handlers
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, resolved_level))
    root_logger.handlers.clear()

    # Add console handler with simple formatting
    if console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, resolved_level))
        console_handler.setFormatter(SimpleConsoleFormatter())
        root_logger.addHandler(console_handler)

    # Add file handler with structured JSON formatting
    if log_file:
        log_path = Path(log_file)
        # Create parent directories if they don't exist
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(getattr(logging, resolved_level))
        file_handler.setFormatter(StructuredFileFormatter())
        root_logger.addHandler(file_handler)

    return root_logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for a module.

    Args:
        name: Logger name (typically __name__ of the module)

    Returns:
        Logger instance

    Examples:
        >>> logger = get_logger(__name__)
        >>> logger.info("Application started")
    """
    return logging.getLogger(name)
