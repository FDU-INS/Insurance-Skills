"""Tests for TrialSim generation module.

Tests the trial-specific profile specifications, executor, templates,
and unified generate() function.
"""

import pytest

from trialsim.generation import (
    generate,
    quick_sample,
    get_template,
    list_templates,
    template_info,
    TRIALSIM_PROFILE_TEMPLATES,
    TrialSimProfileSpecification,
    TrialSimProfileExecutor,
    TrialSimExecutionResult,
    GeneratedSubject,
    ProtocolSpec,
    ArmDistributionSpec,
    TrialSimGenerationSpec,
)
from healthsim.generation.profile_schema import (
    DemographicsSpec,
    DistributionSpec,
)


class TestTrialSimProfileSpecification:
    """Tests for TrialSimProfileSpecification."""

    def test_create_minimal_spec(self):
        """Test creating a minimal specification."""
        spec = TrialSimProfileSpecification(
            id="test-profile",
            name="Test Profile",
        )
        assert spec.id == "test-profile"
        assert spec.name == "Test Profile"

    def test_create_full_spec(self):
        """Test creating a full specification."""
        spec = TrialSimProfileSpecification(
            id="full-test",
            name="Full Test Profile",
            demographics=DemographicsSpec(
                age=DistributionSpec(type="normal", mean=45, std_dev=10),
                gender=DistributionSpec(type="categorical", weights={"M": 0.5, "F": 0.5}),
            ),
            protocol=ProtocolSpec(
                phase="Phase 2",
                therapeutic_area="Oncology",
                indication="Lung Cancer",
                duration_weeks=24,
            ),
            arm_distribution=ArmDistributionSpec(
                weights={"treatment": 0.67, "placebo": 0.33}
            ),
            generation=TrialSimGenerationSpec(count=50, seed=42),
        )
        assert spec.protocol.phase == "Phase 2"
        assert spec.generation.count == 50

    def test_to_core_profile(self):
        """Test conversion to core ProfileSpecification."""
        spec = TrialSimProfileSpecification(
            id="test-convert",
            name="Test Convert",
            protocol=ProtocolSpec(phase="Phase 3"),
        )
        core = spec.to_core_profile()
        assert core.id == "test-convert"
        assert "trial_protocol" in core.custom

    def test_json_roundtrip(self):
        """Test JSON serialization roundtrip."""
        spec = TrialSimProfileSpecification(
            id="json-test",
            name="JSON Test",
            generation=TrialSimGenerationSpec(count=25),
        )
        json_str = spec.to_json()
        restored = TrialSimProfileSpecification.from_json(json_str)
        assert restored.id == spec.id
        assert restored.generation.count == 25


class TestTrialSimProfileExecutor:
    """Tests for TrialSimProfileExecutor."""

    def test_execute_minimal(self):
        """Test executing a minimal profile."""
        spec = TrialSimProfileSpecification(
            id="exec-test",
            name="Executor Test",
            generation=TrialSimGenerationSpec(count=10),
        )
        executor = TrialSimProfileExecutor(spec, seed=42)
        result = executor.execute()

        assert isinstance(result, TrialSimExecutionResult)
        assert result.count == 10
        assert len(result.subjects) == 10
        assert result.profile_id == "exec-test"

    def test_execute_with_demographics(self):
        """Test executing with demographics."""
        spec = TrialSimProfileSpecification(
            id="demo-test",
            name="Demographics Test",
            demographics=DemographicsSpec(
                age=DistributionSpec(type="normal", mean=50, std_dev=5, min=40, max=60),
                gender=DistributionSpec(type="categorical", weights={"M": 0.5, "F": 0.5}),
            ),
            generation=TrialSimGenerationSpec(count=20),
        )
        executor = TrialSimProfileExecutor(spec, seed=42)
        result = executor.execute()

        # Check age bounds
        for subject in result.subjects:
            if subject.age is not None:
                assert 40 <= subject.age <= 60

    def test_execute_with_arm_distribution(self):
        """Test arm distribution is respected."""
        spec = TrialSimProfileSpecification(
            id="arm-test",
            name="Arm Test",
            arm_distribution=ArmDistributionSpec(
                weights={"treatment": 0.5, "placebo": 0.5}
            ),
            generation=TrialSimGenerationSpec(count=100),
        )
        executor = TrialSimProfileExecutor(spec, seed=42)
        result = executor.execute()

        # Should have both arms (arm_counts property)
        assert "treatment" in result.arm_counts
        assert "placebo" in result.arm_counts
        # Rough check on distribution
        assert result.arm_counts["treatment"] > 20
        assert result.arm_counts["placebo"] > 20

    def test_execute_reproducible(self):
        """Test reproducibility with same seed."""
        spec = TrialSimProfileSpecification(
            id="repro-test",
            name="Reproducibility Test",
            generation=TrialSimGenerationSpec(count=10),
        )
        result1 = TrialSimProfileExecutor(spec, seed=42).execute()
        result2 = TrialSimProfileExecutor(spec, seed=42).execute()

        assert result1.count == result2.count
        for s1, s2 in zip(result1.subjects, result2.subjects):
            assert s1.subject_id == s2.subject_id
            assert s1.arm == s2.arm

    def test_execute_dry_run(self):
        """Test dry run generates small sample."""
        spec = TrialSimProfileSpecification(
            id="dry-run-test",
            name="Dry Run Test",
            generation=TrialSimGenerationSpec(count=1000),
        )
        executor = TrialSimProfileExecutor(spec, seed=42)
        result = executor.execute(dry_run=True)

        assert result.count == 5  # Max for dry run

    def test_execute_count_override(self):
        """Test count override."""
        spec = TrialSimProfileSpecification(
            id="override-test",
            name="Override Test",
            generation=TrialSimGenerationSpec(count=100),
        )
        executor = TrialSimProfileExecutor(spec, seed=42)
        result = executor.execute(count_override=25)

        assert result.count == 25

    def test_generated_subject_has_required_fields(self):
        """Test generated subjects have required fields."""
        spec = TrialSimProfileSpecification(
            id="fields-test",
            name="Fields Test",
            generation=TrialSimGenerationSpec(count=5),
        )
        executor = TrialSimProfileExecutor(spec, seed=42)
        result = executor.execute()

        for subject in result.subjects:
            assert isinstance(subject, GeneratedSubject)
            assert subject.subject_id is not None
            assert subject.site_id is not None
            assert subject.screening_date is not None
            # arm may be None for screen-failed subjects
            assert subject.status in ["screen_failed", "enrolled", "randomized"]


class TestTemplates:
    """Tests for profile templates."""

    def test_templates_exist(self):
        """Test that templates are defined."""
        assert len(TRIALSIM_PROFILE_TEMPLATES) > 0
        assert "phase3-oncology-trial" in TRIALSIM_PROFILE_TEMPLATES
        assert "phase2-diabetes-trial" in TRIALSIM_PROFILE_TEMPLATES
        assert "phase1-healthy-volunteers" in TRIALSIM_PROFILE_TEMPLATES

    def test_get_template(self):
        """Test getting a template by name."""
        template = get_template("phase3-oncology-trial")
        assert isinstance(template, TrialSimProfileSpecification)
        assert template.id == "phase3-oncology-trial"

    def test_get_template_returns_copy(self):
        """Test that get_template returns a copy."""
        t1 = get_template("phase3-oncology-trial")
        t2 = get_template("phase3-oncology-trial")
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
        assert "phase3-oncology-trial" in templates
        assert "cvot-trial" in templates

    def test_template_info(self):
        """Test template info function."""
        info = template_info("phase3-oncology-trial")
        assert info["id"] == "phase3-oncology-trial"
        assert "protocol" in info
        assert info["protocol"]["phase"] == "Phase 3"

    def test_all_templates_valid(self):
        """Test that all templates can be used."""
        for name in TRIALSIM_PROFILE_TEMPLATES:
            template = get_template(name)
            assert template.id == name
            # Should be able to convert to core
            core = template.to_core_profile()
            assert core is not None


class TestGenerate:
    """Tests for the unified generate() function."""

    def test_generate_with_template_name(self):
        """Test generate with template name."""
        result = generate("phase3-oncology-trial", count=10, seed=42)
        assert isinstance(result, TrialSimExecutionResult)
        assert result.count == 10

    def test_generate_with_spec(self):
        """Test generate with specification object."""
        spec = TrialSimProfileSpecification(
            id="custom",
            name="Custom",
        )
        result = generate(spec, count=5, seed=42)
        assert result.count == 5
        assert result.profile_id == "custom"

    def test_generate_reproducible(self):
        """Test generate reproducibility."""
        result1 = generate("phase2-diabetes-trial", count=10, seed=42)
        result2 = generate("phase2-diabetes-trial", count=10, seed=42)

        assert result1.count == result2.count
        for s1, s2 in zip(result1.subjects, result2.subjects):
            assert s1.subject_id == s2.subject_id

    def test_quick_sample(self):
        """Test quick_sample convenience function."""
        result = quick_sample()
        assert isinstance(result, TrialSimExecutionResult)
        assert result.count == 10  # Default count

    def test_quick_sample_custom(self):
        """Test quick_sample with custom params."""
        result = quick_sample("cvot-trial", count=5)
        assert result.count == 5


class TestTrialSimExecutionResult:
    """Tests for TrialSimExecutionResult properties."""

    def test_enrolled_count(self):
        """Test enrolled count property."""
        result = generate("phase3-oncology-trial", count=100, seed=42)
        
        # With 25% screening failure rate, expect ~75% enrolled
        assert result.enrolled_count > 0
        assert result.enrolled_count <= result.count

    def test_arm_counts(self):
        """Test arm counts property."""
        result = generate("phase3-oncology-trial", count=100, seed=42)
        
        # Should have both arms
        assert "treatment" in result.arm_counts
        assert "placebo" in result.arm_counts

    def test_validation_report(self):
        """Test validation report in result."""
        result = generate("phase3-oncology-trial", count=50, seed=42)

        assert result.validation is not None


class TestIntegration:
    """Integration tests for the full flow."""

    def test_full_flow_oncology(self):
        """Test full generation flow for oncology trial."""
        result = generate("phase3-oncology-trial", count=100, seed=42)

        assert result.count == 100
        assert result.validation.passed or len(result.validation.errors) == 0

        # Should have distribution across arms
        assert len(result.arm_counts) > 1

        # All subjects should have required fields
        for subject in result.subjects:
            assert subject.subject_id
            assert subject.site_id
            assert subject.screening_date

    def test_full_flow_phase1(self):
        """Test full generation flow for Phase 1 trial."""
        result = generate("phase1-healthy-volunteers", count=48, seed=42)

        assert result.count == 48
        
        # Phase 1 subjects should be younger (healthy volunteers)
        ages = [s.age for s in result.subjects if s.age is not None]
        avg_age = sum(ages) / len(ages) if ages else 0
        assert avg_age < 50  # Healthy volunteers tend to be younger

    def test_full_flow_pediatric(self):
        """Test full generation flow for pediatric trial."""
        result = generate("pediatric-trial", count=50, seed=42)

        assert result.count == 50
        
        # Pediatric subjects should all be under 18
        for subject in result.subjects:
            if subject.age is not None:
                assert subject.age < 18

    def test_multiple_templates_work(self):
        """Test that all templates produce valid output."""
        for template_name in list_templates():
            result = generate(template_name, count=5, seed=42)
            assert result.count == 5
            assert len(result.subjects) == 5
