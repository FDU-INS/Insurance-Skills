"""Tests for MCP session management."""

import pytest

from patientsim.core.generator import PatientGenerator
from patientsim.mcp.session import PatientSession, SessionManager


@pytest.fixture
def generator():
    """Create a patient generator with fixed seed."""
    return PatientGenerator(seed=42)


@pytest.fixture
def patient(generator):
    """Generate a test patient."""
    return generator.generate_patient()


@pytest.fixture
def encounter(generator, patient):
    """Generate a test encounter."""
    return generator.generate_encounter(patient)


@pytest.fixture
def session_manager():
    """Create a fresh session manager."""
    return SessionManager()


class TestPatientSession:
    """Tests for PatientSession class."""

    def test_create_session_minimal(self, patient):
        """Test creating session with just a patient."""
        session = PatientSession(patient=patient)

        assert session.id is not None
        assert len(session.id) == 8
        assert session.patient == patient
        assert session.encounter is None
        assert session.diagnoses == []
        assert session.labs == []
        assert session.vitals == []
        assert session.medications == []
        assert session.procedures == []
        assert session.notes == []

    def test_create_session_complete(self, generator, patient, encounter):
        """Test creating session with all clinical data."""
        diagnoses = [generator.generate_diagnosis(patient, encounter)]
        labs = [generator.generate_lab_result(patient, encounter)]
        vitals = [generator.generate_vital_signs(patient, encounter)]
        medications = [generator.generate_medication(patient, encounter)]

        session = PatientSession(
            patient=patient,
            encounters=[encounter],
            diagnoses=diagnoses,
            labs=labs,
            vitals=vitals,
            medications=medications,
        )

        assert session.patient == patient
        assert session.encounter == encounter  # Legacy property
        assert len(session.encounters) == 1
        assert len(session.diagnoses) == 1
        assert len(session.labs) == 1
        assert len(session.vitals) == 1
        assert len(session.medications) == 1

    def test_to_summary_minimal(self, patient):
        """Test summary generation with minimal data."""
        session = PatientSession(patient=patient)
        summary = session.to_summary()

        assert "id" in summary
        assert "mrn" in summary
        assert "name" in summary
        assert "age" in summary
        assert "gender" in summary
        assert summary["mrn"] == patient.mrn
        assert summary["name"] == patient.full_name

    def test_to_summary_complete(self, generator, patient, encounter):
        """Test summary generation with complete data."""
        diagnoses = [generator.generate_diagnosis(patient, encounter)]
        labs = [generator.generate_lab_result(patient, encounter)]
        vitals = [generator.generate_vital_signs(patient, encounter)]

        session = PatientSession(
            patient=patient,
            encounters=[encounter],
            diagnoses=diagnoses,
            labs=labs,
            vitals=vitals,
        )

        summary = session.to_summary()

        assert "encounter" in summary
        assert "diagnoses" in summary
        assert "lab_count" in summary
        assert "vitals" in summary
        assert summary["lab_count"] == 1
        assert len(summary["diagnoses"]) == 1
        assert "provenance" in summary  # New: provenance in summary


class TestSessionManager:
    """Tests for SessionManager class."""

    def test_initial_state(self, session_manager):
        """Test session manager starts empty."""
        assert session_manager.count() == 0
        assert session_manager.list_all() == []
        assert session_manager.get_latest() is None

    def test_add_patient(self, session_manager, patient):
        """Test adding a patient to session."""
        session = session_manager.add_patient(patient)

        assert session is not None
        assert session.patient == patient
        assert session_manager.count() == 1

    def test_add_multiple_patients(self, session_manager, generator):
        """Test adding multiple patients."""
        patients = [generator.generate_patient() for _ in range(3)]

        for patient in patients:
            session_manager.add_patient(patient)

        assert session_manager.count() == 3

    def test_get_by_id(self, session_manager, patient):
        """Test retrieving patient by ID."""
        session = session_manager.add_patient(patient)

        retrieved = session_manager.get_by_id(session.id)

        assert retrieved is not None
        assert retrieved.id == session.id
        assert retrieved.patient == patient

    def test_get_by_id_not_found(self, session_manager):
        """Test getting non-existent patient."""
        result = session_manager.get_by_id("nonexistent")
        assert result is None

    def test_get_by_position(self, session_manager, generator):
        """Test retrieving patient by position."""
        patients = [generator.generate_patient() for _ in range(3)]

        for patient in patients:
            session_manager.add_patient(patient)

        # 1-indexed positions
        first = session_manager.get_by_position(1)
        second = session_manager.get_by_position(2)
        third = session_manager.get_by_position(3)

        assert first.patient == patients[0]
        assert second.patient == patients[1]
        assert third.patient == patients[2]

    def test_get_by_position_invalid(self, session_manager):
        """Test invalid positions return None."""
        assert session_manager.get_by_position(0) is None
        assert session_manager.get_by_position(99) is None

    def test_get_latest(self, session_manager, generator):
        """Test getting most recently added patient."""
        patients = [generator.generate_patient() for _ in range(3)]

        for patient in patients:
            session_manager.add_patient(patient)

        latest = session_manager.get_latest()

        assert latest is not None
        assert latest.patient == patients[-1]

    def test_list_all(self, session_manager, generator):
        """Test listing all patients."""
        patients = [generator.generate_patient() for _ in range(3)]

        for patient in patients:
            session_manager.add_patient(patient)

        all_sessions = session_manager.list_all()

        assert len(all_sessions) == 3
        assert all(isinstance(s, PatientSession) for s in all_sessions)

    def test_clear(self, session_manager, generator):
        """Test clearing all sessions."""
        patients = [generator.generate_patient() for _ in range(3)]

        for patient in patients:
            session_manager.add_patient(patient)

        assert session_manager.count() == 3

        session_manager.clear()

        assert session_manager.count() == 0
        assert session_manager.list_all() == []

    def test_update_patient(self, session_manager, patient):
        """Test updating a patient."""
        session = session_manager.add_patient(patient)

        # Update mrn (direct field on Patient model)
        modifications = {"mrn": "MRN-UPDATED"}
        updated = session_manager.update_patient(session.id, modifications)

        assert updated is not None
        assert updated.patient.mrn == "MRN-UPDATED"

    def test_update_patient_not_found(self, session_manager):
        """Test updating non-existent patient."""
        result = session_manager.update_patient("nonexistent", {"age": 50})
        assert result is None

    def test_get_by_mrn(self, session_manager, patient):
        """Test retrieving patient by MRN."""
        session = session_manager.add_patient(patient)
        retrieved = session_manager.get_by_mrn(patient.mrn)

        assert retrieved is not None
        assert retrieved.id == session.id
        assert retrieved.patient.mrn == patient.mrn

    def test_get_by_mrn_not_found(self, session_manager):
        """Test getting non-existent MRN."""
        result = session_manager.get_by_mrn("MRN-NONEXISTENT")
        assert result is None

    def test_get_workspace_summary(self, session_manager, generator):
        """Test workspace summary includes all counts."""
        patient = generator.generate_patient()
        encounter = generator.generate_encounter(patient)
        diagnoses = [generator.generate_diagnosis(patient, encounter)]

        session_manager.add_patient(
            patient,
            encounter=encounter,
            diagnoses=diagnoses,
        )

        summary = session_manager.get_workspace_summary()

        assert summary["patient_count"] == 1
        assert summary["encounter_count"] == 1
        assert summary["diagnosis_count"] == 1
        assert "provenance_summary" in summary


class TestPatientSessionProvenance:
    """Tests for provenance tracking in PatientSession."""

    def test_session_has_default_provenance(self, patient):
        """Test session has generated provenance by default."""
        from patientsim.core.state import SourceType

        session = PatientSession(patient=patient)

        assert session.provenance is not None
        assert session.provenance.source_type == SourceType.GENERATED

    def test_session_with_custom_provenance(self, patient):
        """Test session with custom provenance."""
        from patientsim.core.state import Provenance

        prov = Provenance.loaded(source_system="external-system")
        session = PatientSession(patient=patient, provenance=prov)

        assert session.provenance.source_type.value == "loaded"
        assert session.provenance.source_system == "external-system"

    def test_session_summary_includes_provenance(self, patient):
        """Test session summary includes provenance info."""
        session = PatientSession(patient=patient)
        summary = session.to_summary()

        assert "provenance" in summary
        assert "source_type" in summary["provenance"]
        assert "created_at" in summary["provenance"]

    def test_add_entity_with_provenance(self, generator, patient, encounter):
        """Test adding entities with individual provenance."""
        from patientsim.core.state import Provenance

        session = PatientSession(patient=patient)
        diagnosis = generator.generate_diagnosis(patient, encounter)

        prov = Provenance.derived(derived_from=["patient-001"])
        session.add_diagnosis(diagnosis, provenance=prov)

        assert len(session.diagnoses) == 1


class TestPatientSessionEntities:
    """Tests for enhanced entity support in PatientSession."""

    def test_session_with_multiple_encounters(self, generator, patient):
        """Test session with multiple encounters."""
        encounters = [generator.generate_encounter(patient) for _ in range(3)]
        session = PatientSession(patient=patient, encounters=encounters)

        assert len(session.encounters) == 3
        # Legacy property should return first
        assert session.encounter == encounters[0]

    def test_session_with_medications(self, generator, patient, encounter):
        """Test session with medications."""
        session = PatientSession(patient=patient)
        med = generator.generate_medication(patient, encounter)
        session.add_medication(med)

        assert len(session.medications) == 1
        assert session.medications[0] == med

    def test_session_with_multiple_vitals(self, generator, patient, encounter):
        """Test session with multiple vital sign readings."""
        vitals = [generator.generate_vital_signs(patient, encounter) for _ in range(3)]
        session = PatientSession(patient=patient, vitals=vitals)

        assert len(session.vitals) == 3

    def test_to_entities_with_provenance(self, generator, patient, encounter):
        """Test converting session to entities with provenance."""
        diagnoses = [generator.generate_diagnosis(patient, encounter)]
        labs = [generator.generate_lab_result(patient, encounter)]
        vitals = [generator.generate_vital_signs(patient, encounter)]

        session = PatientSession(
            patient=patient,
            encounters=[encounter],
            diagnoses=diagnoses,
            labs=labs,
            vitals=vitals,
        )

        entities = session.to_entities_with_provenance()

        assert "patients" in entities
        assert "encounters" in entities
        assert "diagnoses" in entities
        assert "lab_results" in entities
        assert "vital_signs" in entities

        assert len(entities["patients"]) == 1
        assert len(entities["encounters"]) == 1
        assert len(entities["diagnoses"]) == 1

        # Each entity should have provenance
        patient_entity = entities["patients"][0]
        assert patient_entity.provenance is not None

    def test_summary_with_medications_and_counts(self, generator, patient, encounter):
        """Test summary includes medication and count fields."""
        session = PatientSession(patient=patient)

        med = generator.generate_medication(patient, encounter)
        session.add_medication(med)

        for _ in range(3):
            session.add_lab(generator.generate_lab_result(patient, encounter))

        summary = session.to_summary()

        assert "medications" in summary
        assert len(summary["medications"]) == 1
        assert summary["lab_count"] == 3


class TestSessionManagerCohorts:
    """Tests for scenario save/load in SessionManager."""

    @pytest.fixture
    def temp_scenarios_dir(self, tmp_path):
        """Create temporary scenarios directory."""
        return tmp_path

    @pytest.fixture
    def session_manager(self, temp_scenarios_dir):
        """Create a session manager with temp directory."""
        return SessionManager(workspace_dir=temp_scenarios_dir)

    def test_save_cohort_empty_workspace(self, session_manager, temp_scenarios_dir):
        """Test saving empty workspace raises error context."""
        # Empty workspace should still work but with 0 patients
        scenario = session_manager.save_cohort(name="empty-test")
        assert scenario.get_entity_count("patients") == 0

    def test_save_and_load_cohort(self, session_manager, generator, temp_scenarios_dir):
        """Test saving and loading a scenario."""
        # Add some patients
        for _ in range(3):
            patient = generator.generate_patient()
            session_manager.add_patient(patient)

        # Save
        scenario = session_manager.save_cohort(
            name="test-cohort",
            description="Testing save/load",
            tags=["test"],
        )

        assert scenario.metadata.name == "test-cohort"
        assert scenario.get_entity_count("patients") == 3

        # Clear and verify empty
        session_manager.clear()
        assert session_manager.count() == 0

        # Load
        loaded_scenario, summary = session_manager.load_cohort(name="test-cohort")

        assert loaded_scenario.metadata.name == "test-cohort"
        assert summary["patients_loaded"] == 3
        assert session_manager.count() == 3

    def test_load_cohort_replace_mode(self, session_manager, generator, temp_scenarios_dir):
        """Test loading scenario replaces existing patients."""
        # Add initial patient
        patient1 = generator.generate_patient()
        session_manager.add_patient(patient1)

        # Save as scenario
        session_manager.save_cohort(name="scenario-a")

        # Add another patient
        patient2 = generator.generate_patient()
        session_manager.add_patient(patient2)
        assert session_manager.count() == 2

        # Load scenario in replace mode (default)
        session_manager.load_cohort(name="scenario-a", mode="replace")

        # Should only have 1 patient from scenario
        assert session_manager.count() == 1

    def test_load_cohort_merge_mode(self, session_manager, generator, temp_scenarios_dir):
        """Test loading scenario in merge mode."""
        # Create and save scenario with 2 patients
        for _ in range(2):
            session_manager.add_patient(generator.generate_patient())
        session_manager.save_cohort(name="scenario-merge")

        # Clear and add different patient
        session_manager.clear()
        session_manager.add_patient(generator.generate_patient())
        assert session_manager.count() == 1

        # Load in merge mode
        _, summary = session_manager.load_cohort(name="scenario-merge", mode="merge")

        # Should have 3 patients (1 existing + 2 from scenario)
        assert session_manager.count() == 3
        assert summary["patients_loaded"] == 2

    def test_list_cohorts(self, session_manager, generator, temp_scenarios_dir):
        """Test listing saved scenarios."""
        # Create multiple scenarios
        for _i, name in enumerate(["alpha", "beta", "gamma"]):
            session_manager.clear()
            session_manager.add_patient(generator.generate_patient())
            session_manager.save_cohort(name=name, tags=["test"])

        scenarios = session_manager.list_cohorts()

        assert len(scenarios) == 3
        names = [s["name"] for s in scenarios]
        assert "alpha" in names
        assert "beta" in names
        assert "gamma" in names

    def test_list_cohorts_with_search(self, session_manager, generator, temp_scenarios_dir):
        """Test filtering scenarios by search string."""
        session_manager.add_patient(generator.generate_patient())

        session_manager.save_cohort(name="diabetes-cohort")
        session_manager.save_cohort(name="cardiac-testing")

        results = session_manager.list_cohorts(search="diabetes")

        assert len(results) == 1
        assert results[0]["name"] == "diabetes-cohort"

    def test_list_cohorts_with_tags(self, session_manager, generator, temp_scenarios_dir):
        """Test filtering scenarios by tags."""
        session_manager.add_patient(generator.generate_patient())

        session_manager.save_cohort(name="s1", tags=["training", "diabetes"])
        session_manager.save_cohort(name="s2", tags=["training"])
        session_manager.save_cohort(name="s3", tags=["production"])

        results = session_manager.list_cohorts(tags=["training"])
        assert len(results) == 2

        results = session_manager.list_cohorts(tags=["training", "diabetes"])
        assert len(results) == 1
        assert results[0]["name"] == "s1"

    def test_delete_cohort(self, session_manager, generator, temp_scenarios_dir):
        """Test deleting a scenario."""
        session_manager.add_patient(generator.generate_patient())
        scenario = session_manager.save_cohort(name="to-delete")

        workspace_id = scenario.metadata.workspace_id

        # Verify it exists
        scenarios = session_manager.list_cohorts()
        assert len(scenarios) == 1

        # Delete
        result = session_manager.delete_cohort(workspace_id)

        assert result is not None
        assert result["name"] == "to-delete"

        # Verify deleted
        scenarios = session_manager.list_cohorts()
        assert len(scenarios) == 0

    def test_delete_nonexistent_scenario(self, session_manager, temp_scenarios_dir):
        """Test deleting non-existent scenario returns None."""
        result = session_manager.delete_cohort("nonexistent-id")
        assert result is None

    def test_scenario_preserves_provenance(self, session_manager, generator, temp_scenarios_dir):
        """Test that provenance is preserved through save/load cycle."""
        from patientsim.core.state import Provenance

        patient = generator.generate_patient()
        prov = Provenance.generated(skill_used="diabetes-management")

        session_manager.add_patient(patient, provenance=prov)
        session_manager.save_cohort(name="provenance-test")

        # Clear and reload
        session_manager.clear()
        session_manager.load_cohort(name="provenance-test")

        # After load, provenance is updated to "loaded"
        loaded_session = session_manager.get_latest()
        assert loaded_session.provenance.source_type.value == "loaded"

    def test_save_specific_patients(self, session_manager, generator, temp_scenarios_dir):
        """Test saving only specific patients."""
        patients = [generator.generate_patient() for _ in range(5)]
        sessions = [session_manager.add_patient(p) for p in patients]

        # Save only first 2
        patient_ids = [sessions[0].id, sessions[1].id]
        scenario = session_manager.save_cohort(name="subset", patient_ids=patient_ids)

        assert scenario.get_entity_count("patients") == 2
