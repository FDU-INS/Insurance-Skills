"""Provider fee schedule for claims pricing."""

from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field

# Sample Medicare rates for common procedures
MEDICARE_BASE_RATES: dict[str, Decimal] = {
    "99213": Decimal("92.00"),  # Office Visit Level 3
    "99214": Decimal("134.00"),  # Office Visit Level 4
    "99215": Decimal("181.00"),  # Office Visit Level 5
    "99395": Decimal("152.00"),  # Preventive Visit 18-39
    "99396": Decimal("161.00"),  # Preventive Visit 40-64
    "85025": Decimal("10.00"),  # CBC
    "80053": Decimal("14.00"),  # Comprehensive Metabolic Panel
    "71046": Decimal("26.00"),  # Chest X-ray
    "93000": Decimal("18.00"),  # ECG
}


class FeeSchedule(BaseModel):
    """Fee schedule for provider reimbursement."""

    schedule_id: str = Field(..., description="Fee schedule identifier")
    contract_id: str = Field(..., description="Associated contract")
    effective_date: date = Field(..., description="Schedule effective date")
    termination_date: date | None = Field(None)

    base_rate_type: str = Field("MEDICARE_PCT", description="MEDICARE_PCT, FLAT, CUSTOM")
    medicare_percentage: Decimal = Field(
        Decimal("1.20"), description="e.g., 1.20 = 120% of Medicare"
    )

    # Custom overrides (CPT -> rate)
    custom_rates: dict[str, Decimal] = Field(default_factory=dict)

    def get_allowed_amount(self, procedure_code: str, units: Decimal = Decimal("1")) -> Decimal:
        """Calculate allowed amount for a procedure."""
        # Check for custom override first
        if procedure_code in self.custom_rates:
            return self.custom_rates[procedure_code] * units

        # Use Medicare-based calculation
        if self.base_rate_type == "MEDICARE_PCT":
            base = MEDICARE_BASE_RATES.get(procedure_code, Decimal("50.00"))
            return base * self.medicare_percentage * units

        # Default fallback
        return Decimal("50.00") * units


def create_default_fee_schedule(
    contract_id: str, medicare_pct: Decimal = Decimal("1.20")
) -> FeeSchedule:
    """Create a default fee schedule at specified Medicare percentage."""
    return FeeSchedule(
        schedule_id=f"FS-{contract_id}",
        contract_id=contract_id,
        effective_date=date.today(),
        medicare_percentage=medicare_pct,
    )
