"""
Finance Assistant Scenario Store — Save & Recall Named Scenarios.

Persists named scenario results to .finance/scenarios/{slug}.json so users
can revisit, compare, and track how a plan has changed over time.
"""

from __future__ import annotations

import json
import os
import re
from datetime import date, datetime
from pathlib import Path
from typing import Optional

try:
    from finance_storage import ensure_subdir, get_finance_dir, load_json, save_json
except ImportError:
    import sys
    sys.path.insert(0, os.path.dirname(__file__))
    from finance_storage import ensure_subdir, get_finance_dir, load_json, save_json


# ── Helpers ──────────────────────────────────────────────────────────────────

def _scenarios_dir() -> Path:
    return ensure_subdir("scenarios")


def _slug(name: str) -> str:
    """Convert a scenario name to a filesystem-safe slug."""
    return re.sub(r"[^a-z0-9_]", "_", name.lower().strip()).strip("_")


def _scenario_path(name: str) -> Path:
    return _scenarios_dir() / f"{_slug(name)}.json"


def _profile_snapshot(profile_snapshot: Optional[dict]) -> dict:
    """Extract key metrics from a profile snapshot for storage."""
    if not profile_snapshot:
        return {}
    snap = {}
    for key in ("net_worth", "portfolio_value", "debt_total", "savings_rate",
                "emergency_fund_months", "fire_pct"):
        if key in profile_snapshot:
            snap[key] = profile_snapshot[key]
    return snap


# ── Public API ───────────────────────────────────────────────────────────────

def save_scenario(
    name: str,
    scenario_type: str,
    inputs: dict,
    result: dict,
    profile_snapshot: Optional[dict] = None,
) -> dict:
    """
    Save a named scenario to .finance/scenarios/{slug}.json.

    slug = name.lower().replace(" ", "_")
    Stores: name, type, inputs, result, saved_at, profile_snapshot (key metrics only).
    Returns the saved record.
    """
    record = {
        "name": name,
        "slug": _slug(name),
        "type": scenario_type,
        "inputs": inputs,
        "result": result,
        "saved_at": datetime.now().isoformat(timespec="seconds"),
        "profile_snapshot": _profile_snapshot(profile_snapshot),
    }
    _scenarios_dir()  # ensure dir exists
    path = _scenario_path(name)
    path.write_text(json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8")
    return record


def load_scenario(name: str) -> Optional[dict]:
    """Load scenario by name (fuzzy match on slug). Returns None if not found."""
    target = _slug(name)
    scenarios_dir = _scenarios_dir()
    # Exact match first
    exact = scenarios_dir / f"{target}.json"
    if exact.exists():
        try:
            return json.loads(exact.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return None
    # Fuzzy: find files whose slug starts with or contains target
    for path in sorted(scenarios_dir.glob("*.json")):
        slug_on_disk = path.stem
        if target in slug_on_disk or slug_on_disk.startswith(target):
            try:
                return json.loads(path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                continue
    return None


def list_scenarios() -> list[dict]:
    """List all saved scenarios with name, type, saved_at, one-line summary."""
    results = []
    for path in sorted(_scenarios_dir().glob("*.json")):
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        # Build a one-line summary from the result dict
        result_data = record.get("result", {})
        summary_parts = []
        for key in ("years_to_fire", "recommendation", "best_option", "net_worth",
                    "monthly_payment", "total_interest"):
            val = result_data.get(key)
            if val is not None:
                if isinstance(val, dict):
                    val = val.get("label") or val.get("estimated_annual_net") or str(val)
                summary_parts.append(f"{key}={val}")
            if len(summary_parts) >= 2:
                break
        summary = "; ".join(str(s) for s in summary_parts) if summary_parts else "—"
        results.append({
            "name": record.get("name", path.stem),
            "type": record.get("type", "unknown"),
            "saved_at": record.get("saved_at", ""),
            "summary": summary,
            "slug": record.get("slug", path.stem),
        })
    results.sort(key=lambda r: r.get("saved_at", ""))
    return results


def delete_scenario(name: str) -> bool:
    """Delete a scenario by name. Returns True if deleted."""
    # Try exact slug first, then fuzzy load
    target = _slug(name)
    exact = _scenarios_dir() / f"{target}.json"
    if exact.exists():
        exact.unlink()
        return True
    # Fuzzy
    for path in _scenarios_dir().glob("*.json"):
        if target in path.stem or path.stem.startswith(target):
            path.unlink()
            return True
    return False


def compare_scenario_to_current(name: str, current_profile: dict) -> Optional[dict]:
    """
    Load a saved scenario and compare its profile_snapshot to current profile.

    Returns:
        {
          "scenario_name": str,
          "saved_at": str,
          "days_ago": int,
          "changes_since_saved": {
            "net_worth_delta": float,
            "portfolio_delta": float,
            "debt_delta": float,
            "notes": [str]
          },
          "original_result": dict
        }
    """
    record = load_scenario(name)
    if record is None:
        return None

    saved_at_str = record.get("saved_at", "")
    try:
        saved_at = datetime.fromisoformat(saved_at_str)
        days_ago = (datetime.now() - saved_at).days
    except (ValueError, TypeError):
        days_ago = 0

    snap = record.get("profile_snapshot", {})
    # Current metrics — accept a flat dict or nested under common keys
    def _get(profile: dict, key: str) -> Optional[float]:
        if key in profile:
            return float(profile[key])
        # Also check a nested "metrics" key
        metrics = profile.get("metrics", {})
        if key in metrics:
            return float(metrics[key])
        return None

    net_worth_old = snap.get("net_worth")
    portfolio_old = snap.get("portfolio_value")
    debt_old = snap.get("debt_total")

    net_worth_now = _get(current_profile, "net_worth")
    portfolio_now = _get(current_profile, "portfolio_value")
    debt_now = _get(current_profile, "debt_total")

    def _delta(old, now) -> Optional[float]:
        if old is not None and now is not None:
            return round(now - old, 2)
        return None

    nw_delta = _delta(net_worth_old, net_worth_now)
    pf_delta = _delta(portfolio_old, portfolio_now)
    debt_delta = _delta(debt_old, debt_now)

    notes: list[str] = []
    if nw_delta is not None:
        direction = "grew" if nw_delta >= 0 else "fell"
        notes.append(f"Net worth {direction} €{abs(nw_delta):,.0f} since this scenario was saved")
    if pf_delta is not None:
        direction = "grew" if pf_delta >= 0 else "fell"
        notes.append(f"Portfolio {direction} €{abs(pf_delta):,.0f}")
    if debt_delta is not None:
        direction = "increased" if debt_delta > 0 else "decreased"
        notes.append(f"Total debt {direction} €{abs(debt_delta):,.0f}")
    if not notes:
        notes.append("No comparable metrics in the saved profile snapshot")

    return {
        "scenario_name": record.get("name", name),
        "saved_at": saved_at_str,
        "days_ago": days_ago,
        "changes_since_saved": {
            "net_worth_delta": nw_delta,
            "portfolio_delta": pf_delta,
            "debt_delta": debt_delta,
            "notes": notes,
        },
        "original_result": record.get("result", {}),
    }


def format_scenario_list() -> str:
    """Plain-text list of saved scenarios with type, age, one-liner."""
    items = list_scenarios()
    if not items:
        return "No saved scenarios yet. After any calculation say 'save as [name]' to keep it."

    lines = ["Saved scenarios:"]
    for item in items:
        saved_at = item.get("saved_at", "")
        try:
            saved_dt = datetime.fromisoformat(saved_at)
            days_ago = (datetime.now() - saved_dt).days
            age = f"{days_ago}d ago" if days_ago > 0 else "today"
        except (ValueError, TypeError):
            age = "unknown age"
        lines.append(
            f"  • {item['name']} [{item['type']}] — {age} — {item['summary']}"
        )
    return "\n".join(lines)
