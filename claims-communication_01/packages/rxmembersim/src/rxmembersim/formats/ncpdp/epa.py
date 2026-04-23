"""NCPDP ePA (Electronic Prior Authorization) transactions."""

import random
import string
import xml.etree.ElementTree as ET
from datetime import date, datetime, timedelta
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class ePAMessageType(str, Enum):
    """NCPDP ePA message types."""

    PA_INITIATION_REQUEST = "PAInitiationRequest"
    PA_INITIATION_RESPONSE = "PAInitiationResponse"
    PA_REQUEST = "PARequest"
    PA_RESPONSE = "PAResponse"
    PA_CANCEL_REQUEST = "PACancelRequest"
    PA_CANCEL_RESPONSE = "PACancelResponse"
    PA_APPEAL_REQUEST = "PAAppealRequest"
    PA_APPEAL_RESPONSE = "PAAppealResponse"


class QuestionType(str, Enum):
    """Question types for ePA questionnaires."""

    BOOLEAN = "boolean"
    TEXT = "text"
    SINGLE_SELECT = "single_select"
    MULTI_SELECT = "multi_select"
    NUMERIC = "numeric"
    DATE = "date"
    ATTACHMENT = "attachment"


class ePAQuestion(BaseModel):
    """Single question in ePA questionnaire."""

    question_id: str
    question_text: str
    question_type: QuestionType
    required: bool = True

    # Options for select questions
    options: list[str] = Field(default_factory=list)

    # Numeric constraints
    min_value: float | None = None
    max_value: float | None = None
    unit: str | None = None

    # Conditional display
    depends_on_question: str | None = None
    depends_on_answer: str | None = None

    # Help/guidance
    help_text: str | None = None


class ePAQuestionSet(BaseModel):
    """Set of questions for ePA."""

    question_set_id: str
    drug_name: str
    description: str | None = None
    questions: list[ePAQuestion]


class ePAAnswer(BaseModel):
    """Answer to an ePA question."""

    question_id: str
    answer_type: QuestionType

    boolean_answer: bool | None = None
    text_answer: str | None = None
    selected_options: list[str] = Field(default_factory=list)
    numeric_answer: float | None = None
    date_answer: str | None = None
    attachment_id: str | None = None


class PAInitiationRequest(BaseModel):
    """ePA Initiation Request (PAIREQ)."""

    message_id: str
    message_type: Literal[ePAMessageType.PA_INITIATION_REQUEST] = (
        ePAMessageType.PA_INITIATION_REQUEST
    )
    sent_time: datetime = Field(default_factory=datetime.now)

    # Initiator info
    initiator_type: str  # "pharmacy" or "prescriber"
    initiator_id: str
    pharmacy_ncpdp_id: str | None = None

    # Patient info
    patient_first_name: str
    patient_last_name: str
    patient_dob: str
    patient_gender: str
    member_id: str
    group_id: str | None = None
    bin: str | None = None
    pcn: str | None = None

    # Prescriber info
    prescriber_npi: str
    prescriber_name: str
    prescriber_phone: str | None = None
    prescriber_fax: str | None = None

    # Drug info
    drug_description: str
    ndc: str | None = None
    quantity: str
    days_supply: int
    refills_requested: int = 0

    # Clinical info
    diagnosis_codes: list[str] = Field(default_factory=list)
    urgency_indicator: str = "routine"  # routine, urgent, emergency
    notes: str | None = None


class PAInitiationResponse(BaseModel):
    """ePA Initiation Response (PAIRES)."""

    message_id: str
    relates_to_message_id: str
    message_type: Literal[ePAMessageType.PA_INITIATION_RESPONSE] = (
        ePAMessageType.PA_INITIATION_RESPONSE
    )
    sent_time: datetime = Field(default_factory=datetime.now)

    # Response info
    response_type: str  # "Approved", "Question", "Denied", "Error", "InProcess"
    pa_reference_number: str | None = None

    # Approval details
    pa_number: str | None = None
    effective_date: str | None = None
    expiration_date: str | None = None
    quantity_approved: str | None = None
    refills_approved: int | None = None

    # Question response
    question_set: ePAQuestionSet | None = None

    # Denial info
    denial_reason: str | None = None
    denial_code: str | None = None
    appeal_deadline: str | None = None
    suggested_alternatives: list[str] = Field(default_factory=list)

    # Error info
    error_code: str | None = None
    error_message: str | None = None


class PARequest(BaseModel):
    """ePA Request with answers (PAREQ)."""

    message_id: str
    relates_to_message_id: str
    message_type: Literal[ePAMessageType.PA_REQUEST] = ePAMessageType.PA_REQUEST
    sent_time: datetime = Field(default_factory=datetime.now)

    pa_reference_number: str | None = None

    # Answers to questions
    answers: list[ePAAnswer] = Field(default_factory=list)

    # Additional clinical info
    clinical_notes: str | None = None
    attachments: list[str] = Field(default_factory=list)


class PAResponse(BaseModel):
    """ePA Response with determination (PARES)."""

    message_id: str
    relates_to_message_id: str
    message_type: Literal[ePAMessageType.PA_RESPONSE] = ePAMessageType.PA_RESPONSE
    sent_time: datetime = Field(default_factory=datetime.now)

    # Determination
    determination: str  # "Approved", "Denied", "PartialApproval", "MoreInfoNeeded"
    pa_reference_number: str | None = None

    # Approval details
    pa_number: str | None = None
    effective_date: str | None = None
    expiration_date: str | None = None
    quantity_approved: str | None = None
    days_supply_approved: int | None = None
    refills_approved: int | None = None

    # Denial info
    denial_reason: str | None = None
    denial_code: str | None = None
    appeal_process: str | None = None
    appeal_deadline: str | None = None

    # More info needed
    additional_questions: ePAQuestionSet | None = None
    requested_documents: list[str] = Field(default_factory=list)

    # Alternatives
    suggested_alternatives: list[str] = Field(default_factory=list)


class PACancelRequest(BaseModel):
    """ePA Cancel Request."""

    message_id: str
    relates_to_message_id: str
    message_type: Literal[ePAMessageType.PA_CANCEL_REQUEST] = (
        ePAMessageType.PA_CANCEL_REQUEST
    )
    sent_time: datetime = Field(default_factory=datetime.now)

    pa_reference_number: str
    cancellation_reason: str


class PACancelResponse(BaseModel):
    """ePA Cancel Response."""

    message_id: str
    relates_to_message_id: str
    message_type: Literal[ePAMessageType.PA_CANCEL_RESPONSE] = (
        ePAMessageType.PA_CANCEL_RESPONSE
    )
    sent_time: datetime = Field(default_factory=datetime.now)

    pa_reference_number: str
    cancellation_status: str  # "Cancelled", "CannotCancel"
    status_reason: str | None = None


class ePAGenerator:
    """Generate ePA transactions."""

    def _generate_message_id(self) -> str:
        """Generate unique message ID."""
        return f"MSG{''.join(random.choices(string.digits, k=10))}"

    def _generate_pa_reference(self) -> str:
        """Generate PA reference number."""
        return f"REF{''.join(random.choices(string.digits, k=8))}"

    def generate_initiation_request(
        self,
        member_id: str,
        patient_first: str,
        patient_last: str,
        patient_dob: str,
        patient_gender: str,
        prescriber_npi: str,
        prescriber_name: str,
        drug_description: str,
        ndc: str,
        quantity: str,
        days_supply: int,
        diagnosis_codes: list[str] | None = None,
        urgency: str = "routine",
        initiator_type: str = "pharmacy",
        initiator_id: str = "PHARM001",
    ) -> PAInitiationRequest:
        """Generate PAInitiationRequest."""
        return PAInitiationRequest(
            message_id=self._generate_message_id(),
            initiator_type=initiator_type,
            initiator_id=initiator_id,
            patient_first_name=patient_first,
            patient_last_name=patient_last,
            patient_dob=patient_dob,
            patient_gender=patient_gender,
            member_id=member_id,
            prescriber_npi=prescriber_npi,
            prescriber_name=prescriber_name,
            drug_description=drug_description,
            ndc=ndc,
            quantity=quantity,
            days_supply=days_supply,
            diagnosis_codes=diagnosis_codes or [],
            urgency_indicator=urgency,
        )

    def generate_question_response(
        self,
        initiation: PAInitiationRequest,
        questions: ePAQuestionSet,
    ) -> PAInitiationResponse:
        """Generate response with questions."""
        return PAInitiationResponse(
            message_id=self._generate_message_id(),
            relates_to_message_id=initiation.message_id,
            response_type="Question",
            pa_reference_number=self._generate_pa_reference(),
            question_set=questions,
        )

    def generate_approval_response(
        self,
        request_message_id: str,
        pa_number: str,
        quantity_approved: str | None = None,
        days_supply_approved: int | None = None,
        refills_approved: int = 12,
        duration_days: int = 365,
    ) -> PAResponse:
        """Generate approval response."""
        return PAResponse(
            message_id=self._generate_message_id(),
            relates_to_message_id=request_message_id,
            determination="Approved",
            pa_number=pa_number,
            effective_date=date.today().isoformat(),
            expiration_date=(date.today() + timedelta(days=duration_days)).isoformat(),
            quantity_approved=quantity_approved,
            days_supply_approved=days_supply_approved,
            refills_approved=refills_approved,
        )

    def generate_denial_response(
        self,
        request_message_id: str,
        denial_reason: str,
        denial_code: str | None = None,
        alternatives: list[str] | None = None,
        appeal_days: int = 60,
    ) -> PAResponse:
        """Generate denial response."""
        return PAResponse(
            message_id=self._generate_message_id(),
            relates_to_message_id=request_message_id,
            determination="Denied",
            denial_reason=denial_reason,
            denial_code=denial_code,
            appeal_deadline=(date.today() + timedelta(days=appeal_days)).isoformat(),
            appeal_process="Submit written appeal with additional clinical documentation",
            suggested_alternatives=alternatives or [],
        )

    def generate_more_info_response(
        self,
        request_message_id: str,
        questions: ePAQuestionSet,
        requested_documents: list[str] | None = None,
    ) -> PAResponse:
        """Generate response requesting more information."""
        return PAResponse(
            message_id=self._generate_message_id(),
            relates_to_message_id=request_message_id,
            determination="MoreInfoNeeded",
            additional_questions=questions,
            requested_documents=requested_documents or [],
        )

    def generate_pa_request(
        self,
        relates_to: str,
        pa_reference: str,
        answers: list[ePAAnswer],
        clinical_notes: str | None = None,
    ) -> PARequest:
        """Generate PA request with answers."""
        return PARequest(
            message_id=self._generate_message_id(),
            relates_to_message_id=relates_to,
            pa_reference_number=pa_reference,
            answers=answers,
            clinical_notes=clinical_notes,
        )

    def to_xml(self, message: BaseModel) -> str:
        """Convert ePA message to XML format."""
        root = ET.Element("Message")
        root.set("xmlns", "http://www.ncpdp.org/schema/SCRIPT")
        root.set("version", "2017071")

        # Header
        header = ET.SubElement(root, "Header")
        ET.SubElement(header, "MessageID").text = getattr(message, "message_id", "")
        ET.SubElement(header, "SentTime").text = getattr(
            message, "sent_time", datetime.now()
        ).isoformat()

        if hasattr(message, "relates_to_message_id"):
            ET.SubElement(header, "RelatesToMessageID").text = getattr(
                message, "relates_to_message_id", ""
            )

        # Body
        body = ET.SubElement(root, "Body")
        msg_type = getattr(message, "message_type", "Unknown")
        msg_type_str = msg_type.value if hasattr(msg_type, "value") else str(msg_type)
        content = ET.SubElement(body, msg_type_str)

        # Add fields
        skip_fields = {"message_id", "sent_time", "message_type", "relates_to_message_id"}
        for field_name, value in message.model_dump().items():
            if field_name in skip_fields or value is None:
                continue

            if isinstance(value, list):
                if value:  # Only add non-empty lists
                    list_elem = ET.SubElement(content, field_name)
                    for item in value:
                        if isinstance(item, dict):
                            self._dict_to_xml(list_elem, "item", item)
                        else:
                            ET.SubElement(list_elem, "item").text = str(item)
            elif isinstance(value, dict):
                self._dict_to_xml(content, field_name, value)
            else:
                ET.SubElement(content, field_name).text = str(value)

        return ET.tostring(root, encoding="unicode")

    def _dict_to_xml(
        self, parent: ET.Element, name: str, data: dict
    ) -> ET.Element:
        """Convert dict to XML element."""
        elem = ET.SubElement(parent, name)
        for key, value in data.items():
            if value is None:
                continue
            if isinstance(value, dict):
                self._dict_to_xml(elem, key, value)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        self._dict_to_xml(elem, key, item)
                    else:
                        ET.SubElement(elem, key).text = str(item)
            else:
                ET.SubElement(elem, key).text = str(value)
        return elem
