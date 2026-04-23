"""Pharmacy member-specific profile extensions for RxMemberSim.

Extends core ProfileSpecification with pharmacy benefit attributes
such as formulary tiers, pharmacy preferences, and therapy patterns.
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


class FormularyTierSpec(BaseModel):
    """Distribution of formulary tier utilization."""

    type: Literal["categorical"] = "categorical"
    weights: dict[str, float] = Field(
        default_factory=lambda: {
            "tier1_generic": 0.50,
            "tier2_preferred_brand": 0.30,
            "tier3_non_preferred": 0.15,
            "tier4_specialty": 0.05,
        }
    )

    def validate_weights(self) -> list[str]:
        """Validate weights sum to ~1.0."""
        total = sum(self.weights.values())
        if abs(total - 1.0) > 0.01:
            return [f"Tier weights sum to {total}, should be 1.0"]
        return []


class PharmacyPreferenceSpec(BaseModel):
    """Pharmacy channel preferences."""

    type: Literal["categorical"] = "categorical"
    weights: dict[str, float] = Field(
        default_factory=lambda: {
            "retail": 0.60,
            "mail_order": 0.25,
            "specialty": 0.10,
            "ltc": 0.05,
        }
    )


class TherapyPatternSpec(BaseModel):
    """Therapy adherence and pattern specification."""

    adherence_rate: DistributionSpec = Field(
        default_factory=lambda: DistributionSpec(
            type="normal", mean=0.75, std_dev=0.15, min=0.0, max=1.0
        )
    )
    avg_therapies_per_member: DistributionSpec = Field(
        default_factory=lambda: DistributionSpec(
            type="normal", mean=3.0, std_dev=1.5, min=1, max=15
        )
    )
    refill_pattern: Literal["regular", "sporadic", "stockpile"] = "regular"


class RxEnrollmentSpec(BaseModel):
    """Pharmacy benefit enrollment specification."""

    effective_date: date | None = None
    term_date: date | None = None
    pbm_name: str | None = None
    formulary_id: str | None = None
    network_id: str | None = None


class RxMemberCoverageSpec(BaseModel):
    """Pharmacy-specific coverage specification."""

    coverage_type: str = Field(
        default="Commercial",
        description="Coverage type: Commercial, Medicare Part D, Medicaid, Exchange",
    )
    formulary_tier_distribution: FormularyTierSpec = Field(
        default_factory=FormularyTierSpec
    )
    pharmacy_preference: PharmacyPreferenceSpec = Field(
        default_factory=PharmacyPreferenceSpec
    )
    therapy_pattern: TherapyPatternSpec = Field(
        default_factory=TherapyPatternSpec
    )
    enrollment: RxEnrollmentSpec | None = None
    group_id: str | None = None
    bin_number: str | None = None
    pcn: str | None = None


class RxMemberGenerationSpec(GenerationSpec):
    """Pharmacy member-specific generation options."""

    generate_claim_history: bool = Field(
        default=True,
        description="If True, generate historical pharmacy claims",
    )
    history_months: int = Field(
        default=12,
        ge=0,
        le=60,
        description="Months of claim history to generate",
    )
    include_specialty_rx: bool = Field(
        default=False,
        description="If True, include specialty pharmacy claims",
    )
    include_dur_alerts: bool = Field(
        default=True,
        description="If True, generate DUR (Drug Utilization Review) alerts",
    )


class RxMemberProfileSpecification(BaseModel):
    """Profile specification extended for pharmacy benefit members.

    This extends the core ProfileSpecification with pharmacy-specific
    attributes like formulary tiers, pharmacy preferences, and
    therapy patterns.

    Example:
        >>> spec = RxMemberProfileSpecification(
        ...     id="medicare-partd-polypharmacy",
        ...     name="Medicare Part D Polypharmacy Members",
        ...     demographics=DemographicsSpec(
        ...         age=DistributionSpec(type="normal", mean=75, std_dev=7, min=65),
        ...     ),
        ...     coverage=RxMemberCoverageSpec(
        ...         coverage_type="Medicare Part D",
        ...         therapy_pattern=TherapyPatternSpec(
        ...             avg_therapies_per_member=DistributionSpec(
        ...                 type="normal", mean=8.0, std_dev=2.0, min=5
        ...             )
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

    # Pharmacy-specific
    coverage: RxMemberCoverageSpec = Field(default_factory=RxMemberCoverageSpec)
    generation: RxMemberGenerationSpec = Field(default_factory=RxMemberGenerationSpec)

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
        """Convert to core ProfileSpecification for executor compatibility."""
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
                products=self.generation.products or ["rxmembersim"],
            ),
            journey=None,
            outputs=self.outputs,
            custom={
                "rx_coverage": self.coverage.model_dump(),
                "rx_generation": {
                    "generate_claim_history": self.generation.generate_claim_history,
                    "history_months": self.generation.history_months,
                    "include_specialty_rx": self.generation.include_specialty_rx,
                    "include_dur_alerts": self.generation.include_dur_alerts,
                },
                "rx_journey": self.journey,
                **self.custom,
            },
        )

    @classmethod
    def from_core_profile(
        cls,
        profile: ProfileSpecification,
    ) -> "RxMemberProfileSpecification":
        """Create RxMemberProfileSpecification from core profile."""
        coverage = RxMemberCoverageSpec()
        generation = RxMemberGenerationSpec(
            count=profile.generation.count,
            seed=profile.generation.seed,
            products=profile.generation.products,
        )

        if profile.custom:
            if "rx_coverage" in profile.custom:
                coverage = RxMemberCoverageSpec(**profile.custom["rx_coverage"])
            if "rx_generation" in profile.custom:
                gen_data = profile.custom["rx_generation"]
                generation.generate_claim_history = gen_data.get(
                    "generate_claim_history", True
                )
                generation.history_months = gen_data.get("history_months", 12)
                generation.include_specialty_rx = gen_data.get(
                    "include_specialty_rx", False
                )
                generation.include_dur_alerts = gen_data.get("include_dur_alerts", True)

        return cls(
            id=profile.id,
            name=profile.name,
            description=profile.description,
            version=profile.version,
            demographics=profile.demographics,
            clinical=profile.clinical,
            coverage=coverage,
            generation=generation,
            journey=profile.custom.get("rx_journey") if profile.custom else None,
            outputs=profile.outputs,
            custom={
                k: v
                for k, v in (profile.custom or {}).items()
                if k not in ("rx_coverage", "rx_generation", "rx_journey")
            },
        )

    def to_json(self) -> str:
        """Serialize to JSON string."""
        return self.model_dump_json(indent=2, exclude_none=True)

    @classmethod
    def from_json(cls, json_str: str) -> "RxMemberProfileSpecification":
        """Deserialize from JSON string."""
        return cls.model_validate_json(json_str)
