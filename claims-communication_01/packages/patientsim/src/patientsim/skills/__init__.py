"""Skills-based configuration system for PatientSim.

This module provides the Skills abstraction - Markdown-based configuration files
that define reusable patient generation scenarios, domain knowledge, and validation rules.
"""

from patientsim.skills.composer import SkillComposer, SkillCompositionError
from patientsim.skills.loader import SkillLoader, SkillParseError
from patientsim.skills.schema import (
    GenerationRules,
    ParameterType,
    Skill,
    SkillMetadata,
    SkillParameter,
    SkillType,
    SkillVariation,
)

__all__ = [
    # Schema
    "Skill",
    "SkillMetadata",
    "SkillParameter",
    "SkillType",
    "ParameterType",
    "GenerationRules",
    "SkillVariation",
    # Loader
    "SkillLoader",
    "SkillParseError",
    # Composer
    "SkillComposer",
    "SkillCompositionError",
]
