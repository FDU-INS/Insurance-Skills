"""Logging configuration for HealthSim applications.

Provides standardized logging setup across all HealthSim products.
"""

import logging
import sys
from typing import TextIO


def setup_logging(
    level: str = "INFO",
    app_name: str = "healthsim",
    stream: TextIO | None = None,
    format_string: str | None = None,
) -> logging.Logger:
    """Configure logging for a HealthSim application.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        app_name: Application name for the logger
        stream: Output stream (defaults to sys.stderr)
        format_string: Custom format string (optional)

    Returns:
        Configured logger instance

    Example:
        >>> logger = setup_logging(level="DEBUG", app_name="patientsim")
        >>> logger.info("Application started")
    """
    if format_string is None:
        format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    if stream is None:
        stream = sys.stderr

    # Get or create logger
    logger = logging.getLogger(app_name)
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()

    # Create handler
    handler = logging.StreamHandler(stream)
    handler.setLevel(getattr(logging, level.upper(), logging.INFO))

    # Create formatter
    formatter = logging.Formatter(format_string)
    handler.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(handler)

    return logger
