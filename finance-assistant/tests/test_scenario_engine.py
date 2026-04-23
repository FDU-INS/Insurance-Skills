"""Tests for scenario_engine.py."""
from scenario_engine import (
    compare_salary_packages, compare_mortgage_options,
    project_fire_timeline, compare_debt_payoff_vs_invest,
    compare_rent_vs_buy,
)


def test_salary_comparison():
    result = compare_salary_packages([
        {"label": "Current", "annual_gross": 65000},
        {"label": "New Offer", "annual_gross": 75000, "benefits_value": 1200},
    ])
    assert len(result["packages"]) == 2
    assert result["best_option"]["label"] == "New Offer"


def test_mortgage_comparison():
    result = compare_mortgage_options([
        {"label": "Bank A", "loan_amount": 300000, "interest_rate": 3.5, "term_years": 25},
        {"label": "Bank B", "loan_amount": 300000, "interest_rate": 3.0, "term_years": 30},
    ])
    assert len(result["options"]) == 2
    assert result["best_option"] is not None


def test_fire_projection():
    result = project_fire_timeline(
        current_savings=50000, monthly_contribution=1500,
        annual_expenses=30000,
    )
    assert result["fire_number"] == 750000.0
    assert result["years_to_fire"] > 0
    assert result["achievable"] is True
    assert len(result["milestones"]) > 0


def test_fire_unreachable():
    result = project_fire_timeline(
        current_savings=0, monthly_contribution=10,
        annual_expenses=100000,
    )
    assert result["fire_number"] == 2500000.0


def test_debt_vs_invest():
    result = compare_debt_payoff_vs_invest(
        debt_balance=10000, debt_rate=5,
        investment_return=8, monthly_available=500,
    )
    assert result["recommendation"] in ("pay_debt_first", "invest")
    assert result["difference"] > 0


def test_rent_vs_buy():
    result = compare_rent_vs_buy(
        monthly_rent=1200, home_price=400000,
        down_payment=80000, mortgage_rate=3.5,
    )
    assert result["recommendation"] in ("buy", "rent")
    assert result["buy"]["monthly_mortgage"] > 0
    assert result["rent"]["total_rent_paid"] > 0
    assert result["years"] == 30
