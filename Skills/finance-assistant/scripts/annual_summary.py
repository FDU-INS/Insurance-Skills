"""
Finance Assistant Accountant-Ready Annual Summary.

Generates structured annual summaries for handoff to accountants / Steuerberater.
Renders as standalone print-friendly HTML and clean Markdown.
"""

from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    from finance_storage import ensure_subdir, load_json
    from profile_manager import get_profile
    from transaction_logger import get_transactions, get_totals
    from investment_tracker import get_portfolio
except ImportError:
    import sys
    sys.path.insert(0, os.path.dirname(__file__))
    from finance_storage import ensure_subdir, load_json
    from profile_manager import get_profile
    from transaction_logger import get_transactions, get_totals
    from investment_tracker import get_portfolio


# ── Internal helpers ──────────────────────────────────────────────────────────

def _cur_sym(currency: str) -> str:
    return {"EUR": "€", "GBP": "£", "USD": "$", "CHF": "CHF "}.get(currency, currency + " ")


def _fmt_money(amount: float, currency: str) -> str:
    sym = _cur_sym(currency)
    return f"{sym}{abs(amount):,.2f}"


def _status_badge_html(status: str) -> str:
    colors = {
        "complete":       ("#d4edda", "#155724"),
        "needs_evidence": ("#fff3cd", "#856404"),
        "needs_input":    ("#fff3cd", "#856404"),
        "not_applicable": ("#e2e3e5", "#383d41"),
        "estimated":      ("#cce5ff", "#004085"),
    }
    bg, fg = colors.get(status, ("#e2e3e5", "#383d41"))
    label = status.replace("_", " ").title()
    return (
        f'<span style="background:{bg};color:{fg};padding:2px 8px;'
        f'border-radius:4px;font-size:0.82em;font-weight:600">{label}</span>'
    )


def _load_tax_claims(locale: str, year: int) -> list[dict]:
    """Load tax claims from .finance/taxes/{locale}/{year}-claims.json if available."""
    try:
        path = ensure_subdir("taxes", locale) / f"{year}-claims.json"
        data = load_json(path, default={"claims": []})
        return data.get("claims", []) if isinstance(data, dict) else []
    except Exception:
        return []


def _load_investment_summary(year: int) -> dict:
    """Compute investment summary from portfolio."""
    try:
        portfolio = get_portfolio()
        holdings = portfolio.get("holdings", [])
        total_value = 0.0
        realized_gains = 0.0
        dividends = 0.0
        for h in holdings:
            current = float(h.get("current_value", 0) or h.get("units", 0) * h.get("current_price", 0))
            cost = float(h.get("cost_basis", 0))
            total_value += current
            if h.get("sold", False):
                realized_gains += current - cost
            dividends += float(h.get("dividends_ytd", 0))
        return {
            "total_value": round(total_value, 2),
            "realized_gains": round(realized_gains, 2),
            "dividends": round(dividends, 2),
        }
    except Exception:
        return {"total_value": 0.0, "realized_gains": 0.0, "dividends": 0.0}


def _load_donation_summary(account_id: str, year: int) -> dict:
    """Sum donation-category transactions for the year."""
    try:
        txns = get_transactions(account_id=account_id, year=year, category="gifts")
        total = sum(abs(float(t.get("amount", 0))) for t in txns if float(t.get("amount", 0)) < 0)
        return {"total": round(total, 2)}
    except Exception:
        return {"total": 0.0}


def _load_income_summary(account_id: str, year: int, profile: dict) -> dict:
    """Build income summary from transactions + profile."""
    try:
        totals = get_totals(account_id=account_id, year=year)
        gross = 0.0
        for cat, data in totals.items():
            gross += data.get("income", 0.0)
        net = gross  # no precise net without payslip data; use gross as baseline

        employment = profile.get("employment", {})
        return {
            "gross": round(gross, 2),
            "net": round(net, 2),
            "employer": employment.get("employer_name", ""),
            "type": employment.get("type", ""),
        }
    except Exception:
        return {"gross": 0.0, "net": 0.0, "employer": "", "type": ""}


# ── Public API ────────────────────────────────────────────────────────────────

def generate_annual_summary(
    year: Optional[int] = None,
    profile: Optional[dict] = None,
) -> dict:
    """
    Build a structured annual summary for handoff to accountant/Steuerberater.

    Returns a dict with all sections: income, claims, investments, donations,
    outstanding items, and metadata.
    """
    if year is None:
        year = datetime.now().year - 1  # default to last tax year

    profile = profile or get_profile() or {}
    meta = profile.get("meta", {})
    personal = profile.get("personal", {})
    locale = meta.get("locale", "de")
    currency = meta.get("primary_currency", "EUR")
    account_id = profile.get("accounts", [{}])[0].get("id", "default") if profile.get("accounts") else "default"

    income = _load_income_summary(account_id, year, profile)
    claims = _load_tax_claims(locale, year)
    investments = _load_investment_summary(year)
    donation_data = _load_donation_summary(account_id, year)

    # Gift Aid is UK-specific
    gift_aid = locale == "gb" or currency == "GBP"

    outstanding = [
        c for c in claims
        if c.get("status") in ("needs_evidence", "needs_input")
    ]

    return {
        "year": year,
        "generated_at": datetime.now().isoformat(),
        "profile_name": personal.get("name", ""),
        "locale": locale,
        "currency": currency,
        "income": income,
        "claims": claims,
        "investments": investments,
        "donations": {
            "total": donation_data["total"],
            "gift_aid_eligible": gift_aid,
        },
        "outstanding": outstanding,
        "notes": "",
    }


def render_annual_summary_html(summary: dict) -> str:
    """
    Render as standalone single-file, print-friendly (A4) HTML.

    Sections:
    1. Cover: name, tax year, generated date, locale, currency
    2. Income summary
    3. Deduction claims (table with status badges)
    4. Investment summary
    5. Charitable giving
    6. Outstanding items (amber highlights)
    7. Footer
    """
    year = summary.get("year", "")
    generated = summary.get("generated_at", "")[:10]
    name = summary.get("profile_name", "")
    locale = summary.get("locale", "")
    currency = summary.get("currency", "EUR")
    income = summary.get("income", {})
    claims = summary.get("claims", [])
    investments = summary.get("investments", {})
    donations = summary.get("donations", {})
    outstanding = summary.get("outstanding", [])
    notes = summary.get("notes", "")

    sym = _cur_sym(currency)

    def money(amount: float) -> str:
        return f"{sym}{abs(amount):,.2f}"

    # Build claims table rows
    claims_rows = ""
    for c in claims:
        title = c.get("title", "")
        status = c.get("status", "")
        amount = c.get("amount_estimate", 0.0)
        confidence = c.get("confidence", "")
        evidence = c.get("evidence_required", "")
        law_ref = c.get("law_reference", "")
        row_bg = " style='background:#fffbea'" if status in ("needs_evidence", "needs_input") else ""
        claims_rows += f"""
        <tr{row_bg}>
          <td>{title}</td>
          <td>{_status_badge_html(status)}</td>
          <td style="text-align:right">{money(float(amount)) if amount else "—"}</td>
          <td>{confidence}</td>
          <td>{evidence}</td>
          <td style="color:#555;font-size:0.85em">{law_ref}</td>
        </tr>"""

    outstanding_html = ""
    if outstanding:
        items_list = "".join(
            f"<li><strong>{c.get('title','')}</strong>: {c.get('evidence_required','')}"
            f" <em>({c.get('status','').replace('_',' ')})</em></li>"
            for c in outstanding
        )
        outstanding_html = f"""
        <section class="page-break">
          <h2>6. Outstanding Items</h2>
          <div class="warning-box">
            <p>The following items require attention before filing:</p>
            <ul>{items_list}</ul>
          </div>
        </section>"""

    notes_html = f"<p><strong>Notes:</strong> {notes}</p>" if notes else ""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Annual Summary {year} — {name}</title>
<style>
  /* ── Base ── */
  *, *::before, *::after {{ box-sizing: border-box; }}
  body {{
    font-family: Georgia, 'Times New Roman', serif;
    font-size: 11pt;
    line-height: 1.5;
    color: #1a1a1a;
    background: #fff;
    margin: 0;
    padding: 0;
  }}
  h1 {{ font-size: 1.8em; margin-bottom: 0.2em; }}
  h2 {{ font-size: 1.25em; margin-top: 2em; border-bottom: 1px solid #ccc; padding-bottom: 0.3em; }}
  h3 {{ font-size: 1.05em; color: #333; }}
  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 1em 0;
    font-size: 0.9em;
  }}
  th {{
    background: #f0f0f0;
    text-align: left;
    padding: 6px 8px;
    border-bottom: 2px solid #ccc;
  }}
  td {{ padding: 5px 8px; border-bottom: 1px solid #e5e5e5; }}
  .cover {{ text-align: center; padding: 3cm 2cm 2cm; }}
  .cover-subtitle {{ color: #555; font-size: 1.1em; margin-top: 0.5em; }}
  .meta-grid {{ display: flex; gap: 2em; justify-content: center; margin-top: 1.5em; font-size: 0.95em; color: #444; }}
  section {{ margin: 0 2cm; padding: 0.5cm 0; }}
  .kv-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 0.5em 2em; }}
  .kv-item {{ display: flex; justify-content: space-between; border-bottom: 1px dotted #ddd; padding: 3px 0; }}
  .kv-label {{ color: #555; }}
  .kv-value {{ font-weight: 600; }}
  .warning-box {{
    background: #fffbea;
    border-left: 4px solid #f0ad4e;
    padding: 0.8em 1em;
    margin: 1em 0;
    border-radius: 2px;
  }}
  .footer {{
    text-align: center;
    font-size: 0.8em;
    color: #888;
    border-top: 1px solid #ddd;
    padding: 1em 2cm;
    margin-top: 2em;
  }}
  .page-break {{ page-break-before: always; }}

  /* ── Print ── */
  @media print {{
    @page {{
      size: A4;
      margin: 2cm 2cm 2.5cm;
    }}
    body {{
      font-size: 10pt;
      background: #fff !important;
      color: #000 !important;
    }}
    section {{ margin: 0; }}
    .no-print {{ display: none; }}
    a {{ color: #000; text-decoration: none; }}
    .page-break {{ page-break-before: always; }}
  }}
</style>
</head>
<body>

<!-- 1. Cover -->
<div class="cover">
  <h1>Annual Financial Summary</h1>
  <p class="cover-subtitle">Tax Year {year}</p>
  {"<p style='font-size:1.2em;font-weight:600;margin-top:0.5em'>" + name + "</p>" if name else ""}
  <div class="meta-grid">
    <span>Generated: {generated}</span>
    <span>Locale: {locale.upper()}</span>
    <span>Currency: {currency}</span>
  </div>
</div>

<!-- 2. Income Summary -->
<section>
  <h2>2. Income Summary</h2>
  <div class="kv-grid">
    <div class="kv-item"><span class="kv-label">Gross Income</span><span class="kv-value">{money(income.get('gross', 0))}</span></div>
    <div class="kv-item"><span class="kv-label">Net Income</span><span class="kv-value">{money(income.get('net', 0))}</span></div>
    <div class="kv-item"><span class="kv-label">Employer</span><span class="kv-value">{income.get('employer','—')}</span></div>
    <div class="kv-item"><span class="kv-label">Employment Type</span><span class="kv-value">{income.get('type','—')}</span></div>
  </div>
</section>

<!-- 3. Deduction Claims -->
<section class="page-break">
  <h2>3. Deduction Claims</h2>
  {"<p style='color:#666'>No claims recorded for this year.</p>" if not claims else ""}
  {"<table><thead><tr><th>Description</th><th>Status</th><th style='text-align:right'>Amount Est.</th><th>Confidence</th><th>Evidence Required</th><th>Law Reference</th></tr></thead><tbody>" + claims_rows + "</tbody></table>" if claims else ""}
</section>

<!-- 4. Investment Summary -->
<section class="page-break">
  <h2>4. Investment Summary</h2>
  <div class="kv-grid">
    <div class="kv-item"><span class="kv-label">Portfolio Total Value</span><span class="kv-value">{money(investments.get('total_value', 0))}</span></div>
    <div class="kv-item"><span class="kv-label">Realized Gains</span><span class="kv-value">{money(investments.get('realized_gains', 0))}</span></div>
    <div class="kv-item"><span class="kv-label">Dividends Received</span><span class="kv-value">{money(investments.get('dividends', 0))}</span></div>
  </div>
</section>

<!-- 5. Charitable Giving -->
<section>
  <h2>5. Charitable Giving</h2>
  <div class="kv-grid">
    <div class="kv-item"><span class="kv-label">Total Donations</span><span class="kv-value">{money(donations.get('total', 0))}</span></div>
    <div class="kv-item"><span class="kv-label">Gift Aid Eligible</span><span class="kv-value">{'Yes — include Gift Aid declaration' if donations.get('gift_aid_eligible') else 'No'}</span></div>
  </div>
</section>

<!-- 6. Outstanding Items -->
{outstanding_html}

<!-- Notes -->
{notes_html}

<!-- 7. Footer -->
<div class="footer">
  Prepared with Finance Assistant — verify all figures before filing.<br>
  This document does not constitute legal or tax advice.
</div>

</body>
</html>"""

    return html


def render_annual_summary_markdown(summary: dict) -> str:
    """
    Render the same content as the HTML report as clean Markdown for copy-paste.
    """
    year = summary.get("year", "")
    generated = summary.get("generated_at", "")[:10]
    name = summary.get("profile_name", "")
    locale = summary.get("locale", "")
    currency = summary.get("currency", "EUR")
    income = summary.get("income", {})
    claims = summary.get("claims", [])
    investments = summary.get("investments", {})
    donations = summary.get("donations", {})
    outstanding = summary.get("outstanding", [])
    notes = summary.get("notes", "")

    sym = _cur_sym(currency)

    def money(amount: float) -> str:
        return f"{sym}{abs(amount):,.2f}"

    lines = [
        f"# Annual Financial Summary — {year}",
        "",
        f"**Name:** {name}  ",
        f"**Generated:** {generated}  ",
        f"**Locale:** {locale.upper()}  ",
        f"**Currency:** {currency}",
        "",
        "---",
        "",
        "## 2. Income Summary",
        "",
        f"| Field | Value |",
        f"|-------|-------|",
        f"| Gross Income | {money(income.get('gross', 0))} |",
        f"| Net Income | {money(income.get('net', 0))} |",
        f"| Employer | {income.get('employer','—')} |",
        f"| Employment Type | {income.get('type','—')} |",
        "",
        "---",
        "",
        "## 3. Deduction Claims",
        "",
    ]

    if claims:
        lines.append("| Description | Status | Amount Est. | Confidence | Evidence Required | Law Reference |")
        lines.append("|-------------|--------|-------------|------------|-------------------|---------------|")
        for c in claims:
            status = c.get("status", "").replace("_", " ")
            amt = money(float(c.get("amount_estimate", 0))) if c.get("amount_estimate") else "—"
            lines.append(
                f"| {c.get('title','')} | {status} | {amt} | "
                f"{c.get('confidence','')} | {c.get('evidence_required','')} | "
                f"{c.get('law_reference','')} |"
            )
    else:
        lines.append("_No claims recorded for this year._")

    lines += [
        "",
        "---",
        "",
        "## 4. Investment Summary",
        "",
        f"| Field | Value |",
        f"|-------|-------|",
        f"| Portfolio Total Value | {money(investments.get('total_value', 0))} |",
        f"| Realized Gains | {money(investments.get('realized_gains', 0))} |",
        f"| Dividends Received | {money(investments.get('dividends', 0))} |",
        "",
        "---",
        "",
        "## 5. Charitable Giving",
        "",
        f"| Field | Value |",
        f"|-------|-------|",
        f"| Total Donations | {money(donations.get('total', 0))} |",
        f"| Gift Aid Eligible | {'Yes — include Gift Aid declaration' if donations.get('gift_aid_eligible') else 'No'} |",
        "",
        "---",
        "",
    ]

    if outstanding:
        lines += [
            "## 6. Outstanding Items",
            "",
            "> **Action required** — the following items need attention before filing:",
            "",
        ]
        for c in outstanding:
            status = c.get("status", "").replace("_", " ")
            lines.append(
                f"- **{c.get('title','')}**: {c.get('evidence_required','')} _{status}_"
            )
        lines.append("")

    if notes:
        lines += [f"**Notes:** {notes}", ""]

    lines += [
        "---",
        "",
        "_Prepared with Finance Assistant — verify all figures before filing._",
        "_This document does not constitute legal or tax advice._",
    ]

    return "\n".join(lines)


def save_annual_summary(
    year: Optional[int] = None,
    profile: Optional[dict] = None,
) -> dict:
    """
    Orchestrate: build summary → render both formats → save to
    .finance/reports/annual-YYYY.{html,md}.

    Returns:
        {
            "year": int,
            "html_path": str,
            "markdown_path": str,
            "generated_at": str,
        }
    """
    summary = generate_annual_summary(year=year, profile=profile)
    year = summary["year"]

    reports_dir = ensure_subdir("reports")
    html_path = reports_dir / f"annual-{year}.html"
    md_path = reports_dir / f"annual-{year}.md"

    html_content = render_annual_summary_html(summary)
    md_content = render_annual_summary_markdown(summary)

    html_path.write_text(html_content, encoding="utf-8")
    md_path.write_text(md_content, encoding="utf-8")

    return {
        "year": year,
        "html_path": str(html_path),
        "markdown_path": str(md_path),
        "generated_at": summary["generated_at"],
        "summary": summary,
    }
