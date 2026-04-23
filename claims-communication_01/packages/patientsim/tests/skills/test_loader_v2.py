"""Tests for Skills loader v2.0 format support."""

from patientsim.skills.loader import SkillLoader


class TestSkillLoaderV2Format:
    """Tests for v2.0 format skills."""

    def test_load_minimal_v2_skill(self) -> None:
        """Test loading minimal v2.0 skill with new sections."""
        content = """# Test V2 Skill
A simple v2.0 test skill.

## For Claude

Use this skill when the user requests test patients. This teaches you how to generate test data.

## Metadata
- **Type**: domain-knowledge
- **Version**: 2.0

## Purpose
This skill is for testing the v2.0 loader.

## When to Use This Skill

Apply this skill when the user mentions:

**Direct Keywords**:
- "test", "testing", "test patient"

**Clinical Scenarios**:
- Testing scenarios
"""
        loader = SkillLoader()
        skill = loader.load_string(content)

        assert skill.name == "Test V2 Skill"
        assert skill.is_v2_format()
        assert skill.get_format_version() == "2.0"
        assert skill.for_claude is not None
        assert "Use this skill when" in skill.for_claude
        assert skill.when_to_use is not None
        assert "Direct Keywords" in skill.when_to_use

    def test_load_v2_skill_with_all_sections(self) -> None:
        """Test loading v2.0 skill with all new sections."""
        content = """# Complete V2 Skill
Complete v2.0 skill.

## For Claude

Use this skill when the user asks for septic patients.

## Metadata
- **Type**: scenario-template
- **Version**: 2.0
- **Author**: Test Author
- **Tags**: test, v2, sepsis

## Purpose
Testing complete v2.0 format.

## When to Use This Skill

**Direct Keywords**:
- "sepsis", "septic"

**Clinical Scenarios**:
- ICU admission with infection

## Domain Knowledge

### Sepsis Pathophysiology
Sepsis is a dysregulated host response to infection.

**Why this matters for generation**: Generate appropriate vital signs.

## Generation Guidelines

### How to Apply This Knowledge

**When the user says**: "Generate a septic patient"

**Claude should**:
1. Choose infection source
2. Set severity level

## Parameters
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| severity | enum | moderate | How severe should the sepsis be? |

## Examples

### Example 1: Basic Request
**User says**: "Generate a septic patient"

**Claude interprets**:
- Severity: moderate (default)
"""
        loader = SkillLoader()
        skill = loader.load_string(content)

        assert skill.is_v2_format()
        assert skill.for_claude is not None
        assert skill.when_to_use is not None
        assert skill.generation_guidelines is not None
        assert "How to Apply This Knowledge" in skill.generation_guidelines
        assert "Choose infection source" in skill.generation_guidelines

    def test_v1_skill_not_detected_as_v2(self) -> None:
        """Test that v1.0 skills are not detected as v2.0."""
        content = """# V1 Skill
Old format skill.

## Metadata
- **Type**: domain-knowledge
- **Version**: 1.0

## Purpose
This is a v1.0 skill without new sections.
"""
        loader = SkillLoader()
        skill = loader.load_string(content)

        assert not skill.is_v2_format()
        assert skill.get_format_version() == "1.0"
        assert skill.for_claude is None
        assert skill.when_to_use is None

    def test_v2_skill_with_v1_sections(self) -> None:
        """Test v2.0 skill can still have v1.0 sections (backward compatible)."""
        content = """# Hybrid Skill
Has both v1.0 and v2.0 sections.

## For Claude
Use this when testing.

## Metadata
- **Type**: scenario-template
- **Version**: 2.0

## Purpose
Testing backward compatibility.

## When to Use This Skill
**Keywords**: test

## Generation Rules

### Demographics
- Age: 60-85

### Vital Signs
- Temperature: 101-104 F
"""
        loader = SkillLoader()
        skill = loader.load_string(content)

        # Should be detected as v2.0
        assert skill.is_v2_format()

        # Should also have v1.0 generation rules
        assert skill.generation_rules is not None
        assert "Age" in skill.generation_rules.demographics

    def test_v2_sections_stored_in_content(self) -> None:
        """Test that v2.0 sections are also stored in content dict."""
        content = """# Test Skill

## For Claude
Test content.

## Metadata
- **Type**: domain-knowledge
- **Version**: 2.0

## Purpose
Testing.

## When to Use This Skill
Keywords.

## Generation Guidelines
Guidelines content.
"""
        loader = SkillLoader()
        skill = loader.load_string(content)

        # v2.0 sections should be in both dedicated fields AND content dict
        assert skill.for_claude == "Test content."
        assert skill.content["For Claude"] == "Test content."

        assert skill.when_to_use == "Keywords."
        assert skill.content["When to Use This Skill"] == "Keywords."

        assert skill.generation_guidelines == "Guidelines content."
        assert skill.content["Generation Guidelines"] == "Guidelines content."

    def test_domain_knowledge_parsing_in_v2(self) -> None:
        """Test that Domain Knowledge section is parsed into knowledge dict."""
        content = """# Knowledge Skill

## For Claude
Use for testing.

## Metadata
- **Type**: domain-knowledge
- **Version**: 2.0

## Purpose
Testing knowledge parsing.

## When to Use This Skill
Keywords.

## Domain Knowledge

### Clinical Concepts
Important clinical information.

### Medications
Common medications.
"""
        loader = SkillLoader()
        skill = loader.load_string(content)

        assert skill.is_v2_format()
        # In v2.0, "Domain Knowledge" section should be parsed into knowledge dict
        assert "Clinical Concepts" in skill.knowledge
        assert "Medications" in skill.knowledge
        assert "Important clinical information" in skill.knowledge["Clinical Concepts"]

    def test_example_requests_and_interpretations(self) -> None:
        """Test parsing 'Example Requests and Interpretations' section."""
        content = """# Test Skill

## For Claude
Test.

## Metadata
- **Type**: scenario-template
- **Version**: 2.0

## Purpose
Testing examples.

## When to Use This Skill
Keywords.

## Example Requests and Interpretations

### Example 1: Basic Request
**User says**: "Generate a patient"

**Claude interprets**:
- Default settings

### Example 2: Advanced Request
**User says**: "Generate severe case"

**Claude interprets**:
- Severity: high
"""
        loader = SkillLoader()
        skill = loader.load_string(content)

        assert skill.is_v2_format()
        # This should be captured in the examples list
        assert len(skill.examples) >= 2
        assert "Basic Request" in skill.examples[0]

    def test_related_skills_section(self) -> None:
        """Test parsing 'Related Skills' section."""
        content = """# Test Skill

## For Claude
Test.

## Metadata
- **Type**: scenario-template
- **Version**: 2.0

## Purpose
Testing.

## When to Use This Skill
Keywords.

## Related Skills

Complementary skills:
- **skills/domain/clinical.md** - Clinical knowledge
- **skills/formats/fhir.md** - FHIR formatting
"""
        loader = SkillLoader()
        skill = loader.load_string(content)

        assert skill.is_v2_format()
        assert "Related Skills" in skill.content
        assert "clinical.md" in skill.content["Related Skills"]
