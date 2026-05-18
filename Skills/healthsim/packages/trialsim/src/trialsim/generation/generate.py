"""Unified generation interface for TrialSim.

Provides a simple, consistent API for generating clinical trial subjects.
"""

from __future__ import annotations

from typing import Any

from trialsim.generation.executor import (
    TrialSimExecutionResult,
    TrialSimProfileExecutor,
)
from trialsim.generation.profiles import TrialSimProfileSpecification
from trialsim.generation.templates import (
    TRIALSIM_PROFILE_TEMPLATES,
    get_template,
    list_templates,
)


def generate(
    profile: str | TrialSimProfileSpecification | dict[str, Any],
    count: int | None = None,
    seed: int | None = None,
    **overrides: Any,
) -> TrialSimExecutionResult:
    """Generate clinical trial subjects from a profile specification.

    This is the primary entry point for generating trial data. It accepts
    either a template name, a profile specification object, or a dictionary.

    Args:
        profile: Template name (e.g., "phase3-oncology-trial"),
                TrialSimProfileSpecification, or dict
        count: Override the number of subjects to generate
        seed: Random seed for reproducibility
        **overrides: Additional overrides to apply to the profile

    Returns:
        TrialSimExecutionResult containing generated subjects and sites

    Examples:
        >>> # From template name
        >>> result = generate("phase3-oncology-trial", count=100)
        >>> print(f"Generated {result.count} subjects")

        >>> # With custom seed for reproducibility
        >>> result = generate("phase2-diabetes-trial", count=200, seed=42)

        >>> # From dict specification
        >>> result = generate({
        ...     "id": "custom-trial",
        ...     "name": "Custom Trial",
        ...     "protocol": {"phase": "Phase 2", "therapeutic_area": "Neurology"},
        ...     "generation": {"count": 50},
        ... })

        >>> # With overrides
        >>> result = generate(
        ...     "phase3-oncology-trial",
        ...     count=500,
        ...     arm_distribution={"weights": {"treatment": 0.75, "placebo": 0.25}},
        ... )
    """
    # Resolve profile specification
    if isinstance(profile, str):
        # Template name
        spec = get_template(profile, **overrides)
    elif isinstance(profile, dict):
        # Dictionary specification
        merged = {**profile, **overrides}
        spec = TrialSimProfileSpecification.model_validate(merged)
    else:
        # Already a specification
        if overrides:
            data = profile.model_dump()
            for key, value in overrides.items():
                if isinstance(value, dict) and key in data and isinstance(data[key], dict):
                    data[key].update(value)
                else:
                    data[key] = value
            spec = TrialSimProfileSpecification.model_validate(data)
        else:
            spec = profile

    # Apply count/seed overrides
    if count is not None:
        spec.generation.count = count
    if seed is not None:
        spec.generation.seed = seed

    # Execute
    executor = TrialSimProfileExecutor(spec)
    return executor.execute()


def quick_sample(
    template: str = "phase3-oncology-trial",
    count: int = 10,
    seed: int = 42,
) -> TrialSimExecutionResult:
    """Quickly generate a small sample of trial subjects.

    Convenience function for testing and exploration.

    Args:
        template: Template name to use
        count: Number of subjects to generate
        seed: Random seed for reproducibility

    Returns:
        TrialSimExecutionResult with generated subjects

    Example:
        >>> sample = quick_sample()
        >>> for subject in sample.subjects[:3]:
        ...     print(f"{subject.subject_id}: {subject.arm}")
    """
    return generate(template, count=count, seed=seed)


def from_template(
    template_name: str,
    **overrides: Any,
) -> TrialSimProfileSpecification:
    """Create a profile specification from a template with overrides.

    Use this when you want to customize a template before execution.

    Args:
        template_name: Name of the template
        **overrides: Field overrides to apply

    Returns:
        TrialSimProfileSpecification ready for execution

    Example:
        >>> spec = from_template(
        ...     "phase3-oncology-trial",
        ...     protocol={"indication": "Breast Cancer"},
        ...     generation={"count": 300},
        ... )
        >>> executor = TrialSimProfileExecutor(spec)
        >>> result = executor.execute()
    """
    return get_template(template_name, **overrides)


def generate_with_sites(
    profile: str | TrialSimProfileSpecification | dict[str, Any],
    num_sites: int,
    subjects_per_site: int,
    seed: int | None = None,
    **overrides: Any,
) -> TrialSimExecutionResult:
    """Generate subjects with explicit site configuration.

    Convenience function for controlling site distribution.

    Args:
        profile: Template name, specification, or dict
        num_sites: Number of trial sites
        subjects_per_site: Target subjects per site
        seed: Random seed for reproducibility
        **overrides: Additional overrides

    Returns:
        TrialSimExecutionResult with generated subjects and sites

    Example:
        >>> result = generate_with_sites(
        ...     "phase2-diabetes-trial",
        ...     num_sites=10,
        ...     subjects_per_site=20,
        ... )
        >>> print(f"Generated {result.count} subjects across {len(result.sites)} sites")
    """
    total_count = num_sites * subjects_per_site
    
    site_overrides = {
        "sites": {
            "num_sites": num_sites,
            "subjects_per_site": {
                "type": "normal",
                "mean": float(subjects_per_site),
                "std_dev": subjects_per_site * 0.2,
                "min": max(1, subjects_per_site - 5),
                "max": subjects_per_site + 10,
            },
        },
        **overrides,
    }
    
    return generate(profile, count=total_count, seed=seed, **site_overrides)


__all__ = [
    "generate",
    "quick_sample",
    "from_template",
    "generate_with_sites",
    "list_templates",
    "get_template",
]
