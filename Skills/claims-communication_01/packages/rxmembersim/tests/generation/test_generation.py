"""Tests for RxMemberSim generation module."""

import pytest
from datetime import date


class TestRxMemberProfileSpecification:
    """Tests for RxMemberProfileSpecification."""

    def test_basic_profile(self):
        """Test basic profile creation."""
        from rxmembersim.generation.profiles import RxMemberProfileSpecification

        spec = RxMemberProfileSpecification(
            id="test-profile",
            name="Test Profile",
        )
        assert spec.id == "test-profile"
        assert spec.name == "Test Profile"
        assert spec.coverage.coverage_type == "Commercial"

    def test_profile_with_coverage(self):
        """Test profile with custom coverage."""
        from rxmembersim.generation.profiles import (
            RxMemberCoverageSpec,
            RxMemberProfileSpecification,
        )

        spec = RxMemberProfileSpecification(
            id="partd-test",
            name="Part D Test",
            coverage=RxMemberCoverageSpec(
                coverage_type="Medicare Part D",
                bin_number="123456",
            ),
        )
        assert spec.coverage.coverage_type == "Medicare Part D"
        assert spec.coverage.bin_number == "123456"

    def test_to_core_profile(self):
        """Test conversion to core ProfileSpecification."""
        from rxmembersim.generation.profiles import RxMemberProfileSpecification

        spec = RxMemberProfileSpecification(
            id="test",
            name="Test",
        )
        core = spec.to_core_profile()
        assert core.id == "test"
        assert "rx_coverage" in core.custom

    def test_from_core_profile(self):
        """Test creation from core ProfileSpecification."""
        from healthsim.generation.profile_schema import ProfileSpecification
        from rxmembersim.generation.profiles import RxMemberProfileSpecification

        core = ProfileSpecification(
            id="from-core",
            name="From Core",
            custom={"rx_coverage": {"coverage_type": "Medicaid"}},
        )
        rx_spec = RxMemberProfileSpecification.from_core_profile(core)
        assert rx_spec.id == "from-core"
        assert rx_spec.coverage.coverage_type == "Medicaid"


class TestFormularyTierSpec:
    """Tests for FormularyTierSpec."""

    def test_default_weights(self):
        """Test default tier weights."""
        from rxmembersim.generation.profiles import FormularyTierSpec

        spec = FormularyTierSpec()
        assert sum(spec.weights.values()) == pytest.approx(1.0)

    def test_validate_weights(self):
        """Test weight validation."""
        from rxmembersim.generation.profiles import FormularyTierSpec

        spec = FormularyTierSpec(weights={"tier1": 0.5, "tier2": 0.3})
        errors = spec.validate_weights()
        assert len(errors) == 1
        assert "0.8" in errors[0]


class TestTherapyPatternSpec:
    """Tests for TherapyPatternSpec."""

    def test_default_pattern(self):
        """Test default therapy pattern."""
        from rxmembersim.generation.profiles import TherapyPatternSpec

        spec = TherapyPatternSpec()
        assert spec.refill_pattern == "regular"

    def test_custom_adherence(self):
        """Test custom adherence rate."""
        from healthsim.generation.profile_schema import DistributionSpec
        from rxmembersim.generation.profiles import TherapyPatternSpec

        spec = TherapyPatternSpec(
            adherence_rate=DistributionSpec(type="normal", mean=0.90, std_dev=0.05)
        )
        assert spec.adherence_rate.mean == 0.90


class TestRxMemberProfileExecutor:
    """Tests for RxMemberProfileExecutor."""

    def test_basic_execution(self):
        """Test basic profile execution."""
        from rxmembersim.generation.executor import RxMemberProfileExecutor
        from rxmembersim.generation.profiles import RxMemberProfileSpecification

        spec = RxMemberProfileSpecification(
            id="test",
            name="Test",
        )
        spec.generation.count = 10
        spec.generation.seed = 42

        executor = RxMemberProfileExecutor(spec)
        result = executor.execute()

        assert result.count == 10
        assert len(result.rx_members) == 10

    def test_reproducibility(self):
        """Test that same seed produces same results."""
        from rxmembersim.generation.executor import RxMemberProfileExecutor
        from rxmembersim.generation.profiles import RxMemberProfileSpecification

        spec = RxMemberProfileSpecification(id="repro", name="Reproducibility Test")
        spec.generation.count = 5
        spec.generation.seed = 12345

        executor1 = RxMemberProfileExecutor(spec)
        result1 = executor1.execute()

        executor2 = RxMemberProfileExecutor(spec)
        result2 = executor2.execute()

        for m1, m2 in zip(result1.rx_members, result2.rx_members):
            assert m1.rx_member_id == m2.rx_member_id
            assert m1.first_name == m2.first_name
            assert m1.adherence_score == m2.adherence_score

    def test_generated_member_attributes(self):
        """Test that generated members have required attributes."""
        from rxmembersim.generation.executor import RxMemberProfileExecutor
        from rxmembersim.generation.profiles import RxMemberProfileSpecification

        spec = RxMemberProfileSpecification(id="attr-test", name="Attribute Test")
        spec.generation.count = 1
        spec.generation.seed = 42

        executor = RxMemberProfileExecutor(spec)
        result = executor.execute()

        member = result.rx_members[0]
        assert member.rx_member_id
        assert member.first_name
        assert member.last_name
        assert member.bin_number
        assert member.pcn
        assert 0 <= member.adherence_score <= 1


class TestRxMemberProfileTemplates:
    """Tests for profile templates."""

    def test_list_templates(self):
        """Test listing templates."""
        from rxmembersim.generation.templates import list_templates

        templates = list_templates()
        assert len(templates) >= 8  # We defined 8 templates
        
        # Check structure
        for t in templates:
            assert "id" in t
            assert "name" in t
            assert "coverage_type" in t

    def test_get_template(self):
        """Test getting a specific template."""
        from rxmembersim.generation.templates import get_template

        spec = get_template("commercial-healthy")
        assert spec.id == "commercial-healthy"
        assert spec.coverage.coverage_type == "Commercial"

    def test_get_template_not_found(self):
        """Test getting non-existent template."""
        from rxmembersim.generation.templates import get_template

        with pytest.raises(KeyError):
            get_template("not-a-template")

    def test_all_templates_valid(self):
        """Test that all templates produce valid profiles."""
        from rxmembersim.generation.templates import (
            RXMEMBER_PROFILE_TEMPLATES,
            get_template,
        )

        for template_id in RXMEMBER_PROFILE_TEMPLATES.keys():
            spec = get_template(template_id)
            assert spec.id == template_id
            assert spec.name
            # Verify it can be converted to core
            core = spec.to_core_profile()
            assert core.id == template_id


class TestGenerate:
    """Tests for unified generate function."""

    def test_generate_with_template_name(self):
        """Test generate with template name."""
        from rxmembersim.generation import generate

        result = generate("commercial-healthy", count=5, seed=42)
        assert result.count == 5

    def test_generate_with_dict(self):
        """Test generate with inline dict."""
        from rxmembersim.generation import generate

        result = generate(
            {
                "id": "inline-test",
                "name": "Inline Test",
                "generation": {"count": 3, "seed": 42},
            }
        )
        assert result.count == 3

    def test_generate_with_spec(self):
        """Test generate with specification object."""
        from rxmembersim.generation import generate
        from rxmembersim.generation.profiles import RxMemberProfileSpecification

        spec = RxMemberProfileSpecification(
            id="spec-test",
            name="Spec Test",
        )
        spec.generation.count = 7
        spec.generation.seed = 42

        result = generate(spec)
        assert result.count == 7

    def test_quick_sample(self):
        """Test quick_sample convenience function."""
        from rxmembersim.generation import quick_sample

        members = quick_sample(count=3, seed=42)
        assert len(members) == 3
        assert all(m.rx_member_id for m in members)


class TestIntegration:
    """Integration tests."""

    def test_medicare_partd_polypharmacy(self):
        """Test Medicare Part D polypharmacy profile end-to-end."""
        from rxmembersim.generation import generate

        result = generate("medicare-partd-polypharmacy", count=20, seed=42)

        assert result.count == 20
        assert result.validation.passed

        # Check age distribution is reasonable (should be 65+)
        ages = []
        for m in result.rx_members:
            if m.date_of_birth:
                age = (date.today() - m.date_of_birth).days // 365
                ages.append(age)
        
        avg_age = sum(ages) / len(ages)
        assert avg_age > 65, f"Average age {avg_age} should be > 65 for Medicare"

    def test_specialty_oncology(self):
        """Test specialty oncology profile."""
        from rxmembersim.generation import generate

        result = generate("specialty-oncology", count=10, seed=42)
        
        assert result.count == 10
        
        # Should have specialty eligibility
        specialty_eligible = [m for m in result.rx_members if m.specialty_eligible]
        assert len(specialty_eligible) == 10, "All oncology members should be specialty eligible"
