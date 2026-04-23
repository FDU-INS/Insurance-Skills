"""
Finance Assistant Category Learner.

Remembers user corrections to auto-categorization and improves accuracy
over time. Uses a simple JSON-based keyword store — no ML needed.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

try:
    from finance_storage import ensure_subdir, load_json, save_json
except ImportError:
    import os, sys
    sys.path.insert(0, os.path.dirname(__file__))
    from finance_storage import ensure_subdir, load_json, save_json


def _learner_path():
    return ensure_subdir("learner") / "category_rules.json"


def _load_rules() -> dict:
    return load_json(_learner_path(), default={
        "keyword_overrides": {},  # "rewe" -> "food"
        "payee_rules": {},        # "REWE" -> "food"
        "corrections": [],        # History of corrections
    })


def _save_rules(rules: dict) -> None:
    rules["last_updated"] = datetime.now().isoformat()
    save_json(_learner_path(), rules)


def learn_correction(
    description: str,
    payee: Optional[str],
    old_category: str,
    new_category: str,
) -> dict:
    """
    Record a user correction. Extracts keywords and payee rules
    so future similar transactions auto-categorize correctly.
    """
    rules = _load_rules()

    # Extract meaningful keywords from description (2+ chars, lowercase)
    words = [w.lower() for w in (description or "").split() if len(w) >= 3]

    # Store payee rule (highest priority)
    if payee and len(payee.strip()) >= 2:
        payee_key = payee.strip().lower()
        rules["payee_rules"][payee_key] = new_category

    # Store keyword overrides (for the most distinctive words)
    # Only store if the word isn't too generic
    generic_words = {"the", "and", "for", "von", "der", "die", "das", "und", "mit",
                     "eur", "jan", "feb", "mar", "apr", "may", "jun", "jul", "aug",
                     "sep", "oct", "nov", "dec", "berlin", "münchen", "hamburg"}
    for word in words:
        if word not in generic_words and len(word) >= 4:
            rules["keyword_overrides"][word] = new_category

    # Record the correction for history
    rules["corrections"].append({
        "timestamp": datetime.now().isoformat(),
        "description": description,
        "payee": payee,
        "old_category": old_category,
        "new_category": new_category,
    })

    # Keep only last 500 corrections
    rules["corrections"] = rules["corrections"][-500:]

    _save_rules(rules)

    return {
        "learned": True,
        "payee_rule": payee.strip().lower() if payee else None,
        "keyword_rules": [w for w in words if w not in generic_words and len(w) >= 4],
        "new_category": new_category,
    }


def suggest_category(description: str, payee: Optional[str] = None) -> Optional[str]:
    """
    Check learned rules for a category suggestion.
    Returns None if no learned rule matches (fall through to default auto_categorize).
    """
    rules = _load_rules()

    # 1. Check payee rules (highest priority)
    if payee:
        payee_key = payee.strip().lower()
        if payee_key in rules.get("payee_rules", {}):
            return rules["payee_rules"][payee_key]
        # Partial match
        for stored_payee, category in rules.get("payee_rules", {}).items():
            if stored_payee in payee_key or payee_key in stored_payee:
                return category

    # 2. Check keyword overrides
    desc_lower = (description or "").lower()
    keyword_overrides = rules.get("keyword_overrides", {})
    for keyword, category in keyword_overrides.items():
        if keyword in desc_lower:
            return category

    return None


def get_learned_rules() -> dict:
    """Return current learned rules for display."""
    rules = _load_rules()
    return {
        "payee_rules": len(rules.get("payee_rules", {})),
        "keyword_rules": len(rules.get("keyword_overrides", {})),
        "total_corrections": len(rules.get("corrections", [])),
        "top_payees": dict(list(rules.get("payee_rules", {}).items())[:20]),
        "top_keywords": dict(list(rules.get("keyword_overrides", {}).items())[:20]),
    }


def clear_learned_rules() -> bool:
    """Reset all learned categorization rules."""
    _save_rules({
        "keyword_overrides": {},
        "payee_rules": {},
        "corrections": [],
    })
    return True


def enhanced_auto_categorize(description: str, amount: float, payee: Optional[str] = None) -> tuple[str, str]:
    """
    Auto-categorize with learned rules. Returns (category, source).
    source is "learned" if from user corrections, "default" if from keyword matching.
    """
    # First check learned rules
    learned = suggest_category(description, payee)
    if learned:
        return learned, "learned"

    # Fall through to default auto_categorize
    from transaction_logger import auto_categorize
    category, sub = auto_categorize(description, amount)
    return category, "default"
