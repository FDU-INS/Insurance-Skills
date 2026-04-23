"""
PolicyPulse - Utility Functions

Helper functions used across multiple modules.
Reference: TECH_STACK.md Section 9 (Module Responsibilities)

This module should have minimal dependencies.
"""

from __future__ import annotations

import numpy as np
from numpy.random import Generator


def create_rng(seed: int | None = None) -> Generator:
    """
    Create a numpy random number generator.
    
    Args:
        seed: Optional seed for reproducibility
        
    Returns:
        A numpy Generator instance
    """
    return np.random.default_rng(seed)


def clamp(value: float, min_val: float, max_val: float) -> float:
    """
    Clamp a value to a specified range.
    
    Args:
        value: The value to clamp
        min_val: Minimum allowed value
        max_val: Maximum allowed value
        
    Returns:
        The clamped value
    """
    return max(min_val, min(max_val, value))


def normalize(value: float, min_val: float, max_val: float) -> float:
    """
    Normalize a value to the 0-1 range.
    
    Args:
        value: The value to normalize
        min_val: The minimum of the original range
        max_val: The maximum of the original range
        
    Returns:
        Normalized value between 0 and 1
    """
    if max_val == min_val:
        return 0.5
    return (value - min_val) / (max_val - min_val)


def one_hot_encode(value: str, categories: list[str]) -> list[float]:
    """
    Create a one-hot encoded vector for a categorical value.
    
    Args:
        value: The categorical value to encode
        categories: List of all possible category values
        
    Returns:
        List of floats (0.0 or 1.0) representing the one-hot encoding
    """
    return [1.0 if cat == value else 0.0 for cat in categories]


def format_currency(amount: float) -> str:
    """
    Format a number as USD currency.
    
    Args:
        amount: The dollar amount
        
    Returns:
        Formatted string like "$48,500"
    """
    return f"${amount:,.0f}"


def format_percentage(value: float, include_sign: bool = False) -> str:
    """
    Format a decimal value as a percentage.
    
    Args:
        value: The decimal value (0.5 = 50%)
        include_sign: Whether to include +/- sign
        
    Returns:
        Formatted string like "50%" or "+50%"
    """
    pct = value * 100
    if include_sign and pct > 0:
        return f"+{pct:.1f}%"
    return f"{pct:.1f}%"


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """
    Truncate text to a maximum length with a suffix.
    
    Args:
        text: The text to truncate
        max_length: Maximum length including suffix
        suffix: String to append when truncated
        
    Returns:
        Truncated text with suffix if needed
    """
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix


def generate_scenario_name(policy_title: str, mode: str) -> str:
    """
    Generate a default scenario name from policy and mode.
    
    Reference: DESIGN_DOC.md Section 2.2 (Scenario Naming)
    
    Args:
        policy_title: The title of the policy
        mode: The simulation mode name
        
    Returns:
        Generated scenario name
    """
    truncated_title = truncate_text(policy_title, 30, "...")
    return f"{truncated_title} - {mode}"
