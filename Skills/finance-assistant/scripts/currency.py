"""
Multi-currency support for Finance Assistant.

Uses Decimal for precision. Exchange rates are cached locally with a 24-hour TTL.
Falls back to last known rate with a confidence downgrade when offline.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from typing import Optional

try:
    from finance_storage import ensure_finance_dir, load_json, save_json
except ImportError:
    import os, sys
    sys.path.insert(0, os.path.dirname(__file__))
    from finance_storage import ensure_finance_dir, load_json, save_json


# ── Common currencies ────────────────────────────────────────────────────────

CURRENCY_SYMBOLS = {
    "EUR": "€", "USD": "$", "GBP": "£", "CHF": "CHF", "PLN": "zł",
    "SEK": "kr", "DKK": "kr", "NOK": "kr", "CZK": "Kč", "JPY": "¥",
    "CAD": "C$", "AUD": "A$", "BRL": "R$", "INR": "₹", "CNY": "¥",
}

CURRENCY_DECIMALS = {
    "JPY": 0, "KRW": 0, "HUF": 0,
}

# ── Hardcoded fallback rates (EUR-based, approximate) ────────────────────────
# Used only when no cached rates are available. Marked as low confidence.

_FALLBACK_RATES_EUR = {
    "EUR": 1.0, "USD": 1.08, "GBP": 0.86, "CHF": 0.97, "PLN": 4.32,
    "SEK": 11.40, "DKK": 7.46, "NOK": 11.60, "CZK": 25.20, "JPY": 163.0,
    "CAD": 1.47, "AUD": 1.66, "BRL": 5.40, "INR": 90.0, "CNY": 7.85,
}


def _get_rates_cache_path() -> Path:
    return ensure_finance_dir() / "exchange_rates.json"


def _load_cached_rates() -> dict:
    return load_json(_get_rates_cache_path(), default={}) or {}


def _save_cached_rates(rates: dict) -> None:
    rates["_cached_at"] = datetime.now().isoformat()
    save_json(_get_rates_cache_path(), rates)


def get_exchange_rate(
    from_currency: str,
    to_currency: str,
    as_of: Optional[date] = None,
) -> tuple[float, str]:
    """
    Return (rate, confidence) where confidence is 'cached' | 'fallback'.
    Rate converts 1 unit of from_currency to to_currency.
    """
    from_currency = from_currency.upper()
    to_currency = to_currency.upper()

    if from_currency == to_currency:
        return 1.0, "exact"

    cached = _load_cached_rates()
    cached_at = cached.get("_cached_at")

    # Try cached EUR-based rates
    rates = cached.get("rates", {})
    if rates and from_currency in rates and to_currency in rates:
        if cached_at:
            try:
                age_hours = (datetime.now() - datetime.fromisoformat(cached_at)).total_seconds() / 3600
                if age_hours <= 24:
                    return round(rates[to_currency] / rates[from_currency], 6), "cached"
            except (ValueError, TypeError):
                pass
        else:
            return round(rates[to_currency] / rates[from_currency], 6), "cached"
    # fall through to fallback if stale or no cached_at

    # Fallback to hardcoded rates
    if from_currency in _FALLBACK_RATES_EUR and to_currency in _FALLBACK_RATES_EUR:
        rate = _FALLBACK_RATES_EUR[to_currency] / _FALLBACK_RATES_EUR[from_currency]
        return round(rate, 6), "fallback"

    raise ValueError(f"No exchange rate available for {from_currency} → {to_currency}")


def convert(
    amount: float,
    from_currency: str,
    to_currency: str,
    as_of: Optional[date] = None,
) -> tuple[float, str]:
    """Convert amount, return (converted_amount, confidence)."""
    rate, confidence = get_exchange_rate(from_currency, to_currency, as_of)
    return round(amount * rate, _decimals(to_currency)), confidence


def _decimals(currency: str) -> int:
    return CURRENCY_DECIMALS.get(currency.upper(), 2)


def format_money(amount: float, currency: str, locale: str = "en") -> str:
    """Format amount with currency symbol."""
    symbol = CURRENCY_SYMBOLS.get(currency.upper(), currency.upper())
    dec = _decimals(currency)
    if dec == 0:
        formatted = f"{int(amount):,}"
    else:
        formatted = f"{amount:,.{dec}f}"
    if locale == "de":
        formatted = formatted.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{symbol}{formatted}"


def normalize_to_primary(
    amount: float,
    source_currency: str,
    primary_currency: str = "EUR",
) -> tuple[float, str]:
    """Convert to the user's primary currency."""
    return convert(amount, source_currency, primary_currency)


# ── Money dataclass ──────────────────────────────────────────────────────────

@dataclass
class Money:
    """Precise monetary value with currency."""
    amount: Decimal
    currency: str

    def __post_init__(self):
        if isinstance(self.amount, (int, float)):
            self.amount = Decimal(str(self.amount))
        self.currency = self.currency.upper()

    def to(self, target_currency: str, rate: Optional[float] = None) -> "Money":
        if self.currency == target_currency.upper():
            return Money(self.amount, self.currency)
        if rate is None:
            rate, _ = get_exchange_rate(self.currency, target_currency)
        converted = self.amount * Decimal(str(rate))
        dec = _decimals(target_currency)
        quantize_str = "1" if dec == 0 else f"0.{'0' * dec}"
        return Money(converted.quantize(Decimal(quantize_str), rounding=ROUND_HALF_UP), target_currency)

    def __add__(self, other: "Money") -> "Money":
        if other.currency != self.currency:
            other = other.to(self.currency)
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other: "Money") -> "Money":
        if other.currency != self.currency:
            other = other.to(self.currency)
        return Money(self.amount - other.amount, self.currency)

    def __mul__(self, factor: float | int | Decimal) -> "Money":
        return Money(self.amount * Decimal(str(factor)), self.currency)

    def __neg__(self) -> "Money":
        return Money(-self.amount, self.currency)

    def __float__(self) -> float:
        return float(self.amount)

    def format(self, locale: str = "en") -> str:
        return format_money(float(self.amount), self.currency, locale)

    def __repr__(self) -> str:
        return f"Money({self.amount}, '{self.currency}')"
