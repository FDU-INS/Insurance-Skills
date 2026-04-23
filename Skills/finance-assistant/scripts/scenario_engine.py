"""
Finance Assistant Scenario Engine.

Expanded from TaxDE scenario_engine.py with new financial scenarios:
salary packages, freelance break-even, mortgage comparisons, FIRE projections,
debt-vs-invest, and rent-vs-buy.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Optional

try:
    from profile_manager import get_profile
except ImportError:
    import os, sys
    sys.path.insert(0, os.path.dirname(__file__))
    from profile_manager import get_profile


# ── Salary Package Comparison (from TaxDE) ───────────────────────────────────

def compare_salary_packages(
    packages: list[dict],
    profile: Optional[dict] = None,
    projection_years: int = 3,
    annual_raise_pct: float = 0.0,
) -> dict:
    """Compare employment packages with multi-year projections."""
    if not packages:
        return {"packages": [], "best_option": None}

    evaluations = []
    for pkg in packages:
        gross = float(pkg.get("annual_gross", 0))
        benefits = float(pkg.get("benefits_value", 0))
        bav = float(pkg.get("bav_contribution", 0))

        # Simple net estimation (locale-independent)
        estimated_tax_rate = 0.25  # Default estimate
        estimated_social_rate = 0.20
        net = gross * (1 - estimated_tax_rate - estimated_social_rate) + benefits - bav * 0.5

        projections = []
        for yr in range(projection_years):
            factor = (1 + annual_raise_pct) ** yr
            projections.append({
                "year": yr + 1,
                "annual_gross": round(gross * factor, 2),
                "estimated_annual_net": round(net * factor, 2),
            })

        evaluations.append({
            "label": pkg.get("label", f"Package {len(evaluations) + 1}"),
            "annual_gross": gross,
            "estimated_annual_net": round(net, 2),
            "estimated_monthly_net": round(net / 12, 2),
            "projections": projections,
            "multi_year_net_total": round(sum(p["estimated_annual_net"] for p in projections), 2),
        })

    best = max(evaluations, key=lambda e: e["estimated_annual_net"])
    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "packages": evaluations,
        "best_option": best,
        "projection_years": projection_years,
        "note": "Tax estimates are approximate. Use the tax module for precise locale-specific calculations.",
    }


# ── Mortgage Comparison ──────────────────────────────────────────────────────

def compare_mortgage_options(options: list[dict]) -> dict:
    """Compare mortgage offers with total cost analysis."""
    evaluations = []
    for opt in options:
        amount = float(opt.get("loan_amount", 0))
        rate = float(opt.get("interest_rate", 0)) / 100
        years = int(opt.get("term_years", 30))
        monthly_rate = rate / 12
        months = years * 12

        if monthly_rate > 0:
            payment = amount * monthly_rate / (1 - (1 + monthly_rate) ** -months)
        else:
            payment = amount / months

        total_paid = payment * months
        total_interest = total_paid - amount

        evaluations.append({
            "label": opt.get("label", f"Option {len(evaluations) + 1}"),
            "loan_amount": amount,
            "interest_rate": float(opt.get("interest_rate", 0)),
            "term_years": years,
            "monthly_payment": round(payment, 2),
            "total_paid": round(total_paid, 2),
            "total_interest": round(total_interest, 2),
        })

    best = min(evaluations, key=lambda e: e["total_interest"]) if evaluations else None
    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "options": evaluations,
        "best_option": best,
    }


# ── FIRE Projection ─────────────────────────────────────────────────────────

def project_fire_timeline(
    current_savings: float,
    monthly_contribution: float,
    annual_expenses: float,
    annual_return_pct: float = 0.07,
    withdrawal_rate: float = 0.04,
    inflation_rate: float = 0.02,
) -> dict:
    """Project timeline to financial independence."""
    fire_number = annual_expenses / withdrawal_rate
    monthly_return = annual_return_pct / 12
    balance = current_savings
    months = 0
    max_months = 12 * 60  # 60 year cap

    milestones = []
    while balance < fire_number and months < max_months:
        months += 1
        balance = balance * (1 + monthly_return) + monthly_contribution
        if months % 12 == 0:
            milestones.append({"year": months // 12, "balance": round(balance, 2)})

    years = months / 12
    return {
        "fire_number": round(fire_number, 2),
        "current_savings": current_savings,
        "monthly_contribution": monthly_contribution,
        "years_to_fire": round(years, 1),
        "months_to_fire": months,
        "annual_expenses": annual_expenses,
        "withdrawal_rate": withdrawal_rate,
        "annual_return_pct": annual_return_pct,
        "milestones": milestones,
        "achievable": months < max_months,
    }


# ── Debt vs Invest ───────────────────────────────────────────────────────────

def compare_debt_payoff_vs_invest(
    debt_balance: float,
    debt_rate: float,
    investment_return: float,
    monthly_available: float,
    years: int = 10,
) -> dict:
    """Compare paying off debt faster vs investing the extra money."""
    monthly_debt_rate = debt_rate / 100 / 12
    monthly_invest_rate = investment_return / 100 / 12

    # Scenario A: Pay off debt, then invest
    debt_bal = debt_balance
    months_to_payoff = 0
    total_debt_interest_a = 0.0
    while debt_bal > 0 and months_to_payoff < years * 12:
        months_to_payoff += 1
        interest = debt_bal * monthly_debt_rate
        total_debt_interest_a += interest
        debt_bal = debt_bal + interest - monthly_available
        if debt_bal < 0:
            debt_bal = 0

    invest_months_a = max(0, years * 12 - months_to_payoff)
    invest_balance_a = 0.0
    for _ in range(invest_months_a):
        invest_balance_a = invest_balance_a * (1 + monthly_invest_rate) + monthly_available

    # Scenario B: Minimum debt payments, invest the rest
    min_payment = debt_balance * 0.02  # Assume 2% minimum
    invest_extra = max(0, monthly_available - min_payment)
    debt_bal_b = debt_balance
    invest_balance_b = 0.0
    total_debt_interest_b = 0.0
    for _ in range(years * 12):
        # Debt
        interest = debt_bal_b * monthly_debt_rate
        total_debt_interest_b += interest
        debt_bal_b = max(0, debt_bal_b + interest - min_payment)
        # Invest
        invest_balance_b = invest_balance_b * (1 + monthly_invest_rate) + invest_extra

    net_a = invest_balance_a - total_debt_interest_a
    net_b = invest_balance_b - debt_bal_b - total_debt_interest_b

    return {
        "pay_debt_first": {
            "months_to_payoff": months_to_payoff,
            "total_debt_interest": round(total_debt_interest_a, 2),
            "investment_balance": round(invest_balance_a, 2),
            "net_position": round(net_a, 2),
        },
        "invest_while_paying_minimum": {
            "remaining_debt": round(debt_bal_b, 2),
            "total_debt_interest": round(total_debt_interest_b, 2),
            "investment_balance": round(invest_balance_b, 2),
            "net_position": round(net_b, 2),
        },
        "recommendation": "pay_debt_first" if net_a > net_b else "invest",
        "difference": round(abs(net_a - net_b), 2),
        "note": "This is a simplified model. Tax implications and risk tolerance matter.",
    }


# ── Rent vs Buy ──────────────────────────────────────────────────────────────

def compare_rent_vs_buy(
    monthly_rent: float,
    home_price: float,
    down_payment: float,
    mortgage_rate: float,
    years: int = 30,
    property_tax_rate: float = 0.01,
    maintenance_rate: float = 0.01,
    rent_increase: float = 0.02,
    home_appreciation: float = 0.03,
    investment_return: float = 0.07,
) -> dict:
    """Compare renting vs buying over a given period."""
    loan = home_price - down_payment
    monthly_mortgage_rate = mortgage_rate / 100 / 12
    months = years * 12

    if monthly_mortgage_rate > 0:
        mortgage_payment = loan * monthly_mortgage_rate / (1 - (1 + monthly_mortgage_rate) ** -months)
    else:
        mortgage_payment = loan / months

    # Buying costs
    total_mortgage = mortgage_payment * months
    total_property_tax = home_price * property_tax_rate * years
    total_maintenance = home_price * maintenance_rate * years
    total_buy_cost = down_payment + total_mortgage + total_property_tax + total_maintenance
    future_home_value = home_price * ((1 + home_appreciation) ** years)
    buy_net = future_home_value - total_buy_cost

    # Renting costs + investing the difference
    total_rent = 0
    invest_balance = down_payment  # Invest the down payment instead
    monthly_invest_rate = investment_return / 12
    current_rent = monthly_rent

    for yr in range(years):
        for _ in range(12):
            total_rent += current_rent
            monthly_savings = mortgage_payment + (home_price * property_tax_rate / 12) - current_rent
            if monthly_savings > 0:
                invest_balance = invest_balance * (1 + monthly_invest_rate) + monthly_savings
            else:
                invest_balance = invest_balance * (1 + monthly_invest_rate)
        current_rent *= (1 + rent_increase)

    rent_net = invest_balance - total_rent

    return {
        "buy": {
            "down_payment": down_payment,
            "monthly_mortgage": round(mortgage_payment, 2),
            "total_cost": round(total_buy_cost, 2),
            "future_home_value": round(future_home_value, 2),
            "net_position": round(buy_net, 2),
        },
        "rent": {
            "starting_monthly_rent": monthly_rent,
            "total_rent_paid": round(total_rent, 2),
            "investment_balance": round(invest_balance, 2),
            "net_position": round(rent_net, 2),
        },
        "recommendation": "buy" if buy_net > rent_net else "rent",
        "difference": round(abs(buy_net - rent_net), 2),
        "years": years,
        "assumptions": {
            "mortgage_rate": mortgage_rate,
            "rent_increase": f"{rent_increase*100:.0f}%/year",
            "home_appreciation": f"{home_appreciation*100:.0f}%/year",
            "investment_return": f"{investment_return*100:.0f}%/year",
        },
    }
