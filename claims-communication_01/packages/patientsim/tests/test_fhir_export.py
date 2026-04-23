"""Tests for FHIR R4 export functionality."""

import json
from datetime import date, datetime

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
from patientsim.formats.fhir.resources import (
    CodeSystems,
    get_loinc_code,
    get_vital_loinc,
)
from patientsim.formats.fhir.transformer import FHIRTransformer


class TestLoincMappings:
    """Tests for LOINC code mappings."""

    def test_common_lab_loinc_codes(self) -> None:
        """Test mapping of common lab names to LOINC codes."""
        assert get_loinc_code("hemoglobin") == ("718-7", "Hemoglobin [Mass/volume] in Blood")
        assert get_loinc_code("wbc") == ("6690-2", "Leukocytes [#/volume] in Blood")
        assert get_loinc_code("sodium") == ("2951-2", "Sodium [Moles/volume] in Serum or Plasma")
        assert get_loinc_code("creatinine") == (
            "2160-0",
            "Creatinine [Mass/volume] in Serum or Plasma",
        )

    def test_lab_aliases(self) -> None:
        """Test that lab aliases work correctly."""
        assert get_loinc_code("hgb") == get_loinc_code("hemoglobin")
        assert get_loinc_code("na") == get_loinc_code("sodium")
        assert get_loinc_code("k") == get_loinc_code("potassium")

    def test_unknown_lab_returns_none(self) -> None:
        """Test that unknown lab names return None."""
        assert get_loinc_code("unknown_test") is None
        assert get_loinc_code("nonexistent") is None

    def test_vital_sign_loinc_codes(self) -> None:
        """Test mapping of vital signs to LOINC codes."""
        assert get_vital_loinc("heart_rate") == ("8867-4", "Heart rate")
        assert get_vital_loinc("systolic_bp") == ("8480-6", "Systolic blood pressure")
        assert get_vital_loinc("temperature") == ("8310-5", "Body temperature")

    def test_vital_aliases(self) -> None:
        """Test that vital sign aliases work correctly."""
        assert get_vital_loinc("hr") == get_vital_loinc("heart_rate")
        assert get_vital_loinc("sbp") == get_vital_loinc("systolic_bp")
        assert get_vital_loinc("temp") == get_vital_loinc("temperature")


class TestPatientTransform:
    """Tests for Patient resource transformation."""

    def test_transform_patient(self) -> None:
        """Test transforming a patient to FHIR Patient resource."""
        patient = Patient(
            id="patient-001",
            mrn="MRN001",
            name=PersonName(given_name="John", family_name="Doe"),
            birth_date=date(1959, 3, 15),
            gender=Gender.MALE,
        )

        transformer = FHIRTransformer()
        resource = transformer.transform_patient(patient)

        assert resource.resourceType == "Patient"
        assert resource.id is not None
        assert len(resource.identifier) == 1
        assert resource.identifier[0].value == "MRN001"
        assert resource.identifier[0].system == CodeSystems.PATIENT_MRN
        assert len(resource.name) == 1
        assert resource.name[0].given == ["John"]
        assert resource.name[0].family == "Doe"
        assert resource.gender == "male"
        assert resource.birthDate == "1959-03-15"
        assert resource.deceasedBoolean is None

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

        transformer = FHIRTransformer()
        resource = transformer.transform_patient(patient)

        assert resource.deceasedBoolean is None  # Use dateTime when date available
        assert resource.deceasedDateTime == "2024-01-15"

    def test_patient_json_serialization(self) -> None:
        """Test that Patient resource can be serialized to JSON."""
        patient = Patient(
            id="patient-003",
            mrn="MRN003",
            name=PersonName(given_name="Test", family_name="User"),
            birth_date=date(1980, 1, 1),
            gender=Gender.MALE,
        )

        transformer = FHIRTransformer()
        resource = transformer.transform_patient(patient)

        # Should serialize without error
        json_str = resource.model_dump_json(by_alias=True, exclude_none=True)
        data = json.loads(json_str)

        assert data["resourceType"] == "Patient"
        assert data["gender"] == "male"
        assert "birthDate" in data


class TestEncounterTransform:
    """Tests for Encounter resource transformation."""

    def test_transform_encounter(self) -> None:
        """Test transforming an encounter to FHIR Encounter resource."""
        encounter = Encounter(
            encounter_id="ENC001",
            patient_mrn="MRN001",
            class_code=EncounterClass.EMERGENCY,
            status=EncounterStatus.FINISHED,
            admission_time=datetime(2024, 1, 15, 10, 30),
            discharge_time=datetime(2024, 1, 18, 14, 0),
            admitting_diagnosis="Sepsis",
        )

        transformer = FHIRTransformer()
        # Need to register patient first for reference
        patient = Patient(
            id="patient-004",
            mrn="MRN001",
            name=PersonName(given_name="John", family_name="Doe"),
            birth_date=date(1959, 3, 15),
            gender=Gender.MALE,
        )
        transformer.transform_patient(patient)

        resource = transformer.transform_encounter(encounter)

        assert resource.resourceType == "Encounter"
        assert resource.id is not None
        assert resource.status == "finished"
        assert resource.subject.reference.startswith("Patient/")
        assert resource.period is not None
        assert resource.period.start == "2024-01-15T10:30:00"
        assert resource.period.end == "2024-01-18T14:00:00"
        assert len(resource.reasonCode) == 1
        assert resource.reasonCode[0].text == "Sepsis"

    def test_encounter_class_mapping(self) -> None:
        """Test encounter class code mapping."""
        encounter = Encounter(
            encounter_id="ENC002",
            patient_mrn="MRN001",
            class_code=EncounterClass.INPATIENT,
            status=EncounterStatus.FINISHED,
            admission_time=datetime(2024, 1, 15, 10, 30),
        )

        transformer = FHIRTransformer()
        resource = transformer.transform_encounter(encounter)

        # Check class field (using alias)
        resource_dict = resource.model_dump(by_alias=True)
        assert "class" in resource_dict
        assert resource_dict["class"]["coding"][0]["code"] == "IMP"


class TestConditionTransform:
    """Tests for Condition resource transformation."""

    def test_transform_condition(self) -> None:
        """Test transforming a diagnosis to FHIR Condition resource."""
        diagnosis = Diagnosis(
            code="A41.9",
            description="Sepsis, unspecified organism",
            type=DiagnosisType.FINAL,
            patient_mrn="MRN001",
            encounter_id="ENC001",
            diagnosed_date=date(2024, 1, 15),
        )

        transformer = FHIRTransformer()
        resource = transformer.transform_condition(diagnosis)

        assert resource.resourceType == "Condition"
        assert resource.id is not None
        assert resource.code.coding[0]["system"] == CodeSystems.ICD10
        assert resource.code.coding[0]["code"] == "A41.9"
        assert resource.code.text == "Sepsis, unspecified organism"
        assert resource.subject.reference.startswith("Patient/")
        assert resource.encounter is not None
        assert resource.encounter.reference.startswith("Encounter/")
        assert resource.onsetDateTime == "2024-01-15"


class TestLabObservationTransform:
    """Tests for lab Observation resource transformation."""

    def test_transform_lab_observation(self) -> None:
        """Test transforming a lab result to FHIR Observation resource."""
        lab = LabResult(
            test_name="hemoglobin",
            value="12.5",
            unit="g/dL",
            patient_mrn="MRN001",
            encounter_id="ENC001",
            collected_time=datetime(2024, 1, 15, 14, 30),
        )

        transformer = FHIRTransformer()
        resource = transformer.transform_lab_observation(lab)

        assert resource is not None
        assert resource.resourceType == "Observation"
        assert resource.status == "final"
        assert len(resource.category) == 1
        assert resource.category[0].coding[0]["code"] == "laboratory"
        assert resource.code.coding[0]["system"] == CodeSystems.LOINC
        assert resource.code.coding[0]["code"] == "718-7"
        assert resource.subject.reference.startswith("Patient/")
        assert resource.effectiveDateTime is not None
        assert resource.valueQuantity is not None
        assert resource.valueQuantity.value == 12.5
        assert resource.valueQuantity.unit == "g/dL"

    def test_lab_without_loinc_returns_none(self) -> None:
        """Test that labs without LOINC mapping return None."""
        lab = LabResult(
            test_name="unknown_test",
            value="100",
            unit="units",
            patient_mrn="MRN001",
            collected_time=datetime(2024, 1, 15, 14, 30),
        )

        transformer = FHIRTransformer()
        resource = transformer.transform_lab_observation(lab)

        assert resource is None

    def test_lab_with_non_numeric_value(self) -> None:
        """Test lab with non-numeric value uses valueString."""
        lab = LabResult(
            test_name="hemoglobin",
            value="positive",
            unit="",
            patient_mrn="MRN001",
            collected_time=datetime(2024, 1, 15, 14, 30),
        )

        transformer = FHIRTransformer()
        resource = transformer.transform_lab_observation(lab)

        assert resource is not None
        assert resource.valueQuantity is None
        assert resource.valueString == "positive"


class TestVitalObservationTransform:
    """Tests for vital sign Observation resource transformation."""

    def test_transform_vital_observations(self) -> None:
        """Test transforming vital signs to FHIR Observation resources."""
        vital = VitalSign(
            patient_mrn="MRN001",
            encounter_id="ENC001",
            observation_time=datetime(2024, 1, 15, 12, 0),
            heart_rate=82,
            systolic_bp=128,
            diastolic_bp=80,
            temperature=98.6,
        )

        transformer = FHIRTransformer()
        resources = transformer.transform_vital_observations(vital)

        # Should create 4 observations (HR, SBP, DBP, Temp)
        assert len(resources) == 4

        # Check all are Observations with vital-signs category
        for resource in resources:
            assert resource.resourceType == "Observation"
            assert resource.status == "final"
            assert len(resource.category) == 1
            assert resource.category[0].coding[0]["code"] == "vital-signs"
            assert resource.code.coding[0]["system"] == CodeSystems.LOINC

        # Check specific vital signs
        loinc_codes = [r.code.coding[0]["code"] for r in resources]
        assert "8867-4" in loinc_codes  # Heart rate
        assert "8480-6" in loinc_codes  # Systolic BP
        assert "8462-4" in loinc_codes  # Diastolic BP
        assert "8310-5" in loinc_codes  # Temperature

    def test_vitals_with_partial_measurements(self) -> None:
        """Test that only recorded vitals create observations."""
        vital = VitalSign(
            patient_mrn="MRN001",
            observation_time=datetime(2024, 1, 15, 12, 0),
            heart_rate=82,
            # Only heart rate recorded
        )

        transformer = FHIRTransformer()
        resources = transformer.transform_vital_observations(vital)

        # Should only create 1 observation
        assert len(resources) == 1
        assert resources[0].code.coding[0]["code"] == "8867-4"  # Heart rate


class TestBundleCreation:
    """Tests for FHIR Bundle creation."""

    def test_create_empty_bundle(self) -> None:
        """Test creating an empty bundle."""
        transformer = FHIRTransformer()
        bundle = transformer.create_bundle()

        assert bundle.resourceType == "Bundle"
        assert bundle.type == "collection"
        assert bundle.id is not None
        assert len(bundle.entry) == 0

    def test_create_bundle_with_patient(self) -> None:
        """Test creating a bundle with a patient."""
        patient = Patient(
            id="patient-005",
            mrn="MRN001",
            name=PersonName(given_name="John", family_name="Doe"),
            birth_date=date(1959, 3, 15),
            gender=Gender.MALE,
        )

        transformer = FHIRTransformer()
        bundle = transformer.create_bundle(patients=[patient])

        assert len(bundle.entry) == 1
        assert bundle.entry[0].resource["resourceType"] == "Patient"
        assert bundle.entry[0].fullUrl.startswith("urn:uuid:")

    def test_create_complete_bundle(self) -> None:
        """Test creating a bundle with all resource types."""
        patient = Patient(
            id="patient-006",
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
            code="A41.9",
            description="Sepsis",
            type=DiagnosisType.FINAL,
            patient_mrn="MRN001",
            encounter_id="ENC001",
            diagnosed_date=date(2024, 1, 15),
        )

        lab = LabResult(
            test_name="hemoglobin",
            value="12.5",
            unit="g/dL",
            patient_mrn="MRN001",
            encounter_id="ENC001",
            collected_time=datetime(2024, 1, 15, 14, 30),
        )

        vital = VitalSign(
            patient_mrn="MRN001",
            encounter_id="ENC001",
            observation_time=datetime(2024, 1, 15, 12, 0),
            heart_rate=82,
        )

        transformer = FHIRTransformer()
        bundle = transformer.create_bundle(
            patients=[patient],
            encounters=[encounter],
            diagnoses=[diagnosis],
            labs=[lab],
            vitals=[vital],
        )

        # Should have 5 entries: Patient, Encounter, Condition, Lab Obs, Vital Obs
        assert len(bundle.entry) == 5

        resource_types = [entry.resource["resourceType"] for entry in bundle.entry]
        assert "Patient" in resource_types
        assert "Encounter" in resource_types
        assert "Condition" in resource_types
        assert resource_types.count("Observation") == 2  # Lab + Vital

    def test_bundle_json_serialization(self) -> None:
        """Test that bundle can be serialized to valid JSON."""
        patient = Patient(
            id="patient-007",
            mrn="MRN001",
            name=PersonName(given_name="John", family_name="Doe"),
            birth_date=date(1959, 3, 15),
            gender=Gender.MALE,
        )

        transformer = FHIRTransformer()
        bundle = transformer.create_bundle(patients=[patient])

        # Should serialize without error
        json_str = bundle.model_dump_json(by_alias=True, exclude_none=True)
        data = json.loads(json_str)

        assert data["resourceType"] == "Bundle"
        assert data["type"] == "collection"
        assert "entry" in data
        assert len(data["entry"]) == 1


class TestReferentialIntegrity:
    """Tests for referential integrity between resources."""

    def test_patient_encounter_references(self) -> None:
        """Test that encounter references patient correctly."""
        patient = Patient(
            id="patient-008",
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

        transformer = FHIRTransformer()
        patient_resource = transformer.transform_patient(patient)
        encounter_resource = transformer.transform_encounter(encounter)

        # Encounter should reference the same patient ID
        patient_id = patient_resource.id
        assert encounter_resource.subject.reference == f"Patient/{patient_id}"

    def test_condition_references_patient_and_encounter(self) -> None:
        """Test that condition references both patient and encounter."""
        diagnosis = Diagnosis(
            code="A41.9",
            description="Sepsis",
            type=DiagnosisType.FINAL,
            patient_mrn="MRN001",
            encounter_id="ENC001",
            diagnosed_date=date(2024, 1, 15),
        )

        transformer = FHIRTransformer()
        # Create patient and encounter first
        patient = Patient(
            id="patient-009",
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

        patient_resource = transformer.transform_patient(patient)
        encounter_resource = transformer.transform_encounter(encounter)
        condition_resource = transformer.transform_condition(diagnosis)

        # Should reference same patient and encounter
        assert condition_resource.subject.reference == f"Patient/{patient_resource.id}"
        assert condition_resource.encounter.reference == f"Encounter/{encounter_resource.id}"
