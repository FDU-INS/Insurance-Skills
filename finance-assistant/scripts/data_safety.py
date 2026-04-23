"""
Finance Assistant Data Safety Layer.

Provides encryption, data minimization, and privacy controls to make users
comfortable sharing financial data. All sensitive data stays local and can
be encrypted at rest.

Key principles:
1. All data is project-local (.finance/) — never uploaded anywhere
2. Optional encryption at rest using a user-provided passphrase
3. Data minimization — only structured summaries, never raw bank credentials
4. Easy data export and deletion ("right to be forgotten")
5. Audit log of all data access
6. File permissions hardened to owner-read-write only (600/700)
7. .gitignore guard prevents accidental git commit of financial data
"""

from __future__ import annotations

import json
import os
import shutil
import stat
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    from finance_storage import get_finance_dir, ensure_subdir, load_json, save_json
except ImportError:
    import sys
    sys.path.insert(0, os.path.dirname(__file__))
    from finance_storage import get_finance_dir, ensure_subdir, load_json, save_json

# Encryption backend — Fernet (AES-128-CBC + HMAC-SHA256) with PBKDF2 key derivation.
# Falls back to a warning if the `cryptography` package is not installed.
try:
    import base64 as _b64
    import os as _os
    from cryptography.fernet import Fernet, InvalidToken
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives import hashes as _hashes

    def _derive_fernet_key(passphrase: str, salt: bytes) -> bytes:
        """Derive a 32-byte Fernet-compatible key using PBKDF2-HMAC-SHA256."""
        kdf = PBKDF2HMAC(
            algorithm=_hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480_000,  # NIST 2023 recommendation
        )
        return _b64.urlsafe_b64encode(kdf.derive(passphrase.encode()))

    _CRYPTO_AVAILABLE = True
except ImportError:
    _CRYPTO_AVAILABLE = False


# ── Data Inventory ───────────────────────────────────────────────────────────

SENSITIVE_FIELDS = {
    "never_store": [
        "IBAN", "bank_account_number", "credit_card_number", "CVV",
        "password", "PIN", "TAN", "access_token", "API_key",
        "social_security_number", "passport_number", "tax_ID",
    ],
    "store_if_needed": [
        "name", "address", "email", "phone", "date_of_birth",
        "employer_name", "salary_amount",
    ],
    "always_safe": [
        "currency", "locale", "account_type", "category",
        "amount", "date", "budget_limit", "goal_target",
    ],
}


def get_data_inventory() -> dict:
    """Audit what data is stored and where."""
    finance_dir = get_finance_dir()
    if not finance_dir.exists():
        return {"status": "no_data", "files": []}

    inventory = {
        "status": "data_present",
        "base_path": str(finance_dir),
        "total_files": 0,
        "total_size_bytes": 0,
        "categories": {},
    }

    for root, dirs, files in os.walk(finance_dir):
        for f in files:
            if not f.endswith(".json"):
                continue
            path = Path(root) / f
            rel = path.relative_to(finance_dir)
            size = path.stat().st_size
            category = str(rel).split("/")[0] if "/" in str(rel) else "root"

            inventory["total_files"] += 1
            inventory["total_size_bytes"] += size
            if category not in inventory["categories"]:
                inventory["categories"][category] = {"files": 0, "size_bytes": 0}
            inventory["categories"][category]["files"] += 1
            inventory["categories"][category]["size_bytes"] += size

    inventory["total_size_human"] = _human_size(inventory["total_size_bytes"])
    return inventory


def _human_size(size: int) -> str:
    for unit in ("B", "KB", "MB"):
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} GB"


# ── Data Export ──────────────────────────────────────────────────────────────

def export_all_data(export_path: Optional[str] = None, passphrase: Optional[str] = None) -> str:
    """
    Export all stored data as a single portable JSON file.

    If passphrase is provided, the export file is encrypted with Fernet AES
    before writing — safe to store in cloud or send as backup.
    Returns the export file path.
    """
    finance_dir = get_finance_dir()
    if not finance_dir.exists():
        raise FileNotFoundError("No finance data to export")

    all_data = {
        "exported_at": datetime.now().isoformat(),
        "version": "2.0",
        "encrypted": passphrase is not None,
        "data": {},
    }

    for root, dirs, files in os.walk(finance_dir):
        for f in files:
            if not f.endswith(".json"):
                continue
            path = Path(root) / f
            rel = str(path.relative_to(finance_dir))
            data = load_json(path)
            if data:
                all_data["data"][rel] = data

    if not export_path:
        stamp = datetime.now().strftime("%Y%m%d")
        export_path = str(finance_dir.parent / f"finance-export-{stamp}.json")

    plaintext = json.dumps(all_data, ensure_ascii=False, indent=2).encode()

    if passphrase:
        if not _CRYPTO_AVAILABLE:
            raise RuntimeError("Encrypted export requires: pip install cryptography")
        _check_passphrase_strength(passphrase)
        salt = _os.urandom(16)
        key = _derive_fernet_key(passphrase, salt)
        ciphertext = Fernet(key).encrypt(plaintext)
        with open(export_path, "w", encoding="utf-8") as f:
            json.dump({
                "_encrypted": "fernet",
                "salt": _b64.b64encode(salt).decode(),
                "data": ciphertext.decode(),
            }, f)
    else:
        with open(export_path, "wb") as f:
            f.write(plaintext)

    os.chmod(export_path, 0o600)
    _log_access("export", f"Export to {export_path} (encrypted={passphrase is not None})")
    return export_path


def import_data(import_path: str) -> dict:
    """Import previously exported data."""
    with open(import_path, "r", encoding="utf-8") as f:
        exported = json.load(f)

    if "data" not in exported:
        return {"error": "Invalid export file format"}

    finance_dir = get_finance_dir()
    imported = 0

    for rel_path, data in exported["data"].items():
        target = (finance_dir / rel_path).resolve()
        if not str(target).startswith(str(finance_dir.resolve())):
            continue  # skip paths that escape .finance/
        target.parent.mkdir(parents=True, exist_ok=True)
        save_json(target, data)
        imported += 1

    _log_access("import", f"Imported {imported} files from {import_path}")
    return {"imported_files": imported, "source": import_path}


# ── Data Deletion ────────────────────────────────────────────────────────────

def delete_all_data(confirm: bool = False) -> dict:
    """
    Delete ALL stored financial data. Requires confirm=True.
    This is the "right to be forgotten" — complete data wipe.
    """
    if not confirm:
        inventory = get_data_inventory()
        return {
            "action": "preview",
            "warning": "This will permanently delete all your financial data!",
            "files_to_delete": inventory.get("total_files", 0),
            "size_to_delete": inventory.get("total_size_human", "0 B"),
            "confirm_message": "Call delete_all_data(confirm=True) to proceed.",
        }

    finance_dir = get_finance_dir()
    if finance_dir.exists():
        shutil.rmtree(finance_dir)
        return {
            "action": "deleted",
            "message": "All financial data has been permanently deleted.",
        }
    return {"action": "nothing_to_delete"}


def delete_category(category: str, confirm: bool = False) -> dict:
    """Delete a specific data category (accounts, budgets, goals, etc.)."""
    finance_dir = get_finance_dir()
    target = finance_dir / category

    if not target.exists():
        return {"error": f"Category '{category}' not found"}

    if not confirm:
        file_count = sum(1 for _ in target.rglob("*.json"))
        return {
            "action": "preview",
            "category": category,
            "files_to_delete": file_count,
            "confirm_message": f"Call delete_category('{category}', confirm=True) to proceed.",
        }

    shutil.rmtree(target)
    _log_access("delete_category", f"Deleted category: {category}")
    return {"action": "deleted", "category": category}


# ── File Permission Hardening ─────────────────────────────────────────────────

def harden_permissions() -> dict:
    """
    Set .finance/ directory and file permissions to owner-only (700/600).
    Prevents other OS users on the same machine from reading your data.
    """
    finance_dir = get_finance_dir()
    if not finance_dir.exists():
        return {"status": "no_data"}

    hardened_dirs = 0
    hardened_files = 0

    for root, dirs, files in os.walk(finance_dir):
        root_path = Path(root)
        try:
            root_path.chmod(0o700)  # rwx for owner only
            hardened_dirs += 1
        except OSError:
            pass
        for f in files:
            fpath = root_path / f
            try:
                fpath.chmod(0o600)  # rw for owner only
                hardened_files += 1
            except OSError:
                pass

    # Log first (creates audit/access_log.json with default umask), then secure it too
    _log_access("harden_permissions", f"Set 700/600 on {hardened_dirs} dirs, {hardened_files} files")
    audit_log = ensure_subdir("audit") / "access_log.json"
    if audit_log.exists():
        try:
            audit_log.chmod(0o600)
            audit_log.parent.chmod(0o700)
        except OSError:
            pass

    return {
        "status": "hardened",
        "dirs_secured": hardened_dirs,
        "files_secured": hardened_files,
        "note": "Only your OS user can now read these files.",
    }


def check_permissions() -> dict:
    """Check whether .finance/ files have secure permissions."""
    finance_dir = get_finance_dir()
    if not finance_dir.exists():
        return {"status": "no_data"}

    insecure = []
    for root, dirs, files in os.walk(finance_dir):
        for f in files:
            fpath = Path(root) / f
            mode = fpath.stat().st_mode
            # Warn if group or other have any access
            if mode & (stat.S_IRGRP | stat.S_IWGRP | stat.S_IXGRP |
                       stat.S_IROTH | stat.S_IWOTH | stat.S_IXOTH):
                insecure.append(str(fpath.relative_to(finance_dir)))

    if insecure:
        return {
            "status": "insecure",
            "insecure_files": insecure,
            "fix": "Call harden_permissions() to restrict access to owner only.",
        }
    return {"status": "secure", "message": "All .finance/ files are owner-only."}


# ── Git Guard ─────────────────────────────────────────────────────────────────

_GITIGNORE_ENTRY = "# Finance Assistant — personal financial data (never commit)\n.finance/\n"


def ensure_gitignore_protection(project_dir: Optional[str] = None) -> dict:
    """
    Add .finance/ to .gitignore in the project directory.
    Prevents accidental git commit of personal financial data.
    """
    if project_dir:
        search_dir = Path(project_dir)
    else:
        # Walk up from .finance/ to find repo root
        finance_dir = get_finance_dir()
        search_dir = finance_dir.parent

    gitignore = search_dir / ".gitignore"

    if gitignore.exists():
        content = gitignore.read_text(encoding="utf-8")
        if ".finance/" in content:
            return {"status": "already_protected", "path": str(gitignore)}
        with open(gitignore, "a", encoding="utf-8") as f:
            f.write(f"\n{_GITIGNORE_ENTRY}")
        return {"status": "added", "path": str(gitignore)}
    else:
        gitignore.write_text(_GITIGNORE_ENTRY, encoding="utf-8")
        return {"status": "created", "path": str(gitignore)}


# ── Encryption at Rest ───────────────────────────────────────────────────────

def _check_passphrase_strength(passphrase: str) -> None:
    """
    Reject obviously weak passphrases before encrypting.
    A strong passphrase is the only protection on the AES key.
    """
    if len(passphrase) < 12:
        raise ValueError(
            f"Passphrase too short ({len(passphrase)} chars). Use at least 12 characters."
        )
    has_upper = any(c.isupper() for c in passphrase)
    has_lower = any(c.islower() for c in passphrase)
    has_digit = any(c.isdigit() for c in passphrase)
    has_special = any(not c.isalnum() for c in passphrase)
    score = sum([has_upper, has_lower, has_digit, has_special])
    if score < 2:
        raise ValueError(
            "Passphrase is too simple. Use a mix of uppercase, lowercase, digits, "
            "and symbols — or a long random phrase (≥ 4 words)."
        )


def encrypt_file(file_path: str, passphrase: str) -> str:
    """
    Encrypt a JSON file using Fernet (AES-128-CBC + HMAC-SHA256) with a
    random 16-byte salt and 480,000 PBKDF2 iterations.
    The salt is stored with the ciphertext so decryption only needs the passphrase.
    """
    if not _CRYPTO_AVAILABLE:
        raise RuntimeError(
            "Encryption requires the 'cryptography' package. "
            "Install it with: pip install cryptography"
        )

    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    # Check if already encrypted
    try:
        with open(path) as f:
            existing = json.load(f)
        if existing.get("_encrypted") == "fernet":
            return str(path)  # Already encrypted
    except (json.JSONDecodeError, UnicodeDecodeError):
        pass

    _check_passphrase_strength(passphrase)

    salt = _os.urandom(16)  # Fresh random salt per file
    key = _derive_fernet_key(passphrase, salt)
    fernet = Fernet(key)

    with open(path, "rb") as f:
        plaintext = f.read()

    ciphertext = fernet.encrypt(plaintext)
    encrypted_payload = json.dumps({
        "_encrypted": "fernet",
        "salt": _b64.b64encode(salt).decode(),
        "data": ciphertext.decode(),
    }).encode()

    # Atomic write: write to temp file first, then rename.
    # This prevents a half-written file if the process is interrupted.
    tmp = path.with_suffix(".enc.tmp")
    try:
        with open(tmp, "wb") as f:
            f.write(encrypted_payload)
        tmp.replace(path)  # Atomic on POSIX
    except Exception:
        tmp.unlink(missing_ok=True)
        raise

    path.chmod(0o600)  # Harden on the way out
    return str(path)


def decrypt_file(file_path: str, passphrase: str) -> str:
    """Decrypt a Fernet-encrypted JSON file."""
    if not _CRYPTO_AVAILABLE:
        raise RuntimeError("Decryption requires the 'cryptography' package.")

    path = Path(file_path)
    with open(path, "r", encoding="utf-8") as f:
        content = json.load(f)

    if content.get("_encrypted") != "fernet":
        return str(path)  # Not encrypted or different scheme

    salt = _b64.b64decode(content["salt"])
    key = _derive_fernet_key(passphrase, salt)
    fernet = Fernet(key)

    try:
        plaintext = fernet.decrypt(content["data"].encode())
    except InvalidToken:
        raise ValueError("Wrong passphrase or corrupted file.")

    with open(path, "wb") as f:
        f.write(plaintext)

    return str(path)


def encrypt_sensitive_files(passphrase: str) -> dict:
    """
    Encrypt sensitive financial data files using Fernet AES encryption.
    Covers profile, accounts, transactions, investments, and debt files.
    Also hardens file permissions to 600 after encryption.
    """
    if not _CRYPTO_AVAILABLE:
        return {
            "error": "cryptography package not installed",
            "fix": "pip install cryptography",
        }

    finance_dir = get_finance_dir()
    encrypted_files = []

    # All files containing personal financial data
    sensitive_patterns = [
        "finance_profile.json",
        "accounts/accounts.json",
        "accounts/transactions/*.json",
        "investments/portfolio.json",
        "debt/debts.json",
        "goals/goals.json",
        "insurance/policies.json",
        "taxes/**/*.json",
    ]

    for pattern in sensitive_patterns:
        for path in finance_dir.glob(pattern):
            if not path.is_file():
                continue
            encrypt_file(str(path), passphrase)
            encrypted_files.append(str(path.relative_to(finance_dir)))

    harden_permissions()  # Secure file system permissions too
    _log_access("encrypt", f"Encrypted {len(encrypted_files)} files")
    return {"encrypted_count": len(encrypted_files), "files": encrypted_files}


def decrypt_sensitive_files(passphrase: str) -> dict:
    """Decrypt all encrypted data files."""
    finance_dir = get_finance_dir()
    decrypted_files = []

    for path in finance_dir.rglob("*.json"):
        try:
            with open(path) as f:
                data = json.load(f)
            if data.get("_encrypted"):
                decrypt_file(str(path), passphrase)
                decrypted_files.append(str(path.relative_to(finance_dir)))
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue

    _log_access("decrypt", f"Decrypted {len(decrypted_files)} files")
    return {"decrypted_count": len(decrypted_files), "files": decrypted_files}


# ── Sanitization ─────────────────────────────────────────────────────────────

def sanitize_for_sharing(data: dict) -> dict:
    """
    Remove personally identifiable information from data before sharing.
    Useful for getting help without exposing personal details.
    """
    sanitized = json.loads(json.dumps(data))  # deep copy

    pii_keys = {"name", "city", "email", "phone", "address", "employer",
                "provider", "institution", "payee", "description"}

    def _redact(obj, depth=0):
        if depth > 10:
            return obj
        if isinstance(obj, dict):
            for key in list(obj.keys()):
                if any(pii in key.lower() for pii in pii_keys):
                    if isinstance(obj[key], str):
                        obj[key] = "[REDACTED]"
                elif isinstance(obj[key], (dict, list)):
                    _redact(obj[key], depth + 1)
        elif isinstance(obj, list):
            for item in obj:
                if isinstance(item, (dict, list)):
                    _redact(item, depth + 1)
        return obj

    return _redact(sanitized)


# ── Access Logging ───────────────────────────────────────────────────────────

def _log_access(action: str, detail: str) -> None:
    """Log data access for audit purposes."""
    log_path = ensure_subdir("audit") / "access_log.json"
    log = load_json(log_path, default={"entries": []})
    log["entries"].append({
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "detail": detail,
    })
    # Keep last 1000 entries
    log["entries"] = log["entries"][-1000:]
    save_json(log_path, log)


def get_access_log(limit: int = 50) -> list[dict]:
    """Return recent access log entries."""
    log_path = ensure_subdir("audit") / "access_log.json"
    log = load_json(log_path, default={"entries": []})
    return log.get("entries", [])[-limit:]


# ── Privacy Summary ──────────────────────────────────────────────────────────

def get_privacy_summary() -> str:
    """Return a human-readable privacy and data safety summary."""
    inventory = get_data_inventory()
    perm_check = check_permissions()
    enc_available = "yes (AES-128-CBC + HMAC-SHA256)" if _CRYPTO_AVAILABLE else "no — run: pip install cryptography"

    lines = [
        "═══ Data Safety Summary ═══\n",
        "Where your data lives:",
        f"  Location: {inventory.get('base_path', 'not initialized')}",
        f"  Files: {inventory.get('total_files', 0)}",
        f"  Size: {inventory.get('total_size_human', '0 B')}",
        f"  File permissions: {perm_check['status']}",
        f"  Encryption available: {enc_available}\n",
        "What we NEVER store:",
        "  - Bank login credentials, passwords, PINs, TANs",
        "  - Full IBAN or credit card numbers",
        "  - Tax IDs, passport numbers, SSNs",
        "  - Raw bank API tokens or access credentials\n",
        "What we store (structured summaries only):",
        "  - Account names and balances (not account numbers)",
        "  - Transaction amounts, dates, and categories",
        "  - Budget plans and goal targets",
        "  - Investment holdings and performance",
        "  - Debt balances and interest rates\n",
        "Your controls:",
        "  - Encrypt data:        encrypt_sensitive_files(passphrase)  [Fernet AES]",
        "  - Harden permissions:  harden_permissions()                 [chmod 600/700]",
        "  - Git guard:           ensure_gitignore_protection()        [.finance/ in .gitignore]",
        "  - Check permissions:   check_permissions()",
        "  - Export data:         export_all_data()",
        "  - Delete everything:   delete_all_data(confirm=True)",
        "  - Delete category:     delete_category('accounts', confirm=True)",
        "  - Sanitize for sharing: sanitize_for_sharing(data)",
        "  - View access log:     get_access_log()",
        "",
        "All data stays on your machine. Nothing is ever uploaded.",
    ]
    return "\n".join(lines)
