"""Tests for core data models."""

from datetime import date, datetime, timedelta

import pytest
from healthsim.person import PersonName
from pydantic import ValidationError

from patientsim.core import (
    ClinicalNote,
    Diagnosis,
    DiagnosisType,
    Encounter,
    EncounterClass,
    EncounterStatus,
    Gender,
    LabResult,
    Medication,
    MedicationStatus,
    Patient,
    Procedure,
    VitalSign,
)


class TestPatient:
    """Tests for Patient model."""

    def test_patient_creation_valid(self) -> None:
        """Test creating a valid patient."""
        # Arrange & Act
        patient = Patient(
            id="patient-001",
            mrn="MRN12345",
            name=PersonName(given_name="John", family_name="Doe"),
            birth_date=date(1980, 1, 15),
            gender=Gender.MALE,
        )

        # Assert
        assert patient.mrn == "MRN12345"
        assert patient.full_name == "John Doe"
        assert patient.gender == Gender.MALE
        assert patient.given_name == "John"
        assert patient.family_name == "Doe"

    def test_patient_age_calculation(self) -> None:
        """Test that patient age is calculated correctly."""
        # Arrange - use specific date to avoid leap year issues
        birth_date = date(1980, 1, 15)
        patient = Patient(
            id="patient-002",
            mrn="MRN001",
            name=PersonName(given_name="Test", family_name="User"),
            birth_date=birth_date,
            gender=Gender.FEMALE,
        )

        # Act
        age = patient.age

        # Assert
        # Age should be 45 in 2025 (today's year based on test environment)
        expected_age = date.today().year - 1980
        if date.today() < date(date.today().year, 1, 15):
            expected_age -= 1
        assert age == expected_age

    def test_patient_full_name_with_middle_and_suffix(self) -> None:
        """Test full name construction with all components."""
        # Arrange & Act
        patient = Patient(
            id="patient-003",
            mrn="MRN002",
            name=PersonName(
                given_name="John",
                middle_name="Q",
                family_name="Doe",
                suffix="Jr",
            ),
            birth_date=date(1985, 5, 20),
            gender=Gender.MALE,
        )

        # Assert
        assert patient.full_name == "John Q Doe Jr"

    def test_patient_birth_date_future_invalid(self) -> None:
        """Test that future birth dates are rejected."""
        # Arrange
        future_date = date.today() + timedelta(days=1)

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            Patient(
                id="patient-004",
                mrn="MRN003",
                name=PersonName(given_name="Invalid", family_name="Patient"),
                birth_date=future_date,
                gender=Gender.UNKNOWN,
            )

        assert "birth_date cannot be in the future" in str(exc_info.value)

    def test_patient_deceased_with_death_date(self) -> None:
        """Test that deceased=True with death_date is valid."""
        # Arrange & Act
        patient = Patient(
            id="patient-005",
            mrn="MRN004",
            name=PersonName(given_name="Deceased", family_name="Patient"),
            birth_date=date(1950, 1, 1),
            gender=Gender.MALE,
            deceased=True,
            death_date=date(2020, 1, 1),
        )

        # Assert
        assert patient.deceased is True
        assert patient.death_date == date(2020, 1, 1)

    def test_patient_death_date_requires_deceased_flag(self) -> None:
        """Test that death_date requires deceased=True."""
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            Patient(
                id="patient-006",
                mrn="MRN005",
                name=PersonName(given_name="Test", family_name="Patient"),
                birth_date=date(1950, 1, 1),
                gender=Gender.MALE,
                deceased=False,
                death_date=date(2020, 1, 1),
            )

        assert "death_date set but deceased is False" in str(exc_info.value)

    def test_patient_death_date_after_birth(self) -> None:
        """Test that death date must be after birth date."""
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            Patient(
                id="patient-007",
                mrn="MRN006",
                name=PersonName(given_name="Test", family_name="Patient"),
                birth_date=date(1950, 6, 1),
                gender=Gender.MALE,
                deceased=True,
                death_date=date(1950, 1, 1),  # Before birth
            )

        assert "death_date cannot be before birth_date" in str(exc_info.value)

    def test_patient_serialization(self) -> None:
        """Test that patient can be serialized to dict/JSON."""
        # Arrange
        patient = Patient(
            id="patient-008",
            mrn="MRN007",
            name=PersonName(given_name="Jane", family_name="Smith"),
            birth_date=date(1990, 3, 15),
            gender=Gender.FEMALE,
        )

        # Act
        data = patient.model_dump()

        # Assert
        assert data["mrn"] == "MRN007"
        assert data["name"]["given_name"] == "Jane"
        assert data["gender"] == "F"


class TestEncounter:
    """Tests for Encounter model."""

    def test_encounter_creation_valid(self) -> None:
        """Test creating a valid encounter."""
        # Arrange & Act
        encounter = Encounter(
            encounter_id="V12345",
            patient_mrn="MRN12345",
            class_code=EncounterClass.EMERGENCY,
            status=EncounterStatus.FINISHED,
            admission_time=datetime(2025, 1, 26, 14, 30),
            discharge_time=datetime(2025, 1, 26, 18, 45),
        )

        # Assert
        assert encounter.encounter_id == "V12345"
        assert encounter.class_code == EncounterClass.EMERGENCY
        assert encounter.status == EncounterStatus.FINISHED

    def test_encounter_discharge_before_admission_invalid(self) -> None:
        """Test that discharge cannot be before admission."""
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            Encounter(
                encounter_id="V001",
                patient_mrn="MRN001",
                class_code=EncounterClass.INPATIENT,
                status=EncounterStatus.FINISHED,
                admission_time=datetime(2025, 1, 26, 18, 0),
                discharge_time=datetime(2025, 1, 26, 14, 0),  # Before admission
            )

        assert "Discharge time cannot be before admission time" in str(exc_info.value)

    def test_encounter_length_of_stay_calculation(self) -> None:
        """Test length of stay calculation."""
        # Arrange
        encounter = Encounter(
            encounter_id="V002",
            patient_mrn="MRN002",
            class_code=EncounterClass.INPATIENT,
            status=EncounterStatus.FINISHED,
            admission_time=datetime(2025, 1, 26, 12, 0),
            discharge_time=datetime(2025, 1, 27, 12, 0),  # 24 hours later
        )

        # Act
        los = encounter.length_of_stay_hours

        # Assert
        assert los == 24.0

    def test_encounter_no_discharge_no_los(self) -> None:
        """Test that LOS is None when no discharge time."""
        # Arrange
        encounter = Encounter(
            encounter_id="V003",
            patient_mrn="MRN003",
            class_code=EncounterClass.EMERGENCY,
            status=EncounterStatus.IN_PROGRESS,
            admission_time=datetime(2025, 1, 26, 14, 30),
        )

        # Act
        los = encounter.length_of_stay_hours

        # Assert
        assert los is None


class TestDiagnosis:
    """Tests for Diagnosis model."""

    def test_diagnosis_creation_valid(self) -> None:
        """Test creating a valid diagnosis."""
        # Arrange & Act
        diagnosis = Diagnosis(
            code="E11.9",
            description="Type 2 diabetes mellitus without complications",
            type=DiagnosisType.FINAL,
            patient_mrn="MRN12345",
            diagnosed_date=date(2024, 6, 15),
        )

        # Assert
        assert diagnosis.code == "E11.9"
        assert diagnosis.type == DiagnosisType.FINAL

    def test_diagnosis_resolved_before_diagnosed_invalid(self) -> None:
        """Test that resolved date cannot be before diagnosed date."""
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            Diagnosis(
                code="J44.0",
                description="COPD",
                patient_mrn="MRN001",
                diagnosed_date=date(2024, 6, 1),
                resolved_date=date(2024, 1, 1),  # Before diagnosed
            )

        assert "Resolved date cannot be before diagnosed date" in str(exc_info.value)


class TestProcedure:
    """Tests for Procedure model."""

    def test_procedure_creation_valid(self) -> None:
        """Test creating a valid procedure."""
        # Arrange & Act
        procedure = Procedure(
            code="3E0G76Z",
            description="Insertion of central venous catheter",
            patient_mrn="MRN12345",
            performed_date=datetime(2025, 1, 26, 15, 30),
        )

        # Assert
        assert procedure.code == "3E0G76Z"
        assert procedure.performed_date.year == 2025

    def test_procedure_future_date_invalid(self) -> None:
        """Test that future procedure dates are rejected."""
        # Arrange
        future_date = datetime.now() + timedelta(days=1)

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            Procedure(
                code="TEST",
                description="Future procedure",
                patient_mrn="MRN001",
                performed_date=future_date,
            )

        assert "Procedure date cannot be in the future" in str(exc_info.value)


class TestMedication:
    """Tests for Medication model."""

    def test_medication_creation_valid(self) -> None:
        """Test creating a valid medication."""
        # Arrange & Act
        medication = Medication(
            name="Metformin",
            code="860975",
            dose="500 mg",
            route="PO",
            frequency="BID",
            patient_mrn="MRN12345",
            start_date=datetime(2024, 6, 15, 8, 0),
        )

        # Assert
        assert medication.name == "Metformin"
        assert medication.status == MedicationStatus.ACTIVE

    def test_medication_end_before_start_invalid(self) -> None:
        """Test that end date cannot be before start date."""
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            Medication(
                name="Test Drug",
                dose="10 mg",
                route="IV",
                frequency="QD",
                patient_mrn="MRN001",
                start_date=datetime(2025, 1, 26, 12, 0),
                end_date=datetime(2025, 1, 25, 12, 0),  # Before start
            )

        assert "End date cannot be before start date" in str(exc_info.value)


class TestLabResult:
    """Tests for LabResult model."""

    def test_lab_result_creation_valid(self) -> None:
        """Test creating a valid lab result."""
        # Arrange & Act
        lab = LabResult(
            test_name="Glucose",
            loinc_code="2345-7",
            value="95",
            unit="mg/dL",
            reference_range="70-100",
            patient_mrn="MRN12345",
            collected_time=datetime(2025, 1, 26, 8, 0),
            resulted_time=datetime(2025, 1, 26, 10, 30),
        )

        # Assert
        assert lab.test_name == "Glucose"
        assert lab.value == "95"

    def test_lab_result_resulted_before_collected_invalid(self) -> None:
        """Test that resulted time cannot be before collected time."""
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            LabResult(
                test_name="Test",
                value="100",
                patient_mrn="MRN001",
                collected_time=datetime(2025, 1, 26, 10, 0),
                resulted_time=datetime(2025, 1, 26, 8, 0),  # Before collected
            )

        assert "Resulted time cannot be before collected time" in str(exc_info.value)


class TestVitalSign:
    """Tests for VitalSign model."""

    def test_vital_sign_creation_valid(self) -> None:
        """Test creating valid vital signs."""
        # Arrange & Act
        vitals = VitalSign(
            patient_mrn="MRN12345",
            observation_time=datetime(2025, 1, 26, 14, 0),
            temperature=98.6,
            heart_rate=72,
            respiratory_rate=16,
            systolic_bp=120,
            diastolic_bp=80,
            spo2=98,
        )

        # Assert
        assert vitals.heart_rate == 72
        assert vitals.temperature == 98.6

    def test_vital_sign_blood_pressure_property(self) -> None:
        """Test blood pressure property formatting."""
        # Arrange
        vitals = VitalSign(
            patient_mrn="MRN001",
            observation_time=datetime(2025, 1, 26, 14, 0),
            systolic_bp=120,
            diastolic_bp=80,
        )

        # Act
        bp = vitals.blood_pressure

        # Assert
        assert bp == "120/80"

    def test_vital_sign_bmi_calculation(self) -> None:
        """Test BMI calculation."""
        # Arrange
        vitals = VitalSign(
            patient_mrn="MRN002",
            observation_time=datetime(2025, 1, 26, 14, 0),
            height_cm=175,  # 1.75m
            weight_kg=70,  # 70kg
        )

        # Act
        bmi = vitals.bmi

        # Assert
        assert bmi == 22.9  # 70 / (1.75^2) ≈ 22.9

    def test_vital_sign_incomplete_bp_invalid(self) -> None:
        """Test that BP must have both systolic and diastolic."""
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            VitalSign(
                patient_mrn="MRN003",
                observation_time=datetime(2025, 1, 26, 14, 0),
                systolic_bp=120,
                # Missing diastolic_bp
            )

        assert "Both systolic and diastolic BP must be provided together" in str(exc_info.value)

    def test_vital_sign_systolic_less_than_diastolic_invalid(self) -> None:
        """Test that systolic must be greater than diastolic."""
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            VitalSign(
                patient_mrn="MRN004",
                observation_time=datetime(2025, 1, 26, 14, 0),
                systolic_bp=80,
                diastolic_bp=120,  # Greater than systolic
            )

        assert "Systolic BP must be greater than diastolic BP" in str(exc_info.value)

    def test_vital_sign_temperature_range_validation(self) -> None:
        """Test temperature range validation."""
        # Arrange & Act & Assert
        with pytest.raises(ValidationError):
            VitalSign(
                patient_mrn="MRN005",
                observation_time=datetime(2025, 1, 26, 14, 0),
                temperature=150.0,  # Too high
            )


class TestClinicalNote:
    """Tests for ClinicalNote model."""

    def test_clinical_note_creation_valid(self) -> None:
        """Test creating a valid clinical note."""
        # Arrange & Act
        note = ClinicalNote(
            note_type="Progress Note",
            patient_mrn="MRN12345",
            encounter_id="V12345",
            note_time=datetime(2025, 1, 26, 10, 0),
            text="Patient reports improvement in symptoms.",
            author="Dr. Jane Smith",
        )

        # Assert
        assert note.note_type == "Progress Note"
        assert "improvement" in note.text

    def test_clinical_note_future_time_invalid(self) -> None:
        """Test that future note times are rejected."""
        # Arrange
        future_time = datetime.now() + timedelta(hours=1)

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            ClinicalNote(
                note_type="Test Note",
                patient_mrn="MRN001",
                note_time=future_time,
                text="Future note",
            )

        assert "Note time cannot be in the future" in str(exc_info.value)
