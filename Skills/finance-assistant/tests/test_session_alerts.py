"""Tests for session_alerts.py — proactive session nudges."""

import json
from datetime import date, timedelta
from pathlib import Path
import pytest

from scripts.session_alerts import (
    get_session_alerts,
    format_alerts,
    _budget_alerts,
    _goal_alerts,
    _recurring_alerts,
    URGENCY_LEVELS,
)
from scripts.finance_storage import get_finance_dir


# ── Budget Alerts ─────────────────────────────────────────────────────────────

def test_budget_overspend_is_critical(isolated_finance_dir):
    today = date.today()
    year, month = today.year, today.month
    budget_dir = get_finance_dir() / "budgets"
    budget_dir.mkdir(parents=True, exist_ok=True)
    budget_path = budget_dir / f"{year}-{month:02d}.json"
    budget_path.write_text(json.dumps({
        "categories": {
            "Eating Out": {"planned": 200, "actual": 250}
        }
    }))
    alerts = _budget_alerts(today)
    critical = [a for a in alerts if a["urgency"] == "critical"]
    assert any("Eating Out" in a["title"] for a in critical)


def test_budget_pacing_fast_is_warning(isolated_finance_dir):
    # Simulate day 5 of month, 85% of budget used
    today = date.today().replace(day=5)
    year, month = today.year, today.month
    budget_dir = get_finance_dir() / "budgets"
    budget_dir.mkdir(parents=True, exist_ok=True)
    budget_path = budget_dir / f"{year}-{month:02d}.json"
    budget_path.write_text(json.dumps({
        "categories": {
            "Groceries": {"planned": 400, "actual": 340}
        }
    }))
    alerts = _budget_alerts(today)
    # 340/400 = 85% at 16% of month
    warnings = [a for a in alerts if a["urgency"] in ("warning", "critical")]
    assert any("Groceries" in a["title"] for a in warnings)


def test_no_alert_for_healthy_budget(isolated_finance_dir):
    today = date.today()
    year, month = today.year, today.month
    budget_dir = get_finance_dir() / "budgets"
    budget_dir.mkdir(parents=True, exist_ok=True)
    budget_path = budget_dir / f"{year}-{month:02d}.json"
    budget_path.write_text(json.dumps({
        "categories": {
            "Transport": {"planned": 100, "actual": 40}
        }
    }))
    alerts = _budget_alerts(today)
    assert alerts == []


# ── Goal Alerts ───────────────────────────────────────────────────────────────

def test_goal_deadline_approaching_creates_alert(isolated_finance_dir):
    goals_dir = get_finance_dir() / "goals"
    goals_dir.mkdir(parents=True, exist_ok=True)
    deadline = (date.today() + timedelta(days=15)).isoformat()
    (goals_dir / "goals.json").write_text(json.dumps({
        "goals": [{
            "name": "Notgroschen",
            "target_amount": 5000,
            "current_amount": 2000,
            "deadline": deadline,
            "currency": "EUR",
        }]
    }))
    alerts = _goal_alerts(date.today())
    assert any("Notgroschen" in a["title"] for a in alerts)


def test_completed_goal_no_alert(isolated_finance_dir):
    goals_dir = get_finance_dir() / "goals"
    goals_dir.mkdir(parents=True, exist_ok=True)
    deadline = (date.today() + timedelta(days=10)).isoformat()
    (goals_dir / "goals.json").write_text(json.dumps({
        "goals": [{
            "name": "Emergency Fund",
            "target_amount": 3000,
            "current_amount": 3000,
            "deadline": deadline,
            "currency": "EUR",
        }]
    }))
    alerts = _goal_alerts(date.today())
    assert alerts == []


def test_distant_goal_no_alert(isolated_finance_dir):
    goals_dir = get_finance_dir() / "goals"
    goals_dir.mkdir(parents=True, exist_ok=True)
    deadline = (date.today() + timedelta(days=200)).isoformat()
    (goals_dir / "goals.json").write_text(json.dumps({
        "goals": [{
            "name": "New Laptop",
            "target_amount": 2000,
            "current_amount": 500,
            "deadline": deadline,
            "currency": "EUR",
        }]
    }))
    alerts = _goal_alerts(date.today())
    assert alerts == []


# ── Alert Sorting ─────────────────────────────────────────────────────────────

def test_alerts_sorted_by_urgency(isolated_finance_dir):
    today = date.today()
    year, month = today.year, today.month
    budget_dir = get_finance_dir() / "budgets"
    budget_dir.mkdir(parents=True, exist_ok=True)
    budget_path = budget_dir / f"{year}-{month:02d}.json"
    # One overspend (critical) + one healthy
    budget_path.write_text(json.dumps({
        "categories": {
            "Rent": {"planned": 1000, "actual": 1200},
        }
    }))

    goals_dir = get_finance_dir() / "goals"
    goals_dir.mkdir(parents=True, exist_ok=True)
    deadline = (date.today() + timedelta(days=20)).isoformat()
    (goals_dir / "goals.json").write_text(json.dumps({
        "goals": [{
            "name": "Urlaub",
            "target_amount": 1500,
            "current_amount": 500,
            "deadline": deadline,
            "currency": "EUR",
        }]
    }))

    alerts = get_session_alerts({})
    urgencies = [a["urgency"] for a in alerts]
    order = {u: i for i, u in enumerate(URGENCY_LEVELS)}
    assert urgencies == sorted(urgencies, key=lambda u: order.get(u, 99))


# ── Format ────────────────────────────────────────────────────────────────────

def test_format_alerts_empty():
    assert format_alerts([]) == ""


def test_format_alerts_nonempty():
    alerts = [{
        "urgency": "warning",
        "domain": "budget",
        "title": "Test alert",
        "detail": "Some detail",
        "action": "Do something",
    }]
    output = format_alerts(alerts)
    assert "Test alert" in output
    assert "Do something" in output


def test_get_session_alerts_returns_list(isolated_finance_dir):
    result = get_session_alerts({})
    assert isinstance(result, list)
