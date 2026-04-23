"""Tests for validation framework."""

from datetime import date, datetime, timedelta

from healthsim.person import PersonName

from patientsim.core import (
    Diagnosis,
    Encounter,
    EncounterClass,
    EncounterStatus,
    Gender,
    LabResult,
    Medication,
    Patient,
    PatientGenerator,
    VitalSign,
)
from patientsim.validation import (
    AgeAppropriatenessValidator,
    ClinicalCoherenceValidator,
    ReferentialIntegrityValidator,
    TemporalValidator,
    ValidationSeverity,
    VitalSignPlausibilityValidator,
    validate_patient_record,
)


class TestValidationResult:
    """Tests for ValidationResult."""

    def test_validation_result_initially_valid(self) -> None:
        """Test that ValidationResult starts valid."""
        # Arrange
        from patientsim.validation.base import ValidationResult

        # Act
        result = ValidationResult(valid=True)

        # Assert
        assert result.valid is True
        assert len(result.issues) == 0
        assert len(result.errors) == 0
        assert len(result.warnings) == 0

    def test_add_error_makes_invalid(self) -> None:
        """Test that adding an error makes result invalid."""
        # Arrange
        from patientsim.validation.base import ValidationResult

        result = ValidationResult(valid=True)

        # Act
        result.add_issue(
            code="TEST_001",
            message="Test error",
            severity=ValidationSeverity.ERROR,
        )

        # Assert
        assert result.valid is False
        assert len(result.errors) == 1
        assert result.errors[0].code == "TEST_001"

    def test_add_warning_keeps_valid(self) -> None:
        """Test that adding a warning keeps result valid."""
        # Arrange
        from patientsim.validation.base import ValidationResult

        result = ValidationResult(valid=True)

        # Act
        result.add_issue(
            code="TEST_002",
            message="Test warning",
            severity=ValidationSeverity.WARNING,
        )

        # Assert
        assert result.valid is True
        assert len(result.warnings) == 1
        assert len(result.errors) == 0


class TestTemporalValidator:
    """Tests for TemporalValidator."""

    def test_valid_patient_passes(self) -> None:
        """Test that valid patient passes temporal validation."""
        # Arrange
        validator = TemporalValidator()
        patient = Patient(
            id="patient-001",
            mrn="MRN001",
            name=PersonName(given_name="Test", family_name="Patient"),
            birth_date=date(1980, 1, 15),
            gender=Gender.MALE,
        )

        # Act
        result = validator.validate_patient(patient)

        # Assert
        assert result.valid is True
        assert len(result.issues) == 0

    def test_valid_encounter_passes(self) -> None:
        """Test that valid encounter passes temporal validation."""
        # Arrange
        validator = TemporalValidator()
        encounter = Encounter(
            encounter_id="V001",
            patient_mrn="MRN001",
            class_code=EncounterClass.INPATIENT,
            status=EncounterStatus.FINISHED,
            admission_time=datetime(2025, 1, 1, 10, 0),
            discharge_time=datetime(2025, 1, 3, 14, 0),
        )

        # Act
        result = validator.validate_encounter(encounter)

        # Assert
        assert result.valid is True

    def test_future_admission_warning(self) -> None:
        """Test that future admission generates warning."""
        # Arrange
        validator = TemporalValidator()
        future = datetime.now() + timedelta(days=1)
        encounter = Encounter(
            encounter_id="V002",
            patient_mrn="MRN001",
            class_code=EncounterClass.OUTPATIENT,
            status=EncounterStatus.PLANNED,
            admission_time=future,
        )

        # Act
        result = validator.validate_encounter(encounter)

        # Assert
        assert result.valid is True  # Warning, not error
        assert len(result.warnings) == 1
        assert result.warnings[0].code == "TEMP_002"

    def test_unusually_long_stay_warning(self) -> None:
        """Test that unusually long stay generates warning."""
        # Arrange
        validator = TemporalValidator()
        admission = datetime(2023, 1, 1, 10, 0)
        discharge = datetime(2025, 1, 1, 10, 0)  # 2 years later
        encounter = Encounter(
            encounter_id="V003",
            patient_mrn="MRN001",
            class_code=EncounterClass.INPATIENT,
            status=EncounterStatus.FINISHED,
            admission_time=admission,
            discharge_time=discharge,
        )

        # Act
        result = validator.validate_encounter(encounter)

        # Assert
        assert result.valid is True  # Warning, not error
        assert len(result.warnings) >= 1
        assert any(w.code == "TEMP_003" for w in result.warnings)

    def test_lab_before_admission_warning(self) -> None:
        """Test that lab collected before admission generates warning."""
        # Arrange
        validator = TemporalValidator()
        encounter = Encounter(
            encounter_id="V004",
            patient_mrn="MRN001",
            class_code=EncounterClass.INPATIENT,
            status=EncounterStatus.IN_PROGRESS,
            admission_time=datetime(2025, 1, 26, 10, 0),
        )
        lab = LabResult(
            test_name="Glucose",
            value="95",
            patient_mrn="MRN001",
            encounter_id="V004",
            collected_time=datetime(2025, 1, 25, 10, 0),  # Before admission
            resulted_time=datetime(2025, 1, 25, 12, 0),
        )

        # Act
        result = validator.validate_lab_in_encounter(lab, encounter)

        # Assert
        assert result.valid is True  # Warning, not error
        assert len(result.warnings) == 1
        assert result.warnings[0].code == "TEMP_005"


class TestReferentialIntegrityValidator:
    """Tests for ReferentialIntegrityValidator."""

    def test_valid_diagnosis_reference(self) -> None:
        """Test that valid diagnosis reference passes."""
        # Arrange
        validator = ReferentialIntegrityValidator()
        patient = Patient(
            id="patient-002",
            mrn="MRN001",
            name=PersonName(given_name="Test", family_name="Patient"),
            birth_date=date(1980, 1, 15),
            gender=Gender.MALE,
        )
        diagnosis = Diagnosis(
            code="E11.9",
            description="Type 2 diabetes",
            patient_mrn="MRN001",
            diagnosed_date=date(2024, 6, 15),
        )

        # Act
        result = validator.validate_diagnosis(diagnosis, patient)

        # Assert
        assert result.valid is True
        assert len(result.issues) == 0

    def test_invalid_diagnosis_mrn_error(self) -> None:
        """Test that mismatched diagnosis MRN generates error."""
        # Arrange
        validator = ReferentialIntegrityValidator()
        patient = Patient(
            id="patient-003",
            mrn="MRN001",
            name=PersonName(given_name="Test", family_name="Patient"),
            birth_date=date(1980, 1, 15),
            gender=Gender.MALE,
        )
        diagnosis = Diagnosis(
            code="E11.9",
            description="Type 2 diabetes",
            patient_mrn="MRN999",  # Wrong MRN
            diagnosed_date=date(2024, 6, 15),
        )

        # Act
        result = validator.validate_diagnosis(diagnosis, patient)

        # Assert
        assert result.valid is False
        assert len(result.errors) == 1
        assert result.errors[0].code == "REF_001"

    def test_valid_encounter_reference(self) -> None:
        """Test that valid encounter reference passes."""
        # Arrange
        validator = ReferentialIntegrityValidator()
        patient = Patient(
            id="patient-004",
            mrn="MRN001",
            name=PersonName(given_name="Test", family_name="Patient"),
            birth_date=date(1980, 1, 15),
            gender=Gender.MALE,
        )
        encounter = Encounter(
            encounter_id="V001",
            patient_mrn="MRN001",
            class_code=EncounterClass.OUTPATIENT,
            status=EncounterStatus.FINISHED,
            admission_time=datetime(2025, 1, 26, 10, 0),
        )

        # Act
        result = validator.validate_encounter_patient(encounter, patient)

        # Assert
        assert result.valid is True
        assert len(result.issues) == 0

    def test_invalid_encounter_mrn_error(self) -> None:
        """Test that mismatched encounter MRN generates error."""
        # Arrange
        validator = ReferentialIntegrityValidator()
        patient = Patient(
            id="patient-005",
            mrn="MRN001",
            name=PersonName(given_name="Test", family_name="Patient"),
            birth_date=date(1980, 1, 15),
            gender=Gender.MALE,
        )
        encounter = Encounter(
            encounter_id="V001",
            patient_mrn="MRN999",  # Wrong MRN
            class_code=EncounterClass.OUTPATIENT,
            status=EncounterStatus.FINISHED,
            admission_time=datetime(2025, 1, 26, 10, 0),
        )

        # Act
        result = validator.validate_encounter_patient(encounter, patient)

        # Assert
        assert result.valid is False
        assert len(result.errors) == 1
        assert result.errors[0].code == "REF_002"


class TestAgeAppropriatenessValidator:
    """Tests for AgeAppropriatenessValidator."""

    def test_geriatric_condition_in_elderly_passes(self) -> None:
        """Test that geriatric condition in elderly patient passes."""
        # Arrange
        validator = AgeAppropriatenessValidator()
        patient = Patient(
            id="patient-006",
            mrn="MRN001",
            name=PersonName(given_name="Test", family_name="Patient"),
            birth_date=date(1950, 1, 15),  # ~75 years old
            gender=Gender.MALE,
        )
        diagnosis = Diagnosis(
            code="I50.9",
            description="Heart failure",
            patient_mrn="MRN001",
            diagnosed_date=date(2024, 6, 15),
        )

        # Act
        result = validator.validate_diagnosis_age(diagnosis, patient)

        # Assert
        assert result.valid is True
        assert len(result.warnings) == 0

    def test_geriatric_condition_in_young_patient_warning(self) -> None:
        """Test that geriatric condition in young patient generates warning."""
        # Arrange
        validator = AgeAppropriatenessValidator()
        patient = Patient(
            id="patient-007",
            mrn="MRN001",
            name=PersonName(given_name="Test", family_name="Patient"),
            birth_date=date(2000, 1, 15),  # ~25 years old
            gender=Gender.MALE,
        )
        diagnosis = Diagnosis(
            code="I50.9",
            description="Heart failure",
            patient_mrn="MRN001",
            diagnosed_date=date(2024, 6, 15),
        )

        # Act
        result = validator.validate_diagnosis_age(diagnosis, patient)

        # Assert
        assert result.valid is True  # Warning, not error
        assert len(result.warnings) == 1
        assert result.warnings[0].code == "CLIN_001"


class TestClinicalCoherenceValidator:
    """Tests for ClinicalCoherenceValidator."""

    def test_medication_with_indication_passes(self) -> None:
        """Test that medication with appropriate diagnosis passes."""
        # Arrange
        validator = ClinicalCoherenceValidator()
        medication = Medication(
            name="Metformin",
            code="860975",
            dose="500 mg",
            route="PO",
            frequency="BID",
            patient_mrn="MRN001",
            start_date=datetime(2024, 6, 15),
        )
        diagnoses = [
            Diagnosis(
                code="E11.9",
                description="Type 2 diabetes",
                patient_mrn="MRN001",
                diagnosed_date=date(2024, 6, 15),
            )
        ]

        # Act
        result = validator.validate_medication_indication(medication, diagnoses)

        # Assert
        assert result.valid is True
        assert len(result.infos) == 0

    def test_medication_without_indication_info(self) -> None:
        """Test that medication without typical indication generates info."""
        # Arrange
        validator = ClinicalCoherenceValidator()
        medication = Medication(
            name="Metformin",
            code="860975",
            dose="500 mg",
            route="PO",
            frequency="BID",
            patient_mrn="MRN001",
            start_date=datetime(2024, 6, 15),
        )
        diagnoses = [
            Diagnosis(
                code="I10",
                description="Hypertension",
                patient_mrn="MRN001",
                diagnosed_date=date(2024, 6, 15),
            )
        ]

        # Act
        result = validator.validate_medication_indication(medication, diagnoses)

        # Assert
        assert result.valid is True
        assert len(result.infos) == 1
        assert result.infos[0].code == "CLIN_004"


class TestVitalSignPlausibilityValidator:
    """Tests for VitalSignPlausibilityValidator."""

    def test_normal_vitals_pass(self) -> None:
        """Test that normal vitals pass validation."""
        # Arrange
        validator = VitalSignPlausibilityValidator()
        patient = Patient(
            id="patient-008",
            mrn="MRN001",
            name=PersonName(given_name="Test", family_name="Patient"),
            birth_date=date(1980, 1, 15),
            gender=Gender.MALE,
        )
        vitals = VitalSign(
            patient_mrn="MRN001",
            observation_time=datetime(2025, 1, 26, 10, 0),
            temperature=98.6,
            heart_rate=72,
            respiratory_rate=16,
            systolic_bp=120,
            diastolic_bp=80,
            spo2=98,
        )

        # Act
        result = validator.validate_vitals(vitals, patient)

        # Assert
        assert result.valid is True
        assert len(result.warnings) == 0

    def test_critically_high_temperature_warning(self) -> None:
        """Test that critically high temperature generates warning."""
        # Arrange
        validator = VitalSignPlausibilityValidator()
        patient = Patient(
            id="patient-009",
            mrn="MRN001",
            name=PersonName(given_name="Test", family_name="Patient"),
            birth_date=date(1980, 1, 15),
            gender=Gender.MALE,
        )
        vitals = VitalSign(
            patient_mrn="MRN001",
            observation_time=datetime(2025, 1, 26, 10, 0),
            temperature=107.0,  # Critically high
        )

        # Act
        result = validator.validate_vitals(vitals, patient)

        # Assert
        assert result.valid is True  # Warning, not error
        assert len(result.warnings) >= 1
        assert any(w.code == "CLIN_006" for w in result.warnings)

    def test_critically_low_spo2_warning(self) -> None:
        """Test that critically low SpO2 generates warning."""
        # Arrange
        validator = VitalSignPlausibilityValidator()
        patient = Patient(
            id="patient-010",
            mrn="MRN001",
            name=PersonName(given_name="Test", family_name="Patient"),
            birth_date=date(1980, 1, 15),
            gender=Gender.MALE,
        )
        vitals = VitalSign(
            patient_mrn="MRN001",
            observation_time=datetime(2025, 1, 26, 10, 0),
            spo2=80,  # Critically low
        )

        # Act
        result = validator.validate_vitals(vitals, patient)

        # Assert
        assert result.valid is True  # Warning, not error
        assert len(result.warnings) >= 1
        assert any(w.code == "CLIN_010" for w in result.warnings)

    def test_narrow_pulse_pressure_warning(self) -> None:
        """Test that narrow pulse pressure generates warning."""
        # Arrange
        validator = VitalSignPlausibilityValidator()
        patient = Patient(
            id="patient-011",
            mrn="MRN001",
            name=PersonName(given_name="Test", family_name="Patient"),
            birth_date=date(1980, 1, 15),
            gender=Gender.MALE,
        )
        vitals = VitalSign(
            patient_mrn="MRN001",
            observation_time=datetime(2025, 1, 26, 10, 0),
            systolic_bp=100,
            diastolic_bp=95,  # Pulse pressure = 5
        )

        # Act
        result = validator.validate_vitals(vitals, patient)

        # Assert
        assert result.valid is True  # Warning, not error
        assert len(result.warnings) >= 1
        assert any(w.code == "CLIN_011" for w in result.warnings)


class TestValidatePatientRecord:
    """Tests for validate_patient_record convenience function."""

    def test_generated_patient_passes_validation(self) -> None:
        """Test that generator-created patient passes validation."""
        # Arrange
        gen = PatientGenerator(seed=42)
        patient = gen.generate_patient()

        # Act
        result = validate_patient_record(patient)

        # Assert
        assert result.valid is True

    def test_complete_patient_record_passes(self) -> None:
        """Test that complete patient record passes validation."""
        # Arrange
        gen = PatientGenerator(seed=42)
        patient = gen.generate_patient()
        encounter = gen.generate_encounter(patient)
        diagnosis = gen.generate_diagnosis(patient, encounter)
        medication = gen.generate_medication(patient, encounter)
        lab = gen.generate_lab_result(patient, encounter)
        vitals = gen.generate_vital_signs(patient, encounter)

        # Act
        result = validate_patient_record(
            patient=patient,
            encounters=[encounter],
            diagnoses=[diagnosis],
            medications=[medication],
            labs=[lab],
            vitals=[vitals],
        )

        # Assert
        assert result.valid is True

    def test_invalid_mrn_detected(self) -> None:
        """Test that invalid MRN reference is detected."""
        # Arrange
        gen = PatientGenerator(seed=42)
        patient = gen.generate_patient()
        diagnosis = gen.generate_diagnosis(patient)

        # Corrupt the MRN
        diagnosis.patient_mrn = "INVALID_MRN"

        # Act
        result = validate_patient_record(patient=patient, diagnoses=[diagnosis])

        # Assert
        assert result.valid is False
        assert len(result.errors) >= 1
        assert any(e.code == "REF_001" for e in result.errors)
