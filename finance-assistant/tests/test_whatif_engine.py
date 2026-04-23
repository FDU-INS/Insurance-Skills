"""Tests for scripts/whatif_engine.py — proactive what-if scenario variants."""

from __future__ import annotations

import importlib

import pytest


@pytest.fixture()
def wie():
    import scripts.whatif_engine as m
    importlib.reload(m)
    return m


# ── Shared sample data ────────────────────────────────────────────────────────

FIRE_INPUTS = {
    "current_savings": 50_000,
    "monthly_contribution": 800,
    "annual_expenses": 30_000,
    "annual_return_pct": 0.07,
    "withdrawal_rate": 0.04,
}

FIRE_RESULT = {
    "fire_number": 750_000,
    "years_to_fire": 18.5,
    "achievable": True,
}

DEBT_INPUTS = {
    "strategy": "avalanche",
    "extra_monthly_payment": 0,
}

DEBT_RESULT = {"months_to_payoff": 48, "total_interest": 3_200}

RVB_INPUTS = {
    "monthly_rent": 1_200,
    "home_price": 350_000,
    "down_payment": 70_000,
    "mortgage_rate": 3.5,
    "years": 7,
}

RVB_RESULT = {"recommendation": "buy", "difference": 12_000}

SAVINGS_INPUTS = {
    "target_amount": 20_000,
    "monthly_contribution": 400,
}

SAVINGS_RESULT = {"months_to_goal": 50}


# ── generate_variants ─────────────────────────────────────────────────────────

class TestGenerateVariants:
    def test_fire_generates_three(self, wie):
        variants = wie.generate_variants("fire_calc", FIRE_INPUTS, FIRE_RESULT)
        assert len(variants) == 3

    def test_debt_generates_three(self, wie):
        variants = wie.generate_variants("debt_optimizer", DEBT_INPUTS, DEBT_RESULT)
        assert len(variants) == 3

    def test_rent_vs_buy_generates_three(self, wie):
        variants = wie.generate_variants("scenario_rent_vs_buy", RVB_INPUTS, RVB_RESULT)
        assert len(variants) == 3

    def test_savings_goal_generates_three(self, wie):
        variants = wie.generate_variants("savings_goal", SAVINGS_INPUTS, SAVINGS_RESULT)
        assert len(variants) == 3

    def test_unknown_type_returns_empty(self, wie):
        assert wie.generate_variants("unknown_type", {}, {}) == []

    def test_each_variant_has_label_inputs_delta(self, wie):
        variants = wie.generate_variants("fire_calc", FIRE_INPUTS, FIRE_RESULT)
        for v in variants:
            assert "label" in v
            assert "inputs" in v
            assert "delta_description" in v

    def test_fire_variant_a_increases_contribution(self, wie):
        variants = wie.generate_variants("fire_calc", FIRE_INPUTS, FIRE_RESULT)
        variant_a = variants[0]
        assert variant_a["inputs"]["monthly_contribution"] > FIRE_INPUTS["monthly_contribution"]

    def test_fire_variant_b_lowers_return(self, wie):
        variants = wie.generate_variants("fire_calc", FIRE_INPUTS, FIRE_RESULT)
        variant_b = variants[1]
        assert variant_b["inputs"]["annual_return_pct"] < FIRE_INPUTS["annual_return_pct"]

    def test_fire_variant_c_lowers_expenses(self, wie):
        variants = wie.generate_variants("fire_calc", FIRE_INPUTS, FIRE_RESULT)
        variant_c = variants[2]
        assert variant_c["inputs"]["annual_expenses"] < FIRE_INPUTS["annual_expenses"]

    def test_debt_variant_b_strategy_changes(self, wie):
        variants = wie.generate_variants("debt_optimizer", DEBT_INPUTS, DEBT_RESULT)
        variant_c = variants[2]
        assert variant_c["inputs"]["strategy"] != DEBT_INPUTS["strategy"]

    def test_rvb_variant_a_lower_home_price(self, wie):
        variants = wie.generate_variants("scenario_rent_vs_buy", RVB_INPUTS, RVB_RESULT)
        assert variants[0]["inputs"]["home_price"] < RVB_INPUTS["home_price"]

    def test_rvb_variant_b_higher_rate(self, wie):
        variants = wie.generate_variants("scenario_rent_vs_buy", RVB_INPUTS, RVB_RESULT)
        assert variants[1]["inputs"]["mortgage_rate"] > RVB_INPUTS["mortgage_rate"]

    def test_rvb_variant_c_longer_years(self, wie):
        variants = wie.generate_variants("scenario_rent_vs_buy", RVB_INPUTS, RVB_RESULT)
        assert variants[2]["inputs"]["years"] > RVB_INPUTS["years"]


# ── format_variants ───────────────────────────────────────────────────────────

class TestFormatVariants:
    def test_contains_a_b_c(self, wie):
        variants = wie.generate_variants("fire_calc", FIRE_INPUTS, FIRE_RESULT)
        output = wie.format_variants(variants, FIRE_RESULT)
        assert "A)" in output
        assert "B)" in output
        assert "C)" in output

    def test_starts_with_what_if(self, wie):
        variants = wie.generate_variants("fire_calc", FIRE_INPUTS, FIRE_RESULT)
        output = wie.format_variants(variants, FIRE_RESULT)
        assert "What if" in output

    def test_includes_try_option_prompt(self, wie):
        variants = wie.generate_variants("fire_calc", FIRE_INPUTS, FIRE_RESULT)
        output = wie.format_variants(variants, FIRE_RESULT)
        assert "try option" in output.lower()

    def test_empty_variants_returns_empty_string(self, wie):
        assert wie.format_variants([], {}) == ""

    def test_contains_labels(self, wie):
        variants = wie.generate_variants("fire_calc", FIRE_INPUTS, FIRE_RESULT)
        output = wie.format_variants(variants, FIRE_RESULT)
        for v in variants:
            # Each label should appear somewhere (possibly truncated)
            first_word = v["label"].split()[0]
            assert first_word in output


# ── apply_variant ─────────────────────────────────────────────────────────────

class TestApplyVariant:
    def test_apply_fire_variant_returns_dict(self, wie):
        variants = wie.generate_variants("fire_calc", FIRE_INPUTS, FIRE_RESULT)
        result = wie.apply_variant("fire_calc", FIRE_INPUTS, 0, variants)
        assert isinstance(result, dict)

    def test_apply_fire_variant_a_changes_contribution(self, wie):
        variants = wie.generate_variants("fire_calc", FIRE_INPUTS, FIRE_RESULT)
        result = wie.apply_variant("fire_calc", FIRE_INPUTS, 0, variants)
        # Either a computed FIRE result or the inputs-to-use dict
        if "inputs_to_use" in result:
            assert result["inputs_to_use"]["monthly_contribution"] > FIRE_INPUTS["monthly_contribution"]
        else:
            # actual FIRE result — years_to_fire should be less
            assert "fire_number" in result or "years_to_fire" in result

    def test_apply_out_of_range_returns_error(self, wie):
        variants = wie.generate_variants("fire_calc", FIRE_INPUTS, FIRE_RESULT)
        result = wie.apply_variant("fire_calc", FIRE_INPUTS, 99, variants)
        assert "error" in result

    def test_apply_rvb_variant(self, wie):
        variants = wie.generate_variants("scenario_rent_vs_buy", RVB_INPUTS, RVB_RESULT)
        result = wie.apply_variant("scenario_rent_vs_buy", RVB_INPUTS, 0, variants)
        assert isinstance(result, dict)

    def test_apply_unknown_type_returns_inputs_to_use(self, wie):
        fake_variants = [
            {"label": "test", "inputs": {"x": 1}, "delta_description": "", "index": 0}
        ]
        result = wie.apply_variant("savings_goal", {"x": 0}, 0, fake_variants)
        assert isinstance(result, dict)
        # Should not crash; either returns inputs_to_use or a note
        assert "inputs_to_use" in result or "note" in result or "error" in result
