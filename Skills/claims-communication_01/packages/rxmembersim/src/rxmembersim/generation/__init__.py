"""Generation framework for RxMemberSim.

This module provides a complete generation framework for pharmacy benefit
members, built on healthsim-core infrastructure with pharmacy-specific extensions.

Quick Start:
    >>> from rxmembersim.generation import generate
    >>> result = generate("commercial-healthy", count=100)
    >>> print(f"Generated {result.count} pharmacy members")

    >>> # With reproducibility
    >>> result = generate("medicare-partd-polypharmacy", count=500, seed=42)

    >>> # List available templates
    >>> from rxmembersim.generation import list_templates
    >>> templates = list_templates()

Components:
    - generate(): Unified entry point for pharmacy member generation
    - RxMemberProfileSpecification: Pharmacy-specific profile schema
    - RxMemberProfileExecutor: Profile executor for pharmacy members
    - RXMEMBER_PROFILE_TEMPLATES: Pre-built profile templates
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
from rxmembersim.generation.profiles import (
    FormularyTierSpec,
    PharmacyPreferenceSpec,
    RxEnrollmentSpec,
    RxMemberCoverageSpec,
    RxMemberGenerationSpec,
    RxMemberProfileSpecification,
    TherapyPatternSpec,
)

# Executor
from rxmembersim.generation.executor import (
    GeneratedRxMember,
    RxMemberExecutionResult,
    RxMemberProfileExecutor,
)

# Templates
from rxmembersim.generation.templates import (
    RXMEMBER_PROFILE_TEMPLATES,
    get_template,
    list_templates,
)

# Unified generation function
from rxmembersim.generation.generate import (
    from_template,
    generate,
    quick_sample,
)

__all__ = [
    # Primary API
    "generate",
    "quick_sample",
    "from_template",
    # Profile specification
    "RxMemberProfileSpecification",
    "RxMemberCoverageSpec",
    "RxMemberGenerationSpec",
    "RxEnrollmentSpec",
    "FormularyTierSpec",
    "PharmacyPreferenceSpec",
    "TherapyPatternSpec",
    # Executor
    "RxMemberProfileExecutor",
    "RxMemberExecutionResult",
    "GeneratedRxMember",
    # Templates
    "RXMEMBER_PROFILE_TEMPLATES",
    "get_template",
    "list_templates",
    # Core re-exports
    "WeightedChoice",
    "UniformDistribution",
    "NormalDistribution",
    "AgeDistribution",
    "SeedManager",
]
