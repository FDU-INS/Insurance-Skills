"""Unified generation entry point for HealthSim.

This module provides a single entry point for generating synthetic
healthcare data across all HealthSim products.

Example:
    >>> import healthsim
    >>> 
    >>> # Generate members
    >>> members = healthsim.generate("members", count=100, seed=42)
    >>> 
    >>> # Generate patients with a journey
    >>> patients = healthsim.generate(
    ...     "patients",
    ...     template="diabetic-senior",
    ...     journey="diabetic-first-year",
    ...     count=50,
    ... )
    >>> 
    >>> # Quick sample
    >>> sample = healthsim.quick_sample("members", 10)
"""

from __future__ import annotations

from datetime import date
from typing import Any, TYPE_CHECKING

from healthsim.generation import (
    ProfileSpecification,
    ProfileExecutor,
    ExecutionResult,
    orchestrate,
    OrchestratorResult,
)

if TYPE_CHECKING:
    from healthsim.generation import JourneySpecification


# =============================================================================
# Product Registry
# =============================================================================

_PRODUCT_ALIASES = {
    # MemberSim
    "member": "membersim",
    "members": "membersim",
    "membersim": "membersim",
    # PatientSim
    "patient": "patientsim",
    "patients": "patientsim",
    "patientsim": "patientsim",
    # RxMemberSim
    "rx": "rxmembersim",
    "rxmember": "rxmembersim",
    "rxmembersim": "rxmembersim",
    "pharmacy": "rxmembersim",
    # TrialSim
    "trial": "trialsim",
    "trials": "trialsim",
    "trialsim": "trialsim",
    "subject": "trialsim",
    "subjects": "trialsim",
}


def _resolve_product(product: str) -> str:
    """Resolve product alias to canonical name."""
    normalized = product.lower().replace("-", "").replace("_", "")
    if normalized not in _PRODUCT_ALIASES:
        valid = sorted(set(_PRODUCT_ALIASES.values()))
        raise ValueError(f"Unknown product '{product}'. Valid: {valid}")
    return _PRODUCT_ALIASES[normalized]


def _get_product_generator(product: str):
    """Get product-specific generator."""
    canonical = _resolve_product(product)
    
    if canonical == "membersim":
        from membersim.generation import generate as member_generate
        return member_generate
    elif canonical == "patientsim":
        from patientsim.generation import generate as patient_generate
        return patient_generate
    elif canonical == "rxmembersim":
        from rxmembersim.generation import generate as rx_generate
        return rx_generate
    elif canonical == "trialsim":
        from trialsim.generation import generate as trial_generate
        return trial_generate
    
    raise ValueError(f"No generator for product: {canonical}")


# =============================================================================
# Unified Generate Function
# =============================================================================

def generate(
    product: str,
    template: str | None = None,
    profile: ProfileSpecification | dict | None = None,
    journey: str | "JourneySpecification" | None = None,
    count: int | None = None,
    seed: int | None = None,
    start_date: date | None = None,
    **kwargs: Any,
) -> ExecutionResult | OrchestratorResult:
    """Generate synthetic healthcare data.
    
    This is the unified entry point for all HealthSim data generation.
    It routes to the appropriate product-specific generator based on
    the product parameter.
    
    Args:
        product: Product to use ("members", "patients", "rx", "trials")
        template: Template name for the product
        profile: Custom ProfileSpecification (overrides template)
        journey: Optional journey to apply to generated entities
        count: Number of entities to generate
        seed: Random seed for reproducibility
        start_date: Start date for journeys
        **kwargs: Product-specific parameters
        
    Returns:
        ExecutionResult or OrchestratorResult depending on journey
        
    Examples:
        >>> # Generate members using default template
        >>> result = generate("members", count=100)
        
        >>> # Generate patients with specific template
        >>> result = generate("patients", template="diabetic-senior", count=50)
        
        >>> # Generate with journey
        >>> result = generate(
        ...     "patients",
        ...     template="chronic-condition",
        ...     journey="diabetic-first-year",
        ...     count=100,
        ... )
        
        >>> # Generate trial subjects
        >>> result = generate("trials", template="phase3-oncology-trial", count=200)
    """
    # If journey is provided, use orchestrator
    if journey is not None:
        # Build profile from template or spec
        if profile is not None:
            profile_spec = profile if isinstance(profile, ProfileSpecification) else ProfileSpecification.model_validate(profile)
        elif template is not None:
            # Get template from product
            gen_func = _get_product_generator(product)
            # Call with template to get result, extract spec concept
            profile_spec = ProfileSpecification(
                id=template,
                name=template,
                generation={"count": count or 100, "products": [_resolve_product(product)]},
            )
        else:
            profile_spec = ProfileSpecification(
                id="default",
                name="Default Profile",
                generation={"count": count or 100, "products": [_resolve_product(product)]},
            )
        
        return orchestrate(
            profile=profile_spec,
            journey=journey,
            count=count,
            seed=seed,
            start_date=start_date,
        )
    
    # Otherwise use product-specific generator
    gen_func = _get_product_generator(product)
    
    # Build arguments
    gen_args: dict[str, Any] = {}
    if template:
        gen_args["template"] = template
    if count:
        gen_args["count"] = count
    if seed:
        gen_args["seed"] = seed
    gen_args.update(kwargs)
    
    # If we have a template string, pass it; otherwise pass profile
    if template:
        return gen_func(template, **{k: v for k, v in gen_args.items() if k != "template"})
    elif profile:
        return gen_func(profile, **{k: v for k, v in gen_args.items()})
    else:
        # Use product's default
        return gen_func(count=count or 100, seed=seed or 42)


def quick_sample(
    product: str,
    count: int = 10,
    seed: int = 42,
) -> ExecutionResult:
    """Generate a quick sample of data for testing.
    
    Args:
        product: Product to sample from
        count: Number of entities (default 10)
        seed: Random seed (default 42)
        
    Returns:
        ExecutionResult with sample data
        
    Example:
        >>> sample = quick_sample("members", 5)
        >>> print(f"Got {sample.count} members")
    """
    canonical = _resolve_product(product)
    
    # Use product's quick_sample if available, otherwise use first template
    if canonical == "membersim":
        from membersim.generation import quick_sample as member_quick_sample
        return member_quick_sample(count=count)
    elif canonical == "patientsim":
        from patientsim.generation import quick_sample as patient_quick_sample
        return patient_quick_sample(count=count)
    elif canonical == "rxmembersim":
        from rxmembersim.generation import quick_sample as rx_quick_sample
        return rx_quick_sample(count=count)
    elif canonical == "trialsim":
        from trialsim.generation import quick_sample as trial_quick_sample
        return trial_quick_sample(count=count)
    
    raise ValueError(f"No quick_sample for product: {canonical}")


def list_products() -> list[str]:
    """List available products.
    
    Returns:
        List of canonical product names
    """
    return sorted(set(_PRODUCT_ALIASES.values()))


def list_templates(product: str) -> list[str]:
    """List templates available for a product.
    
    Args:
        product: Product name
        
    Returns:
        List of template names
    """
    canonical = _resolve_product(product)
    
    if canonical == "membersim":
        from membersim.generation.templates import MEMBER_PROFILE_TEMPLATES
        return list(MEMBER_PROFILE_TEMPLATES.keys())
    elif canonical == "patientsim":
        from patientsim.generation.templates import PATIENT_PROFILE_TEMPLATES
        return list(PATIENT_PROFILE_TEMPLATES.keys())
    elif canonical == "rxmembersim":
        from rxmembersim.generation.templates import RXMEMBER_PROFILE_TEMPLATES
        return list(RXMEMBER_PROFILE_TEMPLATES.keys())
    elif canonical == "trialsim":
        from trialsim.generation.templates import TRIALSIM_PROFILE_TEMPLATES
        return list(TRIALSIM_PROFILE_TEMPLATES.keys())
    
    return []


__all__ = [
    "generate",
    "quick_sample",
    "list_products",
    "list_templates",
]
