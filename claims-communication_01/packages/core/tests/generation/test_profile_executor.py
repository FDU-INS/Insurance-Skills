"""Tests for profile executor module."""

import pytest
import random
from datetime import date

from healthsim.generation.profile_executor import (
    HierarchicalSeedManager,
    GeneratedEntity,
    ExecutionResult,
    ValidationMetric,
    ValidationReport,
    ProfileExecutor,
    execute_profile,
)
from healthsim.generation.profile_schema import (
    ProfileSpecification,
    GenerationSpec,
    DemographicsSpec,
    ClinicalSpec,
    CoverageSpec,
    ConditionSpec,
    DistributionSpec,
    DistributionType,
    GeographyReference,
)


# =============================================================================
# HierarchicalSeedManager Tests
# =============================================================================

class TestHierarchicalSeedManager:
    """Tests for HierarchicalSeedManager."""

    def test_basic_creation(self):
        """Test basic creation with seed."""
        manager = HierarchicalSeedManager(master_seed=42)
        
        assert manager.master_seed == 42

    def test_auto_seed_generation(self):
        """Test auto-generated seed when not provided."""
        manager = HierarchicalSeedManager()
        
        assert manager.master_seed is not None
        assert 0 <= manager.master_seed < 2**31

    def test_get_entity_seed_deterministic(self):
        """Test entity seeds are deterministic."""
        manager1 = HierarchicalSeedManager(master_seed=42)
        manager2 = HierarchicalSeedManager(master_seed=42)
        
        assert manager1.get_entity_seed(0) == manager2.get_entity_seed(0)
        assert manager1.get_entity_seed(5) == manager2.get_entity_seed(5)
        assert manager1.get_entity_seed(99) == manager2.get_entity_seed(99)

    def test_different_seeds_different_entities(self):
        """Test different master seeds produce different entity seeds."""
        manager1 = HierarchicalSeedManager(master_seed=42)
        manager2 = HierarchicalSeedManager(master_seed=43)
        
        assert manager1.get_entity_seed(0) != manager2.get_entity_seed(0)

    def test_entity_seeds_are_unique(self):
        """Test each entity gets a unique seed."""
        manager = HierarchicalSeedManager(master_seed=42)
        
        seeds = [manager.get_entity_seed(i) for i in range(100)]
        
        assert len(set(seeds)) == 100  # All unique

    def test_get_entity_rng(self):
        """Test getting RNG for entity."""
        manager = HierarchicalSeedManager(master_seed=42)
        
        rng = manager.get_entity_rng(5)
        
        assert isinstance(rng, random.Random)

    def test_entity_rng_deterministic(self):
        """Test entity RNG produces same sequence."""
        manager = HierarchicalSeedManager(master_seed=42)
        
        rng1 = manager.get_entity_rng(5)
        val1 = rng1.random()
        
        # Get fresh RNG for same entity
        manager2 = HierarchicalSeedManager(master_seed=42)
        rng2 = manager2.get_entity_rng(5)
        val2 = rng2.random()
        
        assert val1 == val2

    def test_reset(self):
        """Test reset clears entity seeds."""
        manager = HierarchicalSeedManager(master_seed=42)
        
        seed_before = manager.get_entity_seed(0)
        manager.reset()
        seed_after = manager.get_entity_seed(0)
        
        # Same seed after reset
        assert seed_before == seed_after

    def test_order_independence(self):
        """Test entity N always has same seed regardless of access order."""
        manager1 = HierarchicalSeedManager(master_seed=42)
        manager2 = HierarchicalSeedManager(master_seed=42)
        
        # Access in different order
        _ = manager1.get_entity_seed(0)
        _ = manager1.get_entity_seed(1)
        seed1_5 = manager1.get_entity_seed(5)
        
        _ = manager2.get_entity_seed(5)  # Access 5 first
        seed2_5 = manager2.get_entity_seed(5)
        
        # Seeds at index 5 should match even with different access patterns
        # Note: This may fail if implementation caches differently
        assert seed1_5 == seed2_5


# =============================================================================
# GeneratedEntity Tests
# =============================================================================

class TestGeneratedEntity:
    """Tests for GeneratedEntity dataclass."""

    def test_basic_creation(self):
        """Test basic entity creation."""
        entity = GeneratedEntity(index=0, seed=12345)
        
        assert entity.index == 0
        assert entity.seed == 12345
        assert entity.age is None
        assert entity.conditions == []

    def test_with_demographics(self):
        """Test entity with demographics."""
        entity = GeneratedEntity(
            index=1,
            seed=12345,
            age=45,
            gender="M",
            birth_date=date(1979, 6, 15),
            state="TX"
        )
        
        assert entity.age == 45
        assert entity.gender == "M"
        assert entity.state == "TX"

    def test_with_clinical(self):
        """Test entity with clinical data."""
        entity = GeneratedEntity(
            index=2,
            seed=12345,
            conditions=["E11", "I10"],
            severity="moderate",
            lab_values={"a1c": 7.5, "glucose": 140}
        )
        
        assert "E11" in entity.conditions
        assert entity.lab_values["a1c"] == 7.5

    def test_with_coverage(self):
        """Test entity with coverage."""
        entity = GeneratedEntity(
            index=3,
            seed=12345,
            coverage_type="Medicare",
            plan_type="Medicare Advantage"
        )
        
        assert entity.coverage_type == "Medicare"
        assert entity.plan_type == "Medicare Advantage"

    def test_attributes_extension(self):
        """Test custom attributes."""
        entity = GeneratedEntity(
            index=4,
            seed=12345,
            attributes={"custom_field": "value", "score": 85}
        )
        
        assert entity.attributes["custom_field"] == "value"


# =============================================================================
# ValidationMetric Tests
# =============================================================================

class TestValidationMetric:
    """Tests for ValidationMetric."""

    def test_passing_metric(self):
        """Test metric that passes."""
        metric = ValidationMetric(
            name="Test",
            target=0.50,
            actual=0.48,
            tolerance=0.05
        )
        
        assert metric.passed is True

    def test_failing_metric(self):
        """Test metric that fails."""
        metric = ValidationMetric(
            name="Test",
            target=0.50,
            actual=0.35,
            tolerance=0.05
        )
        
        assert metric.passed is False

    def test_exact_match(self):
        """Test exact match passes."""
        metric = ValidationMetric(
            name="Test",
            target=0.50,
            actual=0.50,
            tolerance=0.01
        )
        
        assert metric.passed is True

    def test_zero_target(self):
        """Test zero target handling."""
        metric_pass = ValidationMetric(name="Test", target=0, actual=0)
        metric_fail = ValidationMetric(name="Test", target=0, actual=0.1)
        
        assert metric_pass.passed is True
        assert metric_fail.passed is False


# =============================================================================
# ValidationReport Tests
# =============================================================================

class TestValidationReport:
    """Tests for ValidationReport."""

    def test_empty_report_passes(self):
        """Test empty report passes."""
        report = ValidationReport()
        
        assert report.passed is True

    def test_with_passing_metrics(self):
        """Test report with passing metrics."""
        report = ValidationReport(
            metrics=[
                ValidationMetric(name="A", target=0.5, actual=0.48),
                ValidationMetric(name="B", target=0.3, actual=0.31),
            ]
        )
        
        assert report.passed is True

    def test_with_failing_metric(self):
        """Test report with failing metric."""
        report = ValidationReport(
            metrics=[
                ValidationMetric(name="A", target=0.5, actual=0.48),
                ValidationMetric(name="B", target=0.3, actual=0.10),  # Fails
            ]
        )
        
        assert report.passed is False

    def test_with_error(self):
        """Test report with error."""
        report = ValidationReport(errors=["Something went wrong"])
        
        assert report.passed is False

    def test_warnings_dont_fail(self):
        """Test warnings don't cause failure."""
        report = ValidationReport(warnings=["Minor issue"])
        
        assert report.passed is True


# =============================================================================
# ProfileExecutor Tests
# =============================================================================

class TestProfileExecutor:
    """Tests for ProfileExecutor."""

    @pytest.fixture
    def minimal_profile(self):
        """Create minimal profile specification."""
        return ProfileSpecification(
            id="test-minimal",
            name="Minimal Test",
            generation=GenerationSpec(count=10)
        )

    @pytest.fixture
    def demographics_profile(self):
        """Create profile with demographics."""
        return ProfileSpecification(
            id="test-demographics",
            name="Demographics Test",
            generation=GenerationSpec(count=100, seed=42),
            demographics=DemographicsSpec(
                age=DistributionSpec(
                    type=DistributionType.NORMAL,
                    mean=45.0,
                    std_dev=10.0,
                    min=18.0,
                    max=90.0
                ),
                gender=DistributionSpec(
                    type=DistributionType.CATEGORICAL,
                    weights={"M": 0.48, "F": 0.52}
                )
            )
        )

    @pytest.fixture
    def clinical_profile(self):
        """Create profile with clinical data."""
        return ProfileSpecification(
            id="test-clinical",
            name="Clinical Test",
            generation=GenerationSpec(count=100, seed=42),
            clinical=ClinicalSpec(
                primary_condition=ConditionSpec(
                    code="E11",
                    description="Type 2 diabetes",
                    prevalence=1.0
                ),
                comorbidities=[
                    ConditionSpec(code="I10", prevalence=0.75),
                    ConditionSpec(code="E78", prevalence=0.60),
                ]
            )
        )

    @pytest.fixture
    def full_profile(self):
        """Create full profile specification."""
        return ProfileSpecification(
            id="test-full",
            name="Full Test",
            generation=GenerationSpec(count=200, seed=42),
            demographics=DemographicsSpec(
                age=DistributionSpec(
                    type=DistributionType.NORMAL,
                    mean=72.0,
                    std_dev=8.0,
                    min=65.0,
                    max=95.0
                ),
                gender=DistributionSpec(
                    type=DistributionType.CATEGORICAL,
                    weights={"M": 0.48, "F": 0.52}
                )
            ),
            clinical=ClinicalSpec(
                primary_condition=ConditionSpec(code="E11", prevalence=1.0),
                comorbidities=[
                    ConditionSpec(code="I10", prevalence=0.75),
                ]
            ),
            coverage=CoverageSpec(
                type="Medicare",
                plan_distribution={"Medicare Advantage": 0.55, "Original Medicare": 0.45}
            )
        )

    def test_executor_creation(self, minimal_profile):
        """Test executor creation."""
        executor = ProfileExecutor(minimal_profile)
        
        assert executor.profile == minimal_profile
        assert executor.seed is not None

    def test_executor_with_seed(self, minimal_profile):
        """Test executor with explicit seed."""
        executor = ProfileExecutor(minimal_profile, seed=12345)
        
        assert executor.seed == 12345

    def test_execute_minimal(self, minimal_profile):
        """Test executing minimal profile."""
        executor = ProfileExecutor(minimal_profile, seed=42)
        
        result = executor.execute()
        
        assert result.count == 10
        assert len(result.entities) == 10
        assert result.profile_id == "test-minimal"

    def test_execute_with_demographics(self, demographics_profile):
        """Test execution with demographics."""
        executor = ProfileExecutor(demographics_profile)
        
        result = executor.execute()
        
        assert result.count == 100
        
        # Check all entities have age and gender
        for entity in result.entities:
            assert entity.age is not None
            assert 18 <= entity.age <= 90
            assert entity.gender in ["M", "F"]
            assert entity.birth_date is not None

    def test_execute_with_clinical(self, clinical_profile):
        """Test execution with clinical data."""
        executor = ProfileExecutor(clinical_profile)
        
        result = executor.execute()
        
        # All should have primary condition (100% prevalence)
        e11_count = sum(1 for e in result.entities if "E11" in e.conditions)
        assert e11_count == 100
        
        # Comorbidities should be ~75% and ~60%
        i10_count = sum(1 for e in result.entities if "I10" in e.conditions)
        e78_count = sum(1 for e in result.entities if "E78" in e.conditions)
        
        assert 60 < i10_count < 90  # ~75%
        assert 45 < e78_count < 75  # ~60%

    def test_execute_with_coverage(self, full_profile):
        """Test execution with coverage."""
        executor = ProfileExecutor(full_profile)
        
        result = executor.execute()
        
        # Check coverage is set
        ma_count = sum(1 for e in result.entities if e.plan_type == "Medicare Advantage")
        om_count = sum(1 for e in result.entities if e.plan_type == "Original Medicare")
        
        assert ma_count + om_count == 200
        # Roughly 55% MA, 45% OM
        assert 90 < ma_count < 130

    def test_reproducibility(self, demographics_profile):
        """Test same seed produces same results."""
        executor1 = ProfileExecutor(demographics_profile, seed=42)
        executor2 = ProfileExecutor(demographics_profile, seed=42)
        
        result1 = executor1.execute()
        result2 = executor2.execute()
        
        # Same ages
        ages1 = [e.age for e in result1.entities]
        ages2 = [e.age for e in result2.entities]
        assert ages1 == ages2
        
        # Same genders
        genders1 = [e.gender for e in result1.entities]
        genders2 = [e.gender for e in result2.entities]
        assert genders1 == genders2

    def test_different_seeds_different_results(self, demographics_profile):
        """Test different seeds produce different results."""
        executor1 = ProfileExecutor(demographics_profile, seed=42)
        executor2 = ProfileExecutor(demographics_profile, seed=43)
        
        result1 = executor1.execute()
        result2 = executor2.execute()
        
        ages1 = [e.age for e in result1.entities]
        ages2 = [e.age for e in result2.entities]
        
        assert ages1 != ages2

    def test_count_override(self, minimal_profile):
        """Test count override."""
        executor = ProfileExecutor(minimal_profile)
        
        result = executor.execute(count_override=5)
        
        assert result.count == 5
        assert len(result.entities) == 5

    def test_dry_run(self, minimal_profile):
        """Test dry run limits count."""
        minimal_profile.generation.count = 1000
        executor = ProfileExecutor(minimal_profile)
        
        result = executor.execute(dry_run=True)
        
        assert result.count == 5  # Dry run caps at 5

    def test_validation_report_generated(self, demographics_profile):
        """Test validation report is generated."""
        executor = ProfileExecutor(demographics_profile)
        
        result = executor.execute()
        
        assert result.validation is not None
        assert len(result.validation.metrics) > 0

    def test_validation_age_mean(self, demographics_profile):
        """Test age mean validation."""
        executor = ProfileExecutor(demographics_profile)
        
        result = executor.execute()
        
        # Find age mean metric
        age_metric = next(
            (m for m in result.validation.metrics if "Age" in m.name),
            None
        )
        
        assert age_metric is not None
        assert age_metric.target == 45.0
        assert 40 < age_metric.actual < 50  # Close to target

    def test_validation_gender_distribution(self, demographics_profile):
        """Test gender distribution validation."""
        executor = ProfileExecutor(demographics_profile)
        
        result = executor.execute()
        
        # Find gender metrics
        gender_metrics = [
            m for m in result.validation.metrics if "Gender" in m.name
        ]
        
        assert len(gender_metrics) == 2

    def test_entity_indices_sequential(self, minimal_profile):
        """Test entity indices are sequential."""
        executor = ProfileExecutor(minimal_profile)
        
        result = executor.execute()
        
        indices = [e.index for e in result.entities]
        assert indices == list(range(10))

    def test_entity_seeds_unique(self, minimal_profile):
        """Test each entity has unique seed."""
        executor = ProfileExecutor(minimal_profile)
        
        result = executor.execute()
        
        seeds = [e.seed for e in result.entities]
        assert len(set(seeds)) == len(seeds)

    def test_duration_recorded(self, minimal_profile):
        """Test execution duration is recorded."""
        executor = ProfileExecutor(minimal_profile)
        
        result = executor.execute()
        
        assert result.duration_seconds >= 0

    def test_created_timestamp(self, minimal_profile):
        """Test created timestamp is set."""
        executor = ProfileExecutor(minimal_profile)
        
        result = executor.execute()
        
        assert result.created is not None


# =============================================================================
# execute_profile Convenience Function Tests
# =============================================================================

class TestExecuteProfile:
    """Tests for execute_profile convenience function."""

    def test_with_dict(self):
        """Test execution with dict input."""
        result = execute_profile({
            "id": "test-dict",
            "name": "Dict Test",
            "generation": {"count": 10}
        })
        
        assert result.count == 10

    def test_with_json_string(self):
        """Test execution with JSON string input."""
        json_str = '''
        {
            "id": "test-json",
            "name": "JSON Test",
            "generation": {"count": 15}
        }
        '''
        
        result = execute_profile(json_str)
        
        assert result.count == 15

    def test_with_profile_spec(self):
        """Test execution with ProfileSpecification input."""
        spec = ProfileSpecification(
            id="test-spec",
            name="Spec Test",
            generation=GenerationSpec(count=20)
        )
        
        result = execute_profile(spec)
        
        assert result.count == 20

    def test_seed_override(self):
        """Test seed override."""
        result1 = execute_profile(
            {"id": "test", "name": "Test", "generation": {"count": 10}},
            seed=42
        )
        result2 = execute_profile(
            {"id": "test", "name": "Test", "generation": {"count": 10}},
            seed=42
        )
        
        seeds1 = [e.seed for e in result1.entities]
        seeds2 = [e.seed for e in result2.entities]
        
        assert seeds1 == seeds2

    def test_count_override(self):
        """Test count override."""
        result = execute_profile(
            {"id": "test", "name": "Test", "generation": {"count": 100}},
            count=5
        )
        
        assert result.count == 5

    def test_full_profile_dict(self):
        """Test full profile via dict."""
        result = execute_profile({
            "id": "full-test",
            "name": "Full Dict Test",
            "generation": {"count": 50, "seed": 42},
            "demographics": {
                "age": {"type": "normal", "mean": 50, "std_dev": 15},
                "gender": {"type": "categorical", "weights": {"M": 0.5, "F": 0.5}}
            },
            "clinical": {
                "primary_condition": {"code": "E11", "prevalence": 1.0}
            }
        })
        
        assert result.count == 50
        assert all(e.age is not None for e in result.entities)
        assert all("E11" in e.conditions for e in result.entities)


# =============================================================================
# Edge Cases and Error Handling
# =============================================================================

class TestEdgeCases:
    """Tests for edge cases and error handling."""

    def test_empty_demographics(self):
        """Test profile with empty demographics."""
        spec = ProfileSpecification(
            id="test-empty",
            name="Empty Demo",
            generation=GenerationSpec(count=5),
            demographics=DemographicsSpec()
        )
        
        executor = ProfileExecutor(spec)
        result = executor.execute()
        
        assert result.count == 5
        # Entities should have None for demographics
        assert all(e.age is None for e in result.entities)

    def test_empty_clinical(self):
        """Test profile with empty clinical."""
        spec = ProfileSpecification(
            id="test-empty-clinical",
            name="Empty Clinical",
            generation=GenerationSpec(count=5),
            clinical=ClinicalSpec()
        )
        
        executor = ProfileExecutor(spec)
        result = executor.execute()
        
        assert result.count == 5
        # No conditions assigned
        assert all(len(e.conditions) == 0 for e in result.entities)

    def test_zero_prevalence(self):
        """Test condition with zero prevalence."""
        spec = ProfileSpecification(
            id="test-zero-prev",
            name="Zero Prevalence",
            generation=GenerationSpec(count=100, seed=42),
            clinical=ClinicalSpec(
                primary_condition=ConditionSpec(code="E11", prevalence=0.0)
            )
        )
        
        executor = ProfileExecutor(spec)
        result = executor.execute()
        
        # No one should have the condition
        e11_count = sum(1 for e in result.entities if "E11" in e.conditions)
        assert e11_count == 0

    def test_age_bands_distribution(self):
        """Test age bands distribution type."""
        spec = ProfileSpecification(
            id="test-age-bands",
            name="Age Bands Test",
            generation=GenerationSpec(count=100, seed=42),
            demographics=DemographicsSpec(
                age=DistributionSpec(
                    type=DistributionType.AGE_BANDS,
                    bands={"18-34": 0.30, "35-54": 0.40, "55-64": 0.30}
                )
            )
        )
        
        executor = ProfileExecutor(spec)
        result = executor.execute()
        
        # All ages should be within bands
        for entity in result.entities:
            assert 18 <= entity.age <= 64

    def test_geography_reference(self):
        """Test geography reference handling."""
        spec = ProfileSpecification(
            id="test-geo",
            name="Geo Test",
            generation=GenerationSpec(count=10),
            demographics=DemographicsSpec(
                geography=GeographyReference(
                    type="county",
                    fips="48201",
                    state="TX"
                )
            )
        )
        
        executor = ProfileExecutor(spec)
        result = executor.execute()
        
        # Check geography is set
        for entity in result.entities:
            assert entity.county_fips == "48201"

    def test_large_count(self):
        """Test with larger entity count."""
        spec = ProfileSpecification(
            id="test-large",
            name="Large Test",
            generation=GenerationSpec(count=1000, seed=42),
            demographics=DemographicsSpec(
                age=DistributionSpec(type=DistributionType.NORMAL, mean=50.0, std_dev=15.0)
            )
        )
        
        executor = ProfileExecutor(spec)
        result = executor.execute()
        
        assert result.count == 1000
        # Validate mean is close to target
        ages = [e.age for e in result.entities]
        mean_age = sum(ages) / len(ages)
        assert 47 < mean_age < 53  # Within 3 of target
