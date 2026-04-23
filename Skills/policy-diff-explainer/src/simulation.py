"""
PolicyPulse - Simulation Engine

Rule-based simulation engine for policy impact modeling.
Reference: PRD.md Feature F3 (Hybrid AI Simulation Engine)

This implementation provides:
1. Deterministic rule-based simulation (always works)
2. Optional AI-enhanced mode with automatic fallback
3. Explainability layer for both modes

Dependencies: data_models, utils, llm_client
"""

from __future__ import annotations

import logging
import numpy as np
from dataclasses import dataclass
from typing import Callable, TYPE_CHECKING

from numpy.random import Generator

from src.data_models import (
    Citizen,
    CitizenState,
    IncomeLevel,
    Policy,
    PolicyDomain,
    PoliticalView,
    CityZone,
    PopulationConfig,
    SimulationConfig,
    SimulationResult,
    StepMetrics,
    ReactionMethod,
    AIStatus,
)
from src.stats import calculate_step_metrics
from src.utils import clamp, create_rng

if TYPE_CHECKING:
    from src.llm_client import LLMClient
    from src.policy_analyzer import PolicyAnalysis


logger = logging.getLogger("policypulse.simulation")


# =============================================================================
# Policy Impact Rules
# =============================================================================

@dataclass(frozen=True)
class PolicyImpactRules:
    """
    Defines how a policy domain affects different demographic groups.
    
    All values are base multipliers that get adjusted by citizen attributes.
    Positive values indicate beneficial impact, negative indicate harmful.
    """
    # Base impact on happiness (before demographic adjustments)
    happiness_base: float
    
    # Impact modifiers by income level
    happiness_by_income: dict[IncomeLevel, float]
    
    # Base impact on income (percentage change)
    income_change_pct: float
    
    # Income change modifiers by income level
    income_change_by_income: dict[IncomeLevel, float]
    
    # Base policy support shift
    support_base: float
    
    # Support modifiers by political view
    support_by_politics: dict[PoliticalView, float]


# Define impact rules for each policy domain
POLICY_DOMAIN_RULES: dict[PolicyDomain, PolicyImpactRules] = {
    PolicyDomain.ECONOMY: PolicyImpactRules(
        happiness_base=0.02,
        happiness_by_income={
            IncomeLevel.LOW: -0.03,      # Economic policies often favor wealthy
            IncomeLevel.MIDDLE: 0.01,
            IncomeLevel.HIGH: 0.05,
        },
        income_change_pct=0.02,
        income_change_by_income={
            IncomeLevel.LOW: 0.005,
            IncomeLevel.MIDDLE: 0.015,
            IncomeLevel.HIGH: 0.03,
        },
        support_base=0.0,
        support_by_politics={
            PoliticalView.PROGRESSIVE: -0.05,
            PoliticalView.MODERATE: 0.02,
            PoliticalView.CONSERVATIVE: 0.08,
        },
    ),
    PolicyDomain.EDUCATION: PolicyImpactRules(
        happiness_base=0.03,
        happiness_by_income={
            IncomeLevel.LOW: 0.05,       # Education helps lower income most
            IncomeLevel.MIDDLE: 0.03,
            IncomeLevel.HIGH: 0.01,
        },
        income_change_pct=0.01,
        income_change_by_income={
            IncomeLevel.LOW: 0.02,
            IncomeLevel.MIDDLE: 0.01,
            IncomeLevel.HIGH: 0.005,
        },
        support_base=0.05,
        support_by_politics={
            PoliticalView.PROGRESSIVE: 0.10,
            PoliticalView.MODERATE: 0.05,
            PoliticalView.CONSERVATIVE: -0.02,
        },
    ),
    PolicyDomain.SOCIAL: PolicyImpactRules(
        happiness_base=0.04,
        happiness_by_income={
            IncomeLevel.LOW: 0.06,       # Social policies help vulnerable
            IncomeLevel.MIDDLE: 0.03,
            IncomeLevel.HIGH: -0.01,
        },
        income_change_pct=0.005,
        income_change_by_income={
            IncomeLevel.LOW: 0.015,
            IncomeLevel.MIDDLE: 0.005,
            IncomeLevel.HIGH: -0.005,    # May include taxes
        },
        support_base=0.03,
        support_by_politics={
            PoliticalView.PROGRESSIVE: 0.12,
            PoliticalView.MODERATE: 0.03,
            PoliticalView.CONSERVATIVE: -0.08,
        },
    ),
    PolicyDomain.BUSINESS: PolicyImpactRules(
        happiness_base=0.01,
        happiness_by_income={
            IncomeLevel.LOW: -0.02,
            IncomeLevel.MIDDLE: 0.02,
            IncomeLevel.HIGH: 0.06,      # Business policies favor wealthy
        },
        income_change_pct=0.025,
        income_change_by_income={
            IncomeLevel.LOW: 0.01,
            IncomeLevel.MIDDLE: 0.02,
            IncomeLevel.HIGH: 0.04,
        },
        support_base=-0.02,
        support_by_politics={
            PoliticalView.PROGRESSIVE: -0.10,
            PoliticalView.MODERATE: 0.0,
            PoliticalView.CONSERVATIVE: 0.10,
        },
    ),
}

# Zone-based modifiers (urban areas see faster change)
ZONE_CHANGE_MULTIPLIER: dict[CityZone, float] = {
    CityZone.DOWNTOWN: 1.3,
    CityZone.INDUSTRIAL: 1.1,
    CityZone.SUBURBAN: 1.0,
    CityZone.RURAL: 0.8,
}


# =============================================================================
# Simulation Engine
# =============================================================================

def run_simulation(
    policy: Policy,
    citizens: list[Citizen],
    initial_states: list[CitizenState],
    config: SimulationConfig,
    population_config: PopulationConfig,
    scenario_name: str,
    rng: Generator | None = None,
    progress_callback: Callable[[int, int], None] | None = None,
    llm_client: "LLMClient | None" = None,
) -> SimulationResult:
    """
    Run a complete simulation with optional AI enhancement.
    
    The simulation ALWAYS completes using rule-based logic as the foundation.
    AI enhancement is optional and uses a strict fallback chain:
    LLM → rule-based (never fails)
    
    Args:
        policy: The policy being simulated
        citizens: Generated population (immutable)
        initial_states: Initial citizen states (step 0)
        config: Simulation configuration (includes ai_enabled flag)
        population_config: Population configuration
        scenario_name: Name for this simulation run
        rng: Random number generator for reproducibility
        progress_callback: Optional callback(step, total) for progress updates
        llm_client: Optional LLM client for AI-enhanced mode
        
    Returns:
        Complete simulation results with metrics per step
        
    Invariants:
        - Simulation ALWAYS completes
        - AI failure degrades gracefully to rule-based
        - All values stay in valid ranges
    """
    if rng is None:
        rng = create_rng(population_config.random_seed)
    
    # Initialize storage
    states_by_step: dict[int, list[CitizenState]] = {0: initial_states}
    metrics_by_step: list[StepMetrics] = []
    method_counts: dict[int, dict[ReactionMethod, int]] = {}
    
    # Calculate initial metrics
    initial_metrics = calculate_step_metrics(citizens, initial_states, step=0)
    metrics_by_step.append(initial_metrics)
    method_counts[0] = {ReactionMethod.RULE_BASED: len(citizens)}
    
    # Create citizen lookup for efficient access
    citizen_by_id = {c.id: c for c in citizens}
    
    # Determine AI availability
    ai_enabled = config.ai_enabled and llm_client is not None
    ai_available = ai_enabled and llm_client.is_available if llm_client else False
    
    # Track AI usage
    ai_successes = 0
    ai_failures = 0
    last_error: str | None = None
    
    # POLICY UNDERSTANDING: ALWAYS analyze policy with LLM if available
    # This gives intelligent predictions even when AI sampling is disabled
    policy_analysis: PolicyAnalysis | None = None
    if llm_client is not None and llm_client.is_available:
        try:
            from src.policy_analyzer import analyze_policy_with_llm
            logger.info(f"🔍 Analyzing policy with LLM: {policy.title}")
            policy_analysis = analyze_policy_with_llm(policy, llm_client)
            logger.info(
                f"✅ Policy analysis complete (confidence: {policy_analysis.confidence:.2f}) - "
                f"Predictions will use LLM-analyzed features instead of generic rules"
            )
        except Exception as e:
            logger.warning(f"⚠️ Policy analysis failed, falling back to generic rules: {e}")
            policy_analysis = None
    else:
        logger.info("ℹ️ LLM not available - using generic rule-based predictions")
    
    # Deterministically select citizens for AI sampling (if enabled)
    ai_sample_indices: set[int] = set()
    if ai_enabled:
        sample_count = max(1, int(len(citizens) * config.ai_sample_pct))
        sample_count = min(sample_count, len(citizens))
        # Use deterministic selection based on citizen IDs sorted
        sorted_ids = sorted(c.id for c in citizens)
        # Sample evenly across the sorted IDs
        step_size = max(1, len(sorted_ids) // sample_count)
        ai_sample_indices = {sorted_ids[i * step_size] for i in range(sample_count)}
        logger.info(f"AI sampling enabled: {len(ai_sample_indices)} citizens selected")
    
    # Run simulation steps
    for step in range(1, config.steps + 1):
        if progress_callback:
            progress_callback(step, config.steps)
        
        # Get previous states
        previous_states = states_by_step[step - 1]
        
        # Calculate new states with optional AI enhancement
        new_states, step_method_counts, step_ai_successes, step_ai_failures, step_error = _run_step_with_ai(
            citizens=citizens,
            citizen_by_id=citizen_by_id,
            previous_states=previous_states,
            policy=policy,
            step=step,
            rng=rng,
            ai_enabled=ai_enabled,
            ai_sample_indices=ai_sample_indices,
            llm_client=llm_client,
            generate_explanations=config.ai_explanation_enabled,
            policy_analysis=policy_analysis,  # Pass policy understanding
        )
        
        # Store states and metrics
        states_by_step[step] = new_states
        step_metrics = calculate_step_metrics(citizens, new_states, step)
        metrics_by_step.append(step_metrics)
        method_counts[step] = step_method_counts
        
        # Track AI usage
        ai_successes += step_ai_successes
        ai_failures += step_ai_failures
        if step_error:
            last_error = step_error
    
    # Create AI status
    ai_status = AIStatus(
        ai_enabled=config.ai_enabled,
        ai_available=ai_available,
        citizens_sampled=len(ai_sample_indices) * config.steps if ai_enabled else 0,
        ai_successes=ai_successes,
        ai_failures=ai_failures,
        error_message=last_error,
    )
    
    # Generate AI insight if available and enabled
    ai_insight: str | None = None
    if ai_enabled and llm_client and ai_available and ai_successes > 0:
        ai_insight = _generate_ai_insight(policy, metrics_by_step, llm_client)
    
    # Collect reinforcement learning feedback if policy analysis was used
    if policy_analysis is not None:
        try:
            from src.rl_trainer import RLTrainer
            rl_trainer = RLTrainer()
            
            # Create temporary result for feedback (before returning final result)
            temp_result = SimulationResult(
                scenario_name=scenario_name,
                policy=policy,
                config=config,
                population_config=population_config,
                citizens=citizens,
                states_by_step=states_by_step,
                metrics_by_step=metrics_by_step,
                method_counts=method_counts,
                ai_status=AIStatus(
                    ai_enabled=config.ai_enabled,
                    ai_available=ai_available,
                    citizens_sampled=len(ai_sample_indices) * config.steps if ai_enabled else 0,
                    ai_successes=ai_successes,
                    ai_failures=ai_failures,
                    error_message=last_error,
                ),
                ai_insight=ai_insight,
            )
            
            feedback = rl_trainer.collect_feedback(policy_analysis, temp_result)
            logger.info(f"RL feedback collected: error={feedback.happiness_error + feedback.support_error:.3f}")
        except Exception as e:
            logger.warning(f"Failed to collect RL feedback: {e}")
    
    return SimulationResult(
        scenario_name=scenario_name,
        policy=policy,
        config=config,
        population_config=population_config,
        citizens=citizens,
        states_by_step=states_by_step,
        metrics_by_step=metrics_by_step,
        method_counts=method_counts,
        ai_status=ai_status,
        ai_insight=ai_insight,
    )


def _run_step_with_ai(
    citizens: list[Citizen],
    citizen_by_id: dict[int, Citizen],
    previous_states: list[CitizenState],
    policy: Policy,
    step: int,
    rng: Generator,
    ai_enabled: bool,
    ai_sample_indices: set[int],
    llm_client: "LLMClient | None",
    generate_explanations: bool,
    policy_analysis: "PolicyAnalysis | None" = None,
) -> tuple[list[CitizenState], dict[ReactionMethod, int], int, int, str | None]:
    """
    Run a single simulation step with optional AI enhancement.
    
    Priority order:
    1. LLM reactions (for sampled citizens if AI enabled)
    2. Neural Network predictions (for all non-LLM citizens)
    3. Rule-based fallback (if NN fails)
    
    Args:
        citizens: All citizens
        citizen_by_id: Lookup dict
        previous_states: States from previous step
        policy: Policy being simulated
        step: Current step number
        rng: Random generator
        ai_enabled: Whether AI is enabled
        ai_sample_indices: Citizen IDs selected for AI sampling
        llm_client: LLM client (may be None)
        generate_explanations: Whether to generate explanations
        policy_analysis: Optional policy analysis for intelligent weighting
        
    Returns:
        Tuple of (new_states, method_counts, ai_successes, ai_failures, error_msg)
    """
    new_states: list[CitizenState] = []
    method_counts: dict[ReactionMethod, int] = {
        ReactionMethod.RULE_BASED: 0,
        ReactionMethod.LLM: 0,
        ReactionMethod.NEURAL_NETWORK: 0,
    }
    ai_successes = 0
    ai_failures = 0
    last_error: str | None = None
    
    # Import here to avoid circular imports
    from src.llm_client import (
        LLMError,
        generate_rule_based_explanation,
    )
    from src.nn_model import NeuralNetworkModel
    from src.rl_agent import RLAgent
    from src.config import NN_MODEL_PATH, FEATURE_SCALER_PATH, RL_MODEL_PATH
    
    # Initialize NN model (will use heuristics if not trained)
    nn_model = NeuralNetworkModel()
    nn_model.load(NN_MODEL_PATH, FEATURE_SCALER_PATH)  # Try to load, falls back if not available
    
    # Initialize RL agent for real-time learning
    rl_agent = RLAgent()
    try:
        rl_agent.load(RL_MODEL_PATH)
        logger.info(f"RL agent loaded with {rl_agent.total_experiences} experiences")
    except Exception:
        logger.info("Starting with fresh RL agent")
    
    for prev_state in previous_states:
        citizen = citizen_by_id[prev_state.citizen_id]
        
        # Determine if this citizen should use AI
        use_ai = (
            ai_enabled
            and citizen.id in ai_sample_indices
            and llm_client is not None
            and llm_client.is_available
        )
        
        # Initialize defaults
        delta_happiness = 0.0
        delta_support = 0.0
        delta_income_pct = 0.0
        diary_entry: str | None = None
        reaction_method = ReactionMethod.NEURAL_NETWORK  # Default to NN
        
        if use_ai:
            # Try AI reaction with fallback to NN
            try:
                result = llm_client.generate_citizen_reaction(
                    citizen=citizen,
                    current_state=prev_state,
                    policy=policy,
                    step=step,
                )
                
                delta_happiness = result.delta_happiness
                delta_support = result.delta_support
                delta_income_pct = result.delta_income_pct
                diary_entry = result.explanation if generate_explanations else None
                reaction_method = ReactionMethod.LLM
                ai_successes += 1
                
            except LLMError as e:
                # Fallback to NN on LLM error
                logger.warning(f"LLM failed for citizen {citizen.id}, falling back to NN: {e}")
                ai_failures += 1
                last_error = str(e)
                
                # Use neural network
                try:
                    delta_happiness, delta_support, delta_income_pct = nn_model.predict(
                        citizen=citizen,
                        current_state=prev_state,
                        policy=policy,
                    )
                    reaction_method = ReactionMethod.NEURAL_NETWORK
                except Exception as nn_error:
                    # Ultimate fallback to rules
                    logger.warning(f"NN also failed, using rules: {nn_error}")
                    delta_happiness, delta_support, delta_income = apply_rule_based_reaction(
                        citizen=citizen,
                        current_state=prev_state,
                        policy=policy,
                        step=step,
                        rng=rng,
                    )
                    delta_income_pct = delta_income / prev_state.income if prev_state.income > 0 else 0.0
                    reaction_method = ReactionMethod.RULE_BASED
                
                if generate_explanations:
                    diary_entry = generate_rule_based_explanation(
                        citizen=citizen,
                        delta_happiness=delta_happiness,
                        delta_support=delta_support,
                        policy_domain=policy.domain.value,
                    )
        else:
            # Use RL Agent first, then Neural Network, then rules
            state_features = None
            rl_predicted_deltas = None
            
            try:
                # Build feature vector for RL agent
                state_features = nn_model.build_feature_vector(
                    citizen=citizen,
                    current_state=prev_state,
                    policy=policy,
                )
                
                # Get RL prediction
                delta_happiness, delta_support, delta_income_pct = rl_agent.predict(
                    state_features=state_features,
                    use_exploration=True,  # Enable exploration during simulation
                )
                rl_predicted_deltas = (delta_happiness, delta_support, delta_income_pct)
                reaction_method = ReactionMethod.NEURAL_NETWORK  # RL uses NN internally
                
            except Exception as e:
                # Fallback to policy-aware or standard rules
                logger.debug(f"RL/NN prediction failed for citizen {citizen.id}, using rules: {e}")
                
                if policy_analysis is not None:
                    # POLICY-AWARE: Use LLM understanding of policy
                    from src.policy_analyzer import apply_policy_aware_reaction
                    delta_happiness, delta_support, delta_income = apply_policy_aware_reaction(
                        citizen=citizen,
                        current_state=prev_state,
                        policy=policy,
                        policy_analysis=policy_analysis,
                        step=step,
                        rng=rng,
                    )
                else:
                    # Standard rule-based reaction
                    delta_happiness, delta_support, delta_income = apply_rule_based_reaction(
                        citizen=citizen,
                        current_state=prev_state,
                        policy=policy,
                        step=step,
                        rng=rng,
                    )
                
                delta_income_pct = delta_income / prev_state.income if prev_state.income > 0 else 0.0
                reaction_method = ReactionMethod.RULE_BASED
            
            if generate_explanations and citizen.id in ai_sample_indices:
                # Generate template explanation for sampled citizens
                diary_entry = generate_rule_based_explanation(
                    citizen=citizen,
                    delta_happiness=delta_happiness,
                    delta_support=delta_support,
                    policy_domain=policy.domain.value,
                )
        
        # Apply deltas to create new state (immutable pattern)
        delta_income = prev_state.income * delta_income_pct
        new_happiness = clamp(prev_state.happiness + delta_happiness, 0.0, 1.0)
        new_support = clamp(prev_state.policy_support + delta_support, -1.0, 1.0)
        new_income = max(0.0, prev_state.income + delta_income)
        
        new_state = CitizenState(
            citizen_id=citizen.id,
            step=step,
            happiness=new_happiness,
            policy_support=new_support,
            income=new_income,
            reaction_method=reaction_method,
            diary_entry=diary_entry,
        )
        new_states.append(new_state)
        method_counts[reaction_method] = method_counts.get(reaction_method, 0) + 1
        
        # RL LEARNING: Store experience and learn from actual outcomes
        if state_features is not None and rl_predicted_deltas is not None:
            # Calculate actual deltas
            actual_happiness_change = new_happiness - prev_state.happiness
            actual_support_change = new_support - prev_state.policy_support
            actual_income_change_pct = (new_income - prev_state.income) / prev_state.income if prev_state.income > 0 else 0.0
            
            actual_deltas = (actual_happiness_change, actual_support_change, actual_income_change_pct)
            
            # Build policy features
            policy_features = np.zeros(4)  # One-hot for policy domain
            domain_mapping = {
                PolicyDomain.ECONOMY: 0,
                PolicyDomain.EDUCATION: 1,
                PolicyDomain.SOCIAL: 2,
                PolicyDomain.BUSINESS: 3,
            }
            policy_features[domain_mapping[policy.domain]] = 1.0
            
            # Store experience and trigger learning
            reward = rl_agent.store_experience(
                state_features=state_features,
                predicted_deltas=rl_predicted_deltas,
                actual_deltas=actual_deltas,
                policy_features=policy_features,
            )
            
            # Periodically log RL progress
            if len(new_states) % 1000 == 0:
                stats = rl_agent.get_stats()
                logger.info(
                    f"RL Progress: {stats['total_experiences']} experiences, "
                    f"avg_reward={stats['avg_recent_reward']:.4f}, "
                    f"epsilon={stats['epsilon']:.3f}"
                )
    
    # Save RL agent after step completion
    try:
        rl_agent.save(RL_MODEL_PATH)
        logger.debug(f"RL agent saved: {rl_agent.total_experiences} experiences")
    except Exception as e:
        logger.warning(f"Failed to save RL agent: {e}")
    
    return new_states, method_counts, ai_successes, ai_failures, last_error


def _generate_ai_insight(
    policy: Policy,
    metrics_by_step: list[StepMetrics],
    llm_client: "LLMClient",
) -> str | None:
    """
    Generate an AI insight for the simulation results.
    
    Falls back to rule-based insight on failure.
    """
    from src.llm_client import LLMError, generate_rule_based_summary_insight
    
    if len(metrics_by_step) < 2:
        return None
    
    initial = metrics_by_step[0]
    final = metrics_by_step[-1]
    
    metrics = {
        "initial_happiness": initial.avg_happiness,
        "final_happiness": final.avg_happiness,
        "happiness_change": final.avg_happiness - initial.avg_happiness,
        "initial_support": initial.avg_support,
        "final_support": final.avg_support,
        "support_change": final.avg_support - initial.avg_support,
        "initial_income": initial.avg_income,
        "final_income": final.avg_income,
        "income_change": final.avg_income - initial.avg_income,
        "initial_gap": initial.happiness_gap,
        "final_gap": final.happiness_gap,
        "gap_change": final.happiness_gap - initial.happiness_gap,
    }
    
    try:
        result = llm_client.generate_summary_insight(policy, metrics)
        return result.insight
    except LLMError as e:
        logger.warning(f"LLM insight generation failed, using rule-based: {e}")
        return generate_rule_based_summary_insight(
            policy_domain=policy.domain.value,
            happiness_change=metrics["happiness_change"],
            support_change=metrics["support_change"],
            gap_change=metrics["gap_change"],
        )


def apply_rule_based_reaction(
    citizen: Citizen,
    current_state: CitizenState,
    policy: Policy,
    step: int,
    rng: Generator,
) -> tuple[float, float, float]:
    """
    Apply rule-based reaction logic to compute state deltas.
    
    Uses policy domain rules, citizen demographics, and personality
    to determine how the citizen reacts to the policy.
    
    Args:
        citizen: The citizen reacting
        current_state: Their current state
        policy: The policy being reacted to
        step: Current simulation step
        rng: Random number generator for variance
        
    Returns:
        Tuple of (delta_happiness, delta_support, delta_income)
    """
    # Get policy rules
    rules = POLICY_DOMAIN_RULES[policy.domain]
    
    # Base impacts
    happiness_delta = rules.happiness_base
    support_delta = rules.support_base
    income_delta_pct = rules.income_change_pct
    
    # Apply income level modifiers
    happiness_delta += rules.happiness_by_income[citizen.income_level]
    income_delta_pct += rules.income_change_by_income[citizen.income_level]
    
    # Apply political view modifiers
    support_delta += rules.support_by_politics[citizen.political_view]
    
    # Apply zone multiplier (urban areas change faster)
    zone_mult = ZONE_CHANGE_MULTIPLIER[citizen.city_zone]
    happiness_delta *= zone_mult
    support_delta *= zone_mult
    
    # Apply personality modifiers
    # - High openness to change amplifies positive effects
    # - High risk tolerance amplifies all effects
    openness_factor = 0.5 + citizen.openness_to_change * 0.5  # 0.5 to 1.0
    risk_factor = 0.7 + citizen.risk_tolerance * 0.6  # 0.7 to 1.3
    
    if happiness_delta > 0:
        happiness_delta *= openness_factor
    happiness_delta *= risk_factor
    support_delta *= risk_factor
    
    # Apply step decay (impact diminishes over time)
    decay_factor = 1.0 / (1.0 + step * 0.1)  # Gradual decay
    happiness_delta *= decay_factor
    support_delta *= decay_factor
    
    # Add small random variance for realism
    variance = 0.01
    happiness_delta += rng.normal(0, variance)
    support_delta += rng.normal(0, variance)
    
    # Calculate income change in dollars
    income_delta = current_state.income * income_delta_pct * decay_factor
    
    # Education slightly amplifies positive outcomes
    education_bonus = (citizen.education_years - 12) * 0.002  # +/- based on education
    if happiness_delta > 0:
        happiness_delta += education_bonus
    
    # Family size affects sensitivity (larger families more cautious)
    family_sensitivity = 1.0 - (citizen.family_size - 1) * 0.05
    family_sensitivity = max(0.7, family_sensitivity)
    happiness_delta *= family_sensitivity
    
    return happiness_delta, support_delta, income_delta


def get_simulation_summary(result: SimulationResult) -> dict:
    """
    Generate a summary of simulation results.
    
    Args:
        result: Completed simulation result
        
    Returns:
        Dictionary with summary statistics
    """
    if not result.metrics_by_step:
        return {}
    
    initial = result.metrics_by_step[0]
    final = result.metrics_by_step[-1]
    
    return {
        "scenario_name": result.scenario_name,
        "policy_title": result.policy.title,
        "policy_domain": result.policy.domain.value,
        "steps": result.config.steps,
        "population_size": len(result.citizens),
        "initial_happiness": initial.avg_happiness,
        "final_happiness": final.avg_happiness,
        "happiness_change": final.avg_happiness - initial.avg_happiness,
        "initial_support": initial.avg_support,
        "final_support": final.avg_support,
        "support_change": final.avg_support - initial.avg_support,
        "initial_income": initial.avg_income,
        "final_income": final.avg_income,
        "income_change": final.avg_income - initial.avg_income,
        "initial_gap": initial.happiness_gap,
        "final_gap": final.happiness_gap,
        "gap_change": final.happiness_gap - initial.happiness_gap,
    }
