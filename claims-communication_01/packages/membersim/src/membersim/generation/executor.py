"""Member profile executor for MemberSim.

Extends core ProfileExecutor with member-specific generation logic
including plan assignment, subscriber groups, and quality gaps.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import TYPE_CHECKING, Any

from healthsim.generation.profile_executor import (
    ExecutionResult,
    GeneratedEntity,
    HierarchicalSeedManager,
    ProfileExecutor,
    ValidationMetric,
    ValidationReport,
)
from healthsim.generation.profile_schema import ProfileSpecification

from membersim.generation.profiles import (
    MemberCoverageSpec,
    MemberProfileSpecification,
)

if TYPE_CHECKING:
    from membersim.core.member import Member


@dataclass
class GeneratedMember(GeneratedEntity):
    """Extended entity with member-specific attributes."""

    # Plan details
    plan_type: str | None = None
    plan_id: str | None = None

    # Subscriber relationship
    relationship: str | None = None  # subscriber, spouse, dependent
    subscriber_id: str | None = None

    # Coverage details
    coverage_type: str | None = None
    group_id: str | None = None
    effective_date: date | None = None
    term_date: date | None = None

    # Member identifiers
    member_id: str | None = None
    medicaid_id: str | None = None
    medicare_id: str | None = None

    # Quality
    quality_gaps: list[str] = field(default_factory=list)


@dataclass
class MemberExecutionResult:
    """Result of member profile execution."""

    profile_id: str
    seed: int
    count: int
    members: list[GeneratedMember]
    validation: ValidationReport
    duration_seconds: float

    # Member-specific summaries
    plan_distribution: dict[str, int] = field(default_factory=dict)
    relationship_distribution: dict[str, int] = field(default_factory=dict)
    coverage_type_distribution: dict[str, int] = field(default_factory=dict)

    @property
    def subscriber_count(self) -> int:
        """Count of subscribers."""
        return self.relationship_distribution.get("subscriber", 0)

    @property
    def dependent_count(self) -> int:
        """Count of dependents (non-subscribers)."""
        return self.count - self.subscriber_count


class MemberProfileExecutor:
    """Execute member profile specifications to generate health plan members.

    This executor extends the core ProfileExecutor with member-specific logic:
    - Plan type assignment based on distribution
    - Subscriber/dependent relationship management
    - Coverage effective dates
    - Quality gap generation (optional)

    Example:
        >>> spec = MemberProfileSpecification(
        ...     id="commercial-ppo",
        ...     name="Commercial PPO Members",
        ...     generation=MemberGenerationSpec(count=100),
        ... )
        >>> executor = MemberProfileExecutor(spec)
        >>> result = executor.execute()
        >>> print(f"Generated {result.count} members")
    """

    def __init__(
        self,
        profile: MemberProfileSpecification | ProfileSpecification,
        seed: int | None = None,
    ):
        """Initialize executor with profile specification.

        Args:
            profile: Member profile or core profile specification
            seed: Override seed for reproducibility
        """
        # Convert core profile to member profile if needed
        if isinstance(profile, ProfileSpecification):
            self.profile = MemberProfileSpecification.from_core_profile(profile)
        else:
            self.profile = profile

        self.seed = seed or self.profile.generation.seed or random.randint(0, 2**31 - 1)
        self.seed_manager = HierarchicalSeedManager(self.seed)

        # Core executor for base entity generation
        self._core_executor = ProfileExecutor(
            self.profile.to_core_profile(),
            seed=self.seed,
        )

    def execute(
        self,
        count_override: int | None = None,
        dry_run: bool = False,
    ) -> MemberExecutionResult:
        """Execute the profile to generate members.

        Args:
            count_override: Override the count from profile
            dry_run: If True, generate sample only

        Returns:
            MemberExecutionResult with generated members and validation
        """
        import time
        start_time = time.time()

        count = count_override or self.profile.generation.count
        if dry_run:
            count = min(count, 5)

        # Generate base entities using core executor
        core_result = self._core_executor.execute(count_override=count)

        # Extend to members with plan/coverage details
        members: list[GeneratedMember] = []
        plan_counts: dict[str, int] = {}
        relationship_counts: dict[str, int] = {}
        coverage_counts: dict[str, int] = {}

        for entity in core_result.entities:
            member = self._extend_to_member(entity)
            members.append(member)

            # Track distributions
            if member.plan_type:
                plan_counts[member.plan_type] = plan_counts.get(member.plan_type, 0) + 1
            if member.relationship:
                relationship_counts[member.relationship] = (
                    relationship_counts.get(member.relationship, 0) + 1
                )
            if member.coverage_type:
                coverage_counts[member.coverage_type] = (
                    coverage_counts.get(member.coverage_type, 0) + 1
                )

        duration = time.time() - start_time

        # Validate member-specific distributions
        validation = self._validate(members, plan_counts)

        return MemberExecutionResult(
            profile_id=self.profile.id,
            seed=self.seed,
            count=len(members),
            members=members,
            validation=validation,
            duration_seconds=duration,
            plan_distribution=plan_counts,
            relationship_distribution=relationship_counts,
            coverage_type_distribution=coverage_counts,
        )

    def _extend_to_member(self, entity: GeneratedEntity) -> GeneratedMember:
        """Extend a base entity to a full member with plan details.

        Args:
            entity: Base generated entity

        Returns:
            GeneratedMember with plan and coverage details
        """
        rng = self.seed_manager.get_entity_rng(entity.index)
        coverage = self.profile.coverage

        # Sample plan type
        plan_weights = list(coverage.plan_distribution.weights.items())
        plan_type = self._weighted_choice(plan_weights, rng)

        # Sample relationship
        rel_weights = list(coverage.relationship_distribution.weights.items())
        relationship = self._weighted_choice(rel_weights, rng)

        # Generate member ID
        member_id = f"MBR{entity.seed % 10000000:07d}"

        # Generate effective date (within last 3 years)
        today = date.today()
        days_back = rng.randint(0, 3 * 365)
        effective_date = today - timedelta(days=days_back)
        # Align to first of month
        effective_date = effective_date.replace(day=1)

        # Generate group ID for commercial
        group_id = None
        if coverage.coverage_type == "Commercial":
            group_id = coverage.group_id or f"GRP{rng.randint(1000, 9999)}"

        # Generate quality gaps if requested
        quality_gaps = []
        if self.profile.generation.include_quality_gaps:
            quality_gaps = self._generate_quality_gaps(entity, rng)

        return GeneratedMember(
            # Base entity fields
            index=entity.index,
            seed=entity.seed,
            age=entity.age,
            gender=entity.gender,
            birth_date=entity.birth_date,
            race=getattr(entity, "race", None),
            ethnicity=getattr(entity, "ethnicity", None),
            conditions=getattr(entity, "conditions", None),
            # Member-specific
            plan_type=plan_type,
            plan_id=f"PLN-{plan_type[:3].upper()}-{rng.randint(100, 999)}",
            relationship=relationship,
            subscriber_id=member_id if relationship == "subscriber" else None,
            coverage_type=coverage.coverage_type,
            group_id=group_id,
            effective_date=effective_date,
            member_id=member_id,
            quality_gaps=quality_gaps,
        )

    def _weighted_choice(
        self,
        options: list[tuple[str, float]],
        rng: random.Random,
    ) -> str:
        """Select from weighted options.

        Args:
            options: List of (value, weight) tuples
            rng: Random number generator

        Returns:
            Selected value
        """
        total = sum(w for _, w in options)
        r = rng.random() * total
        cumulative = 0.0
        for value, weight in options:
            cumulative += weight
            if r <= cumulative:
                return value
        return options[-1][0]

    def _generate_quality_gaps(
        self,
        entity: GeneratedEntity,
        rng: random.Random,
    ) -> list[str]:
        """Generate HEDIS quality gaps for a member.

        Args:
            entity: Base entity with demographics
            rng: Random number generator

        Returns:
            List of gap measure IDs
        """
        # Common HEDIS measures and their likelihood
        potential_gaps = [
            ("CDC-HbA1c", 0.3),  # Diabetes HbA1c control
            ("CDC-Eye", 0.4),  # Diabetes eye exam
            ("BCS", 0.25),  # Breast cancer screening
            ("COL", 0.35),  # Colorectal cancer screening
            ("AWC", 0.2),  # Adult well-care
            ("CIS", 0.15),  # Childhood immunizations
        ]

        gaps = []
        for measure, probability in potential_gaps:
            # Age-appropriate filtering
            if measure == "BCS" and (
                entity.gender != "F"
                or entity.age is None
                or entity.age < 50
                or entity.age > 74
            ):
                continue
            if measure == "COL" and (entity.age is None or entity.age < 45):
                continue
            if measure == "CIS" and (entity.age is None or entity.age > 2):
                continue
            if measure.startswith("CDC") and not getattr(entity, "conditions", None):
                # Only for diabetics
                continue

            if rng.random() < probability:
                gaps.append(measure)

        return gaps

    def _validate(
        self,
        members: list[GeneratedMember],
        plan_counts: dict[str, int],
    ) -> ValidationReport:
        """Validate generated member distributions.

        Args:
            members: Generated members
            plan_counts: Observed plan distribution

        Returns:
            ValidationReport with metrics
        """
        metrics: list[ValidationMetric] = []
        warnings: list[str] = []
        errors: list[str] = []

        # Validate plan distribution
        expected = self.profile.coverage.plan_distribution.weights
        total = len(members)
        if total > 0:
            for plan, expected_weight in expected.items():
                observed = plan_counts.get(plan, 0)
                observed_weight = observed / total
                deviation = abs(observed_weight - expected_weight)
                tolerance = 0.1  # 10% tolerance

                metrics.append(
                    ValidationMetric(
                        name=f"plan_distribution_{plan}",
                        target=expected_weight,
                        actual=observed_weight,
                        tolerance=tolerance,
                    )
                )

                if not metrics[-1].passed:
                    warnings.append(
                        f"Plan {plan}: expected {expected_weight:.1%}, "
                        f"got {observed_weight:.1%}"
                    )

        return ValidationReport(
            metrics=metrics,
            warnings=warnings,
            errors=errors,
        )
