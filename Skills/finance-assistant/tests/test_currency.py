"""Tests for currency.py."""
from decimal import Decimal
from currency import Money, format_money, convert, get_exchange_rate, normalize_to_primary


def test_money_creation():
    m = Money(100, "EUR")
    assert m.amount == Decimal("100")
    assert m.currency == "EUR"


def test_money_add():
    result = Money(100, "EUR") + Money(50, "EUR")
    assert float(result) == 150.0


def test_money_sub():
    result = Money(100, "EUR") - Money(30, "EUR")
    assert float(result) == 70.0


def test_money_mul():
    result = Money(100, "EUR") * 1.5
    assert float(result) == 150.0


def test_money_neg():
    result = -Money(100, "EUR")
    assert float(result) == -100.0


def test_money_format():
    assert format_money(1234.56, "EUR") == "€1,234.56"
    assert format_money(1234.56, "EUR", "de") == "€1.234,56"
    assert format_money(1000, "JPY") == "¥1,000"


def test_money_format_method():
    m = Money(1234.56, "EUR")
    assert "1,234.56" in m.format()


def test_same_currency_rate():
    rate, confidence = get_exchange_rate("EUR", "EUR")
    assert rate == 1.0
    assert confidence == "exact"


def test_fallback_rate():
    rate, confidence = get_exchange_rate("EUR", "USD")
    assert rate > 0
    assert confidence == "fallback"


def test_convert():
    amount, confidence = convert(100, "EUR", "EUR")
    assert amount == 100.0
    assert confidence == "exact"


def test_normalize_to_primary():
    amount, conf = normalize_to_primary(100, "EUR", "EUR")
    assert amount == 100.0
