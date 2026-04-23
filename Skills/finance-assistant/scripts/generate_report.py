"""
Finance Assistant Report Generator.

Thin orchestrator that:
  1. Loads the user profile
  2. Builds the output suite across all financial domains
  3. Renders both Markdown and HTML reports
  4. Saves them to .finance/reports/YYYY-MM.{md,html}
  5. Returns a dict with both paths and the generation timestamp

Usage:
    from generate_report import generate_monthly_report
    result = generate_monthly_report()
    print(result["markdown_path"])
    print(result["html_path"])
"""

from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path

try:
    from finance_storage import ensure_subdir
    from profile_manager import get_profile
    from output_builder import build_output_suite
    from report_renderer import render_html, render_markdown
except ImportError:
    import sys
    sys.path.insert(0, os.path.dirname(__file__))
    from finance_storage import ensure_subdir
    from profile_manager import get_profile
    from output_builder import build_output_suite
    from report_renderer import render_html, render_markdown


def generate_monthly_report(
    month: str | None = None,
    persist_suite: bool = True,
) -> dict:
    """
    Build and save the monthly finance report in both Markdown and HTML.

    Args:
        month        : Optional "YYYY-MM" string. Defaults to the current month.
        persist_suite: Whether to persist the output suite JSON to disk.

    Returns a dict with keys:
        markdown_path : Absolute path to the saved .md file
        html_path     : Absolute path to the saved .html file
        generated_at  : ISO 8601 timestamp string
    """
    if month is None:
        month = datetime.now().strftime("%Y-%m")

    # 1. Load profile
    profile = get_profile() or {}

    # 2. Build output suite
    suite = build_output_suite(profile=profile, persist=persist_suite)

    # Stamp the month label so reports directory names are consistent
    suite.setdefault("month", month)

    generated_at = suite.get("generated_at", datetime.now().isoformat(timespec="seconds"))

    # 3. Render content
    md_content = render_markdown(suite)
    html_content = _render_html_full(suite)

    # 4. Save to .finance/reports/
    reports_dir: Path = ensure_subdir("reports")

    md_path = reports_dir / f"{month}.md"
    html_path = reports_dir / f"{month}.html"

    md_path.write_text(md_content, encoding="utf-8")
    html_content_str = html_content if isinstance(html_content, str) else render_html(suite)
    html_path.write_text(html_content_str, encoding="utf-8")

    return {
        "markdown_path": str(md_path),
        "html_path": str(html_path),
        "generated_at": generated_at,
    }


# ── Rich HTML renderer (standalone, no external dependencies) ─────────────────

def _badge(status: str) -> str:
    """Return an inline HTML badge for a status string."""
    colour_map = {
        "good": ("#16a34a", "#dcfce7"),
        "ok": ("#ca8a04", "#fef9c3"),
        "warning": ("#ca8a04", "#fef9c3"),
        "critical": ("#dc2626", "#fee2e2"),
        "bad": ("#dc2626", "#fee2e2"),
        "active": ("#2563eb", "#dbeafe"),
        "unknown": ("#6b7280", "#f3f4f6"),
    }
    fg, bg = colour_map.get(status.lower(), ("#6b7280", "#f3f4f6"))
    return (
        f'<span style="display:inline-block;padding:2px 8px;border-radius:4px;'
        f'font-size:0.8em;font-weight:600;color:{fg};background:{bg}">'
        f"{status.upper()}</span>"
    )


def _score_color(score: int) -> str:
    if score >= 75:
        return "#16a34a"
    if score >= 50:
        return "#ca8a04"
    return "#dc2626"


def _fmt(amount: float, currency: str = "EUR") -> str:
    try:
        from currency import format_money
        return format_money(amount, currency)
    except Exception:
        symbol = {"EUR": "€", "USD": "$", "GBP": "£"}.get(currency, currency + " ")
        return f"{symbol}{amount:,.2f}"


def _render_html_full(suite: dict) -> str:
    """
    Render a clean, standalone single-file HTML report with inline CSS.

    Layout: dark sidebar with health score on the left, white content area on the right.
    Badges are colour-coded: green=good, amber=warning, red=critical.
    No external dependencies — works as a plain .html file.
    """
    year = suite.get("year", datetime.now().year)
    month = suite.get("month", datetime.now().strftime("%Y-%m"))
    generated_at = suite.get("generated_at", datetime.now().isoformat(timespec="seconds"))
    health = suite.get("financial_health", {})
    score = int(health.get("score", 0))
    score_col = _score_color(score)
    net_worth = health.get("net_worth", 0)
    trend = health.get("trend", "unknown")

    # ── Build section HTML strings ────────────────────────────────────────────

    sections = ""

    # Budget
    budget = suite.get("budget_report")
    if budget and isinstance(budget, dict) and "error" not in budget:
        income_t = budget.get("income_target", 0)
        total_p = budget.get("total_planned", 0)
        total_a = budget.get("total_actual", 0)
        overspends = budget.get("overspend_categories", [])
        over_html = ""
        if overspends:
            over_html = (
                f'<p><strong>Overspend in:</strong> '
                f'{", ".join(overspends)} {_badge("critical")}</p>'
            )
        sections += f"""
<section>
  <h2>Budget</h2>
  <table>
    <tr><td>Income target</td><td><strong>{_fmt(income_t)}</strong></td></tr>
    <tr><td>Total planned</td><td>{_fmt(total_p)}</td></tr>
    <tr><td>Total actual</td><td>{_fmt(total_a)}</td></tr>
  </table>
  {over_html}
</section>"""

    # Goals
    goals_report = suite.get("goals_report", {})
    goals = goals_report.get("goals", [])
    if goals:
        rows = ""
        for g in goals:
            target = float(g.get("target_amount", 0))
            current = float(g.get("current_amount", 0))
            pct = round(current / target * 100) if target > 0 else 0
            status = g.get("status", "active")
            bar_w = min(pct, 100)
            rows += f"""
    <tr>
      <td>{g.get("name", "—")}</td>
      <td>
        <div style="background:#e5e7eb;border-radius:4px;height:8px;width:120px;display:inline-block;vertical-align:middle">
          <div style="background:#2563eb;border-radius:4px;height:8px;width:{bar_w}%"></div>
        </div>
        <span style="margin-left:6px">{pct}%</span>
      </td>
      <td>{_fmt(current)} / {_fmt(target)}</td>
      <td>{_badge(status)}</td>
    </tr>"""
        sections += f"""
<section>
  <h2>Savings Goals</h2>
  <table>
    <thead><tr><th>Goal</th><th>Progress</th><th>Amount</th><th>Status</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>
</section>"""

    # Investments
    inv = suite.get("investment_report", {})
    if inv and inv.get("total_current_value", 0) > 0:
        ret_pct = inv.get("total_return_pct", 0)
        ret_col = "#16a34a" if ret_pct >= 0 else "#dc2626"
        sections += f"""
<section>
  <h2>Investments</h2>
  <table>
    <tr><td>Portfolio value</td><td><strong>{_fmt(inv.get("total_current_value", 0))}</strong></td></tr>
    <tr><td>Total return</td>
        <td style="color:{ret_col}"><strong>{ret_pct:+.1f}%</strong></td></tr>
    <tr><td>Gain / Loss</td><td>{_fmt(inv.get("total_gain_loss", 0))}</td></tr>
  </table>
</section>"""

    # Debt
    debt = suite.get("debt_report", {})
    debts = debt.get("debts", [])
    if debts:
        total_debt = sum(float(d.get("balance", 0)) for d in debts)
        rows = "".join(
            f"<tr><td>{d.get('name','—')}</td>"
            f"<td>{_fmt(float(d.get('balance', 0)))}</td>"
            f"<td>{d.get('interest_rate', 0):.2f}%</td></tr>"
            for d in debts
        )
        comparison = debt.get("strategy_comparison")
        savings_html = ""
        if comparison and isinstance(comparison, dict):
            comp = comparison.get("comparison", {})
            saved = comp.get("interest_saved_by_avalanche")
            if saved:
                savings_html = (
                    f'<p>Avalanche vs Snowball: saves <strong>{_fmt(saved)}</strong> in interest.</p>'
                )
        sections += f"""
<section>
  <h2>Debt</h2>
  <p>Total debt: <strong>{_fmt(total_debt)}</strong></p>
  <table>
    <thead><tr><th>Name</th><th>Balance</th><th>Rate</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>
  {savings_html}
</section>"""

    # Insurance
    ins = suite.get("insurance_report", {})
    premiums = ins.get("premiums", {})
    if premiums.get("total_annual", 0) > 0:
        coverage = ins.get("coverage", {})
        gaps = coverage.get("gaps", [])
        gaps_html = ""
        if gaps:
            gap_names = ", ".join(g.get("name", "?") for g in gaps)
            gaps_html = f'<p>Coverage gaps: {gap_names} {_badge("warning")}</p>'
        sections += f"""
<section>
  <h2>Insurance</h2>
  <table>
    <tr><td>Annual premiums</td><td><strong>{_fmt(premiums.get("total_annual", 0))}</strong></td></tr>
  </table>
  {gaps_html}
</section>"""

    # Net Worth
    nw = suite.get("net_worth_report", {})
    current_nw = nw.get("current", {})
    if current_nw:
        bd = current_nw.get("breakdown", {})
        liabilities = bd.get("credit_card_balance", 0) + bd.get("loans_and_debt", 0)
        trend_badge = _badge("good") if trend == "up" else _badge("warning") if trend == "stable" else _badge("bad")
        sections += f"""
<section>
  <h2>Net Worth</h2>
  <table>
    <tr><td>Cash &amp; Savings</td><td>{_fmt(bd.get("cash_and_savings", 0))}</td></tr>
    <tr><td>Investments</td><td>{_fmt(bd.get("investments", 0))}</td></tr>
    <tr><td>Liabilities</td><td>{_fmt(liabilities)}</td></tr>
    <tr><td><strong>Net Worth</strong></td><td><strong>{_fmt(current_nw.get("net_worth", 0))}</strong></td></tr>
    <tr><td>Trend</td><td>{trend_badge}</td></tr>
  </table>
</section>"""

    # Action items
    actions = suite.get("action_list", [])
    if actions:
        items = "".join(
            f'<li><label><input type="checkbox"> {a}</label></li>'
            for a in actions[:10]
        )
        sections += f"""
<section>
  <h2>Action Items</h2>
  <ul class="actions">{items}</ul>
</section>"""

    # Insights
    insights = suite.get("insights", [])
    if insights:
        rows = "".join(
            f"<tr>"
            f"<td>{i.get('domain','—')}</td>"
            f"<td>{i.get('title','—')}</td>"
            f"<td>{_badge(i.get('status','unknown'))}</td>"
            f"<td>{i.get('next_action','')}</td>"
            f"</tr>"
            for i in insights[:8]
        )
        sections += f"""
<section>
  <h2>Insights</h2>
  <table>
    <thead><tr><th>Domain</th><th>Insight</th><th>Status</th><th>Action</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>
</section>"""

    # Specialist handoff
    handoff = suite.get("specialist_handoff", {})
    if isinstance(handoff, dict) and handoff.get("requires_specialist_review"):
        triggers = "".join(
            f"<li>{t.get('reason','')}</li>"
            for t in handoff.get("triggers", [])
        )
        sections += f"""
<section class="handoff">
  <h2>Specialist Review Recommended {_badge("critical")}</h2>
  <p>Risk level: <strong>{handoff.get("risk_level","—")}</strong></p>
  <ul>{triggers}</ul>
</section>"""

    # ── CSS ───────────────────────────────────────────────────────────────────
    css = """
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      font-size: 15px;
      line-height: 1.6;
      color: #1a1a1a;
      background: #f5f5f5;
      display: flex;
      min-height: 100vh;
    }
    /* ── Sidebar ── */
    .sidebar {
      width: 220px;
      min-width: 220px;
      background: #1e293b;
      color: #e2e8f0;
      padding: 32px 20px;
      position: sticky;
      top: 0;
      height: 100vh;
      overflow-y: auto;
      flex-shrink: 0;
    }
    .sidebar h1 { font-size: 1rem; color: #94a3b8; text-transform: uppercase;
                  letter-spacing: .08em; margin-bottom: 24px; }
    .score-circle {
      width: 120px; height: 120px;
      border-radius: 50%;
      margin: 0 auto 20px;
      display: flex; flex-direction: column;
      align-items: center; justify-content: center;
      background: conic-gradient(var(--score-col) calc(var(--score-pct) * 1%), #334155 0);
      position: relative;
    }
    .score-inner {
      width: 96px; height: 96px;
      border-radius: 50%;
      background: #1e293b;
      display: flex; flex-direction: column;
      align-items: center; justify-content: center;
    }
    .score-num { font-size: 2em; font-weight: 700; }
    .score-label { font-size: 0.7em; color: #94a3b8; }
    .sidebar-stat { margin-bottom: 14px; }
    .sidebar-stat .label { font-size: 0.75em; color: #64748b; text-transform: uppercase; }
    .sidebar-stat .value { font-weight: 600; font-size: 0.95em; }
    .sidebar hr { border: none; border-top: 1px solid #334155; margin: 20px 0; }
    .sidebar .meta { font-size: 0.75em; color: #64748b; }
    /* ── Main content ── */
    .main {
      flex: 1;
      padding: 32px 36px;
      max-width: 900px;
    }
    .main > h1 { font-size: 1.6rem; margin-bottom: 4px; }
    .main > .subtitle { color: #64748b; font-size: 0.9em; margin-bottom: 32px; }
    section { background: #fff; border-radius: 10px; padding: 24px;
              margin-bottom: 20px; box-shadow: 0 1px 3px rgba(0,0,0,.06); }
    section h2 { font-size: 1.05rem; color: #1e40af; margin-bottom: 16px;
                 padding-bottom: 8px; border-bottom: 1px solid #e5e7eb; }
    table { width: 100%; border-collapse: collapse; font-size: 0.9em; }
    th { text-align: left; font-size: 0.8em; text-transform: uppercase;
         color: #6b7280; letter-spacing: .05em; padding: 6px 8px;
         border-bottom: 2px solid #e5e7eb; }
    td { padding: 8px 8px; border-bottom: 1px solid #f3f4f6; vertical-align: top; }
    tr:last-child td { border-bottom: none; }
    p { margin: 8px 0; }
    ul { padding-left: 20px; }
    li { margin: 4px 0; }
    ul.actions { list-style: none; padding: 0; }
    ul.actions li { padding: 6px 0; border-bottom: 1px solid #f3f4f6; }
    ul.actions li:last-child { border-bottom: none; }
    section.handoff { border-left: 4px solid #dc2626; }
    @media (max-width: 700px) {
      body { flex-direction: column; }
      .sidebar { width: 100%; min-width: 0; height: auto; position: static; }
      .score-circle { width: 80px; height: 80px; }
      .score-inner { width: 62px; height: 62px; }
      .main { padding: 20px 16px; }
    }
    """

    # ── Assemble HTML ─────────────────────────────────────────────────────────
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Finance Report — {month}</title>
  <style>{css}</style>
</head>
<body>

<aside class="sidebar">
  <h1>Finance Report</h1>

  <div class="score-circle"
       style="--score-col:{score_col};--score-pct:{score}">
    <div class="score-inner">
      <span class="score-num" style="color:{score_col}">{score}</span>
      <span class="score-label">/ 100</span>
    </div>
  </div>

  <div class="sidebar-stat">
    <div class="label">Net Worth</div>
    <div class="value">{_fmt(net_worth)}</div>
  </div>

  <div class="sidebar-stat">
    <div class="label">Trend</div>
    <div class="value">{trend}</div>
  </div>

  <hr>
  <div class="meta">Generated<br>{generated_at[:10]}</div>
</aside>

<main class="main">
  <h1>Finance Report — {month}</h1>
  <p class="subtitle">Generated {generated_at}</p>

  {sections}

  <p class="meta" style="color:#94a3b8;font-size:0.8em;text-align:right;margin-top:20px">
    Generated by Finance Assistant
  </p>
</main>

</body>
</html>
"""
    return html


if __name__ == "__main__":
    result = generate_monthly_report()
    print("Report generated:")
    print(f"  Markdown : {result['markdown_path']}")
    print(f"  HTML     : {result['html_path']}")
    print(f"  At       : {result['generated_at']}")
