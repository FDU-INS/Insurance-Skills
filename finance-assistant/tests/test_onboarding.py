"""
Tests for scripts/onboarding.py — guided 7-step onboarding wizard.
"""

import pytest
from onboarding import (
    STEPS,
    get_onboarding_state,
    save_onboarding_state,
    is_onboarding_complete,
    get_current_step,
    get_step_progress,
    get_step_prompt,
    complete_step,
    parse_step_response,
    get_resume_message,
    get_completion_message,
    skip_step,
    reset_onboarding,
)


# ── get_step_progress ─────────────────────────────────────────────────────────

class TestGetStepProgress:
    def test_fresh_state_step_one(self):
        p = get_step_progress()
        assert p["current_step"] == "basics"
        assert p["step_number"] == 1
        assert p["total_steps"] == 7
        assert p["completed_steps"] == []
        assert p["pct_complete"] == 0

    def test_after_first_step_completed(self):
        save_onboarding_state({"completed_steps": ["basics"], "skipped_steps": [], "step_data": {}})
        p = get_step_progress()
        assert p["current_step"] == "employment"
        assert p["step_number"] == 2
        assert p["pct_complete"] == 14  # 1/7

    def test_three_steps_done(self):
        save_onboarding_state({
            "completed_steps": ["basics", "employment", "housing"],
            "skipped_steps": [],
            "step_data": {},
        })
        p = get_step_progress()
        assert p["current_step"] == "accounts"
        assert p["step_number"] == 4
        assert p["pct_complete"] == 42  # 3/7

    def test_all_complete(self):
        save_onboarding_state({
            "completed_steps": STEPS[:],
            "skipped_steps": [],
            "step_data": {},
        })
        p = get_step_progress()
        assert p["current_step"] == "complete"
        assert p["pct_complete"] == 100

    def test_skipped_steps_count_toward_progress(self):
        save_onboarding_state({
            "completed_steps": ["basics"],
            "skipped_steps": ["employment"],
            "step_data": {},
        })
        p = get_step_progress()
        assert p["pct_complete"] == 28  # 2/7
        assert p["current_step"] == "housing"

    def test_remaining_steps_excludes_done(self):
        save_onboarding_state({
            "completed_steps": ["basics", "employment"],
            "skipped_steps": [],
            "step_data": {},
        })
        p = get_step_progress()
        assert "basics" not in p["remaining_steps"]
        assert "employment" not in p["remaining_steps"]
        assert "housing" in p["remaining_steps"]


# ── parse_step_response — basics ──────────────────────────────────────────────

class TestParseBasics:
    def test_im_alex_in_germany(self):
        r = parse_step_response("basics", "I'm Alex, based in Germany")
        assert r["name"] == "Alex"
        assert r["country"] == "DE"
        assert r["locale"] == "de"
        assert r["currency"] == "EUR"

    def test_my_name_is_sara_uk(self):
        r = parse_step_response("basics", "My name is Sara, I live in the UK")
        assert r["name"] == "Sara"
        assert r["country"] == "GB"
        assert r["currency"] == "GBP"

    def test_country_only(self):
        r = parse_step_response("basics", "Germany")
        assert r["country"] == "DE"
        assert r["locale"] == "de"

    def test_france_eur(self):
        r = parse_step_response("basics", "I'm Pierre, living in France")
        assert r["country"] == "FR"
        assert r["currency"] == "EUR"

    def test_poland(self):
        r = parse_step_response("basics", "I'm Marta, Poland")
        assert r["country"] == "PL"
        assert r["currency"] == "PLN"

    def test_empty_needs_clarification(self):
        r = parse_step_response("basics", "Hello there")
        assert r.get("needs_clarification") is True


# ── parse_step_response — employment ─────────────────────────────────────────

class TestParseEmployment:
    def test_employed_65k(self):
        r = parse_step_response("employment", "Employed, €65k/year")
        assert r["employment_type"] == "employed"
        assert r["gross_annual"] == 65000

    def test_freelancer_80k(self):
        r = parse_step_response("employment", "Freelancer, about €80k")
        assert r["employment_type"] == "freelancer"
        assert r["gross_annual"] == 80000

    def test_self_employed(self):
        r = parse_step_response("employment", "Self-employed, €55,000")
        assert r["employment_type"] == "self_employed"
        assert r["gross_annual"] == 55000

    def test_european_number_format(self):
        r = parse_step_response("employment", "employed, 65.000 EUR")
        assert r["employment_type"] == "employed"
        assert r["gross_annual"] == 65000

    def test_retired(self):
        r = parse_step_response("employment", "Retired, pension €20k")
        assert r["employment_type"] == "retired"
        assert r["gross_annual"] == 20000


# ── parse_step_response — housing ────────────────────────────────────────────

class TestParseHousing:
    def test_renting_berlin(self):
        r = parse_step_response("housing", "Renting in Berlin, €1,200/month")
        assert r["housing_type"] == "rent"
        assert r["monthly_cost"] == 1200
        assert r["city"] == "Berlin"

    def test_own_no_mortgage(self):
        r = parse_step_response("housing", "I own my apartment, paid off")
        assert r["housing_type"] == "own"

    def test_mortgage(self):
        r = parse_step_response("housing", "Mortgage, €1,500/month in Munich")
        assert r["housing_type"] == "mortgage"
        assert r["monthly_cost"] == 1500

    def test_rent_no_city(self):
        r = parse_step_response("housing", "Renting, €900/month")
        assert r["housing_type"] == "rent"
        assert r["monthly_cost"] == 900


# ── parse_step_response — tax ────────────────────────────────────────────────

class TestParseTax:
    def test_steuerklasse_1_de(self):
        r = parse_step_response("tax", "Klasse 1, no Kirchensteuer, Berlin", locale="de")
        assert r["steuerklasse"] == 1
        assert r["kirchensteuer"] is False
        assert r["bundesland"] == "Berlin"

    def test_steuerklasse_3(self):
        r = parse_step_response("tax", "Steuerklasse 3, yes Kirchensteuer, Bayern", locale="de")
        assert r["steuerklasse"] == 3
        assert r["kirchensteuer"] is True

    def test_roman_numeral_steuerklasse(self):
        r = parse_step_response("tax", "Klasse IV", locale="de")
        assert r["steuerklasse"] == 4

    def test_uk_tax_code(self):
        r = parse_step_response("tax", "1257L, no self-assessment", locale="gb")
        assert r["tax_code"] == "1257L"
        assert r["self_assessment"] is False

    def test_fr_situation(self):
        r = parse_step_response("tax", "Célibataire, 1 part", locale="fr")
        assert r["situation_familiale"] == "celibataire"
        assert r["parts_fiscales"] == 1.0

    def test_nl_box3(self):
        r = parse_step_response("tax", "No, well under the threshold", locale="nl")
        assert r["box3_above_threshold"] is False

    def test_pl_under_26(self):
        r = parse_step_response("tax", "Tak, mam 24 lata", locale="pl")
        assert r["under_26"] is True


# ── complete_step ─────────────────────────────────────────────────────────────

class TestCompleteStep:
    def test_marks_step_complete(self):
        state = complete_step("basics", {"name": "Alex", "country": "DE", "locale": "de", "currency": "EUR"})
        assert "basics" in state["completed_steps"]

    def test_updates_state_file(self):
        complete_step("basics", {"name": "Alex", "country": "DE", "locale": "de", "currency": "EUR"})
        state = get_onboarding_state()
        assert "basics" in state["completed_steps"]

    def test_saves_step_data(self):
        complete_step("basics", {"name": "Maria", "country": "DE", "locale": "de", "currency": "EUR"})
        state = get_onboarding_state()
        assert state["step_data"]["basics"]["name"] == "Maria"

    def test_removes_from_skipped_when_completed(self):
        skip_step("basics")
        state = get_onboarding_state()
        assert "basics" in state["skipped_steps"]

        complete_step("basics", {"name": "Alex", "country": "DE", "locale": "de", "currency": "EUR"})
        state = get_onboarding_state()
        assert "basics" not in state["skipped_steps"]
        assert "basics" in state["completed_steps"]

    def test_returns_updated_state(self):
        state = complete_step("basics", {"name": "Alex"})
        assert isinstance(state, dict)
        assert "completed_steps" in state

    def test_applies_data_to_profile(self):
        from profile_manager import get_profile
        complete_step("basics", {"name": "Alex", "country": "DE", "locale": "de", "currency": "EUR"})
        profile = get_profile()
        assert profile["personal"]["name"] == "Alex"
        assert profile["meta"]["locale"] == "de"


# ── skip_step ─────────────────────────────────────────────────────────────────

class TestSkipStep:
    def test_marks_step_skipped(self):
        state = skip_step("employment")
        assert "employment" in state["skipped_steps"]

    def test_skipped_not_in_completed(self):
        state = skip_step("housing")
        assert "housing" not in state.get("completed_steps", [])

    def test_skip_advances_current_step(self):
        skip_step("basics")
        assert get_current_step() == "employment"

    def test_skip_multiple_steps(self):
        skip_step("basics")
        skip_step("employment")
        assert get_current_step() == "housing"


# ── is_onboarding_complete ────────────────────────────────────────────────────

class TestIsOnboardingComplete:
    def test_false_when_empty(self):
        assert is_onboarding_complete() is False

    def test_false_when_partial(self):
        save_onboarding_state({"completed_steps": ["basics", "employment"], "skipped_steps": [], "step_data": {}})
        assert is_onboarding_complete() is False

    def test_true_when_all_completed(self):
        save_onboarding_state({"completed_steps": STEPS[:], "skipped_steps": [], "step_data": {}})
        assert is_onboarding_complete() is True

    def test_true_when_all_skipped(self):
        save_onboarding_state({"completed_steps": [], "skipped_steps": STEPS[:], "step_data": {}})
        assert is_onboarding_complete() is True

    def test_true_when_mix_of_completed_and_skipped(self):
        save_onboarding_state({
            "completed_steps": STEPS[:4],
            "skipped_steps": STEPS[4:],
            "step_data": {},
        })
        assert is_onboarding_complete() is True


# ── get_resume_message ────────────────────────────────────────────────────────

class TestGetResumeMessage:
    def test_contains_step_info(self):
        save_onboarding_state({
            "completed_steps": ["basics"],
            "skipped_steps": [],
            "step_data": {},
        })
        msg = get_resume_message()
        assert "Step 2 of 7" in msg
        assert "Employment" in msg

    def test_completed_steps_marked_with_checkmark(self):
        save_onboarding_state({
            "completed_steps": ["basics", "employment"],
            "skipped_steps": [],
            "step_data": {},
        })
        msg = get_resume_message()
        assert "✓" in msg
        assert "Basics" in msg
        assert "Employment" in msg

    def test_contains_progress_bar(self):
        save_onboarding_state({
            "completed_steps": ["basics"],
            "skipped_steps": [],
            "step_data": {},
        })
        msg = get_resume_message()
        # Progress bar uses block chars
        assert "%" in msg
        assert "[" in msg

    def test_welcome_back_in_message(self):
        save_onboarding_state({
            "completed_steps": ["basics"],
            "skipped_steps": [],
            "step_data": {},
        })
        msg = get_resume_message()
        assert "Welcome back" in msg

    def test_skipped_steps_marked(self):
        save_onboarding_state({
            "completed_steps": ["basics"],
            "skipped_steps": ["employment"],
            "step_data": {},
        })
        msg = get_resume_message()
        assert "skipped" in msg.lower() or "~" in msg


# ── get_completion_message ────────────────────────────────────────────────────

class TestGetCompletionMessage:
    def _make_profile(self):
        return {
            "meta": {"primary_currency": "EUR", "locale": "de",
                     "onboarding_accounts": [{"bank": "DKB", "type": "checking"}, {"bank": "ING", "type": "savings"}],
                     "onboarding_goals": [{"name": "Emergency fund", "target_amount": 10000, "timeline": "by end of year"}]},
            "personal": {"name": "Alex", "country": "DE", "city": "Berlin", "region": "Berlin"},
            "employment": {"type": "employed", "annual_gross": 65000, "currency": "EUR"},
            "housing": {"type": "renter", "monthly_rent_or_mortgage": 1200},
            "tax_profile": {"locale": "de", "tax_class": 1, "church_tax": False, "extra": {}},
            "preferences": {"budgeting_method": "50-30-20"},
        }

    def test_contains_name(self):
        msg = get_completion_message(self._make_profile())
        assert "Alex" in msg

    def test_contains_employment(self):
        msg = get_completion_message(self._make_profile())
        assert "65" in msg  # 65k gross

    def test_contains_housing(self):
        msg = get_completion_message(self._make_profile())
        assert "1,200" in msg or "1200" in msg

    def test_contains_budget_splits(self):
        msg = get_completion_message(self._make_profile())
        # 65000/12 * 0.5 = 2708.33
        assert "Needs" in msg
        assert "Wants" in msg
        assert "Savings" in msg

    def test_contains_cta(self):
        msg = get_completion_message(self._make_profile())
        assert "financial health" in msg.lower() or "deduct" in msg.lower()

    def test_you_are_all_set(self):
        msg = get_completion_message(self._make_profile())
        assert "all set" in msg.lower() or "set up" in msg.lower()

    def test_contains_goal(self):
        msg = get_completion_message(self._make_profile())
        assert "Emergency fund" in msg or "10,000" in msg or "10000" in msg


# ── reset_onboarding ──────────────────────────────────────────────────────────

class TestResetOnboarding:
    def test_clears_completed_steps(self):
        save_onboarding_state({
            "completed_steps": ["basics", "employment"],
            "skipped_steps": [],
            "step_data": {"basics": {"name": "Alex"}},
        })
        reset_onboarding()
        state = get_onboarding_state()
        assert state["completed_steps"] == []

    def test_current_step_is_basics_after_reset(self):
        save_onboarding_state({
            "completed_steps": STEPS[:4],
            "skipped_steps": [],
            "step_data": {},
        })
        reset_onboarding()
        assert get_current_step() == "basics"

    def test_is_not_complete_after_reset(self):
        save_onboarding_state({"completed_steps": STEPS[:], "skipped_steps": [], "step_data": {}})
        assert is_onboarding_complete() is True
        reset_onboarding()
        assert is_onboarding_complete() is False

    def test_reset_idempotent_when_no_state_file(self):
        # Should not raise even if file doesn't exist
        reset_onboarding()
        reset_onboarding()  # second call harmless
        assert get_current_step() == "basics"


# ── get_step_prompt ───────────────────────────────────────────────────────────

class TestGetStepPrompt:
    def test_basics_prompt_contains_step_indicator(self):
        p = get_step_prompt("basics")
        assert "Step 1 of 7" in p

    def test_employment_prompt_step_2(self):
        p = get_step_prompt("employment")
        assert "Step 2 of 7" in p
        assert "Employment" in p

    def test_housing_prompt_step_3(self):
        p = get_step_prompt("housing")
        assert "Step 3 of 7" in p

    def test_tax_de_has_steuerklasse(self):
        p = get_step_prompt("tax", locale="de")
        assert "Steuerklasse" in p

    def test_tax_gb_has_tax_code(self):
        p = get_step_prompt("tax", locale="gb")
        assert "tax code" in p.lower()

    def test_tax_fr_has_parts(self):
        p = get_step_prompt("tax", locale="fr")
        assert "parts" in p.lower() or "familiale" in p.lower()

    def test_budget_prompt_step_7(self):
        p = get_step_prompt("budget")
        assert "Step 7 of 7" in p
        assert "50/30/20" in p or "50%" in p
