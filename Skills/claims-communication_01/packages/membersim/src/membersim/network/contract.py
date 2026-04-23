"""Provider contract and network participation."""

from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field


class ProviderContract(BaseModel):
    """Provider contract terms."""

    contract_id: str = Field(..., description="Unique contract identifier")
    provider_npi: str = Field(..., description="Provider NPI or TIN for group")
    network_id: str = Field(..., description="Network this contract belongs to")

    effective_date: date = Field(..., description="Contract start date")
    termination_date: date | None = Field(None, description="Contract end date")

    contract_type: str = Field("FFS", description="FFS, CAPITATION, VALUE_BASED")
    fee_schedule_type: str = Field("MEDICARE_PCT", description="MEDICARE_PCT, FLAT_RATE, CUSTOM")
    fee_schedule_pct: Decimal | None = Field(Decimal("1.20"), description="Percent of Medicare")
    capitation_rate: Decimal | None = Field(None, description="PMPM if capitated")

    quality_bonus_eligible: bool = Field(True, description="Participates in quality incentives")

    # Contract terms
    timely_filing_days: int = Field(90, description="Days to submit claims")
    clean_claim_days: int = Field(30, description="Days to pay clean claims")

    @property
    def is_active(self) -> bool:
        """Check if contract is currently active."""
        today = date.today()
        if self.termination_date is None:
            return self.effective_date <= today
        return self.effective_date <= today <= self.termination_date
