"""Member attribution for value-based care arrangements."""

from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field


class AttributionMethod:
    """Attribution methodology constants."""

    PROSPECTIVE = "PROSPECTIVE"  # Assigned at start of period
    RETROSPECTIVE = "RETROSPECTIVE"  # Assigned after claims analysis
    HYBRID = "HYBRID"  # Combination of both


class Attribution(BaseModel):
    """Member attribution to a provider/practice."""

    attribution_id: str = Field(..., description="Unique attribution ID")
    member_id: str = Field(..., description="Attributed member")
    provider_npi: str = Field(..., description="Attributed PCP/practice NPI")
    provider_tin: str | None = Field(None, description="Provider TIN for group attribution")

    attribution_method: str = Field(AttributionMethod.PROSPECTIVE)
    attribution_reason: str = Field(
        "PCP_SELECTION", description="PCP_SELECTION, PLURALITY, ASSIGNMENT"
    )

    effective_date: date = Field(..., description="Attribution start date")
    termination_date: date | None = Field(None, description="Attribution end date")

    performance_year: int = Field(..., description="Contract/measurement year")

    # Risk scoring
    risk_score: Decimal | None = Field(None, description="Member's risk score (RAF)")
    hcc_codes: list[str] = Field(default_factory=list, description="HCC categories captured")

    @property
    def is_active(self) -> bool:
        """Check if attribution is currently active."""
        today = date.today()
        if self.termination_date:
            return self.effective_date <= today <= self.termination_date
        return self.effective_date <= today


class AttributionPanel(BaseModel):
    """Provider's attributed member panel."""

    provider_npi: str = Field(..., description="Provider NPI")
    provider_name: str = Field(..., description="Provider/practice name")
    performance_year: int = Field(..., description="Contract year")

    attributed_members: list[str] = Field(default_factory=list, description="Member IDs")
    total_members: int = Field(0, description="Panel size")

    avg_risk_score: Decimal | None = Field(None, description="Average RAF score")
    total_pmpm: Decimal | None = Field(None, description="Total PMPM budget")

    @property
    def panel_size(self) -> int:
        return len(self.attributed_members) or self.total_members


# HCC Categories for risk adjustment
HCC_CATEGORIES: dict[str, str] = {
    "HCC18": "Diabetes with Chronic Complications",
    "HCC19": "Diabetes without Complication",
    "HCC85": "Congestive Heart Failure",
    "HCC96": "Specified Heart Arrhythmias",
    "HCC111": "Chronic Obstructive Pulmonary Disease",
    "HCC135": "Acute Renal Failure",
    "HCC136": "Chronic Kidney Disease, Stage 5",
    "HCC137": "Chronic Kidney Disease, Severe (Stage 4)",
    "HCC138": "Chronic Kidney Disease, Moderate (Stage 3B)",
}
