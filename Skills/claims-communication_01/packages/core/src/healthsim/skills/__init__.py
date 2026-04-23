"""Skills framework for HealthSim.

Provides schema, loading, and composition for skill definitions
that guide Claude in generating domain-specific data.
"""

from healthsim.skills.composer import SkillComposer, SkillCompositionError
from healthsim.skills.loader import SkillLoader, SkillParseError
from healthsim.skills.schema import (
    ParameterType,
    Skill,
    SkillMetadata,
    SkillParameter,
    SkillType,
    SkillVariation,
)

__all__ = [
    # Schema
    "SkillType",
    "ParameterType",
    "SkillMetadata",
    "SkillParameter",
    "SkillVariation",
    "Skill",
    # Loader
    "SkillLoader",
    "SkillParseError",
    # Composer
    "SkillComposer",
    "SkillCompositionError",
]
