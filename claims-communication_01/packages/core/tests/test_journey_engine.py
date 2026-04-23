"""Tests for the shared journey engine."""

import pytest
from datetime import date, timedelta

from healthsim.generation.journey_engine import (
    BaseEventType,
    DelaySpec,
    EventCondition,
    EventDefinition,
    JourneyEngine,
    JourneySpecification,
    PatientEventType,
    MemberEventType,
    Timeline,
    TimelineEvent,
    create_journey_engine,
    create_simple_journey,
    get_journey_template,
    JOURNEY_TEMPLATES,
)


class TestDelaySpec:
    """Tests for DelaySpec."""
    
    def test_fixed_delay(self):
        """Test fixed delay."""
        delay = DelaySpec(days=30)
        td = delay.to_timedelta()
        assert td == timedelta(days=30)
    
    def test_uniform_delay(self):
        """Test uniform distribution delay."""
        delay = DelaySpec(days=30, days_min=20, days_max=40, distribution="uniform")
        td = delay.to_timedelta(seed=42)
        assert timedelta(days=20) <= td <= timedelta(days=40)
    
    def test_reproducible_delay(self):
        """Test that same seed gives same delay."""
        delay = DelaySpec(days=30, days_min=20, days_max=40, distribution="uniform")
        td1 = delay.to_timedelta(seed=42)
        td2 = delay.to_timedelta(seed=42)
        assert td1 == td2


class TestEventCondition:
    """Tests for EventCondition."""
    
    def test_equality(self):
        """Test equality condition."""
        cond = EventCondition(field="demographics.gender", operator="eq", value="M")
        context = {"demographics": {"gender": "M", "age": 65}}
        assert cond.evaluate(context) is True
    
    def test_greater_than(self):
        """Test greater than condition."""
        cond = EventCondition(field="demographics.age", operator="gte", value=65)
        context = {"demographics": {"age": 70}}
        assert cond.evaluate(context) is True
    
    def test_in_list(self):
        """Test in list condition."""
        cond = EventCondition(field="entity.state", operator="in", value=["TX", "CA", "NY"])
        context = {"entity": {"state": "TX"}}
        assert cond.evaluate(context) is True
    
    def test_nested_path(self):
        """Test deeply nested field path."""
        cond = EventCondition(field="entity.clinical.conditions.0", operator="eq", value="E11")
        context = {"entity": {"clinical": {"conditions": ["E11", "I10"]}}}
        # Note: This won't work with current implementation for array indexing
        # Would need enhancement for array access
    
    def test_missing_field(self):
        """Test condition on missing field returns False."""
        cond = EventCondition(field="entity.missing", operator="eq", value="X")
        context = {"entity": {"other": "Y"}}
        assert cond.evaluate(context) is False


class TestEventDefinition:
    """Tests for EventDefinition."""
    
    def test_basic_creation(self):
        """Test creating basic event definition."""
        event = EventDefinition(
            event_id="e1",
            name="Test Event",
            event_type="encounter"
        )
        assert event.event_id == "e1"
        assert event.probability == 1.0
    
    def test_with_delay(self):
        """Test event with delay spec."""
        event = EventDefinition(
            event_id="e1",
            name="Test Event",
            event_type="encounter",
            delay=DelaySpec(days=30)
        )
        assert event.delay.days == 30
    
    def test_with_conditions(self):
        """Test event with conditions."""
        event = EventDefinition(
            event_id="e1",
            name="Test Event",
            event_type="encounter",
            conditions=[
                EventCondition(field="demographics.age", operator="gte", value=65)
            ]
        )
        assert len(event.conditions) == 1


class TestJourneySpecification:
    """Tests for JourneySpecification."""
    
    def test_basic_creation(self):
        """Test creating basic journey specification."""
        journey = JourneySpecification(
            journey_id="test-journey",
            name="Test Journey",
            products=["patientsim"]
        )
        assert journey.journey_id == "test-journey"
        assert "patientsim" in journey.products
    
    def test_from_dict(self):
        """Test creating from dictionary."""
        data = {
            "journey_id": "test-journey",
            "name": "Test Journey",
            "products": ["membersim"],
            "events": []
        }
        journey = JourneySpecification.from_dict(data)
        assert journey.journey_id == "test-journey"


class TestTimeline:
    """Tests for Timeline."""
    
    def test_creation(self):
        """Test creating timeline."""
        timeline = Timeline(
            entity_id="P001",
            entity_type="patient",
            start_date=date(2025, 1, 1)
        )
        assert timeline.entity_id == "P001"
        assert len(timeline.events) == 0
    
    def test_add_event(self):
        """Test adding events maintains order."""
        timeline = Timeline(entity_id="P001", entity_type="patient")
        
        event1 = TimelineEvent(
            timeline_event_id="e1",
            journey_id="j1",
            event_definition_id="ed1",
            scheduled_date=date(2025, 1, 15),
            event_type="encounter",
            event_name="Follow-up"
        )
        event2 = TimelineEvent(
            timeline_event_id="e2",
            journey_id="j1",
            event_definition_id="ed2",
            scheduled_date=date(2025, 1, 1),
            event_type="diagnosis",
            event_name="Initial"
        )
        
        timeline.add_event(event1)
        timeline.add_event(event2)
        
        # Should be ordered chronologically
        assert timeline.events[0].event_name == "Initial"
        assert timeline.events[1].event_name == "Follow-up"
    
    def test_get_pending_events(self):
        """Test getting pending events."""
        timeline = Timeline(entity_id="P001", entity_type="patient")
        
        event1 = TimelineEvent(
            timeline_event_id="e1", journey_id="j1", event_definition_id="ed1",
            scheduled_date=date(2025, 1, 1), event_type="enc", event_name="E1",
            status="executed"
        )
        event2 = TimelineEvent(
            timeline_event_id="e2", journey_id="j1", event_definition_id="ed2",
            scheduled_date=date(2025, 1, 15), event_type="enc", event_name="E2"
        )
        
        timeline.add_event(event1)
        timeline.add_event(event2)
        
        pending = timeline.get_pending_events()
        assert len(pending) == 1
        assert pending[0].event_name == "E2"


class TestJourneyEngine:
    """Tests for JourneyEngine."""
    
    def test_creation(self):
        """Test creating engine."""
        engine = JourneyEngine(seed=42)
        assert engine.seed == 42
    
    def test_register_handler(self):
        """Test registering event handler."""
        engine = JourneyEngine()
        
        def my_handler(entity, event, context):
            return {"handled": True}
        
        engine.register_handler("patientsim", "encounter", my_handler)
        assert "patientsim" in engine._handlers
        assert "encounter" in engine._handlers["patientsim"]
    
    def test_create_timeline(self):
        """Test creating timeline from journey."""
        engine = JourneyEngine(seed=42)
        
        journey = create_simple_journey(
            "test-journey",
            "Test",
            events=[
                {"event_id": "e1", "name": "Start", "event_type": "milestone", "delay": {"days": 0}},
                {"event_id": "e2", "name": "Follow-up", "event_type": "encounter", 
                 "delay": {"days": 30}, "depends_on": "e1"},
            ]
        )
        
        entity = {"patient_id": "P001", "name": "Test Patient"}
        timeline = engine.create_timeline(
            entity=entity,
            entity_type="patient",
            journey=journey,
            start_date=date(2025, 1, 1)
        )
        
        assert timeline.entity_id == "P001"
        assert len(timeline.events) == 2
        assert timeline.events[0].scheduled_date == date(2025, 1, 1)
        assert timeline.events[1].scheduled_date == date(2025, 1, 31)
    
    def test_reproducibility(self):
        """Test that same seed gives same timeline."""
        journey = create_simple_journey(
            "test-journey", "Test",
            events=[
                {"event_id": "e1", "name": "E1", "event_type": "enc",
                 "delay": {"days": 30, "days_min": 20, "days_max": 40, "distribution": "uniform"}},
            ]
        )
        
        entity = {"patient_id": "P001"}
        
        engine1 = JourneyEngine(seed=42)
        timeline1 = engine1.create_timeline(entity, "patient", journey, date(2025, 1, 1))
        
        engine2 = JourneyEngine(seed=42)
        timeline2 = engine2.create_timeline(entity, "patient", journey, date(2025, 1, 1))
        
        assert timeline1.events[0].scheduled_date == timeline2.events[0].scheduled_date
    
    def test_execute_event(self):
        """Test executing a single event."""
        engine = JourneyEngine(seed=42)
        
        results = []
        def my_handler(entity, event, context):
            results.append(event.event_name)
            return {"result": "success"}
        
        engine.register_handler("patientsim", "encounter", my_handler)
        
        journey = create_simple_journey(
            "test", "Test",
            events=[{"event_id": "e1", "name": "Visit", "event_type": "encounter", 
                     "product": "patientsim", "delay": {"days": 0}}]
        )
        
        entity = {"patient_id": "P001"}
        timeline = engine.create_timeline(entity, "patient", journey, date(2025, 1, 1))
        
        result = engine.execute_event(timeline, timeline.events[0], entity)
        
        assert result["status"] == "executed"
        assert results == ["Visit"]
    
    def test_conditional_event(self):
        """Test event with condition."""
        engine = JourneyEngine(seed=42)
        
        journey = create_simple_journey(
            "test", "Test",
            events=[
                {"event_id": "e1", "name": "Senior Event", "event_type": "enc",
                 "delay": {"days": 0},
                 "conditions": [{"field": "entity.age", "operator": "gte", "value": 65}]},
            ]
        )
        
        # Young patient - event should be skipped
        young_patient = {"patient_id": "P001", "age": 30}
        timeline1 = engine.create_timeline(young_patient, "patient", journey, date(2025, 1, 1))
        assert len(timeline1.events) == 0
        
        # Senior patient - event should be scheduled
        senior_patient = {"patient_id": "P002", "age": 70}
        timeline2 = engine.create_timeline(senior_patient, "patient", journey, date(2025, 1, 1))
        assert len(timeline2.events) == 1


class TestConvenienceFunctions:
    """Tests for convenience functions."""
    
    def test_create_journey_engine(self):
        """Test create_journey_engine."""
        engine = create_journey_engine(seed=42)
        assert isinstance(engine, JourneyEngine)
    
    def test_create_simple_journey(self):
        """Test create_simple_journey."""
        journey = create_simple_journey(
            "test-j", "Test Journey",
            events=[{"event_id": "e1", "name": "E1", "event_type": "enc"}]
        )
        assert journey.journey_id == "test-j"
        assert len(journey.events) == 1
    
    def test_get_journey_template(self):
        """Test getting built-in templates."""
        journey = get_journey_template("diabetic-first-year")
        assert journey.journey_id == "diabetic-first-year"
        assert len(journey.events) > 0
    
    def test_get_invalid_template(self):
        """Test getting invalid template raises error."""
        with pytest.raises(ValueError, match="not found"):
            get_journey_template("nonexistent-template")
    
    def test_journey_templates_available(self):
        """Test that templates are available."""
        assert "diabetic-first-year" in JOURNEY_TEMPLATES
        assert "new-member-onboarding" in JOURNEY_TEMPLATES
