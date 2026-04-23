"""Healthcare claim model."""

from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field


class ClaimLine(BaseModel):
    """Individual service line within a claim."""

    model_config = {"frozen": True}

    line_number: int = Field(..., description="Sequence within claim")
    procedure_code: str = Field(..., description="CPT/HCPCS code")
    procedure_modifiers: list[str] = Field(default_factory=list, description="Modifier codes")
    service_date: date = Field(..., description="Date of this service")
    units: Decimal = Field(Decimal("1"), description="Quantity of service")
    charge_amount: Decimal = Field(..., description="Billed amount")
    diagnosis_pointers: list[int] = Field(
        default_factory=lambda: [1], description="Which diagnoses apply"
    )
    revenue_code: str | None = Field(None, description="Revenue code (institutional)")
    ndc_code: str | None = Field(None, description="Drug code (if applicable)")
    place_of_service: str = Field("11", description="Place of service code")


class Claim(BaseModel):
    """Healthcare claim with service details."""

    model_config = {"frozen": True}

    claim_id: str = Field(..., description="Unique claim identifier")
    claim_type: str = Field("PROFESSIONAL", description="PROFESSIONAL, INSTITUTIONAL, DENTAL, RX")

    # Member and subscriber
    member_id: str = Field(..., description="Member receiving service")
    subscriber_id: str = Field(..., description="Subscriber on policy")

    # Providers
    provider_npi: str = Field(..., description="Rendering provider NPI")
    facility_npi: str | None = Field(None, description="Facility NPI (for institutional)")

    # Dates
    service_date: date = Field(..., description="Date of service (or admission)")
    admission_date: date | None = Field(None, description="Admission date (inpatient)")
    discharge_date: date | None = Field(None, description="Discharge date (inpatient)")

    # Service details
    place_of_service: str = Field("11", description="POS code: 11=Office, 21=Inpatient, etc.")
    claim_lines: list[ClaimLine] = Field(default_factory=list, description="Service line details")

    # Diagnosis
    principal_diagnosis: str = Field(..., description="Primary ICD-10 code")
    other_diagnoses: list[str] = Field(default_factory=list, description="Secondary diagnoses")

    # Prior auth
    authorization_number: str | None = Field(None, description="Prior auth reference")

    @property
    def total_charge(self) -> Decimal:
        """Calculate total billed amount from all lines."""
        return sum(line.charge_amount * line.units for line in self.claim_lines)

    @property
    def line_count(self) -> int:
        """Get number of service lines."""
        return len(self.claim_lines)

    @property
    def all_diagnoses(self) -> list[str]:
        """Get all diagnoses (principal + other)."""
        return [self.principal_diagnosis] + self.other_diagnoses
