"""Pre-built profile templates for TrialSim.

Provides ready-to-use profile specifications for common clinical trial
subject populations.
"""

from __future__ import annotations

from typing import Any

from healthsim.generation.profile_schema import (
    DistributionSpec,
    DemographicsSpec,
)

from trialsim.generation.profiles import (
    AdverseEventSpec,
    ArmDistributionSpec,
    EnrollmentSpec,
    ExposureComplianceSpec,
    ProtocolSpec,
    SiteSpec,
    TrialSimGenerationSpec,
    TrialSimProfileSpecification,
    VisitComplianceSpec,
)


# =============================================================================
# Template Definitions
# =============================================================================

TRIALSIM_PROFILE_TEMPLATES: dict[str, TrialSimProfileSpecification] = {
    # -------------------------------------------------------------------------
    # Phase 3 Oncology Trial
    # -------------------------------------------------------------------------
    "phase3-oncology-trial": TrialSimProfileSpecification(
        id="phase3-oncology-trial",
        name="Phase 3 Oncology Trial Subjects",
        description="Standard Phase 3 oncology trial with 2:1 randomization",
        demographics=DemographicsSpec(
            age=DistributionSpec(
                type="normal",
                mean=62.0,
                std_dev=10.0,
                min=18,
                max=85,
            ),
            gender=DistributionSpec(
                type="categorical",
                weights={"M": 0.55, "F": 0.45},
            ),
        ),
        protocol=ProtocolSpec(
            phase="Phase 3",
            therapeutic_area="Oncology",
            indication="Non-Small Cell Lung Cancer",
            duration_weeks=52,
        ),
        arm_distribution=ArmDistributionSpec(
            weights={"treatment": 0.67, "placebo": 0.33},
        ),
        enrollment=EnrollmentSpec(
            screening_failure_rate=0.25,
        ),
        sites=SiteSpec(
            num_sites=50,
            subjects_per_site=DistributionSpec(
                type="normal", mean=15.0, std_dev=5.0, min=5, max=30
            ),
        ),
        adverse_events=AdverseEventSpec(
            ae_probability=0.65,  # High for oncology
            serious_ae_probability=0.12,
        ),
        generation=TrialSimGenerationSpec(
            count=100,
            seed=42,
        ),
    ),
    
    # -------------------------------------------------------------------------
    # Phase 2 Diabetes Trial
    # -------------------------------------------------------------------------
    "phase2-diabetes-trial": TrialSimProfileSpecification(
        id="phase2-diabetes-trial",
        name="Phase 2 Diabetes Trial Subjects",
        description="Phase 2 dose-finding study for T2DM",
        demographics=DemographicsSpec(
            age=DistributionSpec(
                type="normal",
                mean=55.0,
                std_dev=12.0,
                min=18,
                max=75,
            ),
            gender=DistributionSpec(
                type="categorical",
                weights={"M": 0.52, "F": 0.48},
            ),
        ),
        protocol=ProtocolSpec(
            phase="Phase 2",
            therapeutic_area="Endocrinology",
            indication="Type 2 Diabetes Mellitus",
            duration_weeks=24,
        ),
        arm_distribution=ArmDistributionSpec(
            weights={
                "low_dose": 0.25,
                "mid_dose": 0.25,
                "high_dose": 0.25,
                "placebo": 0.25,
            },
        ),
        enrollment=EnrollmentSpec(
            screening_failure_rate=0.30,  # Higher for metabolic trials
        ),
        sites=SiteSpec(
            num_sites=20,
            subjects_per_site=DistributionSpec(
                type="normal", mean=10.0, std_dev=3.0, min=5, max=20
            ),
        ),
        adverse_events=AdverseEventSpec(
            ae_probability=0.35,
            serious_ae_probability=0.03,
        ),
        exposure_compliance=ExposureComplianceSpec(
            compliance_rate=DistributionSpec(
                type="normal", mean=0.88, std_dev=0.10, min=0.5, max=1.0
            ),
        ),
        generation=TrialSimGenerationSpec(
            count=100,
            seed=42,
        ),
    ),
    
    # -------------------------------------------------------------------------
    # Phase 1 Healthy Volunteers
    # -------------------------------------------------------------------------
    "phase1-healthy-volunteers": TrialSimProfileSpecification(
        id="phase1-healthy-volunteers",
        name="Phase 1 Healthy Volunteer Study",
        description="First-in-human safety study with healthy volunteers",
        demographics=DemographicsSpec(
            age=DistributionSpec(
                type="normal",
                mean=32.0,
                std_dev=8.0,
                min=18,
                max=55,
            ),
            gender=DistributionSpec(
                type="categorical",
                weights={"M": 0.70, "F": 0.30},  # Often male-predominant
            ),
        ),
        protocol=ProtocolSpec(
            phase="Phase 1",
            therapeutic_area="Clinical Pharmacology",
            indication="Healthy Volunteers",
            duration_weeks=4,
        ),
        arm_distribution=ArmDistributionSpec(
            weights={"treatment": 0.75, "placebo": 0.25},
        ),
        enrollment=EnrollmentSpec(
            screening_failure_rate=0.15,  # Lower for healthy volunteers
        ),
        sites=SiteSpec(
            num_sites=2,  # Usually 1-2 sites for Phase 1
            subjects_per_site=DistributionSpec(
                type="normal", mean=24.0, std_dev=4.0, min=12, max=36
            ),
        ),
        visit_compliance=VisitComplianceSpec(
            attendance_rate=DistributionSpec(
                type="normal", mean=0.98, std_dev=0.02, min=0.9, max=1.0
            ),
        ),
        adverse_events=AdverseEventSpec(
            ae_probability=0.20,
            serious_ae_probability=0.01,
        ),
        generation=TrialSimGenerationSpec(
            count=48,
            seed=42,
        ),
    ),
    
    # -------------------------------------------------------------------------
    # Cardiovascular Outcomes Trial
    # -------------------------------------------------------------------------
    "cvot-trial": TrialSimProfileSpecification(
        id="cvot-trial",
        name="Cardiovascular Outcomes Trial",
        description="Large outcomes trial for CV safety",
        demographics=DemographicsSpec(
            age=DistributionSpec(
                type="normal",
                mean=65.0,
                std_dev=8.0,
                min=50,
                max=85,
            ),
            gender=DistributionSpec(
                type="categorical",
                weights={"M": 0.65, "F": 0.35},
            ),
        ),
        protocol=ProtocolSpec(
            phase="Phase 3",
            therapeutic_area="Cardiology",
            indication="Cardiovascular Risk Reduction",
            duration_weeks=156,  # 3 years
        ),
        arm_distribution=ArmDistributionSpec(
            weights={"treatment": 0.50, "placebo": 0.50},
        ),
        enrollment=EnrollmentSpec(
            screening_failure_rate=0.35,
        ),
        sites=SiteSpec(
            num_sites=200,
            subjects_per_site=DistributionSpec(
                type="normal", mean=50.0, std_dev=20.0, min=10, max=100
            ),
            region_distribution=DistributionSpec(
                type="categorical",
                weights={
                    "North America": 0.30,
                    "Europe": 0.35,
                    "Asia Pacific": 0.25,
                    "Latin America": 0.10,
                },
            ),
        ),
        adverse_events=AdverseEventSpec(
            ae_probability=0.50,
            serious_ae_probability=0.08,
        ),
        exposure_compliance=ExposureComplianceSpec(
            discontinuation_rate=0.25,  # Higher for long trials
        ),
        generation=TrialSimGenerationSpec(
            count=500,
            seed=42,
        ),
    ),
    
    # -------------------------------------------------------------------------
    # Pediatric Trial
    # -------------------------------------------------------------------------
    "pediatric-trial": TrialSimProfileSpecification(
        id="pediatric-trial",
        name="Pediatric Trial Subjects",
        description="Pediatric efficacy and safety study",
        demographics=DemographicsSpec(
            age=DistributionSpec(
                type="categorical",
                weights={
                    "2": 0.10,
                    "5": 0.15,
                    "8": 0.20,
                    "10": 0.20,
                    "12": 0.20,
                    "15": 0.15,
                },
            ),
            gender=DistributionSpec(
                type="categorical",
                weights={"M": 0.50, "F": 0.50},
            ),
        ),
        protocol=ProtocolSpec(
            phase="Phase 3",
            therapeutic_area="Pediatrics",
            indication="Pediatric Condition",
            duration_weeks=26,
        ),
        arm_distribution=ArmDistributionSpec(
            weights={"treatment": 0.67, "placebo": 0.33},
        ),
        enrollment=EnrollmentSpec(
            screening_failure_rate=0.20,
        ),
        sites=SiteSpec(
            num_sites=30,
            subjects_per_site=DistributionSpec(
                type="normal", mean=8.0, std_dev=3.0, min=3, max=15
            ),
        ),
        visit_compliance=VisitComplianceSpec(
            attendance_rate=DistributionSpec(
                type="normal", mean=0.95, std_dev=0.05, min=0.8, max=1.0
            ),
        ),
        adverse_events=AdverseEventSpec(
            ae_probability=0.30,
            serious_ae_probability=0.02,
        ),
        generation=TrialSimGenerationSpec(
            count=150,
            seed=42,
        ),
    ),
}


# =============================================================================
# Template Access Functions
# =============================================================================

def list_templates() -> list[str]:
    """List available template names.

    Returns:
        List of template identifiers
    """
    return list(TRIALSIM_PROFILE_TEMPLATES.keys())


def get_template(
    name: str,
    **overrides: Any,
) -> TrialSimProfileSpecification:
    """Get a profile template by name with optional overrides.

    Args:
        name: Template identifier
        **overrides: Field overrides to apply

    Returns:
        TrialSimProfileSpecification (copy with overrides applied)

    Raises:
        KeyError: If template not found

    Example:
        >>> spec = get_template("phase3-oncology-trial", generation={"count": 500})
    """
    if name not in TRIALSIM_PROFILE_TEMPLATES:
        available = ", ".join(list_templates())
        raise KeyError(f"Template '{name}' not found. Available: {available}")

    # Get base template
    template = TRIALSIM_PROFILE_TEMPLATES[name]

    if not overrides:
        return template.model_copy(deep=True)

    # Apply overrides
    data = template.model_dump()
    for key, value in overrides.items():
        if isinstance(value, dict) and key in data and isinstance(data[key], dict):
            data[key].update(value)
        else:
            data[key] = value

    return TrialSimProfileSpecification.model_validate(data)


def template_info(name: str) -> dict[str, Any]:
    """Get information about a template.

    Args:
        name: Template identifier

    Returns:
        Dictionary with template metadata
    """
    template = get_template(name)
    return {
        "id": template.id,
        "name": template.name,
        "description": template.description,
        "protocol": {
            "phase": template.protocol.phase,
            "therapeutic_area": template.protocol.therapeutic_area,
            "indication": template.protocol.indication,
            "duration_weeks": template.protocol.duration_weeks,
        },
        "arms": list(template.arm_distribution.weights.keys()),
        "default_count": template.generation.count,
        "num_sites": template.sites.num_sites,
    }
