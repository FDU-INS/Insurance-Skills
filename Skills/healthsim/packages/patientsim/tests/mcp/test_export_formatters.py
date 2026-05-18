"""Tests for MCP export response formatters."""

from patientsim.mcp.export_formatters import (
    format_export_error,
    format_export_formats_list,
    format_export_summary,
)


class TestFormatExportSummary:
    """Tests for export summary formatting."""

    def test_format_fhir_export(self, tmp_path):
        """Test formatting FHIR export summary."""
        output_file = tmp_path / "bundle.json"

        result = format_export_summary(
            format_name="FHIR",
            patient_count=5,
            details={
                "resources": {
                    "Patient": 5,
                    "Encounter": 5,
                    "Condition": 10,
                    "Observation": 25,
                }
            },
            file_paths=output_file,
        )

        assert "FHIR Export Complete" in result
        assert "5" in result  # patient count
        assert "**Patient**: 5" in result
        assert "**Encounter**: 5" in result
        assert str(output_file) in result

    def test_format_hl7v2_export(self, tmp_path):
        """Test formatting HL7v2 export summary."""
        output_dir = tmp_path / "messages"

        result = format_export_summary(
            format_name="HL7v2",
            patient_count=3,
            details={
                "messages": {
                    "ADT^A01": 3,
                }
            },
            file_paths=[output_dir],
        )

        assert "HL7v2 Export Complete" in result
        assert "3" in result
        assert "**ADT^A01**: 3" in result

    def test_format_mimic_export(self, tmp_path):
        """Test formatting MIMIC export summary."""
        files = [
            tmp_path / "PATIENTS.csv",
            tmp_path / "ADMISSIONS.csv",
            tmp_path / "DIAGNOSES_ICD.csv",
        ]

        result = format_export_summary(
            format_name="MIMIC",
            patient_count=10,
            details={
                "tables": {
                    "PATIENTS": 10,
                    "ADMISSIONS": 10,
                    "DIAGNOSES_ICD": 25,
                }
            },
            file_paths=files,
        )

        assert "MIMIC Export Complete" in result
        assert "10" in result
        assert "**PATIENTS**: 10 rows" in result
        assert "**ADMISSIONS**: 10 rows" in result

    def test_format_with_validation_warnings(self, tmp_path):
        """Test export summary with validation warnings."""
        output_file = tmp_path / "bundle.json"
        warnings = [
            "Missing encounter reference in 2 observations",
            "1 patient has incomplete address",
        ]

        result = format_export_summary(
            format_name="FHIR",
            patient_count=5,
            details={"resources": {"Patient": 5}},
            file_paths=output_file,
            validation_warnings=warnings,
        )

        assert "Validation Warnings" in result
        assert "Missing encounter reference" in result
        assert "incomplete address" in result

    def test_format_includes_next_steps(self, tmp_path):
        """Test that export summary includes next steps."""
        output_file = tmp_path / "bundle.json"

        result = format_export_summary(
            format_name="FHIR",
            patient_count=1,
            details={"resources": {"Patient": 1}},
            file_paths=output_file,
        )

        assert "Next Steps" in result
        assert "fhir" in result.lower() or "FHIR" in result


class TestFormatExportFormatsList:
    """Tests for export formats list formatting."""

    def test_format_formats_list(self):
        """Test formatting the list of available formats."""
        result = format_export_formats_list()

        assert "Available Export Formats" in result
        assert "FHIR R4" in result
        assert "HL7v2" in result
        assert "MIMIC-III" in result
        assert "JSON" in result

        # Check descriptions are present
        assert "Use Cases" in result
        assert "Output" in result

    def test_formats_list_includes_all_formats(self):
        """Test that all expected formats are included."""
        result = format_export_formats_list()

        # Should describe each format
        assert "HL7 FHIR R4" in result
        assert "HL7 Version 2" in result
        assert "MIMIC-III critical care" in result
        assert "PatientSim JSON" in result


class TestFormatExportError:
    """Tests for export error formatting."""

    def test_format_error_minimal(self):
        """Test formatting error with just message."""
        result = format_export_error("FHIR", "No patients found in session")

        assert "FHIR Export Failed" in result
        assert "No patients found" in result

    def test_format_error_with_suggestion(self):
        """Test formatting error with suggestion."""
        result = format_export_error(
            "HL7v2",
            "Missing encounter data",
            "Ensure patients have encounter information before exporting",
        )

        assert "HL7v2 Export Failed" in result
        assert "Missing encounter data" in result
        assert "Suggestion" in result
        assert "encounter information" in result
