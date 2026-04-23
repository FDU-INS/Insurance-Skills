"""Tests for generation framework.

Tests the healthsim-core generation infrastructure re-exported by membersim,
and the MemberSim-specific cohort generation.
"""

import random

import pytest
from healthsim.generation import (
    AgeDistribution,
    NormalDistribution,
    SeedManager,
    UniformDistribution,
    WeightedChoice,
)

from membersim.generation import (
    CohortConstraints,
    CohortProgress,
    MemberCohortConstraints,
    MemberCohortGenerator,
)

# ============================================================================
# WeightedChoice Tests
# ============================================================================


class TestWeightedChoice:
    """Tests for WeightedChoice."""

    def test_deterministic_with_seed(self) -> None:
        """Same rng seed should produce same sequence."""
        rng1 = random.Random(42)
        rng2 = random.Random(42)

        choice = WeightedChoice(options=[("A", 0.5), ("B", 0.5)])

        results1 = [choice.select(rng=rng1) for _ in range(100)]
        results2 = [choice.select(rng=rng2) for _ in range(100)]

        assert results1 == results2

    def test_respects_weights(self) -> None:
        """Heavily weighted option should be selected more often."""
        rng = random.Random(42)
        choice = WeightedChoice(options=[("A", 0.99), ("B", 0.01)])
        results = [choice.select(rng=rng) for _ in range(1000)]

        a_count = results.count("A")
        assert a_count > 900  # Should be ~99%

    def test_empty_choices_raises(self) -> None:
        """Empty choices should raise ValueError."""
        choice = WeightedChoice(options=[])
        with pytest.raises(ValueError):
            choice.select()

    def test_select_returns_value(self) -> None:
        """Select should return one of the values."""
        choice = WeightedChoice(options=[("X", 0.5), ("Y", 0.5)])
        result = choice.select()
        assert result in ["X", "Y"]


# ============================================================================
# UniformDistribution Tests
# ============================================================================


class TestUniformDistribution:
    """Tests for UniformDistribution."""

    def test_sample_within_bounds(self) -> None:
        """Samples should be within min/max bounds."""
        rng = random.Random(42)
        dist = UniformDistribution(min_val=10.0, max_val=20.0)
        for _ in range(100):
            value = dist.sample(rng=rng)
            assert 10.0 <= value <= 20.0

    def test_sample_int_within_bounds(self) -> None:
        """Integer samples should be within bounds."""
        rng = random.Random(42)
        dist = UniformDistribution(min_val=1.0, max_val=10.0)
        for _ in range(100):
            value = dist.sample_int(rng=rng)
            assert 1 <= value <= 10
            assert isinstance(value, int)

    def test_deterministic_with_seed(self) -> None:
        """Same seed should produce same sequence."""
        rng1 = random.Random(42)
        rng2 = random.Random(42)
        dist = UniformDistribution(min_val=0.0, max_val=100.0)

        values1 = [dist.sample(rng=rng1) for _ in range(10)]
        values2 = [dist.sample(rng=rng2) for _ in range(10)]

        assert values1 == values2


# ============================================================================
# NormalDistribution Tests
# ============================================================================


class TestNormalDistribution:
    """Tests for NormalDistribution."""

    def test_sample_respects_bounds(self) -> None:
        """Bounded samples should respect min/max."""
        rng = random.Random(42)
        dist = NormalDistribution(mean=50.0, std_dev=10.0)
        for _ in range(100):
            value = dist.sample_bounded(min_val=40.0, max_val=60.0, rng=rng)
            assert 40.0 <= value <= 60.0

    def test_unbounded_samples(self) -> None:
        """Unbounded distribution should work."""
        rng = random.Random(42)
        dist = NormalDistribution(mean=0.0, std_dev=1.0)
        values = [dist.sample(rng=rng) for _ in range(100)]
        # Should have some variation
        assert max(values) != min(values)

    def test_deterministic_with_seed(self) -> None:
        """Same seed should produce same sequence."""
        rng1 = random.Random(42)
        rng2 = random.Random(42)
        dist = NormalDistribution(mean=50.0, std_dev=10.0)

        values1 = [dist.sample(rng=rng1) for _ in range(10)]
        values2 = [dist.sample(rng=rng2) for _ in range(10)]

        assert values1 == values2


# ============================================================================
# AgeDistribution Tests
# ============================================================================


class TestAgeDistribution:
    """Tests for AgeDistribution."""

    def test_sample_within_bounds(self) -> None:
        """Ages should be within band bounds."""
        dist = AgeDistribution()  # Default adult distribution
        dist.seed(42)
        for _ in range(100):
            age = dist.sample()
            assert 18 <= age <= 90  # Default bands range

    def test_deterministic_with_seed(self) -> None:
        """Same seed should produce same ages."""
        dist1 = AgeDistribution()
        dist1.seed(42)
        dist2 = AgeDistribution()
        dist2.seed(42)

        ages1 = [dist1.sample() for _ in range(10)]
        ages2 = [dist2.sample() for _ in range(10)]

        assert ages1 == ages2

    def test_pediatric_distribution(self) -> None:
        """Pediatric distribution should produce ages 0-17."""
        dist = AgeDistribution.pediatric()
        dist.seed(42)
        for _ in range(100):
            age = dist.sample()
            assert 0 <= age <= 17


# ============================================================================
# SeedManager Tests
# ============================================================================


class TestSeedManager:
    """Tests for SeedManager."""

    def test_deterministic_random(self) -> None:
        """Same seed should produce same random values."""
        mgr1 = SeedManager(seed=42)
        mgr2 = SeedManager(seed=42)

        assert mgr1.get_random_int(1, 100) == mgr2.get_random_int(1, 100)

    def test_get_child_seed(self) -> None:
        """Child seeds should be deterministic."""
        mgr1 = SeedManager(seed=42)
        mgr2 = SeedManager(seed=42)

        child1 = mgr1.get_child_seed()
        child2 = mgr2.get_child_seed()

        assert child1 == child2

    def test_reset_restores_state(self) -> None:
        """Reset should restore to initial state."""
        mgr = SeedManager(seed=42)
        val1 = mgr.get_random_int(1, 1000)
        mgr.reset()
        val2 = mgr.get_random_int(1, 1000)

        assert val1 == val2


# ============================================================================
# CohortConstraints Tests
# ============================================================================


class TestCohortConstraints:
    """Tests for CohortConstraints."""

    def test_default_constraints_valid(self) -> None:
        """Default constraints should be valid."""
        constraints = CohortConstraints()
        errors = constraints.validate()
        assert errors == []

    def test_invalid_gender_distribution(self) -> None:
        """Invalid gender distribution should report error."""
        constraints = CohortConstraints(
            gender_distribution={"M": 0.3, "F": 0.3}  # Sums to 0.6
        )
        errors = constraints.validate()
        assert len(errors) == 1
        assert "gender" in errors[0]

    def test_invalid_age_distribution(self) -> None:
        """Invalid age distribution should report error."""
        constraints = CohortConstraints(
            age_distribution={"0-17": 0.5}  # Sums to 0.5
        )
        errors = constraints.validate()
        assert len(errors) == 1
        assert "age" in errors[0]


# ============================================================================
# CohortProgress Tests
# ============================================================================


class TestCohortProgress:
    """Tests for CohortProgress."""

    def test_percent_complete(self) -> None:
        """Percent complete should be calculated correctly."""
        progress = CohortProgress(total=100, completed=50)
        assert progress.percent_complete == 50.0

    def test_percent_complete_zero_total(self) -> None:
        """Percent complete with zero total should be 0."""
        progress = CohortProgress(total=0, completed=0)
        assert progress.percent_complete == 0

    def test_is_complete(self) -> None:
        """is_complete should check completed + failed >= total."""
        progress = CohortProgress(total=10, completed=8, failed=2)
        assert progress.is_complete

        progress2 = CohortProgress(total=10, completed=5, failed=0)
        assert not progress2.is_complete


# ============================================================================
# MemberCohortGenerator Tests
# ============================================================================


class TestMemberCohortGenerator:
    """Tests for MemberCohortGenerator."""

    def test_generates_correct_count(self) -> None:
        """Should generate requested number of members."""
        generator = MemberCohortGenerator(seed=42)
        constraints = MemberCohortConstraints(count=10)

        members = generator.generate(constraints)
        assert len(members) == 10

    def test_reproducible_generation(self) -> None:
        """Same seed should produce same cohort."""
        gen1 = MemberCohortGenerator(seed=42)
        gen2 = MemberCohortGenerator(seed=42)

        constraints = MemberCohortConstraints(count=10)

        cohort1 = gen1.generate(constraints)
        cohort2 = gen2.generate(constraints)

        # Compare member IDs to check reproducibility
        ids1 = [m.member_id for m in cohort1]
        ids2 = [m.member_id for m in cohort2]
        assert ids1 == ids2

    def test_progress_callback(self) -> None:
        """Progress callback should be called."""
        progress_reports: list[int] = []

        def track_progress(progress: CohortProgress) -> None:
            progress_reports.append(progress.completed)

        generator = MemberCohortGenerator(seed=42)
        constraints = MemberCohortConstraints(count=50)

        generator.generate(constraints, progress_callback=track_progress)

        # Should have progress reports for each member
        assert len(progress_reports) == 50
