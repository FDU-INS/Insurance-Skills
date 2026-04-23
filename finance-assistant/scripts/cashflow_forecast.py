"""
Finance Assistant Predictive Cash Flow Forecaster.

Projects account balance day-by-day for the next N days, applying recurring
transactions and average daily spend to identify low-balance risk periods.
"""

from __future__ import annotations

import os
from collections import defaultdict
from datetime import date, datetime, timedelta
from typing import Optional

try:
    from account_manager import get_account
    from recurring_engine import get_upcoming
    from transaction_logger import get_transactions
    from currency import format_money
except ImportError:
    import sys
    sys.path.insert(0, os.path.dirname(__file__))
    from account_manager import get_account
    from recurring_engine import get_upcoming
    from transaction_logger import get_transactions
    from currency import format_money


_SPARKLINE_CHARS = "▁▂▃▄▅▆▇█"
_DEFAULT_LOW_THRESHOLD = 200.0  # EUR / GBP


# ── Internal helpers ──────────────────────────────────────────────────────────

def _avg_daily_spend(account_id: str, months: int = 3) -> float:
    """
    Compute average daily net spend from the last `months` months of transactions.
    Returns a negative float representing average daily outflow.
    """
    today = date.today()
    total_expense = 0.0
    total_days = 0

    for m in range(months):
        # Go back m full months
        target_month = today.month - m
        target_year = today.year
        while target_month <= 0:
            target_month += 12
            target_year -= 1

        txns = get_transactions(account_id=account_id, year=target_year, month=target_month)
        for t in txns:
            amt = float(t.get("amount", 0))
            ttype = t.get("type", "")
            if ttype == "expense" or amt < 0:
                total_expense += abs(amt)
        # Days in that month (approximate)
        total_days += 30

    if total_days == 0:
        return 0.0

    daily = total_expense / total_days
    return -round(daily, 4)  # negative = outflow


def _build_recurring_map(account_id: str, days: int) -> dict[str, list[dict]]:
    """
    Build a dict mapping date strings to lists of recurring events for that day.
    Only includes events for the given account_id.
    """
    upcoming = get_upcoming(days=days)
    event_map: dict[str, list[dict]] = defaultdict(list)
    for event in upcoming:
        # Filter to matching account if possible
        evt_account = event.get("account_id", account_id)
        if evt_account and evt_account != account_id:
            continue
        due_date = event.get("due_date", "")
        if due_date:
            event_map[due_date].append(event)
    return event_map


# ── Public API ────────────────────────────────────────────────────────────────

def forecast(
    account_id: str,
    days: int = 90,
    profile: Optional[dict] = None,
) -> dict:
    """
    Project account balance day-by-day for the next `days` days.

    Returns:
    {
      "account_id": str,
      "current_balance": float,
      "forecast": [{"date": "YYYY-MM-DD", "balance": float, "events": [...]}],
      "low_balance_warnings": [{"date": str, "projected_balance": float, "threshold": float}],
      "summary": {"min_balance": float, "min_balance_date": str, "end_balance": float}
    }
    """
    account = get_account(account_id)
    if account is None:
        return {
            "error": f"Account '{account_id}' not found.",
            "account_id": account_id,
            "current_balance": 0.0,
            "forecast": [],
            "low_balance_warnings": [],
            "summary": {"min_balance": 0.0, "min_balance_date": "", "end_balance": 0.0},
        }

    current_balance = float(account.get("current_balance", 0.0))
    currency = account.get("currency", "EUR")

    # Low balance threshold — use profile preference if available
    low_threshold = _DEFAULT_LOW_THRESHOLD
    if profile:
        low_threshold = float(
            profile.get("preferences", {}).get("low_balance_threshold", _DEFAULT_LOW_THRESHOLD)
        )

    daily_spend = _avg_daily_spend(account_id)
    recurring_map = _build_recurring_map(account_id, days)

    today = date.today()
    balance = current_balance
    forecast_days = []
    low_balance_warnings = []

    min_balance = current_balance
    min_balance_date = today.isoformat()

    for i in range(1, days + 1):
        day = today + timedelta(days=i)
        day_str = day.isoformat()
        events = recurring_map.get(day_str, [])

        # Apply recurring events
        day_delta = 0.0
        for event in events:
            day_delta += float(event.get("amount", 0))

        # Apply average daily spend
        day_delta += daily_spend

        balance = round(balance + day_delta, 2)

        forecast_days.append({
            "date": day_str,
            "balance": balance,
            "events": [
                {
                    "name": e.get("name", ""),
                    "amount": float(e.get("amount", 0)),
                    "category": e.get("category", ""),
                }
                for e in events
            ],
        })

        if balance < min_balance:
            min_balance = balance
            min_balance_date = day_str

        if balance < low_threshold:
            # Group consecutive warnings — only add if last warning was more than 3 days ago
            if not low_balance_warnings or (
                date.fromisoformat(low_balance_warnings[-1]["date"]) < day - timedelta(days=3)
            ):
                low_balance_warnings.append({
                    "date": day_str,
                    "projected_balance": balance,
                    "threshold": low_threshold,
                    "currency": currency,
                })

    end_balance = round(balance, 2)

    return {
        "account_id": account_id,
        "current_balance": current_balance,
        "currency": currency,
        "forecast": forecast_days,
        "low_balance_warnings": low_balance_warnings,
        "summary": {
            "min_balance": round(min_balance, 2),
            "min_balance_date": min_balance_date,
            "end_balance": end_balance,
        },
    }


def format_forecast(forecast_result: dict, sparkline: bool = True) -> str:
    """
    Render forecast as text. Includes ASCII sparkline of balance over time if requested.

    Sparkline chars: ▁▂▃▄▅▆▇█ (8 levels, min..max balance mapped to chars)

    Example output:
      Balance forecast (90 days): ▃▃▄▄▄▃▃▂▂▁▂▂▃▃▃▄▄▄▅▅▅▄▄▃
      Min: €180 on 22 Apr  |  End: €1,240
      [!] Low balance warning: ~€180 around 22 Apr (rent due 1 May)
    """
    if "error" in forecast_result:
        return f"Forecast error: {forecast_result['error']}"

    forecast_days = forecast_result.get("forecast", [])
    summary = forecast_result.get("summary", {})
    warnings = forecast_result.get("low_balance_warnings", [])
    currency = forecast_result.get("currency", "EUR")
    days = len(forecast_days)

    lines = []

    if sparkline and forecast_days:
        balances = [d["balance"] for d in forecast_days]
        min_b = min(balances)
        max_b = max(balances)
        span = max_b - min_b if max_b != min_b else 1.0

        # Sample up to 60 chars for the sparkline
        step = max(1, len(balances) // 60)
        sampled = balances[::step]

        spark = "".join(
            _SPARKLINE_CHARS[min(7, int((b - min_b) / span * 7))]
            for b in sampled
        )
        lines.append(f"Balance forecast ({days} days): {spark}")
    else:
        lines.append(f"Balance forecast ({days} days)")

    min_balance = summary.get("min_balance", 0.0)
    min_date = summary.get("min_balance_date", "")
    end_balance = summary.get("end_balance", 0.0)

    # Format dates nicely
    def fmt_date(d: str) -> str:
        try:
            return datetime.strptime(d, "%Y-%m-%d").strftime("%-d %b")
        except Exception:
            return d

    cur_sym = "€" if currency == "EUR" else ("£" if currency == "GBP" else currency + " ")
    lines.append(
        f"Min: {cur_sym}{min_balance:,.0f} on {fmt_date(min_date)}"
        f"  |  End: {cur_sym}{end_balance:,.0f}"
    )

    for w in warnings:
        bal = w.get("projected_balance", 0.0)
        w_date = fmt_date(w.get("date", ""))
        # Find upcoming recurring events near that date to mention
        near_events = []
        try:
            w_dt = datetime.strptime(w["date"], "%Y-%m-%d").date()
            for day in forecast_days:
                try:
                    d_dt = datetime.strptime(day["date"], "%Y-%m-%d").date()
                except ValueError:
                    continue
                if 0 <= (d_dt - w_dt).days <= 14:
                    for evt in day.get("events", []):
                        if float(evt.get("amount", 0)) < 0:
                            near_events.append(evt["name"])
        except Exception:
            pass

        context = f" ({near_events[0]} due soon)" if near_events else ""
        lines.append(
            f"[!] Low balance warning: ~{cur_sym}{bal:,.0f} around {w_date}{context}"
        )

    if not warnings:
        lines.append("No low balance warnings in the forecast period.")

    return "\n".join(lines)
