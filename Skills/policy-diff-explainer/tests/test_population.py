"""
Tests for population generation module.
"""

from __future__ import annotations

import pytest

from src.data_models import (
    Citizen,
    CitizenState,
    IncomeLevel,
    PopulationConfig,
)
from src.population import (
    generate_population,
    generate_initial_states,
    get_population_summary,
)
from src.utils import create_rng


class TestPopulationGeneration:
    """Tests for population generation."""

    def test_population_size(self) -> None:
        """Generated population should match requested size."""
        config = PopulationConfig(size=100)
        rng = create_rng(42)
        population = generate_population(config, rng)
        
        assert len(population) == 100

    def test_income_distribution(self) -> None:
        """Income distribution should match configuration percentages."""
        config = PopulationConfig(
            size=100,
            low_income_pct=0.30,
            middle_income_pct=0.50,
            high_income_pct=0.20,
        )
        rng = create_rng(42)
        population = generate_population(config, rng)
        
        # Count by income level
        counts = {level: 0 for level in IncomeLevel}
        for citizen in population:
            counts[citizen.income_level] += 1
        
        assert counts[IncomeLevel.LOW] == 30
        assert counts[IncomeLevel.MIDDLE] == 50
        assert counts[IncomeLevel.HIGH] == 20

    def test_reproducibility_with_seed(self) -> None:
        """Same seed should produce identical population."""
        config = PopulationConfig(size=50, random_seed=123)
        
        rng1 = create_rng(123)
        population1 = generate_population(config, rng1)
        
        rng2 = create_rng(123)
        population2 = generate_population(config, rng2)
        
        for c1, c2 in zip(population1, population2):
            assert c1.id == c2.id
            assert c1.age == c2.age
            assert c1.income_level == c2.income_level
            assert c1.city_zone == c2.city_zone

    def test_all_citizens_are_valid(self) -> None:
        """All generated citizens should have valid attribute ranges."""
        config = PopulationConfig(size=200)
        rng = create_rng(42)
        population = generate_population(config, rng)
        
        for citizen in population:
            assert 18 <= citizen.age <= 75
            assert citizen.income_level in IncomeLevel
            assert 8 <= citizen.education_years <= 22
            assert 1 <= citizen.family_size <= 6
            assert 0.0 <= citizen.risk_tolerance <= 1.0
            assert 0.0 <= citizen.openness_to_change <= 1.0

    def test_empty_population_rejected(self) -> None:
        """Population size of 0 should raise ValueError."""
        config = PopulationConfig(size=0)
        rng = create_rng(42)
        
        with pytest.raises(ValueError):
            generate_population(config, rng)


class TestInitialStates:
    """Tests for initial state generation."""

    def test_states_match_population(self) -> None:
        """Number of states should match population size."""
        config = PopulationConfig(size=50)
        rng = create_rng(42)
        population = generate_population(config, rng)
        states = generate_initial_states(population, rng)
        
        assert len(states) == len(population)

    def test_states_have_valid_ranges(self) -> None:
        """All initial states should have valid value ranges."""
        config = PopulationConfig(size=100)
        rng = create_rng(42)
        population = generate_population(config, rng)
        states = generate_initial_states(population, rng)
        
        for state in states:
            assert 0.0 <= state.happiness <= 1.0
            assert -1.0 <= state.policy_support <= 1.0
            assert state.income >= 0
            assert state.step == 0

    def test_states_have_citizen_ids(self) -> None:
        """Each state should reference a valid citizen ID."""
        config = PopulationConfig(size=50)
        rng = create_rng(42)
        population = generate_population(config, rng)
        states = generate_initial_states(population, rng)
        
        citizen_ids = {c.id for c in population}
        for state in states:
            assert state.citizen_id in citizen_ids


class TestPopulationSummary:
    """Tests for population summary generation."""

    def test_summary_total_matches(self) -> None:
        """Summary total should match population size."""
        config = PopulationConfig(size=100)
        rng = create_rng(42)
        population = generate_population(config, rng)
        summary = get_population_summary(population)
        
        assert summary["total"] == 100

    def test_summary_has_required_fields(self) -> None:
        """Summary should contain all required fields."""
        config = PopulationConfig(size=50)
        rng = create_rng(42)
        population = generate_population(config, rng)
        summary = get_population_summary(population)
        
        assert "total" in summary
        assert "income_distribution" in summary
        assert "zone_distribution" in summary
        assert "political_distribution" in summary
        assert "avg_age" in summary
        assert "avg_education_years" in summary
        assert "avg_family_size" in summary

    def test_empty_population_summary(self) -> None:
        """Empty population should return minimal summary."""
        summary = get_population_summary([])
        assert summary["total"] == 0
