"""Tests for automatic skill resolution in JourneyEngine."""

import pytest
from datetime import date

from healthsim.generation.journey_engine import (
    JourneyEngine,
    JourneySpecification,
    EventDefinition,
    DelaySpec,
)


class TestJourneyAutoResolution:
    """Tests for condition-based auto-resolution in journeys."""

    @pytest.fixture
    def engine(self):
        """Create a journey engine."""
        return JourneyEngine(seed=42)

    def test_event_with_condition_field(self, engine):
        """Test creating event with condition field."""
        journey = JourneySpecification(
            journey_id="test-auto",
            name="Test Auto-Resolution",
            products=["patientsim"],
            events=[
                EventDefinition(
                    event_id="dx",
                    name="Diagnosis",
                    event_type="diagnosis",
                    product="patientsim",
                    delay=DelaySpec(days=0),
                    condition="diabetes",  # Auto-resolve from diabetes-management skill
                ),
            ],
        )
        
        entity = {"patient_id": "P001"}
        timeline = engine.create_timeline(
            entity=entity,
            entity_type="patient",
            journey=journey,
            start_date=date(2025, 1, 1),
        )
        
        # Event should have condition set
        event = timeline.events[0]
        assert event.condition == "diabetes"

    def test_execute_event_auto_resolves(self, engine):
        """Test that execute_event auto-resolves from condition."""
        # Track what parameters the handler receives
        captured = {}
        
        def capture_handler(entity, event, context):
            captured["params"] = context.get("event_parameters", {})
            return {"status": "success"}
        
        engine.register_handler("patientsim", "diagnosis", capture_handler)
        
        journey = JourneySpecification(
            journey_id="test-auto",
            name="Test",
            products=["patientsim"],
            events=[
                EventDefinition(
                    event_id="dx",
                    name="Diagnosis",
                    event_type="diagnosis",
                    product="patientsim",
                    condition="diabetes",  # Should auto-resolve
                ),
            ],
        )
        
        entity = {"patient_id": "P001"}
        timeline = engine.create_timeline(
            entity=entity,
            entity_type="patient",
            journey=journey,
            start_date=date(2025, 1, 1),
        )
        
        event = timeline.events[0]
        result = engine.execute_event(timeline, event, entity)
        
        # Should have executed
        assert result["status"] == "executed"
        # Should have resolved ICD-10 from diabetes-management skill
        assert "icd10" in captured["params"]
        assert captured["params"]["icd10"].startswith("E11")

    def test_auto_resolve_with_entity_context(self, engine):
        """Test auto-resolution uses entity context."""
        captured = {}
        
        def capture_handler(entity, event, context):
            captured["params"] = context.get("event_parameters", {})
            return {"status": "success"}
        
        engine.register_handler("patientsim", "diagnosis", capture_handler)
        
        journey = JourneySpecification(
            journey_id="test-context",
            name="Test Context",
            products=["patientsim"],
            events=[
                EventDefinition(
                    event_id="dx",
                    name="Diagnosis",
                    event_type="diagnosis",
                    product="patientsim",
                    condition="diabetes",
                ),
            ],
        )
        
        # Entity with control_status
        entity = {"patient_id": "P001", "control_status": "poorly-controlled"}
        timeline = engine.create_timeline(
            entity=entity,
            entity_type="patient",
            journey=journey,
            start_date=date(2025, 1, 1),
        )
        
        event = timeline.events[0]
        engine.execute_event(timeline, event, entity)
        
        # Resolution should have happened with entity context
        assert "icd10" in captured["params"]

    def test_auto_resolve_preserves_extra_params(self, engine):
        """Test that extra parameters are preserved with auto-resolution."""
        captured = {}
        
        def capture_handler(entity, event, context):
            captured["params"] = context.get("event_parameters", {})
            return {"status": "success"}
        
        engine.register_handler("patientsim", "diagnosis", capture_handler)
        
        journey = JourneySpecification(
            journey_id="test-extra",
            name="Test Extra Params",
            products=["patientsim"],
            events=[
                EventDefinition(
                    event_id="dx",
                    name="Diagnosis",
                    event_type="diagnosis",
                    product="patientsim",
                    condition="diabetes",
                    parameters={
                        "severity": "severe",  # Extra param
                        "note": "Initial diagnosis",
                    },
                ),
            ],
        )
        
        entity = {"patient_id": "P001"}
        timeline = engine.create_timeline(
            entity=entity,
            entity_type="patient",
            journey=journey,
            start_date=date(2025, 1, 1),
        )
        
        event = timeline.events[0]
        engine.execute_event(timeline, event, entity)
        
        # Should have both auto-resolved and extra params
        assert "icd10" in captured["params"]
        assert captured["params"]["severity"] == "severe"
        assert captured["params"]["note"] == "Initial diagnosis"

    def test_skill_ref_takes_precedence(self, engine):
        """Test that explicit skill_ref takes precedence over condition."""
        captured = {}
        
        def capture_handler(entity, event, context):
            captured["params"] = context.get("event_parameters", {})
            return {"status": "success"}
        
        engine.register_handler("patientsim", "diagnosis", capture_handler)
        
        journey = JourneySpecification(
            journey_id="test-precedence",
            name="Test Precedence",
            products=["patientsim"],
            events=[
                EventDefinition(
                    event_id="dx",
                    name="Diagnosis",
                    event_type="diagnosis",
                    product="patientsim",
                    condition="ckd",  # Would resolve to CKD codes
                    parameters={
                        "skill_ref": {  # But skill_ref overrides
                            "skill": "diabetes-management",
                            "lookup": "diagnosis_code",
                        }
                    },
                ),
            ],
        )
        
        entity = {"patient_id": "P001"}
        timeline = engine.create_timeline(
            entity=entity,
            entity_type="patient",
            journey=journey,
            start_date=date(2025, 1, 1),
        )
        
        event = timeline.events[0]
        engine.execute_event(timeline, event, entity)
        
        # Should use skill_ref (diabetes) not condition (ckd)
        assert "icd10" in captured["params"]
        assert captured["params"]["icd10"].startswith("E11")  # Diabetes, not N18.x

    def test_unknown_condition_uses_params(self, engine):
        """Test that unknown condition falls back to provided params."""
        captured = {}
        
        def capture_handler(entity, event, context):
            captured["params"] = context.get("event_parameters", {})
            return {"status": "success"}
        
        engine.register_handler("patientsim", "diagnosis", capture_handler)
        
        journey = JourneySpecification(
            journey_id="test-unknown",
            name="Test Unknown",
            products=["patientsim"],
            events=[
                EventDefinition(
                    event_id="dx",
                    name="Diagnosis",
                    event_type="diagnosis",
                    product="patientsim",
                    condition="nonexistent-xyz-123",  # Unknown condition
                    parameters={
                        "icd10": "Z99.99",  # Fallback
                        "description": "Other condition",
                    },
                ),
            ],
        )
        
        entity = {"patient_id": "P001"}
        timeline = engine.create_timeline(
            entity=entity,
            entity_type="patient",
            journey=journey,
            start_date=date(2025, 1, 1),
        )
        
        event = timeline.events[0]
        engine.execute_event(timeline, event, entity)
        
        # Should use provided params as fallback
        assert captured["params"]["icd10"] == "Z99.99"
        assert captured["params"]["description"] == "Other condition"


class TestAutoResolutionJourneyTemplates:
    """Tests for auto-resolution journey templates."""

    @pytest.fixture
    def engine(self):
        return JourneyEngine(seed=42)

    def test_create_auto_resolution_journey(self, engine):
        """Test creating a journey template with auto-resolution."""
        journey_data = {
            "journey_id": "diabetes-auto",
            "name": "Diabetes Journey (Auto-Resolution)",
            "products": ["patientsim"],
            "events": [
                {
                    "event_id": "initial_dx",
                    "name": "Initial Diagnosis",
                    "event_type": "diagnosis",
                    "product": "patientsim",
                    "delay": {"days": 0},
                    "condition": "diabetes",  # Auto-resolve
                },
                {
                    "event_id": "initial_labs",
                    "name": "Initial Labs",
                    "event_type": "lab_order",
                    "product": "patientsim",
                    "delay": {"days": 0},
                    "depends_on": "initial_dx",
                    "condition": "diabetes",  # Auto-resolve labs
                },
                {
                    "event_id": "start_meds",
                    "name": "Start Medication",
                    "event_type": "medication_order",
                    "product": "patientsim",
                    "delay": {"days": 3},
                    "depends_on": "initial_dx",
                    "condition": "diabetes",  # Auto-resolve medication
                },
            ],
        }
        
        journey = JourneySpecification.model_validate(journey_data)
        
        assert len(journey.events) == 3
        assert all(e.condition == "diabetes" for e in journey.events)

    def test_uses_auto_resolution_method(self):
        """Test EventDefinition.uses_auto_resolution() method."""
        event_with_condition = EventDefinition(
            event_id="e1",
            name="Test",
            event_type="diagnosis",
            condition="diabetes",
        )
        
        event_without = EventDefinition(
            event_id="e2",
            name="Test",
            event_type="diagnosis",
        )
        
        assert event_with_condition.uses_auto_resolution() is True
        assert event_without.uses_auto_resolution() is False
