"""
Transaction normalizer — transforms raw imported transactions into the
standard Finance Assistant transaction schema with auto-categorization.
"""

from __future__ import annotations

from typing import Optional

try:
    from transaction_logger import auto_categorize, TRANSACTION_SCHEMA
except ImportError:
    import os, sys
    sys.path.insert(0, os.path.dirname(__file__))
    from transaction_logger import auto_categorize, TRANSACTION_SCHEMA


def normalize_transactions(
    raw_transactions: list[dict],
    account_id: str,
    source_format: str,
    currency: str = "EUR",
) -> list[dict]:
    """
    Normalize raw imported transactions into the standard schema.
    Auto-categorizes based on description keywords.
    """
    normalized = []

    for raw in raw_transactions:
        amount = float(raw.get("amount", 0))
        description = raw.get("description", "")
        payee = raw.get("payee", "")

        # Auto-categorize
        category, subcategory = auto_categorize(
            f"{payee} {description}",
            amount,
        )

        # Determine type
        txn_type = raw.get("type")
        if not txn_type:
            txn_type = "income" if amount > 0 else "expense"

        txn = {
            "date": raw.get("date", ""),
            "account_id": account_id,
            "type": txn_type,
            "amount": round(amount, 2),
            "currency": raw.get("currency", currency),
            "category": category,
            "subcategory": subcategory,
            "description": description.strip(),
            "payee": payee.strip(),
            "import_source": source_format,
            "import_ref": raw.get("import_ref"),
            "is_recurring": False,
            "tags": [],
            "tax_relevant": _is_tax_relevant(category),
        }
        normalized.append(txn)

    return normalized


def _is_tax_relevant(category: str) -> bool:
    """Check if a category is typically tax-relevant."""
    tax_categories = {
        "equipment", "education", "childcare", "healthcare",
        "insurance", "gifts", "salary", "freelance", "business",
        "investment", "rental", "pension",
    }
    return category in tax_categories
