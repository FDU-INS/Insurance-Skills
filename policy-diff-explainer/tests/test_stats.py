"""
Tests for statistics module.
"""

from __future__ import annotations

import pytest

from src.data_models import (
    CitizenState,
    IncomeLevel,
    PopulationConfig,
    ReactionMethod,
)
from src.population import generate_population, generate_initial_states
from src.stats import (
    calculate_step_metrics,
    calculate_metric_deltas,
    create_citizens_dataframe,
    group_by_income_level,
    calculate_inequality_metrics,
)
from src.utils import create_rng


class TestStepMetrics:
    """Tests for step metrics calculation."""

    def test_average_happiness(self) -> None:
        """Average happiness should be correctly calculated."""
        config = PopulationConfig(size=100)
        rng = create_rng(42)
        population = generate_population(config, rng)
        states = generate_initial_states(population, rng)
        
        metrics = calculate_step_metrics(population, states, step=0)
        
        # Manual calculation
        expected_avg = sum(s.happiness for s in states) / len(states)
        
        assert abs(metrics.avg_happiness - expected_avg) < 0.001

    def test_happiness_by_income(self) -> None:
        """Happiness should be grouped by income level."""
        config = PopulationConfig(size=100)
        rng = create_rng(42)
        population = generate_population(config, rng)
        states = generate_initial_states(population, rng)
        
        metrics = calculate_step_metrics(population, states, step=0)
        
        # Should have all three income levels
        assert IncomeLevel.LOW in metrics.happiness_by_income
        assert IncomeLevel.MIDDLE in metrics.happiness_by_income
        assert IncomeLevel.HIGH in metrics.happiness_by_income

    def test_empty_population(self) -> None:
        """Empty population should return zero metrics."""
        metrics = calculate_step_metrics([], [], step=0)
        
        assert metrics.avg_happiness == 0.0
        assert metrics.avg_support == 0.0
        assert metrics.avg_income == 0.0


class TestMetricDeltas:
    """Tests for metric delta calculation."""

    def test_delta_calculation(self) -> None:
        """Deltas should be correctly calculated between steps."""
        config = PopulationConfig(size=50)
        rng = create_rng(42)
        population = generate_population(config, rng)
        states = generate_initial_states(population, rng)
        
        metrics1 = calculate_step_metrics(population, states, step=0)
        
        # Modify states for step 1
        states2 = [
            CitizenState(
                citizen_id=s.citizen_id,
                step=1,
                happiness=s.happiness + 0.1,
                policy_support=s.policy_support + 0.05,
                income=s.income * 1.02,
                reaction_method=ReactionMethod.RULE_BASED,
            )
            for s in states
        ]
        metrics2 = calculate_step_metrics(population, states2, step=1)
        
        deltas = calculate_metric_deltas(metrics2, metrics1)
        
        assert "happiness_delta" in deltas
        assert "support_delta" in deltas
        assert "income_delta" in deltas


class TestCitizensDataframe:
    """Tests for DataFrame creation."""

    def test_dataframe_creation(self) -> None:
        """Should create a valid DataFrame."""
        config = PopulationConfig(size=50)
        rng = create_rng(42)
        population = generate_population(config, rng)
        states = generate_initial_states(population, rng)
        
        df = create_citizens_dataframe(population, states)
        
        assert len(df) == 50
        assert "id" in df.columns
        assert "age" in df.columns
        assert "income_level" in df.columns
        assert "happiness" in df.columns

    def test_empty_dataframe(self) -> None:
        """Empty population should create empty DataFrame."""
        df = create_citizens_dataframe([], [])
        assert len(df) == 0


class TestInequality:
    """Tests for inequality metrics."""

    def test_happiness_gap(self) -> None:
        """Happiness gap should be high minus low income happiness."""
        config = PopulationConfig(size=100)
        rng = create_rng(42)
        population = generate_population(config, rng)
        states = generate_initial_states(population, rng)
        
        metrics = calculate_step_metrics(population, states, step=0)
        
        # Happiness gap should be positive (high income happier)
        assert metrics.happiness_gap > 0

    def test_inequality_metrics(self) -> None:
        """Should calculate all inequality metrics."""
        config = PopulationConfig(size=100)
        rng = create_rng(42)
        population = generate_population(config, rng)
        states = generate_initial_states(population, rng)
        
        df = create_citizens_dataframe(population, states)
        inequality = calculate_inequality_metrics(df)
        
        assert "happiness_gap" in inequality
        assert "support_gap" in inequality
        assert "income_gini" in inequality
