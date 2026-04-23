"""Pharmacy benefit member model.

This module provides pharmacy member models for RxMemberSim.
For shared accumulator infrastructure, see healthsim.benefits.
"""

from datetime import date
from decimal import Decimal

from healthsim.benefits import AccumulatorSet as CoreAccumulatorSet
from healthsim.benefits import BenefitType, create_pharmacy_accumulators
from pydantic import BaseModel, Field


class MemberDemographics(BaseModel):
    """Member demographic information."""

    first_name: str
    last_name: str
    date_of_birth: date
    gender: str  # M, F, U
    address_line1: str | None = None
    address_line2: str | None = None
    city: str | None = None
    state: str | None = None
    zip_code: str | None = None
    phone: str | None = None


class BenefitAccumulators(BaseModel):
    """Member benefit accumulators.

    This is a backward-compatible wrapper. For new code with full accumulator
    functionality, use healthsim.benefits.AccumulatorSet directly via
    the to_accumulator_set() method.

    Example (legacy):
        >>> acc = BenefitAccumulators(
        ...     deductible_remaining=Decimal("100"),
        ...     oop_remaining=Decimal("2000"),
        ... )

    Example (recommended):
        >>> from healthsim.benefits import create_pharmacy_accumulators
        >>> acc_set = create_pharmacy_accumulators(
        ...     member_id="RXM-001",
        ...     plan_year=2024,
        ...     deductible=Decimal("100"),
        ...     oop_max=Decimal("3000"),
        ... )
    """

    deductible_met: Decimal = Field(
        default=Decimal("0"), description="Amount applied to deductible"
    )
    deductible_remaining: Decimal = Field(
        ..., description="Remaining deductible amount"
    )
    oop_met: Decimal = Field(
        default=Decimal("0"), description="Amount applied to OOP max"
    )
    oop_remaining: Decimal = Field(..., description="Remaining OOP amount")

    @property
    def deductible_limit(self) -> Decimal:
        """Calculate original deductible limit."""
        return self.deductible_met + self.deductible_remaining

    @property
    def oop_limit(self) -> Decimal:
        """Calculate original OOP limit."""
        return self.oop_met + self.oop_remaining

    @property
    def is_deductible_met(self) -> bool:
        """Check if deductible has been met."""
        return self.deductible_remaining <= Decimal("0")

    @property
    def is_oop_met(self) -> bool:
        """Check if OOP max has been met."""
        return self.oop_remaining <= Decimal("0")

    def apply(
        self, deductible_amount: Decimal, oop_amount: Decimal
    ) -> "BenefitAccumulators":
        """Apply amounts to accumulators.

        Args:
            deductible_amount: Amount to apply to deductible
            oop_amount: Amount to apply to OOP

        Returns:
            New BenefitAccumulators with updated amounts
        """
        new_ded_applied = min(deductible_amount, self.deductible_remaining)
        new_oop_applied = min(oop_amount, self.oop_remaining)

        return BenefitAccumulators(
            deductible_met=self.deductible_met + new_ded_applied,
            deductible_remaining=self.deductible_remaining - new_ded_applied,
            oop_met=self.oop_met + new_oop_applied,
            oop_remaining=self.oop_remaining - new_oop_applied,
        )

    def to_accumulator_set(self, member_id: str, plan_year: int) -> CoreAccumulatorSet:
        """Convert to a core AccumulatorSet.

        Args:
            member_id: Member identifier
            plan_year: Benefit plan year

        Returns:
            AccumulatorSet configured for pharmacy benefits
        """
        acc_set = create_pharmacy_accumulators(
            member_id=member_id,
            plan_year=plan_year,
            deductible=self.deductible_limit,
            oop_max=self.oop_limit,
        )

        # Apply current amounts
        if self.deductible_met > 0:
            acc_set, _ = acc_set.apply_to_deductible(
                self.deductible_met, benefit_type=BenefitType.PHARMACY
            )
        if self.oop_met > 0:
            acc_set, _ = acc_set.apply_to_oop(
                self.oop_met, benefit_type=BenefitType.PHARMACY
            )

        return acc_set

    @classmethod
    def from_accumulator_set(cls, acc_set: CoreAccumulatorSet) -> "BenefitAccumulators":
        """Create from a core AccumulatorSet.

        Args:
            acc_set: AccumulatorSet to convert from

        Returns:
            BenefitAccumulators instance
        """
        rx_ded = acc_set.rx_deductible
        rx_oop = acc_set.rx_oop

        return cls(
            deductible_met=rx_ded.applied if rx_ded else Decimal("0"),
            deductible_remaining=rx_ded.remaining if rx_ded else Decimal("0"),
            oop_met=rx_oop.applied if rx_oop else Decimal("0"),
            oop_remaining=rx_oop.remaining if rx_oop else Decimal("0"),
        )


class RxMember(BaseModel):
    """Pharmacy benefit member."""

    member_id: str
    cardholder_id: str
    person_code: str = "01"  # 01=cardholder, 02=spouse, 03+=dependent

    # Pharmacy benefit identifiers
    bin: str  # Bank Identification Number
    pcn: str  # Processor Control Number
    group_number: str

    # Demographics
    demographics: MemberDemographics

    # Coverage dates
    effective_date: date
    termination_date: date | None = None

    # Accumulators
    accumulators: BenefitAccumulators

    # Plan info
    plan_code: str | None = None
    formulary_id: str | None = None

    def get_accumulator_set(self, plan_year: int | None = None) -> CoreAccumulatorSet:
        """Get accumulators as a core AccumulatorSet.

        Args:
            plan_year: Benefit year (defaults to effective_date year)

        Returns:
            AccumulatorSet for this member
        """
        year = plan_year or self.effective_date.year
        return self.accumulators.to_accumulator_set(self.member_id, year)


class RxMemberFactory:
    """Simple factory for creating pharmacy members without reproducibility.

    For reproducible generation with seed support, use RxMemberGenerator
    from rxmembersim.core.generator instead.
    """

    def generate(
        self,
        bin: str = "610014",
        pcn: str = "RXTEST",
        group_number: str = "GRP001",
    ) -> RxMember:
        """Generate a random pharmacy member."""
        from faker import Faker

        fake = Faker()

        member_id = f"RXM-{fake.random_number(digits=8, fix_len=True)}"

        return RxMember(
            member_id=member_id,
            cardholder_id=str(fake.random_number(digits=9, fix_len=True)),
            person_code="01",
            bin=bin,
            pcn=pcn,
            group_number=group_number,
            demographics=MemberDemographics(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=85),
                gender=fake.random_element(["M", "F"]),
                address_line1=fake.street_address(),
                city=fake.city(),
                state=fake.state_abbr(),
                zip_code=fake.zipcode(),
            ),
            effective_date=date(2025, 1, 1),
            accumulators=BenefitAccumulators(
                deductible_remaining=Decimal("250"),
                oop_remaining=Decimal("3000"),
            ),
        )


