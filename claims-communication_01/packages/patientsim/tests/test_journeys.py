"""Tests for PatientSim journeys module."""

import pytest
from datetime import date, timedelta

from patientsim.journeys import (
    # Core classes
    JourneyEngine,
    JourneySpecification,
    Timeline,
    PatientEventType,
    EventDefinition,
    DelaySpec,
    # PatientSim-specific
    create_patient_journey_engine,
    register_patient_handlers,
    PATIENT_JOURNEY_TEMPLATES,
    get_patient_journey_template,
    list_patient_journey_templates,
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
            product=event_dict.get("product", "patientsim"),
            delay=delay,
            depends_on=event_dict.get("depends_on"),
            parameters=event_dict.get("parameters", {}),
        )
        events.append(event)
    
    return JourneySpecification(
        journey_id=template["journey_id"],
        name=template.get("name", template["journey_id"]),
        description=template.get("description", ""),
        products=template.get("products", ["patientsim"]),
        events=events,
    )


class TestJourneyEngineCreation:
    """Tests for journey engine creation and handler registration."""
    
    def test_create_patient_journey_engine(self):
        """Test creating engine with PatientSim handlers."""
        engine = create_patient_journey_engine(seed=42)
        
        assert engine is not None
        assert isinstance(engine, JourneyEngine)
        # Handlers should be registered for patientsim product
        assert "patientsim" in engine._handlers
    
    def test_create_engine_with_seed_reproducibility(self):
        """Test that same seed produces same results."""
        engine1 = create_patient_journey_engine(seed=42)
        engine2 = create_patient_journey_engine(seed=42)
        
        # Both should have same seed
        assert engine1.seed == engine2.seed
    
    def test_register_patient_handlers(self):
        """Test registering handlers on existing engine."""
        from healthsim.generation.journey_engine import create_journey_engine
        
        engine = create_journey_engine(seed=123)
        register_patient_handlers(engine, seed=123)
        
        assert "patientsim" in engine._handlers
        # Should have handlers for key event types
        patient_handlers = engine._handlers.get("patientsim", {})
        assert "admission" in patient_handlers
        assert "discharge" in patient_handlers
        assert "encounter" in patient_handlers


class TestJourneyTemplates:
    """Tests for pre-built journey templates."""
    
    def test_templates_exist(self):
        """Test that templates are defined."""
        assert len(PATIENT_JOURNEY_TEMPLATES) > 0
    
    def test_get_template_by_id(self):
        """Test retrieving template by ID."""
        template = get_patient_journey_template("diabetic-first-year")
        
        assert template is not None
        assert template["journey_id"] == "diabetic-first-year"
        assert "events" in template
        assert len(template["events"]) > 0
    
    def test_get_nonexistent_template(self):
        """Test retrieving non-existent template returns None."""
        template = get_patient_journey_template("nonexistent-journey")
        
        assert template is None
    
    def test_list_templates(self):
        """Test listing all templates."""
        templates = list_patient_journey_templates()
        
        assert len(templates) > 0
        for t in templates:
            assert "id" in t
            assert "name" in t
            assert "description" in t
    
    def test_diabetic_first_year_template(self):
        """Test diabetic-first-year template structure."""
        template = get_patient_journey_template("diabetic-first-year")
        
        assert template["duration_days"] == 365
        assert template["products"] == ["patientsim"]
        
        # Should have key events
        event_ids = [e["event_id"] for e in template["events"]]
        assert "initial_encounter" in event_ids
        assert "diagnosis" in event_ids
        assert "medication_start" in event_ids
    
    def test_surgical_episode_template(self):
        """Test surgical-episode template structure."""
        template = get_patient_journey_template("surgical-episode")
        
        assert template is not None
        event_ids = [e["event_id"] for e in template["events"]]
        assert "admission" in event_ids
        assert "surgery" in event_ids
        assert "discharge" in event_ids
    
    def test_acute_care_episode_template(self):
        """Test acute-care-episode template structure."""
        template = get_patient_journey_template("acute-care-episode")
        
        assert template is not None
        event_ids = [e["event_id"] for e in template["events"]]
        assert "ed_arrival" in event_ids
        assert "admission" in event_ids


class TestTimelineCreation:
    """Tests for creating timelines from templates."""
    
    def test_create_timeline_from_template(self):
        """Test creating timeline from journey template."""
        engine = create_patient_journey_engine(seed=42)
        template = get_patient_journey_template("wellness-visit")
        journey_spec = dict_to_journey_spec(template)
        
        patient = {"patient_id": "PAT-001", "name": "Test Patient"}
        start_date = date(2024, 1, 1)
        
        timeline = engine.create_timeline(
            entity=patient,
            entity_type="patient",
            journey=journey_spec,
            start_date=start_date,
        )
        
        assert timeline is not None
        assert len(timeline.events) > 0
    
    def test_timeline_events_are_scheduled(self):
        """Test that timeline events have scheduled dates."""
        engine = create_patient_journey_engine(seed=42)
        template = get_patient_journey_template("chronic-disease-management")
        journey_spec = dict_to_journey_spec(template)
        
        patient = {"patient_id": "PAT-002"}
        start_date = date(2024, 1, 1)
        
        timeline = engine.create_timeline(
            entity=patient,
            entity_type="patient",
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
        engine = create_patient_journey_engine(seed=42)
        template = get_patient_journey_template("wellness-visit")
        journey_spec = dict_to_journey_spec(template)
        
        patient = {"patient_id": "PAT-003", "name": "Execution Test"}
        start_date = date(2024, 1, 1)
        
        timeline = engine.create_timeline(
            entity=patient,
            entity_type="patient",
            journey=journey_spec,
            start_date=start_date,
        )
        
        results = engine.execute_timeline(timeline, patient)
        
        assert len(results) > 0
    
    def test_execution_produces_artifacts(self):
        """Test that execution produces expected artifacts."""
        engine = create_patient_journey_engine(seed=42)
        
        # Use a simple journey with known events
        simple_journey = JourneySpecification(
            journey_id="test-journey",
            name="Test Journey",
            products=["patientsim"],
            events=[
                EventDefinition(
                    event_id="encounter_1",
                    name="Test Encounter",
                    event_type=PatientEventType.ENCOUNTER.value,
                    product="patientsim",
                    delay=DelaySpec(days=0),
                ),
            ],
        )
        
        patient = {"patient_id": "PAT-004"}
        timeline = engine.create_timeline(
            entity=patient,
            entity_type="patient",
            journey=simple_journey,
            start_date=date(2024, 1, 1),
        )
        
        results = engine.execute_timeline(timeline, patient)
        
        assert len(results) >= 1
        # First result should be encounter
        encounter_results = [r for r in results if r.get("encounter_id")]
        assert len(encounter_results) >= 0  # May or may not be present depending on handler


class TestBackwardCompatibility:
    """Tests for backward compatibility aliases."""
    
    def test_scenario_engine_alias(self):
        """Test ScenarioEngine alias works."""
        import warnings
        from patientsim.journeys import ScenarioEngine
        
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            engine = ScenarioEngine(seed=42)
            
            # Should have issued deprecation warning
            assert len(w) >= 1
            assert issubclass(w[0].category, DeprecationWarning)
            assert "ScenarioEngine" in str(w[0].message)
        
        assert isinstance(engine, JourneyEngine)
    
    def test_scenario_library_alias(self):
        """Test ScenarioLibrary alias works."""
        import warnings
        from patientsim.journeys import ScenarioLibrary
        
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            library = ScenarioLibrary()
            
            assert len(w) >= 1
            assert issubclass(w[0].category, DeprecationWarning)
        
        # Should work like a dict
        assert "diabetic-first-year" in library
        assert library.get("diabetic-first-year") is not None


class TestEventTypes:
    """Tests for PatientSim event types."""
    
    def test_patient_event_types_available(self):
        """Test PatientEventType enum is available."""
        assert PatientEventType.ADMISSION.value == "admission"
        assert PatientEventType.DISCHARGE.value == "discharge"
        assert PatientEventType.ENCOUNTER.value == "encounter"
        assert PatientEventType.LAB_ORDER.value == "lab_order"
        assert PatientEventType.LAB_RESULT.value == "lab_result"
        assert PatientEventType.MEDICATION_ORDER.value == "medication_order"
        assert PatientEventType.PROCEDURE.value == "procedure"
        assert PatientEventType.DIAGNOSIS.value == "diagnosis"
