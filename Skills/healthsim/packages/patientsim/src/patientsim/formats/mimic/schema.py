"""MIMIC-III database schema definitions.

This module defines the structure of MIMIC-III tables that we generate.
Based on the official MIMIC-III v1.4 schema.

References:
- https://mimic.mit.edu/docs/iii/tables/
- https://github.com/MIT-LCP/mimic-code/tree/main/mimic-iii
"""

from dataclasses import dataclass

import pandas as pd


@dataclass
class PatientsSchema:
    """Schema for PATIENTS table.

    Demographics and static patient information.
    """

    # Column definitions
    COLUMNS = [
        "row_id",  # INT - Unique row identifier
        "subject_id",  # INT - Primary identifier for patient
        "gender",  # VARCHAR(5) - M or F
        "dob",  # TIMESTAMP - Date of birth (shifted for de-identification)
        "dod",  # TIMESTAMP - Date of death (NULL if alive)
        "dod_hosp",  # TIMESTAMP - Date of death in hospital (NULL if not applicable)
        "dod_ssn",  # TIMESTAMP - Date of death from social security (NULL if not applicable)
        "expire_flag",  # SMALLINT - 1 if patient died, 0 if alive
    ]

    @staticmethod
    def create_empty() -> pd.DataFrame:
        """Create empty DataFrame with correct schema."""
        return pd.DataFrame(columns=PatientsSchema.COLUMNS)


@dataclass
class AdmissionsSchema:
    """Schema for ADMISSIONS table.

    Hospital admissions information.
    """

    COLUMNS = [
        "row_id",  # INT - Unique row identifier
        "subject_id",  # INT - Foreign key to PATIENTS
        "hadm_id",  # INT - Primary identifier for hospital admission
        "admittime",  # TIMESTAMP - Admission time
        "dischtime",  # TIMESTAMP - Discharge time
        "deathtime",  # TIMESTAMP - Time of death (NULL if not applicable)
        "admission_type",  # VARCHAR(50) - EMERGENCY, ELECTIVE, URGENT, NEWBORN
        "admission_location",  # VARCHAR(50) - Where patient admitted from
        "discharge_location",  # VARCHAR(50) - Where patient discharged to
        "insurance",  # VARCHAR(255) - Insurance type
        "language",  # VARCHAR(10) - Preferred language
        "religion",  # VARCHAR(50) - Religious affiliation
        "marital_status",  # VARCHAR(50) - Marital status
        "ethnicity",  # VARCHAR(200) - Ethnicity
        "edregtime",  # TIMESTAMP - ED registration time (NULL if not from ED)
        "edouttime",  # TIMESTAMP - ED out time (NULL if not from ED)
        "diagnosis",  # VARCHAR(255) - Primary diagnosis free text
        "hospital_expire_flag",  # SMALLINT - 1 if died in hospital, 0 otherwise
        "has_chartevents_data",  # SMALLINT - 1 if has chart data, 0 otherwise
    ]

    @staticmethod
    def create_empty() -> pd.DataFrame:
        """Create empty DataFrame with correct schema."""
        return pd.DataFrame(columns=AdmissionsSchema.COLUMNS)


@dataclass
class DiagnosesIcdSchema:
    """Schema for DIAGNOSES_ICD table.

    ICD-9 diagnosis codes assigned to hospital admissions.
    """

    COLUMNS = [
        "row_id",  # INT - Unique row identifier
        "subject_id",  # INT - Foreign key to PATIENTS
        "hadm_id",  # INT - Foreign key to ADMISSIONS
        "seq_num",  # INT - Sequence number (priority order, 1 = primary)
        "icd9_code",  # VARCHAR(10) - ICD-9 diagnosis code
    ]

    @staticmethod
    def create_empty() -> pd.DataFrame:
        """Create empty DataFrame with correct schema."""
        return pd.DataFrame(columns=DiagnosesIcdSchema.COLUMNS)


@dataclass
class LabeventsSchema:
    """Schema for LABEVENTS table.

    Laboratory measurements.
    """

    COLUMNS = [
        "row_id",  # INT - Unique row identifier
        "subject_id",  # INT - Foreign key to PATIENTS
        "hadm_id",  # INT - Foreign key to ADMISSIONS (may be NULL)
        "itemid",  # INT - Foreign key to D_LABITEMS (identifier for lab test)
        "charttime",  # TIMESTAMP - Time measurement was charted
        "value",  # VARCHAR(200) - Value of the measurement (may be NULL)
        "valuenum",  # DOUBLE - Numeric value (NULL if non-numeric)
        "valueuom",  # VARCHAR(20) - Unit of measurement
        "flag",  # VARCHAR(20) - Abnormal flag (normal, abnormal, delta)
    ]

    @staticmethod
    def create_empty() -> pd.DataFrame:
        """Create empty DataFrame with correct schema."""
        return pd.DataFrame(columns=LabeventsSchema.COLUMNS)


@dataclass
class CharteventsSchema:
    """Schema for CHARTEVENTS table.

    Vital signs and other charted observations.
    """

    COLUMNS = [
        "row_id",  # INT - Unique row identifier
        "subject_id",  # INT - Foreign key to PATIENTS
        "hadm_id",  # INT - Foreign key to ADMISSIONS
        "icustay_id",  # INT - Foreign key to ICUSTAYS (may be NULL)
        "itemid",  # INT - Foreign key to D_ITEMS (identifier for measurement type)
        "charttime",  # TIMESTAMP - Time measurement was charted
        "storetime",  # TIMESTAMP - Time measurement was stored
        "cgid",  # INT - Caregiver ID (may be NULL)
        "value",  # VARCHAR(255) - Value of the measurement
        "valuenum",  # DOUBLE - Numeric value (NULL if non-numeric)
        "valueuom",  # VARCHAR(50) - Unit of measurement
        "warning",  # SMALLINT - Flag for warning values
        "error",  # SMALLINT - Flag for error values
        "resultstatus",  # VARCHAR(50) - Status of the result
        "stopped",  # VARCHAR(50) - Stopped flag
    ]

    @staticmethod
    def create_empty() -> pd.DataFrame:
        """Create empty DataFrame with correct schema."""
        return pd.DataFrame(columns=CharteventsSchema.COLUMNS)


# MIMIC-III Item ID mappings
# These are common ITEMIDs from MIMIC-III D_ITEMS and D_LABITEMS tables

CHART_ITEMIDS = {
    # Vital Signs (from CHARTEVENTS)
    "heart_rate": 220045,  # Heart Rate
    "sbp": 220050,  # Systolic BP (non-invasive)
    "dbp": 220051,  # Diastolic BP (non-invasive)
    "mbp": 220052,  # Mean BP (non-invasive)
    "respiratory_rate": 220210,  # Respiratory Rate
    "temperature_f": 223761,  # Temperature Fahrenheit
    "temperature_c": 223762,  # Temperature Celsius
    "spo2": 220277,  # SpO2 (oxygen saturation)
    "weight": 224639,  # Weight (kg)
    "height": 226730,  # Height (cm)
    "bmi": 226512,  # BMI
    "gcs_total": 198,  # Glasgow Coma Scale Total
    "pain_level": 225908,  # Pain Level (0-10)
}

LAB_ITEMIDS = {
    # Hematology
    "hemoglobin": 51222,  # Hemoglobin (g/dL)
    "hematocrit": 51221,  # Hematocrit (%)
    "wbc": 51301,  # White Blood Cells (K/uL)
    "platelets": 51265,  # Platelets (K/uL)
    # Chemistry
    "sodium": 50983,  # Sodium (mEq/L)
    "potassium": 50971,  # Potassium (mEq/L)
    "chloride": 50902,  # Chloride (mEq/L)
    "bicarbonate": 50882,  # Bicarbonate (mEq/L)
    "bun": 51006,  # Blood Urea Nitrogen (mg/dL)
    "creatinine": 50912,  # Creatinine (mg/dL)
    "glucose": 50931,  # Glucose (mg/dL)
    "calcium": 50893,  # Calcium (mg/dL)
    "magnesium": 50960,  # Magnesium (mg/dL)
    # Liver Function
    "alt": 50861,  # Alanine Aminotransferase (IU/L)
    "ast": 50878,  # Aspartate Aminotransferase (IU/L)
    "alkaline_phosphatase": 50863,  # Alkaline Phosphatase (IU/L)
    "bilirubin_total": 50885,  # Total Bilirubin (mg/dL)
    "albumin": 50862,  # Albumin (g/dL)
    # Cardiac
    "troponin_t": 51003,  # Troponin T (ng/mL)
    "troponin_i": 51002,  # Troponin I (ng/mL)
    "bnp": 50963,  # BNP (pg/mL)
    # Coagulation
    "pt": 51274,  # Prothrombin Time (sec)
    "ptt": 51275,  # Partial Thromboplastin Time (sec)
    "inr": 51237,  # INR
    # Lipids
    "cholesterol_total": 50907,  # Total Cholesterol (mg/dL)
    "ldl": 50954,  # LDL (mg/dL)
    "hdl": 50953,  # HDL (mg/dL)
    "triglycerides": 51000,  # Triglycerides (mg/dL)
    # Other
    "lactate": 50813,  # Lactate (mmol/L)
    "hba1c": 50852,  # Hemoglobin A1c (%)
    "tsh": 50993,  # Thyroid Stimulating Hormone (uIU/mL)
}


def get_lab_itemid(lab_name: str) -> int | None:
    """Get MIMIC-III ITEMID for a lab test.

    Args:
        lab_name: Normalized lab name

    Returns:
        ITEMID if found, None otherwise
    """
    # Normalize lab name
    normalized = lab_name.lower().replace(" ", "_").replace("-", "_")

    # Direct lookup
    if normalized in LAB_ITEMIDS:
        return LAB_ITEMIDS[normalized]

    # Common aliases
    aliases = {
        "wbc_count": "wbc",
        "white_blood_cell": "wbc",
        "rbc": "hemoglobin",  # Approximate
        "hgb": "hemoglobin",
        "hct": "hematocrit",
        "plt": "platelets",
        "platelet_count": "platelets",
        "na": "sodium",
        "k": "potassium",
        "cl": "chloride",
        "co2": "bicarbonate",
        "bicarb": "bicarbonate",
        "blood_urea_nitrogen": "bun",
        "cr": "creatinine",
        "glu": "glucose",
        "blood_glucose": "glucose",
        "ca": "calcium",
        "mg": "magnesium",
        "sgot": "ast",
        "sgpt": "alt",
        "alp": "alkaline_phosphatase",
        "tbili": "bilirubin_total",
        "alb": "albumin",
        "trop_t": "troponin_t",
        "trop_i": "troponin_i",
        "chol": "cholesterol_total",
        "a1c": "hba1c",
    }

    if normalized in aliases:
        return LAB_ITEMIDS.get(aliases[normalized])

    return None


def get_chart_itemid(vital_name: str) -> int | None:
    """Get MIMIC-III ITEMID for a vital sign or chart observation.

    Args:
        vital_name: Normalized vital sign name

    Returns:
        ITEMID if found, None otherwise
    """
    # Normalize vital name
    normalized = vital_name.lower().replace(" ", "_").replace("-", "_")

    # Direct lookup
    if normalized in CHART_ITEMIDS:
        return CHART_ITEMIDS[normalized]

    # Common aliases
    aliases = {
        "hr": "heart_rate",
        "pulse": "heart_rate",
        "systolic": "sbp",
        "systolic_bp": "sbp",
        "diastolic": "dbp",
        "diastolic_bp": "dbp",
        "mean_bp": "mbp",
        "rr": "respiratory_rate",
        "resp_rate": "respiratory_rate",
        "temp": "temperature_f",
        "temperature": "temperature_f",
        "o2_sat": "spo2",
        "oxygen_saturation": "spo2",
        "wt": "weight",
        "ht": "height",
        "gcs": "gcs_total",
        "glasgow_coma_scale": "gcs_total",
        "pain": "pain_level",
    }

    if normalized in aliases:
        return CHART_ITEMIDS.get(aliases[normalized])

    return None
