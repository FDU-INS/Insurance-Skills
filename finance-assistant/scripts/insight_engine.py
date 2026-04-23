"""
Finance Assistant Insight Engine.

Generates cross-domain financial insights from profile, accounts, budgets,
investments, debts, insurance, and tax data.

Adapted from TaxDE claim_engine.py — preserves the same 4-status model
(ready, needs_input, needs_evidence, detected) and confidence levels.
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Optional

_log = logging.getLogger(__name__)

try:
    from finance_storage import load_json, save_json, ensure_subdir
    from profile_manager import get_profile
except ImportError:
    import os, sys
    sys.path.insert(0, os.path.dirname(__file__))
    from finance_storage import load_json, save_json, ensure_subdir
    from profile_manager import get_profile


def _insight(domain, title, insight_id, status, impact_amount, confidence, action, notes=""):
    return {
        "id": insight_id,
        "domain": domain,
        "title": title,
        "status": status,
        "impact_amount": round(impact_amount, 2) if impact_amount else None,
        "confidence": confidence,
        "next_action": action,
        "notes": notes,
    }


def _budget_insights(profile: dict) -> list[dict]:
    insights = []
    try:
        from budget_engine import get_budget, get_budget_variance
        year = datetime.now().year
        month = datetime.now().month
        budget = get_budget(year, month)
        if budget:
            variance = get_budget_variance(year, month)
            overspends = variance.get("overspend_categories", [])
            if overspends:
                total_over = sum(
                    abs(variance["categories"][c]["variance"])
                    for c in overspends if c in variance.get("categories", {})
                )
                insights.append(_insight(
                    "budget", f"Budget overspend in {len(overspends)} categories",
                    "budget_overspend", "ready", total_over, "definitive",
                    f"Review spending in: {', '.join(overspends[:3])}"
                ))
        else:
            insights.append(_insight(
                "budget", "No budget set for this month",
                "no_budget", "detected", None, "likely",
                "Create a monthly budget to track spending."
            ))
    except Exception as exc:
        _log.debug("_budget_insights failed: %s", exc, exc_info=True)
    return insights


def _savings_insights(profile: dict) -> list[dict]:
    insights = []
    try:
        from goal_tracker import get_goals, project_goal_completion
        goals = get_goals()
        if not goals:
            insights.append(_insight(
                "savings", "No savings goals set",
                "no_goals", "detected", None, "likely",
                "Set at least one savings goal (emergency fund recommended first)."
            ))
        else:
            for g in goals:
                if g.get("status") != "active":
                    continue
                proj = project_goal_completion(g["id"])
                if proj.get("status") == "stalled":
                    insights.append(_insight(
                        "savings", f"Goal '{g['name']}' has no monthly contribution",
                        f"stalled_{g['id']}", "needs_input",
                        float(g.get("target_amount", 0)) - float(g.get("current_amount", 0)),
                        "likely", "Set a monthly contribution amount."
                    ))
                elif proj.get("on_track") is False:
                    insights.append(_insight(
                        "savings", f"Goal '{g['name']}' is behind schedule",
                        f"behind_{g['id']}", "ready",
                        proj.get("remaining"), "likely",
                        f"Increase monthly contribution or extend target date."
                    ))
    except Exception as exc:
        _log.debug("_savings_insights failed: %s", exc, exc_info=True)
    return insights


def _investment_insights(profile: dict) -> list[dict]:
    insights = []
    try:
        from investment_tracker import get_portfolio, calculate_allocation, suggest_rebalance
        portfolio = get_portfolio()
        holdings = portfolio.get("holdings", [])
        if not holdings:
            insights.append(_insight(
                "investments", "No investments tracked",
                "no_investments", "detected", None, "likely",
                "Add your investment holdings to track portfolio performance."
            ))
        else:
            rebalance = suggest_rebalance()
            if rebalance and not any("suggestion" in r for r in rebalance):
                total_drift = sum(abs(r.get("diff_pct", 0)) for r in rebalance)
                if total_drift > 10:
                    insights.append(_insight(
                        "investments", "Portfolio needs rebalancing",
                        "rebalance_needed", "ready", None, "likely",
                        f"{len(rebalance)} allocation adjustments suggested."
                    ))
    except Exception as exc:
        _log.debug("_investment_insights failed: %s", exc, exc_info=True)
    return insights


def _debt_insights(profile: dict) -> list[dict]:
    insights = []
    try:
        from debt_optimizer import get_debts, compare_payoff_strategies
        debts = get_debts()
        if debts:
            comparison = compare_payoff_strategies(extra_monthly=100)
            interest_saved = comparison["comparison"]["interest_saved_by_avalanche"]
            if interest_saved > 50:
                insights.append(_insight(
                    "debt", f"Avalanche strategy saves {interest_saved:,.0f} in interest",
                    "debt_strategy", "ready", interest_saved, "definitive",
                    "Consider putting extra payments toward highest-rate debt first."
                ))
            # High-rate debt alert
            for d in debts:
                if float(d.get("interest_rate", 0)) > 15:
                    insights.append(_insight(
                        "debt", f"High-interest debt: {d['name']} at {d['interest_rate']}%",
                        f"high_rate_{d['id']}", "ready",
                        float(d["balance"]) * float(d["interest_rate"]) / 100,
                        "definitive", "Prioritize paying this down or refinancing."
                    ))
    except Exception as exc:
        _log.debug("_debt_insights failed: %s", exc, exc_info=True)
    return insights


def _insurance_insights(profile: dict) -> list[dict]:
    insights = []
    try:
        from insurance_analyzer import analyze_coverage, check_renewal_dates
        fam = profile.get("family", {})
        has_dependents = bool(fam.get("children") or fam.get("dependents"))
        is_homeowner = profile.get("housing", {}).get("type") == "owner"
        coverage = analyze_coverage(has_dependents=has_dependents, is_homeowner=is_homeowner)
        for gap in coverage.get("gaps", []):
            insights.append(_insight(
                "insurance", f"Missing: {gap['name']}",
                f"insurance_gap_{gap['type']}", "detected", None,
                "likely" if gap["priority"] == "high" else "debatable",
                gap["reason"]
            ))
        renewals = check_renewal_dates()
        for r in renewals[:2]:
            insights.append(_insight(
                "insurance", f"Renewal: {r['policy']} in {r['days_until']} days",
                f"renewal_{r['policy']}", "ready", float(r.get("annual_premium", 0)),
                "definitive", "Review and compare before auto-renewal."
            ))
    except Exception as exc:
        _log.debug("_insurance_insights failed: %s", exc, exc_info=True)
    return insights


def _tax_insights(profile: dict) -> list[dict]:
    insights = []
    try:
        from tax_engine import generate_tax_claims
        claims = generate_tax_claims(profile, persist=False)
        for claim in claims.get("claims", []):
            if claim.get("status") in ("needs_input", "needs_evidence", "detected"):
                insights.append(_insight(
                    "tax", claim["title"],
                    f"tax_{claim['id']}", claim["status"],
                    claim.get("amount_deductible"),
                    claim.get("confidence", "likely"),
                    claim.get("next_action", "")
                ))
    except Exception as exc:
        _log.debug("_tax_insights failed: %s", exc, exc_info=True)
    return insights


def _net_worth_insights(profile: dict) -> list[dict]:
    insights = []
    try:
        from net_worth_engine import calculate_net_worth_trend
        trend = calculate_net_worth_trend()
        if trend.get("trend") == "declining":
            insights.append(_insight(
                "net_worth", "Net worth is declining",
                "nw_declining", "ready", abs(trend.get("change", 0)),
                "likely", "Review spending and debt to reverse the trend."
            ))
        elif trend.get("trend") == "no_history":
            insights.append(_insight(
                "net_worth", "No net worth history",
                "nw_no_history", "detected", None, "likely",
                "Take a net worth snapshot to start tracking."
            ))
    except Exception as exc:
        _log.debug("_net_worth_insights failed: %s", exc, exc_info=True)
    return insights


def generate_insights(profile: Optional[dict] = None, persist: bool = True) -> dict:
    """Generate cross-domain financial insights."""
    profile = profile or get_profile() or {}
    insights = []

    insights.extend(_budget_insights(profile))
    insights.extend(_savings_insights(profile))
    insights.extend(_investment_insights(profile))
    insights.extend(_debt_insights(profile))
    insights.extend(_insurance_insights(profile))
    insights.extend(_tax_insights(profile))
    insights.extend(_net_worth_insights(profile))

    # Sort: ready first, then by impact
    insights.sort(key=lambda i: (
        {"ready": 0, "needs_evidence": 1, "needs_input": 2, "detected": 3}.get(i["status"], 9),
        -(i["impact_amount"] or 0),
        i["title"],
    ))

    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "insight_count": len(insights),
        "insights": insights,
        "by_domain": _group_by_domain(insights),
    }

    if persist:
        path = ensure_subdir("workspace") / "insights.json"
        save_json(path, payload)

    return payload


def _group_by_domain(insights: list[dict]) -> dict:
    grouped = {}
    for i in insights:
        d = i.get("domain", "other")
        if d not in grouped:
            grouped[d] = []
        grouped[d].append(i)
    return grouped


def format_insights_display(payload: dict) -> str:
    insights = payload.get("insights", [])
    if not insights:
        return "No financial insights to report. Your finances look well-managed!"

    lines = ["═══ Financial Insights ═══\n"]
    for i in insights:
        icon = {"ready": "●", "needs_input": "○", "needs_evidence": "◐", "detected": "◌"}.get(i["status"], "?")
        impact = f" ({i['impact_amount']:,.0f})" if i.get("impact_amount") else ""
        lines.append(f"  {icon} [{i['domain']}] {i['title']}{impact}")
        lines.append(f"    → {i['next_action']}")

    return "\n".join(lines)
