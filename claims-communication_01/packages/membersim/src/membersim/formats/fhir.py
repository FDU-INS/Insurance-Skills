"""FHIR R4 resource generation."""

from typing import Any

from membersim.core.member import Member
from membersim.core.plan import Plan


def member_to_fhir_coverage(member: Member, plan: Plan | None = None) -> dict[str, Any]:
    """Generate FHIR R4 Coverage resource from member.

    Args:
        member: Member instance
        plan: Optional Plan for additional details

    Returns:
        FHIR Coverage resource as dict
    """
    subscriber_id = getattr(member, "subscriber_id", member.member_id)

    resource: dict[str, Any] = {
        "resourceType": "Coverage",
        "id": member.member_id,
        "status": "active" if member.is_active else "cancelled",
        "type": {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
                    "code": "EHCPOL",
                    "display": "extended healthcare",
                }
            ]
        },
        "subscriber": {
            "reference": f"Patient/{subscriber_id}",
        },
        "beneficiary": {
            "reference": f"Patient/{member.member_id}",
        },
        "relationship": {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/subscriber-relationship",
                    "code": _relationship_to_fhir(member.relationship_code),
                }
            ]
        },
        "period": {
            "start": member.coverage_start.isoformat(),
        },
        "payor": [
            {
                "display": "Health Plan",
            }
        ],
        "class": [
            {
                "type": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/coverage-class",
                            "code": "plan",
                        }
                    ]
                },
                "value": member.plan_code,
            },
            {
                "type": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/coverage-class",
                            "code": "group",
                        }
                    ]
                },
                "value": member.group_id,
            },
        ],
    }

    if member.coverage_end:
        resource["period"]["end"] = member.coverage_end.isoformat()

    # Add plan details if provided
    if plan:
        resource["class"].append(
            {
                "type": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/coverage-class",
                            "code": "subplan",
                        }
                    ]
                },
                "value": plan.plan_type,
                "name": plan.plan_name,
            }
        )

    return resource


def member_to_fhir_patient(member: Member) -> dict[str, Any]:
    """Generate FHIR R4 Patient resource from member demographics.

    Args:
        member: Member instance

    Returns:
        FHIR Patient resource as dict
    """
    # Handle both old demographics-based and new Person-based Member
    if hasattr(member, "demographics"):
        demo = member.demographics
        first_name = demo.first_name
        last_name = demo.last_name
        dob = demo.date_of_birth
        gender = demo.gender
        ssn = demo.ssn
        addr = demo.address
    else:
        # New Member extends Person directly
        first_name = member.name.given_name
        last_name = member.name.family_name
        dob = member.birth_date
        gender = member.gender.value if hasattr(member.gender, "value") else str(member.gender)
        ssn = None
        addr = member.address

    resource: dict[str, Any] = {
        "resourceType": "Patient",
        "id": member.member_id,
        "identifier": [
            {
                "system": "http://healthplan.example.org/member-id",
                "value": member.member_id,
            }
        ],
        "name": [
            {
                "use": "official",
                "family": last_name,
                "given": [first_name],
            }
        ],
        "gender": "male" if gender in ("M", "male", "MALE") else "female",
        "birthDate": dob.isoformat(),
    }

    if ssn:
        resource["identifier"].append(
            {
                "system": "http://hl7.org/fhir/sid/us-ssn",
                "value": ssn,
            }
        )

    if addr:
        resource["address"] = [
            {
                "use": "home",
                "line": [addr.street_address],
                "city": addr.city,
                "state": addr.state,
                "postalCode": addr.postal_code,
                "country": "US",
            }
        ]

    return resource


def _relationship_to_fhir(code: str) -> str:
    """Convert X12 relationship code to FHIR."""
    mapping = {
        "18": "self",
        "01": "spouse",
        "19": "child",
        "20": "employee",
        "21": "unknown",
        "G8": "other",
    }
    return mapping.get(code, "other")


def create_fhir_bundle(
    resources: list[dict[str, Any]], bundle_type: str = "collection"
) -> dict[str, Any]:
    """Create FHIR Bundle containing multiple resources.

    Args:
        resources: List of FHIR resources
        bundle_type: collection, batch, transaction, etc.

    Returns:
        FHIR Bundle resource
    """
    return {
        "resourceType": "Bundle",
        "type": bundle_type,
        "total": len(resources),
        "entry": [{"resource": r} for r in resources],
    }
