"""Pharmacy claim response model."""
from decimal import Decimal

from pydantic import BaseModel, Field


class RejectCode(BaseModel):
    """NCPDP reject code."""

    code: str
    description: str


class DURAlert(BaseModel):
    """Drug Utilization Review alert."""

    reason_for_service: str
    clinical_significance: str
    other_pharmacy_indicator: str | None = None
    previous_fill_date: str | None = None
    quantity_of_previous_fill: Decimal | None = None
    database_indicator: str | None = None
    other_prescriber_indicator: str | None = None
    message: str | None = None


class ClaimResponse(BaseModel):
    """Response to pharmacy claim."""

    claim_id: str
    transaction_response_status: str  # A=Accepted, R=Rejected, C=Captured, D=Duplicate
    response_status: str  # P=Paid, R=Rejected, D=Duplicate

    # Authorization
    authorization_number: str | None = None

    # Reject codes (if rejected)
    reject_codes: list[RejectCode] = Field(default_factory=list)

    # Pricing (if approved)
    ingredient_cost_paid: Decimal | None = None
    dispensing_fee_paid: Decimal | None = None
    flat_sales_tax_paid: Decimal | None = None
    percentage_sales_tax_paid: Decimal | None = None
    incentive_amount_paid: Decimal | None = None
    total_amount_paid: Decimal | None = None

    # Patient responsibility
    patient_pay_amount: Decimal | None = None
    copay_amount: Decimal | None = None
    coinsurance_amount: Decimal | None = None
    deductible_amount: Decimal | None = None

    # Accumulators
    amount_applied_to_deductible: Decimal | None = None
    remaining_deductible: Decimal | None = None
    remaining_oop: Decimal | None = None

    # DUR alerts
    dur_alerts: list[DURAlert] = Field(default_factory=list)

    # Messaging
    message: str | None = None
    additional_message: str | None = None
