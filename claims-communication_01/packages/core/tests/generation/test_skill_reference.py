"""Tests for skill reference system."""

import pytest
from pathlib import Path

from healthsim.generation import (
    SkillReference,
    ResolvedParameters,
    SkillResolver,
    ParameterResolver,
    resolve_skill_ref,
)


class TestSkillReference:
    """Tests for SkillReference schema."""

    def test_create_skill_reference(self):
        """Test creating a skill reference."""
        ref = SkillReference(
            skill="diabetes-management",
            lookup="diagnosis_code",
        )
        assert ref.skill == "diabetes-management"
        assert ref.lookup == "diagnosis_code"
        assert ref.context == {}
        assert ref.fallback is None

    def test_skill_reference_with_context(self):
        """Test skill reference with context."""
        ref = SkillReference(
            skill="diabetes-management",
            lookup="lab_order",
            context={"control_status": "${entity.control_status}"},
        )
        assert ref.context["control_status"] == "${entity.control_status}"

    def test_skill_reference_with_fallback(self):
        """Test skill reference with fallback."""
        ref = SkillReference(
            skill="nonexistent-skill",
            lookup="something",
            fallback={"icd10": "Z00.00"},
        )
        assert ref.fallback == {"icd10": "Z00.00"}


class TestSkillResolver:
    """Tests for SkillResolver."""

    @pytest.fixture
    def resolver(self):
        """Create a resolver with the test skills directory."""
        # Find the skills directory
        current = Path(__file__).parent
        while current.parent != current:
            skills_path = current / "skills"
            if skills_path.exists():
                return SkillResolver(skills_path)
            current = current.parent
        
        # Default - let it auto-detect
        return SkillResolver()

    def test_load_skill(self, resolver):
        """Test loading a skill."""
        skill = resolver.load_skill("diabetes-management")
        assert skill is not None
        assert skill.name == "diabetes-management"

    def test_load_nonexistent_skill(self, resolver):
        """Test loading a nonexistent skill."""
        skill = resolver.load_skill("nonexistent-skill-xyz")
        assert skill is None

    def test_skill_caching(self, resolver):
        """Test that skills are cached."""
        skill1 = resolver.load_skill("diabetes-management")
        skill2 = resolver.load_skill("diabetes-management")
        assert skill1 is skill2

    def test_resolve_diagnosis_code(self, resolver):
        """Test resolving a diagnosis code."""
        ref = SkillReference(
            skill="diabetes-management",
            lookup="diagnosis_code",
        )
        result = resolver.resolve(ref)
        
        assert result.resolved_from == "skill"
        assert result.skill_used == "diabetes-management"
        assert "icd10" in result.parameters
        # Should find E11.x code
        assert result.parameters["icd10"].startswith("E11")

    def test_resolve_with_fallback(self, resolver):
        """Test resolution falling back to default."""
        ref = SkillReference(
            skill="nonexistent-skill",
            lookup="something",
            fallback={"default": "value"},
        )
        result = resolver.resolve(ref)
        
        assert result.resolved_from == "fallback"
        assert result.parameters == {"value": {"default": "value"}}

    def test_resolve_icd10_pattern(self, resolver):
        """Test ICD-10 pattern lookup."""
        ref = SkillReference(
            skill="diabetes-management",
            lookup="icd10",
        )
        result = resolver.resolve(ref)
        
        assert "value" in result.parameters
        # Should match E11.x pattern
        assert result.parameters["value"].startswith("E")

    def test_list_skills(self, resolver):
        """Test listing available skills."""
        skills = resolver.list_skills()
        assert isinstance(skills, list)
        # Should have some skills
        assert len(skills) > 0
        # diabetes-management should be present
        assert "diabetes-management" in skills


class TestParameterResolver:
    """Tests for ParameterResolver."""

    @pytest.fixture
    def resolver(self):
        """Create a parameter resolver."""
        return ParameterResolver()

    def test_resolve_direct_parameters(self, resolver):
        """Test resolving direct parameters (no skill ref)."""
        params = {
            "icd10": "E11.9",
            "description": "Type 2 diabetes",
        }
        result = resolver.resolve_event_parameters(params)
        assert result == params

    def test_resolve_entity_variable(self, resolver):
        """Test resolving entity variables."""
        params = {
            "severity": "${entity.control_status}",
            "name": "test",
        }
        entity = {"control_status": "poorly-controlled"}
        
        result = resolver.resolve_event_parameters(params, entity)
        assert result["severity"] == "poorly-controlled"
        assert result["name"] == "test"

    def test_resolve_skill_ref(self, resolver):
        """Test resolving skill reference."""
        params = {
            "skill_ref": {
                "skill": "diabetes-management",
                "lookup": "diagnosis_code",
            },
            "extra": "value",
        }
        
        result = resolver.resolve_event_parameters(params)
        # Should have resolved the skill ref
        assert "icd10" in result
        # Should keep extra params
        assert result["extra"] == "value"

    def test_resolve_nested_entity_var(self, resolver):
        """Test entity variable in nested dict."""
        params = {
            "outer": {
                "inner": "${entity.value}",
            },
        }
        entity = {"value": "resolved"}
        
        result = resolver.resolve_event_parameters(params, entity)
        assert result["outer"]["inner"] == "resolved"

    def test_unresolved_entity_var(self, resolver):
        """Test unresolved entity variable (missing attribute)."""
        params = {"value": "${entity.missing}"}
        entity = {"other": "value"}
        
        result = resolver.resolve_event_parameters(params, entity)
        # Should keep the original if not found
        assert result["value"] == "${entity.missing}"


class TestConvenienceFunction:
    """Tests for resolve_skill_ref convenience function."""

    def test_resolve_skill_ref_function(self):
        """Test the convenience function."""
        result = resolve_skill_ref(
            skill="diabetes-management",
            lookup="diagnosis_code",
        )
        assert "icd10" in result


class TestResolvedParameters:
    """Tests for ResolvedParameters model."""

    def test_default_values(self):
        """Test default values."""
        result = ResolvedParameters()
        assert result.parameters == {}
        assert result.skill_used is None
        assert result.resolved_from == "direct"

    def test_with_values(self):
        """Test with values."""
        result = ResolvedParameters(
            parameters={"icd10": "E11.9"},
            skill_used="diabetes-management",
            lookup_path="diagnosis_code",
            resolved_from="skill",
        )
        assert result.parameters["icd10"] == "E11.9"
        assert result.skill_used == "diabetes-management"
