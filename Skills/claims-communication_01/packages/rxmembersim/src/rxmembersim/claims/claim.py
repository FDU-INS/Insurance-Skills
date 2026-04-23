"""Pharmacy claim model."""
from datetime import date
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel


class TransactionCode(str, Enum):
    """NCPDP transaction codes."""

    BILLING = "B1"
    REVERSAL = "B2"
    REBILL = "B3"


class PharmacyClaim(BaseModel):
    """Pharmacy claim for adjudication."""

    claim_id: str
    transaction_code: TransactionCode
    service_date: date

    # Pharmacy
    pharmacy_npi: str
    pharmacy_ncpdp: str | None = None

    # Member
    member_id: str
    cardholder_id: str
    person_code: str
    bin: str
    pcn: str
    group_number: str

    # Prescription
    prescription_number: str
    fill_number: int
    ndc: str
    quantity_dispensed: Decimal
    days_supply: int
    daw_code: str
    compound_code: str = "0"  # 0=not compound, 1=compound, 2=compound with special rules

    # Prescriber
    prescriber_npi: str

    # Pricing submitted
    ingredient_cost_submitted: Decimal
    dispensing_fee_submitted: Decimal
    usual_customary_charge: Decimal
    gross_amount_due: Decimal

    # Prior authorization
    prior_auth_number: str | None = None
    prior_auth_type: str | None = None

    # DUR/PPS
    dur_pps_code_counter: int = 0
    dur_reason_for_service: str | None = None
    dur_professional_service: str | None = None
    dur_result_of_service: str | None = None
