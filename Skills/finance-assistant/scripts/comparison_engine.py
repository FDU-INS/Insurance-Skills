"""
Finance Assistant — Month-over-Month Comparison Engine (v2.4).

Compares spending across consecutive months, surfaces biggest changes,
and formats results with optional ASCII visualization.
"""

from __future__ import annotations

from datetime import datetime, date
from typing import Optional

try:
    from transaction_logger import get_transactions
    from viz import spending_category_delta
except ImportError:
    import os, sys
    sys.path.insert(0, os.path.dirname(__file__))
    from transaction_logger import get_transactions
    from viz import spending_category_delta


# ── Helpers ───────────────────────────────────────────────────────────────────

def _parse_month(month: Optional[str]) -> tuple[int, int]:
    """Return (year, month_int) from 'YYYY-MM' or default to current month."""
    if month:
        try:
            dt = datetime.strptime(month, "%Y-%m")
            return dt.year, dt.month
        except ValueError:
            pass
    today = date.today()
    return today.year, today.month


def _prev_month(year: int, month: int) -> tuple[int, int]:
    if month == 1:
        return year - 1, 12
    return year, month - 1


def _month_label(year: int, month: int) -> str:
    return f"{year}-{month:02d}"


def _get_category_totals(account_id: Optional[str], year: int, month: int) -> dict[str, float]:
    """Sum expense transactions per category for the given month."""
    try:
        txns = get_transactions(
            account_id=account_id or "default",
            year=year,
            month=month,
        )
    except Exception:
        txns = []

    totals: dict[str, float] = {}
    for txn in txns:
        if txn.get("type") not in ("expense", "debt_payment"):
            continue
        cat = txn.get("category", "other_expense")
        totals[cat] = totals.get(cat, 0.0) + abs(txn.get("amount", 0.0))

    return totals


# ── Public API ────────────────────────────────────────────────────────────────

def get_monthly_comparison(account_id: str = None, month: str = None) -> dict:
    """
    Compare current month's spending to previous month.

    month = "YYYY-MM" (defaults to current month)

    Returns a dict with category-level deltas, totals, highlights, and
    new / dropped categories.
    """
    cur_year, cur_mon = _parse_month(month)
    prev_year, prev_mon = _prev_month(cur_year, cur_mon)

    cur_label = _month_label(cur_year, cur_mon)
    prev_label = _month_label(prev_year, prev_mon)

    cur_totals = _get_category_totals(account_id, cur_year, cur_mon)
    prev_totals = _get_category_totals(account_id, prev_year, prev_mon)

    all_cats = set(cur_totals) | set(prev_totals)
    categories: dict[str, dict] = {}
    for cat in sorted(all_cats):
        cur_val = cur_totals.get(cat, 0.0)
        prev_val = prev_totals.get(cat, 0.0)
        delta = round(cur_val - prev_val, 2)
        delta_pct = round(delta / prev_val * 100, 1) if prev_val else (100.0 if cur_val else 0.0)
        categories[cat] = {
            "current": round(cur_val, 2),
            "previous": round(prev_val, 2),
            "delta": delta,
            "delta_pct": delta_pct,
        }

    # Totals
    cur_total = round(sum(cur_totals.values()), 2)
    prev_total = round(sum(prev_totals.values()), 2)
    total_delta = round(cur_total - prev_total, 2)
    total_delta_pct = round(total_delta / prev_total * 100, 1) if prev_total else 0.0

    # Biggest increase / decrease (only categories present in both months or newly appearing)
    biggest_increase = {"category": None, "delta": 0.0, "delta_pct": 0.0}
    biggest_decrease = {"category": None, "delta": 0.0, "delta_pct": 0.0}
    for cat, vals in categories.items():
        if vals["delta"] > biggest_increase["delta"]:
            biggest_increase = {"category": cat, "delta": vals["delta"], "delta_pct": vals["delta_pct"]}
        if vals["delta"] < biggest_decrease["delta"]:
            biggest_decrease = {"category": cat, "delta": vals["delta"], "delta_pct": vals["delta_pct"]}

    new_categories = sorted(c for c in cur_totals if c not in prev_totals)
    dropped_categories = sorted(c for c in prev_totals if c not in cur_totals)

    return {
        "current_month": cur_label,
        "previous_month": prev_label,
        "categories": categories,
        "totals": {
            "current": cur_total,
            "previous": prev_total,
            "delta": total_delta,
            "delta_pct": total_delta_pct,
        },
        "biggest_increase": biggest_increase,
        "biggest_decrease": biggest_decrease,
        "new_categories": new_categories,
        "dropped_categories": dropped_categories,
    }


def format_comparison(comparison: dict, include_viz: bool = True) -> str:
    """
    Format the comparison as a clean text response.

    Leads with the headline delta, optionally embeds the spending_category_delta
    chart, then lists top 3 changes.
    """
    totals = comparison.get("totals", {})
    cur_label = comparison.get("current_month", "this month")
    prev_label = comparison.get("previous_month", "last month")
    delta = totals.get("delta", 0.0)
    delta_pct = totals.get("delta_pct", 0.0)
    sign = "+" if delta >= 0 else ""
    direction_word = "up" if delta >= 0 else "down"

    # Headline
    lines = [
        f"**{cur_label} vs {prev_label}**",
        f"Total spending {direction_word} {sign}€{delta:.0f} ({sign}{delta_pct:.1f}%)  "
        f"— €{totals.get('current', 0):.0f} this month vs €{totals.get('previous', 0):.0f} last month.",
        "",
    ]

    # Optional viz
    if include_viz:
        categories = comparison.get("categories", {})
        current_map = {k: v["current"] for k, v in categories.items()}
        previous_map = {k: v["previous"] for k, v in categories.items()}
        chart = spending_category_delta(current_map, previous_map)
        lines.append(chart)
        lines.append("")

    # Top 3 changes by absolute delta
    categories = comparison.get("categories", {})
    sorted_cats = sorted(categories.items(), key=lambda x: abs(x[1]["delta"]), reverse=True)[:3]
    if sorted_cats:
        lines.append("**Top changes:**")
        for cat, vals in sorted_cats:
            sign2 = "+" if vals["delta"] >= 0 else ""
            arrow = "▲" if vals["delta"] > 0 else "▼"
            warn = "  ⚠" if vals["delta"] > 0 and vals["delta_pct"] > 20 else ""
            lines.append(
                f"  {arrow} {cat}: {sign2}€{vals['delta']:.0f} ({sign2}{vals['delta_pct']:.1f}%){warn}"
            )
        lines.append("")

    # New / dropped
    new_cats = comparison.get("new_categories", [])
    dropped_cats = comparison.get("dropped_categories", [])
    if new_cats:
        lines.append(f"**New this month:** {', '.join(new_cats)}")
    if dropped_cats:
        lines.append(f"**Not seen this month:** {', '.join(dropped_cats)}")

    return "\n".join(lines).strip()


def compare_budgets(month: str = None) -> dict:
    """
    Compare budget limits vs actuals for current and previous month.

    Returns per-category: limit, current_actual, previous_actual, delta.
    """
    cur_year, cur_mon = _parse_month(month)
    prev_year, prev_mon = _prev_month(cur_year, cur_mon)

    # Try to load budget limits
    try:
        from budget_engine import get_budget
        budget_data = get_budget() or {}
        limits: dict[str, float] = {}
        for cat, entry in budget_data.get("categories", {}).items():
            limits[cat] = entry.get("limit", 0.0)
    except Exception:
        limits = {}

    cur_totals = _get_category_totals(None, cur_year, cur_mon)
    prev_totals = _get_category_totals(None, prev_year, prev_mon)

    all_cats = set(limits) | set(cur_totals) | set(prev_totals)
    result: dict[str, dict] = {}
    for cat in sorted(all_cats):
        cur_val = cur_totals.get(cat, 0.0)
        prev_val = prev_totals.get(cat, 0.0)
        result[cat] = {
            "limit": limits.get(cat, None),
            "current_actual": round(cur_val, 2),
            "previous_actual": round(prev_val, 2),
            "delta": round(cur_val - prev_val, 2),
        }

    return {
        "current_month": _month_label(cur_year, cur_mon),
        "previous_month": _month_label(prev_year, prev_mon),
        "categories": result,
    }
