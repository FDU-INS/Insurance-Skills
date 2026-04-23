"""
PolicyPulse - Statistics and Aggregation

Statistical calculations and metric aggregation for simulation results.
Reference: TECH_STACK.md Section 6 (Data Processing: Pandas + NumPy)

Dependencies: pandas, numpy, data_models
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from src.data_models import (
    Citizen,
    CitizenState,
    CityZone,
    IncomeLevel,
    StepMetrics,
)


# =============================================================================
# Aggregation Functions
# =============================================================================

def calculate_step_metrics(
    citizens: list[Citizen],
    states: list[CitizenState],
    step: int,
) -> StepMetrics:
    """
    Calculate aggregated metrics for a simulation step.
    
    Reference: DESIGN_DOC.md Section 3.3 (Metrics Cards)
    
    Args:
        citizens: All citizens in the population
        states: All citizen states for this step
        step: The step number
        
    Returns:
        Aggregated metrics for the step
    """
    if not citizens or not states:
        return StepMetrics(
            step=step,
            avg_happiness=0.0,
            avg_support=0.0,
            avg_income=0.0,
        )
    
    # Create lookup for states by citizen ID
    state_by_id = {s.citizen_id: s for s in states}
    
    # Calculate overall averages
    happiness_values = [s.happiness for s in states]
    support_values = [s.policy_support for s in states]
    income_values = [s.income for s in states]
    
    avg_happiness = float(np.mean(happiness_values))
    avg_support = float(np.mean(support_values))
    avg_income = float(np.mean(income_values))
    
    # Calculate happiness by income level
    happiness_by_income: dict[IncomeLevel, float] = {}
    support_by_income: dict[IncomeLevel, float] = {}
    
    for level in IncomeLevel:
        level_citizens = [c for c in citizens if c.income_level == level]
        if level_citizens:
            level_states = [state_by_id[c.id] for c in level_citizens if c.id in state_by_id]
            if level_states:
                happiness_by_income[level] = float(np.mean([s.happiness for s in level_states]))
                support_by_income[level] = float(np.mean([s.policy_support for s in level_states]))
    
    # Calculate happiness gap
    high_happiness = happiness_by_income.get(IncomeLevel.HIGH, 0.0)
    low_happiness = happiness_by_income.get(IncomeLevel.LOW, 0.0)
    happiness_gap = high_happiness - low_happiness
    
    return StepMetrics(
        step=step,
        avg_happiness=avg_happiness,
        avg_support=avg_support,
        avg_income=avg_income,
        happiness_by_income=happiness_by_income,
        support_by_income=support_by_income,
        happiness_gap=happiness_gap,
    )


def calculate_metric_deltas(
    current: StepMetrics,
    previous: StepMetrics,
) -> dict[str, float]:
    """
    Calculate the change in metrics between two steps.
    
    Args:
        current: Metrics for the current step
        previous: Metrics for the previous step
        
    Returns:
        Dictionary of metric deltas
    """
    return {
        "happiness_delta": current.avg_happiness - previous.avg_happiness,
        "support_delta": current.avg_support - previous.avg_support,
        "income_delta": current.avg_income - previous.avg_income,
        "gap_delta": current.happiness_gap - previous.happiness_gap,
    }


def create_citizens_dataframe(
    citizens: list[Citizen],
    states: list[CitizenState],
) -> pd.DataFrame:
    """
    Create a Pandas DataFrame combining citizens and their states.
    
    Useful for filtering, grouping, and export operations.
    
    Args:
        citizens: List of citizens
        states: List of citizen states (should be same step)
        
    Returns:
        DataFrame with citizen attributes and state values
    """
    if not citizens:
        return pd.DataFrame()
    
    # Create state lookup
    state_by_id = {s.citizen_id: s for s in states}
    
    rows = []
    for citizen in citizens:
        state = state_by_id.get(citizen.id)
        row = {
            "id": citizen.id,
            "age": citizen.age,
            "gender": citizen.gender,
            "income_level": citizen.income_level.value,
            "city_zone": citizen.city_zone.value,
            "education_years": citizen.education_years,
            "profession": citizen.profession,
            "family_size": citizen.family_size,
            "political_view": citizen.political_view.value,
            "risk_tolerance": citizen.risk_tolerance,
            "openness_to_change": citizen.openness_to_change,
        }
        if state:
            row.update({
                "step": state.step,
                "happiness": state.happiness,
                "policy_support": state.policy_support,
                "income": state.income,
                "reaction_method": state.reaction_method.value,
            })
        rows.append(row)
    
    return pd.DataFrame(rows)


def group_by_income_level(
    df: pd.DataFrame,
    metric: str,
) -> dict[str, float]:
    """
    Group a metric by income level and calculate means.
    
    Args:
        df: Citizens DataFrame
        metric: Column name to aggregate
        
    Returns:
        Dictionary mapping income level to mean value
    """
    if df.empty or metric not in df.columns:
        return {}
    
    grouped = df.groupby("income_level")[metric].mean()
    return grouped.to_dict()


def group_by_city_zone(
    df: pd.DataFrame,
    metric: str,
) -> dict[str, float]:
    """
    Group a metric by city zone and calculate means.
    
    Args:
        df: Citizens DataFrame
        metric: Column name to aggregate
        
    Returns:
        Dictionary mapping city zone to mean value
    """
    if df.empty or metric not in df.columns:
        return {}
    
    grouped = df.groupby("city_zone")[metric].mean()
    return grouped.to_dict()


def calculate_inequality_metrics(
    df: pd.DataFrame,
) -> dict[str, float]:
    """
    Calculate inequality metrics across the population.
    
    Includes:
    - Happiness gap (high income - low income)
    - Support gap
    - Income Gini coefficient
    
    Args:
        df: Citizens DataFrame
        
    Returns:
        Dictionary of inequality metrics
    """
    if df.empty:
        return {"happiness_gap": 0.0, "support_gap": 0.0, "income_gini": 0.0}
    
    # Get metrics by income level
    happiness_by_income = group_by_income_level(df, "happiness")
    support_by_income = group_by_income_level(df, "policy_support")
    
    # Calculate gaps
    high_happiness = happiness_by_income.get("High", 0.0)
    low_happiness = happiness_by_income.get("Low", 0.0)
    happiness_gap = high_happiness - low_happiness
    
    high_support = support_by_income.get("High", 0.0)
    low_support = support_by_income.get("Low", 0.0)
    support_gap = high_support - low_support
    
    # Simple Gini coefficient calculation
    incomes = df["income"].values if "income" in df.columns else np.array([])
    if len(incomes) > 0:
        sorted_incomes = np.sort(incomes)
        n = len(sorted_incomes)
        cumulative = np.cumsum(sorted_incomes)
        gini = (2 * np.sum((np.arange(1, n + 1) * sorted_incomes))) / (n * np.sum(sorted_incomes)) - (n + 1) / n
        gini = max(0.0, min(1.0, gini))
    else:
        gini = 0.0
    
    return {
        "happiness_gap": happiness_gap,
        "support_gap": support_gap,
        "income_gini": float(gini),
    }


def export_simulation_results(
    citizens: list[Citizen],
    states_by_step: dict[int, list[CitizenState]],
    path: str,
) -> None:
    """
    Export simulation results to CSV.
    
    Reference: PRD.md Feature F9 (Data Export)
    
    Args:
        citizens: All citizens
        states_by_step: States organized by step number
        path: Output file path
    """
    all_rows = []
    
    for step, states in sorted(states_by_step.items()):
        df = create_citizens_dataframe(citizens, states)
        all_rows.append(df)
    
    if all_rows:
        combined = pd.concat(all_rows, ignore_index=True)
        combined.to_csv(path, index=False)
