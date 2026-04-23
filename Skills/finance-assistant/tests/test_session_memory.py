"""Tests for scripts/session_memory.py — in-session query memory."""

from __future__ import annotations

import importlib

import pytest


@pytest.fixture()
def mem():
    """Fresh module state for each test."""
    import scripts.session_memory as m
    importlib.reload(m)
    return m


# ── record / retrieve ─────────────────────────────────────────────────────────

class TestRecordAndRetrieve:
    def test_record_single_query(self, mem):
        mem.record_query("budget_check", {"month": "2026-04"}, {"status": "ok"})
        last = mem.get_last_query()
        assert last is not None
        assert last["query_type"] == "budget_check"
        assert last["params"]["month"] == "2026-04"

    def test_last_result_updated(self, mem):
        mem.record_query("fire_calc", {}, {"years_to_fire": 15})
        assert mem._session["last_result"] == {"years_to_fire": 15}

    def test_recorded_at_present(self, mem):
        mem.record_query("budget_check", {}, {})
        last = mem.get_last_query()
        assert "recorded_at" in last
        assert ":" in last["recorded_at"]  # HH:MM format


class TestHistoryCap:
    def test_capped_at_10(self, mem):
        for i in range(15):
            mem.record_query(f"type_{i}", {}, {})
        assert len(mem._session["query_history"]) == 10

    def test_oldest_dropped(self, mem):
        for i in range(15):
            mem.record_query(f"type_{i}", {"i": i}, {})
        types = [e["query_type"] for e in mem._session["query_history"]]
        assert "type_0" not in types
        assert "type_14" in types


class TestGetLastQueryFiltered:
    def test_filter_by_type(self, mem):
        mem.record_query("budget_check", {"a": 1}, {})
        mem.record_query("fire_calc", {"b": 2}, {})
        mem.record_query("budget_check", {"a": 3}, {})
        last_budget = mem.get_last_query("budget_check")
        assert last_budget["params"]["a"] == 3

    def test_filter_returns_none_if_not_found(self, mem):
        mem.record_query("budget_check", {}, {})
        assert mem.get_last_query("fire_calc") is None

    def test_no_filter_returns_most_recent(self, mem):
        mem.record_query("budget_check", {}, {})
        mem.record_query("fire_calc", {"z": 99}, {})
        last = mem.get_last_query()
        assert last["query_type"] == "fire_calc"

    def test_empty_history_returns_none(self, mem):
        assert mem.get_last_query() is None


class TestContext:
    def test_set_and_get(self, mem):
        mem.set_context("last_account", "acc_123")
        assert mem.get_context("last_account") == "acc_123"

    def test_overwrite(self, mem):
        mem.set_context("last_account", "acc_1")
        mem.set_context("last_account", "acc_2")
        assert mem.get_context("last_account") == "acc_2"

    def test_default_returned_when_missing(self, mem):
        assert mem.get_context("nonexistent", default="fallback") == "fallback"

    def test_multiple_keys_independent(self, mem):
        mem.set_context("x", 1)
        mem.set_context("y", 2)
        assert mem.get_context("x") == 1
        assert mem.get_context("y") == 2


class TestSessionSummary:
    def test_contains_query_types(self, mem):
        mem.record_query("budget_check", {}, {})
        mem.record_query("fire_calc", {}, {})
        summary = mem.get_session_summary()
        assert "budget" in summary.lower()
        assert "fire" in summary.lower() or "FIRE" in summary

    def test_empty_session(self, mem):
        summary = mem.get_session_summary()
        assert "Nothing" in summary or "nothing" in summary or summary == "Nothing done yet this session."

    def test_includes_time(self, mem):
        mem.record_query("budget_check", {}, {})
        summary = mem.get_session_summary()
        # Time is HH:MM format surrounded by parens
        assert "(" in summary


class TestClear:
    def test_clear_resets_history(self, mem):
        mem.record_query("budget_check", {}, {})
        mem.clear_session()
        assert mem._session["query_history"] == []

    def test_clear_resets_last_result(self, mem):
        mem.record_query("fire_calc", {}, {"x": 1})
        mem.clear_session()
        assert mem._session["last_result"] is None

    def test_clear_resets_context(self, mem):
        mem.set_context("k", "v")
        mem.clear_session()
        assert mem._session["context"] == {}

    def test_clear_allows_new_records(self, mem):
        mem.record_query("fire_calc", {}, {})
        mem.clear_session()
        mem.record_query("budget_check", {}, {})
        assert len(mem._session["query_history"]) == 1
