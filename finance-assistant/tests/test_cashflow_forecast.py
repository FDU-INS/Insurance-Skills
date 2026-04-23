"""
Tests for cashflow_forecast.py.

Uses mocked account_manager, recurring_engine, and transaction_logger
so no filesystem state is required.
"""

import os
import sys
import pytest
from datetime import date, timedelta
from unittest.mock import patch, MagicMock

# Ensure scripts/ is on the path
scripts_dir = os.path.join(os.path.dirname(__file__), "..", "scripts")
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)


# ── Helpers ────────────────────────────────────────────────────────────────────

def _make_account(balance: float = 1000.0, currency: str = "EUR") -> dict:
    return {
        "id": "test-checking",
        "name": "Test Checking",
        "type": "checking",
        "currency": currency,
        "current_balance": balance,
        "is_asset": True,
    }


def _make_recurring_event(name: str, amount: float, due_date: str) -> dict:
    return {
        "name": name,
        "amount": amount,
        "category": "housing",
        "due_date": due_date,
        "account_id": "test-checking",
    }


# ── forecast() ────────────────────────────────────────────────────────────────

def test_forecast_no_account():
    with patch("cashflow_forecast.get_account", return_value=None):
        with patch("cashflow_forecast.get_upcoming", return_value=[]):
            with patch("cashflow_forecast.get_transactions", return_value=[]):
                from cashflow_forecast import forecast
                result = forecast("nonexistent-account", days=10)

    assert "error" in result
    assert result["forecast"] == []
    assert result["low_balance_warnings"] == []


def test_forecast_stable_balance_no_spend():
    """With no spend and no recurring events, balance should be stable."""
    account = _make_account(balance=2000.0)

    with patch("cashflow_forecast.get_account", return_value=account):
        with patch("cashflow_forecast.get_upcoming", return_value=[]):
            with patch("cashflow_forecast.get_transactions", return_value=[]):
                from cashflow_forecast import forecast
                result = forecast("test-checking", days=30)

    assert result["current_balance"] == 2000.0
    assert len(result["forecast"]) == 30
    # All balances should be exactly 2000 (no spend)
    for day in result["forecast"]:
        assert day["balance"] == 2000.0
    assert result["low_balance_warnings"] == []
    assert result["summary"]["min_balance"] == 2000.0
    assert result["summary"]["end_balance"] == 2000.0


def test_forecast_with_recurring_rent():
    """Rent deduction should appear on the correct date."""
    account = _make_account(balance=1500.0)
    today = date.today()
    # Place rent 5 days from now
    rent_date = (today + timedelta(days=5)).isoformat()

    recurring = [_make_recurring_event("Rent", -800.0, rent_date)]

    with patch("cashflow_forecast.get_account", return_value=account):
        with patch("cashflow_forecast.get_upcoming", return_value=recurring):
            with patch("cashflow_forecast.get_transactions", return_value=[]):
                from cashflow_forecast import forecast
                result = forecast("test-checking", days=30)

    # Find day 5 in forecast
    rent_day = next(d for d in result["forecast"] if d["date"] == rent_date)
    assert len(rent_day["events"]) == 1
    assert rent_day["events"][0]["amount"] == -800.0

    # Balance on that day should have dropped by 800
    # (day before = 1500, day of rent = 700)
    assert rent_day["balance"] == pytest.approx(700.0, abs=5.0)


def test_forecast_low_balance_warning():
    """Balance dropping below threshold should trigger a warning."""
    # Start with 300, rent of 200 due in 3 days → should dip below 200
    account = _make_account(balance=300.0)
    today = date.today()
    rent_date = (today + timedelta(days=3)).isoformat()

    recurring = [_make_recurring_event("Subscription", -150.0, rent_date)]

    with patch("cashflow_forecast.get_account", return_value=account):
        with patch("cashflow_forecast.get_upcoming", return_value=recurring):
            with patch("cashflow_forecast.get_transactions", return_value=[]):
                from cashflow_forecast import forecast
                result = forecast("test-checking", days=30)

    assert len(result["low_balance_warnings"]) >= 1
    warning = result["low_balance_warnings"][0]
    assert warning["projected_balance"] < 200.0
    assert "date" in warning
    assert "threshold" in warning


def test_forecast_returns_correct_structure():
    """Result dict has all required keys."""
    account = _make_account(balance=500.0)

    with patch("cashflow_forecast.get_account", return_value=account):
        with patch("cashflow_forecast.get_upcoming", return_value=[]):
            with patch("cashflow_forecast.get_transactions", return_value=[]):
                from cashflow_forecast import forecast
                result = forecast("test-checking", days=7)

    assert "account_id" in result
    assert "current_balance" in result
    assert "forecast" in result
    assert "low_balance_warnings" in result
    assert "summary" in result
    assert "min_balance" in result["summary"]
    assert "min_balance_date" in result["summary"]
    assert "end_balance" in result["summary"]
    assert len(result["forecast"]) == 7


def test_forecast_summary_tracks_minimum():
    """Summary min_balance should track the actual minimum."""
    account = _make_account(balance=1000.0)
    today = date.today()
    dip_date = (today + timedelta(days=5)).isoformat()
    recover_date = (today + timedelta(days=10)).isoformat()

    recurring = [
        _make_recurring_event("Big Bill", -900.0, dip_date),
        _make_recurring_event("Income", +1000.0, recover_date),
    ]

    with patch("cashflow_forecast.get_account", return_value=account):
        with patch("cashflow_forecast.get_upcoming", return_value=recurring):
            with patch("cashflow_forecast.get_transactions", return_value=[]):
                from cashflow_forecast import forecast
                result = forecast("test-checking", days=15)

    assert result["summary"]["min_balance"] == pytest.approx(100.0, abs=5.0)
    assert result["summary"]["min_balance_date"] == dip_date
    assert result["summary"]["end_balance"] > result["summary"]["min_balance"]


# ── format_forecast() ─────────────────────────────────────────────────────────

def test_format_forecast_sparkline():
    account = _make_account(balance=1000.0)
    today = date.today()
    dip = (today + timedelta(days=15)).isoformat()
    recurring = [_make_recurring_event("Rent", -800.0, dip)]

    with patch("cashflow_forecast.get_account", return_value=account):
        with patch("cashflow_forecast.get_upcoming", return_value=recurring):
            with patch("cashflow_forecast.get_transactions", return_value=[]):
                from cashflow_forecast import forecast, format_forecast
                result = forecast("test-checking", days=30)
                text = format_forecast(result, sparkline=True)

    assert "Balance forecast" in text
    # Check sparkline chars are present
    sparkline_chars = set("▁▂▃▄▅▆▇█")
    assert any(c in text for c in sparkline_chars), "Sparkline should be present"


def test_format_forecast_no_sparkline():
    account = _make_account(balance=500.0)

    with patch("cashflow_forecast.get_account", return_value=account):
        with patch("cashflow_forecast.get_upcoming", return_value=[]):
            with patch("cashflow_forecast.get_transactions", return_value=[]):
                from cashflow_forecast import forecast, format_forecast
                result = forecast("test-checking", days=10)
                text = format_forecast(result, sparkline=False)

    assert "Balance forecast" in text
    sparkline_chars = set("▁▂▃▄▅▆▇█")
    assert not any(c in text for c in sparkline_chars), "No sparkline expected"


def test_format_forecast_shows_warning():
    account = _make_account(balance=250.0)
    today = date.today()
    dip = (today + timedelta(days=3)).isoformat()
    recurring = [_make_recurring_event("Bill", -100.0, dip)]

    with patch("cashflow_forecast.get_account", return_value=account):
        with patch("cashflow_forecast.get_upcoming", return_value=recurring):
            with patch("cashflow_forecast.get_transactions", return_value=[]):
                from cashflow_forecast import forecast, format_forecast
                result = forecast("test-checking", days=30)
                text = format_forecast(result)

    assert "[!]" in text or "Low balance" in text


def test_format_forecast_error():
    from cashflow_forecast import format_forecast
    result = {"error": "Account not found"}
    text = format_forecast(result)
    assert "error" in text.lower()


def test_format_forecast_min_and_end_shown():
    account = _make_account(balance=1000.0)

    with patch("cashflow_forecast.get_account", return_value=account):
        with patch("cashflow_forecast.get_upcoming", return_value=[]):
            with patch("cashflow_forecast.get_transactions", return_value=[]):
                from cashflow_forecast import forecast, format_forecast
                result = forecast("test-checking", days=7)
                text = format_forecast(result)

    assert "Min:" in text
    assert "End:" in text


# ── Daily spend calculation ────────────────────────────────────────────────────

def test_avg_daily_spend_empty_history():
    with patch("cashflow_forecast.get_transactions", return_value=[]):
        from cashflow_forecast import _avg_daily_spend
        result = _avg_daily_spend("test-checking")
    # No transactions → zero spend
    assert result == 0.0


def test_avg_daily_spend_with_expenses():
    # get_transactions is called once per month (3 months).
    # Each call returns the same list: 80 expense + 100 income.
    # Total expense = 80 * 3 = 240 over 90 days → ~2.67/day
    txns = [
        {"amount": -30.0, "type": "expense"},
        {"amount": -50.0, "type": "expense"},
        {"amount": 100.0, "type": "income"},  # income not counted as spend
    ]
    with patch("cashflow_forecast.get_transactions", return_value=txns):
        from cashflow_forecast import _avg_daily_spend
        result = _avg_daily_spend("test-checking")
    assert result < 0  # should be negative (outflow)
    # 80 expense per month × 3 months / 90 days = 80/30 per day ≈ 2.67
    assert abs(result) == pytest.approx(80 * 3 / 90, abs=0.05)
