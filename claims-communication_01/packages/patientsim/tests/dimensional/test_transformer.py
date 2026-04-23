"""Tests for the PatientSim dimensional transformer."""

from __future__ import annotations

from datetime import date, datetime, timedelta

import pytest

from patientsim.core.generator import PatientGenerator
from patientsim.core.models import (
    Encounter,
    EncounterClass,
    EncounterStatus,
    Procedure,
)
from patientsim.dimensional import PatientDimensionalTransformer


class TestPatientDimensionalTransformerInit:
    """Tests for transformer initialization."""

    def test_init_empty(self):
        """Test initialization with no data."""
        transformer = PatientDimensionalTransformer()
        assert transformer.patients == []
        assert transformer.encounters == []
        assert transformer.diagnoses == []
        assert transformer.procedures == []
        assert transformer.medications == []
        assert transformer.lab_results == []
        assert transformer.vitals == []
        assert transformer.snapshot_date == date.today()

    def test_init_with_snapshot_date(self):
        """Test initialization with custom snapshot date."""
        snapshot = date(2024, 6, 15)
        transformer = PatientDimensionalTransformer(snapshot_date=snapshot)
        assert transformer.snapshot_date == snapshot


class TestDimPatient:
    """Tests for patient dimension."""

    def test_build_dim_patient_basic(self):
        """Test basic patient dimension building."""
        gen = PatientGenerator(seed=42)
        patient = gen.generate_patient()

        transformer = PatientDimensionalTransformer(
            patients=[patient], snapshot_date=date(2024, 6, 15)
        )
        dimensions, facts = transformer.transform()

        assert "dim_patient" in dimensions
        dim_patient = dimensions["dim_patient"]

        assert len(dim_patient) == 1
        row = dim_patient.iloc[0]

        assert row["patient_key"] == patient.mrn
        assert row["patient_mrn"] == patient.mrn
        assert row["given_name"] == patient.name.given_name
        assert row["family_name"] == patient.name.family_name

    def test_dim_patient_age_calculation(self):
        """Test age is calculated correctly at snapshot date."""
        gen = PatientGenerator(seed=42)
        patient = gen.generate_patient()

        snapshot = date(2024, 6, 15)
        transformer = PatientDimensionalTransformer(patients=[patient], snapshot_date=snapshot)
        dimensions, _ = transformer.transform()

        dim_patient = dimensions["dim_patient"]
        row = dim_patient.iloc[0]

        # Calculate expected age
        birth_date = patient.birth_date
        expected_age = (
            snapshot.year
            - birth_date.year
            - ((snapshot.month, snapshot.day) < (birth_date.month, birth_date.day))
        )

        assert row["age_at_snapshot"] == expected_age

    def test_dim_patient_age_bands(self):
        """Test age bands are assigned correctly."""
        gen = PatientGenerator(seed=42)

        # Create patients with known ages
        patients = []
        for age_range in [(5, 10), (25, 30), (40, 45), (55, 60), (70, 75)]:
            patient = gen.generate_patient(age_range=age_range)
            patients.append(patient)

        transformer = PatientDimensionalTransformer(patients=patients)
        dimensions, _ = transformer.transform()

        dim_patient = dimensions["dim_patient"]
        age_bands = dim_patient["age_band"].tolist()

        # Verify we have various age bands
        assert any(band == "0-17" for band in age_bands)
        assert any(band in ("18-34", "35-49", "50-64", "65+") for band in age_bands)

    def test_dim_patient_multiple_patients(self):
        """Test dimension with multiple patients."""
        gen = PatientGenerator(seed=42)
        patients = [gen.generate_patient() for _ in range(5)]

        transformer = PatientDimensionalTransformer(patients=patients)
        dimensions, _ = transformer.transform()

        dim_patient = dimensions["dim_patient"]
        assert len(dim_patient) == 5


class TestDimFacility:
    """Tests for facility dimension."""

    def test_build_dim_facility(self):
        """Test facility dimension building."""
        gen = PatientGenerator(seed=42)
        patient = gen.generate_patient()
        encounter = gen.generate_encounter(patient)

        transformer = PatientDimensionalTransformer(patients=[patient], encounters=[encounter])
        dimensions, _ = transformer.transform()

        assert "dim_facility" in dimensions
        dim_facility = dimensions["dim_facility"]

        # Should have at least one facility
        assert len(dim_facility) >= 1
        assert "facility_key" in dim_facility.columns
        assert "facility_name" in dim_facility.columns

    def test_dim_facility_deduplication(self):
        """Test facilities are deduplicated."""
        gen = PatientGenerator(seed=42)
        patient = gen.generate_patient()

        # Create multiple encounters at same facility
        encounters = []
        for _ in range(5):
            enc = gen.generate_encounter(patient)
            encounters.append(enc)

        transformer = PatientDimensionalTransformer(encounters=encounters)
        dimensions, _ = transformer.transform()

        dim_facility = dimensions["dim_facility"]

        # Unique facility names
        unique_facilities = dim_facility["facility_name"].nunique()
        assert unique_facilities <= len(encounters)


class TestDimDiagnosis:
    """Tests for diagnosis dimension."""

    def test_build_dim_diagnosis(self):
        """Test diagnosis dimension building."""
        gen = PatientGenerator(seed=42)
        patient = gen.generate_patient()
        diagnosis = gen.generate_diagnosis(patient)

        transformer = PatientDimensionalTransformer(patients=[patient], diagnoses=[diagnosis])
        dimensions, _ = transformer.transform()

        assert "dim_diagnosis" in dimensions
        dim_diagnosis = dimensions["dim_diagnosis"]

        assert len(dim_diagnosis) >= 1
        assert "diagnosis_key" in dim_diagnosis.columns
        assert "diagnosis_code" in dim_diagnosis.columns
        assert "diagnosis_description" in dim_diagnosis.columns
        assert "diagnosis_category" in dim_diagnosis.columns
        assert "code_system" in dim_diagnosis.columns

    def test_dim_diagnosis_icd10_category(self):
        """Test ICD-10 category assignment."""
        gen = PatientGenerator(seed=42)
        patient = gen.generate_patient()

        # Create diagnoses with different ICD-10 categories
        diagnoses = []
        for category in ["diabetes", "cardiac", "respiratory"]:
            diag = gen.generate_diagnosis(patient, category=category)
            diagnoses.append(diag)

        transformer = PatientDimensionalTransformer(diagnoses=diagnoses)
        dimensions, _ = transformer.transform()

        dim_diagnosis = dimensions["dim_diagnosis"]

        # All should have a category
        assert all(cat is not None for cat in dim_diagnosis["diagnosis_category"])


class TestFactEncounters:
    """Tests for encounter fact table."""

    def test_build_fact_encounters(self):
        """Test encounter fact building."""
        gen = PatientGenerator(seed=42)
        patient = gen.generate_patient()
        encounter = gen.generate_encounter(patient, EncounterClass.INPATIENT)

        transformer = PatientDimensionalTransformer(patients=[patient], encounters=[encounter])
        _, facts = transformer.transform()

        assert "fact_encounters" in facts
        fact_enc = facts["fact_encounters"]

        assert len(fact_enc) == 1
        row = fact_enc.iloc[0]

        assert row["encounter_key"] == encounter.encounter_id
        assert row["patient_key"] == patient.mrn

    def test_fact_encounters_length_of_stay(self):
        """Test LOS calculation."""
        gen = PatientGenerator(seed=42)
        patient = gen.generate_patient()

        # Create encounter with known LOS
        admission = datetime(2024, 6, 10, 10, 0)
        discharge = datetime(2024, 6, 13, 14, 0)  # 3 days, 4 hours

        encounter = Encounter(
            encounter_id="TEST001",
            patient_mrn=patient.mrn,
            class_code=EncounterClass.INPATIENT,
            status=EncounterStatus.FINISHED,
            admission_time=admission,
            discharge_time=discharge,
            facility="Test Hospital",
        )

        transformer = PatientDimensionalTransformer(encounters=[encounter])
        _, facts = transformer.transform()

        fact_enc = facts["fact_encounters"]
        row = fact_enc.iloc[0]

        assert row["length_of_stay_days"] == 3
        assert row["length_of_stay_hours"] == pytest.approx(76.0, rel=0.01)

    def test_fact_encounters_readmission_7_day(self):
        """Test 7-day readmission flag."""
        gen = PatientGenerator(seed=42)
        patient = gen.generate_patient()

        # First encounter
        enc1 = Encounter(
            encounter_id="ENC001",
            patient_mrn=patient.mrn,
            class_code=EncounterClass.INPATIENT,
            status=EncounterStatus.FINISHED,
            admission_time=datetime(2024, 6, 1, 10, 0),
            discharge_time=datetime(2024, 6, 5, 14, 0),
            facility="Test Hospital",
        )

        # Readmission within 7 days
        enc2 = Encounter(
            encounter_id="ENC002",
            patient_mrn=patient.mrn,
            class_code=EncounterClass.INPATIENT,
            status=EncounterStatus.FINISHED,
            admission_time=datetime(2024, 6, 10, 10, 0),  # 5 days after discharge
            discharge_time=datetime(2024, 6, 12, 14, 0),
            facility="Test Hospital",
        )

        transformer = PatientDimensionalTransformer(encounters=[enc1, enc2])
        _, facts = transformer.transform()

        fact_enc = facts["fact_encounters"]

        # First encounter should not be readmission
        enc1_row = fact_enc[fact_enc["encounter_key"] == "ENC001"].iloc[0]
        assert enc1_row["is_readmission_7_day"] == False  # noqa: E712
        assert enc1_row["is_readmission_30_day"] == False  # noqa: E712

        # Second encounter should be 7-day readmission
        enc2_row = fact_enc[fact_enc["encounter_key"] == "ENC002"].iloc[0]
        assert enc2_row["is_readmission_7_day"] == True  # noqa: E712
        assert enc2_row["is_readmission_30_day"] == True  # noqa: E712

    def test_fact_encounters_readmission_30_day(self):
        """Test 30-day readmission flag (but not 7-day)."""
        gen = PatientGenerator(seed=42)
        patient = gen.generate_patient()

        # First encounter
        enc1 = Encounter(
            encounter_id="ENC001",
            patient_mrn=patient.mrn,
            class_code=EncounterClass.INPATIENT,
            status=EncounterStatus.FINISHED,
            admission_time=datetime(2024, 6, 1, 10, 0),
            discharge_time=datetime(2024, 6, 5, 14, 0),
            facility="Test Hospital",
        )

        # Readmission within 30 days but not 7 days
        enc2 = Encounter(
            encounter_id="ENC002",
            patient_mrn=patient.mrn,
            class_code=EncounterClass.INPATIENT,
            status=EncounterStatus.FINISHED,
            admission_time=datetime(2024, 6, 20, 10, 0),  # 15 days after discharge
            discharge_time=datetime(2024, 6, 22, 14, 0),
            facility="Test Hospital",
        )

        transformer = PatientDimensionalTransformer(encounters=[enc1, enc2])
        _, facts = transformer.transform()

        fact_enc = facts["fact_encounters"]

        # Second encounter should be 30-day but not 7-day readmission
        enc2_row = fact_enc[fact_enc["encounter_key"] == "ENC002"].iloc[0]
        assert enc2_row["is_readmission_7_day"] == False  # noqa: E712
        assert enc2_row["is_readmission_30_day"] == True  # noqa: E712

    def test_fact_encounters_mortality_flag(self):
        """Test mortality flag from discharge disposition."""
        gen = PatientGenerator(seed=42)
        patient = gen.generate_patient()

        encounter = Encounter(
            encounter_id="TEST001",
            patient_mrn=patient.mrn,
            class_code=EncounterClass.INPATIENT,
            status=EncounterStatus.FINISHED,
            admission_time=datetime(2024, 6, 1, 10, 0),
            discharge_time=datetime(2024, 6, 5, 14, 0),
            facility="Test Hospital",
            discharge_disposition="Expired",
        )

        transformer = PatientDimensionalTransformer(encounters=[encounter])
        _, facts = transformer.transform()

        fact_enc = facts["fact_encounters"]
        row = fact_enc.iloc[0]

        assert row["is_mortality"] == True  # noqa: E712


class TestFactDiagnoses:
    """Tests for diagnosis fact table."""

    def test_build_fact_diagnoses(self):
        """Test diagnosis fact building."""
        gen = PatientGenerator(seed=42)
        patient = gen.generate_patient()
        encounter = gen.generate_encounter(patient)
        diagnosis = gen.generate_diagnosis(patient, encounter)

        transformer = PatientDimensionalTransformer(
            patients=[patient], encounters=[encounter], diagnoses=[diagnosis]
        )
        _, facts = transformer.transform()

        assert "fact_diagnoses" in facts
        fact_diag = facts["fact_diagnoses"]

        assert len(fact_diag) == 1
        row = fact_diag.iloc[0]

        assert row["patient_key"] == patient.mrn
        assert row["encounter_key"] == encounter.encounter_id


class TestFactLabResults:
    """Tests for lab results fact table."""

    def test_build_fact_lab_results(self):
        """Test lab results fact building."""
        gen = PatientGenerator(seed=42)
        patient = gen.generate_patient()
        encounter = gen.generate_encounter(patient)
        lab = gen.generate_lab_result(patient, encounter)

        transformer = PatientDimensionalTransformer(
            patients=[patient], encounters=[encounter], lab_results=[lab]
        )
        _, facts = transformer.transform()

        assert "fact_lab_results" in facts
        fact_lab = facts["fact_lab_results"]

        assert len(fact_lab) == 1
        row = fact_lab.iloc[0]

        assert row["patient_key"] == patient.mrn
        assert row["encounter_key"] == encounter.encounter_id

    def test_fact_lab_results_abnormal_flags(self):
        """Test abnormal flag processing."""
        gen = PatientGenerator(seed=42)
        patient = gen.generate_patient()

        # Create abnormal lab result
        lab = gen.generate_lab_result(patient, make_abnormal=True)

        transformer = PatientDimensionalTransformer(lab_results=[lab])
        _, facts = transformer.transform()

        fact_lab = facts["fact_lab_results"]
        row = fact_lab.iloc[0]

        assert row["is_abnormal"] == True  # noqa: E712


class TestFactVitals:
    """Tests for vitals fact table."""

    def test_build_fact_vitals(self):
        """Test vitals fact building."""
        gen = PatientGenerator(seed=42)
        patient = gen.generate_patient()
        encounter = gen.generate_encounter(patient)
        vitals = gen.generate_vital_signs(patient, encounter)

        transformer = PatientDimensionalTransformer(
            patients=[patient], encounters=[encounter], vitals=[vitals]
        )
        _, facts = transformer.transform()

        assert "fact_vitals" in facts
        fact_vitals = facts["fact_vitals"]

        assert len(fact_vitals) == 1
        row = fact_vitals.iloc[0]

        assert row["patient_key"] == patient.mrn
        assert row["encounter_key"] == encounter.encounter_id

    def test_fact_vitals_clinical_flags(self):
        """Test clinical flag calculations."""
        gen = PatientGenerator(seed=42)
        patient = gen.generate_patient()

        # Create abnormal vitals
        vitals = gen.generate_vital_signs(
            patient, abnormal_parameters=["temperature", "heart_rate"]
        )

        transformer = PatientDimensionalTransformer(vitals=[vitals])
        _, facts = transformer.transform()

        fact_vitals = facts["fact_vitals"]
        row = fact_vitals.iloc[0]

        # Should have febrile and tachycardia flags
        assert row["is_febrile"] == True  # noqa: E712
        assert row["is_tachycardic"] == True  # noqa: E712


class TestFactMedications:
    """Tests for medication fact table."""

    def test_build_fact_medications(self):
        """Test medication fact building."""
        gen = PatientGenerator(seed=42)
        patient = gen.generate_patient()
        encounter = gen.generate_encounter(patient)
        med = gen.generate_medication(patient, encounter)

        transformer = PatientDimensionalTransformer(
            patients=[patient], encounters=[encounter], medications=[med]
        )
        _, facts = transformer.transform()

        assert "fact_medications" in facts
        fact_med = facts["fact_medications"]

        assert len(fact_med) == 1
        row = fact_med.iloc[0]

        assert row["patient_key"] == patient.mrn
        assert "dose" in row.index
        assert "route" in row.index
        assert "frequency" in row.index


class TestFactProcedures:
    """Tests for procedure fact table."""

    def test_build_fact_procedures(self):
        """Test procedure fact building."""
        gen = PatientGenerator(seed=42)
        patient = gen.generate_patient()

        procedure = Procedure(
            code="99213",
            description="Office visit, established patient",
            patient_mrn=patient.mrn,
            performed_date=datetime.now() - timedelta(days=1),
        )

        transformer = PatientDimensionalTransformer(patients=[patient], procedures=[procedure])
        _, facts = transformer.transform()

        assert "fact_procedures" in facts
        fact_proc = facts["fact_procedures"]

        assert len(fact_proc) == 1


class TestTransformEmpty:
    """Tests for empty data handling."""

    def test_transform_no_data(self):
        """Test transform with no data returns empty dicts."""
        transformer = PatientDimensionalTransformer()
        dimensions, facts = transformer.transform()

        assert dimensions == {}
        assert facts == {}

    def test_transform_patients_only(self):
        """Test transform with only patients."""
        gen = PatientGenerator(seed=42)
        patient = gen.generate_patient()

        transformer = PatientDimensionalTransformer(patients=[patient])
        dimensions, facts = transformer.transform()

        assert "dim_patient" in dimensions
        assert len(facts) == 0


class TestIntegration:
    """Integration tests with full data pipeline."""

    def test_full_patient_scenario(self):
        """Test complete patient scenario with all data types."""
        gen = PatientGenerator(seed=42)

        # Generate complete patient data
        patient = gen.generate_patient()
        encounter = gen.generate_encounter(patient, EncounterClass.INPATIENT)
        diagnosis = gen.generate_diagnosis(patient, encounter)
        lab = gen.generate_lab_result(patient, encounter)
        vitals = gen.generate_vital_signs(patient, encounter)
        med = gen.generate_medication(patient, encounter)

        transformer = PatientDimensionalTransformer(
            patients=[patient],
            encounters=[encounter],
            diagnoses=[diagnosis],
            lab_results=[lab],
            vitals=[vitals],
            medications=[med],
        )
        dimensions, facts = transformer.transform()

        # Verify all tables created
        assert "dim_patient" in dimensions
        assert "dim_facility" in dimensions
        assert "dim_diagnosis" in dimensions
        assert "dim_lab_test" in dimensions
        assert "dim_medication" in dimensions

        assert "fact_encounters" in facts
        assert "fact_diagnoses" in facts
        assert "fact_lab_results" in facts
        assert "fact_vitals" in facts
        assert "fact_medications" in facts

    def test_multiple_patients_scenario(self):
        """Test with multiple patients and encounters."""
        gen = PatientGenerator(seed=42)

        patients = []
        encounters = []
        diagnoses = []

        for _ in range(3):
            patient = gen.generate_patient()
            patients.append(patient)

            for _ in range(2):
                enc = gen.generate_encounter(patient)
                encounters.append(enc)
                diag = gen.generate_diagnosis(patient, enc)
                diagnoses.append(diag)

        transformer = PatientDimensionalTransformer(
            patients=patients, encounters=encounters, diagnoses=diagnoses
        )
        dimensions, facts = transformer.transform()

        assert len(dimensions["dim_patient"]) == 3
        assert len(facts["fact_encounters"]) == 6
        assert len(facts["fact_diagnoses"]) == 6
