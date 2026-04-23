"""Tests for profile specification schema."""

import pytest
from datetime import datetime

from healthsim.generation.profile_schema import (
    ClinicalSpec,
    ConditionSpec,
    CoverageSpec,
    DemographicsSpec,
    DistributionSpec,
    DistributionType,
    GenerationSpec,
    GeographyReference,
    OutputSpec,
    ProfileSpecification,
    PROFILE_TEMPLATES,
)


class TestDistributionSpec:
    """Tests for DistributionSpec."""

    def test_categorical_distribution(self) -> None:
        """Test creating categorical distribution."""
        spec = DistributionSpec(
            type=DistributionType.CATEGORICAL,
            weights={"M": 0.48, "F": 0.52},
        )
        assert spec.type == DistributionType.CATEGORICAL
        assert spec.weights == {"M": 0.48, "F": 0.52}

    def test_normal_distribution(self) -> None:
        """Test creating normal distribution."""
        spec = DistributionSpec(
            type=DistributionType.NORMAL,
            mean=72,
            std_dev=8,
            min=65,
            max=95,
        )
        assert spec.type == DistributionType.NORMAL
        assert spec.mean == 72
        assert spec.std_dev == 8

    def test_age_bands_distribution(self) -> None:
        """Test creating age bands distribution."""
        spec = DistributionSpec(
            type=DistributionType.AGE_BANDS,
            bands={"18-34": 0.3, "35-54": 0.4, "55+": 0.3},
        )
        assert spec.type == DistributionType.AGE_BANDS
        assert len(spec.bands) == 3


class TestDemographicsSpec:
    """Tests for DemographicsSpec."""

    def test_creation(self) -> None:
        """Test creating demographics spec."""
        spec = DemographicsSpec(
            age=DistributionSpec(type=DistributionType.NORMAL, mean=45, std_dev=15),
            gender=DistributionSpec(
                type=DistributionType.CATEGORICAL,
                weights={"M": 0.5, "F": 0.5},
            ),
        )
        assert spec.age.mean == 45
        assert spec.gender.weights == {"M": 0.5, "F": 0.5}

    def test_with_geography(self) -> None:
        """Test demographics with geography reference."""
        spec = DemographicsSpec(
            source="populationsim",
            reference=GeographyReference(
                type="county",
                fips="48201",
                datasets=["acs_demographics"],
            ),
        )
        assert spec.source == "populationsim"
        assert spec.reference.fips == "48201"


class TestClinicalSpec:
    """Tests for ClinicalSpec."""

    def test_primary_condition(self) -> None:
        """Test creating clinical spec with primary condition."""
        spec = ClinicalSpec(
            primary_condition=ConditionSpec(
                code="E11",
                description="Type 2 diabetes",
                prevalence=1.0,
            )
        )
        assert spec.primary_condition.code == "E11"

    def test_with_comorbidities(self) -> None:
        """Test clinical spec with comorbidities."""
        spec = ClinicalSpec(
            primary_condition=ConditionSpec(code="E11", prevalence=1.0),
            comorbidities=[
                ConditionSpec(code="I10", description="Hypertension", prevalence=0.75),
                ConditionSpec(code="E78", description="Hyperlipidemia", prevalence=0.70),
            ],
        )
        assert len(spec.comorbidities) == 2
        assert spec.comorbidities[0].prevalence == 0.75


class TestGenerationSpec:
    """Tests for GenerationSpec."""

    def test_defaults(self) -> None:
        """Test default values."""
        spec = GenerationSpec()
        assert spec.count == 100
        assert spec.products == ["patientsim"]
        assert spec.validation == "strict"

    def test_custom_values(self) -> None:
        """Test custom values."""
        spec = GenerationSpec(
            count=500,
            products=["patientsim", "membersim"],
            seed=42,
        )
        assert spec.count == 500
        assert "membersim" in spec.products
        assert spec.seed == 42

    def test_count_bounds(self) -> None:
        """Test count validation."""
        with pytest.raises(ValueError):
            GenerationSpec(count=0)  # Below minimum

        with pytest.raises(ValueError):
            GenerationSpec(count=200000)  # Above maximum


class TestProfileSpecification:
    """Tests for ProfileSpecification."""

    def test_minimal_profile(self) -> None:
        """Test creating minimal valid profile."""
        profile = ProfileSpecification(
            id="test-profile-001",
            name="Test Profile",
        )
        assert profile.id == "test-profile-001"
        assert profile.generation.count == 100

    def test_complete_profile(self) -> None:
        """Test creating complete profile."""
        profile = ProfileSpecification(
            id="complete-profile-001",
            name="Complete Test Profile",
            version="1.0",
            description="A complete profile for testing",
            generation=GenerationSpec(count=200, products=["patientsim", "membersim"]),
            demographics=DemographicsSpec(
                age=DistributionSpec(type=DistributionType.NORMAL, mean=72, std_dev=8),
                gender=DistributionSpec(
                    type=DistributionType.CATEGORICAL,
                    weights={"M": 0.48, "F": 0.52},
                ),
            ),
            clinical=ClinicalSpec(
                primary_condition=ConditionSpec(code="E11", prevalence=1.0)
            ),
            coverage=CoverageSpec(type="Medicare"),
        )

        assert profile.generation.count == 200
        assert profile.demographics.age.mean == 72
        assert profile.clinical.primary_condition.code == "E11"

    def test_id_validation(self) -> None:
        """Test ID must be lowercase with hyphens."""
        # Valid IDs
        profile = ProfileSpecification(id="valid-id-123", name="Test")
        assert profile.id == "valid-id-123"

        # Uppercase gets lowercased
        profile = ProfileSpecification(id="UPPER-CASE", name="Test")
        assert profile.id == "upper-case"

    def test_to_json(self) -> None:
        """Test JSON serialization."""
        profile = ProfileSpecification(
            id="json-test-001",
            name="JSON Test",
            generation=GenerationSpec(count=50),
        )

        json_str = profile.to_json()
        assert '"id": "json-test-001"' in json_str
        assert '"count": 50' in json_str

    def test_from_json(self) -> None:
        """Test JSON deserialization."""
        json_str = '''
        {
            "id": "from-json-001",
            "name": "From JSON Test",
            "generation": {"count": 75}
        }
        '''

        profile = ProfileSpecification.from_json(json_str)
        assert profile.id == "from-json-001"
        assert profile.generation.count == 75

    def test_roundtrip(self) -> None:
        """Test JSON roundtrip (serialize and deserialize)."""
        original = ProfileSpecification(
            id="roundtrip-001",
            name="Roundtrip Test",
            generation=GenerationSpec(count=100, products=["patientsim"]),
            demographics=DemographicsSpec(
                age=DistributionSpec(type=DistributionType.NORMAL, mean=50, std_dev=10)
            ),
        )

        json_str = original.to_json()
        restored = ProfileSpecification.from_json(json_str)

        assert restored.id == original.id
        assert restored.generation.count == original.generation.count
        assert restored.demographics.age.mean == original.demographics.age.mean


class TestProfileTemplates:
    """Tests for profile templates."""

    def test_medicare_diabetic_template(self) -> None:
        """Test medicare diabetic template is valid."""
        template = PROFILE_TEMPLATES["medicare-diabetic"]
        profile = ProfileSpecification.model_validate(template)

        assert profile.id == "medicare-diabetic-template"
        assert profile.clinical.primary_condition.code == "E11"
        assert len(profile.clinical.comorbidities) == 2

    def test_commercial_healthy_template(self) -> None:
        """Test commercial healthy template is valid."""
        template = PROFILE_TEMPLATES["commercial-healthy"]
        profile = ProfileSpecification.model_validate(template)

        assert profile.id == "commercial-healthy-template"
        assert profile.demographics.age.mean == 38

    def test_medicaid_pediatric_template(self) -> None:
        """Test medicaid pediatric template is valid."""
        template = PROFILE_TEMPLATES["medicaid-pediatric"]
        profile = ProfileSpecification.model_validate(template)

        assert profile.id == "medicaid-pediatric-template"
        assert profile.demographics.age.type == DistributionType.AGE_BANDS
