"""Tests for the German locale plugin."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from locales.de import (
    LOCALE_CODE, LOCALE_NAME, SUPPORTED_YEARS,
    get_tax_rules, calculate_tax, get_filing_deadlines,
    get_social_contributions, get_deduction_categories,
)
from locales.de.tax_rules import TAX_YEAR_RULES, calculate_income_tax, calculate_soli


def test_locale_metadata():
    assert LOCALE_CODE == "de"
    assert LOCALE_NAME == "Germany"
    assert 2024 in SUPPORTED_YEARS
    assert 2025 in SUPPORTED_YEARS
    assert 2026 in SUPPORTED_YEARS


def test_2026_ruerup_fixed():
    """The 2026 ruerup_max_single was None in TaxDE — verify it's fixed."""
    rules = TAX_YEAR_RULES[2026]
    assert rules["ruerup_max_single"] == 30784
    assert rules["ruerup_max_single"] is not None


def test_all_years_complete():
    """No None values in any year's critical parameters."""
    critical_keys = ["grundfreibetrag", "kindergeld_per_child", "riester_max",
                     "ruerup_max_single", "bav_4pct_bbg"]
    for year in SUPPORTED_YEARS:
        rules = TAX_YEAR_RULES[year]
        for key in critical_keys:
            assert rules[key] is not None, f"{year}.{key} is None"


def test_grundfreibetrag_progression():
    assert TAX_YEAR_RULES[2024]["grundfreibetrag"] < TAX_YEAR_RULES[2025]["grundfreibetrag"]
    assert TAX_YEAR_RULES[2025]["grundfreibetrag"] < TAX_YEAR_RULES[2026]["grundfreibetrag"]


def test_income_tax_zero_below_grundfreibetrag():
    for year in SUPPORTED_YEARS:
        grundfreibetrag = TAX_YEAR_RULES[year]["grundfreibetrag"]
        assert calculate_income_tax(grundfreibetrag, year) == 0.0
        assert calculate_income_tax(grundfreibetrag - 1, year) == 0.0


def test_income_tax_positive_above_grundfreibetrag():
    for year in SUPPORTED_YEARS:
        assert calculate_income_tax(50000, year) > 0


def test_soli_zero_below_threshold():
    for year in SUPPORTED_YEARS:
        threshold = TAX_YEAR_RULES[year]["soli_freigrenze_single"]
        assert calculate_soli(threshold, year) == 0.0


def test_calculate_tax_with_profile(isolated_finance_dir):
    from profile_manager import update_profile
    update_profile({
        "meta": {"tax_year": 2026, "locale": "de"},
        "employment": {"type": "employed", "annual_gross": 65000},
        "tax_profile": {"locale": "de", "tax_class": "I", "extra": {}},
        "family": {"status": "single"},
        "housing": {"homeoffice_days_per_week": 3, "commute_km": 15, "commute_days_per_year": 100},
        "current_year_receipts": [],
    })
    from profile_manager import get_profile
    result = calculate_tax(get_profile(), 2026)
    assert result["estimated_refund"] is not None
    assert result["confidence_pct"] > 0


def test_filing_deadlines():
    deadlines = get_filing_deadlines(2026)
    assert len(deadlines) == 2
    assert any("2027" in d["deadline"] for d in deadlines)


def test_social_contributions():
    social = get_social_contributions(65000, 2026)
    assert social["total"] > 0
    assert social["pension"] > 0
    assert social["health"] > 0


def test_deduction_categories():
    cats = get_deduction_categories()
    ids = [c["id"] for c in cats]
    assert "homeoffice" in ids
    assert "commute" in ids
    assert "childcare" in ids
