"""
Tests for data_models module.
"""

from __future__ import annotations

import pytest

from src.data_models import (
    Citizen,
    CitizenState,
    IncomeLevel,
    CityZone,
    PoliticalView,
    PolicyDomain,
    SimulationMode,
    Policy,
    PopulationConfig,
    SimulationConfig,
)


class TestPopulationConfig:
    """Tests for PopulationConfig validation."""

    def test_valid_income_distribution(self) -> None:
        """Income percentages summing to 1.0 should be valid."""
        config = PopulationConfig(
            size=1000,
            low_income_pct=0.30,
            middle_income_pct=0.50,
            high_income_pct=0.20,
        )
        assert config.size == 1000

    def test_invalid_income_distribution(self) -> None:
        """Income percentages not summing to 1.0 should raise error."""
        with pytest.raises(ValueError, match="must sum to 1.0"):
            PopulationConfig(
                low_income_pct=0.30,
                middle_income_pct=0.50,
                high_income_pct=0.30,  # Sum = 1.1
            )


class TestCitizen:
    """Tests for Citizen dataclass."""

    def test_citizen_is_frozen(self) -> None:
        """Citizens should be immutable."""
        citizen = Citizen(
            id=1,
            age=35,
            gender="Male",
            income_level=IncomeLevel.MIDDLE,
            city_zone=CityZone.SUBURBAN,
            education_years=16,
            profession="Teacher",
            family_size=3,
            political_view=PoliticalView.MODERATE,
            risk_tolerance=0.5,
            openness_to_change=0.6,
        )
        with pytest.raises(Exception):  # FrozenInstanceError
            citizen.age = 36  # type: ignore


class TestPolicy:
    """Tests for Policy dataclass."""

    def test_policy_creation(self) -> None:
        """Policy should be creatable with all required fields."""
        policy = Policy(
            title="Test Policy",
            description="A test policy description",
            domain=PolicyDomain.ECONOMY,
        )
        assert policy.title == "Test Policy"
        assert policy.domain == PolicyDomain.ECONOMY
