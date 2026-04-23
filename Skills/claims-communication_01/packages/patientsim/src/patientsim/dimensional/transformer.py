"""PatientSim Dimensional Transformer.

Transforms PatientSim canonical models into dimensional (star schema) format
for analytics and BI tools.
"""

from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

import pandas as pd
from healthsim.dimensional import BaseDimensionalTransformer

if TYPE_CHECKING:
    from patientsim.core.models import (
        Diagnosis,
        Encounter,
        LabResult,
        Medication,
        Patient,
        Procedure,
        VitalSign,
    )


class PatientDimensionalTransformer(BaseDimensionalTransformer):
    """Transform PatientSim canonical models into dimensional format.

    Creates star schema with dimensions and fact tables optimized for
    healthcare analytics.

    Dimensions:
        - dim_patient: Patient demographics with age bands
        - dim_provider: Healthcare providers
        - dim_facility: Healthcare facilities
        - dim_diagnosis: ICD-10 diagnosis codes
        - dim_procedure: Procedure codes
        - dim_medication: Medication information
        - dim_lab_test: Laboratory test definitions

    Facts:
        - fact_encounters: Encounter metrics (LOS, readmission flags)
        - fact_diagnoses: Diagnosis events
        - fact_procedures: Procedure events
        - fact_medications: Medication orders
        - fact_lab_results: Laboratory results
        - fact_vitals: Vital sign observations

    Example:
        >>> from patientsim.core import PatientGenerator
        >>> from patientsim.dimensional import PatientDimensionalTransformer
        >>>
        >>> gen = PatientGenerator(seed=42)
        >>> patient = gen.generate_patient()
        >>> encounter = gen.generate_encounter(patient)
        >>> diagnosis = gen.generate_diagnosis(patient, encounter)
        >>>
        >>> transformer = PatientDimensionalTransformer(
        ...     patients=[patient],
        ...     encounters=[encounter],
        ...     diagnoses=[diagnosis],
        ... )
        >>> dimensions, facts = transformer.transform()
    """

    def __init__(
        self,
        patients: list[Patient] | None = None,
        encounters: list[Encounter] | None = None,
        diagnoses: list[Diagnosis] | None = None,
        procedures: list[Procedure] | None = None,
        medications: list[Medication] | None = None,
        lab_results: list[LabResult] | None = None,
        vitals: list[VitalSign] | None = None,
        snapshot_date: date | None = None,
    ) -> None:
        """Initialize the transformer with canonical model data.

        Args:
            patients: List of Patient objects.
            encounters: List of Encounter objects.
            diagnoses: List of Diagnosis objects.
            procedures: List of Procedure objects.
            medications: List of Medication objects.
            lab_results: List of LabResult objects.
            vitals: List of VitalSign objects.
            snapshot_date: Date for age calculations. Defaults to today.
        """
        self.patients = patients or []
        self.encounters = encounters or []
        self.diagnoses = diagnoses or []
        self.procedures = procedures or []
        self.medications = medications or []
        self.lab_results = lab_results or []
        self.vitals = vitals or []
        self.snapshot_date = snapshot_date or date.today()

    def transform(self) -> tuple[dict[str, pd.DataFrame], dict[str, pd.DataFrame]]:
        """Transform canonical models into dimensional format.

        Returns:
            Tuple of (dimensions dict, facts dict) where each dict maps
            table names to DataFrames.
        """
        dimensions = {}
        facts = {}

        # Build dimensions
        if self.patients:
            dimensions["dim_patient"] = self._build_dim_patient()

        if self.encounters:
            dimensions["dim_facility"] = self._build_dim_facility()
            dimensions["dim_provider"] = self._build_dim_provider()

        if self.diagnoses:
            dimensions["dim_diagnosis"] = self._build_dim_diagnosis()

        if self.procedures:
            dimensions["dim_procedure"] = self._build_dim_procedure()

        if self.medications:
            dimensions["dim_medication"] = self._build_dim_medication()

        if self.lab_results:
            dimensions["dim_lab_test"] = self._build_dim_lab_test()

        # Build facts
        if self.encounters:
            facts["fact_encounters"] = self._build_fact_encounters()

        if self.diagnoses:
            facts["fact_diagnoses"] = self._build_fact_diagnoses()

        if self.procedures:
            facts["fact_procedures"] = self._build_fact_procedures()

        if self.medications:
            facts["fact_medications"] = self._build_fact_medications()

        if self.lab_results:
            facts["fact_lab_results"] = self._build_fact_lab_results()

        if self.vitals:
            facts["fact_vitals"] = self._build_fact_vitals()

        return dimensions, facts

    # -------------------------------------------------------------------------
    # Dimension Builders
    # -------------------------------------------------------------------------

    def _build_dim_patient(self) -> pd.DataFrame:
        """Build patient dimension with demographics and age bands."""
        records = []
        for patient in self.patients:
            age = self.calculate_age(patient.birth_date, self.snapshot_date)
            records.append(
                {
                    "patient_key": patient.mrn,
                    "patient_mrn": patient.mrn,
                    "patient_id": patient.id,
                    "given_name": patient.name.given_name,
                    "family_name": patient.name.family_name,
                    "full_name": patient.full_name,
                    "birth_date_key": self.date_to_key(patient.birth_date),
                    "birth_date": patient.birth_date,
                    "gender_code": (
                        patient.gender.value if hasattr(patient.gender, "value") else patient.gender
                    ),
                    "gender_description": self._get_gender_description(patient.gender),
                    "race": patient.race,
                    "language": patient.language,
                    "age_at_snapshot": age,
                    "age_band": self.age_band(age),
                    "city": self.get_attr(patient, "address.city"),
                    "state": self.get_attr(patient, "address.state"),
                    "postal_code": self.get_attr(patient, "address.postal_code"),
                }
            )
        return pd.DataFrame(records)

    def _build_dim_facility(self) -> pd.DataFrame:
        """Build facility dimension from encounter data."""
        facilities = set()
        for enc in self.encounters:
            if enc.facility:
                facilities.add(enc.facility)

        records = []
        for idx, facility in enumerate(sorted(facilities), start=1):
            records.append(
                {
                    "facility_key": idx,
                    "facility_name": facility,
                    "facility_type": "Hospital",  # Default
                }
            )

        if not records:
            # Ensure at least one record for referential integrity
            records.append(
                {
                    "facility_key": -1,
                    "facility_name": "Unknown",
                    "facility_type": "Unknown",
                }
            )

        return pd.DataFrame(records)

    def _build_dim_provider(self) -> pd.DataFrame:
        """Build provider dimension from encounter data."""
        providers = set()
        for enc in self.encounters:
            if enc.attending_physician:
                providers.add(enc.attending_physician)
            if enc.admitting_physician:
                providers.add(enc.admitting_physician)

        records = []
        for idx, provider_id in enumerate(sorted(providers), start=1):
            records.append(
                {
                    "provider_key": idx,
                    "provider_id": provider_id,
                    "provider_name": provider_id,  # Name not available in canonical model
                    "provider_type": "Physician",
                }
            )

        if not records:
            # Ensure at least one record for referential integrity
            records.append(
                {
                    "provider_key": -1,
                    "provider_id": "UNKNOWN",
                    "provider_name": "Unknown",
                    "provider_type": "Unknown",
                }
            )

        return pd.DataFrame(records)

    def _build_dim_diagnosis(self) -> pd.DataFrame:
        """Build diagnosis dimension from diagnosis codes."""
        diagnosis_codes: dict[str, str] = {}
        for diag in self.diagnoses:
            if diag.code not in diagnosis_codes:
                diagnosis_codes[diag.code] = diag.description

        records = []
        for idx, (code, description) in enumerate(sorted(diagnosis_codes.items()), start=1):
            # Extract category from ICD-10 code (first letter or first 3 chars)
            category = self._get_icd10_category(code)
            records.append(
                {
                    "diagnosis_key": idx,
                    "diagnosis_code": code,
                    "diagnosis_description": description,
                    "diagnosis_category": category,
                    "code_system": "ICD-10-CM",
                }
            )

        return (
            pd.DataFrame(records)
            if records
            else pd.DataFrame(
                columns=[
                    "diagnosis_key",
                    "diagnosis_code",
                    "diagnosis_description",
                    "diagnosis_category",
                    "code_system",
                ]
            )
        )

    def _build_dim_procedure(self) -> pd.DataFrame:
        """Build procedure dimension from procedure codes."""
        procedure_codes: dict[str, str] = {}
        for proc in self.procedures:
            if proc.code not in procedure_codes:
                procedure_codes[proc.code] = proc.description

        records = []
        for idx, (code, description) in enumerate(sorted(procedure_codes.items()), start=1):
            records.append(
                {
                    "procedure_key": idx,
                    "procedure_code": code,
                    "procedure_description": description,
                    "code_system": self._infer_procedure_code_system(code),
                }
            )

        return (
            pd.DataFrame(records)
            if records
            else pd.DataFrame(
                columns=["procedure_key", "procedure_code", "procedure_description", "code_system"]
            )
        )

    def _build_dim_medication(self) -> pd.DataFrame:
        """Build medication dimension from medication data."""
        medications: dict[str, dict] = {}
        for med in self.medications:
            if med.name not in medications:
                medications[med.name] = {
                    "name": med.name,
                    "code": med.code,
                    "indication": med.indication,
                }

        records = []
        for idx, med_info in enumerate(
            sorted(medications.values(), key=lambda x: x["name"]), start=1
        ):
            records.append(
                {
                    "medication_key": idx,
                    "medication_name": med_info["name"],
                    "medication_code": med_info["code"],
                    "code_system": "RxNorm" if med_info["code"] else None,
                    "indication": med_info["indication"],
                }
            )

        return (
            pd.DataFrame(records)
            if records
            else pd.DataFrame(
                columns=[
                    "medication_key",
                    "medication_name",
                    "medication_code",
                    "code_system",
                    "indication",
                ]
            )
        )

    def _build_dim_lab_test(self) -> pd.DataFrame:
        """Build lab test dimension from lab results."""
        lab_tests: dict[str, dict] = {}
        for lab in self.lab_results:
            if lab.test_name not in lab_tests:
                lab_tests[lab.test_name] = {
                    "test_name": lab.test_name,
                    "loinc_code": lab.loinc_code,
                    "unit": lab.unit,
                    "reference_range": lab.reference_range,
                }

        records = []
        for idx, test_info in enumerate(
            sorted(lab_tests.values(), key=lambda x: x["test_name"]), start=1
        ):
            records.append(
                {
                    "lab_test_key": idx,
                    "test_name": test_info["test_name"],
                    "loinc_code": test_info["loinc_code"],
                    "unit": test_info["unit"],
                    "reference_range": test_info["reference_range"],
                    "code_system": "LOINC" if test_info["loinc_code"] else None,
                }
            )

        return (
            pd.DataFrame(records)
            if records
            else pd.DataFrame(
                columns=[
                    "lab_test_key",
                    "test_name",
                    "loinc_code",
                    "unit",
                    "reference_range",
                    "code_system",
                ]
            )
        )

    # -------------------------------------------------------------------------
    # Fact Builders
    # -------------------------------------------------------------------------

    def _build_fact_encounters(self) -> pd.DataFrame:
        """Build encounter fact table with LOS and readmission flags."""
        # Build lookup maps
        facility_map = self._build_facility_lookup()
        provider_map = self._build_provider_lookup()

        # Sort encounters by patient and admission time for readmission calc
        patient_encounters: dict[str, list] = {}
        for enc in self.encounters:
            if enc.patient_mrn not in patient_encounters:
                patient_encounters[enc.patient_mrn] = []
            patient_encounters[enc.patient_mrn].append(enc)

        # Sort each patient's encounters by admission time
        for mrn in patient_encounters:
            patient_encounters[mrn].sort(key=lambda x: x.admission_time)

        records = []
        for enc in self.encounters:
            # Calculate length of stay
            los_hours = None
            los_days = None
            if enc.discharge_time:
                delta = enc.discharge_time - enc.admission_time
                los_hours = delta.total_seconds() / 3600
                los_days = delta.days

            # Calculate readmission flags
            is_readmission_7_day, is_readmission_30_day = self._calculate_readmission_flags(
                enc, patient_encounters.get(enc.patient_mrn, [])
            )

            # Is patient deceased (based on discharge disposition)
            is_mortality = self._check_mortality(enc.discharge_disposition)

            records.append(
                {
                    "encounter_key": enc.encounter_id,
                    "patient_key": enc.patient_mrn,
                    "facility_key": facility_map.get(enc.facility, -1),
                    "attending_provider_key": provider_map.get(enc.attending_physician, -1),
                    "admitting_provider_key": provider_map.get(enc.admitting_physician, -1),
                    "admission_date_key": self.date_to_key(enc.admission_time.date()),
                    "discharge_date_key": (
                        self.date_to_key(enc.discharge_time.date()) if enc.discharge_time else None
                    ),
                    "admission_datetime": enc.admission_time,
                    "discharge_datetime": enc.discharge_time,
                    "encounter_class_code": (
                        enc.class_code.value if hasattr(enc.class_code, "value") else enc.class_code
                    ),
                    "encounter_status_code": (
                        enc.status.value if hasattr(enc.status, "value") else enc.status
                    ),
                    "chief_complaint": enc.chief_complaint,
                    "discharge_disposition": enc.discharge_disposition,
                    "department": enc.department,
                    "room": enc.room,
                    "bed": enc.bed,
                    "length_of_stay_hours": round(los_hours, 2) if los_hours else None,
                    "length_of_stay_days": los_days,
                    "is_readmission_7_day": is_readmission_7_day,
                    "is_readmission_30_day": is_readmission_30_day,
                    "is_mortality": is_mortality,
                }
            )

        return pd.DataFrame(records)

    def _build_fact_diagnoses(self) -> pd.DataFrame:
        """Build diagnosis fact table."""
        diagnosis_key_map = self._build_diagnosis_lookup()

        records = []
        for idx, diag in enumerate(self.diagnoses, start=1):
            records.append(
                {
                    "diagnosis_fact_key": idx,
                    "patient_key": diag.patient_mrn,
                    "encounter_key": diag.encounter_id,
                    "diagnosis_key": diagnosis_key_map.get(diag.code, -1),
                    "diagnosed_date_key": self.date_to_key(diag.diagnosed_date),
                    "resolved_date_key": (
                        self.date_to_key(diag.resolved_date) if diag.resolved_date else None
                    ),
                    "diagnosis_type_code": (
                        diag.type.value if hasattr(diag.type, "value") else diag.type
                    ),
                    "is_primary": (
                        diag.type.value == "admitting"
                        if hasattr(diag.type, "value")
                        else diag.type == "admitting"
                    ),
                    "is_resolved": diag.resolved_date is not None,
                }
            )

        return pd.DataFrame(records)

    def _build_fact_procedures(self) -> pd.DataFrame:
        """Build procedure fact table."""
        procedure_key_map = self._build_procedure_lookup()

        records = []
        for idx, proc in enumerate(self.procedures, start=1):
            records.append(
                {
                    "procedure_fact_key": idx,
                    "patient_key": proc.patient_mrn,
                    "encounter_key": proc.encounter_id,
                    "procedure_key": procedure_key_map.get(proc.code, -1),
                    "performed_date_key": self.date_to_key(proc.performed_date.date()),
                    "performed_datetime": proc.performed_date,
                    "performer": proc.performer,
                    "location": proc.location,
                }
            )

        return pd.DataFrame(records)

    def _build_fact_medications(self) -> pd.DataFrame:
        """Build medication fact table."""
        medication_key_map = self._build_medication_lookup()

        records = []
        for idx, med in enumerate(self.medications, start=1):
            records.append(
                {
                    "medication_fact_key": idx,
                    "patient_key": med.patient_mrn,
                    "encounter_key": med.encounter_id,
                    "medication_key": medication_key_map.get(med.name, -1),
                    "start_date_key": self.date_to_key(med.start_date.date()),
                    "end_date_key": (
                        self.date_to_key(med.end_date.date()) if med.end_date else None
                    ),
                    "start_datetime": med.start_date,
                    "end_datetime": med.end_date,
                    "dose": med.dose,
                    "route": med.route,
                    "frequency": med.frequency,
                    "status_code": med.status.value if hasattr(med.status, "value") else med.status,
                    "prescriber": med.prescriber,
                    "is_active": (med.status.value if hasattr(med.status, "value") else med.status)
                    == "active",
                }
            )

        return pd.DataFrame(records)

    def _build_fact_lab_results(self) -> pd.DataFrame:
        """Build lab results fact table."""
        lab_test_key_map = self._build_lab_test_lookup()

        records = []
        for idx, lab in enumerate(self.lab_results, start=1):
            # Parse numeric value if possible
            numeric_value = self.safe_decimal(lab.value)

            records.append(
                {
                    "lab_result_fact_key": idx,
                    "patient_key": lab.patient_mrn,
                    "encounter_key": lab.encounter_id,
                    "lab_test_key": lab_test_key_map.get(lab.test_name, -1),
                    "collected_date_key": self.date_to_key(lab.collected_time.date()),
                    "resulted_date_key": (
                        self.date_to_key(lab.resulted_time.date()) if lab.resulted_time else None
                    ),
                    "collected_datetime": lab.collected_time,
                    "resulted_datetime": lab.resulted_time,
                    "result_value": lab.value,
                    "result_numeric": float(numeric_value) if numeric_value else None,
                    "unit": lab.unit,
                    "abnormal_flag": lab.abnormal_flag,
                    "is_abnormal": lab.abnormal_flag is not None,
                    "is_critical": lab.abnormal_flag in ("HH", "LL", "A"),
                    "performing_lab": lab.performing_lab,
                    "ordering_provider": lab.ordering_provider,
                }
            )

        return pd.DataFrame(records)

    def _build_fact_vitals(self) -> pd.DataFrame:
        """Build vitals fact table."""
        records = []
        for idx, vital in enumerate(self.vitals, start=1):
            records.append(
                {
                    "vitals_fact_key": idx,
                    "patient_key": vital.patient_mrn,
                    "encounter_key": vital.encounter_id,
                    "observation_date_key": self.date_to_key(vital.observation_time.date()),
                    "observation_datetime": vital.observation_time,
                    "temperature_f": vital.temperature,
                    "heart_rate_bpm": vital.heart_rate,
                    "respiratory_rate": vital.respiratory_rate,
                    "systolic_bp": vital.systolic_bp,
                    "diastolic_bp": vital.diastolic_bp,
                    "blood_pressure": vital.blood_pressure,
                    "spo2_pct": vital.spo2,
                    "height_cm": vital.height_cm,
                    "weight_kg": vital.weight_kg,
                    "bmi": vital.bmi,
                    "is_febrile": vital.temperature and vital.temperature >= 100.4,
                    "is_tachycardic": vital.heart_rate and vital.heart_rate > 100,
                    "is_hypotensive": vital.systolic_bp and vital.systolic_bp < 90,
                    "is_hypertensive": vital.systolic_bp and vital.systolic_bp >= 140,
                    "is_hypoxic": vital.spo2 and vital.spo2 < 90,
                }
            )

        return pd.DataFrame(records)

    # -------------------------------------------------------------------------
    # Helper Methods
    # -------------------------------------------------------------------------

    def _build_facility_lookup(self) -> dict[str, int]:
        """Build facility name to key lookup."""
        facilities = sorted({enc.facility for enc in self.encounters if enc.facility})
        return {name: idx for idx, name in enumerate(facilities, start=1)}

    def _build_provider_lookup(self) -> dict[str, int]:
        """Build provider ID to key lookup."""
        providers = set()
        for enc in self.encounters:
            if enc.attending_physician:
                providers.add(enc.attending_physician)
            if enc.admitting_physician:
                providers.add(enc.admitting_physician)
        return {pid: idx for idx, pid in enumerate(sorted(providers), start=1)}

    def _build_diagnosis_lookup(self) -> dict[str, int]:
        """Build diagnosis code to key lookup."""
        codes = sorted({diag.code for diag in self.diagnoses})
        return {code: idx for idx, code in enumerate(codes, start=1)}

    def _build_procedure_lookup(self) -> dict[str, int]:
        """Build procedure code to key lookup."""
        codes = sorted({proc.code for proc in self.procedures})
        return {code: idx for idx, code in enumerate(codes, start=1)}

    def _build_medication_lookup(self) -> dict[str, int]:
        """Build medication name to key lookup."""
        names = sorted({med.name for med in self.medications})
        return {name: idx for idx, name in enumerate(names, start=1)}

    def _build_lab_test_lookup(self) -> dict[str, int]:
        """Build lab test name to key lookup."""
        names = sorted({lab.test_name for lab in self.lab_results})
        return {name: idx for idx, name in enumerate(names, start=1)}

    def _calculate_readmission_flags(
        self,
        current_encounter: Encounter,
        patient_encounters: list[Encounter],
    ) -> tuple[bool, bool]:
        """Calculate 7-day and 30-day readmission flags.

        An encounter is a readmission if there was a prior encounter
        that discharged within 7 or 30 days before this admission.

        Args:
            current_encounter: The encounter to check.
            patient_encounters: All encounters for this patient, sorted by admission time.

        Returns:
            Tuple of (is_readmission_7_day, is_readmission_30_day).
        """
        is_readmission_7_day = False
        is_readmission_30_day = False

        for prior_enc in patient_encounters:
            # Skip if same encounter or no discharge time
            if prior_enc.encounter_id == current_encounter.encounter_id:
                continue
            if not prior_enc.discharge_time:
                continue
            # Only consider prior encounters
            if prior_enc.admission_time >= current_encounter.admission_time:
                continue

            days_since_discharge = (
                current_encounter.admission_time.date() - prior_enc.discharge_time.date()
            ).days

            if 0 <= days_since_discharge <= 7:
                is_readmission_7_day = True
                is_readmission_30_day = True
                break
            elif 0 <= days_since_discharge <= 30:
                is_readmission_30_day = True

        return is_readmission_7_day, is_readmission_30_day

    def _check_mortality(self, discharge_disposition: str | None) -> bool:
        """Check if discharge disposition indicates mortality."""
        if not discharge_disposition:
            return False
        disposition_lower = discharge_disposition.lower()
        mortality_keywords = ["expired", "died", "death", "deceased", "morgue"]
        return any(kw in disposition_lower for kw in mortality_keywords)

    def _get_gender_description(self, gender) -> str:
        """Get human-readable gender description."""
        gender_value = gender.value if hasattr(gender, "value") else gender
        descriptions = {
            "M": "Male",
            "F": "Female",
            "O": "Other",
            "U": "Unknown",
        }
        return descriptions.get(gender_value, "Unknown")

    def _get_icd10_category(self, code: str) -> str:
        """Get ICD-10 category from code.

        ICD-10 categories are based on the first letter:
        A-B: Infectious diseases
        C-D: Neoplasms
        E: Endocrine, nutritional, metabolic
        F: Mental/behavioral
        G: Nervous system
        H: Eye/ear
        I: Circulatory
        J: Respiratory
        K: Digestive
        L: Skin
        M: Musculoskeletal
        N: Genitourinary
        O: Pregnancy
        P: Perinatal
        Q: Congenital
        R: Symptoms
        S-T: Injury
        V-Y: External causes
        Z: Health status
        """
        if not code:
            return "Unknown"

        first_char = code[0].upper()
        categories = {
            "A": "Infectious",
            "B": "Infectious",
            "C": "Neoplasm",
            "D": "Neoplasm/Blood",
            "E": "Endocrine/Metabolic",
            "F": "Mental/Behavioral",
            "G": "Nervous System",
            "H": "Eye/Ear",
            "I": "Circulatory",
            "J": "Respiratory",
            "K": "Digestive",
            "L": "Skin",
            "M": "Musculoskeletal",
            "N": "Genitourinary",
            "O": "Pregnancy",
            "P": "Perinatal",
            "Q": "Congenital",
            "R": "Symptoms",
            "S": "Injury",
            "T": "Injury/Poisoning",
            "V": "External Causes",
            "W": "External Causes",
            "X": "External Causes",
            "Y": "External Causes",
            "Z": "Health Status",
        }
        return categories.get(first_char, "Other")

    def _infer_procedure_code_system(self, code: str) -> str:
        """Infer procedure code system from code format.

        - ICD-10-PCS: 7 alphanumeric characters
        - CPT: 5 digits
        - HCPCS: 1 letter + 4 digits
        """
        if not code:
            return "Unknown"

        code = code.strip()

        # CPT codes are 5 digits
        if code.isdigit() and len(code) == 5:
            return "CPT"

        # HCPCS codes start with letter and have 4 digits
        if len(code) == 5 and code[0].isalpha() and code[1:].isdigit():
            return "HCPCS"

        # ICD-10-PCS codes are 7 alphanumeric
        if len(code) == 7 and code.isalnum():
            return "ICD-10-PCS"

        return "Unknown"
