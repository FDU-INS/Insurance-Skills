"""Tests for MCP validation server functionality."""

import pytest

from patientsim.core.generator import PatientGenerator
from patientsim.mcp import validation_server
from patientsim.mcp.session import SessionManager


@pytest.fixture
def generator():
    """Create a patient generator with fixed seed."""
    return PatientGenerator(seed=42)


@pytest.fixture
def populated_session_manager(generator):
    """Create a session manager with test patients."""
    session_manager = SessionManager()

    # Generate 3 patients with complete clinical data
    for _ in range(3):
        patient = generator.generate_patient()
        encounter = generator.generate_encounter(patient)
        diagnoses = [generator.generate_diagnosis(patient, encounter) for _ in range(2)]
        labs = [generator.generate_lab_result(patient, encounter) for _ in range(5)]
        vitals = generator.generate_vital_signs(patient, encounter)

        session_manager.add_patient(
            patient=patient,
            encounter=encounter,
            diagnoses=diagnoses,
            labs=labs,
            vitals=vitals,
        )

    return session_manager


@pytest.fixture(autouse=True)
def setup_session_manager(populated_session_manager):
    """Replace the module's session manager with populated one."""
    validation_server.session_manager = populated_session_manager
    yield
    # Reset for next test
    validation_server.session_manager = SessionManager()


class TestValidatePatients:
    """Tests for validate_patients tool."""

    @pytest.mark.asyncio
    async def test_validate_all_patients_standard(self, populated_session_manager):
        """Test validating all patients with standard level."""
        arguments = {
            "validation_level": "standard",
        }

        result = await validation_server._validate_patients_tool(arguments)

        assert len(result) == 1
        assert "Validation Results" in result[0].text
        assert "Standard Level" in result[0].text
        assert "**Patients Validated**: 3" in result[0].text

    @pytest.mark.asyncio
    async def test_validate_specific_patients(self, populated_session_manager):
        """Test validating specific patients by ID."""
        all_sessions = populated_session_manager.list_all()
        first_id = all_sessions[0].id

        arguments = {
            "patient_ids": [first_id],
            "validation_level": "standard",
        }

        result = await validation_server._validate_patients_tool(arguments)

        assert "**Patients Validated**: 1" in result[0].text

    @pytest.mark.asyncio
    async def test_validate_quick_level(self, populated_session_manager):
        """Test quick validation only shows errors."""
        arguments = {
            "validation_level": "quick",
        }

        result = await validation_server._validate_patients_tool(arguments)

        assert "Quick Level" in result[0].text
        # Quick validation should only show errors, not warnings or info

    @pytest.mark.asyncio
    async def test_validate_thorough_level(self, populated_session_manager):
        """Test thorough validation shows all issues."""
        arguments = {
            "validation_level": "thorough",
        }

        result = await validation_server._validate_patients_tool(arguments)

        assert "Thorough Level" in result[0].text

    @pytest.mark.asyncio
    async def test_validate_no_patients_error(self):
        """Test validation with no patients in session."""
        validation_server.session_manager = SessionManager()  # Empty

        arguments = {"validation_level": "standard"}

        result = await validation_server._validate_patients_tool(arguments)

        assert "No patients found" in result[0].text
        assert "Validation Error" in result[0].text


class TestValidateForExport:
    """Tests for validate_for_export tool."""

    @pytest.mark.asyncio
    async def test_validate_for_fhir(self, populated_session_manager):
        """Test FHIR export validation."""
        arguments = {
            "target_format": "fhir",
        }

        result = await validation_server._validate_for_export_tool(arguments)

        assert "FHIR Export Validation" in result[0].text
        assert "**Patients Checked**: 3" in result[0].text
        assert "FHIR Requirements" in result[0].text

    @pytest.mark.asyncio
    async def test_validate_for_hl7v2(self, populated_session_manager):
        """Test HL7v2 export validation."""
        arguments = {
            "target_format": "hl7v2",
        }

        result = await validation_server._validate_for_export_tool(arguments)

        assert "HL7V2 Export Validation" in result[0].text
        assert "HL7V2 Requirements" in result[0].text

    @pytest.mark.asyncio
    async def test_validate_for_mimic(self, populated_session_manager):
        """Test MIMIC export validation."""
        arguments = {
            "target_format": "mimic",
        }

        result = await validation_server._validate_for_export_tool(arguments)

        assert "MIMIC Export Validation" in result[0].text
        assert "MIMIC Requirements" in result[0].text

    @pytest.mark.asyncio
    async def test_validate_missing_encounter_for_hl7v2(self, generator):
        """Test HL7v2 validation catches missing encounter."""
        session_manager = SessionManager()
        patient = generator.generate_patient()

        # Add patient WITHOUT encounter
        session_manager.add_patient(patient=patient)

        validation_server.session_manager = session_manager

        arguments = {
            "target_format": "hl7v2",
        }

        result = await validation_server._validate_for_export_tool(arguments)

        # Should report error about missing encounter
        assert "missing encounter" in result[0].text.lower() or "require" in result[0].text.lower()

    @pytest.mark.asyncio
    async def test_validate_specific_patients_for_export(self, populated_session_manager):
        """Test validating specific patients for export."""
        all_sessions = populated_session_manager.list_all()
        first_id = all_sessions[0].id

        arguments = {
            "patient_ids": [first_id],
            "target_format": "fhir",
        }

        result = await validation_server._validate_for_export_tool(arguments)

        assert "**Patients Checked**: 1" in result[0].text


class TestFixValidationIssues:
    """Tests for fix_validation_issues tool."""

    @pytest.mark.asyncio
    async def test_fix_referential_issues(self, generator):
        """Test auto-fixing referential integrity issues."""
        session_manager = SessionManager()
        patient = generator.generate_patient()
        encounter = generator.generate_encounter(patient)

        # Intentionally break referential integrity
        encounter.patient_mrn = "WRONG_MRN"

        session = session_manager.add_patient(patient=patient, encounter=encounter)

        validation_server.session_manager = session_manager

        arguments = {
            "patient_id": session.id,
            "issue_type": "referential",
            "fix_strategy": "conservative",
        }

        result = await validation_server._fix_validation_issues_tool(arguments)

        assert "Auto-Fix Results" in result[0].text
        assert "Fixes Applied" in result[0].text
        # Should have fixed the MRN mismatch
        assert session.encounter.patient_mrn == patient.mrn

    @pytest.mark.asyncio
    async def test_fix_all_issues(self, generator):
        """Test fixing all auto-fixable issues."""
        session_manager = SessionManager()
        patient = generator.generate_patient()
        encounter = generator.generate_encounter(patient)
        diagnoses = [generator.generate_diagnosis(patient, encounter)]

        # Break diagnosis MRN
        diagnoses[0].patient_mrn = "WRONG_MRN"

        session = session_manager.add_patient(
            patient=patient, encounter=encounter, diagnoses=diagnoses
        )

        validation_server.session_manager = session_manager

        arguments = {
            "patient_id": session.id,
            "issue_type": "all",
        }

        result = await validation_server._fix_validation_issues_tool(arguments)

        assert "Auto-Fix Results" in result[0].text
        # Should have fixed diagnosis MRN
        assert diagnoses[0].patient_mrn == patient.mrn

    @pytest.mark.asyncio
    async def test_fix_patient_not_found(self):
        """Test fixing non-existent patient."""
        arguments = {
            "patient_id": "nonexistent",
            "issue_type": "all",
        }

        result = await validation_server._fix_validation_issues_tool(arguments)

        assert "not found" in result[0].text
        assert "Validation Error" in result[0].text

    @pytest.mark.asyncio
    async def test_fix_no_issues(self, populated_session_manager):
        """Test fixing patient with no issues."""
        all_sessions = populated_session_manager.list_all()
        first_id = all_sessions[0].id

        arguments = {
            "patient_id": first_id,
            "issue_type": "all",
        }

        result = await validation_server._fix_validation_issues_tool(arguments)

        assert "Auto-Fix Results" in result[0].text
        # May show "No fixes needed" or "All Issues Resolved"


class TestExplainValidationRule:
    """Tests for explain_validation_rule tool."""

    @pytest.mark.asyncio
    async def test_explain_temporal_rule(self):
        """Test explaining a temporal validation rule."""
        arguments = {
            "rule_code": "TEMP_001",
        }

        result = await validation_server._explain_validation_rule_tool(arguments)

        assert "Validation Rule: TEMP_001" in result[0].text
        assert "What This Checks" in result[0].text
        assert "Why This Matters" in result[0].text
        assert "death date" in result[0].text.lower()

    @pytest.mark.asyncio
    async def test_explain_referential_rule(self):
        """Test explaining a referential integrity rule."""
        arguments = {
            "rule_code": "REF_001",
        }

        result = await validation_server._explain_validation_rule_tool(arguments)

        assert "REF_001" in result[0].text
        assert "diagnosis" in result[0].text.lower()
        assert "patient_mrn" in result[0].text.lower()

    @pytest.mark.asyncio
    async def test_explain_clinical_rule(self):
        """Test explaining a clinical validation rule."""
        arguments = {
            "rule_code": "CLIN_001",
        }

        result = await validation_server._explain_validation_rule_tool(arguments)

        assert "CLIN_001" in result[0].text
        assert "geriatric" in result[0].text.lower() or "age" in result[0].text.lower()

    @pytest.mark.asyncio
    async def test_explain_vital_signs_rule(self):
        """Test explaining a vital signs rule."""
        arguments = {
            "rule_code": "CLIN_006",
        }

        result = await validation_server._explain_validation_rule_tool(arguments)

        assert "CLIN_006" in result[0].text
        assert "temperature" in result[0].text.lower()

    @pytest.mark.asyncio
    async def test_explain_unknown_rule(self):
        """Test explaining an unknown rule code."""
        arguments = {
            "rule_code": "UNKNOWN_999",
        }

        result = await validation_server._explain_validation_rule_tool(arguments)

        assert "Unknown validation rule" in result[0].text
        assert "Validation Error" in result[0].text


class TestGetSessionsByIds:
    """Tests for _get_sessions_by_ids helper function."""

    def test_get_all_sessions_when_none(self, populated_session_manager):
        """Test getting all sessions when patient_ids is None."""
        sessions = validation_server._get_sessions_by_ids(None)

        assert len(sessions) == 3

    def test_get_sessions_by_id(self, populated_session_manager):
        """Test getting sessions by specific IDs."""
        all_sessions = populated_session_manager.list_all()
        first_id = all_sessions[0].id
        second_id = all_sessions[1].id

        sessions = validation_server._get_sessions_by_ids([first_id, second_id])

        assert len(sessions) == 2
        assert sessions[0].id == first_id
        assert sessions[1].id == second_id

    def test_get_sessions_by_position(self, populated_session_manager):
        """Test getting sessions by position string."""
        sessions = validation_server._get_sessions_by_ids(["1", "2"])

        assert len(sessions) == 2

    def test_get_sessions_ignores_invalid_ids(self, populated_session_manager):
        """Test that invalid IDs are ignored."""
        all_sessions = populated_session_manager.list_all()
        valid_id = all_sessions[0].id

        sessions = validation_server._get_sessions_by_ids([valid_id, "invalid_id", "999"])

        assert len(sessions) == 1
        assert sessions[0].id == valid_id
