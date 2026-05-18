"""Unified generation interface for RxMemberSim.

Provides a simple entry point for generating pharmacy benefit members.

Quick Start:
    >>> from rxmembersim.generation import generate
    >>> result = generate("commercial-healthy", count=100)
    >>> print(f"Generated {result.count} pharmacy members")

    >>> # With reproducibility
    >>> result = generate("medicare-partd-polypharmacy", count=500, seed=42)

    >>> # Custom specification
    >>> result = generate({
    ...     "id": "custom-specialty",
    ...     "name": "Custom Specialty Members",
    ...     "coverage": {"coverage_type": "Commercial"},
    ...     "generation": {"count": 50, "include_specialty_rx": True}
    ... })
"""

from __future__ import annotations

from typing import Any

from rxmembersim.generation.executor import (
    GeneratedRxMember,
    RxMemberExecutionResult,
    RxMemberProfileExecutor,
)
from rxmembersim.generation.profiles import RxMemberProfileSpecification
from rxmembersim.generation.templates import (
    RXMEMBER_PROFILE_TEMPLATES,
    get_template,
)


def generate(
    profile: str | dict[str, Any] | RxMemberProfileSpecification,
    count: int | None = None,
    seed: int | None = None,
    **kwargs: Any,
) -> RxMemberExecutionResult:
    """Generate pharmacy benefit members from a profile specification.

    This is the primary entry point for generating RxMemberSim data.

    Args:
        profile: One of:
            - Template name (str): e.g., "commercial-healthy", "medicare-partd-polypharmacy"
            - Dictionary: Inline profile specification
            - RxMemberProfileSpecification: Pre-built specification object
        count: Number of members to generate (overrides profile setting)
        seed: Random seed for reproducibility (overrides profile setting)
        **kwargs: Additional overrides applied to profile specification

    Returns:
        RxMemberExecutionResult containing generated members and metadata

    Examples:
        >>> # Using a template
        >>> result = generate("commercial-healthy", count=100)

        >>> # Using a template with seed
        >>> result = generate("medicare-partd-polypharmacy", count=500, seed=42)

        >>> # Using inline specification
        >>> result = generate({
        ...     "id": "custom",
        ...     "name": "Custom Profile",
        ...     "demographics": {"age": {"type": "normal", "mean": 45, "std_dev": 10}},
        ...     "coverage": {"coverage_type": "Commercial"},
        ...     "generation": {"count": 100}
        ... })

        >>> # Accessing results
        >>> for member in result.rx_members[:5]:
        ...     print(f"{member.first_name} {member.last_name}: {member.adherence_score}")
    """
    # Resolve profile specification
    if isinstance(profile, str):
        spec = get_template(profile)
    elif isinstance(profile, dict):
        spec = RxMemberProfileSpecification.model_validate(profile)
    else:
        spec = profile

    # Apply overrides
    if count is not None:
        spec.generation.count = count

    if seed is not None:
        spec.generation.seed = seed

    # Apply additional kwargs to appropriate places
    for key, value in kwargs.items():
        if hasattr(spec.generation, key):
            setattr(spec.generation, key, value)
        elif hasattr(spec.coverage, key):
            setattr(spec.coverage, key, value)

    # Execute
    executor = RxMemberProfileExecutor(spec)
    return executor.execute()


def quick_sample(
    template: str = "commercial-healthy",
    count: int = 10,
    seed: int = 42,
) -> list[GeneratedRxMember]:
    """Generate a quick sample of pharmacy members.

    Convenience function for testing and exploration.

    Args:
        template: Template name (default: "commercial-healthy")
        count: Number of members (default: 10)
        seed: Random seed (default: 42)

    Returns:
        List of generated pharmacy members
    """
    result = generate(template, count=count, seed=seed)
    return result.rx_members


def from_template(
    template_id: str,
    overrides: dict[str, Any] | None = None,
) -> RxMemberProfileSpecification:
    """Create a profile specification from a template with optional overrides.

    Args:
        template_id: Template identifier
        overrides: Dictionary of values to override in the template

    Returns:
        New RxMemberProfileSpecification based on template
    """
    spec = get_template(template_id)

    if overrides:
        # Deep merge overrides
        spec_dict = spec.model_dump()
        _deep_merge(spec_dict, overrides)
        spec = RxMemberProfileSpecification.model_validate(spec_dict)

    return spec


def _deep_merge(base: dict, override: dict) -> None:
    """Deep merge override dict into base dict (in place)."""
    for key, value in override.items():
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            _deep_merge(base[key], value)
        else:
            base[key] = value
