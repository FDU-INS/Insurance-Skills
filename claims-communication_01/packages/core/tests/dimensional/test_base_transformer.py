"""Tests for the base dimensional transformer."""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

import pandas as pd
import pytest

from healthsim.dimensional import BaseDimensionalTransformer


class ConcreteTransformer(BaseDimensionalTransformer):
    """Concrete implementation for testing."""

    def transform(self) -> tuple[dict[str, pd.DataFrame], dict[str, pd.DataFrame]]:
        return ({}, {})


class TestDateToKey:
    """Tests for date_to_key method."""

    def test_date_to_key_with_date(self):
        """Test conversion with date object."""
        assert BaseDimensionalTransformer.date_to_key(date(2024, 12, 15)) == 20241215
        assert BaseDimensionalTransformer.date_to_key(date(2024, 1, 1)) == 20240101
        assert BaseDimensionalTransformer.date_to_key(date(2024, 6, 30)) == 20240630

    def test_date_to_key_with_datetime(self):
        """Test conversion with datetime object."""
        assert BaseDimensionalTransformer.date_to_key(datetime(2024, 12, 15, 10, 30)) == 20241215

    def test_date_to_key_with_string(self):
        """Test conversion with ISO string."""
        assert BaseDimensionalTransformer.date_to_key("2024-12-15") == 20241215
        assert BaseDimensionalTransformer.date_to_key("2024-01-01") == 20240101

    def test_date_to_key_with_none(self):
        """Test conversion with None."""
        assert BaseDimensionalTransformer.date_to_key(None) is None

    def test_date_to_key_with_invalid_string(self):
        """Test conversion with invalid string."""
        assert BaseDimensionalTransformer.date_to_key("not-a-date") is None
        assert BaseDimensionalTransformer.date_to_key("2024/12/15") is None


class TestKeyToDate:
    """Tests for key_to_date method."""

    def test_key_to_date_basic(self):
        """Test basic conversion."""
        assert BaseDimensionalTransformer.key_to_date(20241215) == date(2024, 12, 15)
        assert BaseDimensionalTransformer.key_to_date(20240101) == date(2024, 1, 1)
        assert BaseDimensionalTransformer.key_to_date(20240630) == date(2024, 6, 30)

    def test_key_to_date_with_none(self):
        """Test conversion with None."""
        assert BaseDimensionalTransformer.key_to_date(None) is None

    def test_key_to_date_with_invalid_key(self):
        """Test conversion with invalid key."""
        assert BaseDimensionalTransformer.key_to_date(2024121) is None  # Too short
        assert BaseDimensionalTransformer.key_to_date(202412150) is None  # Too long
        assert BaseDimensionalTransformer.key_to_date(20241332) is None  # Invalid month
        assert BaseDimensionalTransformer.key_to_date(20240230) is None  # Invalid day

    def test_roundtrip_date_conversion(self):
        """Test that date_to_key and key_to_date are inverse operations."""
        test_date = date(2024, 6, 15)
        key = BaseDimensionalTransformer.date_to_key(test_date)
        recovered = BaseDimensionalTransformer.key_to_date(key)
        assert recovered == test_date


class TestCalculateAge:
    """Tests for calculate_age method."""

    def test_calculate_age_exact_birthday(self):
        """Test age on exact birthday."""
        assert BaseDimensionalTransformer.calculate_age("1990-06-15", "2024-06-15") == 34

    def test_calculate_age_day_before_birthday(self):
        """Test age day before birthday."""
        assert BaseDimensionalTransformer.calculate_age("1990-06-15", "2024-06-14") == 33

    def test_calculate_age_day_after_birthday(self):
        """Test age day after birthday."""
        assert BaseDimensionalTransformer.calculate_age("1990-06-15", "2024-06-16") == 34

    def test_calculate_age_with_date_objects(self):
        """Test age with date objects."""
        assert BaseDimensionalTransformer.calculate_age(date(2000, 1, 1), date(2024, 12, 31)) == 24

    def test_calculate_age_none_dob(self):
        """Test age with None dob."""
        assert BaseDimensionalTransformer.calculate_age(None, "2024-06-15") is None

    def test_calculate_age_defaults_to_today(self):
        """Test age defaults to today when as_of_date not provided."""
        # This should not raise an error
        result = BaseDimensionalTransformer.calculate_age("1990-01-01")
        assert isinstance(result, int)
        assert result >= 34  # At least 34 as of 2024

    def test_calculate_age_leap_year_birthday(self):
        """Test age for person born on Feb 29."""
        # Born Feb 29, 2000 (leap year)
        # On Feb 28, 2024 - still 23
        assert BaseDimensionalTransformer.calculate_age("2000-02-29", "2024-02-28") == 23
        # On Feb 29, 2024 - turns 24
        assert BaseDimensionalTransformer.calculate_age("2000-02-29", "2024-02-29") == 24
        # On Mar 1, 2024 - still 24
        assert BaseDimensionalTransformer.calculate_age("2000-02-29", "2024-03-01") == 24

    def test_calculate_age_newborn(self):
        """Test age for newborn."""
        assert BaseDimensionalTransformer.calculate_age("2024-06-15", "2024-06-15") == 0
        assert BaseDimensionalTransformer.calculate_age("2024-06-15", "2024-12-31") == 0

    def test_calculate_age_invalid_string(self):
        """Test age with invalid date string."""
        assert BaseDimensionalTransformer.calculate_age("not-a-date", "2024-06-15") is None
        assert BaseDimensionalTransformer.calculate_age("1990-06-15", "not-a-date") is None


class TestAgeBand:
    """Tests for age_band method."""

    def test_age_band_pediatric(self):
        """Test age band for pediatric ages."""
        assert BaseDimensionalTransformer.age_band(0) == "0-17"
        assert BaseDimensionalTransformer.age_band(10) == "0-17"
        assert BaseDimensionalTransformer.age_band(16) == "0-17"
        assert BaseDimensionalTransformer.age_band(17) == "0-17"

    def test_age_band_young_adult(self):
        """Test age band for young adults."""
        assert BaseDimensionalTransformer.age_band(18) == "18-34"
        assert BaseDimensionalTransformer.age_band(25) == "18-34"
        assert BaseDimensionalTransformer.age_band(34) == "18-34"

    def test_age_band_middle_age(self):
        """Test age band for middle age."""
        assert BaseDimensionalTransformer.age_band(35) == "35-49"
        assert BaseDimensionalTransformer.age_band(45) == "35-49"
        assert BaseDimensionalTransformer.age_band(49) == "35-49"

    def test_age_band_older_adult(self):
        """Test age band for older adults."""
        assert BaseDimensionalTransformer.age_band(50) == "50-64"
        assert BaseDimensionalTransformer.age_band(55) == "50-64"
        assert BaseDimensionalTransformer.age_band(64) == "50-64"

    def test_age_band_senior(self):
        """Test age band for seniors."""
        assert BaseDimensionalTransformer.age_band(65) == "65+"
        assert BaseDimensionalTransformer.age_band(70) == "65+"
        assert BaseDimensionalTransformer.age_band(100) == "65+"

    def test_age_band_none(self):
        """Test age band with None."""
        assert BaseDimensionalTransformer.age_band(None) is None

    def test_age_band_negative(self):
        """Test age band with negative age."""
        assert BaseDimensionalTransformer.age_band(-1) is None


class TestCleanString:
    """Tests for clean_string method."""

    def test_clean_string_basic(self):
        """Test basic string cleaning."""
        assert BaseDimensionalTransformer.clean_string("hello") == "HELLO"
        assert BaseDimensionalTransformer.clean_string("Hello World") == "HELLO WORLD"

    def test_clean_string_strips_whitespace(self):
        """Test whitespace stripping."""
        assert BaseDimensionalTransformer.clean_string("  hello  ") == "HELLO"
        assert BaseDimensionalTransformer.clean_string("\t\nhello\t\n") == "HELLO"

    def test_clean_string_preserves_case(self):
        """Test preserving case."""
        assert BaseDimensionalTransformer.clean_string("  Hello  ", uppercase=False) == "Hello"

    def test_clean_string_none(self):
        """Test with None."""
        assert BaseDimensionalTransformer.clean_string(None) is None

    def test_clean_string_empty(self):
        """Test with empty string."""
        assert BaseDimensionalTransformer.clean_string("") is None
        assert BaseDimensionalTransformer.clean_string("   ") is None


class TestSafeDecimal:
    """Tests for safe_decimal method."""

    def test_safe_decimal_from_string(self):
        """Test conversion from string."""
        assert BaseDimensionalTransformer.safe_decimal("123.456") == Decimal("123.46")
        assert BaseDimensionalTransformer.safe_decimal("100") == Decimal("100.00")

    def test_safe_decimal_from_int(self):
        """Test conversion from int."""
        assert BaseDimensionalTransformer.safe_decimal(100) == Decimal("100.00")
        assert BaseDimensionalTransformer.safe_decimal(100, precision=0) == Decimal("100")

    def test_safe_decimal_from_float(self):
        """Test conversion from float."""
        assert BaseDimensionalTransformer.safe_decimal(123.456) == Decimal("123.46")

    def test_safe_decimal_from_decimal(self):
        """Test conversion from Decimal."""
        assert BaseDimensionalTransformer.safe_decimal(Decimal("123.456")) == Decimal("123.46")

    def test_safe_decimal_precision(self):
        """Test precision parameter."""
        assert BaseDimensionalTransformer.safe_decimal("123.456", precision=0) == Decimal("123")
        assert BaseDimensionalTransformer.safe_decimal("123.456", precision=1) == Decimal("123.5")
        assert BaseDimensionalTransformer.safe_decimal("123.456", precision=3) == Decimal("123.456")

    def test_safe_decimal_rounding(self):
        """Test rounding behavior (half up)."""
        assert BaseDimensionalTransformer.safe_decimal("123.455") == Decimal("123.46")
        assert BaseDimensionalTransformer.safe_decimal("123.444") == Decimal("123.44")

    def test_safe_decimal_none(self):
        """Test with None."""
        assert BaseDimensionalTransformer.safe_decimal(None) is None

    def test_safe_decimal_default(self):
        """Test default value."""
        assert BaseDimensionalTransformer.safe_decimal(None, default=Decimal("0")) == Decimal("0")
        assert BaseDimensionalTransformer.safe_decimal("invalid", default=Decimal("0")) == Decimal(
            "0"
        )

    def test_safe_decimal_invalid(self):
        """Test with invalid value."""
        assert BaseDimensionalTransformer.safe_decimal("invalid") is None
        assert BaseDimensionalTransformer.safe_decimal("abc123") is None


class TestSafeInt:
    """Tests for safe_int method."""

    def test_safe_int_from_string(self):
        """Test conversion from string."""
        assert BaseDimensionalTransformer.safe_int("42") == 42
        assert BaseDimensionalTransformer.safe_int("-10") == -10

    def test_safe_int_from_float(self):
        """Test conversion from float."""
        assert BaseDimensionalTransformer.safe_int(3.7) == 3
        assert BaseDimensionalTransformer.safe_int(3.2) == 3

    def test_safe_int_from_int(self):
        """Test conversion from int."""
        assert BaseDimensionalTransformer.safe_int(42) == 42

    def test_safe_int_none(self):
        """Test with None."""
        assert BaseDimensionalTransformer.safe_int(None) is None

    def test_safe_int_default(self):
        """Test default value."""
        assert BaseDimensionalTransformer.safe_int(None, default=0) == 0
        assert BaseDimensionalTransformer.safe_int("invalid", default=0) == 0

    def test_safe_int_invalid(self):
        """Test with invalid value."""
        assert BaseDimensionalTransformer.safe_int("invalid") is None
        assert BaseDimensionalTransformer.safe_int("12.34") is None


class TestGetAttr:
    """Tests for get_attr method."""

    def test_get_attr_simple_object(self):
        """Test simple attribute access on object."""

        class Person:
            name = "John"
            age = 30

        person = Person()
        assert BaseDimensionalTransformer.get_attr(person, "name") == "John"
        assert BaseDimensionalTransformer.get_attr(person, "age") == 30

    def test_get_attr_nested_object(self):
        """Test nested attribute access on object."""

        class Address:
            city = "Boston"
            state = "MA"

        class Person:
            address = Address()

        person = Person()
        assert BaseDimensionalTransformer.get_attr(person, "address.city") == "Boston"
        assert BaseDimensionalTransformer.get_attr(person, "address.state") == "MA"

    def test_get_attr_simple_dict(self):
        """Test simple key access on dict."""
        data = {"name": "John", "age": 30}
        assert BaseDimensionalTransformer.get_attr(data, "name") == "John"
        assert BaseDimensionalTransformer.get_attr(data, "age") == 30

    def test_get_attr_nested_dict(self):
        """Test nested key access on dict."""
        data = {"address": {"city": "Boston", "state": "MA"}}
        assert BaseDimensionalTransformer.get_attr(data, "address.city") == "Boston"
        assert BaseDimensionalTransformer.get_attr(data, "address.state") == "MA"

    def test_get_attr_mixed_nesting(self):
        """Test mixed object and dict nesting."""

        class Person:
            info = {"name": "John", "details": {"age": 30}}

        person = Person()
        assert BaseDimensionalTransformer.get_attr(person, "info.name") == "John"
        assert BaseDimensionalTransformer.get_attr(person, "info.details.age") == 30

    def test_get_attr_missing_attribute(self):
        """Test missing attribute returns default."""

        class Person:
            name = "John"

        person = Person()
        assert BaseDimensionalTransformer.get_attr(person, "missing") is None
        assert BaseDimensionalTransformer.get_attr(person, "missing", "N/A") == "N/A"

    def test_get_attr_missing_nested(self):
        """Test missing nested attribute returns default."""

        class Person:
            name = "John"

        person = Person()
        assert BaseDimensionalTransformer.get_attr(person, "address.city") is None
        assert BaseDimensionalTransformer.get_attr(person, "address.city", "Unknown") == "Unknown"

    def test_get_attr_none_object(self):
        """Test with None object."""
        assert BaseDimensionalTransformer.get_attr(None, "name") is None
        assert BaseDimensionalTransformer.get_attr(None, "name", "default") == "default"

    def test_get_attr_empty_path(self):
        """Test with empty path."""
        data = {"name": "John"}
        assert BaseDimensionalTransformer.get_attr(data, "") is None

    def test_get_attr_deeply_nested(self):
        """Test deeply nested access."""
        data = {"a": {"b": {"c": {"d": "value"}}}}
        assert BaseDimensionalTransformer.get_attr(data, "a.b.c.d") == "value"


class TestConcreteTransformer:
    """Tests for transformer interface."""

    def test_transform_returns_tuple(self):
        """Test that transform returns correct tuple structure."""
        transformer = ConcreteTransformer()
        dimensions, facts = transformer.transform()

        assert isinstance(dimensions, dict)
        assert isinstance(facts, dict)

    def test_abstract_method_required(self):
        """Test that transform must be implemented."""

        class IncompleteTransformer(BaseDimensionalTransformer):
            pass

        with pytest.raises(TypeError):
            IncompleteTransformer()  # Can't instantiate without transform()
