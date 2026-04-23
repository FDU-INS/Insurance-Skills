"""
Finance Assistant Receipt Scanner.

OCR-based receipt processing using pytesseract + Pillow.
Extracts merchant, date, total, currency, and line items from receipt images.
"""

from __future__ import annotations

import os
import re
from datetime import datetime
from typing import Optional

# Graceful optional imports
try:
    from PIL import Image, ImageEnhance, ImageFilter, ImageOps
    _PIL_AVAILABLE = True
except ImportError:
    _PIL_AVAILABLE = False

try:
    import pytesseract
    _TESSERACT_AVAILABLE = True
except ImportError:
    _TESSERACT_AVAILABLE = False


# ── Language / number format detection ───────────────────────────────────────

_DE_INDICATORS = [
    "gesamt", "summe", "betrag", "mwst", "mehrwertsteuer", "eur",
    "danke", "quittung", "kassenbon", "rechnung", "rabatt",
    "preis", "artikel", "stück",
]

_CURRENCY_SYMBOLS = {
    "€": "EUR", "$": "USD", "£": "GBP", "CHF": "CHF", "SEK": "SEK",
    "NOK": "NOK", "DKK": "DKK", "PLN": "PLN", "CZK": "CZK",
}


def detect_language(text: str) -> str:
    """
    Detect language from OCR text.
    Returns "de" for German, "en" for English (default).
    """
    text_lower = text.lower()
    de_hits = sum(1 for kw in _DE_INDICATORS if kw in text_lower)
    return "de" if de_hits >= 2 else "en"


def _preprocess_image(image_path: str):
    """
    Preprocess image for better OCR accuracy.
    Steps: grayscale → contrast enhance → threshold (Otsu-like binarize).
    Returns a PIL Image object.
    """
    img = Image.open(image_path).convert("L")  # grayscale
    # Contrast enhancement
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2.0)
    # Sharpness
    img = img.filter(ImageFilter.SHARPEN)
    # Binarize with a fixed threshold (approximation of Otsu)
    img = img.point(lambda p: 255 if p > 140 else 0, "1")
    return img


def _parse_amount_de(text: str) -> Optional[float]:
    """Parse German number format: 1.234,56 → 1234.56"""
    # German: dots as thousands sep, comma as decimal
    match = re.search(r"(\d{1,3}(?:\.\d{3})*,\d{2})", text)
    if match:
        raw = match.group(1).replace(".", "").replace(",", ".")
        try:
            return float(raw)
        except ValueError:
            pass
    # Simple fallback: comma decimal
    match = re.search(r"(\d+),(\d{2})\b", text)
    if match:
        try:
            return float(f"{match.group(1)}.{match.group(2)}")
        except ValueError:
            pass
    return None


def _parse_amount_en(text: str) -> Optional[float]:
    """Parse English number format: 1,234.56 → 1234.56"""
    match = re.search(r"(\d{1,3}(?:,\d{3})*\.\d{2})", text)
    if match:
        raw = match.group(1).replace(",", "")
        try:
            return float(raw)
        except ValueError:
            pass
    # Simple fallback: dot decimal
    match = re.search(r"(\d+)\.(\d{2})\b", text)
    if match:
        try:
            return float(f"{match.group(1)}.{match.group(2)}")
        except ValueError:
            pass
    return None


def _parse_amount(text: str, lang: str) -> Optional[float]:
    if lang == "de":
        return _parse_amount_de(text)
    return _parse_amount_en(text)


def _detect_currency(text: str) -> str:
    """Detect currency symbol/code from text."""
    for symbol, code in _CURRENCY_SYMBOLS.items():
        if symbol in text:
            return code
    return "EUR"  # default


def _extract_date(text: str) -> str:
    """Extract date from receipt text. Returns ISO 8601 or empty string."""
    # Try common date patterns
    patterns = [
        (r"\b(\d{2})\.(\d{2})\.(\d{4})\b", "%d.%m.%Y"),   # 15.03.2025
        (r"\b(\d{4})-(\d{2})-(\d{2})\b", "%Y-%m-%d"),      # 2025-03-15
        (r"\b(\d{2})/(\d{2})/(\d{4})\b", "%d/%m/%Y"),       # 15/03/2025
        (r"\b(\d{2})-(\d{2})-(\d{4})\b", "%d-%m-%Y"),       # 15-03-2025
    ]
    for pattern, fmt in patterns:
        m = re.search(pattern, text)
        if m:
            try:
                if fmt == "%Y-%m-%d":
                    return m.group(0)
                else:
                    dt = datetime.strptime(m.group(0), fmt)
                    return dt.strftime("%Y-%m-%d")
            except ValueError:
                continue
    return ""


def _extract_merchant(lines: list[str]) -> str:
    """
    Heuristic: merchant name is usually in the first 3 non-empty lines.
    Pick the longest token that looks like a name (not a date, not pure digits).
    """
    candidates = []
    for line in lines[:5]:
        line = line.strip()
        if not line:
            continue
        # Skip lines that are mostly digits or look like dates/amounts
        if re.match(r"^[\d\s.,:/%-]+$", line):
            continue
        if len(line) >= 3:
            candidates.append(line)
    if candidates:
        return candidates[0][:60]
    return "Unknown"


def _extract_items(lines: list[str], lang: str) -> list[dict]:
    """
    Extract line items: lines with a description and an amount.
    Returns list of {"description": str, "amount": float}.
    """
    items = []
    # Pattern: "ITEM NAME   4.99" or "ITEM NAME   4,99"
    if lang == "de":
        amount_re = re.compile(r"(.+?)\s+(\d+[,\.]\d{2})\s*$")
    else:
        amount_re = re.compile(r"(.+?)\s+(\d+[,\.]\d{2})\s*$")

    for line in lines:
        line = line.strip()
        if not line:
            continue
        m = amount_re.match(line)
        if m:
            desc = m.group(1).strip()
            amt_str = m.group(2)
            # Skip total/sum lines
            skip_keywords = ["total", "summe", "gesamt", "summ", "mwst", "tax", "tip", "trinkgeld"]
            if any(kw in desc.lower() for kw in skip_keywords):
                continue
            amt = _parse_amount(amt_str, lang)
            if amt is not None and len(desc) >= 2:
                items.append({"description": desc, "amount": amt})
    return items


def _find_total(lines: list[str], lang: str) -> Optional[float]:
    """Find the total amount. Look for 'total', 'gesamt', 'summe', etc."""
    total_keywords_de = ["gesamt", "summe", "total", "endbetrag", "zu zahlen", "zu bezahlen", "betrag"]
    total_keywords_en = ["total", "amount due", "grand total", "subtotal", "balance due"]
    keywords = total_keywords_de + total_keywords_en

    # Look backwards from end for total line
    for line in reversed(lines):
        line_lower = line.lower()
        if any(kw in line_lower for kw in keywords):
            amt = _parse_amount(line, lang)
            if amt is not None:
                return amt

    # Fallback: last parseable amount
    for line in reversed(lines):
        amt = _parse_amount(line, lang)
        if amt is not None:
            return amt

    return None


# ── Public API ────────────────────────────────────────────────────────────────

def scan_receipt(image_path: str) -> dict:
    """
    Primary entry point: OCR a receipt image and extract structured data.

    Args:
        image_path: Path to a receipt image (.jpg, .jpeg, .png, .webp, etc.)

    Returns:
        {
            "merchant": str,
            "date": str,          # ISO 8601 or ""
            "total": float,       # 0.0 if not found
            "currency": str,
            "items": [{"description": str, "amount": float}],
            "raw_text": str,
            "confidence": str,    # "high" | "medium" | "low"
        }
    """
    result = {
        "merchant": "Unknown",
        "date": "",
        "total": 0.0,
        "currency": "EUR",
        "items": [],
        "raw_text": "",
        "confidence": "low",
    }

    if not _PIL_AVAILABLE:
        result["error"] = "Pillow is not installed. Install it with: pip install Pillow"
        return result

    if not _TESSERACT_AVAILABLE:
        result["error"] = "pytesseract is not installed. Install it with: pip install pytesseract"
        return result

    if not os.path.isfile(image_path):
        result["error"] = f"File not found: {image_path}"
        return result

    try:
        img = _preprocess_image(image_path)
        raw_text = pytesseract.image_to_string(img, config="--psm 6")
    except Exception as e:
        result["error"] = f"OCR failed: {e}"
        return result

    result["raw_text"] = raw_text
    lines = raw_text.splitlines()

    lang = detect_language(raw_text)
    currency = _detect_currency(raw_text)
    merchant = _extract_merchant(lines)
    date = _extract_date(raw_text)
    items = _extract_items(lines, lang)
    total = _find_total(lines, lang)

    result.update({
        "merchant": merchant,
        "date": date,
        "total": total if total is not None else 0.0,
        "currency": currency,
        "items": items,
    })

    # Confidence: high if we got merchant + date + total, medium if 2/3, low otherwise
    fields_found = sum([
        merchant != "Unknown",
        bool(date),
        total is not None and total > 0,
    ])
    result["confidence"] = "high" if fields_found >= 3 else ("medium" if fields_found >= 2 else "low")

    return result


def scan_to_transaction(
    image_path: str,
    account_id: str,
    category: Optional[str] = None,
) -> dict:
    """
    Scan a receipt and return a transaction dict ready for
    transaction_logger.add_transaction().

    Args:
        image_path:  Path to receipt image.
        account_id:  Target account.
        category:    Optional override; auto-categorized from merchant if None.

    Returns:
        A dict with keys: date, type, amount, category, description, account_id,
        currency, payee, tags, and scan_result (the raw scan output).
    """
    scan = scan_receipt(image_path)

    # Infer category from merchant name if not provided
    if category is None:
        merchant_lower = scan.get("merchant", "").lower()
        if any(kw in merchant_lower for kw in ["rewe", "aldi", "lidl", "edeka", "netto", "penny"]):
            category = "food"
        elif any(kw in merchant_lower for kw in ["restaurant", "café", "cafe", "bistro", "pizza"]):
            category = "dining"
        elif any(kw in merchant_lower for kw in ["apotheke", "pharmacy"]):
            category = "healthcare"
        elif any(kw in merchant_lower for kw in ["tank", "shell", "aral", "fuel"]):
            category = "transport"
        else:
            category = "other_expense"

    total = scan.get("total", 0.0)
    # Expenses are negative
    amount = -abs(total) if total > 0 else total

    date = scan.get("date") or datetime.now().date().isoformat()

    txn = {
        "date": date,
        "type": "expense",
        "amount": amount,
        "category": category,
        "description": scan.get("merchant", "Receipt import"),
        "account_id": account_id,
        "currency": scan.get("currency", "EUR"),
        "payee": scan.get("merchant", ""),
        "tags": ["receipt", "scanned"],
        "scan_result": scan,
    }
    return txn
