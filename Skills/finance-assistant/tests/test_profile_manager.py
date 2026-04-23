"""Tests for profile_manager.py."""
from profile_manager import (
    get_profile, update_profile, delete_profile, display_profile,
    add_child, add_filing_year,
    get_missing_fields, get_profile_completeness_pct,
    get_locale, get_primary_currency, set_locale,
)


def test_empty_profile(isolated_finance_dir):
    assert get_profile() == {}


def test_create_and_read_profile(isolated_finance_dir, sample_profile):
    update_profile(sample_profile)
    p = get_profile()
    assert p["personal"]["name"] == "Max Mustermann"
    assert p["employment"]["annual_gross"] == 65000
    assert p["meta"]["created"] is not None


def test_deep_merge(isolated_finance_dir, sample_profile):
    update_profile(sample_profile)
    update_profile({"employment": {"side_income": 5000}})
    p = get_profile()
    assert p["employment"]["annual_gross"] == 65000  # preserved
    assert p["employment"]["side_income"] == 5000     # added


def test_delete_profile(isolated_finance_dir, sample_profile):
    update_profile(sample_profile)
    assert delete_profile() is True
    assert get_profile() == {}
    assert delete_profile() is False


def test_add_child(isolated_finance_dir, sample_profile):
    update_profile(sample_profile)
    add_child({"birth_year": 2022, "name": "Lena"})
    p = get_profile()
    assert len(p["family"]["children"]) == 1
    assert p["family"]["children"][0]["birth_year"] == 2022


def test_add_filing_year(isolated_finance_dir, sample_profile):
    update_profile(sample_profile)
    add_filing_year({"year": 2025, "refund": 1200, "filed_via": "ELSTER"})
    p = get_profile()
    assert len(p["filing_history"]) == 1
    assert p["filing_history"][0]["refund"] == 1200


def test_display_profile(isolated_finance_dir, sample_profile):
    update_profile(sample_profile)
    display = display_profile()
    assert "Max Mustermann" in display
    assert "Berlin" in display


def test_missing_fields(isolated_finance_dir):
    update_profile({"meta": {"primary_currency": "EUR"}, "employment": {"annual_gross": 65000}})
    missing = get_missing_fields()
    assert "personal.country" in missing
    assert "employment.annual_gross" not in missing


def test_completeness(isolated_finance_dir, sample_profile):
    update_profile(sample_profile)
    pct = get_profile_completeness_pct()
    assert pct > 50


def test_locale_helpers(isolated_finance_dir, sample_profile):
    update_profile(sample_profile)
    assert get_locale() == "de"
    assert get_primary_currency() == "EUR"
    set_locale("pl")
    assert get_locale() == "pl"
