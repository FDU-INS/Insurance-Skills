"""Tests for journey engine module."""

import pytest
from datetime import date, datetime, timedelta

from healthsim.generation.journey_engine import (
    # Event Types
    BaseEventType,
    PatientEventType,
    MemberEventType,
    RxEventType,
    TrialEventType,
    # Timing
    DelaySpec,
    # Conditions
    EventCondition,
    # Definitions
    EventDefinition,
    TriggerSpec,
    JourneySpecification,
    # Timeline
    TimelineEvent,
    Timeline,
    # Engine
    JourneyEngine,
    # Convenience
    create_journey_engine,
    create_simple_journey,
    get_journey_template,
    JOURNEY_TEMPLATES,
)


# =============================================================================
# Event Type Tests
# =============================================================================

class TestEventTypes:
    """Tests for event type enums."""

    def test_base_event_types(self):
        """Test base event types exist."""
        assert BaseEventType.ENTITY_CREATED.value == "entity_created"
        assert BaseEventType.JOURNEY_START.value == "journey_start"
        assert BaseEventType.TRIGGER_OUTBOUND.value == "trigger_outbound"

    def test_patient_event_types(self):
        """Test patient event types."""
        assert PatientEventType.ADMISSION.value == "admission"
        assert PatientEventType.ENCOUNTER.value == "encounter"
        assert PatientEventType.LAB_RESULT.value == "lab_result"

    def test_member_event_types(self):
        """Test member event types."""
        assert MemberEventType.NEW_ENROLLMENT.value == "new_enrollment"
        assert MemberEventType.CLAIM_PROFESSIONAL.value == "claim_professional"
        assert MemberEventType.GAP_CLOSED.value == "gap_closed"

    def test_rx_event_types(self):
        """Test pharmacy event types."""
        assert RxEventType.NEW_RX.value == "new_rx"
        assert RxEventType.REFILL.value == "refill"
        assert RxEventType.ADHERENCE_GAP.value == "adherence_gap"

    def test_trial_event_types(self):
        """Test trial event types."""
        assert TrialEventType.SCREENING.value == "screening"
        assert TrialEventType.RANDOMIZATION.value == "randomization"
        assert TrialEventType.ADVERSE_EVENT.value == "adverse_event"


# =============================================================================
# DelaySpec Tests
# =============================================================================

class TestDelaySpec:
    """Tests for DelaySpec."""

    def test_fixed_delay(self):
        """Test fixed delay."""
        spec = DelaySpec(days=7)
        
        td = spec.to_timedelta()
        
        assert td == timedelta(days=7)

    def test_uniform_delay(self):
        """Test uniform distribution delay."""
        spec = DelaySpec(
            days=7,
            days_min=5,
            days_max=10,
            distribution="uniform"
        )
        
        # Sample multiple times with same seed
        results = [spec.to_timedelta(seed=42).days for _ in range(10)]
        
        # All should be in range
        assert all(5 <= d <= 10 for d in results)
        # Same seed = same result
        assert len(set(results)) == 1

    def test_uniform_delay_variation(self):
        """Test uniform delay varies with different seeds."""
        spec = DelaySpec(
            days=7,
            days_min=1,
            days_max=30,
            distribution="uniform"
        )
        
        results = [spec.to_timedelta(seed=i).days for i in range(100)]
        
        # Should have variation
        assert len(set(results)) > 1

    def test_normal_delay(self):
        """Test normal distribution delay."""
        spec = DelaySpec(
            days=30,
            days_min=20,
            days_max=40,
            distribution="normal"
        )
        
        results = [spec.to_timedelta(seed=i).days for i in range(100)]
        
        # Mean should be around 30
        mean = sum(results) / len(results)
        assert 25 < mean < 35

    def test_default_values(self):
        """Test default values."""
        spec = DelaySpec()
        
        assert spec.days == 0
        assert spec.distribution == "fixed"


# =============================================================================
# EventCondition Tests
# =============================================================================

class TestEventCondition:
    """Tests for EventCondition."""

    def test_eq_condition(self):
        """Test equality condition."""
        cond = EventCondition(field="gender", operator="eq", value="M")
        
        assert cond.evaluate({"gender": "M"}) is True
        assert cond.evaluate({"gender": "F"}) is False

    def test_ne_condition(self):
        """Test not equal condition."""
        cond = EventCondition(field="gender", operator="ne", value="M")
        
        assert cond.evaluate({"gender": "F"}) is True
        assert cond.evaluate({"gender": "M"}) is False

    def test_gt_condition(self):
        """Test greater than condition."""
        cond = EventCondition(field="age", operator="gt", value=65)
        
        assert cond.evaluate({"age": 70}) is True
        assert cond.evaluate({"age": 65}) is False
        assert cond.evaluate({"age": 60}) is False

    def test_gte_condition(self):
        """Test greater than or equal condition."""
        cond = EventCondition(field="age", operator="gte", value=65)
        
        assert cond.evaluate({"age": 70}) is True
        assert cond.evaluate({"age": 65}) is True
        assert cond.evaluate({"age": 60}) is False

    def test_lt_condition(self):
        """Test less than condition."""
        cond = EventCondition(field="age", operator="lt", value=18)
        
        assert cond.evaluate({"age": 15}) is True
        assert cond.evaluate({"age": 18}) is False

    def test_lte_condition(self):
        """Test less than or equal condition."""
        cond = EventCondition(field="age", operator="lte", value=18)
        
        assert cond.evaluate({"age": 18}) is True
        assert cond.evaluate({"age": 19}) is False

    def test_in_condition(self):
        """Test 'in' condition."""
        cond = EventCondition(field="state", operator="in", value=["TX", "CA", "NY"])
        
        assert cond.evaluate({"state": "TX"}) is True
        assert cond.evaluate({"state": "FL"}) is False

    def test_not_in_condition(self):
        """Test 'not in' condition."""
        cond = EventCondition(field="state", operator="not_in", value=["TX", "CA"])
        
        assert cond.evaluate({"state": "NY"}) is True
        assert cond.evaluate({"state": "TX"}) is False

    def test_contains_condition(self):
        """Test 'contains' condition."""
        cond = EventCondition(field="conditions", operator="contains", value="E11")
        
        assert cond.evaluate({"conditions": ["E11", "I10"]}) is True
        assert cond.evaluate({"conditions": ["I10", "E78"]}) is False

    def test_nested_field(self):
        """Test nested field access."""
        cond = EventCondition(field="demographics.age", operator="gte", value=65)
        
        assert cond.evaluate({"demographics": {"age": 70}}) is True
        assert cond.evaluate({"demographics": {"age": 50}}) is False

    def test_missing_field_returns_false(self):
        """Test missing field returns False."""
        cond = EventCondition(field="nonexistent", operator="eq", value="x")
        
        assert cond.evaluate({}) is False
        assert cond.evaluate({"other": "value"}) is False


# =============================================================================
# EventDefinition Tests
# =============================================================================

class TestEventDefinition:
    """Tests for EventDefinition."""

    def test_basic_creation(self):
        """Test basic event definition."""
        event = EventDefinition(
            event_id="evt1",
            name="Test Event",
            event_type="encounter"
        )
        
        assert event.event_id == "evt1"
        assert event.event_type == "encounter"
        assert event.product == "core"
        assert event.probability == 1.0

    def test_with_delay(self):
        """Test event with delay."""
        event = EventDefinition(
            event_id="evt1",
            name="Delayed Event",
            event_type="encounter",
            delay=DelaySpec(days=7, distribution="fixed")
        )
        
        assert event.delay.days == 7

    def test_with_conditions(self):
        """Test event with conditions."""
        event = EventDefinition(
            event_id="evt1",
            name="Conditional Event",
            event_type="encounter",
            conditions=[
                EventCondition(field="age", operator="gte", value=65)
            ]
        )
        
        assert len(event.conditions) == 1

    def test_with_triggers(self):
        """Test event with triggers."""
        event = EventDefinition(
            event_id="evt1",
            name="Triggering Event",
            event_type="discharge",
            triggers=[
                TriggerSpec(target_product="membersim", event_type="claim_institutional")
            ]
        )
        
        assert len(event.triggers) == 1
        assert event.triggers[0].target_product == "membersim"


# =============================================================================
# JourneySpecification Tests
# =============================================================================

class TestJourneySpecification:
    """Tests for JourneySpecification."""

    def test_basic_creation(self):
        """Test basic journey creation."""
        journey = JourneySpecification(
            journey_id="test-journey",
            name="Test Journey"
        )
        
        assert journey.journey_id == "test-journey"
        assert journey.version == "1.0"
        assert journey.products == ["patientsim"]

    def test_with_events(self):
        """Test journey with events."""
        journey = JourneySpecification(
            journey_id="test-journey",
            name="Test Journey",
            events=[
                EventDefinition(event_id="e1", name="Event 1", event_type="encounter"),
                EventDefinition(event_id="e2", name="Event 2", event_type="lab_order"),
            ]
        )
        
        assert len(journey.events) == 2

    def test_from_dict(self):
        """Test creating from dictionary."""
        data = {
            "journey_id": "from-dict",
            "name": "From Dict Journey",
            "duration_days": 30,
        }
        
        journey = JourneySpecification.from_dict(data)
        
        assert journey.journey_id == "from-dict"
        assert journey.duration_days == 30


# =============================================================================
# TimelineEvent Tests
# =============================================================================

class TestTimelineEvent:
    """Tests for TimelineEvent."""

    def test_basic_creation(self):
        """Test basic timeline event creation."""
        event = TimelineEvent(
            timeline_event_id="te1",
            journey_id="j1",
            event_definition_id="e1",
            scheduled_date=date(2024, 1, 15),
            event_type="encounter",
            event_name="Test Encounter"
        )
        
        assert event.status == "pending"
        assert event.scheduled_date == date(2024, 1, 15)
        assert event.executed_at is None

    def test_with_execution(self):
        """Test event with execution details."""
        event = TimelineEvent(
            timeline_event_id="te1",
            journey_id="j1",
            event_definition_id="e1",
            scheduled_date=date(2024, 1, 15),
            event_type="encounter",
            event_name="Test",
            status="executed",
            executed_at=datetime(2024, 1, 15, 10, 30),
            result={"success": True}
        )
        
        assert event.status == "executed"
        assert event.result["success"] is True


# =============================================================================
# Timeline Tests
# =============================================================================

class TestTimeline:
    """Tests for Timeline."""

    def test_basic_creation(self):
        """Test basic timeline creation."""
        timeline = Timeline(
            entity_id="P001",
            entity_type="patient"
        )
        
        assert timeline.entity_id == "P001"
        assert len(timeline.events) == 0

    def test_add_event(self):
        """Test adding events to timeline."""
        timeline = Timeline(
            entity_id="P001",
            entity_type="patient"
        )
        
        event = TimelineEvent(
            timeline_event_id="te1",
            journey_id="j1",
            event_definition_id="e1",
            scheduled_date=date(2024, 1, 15),
            event_type="encounter",
            event_name="Test"
        )
        
        timeline.add_event(event)
        
        assert len(timeline.events) == 1

    def test_events_sorted_chronologically(self):
        """Test events are sorted by date."""
        timeline = Timeline(entity_id="P001", entity_type="patient")
        
        # Add out of order
        timeline.add_event(TimelineEvent(
            timeline_event_id="te2", journey_id="j1", event_definition_id="e2",
            scheduled_date=date(2024, 3, 1), event_type="encounter", event_name="Late"
        ))
        timeline.add_event(TimelineEvent(
            timeline_event_id="te1", journey_id="j1", event_definition_id="e1",
            scheduled_date=date(2024, 1, 1), event_type="encounter", event_name="Early"
        ))
        
        assert timeline.events[0].scheduled_date < timeline.events[1].scheduled_date

    def test_get_pending_events(self):
        """Test getting pending events."""
        timeline = Timeline(entity_id="P001", entity_type="patient")
        
        timeline.add_event(TimelineEvent(
            timeline_event_id="te1", journey_id="j1", event_definition_id="e1",
            scheduled_date=date(2024, 1, 1), event_type="a", event_name="A",
            status="executed"
        ))
        timeline.add_event(TimelineEvent(
            timeline_event_id="te2", journey_id="j1", event_definition_id="e2",
            scheduled_date=date(2024, 2, 1), event_type="b", event_name="B",
            status="pending"
        ))
        
        pending = timeline.get_pending_events()
        
        assert len(pending) == 1
        assert pending[0].timeline_event_id == "te2"

    def test_get_events_by_date(self):
        """Test getting events by date."""
        timeline = Timeline(entity_id="P001", entity_type="patient")
        
        timeline.add_event(TimelineEvent(
            timeline_event_id="te1", journey_id="j1", event_definition_id="e1",
            scheduled_date=date(2024, 1, 15), event_type="a", event_name="A"
        ))
        timeline.add_event(TimelineEvent(
            timeline_event_id="te2", journey_id="j1", event_definition_id="e2",
            scheduled_date=date(2024, 1, 15), event_type="b", event_name="B"
        ))
        timeline.add_event(TimelineEvent(
            timeline_event_id="te3", journey_id="j1", event_definition_id="e3",
            scheduled_date=date(2024, 1, 16), event_type="c", event_name="C"
        ))
        
        events = timeline.get_events_by_date(date(2024, 1, 15))
        
        assert len(events) == 2

    def test_get_events_up_to(self):
        """Test getting events up to a date."""
        timeline = Timeline(entity_id="P001", entity_type="patient")
        
        timeline.add_event(TimelineEvent(
            timeline_event_id="te1", journey_id="j1", event_definition_id="e1",
            scheduled_date=date(2024, 1, 1), event_type="a", event_name="A"
        ))
        timeline.add_event(TimelineEvent(
            timeline_event_id="te2", journey_id="j1", event_definition_id="e2",
            scheduled_date=date(2024, 2, 1), event_type="b", event_name="B"
        ))
        timeline.add_event(TimelineEvent(
            timeline_event_id="te3", journey_id="j1", event_definition_id="e3",
            scheduled_date=date(2024, 3, 1), event_type="c", event_name="C"
        ))
        
        events = timeline.get_events_up_to(date(2024, 2, 15))
        
        assert len(events) == 2

    def test_mark_executed(self):
        """Test marking event as executed."""
        timeline = Timeline(entity_id="P001", entity_type="patient")
        
        timeline.add_event(TimelineEvent(
            timeline_event_id="te1", journey_id="j1", event_definition_id="e1",
            scheduled_date=date(2024, 1, 1), event_type="a", event_name="A"
        ))
        
        timeline.mark_executed("te1", {"output": "success"})
        
        assert timeline.events[0].status == "executed"
        assert timeline.events[0].result["output"] == "success"
        assert timeline.events[0].executed_at is not None


# =============================================================================
# JourneyEngine Tests
# =============================================================================

class TestJourneyEngine:
    """Tests for JourneyEngine."""

    @pytest.fixture
    def engine(self):
        """Create engine fixture."""
        return JourneyEngine(seed=42)

    @pytest.fixture
    def simple_journey(self):
        """Create simple journey fixture."""
        return JourneySpecification(
            journey_id="simple-journey",
            name="Simple Journey",
            events=[
                EventDefinition(
                    event_id="e1",
                    name="First Event",
                    event_type="encounter",
                    delay=DelaySpec(days=0)
                ),
                EventDefinition(
                    event_id="e2",
                    name="Second Event",
                    event_type="lab_order",
                    delay=DelaySpec(days=7),
                    depends_on="e1"
                ),
            ]
        )

    def test_engine_creation(self, engine):
        """Test engine creation."""
        assert engine.seed == 42

    def test_engine_creation_no_seed(self):
        """Test engine creation without seed."""
        engine = JourneyEngine()
        
        assert engine.seed is None

    def test_register_handler(self, engine):
        """Test registering event handler."""
        def my_handler(entity, event, context):
            return {"handled": True}
        
        engine.register_handler("patientsim", "encounter", my_handler)
        
        assert "patientsim" in engine._handlers
        assert "encounter" in engine._handlers["patientsim"]

    def test_create_timeline(self, engine, simple_journey):
        """Test creating timeline from journey."""
        entity = {"patient_id": "P001", "name": "Test Patient"}
        
        timeline = engine.create_timeline(
            entity=entity,
            entity_type="patient",
            journey=simple_journey,
            start_date=date(2024, 1, 1)
        )
        
        assert timeline.entity_id == "P001"
        assert len(timeline.events) == 2
        assert timeline.start_date == date(2024, 1, 1)

    def test_timeline_event_scheduling(self, engine, simple_journey):
        """Test events are scheduled correctly."""
        entity = {"patient_id": "P001"}
        
        timeline = engine.create_timeline(
            entity=entity,
            entity_type="patient",
            journey=simple_journey,
            start_date=date(2024, 1, 1)
        )
        
        # First event on start date
        assert timeline.events[0].scheduled_date == date(2024, 1, 1)
        # Second event 7 days later
        assert timeline.events[1].scheduled_date == date(2024, 1, 8)

    def test_conditional_event_included(self, engine):
        """Test conditional event is included when condition met."""
        journey = JourneySpecification(
            journey_id="conditional-journey",
            name="Conditional Journey",
            events=[
                EventDefinition(
                    event_id="e1",
                    name="Senior Event",
                    event_type="encounter",
                    conditions=[
                        EventCondition(field="entity.age", operator="gte", value=65)
                    ]
                )
            ]
        )
        
        entity = {"patient_id": "P001", "age": 70}
        timeline = engine.create_timeline(entity, "patient", journey)
        
        assert len(timeline.events) == 1

    def test_conditional_event_excluded(self, engine):
        """Test conditional event is excluded when condition not met."""
        journey = JourneySpecification(
            journey_id="conditional-journey",
            name="Conditional Journey",
            events=[
                EventDefinition(
                    event_id="e1",
                    name="Senior Event",
                    event_type="encounter",
                    conditions=[
                        EventCondition(field="entity.age", operator="gte", value=65)
                    ]
                )
            ]
        )
        
        entity = {"patient_id": "P002", "age": 40}
        timeline = engine.create_timeline(entity, "patient", journey)
        
        assert len(timeline.events) == 0

    def test_probabilistic_event(self, engine):
        """Test probabilistic event inclusion."""
        journey = JourneySpecification(
            journey_id="prob-journey",
            name="Probabilistic Journey",
            events=[
                EventDefinition(
                    event_id="e1",
                    name="Rare Event",
                    event_type="encounter",
                    probability=0.5
                )
            ]
        )
        
        # With seed=42, some entities will have event, some won't
        included = 0
        for i in range(100):
            engine_i = JourneyEngine(seed=i)
            timeline = engine_i.create_timeline(
                {"patient_id": f"P{i}"},
                "patient",
                journey
            )
            if len(timeline.events) > 0:
                included += 1
        
        # Should be roughly 50%
        assert 30 < included < 70

    def test_execute_event_with_handler(self, engine, simple_journey):
        """Test executing event with registered handler."""
        results = []
        
        def encounter_handler(entity, event, context):
            results.append(event.event_type)
            return {"encounter_id": "E001"}
        
        engine.register_handler("core", "encounter", encounter_handler)
        
        entity = {"patient_id": "P001"}
        timeline = engine.create_timeline(entity, "patient", simple_journey)
        
        result = engine.execute_event(
            timeline,
            timeline.events[0],
            entity,
            {}
        )
        
        assert result["status"] == "executed"
        assert "encounter" in results

    def test_execute_event_without_handler(self, engine, simple_journey):
        """Test executing event without handler."""
        entity = {"patient_id": "P001"}
        timeline = engine.create_timeline(entity, "patient", simple_journey)
        
        result = engine.execute_event(timeline, timeline.events[0], entity, {})
        
        assert result["status"] == "skipped"

    def test_execute_timeline(self, engine, simple_journey):
        """Test executing entire timeline."""
        def handler(entity, event, context):
            return {"done": True}
        
        engine.register_handler("core", "encounter", handler)
        engine.register_handler("core", "lab_order", handler)
        
        entity = {"patient_id": "P001"}
        timeline = engine.create_timeline(
            entity, "patient", simple_journey,
            start_date=date(2024, 1, 1)
        )
        
        results = engine.execute_timeline(
            timeline, entity,
            up_to_date=date(2024, 1, 10)
        )
        
        assert len(results) == 2
        assert all(r["status"] == "executed" for r in results)

    def test_timeline_end_date(self, engine, simple_journey):
        """Test timeline end date is set correctly."""
        entity = {"patient_id": "P001"}
        timeline = engine.create_timeline(
            entity, "patient", simple_journey,
            start_date=date(2024, 1, 1)
        )
        
        # End date should be date of last event
        assert timeline.end_date == date(2024, 1, 8)

    def test_reproducibility(self, simple_journey):
        """Test reproducibility with same seed."""
        entity = {"patient_id": "P001"}
        
        engine1 = JourneyEngine(seed=42)
        timeline1 = engine1.create_timeline(entity, "patient", simple_journey)
        
        engine2 = JourneyEngine(seed=42)
        timeline2 = engine2.create_timeline(entity, "patient", simple_journey)
        
        dates1 = [e.scheduled_date for e in timeline1.events]
        dates2 = [e.scheduled_date for e in timeline2.events]
        
        assert dates1 == dates2


# =============================================================================
# Convenience Function Tests
# =============================================================================

class TestConvenienceFunctions:
    """Tests for convenience functions."""

    def test_create_journey_engine(self):
        """Test create_journey_engine function."""
        engine = create_journey_engine(seed=123)
        
        assert engine.seed == 123

    def test_create_simple_journey(self):
        """Test create_simple_journey function."""
        journey = create_simple_journey(
            journey_id="test",
            name="Test Journey",
            events=[
                {"event_id": "e1", "name": "Event 1", "event_type": "encounter"},
                {"event_id": "e2", "name": "Event 2", "event_type": "lab_order",
                 "delay": {"days": 7}},
            ]
        )
        
        assert journey.journey_id == "test"
        assert len(journey.events) == 2
        assert journey.events[1].delay.days == 7

    def test_create_simple_journey_with_conditions(self):
        """Test create_simple_journey with conditions."""
        journey = create_simple_journey(
            journey_id="conditional",
            name="Conditional Journey",
            events=[
                {
                    "event_id": "e1",
                    "name": "Conditional Event",
                    "event_type": "encounter",
                    "conditions": [
                        {"field": "age", "operator": "gte", "value": 65}
                    ]
                }
            ]
        )
        
        assert len(journey.events[0].conditions) == 1


# =============================================================================
# Journey Templates Tests
# =============================================================================

class TestJourneyTemplates:
    """Tests for built-in journey templates."""

    def test_templates_exist(self):
        """Test that templates exist."""
        assert "diabetic-first-year" in JOURNEY_TEMPLATES
        assert "new-member-onboarding" in JOURNEY_TEMPLATES
        assert "phase3-pivotal-subject" in JOURNEY_TEMPLATES

    def test_get_journey_template(self):
        """Test getting journey template."""
        journey = get_journey_template("diabetic-first-year")
        
        assert journey.journey_id == "diabetic-first-year"
        assert len(journey.events) > 0

    def test_get_unknown_template_raises(self):
        """Test error for unknown template."""
        with pytest.raises(ValueError, match="not found"):
            get_journey_template("nonexistent-template")

    def test_diabetic_first_year_template(self):
        """Test diabetic first year template structure."""
        journey = get_journey_template("diabetic-first-year")
        
        event_ids = [e.event_id for e in journey.events]
        
        assert "initial_dx" in event_ids
        assert "initial_a1c" in event_ids
        assert "metformin_start" in event_ids

    def test_phase3_pivotal_template(self):
        """Test Phase 3 pivotal template structure."""
        journey = get_journey_template("phase3-pivotal-subject")
        
        event_ids = [e.event_id for e in journey.events]
        
        assert "screening" in event_ids
        assert "randomization" in event_ids
        assert "baseline_visit" in event_ids

    def test_template_creates_valid_timeline(self):
        """Test template can create valid timeline."""
        journey = get_journey_template("new-member-onboarding")
        engine = JourneyEngine(seed=42)
        
        timeline = engine.create_timeline(
            {"member_id": "M001"},
            "member",
            journey,
            start_date=date(2024, 1, 1)
        )
        
        assert len(timeline.events) >= 1
        assert timeline.start_date == date(2024, 1, 1)

    def test_all_templates_valid(self):
        """Test all templates can be parsed."""
        for template_name in JOURNEY_TEMPLATES:
            journey = get_journey_template(template_name)
            assert journey.journey_id is not None
            assert journey.name is not None
