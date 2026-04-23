"""Tests for budget_engine.py."""
from budget_engine import (
    create_budget, get_budget, get_budget_variance,
    suggest_budget_from_history, format_budget_display,
)
from transaction_logger import add_transaction


def test_create_budget(isolated_finance_dir):
    budget = create_budget(2026, 4, method="custom", income_target=3500,
                           category_limits={"housing": 1200, "food": 400, "transport": 200})
    assert budget["year"] == 2026
    assert budget["month"] == 4
    assert budget["category_limits"]["housing"] == 1200


def test_get_budget(isolated_finance_dir):
    create_budget(2026, 4, income_target=3500)
    budget = get_budget(2026, 4)
    assert budget is not None
    assert budget["income_target"] == 3500


def test_50_30_20_method(isolated_finance_dir):
    budget = create_budget(2026, 4, method="50-30-20", income_target=4000)
    assert budget["method_breakdown"]["needs"] == 2000.0
    assert budget["method_breakdown"]["wants"] == 1200.0
    assert budget["method_breakdown"]["savings"] == 800.0


def test_budget_variance(isolated_finance_dir):
    create_budget(2026, 4, category_limits={"food": 400, "transport": 200})
    add_transaction("2026-04-01", "expense", -350, "food", "Groceries")
    add_transaction("2026-04-01", "expense", -250, "transport", "BVG + fuel")

    from budget_engine import update_budget_actuals
    update_budget_actuals(2026, 4)
    variance = get_budget_variance(2026, 4)

    assert variance["categories"]["food"]["status"] == "under"
    assert variance["categories"]["transport"]["status"] == "over"
    assert "transport" in variance["overspend_categories"]


def test_format_budget_display(isolated_finance_dir):
    budget = create_budget(2026, 4, income_target=3500, category_limits={"food": 400})
    display = format_budget_display(budget)
    assert "2026-04" in display
    assert "food" in display
