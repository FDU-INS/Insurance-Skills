"""
PolicyPulse - Population Generation

Synthetic citizen population generation with configurable demographics.
Reference: PRD.md Feature F1 (Population Generation Engine)

Dependencies: numpy, data_models
"""

from __future__ import annotations

from typing import Literal

import numpy as np
from numpy.random import Generator

from src.data_models import (
    Citizen,
    CitizenState,
    CityZone,
    IncomeLevel,
    PoliticalView,
    PopulationConfig,
    ReactionMethod,
)
from src.utils import clamp


# =============================================================================
# Constants
# =============================================================================

# Gender options with distribution weights
GENDERS: list[Literal["Male", "Female", "Non-binary"]] = ["Male", "Female", "Non-binary"]
GENDER_WEIGHTS = [0.48, 0.48, 0.04]

# Profession lists by income level
# Reference: PRD.md - realistic attribute correlation
PROFESSIONS_BY_INCOME: dict[IncomeLevel, list[str]] = {
    IncomeLevel.LOW: [
        "Retail Worker",
        "Food Service Worker",
        "Warehouse Worker",
        "Janitor",
        "Home Health Aide",
        "Cashier",
        "Security Guard",
        "Farm Worker",
    ],
    IncomeLevel.MIDDLE: [
        "Teacher",
        "Nurse",
        "Accountant",
        "Sales Representative",
        "Office Manager",
        "Electrician",
        "Plumber",
        "Police Officer",
        "Firefighter",
        "IT Support",
    ],
    IncomeLevel.HIGH: [
        "Software Engineer",
        "Doctor",
        "Lawyer",
        "Executive",
        "Financial Analyst",
        "Consultant",
        "Architect",
        "Pharmacist",
        "Dentist",
        "Business Owner",
    ],
}

# Income ranges by level (annual, USD)
INCOME_RANGES: dict[IncomeLevel, tuple[float, float]] = {
    IncomeLevel.LOW: (15_000, 35_000),
    IncomeLevel.MIDDLE: (35_000, 80_000),
    IncomeLevel.HIGH: (80_000, 250_000),
}

# Education years correlation with income (mean, std)
EDUCATION_BY_INCOME: dict[IncomeLevel, tuple[float, float]] = {
    IncomeLevel.LOW: (11, 2),
    IncomeLevel.MIDDLE: (14, 2),
    IncomeLevel.HIGH: (18, 2),
}

# Base happiness by income level (mean, std)
HAPPINESS_BY_INCOME: dict[IncomeLevel, tuple[float, float]] = {
    IncomeLevel.LOW: (0.45, 0.15),
    IncomeLevel.MIDDLE: (0.60, 0.12),
    IncomeLevel.HIGH: (0.72, 0.10),
}

# City zone distribution by income level
ZONE_WEIGHTS_BY_INCOME: dict[IncomeLevel, dict[CityZone, float]] = {
    IncomeLevel.LOW: {
        CityZone.DOWNTOWN: 0.15,
        CityZone.INDUSTRIAL: 0.45,
        CityZone.SUBURBAN: 0.25,
        CityZone.RURAL: 0.15,
    },
    IncomeLevel.MIDDLE: {
        CityZone.DOWNTOWN: 0.20,
        CityZone.INDUSTRIAL: 0.15,
        CityZone.SUBURBAN: 0.50,
        CityZone.RURAL: 0.15,
    },
    IncomeLevel.HIGH: {
        CityZone.DOWNTOWN: 0.35,
        CityZone.INDUSTRIAL: 0.05,
        CityZone.SUBURBAN: 0.50,
        CityZone.RURAL: 0.10,
    },
}

# Political view distribution by income level
POLITICAL_WEIGHTS_BY_INCOME: dict[IncomeLevel, dict[PoliticalView, float]] = {
    IncomeLevel.LOW: {
        PoliticalView.PROGRESSIVE: 0.45,
        PoliticalView.MODERATE: 0.35,
        PoliticalView.CONSERVATIVE: 0.20,
    },
    IncomeLevel.MIDDLE: {
        PoliticalView.PROGRESSIVE: 0.30,
        PoliticalView.MODERATE: 0.45,
        PoliticalView.CONSERVATIVE: 0.25,
    },
    IncomeLevel.HIGH: {
        PoliticalView.PROGRESSIVE: 0.25,
        PoliticalView.MODERATE: 0.35,
        PoliticalView.CONSERVATIVE: 0.40,
    },
}


# =============================================================================
# Population Generation Functions
# =============================================================================

def generate_population(
    config: PopulationConfig,
    rng: Generator,
) -> list[Citizen]:
    """
    Generate a synthetic population of citizens.
    
    Creates citizens with correlated attributes based on income level.
    All citizens are valid by construction with realistic distributions.
    
    Args:
        config: Population configuration settings
        rng: Numpy random generator for reproducibility
        
    Returns:
        List of generated Citizen objects
        
    Raises:
        ValueError: If config has invalid population size
    """
    if config.size < 1:
        raise ValueError(f"Population size must be at least 1, got {config.size}")
    
    citizens: list[Citizen] = []
    
    for i in range(config.size):
        income_level = _assign_income_level(i, config.size, config)
        citizen = _generate_citizen_attributes(i, income_level, rng)
        citizens.append(citizen)
    
    return citizens


def generate_initial_states(
    citizens: list[Citizen],
    rng: Generator,
) -> list[CitizenState]:
    """
    Generate initial states (step 0) for all citizens.
    
    Initial happiness and income are correlated with income level.
    Initial policy support is neutral (0.0) with small random variance.
    
    Args:
        citizens: List of citizens to generate states for
        rng: Numpy random generator
        
    Returns:
        List of CitizenState objects for step 0
    """
    states: list[CitizenState] = []
    
    for citizen in citizens:
        # Generate income within range for income level
        income_min, income_max = INCOME_RANGES[citizen.income_level]
        income = rng.uniform(income_min, income_max)
        
        # Generate happiness correlated with income level
        happiness_mean, happiness_std = HAPPINESS_BY_INCOME[citizen.income_level]
        happiness = rng.normal(happiness_mean, happiness_std)
        happiness = clamp(happiness, 0.0, 1.0)
        
        # Initial policy support is neutral with small variance
        support = rng.normal(0.0, 0.1)
        support = clamp(support, -1.0, 1.0)
        
        state = CitizenState(
            citizen_id=citizen.id,
            step=0,
            happiness=happiness,
            policy_support=support,
            income=income,
            reaction_method=ReactionMethod.RULE_BASED,
            diary_entry=None,
        )
        states.append(state)
    
    return states


def _assign_income_level(
    index: int,
    total: int,
    config: PopulationConfig,
) -> IncomeLevel:
    """
    Determine income level for a citizen based on configured distribution.
    
    Uses index-based assignment to ensure exact percentages.
    
    Args:
        index: The citizen's index (0-based)
        total: Total population size
        config: Population configuration with income percentages
        
    Returns:
        The assigned IncomeLevel
    """
    low_count = int(total * config.low_income_pct)
    middle_count = int(total * config.middle_income_pct)
    
    if index < low_count:
        return IncomeLevel.LOW
    elif index < low_count + middle_count:
        return IncomeLevel.MIDDLE
    else:
        return IncomeLevel.HIGH


def _generate_citizen_attributes(
    citizen_id: int,
    income_level: IncomeLevel,
    rng: Generator,
) -> Citizen:
    """
    Generate all attributes for a single citizen.
    
    Attributes are correlated with income level per PRD specifications.
    
    Args:
        citizen_id: Unique identifier for this citizen
        income_level: The citizen's income level
        rng: Numpy random generator
        
    Returns:
        A fully populated Citizen object
    """
    # Age distribution: 18-75, normal around 42
    age = int(rng.normal(42, 15))
    age = max(18, min(75, age))
    
    # Gender with weighted selection - use index then lookup
    gender_idx = rng.choice(len(GENDERS), p=GENDER_WEIGHTS)
    gender = GENDERS[gender_idx]
    
    # City zone correlated with income - use index then lookup
    zone_weights = ZONE_WEIGHTS_BY_INCOME[income_level]
    zones = list(zone_weights.keys())
    zone_probs = list(zone_weights.values())
    zone_idx = rng.choice(len(zones), p=zone_probs)
    city_zone = zones[zone_idx]
    
    # Education years correlated with income
    edu_mean, edu_std = EDUCATION_BY_INCOME[income_level]
    education_years = int(rng.normal(edu_mean, edu_std))
    education_years = max(8, min(22, education_years))
    
    # Profession from income-appropriate list - use index then lookup
    professions = PROFESSIONS_BY_INCOME[income_level]
    prof_idx = rng.choice(len(professions))
    profession = professions[prof_idx]
    
    # Family size: 1-6, weighted toward smaller
    family_size = int(rng.exponential(1.5)) + 1
    family_size = max(1, min(6, family_size))
    
    # Political view correlated with income - use index then lookup
    political_weights = POLITICAL_WEIGHTS_BY_INCOME[income_level]
    views = list(political_weights.keys())
    view_probs = list(political_weights.values())
    view_idx = rng.choice(len(views), p=view_probs)
    political_view = views[view_idx]
    
    # Personality traits: uniform distribution
    risk_tolerance = float(rng.uniform(0.0, 1.0))
    openness_to_change = float(rng.uniform(0.0, 1.0))
    
    return Citizen(
        id=citizen_id,
        age=age,
        gender=gender,
        income_level=income_level,
        city_zone=city_zone,
        education_years=education_years,
        profession=profession,
        family_size=family_size,
        political_view=political_view,
        risk_tolerance=risk_tolerance,
        openness_to_change=openness_to_change,
    )


def get_population_summary(citizens: list[Citizen]) -> dict:
    """
    Generate summary statistics for a population.
    
    Args:
        citizens: List of citizens to summarize
        
    Returns:
        Dictionary with population summary statistics
    """
    if not citizens:
        return {"total": 0}
    
    # Count by income level
    income_counts = {level: 0 for level in IncomeLevel}
    for citizen in citizens:
        income_counts[citizen.income_level] += 1
    
    # Count by city zone
    zone_counts = {zone: 0 for zone in CityZone}
    for citizen in citizens:
        zone_counts[citizen.city_zone] += 1
    
    # Count by political view
    political_counts = {view: 0 for view in PoliticalView}
    for citizen in citizens:
        political_counts[citizen.political_view] += 1
    
    # Calculate averages
    ages = [c.age for c in citizens]
    education_years = [c.education_years for c in citizens]
    family_sizes = [c.family_size for c in citizens]
    
    return {
        "total": len(citizens),
        "income_distribution": {k.value: v for k, v in income_counts.items()},
        "zone_distribution": {k.value: v for k, v in zone_counts.items()},
        "political_distribution": {k.value: v for k, v in political_counts.items()},
        "avg_age": float(np.mean(ages)),
        "avg_education_years": float(np.mean(education_years)),
        "avg_family_size": float(np.mean(family_sizes)),
    }
