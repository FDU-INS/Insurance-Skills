"""Tests for investment_tracker.py."""
from investment_tracker import (
    get_portfolio, add_holding, update_holding, delete_holding,
    calculate_allocation, calculate_total_return, suggest_rebalance,
    calculate_fire_number, project_portfolio_growth,
    take_portfolio_snapshot, format_portfolio_display,
)


def test_empty_portfolio(isolated_finance_dir):
    p = get_portfolio()
    assert p["holdings"] == []


def test_add_holding(isolated_finance_dir):
    h = add_holding({"symbol": "VWCE", "name": "Vanguard All-World", "type": "etf",
                      "units": 50, "cost_basis": 5000, "current_value": 6200})
    assert h["symbol"] == "VWCE"
    assert h["current_value"] == 6200


def test_total_return(isolated_finance_dir):
    add_holding({"symbol": "VWCE", "type": "etf", "cost_basis": 5000, "current_value": 6200})
    add_holding({"symbol": "BND", "type": "bond", "cost_basis": 3000, "current_value": 3100})
    ret = calculate_total_return()
    assert ret["total_gain_loss"] == 1300.0
    assert ret["total_return_pct"] > 0


def test_allocation(isolated_finance_dir):
    add_holding({"symbol": "VWCE", "type": "etf", "current_value": 7000})
    add_holding({"symbol": "BND", "type": "bond", "current_value": 3000})
    alloc = calculate_allocation()
    assert alloc["allocation"]["etf"]["pct"] == 70.0
    assert alloc["allocation"]["bond"]["pct"] == 30.0


def test_rebalance_suggestions(isolated_finance_dir):
    add_holding({"symbol": "VWCE", "type": "etf", "current_value": 8000})
    add_holding({"symbol": "BND", "type": "bond", "current_value": 2000})
    portfolio = get_portfolio()
    portfolio["target_allocation"] = {"etf": 70, "bond": 30}
    from finance_storage import save_json, get_portfolio_path
    save_json(get_portfolio_path(), portfolio)
    suggestions = suggest_rebalance()
    assert len(suggestions) > 0


def test_fire_number(isolated_finance_dir):
    add_holding({"symbol": "VWCE", "type": "etf", "current_value": 100000})
    fire = calculate_fire_number(30000)
    assert fire["fire_number"] == 750000.0
    assert fire["progress_pct"] > 0


def test_project_growth(isolated_finance_dir):
    add_holding({"symbol": "VWCE", "type": "etf", "current_value": 10000})
    proj = project_portfolio_growth(500, annual_return_pct=0.07, years=5)
    assert len(proj) == 5
    assert proj[-1]["balance"] > 10000 + 500 * 60  # growth > just contributions


def test_snapshot(isolated_finance_dir):
    add_holding({"symbol": "VWCE", "type": "etf", "current_value": 5000})
    snap = take_portfolio_snapshot()
    assert snap["total_value"] == 5000


def test_format_display(isolated_finance_dir):
    add_holding({"symbol": "VWCE", "name": "Vanguard", "type": "etf",
                  "cost_basis": 5000, "current_value": 6200})
    display = format_portfolio_display()
    assert "VWCE" in display
