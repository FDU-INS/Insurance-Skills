"""Tests for the import system (csv_importer, mt940_importer, ofx_importer, import_router)."""
import os
import tempfile
from csv_importer import parse_csv, detect_bank_format, _parse_amount, _parse_date
from ofx_importer import parse_ofx, _extract_tag, _parse_ofx_date
from mt940_importer import _clean_mt940_details, _extract_currency
from import_router import detect_format
from transaction_normalizer import normalize_transactions, _is_tax_relevant


# ── CSV Importer ─────────────────────────────────────────────────────────────

def test_parse_amount_german():
    assert _parse_amount("1.234,56", ",") == 1234.56
    assert _parse_amount("-45,50", ",") == -45.50
    assert _parse_amount("0,00", ",") == 0.0


def test_parse_amount_us():
    assert _parse_amount("1,234.56", ".") == 1234.56
    assert _parse_amount("-45.50", ".") == -45.50


def test_parse_date_formats():
    assert _parse_date("01.04.2026", "%d.%m.%Y") == "2026-04-01"
    assert _parse_date("2026-04-01", "%Y-%m-%d") == "2026-04-01"
    assert _parse_date("01/04/2026", "%d/%m/%Y") == "2026-04-01"


def test_parse_generic_csv():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8") as f:
        f.write("Date,Amount,Description\n")
        f.write("2026-04-01,-45.50,REWE Berlin\n")
        f.write("2026-04-02,3500.00,Gehalt April\n")
        f.name
    try:
        txns = parse_csv(f.name, currency="EUR")
        assert len(txns) == 2
        assert txns[0]["amount"] == -45.50
        assert txns[1]["amount"] == 3500.0
    finally:
        os.unlink(f.name)


def test_detect_bank_format_dkb():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="latin-1") as f:
        f.write('"Kontonummer:";"DE123456";\n\n')
        f.write('"Buchungsdatum";"Wertstellung";"Buchungstext";"Auftraggeber / Begünstigter";"Verwendungszweck";"Kontonummer";"BLZ";"Betrag (EUR)";"Gläubiger-ID";"Mandatsreferenz";"Kundenreferenz"\n')
        f.write('"01.04.2026";"01.04.2026";"Lastschrift";"REWE";"REWE BERLIN";"";"";""-45,50";"";"";""\n')
    try:
        fmt = detect_bank_format(f.name)
        assert fmt == "dkb"
    finally:
        os.unlink(f.name)


# ── OFX Importer ────────────────────────────────────────────────────────────

def test_extract_tag():
    assert _extract_tag("<TRNAMT>-45.50", "TRNAMT") == "-45.50"
    assert _extract_tag("<NAME>REWE Berlin</NAME>", "NAME") == "REWE Berlin"
    assert _extract_tag("no tag here", "MISSING") is None


def test_parse_ofx_date():
    assert _parse_ofx_date("20260401") == "2026-04-01"
    assert _parse_ofx_date("20260401120000") == "2026-04-01"
    assert _parse_ofx_date("20260401120000[-5:EST]") == "2026-04-01"


def test_parse_ofx_file():
    content = """OFXHEADER:100
<OFX>
<BANKMSGSRSV1><STMTTRNRS><STMTRS>
<CURDEF>EUR
<BANKTRANLIST>
<STMTTRN>
<TRNTYPE>DEBIT
<DTPOSTED>20260401
<TRNAMT>-45.50
<FITID>2026040100001
<NAME>REWE Berlin
</STMTTRN>
<STMTTRN>
<TRNTYPE>CREDIT
<DTPOSTED>20260401
<TRNAMT>3500.00
<FITID>2026040100002
<NAME>Gehalt
</STMTTRN>
</BANKTRANLIST>
</STMTRS></STMTTRNRS></BANKMSGSRSV1></OFX>"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".ofx", delete=False) as f:
        f.write(content)
    try:
        txns = parse_ofx(f.name)
        assert len(txns) == 2
        assert txns[0]["amount"] == -45.50
        assert txns[1]["amount"] == 3500.0
    finally:
        os.unlink(f.name)


# ── MT940 helpers ────────────────────────────────────────────────────────────

def test_clean_mt940_details():
    raw = "?20REWE?21Berlin?22Lebensmittel"
    cleaned = _clean_mt940_details(raw)
    assert "REWE" in cleaned
    assert "Berlin" in cleaned


def test_extract_currency_mt940():
    assert _extract_currency(":60F:C260401EUR123456,78") == "EUR"


# ── Format detection ─────────────────────────────────────────────────────────

def test_detect_csv():
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as f:
        f.write(b"a,b,c\n1,2,3\n")
    try:
        assert detect_format(f.name) == "csv"
    finally:
        os.unlink(f.name)


def test_detect_ofx():
    with tempfile.NamedTemporaryFile(suffix=".ofx", delete=False) as f:
        f.write(b"OFXHEADER:100\n<OFX>")
    try:
        assert detect_format(f.name) == "ofx"
    finally:
        os.unlink(f.name)


# ── Normalizer ───────────────────────────────────────────────────────────────

def test_normalize_transactions():
    raw = [
        {"date": "2026-04-01", "amount": -45.50, "description": "REWE Berlin", "payee": "REWE"},
        {"date": "2026-04-01", "amount": 3500, "description": "Gehalt", "payee": "Arbeitgeber"},
    ]
    normalized = normalize_transactions(raw, "checking", "csv", "EUR")
    assert len(normalized) == 2
    assert normalized[0]["category"] == "food"
    assert normalized[1]["category"] == "salary"
    assert normalized[0]["type"] == "expense"
    assert normalized[1]["type"] == "income"


def test_is_tax_relevant():
    assert _is_tax_relevant("education") is True
    assert _is_tax_relevant("entertainment") is False
