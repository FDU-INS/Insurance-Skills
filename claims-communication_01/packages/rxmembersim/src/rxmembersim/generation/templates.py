"""Pre-built profile templates for RxMemberSim.

Provides ready-to-use profile specifications for common pharmacy
benefit scenarios.
"""

from __future__ import annotations

from healthsim.generation.profile_schema import (
    ClinicalSpec,
    ConditionSpec,
    DemographicsSpec,
    DistributionSpec,
)

from rxmembersim.generation.profiles import (
    FormularyTierSpec,
    PharmacyPreferenceSpec,
    RxEnrollmentSpec,
    RxMemberCoverageSpec,
    RxMemberGenerationSpec,
    RxMemberProfileSpecification,
    TherapyPatternSpec,
)


# =============================================================================
# Profile Templates
# =============================================================================

RXMEMBER_PROFILE_TEMPLATES: dict[str, RxMemberProfileSpecification] = {
    # -------------------------------------------------------------------------
    # Commercial Templates
    # -------------------------------------------------------------------------
    "commercial-healthy": RxMemberProfileSpecification(
        id="commercial-healthy",
        name="Commercial Healthy Adults",
        description="Low-utilization commercial members with minimal prescriptions",
        demographics=DemographicsSpec(
            age=DistributionSpec(type="normal", mean=35, std_dev=10, min=18, max=64),
            gender=DistributionSpec(type="categorical", weights={"M": 0.48, "F": 0.52}),
        ),
        coverage=RxMemberCoverageSpec(
            coverage_type="Commercial",
            formulary_tier_distribution=FormularyTierSpec(
                weights={
                    "tier1_generic": 0.70,
                    "tier2_preferred_brand": 0.25,
                    "tier3_non_preferred": 0.05,
                    "tier4_specialty": 0.00,
                }
            ),
            pharmacy_preference=PharmacyPreferenceSpec(
                weights={"retail": 0.85, "mail_order": 0.15, "specialty": 0.00, "ltc": 0.00}
            ),
            therapy_pattern=TherapyPatternSpec(
                adherence_rate=DistributionSpec(type="normal", mean=0.80, std_dev=0.10),
                avg_therapies_per_member=DistributionSpec(type="normal", mean=1.5, std_dev=0.5, min=0, max=4),
            ),
        ),
        generation=RxMemberGenerationSpec(
            count=100,
            generate_claim_history=True,
            history_months=12,
            include_specialty_rx=False,
        ),
    ),

    "commercial-chronic": RxMemberProfileSpecification(
        id="commercial-chronic",
        name="Commercial Chronic Condition Members",
        description="Commercial members managing chronic conditions",
        demographics=DemographicsSpec(
            age=DistributionSpec(type="normal", mean=50, std_dev=10, min=30, max=64),
        ),
        clinical=ClinicalSpec(
            conditions=[
                ConditionSpec(code="E11", description="Type 2 Diabetes", prevalence=0.40),
                ConditionSpec(code="I10", description="Hypertension", prevalence=0.50),
                ConditionSpec(code="E78", description="Hyperlipidemia", prevalence=0.35),
            ]
        ),
        coverage=RxMemberCoverageSpec(
            coverage_type="Commercial",
            therapy_pattern=TherapyPatternSpec(
                adherence_rate=DistributionSpec(type="normal", mean=0.70, std_dev=0.15),
                avg_therapies_per_member=DistributionSpec(type="normal", mean=4.0, std_dev=1.5, min=2, max=10),
            ),
        ),
        generation=RxMemberGenerationSpec(
            count=100,
            history_months=24,
            include_dur_alerts=True,
        ),
    ),

    # -------------------------------------------------------------------------
    # Medicare Part D Templates
    # -------------------------------------------------------------------------
    "medicare-partd-standard": RxMemberProfileSpecification(
        id="medicare-partd-standard",
        name="Medicare Part D Standard",
        description="Typical Medicare Part D beneficiary",
        demographics=DemographicsSpec(
            age=DistributionSpec(type="normal", mean=72, std_dev=7, min=65, max=100),
        ),
        coverage=RxMemberCoverageSpec(
            coverage_type="Medicare Part D",
            formulary_tier_distribution=FormularyTierSpec(
                weights={
                    "tier1_generic": 0.55,
                    "tier2_preferred_brand": 0.30,
                    "tier3_non_preferred": 0.12,
                    "tier4_specialty": 0.03,
                }
            ),
            pharmacy_preference=PharmacyPreferenceSpec(
                weights={"retail": 0.70, "mail_order": 0.25, "specialty": 0.03, "ltc": 0.02}
            ),
            therapy_pattern=TherapyPatternSpec(
                avg_therapies_per_member=DistributionSpec(type="normal", mean=5.0, std_dev=2.0, min=1, max=15),
            ),
        ),
        generation=RxMemberGenerationSpec(
            count=100,
            history_months=12,
        ),
    ),

    "medicare-partd-polypharmacy": RxMemberProfileSpecification(
        id="medicare-partd-polypharmacy",
        name="Medicare Part D Polypharmacy",
        description="Medicare members with high medication burden",
        demographics=DemographicsSpec(
            age=DistributionSpec(type="normal", mean=78, std_dev=6, min=65, max=100),
        ),
        clinical=ClinicalSpec(
            conditions=[
                ConditionSpec(code="E11", description="Type 2 Diabetes", prevalence=0.60),
                ConditionSpec(code="I10", description="Hypertension", prevalence=0.80),
                ConditionSpec(code="I50", description="Heart Failure", prevalence=0.30),
                ConditionSpec(code="J44", description="COPD", prevalence=0.25),
                ConditionSpec(code="M81", description="Osteoporosis", prevalence=0.20),
            ]
        ),
        coverage=RxMemberCoverageSpec(
            coverage_type="Medicare Part D",
            formulary_tier_distribution=FormularyTierSpec(
                weights={
                    "tier1_generic": 0.45,
                    "tier2_preferred_brand": 0.35,
                    "tier3_non_preferred": 0.15,
                    "tier4_specialty": 0.05,
                }
            ),
            therapy_pattern=TherapyPatternSpec(
                adherence_rate=DistributionSpec(type="normal", mean=0.65, std_dev=0.18),
                avg_therapies_per_member=DistributionSpec(type="normal", mean=9.0, std_dev=2.5, min=6, max=18),
            ),
        ),
        generation=RxMemberGenerationSpec(
            count=100,
            history_months=24,
            include_dur_alerts=True,
        ),
    ),

    "medicare-partd-lis": RxMemberProfileSpecification(
        id="medicare-partd-lis",
        name="Medicare Part D Low Income Subsidy",
        description="Medicare LIS (Extra Help) beneficiaries",
        demographics=DemographicsSpec(
            age=DistributionSpec(type="normal", mean=74, std_dev=8, min=65, max=100),
        ),
        coverage=RxMemberCoverageSpec(
            coverage_type="Medicare Part D",
            formulary_tier_distribution=FormularyTierSpec(
                weights={
                    "tier1_generic": 0.70,
                    "tier2_preferred_brand": 0.25,
                    "tier3_non_preferred": 0.05,
                    "tier4_specialty": 0.00,
                }
            ),
            pharmacy_preference=PharmacyPreferenceSpec(
                weights={"retail": 0.90, "mail_order": 0.08, "specialty": 0.01, "ltc": 0.01}
            ),
            therapy_pattern=TherapyPatternSpec(
                avg_therapies_per_member=DistributionSpec(type="normal", mean=6.0, std_dev=2.0, min=2, max=12),
            ),
        ),
        generation=RxMemberGenerationSpec(
            count=100,
            history_months=12,
        ),
    ),

    # -------------------------------------------------------------------------
    # Specialty Pharmacy Templates
    # -------------------------------------------------------------------------
    "specialty-oncology": RxMemberProfileSpecification(
        id="specialty-oncology",
        name="Specialty Oncology Members",
        description="Members on oral oncology specialty medications",
        demographics=DemographicsSpec(
            age=DistributionSpec(type="normal", mean=62, std_dev=12, min=25, max=90),
        ),
        clinical=ClinicalSpec(
            conditions=[
                ConditionSpec(code="C50", description="Breast Cancer", prevalence=0.25),
                ConditionSpec(code="C34", description="Lung Cancer", prevalence=0.20),
                ConditionSpec(code="C61", description="Prostate Cancer", prevalence=0.15),
                ConditionSpec(code="C18", description="Colon Cancer", prevalence=0.10),
            ]
        ),
        coverage=RxMemberCoverageSpec(
            coverage_type="Commercial",
            formulary_tier_distribution=FormularyTierSpec(
                weights={
                    "tier1_generic": 0.10,
                    "tier2_preferred_brand": 0.15,
                    "tier3_non_preferred": 0.15,
                    "tier4_specialty": 0.60,
                }
            ),
            pharmacy_preference=PharmacyPreferenceSpec(
                weights={"retail": 0.05, "mail_order": 0.10, "specialty": 0.85, "ltc": 0.00}
            ),
            therapy_pattern=TherapyPatternSpec(
                adherence_rate=DistributionSpec(type="normal", mean=0.85, std_dev=0.10),
                avg_therapies_per_member=DistributionSpec(type="normal", mean=4.0, std_dev=1.5, min=1, max=8),
            ),
        ),
        generation=RxMemberGenerationSpec(
            count=50,
            include_specialty_rx=True,
            history_months=12,
        ),
    ),

    "specialty-autoimmune": RxMemberProfileSpecification(
        id="specialty-autoimmune",
        name="Specialty Autoimmune Members",
        description="Members on biologic therapies for autoimmune conditions",
        demographics=DemographicsSpec(
            age=DistributionSpec(type="normal", mean=48, std_dev=14, min=18, max=75),
        ),
        clinical=ClinicalSpec(
            conditions=[
                ConditionSpec(code="M05", description="Rheumatoid Arthritis", prevalence=0.40),
                ConditionSpec(code="L40", description="Psoriasis", prevalence=0.25),
                ConditionSpec(code="K50", description="Crohn's Disease", prevalence=0.20),
                ConditionSpec(code="M45", description="Ankylosing Spondylitis", prevalence=0.15),
            ]
        ),
        coverage=RxMemberCoverageSpec(
            coverage_type="Commercial",
            formulary_tier_distribution=FormularyTierSpec(
                weights={
                    "tier1_generic": 0.15,
                    "tier2_preferred_brand": 0.20,
                    "tier3_non_preferred": 0.15,
                    "tier4_specialty": 0.50,
                }
            ),
            pharmacy_preference=PharmacyPreferenceSpec(
                weights={"retail": 0.10, "mail_order": 0.15, "specialty": 0.75, "ltc": 0.00}
            ),
        ),
        generation=RxMemberGenerationSpec(
            count=50,
            include_specialty_rx=True,
            history_months=24,
        ),
    ),

    # -------------------------------------------------------------------------
    # Long-Term Care Templates
    # -------------------------------------------------------------------------
    "ltc-nursing-home": RxMemberProfileSpecification(
        id="ltc-nursing-home",
        name="Long-Term Care Nursing Home",
        description="Skilled nursing facility residents",
        demographics=DemographicsSpec(
            age=DistributionSpec(type="normal", mean=82, std_dev=8, min=65, max=105),
        ),
        clinical=ClinicalSpec(
            conditions=[
                ConditionSpec(code="F03", description="Dementia", prevalence=0.50),
                ConditionSpec(code="I10", description="Hypertension", prevalence=0.75),
                ConditionSpec(code="E11", description="Type 2 Diabetes", prevalence=0.35),
                ConditionSpec(code="I50", description="Heart Failure", prevalence=0.30),
            ]
        ),
        coverage=RxMemberCoverageSpec(
            coverage_type="Medicare Part D",
            pharmacy_preference=PharmacyPreferenceSpec(
                weights={"retail": 0.00, "mail_order": 0.00, "specialty": 0.05, "ltc": 0.95}
            ),
            therapy_pattern=TherapyPatternSpec(
                adherence_rate=DistributionSpec(type="normal", mean=0.95, std_dev=0.03),
                avg_therapies_per_member=DistributionSpec(type="normal", mean=10.0, std_dev=3.0, min=5, max=20),
            ),
        ),
        generation=RxMemberGenerationSpec(
            count=100,
            history_months=12,
            include_dur_alerts=True,
        ),
    ),
}


def get_template(template_id: str) -> RxMemberProfileSpecification:
    """Get a profile template by ID.

    Args:
        template_id: Template identifier

    Returns:
        Copy of the template specification

    Raises:
        KeyError: If template not found
    """
    if template_id not in RXMEMBER_PROFILE_TEMPLATES:
        available = list(RXMEMBER_PROFILE_TEMPLATES.keys())
        raise KeyError(
            f"Template '{template_id}' not found. Available: {available}"
        )
    
    # Return a copy to prevent modification of template
    template = RXMEMBER_PROFILE_TEMPLATES[template_id]
    return RxMemberProfileSpecification.model_validate(template.model_dump())


def list_templates() -> list[dict[str, str]]:
    """List available profile templates.

    Returns:
        List of template summaries with id, name, and description
    """
    return [
        {
            "id": spec.id,
            "name": spec.name,
            "description": spec.description or "",
            "coverage_type": spec.coverage.coverage_type,
        }
        for spec in RXMEMBER_PROFILE_TEMPLATES.values()
    ]
