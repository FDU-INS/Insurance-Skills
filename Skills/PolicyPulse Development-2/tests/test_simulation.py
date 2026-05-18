"""
Tests for simulation engine module.
"""

from __future__ import annotations

import pytest

from src.data_models import (
    Citizen,
    CitizenState,
    IncomeLevel,
    Policy,
    PolicyDomain,
    PopulationConfig,
    SimulationConfig,
    SimulationMode,
    ReactionMethod,
)
from src.population import generate_population, generate_initial_states
from src.simulation import (
    run_simulation,
    apply_rule_based_reaction,
    get_simulation_summary,
    POLICY_DOMAIN_RULES,
)
from src.utils import create_rng


class TestRuleBasedReaction:
    """Tests for rule-based reaction logic."""

    def test_reaction_returns_tuple(self) -> None:
        """Reaction should return three delta values."""
        config = PopulationConfig(size=10)
        rng = create_rng(42)
        population = generate_population(config, rng)
        states = generate_initial_states(population, rng)
        
        citizen = population[0]
        state = states[0]
        policy = Policy(
            title="Test Policy",
            description="A test policy",
            domain=PolicyDomain.ECONOMY,
        )
        
        result = apply_rule_based_reaction(citizen, state, policy, step=1, rng=rng)
        
        assert isinstance(result, tuple)
        assert len(result) == 3
        assert all(isinstance(v, float) for v in result)

    def test_policy_domains_have_different_effects(self) -> None:
        """Different policy domains should produce different reactions."""
        config = PopulationConfig(size=10)
        rng = create_rng(42)
        population = generate_population(config, rng)
        states = generate_initial_states(population, rng)
        
        citizen = population[0]
        state = states[0]
        
        results = {}
        for domain in PolicyDomain:
            policy = Policy(
                title="Test Policy",
                description="A test policy",
                domain=domain,
            )
            rng = create_rng(42)  # Reset RNG for fair comparison
            results[domain] = apply_rule_based_reaction(citizen, state, policy, step=1, rng=rng)
        
        # At least some domains should have different effects
        unique_results = set(results.values())
        assert len(unique_results) > 1, "All domains produced identical results"


class TestSimulationRun:
    """Tests for running complete simulations."""

    def test_simulation_returns_result(self) -> None:
        """Simulation should return a SimulationResult."""
        config = PopulationConfig(size=50)
        rng = create_rng(42)
        population = generate_population(config, rng)
        initial_states = generate_initial_states(population, rng)
        
        sim_config = SimulationConfig(steps=3)
        policy = Policy(
            title="Test Policy",
            description="A test policy",
            domain=PolicyDomain.ECONOMY,
        )
        
        result = run_simulation(
            policy=policy,
            citizens=population,
            initial_states=initial_states,
            config=sim_config,
            population_config=config,
            scenario_name="Test Scenario",
        )
        
        assert result.scenario_name == "Test Scenario"
        assert result.policy == policy
        assert result.config == sim_config
        assert len(result.citizens) == 50

    def test_simulation_produces_metrics_per_step(self) -> None:
        """Simulation should produce metrics for each step."""
        config = PopulationConfig(size=50)
        rng = create_rng(42)
        population = generate_population(config, rng)
        initial_states = generate_initial_states(population, rng)
        
        sim_config = SimulationConfig(steps=5)
        policy = Policy(
            title="Test Policy",
            description="A test policy",
            domain=PolicyDomain.EDUCATION,
        )
        
        result = run_simulation(
            policy=policy,
            citizens=population,
            initial_states=initial_states,
            config=sim_config,
            population_config=config,
            scenario_name="Test Scenario",
        )
        
        # Should have metrics for step 0 through step 5 (6 total)
        assert len(result.metrics_by_step) == 6
        
        # Check step numbers are correct
        for i, metrics in enumerate(result.metrics_by_step):
            assert metrics.step == i

    def test_simulation_states_are_immutable_per_step(self) -> None:
        """Each step should have its own list of states."""
        config = PopulationConfig(size=20)
        rng = create_rng(42)
        population = generate_population(config, rng)
        initial_states = generate_initial_states(population, rng)
        
        sim_config = SimulationConfig(steps=3)
        policy = Policy(
            title="Test Policy",
            description="A test policy",
            domain=PolicyDomain.SOCIAL,
        )
        
        result = run_simulation(
            policy=policy,
            citizens=population,
            initial_states=initial_states,
            config=sim_config,
            population_config=config,
            scenario_name="Test Scenario",
        )
        
        # Each step should have separate state lists
        assert 0 in result.states_by_step
        assert 1 in result.states_by_step
        assert 2 in result.states_by_step
        assert 3 in result.states_by_step
        
        # States at different steps should be different objects
        step0_state = result.states_by_step[0][0]
        step1_state = result.states_by_step[1][0]
        assert step0_state is not step1_state
        assert step0_state.step == 0
        assert step1_state.step == 1

    def test_simulation_values_stay_in_bounds(self) -> None:
        """Happiness and support should remain within valid ranges."""
        config = PopulationConfig(size=100)
        rng = create_rng(42)
        population = generate_population(config, rng)
        initial_states = generate_initial_states(population, rng)
        
        sim_config = SimulationConfig(steps=10)  # Run many steps
        policy = Policy(
            title="Extreme Policy",
            description="Testing bounds",
            domain=PolicyDomain.BUSINESS,
        )
        
        result = run_simulation(
            policy=policy,
            citizens=population,
            initial_states=initial_states,
            config=sim_config,
            population_config=config,
            scenario_name="Bounds Test",
        )
        
        # Check all states are within bounds
        for step, states in result.states_by_step.items():
            for state in states:
                assert 0.0 <= state.happiness <= 1.0, f"Happiness out of bounds at step {step}"
                assert -1.0 <= state.policy_support <= 1.0, f"Support out of bounds at step {step}"
                assert state.income >= 0, f"Income negative at step {step}"

    def test_simulation_is_reproducible(self) -> None:
        """Same seed should produce identical results."""
        config = PopulationConfig(size=50, random_seed=123)
        policy = Policy(
            title="Test Policy",
            description="A test policy",
            domain=PolicyDomain.ECONOMY,
        )
        sim_config = SimulationConfig(steps=5)
        
        # Run 1
        rng1 = create_rng(123)
        pop1 = generate_population(config, rng1)
        states1 = generate_initial_states(pop1, rng1)
        result1 = run_simulation(
            policy=policy,
            citizens=pop1,
            initial_states=states1,
            config=sim_config,
            population_config=config,
            scenario_name="Run 1",
            rng=create_rng(123),
        )
        
        # Run 2
        rng2 = create_rng(123)
        pop2 = generate_population(config, rng2)
        states2 = generate_initial_states(pop2, rng2)
        result2 = run_simulation(
            policy=policy,
            citizens=pop2,
            initial_states=states2,
            config=sim_config,
            population_config=config,
            scenario_name="Run 2",
            rng=create_rng(123),
        )
        
        # Compare final metrics
        final1 = result1.metrics_by_step[-1]
        final2 = result2.metrics_by_step[-1]
        
        assert abs(final1.avg_happiness - final2.avg_happiness) < 0.001
        assert abs(final1.avg_support - final2.avg_support) < 0.001


class TestSimulationSummary:
    """Tests for simulation summary generation."""

    def test_summary_has_required_fields(self) -> None:
        """Summary should contain all expected fields."""
        config = PopulationConfig(size=50)
        rng = create_rng(42)
        population = generate_population(config, rng)
        initial_states = generate_initial_states(population, rng)
        
        sim_config = SimulationConfig(steps=3)
        policy = Policy(
            title="Test Policy",
            description="A test policy",
            domain=PolicyDomain.EDUCATION,
        )
        
        result = run_simulation(
            policy=policy,
            citizens=population,
            initial_states=initial_states,
            config=sim_config,
            population_config=config,
            scenario_name="Test Scenario",
        )
        
        summary = get_simulation_summary(result)
        
        assert "scenario_name" in summary
        assert "policy_title" in summary
        assert "policy_domain" in summary
        assert "steps" in summary
        assert "initial_happiness" in summary
        assert "final_happiness" in summary
        assert "happiness_change" in summary
        assert "initial_support" in summary
        assert "final_support" in summary
        assert "support_change" in summary


class TestPolicyDomainRules:
    """Tests for policy domain rule definitions."""

    def test_all_domains_have_rules(self) -> None:
        """Every policy domain should have defined rules."""
        for domain in PolicyDomain:
            assert domain in POLICY_DOMAIN_RULES, f"Missing rules for {domain}"

    def test_rules_cover_all_income_levels(self) -> None:
        """Rules should define impacts for all income levels."""
        for domain, rules in POLICY_DOMAIN_RULES.items():
            for level in IncomeLevel:
                assert level in rules.happiness_by_income, f"Missing {level} in {domain}"
                assert level in rules.income_change_by_income, f"Missing {level} in {domain}"


class TestAIIntegration:
    """Tests for AI-enhanced simulation mode."""

    def test_simulation_works_without_llm_client(self) -> None:
        """Simulation should work perfectly without LLM client."""
        config = PopulationConfig(size=50)
        rng = create_rng(42)
        population = generate_population(config, rng)
        initial_states = generate_initial_states(population, rng)
        
        sim_config = SimulationConfig(
            steps=3,
            ai_enabled=True,  # AI enabled but no client provided
        )
        policy = Policy(
            title="Test Policy",
            description="A test policy",
            domain=PolicyDomain.ECONOMY,
        )
        
        # Should not raise, should use rule-based fallback
        result = run_simulation(
            policy=policy,
            citizens=population,
            initial_states=initial_states,
            config=sim_config,
            population_config=config,
            scenario_name="No LLM Test",
            llm_client=None,  # No LLM client
        )
        
        assert result is not None
        assert result.ai_status is not None
        assert result.ai_status.ai_enabled is True
        assert result.ai_status.ai_available is False  # No client
        assert result.ai_status.ai_successes == 0

    def test_ai_status_populated_when_disabled(self) -> None:
        """AI status should indicate AI was disabled."""
        config = PopulationConfig(size=50)
        rng = create_rng(42)
        population = generate_population(config, rng)
        initial_states = generate_initial_states(population, rng)
        
        sim_config = SimulationConfig(
            steps=3,
            ai_enabled=False,
        )
        policy = Policy(
            title="Test Policy",
            description="A test policy",
            domain=PolicyDomain.ECONOMY,
        )
        
        result = run_simulation(
            policy=policy,
            citizens=population,
            initial_states=initial_states,
            config=sim_config,
            population_config=config,
            scenario_name="AI Disabled Test",
        )
        
        assert result.ai_status is not None
        assert result.ai_status.ai_enabled is False
        assert result.ai_status.citizens_sampled == 0

    def test_ai_sample_pct_limits_sampling(self) -> None:
        """AI sample percentage config is stored correctly."""
        config = PopulationConfig(size=100)
        rng = create_rng(42)
        population = generate_population(config, rng)
        initial_states = generate_initial_states(population, rng)
        
        sim_config = SimulationConfig(
            steps=1,
            ai_enabled=True,
            ai_sample_pct=0.1,  # 10% = 10 citizens
        )
        policy = Policy(
            title="Test Policy",
            description="A test policy",
            domain=PolicyDomain.ECONOMY,
        )
        
        result = run_simulation(
            policy=policy,
            citizens=population,
            initial_states=initial_states,
            config=sim_config,
            population_config=config,
            scenario_name="Sample Limit Test",
            llm_client=None,  # No client, so AI not actually available
        )
        
        # ai_enabled in status reflects config setting
        # ai_available reflects actual availability (no client = not available)
        assert result.ai_status.ai_enabled is True  # Config setting
        assert result.ai_status.ai_available is False  # No client available
        # No citizens sampled since AI wasn't actually used
        assert result.ai_status.citizens_sampled == 0
        # Config still stores the setting
        assert result.config.ai_sample_pct == 0.1

    def test_all_rule_based_when_ai_disabled(self) -> None:
        """All reactions should be rule-based when AI is disabled."""
        config = PopulationConfig(size=50)
        rng = create_rng(42)
        population = generate_population(config, rng)
        initial_states = generate_initial_states(population, rng)
        
        sim_config = SimulationConfig(
            steps=3,
            ai_enabled=False,
        )
        policy = Policy(
            title="Test Policy",
            description="A test policy",
            domain=PolicyDomain.ECONOMY,
        )
        
        result = run_simulation(
            policy=policy,
            citizens=population,
            initial_states=initial_states,
            config=sim_config,
            population_config=config,
            scenario_name="Rule Based Test",
        )
        
        # Check method counts for each step
        for step in range(1, sim_config.steps + 1):
            counts = result.method_counts[step]
            assert counts.get(ReactionMethod.RULE_BASED, 0) == 50
            assert counts.get(ReactionMethod.LLM, 0) == 0

    def test_explanation_disabled_produces_no_diary_entries(self) -> None:
        """When explanations disabled, no diary entries should be generated."""
        config = PopulationConfig(size=50)
        rng = create_rng(42)
        population = generate_population(config, rng)
        initial_states = generate_initial_states(population, rng)
        
        sim_config = SimulationConfig(
            steps=2,
            ai_enabled=False,
            ai_explanation_enabled=False,
        )
        policy = Policy(
            title="Test Policy",
            description="A test policy",
            domain=PolicyDomain.ECONOMY,
        )
        
        result = run_simulation(
            policy=policy,
            citizens=population,
            initial_states=initial_states,
            config=sim_config,
            population_config=config,
            scenario_name="No Explanations Test",
        )
        
        # Check final states for diary entries
        final_states = result.states_by_step[sim_config.steps]
        for state in final_states:
            assert state.diary_entry is None

    def test_deterministic_sampling_is_consistent(self) -> None:
        """Same population should produce same AI sample selection."""
        config = PopulationConfig(size=100, random_seed=42)
        
        # Run 1
        rng1 = create_rng(42)
        pop1 = generate_population(config, rng1)
        states1 = generate_initial_states(pop1, rng1)
        
        sim_config = SimulationConfig(
            steps=1,
            ai_enabled=True,
            ai_sample_pct=0.1,
        )
        policy = Policy(
            title="Test",
            description="Test",
            domain=PolicyDomain.ECONOMY,
        )
        
        result1 = run_simulation(
            policy=policy,
            citizens=pop1,
            initial_states=states1,
            config=sim_config,
            population_config=config,
            scenario_name="Run 1",
            rng=create_rng(42),
        )
        
        # Run 2 - should be identical
        rng2 = create_rng(42)
        pop2 = generate_population(config, rng2)
        states2 = generate_initial_states(pop2, rng2)
        
        result2 = run_simulation(
            policy=policy,
            citizens=pop2,
            initial_states=states2,
            config=sim_config,
            population_config=config,
            scenario_name="Run 2",
            rng=create_rng(42),
        )
        
        # Same citizens should be sampled
        assert result1.ai_status.citizens_sampled == result2.ai_status.citizens_sampled
        
        # Final metrics should be identical (both rule-based fallback)
        final1 = result1.metrics_by_step[-1]
        final2 = result2.metrics_by_step[-1]
        assert abs(final1.avg_happiness - final2.avg_happiness) < 0.001
