"""Tests for workspace_builder.py."""
from profile_manager import update_profile
from account_manager import add_account
from workspace_builder import build_workspace, format_workspace_display


def test_build_workspace_empty(isolated_finance_dir):
    update_profile({"meta": {"locale": "de"}, "employment": {"type": "employed"}})
    ws = build_workspace(persist=False)
    assert "financial_health_pct" in ws
    assert ws["financial_health_pct"] >= 0


def test_workspace_with_data(isolated_finance_dir):
    update_profile({
        "meta": {"locale": "de", "primary_currency": "EUR"},
        "employment": {"type": "employed", "annual_gross": 65000},
        "family": {"status": "single"},
    })
    add_account({"name": "Checking", "type": "checking", "current_balance": 5000})
    ws = build_workspace(persist=False)
    assert ws["net_worth"] > 0


def test_format_display(isolated_finance_dir):
    update_profile({"meta": {"locale": "de"}})
    ws = build_workspace(persist=False)
    display = format_workspace_display(ws)
    assert "Financial Health" in display
    assert "%" in display
