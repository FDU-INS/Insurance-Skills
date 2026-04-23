"""Tests for Skills schema models."""

import pytest
from pydantic import ValidationError

from patientsim.skills.schema import (
    GenerationRules,
    ParameterType,
    Skill,
    SkillMetadata,
    SkillParameter,
    SkillType,
    SkillVariation,
)


class TestSkillMetadata:
    """Tests for SkillMetadata model."""

    def test_valid_metadata(self) -> None:
        """Test creating valid metadata."""
        metadata = SkillMetadata(
            type=SkillType.SCENARIO_TEMPLATE,
            version="1.0",
            author="Test Author",
            tags=["test", "scenario"],
        )

        assert metadata.type == SkillType.SCENARIO_TEMPLATE
        assert metadata.version == "1.0"
        assert metadata.author == "Test Author"
        assert metadata.tags == ["test", "scenario"]

    def test_version_validation_valid(self) -> None:
        """Test version validation accepts valid versions."""
        # Valid versions
        SkillMetadata(type=SkillType.DOMAIN_KNOWLEDGE, version="1.0")
        SkillMetadata(type=SkillType.DOMAIN_KNOWLEDGE, version="1.2.3")
        SkillMetadata(type=SkillType.DOMAIN_KNOWLEDGE, version="10.5.3")

    def test_version_validation_invalid(self) -> None:
        """Test version validation rejects invalid versions."""
        with pytest.raises(ValidationError, match="Version must be in format"):
            SkillMetadata(type=SkillType.DOMAIN_KNOWLEDGE, version="1")

        with pytest.raises(ValidationError, match="Version parts must be numeric"):
            SkillMetadata(type=SkillType.DOMAIN_KNOWLEDGE, version="1.x.3")

    def test_metadata_defaults(self) -> None:
        """Test metadata with default values."""
        metadata = SkillMetadata(type=SkillType.FORMAT_SPEC, version="2.1")

        assert metadata.author is None
        assert metadata.tags == []
        assert metadata.created is None
        assert metadata.updated is None


class TestSkillParameter:
    """Tests for SkillParameter model."""

    def test_valid_parameter(self) -> None:
        """Test creating valid parameter."""
        param = SkillParameter(
            name="age_range",
            type=ParameterType.RANGE,
            default="60-85",
            description="Patient age range",
        )

        assert param.name == "age_range"
        assert param.type == ParameterType.RANGE
        assert param.default == "60-85"

    def test_parameter_name_validation(self) -> None:
        """Test parameter name validation."""
        # Valid names
        SkillParameter(name="age", type=ParameterType.INTEGER, default=50, description="Age")
        SkillParameter(
            name="age_range", type=ParameterType.RANGE, default="40-70", description="Range"
        )
        SkillParameter(
            name="severity_level",
            type=ParameterType.STRING,
            default="moderate",
            description="Level",
        )

        # Invalid names
        with pytest.raises(ValidationError, match="must be alphanumeric"):
            SkillParameter(
                name="age-range", type=ParameterType.RANGE, default="40-70", description="Range"
            )

        with pytest.raises(ValidationError, match="cannot start with a digit"):
            SkillParameter(
                name="1_param", type=ParameterType.STRING, default="test", description="Test"
            )

    def test_validate_value_boolean(self) -> None:
        """Test validating boolean parameter values."""
        param = SkillParameter(
            name="enabled", type=ParameterType.BOOLEAN, default=True, description="Enable feature"
        )

        assert param.validate_value(True) is True
        assert param.validate_value(False) is True
        assert param.validate_value("true") is False
        assert param.validate_value(1) is False

    def test_validate_value_integer(self) -> None:
        """Test validating integer parameter values."""
        param = SkillParameter(
            name="count", type=ParameterType.INTEGER, default=5, description="Count"
        )

        assert param.validate_value(10) is True
        assert param.validate_value(0) is True
        assert param.validate_value(-5) is True
        assert param.validate_value(3.14) is False
        assert param.validate_value("10") is False

    def test_validate_value_string(self) -> None:
        """Test validating string parameter values."""
        param = SkillParameter(
            name="name", type=ParameterType.STRING, default="test", description="Name"
        )

        assert param.validate_value("hello") is True
        assert param.validate_value("") is True
        assert param.validate_value(123) is False

    def test_validate_value_range(self) -> None:
        """Test validating range parameter values."""
        param = SkillParameter(
            name="age_range", type=ParameterType.RANGE, default="40-70", description="Range"
        )

        assert param.validate_value("40-70") is True
        assert param.validate_value("0-100") is True
        assert param.validate_value("2.5-5.0") is True
        assert param.validate_value("70-40") is False  # min > max
        assert param.validate_value("not-a-range") is False
        assert param.validate_value(50) is False

    def test_validate_value_enum(self) -> None:
        """Test validating enum parameter values."""
        param = SkillParameter(
            name="severity",
            type=ParameterType.ENUM,
            default="moderate",
            description="Severity: mild, moderate, severe",
        )

        # For now, just checks it's a string
        assert param.validate_value("mild") is True
        assert param.validate_value("severe") is True
        assert param.validate_value(123) is False


class TestSkill:
    """Tests for Skill model."""

    def test_minimal_skill(self) -> None:
        """Test creating minimal valid skill."""
        skill = Skill(
            name="Test Skill",
            description="A test skill",
            metadata=SkillMetadata(type=SkillType.DOMAIN_KNOWLEDGE, version="1.0"),
            purpose="Testing purposes",
            raw_text="# Test Skill\nTest content",
        )

        assert skill.name == "Test Skill"
        assert skill.description == "A test skill"
        assert skill.metadata.type == SkillType.DOMAIN_KNOWLEDGE
        assert skill.purpose == "Testing purposes"
        assert skill.parameters == []
        assert skill.generation_rules is None

    def test_skill_with_parameters(self) -> None:
        """Test skill with parameters."""
        params = [
            SkillParameter(
                name="age_range",
                type=ParameterType.RANGE,
                default="60-85",
                description="Age range",
            ),
            SkillParameter(
                name="severity",
                type=ParameterType.ENUM,
                default="moderate",
                description="Severity level",
            ),
        ]

        skill = Skill(
            name="Scenario Skill",
            description="A scenario template",
            metadata=SkillMetadata(type=SkillType.SCENARIO_TEMPLATE, version="1.0"),
            purpose="Generate scenarios",
            parameters=params,
            raw_text="# Scenario Skill",
        )

        assert len(skill.parameters) == 2
        assert skill.get_parameter("age_range") is not None
        assert skill.get_parameter("severity") is not None
        assert skill.get_parameter("nonexistent") is None

    def test_get_parameter_default(self) -> None:
        """Test getting parameter default values."""
        skill = Skill(
            name="Test",
            description="Test",
            metadata=SkillMetadata(type=SkillType.SCENARIO_TEMPLATE, version="1.0"),
            purpose="Test",
            parameters=[
                SkillParameter(
                    name="age_range",
                    type=ParameterType.RANGE,
                    default="40-70",
                    description="Age",
                )
            ],
            raw_text="",
        )

        assert skill.get_parameter_default("age_range") == "40-70"
        assert skill.get_parameter_default("nonexistent") is None

    def test_validate_parameters_valid(self) -> None:
        """Test validating valid parameter values."""
        skill = Skill(
            name="Test",
            description="Test",
            metadata=SkillMetadata(type=SkillType.SCENARIO_TEMPLATE, version="1.0"),
            purpose="Test",
            parameters=[
                SkillParameter(
                    name="age_range",
                    type=ParameterType.RANGE,
                    default="40-70",
                    description="Age",
                ),
                SkillParameter(
                    name="enabled",
                    type=ParameterType.BOOLEAN,
                    default=True,
                    description="Enable",
                ),
            ],
            raw_text="",
        )

        errors = skill.validate_parameters({"age_range": "50-80", "enabled": False})
        assert errors == []

    def test_validate_parameters_unknown(self) -> None:
        """Test validating with unknown parameter."""
        skill = Skill(
            name="Test",
            description="Test",
            metadata=SkillMetadata(type=SkillType.SCENARIO_TEMPLATE, version="1.0"),
            purpose="Test",
            parameters=[],
            raw_text="",
        )

        errors = skill.validate_parameters({"unknown_param": "value"})
        assert len(errors) == 1
        assert "Unknown parameter" in errors[0]

    def test_validate_parameters_invalid_value(self) -> None:
        """Test validating with invalid value type."""
        skill = Skill(
            name="Test",
            description="Test",
            metadata=SkillMetadata(type=SkillType.SCENARIO_TEMPLATE, version="1.0"),
            purpose="Test",
            parameters=[
                SkillParameter(
                    name="age_range",
                    type=ParameterType.RANGE,
                    default="40-70",
                    description="Age",
                )
            ],
            raw_text="",
        )

        errors = skill.validate_parameters({"age_range": 123})  # Should be string
        assert len(errors) == 1
        assert "Invalid value" in errors[0]

    def test_skill_type_checks(self) -> None:
        """Test skill type checking methods."""
        scenario_skill = Skill(
            name="Scenario",
            description="Test",
            metadata=SkillMetadata(type=SkillType.SCENARIO_TEMPLATE, version="1.0"),
            purpose="Test",
            raw_text="",
        )

        assert scenario_skill.is_scenario_template() is True
        assert scenario_skill.is_domain_knowledge() is False
        assert scenario_skill.is_format_spec() is False
        assert scenario_skill.is_validation_rules() is False

        knowledge_skill = Skill(
            name="Knowledge",
            description="Test",
            metadata=SkillMetadata(type=SkillType.DOMAIN_KNOWLEDGE, version="1.0"),
            purpose="Test",
            raw_text="",
        )

        assert knowledge_skill.is_scenario_template() is False
        assert knowledge_skill.is_domain_knowledge() is True


class TestGenerationRules:
    """Tests for GenerationRules model."""

    def test_empty_generation_rules(self) -> None:
        """Test creating empty generation rules."""
        rules = GenerationRules()

        assert rules.demographics == {}
        assert rules.conditions == {}
        assert rules.vital_signs == {}
        assert rules.laboratory == {}
        assert rules.medications == []
        assert rules.timeline == []

    def test_generation_rules_with_data(self) -> None:
        """Test generation rules with data."""
        rules = GenerationRules(
            demographics={"Age": "60-85", "Gender": "any"},
            conditions={"primary": ["A41.9"], "comorbidities": ["I10", "E11.9"]},
            vital_signs={"Temperature": "101-104 F", "Heart Rate": "110-140 bpm"},
            laboratory={"WBC": "15-25 x10^3/uL", "CRP": "100-200 mg/L"},
            medications=["Ceftriaxone 2g IV Q24H", "Vancomycin 1.5g IV Q12H"],
            timeline=["Hour 1: Blood cultures", "Hour 3: Repeat vitals"],
        )

        assert rules.demographics["Age"] == "60-85"
        assert len(rules.conditions["primary"]) == 1
        assert len(rules.medications) == 2
        assert len(rules.timeline) == 2


class TestSkillVariation:
    """Tests for SkillVariation model."""

    def test_skill_variation(self) -> None:
        """Test creating skill variation."""
        variation = SkillVariation(
            name="Severe Case",
            description="Override for severe presentation",
            overrides={"severity": "severe", "age_range": "70-90"},
        )

        assert variation.name == "Severe Case"
        assert variation.description == "Override for severe presentation"
        assert variation.overrides["severity"] == "severe"
        assert variation.overrides["age_range"] == "70-90"
