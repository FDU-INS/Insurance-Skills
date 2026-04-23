"""
Finance Assistant Workspace Builder.

Builds a financial health dashboard aggregating data from all domains.
Adapted from TaxDE workspace_builder.py.
"""

from __future__ import annotations

import logging
from datetime import date, datetime
from typing import Optional

_log = logging.getLogger(__name__)

try:
    from finance_storage import get_workspace_path, save_json
    from profile_manager import get_profile
    from insight_engine import generate_insights
except ImportError:
    import os, sys
    sys.path.insert(0, os.path.dirname(__file__))
    from finance_storage import get_workspace_path, save_json
    from profile_manager import get_profile
    from insight_engine import generate_insights


def _safe_call(fn, *args, default=None, **kwargs):
    try:
        return fn(*args, **kwargs)
    except Exception as exc:
        _log.debug("_safe_call(%s) failed: %s", getattr(fn, "__name__", fn), exc, exc_info=True)
        return default


def build_workspace(
    profile: Optional[dict] = None,
    persist: bool = True,
) -> dict:
    """Build a comprehensive financial health workspace."""
    profile = profile or get_profile() or {}
    year = datetime.now().year

    # Gather data from all domains
    from net_worth_engine import calculate_net_worth
    from budget_engine import get_budget, get_budget_variance
    from goal_tracker import get_goals
    from investment_tracker import calculate_total_return, calculate_allocation
    from debt_optimizer import get_debts
    from insurance_analyzer import calculate_total_premiums, analyze_coverage
    from account_manager import get_total_balance

    nw = _safe_call(calculate_net_worth, default={"net_worth": 0, "total_assets": 0, "total_liabilities": 0})
    month = datetime.now().month
    budget = _safe_call(get_budget, year, month)
    budget_variance = _safe_call(get_budget_variance, year, month) if budget else None
    goals = _safe_call(get_goals, default=[])
    portfolio_return = _safe_call(calculate_total_return, default={"total_return_pct": 0})
    allocation = _safe_call(calculate_allocation, default={"total_value": 0})
    debts = _safe_call(get_debts, default=[])
    insurance = _safe_call(calculate_total_premiums, default={"total_annual": 0})
    accounts = _safe_call(get_total_balance, default={"net": 0})
    insights = _safe_call(generate_insights, profile, persist=False, default={"insights": []})

    # ── Health Scores ────────────────────────────────────────────────────
    budget_score = _budget_health(budget_variance)
    savings_score = _savings_health(goals)
    investment_score = _investment_health(portfolio_return, allocation)
    debt_score = _debt_health(debts)
    insurance_score = _insurance_health(profile)
    nw_score = 0.7  # Base score, improves with trend data

    readiness_pct = round(
        (budget_score * 0.15 + savings_score * 0.15 + investment_score * 0.15 +
         debt_score * 0.15 + insurance_score * 0.10 + nw_score * 0.15 + 0.15) * 100
    )
    readiness_pct = min(100, max(0, readiness_pct))

    # ── Open tasks ───────────────────────────────────────────────────────
    open_tasks = []
    all_insights = insights.get("insights", []) if isinstance(insights, dict) else []
    for i in all_insights:
        if i.get("status") in ("needs_input", "needs_evidence", "detected"):
            open_tasks.append(f"[{i['domain']}] {i['title']}: {i['next_action']}")
    open_tasks = open_tasks[:10]

    workspace = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "year": year,
        "financial_health_pct": readiness_pct,
        "net_worth": nw.get("net_worth", 0) if isinstance(nw, dict) else 0,
        "total_assets": nw.get("total_assets", 0) if isinstance(nw, dict) else 0,
        "total_liabilities": nw.get("total_liabilities", 0) if isinstance(nw, dict) else 0,
        "scores": {
            "budget": round(budget_score * 100),
            "savings": round(savings_score * 100),
            "investments": round(investment_score * 100),
            "debt": round(debt_score * 100),
            "insurance": round(insurance_score * 100),
        },
        "budget_status": {
            "has_budget": budget is not None,
            "overspend_categories": budget_variance.get("overspend_categories", []) if budget_variance else [],
        },
        "goal_count": len(goals) if isinstance(goals, list) else 0,
        "portfolio_value": allocation.get("total_value", 0) if isinstance(allocation, dict) else 0,
        "portfolio_return_pct": portfolio_return.get("total_return_pct", 0) if isinstance(portfolio_return, dict) else 0,
        "debt_count": len(debts) if isinstance(debts, list) else 0,
        "debt_total": round(sum(float(d.get("balance", 0)) for d in debts), 2) if isinstance(debts, list) else 0,
        "insurance_annual": insurance.get("total_annual", 0) if isinstance(insurance, dict) else 0,
        "insight_count": len(all_insights),
        "open_tasks": open_tasks,
        "insights_summary": all_insights[:5],
    }

    if persist:
        save_json(get_workspace_path(year), workspace)

    return workspace


def _budget_health(variance) -> float:
    if not variance or "error" in (variance or {}):
        return 0.3
    overspends = len(variance.get("overspend_categories", []))
    if overspends == 0:
        return 1.0
    if overspends <= 2:
        return 0.7
    return 0.4


def _savings_health(goals) -> float:
    if not goals:
        return 0.3
    active = [g for g in goals if g.get("status") == "active"]
    if not active:
        return 0.5
    funded = sum(1 for g in active if float(g.get("current_amount", 0)) > 0)
    return min(1.0, 0.5 + funded / len(active) * 0.5)


def _investment_health(returns, allocation) -> float:
    if not allocation or float(allocation.get("total_value", 0)) == 0:
        return 0.3
    ret_pct = float(returns.get("total_return_pct", 0)) if returns else 0
    if ret_pct > 5:
        return 1.0
    if ret_pct > 0:
        return 0.7
    return 0.5


def _debt_health(debts) -> float:
    if not debts:
        return 1.0
    high_rate = sum(1 for d in debts if float(d.get("interest_rate", 0)) > 10)
    if high_rate > 0:
        return 0.3
    return 0.7


def _insurance_health(profile) -> float:
    try:
        from insurance_analyzer import analyze_coverage
        fam = profile.get("family", {})
        coverage = analyze_coverage(
            has_dependents=bool(fam.get("children")),
            is_homeowner=profile.get("housing", {}).get("type") == "owner",
        )
        gaps = len(coverage.get("gaps", []))
        if gaps == 0:
            return 1.0
        if gaps <= 2:
            return 0.6
        return 0.3
    except Exception:
        return 0.5


def format_workspace_display(workspace: dict) -> str:
    lines = [
        f"═══ Financial Health Dashboard ═══\n",
        f"  Overall Health: {workspace['financial_health_pct']}%",
        f"  Net Worth: EUR {workspace['net_worth']:,.0f}\n",
        "  Domain Scores:",
    ]
    scores = workspace.get("scores", {})
    for domain, score in sorted(scores.items()):
        bar = "█" * (score // 10) + "░" * (10 - score // 10)
        lines.append(f"    {domain:<15} [{bar}] {score}%")

    lines.append(f"\n  Portfolio: EUR {workspace.get('portfolio_value', 0):,.0f} "
                 f"({workspace.get('portfolio_return_pct', 0):+.1f}%)")
    lines.append(f"  Debts: EUR {workspace.get('debt_total', 0):,.0f} ({workspace.get('debt_count', 0)} active)")
    lines.append(f"  Insurance: EUR {workspace.get('insurance_annual', 0):,.0f}/year")
    lines.append(f"  Goals: {workspace.get('goal_count', 0)} active")

    tasks = workspace.get("open_tasks", [])
    if tasks:
        lines.append(f"\n  Open Tasks ({len(tasks)}):")
        for t in tasks[:5]:
            lines.append(f"    → {t}")

    return "\n".join(lines)
