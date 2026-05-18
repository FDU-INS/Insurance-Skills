"""Unified generation entry point for MemberSim.

Provides a simple, consistent API for generating health plan members.

Example:
    >>> from membersim.generation import generate
    >>> result = generate("commercial-ppo-healthy", count=100)
    >>> print(f"Generated {result.count} members")
"""

from __future__ import annotations

from typing import Any, overload

from membersim.generation.executor import (
    MemberExecutionResult,
    MemberProfileExecutor,
)
from membersim.generation.profiles import MemberProfileSpecification
from membersim.generation.templates import (
    MEMBER_PROFILE_TEMPLATES,
    get_template,
    list_templates,
)


@overload
def generate(
    profile: str,
    *,
    count: int | None = None,
    seed: int | None = None,
    dry_run: bool = False,
    **overrides: Any,
) -> MemberExecutionResult: ...


@overload
def generate(
    profile: MemberProfileSpecification,
    *,
    count: int | None = None,
    seed: int | None = None,
    dry_run: bool = False,
    **overrides: Any,
) -> MemberExecutionResult: ...


def generate(
    profile: str | MemberProfileSpecification,
    *,
    count: int | None = None,
    seed: int | None = None,
    dry_run: bool = False,
    **overrides: Any,
) -> MemberExecutionResult:
    """Generate health plan members from a profile specification.

    This is the primary entry point for member generation. It accepts either
    a template name (string) or a full MemberProfileSpecification.

    Args:
        profile: Template name (e.g., "commercial-ppo-healthy") or
                 MemberProfileSpecification instance
        count: Override the count from profile (optional)
        seed: Override seed for reproducibility (optional)
        dry_run: If True, generate a small sample only (default: False)
        **overrides: Additional profile field overrides

    Returns:
        MemberExecutionResult containing generated members, validation,
        and distribution summaries

    Examples:
        Basic usage with template:
        >>> result = generate("commercial-ppo-healthy")
        >>> print(f"Generated {result.count} members")

        With count override:
        >>> result = generate("medicare-advantage-diabetic", count=500)

        With reproducibility:
        >>> result = generate("medicaid-pediatric", count=100, seed=42)

        With custom profile:
        >>> spec = MemberProfileSpecification(
        ...     id="custom-profile",
        ...     name="Custom Profile",
        ... )
        >>> result = generate(spec, count=50)

    Raises:
        KeyError: If template name not found
        ValueError: If profile specification is invalid
    """
    # Resolve template if string
    if isinstance(profile, str):
        spec = get_template(profile)
    else:
        # Make a copy to avoid modifying original
        spec = MemberProfileSpecification.model_validate(profile.model_dump())

    # Apply overrides
    if overrides:
        spec_data = spec.model_dump()
        _apply_overrides(spec_data, overrides)
        spec = MemberProfileSpecification.model_validate(spec_data)

    # Create executor and run
    executor = MemberProfileExecutor(spec, seed=seed)
    return executor.execute(count_override=count, dry_run=dry_run)


def _apply_overrides(data: dict[str, Any], overrides: dict[str, Any]) -> None:
    """Apply nested overrides to a data dictionary.

    Supports dot notation for nested keys:
        demographics.age.mean=72

    Args:
        data: Dictionary to modify in place
        overrides: Overrides to apply
    """
    for key, value in overrides.items():
        if "." in key:
            # Nested key
            parts = key.split(".")
            current = data
            for part in parts[:-1]:
                if part not in current:
                    current[part] = {}
                current = current[part]
            current[parts[-1]] = value
        else:
            data[key] = value


def quick_sample(
    template: str = "commercial-family-mix",
    count: int = 10,
) -> MemberExecutionResult:
    """Generate a quick sample for testing or exploration.

    Convenience function for rapid prototyping.

    Args:
        template: Template name (default: "commercial-family-mix")
        count: Number of members (default: 10)

    Returns:
        MemberExecutionResult with sample members
    """
    return generate(template, count=count, seed=42)


__all__ = [
    "generate",
    "quick_sample",
    "get_template",
    "list_templates",
    "MEMBER_PROFILE_TEMPLATES",
    "MemberProfileSpecification",
    "MemberProfileExecutor",
    "MemberExecutionResult",
]
