"""Reference data for patient generation.

This module contains medical codes, laboratory reference ranges, medication
information, and other reference data used for generating realistic patient data.
"""

from dataclasses import dataclass


@dataclass
class ICD10Code:
    """ICD-10 diagnosis code with description."""

    code: str
    description: str
    category: str  # For grouping (diabetes, cardiac, respiratory, etc.)


@dataclass
class LabTest:
    """Laboratory test with reference range."""

    name: str
    loinc_code: str
    normal_min: float
    normal_max: float
    unit: str
    critical_low: float | None = None
    critical_high: float | None = None


@dataclass
class MedicationInfo:
    """Medication information."""

    name: str
    rxnorm_code: str
    common_doses: list[str]
    routes: list[str]
    frequencies: list[str]
    indication: str


# Common ICD-10 diagnosis codes
COMMON_DIAGNOSES = [
    # Diabetes
    ICD10Code("E11.9", "Type 2 diabetes mellitus without complications", "diabetes"),
    ICD10Code("E11.65", "Type 2 diabetes with hyperglycemia", "diabetes"),
    ICD10Code("E10.9", "Type 1 diabetes mellitus without complications", "diabetes"),
    # Hypertension
    ICD10Code("I10", "Essential (primary) hypertension", "cardiac"),
    ICD10Code("I11.9", "Hypertensive heart disease without heart failure", "cardiac"),
    # Cardiac
    ICD10Code("I25.10", "Atherosclerotic heart disease of native coronary artery", "cardiac"),
    ICD10Code("I48.91", "Atrial fibrillation, unspecified", "cardiac"),
    ICD10Code("I50.9", "Heart failure, unspecified", "cardiac"),
    # Respiratory
    ICD10Code(
        "J44.0",
        "Chronic obstructive pulmonary disease with acute lower respiratory infection",
        "respiratory",
    ),
    ICD10Code("J44.1", "COPD with acute exacerbation", "respiratory"),
    ICD10Code("J18.9", "Pneumonia, unspecified organism", "respiratory"),
    ICD10Code("J45.909", "Unspecified asthma, uncomplicated", "respiratory"),
    # Kidney
    ICD10Code("N18.3", "Chronic kidney disease, stage 3", "renal"),
    ICD10Code("N18.4", "Chronic kidney disease, stage 4", "renal"),
    ICD10Code("N17.9", "Acute kidney failure, unspecified", "renal"),
    # Infection
    ICD10Code("A41.9", "Sepsis, unspecified organism", "infection"),
    ICD10Code("A49.9", "Bacterial infection, unspecified", "infection"),
    # Other common
    ICD10Code("M79.3", "Panniculitis, unspecified", "musculoskeletal"),
    ICD10Code("E78.5", "Hyperlipidemia, unspecified", "metabolic"),
    ICD10Code("E66.9", "Obesity, unspecified", "metabolic"),
]


# Laboratory tests with reference ranges
LAB_TESTS = [
    # Basic Metabolic Panel (BMP)
    LabTest("Glucose", "2345-7", 70, 100, "mg/dL", 40, 400),
    LabTest("Sodium", "2951-2", 136, 145, "mmol/L", 120, 160),
    LabTest("Potassium", "2823-3", 3.5, 5.0, "mmol/L", 2.5, 6.5),
    LabTest("Chloride", "2075-0", 98, 107, "mmol/L", 80, 120),
    LabTest("CO2", "2028-9", 23, 29, "mmol/L", 15, 40),
    LabTest("BUN", "3094-0", 7, 20, "mg/dL", 3, 100),
    LabTest("Creatinine", "2160-0", 0.7, 1.3, "mg/dL", 0.4, 10),
    LabTest("Calcium", "17861-6", 8.5, 10.5, "mg/dL", 6.0, 14.0),
    # Complete Blood Count (CBC)
    LabTest("WBC", "6690-2", 4.5, 11.0, "x10^3/uL", 1.0, 50.0),
    LabTest("RBC", "789-8", 4.5, 5.9, "x10^6/uL", 2.0, 8.0),
    LabTest("Hemoglobin", "718-7", 13.5, 17.5, "g/dL", 7.0, 20.0),
    LabTest("Hematocrit", "4544-3", 39, 50, "%", 20, 65),
    LabTest("Platelets", "777-3", 150, 400, "x10^3/uL", 50, 1000),
    # Liver Function
    LabTest("ALT", "1742-6", 7, 56, "U/L", 0, 500),
    LabTest("AST", "1920-8", 10, 40, "U/L", 0, 500),
    LabTest("Bilirubin Total", "1975-2", 0.3, 1.2, "mg/dL", 0, 20),
    LabTest("Albumin", "1751-7", 3.5, 5.5, "g/dL", 2.0, 6.0),
    # Cardiac
    LabTest("Troponin I", "10839-9", 0, 0.04, "ng/mL", None, 10.0),
    LabTest("BNP", "30934-4", 0, 100, "pg/mL", None, 5000),
    # Other
    LabTest("CRP", "1988-5", 0, 3.0, "mg/L", None, 200),
    LabTest("HbA1c", "4548-4", 4.0, 5.6, "%", None, 15.0),
]


# Common medications
MEDICATIONS = [
    # Diabetes
    MedicationInfo(
        "Metformin",
        "860975",
        ["500 mg", "850 mg", "1000 mg"],
        ["PO"],
        ["BID", "TID"],
        "Type 2 diabetes",
    ),
    MedicationInfo(
        "Insulin Glargine",
        "274783",
        ["10 units", "20 units", "30 units"],
        ["SubQ"],
        ["QD"],
        "Diabetes",
    ),
    # Hypertension
    MedicationInfo(
        "Lisinopril",
        "104376",
        ["5 mg", "10 mg", "20 mg", "40 mg"],
        ["PO"],
        ["QD"],
        "Hypertension",
    ),
    MedicationInfo(
        "Amlodipine",
        "17767",
        ["2.5 mg", "5 mg", "10 mg"],
        ["PO"],
        ["QD"],
        "Hypertension",
    ),
    MedicationInfo(
        "Hydrochlorothiazide",
        "5487",
        ["12.5 mg", "25 mg", "50 mg"],
        ["PO"],
        ["QD"],
        "Hypertension",
    ),
    # Cardiac
    MedicationInfo(
        "Atorvastatin",
        "83367",
        ["10 mg", "20 mg", "40 mg", "80 mg"],
        ["PO"],
        ["QD"],
        "Hyperlipidemia",
    ),
    MedicationInfo(
        "Aspirin",
        "1191",
        ["81 mg", "325 mg"],
        ["PO"],
        ["QD"],
        "CAD prophylaxis",
    ),
    MedicationInfo(
        "Metoprolol",
        "6918",
        ["25 mg", "50 mg", "100 mg"],
        ["PO"],
        ["BID"],
        "Hypertension/CAD",
    ),
    # Respiratory
    MedicationInfo(
        "Albuterol",
        "435",
        ["90 mcg/actuation"],
        ["INH"],
        ["PRN"],
        "Asthma/COPD",
    ),
    MedicationInfo(
        "Fluticasone",
        "202318",
        ["110 mcg/actuation", "220 mcg/actuation"],
        ["INH"],
        ["BID"],
        "Asthma/COPD",
    ),
    # Infection
    MedicationInfo(
        "Azithromycin",
        "18631",
        ["250 mg", "500 mg"],
        ["PO"],
        ["QD"],
        "Bacterial infection",
    ),
    MedicationInfo(
        "Ceftriaxone",
        "2193",
        ["1 g", "2 g"],
        ["IV"],
        ["Q24H"],
        "Bacterial infection",
    ),
    MedicationInfo(
        "Vancomycin",
        "11124",
        ["1 g", "1.5 g"],
        ["IV"],
        ["Q12H"],
        "MRSA/serious infection",
    ),
]


# Vital sign reference ranges by age group
VITAL_RANGES: dict[str, dict[str, tuple[float, float] | tuple[int, int]]] = {
    "adult": {
        "temperature": (97.0, 99.5),  # Fahrenheit (float)
        "heart_rate": (60, 100),  # bpm (int)
        "respiratory_rate": (12, 20),  # per minute (int)
        "systolic_bp": (90, 140),  # mmHg (int)
        "diastolic_bp": (60, 90),  # mmHg (int)
        "spo2": (95, 100),  # percentage (int)
    },
    "pediatric": {
        "temperature": (97.0, 99.5),
        "heart_rate": (70, 120),
        "respiratory_rate": (20, 30),
        "systolic_bp": (80, 120),
        "diastolic_bp": (50, 80),
        "spo2": (95, 100),
    },
}


# Common clinical scenarios with associated conditions
CLINICAL_SCENARIOS = {
    "sepsis": {
        "primary_diagnosis": "A41.9",
        "likely_labs": ["WBC", "CRP", "Lactate"],
        "abnormal_vitals": ["temperature", "heart_rate", "respiratory_rate"],
        "typical_meds": ["Ceftriaxone", "Vancomycin"],
    },
    "heart_failure": {
        "primary_diagnosis": "I50.9",
        "likely_labs": ["BNP", "Creatinine", "Sodium"],
        "abnormal_vitals": ["respiratory_rate", "spo2"],
        "typical_meds": ["Lisinopril", "Metoprolol"],
    },
    "pneumonia": {
        "primary_diagnosis": "J18.9",
        "likely_labs": ["WBC", "CRP"],
        "abnormal_vitals": ["temperature", "respiratory_rate", "spo2"],
        "typical_meds": ["Azithromycin", "Ceftriaxone"],
    },
    "diabetic": {
        "primary_diagnosis": "E11.65",
        "likely_labs": ["Glucose", "HbA1c"],
        "abnormal_vitals": [],
        "typical_meds": ["Metformin", "Insulin Glargine"],
    },
}


def get_diagnosis_by_code(code: str) -> ICD10Code | None:
    """Get diagnosis by ICD-10 code."""
    for diag in COMMON_DIAGNOSES:
        if diag.code == code:
            return diag
    return None


def get_diagnoses_by_category(category: str) -> list[ICD10Code]:
    """Get all diagnoses in a category."""
    return [d for d in COMMON_DIAGNOSES if d.category == category]


def get_lab_test(name: str) -> LabTest | None:
    """Get lab test by name."""
    for test in LAB_TESTS:
        if test.name == name:
            return test
    return None


def get_medication(name: str) -> MedicationInfo | None:
    """Get medication by name."""
    for med in MEDICATIONS:
        if med.name == name:
            return med
    return None
