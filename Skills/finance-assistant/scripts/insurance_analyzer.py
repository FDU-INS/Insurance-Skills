"""
Finance Assistant Insurance Analyzer.

Track insurance policies, analyze coverage, and flag renewal dates.
"""

from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import Optional

try:
    from finance_storage import get_insurance_path, load_json, save_json
    from currency import format_money
except ImportError:
    import os, sys
    sys.path.insert(0, os.path.dirname(__file__))
    from finance_storage import get_insurance_path, load_json, save_json
    from currency import format_money


POLICY_TYPES = {
    "health":        "Health Insurance",
    "life":          "Life Insurance",
    "disability":    "Disability Insurance",
    "liability":     "Personal Liability",
    "home":          "Home / Renters Insurance",
    "car":           "Car Insurance",
    "legal":         "Legal Insurance",
    "travel":        "Travel Insurance",
    "pet":           "Pet Insurance",
    "dental":        "Dental Insurance",
    "long_term_care":"Long-term Care Insurance",
    "other":         "Other Insurance",
}

ESSENTIAL_TYPES = {"health", "liability", "disability", "home"}


def _load_policies() -> list[dict]:
    data = load_json(get_insurance_path(), default={"policies": []})
    return data.get("policies", []) if isinstance(data, dict) else []


def _save_policies(policies: list[dict]) -> None:
    save_json(get_insurance_path(), {
        "last_updated": datetime.now().isoformat(),
        "policies": policies,
    })


def get_policies() -> list[dict]:
    return _load_policies()


def add_policy(policy_data: dict) -> dict:
    policies = _load_policies()
    policy = {
        "id": policy_data.get("id") or str(uuid.uuid4())[:8],
        "type": policy_data.get("type", "other"),
        "provider": policy_data.get("provider", ""),
        "name": policy_data.get("name", ""),
        "annual_premium": float(policy_data.get("annual_premium", 0)),
        "monthly_premium": float(policy_data.get("monthly_premium", 0)),
        "coverage_amount": float(policy_data.get("coverage_amount", 0)),
        "deductible": float(policy_data.get("deductible", 0)),
        "currency": policy_data.get("currency", "EUR"),
        "renewal_date": policy_data.get("renewal_date"),
        "status": "active",
        "notes": policy_data.get("notes", ""),
    }
    # Auto-calculate monthly from annual or vice versa
    if policy["annual_premium"] and not policy["monthly_premium"]:
        policy["monthly_premium"] = round(policy["annual_premium"] / 12, 2)
    elif policy["monthly_premium"] and not policy["annual_premium"]:
        policy["annual_premium"] = round(policy["monthly_premium"] * 12, 2)

    policies.append(policy)
    _save_policies(policies)
    return policy


def update_policy(policy_id: str, updates: dict) -> Optional[dict]:
    policies = _load_policies()
    for i, p in enumerate(policies):
        if p["id"] == policy_id:
            p.update(updates)
            policies[i] = p
            _save_policies(policies)
            return p
    return None


def delete_policy(policy_id: str) -> bool:
    policies = _load_policies()
    filtered = [p for p in policies if p["id"] != policy_id]
    if len(filtered) == len(policies):
        return False
    _save_policies(filtered)
    return True


def analyze_coverage(has_dependents: bool = False, is_homeowner: bool = False) -> dict:
    """Analyze insurance coverage and identify gaps."""
    policies = _load_policies()
    active_types = {p["type"] for p in policies if p.get("status") == "active"}

    gaps = []
    recommendations = []

    for essential in ESSENTIAL_TYPES:
        if essential not in active_types:
            gaps.append({
                "type": essential,
                "name": POLICY_TYPES.get(essential, essential),
                "priority": "high",
                "reason": f"{POLICY_TYPES.get(essential, essential)} is generally considered essential coverage.",
            })

    if has_dependents and "life" not in active_types:
        gaps.append({
            "type": "life",
            "name": "Life Insurance",
            "priority": "high",
            "reason": "Life insurance is important when you have dependents.",
        })

    if is_homeowner and "home" not in active_types:
        gaps.append({
            "type": "home",
            "name": "Home Insurance",
            "priority": "high",
            "reason": "Home insurance protects your largest asset.",
        })

    # Check for potentially redundant coverage
    type_counts = {}
    for p in policies:
        t = p["type"]
        type_counts[t] = type_counts.get(t, 0) + 1
    for t, count in type_counts.items():
        if count > 1:
            recommendations.append(f"You have {count} {POLICY_TYPES.get(t, t)} policies — check for overlap.")

    total_annual = sum(float(p.get("annual_premium", 0)) for p in policies if p.get("status") == "active")

    return {
        "active_policies": len([p for p in policies if p.get("status") == "active"]),
        "total_annual_premium": round(total_annual, 2),
        "total_monthly_premium": round(total_annual / 12, 2),
        "covered_types": sorted(active_types),
        "gaps": gaps,
        "recommendations": recommendations,
    }


def check_renewal_dates() -> list[dict]:
    """Find policies with upcoming renewal dates."""
    policies = _load_policies()
    today = date.today()
    upcoming = []

    for p in policies:
        if p.get("status") != "active" or not p.get("renewal_date"):
            continue
        try:
            renewal = date.fromisoformat(p["renewal_date"])
            days_until = (renewal - today).days
            if 0 <= days_until <= 90:
                upcoming.append({
                    "policy": p["name"] or POLICY_TYPES.get(p["type"], p["type"]),
                    "provider": p["provider"],
                    "renewal_date": p["renewal_date"],
                    "days_until": days_until,
                    "annual_premium": p["annual_premium"],
                })
        except (ValueError, TypeError):
            continue

    return sorted(upcoming, key=lambda x: x["days_until"])


def calculate_total_premiums() -> dict:
    policies = _load_policies()
    active = [p for p in policies if p.get("status") == "active"]
    total_annual = sum(float(p.get("annual_premium", 0)) for p in active)
    by_type = {}
    for p in active:
        t = p["type"]
        if t not in by_type:
            by_type[t] = 0.0
        by_type[t] += float(p.get("annual_premium", 0))

    return {
        "total_annual": round(total_annual, 2),
        "total_monthly": round(total_annual / 12, 2),
        "by_type": {k: round(v, 2) for k, v in sorted(by_type.items())},
        "policy_count": len(active),
    }


def format_insurance_display() -> str:
    policies = _load_policies()
    if not policies:
        return "No insurance policies tracked yet."

    premiums = calculate_total_premiums()
    lines = ["═══ Your Insurance ═══\n"]
    lines.append(f"Total annual: {format_money(premiums['total_annual'], 'EUR')} "
                 f"({format_money(premiums['total_monthly'], 'EUR')}/month)\n")

    for p in sorted(policies, key=lambda x: x.get("type", "")):
        status = "active" if p.get("status") == "active" else "inactive"
        name = p.get("name") or POLICY_TYPES.get(p["type"], p["type"])
        lines.append(f"  {name} [{status}]")
        lines.append(f"    Provider: {p.get('provider', '—')}  "
                     f"Premium: {format_money(p.get('annual_premium', 0), 'EUR')}/year")
        if p.get("coverage_amount"):
            lines.append(f"    Coverage: {format_money(p['coverage_amount'], 'EUR')}")
        if p.get("renewal_date"):
            lines.append(f"    Renewal: {p['renewal_date']}")

    return "\n".join(lines)
