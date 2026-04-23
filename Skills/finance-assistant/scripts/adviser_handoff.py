"""
Finance Assistant Specialist Handoff.

Build a structured brief for when the user needs professional advice
(financial planner, tax adviser, insurance broker, lawyer).

Adapted from TaxDE adviser_handoff.py with multi-domain support.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

try:
    from profile_manager import get_profile
    from insight_engine import generate_insights
except ImportError:
    import os, sys
    sys.path.insert(0, os.path.dirname(__file__))
    from profile_manager import get_profile
    from insight_engine import generate_insights


REFERRAL_TRIGGERS = {
    "tax_complex": {
        "priority": "high",
        "specialist": "Tax Adviser / Steuerberater",
        "reason": "Complex tax situation requiring professional review.",
    },
    "cross_border": {
        "priority": "high",
        "specialist": "International Tax Adviser",
        "reason": "Cross-border taxation likely affects the return.",
    },
    "estate_planning": {
        "priority": "high",
        "specialist": "Estate Planning Attorney",
        "reason": "Estate or inheritance planning requires legal expertise.",
    },
    "insurance_dispute": {
        "priority": "medium",
        "specialist": "Insurance Broker / Ombudsman",
        "reason": "Insurance claim dispute or complex coverage question.",
    },
    "investment_complex": {
        "priority": "medium",
        "specialist": "Certified Financial Planner",
        "reason": "Complex investment structures or large portfolio decisions.",
    },
    "debt_crisis": {
        "priority": "high",
        "specialist": "Debt Counselor / Schuldnerberatung",
        "reason": "Debt-to-income ratio suggests professional debt counseling.",
    },
    "business_restructuring": {
        "priority": "high",
        "specialist": "Business Tax Adviser",
        "reason": "Business restructuring or major organizational changes.",
    },
}


def _detect_triggers(profile: dict, insights: list[dict]) -> list[dict]:
    """Detect situations requiring specialist referral."""
    triggers = []
    tax_extra = profile.get("tax_profile", {}).get("extra", {})
    emp = profile.get("employment", {})

    # Cross-border
    if tax_extra.get("expat") or tax_extra.get("dba_relevant"):
        triggers.append(REFERRAL_TRIGGERS["cross_border"])

    # Complex business
    if emp.get("type") in ("self_employed", "mixed"):
        triggers.append(REFERRAL_TRIGGERS["tax_complex"])

    # High-impact unresolved insights
    high_impact = [
        i for i in insights
        if i.get("status") != "ready" and (i.get("impact_amount") or 0) >= 500
    ]
    if len(high_impact) >= 3:
        triggers.append(REFERRAL_TRIGGERS["investment_complex"])

    # Debt stress
    try:
        from debt_optimizer import get_debts
        debts = get_debts()
        total_debt = sum(float(d.get("balance", 0)) for d in debts)
        gross = float(emp.get("annual_gross", 0))
        if gross > 0 and total_debt / gross > 0.5:
            triggers.append(REFERRAL_TRIGGERS["debt_crisis"])
    except Exception:
        pass

    return triggers


def _questions_for_triggers(triggers: list[dict]) -> list[str]:
    questions = []
    specialist_types = {t.get("specialist", "") for t in triggers}
    if "International Tax Adviser" in specialist_types:
        questions.append("How should tax residence and treaty allocation be handled?")
        questions.append("Which foreign income items need local reporting?")
    if "Tax Adviser / Steuerberater" in specialist_types:
        questions.append("Can you validate the filing preparation and identify material blind spots?")
    if "Certified Financial Planner" in specialist_types:
        questions.append("Given my portfolio and goals, what allocation changes do you recommend?")
    if "Debt Counselor / Schuldnerberatung" in specialist_types:
        questions.append("What is the best path to reduce my debt burden sustainably?")
    if not questions:
        questions.append("Can you review my financial situation and identify any material risks?")
    return questions[:8]


def build_adviser_handoff(
    profile: Optional[dict] = None,
    domain: Optional[str] = None,
) -> dict:
    """Build a structured specialist handoff brief."""
    profile = profile or get_profile() or {}
    insights_payload = generate_insights(profile, persist=False)
    all_insights = insights_payload.get("insights", [])

    # Filter by domain if specified
    insights = all_insights if not domain else [i for i in all_insights if i.get("domain") == domain]

    triggers = _detect_triggers(profile, insights)
    risk_level = "low"
    if any(t.get("priority") == "high" for t in triggers):
        risk_level = "high"
    elif triggers:
        risk_level = "medium"

    unresolved = [
        {"id": i["id"], "domain": i["domain"], "title": i["title"],
         "status": i["status"], "impact": i.get("impact_amount")}
        for i in insights if i.get("status") != "ready"
    ][:10]

    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "requires_specialist_review": bool(triggers),
        "risk_level": risk_level,
        "triggers": triggers,
        "questions_for_specialist": _questions_for_triggers(triggers),
        "unresolved_items": unresolved,
        "profile_summary": {
            "employment": profile.get("employment", {}).get("type"),
            "locale": profile.get("meta", {}).get("locale"),
            "family": profile.get("family", {}).get("status"),
            "housing": profile.get("housing", {}).get("type"),
        },
        "handoff_summary": (
            "Professional review recommended — see triggers and questions above."
            if triggers else
            "No specialist trigger detected, but this brief is available if needed."
        ),
    }
