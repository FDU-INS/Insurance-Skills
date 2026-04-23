"""Temporal management for synthetic data generation.

This module provides timeline, period, and date utilities
for managing temporal aspects of synthetic data.
"""

from healthsim.temporal.periods import Period, PeriodCollection, TimePeriod
from healthsim.temporal.timeline import (
    EventDelay,
    EventStatus,
    Timeline,
    TimelineEvent,
)
from healthsim.temporal.utils import (
    business_days_between,
    calculate_age,
    date_range,
    days_between,
    format_date_iso,
    format_datetime_iso,
    is_future_date,
    next_business_day,
    parse_date,
    parse_datetime,
    random_date_in_range,
    random_datetime_in_range,
    relative_date,
)

__all__ = [
    # Timeline
    "Timeline",
    "TimelineEvent",
    "EventStatus",
    "EventDelay",
    # Periods
    "Period",
    "PeriodCollection",
    "TimePeriod",
    # Utilities
    "calculate_age",
    "relative_date",
    "date_range",
    "days_between",
    "business_days_between",
    "next_business_day",
    "is_future_date",
    "format_datetime_iso",
    "format_date_iso",
    "parse_datetime",
    "parse_date",
    "random_date_in_range",
    "random_datetime_in_range",
]
