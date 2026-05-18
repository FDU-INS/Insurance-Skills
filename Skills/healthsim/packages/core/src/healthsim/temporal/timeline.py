"""Timeline and event management for synthetic data generation.

This module provides infrastructure for managing sequences of events
with temporal relationships, delays, and dependencies.
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from enum import Enum
from typing import Any, Generic, TypeVar
from uuid import uuid4


class EventStatus(str, Enum):
    """Status of a timeline event."""

    PENDING = "pending"
    EXECUTED = "executed"
    SKIPPED = "skipped"
    FAILED = "failed"


@dataclass
class EventDelay:
    """Configurable delay between events.

    Supports fixed delays, ranges, and relative timing.
    """

    min_days: int = 0
    max_days: int = 0
    min_hours: int = 0
    max_hours: int = 0

    def calculate(self, rng: Any = None) -> timedelta:
        """Calculate actual delay using optional random generator."""
        import random

        r = rng or random
        if self.max_days > self.min_days:
            days = r.randint(self.min_days, self.max_days)
        else:
            days = self.min_days
        if self.max_hours > self.min_hours:
            hours = r.randint(self.min_hours, self.max_hours)
        else:
            hours = self.min_hours
        return timedelta(days=days, hours=hours)


T = TypeVar("T")


@dataclass
class TimelineEvent(Generic[T]):
    """A single event on a timeline.

    Generic type T represents the event payload/result type.
    """

    event_id: str = field(default_factory=lambda: str(uuid4())[:8])
    event_type: str = ""
    name: str = ""
    scheduled_date: date | datetime | None = None
    status: EventStatus = EventStatus.PENDING

    # Event relationships
    depends_on: str | None = None  # Event ID this depends on
    delay_from_previous: EventDelay = field(default_factory=EventDelay)

    # Execution
    payload: dict[str, Any] = field(default_factory=dict)
    result: T | None = None
    error: str | None = None

    # Metadata
    tags: list[str] = field(default_factory=list)

    # For compatibility with existing code
    timestamp: datetime | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Initialize timestamp from scheduled_date if not set."""
        if self.timestamp is None and self.scheduled_date is not None:
            if isinstance(self.scheduled_date, datetime):
                self.timestamp = self.scheduled_date
            else:
                self.timestamp = datetime.combine(self.scheduled_date, datetime.min.time())

    def mark_executed(self, result: T | None = None) -> None:
        """Mark event as successfully executed."""
        self.status = EventStatus.EXECUTED
        self.result = result

    def mark_failed(self, error: str) -> None:
        """Mark event as failed."""
        self.status = EventStatus.FAILED
        self.error = error

    def mark_skipped(self, reason: str = "") -> None:
        """Mark event as skipped."""
        self.status = EventStatus.SKIPPED
        self.error = reason

    def __lt__(self, other: TimelineEvent[T]) -> bool:
        """Compare events by timestamp/scheduled_date for sorting."""
        self_date = self.timestamp or self.scheduled_date
        other_date = other.timestamp or other.scheduled_date
        if self_date is None or other_date is None:
            return False
        # Convert dates to datetime for comparison
        if isinstance(self_date, date) and not isinstance(self_date, datetime):
            self_date = datetime.combine(self_date, datetime.min.time())
        if isinstance(other_date, date) and not isinstance(other_date, datetime):
            other_date = datetime.combine(other_date, datetime.min.time())
        return self_date < other_date


@dataclass
class Timeline(Generic[T]):
    """Manages a sequence of events with temporal relationships.

    Provides methods to add, schedule, and iterate through events
    while maintaining temporal consistency.
    """

    timeline_id: str = field(default_factory=lambda: str(uuid4())[:8])
    name: str = ""
    start_date: date | datetime = field(default_factory=date.today)
    events: list[TimelineEvent[T]] = field(default_factory=list)

    # For compatibility with existing code
    entity_id: str = ""

    def __post_init__(self) -> None:
        """Initialize entity_id from timeline_id if not set."""
        if not self.entity_id:
            self.entity_id = self.timeline_id

    def add_event(self, event: TimelineEvent[T]) -> TimelineEvent[T]:
        """Add an event to the timeline."""
        self.events.append(event)
        self._sort_events()
        return event

    def _sort_events(self) -> None:
        """Sort events by timestamp/scheduled_date."""

        def get_sort_key(e: TimelineEvent[T]) -> datetime:
            ts = e.timestamp or e.scheduled_date
            if ts is None:
                return datetime.max
            if isinstance(ts, datetime):
                return ts
            return datetime.combine(ts, datetime.min.time())

        self.events.sort(key=get_sort_key)

    def create_event(
        self,
        event_type: str,
        name: str = "",
        delay: EventDelay | None = None,
        depends_on: str | None = None,
        **payload: Any,
    ) -> TimelineEvent[T]:
        """Create and add a new event."""
        event: TimelineEvent[T] = TimelineEvent(
            event_type=event_type,
            name=name or event_type,
            delay_from_previous=delay or EventDelay(),
            depends_on=depends_on,
            payload=payload,
        )
        return self.add_event(event)

    def schedule_events(self, rng: Any = None) -> None:
        """Calculate scheduled dates for all events based on delays and dependencies."""
        import random

        r = rng or random

        scheduled: dict[str, date | datetime] = {}

        for event in self.events:
            if event.depends_on and event.depends_on in scheduled:
                base_date = scheduled[event.depends_on]
            elif scheduled:
                # Use last scheduled event
                base_date = list(scheduled.values())[-1]
            else:
                base_date = self.start_date

            delay = event.delay_from_previous.calculate(r)
            if isinstance(base_date, datetime):
                event.scheduled_date = base_date + delay
                event.timestamp = event.scheduled_date
            else:
                event.scheduled_date = base_date + timedelta(days=delay.days)
                event.timestamp = datetime.combine(event.scheduled_date, datetime.min.time())

            scheduled[event.event_id] = event.scheduled_date

    def get_pending_events(
        self, up_to_date: date | datetime | None = None
    ) -> Iterator[TimelineEvent[T]]:
        """Get pending events up to a given date."""
        cutoff = up_to_date or date.today()
        for event in self.events:
            if event.status == EventStatus.PENDING:
                event_date = event.scheduled_date or event.timestamp
                if event_date is None:
                    yield event
                elif isinstance(event_date, datetime) and isinstance(cutoff, datetime):
                    if event_date <= cutoff:
                        yield event
                elif isinstance(event_date, date) and isinstance(cutoff, date):
                    if event_date <= cutoff:
                        yield event
                else:
                    # Mixed types - convert to date for comparison
                    event_d = event_date.date() if isinstance(event_date, datetime) else event_date
                    cutoff_d = cutoff.date() if isinstance(cutoff, datetime) else cutoff
                    if event_d <= cutoff_d:
                        yield event

    def get_events_by_type(self, event_type: str) -> list[TimelineEvent[T]]:
        """Get all events of a specific type."""
        return [e for e in self.events if e.event_type == event_type]

    def get_events_by_status(self, status: EventStatus) -> list[TimelineEvent[T]]:
        """Get all events with a specific status."""
        return [e for e in self.events if e.status == status]

    def get_event(self, event_id: str) -> TimelineEvent[T] | None:
        """Get an event by ID."""
        for event in self.events:
            if event.event_id == event_id:
                return event
        return None

    def get_event_by_id(self, event_id: str) -> TimelineEvent[T] | None:
        """Get an event by its ID (alias for get_event)."""
        return self.get_event(event_id)

    def get_events_in_range(
        self,
        start: datetime,
        end: datetime,
    ) -> list[TimelineEvent[T]]:
        """Get all events within a time range."""
        result = []
        for e in self.events:
            ts = e.timestamp or (
                datetime.combine(e.scheduled_date, datetime.min.time())
                if e.scheduled_date
                else None
            )
            if ts and start <= ts <= end:
                result.append(e)
        return result

    def get_first_event(self) -> TimelineEvent[T] | None:
        """Get the earliest event."""
        return self.events[0] if self.events else None

    def get_last_event(self) -> TimelineEvent[T] | None:
        """Get the most recent event."""
        return self.events[-1] if self.events else None

    def remove_event(self, event_id: str) -> bool:
        """Remove an event by ID."""
        for i, event in enumerate(self.events):
            if event.event_id == event_id:
                del self.events[i]
                return True
        return False

    def clear(self) -> None:
        """Remove all events from the timeline."""
        self.events.clear()

    @property
    def is_complete(self) -> bool:
        """Check if all events are executed or skipped."""
        return all(e.status in (EventStatus.EXECUTED, EventStatus.SKIPPED) for e in self.events)

    def __len__(self) -> int:
        return len(self.events)

    def __iter__(self) -> Iterator[TimelineEvent[T]]:
        return iter(self.events)

    def __contains__(self, event_id: str) -> bool:
        """Check if an event ID exists in the timeline."""
        return any(e.event_id == event_id for e in self.events)
