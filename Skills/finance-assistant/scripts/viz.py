"""
Finance Assistant — ASCII Visualization Module (v2.4).

All functions return a string ready to embed in Claude's response.
No dependencies beyond stdlib.
"""

from __future__ import annotations

import math
from datetime import datetime, date
from typing import Optional


# ── Shared helpers ────────────────────────────────────────────────────────────

def _fmt_money(amount: float, decimals: int = 0) -> str:
    """Format a float as €-prefixed string."""
    if abs(amount) >= 1_000_000:
        return f"€{amount / 1_000_000:.1f}M"
    if abs(amount) >= 1_000:
        return f"€{amount / 1_000:.0f}k" if decimals == 0 else f"€{amount / 1_000:.1f}k"
    if decimals:
        return f"€{amount:.{decimals}f}"
    return f"€{amount:.0f}"


def _bar(filled: int, total: int, over: bool = False) -> str:
    """Return a bar string of `total` chars: █ for filled, ░ for remaining, ▓ for over."""
    if over:
        return "▓" * total
    filled = max(0, min(filled, total))
    return "█" * filled + "░" * (total - filled)


# ── budget_bars ───────────────────────────────────────────────────────────────

def budget_bars(categories: dict, width: int = 40) -> str:
    """
    Horizontal bar chart for budget categories.

    categories = {"Food": {"limit": 400, "actual": 340}, ...}

    Sorted by % used descending. Over-budget items use ▓ fill.
    """
    if not categories:
        return "(no budget data)"

    # Build sorted list (descending by pct used)
    items = []
    for name, vals in categories.items():
        limit = vals.get("limit", 0) or 0
        actual = vals.get("actual", 0) or 0
        pct = (actual / limit * 100) if limit else float("inf")
        items.append((name, limit, actual, pct))
    items.sort(key=lambda x: x[3], reverse=True)

    label_w = max(len(x[0]) for x in items) + 1
    bar_w = width

    lines = []
    for name, limit, actual, pct in items:
        over = actual > limit
        if over:
            bar = "▓" * bar_w
            status = f"  ⚠ OVER"
        else:
            filled = round(bar_w * actual / limit) if limit else 0
            bar = "█" * filled + "░" * (bar_w - filled)
            status = f"  ({pct:.0f}%)"

        money = f"  {_fmt_money(actual)} / {_fmt_money(limit)}"
        lines.append(f"  {name:<{label_w}} {bar}{money}{status}")

    return "\n".join(lines)


# ── portfolio_allocation ──────────────────────────────────────────────────────

_CLASS_CHARS = ["█", "▓", "░", "▒", "■", "□"]


def portfolio_allocation(holdings: list, width: int = 40) -> str:
    """
    Stacked horizontal bar + legend showing portfolio allocation by asset class.

    holdings = [{"name": str, "value": float, "asset_class": str}, ...]
    """
    if not holdings:
        return "(no holdings)"

    total = sum(h.get("value", 0) for h in holdings)
    if total <= 0:
        return "(zero portfolio value)"

    # Group by asset class
    classes: dict[str, float] = {}
    for h in holdings:
        cls = h.get("asset_class", "Other")
        classes[cls] = classes.get(cls, 0.0) + h.get("value", 0.0)

    sorted_classes = sorted(classes.items(), key=lambda x: x[1], reverse=True)

    # Build stacked bar
    bar_chars: list[str] = []
    char_map: dict[str, str] = {}
    for i, (cls, val) in enumerate(sorted_classes):
        ch = _CLASS_CHARS[i % len(_CLASS_CHARS)]
        char_map[cls] = ch
        count = round(width * val / total)
        bar_chars.extend([ch] * count)

    # Trim / pad to exact width
    bar_chars = bar_chars[:width]
    while len(bar_chars) < width:
        bar_chars.append(_CLASS_CHARS[0])

    bar_line = "  " + "".join(bar_chars)

    # Legend
    legend_parts = []
    for cls, val in sorted_classes:
        pct = val / total * 100
        legend_parts.append(f"{char_map[cls]} {cls} {pct:.0f}%")
    legend_line = "  " + "  │  ".join(legend_parts)

    # Top 3 holdings
    top3 = sorted(holdings, key=lambda h: h.get("value", 0), reverse=True)[:3]
    top3_lines = ["", "  Top holdings:"]
    for h in top3:
        pct = h.get("value", 0) / total * 100
        top3_lines.append(f"    {h.get('name','?'):<20} {_fmt_money(h.get('value', 0)):>10}  ({pct:.1f}%)")

    return "\n".join([bar_line, legend_line] + top3_lines)


# ── net_worth_timeline ────────────────────────────────────────────────────────

_SPARK_CHARS = "▁▂▃▄▅▆▇█"


def net_worth_timeline(snapshots: list, width: int = 50) -> str:
    """
    Sparkline of net worth over monthly snapshots (last 12 months max).

    snapshots = [{"date": "YYYY-MM-DD", "net_worth": float}, ...]
    """
    if not snapshots:
        return "(no net worth snapshots)"

    # Sort and take last 12
    def _parse_date(s: dict) -> date:
        raw = s.get("date", "1970-01-01")
        try:
            return datetime.fromisoformat(raw).date()
        except ValueError:
            return date(1970, 1, 1)

    sorted_snaps = sorted(snapshots, key=_parse_date)[-12:]
    values = [s.get("net_worth", 0.0) for s in sorted_snaps]
    n = len(values)

    if n < 2:
        single = values[0] if values else 0
        return f"  Net worth (1 month): {_SPARK_CHARS[-1]}\n  {_fmt_money(single)}"

    lo, hi = min(values), max(values)
    rng = hi - lo

    def _spark_char(v: float) -> str:
        if rng == 0:
            return _SPARK_CHARS[4]
        idx = round((v - lo) / rng * (len(_SPARK_CHARS) - 1))
        return _SPARK_CHARS[max(0, min(idx, len(_SPARK_CHARS) - 1))]

    spark = "".join(_spark_char(v) for v in values)
    first, last = values[0], values[-1]
    delta = last - first
    delta_pct = (delta / abs(first) * 100) if first else 0.0
    sign = "+" if delta >= 0 else ""

    line1 = f"  Net worth ({n} months): {spark}"
    line2 = f"  {_fmt_money(first)} → {_fmt_money(last)}  ({sign}{_fmt_money(delta)}, {sign}{delta_pct:.1f}%)"
    return "\n".join([line1, line2])


# ── debt_payoff_curves ────────────────────────────────────────────────────────

def debt_payoff_curves(avalanche: list, snowball: list, width: int = 50) -> str:
    """
    Two-line ASCII chart showing remaining debt over months.

    avalanche/snowball = [{"month": int, "remaining": float}, ...]
    """
    if not avalanche and not snowball:
        return "(no debt payoff data)"

    all_points = avalanche + snowball
    max_remaining = max(p.get("remaining", 0) for p in all_points) if all_points else 1
    max_month = max(p.get("month", 0) for p in all_points) if all_points else 1

    height = 6
    chart_w = width

    def _to_col(month: int) -> int:
        return round(month / max_month * (chart_w - 1)) if max_month else 0

    def _to_row(remaining: float) -> int:
        if max_remaining <= 0:
            return height - 1
        return round((1 - remaining / max_remaining) * (height - 1))

    # Build grid
    grid = [[" "] * chart_w for _ in range(height)]

    def _plot(series: list, ch: str) -> None:
        pts = {p["month"]: p["remaining"] for p in series}
        months = sorted(pts)
        for i, m in enumerate(months):
            col = _to_col(m)
            row = _to_row(pts[m])
            row = max(0, min(row, height - 1))
            col = max(0, min(col, chart_w - 1))
            grid[row][col] = ch

    _plot(avalanche, "─")
    _plot(snowball, "╌")

    # Y-axis labels
    label_hi = _fmt_money(max_remaining)
    label_lo = "€0k" if max_remaining >= 1000 else "€0"

    lines = []
    for r, row in enumerate(grid):
        if r == 0:
            prefix = f"{label_hi:>6} ┤"
        elif r == height - 1:
            prefix = f"{label_lo:>6} ┤"
        else:
            prefix = "       │"
        lines.append(prefix + "".join(row))

    # X-axis
    lines.append("       ┴" + "─" * chart_w)

    # Tick labels
    mid_month = max_month // 2
    x_labels = (
        f"       {'0m':<{_to_col(0) + 1}}"
        f"{'%dm' % mid_month:<{_to_col(mid_month) - _to_col(0)}}"
        f"{'%dm' % max_month}"
    )
    lines.append(x_labels)

    # Legend
    lines.append("")
    lines.append("  Avalanche ──   Snowball ╌╌")

    return "\n".join(lines)


# ── fire_milestone_chart ──────────────────────────────────────────────────────

def fire_milestone_chart(
    current: float,
    target: float,
    monthly_contribution: float,
    annual_return: float = 0.07,
    width: int = 50,
) -> str:
    """
    FIRE progress bar + milestone markers at 25%, 50%, 75%, 100%.
    """
    if target <= 0:
        return "(invalid FIRE target)"

    pct = min(current / target * 100, 100.0)

    # Progress bar
    filled = round(width * pct / 100)
    bar = "█" * filled + "░" * (width - filled)
    bar_line = f"  FIRE Progress  [{bar}]  {pct:.0f}%"

    # Milestone markers
    milestones = [25, 50, 75, 100]
    marker_line_parts = ["  ├"]
    for i, m in enumerate(milestones):
        reached = pct >= m
        check = " ✓" if reached else " "
        label = f"─{m}%{check}"
        if i < len(milestones) - 1:
            segment_w = width // len(milestones)
            marker_line_parts.append(f"{label}{'─' * max(0, segment_w - len(label))}")
        else:
            marker_line_parts.append(f"{label}┤")
    milestone_line = "".join(marker_line_parts)

    # Years remaining estimate (FV formula: FV = PV*(1+r)^n + PMT*((1+r)^n-1)/r)
    monthly_r = annual_return / 12
    needed = target - current
    years_remaining = None
    if monthly_contribution > 0 and monthly_r > 0:
        # Solve for n: target = current*(1+r)^n + PMT*((1+r)^n-1)/r
        # Binary search on n
        lo_n, hi_n = 0, 600
        for _ in range(60):
            mid = (lo_n + hi_n) / 2
            fv = current * (1 + monthly_r) ** mid + monthly_contribution * ((1 + monthly_r) ** mid - 1) / monthly_r
            if fv >= target:
                hi_n = mid
            else:
                lo_n = mid
        years_remaining = round(hi_n / 12, 1)
    elif monthly_contribution > 0:
        years_remaining = round(needed / (monthly_contribution * 12), 1)

    years_str = f"~{years_remaining} years remaining" if years_remaining is not None else "n/a"
    summary_line = f"  {_fmt_money(current)} of {_fmt_money(target)}  │  {years_str} at {_fmt_money(monthly_contribution)}/month"

    return "\n".join([bar_line, milestone_line, summary_line])


# ── spending_category_delta ───────────────────────────────────────────────────

def spending_category_delta(current: dict, previous: dict, width: int = 35) -> str:
    """
    Side-by-side comparison of current vs previous month spending per category.
    Sorted by absolute delta descending. Flags increases > 20% with ⚠.

    current/previous = {"Food": 340.0, "Transport": 112.0, ...}
    """
    all_cats = sorted(set(list(current.keys()) + list(previous.keys())))
    if not all_cats:
        return "(no spending data)"

    items = []
    for cat in all_cats:
        cur = current.get(cat, 0.0)
        prev = previous.get(cat, 0.0)
        delta = cur - prev
        delta_pct = (delta / prev * 100) if prev else (100.0 if cur else 0.0)
        items.append((cat, cur, prev, delta, delta_pct))

    items.sort(key=lambda x: abs(x[3]), reverse=True)

    cat_w = max(len(x[0]) for x in items) + 1
    header = f"  {'Category':<{cat_w}}  {'This month':>10}  {'vs Last':>10}    Δ"
    lines = [header, "  " + "─" * (cat_w + 40)]

    for cat, cur, prev, delta, delta_pct in items:
        direction = "▲" if delta > 0 else ("▼" if delta < 0 else " ")
        warn = "  ⚠" if delta > 0 and delta_pct > 20 else ""
        sign = "+" if delta >= 0 else ""
        delta_str = f"{sign}{_fmt_money(delta)}"
        lines.append(
            f"  {cat:<{cat_w}}  {_fmt_money(cur):>10}  {_fmt_money(prev):>10}  "
            f"{delta_str:>7}  {direction}{warn}"
        )

    return "\n".join(lines)
