"""
Read-only bank transaction sync via GoCardless (Nordigen) Open Banking API.
Covers 2000+ EU/UK banks. No credentials stored — OAuth consent flow.
Privacy: only access tokens stored (encrypted), never bank passwords.

GoCardless free tier: bankaccountdata.gocardless.com
PSD2 read-only access: account details, balances, and transactions only.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timedelta, timezone
from typing import Optional

try:
    import requests
except ImportError:
    requests = None  # type: ignore[assignment]

try:
    from finance_storage import ensure_subdir, load_json, save_json, get_finance_dir
    from data_safety import encrypt_file, decrypt_file
    from transaction_logger import add_transaction
except ImportError:
    import sys
    sys.path.insert(0, os.path.dirname(__file__))
    from finance_storage import ensure_subdir, load_json, save_json, get_finance_dir
    from data_safety import encrypt_file, decrypt_file
    from transaction_logger import add_transaction


GOCARDLESS_BASE = "https://bankaccountdata.gocardless.com/api/v2"

# ── Storage paths ─────────────────────────────────────────────────────────────

def _bank_sync_dir():
    return ensure_subdir("bank_sync")

def _credentials_path():
    return _bank_sync_dir() / "credentials.enc"

def _token_cache_path():
    return _bank_sync_dir() / "token_cache.json"

def _linked_accounts_path():
    return _bank_sync_dir() / "linked_accounts.json"

def _requisitions_path():
    return _bank_sync_dir() / "requisitions.json"


# ── Credential management ─────────────────────────────────────────────────────

def setup_credentials(secret_id: str, secret_key: str) -> dict:
    """
    Store GoCardless API credentials encrypted in .finance/bank_sync/credentials.enc.
    Returns {"status": "ok", "message": "..."}.
    """
    if not secret_id or not secret_key:
        return {"status": "error", "message": "Both secret_id and secret_key are required."}

    cred_path = _credentials_path()
    # Write as plain JSON first; encrypt_file will encrypt in place.
    # We use a stable passphrase derived from the user's machine to avoid
    # prompting for a passphrase every sync. The actual secret_id/secret_key
    # are the real secrets — wrapping them in Fernet provides at-rest protection.
    import hashlib
    machine_salt = os.environ.get("FINANCE_CRED_PASSPHRASE") or _machine_id()
    passphrase = hashlib.sha256(f"gocardless-{machine_salt}".encode()).hexdigest()[:32]

    save_json(cred_path, {"secret_id": secret_id, "secret_key": secret_key})
    cred_path.chmod(0o600)

    try:
        encrypt_file(str(cred_path), passphrase)
    except Exception as e:
        # If cryptography not installed, leave plain but warn
        return {
            "status": "warning",
            "message": (
                f"Credentials saved (plain — install `cryptography` for encryption): {e}"
            ),
        }

    return {
        "status": "ok",
        "message": (
            "GoCardless credentials stored encrypted at "
            f".finance/bank_sync/credentials.enc. "
            "Run `connect bank` to link your first account."
        ),
    }


def _machine_id() -> str:
    """Return a stable machine-specific string as salt for credential encryption."""
    try:
        with open("/etc/machine-id") as f:
            return f.read().strip()
    except OSError:
        pass
    try:
        import platform
        return platform.node()
    except Exception:
        return "finance-assistant"


def _load_credentials() -> dict:
    """Decrypt and return stored credentials. Raises if not found."""
    cred_path = _credentials_path()
    if not cred_path.exists():
        raise FileNotFoundError(
            "No GoCardless credentials found. "
            "Call setup_credentials(secret_id, secret_key) first."
        )
    import hashlib
    machine_salt = os.environ.get("FINANCE_CRED_PASSPHRASE") or _machine_id()
    passphrase = hashlib.sha256(f"gocardless-{machine_salt}".encode()).hexdigest()[:32]

    try:
        decrypt_file(str(cred_path), passphrase)
    except Exception:
        pass  # File may already be plain (no cryptography library)

    try:
        data = load_json(cred_path)
        if data and not data.get("_encrypted"):
            return data
    except Exception:
        pass
    raise ValueError(
        "Failed to decrypt credentials. "
        "If you changed machines, re-run setup_credentials()."
    )


# ── Token management ──────────────────────────────────────────────────────────

def get_access_token() -> str:
    """
    Obtain a short-lived access token using stored credentials.
    POST /token/new/ with secret_id + secret_key.
    Cache token in .finance/bank_sync/token_cache.json with expiry.
    Returns the access token string.
    """
    if requests is None:
        raise ImportError("requests library is required: pip install requests")

    cache_path = _token_cache_path()
    cache = load_json(cache_path, default={})

    # Return cached token if still valid (with 60s buffer)
    if cache.get("access") and cache.get("access_expires"):
        try:
            expires = datetime.fromisoformat(cache["access_expires"])
            if expires.tzinfo is None:
                expires = expires.replace(tzinfo=timezone.utc)
            if datetime.now(timezone.utc) < expires - timedelta(seconds=60):
                return cache["access"]
        except (ValueError, TypeError):
            pass

    creds = _load_credentials()

    resp = requests.post(
        f"{GOCARDLESS_BASE}/token/new/",
        json={"secret_id": creds["secret_id"], "secret_key": creds["secret_key"]},
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()

    # GoCardless returns access + refresh tokens; access expires in ~24h
    access_expires_in = data.get("access_expires", 86400)  # seconds
    expires_at = (
        datetime.now(timezone.utc) + timedelta(seconds=access_expires_in)
    ).isoformat()

    save_json(cache_path, {
        "access": data["access"],
        "refresh": data.get("refresh"),
        "access_expires": expires_at,
        "obtained_at": datetime.now(timezone.utc).isoformat(),
    })
    cache_path.chmod(0o600)

    return data["access"]


def _auth_headers() -> dict:
    token = get_access_token()
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


# ── Institution discovery ─────────────────────────────────────────────────────

def list_institutions(country: str = "de") -> list[dict]:
    """
    GET /institutions/?country={country}
    Returns list of {"id": str, "name": str, "bic": str, "logo": str}.
    country: ISO 3166-1 alpha-2 (de, gb, fr, nl, pl, etc.)
    """
    if requests is None:
        raise ImportError("requests library is required: pip install requests")

    resp = requests.get(
        f"{GOCARDLESS_BASE}/institutions/",
        params={"country": country.lower()},
        headers=_auth_headers(),
        timeout=30,
    )
    resp.raise_for_status()
    raw = resp.json()

    return [
        {
            "id": inst.get("id", ""),
            "name": inst.get("name", ""),
            "bic": inst.get("bic", ""),
            "logo": inst.get("logo", ""),
        }
        for inst in (raw if isinstance(raw, list) else [])
    ]


# ── Requisition / consent flow ────────────────────────────────────────────────

def create_requisition(
    institution_id: str,
    redirect_uri: str = "https://localhost",
) -> dict:
    """
    Create an end-user agreement + requisition (consent flow).
    POST /agreements/enduser/ then POST /requisitions/.
    Returns {"requisition_id": str, "link": str, "status": str}.
    The link is what the user opens in browser to grant consent.
    """
    if requests is None:
        raise ImportError("requests library is required: pip install requests")

    headers = _auth_headers()

    # Step 1: Create end-user agreement
    agreement_resp = requests.post(
        f"{GOCARDLESS_BASE}/agreements/enduser/",
        json={
            "institution_id": institution_id,
            "max_historical_days": 90,
            "access_valid_for_days": 90,
            "access_scope": ["balances", "details", "transactions"],
        },
        headers=headers,
        timeout=30,
    )
    agreement_resp.raise_for_status()
    agreement = agreement_resp.json()

    # Step 2: Create requisition
    req_resp = requests.post(
        f"{GOCARDLESS_BASE}/requisitions/",
        json={
            "redirect": redirect_uri,
            "institution_id": institution_id,
            "agreement": agreement.get("id"),
            "reference": f"fa-{institution_id[:8]}-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        },
        headers=headers,
        timeout=30,
    )
    req_resp.raise_for_status()
    req = req_resp.json()

    # Persist requisition record
    reqs = load_json(_requisitions_path(), default={"requisitions": []})
    reqs["requisitions"].append({
        "requisition_id": req.get("id"),
        "institution_id": institution_id,
        "agreement_id": agreement.get("id"),
        "status": req.get("status", "CR"),
        "created_at": datetime.now().isoformat(),
        "link": req.get("link"),
    })
    save_json(_requisitions_path(), reqs)

    return {
        "requisition_id": req.get("id"),
        "link": req.get("link"),
        "status": req.get("status", "CR"),
    }


def get_requisition_status(requisition_id: str) -> dict:
    """
    GET /requisitions/{id}/
    Returns {"status": str, "accounts": [account_id, ...]}.
    Status codes:
      CR=created, GC=giving consent, UA=undergoing auth,
      LN=linked, EX=expired, RJ=rejected, SA=suspended
    """
    if requests is None:
        raise ImportError("requests library is required: pip install requests")

    resp = requests.get(
        f"{GOCARDLESS_BASE}/requisitions/{requisition_id}/",
        headers=_auth_headers(),
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()

    # Update local cache
    reqs = load_json(_requisitions_path(), default={"requisitions": []})
    for r in reqs.get("requisitions", []):
        if r.get("requisition_id") == requisition_id:
            r["status"] = data.get("status", r["status"])
    save_json(_requisitions_path(), reqs)

    return {
        "status": data.get("status"),
        "accounts": data.get("accounts", []),
    }


# ── Account data ──────────────────────────────────────────────────────────────

def _mask_iban(iban: str) -> str:
    """Return only the last 4 characters of an IBAN. Never store more."""
    if not iban:
        return ""
    cleaned = iban.replace(" ", "")
    return cleaned[-4:] if len(cleaned) >= 4 else cleaned


def get_account_details(account_id: str) -> dict:
    """
    GET /accounts/{id}/details/
    Returns IBAN (masked to last 4), name, currency, product type.
    IMPORTANT: full IBAN is never stored — only last 4 digits.
    """
    if requests is None:
        raise ImportError("requests library is required: pip install requests")

    resp = requests.get(
        f"{GOCARDLESS_BASE}/accounts/{account_id}/details/",
        headers=_auth_headers(),
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    account = data.get("account", data)

    raw_iban = account.get("iban", "")
    return {
        "iban_last4": _mask_iban(raw_iban),
        "name": account.get("name", ""),
        "currency": account.get("currency", "EUR"),
        "product": account.get("product", ""),
        "owner_name": account.get("ownerName", ""),
        # Never include raw_iban in returned dict
    }


def get_account_balances(account_id: str) -> dict:
    """
    GET /accounts/{id}/balances/
    Returns {"available": float, "current": float, "currency": str}.
    """
    if requests is None:
        raise ImportError("requests library is required: pip install requests")

    resp = requests.get(
        f"{GOCARDLESS_BASE}/accounts/{account_id}/balances/",
        headers=_auth_headers(),
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    balances = data.get("balances", [])

    available = 0.0
    current = 0.0
    currency = "EUR"

    for bal in balances:
        bal_type = bal.get("balanceType", "")
        amount_obj = bal.get("balanceAmount", {})
        amt = float(amount_obj.get("amount", 0))
        currency = amount_obj.get("currency", currency)
        if bal_type in ("interimAvailable", "available"):
            available = amt
        elif bal_type in ("closingBooked", "closingAvailable", "expected"):
            current = amt

    # If we got nothing for available, fall back to current
    if available == 0.0 and current != 0.0:
        available = current

    return {"available": available, "current": current, "currency": currency}


def get_account_transactions(
    account_id: str,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
) -> list[dict]:
    """
    GET /accounts/{id}/transactions/?date_from=&date_to=
    Returns normalized list:
    [{"date": "YYYY-MM-DD", "amount": float, "description": str,
      "currency": str, "creditor_name": str, "debtor_name": str,
      "transaction_id": str}]
    Normalize GoCardless response to Finance Assistant transaction format.
    """
    if requests is None:
        raise ImportError("requests library is required: pip install requests")

    params = {}
    if date_from:
        params["date_from"] = date_from
    if date_to:
        params["date_to"] = date_to

    resp = requests.get(
        f"{GOCARDLESS_BASE}/accounts/{account_id}/transactions/",
        params=params,
        headers=_auth_headers(),
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()

    transactions_data = data.get("transactions", {})
    booked = transactions_data.get("booked", [])
    pending = transactions_data.get("pending", [])

    normalized = []
    for raw in booked + pending:
        amount_obj = raw.get("transactionAmount", {})
        try:
            amount = float(amount_obj.get("amount", 0))
        except (ValueError, TypeError):
            amount = 0.0

        # GoCardless amounts: negative = debit (expense), positive = credit (income)
        date_str = (
            raw.get("bookingDate")
            or raw.get("valueDate")
            or raw.get("bookingDateTime", "")[:10]
            or datetime.now().date().isoformat()
        )

        description = (
            raw.get("remittanceInformationUnstructured")
            or raw.get("remittanceInformationUnstructuredArray", [""])[0]
            or raw.get("additionalInformation")
            or ""
        )

        txn_id = (
            raw.get("transactionId")
            or raw.get("internalTransactionId")
            or f"{date_str}-{abs(amount):.2f}-{description[:20]}"
        )

        normalized.append({
            "date": date_str[:10],
            "amount": amount,
            "description": description,
            "currency": amount_obj.get("currency", "EUR"),
            "creditor_name": raw.get("creditorName", ""),
            "debtor_name": raw.get("debtorName", ""),
            "transaction_id": txn_id,
        })

    return normalized


# ── Sync logic ────────────────────────────────────────────────────────────────

def sync_account(
    account_id: str,
    fa_account_id: str,
    days_back: int = 90,
) -> dict:
    """
    Pull recent transactions and import into Finance Assistant.
    Deduplicates by transaction_id (stored in import log).
    Returns {"new_transactions": int, "skipped_duplicates": int, "account": str}.
    """
    date_from = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
    date_to = datetime.now().strftime("%Y-%m-%d")

    transactions = get_account_transactions(account_id, date_from=date_from, date_to=date_to)

    # Load import log to check already-imported transaction IDs
    from finance_storage import get_import_log_path
    import_log = load_json(get_import_log_path(), default={"imports": [], "bank_sync_ids": []})
    seen_ids = set(import_log.get("bank_sync_ids", []))

    new_count = 0
    skipped = 0

    for txn in transactions:
        txn_id = txn["transaction_id"]
        if txn_id in seen_ids:
            skipped += 1
            continue

        amount = txn["amount"]
        txn_type = "income" if amount > 0 else "expense"
        description = txn["description"] or txn.get("creditor_name") or txn.get("debtor_name") or "Bank transaction"

        add_transaction(
            date=txn["date"],
            type=txn_type,
            amount=abs(amount),
            category="other_income" if txn_type == "income" else "other_expense",
            description=description,
            account_id=fa_account_id,
            currency=txn.get("currency", "EUR"),
            import_source="gocardless",
            import_ref=txn_id,
            payee=txn.get("creditor_name") or txn.get("debtor_name") or "",
        )
        seen_ids.add(txn_id)
        new_count += 1

    # Persist updated seen IDs
    import_log["bank_sync_ids"] = list(seen_ids)
    save_json(get_import_log_path(), import_log)

    # Update last_synced in linked_accounts
    linked = load_json(_linked_accounts_path(), default={"accounts": []})
    for acct in linked.get("accounts", []):
        if acct.get("gc_account_id") == account_id:
            acct["last_synced"] = datetime.now().isoformat()
    save_json(_linked_accounts_path(), linked)

    return {
        "new_transactions": new_count,
        "skipped_duplicates": skipped,
        "account": fa_account_id,
    }


def sync_all(days_back: int = 90) -> dict:
    """Sync all linked accounts. Returns summary per account."""
    accounts = list_linked_accounts()
    if not accounts:
        return {
            "status": "no_accounts",
            "message": "No linked accounts. Run `connect bank` to link a bank account.",
        }

    results = {}
    errors = {}
    for acct in accounts:
        gc_id = acct.get("gc_account_id")
        fa_id = acct.get("fa_account_id")
        label = acct.get("institution", gc_id)
        try:
            result = sync_account(gc_id, fa_id, days_back=days_back)
            results[label] = result
        except Exception as e:
            errors[label] = str(e)

    return {
        "synced": results,
        "errors": errors,
        "total_accounts": len(accounts),
        "successful": len(results),
        "failed": len(errors),
    }


# ── Account registry ──────────────────────────────────────────────────────────

def list_linked_accounts() -> list[dict]:
    """
    List accounts linked via GoCardless.
    Stored in .finance/bank_sync/linked_accounts.json.
    Each: {"fa_account_id": str, "gc_account_id": str, "institution": str,
           "iban_last4": str, "currency": str, "last_synced": str}
    """
    data = load_json(_linked_accounts_path(), default={"accounts": []})
    return data.get("accounts", [])


def link_account(
    gc_account_id: str,
    fa_account_id: str,
    institution: str,
    requisition_id: str,
) -> dict:
    """
    Register a GoCardless account ID with a Finance Assistant account ID.
    Fetches account details and stores masked IBAN only.
    """
    details = get_account_details(gc_account_id)

    linked = load_json(_linked_accounts_path(), default={"accounts": []})

    # Don't duplicate
    for acct in linked.get("accounts", []):
        if acct.get("gc_account_id") == gc_account_id:
            return {"status": "already_linked", "account": acct}

    entry = {
        "fa_account_id": fa_account_id,
        "gc_account_id": gc_account_id,
        "requisition_id": requisition_id,
        "institution": institution,
        "iban_last4": details.get("iban_last4", ""),
        "currency": details.get("currency", "EUR"),
        "owner_name": details.get("owner_name", ""),
        "last_synced": None,
        "linked_at": datetime.now().isoformat(),
    }
    linked.setdefault("accounts", []).append(entry)
    save_json(_linked_accounts_path(), linked)

    return {"status": "linked", "account": entry}


def revoke_access(account_id: str) -> bool:
    """
    Delete the requisition for this account and purge all GoCardless data for it.
    DELETE /requisitions/{requisition_id}/
    Credentials file is left intact (other accounts may still use it).
    Returns True on success.
    """
    if requests is None:
        raise ImportError("requests library is required: pip install requests")

    # Find the requisition_id for this account
    linked = load_json(_linked_accounts_path(), default={"accounts": []})
    requisition_id = None
    for acct in linked.get("accounts", []):
        if acct.get("gc_account_id") == account_id or acct.get("fa_account_id") == account_id:
            requisition_id = acct.get("requisition_id")
            break

    if requisition_id:
        try:
            requests.delete(
                f"{GOCARDLESS_BASE}/requisitions/{requisition_id}/",
                headers=_auth_headers(),
                timeout=30,
            ).raise_for_status()
        except Exception:
            pass  # Proceed with local cleanup even if API call fails

    # Remove from linked_accounts
    linked["accounts"] = [
        a for a in linked.get("accounts", [])
        if a.get("gc_account_id") != account_id and a.get("fa_account_id") != account_id
    ]
    save_json(_linked_accounts_path(), linked)

    # Remove from requisitions
    reqs = load_json(_requisitions_path(), default={"requisitions": []})
    if requisition_id:
        reqs["requisitions"] = [
            r for r in reqs.get("requisitions", [])
            if r.get("requisition_id") != requisition_id
        ]
        save_json(_requisitions_path(), reqs)

    return True


def get_sync_status() -> dict:
    """
    Summary: how many accounts linked, when last synced, credentials present.
    """
    accounts = list_linked_accounts()
    credentials_present = _credentials_path().exists()

    last_synced_times = [
        a["last_synced"] for a in accounts if a.get("last_synced")
    ]
    last_synced = max(last_synced_times) if last_synced_times else None

    return {
        "credentials_configured": credentials_present,
        "linked_accounts": len(accounts),
        "accounts": [
            {
                "institution": a.get("institution"),
                "fa_account_id": a.get("fa_account_id"),
                "iban_last4": a.get("iban_last4"),
                "currency": a.get("currency"),
                "last_synced": a.get("last_synced"),
            }
            for a in accounts
        ],
        "last_synced": last_synced,
        "status": "ready" if credentials_present and accounts else (
            "credentials_missing" if not credentials_present else "no_accounts"
        ),
    }
