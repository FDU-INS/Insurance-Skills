"""Tests for Skills composer."""

from pathlib import Path

import pytest

from patientsim.skills.composer import SkillComposer, SkillCompositionError
from patientsim.skills.schema import SkillType


class TestSkillComposer:
    """Tests for SkillComposer."""

    def test_compose_single_skill(self, tmp_path: Path) -> None:
        """Test composing a single skill."""
        skill_file = tmp_path / "test.md"
        skill_file.write_text(
            """# Test Skill
Simple skill.

## Metadata
- **Type**: domain-knowledge
- **Version**: 1.0

## Purpose
Testing single skill composition.
"""
        )

        composer = SkillComposer(skills_dir=tmp_path)
        skill = composer.compose([skill_file])

        assert skill.name == "Test Skill"
        assert skill.metadata.type == SkillType.DOMAIN_KNOWLEDGE

    def test_compose_multiple_skills(self, tmp_path: Path) -> None:
        """Test composing multiple skills."""
        # Create first skill
        skill1 = tmp_path / "skill1.md"
        skill1.write_text(
            """# Skill One
First skill.

## Metadata
- **Type**: domain-knowledge
- **Version**: 1.0

## Purpose
Base knowledge.

## Knowledge

### Concepts
- Basic concept
"""
        )

        # Create second skill
        skill2 = tmp_path / "skill2.md"
        skill2.write_text(
            """# Skill Two
Second skill.

## Metadata
- **Type**: domain-knowledge
- **Version**: 1.0

## Purpose
Additional knowledge.

## Knowledge

### Advanced Topics
- Advanced concept
"""
        )

        composer = SkillComposer(skills_dir=tmp_path)
        merged = composer.compose([skill1, skill2])

        assert "Skill One + Skill Two" in merged.name
        assert len(merged.knowledge) == 2
        assert "Concepts" in merged.knowledge
        assert "Advanced Topics" in merged.knowledge

    def test_compose_with_parameters_override(self, tmp_path: Path) -> None:
        """Test that later skills override earlier parameters."""
        skill1 = tmp_path / "base.md"
        skill1.write_text(
            """# Base Skill
Base.

## Metadata
- **Type**: scenario-template
- **Version**: 1.0

## Purpose
Base scenario.

## Parameters
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| age_range | range | 40-70 | Age range |
| severity | enum | moderate | Severity |
"""
        )

        skill2 = tmp_path / "override.md"
        skill2.write_text(
            """# Override Skill
Override.

## Metadata
- **Type**: scenario-template
- **Version**: 1.0

## Purpose
Override parameters.

## Parameters
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| age_range | range | 60-85 | Different age range |
"""
        )

        composer = SkillComposer(skills_dir=tmp_path)
        merged = composer.compose([skill1, skill2])

        # Later skill should override age_range
        age_param = merged.get_parameter("age_range")
        assert age_param is not None
        assert age_param.default == "60-85"

        # severity should still be present from first skill
        severity_param = merged.get_parameter("severity")
        assert severity_param is not None

    def test_compose_generation_rules_merge(self, tmp_path: Path) -> None:
        """Test merging generation rules."""
        skill1 = tmp_path / "demographics.md"
        skill1.write_text(
            """# Demographics Skill
Demographics.

## Metadata
- **Type**: scenario-template
- **Version**: 1.0

## Purpose
Demographics.

## Generation Rules

### Demographics
- Age: 40-70
- Gender: any
"""
        )

        skill2 = tmp_path / "vitals.md"
        skill2.write_text(
            """# Vitals Skill
Vitals.

## Metadata
- **Type**: scenario-template
- **Version**: 1.0

## Purpose
Vitals.

## Generation Rules

### Vital Signs
**Temperature**: 98-99 F
**Heart Rate**: 60-100 bpm
"""
        )

        composer = SkillComposer(skills_dir=tmp_path)
        merged = composer.compose([skill1, skill2])

        assert merged.generation_rules is not None
        assert len(merged.generation_rules.demographics) > 0
        assert len(merged.generation_rules.vital_signs) > 0

    def test_compose_with_dependencies(self, tmp_path: Path) -> None:
        """Test automatic dependency resolution."""
        # Create base skill
        base = tmp_path / "base.md"
        base.write_text(
            """# Base Knowledge
Base.

## Metadata
- **Type**: domain-knowledge
- **Version**: 1.0

## Purpose
Base knowledge.

## Knowledge

### Basics
- Basic info
"""
        )

        # Create dependent skill
        dependent = tmp_path / "dependent.md"
        dependent.write_text(
            """# Dependent Skill
Depends on base.

## Metadata
- **Type**: scenario-template
- **Version**: 1.0

## Purpose
Uses base knowledge.

## Dependencies
- base.md
"""
        )

        composer = SkillComposer(skills_dir=tmp_path)
        merged = composer.compose([dependent], resolve_dependencies=True)

        # Should include both skills
        assert "Base Knowledge" in merged.name
        assert "Dependent Skill" in merged.name
        assert len(merged.knowledge) > 0

    def test_compose_circular_dependency_error(self, tmp_path: Path) -> None:
        """Test error on circular dependencies."""
        skill1 = tmp_path / "skill1.md"
        skill1.write_text(
            """# Skill One
Skill 1.

## Metadata
- **Type**: domain-knowledge
- **Version**: 1.0

## Purpose
Test.

## Dependencies
- skill2.md
"""
        )

        skill2 = tmp_path / "skill2.md"
        skill2.write_text(
            """# Skill Two
Skill 2.

## Metadata
- **Type**: domain-knowledge
- **Version**: 1.0

## Purpose
Test.

## Dependencies
- skill1.md
"""
        )

        composer = SkillComposer(skills_dir=tmp_path)

        with pytest.raises(SkillCompositionError, match="Circular dependency"):
            composer.compose([skill1, skill2], resolve_dependencies=True)

    def test_compose_knowledge_additive(self, tmp_path: Path) -> None:
        """Test that knowledge sections are additive."""
        skill1 = tmp_path / "knowledge1.md"
        skill1.write_text(
            """# Knowledge One
First.

## Metadata
- **Type**: domain-knowledge
- **Version**: 1.0

## Purpose
Test.

## Knowledge

### Concepts
Concept A from skill 1.
"""
        )

        skill2 = tmp_path / "knowledge2.md"
        skill2.write_text(
            """# Knowledge Two
Second.

## Metadata
- **Type**: domain-knowledge
- **Version**: 1.0

## Purpose
Test.

## Knowledge

### Concepts
Concept B from skill 2.
"""
        )

        composer = SkillComposer(skills_dir=tmp_path)
        merged = composer.compose([skill1, skill2])

        # Both concepts should be present
        assert "Concept A" in merged.knowledge["Concepts"]
        assert "Concept B" in merged.knowledge["Concepts"]

    def test_compose_examples_combined(self, tmp_path: Path) -> None:
        """Test that examples are combined."""
        skill1 = tmp_path / "ex1.md"
        skill1.write_text(
            """# Skill One
First.

## Metadata
- **Type**: scenario-template
- **Version**: 1.0

## Purpose
Test.

## Examples

### Example 1: First Example
Example from skill 1.
"""
        )

        skill2 = tmp_path / "ex2.md"
        skill2.write_text(
            """# Skill Two
Second.

## Metadata
- **Type**: scenario-template
- **Version**: 1.0

## Purpose
Test.

## Examples

### Example 2: Second Example
Example from skill 2.
"""
        )

        composer = SkillComposer(skills_dir=tmp_path)
        merged = composer.compose([skill1, skill2])

        assert len(merged.examples) == 2

    def test_compose_references_unique(self, tmp_path: Path) -> None:
        """Test that duplicate references are removed."""
        skill1 = tmp_path / "ref1.md"
        skill1.write_text(
            """# Skill One
First.

## Metadata
- **Type**: domain-knowledge
- **Version**: 1.0

## Purpose
Test.

## References
- Reference A
- Reference B
"""
        )

        skill2 = tmp_path / "ref2.md"
        skill2.write_text(
            """# Skill Two
Second.

## Metadata
- **Type**: domain-knowledge
- **Version**: 1.0

## Purpose
Test.

## References
- Reference B
- Reference C
"""
        )

        composer = SkillComposer(skills_dir=tmp_path)
        merged = composer.compose([skill1, skill2])

        # Should have 3 unique references (A, B, C)
        assert len(merged.references) == 3
        assert "Reference A" in merged.references
        assert "Reference C" in merged.references

    def test_compose_empty_list_error(self) -> None:
        """Test error when composing empty skill list."""
        composer = SkillComposer()

        with pytest.raises(SkillCompositionError, match="No skills provided"):
            composer.compose([])

    def test_compose_caching(self, tmp_path: Path) -> None:
        """Test that loaded skills are cached."""
        skill_file = tmp_path / "cached.md"
        skill_file.write_text(
            """# Cached Skill
Test caching.

## Metadata
- **Type**: domain-knowledge
- **Version**: 1.0

## Purpose
Test skill caching.
"""
        )

        composer = SkillComposer(skills_dir=tmp_path)

        # Load same skill twice
        skill1 = composer._load_skill(skill_file)
        skill2 = composer._load_skill(skill_file)

        # Should be same instance (cached)
        assert skill1 is skill2
        assert str(skill_file) in composer._loaded_skills

    def test_compose_medications_additive(self, tmp_path: Path) -> None:
        """Test that medications are combined additively."""
        skill1 = tmp_path / "meds1.md"
        skill1.write_text(
            """# Meds One
First.

## Metadata
- **Type**: scenario-template
- **Version**: 1.0

## Purpose
Test.

## Generation Rules

### Medications
- Aspirin 81mg PO QD
- Lisinopril 10mg PO QD
"""
        )

        skill2 = tmp_path / "meds2.md"
        skill2.write_text(
            """# Meds Two
Second.

## Metadata
- **Type**: scenario-template
- **Version**: 1.0

## Purpose
Test.

## Generation Rules

### Medications
- Metformin 500mg PO BID
"""
        )

        composer = SkillComposer(skills_dir=tmp_path)
        merged = composer.compose([skill1, skill2])

        assert merged.generation_rules is not None
        # Should have all 3 medications
        assert len(merged.generation_rules.medications) >= 3

    def test_compose_variations_no_duplicates(self, tmp_path: Path) -> None:
        """Test that variations with same name use first occurrence."""
        skill1 = tmp_path / "var1.md"
        skill1.write_text(
            """# Skill One
First.

## Metadata
- **Type**: scenario-template
- **Version**: 1.0

## Purpose
Test.

## Variations

### Variation: Severe
From skill 1.
- severity: severe
"""
        )

        skill2 = tmp_path / "var2.md"
        skill2.write_text(
            """# Skill Two
Second.

## Metadata
- **Type**: scenario-template
- **Version**: 1.0

## Purpose
Test.

## Variations

### Variation: Severe
From skill 2 (should be ignored).
- severity: critical
"""
        )

        composer = SkillComposer(skills_dir=tmp_path)
        merged = composer.compose([skill1, skill2])

        # Should only have one "Severe" variation (from first skill)
        severe_variations = [v for v in merged.variations if v.name == "Severe"]
        assert len(severe_variations) == 1
