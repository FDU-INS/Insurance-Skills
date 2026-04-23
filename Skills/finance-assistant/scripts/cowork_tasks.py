"""
Finance Assistant — Cowork Scheduled Task Functions.

Three callable task functions intended for Cowork's task scheduler:

    daily_brief()    — Morning: session alerts + critical insights
    weekly_summary() — Monday: budget pace, top 3 insights, upcoming bills
    monthly_snapshot()— Month-end: snapshots + HTML report + summary string

Each function is completely self-contained, imports everything it needs,
never crashes the caller, and returns a clean formatted string.
"""

from __future__ import annotations

import os
import sys
import traceback
from datetime import datetime, date

# Ensure scripts dir is on the path when called from outside the package
_SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)


# ── Internal helpers ──────────────────────────────────────────────────────────

def _safe_import(module_name: str):
    """Import a module, returning None on failure instead of raising."""
    try:
        import importlib
        return importlib.import_module(module_name)
    except Exception:
        return None


def _fmt_amount(amount, currency: str = "EUR") -> str:
    try:
        from currency import format_money
        return format_money(float(amount), currency)
    except Exception:
        sym = {"EUR": "€", "USD": "$", "GBP": "£"}.get(currency, currency + " ")
        return f"{sym}{float(amount):,.2f}"


def _divider(char: str = "─", width: int = 48) -> str:
    return char * width


# ── Task 1: Daily Brief ───────────────────────────────────────────────────────

def daily_brief() -> str:
    """
    Morning brief: session alerts + any critical insights.

    Pulls session alerts from session_alerts.py and top critical insights from
    insight_engine.py. Returns a formatted string Claude can present directly.
    """
    lines: list[str] = [
        f"**Finance Daily Brief — {date.today().strftime('%A, %d %b %Y')}**",
        _divider(),
    ]

    try:
        # Session alerts
        from session_alerts import get_session_alerts, format_alerts
        from profile_manager import get_profile
        profile = get_profile() or {}
        alerts = get_session_alerts(profile)
        if alerts:
            lines.append(format_alerts(alerts))
        else:
            lines.append("No active alerts — all good.")
    except Exception:
        lines.append("(Session alerts unavailable)")

    lines.append("")

    try:
        # Critical insights only
        from insight_engine import generate_insights
        from profile_manager import get_profile
        profile = get_profile() or {}
        insights_result = generate_insights(profile, persist=False)
        all_insights = insights_result.get("insights", []) if isinstance(insights_result, dict) else []
        critical = [i for i in all_insights if i.get("status") == "ready" and i.get("confidence") in ("definitive", "high")]
        if critical:
            lines.append("**Critical insights:**")
            for ins in critical[:3]:
                impact = ins.get("impact_amount")
                impact_str = f" ({_fmt_amount(impact)})" if impact else ""
                lines.append(f"• [{ins.get('domain','?')}] {ins.get('title','?')}{impact_str}")
                if ins.get("next_action"):
                    lines.append(f"  → {ins['next_action']}")
        else:
            lines.append("No critical insights today.")
    except Exception:
        lines.append("(Insight engine unavailable)")

    lines.append("")
    lines.append(_divider("─"))
    lines.append(f"_Generated {datetime.now().strftime('%H:%M')}_")

    return "\n".join(lines)


# ── Task 2: Weekly Summary ────────────────────────────────────────────────────

def weekly_summary() -> str:
    """
    Weekly summary: budget pace, top 3 insights, upcoming bills.

    Pulls budget variance, insight engine, and recurring payments.
    Returns a formatted string suitable for a Monday morning review.
    """
    today = date.today()
    week_str = f"Week of {today.strftime('%d %b %Y')}"

    lines: list[str] = [
        f"**Finance Weekly Summary — {week_str}**",
        _divider(),
    ]

    # Budget pace
    try:
        from budget_engine import get_budget_variance
        import calendar as _cal
        year, month = today.year, today.month
        variance = get_budget_variance(year, month)
        if variance and "error" not in variance:
            days_in = today.day
            days_total = _cal.monthrange(year, month)[1]
            pct_elapsed = round(days_in / days_total * 100)
            total_a = variance.get("total_actual", 0)
            total_p = variance.get("total_planned", 0)
            pct_spent = round(total_a / total_p * 100) if total_p else 0
            pace_label = "on track" if pct_spent <= pct_elapsed + 5 else "ahead of pace — review spending"
            overspends = variance.get("overspend_categories", [])

            lines.append("**Budget Pace**")
            lines.append(
                f"Month is {pct_elapsed}% complete — spent {pct_spent}% of budget "
                f"({_fmt_amount(total_a)} / {_fmt_amount(total_p)}) → _{pace_label}_"
            )
            if overspends:
                lines.append(f"Overspend categories: {', '.join(overspends)}")
        else:
            lines.append("**Budget Pace** — no budget data for this month.")
    except Exception:
        lines.append("**Budget Pace** — (unavailable)")

    lines.append("")

    # Top 3 insights
    try:
        from insight_engine import generate_insights
        from profile_manager import get_profile
        profile = get_profile() or {}
        insights_result = generate_insights(profile, persist=False)
        all_insights = insights_result.get("insights", []) if isinstance(insights_result, dict) else []
        top = all_insights[:3]
        if top:
            lines.append("**Top Insights**")
            for i, ins in enumerate(top, 1):
                impact = ins.get("impact_amount")
                impact_str = f" — {_fmt_amount(impact)}" if impact else ""
                lines.append(f"{i}. [{ins.get('domain','?')}] {ins.get('title','?')}{impact_str}")
                if ins.get("next_action"):
                    lines.append(f"   → {ins['next_action']}")
        else:
            lines.append("**Top Insights** — none available.")
    except Exception:
        lines.append("**Top Insights** — (unavailable)")

    lines.append("")

    # Upcoming bills (next 7 days)
    try:
        from recurring_engine import get_upcoming
        upcoming = get_upcoming(days=7)
        if upcoming:
            lines.append("**Upcoming Bills (next 7 days)**")
            for item in upcoming[:5]:
                due = item.get("due_date", "?")[:10]
                name = item.get("name", "Payment")
                amount = item.get("amount", 0)
                currency = item.get("currency", "EUR")
                lines.append(f"• {due}  {name}  {_fmt_amount(amount, currency)}")
        else:
            lines.append("**Upcoming Bills** — none in the next 7 days.")
    except Exception:
        lines.append("**Upcoming Bills** — (unavailable)")

    lines.append("")
    lines.append(_divider())
    lines.append(f"_Generated {datetime.now().strftime('%Y-%m-%d %H:%M')}_")

    return "\n".join(lines)


# ── Task 3: Monthly Snapshot ──────────────────────────────────────────────────

def monthly_snapshot() -> str:
    """
    Month-end task: trigger net worth + portfolio snapshots, generate HTML
    report, and return a concise summary string.
    """
    today = date.today()
    month_str = today.strftime("%Y-%m")

    lines: list[str] = [
        f"**Finance Monthly Snapshot — {today.strftime('%B %Y')}**",
        _divider("═"),
    ]

    # Net worth snapshot
    nw_summary = "—"
    try:
        from net_worth_engine import take_snapshot, calculate_net_worth
        nw = calculate_net_worth()
        snap = take_snapshot()
        nw_val = nw.get("net_worth", 0) if isinstance(nw, dict) else 0
        nw_summary = _fmt_amount(nw_val)
        lines.append(f"Net Worth Snapshot: **{nw_summary}**")
        lines.append(f"  Snapshot saved: {snap.get('date', today.isoformat()) if isinstance(snap, dict) else today.isoformat()}")
    except Exception as exc:
        lines.append(f"Net Worth Snapshot: (error — {exc})")

    lines.append("")

    # Portfolio snapshot
    try:
        from investment_tracker import take_portfolio_snapshot, calculate_total_return
        portfolio = calculate_total_return()
        snap = take_portfolio_snapshot()
        portfolio_val = portfolio.get("total_current_value", 0) if isinstance(portfolio, dict) else 0
        ret_pct = portfolio.get("total_return_pct", 0) if isinstance(portfolio, dict) else 0
        lines.append(f"Portfolio Snapshot: **{_fmt_amount(portfolio_val)}** ({ret_pct:+.1f}% total return)")
    except Exception as exc:
        lines.append(f"Portfolio Snapshot: (error — {exc})")

    lines.append("")

    # Generate HTML + Markdown report
    report_paths: dict = {}
    try:
        from generate_report import generate_monthly_report
        report_paths = generate_monthly_report(month=month_str)
        lines.append("Reports generated:")
        lines.append(f"  Markdown : {report_paths.get('markdown_path', '—')}")
        lines.append(f"  HTML     : {report_paths.get('html_path', '—')}")
    except Exception as exc:
        lines.append(f"Report generation: (error — {exc})")

    lines.append("")
    lines.append(_divider("═"))
    lines.append(f"_Month-end snapshot completed {datetime.now().strftime('%Y-%m-%d %H:%M')}_")

    return "\n".join(lines)


# ── CLI entry point (manual test) ─────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Finance Assistant Cowork Tasks")
    parser.add_argument(
        "task",
        choices=["daily", "weekly", "monthly"],
        help="Which task to run",
    )
    args = parser.parse_args()

    if args.task == "daily":
        print(daily_brief())
    elif args.task == "weekly":
        print(weekly_summary())
    elif args.task == "monthly":
        print(monthly_snapshot())
