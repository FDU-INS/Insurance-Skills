"""
Integration tests for Auto-Persist Phase 2 features.

Tests full workflows across multiple entity types, large batches,
and all export formats.
"""

import json
import tempfile
import time
from pathlib import Path
from uuid import uuid4

import pytest

from healthsim.db import DatabaseConnection
from healthsim.state.auto_persist import AutoPersistService

# Check for pyarrow availability
try:
    import pyarrow
    PYARROW_AVAILABLE = True
except ImportError:
    PYARROW_AVAILABLE = False

requires_pyarrow = pytest.mark.skipif(
    not PYARROW_AVAILABLE, 
    reason="pyarrow not installed"
)


@pytest.fixture
def db_connection():
    """Create a temporary database connection."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "integration_test.duckdb"
        db_conn = DatabaseConnection(db_path)
        conn = db_conn.connect()
        yield conn
        db_conn.close()


@pytest.fixture
def service(db_connection):
    """Create AutoPersistService instance."""
    return AutoPersistService(db_connection)


@requires_pyarrow
class TestParquetExport:
    """Test Parquet export functionality."""

    def test_parquet_export_creates_valid_files(self, service):
        """Verify Parquet export creates readable files."""
        # Create test data
        patients = [
            {
                "id": str(uuid4()),
                "given_name": f"Patient{i}",
                "family_name": "Test",
                "gender": "male" if i % 2 == 0 else "female",
                "birth_date": f"198{i % 10}-01-15",
            }
            for i in range(10)
        ]

        result = service.persist_entities(
            entities=patients, entity_type="patient", cohort_name="parquet-test"
        )

        with tempfile.TemporaryDirectory() as export_dir:
            exp = service.export_cohort(result.cohort_id, "parquet", export_dir)

            # Verify export succeeded
            assert Path(exp.file_path).exists()
            assert exp.total_entities > 0

            # Verify parquet files created
            parquet_files = list(Path(exp.file_path).glob("*.parquet"))
            assert len(parquet_files) > 0
            assert "patients.parquet" in [f.name for f in parquet_files]

            # Verify files are readable with pyarrow
            try:
                import pyarrow.parquet as pq

                for pf in parquet_files:
                    table = pq.read_table(pf)
                    assert table.num_rows > 0
            except ImportError:
                pytest.skip("pyarrow not installed")


class TestPerformance:
    """Performance tests with large batches."""

    def test_persist_1000_entities_under_5_seconds(self, service):
        """Persist 1000 patients should complete in under 5 seconds."""
        patients = [
            {
                "id": str(uuid4()),
                "given_name": f"Patient{i}",
                "family_name": f"Family{i}",
                "gender": "male" if i % 2 == 0 else "female",
                "birth_date": f"{1950 + (i % 50)}-{(i % 12) + 1:02d}-{(i % 28) + 1:02d}",
            }
            for i in range(1000)
        ]

        start = time.time()
        result = service.persist_entities(
            entities=patients, entity_type="patient", cohort_name="perf-test"
        )
        elapsed = time.time() - start

        assert result.entities_persisted == 1000
        assert elapsed < 5.0, f"Persist took {elapsed:.2f}s, expected < 5s"

    def test_clone_1000_entities_under_5_seconds(self, service):
        """Clone 1000 patients should complete in under 5 seconds."""
        patients = [
            {
                "id": str(uuid4()),
                "given_name": f"Patient{i}",
                "family_name": f"Family{i}",
                "gender": "male",
                "birth_date": "1980-01-15",
            }
            for i in range(1000)
        ]

        result = service.persist_entities(
            entities=patients, entity_type="patient", cohort_name="clone-perf-test"
        )

        start = time.time()
        clone = service.clone_cohort(result.cohort_id, "cloned-1000")
        elapsed = time.time() - start

        assert clone.total_entities == 1000
        assert elapsed < 5.0, f"Clone took {elapsed:.2f}s, expected < 5s"

    @requires_pyarrow
    def test_export_1000_entities_all_formats(self, service):
        """Export 1000 patients in all formats should be fast."""
        patients = [
            {
                "id": str(uuid4()),
                "given_name": f"Patient{i}",
                "family_name": f"Family{i}",
                "gender": "male",
                "birth_date": "1980-01-15",
            }
            for i in range(1000)
        ]

        result = service.persist_entities(
            entities=patients, entity_type="patient", cohort_name="export-perf-test"
        )

        with tempfile.TemporaryDirectory() as export_dir:
            # JSON export
            start = time.time()
            exp_json = service.export_cohort(result.cohort_id, "json", export_dir)
            json_time = time.time() - start
            assert Path(exp_json.file_path).exists()
            assert json_time < 2.0, f"JSON export took {json_time:.2f}s"

            # CSV export
            start = time.time()
            exp_csv = service.export_cohort(
                result.cohort_id, "csv", f"{export_dir}/csv"
            )
            csv_time = time.time() - start
            assert Path(exp_csv.file_path).exists()
            assert csv_time < 2.0, f"CSV export took {csv_time:.2f}s"

            # Parquet export
            start = time.time()
            exp_pq = service.export_cohort(
                result.cohort_id, "parquet", f"{export_dir}/pq"
            )
            pq_time = time.time() - start
            assert Path(exp_pq.file_path).exists()
            assert pq_time < 2.0, f"Parquet export took {pq_time:.2f}s"


class TestCrossProductIntegration:
    """Test cohorts with multiple entity types."""

    def test_cohort_with_patients_and_encounters(self, service):
        """Create cohort with patients and encounters, then clone and merge."""
        # Create patients with MRNs
        mrns = [f"MRN-{i:04d}" for i in range(5)]
        patients = [
            {
                "id": str(uuid4()),
                "mrn": mrn,
                "given_name": f"Patient{i}",
                "family_name": "Test",
                "gender": "male",
                "birth_date": "1980-01-15",
            }
            for i, mrn in enumerate(mrns)
        ]

        result = service.persist_entities(
            entities=patients,
            entity_type="patient",
            cohort_name="multi-entity-test",
            tags=["integration-test"],
        )
        assert result.entities_persisted == 5

        # Add encounters for each patient
        encounters = []
        for mrn in mrns:
            for j in range(3):
                encounters.append(
                    {
                        "encounter_id": str(uuid4()),
                        "patient_mrn": mrn,
                        "class_code": "AMB",
                        "status": "finished",
                        "admission_time": f"2024-0{j+1}-15T09:00:00",
                        "discharge_time": f"2024-0{j+1}-15T10:00:00",
                    }
                )

        result2 = service.persist_entities(
            entities=encounters, entity_type="encounter", cohort_id=result.cohort_id
        )
        assert result2.entities_persisted == 15

        # Verify summary
        summary = service.get_cohort_summary(result.cohort_id)
        assert summary.entity_counts == {"patients": 5, "encounters": 15}

        # Clone and verify IDs are different
        clone = service.clone_cohort(result.cohort_id, "multi-entity-clone")
        assert clone.total_entities == 20

        orig_patients = service.query_cohort(result.cohort_id, "SELECT id FROM patients")
        clone_patients = service.query_cohort(clone.new_cohort_id, "SELECT id FROM patients")
        
        orig_ids = {r["id"] for r in orig_patients.results}
        clone_ids = {r["id"] for r in clone_patients.results}
        assert orig_ids != clone_ids, "Cloned IDs should be different"

    def test_merge_cohorts_with_different_entity_types(self, service):
        """Merge cohorts where one has encounters and one doesn't."""
        # First cohort: patients + encounters
        patients1 = [
            {
                "id": str(uuid4()),
                "mrn": f"MRN-A{i:03d}",
                "given_name": f"PatientA{i}",
                "family_name": "Test",
                "gender": "male",
                "birth_date": "1980-01-15",
            }
            for i in range(3)
        ]
        result1 = service.persist_entities(
            entities=patients1, entity_type="patient", cohort_name="cohort-a"
        )

        encounters = [
            {
                "encounter_id": str(uuid4()),
                "patient_mrn": f"MRN-A{i:03d}",
                "class_code": "AMB",
                "status": "finished",
                "admission_time": "2024-01-15T09:00:00",
            }
            for i in range(3)
        ]
        service.persist_entities(
            entities=encounters, entity_type="encounter", cohort_id=result1.cohort_id
        )

        # Second cohort: patients only
        patients2 = [
            {
                "id": str(uuid4()),
                "mrn": f"MRN-B{i:03d}",
                "given_name": f"PatientB{i}",
                "family_name": "Test",
                "gender": "female",
                "birth_date": "1990-06-20",
            }
            for i in range(2)
        ]
        result2 = service.persist_entities(
            entities=patients2, entity_type="patient", cohort_name="cohort-b"
        )

        # Merge
        merged = service.merge_cohorts(
            [result1.cohort_id, result2.cohort_id], "merged-cohort"
        )

        # Verify counts
        assert merged.entities_merged["patients"] == 5  # 3 + 2
        assert merged.entities_merged["encounters"] == 3  # only from cohort-a

    def test_export_multi_entity_cohort(self, service):
        """Export cohort with multiple entity types."""
        # Create patients
        patients = [
            {
                "id": str(uuid4()),
                "mrn": f"MRN-{i:04d}",
                "given_name": f"Patient{i}",
                "family_name": "Test",
                "gender": "male",
                "birth_date": "1980-01-15",
            }
            for i in range(3)
        ]
        result = service.persist_entities(
            entities=patients, entity_type="patient", cohort_name="export-multi-test"
        )

        # Add encounters
        encounters = [
            {
                "encounter_id": str(uuid4()),
                "patient_mrn": f"MRN-{i:04d}",
                "class_code": "AMB",
                "status": "finished",
                "admission_time": "2024-01-15T09:00:00",
            }
            for i in range(3)
        ]
        service.persist_entities(
            entities=encounters, entity_type="encounter", cohort_id=result.cohort_id
        )

        with tempfile.TemporaryDirectory() as export_dir:
            # JSON export
            exp = service.export_cohort(result.cohort_id, "json", export_dir)
            with open(exp.file_path) as f:
                data = json.load(f)

            entities = data.get("entities", {})
            assert "patients" in entities
            assert "encounters" in entities
            assert len(entities["patients"]) == 3
            assert len(entities["encounters"]) == 3

            # CSV export
            exp_csv = service.export_cohort(
                result.cohort_id, "csv", f"{export_dir}/csv"
            )
            csv_files = list(Path(exp_csv.file_path).glob("*.csv"))
            csv_names = [f.name for f in csv_files]
            assert "patients.csv" in csv_names
            assert "encounters.csv" in csv_names


class TestFullWorkflow:
    """End-to-end workflow tests."""

    def test_generate_persist_tag_clone_merge_export(self, service):
        """Complete workflow: generate -> persist -> tag -> clone -> merge -> export."""
        # Step 1: Generate and persist initial patients
        patients = [
            {
                "id": str(uuid4()),
                "given_name": f"Patient{i}",
                "family_name": "Original",
                "gender": "male",
                "birth_date": "1980-01-15",
            }
            for i in range(5)
        ]
        result = service.persist_entities(
            entities=patients, entity_type="patient", cohort_name="workflow-test"
        )
        cohort_id = result.cohort_id
        assert result.entities_persisted == 5

        # Step 2: Add tags
        service.add_tag(cohort_id, "diabetes-cohort")
        service.add_tag(cohort_id, "2024-study")
        tags = service.get_tags(cohort_id)
        assert "diabetes-cohort" in tags
        assert "2024-study" in tags

        # Step 3: Clone for A/B testing
        clone_a = service.clone_cohort(cohort_id, "control-group")
        clone_b = service.clone_cohort(cohort_id, "treatment-group")
        service.add_tag(clone_a.new_cohort_id, "control")
        service.add_tag(clone_b.new_cohort_id, "treatment")

        # Step 4: Verify clones are independent
        control_count = service.query_cohort(
            clone_a.new_cohort_id, "SELECT COUNT(*) as cnt FROM patients"
        )
        treatment_count = service.query_cohort(
            clone_b.new_cohort_id, "SELECT COUNT(*) as cnt FROM patients"
        )
        assert control_count.results[0]["cnt"] == 5
        assert treatment_count.results[0]["cnt"] == 5

        # Step 5: Create additional cohort
        more_patients = [
            {
                "id": str(uuid4()),
                "given_name": f"NewPatient{i}",
                "family_name": "Additional",
                "gender": "female",
                "birth_date": "1990-06-20",
            }
            for i in range(3)
        ]
        additional = service.persist_entities(
            entities=more_patients,
            entity_type="patient",
            cohort_name="additional-cohort",
        )

        # Step 6: Merge cohorts
        merged = service.merge_cohorts(
            [clone_a.new_cohort_id, additional.cohort_id], "combined-study"
        )
        assert merged.total_entities == 8  # 5 + 3

        # Step 7: Export final dataset
        with tempfile.TemporaryDirectory() as export_dir:
            exp = service.export_cohort(
                merged.target_cohort_id, "json", export_dir
            )
            assert Path(exp.file_path).exists()

            with open(exp.file_path) as f:
                data = json.load(f)
            assert len(data["entities"]["patients"]) == 8

        # Verify tag filtering works
        diabetes_cohorts = service.cohorts_by_tag("diabetes-cohort")
        cohort_ids = [s.cohort_id for s in diabetes_cohorts]
        assert cohort_id in cohort_ids
