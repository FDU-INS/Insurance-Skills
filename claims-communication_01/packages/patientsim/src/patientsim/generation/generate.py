"""Unified generation entry point for PatientSim.

This module provides the primary API for generating synthetic patient data.
It offers a simple interface that handles profile resolution, execution,
and optional state persistence.

Example:
    >>> from patientsim.generation import generate
    >>> 
    >>> # Generate from a template
    >>> result = generate("diabetic-senior", count=100)
    >>> print(f"Generated {result.count} patients")
    >>> 
    >>> # Generate with custom spec
    >>> from patientsim.generation import PatientProfileSpecification
    >>> spec = PatientProfileSpecification(id="custom", ...)
    >>> result = generate(spec)
    >>> 
    >>> # Quick sample for testing
    >>> patients = quick_sample(5, template="healthy-adult")
"""

from typing import Any, overload

from patientsim.generation.executor import (
    GeneratedPatient,
    PatientExecutionResult,
    PatientProfileExecutor,
)
from patientsim.generation.profiles import (
    PatientDemographicsSpec,
    PatientProfileSpecification,
)
from patientsim.generation.templates import (
    PATIENT_PROFILE_TEMPLATES,
    get_template,
)


@overload
def generate(
    profile: str,
    *,
    count: int | None = None,
    seed: int | None = None,
    persist: bool = False,
    **overrides: Any,
) -> PatientExecutionResult: ...


@overload
def generate(
    profile: PatientProfileSpecification,
    *,
    count: int | None = None,
    seed: int | None = None,
    persist: bool = False,
    **overrides: Any,
) -> PatientExecutionResult: ...


def generate(
    profile: str | PatientProfileSpecification,
    *,
    count: int | None = None,
    seed: int | None = None,
    persist: bool = False,
    **overrides: Any,
) -> PatientExecutionResult:
    """Generate synthetic patient data.
    
    This is the primary entry point for patient generation. It accepts either
    a template name or a full specification object.
    
    Args:
        profile: Either a template name (e.g., "diabetic-senior") or a
            PatientProfileSpecification object
        count: Override the number of patients to generate
        seed: Random seed for reproducibility
        persist: Whether to persist results to state management
        **overrides: Additional overrides to apply to the profile
        
    Returns:
        PatientExecutionResult containing generated patients
        
    Raises:
        KeyError: If template name not found
        ValueError: If profile specification is invalid
        
    Example:
        >>> # From template
        >>> result = generate("diabetic-senior", count=500, seed=42)
        >>> 
        >>> # From custom spec
        >>> spec = PatientProfileSpecification(
        ...     id="my-cohort",
        ...     demographics=PatientDemographicsSpec(count=100)
        ... )
        >>> result = generate(spec, seed=42)
    """
    # Resolve profile
    if isinstance(profile, str):
        spec = get_template(profile)
    else:
        spec = profile.model_copy(deep=True)
    
    # Apply count override
    if count is not None:
        spec.generation.count = count
    
    # Apply additional overrides
    _apply_overrides(spec, overrides)
    
    # Execute
    executor = PatientProfileExecutor(spec, seed=seed)
    result = executor.execute()
    
    # Persist if requested
    if persist:
        _persist_result(result)
    
    return result


def quick_sample(
    count: int = 10,
    template: str = "healthy-adult",
    seed: int | None = None,
) -> list[GeneratedPatient]:
    """Generate a quick sample of patients for testing.
    
    This is a convenience function for rapid prototyping and testing.
    It returns just the generated patients without the full result wrapper.
    
    Args:
        count: Number of patients to generate (default: 10)
        template: Template to use (default: "healthy-adult")
        seed: Random seed for reproducibility
        
    Returns:
        List of GeneratedPatient objects
        
    Example:
        >>> patients = quick_sample(5)
        >>> for p in patients:
        ...     print(f"{p.patient.name}: {p.mrn}")
    """
    result = generate(template, count=count, seed=seed)
    return result.patients


def _apply_overrides(
    spec: PatientProfileSpecification,
    overrides: dict[str, Any],
) -> None:
    """Apply override values to a specification.
    
    Args:
        spec: Specification to modify in place
        overrides: Override values to apply
    """
    for key, value in overrides.items():
        if hasattr(spec.demographics, key):
            setattr(spec.demographics, key, value)
        elif spec.clinical and hasattr(spec.clinical, key):
            setattr(spec.clinical, key, value)
        elif hasattr(spec.generation, key):
            setattr(spec.generation, key, value)


def _persist_result(result: PatientExecutionResult) -> None:
    """Persist execution result to state management.
    
    Args:
        result: Result to persist
    """
    # TODO: Implement state persistence integration
    # This will be completed in Phase 5
    pass


__all__ = [
    "generate",
    "quick_sample",
]
