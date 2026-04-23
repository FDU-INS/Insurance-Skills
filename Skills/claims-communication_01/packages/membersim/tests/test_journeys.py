"""Tests for Journey Engine and Timeline functionality."""

from datetime import date, timedelta

from membersim import Member
from membersim.journeys import (
    # Core classes
    JourneyEngine,
    JourneySpecification,
    Timeline,
    TimelineEvent,
    EventDefinition,
    DelaySpec,
    EventCondition,
    MemberEventType,
    # MemberSim-specific
    create_member_journey_engine,
    MEMBER_JOURNEY_TEMPLATES,
    get_member_journey_template,
    # Backward compat aliases
    ScenarioDefinition,
    ScenarioEngine,
    MemberTimeline,
)
from membersim.journeys.templates import (
    NEW_MEMBER_ONBOARDING,
    ANNUAL_WELLNESS,
    CHRONIC_CARE_MANAGEMENT,
    SURGICAL_EPISODE,
    QUALITY_GAP_CLOSURE,
)


class TestEventTypes:
    """Test event type enumerations."""

    def test_member_event_types(self) -> None:
        """Test that key member event types exist."""
        assert MemberEventType.NEW_ENROLLMENT.value == "new_enrollment"
        assert MemberEventType.CLAIM_PROFESSIONAL.value == "claim_professional"
        assert MemberEventType.GAP_CLOSED.value == "gap_closed"


class TestDelaySpec:
    """Test delay specification calculations."""

    def test_fixed_delay(self) -> None:
        """Test fixed delay."""
        delay = DelaySpec(days=30)
        td = delay.to_timedelta()
        assert td == timedelta(days=30)

    def test_uniform_delay_range(self) -> None:
        """Test uniform delay with range."""
        delay = DelaySpec(
            days=15,
            days_min=10,
            days_max=20,
            distribution="uniform",
        )
        # Run multiple times to verify range
        results = [delay.to_timedelta(seed=i).days for i in range(100)]
        assert min(results) >= 10
        assert max(results) <= 20

    def test_zero_delay(self) -> None:
        """Test zero delay."""
        delay = DelaySpec(days=0)
        td = delay.to_timedelta()
        assert td == timedelta(days=0)


class TestEventCondition:
    """Test event condition evaluation."""

    def test_equality_condition(self) -> None:
        """Test equality operator."""
        condition = EventCondition(
            field="demographics.gender",
            operator="eq",
            value="M",
        )
        context = {"demographics": {"gender": "M", "age": 45}}
        assert condition.evaluate(context) is True

    def test_greater_than_condition(self) -> None:
        """Test greater than operator."""
        condition = EventCondition(
            field="demographics.age",
            operator="gte",
            value=65,
        )
        context = {"demographics": {"age": 70}}
        assert condition.evaluate(context) is True

        context = {"demographics": {"age": 50}}
        assert condition.evaluate(context) is False

    def test_in_condition(self) -> None:
        """Test 'in' operator."""
        condition = EventCondition(
            field="entity.plan_type",
            operator="in",
            value=["HMO", "PPO"],
        )
        context = {"entity": {"plan_type": "HMO"}}
        assert condition.evaluate(context) is True

        context = {"entity": {"plan_type": "EPO"}}
        assert condition.evaluate(context) is False


class TestEventDefinition:
    """Test event definition construction."""

    def test_basic_event(self) -> None:
        """Test basic event creation."""
        event = EventDefinition(
            event_id="enroll_1",
            name="New Enrollment",
            event_type=MemberEventType.NEW_ENROLLMENT.value,
            product="membersim",
        )
        assert event.event_id == "enroll_1"
        assert event.probability == 1.0

    def test_event_with_delay(self) -> None:
        """Test event with delay specification."""
        event = EventDefinition(
            event_id="followup",
            name="Follow-up Visit",
            event_type=MemberEventType.CLAIM_PROFESSIONAL.value,
            product="membersim",
            delay=DelaySpec(days=30, days_min=25, days_max=35, distribution="uniform"),
            depends_on="initial_visit",
        )
        assert event.depends_on == "initial_visit"
        assert event.delay.days_min == 25

    def test_event_with_conditions(self) -> None:
        """Test event with conditions."""
        event = EventDefinition(
            event_id="high_risk_outreach",
            name="High Risk Outreach",
            event_type="milestone",
            product="membersim",
            conditions=[
                EventCondition(field="entity.risk_score", operator="gte", value=3.0),
            ],
            probability=0.8,
        )
        assert len(event.conditions) == 1
        assert event.probability == 0.8


class TestJourneySpecification:
    """Test journey specification construction."""

    def test_basic_journey(self) -> None:
        """Test basic journey creation."""
        journey = JourneySpecification(
            journey_id="test-journey",
            name="Test Journey",
            description="A test journey",
            products=["membersim"],
            events=[
                EventDefinition(
                    event_id="start",
                    name="Journey Start",
                    event_type=MemberEventType.NEW_ENROLLMENT.value,
                    product="membersim",
                ),
            ],
        )
        assert journey.journey_id == "test-journey"
        assert len(journey.events) == 1

    def test_journey_templates_available(self) -> None:
        """Test that journey templates are available."""
        assert "new-member-onboarding" in MEMBER_JOURNEY_TEMPLATES
        assert "annual-wellness" in MEMBER_JOURNEY_TEMPLATES
        assert "chronic-care-management" in MEMBER_JOURNEY_TEMPLATES

    def test_get_journey_template(self) -> None:
        """Test getting a journey template."""
        journey = get_member_journey_template("new-member-onboarding")
        assert journey.name == "New Member Onboarding"
        assert len(journey.events) > 0


class TestJourneyEngine:
    """Test journey engine functionality."""

    def test_create_engine(self) -> None:
        """Test engine creation."""
        engine = create_member_journey_engine(seed=42)
        assert engine is not None
        assert engine.seed == 42

    def test_create_timeline(self) -> None:
        """Test timeline creation from journey."""
        engine = create_member_journey_engine(seed=42)
        
        # Create a simple member-like object
        class SimpleMember:
            member_id = "M001"
            plan_code = "HMO001"
            group_id = "G001"
        
        member = SimpleMember()
        journey = get_member_journey_template("new-member-onboarding")
        
        timeline = engine.create_timeline(
            entity=member,
            entity_type="member",
            journey=journey,
            start_date=date(2024, 1, 1),
        )
        
        assert timeline.entity_id == "M001"
        assert timeline.entity_type == "member"
        assert len(timeline.events) > 0
        assert timeline.start_date == date(2024, 1, 1)

    def test_timeline_events_ordered(self) -> None:
        """Test that timeline events are in chronological order."""
        engine = create_member_journey_engine(seed=42)
        
        class SimpleMember:
            member_id = "M002"
        
        member = SimpleMember()
        journey = get_member_journey_template("surgical-episode")
        
        timeline = engine.create_timeline(
            entity=member,
            entity_type="member",
            journey=journey,
            start_date=date(2024, 1, 1),
        )
        
        dates = [e.scheduled_date for e in timeline.events]
        assert dates == sorted(dates), "Events should be in chronological order"


class TestTimeline:
    """Test timeline functionality."""

    def test_pending_events(self) -> None:
        """Test getting pending events."""
        timeline = Timeline(
            entity_id="M001",
            entity_type="member",
            start_date=date(2024, 1, 1),
        )
        
        event1 = TimelineEvent(
            timeline_event_id="e1",
            journey_id="test",
            event_definition_id="ev1",
            scheduled_date=date(2024, 1, 5),
            event_type="milestone",
            event_name="Event 1",
            status="pending",
        )
        event2 = TimelineEvent(
            timeline_event_id="e2",
            journey_id="test",
            event_definition_id="ev2",
            scheduled_date=date(2024, 1, 10),
            event_type="milestone",
            event_name="Event 2",
            status="executed",
        )
        
        timeline.add_event(event1)
        timeline.add_event(event2)
        
        pending = timeline.get_pending_events()
        assert len(pending) == 1
        assert pending[0].timeline_event_id == "e1"

    def test_events_up_to_date(self) -> None:
        """Test getting events up to a specific date."""
        timeline = Timeline(
            entity_id="M001",
            entity_type="member",
            start_date=date(2024, 1, 1),
        )
        
        for i in range(5):
            event = TimelineEvent(
                timeline_event_id=f"e{i}",
                journey_id="test",
                event_definition_id=f"ev{i}",
                scheduled_date=date(2024, 1, 1) + timedelta(days=i * 7),
                event_type="milestone",
                event_name=f"Event {i}",
            )
            timeline.add_event(event)
        
        events = timeline.get_events_up_to(date(2024, 1, 15))
        assert len(events) == 3  # Days 0, 7, 14


class TestBackwardCompatibility:
    """Test backward compatibility aliases."""

    def test_scenario_definition_alias(self) -> None:
        """Test ScenarioDefinition is aliased to JourneySpecification."""
        # ScenarioDefinition should work but issue deprecation warning
        import warnings
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            scenario = ScenarioDefinition(
                journey_id="compat-test",
                name="Compat Test",
                products=["membersim"],
                events=[],
            )
            assert len(w) == 1
            assert "deprecated" in str(w[0].message).lower()

    def test_scenario_engine_alias(self) -> None:
        """Test ScenarioEngine is aliased to JourneyEngine."""
        import warnings
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            engine = ScenarioEngine(seed=42)
            assert len(w) == 1
            assert "deprecated" in str(w[0].message).lower()


class TestPrebuiltTemplates:
    """Test pre-built journey templates."""

    def test_new_member_onboarding(self) -> None:
        """Test new member onboarding template."""
        journey = NEW_MEMBER_ONBOARDING
        assert journey.journey_id == "new-member-onboarding"
        assert "membersim" in journey.products
        
        # Check for expected events
        event_ids = [e.event_id for e in journey.events]
        assert "enrollment" in event_ids

    def test_annual_wellness(self) -> None:
        """Test annual wellness template."""
        journey = ANNUAL_WELLNESS
        assert journey.journey_id == "annual-wellness"

    def test_surgical_episode(self) -> None:
        """Test surgical episode template."""
        journey = SURGICAL_EPISODE
        assert journey.journey_id == "surgical-episode"
        
        # Should have consultation, pre-op, surgery, follow-ups
        event_names = [e.name for e in journey.events]
        assert any("consult" in name.lower() for name in event_names)
        assert any("surgery" in name.lower() or "surgical" in name.lower() for name in event_names)

    def test_quality_gap_closure(self) -> None:
        """Test quality gap closure template."""
        journey = QUALITY_GAP_CLOSURE
        assert journey.journey_id == "quality-gap-closure"
        
        event_types = [e.event_type for e in journey.events]
        assert MemberEventType.GAP_IDENTIFIED.value in event_types
        assert MemberEventType.GAP_CLOSED.value in event_types
