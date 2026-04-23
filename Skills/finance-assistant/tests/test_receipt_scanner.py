"""
Tests for receipt_scanner.py.

pytesseract and Pillow are mocked to allow testing all parsing logic
without requiring a real Tesseract installation.
"""

import sys
import types
import os
import pytest
from unittest.mock import MagicMock, patch


# ── Mock PIL and pytesseract before import ────────────────────────────────────

def _make_pil_mock():
    """Create a minimal PIL mock that satisfies receipt_scanner imports."""
    pil = types.ModuleType("PIL")

    class FakeImage:
        @staticmethod
        def open(path):
            img = FakeImage()
            img._mode = "RGB"
            return img

        def convert(self, mode):
            return self

        def filter(self, f):
            return self

        def point(self, fn, mode=None):
            return self

        def __enter__(self):
            return self

        def __exit__(self, *a):
            pass

    class FakeImageEnhance:
        class Contrast:
            def __init__(self, img):
                self._img = img

            def enhance(self, factor):
                return self._img

    class FakeImageFilter:
        SHARPEN = "SHARPEN"

    class FakeImageOps:
        pass

    pil.Image = FakeImage
    pil.ImageEnhance = FakeImageEnhance
    pil.ImageFilter = FakeImageFilter
    pil.ImageOps = FakeImageOps

    # Make sub-module imports work
    sys.modules["PIL"] = pil
    sys.modules["PIL.Image"] = pil
    sys.modules["PIL.ImageEnhance"] = pil
    sys.modules["PIL.ImageFilter"] = pil
    sys.modules["PIL.ImageOps"] = pil
    return pil


def _make_tesseract_mock(text: str):
    tess = types.ModuleType("pytesseract")
    tess.image_to_string = MagicMock(return_value=text)
    sys.modules["pytesseract"] = tess
    return tess


# ── Language detection ────────────────────────────────────────────────────────

def test_detect_language_german():
    _make_pil_mock()
    _make_tesseract_mock("")
    # Re-import to pick up mocks
    if "receipt_scanner" in sys.modules:
        del sys.modules["receipt_scanner"]
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
    from receipt_scanner import detect_language

    de_text = "Gesamt 12,99 EUR\nMwst 7%\nVielen Dank\nKassenbon"
    assert detect_language(de_text) == "de"


def test_detect_language_english():
    if "receipt_scanner" in sys.modules:
        del sys.modules["receipt_scanner"]
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
    from receipt_scanner import detect_language

    en_text = "Total: 12.99\nThank you for shopping with us\nReceipt"
    assert detect_language(en_text) == "en"


# ── Amount parsing ────────────────────────────────────────────────────────────

def test_parse_amount_de_format():
    if "receipt_scanner" in sys.modules:
        del sys.modules["receipt_scanner"]
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
    from receipt_scanner import _parse_amount_de

    assert _parse_amount_de("1.234,56") == 1234.56
    assert _parse_amount_de("45,99") == 45.99
    assert _parse_amount_de("Gesamt 12,99") == 12.99


def test_parse_amount_en_format():
    if "receipt_scanner" in sys.modules:
        del sys.modules["receipt_scanner"]
    from receipt_scanner import _parse_amount_en

    assert _parse_amount_en("1,234.56") == 1234.56
    assert _parse_amount_en("45.99") == 45.99
    assert _parse_amount_en("Total 12.99") == 12.99


def test_parse_amount_dispatch():
    if "receipt_scanner" in sys.modules:
        del sys.modules["receipt_scanner"]
    from receipt_scanner import _parse_amount

    assert _parse_amount("12,99", "de") == 12.99
    assert _parse_amount("12.99", "en") == 12.99


# ── Currency detection ────────────────────────────────────────────────────────

def test_detect_currency_eur():
    if "receipt_scanner" in sys.modules:
        del sys.modules["receipt_scanner"]
    from receipt_scanner import _detect_currency

    assert _detect_currency("Gesamt: 12,99 €") == "EUR"
    assert _detect_currency("Total EUR 12.99") == "EUR"


def test_detect_currency_gbp():
    if "receipt_scanner" in sys.modules:
        del sys.modules["receipt_scanner"]
    from receipt_scanner import _detect_currency

    assert _detect_currency("Total: £12.99") == "GBP"


def test_detect_currency_usd():
    if "receipt_scanner" in sys.modules:
        del sys.modules["receipt_scanner"]
    from receipt_scanner import _detect_currency

    assert _detect_currency("Total: $12.99") == "USD"


# ── Date extraction ───────────────────────────────────────────────────────────

def test_extract_date_german_format():
    if "receipt_scanner" in sys.modules:
        del sys.modules["receipt_scanner"]
    from receipt_scanner import _extract_date

    assert _extract_date("Datum: 15.03.2025") == "2025-03-15"


def test_extract_date_iso_format():
    if "receipt_scanner" in sys.modules:
        del sys.modules["receipt_scanner"]
    from receipt_scanner import _extract_date

    assert _extract_date("Date: 2025-03-15") == "2025-03-15"


def test_extract_date_slash_format():
    if "receipt_scanner" in sys.modules:
        del sys.modules["receipt_scanner"]
    from receipt_scanner import _extract_date

    assert _extract_date("15/03/2025") == "2025-03-15"


def test_extract_date_not_found():
    if "receipt_scanner" in sys.modules:
        del sys.modules["receipt_scanner"]
    from receipt_scanner import _extract_date

    assert _extract_date("No date in this text") == ""


# ── Merchant extraction ───────────────────────────────────────────────────────

def test_extract_merchant_picks_first_text_line():
    if "receipt_scanner" in sys.modules:
        del sys.modules["receipt_scanner"]
    from receipt_scanner import _extract_merchant

    lines = ["REWE Markt GmbH", "Berlin Mitte", "15.03.2025", "Artikel 1   2,99"]
    assert _extract_merchant(lines) == "REWE Markt GmbH"


def test_extract_merchant_skips_digit_lines():
    if "receipt_scanner" in sys.modules:
        del sys.modules["receipt_scanner"]
    from receipt_scanner import _extract_merchant

    lines = ["12345", "15.03.2025", "REWE Berlin"]
    assert _extract_merchant(lines) == "REWE Berlin"


# ── Item extraction ───────────────────────────────────────────────────────────

def test_extract_items_en():
    if "receipt_scanner" in sys.modules:
        del sys.modules["receipt_scanner"]
    from receipt_scanner import _extract_items

    lines = [
        "REWE Store",
        "Apple Juice   2.49",
        "Bread         1.99",
        "Total         4.48",
    ]
    items = _extract_items(lines, "en")
    assert len(items) == 2
    assert items[0]["description"] == "Apple Juice"
    assert items[0]["amount"] == 2.49
    assert items[1]["description"] == "Bread"


def test_extract_items_de():
    if "receipt_scanner" in sys.modules:
        del sys.modules["receipt_scanner"]
    from receipt_scanner import _extract_items

    lines = [
        "REWE Markt",
        "Apfelsaft   2,49",
        "Brot        1,99",
        "Gesamt      4,48",
    ]
    items = _extract_items(lines, "de")
    assert len(items) == 2
    assert items[0]["description"] == "Apfelsaft"
    assert items[0]["amount"] == 2.49


def test_extract_items_skips_total_line():
    if "receipt_scanner" in sys.modules:
        del sys.modules["receipt_scanner"]
    from receipt_scanner import _extract_items

    lines = ["Item A   5.00", "Total    5.00", "Tax      0.50"]
    items = _extract_items(lines, "en")
    descriptions = [i["description"] for i in items]
    assert "Total" not in descriptions


# ── Total finding ─────────────────────────────────────────────────────────────

def test_find_total_de():
    if "receipt_scanner" in sys.modules:
        del sys.modules["receipt_scanner"]
    from receipt_scanner import _find_total

    lines = [
        "Artikel 1   2,99",
        "Artikel 2   5,00",
        "Gesamt      7,99",
    ]
    assert _find_total(lines, "de") == 7.99


def test_find_total_en():
    if "receipt_scanner" in sys.modules:
        del sys.modules["receipt_scanner"]
    from receipt_scanner import _find_total

    lines = [
        "Item A   5.00",
        "Item B   2.99",
        "Total    7.99",
    ]
    assert _find_total(lines, "en") == 7.99


# ── scan_receipt with mocked OCR ──────────────────────────────────────────────

SAMPLE_DE_RECEIPT = """REWE Markt GmbH
Berlin, Friedrichstr. 10

Datum: 15.03.2025

Apfelsaft              2,49
Vollkornbrot           1,99
Bananen (1 kg)         1,29

MwSt 7%                0,40
Gesamt                 5,77 €

Vielen Dank fuer Ihren Einkauf!
"""

SAMPLE_EN_RECEIPT = """Tesco Express
London, EC1A 1BB

Date: 15/03/2025

Apple Juice            2.49
Wholemeal Bread        1.99
Bananas 1kg            1.29

Total                  5.77
"""


def test_scan_receipt_german_receipt(tmp_path):
    _make_pil_mock()
    _make_tesseract_mock(SAMPLE_DE_RECEIPT)

    if "receipt_scanner" in sys.modules:
        del sys.modules["receipt_scanner"]
    from receipt_scanner import scan_receipt

    # Create a dummy image file
    img_path = str(tmp_path / "receipt.jpg")
    with open(img_path, "wb") as f:
        f.write(b"FAKE IMAGE DATA")  # PIL is mocked, content doesn't matter

    result = scan_receipt(img_path)

    assert "error" not in result, f"Unexpected error: {result.get('error')}"
    assert result["currency"] == "EUR"
    assert result["date"] == "2025-03-15"
    assert result["total"] > 0
    assert result["merchant"] != "Unknown"
    assert isinstance(result["items"], list)
    assert isinstance(result["raw_text"], str)
    assert result["confidence"] in ("high", "medium", "low")


def test_scan_receipt_english_receipt(tmp_path):
    _make_pil_mock()
    _make_tesseract_mock(SAMPLE_EN_RECEIPT)

    if "receipt_scanner" in sys.modules:
        del sys.modules["receipt_scanner"]
    from receipt_scanner import scan_receipt

    img_path = str(tmp_path / "receipt.jpg")
    with open(img_path, "wb") as f:
        f.write(b"FAKE IMAGE DATA")

    result = scan_receipt(img_path)

    assert result["date"] == "2025-03-15"
    assert result["total"] > 0


def test_scan_receipt_missing_file():
    if "receipt_scanner" in sys.modules:
        del sys.modules["receipt_scanner"]
    from receipt_scanner import scan_receipt

    result = scan_receipt("/nonexistent/path/receipt.jpg")
    assert "error" in result


# ── scan_to_transaction ───────────────────────────────────────────────────────

def test_scan_to_transaction_structure(tmp_path):
    _make_pil_mock()
    _make_tesseract_mock(SAMPLE_DE_RECEIPT)

    if "receipt_scanner" in sys.modules:
        del sys.modules["receipt_scanner"]
    from receipt_scanner import scan_to_transaction

    img_path = str(tmp_path / "receipt.jpg")
    with open(img_path, "wb") as f:
        f.write(b"FAKE IMAGE DATA")

    txn = scan_to_transaction(img_path, "checking")

    assert "date" in txn
    assert "type" in txn
    assert "amount" in txn
    assert txn["type"] == "expense"
    assert txn["amount"] <= 0  # expenses are negative
    assert txn["account_id"] == "checking"
    assert "category" in txn
    assert "scan_result" in txn


def test_scan_to_transaction_category_override(tmp_path):
    _make_pil_mock()
    _make_tesseract_mock(SAMPLE_EN_RECEIPT)

    if "receipt_scanner" in sys.modules:
        del sys.modules["receipt_scanner"]
    from receipt_scanner import scan_to_transaction

    img_path = str(tmp_path / "receipt.jpg")
    with open(img_path, "wb") as f:
        f.write(b"FAKE IMAGE DATA")

    txn = scan_to_transaction(img_path, "savings", category="dining")
    assert txn["category"] == "dining"


def test_scan_to_transaction_rewe_autocategory(tmp_path):
    _make_pil_mock()
    rewe_text = "REWE Markt\nDatum: 01.01.2025\nGesamt 10,00 €"
    _make_tesseract_mock(rewe_text)

    if "receipt_scanner" in sys.modules:
        del sys.modules["receipt_scanner"]
    from receipt_scanner import scan_to_transaction

    img_path = str(tmp_path / "receipt.jpg")
    with open(img_path, "wb") as f:
        f.write(b"FAKE IMAGE DATA")

    txn = scan_to_transaction(img_path, "default")
    assert txn["category"] == "food"
