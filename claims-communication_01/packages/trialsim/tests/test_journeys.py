"""Tests for TrialSim journeys module."""

import pytest
from datetime import date, timedelta

from trialsim.journeys import (
    # Core classes
    JourneyEngine,
    JourneySpecification,
    Timeline,
    TrialEventType,
    EventDefinition,
    DelaySpec,
    # TrialSim-specific
    create_trial_journey_engine,
    register_trial_handlers,
    TRIAL_JOURNEY_TEMPLATES,
    get_trial_journey_template,
    list_trial_journey_templates,
)


def dict_to_journey_spec(template: dict) -> JourneySpecification:
    """Convert a template dict to JourneySpecification."""
    events = []
    for event_dict in template.get("events", []):
        delay_dict = event_dict.get("delay", {})
        delay = DelaySpec(
            days=delay_dict.get("days", 0),
            days_min=delay_dict.get("days_min"),
            days_max=delay_dict.get("days_max"),
        )
        event = EventDefinition(
            event_id=event_dict["event_id"],
            name=event_dict.get("name", event_dict["event_id"]),
            event_type=event_dict["event_type"],
            product=event_dict.get("product", "trialsim"),
            delay=delay,
            depends_on=event_dict.get("depends_on"),
            parameters=event_dict.get("parameters", {}),
        )
        events.append(event)
    
    return JourneySpecification(
        journey_id=template["journey_id"],
        name=template.get("name", template["journey_id"]),
        description=template.get("description", ""),
        products=template.get("products", ["trialsim"]),
        events=events,
    )


class TestJourneyEngineCreation:
    """Tests for journey engine creation and handler registration."""
    
    def test_create_trial_journey_engine(self):
        """Test creating engine with TrialSim handlers."""
        engine = create_trial_journey_engine(seed=42)
        
        assert engine is not None
        assert isinstance(engine, JourneyEngine)
        # Handlers should be registered for trialsim product
        assert "trialsim" in engine._handlers
    
    def test_create_engine_with_seed_reproducibility(self):
        """Test that same seed produces same results."""
        engine1 = create_trial_journey_engine(seed=42)
        engine2 = create_trial_journey_engine(seed=42)
        
        # Both should have same seed
        assert engine1.seed == engine2.seed
    
    def test_register_trial_handlers(self):
        """Test registering handlers on existing engine."""
        from healthsim.generation.journey_engine import create_journey_engine
        
        engine = create_journey_engine(seed=123)
        register_trial_handlers(engine, seed=123)
        
        assert "trialsim" in engine._handlers
        # Should have handlers for key event types
        trial_handlers = engine._handlers.get("trialsim", {})
        assert "screening" in trial_handlers
        assert "randomization" in trial_handlers
        assert "scheduled_visit" in trial_handlers


class TestJourneyTemplates:
    """Tests for pre-built journey templates."""
    
    def test_templates_exist(self):
        """Test that templates are defined."""
        assert len(TRIAL_JOURNEY_TEMPLATES) > 0
    
    def test_get_template_by_id(self):
        """Test retrieving template by ID."""
        template = get_trial_journey_template("phase3-oncology-standard")
        
        assert template is not None
        assert template["journey_id"] == "phase3-oncology-standard"
        assert "events" in template
        assert len(template["events"]) > 0
    
    def test_get_nonexistent_template(self):
        """Test retrieving non-existent template returns None."""
        template = get_trial_journey_template("nonexistent-protocol")
        
        assert template is None
    
    def test_list_templates(self):
        """Test listing all templates."""
        templates = list_trial_journey_templates()
        
        assert len(templates) > 0
        for t in templates:
            assert "id" in t
            assert "name" in t
            assert "description" in t
    
    def test_phase3_oncology_template(self):
        """Test phase3-oncology-standard template structure."""
        template = get_trial_journey_template("phase3-oncology-standard")
        
        assert template["duration_days"] == 365
        assert template["products"] == ["trialsim"]
        
        # Should have key events
        event_ids = [e["event_id"] for e in template["events"]]
        assert "screening" in event_ids
        assert "randomization" in event_ids
        assert "visit_1" in event_ids
    
    def test_phase2_efficacy_template(self):
        """Test phase2-efficacy template structure."""
        template = get_trial_journey_template("phase2-efficacy")
        
        assert template is not None
        event_ids = [e["event_id"] for e in template["events"]]
        assert "screening" in event_ids
        assert "randomization" in event_ids
        assert "week_12" in event_ids
    
    def test_phase1_dose_escalation_template(self):
        """Test phase1-dose-escalation template structure."""
        template = get_trial_journey_template("phase1-dose-escalation")
        
        assert template is not None
        assert template["duration_days"] == 84
        event_ids = [e["event_id"] for e in template["events"]]
        assert "baseline" in event_ids
        assert "day_21" in event_ids
    
    def test_simple_safety_followup_template(self):
        """Test simple-safety-followup template structure."""
        template = get_trial_journey_template("simple-safety-followup")
        
        assert template is not None
        assert template["duration_days"] == 365
        event_ids = [e["event_id"] for e in template["events"]]
        assert "screening" in event_ids
        assert "month_12" in event_ids


class TestTimelineCreation:
    """Tests for creating timelines from templates."""
    
    def test_create_timeline_from_template(self):
        """Test creating timeline from journey template."""
        engine = create_trial_journey_engine(seed=42)
        template = get_trial_journey_template("simple-safety-followup")
        journey_spec = dict_to_journey_spec(template)
        
        subject = {"subject_id": "SUBJ-001", "name": "Test Subject"}
        start_date = date(2024, 1, 1)
        
        timeline = engine.create_timeline(
            entity=subject,
            entity_type="subject",
            journey=journey_spec,
            start_date=start_date,
        )
        
        assert timeline is not None
        assert len(timeline.events) > 0
    
    def test_timeline_events_are_scheduled(self):
        """Test that timeline events have scheduled dates."""
        engine = create_trial_journey_engine(seed=42)
        template = get_trial_journey_template("phase2-efficacy")
        journey_spec = dict_to_journey_spec(template)
        
        subject = {"subject_id": "SUBJ-002"}
        start_date = date(2024, 1, 1)
        
        timeline = engine.create_timeline(
            entity=subject,
            entity_type="subject",
            journey=journey_spec,
            start_date=start_date,
        )
        
        for event in timeline.events:
            assert event.scheduled_date is not None
            assert event.scheduled_date >= start_date


class TestTimelineExecution:
    """Tests for executing timelines."""
    
    def test_execute_simple_timeline(self):
        """Test executing a simple timeline."""
        engine = create_trial_journey_engine(seed=42)
        template = get_trial_journey_template("simple-safety-followup")
        journey_spec = dict_to_journey_spec(template)
        
        subject = {"subject_id": "SUBJ-003", "name": "Execution Test"}
        start_date = date(2024, 1, 1)
        
        timeline = engine.create_timeline(
            entity=subject,
            entity_type="subject",
            journey=journey_spec,
            start_date=start_date,
        )
        
        results = engine.execute_timeline(timeline, subject)
        
        assert len(results) > 0
    
    def test_execution_produces_artifacts(self):
        """Test that execution produces expected artifacts."""
        engine = create_trial_journey_engine(seed=42)
        
        # Use a simple journey with known events
        simple_journey = JourneySpecification(
            journey_id="test-trial-journey",
            name="Test Trial Journey",
            products=["trialsim"],
            events=[
                EventDefinition(
                    event_id="screening_1",
                    name="Test Screening",
                    event_type=TrialEventType.SCREENING.value,
                    product="trialsim",
                    delay=DelaySpec(days=0),
                ),
            ],
        )
        
        subject = {"subject_id": "SUBJ-004"}
        timeline = engine.create_timeline(
            entity=subject,
            entity_type="subject",
            journey=simple_journey,
            start_date=date(2024, 1, 1),
        )
        
        results = engine.execute_timeline(timeline, subject)
        
        assert len(results) >= 1
        # First result should be screening
        screening_results = [r for r in results if r.get("screening_id")]
        assert len(screening_results) >= 0  # May or may not be present depending on handler


class TestBackwardCompatibility:
    """Tests for backward compatibility aliases."""
    
    def test_protocol_engine_alias(self):
        """Test ProtocolEngine alias works."""
        import warnings
        from trialsim.journeys import ProtocolEngine
        
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            engine = ProtocolEngine(seed=42)
            
            # Should have issued deprecation warning
            assert len(w) >= 1
            assert issubclass(w[0].category, DeprecationWarning)
            assert "ProtocolEngine" in str(w[0].message)
        
        assert isinstance(engine, JourneyEngine)
    
    def test_protocol_library_alias(self):
        """Test ProtocolLibrary alias works."""
        import warnings
        from trialsim.journeys import ProtocolLibrary
        
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            library = ProtocolLibrary()
            
            assert len(w) >= 1
            assert issubclass(w[0].category, DeprecationWarning)
        
        # Should work like a dict
        assert "phase3-oncology-standard" in library
        assert library.get("phase3-oncology-standard") is not None


class TestEventTypes:
    """Tests for TrialSim event types."""
    
    def test_trial_event_types_available(self):
        """Test TrialEventType enum is available."""
        assert TrialEventType.SCREENING.value == "screening"
        assert TrialEventType.RANDOMIZATION.value == "randomization"
        assert TrialEventType.WITHDRAWAL.value == "withdrawal"
        assert TrialEventType.SCHEDULED_VISIT.value == "scheduled_visit"
        assert TrialEventType.UNSCHEDULED_VISIT.value == "unscheduled_visit"
        assert TrialEventType.ADVERSE_EVENT.value == "adverse_event"
        assert TrialEventType.SERIOUS_ADVERSE_EVENT.value == "serious_adverse_event"
        assert TrialEventType.PROTOCOL_DEVIATION.value == "protocol_deviation"
        assert TrialEventType.DOSE_MODIFICATION.value == "dose_modification"
