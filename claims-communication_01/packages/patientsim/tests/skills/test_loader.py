"""Tests for Skills loader."""

import pytest

from patientsim.skills.loader import SkillLoader, SkillParseError
from patientsim.skills.schema import ParameterType, SkillType


class TestSkillLoader:
    """Tests for SkillLoader."""

    def test_load_minimal_skill(self) -> None:
        """Test loading minimal valid skill."""
        content = """# Test Skill
A simple test skill.

## Metadata
- **Type**: domain-knowledge
- **Version**: 1.0

## Purpose
This skill is for testing the loader.
"""
        loader = SkillLoader()
        skill = loader.load_string(content)

        assert skill.name == "Test Skill"
        assert skill.metadata.type == SkillType.DOMAIN_KNOWLEDGE
        assert skill.metadata.version == "1.0"
        assert "testing" in skill.purpose.lower()

    def test_load_skill_with_metadata(self) -> None:
        """Test loading skill with full metadata."""
        content = """# Full Metadata Skill
Test skill with complete metadata.

## Metadata
- **Type**: scenario-template
- **Version**: 2.1.3
- **Author**: Test Author
- **Tags**: test, scenario, example

## Purpose
Testing metadata parsing.
"""
        loader = SkillLoader()
        skill = loader.load_string(content)

        assert skill.metadata.type == SkillType.SCENARIO_TEMPLATE
        assert skill.metadata.version == "2.1.3"
        assert skill.metadata.author == "Test Author"
        assert skill.metadata.tags == ["test", "scenario", "example"]

    def test_load_skill_with_parameters(self) -> None:
        """Test loading skill with parameters table."""
        content = """# Parameterized Skill
Skill with parameters.

## Metadata
- **Type**: scenario-template
- **Version**: 1.0

## Purpose
Testing parameter parsing.

## Parameters
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| age_range | range | 60-85 | Patient age range |
| severity | enum | moderate | Severity level |
| enabled | boolean | true | Enable feature |
| count | integer | 5 | Count value |
"""
        loader = SkillLoader()
        skill = loader.load_string(content)

        assert len(skill.parameters) == 4

        age_param = skill.get_parameter("age_range")
        assert age_param is not None
        assert age_param.type == ParameterType.RANGE
        assert age_param.default == "60-85"

        severity_param = skill.get_parameter("severity")
        assert severity_param is not None
        assert severity_param.type == ParameterType.ENUM

        enabled_param = skill.get_parameter("enabled")
        assert enabled_param is not None
        assert enabled_param.type == ParameterType.BOOLEAN
        assert enabled_param.default is True

        count_param = skill.get_parameter("count")
        assert count_param is not None
        assert count_param.type == ParameterType.INTEGER
        assert count_param.default == 5

    def test_load_skill_with_generation_rules(self) -> None:
        """Test loading skill with generation rules."""
        content = """# Scenario Skill
Skill with generation rules.

## Metadata
- **Type**: scenario-template
- **Version**: 1.0

## Purpose
Testing generation rules parsing.

## Generation Rules

### Demographics
- Age: 60-85
- Gender: weighted(male: 0.6, female: 0.4)

### Conditions
**Primary Diagnosis**:
- A41.9 (Sepsis, unspecified organism)

**Comorbidities**:
- I10 (Hypertension)
- E11.9 (Type 2 diabetes)

### Vital Signs
**Temperature**: 101-104 F
**Heart Rate**: 110-140 bpm

### Laboratory
**Infection Markers**:
- WBC: 15-25 x10^3/uL
- CRP: 100-200 mg/L

### Medications
- Ceftriaxone 2g IV Q24H
- Vancomycin 1.5g IV Q12H

### Timeline
1. Hour 1: Blood cultures
2. Hour 3: Repeat vitals
"""
        loader = SkillLoader()
        skill = loader.load_string(content)

        assert skill.generation_rules is not None

        # Check demographics
        assert "Age" in skill.generation_rules.demographics
        assert skill.generation_rules.demographics["Age"] == "60-85"

        # Check conditions
        assert "primary" in skill.generation_rules.conditions
        assert "comorbidities" in skill.generation_rules.conditions

        # Check vital signs
        assert "Temperature" in skill.generation_rules.vital_signs

        # Check medications
        assert len(skill.generation_rules.medications) == 2

        # Check timeline
        assert len(skill.generation_rules.timeline) >= 2

    def test_load_skill_with_knowledge(self) -> None:
        """Test loading domain knowledge skill."""
        content = """# Clinical Knowledge
Domain knowledge skill.

## Metadata
- **Type**: domain-knowledge
- **Version**: 1.0

## Purpose
Provide clinical background.

## Knowledge

### Clinical Concepts
- **Sepsis**: Life-threatening organ dysfunction
- **SIRS**: Systemic Inflammatory Response Syndrome

### Terminology
- **qSOFA**: Quick Sequential Organ Failure Assessment
- **MAP**: Mean Arterial Pressure
"""
        loader = SkillLoader()
        skill = loader.load_string(content)

        assert skill.metadata.type == SkillType.DOMAIN_KNOWLEDGE
        assert len(skill.knowledge) == 2
        assert "Clinical Concepts" in skill.knowledge
        assert "Terminology" in skill.knowledge
        assert "Sepsis" in skill.knowledge["Clinical Concepts"]

    def test_load_skill_with_variations(self) -> None:
        """Test loading skill with variations."""
        content = """# Skill with Variations
Test variations.

## Metadata
- **Type**: scenario-template
- **Version**: 1.0

## Purpose
Testing variations.

## Variations

### Variation: Severe Case
Override for severe presentation.
- severity: severe
- age_range: 70-90

### Variation: Mild Case
- severity: mild
- age_range: 40-60
"""
        loader = SkillLoader()
        skill = loader.load_string(content)

        assert len(skill.variations) == 2

        severe = skill.variations[0]
        assert severe.name == "Severe Case"
        assert severe.overrides["severity"] == "severe"
        assert severe.overrides["age_range"] == "70-90"

    def test_load_skill_with_examples(self) -> None:
        """Test loading skill with examples."""
        content = """# Skill with Examples
Test examples.

## Metadata
- **Type**: scenario-template
- **Version**: 1.0

## Purpose
Testing examples.

## Examples

### Example 1: Basic Usage
```
User: Generate a patient
Expected: Patient with default parameters
```

### Example 2: Custom Parameters
```
User: Generate with severity=severe
Expected: Severe case
```
"""
        loader = SkillLoader()
        skill = loader.load_string(content)

        assert len(skill.examples) >= 2
        assert "Basic Usage" in skill.examples[0]

    def test_load_skill_with_references(self) -> None:
        """Test loading skill with references."""
        content = """# Skill with References
Test references.

## Metadata
- **Type**: domain-knowledge
- **Version**: 1.0

## Purpose
Testing references.

## References
- Surviving Sepsis Campaign Guidelines
- SIRS Criteria
- qSOFA Score
"""
        loader = SkillLoader()
        skill = loader.load_string(content)

        assert len(skill.references) == 3
        assert "Surviving Sepsis Campaign Guidelines" in skill.references

    def test_load_skill_with_dependencies(self) -> None:
        """Test loading skill with dependencies."""
        content = """# Skill with Dependencies
Test dependencies.

## Metadata
- **Type**: scenario-template
- **Version**: 1.0

## Purpose
Testing dependencies.

## Dependencies
- skills/domain/clinical-basics.md
- skills/formats/hl7v2-adt.md
"""
        loader = SkillLoader()
        skill = loader.load_string(content)

        assert len(skill.dependencies) == 2
        assert "skills/domain/clinical-basics.md" in skill.dependencies

    def test_missing_title_error(self) -> None:
        """Test error when H1 title is missing."""
        content = """
## Metadata
- **Type**: domain-knowledge
- **Version**: 1.0

## Purpose
No title!
"""
        loader = SkillLoader()

        with pytest.raises(SkillParseError, match="No H1 title found"):
            loader.load_string(content)

    def test_missing_metadata_error(self) -> None:
        """Test error when Metadata section is missing."""
        content = """# Skill Without Metadata
Missing metadata section.

## Purpose
This will fail.
"""
        loader = SkillLoader()

        with pytest.raises(SkillParseError, match="Metadata.*not found"):
            loader.load_string(content)

    def test_missing_purpose_error(self) -> None:
        """Test error when Purpose section is missing."""
        content = """# Skill Without Purpose
Missing purpose.

## Metadata
- **Type**: domain-knowledge
- **Version**: 1.0
"""
        loader = SkillLoader()

        with pytest.raises(SkillParseError, match="Purpose.*not found"):
            loader.load_string(content)

    def test_invalid_metadata_type(self) -> None:
        """Test error when metadata type is invalid."""
        content = """# Invalid Type Skill
Bad type.

## Metadata
- **Type**: invalid-type
- **Version**: 1.0

## Purpose
This will fail.
"""
        loader = SkillLoader()

        with pytest.raises(SkillParseError):
            loader.load_string(content)

    def test_invalid_version_format(self) -> None:
        """Test error when version format is invalid."""
        content = """# Invalid Version Skill
Bad version.

## Metadata
- **Type**: domain-knowledge
- **Version**: not-a-version

## Purpose
This will fail.
"""
        loader = SkillLoader()

        with pytest.raises(SkillParseError):
            loader.load_string(content)

    def test_file_not_found_error(self) -> None:
        """Test error when file doesn't exist."""
        loader = SkillLoader()

        with pytest.raises(FileNotFoundError):
            loader.load_file("nonexistent-file.md")

    def test_parse_sections(self) -> None:
        """Test section parsing."""
        content = """# Title

## Section One
Content one.

## Section Two
Content two.
Multiple lines.

## Section Three
Content three.
"""
        loader = SkillLoader()
        sections = loader._parse_sections(content)

        assert "Section One" in sections
        assert "Section Two" in sections
        assert "Section Three" in sections
        assert "Content one" in sections["Section One"]
        assert "Multiple lines" in sections["Section Two"]

    def test_parse_empty_parameters_section(self) -> None:
        """Test parsing empty parameters section."""
        content = """# Skill
Test.

## Metadata
- **Type**: scenario-template
- **Version**: 1.0

## Purpose
Test.

## Parameters
"""
        loader = SkillLoader()
        skill = loader.load_string(content)

        assert skill.parameters == []

    def test_no_dependencies_handled(self) -> None:
        """Test that 'None' in dependencies is filtered out."""
        content = """# Skill
Test.

## Metadata
- **Type**: scenario-template
- **Version**: 1.0

## Purpose
Test.

## Dependencies
None - this is a standalone skill.
"""
        loader = SkillLoader()
        skill = loader.load_string(content)

        assert skill.dependencies == []
