"""Tests for transaction_logger.py."""
from transaction_logger import (
    add_transaction, get_transactions, get_totals,
    get_summary_display, auto_categorize, deduplicate,
)


def test_add_transaction(isolated_finance_dir):
    result = add_transaction("2026-04-01", "expense", -45.50, "food", "REWE Supermarket")
    txn = result["transaction_added"]
    assert txn["amount"] == -45.50
    assert txn["category"] == "food"


def test_get_transactions(isolated_finance_dir):
    add_transaction("2026-04-01", "expense", -50, "food", "REWE")
    add_transaction("2026-04-02", "expense", -30, "dining", "Restaurant")
    txns = get_transactions(year=2026)
    assert len(txns) == 2


def test_get_transactions_filtered(isolated_finance_dir):
    add_transaction("2026-04-01", "expense", -50, "food", "REWE")
    add_transaction("2026-04-01", "income", 3000, "salary", "Gehalt")
    txns = get_transactions(year=2026, type="income")
    assert len(txns) == 1
    assert txns[0]["category"] == "salary"


def test_get_totals(isolated_finance_dir):
    add_transaction("2026-04-01", "expense", -100, "food", "REWE")
    add_transaction("2026-04-02", "expense", -50, "food", "ALDI")
    add_transaction("2026-04-01", "income", 3000, "salary", "Gehalt")
    totals = get_totals(year=2026)
    assert totals["food"]["expense"] == 150.0
    assert totals["salary"]["income"] == 3000.0


def test_auto_categorize():
    cat, _ = auto_categorize("REWE Berlin Supermarkt", -45)
    assert cat == "food"
    cat, _ = auto_categorize("Netflix Subscription", -12.99)
    assert cat == "subscriptions"
    cat, _ = auto_categorize("Gehalt April", 3500)
    assert cat == "salary"


def test_deduplicate():
    existing = [{"date": "2026-04-01", "amount": -45.50, "description": "REWE"}]
    new = [
        {"date": "2026-04-01", "amount": -45.50, "description": "REWE"},  # duplicate
        {"date": "2026-04-02", "amount": -30.00, "description": "ALDI"},  # unique
    ]
    unique = deduplicate(new, existing)
    assert len(unique) == 1
    assert unique[0]["description"] == "ALDI"


def test_summary_display(isolated_finance_dir):
    add_transaction("2026-04-01", "expense", -100, "food", "REWE")
    display = get_summary_display(year=2026, month=4)
    assert "food" in display.lower() or "Food" in display
