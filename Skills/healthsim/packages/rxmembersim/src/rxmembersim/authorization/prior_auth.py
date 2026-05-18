"""Prior authorization models and workflows."""

import random
import string
from datetime import date, datetime, timedelta
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, Field


class PAStatus(str, Enum):
    """Prior authorization status."""

    PENDING = "pending"
    APPROVED = "approved"
    DENIED = "denied"
    PARTIAL = "partial"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


class PARequestType(str, Enum):
    """Type of PA request."""

    NEW = "new"
    RENEWAL = "renewal"
    APPEAL = "appeal"
    EXPEDITED = "expedited"


class PADenialReason(str, Enum):
    """Reason for PA denial."""

    CRITERIA_NOT_MET = "criteria_not_met"
    STEP_THERAPY_REQUIRED = "step_therapy"
    ALTERNATIVE_AVAILABLE = "alternative_available"
    QUANTITY_EXCEEDS_LIMIT = "quantity_exceeds"
    NOT_MEDICALLY_NECESSARY = "not_medically_necessary"
    DOCUMENTATION_INSUFFICIENT = "insufficient_docs"
    DIAGNOSIS_NOT_COVERED = "diagnosis_not_covered"


class PriorAuthRequest(BaseModel):
    """Prior authorization request."""

    pa_request_id: str
    request_type: PARequestType = PARequestType.NEW
    request_date: datetime = Field(default_factory=datetime.now)
    urgency: str = "routine"  # routine, urgent, emergency

    # Member info
    member_id: str
    cardholder_id: str

    # Drug info
    ndc: str
    drug_name: str
    quantity_requested: Decimal
    days_supply_requested: int

    # Prescriber info
    prescriber_npi: str
    prescriber_name: str
    prescriber_phone: str | None = None
    prescriber_fax: str | None = None
    prescriber_specialty: str | None = None

    # Clinical info
    diagnosis_codes: list[str] = Field(default_factory=list)
    clinical_notes: str | None = None
    previous_therapies: list[str] = Field(default_factory=list)
    reason_for_request: str | None = None

    # Lab results
    lab_results: dict[str, float] = Field(default_factory=dict)

    # Attachments
    has_attachments: bool = False
    attachment_types: list[str] = Field(default_factory=list)


class PriorAuthResponse(BaseModel):
    """Prior authorization response."""

    pa_request_id: str
    pa_number: str | None = None
    response_date: datetime = Field(default_factory=datetime.now)
    status: PAStatus

    # Approval details
    effective_date: date | None = None
    expiration_date: date | None = None
    quantity_approved: Decimal | None = None
    days_supply_approved: int | None = None
    refills_approved: int | None = None

    # Denial details
    denial_reason: PADenialReason | None = None
    denial_message: str | None = None
    suggested_alternatives: list[str] = Field(default_factory=list)

    # Appeal info
    appeal_deadline: date | None = None
    appeal_instructions: str | None = None

    # Processing info
    reviewed_by: str | None = None
    auto_approved: bool = False


class PriorAuthRecord(BaseModel):
    """Complete PA record with request and response."""

    request: PriorAuthRequest
    response: PriorAuthResponse | None = None
    status_history: list[dict] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class PriorAuthWorkflow:
    """Prior authorization workflow engine."""

    def __init__(self) -> None:
        self.records: dict[str, PriorAuthRecord] = {}

    def create_request(
        self,
        member_id: str,
        cardholder_id: str,
        ndc: str,
        drug_name: str,
        quantity: Decimal,
        days_supply: int,
        prescriber_npi: str,
        prescriber_name: str,
        diagnosis_codes: list[str] | None = None,
        urgency: str = "routine",
        previous_therapies: list[str] | None = None,
        prescriber_specialty: str | None = None,
        lab_results: dict[str, float] | None = None,
    ) -> PriorAuthRequest:
        """Create a new PA request."""
        request = PriorAuthRequest(
            pa_request_id=self._generate_request_id(),
            member_id=member_id,
            cardholder_id=cardholder_id,
            ndc=ndc,
            drug_name=drug_name,
            quantity_requested=quantity,
            days_supply_requested=days_supply,
            prescriber_npi=prescriber_npi,
            prescriber_name=prescriber_name,
            diagnosis_codes=diagnosis_codes or [],
            urgency=urgency,
            previous_therapies=previous_therapies or [],
            prescriber_specialty=prescriber_specialty,
            lab_results=lab_results or {},
        )

        # Store the record
        self.records[request.pa_request_id] = PriorAuthRecord(
            request=request,
            status_history=[
                {
                    "status": PAStatus.PENDING.value,
                    "timestamp": datetime.now().isoformat(),
                    "note": "Request created",
                }
            ],
        )

        return request

    def check_auto_approval(
        self, request: PriorAuthRequest
    ) -> PriorAuthResponse | None:
        """Check if request qualifies for auto-approval."""
        # Auto-approve emergency requests
        if request.urgency == "emergency":
            return self.approve(request, auto=True, duration_days=30)

        # Auto-approve renewals with good history
        if request.request_type == PARequestType.RENEWAL:
            return self.approve(request, auto=True)

        return None

    def approve(
        self,
        request: PriorAuthRequest,
        auto: bool = False,
        duration_days: int = 365,
        quantity: Decimal | None = None,
        days_supply: int | None = None,
        refills: int = 12,
        reviewed_by: str | None = None,
    ) -> PriorAuthResponse:
        """Approve a PA request."""
        response = PriorAuthResponse(
            pa_request_id=request.pa_request_id,
            pa_number=self._generate_pa_number(),
            status=PAStatus.APPROVED,
            effective_date=date.today(),
            expiration_date=date.today() + timedelta(days=duration_days),
            quantity_approved=quantity or request.quantity_requested,
            days_supply_approved=days_supply or request.days_supply_requested,
            refills_approved=refills,
            auto_approved=auto,
            reviewed_by=reviewed_by or ("AUTO" if auto else None),
        )

        self._update_record(request.pa_request_id, response)
        return response

    def deny(
        self,
        request: PriorAuthRequest,
        reason: PADenialReason,
        message: str | None = None,
        alternatives: list[str] | None = None,
        reviewed_by: str | None = None,
    ) -> PriorAuthResponse:
        """Deny a PA request."""
        response = PriorAuthResponse(
            pa_request_id=request.pa_request_id,
            status=PAStatus.DENIED,
            denial_reason=reason,
            denial_message=message or f"Denied: {reason.value}",
            suggested_alternatives=alternatives or [],
            appeal_deadline=date.today() + timedelta(days=60),
            appeal_instructions="Submit appeal with additional clinical documentation "
            "to the PA department. Include relevant lab results, clinical notes, "
            "and documentation of previous therapy failures.",
            reviewed_by=reviewed_by,
        )

        self._update_record(request.pa_request_id, response)
        return response

    def partial_approve(
        self,
        request: PriorAuthRequest,
        quantity: Decimal,
        days_supply: int,
        duration_days: int = 90,
        reason: str | None = None,
        reviewed_by: str | None = None,
    ) -> PriorAuthResponse:
        """Partially approve a PA request with modified terms."""
        response = PriorAuthResponse(
            pa_request_id=request.pa_request_id,
            pa_number=self._generate_pa_number(),
            status=PAStatus.PARTIAL,
            effective_date=date.today(),
            expiration_date=date.today() + timedelta(days=duration_days),
            quantity_approved=quantity,
            days_supply_approved=days_supply,
            refills_approved=3,
            denial_message=reason or "Approved with modifications",
            reviewed_by=reviewed_by,
        )

        self._update_record(request.pa_request_id, response)
        return response

    def get_record(self, pa_request_id: str) -> PriorAuthRecord | None:
        """Get a PA record by request ID."""
        return self.records.get(pa_request_id)

    def check_existing_auth(
        self,
        member_id: str,
        ndc: str,
        service_date: date | None = None,
    ) -> PriorAuthResponse | None:
        """Check if member has existing valid authorization for drug."""
        check_date = service_date or date.today()

        for record in self.records.values():
            if record.request.member_id != member_id:
                continue
            if record.request.ndc != ndc:
                continue
            if not record.response:
                continue
            if record.response.status != PAStatus.APPROVED:
                continue
            if not record.response.effective_date:
                continue
            if not record.response.expiration_date:
                continue

            if (
                record.response.effective_date
                <= check_date
                <= record.response.expiration_date
            ):
                return record.response

        return None

    def _update_record(
        self, pa_request_id: str, response: PriorAuthResponse
    ) -> None:
        """Update PA record with response."""
        if pa_request_id in self.records:
            record = self.records[pa_request_id]
            record.response = response
            record.status_history.append(
                {
                    "status": response.status.value,
                    "timestamp": datetime.now().isoformat(),
                    "note": f"Status changed to {response.status.value}",
                }
            )

    def _generate_request_id(self) -> str:
        """Generate unique PA request ID."""
        date_part = datetime.now().strftime("%Y%m%d")
        random_part = "".join(random.choices(string.digits, k=6))
        return f"PA-{date_part}-{random_part}"

    def _generate_pa_number(self) -> str:
        """Generate unique PA number."""
        return f"AUTH{''.join(random.choices(string.digits, k=9))}"
