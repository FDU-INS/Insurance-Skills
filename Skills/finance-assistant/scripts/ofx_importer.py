"""
OFX/QFX file importer.

OFX (Open Financial Exchange) is used by many US and international banks.
This parser handles both SGML-style OFX 1.x and XML-style OFX 2.x.
"""

from __future__ import annotations

import re
from datetime import datetime


def parse_ofx(file_path: str) -> list[dict]:
    """Parse an OFX/QFX file. Returns list of raw transaction dicts."""
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    transactions = []
    currency = _extract_tag(content, "CURDEF") or "USD"

    # Find all STMTTRN blocks
    txn_blocks = re.findall(
        r"<STMTTRN>(.*?)</STMTTRN>",
        content,
        re.DOTALL | re.IGNORECASE,
    )

    # Also handle SGML-style (no closing tags)
    if not txn_blocks:
        txn_blocks = re.findall(
            r"<STMTTRN>(.*?)(?=<STMTTRN>|</BANKTRANLIST|</STMTTRNRS|$)",
            content,
            re.DOTALL | re.IGNORECASE,
        )

    for block in txn_blocks:
        trntype = _extract_tag(block, "TRNTYPE") or ""
        date_str = _extract_tag(block, "DTPOSTED") or ""
        amount_str = _extract_tag(block, "TRNAMT") or "0"
        name = _extract_tag(block, "NAME") or ""
        memo = _extract_tag(block, "MEMO") or ""
        fitid = _extract_tag(block, "FITID") or ""

        # Parse date (YYYYMMDD or YYYYMMDDHHMMSS)
        iso_date = _parse_ofx_date(date_str)

        # Parse amount
        try:
            amount = float(amount_str.replace(",", ""))
        except ValueError:
            amount = 0.0

        description = f"{name} {memo}".strip() if memo and memo != name else name

        transactions.append({
            "date": iso_date,
            "amount": round(amount, 2),
            "description": description,
            "payee": name,
            "currency": currency,
            "type": _map_trntype(trntype),
            "import_ref": f"ofx:{fitid}" if fitid else None,
        })

    return transactions


def _extract_tag(text: str, tag: str) -> str | None:
    """Extract value of an OFX tag (handles both SGML and XML style)."""
    # XML style: <TAG>value</TAG>
    match = re.search(rf"<{tag}>(.*?)</{tag}>", text, re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1).strip()

    # SGML style: <TAG>value\n
    match = re.search(rf"<{tag}>([^\n<]+)", text, re.IGNORECASE)
    if match:
        return match.group(1).strip()

    return None


def _parse_ofx_date(date_str: str) -> str:
    """Parse OFX date format to ISO."""
    if not date_str:
        return ""
    # Remove timezone info if present
    date_str = re.sub(r"\[.*?\]", "", date_str).strip()
    for fmt, length in (("%Y%m%d%H%M%S", 14), ("%Y%m%d%H%M", 12), ("%Y%m%d", 8)):
        try:
            return datetime.strptime(date_str[:length], fmt).date().isoformat()
        except ValueError:
            continue
    return date_str[:10]


def _map_trntype(trntype: str) -> str:
    """Map OFX transaction type to our type system."""
    trntype = trntype.upper()
    income_types = {"CREDIT", "DEP", "DIRECTDEP", "INT", "DIV"}
    if trntype in income_types:
        return "income"
    return "expense"
