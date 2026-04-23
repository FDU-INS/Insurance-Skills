"""Tests for MemberSim generation module.

Tests the member-specific profile specifications, executor, templates,
and unified generate() function.
"""

import pytest

from membersim.generation import (
    generate,
    quick_sample,
    get_template,
    list_templates,
    MEMBER_PROFILE_TEMPLATES,
    MemberProfileSpecification,
    MemberProfileExecutor,
    MemberExecutionResult,
    GeneratedMember,
    MemberCoverageSpec,
    MemberGenerationSpec,
    PlanDistributionSpec,
)
from healthsim.generation.profile_schema import (
    DemographicsSpec,
    DistributionSpec,
)


class TestMemberProfileSpecification:
    """Tests for MemberProfileSpecification."""

    def test_create_minimal_spec(self):
        """Test creating a minimal specification."""
        spec = MemberProfileSpecification(
            id="test-profile",
            name="Test Profile",
        )
        assert spec.id == "test-profile"
        assert spec.name == "Test Profile"
        assert spec.coverage.coverage_type == "Commercial"

    def test_create_full_spec(self):
        """Test creating a full specification."""
        spec = MemberProfileSpecification(
            id="full-test",
            name="Full Test Profile",
            demographics=DemographicsSpec(
                age=DistributionSpec(type="normal", mean=45, std_dev=10),
                gender=DistributionSpec(type="categorical", weights={"M": 0.5, "F": 0.5}),
            ),
            coverage=MemberCoverageSpec(
                coverage_type="Medicare",
                plan_distribution=PlanDistributionSpec(
                    weights={"Medicare Advantage HMO": 0.6, "Medicare Advantage PPO": 0.4}
                ),
            ),
            generation=MemberGenerationSpec(count=50, seed=42),
        )
        assert spec.coverage.coverage_type == "Medicare"
        assert spec.generation.count == 50

    def test_to_core_profile(self):
        """Test conversion to core ProfileSpecification."""
        spec = MemberProfileSpecification(
            id="test-convert",
            name="Test Convert",
            coverage=MemberCoverageSpec(coverage_type="Medicaid"),
        )
        core = spec.to_core_profile()
        assert core.id == "test-convert"
        assert "member_coverage" in core.custom
        assert core.custom["member_coverage"]["coverage_type"] == "Medicaid"

    def test_from_core_profile(self):
        """Test creating from core ProfileSpecification."""
        from healthsim.generation.profile_schema import ProfileSpecification

        core = ProfileSpecification(
            id="from-core",
            name="From Core",
            custom={
                "member_coverage": {
                    "coverage_type": "Exchange",
                    "plan_distribution": {"type": "categorical", "weights": {"Silver": 1.0}},
                    "relationship_distribution": {"type": "categorical", "weights": {"subscriber": 1.0}},
                },
            },
        )
        spec = MemberProfileSpecification.from_core_profile(core)
        assert spec.coverage.coverage_type == "Exchange"
        assert spec.id == "from-core"

    def test_json_roundtrip(self):
        """Test JSON serialization roundtrip."""
        spec = MemberProfileSpecification(
            id="json-test",
            name="JSON Test",
            generation=MemberGenerationSpec(count=25),
        )
        json_str = spec.to_json()
        restored = MemberProfileSpecification.from_json(json_str)
        assert restored.id == spec.id
        assert restored.generation.count == 25


class TestMemberProfileExecutor:
    """Tests for MemberProfileExecutor."""

    def test_execute_minimal(self):
        """Test executing a minimal profile."""
        spec = MemberProfileSpecification(
            id="exec-test",
            name="Executor Test",
            generation=MemberGenerationSpec(count=10),
        )
        executor = MemberProfileExecutor(spec, seed=42)
        result = executor.execute()

        assert isinstance(result, MemberExecutionResult)
        assert result.count == 10
        assert len(result.members) == 10
        assert result.profile_id == "exec-test"

    def test_execute_with_demographics(self):
        """Test executing with demographics."""
        spec = MemberProfileSpecification(
            id="demo-test",
            name="Demographics Test",
            demographics=DemographicsSpec(
                age=DistributionSpec(type="normal", mean=50, std_dev=5, min=40, max=60),
                gender=DistributionSpec(type="categorical", weights={"M": 0.5, "F": 0.5}),
            ),
            generation=MemberGenerationSpec(count=20),
        )
        executor = MemberProfileExecutor(spec, seed=42)
        result = executor.execute()

        # Check age bounds
        for member in result.members:
            if member.age is not None:
                assert 40 <= member.age <= 60

    def test_execute_with_plan_distribution(self):
        """Test plan distribution is respected."""
        spec = MemberProfileSpecification(
            id="plan-test",
            name="Plan Test",
            coverage=MemberCoverageSpec(
                plan_distribution=PlanDistributionSpec(
                    weights={"PPO": 0.5, "HMO": 0.5}
                ),
            ),
            generation=MemberGenerationSpec(count=100),
        )
        executor = MemberProfileExecutor(spec, seed=42)
        result = executor.execute()

        # Should have both plan types
        assert "PPO" in result.plan_distribution
        assert "HMO" in result.plan_distribution
        # Rough check on distribution (not exact due to randomness)
        assert result.plan_distribution["PPO"] > 30
        assert result.plan_distribution["HMO"] > 30

    def test_execute_reproducible(self):
        """Test reproducibility with same seed."""
        spec = MemberProfileSpecification(
            id="repro-test",
            name="Reproducibility Test",
            generation=MemberGenerationSpec(count=10),
        )
        result1 = MemberProfileExecutor(spec, seed=42).execute()
        result2 = MemberProfileExecutor(spec, seed=42).execute()

        assert result1.count == result2.count
        for m1, m2 in zip(result1.members, result2.members):
            assert m1.member_id == m2.member_id
            assert m1.plan_type == m2.plan_type

    def test_execute_dry_run(self):
        """Test dry run generates small sample."""
        spec = MemberProfileSpecification(
            id="dry-run-test",
            name="Dry Run Test",
            generation=MemberGenerationSpec(count=1000),
        )
        executor = MemberProfileExecutor(spec, seed=42)
        result = executor.execute(dry_run=True)

        assert result.count == 5  # Max for dry run

    def test_execute_count_override(self):
        """Test count override."""
        spec = MemberProfileSpecification(
            id="override-test",
            name="Override Test",
            generation=MemberGenerationSpec(count=100),
        )
        executor = MemberProfileExecutor(spec, seed=42)
        result = executor.execute(count_override=25)

        assert result.count == 25

    def test_generated_member_has_required_fields(self):
        """Test generated members have required fields."""
        spec = MemberProfileSpecification(
            id="fields-test",
            name="Fields Test",
            generation=MemberGenerationSpec(count=5),
        )
        executor = MemberProfileExecutor(spec, seed=42)
        result = executor.execute()

        for member in result.members:
            assert isinstance(member, GeneratedMember)
            assert member.member_id is not None
            assert member.plan_type is not None
            assert member.relationship is not None
            assert member.coverage_type is not None
            assert member.effective_date is not None


class TestTemplates:
    """Tests for profile templates."""

    def test_templates_exist(self):
        """Test that templates are defined."""
        assert len(MEMBER_PROFILE_TEMPLATES) > 0
        assert "commercial-ppo-healthy" in MEMBER_PROFILE_TEMPLATES
        assert "medicare-advantage-diabetic" in MEMBER_PROFILE_TEMPLATES

    def test_get_template(self):
        """Test getting a template by name."""
        template = get_template("commercial-ppo-healthy")
        assert isinstance(template, MemberProfileSpecification)
        assert template.id == "commercial-ppo-healthy"

    def test_get_template_returns_copy(self):
        """Test that get_template returns a copy."""
        t1 = get_template("commercial-ppo-healthy")
        t2 = get_template("commercial-ppo-healthy")
        t1.generation.count = 999
        assert t2.generation.count != 999

    def test_get_template_not_found(self):
        """Test KeyError for unknown template."""
        with pytest.raises(KeyError, match="Unknown template"):
            get_template("nonexistent-template")

    def test_list_templates(self):
        """Test listing templates."""
        templates = list_templates()
        assert isinstance(templates, list)
        assert len(templates) > 0
        assert all("id" in t and "name" in t for t in templates)

    def test_all_templates_valid(self):
        """Test that all templates can be used."""
        for name, template in MEMBER_PROFILE_TEMPLATES.items():
            assert template.id == name
            # Should be able to convert to core
            core = template.to_core_profile()
            assert core is not None


class TestGenerate:
    """Tests for the unified generate() function."""

    def test_generate_with_template_name(self):
        """Test generate with template name."""
        result = generate("commercial-ppo-healthy", count=10, seed=42)
        assert isinstance(result, MemberExecutionResult)
        assert result.count == 10

    def test_generate_with_spec(self):
        """Test generate with specification object."""
        spec = MemberProfileSpecification(
            id="custom",
            name="Custom",
        )
        result = generate(spec, count=5, seed=42)
        assert result.count == 5
        assert result.profile_id == "custom"

    def test_generate_with_overrides(self):
        """Test generate with field overrides."""
        result = generate(
            "commercial-ppo-healthy",
            count=10,
            seed=42,
            name="Overridden Name",
        )
        assert result.count == 10

    def test_generate_reproducible(self):
        """Test generate reproducibility."""
        result1 = generate("commercial-ppo-healthy", count=10, seed=42)
        result2 = generate("commercial-ppo-healthy", count=10, seed=42)

        assert result1.count == result2.count
        for m1, m2 in zip(result1.members, result2.members):
            assert m1.member_id == m2.member_id

    def test_quick_sample(self):
        """Test quick_sample convenience function."""
        result = quick_sample()
        assert isinstance(result, MemberExecutionResult)
        assert result.count == 10  # Default count

    def test_quick_sample_custom(self):
        """Test quick_sample with custom params."""
        result = quick_sample("medicare-advantage-diabetic", count=5)
        assert result.count == 5


class TestMemberExecutionResult:
    """Tests for MemberExecutionResult properties."""

    def test_subscriber_count(self):
        """Test subscriber count property."""
        from membersim.generation.profiles import SubscriberRelationshipSpec
        
        spec = MemberProfileSpecification(
            id="sub-test",
            name="Subscriber Test",
            coverage=MemberCoverageSpec(
                relationship_distribution=SubscriberRelationshipSpec(
                    weights={"subscriber": 0.5, "spouse": 0.25, "dependent": 0.25}
                ),
            ),
            generation=MemberGenerationSpec(count=100),
        )
        result = generate(spec, seed=42)

        # Should have some subscribers
        assert result.subscriber_count > 0
        assert result.dependent_count > 0
        assert result.subscriber_count + result.dependent_count == result.count

    def test_validation_report(self):
        """Test validation report in result."""
        result = generate("commercial-ppo-healthy", count=50, seed=42)

        assert result.validation is not None
        # Should pass validation
        assert result.validation.passed or len(result.validation.warnings) > 0


class TestIntegration:
    """Integration tests for the full flow."""

    def test_full_flow_commercial(self):
        """Test full generation flow for commercial population."""
        result = generate(
            "commercial-family-mix",
            count=100,
            seed=42,
        )

        assert result.count == 100
        assert result.validation.passed or len(result.validation.errors) == 0

        # Should have distribution across plan types
        assert len(result.plan_distribution) > 1

        # All members should have required fields
        for member in result.members:
            assert member.member_id
            assert member.plan_type
            assert member.effective_date

    def test_full_flow_medicare(self):
        """Test full generation flow for Medicare population."""
        result = generate(
            "medicare-advantage-diabetic",
            count=50,
            seed=42,
        )

        assert result.count == 50
        # Medicare members should all be subscribers
        assert result.subscriber_count == 50

        # Should have quality gaps since template enables them
        members_with_gaps = [m for m in result.members if m.quality_gaps]
        assert len(members_with_gaps) > 0
