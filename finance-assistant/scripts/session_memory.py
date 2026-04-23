"""
Finance Assistant Session Memory — Lightweight in-session query store.

A module-level dict that lives only for the current conversation.
Not persisted to disk. Used to power "same as before", "repeat that",
"same parameters", and session summaries.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

# ── Module-level session state ────────────────────────────────────────────────

_session: dict = {
    "query_history": [],   # last 10 queries with type + key params
    "last_result": None,   # last computation result
    "context": {},         # named values set during session
}

_MAX_HISTORY = 10


# ── Public API ────────────────────────────────────────────────────────────────

def record_query(query_type: str, params: dict, result_summary: dict) -> None:
    """
    Record a query to session history. Keeps last 10.

    query_type: "budget_check", "fire_calc", "debt_optimizer", "scenario", etc.
    params: the key inputs used
    result_summary: key outputs (headline numbers only, not full result)
    """
    entry = {
        "query_type": query_type,
        "params": params,
        "result_summary": result_summary,
        "recorded_at": datetime.now().strftime("%H:%M"),
    }
    _session["query_history"].append(entry)
    if len(_session["query_history"]) > _MAX_HISTORY:
        _session["query_history"] = _session["query_history"][-_MAX_HISTORY:]
    _session["last_result"] = result_summary


def get_last_query(query_type: Optional[str] = None) -> Optional[dict]:
    """
    Get the most recent query, optionally filtered by type.

    Used for "same as before", "same parameters", "repeat that" etc.
    Returns None if no matching query exists.
    """
    history = _session["query_history"]
    if not history:
        return None
    if query_type is None:
        return history[-1]
    # Walk backwards to find the most recent matching type
    for entry in reversed(history):
        if entry.get("query_type") == query_type:
            return entry
    return None


def set_context(key: str, value: Any) -> None:
    """Set a named context value for the session (e.g., last_account_id)."""
    _session["context"][key] = value


def get_context(key: str, default: Any = None) -> Any:
    """Get a named context value."""
    return _session["context"].get(key, default)


def get_session_summary() -> str:
    """
    Plain-text summary of what's been done this session.

    Example:
        "This session: checked budget (14:23), ran FIRE calc (14:31), optimized debt (14:45)"
    """
    history = _session["query_history"]
    if not history:
        return "Nothing done yet this session."

    # Human-readable labels for query types
    _labels = {
        "budget_check": "checked budget",
        "fire_calc": "ran FIRE calc",
        "debt_optimizer": "optimized debt",
        "scenario": "ran scenario",
        "net_worth": "checked net worth",
        "goal_tracker": "reviewed goals",
        "investment_tracker": "reviewed portfolio",
        "tax_estimate": "estimated tax",
        "insurance_review": "reviewed insurance",
        "import": "imported data",
        "transaction_log": "logged transaction",
        "cashflow_forecast": "forecasted cash flow",
    }

    parts = []
    for entry in history:
        qtype = entry.get("query_type", "query")
        label = _labels.get(qtype, qtype.replace("_", " "))
        time = entry.get("recorded_at", "")
        parts.append(f"{label} ({time})" if time else label)

    return "This session: " + ", ".join(parts)


def clear_session() -> None:
    """Reset session state (called at session start by skill.py)."""
    _session["query_history"] = []
    _session["last_result"] = None
    _session["context"] = {}
