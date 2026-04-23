"""TrialSim journey templates.

Pre-built journey specifications for common clinical trial protocols.
These templates can be used directly or customized for specific needs.
"""

from healthsim.generation.journey_engine import (
    JourneySpecification,
    EventDefinition,
    DelaySpec,
    EventCondition,
    TrialEventType,
    create_simple_journey,
)


# =============================================================================
# Journey Template Definitions
# =============================================================================

TRIAL_JOURNEY_TEMPLATES = {
    "phase3-oncology-standard": {
        "journey_id": "phase3-oncology-standard",
        "name": "Phase 3 Oncology Standard Protocol",
        "description": "Standard Phase 3 oncology trial with 24-week treatment period",
        "products": ["trialsim"],
        "duration_days": 365,
        "events": [
            {
                "event_id": "screening",
                "name": "Screening Visit",
                "event_type": TrialEventType.SCREENING.value,
                "product": "trialsim",
                "delay": {"days": 0},
                "parameters": {
                    "pass_rate": 0.75,
                },
            },
            {
                "event_id": "randomization",
                "name": "Randomization",
                "event_type": TrialEventType.RANDOMIZATION.value,
                "product": "trialsim",
                "delay": {"days": 14, "days_min": 7, "days_max": 21},
                "depends_on": "screening",
                "parameters": {
                    "arm_weights": {"Treatment": 0.67, "Placebo": 0.33},
                },
            },
            {
                "event_id": "visit_1",
                "name": "Week 1 Visit",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 7, "days_min": 5, "days_max": 9},
                "depends_on": "randomization",
                "parameters": {
                    "visit_number": 1,
                    "visit_name": "Week 1",
                    "procedures": ["vital_signs", "labs", "ecg"],
                },
            },
            {
                "event_id": "visit_2",
                "name": "Week 4 Visit",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 28, "days_min": 25, "days_max": 31},
                "depends_on": "randomization",
                "parameters": {
                    "visit_number": 2,
                    "visit_name": "Week 4",
                    "procedures": ["vital_signs", "labs", "tumor_assessment"],
                },
            },
            {
                "event_id": "visit_3",
                "name": "Week 8 Visit",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 56, "days_min": 52, "days_max": 60},
                "depends_on": "randomization",
                "parameters": {
                    "visit_number": 3,
                    "visit_name": "Week 8",
                    "procedures": ["vital_signs", "labs", "tumor_assessment", "imaging"],
                },
            },
            {
                "event_id": "visit_4",
                "name": "Week 12 Visit",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 84, "days_min": 80, "days_max": 88},
                "depends_on": "randomization",
                "parameters": {
                    "visit_number": 4,
                    "visit_name": "Week 12",
                    "procedures": ["vital_signs", "labs", "tumor_assessment"],
                },
            },
            {
                "event_id": "visit_5",
                "name": "Week 16 Visit",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 112, "days_min": 108, "days_max": 116},
                "depends_on": "randomization",
                "parameters": {
                    "visit_number": 5,
                    "visit_name": "Week 16",
                    "procedures": ["vital_signs", "labs", "tumor_assessment", "imaging"],
                },
            },
            {
                "event_id": "visit_6",
                "name": "Week 24 Visit (End of Treatment)",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 168, "days_min": 164, "days_max": 172},
                "depends_on": "randomization",
                "parameters": {
                    "visit_number": 6,
                    "visit_name": "Week 24 (EOT)",
                    "procedures": ["vital_signs", "labs", "tumor_assessment", "imaging", "ecg"],
                },
            },
            {
                "event_id": "followup_1",
                "name": "Safety Follow-up Visit",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 196, "days_min": 190, "days_max": 200},
                "depends_on": "visit_6",
                "parameters": {
                    "visit_number": 7,
                    "visit_name": "Safety Follow-up",
                    "procedures": ["vital_signs", "labs", "ae_review"],
                },
            },
        ],
    },
    
    "phase1-dose-escalation": {
        "journey_id": "phase1-dose-escalation",
        "name": "Phase 1 Dose Escalation Study",
        "description": "First-in-human dose escalation with DLT evaluation",
        "products": ["trialsim"],
        "duration_days": 84,
        "events": [
            {
                "event_id": "screening",
                "name": "Screening Visit",
                "event_type": TrialEventType.SCREENING.value,
                "product": "trialsim",
                "delay": {"days": 0},
                "parameters": {
                    "pass_rate": 0.60,
                },
            },
            {
                "event_id": "baseline",
                "name": "Baseline/Day 1",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 7, "days_min": 3, "days_max": 14},
                "depends_on": "screening",
                "parameters": {
                    "visit_number": 1,
                    "visit_name": "Baseline/Day 1",
                    "procedures": ["vital_signs", "labs", "pk_sample", "first_dose"],
                },
            },
            {
                "event_id": "day_2",
                "name": "Day 2 PK Visit",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 1},
                "depends_on": "baseline",
                "parameters": {
                    "visit_number": 2,
                    "visit_name": "Day 2",
                    "procedures": ["vital_signs", "pk_sample"],
                },
            },
            {
                "event_id": "day_8",
                "name": "Day 8 Visit",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 7, "days_min": 6, "days_max": 8},
                "depends_on": "baseline",
                "parameters": {
                    "visit_number": 3,
                    "visit_name": "Day 8",
                    "procedures": ["vital_signs", "labs", "pk_sample"],
                },
            },
            {
                "event_id": "day_15",
                "name": "Day 15 Visit",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 14, "days_min": 13, "days_max": 15},
                "depends_on": "baseline",
                "parameters": {
                    "visit_number": 4,
                    "visit_name": "Day 15",
                    "procedures": ["vital_signs", "labs", "pk_sample"],
                },
            },
            {
                "event_id": "day_21",
                "name": "Day 21 (DLT Evaluation)",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 21, "days_min": 20, "days_max": 22},
                "depends_on": "baseline",
                "parameters": {
                    "visit_number": 5,
                    "visit_name": "Day 21 (DLT Eval)",
                    "procedures": ["vital_signs", "labs", "dlt_assessment"],
                },
            },
            {
                "event_id": "day_28",
                "name": "Day 28 (End of Cycle 1)",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 28, "days_min": 27, "days_max": 29},
                "depends_on": "baseline",
                "parameters": {
                    "visit_number": 6,
                    "visit_name": "Day 28 (EOC1)",
                    "procedures": ["vital_signs", "labs", "pk_sample", "ecg"],
                },
            },
        ],
    },
    
    "phase2-efficacy": {
        "journey_id": "phase2-efficacy",
        "name": "Phase 2 Efficacy Study",
        "description": "Randomized Phase 2 study with efficacy endpoints",
        "products": ["trialsim"],
        "duration_days": 180,
        "events": [
            {
                "event_id": "screening",
                "name": "Screening Visit",
                "event_type": TrialEventType.SCREENING.value,
                "product": "trialsim",
                "delay": {"days": 0},
                "parameters": {
                    "pass_rate": 0.70,
                },
            },
            {
                "event_id": "randomization",
                "name": "Randomization",
                "event_type": TrialEventType.RANDOMIZATION.value,
                "product": "trialsim",
                "delay": {"days": 14, "days_min": 7, "days_max": 28},
                "depends_on": "screening",
                "parameters": {
                    "arm_weights": {"Treatment A": 0.33, "Treatment B": 0.33, "Placebo": 0.34},
                },
            },
            {
                "event_id": "week_2",
                "name": "Week 2 Visit",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 14, "days_min": 12, "days_max": 16},
                "depends_on": "randomization",
                "parameters": {
                    "visit_number": 1,
                    "visit_name": "Week 2",
                },
            },
            {
                "event_id": "week_4",
                "name": "Week 4 Visit",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 28, "days_min": 25, "days_max": 31},
                "depends_on": "randomization",
                "parameters": {
                    "visit_number": 2,
                    "visit_name": "Week 4",
                },
            },
            {
                "event_id": "week_8",
                "name": "Week 8 Visit",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 56, "days_min": 52, "days_max": 60},
                "depends_on": "randomization",
                "parameters": {
                    "visit_number": 3,
                    "visit_name": "Week 8",
                    "procedures": ["efficacy_assessment"],
                },
            },
            {
                "event_id": "week_12",
                "name": "Week 12 Visit (Primary Endpoint)",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 84, "days_min": 80, "days_max": 88},
                "depends_on": "randomization",
                "parameters": {
                    "visit_number": 4,
                    "visit_name": "Week 12 (Primary)",
                    "procedures": ["efficacy_assessment", "labs", "imaging"],
                },
            },
            {
                "event_id": "week_24",
                "name": "Week 24 Visit (End of Study)",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 168, "days_min": 164, "days_max": 172},
                "depends_on": "randomization",
                "parameters": {
                    "visit_number": 5,
                    "visit_name": "Week 24 (EOS)",
                    "procedures": ["efficacy_assessment", "labs", "imaging", "final_assessment"],
                },
            },
        ],
    },
    
    "simple-safety-followup": {
        "journey_id": "simple-safety-followup",
        "name": "Simple Safety Follow-up Protocol",
        "description": "Basic safety monitoring with quarterly visits",
        "products": ["trialsim"],
        "duration_days": 365,
        "events": [
            {
                "event_id": "screening",
                "name": "Screening",
                "event_type": TrialEventType.SCREENING.value,
                "product": "trialsim",
                "delay": {"days": 0},
            },
            {
                "event_id": "baseline",
                "name": "Baseline Visit",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 14},
                "depends_on": "screening",
                "parameters": {
                    "visit_number": 1,
                    "visit_name": "Baseline",
                },
            },
            {
                "event_id": "month_3",
                "name": "Month 3 Visit",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 90, "days_min": 80, "days_max": 100},
                "depends_on": "baseline",
                "parameters": {
                    "visit_number": 2,
                    "visit_name": "Month 3",
                },
            },
            {
                "event_id": "month_6",
                "name": "Month 6 Visit",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 180, "days_min": 170, "days_max": 190},
                "depends_on": "baseline",
                "parameters": {
                    "visit_number": 3,
                    "visit_name": "Month 6",
                },
            },
            {
                "event_id": "month_9",
                "name": "Month 9 Visit",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 270, "days_min": 260, "days_max": 280},
                "depends_on": "baseline",
                "parameters": {
                    "visit_number": 4,
                    "visit_name": "Month 9",
                },
            },
            {
                "event_id": "month_12",
                "name": "Month 12 Visit (End of Study)",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 365, "days_min": 350, "days_max": 380},
                "depends_on": "baseline",
                "parameters": {
                    "visit_number": 5,
                    "visit_name": "Month 12 (EOS)",
                },
            },
        ],
    },
    
    "ae-intensive-monitoring": {
        "journey_id": "ae-intensive-monitoring",
        "name": "Adverse Event Intensive Monitoring",
        "description": "Protocol with frequent AE assessment for high-risk treatments",
        "products": ["trialsim"],
        "duration_days": 56,
        "events": [
            {
                "event_id": "screening",
                "name": "Screening",
                "event_type": TrialEventType.SCREENING.value,
                "product": "trialsim",
                "delay": {"days": 0},
            },
            {
                "event_id": "baseline",
                "name": "Baseline/First Dose",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 7},
                "depends_on": "screening",
                "parameters": {
                    "visit_number": 1,
                    "visit_name": "Day 1",
                },
            },
            {
                "event_id": "day_3",
                "name": "Day 3 Safety Check",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 2},
                "depends_on": "baseline",
                "parameters": {
                    "visit_number": 2,
                    "visit_name": "Day 3",
                    "procedures": ["ae_assessment", "labs"],
                },
            },
            {
                "event_id": "day_7",
                "name": "Day 7 Safety Check",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 6},
                "depends_on": "baseline",
                "parameters": {
                    "visit_number": 3,
                    "visit_name": "Day 7",
                    "procedures": ["ae_assessment", "labs"],
                },
            },
            {
                "event_id": "day_14",
                "name": "Day 14 Visit",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 13},
                "depends_on": "baseline",
                "parameters": {
                    "visit_number": 4,
                    "visit_name": "Day 14",
                    "procedures": ["ae_assessment", "labs", "ecg"],
                },
            },
            {
                "event_id": "day_28",
                "name": "Day 28 Visit",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 27},
                "depends_on": "baseline",
                "parameters": {
                    "visit_number": 5,
                    "visit_name": "Day 28",
                    "procedures": ["ae_assessment", "labs", "ecg"],
                },
            },
            {
                "event_id": "day_56",
                "name": "Day 56 (End of Treatment)",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 55},
                "depends_on": "baseline",
                "parameters": {
                    "visit_number": 6,
                    "visit_name": "Day 56 (EOT)",
                    "procedures": ["ae_assessment", "labs", "ecg", "final_safety"],
                },
            },
        ],
    },
}


def get_trial_journey_template(template_id: str) -> dict | None:
    """Get a trial journey template by ID.
    
    Args:
        template_id: Template identifier (e.g., 'phase3-oncology-standard')
        
    Returns:
        Template dictionary or None if not found
    """
    return TRIAL_JOURNEY_TEMPLATES.get(template_id)


def list_trial_journey_templates() -> list[dict]:
    """List all available trial journey templates.
    
    Returns:
        List of template summaries with id, name, description
    """
    return [
        {
            "id": template_id,
            "name": template.get("name", template_id),
            "description": template.get("description", ""),
            "duration_days": template.get("duration_days", 0),
            "event_count": len(template.get("events", [])),
        }
        for template_id, template in TRIAL_JOURNEY_TEMPLATES.items()
    ]
