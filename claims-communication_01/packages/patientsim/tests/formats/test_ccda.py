"""Tests for C-CDA format transformer and validators.

Tests cover:
- ValidationResult dataclass
- CCDAValidator template validation
- CCDAValidator section validation
- CCDAValidator code system validation
- XML parsing and error handling
"""

import pytest

from patientsim.formats.ccda import CCDAValidator, ValidationResult


class TestValidationResult:
    """Tests for ValidationResult dataclass."""

    def test_default_is_valid(self):
        """ValidationResult should default to valid."""
        result = ValidationResult()
        assert result.is_valid is True
        assert result.errors == []
        assert result.warnings == []

    def test_add_error_marks_invalid(self):
        """Adding an error should mark result as invalid."""
        result = ValidationResult()
        result.add_error("Test error")
        assert result.is_valid is False
        assert "Test error" in result.errors

    def test_add_warning_keeps_valid(self):
        """Adding a warning should not affect validity."""
        result = ValidationResult()
        result.add_warning("Test warning")
        assert result.is_valid is True
        assert "Test warning" in result.warnings

    def test_merge_results(self):
        """Merging results should combine errors and warnings."""
        result1 = ValidationResult()
        result1.add_error("Error 1")

        result2 = ValidationResult()
        result2.add_warning("Warning 1")

        result1.merge(result2)
        assert result1.is_valid is False
        assert "Error 1" in result1.errors
        assert "Warning 1" in result1.warnings

    def test_merge_invalid_result(self):
        """Merging an invalid result should make target invalid."""
        result1 = ValidationResult()
        result2 = ValidationResult()
        result2.add_error("Error from result2")

        result1.merge(result2)
        assert result1.is_valid is False


class TestCCDAValidator:
    """Tests for CCDAValidator class."""

    @pytest.fixture
    def validator(self):
        """Create a validator instance."""
        return CCDAValidator()

    @pytest.fixture
    def minimal_valid_ccda(self):
        """Return minimal valid C-CDA XML structure."""
        return """<?xml version="1.0" encoding="UTF-8"?>
<ClinicalDocument xmlns="urn:hl7-org:v3">
    <templateId root="2.16.840.1.113883.10.20.22.1.1"/>
    <templateId root="2.16.840.1.113883.10.20.22.1.2"/>
    <id root="2.16.840.1.113883.3.1234" extension="12345"/>
    <code code="34133-9" codeSystem="2.16.840.1.113883.6.1"/>
    <effectiveTime value="20231201"/>
    <confidentialityCode code="N" codeSystem="2.16.840.1.113883.5.25"/>
    <recordTarget>
        <patientRole>
            <id root="2.16.840.1.113883.3.1234" extension="PAT001"/>
        </patientRole>
    </recordTarget>
    <author>
        <time value="20231201"/>
        <assignedAuthor>
            <id root="2.16.840.1.113883.3.1234"/>
        </assignedAuthor>
    </author>
    <custodian>
        <assignedCustodian>
            <representedCustodianOrganization>
                <id root="2.16.840.1.113883.3.1234"/>
            </representedCustodianOrganization>
        </assignedCustodian>
    </custodian>
</ClinicalDocument>"""

    @pytest.fixture
    def invalid_xml(self):
        """Return invalid XML."""
        return "<ClinicalDocument><unclosed>"

    @pytest.fixture
    def wrong_root_element(self):
        """Return XML with wrong root element."""
        return """<?xml version="1.0"?>
<Document xmlns="urn:hl7-org:v3">
    <templateId root="2.16.840.1.113883.10.20.22.1.1"/>
</Document>"""

    @pytest.fixture
    def missing_us_realm_header(self):
        """Return C-CDA missing US Realm Header template."""
        return """<?xml version="1.0" encoding="UTF-8"?>
<ClinicalDocument xmlns="urn:hl7-org:v3">
    <templateId root="2.16.840.1.113883.10.20.22.1.2"/>
    <id root="2.16.840.1.113883.3.1234"/>
    <code code="34133-9" codeSystem="2.16.840.1.113883.6.1"/>
    <effectiveTime value="20231201"/>
    <confidentialityCode code="N"/>
    <recordTarget><patientRole><id root="1.2.3"/></patientRole></recordTarget>
    <author><time value="20231201"/><assignedAuthor><id root="1.2.3"/></assignedAuthor></author>
    <custodian><assignedCustodian><representedCustodianOrganization><id root="1.2.3"/></representedCustodianOrganization></assignedCustodian></custodian>
</ClinicalDocument>"""

    def test_validate_valid_ccda(self, validator, minimal_valid_ccda):
        """Valid C-CDA should pass validation."""
        result = validator.validate(minimal_valid_ccda)
        assert result.is_valid is True
        assert len(result.errors) == 0

    def test_validate_invalid_xml(self, validator, invalid_xml):
        """Invalid XML should fail with parse error."""
        result = validator.validate(invalid_xml)
        assert result.is_valid is False
        assert any("parse error" in e.lower() for e in result.errors)

    def test_validate_wrong_root_element(self, validator, wrong_root_element):
        """Wrong root element should fail validation."""
        result = validator.validate(wrong_root_element)
        assert result.is_valid is False
        assert any("ClinicalDocument" in e for e in result.errors)

    def test_validate_missing_us_realm_header(self, validator, missing_us_realm_header):
        """Missing US Realm Header should fail validation."""
        result = validator.validate(missing_us_realm_header)
        assert result.is_valid is False
        assert any("US Realm Header" in e for e in result.errors)

    def test_document_templates_defined(self, validator):
        """Validator should have document templates defined."""
        assert "CCD" in validator.DOCUMENT_TEMPLATES
        assert "DISCHARGE_SUMMARY" in validator.DOCUMENT_TEMPLATES
        assert "REFERRAL_NOTE" in validator.DOCUMENT_TEMPLATES
        assert "TRANSFER_SUMMARY" in validator.DOCUMENT_TEMPLATES

    def test_section_templates_defined(self, validator):
        """Validator should have section templates defined."""
        assert "problems" in validator.SECTION_TEMPLATES
        assert "medications" in validator.SECTION_TEMPLATES
        assert "allergies" in validator.SECTION_TEMPLATES
        assert "results" in validator.SECTION_TEMPLATES

    def test_required_sections_by_doc_type(self, validator):
        """Validator should have required sections by document type."""
        assert "problems" in validator.REQUIRED_SECTIONS["CCD"]
        assert "medications" in validator.REQUIRED_SECTIONS["CCD"]
        assert "hospital_course" in validator.REQUIRED_SECTIONS["DISCHARGE_SUMMARY"]
        assert "reason_for_referral" in validator.REQUIRED_SECTIONS["REFERRAL_NOTE"]

    def test_valid_code_systems_defined(self, validator):
        """Validator should have valid code systems defined."""
        # SNOMED CT
        assert "2.16.840.1.113883.6.96" in validator.VALID_CODE_SYSTEMS
        # RxNorm
        assert "2.16.840.1.113883.6.88" in validator.VALID_CODE_SYSTEMS
        # LOINC
        assert "2.16.840.1.113883.6.1" in validator.VALID_CODE_SYSTEMS
        # ICD-10-CM
        assert "2.16.840.1.113883.6.90" in validator.VALID_CODE_SYSTEMS

    def test_validate_file_not_found(self, validator, tmp_path):
        """Validating non-existent file should fail gracefully."""
        result = validator.validate_file(str(tmp_path / "nonexistent.xml"))
        assert result.is_valid is False
        assert any("not found" in e.lower() for e in result.errors)

    def test_validate_file_success(self, validator, minimal_valid_ccda, tmp_path):
        """Validating file should work for valid content."""
        file_path = tmp_path / "test.xml"
        file_path.write_text(minimal_valid_ccda)

        result = validator.validate_file(str(file_path))
        assert result.is_valid is True

    def test_validate_batch(self, validator, minimal_valid_ccda, invalid_xml):
        """Batch validation should return results for all documents."""
        documents = [
            ("valid.xml", minimal_valid_ccda),
            ("invalid.xml", invalid_xml),
        ]

        results = validator.validate_batch(documents)

        assert "valid.xml" in results
        assert "invalid.xml" in results
        assert results["valid.xml"].is_valid is True
        assert results["invalid.xml"].is_valid is False


class TestCCDAValidatorCodeSystems:
    """Tests for code system validation."""

    @pytest.fixture
    def validator(self):
        return CCDAValidator()

    def test_unknown_code_system_warning(self, validator):
        """Unknown but valid OID format should generate warning."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
<ClinicalDocument xmlns="urn:hl7-org:v3">
    <templateId root="2.16.840.1.113883.10.20.22.1.1"/>
    <templateId root="2.16.840.1.113883.10.20.22.1.2"/>
    <id root="2.16.840.1.113883.3.1234"/>
    <code code="34133-9" codeSystem="2.16.840.1.113883.6.1"/>
    <effectiveTime value="20231201"/>
    <confidentialityCode code="N" codeSystem="2.16.840.1.113883.5.25"/>
    <recordTarget><patientRole><id root="1.2.3"/></patientRole></recordTarget>
    <author><time value="20231201"/><assignedAuthor><id root="1.2.3"/></assignedAuthor></author>
    <custodian><assignedCustodian><representedCustodianOrganization><id root="1.2.3"/></representedCustodianOrganization></assignedCustodian></custodian>
    <component>
        <structuredBody>
            <component>
                <section>
                    <code code="TEST" codeSystem="9.9.9.9.9.9"/>
                </section>
            </component>
        </structuredBody>
    </component>
</ClinicalDocument>"""

        result = validator.validate(xml)
        # Should have warning about unknown code system
        assert any("9.9.9.9.9.9" in w for w in result.warnings)


class TestCCDAValidatorIntegration:
    """Integration tests using example C-CDA files."""

    @pytest.fixture
    def validator(self):
        return CCDAValidator()

    @pytest.fixture
    def examples_dir(self):
        """Get examples directory path."""
        from pathlib import Path

        examples = Path(__file__).parent.parent.parent / "examples" / "ccda"
        if not examples.exists():
            pytest.skip("Examples directory not found")
        return examples

    def test_validate_ccd_examples(self, validator, examples_dir):
        """All CCD examples should pass validation."""
        ccd_dir = examples_dir / "ccd"
        if not ccd_dir.exists():
            pytest.skip("CCD examples not found")

        for xml_file in ccd_dir.glob("*.xml"):
            result = validator.validate_file(str(xml_file))
            assert result.is_valid, f"{xml_file.name} failed: {result.errors}"

    def test_validate_discharge_summary_examples(self, validator, examples_dir):
        """All discharge summary examples should pass validation."""
        discharge_dir = examples_dir / "discharge-summary"
        if not discharge_dir.exists():
            pytest.skip("Discharge summary examples not found")

        for xml_file in discharge_dir.glob("*.xml"):
            result = validator.validate_file(str(xml_file))
            assert result.is_valid, f"{xml_file.name} failed: {result.errors}"

    def test_validate_referral_note_examples(self, validator, examples_dir):
        """All referral note examples should pass validation."""
        referral_dir = examples_dir / "referral-note"
        if not referral_dir.exists():
            pytest.skip("Referral note examples not found")

        for xml_file in referral_dir.glob("*.xml"):
            result = validator.validate_file(str(xml_file))
            assert result.is_valid, f"{xml_file.name} failed: {result.errors}"

    def test_validate_transfer_summary_examples(self, validator, examples_dir):
        """All transfer summary examples should pass validation."""
        transfer_dir = examples_dir / "transfer-summary"
        if not transfer_dir.exists():
            pytest.skip("Transfer summary examples not found")

        for xml_file in transfer_dir.glob("*.xml"):
            result = validator.validate_file(str(xml_file))
            assert result.is_valid, f"{xml_file.name} failed: {result.errors}"
