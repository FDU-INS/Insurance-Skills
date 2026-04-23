"""
Finance Assistant Snapshot Scheduler.

Auto-snapshots net worth and portfolio at configurable intervals.
Checks on each session start whether a snapshot is due.
"""

from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import Optional

try:
    from finance_storage import ensure_subdir, load_json, save_json
    from net_worth_engine import take_snapshot as take_nw_snapshot, get_snapshots
    from investment_tracker import take_portfolio_snapshot
except ImportError:
    import os, sys
    sys.path.insert(0, os.path.dirname(__file__))
    from finance_storage import ensure_subdir, load_json, save_json
    from net_worth_engine import take_snapshot as take_nw_snapshot, get_snapshots
    from investment_tracker import take_portfolio_snapshot


DEFAULT_INTERVAL_DAYS = 30


def _config_path():
    return ensure_subdir("config") / "snapshot_config.json"


def _load_config() -> dict:
    return load_json(_config_path(), default={
        "net_worth_interval_days": DEFAULT_INTERVAL_DAYS,
        "portfolio_interval_days": DEFAULT_INTERVAL_DAYS,
        "auto_snapshot_enabled": True,
        "last_nw_snapshot": None,
        "last_portfolio_snapshot": None,
    })


def _save_config(config: dict) -> None:
    save_json(_config_path(), config)


def configure_snapshots(
    net_worth_interval: Optional[int] = None,
    portfolio_interval: Optional[int] = None,
    enabled: Optional[bool] = None,
) -> dict:
    """Configure snapshot intervals."""
    config = _load_config()
    if net_worth_interval is not None:
        config["net_worth_interval_days"] = net_worth_interval
    if portfolio_interval is not None:
        config["portfolio_interval_days"] = portfolio_interval
    if enabled is not None:
        config["auto_snapshot_enabled"] = enabled
    _save_config(config)
    return config


def check_and_snapshot() -> dict:
    """
    Check if snapshots are due and take them if so.
    Call this at session start.
    """
    config = _load_config()
    if not config.get("auto_snapshot_enabled", True):
        return {"action": "disabled"}

    today = date.today()
    results = {"date": today.isoformat(), "snapshots_taken": []}

    # Net worth snapshot
    nw_interval = config.get("net_worth_interval_days", DEFAULT_INTERVAL_DAYS)
    last_nw = config.get("last_nw_snapshot")
    nw_due = True
    if last_nw:
        last_date = date.fromisoformat(last_nw)
        nw_due = (today - last_date).days >= nw_interval

    if nw_due:
        try:
            snap = take_nw_snapshot()
            config["last_nw_snapshot"] = today.isoformat()
            results["snapshots_taken"].append({
                "type": "net_worth",
                "net_worth": snap.get("net_worth"),
            })
        except Exception as e:
            results["net_worth_error"] = str(e)

    # Portfolio snapshot
    port_interval = config.get("portfolio_interval_days", DEFAULT_INTERVAL_DAYS)
    last_port = config.get("last_portfolio_snapshot")
    port_due = True
    if last_port:
        last_date = date.fromisoformat(last_port)
        port_due = (today - last_date).days >= port_interval

    if port_due:
        try:
            snap = take_portfolio_snapshot()
            config["last_portfolio_snapshot"] = today.isoformat()
            results["snapshots_taken"].append({
                "type": "portfolio",
                "total_value": snap.get("total_value"),
            })
        except Exception as e:
            results["portfolio_error"] = str(e)

    _save_config(config)
    return results


def get_snapshot_status() -> dict:
    """Return current snapshot schedule status."""
    config = _load_config()
    today = date.today()

    nw_last = config.get("last_nw_snapshot")
    port_last = config.get("last_portfolio_snapshot")

    nw_days_ago = (today - date.fromisoformat(nw_last)).days if nw_last else None
    port_days_ago = (today - date.fromisoformat(port_last)).days if port_last else None

    nw_interval = config.get("net_worth_interval_days", DEFAULT_INTERVAL_DAYS)
    port_interval = config.get("portfolio_interval_days", DEFAULT_INTERVAL_DAYS)

    return {
        "enabled": config.get("auto_snapshot_enabled", True),
        "net_worth": {
            "interval_days": nw_interval,
            "last_snapshot": nw_last,
            "days_ago": nw_days_ago,
            "due": nw_days_ago is None or nw_days_ago >= nw_interval,
        },
        "portfolio": {
            "interval_days": port_interval,
            "last_snapshot": port_last,
            "days_ago": port_days_ago,
            "due": port_days_ago is None or port_days_ago >= port_interval,
        },
    }
