"""
PolicyPulse - Policy Analyzer

Uses LLM to understand policy text and generate policy-specific impact weights.
This replaces random guessing with actual policy comprehension.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from src.data_models import (
    Policy,
    PolicyDomain,
    IncomeLevel,
    PoliticalView,
    CityZone,
)

if TYPE_CHECKING:
    from src.llm_client import LLMClient


@dataclass
class PolicyAnalysis:
    """
    LLM-generated analysis of a policy's expected impacts.
    
    This replaces hardcoded rules with policy-specific understanding.
    """
    # Overall sentiment
    is_progressive: float  # 0.0 (conservative) to 1.0 (progressive)
    is_redistributive: float  # 0.0 (no) to 1.0 (yes)
    
    # Impact predictions by income level
    low_income_happiness_impact: float  # -1.0 to +1.0
    middle_income_happiness_impact: float
    high_income_happiness_impact: float
    
    low_income_income_impact: float  # Percentage change
    middle_income_income_impact: float
    high_income_income_impact: float
    
    # Political alignment scores
    progressive_support: float  # -1.0 to +1.0
    moderate_support: float
    conservative_support: float
    
    # Feature importance weights (for ML model)
    income_level_weight: float  # 0.0 to 1.0
    political_view_weight: float
    education_weight: float
    age_weight: float
    family_size_weight: float
    zone_weight: float
    
    # Confidence score
    confidence: float  # 0.0 to 1.0


def analyze_policy_with_llm(
    policy: Policy,
    llm_client: LLMClient,
) -> PolicyAnalysis:
    """
    Use LLM to analyze policy text and predict impacts.
    
    This replaces generic domain rules with policy-specific understanding.
    
    Args:
        policy: The policy to analyze
        llm_client: LLM client for analysis
        
    Returns:
        Policy analysis with predicted impacts and feature weights
    """
    prompt = f"""You are a policy impact analyst. Analyze this policy and predict its impacts on different demographic groups.

Policy Title: {policy.title}
Policy Domain: {policy.domain.value}
Policy Description: {policy.description}

Analyze and provide:

1. POLICY ORIENTATION (0.0 to 1.0):
   - is_progressive: How progressive is this policy? (0.0 = very conservative, 1.0 = very progressive)
   - is_redistributive: Does it redistribute wealth? (0.0 = no, 1.0 = yes)

2. HAPPINESS IMPACT BY INCOME LEVEL (-1.0 to +1.0):
   - low_income_happiness: How will low-income people's happiness change?
   - middle_income_happiness: How will middle-income people's happiness change?
   - high_income_happiness: How will high-income people's happiness change?

3. INCOME IMPACT BY INCOME LEVEL (percentage change):
   - low_income_income: Percentage income change for low-income people
   - middle_income_income: Percentage income change for middle-income people
   - high_income_income: Percentage income change for high-income people

4. POLITICAL SUPPORT SCORES (-1.0 to +1.0):
   - progressive_support: How much will progressives support this?
   - moderate_support: How much will moderates support this?
   - conservative_support: How much will conservatives support this?

5. FEATURE IMPORTANCE WEIGHTS (0.0 to 1.0):
Which citizen characteristics matter most for this policy?
   - income_level_weight: How much does income level matter?
   - political_view_weight: How much does political view matter?
   - education_weight: How much does education matter?
   - age_weight: How much does age matter?
   - family_size_weight: How much does family size matter?
   - zone_weight: How much does city zone matter?

6. CONFIDENCE (0.0 to 1.0):
   - confidence: How confident are you in this analysis?

Respond with ONLY a JSON object with these exact keys (use underscores):
{{
    "is_progressive": 0.0-1.0,
    "is_redistributive": 0.0-1.0,
    "low_income_happiness_impact": -1.0 to +1.0,
    "middle_income_happiness_impact": -1.0 to +1.0,
    "high_income_happiness_impact": -1.0 to +1.0,
    "low_income_income_impact": percentage as decimal,
    "middle_income_income_impact": percentage as decimal,
    "high_income_income_impact": percentage as decimal,
    "progressive_support": -1.0 to +1.0,
    "moderate_support": -1.0 to +1.0,
    "conservative_support": -1.0 to +1.0,
    "income_level_weight": 0.0-1.0,
    "political_view_weight": 0.0-1.0,
    "education_weight": 0.0-1.0,
    "age_weight": 0.0-1.0,
    "family_size_weight": 0.0-1.0,
    "zone_weight": 0.0-1.0,
    "confidence": 0.0-1.0
}}"""

    try:
        import json
        
        response = llm_client.generate(prompt, max_tokens=500, temperature=0.3)
        
        # Extract JSON from response
        response_text = response.strip()
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0]
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0]
        
        data = json.loads(response_text.strip())
        
        return PolicyAnalysis(
            is_progressive=float(data["is_progressive"]),
            is_redistributive=float(data["is_redistributive"]),
            low_income_happiness_impact=float(data["low_income_happiness_impact"]),
            middle_income_happiness_impact=float(data["middle_income_happiness_impact"]),
            high_income_happiness_impact=float(data["high_income_happiness_impact"]),
            low_income_income_impact=float(data["low_income_income_impact"]),
            middle_income_income_impact=float(data["middle_income_income_impact"]),
            high_income_income_impact=float(data["high_income_income_impact"]),
            progressive_support=float(data["progressive_support"]),
            moderate_support=float(data["moderate_support"]),
            conservative_support=float(data["conservative_support"]),
            income_level_weight=float(data["income_level_weight"]),
            political_view_weight=float(data["political_view_weight"]),
            education_weight=float(data["education_weight"]),
            age_weight=float(data["age_weight"]),
            family_size_weight=float(data["family_size_weight"]),
            zone_weight=float(data["zone_weight"]),
            confidence=float(data["confidence"]),
        )
        
    except Exception as e:
        # Fallback to neutral analysis if LLM fails
        return PolicyAnalysis(
            is_progressive=0.5,
            is_redistributive=0.3,
            low_income_happiness_impact=0.02,
            middle_income_happiness_impact=0.01,
            high_income_happiness_impact=0.01,
            low_income_income_impact=0.01,
            middle_income_income_impact=0.01,
            high_income_income_impact=0.01,
            progressive_support=0.0,
            moderate_support=0.0,
            conservative_support=0.0,
            income_level_weight=0.5,
            political_view_weight=0.5,
            education_weight=0.3,
            age_weight=0.2,
            family_size_weight=0.2,
            zone_weight=0.3,
            confidence=0.3,
        )


def apply_policy_aware_reaction(
    citizen: "Citizen",
    current_state: "CitizenState",
    policy: Policy,
    policy_analysis: PolicyAnalysis,
    step: int,
    rng: "Generator",
) -> tuple[float, float, float]:
    """
    Apply policy-aware reaction using LLM analysis instead of hardcoded rules.
    
    This uses the actual policy understanding to generate realistic reactions.
    
    Args:
        citizen: The citizen reacting
        current_state: Their current state
        policy: The policy being reacted to
        policy_analysis: LLM analysis of the policy
        step: Current simulation step
        rng: Random number generator
        
    Returns:
        Tuple of (delta_happiness, delta_support, delta_income)
    """
    from src.data_models import Citizen, CitizenState
    from numpy.random import Generator
    
    # Get base impacts from policy analysis based on citizen's income level
    if citizen.income_level == IncomeLevel.LOW:
        happiness_base = policy_analysis.low_income_happiness_impact
        income_change_pct = policy_analysis.low_income_income_impact
    elif citizen.income_level == IncomeLevel.MIDDLE:
        happiness_base = policy_analysis.middle_income_happiness_impact
        income_change_pct = policy_analysis.middle_income_income_impact
    else:  # HIGH
        happiness_base = policy_analysis.high_income_happiness_impact
        income_change_pct = policy_analysis.high_income_income_impact
    
    # Get support based on political view
    if citizen.political_view == PoliticalView.PROGRESSIVE:
        support_base = policy_analysis.progressive_support
    elif citizen.political_view == PoliticalView.MODERATE:
        support_base = policy_analysis.moderate_support
    else:  # CONSERVATIVE
        support_base = policy_analysis.conservative_support
    
    # Apply feature weights from policy analysis
    # These weights tell us which citizen characteristics matter for THIS policy
    
    # Education factor (weighted by policy)
    if policy_analysis.education_weight > 0.5:
        education_factor = (citizen.education_years - 12) / 10  # -1.2 to 1.3
        happiness_base += education_factor * 0.1 * policy_analysis.education_weight
    
    # Age factor (weighted by policy)
    if policy_analysis.age_weight > 0.5:
        age_factor = (citizen.age - 40) / 40  # -1.0 to 1.5
        # Older people might be more cautious
        happiness_base *= (1.0 - abs(age_factor) * 0.1 * policy_analysis.age_weight)
    
    # Family size factor (weighted by policy)
    if policy_analysis.family_size_weight > 0.5:
        family_factor = 1.0 - (citizen.family_size - 1) * 0.05 * policy_analysis.family_size_weight
        family_factor = max(0.7, family_factor)
        happiness_base *= family_factor
    
    # Zone factor (weighted by policy)
    if policy_analysis.zone_weight > 0.5:
        zone_multipliers = {
            CityZone.DOWNTOWN: 1.2,
            CityZone.INDUSTRIAL: 1.0,
            CityZone.SUBURBAN: 0.9,
            CityZone.RURAL: 0.8,
        }
        zone_mult = zone_multipliers.get(citizen.city_zone, 1.0)
        happiness_base *= zone_mult * policy_analysis.zone_weight
    
    # Personality modifiers
    openness_factor = 0.5 + citizen.openness_to_change * 0.5
    risk_factor = 0.7 + citizen.risk_tolerance * 0.6
    
    if happiness_base > 0:
        happiness_base *= openness_factor
    happiness_base *= risk_factor
    support_base *= risk_factor
    
    # Time decay
    decay = 1.0 / (1.0 + step * 0.1)
    happiness_base *= decay
    support_base *= decay
    income_change_pct *= decay
    
    # Add small variance
    happiness_base += rng.normal(0, 0.01)
    support_base += rng.normal(0, 0.01)
    
    # Calculate income change
    income_delta = current_state.income * income_change_pct
    
    return happiness_base, support_base, income_delta
