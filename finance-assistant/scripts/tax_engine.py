"""
Country-agnostic tax engine for Finance Assistant.

Delegates all tax calculations to the active locale plugin.
The rest of the system never needs to know which country's rules apply.
"""

from __future__ import annotations

import importlib
from datetime import datetime
from typing import Optional

try:
    from profile_manager import get_profile, get_locale
    from finance_storage import get_tax_path, get_tax_claims_path, load_json, save_json
except ImportError:
    import os, sys
    sys.path.insert(0, os.path.dirname(__file__))
    from profile_manager import get_profile, get_locale
    from finance_storage import get_tax_path, get_tax_claims_path, load_json, save_json


def _load_locale(locale_code: str):
    """Dynamically import a locale plugin."""
    try:
        return importlib.import_module(f"locales.{locale_code}")
    except ImportError:
        # Try adding project root to path
        import os, sys
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if project_root not in sys.path:
            sys.path.insert(0, project_root)
        return importlib.import_module(f"locales.{locale_code}")


def get_active_locale() -> str:
    return get_locale()


def calculate_tax_estimate(profile: Optional[dict] = None, year: Optional[int] = None) -> dict:
    """Calculate tax estimate using the active locale plugin."""
    profile = profile or get_profile() or {}
    locale_code = profile.get("tax_profile", {}).get("locale") or get_locale()
    year = year or profile.get("meta", {}).get("tax_year", datetime.now().year)

    try:
        locale = _load_locale(locale_code)
        try:
            from locales.context import LocaleContext
            ctx = LocaleContext.from_finance_profile(profile, tax_year=year)
        except (ImportError, Exception):
            ctx = profile  # fallback to dict for locales that handle it
        result = locale.calculate_tax(ctx, year)
        result["locale"] = locale_code
        result["locale_name"] = getattr(locale, "LOCALE_NAME", locale_code.upper())
        return result
    except (ImportError, AttributeError) as e:
        return {
            "error": f"Locale '{locale_code}' not available or incomplete: {e}",
            "locale": locale_code,
            "suggestion": "Use set_locale() to change locale or help build the missing locale plugin.",
        }


def generate_tax_claims(profile: Optional[dict] = None, year: Optional[int] = None, persist: bool = True) -> dict:
    """Generate tax claims using the active locale plugin."""
    profile = profile or get_profile() or {}
    locale_code = profile.get("tax_profile", {}).get("locale") or get_locale()
    year = year or profile.get("meta", {}).get("tax_year", datetime.now().year)

    try:
        locale = _load_locale(locale_code)
        try:
            from locales.context import LocaleContext
            ctx = LocaleContext.from_finance_profile(profile, tax_year=year)
        except (ImportError, Exception):
            ctx = profile  # fallback to dict for locales that handle it
        claims = locale.generate_tax_claims(ctx, year)
        payload = {
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            "locale": locale_code,
            "tax_year": year,
            "claim_count": len(claims),
            "claims": claims,
        }
        if persist:
            save_json(get_tax_claims_path(locale_code, year), payload)
        return payload
    except (ImportError, AttributeError) as e:
        return {"error": str(e), "locale": locale_code, "claims": []}


def get_tax_deadlines(profile: Optional[dict] = None, year: Optional[int] = None) -> list[dict]:
    """Get filing deadlines from the active locale plugin."""
    profile = profile or get_profile() or {}
    locale_code = profile.get("tax_profile", {}).get("locale") or get_locale()
    year = year or datetime.now().year

    try:
        locale = _load_locale(locale_code)
        return locale.get_filing_deadlines(year)
    except (ImportError, AttributeError):
        return [{"error": f"Locale '{locale_code}' has no deadline information."}]


def get_tax_rules(profile: Optional[dict] = None, year: Optional[int] = None) -> dict:
    """Get tax rules from the active locale plugin."""
    profile = profile or get_profile() or {}
    locale_code = profile.get("tax_profile", {}).get("locale") or get_locale()
    year = year or datetime.now().year

    try:
        locale = _load_locale(locale_code)
        return locale.get_tax_rules(year)
    except (ImportError, AttributeError):
        return {"error": f"Locale '{locale_code}' not available."}


_available_locales_cache: list[dict] | None = None


def get_available_locales() -> list[dict]:
    """List available locale plugins."""
    global _available_locales_cache
    if _available_locales_cache is not None:
        return _available_locales_cache

    import os
    locales_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "locales")
    available = []
    if os.path.isdir(locales_dir):
        for entry in sorted(os.listdir(locales_dir)):
            init_path = os.path.join(locales_dir, entry, "__init__.py")
            if os.path.isfile(init_path):
                try:
                    locale = _load_locale(entry)
                    available.append({
                        "code": entry,
                        "name": getattr(locale, "LOCALE_NAME", entry.upper()),
                        "years": getattr(locale, "SUPPORTED_YEARS", []),
                        "currency": getattr(locale, "CURRENCY", ""),
                    })
                except ImportError:
                    available.append({"code": entry, "name": entry.upper(), "years": [], "error": "import failed"})
    _available_locales_cache = available
    return available
