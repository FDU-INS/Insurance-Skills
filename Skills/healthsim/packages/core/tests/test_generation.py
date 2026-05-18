"""Tests for healthsim.generation module."""

import random
from dataclasses import dataclass

import pytest

from healthsim.generation import (
    AgeDistribution,
    BaseGenerator,
    CohortConstraints,
    CohortGenerator,
    CohortProgress,
    NormalDistribution,
    PersonGenerator,
    SeedManager,
    UniformDistribution,
    WeightedChoice,
)
from healthsim.person import Gender


class TestSeedManager:
    """Tests for SeedManager."""

    def test_creation(self) -> None:
        """Test creating a seed manager."""
        manager = SeedManager(seed=42)
        assert manager.seed == 42

    def test_reproducibility(self) -> None:
        """Test that same seed produces same results."""
        manager1 = SeedManager(seed=42)
        manager2 = SeedManager(seed=42)

        vals1 = [manager1.get_random_int(1, 100) for _ in range(5)]
        vals2 = [manager2.get_random_int(1, 100) for _ in range(5)]

        assert vals1 == vals2

    def test_different_seeds(self) -> None:
        """Test that different seeds produce different results."""
        manager1 = SeedManager(seed=42)
        manager2 = SeedManager(seed=123)

        vals1 = [manager1.get_random_int(1, 100) for _ in range(5)]
        vals2 = [manager2.get_random_int(1, 100) for _ in range(5)]

        assert vals1 != vals2

    def test_reset(self) -> None:
        """Test resetting the seed manager."""
        manager = SeedManager(seed=42)

        first_run = [manager.get_random_int(1, 100) for _ in range(5)]

        manager.reset()

        second_run = [manager.get_random_int(1, 100) for _ in range(5)]

        assert first_run == second_run

    def test_random_choice(self) -> None:
        """Test random choice."""
        manager = SeedManager(seed=42)
        options = ["a", "b", "c", "d"]

        choice = manager.get_random_choice(options)
        assert choice in options

    def test_random_sample(self) -> None:
        """Test random sample."""
        manager = SeedManager(seed=42)
        options = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        sample = manager.get_random_sample(options, 3)
        assert len(sample) == 3
        assert all(s in options for s in sample)

    def test_random_bool(self) -> None:
        """Test random boolean."""
        manager = SeedManager(seed=42)

        # With probability 1.0, should always be True
        assert manager.get_random_bool(1.0) is True

        # With probability 0.0, should always be False
        manager.reset()
        assert manager.get_random_bool(0.0) is False

    def test_child_seed(self) -> None:
        """Test getting deterministic child seed."""
        manager = SeedManager(seed=42)

        seed1 = manager.get_child_seed()
        manager.reset()
        seed2 = manager.get_child_seed()

        assert seed1 == seed2


class TestWeightedChoice:
    """Tests for WeightedChoice."""

    def test_creation(self) -> None:
        """Test creating weighted choice."""
        wc = WeightedChoice(
            options=[
                ("common", 0.7),
                ("rare", 0.3),
            ]
        )

        assert len(wc.options) == 2

    def test_select(self) -> None:
        """Test selection."""
        wc = WeightedChoice(
            options=[
                ("a", 0.5),
                ("b", 0.5),
            ]
        )

        rng = random.Random(42)
        choice = wc.select(rng)
        assert choice in ["a", "b"]

    def test_weighted_distribution(self) -> None:
        """Test that weights affect distribution."""
        wc = WeightedChoice(
            options=[
                ("common", 0.9),
                ("rare", 0.1),
            ]
        )

        rng = random.Random(42)
        results = [wc.select(rng) for _ in range(1000)]

        common_count = results.count("common")
        assert common_count > 800  # Should be ~90%

    def test_empty_options_raises(self) -> None:
        """Test that empty options raises error."""
        wc = WeightedChoice(options=[])

        with pytest.raises(ValueError, match="No options"):
            wc.select()

    def test_select_multiple(self) -> None:
        """Test selecting multiple items."""
        wc = WeightedChoice(
            options=[
                ("a", 1),
                ("b", 1),
                ("c", 1),
            ]
        )

        rng = random.Random(42)
        choices = wc.select_multiple(5, rng)

        assert len(choices) == 5
        assert all(c in ["a", "b", "c"] for c in choices)

    def test_select_multiple_unique(self) -> None:
        """Test selecting unique items."""
        wc = WeightedChoice(
            options=[
                ("a", 1),
                ("b", 1),
                ("c", 1),
            ]
        )

        rng = random.Random(42)
        choices = wc.select_multiple(3, rng, unique=True)

        assert len(choices) == 3
        assert len(set(choices)) == 3  # All unique


class TestNormalDistribution:
    """Tests for NormalDistribution."""

    def test_creation(self) -> None:
        """Test creating normal distribution."""
        dist = NormalDistribution(mean=100, std_dev=15)
        assert dist.mean == 100
        assert dist.std_dev == 15

    def test_sample(self) -> None:
        """Test sampling from distribution."""
        dist = NormalDistribution(mean=100, std_dev=15)
        rng = random.Random(42)

        # Sample many times and check mean is close
        samples = [dist.sample(rng) for _ in range(1000)]
        avg = sum(samples) / len(samples)

        assert 95 < avg < 105  # Should be close to 100

    def test_sample_int(self) -> None:
        """Test sampling integers."""
        dist = NormalDistribution(mean=100, std_dev=15)
        rng = random.Random(42)

        value = dist.sample_int(rng)
        assert isinstance(value, int)

    def test_sample_bounded(self) -> None:
        """Test bounded sampling."""
        dist = NormalDistribution(mean=100, std_dev=15)
        rng = random.Random(42)

        value = dist.sample_bounded(min_val=80, max_val=120, rng=rng)
        assert 80 <= value <= 120


class TestUniformDistribution:
    """Tests for UniformDistribution."""

    def test_creation(self) -> None:
        """Test creating uniform distribution."""
        dist = UniformDistribution(min_val=0, max_val=100)
        assert dist.min_val == 0
        assert dist.max_val == 100

    def test_sample(self) -> None:
        """Test sampling."""
        dist = UniformDistribution(min_val=0, max_val=100)
        rng = random.Random(42)

        for _ in range(100):
            value = dist.sample(rng)
            assert 0 <= value <= 100

    def test_sample_int(self) -> None:
        """Test integer sampling."""
        dist = UniformDistribution(min_val=1, max_val=6)
        rng = random.Random(42)

        for _ in range(100):
            value = dist.sample_int(rng)
            assert 1 <= value <= 6
            assert isinstance(value, int)


class TestBaseGenerator:
    """Tests for BaseGenerator."""

    def test_creation(self) -> None:
        """Test creating a generator."""
        gen = BaseGenerator(seed=42)
        assert gen.seed_manager.seed == 42

    def test_reproducibility(self) -> None:
        """Test that same seed produces same random values."""
        gen1 = BaseGenerator(seed=42)
        gen2 = BaseGenerator(seed=42)

        # Random values should be the same with same seed
        vals1 = [gen1.random_int(1, 100) for _ in range(5)]
        vals2 = [gen2.random_int(1, 100) for _ in range(5)]
        assert vals1 == vals2

    def test_generate_id(self) -> None:
        """Test ID generation."""
        gen = BaseGenerator()

        id1 = gen.generate_id("ITEM")
        id2 = gen.generate_id("ITEM")

        assert id1.startswith("ITEM-")
        assert id2.startswith("ITEM-")
        assert id1 != id2  # Should be unique

    def test_generate_id_no_prefix(self) -> None:
        """Test ID generation without prefix."""
        gen = BaseGenerator()
        id = gen.generate_id()
        assert "-" not in id  # No prefix dash

    def test_random_choice(self) -> None:
        """Test random choice."""
        gen = BaseGenerator(seed=42)
        options = [1, 2, 3, 4, 5]

        choice = gen.random_choice(options)
        assert choice in options

    def test_random_int(self) -> None:
        """Test random integer."""
        gen = BaseGenerator(seed=42)

        for _ in range(100):
            val = gen.random_int(1, 10)
            assert 1 <= val <= 10

    def test_random_float(self) -> None:
        """Test random float."""
        gen = BaseGenerator(seed=42)

        for _ in range(100):
            val = gen.random_float(0.0, 1.0)
            assert 0.0 <= val <= 1.0

    def test_weighted_choice(self) -> None:
        """Test weighted choice."""
        gen = BaseGenerator(seed=42)
        options = [("heavy", 0.9), ("light", 0.1)]

        results = [gen.weighted_choice(options) for _ in range(100)]
        heavy_count = results.count("heavy")

        assert heavy_count > 70  # Should be ~90%


class TestPersonGenerator:
    """Tests for PersonGenerator."""

    def test_creation(self) -> None:
        """Test creating a person generator."""
        gen = PersonGenerator(seed=42)
        assert gen.seed_manager.seed == 42

    def test_generate_person(self) -> None:
        """Test generating a person."""
        gen = PersonGenerator(seed=42)
        person = gen.generate_person()

        assert person.id.startswith("PERSON-")
        assert person.name.given_name is not None
        assert person.name.family_name is not None
        assert person.gender in [Gender.MALE, Gender.FEMALE]
        assert person.birth_date is not None

    def test_generate_person_with_age_range(self) -> None:
        """Test generating person with age constraints."""
        gen = PersonGenerator(seed=42)
        person = gen.generate_person(age_range=(25, 35))

        assert 25 <= person.age <= 35

    def test_generate_person_with_gender(self) -> None:
        """Test generating person with specific gender."""
        gen = PersonGenerator(seed=42)
        person = gen.generate_person(gender=Gender.FEMALE)

        assert person.gender == Gender.FEMALE

    def test_generate_person_with_address(self) -> None:
        """Test generating person with address."""
        gen = PersonGenerator(seed=42)
        person = gen.generate_person(include_address=True)

        assert person.address is not None
        assert person.address.city is not None

    def test_generate_person_without_address(self) -> None:
        """Test generating person without address."""
        gen = PersonGenerator(seed=42)
        person = gen.generate_person(include_address=False)

        assert person.address is None

    def test_generate_name(self) -> None:
        """Test generating just a name."""
        gen = PersonGenerator(seed=42)
        name = gen.generate_name(Gender.MALE)

        assert name.given_name is not None
        assert name.family_name is not None

    def test_generate_address(self) -> None:
        """Test generating just an address."""
        gen = PersonGenerator(seed=42)
        address = gen.generate_address()

        assert address.street_address is not None
        assert address.city is not None
        assert address.state is not None
        assert address.postal_code is not None
        assert address.country == "US"

    def test_generate_contact(self) -> None:
        """Test generating contact info."""
        gen = PersonGenerator(seed=42)
        contact = gen.generate_contact()

        assert contact.phone is not None
        assert contact.email is not None

    def test_reproducibility(self) -> None:
        """Test that same seed produces same person."""
        gen1 = PersonGenerator(seed=42)
        gen2 = PersonGenerator(seed=42)

        person1 = gen1.generate_person()
        person2 = gen2.generate_person()

        assert person1.name.given_name == person2.name.given_name
        assert person1.name.family_name == person2.name.family_name
        assert person1.gender == person2.gender
        assert person1.birth_date == person2.birth_date


class TestAgeDistribution:
    """Tests for AgeDistribution."""

    def test_creation_default(self) -> None:
        """Test creating with default bands."""
        dist = AgeDistribution()
        assert len(dist.bands) == 5

    def test_creation_custom_bands(self) -> None:
        """Test creating with custom bands."""
        bands = [(18, 30, 0.5), (31, 50, 0.5)]
        dist = AgeDistribution(bands=bands)
        assert len(dist.bands) == 2

    def test_sample(self) -> None:
        """Test sampling an age."""
        dist = AgeDistribution()
        dist.seed(42)

        age = dist.sample()
        assert 18 <= age <= 90

    def test_sample_many(self) -> None:
        """Test sampling multiple ages."""
        dist = AgeDistribution()
        dist.seed(42)

        ages = dist.sample_many(100)
        assert len(ages) == 100
        assert all(18 <= age <= 90 for age in ages)

    def test_pediatric(self) -> None:
        """Test pediatric age distribution."""
        dist = AgeDistribution.pediatric()
        dist.seed(42)

        ages = dist.sample_many(100)
        assert all(0 <= age <= 17 for age in ages)

    def test_adult(self) -> None:
        """Test adult age distribution."""
        dist = AgeDistribution.adult()
        dist.seed(42)

        ages = dist.sample_many(100)
        assert all(18 <= age <= 90 for age in ages)

    def test_senior(self) -> None:
        """Test senior age distribution."""
        dist = AgeDistribution.senior()
        dist.seed(42)

        ages = dist.sample_many(100)
        assert all(65 <= age <= 95 for age in ages)

    def test_reproducibility(self) -> None:
        """Test that same seed produces same ages."""
        dist1 = AgeDistribution()
        dist1.seed(42)

        dist2 = AgeDistribution()
        dist2.seed(42)

        ages1 = dist1.sample_many(10)
        ages2 = dist2.sample_many(10)

        assert ages1 == ages2


class TestCohortConstraints:
    """Tests for CohortConstraints."""

    def test_creation_defaults(self) -> None:
        """Test creating with defaults."""
        constraints = CohortConstraints()
        assert constraints.count == 100
        assert constraints.min_age is None
        assert constraints.max_age is None

    def test_creation_with_values(self) -> None:
        """Test creating with specific values."""
        constraints = CohortConstraints(
            count=50,
            min_age=18,
            max_age=65,
            gender_distribution={"M": 50.0, "F": 50.0},
        )

        assert constraints.count == 50
        assert constraints.min_age == 18
        assert constraints.max_age == 65
        assert constraints.gender_distribution == {"M": 50.0, "F": 50.0}

    def test_to_dict(self) -> None:
        """Test converting to dictionary."""
        constraints = CohortConstraints(
            count=25,
            min_age=30,
            max_age=40,
        )

        d = constraints.to_dict()

        assert d["count"] == 25
        assert d["min_age"] == 30
        assert d["max_age"] == 40

    def test_custom_constraints(self) -> None:
        """Test custom constraints field."""
        constraints = CohortConstraints(custom={"include_veterans": True, "region": "midwest"})

        assert constraints.custom["include_veterans"] is True
        assert constraints.custom["region"] == "midwest"


class TestCohortProgress:
    """Tests for CohortProgress."""

    def test_creation(self) -> None:
        """Test creating progress tracker."""
        progress = CohortProgress(total=100)
        assert progress.total == 100
        assert progress.completed == 0
        assert progress.failed == 0

    def test_percent_complete(self) -> None:
        """Test percentage calculation."""
        progress = CohortProgress(total=100, completed=25)
        assert progress.percent_complete == 25.0

    def test_percent_complete_empty(self) -> None:
        """Test percentage with zero total."""
        progress = CohortProgress(total=0)
        assert progress.percent_complete == 0.0

    def test_is_complete(self) -> None:
        """Test completion check."""
        progress = CohortProgress(total=10)
        assert progress.is_complete is False

        progress.completed = 10
        assert progress.is_complete is True

    def test_is_complete_with_failures(self) -> None:
        """Test completion check includes failures."""
        progress = CohortProgress(total=10, completed=7, failed=3)
        assert progress.is_complete is True


class TestCohortGenerator:
    """Tests for CohortGenerator."""

    def test_creation(self) -> None:
        """Test creating a generator."""
        gen = CohortGenerator(seed=42)
        assert gen.seed_manager.seed == 42

    def test_generate_one_not_implemented(self) -> None:
        """Test that base class raises NotImplementedError."""
        gen = CohortGenerator()
        constraints = CohortConstraints()

        with pytest.raises(NotImplementedError):
            gen.generate_one(0, constraints)

    def test_progress_tracking(self) -> None:
        """Test progress tracking during generation."""

        # Create a simple concrete generator
        @dataclass
        class SimpleItem:
            index: int

        class SimpleCohortGenerator(CohortGenerator[SimpleItem]):
            def generate_one(self, index: int, constraints: CohortConstraints) -> SimpleItem:
                return SimpleItem(index=index)

        gen = SimpleCohortGenerator(seed=42)
        constraints = CohortConstraints(count=5)

        results = gen.generate(constraints)

        assert len(results) == 5
        assert gen.progress.completed == 5
        assert gen.progress.is_complete is True

    def test_generate_iter(self) -> None:
        """Test iterator-based generation."""

        @dataclass
        class SimpleItem:
            index: int

        class SimpleCohortGenerator(CohortGenerator[SimpleItem]):
            def generate_one(self, index: int, constraints: CohortConstraints) -> SimpleItem:
                return SimpleItem(index=index)

        gen = SimpleCohortGenerator(seed=42)
        constraints = CohortConstraints(count=3)

        items = list(gen.generate_iter(constraints))

        assert len(items) == 3
        assert items[0].index == 0
        assert items[1].index == 1
        assert items[2].index == 2

    def test_progress_callback(self) -> None:
        """Test progress callback is called."""

        @dataclass
        class SimpleItem:
            index: int

        class SimpleCohortGenerator(CohortGenerator[SimpleItem]):
            def generate_one(self, index: int, constraints: CohortConstraints) -> SimpleItem:
                return SimpleItem(index=index)

        gen = SimpleCohortGenerator(seed=42)
        constraints = CohortConstraints(count=3)

        callbacks_received = []

        def callback(progress: CohortProgress) -> None:
            callbacks_received.append(progress.completed)

        gen.generate(constraints, progress_callback=callback)

        assert len(callbacks_received) == 3
        assert callbacks_received == [1, 2, 3]

    def test_reset(self) -> None:
        """Test resetting the generator."""

        @dataclass
        class SimpleItem:
            value: int

        class SimpleCohortGenerator(CohortGenerator[SimpleItem]):
            def generate_one(self, index: int, constraints: CohortConstraints) -> SimpleItem:
                return SimpleItem(value=self.seed_manager.get_random_int(1, 1000))

        gen = SimpleCohortGenerator(seed=42)
        constraints = CohortConstraints(count=3)

        results1 = gen.generate(constraints)
        gen.reset()
        results2 = gen.generate(constraints)

        # After reset, should get same values
        assert [r.value for r in results1] == [r.value for r in results2]



# ============================================================================
# Tests for new distribution classes
# ============================================================================

from healthsim.generation.distributions import (
    AgeBandDistribution,
    CategoricalDistribution,
    ConditionalDistribution,
    ExplicitDistribution,
    LogNormalDistribution,
    create_distribution,
)


class TestLogNormalDistribution:
    """Tests for LogNormalDistribution."""

    def test_creation(self) -> None:
        """Test creating log-normal distribution."""
        dist = LogNormalDistribution(mean=5000, std_dev=8000)
        assert dist.mean == 5000
        assert dist.std_dev == 8000

    def test_sample_positive(self) -> None:
        """Test that samples are always positive."""
        dist = LogNormalDistribution(mean=5000, std_dev=8000)
        rng = random.Random(42)

        for _ in range(100):
            value = dist.sample(rng)
            assert value >= 0

    def test_sample_bounded(self) -> None:
        """Test bounded sampling."""
        dist = LogNormalDistribution(mean=100, std_dev=50)
        rng = random.Random(42)

        value = dist.sample_bounded(max_val=500, rng=rng)
        assert value <= 500

    def test_right_skewed(self) -> None:
        """Test that distribution is right-skewed (median < mean)."""
        dist = LogNormalDistribution(mean=1000, std_dev=2000)
        rng = random.Random(42)

        samples = [dist.sample(rng) for _ in range(1000)]
        median = sorted(samples)[500]
        mean = sum(samples) / len(samples)

        # Log-normal is right-skewed, median typically < mean
        assert median < mean


class TestCategoricalDistribution:
    """Tests for CategoricalDistribution."""

    def test_creation(self) -> None:
        """Test creating categorical distribution."""
        dist = CategoricalDistribution(weights={"M": 0.48, "F": 0.52})
        assert dist.weights == {"M": 0.48, "F": 0.52}

    def test_weights_validation(self) -> None:
        """Test that weights must sum to 1.0."""
        with pytest.raises(ValueError, match="sum to 1.0"):
            CategoricalDistribution(weights={"A": 0.3, "B": 0.3})

    def test_sample(self) -> None:
        """Test sampling."""
        dist = CategoricalDistribution(weights={"M": 0.48, "F": 0.52})
        rng = random.Random(42)

        result = dist.sample(rng)
        assert result in ["M", "F"]

    def test_weighted_selection(self) -> None:
        """Test that weights affect selection."""
        dist = CategoricalDistribution(weights={"common": 0.95, "rare": 0.05})
        rng = random.Random(42)

        results = [dist.sample(rng) for _ in range(1000)]
        common_count = results.count("common")

        assert common_count > 900  # Should be ~95%

    def test_sample_multiple(self) -> None:
        """Test sampling multiple values."""
        dist = CategoricalDistribution(weights={"A": 0.5, "B": 0.5})
        rng = random.Random(42)

        results = dist.sample_multiple(100, rng)
        assert len(results) == 100
        assert all(r in ["A", "B"] for r in results)


class TestAgeBandDistribution:
    """Tests for AgeBandDistribution."""

    def test_creation(self) -> None:
        """Test creating age band distribution."""
        dist = AgeBandDistribution(bands={"18-34": 0.5, "35-54": 0.3, "55+": 0.2})
        assert len(dist.bands) == 3

    def test_sample_in_bands(self) -> None:
        """Test that samples fall within defined bands."""
        dist = AgeBandDistribution(bands={"18-34": 0.5, "35-54": 0.3, "55-75": 0.2})
        rng = random.Random(42)

        for _ in range(100):
            age = dist.sample(rng)
            assert 18 <= age <= 75

    def test_senior_band(self) -> None:
        """Test handling of 65+ style bands."""
        dist = AgeBandDistribution(bands={"65+": 1.0})
        rng = random.Random(42)

        for _ in range(100):
            age = dist.sample(rng)
            assert 65 <= age <= 95  # Upper bound defaults to 95

    def test_sample_multiple(self) -> None:
        """Test sampling multiple ages."""
        dist = AgeBandDistribution(bands={"18-64": 0.7, "65+": 0.3})
        rng = random.Random(42)

        ages = dist.sample_multiple(100, rng)
        assert len(ages) == 100


class TestExplicitDistribution:
    """Tests for ExplicitDistribution."""

    def test_creation(self) -> None:
        """Test creating explicit distribution."""
        dist = ExplicitDistribution(values=[
            ("48201", 0.4),
            ("48113", 0.35),
            ("48029", 0.25),
        ])
        assert len(dist.values) == 3

    def test_sample(self) -> None:
        """Test sampling."""
        dist = ExplicitDistribution(values=[
            ("A", 0.5),
            ("B", 0.3),
            ("C", 0.2),
        ])
        rng = random.Random(42)

        result = dist.sample(rng)
        assert result in ["A", "B", "C"]

    def test_sample_multiple_unique(self) -> None:
        """Test sampling unique values."""
        dist = ExplicitDistribution(values=[
            ("A", 0.4),
            ("B", 0.3),
            ("C", 0.3),
        ])
        rng = random.Random(42)

        results = dist.sample_multiple(3, rng, unique=True)
        assert len(results) == 3
        assert len(set(results)) == 3  # All unique


class TestConditionalDistribution:
    """Tests for ConditionalDistribution."""

    def test_creation(self) -> None:
        """Test creating conditional distribution."""
        dist = ConditionalDistribution(rules=[
            {"condition": "severity == 'mild'", "distribution": {"type": "normal", "mean": 5, "std_dev": 1}},
            {"condition": "severity == 'severe'", "distribution": {"type": "normal", "mean": 15, "std_dev": 2}},
        ])
        assert len(dist.rules) == 2

    def test_condition_evaluation(self) -> None:
        """Test that conditions are evaluated correctly."""
        dist = ConditionalDistribution(rules=[
            {"condition": "category == 'A'", "distribution": {"type": "normal", "mean": 10, "std_dev": 1}},
            {"condition": "category == 'B'", "distribution": {"type": "normal", "mean": 100, "std_dev": 1}},
        ])
        rng = random.Random(42)

        # Sample with category A - should get values around 10
        values_a = [dist.sample({"category": "A"}, rng) for _ in range(100)]
        mean_a = sum(values_a) / len(values_a)
        assert 8 < mean_a < 12

        # Sample with category B - should get values around 100
        values_b = [dist.sample({"category": "B"}, rng) for _ in range(100)]
        mean_b = sum(values_b) / len(values_b)
        assert 95 < mean_b < 105

    def test_default_distribution(self) -> None:
        """Test default distribution when no condition matches."""
        dist = ConditionalDistribution(
            rules=[
                {"condition": "x == 'specific'", "distribution": {"type": "normal", "mean": 100, "std_dev": 1}},
            ],
            default={"type": "normal", "mean": 50, "std_dev": 1},
        )
        rng = random.Random(42)

        # No condition matches, should use default
        values = [dist.sample({"x": "other"}, rng) for _ in range(100)]
        mean = sum(values) / len(values)
        assert 45 < mean < 55


class TestCreateDistribution:
    """Tests for the create_distribution factory function."""

    def test_create_categorical(self) -> None:
        """Test creating categorical distribution from spec."""
        dist = create_distribution({
            "type": "categorical",
            "weights": {"M": 0.5, "F": 0.5}
        })
        assert isinstance(dist, CategoricalDistribution)

    def test_create_normal(self) -> None:
        """Test creating normal distribution from spec."""
        dist = create_distribution({
            "type": "normal",
            "mean": 100,
            "std_dev": 15
        })
        assert isinstance(dist, NormalDistribution)
        assert dist.mean == 100

    def test_create_log_normal(self) -> None:
        """Test creating log-normal distribution from spec."""
        dist = create_distribution({
            "type": "log_normal",
            "mean": 5000,
            "std_dev": 8000
        })
        assert isinstance(dist, LogNormalDistribution)

    def test_create_uniform(self) -> None:
        """Test creating uniform distribution from spec."""
        dist = create_distribution({
            "type": "uniform",
            "min": 0,
            "max": 100
        })
        assert isinstance(dist, UniformDistribution)

    def test_create_age_bands(self) -> None:
        """Test creating age band distribution from spec."""
        dist = create_distribution({
            "type": "age_bands",
            "bands": {"18-34": 0.5, "35-54": 0.5}
        })
        assert isinstance(dist, AgeBandDistribution)

    def test_create_explicit_dict_format(self) -> None:
        """Test creating explicit distribution from dict format."""
        dist = create_distribution({
            "type": "explicit",
            "values": {"A": 0.5, "B": 0.5}
        })
        assert isinstance(dist, ExplicitDistribution)

    def test_create_explicit_list_format(self) -> None:
        """Test creating explicit distribution from list format."""
        dist = create_distribution({
            "type": "explicit",
            "values": [
                {"value": "A", "weight": 0.5},
                {"value": "B", "weight": 0.5}
            ]
        })
        assert isinstance(dist, ExplicitDistribution)

    def test_unknown_type_raises(self) -> None:
        """Test that unknown type raises error."""
        with pytest.raises(ValueError, match="Unknown distribution type"):
            create_distribution({"type": "invalid"})
