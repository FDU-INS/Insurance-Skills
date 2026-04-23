"""Tests for MCP export server functionality."""

import json

import pytest

from patientsim.core.generator import PatientGenerator
from patientsim.mcp import export_server
from patientsim.mcp.session import SessionManager

# Check for optional dependencies
try:
    import pyarrow  # noqa: F401

    HAS_PYARROW = True
except ImportError:
    HAS_PYARROW = False


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
    export_server.session_manager = populated_session_manager
    yield
    # Reset for next test
    export_server.session_manager = SessionManager()


class TestGetSessionsByIds:
    """Tests for _get_sessions_by_ids helper function."""

    def test_get_all_sessions_when_none(self, populated_session_manager):
        """Test getting all sessions when patient_ids is None."""
        sessions = export_server._get_sessions_by_ids(None)

        assert len(sessions) == 3

    def test_get_sessions_by_id(self, populated_session_manager):
        """Test getting sessions by specific IDs."""
        all_sessions = populated_session_manager.list_all()
        first_id = all_sessions[0].id
        second_id = all_sessions[1].id

        sessions = export_server._get_sessions_by_ids([first_id, second_id])

        assert len(sessions) == 2
        assert sessions[0].id == first_id
        assert sessions[1].id == second_id

    def test_get_sessions_by_position(self, populated_session_manager):
        """Test getting sessions by position string."""
        sessions = export_server._get_sessions_by_ids(["1", "2"])

        assert len(sessions) == 2

    def test_get_sessions_ignores_invalid_ids(self, populated_session_manager):
        """Test that invalid IDs are ignored."""
        all_sessions = populated_session_manager.list_all()
        valid_id = all_sessions[0].id

        sessions = export_server._get_sessions_by_ids([valid_id, "invalid_id", "999"])

        assert len(sessions) == 1
        assert sessions[0].id == valid_id


class TestExportFHIR:
    """Tests for FHIR export functionality."""

    @pytest.mark.asyncio
    async def test_export_fhir_all_patients(self, tmp_path, populated_session_manager):
        """Test exporting all patients to FHIR."""
        output_file = tmp_path / "test_bundle.json"

        arguments = {
            "output_path": str(output_file),
            "bundle_type": "collection",
        }

        result = await export_server._export_fhir_tool(arguments)

        assert len(result) == 1
        assert "FHIR Export Complete" in result[0].text
        assert "3" in result[0].text  # 3 patients

        # Verify file was created
        assert output_file.exists()

        # Verify it's valid JSON
        with open(output_file) as f:
            bundle = json.load(f)

        assert bundle["resourceType"] == "Bundle"
        assert bundle["type"] == "collection"
        assert len(bundle["entry"]) > 0

    @pytest.mark.asyncio
    async def test_export_fhir_specific_patients(self, tmp_path, populated_session_manager):
        """Test exporting specific patients by ID."""
        all_sessions = populated_session_manager.list_all()
        first_id = all_sessions[0].id

        output_file = tmp_path / "single_bundle.json"

        arguments = {
            "patient_ids": [first_id],
            "output_path": str(output_file),
        }

        result = await export_server._export_fhir_tool(arguments)

        assert "FHIR Export Complete" in result[0].text
        assert "1" in result[0].text  # 1 patient

        assert output_file.exists()

    @pytest.mark.asyncio
    async def test_export_fhir_no_patients_error(self):
        """Test FHIR export with no patients in session."""
        export_server.session_manager = SessionManager()  # Empty

        arguments = {"bundle_type": "collection"}

        result = await export_server._export_fhir_tool(arguments)

        assert "No patients found" in result[0].text
        assert "FHIR Export Failed" in result[0].text


class TestExportHL7v2:
    """Tests for HL7v2 export functionality."""

    @pytest.mark.asyncio
    async def test_export_hl7v2_all_patients(self, tmp_path, populated_session_manager):
        """Test exporting all patients to HL7v2."""
        output_dir = tmp_path / "hl7_messages"

        arguments = {
            "output_dir": str(output_dir),
            "message_types": ["ADT^A01"],
        }

        result = await export_server._export_hl7v2_tool(arguments)

        assert "HL7v2 Export Complete" in result[0].text
        assert "3" in result[0].text  # 3 patients

        # Verify directory was created
        assert output_dir.exists()
        assert output_dir.is_dir()

        # Verify message files were created
        message_files = list(output_dir.glob("*.hl7"))
        assert len(message_files) == 3

    @pytest.mark.asyncio
    async def test_export_hl7v2_message_content(self, tmp_path, populated_session_manager):
        """Test HL7v2 message content is valid."""
        output_dir = tmp_path / "messages"

        arguments = {
            "output_dir": str(output_dir),
            "message_types": ["ADT^A01"],
        }

        await export_server._export_hl7v2_tool(arguments)

        # Read one message file
        message_file = list(output_dir.glob("*.hl7"))[0]
        with open(message_file) as f:
            message = f.read()

        # Verify HL7v2 structure
        assert message.startswith("MSH|")
        assert "\n" in message  # Should have segment separators
        assert "ADT^A01" in message


class TestExportMIMIC:
    """Tests for MIMIC export functionality."""

    @pytest.mark.asyncio
    async def test_export_mimic_all_tables(self, tmp_path, populated_session_manager):
        """Test exporting all MIMIC tables."""
        output_dir = tmp_path / "mimic"

        arguments = {
            "output_dir": str(output_dir),
            "tables": ["all"],
            "format": "csv",
        }

        result = await export_server._export_mimic_tool(arguments)

        assert "MIMIC Export Complete" in result[0].text
        assert "3" in result[0].text  # 3 patients

        # Verify tables were created
        assert (output_dir / "PATIENTS.csv").exists()
        assert (output_dir / "ADMISSIONS.csv").exists()
        assert (output_dir / "DIAGNOSES_ICD.csv").exists()
        assert (output_dir / "LABEVENTS.csv").exists()
        assert (output_dir / "CHARTEVENTS.csv").exists()

    @pytest.mark.asyncio
    async def test_export_mimic_specific_tables(self, tmp_path, populated_session_manager):
        """Test exporting specific MIMIC tables."""
        output_dir = tmp_path / "mimic_partial"

        arguments = {
            "output_dir": str(output_dir),
            "tables": ["PATIENTS", "ADMISSIONS"],
            "format": "csv",
        }

        result = await export_server._export_mimic_tool(arguments)

        assert "MIMIC Export Complete" in result[0].text

        # Verify only requested tables were created
        assert (output_dir / "PATIENTS.csv").exists()
        assert (output_dir / "ADMISSIONS.csv").exists()
        assert not (output_dir / "DIAGNOSES_ICD.csv").exists()

    @pytest.mark.asyncio
    @pytest.mark.skipif(not HAS_PYARROW, reason="pyarrow not installed")
    async def test_export_mimic_parquet_format(self, tmp_path, populated_session_manager):
        """Test exporting MIMIC in parquet format."""
        output_dir = tmp_path / "mimic_parquet"

        arguments = {
            "output_dir": str(output_dir),
            "tables": ["PATIENTS"],
            "format": "parquet",
        }

        result = await export_server._export_mimic_tool(arguments)

        assert "MIMIC Export Complete" in result[0].text
        assert (output_dir / "PATIENTS.parquet").exists()


class TestExportJSON:
    """Tests for JSON export functionality."""

    @pytest.mark.asyncio
    async def test_export_json_all_patients(self, tmp_path, populated_session_manager):
        """Test exporting all patients to JSON."""
        output_file = tmp_path / "patients.json"

        arguments = {
            "output_path": str(output_file),
            "include_metadata": True,
        }

        result = await export_server._export_json_tool(arguments)

        assert "JSON Export Complete" in result[0].text
        assert "3" in result[0].text

        # Verify file was created
        assert output_file.exists()

        # Verify JSON structure
        with open(output_file) as f:
            data = json.load(f)

        assert "patients" in data
        assert len(data["patients"]) == 3
        assert "metadata" in data
        assert data["metadata"]["patient_count"] == 3

    @pytest.mark.asyncio
    async def test_export_json_without_metadata(self, tmp_path, populated_session_manager):
        """Test exporting JSON without metadata."""
        output_file = tmp_path / "patients_no_meta.json"

        arguments = {
            "output_path": str(output_file),
            "include_metadata": False,
        }

        await export_server._export_json_tool(arguments)

        with open(output_file) as f:
            data = json.load(f)

        assert "patients" in data
        assert "metadata" not in data


class TestListExportFormats:
    """Tests for listing export formats."""

    @pytest.mark.asyncio
    async def test_list_export_formats(self):
        """Test listing available export formats."""
        result = await export_server._list_export_formats_tool({})

        assert len(result) == 1
        assert "Available Export Formats" in result[0].text
        assert "FHIR" in result[0].text
        assert "HL7v2" in result[0].text
        assert "MIMIC" in result[0].text
        assert "JSON" in result[0].text
