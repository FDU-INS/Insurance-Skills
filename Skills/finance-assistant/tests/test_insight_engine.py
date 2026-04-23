"""Tests for insight_engine.py."""
from profile_manager import update_profile
from insight_engine import generate_insights, format_insights_display


def test_generate_insights_empty(isolated_finance_dir):
    update_profile({"meta": {"locale": "de"}, "employment": {"type": "employed"}})
    result = generate_insights(persist=False)
    assert "insights" in result
    assert result["insight_count"] >= 0


def test_insights_detect_no_budget(isolated_finance_dir):
    update_profile({"meta": {"locale": "de"}})
    result = generate_insights(persist=False)
    ids = [i["id"] for i in result["insights"]]
    assert "no_budget" in ids


def test_insights_detect_no_goals(isolated_finance_dir):
    update_profile({"meta": {"locale": "de"}})
    result = generate_insights(persist=False)
    ids = [i["id"] for i in result["insights"]]
    assert "no_goals" in ids


def test_insights_sorted_by_status(isolated_finance_dir):
    update_profile({"meta": {"locale": "de"}})
    result = generate_insights(persist=False)
    statuses = [i["status"] for i in result["insights"]]
    status_order = {"ready": 0, "needs_evidence": 1, "needs_input": 2, "detected": 3}
    orders = [status_order.get(s, 9) for s in statuses]
    assert orders == sorted(orders)


def test_format_insights(isolated_finance_dir):
    update_profile({"meta": {"locale": "de"}})
    result = generate_insights(persist=False)
    display = format_insights_display(result)
    assert "Insights" in display or "insight" in display.lower()
