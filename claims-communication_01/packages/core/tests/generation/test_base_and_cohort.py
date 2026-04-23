"""Tests for base generator classes, cohort generation, and reproducibility."""

import pytest
from datetime import date, datetime, timedelta

from healthsim.generation.base import BaseGenerator, PersonGenerator
from healthsim.generation.cohort import (
    CohortConstraints,
    CohortProgress,
    CohortGenerator,
)
from healthsim.generation.reproducibility import SeedManager
from healthsim.person.demographics import Gender


# =============================================================================
# SeedManager Tests
# =============================================================================

class TestSeedManager:
    """Tests for SeedManager class."""

    def test_initialization_with_seed(self):
        """Test initialization with a specific seed."""
        manager = SeedManager(seed=42)
        
        assert manager.seed == 42
        assert manager.rng is not None
        assert manager.faker is not None

    def test_initialization_without_seed(self):
        """Test initialization without a seed."""
        manager = SeedManager()
        
        assert manager.seed is None

    def test_initialization_with_locale(self):
        """Test initialization with a specific locale."""
        manager = SeedManager(seed=42, locale="de_DE")
        
        assert manager.locale == "de_DE"

    def test_get_random_int(self):
        """Test random integer generation."""
        manager = SeedManager(seed=42)
        
        value = manager.get_random_int(1, 100)
        
        assert 1 <= value <= 100

    def test_get_random_int_reproducible(self):
        """Test random integers are reproducible with same seed."""
        m1 = SeedManager(seed=42)
        m2 = SeedManager(seed=42)
        
        assert m1.get_random_int(1, 100) == m2.get_random_int(1, 100)
        assert m1.get_random_int(1, 100) == m2.get_random_int(1, 100)

    def test_get_random_float(self):
        """Test random float generation."""
        manager = SeedManager(seed=42)
        
        value = manager.get_random_float(0.0, 1.0)
        
        assert 0.0 <= value <= 1.0

    def test_get_random_float_range(self):
        """Test random float in specific range."""
        manager = SeedManager(seed=42)
        
        value = manager.get_random_float(10.0, 20.0)
        
        assert 10.0 <= value <= 20.0

    def test_get_random_choice(self):
        """Test random choice from list."""
        manager = SeedManager(seed=42)
        options = ["a", "b", "c", "d"]
        
        choice = manager.get_random_choice(options)
        
        assert choice in options

    def test_get_random_sample(self):
        """Test random sample from list."""
        manager = SeedManager(seed=42)
        options = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        
        sample = manager.get_random_sample(options, 3)
        
        assert len(sample) == 3
        assert all(s in options for s in sample)

    def test_get_random_sample_large_k(self):
        """Test sample with k larger than list."""
        manager = SeedManager(seed=42)
        options = [1, 2, 3]
        
        sample = manager.get_random_sample(options, 10)
        
        assert len(sample) == 3  # Limited to list size

    def test_shuffle(self):
        """Test list shuffling."""
        manager = SeedManager(seed=42)
        items = [1, 2, 3, 4, 5]
        original = items.copy()
        
        result = manager.shuffle(items)
        
        assert result is items  # In place
        assert set(result) == set(original)

    def test_get_random_bool_default(self):
        """Test random boolean with default probability."""
        manager = SeedManager(seed=42)
        
        # Sample many times to verify roughly 50/50
        results = [manager.get_random_bool() for _ in range(100)]
        
        assert 30 < sum(results) < 70  # Roughly 50%

    def test_get_random_bool_high_probability(self):
        """Test random boolean with high probability."""
        manager = SeedManager(seed=42)
        
        results = [manager.get_random_bool(0.9) for _ in range(100)]
        
        assert sum(results) > 70  # Most should be True

    def test_get_child_seed(self):
        """Test child seed generation."""
        manager = SeedManager(seed=42)
        
        child1 = manager.get_child_seed()
        child2 = manager.get_child_seed()
        
        assert isinstance(child1, int)
        assert child1 != child2  # Different seeds

    def test_get_child_seed_reproducible(self):
        """Test child seeds are reproducible."""
        m1 = SeedManager(seed=42)
        m2 = SeedManager(seed=42)
        
        assert m1.get_child_seed() == m2.get_child_seed()

    def test_reset(self):
        """Test reset restores initial state."""
        manager = SeedManager(seed=42)
        
        # Generate some values
        v1 = manager.get_random_int(1, 100)
        v2 = manager.get_random_int(1, 100)
        
        # Reset and generate again
        manager.reset()
        
        assert manager.get_random_int(1, 100) == v1
        assert manager.get_random_int(1, 100) == v2


# =============================================================================
# BaseGenerator Tests
# =============================================================================

class TestBaseGenerator:
    """Tests for BaseGenerator class."""

    @pytest.fixture
    def generator(self):
        """Create generator fixture."""
        return BaseGenerator(seed=42)

    def test_initialization(self, generator):
        """Test generator initialization."""
        assert generator.seed_manager is not None
        assert generator.faker is not None

    def test_rng_property(self, generator):
        """Test rng property."""
        assert generator.rng is not None

    def test_generate_id_with_prefix(self, generator):
        """Test ID generation with prefix."""
        id1 = generator.generate_id("PERSON")
        
        assert id1.startswith("PERSON-")
        assert len(id1) == 15  # PERSON- + 8 chars

    def test_generate_id_without_prefix(self, generator):
        """Test ID generation without prefix."""
        id1 = generator.generate_id()
        
        assert len(id1) == 8

    def test_generate_id_unique(self, generator):
        """Test generated IDs are unique."""
        ids = [generator.generate_id("TEST") for _ in range(100)]
        
        assert len(ids) == len(set(ids))

    def test_random_choice(self, generator):
        """Test random choice."""
        options = ["a", "b", "c"]
        
        choice = generator.random_choice(options)
        
        assert choice in options

    def test_random_int(self, generator):
        """Test random integer."""
        value = generator.random_int(10, 20)
        
        assert 10 <= value <= 20

    def test_random_float(self, generator):
        """Test random float."""
        value = generator.random_float(0.0, 1.0)
        
        assert 0.0 <= value <= 1.0

    def test_random_bool(self, generator):
        """Test random boolean."""
        value = generator.random_bool(0.5)
        
        assert isinstance(value, bool)

    def test_weighted_choice(self, generator):
        """Test weighted choice."""
        options = [("a", 0.9), ("b", 0.1)]
        
        # Sample many times
        results = [generator.weighted_choice(options) for _ in range(100)]
        
        # 'a' should be much more common
        assert results.count("a") > results.count("b")

    def test_random_date_between(self, generator):
        """Test random date in range."""
        start = date(2024, 1, 1)
        end = date(2024, 12, 31)
        
        result = generator.random_date_between(start, end)
        
        assert start <= result <= end

    def test_random_datetime_between(self, generator):
        """Test random datetime in range."""
        start = datetime(2024, 1, 1, 0, 0, 0)
        end = datetime(2024, 12, 31, 23, 59, 59)
        
        result = generator.random_datetime_between(start, end)
        
        assert start <= result <= end

    def test_reset(self, generator):
        """Test generator reset."""
        v1 = generator.random_int(1, 100)
        v2 = generator.random_int(1, 100)
        
        generator.reset()
        
        assert generator.random_int(1, 100) == v1
        assert generator.random_int(1, 100) == v2

    def test_reproducibility(self):
        """Test generators with same seed produce same results."""
        g1 = BaseGenerator(seed=42)
        g2 = BaseGenerator(seed=42)
        
        assert g1.random_int(1, 100) == g2.random_int(1, 100)
        assert g1.random_float(0, 1) == g2.random_float(0, 1)


# =============================================================================
# PersonGenerator Tests
# =============================================================================

class TestPersonGenerator:
    """Tests for PersonGenerator class."""

    @pytest.fixture
    def generator(self):
        """Create generator fixture."""
        return PersonGenerator(seed=42)

    def test_generate_person_basic(self, generator):
        """Test basic person generation."""
        person = generator.generate_person()
        
        assert person.id is not None
        assert person.name is not None
        assert person.birth_date is not None
        assert person.gender is not None

    def test_generate_person_with_age_range(self, generator):
        """Test person generation with age range."""
        person = generator.generate_person(age_range=(25, 35))
        
        today = date.today()
        age = (today - person.birth_date).days // 365
        
        assert 24 <= age <= 36  # Allow some margin

    def test_generate_person_with_gender(self, generator):
        """Test person generation with specific gender."""
        male = generator.generate_person(gender=Gender.MALE)
        
        assert male.gender == Gender.MALE

    def test_generate_person_with_address(self, generator):
        """Test person with address."""
        person = generator.generate_person(include_address=True)
        
        assert person.address is not None
        assert person.address.city is not None
        assert person.address.state is not None

    def test_generate_person_without_address(self, generator):
        """Test person without address."""
        person = generator.generate_person(include_address=False)
        
        assert person.address is None

    def test_generate_person_with_contact(self, generator):
        """Test person with contact info."""
        person = generator.generate_person(include_contact=True)
        
        assert person.contact is not None
        assert person.contact.email is not None

    def test_generate_person_without_contact(self, generator):
        """Test person without contact info."""
        person = generator.generate_person(include_contact=False)
        
        assert person.contact is None

    def test_generate_name_male(self, generator):
        """Test male name generation."""
        name = generator.generate_name(Gender.MALE)
        
        assert name.given_name is not None
        assert name.family_name is not None

    def test_generate_name_female(self, generator):
        """Test female name generation."""
        name = generator.generate_name(Gender.FEMALE)
        
        assert name.given_name is not None
        assert name.family_name is not None

    def test_generate_birth_date(self, generator):
        """Test birth date generation."""
        birth_date = generator.generate_birth_date((30, 40))
        
        today = date.today()
        age = (today - birth_date).days // 365
        
        assert 29 <= age <= 41

    def test_generate_address(self, generator):
        """Test address generation."""
        address = generator.generate_address()
        
        assert address.street_address is not None
        assert address.city is not None
        assert address.state is not None
        assert address.postal_code is not None
        assert address.country == "US"

    def test_generate_contact(self, generator):
        """Test contact info generation."""
        contact = generator.generate_contact()
        
        assert contact.phone is not None
        assert contact.email is not None

    def test_generate_ssn(self, generator):
        """Test SSN generation."""
        ssn = generator.generate_ssn()
        
        assert len(ssn) == 11  # XXX-XX-XXXX format

    def test_reproducibility(self):
        """Test person generation is reproducible for seeded elements."""
        g1 = PersonGenerator(seed=42)
        g2 = PersonGenerator(seed=42)
        
        p1 = g1.generate_person()
        p2 = g2.generate_person()
        
        # IDs use uuid4 which isn't seeded, so skip ID comparison
        # But the seeded elements should match
        assert p1.name.given_name == p2.name.given_name
        assert p1.name.family_name == p2.name.family_name
        assert p1.birth_date == p2.birth_date
        assert p1.gender == p2.gender


# =============================================================================
# CohortConstraints Tests
# =============================================================================

class TestCohortConstraints:
    """Tests for CohortConstraints dataclass."""

    def test_default_values(self):
        """Test default constraint values."""
        constraints = CohortConstraints()
        
        assert constraints.count == 100
        assert constraints.min_age is None
        assert constraints.max_age is None
        assert constraints.gender_distribution == {}
        assert constraints.custom == {}

    def test_with_count(self):
        """Test constraints with count."""
        constraints = CohortConstraints(count=50)
        
        assert constraints.count == 50

    def test_with_age_range(self):
        """Test constraints with age range."""
        constraints = CohortConstraints(min_age=18, max_age=65)
        
        assert constraints.min_age == 18
        assert constraints.max_age == 65

    def test_with_gender_distribution(self):
        """Test constraints with gender distribution."""
        constraints = CohortConstraints(
            gender_distribution={"male": 50, "female": 50}
        )
        
        assert constraints.gender_distribution["male"] == 50

    def test_with_custom(self):
        """Test constraints with custom values."""
        constraints = CohortConstraints(
            custom={"condition": "diabetes", "severity": "moderate"}
        )
        
        assert constraints.custom["condition"] == "diabetes"

    def test_to_dict(self):
        """Test conversion to dictionary."""
        constraints = CohortConstraints(
            count=50,
            min_age=18,
            max_age=65
        )
        
        d = constraints.to_dict()
        
        assert d["count"] == 50
        assert d["min_age"] == 18
        assert d["max_age"] == 65


# =============================================================================
# CohortProgress Tests
# =============================================================================

class TestCohortProgress:
    """Tests for CohortProgress dataclass."""

    def test_default_values(self):
        """Test default progress values."""
        progress = CohortProgress()
        
        assert progress.total == 0
        assert progress.completed == 0
        assert progress.failed == 0
        assert progress.current_item == 0

    def test_percent_complete_empty(self):
        """Test percent complete with no items."""
        progress = CohortProgress(total=0)
        
        assert progress.percent_complete == 0.0

    def test_percent_complete_partial(self):
        """Test percent complete partial."""
        progress = CohortProgress(total=100, completed=50)
        
        assert progress.percent_complete == 50.0

    def test_percent_complete_full(self):
        """Test percent complete full."""
        progress = CohortProgress(total=100, completed=100)
        
        assert progress.percent_complete == 100.0

    def test_is_complete_false(self):
        """Test is_complete when not done."""
        progress = CohortProgress(total=100, completed=50)
        
        assert progress.is_complete is False

    def test_is_complete_true(self):
        """Test is_complete when done."""
        progress = CohortProgress(total=100, completed=100)
        
        assert progress.is_complete is True

    def test_is_complete_with_failures(self):
        """Test is_complete counts failures."""
        progress = CohortProgress(total=100, completed=90, failed=10)
        
        assert progress.is_complete is True


# =============================================================================
# CohortGenerator Tests
# =============================================================================

class TestCohortGenerator:
    """Tests for CohortGenerator base class."""

    class SimpleCohortGenerator(CohortGenerator[dict]):
        """Simple implementation for testing."""
        
        def generate_one(self, index: int, constraints: CohortConstraints) -> dict:
            return {"index": index, "id": f"ITEM-{index:04d}"}

    @pytest.fixture
    def generator(self):
        """Create generator fixture."""
        return self.SimpleCohortGenerator(seed=42)

    def test_initialization(self, generator):
        """Test generator initialization."""
        assert generator.seed_manager is not None

    def test_generate_one_not_implemented(self):
        """Test base class raises NotImplementedError."""
        base = CohortGenerator(seed=42)
        
        with pytest.raises(NotImplementedError):
            base.generate_one(0, CohortConstraints())

    def test_generate(self, generator):
        """Test batch generation."""
        constraints = CohortConstraints(count=10)
        
        results = generator.generate(constraints)
        
        assert len(results) == 10
        assert results[0]["index"] == 0
        assert results[9]["index"] == 9

    def test_generate_with_callback(self, generator):
        """Test generation with progress callback."""
        constraints = CohortConstraints(count=5)
        progress_updates = []
        
        def callback(progress):
            progress_updates.append(progress.completed)
        
        generator.generate(constraints, progress_callback=callback)
        
        assert len(progress_updates) == 5
        assert progress_updates[-1] == 5

    def test_generate_iter(self, generator):
        """Test iterator generation."""
        constraints = CohortConstraints(count=5)
        
        results = list(generator.generate_iter(constraints))
        
        assert len(results) == 5

    def test_progress_property(self, generator):
        """Test progress property."""
        constraints = CohortConstraints(count=10)
        generator.generate(constraints)
        
        progress = generator.progress
        
        assert progress.total == 10
        assert progress.completed == 10
        assert progress.is_complete

    def test_reset(self, generator):
        """Test generator reset."""
        constraints = CohortConstraints(count=3)
        
        r1 = generator.generate(constraints)
        generator.reset()
        r2 = generator.generate(constraints)
        
        # Results should be identical after reset
        for i in range(3):
            assert r1[i]["id"] == r2[i]["id"]


# =============================================================================
# Integration Tests
# =============================================================================

class TestGeneratorIntegration:
    """Integration tests for generators."""

    def test_person_cohort_generation(self):
        """Test generating a cohort of persons."""
        
        class PersonCohortGenerator(CohortGenerator):
            def __init__(self, seed=None):
                super().__init__(seed)
                self.person_gen = PersonGenerator(seed=seed)
            
            def generate_one(self, index, constraints):
                age_range = (
                    constraints.min_age or 18,
                    constraints.max_age or 85
                )
                return self.person_gen.generate_person(age_range=age_range)
        
        generator = PersonCohortGenerator(seed=42)
        constraints = CohortConstraints(count=5, min_age=25, max_age=35)
        
        persons = generator.generate(constraints)
        
        assert len(persons) == 5
        for person in persons:
            assert person.id is not None
            # Check age is in range
            today = date.today()
            age = (today - person.birth_date).days // 365
            assert 24 <= age <= 36

    def test_seed_propagation(self):
        """Test seed propagates through generator hierarchy."""
        
        class NestedGenerator(BaseGenerator):
            def __init__(self, seed=None):
                super().__init__(seed)
                self.child_seed = self.seed_manager.get_child_seed()
                self.child_gen = BaseGenerator(seed=self.child_seed)
            
            def generate(self):
                return {
                    "parent": self.random_int(1, 100),
                    "child": self.child_gen.random_int(1, 100)
                }
        
        g1 = NestedGenerator(seed=42)
        g2 = NestedGenerator(seed=42)
        
        r1 = g1.generate()
        r2 = g2.generate()
        
        assert r1 == r2

    def test_large_cohort_memory_efficient(self):
        """Test iterator is memory efficient for large cohorts."""
        
        class CountingGenerator(CohortGenerator[int]):
            def generate_one(self, index, constraints):
                return index
        
        generator = CountingGenerator(seed=42)
        constraints = CohortConstraints(count=10000)
        
        # Use iterator instead of loading all to memory
        count = 0
        for item in generator.generate_iter(constraints):
            count += 1
            if count > 100:
                break  # Don't need to iterate all
        
        assert count == 101
