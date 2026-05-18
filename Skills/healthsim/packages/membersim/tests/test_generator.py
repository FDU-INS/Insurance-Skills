"""Tests for MemberGenerator."""

from healthsim.generation import BaseGenerator

from membersim.core.generator import MemberGenerator
from membersim.core.models import ClaimStatus, CoverageType


class TestMemberGenerator:
    """Tests for MemberGenerator."""

    def test_extends_base_generator(self) -> None:
        """Test that MemberGenerator extends BaseGenerator."""
        assert issubclass(MemberGenerator, BaseGenerator)

    def test_seed_reproducibility(self) -> None:
        """Test that same seed produces same results."""
        gen1 = MemberGenerator(seed=42)
        gen2 = MemberGenerator(seed=42)

        member1 = gen1.generate_member()
        member2 = gen2.generate_member()

        assert member1.member_id == member2.member_id
        assert member1.full_name == member2.full_name
        assert member1.birth_date == member2.birth_date

    def test_reset_reproducibility(self) -> None:
        """Test that reset restores initial state."""
        gen = MemberGenerator(seed=42)
        member1 = gen.generate_member()

        gen.reset()
        member2 = gen.generate_member()

        assert member1.member_id == member2.member_id
        assert member1.full_name == member2.full_name

    def test_generate_member(self) -> None:
        """Test basic member generation."""
        gen = MemberGenerator(seed=123)
        member = gen.generate_member()

        assert member.member_id.startswith("M")
        assert member.subscriber_id.startswith("S")
        assert member.given_name
        assert member.family_name
        assert member.birth_date
        assert member.gender in ["M", "F"]
        assert member.age >= 0

    def test_generate_member_age_range(self) -> None:
        """Test member generation with specific age range."""
        gen = MemberGenerator(seed=456)
        member = gen.generate_member(age_range=(25, 35))

        assert 25 <= member.age <= 35

    def test_generate_coverage(self) -> None:
        """Test coverage generation."""
        gen = MemberGenerator(seed=789)
        member = gen.generate_member()
        coverage = gen.generate_coverage(member, CoverageType.MEDICAL)

        assert coverage.coverage_id.startswith("COV")
        assert coverage.member_id == member.member_id
        assert coverage.coverage_type == CoverageType.MEDICAL
        assert coverage.start_date
        assert coverage.deductible is not None
        assert coverage.copay is not None

    def test_generate_enrollment(self) -> None:
        """Test enrollment generation."""
        gen = MemberGenerator(seed=321)
        member = gen.generate_member()
        enrollment = gen.generate_enrollment(member)

        assert enrollment.enrollment_id.startswith("ENR")
        assert enrollment.member_id == member.member_id
        assert enrollment.enrollment_date

    def test_generate_claim(self) -> None:
        """Test claim generation."""
        gen = MemberGenerator(seed=654)
        member = gen.generate_member()
        claim = gen.generate_claim(member, num_lines=3)

        assert claim.claim_id.startswith("CLM")
        assert claim.member_id == member.member_id
        assert claim.service_date
        assert claim.submission_date >= claim.service_date
        assert len(claim.lines) == 3
        assert claim.total_billed > 0
        assert claim.status in ClaimStatus

    def test_generate_member_with_history(self) -> None:
        """Test full member history generation."""
        gen = MemberGenerator(seed=999)
        member, coverages, enrollments, claims = gen.generate_member_with_history(num_claims=10)

        assert member.member_id
        assert len(coverages) == 2  # Medical + Pharmacy
        assert len(enrollments) == 1
        assert len(claims) == 10

        # Verify relationships
        for coverage in coverages:
            assert coverage.member_id == member.member_id
        for enrollment in enrollments:
            assert enrollment.member_id == member.member_id
        for claim in claims:
            assert claim.member_id == member.member_id

    def test_inherited_methods(self) -> None:
        """Test that inherited methods from BaseGenerator work."""
        gen = MemberGenerator(seed=111)

        # Test random_int
        val = gen.random_int(1, 100)
        assert 1 <= val <= 100

        # Test random_choice
        options = ["a", "b", "c"]
        choice = gen.random_choice(options)
        assert choice in options

        # Test random_bool
        result = gen.random_bool(0.5)
        assert isinstance(result, bool)

        # Test faker
        name = gen.faker.first_name()
        assert isinstance(name, str)
