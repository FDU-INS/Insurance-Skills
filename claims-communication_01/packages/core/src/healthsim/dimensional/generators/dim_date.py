"""Date dimension generator with US federal holidays.

Generates a date dimension table suitable for star schema analytics,
including comprehensive date attributes and US federal holiday flags.
"""

from __future__ import annotations

from datetime import date, timedelta
from typing import TYPE_CHECKING

import pandas as pd

if TYPE_CHECKING:
    pass


def _parse_date(d: str | date) -> date:
    """Parse a date string or return a date object."""
    if isinstance(d, date):
        return d
    return date.fromisoformat(d)


def _get_nth_weekday_of_month(year: int, month: int, weekday: int, n: int) -> date:
    """Get the nth occurrence of a weekday in a month.

    Args:
        year: The year
        month: The month (1-12)
        weekday: The day of week (0=Monday, 6=Sunday)
        n: Which occurrence (1=first, 2=second, etc.)

    Returns:
        The date of the nth weekday in the month
    """
    first_day = date(year, month, 1)
    first_weekday = first_day.weekday()

    days_until_weekday = (weekday - first_weekday) % 7
    first_occurrence = first_day + timedelta(days=days_until_weekday)

    return first_occurrence + timedelta(weeks=n - 1)


def _get_last_weekday_of_month(year: int, month: int, weekday: int) -> date:
    """Get the last occurrence of a weekday in a month.

    Args:
        year: The year
        month: The month (1-12)
        weekday: The day of week (0=Monday, 6=Sunday)

    Returns:
        The date of the last weekday in the month
    """
    if month == 12:
        next_month = date(year + 1, 1, 1)
    else:
        next_month = date(year, month + 1, 1)

    last_day = next_month - timedelta(days=1)
    days_back = (last_day.weekday() - weekday) % 7
    return last_day - timedelta(days=days_back)


def _get_observed_date(holiday_date: date) -> date:
    """Get the observed date for a holiday.

    If the holiday falls on Saturday, observe on Friday.
    If the holiday falls on Sunday, observe on Monday.

    Args:
        holiday_date: The actual holiday date

    Returns:
        The observed date
    """
    weekday = holiday_date.weekday()
    if weekday == 5:  # Saturday
        return holiday_date - timedelta(days=1)
    elif weekday == 6:  # Sunday
        return holiday_date + timedelta(days=1)
    return holiday_date


def _get_us_federal_holidays(year: int) -> dict[date, str]:
    """Get all US federal holidays for a given year.

    Args:
        year: The year to get holidays for

    Returns:
        Dictionary mapping observed date to holiday name
    """
    holidays: dict[date, str] = {}

    # New Year's Day (January 1, observed)
    new_years = date(year, 1, 1)
    observed = _get_observed_date(new_years)
    holidays[observed] = "New Year's Day"

    # Martin Luther King Jr. Day (3rd Monday of January)
    mlk_day = _get_nth_weekday_of_month(year, 1, 0, 3)
    holidays[mlk_day] = "Martin Luther King Jr. Day"

    # Presidents Day (3rd Monday of February)
    presidents_day = _get_nth_weekday_of_month(year, 2, 0, 3)
    holidays[presidents_day] = "Presidents Day"

    # Memorial Day (Last Monday of May)
    memorial_day = _get_last_weekday_of_month(year, 5, 0)
    holidays[memorial_day] = "Memorial Day"

    # Juneteenth (June 19, observed)
    juneteenth = date(year, 6, 19)
    observed = _get_observed_date(juneteenth)
    holidays[observed] = "Juneteenth"

    # Independence Day (July 4, observed)
    independence_day = date(year, 7, 4)
    observed = _get_observed_date(independence_day)
    holidays[observed] = "Independence Day"

    # Labor Day (1st Monday of September)
    labor_day = _get_nth_weekday_of_month(year, 9, 0, 1)
    holidays[labor_day] = "Labor Day"

    # Columbus Day (2nd Monday of October)
    columbus_day = _get_nth_weekday_of_month(year, 10, 0, 2)
    holidays[columbus_day] = "Columbus Day"

    # Veterans Day (November 11, observed)
    veterans_day = date(year, 11, 11)
    observed = _get_observed_date(veterans_day)
    holidays[observed] = "Veterans Day"

    # Thanksgiving (4th Thursday of November)
    thanksgiving = _get_nth_weekday_of_month(year, 11, 3, 4)
    holidays[thanksgiving] = "Thanksgiving"

    # Christmas Day (December 25, observed)
    christmas = date(year, 12, 25)
    observed = _get_observed_date(christmas)
    holidays[observed] = "Christmas Day"

    return holidays


def generate_dim_date(
    start_date: str | date = "2020-01-01",
    end_date: str | date = "2030-12-31",
) -> pd.DataFrame:
    """Generate a date dimension table with US federal holidays.

    Creates a comprehensive date dimension with all standard date attributes
    plus US federal holiday flags. This is suitable for use in star schema
    dimensional models.

    Args:
        start_date: Start date (inclusive) as ISO string or date object.
            Defaults to '2020-01-01'.
        end_date: End date (inclusive) as ISO string or date object.
            Defaults to '2030-12-31'.

    Returns:
        DataFrame with one row per date and the following columns:
        - date_key: Integer key in YYYYMMDD format (PRIMARY KEY)
        - full_date: The actual date value
        - year: 4-digit year
        - quarter: Quarter number (1-4)
        - month: Month number (1-12)
        - day: Day of month (1-31)
        - day_of_week: ISO weekday (1=Monday, 7=Sunday)
        - day_of_year: Day number in year (1-366)
        - week_of_year: ISO week number
        - day_name: Full day name (e.g., 'Monday')
        - month_name: Full month name (e.g., 'January')
        - quarter_name: Quarter label (e.g., 'Q1')
        - year_month: Year-month string (e.g., '2024-01')
        - year_quarter: Year-quarter string (e.g., '2024-Q1')
        - is_weekend: True for Saturday/Sunday
        - is_month_start: True for first day of month
        - is_month_end: True for last day of month
        - is_quarter_start: True for first day of quarter
        - is_quarter_end: True for last day of quarter
        - is_year_start: True for January 1st
        - is_year_end: True for December 31st
        - is_us_federal_holiday: True for US federal holidays
        - holiday_name: Name of holiday or None

    Example:
        >>> df = generate_dim_date('2024-01-01', '2024-12-31')
        >>> len(df)  # 2024 is a leap year
        366
        >>> df.iloc[0]['date_key']
        20240101
        >>> df[df['is_us_federal_holiday']].shape[0]  # At least 11 holidays
        11
    """
    start = _parse_date(start_date)
    end = _parse_date(end_date)

    if start > end:
        raise ValueError(f"start_date ({start}) must be <= end_date ({end})")

    # Pre-compute all holidays for the date range
    all_holidays: dict[date, str] = {}
    for year in range(start.year, end.year + 1):
        all_holidays.update(_get_us_federal_holidays(year))

    # Generate date range
    dates = []
    current = start
    while current <= end:
        dates.append(current)
        current += timedelta(days=1)

    # Build data rows
    rows = []
    for d in dates:
        # Get next month's first day for month_end calculation
        if d.month == 12:
            next_month_first = date(d.year + 1, 1, 1)
        else:
            next_month_first = date(d.year, d.month + 1, 1)

        is_month_end = d == next_month_first - timedelta(days=1)

        # Quarter calculations
        quarter = (d.month - 1) // 3 + 1
        quarter_start_month = (quarter - 1) * 3 + 1
        quarter_end_month = quarter * 3

        is_quarter_start = d.month == quarter_start_month and d.day == 1

        if quarter_end_month == 12:
            quarter_end_date = date(d.year, 12, 31)
        else:
            quarter_end_date = date(d.year, quarter_end_month + 1, 1) - timedelta(days=1)
        is_quarter_end = d == quarter_end_date

        # Holiday info
        holiday_name = all_holidays.get(d)
        is_holiday = holiday_name is not None

        row = {
            "date_key": int(d.strftime("%Y%m%d")),
            "full_date": d,
            "year": d.year,
            "quarter": quarter,
            "month": d.month,
            "day": d.day,
            "day_of_week": d.isoweekday(),  # 1=Monday, 7=Sunday (ISO)
            "day_of_year": d.timetuple().tm_yday,
            "week_of_year": d.isocalendar()[1],
            "day_name": d.strftime("%A"),
            "month_name": d.strftime("%B"),
            "quarter_name": f"Q{quarter}",
            "year_month": d.strftime("%Y-%m"),
            "year_quarter": f"{d.year}-Q{quarter}",
            "is_weekend": d.weekday() >= 5,
            "is_month_start": d.day == 1,
            "is_month_end": is_month_end,
            "is_quarter_start": is_quarter_start,
            "is_quarter_end": is_quarter_end,
            "is_year_start": d.month == 1 and d.day == 1,
            "is_year_end": d.month == 12 and d.day == 31,
            "is_us_federal_holiday": is_holiday,
            "holiday_name": holiday_name,
        }
        rows.append(row)

    return pd.DataFrame(rows)
