"""Tests for insurance_analyzer.py."""
from insurance_analyzer import (
    get_policies, add_policy, update_policy, delete_policy,
    analyze_coverage, check_renewal_dates, calculate_total_premiums,
    format_insurance_display,
)


def test_empty_policies(isolated_finance_dir):
    assert get_policies() == []


def test_add_policy(isolated_finance_dir):
    p = add_policy({"type": "health", "provider": "TK", "annual_premium": 4800})
    assert p["type"] == "health"
    assert p["monthly_premium"] == 400.0  # auto-calculated


def test_coverage_gaps(isolated_finance_dir):
    add_policy({"type": "health", "provider": "TK", "annual_premium": 4800})
    coverage = analyze_coverage()
    gap_types = [g["type"] for g in coverage["gaps"]]
    assert "liability" in gap_types  # Missing essential
    assert "health" not in gap_types  # Covered


def test_coverage_with_dependents(isolated_finance_dir):
    coverage = analyze_coverage(has_dependents=True)
    gap_types = [g["type"] for g in coverage["gaps"]]
    assert "life" in gap_types  # Life insurance needed with dependents


def test_total_premiums(isolated_finance_dir):
    add_policy({"type": "health", "annual_premium": 4800})
    add_policy({"type": "liability", "annual_premium": 60})
    totals = calculate_total_premiums()
    assert totals["total_annual"] == 4860.0
    assert totals["policy_count"] == 2


def test_format_display(isolated_finance_dir):
    add_policy({"type": "health", "provider": "TK", "annual_premium": 4800})
    display = format_insurance_display()
    assert "TK" in display
