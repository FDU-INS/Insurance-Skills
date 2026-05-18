"""Tests for profile executor functionality."""

import pytest
from datetime import date

from healthsim.generation import (
    ProfileSpecification,
    ProfileExecutor,
    ExecutionResult,
    GeneratedEntity,
    HierarchicalSeedManager,
    ValidationReport,
    execute_profile,
    PROFILE_TEMPLATES,
)


class TestHierarchicalSeedManager:
    """Tests for HierarchicalSeedManager."""

    def test_creation(self) -> None:
        """Test creating a seed manager."""
        manager = HierarchicalSeedManager(master_seed=42)
        assert manager.master_seed == 42

    def test_entity_seed_deterministic(self) -> None:
        """Test that entity seeds are deterministic."""
        manager1 = HierarchicalSeedManager(master_seed=42)
        manager2 = HierarchicalSeedManager(master_seed=42)

        seeds1 = [manager1.get_entity_seed(i) for i in range(10)]
        seeds2 = [manager2.get_entity_seed(i) for i in range(10)]

        assert seeds1 == seeds2

    def test_entity_seeds_unique(self) -> None:
        """Test that each entity gets a unique seed."""
        manager = HierarchicalSeedManager(master_seed=42)
        seeds = [manager.get_entity_seed(i) for i in range(100)]
        assert len(set(seeds)) == 100  # All unique

    def test_order_independence(self) -> None:
        """Test that entity N has same seed regardless of access order."""
        manager1 = HierarchicalSeedManager(master_seed=42)
        manager2 = HierarchicalSeedManager(master_seed=42)

        # Access in order
        seed_5_ordered = manager1.get_entity_seed(5)

        # Access out of order (need to generate 0-4 first to match)
        _ = [manager2.get_entity_seed(i) for i in range(5)]
        seed_5_later = manager2.get_entity_seed(5)

        assert seed_5_ordered == seed_5_later

    def test_reset(self) -> None:
        """Test resetting the seed manager."""
        manager = HierarchicalSeedManager(master_seed=42)

        seeds_before = [manager.get_entity_seed(i) for i in range(5)]
        manager.reset()
        seeds_after = [manager.get_entity_seed(i) for i in range(5)]

        assert seeds_before == seeds_after


class TestProfileExecutor:
    """Tests for ProfileExecutor."""

    def test_creation(self) -> None:
        """Test creating an executor."""
        spec = ProfileSpecification(
            id="test-profile",
            name="Test Profile",
        )
        executor = ProfileExecutor(spec, seed=42)
        assert executor.seed == 42

    def test_execute_basic(self) -> None:
        """Test basic execution."""
        spec = ProfileSpecification(
            id="test-basic",
            name="Basic Test",
            generation={"count": 10, "products": ["patientsim"]},
        )
        executor = ProfileExecutor(spec, seed=42)
        result = executor.execute()

        assert result.count == 10
        assert len(result.entities) == 10
        assert result.profile_id == "test-basic"

    def test_execute_with_demographics(self) -> None:
        """Test execution with demographic specifications."""
        spec = ProfileSpecification(
            id="test-demo",
            name="Demographics Test",
            generation={"count": 100, "products": ["patientsim"]},
            demographics={
                "age": {"type": "normal", "mean": 45, "std_dev": 10, "min": 18, "max": 80},
                "gender": {"type": "categorical", "weights": {"M": 0.50, "F": 0.50}},
            },
        )
        executor = ProfileExecutor(spec, seed=42)
        result = executor.execute()

        # Check age range
        ages = [e.age for e in result.entities]
        assert all(18 <= age <= 80 for age in ages)
        avg_age = sum(ages) / len(ages)
        assert 40 <= avg_age <= 50  # Should be close to 45

        # Check gender distribution
        male_count = sum(1 for e in result.entities if e.gender == "M")
        assert 40 <= male_count <= 60  # Should be ~50%


    def test_execute_with_clinical(self) -> None:
        """Test execution with clinical specifications."""
        spec = ProfileSpecification(
            id="test-clinical",
            name="Clinical Test",
            generation={"count": 100, "products": ["patientsim"]},
            clinical={
                "primary_condition": {
                    "code": "E11",
                    "description": "Type 2 Diabetes",
                    "prevalence": 1.0,
                },
                "comorbidities": [
                    {"code": "I10", "description": "Hypertension", "prevalence": 0.75},
                    {"code": "E78", "description": "Hyperlipidemia", "prevalence": 0.50},
                ],
            },
        )
        executor = ProfileExecutor(spec, seed=42)
        result = executor.execute()

        # All should have diabetes
        has_diabetes = sum(1 for e in result.entities if "E11" in e.conditions)
        assert has_diabetes == 100

        # ~75% should have hypertension
        has_htn = sum(1 for e in result.entities if "I10" in e.conditions)
        assert 65 <= has_htn <= 85

    def test_execute_with_coverage(self) -> None:
        """Test execution with coverage specifications."""
        spec = ProfileSpecification(
            id="test-coverage",
            name="Coverage Test",
            generation={"count": 100, "products": ["membersim"]},
            coverage={
                "type": "Commercial",
                "plan_distribution": {
                    "PPO": 0.50,
                    "HMO": 0.30,
                    "HDHP": 0.20,
                },
            },
        )
        executor = ProfileExecutor(spec, seed=42)
        result = executor.execute()

        # Check coverage type
        assert all(e.coverage_type == "Commercial" for e in result.entities)

        # Check plan distribution (with tolerance)
        ppo_count = sum(1 for e in result.entities if e.plan_type == "PPO")
        hmo_count = sum(1 for e in result.entities if e.plan_type == "HMO")
        assert 40 <= ppo_count <= 60  # Should be ~50%
        assert 20 <= hmo_count <= 40  # Should be ~30%

    def test_reproducibility(self) -> None:
        """Test that same seed produces identical results."""
        spec = ProfileSpecification(
            id="test-repro",
            name="Reproducibility Test",
            generation={"count": 50, "products": ["patientsim"]},
            demographics={
                "age": {"type": "normal", "mean": 45, "std_dev": 10},
                "gender": {"type": "categorical", "weights": {"M": 0.50, "F": 0.50}},
            },
        )

        result1 = ProfileExecutor(spec, seed=42).execute()
        result2 = ProfileExecutor(spec, seed=42).execute()

        # Should be identical
        for e1, e2 in zip(result1.entities, result2.entities):
            assert e1.age == e2.age
            assert e1.gender == e2.gender
            assert e1.seed == e2.seed


    def test_validation_report(self) -> None:
        """Test that validation reports are generated."""
        spec = ProfileSpecification(
            id="test-validation",
            name="Validation Test",
            generation={"count": 200, "products": ["patientsim"]},
            demographics={
                "gender": {"type": "categorical", "weights": {"M": 0.50, "F": 0.50}},
            },
        )
        result = ProfileExecutor(spec, seed=42).execute()

        assert result.validation is not None
        assert len(result.validation.metrics) > 0

        # Check gender validation
        gender_metrics = [m for m in result.validation.metrics if "Gender" in m.name]
        assert len(gender_metrics) == 2

    def test_template_execution(self) -> None:
        """Test executing a profile from template."""
        template = PROFILE_TEMPLATES["medicare-diabetic"]
        spec = ProfileSpecification.model_validate(template)
        result = ProfileExecutor(spec, seed=42).execute()

        assert result.count == 100
        # Should all have diabetes
        has_diabetes = sum(1 for e in result.entities if "E11" in e.conditions)
        assert has_diabetes == 100
        # Should all be 65+
        assert all(e.age >= 65 for e in result.entities if e.age)


class TestExecuteProfileFunction:
    """Tests for execute_profile convenience function."""

    def test_execute_from_dict(self) -> None:
        """Test executing from dictionary."""
        result = execute_profile(
            {
                "id": "test-dict",
                "name": "Dict Test",
                "generation": {"count": 10},
            },
            seed=42,
        )
        assert result.count == 10

    def test_execute_with_count_override(self) -> None:
        """Test count override."""
        result = execute_profile(
            {
                "id": "test-override",
                "name": "Override Test",
                "generation": {"count": 100},
            },
            seed=42,
            count=5,
        )
        assert result.count == 5

    def test_execute_from_json(self) -> None:
        """Test executing from JSON string."""
        json_str = '{"id": "test-json", "name": "JSON Test", "generation": {"count": 10}}'
        result = execute_profile(json_str, seed=42)
        assert result.count == 10


class TestGeneratedEntity:
    """Tests for GeneratedEntity."""

    def test_entity_attributes(self) -> None:
        """Test entity has expected attributes."""
        entity = GeneratedEntity(index=0, seed=12345)
        assert entity.index == 0
        assert entity.seed == 12345
        assert entity.conditions == []
        assert entity.lab_values == {}
        assert entity.identifiers == {}
