"""Date and time utility functions.

Provides common date/time operations used throughout HealthSim.
"""

import random
from datetime import date, datetime, timedelta

from dateutil.parser import parse as dateutil_parse


def calculate_age(birth_date: date, as_of: date | None = None) -> int:
    """Calculate age in years from a birth date.

    Args:
        birth_date: Date of birth
        as_of: Reference date (defaults to today)

    Returns:
        Age in complete years

    Example:
        >>> from datetime import date
        >>> calculate_age(date(1990, 6, 15), date(2024, 1, 1))
        33
    """
    if as_of is None:
        as_of = date.today()

    age = as_of.year - birth_date.year

    # Adjust if birthday hasn't occurred yet this year
    if (as_of.month, as_of.day) < (birth_date.month, birth_date.day):
        age -= 1

    return age


def format_datetime_iso(dt: datetime) -> str:
    """Format datetime as ISO 8601 string.

    Args:
        dt: Datetime to format

    Returns:
        ISO 8601 formatted string

    Example:
        >>> from datetime import datetime
        >>> format_datetime_iso(datetime(2024, 1, 15, 14, 30, 0))
        '2024-01-15T14:30:00'
    """
    return dt.isoformat()


def format_date_iso(d: date) -> str:
    """Format date as ISO 8601 string.

    Args:
        d: Date to format

    Returns:
        ISO 8601 formatted string (YYYY-MM-DD)

    Example:
        >>> from datetime import date
        >>> format_date_iso(date(2024, 1, 15))
        '2024-01-15'
    """
    return d.isoformat()


def parse_datetime(s: str) -> datetime:
    """Parse a datetime string in various formats.

    Uses dateutil for flexible parsing.

    Args:
        s: String to parse

    Returns:
        Parsed datetime

    Raises:
        ValueError: If string cannot be parsed

    Example:
        >>> parse_datetime("2024-01-15T14:30:00")
        datetime.datetime(2024, 1, 15, 14, 30)
        >>> parse_datetime("January 15, 2024 2:30 PM")
        datetime.datetime(2024, 1, 15, 14, 30)
    """
    return dateutil_parse(s)


def parse_date(s: str) -> date:
    """Parse a date string in various formats.

    Args:
        s: String to parse

    Returns:
        Parsed date

    Raises:
        ValueError: If string cannot be parsed

    Example:
        >>> parse_date("2024-01-15")
        datetime.date(2024, 1, 15)
    """
    return dateutil_parse(s).date()


def random_date_in_range(
    start: date,
    end: date,
    rng: random.Random | None = None,
) -> date:
    """Generate a random date within a range.

    Args:
        start: Start of range (inclusive)
        end: End of range (inclusive)
        rng: Random number generator (for reproducibility)

    Returns:
        Random date in the range

    Example:
        >>> import random
        >>> rng = random.Random(42)
        >>> random_date_in_range(date(2024, 1, 1), date(2024, 12, 31), rng)
        datetime.date(2024, 9, 11)
    """
    if rng is None:
        rng = random.Random()

    delta = end - start
    random_days = rng.randint(0, delta.days)
    return start + timedelta(days=random_days)


def random_datetime_in_range(
    start: datetime,
    end: datetime,
    rng: random.Random | None = None,
) -> datetime:
    """Generate a random datetime within a range.

    Args:
        start: Start of range (inclusive)
        end: End of range (inclusive)
        rng: Random number generator (for reproducibility)

    Returns:
        Random datetime in the range

    Example:
        >>> import random
        >>> rng = random.Random(42)
        >>> random_datetime_in_range(
        ...     datetime(2024, 1, 1, 0, 0),
        ...     datetime(2024, 1, 1, 23, 59),
        ...     rng
        ... )
        datetime.datetime(2024, 1, 1, 15, 7, ...)
    """
    if rng is None:
        rng = random.Random()

    delta = end - start
    random_seconds = rng.randint(0, int(delta.total_seconds()))
    return start + timedelta(seconds=random_seconds)


def date_range(
    start: date,
    end: date,
    step: timedelta = timedelta(days=1),
) -> list[date]:
    """Generate a list of dates in a range.

    Args:
        start: Start date (inclusive)
        end: End date (inclusive)
        step: Step between dates

    Returns:
        List of dates

    Example:
        >>> date_range(date(2024, 1, 1), date(2024, 1, 5))
        [date(2024, 1, 1), date(2024, 1, 2), date(2024, 1, 3), date(2024, 1, 4), date(2024, 1, 5)]
    """
    dates = []
    current = start
    while current <= end:
        dates.append(current)
        current += step
    return dates


def days_between(d1: date, d2: date) -> int:
    """Calculate the number of days between two dates.

    Args:
        d1: First date
        d2: Second date

    Returns:
        Number of days (positive if d2 > d1)

    Example:
        >>> days_between(date(2024, 1, 1), date(2024, 1, 15))
        14
    """
    return (d2 - d1).days


def relative_date(
    base: date, years: int = 0, months: int = 0, days: int = 0, direction: str = "after"
) -> date:
    """Calculate a date relative to a base date.

    Args:
        base: The reference date
        years: Number of years to add/subtract
        months: Number of months to add/subtract
        days: Number of days to add/subtract
        direction: "after" adds, "before" subtracts

    Returns:
        The calculated date
    """
    multiplier = 1 if direction == "after" else -1

    # Handle days simply
    result = base + timedelta(days=days * multiplier)

    # Handle months (approximate as 30 days)
    result += timedelta(days=months * 30 * multiplier)

    # Handle years
    try:
        result = result.replace(year=result.year + (years * multiplier))
    except ValueError:
        # Handle Feb 29 edge case
        result = result.replace(month=2, day=28, year=result.year + (years * multiplier))

    return result


def business_days_between(start: date, end: date) -> int:
    """Count business days (Mon-Fri) between two dates.

    Args:
        start: Start date (inclusive)
        end: End date (inclusive)

    Returns:
        Number of business days
    """
    if end < start:
        return 0
    count = 0
    current = start
    while current <= end:
        if current.weekday() < 5:  # Monday = 0, Friday = 4
            count += 1
        current += timedelta(days=1)
    return count


def next_business_day(from_date: date) -> date:
    """Get the next business day (Mon-Fri) from a date.

    Args:
        from_date: Starting date

    Returns:
        Next business day after from_date
    """
    current = from_date + timedelta(days=1)
    while current.weekday() >= 5:  # Skip weekends
        current += timedelta(days=1)
    return current


def is_future_date(check_date: date, reference: date | None = None) -> bool:
    """Check if a date is in the future relative to reference (default: today).

    Args:
        check_date: Date to check
        reference: Reference date (defaults to today)

    Returns:
        True if check_date is after reference
    """
    ref = reference or date.today()
    return check_date > ref
