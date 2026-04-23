"""Base transformer class for dimensional model transformations.

Provides an abstract base class with common utility methods for transforming
canonical entities into dimensional model tables (facts and dimensions).
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date, datetime
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation
from typing import Any

import pandas as pd


class BaseDimensionalTransformer(ABC):
    """Abstract base class for all dimensional transformers.

    Product-specific transformers (PatientSim, MemberSim, RxMemberSim) should
    extend this class and implement the transform() method to convert their
    canonical entities into dimensional model tables.

    The utility methods provided handle common operations like date key
    conversions, age calculations, string normalization, and safe type
    coercion.

    Example:
        >>> class PatientTransformer(BaseDimensionalTransformer):
        ...     def __init__(self, patients: list[Patient]):
        ...         self.patients = patients
        ...
        ...     def transform(self):
        ...         # Build dimension and fact DataFrames
        ...         dim_patient = pd.DataFrame([...])
        ...         fact_encounters = pd.DataFrame([...])
        ...         return (
        ...             {'dim_patient': dim_patient},
        ...             {'fact_encounter': fact_encounters}
        ...         )
    """

    @abstractmethod
    def transform(self) -> tuple[dict[str, pd.DataFrame], dict[str, pd.DataFrame]]:
        """Transform canonical entities to dimensional model.

        Subclasses must implement this method to perform the actual
        transformation from canonical entities to dimensional tables.

        Returns:
            A tuple of (dimensions_dict, facts_dict) where each dict
            maps table_name -> DataFrame. Dimensions typically include
            tables like dim_patient, dim_provider, dim_date. Facts
            include tables like fact_encounter, fact_claim, etc.
        """
        pass

    @staticmethod
    def date_to_key(d: date | datetime | str | None) -> int | None:
        """Convert date to YYYYMMDD integer key.

        This is the standard date key format for dimensional models,
        allowing efficient joins and range queries on dates.

        Args:
            d: Date value as date, datetime, ISO string, or None.

        Returns:
            Integer in YYYYMMDD format (e.g., 20241215 for Dec 15, 2024),
            or None if input is None or invalid.

        Examples:
            >>> BaseDimensionalTransformer.date_to_key(date(2024, 12, 15))
            20241215
            >>> BaseDimensionalTransformer.date_to_key('2024-06-01')
            20240601
            >>> BaseDimensionalTransformer.date_to_key(None)
            None
        """
        if d is None:
            return None

        if isinstance(d, str):
            try:
                d = date.fromisoformat(d)
            except ValueError:
                return None

        if isinstance(d, datetime):
            d = d.date()

        if not isinstance(d, date):
            return None

        return int(d.strftime("%Y%m%d"))

    @staticmethod
    def key_to_date(key: int | None) -> date | None:
        """Convert YYYYMMDD integer key back to date.

        Args:
            key: Integer in YYYYMMDD format, or None.

        Returns:
            Date object, or None if key is None or invalid.

        Examples:
            >>> BaseDimensionalTransformer.key_to_date(20241215)
            datetime.date(2024, 12, 15)
            >>> BaseDimensionalTransformer.key_to_date(None)
            None
        """
        if key is None:
            return None

        try:
            key_str = str(key)
            if len(key_str) != 8:
                return None
            year = int(key_str[:4])
            month = int(key_str[4:6])
            day = int(key_str[6:8])
            return date(year, month, day)
        except (ValueError, TypeError):
            return None

    @staticmethod
    def calculate_age(dob: date | str | None, as_of_date: date | str | None = None) -> int | None:
        """Calculate age in complete years.

        Calculates age based on the number of complete years between
        the date of birth and the as-of date. Uses standard age
        calculation where age increments on the birthday.

        Args:
            dob: Date of birth as date object or ISO string.
            as_of_date: Date to calculate age as of. Defaults to today
                if not specified.

        Returns:
            Age in complete years, or None if dob is None or invalid.

        Examples:
            >>> BaseDimensionalTransformer.calculate_age('1990-06-15', '2024-06-15')
            34
            >>> BaseDimensionalTransformer.calculate_age('1990-06-15', '2024-06-14')
            33
            >>> BaseDimensionalTransformer.calculate_age(date(2000, 1, 1), date(2024, 12, 31))
            24
        """
        if dob is None:
            return None

        if isinstance(dob, str):
            try:
                dob = date.fromisoformat(dob)
            except ValueError:
                return None

        if as_of_date is None:
            as_of_date = date.today()
        elif isinstance(as_of_date, str):
            try:
                as_of_date = date.fromisoformat(as_of_date)
            except ValueError:
                return None

        if not isinstance(dob, date) or not isinstance(as_of_date, date):
            return None

        age = as_of_date.year - dob.year
        # Subtract 1 if birthday hasn't occurred yet this year
        if (as_of_date.month, as_of_date.day) < (dob.month, dob.day):
            age -= 1

        return max(0, age)

    @staticmethod
    def age_band(age: int | None) -> str | None:
        """Categorize age into standard demographic bands.

        Provides consistent age banding for analytics and reporting.

        Args:
            age: Age in years, or None.

        Returns:
            Age band string ('0-17', '18-34', '35-49', '50-64', '65+'),
            or None if age is None.

        Examples:
            >>> BaseDimensionalTransformer.age_band(16)
            '0-17'
            >>> BaseDimensionalTransformer.age_band(25)
            '18-34'
            >>> BaseDimensionalTransformer.age_band(70)
            '65+'
        """
        if age is None:
            return None

        if age < 0:
            return None

        if age <= 17:
            return "0-17"
        elif age <= 34:
            return "18-34"
        elif age <= 49:
            return "35-49"
        elif age <= 64:
            return "50-64"
        else:
            return "65+"

    @staticmethod
    def clean_string(s: str | None, uppercase: bool = True) -> str | None:
        """Normalize string: strip whitespace, optionally uppercase.

        Provides consistent string formatting for dimensional model
        values, ensuring uniform case and no leading/trailing whitespace.

        Args:
            s: String to clean, or None.
            uppercase: If True (default), convert to uppercase.
                If False, preserve original case but still strip whitespace.

        Returns:
            Cleaned string, or None if input is None or empty after stripping.

        Examples:
            >>> BaseDimensionalTransformer.clean_string('  hello world  ')
            'HELLO WORLD'
            >>> BaseDimensionalTransformer.clean_string('  Hello  ', uppercase=False)
            'Hello'
            >>> BaseDimensionalTransformer.clean_string('')
            None
        """
        if s is None:
            return None

        s = str(s).strip()
        if not s:
            return None

        return s.upper() if uppercase else s

    @staticmethod
    def safe_decimal(
        value: Any, default: Decimal | None = None, precision: int = 2
    ) -> Decimal | None:
        """Safely convert value to Decimal with specified precision.

        Handles various input types and provides consistent decimal
        precision for monetary and other precise numeric values.

        Args:
            value: Value to convert (str, int, float, Decimal, or None).
            default: Default value if conversion fails. Defaults to None.
            precision: Number of decimal places to round to. Defaults to 2.

        Returns:
            Decimal value rounded to specified precision, or default if
            conversion fails.

        Examples:
            >>> BaseDimensionalTransformer.safe_decimal('123.456')
            Decimal('123.46')
            >>> BaseDimensionalTransformer.safe_decimal(100, precision=0)
            Decimal('100')
            >>> BaseDimensionalTransformer.safe_decimal('invalid', default=Decimal('0'))
            Decimal('0')
        """
        if value is None:
            return default

        try:
            if isinstance(value, Decimal):
                d = value
            elif isinstance(value, float):
                d = Decimal(str(value))
            else:
                d = Decimal(value)

            # Round to specified precision
            quantize_str = "0." + "0" * precision if precision > 0 else "0"
            return d.quantize(Decimal(quantize_str), rounding=ROUND_HALF_UP)

        except (InvalidOperation, TypeError, ValueError):
            return default

    @staticmethod
    def safe_int(value: Any, default: int | None = None) -> int | None:
        """Safely convert value to integer.

        Handles various input types including strings and floats.

        Args:
            value: Value to convert (str, int, float, or None).
            default: Default value if conversion fails. Defaults to None.

        Returns:
            Integer value, or default if conversion fails.

        Examples:
            >>> BaseDimensionalTransformer.safe_int('42')
            42
            >>> BaseDimensionalTransformer.safe_int(3.7)
            3
            >>> BaseDimensionalTransformer.safe_int('invalid', default=0)
            0
        """
        if value is None:
            return default

        try:
            if isinstance(value, float):
                return int(value)
            return int(value)
        except (TypeError, ValueError):
            return default

    @staticmethod
    def get_attr(obj: Any, path: str, default: Any = None) -> Any:
        """Safely get nested attribute from object or dict.

        Supports both object attribute access and dictionary key access,
        with dot-notation path traversal for nested structures.

        Args:
            obj: Object or dict to get attribute from.
            path: Dot-separated path (e.g., 'address.city').
            default: Default value if path not found. Defaults to None.

        Returns:
            Value at path, or default if any part of path is not found.

        Examples:
            >>> class Address:
            ...     city = 'Boston'
            >>> class Person:
            ...     address = Address()
            >>> person = Person()
            >>> BaseDimensionalTransformer.get_attr(person, 'address.city')
            'Boston'
            >>> BaseDimensionalTransformer.get_attr({'a': {'b': 1}}, 'a.b')
            1
            >>> BaseDimensionalTransformer.get_attr(person, 'missing', 'N/A')
            'N/A'
        """
        if obj is None or not path:
            return default

        parts = path.split(".")
        current = obj

        for part in parts:
            if current is None:
                return default

            # Try dict access first
            if isinstance(current, dict):
                current = current.get(part, None)
                if current is None:
                    return default
            else:
                # Try attribute access
                try:
                    current = getattr(current, part, None)
                    if current is None:
                        return default
                except (AttributeError, TypeError):
                    return default

        return current if current is not None else default
