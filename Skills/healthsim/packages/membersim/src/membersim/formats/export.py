"""Export utilities for JSON and CSV formats."""

import csv
import json
from datetime import date
from decimal import Decimal
from io import StringIO
from typing import Any

from pydantic import BaseModel


class JSONEncoder(json.JSONEncoder):
    """Custom JSON encoder for MemberSim models."""

    def default(self, obj: Any) -> Any:
        if isinstance(obj, date):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, BaseModel):
            return obj.model_dump()
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
            else:
                row[field] = value
        writer.writerow(row)

    return output.getvalue()


def members_to_csv(members: list) -> str:
    """Export members to CSV with flattened demographics."""
    output = StringIO()

    fields = [
        "member_id",
        "subscriber_id",
        "plan_code",
        "group_id",
        "first_name",
        "last_name",
        "date_of_birth",
        "gender",
        "street",
        "city",
        "state",
        "zip_code",
        "coverage_start",
        "coverage_end",
        "is_active",
    ]

    writer = csv.DictWriter(output, fieldnames=fields)
    writer.writeheader()

    for member in members:
        # Handle both old demographics-based and new Person-based Member
        if hasattr(member, "demographics"):
            demo = member.demographics
            addr = demo.address
            first_name = demo.first_name
            last_name = demo.last_name
            dob = demo.date_of_birth
            gender = demo.gender
        else:
            # New Member extends Person directly
            first_name = member.name.given_name
            last_name = member.name.family_name
            dob = member.birth_date
            gender = member.gender.value if hasattr(member.gender, "value") else str(member.gender)
            addr = member.address

        row = {
            "member_id": member.member_id,
            "subscriber_id": getattr(member, "subscriber_id", member.member_id),
            "plan_code": member.plan_code,
            "group_id": member.group_id,
            "first_name": first_name,
            "last_name": last_name,
            "date_of_birth": dob.isoformat(),
            "gender": gender,
            "street": addr.street_address if addr else "",
            "city": addr.city if addr else "",
            "state": addr.state if addr else "",
            "zip_code": addr.postal_code if addr else "",
            "coverage_start": member.coverage_start.isoformat(),
            "coverage_end": member.coverage_end.isoformat() if member.coverage_end else "",
            "is_active": member.is_active,
        }
        writer.writerow(row)

    return output.getvalue()


def claims_to_csv(claims: list) -> str:
    """Export claims to CSV."""
    output = StringIO()

    fields = [
        "claim_id",
        "member_id",
        "subscriber_id",
        "provider_npi",
        "service_date",
        "claim_type",
        "place_of_service",
        "principal_diagnosis",
        "total_charge",
        "status",
    ]

    writer = csv.DictWriter(output, fieldnames=fields)
    writer.writeheader()

    for claim in claims:
        row = {
            "claim_id": claim.claim_id,
            "member_id": claim.member_id,
            "subscriber_id": claim.subscriber_id,
            "provider_npi": claim.provider_npi,
            "service_date": claim.service_date.isoformat(),
            "claim_type": claim.claim_type,
            "place_of_service": claim.place_of_service,
            "principal_diagnosis": claim.principal_diagnosis,
            "total_charge": str(claim.total_charge),
            "status": claim.status,
        }
        writer.writerow(row)

    return output.getvalue()
