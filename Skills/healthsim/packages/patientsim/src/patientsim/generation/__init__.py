"""Generation framework for PatientSim.

This module provides a complete generation framework for clinical patients,
built on healthsim-core infrastructure with patient-specific extensions.

Quick Start:
    >>> from patientsim.generation import generate
    >>> result = generate("diabetic-senior", count=100)
    >>> print(f"Generated {result.count} patients")

    >>> # With reproducibility
    >>> result = generate("oncology", count=500, seed=42)

    >>> # List available templates
    >>> from patientsim.generation import list_templates
    >>> templates = list_templates()

Components:
    - generate(): Unified entry point for patient generation
    - PatientProfileSpecification: Patient-specific profile schema
    - PatientProfileExecutor: Profile executor for patients
    - PATIENT_PROFILE_TEMPLATES: Pre-built profile templates
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
from patientsim.generation.profiles import (
    EncounterSpec,
    FacilitySpec,
    PatientClinicalSpec,
    PatientConditionSpec,
    PatientDemographicsSpec,
    PatientDistributionSpec,
    PatientGenerationSpec,
    PatientProfileSpecification,
)

# Executor
from patientsim.generation.executor import (
    GeneratedPatient,
    PatientExecutionResult,
    PatientProfileExecutor,
)

# Templates
from patientsim.generation.templates import (
    PATIENT_PROFILE_TEMPLATES,
    get_template,
    list_templates,
)

# Unified generation function
from patientsim.generation.generate import (
    generate,
    quick_sample,
)

__all__ = [
    # Primary API
    "generate",
    "quick_sample",
    # Profile specification
    "PatientProfileSpecification",
    "PatientDemographicsSpec",
    "PatientClinicalSpec",
    "PatientGenerationSpec",
    "PatientConditionSpec",
    "PatientDistributionSpec",
    "EncounterSpec",
    "FacilitySpec",
    # Executor
    "PatientProfileExecutor",
    "PatientExecutionResult",
    "GeneratedPatient",
    # Templates
    "PATIENT_PROFILE_TEMPLATES",
    "get_template",
    "list_templates",
    # Core re-exports
    "WeightedChoice",
    "UniformDistribution",
    "NormalDistribution",
    "AgeDistribution",
    "SeedManager",
]
