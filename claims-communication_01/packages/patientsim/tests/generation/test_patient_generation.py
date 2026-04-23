"""Tests for PatientSim generation module.

Tests the patient-specific profile specifications, executor, templates,
and unified generate() function.
"""

import pytest

from patientsim.generation import (
    generate,
    quick_sample,
    get_template,
    list_templates,
    PATIENT_PROFILE_TEMPLATES,
    PatientProfileSpecification,
    PatientProfileExecutor,
    PatientExecutionResult,
    GeneratedPatient,
    PatientClinicalSpec,
    PatientDemographicsSpec,
    PatientGenerationSpec,
)


class TestPatientProfileSpecification:
    """Tests for PatientProfileSpecification."""

    def test_create_minimal_spec(self):
        """Test creating a minimal specification."""
        spec = PatientProfileSpecification(
            id="test-profile",
            name="Test Profile",
        )
        assert spec.id == "test-profile"
        assert spec.name == "Test Profile"

    def test_create_full_spec(self):
        """Test creating a full specification."""
        spec = PatientProfileSpecification(
            id="full-test",
            name="Full Test Profile",
            demographics=PatientDemographicsSpec(
                age={"type": "normal", "mean": 45, "std": 10},
                gender={"type": "categorical", "weights": {"M": 0.5, "F": 0.5}},
            ),
            clinical=PatientClinicalSpec(
                primary_condition={"code": "E11.9", "description": "Type 2 diabetes"},
            ),
            generation=PatientGenerationSpec(count=50, seed=42),
        )
        assert spec.generation.count == 50
        assert spec.clinical.primary_condition.code == "E11.9"

    def test_json_roundtrip(self):
        """Test JSON serialization roundtrip."""
        spec = PatientProfileSpecification(
            id="json-test",
            name="JSON Test",
            generation=PatientGenerationSpec(count=25),
        )
        json_str = spec.to_json()
        restored = PatientProfileSpecification.from_json(json_str)
        assert restored.id == spec.id
        assert restored.generation.count == 25

    def test_model_copy(self):
        """Test model copy creates independent copy."""
        spec = PatientProfileSpecification(
            id="copy-test",
            name="Copy Test",
            generation=PatientGenerationSpec(count=100),
        )
        copy = spec.model_copy(deep=True)
        copy.generation.count = 999
        assert spec.generation.count == 100


class TestPatientProfileExecutor:
    """Tests for PatientProfileExecutor."""

    def test_execute_minimal(self):
        """Test executing a minimal profile."""
        spec = PatientProfileSpecification(
            id="exec-test",
            name="Executor Test",
            generation=PatientGenerationSpec(count=10),
        )
        executor = PatientProfileExecutor(spec, seed=42)
        result = executor.execute()

        assert isinstance(result, PatientExecutionResult)
        assert result.count == 10
        assert len(result.patients) == 10
        assert result.profile_id == "exec-test"

    def test_execute_with_demographics(self):
        """Test executing with demographics."""
        spec = PatientProfileSpecification(
            id="demo-test",
            name="Demographics Test",
            demographics=PatientDemographicsSpec(
                age={"type": "normal", "mean": 50, "std": 5, "min": 40, "max": 60},
                gender={"type": "categorical", "weights": {"M": 0.5, "F": 0.5}},
            ),
            generation=PatientGenerationSpec(count=20),
        )
        executor = PatientProfileExecutor(spec, seed=42)
        result = executor.execute()

        # Check age bounds
        for patient in result.patients:
            if patient.age is not None:
                assert 40 <= patient.age <= 60

    def test_execute_reproducible(self):
        """Test reproducibility with same seed."""
        spec = PatientProfileSpecification(
            id="repro-test",
            name="Reproducibility Test",
            generation=PatientGenerationSpec(count=10),
        )
        result1 = PatientProfileExecutor(spec, seed=42).execute()
        result2 = PatientProfileExecutor(spec, seed=42).execute()

        assert result1.count == result2.count
        for p1, p2 in zip(result1.patients, result2.patients):
            assert p1.mrn == p2.mrn
            assert p1.gender == p2.gender

    def test_execute_dry_run(self):
        """Test dry run generates small sample."""
        spec = PatientProfileSpecification(
            id="dry-run-test",
            name="Dry Run Test",
            generation=PatientGenerationSpec(count=1000),
        )
        executor = PatientProfileExecutor(spec, seed=42)
        result = executor.execute(dry_run=True)

        assert result.count == 5  # Max for dry run

    def test_execute_count_override(self):
        """Test count override."""
        spec = PatientProfileSpecification(
            id="override-test",
            name="Override Test",
            generation=PatientGenerationSpec(count=100),
        )
        executor = PatientProfileExecutor(spec, seed=42)
        result = executor.execute(count_override=25)

        assert result.count == 25

    def test_generated_patient_has_required_fields(self):
        """Test generated patients have required fields."""
        spec = PatientProfileSpecification(
            id="fields-test",
            name="Fields Test",
            generation=PatientGenerationSpec(count=5),
        )
        executor = PatientProfileExecutor(spec, seed=42)
        result = executor.execute()

        for patient in result.patients:
            assert isinstance(patient, GeneratedPatient)
            assert patient.mrn is not None
            assert patient.first_name is not None
            assert patient.last_name is not None
            assert patient.gender is not None
            assert patient.date_of_birth is not None


class TestTemplates:
    """Tests for profile templates."""

    def test_templates_exist(self):
        """Test that templates are defined."""
        assert len(PATIENT_PROFILE_TEMPLATES) > 0
        assert "diabetic-senior" in PATIENT_PROFILE_TEMPLATES
        assert "healthy-adult" in PATIENT_PROFILE_TEMPLATES
        assert "pediatric-asthma" in PATIENT_PROFILE_TEMPLATES

    def test_get_template(self):
        """Test getting a template by name."""
        template = get_template("diabetic-senior")
        assert isinstance(template, PatientProfileSpecification)
        assert template.id == "diabetic-senior"

    def test_get_template_returns_copy(self):
        """Test that get_template returns a copy."""
        t1 = get_template("diabetic-senior")
        t2 = get_template("diabetic-senior")
        t1.generation.count = 999
        assert t2.generation.count != 999

    def test_get_template_not_found(self):
        """Test KeyError for unknown template."""
        with pytest.raises(KeyError):
            get_template("nonexistent-template")

    def test_list_templates(self):
        """Test listing templates."""
        templates = list_templates()
        assert isinstance(templates, list)
        assert len(templates) > 0
        assert "diabetic-senior" in templates
        assert "oncology" in templates

    def test_all_templates_can_be_retrieved(self):
        """Test that all templates can be retrieved."""
        for name in PATIENT_PROFILE_TEMPLATES:
            template = get_template(name)
            assert template.id == name


class TestGenerate:
    """Tests for the unified generate() function."""

    def test_generate_with_template_name(self):
        """Test generate with template name."""
        result = generate("healthy-adult", count=10, seed=42)
        assert isinstance(result, PatientExecutionResult)
        assert result.count == 10

    def test_generate_with_spec(self):
        """Test generate with specification object."""
        spec = PatientProfileSpecification(
            id="custom",
            name="Custom",
        )
        result = generate(spec, count=5, seed=42)
        assert result.count == 5
        assert result.profile_id == "custom"

    def test_generate_reproducible(self):
        """Test generate reproducibility."""
        result1 = generate("healthy-adult", count=10, seed=42)
        result2 = generate("healthy-adult", count=10, seed=42)

        assert result1.count == result2.count
        for p1, p2 in zip(result1.patients, result2.patients):
            assert p1.mrn == p2.mrn

    def test_quick_sample_returns_list(self):
        """Test quick_sample returns list of patients."""
        patients = quick_sample(count=10)
        assert isinstance(patients, list)
        assert len(patients) == 10
        assert all(isinstance(p, GeneratedPatient) for p in patients)

    def test_quick_sample_with_template(self):
        """Test quick_sample with custom template."""
        patients = quick_sample(count=5, template="oncology")
        assert len(patients) == 5


class TestIntegration:
    """Integration tests for the full flow."""

    def test_full_flow_custom_spec(self):
        """Test full generation flow with custom spec."""
        spec = PatientProfileSpecification(
            id="integration-test",
            name="Integration Test",
            demographics=PatientDemographicsSpec(
                age={"type": "uniform", "min": 30, "max": 50},
            ),
            generation=PatientGenerationSpec(count=50),
        )
        result = generate(spec, seed=42)

        assert result.count == 50
        assert result.validation.passed or len(result.validation.errors) == 0

        # All patients should have required fields
        for patient in result.patients:
            assert patient.mrn
            assert patient.first_name
            assert patient.date_of_birth

    def test_full_flow_healthy_adult(self):
        """Test full generation flow for healthy adult template."""
        result = generate("healthy-adult", count=30, seed=42)

        assert result.count == 30
        
        # All patients should have required fields
        for patient in result.patients:
            assert patient.mrn
            assert patient.first_name

    def test_multiple_templates_work(self):
        """Test that several templates produce valid output."""
        for template_name in ["healthy-adult", "diabetic-senior", "oncology"]:
            result = generate(template_name, count=5, seed=42)
            assert result.count == 5
            assert len(result.patients) == 5
