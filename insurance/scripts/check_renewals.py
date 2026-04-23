#!/usr/bin/env python3
"""Check upcoming policy renewals."""
import argparse
from datetime import datetime, timedelta

from lib.output import ok, error
from lib.schema import DEFAULT_POLICIES
from lib.storage import load_json


def main() -> None:
    parser = argparse.ArgumentParser(description="Check upcoming renewals")
    parser.add_argument("--days", type=int, default=60, help="Look-ahead window in days")
    args = parser.parse_args()

    if args.days < 0:
        error("days must be non-negative.")
        return

    data = load_json("policies.json", DEFAULT_POLICIES)
    policies = data.get("policies", [])

    today = datetime.today().date()
    end_date = today + timedelta(days=args.days)

    upcoming = []
    for policy in policies:
        renewal = policy.get("renewal_date", "")
        if not renewal:
            continue
        try:
            renewal_date = datetime.strptime(renewal, "%Y-%m-%d").date()
        except ValueError:
            continue

        if today <= renewal_date <= end_date:
            upcoming.append(
                {
                    "id": policy.get("id", ""),
                    "type": policy.get("type", ""),
                    "carrier": policy.get("carrier", ""),
                    "renewal_date": renewal,
                    "days_until": (renewal_date - today).days,
                }
            )

    ok(
        "Renewal check completed.",
        {
            "days_checked": args.days,
            "count": len(upcoming),
            "renewals": sorted(upcoming, key=lambda x: x["renewal_date"]),
        },
    )


if __name__ == "__main__":
    main()
