"""Tests for scripts/scenario_store.py — save/recall named scenarios."""

from __future__ import annotations

import json
import os
import time
from pathlib import Path

import pytest


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture(autouse=True)
def isolated_finance_dir(tmp_path, monkeypatch):
    """Each test gets a fresh .finance/ directory."""
    monkeypatch.setenv("FINANCE_PROJECT_DIR", str(tmp_path))
    yield tmp_path


@pytest.fixture()
def store():
    import importlib
    import scripts.scenario_store as m
    importlib.reload(m)
    return m


# ── Helpers ───────────────────────────────────────────────────────────────────

def _sample_inputs():
    return {"current_savings": 50_000, "monthly_contribution": 800, "annual_expenses": 30_000}


def _sample_result():
    return {"fire_number": 750_000, "years_to_fire": 18.5, "achievable": True}


def _sample_profile():
    return {"net_worth": 55_000, "portfolio_value": 50_000, "debt_total": 5_000}


# ── Tests ─────────────────────────────────────────────────────────────────────

class TestSaveLoad:
    def test_save_returns_record(self, store):
        record = store.save_scenario("My FIRE Plan", "fire_calc", _sample_inputs(), _sample_result())
        assert record["name"] == "My FIRE Plan"
        assert record["type"] == "fire_calc"
        assert record["slug"] == "my_fire_plan"
        assert "saved_at" in record
        assert record["inputs"]["current_savings"] == 50_000

    def test_roundtrip(self, store):
        store.save_scenario("My FIRE Plan", "fire_calc", _sample_inputs(), _sample_result())
        loaded = store.load_scenario("My FIRE Plan")
        assert loaded is not None
        assert loaded["result"]["years_to_fire"] == 18.5

    def test_load_by_slug(self, store):
        store.save_scenario("My FIRE Plan", "fire_calc", _sample_inputs(), _sample_result())
        loaded = store.load_scenario("my_fire_plan")
        assert loaded is not None
        assert loaded["name"] == "My FIRE Plan"

    def test_load_nonexistent_returns_none(self, store):
        assert store.load_scenario("nonexistent scenario xyz") is None

    def test_profile_snapshot_stored_with_key_metrics_only(self, store):
        full_profile = {**_sample_profile(), "full_name": "Alice", "iban": "DE123"}
        record = store.save_scenario(
            "test", "fire_calc", _sample_inputs(), _sample_result(),
            profile_snapshot=full_profile,
        )
        snap = record["profile_snapshot"]
        assert "net_worth" in snap
        assert "iban" not in snap
        assert "full_name" not in snap


class TestFuzzyMatch:
    def test_fuzzy_partial_slug(self, store):
        store.save_scenario("Retirement 2040", "fire_calc", _sample_inputs(), _sample_result())
        loaded = store.load_scenario("retirement")
        assert loaded is not None

    def test_slug_normalization(self, store):
        """Spaces, uppercase, special chars all normalise."""
        store.save_scenario("Q1 Budget Check!", "budget_check", {}, {})
        loaded = store.load_scenario("q1 budget check")
        assert loaded is not None

    def test_overwrite_same_name(self, store):
        store.save_scenario("Plan A", "fire_calc", {"x": 1}, {"y": 1})
        store.save_scenario("Plan A", "fire_calc", {"x": 2}, {"y": 2})
        loaded = store.load_scenario("Plan A")
        assert loaded["inputs"]["x"] == 2


class TestListScenarios:
    def test_list_returns_all(self, store):
        store.save_scenario("Plan A", "fire_calc", _sample_inputs(), _sample_result())
        store.save_scenario("Plan B", "debt_optimizer", {}, {})
        items = store.list_scenarios()
        names = [i["name"] for i in items]
        assert "Plan A" in names
        assert "Plan B" in names

    def test_list_sorted_by_saved_at(self, store):
        store.save_scenario("First", "fire_calc", {}, {})
        time.sleep(0.05)
        store.save_scenario("Second", "fire_calc", {}, {})
        items = store.list_scenarios()
        assert items[0]["name"] == "First"
        assert items[1]["name"] == "Second"

    def test_list_includes_required_fields(self, store):
        store.save_scenario("Plan A", "fire_calc", _sample_inputs(), _sample_result())
        items = store.list_scenarios()
        for item in items:
            assert "name" in item
            assert "type" in item
            assert "saved_at" in item
            assert "summary" in item

    def test_empty_list(self, store):
        assert store.list_scenarios() == []


class TestDelete:
    def test_delete_existing(self, store):
        store.save_scenario("Plan A", "fire_calc", {}, {})
        assert store.delete_scenario("Plan A") is True
        assert store.load_scenario("Plan A") is None

    def test_delete_nonexistent(self, store):
        assert store.delete_scenario("does not exist") is False

    def test_delete_removes_file(self, store, tmp_path):
        store.save_scenario("Plan A", "fire_calc", {}, {})
        scenarios_dir = tmp_path / ".finance" / "scenarios"
        assert any(scenarios_dir.glob("plan_a.json"))
        store.delete_scenario("Plan A")
        assert not any(scenarios_dir.glob("plan_a.json"))


class TestCompareScenarioToCurrent:
    def test_computes_net_worth_delta(self, store):
        snap = {"net_worth": 100_000, "portfolio_value": 90_000, "debt_total": 10_000}
        store.save_scenario("Baseline", "fire_calc", _sample_inputs(), _sample_result(),
                             profile_snapshot=snap)
        current = {"net_worth": 112_000, "portfolio_value": 105_000, "debt_total": 8_000}
        comparison = store.compare_scenario_to_current("Baseline", current)
        assert comparison is not None
        assert comparison["scenario_name"] == "Baseline"
        changes = comparison["changes_since_saved"]
        assert changes["net_worth_delta"] == pytest.approx(12_000.0)
        assert changes["portfolio_delta"] == pytest.approx(15_000.0)
        assert changes["debt_delta"] == pytest.approx(-2_000.0)

    def test_notes_describe_growth(self, store):
        snap = {"net_worth": 100_000}
        store.save_scenario("Baseline", "fire_calc", _sample_inputs(), _sample_result(),
                             profile_snapshot=snap)
        current = {"net_worth": 115_000}
        comparison = store.compare_scenario_to_current("Baseline", current)
        notes = comparison["changes_since_saved"]["notes"]
        assert any("net worth" in n.lower() for n in notes)
        assert any("grew" in n.lower() for n in notes)

    def test_original_result_preserved(self, store):
        store.save_scenario("Baseline", "fire_calc", _sample_inputs(), _sample_result())
        comparison = store.compare_scenario_to_current("Baseline", {})
        assert comparison["original_result"]["years_to_fire"] == 18.5

    def test_compare_nonexistent_returns_none(self, store):
        assert store.compare_scenario_to_current("no such scenario", {}) is None

    def test_days_ago_positive(self, store):
        store.save_scenario("Old Plan", "fire_calc", {}, {})
        comparison = store.compare_scenario_to_current("Old Plan", {})
        assert comparison["days_ago"] >= 0


class TestFormatScenarioList:
    def test_empty(self, store):
        output = store.format_scenario_list()
        assert "No saved scenarios" in output

    def test_lists_names_and_types(self, store):
        store.save_scenario("Retirement 2040", "fire_calc", _sample_inputs(), _sample_result())
        output = store.format_scenario_list()
        assert "Retirement 2040" in output
        assert "fire_calc" in output
