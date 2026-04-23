"""
Locale-aware rule registry with provenance metadata.

Adapted from TaxDE rule_registry.py to support multiple locale plugins.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

try:
    from tax_engine import _load_locale, get_active_locale
except ImportError:
    import os, sys
    sys.path.insert(0, os.path.dirname(__file__))
    from tax_engine import _load_locale, get_active_locale


def get_rule_registry(locale_code: Optional[str] = None, year: int = None) -> dict:
    """Get rule registry with provenance for a locale."""
    locale_code = locale_code or get_active_locale()
    year = year or datetime.now().year

    try:
        locale = _load_locale(locale_code)
        rules = locale.get_tax_rules(year)
        deadlines = locale.get_filing_deadlines(year)

        return {
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            "locale": locale_code,
            "locale_name": getattr(locale, "LOCALE_NAME", locale_code.upper()),
            "requested_year": year,
            "resolved_year": year,
            "supported_years": getattr(locale, "SUPPORTED_YEARS", []),
            "rules": rules,
            "deadlines": deadlines,
        }
    except (ImportError, AttributeError) as e:
        return {
            "locale": locale_code,
            "error": str(e),
            "requested_year": year,
        }


def format_rule_registry_display(registry: dict) -> str:
    if "error" in registry:
        return f"Locale '{registry['locale']}': {registry['error']}"

    lines = [
        f"Rule registry for {registry['locale_name']} ({registry['locale']})",
        f"Year: {registry['requested_year']}",
        f"Supported years: {registry.get('supported_years', [])}",
    ]

    deadlines = registry.get("deadlines", [])
    if deadlines:
        lines.append("\nDeadlines:")
        for d in deadlines:
            if isinstance(d, dict) and "label" in d:
                lines.append(f"  - {d['label']}")

    return "\n".join(lines)
