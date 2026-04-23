"""
PolicyPulse - Data Models

Dataclass definitions for all domain objects.
Reference: PRD.md Section 10.1 (Glossary), TECH_STACK.md Section 9

This module has NO external dependencies (stdlib only).
All other modules may import from here.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal
from enum import Enum


# =============================================================================
# Enumerations
# =============================================================================

class IncomeLevel(str, Enum):
    """Income level classification for citizens."""
    LOW = "Low"
    MIDDLE = "Middle"
    HIGH = "High"


class CityZone(str, Enum):
    """Geographic zones within the simulated city."""
    DOWNTOWN = "Downtown"
    INDUSTRIAL = "Industrial"
    SUBURBAN = "Suburban"
    RURAL = "Rural"


class PoliticalView(str, Enum):
    """Political orientation spectrum."""
    PROGRESSIVE = "Progressive"
    MODERATE = "Moderate"
    CONSERVATIVE = "Conservative"


class PolicyDomain(str, Enum):
    """Categories of policies that can be simulated."""
    ECONOMY = "Economy"
    EDUCATION = "Education"
    SOCIAL = "Social"
    BUSINESS = "Business"


class SimulationMode(str, Enum):
    """
    Simulation execution modes.
    
    PRECISION: LLM-powered reactions for maximum nuance (slower, API-dependent)
    BALANCED: Hybrid LLM sampling + neural network scaling
    SPEED: Trained neural network only (fast, no API required)
    """
    PRECISION = "Precision"
    BALANCED = "Balanced"
    SPEED = "Speed"


class ReactionMethod(str, Enum):
    """Method used to generate a citizen's reaction."""
    LLM = "LLM"
    NEURAL_NETWORK = "NeuralNetwork"
    RULE_BASED = "RuleBased"


# =============================================================================
# Core Data Models
# =============================================================================

@dataclass(frozen=True)
class Citizen:
    """
    A synthetic individual in the simulated population.
    
    Attributes are immutable once created. State changes are tracked
    separately in CitizenState objects.
    
    Reference: PRD.md Feature F1 (Population Generation Engine)
    """
    id: int
    age: int
    gender: Literal["Male", "Female", "Non-binary"]
    income_level: IncomeLevel
    city_zone: CityZone
    education_years: int
    profession: str
    family_size: int
    political_view: PoliticalView
    risk_tolerance: float  # 0.0 to 1.0
    openness_to_change: float  # 0.0 to 1.0


@dataclass
class CitizenState:
    """
    The condition of a citizen at a specific simulation step.
    
    Mutable to allow updates during simulation.
    
    Reference: PRD.md Section 10.1 (Glossary)
    """
    citizen_id: int
    step: int
    happiness: float  # 0.0 to 1.0
    policy_support: float  # -1.0 to 1.0
    income: float  # Annual income in dollars
    reaction_method: ReactionMethod = ReactionMethod.RULE_BASED
    diary_entry: str | None = None


@dataclass(frozen=True)
class Policy:
    """
    A defined intervention being simulated.
    
    Reference: PRD.md Feature F2 (Policy Definition Interface)
    """
    title: str
    description: str
    domain: PolicyDomain


@dataclass
class PopulationConfig:
    """
    Configuration for generating a synthetic population.
    
    Reference: PRD.md Feature F1
    """
    size: int = 1000
    low_income_pct: float = 0.30
    middle_income_pct: float = 0.50
    high_income_pct: float = 0.20
    random_seed: int | None = None

    def __post_init__(self) -> None:
        """Validate that income percentages sum to 1.0."""
        total = self.low_income_pct + self.middle_income_pct + self.high_income_pct
        if abs(total - 1.0) > 0.001:
            raise ValueError(f"Income percentages must sum to 1.0, got {total}")


@dataclass
class SimulationConfig:
    """
    Configuration for running a simulation.
    
    Reference: PRD.md Feature F3 (Hybrid AI Simulation Engine)
    """
    mode: SimulationMode = SimulationMode.BALANCED
    steps: int = 5
    llm_sample_size: int = 300  # Citizens sampled for LLM in Balanced mode
    ai_enabled: bool = False  # Whether AI enhancement is enabled
    ai_sample_pct: float = 0.1  # Percentage of citizens to sample for AI (0.0-1.0)
    ai_explanation_enabled: bool = True  # Generate AI explanations


@dataclass(frozen=True)
class AIStatus:
    """
    Status of AI integration for a simulation run.
    
    Provides transparency about what AI was used and any fallbacks.
    """
    ai_enabled: bool
    ai_available: bool  # Whether LLM was actually available
    citizens_sampled: int  # Number of citizens processed by AI
    ai_successes: int  # Successful AI reactions
    ai_failures: int  # Failures that fell back to rules
    error_message: str | None = None  # Last error if any


# =============================================================================
# Result Data Models
# =============================================================================

@dataclass
class StepMetrics:
    """
    Aggregated metrics for a single simulation step.
    
    Reference: DESIGN_DOC.md Section 3.3 (Metrics Cards)
    """
    step: int
    avg_happiness: float
    avg_support: float
    avg_income: float
    happiness_by_income: dict[IncomeLevel, float] = field(default_factory=dict)
    support_by_income: dict[IncomeLevel, float] = field(default_factory=dict)
    happiness_gap: float = 0.0  # High income happiness - Low income happiness


@dataclass
class SimulationResult:
    """
    Complete results of a simulation run.
    
    Reference: PRD.md Feature F8 (Scenario Management)
    """
    scenario_name: str
    policy: Policy
    config: SimulationConfig
    population_config: PopulationConfig
    citizens: list[Citizen]
    states_by_step: dict[int, list[CitizenState]]
    metrics_by_step: list[StepMetrics]
    method_counts: dict[int, dict[ReactionMethod, int]]  # step -> method -> count
    ai_status: AIStatus | None = None  # AI integration status
    ai_insight: str | None = None  # AI-generated summary insight (if available)


@dataclass
class ExpertPerspective:
    """
    AI-generated analysis from a stakeholder viewpoint.
    
    Reference: PRD.md Feature F7 (Expert Perspectives)
    """
    viewpoint: Literal["Economist", "Activist", "BusinessOwner"]
    analysis: str
    metrics_referenced: list[str] = field(default_factory=list)


@dataclass
class TrainingSample:
    """
    A single training sample for the neural network.
    
    Captures citizen features and their LLM-generated reaction deltas.
    Reference: TECH_STACK.md Section 5 (Feature Engineering)
    """
    features: list[float]  # 24-dimensional feature vector
    delta_happiness: float
    delta_support: float
    delta_income: float


@dataclass
class NNModelMetrics:
    """
    Performance metrics for the trained neural network.
    
    Reference: PRD.md Section 8.3 (Quality Metrics)
    """
    samples_count: int
    is_trained: bool
    mae_happiness: float | None = None
    mae_support: float | None = None
    mae_income: float | None = None
    last_training_time: str | None = None
