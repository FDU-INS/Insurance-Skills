"""Tests for finance_storage.py."""
from finance_storage import (
    get_finance_dir, ensure_finance_dir, ensure_subdir,
    get_profile_path, get_accounts_path, get_transactions_path,
    get_budget_path, get_goals_path, get_portfolio_path,
    get_debts_path, get_insurance_path, get_net_worth_snapshot_path,
    get_tax_path, get_tax_claims_path, get_workspace_path,
    get_import_log_path, get_locale_dir,
    load_json, save_json,
)


def test_ensure_finance_dir_creates_directory(isolated_finance_dir):
    path = ensure_finance_dir()
    assert path.exists()
    assert path.name == ".finance"


def test_ensure_subdir(isolated_finance_dir):
    path = ensure_subdir("accounts", "transactions")
    assert path.exists()
    assert path.name == "transactions"


def test_save_and_load_json(isolated_finance_dir):
    path = ensure_finance_dir() / "test.json"
    save_json(path, {"key": "value", "num": 42})
    loaded = load_json(path)
    assert loaded["key"] == "value"
    assert loaded["num"] == 42


def test_load_json_missing_file(isolated_finance_dir):
    path = ensure_finance_dir() / "nonexistent.json"
    assert load_json(path, default={"empty": True}) == {"empty": True}


def test_path_helpers_return_paths(isolated_finance_dir):
    assert get_profile_path().name == "finance_profile.json"
    assert get_accounts_path().name == "accounts.json"
    assert "2026" in get_transactions_path("checking", 2026).name
    assert get_budget_path(2026, 4).name == "2026-04.json"
    assert get_goals_path().name == "goals.json"
    assert get_portfolio_path().name == "portfolio.json"
    assert get_debts_path().name == "debts.json"
    assert get_insurance_path().name == "policies.json"
    assert "2026-04-01" in get_net_worth_snapshot_path("2026-04-01").name
    assert get_tax_path("de", 2026).name == "2026.json"
    assert get_tax_claims_path("de", 2026).name == "2026-claims.json"
    assert get_workspace_path(2026).name == "2026.json"
    assert get_import_log_path().name == "import_log.json"
    assert get_locale_dir("de").name == "de"
