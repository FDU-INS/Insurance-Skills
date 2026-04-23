"""
Guided onboarding wizard for new Finance Assistant users.
7 steps, saves progress after each step, resumable.
State stored in .finance/onboarding_state.json
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any

try:
    from finance_storage import get_finance_dir, save_json, load_json
    from profile_manager import update_profile, get_profile
except ImportError:
    import sys
    sys.path.insert(0, os.path.dirname(__file__))
    from finance_storage import get_finance_dir, save_json, load_json
    from profile_manager import update_profile, get_profile


STEPS = [
    "basics",       # name, country, currency
    "employment",   # type, gross income, employer
    "housing",      # rent/own, monthly cost, location
    "accounts",     # at least one bank account
    "goals",        # at least one savings goal
    "tax",          # locale-specific: Steuerklasse / tax code / etc.
    "budget",       # auto-suggest 50/30/20 or custom
]

STEP_LABELS = {
    "basics": "Basics",
    "employment": "Employment",
    "housing": "Housing",
    "accounts": "Accounts",
    "goals": "Savings Goals",
    "tax": "Tax",
    "budget": "Budget",
}

# Country code → locale mapping
_COUNTRY_TO_LOCALE: dict[str, str] = {
    "germany": "de", "deutschland": "de", "de": "de",
    "uk": "gb", "united kingdom": "gb", "england": "gb", "gb": "gb", "britain": "gb",
    "france": "fr", "frankreich": "fr", "fr": "fr",
    "netherlands": "nl", "holland": "nl", "nl": "nl",
    "poland": "pl", "polska": "pl", "pl": "pl",
    "austria": "at", "österreich": "at", "at": "at",
    "switzerland": "ch", "schweiz": "ch", "ch": "ch",
    "usa": "us", "us": "us", "united states": "us", "america": "us",
}

_COUNTRY_CURRENCY: dict[str, str] = {
    "de": "EUR", "fr": "EUR", "nl": "EUR", "at": "EUR",
    "gb": "GBP",
    "ch": "CHF",
    "pl": "PLN",
    "us": "USD",
}


# ── State file ────────────────────────────────────────────────────────────────

def _get_state_path() -> Path:
    return get_finance_dir() / "onboarding_state.json"


def get_onboarding_state() -> dict:
    """Load current onboarding state from .finance/onboarding_state.json"""
    path = _get_state_path()
    default: dict[str, Any] = {
        "completed_steps": [],
        "skipped_steps": [],
        "step_data": {},
        "started": False,
    }
    return load_json(path, default=default) or default


def save_onboarding_state(state: dict) -> None:
    """Save onboarding state atomically."""
    save_json(_get_state_path(), state)


# ── Progress queries ──────────────────────────────────────────────────────────

def is_onboarding_complete() -> bool:
    """True if all 7 steps completed or skipped."""
    state = get_onboarding_state()
    done = set(state.get("completed_steps", [])) | set(state.get("skipped_steps", []))
    return all(s in done for s in STEPS)


def get_current_step() -> str:
    """Return the current incomplete step name, or 'complete'."""
    state = get_onboarding_state()
    done = set(state.get("completed_steps", [])) | set(state.get("skipped_steps", []))
    for step in STEPS:
        if step not in done:
            return step
    return "complete"


def get_step_progress() -> dict:
    """
    Return:
    {
      "current_step": str,
      "step_number": int,       # 1-7
      "total_steps": int,       # 7
      "completed_steps": [str],
      "remaining_steps": [str],
      "pct_complete": int,
    }
    """
    state = get_onboarding_state()
    completed = state.get("completed_steps", [])
    skipped = state.get("skipped_steps", [])
    done = set(completed) | set(skipped)

    current = get_current_step()
    remaining = [s for s in STEPS if s not in done]

    if current == "complete":
        step_number = len(STEPS)
    else:
        step_number = STEPS.index(current) + 1

    total = len(STEPS)
    finished_count = len(done)
    pct = int(finished_count / total * 100)

    return {
        "current_step": current,
        "step_number": step_number,
        "total_steps": total,
        "completed_steps": completed,
        "skipped_steps": skipped,
        "remaining_steps": remaining,
        "pct_complete": pct,
    }


# ── Prompts ───────────────────────────────────────────────────────────────────

def get_step_prompt(step: str, locale: str = "de") -> str:
    """
    Return the question Claude should ask for this step.
    Includes progress indicator and examples.
    """
    idx = STEPS.index(step) + 1 if step in STEPS else 0
    total = len(STEPS)

    if step == "basics":
        return (
            f"Step {idx} of {total} — Let's get started!\n\n"
            "What's your name, and which country are you in?\n"
            "(e.g. 'I'm Alex, based in Germany' or just 'Germany' is fine)"
        )

    if step == "employment":
        return (
            f"Step {idx} of {total} — Employment\n\n"
            "Are you employed, self-employed, or freelance?\n"
            "And roughly what's your gross annual income?\n"
            "(e.g. 'Employed, €65k/year' or 'Freelancer, about €80k')"
        )

    if step == "housing":
        return (
            f"Step {idx} of {total} — Housing\n\n"
            "Do you rent or own? What's your monthly housing cost (rent or mortgage)?\n"
            "(e.g. 'Renting in Berlin, €1,200/month')"
        )

    if step == "accounts":
        return (
            f"Step {idx} of {total} — Accounts\n\n"
            "What bank(s) do you use? I'll track balances and transactions per account.\n"
            "(e.g. 'DKB checking, ING savings' — no account numbers needed)"
        )

    if step == "goals":
        return (
            f"Step {idx} of {total} — Savings Goals\n\n"
            "What are you saving for? Name a goal, target amount, and rough timeline.\n"
            "(e.g. 'Emergency fund €10k by end of year' or 'Trip to Japan €3k in 8 months')"
        )

    if step == "tax":
        if locale == "de":
            return (
                f"Step {idx} of {total} — Tax\n\n"
                "A few German tax questions:\n"
                "• Steuerklasse (1–6)?\n"
                "• Do you pay Kirchensteuer?\n"
                "• Bundesland? (affects Kirchensteuer rate)\n"
                "(e.g. 'Klasse 1, no Kirchensteuer, Berlin')"
            )
        if locale == "gb":
            return (
                f"Step {idx} of {total} — Tax\n\n"
                "A couple of UK tax questions:\n"
                "• What's your tax code? (e.g. 1257L)\n"
                "• Do you file a Self Assessment return?\n"
                "(e.g. '1257L, no self-assessment')"
            )
        if locale == "fr":
            return (
                f"Step {idx} of {total} — Tax\n\n"
                "Quelques questions sur votre situation fiscale :\n"
                "• Situation familiale (célibataire, marié·e, pacsé·e) ?\n"
                "• Nombre de parts fiscales ?\n"
                "(e.g. 'Célibataire, 1 part')"
            )
        if locale == "nl":
            return (
                f"Step {idx} of {total} — Tax\n\n"
                "One quick Dutch tax question:\n"
                "• Do your Box 3 assets (savings + investments) exceed €57,000?\n"
                "(e.g. 'No, well under that threshold')"
            )
        if locale == "pl":
            return (
                f"Step {idx} of {total} — Tax\n\n"
                "Kilka pytań podatkowych:\n"
                "• Czy masz mniej niż 26 lat? (ulga dla młodych)\n"
                "• Czy rozliczasz się wspólnie z małżonkiem?\n"
                "(np. 'Tak, mam 24 lata' lub 'Nie, rozliczam się samodzielnie')"
            )
        # Generic fallback
        return (
            f"Step {idx} of {total} — Tax\n\n"
            "A few tax questions to help with planning:\n"
            "• What's your filing status? (single, married, etc.)\n"
            "• Any special tax situations worth noting?\n"
            "(Keep it brief — we can go deeper later)"
        )

    if step == "budget":
        profile = get_profile() or {}
        emp = profile.get("employment", {})
        gross = emp.get("annual_gross")
        currency = profile.get("meta", {}).get("primary_currency", "EUR")
        if gross:
            monthly = gross / 12
            needs = monthly * 0.50
            wants = monthly * 0.30
            savings = monthly * 0.20
            income_line = (
                f"Based on your income of {currency} {monthly:,.0f}/month, that's:\n"
                f"  Needs {currency} {needs:,.0f} | Wants {currency} {wants:,.0f} | "
                f"Savings {currency} {savings:,.0f}"
            )
        else:
            income_line = "Enter your monthly take-home and I'll calculate the splits."

        return (
            f"Step {idx} of {total} — Budget\n\n"
            "I can set up a budget automatically using the 50/30/20 rule:\n"
            "  • 50% needs (housing, food, transport)\n"
            "  • 30% wants (dining out, entertainment, subscriptions)\n"
            "  • 20% savings & debt\n\n"
            f"{income_line}\n\n"
            "Shall I use this, or would you like to adjust?"
        )

    return f"Step {idx} of {total} — {STEP_LABELS.get(step, step)}\n\nLet's set up your {step}."


# ── Parse responses ───────────────────────────────────────────────────────────

def parse_step_response(step: str, user_text: str, locale: str = "de") -> dict:
    """
    Extract structured data from a natural language response.
    Returns a dict of extracted fields, or {"needs_clarification": True, "question": str}.
    Uses regex + heuristics — deterministic, no LLM calls.
    """
    text = user_text.strip()
    lower = text.lower()

    if step == "basics":
        return _parse_basics(text, lower)

    if step == "employment":
        return _parse_employment(text, lower)

    if step == "housing":
        return _parse_housing(text, lower)

    if step == "accounts":
        return _parse_accounts(text, lower)

    if step == "goals":
        return _parse_goals(text, lower)

    if step == "tax":
        return _parse_tax(text, lower, locale)

    if step == "budget":
        return _parse_budget(text, lower)

    return {"raw": text}


def _parse_basics(text: str, lower: str) -> dict:
    result: dict[str, Any] = {}

    # Extract name — "I'm Alex", "my name is Alex", "I am Alex"
    name_match = re.search(
        r"(?:i(?:'m| am)|my name is|name[:\s]+)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)",
        text, re.IGNORECASE
    )
    if name_match:
        result["name"] = name_match.group(1).strip()

    # Extract country
    for country_str, code in _COUNTRY_TO_LOCALE.items():
        if re.search(r'\b' + re.escape(country_str) + r'\b', lower):
            result["country"] = code.upper()
            result["locale"] = code
            result["currency"] = _COUNTRY_CURRENCY.get(code, "EUR")
            break

    if not result:
        return {"needs_clarification": True, "question": "Could you tell me your name and country?"}

    return result


def _parse_employment(text: str, lower: str) -> dict:
    result: dict[str, Any] = {}

    # Employment type
    if re.search(r'\b(self.?employed|selbst.?st[äa]ndig)\b', lower):
        result["employment_type"] = "self_employed"
    elif re.search(r'\bfreelance[rd]?\b', lower):
        result["employment_type"] = "freelancer"
    elif re.search(r'\b(employed|angestellt|employee)\b', lower):
        result["employment_type"] = "employed"
    elif re.search(r'\b(retired|rentner|pension)\b', lower):
        result["employment_type"] = "retired"

    # Gross income — match €65k, €65,000, 65k, 65000, £80k, $90k, 80.000
    amount_match = re.search(
        r'(?:[€£$]|eur|gbp|usd)?\s*'
        r'(\d{1,3}(?:[.,]\d{3})*(?:\.\d+)?|\d+)\s*'
        r'(k|tsd\.?|thousand)?'
        r'(?:\s*(?:euro|euros|EUR|GBP|USD|CHF|PLN))?'
        r'(?:\s*/?\s*(?:year|yr|p\.a\.|pa|annual|jährlich))?',
        lower
    )
    if amount_match:
        raw = amount_match.group(1).replace(",", "").replace(".", "")
        # Handle European decimal: 65.000 → 65000
        if "." in amount_match.group(1) and amount_match.group(1).count(".") == 1:
            parts = amount_match.group(1).split(".")
            if len(parts[1]) == 3:
                raw = amount_match.group(1).replace(".", "")
        try:
            val = float(raw)
            if amount_match.group(2):  # k / tsd
                val *= 1000
            if val > 0:
                result["gross_annual"] = int(val)
        except ValueError:
            pass

    if not result:
        return {"needs_clarification": True, "question": "Are you employed, self-employed, or freelance? And roughly what's your gross annual income?"}

    return result


def _parse_housing(text: str, lower: str) -> dict:
    result: dict[str, Any] = {}

    # Housing type
    if re.search(r'\b(rent(ing|er)?|miete[rn]?|tenant)\b', lower):
        result["housing_type"] = "rent"
    elif re.search(r'\b(mortgage|hypothek|mortgaged)\b', lower):
        result["housing_type"] = "mortgage"
    elif re.search(r'\b(own(er)?|eigentuemer|eigentümer|bought|freehold)\b', lower):
        result["housing_type"] = "own"

    # Monthly cost
    cost_match = re.search(
        r'(?:[€£$])?\s*(\d{1,3}(?:[.,]\d{3})*|\d+)'
        r'\s*(?:[€£$])?\s*(?:/\s*(?:month|mo|monat))?',
        lower
    )
    if cost_match:
        raw = cost_match.group(1).replace(",", "").replace(".", "")
        if "." in cost_match.group(1):
            parts = cost_match.group(1).split(".")
            if len(parts[1]) == 3:
                raw = cost_match.group(1).replace(".", "")
        try:
            val = int(raw)
            if 100 <= val <= 20000:
                result["monthly_cost"] = val
        except ValueError:
            pass

    # City — common pattern: "in Berlin", "in Munich", "in London"
    city_match = re.search(r'\bin\s+([A-Z][a-zA-Zä-üÄ-Ü\s\-]+?)(?:\s*[,\.€£$\d]|$)', text)
    if city_match:
        city = city_match.group(1).strip().rstrip(",.")
        if len(city) > 1 and city.lower() not in ("a", "the", "an"):
            result["city"] = city

    if not result:
        return {"needs_clarification": True, "question": "Do you rent or own? What's your monthly housing cost?"}

    return result


def _parse_accounts(text: str, lower: str) -> dict:
    result: dict[str, Any] = {}
    accounts = []

    # Common banks and account type keywords
    bank_pattern = re.compile(
        r'\b(dkb|ing|sparkasse|volksbank|commerzbank|deutsche bank|n26|revolut|'
        r'barclays|lloyds|hsbc|natwest|santander|monzo|starling|wise|'
        r'bnp|socgen|crédit agricole|bnp paribas|abn amro|rabobank|'
        r'pkobp|pko|mbank|ing bank)\b',
        re.IGNORECASE
    )
    type_pattern = re.compile(r'\b(checking|current|savings?|depot|brokerage|investment|tagesgeld|girokonto)\b', re.IGNORECASE)

    for bank_match in bank_pattern.finditer(text):
        bank_name = bank_match.group(1)
        start = bank_match.start()
        # Look for account type nearby (within 30 chars before/after)
        context = text[max(0, start - 30):start + 30].lower()
        type_m = type_pattern.search(context)
        acc_type = type_m.group(1).lower() if type_m else "checking"
        # Normalize
        if acc_type in ("current", "girokonto"):
            acc_type = "checking"
        elif acc_type in ("tagesgeld",):
            acc_type = "savings"
        accounts.append({"bank": bank_name, "type": acc_type})

    # Also parse free-form "X checking, Y savings"
    if not accounts:
        free_pattern = re.compile(
            r'([A-Za-z][A-Za-z\s]+?)\s+(checking|current|savings?|depot|brokerage)',
            re.IGNORECASE
        )
        for m in free_pattern.finditer(text):
            bank = m.group(1).strip()
            acc_type = m.group(2).lower()
            if acc_type in ("current",):
                acc_type = "checking"
            if len(bank) <= 40:
                accounts.append({"bank": bank, "type": acc_type})

    if accounts:
        result["accounts"] = accounts
    else:
        # Store raw text as fallback
        result["accounts_raw"] = text

    return result


def _parse_goals(text: str, lower: str) -> dict:
    result: dict[str, Any] = {}
    goals = []

    # Amount: €10k, €3,000, 10000
    amounts = re.findall(
        r'(?:[€£$])?\s*(\d{1,3}(?:[.,]\d{3})*|\d+)\s*(k|tsd\.?)?'
        r'\s*(?:euro|euros|EUR|GBP|USD)?',
        lower
    )
    parsed_amounts = []
    for raw, suffix in amounts:
        raw_clean = raw.replace(",", "").replace(".", "")
        try:
            val = float(raw_clean)
            if suffix:
                val *= 1000
            if val >= 100:
                parsed_amounts.append(int(val))
        except ValueError:
            pass

    # Timeline: "by end of year", "in 8 months", "by Dec 2025"
    timeline_match = re.search(
        r'(?:by\s+(?:end of\s+)?(?:the\s+)?year|'
        r'in\s+(\d+)\s+months?|'
        r'by\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s*\d{4}|'
        r'by\s+\d{4})',
        lower
    )
    timeline = timeline_match.group(0) if timeline_match else None

    # Goal name heuristics
    goal_keywords = re.search(
        r'\b(emergency fund|notgroschen|trip|vacation|urlaub|car|auto|house|'
        r'wedding|hochzeit|education|ausbildung|retirement|rente|laptop|'
        r'investment|anlage)\b',
        lower
    )
    goal_name = goal_keywords.group(1).title() if goal_keywords else "Savings Goal"

    goals.append({
        "name": goal_name,
        "target_amount": parsed_amounts[0] if parsed_amounts else None,
        "timeline": timeline,
        "raw": text,
    })

    result["goals"] = goals
    return result


def _parse_tax(text: str, lower: str, locale: str) -> dict:
    result: dict[str, Any] = {}

    if locale == "de":
        # Steuerklasse 1–6
        sk_match = re.search(r'(?:klasse|class|steuerklasse)?\s*([1-6])\b', lower)
        if sk_match:
            result["steuerklasse"] = int(sk_match.group(1))
        # Also match "Klasse IV" roman numeral
        sk_roman = re.search(r'klasse\s+(I{1,3}|IV|V|VI)\b', lower, re.IGNORECASE)
        if sk_roman and "steuerklasse" not in result:
            roman_map = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6}
            result["steuerklasse"] = roman_map.get(sk_roman.group(1).upper(), 1)

        # Kirchensteuer
        if re.search(r'\b(no|ohne|kein[e]?)\s+kirchensteuer\b', lower):
            result["kirchensteuer"] = False
        elif re.search(r'\bkirchensteuer\b', lower):
            result["kirchensteuer"] = True

        # Bundesland
        bundeslaender = [
            "Berlin", "Bavaria", "Bayern", "Baden-Württemberg", "Brandenburg",
            "Bremen", "Hamburg", "Hessen", "Mecklenburg-Vorpommern",
            "Niedersachsen", "Nordrhein-Westfalen", "NRW", "Rheinland-Pfalz",
            "Saarland", "Sachsen", "Sachsen-Anhalt", "Schleswig-Holstein",
            "Thüringen",
        ]
        for bl in bundeslaender:
            if bl.lower() in lower:
                result["bundesland"] = bl
                break

    elif locale == "gb":
        # Tax code e.g. 1257L
        tax_code_match = re.search(r'\b(\d{3,4}[LMN])\b', text.upper())
        if tax_code_match:
            result["tax_code"] = tax_code_match.group(1)
        # Self assessment
        if re.search(r'\b(no|not|don.t)\s+(do\s+)?self.?assess', lower):
            result["self_assessment"] = False
        elif re.search(r'\bself.?assess', lower):
            result["self_assessment"] = True

    elif locale == "fr":
        # Situation familiale
        if re.search(r'\b(celibataire|célibataire|single)\b', lower):
            result["situation_familiale"] = "celibataire"
        elif re.search(r'\b(mari[ée]|married)\b', lower):
            result["situation_familiale"] = "marie"
        elif re.search(r'\b(pacs[ée]?|civil partnership)\b', lower):
            result["situation_familiale"] = "pacse"
        # Parts
        parts_match = re.search(r'(\d+(?:[.,]\d)?)\s+parts?', lower)
        if parts_match:
            try:
                result["parts_fiscales"] = float(parts_match.group(1).replace(",", "."))
            except ValueError:
                pass

    elif locale == "nl":
        # Box 3 threshold
        if re.search(r'\b(no|nee|not|under|below|beneath)\b', lower):
            result["box3_above_threshold"] = False
        elif re.search(r'\b(yes|ja|above|over)\b', lower):
            result["box3_above_threshold"] = True

    elif locale == "pl":
        # Under 26 (ulga dla młodych)
        age_match = re.search(r'\b(2[0-5])\s+(?:lat|year)', lower)
        if age_match:
            result["under_26"] = int(age_match.group(1)) < 26
        elif re.search(r'\b(tak|yes)\b.*\b26\b|\b26\b.*\b(tak|yes)\b', lower):
            result["under_26"] = True
        elif re.search(r'\b(nie|no)\b', lower):
            result["under_26"] = False

        # Joint filing
        if re.search(r'\b(wspólnie|joint(ly)?|razem)\b', lower):
            result["joint_filing"] = True
        elif re.search(r'\b(samodzielnie|individual|sam|sama)\b', lower):
            result["joint_filing"] = False

    if not result:
        result["tax_raw"] = text

    return result


def _parse_budget(text: str, lower: str) -> dict:
    result: dict[str, Any] = {}

    if re.search(r'\b(yes|yeah|sure|ok|okay|sounds good|go ahead|use it|fine|perfect|great)\b', lower):
        result["budget_method"] = "50-30-20"
        result["confirmed"] = True
    elif re.search(r'\b(custom|adjust|change|different|own|modify)\b', lower):
        result["budget_method"] = "custom"
        result["confirmed"] = False
    elif re.search(r'\b(zero.?based?|zero)\b', lower):
        result["budget_method"] = "zero-based"
        result["confirmed"] = True
    elif re.search(r'\b(envelope)\b', lower):
        result["budget_method"] = "envelope"
        result["confirmed"] = True
    else:
        result["budget_method"] = "50-30-20"
        result["confirmed"] = True

    return result


# ── Step completion ───────────────────────────────────────────────────────────

def complete_step(step: str, data: dict) -> dict:
    """
    Mark step as complete and save the data to the profile.
    Calls profile_manager to update the relevant fields.
    Returns updated onboarding state.
    """
    state = get_onboarding_state()

    # Save step data in state
    state.setdefault("step_data", {})[step] = data
    state.setdefault("started", True)

    if step not in state.get("completed_steps", []):
        state.setdefault("completed_steps", []).append(step)

    # Remove from skipped if previously skipped
    state["skipped_steps"] = [s for s in state.get("skipped_steps", []) if s != step]

    # Persist to profile
    _apply_step_to_profile(step, data)

    save_onboarding_state(state)
    return state


def _apply_step_to_profile(step: str, data: dict) -> None:
    """Write parsed step data into the finance profile."""
    if step == "basics":
        updates: dict[str, Any] = {}
        if data.get("name"):
            updates.setdefault("personal", {})["name"] = data["name"]
        if data.get("country"):
            updates.setdefault("personal", {})["country"] = data["country"]
        if data.get("locale"):
            updates.setdefault("meta", {})["locale"] = data["locale"]
            updates.setdefault("tax_profile", {})["locale"] = data["locale"]
        if data.get("currency"):
            updates.setdefault("meta", {})["primary_currency"] = data["currency"]
        if updates:
            update_profile(updates)

    elif step == "employment":
        updates = {}
        if data.get("employment_type"):
            updates.setdefault("employment", {})["type"] = data["employment_type"]
        if data.get("gross_annual"):
            updates.setdefault("employment", {})["annual_gross"] = data["gross_annual"]
            updates.setdefault("employment", {})["currency"] = "EUR"
        if updates:
            update_profile(updates)

    elif step == "housing":
        updates = {}
        type_map = {"rent": "renter", "own": "owner", "mortgage": "mortgage"}
        if data.get("housing_type"):
            updates.setdefault("housing", {})["type"] = type_map.get(data["housing_type"], data["housing_type"])
        if data.get("monthly_cost"):
            updates.setdefault("housing", {})["monthly_rent_or_mortgage"] = data["monthly_cost"]
        if data.get("city"):
            updates.setdefault("personal", {})["city"] = data["city"]
        if updates:
            update_profile(updates)

    elif step == "accounts":
        # Accounts stored in a separate file; for now save as profile note
        if data.get("accounts") or data.get("accounts_raw"):
            update_profile({"meta": {"onboarding_accounts": data.get("accounts") or data.get("accounts_raw")}})

    elif step == "goals":
        if data.get("goals"):
            update_profile({"meta": {"onboarding_goals": data["goals"]}})

    elif step == "tax":
        updates = {}
        locale = data.get("locale", "de")
        if data.get("steuerklasse"):
            updates.setdefault("tax_profile", {})["tax_class"] = data["steuerklasse"]
            updates.setdefault("employment", {})["type"] = updates.get("employment", {}).get("type")
        if "kirchensteuer" in data:
            updates.setdefault("tax_profile", {})["church_tax"] = data["kirchensteuer"]
        if data.get("bundesland"):
            updates.setdefault("personal", {})["region"] = data["bundesland"]
        # Store locale-specific extras
        extra_keys = ["tax_code", "self_assessment", "situation_familiale", "parts_fiscales",
                      "box3_above_threshold", "under_26", "joint_filing"]
        extra = {k: data[k] for k in extra_keys if k in data}
        if extra:
            updates.setdefault("tax_profile", {})["extra"] = extra
        if updates:
            update_profile(updates)

    elif step == "budget":
        method = data.get("budget_method", "50-30-20")
        update_profile({"preferences": {"budgeting_method": method}})


def skip_step(step: str) -> dict:
    """Mark a step as skipped (user said 'skip'). Can be revisited later."""
    state = get_onboarding_state()
    state.setdefault("started", True)
    if step not in state.get("skipped_steps", []):
        state.setdefault("skipped_steps", []).append(step)
    # Remove from completed if it was there
    state["completed_steps"] = [s for s in state.get("completed_steps", []) if s != step]
    save_onboarding_state(state)
    return state


def reset_onboarding() -> None:
    """Clear onboarding state to restart from step 1."""
    path = _get_state_path()
    if path.exists():
        path.unlink()


# ── Messages ──────────────────────────────────────────────────────────────────

def _progress_bar(completed: list[str], skipped: list[str], total: int = 7) -> str:
    """Render a simple text progress bar."""
    done = set(completed) | set(skipped)
    bar = ""
    for step in STEPS:
        if step in set(completed):
            bar += "█"
        elif step in set(skipped):
            bar += "░"
        else:
            bar += "·"
    pct = int(len(done) / total * 100)
    return f"[{bar}] {pct}%"


def get_resume_message() -> str:
    """
    For returning users mid-onboarding.
    Shows progress bar and completed steps.
    """
    state = get_onboarding_state()
    progress = get_step_progress()
    completed = state.get("completed_steps", [])
    skipped = state.get("skipped_steps", [])
    current = progress["current_step"]
    step_num = progress["step_number"]
    total = progress["total_steps"]
    bar = _progress_bar(completed, skipped)

    label = STEP_LABELS.get(current, current.title()) if current != "complete" else "Done"
    header = f"Welcome back! You're on Step {step_num} of {total} — {label}."
    progress_line = f"Progress: {bar}"

    step_status = []
    for step in STEPS:
        if step in set(completed):
            step_status.append(f"  ✓ {STEP_LABELS[step]}")
        elif step in set(skipped):
            step_status.append(f"  ~ {STEP_LABELS[step]} (skipped)")
        elif step == current:
            step_status.append(f"  → {STEP_LABELS[step]} ← you are here")
        else:
            step_status.append(f"  ○ {STEP_LABELS[step]}")

    lines = [header, progress_line, ""] + step_status

    if current != "complete":
        lines += ["", get_step_prompt(current)]

    return "\n".join(lines)


def get_completion_message(profile: dict) -> str:
    """Final message when all 7 steps done. Summarizes the full setup."""
    personal = profile.get("personal", {})
    emp = profile.get("employment", {})
    housing = profile.get("housing", {})
    meta = profile.get("meta", {})
    tax = profile.get("tax_profile", {})
    prefs = profile.get("preferences", {})

    currency = meta.get("primary_currency", "EUR")

    # Personal line
    name = personal.get("name", "")
    country = personal.get("country", meta.get("locale", "").upper())
    personal_line = f"  • Profile: {name} | {country} | {currency}" if name else f"  • Profile: {country} | {currency}"

    # Employment line
    emp_type = emp.get("type", "")
    gross = emp.get("annual_gross")
    gross_str = f", {currency} {gross/1000:.0f}k gross" if gross else ""
    emp_line = f"  • Employment: {emp_type.title()}{gross_str}" if emp_type else ""

    # Housing line
    h_type = housing.get("type", "")
    monthly = housing.get("monthly_rent_or_mortgage")
    city = personal.get("city", "")
    h_parts = []
    if h_type:
        h_parts.append(h_type.title())
    if city:
        h_parts.append(city)
    if monthly:
        h_parts.append(f"{currency} {monthly:,.0f}/month")
    housing_line = f"  • Housing: {' '.join(h_parts)}" if h_parts else ""

    # Accounts
    state = get_onboarding_state()
    accounts_raw = meta.get("onboarding_accounts")
    accounts_line = ""
    if accounts_raw:
        if isinstance(accounts_raw, list):
            acc_strs = [f"{a.get('bank', '?')} ({a.get('type', '?')})" for a in accounts_raw]
            accounts_line = f"  • Accounts: {', '.join(acc_strs)}"
        else:
            accounts_line = f"  • Accounts: {accounts_raw}"

    # Goals
    goals_raw = meta.get("onboarding_goals")
    goals_line = ""
    if goals_raw and isinstance(goals_raw, list) and goals_raw:
        g = goals_raw[0]
        name_g = g.get("name", "Goal")
        amount = g.get("target_amount")
        timeline = g.get("timeline", "")
        amount_str = f" {currency} {amount:,}" if amount else ""
        goals_line = f"  • Goal: {name_g}{amount_str}" + (f" {timeline}" if timeline else "")

    # Tax
    tax_class = tax.get("tax_class")
    church = tax.get("church_tax")
    region = personal.get("region", "")
    tax_parts = []
    if tax_class:
        tax_parts.append(f"Steuerklasse {tax_class}")
    if region:
        tax_parts.append(region)
    if church is not None:
        tax_parts.append("Kirchensteuer" if church else "no Kirchensteuer")
    tax_line = f"  • Tax: {', '.join(tax_parts)}" if tax_parts else ""

    # Budget
    budget_method = prefs.get("budgeting_method", "50-30-20")
    budget_line = ""
    if gross and budget_method == "50-30-20":
        monthly_income = gross / 12
        needs = monthly_income * 0.50
        wants = monthly_income * 0.30
        savings = monthly_income * 0.20
        budget_line = (
            f"  • Budget: 50/30/20 → "
            f"Needs {currency} {needs:,.0f} | "
            f"Wants {currency} {wants:,.0f} | "
            f"Savings {currency} {savings:,.0f}"
        )
    elif budget_method:
        budget_line = f"  • Budget: {budget_method}"

    detail_lines = [l for l in [personal_line, emp_line, housing_line, accounts_line, goals_line, tax_line, budget_line] if l]
    details = "\n".join(detail_lines)

    return (
        "You're all set!\n\n"
        "Here's what I've set up:\n"
        f"{details}\n\n"
        "What would you like to do first? Try:\n"
        "  'show my financial health'  or  'what can I deduct this year?'"
    )
