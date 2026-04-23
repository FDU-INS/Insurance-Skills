"""Export utilities for JSON and CSV formats."""

import csv
import json
from datetime import date
from decimal import Decimal
from io import StringIO
from typing import Any

from pydantic import BaseModel


class JSONEncoder(json.JSONEncoder):
    """Custom JSON encoder for RxMemberSim models."""

    def default(self, obj: Any) -> Any:
        if isinstance(obj, date):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, BaseModel):
            return obj.model_dump()
        if hasattr(obj, "value"):  # Enum
            return obj.value
        return super().default(obj)


def to_json(data: Any, pretty: bool = True) -> str:
    """Convert data to JSON string.

    Args:
        data: Model instance, list, or dict
        pretty: Use indentation for readability

    Returns:
        JSON string
    """
    indent = 2 if pretty else None

    if isinstance(data, BaseModel):
        return json.dumps(data.model_dump(), cls=JSONEncoder, indent=indent)
    elif isinstance(data, list):
        items = [item.model_dump() if isinstance(item, BaseModel) else item for item in data]
        return json.dumps(items, cls=JSONEncoder, indent=indent)
    else:
        return json.dumps(data, cls=JSONEncoder, indent=indent)


def to_csv(data: list[BaseModel], include_header: bool = True) -> str:
    """Convert list of models to CSV string.

    Args:
        data: List of Pydantic model instances
        include_header: Include column headers

    Returns:
        CSV string
    """
    if not data:
        return ""

    output = StringIO()

    # Get fields from first item
    first = data[0]
    fields = list(first.model_fields.keys())

    writer = csv.DictWriter(output, fieldnames=fields)

    if include_header:
        writer.writeheader()

    for item in data:
        row = {}
        for field in fields:
            value = getattr(item, field)
            if isinstance(value, date):
                row[field] = value.isoformat()
            elif isinstance(value, Decimal):
                row[field] = str(value)
            elif isinstance(value, list):
                row[field] = "|".join(str(v) for v in value)
            elif isinstance(value, BaseModel):
                row[field] = json.dumps(value.model_dump(), cls=JSONEncoder)
            elif hasattr(value, "value"):  # Enum
                row[field] = value.value
            else:
                row[field] = value
        writer.writerow(row)

    return output.getvalue()


def members_to_csv(members: list) -> str:
    """Export RxMember instances to CSV with flattened demographics.

    Args:
        members: List of RxMember instances

    Returns:
        CSV string with flattened member data
    """
    output = StringIO()

    fields = [
        "member_id",
        "cardholder_id",
        "person_code",
        "bin",
        "pcn",
        "group_number",
        "plan_code",
        "formulary_id",
        "first_name",
        "last_name",
        "date_of_birth",
        "gender",
        "address_line1",
        "city",
        "state",
        "zip_code",
        "effective_date",
        "termination_date",
        "deductible_met",
        "deductible_remaining",
        "oop_met",
        "oop_remaining",
    ]

    writer = csv.DictWriter(output, fieldnames=fields)
    writer.writeheader()

    for member in members:
        demo = member.demographics
        accum = member.accumulators

        row = {
            "member_id": member.member_id,
            "cardholder_id": member.cardholder_id,
            "person_code": member.person_code,
            "bin": member.bin,
            "pcn": member.pcn,
            "group_number": member.group_number,
            "plan_code": member.plan_code or "",
            "formulary_id": member.formulary_id or "",
            "first_name": demo.first_name,
            "last_name": demo.last_name,
            "date_of_birth": demo.date_of_birth.isoformat(),
            "gender": demo.gender,
            "address_line1": demo.address_line1 or "",
            "city": demo.city or "",
            "state": demo.state or "",
            "zip_code": demo.zip_code or "",
            "effective_date": member.effective_date.isoformat(),
            "termination_date": member.termination_date.isoformat() if member.termination_date else "",
            "deductible_met": str(accum.deductible_met),
            "deductible_remaining": str(accum.deductible_remaining),
            "oop_met": str(accum.oop_met),
            "oop_remaining": str(accum.oop_remaining),
        }
        writer.writerow(row)

    return output.getvalue()


def prescriptions_to_csv(prescriptions: list) -> str:
    """Export Prescription instances to CSV.

    Args:
        prescriptions: List of Prescription instances

    Returns:
        CSV string with prescription data
    """
    output = StringIO()

    fields = [
        "prescription_number",
        "ndc",
        "drug_name",
        "quantity_prescribed",
        "days_supply",
        "refills_authorized",
        "refills_remaining",
        "prescriber_npi",
        "prescriber_name",
        "written_date",
        "expiration_date",
        "daw_code",
        "diagnosis_codes",
        "directions",
    ]

    writer = csv.DictWriter(output, fieldnames=fields)
    writer.writeheader()

    for rx in prescriptions:
        row = {
            "prescription_number": rx.prescription_number,
            "ndc": rx.ndc,
            "drug_name": rx.drug_name,
            "quantity_prescribed": str(rx.quantity_prescribed),
            "days_supply": rx.days_supply,
            "refills_authorized": rx.refills_authorized,
            "refills_remaining": rx.refills_remaining,
            "prescriber_npi": rx.prescriber_npi,
            "prescriber_name": rx.prescriber_name or "",
            "written_date": rx.written_date.isoformat(),
            "expiration_date": rx.expiration_date.isoformat(),
            "daw_code": rx.daw_code.value if hasattr(rx.daw_code, "value") else str(rx.daw_code),
            "diagnosis_codes": "|".join(rx.diagnosis_codes),
            "directions": rx.directions or "",
        }
        writer.writerow(row)

    return output.getvalue()


def claims_to_csv(claims: list) -> str:
    """Export PharmacyClaim instances to CSV.

    Args:
        claims: List of PharmacyClaim instances

    Returns:
        CSV string with claim data
    """
    output = StringIO()

    fields = [
        "claim_id",
        "transaction_code",
        "service_date",
        "pharmacy_npi",
        "member_id",
        "cardholder_id",
        "bin",
        "pcn",
        "group_number",
        "prescription_number",
        "fill_number",
        "ndc",
        "quantity_dispensed",
        "days_supply",
        "daw_code",
        "prescriber_npi",
        "ingredient_cost_submitted",
        "dispensing_fee_submitted",
        "gross_amount_due",
        "prior_auth_number",
    ]

    writer = csv.DictWriter(output, fieldnames=fields)
    writer.writeheader()

    for claim in claims:
        row = {
            "claim_id": claim.claim_id,
            "transaction_code": claim.transaction_code.value if hasattr(claim.transaction_code, "value") else str(claim.transaction_code),
            "service_date": claim.service_date.isoformat(),
            "pharmacy_npi": claim.pharmacy_npi,
            "member_id": claim.member_id,
            "cardholder_id": claim.cardholder_id,
            "bin": claim.bin,
            "pcn": claim.pcn,
            "group_number": claim.group_number,
            "prescription_number": claim.prescription_number,
            "fill_number": claim.fill_number,
            "ndc": claim.ndc,
            "quantity_dispensed": str(claim.quantity_dispensed),
            "days_supply": claim.days_supply,
            "daw_code": claim.daw_code,
            "prescriber_npi": claim.prescriber_npi,
            "ingredient_cost_submitted": str(claim.ingredient_cost_submitted),
            "dispensing_fee_submitted": str(claim.dispensing_fee_submitted),
            "gross_amount_due": str(claim.gross_amount_due),
            "prior_auth_number": claim.prior_auth_number or "",
        }
        writer.writerow(row)

    return output.getvalue()
