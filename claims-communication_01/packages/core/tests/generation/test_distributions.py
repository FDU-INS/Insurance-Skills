"""Tests for statistical distributions module."""

import pytest
import random
from unittest.mock import MagicMock

from healthsim.generation.distributions import (
    WeightedChoice,
    NormalDistribution,
    UniformDistribution,
    LogNormalDistribution,
    ExplicitDistribution,
    CategoricalDistribution,
    AgeBandDistribution,
    AgeDistribution,
    ConditionalDistribution,
    create_distribution,
)


# =============================================================================
# WeightedChoice Tests
# =============================================================================

class TestWeightedChoice:
    """Tests for WeightedChoice."""

    def test_basic_selection(self):
        """Test basic weighted selection."""
        choices = WeightedChoice(options=[
            ("a", 0.5),
            ("b", 0.3),
            ("c", 0.2),
        ])
        
        result = choices.select()
        assert result in ["a", "b", "c"]

    def test_empty_options_raises(self):
        """Test that empty options raises error."""
        choices = WeightedChoice(options=[])
        
        with pytest.raises(ValueError, match="No options"):
            choices.select()

    def test_deterministic_with_seed(self):
        """Test reproducibility with seeded RNG."""
        choices = WeightedChoice(options=[
            ("a", 0.5),
            ("b", 0.5),
        ])
        
        rng1 = random.Random(42)
        rng2 = random.Random(42)
        
        result1 = choices.select(rng1)
        result2 = choices.select(rng2)
        
        assert result1 == result2

    def test_select_multiple(self):
        """Test selecting multiple options."""
        choices = WeightedChoice(options=[
            ("a", 0.5),
            ("b", 0.3),
            ("c", 0.2),
        ])
        
        results = choices.select_multiple(10)
        
        assert len(results) == 10
        assert all(r in ["a", "b", "c"] for r in results)

    def test_select_multiple_unique(self):
        """Test selecting unique options."""
        choices = WeightedChoice(options=[
            ("a", 0.5),
            ("b", 0.3),
            ("c", 0.2),
        ])
        
        results = choices.select_multiple(3, unique=True)
        
        assert len(results) == 3
        assert len(set(results)) == 3  # All unique

    def test_select_multiple_unique_exceeds_options(self):
        """Test error when requesting more unique than available."""
        choices = WeightedChoice(options=[
            ("a", 0.5),
            ("b", 0.5),
        ])
        
        with pytest.raises(ValueError, match="Cannot select"):
            choices.select_multiple(5, unique=True)

    def test_weight_distribution(self):
        """Test that weights are approximately respected."""
        choices = WeightedChoice(options=[
            ("heavy", 0.9),
            ("light", 0.1),
        ])
        
        rng = random.Random(42)
        results = [choices.select(rng) for _ in range(1000)]
        
        heavy_count = results.count("heavy")
        # Should be roughly 900 +/- 50
        assert 800 < heavy_count < 980


# =============================================================================
# NormalDistribution Tests
# =============================================================================

class TestNormalDistribution:
    """Tests for NormalDistribution."""

    def test_basic_sample(self):
        """Test basic sampling."""
        dist = NormalDistribution(mean=100, std_dev=10)
        
        value = dist.sample()
        # Should typically be within 3 std devs
        assert 70 < value < 130

    def test_mean_approximate(self):
        """Test that mean is approximately correct."""
        dist = NormalDistribution(mean=100, std_dev=10)
        rng = random.Random(42)
        
        samples = [dist.sample(rng) for _ in range(1000)]
        sample_mean = sum(samples) / len(samples)
        
        assert 95 < sample_mean < 105

    def test_sample_int(self):
        """Test integer sampling."""
        dist = NormalDistribution(mean=50, std_dev=5)
        
        value = dist.sample_int()
        
        assert isinstance(value, int)

    def test_sample_bounded(self):
        """Test bounded sampling."""
        dist = NormalDistribution(mean=50, std_dev=20)
        rng = random.Random(42)
        
        for _ in range(100):
            value = dist.sample_bounded(min_val=30, max_val=70, rng=rng)
            assert 30 <= value <= 70

    def test_sample_bounded_min_only(self):
        """Test bounded with min only."""
        dist = NormalDistribution(mean=50, std_dev=20)
        rng = random.Random(42)
        
        for _ in range(50):
            value = dist.sample_bounded(min_val=0, rng=rng)
            assert value >= 0

    def test_sample_bounded_max_only(self):
        """Test bounded with max only."""
        dist = NormalDistribution(mean=50, std_dev=20)
        rng = random.Random(42)
        
        for _ in range(50):
            value = dist.sample_bounded(max_val=100, rng=rng)
            assert value <= 100

    def test_reproducibility(self):
        """Test reproducibility with same seed."""
        dist = NormalDistribution(mean=100, std_dev=15)
        
        rng1 = random.Random(123)
        rng2 = random.Random(123)
        
        assert dist.sample(rng1) == dist.sample(rng2)


# =============================================================================
# UniformDistribution Tests
# =============================================================================

class TestUniformDistribution:
    """Tests for UniformDistribution."""

    def test_basic_sample(self):
        """Test basic sampling."""
        dist = UniformDistribution(min_val=0, max_val=100)
        
        value = dist.sample()
        
        assert 0 <= value <= 100

    def test_sample_int(self):
        """Test integer sampling."""
        dist = UniformDistribution(min_val=1, max_val=10)
        
        value = dist.sample_int()
        
        assert isinstance(value, int)
        assert 1 <= value <= 10

    def test_uniform_distribution(self):
        """Test that distribution is roughly uniform."""
        dist = UniformDistribution(min_val=0, max_val=10)
        rng = random.Random(42)
        
        samples = [dist.sample(rng) for _ in range(1000)]
        
        # Check that values are spread across the range
        below_5 = sum(1 for s in samples if s < 5)
        # Should be roughly 500 +/- 50
        assert 400 < below_5 < 600

    def test_reproducibility(self):
        """Test reproducibility."""
        dist = UniformDistribution(min_val=0, max_val=1)
        
        rng1 = random.Random(42)
        rng2 = random.Random(42)
        
        assert dist.sample(rng1) == dist.sample(rng2)


# =============================================================================
# LogNormalDistribution Tests
# =============================================================================

class TestLogNormalDistribution:
    """Tests for LogNormalDistribution."""

    def test_basic_sample(self):
        """Test basic sampling."""
        dist = LogNormalDistribution(mean=1000, std_dev=500)
        
        value = dist.sample()
        
        assert value >= 0  # Log-normal is always positive

    def test_min_val_enforced(self):
        """Test minimum value is enforced."""
        dist = LogNormalDistribution(mean=100, std_dev=200, min_val=10)
        rng = random.Random(42)
        
        for _ in range(50):
            value = dist.sample(rng)
            assert value >= 10

    def test_sample_bounded(self):
        """Test bounded sampling."""
        dist = LogNormalDistribution(mean=100, std_dev=50)
        rng = random.Random(42)
        
        for _ in range(50):
            value = dist.sample_bounded(max_val=500, rng=rng)
            assert value <= 500

    def test_right_skew(self):
        """Test that distribution is right-skewed (median < mean)."""
        dist = LogNormalDistribution(mean=100, std_dev=100)
        rng = random.Random(42)
        
        samples = sorted([dist.sample(rng) for _ in range(1000)])
        median = samples[500]
        mean = sum(samples) / len(samples)
        
        # Log-normal should have median < mean
        assert median < mean

    def test_zero_mean_returns_min(self):
        """Test that zero/negative mean returns min_val."""
        dist = LogNormalDistribution(mean=0, std_dev=10, min_val=5)
        
        value = dist.sample()
        
        assert value == 5


# =============================================================================
# ExplicitDistribution Tests
# =============================================================================

class TestExplicitDistribution:
    """Tests for ExplicitDistribution."""

    def test_basic_sample(self):
        """Test basic sampling."""
        dist = ExplicitDistribution(values=[
            ("TX", 0.5),
            ("CA", 0.3),
            ("NY", 0.2),
        ])
        
        value = dist.sample()
        
        assert value in ["TX", "CA", "NY"]

    def test_empty_values_raises(self):
        """Test that empty values raises error."""
        dist = ExplicitDistribution(values=[])
        
        with pytest.raises(ValueError, match="No values"):
            dist.sample()

    def test_sample_multiple(self):
        """Test sampling multiple values."""
        dist = ExplicitDistribution(values=[
            ("a", 0.5),
            ("b", 0.5),
        ])
        
        results = dist.sample_multiple(5)
        
        assert len(results) == 5

    def test_sample_multiple_unique(self):
        """Test sampling unique values."""
        dist = ExplicitDistribution(values=[
            ("a", 0.33),
            ("b", 0.33),
            ("c", 0.34),
        ])
        
        results = dist.sample_multiple(3, unique=True)
        
        assert len(results) == 3
        assert len(set(results)) == 3

    def test_sample_multiple_unique_exceeds(self):
        """Test error when requesting too many unique."""
        dist = ExplicitDistribution(values=[
            ("a", 1.0),
        ])
        
        with pytest.raises(ValueError, match="Cannot select"):
            dist.sample_multiple(2, unique=True)

    def test_weight_distribution(self):
        """Test weights are respected."""
        dist = ExplicitDistribution(values=[
            ("heavy", 0.9),
            ("light", 0.1),
        ])
        rng = random.Random(42)
        
        results = [dist.sample(rng) for _ in range(1000)]
        heavy_count = results.count("heavy")
        
        assert 800 < heavy_count < 980


# =============================================================================
# CategoricalDistribution Tests
# =============================================================================

class TestCategoricalDistribution:
    """Tests for CategoricalDistribution."""

    def test_basic_sample(self):
        """Test basic sampling."""
        dist = CategoricalDistribution(weights={"M": 0.48, "F": 0.52})
        
        value = dist.sample()
        
        assert value in ["M", "F"]

    def test_weights_must_sum_to_one(self):
        """Test that weights must sum to approximately 1.0."""
        with pytest.raises(ValueError, match="sum to 1.0"):
            CategoricalDistribution(weights={"a": 0.5, "b": 0.3})

    def test_weights_tolerance(self):
        """Test weights sum tolerance."""
        # These should be acceptable (within 0.99-1.01)
        dist = CategoricalDistribution(weights={"a": 0.5, "b": 0.505})
        assert dist is not None

    def test_empty_weights_raises(self):
        """Test that empty weights raises error at creation time."""
        with pytest.raises(ValueError, match="sum to 1.0"):
            CategoricalDistribution(weights={})

    def test_sample_multiple(self):
        """Test sampling multiple values."""
        dist = CategoricalDistribution(weights={"a": 0.5, "b": 0.5})
        
        results = dist.sample_multiple(10)
        
        assert len(results) == 10
        assert all(r in ["a", "b"] for r in results)

    def test_reproducibility(self):
        """Test reproducibility."""
        dist = CategoricalDistribution(weights={"a": 0.5, "b": 0.5})
        
        rng1 = random.Random(42)
        rng2 = random.Random(42)
        
        assert dist.sample(rng1) == dist.sample(rng2)


# =============================================================================
# AgeBandDistribution Tests
# =============================================================================

class TestAgeBandDistribution:
    """Tests for AgeBandDistribution."""

    def test_basic_sample(self):
        """Test basic sampling."""
        dist = AgeBandDistribution(bands={
            "0-17": 0.20,
            "18-64": 0.60,
            "65+": 0.20,
        })
        
        age = dist.sample()
        
        assert 0 <= age <= 95

    def test_sample_within_band(self):
        """Test that samples fall within selected bands."""
        dist = AgeBandDistribution(bands={
            "18-34": 0.50,
            "35-54": 0.50,
        })
        rng = random.Random(42)
        
        ages = [dist.sample(rng) for _ in range(100)]
        
        assert all(18 <= age <= 54 for age in ages)

    def test_parse_plus_band(self):
        """Test parsing of '65+' style bands."""
        dist = AgeBandDistribution(bands={"65+": 1.0})
        rng = random.Random(42)
        
        ages = [dist.sample(rng) for _ in range(50)]
        
        assert all(65 <= age <= 95 for age in ages)

    def test_sample_multiple(self):
        """Test sampling multiple ages."""
        dist = AgeBandDistribution(bands={
            "18-65": 1.0,
        })
        
        ages = dist.sample_multiple(10)
        
        assert len(ages) == 10
        assert all(isinstance(a, int) for a in ages)

    def test_empty_bands_raises(self):
        """Test that empty bands raises error."""
        dist = AgeBandDistribution(bands={})
        
        with pytest.raises(ValueError, match="No age bands"):
            dist.sample()

    def test_single_age_band(self):
        """Test single-value age band."""
        dist = AgeBandDistribution(bands={"30": 1.0})
        
        age = dist.sample()
        
        assert age == 30


# =============================================================================
# AgeDistribution Tests (Legacy class)
# =============================================================================

class TestAgeDistribution:
    """Tests for AgeDistribution class."""

    def test_default_distribution(self):
        """Test default adult distribution."""
        dist = AgeDistribution()
        
        age = dist.sample()
        
        assert 18 <= age <= 90

    def test_custom_bands(self):
        """Test with custom bands."""
        dist = AgeDistribution(bands=[
            (0, 10, 0.5),
            (11, 20, 0.5),
        ])
        
        age = dist.sample()
        
        assert 0 <= age <= 20

    def test_seed(self):
        """Test seeding for reproducibility."""
        dist1 = AgeDistribution()
        dist1.seed(42)
        
        dist2 = AgeDistribution()
        dist2.seed(42)
        
        assert dist1.sample() == dist2.sample()

    def test_sample_many(self):
        """Test sampling many ages."""
        dist = AgeDistribution()
        
        ages = dist.sample_many(10)
        
        assert len(ages) == 10
        assert all(18 <= a <= 90 for a in ages)

    def test_pediatric_factory(self):
        """Test pediatric distribution factory."""
        dist = AgeDistribution.pediatric()
        
        ages = dist.sample_many(50)
        
        assert all(0 <= a <= 17 for a in ages)

    def test_adult_factory(self):
        """Test adult distribution factory."""
        dist = AgeDistribution.adult()
        
        ages = dist.sample_many(50)
        
        assert all(18 <= a <= 90 for a in ages)

    def test_senior_factory(self):
        """Test senior distribution factory."""
        dist = AgeDistribution.senior()
        
        ages = dist.sample_many(50)
        
        assert all(65 <= a <= 95 for a in ages)


# =============================================================================
# ConditionalDistribution Tests
# =============================================================================

class TestConditionalDistribution:
    """Tests for ConditionalDistribution."""

    def test_basic_conditional(self):
        """Test basic conditional selection."""
        dist = ConditionalDistribution(rules=[
            {
                "condition": "severity == 'mild'",
                "distribution": {"type": "normal", "mean": 6.0, "std_dev": 0.3}
            },
            {
                "condition": "severity == 'severe'",
                "distribution": {"type": "normal", "mean": 9.0, "std_dev": 0.5}
            },
        ])
        
        mild_value = dist.sample({"severity": "mild"})
        severe_value = dist.sample({"severity": "severe"})
        
        # Mild should be around 6, severe around 9
        assert 5 < mild_value < 7
        assert 7 < severe_value < 11

    def test_default_distribution(self):
        """Test default when no condition matches."""
        dist = ConditionalDistribution(
            rules=[
                {
                    "condition": "x == 'a'",
                    "distribution": {"type": "uniform", "min": 0, "max": 10}
                }
            ],
            default={"type": "uniform", "min": 100, "max": 200}
        )
        
        # No match - should use default
        value = dist.sample({"x": "b"})
        
        assert 100 <= value <= 200

    def test_no_match_no_default_raises(self):
        """Test error when no match and no default."""
        dist = ConditionalDistribution(rules=[
            {
                "condition": "x == 'never'",
                "distribution": {"type": "uniform", "min": 0, "max": 1}
            }
        ])
        
        with pytest.raises(ValueError, match="No condition matched"):
            dist.sample({"x": "something"})

    def test_numeric_condition(self):
        """Test numeric conditions."""
        dist = ConditionalDistribution(rules=[
            {
                "condition": "age >= 65",
                "distribution": {"type": "categorical", "weights": {"senior": 1.0}}
            },
            {
                "condition": "age < 65",
                "distribution": {"type": "categorical", "weights": {"adult": 1.0}}
            },
        ])
        
        senior = dist.sample({"age": 70})
        adult = dist.sample({"age": 40})
        
        assert senior == "senior"
        assert adult == "adult"


# =============================================================================
# create_distribution Factory Tests
# =============================================================================

class TestCreateDistribution:
    """Tests for create_distribution factory function."""

    def test_create_categorical(self):
        """Test creating categorical distribution."""
        spec = {"type": "categorical", "weights": {"a": 0.5, "b": 0.5}}
        
        dist = create_distribution(spec)
        
        assert isinstance(dist, CategoricalDistribution)
        assert dist.sample() in ["a", "b"]

    def test_create_normal(self):
        """Test creating normal distribution."""
        spec = {"type": "normal", "mean": 100, "std_dev": 10}
        
        dist = create_distribution(spec)
        
        assert isinstance(dist, NormalDistribution)
        assert 70 < dist.sample() < 130

    def test_create_lognormal(self):
        """Test creating log-normal distribution."""
        spec = {"type": "log_normal", "mean": 100, "std_dev": 50}
        
        dist = create_distribution(spec)
        
        assert isinstance(dist, LogNormalDistribution)
        assert dist.sample() > 0

    def test_create_lognormal_alternate_name(self):
        """Test creating log-normal with alternate name."""
        spec = {"type": "lognormal", "mean": 100, "std_dev": 50}
        
        dist = create_distribution(spec)
        
        assert isinstance(dist, LogNormalDistribution)

    def test_create_uniform(self):
        """Test creating uniform distribution."""
        spec = {"type": "uniform", "min": 0, "max": 100}
        
        dist = create_distribution(spec)
        
        assert isinstance(dist, UniformDistribution)
        assert 0 <= dist.sample() <= 100

    def test_create_age_bands(self):
        """Test creating age band distribution."""
        spec = {
            "type": "age_bands",
            "bands": {"0-17": 0.20, "18-64": 0.60, "65+": 0.20}
        }
        
        dist = create_distribution(spec)
        
        assert isinstance(dist, AgeBandDistribution)
        assert 0 <= dist.sample() <= 95

    def test_create_explicit_list_format(self):
        """Test creating explicit distribution from list format."""
        spec = {
            "type": "explicit",
            "values": [("a", 0.5), ("b", 0.5)]
        }
        
        dist = create_distribution(spec)
        
        assert isinstance(dist, ExplicitDistribution)

    def test_create_explicit_dict_format(self):
        """Test creating explicit distribution from dict format."""
        spec = {
            "type": "explicit",
            "values": {"a": 0.5, "b": 0.5}
        }
        
        dist = create_distribution(spec)
        
        assert isinstance(dist, ExplicitDistribution)
        assert dist.sample() in ["a", "b"]

    def test_create_explicit_structured_format(self):
        """Test creating explicit from structured format."""
        spec = {
            "type": "explicit",
            "values": [
                {"value": "x", "weight": 0.5},
                {"value": "y", "weight": 0.5}
            ]
        }
        
        dist = create_distribution(spec)
        
        assert isinstance(dist, ExplicitDistribution)
        assert dist.sample() in ["x", "y"]

    def test_unknown_type_raises(self):
        """Test that unknown type raises error."""
        spec = {"type": "unknown_distribution"}
        
        with pytest.raises(ValueError, match="Unknown distribution type"):
            create_distribution(spec)

    def test_create_with_defaults(self):
        """Test that defaults are applied."""
        # Normal with just type - should use defaults
        spec = {"type": "normal"}
        
        dist = create_distribution(spec)
        
        assert isinstance(dist, NormalDistribution)
        assert dist.mean == 0
        assert dist.std_dev == 1
