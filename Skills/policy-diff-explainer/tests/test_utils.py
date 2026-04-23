"""
Tests for utils module.
"""

from __future__ import annotations

import pytest

from src.utils import (
    clamp,
    normalize,
    one_hot_encode,
    format_currency,
    format_percentage,
    truncate_text,
    generate_scenario_name,
)


class TestClamp:
    """Tests for clamp function."""

    def test_value_within_range(self) -> None:
        """Value within range should be unchanged."""
        assert clamp(0.5, 0.0, 1.0) == 0.5

    def test_value_below_min(self) -> None:
        """Value below min should be clamped to min."""
        assert clamp(-0.5, 0.0, 1.0) == 0.0

    def test_value_above_max(self) -> None:
        """Value above max should be clamped to max."""
        assert clamp(1.5, 0.0, 1.0) == 1.0


class TestNormalize:
    """Tests for normalize function."""

    def test_normalize_midpoint(self) -> None:
        """Midpoint of range should normalize to 0.5."""
        assert normalize(50, 0, 100) == 0.5

    def test_normalize_min(self) -> None:
        """Minimum value should normalize to 0."""
        assert normalize(0, 0, 100) == 0.0

    def test_normalize_max(self) -> None:
        """Maximum value should normalize to 1."""
        assert normalize(100, 0, 100) == 1.0


class TestOneHotEncode:
    """Tests for one_hot_encode function."""

    def test_first_category(self) -> None:
        """First category should have 1 at index 0."""
        result = one_hot_encode("Low", ["Low", "Middle", "High"])
        assert result == [1.0, 0.0, 0.0]

    def test_middle_category(self) -> None:
        """Middle category should have 1 at index 1."""
        result = one_hot_encode("Middle", ["Low", "Middle", "High"])
        assert result == [0.0, 1.0, 0.0]


class TestFormatCurrency:
    """Tests for format_currency function."""

    def test_format_with_thousands(self) -> None:
        """Should format with comma separators."""
        assert format_currency(48500) == "$48,500"

    def test_format_large_number(self) -> None:
        """Should handle large numbers."""
        assert format_currency(1250000) == "$1,250,000"


class TestFormatPercentage:
    """Tests for format_percentage function."""

    def test_format_basic(self) -> None:
        """Should format as percentage."""
        assert format_percentage(0.5) == "50.0%"

    def test_format_with_sign_positive(self) -> None:
        """Positive values should show + sign when requested."""
        assert format_percentage(0.25, include_sign=True) == "+25.0%"

    def test_format_with_sign_negative(self) -> None:
        """Negative values should show - sign."""
        assert format_percentage(-0.1, include_sign=True) == "-10.0%"


class TestTruncateText:
    """Tests for truncate_text function."""

    def test_short_text_unchanged(self) -> None:
        """Text shorter than max should be unchanged."""
        assert truncate_text("Hello", 10) == "Hello"

    def test_long_text_truncated(self) -> None:
        """Long text should be truncated with suffix."""
        assert truncate_text("Hello World", 8) == "Hello..."


class TestGenerateScenarioName:
    """Tests for generate_scenario_name function."""

    def test_basic_generation(self) -> None:
        """Should combine policy title and mode."""
        name = generate_scenario_name("Tax Increase", "Precision")
        assert name == "Tax Increase - Precision"

    def test_long_title_truncated(self) -> None:
        """Long policy titles should be truncated."""
        name = generate_scenario_name(
            "A Very Long Policy Title That Exceeds The Maximum Length",
            "Balanced"
        )
        assert "Balanced" in name
        assert len(name.split(" - ")[0]) <= 30
