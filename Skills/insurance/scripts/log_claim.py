#!/usr/bin/env python3
"""Log an insurance claim or incident record."""
import argparse
import uuid
from datetime import datetime

from lib.output import error, ok
from lib.schema import DEFAULT_CLAIMS, validate_date
from lib.storage import load_json, save_json


def main() -> None:
    parser = argparse.ArgumentParser(description="Log claim or incident")
    parser.add_argument("--policy-id", required=True, help="Policy ID related to the claim")
    parser.add_argument("--incident", required=True, help="Incident type or short description")
    parser.add_argument("--date", required=True, help="Incident date (YYYY-MM-DD)")
    parser.add_argument("--status", default="logged", help="Claim status")
    parser.add_argument("--notes", default="", help="Additional notes")

    args = parser.parse_args()

    try:
        incident_date = validate_date(args.date, "date")
    except ValueError as exc:
        error(str(exc))
        return

    data = load_json("claims.json", DEFAULT_CLAIMS)
    claim_id = f"CLM-{str(uuid.uuid4())[:6].upper()}"

    claim = {
        "id": claim_id,
        "policy_id": args.policy_id.strip(),
        "incident": args.incident.strip(),
        "incident_date": incident_date,
        "status": args.status.strip() or "logged",
        "notes": args.notes.strip(),
        "logged_at": datetime.now().isoformat(),
    }

    data["claims"].append(claim)
    save_json("claims.json", data)

    ok(
        "Claim event logged successfully.",
        {
            "claim_id": claim_id,
            "policy_id": claim["policy_id"],
            "incident_date": incident_date,
            "status": claim["status"],
        },
    )


if __name__ == "__main__":
    main()
