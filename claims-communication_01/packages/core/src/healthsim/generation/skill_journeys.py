"""Skill-aware journey templates.

This module provides journey templates that use skill references
instead of hardcoded clinical codes. This allows:

1. Single source of truth: Clinical codes defined in skills
2. Context-aware resolution: Different codes based on entity attributes
3. Maintainability: Update codes in one place

Usage:
    from healthsim.generation.skill_journeys import SKILL_AWARE_TEMPLATES
    
    # Get a template
    template = SKILL_AWARE_TEMPLATES["diabetic-first-year-skill"]
"""

from __future__ import annotations


# =============================================================================
# Diabetes Care Journeys (Skill-Aware)
# =============================================================================

DIABETIC_FIRST_YEAR_SKILL = {
    "journey_id": "diabetic-first-year-skill",
    "name": "First Year of Diabetic Care (Skill-Aware)",
    "description": "Standard care journey for newly diagnosed Type 2 diabetes using skill references",
    "products": ["patientsim", "membersim"],
    "duration_days": 365,
    "events": [
        {
            "event_id": "initial_dx",
            "name": "Initial Diabetes Diagnosis",
            "event_type": "diagnosis",
            "product": "patientsim",
            "delay": {"days": 0},
            "parameters": {
                "skill_ref": {
                    "skill": "diabetes-management",
                    "lookup": "diagnosis_code",
                    "context": {"stage": "new_diagnosis"},
                    "fallback": {"icd10": "E11.9", "description": "Type 2 diabetes"},
                }
            },
        },
        {
            "event_id": "initial_a1c",
            "name": "Initial A1C Test",
            "event_type": "lab_order",
            "product": "patientsim",
            "delay": {"days": 0, "days_min": 0, "days_max": 7, "distribution": "uniform"},
            "depends_on": "initial_dx",
            "parameters": {
                "skill_ref": {
                    "skill": "diabetes-management",
                    "lookup": "loinc",
                    "context": {"test_type": "a1c"},
                    "fallback": {"loinc": "4548-4", "test_name": "Hemoglobin A1c"},
                }
            },
        },
        {
            "event_id": "metformin_start",
            "name": "Start Metformin",
            "event_type": "medication_order",
            "product": "patientsim",
            "delay": {"days": 3, "days_min": 1, "days_max": 7, "distribution": "uniform"},
            "depends_on": "initial_dx",
            "parameters": {
                "skill_ref": {
                    "skill": "diabetes-management",
                    "lookup": "first_line_medication",
                    "fallback": {"rxnorm": "860975", "drug_name": "Metformin 500 MG"},
                }
            },
        },
        {
            "event_id": "followup_1",
            "name": "3-Month Follow-up",
            "event_type": "encounter",
            "product": "patientsim",
            "delay": {"days": 90, "days_min": 80, "days_max": 100, "distribution": "uniform"},
            "depends_on": "initial_dx",
            "parameters": {
                "encounter_type": "outpatient",
                "reason": "Diabetes follow-up",
            },
        },
        {
            "event_id": "followup_a1c",
            "name": "3-Month A1C",
            "event_type": "lab_order",
            "product": "patientsim",
            "delay": {"days": 0},
            "depends_on": "followup_1",
            "parameters": {
                "skill_ref": {
                    "skill": "diabetes-management",
                    "lookup": "loinc",
                    "context": {"test_type": "a1c"},
                }
            },
        },
        {
            "event_id": "quality_gap",
            "name": "A1C Gap Identified",
            "event_type": "gap_identified",
            "product": "membersim",
            "delay": {"days": 30},
            "depends_on": "initial_dx",
            "probability": 0.3,
            "parameters": {
                "measure": "CDC",
                "description": "A1C not completed within 90 days",
            },
        },
        # 6-month events
        {
            "event_id": "followup_2",
            "name": "6-Month Follow-up",
            "event_type": "encounter",
            "product": "patientsim",
            "delay": {"days": 180, "days_min": 170, "days_max": 190, "distribution": "uniform"},
            "depends_on": "initial_dx",
            "parameters": {
                "encounter_type": "outpatient",
                "reason": "Diabetes management review",
            },
        },
        {
            "event_id": "medication_review",
            "name": "Medication Review",
            "event_type": "medication_order",
            "product": "patientsim",
            "delay": {"days": 0},
            "depends_on": "followup_2",
            "probability": 0.4,  # 40% chance of medication adjustment
            "parameters": {
                "skill_ref": {
                    "skill": "diabetes-management",
                    "lookup": "medication",
                    "context": {"therapy_stage": "${entity.control_status}"},
                }
            },
        },
        # Annual events
        {
            "event_id": "annual_eye_exam",
            "name": "Annual Dilated Eye Exam",
            "event_type": "referral",
            "product": "patientsim",
            "delay": {"days": 365, "days_min": 330, "days_max": 400, "distribution": "uniform"},
            "depends_on": "initial_dx",
            "parameters": {
                "specialty": "ophthalmology",
                "reason": "Diabetes - annual retinopathy screening",
            },
        },
        {
            "event_id": "annual_foot_exam",
            "name": "Annual Foot Exam",
            "event_type": "procedure",
            "product": "patientsim",
            "delay": {"days": 365, "days_min": 330, "days_max": 400, "distribution": "uniform"},
            "depends_on": "initial_dx",
            "parameters": {
                "procedure": "monofilament_test",
                "reason": "Diabetes - annual neuropathy screening",
            },
        },
    ],
}


# =============================================================================
# Chronic Kidney Disease Journeys (Skill-Aware)
# =============================================================================

CKD_MANAGEMENT_SKILL = {
    "journey_id": "ckd-management-skill",
    "name": "CKD Management Journey (Skill-Aware)",
    "description": "Chronic kidney disease monitoring and management using skill references",
    "products": ["patientsim", "membersim"],
    "duration_days": 365,
    "events": [
        {
            "event_id": "ckd_dx",
            "name": "CKD Diagnosis",
            "event_type": "diagnosis",
            "product": "patientsim",
            "delay": {"days": 0},
            "parameters": {
                "skill_ref": {
                    "skill": "chronic-kidney-disease",
                    "lookup": "diagnosis_code",
                    "context": {"stage": "${entity.ckd_stage}"},
                    "fallback": {"icd10": "N18.3", "description": "CKD Stage 3"},
                }
            },
        },
        {
            "event_id": "baseline_labs",
            "name": "Baseline Renal Function Labs",
            "event_type": "lab_order",
            "product": "patientsim",
            "delay": {"days": 0},
            "depends_on": "ckd_dx",
            "parameters": {
                "panel": "renal_function",
                "tests": ["creatinine", "eGFR", "BUN", "urine_albumin"],
            },
        },
        {
            "event_id": "nephrology_referral",
            "name": "Nephrology Referral",
            "event_type": "referral",
            "product": "patientsim",
            "delay": {"days": 14, "days_min": 7, "days_max": 30, "distribution": "uniform"},
            "depends_on": "ckd_dx",
            "probability": 0.6,  # Stage 3b+ usually gets referral
            "parameters": {
                "specialty": "nephrology",
                "reason": "CKD management evaluation",
            },
        },
        {
            "event_id": "quarterly_labs",
            "name": "Quarterly Renal Labs",
            "event_type": "lab_order",
            "product": "patientsim",
            "delay": {"days": 90, "days_min": 80, "days_max": 100, "distribution": "uniform"},
            "depends_on": "ckd_dx",
            "parameters": {
                "panel": "renal_function",
                "tests": ["creatinine", "eGFR"],
            },
        },
    ],
}


# =============================================================================
# Heart Failure Journeys (Skill-Aware)
# =============================================================================

HF_MANAGEMENT_SKILL = {
    "journey_id": "hf-management-skill",
    "name": "Heart Failure Management Journey (Skill-Aware)",
    "description": "Heart failure monitoring and management using skill references",
    "products": ["patientsim", "membersim"],
    "duration_days": 365,
    "events": [
        {
            "event_id": "hf_dx",
            "name": "Heart Failure Diagnosis",
            "event_type": "diagnosis",
            "product": "patientsim",
            "delay": {"days": 0},
            "parameters": {
                "skill_ref": {
                    "skill": "heart-failure",
                    "lookup": "diagnosis_code",
                    "context": {"type": "${entity.hf_type}"},
                    "fallback": {"icd10": "I50.9", "description": "Heart failure, unspecified"},
                }
            },
        },
        {
            "event_id": "baseline_echo",
            "name": "Baseline Echocardiogram",
            "event_type": "procedure",
            "product": "patientsim",
            "delay": {"days": 7, "days_min": 0, "days_max": 14, "distribution": "uniform"},
            "depends_on": "hf_dx",
            "parameters": {
                "procedure_code": "93306",
                "procedure_name": "Echocardiography, transthoracic",
            },
        },
        {
            "event_id": "bnp_baseline",
            "name": "Baseline BNP",
            "event_type": "lab_order",
            "product": "patientsim",
            "delay": {"days": 0},
            "depends_on": "hf_dx",
            "parameters": {
                "loinc": "30934-4",
                "test_name": "BNP",
            },
        },
        {
            "event_id": "gdmt_start",
            "name": "Start GDMT",
            "event_type": "medication_order",
            "product": "patientsim",
            "delay": {"days": 3, "days_min": 1, "days_max": 7, "distribution": "uniform"},
            "depends_on": "hf_dx",
            "parameters": {
                "skill_ref": {
                    "skill": "heart-failure",
                    "lookup": "first_line_medication",
                    "fallback": {"rxnorm": "197361", "drug_name": "Lisinopril 5 MG"},
                }
            },
        },
    ],
}


# =============================================================================
# RxMemberSim Pharmacy Journeys (Skill-Aware)
# =============================================================================

PHARMACY_ADHERENCE_SKILL = {
    "journey_id": "pharmacy-adherence-skill",
    "name": "Pharmacy Adherence Journey (Skill-Aware)",
    "description": "Medication adherence monitoring using skill references",
    "products": ["rxmembersim"],
    "duration_days": 180,
    "events": [
        {
            "event_id": "initial_fill",
            "name": "Initial Fill",
            "event_type": "fill",
            "product": "rxmembersim",
            "delay": {"days": 0},
            "parameters": {
                "skill_ref": {
                    "skill": "diabetes-management",
                    "lookup": "first_line_medication",
                },
                "days_supply": 30,
                "quantity": 60,
            },
        },
        {
            "event_id": "refill_1",
            "name": "First Refill",
            "event_type": "refill",
            "product": "rxmembersim",
            "delay": {"days": 30, "days_min": 25, "days_max": 35, "distribution": "uniform"},
            "depends_on": "initial_fill",
            "parameters": {
                "days_supply": 30,
            },
        },
        {
            "event_id": "refill_2",
            "name": "Second Refill",
            "event_type": "refill",
            "product": "rxmembersim",
            "delay": {"days": 30, "days_min": 25, "days_max": 40, "distribution": "uniform"},
            "depends_on": "refill_1",
            "probability": 0.85,  # 15% chance of non-adherence
            "parameters": {
                "days_supply": 30,
            },
        },
        {
            "event_id": "refill_3",
            "name": "Third Refill",
            "event_type": "refill",
            "product": "rxmembersim",
            "delay": {"days": 30, "days_min": 25, "days_max": 45, "distribution": "uniform"},
            "depends_on": "refill_2",
            "probability": 0.80,  # Adherence drops over time
            "parameters": {
                "days_supply": 30,
            },
        },
        {
            "event_id": "adherence_outreach",
            "name": "Adherence Outreach",
            "event_type": "outreach",
            "product": "rxmembersim",
            "delay": {"days": 100, "days_min": 90, "days_max": 120, "distribution": "uniform"},
            "depends_on": "initial_fill",
            "probability": 0.3,  # Only triggered for some patients
            "parameters": {
                "outreach_type": "phone",
                "reason": "PDC below threshold",
            },
        },
    ],
}


# =============================================================================
# All Skill-Aware Templates
# =============================================================================

SKILL_AWARE_TEMPLATES = {
    # Diabetes
    "diabetic-first-year-skill": DIABETIC_FIRST_YEAR_SKILL,
    
    # CKD
    "ckd-management-skill": CKD_MANAGEMENT_SKILL,
    
    # Heart Failure
    "hf-management-skill": HF_MANAGEMENT_SKILL,
    
    # Pharmacy
    "pharmacy-adherence-skill": PHARMACY_ADHERENCE_SKILL,
}


def list_skill_aware_templates() -> list[str]:
    """List available skill-aware templates."""
    return list(SKILL_AWARE_TEMPLATES.keys())


def get_skill_aware_template(name: str) -> dict | None:
    """Get a skill-aware template by name."""
    return SKILL_AWARE_TEMPLATES.get(name)


__all__ = [
    "SKILL_AWARE_TEMPLATES",
    "DIABETIC_FIRST_YEAR_SKILL",
    "CKD_MANAGEMENT_SKILL",
    "HF_MANAGEMENT_SKILL",
    "PHARMACY_ADHERENCE_SKILL",
    "list_skill_aware_templates",
    "get_skill_aware_template",
]
