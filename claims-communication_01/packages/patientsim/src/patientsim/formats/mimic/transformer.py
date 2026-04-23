"""MIMIC-III format transformer.

Converts PatientSim Patient/Encounter objects to MIMIC-III database tables.
"""

import contextlib
from datetime import datetime, timedelta

import pandas as pd

from patientsim.core.models import (
    Diagnosis,
    Encounter,
    LabResult,
    Patient,
    VitalSign,
)
from patientsim.formats.mimic.schema import (
    AdmissionsSchema,
    CharteventsSchema,
    DiagnosesIcdSchema,
    LabeventsSchema,
    PatientsSchema,
    get_chart_itemid,
    get_lab_itemid,
)


class IDGenerator:
    """Generates unique IDs for MIMIC-III entities.

    Maintains state to ensure IDs are unique and consistent within
    a transformation session.
    """

    def __init__(self, start_id: int = 10000) -> None:
        """Initialize ID generator.

        Args:
            start_id: Starting ID value (default 10000 to avoid conflicts)
        """
        self.row_id = start_id
        self.subject_id = start_id
        self.hadm_id = start_id
        self._subject_map: dict[str, int] = {}  # mrn -> subject_id
        self._hadm_map: dict[str, int] = {}  # encounter_id -> hadm_id

    def get_row_id(self) -> int:
        """Get next row_id."""
        current = self.row_id
        self.row_id += 1
        return current

    def get_subject_id(self, mrn: str) -> int:
        """Get subject_id for a patient MRN, creating if needed.

        Args:
            mrn: Medical Record Number

        Returns:
            MIMIC subject_id
        """
        if mrn not in self._subject_map:
            self._subject_map[mrn] = self.subject_id
            self.subject_id += 1
        return self._subject_map[mrn]

    def get_hadm_id(self, encounter_id: str) -> int:
        """Get hadm_id for an encounter, creating if needed.

        Args:
            encounter_id: Encounter identifier

        Returns:
            MIMIC hadm_id
        """
        if encounter_id not in self._hadm_map:
            self._hadm_map[encounter_id] = self.hadm_id
            self.hadm_id += 1
        return self._hadm_map[encounter_id]


class MIMICTransformer:
    """Transforms PatientSim objects to MIMIC-III tables.

    Example:
        >>> transformer = MIMICTransformer()
        >>> patients_df = transformer.transform_patients([patient1, patient2])
        >>> encounters_df = transformer.transform_admissions([enc1, enc2])
    """

    def __init__(self, start_id: int = 10000) -> None:
        """Initialize transformer.

        Args:
            start_id: Starting ID for generated identifiers
        """
        self.id_gen = IDGenerator(start_id=start_id)

    def transform_patients(self, patients: list[Patient]) -> pd.DataFrame:
        """Transform patients to PATIENTS table.

        Args:
            patients: List of Patient objects

        Returns:
            DataFrame matching PATIENTS schema
        """
        rows = []

        for patient in patients:
            subject_id = self.id_gen.get_subject_id(patient.mrn)

            # Calculate dates of death if applicable
            dod = None
            dod_hosp = None
            dod_ssn = None
            expire_flag = 0

            if patient.deceased:
                # For deceased patients, use death_date if available
                if patient.death_date:
                    dod = datetime.combine(patient.death_date, datetime.min.time())
                else:
                    # Estimate death date from age
                    years_lived = patient.age
                    dod = datetime.combine(patient.birth_date, datetime.min.time()) + timedelta(
                        days=years_lived * 365
                    )

                dod_hosp = dod  # Assume death in hospital
                dod_ssn = dod
                expire_flag = 1

            row = {
                "row_id": self.id_gen.get_row_id(),
                "subject_id": subject_id,
                "gender": patient.gender,  # Already "M" or "F" from Gender enum
                "dob": datetime.combine(patient.birth_date, datetime.min.time()),
                "dod": dod,
                "dod_hosp": dod_hosp,
                "dod_ssn": dod_ssn,
                "expire_flag": expire_flag,
            }
            rows.append(row)

        if not rows:
            return PatientsSchema.create_empty()

        return pd.DataFrame(rows, columns=PatientsSchema.COLUMNS)

    def transform_admissions(self, encounters: list[Encounter]) -> pd.DataFrame:
        """Transform encounters to ADMISSIONS table.

        Args:
            encounters: List of Encounter objects

        Returns:
            DataFrame matching ADMISSIONS schema
        """
        rows = []

        for encounter in encounters:
            subject_id = self.id_gen.get_subject_id(encounter.patient_mrn)
            hadm_id = self.id_gen.get_hadm_id(encounter.encounter_id)

            # Determine death time if applicable
            death_time = None
            hospital_expire_flag = 0
            # Death would be indicated by discharge disposition or status
            # For now, assume not expired unless explicitly indicated

            # Map encounter class to admission type
            admission_type = "EMERGENCY"  # Default
            if encounter.class_code == "I":
                admission_type = "EMERGENCY"  # Inpatient often emergency
            elif encounter.class_code == "E":
                admission_type = "EMERGENCY"
            elif encounter.class_code == "O":
                admission_type = "ELECTIVE"

            # Determine admission location
            admission_location = "EMERGENCY ROOM ADMIT"
            if admission_type == "ELECTIVE":
                admission_location = "PHYS REFERRAL/NORMAL DELI"

            # Determine discharge location
            discharge_location = "HOME"
            if encounter.discharge_disposition:
                disp = encounter.discharge_disposition.upper()
                if "SNF" in disp or "NURSING" in disp:
                    discharge_location = "SNF"
                elif "REHAB" in disp:
                    discharge_location = "REHAB/DISTINCT PART HOSP"
                elif "DEAD" in disp or "EXPIRED" in disp or "DECEASED" in disp:
                    discharge_location = "DEAD/EXPIRED"
                    hospital_expire_flag = 1
                    if encounter.discharge_time:
                        death_time = encounter.discharge_time

            # Get primary diagnosis text
            diagnosis_text = encounter.admitting_diagnosis or "Unspecified"

            row = {
                "row_id": self.id_gen.get_row_id(),
                "subject_id": subject_id,
                "hadm_id": hadm_id,
                "admittime": encounter.admission_time,
                "dischtime": encounter.discharge_time,
                "deathtime": death_time,
                "admission_type": admission_type,
                "admission_location": admission_location,
                "discharge_location": discharge_location,
                "insurance": "Medicare",  # Default - could be parameterized
                "language": "ENGL",
                "religion": "NOT SPECIFIED",
                "marital_status": "SINGLE",  # Could be from patient data
                "ethnicity": "UNKNOWN/NOT SPECIFIED",  # Would come from patient
                "edregtime": None,  # Set if admission from ED
                "edouttime": None,
                "diagnosis": diagnosis_text,
                "hospital_expire_flag": hospital_expire_flag,
                "has_chartevents_data": 1,  # Assume yes
            }

            # If emergency admission, set ED times
            if admission_type == "EMERGENCY":
                row["edregtime"] = encounter.admission_time - timedelta(hours=2)
                row["edouttime"] = encounter.admission_time

            rows.append(row)

        if not rows:
            return AdmissionsSchema.create_empty()

        return pd.DataFrame(rows, columns=AdmissionsSchema.COLUMNS)

    def transform_diagnoses_icd(self, diagnoses: list[Diagnosis]) -> pd.DataFrame:
        """Transform diagnoses to DIAGNOSES_ICD table.

        Args:
            diagnoses: List of Diagnosis objects

        Returns:
            DataFrame matching DIAGNOSES_ICD schema
        """
        rows = []

        # Group diagnoses by encounter
        encounter_groups: dict[str, list[Diagnosis]] = {}
        for diagnosis in diagnoses:
            enc_id = diagnosis.encounter_id or "unknown"
            if enc_id not in encounter_groups:
                encounter_groups[enc_id] = []
            encounter_groups[enc_id].append(diagnosis)

        # Process each encounter's diagnoses
        for enc_id, diag_list in encounter_groups.items():
            if enc_id == "unknown":
                continue  # Skip diagnoses not linked to encounters

            subject_id = self.id_gen.get_subject_id(diag_list[0].patient_mrn)
            hadm_id = self.id_gen.get_hadm_id(enc_id)

            for seq_num, diagnosis in enumerate(diag_list, start=1):
                # Extract ICD code (ICD-10 code)
                icd_code = self._extract_icd_code(diagnosis.code)

                if icd_code:
                    row = {
                        "row_id": self.id_gen.get_row_id(),
                        "subject_id": subject_id,
                        "hadm_id": hadm_id,
                        "seq_num": seq_num,
                        "icd9_code": icd_code,  # Note: storing ICD-10 in ICD-9 field for demo
                    }
                    rows.append(row)

        if not rows:
            return DiagnosesIcdSchema.create_empty()

        return pd.DataFrame(rows, columns=DiagnosesIcdSchema.COLUMNS)

    def transform_labevents(self, lab_results: list[LabResult]) -> pd.DataFrame:
        """Transform lab results to LABEVENTS table.

        Args:
            lab_results: List of LabResult objects

        Returns:
            DataFrame matching LABEVENTS schema
        """
        rows = []

        for lab in lab_results:
            subject_id = self.id_gen.get_subject_id(lab.patient_mrn)

            # Get hadm_id if encounter is linked
            hadm_id = None
            if lab.encounter_id:
                hadm_id = self.id_gen.get_hadm_id(lab.encounter_id)

            # Get MIMIC ITEMID for this lab
            itemid = get_lab_itemid(lab.test_name)
            if not itemid:
                # Skip labs we don't have mappings for
                continue

            # Determine chart time
            chart_time = lab.collected_time

            # Parse numeric value
            value_num = None
            value_str = str(lab.value)
            with contextlib.suppress(ValueError, TypeError):
                value_num = float(lab.value)

            # Determine abnormal flag
            flag = "normal"  # Default
            # In real implementation, would check reference ranges

            row = {
                "row_id": self.id_gen.get_row_id(),
                "subject_id": subject_id,
                "hadm_id": hadm_id,
                "itemid": itemid,
                "charttime": chart_time,
                "value": value_str,
                "valuenum": value_num,
                "valueuom": lab.unit,
                "flag": flag,
            }
            rows.append(row)

        if not rows:
            return LabeventsSchema.create_empty()

        return pd.DataFrame(rows, columns=LabeventsSchema.COLUMNS)

    def transform_chartevents(self, vital_signs: list[VitalSign]) -> pd.DataFrame:
        """Transform vital signs to CHARTEVENTS table.

        Args:
            vital_signs: List of VitalSign objects

        Returns:
            DataFrame matching CHARTEVENTS schema
        """
        rows = []

        for vital in vital_signs:
            subject_id = self.id_gen.get_subject_id(vital.patient_mrn)

            # Get hadm_id if encounter is linked
            hadm_id = None
            if vital.encounter_id:
                hadm_id = self.id_gen.get_hadm_id(vital.encounter_id)

            chart_time = vital.observation_time
            store_time = chart_time + timedelta(minutes=5)  # Simulate storage delay

            # Create a row for each vital sign measurement present
            vital_mappings = [
                ("temperature", vital.temperature, "temperature_f", "F"),
                ("heart_rate", vital.heart_rate, "heart_rate", "bpm"),
                ("respiratory_rate", vital.respiratory_rate, "respiratory_rate", "/min"),
                ("systolic_bp", vital.systolic_bp, "sbp", "mmHg"),
                ("diastolic_bp", vital.diastolic_bp, "dbp", "mmHg"),
                ("spo2", vital.spo2, "spo2", "%"),
            ]

            for _field_name, value, vital_type, unit in vital_mappings:
                if value is None:
                    continue

                # Get MIMIC ITEMID for this vital type
                itemid = get_chart_itemid(vital_type)
                if not itemid:
                    continue

                row = {
                    "row_id": self.id_gen.get_row_id(),
                    "subject_id": subject_id,
                    "hadm_id": hadm_id,
                    "icustay_id": None,  # We don't track ICU stays currently
                    "itemid": itemid,
                    "charttime": chart_time,
                    "storetime": store_time,
                    "cgid": 1,  # Caregiver ID - placeholder
                    "value": str(value),
                    "valuenum": float(value),
                    "valueuom": unit,
                    "warning": 0,
                    "error": 0,
                    "resultstatus": "Final",
                    "stopped": "NotStopped",
                }
                rows.append(row)

        if not rows:
            return CharteventsSchema.create_empty()

        return pd.DataFrame(rows, columns=CharteventsSchema.COLUMNS)

    def _extract_icd_code(self, code: str) -> str:
        """Extract ICD code from diagnosis code string.

        Args:
            code: ICD code (ICD-10 format)

        Returns:
            Cleaned ICD code string
        """
        # For now, just return the code as-is
        # In production, might convert ICD-10 to ICD-9 or validate format
        return code.strip()
