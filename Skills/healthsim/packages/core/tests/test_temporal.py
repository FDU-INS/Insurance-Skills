"""Tests for healthsim.temporal module."""

import random
from datetime import date, datetime, timedelta

import pytest

from healthsim.temporal import (
    EventDelay,
    EventStatus,
    Period,
    PeriodCollection,
    Timeline,
    TimelineEvent,
    TimePeriod,
    business_days_between,
    calculate_age,
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


class TestTimePeriod:
    """Tests for TimePeriod."""

    def test_creation(self) -> None:
        """Test creating a time period."""
        period = TimePeriod(
            start=datetime(2024, 1, 1, 10, 0),
            end=datetime(2024, 1, 1, 14, 0),
        )

        assert period.start == datetime(2024, 1, 1, 10, 0)
        assert period.end == datetime(2024, 1, 1, 14, 0)

    def test_open_ended_period(self) -> None:
        """Test period without end date."""
        period = TimePeriod(start=datetime(2024, 1, 1, 10, 0))

        assert period.end is None
        assert period.duration is None

    def test_duration(self) -> None:
        """Test duration calculation."""
        period = TimePeriod(
            start=datetime(2024, 1, 1, 10, 0),
            end=datetime(2024, 1, 1, 14, 30),
        )

        assert period.duration == timedelta(hours=4, minutes=30)
        assert period.duration_hours == 4.5

    def test_duration_days(self) -> None:
        """Test duration in days."""
        period = TimePeriod(
            start=datetime(2024, 1, 1),
            end=datetime(2024, 1, 8),
        )

        assert period.duration_days == 7.0

    def test_end_must_be_after_start(self) -> None:
        """Test that end must be after start."""
        with pytest.raises(ValueError, match="end must be after start"):
            TimePeriod(
                start=datetime(2024, 1, 2),
                end=datetime(2024, 1, 1),
            )

    def test_contains(self) -> None:
        """Test contains method."""
        period = TimePeriod(
            start=datetime(2024, 1, 1, 10, 0),
            end=datetime(2024, 1, 1, 14, 0),
        )

        assert period.contains(datetime(2024, 1, 1, 12, 0)) is True
        assert period.contains(datetime(2024, 1, 1, 8, 0)) is False
        assert period.contains(datetime(2024, 1, 1, 16, 0)) is False

    def test_contains_open_ended(self) -> None:
        """Test contains for open-ended period."""
        period = TimePeriod(start=datetime(2024, 1, 1, 10, 0))

        assert period.contains(datetime(2024, 1, 1, 12, 0)) is True
        assert period.contains(datetime(2024, 12, 31, 23, 59)) is True
        assert period.contains(datetime(2024, 1, 1, 8, 0)) is False

    def test_overlaps(self) -> None:
        """Test overlaps method."""
        period1 = TimePeriod(
            start=datetime(2024, 1, 1, 10, 0),
            end=datetime(2024, 1, 1, 14, 0),
        )
        period2 = TimePeriod(
            start=datetime(2024, 1, 1, 12, 0),
            end=datetime(2024, 1, 1, 16, 0),
        )
        period3 = TimePeriod(
            start=datetime(2024, 1, 1, 15, 0),
            end=datetime(2024, 1, 1, 17, 0),
        )

        assert period1.overlaps(period2) is True
        assert period1.overlaps(period3) is False

    def test_merge(self) -> None:
        """Test merging overlapping periods."""
        period1 = TimePeriod(
            start=datetime(2024, 1, 1, 10, 0),
            end=datetime(2024, 1, 1, 14, 0),
        )
        period2 = TimePeriod(
            start=datetime(2024, 1, 1, 12, 0),
            end=datetime(2024, 1, 1, 16, 0),
        )

        merged = period1.merge(period2)

        assert merged.start == datetime(2024, 1, 1, 10, 0)
        assert merged.end == datetime(2024, 1, 1, 16, 0)

    def test_merge_non_overlapping_raises(self) -> None:
        """Test merging non-overlapping periods raises error."""
        period1 = TimePeriod(
            start=datetime(2024, 1, 1, 10, 0),
            end=datetime(2024, 1, 1, 12, 0),
        )
        period2 = TimePeriod(
            start=datetime(2024, 1, 1, 14, 0),
            end=datetime(2024, 1, 1, 16, 0),
        )

        with pytest.raises(ValueError, match="non-overlapping"):
            period1.merge(period2)


class TestTimelineEvent:
    """Tests for TimelineEvent."""

    def test_creation(self) -> None:
        """Test creating an event."""
        event = TimelineEvent(
            event_id="evt-001",
            event_type="registration",
            timestamp=datetime(2024, 1, 15, 9, 30),
            metadata={"source": "web"},
        )

        assert event.event_id == "evt-001"
        assert event.event_type == "registration"
        assert event.metadata == {"source": "web"}

    def test_comparison(self) -> None:
        """Test event comparison by timestamp."""
        event1 = TimelineEvent(
            event_id="1",
            event_type="a",
            timestamp=datetime(2024, 1, 1),
        )
        event2 = TimelineEvent(
            event_id="2",
            event_type="b",
            timestamp=datetime(2024, 1, 2),
        )

        assert event1 < event2


class TestTimeline:
    """Tests for Timeline."""

    def test_creation(self) -> None:
        """Test creating a timeline."""
        timeline = Timeline(entity_id="person-123")

        assert timeline.entity_id == "person-123"
        assert len(timeline) == 0

    def test_add_event(self) -> None:
        """Test adding events."""
        timeline = Timeline(entity_id="person-123")
        event = TimelineEvent(
            event_id="evt-001",
            event_type="created",
            timestamp=datetime(2024, 1, 1),
        )

        timeline.add_event(event)

        assert len(timeline) == 1
        assert timeline.get_first_event() == event

    def test_events_sorted(self) -> None:
        """Test events are kept in chronological order."""
        timeline = Timeline(entity_id="test")

        timeline.add_event(
            TimelineEvent(
                event_id="2",
                event_type="b",
                timestamp=datetime(2024, 1, 15),
            )
        )
        timeline.add_event(
            TimelineEvent(
                event_id="1",
                event_type="a",
                timestamp=datetime(2024, 1, 1),
            )
        )
        timeline.add_event(
            TimelineEvent(
                event_id="3",
                event_type="c",
                timestamp=datetime(2024, 1, 10),
            )
        )

        events = list(timeline)
        assert events[0].event_id == "1"
        assert events[1].event_id == "3"
        assert events[2].event_id == "2"

    def test_get_events_by_type(self) -> None:
        """Test filtering events by type."""
        timeline = Timeline(entity_id="test")
        timeline.add_event(
            TimelineEvent(
                event_id="1",
                event_type="login",
                timestamp=datetime(2024, 1, 1),
            )
        )
        timeline.add_event(
            TimelineEvent(
                event_id="2",
                event_type="purchase",
                timestamp=datetime(2024, 1, 2),
            )
        )
        timeline.add_event(
            TimelineEvent(
                event_id="3",
                event_type="login",
                timestamp=datetime(2024, 1, 3),
            )
        )

        logins = timeline.get_events_by_type("login")
        assert len(logins) == 2

    def test_get_events_in_range(self) -> None:
        """Test getting events in time range."""
        timeline = Timeline(entity_id="test")
        timeline.add_event(
            TimelineEvent(
                event_id="1",
                event_type="a",
                timestamp=datetime(2024, 1, 1),
            )
        )
        timeline.add_event(
            TimelineEvent(
                event_id="2",
                event_type="b",
                timestamp=datetime(2024, 1, 15),
            )
        )
        timeline.add_event(
            TimelineEvent(
                event_id="3",
                event_type="c",
                timestamp=datetime(2024, 2, 1),
            )
        )

        events = timeline.get_events_in_range(
            start=datetime(2024, 1, 10),
            end=datetime(2024, 1, 20),
        )

        assert len(events) == 1
        assert events[0].event_id == "2"

    def test_remove_event(self) -> None:
        """Test removing an event."""
        timeline = Timeline(entity_id="test")
        timeline.add_event(
            TimelineEvent(
                event_id="1",
                event_type="a",
                timestamp=datetime(2024, 1, 1),
            )
        )

        assert timeline.remove_event("1") is True
        assert len(timeline) == 0
        assert timeline.remove_event("1") is False

    def test_contains(self) -> None:
        """Test contains check."""
        timeline = Timeline(entity_id="test")
        timeline.add_event(
            TimelineEvent(
                event_id="evt-123",
                event_type="test",
                timestamp=datetime(2024, 1, 1),
            )
        )

        assert "evt-123" in timeline
        assert "evt-456" not in timeline


class TestTemporalUtils:
    """Tests for temporal utility functions."""

    def test_calculate_age(self) -> None:
        """Test age calculation."""
        # Test with known dates
        age = calculate_age(date(1990, 6, 15), date(2024, 1, 1))
        assert age == 33

        # Birthday not yet occurred this year
        age = calculate_age(date(1990, 6, 15), date(2024, 6, 1))
        assert age == 33

        # After birthday
        age = calculate_age(date(1990, 6, 15), date(2024, 7, 1))
        assert age == 34

    def test_format_datetime_iso(self) -> None:
        """Test ISO datetime formatting."""
        dt = datetime(2024, 1, 15, 14, 30, 0)
        formatted = format_datetime_iso(dt)
        assert formatted == "2024-01-15T14:30:00"

    def test_format_date_iso(self) -> None:
        """Test ISO date formatting."""
        d = date(2024, 1, 15)
        formatted = format_date_iso(d)
        assert formatted == "2024-01-15"

    def test_parse_datetime(self) -> None:
        """Test datetime parsing."""
        dt = parse_datetime("2024-01-15T14:30:00")
        assert dt.year == 2024
        assert dt.month == 1
        assert dt.day == 15
        assert dt.hour == 14
        assert dt.minute == 30

    def test_parse_date(self) -> None:
        """Test date parsing."""
        d = parse_date("2024-01-15")
        assert d == date(2024, 1, 15)

    def test_random_date_in_range(self) -> None:
        """Test random date generation."""
        start = date(2024, 1, 1)
        end = date(2024, 12, 31)
        rng = random.Random(42)

        d = random_date_in_range(start, end, rng)

        assert start <= d <= end

    def test_random_date_reproducibility(self) -> None:
        """Test reproducibility with same seed."""
        start = date(2024, 1, 1)
        end = date(2024, 12, 31)

        rng1 = random.Random(42)
        rng2 = random.Random(42)

        d1 = random_date_in_range(start, end, rng1)
        d2 = random_date_in_range(start, end, rng2)

        assert d1 == d2

    def test_random_datetime_in_range(self) -> None:
        """Test random datetime generation."""
        start = datetime(2024, 1, 1, 0, 0)
        end = datetime(2024, 1, 1, 23, 59)
        rng = random.Random(42)

        dt = random_datetime_in_range(start, end, rng)

        assert start <= dt <= end

    def test_relative_date_after(self) -> None:
        """Test relative date calculation (after)."""
        base = date(2024, 1, 15)

        result = relative_date(base, days=10, direction="after")
        assert result == date(2024, 1, 25)

        result = relative_date(base, years=1, direction="after")
        assert result == date(2025, 1, 15)

    def test_relative_date_before(self) -> None:
        """Test relative date calculation (before)."""
        base = date(2024, 6, 15)

        result = relative_date(base, days=10, direction="before")
        assert result == date(2024, 6, 5)

        result = relative_date(base, years=1, direction="before")
        assert result == date(2023, 6, 15)

    def test_business_days_between(self) -> None:
        """Test counting business days."""
        # Monday to Friday (5 business days)
        start = date(2024, 1, 1)  # Monday
        end = date(2024, 1, 5)  # Friday
        assert business_days_between(start, end) == 5

        # Span a weekend
        start = date(2024, 1, 1)  # Monday
        end = date(2024, 1, 8)  # Monday
        assert business_days_between(start, end) == 6

    def test_business_days_between_empty(self) -> None:
        """Test business days with end before start."""
        start = date(2024, 1, 10)
        end = date(2024, 1, 5)
        assert business_days_between(start, end) == 0

    def test_next_business_day(self) -> None:
        """Test finding next business day."""
        # From Friday, should be Monday
        friday = date(2024, 1, 5)
        assert next_business_day(friday) == date(2024, 1, 8)

        # From Wednesday, should be Thursday
        wednesday = date(2024, 1, 3)
        assert next_business_day(wednesday) == date(2024, 1, 4)

        # From Saturday, should be Monday
        saturday = date(2024, 1, 6)
        assert next_business_day(saturday) == date(2024, 1, 8)

    def test_is_future_date(self) -> None:
        """Test future date check."""
        reference = date(2024, 6, 15)

        assert is_future_date(date(2024, 6, 20), reference) is True
        assert is_future_date(date(2024, 6, 10), reference) is False
        assert is_future_date(date(2024, 6, 15), reference) is False


class TestEventStatus:
    """Tests for EventStatus enum."""

    def test_values(self) -> None:
        """Test enum values."""
        assert EventStatus.PENDING.value == "pending"
        assert EventStatus.EXECUTED.value == "executed"
        assert EventStatus.SKIPPED.value == "skipped"
        assert EventStatus.FAILED.value == "failed"


class TestEventDelay:
    """Tests for EventDelay."""

    def test_creation(self) -> None:
        """Test creating an event delay."""
        delay = EventDelay(min_days=1, max_days=5)
        assert delay.min_days == 1
        assert delay.max_days == 5

    def test_calculate_fixed(self) -> None:
        """Test calculating fixed delay."""
        delay = EventDelay(min_days=3, max_days=3)
        result = delay.calculate()
        assert result == timedelta(days=3)

    def test_calculate_range(self) -> None:
        """Test calculating delay from range."""
        delay = EventDelay(min_days=1, max_days=10)
        rng = random.Random(42)

        result = delay.calculate(rng)
        assert timedelta(days=1) <= result <= timedelta(days=10)

    def test_calculate_with_hours(self) -> None:
        """Test calculating delay with hours."""
        delay = EventDelay(min_days=0, max_days=0, min_hours=2, max_hours=2)
        result = delay.calculate()
        assert result == timedelta(hours=2)

    def test_calculate_reproducibility(self) -> None:
        """Test delay calculation reproducibility."""
        delay = EventDelay(min_days=1, max_days=30)
        rng1 = random.Random(42)
        rng2 = random.Random(42)

        result1 = delay.calculate(rng1)
        result2 = delay.calculate(rng2)
        assert result1 == result2


class TestTimelineEventEnhanced:
    """Tests for enhanced TimelineEvent features."""

    def test_mark_executed(self) -> None:
        """Test marking event as executed."""
        event = TimelineEvent(event_type="test")
        assert event.status == EventStatus.PENDING

        event.mark_executed(result={"data": "value"})

        assert event.status == EventStatus.EXECUTED
        assert event.result == {"data": "value"}

    def test_mark_failed(self) -> None:
        """Test marking event as failed."""
        event = TimelineEvent(event_type="test")

        event.mark_failed("Connection error")

        assert event.status == EventStatus.FAILED
        assert event.error == "Connection error"

    def test_mark_skipped(self) -> None:
        """Test marking event as skipped."""
        event = TimelineEvent(event_type="test")

        event.mark_skipped("Not applicable")

        assert event.status == EventStatus.SKIPPED
        assert event.error == "Not applicable"

    def test_event_with_scheduled_date(self) -> None:
        """Test event with scheduled date."""
        event = TimelineEvent(
            event_type="appointment",
            scheduled_date=date(2024, 6, 15),
        )

        assert event.scheduled_date == date(2024, 6, 15)
        # timestamp should be auto-set from scheduled_date
        assert event.timestamp is not None

    def test_event_with_delay(self) -> None:
        """Test event with delay configuration."""
        delay = EventDelay(min_days=7, max_days=14)
        event = TimelineEvent(
            event_type="followup",
            delay_from_previous=delay,
        )

        assert event.delay_from_previous.min_days == 7
        assert event.delay_from_previous.max_days == 14


class TestTimelineEnhanced:
    """Tests for enhanced Timeline features."""

    def test_create_event(self) -> None:
        """Test creating event via timeline."""
        timeline = Timeline(start_date=date(2024, 1, 1))

        event = timeline.create_event(
            event_type="registration",
            name="Initial Registration",
            key="value",
        )

        assert event.event_type == "registration"
        assert event.name == "Initial Registration"
        assert event.payload == {"key": "value"}
        assert event in timeline.events

    def test_schedule_events(self) -> None:
        """Test scheduling events with delays."""
        timeline = Timeline(start_date=date(2024, 1, 1))

        timeline.create_event(
            event_type="step1",
            delay=EventDelay(min_days=0, max_days=0),
        )
        timeline.create_event(
            event_type="step2",
            delay=EventDelay(min_days=7, max_days=7),
        )
        timeline.create_event(
            event_type="step3",
            delay=EventDelay(min_days=14, max_days=14),
        )

        timeline.schedule_events()

        # Events should have scheduled dates
        events = timeline.events
        assert events[0].scheduled_date == date(2024, 1, 1)
        assert events[1].scheduled_date == date(2024, 1, 8)
        assert events[2].scheduled_date == date(2024, 1, 22)

    def test_get_pending_events(self) -> None:
        """Test getting pending events."""
        timeline = Timeline(start_date=date(2024, 1, 1))
        event1 = timeline.create_event(event_type="a")
        event2 = timeline.create_event(event_type="b")

        event1.scheduled_date = date(2024, 1, 5)
        event2.scheduled_date = date(2024, 1, 15)

        event1.mark_executed()

        pending = list(timeline.get_pending_events(up_to_date=date(2024, 1, 20)))
        assert len(pending) == 1
        assert pending[0] == event2

    def test_get_events_by_status(self) -> None:
        """Test filtering events by status."""
        timeline = Timeline()
        e1 = timeline.create_event(event_type="a")
        e2 = timeline.create_event(event_type="b")
        e3 = timeline.create_event(event_type="c")

        e1.mark_executed()
        e2.mark_failed("error")

        executed = timeline.get_events_by_status(EventStatus.EXECUTED)
        assert len(executed) == 1
        assert executed[0] == e1

        pending = timeline.get_events_by_status(EventStatus.PENDING)
        assert len(pending) == 1
        assert pending[0] == e3

    def test_is_complete(self) -> None:
        """Test timeline completion check."""
        timeline = Timeline()
        e1 = timeline.create_event(event_type="a")
        e2 = timeline.create_event(event_type="b")

        assert timeline.is_complete is False

        e1.mark_executed()
        e2.mark_skipped()

        assert timeline.is_complete is True

    def test_clear(self) -> None:
        """Test clearing timeline."""
        timeline = Timeline()
        timeline.create_event(event_type="a")
        timeline.create_event(event_type="b")

        assert len(timeline) == 2

        timeline.clear()

        assert len(timeline) == 0


class TestPeriod:
    """Tests for Period dataclass."""

    def test_creation(self) -> None:
        """Test creating a period."""
        period = Period(
            start_date=date(2024, 1, 1),
            end_date=date(2024, 12, 31),
            label="Year 2024",
        )

        assert period.start_date == date(2024, 1, 1)
        assert period.end_date == date(2024, 12, 31)
        assert period.label == "Year 2024"

    def test_open_ended_period(self) -> None:
        """Test open-ended period."""
        period = Period(start_date=date(2024, 1, 1))

        assert period.is_open is True
        assert period.duration_days is None

    def test_duration_days(self) -> None:
        """Test duration calculation."""
        period = Period(
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 10),
        )

        # Inclusive: Jan 1-10 = 10 days
        assert period.duration_days == 10

    def test_contains(self) -> None:
        """Test date containment check."""
        period = Period(
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31),
        )

        assert period.contains(date(2024, 1, 15)) is True
        assert period.contains(date(2024, 2, 1)) is False
        assert period.contains(date(2023, 12, 31)) is False

    def test_contains_open_ended(self) -> None:
        """Test containment for open-ended period."""
        period = Period(start_date=date(2024, 1, 1))

        assert period.contains(date(2024, 6, 15)) is True
        assert period.contains(date(2030, 1, 1)) is True
        assert period.contains(date(2023, 12, 31)) is False

    def test_overlaps(self) -> None:
        """Test period overlap detection."""
        period1 = Period(
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31),
        )
        period2 = Period(
            start_date=date(2024, 1, 15),
            end_date=date(2024, 2, 15),
        )
        period3 = Period(
            start_date=date(2024, 3, 1),
            end_date=date(2024, 3, 31),
        )

        assert period1.overlaps(period2) is True
        assert period1.overlaps(period3) is False

    def test_adjacent_to(self) -> None:
        """Test adjacent period detection."""
        period1 = Period(
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31),
        )
        period2 = Period(
            start_date=date(2024, 2, 1),
            end_date=date(2024, 2, 29),
        )
        period3 = Period(
            start_date=date(2024, 3, 1),
            end_date=date(2024, 3, 31),
        )

        assert period1.adjacent_to(period2) is True
        assert period1.adjacent_to(period3) is False

    def test_merge_with(self) -> None:
        """Test merging periods."""
        period1 = Period(
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31),
        )
        period2 = Period(
            start_date=date(2024, 1, 15),
            end_date=date(2024, 2, 15),
        )

        merged = period1.merge_with(period2)

        assert merged.start_date == date(2024, 1, 1)
        assert merged.end_date == date(2024, 2, 15)

    def test_iter_dates(self) -> None:
        """Test iterating through dates."""
        period = Period(
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 5),
        )

        dates = list(period.iter_dates())

        assert len(dates) == 5
        assert dates[0] == date(2024, 1, 1)
        assert dates[-1] == date(2024, 1, 5)

    def test_iter_dates_open_ended_raises(self) -> None:
        """Test that iterating open-ended period raises."""
        period = Period(start_date=date(2024, 1, 1))

        with pytest.raises(ValueError, match="open-ended"):
            list(period.iter_dates())


class TestPeriodCollection:
    """Tests for PeriodCollection."""

    def test_add(self) -> None:
        """Test adding periods."""
        collection = PeriodCollection()

        collection.add(Period(start_date=date(2024, 3, 1), end_date=date(2024, 3, 31)))
        collection.add(Period(start_date=date(2024, 1, 1), end_date=date(2024, 1, 31)))

        # Should be sorted by start_date
        assert collection.periods[0].start_date == date(2024, 1, 1)
        assert collection.periods[1].start_date == date(2024, 3, 1)

    def test_find_gaps(self) -> None:
        """Test finding gaps between periods."""
        collection = PeriodCollection()
        collection.add(Period(start_date=date(2024, 1, 1), end_date=date(2024, 1, 31)))
        collection.add(Period(start_date=date(2024, 3, 1), end_date=date(2024, 3, 31)))

        gaps = collection.find_gaps()

        assert len(gaps) == 1
        assert gaps[0].start_date == date(2024, 2, 1)
        assert gaps[0].end_date == date(2024, 2, 29)

    def test_find_gaps_no_gaps(self) -> None:
        """Test find_gaps with no gaps."""
        collection = PeriodCollection()
        collection.add(Period(start_date=date(2024, 1, 1), end_date=date(2024, 1, 31)))
        collection.add(Period(start_date=date(2024, 2, 1), end_date=date(2024, 2, 29)))

        gaps = collection.find_gaps()
        assert len(gaps) == 0

    def test_find_overlaps(self) -> None:
        """Test finding overlapping periods."""
        collection = PeriodCollection()
        p1 = Period(start_date=date(2024, 1, 1), end_date=date(2024, 1, 31))
        p2 = Period(start_date=date(2024, 1, 15), end_date=date(2024, 2, 15))
        collection.add(p1)
        collection.add(p2)

        overlaps = collection.find_overlaps()

        assert len(overlaps) == 1
        assert overlaps[0] == (p1, p2)

    def test_consolidate(self) -> None:
        """Test consolidating overlapping periods."""
        collection = PeriodCollection()
        collection.add(Period(start_date=date(2024, 1, 1), end_date=date(2024, 1, 31)))
        collection.add(Period(start_date=date(2024, 1, 15), end_date=date(2024, 2, 15)))
        collection.add(Period(start_date=date(2024, 3, 1), end_date=date(2024, 3, 31)))

        consolidated = collection.consolidate()

        assert len(consolidated) == 2
        assert consolidated[0].start_date == date(2024, 1, 1)
        assert consolidated[0].end_date == date(2024, 2, 15)
        assert consolidated[1].start_date == date(2024, 3, 1)

    def test_contains_date(self) -> None:
        """Test checking if any period contains a date."""
        collection = PeriodCollection()
        collection.add(Period(start_date=date(2024, 1, 1), end_date=date(2024, 1, 31)))
        collection.add(Period(start_date=date(2024, 3, 1), end_date=date(2024, 3, 31)))

        assert collection.contains_date(date(2024, 1, 15)) is True
        assert collection.contains_date(date(2024, 2, 15)) is False

    def test_get_period_at(self) -> None:
        """Test getting period at a specific date."""
        collection = PeriodCollection()
        p1 = Period(start_date=date(2024, 1, 1), end_date=date(2024, 1, 31))
        collection.add(p1)

        result = collection.get_period_at(date(2024, 1, 15))
        assert result == p1

        result = collection.get_period_at(date(2024, 2, 15))
        assert result is None
