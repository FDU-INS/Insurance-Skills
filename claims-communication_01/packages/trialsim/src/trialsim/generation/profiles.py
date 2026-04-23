"""Clinical trial subject profile extensions for TrialSim.

Extends core ProfileSpecification with clinical trial attributes
such as protocol assignment, arm randomization, and visit compliance.
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


class ProtocolSpec(BaseModel):
    """Protocol and study design specification."""

    protocol_id: str | None = Field(
        default=None,
        description="Protocol identifier (auto-generated if not provided)",
    )
    phase: Literal["Phase 1", "Phase 2", "Phase 3", "Phase 4"] = Field(
        default="Phase 3",
        description="Clinical trial phase",
    )
    therapeutic_area: str = Field(
        default="Oncology",
        description="Therapeutic area (e.g., Oncology, Cardiology, Neurology)",
    )
    indication: str | None = Field(
        default=None,
        description="Target indication (e.g., Type 2 Diabetes, NSCLC)",
    )
    duration_weeks: int = Field(
        default=52,
        ge=1,
        le=520,
        description="Study duration in weeks",
    )


class ArmDistributionSpec(BaseModel):
    """Treatment arm randomization distribution."""

    type: Literal["categorical"] = "categorical"
    weights: dict[str, float] = Field(
        default_factory=lambda: {
            "treatment": 0.67,
            "placebo": 0.33,
        },
        description="Randomization weights per arm",
    )

    def validate_weights(self) -> list[str]:
        """Validate weights sum to ~1.0."""
        total = sum(self.weights.values())
        if abs(total - 1.0) > 0.01:
            return [f"Arm weights sum to {total}, should be 1.0"]
        return []


class VisitComplianceSpec(BaseModel):
    """Visit attendance and compliance specification."""

    attendance_rate: DistributionSpec = Field(
        default_factory=lambda: DistributionSpec(
            type="normal", mean=0.90, std_dev=0.08, min=0.5, max=1.0
        ),
        description="Probability of attending scheduled visits",
    )
    window_adherence: DistributionSpec = Field(
        default_factory=lambda: DistributionSpec(
            type="normal", mean=0.85, std_dev=0.10, min=0.0, max=1.0
        ),
        description="Probability of visiting within protocol window",
    )


class AdverseEventSpec(BaseModel):
    """Adverse event generation specification."""

    ae_probability: float = Field(
        default=0.30,
        ge=0.0,
        le=1.0,
        description="Base probability of experiencing any AE",
    )
    serious_ae_probability: float = Field(
        default=0.05,
        ge=0.0,
        le=1.0,
        description="Probability of SAE given AE occurs",
    )
    severity_distribution: DistributionSpec = Field(
        default_factory=lambda: DistributionSpec(
            type="categorical",
            weights={
                "grade_1_mild": 0.50,
                "grade_2_moderate": 0.30,
                "grade_3_severe": 0.15,
                "grade_4_life_threatening": 0.04,
                "grade_5_death": 0.01,
            },
        ),
        description="Severity grade distribution",
    )


class ExposureComplianceSpec(BaseModel):
    """Drug exposure and treatment compliance specification."""

    compliance_rate: DistributionSpec = Field(
        default_factory=lambda: DistributionSpec(
            type="normal", mean=0.85, std_dev=0.12, min=0.0, max=1.0
        ),
        description="Treatment compliance rate",
    )
    discontinuation_rate: float = Field(
        default=0.15,
        ge=0.0,
        le=1.0,
        description="Probability of early discontinuation",
    )
    discontinuation_reasons: DistributionSpec = Field(
        default_factory=lambda: DistributionSpec(
            type="categorical",
            weights={
                "adverse_event": 0.35,
                "lack_of_efficacy": 0.25,
                "withdrawal_of_consent": 0.20,
                "protocol_deviation": 0.10,
                "lost_to_followup": 0.10,
            },
        ),
        description="Reasons for early discontinuation",
    )


class EnrollmentSpec(BaseModel):
    """Subject enrollment specification."""

    screening_failure_rate: float = Field(
        default=0.20,
        ge=0.0,
        le=1.0,
        description="Probability of screen failure",
    )
    screening_failure_reasons: DistributionSpec = Field(
        default_factory=lambda: DistributionSpec(
            type="categorical",
            weights={
                "inclusion_criteria": 0.40,
                "exclusion_criteria": 0.30,
                "consent_withdrawn": 0.15,
                "lab_abnormality": 0.10,
                "other": 0.05,
            },
        ),
        description="Reasons for screening failure",
    )
    enrollment_start: date | None = None
    enrollment_end: date | None = None


class SiteSpec(BaseModel):
    """Site distribution and characteristics."""

    num_sites: int = Field(
        default=10,
        ge=1,
        le=500,
        description="Number of trial sites",
    )
    subjects_per_site: DistributionSpec = Field(
        default_factory=lambda: DistributionSpec(
            type="normal", mean=10.0, std_dev=5.0, min=1, max=50
        ),
        description="Subjects enrolled per site",
    )
    region_distribution: DistributionSpec = Field(
        default_factory=lambda: DistributionSpec(
            type="categorical",
            weights={
                "North America": 0.40,
                "Europe": 0.35,
                "Asia Pacific": 0.20,
                "Latin America": 0.05,
            },
        ),
        description="Geographic distribution of sites",
    )


class TrialSimGenerationSpec(GenerationSpec):
    """Clinical trial-specific generation options."""

    generate_visit_records: bool = Field(
        default=True,
        description="If True, generate visit records per protocol schedule",
    )
    generate_adverse_events: bool = Field(
        default=True,
        description="If True, generate adverse event records",
    )
    generate_exposures: bool = Field(
        default=True,
        description="If True, generate drug exposure records",
    )
    export_sdtm: bool = Field(
        default=False,
        description="If True, generate SDTM datasets on execution",
    )


class TrialSimProfileSpecification(BaseModel):
    """Profile specification extended for clinical trial subjects.

    This extends the core ProfileSpecification with trial-specific
    attributes like protocol design, arm randomization, and
    adverse event patterns.

    Example:
        >>> spec = TrialSimProfileSpecification(
        ...     id="phase3-oncology-trial",
        ...     name="Phase 3 Oncology Trial Subjects",
        ...     demographics=DemographicsSpec(
        ...         age=DistributionSpec(type="normal", mean=62, std_dev=10, min=18),
        ...     ),
        ...     protocol=ProtocolSpec(
        ...         phase="Phase 3",
        ...         therapeutic_area="Oncology",
        ...         indication="NSCLC",
        ...         duration_weeks=52,
        ...     ),
        ...     arm_distribution=ArmDistributionSpec(
        ...         weights={"treatment": 0.67, "placebo": 0.33}
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

    # Trial-specific
    protocol: ProtocolSpec = Field(default_factory=ProtocolSpec)
    arm_distribution: ArmDistributionSpec = Field(default_factory=ArmDistributionSpec)
    enrollment: EnrollmentSpec = Field(default_factory=EnrollmentSpec)
    sites: SiteSpec = Field(default_factory=SiteSpec)
    visit_compliance: VisitComplianceSpec = Field(default_factory=VisitComplianceSpec)
    adverse_events: AdverseEventSpec = Field(default_factory=AdverseEventSpec)
    exposure_compliance: ExposureComplianceSpec = Field(
        default_factory=ExposureComplianceSpec
    )
    generation: TrialSimGenerationSpec = Field(default_factory=TrialSimGenerationSpec)

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
                products=self.generation.products or ["trialsim"],
            ),
            journey=None,
            outputs=self.outputs,
            custom={
                "trial_protocol": self.protocol.model_dump(),
                "trial_arm_distribution": self.arm_distribution.model_dump(),
                "trial_enrollment": self.enrollment.model_dump(),
                "trial_sites": self.sites.model_dump(),
                "trial_visit_compliance": self.visit_compliance.model_dump(),
                "trial_adverse_events": self.adverse_events.model_dump(),
                "trial_exposure_compliance": self.exposure_compliance.model_dump(),
                "trial_generation": {
                    "generate_visit_records": self.generation.generate_visit_records,
                    "generate_adverse_events": self.generation.generate_adverse_events,
                    "generate_exposures": self.generation.generate_exposures,
                    "export_sdtm": self.generation.export_sdtm,
                },
                "trial_journey": self.journey,
                **self.custom,
            },
        )

    @classmethod
    def from_core_profile(
        cls,
        profile: ProfileSpecification,
    ) -> "TrialSimProfileSpecification":
        """Create TrialSimProfileSpecification from core profile."""
        protocol = ProtocolSpec()
        arm_dist = ArmDistributionSpec()
        enrollment = EnrollmentSpec()
        sites = SiteSpec()
        visit_comp = VisitComplianceSpec()
        ae_spec = AdverseEventSpec()
        exp_comp = ExposureComplianceSpec()
        generation = TrialSimGenerationSpec(
            count=profile.generation.count,
            seed=profile.generation.seed,
            products=profile.generation.products,
        )

        if profile.custom:
            if "trial_protocol" in profile.custom:
                protocol = ProtocolSpec(**profile.custom["trial_protocol"])
            if "trial_arm_distribution" in profile.custom:
                arm_dist = ArmDistributionSpec(
                    **profile.custom["trial_arm_distribution"]
                )
            if "trial_enrollment" in profile.custom:
                enrollment = EnrollmentSpec(**profile.custom["trial_enrollment"])
            if "trial_sites" in profile.custom:
                sites = SiteSpec(**profile.custom["trial_sites"])
            if "trial_visit_compliance" in profile.custom:
                visit_comp = VisitComplianceSpec(
                    **profile.custom["trial_visit_compliance"]
                )
            if "trial_adverse_events" in profile.custom:
                ae_spec = AdverseEventSpec(**profile.custom["trial_adverse_events"])
            if "trial_exposure_compliance" in profile.custom:
                exp_comp = ExposureComplianceSpec(
                    **profile.custom["trial_exposure_compliance"]
                )
            if "trial_generation" in profile.custom:
                gen_data = profile.custom["trial_generation"]
                generation.generate_visit_records = gen_data.get(
                    "generate_visit_records", True
                )
                generation.generate_adverse_events = gen_data.get(
                    "generate_adverse_events", True
                )
                generation.generate_exposures = gen_data.get(
                    "generate_exposures", True
                )
                generation.export_sdtm = gen_data.get("export_sdtm", False)

        return cls(
            id=profile.id,
            name=profile.name,
            description=profile.description,
            version=profile.version,
            demographics=profile.demographics,
            clinical=profile.clinical,
            protocol=protocol,
            arm_distribution=arm_dist,
            enrollment=enrollment,
            sites=sites,
            visit_compliance=visit_comp,
            adverse_events=ae_spec,
            exposure_compliance=exp_comp,
            generation=generation,
            journey=profile.custom.get("trial_journey") if profile.custom else None,
            outputs=profile.outputs,
            custom={
                k: v
                for k, v in (profile.custom or {}).items()
                if not k.startswith("trial_")
            },
        )

    def to_json(self) -> str:
        """Serialize to JSON string."""
        return self.model_dump_json(indent=2, exclude_none=True)

    @classmethod
    def from_json(cls, json_str: str) -> "TrialSimProfileSpecification":
        """Deserialize from JSON string."""
        return cls.model_validate_json(json_str)
