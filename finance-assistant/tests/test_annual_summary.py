"""
Tests for annual_summary.py.

Uses mocked dependencies (profile_manager, transaction_logger, investment_tracker)
and a temporary .finance directory for file output tests.
"""

import os
import sys
import pytest
from unittest.mock import patch, MagicMock

scripts_dir = os.path.join(os.path.dirname(__file__), "..", "scripts")
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)


@pytest.fixture(autouse=True)
def isolated_finance_dir(tmp_path, monkeypatch):
    """Each test gets a fresh .finance/ directory."""
    monkeypatch.setenv("FINANCE_PROJECT_DIR", str(tmp_path))
    for mod in ["finance_storage", "annual_summary", "profile_manager",
                "transaction_logger", "investment_tracker", "currency"]:
        if mod in sys.modules:
            del sys.modules[mod]
    yield tmp_path


# ── Sample data ───────────────────────────────────────────────────────────────

SAMPLE_PROFILE = {
    "meta": {
        "version": "2.0",
        "primary_currency": "EUR",
        "locale": "de",
        "language": "en",
    },
    "personal": {"name": "Max Mustermann"},
    "employment": {
        "type": "employed",
        "employer_name": "ACME GmbH",
    },
    "accounts": [{"id": "checking"}],
}

SAMPLE_CLAIMS = [
    {
        "title": "Home Office Deduction",
        "status": "complete",
        "amount_estimate": 1200.0,
        "confidence": "high",
        "evidence_required": "Employer certificate",
        "law_reference": "§ 4 Abs. 5 EStG",
    },
    {
        "title": "Professional Development",
        "status": "needs_evidence",
        "amount_estimate": 800.0,
        "confidence": "medium",
        "evidence_required": "Course receipts",
        "law_reference": "§ 9 EStG",
    },
    {
        "title": "Commute",
        "status": "needs_input",
        "amount_estimate": 600.0,
        "confidence": "likely",
        "evidence_required": "Days worked, distance",
        "law_reference": "§ 9 Abs. 1 Nr. 4 EStG",
    },
]

SAMPLE_TRANSACTIONS_INCOME = [
    {"date": "2024-03-15", "amount": 3500.0, "type": "income", "category": "salary"},
    {"date": "2024-04-15", "amount": 3500.0, "type": "income", "category": "salary"},
]

SAMPLE_PORTFOLIO = {
    "holdings": [
        {
            "id": "etf1",
            "symbol": "VWCE",
            "units": 10,
            "cost_basis": 8000.0,
            "current_value": 9500.0,
            "sold": False,
            "dividends_ytd": 50.0,
        },
        {
            "id": "stock1",
            "symbol": "AAPL",
            "units": 5,
            "cost_basis": 1000.0,
            "current_value": 1200.0,
            "sold": True,  # realized gain
        },
    ]
}


# ── generate_annual_summary ───────────────────────────────────────────────────

def test_generate_annual_summary_structure():
    with patch("annual_summary.get_profile", return_value=SAMPLE_PROFILE):
        with patch("annual_summary.get_transactions", return_value=SAMPLE_TRANSACTIONS_INCOME):
            with patch("annual_summary.get_totals", return_value={"salary": {"income": 42000.0, "expense": 0.0, "count": 12, "net": 42000.0}}):
                with patch("annual_summary.get_portfolio", return_value=SAMPLE_PORTFOLIO):
                    from annual_summary import generate_annual_summary
                    result = generate_annual_summary(year=2024)

    # All required top-level keys
    required_keys = ["year", "generated_at", "profile_name", "locale", "currency",
                     "income", "claims", "investments", "donations", "outstanding", "notes"]
    for key in required_keys:
        assert key in result, f"Missing key: {key}"

    assert result["year"] == 2024
    assert result["profile_name"] == "Max Mustermann"
    assert result["locale"] == "de"
    assert result["currency"] == "EUR"


def test_generate_annual_summary_income():
    with patch("annual_summary.get_profile", return_value=SAMPLE_PROFILE):
        with patch("annual_summary.get_transactions", return_value=SAMPLE_TRANSACTIONS_INCOME):
            with patch("annual_summary.get_totals", return_value={"salary": {"income": 42000.0, "expense": 0.0, "count": 12, "net": 42000.0}}):
                with patch("annual_summary.get_portfolio", return_value={"holdings": []}):
                    from annual_summary import generate_annual_summary
                    result = generate_annual_summary(year=2024)

    income = result["income"]
    assert income["gross"] == 42000.0
    assert income["employer"] == "ACME GmbH"
    assert income["type"] == "employed"


def test_generate_annual_summary_investments():
    with patch("annual_summary.get_profile", return_value=SAMPLE_PROFILE):
        with patch("annual_summary.get_transactions", return_value=[]):
            with patch("annual_summary.get_totals", return_value={}):
                with patch("annual_summary.get_portfolio", return_value=SAMPLE_PORTFOLIO):
                    from annual_summary import generate_annual_summary
                    result = generate_annual_summary(year=2024)

    inv = result["investments"]
    assert inv["total_value"] > 0
    assert inv["realized_gains"] > 0  # AAPL was sold at a gain
    assert inv["dividends"] == 50.0


def test_generate_annual_summary_outstanding():
    """Outstanding should filter to needs_evidence / needs_input claims."""
    with patch("annual_summary.get_profile", return_value=SAMPLE_PROFILE):
        with patch("annual_summary.get_transactions", return_value=[]):
            with patch("annual_summary.get_totals", return_value={}):
                with patch("annual_summary.get_portfolio", return_value={"holdings": []}):
                    with patch("annual_summary._load_tax_claims", return_value=SAMPLE_CLAIMS):
                        from annual_summary import generate_annual_summary
                        result = generate_annual_summary(year=2024)

    outstanding = result["outstanding"]
    statuses = {c["status"] for c in outstanding}
    assert "complete" not in statuses
    assert "needs_evidence" in statuses or "needs_input" in statuses
    assert len(outstanding) == 2  # Professional Development + Commute


def test_generate_annual_summary_gift_aid_uk():
    """Gift Aid should be True for GBP locale."""
    uk_profile = {**SAMPLE_PROFILE, "meta": {**SAMPLE_PROFILE["meta"], "locale": "gb", "primary_currency": "GBP"}}
    with patch("annual_summary.get_profile", return_value=uk_profile):
        with patch("annual_summary.get_transactions", return_value=[]):
            with patch("annual_summary.get_totals", return_value={}):
                with patch("annual_summary.get_portfolio", return_value={"holdings": []}):
                    from annual_summary import generate_annual_summary
                    result = generate_annual_summary(year=2024, profile=uk_profile)

    assert result["donations"]["gift_aid_eligible"] is True


def test_generate_annual_summary_gift_aid_de():
    """Gift Aid should be False for non-UK locale."""
    with patch("annual_summary.get_profile", return_value=SAMPLE_PROFILE):
        with patch("annual_summary.get_transactions", return_value=[]):
            with patch("annual_summary.get_totals", return_value={}):
                with patch("annual_summary.get_portfolio", return_value={"holdings": []}):
                    from annual_summary import generate_annual_summary
                    result = generate_annual_summary(year=2024, profile=SAMPLE_PROFILE)

    assert result["donations"]["gift_aid_eligible"] is False


def test_generate_annual_summary_defaults_to_last_year():
    from datetime import datetime
    with patch("annual_summary.get_profile", return_value={}):
        with patch("annual_summary.get_transactions", return_value=[]):
            with patch("annual_summary.get_totals", return_value={}):
                with patch("annual_summary.get_portfolio", return_value={"holdings": []}):
                    from annual_summary import generate_annual_summary
                    result = generate_annual_summary()

    assert result["year"] == datetime.now().year - 1


# ── render_annual_summary_html ────────────────────────────────────────────────

def _make_summary(year=2024, claims=None):
    return {
        "year": year,
        "generated_at": f"{year}-12-31T23:59:00",
        "profile_name": "Max Mustermann",
        "locale": "de",
        "currency": "EUR",
        "income": {"gross": 42000.0, "net": 30000.0, "employer": "ACME GmbH", "type": "employed"},
        "claims": claims or [],
        "investments": {"total_value": 10700.0, "realized_gains": 200.0, "dividends": 50.0},
        "donations": {"total": 250.0, "gift_aid_eligible": False},
        "outstanding": [c for c in (claims or []) if c.get("status") in ("needs_evidence", "needs_input")],
        "notes": "",
    }


def test_html_contains_cover_info():
    from annual_summary import render_annual_summary_html

    html = render_annual_summary_html(_make_summary())

    assert "Annual Financial Summary" in html
    assert "2024" in html
    assert "Max Mustermann" in html
    assert "DE" in html or "de" in html.lower()
    assert "EUR" in html


def test_html_contains_income_section():
    from annual_summary import render_annual_summary_html

    html = render_annual_summary_html(_make_summary())

    assert "Income" in html
    assert "42" in html  # part of 42,000
    assert "ACME GmbH" in html


def test_html_contains_investment_section():
    from annual_summary import render_annual_summary_html

    html = render_annual_summary_html(_make_summary())

    assert "Investment" in html
    assert "10,700" in html or "10700" in html


def test_html_contains_donations_section():
    from annual_summary import render_annual_summary_html

    html = render_annual_summary_html(_make_summary())

    assert "Charitable" in html or "Donation" in html
    assert "250" in html


def test_html_contains_deductions_table():
    from annual_summary import render_annual_summary_html

    html = render_annual_summary_html(_make_summary(claims=SAMPLE_CLAIMS))

    assert "Home Office" in html
    assert "Professional Development" in html
    assert "<table" in html
    assert "<tr" in html


def test_html_contains_outstanding_section():
    from annual_summary import render_annual_summary_html

    html = render_annual_summary_html(_make_summary(claims=SAMPLE_CLAIMS))

    assert "Outstanding" in html
    assert "Professional Development" in html  # needs_evidence
    assert "Commute" in html  # needs_input


def test_html_contains_footer():
    from annual_summary import render_annual_summary_html

    html = render_annual_summary_html(_make_summary())

    assert "Finance Assistant" in html
    assert "verify all figures" in html.lower() or "verify" in html.lower()


def test_html_is_print_friendly():
    """HTML should include @media print CSS."""
    from annual_summary import render_annual_summary_html

    html = render_annual_summary_html(_make_summary())

    assert "@media print" in html
    assert "A4" in html
    assert "page-break" in html


def test_html_is_standalone():
    """Should start with DOCTYPE and have complete structure."""
    from annual_summary import render_annual_summary_html

    html = render_annual_summary_html(_make_summary())

    assert html.startswith("<!DOCTYPE html>")
    assert "<html" in html
    assert "<head>" in html
    assert "<body>" in html
    assert "</html>" in html


def test_html_status_badges():
    """Status badges should be rendered for claims."""
    from annual_summary import render_annual_summary_html

    html = render_annual_summary_html(_make_summary(claims=SAMPLE_CLAIMS))

    assert "Complete" in html or "complete" in html.lower()
    assert "Needs Evidence" in html or "needs_evidence" in html.lower()


# ── render_annual_summary_markdown ────────────────────────────────────────────

def test_markdown_contains_all_sections():
    from annual_summary import render_annual_summary_markdown

    md = render_annual_summary_markdown(_make_summary(claims=SAMPLE_CLAIMS))

    assert "# Annual Financial Summary" in md
    assert "## 2. Income Summary" in md
    assert "## 3. Deduction Claims" in md
    assert "## 4. Investment Summary" in md
    assert "## 5. Charitable Giving" in md


def test_markdown_contains_income_data():
    from annual_summary import render_annual_summary_markdown

    md = render_annual_summary_markdown(_make_summary())

    assert "42,000" in md or "42000" in md
    assert "ACME GmbH" in md


def test_markdown_contains_claims_table():
    from annual_summary import render_annual_summary_markdown

    md = render_annual_summary_markdown(_make_summary(claims=SAMPLE_CLAIMS))

    assert "Home Office" in md
    assert "|" in md  # markdown table
    assert "needs evidence" in md.lower()


def test_markdown_contains_outstanding_section():
    from annual_summary import render_annual_summary_markdown

    md = render_annual_summary_markdown(_make_summary(claims=SAMPLE_CLAIMS))

    assert "## 6. Outstanding Items" in md
    assert "Professional Development" in md
    assert "Commute" in md


def test_markdown_no_claims_shows_placeholder():
    from annual_summary import render_annual_summary_markdown

    md = render_annual_summary_markdown(_make_summary(claims=[]))

    assert "No claims recorded" in md


def test_markdown_contains_footer_note():
    from annual_summary import render_annual_summary_markdown

    md = render_annual_summary_markdown(_make_summary())

    assert "Finance Assistant" in md
    assert "verify" in md.lower()


def test_markdown_gift_aid_uk():
    """Gift Aid note should appear for UK locale."""
    summary = _make_summary()
    summary["donations"]["gift_aid_eligible"] = True

    from annual_summary import render_annual_summary_markdown

    md = render_annual_summary_markdown(summary)
    assert "Gift Aid" in md


# ── save_annual_summary ───────────────────────────────────────────────────────

def test_save_annual_summary_creates_files():
    with patch("annual_summary.get_profile", return_value=SAMPLE_PROFILE):
        with patch("annual_summary.get_transactions", return_value=[]):
            with patch("annual_summary.get_totals", return_value={}):
                with patch("annual_summary.get_portfolio", return_value={"holdings": []}):
                    from annual_summary import save_annual_summary
                    result = save_annual_summary(year=2024)

    assert "html_path" in result
    assert "markdown_path" in result
    assert os.path.isfile(result["html_path"]), "HTML file should exist"
    assert os.path.isfile(result["markdown_path"]), "Markdown file should exist"


def test_save_annual_summary_html_content():
    with patch("annual_summary.get_profile", return_value=SAMPLE_PROFILE):
        with patch("annual_summary.get_transactions", return_value=[]):
            with patch("annual_summary.get_totals", return_value={}):
                with patch("annual_summary.get_portfolio", return_value={"holdings": []}):
                    from annual_summary import save_annual_summary
                    result = save_annual_summary(year=2024)

    html = open(result["html_path"], encoding="utf-8").read()
    assert "<!DOCTYPE html>" in html
    assert "2024" in html


def test_save_annual_summary_markdown_content():
    with patch("annual_summary.get_profile", return_value=SAMPLE_PROFILE):
        with patch("annual_summary.get_transactions", return_value=[]):
            with patch("annual_summary.get_totals", return_value={}):
                with patch("annual_summary.get_portfolio", return_value={"holdings": []}):
                    from annual_summary import save_annual_summary
                    result = save_annual_summary(year=2024)

    md = open(result["markdown_path"], encoding="utf-8").read()
    assert "# Annual Financial Summary" in md


def test_save_annual_summary_filename_contains_year():
    with patch("annual_summary.get_profile", return_value=SAMPLE_PROFILE):
        with patch("annual_summary.get_transactions", return_value=[]):
            with patch("annual_summary.get_totals", return_value={}):
                with patch("annual_summary.get_portfolio", return_value={"holdings": []}):
                    from annual_summary import save_annual_summary
                    result = save_annual_summary(year=2023)

    assert "2023" in result["html_path"]
    assert "2023" in result["markdown_path"]


# ── _status_badge_html ────────────────────────────────────────────────────────

def test_status_badge_html_complete():
    from annual_summary import _status_badge_html

    badge = _status_badge_html("complete")
    assert "Complete" in badge
    assert "span" in badge
    # Complete is green-ish
    assert "#155724" in badge or "d4edda" in badge


def test_status_badge_html_needs_evidence():
    from annual_summary import _status_badge_html

    badge = _status_badge_html("needs_evidence")
    assert "Needs Evidence" in badge
    # Warning amber color
    assert "#856404" in badge or "fff3cd" in badge


def test_status_badge_html_unknown():
    from annual_summary import _status_badge_html

    badge = _status_badge_html("unknown_status")
    assert "span" in badge
    assert "Unknown Status" in badge
