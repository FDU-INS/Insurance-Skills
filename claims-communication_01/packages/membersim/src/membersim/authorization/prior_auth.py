"""Prior authorization model and workflows."""

from datetime import date

from pydantic import BaseModel, Field


class AuthorizationStatus:
    """Authorization status constants."""

    PENDING = "PENDING"
    APPROVED = "APPROVED"
    DENIED = "DENIED"
    MODIFIED = "MODIFIED"
    CANCELLED = "CANCELLED"


class Authorization(BaseModel):
    """Prior authorization request and decision."""

    auth_number: str = Field(..., description="Unique authorization ID")
    member_id: str = Field(..., description="Member reference")
    provider_npi: str = Field(..., description="Requesting provider NPI")

    service_type: str = Field(..., description="INPATIENT, OUTPATIENT, DME, RX, BEHAVIORAL")
    procedure_codes: list[str] = Field(default_factory=list, description="Requested CPT/HCPCS")
    diagnosis_codes: list[str] = Field(default_factory=list, description="Supporting diagnoses")

    request_date: date = Field(..., description="Date auth was requested")
    decision_date: date | None = Field(None, description="Date decision was made")

    status: str = Field(AuthorizationStatus.PENDING, description="Current status")

    # Approval details
    approved_units: int | None = Field(None, description="Units/days approved")
    effective_start: date | None = Field(None, description="Auth valid from")
    effective_end: date | None = Field(None, description="Auth valid through")

    # Denial details
    denial_reason: str | None = Field(None, description="Reason for denial")
    denial_code: str | None = Field(None, description="Denial reason code")

    review_type: str = Field("PROSPECTIVE", description="PROSPECTIVE, CONCURRENT, RETROSPECTIVE")
    urgency: str = Field("STANDARD", description="STANDARD, EXPEDITED, URGENT")

    @property
    def is_approved(self) -> bool:
        """Check if authorization is approved."""
        return self.status == AuthorizationStatus.APPROVED

    @property
    def is_pending(self) -> bool:
        """Check if authorization is pending."""
        return self.status == AuthorizationStatus.PENDING

    @property
    def is_valid(self) -> bool:
        """Check if authorization is currently valid."""
        if not self.is_approved:
            return False
        today = date.today()
        if self.effective_start and today < self.effective_start:
            return False
        return not (self.effective_end and today > self.effective_end)


# Common denial reasons
DENIAL_REASONS: dict[str, str] = {
    "MNC": "Medical necessity criteria not met",
    "INFO": "Insufficient information to make determination",
    "DUP": "Duplicate request",
    "EXCL": "Service not covered under member's plan",
    "NETW": "Out-of-network provider",
    "FREQ": "Service frequency exceeded",
    "EXP": "Prior authorization expired",
}


# Services typically requiring prior auth
PRIOR_AUTH_REQUIRED: dict[str, list[str]] = {
    "INPATIENT": ["elective admission", "skilled nursing", "rehab"],
    "OUTPATIENT": ["MRI", "CT scan", "PET scan", "advanced imaging"],
    "DME": ["CPAP", "wheelchair", "prosthetics"],
    "RX": ["specialty drugs", "biologics", "step therapy override"],
    "BEHAVIORAL": ["inpatient psych", "residential treatment", "intensive outpatient"],
}
