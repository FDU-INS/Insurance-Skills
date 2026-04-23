#!/usr/bin/env python3
"""Generate insurance portfolio summary."""
from collections import Counter

from lib.output import ok
from lib.schema import DEFAULT_POLICIES
from lib.storage import load_json


def main() -> None:
    data = load_json("policies.json", DEFAULT_POLICIES)
    policies = data.get("policies", [])

    total_annual_premium = sum(float(p.get("premium", 0) or 0) for p in policies)
    by_type = Counter(p.get("type", "unknown") for p in policies)

    ok(
        "Insurance summary generated.",
        {
            "total_policies": len(policies),
            "total_annual_premium": round(total_annual_premium, 2),
            "policies_by_type": dict(by_type),
        },
    )


if __name__ == "__main__":
    main()
