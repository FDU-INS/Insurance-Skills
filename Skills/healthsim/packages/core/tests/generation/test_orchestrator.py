"""Tests for ProfileJourneyOrchestrator."""

import pytest
from datetime import date, timedelta

from healthsim.generation import (
    ProfileJourneyOrchestrator,
    EntityWithTimeline,
    OrchestratorResult,
    orchestrate,
    ProfileSpecification,
    JourneySpecification,
    EventDefinition,
    DelaySpec,
)


class TestProfileJourneyOrchestrator:
    """Tests for ProfileJourneyOrchestrator class."""

    def test_create_orchestrator(self):
        """Test creating orchestrator."""
        orch = ProfileJourneyOrchestrator(seed=42)
        assert orch.seed == 42
        assert orch.journey_engine is not None

    def test_execute_profile_only(self):
        """Test executing with profile but no journey."""
        orch = ProfileJourneyOrchestrator(seed=42)
        result = orch.execute(
            profile=ProfileSpecification(id="test", name="Test"),
            count=10,
        )
        
        assert isinstance(result, OrchestratorResult)
        assert result.entity_count == 10
        assert result.journey_ids == []

    def test_execute_with_journey(self):
        """Test executing with profile and journey."""
        orch = ProfileJourneyOrchestrator(seed=42)
        
        journey = JourneySpecification(
            journey_id="test-journey",
            name="Test Journey",
            events=[
                EventDefinition(
                    event_id="e1",
                    name="Event 1",
                    event_type="milestone",
                    delay=DelaySpec(days=0),
                ),
                EventDefinition(
                    event_id="e2",
                    name="Event 2",
                    event_type="milestone",
                    delay=DelaySpec(days=7),
                    depends_on="e1",
                ),
            ],
        )
        
        result = orch.execute(
            profile=ProfileSpecification(id="test", name="Test"),
            journey=journey,
            count=5,
        )
        
        assert result.entity_count == 5
        assert result.journey_ids == ["test-journey"]
        assert result.event_count == 10  # 2 events per entity

    def test_execute_with_template_journey(self):
        """Test executing with template journey name."""
        orch = ProfileJourneyOrchestrator(seed=42)
        result = orch.execute(
            profile=ProfileSpecification(id="test", name="Test"),
            journey="diabetic-first-year",  # Built-in template
            count=5,
        )
        
        assert result.entity_count == 5
        assert "diabetic-first-year" in result.journey_ids
        assert result.event_count > 0

    def test_reproducibility(self):
        """Test that same seed produces same results."""
        orch1 = ProfileJourneyOrchestrator(seed=42)
        orch2 = ProfileJourneyOrchestrator(seed=42)
        
        journey = JourneySpecification(
            journey_id="test",
            name="Test",
            events=[
                EventDefinition(
                    event_id="e1",
                    name="Event",
                    event_type="milestone",
                    delay=DelaySpec(days=0, days_min=0, days_max=10, distribution="uniform"),
                ),
            ],
        )
        
        result1 = orch1.execute(
            profile=ProfileSpecification(id="test", name="Test"),
            journey=journey,
            count=10,
        )
        result2 = orch2.execute(
            profile=ProfileSpecification(id="test", name="Test"),
            journey=journey,
            count=10,
        )
        
        # Should have same event dates
        for e1, e2 in zip(result1.entities, result2.entities):
            assert len(e1.timeline.events) == len(e2.timeline.events)
            for ev1, ev2 in zip(e1.timeline.events, e2.timeline.events):
                assert ev1.scheduled_date == ev2.scheduled_date

    def test_entity_with_timeline_properties(self):
        """Test EntityWithTimeline properties."""
        orch = ProfileJourneyOrchestrator(seed=42)
        
        journey = JourneySpecification(
            journey_id="test",
            name="Test",
            events=[
                EventDefinition(event_id="e1", name="E1", event_type="milestone"),
                EventDefinition(event_id="e2", name="E2", event_type="milestone"),
            ],
        )
        
        result = orch.execute(
            profile=ProfileSpecification(id="test", name="Test"),
            journey=journey,
            count=1,
        )
        
        entity = result.entities[0]
        assert isinstance(entity, EntityWithTimeline)
        assert entity.pending_events == 2
        assert entity.executed_events == 0

    def test_start_date(self):
        """Test custom start date for journeys."""
        orch = ProfileJourneyOrchestrator(seed=42)
        start = date(2025, 1, 1)
        
        journey = JourneySpecification(
            journey_id="test",
            name="Test",
            events=[
                EventDefinition(event_id="e1", name="E1", event_type="milestone"),
            ],
        )
        
        result = orch.execute(
            profile=ProfileSpecification(id="test", name="Test"),
            journey=journey,
            count=1,
            start_date=start,
        )
        
        assert result.entities[0].timeline.start_date == start

    def test_get_events_by_date(self):
        """Test getting events by date."""
        orch = ProfileJourneyOrchestrator(seed=42)
        start = date(2025, 1, 1)
        
        journey = JourneySpecification(
            journey_id="test",
            name="Test",
            events=[
                EventDefinition(event_id="e1", name="Day0", event_type="milestone", delay=DelaySpec(days=0)),
                EventDefinition(event_id="e2", name="Day7", event_type="milestone", delay=DelaySpec(days=7)),
            ],
        )
        
        result = orch.execute(
            profile=ProfileSpecification(id="test", name="Test"),
            journey=journey,
            count=3,
            start_date=start,
        )
        
        day0_events = result.get_events_by_date(start)
        day7_events = result.get_events_by_date(start + timedelta(days=7))
        
        assert len(day0_events) == 3  # One event per entity on day 0
        assert len(day7_events) == 3  # One event per entity on day 7


class TestOrchestrateFunction:
    """Tests for the orchestrate convenience function."""

    def test_orchestrate_basic(self):
        """Test basic orchestrate call."""
        result = orchestrate(
            profile=ProfileSpecification(id="test", name="Test"),
            count=5,
            seed=42,
        )
        
        assert isinstance(result, OrchestratorResult)
        assert result.entity_count == 5

    def test_orchestrate_with_journey(self):
        """Test orchestrate with journey."""
        result = orchestrate(
            profile=ProfileSpecification(id="test", name="Test"),
            journey="new-member-onboarding",
            count=10,
            seed=42,
        )
        
        assert result.entity_count == 10
        assert result.event_count > 0

    def test_orchestrate_reproducible(self):
        """Test orchestrate reproducibility."""
        result1 = orchestrate(
            profile=ProfileSpecification(id="test", name="Test"),
            journey="new-member-onboarding",
            count=5,
            seed=42,
        )
        result2 = orchestrate(
            profile=ProfileSpecification(id="test", name="Test"),
            journey="new-member-onboarding",
            count=5,
            seed=42,
        )
        
        assert result1.entity_count == result2.entity_count
        assert result1.event_count == result2.event_count


class TestMultipleJourneys:
    """Tests for multiple journey assignment."""

    def test_multiple_journeys(self):
        """Test assigning multiple journeys to entities."""
        orch = ProfileJourneyOrchestrator(seed=42)
        
        journeys = [
            JourneySpecification(
                journey_id="journey1",
                name="Journey 1",
                events=[EventDefinition(event_id="j1e1", name="J1E1", event_type="milestone")],
            ),
            JourneySpecification(
                journey_id="journey2",
                name="Journey 2",
                events=[EventDefinition(event_id="j2e1", name="J2E1", event_type="milestone")],
            ),
        ]
        
        result = orch.execute(
            profile=ProfileSpecification(id="test", name="Test"),
            journey=journeys,
            count=5,
        )
        
        assert set(result.journey_ids) == {"journey1", "journey2"}
        # Each entity should have events from both journeys
        for entity in result.entities:
            assert len(entity.timeline.events) == 2
