"""Tests for profile schema models."""

import pytest
import json
from datetime import datetime

from healthsim.generation.profile_schema import (
    DistributionType,
    DistributionSpec,
    GeographyReference,
    DemographicsSpec,
    ConditionSpec,
    ClinicalSpec,
    CoverageSpec,
    OutputSpec,
    GenerationSpec,
    JourneyReference,
    ProfileSpecification,
    PROFILE_TEMPLATES,
)


# =============================================================================
# DistributionType Tests
# =============================================================================

class TestDistributionType:
    """Tests for DistributionType enum."""

    def test_all_types_defined(self):
        """Test that all expected types are defined."""
        types = [t.value for t in DistributionType]
        
        assert "categorical" in types
        assert "normal" in types
        assert "log_normal" in types
        assert "uniform" in types
        assert "age_bands" in types
        assert "explicit" in types
        assert "conditional" in types


# =============================================================================
# DistributionSpec Tests
# =============================================================================

class TestDistributionSpec:
    """Tests for DistributionSpec model."""

    def test_categorical_spec(self):
        """Test categorical distribution spec."""
        spec = DistributionSpec(
            type=DistributionType.CATEGORICAL,
            weights={"M": 0.48, "F": 0.52}
        )
        
        assert spec.type == DistributionType.CATEGORICAL
        assert spec.weights["M"] == 0.48

    def test_normal_spec(self):
        """Test normal distribution spec."""
        spec = DistributionSpec(
            type=DistributionType.NORMAL,
            mean=72.0,
            std_dev=8.0,
            min=65.0,
            max=95.0
        )
        
        assert spec.mean == 72.0
        assert spec.std_dev == 8.0
        assert spec.min == 65.0
        assert spec.max == 95.0

    def test_age_bands_spec(self):
        """Test age bands distribution spec."""
        spec = DistributionSpec(
            type=DistributionType.AGE_BANDS,
            bands={"0-17": 0.20, "18-64": 0.60, "65+": 0.20}
        )
        
        assert spec.type == DistributionType.AGE_BANDS
        assert "0-17" in spec.bands

    def test_uniform_spec(self):
        """Test uniform distribution spec."""
        spec = DistributionSpec(
            type=DistributionType.UNIFORM,
            min=0.0,
            max=100.0
        )
        
        assert spec.min == 0.0
        assert spec.max == 100.0

    def test_explicit_spec(self):
        """Test explicit distribution spec."""
        spec = DistributionSpec(
            type=DistributionType.EXPLICIT,
            values=[{"value": "TX", "weight": 0.5}, {"value": "CA", "weight": 0.5}]
        )
        
        assert spec.type == DistributionType.EXPLICIT
        assert len(spec.values) == 2

    def test_conditional_spec(self):
        """Test conditional distribution spec."""
        spec = DistributionSpec(
            type=DistributionType.CONDITIONAL,
            rules=[
                {"condition": "severity == 'controlled'", 
                 "distribution": {"type": "normal", "mean": 6.5}}
            ],
            default={"type": "normal", "mean": 7.5}
        )
        
        assert spec.type == DistributionType.CONDITIONAL
        assert len(spec.rules) == 1


# =============================================================================
# GeographyReference Tests
# =============================================================================

class TestGeographyReference:
    """Tests for GeographyReference model."""

    def test_county_reference(self):
        """Test county reference."""
        ref = GeographyReference(
            type="county",
            fips="48201"
        )
        
        assert ref.source == "populationsim"
        assert ref.type == "county"
        assert ref.fips == "48201"

    def test_state_reference(self):
        """Test state reference."""
        ref = GeographyReference(
            type="state",
            state="TX"
        )
        
        assert ref.type == "state"
        assert ref.state == "TX"

    def test_with_datasets(self):
        """Test reference with datasets specified."""
        ref = GeographyReference(
            type="county",
            fips="06037",
            datasets=["acs_demographics", "cdc_places"]
        )
        
        assert len(ref.datasets) == 2
        assert "cdc_places" in ref.datasets


# =============================================================================
# DemographicsSpec Tests
# =============================================================================

class TestDemographicsSpec:
    """Tests for DemographicsSpec model."""

    def test_basic_demographics(self):
        """Test basic demographics specification."""
        demo = DemographicsSpec(
            age=DistributionSpec(type=DistributionType.NORMAL, mean=45.0, std_dev=10.0),
            gender=DistributionSpec(type=DistributionType.CATEGORICAL, 
                                     weights={"M": 0.5, "F": 0.5})
        )
        
        assert demo.age.mean == 45.0
        assert demo.gender.weights["M"] == 0.5

    def test_with_geography(self):
        """Test demographics with geography."""
        demo = DemographicsSpec(
            source="populationsim",
            reference=GeographyReference(type="county", fips="48201")
        )
        
        assert demo.source == "populationsim"
        assert demo.reference.fips == "48201"

    def test_hybrid_demographics(self):
        """Test hybrid demographics (reference + overrides)."""
        demo = DemographicsSpec(
            source="hybrid",
            reference=GeographyReference(type="state", state="TX"),
            age=DistributionSpec(type=DistributionType.NORMAL, mean=72.0, std_dev=8.0, min=65.0)
        )
        
        assert demo.source == "hybrid"
        assert demo.age.min == 65.0


# =============================================================================
# ConditionSpec Tests
# =============================================================================

class TestConditionSpec:
    """Tests for ConditionSpec model."""

    def test_basic_condition(self):
        """Test basic condition specification."""
        cond = ConditionSpec(
            code="E11",
            description="Type 2 diabetes",
            prevalence=0.12
        )
        
        assert cond.code == "E11"
        assert cond.prevalence == 0.12

    def test_default_prevalence(self):
        """Test default prevalence is 1.0."""
        cond = ConditionSpec(code="I10")
        
        assert cond.prevalence == 1.0

    def test_with_severity(self):
        """Test condition with severity distribution."""
        cond = ConditionSpec(
            code="E11",
            severity=DistributionSpec(
                type=DistributionType.CATEGORICAL,
                weights={"mild": 0.4, "moderate": 0.4, "severe": 0.2}
            )
        )
        
        assert cond.severity.weights["severe"] == 0.2


# =============================================================================
# ClinicalSpec Tests
# =============================================================================

class TestClinicalSpec:
    """Tests for ClinicalSpec model."""

    def test_basic_clinical(self):
        """Test basic clinical specification."""
        clinical = ClinicalSpec(
            primary_condition=ConditionSpec(code="E11", prevalence=1.0)
        )
        
        assert clinical.primary_condition.code == "E11"

    def test_with_comorbidities(self):
        """Test clinical with comorbidities."""
        clinical = ClinicalSpec(
            primary_condition=ConditionSpec(code="E11"),
            comorbidities=[
                ConditionSpec(code="I10", prevalence=0.75),
                ConditionSpec(code="E78", prevalence=0.70),
            ]
        )
        
        assert len(clinical.comorbidities) == 2
        assert clinical.comorbidities[0].prevalence == 0.75

    def test_with_lab_values(self):
        """Test clinical with lab values."""
        clinical = ClinicalSpec(
            lab_values={
                "a1c": DistributionSpec(type=DistributionType.NORMAL, mean=7.5, std_dev=1.2),
                "glucose": DistributionSpec(type=DistributionType.NORMAL, mean=140, std_dev=30),
            }
        )
        
        assert clinical.lab_values["a1c"].mean == 7.5


# =============================================================================
# CoverageSpec Tests
# =============================================================================

class TestCoverageSpec:
    """Tests for CoverageSpec model."""

    def test_basic_coverage(self):
        """Test basic coverage specification."""
        coverage = CoverageSpec(type="Medicare")
        
        assert coverage.type == "Medicare"

    def test_with_plan_distribution(self):
        """Test coverage with plan distribution."""
        coverage = CoverageSpec(
            type="Commercial",
            plan_distribution={"PPO": 0.45, "HMO": 0.35, "HDHP": 0.20}
        )
        
        assert sum(coverage.plan_distribution.values()) == 1.0


# =============================================================================
# GenerationSpec Tests
# =============================================================================

class TestGenerationSpec:
    """Tests for GenerationSpec model."""

    def test_defaults(self):
        """Test default values."""
        gen = GenerationSpec()
        
        assert gen.count == 100
        assert gen.products == ["patientsim"]
        assert gen.validation == "strict"

    def test_custom_values(self):
        """Test custom values."""
        gen = GenerationSpec(
            count=500,
            products=["patientsim", "membersim"],
            seed=12345,
            validation="warn"
        )
        
        assert gen.count == 500
        assert gen.seed == 12345

    def test_count_bounds(self):
        """Test count bounds validation."""
        with pytest.raises(ValueError):
            GenerationSpec(count=0)
        
        with pytest.raises(ValueError):
            GenerationSpec(count=200000)


# =============================================================================
# ProfileSpecification Tests
# =============================================================================

class TestProfileSpecification:
    """Tests for ProfileSpecification model."""

    def test_minimal_profile(self):
        """Test minimal valid profile."""
        profile = ProfileSpecification(
            id="test-profile",
            name="Test Profile"
        )
        
        assert profile.id == "test-profile"
        assert profile.version == "1.0"

    def test_id_validation(self):
        """Test ID validation."""
        # Valid IDs
        ProfileSpecification(id="test-profile", name="Test")
        ProfileSpecification(id="test_profile", name="Test")
        ProfileSpecification(id="TestProfile123", name="Test")
        
        # Invalid ID
        with pytest.raises(ValueError):
            ProfileSpecification(id="test profile", name="Test")

    def test_id_lowercase_conversion(self):
        """Test ID is converted to lowercase."""
        profile = ProfileSpecification(id="TestProfile", name="Test")
        
        assert profile.id == "testprofile"

    def test_full_profile(self):
        """Test full profile specification."""
        profile = ProfileSpecification(
            id="medicare-diabetic-001",
            name="Medicare Diabetic Population",
            description="Test population",
            generation=GenerationSpec(count=200, products=["patientsim", "membersim"]),
            demographics=DemographicsSpec(
                age=DistributionSpec(type=DistributionType.NORMAL, mean=72.0, std_dev=8.0)
            ),
            clinical=ClinicalSpec(
                primary_condition=ConditionSpec(code="E11", prevalence=1.0)
            ),
            coverage=CoverageSpec(type="Medicare")
        )
        
        assert profile.generation.count == 200
        assert profile.demographics.age.mean == 72.0
        assert profile.clinical.primary_condition.code == "E11"

    def test_to_json(self):
        """Test JSON serialization."""
        profile = ProfileSpecification(
            id="test-json",
            name="JSON Test",
            generation=GenerationSpec(count=50)
        )
        
        json_str = profile.to_json()
        
        assert "test-json" in json_str
        assert "50" in json_str

    def test_from_json(self):
        """Test JSON deserialization."""
        json_str = '''
        {
            "id": "from-json",
            "name": "From JSON",
            "generation": {"count": 75}
        }
        '''
        
        profile = ProfileSpecification.from_json(json_str)
        
        assert profile.id == "from-json"
        assert profile.generation.count == 75

    def test_get_distribution(self):
        """Test getting distribution by path."""
        profile = ProfileSpecification(
            id="test-dist",
            name="Test",
            demographics=DemographicsSpec(
                age=DistributionSpec(type=DistributionType.NORMAL, mean=45.0, std_dev=10.0)
            )
        )
        
        dist = profile.get_distribution("demographics.age")
        
        assert dist is not None
        assert dist.mean == 45.0

    def test_get_distribution_not_found(self):
        """Test getting distribution that doesn't exist."""
        profile = ProfileSpecification(id="test", name="Test")
        
        dist = profile.get_distribution("demographics.age")
        
        assert dist is None

    def test_with_journey(self):
        """Test profile with journey reference."""
        profile = ProfileSpecification(
            id="test-journey",
            name="Journey Test",
            journey=JourneyReference(template="diabetic_management_year")
        )
        
        assert profile.journey.template == "diabetic_management_year"

    def test_with_outputs(self):
        """Test profile with output specifications."""
        profile = ProfileSpecification(
            id="test-outputs",
            name="Output Test",
            outputs={
                "patientsim": OutputSpec(formats=["fhir_r4", "hl7v2_adt"]),
                "membersim": OutputSpec(formats=["x12_837"]),
            }
        )
        
        assert "fhir_r4" in profile.outputs["patientsim"].formats

    def test_with_custom_fields(self):
        """Test profile with custom extension fields."""
        profile = ProfileSpecification(
            id="test-custom",
            name="Custom Test",
            custom={
                "study_id": "STUDY001",
                "protocol_version": "2.0"
            }
        )
        
        assert profile.custom["study_id"] == "STUDY001"


# =============================================================================
# Profile Templates Tests
# =============================================================================

class TestProfileTemplates:
    """Tests for built-in profile templates."""

    def test_medicare_diabetic_template(self):
        """Test Medicare diabetic template exists and is valid."""
        template = PROFILE_TEMPLATES["medicare-diabetic"]
        
        # Should be parseable
        profile = ProfileSpecification.model_validate(template)
        
        assert profile.id == "medicare-diabetic-template"
        assert profile.clinical.primary_condition.code == "E11"

    def test_commercial_healthy_template(self):
        """Test commercial healthy template."""
        template = PROFILE_TEMPLATES["commercial-healthy"]
        profile = ProfileSpecification.model_validate(template)
        
        assert profile.coverage.type == "Commercial"

    def test_medicaid_pediatric_template(self):
        """Test Medicaid pediatric template."""
        template = PROFILE_TEMPLATES["medicaid-pediatric"]
        profile = ProfileSpecification.model_validate(template)
        
        assert profile.demographics.age.type == DistributionType.AGE_BANDS
        assert "0-2" in profile.demographics.age.bands

    def test_all_templates_valid(self):
        """Test all templates are valid profile specifications."""
        for name, template in PROFILE_TEMPLATES.items():
            profile = ProfileSpecification.model_validate(template)
            assert profile.id is not None
            assert profile.name is not None
