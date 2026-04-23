"""
Tests for scripts/bank_sync.py

HTTP calls are mocked by patching the `requests` attribute on the bank_sync
module itself (bank_sync.requests.*). This works regardless of whether the
`requests` package is installed in the test environment.
No real network calls are made.
"""

from __future__ import annotations

import json
import os
import sys
import types
from datetime import datetime, timezone, timedelta
from pathlib import Path
from unittest.mock import MagicMock, patch, call

import pytest

# Ensure scripts/ is on the path
_SCRIPTS = os.path.join(os.path.dirname(__file__), "..", "scripts")
if _SCRIPTS not in sys.path:
    sys.path.insert(0, _SCRIPTS)

# ── Inject a stub `requests` module so bank_sync can import cleanly without
#    the package being installed. Tests then patch bank_sync.requests.*  ──────

def _make_requests_stub():
    stub = types.ModuleType("requests")
    stub.get = MagicMock()
    stub.post = MagicMock()
    stub.delete = MagicMock()
    return stub

if "requests" not in sys.modules:
    sys.modules["requests"] = _make_requests_stub()


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture()
def finance_dir(tmp_path, monkeypatch):
    """Redirect all .finance/ I/O to a temp directory."""
    monkeypatch.setenv("FINANCE_PROJECT_DIR", str(tmp_path))
    monkeypatch.setenv("FINANCE_CRED_PASSPHRASE", "test-passphrase-12345")
    yield tmp_path / ".finance"


@pytest.fixture()
def bank_sync(finance_dir):
    """Return a freshly reloaded bank_sync module scoped to the temp dir."""
    import importlib
    import bank_sync as bs
    importlib.reload(bs)
    # Replace bs.requests with a fresh mock so tests get a clean slate
    bs.requests = _make_requests_stub()
    return bs


def _setup_token(finance_dir):
    """Write a valid cached token into .finance/bank_sync/token_cache.json."""
    bsd = finance_dir / "bank_sync"
    bsd.mkdir(parents=True, exist_ok=True)
    future = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
    (bsd / "token_cache.json").write_text(
        json.dumps({"access": "tok", "access_expires": future})
    )
    return bsd


def _mock_response(json_data, status_code=200):
    resp = MagicMock()
    resp.json.return_value = json_data
    resp.status_code = status_code
    resp.raise_for_status = MagicMock()
    return resp


# ── 1. get_access_token ───────────────────────────────────────────────────────

class TestGetAccessToken:
    def test_returns_cached_token_when_valid(self, bank_sync, finance_dir):
        """If a cached token exists and is not expired, return it without HTTP."""
        bsd = _setup_token(finance_dir)

        token = bank_sync.get_access_token()

        assert token == "tok"
        bank_sync.requests.post.assert_not_called()

    def test_fetches_new_token_when_expired(self, bank_sync, finance_dir):
        """If cache is expired, POST /token/new/ to get a fresh token."""
        bsd = finance_dir / "bank_sync"
        bsd.mkdir(parents=True, exist_ok=True)
        past = (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat()
        (bsd / "token_cache.json").write_text(
            json.dumps({"access": "old_token", "access_expires": past})
        )
        (bsd / "credentials.enc").write_text(
            json.dumps({"secret_id": "test-id", "secret_key": "test-key"})
        )
        bank_sync.requests.post.return_value = _mock_response(
            {"access": "new_token_xyz", "access_expires": 86400}
        )

        token = bank_sync.get_access_token()

        assert token == "new_token_xyz"
        bank_sync.requests.post.assert_called_once()
        call_url = bank_sync.requests.post.call_args[0][0]
        assert "token/new" in call_url

    def test_fetches_new_token_when_no_cache(self, bank_sync, finance_dir):
        """No cache file → fetch a fresh token."""
        bsd = finance_dir / "bank_sync"
        bsd.mkdir(parents=True, exist_ok=True)
        (bsd / "credentials.enc").write_text(
            json.dumps({"secret_id": "sid", "secret_key": "skey"})
        )
        bank_sync.requests.post.return_value = _mock_response(
            {"access": "fresh_token", "access_expires": 3600}
        )

        token = bank_sync.get_access_token()
        assert token == "fresh_token"


# ── 2. list_institutions ──────────────────────────────────────────────────────

class TestListInstitutions:
    def test_constructs_correct_url_and_normalizes(self, bank_sync, finance_dir):
        _setup_token(finance_dir)
        bank_sync.requests.get.return_value = _mock_response([
            {"id": "SPARKASSE_DE", "name": "Sparkasse", "bic": "BELADEBE", "logo": "https://example.com/logo.png"},
            {"id": "ING_DE", "name": "ING", "bic": "INGDDEFF", "logo": ""},
        ])

        result = bank_sync.list_institutions(country="de")

        get_call = bank_sync.requests.get.call_args
        assert "institutions" in get_call[0][0]
        assert get_call[1]["params"]["country"] == "de"
        assert len(result) == 2
        assert result[0]["id"] == "SPARKASSE_DE"
        assert result[1]["name"] == "ING"

    def test_uppercase_country_lowercased(self, bank_sync, finance_dir):
        _setup_token(finance_dir)
        bank_sync.requests.get.return_value = _mock_response([])

        bank_sync.list_institutions(country="GB")
        assert bank_sync.requests.get.call_args[1]["params"]["country"] == "gb"


# ── 3. get_account_transactions ───────────────────────────────────────────────

class TestGetAccountTransactions:
    def test_normalizes_booked_transactions(self, bank_sync, finance_dir):
        _setup_token(finance_dir)
        bank_sync.requests.get.return_value = _mock_response({
            "transactions": {
                "booked": [
                    {
                        "transactionId": "TX001",
                        "bookingDate": "2024-03-15",
                        "transactionAmount": {"amount": "-42.50", "currency": "EUR"},
                        "remittanceInformationUnstructured": "REWE Berlin",
                        "creditorName": "REWE GmbH",
                        "debtorName": "",
                    },
                    {
                        "transactionId": "TX002",
                        "bookingDate": "2024-03-16",
                        "transactionAmount": {"amount": "3000.00", "currency": "EUR"},
                        "remittanceInformationUnstructured": "Gehalt März",
                        "creditorName": "",
                        "debtorName": "ACME Corp",
                    },
                ],
                "pending": [],
            }
        })

        txns = bank_sync.get_account_transactions("acc-123")

        assert len(txns) == 2
        assert txns[0]["amount"] == -42.50
        assert txns[0]["description"] == "REWE Berlin"
        assert txns[0]["creditor_name"] == "REWE GmbH"
        assert txns[0]["transaction_id"] == "TX001"
        assert txns[0]["date"] == "2024-03-15"
        # Positive = income
        assert txns[1]["amount"] == 3000.00
        assert txns[1]["debtor_name"] == "ACME Corp"

    def test_includes_pending_transactions(self, bank_sync, finance_dir):
        _setup_token(finance_dir)
        bank_sync.requests.get.return_value = _mock_response({
            "transactions": {
                "booked": [],
                "pending": [
                    {
                        "transactionId": "PEND001",
                        "valueDate": "2024-03-20",
                        "transactionAmount": {"amount": "-15.00", "currency": "EUR"},
                        "remittanceInformationUnstructured": "Coffee shop",
                    }
                ],
            }
        })

        txns = bank_sync.get_account_transactions("acc-123")
        assert len(txns) == 1
        assert txns[0]["amount"] == -15.00
        assert txns[0]["transaction_id"] == "PEND001"

    def test_date_range_params_passed(self, bank_sync, finance_dir):
        _setup_token(finance_dir)
        bank_sync.requests.get.return_value = _mock_response(
            {"transactions": {"booked": [], "pending": []}}
        )

        bank_sync.get_account_transactions(
            "acc-x", date_from="2024-01-01", date_to="2024-03-31"
        )
        params = bank_sync.requests.get.call_args[1]["params"]
        assert params["date_from"] == "2024-01-01"
        assert params["date_to"] == "2024-03-31"


# ── 4. sync_account: deduplication ───────────────────────────────────────────

class TestSyncAccountDeduplication:
    def _txn_response(self):
        return _mock_response({
            "transactions": {
                "booked": [
                    {
                        "transactionId": "DEDUP001",
                        "bookingDate": "2024-03-15",
                        "transactionAmount": {"amount": "-10.00", "currency": "EUR"},
                        "remittanceInformationUnstructured": "Coffee",
                    }
                ],
                "pending": [],
            }
        })

    def test_duplicate_not_imported_twice(self, bank_sync, finance_dir):
        """Same transaction_id is skipped on the second sync."""
        _setup_token(finance_dir)
        bank_sync.requests.get.return_value = self._txn_response()

        with patch("bank_sync.add_transaction") as mock_add:
            result1 = bank_sync.sync_account("gc-acc", "fa-acc")
            # Re-set mock return for second call
            bank_sync.requests.get.return_value = self._txn_response()
            result2 = bank_sync.sync_account("gc-acc", "fa-acc")

        assert result1["new_transactions"] == 1
        assert result1["skipped_duplicates"] == 0
        assert result2["new_transactions"] == 0
        assert result2["skipped_duplicates"] == 1
        assert mock_add.call_count == 1

    def test_new_transactions_increment_count(self, bank_sync, finance_dir):
        _setup_token(finance_dir)
        bank_sync.requests.get.return_value = _mock_response({
            "transactions": {
                "booked": [
                    {
                        "transactionId": f"TX{i}",
                        "bookingDate": "2024-03-15",
                        "transactionAmount": {"amount": "-5.00", "currency": "EUR"},
                        "remittanceInformationUnstructured": f"Item {i}",
                    }
                    for i in range(3)
                ],
                "pending": [],
            }
        })

        with patch("bank_sync.add_transaction"):
            result = bank_sync.sync_account("gc-acc", "fa-acc")

        assert result["new_transactions"] == 3
        assert result["skipped_duplicates"] == 0


# ── 5. list_linked_accounts ───────────────────────────────────────────────────

class TestListLinkedAccounts:
    def test_returns_empty_list_when_file_missing(self, bank_sync, finance_dir):
        result = bank_sync.list_linked_accounts()
        assert result == []

    def test_returns_accounts_from_file(self, bank_sync, finance_dir):
        bsd = finance_dir / "bank_sync"
        bsd.mkdir(parents=True, exist_ok=True)
        (bsd / "linked_accounts.json").write_text(json.dumps({
            "accounts": [
                {
                    "fa_account_id": "checking",
                    "gc_account_id": "gc-123",
                    "institution": "Sparkasse",
                    "iban_last4": "4567",
                    "currency": "EUR",
                    "last_synced": None,
                }
            ]
        }))

        result = bank_sync.list_linked_accounts()
        assert len(result) == 1
        assert result[0]["institution"] == "Sparkasse"
        assert result[0]["iban_last4"] == "4567"


# ── 6. IBAN masking ───────────────────────────────────────────────────────────

class TestIbanMasking:
    def test_full_iban_never_stored(self, bank_sync, finance_dir):
        """get_account_details must never return the full IBAN."""
        _setup_token(finance_dir)
        full_iban = "DE89370400440532013000"
        bank_sync.requests.get.return_value = _mock_response({
            "account": {
                "iban": full_iban,
                "name": "Girokonto",
                "currency": "EUR",
                "product": "Current Account",
            }
        })

        details = bank_sync.get_account_details("acc-id")

        result_str = json.dumps(details)
        assert full_iban not in result_str
        assert details["iban_last4"] == "3000"

    def test_mask_iban_helper_various_formats(self, bank_sync):
        assert bank_sync._mask_iban("DE89370400440532013000") == "3000"
        assert bank_sync._mask_iban("GB29NWBK60161331926819") == "6819"
        assert bank_sync._mask_iban("DE89 3704 0044 0532 0130 00") == "3000"
        assert bank_sync._mask_iban("") == ""
        assert bank_sync._mask_iban("ABC") == "ABC"  # shorter than 4: return as-is

    def test_link_account_stores_only_masked_iban(self, bank_sync, finance_dir):
        """link_account must store only iban_last4, never full IBAN."""
        _setup_token(finance_dir)
        full_iban = "DE89370400440532013000"
        bank_sync.requests.get.return_value = _mock_response({
            "account": {"iban": full_iban, "currency": "EUR"}
        })

        result = bank_sync.link_account("gc-123", "checking", "Sparkasse", "req-456")

        la_path = finance_dir / "bank_sync" / "linked_accounts.json"
        la_content = la_path.read_text()
        assert full_iban not in la_content
        assert "3000" in la_content
        assert result["account"]["iban_last4"] == "3000"


# ── 7. revoke_access ─────────────────────────────────────────────────────────

class TestRevokeAccess:
    def _setup(self, finance_dir):
        bsd = finance_dir / "bank_sync"
        bsd.mkdir(parents=True, exist_ok=True)
        future = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
        (bsd / "token_cache.json").write_text(
            json.dumps({"access": "tok", "access_expires": future})
        )
        (bsd / "linked_accounts.json").write_text(json.dumps({
            "accounts": [
                {
                    "fa_account_id": "checking",
                    "gc_account_id": "gc-123",
                    "requisition_id": "req-456",
                    "institution": "Sparkasse",
                    "iban_last4": "0001",
                }
            ]
        }))
        (bsd / "requisitions.json").write_text(json.dumps({
            "requisitions": [
                {"requisition_id": "req-456", "institution_id": "SPARKASSE_DE", "status": "LN"}
            ]
        }))
        return bsd

    def test_removes_account_from_linked_accounts(self, bank_sync, finance_dir):
        bsd = self._setup(finance_dir)
        bank_sync.requests.delete.return_value = _mock_response({})

        result = bank_sync.revoke_access("gc-123")

        assert result is True
        la = json.loads((bsd / "linked_accounts.json").read_text())
        assert all(a["gc_account_id"] != "gc-123" for a in la["accounts"])

    def test_removes_requisition(self, bank_sync, finance_dir):
        bsd = self._setup(finance_dir)
        bank_sync.requests.delete.return_value = _mock_response({})

        bank_sync.revoke_access("gc-123")

        reqs = json.loads((bsd / "requisitions.json").read_text())
        assert all(r["requisition_id"] != "req-456" for r in reqs["requisitions"])

    def test_credentials_left_intact(self, bank_sync, finance_dir):
        """Revoking one account must NOT delete credentials.enc."""
        bsd = self._setup(finance_dir)
        creds_path = bsd / "credentials.enc"
        creds_path.write_text(json.dumps({"secret_id": "sid", "secret_key": "skey"}))
        bank_sync.requests.delete.return_value = _mock_response({})

        bank_sync.revoke_access("gc-123")

        assert creds_path.exists(), "credentials.enc must not be deleted on revoke"

    def test_calls_delete_endpoint(self, bank_sync, finance_dir):
        self._setup(finance_dir)
        bank_sync.requests.delete.return_value = _mock_response({})

        bank_sync.revoke_access("gc-123")

        bank_sync.requests.delete.assert_called_once()
        assert "req-456" in bank_sync.requests.delete.call_args[0][0]


# ── 8. get_sync_status ────────────────────────────────────────────────────────

class TestGetSyncStatus:
    def test_status_when_no_accounts_no_credentials(self, bank_sync, finance_dir):
        status = bank_sync.get_sync_status()
        assert status["linked_accounts"] == 0
        assert status["credentials_configured"] is False
        assert status["status"] == "credentials_missing"
        assert status["accounts"] == []
        assert status["last_synced"] is None

    def test_status_with_credentials_no_accounts(self, bank_sync, finance_dir):
        bsd = finance_dir / "bank_sync"
        bsd.mkdir(parents=True, exist_ok=True)
        (bsd / "credentials.enc").write_text("{}")

        status = bank_sync.get_sync_status()
        assert status["credentials_configured"] is True
        assert status["linked_accounts"] == 0
        assert status["status"] == "no_accounts"

    def test_status_with_linked_accounts(self, bank_sync, finance_dir):
        bsd = finance_dir / "bank_sync"
        bsd.mkdir(parents=True, exist_ok=True)
        (bsd / "credentials.enc").write_text("{}")
        synced_at = "2024-03-15T10:00:00"
        (bsd / "linked_accounts.json").write_text(json.dumps({
            "accounts": [
                {
                    "fa_account_id": "checking",
                    "gc_account_id": "gc-123",
                    "institution": "Sparkasse",
                    "iban_last4": "0001",
                    "currency": "EUR",
                    "last_synced": synced_at,
                }
            ]
        }))

        status = bank_sync.get_sync_status()
        assert status["credentials_configured"] is True
        assert status["linked_accounts"] == 1
        assert status["status"] == "ready"
        assert status["last_synced"] == synced_at
        assert status["accounts"][0]["institution"] == "Sparkasse"
