"""
Finance Assistant Budget Engine.

Create, track, and analyze budgets with variance reporting.
Supports monthly and annual budgets with category-level tracking.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

try:
    from finance_storage import get_budget_path, load_json, save_json
    from transaction_logger import get_totals as get_transaction_totals, EXPENSE_CATEGORIES
    from currency import format_money
except ImportError:
    import os, sys
    sys.path.insert(0, os.path.dirname(__file__))
    from finance_storage import get_budget_path, load_json, save_json
    from transaction_logger import get_totals as get_transaction_totals, EXPENSE_CATEGORIES
    from currency import format_money


BUDGET_METHODS = {
    "custom":      "Custom category limits",
    "50-30-20":    "50% needs, 30% wants, 20% savings",
    "zero-based":  "Every dollar has a job (income - expenses = 0)",
    "envelope":    "Fixed envelopes per category",
    "80-20":       "80% spending, 20% savings",
}

# 50-30-20 category classification
NEEDS_CATEGORIES = {"housing", "food", "transport", "insurance", "healthcare", "childcare", "telecom", "taxes"}
WANTS_CATEGORIES = {"dining", "entertainment", "subscriptions", "clothing", "travel", "personal_care", "gifts", "pets"}
SAVINGS_CATEGORIES = {"savings", "debt_payment"}


# ── Public API ───────────────────────────────────────────────────────────────

def create_budget(
    year: int,
    month: Optional[int] = None,
    method: str = "custom",
    income_target: Optional[float] = None,
    category_limits: Optional[dict] = None,
    currency: str = "EUR",
) -> dict:
    """Create a new budget. Returns the budget dict."""
    budget = {
        "created_at": datetime.now().isoformat(),
        "year": year,
        "month": month,
        "method": method,
        "currency": currency,
        "income_target": income_target or 0.0,
        "category_limits": category_limits or {},
        "actuals": {},
    }

    # Auto-generate limits for 50-30-20
    if method == "50-30-20" and income_target:
        needs = income_target * 0.50
        wants = income_target * 0.30
        savings = income_target * 0.20
        budget["method_breakdown"] = {
            "needs": round(needs, 2),
            "wants": round(wants, 2),
            "savings": round(savings, 2),
        }
        if not category_limits:
            budget["category_limits"] = _distribute_50_30_20(income_target)

    elif method == "80-20" and income_target:
        budget["method_breakdown"] = {
            "spending": round(income_target * 0.80, 2),
            "savings": round(income_target * 0.20, 2),
        }

    save_json(get_budget_path(year, month), budget)
    return budget


def get_budget(year: int, month: Optional[int] = None) -> Optional[dict]:
    return load_json(get_budget_path(year, month))


def update_budget_actuals(
    year: int,
    month: Optional[int] = None,
    account_id: str = "default",
) -> dict:
    """Refresh actuals from transaction log. Returns updated budget."""
    budget = get_budget(year, month)
    if not budget:
        return {"error": f"No budget found for {year}" + (f"-{month:02d}" if month else "")}

    totals = get_transaction_totals(account_id=account_id, year=year, month=month)
    actuals = {}
    for cat, data in totals.items():
        actuals[cat] = {
            "spent": data.get("expense", 0.0),
            "earned": data.get("income", 0.0),
            "count": data.get("count", 0),
        }

    budget["actuals"] = actuals
    budget["last_refreshed"] = datetime.now().isoformat()
    save_json(get_budget_path(year, month), budget)
    return budget


def get_budget_variance(year: int, month: Optional[int] = None) -> dict:
    """Compare planned vs actual. Returns variance by category."""
    budget = get_budget(year, month)
    if not budget:
        return {"error": "No budget found"}

    limits = budget.get("category_limits", {})
    actuals = budget.get("actuals", {})
    variance = {}

    all_cats = set(limits.keys()) | set(actuals.keys())
    for cat in sorted(all_cats):
        planned = float(limits.get(cat, 0))
        actual_data = actuals.get(cat, {})
        spent = float(actual_data.get("spent", 0)) if isinstance(actual_data, dict) else float(actual_data)
        diff = planned - spent
        variance[cat] = {
            "planned": round(planned, 2),
            "actual": round(spent, 2),
            "variance": round(diff, 2),
            "pct_used": round((spent / planned * 100) if planned > 0 else 0, 1),
            "status": "under" if diff > 0 else ("over" if diff < 0 else "on_budget"),
        }

    total_planned = sum(float(limits.get(c, 0)) for c in limits)
    total_actual = sum(
        float(actuals[c].get("spent", 0)) if isinstance(actuals.get(c), dict) else 0
        for c in actuals
    )

    return {
        "year": year,
        "month": month,
        "method": budget.get("method"),
        "income_target": budget.get("income_target"),
        "total_planned": round(total_planned, 2),
        "total_actual": round(total_actual, 2),
        "total_variance": round(total_planned - total_actual, 2),
        "categories": variance,
        "overspend_categories": [c for c, v in variance.items() if v["status"] == "over"],
        "underspend_categories": [c for c, v in variance.items() if v["status"] == "under" and v["variance"] > 50],
    }


def suggest_budget_from_history(
    account_id: str = "default",
    year: Optional[int] = None,
    months_back: int = 3,
) -> dict:
    """Suggest category limits based on recent spending history."""
    year = year or datetime.now().year
    current_month = datetime.now().month

    all_totals: dict = {}
    months_counted = 0

    for offset in range(months_back):
        m = current_month - offset
        y = year
        if m <= 0:
            m += 12
            y -= 1
        totals = get_transaction_totals(account_id=account_id, year=y, month=m)
        if totals:
            months_counted += 1
            for cat, data in totals.items():
                if cat not in all_totals:
                    all_totals[cat] = 0.0
                all_totals[cat] += float(data.get("expense", 0))

    if months_counted == 0:
        return {"error": "No transaction history found for suggestion."}

    suggested = {}
    for cat, total in sorted(all_totals.items()):
        avg = total / months_counted
        # Round up to nearest 10 for a comfortable buffer
        suggested[cat] = round(((avg + 9) // 10) * 10, 2)

    return {
        "based_on_months": months_counted,
        "suggested_limits": suggested,
        "total_suggested": round(sum(suggested.values()), 2),
    }


def format_budget_display(budget: dict) -> str:
    """Format budget for display."""
    if "error" in budget:
        return budget["error"]

    year = budget.get("year")
    month = budget.get("month")
    method = BUDGET_METHODS.get(budget.get("method", ""), budget.get("method", ""))
    period = f"{year}-{month:02d}" if month else str(year)

    lines = [
        f"Budget for {period}",
        f"Method: {method}",
        f"Income target: {format_money(budget.get('income_target', 0), budget.get('currency', 'EUR'))}",
        "",
    ]

    limits = budget.get("category_limits", {})
    actuals = budget.get("actuals", {})

    if limits:
        lines.append(f"{'Category':<25} {'Planned':>10} {'Actual':>10} {'Remaining':>10}")
        lines.append("-" * 58)
        for cat in sorted(limits.keys()):
            planned = float(limits[cat])
            actual_data = actuals.get(cat, {})
            spent = float(actual_data.get("spent", 0)) if isinstance(actual_data, dict) else 0
            remaining = planned - spent
            flag = " (!)" if remaining < 0 else ""
            lines.append(
                f"  {cat:<23} {planned:>10,.0f} {spent:>10,.0f} {remaining:>10,.0f}{flag}"
            )

    if budget.get("method_breakdown"):
        lines.append("")
        lines.append("Method breakdown:")
        for key, val in budget["method_breakdown"].items():
            lines.append(f"  {key}: {format_money(val, budget.get('currency', 'EUR'))}")

    return "\n".join(lines)


# ── Helpers ──────────────────────────────────────────────────────────────────

def _distribute_50_30_20(monthly_income: float) -> dict:
    """Auto-distribute income into needs/wants/savings categories."""
    needs_budget = monthly_income * 0.50
    wants_budget = monthly_income * 0.30
    savings_budget = monthly_income * 0.20

    limits = {}
    # Distribute needs proportionally
    needs_list = [c for c in NEEDS_CATEGORIES if c in EXPENSE_CATEGORIES]
    if needs_list:
        per_need = needs_budget / len(needs_list)
        for c in needs_list:
            limits[c] = round(per_need, 2)

    wants_list = [c for c in WANTS_CATEGORIES if c in EXPENSE_CATEGORIES]
    if wants_list:
        per_want = wants_budget / len(wants_list)
        for c in wants_list:
            limits[c] = round(per_want, 2)

    limits["savings"] = round(savings_budget, 2)
    return limits
