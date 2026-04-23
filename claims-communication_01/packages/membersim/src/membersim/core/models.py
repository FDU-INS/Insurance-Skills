"""Core models for health plan member data.

This module defines member-specific models that extend or complement
healthsim-core's base models for health plan/insurance use cases.
"""

from datetime import date
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, Field


class CoverageType(str, Enum):
    """Types of health coverage."""

    MEDICAL = "medical"
    DENTAL = "dental"
    VISION = "vision"
    PHARMACY = "pharmacy"


class ClaimStatus(str, Enum):
    """Status of a claim."""

    SUBMITTED = "submitted"
    PENDING = "pending"
    APPROVED = "approved"
    DENIED = "denied"
    PAID = "paid"


class Member(BaseModel):
    """Health plan member.

    Represents an individual enrolled in a health plan. This model
    focuses on insurance/administrative data rather than clinical data.

    Example:
        >>> member = Member(
        ...     member_id="M12345",
        ...     given_name="John",
        ...     family_name="Doe",
        ...     birth_date=date(1980, 1, 15),
        ...     gender="M",
        ...     subscriber_id="S98765"
        ... )
    """

    member_id: str = Field(..., description="Unique member identifier")
    subscriber_id: str = Field(..., description="Subscriber/policyholder ID")

    # Demographics (from Person)
    given_name: str = Field(..., description="First name")
    family_name: str = Field(..., description="Last name")
    birth_date: date = Field(..., description="Date of birth")
    gender: str = Field(..., description="M/F/O/U")

    # Contact
    street_address: str | None = Field(None, description="Street address")
    city: str | None = Field(None, description="City")
    state: str | None = Field(None, description="State")
    postal_code: str | None = Field(None, description="Postal code")
    phone: str | None = Field(None, description="Phone number")
    email: str | None = Field(None, description="Email address")

    # Plan info
    group_number: str | None = Field(None, description="Employer group number")
    plan_code: str | None = Field(None, description="Plan identifier")

    @property
    def full_name(self) -> str:
        """Get full name."""
        return f"{self.given_name} {self.family_name}"

    @property
    def age(self) -> int:
        """Calculate current age."""
        today = date.today()
        return (
            today.year
            - self.birth_date.year
            - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        )


class Coverage(BaseModel):
    """Coverage period for a member.

    Represents active coverage under a health plan.
    """

    coverage_id: str = Field(..., description="Coverage identifier")
    member_id: str = Field(..., description="Member this coverage is for")
    coverage_type: CoverageType = Field(..., description="Type of coverage")

    start_date: date = Field(..., description="Coverage start date")
    end_date: date | None = Field(None, description="Coverage end date (None = active)")

    plan_name: str | None = Field(None, description="Plan name")
    network: str | None = Field(None, description="Network (HMO, PPO, etc.)")

    deductible: Decimal | None = Field(None, description="Annual deductible")
    copay: Decimal | None = Field(None, description="Standard copay amount")

    @property
    def is_active(self) -> bool:
        """Check if coverage is currently active."""
        today = date.today()
        if self.end_date:
            return self.start_date <= today <= self.end_date
        return self.start_date <= today


class Enrollment(BaseModel):
    """Enrollment record for a member.

    Tracks when a member enrolled/disenrolled from a plan.
    """

    enrollment_id: str = Field(..., description="Enrollment record ID")
    member_id: str = Field(..., description="Member ID")

    enrollment_date: date = Field(..., description="Date enrolled")
    disenrollment_date: date | None = Field(None, description="Date disenrolled")
    reason_code: str | None = Field(None, description="Enrollment/disenrollment reason")


class ClaimLine(BaseModel):
    """Individual line item on a claim."""

    line_number: int = Field(..., description="Line number")
    procedure_code: str = Field(..., description="CPT/HCPCS code")
    diagnosis_code: str | None = Field(None, description="ICD-10 code")

    quantity: int = Field(1, description="Units/quantity")
    billed_amount: Decimal = Field(..., description="Amount billed")
    allowed_amount: Decimal | None = Field(None, description="Amount allowed")
    paid_amount: Decimal | None = Field(None, description="Amount paid")


class Claim(BaseModel):
    """Health insurance claim.

    Represents a claim submitted for payment.
    """

    claim_id: str = Field(..., description="Unique claim identifier")
    member_id: str = Field(..., description="Member ID")

    service_date: date = Field(..., description="Date of service")
    submission_date: date = Field(..., description="Date claim submitted")

    provider_npi: str | None = Field(None, description="Provider NPI")
    provider_name: str | None = Field(None, description="Provider name")
    facility_name: str | None = Field(None, description="Facility name")

    status: ClaimStatus = Field(ClaimStatus.SUBMITTED, description="Claim status")
    claim_type: str | None = Field(None, description="Professional/Institutional")

    total_billed: Decimal = Field(..., description="Total billed amount")
    total_allowed: Decimal | None = Field(None, description="Total allowed amount")
    total_paid: Decimal | None = Field(None, description="Total paid amount")
    member_responsibility: Decimal | None = Field(None, description="Member owes")

    lines: list[ClaimLine] = Field(default_factory=list, description="Claim lines")
