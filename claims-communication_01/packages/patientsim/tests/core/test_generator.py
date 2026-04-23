"""Tests for patient data generation."""

from datetime import date, datetime

import pytest

from patientsim.core import (
    EncounterClass,
    EncounterStatus,
    Gender,
    MedicationStatus,
    PatientGenerator,
    generate_patient,
)


class TestPatientGenerator:
    """Tests for PatientGenerator class."""

    def test_generator_initialization_default(self) -> None:
        """Test generator initialization with default settings."""
        # Arrange & Act
        gen = PatientGenerator()

        # Assert
        assert gen.faker is not None
        assert gen.seed is None

    def test_generator_initialization_with_seed(self) -> None:
        """Test generator initialization with seed."""
        # Arrange & Act
        gen = PatientGenerator(seed=42)

        # Assert
        assert gen.seed == 42

    def test_generator_reproducibility_same_seed(self) -> None:
        """Test that same seed produces same patient."""
        # Arrange & Act - Create and use generators separately to reset state
        gen1 = PatientGenerator(seed=42)
        patient1 = gen1.generate_patient()

        # Create second generator with same seed
        gen2 = PatientGenerator(seed=42)
        patient2 = gen2.generate_patient()

        # Assert - All fields should be identical
        assert patient1.mrn == patient2.mrn
        assert patient1.given_name == patient2.given_name
        assert patient1.family_name == patient2.family_name
        assert patient1.birth_date == patient2.birth_date
        assert patient1.gender == patient2.gender
        assert patient1.contact.email == patient2.contact.email

    def test_generator_reproducibility_different_seeds(self) -> None:
        """Test that different seeds produce different patients."""
        # Arrange
        gen1 = PatientGenerator(seed=42)
        gen2 = PatientGenerator(seed=123)

        # Act
        patient1 = gen1.generate_patient()
        patient2 = gen2.generate_patient()

        # Assert - At least some fields should differ
        assert (
            patient1.mrn != patient2.mrn
            or patient1.given_name != patient2.given_name
            or patient1.family_name != patient2.family_name
        )


class TestPatientGeneration:
    """Tests for patient generation."""

    def test_generate_patient_default(self) -> None:
        """Test generating patient with default parameters."""
        # Arrange
        gen = PatientGenerator(seed=42)

        # Act
        patient = gen.generate_patient()

        # Assert
        assert patient.mrn.startswith("MRN")
        assert patient.id.startswith("patient-")
        assert len(patient.given_name) > 0
        assert len(patient.family_name) > 0
        assert patient.birth_date < date.today()
        assert patient.gender in list(Gender)
        assert 18 <= patient.age <= 85  # Default range

    def test_generate_patient_age_range_constraint(self) -> None:
        """Test that age range constraint is respected."""
        # Arrange
        gen = PatientGenerator(seed=42)

        # Act
        patient = gen.generate_patient(age_range=(65, 75))

        # Assert
        assert 65 <= patient.age <= 75

    def test_generate_patient_gender_specification(self) -> None:
        """Test generating patient with specific gender."""
        # Arrange
        gen = PatientGenerator(seed=42)

        # Act
        patient_male = gen.generate_patient(gender=Gender.MALE)
        patient_female = gen.generate_patient(gender=Gender.FEMALE)

        # Assert
        assert patient_male.gender == Gender.MALE
        assert patient_female.gender == Gender.FEMALE

    def test_generate_patient_has_contact_info(self) -> None:
        """Test that patient has contact information."""
        # Arrange
        gen = PatientGenerator(seed=42)

        # Act
        patient = gen.generate_patient()

        # Assert
        assert patient.contact is not None
        assert patient.contact.phone is not None
        assert patient.contact.email is not None
        assert "@" in patient.contact.email

    def test_generate_patient_has_address(self) -> None:
        """Test that patient has complete address."""
        # Arrange
        gen = PatientGenerator(seed=42)

        # Act
        patient = gen.generate_patient()

        # Assert
        assert patient.address is not None
        assert patient.address.street_address is not None
        assert patient.address.city is not None
        assert patient.address.state is not None
        assert patient.address.postal_code is not None

    def test_generate_patient_has_identifiers(self) -> None:
        """Test that patient has proper identifiers."""
        # Arrange
        gen = PatientGenerator(seed=42)

        # Act
        patient = gen.generate_patient()

        # Assert
        assert patient.id is not None
        assert patient.mrn is not None
        assert patient.ssn is not None
        assert len(patient.ssn) == 9  # SSN format: 9 digits


class TestEncounterGeneration:
    """Tests for encounter generation."""

    def test_generate_encounter_default(self) -> None:
        """Test generating encounter with default parameters."""
        # Arrange
        gen = PatientGenerator(seed=42)
        patient = gen.generate_patient()

        # Act
        encounter = gen.generate_encounter(patient)

        # Assert
        assert encounter.encounter_id.startswith("V")
        assert encounter.patient_mrn == patient.mrn
        assert encounter.class_code in list(EncounterClass)
        assert encounter.status in list(EncounterStatus)
        assert encounter.admission_time <= datetime.now()

    def test_generate_encounter_specific_class(self) -> None:
        """Test generating encounter with specific class."""
        # Arrange
        gen = PatientGenerator(seed=42)
        patient = gen.generate_patient()

        # Act
        encounter = gen.generate_encounter(patient, encounter_class=EncounterClass.INPATIENT)

        # Assert
        assert encounter.class_code == EncounterClass.INPATIENT

    def test_generate_encounter_timing_logic(self) -> None:
        """Test that discharge is after admission."""
        # Arrange
        gen = PatientGenerator(seed=42)
        patient = gen.generate_patient()

        # Act
        encounter = gen.generate_encounter(
            patient, encounter_class=EncounterClass.INPATIENT, length_of_stay_days=3
        )

        # Assert
        if encounter.discharge_time:
            assert encounter.discharge_time > encounter.admission_time

    def test_generate_encounter_length_of_stay(self) -> None:
        """Test length of stay calculation."""
        # Arrange
        gen = PatientGenerator(seed=42)
        patient = gen.generate_patient()
        admission = datetime(2025, 1, 26, 10, 0)

        # Act
        encounter = gen.generate_encounter(
            patient,
            encounter_class=EncounterClass.INPATIENT,
            admission_date=admission,
            length_of_stay_days=2,
        )

        # Assert
        assert encounter.status == EncounterStatus.FINISHED
        assert encounter.discharge_time is not None
        # Should be roughly 2 days (48 hours) + random hours (8-18)
        los_hours = encounter.length_of_stay_hours
        assert los_hours is not None
        assert 48 <= los_hours <= 66  # 2 days + up to 18 random hours

    def test_generate_encounter_inpatient_has_location(self) -> None:
        """Test that inpatient encounters have location details."""
        # Arrange
        gen = PatientGenerator(seed=42)
        patient = gen.generate_patient()

        # Act
        encounter = gen.generate_encounter(patient, encounter_class=EncounterClass.INPATIENT)

        # Assert
        # Inpatient should have department assigned (probabilistic, but seed makes it deterministic)
        assert encounter.facility is not None


class TestDiagnosisGeneration:
    """Tests for diagnosis generation."""

    def test_generate_diagnosis_default(self) -> None:
        """Test generating diagnosis with default parameters."""
        # Arrange
        gen = PatientGenerator(seed=42)
        patient = gen.generate_patient()

        # Act
        diagnosis = gen.generate_diagnosis(patient)

        # Assert
        assert len(diagnosis.code) > 0
        assert len(diagnosis.description) > 0
        assert diagnosis.patient_mrn == patient.mrn
        assert diagnosis.diagnosed_date <= date.today()

    def test_generate_diagnosis_specific_category(self) -> None:
        """Test generating diagnosis from specific category."""
        # Arrange
        gen = PatientGenerator(seed=42)
        patient = gen.generate_patient()

        # Act
        diagnosis = gen.generate_diagnosis(patient, category="diabetes")

        # Assert
        # Should be a diabetes-related ICD-10 code
        assert diagnosis.code.startswith("E1")  # Diabetes codes start with E10 or E11

    def test_generate_diagnosis_with_encounter(self) -> None:
        """Test linking diagnosis to encounter."""
        # Arrange
        gen = PatientGenerator(seed=42)
        patient = gen.generate_patient()
        encounter = gen.generate_encounter(patient)

        # Act
        diagnosis = gen.generate_diagnosis(patient, encounter=encounter)

        # Assert
        assert diagnosis.encounter_id == encounter.encounter_id

    def test_generate_diagnosis_invalid_category(self) -> None:
        """Test that invalid category raises error."""
        # Arrange
        gen = PatientGenerator(seed=42)
        patient = gen.generate_patient()

        # Act & Assert
        with pytest.raises(ValueError, match="No diagnoses found for category"):
            gen.generate_diagnosis(patient, category="invalid_category")


class TestLabResultGeneration:
    """Tests for lab result generation."""

    def test_generate_lab_result_default(self) -> None:
        """Test generating lab result with default parameters."""
        # Arrange
        gen = PatientGenerator(seed=42)
        patient = gen.generate_patient()

        # Act
        lab = gen.generate_lab_result(patient)

        # Assert
        assert len(lab.test_name) > 0
        assert lab.patient_mrn == patient.mrn
        assert lab.collected_time <= datetime.now()
        assert lab.resulted_time > lab.collected_time

    def test_generate_lab_result_specific_test(self) -> None:
        """Test generating specific lab test."""
        # Arrange
        gen = PatientGenerator(seed=42)
        patient = gen.generate_patient()

        # Act
        lab = gen.generate_lab_result(patient, test_name="Glucose")

        # Assert
        assert lab.test_name == "Glucose"
        assert lab.loinc_code == "2345-7"
        assert lab.unit == "mg/dL"

    def test_generate_lab_result_normal_value(self) -> None:
        """Test generating normal lab value."""
        # Arrange
        gen = PatientGenerator(seed=42)
        patient = gen.generate_patient()

        # Act
        lab = gen.generate_lab_result(patient, test_name="Glucose", make_abnormal=False)

        # Assert
        value = float(lab.value)
        assert 70 <= value <= 100  # Normal glucose range
        assert lab.abnormal_flag is None

    def test_generate_lab_result_abnormal_value(self) -> None:
        """Test generating abnormal lab value."""
        # Arrange
        gen = PatientGenerator(seed=42)
        patient = gen.generate_patient()

        # Act
        lab = gen.generate_lab_result(patient, test_name="Glucose", make_abnormal=True)

        # Assert
        value = float(lab.value)
        # Should be outside normal range (70-100)
        assert value < 70 or value > 100
        assert lab.abnormal_flag in ["L", "LL", "H", "HH"]

    def test_generate_lab_result_invalid_test(self) -> None:
        """Test that invalid test name raises error."""
        # Arrange
        gen = PatientGenerator(seed=42)
        patient = gen.generate_patient()

        # Act & Assert
        with pytest.raises(ValueError, match="Unknown lab test"):
            gen.generate_lab_result(patient, test_name="InvalidTest")

    def test_generate_lab_result_with_encounter(self) -> None:
        """Test linking lab to encounter."""
        # Arrange
        gen = PatientGenerator(seed=42)
        patient = gen.generate_patient()
        encounter = gen.generate_encounter(patient)

        # Act
        lab = gen.generate_lab_result(patient, encounter=encounter)

        # Assert
        assert lab.encounter_id == encounter.encounter_id
        # Lab should be collected after admission
        assert lab.collected_time >= encounter.admission_time


class TestVitalSignsGeneration:
    """Tests for vital signs generation."""

    def test_generate_vital_signs_default(self) -> None:
        """Test generating vital signs with default parameters."""
        # Arrange
        gen = PatientGenerator(seed=42)
        patient = gen.generate_patient()

        # Act
        vitals = gen.generate_vital_signs(patient)

        # Assert
        assert vitals.patient_mrn == patient.mrn
        assert vitals.temperature is not None
        assert vitals.heart_rate is not None
        assert vitals.respiratory_rate is not None
        assert vitals.systolic_bp is not None
        assert vitals.diastolic_bp is not None
        assert vitals.spo2 is not None

    def test_generate_vital_signs_age_appropriate(self) -> None:
        """Test that vitals are age-appropriate."""
        # Arrange
        gen = PatientGenerator(seed=42)
        adult_patient = gen.generate_patient(age_range=(25, 35))
        pediatric_patient = gen.generate_patient(age_range=(5, 10))

        # Act
        adult_vitals = gen.generate_vital_signs(adult_patient)
        pediatric_vitals = gen.generate_vital_signs(pediatric_patient)

        # Assert - Adult ranges
        assert 60 <= adult_vitals.heart_rate <= 100
        assert 12 <= adult_vitals.respiratory_rate <= 20

        # Pediatric ranges (higher heart rate and respiratory rate)
        assert 70 <= pediatric_vitals.heart_rate <= 120
        assert 20 <= pediatric_vitals.respiratory_rate <= 30

    def test_generate_vital_signs_abnormal_temperature(self) -> None:
        """Test generating abnormal temperature."""
        # Arrange
        gen = PatientGenerator(seed=42)
        patient = gen.generate_patient()

        # Act
        vitals = gen.generate_vital_signs(patient, abnormal_parameters=["temperature"])

        # Assert
        assert vitals.temperature is not None
        # Fever range
        assert vitals.temperature > 100.4

    def test_generate_vital_signs_abnormal_blood_pressure(self) -> None:
        """Test generating abnormal blood pressure."""
        # Arrange
        gen = PatientGenerator(seed=42)
        patient = gen.generate_patient()

        # Act
        vitals = gen.generate_vital_signs(patient, abnormal_parameters=["blood_pressure"])

        # Assert
        # Hypertensive (above normal adult range)
        assert vitals.systolic_bp > 140

    def test_generate_vital_signs_blood_pressure_property(self) -> None:
        """Test blood pressure property formatting."""
        # Arrange
        gen = PatientGenerator(seed=42)
        patient = gen.generate_patient()

        # Act
        vitals = gen.generate_vital_signs(patient)

        # Assert
        bp = vitals.blood_pressure
        assert "/" in bp
        parts = bp.split("/")
        assert len(parts) == 2
        assert int(parts[0]) > int(parts[1])  # Systolic > diastolic

    def test_generate_vital_signs_bmi_calculation(self) -> None:
        """Test that BMI is calculated when height/weight present."""
        # Arrange
        gen = PatientGenerator(seed=42)
        patient = gen.generate_patient()

        # Act
        vitals = gen.generate_vital_signs(patient)

        # Assert
        assert vitals.height_cm is not None
        assert vitals.weight_kg is not None
        assert vitals.bmi is not None
        # BMI should be in reasonable range
        assert 10 < vitals.bmi < 60


class TestMedicationGeneration:
    """Tests for medication generation."""

    def test_generate_medication_default(self) -> None:
        """Test generating medication with default parameters."""
        # Arrange
        gen = PatientGenerator(seed=42)
        patient = gen.generate_patient()

        # Act
        med = gen.generate_medication(patient)

        # Assert
        assert len(med.name) > 0
        assert med.patient_mrn == patient.mrn
        assert med.dose is not None
        assert med.route is not None
        assert med.frequency is not None
        assert med.status in list(MedicationStatus)

    def test_generate_medication_specific_drug(self) -> None:
        """Test generating specific medication."""
        # Arrange
        gen = PatientGenerator(seed=42)
        patient = gen.generate_patient()

        # Act
        med = gen.generate_medication(patient, medication_name="Metformin")

        # Assert
        assert med.name == "Metformin"
        assert med.code == "860975"  # RxNorm code
        assert "mg" in med.dose

    def test_generate_medication_invalid_drug(self) -> None:
        """Test that invalid medication raises error."""
        # Arrange
        gen = PatientGenerator(seed=42)
        patient = gen.generate_patient()

        # Act & Assert
        with pytest.raises(ValueError, match="Unknown medication"):
            gen.generate_medication(patient, medication_name="InvalidDrug")

    def test_generate_medication_with_encounter(self) -> None:
        """Test linking medication to encounter."""
        # Arrange
        gen = PatientGenerator(seed=42)
        patient = gen.generate_patient()
        encounter = gen.generate_encounter(patient)

        # Act
        med = gen.generate_medication(patient, encounter=encounter)

        # Assert
        assert med.encounter_id == encounter.encounter_id
        assert med.start_date >= encounter.admission_time

    def test_generate_medication_status_distribution(self) -> None:
        """Test that medication statuses vary."""
        # Arrange
        gen = PatientGenerator(seed=42)
        patient = gen.generate_patient()

        # Act - Generate multiple medications to see status variation
        meds = [gen.generate_medication(patient) for _ in range(20)]
        statuses = {med.status for med in meds}

        # Assert - Should have at least 2 different statuses
        assert len(statuses) >= 2

    def test_generate_medication_end_date_logic(self) -> None:
        """Test that non-active medications have end dates."""
        # Arrange
        gen = PatientGenerator(seed=42)
        patient = gen.generate_patient()

        # Act - Generate many to ensure we get a non-active one
        meds = [gen.generate_medication(patient) for _ in range(50)]
        non_active_meds = [m for m in meds if m.status != MedicationStatus.ACTIVE]

        # Assert
        if non_active_meds:  # If we got any non-active meds
            for med in non_active_meds:
                assert med.end_date is not None
                assert med.end_date > med.start_date


class TestConvenienceFunction:
    """Tests for convenience functions."""

    def test_generate_patient_function(self) -> None:
        """Test the convenience generate_patient function."""
        # Act
        patient = generate_patient(seed=42)

        # Assert
        assert patient.mrn is not None
        assert patient.age >= 18

    def test_generate_patient_function_with_params(self) -> None:
        """Test convenience function with parameters."""
        # Act
        patient = generate_patient(seed=42, age_range=(60, 70), gender=Gender.FEMALE)

        # Assert
        assert 60 <= patient.age <= 70
        assert patient.gender == Gender.FEMALE
