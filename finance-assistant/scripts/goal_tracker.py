"""
Finance Assistant Goal Tracker.

Track savings goals with projections, contribution planning, and progress monitoring.
"""

from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import Optional

try:
    from finance_storage import get_goals_path, load_json, save_json
    from currency import format_money
except ImportError:
    import os, sys
    sys.path.insert(0, os.path.dirname(__file__))
    from finance_storage import get_goals_path, load_json, save_json
    from currency import format_money


GOAL_TYPES = {
    "emergency_fund":     "Emergency Fund",
    "house_down_payment": "House Down Payment",
    "vacation":           "Vacation",
    "education":          "Education",
    "car":                "Car Purchase",
    "retirement":         "Retirement",
    "debt_payoff":        "Debt Payoff",
    "wedding":            "Wedding",
    "custom":             "Custom Goal",
}


def _load_goals() -> list[dict]:
    data = load_json(get_goals_path(), default={"goals": []})
    return data.get("goals", []) if isinstance(data, dict) else []


def _save_goals(goals: list[dict]) -> None:
    save_json(get_goals_path(), {
        "last_updated": datetime.now().isoformat(),
        "goals": goals,
    })


def get_goals() -> list[dict]:
    return _load_goals()


def add_goal(goal_data: dict) -> dict:
    goals = _load_goals()
    goal = {
        "id": goal_data.get("id") or str(uuid.uuid4())[:8],
        "name": goal_data.get("name", "Unnamed goal"),
        "type": goal_data.get("type", "custom"),
        "target_amount": float(goal_data.get("target_amount", 0)),
        "current_amount": float(goal_data.get("current_amount", 0)),
        "currency": goal_data.get("currency", "EUR"),
        "target_date": goal_data.get("target_date"),
        "monthly_contribution": float(goal_data.get("monthly_contribution", 0)),
        "linked_account_id": goal_data.get("linked_account_id"),
        "priority": goal_data.get("priority", "medium"),
        "status": "active",
        "created_at": datetime.now().isoformat(),
    }
    goals.append(goal)
    _save_goals(goals)
    return goal


def update_goal(goal_id: str, updates: dict) -> Optional[dict]:
    goals = _load_goals()
    for i, g in enumerate(goals):
        if g["id"] == goal_id:
            g.update(updates)
            goals[i] = g
            _save_goals(goals)
            return g
    return None


def delete_goal(goal_id: str) -> bool:
    goals = _load_goals()
    filtered = [g for g in goals if g["id"] != goal_id]
    if len(filtered) == len(goals):
        return False
    _save_goals(filtered)
    return True


def project_goal_completion(goal_id: str, monthly_contribution: Optional[float] = None) -> dict:
    """Project when a goal will be reached."""
    goals = _load_goals()
    goal = next((g for g in goals if g["id"] == goal_id), None)
    if not goal:
        return {"error": f"Goal '{goal_id}' not found."}

    target = float(goal["target_amount"])
    current = float(goal["current_amount"])
    monthly = monthly_contribution or float(goal.get("monthly_contribution", 0))
    remaining = max(0, target - current)

    if remaining == 0:
        return {"goal": goal, "status": "completed", "remaining": 0, "months_to_go": 0}

    if monthly <= 0:
        return {
            "goal": goal,
            "status": "stalled",
            "remaining": round(remaining, 2),
            "months_to_go": None,
            "suggestion": f"To reach this goal in 12 months, save {format_money(remaining / 12, goal['currency'])}/month.",
        }

    months_to_go = remaining / monthly
    completion_date = None
    today = date.today()
    try:
        month = today.month + int(months_to_go)
        year = today.year + (month - 1) // 12
        month = ((month - 1) % 12) + 1
        completion_date = date(year, month, min(today.day, 28)).isoformat()
    except (ValueError, OverflowError):
        pass

    # Check against target date
    on_track = True
    if goal.get("target_date") and completion_date:
        on_track = completion_date <= goal["target_date"]

    return {
        "goal": goal,
        "status": "on_track" if on_track else "behind",
        "remaining": round(remaining, 2),
        "monthly_contribution": round(monthly, 2),
        "months_to_go": round(months_to_go, 1),
        "projected_completion": completion_date,
        "on_track": on_track,
        "pct_complete": round(current / target * 100, 1) if target > 0 else 0,
    }


def suggest_emergency_fund(monthly_expenses: float, months: int = 6, currency: str = "EUR") -> dict:
    """Suggest an emergency fund size."""
    target = monthly_expenses * months
    return {
        "suggested_target": round(target, 2),
        "monthly_expenses": round(monthly_expenses, 2),
        "months_coverage": months,
        "currency": currency,
        "rationale": f"{months} months of expenses at {format_money(monthly_expenses, currency)}/month",
    }


def format_goals_display() -> str:
    goals = _load_goals()
    if not goals:
        return "No savings goals set yet. Add your first goal to start tracking."

    lines = ["═══ Your Savings Goals ═══\n"]
    total_target = 0
    total_current = 0

    for g in sorted(goals, key=lambda x: x.get("priority", "medium")):
        target = float(g["target_amount"])
        current = float(g["current_amount"])
        total_target += target
        total_current += current
        pct = round(current / target * 100) if target > 0 else 0
        bar_len = 20
        filled = int(bar_len * pct / 100)
        bar = "█" * filled + "░" * (bar_len - filled)
        cur = g.get("currency", "EUR")

        lines.append(f"  {g['name']} ({GOAL_TYPES.get(g['type'], g['type'])})")
        lines.append(f"    [{bar}] {pct}%")
        lines.append(f"    {format_money(current, cur)} / {format_money(target, cur)}")
        if g.get("monthly_contribution"):
            lines.append(f"    Saving: {format_money(g['monthly_contribution'], cur)}/month")
        if g.get("target_date"):
            lines.append(f"    Target date: {g['target_date']}")
        lines.append("")

    overall_pct = round(total_current / total_target * 100) if total_target > 0 else 0
    lines.append(f"  Overall: {format_money(total_current, 'EUR')} / {format_money(total_target, 'EUR')} ({overall_pct}%)")

    return "\n".join(lines)
