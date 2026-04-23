"""C-CDA document validators.

Provides validation utilities for C-CDA documents to ensure
conformance with C-CDA 2.1 structure requirements.

Example:
    >>> from patientsim.formats.ccda.validators import CCDAValidator, ValidationResult
    >>> validator = CCDAValidator()
    >>> result = validator.validate(xml_string)
    >>> if result.is_valid:
    ...     print("Document is valid")
    ... else:
    ...     for error in result.errors:
    ...         print(f"Error: {error}")
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import TYPE_CHECKING
from xml.etree import ElementTree as ET

if TYPE_CHECKING:
    from collections.abc import Sequence


@dataclass
class ValidationResult:
    """Result of C-CDA document validation.

    Attributes:
        is_valid: Whether the document passed all required validations.
        errors: List of validation errors (failures that indicate non-conformance).
        warnings: List of validation warnings (issues that should be reviewed).
    """

    is_valid: bool = True
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def add_error(self, message: str) -> None:
        """Add an error and mark result as invalid."""
        self.errors.append(message)
        self.is_valid = False

    def add_warning(self, message: str) -> None:
        """Add a warning without affecting validity."""
        self.warnings.append(message)

    def merge(self, other: ValidationResult) -> None:
        """Merge another validation result into this one."""
        if not other.is_valid:
            self.is_valid = False
        self.errors.extend(other.errors)
        self.warnings.extend(other.warnings)


class CCDAValidator:
    """Validator for C-CDA 2.1 documents.

    Validates C-CDA documents for structural conformance including:
    - XML well-formedness
    - Required template OIDs
    - Required sections by document type
    - Code system OID validity

    Example:
        >>> validator = CCDAValidator()
        >>> result = validator.validate(xml_string)
        >>> print(f"Valid: {result.is_valid}, Errors: {len(result.errors)}")
    """

    # US Realm Header template OID (required for all C-CDA documents)
    US_REALM_HEADER_OID = "2.16.840.1.113883.10.20.22.1.1"

    # Document type template OIDs
    DOCUMENT_TEMPLATES: dict[str, str] = {
        "CCD": "2.16.840.1.113883.10.20.22.1.2",
        "DISCHARGE_SUMMARY": "2.16.840.1.113883.10.20.22.1.8",
        "REFERRAL_NOTE": "2.16.840.1.113883.10.20.22.1.14",
        "TRANSFER_SUMMARY": "2.16.840.1.113883.10.20.22.1.13",
    }

    # Section template OIDs
    SECTION_TEMPLATES: dict[str, str] = {
        "problems": "2.16.840.1.113883.10.20.22.2.5.1",
        "medications": "2.16.840.1.113883.10.20.22.2.1.1",
        "allergies": "2.16.840.1.113883.10.20.22.2.6.1",
        "results": "2.16.840.1.113883.10.20.22.2.3.1",
        "vital_signs": "2.16.840.1.113883.10.20.22.2.4.1",
        "procedures": "2.16.840.1.113883.10.20.22.2.7.1",
        "encounters": "2.16.840.1.113883.10.20.22.2.22.1",
        "immunizations": "2.16.840.1.113883.10.20.22.2.2.1",
        "social_history": "2.16.840.1.113883.10.20.22.2.17",
        "plan_of_treatment": "2.16.840.1.113883.10.20.22.2.10",
        "hospital_course": "1.3.6.1.4.1.19376.1.5.3.1.3.5",
        "discharge_instructions": "2.16.840.1.113883.10.20.22.2.41",
        "reason_for_referral": "1.3.6.1.4.1.19376.1.5.3.1.3.1",
    }

    # Required sections by document type (SHALL requirements)
    REQUIRED_SECTIONS: dict[str, list[str]] = {
        "CCD": [
            "problems",
            "medications",
            "allergies",
        ],
        "DISCHARGE_SUMMARY": [
            "problems",
            "medications",
            "allergies",
            "hospital_course",
        ],
        "REFERRAL_NOTE": [
            "problems",
            "reason_for_referral",
        ],
        "TRANSFER_SUMMARY": [
            "problems",
            "medications",
        ],
    }

    # Valid code system OIDs
    VALID_CODE_SYSTEMS: dict[str, str] = {
        # Clinical terminologies
        "2.16.840.1.113883.6.96": "SNOMED CT",
        "2.16.840.1.113883.6.90": "ICD-10-CM",
        "2.16.840.1.113883.6.88": "RxNorm",
        "2.16.840.1.113883.6.1": "LOINC",
        "2.16.840.1.113883.6.12": "CPT",
        "2.16.840.1.113883.12.292": "CVX",
        "2.16.840.1.113883.6.69": "NDC",
        "2.16.840.1.113883.3.26.1.1": "NCI Thesaurus",
        # HL7 vocabulary domains
        "2.16.840.1.113883.5.1": "AdministrativeGender",
        "2.16.840.1.113883.5.2": "MaritalStatus",
        "2.16.840.1.113883.5.4": "ActCode",
        "2.16.840.1.113883.5.6": "ActClass",
        "2.16.840.1.113883.5.25": "Confidentiality",
        "2.16.840.1.113883.5.83": "ObservationInterpretation",
        "2.16.840.1.113883.5.88": "ParticipationFunction",
        "2.16.840.1.113883.5.111": "RoleCode",
        # Provider and demographic code systems
        "2.16.840.1.113883.6.101": "NUCC Healthcare Provider Taxonomy",
        "2.16.840.1.113883.6.238": "CDC Race and Ethnicity",
        "2.16.840.1.113883.6.301.5": "NUBC UB-04 Point of Origin",
    }

    # CDA namespace
    CDA_NS = "urn:hl7-org:v3"
    NAMESPACES = {"cda": CDA_NS}

    def __init__(self) -> None:
        """Initialize the validator."""
        pass

    def validate(self, xml_string: str) -> ValidationResult:
        """Validate a C-CDA document.

        Args:
            xml_string: The C-CDA XML document as a string.

        Returns:
            ValidationResult with is_valid status, errors, and warnings.
        """
        result = ValidationResult()

        # Step 1: Parse XML
        try:
            # Handle namespace prefix
            root = ET.fromstring(xml_string)
        except ET.ParseError as e:
            result.add_error(f"XML parse error: {e}")
            return result

        # Step 2: Check for ClinicalDocument root
        root_tag = root.tag.replace(f"{{{self.CDA_NS}}}", "")
        if root_tag != "ClinicalDocument":
            result.add_error(f"Root element must be 'ClinicalDocument', found '{root_tag}'")
            return result

        # Step 3: Check US Realm Header template
        result.merge(self._validate_us_realm_header(root))

        # Step 4: Determine document type and validate template
        doc_type = self._determine_document_type(root)
        if doc_type:
            result.merge(self._validate_document_type(root, doc_type))
        else:
            result.add_warning("Could not determine document type from templateId elements")

        # Step 5: Validate required sections (if document type known)
        if doc_type:
            result.merge(self._validate_required_sections(root, doc_type))

        # Step 6: Validate code systems used
        result.merge(self._validate_code_systems(root))

        # Step 7: Check for required header elements
        result.merge(self._validate_header_elements(root))

        return result

    def _validate_us_realm_header(self, root: ET.Element) -> ValidationResult:
        """Validate presence of US Realm Header template."""
        result = ValidationResult()

        template_ids = self._get_template_ids(root)
        if self.US_REALM_HEADER_OID not in template_ids:
            result.add_error(f"Missing US Realm Header template (OID: {self.US_REALM_HEADER_OID})")

        return result

    def _determine_document_type(self, root: ET.Element) -> str | None:
        """Determine C-CDA document type from template IDs."""
        template_ids = self._get_template_ids(root)

        for doc_type, oid in self.DOCUMENT_TEMPLATES.items():
            if oid in template_ids:
                return doc_type

        return None

    def _validate_document_type(self, root: ET.Element, doc_type: str) -> ValidationResult:
        """Validate document type template is present."""
        result = ValidationResult()

        expected_oid = self.DOCUMENT_TEMPLATES.get(doc_type)
        if expected_oid:
            template_ids = self._get_template_ids(root)
            if expected_oid not in template_ids:
                result.add_error(f"Missing {doc_type} document template (OID: {expected_oid})")

        return result

    def _validate_required_sections(self, root: ET.Element, doc_type: str) -> ValidationResult:
        """Validate required sections are present for document type."""
        result = ValidationResult()

        required = self.REQUIRED_SECTIONS.get(doc_type, [])
        present_sections = self._get_section_template_ids(root)

        for section_name in required:
            section_oid = self.SECTION_TEMPLATES.get(section_name)
            if section_oid and section_oid not in present_sections:
                result.add_warning(
                    f"Missing required section '{section_name}' "
                    f"(OID: {section_oid}) for {doc_type}"
                )

        return result

    def _validate_code_systems(self, root: ET.Element) -> ValidationResult:
        """Validate code system OIDs used in the document."""
        result = ValidationResult()

        # Find all elements with codeSystem attribute
        unknown_systems: set[str] = set()

        for elem in root.iter():
            code_system = elem.get("codeSystem")
            if code_system and code_system not in self.VALID_CODE_SYSTEMS:
                # Check if it looks like a valid OID format
                if re.match(r"^[\d.]+$", code_system):
                    unknown_systems.add(code_system)
                else:
                    result.add_warning(f"Invalid codeSystem format: {code_system}")

        # Report unknown but valid-format OIDs as warnings
        for oid in sorted(unknown_systems):
            result.add_warning(f"Unknown code system OID: {oid}")

        return result

    def _validate_header_elements(self, root: ET.Element) -> ValidationResult:
        """Validate required header elements are present."""
        result = ValidationResult()

        # Check for required elements (simplified check using local name)
        required_elements = [
            ("id", "Document ID"),
            ("code", "Document type code"),
            ("effectiveTime", "Document effective time"),
            ("confidentialityCode", "Confidentiality code"),
            ("recordTarget", "Patient (recordTarget)"),
            ("author", "Author"),
            ("custodian", "Custodian"),
        ]

        for elem_name, description in required_elements:
            # Search with and without namespace
            found = root.find(f"cda:{elem_name}", self.NAMESPACES)
            if found is None:
                found = root.find(elem_name)
            if found is None:
                # Try finding by local name in all elements
                found = self._find_by_local_name(root, elem_name)

            if found is None:
                result.add_error(f"Missing required header element: {description}")

        return result

    def _get_template_ids(self, root: ET.Element) -> set[str]:
        """Extract all templateId root values from document level."""
        template_ids: set[str] = set()

        # Get direct children templateId elements
        for elem in root:
            local_name = elem.tag.replace(f"{{{self.CDA_NS}}}", "")
            if local_name == "templateId":
                root_attr = elem.get("root")
                if root_attr:
                    template_ids.add(root_attr)

        return template_ids

    def _get_section_template_ids(self, root: ET.Element) -> set[str]:
        """Extract all templateId root values from sections."""
        template_ids: set[str] = set()

        # Find all section elements
        for section in root.iter():
            local_name = section.tag.replace(f"{{{self.CDA_NS}}}", "")
            if local_name == "section":
                for child in section:
                    child_name = child.tag.replace(f"{{{self.CDA_NS}}}", "")
                    if child_name == "templateId":
                        root_attr = child.get("root")
                        if root_attr:
                            template_ids.add(root_attr)

        return template_ids

    def _find_by_local_name(self, root: ET.Element, local_name: str) -> ET.Element | None:
        """Find element by local name (ignoring namespace)."""
        for elem in root:
            elem_local = elem.tag.replace(f"{{{self.CDA_NS}}}", "")
            if elem_local == local_name:
                return elem
        return None

    def validate_file(self, file_path: str) -> ValidationResult:
        """Validate a C-CDA document from a file path.

        Args:
            file_path: Path to the XML file.

        Returns:
            ValidationResult with is_valid status, errors, and warnings.
        """
        result = ValidationResult()

        try:
            with open(file_path, encoding="utf-8") as f:
                xml_string = f.read()
        except FileNotFoundError:
            result.add_error(f"File not found: {file_path}")
            return result
        except OSError as e:
            result.add_error(f"Error reading file: {e}")
            return result

        return self.validate(xml_string)

    def validate_batch(
        self, xml_documents: Sequence[tuple[str, str]]
    ) -> dict[str, ValidationResult]:
        """Validate multiple C-CDA documents.

        Args:
            xml_documents: Sequence of (name, xml_string) tuples.

        Returns:
            Dictionary mapping document names to ValidationResults.
        """
        results: dict[str, ValidationResult] = {}

        for name, xml_string in xml_documents:
            results[name] = self.validate(xml_string)

        return results
