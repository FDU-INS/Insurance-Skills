"""
Dynamic locale loading and on-demand locale building.

Locales are Python packages in the locales/ directory. When a locale
is not available, this module creates a skeleton directory for it.
"""

from __future__ import annotations

import importlib
import os
from pathlib import Path
from typing import Optional


def _locales_dir() -> Path:
    return Path(__file__).parent.parent / "locales"


def load_locale(locale_code: str):
    """Dynamically import a locale plugin. Raises ImportError if not found."""
    import sys
    project_root = str(Path(__file__).parent.parent)
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    return importlib.import_module(f"locales.{locale_code}")


def is_locale_available(locale_code: str) -> bool:
    """Check if a locale plugin exists and can be imported."""
    try:
        load_locale(locale_code)
        return True
    except ImportError:
        return False


def get_available_locales() -> list[str]:
    """List all available locale codes."""
    locales_path = _locales_dir()
    if not locales_path.is_dir():
        return []
    return sorted(
        d.name for d in locales_path.iterdir()
        if d.is_dir() and (d / "__init__.py").is_file()
    )


def build_locale_on_demand(locale_code: str) -> dict:
    """
    Create a skeleton locale directory for a new country.
    Returns a manifest of what was created and what needs to be populated.
    """
    locale_dir = _locales_dir() / locale_code
    if locale_dir.exists() and (locale_dir / "__init__.py").exists():
        return {"status": "already_exists", "path": str(locale_dir)}

    locale_dir.mkdir(parents=True, exist_ok=True)

    init_content = f'''"""
{locale_code.upper()} locale plugin for Finance Assistant.

This is a skeleton — fill in the tax rules, deadlines, and social contributions
for your country.
"""

LOCALE_CODE = "{locale_code}"
LOCALE_NAME = "{locale_code.upper()}"
SUPPORTED_YEARS = []
CURRENCY = ""


def get_tax_rules(year: int) -> dict:
    raise NotImplementedError(f"Tax rules for {{LOCALE_NAME}} year {{year}} not yet implemented.")


def calculate_tax(profile: dict, year: int = None) -> dict:
    raise NotImplementedError(f"Tax calculation for {{LOCALE_NAME}} not yet implemented.")


def get_filing_deadlines(year: int) -> list[dict]:
    return []


def get_social_contributions(gross: float, year: int) -> dict:
    raise NotImplementedError(f"Social contributions for {{LOCALE_NAME}} not yet implemented.")


def get_deduction_categories() -> list[dict]:
    return []


def generate_tax_claims(profile: dict, year: int = None) -> list[dict]:
    return []
'''

    (locale_dir / "__init__.py").write_text(init_content, encoding="utf-8")

    return {
        "status": "created_skeleton",
        "path": str(locale_dir),
        "files_created": ["__init__.py"],
        "next_steps": [
            f"Set LOCALE_NAME, CURRENCY, and SUPPORTED_YEARS in locales/{locale_code}/__init__.py",
            f"Add tax_rules.py with year-specific parameters",
            f"Add tax_calculator.py with calculation logic",
            f"Add tax_dates.py with filing deadlines",
            f"Add social_contributions.py if applicable",
        ],
    }
