"""Auto-resolution journey templates.

These templates use the `condition` field for automatic skill resolution,
making them simpler and more maintainable than explicit skill_ref templates.

Instead of:
    "parameters": {
        "skill_ref": {
            "skill": "diabetes-management",
            "lookup": "diagnosis_code",
        }
    }

You just write:
    "condition": "diabetes"

The SkillRegistry automatically finds the right skill and lookup.

Usage:
    from healthsim.generation.auto_journeys import AUTO_RESOLUTION_TEMPLATES
    
    template = AUTO_RESOLUTION_TEMPLATES["diabetic-care-auto"]
    journey = JourneySpecification.model_validate(template)
"""

from __future__ import annotations


# =============================================================================
# Diabetes Care (Auto-Resolution)
# =============================================================================

DIABETIC_CARE_AUTO = {
    "journey_id": "diabetic-care-auto",
    "name": "Diabetic Care Journey (Auto-Resolution)",
    "description": "First year of diabetes care using automatic skill resolution",
    "products": ["patientsim", "membersim"],
    "duration_days": 365,
    "events": [
        {
            "event_id": "initial_dx",
            "name": "Initial Diabetes Diagnosis",
            "event_type": "diagnosis",
            "product": "patientsim",
            "delay": {"days": 0},
            "condition": "diabetes",
        },
        {
            "event_id": "initial_a1c",
            "name": "Initial A1C Test",
            "event_type": "lab_order",
            "product": "patientsim",
            "delay": {"days": 0, "days_min": 0, "days_max": 7, "distribution": "uniform"},
            "depends_on": "initial_dx",
            "condition": "diabetes",
        },
        {
            "event_id": "metformin_start",
            "name": "Start Metformin",
            "event_type": "medication_order",
            "product": "patientsim",
            "delay": {"days": 3, "days_min": 1, "days_max": 7, "distribution": "uniform"},
            "depends_on": "initial_dx",
            "condition": "diabetes",
        },
        {
            "event_id": "followup_1",
            "name": "3-Month Follow-up",
            "event_type": "encounter",
            "product": "patientsim",
            "delay": {"days": 90, "days_min": 80, "days_max": 100, "distribution": "uniform"},
            "depends_on": "initial_dx",
            "parameters": {"encounter_type": "outpatient", "reason": "Diabetes follow-up"},
        },
        {
            "event_id": "followup_a1c",
            "name": "3-Month A1C",
            "event_type": "lab_order",
            "product": "patientsim",
            "delay": {"days": 0},
            "depends_on": "followup_1",
            "condition": "diabetes",
        },
        {
            "event_id": "annual_eye",
            "name": "Annual Eye Exam",
            "event_type": "referral",
            "product": "patientsim",
            "delay": {"days": 365, "days_min": 330, "days_max": 400, "distribution": "uniform"},
            "depends_on": "initial_dx",
            "parameters": {"specialty": "ophthalmology", "reason": "Diabetic retinopathy screening"},
        },
    ],
}


# =============================================================================
# CKD Management (Auto-Resolution)
# =============================================================================

CKD_CARE_AUTO = {
    "journey_id": "ckd-care-auto",
    "name": "CKD Management Journey (Auto-Resolution)",
    "description": "Chronic kidney disease monitoring using automatic skill resolution",
    "products": ["patientsim", "membersim"],
    "duration_days": 365,
    "events": [
        {
            "event_id": "ckd_dx",
            "name": "CKD Diagnosis",
            "event_type": "diagnosis",
            "product": "patientsim",
            "delay": {"days": 0},
            "condition": "ckd",
        },
        {
            "event_id": "baseline_labs",
            "name": "Baseline Renal Labs",
            "event_type": "lab_order",
            "product": "patientsim",
            "delay": {"days": 0},
            "depends_on": "ckd_dx",
            "condition": "ckd",
        },
        {
            "event_id": "nephrology_referral",
            "name": "Nephrology Referral",
            "event_type": "referral",
            "product": "patientsim",
            "delay": {"days": 14, "days_min": 7, "days_max": 30, "distribution": "uniform"},
            "depends_on": "ckd_dx",
            "probability": 0.6,
            "parameters": {"specialty": "nephrology", "reason": "CKD evaluation"},
        },
        {
            "event_id": "quarterly_labs",
            "name": "Quarterly Labs",
            "event_type": "lab_order",
            "product": "patientsim",
            "delay": {"days": 90, "days_min": 80, "days_max": 100, "distribution": "uniform"},
            "depends_on": "ckd_dx",
            "condition": "ckd",
        },
    ],
}


# =============================================================================
# Heart Failure (Auto-Resolution)
# =============================================================================

HEART_FAILURE_AUTO = {
    "journey_id": "heart-failure-auto",
    "name": "Heart Failure Management (Auto-Resolution)",
    "description": "Heart failure care using automatic skill resolution",
    "products": ["patientsim", "membersim"],
    "duration_days": 365,
    "events": [
        {
            "event_id": "hf_dx",
            "name": "Heart Failure Diagnosis",
            "event_type": "diagnosis",
            "product": "patientsim",
            "delay": {"days": 0},
            "condition": "heart failure",
        },
        {
            "event_id": "baseline_echo",
            "name": "Baseline Echocardiogram",
            "event_type": "procedure",
            "product": "patientsim",
            "delay": {"days": 7, "days_min": 0, "days_max": 14, "distribution": "uniform"},
            "depends_on": "hf_dx",
            "condition": "heart failure",
        },
        {
            "event_id": "bnp_baseline",
            "name": "Baseline BNP",
            "event_type": "lab_order",
            "product": "patientsim",
            "delay": {"days": 0},
            "depends_on": "hf_dx",
            "condition": "heart failure",
        },
        {
            "event_id": "gdmt_start",
            "name": "Start GDMT",
            "event_type": "medication_order",
            "product": "patientsim",
            "delay": {"days": 3, "days_min": 1, "days_max": 7, "distribution": "uniform"},
            "depends_on": "hf_dx",
            "condition": "heart failure",
        },
        {
            "event_id": "cardiology_followup",
            "name": "Cardiology Follow-up",
            "event_type": "encounter",
            "product": "patientsim",
            "delay": {"days": 14, "days_min": 7, "days_max": 21, "distribution": "uniform"},
            "depends_on": "hf_dx",
            "parameters": {"encounter_type": "specialist", "specialty": "cardiology"},
        },
    ],
}


# =============================================================================
# Hypertension (Auto-Resolution)
# =============================================================================

HYPERTENSION_AUTO = {
    "journey_id": "hypertension-auto",
    "name": "Hypertension Management (Auto-Resolution)",
    "description": "Blood pressure management using automatic skill resolution",
    "products": ["patientsim", "membersim"],
    "duration_days": 365,
    "events": [
        {
            "event_id": "htn_dx",
            "name": "Hypertension Diagnosis",
            "event_type": "diagnosis",
            "product": "patientsim",
            "delay": {"days": 0},
            "condition": "hypertension",
        },
        {
            "event_id": "start_bp_med",
            "name": "Start BP Medication",
            "event_type": "medication_order",
            "product": "patientsim",
            "delay": {"days": 7, "days_min": 0, "days_max": 14, "distribution": "uniform"},
            "depends_on": "htn_dx",
            "condition": "hypertension",
        },
        {
            "event_id": "bp_check_1",
            "name": "2-Week BP Check",
            "event_type": "encounter",
            "product": "patientsim",
            "delay": {"days": 14, "days_min": 10, "days_max": 21, "distribution": "uniform"},
            "depends_on": "htn_dx",
            "parameters": {"encounter_type": "nurse_visit", "reason": "BP recheck"},
        },
        {
            "event_id": "monthly_followup",
            "name": "Monthly Follow-up",
            "event_type": "encounter",
            "product": "patientsim",
            "delay": {"days": 30, "days_min": 25, "days_max": 35, "distribution": "uniform"},
            "depends_on": "bp_check_1",
            "parameters": {"encounter_type": "outpatient"},
        },
    ],
}


# =============================================================================
# Multi-Condition Journey (Auto-Resolution)
# =============================================================================

MULTI_CONDITION_AUTO = {
    "journey_id": "multi-condition-auto",
    "name": "Multi-Condition Patient Journey",
    "description": "Patient with diabetes, hypertension, and CKD",
    "products": ["patientsim", "membersim"],
    "duration_days": 365,
    "events": [
        # Diabetes events
        {
            "event_id": "dm_dx",
            "name": "Diabetes Diagnosis",
            "event_type": "diagnosis",
            "product": "patientsim",
            "delay": {"days": 0},
            "condition": "diabetes",
        },
        # Hypertension events
        {
            "event_id": "htn_dx",
            "name": "Hypertension Diagnosis",
            "event_type": "diagnosis",
            "product": "patientsim",
            "delay": {"days": 30},
            "condition": "hypertension",
        },
        # CKD events (discovered during diabetes workup)
        {
            "event_id": "ckd_dx",
            "name": "CKD Diagnosis",
            "event_type": "diagnosis",
            "product": "patientsim",
            "delay": {"days": 60, "days_min": 45, "days_max": 90, "distribution": "uniform"},
            "depends_on": "dm_dx",
            "condition": "ckd",
        },
        # Labs combining conditions
        {
            "event_id": "comprehensive_labs",
            "name": "Comprehensive Labs",
            "event_type": "lab_order",
            "product": "patientsim",
            "delay": {"days": 90, "days_min": 80, "days_max": 100, "distribution": "uniform"},
            "depends_on": "dm_dx",
            "parameters": {
                "panel": "comprehensive",
                "tests": ["a1c", "cmp", "lipid", "urine_albumin"],
            },
        },
    ],
}


# =============================================================================
# RxMemberSim Pharmacy Journey (Auto-Resolution)
# =============================================================================

PHARMACY_DIABETES_AUTO = {
    "journey_id": "pharmacy-diabetes-auto",
    "name": "Diabetes Pharmacy Journey (Auto-Resolution)",
    "description": "Pharmacy adherence for diabetes medications",
    "products": ["rxmembersim"],
    "duration_days": 180,
    "events": [
        {
            "event_id": "initial_fill",
            "name": "Initial Fill",
            "event_type": "fill",
            "product": "rxmembersim",
            "delay": {"days": 0},
            "condition": "diabetes",
            "parameters": {"days_supply": 30, "quantity": 60},
        },
        {
            "event_id": "refill_1",
            "name": "First Refill",
            "event_type": "refill",
            "product": "rxmembersim",
            "delay": {"days": 30, "days_min": 25, "days_max": 35, "distribution": "uniform"},
            "depends_on": "initial_fill",
            "condition": "diabetes",
            "parameters": {"days_supply": 30},
        },
        {
            "event_id": "refill_2",
            "name": "Second Refill",
            "event_type": "refill",
            "product": "rxmembersim",
            "delay": {"days": 30, "days_min": 25, "days_max": 40, "distribution": "uniform"},
            "depends_on": "refill_1",
            "probability": 0.85,
            "condition": "diabetes",
            "parameters": {"days_supply": 30},
        },
    ],
}


# =============================================================================
# TrialSim Clinical Trial Journey (Auto-Resolution)
# =============================================================================

TRIAL_DIABETES_AUTO = {
    "journey_id": "trial-diabetes-auto",
    "name": "Diabetes Clinical Trial (Auto-Resolution)",
    "description": "Clinical trial subject journey for diabetes study",
    "products": ["trialsim", "patientsim"],
    "duration_days": 365,
    "events": [
        {
            "event_id": "screening",
            "name": "Screening Visit",
            "event_type": "screening",
            "product": "trialsim",
            "delay": {"days": 0},
            "parameters": {"pass_rate": 0.75},
        },
        {
            "event_id": "confirm_dx",
            "name": "Confirm Diabetes Diagnosis",
            "event_type": "diagnosis",
            "product": "patientsim",
            "delay": {"days": 0},
            "depends_on": "screening",
            "condition": "diabetes",
        },
        {
            "event_id": "baseline_a1c",
            "name": "Baseline A1C",
            "event_type": "lab_order",
            "product": "patientsim",
            "delay": {"days": 0},
            "depends_on": "confirm_dx",
            "condition": "diabetes",
        },
        {
            "event_id": "randomization",
            "name": "Randomization",
            "event_type": "randomization",
            "product": "trialsim",
            "delay": {"days": 14, "days_min": 7, "days_max": 28, "distribution": "uniform"},
            "depends_on": "screening",
            "parameters": {"arm_weights": {"Treatment": 0.5, "Placebo": 0.5}},
        },
        {
            "event_id": "week12_visit",
            "name": "Week 12 Visit",
            "event_type": "scheduled_visit",
            "product": "trialsim",
            "delay": {"days": 84, "days_min": 77, "days_max": 91, "distribution": "uniform"},
            "depends_on": "randomization",
            "parameters": {"visit_number": 3, "visit_name": "Week 12"},
        },
        {
            "event_id": "week12_a1c",
            "name": "Week 12 A1C",
            "event_type": "lab_order",
            "product": "patientsim",
            "delay": {"days": 0},
            "depends_on": "week12_visit",
            "condition": "diabetes",
        },
    ],
}


# =============================================================================
# All Auto-Resolution Templates
# =============================================================================

AUTO_RESOLUTION_TEMPLATES = {
    # Diabetes
    "diabetic-care-auto": DIABETIC_CARE_AUTO,
    
    # CKD
    "ckd-care-auto": CKD_CARE_AUTO,
    
    # Heart Failure
    "heart-failure-auto": HEART_FAILURE_AUTO,
    
    # Hypertension
    "hypertension-auto": HYPERTENSION_AUTO,
    
    # Multi-condition
    "multi-condition-auto": MULTI_CONDITION_AUTO,
    
    # Pharmacy
    "pharmacy-diabetes-auto": PHARMACY_DIABETES_AUTO,
    
    # Clinical Trial
    "trial-diabetes-auto": TRIAL_DIABETES_AUTO,
}


def list_auto_templates() -> list[str]:
    """List available auto-resolution templates."""
    return list(AUTO_RESOLUTION_TEMPLATES.keys())


def get_auto_template(name: str) -> dict | None:
    """Get an auto-resolution template by name."""
    return AUTO_RESOLUTION_TEMPLATES.get(name)


__all__ = [
    "AUTO_RESOLUTION_TEMPLATES",
    "DIABETIC_CARE_AUTO",
    "CKD_CARE_AUTO",
    "HEART_FAILURE_AUTO",
    "HYPERTENSION_AUTO",
    "MULTI_CONDITION_AUTO",
    "PHARMACY_DIABETES_AUTO",
    "TRIAL_DIABETES_AUTO",
    "list_auto_templates",
    "get_auto_template",
]
