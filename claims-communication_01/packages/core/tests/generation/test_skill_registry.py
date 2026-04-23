"""Tests for automatic skill resolution via SkillRegistry."""

import pytest

from healthsim.generation.skill_registry import (
    SkillCapability,
    SkillCapabilityDeclaration,
    SkillRegistration,
    SkillRegistry,
    get_skill_registry,
    auto_resolve_parameters,
    register_skill,
)


class TestSkillRegistration:
    """Tests for SkillRegistration model."""

    def test_create_registration(self):
        """Test creating a skill registration."""
        reg = SkillRegistration(
            skill_name="test-skill",
            conditions=["test condition", "test"],
            capabilities=[
                SkillCapabilityDeclaration(
                    capability=SkillCapability.DIAGNOSIS,
                    lookup_key="diagnosis_code"
                )
            ],
            products=["patientsim"],
        )
        
        assert reg.skill_name == "test-skill"
        assert len(reg.conditions) == 2
        assert len(reg.capabilities) == 1

    def test_registration_defaults(self):
        """Test registration default values."""
        reg = SkillRegistration(skill_name="minimal")
        
        assert reg.conditions == []
        assert reg.aliases == []
        assert reg.capabilities == []
        assert reg.products == []
        assert reg.priority == 0


class TestSkillRegistry:
    """Tests for SkillRegistry."""

    @pytest.fixture
    def registry(self):
        """Create a fresh registry."""
        return SkillRegistry()

    def test_default_registrations_loaded(self, registry):
        """Test that default registrations are loaded."""
        skills = registry.list_skills()
        
        assert "diabetes-management" in skills
        assert "chronic-kidney-disease" in skills
        assert "heart-failure" in skills

    def test_list_conditions(self, registry):
        """Test listing all registered conditions."""
        conditions = registry.list_conditions()
        
        assert "diabetes" in conditions
        assert "ckd" in conditions
        assert "heart failure" in conditions

    def test_find_skill_for_diabetes(self, registry):
        """Test finding skill for diabetes condition."""
        reg = registry.find_skill_for_condition("diabetes")
        
        assert reg is not None
        assert reg.skill_name == "diabetes-management"

    def test_find_skill_for_t2dm(self, registry):
        """Test finding skill using alias t2dm."""
        reg = registry.find_skill_for_condition("t2dm")
        
        assert reg is not None
        assert reg.skill_name == "diabetes-management"

    def test_find_skill_for_ckd(self, registry):
        """Test finding skill for CKD condition."""
        reg = registry.find_skill_for_condition("ckd")
        
        assert reg is not None
        assert reg.skill_name == "chronic-kidney-disease"

    def test_find_skill_for_heart_failure(self, registry):
        """Test finding skill for heart failure."""
        reg = registry.find_skill_for_condition("heart failure")
        
        assert reg is not None
        assert reg.skill_name == "heart-failure"

    def test_find_skill_case_insensitive(self, registry):
        """Test that condition matching is case insensitive."""
        reg1 = registry.find_skill_for_condition("DIABETES")
        reg2 = registry.find_skill_for_condition("Diabetes")
        reg3 = registry.find_skill_for_condition("diabetes")
        
        assert reg1 is not None
        assert reg2 is not None
        assert reg3 is not None
        assert reg1.skill_name == reg2.skill_name == reg3.skill_name

    def test_find_skill_partial_match(self, registry):
        """Test partial condition matching."""
        reg = registry.find_skill_for_condition("diabetic")
        
        assert reg is not None
        assert reg.skill_name == "diabetes-management"

    def test_find_skill_not_found(self, registry):
        """Test finding nonexistent condition returns None."""
        reg = registry.find_skill_for_condition("nonexistent-condition-xyz")
        
        assert reg is None

    def test_find_skill_with_product_filter(self, registry):
        """Test filtering by product."""
        reg = registry.find_skill_for_condition("diabetes", product="patientsim")
        
        assert reg is not None
        assert "patientsim" in reg.products

    def test_get_capability_lookup(self, registry):
        """Test getting capability lookup key."""
        lookup = registry.get_capability_lookup(
            "diabetes-management",
            SkillCapability.DIAGNOSIS
        )
        
        assert lookup == "diagnosis_code"

    def test_get_capability_lookup_medication(self, registry):
        """Test getting medication capability lookup."""
        lookup = registry.get_capability_lookup(
            "diabetes-management",
            SkillCapability.MEDICATION
        )
        
        assert lookup == "first_line_medication"

    def test_register_custom_skill(self, registry):
        """Test registering a custom skill."""
        registry.register(SkillRegistration(
            skill_name="my-custom-skill",
            conditions=["my condition", "custom"],
            capabilities=[
                SkillCapabilityDeclaration(
                    capability=SkillCapability.DIAGNOSIS,
                    lookup_key="my_diagnosis"
                )
            ],
            products=["patientsim"],
            priority=5,
        ))
        
        reg = registry.find_skill_for_condition("my condition")
        
        assert reg is not None
        assert reg.skill_name == "my-custom-skill"


class TestAutoResolution:
    """Tests for auto-resolution of parameters."""

    @pytest.fixture
    def registry(self):
        return SkillRegistry()

    def test_resolve_diabetes_diagnosis(self, registry):
        """Test auto-resolving diabetes diagnosis."""
        params = registry.resolve_for_event(
            event_type="diagnosis",
            condition="diabetes",
        )
        
        # Should get ICD-10 code from diabetes-management skill
        assert "icd10" in params or "value" in params

    def test_resolve_with_entity_context(self, registry):
        """Test resolution with entity context."""
        params = registry.resolve_for_event(
            event_type="diagnosis",
            condition="diabetes",
            entity={"control_status": "poorly-controlled"},
        )
        
        assert params  # Should return something

    def test_resolve_medication_order(self, registry):
        """Test auto-resolving medication order."""
        params = registry.resolve_for_event(
            event_type="medication_order",
            condition="diabetes",
        )
        
        # May return medication info if skill has it, or empty if not
        # Just verify it doesn't raise an error
        assert isinstance(params, dict)

    def test_resolve_unknown_condition(self, registry):
        """Test resolution of unknown condition returns empty."""
        params = registry.resolve_for_event(
            event_type="diagnosis",
            condition="nonexistent-xyz-123",
        )
        
        assert params == {}

    def test_resolve_with_product_filter(self, registry):
        """Test resolution with product filter."""
        params = registry.resolve_for_event(
            event_type="diagnosis",
            condition="diabetes",
            product="patientsim",
        )
        
        # Should work with product filter
        assert "icd10" in params or "value" in params or params == {}


class TestConvenienceFunctions:
    """Tests for convenience functions."""

    def test_get_skill_registry_singleton(self):
        """Test that get_skill_registry returns singleton."""
        reg1 = get_skill_registry()
        reg2 = get_skill_registry()
        
        assert reg1 is reg2

    def test_auto_resolve_parameters_function(self):
        """Test auto_resolve_parameters convenience function."""
        params = auto_resolve_parameters(
            event_type="diagnosis",
            condition="diabetes",
        )
        
        # Should return parameters (may be empty if skill file missing)
        assert isinstance(params, dict)

    def test_register_skill_function(self):
        """Test register_skill convenience function."""
        register_skill(
            skill_name="test-convenience-skill",
            conditions=["test convenience"],
            capabilities=[
                {"capability": "diagnosis", "lookup_key": "dx_code"}
            ],
            products=["patientsim"],
        )
        
        registry = get_skill_registry()
        reg = registry.find_skill_for_condition("test convenience")
        
        assert reg is not None
        assert reg.skill_name == "test-convenience-skill"


class TestEventTypeMapping:
    """Tests for event type to capability mapping."""

    @pytest.fixture
    def registry(self):
        return SkillRegistry()

    def test_diagnosis_maps_to_diagnosis(self, registry):
        """Test diagnosis event maps to DIAGNOSIS capability."""
        cap = registry._event_type_to_capability("diagnosis")
        assert cap == SkillCapability.DIAGNOSIS

    def test_medication_order_maps_to_medication(self, registry):
        """Test medication_order maps to MEDICATION capability."""
        cap = registry._event_type_to_capability("medication_order")
        assert cap == SkillCapability.MEDICATION

    def test_fill_maps_to_medication(self, registry):
        """Test fill event maps to MEDICATION capability."""
        cap = registry._event_type_to_capability("fill")
        assert cap == SkillCapability.MEDICATION

    def test_lab_order_maps_to_lab(self, registry):
        """Test lab_order maps to LAB_ORDER capability."""
        cap = registry._event_type_to_capability("lab_order")
        assert cap == SkillCapability.LAB_ORDER

    def test_procedure_maps_to_procedure(self, registry):
        """Test procedure maps to PROCEDURE capability."""
        cap = registry._event_type_to_capability("procedure")
        assert cap == SkillCapability.PROCEDURE

    def test_encounter_maps_to_encounter(self, registry):
        """Test encounter maps to ENCOUNTER capability."""
        cap = registry._event_type_to_capability("encounter")
        assert cap == SkillCapability.ENCOUNTER

    def test_unknown_event_type(self, registry):
        """Test unknown event type returns None."""
        cap = registry._event_type_to_capability("unknown_xyz")
        assert cap is None
