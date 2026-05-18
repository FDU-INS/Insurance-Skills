"""Pydantic models for Skills configuration files.

This module defines the schema for parsing and validating Skills files.
"""

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, field_validator


class SkillType(str, Enum):
    """Type of skill."""

    DOMAIN_KNOWLEDGE = "domain-knowledge"
    SCENARIO_TEMPLATE = "scenario-template"
    FORMAT_SPEC = "format-spec"
    VALIDATION_RULES = "validation-rules"


class ParameterType(str, Enum):
    """Type of skill parameter."""

    RANGE = "range"
    ENUM = "enum"
    BOOLEAN = "boolean"
    INTEGER = "integer"
    STRING = "string"


class SkillMetadata(BaseModel):
    """Metadata for a skill.

    Attributes:
        type: Type of skill
        version: Semantic version string
        author: Optional author or team name
        tags: List of categorization tags
        created: Optional creation date (ISO format)
        updated: Optional last update date (ISO format)
    """

    type: SkillType
    version: str
    author: str | None = None
    tags: list[str] = Field(default_factory=list)
    created: str | None = None
    updated: str | None = None

    @field_validator("version")
    @classmethod
    def validate_version(cls, v: str) -> str:
        """Validate semantic version format."""
        parts = v.split(".")
        if len(parts) < 2 or len(parts) > 3:
            raise ValueError(f"Version must be in format X.Y or X.Y.Z, got: {v}")
        for part in parts:
            if not part.isdigit():
                raise ValueError(f"Version parts must be numeric, got: {v}")
        return v


class SkillParameter(BaseModel):
    """A configurable parameter for a skill.

    Attributes:
        name: Parameter name (snake_case)
        type: Parameter type
        default: Default value
        description: Human-readable description
    """

    name: str
    type: ParameterType
    default: Any
    description: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate parameter name is a valid identifier."""
        if not v.replace("_", "").isalnum():
            raise ValueError(f"Parameter name must be alphanumeric with underscores: {v}")
        if v[0].isdigit():
            raise ValueError(f"Parameter name cannot start with a digit: {v}")
        return v

    def validate_value(self, value: Any) -> bool:
        """Validate a value matches this parameter's type.

        Args:
            value: Value to validate

        Returns:
            True if valid, False otherwise
        """
        if self.type == ParameterType.BOOLEAN:
            return isinstance(value, bool)
        elif self.type == ParameterType.INTEGER:
            return isinstance(value, int)
        elif self.type == ParameterType.STRING:
            return isinstance(value, str)
        elif self.type == ParameterType.RANGE:
            # Expect "min-max" format
            if isinstance(value, str):
                parts = value.split("-")
                if len(parts) == 2:
                    try:
                        min_val, max_val = float(parts[0]), float(parts[1])
                        return min_val <= max_val
                    except ValueError:
                        return False
            return False
        elif self.type == ParameterType.ENUM:
            # Value should be in description's allowed values
            # For now, just check it's a string
            return isinstance(value, str)
        return False


class GenerationRules(BaseModel):
    """Generation rules for a scenario template.

    This is a flexible container that holds parsed generation rules.
    The actual structure depends on what sections are present in the skill.

    Attributes:
        demographics: Demographic generation rules
        conditions: Diagnosis/condition rules
        vital_signs: Vital sign ranges
        laboratory: Lab test rules
        medications: Medication rules
        timeline: Event timeline
        raw_sections: All raw section content
    """

    demographics: dict[str, Any] = Field(default_factory=dict)
    conditions: dict[str, Any] = Field(default_factory=dict)
    vital_signs: dict[str, Any] = Field(default_factory=dict)
    laboratory: dict[str, Any] = Field(default_factory=dict)
    medications: list[str] = Field(default_factory=list)
    timeline: list[str] = Field(default_factory=list)
    raw_sections: dict[str, str] = Field(default_factory=dict)


class SkillVariation(BaseModel):
    """A named variation on a skill's base configuration.

    Attributes:
        name: Variation name
        description: What this variation changes
        overrides: Parameter overrides for this variation
    """

    name: str
    description: str
    overrides: dict[str, Any] = Field(default_factory=dict)


class Skill(BaseModel):
    """A complete skill definition.

    Attributes:
        name: Skill name (from H1 title)
        description: Brief description (first paragraph)
        metadata: Skill metadata
        purpose: Detailed purpose explanation
        parameters: Configurable parameters (for scenario-template)
        generation_rules: Generation rules (for scenario-template)
        knowledge: Domain knowledge sections (for domain-knowledge)
        variations: Named variations (for scenario-template)
        examples: Usage examples
        references: External references
        dependencies: Other skills this depends on
        raw_text: Original markdown text
        content: All parsed content sections
        for_claude: Optional v2.0 section - direct instructions to Claude (v2.0)
        when_to_use: Optional v2.0 section - intent recognition keywords (v2.0)
        generation_guidelines: Optional v2.0 section - how to apply knowledge (v2.0)
    """

    name: str
    description: str
    metadata: SkillMetadata
    purpose: str
    parameters: list[SkillParameter] = Field(default_factory=list)
    generation_rules: GenerationRules | None = None
    knowledge: dict[str, str] = Field(default_factory=dict)
    variations: list[SkillVariation] = Field(default_factory=list)
    examples: list[str] = Field(default_factory=list)
    references: list[str] = Field(default_factory=list)
    dependencies: list[str] = Field(default_factory=list)
    raw_text: str
    content: dict[str, Any] = Field(default_factory=dict)
    # v2.0 format fields
    for_claude: str | None = None
    when_to_use: str | None = None
    generation_guidelines: str | None = None

    def get_parameter(self, name: str) -> SkillParameter | None:
        """Get a parameter by name.

        Args:
            name: Parameter name

        Returns:
            SkillParameter if found, None otherwise
        """
        for param in self.parameters:
            if param.name == name:
                return param
        return None

    def get_parameter_default(self, name: str) -> Any:
        """Get a parameter's default value.

        Args:
            name: Parameter name

        Returns:
            Default value if parameter exists, None otherwise
        """
        param = self.get_parameter(name)
        return param.default if param else None

    def validate_parameters(self, values: dict[str, Any]) -> list[str]:
        """Validate a set of parameter values.

        Args:
            values: Parameter name -> value mapping

        Returns:
            List of error messages (empty if all valid)
        """
        errors = []

        # Check for unknown parameters
        known_params = {p.name for p in self.parameters}
        for name in values:
            if name not in known_params:
                errors.append(f"Unknown parameter: {name}")

        # Validate each provided value
        for param in self.parameters:
            if param.name in values:
                value = values[param.name]
                if not param.validate_value(value):
                    errors.append(
                        f"Invalid value for parameter '{param.name}': "
                        f"{value} (expected {param.type.value})"
                    )

        return errors

    def is_scenario_template(self) -> bool:
        """Check if this is a scenario template skill."""
        return self.metadata.type == SkillType.SCENARIO_TEMPLATE

    def is_domain_knowledge(self) -> bool:
        """Check if this is a domain knowledge skill."""
        return self.metadata.type == SkillType.DOMAIN_KNOWLEDGE

    def is_format_spec(self) -> bool:
        """Check if this is a format specification skill."""
        return self.metadata.type == SkillType.FORMAT_SPEC

    def is_validation_rules(self) -> bool:
        """Check if this is a validation rules skill."""
        return self.metadata.type == SkillType.VALIDATION_RULES

    def is_v2_format(self) -> bool:
        """Check if this skill uses the v2.0 format.

        v2.0 skills have "For Claude" and "When to Use This Skill" sections.

        Returns:
            True if v2.0 format, False if v1.0 format
        """
        return self.for_claude is not None and self.when_to_use is not None

    def get_format_version(self) -> str:
        """Get the skill format version.

        Returns:
            "2.0" if v2.0 format, "1.0" otherwise
        """
        return "2.0" if self.is_v2_format() else "1.0"
