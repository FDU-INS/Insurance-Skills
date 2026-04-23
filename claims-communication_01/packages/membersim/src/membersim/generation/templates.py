"""Pre-built member profile templates for common scenarios.

These templates provide starting points for common member cohort types.
They can be used directly or customized via the MemberProfileSpecification API.
"""

from healthsim.generation.profile_schema import (
    ClinicalSpec,
    ConditionSpec,
    DemographicsSpec,
    DistributionSpec,
)

from membersim.generation.profiles import (
    MemberCoverageSpec,
    MemberGenerationSpec,
    MemberProfileSpecification,
    PlanDistributionSpec,
    SubscriberRelationshipSpec,
)


# =============================================================================
# Commercial Templates
# =============================================================================

COMMERCIAL_PPO_HEALTHY = MemberProfileSpecification(
    id="commercial-ppo-healthy",
    name="Commercial PPO Healthy Adults",
    description="Working-age adults with commercial PPO coverage, no chronic conditions",
    demographics=DemographicsSpec(
        age=DistributionSpec(
            type="normal",
            mean=38,
            std_dev=12,
            min=18,
            max=64,
        ),
        gender=DistributionSpec(
            type="categorical",
            weights={"M": 0.50, "F": 0.50},
        ),
    ),
    coverage=MemberCoverageSpec(
        coverage_type="Commercial",
        plan_distribution=PlanDistributionSpec(
            weights={"PPO": 1.0},
        ),
        relationship_distribution=SubscriberRelationshipSpec(
            weights={"subscriber": 0.50, "spouse": 0.25, "dependent": 0.25},
        ),
    ),
    generation=MemberGenerationSpec(count=100),
)

COMMERCIAL_HDHP_YOUNG = MemberProfileSpecification(
    id="commercial-hdhp-young",
    name="Commercial HDHP Young Adults",
    description="Young adults with high-deductible health plans",
    demographics=DemographicsSpec(
        age=DistributionSpec(
            type="normal",
            mean=28,
            std_dev=5,
            min=22,
            max=40,
        ),
        gender=DistributionSpec(
            type="categorical",
            weights={"M": 0.52, "F": 0.48},
        ),
    ),
    coverage=MemberCoverageSpec(
        coverage_type="Commercial",
        plan_distribution=PlanDistributionSpec(
            weights={"HDHP": 1.0},
        ),
        relationship_distribution=SubscriberRelationshipSpec(
            weights={"subscriber": 0.70, "spouse": 0.15, "dependent": 0.15},
        ),
    ),
    generation=MemberGenerationSpec(count=100),
)

COMMERCIAL_FAMILY_MIX = MemberProfileSpecification(
    id="commercial-family-mix",
    name="Commercial Family Coverage Mix",
    description="Diverse commercial population with families across plan types",
    demographics=DemographicsSpec(
        age=DistributionSpec(
            type="age_bands",
            bands={
                "0-17": 0.25,
                "18-34": 0.25,
                "35-54": 0.35,
                "55-64": 0.15,
            },
        ),
        gender=DistributionSpec(
            type="categorical",
            weights={"M": 0.49, "F": 0.51},
        ),
    ),
    coverage=MemberCoverageSpec(
        coverage_type="Commercial",
        plan_distribution=PlanDistributionSpec(
            weights={"PPO": 0.40, "HMO": 0.35, "HDHP": 0.25},
        ),
        relationship_distribution=SubscriberRelationshipSpec(
            weights={"subscriber": 0.40, "spouse": 0.25, "dependent": 0.35},
        ),
    ),
    generation=MemberGenerationSpec(
        count=100,
        generate_subscriber_groups=True,
        avg_dependents_per_subscriber=1.8,
    ),
)


# =============================================================================
# Medicare Templates
# =============================================================================

MEDICARE_ADVANTAGE_DIABETIC = MemberProfileSpecification(
    id="medicare-advantage-diabetic",
    name="Medicare Advantage Diabetic Population",
    description="Medicare Advantage members with Type 2 diabetes and common comorbidities",
    demographics=DemographicsSpec(
        age=DistributionSpec(
            type="normal",
            mean=72,
            std_dev=7,
            min=65,
            max=95,
        ),
        gender=DistributionSpec(
            type="categorical",
            weights={"M": 0.48, "F": 0.52},
        ),
    ),
    clinical=ClinicalSpec(
        primary_condition=ConditionSpec(
            code="E11",
            description="Type 2 diabetes mellitus",
            prevalence=1.0,
        ),
        comorbidities=[
            ConditionSpec(code="I10", description="Essential hypertension", prevalence=0.75),
            ConditionSpec(code="E78", description="Disorders of lipoprotein metabolism", prevalence=0.70),
            ConditionSpec(code="I25", description="Chronic ischemic heart disease", prevalence=0.35),
            ConditionSpec(code="N18", description="Chronic kidney disease", prevalence=0.25),
        ],
    ),
    coverage=MemberCoverageSpec(
        coverage_type="Medicare",
        plan_distribution=PlanDistributionSpec(
            weights={"Medicare Advantage HMO": 0.55, "Medicare Advantage PPO": 0.45},
        ),
        relationship_distribution=SubscriberRelationshipSpec(
            weights={"subscriber": 1.0},  # No dependents on Medicare
        ),
    ),
    generation=MemberGenerationSpec(
        count=100,
        include_quality_gaps=True,
    ),
)

MEDICARE_ORIGINAL_HEALTHY = MemberProfileSpecification(
    id="medicare-original-healthy",
    name="Original Medicare Healthy Seniors",
    description="Traditional Medicare beneficiaries in good health",
    demographics=DemographicsSpec(
        age=DistributionSpec(
            type="normal",
            mean=70,
            std_dev=5,
            min=65,
            max=85,
        ),
        gender=DistributionSpec(
            type="categorical",
            weights={"M": 0.45, "F": 0.55},
        ),
    ),
    coverage=MemberCoverageSpec(
        coverage_type="Medicare",
        plan_distribution=PlanDistributionSpec(
            weights={"Original Medicare": 1.0},
        ),
        relationship_distribution=SubscriberRelationshipSpec(
            weights={"subscriber": 1.0},
        ),
    ),
    generation=MemberGenerationSpec(count=100),
)


# =============================================================================
# Medicaid Templates
# =============================================================================

MEDICAID_PEDIATRIC = MemberProfileSpecification(
    id="medicaid-pediatric",
    name="Medicaid Pediatric Population",
    description="Children covered under Medicaid/CHIP",
    demographics=DemographicsSpec(
        age=DistributionSpec(
            type="age_bands",
            bands={
                "0-2": 0.15,
                "3-5": 0.15,
                "6-12": 0.40,
                "13-17": 0.30,
            },
        ),
        gender=DistributionSpec(
            type="categorical",
            weights={"M": 0.51, "F": 0.49},
        ),
    ),
    coverage=MemberCoverageSpec(
        coverage_type="Medicaid",
        plan_distribution=PlanDistributionSpec(
            weights={"Medicaid MCO": 0.75, "Medicaid FFS": 0.25},
        ),
        relationship_distribution=SubscriberRelationshipSpec(
            weights={"dependent": 1.0},
        ),
    ),
    generation=MemberGenerationSpec(
        count=100,
        include_quality_gaps=True,
    ),
)

MEDICAID_ADULT_EXPANSION = MemberProfileSpecification(
    id="medicaid-adult-expansion",
    name="Medicaid Expansion Adult Population",
    description="Adults covered under Medicaid expansion",
    demographics=DemographicsSpec(
        age=DistributionSpec(
            type="normal",
            mean=38,
            std_dev=12,
            min=19,
            max=64,
        ),
        gender=DistributionSpec(
            type="categorical",
            weights={"M": 0.48, "F": 0.52},
        ),
    ),
    coverage=MemberCoverageSpec(
        coverage_type="Medicaid",
        plan_distribution=PlanDistributionSpec(
            weights={"Medicaid MCO": 0.80, "Medicaid FFS": 0.20},
        ),
        relationship_distribution=SubscriberRelationshipSpec(
            weights={"subscriber": 1.0},
        ),
    ),
    generation=MemberGenerationSpec(count=100),
)


# =============================================================================
# Exchange/Marketplace Templates
# =============================================================================

EXCHANGE_SILVER_PLAN = MemberProfileSpecification(
    id="exchange-silver-plan",
    name="ACA Exchange Silver Plan Members",
    description="Health insurance marketplace members with Silver plans",
    demographics=DemographicsSpec(
        age=DistributionSpec(
            type="normal",
            mean=42,
            std_dev=14,
            min=18,
            max=64,
        ),
        gender=DistributionSpec(
            type="categorical",
            weights={"M": 0.47, "F": 0.53},
        ),
    ),
    coverage=MemberCoverageSpec(
        coverage_type="Exchange",
        plan_distribution=PlanDistributionSpec(
            weights={"Silver HMO": 0.50, "Silver PPO": 0.30, "Silver EPO": 0.20},
        ),
        relationship_distribution=SubscriberRelationshipSpec(
            weights={"subscriber": 0.55, "spouse": 0.20, "dependent": 0.25},
        ),
    ),
    generation=MemberGenerationSpec(count=100),
)


# =============================================================================
# Template Registry
# =============================================================================

MEMBER_PROFILE_TEMPLATES: dict[str, MemberProfileSpecification] = {
    # Commercial
    "commercial-ppo-healthy": COMMERCIAL_PPO_HEALTHY,
    "commercial-hdhp-young": COMMERCIAL_HDHP_YOUNG,
    "commercial-family-mix": COMMERCIAL_FAMILY_MIX,
    # Medicare
    "medicare-advantage-diabetic": MEDICARE_ADVANTAGE_DIABETIC,
    "medicare-original-healthy": MEDICARE_ORIGINAL_HEALTHY,
    # Medicaid
    "medicaid-pediatric": MEDICAID_PEDIATRIC,
    "medicaid-adult-expansion": MEDICAID_ADULT_EXPANSION,
    # Exchange
    "exchange-silver-plan": EXCHANGE_SILVER_PLAN,
}


def get_template(name: str) -> MemberProfileSpecification:
    """Get a profile template by name.

    Args:
        name: Template name (e.g., "commercial-ppo-healthy")

    Returns:
        Copy of the template specification

    Raises:
        KeyError: If template not found
    """
    if name not in MEMBER_PROFILE_TEMPLATES:
        available = ", ".join(sorted(MEMBER_PROFILE_TEMPLATES.keys()))
        raise KeyError(f"Unknown template '{name}'. Available: {available}")

    # Return a copy to prevent modification of template
    template = MEMBER_PROFILE_TEMPLATES[name]
    return MemberProfileSpecification.model_validate(template.model_dump())


def list_templates() -> list[dict[str, str]]:
    """List all available templates with descriptions.

    Returns:
        List of dicts with id, name, description
    """
    return [
        {
            "id": template.id,
            "name": template.name,
            "description": template.description or "",
        }
        for template in MEMBER_PROFILE_TEMPLATES.values()
    ]
