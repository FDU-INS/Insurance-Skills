"""
Finance Assistant Net Worth Engine.

Calculate, snapshot, and track net worth over time.
"""

from __future__ import annotations

import os
from datetime import date, datetime
from typing import Optional

try:
    from finance_storage import (
        get_net_worth_snapshot_path, ensure_subdir,
        load_json, save_json,
    )
    from account_manager import get_accounts, get_total_balance
    from investment_tracker import get_portfolio
    from debt_optimizer import get_debts
    from currency import format_money
except ImportError:
    import sys
    sys.path.insert(0, os.path.dirname(__file__))
    from finance_storage import get_net_worth_snapshot_path, ensure_subdir, load_json, save_json
    from account_manager import get_accounts, get_total_balance
    from investment_tracker import get_portfolio
    from debt_optimizer import get_debts
    from currency import format_money


def calculate_net_worth() -> dict:
    """Calculate current net worth from all sources."""
    # Bank accounts
    accounts = get_accounts()
    cash_assets = sum(float(a.get("current_balance", 0)) for a in accounts
                      if a.get("is_asset", True) and a.get("include_in_net_worth", True))
    cash_liabilities = sum(abs(float(a.get("current_balance", 0))) for a in accounts
                           if not a.get("is_asset", True) and a.get("include_in_net_worth", True))

    # Investments
    portfolio = get_portfolio()
    investment_value = sum(float(h.get("current_value", 0)) for h in portfolio.get("holdings", []))

    # Debts
    debts = get_debts()
    debt_total = sum(float(d.get("balance", 0)) for d in debts)

    total_assets = cash_assets + investment_value
    total_liabilities = cash_liabilities + debt_total
    net_worth = total_assets - total_liabilities

    return {
        "date": date.today().isoformat(),
        "net_worth": round(net_worth, 2),
        "total_assets": round(total_assets, 2),
        "total_liabilities": round(total_liabilities, 2),
        "breakdown": {
            "cash_and_savings": round(cash_assets, 2),
            "investments": round(investment_value, 2),
            "credit_card_balance": round(cash_liabilities, 2),
            "loans_and_debt": round(debt_total, 2),
        },
        "account_count": len(accounts),
        "holding_count": len(portfolio.get("holdings", [])),
        "debt_count": len(debts),
    }


def take_snapshot() -> dict:
    """Take a point-in-time net worth snapshot and persist it."""
    nw = calculate_net_worth()
    today = date.today().isoformat()
    save_json(get_net_worth_snapshot_path(today), nw)
    return nw


def get_snapshots(start_date: Optional[str] = None, end_date: Optional[str] = None) -> list[dict]:
    """Retrieve net worth snapshots within a date range."""
    snapshot_dir = ensure_subdir("net_worth", "snapshots")
    snapshots = []

    for f in sorted(snapshot_dir.iterdir()):
        if not f.name.endswith(".json"):
            continue
        date_str = f.stem
        if start_date and date_str < start_date:
            continue
        if end_date and date_str > end_date:
            continue
        data = load_json(f)
        if data:
            snapshots.append(data)

    return snapshots


def calculate_net_worth_trend(months: int = 12) -> dict:
    """Calculate net worth trend from historical snapshots."""
    snapshots = get_snapshots()
    if not snapshots:
        current = calculate_net_worth()
        return {
            "current": current,
            "trend": "no_history",
            "snapshots": [],
            "suggestion": "Take regular snapshots to track your net worth over time.",
        }

    current = snapshots[-1] if snapshots else calculate_net_worth()

    # Calculate change
    if len(snapshots) >= 2:
        oldest = snapshots[0]
        change = current["net_worth"] - oldest["net_worth"]
        pct_change = (change / abs(oldest["net_worth"]) * 100) if oldest["net_worth"] != 0 else 0
        trend = "growing" if change > 0 else "declining" if change < 0 else "flat"
    else:
        change = 0
        pct_change = 0
        trend = "insufficient_data"

    return {
        "current": current,
        "trend": trend,
        "change": round(change, 2),
        "change_pct": round(pct_change, 1),
        "snapshot_count": len(snapshots),
        "first_snapshot_date": snapshots[0].get("date") if snapshots else None,
        "latest_snapshot_date": snapshots[-1].get("date") if snapshots else None,
    }


def format_net_worth_display() -> str:
    nw = calculate_net_worth()
    bd = nw["breakdown"]

    lines = [
        "═══ Your Net Worth ═══\n",
        f"  Net Worth: {format_money(nw['net_worth'], 'EUR')}\n",
        "  Assets:",
        f"    Cash & Savings:  {format_money(bd['cash_and_savings'], 'EUR')}",
        f"    Investments:     {format_money(bd['investments'], 'EUR')}",
        f"    Total Assets:    {format_money(nw['total_assets'], 'EUR')}\n",
        "  Liabilities:",
        f"    Credit Cards:    {format_money(bd['credit_card_balance'], 'EUR')}",
        f"    Loans & Debt:    {format_money(bd['loans_and_debt'], 'EUR')}",
        f"    Total Liab.:     {format_money(nw['total_liabilities'], 'EUR')}\n",
        f"  ══════════════════════",
        f"  NET WORTH:         {format_money(nw['net_worth'], 'EUR')}",
    ]

    # Add trend if available
    trend = calculate_net_worth_trend()
    if trend["trend"] not in ("no_history", "insufficient_data"):
        sign = "+" if trend["change"] >= 0 else ""
        lines.append(f"\n  Trend: {sign}{format_money(trend['change'], 'EUR')} ({sign}{trend['change_pct']}%)")
        lines.append(f"  Since: {trend['first_snapshot_date']}")

    return "\n".join(lines)
