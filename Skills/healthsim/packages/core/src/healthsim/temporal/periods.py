"""Date period and range management.

Provides classes for managing date ranges, coverage spans,
and temporal boundaries.
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta

from pydantic import BaseModel, field_validator, model_validator


@dataclass
class Period:
    """A date range with start and end dates.

    End date is inclusive. If end_date is None, the period is open-ended.
    """

    start_date: date
    end_date: date | None = None
    label: str = ""

    @property
    def is_open(self) -> bool:
        """Check if period is open-ended (no end date)."""
        return self.end_date is None

    @property
    def duration_days(self) -> int | None:
        """Get duration in days, or None if open-ended."""
        if self.end_date is None:
            return None
        return (self.end_date - self.start_date).days + 1

    def contains(self, check_date: date) -> bool:
        """Check if a date falls within this period."""
        if check_date < self.start_date:
            return False
        if self.end_date is not None and check_date > self.end_date:
            return False
        return True

    def overlaps(self, other: Period) -> bool:
        """Check if this period overlaps with another."""
        # If either is open-ended, check start dates
        if self.end_date is None:
            return other.end_date is None or other.end_date >= self.start_date
        if other.end_date is None:
            return self.end_date >= other.start_date

        # Both have end dates
        return not (self.end_date < other.start_date or other.end_date < self.start_date)

    def adjacent_to(self, other: Period) -> bool:
        """Check if this period is immediately adjacent to another."""
        if self.end_date is None or other.end_date is None:
            return False
        return (
            self.end_date + timedelta(days=1) == other.start_date
            or other.end_date + timedelta(days=1) == self.start_date
        )

    def merge_with(self, other: Period) -> Period:
        """Merge with an overlapping or adjacent period."""
        new_start = min(self.start_date, other.start_date)
        if self.end_date is None or other.end_date is None:
            new_end = None
        else:
            new_end = max(self.end_date, other.end_date)
        return Period(start_date=new_start, end_date=new_end)

    def iter_dates(self) -> Iterator[date]:
        """Iterate through all dates in the period."""
        if self.end_date is None:
            raise ValueError("Cannot iterate over open-ended period")
        current = self.start_date
        while current <= self.end_date:
            yield current
            current += timedelta(days=1)


@dataclass
class PeriodCollection:
    """A collection of periods with gap and overlap detection."""

    periods: list[Period] = field(default_factory=list)

    def add(self, period: Period) -> None:
        """Add a period to the collection."""
        self.periods.append(period)
        self.periods.sort(key=lambda p: p.start_date)

    def find_gaps(self) -> list[Period]:
        """Find gaps between periods."""
        if len(self.periods) < 2:
            return []

        gaps = []
        for i in range(len(self.periods) - 1):
            current = self.periods[i]
            next_period = self.periods[i + 1]

            if current.end_date is None:
                continue

            gap_start = current.end_date + timedelta(days=1)
            gap_end = next_period.start_date - timedelta(days=1)

            if gap_start <= gap_end:
                gaps.append(Period(start_date=gap_start, end_date=gap_end, label="gap"))

        return gaps

    def find_overlaps(self) -> list[tuple[Period, Period]]:
        """Find overlapping period pairs."""
        overlaps = []
        for i, p1 in enumerate(self.periods):
            for p2 in self.periods[i + 1 :]:
                if p1.overlaps(p2):
                    overlaps.append((p1, p2))
        return overlaps

    def consolidate(self) -> list[Period]:
        """Merge overlapping and adjacent periods."""
        if not self.periods:
            return []

        sorted_periods = sorted(self.periods, key=lambda p: p.start_date)
        result = [sorted_periods[0]]

        for period in sorted_periods[1:]:
            last = result[-1]
            if last.overlaps(period) or last.adjacent_to(period):
                result[-1] = last.merge_with(period)
            else:
                result.append(period)

        return result

    def contains_date(self, check_date: date) -> bool:
        """Check if any period contains the given date."""
        return any(p.contains(check_date) for p in self.periods)

    def get_period_at(self, check_date: date) -> Period | None:
        """Get the period containing the given date, if any."""
        for period in self.periods:
            if period.contains(check_date):
                return period
        return None


class TimePeriod(BaseModel):
    """A period of time with start and optional end.

    Represents a time span that can be open-ended (no end) or bounded.
    Uses datetime for more precise temporal boundaries.

    Attributes:
        start: Start datetime of the period
        end: End datetime of the period (None for ongoing)

    Example:
        >>> period = TimePeriod(
        ...     start=datetime(2024, 1, 1, 10, 0),
        ...     end=datetime(2024, 1, 1, 14, 30)
        ... )
        >>> period.duration_hours
        4.5
        >>> period.is_active
        False
    """

    start: datetime
    end: datetime | None = None

    @field_validator("start", "end", mode="before")
    @classmethod
    def parse_datetime(cls, v: str | datetime | None) -> datetime | None:
        """Parse datetime from string if needed."""
        if v is None:
            return None
        if isinstance(v, str):
            return datetime.fromisoformat(v)
        return v

    @model_validator(mode="after")
    def validate_end_after_start(self) -> TimePeriod:
        """Ensure end is after start if both are provided."""
        if self.end is not None and self.end < self.start:
            raise ValueError("end must be after start")
        return self

    @property
    def duration(self) -> timedelta | None:
        """Get the duration of the period.

        Returns:
            Duration as timedelta, or None if period is open-ended
        """
        if self.end is None:
            return None
        return self.end - self.start

    @property
    def duration_hours(self) -> float | None:
        """Get the duration in hours.

        Returns:
            Duration in hours, or None if period is open-ended
        """
        duration = self.duration
        if duration is None:
            return None
        return duration.total_seconds() / 3600

    @property
    def duration_days(self) -> float | None:
        """Get the duration in days.

        Returns:
            Duration in days, or None if period is open-ended
        """
        duration = self.duration
        if duration is None:
            return None
        return duration.total_seconds() / 86400

    @property
    def is_active(self) -> bool:
        """Check if the period is currently active (ongoing or contains now).

        Returns:
            True if period has no end or contains current time
        """
        now = datetime.now()
        if self.end is None:
            return self.start <= now
        return self.start <= now <= self.end

    def contains(self, dt: datetime) -> bool:
        """Check if a datetime falls within this period.

        Args:
            dt: Datetime to check

        Returns:
            True if dt is within the period
        """
        if self.end is None:
            return dt >= self.start
        return self.start <= dt <= self.end

    def overlaps(self, other: TimePeriod) -> bool:
        """Check if this period overlaps with another.

        Args:
            other: Another TimePeriod to check

        Returns:
            True if the periods overlap
        """
        # If either is open-ended, use a far-future date
        self_end = self.end or datetime.max
        other_end = other.end or datetime.max

        return self.start < other_end and other.start < self_end

    def merge(self, other: TimePeriod) -> TimePeriod:
        """Merge this period with another overlapping period.

        Args:
            other: Another TimePeriod to merge

        Returns:
            New TimePeriod spanning both periods

        Raises:
            ValueError: If periods don't overlap
        """
        if not self.overlaps(other):
            raise ValueError("Cannot merge non-overlapping periods")

        new_start = min(self.start, other.start)

        # Handle open-ended periods
        if self.end is None or other.end is None:
            new_end = None
        else:
            new_end = max(self.end, other.end)

        return TimePeriod(start=new_start, end=new_end)
