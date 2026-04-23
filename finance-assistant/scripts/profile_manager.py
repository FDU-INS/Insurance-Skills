"""
Finance Assistant Profile Manager.

Reads and writes the finance profile from project-scoped storage.
All profile data is stored as structured JSON — never raw documents.

Backwards-compatible with TaxDE profiles via migration.
"""

import json
import os
from datetime import datetime
from typing import Optional

try:
    from finance_storage import (
        get_profile_path, load_json, save_json,
        has_legacy_data, get_legacy_taxde_dir,
    )
except ImportError:
    import sys
    sys.path.insert(0, os.path.dirname(__file__))
    from finance_storage import (
        get_profile_path, load_json, save_json,
        has_legacy_data, get_legacy_taxde_dir,
    )


# ── Schema ────────────────────────────────────────────────────────────────────

PROFILE_SCHEMA = {
    "meta": {
        "version": "2.0",
        "created": None,
        "last_updated": None,
        "primary_currency": "EUR",
        "locale": "de",
        "language": "en",
        "fiscal_year_start": "01-01",
    },
    "personal": {
        "name": None,
        "city": None,
        "country": None,
        "region": None,
        "date_of_birth": None,
    },
    "employment": {
        "type": None,              # "employed"|"self_employed"|"freelancer"|"retired"|"mixed"
        "employer_count": None,
        "annual_gross": None,
        "currency": None,
        "side_income": None,
        "side_income_type": None,
    },
    "family": {
        "status": None,            # "single"|"married"|"divorced"|"civil_partnership"|"widowed"
        "partner_employed": None,
        "partner_annual_gross": None,
        "children": [],
        "dependents": [],
    },
    "housing": {
        "type": None,              # "renter"|"owner"|"mortgage"
        "monthly_rent_or_mortgage": None,
        "property_value": None,
        "mortgage_balance": None,
        "mortgage_rate": None,
        "mortgage_term_remaining_months": None,
        "homeoffice_days_per_week": None,
        "homeoffice_room_type": None,
        "commute_km": None,
        "commute_days_per_year": None,
    },
    "insurance": {
        "health_type": None,
        "health_provider": None,
        "health_monthly_premium": None,
        "policies": [],
    },
    "retirement": {
        "target_age": None,
        "current_retirement_savings": None,
        "monthly_contribution": None,
        "employer_match_pct": None,
        "pension_entitlement": None,
    },
    "tax_profile": {
        "locale": None,
        "filing_status": None,
        "tax_class": None,
        "church_tax": None,
        "extra": {},               # Locale-specific extension bucket
    },
    "preferences": {
        "risk_tolerance": None,    # "conservative"|"moderate"|"aggressive"
        "budgeting_method": None,  # "50-30-20"|"zero-based"|"envelope"|"custom"
        "debt_strategy": None,     # "avalanche"|"snowball"
        "fire_target": None,       # Annual expenses target for FIRE
    },
    "filing_history": [],
    "current_year_receipts": [],
    "law_changes_noted": [],
}

CHILD_SCHEMA = {
    "birth_year": None,
    "name": None,
    "childcare": None,
    "childcare_annual_cost": None,
    "education": None,
    "education_away_from_home": None,
}

FILING_SCHEMA = {
    "year": None,
    "refund": None,
    "filed_date": None,
    "filed_via": None,
    "reviewed": False,
    "notes": "",
}

RECEIPT_SCHEMA = {
    "date": None,
    "category": None,
    "description": None,
    "amount": None,
    "currency": None,
    "business_use_pct": 100.0,
    "deductible_amount": None,
    "tax_relevant": False,
    "document_ref": None,
}


# ── Storage helpers ──────────────────────────────────────────────────────────

def _load_raw() -> dict:
    path = get_profile_path()
    data = load_json(path, default={})
    if data:
        return data

    # Check for legacy TaxDE profile
    if has_legacy_data():
        legacy_path = get_legacy_taxde_dir() / "taxde_profile.json"
        legacy = load_json(legacy_path, default={})
        if legacy:
            return _migrate_taxde_profile(legacy)

    return {}


def _save_raw(data: dict) -> None:
    save_json(get_profile_path(), data)


def _migrate_taxde_profile(taxde: dict) -> dict:
    """Convert a TaxDE profile to the Finance Assistant schema."""
    profile = json.loads(json.dumps(PROFILE_SCHEMA))  # deep copy
    profile["meta"]["created"] = taxde.get("meta", {}).get("created")
    profile["meta"]["last_updated"] = datetime.now().isoformat()
    profile["meta"]["locale"] = "de"
    profile["meta"]["language"] = taxde.get("meta", {}).get("language", "de")

    # Personal
    personal = taxde.get("personal", {})
    profile["personal"]["name"] = personal.get("name")
    profile["personal"]["city"] = personal.get("city")
    profile["personal"]["country"] = "DE"
    profile["personal"]["region"] = personal.get("bundesland")

    # Employment — map German types to generic
    emp = taxde.get("employment", {})
    type_map = {
        "angestellter": "employed", "freelancer": "freelancer",
        "freiberufler": "freelancer", "gewerbe": "self_employed",
        "mixed": "mixed", "rentner": "retired",
    }
    profile["employment"]["type"] = type_map.get(emp.get("type"), emp.get("type"))
    profile["employment"]["employer_count"] = emp.get("employer_count")
    profile["employment"]["annual_gross"] = emp.get("annual_gross")
    profile["employment"]["currency"] = "EUR"
    if emp.get("nebenjob"):
        profile["employment"]["side_income"] = emp.get("nebenjob_income")
        profile["employment"]["side_income_type"] = emp.get("nebenjob_type")

    # Family
    fam = taxde.get("family", {})
    profile["family"]["status"] = fam.get("status")
    profile["family"]["partner_employed"] = fam.get("partner_employed")
    profile["family"]["partner_annual_gross"] = fam.get("partner_annual_gross")
    for child in fam.get("children", []):
        profile["family"]["children"].append({
            "birth_year": child.get("birth_year"),
            "childcare": child.get("kita"),
            "childcare_annual_cost": child.get("kita_annual_cost"),
            "education": child.get("ausbildung"),
            "education_away_from_home": child.get("ausbildung_away"),
        })

    # Housing
    housing = taxde.get("housing", {})
    type_map_h = {"mieter": "renter", "eigentuemer": "owner"}
    profile["housing"]["type"] = type_map_h.get(housing.get("type"), housing.get("type"))
    profile["housing"]["homeoffice_days_per_week"] = housing.get("homeoffice_days_per_week")
    profile["housing"]["homeoffice_room_type"] = housing.get("homeoffice_room_type")
    profile["housing"]["commute_km"] = housing.get("commute_km")
    profile["housing"]["commute_days_per_year"] = housing.get("commute_days_per_year")

    # Insurance
    ins = taxde.get("insurance", {})
    profile["insurance"]["health_type"] = ins.get("krankenkasse_type")
    profile["insurance"]["health_provider"] = ins.get("krankenkasse_provider")

    # Tax profile — German-specific fields
    profile["tax_profile"]["locale"] = "de"
    profile["tax_profile"]["tax_class"] = emp.get("steuerklasse")
    profile["tax_profile"]["church_tax"] = personal.get("kirchensteuer")
    profile["tax_profile"]["extra"] = {
        "kirchensteuer_denomination": personal.get("kirchensteuer_denomination"),
        "zusatzbeitrag_rate": ins.get("zusatzbeitrag_rate"),
        "riester": ins.get("riester"),
        "riester_contribution": ins.get("riester_contribution"),
        "ruerup": ins.get("ruerup"),
        "ruerup_contribution": ins.get("ruerup_contribution"),
        "bav": ins.get("bav"),
        "bav_contribution": ins.get("bav_contribution"),
        "expat": taxde.get("special", {}).get("expat"),
        "dba_relevant": taxde.get("special", {}).get("dba_relevant"),
        "disability_grade": taxde.get("special", {}).get("disability_grade"),
        "gewerkschaft_beitrag": taxde.get("special", {}).get("gewerkschaft_beitrag"),
    }

    # Filing history
    profile["filing_history"] = taxde.get("filing_history", [])
    profile["current_year_receipts"] = taxde.get("current_year_receipts", [])
    profile["law_changes_noted"] = taxde.get("law_changes_noted", [])

    return profile


# ── Public API ───────────────────────────────────────────────────────────────

def get_profile() -> dict:
    return _load_raw()


def update_profile(updates: dict) -> dict:
    profile = _load_raw()

    def deep_merge(base: dict, overlay: dict) -> dict:
        result = dict(base)
        for k, v in overlay.items():
            if k in result and isinstance(result[k], dict) and isinstance(v, dict):
                result[k] = deep_merge(result[k], v)
            else:
                result[k] = v
        return result

    if not profile:
        profile = json.loads(json.dumps(PROFILE_SCHEMA))
        profile["meta"]["created"] = datetime.now().isoformat()

    profile["meta"]["last_updated"] = datetime.now().isoformat()
    merged = deep_merge(profile, updates)
    _save_raw(merged)
    return merged


def add_child(child_data: dict) -> dict:
    profile = get_profile() or {}
    children = profile.get("family", {}).get("children", [])
    new_child = dict(CHILD_SCHEMA)
    new_child.update(child_data)
    children.append(new_child)
    return update_profile({"family": {"children": children}})


def add_filing_year(filing_data: dict) -> dict:
    profile = get_profile() or {}
    history = profile.get("filing_history", [])
    year = filing_data.get("year")
    history = [h for h in history if h.get("year") != year]
    new_entry = dict(FILING_SCHEMA)
    new_entry.update(filing_data)
    history.append(new_entry)
    history.sort(key=lambda x: x.get("year", 0))
    return update_profile({"filing_history": history})


def delete_profile() -> bool:
    try:
        from finance_storage import get_finance_dir
        from data_safety import delete_all_data, get_data_inventory
        # Only consider it a real deletion if there is actual data present
        inventory = get_data_inventory()
        if inventory.get("status") == "no_data" or inventory.get("total_files", 0) == 0:
            return False
        result = delete_all_data(confirm=True)
        return result.get("action") == "deleted"
    except ImportError:
        # fallback: just delete the profile file
        path = get_profile_path()
        if path.exists():
            path.unlink()
            return True
        return False


def display_profile(compact: bool = False) -> str:
    p = get_profile()
    if not p:
        return "No finance profile found. Start a conversation to create one."

    if compact:
        meta = p.get("meta", {})
        emp = p.get("employment", {})
        personal = p.get("personal", {})
        currency = meta.get("primary_currency", "EUR")
        locale = meta.get("locale", "—")
        emp_type = emp.get("type", "")
        gross = emp.get("annual_gross")
        gross_str = f" €{gross/1000:.0f}k" if gross else ""
        emp_summary = f"{emp_type}{gross_str}" if emp_type else ""
        city = personal.get("city") or personal.get("region") or ""
        last_updated = (meta.get("last_updated") or "—")[:10]
        parts = [currency, locale]
        if emp_summary:
            parts.append(f"employed {emp_summary}" if emp_type == "employed" else emp_summary)
        if city:
            parts.append(city)
        parts.append(f"Last updated: {last_updated}")
        return " | ".join(parts)

    lines = ["═══ Your Finance Profile ═══\n"]

    meta = p.get("meta", {})
    lines.append(f"Currency: {meta.get('primary_currency', '—')}  |  "
                 f"Locale: {meta.get('locale', '—')}  |  "
                 f"Last updated: {(meta.get('last_updated') or '—')[:10]}")

    personal = p.get("personal", {})
    if personal.get("name"):
        lines.append(f"\nName: {personal['name']}")
    loc_parts = [personal.get("city"), personal.get("region"), personal.get("country")]
    loc = ", ".join(x for x in loc_parts if x)
    if loc:
        lines.append(f"Location: {loc}")

    emp = p.get("employment", {})
    if emp.get("type"):
        lines.append(f"\nEmployment: {emp['type']}")
    if emp.get("annual_gross"):
        cur = emp.get("currency") or meta.get("primary_currency", "EUR")
        lines.append(f"Annual gross: {cur} {emp['annual_gross']:,.0f}")
    if emp.get("side_income"):
        lines.append(f"Side income: {emp.get('side_income_type', 'misc')} — {emp['side_income']:,.0f}")

    fam = p.get("family", {})
    if fam.get("status"):
        lines.append(f"\nFamily: {fam['status']}")
    children = fam.get("children", [])
    if children:
        lines.append(f"Children: {len(children)}")

    housing = p.get("housing", {})
    if housing.get("type"):
        lines.append(f"\nHousing: {housing['type']}")
    if housing.get("monthly_rent_or_mortgage"):
        lines.append(f"Monthly housing cost: {housing['monthly_rent_or_mortgage']:,.0f}")

    ret = p.get("retirement", {})
    if ret.get("target_age"):
        lines.append(f"\nRetirement target: age {ret['target_age']}")
    if ret.get("current_retirement_savings"):
        lines.append(f"Retirement savings: {ret['current_retirement_savings']:,.0f}")

    prefs = p.get("preferences", {})
    pref_parts = []
    if prefs.get("risk_tolerance"):
        pref_parts.append(f"risk: {prefs['risk_tolerance']}")
    if prefs.get("budgeting_method"):
        pref_parts.append(f"budget: {prefs['budgeting_method']}")
    if prefs.get("debt_strategy"):
        pref_parts.append(f"debt: {prefs['debt_strategy']}")
    if pref_parts:
        lines.append(f"\nPreferences: {', '.join(pref_parts)}")

    return "\n".join(lines)


def get_missing_fields() -> list:
    p = get_profile()
    if not p:
        return ["entire profile — not yet created"]

    missing = []
    checks = [
        ("employment.annual_gross", p.get("employment", {}).get("annual_gross")),
        ("employment.type", p.get("employment", {}).get("type")),
        ("personal.country", p.get("personal", {}).get("country")),
        ("family.status", p.get("family", {}).get("status")),
        ("housing.type", p.get("housing", {}).get("type")),
        ("housing.monthly_rent_or_mortgage", p.get("housing", {}).get("monthly_rent_or_mortgage")),
        ("meta.primary_currency", p.get("meta", {}).get("primary_currency")),
        ("meta.locale", p.get("meta", {}).get("locale")),
    ]
    for field, value in checks:
        if value is None:
            missing.append(field)
    return missing


def get_profile_completeness_pct() -> int:
    all_fields = [
        "employment.annual_gross", "employment.type",
        "personal.name", "personal.country",
        "family.status",
        "housing.type", "housing.monthly_rent_or_mortgage",
        "meta.primary_currency", "meta.locale",
        "retirement.target_age",
        "preferences.risk_tolerance",
    ]
    missing = get_missing_fields()
    filled = len(all_fields) - len([m for m in missing if m in all_fields])
    return int(filled / len(all_fields) * 100)


def get_locale() -> str:
    p = get_profile()
    return p.get("meta", {}).get("locale") or p.get("tax_profile", {}).get("locale") or "de"


def get_primary_currency() -> str:
    p = get_profile()
    return p.get("meta", {}).get("primary_currency") or "EUR"


def set_locale(locale_code: str) -> dict:
    return update_profile({"meta": {"locale": locale_code}, "tax_profile": {"locale": locale_code}})


if __name__ == "__main__":
    import tempfile
    print("Testing profile_manager...")
    with tempfile.TemporaryDirectory() as tmpdir:
        os.environ["FINANCE_PROJECT_DIR"] = tmpdir
        delete_profile()
        assert get_profile() == {}

        update_profile({
            "meta": {"primary_currency": "EUR", "locale": "de"},
            "personal": {"name": "Max Mustermann", "city": "Berlin", "country": "DE"},
            "employment": {"type": "employed", "annual_gross": 65000, "currency": "EUR"},
        })
        p = get_profile()
        assert p["personal"]["name"] == "Max Mustermann"
        assert p["employment"]["annual_gross"] == 65000

        print(display_profile())
        print("Missing fields:", get_missing_fields())
        print("Completeness:", get_profile_completeness_pct(), "%")
        delete_profile()
        del os.environ["FINANCE_PROJECT_DIR"]
        print("All tests passed.")
