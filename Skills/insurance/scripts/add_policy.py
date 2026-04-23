#!/usr/bin/env python3
"""Add insurance policy."""
import argparse
import uuid
from datetime import datetime

from lib.output import error, ok
from lib.schema import (
    DEFAULT_POLICIES,
    non_negative_amount,
    normalize_policy_type,
    parse_json_object,
    validate_date,
)
from lib.storage import load_json, save_json


def main() -> None:
    parser = argparse.ArgumentParser(description="Add insurance policy")
    parser.add_argument("--type", required=True, help="Policy type")
    parser.add_argument("--carrier", required=True, help="Insurance company")
    parser.add_argument("--premium", type=float, required=True, help="Annual premium")
    parser.add_argument("--renewal", default="", help="Renewal date (YYYY-MM-DD)")
    parser.add_argument("--effective-date", default="", help="Effective date (YYYY-MM-DD)")
    parser.add_argument("--expiration-date", default="", help="Expiration date (YYYY-MM-DD)")
    parser.add_argument("--policy-number", default="", help="Policy number")
    parser.add_argument("--insured-name", default="", help="Insured person or entity")
    parser.add_argument("--notes", default="", help="Free-form notes")
    parser.add_argument(
        "--coverage-limits",
        default="{}",
        help='JSON object of coverage limits, e.g. {"liability":300000}',
    )
    parser.add_argument(
        "--deductibles",
        default="{}",
        help='JSON object of deductibles, e.g. {"collision":500}',
    )

    args = parser.parse_args()

    try:
        policy_type = normalize_policy_type(args.type)
        carrier = args.carrier.strip()
        if not carrier:
            raise ValueError("carrier is required.")

        premium = non_negative_amount(args.premium, "premium")
        renewal_date = validate_date(args.renewal, "renewal")
        effective_date = validate_date(args.effective_date, "effective-date")
        expiration_date = validate_date(args.expiration_date, "expiration-date")
        coverage_limits = parse_json_object(args.coverage_limits, "coverage-limits")
        deductibles = parse_json_object(args.deductibles, "deductibles")
    except ValueError as exc:
        error(str(exc))
        return

    data = load_json("policies.json", DEFAULT_POLICIES)

    policy_id = f"POL-{str(uuid.uuid4())[:6].upper()}"
    now = datetime.now().isoformat()

    policy = {
        "id": policy_id,
        "type": policy_type,
        "carrier": carrier,
        "policy_number": args.policy_number.strip(),
        "insured_name": args.insured_name.strip(),
        "premium": premium,
        "effective_date": effective_date,
        "renewal_date": renewal_date,
        "expiration_date": expiration_date,
        "coverage_limits": coverage_limits,
        "deductibles": deductibles,
        "notes": args.notes.strip(),
        "added_at": now,
        "updated_at": now,
    }

    data["policies"].append(policy)
    save_json("policies.json", data)

    ok(
        "Policy added successfully.",
        {
            "policy_id": policy_id,
            "type": policy_type,
            "carrier": carrier,
            "premium": premium,
            "renewal_date": renewal_date,
        },
    )


if __name__ == "__main__":
    main()
