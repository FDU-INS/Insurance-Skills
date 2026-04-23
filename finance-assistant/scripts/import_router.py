"""
Finance Assistant Import Router.

Detects file format and routes to the appropriate parser.
Supports CSV (bank statements), MT940, and OFX/QFX.
"""

from __future__ import annotations

import os
from datetime import datetime
from typing import Optional

try:
    from finance_storage import get_import_log_path, load_json, save_json
    from transaction_logger import add_transaction, deduplicate, get_transactions
except ImportError:
    import sys
    sys.path.insert(0, os.path.dirname(__file__))
    from finance_storage import get_import_log_path, load_json, save_json
    from transaction_logger import add_transaction, deduplicate, get_transactions


def detect_format(file_path: str) -> str:
    """Detect file format from extension and content sniffing."""
    ext = os.path.splitext(file_path)[1].lower()

    if ext in (".ofx", ".qfx"):
        return "ofx"
    if ext == ".mt940" or ext == ".sta":
        return "mt940"
    if ext == ".csv":
        return "csv"
    if ext == ".pdf":
        return "pdf"
    if ext in (".jpg", ".jpeg", ".png", ".webp"):
        return "image"

    # Content sniffing
    try:
        with open(file_path, "rb") as f:
            header_bytes = f.read(8)
        if header_bytes.startswith(b"%PDF"):
            return "pdf"
        first_lines = header_bytes.decode("utf-8", errors="replace")
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            first_lines = f.read(2000)
        if "OFXHEADER" in first_lines or "<OFX>" in first_lines:
            return "ofx"
        if first_lines.startswith(":20:") or ":60F:" in first_lines:
            return "mt940"
        if "," in first_lines or ";" in first_lines or "\t" in first_lines:
            return "csv"
    except Exception:
        pass

    return "unknown"


def import_file(
    file_path: str,
    account_id: str,
    format_hint: Optional[str] = None,
    currency: str = "EUR",
    dry_run: bool = True,
) -> dict:
    """Import transactions from a file. Returns preview or import result."""
    fmt = format_hint or detect_format(file_path)

    if fmt == "csv":
        from csv_importer import parse_csv
        raw = parse_csv(file_path, currency=currency)
    elif fmt == "mt940":
        from mt940_importer import parse_mt940
        raw = parse_mt940(file_path)
    elif fmt == "ofx":
        from ofx_importer import parse_ofx
        raw = parse_ofx(file_path)
    elif fmt == "pdf":
        from pdf_importer import parse_pdf
        raw = parse_pdf(file_path, currency=currency)
    elif fmt == "image":
        from receipt_scanner import scan_to_transaction
        txn = scan_to_transaction(file_path, account_id)
        if "error" in txn.get("scan_result", {}):
            return {
                "error": txn["scan_result"]["error"],
                "file": file_path,
                "format": "image",
            }
        result = {
            "file": os.path.basename(file_path),
            "format": "image",
            "account_id": account_id,
            "currency": txn.get("currency", currency),
            "total_parsed": 1,
            "total_normalized": 1,
            "duplicates_removed": 0,
            "to_import": 1,
            "preview": [txn],
            "dry_run": dry_run,
            "scan_confidence": txn.get("scan_result", {}).get("confidence", "low"),
        }
        if not dry_run:
            add_transaction(
                date=txn["date"],
                type=txn.get("type", "expense"),
                amount=txn["amount"],
                category=txn.get("category", "other_expense"),
                description=txn.get("description", ""),
                account_id=account_id,
                currency=txn.get("currency", currency),
                payee=txn.get("payee", ""),
                tags=txn.get("tags", []),
                import_source="image",
            )
            result["imported"] = 1
            result["dry_run"] = False
        return result
    else:
        return {"error": f"Unknown format: {fmt}", "file": file_path}

    from transaction_normalizer import normalize_transactions
    normalized = normalize_transactions(raw, account_id, fmt, currency)

    # Deduplicate against existing
    year = datetime.now().year
    if normalized:
        try:
            first_date = normalized[0].get("date", "")
            year = int(first_date[:4]) if first_date else year
        except (ValueError, IndexError):
            pass
    existing = get_transactions(account_id=account_id, year=year)
    unique = deduplicate(normalized, existing)

    result = {
        "file": os.path.basename(file_path),
        "format": fmt,
        "account_id": account_id,
        "currency": currency,
        "total_parsed": len(raw),
        "total_normalized": len(normalized),
        "duplicates_removed": len(normalized) - len(unique),
        "to_import": len(unique),
        "preview": unique[:10],
        "dry_run": dry_run,
    }

    if not dry_run and unique:
        imported = 0
        for txn in unique:
            add_transaction(
                date=txn["date"],
                type=txn.get("type", "expense"),
                amount=txn["amount"],
                category=txn.get("category", "other_expense"),
                description=txn.get("description", ""),
                account_id=account_id,
                currency=txn.get("currency", currency),
                import_source=fmt,
                import_ref=txn.get("import_ref"),
            )
            imported += 1
        result["imported"] = imported
        result["dry_run"] = False

        # Log import
        log = load_json(get_import_log_path(), default={"imports": []})
        log["imports"].append({
            "timestamp": datetime.now().isoformat(),
            "file": os.path.basename(file_path),
            "format": fmt,
            "account_id": account_id,
            "imported": imported,
        })
        save_json(get_import_log_path(), log)

    return result


def sync_bank(days_back: int = 90) -> dict:
    """
    Trigger: user says "sync bank" or "sync transactions".
    Pulls latest transactions from all linked GoCardless accounts.
    """
    try:
        from bank_sync import sync_all
    except ImportError:
        import sys
        sys.path.insert(0, os.path.dirname(__file__))
        from bank_sync import sync_all
    return sync_all(days_back=days_back)


def import_folder(
    folder_path: str,
    account_id: str = "default",
    dry_run: bool = True,
) -> dict:
    """Import all supported files from a folder."""
    results = []
    for entry in sorted(os.listdir(folder_path)):
        full_path = os.path.join(folder_path, entry)
        if not os.path.isfile(full_path):
            continue
        fmt = detect_format(full_path)
        if fmt != "unknown":
            result = import_file(full_path, account_id, format_hint=fmt, dry_run=dry_run)
            results.append(result)

    return {
        "folder": folder_path,
        "files_found": len(results),
        "results": results,
        "dry_run": dry_run,
    }
