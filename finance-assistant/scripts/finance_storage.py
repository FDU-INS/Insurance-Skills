"""
Shared project-local storage helpers for Finance Assistant.

Finance Assistant keeps runtime state in the active project's `.finance/` directory.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


PROFILE_DIRNAME = ".finance"


def get_project_dir() -> Path:
    project_dir = (
        os.environ.get("FINANCE_PROJECT_DIR")
        or os.environ.get("CLAUDE_PROJECT_DIR")
        or os.getcwd()
    )
    return Path(project_dir).expanduser().resolve()


def get_finance_dir() -> Path:
    return get_project_dir() / PROFILE_DIRNAME


def ensure_finance_dir() -> Path:
    path = get_finance_dir()
    path.mkdir(parents=True, exist_ok=True)
    return path


def ensure_subdir(*parts: str) -> Path:
    path = ensure_finance_dir().joinpath(*parts)
    path.mkdir(parents=True, exist_ok=True)
    return path


# ── Profile ──────────────────────────────────────────────────────────────────

def get_profile_path() -> Path:
    explicit = os.environ.get("FINANCE_PROFILE_PATH")
    if explicit:
        return Path(explicit).expanduser().resolve()
    return ensure_finance_dir() / "finance_profile.json"


# ── Accounts & Transactions ──────────────────────────────────────────────────

def get_accounts_path() -> Path:
    return ensure_subdir("accounts") / "accounts.json"


def get_transactions_path(account_id: str, year: int) -> Path:
    return ensure_subdir("accounts", "transactions") / f"{account_id}_{year}.json"


# ── Budgets ──────────────────────────────────────────────────────────────────

def get_budget_path(year: int, month: int | None = None) -> Path:
    if month:
        return ensure_subdir("budgets") / f"{year}-{month:02d}.json"
    return ensure_subdir("budgets") / f"{year}.json"


# ── Goals ────────────────────────────────────────────────────────────────────

def get_goals_path() -> Path:
    return ensure_subdir("goals") / "goals.json"


# ── Investments ──────────────────────────────────────────────────────────────

def get_portfolio_path() -> Path:
    return ensure_subdir("investments") / "portfolio.json"


def get_investment_snapshot_path(date_str: str) -> Path:
    return ensure_subdir("investments", "snapshots") / f"{date_str}.json"


# ── Debt ─────────────────────────────────────────────────────────────────────

def get_debts_path() -> Path:
    return ensure_subdir("debt") / "debts.json"


def get_payoff_plan_path(plan_id: str) -> Path:
    return ensure_subdir("debt", "payoff_plans") / f"{plan_id}.json"


# ── Insurance ────────────────────────────────────────────────────────────────

def get_insurance_path() -> Path:
    return ensure_subdir("insurance") / "policies.json"


# ── Net Worth ────────────────────────────────────────────────────────────────

def get_net_worth_snapshot_path(date_str: str) -> Path:
    return ensure_subdir("net_worth", "snapshots") / f"{date_str}.json"


# ── Taxes ────────────────────────────────────────────────────────────────────

def get_tax_path(locale: str, year: int) -> Path:
    return ensure_subdir("taxes", locale) / f"{year}.json"


def get_tax_claims_path(locale: str, year: int) -> Path:
    return ensure_subdir("taxes", locale) / f"{year}-claims.json"


# ── Workspace ────────────────────────────────────────────────────────────────

def get_workspace_path(year: int) -> Path:
    return ensure_subdir("workspace") / f"{year}.json"


def get_output_suite_path(year: int) -> Path:
    return ensure_subdir("workspace") / f"{year}-outputs.json"


# ── Imports ──────────────────────────────────────────────────────────────────

def get_import_log_path() -> Path:
    return ensure_subdir("imports") / "import_log.json"


# ── Locales ──────────────────────────────────────────────────────────────────

def get_locale_dir(locale_code: str) -> Path:
    return ensure_subdir("locales", locale_code)


# ── Source snapshots (for rule updater) ──────────────────────────────────────

def get_source_snapshot_dir() -> Path:
    return ensure_subdir("source_snapshots")


def get_proposal_dir() -> Path:
    return ensure_subdir("proposals")


# ── Generic I/O ──────────────────────────────────────────────────────────────

def load_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def save_json(path: Path, data: Any) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    try:
        with tmp.open("w", encoding="utf-8") as handle:
            json.dump(data, handle, ensure_ascii=False, indent=2)
        tmp.replace(path)  # atomic on POSIX
    except Exception:
        tmp.unlink(missing_ok=True)
        raise
    return path


# ── Migration from .taxde/ ───────────────────────────────────────────────────

def get_legacy_taxde_dir() -> Path:
    return get_project_dir() / ".taxde"


def has_legacy_data() -> bool:
    legacy = get_legacy_taxde_dir()
    return legacy.exists() and (legacy / "taxde_profile.json").exists()
