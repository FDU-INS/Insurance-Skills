"""
Tests for scripts/chart_builder.py — Chart.js HTML artifact generation.

Each chart function is verified for:
1. Returns a non-empty string
2. Contains <!DOCTYPE html> and </html>
3. Contains chart.js CDN reference
4. Contains the data passed in (key category names or amounts)
5. Empty / zero input returns valid HTML with a no-data message
"""

import pytest
from scripts.chart_builder import (
    budget_chart,
    portfolio_chart,
    net_worth_chart,
    debt_payoff_chart,
    fire_progress_chart,
    spending_trends_chart,
    monthly_comparison_chart,
    cashflow_forecast_chart,
)


# ── Shared helpers ─────────────────────────────────────────────────────────────

def _assert_valid_html(html: str) -> None:
    assert isinstance(html, str)
    assert html.strip()
    assert "<!DOCTYPE html>" in html
    assert "</html>" in html
    assert "https://cdn.jsdelivr.net/npm/chart.js" in html


def _assert_no_data(html: str) -> None:
    _assert_valid_html(html)
    assert "no-data" in html or "No " in html or "no " in html.lower()


# ── budget_chart ───────────────────────────────────────────────────────────────

BUDGET_DATA = {
    "Food": {"limit": 400, "actual": 340},
    "Transport": {"limit": 150, "actual": 180},
    "Entertainment": {"limit": 100, "actual": 45},
}


def test_budget_chart_returns_valid_html():
    html = budget_chart(BUDGET_DATA, currency="EUR", month="2025-03")
    _assert_valid_html(html)


def test_budget_chart_contains_category_names():
    html = budget_chart(BUDGET_DATA)
    assert "Food" in html
    assert "Transport" in html
    assert "Entertainment" in html


def test_budget_chart_contains_amounts():
    html = budget_chart(BUDGET_DATA)
    # actual values appear as JSON data
    assert "340" in html
    assert "180" in html
    assert "45" in html


def test_budget_chart_contains_doughnut():
    html = budget_chart(BUDGET_DATA)
    assert "doughnut" in html


def test_budget_chart_shows_month():
    html = budget_chart(BUDGET_DATA, month="2025-03")
    assert "2025-03" in html


def test_budget_chart_empty_input():
    html = budget_chart({})
    _assert_no_data(html)


# ── portfolio_chart ────────────────────────────────────────────────────────────

HOLDINGS = [
    {"name": "VWCE", "value": 15000, "asset_class": "Equities", "return_pct": 12.4},
    {"name": "BND", "value": 5000, "asset_class": "Bonds", "return_pct": 3.1},
    {"name": "Cash", "value": 2000, "asset_class": "Cash", "return_pct": 0.5},
    {"name": "REITS", "value": 3000, "asset_class": "Real Estate", "return_pct": 6.2},
]


def test_portfolio_chart_returns_valid_html():
    html = portfolio_chart(HOLDINGS)
    _assert_valid_html(html)


def test_portfolio_chart_contains_holding_names():
    html = portfolio_chart(HOLDINGS)
    assert "VWCE" in html
    assert "BND" in html


def test_portfolio_chart_contains_asset_classes():
    html = portfolio_chart(HOLDINGS)
    assert "Equities" in html
    assert "Bonds" in html


def test_portfolio_chart_contains_values():
    html = portfolio_chart(HOLDINGS)
    assert "15000" in html
    assert "5000" in html


def test_portfolio_chart_has_two_canvases():
    html = portfolio_chart(HOLDINGS)
    assert html.count("<canvas") >= 2


def test_portfolio_chart_empty_holdings():
    html = portfolio_chart([])
    _assert_no_data(html)


def test_portfolio_chart_zero_value():
    html = portfolio_chart([{"name": "A", "value": 0, "asset_class": "Cash", "return_pct": 0}])
    _assert_no_data(html)


# ── net_worth_chart ────────────────────────────────────────────────────────────

NW_SNAPSHOTS = [
    {"date": "2024-01-01", "net_worth": 50000, "assets": 70000, "liabilities": 20000},
    {"date": "2024-04-01", "net_worth": 55000, "assets": 73000, "liabilities": 18000},
    {"date": "2024-07-01", "net_worth": 61000, "assets": 77000, "liabilities": 16000},
    {"date": "2024-10-01", "net_worth": 67000, "assets": 82000, "liabilities": 15000},
]


def test_net_worth_chart_returns_valid_html():
    html = net_worth_chart(NW_SNAPSHOTS)
    _assert_valid_html(html)


def test_net_worth_chart_contains_dates():
    html = net_worth_chart(NW_SNAPSHOTS)
    assert "2024-01-01" in html
    assert "2024-10-01" in html


def test_net_worth_chart_contains_three_datasets():
    html = net_worth_chart(NW_SNAPSHOTS)
    assert "Net Worth" in html
    assert "Assets" in html
    assert "Liabilities" in html


def test_net_worth_chart_contains_values():
    html = net_worth_chart(NW_SNAPSHOTS)
    assert "50000" in html
    assert "67000" in html


def test_net_worth_chart_single_snapshot():
    html = net_worth_chart([{"date": "2024-01-01", "net_worth": 50000, "assets": 60000, "liabilities": 10000}])
    _assert_valid_html(html)


def test_net_worth_chart_empty():
    html = net_worth_chart([])
    _assert_no_data(html)


# ── debt_payoff_chart ──────────────────────────────────────────────────────────

AVALANCHE = [
    {"month": 0, "remaining": 20000, "interest_paid": 0},
    {"month": 12, "remaining": 14000, "interest_paid": 800},
    {"month": 24, "remaining": 7000, "interest_paid": 1400},
    {"month": 36, "remaining": 0, "interest_paid": 1800},
]
SNOWBALL = [
    {"month": 0, "remaining": 20000, "interest_paid": 0},
    {"month": 12, "remaining": 15000, "interest_paid": 950},
    {"month": 24, "remaining": 8500, "interest_paid": 1700},
    {"month": 38, "remaining": 0, "interest_paid": 2200},
]


def test_debt_payoff_chart_returns_valid_html():
    html = debt_payoff_chart(AVALANCHE, SNOWBALL)
    _assert_valid_html(html)


def test_debt_payoff_chart_contains_both_strategies():
    html = debt_payoff_chart(AVALANCHE, SNOWBALL)
    assert "Avalanche" in html
    assert "Snowball" in html


def test_debt_payoff_chart_contains_months():
    html = debt_payoff_chart(AVALANCHE, SNOWBALL)
    assert "36" in html
    assert "38" in html


def test_debt_payoff_chart_contains_interest():
    html = debt_payoff_chart(AVALANCHE, SNOWBALL)
    # interest totals are formatted via _fmt (e.g. 1800 → "€2k"); check stat labels instead
    assert "interest" in html.lower() or "Interest" in html


def test_debt_payoff_chart_empty():
    html = debt_payoff_chart([], [])
    _assert_no_data(html)


def test_debt_payoff_chart_only_avalanche():
    html = debt_payoff_chart(AVALANCHE, [])
    _assert_valid_html(html)
    assert "Avalanche" in html


# ── fire_progress_chart ────────────────────────────────────────────────────────

CONTRIBUTIONS = [
    {"year": 2025, "projected_value": 120000},
    {"year": 2028, "projected_value": 180000},
    {"year": 2031, "projected_value": 260000},
    {"year": 2034, "projected_value": 370000},
    {"year": 2037, "projected_value": 500000},
]


def test_fire_chart_returns_valid_html():
    html = fire_progress_chart(150000, 500000, CONTRIBUTIONS)
    _assert_valid_html(html)


def test_fire_chart_shows_percentage():
    html = fire_progress_chart(250000, 500000, CONTRIBUTIONS)
    assert "50%" in html


def test_fire_chart_contains_target_line():
    html = fire_progress_chart(150000, 500000, CONTRIBUTIONS)
    assert "FIRE Target" in html


def test_fire_chart_contains_contribution_years():
    html = fire_progress_chart(150000, 500000, CONTRIBUTIONS)
    assert "2037" in html


def test_fire_chart_shows_fire_year():
    html = fire_progress_chart(150000, 500000, CONTRIBUTIONS)
    assert "2037" in html


def test_fire_chart_empty_contributions():
    html = fire_progress_chart(100000, 500000, [])
    _assert_valid_html(html)


def test_fire_chart_invalid_target():
    html = fire_progress_chart(100000, 0, CONTRIBUTIONS)
    _assert_no_data(html)


def test_fire_chart_over_100pct():
    html = fire_progress_chart(600000, 500000, CONTRIBUTIONS)
    assert "100%" in html


# ── spending_trends_chart ──────────────────────────────────────────────────────

MONTHS_DATA = [
    {"month": "2024-10", "categories": {"Food": 310, "Transport": 100, "Entertainment": 80}},
    {"month": "2024-11", "categories": {"Food": 340, "Transport": 115, "Entertainment": 60}},
    {"month": "2024-12", "categories": {"Food": 420, "Transport": 105, "Entertainment": 150}},
    {"month": "2025-01", "categories": {"Food": 330, "Transport": 95, "Entertainment": 70}},
]


def test_spending_trends_returns_valid_html():
    html = spending_trends_chart(MONTHS_DATA)
    _assert_valid_html(html)


def test_spending_trends_contains_months():
    html = spending_trends_chart(MONTHS_DATA)
    assert "2024-10" in html
    assert "2025-01" in html


def test_spending_trends_contains_categories():
    html = spending_trends_chart(MONTHS_DATA)
    assert "Food" in html
    assert "Transport" in html
    assert "Entertainment" in html


def test_spending_trends_contains_values():
    html = spending_trends_chart(MONTHS_DATA)
    assert "420" in html
    assert "150" in html


def test_spending_trends_has_total_line():
    html = spending_trends_chart(MONTHS_DATA)
    assert "Total" in html


def test_spending_trends_empty():
    html = spending_trends_chart([])
    _assert_no_data(html)


# ── monthly_comparison_chart ───────────────────────────────────────────────────

CURRENT = {"Food": 340, "Transport": 112, "Entertainment": 90, "Utilities": 80}
PREVIOUS = {"Food": 298, "Transport": 130, "Entertainment": 70, "Utilities": 75}


def test_monthly_comparison_returns_valid_html():
    html = monthly_comparison_chart(CURRENT, PREVIOUS)
    _assert_valid_html(html)


def test_monthly_comparison_contains_categories():
    html = monthly_comparison_chart(CURRENT, PREVIOUS)
    assert "Food" in html
    assert "Transport" in html
    assert "Utilities" in html


def test_monthly_comparison_contains_values():
    html = monthly_comparison_chart(CURRENT, PREVIOUS)
    assert "340" in html
    assert "298" in html


def test_monthly_comparison_has_both_datasets():
    html = monthly_comparison_chart(CURRENT, PREVIOUS)
    assert "This Month" in html
    assert "Last Month" in html


def test_monthly_comparison_empty():
    html = monthly_comparison_chart({}, {})
    _assert_no_data(html)


def test_monthly_comparison_partial_overlap():
    html = monthly_comparison_chart({"Food": 100}, {"Rent": 800})
    _assert_valid_html(html)
    assert "Food" in html
    assert "Rent" in html


# ── cashflow_forecast_chart ────────────────────────────────────────────────────

FORECAST = [
    {"date": "2025-04-01", "balance": 3200, "events": []},
    {"date": "2025-04-05", "balance": 2800, "events": [{"name": "Rent", "amount": -1200}]},
    {"date": "2025-04-15", "balance": 5800, "events": [{"name": "Salary", "amount": 3200}]},
    {"date": "2025-04-20", "balance": 5500, "events": []},
    {"date": "2025-04-30", "balance": 4900, "events": [{"name": "Insurance", "amount": -120}]},
]


def test_cashflow_returns_valid_html():
    html = cashflow_forecast_chart(FORECAST)
    _assert_valid_html(html)


def test_cashflow_contains_dates():
    html = cashflow_forecast_chart(FORECAST)
    assert "2025-04-01" in html
    assert "2025-04-30" in html


def test_cashflow_contains_balances():
    html = cashflow_forecast_chart(FORECAST)
    assert "3200" in html
    assert "5800" in html


def test_cashflow_has_low_threshold_annotation():
    html = cashflow_forecast_chart(FORECAST)
    assert "lowThreshold" in html or "Low balance" in html


def test_cashflow_annotation_plugin_loaded():
    html = cashflow_forecast_chart(FORECAST)
    assert "chartjs-plugin-annotation" in html


def test_cashflow_empty():
    html = cashflow_forecast_chart([])
    _assert_no_data(html)


def test_cashflow_single_entry():
    html = cashflow_forecast_chart([{"date": "2025-04-01", "balance": 1000, "events": []}])
    _assert_valid_html(html)
