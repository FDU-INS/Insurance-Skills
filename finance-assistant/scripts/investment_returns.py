"""
Finance Assistant Investment Return Calculations.

Time-Weighted Return (TWR) and approximate XIRR for portfolio performance.
"""

from __future__ import annotations

import math
from datetime import date, datetime
from typing import Optional

try:
    from finance_storage import load_json
    from investment_tracker import get_portfolio
except ImportError:
    import os, sys
    sys.path.insert(0, os.path.dirname(__file__))
    from finance_storage import load_json
    from investment_tracker import get_portfolio


def calculate_simple_return(cost_basis: float, current_value: float) -> dict:
    """Simple return calculation."""
    gain = current_value - cost_basis
    pct = (gain / cost_basis * 100) if cost_basis > 0 else 0
    return {
        "cost_basis": round(cost_basis, 2),
        "current_value": round(current_value, 2),
        "gain_loss": round(gain, 2),
        "return_pct": round(pct, 2),
    }


def calculate_annualized_return(
    cost_basis: float,
    current_value: float,
    years: float,
) -> dict:
    """Annualized return (CAGR)."""
    if cost_basis <= 0 or years <= 0:
        return {"annualized_return_pct": 0, "years": years}

    cagr = (current_value / cost_basis) ** (1 / years) - 1
    return {
        "annualized_return_pct": round(cagr * 100, 2),
        "total_return_pct": round((current_value / cost_basis - 1) * 100, 2),
        "years": round(years, 2),
    }


def calculate_twr(snapshots: list[dict]) -> dict:
    """
    Time-Weighted Return from portfolio snapshots.
    Each snapshot needs: {"date": "YYYY-MM-DD", "total_value": float}
    """
    if len(snapshots) < 2:
        return {"twr_pct": 0, "periods": 0, "error": "Need at least 2 snapshots"}

    # Calculate sub-period returns
    sub_returns = []
    for i in range(1, len(snapshots)):
        prev_val = float(snapshots[i-1].get("total_value", 0))
        curr_val = float(snapshots[i].get("total_value", 0))
        if prev_val > 0:
            sub_return = curr_val / prev_val
            sub_returns.append(sub_return)

    if not sub_returns:
        return {"twr_pct": 0, "periods": 0}

    # TWR = product of (1 + sub_returns) - 1
    cumulative = 1.0
    for r in sub_returns:
        cumulative *= r
    twr = cumulative - 1

    # Annualize if we have date information
    first_date = date.fromisoformat(snapshots[0]["date"])
    last_date = date.fromisoformat(snapshots[-1]["date"])
    days = (last_date - first_date).days
    years = days / 365.25

    annualized = 0.0
    if years > 0 and cumulative > 0:
        annualized = cumulative ** (1 / years) - 1

    return {
        "twr_pct": round(twr * 100, 2),
        "annualized_twr_pct": round(annualized * 100, 2),
        "periods": len(sub_returns),
        "start_date": snapshots[0]["date"],
        "end_date": snapshots[-1]["date"],
        "days": days,
    }


def approximate_xirr(
    cashflows: list[dict],
    current_value: float,
    as_of: Optional[str] = None,
) -> dict:
    """
    Approximate XIRR (internal rate of return with dates).

    cashflows: [{"date": "YYYY-MM-DD", "amount": float}]
    Negative amounts = money invested, positive = money withdrawn.
    current_value is treated as a final positive cashflow on as_of date.

    Uses Newton's method to find the rate.
    """
    if not cashflows:
        return {"xirr_pct": 0, "error": "No cashflows provided"}

    as_of_date = date.fromisoformat(as_of) if as_of else date.today()

    # Add current portfolio value as final cashflow
    all_flows = []
    for cf in cashflows:
        all_flows.append((date.fromisoformat(cf["date"]), float(cf["amount"])))
    all_flows.append((as_of_date, current_value))

    # Sort by date
    all_flows.sort(key=lambda x: x[0])

    first_date = all_flows[0][0]

    def npv(rate):
        """Calculate NPV at a given rate."""
        total = 0.0
        for d, amount in all_flows:
            years = (d - first_date).days / 365.25
            if rate == -1 and years > 0:
                return float("inf")
            try:
                total += amount / ((1 + rate) ** years)
            except (OverflowError, ZeroDivisionError):
                return float("inf")
        return total

    def npv_derivative(rate):
        """Derivative of NPV for Newton's method."""
        total = 0.0
        for d, amount in all_flows:
            years = (d - first_date).days / 365.25
            if years == 0:
                continue
            try:
                total -= years * amount / ((1 + rate) ** (years + 1))
            except (OverflowError, ZeroDivisionError):
                return float("inf")
        return total

    # Newton's method
    rate = 0.1  # Initial guess: 10%
    for _ in range(100):
        n = npv(rate)
        d = npv_derivative(rate)
        if abs(d) < 1e-12:
            break
        new_rate = rate - n / d
        # Clamp to reasonable range
        new_rate = max(-0.99, min(10.0, new_rate))
        if abs(new_rate - rate) < 1e-8:
            rate = new_rate
            break
        rate = new_rate

    return {
        "xirr_pct": round(rate * 100, 2),
        "cashflow_count": len(all_flows),
        "first_date": all_flows[0][0].isoformat(),
        "last_date": all_flows[-1][0].isoformat(),
        "total_invested": round(sum(-cf[1] for cf in all_flows if cf[1] < 0), 2),
        "current_value": round(current_value, 2),
    }


def calculate_portfolio_returns() -> dict:
    """Calculate returns for the full portfolio using available data."""
    portfolio = get_portfolio()
    holdings = portfolio.get("holdings", [])

    if not holdings:
        return {"error": "No holdings to analyze"}

    total_cost = sum(float(h.get("cost_basis", 0)) for h in holdings)
    total_value = sum(float(h.get("current_value", 0)) for h in holdings)

    simple = calculate_simple_return(total_cost, total_value)

    # Per-holding returns
    holding_returns = []
    for h in holdings:
        cost = float(h.get("cost_basis", 0))
        value = float(h.get("current_value", 0))
        if cost > 0:
            holding_returns.append({
                "symbol": h.get("symbol", "?"),
                "name": h.get("name", ""),
                "return_pct": round((value / cost - 1) * 100, 2),
                "gain_loss": round(value - cost, 2),
            })

    holding_returns.sort(key=lambda x: x["return_pct"], reverse=True)

    return {
        "portfolio": simple,
        "best_performer": holding_returns[0] if holding_returns else None,
        "worst_performer": holding_returns[-1] if holding_returns else None,
        "holding_returns": holding_returns,
    }
