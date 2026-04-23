"""Pre-built patient profile templates for common scenarios.

This module provides ready-to-use profile templates for typical patient populations.
Templates can be used directly or customized for specific needs.

Example:
    >>> from patientsim.generation import get_template, list_templates
    >>> 
    >>> # List available templates
    >>> templates = list_templates()
    >>> print(templates)  # ['diabetic-senior', 'healthy-adult', ...]
    >>> 
    >>> # Get a specific template
    >>> spec = get_template("diabetic-senior")
    >>> spec.demographics.count = 500  # Customize
"""

from patientsim.generation.profiles import (
    EncounterSpec,
    PatientClinicalSpec,
    PatientDemographicsSpec,
    PatientGenerationSpec,
    PatientProfileSpecification,
)


# =============================================================================
# Template Definitions
# =============================================================================

DIABETIC_SENIOR = PatientProfileSpecification(
    id="diabetic-senior",
    name="Diabetic Senior Patients",
    description="Medicare-age patients with Type 2 diabetes and common comorbidities",
    demographics=PatientDemographicsSpec(
        age={"type": "normal", "mean": 72, "std_dev": 8, "min": 65, "max": 95},
        gender={"type": "categorical", "weights": {"M": 0.48, "F": 0.52}},
    ),
    clinical=PatientClinicalSpec(
        primary_condition={"code": "E11.9", "description": "Type 2 diabetes mellitus"},
        comorbidities=[
            {"code": "I10", "description": "Essential hypertension", "prevalence": 0.75},
            {"code": "E78.5", "description": "Hyperlipidemia", "prevalence": 0.65},
            {"code": "I25.10", "description": "Atherosclerotic heart disease", "prevalence": 0.30},
            {"code": "N18.3", "description": "Chronic kidney disease, stage 3", "prevalence": 0.25},
            {"code": "E66.9", "description": "Obesity", "prevalence": 0.40},
        ],
        encounter_pattern=EncounterSpec(
            encounter_class="outpatient",
            frequency={"type": "normal", "mean": 6, "std_dev": 2, "min": 2},
        ),
    ),
    generation=PatientGenerationSpec(
        count=100,
        include_encounters=True,
        include_medications=True,
        include_labs=True,
        include_vitals=True,
    ),
)


HEALTHY_ADULT = PatientProfileSpecification(
    id="healthy-adult",
    name="Healthy Adult Patients",
    description="Working-age adults with no significant medical history",
    demographics=PatientDemographicsSpec(
        age={"type": "uniform", "min": 25, "max": 55},
        gender={"type": "categorical", "weights": {"M": 0.50, "F": 0.50}},
    ),
    clinical=PatientClinicalSpec(
        encounter_pattern=EncounterSpec(
            encounter_class="outpatient",
            frequency={"type": "normal", "mean": 2, "std_dev": 1, "min": 0},
        ),
    ),
    generation=PatientGenerationSpec(
        count=100,
        include_encounters=True,
        include_medications=False,
        include_labs=True,
        include_vitals=True,
    ),
)


PEDIATRIC_ASTHMA = PatientProfileSpecification(
    id="pediatric-asthma",
    name="Pediatric Asthma Patients",
    description="Children with asthma requiring regular management",
    demographics=PatientDemographicsSpec(
        age={"type": "age_bands", "bands": {"5-10": 0.40, "11-14": 0.35, "15-17": 0.25}},
        gender={"type": "categorical", "weights": {"M": 0.55, "F": 0.45}},
        mrn_prefix="PEDS",
    ),
    clinical=PatientClinicalSpec(
        primary_condition={"code": "J45.20", "description": "Mild intermittent asthma"},
        comorbidities=[
            {"code": "J30.9", "description": "Allergic rhinitis", "prevalence": 0.60},
            {"code": "L20.9", "description": "Atopic dermatitis", "prevalence": 0.30},
        ],
        encounter_pattern=EncounterSpec(
            encounter_class="outpatient",
            frequency={"type": "normal", "mean": 4, "std_dev": 2, "min": 1},
        ),
    ),
    generation=PatientGenerationSpec(
        count=100,
        include_encounters=True,
        include_medications=True,
        include_labs=False,
        include_vitals=True,
    ),
)


ED_FREQUENT_FLYER = PatientProfileSpecification(
    id="ed-frequent-flyer",
    name="ED Frequent Flyer Patients",
    description="Patients with multiple ED visits per year, often with behavioral health needs",
    demographics=PatientDemographicsSpec(
        age={"type": "normal", "mean": 45, "std_dev": 15, "min": 18, "max": 75},
        gender={"type": "categorical", "weights": {"M": 0.55, "F": 0.45}},
    ),
    clinical=PatientClinicalSpec(
        primary_condition={"code": "F10.20", "description": "Alcohol dependence, uncomplicated"},
        comorbidities=[
            {"code": "F32.9", "description": "Major depressive disorder", "prevalence": 0.50},
            {"code": "F41.1", "description": "Generalized anxiety disorder", "prevalence": 0.40},
            {"code": "G43.909", "description": "Migraine, unspecified", "prevalence": 0.35},
            {"code": "M54.5", "description": "Low back pain", "prevalence": 0.55},
        ],
        encounter_pattern=EncounterSpec(
            encounter_class="emergency",
            frequency={"type": "normal", "mean": 8, "std_dev": 4, "min": 4},
        ),
    ),
    generation=PatientGenerationSpec(
        count=50,
        include_encounters=True,
        include_medications=True,
        include_labs=True,
        include_vitals=True,
    ),
)


SURGICAL_INPATIENT = PatientProfileSpecification(
    id="surgical-inpatient",
    name="Surgical Inpatient Patients",
    description="Patients admitted for elective surgical procedures",
    demographics=PatientDemographicsSpec(
        age={"type": "normal", "mean": 58, "std_dev": 12, "min": 30, "max": 80},
        gender={"type": "categorical", "weights": {"M": 0.52, "F": 0.48}},
    ),
    clinical=PatientClinicalSpec(
        comorbidities=[
            {"code": "I10", "description": "Essential hypertension", "prevalence": 0.45},
            {"code": "E11.9", "description": "Type 2 diabetes mellitus", "prevalence": 0.25},
            {"code": "E66.9", "description": "Obesity", "prevalence": 0.35},
        ],
        encounter_pattern=EncounterSpec(
            encounter_class="inpatient",
            duration={"type": "log_normal", "mean": 72, "sigma": 0.5, "min": 24},
        ),
    ),
    generation=PatientGenerationSpec(
        count=100,
        include_encounters=True,
        include_medications=True,
        include_labs=True,
        include_vitals=True,
        include_notes=True,
    ),
)


MATERNITY = PatientProfileSpecification(
    id="maternity",
    name="Maternity Patients",
    description="Pregnant patients for OB care and delivery",
    demographics=PatientDemographicsSpec(
        age={"type": "normal", "mean": 30, "std_dev": 5, "min": 18, "max": 45},
        gender={"type": "categorical", "weights": {"F": 1.0}},
        mrn_prefix="OB",
    ),
    clinical=PatientClinicalSpec(
        primary_condition={"code": "Z34.00", "description": "Supervision of normal pregnancy"},
        comorbidities=[
            {"code": "O24.410", "description": "Gestational diabetes mellitus", "prevalence": 0.15},
            {"code": "O13.9", "description": "Gestational hypertension", "prevalence": 0.10},
            {"code": "O99.810", "description": "Abnormal glucose complicating pregnancy", "prevalence": 0.08},
        ],
        encounter_pattern=EncounterSpec(
            encounter_class="outpatient",
            frequency={"type": "normal", "mean": 13, "std_dev": 2, "min": 10},  # Prenatal visits
        ),
    ),
    generation=PatientGenerationSpec(
        count=100,
        include_encounters=True,
        include_medications=True,
        include_labs=True,
        include_vitals=True,
    ),
)


ONCOLOGY = PatientProfileSpecification(
    id="oncology",
    name="Oncology Patients",
    description="Patients with cancer diagnoses requiring ongoing treatment",
    demographics=PatientDemographicsSpec(
        count=100,
        age={"type": "normal", "mean": 65, "std_dev": 12, "min": 30, "max": 90},
        gender={"type": "categorical", "weights": {"M": 0.48, "F": 0.52}},
        mrn_prefix="ONC",
    ),
    clinical=PatientClinicalSpec(
        primary_condition={"code": "C34.90", "description": "Malignant neoplasm of lung"},
        comorbidities=[
            {"code": "J44.9", "description": "COPD", "prevalence": 0.35},
            {"code": "D64.9", "description": "Anemia", "prevalence": 0.45},
            {"code": "R53.83", "description": "Fatigue", "prevalence": 0.70},
            {"code": "R63.0", "description": "Anorexia", "prevalence": 0.40},
        ],
        encounter_pattern=EncounterSpec(
            encounter_class="outpatient",
            frequency={"type": "normal", "mean": 18, "std_dev": 6, "min": 6},
        ),
    ),
    generation=PatientGenerationSpec(
        include_encounters=True,
        include_medications=True,
        include_labs=True,
        include_vitals=True,
        include_notes=True,
    ),
)


# =============================================================================
# Template Registry
# =============================================================================

PATIENT_PROFILE_TEMPLATES: dict[str, PatientProfileSpecification] = {
    "diabetic-senior": DIABETIC_SENIOR,
    "healthy-adult": HEALTHY_ADULT,
    "pediatric-asthma": PEDIATRIC_ASTHMA,
    "ed-frequent-flyer": ED_FREQUENT_FLYER,
    "surgical-inpatient": SURGICAL_INPATIENT,
    "maternity": MATERNITY,
    "oncology": ONCOLOGY,
}


def list_templates() -> list[str]:
    """List available template names.
    
    Returns:
        List of template IDs
    """
    return list(PATIENT_PROFILE_TEMPLATES.keys())


def get_template(name: str) -> PatientProfileSpecification:
    """Get a copy of a profile template by name.
    
    Args:
        name: Template ID
        
    Returns:
        Copy of the template specification
        
    Raises:
        KeyError: If template not found
    """
    if name not in PATIENT_PROFILE_TEMPLATES:
        available = ", ".join(list_templates())
        raise KeyError(f"Template '{name}' not found. Available: {available}")
    
    # Return a deep copy so modifications don't affect the original
    return PATIENT_PROFILE_TEMPLATES[name].model_copy(deep=True)


__all__ = [
    "PATIENT_PROFILE_TEMPLATES",
    "list_templates",
    "get_template",
    # Individual templates for direct access
    "DIABETIC_SENIOR",
    "HEALTHY_ADULT",
    "PEDIATRIC_ASTHMA",
    "ED_FREQUENT_FLYER",
    "SURGICAL_INPATIENT",
    "MATERNITY",
    "ONCOLOGY",
]
