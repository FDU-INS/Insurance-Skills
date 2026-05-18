"""Quality measure definitions and status tracking."""

from datetime import date

from pydantic import BaseModel, Field


class QualityMeasure(BaseModel):
    """HEDIS/Star Rating measure definition."""

    measure_id: str = Field(..., description="HEDIS measure ID (e.g., 'BCS', 'CDC')")
    measure_name: str = Field(..., description="Full measure name")
    measure_year: int = Field(..., description="Measurement year")

    denominator_criteria: str = Field(..., description="Who is eligible for the measure")
    numerator_criteria: str = Field(..., description="What constitutes compliance")

    measure_type: str = Field("ADMINISTRATIVE", description="ADMINISTRATIVE, HYBRID, SURVEY")
    measure_domain: str = Field("EFFECTIVENESS", description="EFFECTIVENESS, ACCESS, EXPERIENCE")

    # Age eligibility
    min_age: int | None = Field(None, description="Minimum age for denominator")
    max_age: int | None = Field(None, description="Maximum age for denominator")
    gender: str | None = Field(None, description="Required gender (M, F, or None for both)")

    # Compliance codes
    compliant_codes: list[str] = Field(
        default_factory=list, description="CPT/HCPCS codes that close gap"
    )
    exclusion_codes: list[str] = Field(
        default_factory=list, description="Codes that exclude from measure"
    )


class MemberMeasureStatus(BaseModel):
    """Individual member's status for a quality measure."""

    member_id: str = Field(..., description="Member reference")
    measure_id: str = Field(..., description="Measure reference")
    measure_year: int = Field(..., description="Measurement year")

    in_denominator: bool = Field(False, description="Member meets denominator criteria")
    in_numerator: bool = Field(False, description="Member is compliant (gap closed)")

    gap_status: str = Field("NOT_APPLICABLE", description="OPEN, CLOSED, EXCLUDED, NOT_APPLICABLE")

    last_service_date: date | None = Field(
        None, description="Date of most recent compliant service"
    )
    exclusion_reason: str | None = Field(None, description="Why excluded from measure")

    @property
    def has_open_gap(self) -> bool:
        """Check if member has an open care gap."""
        return self.in_denominator and not self.in_numerator and self.gap_status == "OPEN"


class GapStatus:
    """Gap status constants."""

    OPEN = "OPEN"
    CLOSED = "CLOSED"
    EXCLUDED = "EXCLUDED"
    NOT_APPLICABLE = "NOT_APPLICABLE"
