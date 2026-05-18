"""PatientSim journey templates.

Pre-built journey specifications for common clinical scenarios.
These templates can be used directly or customized for specific needs.
"""

from healthsim.generation.journey_engine import (
    JourneySpecification,
    EventDefinition,
    DelaySpec,
    EventCondition,
    PatientEventType,
    create_simple_journey,
)


# =============================================================================
# Journey Template Definitions
# =============================================================================

PATIENT_JOURNEY_TEMPLATES = {
    "diabetic-first-year": {
        "journey_id": "diabetic-first-year",
        "name": "Diabetic Patient First Year",
        "description": "Initial diabetes diagnosis through first year of management",
        "products": ["patientsim"],
        "duration_days": 365,
        "events": [
            {
                "event_id": "initial_encounter",
                "name": "Initial Presentation",
                "event_type": PatientEventType.ENCOUNTER.value,
                "product": "patientsim",
                "delay": {"days": 0},
                "parameters": {
                    "encounter_type": "outpatient",
                    "reason": "Fatigue, increased thirst",
                },
            },
            {
                "event_id": "initial_labs",
                "name": "Diagnostic Labs Ordered",
                "event_type": PatientEventType.LAB_ORDER.value,
                "product": "patientsim",
                "delay": {"days": 0},
                "depends_on": "initial_encounter",
                "parameters": {
                    "loinc": "4548-4",
                    "test_name": "Hemoglobin A1c",
                },
            },
            {
                "event_id": "lab_results",
                "name": "Lab Results Available",
                "event_type": PatientEventType.LAB_RESULT.value,
                "product": "patientsim",
                "delay": {"days": 2, "days_min": 1, "days_max": 3},
                "depends_on": "initial_labs",
                "parameters": {
                    "loinc": "4548-4",
                    "value_range": {"min": 7.0, "max": 10.0},
                },
            },
            {
                "event_id": "diagnosis",
                "name": "Diabetes Diagnosis",
                "event_type": PatientEventType.DIAGNOSIS.value,
                "product": "patientsim",
                "delay": {"days": 0},
                "depends_on": "lab_results",
                "parameters": {
                    "icd10": "E11.9",
                    "description": "Type 2 diabetes mellitus without complications",
                },
            },
            {
                "event_id": "medication_start",
                "name": "Metformin Started",
                "event_type": PatientEventType.MEDICATION_ORDER.value,
                "product": "patientsim",
                "delay": {"days": 0},
                "depends_on": "diagnosis",
                "parameters": {
                    "medication": "Metformin",
                    "ndc": "00093-7267-01",
                    "dose": "500mg",
                    "frequency": "twice daily",
                },
            },
            {
                "event_id": "followup_1",
                "name": "First Follow-up",
                "event_type": PatientEventType.ENCOUNTER.value,
                "product": "patientsim",
                "delay": {"days": 30, "days_min": 25, "days_max": 35},
                "depends_on": "medication_start",
            },
            {
                "event_id": "a1c_check_1",
                "name": "3-Month A1c Check",
                "event_type": PatientEventType.LAB_ORDER.value,
                "product": "patientsim",
                "delay": {"days": 90, "days_min": 85, "days_max": 100},
                "depends_on": "diagnosis",
            },
            {
                "event_id": "a1c_result_1",
                "name": "3-Month A1c Result",
                "event_type": PatientEventType.LAB_RESULT.value,
                "product": "patientsim",
                "delay": {"days": 2},
                "depends_on": "a1c_check_1",
            },
            {
                "event_id": "followup_2",
                "name": "Quarterly Follow-up",
                "event_type": PatientEventType.ENCOUNTER.value,
                "product": "patientsim",
                "delay": {"days": 180, "days_min": 170, "days_max": 190},
                "depends_on": "diagnosis",
            },
            {
                "event_id": "annual_eye_exam",
                "name": "Annual Eye Exam Referral",
                "event_type": PatientEventType.REFERRAL.value,
                "product": "patientsim",
                "delay": {"days": 270, "days_min": 250, "days_max": 300},
                "depends_on": "diagnosis",
                "parameters": {
                    "specialty": "Ophthalmology",
                    "reason": "Diabetic retinopathy screening",
                },
            },
            {
                "event_id": "a1c_check_2",
                "name": "Annual A1c Check",
                "event_type": PatientEventType.LAB_ORDER.value,
                "product": "patientsim",
                "delay": {"days": 365, "days_min": 350, "days_max": 380},
                "depends_on": "diagnosis",
            },
        ],
    },
    
    "surgical-episode": {
        "journey_id": "surgical-episode",
        "name": "Elective Surgery Episode",
        "description": "Pre-operative evaluation through post-surgical recovery",
        "products": ["patientsim"],
        "duration_days": 90,
        "events": [
            {
                "event_id": "surgical_consult",
                "name": "Surgical Consultation",
                "event_type": PatientEventType.ENCOUNTER.value,
                "product": "patientsim",
                "delay": {"days": 0},
                "parameters": {
                    "encounter_type": "outpatient",
                    "specialty": "Surgery",
                },
            },
            {
                "event_id": "preop_labs",
                "name": "Pre-operative Labs",
                "event_type": PatientEventType.LAB_ORDER.value,
                "product": "patientsim",
                "delay": {"days": 14, "days_min": 7, "days_max": 21},
                "depends_on": "surgical_consult",
                "parameters": {
                    "panel": "pre-operative",
                },
            },
            {
                "event_id": "preop_clearance",
                "name": "Pre-operative Clearance",
                "event_type": PatientEventType.ENCOUNTER.value,
                "product": "patientsim",
                "delay": {"days": 21, "days_min": 14, "days_max": 28},
                "depends_on": "surgical_consult",
                "parameters": {
                    "encounter_type": "outpatient",
                    "reason": "Pre-operative medical clearance",
                },
            },
            {
                "event_id": "admission",
                "name": "Hospital Admission",
                "event_type": PatientEventType.ADMISSION.value,
                "product": "patientsim",
                "delay": {"days": 30, "days_min": 28, "days_max": 35},
                "depends_on": "surgical_consult",
                "parameters": {
                    "admission_type": "elective",
                },
            },
            {
                "event_id": "surgery",
                "name": "Surgical Procedure",
                "event_type": PatientEventType.PROCEDURE.value,
                "product": "patientsim",
                "delay": {"days": 0},
                "depends_on": "admission",
                "parameters": {
                    "procedure_type": "surgical",
                },
            },
            {
                "event_id": "discharge",
                "name": "Hospital Discharge",
                "event_type": PatientEventType.DISCHARGE.value,
                "product": "patientsim",
                "delay": {"days": 2, "days_min": 1, "days_max": 5},
                "depends_on": "surgery",
                "parameters": {
                    "disposition": "home",
                },
            },
            {
                "event_id": "postop_1",
                "name": "First Post-op Visit",
                "event_type": PatientEventType.ENCOUNTER.value,
                "product": "patientsim",
                "delay": {"days": 7, "days_min": 5, "days_max": 10},
                "depends_on": "discharge",
            },
            {
                "event_id": "postop_2",
                "name": "Second Post-op Visit",
                "event_type": PatientEventType.ENCOUNTER.value,
                "product": "patientsim",
                "delay": {"days": 30, "days_min": 25, "days_max": 35},
                "depends_on": "discharge",
            },
            {
                "event_id": "postop_final",
                "name": "Final Post-op Clearance",
                "event_type": PatientEventType.ENCOUNTER.value,
                "product": "patientsim",
                "delay": {"days": 60, "days_min": 50, "days_max": 70},
                "depends_on": "discharge",
            },
        ],
    },
    
    "acute-care-episode": {
        "journey_id": "acute-care-episode",
        "name": "Acute Care Episode",
        "description": "Emergency presentation through hospitalization and discharge",
        "products": ["patientsim"],
        "duration_days": 30,
        "events": [
            {
                "event_id": "ed_arrival",
                "name": "ED Arrival",
                "event_type": PatientEventType.ENCOUNTER.value,
                "product": "patientsim",
                "delay": {"days": 0},
                "parameters": {
                    "encounter_type": "emergency",
                },
            },
            {
                "event_id": "ed_labs",
                "name": "ED Labs",
                "event_type": PatientEventType.LAB_ORDER.value,
                "product": "patientsim",
                "delay": {"hours": 1},
                "depends_on": "ed_arrival",
            },
            {
                "event_id": "ed_imaging",
                "name": "ED Imaging",
                "event_type": PatientEventType.PROCEDURE.value,
                "product": "patientsim",
                "delay": {"hours": 2},
                "depends_on": "ed_arrival",
                "parameters": {
                    "procedure_type": "imaging",
                },
            },
            {
                "event_id": "admission",
                "name": "Hospital Admission",
                "event_type": PatientEventType.ADMISSION.value,
                "product": "patientsim",
                "delay": {"hours": 6, "hours_min": 4, "hours_max": 12},
                "depends_on": "ed_arrival",
                "parameters": {
                    "admission_type": "emergency",
                },
            },
            {
                "event_id": "inpatient_labs",
                "name": "Daily Labs",
                "event_type": PatientEventType.LAB_ORDER.value,
                "product": "patientsim",
                "delay": {"days": 1},
                "depends_on": "admission",
            },
            {
                "event_id": "discharge",
                "name": "Hospital Discharge",
                "event_type": PatientEventType.DISCHARGE.value,
                "product": "patientsim",
                "delay": {"days": 3, "days_min": 2, "days_max": 7},
                "depends_on": "admission",
                "parameters": {
                    "disposition": "home",
                },
            },
            {
                "event_id": "followup",
                "name": "Post-Discharge Follow-up",
                "event_type": PatientEventType.ENCOUNTER.value,
                "product": "patientsim",
                "delay": {"days": 7, "days_min": 5, "days_max": 14},
                "depends_on": "discharge",
            },
        ],
    },
    
    "chronic-disease-management": {
        "journey_id": "chronic-disease-management",
        "name": "Chronic Disease Management",
        "description": "Ongoing quarterly visits for chronic condition management",
        "products": ["patientsim"],
        "duration_days": 365,
        "events": [
            {
                "event_id": "q1_visit",
                "name": "Q1 Visit",
                "event_type": PatientEventType.ENCOUNTER.value,
                "product": "patientsim",
                "delay": {"days": 0},
                "parameters": {
                    "encounter_type": "outpatient",
                    "reason": "Chronic disease management",
                },
            },
            {
                "event_id": "q1_labs",
                "name": "Q1 Labs",
                "event_type": PatientEventType.LAB_ORDER.value,
                "product": "patientsim",
                "delay": {"days": 0},
                "depends_on": "q1_visit",
            },
            {
                "event_id": "q2_visit",
                "name": "Q2 Visit",
                "event_type": PatientEventType.ENCOUNTER.value,
                "product": "patientsim",
                "delay": {"days": 90, "days_min": 80, "days_max": 100},
                "depends_on": "q1_visit",
            },
            {
                "event_id": "q2_labs",
                "name": "Q2 Labs",
                "event_type": PatientEventType.LAB_ORDER.value,
                "product": "patientsim",
                "delay": {"days": 0},
                "depends_on": "q2_visit",
            },
            {
                "event_id": "q3_visit",
                "name": "Q3 Visit",
                "event_type": PatientEventType.ENCOUNTER.value,
                "product": "patientsim",
                "delay": {"days": 180, "days_min": 170, "days_max": 190},
                "depends_on": "q1_visit",
            },
            {
                "event_id": "q3_labs",
                "name": "Q3 Labs",
                "event_type": PatientEventType.LAB_ORDER.value,
                "product": "patientsim",
                "delay": {"days": 0},
                "depends_on": "q3_visit",
            },
            {
                "event_id": "q4_visit",
                "name": "Q4/Annual Visit",
                "event_type": PatientEventType.ENCOUNTER.value,
                "product": "patientsim",
                "delay": {"days": 270, "days_min": 260, "days_max": 280},
                "depends_on": "q1_visit",
            },
            {
                "event_id": "q4_labs",
                "name": "Annual Labs",
                "event_type": PatientEventType.LAB_ORDER.value,
                "product": "patientsim",
                "delay": {"days": 0},
                "depends_on": "q4_visit",
            },
            {
                "event_id": "annual_review",
                "name": "Annual Care Plan Review",
                "event_type": PatientEventType.CARE_PLAN_UPDATE.value,
                "product": "patientsim",
                "delay": {"days": 365, "days_min": 350, "days_max": 380},
                "depends_on": "q1_visit",
            },
        ],
    },
    
    "wellness-visit": {
        "journey_id": "wellness-visit",
        "name": "Annual Wellness Visit",
        "description": "Preventive care with age-appropriate screenings",
        "products": ["patientsim"],
        "duration_days": 30,
        "events": [
            {
                "event_id": "wellness_encounter",
                "name": "Annual Wellness Encounter",
                "event_type": PatientEventType.ENCOUNTER.value,
                "product": "patientsim",
                "delay": {"days": 0},
                "parameters": {
                    "encounter_type": "wellness",
                    "reason": "Annual preventive care",
                },
            },
            {
                "event_id": "wellness_labs",
                "name": "Preventive Labs",
                "event_type": PatientEventType.LAB_ORDER.value,
                "product": "patientsim",
                "delay": {"days": 0},
                "depends_on": "wellness_encounter",
                "parameters": {
                    "panel": "preventive",
                },
            },
            {
                "event_id": "lab_results",
                "name": "Lab Results",
                "event_type": PatientEventType.LAB_RESULT.value,
                "product": "patientsim",
                "delay": {"days": 3, "days_min": 2, "days_max": 5},
                "depends_on": "wellness_labs",
            },
            {
                "event_id": "results_followup",
                "name": "Results Review (if needed)",
                "event_type": PatientEventType.ENCOUNTER.value,
                "product": "patientsim",
                "delay": {"days": 14, "days_min": 10, "days_max": 21},
                "depends_on": "lab_results",
                "conditions": [
                    {
                        "type": "parameter",
                        "parameter": "abnormal_results",
                        "operator": "equals",
                        "value": True,
                    }
                ],
            },
        ],
    },
}


def get_patient_journey_template(template_id: str) -> dict | None:
    """Get a patient journey template by ID.
    
    Args:
        template_id: Template identifier (e.g., 'diabetic-first-year')
        
    Returns:
        Template dictionary or None if not found
    """
    return PATIENT_JOURNEY_TEMPLATES.get(template_id)


def list_patient_journey_templates() -> list[dict]:
    """List all available patient journey templates.
    
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
        for template_id, template in PATIENT_JOURNEY_TEMPLATES.items()
    ]
