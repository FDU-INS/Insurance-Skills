"""Capitation payment calculations."""

from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field


class CapitationRate(BaseModel):
    """PMPM capitation rate by category."""

    rate_id: str = Field(..., description="Rate identifier")
    contract_id: str = Field(..., description="Associated contract")

    effective_date: date = Field(..., description="Rate effective date")
    termination_date: date | None = Field(None)

    # Base PMPM rates by age/gender
    rate_category: str = Field("ADULT", description="PEDIATRIC, ADULT, SENIOR")
    base_pmpm: Decimal = Field(..., description="Base per-member-per-month rate")

    # Adjustments
    risk_adjusted: bool = Field(True, description="Apply risk score adjustment")
    quality_adjustment_pct: Decimal | None = Field(None, description="Quality bonus/penalty %")

    def calculate_pmpm(self, risk_score: Decimal = Decimal("1.0")) -> Decimal:
        """Calculate risk-adjusted PMPM."""
        adjusted = self.base_pmpm
        if self.risk_adjusted:
            adjusted = adjusted * risk_score
        return adjusted.quantize(Decimal("0.01"))


class CapitationPayment(BaseModel):
    """Monthly capitation payment record."""

    payment_id: str = Field(..., description="Payment identifier")
    provider_npi: str = Field(..., description="Payee provider")
    contract_id: str = Field(..., description="Contract reference")

    payment_period: str = Field(..., description="YYYY-MM format")
    payment_date: date = Field(..., description="Date payment issued")

    member_months: int = Field(..., description="Number of member-months")
    base_amount: Decimal = Field(..., description="Base capitation amount")
    risk_adjustment: Decimal = Field(Decimal("0"), description="Risk adjustment amount")
    quality_adjustment: Decimal = Field(Decimal("0"), description="Quality bonus/penalty")

    total_amount: Decimal = Field(..., description="Final payment amount")

    # Breakdown by category
    pediatric_members: int = Field(0)
    adult_members: int = Field(0)
    senior_members: int = Field(0)


def calculate_capitation_payment(
    provider_npi: str,
    contract_id: str,
    payment_period: str,
    members: list[dict],  # List of {member_id, age, risk_score}
    rates: dict[str, CapitationRate],
) -> CapitationPayment:
    """Calculate monthly capitation payment for a provider.

    Args:
        provider_npi: Provider NPI
        contract_id: Contract reference
        payment_period: YYYY-MM
        members: List of attributed members with age and risk score
        rates: Capitation rates by category

    Returns:
        CapitationPayment record
    """
    pediatric = [m for m in members if m.get("age", 30) < 18]
    adults = [m for m in members if 18 <= m.get("age", 30) < 65]
    seniors = [m for m in members if m.get("age", 30) >= 65]

    base_amount = Decimal("0")
    risk_amount = Decimal("0")

    # Calculate by category
    for category, member_list in [
        ("PEDIATRIC", pediatric),
        ("ADULT", adults),
        ("SENIOR", seniors),
    ]:
        rate = rates.get(category)
        if rate and member_list:
            for m in member_list:
                risk = Decimal(str(m.get("risk_score", 1.0)))
                member_base = rate.base_pmpm
                base_amount += member_base
                if rate.risk_adjusted:
                    risk_amount += member_base * (risk - Decimal("1.0"))

    total = base_amount + risk_amount

    return CapitationPayment(
        payment_id=f"CAP-{provider_npi}-{payment_period}",
        provider_npi=provider_npi,
        contract_id=contract_id,
        payment_period=payment_period,
        payment_date=date.today(),
        member_months=len(members),
        base_amount=base_amount.quantize(Decimal("0.01")),
        risk_adjustment=risk_amount.quantize(Decimal("0.01")),
        total_amount=total.quantize(Decimal("0.01")),
        pediatric_members=len(pediatric),
        adult_members=len(adults),
        senior_members=len(seniors),
    )
