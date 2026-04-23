"""Tests for goal_tracker.py."""
from goal_tracker import (
    get_goals, add_goal, update_goal, delete_goal,
    project_goal_completion, suggest_emergency_fund, format_goals_display,
)


def test_empty_goals(isolated_finance_dir):
    assert get_goals() == []


def test_add_goal(isolated_finance_dir):
    g = add_goal({"name": "Emergency Fund", "type": "emergency_fund",
                   "target_amount": 15000, "current_amount": 3000, "monthly_contribution": 500})
    assert g["name"] == "Emergency Fund"
    assert g["status"] == "active"


def test_update_goal(isolated_finance_dir):
    g = add_goal({"name": "Vacation", "target_amount": 3000})
    updated = update_goal(g["id"], {"current_amount": 1500})
    assert updated["current_amount"] == 1500


def test_delete_goal(isolated_finance_dir):
    g = add_goal({"name": "Test", "target_amount": 1000})
    assert delete_goal(g["id"]) is True
    assert len(get_goals()) == 0


def test_project_completion(isolated_finance_dir):
    g = add_goal({"name": "House", "target_amount": 50000,
                   "current_amount": 10000, "monthly_contribution": 1000})
    proj = project_goal_completion(g["id"])
    assert proj["months_to_go"] == 40.0
    assert proj["pct_complete"] == 20.0
    assert proj["status"] == "on_track"


def test_project_stalled(isolated_finance_dir):
    g = add_goal({"name": "Stalled", "target_amount": 5000, "current_amount": 1000})
    proj = project_goal_completion(g["id"])
    assert proj["status"] == "stalled"
    assert "suggestion" in proj


def test_suggest_emergency_fund():
    suggestion = suggest_emergency_fund(2500, months=6)
    assert suggestion["suggested_target"] == 15000.0
    assert suggestion["months_coverage"] == 6


def test_format_display(isolated_finance_dir):
    add_goal({"name": "Emergency", "type": "emergency_fund",
              "target_amount": 10000, "current_amount": 5000})
    display = format_goals_display()
    assert "Emergency" in display
    assert "50%" in display
