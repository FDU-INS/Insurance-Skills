"""
Finance Assistant Report Renderer.

Generates clean markdown and HTML reports from the output suite.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

try:
    from finance_storage import ensure_subdir
    from currency import format_money
except ImportError:
    import os, sys
    sys.path.insert(0, os.path.dirname(__file__))
    from finance_storage import ensure_subdir
    from currency import format_money


def render_markdown(suite: dict) -> str:
    """Render the output suite as a clean markdown report."""
    year = suite.get("year", datetime.now().year)
    health = suite.get("financial_health", {})
    lines = [
        f"# Finance Report — {year}",
        f"*Generated: {suite.get('generated_at', datetime.now().isoformat())}*\n",
        "---\n",
        f"## Financial Health: {health.get('score', 0)}%",
        f"- **Net Worth:** {format_money(health.get('net_worth', 0), 'EUR')}",
        f"- **Trend:** {health.get('trend', 'unknown')}\n",
    ]

    # Budget
    budget = suite.get("budget_report")
    if budget and isinstance(budget, dict) and "error" not in budget:
        lines.append("## Budget")
        lines.append(f"- Income target: {format_money(budget.get('income_target', 0), 'EUR')}")
        lines.append(f"- Total planned: {format_money(budget.get('total_planned', 0), 'EUR')}")
        lines.append(f"- Total actual: {format_money(budget.get('total_actual', 0), 'EUR')}")
        overspends = budget.get("overspend_categories", [])
        if overspends:
            lines.append(f"- Overspend in: {', '.join(overspends)}")
        lines.append("")

    # Goals
    goals_report = suite.get("goals_report", {})
    goals = goals_report.get("goals", [])
    if goals:
        lines.append("## Savings Goals")
        for g in goals:
            target = float(g.get("target_amount", 0))
            current = float(g.get("current_amount", 0))
            pct = round(current / target * 100) if target > 0 else 0
            lines.append(f"- **{g.get('name', '?')}**: {format_money(current, 'EUR')} / "
                        f"{format_money(target, 'EUR')} ({pct}%)")
        lines.append("")

    # Investments
    inv = suite.get("investment_report", {})
    if inv and inv.get("total_current_value", 0) > 0:
        lines.append("## Investments")
        lines.append(f"- Portfolio value: {format_money(inv.get('total_current_value', 0), 'EUR')}")
        lines.append(f"- Total return: {inv.get('total_return_pct', 0):+.1f}%")
        lines.append(f"- Gain/Loss: {format_money(inv.get('total_gain_loss', 0), 'EUR')}")
        lines.append("")

    # Debt
    debt = suite.get("debt_report", {})
    debts = debt.get("debts", [])
    if debts:
        lines.append("## Debt")
        total_debt = sum(float(d.get("balance", 0)) for d in debts)
        lines.append(f"- Total debt: {format_money(total_debt, 'EUR')}")
        for d in debts:
            lines.append(f"  - {d.get('name', '?')}: {format_money(d.get('balance', 0), 'EUR')} "
                        f"at {d.get('interest_rate', 0)}%")
        comparison = debt.get("strategy_comparison")
        if comparison and isinstance(comparison, dict):
            comp = comparison.get("comparison", {})
            if comp.get("interest_saved_by_avalanche"):
                lines.append(f"- Avalanche saves: {format_money(comp['interest_saved_by_avalanche'], 'EUR')} in interest")
        lines.append("")

    # Insurance
    ins = suite.get("insurance_report", {})
    premiums = ins.get("premiums", {})
    if premiums.get("total_annual", 0) > 0:
        lines.append("## Insurance")
        lines.append(f"- Annual premiums: {format_money(premiums.get('total_annual', 0), 'EUR')}")
        coverage = ins.get("coverage", {})
        gaps = coverage.get("gaps", [])
        if gaps:
            lines.append(f"- Coverage gaps: {', '.join(g.get('name', '?') for g in gaps)}")
        lines.append("")

    # Net Worth
    nw = suite.get("net_worth_report", {})
    current_nw = nw.get("current", {})
    if current_nw:
        lines.append("## Net Worth")
        bd = current_nw.get("breakdown", {})
        lines.append(f"- Cash & Savings: {format_money(bd.get('cash_and_savings', 0), 'EUR')}")
        lines.append(f"- Investments: {format_money(bd.get('investments', 0), 'EUR')}")
        lines.append(f"- Liabilities: {format_money(bd.get('credit_card_balance', 0) + bd.get('loans_and_debt', 0), 'EUR')}")
        lines.append(f"- **Net Worth: {format_money(current_nw.get('net_worth', 0), 'EUR')}**")
        lines.append("")

    # Actions
    actions = suite.get("action_list", [])
    if actions:
        lines.append("## Action Items")
        for a in actions[:10]:
            lines.append(f"- [ ] {a}")
        lines.append("")

    # Specialist
    handoff = suite.get("specialist_handoff", {})
    if isinstance(handoff, dict) and handoff.get("requires_specialist_review"):
        lines.append("## Specialist Review Recommended")
        lines.append(f"Risk level: {handoff.get('risk_level', '—')}")
        for t in handoff.get("triggers", []):
            lines.append(f"- {t.get('reason', '')}")
        lines.append("")

    lines.append("---")
    lines.append("*Generated by Finance Assistant*")

    return "\n".join(lines)


def render_html(suite: dict) -> str:
    """Render the output suite as an HTML report."""
    md = render_markdown(suite)
    # Simple markdown to HTML conversion for key elements
    html_lines = [
        "<!DOCTYPE html>",
        "<html><head>",
        "<meta charset='utf-8'>",
        "<title>Finance Report</title>",
        "<style>",
        "body { font-family: -apple-system, system-ui, sans-serif; max-width: 800px; margin: 40px auto; padding: 0 20px; color: #1a1a1a; line-height: 1.6; }",
        "h1 { border-bottom: 2px solid #333; padding-bottom: 10px; }",
        "h2 { color: #2563eb; margin-top: 30px; }",
        "hr { border: none; border-top: 1px solid #e5e5e5; margin: 20px 0; }",
        ".score { font-size: 2em; font-weight: bold; }",
        ".score.good { color: #16a34a; } .score.ok { color: #ca8a04; } .score.bad { color: #dc2626; }",
        "ul { padding-left: 20px; }",
        "li { margin: 5px 0; }",
        "em { color: #666; font-size: 0.9em; }",
        "</style>",
        "</head><body>",
    ]

    for line in md.split("\n"):
        if line.startswith("# "):
            html_lines.append(f"<h1>{line[2:]}</h1>")
        elif line.startswith("## "):
            html_lines.append(f"<h2>{line[3:]}</h2>")
        elif line.startswith("- **"):
            content = line[2:]
            content = content.replace("**", "<strong>", 1).replace("**", "</strong>", 1)
            html_lines.append(f"<li>{content}</li>")
        elif line.startswith("- [ ] "):
            html_lines.append(f"<li><input type='checkbox'> {line[6:]}</li>")
        elif line.startswith("- "):
            html_lines.append(f"<li>{line[2:]}</li>")
        elif line.startswith("  - "):
            html_lines.append(f"<li style='margin-left:20px'>{line[4:]}</li>")
        elif line.startswith("*") and line.endswith("*"):
            html_lines.append(f"<em>{line.strip('*')}</em>")
        elif line == "---":
            html_lines.append("<hr>")
        elif line:
            html_lines.append(f"<p>{line}</p>")

    html_lines.extend(["</body></html>"])
    return "\n".join(html_lines)


def save_report(suite: dict, format: str = "markdown") -> str:
    """Save report to the workspace directory. Returns file path."""
    year = suite.get("year", datetime.now().year)
    reports_dir = ensure_subdir("workspace", "reports")

    if format == "html":
        content = render_html(suite)
        path = reports_dir / f"finance-report-{year}.html"
    else:
        content = render_markdown(suite)
        path = reports_dir / f"finance-report-{year}.md"

    path.write_text(content, encoding="utf-8")
    return str(path)
