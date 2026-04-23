"""
Finance Assistant Output Builder.

Build structured financial deliverables across all domains.
Adapted from TaxDE output_builder.py.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

try:
    from profile_manager import get_profile
    from finance_storage import get_output_suite_path, save_json
except ImportError:
    import os, sys
    sys.path.insert(0, os.path.dirname(__file__))
    from profile_manager import get_profile
    from finance_storage import get_output_suite_path, save_json


def _safe(fn, *args, default=None, **kwargs):
    try:
        return fn(*args, **kwargs)
    except Exception:
        return default


def build_output_suite(
    profile: Optional[dict] = None,
    persist: bool = True,
) -> dict:
    """Build a comprehensive financial output suite."""
    profile = profile or get_profile() or {}
    year = datetime.now().year

    from workspace_builder import build_workspace
    from insight_engine import generate_insights
    from net_worth_engine import calculate_net_worth, calculate_net_worth_trend
    from budget_engine import get_budget_variance
    from goal_tracker import get_goals
    from investment_tracker import calculate_total_return
    from debt_optimizer import get_debts, compare_payoff_strategies
    from insurance_analyzer import calculate_total_premiums, analyze_coverage
    from adviser_handoff import build_adviser_handoff

    workspace = _safe(build_workspace, profile, persist=False, default={})
    insights = _safe(generate_insights, profile, persist=False, default={"insights": []})
    nw = _safe(calculate_net_worth, default={})
    nw_trend = _safe(calculate_net_worth_trend, default={})
    month = datetime.now().month
    budget_var = _safe(get_budget_variance, year, month)
    goals = _safe(get_goals, default=[])
    portfolio = _safe(calculate_total_return, default={})
    debts = _safe(get_debts, default=[])
    debt_comparison = _safe(compare_payoff_strategies, default={}) if debts else None
    insurance = _safe(calculate_total_premiums, default={})
    coverage = _safe(analyze_coverage, default={})
    handoff = _safe(build_adviser_handoff, profile, default={})

    suite = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "year": year,
        "financial_health": {
            "score": workspace.get("financial_health_pct", 0) if isinstance(workspace, dict) else 0,
            "net_worth": nw.get("net_worth", 0) if isinstance(nw, dict) else 0,
            "trend": nw_trend.get("trend", "unknown") if isinstance(nw_trend, dict) else "unknown",
        },
        "budget_report": budget_var if isinstance(budget_var, dict) else None,
        "goals_report": {
            "active_goals": len([g for g in goals if g.get("status") == "active"]) if isinstance(goals, list) else 0,
            "goals": goals if isinstance(goals, list) else [],
        },
        "investment_report": portfolio if isinstance(portfolio, dict) else {},
        "debt_report": {
            "debts": debts if isinstance(debts, list) else [],
            "strategy_comparison": debt_comparison if isinstance(debt_comparison, dict) else None,
        },
        "insurance_report": {
            "premiums": insurance if isinstance(insurance, dict) else {},
            "coverage": coverage if isinstance(coverage, dict) else {},
        },
        "net_worth_report": {
            "current": nw if isinstance(nw, dict) else {},
            "trend": nw_trend if isinstance(nw_trend, dict) else {},
        },
        "insights": insights.get("insights", [])[:10] if isinstance(insights, dict) else [],
        "specialist_handoff": handoff if isinstance(handoff, dict) else {},
        "action_list": _build_action_list(workspace, insights),
    }

    if persist:
        save_json(get_output_suite_path(year), suite)

    return suite


def _build_action_list(workspace, insights) -> list[str]:
    actions = []
    if isinstance(workspace, dict):
        actions.extend(workspace.get("open_tasks", [])[:5])
    if isinstance(insights, dict):
        for i in insights.get("insights", []):
            if i.get("status") in ("ready", "needs_input") and i.get("next_action"):
                actions.append(f"[{i['domain']}] {i['next_action']}")
    # Deduplicate
    seen = set()
    deduped = []
    for a in actions:
        if a not in seen:
            seen.add(a)
            deduped.append(a)
    return deduped[:10]


def format_output_suite_display(suite: dict) -> str:
    health = suite.get("financial_health", {})
    lines = [
        f"Finance Assistant — Annual Report {suite['year']}",
        f"Financial Health: {health.get('score', 0)}%",
        f"Net Worth: EUR {health.get('net_worth', 0):,.0f} (trend: {health.get('trend', '—')})",
        "",
    ]

    actions = suite.get("action_list", [])
    if actions:
        lines.append("Top Actions:")
        for a in actions[:5]:
            lines.append(f"  → {a}")

    handoff = suite.get("specialist_handoff", {})
    if isinstance(handoff, dict) and handoff.get("requires_specialist_review"):
        lines.append(f"\nSpecialist review: recommended ({handoff.get('risk_level', '—')} priority)")

    return "\n".join(lines)
