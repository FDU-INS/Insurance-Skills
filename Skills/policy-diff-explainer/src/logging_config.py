"""
PolicyPulse - Logging Configuration

Centralized logging setup for the application.
Reference: TECH_STACK.md Section 11 (Security Considerations)
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path


# =============================================================================
# Log Format Configuration
# =============================================================================

LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Streamlit-compatible format (simpler for UI display)
SIMPLE_FORMAT = "%(levelname)s: %(message)s"


# =============================================================================
# Logger Setup
# =============================================================================

def setup_logging(
    debug: bool = False,
    log_file: Path | None = None,
) -> logging.Logger:
    """
    Configure application-wide logging.
    
    Args:
        debug: If True, set level to DEBUG; otherwise INFO
        log_file: Optional path to write logs to file
        
    Returns:
        The root logger for PolicyPulse
    """
    # Determine log level
    level = logging.DEBUG if debug else logging.INFO
    
    # Create PolicyPulse logger
    logger = logging.getLogger("policypulse")
    logger.setLevel(level)
    
    # Clear any existing handlers
    logger.handlers.clear()
    
    # Console handler (stderr for Streamlit compatibility)
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(level)
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT, LOG_DATE_FORMAT))
    logger.addHandler(console_handler)
    
    # Optional file handler
    if log_file:
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)  # Always debug level in file
        file_handler.setFormatter(logging.Formatter(LOG_FORMAT, LOG_DATE_FORMAT))
        logger.addHandler(file_handler)
    
    # Reduce noise from third-party libraries
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("google").setLevel(logging.WARNING)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a child logger for a specific module.
    
    Args:
        name: Module name (e.g., "simulation", "llm_client")
        
    Returns:
        Logger instance for the module
        
    Usage:
        from src.logging_config import get_logger
        logger = get_logger(__name__)
        logger.info("Message")
    """
    return logging.getLogger(f"policypulse.{name}")


# =============================================================================
# Convenience Functions
# =============================================================================

def log_api_call(
    logger: logging.Logger,
    operation: str,
    success: bool,
    duration_ms: float | None = None,
    details: str | None = None,
) -> None:
    """
    Log an API call with consistent formatting.
    
    Args:
        logger: Logger instance
        operation: Name of the operation (e.g., "generate_reaction")
        success: Whether the call succeeded
        duration_ms: Optional duration in milliseconds
        details: Optional additional details
    """
    status = "✓" if success else "✗"
    duration_str = f" ({duration_ms:.0f}ms)" if duration_ms else ""
    details_str = f" - {details}" if details else ""
    
    if success:
        logger.debug(f"API {status} {operation}{duration_str}{details_str}")
    else:
        logger.warning(f"API {status} {operation}{duration_str}{details_str}")


def log_simulation_progress(
    logger: logging.Logger,
    step: int,
    total_steps: int,
    mode: str,
    citizens_processed: int,
) -> None:
    """
    Log simulation progress.
    
    Args:
        logger: Logger instance
        step: Current step number
        total_steps: Total number of steps
        mode: Simulation mode name
        citizens_processed: Number of citizens processed this step
    """
    logger.info(
        f"Step {step}/{total_steps} [{mode}] - "
        f"Processed {citizens_processed} citizens"
    )
