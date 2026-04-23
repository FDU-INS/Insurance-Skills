"""Tests for MCP response formatters."""

import pytest

from patientsim.core.generator import PatientGenerator
from patientsim.mcp.formatters import (
    format_cohort_summary,
    format_error,
    format_patient_summary,
    format_skill_details,
    format_skill_list,
    format_success,
)
from patientsim.mcp.session import PatientSession


@pytest.fixture
def generator():
    """Create a patient generator with fixed seed."""
    return PatientGenerator(seed=42)


@pytest.fixture
def patient_session(generator):
    """Create a complete patient session."""
    patient = generator.generate_patient()
    encounter = generator.generate_encounter(patient)
    diagnoses = [generator.generate_diagnosis(patient, encounter)]
    labs = [generator.generate_lab_result(patient, encounter)]
    vitals = generator.generate_vital_signs(patient, encounter)

    return PatientSession(
        patient=patient,
        encounters=[encounter],
        diagnoses=diagnoses,
        labs=labs,
        vitals=[vitals],
    )


class TestFormatPatientSummary:
    """Tests for patient summary formatting."""

    def test_format_minimal_patient(self, generator):
        """Test formatting patient with minimal data."""
        patient = generator.generate_patient()
        session = PatientSession(patient=patient)

        result = format_patient_summary(session)

        assert "##" in result  # Markdown header
        assert patient.full_name in result
        assert session.id in result
        assert patient.mrn in result
        assert str(patient.age) in result

    def test_format_complete_patient(self, patient_session):
        """Test formatting patient with all data."""
        result = format_patient_summary(patient_session)

        # Check all sections are present
        assert "Patient:" in result
        assert "Encounter" in result
        assert "Diagnoses" in result
        assert "Vital Signs" in result
        assert "Lab Results" in result

        # Check vital signs details
        assert "Heart Rate" in result
        assert "Blood Pressure" in result
        assert "Temperature" in result

    def test_format_includes_diagnosis_details(self, patient_session):
        """Test diagnosis details are included."""
        result = format_patient_summary(patient_session)

        # Should include ICD-10 codes
        assert "ICD-10:" in result
        assert patient_session.diagnoses[0].description in result


class TestFormatCohortSummary:
    """Tests for cohort summary formatting."""

    def test_format_empty_cohort(self):
        """Test formatting empty cohort."""
        result = format_cohort_summary([])

        assert "No patients generated" in result

    def test_format_single_patient_cohort(self, generator):
        """Test formatting cohort with one patient."""
        patient = generator.generate_patient()
        session = PatientSession(patient=patient)

        result = format_cohort_summary([session])

        assert "1 Patient" in result or "1 patients" in result.lower()
        assert patient.full_name in result

    def test_format_multiple_patients(self, generator):
        """Test formatting cohort with multiple patients."""
        sessions = []
        for _ in range(5):
            patient = generator.generate_patient()
            sessions.append(PatientSession(patient=patient))

        result = format_cohort_summary(sessions)

        assert "5 Patients" in result or "5 patients" in result.lower()
        assert "Demographics" in result
        assert "Age Range" in result

    def test_format_with_scenario(self, generator):
        """Test formatting cohort with scenario name."""
        sessions = []
        for _ in range(3):
            patient = generator.generate_patient()
            sessions.append(PatientSession(patient=patient))

        result = format_cohort_summary(sessions, scenario="icu_sepsis")

        assert "icu_sepsis" in result

    def test_format_shows_demographics(self, generator):
        """Test cohort summary includes demographics."""
        sessions = []
        for _ in range(10):
            patient = generator.generate_patient()
            sessions.append(PatientSession(patient=patient))

        result = format_cohort_summary(sessions)

        # Should show gender distribution
        assert "Male" in result or "Female" in result
        # Should show age statistics
        assert "Age Range" in result


class TestFormatScenarios:
    """Tests for scenario formatting."""

    def test_format_empty_scenario_list(self):
        """Test formatting empty scenario list."""
        result = format_skill_list({})

        assert "No skills available" in result

    def test_format_skill_list(self):
        """Test formatting scenario list."""
        scenarios = {
            "icu_sepsis": {
                "description": "ICU patient with sepsis",
                "category": "critical_care",
            },
            "ed_chest_pain": {
                "description": "Emergency department chest pain",
                "category": "emergency",
            },
        }

        result = format_skill_list(scenarios)

        assert "Available Skills" in result
        assert "icu_sepsis" in result
        assert "ed_chest_pain" in result
        assert "ICU patient with sepsis" in result

    def test_format_skill_details(self):
        """Test formatting scenario details."""
        metadata = {
            "description": "ICU patient with sepsis",
            "parameters": {
                "age_range": {
                    "type": "tuple",
                    "description": "Age range for patient",
                },
            },
            "example": "generate_patient(scenario='icu_sepsis')",
            "category": "critical_care",
        }

        result = format_skill_details("icu_sepsis", metadata)

        assert "Skill: icu_sepsis" in result
        assert "ICU patient with sepsis" in result
        assert "Parameters" in result
        assert "age_range" in result
        assert "Example Usage" in result


class TestFormatMessages:
    """Tests for error and success message formatting."""

    def test_format_error_minimal(self):
        """Test formatting error with just message."""
        result = format_error("Something went wrong")

        assert "Error" in result
        assert "Something went wrong" in result

    def test_format_error_with_suggestion(self):
        """Test formatting error with suggestion."""
        result = format_error("Invalid age range", "Try using age_range=[18, 85] instead")

        assert "Error" in result
        assert "Invalid age range" in result
        assert "Suggestion" in result
        assert "Try using" in result

    def test_format_success_minimal(self):
        """Test formatting success with just message."""
        result = format_success("Patient generated successfully")

        assert "Patient generated successfully" in result

    def test_format_success_with_next_steps(self):
        """Test formatting success with next steps."""
        next_steps = [
            "Export to FHIR",
            "View patient details",
        ]

        result = format_success("Patient generated successfully", next_steps)

        assert "Patient generated successfully" in result
        assert "Next steps" in result
        assert "Export to FHIR" in result
        assert "View patient details" in result
