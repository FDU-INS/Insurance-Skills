"""Generation framework for MemberSim.

This module provides a complete generation framework for health plan members,
built on healthsim-core infrastructure with member-specific extensions.

Quick Start:
    >>> from membersim.generation import generate
    >>> result = generate("commercial-ppo-healthy", count=100)
    >>> print(f"Generated {result.count} members")

    >>> # With reproducibility
    >>> result = generate("medicare-advantage-diabetic", count=500, seed=42)

    >>> # List available templates
    >>> from membersim.generation import list_templates
    >>> templates = list_templates()

Components:
    - generate(): Unified entry point for member generation
    - MemberProfileSpecification: Member-specific profile schema
    - MemberProfileExecutor: Profile executor for members
    - MEMBER_PROFILE_TEMPLATES: Pre-built profile templates
    - MemberCohortGenerator: Legacy cohort-based generation
"""

# Core re-exports
from healthsim.generation import (
    AgeDistribution,
    NormalDistribution,
    SeedManager,
    UniformDistribution,
    WeightedChoice,
)

# Profile specifications
from membersim.generation.profiles import (
    EnrollmentSpec,
    MemberCoverageSpec,
    MemberGenerationSpec,
    MemberProfileSpecification,
    PlanDistributionSpec,
    SubscriberRelationshipSpec,
)

# Executor
from membersim.generation.executor import (
    GeneratedMember,
    MemberExecutionResult,
    MemberProfileExecutor,
)

# Templates
from membersim.generation.templates import (
    MEMBER_PROFILE_TEMPLATES,
    get_template,
    list_templates,
)

# Unified generation function
from membersim.generation.generate import (
    generate,
    quick_sample,
)

# Legacy cohort generation (backward compatibility)
from membersim.generation.cohort import (
    CohortConstraints,
    CohortGenerator,
    CohortProgress,
    MemberCohortConstraints,
    MemberCohortGenerator,
)

__all__ = [
    # Primary API
    "generate",
    "quick_sample",
    # Profile specification
    "MemberProfileSpecification",
    "MemberCoverageSpec",
    "MemberGenerationSpec",
    "PlanDistributionSpec",
    "SubscriberRelationshipSpec",
    "EnrollmentSpec",
    # Executor
    "MemberProfileExecutor",
    "MemberExecutionResult",
    "GeneratedMember",
    # Templates
    "MEMBER_PROFILE_TEMPLATES",
    "get_template",
    "list_templates",
    # Core re-exports
    "WeightedChoice",
    "UniformDistribution",
    "NormalDistribution",
    "AgeDistribution",
    "SeedManager",
    # Legacy cohort (backward compat)
    "MemberCohortConstraints",
    "MemberCohortGenerator",
    "CohortConstraints",
    "CohortProgress",
    "CohortGenerator",
]
