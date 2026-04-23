"""
CSV bank statement importer.

Supports auto-detection of common German and international bank formats.
Falls back to generic column-position-based parsing.
"""

from __future__ import annotations

import csv
import os
import re
from datetime import datetime
from typing import Optional


# ── Known bank formats ───────────────────────────────────────────────────────

KNOWN_FORMATS = {
    "dkb": {
        "detect": ["Buchungsdatum", "Wertstellung", "Betrag (EUR)"],
        "date": "Buchungsdatum",
        "amount": "Betrag (EUR)",
        "description": "Verwendungszweck",
        "payee": "Auftraggeber / Begünstigter",
        "date_format": "%d.%m.%Y",
        "delimiter": ";",
        "encoding": "latin-1",
        "decimal": ",",
    },
    "ing": {
        "detect": ["Buchung", "Valuta", "Betrag"],
        "date": "Buchung",
        "amount": "Betrag",
        "description": "Verwendungszweck",
        "payee": "Auftraggeber/Empfänger",
        "date_format": "%d.%m.%Y",
        "delimiter": ";",
        "encoding": "latin-1",
        "decimal": ",",
    },
    "sparkasse": {
        "detect": ["Buchungstag", "Wertstellung", "Betrag"],
        "date": "Buchungstag",
        "amount": "Betrag",
        "description": "Verwendungszweck",
        "payee": "Beguenstigter/Zahlungspflichtiger",
        "date_format": "%d.%m.%y",
        "delimiter": ";",
        "encoding": "latin-1",
        "decimal": ",",
    },
    "n26": {
        "detect": ["Date", "Payee", "Amount (EUR)"],
        "date": "Date",
        "amount": "Amount (EUR)",
        "description": "Payment reference",
        "payee": "Payee",
        "date_format": "%Y-%m-%d",
        "delimiter": ",",
        "encoding": "utf-8",
        "decimal": ".",
    },
    "wise": {
        "detect": ["TransferWise ID", "Date", "Amount"],
        "date": "Date",
        "amount": "Amount",
        "description": "Description",
        "payee": "Merchant",
        "date_format": "%d-%m-%Y",
        "delimiter": ",",
        "encoding": "utf-8",
        "decimal": ".",
    },
    "revolut": {
        "detect": ["Type", "Started Date", "Amount"],
        "date": "Started Date",
        "amount": "Amount",
        "description": "Description",
        "payee": "Description",
        "date_format": "%Y-%m-%d %H:%M:%S",
        "delimiter": ",",
        "encoding": "utf-8",
        "decimal": ".",
    },
    "commerzbank": {
        "detect": ["Buchungstag", "Wertstellung", "Umsatzart"],
        "date": "Buchungstag",
        "amount": "Betrag",
        "description": "Buchungstext",
        "payee": "Auftraggeber / Begünstigter",
        "date_format": "%d.%m.%Y",
        "delimiter": ";",
        "encoding": "latin-1",
        "decimal": ",",
    },
}


def detect_bank_format(file_path: str) -> Optional[str]:
    """Detect which bank format a CSV is from by checking headers."""
    for enc in ("utf-8", "latin-1", "cp1252"):
        try:
            with open(file_path, "r", encoding=enc) as f:
                # Read first few lines, skip potential metadata rows
                lines = []
                for _ in range(15):
                    line = f.readline()
                    if line:
                        lines.append(line.strip())

            # Check each line for header matches
            for line in lines:
                for bank_name, fmt in KNOWN_FORMATS.items():
                    detect_cols = fmt["detect"]
                    if all(col in line for col in detect_cols):
                        return bank_name
        except (UnicodeDecodeError, IOError):
            continue
    return None


def _parse_amount(value: str, decimal: str = ",") -> float:
    """Parse a potentially German-formatted number."""
    if not value:
        return 0.0
    value = value.strip().strip('"')
    if decimal == ",":
        value = value.replace(".", "").replace(",", ".")
    else:
        value = value.replace(",", "")
    try:
        return float(value)
    except ValueError:
        return 0.0


def _parse_date(value: str, fmt: str = "%d.%m.%Y") -> str:
    """Parse date string to ISO format."""
    value = value.strip().strip('"')
    try:
        dt = datetime.strptime(value, fmt)
        return dt.date().isoformat()
    except ValueError:
        # Try common alternatives
        for alt_fmt in ("%Y-%m-%d", "%d.%m.%Y", "%d/%m/%Y", "%m/%d/%Y", "%d-%m-%Y"):
            try:
                dt = datetime.strptime(value[:10], alt_fmt)
                return dt.date().isoformat()
            except ValueError:
                continue
    return value[:10]  # Best effort


def parse_csv(
    file_path: str,
    bank_format: Optional[str] = None,
    currency: str = "EUR",
    date_format: Optional[str] = None,
) -> list[dict]:
    """Parse a bank CSV file. Returns list of raw transaction dicts."""
    bank_format = bank_format or detect_bank_format(file_path)

    if bank_format and bank_format in KNOWN_FORMATS:
        return _parse_known_format(file_path, KNOWN_FORMATS[bank_format], currency)

    return _parse_generic(file_path, currency, date_format)


def _parse_known_format(file_path: str, fmt: dict, currency: str) -> list[dict]:
    """Parse using a known bank format definition."""
    encoding = fmt.get("encoding", "utf-8")
    delimiter = fmt.get("delimiter", ",")
    decimal = fmt.get("decimal", ".")
    dfmt = fmt.get("date_format", "%Y-%m-%d")

    transactions = []

    with open(file_path, "r", encoding=encoding, errors="replace") as f:
        content = f.read()

    # Find the header row
    lines = content.split("\n")
    header_idx = None
    for i, line in enumerate(lines):
        if fmt["detect"][0] in line:
            header_idx = i
            break

    if header_idx is None:
        return []

    # Parse from header row onwards
    csv_lines = "\n".join(lines[header_idx:])
    reader = csv.DictReader(csv_lines.splitlines(), delimiter=delimiter)

    for row in reader:
        date_val = row.get(fmt["date"], "")
        amount_val = row.get(fmt["amount"], "")
        desc_val = row.get(fmt.get("description", ""), "")
        payee_val = row.get(fmt.get("payee", ""), "")

        if not date_val or not amount_val:
            continue

        amount = _parse_amount(amount_val, decimal)
        transactions.append({
            "date": _parse_date(date_val, dfmt),
            "amount": round(amount, 2),
            "description": (desc_val or "").strip(),
            "payee": (payee_val or "").strip(),
            "currency": currency,
            "raw": dict(row),
        })

    return transactions


def _parse_generic(file_path: str, currency: str, date_format: Optional[str] = None) -> list[dict]:
    """Fallback: parse a generic CSV by guessing columns."""
    transactions = []

    for enc in ("utf-8", "latin-1", "cp1252"):
        try:
            with open(file_path, "r", encoding=enc) as f:
                # Try both comma and semicolon
                sample = f.read(4000)
                delimiter = ";" if sample.count(";") > sample.count(",") else ","
                f.seek(0)
                reader = csv.reader(f, delimiter=delimiter)
                rows = list(reader)
            break
        except UnicodeDecodeError:
            continue
    else:
        return []

    if len(rows) < 2:
        return []

    headers = [h.strip().lower() for h in rows[0]]

    # Guess column indices
    date_col = _find_col(headers, ["date", "datum", "buchungsdatum", "buchung", "buchungstag", "started date"])
    amount_col = _find_col(headers, ["amount", "betrag", "betrag (eur)", "amount (eur)", "value"])
    desc_col = _find_col(headers, ["description", "verwendungszweck", "buchungstext", "payment reference", "memo"])
    payee_col = _find_col(headers, ["payee", "auftraggeber", "empfänger", "begünstigter", "merchant", "name"])

    if date_col is None or amount_col is None:
        return []

    dfmt = date_format or "%d.%m.%Y"

    for row in rows[1:]:
        if len(row) <= max(date_col, amount_col):
            continue
        date_val = row[date_col].strip()
        amount_val = row[amount_col].strip()
        if not date_val or not amount_val:
            continue

        # Guess decimal format
        decimal = "," if "," in amount_val and "." not in amount_val else "."
        amount = _parse_amount(amount_val, decimal)

        desc = row[desc_col].strip() if desc_col is not None and desc_col < len(row) else ""
        payee = row[payee_col].strip() if payee_col is not None and payee_col < len(row) else ""

        transactions.append({
            "date": _parse_date(date_val, dfmt),
            "amount": round(amount, 2),
            "description": desc,
            "payee": payee,
            "currency": currency,
        })

    return transactions


def _find_col(headers: list[str], candidates: list[str]) -> Optional[int]:
    for i, h in enumerate(headers):
        for c in candidates:
            if c in h:
                return i
    return None
