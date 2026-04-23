"""
Tests for household.py.

Uses a temporary .finance directory to avoid touching real data.
"""

import os
import sys
import json
import tempfile
import pytest

scripts_dir = os.path.join(os.path.dirname(__file__), "..", "scripts")
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)


@pytest.fixture(autouse=True)
def isolated_finance_dir(tmp_path, monkeypatch):
    """Each test gets a fresh .finance/ directory."""
    monkeypatch.setenv("FINANCE_PROJECT_DIR", str(tmp_path))
    # Force reimport so finance_storage picks up the new env var
    for mod in ["finance_storage", "household", "currency"]:
        if mod in sys.modules:
            del sys.modules[mod]
    yield tmp_path


# ── create_household ──────────────────────────────────────────────────────────

def test_create_household_basic():
    from household import create_household, get_household

    result = create_household("Flat 3B", ["alice", "bob", "carol"])
    assert result["name"] == "Flat 3B"
    assert result["members"] == ["alice", "bob", "carol"]

    # Persisted
    loaded = get_household()
    assert loaded["name"] == "Flat 3B"
    assert "carol" in loaded["members"]


def test_create_household_empty_members_raises():
    from household import create_household

    with pytest.raises(ValueError, match="at least one member"):
        create_household("Empty Flat", [])


def test_create_household_overwrites_existing():
    from household import create_household, get_household

    create_household("Old Flat", ["alice"])
    create_household("New Flat", ["bob", "carol"])

    loaded = get_household()
    assert loaded["name"] == "New Flat"
    assert "alice" not in loaded["members"]


# ── get_household ─────────────────────────────────────────────────────────────

def test_get_household_returns_empty_when_none():
    from household import get_household

    result = get_household()
    assert result == {}


# ── log_shared_expense ────────────────────────────────────────────────────────

def test_log_shared_expense_equal_split():
    from household import create_household, log_shared_expense

    create_household("Test Flat", ["alice", "bob"])
    result = log_shared_expense(
        amount=60.0,
        category="food",
        paid_by="alice",
        description="Weekly groceries",
    )

    expense = result["expense"]
    assert expense["amount"] == 60.0
    assert expense["paid_by"] == "alice"
    assert expense["category"] == "food"
    # Equal split: alice and bob each owe 0.5
    split = expense["split"]
    assert abs(split["alice"] - 0.5) < 0.001
    assert abs(split["bob"] - 0.5) < 0.001


def test_log_shared_expense_custom_split():
    from household import create_household, log_shared_expense

    create_household("Test Flat", ["alice", "bob"])
    result = log_shared_expense(
        amount=100.0,
        category="housing",
        paid_by="alice",
        split={"alice": 0.6, "bob": 0.4},
    )

    split = result["expense"]["split"]
    assert abs(split["alice"] - 0.6) < 0.001
    assert abs(split["bob"] - 0.4) < 0.001


def test_log_shared_expense_normalizes_fractions():
    """Fractions that don't sum to 1 should be normalized."""
    from household import create_household, log_shared_expense

    create_household("Test Flat", ["alice", "bob"])
    result = log_shared_expense(
        amount=100.0,
        category="utilities",
        paid_by="bob",
        split={"alice": 2.0, "bob": 1.0},  # 2:1 ratio, sums to 3 not 1
    )

    split = result["expense"]["split"]
    total = sum(split.values())
    assert abs(total - 1.0) < 0.001
    assert abs(split["alice"] - 2/3) < 0.001
    assert abs(split["bob"] - 1/3) < 0.001


def test_log_shared_expense_multiple_expenses():
    """Multiple expenses accumulate correctly."""
    from household import create_household, log_shared_expense, get_shared_balance

    create_household("Test Flat", ["alice", "bob"])
    log_shared_expense(60.0, "food", "alice")  # alice pays 60; each owes 30
    log_shared_expense(40.0, "utilities", "bob")  # bob pays 40; each owes 20

    # alice: paid 60, owes 30+20=50 → net +10
    # bob: paid 40, owes 30+20=50 → net -10
    balance = get_shared_balance()
    balances = balance["balances"]

    assert abs(balances["alice"] - 10.0) < 0.01
    assert abs(balances["bob"] + 10.0) < 0.01


# ── get_shared_balance ────────────────────────────────────────────────────────

def test_get_shared_balance_empty():
    from household import create_household, get_shared_balance

    create_household("Test Flat", ["alice", "bob"])
    result = get_shared_balance()

    assert result["balances"] == {}
    assert result["settle_up"] == []


def test_get_shared_balance_settle_up_direction():
    """Debtor pays creditor in settle_up."""
    from household import create_household, log_shared_expense, get_shared_balance

    create_household("Flat", ["alice", "bob"])
    # Alice pays 100 for equal split → alice is owed 50 by bob
    log_shared_expense(100.0, "food", "alice")

    result = get_shared_balance()
    settle = result["settle_up"]

    assert len(settle) == 1
    assert settle[0]["from"] == "bob"
    assert settle[0]["to"] == "alice"
    assert abs(settle[0]["amount"] - 50.0) < 0.01


def test_settle_up_three_members():
    """Settle-up with three members produces minimal transfers."""
    from household import create_household, log_shared_expense, get_shared_balance

    create_household("Flat", ["alice", "bob", "carol"])
    # alice pays 90 → each owes 30; alice net: +60, bob: -30, carol: -30
    log_shared_expense(90.0, "rent", "alice")

    result = get_shared_balance()
    settle = result["settle_up"]

    # Should be 2 transfers: bob→alice and carol→alice
    assert len(settle) == 2
    for t in settle:
        assert t["to"] == "alice"
        assert abs(t["amount"] - 30.0) < 0.01


def test_settle_up_already_balanced():
    """If all settled, no transfers needed."""
    from household import create_household, log_shared_expense, get_shared_balance

    create_household("Flat", ["alice", "bob"])
    log_shared_expense(100.0, "food", "alice")
    log_shared_expense(100.0, "utilities", "bob")

    result = get_shared_balance()
    # Both paid 100, equal split → both owe 50, both get 50 → net 0
    assert result["settle_up"] == []


# ── get_shared_budget_status ──────────────────────────────────────────────────

def test_shared_budget_status_current_month():
    from household import create_household, log_shared_expense, get_shared_budget_status
    from datetime import datetime

    create_household("Flat", ["alice", "bob"])
    log_shared_expense(60.0, "food", "alice")
    log_shared_expense(40.0, "utilities", "bob")

    status = get_shared_budget_status()
    current_month = datetime.now().strftime("%Y-%m")

    assert status["month"] == current_month
    assert abs(status["total_spend"] - 100.0) < 0.01
    assert "food" in status["by_category"]
    assert "utilities" in status["by_category"]


def test_shared_budget_status_member_totals():
    from household import create_household, log_shared_expense, get_shared_budget_status

    create_household("Flat", ["alice", "bob"])
    # alice pays 100, split equally → each responsible for 50
    log_shared_expense(100.0, "food", "alice")

    status = get_shared_budget_status()
    member_totals = status["member_totals"]

    assert abs(member_totals.get("alice", 0) - 50.0) < 0.01
    assert abs(member_totals.get("bob", 0) - 50.0) < 0.01


def test_shared_budget_status_filters_by_month():
    """Expenses from other months should not appear in current month status."""
    import json
    from household import create_household, log_shared_expense, get_shared_budget_status, _shared_expenses_path
    from finance_storage import load_json, save_json

    create_household("Flat", ["alice", "bob"])
    log_shared_expense(100.0, "food", "alice")  # current month

    # Manually add an old expense
    path = _shared_expenses_path()
    data = load_json(path, default={"expenses": []})
    data["expenses"].append({
        "id": "old123",
        "date": "2020-01-15",
        "amount": 999.0,
        "category": "rent",
        "paid_by": "bob",
        "split": {"alice": 0.5, "bob": 0.5},
        "description": "Old rent",
        "currency": "EUR",
        "created_at": "2020-01-15T00:00:00",
    })
    save_json(path, data)

    status = get_shared_budget_status()
    assert abs(status["total_spend"] - 100.0) < 0.01  # old expense not included


# ── format_household_summary ──────────────────────────────────────────────────

def test_format_household_summary_no_household():
    from household import format_household_summary

    text = format_household_summary()
    assert "No household" in text


def test_format_household_summary_with_data():
    from household import create_household, log_shared_expense, format_household_summary

    create_household("Sunny Flat", ["alice", "bob"])
    log_shared_expense(60.0, "food", "alice", description="Groceries")

    text = format_household_summary()
    assert "Sunny Flat" in text
    assert "alice" in text
    assert "bob" in text
    assert "60" in text


def test_format_household_summary_settle_up_instructions():
    from household import create_household, log_shared_expense, format_household_summary

    create_household("Flat", ["alice", "bob"])
    log_shared_expense(100.0, "food", "alice")

    text = format_household_summary()
    assert "→" in text  # settle-up arrow present
    assert "alice" in text
    assert "bob" in text
