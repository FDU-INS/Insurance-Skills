"""Member-specific profile extensions for MemberSim.

Extends core ProfileSpecification with health plan member attributes
such as plan types, subscriber relationships, and enrollment details.
"""

from __future__ import annotations

from datetime import date
from typing import Any, Literal

from pydantic import BaseModel, Field

from healthsim.generation.profile_schema import (
    ClinicalSpec,
    DemographicsSpec,
    DistributionSpec,
    GenerationSpec,
    OutputSpec,
    ProfileSpecification,
)


class PlanDistributionSpec(BaseModel):
    """Distribution of health plan types."""

    type: Literal["categorical"] = "categorical"
    weights: dict[str, float] = Field(
        default_factory=lambda: {"PPO": 0.40, "HMO": 0.35, "HDHP": 0.25}
    )

    def validate_weights(self) -> list[str]:
        """Validate weights sum to ~1.0."""
        total = sum(self.weights.values())
        if abs(total - 1.0) > 0.01:
            return [f"Plan weights sum to {total}, should be 1.0"]
        return []


class SubscriberRelationshipSpec(BaseModel):
    """Specification for subscriber/dependent relationships."""

    type: Literal["categorical"] = "categorical"
    weights: dict[str, float] = Field(
        default_factory=lambda: {
            "subscriber": 0.45,
            "spouse": 0.25,
            "dependent": 0.30,
        }
    )


class EnrollmentSpec(BaseModel):
    """Enrollment period specification."""

    effective_date: date | None = None
    term_date: date | None = None
    enrollment_duration_months: DistributionSpec | None = None
    auto_renew: bool = True


class MemberCoverageSpec(BaseModel):
    """Member-specific coverage specification.

    Extends base CoverageSpec with plan-specific details.
    """

    coverage_type: str = Field(
        default="Commercial",
        description="Coverage type: Commercial, Medicare, Medicaid, Exchange",
    )
    plan_distribution: PlanDistributionSpec = Field(
        default_factory=PlanDistributionSpec
    )
    relationship_distribution: SubscriberRelationshipSpec = Field(
        default_factory=SubscriberRelationshipSpec
    )
    enrollment: EnrollmentSpec | None = None
    group_id: str | None = None
    group_name: str | None = None


class MemberGenerationSpec(GenerationSpec):
    """Member-specific generation options."""

    generate_subscriber_groups: bool = Field(
        default=False,
        description="If True, generate family/subscriber groups",
    )
    avg_dependents_per_subscriber: float = Field(
        default=1.5,
        ge=0,
        le=10,
    )
    include_quality_gaps: bool = Field(
        default=False,
        description="If True, generate HEDIS quality gaps",
    )


class MemberProfileSpecification(BaseModel):
    """Profile specification extended for health plan members.

    This extends the core ProfileSpecification with member-specific
    attributes like plan types, subscriber relationships, and
    enrollment details.

    Example:
        >>> spec = MemberProfileSpecification(
        ...     id="medicare-advantage-diabetic",
        ...     name="Medicare Advantage Diabetic Members",
        ...     demographics=DemographicsSpec(
        ...         age=DistributionSpec(type="normal", mean=72, std_dev=8, min=65),
        ...     ),
        ...     coverage=MemberCoverageSpec(
        ...         coverage_type="Medicare",
        ...         plan_distribution=PlanDistributionSpec(
        ...             weights={"Medicare Advantage HMO": 0.6, "Medicare Advantage PPO": 0.4}
        ...         ),
        ...     ),
        ... )
    """

    # Core fields (matching ProfileSpecification)
    id: str = Field(..., description="Unique identifier for this profile")
    name: str = Field(..., description="Human-readable name")
    description: str | None = None
    version: str = "1.0"

    # Core specs (inherited pattern)
    demographics: DemographicsSpec | None = None
    clinical: ClinicalSpec | None = None

    # Member-specific
    coverage: MemberCoverageSpec = Field(default_factory=MemberCoverageSpec)
    generation: MemberGenerationSpec = Field(default_factory=MemberGenerationSpec)

    # Journey reference (optional)
    journey: str | dict[str, Any] | None = Field(
        default=None,
        description="Journey template name or inline specification",
    )

    # Output formats (matches core schema)
    outputs: dict[str, OutputSpec] | None = Field(
        default=None,
        description="Output specifications per product",
    )

    # Custom fields for extensibility
    custom: dict[str, Any] = Field(default_factory=dict)

    def to_core_profile(self) -> ProfileSpecification:
        """Convert to core ProfileSpecification for executor compatibility.

        Returns:
            Core ProfileSpecification with member extensions in custom field
        """
        return ProfileSpecification(
            id=self.id,
            name=self.name,
            description=self.description,
            version=self.version,
            demographics=self.demographics,
            clinical=self.clinical,
            generation=GenerationSpec(
                count=self.generation.count,
                seed=self.generation.seed,
                products=self.generation.products or ["membersim"],
            ),
            journey=None,  # Journey handled separately
            outputs=self.outputs,
            custom={
                "member_coverage": self.coverage.model_dump(),
                "member_generation": {
                    "generate_subscriber_groups": self.generation.generate_subscriber_groups,
                    "avg_dependents_per_subscriber": self.generation.avg_dependents_per_subscriber,
                    "include_quality_gaps": self.generation.include_quality_gaps,
                },
                "member_journey": self.journey,
                **self.custom,
            },
        )

    @classmethod
    def from_core_profile(
        cls,
        profile: ProfileSpecification,
    ) -> "MemberProfileSpecification":
        """Create MemberProfileSpecification from core profile.

        Args:
            profile: Core ProfileSpecification

        Returns:
            MemberProfileSpecification with extracted member details
        """
        coverage = MemberCoverageSpec()
        generation = MemberGenerationSpec(
            count=profile.generation.count,
            seed=profile.generation.seed,
            products=profile.generation.products,
        )

        # Extract member-specific from custom if present
        if profile.custom:
            if "member_coverage" in profile.custom:
                coverage = MemberCoverageSpec(**profile.custom["member_coverage"])
            if "member_generation" in profile.custom:
                gen_data = profile.custom["member_generation"]
                generation.generate_subscriber_groups = gen_data.get(
                    "generate_subscriber_groups", False
                )
                generation.avg_dependents_per_subscriber = gen_data.get(
                    "avg_dependents_per_subscriber", 1.5
                )
                generation.include_quality_gaps = gen_data.get(
                    "include_quality_gaps", False
                )

        return cls(
            id=profile.id,
            name=profile.name,
            description=profile.description,
            version=profile.version,
            demographics=profile.demographics,
            clinical=profile.clinical,
            coverage=coverage,
            generation=generation,
            journey=profile.custom.get("member_journey") if profile.custom else None,
            outputs=profile.outputs,
            custom={
                k: v
                for k, v in (profile.custom or {}).items()
                if k not in ("member_coverage", "member_generation", "member_journey")
            },
        )

    def to_json(self) -> str:
        """Serialize to JSON string."""
        return self.model_dump_json(indent=2, exclude_none=True)

    @classmethod
    def from_json(cls, json_str: str) -> "MemberProfileSpecification":
        """Deserialize from JSON string."""
        return cls.model_validate_json(json_str)
