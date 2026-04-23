"""
Finance Assistant Transaction Logger.

Logs income and expense transactions with auto-categorization and budget alerts.
Transactions are stored per-account per-year in .finance/accounts/transactions/.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

try:
    from finance_storage import (
        get_transactions_path, load_json, save_json,
    )
    from currency import format_money
except ImportError:
    import os, sys
    sys.path.insert(0, os.path.dirname(__file__))
    from finance_storage import get_transactions_path, load_json, save_json
    from currency import format_money


# ── Category definitions ─────────────────────────────────────────────────────

EXPENSE_CATEGORIES = {
    "housing":          "Housing (rent, mortgage, utilities)",
    "food":             "Food & Groceries",
    "dining":           "Dining & Restaurants",
    "transport":        "Transport (fuel, transit, car)",
    "insurance":        "Insurance Premiums",
    "healthcare":       "Healthcare & Medical",
    "education":        "Education & Training",
    "childcare":        "Childcare",
    "clothing":         "Clothing & Personal",
    "entertainment":    "Entertainment & Leisure",
    "subscriptions":    "Subscriptions & Memberships",
    "telecom":          "Phone, Internet & TV",
    "household":        "Household & Maintenance",
    "equipment":        "Equipment & Electronics",
    "gifts":            "Gifts & Donations",
    "travel":           "Travel & Vacation",
    "taxes":            "Taxes & Government Fees",
    "debt_payment":     "Debt Payments (beyond minimum)",
    "savings":          "Savings & Investments",
    "fees":             "Bank & Service Fees",
    "pets":             "Pets",
    "personal_care":    "Personal Care & Beauty",
    "other_expense":    "Other Expense",
}

INCOME_CATEGORIES = {
    "salary":           "Salary / Wages",
    "freelance":        "Freelance / Contract Income",
    "business":         "Business Income",
    "investment":       "Investment Income (dividends, interest)",
    "rental":           "Rental Income",
    "pension":          "Pension / Retirement Income",
    "benefits":         "Government Benefits",
    "gift_received":    "Gifts / Inheritance Received",
    "refund":           "Tax Refund",
    "other_income":     "Other Income",
}

ALL_CATEGORIES = {**EXPENSE_CATEGORIES, **INCOME_CATEGORIES}

TRANSACTION_SCHEMA = {
    "id": None,
    "date": None,
    "account_id": None,
    "type": None,                  # "income"|"expense"|"transfer"|"investment"|"debt_payment"
    "amount": None,
    "currency": None,
    "category": None,
    "subcategory": None,
    "description": None,
    "payee": None,
    "is_recurring": False,
    "tags": [],
    "tax_relevant": False,
    "tax_category": None,
    "business_use_pct": 100.0,
    "import_source": None,
    "import_ref": None,
}


# ── Auto-categorization ─────────────────────────────────────────────────────

_CATEGORY_KEYWORDS = {
    "housing": ["miete", "rent", "mortgage", "hypothek", "nebenkosten", "strom", "gas", "wasser", "utilities"],
    "food": ["rewe", "edeka", "aldi", "lidl", "penny", "netto", "kaufland", "grocery", "supermarket", "lebensmittel"],
    "dining": ["restaurant", "cafe", "lieferando", "uber eats", "deliveroo", "mcdonald", "starbucks", "gastronomie"],
    "transport": ["db ", "bahn", "bvg", "mvv", "tankstelle", "fuel", "petrol", "parking", "taxi", "uber", "bolt", "shell", "aral"],
    "insurance": ["versicherung", "insurance", "allianz", "huk", "ergo", "axa"],
    "healthcare": ["apotheke", "pharmacy", "arzt", "doctor", "zahnarzt", "dentist", "hospital", "krankenhaus"],
    "education": ["udemy", "coursera", "buch", "book", "kurs", "course", "schule", "university", "uni"],
    "childcare": ["kita", "kindergarten", "daycare", "babysitter"],
    "subscriptions": ["netflix", "spotify", "amazon prime", "disney", "youtube", "gym", "fitnessstudio"],
    "telecom": ["telekom", "vodafone", "o2", "1&1", "internet", "telefon", "phone"],
    "equipment": ["mediamarkt", "saturn", "apple", "amazon", "computer", "laptop"],
    "gifts": ["spende", "donation", "geschenk", "gift"],
    "travel": ["hotel", "airbnb", "booking", "flug", "flight", "ryanair", "lufthansa"],
    "salary": ["gehalt", "salary", "wages", "lohn"],
    "freelance": ["honorar", "invoice", "rechnung"],
    "investment": ["dividende", "dividend", "zinsen", "interest", "kapitalertrag"],
    "refund": ["erstattung", "refund", "rückzahlung"],
}


def auto_categorize(description: str, amount: float) -> tuple[str, Optional[str]]:
    """Guess category from description keywords. Returns (category, None)."""
    desc_lower = (description or "").lower()
    for category, keywords in _CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if kw in desc_lower:
                return category, None
    return ("other_income" if amount > 0 else "other_expense"), None


# ── Transaction Storage ──────────────────────────────────────────────────────

def _load_transactions(account_id: str, year: int) -> list[dict]:
    data = load_json(get_transactions_path(account_id, year), default={"transactions": []})
    return data.get("transactions", []) if isinstance(data, dict) else []


def _save_transactions(account_id: str, year: int, transactions: list[dict]) -> None:
    save_json(get_transactions_path(account_id, year), {
        "account_id": account_id,
        "year": year,
        "last_updated": datetime.now().isoformat(),
        "transaction_count": len(transactions),
        "transactions": transactions,
    })


# ── Public API ───────────────────────────────────────────────────────────────

def add_transaction(
    date: str,
    type: str,
    amount: float,
    category: str,
    description: str,
    account_id: str = "default",
    currency: str = "EUR",
    **kwargs,
) -> dict:
    """Add a transaction. Returns the new transaction plus updated totals."""
    # Normalize date
    try:
        parsed = datetime.fromisoformat(date)
        year = parsed.year
    except (ValueError, TypeError):
        date = datetime.now().date().isoformat()
        year = datetime.now().year

    # Auto-categorize if category is unknown
    if category not in ALL_CATEGORIES:
        category, _ = auto_categorize(description, amount)

    # Infer type from amount sign if not explicit
    if type not in ("income", "expense", "transfer", "investment", "debt_payment"):
        type = "income" if amount > 0 else "expense"

    txn = dict(TRANSACTION_SCHEMA)
    txn.update({
        "id": str(uuid.uuid4())[:8],
        "date": date,
        "account_id": account_id,
        "type": type,
        "amount": round(amount, 2),
        "currency": currency,
        "category": category,
        "description": description,
    })
    txn.update(kwargs)

    transactions = _load_transactions(account_id, year)
    transactions.append(txn)
    transactions.sort(key=lambda t: t.get("date", ""))
    _save_transactions(account_id, year, transactions)

    return {
        "transaction_added": txn,
        "display": _format_transaction_added(txn),
    }


def get_transactions(
    account_id: str = "default",
    year: Optional[int] = None,
    month: Optional[int] = None,
    category: Optional[str] = None,
    type: Optional[str] = None,
) -> list[dict]:
    """Retrieve filtered transactions."""
    year = year or datetime.now().year
    txns = _load_transactions(account_id, year)
    if month:
        txns = [t for t in txns if t.get("date", "")[5:7] == f"{month:02d}"]
    if category:
        txns = [t for t in txns if t.get("category") == category]
    if type:
        txns = [t for t in txns if t.get("type") == type]
    return txns


def get_totals(
    account_id: str = "default",
    year: Optional[int] = None,
    month: Optional[int] = None,
    group_by: str = "category",
) -> dict:
    """Return totals grouped by category or type."""
    txns = get_transactions(account_id=account_id, year=year, month=month)
    totals: dict = {}
    for t in txns:
        key = t.get(group_by, "other")
        if key not in totals:
            totals[key] = {"count": 0, "income": 0.0, "expense": 0.0, "net": 0.0}
        totals[key]["count"] += 1
        amt = float(t.get("amount", 0))
        if amt >= 0:
            totals[key]["income"] += amt
        else:
            totals[key]["expense"] += abs(amt)
        totals[key]["net"] += amt

    for key in totals:
        for field in ("income", "expense", "net"):
            totals[key][field] = round(totals[key][field], 2)

    return totals


def get_summary_display(
    account_id: str = "default",
    year: Optional[int] = None,
    month: Optional[int] = None,
) -> str:
    """Return a formatted transaction summary."""
    year = year or datetime.now().year
    totals = get_totals(account_id=account_id, year=year, month=month)
    if not totals:
        period = f"{year}-{month:02d}" if month else str(year)
        return f"No transactions logged for {period}."

    period = f"{year}-{month:02d}" if month else str(year)
    lines = [f"Transaction summary for {period}\n"]

    total_income = 0.0
    total_expense = 0.0

    for cat, data in sorted(totals.items()):
        label = ALL_CATEGORIES.get(cat, cat)[:35]
        if data["income"] > 0:
            total_income += data["income"]
            lines.append(f"  + {label:<35} {data['count']:>3} txns  +{format_money(data['income'], 'EUR')}")
        if data["expense"] > 0:
            total_expense += data["expense"]
            lines.append(f"  - {label:<35} {data['count']:>3} txns  -{format_money(data['expense'], 'EUR')}")

    lines.append(f"\n  Total income:   +{format_money(total_income, 'EUR')}")
    lines.append(f"  Total expenses: -{format_money(total_expense, 'EUR')}")
    lines.append(f"  Net:            {format_money(total_income - total_expense, 'EUR')}")

    return "\n".join(lines)


def _format_transaction_added(txn: dict) -> str:
    amt = float(txn.get("amount", 0))
    cur = txn.get("currency", "EUR")
    sign = "+" if amt >= 0 else ""
    label = ALL_CATEGORIES.get(txn.get("category", ""), txn.get("category", ""))
    return (
        f"Transaction logged: {txn['description']}\n"
        f"  {sign}{format_money(amt, cur)}  |  {label}\n"
        f"  Date: {txn['date']}  |  Account: {txn['account_id']}"
    )


def deduplicate(new_transactions: list[dict], existing_transactions: list[dict]) -> list[dict]:
    """Remove likely duplicates based on date + amount + description."""
    existing_keys = set()
    for t in existing_transactions:
        key = (t.get("date"), round(float(t.get("amount", 0)), 2), (t.get("description") or "").lower()[:50])
        existing_keys.add(key)

    unique = []
    for t in new_transactions:
        key = (t.get("date"), round(float(t.get("amount", 0)), 2), (t.get("description") or "").lower()[:50])
        if key not in existing_keys:
            unique.append(t)
            existing_keys.add(key)

    return unique
