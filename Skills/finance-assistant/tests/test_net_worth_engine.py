"""Tests for net_worth_engine.py."""
from account_manager import add_account
from investment_tracker import add_holding
from debt_optimizer import add_debt
from net_worth_engine import (
    calculate_net_worth, take_snapshot, get_snapshots,
    calculate_net_worth_trend, format_net_worth_display,
)


def test_empty_net_worth(isolated_finance_dir):
    nw = calculate_net_worth()
    assert nw["net_worth"] == 0
    assert nw["total_assets"] == 0


def test_net_worth_with_accounts(isolated_finance_dir):
    add_account({"name": "Checking", "type": "checking", "current_balance": 5000})
    add_account({"name": "Savings", "type": "savings", "current_balance": 10000})
    add_account({"name": "CC", "type": "credit_card", "current_balance": -500})
    nw = calculate_net_worth()
    assert nw["breakdown"]["cash_and_savings"] == 15000.0
    assert nw["breakdown"]["credit_card_balance"] == 500.0


def test_net_worth_with_investments(isolated_finance_dir):
    add_account({"name": "Checking", "type": "checking", "current_balance": 5000})
    add_holding({"symbol": "VWCE", "type": "etf", "current_value": 20000})
    nw = calculate_net_worth()
    assert nw["total_assets"] == 25000.0
    assert nw["breakdown"]["investments"] == 20000.0


def test_net_worth_with_debt(isolated_finance_dir):
    add_account({"name": "Checking", "type": "checking", "current_balance": 10000})
    add_debt({"name": "Loan", "balance": 15000, "interest_rate": 5, "minimum_payment": 200})
    nw = calculate_net_worth()
    assert nw["net_worth"] == -5000.0


def test_take_snapshot(isolated_finance_dir):
    add_account({"name": "Checking", "type": "checking", "current_balance": 5000})
    snap = take_snapshot()
    assert snap["net_worth"] == 5000.0
    assert snap["date"] is not None


def test_get_snapshots(isolated_finance_dir):
    add_account({"name": "Checking", "type": "checking", "current_balance": 5000})
    take_snapshot()
    snaps = get_snapshots()
    assert len(snaps) == 1


def test_trend_no_history(isolated_finance_dir):
    trend = calculate_net_worth_trend()
    assert trend["trend"] == "no_history"


def test_format_display(isolated_finance_dir):
    add_account({"name": "Checking", "type": "checking", "current_balance": 8000})
    add_holding({"symbol": "VWCE", "type": "etf", "current_value": 12000})
    display = format_net_worth_display()
    assert "Net Worth" in display
    assert "20,000" in display
