"""Tests for MIMIC-III export functionality."""

from datetime import date, datetime

import pandas as pd
from healthsim.person import PersonName

from patientsim.core.models import (
    Diagnosis,
    DiagnosisType,
    Encounter,
    EncounterClass,
    EncounterStatus,
    Gender,
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
from patientsim.formats.mimic.transformer import IDGenerator, MIMICTransformer


class TestIDGenerator:
    """Tests for ID generator."""

    def test_row_id_increments(self) -> None:
        """Test that row IDs increment correctly."""
        gen = IDGenerator(start_id=100)

        id1 = gen.get_row_id()
        id2 = gen.get_row_id()
        id3 = gen.get_row_id()

        assert id1 == 100
        assert id2 == 101
        assert id3 == 102

    def test_subject_id_consistency(self) -> None:
        """Test that same MRN always gets same subject_id."""
        gen = IDGenerator(start_id=100)

        subj1a = gen.get_subject_id("MRN001")
        subj1b = gen.get_subject_id("MRN001")
        subj2 = gen.get_subject_id("MRN002")

        # Same MRN should return same subject_id
        assert subj1a == subj1b
        assert subj1a == 100

        # Different MRN should get different subject_id
        assert subj2 == 101
        assert subj2 != subj1a

    def test_hadm_id_consistency(self) -> None:
        """Test that same encounter gets same hadm_id."""
        gen = IDGenerator(start_id=100)

        hadm1a = gen.get_hadm_id("ENC001")
        hadm1b = gen.get_hadm_id("ENC001")

        # Same encounter ID should return same hadm_id
        assert hadm1a == hadm1b
        assert hadm1a == 100

        # Different encounter should get different hadm_id
        hadm2 = gen.get_hadm_id("ENC002")
        assert hadm2 == 101
        assert hadm2 != hadm1a


class TestLabItemIDMapping:
    """Tests for lab ITEMID mappings."""

    def test_common_lab_mappings(self) -> None:
        """Test mapping of common lab names to ITEMIDs."""
        assert get_lab_itemid("hemoglobin") == 51222
        assert get_lab_itemid("wbc") == 51301
        assert get_lab_itemid("sodium") == 50983
        assert get_lab_itemid("potassium") == 50971
        assert get_lab_itemid("creatinine") == 50912
        assert get_lab_itemid("glucose") == 50931

    def test_lab_aliases(self) -> None:
        """Test that lab aliases work correctly."""
        # Hemoglobin aliases
        assert get_lab_itemid("hgb") == 51222
        assert get_lab_itemid("hemoglobin") == 51222

        # WBC aliases
        assert get_lab_itemid("wbc") == 51301
        assert get_lab_itemid("white_blood_cell") == 51301

        # Sodium aliases
        assert get_lab_itemid("sodium") == 50983
        assert get_lab_itemid("na") == 50983

    def test_unknown_lab_returns_none(self) -> None:
        """Test that unknown lab names return None."""
        assert get_lab_itemid("unknown_test") is None
        assert get_lab_itemid("nonexistent") is None


class TestChartItemIDMapping:
    """Tests for chart/vital ITEMID mappings."""

    def test_common_vital_mappings(self) -> None:
        """Test mapping of common vital signs to ITEMIDs."""
        assert get_chart_itemid("heart_rate") == 220045
        assert get_chart_itemid("sbp") == 220050
        assert get_chart_itemid("dbp") == 220051
        assert get_chart_itemid("respiratory_rate") == 220210
        assert get_chart_itemid("temperature_f") == 223761
        assert get_chart_itemid("spo2") == 220277

    def test_vital_aliases(self) -> None:
        """Test that vital sign aliases work correctly."""
        # Heart rate aliases
        assert get_chart_itemid("heart_rate") == 220045
        assert get_chart_itemid("hr") == 220045
        assert get_chart_itemid("pulse") == 220045

        # Blood pressure aliases
        assert get_chart_itemid("sbp") == 220050
        assert get_chart_itemid("systolic") == 220050

    def test_unknown_vital_returns_none(self) -> None:
        """Test that unknown vital names return None."""
        assert get_chart_itemid("unknown_vital") is None


class TestPatientsTransform:
    """Tests for PATIENTS table transformation."""

    def test_transform_single_patient(self) -> None:
        """Test transforming a single patient."""
        patient = Patient(
            id="patient-001",
            mrn="MRN001",
            name=PersonName(given_name="John", family_name="Doe"),
            birth_date=date(1959, 3, 15),
            gender=Gender.MALE,
        )

        transformer = MIMICTransformer(start_id=1000)
        df = transformer.transform_patients([patient])

        assert len(df) == 1
        assert list(df.columns) == PatientsSchema.COLUMNS

        row = df.iloc[0]
        assert row["subject_id"] == 1000
        assert row["gender"] == "M"
        assert row["expire_flag"] == 0
        assert pd.isna(row["dod"])

    def test_transform_deceased_patient(self) -> None:
        """Test transforming a deceased patient."""
        patient = Patient(
            id="patient-002",
            mrn="MRN002",
            name=PersonName(given_name="Jane", family_name="Smith"),
            birth_date=date(1952, 7, 20),
            gender=Gender.FEMALE,
            deceased=True,
            death_date=date(2024, 1, 15),
        )

        transformer = MIMICTransformer(start_id=2000)
        df = transformer.transform_patients([patient])

        assert len(df) == 1
        row = df.iloc[0]
        assert row["expire_flag"] == 1
        assert pd.notna(row["dod"])
        assert pd.notna(row["dod_hosp"])

    def test_empty_patient_list(self) -> None:
        """Test transforming empty patient list."""
        transformer = MIMICTransformer()
        df = transformer.transform_patients([])

        assert len(df) == 0
        assert list(df.columns) == PatientsSchema.COLUMNS


class TestAdmissionsTransform:
    """Tests for ADMISSIONS table transformation."""

    def test_transform_single_encounter(self) -> None:
        """Test transforming a single encounter."""
        encounter = Encounter(
            encounter_id="ENC001",
            patient_mrn="MRN001",
            class_code=EncounterClass.EMERGENCY,
            status=EncounterStatus.FINISHED,
            admission_time=datetime(2024, 1, 15, 10, 30),
            discharge_time=datetime(2024, 1, 18, 14, 0),
        )

        transformer = MIMICTransformer(start_id=1000)
        df = transformer.transform_admissions([encounter])

        assert len(df) == 1
        assert list(df.columns) == AdmissionsSchema.COLUMNS

        row = df.iloc[0]
        assert row["subject_id"] == 1000
        assert row["hadm_id"] == 1000
        assert row["admission_type"] == "EMERGENCY"
        assert row["hospital_expire_flag"] == 0

    def test_empty_encounter_list(self) -> None:
        """Test transforming empty encounter list."""
        transformer = MIMICTransformer()
        df = transformer.transform_admissions([])

        assert len(df) == 0
        assert list(df.columns) == AdmissionsSchema.COLUMNS


class TestDiagnosesIcdTransform:
    """Tests for DIAGNOSES_ICD table transformation."""

    def test_transform_diagnoses(self) -> None:
        """Test transforming diagnoses."""
        diagnoses = [
            Diagnosis(
                code="I21.0",
                description="Acute MI",
                type=DiagnosisType.FINAL,
                patient_mrn="MRN001",
                encounter_id="ENC001",
                diagnosed_date=date(2024, 1, 15),
            ),
            Diagnosis(
                code="E11.9",
                description="Type 2 DM",
                type=DiagnosisType.FINAL,
                patient_mrn="MRN001",
                encounter_id="ENC001",
                diagnosed_date=date(2024, 1, 15),
            ),
        ]

        transformer = MIMICTransformer(start_id=1000)
        df = transformer.transform_diagnoses_icd(diagnoses)

        assert len(df) == 2
        assert list(df.columns) == DiagnosesIcdSchema.COLUMNS

        # Check sequence numbers
        assert list(df["seq_num"]) == [1, 2]

    def test_empty_diagnoses(self) -> None:
        """Test empty diagnoses list."""
        transformer = MIMICTransformer()
        df = transformer.transform_diagnoses_icd([])

        assert len(df) == 0
        assert list(df.columns) == DiagnosesIcdSchema.COLUMNS


class TestLabeventsTransform:
    """Tests for LABEVENTS table transformation."""

    def test_transform_lab_results(self) -> None:
        """Test transforming lab results."""
        labs = [
            LabResult(
                test_name="hemoglobin",
                value="12.5",
                unit="g/dL",
                patient_mrn="MRN001",
                encounter_id="ENC001",
                collected_time=datetime(2024, 1, 15, 14, 30),
            ),
            LabResult(
                test_name="wbc",
                value="8.2",
                unit="K/uL",
                patient_mrn="MRN001",
                encounter_id="ENC001",
                collected_time=datetime(2024, 1, 15, 14, 30),
            ),
        ]

        transformer = MIMICTransformer(start_id=1000)
        df = transformer.transform_labevents(labs)

        assert len(df) == 2
        assert list(df.columns) == LabeventsSchema.COLUMNS

        # Check ITEMIDs are mapped
        assert 51222 in list(df["itemid"])  # Hemoglobin
        assert 51301 in list(df["itemid"])  # WBC

    def test_empty_labs(self) -> None:
        """Test empty lab results list."""
        transformer = MIMICTransformer()
        df = transformer.transform_labevents([])

        assert len(df) == 0
        assert list(df.columns) == LabeventsSchema.COLUMNS


class TestCharteventsTransform:
    """Tests for CHARTEVENTS table transformation."""

    def test_transform_vital_signs(self) -> None:
        """Test transforming vital signs."""
        vitals = [
            VitalSign(
                patient_mrn="MRN001",
                encounter_id="ENC001",
                observation_time=datetime(2024, 1, 15, 12, 0),
                heart_rate=82,
                systolic_bp=128,
                diastolic_bp=80,
            ),
        ]

        transformer = MIMICTransformer(start_id=1000)
        df = transformer.transform_chartevents(vitals)

        # Should create 3 rows (heart_rate, sbp, dbp)
        assert len(df) == 3
        assert list(df.columns) == CharteventsSchema.COLUMNS

        # Check ITEMIDs are mapped
        assert 220045 in list(df["itemid"])  # Heart rate
        assert 220050 in list(df["itemid"])  # SBP
        assert 220051 in list(df["itemid"])  # DBP

    def test_empty_vitals(self) -> None:
        """Test empty vital signs list."""
        transformer = MIMICTransformer()
        df = transformer.transform_chartevents([])

        assert len(df) == 0
        assert list(df.columns) == CharteventsSchema.COLUMNS


class TestReferentialIntegrity:
    """Tests for referential integrity across tables."""

    def test_subject_id_consistency(self) -> None:
        """Test that same patient gets same subject_id across tables."""
        patient = Patient(
            id="patient-003",
            mrn="MRN001",
            name=PersonName(given_name="John", family_name="Doe"),
            birth_date=date(1959, 3, 15),
            gender=Gender.MALE,
        )

        encounter = Encounter(
            encounter_id="ENC001",
            patient_mrn="MRN001",
            class_code=EncounterClass.EMERGENCY,
            status=EncounterStatus.FINISHED,
            admission_time=datetime(2024, 1, 15, 10, 30),
        )

        diagnosis = Diagnosis(
            code="I21.0",
            description="Acute MI",
            type=DiagnosisType.FINAL,
            patient_mrn="MRN001",
            encounter_id="ENC001",
            diagnosed_date=date(2024, 1, 15),
        )

        transformer = MIMICTransformer(start_id=1000)

        patients_df = transformer.transform_patients([patient])
        admissions_df = transformer.transform_admissions([encounter])
        diagnoses_df = transformer.transform_diagnoses_icd([diagnosis])

        # All should have same subject_id
        assert patients_df.iloc[0]["subject_id"] == 1000
        assert admissions_df.iloc[0]["subject_id"] == 1000
        assert diagnoses_df.iloc[0]["subject_id"] == 1000

    def test_hadm_id_consistency(self) -> None:
        """Test that same encounter gets same hadm_id across tables."""
        encounter = Encounter(
            encounter_id="ENC001",
            patient_mrn="MRN001",
            class_code=EncounterClass.EMERGENCY,
            status=EncounterStatus.FINISHED,
            admission_time=datetime(2024, 1, 15, 10, 30),
        )

        diagnosis = Diagnosis(
            code="I21.0",
            description="Acute MI",
            type=DiagnosisType.FINAL,
            patient_mrn="MRN001",
            encounter_id="ENC001",
            diagnosed_date=date(2024, 1, 15),
        )

        transformer = MIMICTransformer(start_id=1000)

        admissions_df = transformer.transform_admissions([encounter])
        diagnoses_df = transformer.transform_diagnoses_icd([diagnosis])

        # Both should have same hadm_id
        assert admissions_df.iloc[0]["hadm_id"] == 1000
        assert diagnoses_df.iloc[0]["hadm_id"] == 1000
