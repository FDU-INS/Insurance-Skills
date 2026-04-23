"""
Finance Assistant Threshold Alerts — User-configured milestone tracking.

Users set numeric thresholds (e.g. "net worth > €200k") and get proactive
alerts when those milestones are crossed during a session.

Storage: .finance/thresholds.json
"""

from __future__ import annotations

import os
from typing import Optional

try:
    from finance_storage import get_finance_dir, ensure_finance_dir, load_json, save_json
except ImportError:
    import sys
    sys.path.insert(0, os.path.dirname(__file__))
    from finance_storage import get_finance_dir, ensure_finance_dir, load_json, save_json


# ── Storage helpers ───────────────────────────────────────────────────────────

def _thresholds_path():
    ensure_finance_dir()
    return get_finance_dir() / "thresholds.json"


def _load_all() -> list[dict]:
    data = load_json(_thresholds_path(), default={})
    return data.get("thresholds", [])


def _save_all(thresholds: list[dict]) -> None:
    save_json(_thresholds_path(), {"thresholds": thresholds})


# ── Public API ────────────────────────────────────────────────────────────────

VALID_METRICS = {
    "net_worth", "portfolio_value", "debt_total", "savings_rate",
    "emergency_fund_months", "fire_pct",
}


def set_threshold(
    metric: str,
    value: float,
    direction: str = "above",
    label: Optional[str] = None,
) -> dict:
    """
    Set a milestone threshold. Saved to .finance/thresholds.json.

    metric: "net_worth", "portfolio_value", "debt_total", "savings_rate",
            "emergency_fund_months", "fire_pct", "budget_category_{name}"
    direction: "above" (alert when value crosses above) or "below" (crosses below)
    label: optional friendly name e.g. "€200k net worth milestone"

    Example: set_threshold("net_worth", 200_000, "above", "€200k milestone")
    """
    if direction not in ("above", "below"):
        raise ValueError(f"direction must be 'above' or 'below', got {direction!r}")

    record: dict = {
        "metric": metric,
        "value": float(value),
        "direction": direction,
        "label": label or f"{metric} {direction} {value:,.0f}",
    }

    thresholds = _load_all()
    # Replace if exact metric+value+direction already exists
    thresholds = [
        t for t in thresholds
        if not (t["metric"] == metric and t["value"] == record["value"]
                and t["direction"] == direction)
    ]
    thresholds.append(record)
    _save_all(thresholds)
    return record


def get_thresholds() -> list[dict]:
    """Load all configured thresholds."""
    return _load_all()


def delete_threshold(metric: str, value: float) -> bool:
    """Remove a threshold by metric + value. Returns True if removed."""
    thresholds = _load_all()
    original_len = len(thresholds)
    thresholds = [
        t for t in thresholds
        if not (t["metric"] == metric and t["value"] == float(value))
    ]
    if len(thresholds) < original_len:
        _save_all(thresholds)
        return True
    return False


def check_thresholds(current_metrics: dict) -> list[dict]:
    """
    Check all thresholds against current metrics.

    current_metrics = {"net_worth": float, "portfolio_value": float, ...}

    Returns list of triggered thresholds:
    [{"metric": str, "threshold": float, "current": float, "label": str, "direction": str}]
    """
    triggered = []
    for t in _load_all():
        metric = t["metric"]
        threshold_val = float(t["value"])
        direction = t["direction"]

        current_val = current_metrics.get(metric)
        if current_val is None:
            continue
        current_val = float(current_val)

        hit = (
            (direction == "above" and current_val >= threshold_val) or
            (direction == "below" and current_val <= threshold_val)
        )
        if hit:
            triggered.append({
                "metric": metric,
                "threshold": threshold_val,
                "current": current_val,
                "label": t.get("label", metric),
                "direction": direction,
            })
    return triggered


def format_threshold_alerts(triggered: list) -> str:
    """
    Format triggered thresholds for session alerts.

    Example output:
        🎯 Milestone reached: Net worth crossed €200k (now €203,450)
    """
    if not triggered:
        return ""

    _metric_labels = {
        "net_worth": "Net worth",
        "portfolio_value": "Portfolio value",
        "debt_total": "Total debt",
        "savings_rate": "Savings rate",
        "emergency_fund_months": "Emergency fund",
        "fire_pct": "FIRE progress",
    }

    lines = []
    for item in triggered:
        metric = item["metric"]
        label = item.get("label") or _metric_labels.get(metric, metric)
        direction = item["direction"]
        threshold = item["threshold"]
        current = item["current"]

        if metric in ("savings_rate", "fire_pct"):
            fmt_threshold = f"{threshold:.1f}%"
            fmt_current = f"{current:.1f}%"
        elif metric == "emergency_fund_months":
            fmt_threshold = f"{threshold:.1f} months"
            fmt_current = f"{current:.1f} months"
        else:
            fmt_threshold = f"€{threshold:,.0f}"
            fmt_current = f"€{current:,.0f}"

        verb = "crossed above" if direction == "above" else "dropped below"
        lines.append(
            f"🎯 Milestone reached: {label} {verb} {fmt_threshold} (now {fmt_current})"
        )

    return "\n".join(lines)
