"""RxMemberSim journey templates.

Pre-built journey specifications for common pharmacy scenarios.
These templates can be used directly or customized for specific needs.
"""

from healthsim.generation.journey_engine import (
    JourneySpecification,
    EventDefinition,
    DelaySpec,
    EventCondition,
    RxEventType,
    create_simple_journey,
)


# =============================================================================
# Journey Template Definitions
# =============================================================================

RX_JOURNEY_TEMPLATES = {
    "new-therapy-start": {
        "journey_id": "new-therapy-start",
        "name": "New Therapy Start",
        "description": "Standard journey for starting a new medication therapy",
        "products": ["rxmembersim"],
        "duration_days": 180,
        "events": [
            {
                "event_id": "prescription",
                "name": "New Prescription Written",
                "event_type": RxEventType.NEW_RX.value,
                "product": "rxmembersim",
                "delay": {"days": 0},
                "parameters": {
                    "quantity": 30,
                    "days_supply": 30,
                },
            },
            {
                "event_id": "first_fill",
                "name": "First Fill",
                "event_type": RxEventType.FILL.value,
                "product": "rxmembersim",
                "delay": {"days": 1, "days_min": 0, "days_max": 3, "distribution": "uniform"},
                "depends_on": "prescription",
            },
            {
                "event_id": "therapy_start",
                "name": "Therapy Started",
                "event_type": RxEventType.THERAPY_START.value,
                "product": "rxmembersim",
                "delay": {"days": 0},
                "depends_on": "first_fill",
            },
            {
                "event_id": "refill_1",
                "name": "First Refill",
                "event_type": RxEventType.REFILL.value,
                "product": "rxmembersim",
                "delay": {"days": 28, "days_min": 25, "days_max": 35, "distribution": "uniform"},
                "depends_on": "first_fill",
                "probability": 0.85,
            },
            {
                "event_id": "fill_2",
                "name": "Second Fill",
                "event_type": RxEventType.FILL.value,
                "product": "rxmembersim",
                "delay": {"days": 1, "days_min": 0, "days_max": 2, "distribution": "uniform"},
                "depends_on": "refill_1",
            },
            {
                "event_id": "refill_2",
                "name": "Second Refill",
                "event_type": RxEventType.REFILL.value,
                "product": "rxmembersim",
                "delay": {"days": 28, "days_min": 25, "days_max": 35, "distribution": "uniform"},
                "depends_on": "fill_2",
                "probability": 0.80,
            },
            {
                "event_id": "fill_3",
                "name": "Third Fill",
                "event_type": RxEventType.FILL.value,
                "product": "rxmembersim",
                "delay": {"days": 1, "days_min": 0, "days_max": 2, "distribution": "uniform"},
                "depends_on": "refill_2",
            },
        ],
    },
    
    "chronic-therapy-maintenance": {
        "journey_id": "chronic-therapy-maintenance",
        "name": "Chronic Therapy Maintenance",
        "description": "Ongoing therapy for chronic condition management (90-day fills)",
        "products": ["rxmembersim"],
        "duration_days": 365,
        "events": [
            {
                "event_id": "prescription",
                "name": "Chronic Rx Written",
                "event_type": RxEventType.NEW_RX.value,
                "product": "rxmembersim",
                "delay": {"days": 0},
                "parameters": {
                    "quantity": 90,
                    "days_supply": 90,
                },
            },
            {
                "event_id": "fill_1",
                "name": "Initial 90-Day Fill",
                "event_type": RxEventType.FILL.value,
                "product": "rxmembersim",
                "delay": {"days": 1, "days_min": 0, "days_max": 3, "distribution": "uniform"},
                "depends_on": "prescription",
            },
            {
                "event_id": "refill_1",
                "name": "Refill 1 (Q2)",
                "event_type": RxEventType.REFILL.value,
                "product": "rxmembersim",
                "delay": {"days": 85, "days_min": 80, "days_max": 95, "distribution": "uniform"},
                "depends_on": "fill_1",
                "probability": 0.9,
            },
            {
                "event_id": "fill_2",
                "name": "Second 90-Day Fill",
                "event_type": RxEventType.FILL.value,
                "product": "rxmembersim",
                "delay": {"days": 1, "days_min": 0, "days_max": 2, "distribution": "uniform"},
                "depends_on": "refill_1",
            },
            {
                "event_id": "refill_2",
                "name": "Refill 2 (Q3)",
                "event_type": RxEventType.REFILL.value,
                "product": "rxmembersim",
                "delay": {"days": 85, "days_min": 80, "days_max": 95, "distribution": "uniform"},
                "depends_on": "fill_2",
                "probability": 0.85,
            },
            {
                "event_id": "fill_3",
                "name": "Third 90-Day Fill",
                "event_type": RxEventType.FILL.value,
                "product": "rxmembersim",
                "delay": {"days": 1, "days_min": 0, "days_max": 2, "distribution": "uniform"},
                "depends_on": "refill_2",
            },
            {
                "event_id": "refill_3",
                "name": "Refill 3 (Q4)",
                "event_type": RxEventType.REFILL.value,
                "product": "rxmembersim",
                "delay": {"days": 85, "days_min": 80, "days_max": 95, "distribution": "uniform"},
                "depends_on": "fill_3",
                "probability": 0.8,
            },
            {
                "event_id": "fill_4",
                "name": "Fourth 90-Day Fill",
                "event_type": RxEventType.FILL.value,
                "product": "rxmembersim",
                "delay": {"days": 1, "days_min": 0, "days_max": 2, "distribution": "uniform"},
                "depends_on": "refill_3",
            },
        ],
    },
    
    "specialty-onboarding": {
        "journey_id": "specialty-onboarding",
        "name": "Specialty Drug Onboarding",
        "description": "Complex journey for specialty medication with PA and hub enrollment",
        "products": ["rxmembersim", "membersim"],
        "duration_days": 90,
        "events": [
            {
                "event_id": "prescription",
                "name": "Specialty Rx Written",
                "event_type": RxEventType.NEW_RX.value,
                "product": "rxmembersim",
                "delay": {"days": 0},
                "parameters": {
                    "specialty": True,
                    "requires_pa": True,
                },
            },
            {
                "event_id": "benefits_investigation",
                "name": "Benefits Investigation",
                "event_type": "milestone",
                "product": "rxmembersim",
                "delay": {"days": 1, "days_min": 1, "days_max": 3, "distribution": "uniform"},
                "depends_on": "prescription",
            },
            {
                "event_id": "pa_submission",
                "name": "PA Submitted",
                "event_type": "milestone",
                "product": "rxmembersim",
                "delay": {"days": 3, "days_min": 2, "days_max": 5, "distribution": "uniform"},
                "depends_on": "benefits_investigation",
            },
            {
                "event_id": "pa_decision",
                "name": "PA Approved",
                "event_type": "milestone",
                "product": "rxmembersim",
                "delay": {"days": 5, "days_min": 3, "days_max": 14, "distribution": "uniform"},
                "depends_on": "pa_submission",
                "probability": 0.85,
            },
            {
                "event_id": "hub_enrollment",
                "name": "Hub/Patient Support Enrollment",
                "event_type": "milestone",
                "product": "rxmembersim",
                "delay": {"days": 2, "days_min": 1, "days_max": 5, "distribution": "uniform"},
                "depends_on": "pa_decision",
            },
            {
                "event_id": "copay_assistance",
                "name": "Copay Assistance Applied",
                "event_type": "milestone",
                "product": "rxmembersim",
                "delay": {"days": 1, "days_min": 0, "days_max": 3, "distribution": "uniform"},
                "depends_on": "hub_enrollment",
                "probability": 0.6,
            },
            {
                "event_id": "first_fill",
                "name": "First Specialty Fill",
                "event_type": RxEventType.FILL.value,
                "product": "rxmembersim",
                "delay": {"days": 5, "days_min": 3, "days_max": 10, "distribution": "uniform"},
                "depends_on": "pa_decision",
            },
            {
                "event_id": "therapy_start",
                "name": "Specialty Therapy Started",
                "event_type": RxEventType.THERAPY_START.value,
                "product": "rxmembersim",
                "delay": {"days": 0},
                "depends_on": "first_fill",
            },
            {
                "event_id": "welcome_call",
                "name": "Nurse Welcome Call",
                "event_type": "milestone",
                "product": "rxmembersim",
                "delay": {"days": 3, "days_min": 1, "days_max": 7, "distribution": "uniform"},
                "depends_on": "therapy_start",
            },
        ],
    },
    
    "step-therapy": {
        "journey_id": "step-therapy",
        "name": "Step Therapy Journey",
        "description": "Journey through step therapy protocol with medication changes",
        "products": ["rxmembersim"],
        "duration_days": 120,
        "events": [
            {
                "event_id": "first_line_rx",
                "name": "First-Line Therapy Prescribed",
                "event_type": RxEventType.NEW_RX.value,
                "product": "rxmembersim",
                "delay": {"days": 0},
                "parameters": {
                    "step": 1,
                    "drug_class": "first_line",
                },
            },
            {
                "event_id": "first_fill",
                "name": "First-Line Fill",
                "event_type": RxEventType.FILL.value,
                "product": "rxmembersim",
                "delay": {"days": 1, "days_min": 0, "days_max": 3, "distribution": "uniform"},
                "depends_on": "first_line_rx",
            },
            {
                "event_id": "trial_period",
                "name": "30-Day Trial Period",
                "event_type": "milestone",
                "product": "rxmembersim",
                "delay": {"days": 30},
                "depends_on": "first_fill",
            },
            {
                "event_id": "therapy_failure",
                "name": "First-Line Therapy Failure",
                "event_type": RxEventType.THERAPY_DISCONTINUE.value,
                "product": "rxmembersim",
                "delay": {"days": 7, "days_min": 3, "days_max": 14, "distribution": "uniform"},
                "depends_on": "trial_period",
                "probability": 0.4,
                "parameters": {
                    "reason": "inadequate_response",
                },
            },
            {
                "event_id": "second_line_rx",
                "name": "Second-Line Therapy Prescribed",
                "event_type": RxEventType.NEW_RX.value,
                "product": "rxmembersim",
                "delay": {"days": 3, "days_min": 1, "days_max": 7, "distribution": "uniform"},
                "depends_on": "therapy_failure",
                "parameters": {
                    "step": 2,
                    "drug_class": "second_line",
                },
            },
            {
                "event_id": "therapy_change",
                "name": "Therapy Change Recorded",
                "event_type": RxEventType.THERAPY_CHANGE.value,
                "product": "rxmembersim",
                "delay": {"days": 0},
                "depends_on": "second_line_rx",
            },
            {
                "event_id": "second_fill",
                "name": "Second-Line Fill",
                "event_type": RxEventType.FILL.value,
                "product": "rxmembersim",
                "delay": {"days": 1, "days_min": 0, "days_max": 3, "distribution": "uniform"},
                "depends_on": "second_line_rx",
            },
        ],
    },
    
    "adherence-intervention": {
        "journey_id": "adherence-intervention",
        "name": "Adherence Intervention",
        "description": "Journey from adherence gap identification through intervention",
        "products": ["rxmembersim"],
        "duration_days": 60,
        "events": [
            {
                "event_id": "gap_detected",
                "name": "Adherence Gap Detected",
                "event_type": RxEventType.ADHERENCE_GAP.value,
                "product": "rxmembersim",
                "delay": {"days": 0},
                "parameters": {
                    "days_without_fill": 14,
                },
            },
            {
                "event_id": "outreach_1",
                "name": "First Outreach Attempt",
                "event_type": "milestone",
                "product": "rxmembersim",
                "delay": {"days": 3, "days_min": 1, "days_max": 5, "distribution": "uniform"},
                "depends_on": "gap_detected",
            },
            {
                "event_id": "outreach_2",
                "name": "Second Outreach Attempt",
                "event_type": "milestone",
                "product": "rxmembersim",
                "delay": {"days": 7, "days_min": 5, "days_max": 10, "distribution": "uniform"},
                "depends_on": "outreach_1",
                "probability": 0.6,
            },
            {
                "event_id": "refill_reminder",
                "name": "Automated Refill Reminder",
                "event_type": "milestone",
                "product": "rxmembersim",
                "delay": {"days": 2, "days_min": 1, "days_max": 3, "distribution": "uniform"},
                "depends_on": "outreach_1",
            },
            {
                "event_id": "refill",
                "name": "Refill Request",
                "event_type": RxEventType.REFILL.value,
                "product": "rxmembersim",
                "delay": {"days": 14, "days_min": 7, "days_max": 21, "distribution": "uniform"},
                "depends_on": "gap_detected",
                "probability": 0.7,
            },
            {
                "event_id": "fill",
                "name": "Gap Closure Fill",
                "event_type": RxEventType.FILL.value,
                "product": "rxmembersim",
                "delay": {"days": 1, "days_min": 0, "days_max": 2, "distribution": "uniform"},
                "depends_on": "refill",
            },
            {
                "event_id": "mpr_update",
                "name": "MPR Updated",
                "event_type": RxEventType.MPR_THRESHOLD.value,
                "product": "rxmembersim",
                "delay": {"days": 0},
                "depends_on": "fill",
                "parameters": {
                    "threshold": 0.8,
                },
            },
        ],
    },
    
    "therapy-discontinuation": {
        "journey_id": "therapy-discontinuation",
        "name": "Therapy Discontinuation",
        "description": "Journey for planned or unplanned therapy discontinuation",
        "products": ["rxmembersim"],
        "duration_days": 30,
        "events": [
            {
                "event_id": "last_fill",
                "name": "Final Fill",
                "event_type": RxEventType.FILL.value,
                "product": "rxmembersim",
                "delay": {"days": 0},
            },
            {
                "event_id": "discontinue_decision",
                "name": "Discontinuation Decision",
                "event_type": "milestone",
                "product": "rxmembersim",
                "delay": {"days": 7, "days_min": 0, "days_max": 14, "distribution": "uniform"},
                "depends_on": "last_fill",
            },
            {
                "event_id": "therapy_end",
                "name": "Therapy Discontinued",
                "event_type": RxEventType.THERAPY_DISCONTINUE.value,
                "product": "rxmembersim",
                "delay": {"days": 1, "days_min": 0, "days_max": 3, "distribution": "uniform"},
                "depends_on": "discontinue_decision",
                "parameters": {
                    "reason": "therapy_complete",
                },
            },
            {
                "event_id": "followup",
                "name": "Discontinuation Follow-up",
                "event_type": "milestone",
                "product": "rxmembersim",
                "delay": {"days": 7, "days_min": 3, "days_max": 14, "distribution": "uniform"},
                "depends_on": "therapy_end",
                "probability": 0.5,
            },
        ],
    },
}


# =============================================================================
# Template Access Functions
# =============================================================================

def get_rx_journey_template(template_name: str) -> JourneySpecification:
    """Get an RxMemberSim journey template by name.
    
    Args:
        template_name: Name of the template
        
    Returns:
        JourneySpecification
        
    Raises:
        ValueError: If template not found
        
    Example:
        >>> journey = get_rx_journey_template("new-therapy-start")
        >>> print(journey.name)
        "New Therapy Start"
    """
    if template_name not in RX_JOURNEY_TEMPLATES:
        available = ", ".join(RX_JOURNEY_TEMPLATES.keys())
        raise ValueError(f"Template '{template_name}' not found. Available: {available}")
    
    template = RX_JOURNEY_TEMPLATES[template_name]
    return create_simple_journey(
        journey_id=template["journey_id"],
        name=template["name"],
        events=template["events"],
        products=template.get("products"),
    )


def list_rx_journey_templates() -> dict[str, str]:
    """List available RxMemberSim journey templates.
    
    Returns:
        Dict mapping template name to description
        
    Example:
        >>> templates = list_rx_journey_templates()
        >>> for name, desc in templates.items():
        ...     print(f"{name}: {desc}")
    """
    return {
        name: template["description"]
        for name, template in RX_JOURNEY_TEMPLATES.items()
    }


# Convenience aliases for common templates
NEW_THERAPY_START = get_rx_journey_template("new-therapy-start")
CHRONIC_THERAPY_MAINTENANCE = get_rx_journey_template("chronic-therapy-maintenance")
SPECIALTY_ONBOARDING = get_rx_journey_template("specialty-onboarding")
STEP_THERAPY = get_rx_journey_template("step-therapy")
ADHERENCE_INTERVENTION = get_rx_journey_template("adherence-intervention")
THERAPY_DISCONTINUATION = get_rx_journey_template("therapy-discontinuation")
