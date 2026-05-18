"""MemberSim journey templates.

Pre-built journey specifications for common member scenarios.
These templates can be used directly or customized for specific needs.
"""

from healthsim.generation.journey_engine import (
    JourneySpecification,
    EventDefinition,
    DelaySpec,
    EventCondition,
    MemberEventType,
    create_simple_journey,
)


# =============================================================================
# Journey Template Definitions
# =============================================================================

MEMBER_JOURNEY_TEMPLATES = {
    "new-member-onboarding": {
        "journey_id": "new-member-onboarding",
        "name": "New Member Onboarding",
        "description": "Standard journey for new health plan enrollment through initial engagement",
        "products": ["membersim"],
        "duration_days": 90,
        "events": [
            {
                "event_id": "enrollment",
                "name": "New Enrollment",
                "event_type": MemberEventType.NEW_ENROLLMENT.value,
                "product": "membersim",
                "delay": {"days": 0},
            },
            {
                "event_id": "id_card",
                "name": "ID Card Generated",
                "event_type": "milestone",
                "product": "membersim",
                "delay": {"days": 3, "days_min": 2, "days_max": 5, "distribution": "uniform"},
                "depends_on": "enrollment",
            },
            {
                "event_id": "welcome_call",
                "name": "Welcome Call",
                "event_type": "milestone",
                "product": "membersim",
                "delay": {"days": 14, "days_min": 7, "days_max": 21, "distribution": "uniform"},
                "depends_on": "enrollment",
                "probability": 0.6,
            },
            {
                "event_id": "hra",
                "name": "Health Risk Assessment",
                "event_type": "milestone",
                "product": "membersim",
                "delay": {"days": 30, "days_min": 14, "days_max": 60, "distribution": "uniform"},
                "depends_on": "enrollment",
                "probability": 0.4,
            },
            {
                "event_id": "pcp_assignment",
                "name": "PCP Assignment",
                "event_type": "milestone",
                "product": "membersim",
                "delay": {"days": 7, "days_min": 3, "days_max": 14, "distribution": "uniform"},
                "depends_on": "enrollment",
            },
        ],
    },
    
    "annual-wellness": {
        "journey_id": "annual-wellness",
        "name": "Annual Wellness Journey",
        "description": "Standard annual wellness visit and preventive care journey",
        "products": ["membersim", "patientsim"],
        "duration_days": 365,
        "events": [
            {
                "event_id": "wellness_reminder",
                "name": "Wellness Visit Reminder",
                "event_type": "milestone",
                "product": "membersim",
                "delay": {"days": 0},
            },
            {
                "event_id": "wellness_visit",
                "name": "Annual Wellness Visit",
                "event_type": MemberEventType.CLAIM_PROFESSIONAL.value,
                "product": "membersim",
                "delay": {"days": 30, "days_min": 14, "days_max": 60, "distribution": "uniform"},
                "depends_on": "wellness_reminder",
                "probability": 0.7,
                "parameters": {
                    "procedure_codes": ["99395", "99396", "99397"],
                    "diagnosis_codes": ["Z00.00"],
                },
            },
            {
                "event_id": "preventive_lab",
                "name": "Preventive Lab Work",
                "event_type": MemberEventType.CLAIM_PROFESSIONAL.value,
                "product": "membersim",
                "delay": {"days": 0, "days_min": 0, "days_max": 7, "distribution": "uniform"},
                "depends_on": "wellness_visit",
                "probability": 0.8,
                "parameters": {
                    "procedure_codes": ["80061", "82947"],  # Lipid panel, glucose
                },
            },
        ],
    },
    
    "chronic-care-management": {
        "journey_id": "chronic-care-management",
        "name": "Chronic Care Management",
        "description": "Ongoing care journey for members with chronic conditions",
        "products": ["membersim", "patientsim"],
        "duration_days": 365,
        "events": [
            {
                "event_id": "ccm_enrollment",
                "name": "CCM Program Enrollment",
                "event_type": "milestone",
                "product": "membersim",
                "delay": {"days": 0},
            },
            {
                "event_id": "initial_assessment",
                "name": "Initial Care Assessment",
                "event_type": MemberEventType.CLAIM_PROFESSIONAL.value,
                "product": "membersim",
                "delay": {"days": 7, "days_min": 3, "days_max": 14, "distribution": "uniform"},
                "depends_on": "ccm_enrollment",
                "parameters": {
                    "procedure_codes": ["99490"],  # CCM initial
                },
            },
            {
                "event_id": "monthly_ccm_1",
                "name": "Monthly CCM - Month 1",
                "event_type": MemberEventType.CLAIM_PROFESSIONAL.value,
                "product": "membersim",
                "delay": {"days": 30, "days_min": 25, "days_max": 35, "distribution": "uniform"},
                "depends_on": "initial_assessment",
                "parameters": {
                    "procedure_codes": ["99491"],
                },
            },
            {
                "event_id": "monthly_ccm_2",
                "name": "Monthly CCM - Month 2",
                "event_type": MemberEventType.CLAIM_PROFESSIONAL.value,
                "product": "membersim",
                "delay": {"days": 30, "days_min": 25, "days_max": 35, "distribution": "uniform"},
                "depends_on": "monthly_ccm_1",
                "parameters": {
                    "procedure_codes": ["99491"],
                },
            },
            {
                "event_id": "monthly_ccm_3",
                "name": "Monthly CCM - Month 3",
                "event_type": MemberEventType.CLAIM_PROFESSIONAL.value,
                "product": "membersim",
                "delay": {"days": 30, "days_min": 25, "days_max": 35, "distribution": "uniform"},
                "depends_on": "monthly_ccm_2",
                "parameters": {
                    "procedure_codes": ["99491"],
                },
            },
            {
                "event_id": "quarterly_review",
                "name": "Quarterly Care Plan Review",
                "event_type": "milestone",
                "product": "membersim",
                "delay": {"days": 0},
                "depends_on": "monthly_ccm_3",
            },
        ],
    },
    
    "surgical-episode": {
        "journey_id": "surgical-episode",
        "name": "Surgical Episode",
        "description": "End-to-end journey for a planned surgical procedure",
        "products": ["membersim", "patientsim"],
        "duration_days": 120,
        "events": [
            {
                "event_id": "consult",
                "name": "Surgical Consultation",
                "event_type": MemberEventType.CLAIM_PROFESSIONAL.value,
                "product": "membersim",
                "delay": {"days": 0},
                "parameters": {
                    "procedure_codes": ["99244"],
                    "place_of_service": "11",
                },
            },
            {
                "event_id": "auth_request",
                "name": "Prior Authorization Request",
                "event_type": "milestone",
                "product": "membersim",
                "delay": {"days": 3, "days_min": 1, "days_max": 7, "distribution": "uniform"},
                "depends_on": "consult",
            },
            {
                "event_id": "pre_op",
                "name": "Pre-operative Testing",
                "event_type": MemberEventType.CLAIM_PROFESSIONAL.value,
                "product": "membersim",
                "delay": {"days": 14, "days_min": 7, "days_max": 21, "distribution": "uniform"},
                "depends_on": "auth_request",
                "parameters": {
                    "procedure_codes": ["93000", "71046"],  # EKG, Chest X-ray
                },
            },
            {
                "event_id": "surgery",
                "name": "Surgical Procedure",
                "event_type": MemberEventType.CLAIM_INSTITUTIONAL.value,
                "product": "membersim",
                "delay": {"days": 7, "days_min": 3, "days_max": 14, "distribution": "uniform"},
                "depends_on": "pre_op",
                "parameters": {
                    "facility_type": "hospital",
                    "revenue_codes": ["0120", "0250", "0360"],
                },
            },
            {
                "event_id": "post_op_1",
                "name": "Post-op Follow-up 1",
                "event_type": MemberEventType.CLAIM_PROFESSIONAL.value,
                "product": "membersim",
                "delay": {"days": 7, "days_min": 5, "days_max": 10, "distribution": "uniform"},
                "depends_on": "surgery",
                "parameters": {
                    "procedure_codes": ["99213"],
                },
            },
            {
                "event_id": "post_op_2",
                "name": "Post-op Follow-up 2",
                "event_type": MemberEventType.CLAIM_PROFESSIONAL.value,
                "product": "membersim",
                "delay": {"days": 30, "days_min": 21, "days_max": 42, "distribution": "uniform"},
                "depends_on": "surgery",
                "parameters": {
                    "procedure_codes": ["99214"],
                },
            },
        ],
    },
    
    "quality-gap-closure": {
        "journey_id": "quality-gap-closure",
        "name": "Quality Gap Closure",
        "description": "Journey from gap identification through closure",
        "products": ["membersim"],
        "duration_days": 90,
        "events": [
            {
                "event_id": "gap_identified",
                "name": "Quality Gap Identified",
                "event_type": MemberEventType.GAP_IDENTIFIED.value,
                "product": "membersim",
                "delay": {"days": 0},
                "parameters": {
                    "measure_id": "CDC",
                    "measure_name": "Comprehensive Diabetes Care - A1C",
                },
            },
            {
                "event_id": "outreach_1",
                "name": "Initial Outreach",
                "event_type": "milestone",
                "product": "membersim",
                "delay": {"days": 7, "days_min": 3, "days_max": 14, "distribution": "uniform"},
                "depends_on": "gap_identified",
            },
            {
                "event_id": "outreach_2",
                "name": "Follow-up Outreach",
                "event_type": "milestone",
                "product": "membersim",
                "delay": {"days": 21, "days_min": 14, "days_max": 28, "distribution": "uniform"},
                "depends_on": "outreach_1",
                "probability": 0.6,
            },
            {
                "event_id": "gap_closure_visit",
                "name": "Gap Closure Visit",
                "event_type": MemberEventType.CLAIM_PROFESSIONAL.value,
                "product": "membersim",
                "delay": {"days": 30, "days_min": 14, "days_max": 60, "distribution": "uniform"},
                "depends_on": "gap_identified",
                "probability": 0.7,
                "parameters": {
                    "procedure_codes": ["83036"],  # A1C test
                },
            },
            {
                "event_id": "gap_closed",
                "name": "Quality Gap Closed",
                "event_type": MemberEventType.GAP_CLOSED.value,
                "product": "membersim",
                "delay": {"days": 3, "days_min": 1, "days_max": 7, "distribution": "uniform"},
                "depends_on": "gap_closure_visit",
                "parameters": {
                    "measure_id": "CDC",
                    "closed_by": "claim",
                },
            },
        ],
    },
    
    "member-termination": {
        "journey_id": "member-termination",
        "name": "Member Termination",
        "description": "Journey for member termination and COBRA eligibility",
        "products": ["membersim"],
        "duration_days": 90,
        "events": [
            {
                "event_id": "termination_notice",
                "name": "Termination Notice Received",
                "event_type": "milestone",
                "product": "membersim",
                "delay": {"days": 0},
            },
            {
                "event_id": "termination",
                "name": "Coverage Termination",
                "event_type": MemberEventType.TERMINATION.value,
                "product": "membersim",
                "delay": {"days": 30, "days_min": 14, "days_max": 30, "distribution": "uniform"},
                "depends_on": "termination_notice",
            },
            {
                "event_id": "cobra_notice",
                "name": "COBRA Notice Sent",
                "event_type": "milestone",
                "product": "membersim",
                "delay": {"days": 14, "days_min": 7, "days_max": 14, "distribution": "uniform"},
                "depends_on": "termination",
            },
            {
                "event_id": "cobra_election",
                "name": "COBRA Election",
                "event_type": MemberEventType.NEW_ENROLLMENT.value,
                "product": "membersim",
                "delay": {"days": 45, "days_min": 30, "days_max": 60, "distribution": "uniform"},
                "depends_on": "cobra_notice",
                "probability": 0.2,
                "parameters": {
                    "coverage_type": "COBRA",
                },
            },
        ],
    },
}


# =============================================================================
# Template Access Functions
# =============================================================================

def get_member_journey_template(template_name: str) -> JourneySpecification:
    """Get a MemberSim journey template by name.
    
    Args:
        template_name: Name of the template
        
    Returns:
        JourneySpecification
        
    Raises:
        ValueError: If template not found
        
    Example:
        >>> journey = get_member_journey_template("new-member-onboarding")
        >>> print(journey.name)
        "New Member Onboarding"
    """
    if template_name not in MEMBER_JOURNEY_TEMPLATES:
        available = ", ".join(MEMBER_JOURNEY_TEMPLATES.keys())
        raise ValueError(f"Template '{template_name}' not found. Available: {available}")
    
    template = MEMBER_JOURNEY_TEMPLATES[template_name]
    return create_simple_journey(
        journey_id=template["journey_id"],
        name=template["name"],
        events=template["events"],
        products=template.get("products"),
    )


def list_member_journey_templates() -> dict[str, str]:
    """List available MemberSim journey templates.
    
    Returns:
        Dict mapping template name to description
        
    Example:
        >>> templates = list_member_journey_templates()
        >>> for name, desc in templates.items():
        ...     print(f"{name}: {desc}")
    """
    return {
        name: template["description"]
        for name, template in MEMBER_JOURNEY_TEMPLATES.items()
    }


# Convenience aliases for common templates
NEW_MEMBER_ONBOARDING = get_member_journey_template("new-member-onboarding")
ANNUAL_WELLNESS = get_member_journey_template("annual-wellness")
CHRONIC_CARE_MANAGEMENT = get_member_journey_template("chronic-care-management")
SURGICAL_EPISODE = get_member_journey_template("surgical-episode")
QUALITY_GAP_CLOSURE = get_member_journey_template("quality-gap-closure")
MEMBER_TERMINATION = get_member_journey_template("member-termination")
