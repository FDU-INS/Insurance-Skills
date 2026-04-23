"""Tests for FHIR R4 format transformer and bulk exporter.

Tests cover:
- FHIRTransformer resource transformations
- FHIRBulkExporter NDJSON generation
- BulkExportManifest structure
- ExportResult data class
- Streaming and file export
"""

import json
from datetime import date, datetime

import pytest

from patientsim.formats.fhir import (
    BulkExportManifest,
    ExportResult,
    FHIRBulkExporter,
    FHIRTransformer,
)


class TestBulkExportManifest:
    """Tests for BulkExportManifest dataclass."""

    def test_manifest_creation(self):
        """BulkExportManifest should create with required fields."""
        manifest = BulkExportManifest(transactionTime="2024-01-15T10:30:00Z")
        assert manifest.transactionTime == "2024-01-15T10:30:00Z"
        assert manifest.request == "https://healthsim.local/$export"
        assert manifest.requiresAccessToken is False
        assert manifest.output == []
        assert manifest.error == []

    def test_manifest_to_dict(self):
        """to_dict should return proper dictionary."""
        manifest = BulkExportManifest(
            transactionTime="2024-01-15T10:30:00Z",
            output=[{"type": "Patient", "url": "Patient.ndjson", "count": 10}],
        )
        result = manifest.to_dict()

        assert result["transactionTime"] == "2024-01-15T10:30:00Z"
        assert len(result["output"]) == 1
        assert result["output"][0]["type"] == "Patient"
        assert result["output"][0]["count"] == 10

    def test_manifest_with_errors(self):
        """Manifest should support error entries."""
        manifest = BulkExportManifest(
            transactionTime="2024-01-15T10:30:00Z",
            error=[{"type": "OperationOutcome", "url": "error.ndjson"}],
        )
        assert len(manifest.error) == 1


class TestExportResult:
    """Tests for ExportResult dataclass."""

    def test_export_result_creation(self, tmp_path):
        """ExportResult should capture export metadata."""
        manifest = BulkExportManifest(transactionTime="2024-01-15T10:30:00Z")
        result = ExportResult(
            output_dir=tmp_path,
            manifest=manifest,
            resource_counts={"Patient": 5, "Observation": 10},
            total_resources=15,
            files_created=[tmp_path / "Patient.ndjson"],
        )

        assert result.output_dir == tmp_path
        assert result.total_resources == 15
        assert result.resource_counts["Patient"] == 5
        assert len(result.files_created) == 1


class TestFHIRTransformer:
    """Tests for FHIRTransformer class."""

    @pytest.fixture
    def transformer(self):
        """Create a transformer instance."""
        return FHIRTransformer()

    @pytest.fixture
    def sample_patient(self):
        """Create a sample Patient for testing."""
        # Import here to avoid issues if patientsim.core is not available
        try:
            from healthsim.person import Gender, PersonName

            from patientsim.core.models import Patient

            return Patient(
                id="P001",
                mrn="MRN12345",
                name=PersonName(given_name="John", family_name="Doe"),
                gender=Gender.MALE,
                birth_date=date(1980, 5, 15),
                deceased=False,
            )
        except ImportError:
            pytest.skip("patientsim.core.models not available")

    @pytest.fixture
    def sample_encounter(self):
        """Create a sample Encounter for testing."""
        try:
            from patientsim.core.models import Encounter

            return Encounter(
                encounter_id="E001",
                patient_mrn="MRN12345",
                class_code="I",
                status="finished",
                admission_time=datetime(2024, 1, 10, 8, 0, 0),
                discharge_time=datetime(2024, 1, 12, 14, 0, 0),
            )
        except ImportError:
            pytest.skip("patientsim.core.models not available")

    @pytest.fixture
    def sample_diagnosis(self):
        """Create a sample Diagnosis for testing."""
        try:
            from patientsim.core.models import Diagnosis

            return Diagnosis(
                patient_mrn="MRN12345",
                code="E11.9",
                description="Type 2 diabetes mellitus without complications",
                diagnosed_date=date(2024, 1, 10),
            )
        except ImportError:
            pytest.skip("patientsim.core.models not available")

    def test_transform_patient_creates_resource(self, transformer, sample_patient):
        """transform_patient should create valid FHIR Patient."""
        resource = transformer.transform_patient(sample_patient)

        assert resource.resourceType == "Patient"
        assert resource.id is not None
        assert resource.gender == "male"
        assert resource.birthDate == "1980-05-15"
        assert len(resource.name) == 1
        assert resource.name[0].family == "Doe"
        assert "John" in resource.name[0].given

    def test_transform_patient_identifier(self, transformer, sample_patient):
        """transform_patient should include MRN identifier."""
        resource = transformer.transform_patient(sample_patient)

        assert len(resource.identifier) == 1
        assert resource.identifier[0].value == "MRN12345"

    def test_transform_encounter_creates_resource(self, transformer, sample_encounter):
        """transform_encounter should create valid FHIR Encounter."""
        resource = transformer.transform_encounter(sample_encounter)

        assert resource.resourceType == "Encounter"
        assert resource.id is not None
        assert resource.status == "finished"
        assert resource.subject is not None

    def test_transform_condition_creates_resource(self, transformer, sample_diagnosis):
        """transform_condition should create valid FHIR Condition."""
        resource = transformer.transform_condition(sample_diagnosis)

        assert resource.resourceType == "Condition"
        assert resource.id is not None
        assert resource.code is not None
        assert resource.subject is not None

    def test_create_bundle_type(self, transformer, sample_patient):
        """create_bundle should create bundle with correct type."""
        bundle = transformer.create_bundle(patients=[sample_patient])

        assert bundle.resourceType == "Bundle"
        assert bundle.type == "collection"
        assert bundle.id is not None

    def test_create_bundle_entries(self, transformer, sample_patient):
        """create_bundle should include all resources as entries."""
        bundle = transformer.create_bundle(patients=[sample_patient])

        assert len(bundle.entry) == 1
        assert bundle.entry[0].resource["resourceType"] == "Patient"

    def test_resource_id_consistency(self, transformer, sample_patient):
        """Same source ID should produce same FHIR resource ID."""
        resource1 = transformer.transform_patient(sample_patient)
        resource2 = transformer.transform_patient(sample_patient)

        assert resource1.id == resource2.id


class TestFHIRBulkExporter:
    """Tests for FHIRBulkExporter class."""

    @pytest.fixture
    def exporter(self):
        """Create an exporter instance."""
        return FHIRBulkExporter()

    @pytest.fixture
    def compressed_exporter(self):
        """Create a compressed exporter instance."""
        return FHIRBulkExporter(compress=True)

    @pytest.fixture
    def sample_patients(self):
        """Create sample patients for testing."""
        try:
            from healthsim.person import Gender, PersonName

            from patientsim.core.models import Patient

            return [
                Patient(
                    id=f"P00{i}",
                    mrn=f"MRN{i:05d}",
                    name=PersonName(given_name=f"Patient{i}", family_name="Test"),
                    gender=Gender.MALE if i % 2 == 0 else Gender.FEMALE,
                    birth_date=date(1980 + i, 1, 1),
                    deceased=False,
                )
                for i in range(1, 4)
            ]
        except ImportError:
            pytest.skip("patientsim.core.models not available")

    def test_export_patients_creates_file(self, exporter, sample_patients, tmp_path):
        """export_patients should create NDJSON file."""
        output_file = tmp_path / "Patient.ndjson"
        count = exporter.export_patients(sample_patients, output_file)

        assert count == 3
        assert output_file.exists()

    def test_export_patients_ndjson_format(self, exporter, sample_patients, tmp_path):
        """Output should be valid NDJSON (one JSON per line)."""
        output_file = tmp_path / "Patient.ndjson"
        exporter.export_patients(sample_patients, output_file)

        with open(output_file) as f:
            lines = f.readlines()

        assert len(lines) == 3
        for line in lines:
            resource = json.loads(line)
            assert resource["resourceType"] == "Patient"
            assert "id" in resource

    def test_export_to_directory_creates_files(self, exporter, sample_patients, tmp_path):
        """export_to_directory should create all resource files."""
        result = exporter.export_to_directory(
            output_dir=tmp_path,
            patients=sample_patients,
        )

        assert result.total_resources == 3
        assert (tmp_path / "Patient.ndjson").exists()
        assert (tmp_path / "manifest.json").exists()

    def test_export_to_directory_manifest(self, exporter, sample_patients, tmp_path):
        """Manifest should contain correct metadata."""
        exporter.export_to_directory(
            output_dir=tmp_path,
            patients=sample_patients,
        )

        # Read manifest
        with open(tmp_path / "manifest.json") as f:
            manifest = json.load(f)

        assert "transactionTime" in manifest
        assert len(manifest["output"]) == 1
        assert manifest["output"][0]["type"] == "Patient"
        assert manifest["output"][0]["count"] == 3

    def test_export_no_manifest(self, exporter, sample_patients, tmp_path):
        """export_to_directory should support skipping manifest."""
        exporter.export_to_directory(
            output_dir=tmp_path,
            patients=sample_patients,
            create_manifest=False,
        )

        assert not (tmp_path / "manifest.json").exists()

    def test_stream_resources_patients(self, exporter, sample_patients):
        """stream_resources should yield NDJSON lines."""
        lines = list(exporter.stream_resources("Patient", patients=sample_patients))

        assert len(lines) == 3
        for line in lines:
            assert line.endswith("\n")
            resource = json.loads(line)
            assert resource["resourceType"] == "Patient"

    def test_to_ndjson_string(self, exporter, sample_patients):
        """to_ndjson_string should return dict of NDJSON strings."""
        result = exporter.to_ndjson_string(patients=sample_patients)

        assert "Patient" in result
        lines = result["Patient"].strip().split("\n")
        assert len(lines) == 3

    def test_compressed_export(self, compressed_exporter, sample_patients, tmp_path):
        """Compressed exporter should create .gz files."""
        output_file = tmp_path / "Patient.ndjson"
        compressed_exporter.export_patients(sample_patients, output_file)

        # Should create .ndjson.gz file
        assert (tmp_path / "Patient.ndjson.gz").exists()

    def test_resource_files_mapping(self, exporter):
        """RESOURCE_FILES should map all supported types."""
        assert "Patient" in exporter.RESOURCE_FILES
        assert "Encounter" in exporter.RESOURCE_FILES
        assert "Condition" in exporter.RESOURCE_FILES
        assert "Observation" in exporter.RESOURCE_FILES


class TestFHIRExporterIntegration:
    """Integration tests for complete export workflows."""

    @pytest.fixture
    def full_dataset(self):
        """Create a full dataset with all resource types."""
        try:
            from healthsim.person import Gender, PersonName

            from patientsim.core.models import (
                Diagnosis,
                Encounter,
                Patient,
                VitalSign,
            )

            patient = Patient(
                id="P001",
                mrn="MRN12345",
                name=PersonName(given_name="Jane", family_name="Smith"),
                gender=Gender.FEMALE,
                birth_date=date(1975, 3, 20),
                deceased=False,
            )

            encounter = Encounter(
                encounter_id="E001",
                patient_mrn="MRN12345",
                class_code="I",
                status="finished",
                admission_time=datetime(2024, 1, 10, 8, 0, 0),
                discharge_time=datetime(2024, 1, 12, 14, 0, 0),
            )

            diagnosis = Diagnosis(
                patient_mrn="MRN12345",
                code="I10",
                description="Essential hypertension",
                diagnosed_date=date(2024, 1, 10),
                encounter_id="E001",
            )

            vital = VitalSign(
                patient_mrn="MRN12345",
                encounter_id="E001",
                observation_time=datetime(2024, 1, 10, 9, 0, 0),
                temperature=98.6,
                heart_rate=72,
                systolic_bp=140,
                diastolic_bp=90,
                spo2=98,
            )

            return {
                "patients": [patient],
                "encounters": [encounter],
                "diagnoses": [diagnosis],
                "vitals": [vital],
            }
        except ImportError:
            pytest.skip("patientsim.core.models not available")

    def test_full_export_workflow(self, full_dataset, tmp_path):
        """Complete export should create all expected files."""
        exporter = FHIRBulkExporter()
        exporter.export_to_directory(
            output_dir=tmp_path,
            **full_dataset,
        )

        assert (tmp_path / "Patient.ndjson").exists()
        assert (tmp_path / "Encounter.ndjson").exists()
        assert (tmp_path / "Condition.ndjson").exists()
        assert (tmp_path / "Observation.ndjson").exists()
        assert (tmp_path / "manifest.json").exists()

    def test_full_export_resource_counts(self, full_dataset, tmp_path):
        """Export result should have correct resource counts."""
        exporter = FHIRBulkExporter()
        result = exporter.export_to_directory(
            output_dir=tmp_path,
            **full_dataset,
        )

        assert result.resource_counts["Patient"] == 1
        assert result.resource_counts["Encounter"] == 1
        assert result.resource_counts["Condition"] == 1
        # Vitals can produce multiple observations (one per measurement)
        assert result.resource_counts["Observation"] > 0

    def test_bundle_and_ndjson_consistency(self, full_dataset, tmp_path):
        """Bundle and NDJSON exports should contain same data."""
        transformer = FHIRTransformer()
        exporter = FHIRBulkExporter()

        # Create bundle
        bundle = transformer.create_bundle(
            patients=full_dataset["patients"],
            encounters=full_dataset["encounters"],
            diagnoses=full_dataset["diagnoses"],
        )

        # Export NDJSON
        ndjson = exporter.to_ndjson_string(
            patients=full_dataset["patients"],
            encounters=full_dataset["encounters"],
            diagnoses=full_dataset["diagnoses"],
        )

        # Count resources in bundle
        bundle_patient_count = sum(
            1 for e in bundle.entry if e.resource.get("resourceType") == "Patient"
        )

        # Count resources in NDJSON
        ndjson_patient_count = len(ndjson.get("Patient", "").strip().split("\n"))
        if ndjson.get("Patient", "").strip() == "":
            ndjson_patient_count = 0

        assert bundle_patient_count == ndjson_patient_count
