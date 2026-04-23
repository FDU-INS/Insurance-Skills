"""Deductible and OOP accumulator tracking.

This module provides backward-compatible accumulator tracking for MemberSim.
It wraps the shared accumulator infrastructure from healthsim-core.

For new code, prefer using healthsim.benefits directly:
    >>> from healthsim.benefits import AccumulatorSet, create_medical_accumulators

The legacy Accumulator class is maintained for backward compatibility.
"""

from datetime import datetime
from decimal import Decimal

from healthsim.benefits import Accumulator as CoreAccumulator
from healthsim.benefits import (
    AccumulatorLevel,
    AccumulatorSet,
    AccumulatorType,
    BenefitType,
    NetworkTier,
    create_integrated_accumulators,
    create_medical_accumulators,
    create_pharmacy_accumulators,
)
from pydantic import BaseModel, Field

__all__ = [
    # Legacy class (backward compatible)
    "Accumulator",
    # Core classes (re-exported)
    "CoreAccumulator",
    "AccumulatorSet",
    "AccumulatorType",
    "AccumulatorLevel",
    "NetworkTier",
    "BenefitType",
    # Factory functions
    "create_medical_accumulators",
    "create_pharmacy_accumulators",
    "create_integrated_accumulators",
]


class Accumulator(BaseModel):
    """Track deductible and OOP accumulations for a member.

    This is a backward-compatible wrapper around healthsim.benefits.AccumulatorSet.
    For new code, prefer using AccumulatorSet directly which provides:
    - Individual and family accumulator tracking
    - In-network and out-of-network separation
    - Pharmacy-specific accumulator support

    Example (legacy):
        >>> acc = Accumulator(
        ...     member_id="MEM-001",
        ...     plan_year=2024,
        ...     deductible_limit=Decimal("500"),
        ...     oop_limit=Decimal("3000"),
        ... )
        >>> new_acc = acc.apply_payment(Decimal("100"), Decimal("100"))

    Example (recommended):
        >>> from healthsim.benefits import create_medical_accumulators
        >>> acc_set = create_medical_accumulators(
        ...     member_id="MEM-001",
        ...     plan_year=2024,
        ...     deductible_individual=Decimal("500"),
        ...     deductible_family=Decimal("1500"),
        ...     oop_individual=Decimal("3000"),
        ...     oop_family=Decimal("6000"),
        ... )
        >>> new_set, applied = acc_set.apply_to_deductible(Decimal("100"))
    """

    member_id: str = Field(..., description="Member reference")
    plan_year: int = Field(..., description="Benefit year")

    # Deductible tracking
    deductible_applied: Decimal = Field(
        default=Decimal("0"), description="Amount applied to deductible"
    )
    deductible_limit: Decimal = Field(..., description="Deductible limit for this member")

    # OOP tracking
    oop_applied: Decimal = Field(
        default=Decimal("0"), description="Amount applied to OOP max"
    )
    oop_limit: Decimal = Field(..., description="OOP maximum for this member")

    last_updated: datetime = Field(default_factory=datetime.now)

    @property
    def deductible_remaining(self) -> Decimal:
        """Calculate remaining deductible."""
        return max(Decimal("0"), self.deductible_limit - self.deductible_applied)

    @property
    def deductible_met(self) -> bool:
        """Check if deductible has been met."""
        return self.deductible_applied >= self.deductible_limit

    @property
    def oop_remaining(self) -> Decimal:
        """Calculate remaining OOP."""
        return max(Decimal("0"), self.oop_limit - self.oop_applied)

    @property
    def oop_met(self) -> bool:
        """Check if OOP max has been reached."""
        return self.oop_applied >= self.oop_limit

    def apply_payment(
        self, deductible_amount: Decimal, oop_amount: Decimal
    ) -> "Accumulator":
        """Apply a payment to accumulators, returning new accumulator state.

        Args:
            deductible_amount: Amount to apply to deductible
            oop_amount: Amount to apply to OOP max

        Returns:
            New Accumulator instance with updated amounts
        """
        return Accumulator(
            member_id=self.member_id,
            plan_year=self.plan_year,
            deductible_applied=min(
                self.deductible_limit, self.deductible_applied + deductible_amount
            ),
            deductible_limit=self.deductible_limit,
            oop_applied=min(self.oop_limit, self.oop_applied + oop_amount),
            oop_limit=self.oop_limit,
            last_updated=datetime.now(),
        )

    def to_accumulator_set(self) -> AccumulatorSet:
        """Convert to an AccumulatorSet for use with core infrastructure.

        Returns:
            AccumulatorSet with individual in-network accumulators
        """
        return AccumulatorSet(
            member_id=self.member_id,
            plan_year=self.plan_year,
            deductible_individual_in=CoreAccumulator(
                accumulator_type=AccumulatorType.DEDUCTIBLE,
                level=AccumulatorLevel.INDIVIDUAL,
                network_tier=NetworkTier.IN_NETWORK,
                benefit_type=BenefitType.MEDICAL,
                limit=self.deductible_limit,
                applied=self.deductible_applied,
                plan_year=self.plan_year,
            ),
            oop_individual_in=CoreAccumulator(
                accumulator_type=AccumulatorType.OUT_OF_POCKET_MAX,
                level=AccumulatorLevel.INDIVIDUAL,
                network_tier=NetworkTier.IN_NETWORK,
                benefit_type=BenefitType.MEDICAL,
                limit=self.oop_limit,
                applied=self.oop_applied,
                plan_year=self.plan_year,
            ),
        )

    @classmethod
    def from_accumulator_set(cls, acc_set: AccumulatorSet) -> "Accumulator":
        """Create from an AccumulatorSet.

        Uses individual in-network accumulators.

        Args:
            acc_set: AccumulatorSet to convert from

        Returns:
            Accumulator instance
        """
        ded = acc_set.deductible_individual_in
        oop = acc_set.oop_individual_in

        return cls(
            member_id=acc_set.member_id,
            plan_year=acc_set.plan_year,
            deductible_applied=ded.applied if ded else Decimal("0"),
            deductible_limit=ded.limit if ded else Decimal("0"),
            oop_applied=oop.applied if oop else Decimal("0"),
            oop_limit=oop.limit if oop else Decimal("0"),
        )
