"""Benefit accumulator tracking.

This module provides shared accumulator models for tracking deductibles,
out-of-pocket maximums, and other benefit limits. It supports both medical
(X12) and pharmacy (NCPDP) use cases with a unified implementation.

Key Classes:
    - Accumulator: Single benefit accumulator with limit/applied tracking
    - AccumulatorSet: Collection of related accumulators for a member

Key Enums:
    - AccumulatorType: Type of accumulator (deductible, OOP, etc.)
    - AccumulatorLevel: Aggregation level (individual, family)
    - NetworkTier: Network tier for cost sharing
    - BenefitType: Benefit category (medical, pharmacy, combined)

Factory Functions:
    - create_medical_accumulators: Create standard medical benefit accumulators
    - create_pharmacy_accumulators: Create pharmacy benefit accumulators
    - create_integrated_accumulators: Create combined medical+Rx accumulators

Example:
    >>> from decimal import Decimal
    >>> from healthsim.benefits import Accumulator, AccumulatorType, AccumulatorLevel
    >>>
    >>> # Create a single accumulator
    >>> deductible = Accumulator(
    ...     accumulator_type=AccumulatorType.DEDUCTIBLE,
    ...     level=AccumulatorLevel.INDIVIDUAL,
    ...     limit=Decimal("500"),
    ...     plan_year=2024,
    ... )
    >>>
    >>> # Apply an amount
    >>> new_deductible, applied = deductible.apply(Decimal("150"))
    >>> print(f"Applied: ${applied}, Remaining: ${new_deductible.remaining}")
    Applied: $150, Remaining: $350
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, Field, computed_field


class AccumulatorType(str, Enum):
    """Type of benefit accumulator.

    Standard accumulator types used across medical and pharmacy benefits.

    Attributes:
        DEDUCTIBLE: Annual deductible amount
        OUT_OF_POCKET_MAX: Maximum out-of-pocket spending
        COPAY_MAX: Annual copay maximum (some plans cap total copays)
        COINSURANCE_MAX: Annual coinsurance maximum
        RX_DEDUCTIBLE: Separate pharmacy deductible (carved-out Rx)
        RX_OOP_MAX: Separate pharmacy out-of-pocket maximum
        SPECIALTY_OOP: Specialty drug out-of-pocket (often separate limit)
        LIFETIME_MAX: Lifetime maximum benefit (rare, mostly grandfathered)
    """

    DEDUCTIBLE = "deductible"
    OUT_OF_POCKET_MAX = "oop_max"
    COPAY_MAX = "copay_max"
    COINSURANCE_MAX = "coinsurance_max"
    RX_DEDUCTIBLE = "rx_deductible"
    RX_OOP_MAX = "rx_oop_max"
    SPECIALTY_OOP = "specialty_oop"
    LIFETIME_MAX = "lifetime_max"


class AccumulatorLevel(str, Enum):
    """Aggregation level for accumulator.

    Defines how the accumulator aggregates across family members.

    Attributes:
        INDIVIDUAL: Tracks single member's spending
        FAMILY: Tracks combined family spending
        CARDHOLDER: Pharmacy-specific, maps to NCPDP person_code=01
    """

    INDIVIDUAL = "individual"
    FAMILY = "family"
    CARDHOLDER = "cardholder"


class NetworkTier(str, Enum):
    """Network tier for cost sharing.

    Defines the provider/pharmacy network tier, which affects
    cost sharing levels.

    Attributes:
        IN_NETWORK: Standard in-network providers
        OUT_OF_NETWORK: Out-of-network providers
        TIER_1: Preferred/high-performance providers
        TIER_2: Standard in-network providers
        TIER_3: Out-of-network providers
        PREFERRED_PHARMACY: Preferred retail pharmacy
        STANDARD_PHARMACY: Standard retail pharmacy
        MAIL_ORDER: Mail-order pharmacy (typically 90-day)
        SPECIALTY_PHARMACY: Specialty pharmacy for complex medications
    """

    IN_NETWORK = "in_network"
    OUT_OF_NETWORK = "out_of_network"
    TIER_1 = "tier_1"
    TIER_2 = "tier_2"
    TIER_3 = "tier_3"
    PREFERRED_PHARMACY = "preferred_pharmacy"
    STANDARD_PHARMACY = "standard_pharmacy"
    MAIL_ORDER = "mail_order"
    SPECIALTY_PHARMACY = "specialty_pharmacy"


class BenefitType(str, Enum):
    """Type of benefit for categorizing accumulator application.

    Some plans have integrated accumulators (medical + Rx combined),
    while others track them separately.

    Attributes:
        MEDICAL: Medical/professional services only
        PHARMACY: Pharmacy benefits only
        DENTAL: Dental benefits
        VISION: Vision benefits
        BEHAVIORAL_HEALTH: Mental health and substance abuse
        COMBINED: Integrated medical + pharmacy
    """

    MEDICAL = "medical"
    PHARMACY = "pharmacy"
    DENTAL = "dental"
    VISION = "vision"
    BEHAVIORAL_HEALTH = "behavioral_health"
    COMBINED = "combined"


class Accumulator(BaseModel):
    """Single benefit accumulator.

    Tracks a single benefit limit such as deductible or out-of-pocket maximum.
    Immutable design - the apply() method returns a new instance.

    This is the core building block used by both medical (MemberSim) and
    pharmacy (RxMemberSim) products for tracking benefit accumulations.

    Attributes:
        accumulator_type: Type of accumulator (deductible, OOP, etc.)
        level: Aggregation level (individual or family)
        network_tier: Network tier this accumulator applies to
        benefit_type: Benefit category (medical, pharmacy, combined)
        limit: Maximum amount for this accumulator
        applied: Amount applied year-to-date
        plan_year: Benefit plan year
        last_updated: Date of last update

    Properties:
        remaining: Amount remaining until limit is reached
        met: Whether the limit has been reached
        percent_used: Percentage of limit used

    Example:
        >>> deductible = Accumulator(
        ...     accumulator_type=AccumulatorType.DEDUCTIBLE,
        ...     level=AccumulatorLevel.INDIVIDUAL,
        ...     limit=Decimal("500"),
        ...     plan_year=2024,
        ... )
        >>> new_ded, applied = deductible.apply(Decimal("150"))
        >>> print(f"Remaining: ${new_ded.remaining}")
        Remaining: $350
    """

    accumulator_type: AccumulatorType = Field(..., description="Type of accumulator")
    level: AccumulatorLevel = Field(
        default=AccumulatorLevel.INDIVIDUAL,
        description="Aggregation level",
    )
    network_tier: NetworkTier = Field(
        default=NetworkTier.IN_NETWORK,
        description="Network tier",
    )
    benefit_type: BenefitType = Field(
        default=BenefitType.COMBINED,
        description="Benefit category",
    )
    limit: Decimal = Field(..., description="Maximum amount for this accumulator")
    applied: Decimal = Field(
        default=Decimal("0"),
        description="Amount applied year-to-date",
    )
    plan_year: int = Field(..., description="Benefit plan year")
    last_updated: date = Field(
        default_factory=date.today,
        description="Date of last update",
    )

    @computed_field
    @property
    def remaining(self) -> Decimal:
        """Calculate remaining amount until limit is reached."""
        return max(Decimal("0"), self.limit - self.applied)

    @computed_field
    @property
    def met(self) -> bool:
        """Check if accumulator limit has been reached."""
        return self.applied >= self.limit

    @computed_field
    @property
    def percent_used(self) -> float:
        """Calculate percentage of limit used."""
        if self.limit == 0:
            return 100.0
        return float((self.applied / self.limit) * 100)

    def apply(self, amount: Decimal) -> tuple[Accumulator, Decimal]:
        """Apply an amount to this accumulator.

        Returns a new accumulator instance with the updated applied amount,
        along with the amount that was actually applied (may be less than
        requested if limit would be exceeded).

        Args:
            amount: Amount to apply

        Returns:
            Tuple of (new_accumulator, amount_actually_applied)

        Example:
            >>> acc = Accumulator(
            ...     accumulator_type=AccumulatorType.DEDUCTIBLE,
            ...     level=AccumulatorLevel.INDIVIDUAL,
            ...     limit=Decimal("100"),
            ...     applied=Decimal("80"),
            ...     plan_year=2024,
            ... )
            >>> new_acc, applied = acc.apply(Decimal("50"))
            >>> print(f"Applied: ${applied}, Met: {new_acc.met}")
            Applied: $20, Met: True
        """
        applicable = min(amount, self.remaining)
        new_acc = self.model_copy(
            update={
                "applied": self.applied + applicable,
                "last_updated": date.today(),
            }
        )
        return new_acc, applicable

    def reset(self, new_plan_year: int | None = None) -> Accumulator:
        """Reset accumulator for new plan year.

        Args:
            new_plan_year: New plan year (defaults to current year + 1)

        Returns:
            New accumulator with applied amount reset to zero
        """
        return self.model_copy(
            update={
                "applied": Decimal("0"),
                "plan_year": new_plan_year or (self.plan_year + 1),
                "last_updated": date.today(),
            }
        )


class AccumulatorSet(BaseModel):
    """Collection of related accumulators for a member.

    Manages a set of accumulators and handles coordination between
    individual and family accumulators, and between different network tiers.

    This class provides convenience methods for applying amounts to
    deductibles and out-of-pocket accumulators while properly updating
    both individual and family-level tracking.

    Attributes:
        member_id: Member identifier
        plan_year: Benefit plan year
        deductible_individual_in: Individual in-network deductible
        deductible_individual_out: Individual out-of-network deductible
        deductible_family_in: Family in-network deductible
        deductible_family_out: Family out-of-network deductible
        oop_individual_in: Individual in-network OOP max
        oop_individual_out: Individual out-of-network OOP max
        oop_family_in: Family in-network OOP max
        oop_family_out: Family out-of-network OOP max
        rx_deductible: Pharmacy deductible (if separate from medical)
        rx_oop: Pharmacy OOP max (if separate from medical)
        specialty_oop: Specialty drug OOP (if separate limit)

    Example:
        >>> acc_set = create_medical_accumulators(
        ...     member_id="MEM-001",
        ...     plan_year=2024,
        ...     deductible_individual=Decimal("500"),
        ...     deductible_family=Decimal("1500"),
        ...     oop_individual=Decimal("3000"),
        ...     oop_family=Decimal("6000"),
        ... )
        >>> acc_set, applied = acc_set.apply_to_deductible(Decimal("200"))
        >>> print(f"Applied: ${applied}")
        Applied: $200
    """

    member_id: str = Field(..., description="Member identifier")
    plan_year: int = Field(..., description="Benefit plan year")

    # Standard medical accumulators
    deductible_individual_in: Accumulator | None = Field(
        default=None, description="Individual in-network deductible"
    )
    deductible_individual_out: Accumulator | None = Field(
        default=None, description="Individual out-of-network deductible"
    )
    deductible_family_in: Accumulator | None = Field(
        default=None, description="Family in-network deductible"
    )
    deductible_family_out: Accumulator | None = Field(
        default=None, description="Family out-of-network deductible"
    )

    oop_individual_in: Accumulator | None = Field(
        default=None, description="Individual in-network OOP max"
    )
    oop_individual_out: Accumulator | None = Field(
        default=None, description="Individual out-of-network OOP max"
    )
    oop_family_in: Accumulator | None = Field(default=None, description="Family in-network OOP max")
    oop_family_out: Accumulator | None = Field(
        default=None, description="Family out-of-network OOP max"
    )

    # Pharmacy-specific accumulators (optional, for carved-out Rx)
    rx_deductible: Accumulator | None = Field(
        default=None, description="Pharmacy deductible (if separate)"
    )
    rx_oop: Accumulator | None = Field(default=None, description="Pharmacy OOP max (if separate)")
    specialty_oop: Accumulator | None = Field(
        default=None, description="Specialty drug OOP (if separate limit)"
    )

    def _is_in_network(self, network: NetworkTier) -> bool:
        """Check if network tier is considered in-network."""
        return network in (
            NetworkTier.IN_NETWORK,
            NetworkTier.TIER_1,
            NetworkTier.TIER_2,
            NetworkTier.PREFERRED_PHARMACY,
            NetworkTier.MAIL_ORDER,
        )

    def apply_to_deductible(
        self,
        amount: Decimal,
        network: NetworkTier = NetworkTier.IN_NETWORK,
        benefit_type: BenefitType = BenefitType.COMBINED,
    ) -> tuple[AccumulatorSet, Decimal]:
        """Apply amount to deductible accumulators.

        Handles individual + family coordination:
        - Amount applies to individual accumulator first
        - Also applies to family accumulator (tracks aggregate)
        - Once family deductible is met, individual is considered met too

        Args:
            amount: Amount to apply to deductible
            network: Network tier for the service
            benefit_type: Type of benefit (medical, pharmacy, combined)

        Returns:
            Tuple of (new_accumulator_set, amount_actually_applied)
        """
        updates: dict = {}
        total_applied = Decimal("0")

        # Handle pharmacy-specific deductible
        if benefit_type == BenefitType.PHARMACY and self.rx_deductible:
            new_rx_ded, applied = self.rx_deductible.apply(amount)
            updates["rx_deductible"] = new_rx_ded
            return self.model_copy(update=updates), applied

        # Select appropriate accumulators based on network
        if self._is_in_network(network):
            ind_acc = self.deductible_individual_in
            fam_acc = self.deductible_family_in
            ind_key = "deductible_individual_in"
            fam_key = "deductible_family_in"
        else:
            ind_acc = self.deductible_individual_out
            fam_acc = self.deductible_family_out
            ind_key = "deductible_individual_out"
            fam_key = "deductible_family_out"

        # Check if family deductible is already met (waives individual)
        if fam_acc and fam_acc.met:
            return self, Decimal("0")

        # Apply to individual
        if ind_acc and not ind_acc.met:
            new_ind, applied = ind_acc.apply(amount)
            updates[ind_key] = new_ind
            total_applied = applied

        # Apply to family (same amount, tracks family aggregate)
        if fam_acc and total_applied > 0:
            new_fam, _ = fam_acc.apply(total_applied)
            updates[fam_key] = new_fam

        return self.model_copy(update=updates), total_applied

    def apply_to_oop(
        self,
        amount: Decimal,
        network: NetworkTier = NetworkTier.IN_NETWORK,
        benefit_type: BenefitType = BenefitType.COMBINED,
    ) -> tuple[AccumulatorSet, Decimal]:
        """Apply amount to out-of-pocket accumulators.

        Handles individual + family coordination similar to deductible.
        Note: Amounts applied to deductible should also be applied to OOP
        since deductible counts toward out-of-pocket maximum.

        Args:
            amount: Amount to apply to OOP
            network: Network tier for the service
            benefit_type: Type of benefit (medical, pharmacy, combined)

        Returns:
            Tuple of (new_accumulator_set, amount_actually_applied)
        """
        updates: dict = {}
        total_applied = Decimal("0")

        # Handle pharmacy-specific OOP
        if benefit_type == BenefitType.PHARMACY and self.rx_oop:
            new_rx_oop, applied = self.rx_oop.apply(amount)
            updates["rx_oop"] = new_rx_oop
            return self.model_copy(update=updates), applied

        # Select appropriate accumulators based on network
        if self._is_in_network(network):
            ind_acc = self.oop_individual_in
            fam_acc = self.oop_family_in
            ind_key = "oop_individual_in"
            fam_key = "oop_family_in"
        else:
            ind_acc = self.oop_individual_out
            fam_acc = self.oop_family_out
            ind_key = "oop_individual_out"
            fam_key = "oop_family_out"

        # Check if family OOP is already met (plan pays 100%)
        if fam_acc and fam_acc.met:
            return self, Decimal("0")

        # Apply to individual
        if ind_acc and not ind_acc.met:
            new_ind, applied = ind_acc.apply(amount)
            updates[ind_key] = new_ind
            total_applied = applied

        # Apply to family
        if fam_acc and total_applied > 0:
            new_fam, _ = fam_acc.apply(total_applied)
            updates[fam_key] = new_fam

        return self.model_copy(update=updates), total_applied

    def apply_to_specialty_oop(self, amount: Decimal) -> tuple[AccumulatorSet, Decimal]:
        """Apply amount to specialty drug OOP accumulator.

        Some plans have a separate out-of-pocket maximum for specialty
        medications that is lower than the overall OOP max.

        Args:
            amount: Amount to apply

        Returns:
            Tuple of (new_accumulator_set, amount_actually_applied)
        """
        if not self.specialty_oop:
            return self, Decimal("0")

        new_specialty, applied = self.specialty_oop.apply(amount)
        return self.model_copy(update={"specialty_oop": new_specialty}), applied

    def is_deductible_met(
        self,
        network: NetworkTier = NetworkTier.IN_NETWORK,
        benefit_type: BenefitType = BenefitType.COMBINED,
    ) -> bool:
        """Check if deductible is met (individual OR family).

        Args:
            network: Network tier to check
            benefit_type: Benefit type to check

        Returns:
            True if deductible is met
        """
        # Check pharmacy-specific deductible
        if benefit_type == BenefitType.PHARMACY and self.rx_deductible:
            return self.rx_deductible.met

        if self._is_in_network(network):
            ind = self.deductible_individual_in
            fam = self.deductible_family_in
        else:
            ind = self.deductible_individual_out
            fam = self.deductible_family_out

        # Family met = everyone's deductible is waived
        if fam and fam.met:
            return True
        # Otherwise check individual
        return ind.met if ind else False

    def is_oop_met(
        self,
        network: NetworkTier = NetworkTier.IN_NETWORK,
        benefit_type: BenefitType = BenefitType.COMBINED,
    ) -> bool:
        """Check if out-of-pocket maximum is met.

        Args:
            network: Network tier to check
            benefit_type: Benefit type to check

        Returns:
            True if OOP max is met (plan pays 100%)
        """
        # Check pharmacy-specific OOP
        if benefit_type == BenefitType.PHARMACY and self.rx_oop:
            return self.rx_oop.met

        if self._is_in_network(network):
            ind = self.oop_individual_in
            fam = self.oop_family_in
        else:
            ind = self.oop_individual_out
            fam = self.oop_family_out

        # Family met = plan pays 100% for everyone
        if fam and fam.met:
            return True
        return ind.met if ind else False

    def get_deductible_remaining(
        self,
        network: NetworkTier = NetworkTier.IN_NETWORK,
        benefit_type: BenefitType = BenefitType.COMBINED,
    ) -> Decimal:
        """Get remaining deductible amount.

        Args:
            network: Network tier to check
            benefit_type: Benefit type to check

        Returns:
            Remaining deductible amount
        """
        if benefit_type == BenefitType.PHARMACY and self.rx_deductible:
            return self.rx_deductible.remaining

        if self._is_in_network(network):
            ind = self.deductible_individual_in
            fam = self.deductible_family_in
        else:
            ind = self.deductible_individual_out
            fam = self.deductible_family_out

        # If family is met, individual remaining is 0
        if fam and fam.met:
            return Decimal("0")
        return ind.remaining if ind else Decimal("0")

    def get_oop_remaining(
        self,
        network: NetworkTier = NetworkTier.IN_NETWORK,
        benefit_type: BenefitType = BenefitType.COMBINED,
    ) -> Decimal:
        """Get remaining out-of-pocket amount.

        Args:
            network: Network tier to check
            benefit_type: Benefit type to check

        Returns:
            Remaining OOP amount
        """
        if benefit_type == BenefitType.PHARMACY and self.rx_oop:
            return self.rx_oop.remaining

        if self._is_in_network(network):
            ind = self.oop_individual_in
            fam = self.oop_family_in
        else:
            ind = self.oop_individual_out
            fam = self.oop_family_out

        if fam and fam.met:
            return Decimal("0")
        return ind.remaining if ind else Decimal("0")

    def reset_for_new_year(self, new_plan_year: int | None = None) -> AccumulatorSet:
        """Reset all accumulators for a new plan year.

        Args:
            new_plan_year: New plan year (defaults to current + 1)

        Returns:
            New AccumulatorSet with all accumulators reset
        """
        new_year = new_plan_year or (self.plan_year + 1)
        updates: dict = {"plan_year": new_year}

        for field_name in [
            "deductible_individual_in",
            "deductible_individual_out",
            "deductible_family_in",
            "deductible_family_out",
            "oop_individual_in",
            "oop_individual_out",
            "oop_family_in",
            "oop_family_out",
            "rx_deductible",
            "rx_oop",
            "specialty_oop",
        ]:
            acc = getattr(self, field_name)
            if acc:
                updates[field_name] = acc.reset(new_year)

        return self.model_copy(update=updates)


# =============================================================================
# Factory Functions
# =============================================================================


def create_medical_accumulators(
    member_id: str,
    plan_year: int,
    deductible_individual: Decimal,
    deductible_family: Decimal,
    oop_individual: Decimal,
    oop_family: Decimal,
    deductible_individual_oon: Decimal | None = None,
    deductible_family_oon: Decimal | None = None,
    oop_individual_oon: Decimal | None = None,
    oop_family_oon: Decimal | None = None,
) -> AccumulatorSet:
    """Create accumulator set for medical benefits.

    Creates a standard set of medical benefit accumulators including
    individual and family deductibles and out-of-pocket maximums
    for both in-network and out-of-network tiers.

    Args:
        member_id: Member identifier
        plan_year: Benefit plan year
        deductible_individual: Individual in-network deductible
        deductible_family: Family in-network deductible
        oop_individual: Individual in-network OOP maximum
        oop_family: Family in-network OOP maximum
        deductible_individual_oon: Individual OON deductible (default: 2x in-network)
        deductible_family_oon: Family OON deductible (default: 2x in-network)
        oop_individual_oon: Individual OON OOP max (default: 2x in-network)
        oop_family_oon: Family OON OOP max (default: 2x in-network)

    Returns:
        AccumulatorSet configured for medical benefits

    Example:
        >>> acc_set = create_medical_accumulators(
        ...     member_id="MEM-001",
        ...     plan_year=2024,
        ...     deductible_individual=Decimal("500"),
        ...     deductible_family=Decimal("1500"),
        ...     oop_individual=Decimal("3000"),
        ...     oop_family=Decimal("6000"),
        ... )
    """
    return AccumulatorSet(
        member_id=member_id,
        plan_year=plan_year,
        deductible_individual_in=Accumulator(
            accumulator_type=AccumulatorType.DEDUCTIBLE,
            level=AccumulatorLevel.INDIVIDUAL,
            network_tier=NetworkTier.IN_NETWORK,
            benefit_type=BenefitType.MEDICAL,
            limit=deductible_individual,
            plan_year=plan_year,
        ),
        deductible_family_in=Accumulator(
            accumulator_type=AccumulatorType.DEDUCTIBLE,
            level=AccumulatorLevel.FAMILY,
            network_tier=NetworkTier.IN_NETWORK,
            benefit_type=BenefitType.MEDICAL,
            limit=deductible_family,
            plan_year=plan_year,
        ),
        oop_individual_in=Accumulator(
            accumulator_type=AccumulatorType.OUT_OF_POCKET_MAX,
            level=AccumulatorLevel.INDIVIDUAL,
            network_tier=NetworkTier.IN_NETWORK,
            benefit_type=BenefitType.MEDICAL,
            limit=oop_individual,
            plan_year=plan_year,
        ),
        oop_family_in=Accumulator(
            accumulator_type=AccumulatorType.OUT_OF_POCKET_MAX,
            level=AccumulatorLevel.FAMILY,
            network_tier=NetworkTier.IN_NETWORK,
            benefit_type=BenefitType.MEDICAL,
            limit=oop_family,
            plan_year=plan_year,
        ),
        deductible_individual_out=Accumulator(
            accumulator_type=AccumulatorType.DEDUCTIBLE,
            level=AccumulatorLevel.INDIVIDUAL,
            network_tier=NetworkTier.OUT_OF_NETWORK,
            benefit_type=BenefitType.MEDICAL,
            limit=deductible_individual_oon or deductible_individual * 2,
            plan_year=plan_year,
        ),
        deductible_family_out=Accumulator(
            accumulator_type=AccumulatorType.DEDUCTIBLE,
            level=AccumulatorLevel.FAMILY,
            network_tier=NetworkTier.OUT_OF_NETWORK,
            benefit_type=BenefitType.MEDICAL,
            limit=deductible_family_oon or deductible_family * 2,
            plan_year=plan_year,
        ),
        oop_individual_out=Accumulator(
            accumulator_type=AccumulatorType.OUT_OF_POCKET_MAX,
            level=AccumulatorLevel.INDIVIDUAL,
            network_tier=NetworkTier.OUT_OF_NETWORK,
            benefit_type=BenefitType.MEDICAL,
            limit=oop_individual_oon or oop_individual * 2,
            plan_year=plan_year,
        ),
        oop_family_out=Accumulator(
            accumulator_type=AccumulatorType.OUT_OF_POCKET_MAX,
            level=AccumulatorLevel.FAMILY,
            network_tier=NetworkTier.OUT_OF_NETWORK,
            benefit_type=BenefitType.MEDICAL,
            limit=oop_family_oon or oop_family * 2,
            plan_year=plan_year,
        ),
    )


def create_pharmacy_accumulators(
    member_id: str,
    plan_year: int,
    deductible: Decimal,
    oop_max: Decimal,
    specialty_oop: Decimal | None = None,
) -> AccumulatorSet:
    """Create accumulator set for pharmacy benefits.

    Creates accumulators for carved-out pharmacy benefits with separate
    deductible and OOP tracking from medical benefits.

    Args:
        member_id: Member identifier
        plan_year: Benefit plan year
        deductible: Pharmacy deductible
        oop_max: Pharmacy out-of-pocket maximum
        specialty_oop: Specialty drug OOP limit (optional)

    Returns:
        AccumulatorSet configured for pharmacy benefits

    Example:
        >>> acc_set = create_pharmacy_accumulators(
        ...     member_id="RXM-001",
        ...     plan_year=2024,
        ...     deductible=Decimal("100"),
        ...     oop_max=Decimal("2000"),
        ...     specialty_oop=Decimal("500"),
        ... )
    """
    acc_set = AccumulatorSet(
        member_id=member_id,
        plan_year=plan_year,
        rx_deductible=Accumulator(
            accumulator_type=AccumulatorType.RX_DEDUCTIBLE,
            level=AccumulatorLevel.INDIVIDUAL,
            network_tier=NetworkTier.PREFERRED_PHARMACY,
            benefit_type=BenefitType.PHARMACY,
            limit=deductible,
            plan_year=plan_year,
        ),
        rx_oop=Accumulator(
            accumulator_type=AccumulatorType.RX_OOP_MAX,
            level=AccumulatorLevel.INDIVIDUAL,
            network_tier=NetworkTier.PREFERRED_PHARMACY,
            benefit_type=BenefitType.PHARMACY,
            limit=oop_max,
            plan_year=plan_year,
        ),
    )

    if specialty_oop:
        acc_set = acc_set.model_copy(
            update={
                "specialty_oop": Accumulator(
                    accumulator_type=AccumulatorType.SPECIALTY_OOP,
                    level=AccumulatorLevel.INDIVIDUAL,
                    network_tier=NetworkTier.SPECIALTY_PHARMACY,
                    benefit_type=BenefitType.PHARMACY,
                    limit=specialty_oop,
                    plan_year=plan_year,
                )
            }
        )

    return acc_set


def create_integrated_accumulators(
    member_id: str,
    plan_year: int,
    deductible_individual: Decimal,
    deductible_family: Decimal,
    oop_individual: Decimal,
    oop_family: Decimal,
) -> AccumulatorSet:
    """Create accumulator set for integrated medical + pharmacy benefits.

    Creates accumulators for plans where medical and pharmacy share
    the same deductible and out-of-pocket maximums.

    Args:
        member_id: Member identifier
        plan_year: Benefit plan year
        deductible_individual: Combined individual deductible
        deductible_family: Combined family deductible
        oop_individual: Combined individual OOP maximum
        oop_family: Combined family OOP maximum

    Returns:
        AccumulatorSet configured for integrated benefits

    Example:
        >>> acc_set = create_integrated_accumulators(
        ...     member_id="INT-001",
        ...     plan_year=2024,
        ...     deductible_individual=Decimal("750"),
        ...     deductible_family=Decimal("2250"),
        ...     oop_individual=Decimal("4000"),
        ...     oop_family=Decimal("8000"),
        ... )
    """
    return AccumulatorSet(
        member_id=member_id,
        plan_year=plan_year,
        deductible_individual_in=Accumulator(
            accumulator_type=AccumulatorType.DEDUCTIBLE,
            level=AccumulatorLevel.INDIVIDUAL,
            network_tier=NetworkTier.IN_NETWORK,
            benefit_type=BenefitType.COMBINED,
            limit=deductible_individual,
            plan_year=plan_year,
        ),
        deductible_family_in=Accumulator(
            accumulator_type=AccumulatorType.DEDUCTIBLE,
            level=AccumulatorLevel.FAMILY,
            network_tier=NetworkTier.IN_NETWORK,
            benefit_type=BenefitType.COMBINED,
            limit=deductible_family,
            plan_year=plan_year,
        ),
        oop_individual_in=Accumulator(
            accumulator_type=AccumulatorType.OUT_OF_POCKET_MAX,
            level=AccumulatorLevel.INDIVIDUAL,
            network_tier=NetworkTier.IN_NETWORK,
            benefit_type=BenefitType.COMBINED,
            limit=oop_individual,
            plan_year=plan_year,
        ),
        oop_family_in=Accumulator(
            accumulator_type=AccumulatorType.OUT_OF_POCKET_MAX,
            level=AccumulatorLevel.FAMILY,
            network_tier=NetworkTier.IN_NETWORK,
            benefit_type=BenefitType.COMBINED,
            limit=oop_family,
            plan_year=plan_year,
        ),
    )
