"""
Finance Assistant PDF Statement Importer.

Parses PDF bank statements (DKB, ING-DiBa, generic) using pdfplumber
and returns a list of transaction dicts compatible with the import pipeline.

Usage:
    from pdf_importer import parse_pdf, detect_pdf_bank
    transactions = parse_pdf("statement.pdf", currency="EUR")
"""

from __future__ import annotations

import re
from datetime import datetime
from typing import Optional


# ── Dependency guard ──────────────────────────────────────────────────────────

try:
    import pdfplumber  # noqa: F401
    _PDFPLUMBER_AVAILABLE = True
except ImportError:
    _PDFPLUMBER_AVAILABLE = False


def _require_pdfplumber() -> None:
    if not _PDFPLUMBER_AVAILABLE:
        raise ImportError(
            "pdfplumber is required for PDF import but is not installed. "
            "Run: pip install pdfplumber"
        )


# ── Bank detection ────────────────────────────────────────────────────────────

# Patterns used to identify the bank from the first page of text
_BANK_SIGNATURES: list[tuple[str, str]] = [
    # (regex_pattern, bank_name)
    (r"DKB\s*-?\s*Deutsche\s*Kreditbank|DKB\s*AG", "dkb"),
    (r"ING[-\s]DiBa|ING\s+Deutschland", "ing"),
    (r"Commerzbank", "commerzbank"),
    (r"Deutsche\s+Bank", "deutsche_bank"),
    (r"Sparkasse", "sparkasse"),
    (r"Volksbank|Raiffeisenbank", "volksbank"),
    (r"Postbank", "postbank"),
    (r"N26\s+Bank|N26\s+GmbH", "n26"),
]


def detect_pdf_bank(text: str) -> str:
    """
    Detect which bank issued the PDF from its text content.

    Returns a short bank identifier string ("dkb", "ing", etc.)
    or "generic" if no known bank is detected.
    """
    for pattern, bank in _BANK_SIGNATURES:
        if re.search(pattern, text, re.IGNORECASE):
            return bank
    return "generic"


# ── Amount parsing helpers ────────────────────────────────────────────────────

def _parse_german_amount(raw: str) -> Optional[float]:
    """
    Parse a German-formatted amount string like "1.234,56" or "-1.234,56".

    Returns a float (negative = debit) or None on failure.
    """
    raw = raw.strip().replace("\xa0", "").replace(" ", "")
    # Strip currency symbols
    raw = re.sub(r"[€$£]", "", raw)
    # Determine sign from trailing +/- or explicit leading -
    negative = False
    if raw.endswith("-"):
        negative = True
        raw = raw[:-1]
    elif raw.endswith("+"):
        raw = raw[:-1]
    elif raw.startswith("-"):
        negative = True
        raw = raw[1:]

    # German format: periods as thousands separator, comma as decimal
    if "," in raw:
        raw = raw.replace(".", "").replace(",", ".")
    else:
        # Plain integer or already dot-decimal
        raw = raw.replace(",", "")

    try:
        value = float(raw)
        return -value if negative else value
    except ValueError:
        return None


def _parse_date(raw: str) -> Optional[str]:
    """
    Attempt to parse common date formats into ISO 8601 (YYYY-MM-DD).
    Handles DD.MM.YYYY, DD.MM.YY, YYYY-MM-DD, DD/MM/YYYY.
    """
    formats = [
        ("%d.%m.%Y", r"\d{2}\.\d{2}\.\d{4}"),
        ("%d.%m.%y", r"\d{2}\.\d{2}\.\d{2}"),
        ("%Y-%m-%d", r"\d{4}-\d{2}-\d{2}"),
        ("%d/%m/%Y", r"\d{2}/\d{2}/\d{4}"),
    ]
    for fmt, _ in formats:
        try:
            return datetime.strptime(raw.strip(), fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return None


# ── DKB parser ────────────────────────────────────────────────────────────────

# DKB Giro statement columns:
# Buchungstag | Wertstellung | Gläubiger-ID | Auftraggeber... | Verwendungszweck | Konto | BLZ | Betrag | Gläubiger-ID | Mandatsreferenz | Kundenreferenz

_DKB_ROW_RE = re.compile(
    r"^(?P<date>\d{2}\.\d{2}\.\d{4})"         # Buchungstag
    r"\s+(?P<value_date>\d{2}\.\d{2}\.\d{4})"  # Wertstellung
    r"\s+(?P<payee>.+?)"                        # Auftraggeber/Payee (non-greedy)
    r"\s+(?P<desc>.+?)"                         # Verwendungszweck
    r"\s+(?P<amount>-?[\d.,]+[+-]?)\s*$",       # Betrag
    re.MULTILINE,
)


def _parse_dkb(pages: list) -> list[dict]:
    """Parse DKB Girocard / credit card PDF pages."""
    transactions: list[dict] = []

    for page in pages:
        # Extract table rows (pdfplumber table extraction)
        tables = page.extract_tables()
        for table in tables:
            for row in table:
                if not row or len(row) < 4:
                    continue
                # Skip header rows
                first = (row[0] or "").strip()
                if not re.match(r"\d{2}\.\d{2}\.\d{4}", first):
                    continue

                date_iso = _parse_date(first)
                if not date_iso:
                    continue

                # DKB table: col 0=date, col 1=value_date, col 2=payee, col 3=desc, last=amount
                payee = (row[2] or "").strip()
                desc = (row[3] or "").strip()
                amount_raw = (row[-1] or "").strip()

                amount = _parse_german_amount(amount_raw)
                if amount is None:
                    continue

                description = f"{payee} — {desc}" if desc else payee
                transactions.append({
                    "date": date_iso,
                    "amount": amount,
                    "description": description,
                    "currency": "EUR",
                })

    return transactions


# ── ING-DiBa parser ───────────────────────────────────────────────────────────

def _parse_ing(pages: list) -> list[dict]:
    """Parse ING-DiBa bank statement pages."""
    transactions: list[dict] = []

    for page in pages:
        tables = page.extract_tables()
        for table in tables:
            for row in table:
                if not row or len(row) < 3:
                    continue
                first = (row[0] or "").strip()
                if not re.match(r"\d{2}\.\d{2}\.\d{4}", first):
                    continue

                date_iso = _parse_date(first)
                if not date_iso:
                    continue

                # ING layout: Buchung | Auftraggeber/Empfänger | Verwendungszweck | Betrag
                # Columns may vary; look for the rightmost numeric-looking cell as amount
                amount = None
                for cell in reversed(row):
                    if cell and re.search(r"[\d,]+", str(cell)):
                        parsed = _parse_german_amount(str(cell))
                        if parsed is not None:
                            amount = parsed
                            break

                if amount is None:
                    continue

                # Payee in col 1, description in col 2
                payee = (row[1] or "").strip() if len(row) > 1 else ""
                desc = (row[2] or "").strip() if len(row) > 2 else ""
                description = f"{payee} — {desc}" if (payee and desc) else payee or desc

                transactions.append({
                    "date": date_iso,
                    "amount": amount,
                    "description": description,
                    "currency": "EUR",
                })

    return transactions


# ── Generic fallback parser ───────────────────────────────────────────────────

# Matches lines like: "15.03.2024  Supermarkt REWE  -45,60"
_GENERIC_LINE_RE = re.compile(
    r"(?P<date>\d{2}[./]\d{2}[./]\d{2,4})"
    r"[^\d\-+]*"
    r"(?P<desc>[A-Za-zÄÖÜäöüß][\w\s\-./,&()']{3,60}?)"
    r"\s+"
    r"(?P<amount>-?[\d]+[.,][\d]{2}[+-]?)",
)


def _parse_generic(pages: list) -> list[dict]:
    """
    Generic regex-based fallback parser.

    Scans each text line for a date + description + amount pattern.
    Works on many European bank statements without dedicated support.
    """
    transactions: list[dict] = []

    for page in pages:
        text = page.extract_text() or ""
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            m = _GENERIC_LINE_RE.search(line)
            if not m:
                continue

            date_iso = _parse_date(m.group("date"))
            if not date_iso:
                continue

            amount = _parse_german_amount(m.group("amount"))
            if amount is None:
                continue

            description = m.group("desc").strip()
            transactions.append({
                "date": date_iso,
                "amount": amount,
                "description": description,
                "currency": "EUR",
            })

    return transactions


# ── Public API ────────────────────────────────────────────────────────────────

_BANK_PARSERS = {
    "dkb": _parse_dkb,
    "ing": _parse_ing,
}


def parse_pdf(
    file_path: str,
    currency: str = "EUR",
    bank_hint: Optional[str] = None,
) -> list[dict]:
    """
    Parse a PDF bank statement and return a list of transaction dicts.

    Each dict has the keys:
        date        : "YYYY-MM-DD"
        amount      : float  (positive = credit/income, negative = debit/expense)
        description : str
        currency    : str    (defaults to the currency argument)

    Args:
        file_path : Path to the PDF file.
        currency  : ISO 4217 currency code used when the PDF doesn't specify one.
        bank_hint : Optional bank identifier to skip auto-detection.
                    Accepted values: "dkb", "ing", "generic".

    Raises:
        ImportError : If pdfplumber is not installed.
        FileNotFoundError : If the PDF does not exist.
    """
    _require_pdfplumber()

    import pdfplumber  # noqa: F811 (shadowed locally after guard)

    with pdfplumber.open(file_path) as pdf:
        pages = pdf.pages

        if not pages:
            return []

        # Detect bank from first-page text (or honour caller hint)
        if bank_hint:
            bank = bank_hint
        else:
            first_text = pages[0].extract_text() or ""
            bank = detect_pdf_bank(first_text)

        parser = _BANK_PARSERS.get(bank, _parse_generic)
        transactions = parser(pages)

        # If dedicated parser returned nothing, fall back to generic
        if not transactions and bank != "generic":
            transactions = _parse_generic(pages)

    # Normalise currency on all rows
    for txn in transactions:
        if not txn.get("currency"):
            txn["currency"] = currency

    # Sort by date ascending (best effort)
    transactions.sort(key=lambda t: t.get("date", ""))

    return transactions
