"""Tests for scripts/threshold_alerts.py — user-configured milestone tracking."""

from __future__ import annotations

import importlib

import pytest


@pytest.fixture(autouse=True)
def isolated_finance_dir(tmp_path, monkeypatch):
    monkeypatch.setenv("FINANCE_PROJECT_DIR", str(tmp_path))
    yield tmp_path


@pytest.fixture()
def ta():
    import scripts.threshold_alerts as m
    importlib.reload(m)
    return m


# ── set / get / delete ────────────────────────────────────────────────────────

class TestSetGetDelete:
    def test_set_returns_record(self, ta):
        rec = ta.set_threshold("net_worth", 200_000, "above", "€200k milestone")
        assert rec["metric"] == "net_worth"
        assert rec["value"] == 200_000.0
        assert rec["direction"] == "above"
        assert rec["label"] == "€200k milestone"

    def test_get_thresholds_returns_saved(self, ta):
        ta.set_threshold("net_worth", 200_000, "above")
        items = ta.get_thresholds()
        assert len(items) == 1
        assert items[0]["metric"] == "net_worth"

    def test_multiple_thresholds_stored(self, ta):
        ta.set_threshold("net_worth", 200_000, "above")
        ta.set_threshold("debt_total", 10_000, "below")
        items = ta.get_thresholds()
        metrics = {i["metric"] for i in items}
        assert "net_worth" in metrics
        assert "debt_total" in metrics

    def test_delete_existing(self, ta):
        ta.set_threshold("net_worth", 200_000, "above")
        assert ta.delete_threshold("net_worth", 200_000) is True
        assert ta.get_thresholds() == []

    def test_delete_nonexistent_returns_false(self, ta):
        assert ta.delete_threshold("net_worth", 999_999) is False

    def test_duplicate_same_metric_value_direction_replaced(self, ta):
        ta.set_threshold("net_worth", 200_000, "above", "first label")
        ta.set_threshold("net_worth", 200_000, "above", "second label")
        items = ta.get_thresholds()
        assert len([i for i in items if i["metric"] == "net_worth" and i["value"] == 200_000]) == 1
        assert items[-1]["label"] == "second label"

    def test_invalid_direction_raises(self, ta):
        with pytest.raises(ValueError):
            ta.set_threshold("net_worth", 200_000, "sideways")


# ── check_thresholds ──────────────────────────────────────────────────────────

class TestCheckThresholds:
    def test_above_triggered(self, ta):
        ta.set_threshold("net_worth", 200_000, "above", "€200k milestone")
        triggered = ta.check_thresholds({"net_worth": 203_450})
        assert len(triggered) == 1
        assert triggered[0]["metric"] == "net_worth"
        assert triggered[0]["current"] == 203_450.0

    def test_above_not_triggered_below(self, ta):
        ta.set_threshold("net_worth", 200_000, "above")
        triggered = ta.check_thresholds({"net_worth": 150_000})
        assert triggered == []

    def test_below_triggered(self, ta):
        ta.set_threshold("debt_total", 5_000, "below", "debt below €5k")
        triggered = ta.check_thresholds({"debt_total": 4_200})
        assert len(triggered) == 1
        assert triggered[0]["metric"] == "debt_total"

    def test_below_not_triggered_above(self, ta):
        ta.set_threshold("debt_total", 5_000, "below")
        triggered = ta.check_thresholds({"debt_total": 8_000})
        assert triggered == []

    def test_exact_threshold_value_triggers(self, ta):
        ta.set_threshold("net_worth", 200_000, "above")
        triggered = ta.check_thresholds({"net_worth": 200_000})
        assert len(triggered) == 1

    def test_missing_metric_not_triggered(self, ta):
        ta.set_threshold("portfolio_value", 100_000, "above")
        triggered = ta.check_thresholds({"net_worth": 250_000})
        assert triggered == []

    def test_multiple_triggered(self, ta):
        ta.set_threshold("net_worth", 200_000, "above")
        ta.set_threshold("debt_total", 5_000, "below")
        triggered = ta.check_thresholds({"net_worth": 210_000, "debt_total": 3_000})
        assert len(triggered) == 2


# ── format_threshold_alerts ───────────────────────────────────────────────────

class TestFormatThresholdAlerts:
    def test_empty_returns_empty_string(self, ta):
        assert ta.format_threshold_alerts([]) == ""

    def test_above_milestone_format(self, ta):
        triggered = [
            {"metric": "net_worth", "threshold": 200_000, "current": 203_450,
             "label": "€200k milestone", "direction": "above"}
        ]
        output = ta.format_threshold_alerts(triggered)
        assert "🎯" in output
        assert "€200k milestone" in output or "Net worth" in output
        assert "203,450" in output or "203450" in output

    def test_below_milestone_format(self, ta):
        triggered = [
            {"metric": "debt_total", "threshold": 5_000, "current": 3_200,
             "label": "debt below €5k", "direction": "below"}
        ]
        output = ta.format_threshold_alerts(triggered)
        assert "below" in output.lower() or "dropped" in output.lower()

    def test_savings_rate_format_uses_percent(self, ta):
        triggered = [
            {"metric": "savings_rate", "threshold": 20.0, "current": 22.5,
             "label": "20% savings rate", "direction": "above"}
        ]
        output = ta.format_threshold_alerts(triggered)
        assert "%" in output

    def test_multiple_alerts_multi_line(self, ta):
        triggered = [
            {"metric": "net_worth", "threshold": 200_000, "current": 210_000,
             "label": "NW milestone", "direction": "above"},
            {"metric": "debt_total", "threshold": 5_000, "current": 2_000,
             "label": "debt clear", "direction": "below"},
        ]
        output = ta.format_threshold_alerts(triggered)
        assert output.count("🎯") == 2
