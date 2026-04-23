"""
Finance Assistant What-If Engine — Proactive scenario variants.

After any major scenario, automatically generates 3 alternative what-if
calculations to prompt the user to explore adjacent options.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Optional

try:
    from scenario_engine import (
        project_fire_timeline,
        compare_rent_vs_buy,
    )
    from debt_optimizer import optimize_debt_payoff
    from goal_tracker import project_goal
except ImportError:
    import os, sys
    sys.path.insert(0, os.path.dirname(__file__))
    try:
        from scenario_engine import project_fire_timeline, compare_rent_vs_buy
    except ImportError:
        project_fire_timeline = None
        compare_rent_vs_buy = None
    try:
        from debt_optimizer import optimize_debt_payoff
    except ImportError:
        optimize_debt_payoff = None
    try:
        from goal_tracker import project_goal
    except ImportError:
        project_goal = None


# ── Variant generators ────────────────────────────────────────────────────────

def _variants_fire_calc(base_inputs: dict, base_result: dict) -> list[dict]:
    """Three what-if variants for a FIRE calculation."""
    variants = []

    # A) +€200/month contribution
    extra = 200.0
    variants.append({
        "label": f"Add €{extra:.0f}/month to contributions",
        "inputs": {**base_inputs, "monthly_contribution": base_inputs.get("monthly_contribution", 0) + extra},
        "delta_description": f"retire earlier by contributing €{extra:.0f}/month more",
        "index": 0,
    })

    # B) -1% return assumption
    lower_return = max(0.0, base_inputs.get("annual_return_pct", 0.07) - 0.01)
    variants.append({
        "label": "Returns average 1% lower",
        "inputs": {**base_inputs, "annual_return_pct": lower_return},
        "delta_description": "retire later with lower return assumption",
        "index": 1,
    })

    # C) 10% lower target (lean FIRE)
    current_expenses = base_inputs.get("annual_expenses", 0)
    lean_expenses = current_expenses * 0.9
    variants.append({
        "label": f"Lean FIRE: target €{lean_expenses:,.0f}/year (10% less)",
        "inputs": {**base_inputs, "annual_expenses": lean_expenses},
        "delta_description": "retire earlier by reducing target spend by 10%",
        "index": 2,
    })

    return variants


def _variants_debt_optimizer(base_inputs: dict, base_result: dict) -> list[dict]:
    """Three what-if variants for a debt optimization."""
    variants = []

    extra = 100.0
    variants.append({
        "label": f"Add €{extra:.0f}/month extra payment",
        "inputs": {**base_inputs, "extra_monthly_payment": base_inputs.get("extra_monthly_payment", 0) + extra},
        "delta_description": f"pay off sooner and save interest with €{extra:.0f}/month extra",
        "index": 0,
    })

    variants.append({
        "label": "Refinance highest-rate debt to 3%",
        "inputs": {**base_inputs, "_refinance_top_to_rate": 3.0},
        "delta_description": "refinance highest-rate debt to 3% and compare interest saved",
        "index": 1,
    })

    current_strategy = base_inputs.get("strategy", "avalanche")
    alt_strategy = "snowball" if current_strategy == "avalanche" else "avalanche"
    variants.append({
        "label": f"Switch to {alt_strategy} strategy",
        "inputs": {**base_inputs, "strategy": alt_strategy},
        "delta_description": f"compare {alt_strategy} vs current {current_strategy} in months and total interest",
        "index": 2,
    })

    return variants


def _variants_rent_vs_buy(base_inputs: dict, base_result: dict) -> list[dict]:
    """Three what-if variants for a rent-vs-buy scenario."""
    variants = []

    home_price = base_inputs.get("home_price", 0)
    variants.append({
        "label": f"House price 10% lower (€{home_price * 0.9:,.0f})",
        "inputs": {**base_inputs, "home_price": home_price * 0.9},
        "delta_description": "how a 10% lower purchase price shifts the buy/rent breakeven",
        "index": 0,
    })

    current_rate = base_inputs.get("mortgage_rate", 3.5)
    variants.append({
        "label": f"Interest rate +0.5% ({current_rate + 0.5:.1f}%)",
        "inputs": {**base_inputs, "mortgage_rate": current_rate + 0.5},
        "delta_description": "how a 0.5% higher mortgage rate shifts the breakeven",
        "index": 1,
    })

    longer_years = max(base_inputs.get("years", 7) + 3, 10)
    variants.append({
        "label": f"Stay {longer_years} years instead of {base_inputs.get('years', 7)}",
        "inputs": {**base_inputs, "years": longer_years},
        "delta_description": f"compare total cost if you stay {longer_years} years",
        "index": 2,
    })

    return variants


def _variants_savings_goal(base_inputs: dict, base_result: dict) -> list[dict]:
    """Three what-if variants for a savings goal."""
    variants = []

    extra = 50.0
    variants.append({
        "label": f"Add €{extra:.0f}/month",
        "inputs": {**base_inputs, "monthly_contribution": base_inputs.get("monthly_contribution", 0) + extra},
        "delta_description": f"reach goal X months sooner with €{extra:.0f}/month more",
        "index": 0,
    })

    target = base_inputs.get("target_amount", 0)
    lower_target = target * 0.9
    variants.append({
        "label": f"Lower target by 10% (€{lower_target:,.0f})",
        "inputs": {**base_inputs, "target_amount": lower_target},
        "delta_description": "reach goal sooner with a 10% lower target",
        "index": 1,
    })

    variants.append({
        "label": "Start immediately vs wait 3 months",
        "inputs": {**base_inputs, "_start_delay_months": 0},
        "delta_description": "impact of starting now vs delaying 3 months",
        "index": 2,
    })

    return variants


# ── Public API ────────────────────────────────────────────────────────────────

_VARIANT_GENERATORS = {
    "fire_calc": _variants_fire_calc,
    "debt_optimizer": _variants_debt_optimizer,
    "scenario_rent_vs_buy": _variants_rent_vs_buy,
    "savings_goal": _variants_savings_goal,
}


def generate_variants(
    scenario_type: str,
    base_inputs: dict,
    base_result: dict,
) -> list[dict]:
    """
    Generate 3 automatic what-if variants after a scenario.

    Returns list of {"label": str, "inputs": dict, "delta_description": str, "index": int}.
    Returns empty list for unknown scenario types.
    """
    generator = _VARIANT_GENERATORS.get(scenario_type)
    if generator is None:
        return []
    return generator(base_inputs, base_result)


def format_variants(
    variants: list,
    base_result: dict,
    currency: str = "EUR",
) -> str:
    """
    Format 3 what-if options as a clean follow-up block.

    Output:
      💡 What if...
        A) You add €200/month → retire 2 years earlier (2041 vs 2043)
        B) Returns average 6% instead of 7% → retire 3 years later (2046)
        C) You target lean FIRE (€27k/year) → retire in 2038
      Say "try option A/B/C" or ask your own variation.
    """
    if not variants:
        return ""

    letters = ["A", "B", "C", "D", "E"]
    lines = ["💡 What if..."]
    for i, variant in enumerate(variants[:5]):
        letter = letters[i]
        label = variant.get("label", f"Variant {i + 1}")
        delta = variant.get("delta_description", "")
        if delta:
            lines.append(f"  {letter}) {label} → {delta}")
        else:
            lines.append(f"  {letter}) {label}")

    lines.append('Say "try option A/B/C" or ask your own variation.')
    return "\n".join(lines)


def apply_variant(
    scenario_type: str,
    base_inputs: dict,
    variant_index: int,
    variants: list,
) -> dict:
    """
    Run the actual calculation for a chosen variant. Returns new result dict.

    Merges variant inputs on top of base_inputs and re-runs the appropriate
    scenario function. Falls back to returning the variant inputs if the
    engine function is not available.
    """
    if variant_index < 0 or variant_index >= len(variants):
        return {"error": f"Variant index {variant_index} out of range"}

    variant = variants[variant_index]
    merged_inputs = {**base_inputs, **variant.get("inputs", {})}

    # Strip internal control keys (prefixed with _)
    calc_inputs = {k: v for k, v in merged_inputs.items() if not k.startswith("_")}

    # Dispatch to the right engine
    if scenario_type == "fire_calc" and project_fire_timeline is not None:
        fire_keys = (
            "current_savings", "monthly_contribution", "annual_expenses",
            "annual_return_pct", "withdrawal_rate", "inflation_rate",
        )
        kwargs = {k: calc_inputs[k] for k in fire_keys if k in calc_inputs}
        try:
            return project_fire_timeline(**kwargs)
        except Exception as exc:
            return {"error": str(exc), "inputs_used": kwargs}

    if scenario_type == "scenario_rent_vs_buy" and compare_rent_vs_buy is not None:
        rvb_keys = (
            "monthly_rent", "home_price", "down_payment", "mortgage_rate",
            "years", "property_tax_rate", "maintenance_rate", "rent_increase",
            "home_appreciation", "investment_return",
        )
        kwargs = {k: calc_inputs[k] for k in rvb_keys if k in calc_inputs}
        try:
            return compare_rent_vs_buy(**kwargs)
        except Exception as exc:
            return {"error": str(exc), "inputs_used": kwargs}

    # For other scenario types (debt, savings_goal) or missing engines,
    # return the inputs so the caller / Claude can complete the calculation.
    return {
        "variant_label": variant.get("label"),
        "inputs_to_use": calc_inputs,
        "note": "Re-run your scenario engine with these inputs to compute the result.",
    }
