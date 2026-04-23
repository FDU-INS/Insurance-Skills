"""Shared pytest fixtures for Finance Assistant tests."""

import os
import sys
import shutil
import tempfile
import pytest

# Ensure scripts/ and project root are on path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(PROJECT_ROOT, "scripts")
for p in (PROJECT_ROOT, SCRIPTS_DIR):
    if p not in sys.path:
        sys.path.insert(0, p)


@pytest.fixture(autouse=True)
def isolated_finance_dir(tmp_path, monkeypatch):
    """Every test gets its own .finance/ directory."""
    monkeypatch.setenv("FINANCE_PROJECT_DIR", str(tmp_path))
    yield tmp_path


@pytest.fixture
def sample_profile():
    """A realistic Berlin-based profile for testing."""
    return {
        "meta": {"primary_currency": "EUR", "locale": "de", "language": "en", "tax_year": 2026},
        "personal": {"name": "Max Mustermann", "city": "Berlin", "country": "DE", "region": "Berlin"},
        "employment": {"type": "employed", "annual_gross": 65000, "currency": "EUR"},
        "family": {"status": "single", "children": []},
        "housing": {
            "type": "renter", "monthly_rent_or_mortgage": 1200,
            "homeoffice_days_per_week": 3, "commute_km": 15, "commute_days_per_year": 100,
        },
        "tax_profile": {"locale": "de", "tax_class": "I", "church_tax": False, "extra": {}},
        "insurance": {"health_type": "gesetzlich", "health_provider": "TK"},
        "retirement": {"target_age": 65},
        "preferences": {"risk_tolerance": "moderate", "debt_strategy": "avalanche"},
    }
