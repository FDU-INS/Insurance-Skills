"""Tests for account_manager.py."""
from account_manager import (
    get_accounts, add_account, update_account, delete_account,
    get_account, get_total_balance, display_accounts,
)


def test_empty_accounts(isolated_finance_dir):
    assert get_accounts() == []


def test_add_account(isolated_finance_dir):
    acc = add_account({"name": "DKB Checking", "type": "checking", "institution": "DKB", "current_balance": 5000})
    assert acc["id"] == "dkb-checking"
    assert acc["is_asset"] is True
    assert acc["current_balance"] == 5000


def test_credit_card_is_liability(isolated_finance_dir):
    acc = add_account({"name": "VISA", "type": "credit_card", "current_balance": -450})
    assert acc["is_asset"] is False


def test_get_account(isolated_finance_dir):
    add_account({"name": "Test", "type": "savings", "current_balance": 1000})
    assert get_account("test") is not None
    assert get_account("nonexistent") is None


def test_update_account(isolated_finance_dir):
    add_account({"name": "Test", "type": "savings", "current_balance": 1000})
    updated = update_account("test", {"current_balance": 2000})
    assert updated["current_balance"] == 2000


def test_delete_account(isolated_finance_dir):
    add_account({"name": "Test", "type": "savings"})
    assert delete_account("test") is True
    assert delete_account("test") is False
    assert len(get_accounts()) == 0


def test_total_balance(isolated_finance_dir):
    add_account({"name": "Checking", "type": "checking", "current_balance": 5000})
    add_account({"name": "Savings", "type": "savings", "current_balance": 10000})
    add_account({"name": "Card", "type": "credit_card", "current_balance": -500})
    totals = get_total_balance()
    assert totals["assets"] == 15000.0
    assert totals["liabilities"] == 500.0
    assert totals["net"] == 14500.0


def test_display_accounts(isolated_finance_dir):
    add_account({"name": "DKB", "type": "checking", "institution": "DKB", "current_balance": 3000})
    display = display_accounts()
    assert "DKB" in display
    assert "3,000" in display


def test_unique_ids(isolated_finance_dir):
    add_account({"name": "Test", "type": "checking"})
    add_account({"name": "Test", "type": "checking"})
    accounts = get_accounts()
    ids = [a["id"] for a in accounts]
    assert len(set(ids)) == 2  # IDs are unique
