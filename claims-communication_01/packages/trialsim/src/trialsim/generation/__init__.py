"""Generation framework for TrialSim.

This module provides a complete generation framework for clinical trial
subjects, built on healthsim-core infrastructure with trial-specific extensions.

Quick Start:
    >>> from trialsim.generation import generate
    >>> result = generate("phase3-oncology-trial", count=100)
    >>> print(f"Generated {result.count} subjects ({result.enrolled_count} enrolled)")

    >>> # With reproducibility
    >>> result = generate("phase2-diabetes-trial", count=500, seed=42)

    >>> # List available templates
    >>> from trialsim.generation import list_templates
    >>> templates = list_templates()

Components:
    - generate(): Unified entry point for trial subject generation
    - TrialSimProfileSpecification: Trial-specific profile schema
    - TrialSimProfileExecutor: Profile executor for trial subjects
    - TRIALSIM_PROFILE_TEMPLATES: Pre-built profile templates
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
from trialsim.generation.profiles import (
    AdverseEventSpec,
    ArmDistributionSpec,
    EnrollmentSpec,
    ExposureComplianceSpec,
    ProtocolSpec,
    SiteSpec,
    TrialSimGenerationSpec,
    TrialSimProfileSpecification,
    VisitComplianceSpec,
)

# Executor
from trialsim.generation.executor import (
    GeneratedSite,
    GeneratedSubject,
    TrialSimExecutionResult,
    TrialSimProfileExecutor,
)

# Templates
from trialsim.generation.templates import (
    TRIALSIM_PROFILE_TEMPLATES,
    get_template,
    list_templates,
    template_info,
)

# Unified generation functions
from trialsim.generation.generate import (
    from_template,
    generate,
    generate_with_sites,
    quick_sample,
)

__all__ = [
    # Primary API
    "generate",
    "quick_sample",
    "from_template",
    "generate_with_sites",
    # Profile specification
    "TrialSimProfileSpecification",
    "ProtocolSpec",
    "ArmDistributionSpec",
    "EnrollmentSpec",
    "SiteSpec",
    "VisitComplianceSpec",
    "AdverseEventSpec",
    "ExposureComplianceSpec",
    "TrialSimGenerationSpec",
    # Executor
    "TrialSimProfileExecutor",
    "TrialSimExecutionResult",
    "GeneratedSubject",
    "GeneratedSite",
    # Templates
    "TRIALSIM_PROFILE_TEMPLATES",
    "get_template",
    "list_templates",
    "template_info",
    # Core re-exports
    "WeightedChoice",
    "UniformDistribution",
    "NormalDistribution",
    "AgeDistribution",
    "SeedManager",
]
