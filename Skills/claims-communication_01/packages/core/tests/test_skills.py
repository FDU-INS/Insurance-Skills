"""Tests for healthsim.skills module."""

from pathlib import Path
from tempfile import NamedTemporaryFile

import pytest

from healthsim.skills import (
    ParameterType,
    Skill,
    SkillComposer,
    SkillCompositionError,
    SkillLoader,
    SkillMetadata,
    SkillParameter,
    SkillType,
    SkillVariation,
)


class TestSkillType:
    """Tests for SkillType enum."""

    def test_values(self) -> None:
        """Test enum values."""
        assert SkillType.DOMAIN_KNOWLEDGE.value == "domain-knowledge"
        assert SkillType.COHORT_TEMPLATE.value == "cohort-template"
        assert SkillType.FORMAT_SPEC.value == "format-spec"
        assert SkillType.VALIDATION_RULES.value == "validation-rules"
        assert SkillType.GENERATION_GUIDE.value == "generation-guide"


class TestParameterType:
    """Tests for ParameterType enum."""

    def test_values(self) -> None:
        """Test enum values."""
        assert ParameterType.RANGE.value == "range"
        assert ParameterType.ENUM.value == "enum"
        assert ParameterType.BOOLEAN.value == "boolean"
        assert ParameterType.INTEGER.value == "integer"
        assert ParameterType.STRING.value == "string"


class TestSkillParameter:
    """Tests for SkillParameter."""

    def test_creation(self) -> None:
        """Test creating a parameter."""
        param = SkillParameter(
            name="age_range",
            type=ParameterType.RANGE,
            default=[18, 65],
            description="Age range for generation",
        )

        assert param.name == "age_range"
        assert param.type == ParameterType.RANGE
        assert param.default == [18, 65]

    def test_validate_value_enum(self) -> None:
        """Test validating enum values."""
        param = SkillParameter(
            name="status",
            type=ParameterType.ENUM,
            options=["active", "inactive"],
        )

        assert param.validate_value("active") is True
        assert param.validate_value("pending") is False

    def test_validate_value_boolean(self) -> None:
        """Test validating boolean values."""
        param = SkillParameter(
            name="enabled",
            type=ParameterType.BOOLEAN,
        )

        assert param.validate_value(True) is True
        assert param.validate_value(False) is True
        assert param.validate_value("yes") is False

    def test_validate_value_integer_range(self) -> None:
        """Test validating integer with range."""
        param = SkillParameter(
            name="count",
            type=ParameterType.INTEGER,
            min_value=1,
            max_value=100,
        )

        assert param.validate_value(50) is True
        assert param.validate_value(0) is False
        assert param.validate_value(150) is False

    def test_validate_value_range_type(self) -> None:
        """Test validating range values."""
        param = SkillParameter(
            name="age_range",
            type=ParameterType.RANGE,
        )

        assert param.validate_value([18, 65]) is True
        assert param.validate_value([65, 18]) is False  # Invalid order
        assert param.validate_value([18]) is False  # Wrong length

    def test_validate_required(self) -> None:
        """Test required parameter validation."""
        param = SkillParameter(
            name="required_param",
            type=ParameterType.STRING,
            required=True,
        )

        assert param.validate_value(None) is False
        assert param.validate_value("value") is True


class TestSkillVariation:
    """Tests for SkillVariation."""

    def test_creation(self) -> None:
        """Test creating a variation."""
        variation = SkillVariation(
            name="verbose",
            description="Verbose output mode",
            parameter_overrides={"detail_level": "high"},
        )

        assert variation.name == "verbose"
        assert variation.description == "Verbose output mode"
        assert variation.parameter_overrides["detail_level"] == "high"


class TestSkill:
    """Tests for Skill."""

    def test_creation(self) -> None:
        """Test creating a skill."""
        skill = Skill(
            name="Test Skill",
            description="A test skill",
            metadata=SkillMetadata(type=SkillType.GENERATION_GUIDE),
            parameters=[SkillParameter(name="count", type=ParameterType.INTEGER, default=10)],
        )

        assert skill.name == "Test Skill"
        assert skill.metadata.type == SkillType.GENERATION_GUIDE
        assert len(skill.parameters) == 1

    def test_get_parameter(self) -> None:
        """Test getting parameter by name."""
        skill = Skill(
            name="Test",
            parameters=[
                SkillParameter(name="a", type=ParameterType.INTEGER),
                SkillParameter(name="b", type=ParameterType.STRING),
            ],
        )

        param = skill.get_parameter("a")
        assert param is not None
        assert param.name == "a"

        assert skill.get_parameter("nonexistent") is None

    def test_get_parameter_value(self) -> None:
        """Test getting parameter value with overrides."""
        skill = Skill(
            name="Test",
            parameters=[SkillParameter(name="count", type=ParameterType.INTEGER, default=10)],
        )

        # Default value
        assert skill.get_parameter_value("count") == 10

        # With override
        assert skill.get_parameter_value("count", {"count": 20}) == 20

    def test_apply_variation(self) -> None:
        """Test applying a variation."""
        skill = Skill(
            name="Test",
            parameters=[SkillParameter(name="mode", type=ParameterType.STRING, default="normal")],
            variations=[
                SkillVariation(
                    name="debug",
                    description="Debug mode",
                    parameter_overrides={"mode": "debug"},
                )
            ],
        )

        modified = skill.apply_variation("debug")

        assert "debug" in modified.name
        assert modified.get_parameter("mode").default == "debug"

    def test_apply_nonexistent_variation(self) -> None:
        """Test applying nonexistent variation raises error."""
        skill = Skill(name="Test")

        with pytest.raises(ValueError, match="not found"):
            skill.apply_variation("nonexistent")


class TestSkillLoader:
    """Tests for SkillLoader."""

    def test_load_minimal_skill(self) -> None:
        """Test loading a minimal skill file."""
        content = """---
name: Test Skill
description: A simple test skill
---

## Purpose

This is a test skill.
"""
        loader = SkillLoader()
        skill = loader.load_string(content)

        assert skill.name == "Test Skill"
        assert skill.description == "A simple test skill"
        assert "test skill" in skill.purpose.lower()

    def test_load_skill_with_metadata(self) -> None:
        """Test loading skill with full metadata."""
        content = """---
name: Full Skill
description: A skill with metadata
type: domain-knowledge
version: "2.0"
author: Test Author
tags:
  - testing
  - example
---

## Purpose

Test purpose.
"""
        loader = SkillLoader()
        skill = loader.load_string(content)

        assert skill.name == "Full Skill"
        assert skill.metadata.type == SkillType.DOMAIN_KNOWLEDGE
        assert skill.metadata.version == "2.0"
        assert skill.metadata.author == "Test Author"
        assert "testing" in skill.metadata.tags

    def test_load_skill_with_parameters(self) -> None:
        """Test loading skill with parameters section."""
        content = """---
name: Parameterized Skill
---

## Parameters

- **count** (integer): Number of items [default: 10]
- **name** (string): Item name
"""
        loader = SkillLoader()
        skill = loader.load_string(content)

        assert len(skill.parameters) == 2

        count_param = skill.get_parameter("count")
        assert count_param is not None
        assert count_param.type == ParameterType.INTEGER
        assert count_param.default == 10

    def test_load_skill_with_examples(self) -> None:
        """Test loading skill with examples."""
        content = """---
name: Example Skill
---

## Examples

- First example
- Second example
- Third example
"""
        loader = SkillLoader()
        skill = loader.load_string(content)

        assert len(skill.examples) == 3
        assert "First example" in skill.examples

    def test_load_skill_from_file(self) -> None:
        """Test loading skill from actual file."""
        content = """---
name: File Test
description: Test loading from file
---

## Purpose

Testing file loading.
"""
        with NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as f:
            f.write(content)
            path = Path(f.name)

        try:
            loader = SkillLoader()
            skill = loader.load_file(path)
            assert skill.name == "File Test"
        finally:
            path.unlink()

    def test_load_nonexistent_file(self) -> None:
        """Test loading nonexistent file raises error."""
        loader = SkillLoader()

        with pytest.raises(FileNotFoundError):
            loader.load_file(Path("/nonexistent/file.md"))

    def test_load_skill_no_frontmatter(self) -> None:
        """Test loading skill without frontmatter."""
        content = """# My Skill

## Purpose

A skill without YAML frontmatter.
"""
        loader = SkillLoader()
        skill = loader.load_string(content)

        # Should use source path as name
        assert skill.name == "<string>"
        assert "skill without yaml frontmatter" in skill.purpose.lower()


class TestSkillComposer:
    """Tests for SkillComposer."""

    def _create_skill_file(self, name: str, content: str) -> Path:
        """Helper to create a temporary skill file."""
        with NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, prefix=name, encoding="utf-8"
        ) as f:
            f.write(content)
            return Path(f.name)

    def test_compose_single_skill(self) -> None:
        """Test composing with single skill returns it unchanged."""
        content = """---
name: Single Skill
---

## Purpose

Test.
"""
        path = self._create_skill_file("single", content)

        try:
            composer = SkillComposer(skills_dir=path.parent)
            skill = composer.compose([path.name])
            assert skill.name == "Single Skill"
        finally:
            path.unlink()

    def test_compose_multiple_skills(self) -> None:
        """Test composing multiple skills."""
        content1 = """---
name: Skill One
---

## Purpose

First purpose.
"""
        content2 = """---
name: Skill Two
---

## Purpose

Second purpose.
"""
        path1 = self._create_skill_file("one", content1)
        path2 = self._create_skill_file("two", content2)

        try:
            composer = SkillComposer(skills_dir=path1.parent)
            skill = composer.compose([path1.name, path2.name])

            assert "Skill One" in skill.name
            assert "Skill Two" in skill.name
            assert "First purpose" in skill.purpose
            assert "Second purpose" in skill.purpose
        finally:
            path1.unlink()
            path2.unlink()

    def test_compose_merges_parameters(self) -> None:
        """Test that parameters are merged correctly."""
        content1 = """---
name: Skill One
---

## Parameters

- **param1** (integer): First param [default: 10]
"""
        content2 = """---
name: Skill Two
---

## Parameters

- **param2** (string): Second param
- **param1** (integer): Overridden [default: 20]
"""
        path1 = self._create_skill_file("one", content1)
        path2 = self._create_skill_file("two", content2)

        try:
            composer = SkillComposer(skills_dir=path1.parent)
            skill = composer.compose([path1.name, path2.name])

            # param1 should be overridden by later skill
            param1 = skill.get_parameter("param1")
            assert param1.default == 20

            # param2 should exist
            assert skill.get_parameter("param2") is not None
        finally:
            path1.unlink()
            path2.unlink()

    def test_compose_empty_list(self) -> None:
        """Test composing empty list raises error."""
        composer = SkillComposer()

        with pytest.raises(SkillCompositionError, match="No skills"):
            composer.compose([])

    def test_compose_merges_knowledge(self) -> None:
        """Test that knowledge sections are merged."""
        content1 = """---
name: Skill One
---

## Knowledge

### Topic A

Content for topic A.
"""
        content2 = """---
name: Skill Two
---

## Knowledge

### Topic B

Content for topic B.
"""
        path1 = self._create_skill_file("one", content1)
        path2 = self._create_skill_file("two", content2)

        try:
            composer = SkillComposer(skills_dir=path1.parent)
            skill = composer.compose([path1.name, path2.name])

            # Both knowledge sections should be present
            assert len(skill.knowledge) >= 1
        finally:
            path1.unlink()
            path2.unlink()
