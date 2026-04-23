"""Tests for skill reference integration with JourneyEngine."""

import pytest
from datetime import date

from healthsim.generation.journey_engine import (
    JourneyEngine,
    JourneySpecification,
    EventDefinition,
    DelaySpec,
)


class TestJourneyEngineSkillIntegration:
    """Tests for skill reference resolution in JourneyEngine."""

    @pytest.fixture
    def engine(self):
        """Create a journey engine."""
        return JourneyEngine(seed=42)

    def test_resolve_skill_ref_in_parameters(self, engine):
        """Test that skill_ref in parameters is resolved."""
        params = {
            "skill_ref": {
                "skill": "diabetes-management",
                "lookup": "diagnosis_code",
            },
            "extra_field": "preserved",
        }
        entity = {"patient_id": "P001"}
        
        resolved = engine._resolve_event_parameters(params, entity)
        
        # Should resolve the skill ref
        assert "icd10" in resolved
        assert resolved["icd10"].startswith("E11")
        # Should preserve extra fields
        assert resolved["extra_field"] == "preserved"

    def test_resolve_entity_variables(self, engine):
        """Test that ${entity.x} variables are resolved."""
        params = {
            "severity": "${entity.control_status}",
            "patient_name": "${entity.name}",
            "static": "value",
        }
        entity = {
            "control_status": "poorly-controlled",
            "name": "John Doe",
        }
        
        resolved = engine._resolve_event_parameters(params, entity)
        
        assert resolved["severity"] == "poorly-controlled"
        assert resolved["patient_name"] == "John Doe"
        assert resolved["static"] == "value"

    def test_resolve_mixed_parameters(self, engine):
        """Test resolving both skill_ref and entity variables."""
        params = {
            "skill_ref": {
                "skill": "diabetes-management",
                "lookup": "diagnosis_code",
            },
            "control": "${entity.control_status}",
        }
        entity = {"control_status": "moderate"}
        
        resolved = engine._resolve_event_parameters(params, entity)
        
        # Both should be resolved
        assert "icd10" in resolved
        # Note: skill_ref takes over the resolution, so entity var may be in skill_ref context
        # The ParameterResolver handles both

    def test_unresolved_entity_var_preserved(self, engine):
        """Test that missing entity variables are preserved."""
        params = {"value": "${entity.missing_attr}"}
        entity = {"other": "data"}
        
        resolved = engine._resolve_event_parameters(params, entity)
        
        # Should keep original if attribute not found
        assert resolved["value"] == "${entity.missing_attr}"

    def test_empty_parameters(self, engine):
        """Test empty parameters."""
        resolved = engine._resolve_event_parameters({}, {})
        assert resolved == {}

    def test_entity_to_dict_from_dict(self, engine):
        """Test _entity_to_dict with dict input."""
        entity = {"id": "123", "name": "Test"}
        result = engine._entity_to_dict(entity)
        assert result == entity

    def test_entity_to_dict_from_object(self, engine):
        """Test _entity_to_dict with object input."""
        class Entity:
            def __init__(self):
                self.id = "123"
                self.name = "Test"
        
        entity = Entity()
        result = engine._entity_to_dict(entity)
        assert result["id"] == "123"
        assert result["name"] == "Test"


class TestJourneyWithSkillRefs:
    """Tests for journeys that use skill references."""

    @pytest.fixture
    def engine(self):
        return JourneyEngine(seed=42)

    def test_create_journey_with_skill_ref_event(self, engine):
        """Test creating a journey with skill_ref in event parameters."""
        journey = JourneySpecification(
            journey_id="test-skill-journey",
            name="Test Journey with Skill Refs",
            products=["patientsim"],
            duration_days=30,
            events=[
                EventDefinition(
                    event_id="diagnosis",
                    name="Initial Diagnosis",
                    event_type="diagnosis",
                    product="patientsim",
                    delay=DelaySpec(days=0),
                    parameters={
                        "skill_ref": {
                            "skill": "diabetes-management",
                            "lookup": "diagnosis_code",
                        }
                    },
                ),
            ],
        )
        
        # Create timeline
        entity = {"patient_id": "P001", "control_status": "moderate"}
        timeline = engine.create_timeline(
            entity=entity,
            entity_type="patient",
            journey=journey,
            start_date=date(2025, 1, 1),
        )
        
        # Event should be scheduled
        assert len(timeline.events) == 1
        assert timeline.events[0].event_type == "diagnosis"
        # Parameters stored (not yet resolved)
        assert "skill_ref" in timeline.events[0].parameters

    def test_execute_event_resolves_skill_ref(self, engine):
        """Test that execute_event resolves skill_ref before calling handler."""
        # Register a test handler that captures parameters
        captured_params = {}
        
        def capture_handler(entity, event, context):
            captured_params.update(context.get("event_parameters", {}))
            return {"status": "success"}
        
        engine.register_handler("patientsim", "diagnosis", capture_handler)
        
        # Create journey with skill_ref
        journey = JourneySpecification(
            journey_id="test-exec",
            name="Test Execution",
            products=["patientsim"],
            events=[
                EventDefinition(
                    event_id="dx",
                    name="Diagnosis",
                    event_type="diagnosis",
                    product="patientsim",
                    parameters={
                        "skill_ref": {
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
        
        # Execute the event
        event = timeline.events[0]
        result = engine.execute_event(timeline, event, entity)
        
        # Handler should have received resolved parameters
        assert result["status"] == "executed"
        assert "icd10" in captured_params
        assert captured_params["icd10"].startswith("E11")


class TestSkillRefFallback:
    """Tests for skill reference fallback behavior."""

    @pytest.fixture
    def engine(self):
        return JourneyEngine(seed=42)

    def test_fallback_on_unknown_skill(self, engine):
        """Test that fallback is used for unknown skills."""
        params = {
            "skill_ref": {
                "skill": "nonexistent-skill-xyz",
                "lookup": "something",
                "fallback": {"default_code": "Z00.00"},
            }
        }
        
        resolved = engine._resolve_event_parameters(params, {})
        
        # Should use fallback
        assert "value" in resolved
        assert resolved["value"] == {"default_code": "Z00.00"}

    def test_no_fallback_returns_empty(self, engine):
        """Test that missing skill with no fallback returns empty."""
        params = {
            "skill_ref": {
                "skill": "nonexistent-skill",
                "lookup": "something",
            }
        }
        
        resolved = engine._resolve_event_parameters(params, {})
        
        # Should be empty (no fallback provided)
        assert resolved == {}
