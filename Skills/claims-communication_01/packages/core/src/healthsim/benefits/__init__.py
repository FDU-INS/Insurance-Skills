"""Benefit management infrastructure.

This module provides shared models and utilities for managing health plan
benefits across medical, pharmacy, dental, and vision domains.

Key Components:
    - Accumulators: Track deductibles, out-of-pocket maximums, and other
      benefit limits across plan years
    - Cost Sharing: Common copay, coinsurance, and deductible application logic

Example:
    >>> from healthsim.benefits import (
    ...     Accumulator,
    ...     AccumulatorSet,
    ...     AccumulatorType,
    ...     create_medical_accumulators,
    ... )
    >>> acc_set = create_medical_accumulators(
    ...     member_id="MEM-001",
    ...     plan_year=2024,
    ...     deductible_individual=Decimal("500"),
    ...     deductible_family=Decimal("1500"),
    ...     oop_individual=Decimal("3000"),
    ...     oop_family=Decimal("6000"),
    ... )
    >>> acc_set.is_deductible_met()
    False
"""

from healthsim.benefits.accumulators import (
    Accumulator,
    AccumulatorLevel,
    AccumulatorSet,
    AccumulatorType,
    BenefitType,
    NetworkTier,
    create_integrated_accumulators,
    create_medical_accumulators,
    create_pharmacy_accumulators,
)

__all__ = [
    # Core model
    "Accumulator",
    "AccumulatorSet",
    # Enums
    "AccumulatorType",
    "AccumulatorLevel",
    "NetworkTier",
    "BenefitType",
    # Factory functions
    "create_medical_accumulators",
    "create_pharmacy_accumulators",
    "create_integrated_accumulators",
]
