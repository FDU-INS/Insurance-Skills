"""Tests for RxMemberSim journey functionality.

These tests verify the journey engine integration with RxMemberSim,
including template execution, timeline generation, and event handling.
"""

from datetime import date, timedelta

import pytest

from rxmembersim.journeys import (
    JourneyEngine,
    JourneySpecification,
    Timeline,
    TimelineEvent,
    EventDefinition,
    DelaySpec,
    RxEventType,
    create_rx_journey_engine,
    get_rx_journey_template,
    RX_JOURNEY_TEMPLATES,
    list_rx_journey_templates,
)
from rxmembersim.journeys.templates import (
    NEW_THERAPY_START,
    CHRONIC_THERAPY_MAINTENANCE,
    SPECIALTY_ONBOARDING,
    STEP_THERAPY,
    ADHERENCE_INTERVENTION,
)


class TestRxJourneyEngine:
    """Tests for RxMemberSim journey engine integration."""

    def test_create_rx_journey_engine(self) -> None:
        """Test creating an RxMemberSim journey engine."""
        engine = create_rx_journey_engine(seed=42)
        assert isinstance(engine, JourneyEngine)

    def test_create_timeline_from_template(self) -> None:
        """Test creating a timeline from a journey template."""
        engine = create_rx_journey_engine(seed=42)
        journey = get_rx_journey_template("new-therapy-start")
        
        # Mock rx_member as dict for testing
        rx_member = {"member_id": "RX001", "name": "Test Member"}
        start_date = date(2025, 1, 1)
        
        timeline = engine.create_timeline(
            entity=rx_member,
            entity_type="rx_member",
            journey=journey,
            start_date=start_date,
        )
        
        assert isinstance(timeline, Timeline)
        assert timeline.entity_id == "RX001"
        assert len(timeline.events) > 0

    def test_new_therapy_start_events(self) -> None:
        """Test new therapy start journey has expected events."""
        engine = create_rx_journey_engine(seed=42)
        rx_member = {"member_id": "RX002"}
        start_date = date(2025, 1, 1)
        
        timeline = engine.create_timeline(
            entity=rx_member,
            entity_type="rx_member",
            journey=NEW_THERAPY_START,
            start_date=start_date,
        )
        
        # Should have prescription and fill events
        event_types = [e.event_type for e in timeline.events]
        assert RxEventType.NEW_RX.value in event_types
        assert RxEventType.FILL.value in event_types

    def test_specialty_onboarding_journey(self) -> None:
        """Test specialty onboarding journey has PA and hub events."""
        engine = create_rx_journey_engine(seed=42)
        rx_member = {"member_id": "RX003"}
        start_date = date(2025, 1, 1)
        
        timeline = engine.create_timeline(
            entity=rx_member,
            entity_type="rx_member",
            journey=SPECIALTY_ONBOARDING,
            start_date=start_date,
        )
        
        # Should have prescription, fill, therapy start, and milestones
        event_types = [e.event_type for e in timeline.events]
        assert RxEventType.NEW_RX.value in event_types
        assert RxEventType.FILL.value in event_types
        assert "milestone" in event_types  # PA, hub enrollment events

    def test_adherence_intervention_journey(self) -> None:
        """Test adherence intervention journey."""
        engine = create_rx_journey_engine(seed=42)
        rx_member = {"member_id": "RX004"}
        start_date = date(2025, 1, 1)
        
        timeline = engine.create_timeline(
            entity=rx_member,
            entity_type="rx_member",
            journey=ADHERENCE_INTERVENTION,
            start_date=start_date,
        )
        
        # Should have adherence gap event
        event_types = [e.event_type for e in timeline.events]
        assert RxEventType.ADHERENCE_GAP.value in event_types


class TestRxJourneyTemplates:
    """Tests for RxMemberSim journey templates."""

    def test_list_templates(self) -> None:
        """Test listing all available templates."""
        templates = list_rx_journey_templates()
        
        assert len(templates) >= 5
        assert "new-therapy-start" in templates
        assert "specialty-onboarding" in templates
        assert "adherence-intervention" in templates

    def test_get_template(self) -> None:
        """Test getting a specific template."""
        journey = get_rx_journey_template("new-therapy-start")
        
        assert isinstance(journey, JourneySpecification)
        assert journey.journey_id == "new-therapy-start"
        assert journey.name == "New Therapy Start"
        assert len(journey.events) > 0

    def test_get_invalid_template_raises(self) -> None:
        """Test that invalid template name raises ValueError."""
        with pytest.raises(ValueError, match="not found"):
            get_rx_journey_template("nonexistent-template")

    def test_template_has_required_fields(self) -> None:
        """Test that all templates have required fields."""
        for template_name in RX_JOURNEY_TEMPLATES:
            journey = get_rx_journey_template(template_name)
            
            assert journey.journey_id
            assert journey.name
            assert len(journey.events) > 0
            assert len(journey.products) > 0


class TestRxTimeline:
    """Tests for RxMemberSim timeline functionality."""

    def test_events_chronologically_ordered(self) -> None:
        """Test that timeline events are sorted chronologically."""
        engine = create_rx_journey_engine(seed=42)
        rx_member = {"member_id": "RX005"}
        start_date = date(2025, 1, 1)
        
        timeline = engine.create_timeline(
            entity=rx_member,
            entity_type="rx_member",
            journey=NEW_THERAPY_START,
            start_date=start_date,
        )
        
        dates = [e.scheduled_date for e in timeline.events]
        assert dates == sorted(dates)

    def test_get_pending_events(self) -> None:
        """Test getting pending events from timeline."""
        engine = create_rx_journey_engine(seed=42)
        rx_member = {"member_id": "RX006"}
        start_date = date(2025, 1, 1)
        
        timeline = engine.create_timeline(
            entity=rx_member,
            entity_type="rx_member",
            journey=NEW_THERAPY_START,
            start_date=start_date,
        )
        
        pending = timeline.get_pending_events()
        assert len(pending) == len(timeline.events)
        assert all(e.status == "pending" for e in pending)

    def test_get_events_up_to_date(self) -> None:
        """Test getting events up to a specific date."""
        engine = create_rx_journey_engine(seed=42)
        rx_member = {"member_id": "RX007"}
        start_date = date(2025, 1, 1)
        
        timeline = engine.create_timeline(
            entity=rx_member,
            entity_type="rx_member",
            journey=CHRONIC_THERAPY_MAINTENANCE,  # Has 90-day events spread out
            start_date=start_date,
        )
        
        # Get events in first 30 days
        target_date = start_date + timedelta(days=30)
        events = timeline.get_events_up_to(target_date)
        
        assert len(events) >= 1
        assert all(e.scheduled_date <= target_date for e in events)


class TestRxEventTypes:
    """Tests for RxMemberSim event types."""

    def test_rx_event_types_defined(self) -> None:
        """Test that RxEventType enum has expected values."""
        assert hasattr(RxEventType, "NEW_RX")
        assert hasattr(RxEventType, "REFILL")
        assert hasattr(RxEventType, "FILL")
        assert hasattr(RxEventType, "REVERSAL")
        assert hasattr(RxEventType, "THERAPY_START")
        assert hasattr(RxEventType, "THERAPY_CHANGE")
        assert hasattr(RxEventType, "THERAPY_DISCONTINUE")
        assert hasattr(RxEventType, "ADHERENCE_GAP")
        assert hasattr(RxEventType, "MPR_THRESHOLD")

    def test_event_type_values_are_strings(self) -> None:
        """Test that event type values are strings."""
        assert RxEventType.NEW_RX.value == "new_rx"
        assert RxEventType.FILL.value == "fill"
        assert RxEventType.ADHERENCE_GAP.value == "adherence_gap"


class TestDelaySpec:
    """Tests for delay specifications in journeys."""

    def test_fixed_delay(self) -> None:
        """Test fixed delay calculation."""
        delay = DelaySpec(days=7)
        td = delay.to_timedelta()
        assert td.days == 7

    def test_uniform_delay_range(self) -> None:
        """Test uniform distribution delay."""
        delay = DelaySpec(
            days=5,
            days_min=3,
            days_max=7,
            distribution="uniform",
        )
        
        # Sample multiple times to verify range
        for seed in range(10):
            td = delay.to_timedelta(seed=seed)
            assert 3 <= td.days <= 7

    def test_zero_delay(self) -> None:
        """Test zero delay for immediate events."""
        delay = DelaySpec(days=0)
        td = delay.to_timedelta()
        assert td.days == 0


class TestBackwardCompatibility:
    """Tests for backward compatibility with old scenario terminology."""

    def test_rx_scenario_engine_alias(self) -> None:
        """Test that RxScenarioEngine alias works."""
        from rxmembersim.journeys.compat import RxScenarioEngine
        
        # Should issue deprecation warning but still work
        import warnings
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            engine = RxScenarioEngine(seed=42)
            
            # Should have triggered deprecation warning
            assert any("deprecated" in str(warning.message).lower() for warning in w)

    def test_legacy_builtin_scenarios_alias(self) -> None:
        """Test that BUILTIN_SCENARIOS alias maps to journey templates."""
        from rxmembersim import BUILTIN_SCENARIOS
        
        assert BUILTIN_SCENARIOS is RX_JOURNEY_TEMPLATES
        assert "new-therapy-start" in BUILTIN_SCENARIOS
