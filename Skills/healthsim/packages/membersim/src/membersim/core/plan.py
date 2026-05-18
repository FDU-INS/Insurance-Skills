"""Benefit plan and coverage model."""

from decimal import Decimal

from pydantic import BaseModel, Field


class Plan(BaseModel):
    """Benefit plan with cost sharing details."""

    model_config = {"frozen": True}

    plan_code: str = Field(..., description="Plan identifier")
    plan_name: str = Field(..., description="Human-readable plan name")
    plan_type: str = Field(..., description="HMO, PPO, EPO, POS, HDHP")
    coverage_type: str = Field("MEDICAL", description="MEDICAL, DENTAL, VISION, RX")

    # Deductibles
    deductible_individual: Decimal = Field(
        Decimal("500"), description="Annual individual deductible"
    )
    deductible_family: Decimal = Field(Decimal("1500"), description="Annual family deductible")

    # Out-of-pocket maximums
    oop_max_individual: Decimal = Field(Decimal("3000"), description="Individual OOP maximum")
    oop_max_family: Decimal = Field(Decimal("6000"), description="Family OOP maximum")

    # Cost sharing
    copay_pcp: Decimal = Field(Decimal("25"), description="Primary care copay")
    copay_specialist: Decimal = Field(Decimal("50"), description="Specialist copay")
    copay_er: Decimal = Field(Decimal("250"), description="Emergency room copay")
    coinsurance: Decimal = Field(Decimal("0.20"), description="Coinsurance percentage (0.20 = 20%)")

    # Network
    requires_pcp: bool = Field(False, description="Requires PCP assignment (HMO)")
    requires_referral: bool = Field(False, description="Requires referral for specialists")


# Sample plan configurations
SAMPLE_PLANS = {
    "PPO_GOLD": Plan(
        plan_code="PPO_GOLD",
        plan_name="Gold PPO Plan",
        plan_type="PPO",
        deductible_individual=Decimal("500"),
        deductible_family=Decimal("1000"),
        oop_max_individual=Decimal("3000"),
        oop_max_family=Decimal("6000"),
        copay_pcp=Decimal("20"),
        copay_specialist=Decimal("40"),
        copay_er=Decimal("150"),
        coinsurance=Decimal("0.20"),
    ),
    "HMO_STANDARD": Plan(
        plan_code="HMO_STANDARD",
        plan_name="Standard HMO Plan",
        plan_type="HMO",
        deductible_individual=Decimal("250"),
        deductible_family=Decimal("500"),
        oop_max_individual=Decimal("2500"),
        oop_max_family=Decimal("5000"),
        copay_pcp=Decimal("15"),
        copay_specialist=Decimal("30"),
        copay_er=Decimal("100"),
        coinsurance=Decimal("0.10"),
        requires_pcp=True,
        requires_referral=True,
    ),
    "HDHP_HSA": Plan(
        plan_code="HDHP_HSA",
        plan_name="High Deductible Health Plan with HSA",
        plan_type="HDHP",
        deductible_individual=Decimal("1500"),
        deductible_family=Decimal("3000"),
        oop_max_individual=Decimal("7500"),
        oop_max_family=Decimal("15000"),
        copay_pcp=Decimal("0"),  # No copay until deductible met
        copay_specialist=Decimal("0"),
        copay_er=Decimal("0"),
        coinsurance=Decimal("0.20"),
    ),
}
