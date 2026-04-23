"""
Finance Assistant Investment Tracker.

Portfolio tracking, allocation analysis, FIRE calculations, and rebalancing suggestions.
"""

from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import Optional

try:
    from finance_storage import (
        get_portfolio_path, get_investment_snapshot_path,
        load_json, save_json,
    )
    from currency import format_money
except ImportError:
    import os, sys
    sys.path.insert(0, os.path.dirname(__file__))
    from finance_storage import get_portfolio_path, get_investment_snapshot_path, load_json, save_json
    from currency import format_money


ASSET_TYPES = {
    "stock": "Individual Stock",
    "etf": "ETF",
    "bond": "Bond / Fixed Income",
    "fund": "Mutual Fund",
    "crypto": "Cryptocurrency",
    "real_estate": "Real Estate",
    "commodity": "Commodity",
    "cash": "Cash / Money Market",
    "other": "Other",
}


def _load_portfolio() -> dict:
    return load_json(get_portfolio_path(), default={"holdings": [], "target_allocation": {}})


def _save_portfolio(data: dict) -> None:
    data["last_updated"] = datetime.now().isoformat()
    save_json(get_portfolio_path(), data)


def get_portfolio() -> dict:
    return _load_portfolio()


def add_holding(holding_data: dict) -> dict:
    portfolio = _load_portfolio()
    holding = {
        "id": holding_data.get("id") or str(uuid.uuid4())[:8],
        "symbol": holding_data.get("symbol", ""),
        "name": holding_data.get("name", ""),
        "type": holding_data.get("type", "other"),
        "units": float(holding_data.get("units", 0)),
        "cost_basis": float(holding_data.get("cost_basis", 0)),
        "current_value": float(holding_data.get("current_value", 0)),
        "currency": holding_data.get("currency", "EUR"),
        "account_id": holding_data.get("account_id"),
        "last_updated": datetime.now().isoformat(),
    }
    portfolio["holdings"].append(holding)
    _save_portfolio(portfolio)
    return holding


def update_holding(holding_id: str, updates: dict) -> Optional[dict]:
    portfolio = _load_portfolio()
    for i, h in enumerate(portfolio["holdings"]):
        if h["id"] == holding_id:
            h.update(updates)
            h["last_updated"] = datetime.now().isoformat()
            portfolio["holdings"][i] = h
            _save_portfolio(portfolio)
            return h
    return None


def delete_holding(holding_id: str) -> bool:
    portfolio = _load_portfolio()
    orig_len = len(portfolio["holdings"])
    portfolio["holdings"] = [h for h in portfolio["holdings"] if h["id"] != holding_id]
    if len(portfolio["holdings"]) == orig_len:
        return False
    _save_portfolio(portfolio)
    return True


def calculate_allocation() -> dict:
    """Calculate current portfolio allocation by asset type."""
    portfolio = _load_portfolio()
    holdings = portfolio["holdings"]
    total_value = sum(float(h.get("current_value", 0)) for h in holdings)

    allocation = {}
    for h in holdings:
        asset_type = h.get("type", "other")
        value = float(h.get("current_value", 0))
        if asset_type not in allocation:
            allocation[asset_type] = {"value": 0.0, "pct": 0.0, "count": 0}
        allocation[asset_type]["value"] += value
        allocation[asset_type]["count"] += 1

    if total_value > 0:
        for asset_type in allocation:
            allocation[asset_type]["pct"] = round(allocation[asset_type]["value"] / total_value * 100, 1)
            allocation[asset_type]["value"] = round(allocation[asset_type]["value"], 2)

    return {
        "total_value": round(total_value, 2),
        "allocation": allocation,
        "target_allocation": portfolio.get("target_allocation", {}),
    }


def calculate_total_return() -> dict:
    """Calculate total return across portfolio."""
    portfolio = _load_portfolio()
    total_cost = sum(float(h.get("cost_basis", 0)) for h in portfolio["holdings"])
    total_value = sum(float(h.get("current_value", 0)) for h in portfolio["holdings"])
    gain = total_value - total_cost
    pct = (gain / total_cost * 100) if total_cost > 0 else 0

    return {
        "total_cost_basis": round(total_cost, 2),
        "total_current_value": round(total_value, 2),
        "total_gain_loss": round(gain, 2),
        "total_return_pct": round(pct, 2),
    }


def suggest_rebalance(target_allocation: Optional[dict] = None) -> list[dict]:
    """Suggest trades to rebalance toward target allocation."""
    portfolio = _load_portfolio()
    target = target_allocation or portfolio.get("target_allocation", {})
    if not target:
        return [{"suggestion": "Set a target allocation first (e.g., 70% stocks, 20% bonds, 10% cash)."}]

    alloc = calculate_allocation()
    total = alloc["total_value"]
    if total <= 0:
        return []

    suggestions = []
    for asset_type, target_pct in target.items():
        current = alloc["allocation"].get(asset_type, {"pct": 0, "value": 0})
        current_pct = current["pct"]
        diff_pct = target_pct - current_pct
        diff_value = total * diff_pct / 100

        if abs(diff_pct) >= 2:  # Only suggest if >2% off target
            action = "buy" if diff_pct > 0 else "sell"
            suggestions.append({
                "asset_type": asset_type,
                "action": action,
                "current_pct": current_pct,
                "target_pct": target_pct,
                "diff_pct": round(diff_pct, 1),
                "amount": round(abs(diff_value), 2),
            })

    return sorted(suggestions, key=lambda s: abs(s["diff_pct"]), reverse=True)


def calculate_fire_number(
    annual_expenses: float,
    withdrawal_rate: float = 0.04,
    inflation_rate: float = 0.02,
    years_to_retirement: Optional[int] = None,
) -> dict:
    """Calculate FIRE (Financial Independence) target number."""
    fire_number = annual_expenses / withdrawal_rate

    # Inflation-adjusted if years given
    if years_to_retirement:
        adjusted_expenses = annual_expenses * ((1 + inflation_rate) ** years_to_retirement)
        fire_number_inflated = adjusted_expenses / withdrawal_rate
    else:
        fire_number_inflated = fire_number

    portfolio = _load_portfolio()
    current_value = sum(float(h.get("current_value", 0)) for h in portfolio["holdings"])
    progress_pct = (current_value / fire_number * 100) if fire_number > 0 else 0

    return {
        "fire_number": round(fire_number, 2),
        "fire_number_inflation_adjusted": round(fire_number_inflated, 2),
        "annual_expenses": annual_expenses,
        "withdrawal_rate": withdrawal_rate,
        "current_portfolio_value": round(current_value, 2),
        "progress_pct": round(progress_pct, 1),
        "remaining": round(max(0, fire_number - current_value), 2),
    }


def project_portfolio_growth(
    monthly_contribution: float,
    annual_return_pct: float = 0.07,
    years: int = 10,
) -> list[dict]:
    """Project portfolio growth with compound interest."""
    portfolio = _load_portfolio()
    current = sum(float(h.get("current_value", 0)) for h in portfolio["holdings"])
    monthly_rate = annual_return_pct / 12

    projections = []
    balance = current
    total_contributed = 0.0

    for year in range(1, years + 1):
        for _ in range(12):
            balance = balance * (1 + monthly_rate) + monthly_contribution
            total_contributed += monthly_contribution
        projections.append({
            "year": year,
            "balance": round(balance, 2),
            "total_contributed": round(total_contributed, 2),
            "initial_portfolio": round(current, 2),
            "total_basis": round(current + total_contributed, 2),
            "total_growth": round(balance - current - total_contributed, 2),
        })

    return projections


def take_portfolio_snapshot() -> dict:
    """Take a point-in-time snapshot of the portfolio."""
    portfolio = _load_portfolio()
    total = sum(float(h.get("current_value", 0)) for h in portfolio["holdings"])
    alloc = calculate_allocation()
    today = date.today().isoformat()

    snapshot = {
        "date": today,
        "total_value": round(total, 2),
        "holding_count": len(portfolio["holdings"]),
        "allocation": alloc["allocation"],
    }
    save_json(get_investment_snapshot_path(today), snapshot)
    return snapshot


def format_portfolio_display() -> str:
    portfolio = _load_portfolio()
    holdings = portfolio["holdings"]
    if not holdings:
        return "No investment holdings tracked yet."

    total_return = calculate_total_return()
    alloc = calculate_allocation()

    lines = ["═══ Your Portfolio ═══\n"]
    lines.append(f"Total value: {format_money(total_return['total_current_value'], 'EUR')}")
    lines.append(f"Total return: {format_money(total_return['total_gain_loss'], 'EUR')} "
                 f"({total_return['total_return_pct']:+.1f}%)\n")

    lines.append("Holdings:")
    for h in sorted(holdings, key=lambda x: float(x.get("current_value", 0)), reverse=True):
        symbol = h.get("symbol") or h.get("name", "?")
        value = float(h.get("current_value", 0))
        cost = float(h.get("cost_basis", 0))
        gain = value - cost
        gain_pct = (gain / cost * 100) if cost > 0 else 0
        lines.append(f"  {symbol:<12} {format_money(value, 'EUR'):>12}  ({gain_pct:+.1f}%)")

    lines.append("\nAllocation:")
    for asset_type, data in sorted(alloc["allocation"].items(), key=lambda x: x[1]["pct"], reverse=True):
        label = ASSET_TYPES.get(asset_type, asset_type)
        lines.append(f"  {label:<20} {data['pct']:>5.1f}%  {format_money(data['value'], 'EUR')}")

    return "\n".join(lines)
