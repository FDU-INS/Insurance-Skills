#!/usr/bin/env python3
"""List stored insurance policies."""
from lib.output import ok
from lib.schema import DEFAULT_POLICIES
from lib.storage import load_json


def main() -> None:
    data = load_json("policies.json", DEFAULT_POLICIES)
    policies = data.get("policies", [])

    simplified = [
        {
            "id": p.get("id", ""),
            "type": p.get("type", ""),
            "carrier": p.get("carrier", ""),
            "premium": p.get("premium", 0),
            "renewal_date": p.get("renewal_date", ""),
        }
        for p in policies
    ]

    ok(
        "Policies loaded.",
        {
            "count": len(simplified),
            "policies": simplified,
        },
    )


if __name__ == "__main__":
    main()
