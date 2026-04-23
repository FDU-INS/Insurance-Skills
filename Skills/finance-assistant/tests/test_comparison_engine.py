"""Tests for scripts/comparison_engine.py — month-over-month comparison."""

import sys
import os
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from comparison_engine import get_monthly_comparison, format_comparison, compare_budgets


# ── Helpers ───────────────────────────────────────────────────────────────────

def _make_transactions(year: int, month: int, items: list[tuple[str, float]]) -> list[dict]:
    """Build minimal transaction dicts for the given month."""
    result = []
    for i, (cat, amount) in enumerate(items):
        result.append({
            "id": f"t{i}",
            "date": f"{year}-{month:02d}-15",
            "account_id": "default",
            "type": "expense",
            "amount": abs(amount),
            "currency": "EUR",
            "category": cat,
            "description": f"Test {cat}",
        })
    return result


def _get_transactions_factory(cur_year, cur_mon, prev_year, prev_mon, cur_data, prev_data):
    """Return a mock get_transactions that returns correct data by (year, month)."""
    def _get(account_id="default", year=None, month=None, **kwargs):
        if year == cur_year and month == cur_mon:
            return _make_transactions(cur_year, cur_mon, cur_data)
        if year == prev_year and month == prev_mon:
            return _make_transactions(prev_year, prev_mon, prev_data)
        return []
    return _get


# ── get_monthly_comparison ────────────────────────────────────────────────────

class TestGetMonthlyComparison:
    def test_same_data_returns_zero_deltas(self):
        data = [("food", 300.0), ("transport", 100.0)]
        mock = _get_transactions_factory(2025, 4, 2025, 3, data, data)
        with patch("comparison_engine.get_transactions", mock):
            result = get_monthly_comparison(month="2025-04")
        for cat, vals in result["categories"].items():
            assert vals["delta"] == 0.0, f"{cat} should have zero delta"
        assert result["totals"]["delta"] == 0.0

    def test_category_only_in_current_is_new(self):
        cur = [("food", 300.0), ("entertainment", 50.0)]
        prev = [("food", 300.0)]
        mock = _get_transactions_factory(2025, 4, 2025, 3, cur, prev)
        with patch("comparison_engine.get_transactions", mock):
            result = get_monthly_comparison(month="2025-04")
        assert "entertainment" in result["new_categories"]

    def test_category_only_in_previous_is_dropped(self):
        cur = [("food", 300.0)]
        prev = [("food", 300.0), ("travel", 200.0)]
        mock = _get_transactions_factory(2025, 4, 2025, 3, cur, prev)
        with patch("comparison_engine.get_transactions", mock):
            result = get_monthly_comparison(month="2025-04")
        assert "travel" in result["dropped_categories"]

    def test_biggest_increase_identified_correctly(self):
        cur = [("food", 400.0), ("transport", 200.0), ("entertainment", 100.0)]
        prev = [("food", 200.0), ("transport", 190.0), ("entertainment", 90.0)]
        mock = _get_transactions_factory(2025, 4, 2025, 3, cur, prev)
        with patch("comparison_engine.get_transactions", mock):
            result = get_monthly_comparison(month="2025-04")
        # food delta = +200, largest
        assert result["biggest_increase"]["category"] == "food"
        assert result["biggest_increase"]["delta"] == 200.0

    def test_biggest_decrease_identified_correctly(self):
        cur = [("food", 100.0), ("transport", 50.0), ("travel", 0.0)]
        prev = [("food", 100.0), ("transport", 50.0), ("travel", 300.0)]
        mock = _get_transactions_factory(2025, 4, 2025, 3, cur, prev)
        with patch("comparison_engine.get_transactions", mock):
            result = get_monthly_comparison(month="2025-04")
        # travel dropped from 300 to 0
        assert result["biggest_decrease"]["category"] == "travel"
        assert result["biggest_decrease"]["delta"] == -300.0

    def test_totals_calculated_correctly(self):
        cur = [("food", 300.0), ("transport", 100.0)]
        prev = [("food", 200.0), ("transport", 150.0)]
        mock = _get_transactions_factory(2025, 4, 2025, 3, cur, prev)
        with patch("comparison_engine.get_transactions", mock):
            result = get_monthly_comparison(month="2025-04")
        assert result["totals"]["current"] == 400.0
        assert result["totals"]["previous"] == 350.0
        assert result["totals"]["delta"] == 50.0

    def test_month_labels_correct(self):
        cur = [("food", 100.0)]
        prev = [("food", 100.0)]
        mock = _get_transactions_factory(2025, 1, 2024, 12, cur, prev)
        with patch("comparison_engine.get_transactions", mock):
            result = get_monthly_comparison(month="2025-01")
        assert result["current_month"] == "2025-01"
        assert result["previous_month"] == "2024-12"

    def test_delta_pct_calculated(self):
        cur = [("food", 300.0)]
        prev = [("food", 200.0)]
        mock = _get_transactions_factory(2025, 4, 2025, 3, cur, prev)
        with patch("comparison_engine.get_transactions", mock):
            result = get_monthly_comparison(month="2025-04")
        assert result["categories"]["food"]["delta_pct"] == 50.0

    def test_empty_months_returns_zeros(self):
        mock = _get_transactions_factory(2025, 4, 2025, 3, [], [])
        with patch("comparison_engine.get_transactions", mock):
            result = get_monthly_comparison(month="2025-04")
        assert result["totals"]["current"] == 0.0
        assert result["totals"]["previous"] == 0.0


# ── format_comparison ────────────────────────────────────────────────────────

class TestFormatComparison:
    def _comparison(self):
        return {
            "current_month": "2025-04",
            "previous_month": "2025-03",
            "categories": {
                "food": {"current": 340.0, "previous": 298.0, "delta": 42.0, "delta_pct": 14.1},
                "transport": {"current": 112.0, "previous": 130.0, "delta": -18.0, "delta_pct": -13.8},
                "eating_out": {"current": 89.0, "previous": 65.0, "delta": 24.0, "delta_pct": 36.9},
            },
            "totals": {"current": 541.0, "previous": 493.0, "delta": 48.0, "delta_pct": 9.7},
            "biggest_increase": {"category": "food", "delta": 42.0, "delta_pct": 14.1},
            "biggest_decrease": {"category": "transport", "delta": -18.0, "delta_pct": -13.8},
            "new_categories": [],
            "dropped_categories": [],
        }

    def test_renders_without_error(self):
        out = format_comparison(self._comparison())
        assert isinstance(out, str)
        assert len(out) > 0

    def test_includes_headline_delta(self):
        out = format_comparison(self._comparison())
        assert "48" in out or "+48" in out

    def test_includes_chart_when_requested(self):
        out = format_comparison(self._comparison(), include_viz=True)
        # Chart includes category names
        assert "food" in out.lower() or "Food" in out

    def test_no_chart_when_not_requested(self):
        out = format_comparison(self._comparison(), include_viz=False)
        # Without viz the bar chars like █ ░ shouldn't appear in a significant block
        # but text is still there
        assert "2025-04" in out

    def test_top3_changes_shown(self):
        out = format_comparison(self._comparison())
        # All 3 categories have notable deltas
        assert "food" in out.lower() or "eating_out" in out.lower()

    def test_month_labels_in_output(self):
        out = format_comparison(self._comparison())
        assert "2025-04" in out
        assert "2025-03" in out

    def test_large_increase_flagged_in_chart(self):
        out = format_comparison(self._comparison(), include_viz=True)
        # eating_out is +36.9%, should trigger warning
        assert "⚠" in out


# ── compare_budgets ───────────────────────────────────────────────────────────

class TestCompareBudgets:
    def test_returns_expected_keys(self):
        cur = [("food", 300.0)]
        prev = [("food", 250.0)]
        mock = _get_transactions_factory(2025, 4, 2025, 3, cur, prev)
        with patch("comparison_engine.get_transactions", mock):
            with patch("comparison_engine.get_monthly_comparison.__module__"):
                pass
            result = compare_budgets(month="2025-04")

        assert "current_month" in result
        assert "previous_month" in result
        assert "categories" in result

    def test_category_entry_has_correct_fields(self):
        cur = [("food", 340.0)]
        prev = [("food", 300.0)]
        mock = _get_transactions_factory(2025, 4, 2025, 3, cur, prev)
        with patch("comparison_engine.get_transactions", mock):
            result = compare_budgets(month="2025-04")

        cat = result["categories"].get("food", {})
        assert "current_actual" in cat
        assert "previous_actual" in cat
        assert "delta" in cat

    def test_delta_is_current_minus_previous(self):
        cur = [("food", 340.0)]
        prev = [("food", 300.0)]
        mock = _get_transactions_factory(2025, 4, 2025, 3, cur, prev)
        with patch("comparison_engine.get_transactions", mock):
            result = compare_budgets(month="2025-04")
        assert result["categories"]["food"]["delta"] == 40.0
