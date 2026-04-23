"""Tests for skill-aware journey templates."""

import pytest
from datetime import date

from healthsim.generation import (
    SKILL_AWARE_TEMPLATES,
    list_skill_aware_templates,
    get_skill_aware_template,
)
from healthsim.generation.journey_engine import (
    JourneyEngine,
    JourneySpecification,
)


class TestSkillAwareTemplates:
    """Tests for skill-aware template definitions."""

    def test_list_templates(self):
        """Test listing available templates."""
        templates = list_skill_aware_templates()
        assert isinstance(templates, list)
        assert len(templates) >= 4
        assert "diabetic-first-year-skill" in templates

    def test_get_template(self):
        """Test getting a specific template."""
        template = get_skill_aware_template("diabetic-first-year-skill")
        assert template is not None
        assert template["journey_id"] == "diabetic-first-year-skill"
        assert "events" in template

    def test_get_nonexistent_template(self):
        """Test getting nonexistent template returns None."""
        template = get_skill_aware_template("nonexistent-template")
        assert template is None

    def test_diabetic_template_has_skill_refs(self):
        """Test that diabetic template uses skill references."""
        template = get_skill_aware_template("diabetic-first-year-skill")
        
        # Find the initial diagnosis event
        dx_event = None
        for event in template["events"]:
            if event["event_id"] == "initial_dx":
                dx_event = event
                break
        
        assert dx_event is not None
        assert "skill_ref" in dx_event["parameters"]
        assert dx_event["parameters"]["skill_ref"]["skill"] == "diabetes-management"

    def test_all_templates_have_required_fields(self):
        """Test all templates have required fields."""
        for name in list_skill_aware_templates():
            template = get_skill_aware_template(name)
            assert "journey_id" in template, f"{name} missing journey_id"
            assert "name" in template, f"{name} missing name"
            assert "events" in template, f"{name} missing events"
            assert "products" in template, f"{name} missing products"


class TestSkillAwareJourneyExecution:
    """Tests for executing skill-aware journeys."""

    @pytest.fixture
    def engine(self):
        """Create a journey engine."""
        return JourneyEngine(seed=42)

    def test_create_journey_from_skill_template(self, engine):
        """Test creating a JourneySpecification from skill-aware template."""
        template = get_skill_aware_template("diabetic-first-year-skill")
        journey = JourneySpecification.model_validate(template)
        
        assert journey.journey_id == "diabetic-first-year-skill"
        assert len(journey.events) >= 6
        assert "patientsim" in journey.products

    def test_create_timeline_from_skill_journey(self, engine):
        """Test creating a timeline from skill-aware journey."""
        template = get_skill_aware_template("diabetic-first-year-skill")
        journey = JourneySpecification.model_validate(template)
        
        entity = {
            "patient_id": "P001",
            "control_status": "moderate",
        }
        
        timeline = engine.create_timeline(
            entity=entity,
            entity_type="patient",
            journey=journey,
            start_date=date(2025, 1, 1),
        )
        
        assert timeline is not None
        assert len(timeline.events) >= 6
        # Events should have skill_ref in parameters
        dx_event = next(e for e in timeline.events if e.event_definition_id == "initial_dx")
        assert "skill_ref" in dx_event.parameters

    def test_execute_skill_aware_event(self, engine):
        """Test executing an event with skill_ref resolution."""
        # Track resolved parameters
        captured = {}
        
        def capture_handler(entity, event, context):
            captured["params"] = context.get("event_parameters", {})
            return {"status": "success"}
        
        engine.register_handler("patientsim", "diagnosis", capture_handler)
        
        template = get_skill_aware_template("diabetic-first-year-skill")
        journey = JourneySpecification.model_validate(template)
        
        entity = {"patient_id": "P001"}
        timeline = engine.create_timeline(
            entity=entity,
            entity_type="patient",
            journey=journey,
            start_date=date(2025, 1, 1),
        )
        
        # Execute the diagnosis event
        dx_event = next(e for e in timeline.events if e.event_definition_id == "initial_dx")
        result = engine.execute_event(timeline, dx_event, entity)
        
        # Should have resolved skill_ref
        assert result["status"] == "executed"
        assert "icd10" in captured["params"]
        # Should resolve to E11.x (diabetes code)
        assert captured["params"]["icd10"].startswith("E11")


class TestSkillAwareFallbacks:
    """Tests for fallback behavior in skill-aware journeys."""

    @pytest.fixture
    def engine(self):
        return JourneyEngine(seed=42)

    def test_fallback_used_for_unknown_skill(self, engine):
        """Test that fallback is used when skill can't be resolved."""
        # Create a journey with an unknown skill but valid fallback
        journey_data = {
            "journey_id": "test-fallback",
            "name": "Test Fallback",
            "products": ["patientsim"],
            "events": [
                {
                    "event_id": "test_event",
                    "name": "Test Event",
                    "event_type": "diagnosis",
                    "product": "patientsim",
                    "delay": {"days": 0},
                    "parameters": {
                        "skill_ref": {
                            "skill": "nonexistent-skill-xyz",
                            "lookup": "diagnosis_code",
                            "fallback": {"icd10": "Z00.00", "description": "Fallback code"},
                        }
                    },
                }
            ],
        }
        
        journey = JourneySpecification.model_validate(journey_data)
        entity = {"patient_id": "P001"}
        timeline = engine.create_timeline(
            entity=entity,
            entity_type="patient",
            journey=journey,
            start_date=date(2025, 1, 1),
        )
        
        # Resolve parameters
        event = timeline.events[0]
        entity_dict = engine._entity_to_dict(entity)
        resolved = engine._resolve_event_parameters(event.parameters, entity_dict)
        
        # Should use fallback
        assert "value" in resolved
        assert resolved["value"]["icd10"] == "Z00.00"


class TestMultipleSkillJourneys:
    """Tests for different skill-aware journey types."""

    @pytest.fixture
    def engine(self):
        return JourneyEngine(seed=42)

    def test_ckd_journey(self, engine):
        """Test CKD management journey."""
        template = get_skill_aware_template("ckd-management-skill")
        journey = JourneySpecification.model_validate(template)
        
        entity = {"patient_id": "P001", "ckd_stage": "3b"}
        timeline = engine.create_timeline(
            entity=entity,
            entity_type="patient",
            journey=journey,
            start_date=date(2025, 1, 1),
        )
        
        assert len(timeline.events) >= 3

    def test_hf_journey(self, engine):
        """Test heart failure management journey."""
        template = get_skill_aware_template("hf-management-skill")
        journey = JourneySpecification.model_validate(template)
        
        entity = {"patient_id": "P001", "hf_type": "reduced"}
        timeline = engine.create_timeline(
            entity=entity,
            entity_type="patient",
            journey=journey,
            start_date=date(2025, 1, 1),
        )
        
        assert len(timeline.events) >= 3

    def test_pharmacy_journey(self, engine):
        """Test pharmacy adherence journey."""
        template = get_skill_aware_template("pharmacy-adherence-skill")
        journey = JourneySpecification.model_validate(template)
        
        entity = {"rx_member_id": "RX001"}
        timeline = engine.create_timeline(
            entity=entity,
            entity_type="rx_member",
            journey=journey,
            start_date=date(2025, 1, 1),
        )
        
        assert len(timeline.events) >= 4
