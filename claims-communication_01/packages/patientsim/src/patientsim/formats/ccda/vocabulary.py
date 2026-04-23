"""C-CDA vocabulary utilities.

Provides code system definitions, ICD-10 to SNOMED mappings, and
vocabulary lookup utilities for C-CDA generation.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar


@dataclass
class CodedValue:
    """Represents a coded value with optional translation.

    Attributes:
        code: The code value
        display_name: Human-readable display name
        code_system: Code system OID
        code_system_name: Human-readable code system name
        translation: Optional secondary code (e.g., ICD-10 translation of SNOMED)
    """

    code: str
    display_name: str
    code_system: str
    code_system_name: str
    translation: CodedValue | None = None

    def to_xml(self, xsi_type: str = "CD", include_translation: bool = True) -> str:
        """Generate XML representation of the coded value.

        Args:
            xsi_type: XML schema type (CD, CE, etc.)
            include_translation: Whether to include translation element

        Returns:
            XML string for the value element
        """
        translation_xml = ""
        if include_translation and self.translation:
            translation_xml = (
                f'\n  <translation code="{self.translation.code}" '
                f'codeSystem="{self.translation.code_system}" '
                f'codeSystemName="{self.translation.code_system_name}" '
                f'displayName="{self.translation.display_name}"/>'
            )

        return (
            f'<value xsi:type="{xsi_type}" '
            f'code="{self.code}" '
            f'codeSystem="{self.code_system}" '
            f'codeSystemName="{self.code_system_name}" '
            f'displayName="{self.display_name}">'
            f"{translation_xml}"
            f"</value>"
        )

    def to_code_xml(self) -> str:
        """Generate XML for a code element (not value)."""
        return (
            f'<code code="{self.code}" '
            f'codeSystem="{self.code_system}" '
            f'codeSystemName="{self.code_system_name}" '
            f'displayName="{self.display_name}"/>'
        )


# =============================================================================
# Code System Definitions
# =============================================================================


CODE_SYSTEMS: dict[str, tuple[str, str]] = {
    "SNOMED": ("2.16.840.1.113883.6.96", "SNOMED CT"),
    "RXNORM": ("2.16.840.1.113883.6.88", "RxNorm"),
    "LOINC": ("2.16.840.1.113883.6.1", "LOINC"),
    "ICD10CM": ("2.16.840.1.113883.6.90", "ICD-10-CM"),
    "ICD10": ("2.16.840.1.113883.6.90", "ICD-10-CM"),  # Alias
    "CPT": ("2.16.840.1.113883.6.12", "CPT"),
    "CVX": ("2.16.840.1.113883.12.292", "CVX"),
    "NDC": ("2.16.840.1.113883.6.69", "NDC"),
    "UCUM": ("2.16.840.1.113883.6.8", "UCUM"),
    "HCPCS": ("2.16.840.1.113883.6.285", "HCPCS"),
    "ICD10PCS": ("2.16.840.1.113883.6.4", "ICD-10-PCS"),
    "HL7_ACT_CODE": ("2.16.840.1.113883.5.4", "ActCode"),
    "HL7_ROUTE": ("2.16.840.1.113883.5.112", "RouteOfAdministration"),
    "HL7_GENDER": ("2.16.840.1.113883.5.1", "AdministrativeGender"),
    "HL7_NULL_FLAVOR": ("2.16.840.1.113883.5.1008", "NullFlavor"),
    "HL7_CONFIDENTIALITY": ("2.16.840.1.113883.5.25", "Confidentiality"),
    "HL7_OBSERVATION_INTERP": ("2.16.840.1.113883.5.83", "ObservationInterpretation"),
}


@dataclass
class SNOMEDMapping:
    """Mapping from ICD-10 to SNOMED CT code."""

    icd10_code: str
    icd10_display: str
    snomed_code: str
    snomed_display: str
    domain: str = ""


class CodeSystemRegistry:
    """Registry for code system lookups and ICD-10 to SNOMED mappings.

    Loads mappings from CSV reference files and provides lookup methods.

    Example:
        >>> registry = CodeSystemRegistry()
        >>> registry.load_mappings("/path/to/ccda-snomed-problem-mappings.csv")
        >>> coded = registry.get_snomed_for_icd10("E11.9")
        >>> print(coded.code)  # SNOMED code
        >>> print(coded.translation.code)  # ICD-10 code
    """

    # Default path to mappings file (relative to skills repo)
    DEFAULT_MAPPINGS_PATH: ClassVar[str] = "references/ccda/ccda-snomed-problem-mappings.csv"

    def __init__(self) -> None:
        """Initialize empty registry."""
        self._snomed_mappings: dict[str, SNOMEDMapping] = {}
        self._loaded = False

    def load_mappings(self, csv_path: str | Path | None = None) -> None:
        """Load ICD-10 to SNOMED mappings from CSV file.

        Args:
            csv_path: Path to CSV file. If None, tries default locations.

        Raises:
            FileNotFoundError: If CSV file not found
        """
        if csv_path:
            path = Path(csv_path)
        else:
            # Try to find the mappings file in common locations
            possible_paths = [
                Path(__file__).parent / "data" / "ccda-snomed-problem-mappings.csv",
                Path(__file__).parent.parent.parent.parent.parent
                / "healthsim-skills"
                / "references"
                / "ccda"
                / "ccda-snomed-problem-mappings.csv",
            ]
            path = None
            for p in possible_paths:
                if p.exists():
                    path = p
                    break

            if path is None:
                # Return without loading - mappings will be empty
                self._loaded = True
                return

        if not path.exists():
            raise FileNotFoundError(f"Mappings file not found: {path}")

        self._load_csv(path)
        self._loaded = True

    def _load_csv(self, path: Path) -> None:
        """Load mappings from CSV file."""
        with path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                icd10_code = row.get("icd10_code", "").strip()
                if icd10_code:
                    mapping = SNOMEDMapping(
                        icd10_code=icd10_code,
                        icd10_display=row.get("icd10_display", "").strip(),
                        snomed_code=row.get("snomed_code", "").strip(),
                        snomed_display=row.get("snomed_display", "").strip(),
                        domain=row.get("domain", "").strip(),
                    )
                    self._snomed_mappings[icd10_code] = mapping

    def get_snomed_for_icd10(self, icd10_code: str) -> CodedValue | None:
        """Look up SNOMED code for an ICD-10 code.

        Returns CodedValue with SNOMED as primary and ICD-10 as translation.

        Args:
            icd10_code: ICD-10-CM diagnosis code

        Returns:
            CodedValue with SNOMED primary and ICD-10 translation, or None if not found
        """
        if not self._loaded:
            try:
                self.load_mappings()
            except FileNotFoundError:
                return None

        mapping = self._snomed_mappings.get(icd10_code)
        if not mapping:
            return None

        snomed_oid, snomed_name = CODE_SYSTEMS["SNOMED"]
        icd10_oid, icd10_name = CODE_SYSTEMS["ICD10CM"]

        return CodedValue(
            code=mapping.snomed_code,
            display_name=mapping.snomed_display,
            code_system=snomed_oid,
            code_system_name=snomed_name,
            translation=CodedValue(
                code=mapping.icd10_code,
                display_name=mapping.icd10_display,
                code_system=icd10_oid,
                code_system_name=icd10_name,
            ),
        )

    def get_icd10_only(self, icd10_code: str, display: str) -> CodedValue:
        """Create CodedValue for ICD-10 code without SNOMED mapping.

        Args:
            icd10_code: ICD-10-CM code
            display: Display name

        Returns:
            CodedValue with ICD-10 as primary code
        """
        icd10_oid, icd10_name = CODE_SYSTEMS["ICD10CM"]
        return CodedValue(
            code=icd10_code,
            display_name=display,
            code_system=icd10_oid,
            code_system_name=icd10_name,
        )

    def get_coded_value(
        self,
        code: str,
        display: str,
        system_name: str,
        translation_code: str | None = None,
        translation_display: str | None = None,
        translation_system: str | None = None,
    ) -> CodedValue:
        """Create a CodedValue with optional translation.

        Args:
            code: Primary code
            display: Primary display name
            system_name: Code system name (key in CODE_SYSTEMS)
            translation_code: Optional secondary code
            translation_display: Optional secondary display
            translation_system: Optional secondary system name

        Returns:
            CodedValue with specified codes
        """
        system_oid, system_display = get_code_system(system_name)

        translation = None
        if translation_code and translation_system:
            trans_oid, trans_display = get_code_system(translation_system)
            translation = CodedValue(
                code=translation_code,
                display_name=translation_display or "",
                code_system=trans_oid,
                code_system_name=trans_display,
            )

        return CodedValue(
            code=code,
            display_name=display,
            code_system=system_oid,
            code_system_name=system_display,
            translation=translation,
        )

    def get_mappings_by_domain(self, domain: str) -> list[SNOMEDMapping]:
        """Get all mappings for a specific clinical domain.

        Args:
            domain: Domain name (e.g., "diabetes", "heart-failure", "ckd")

        Returns:
            List of SNOMEDMapping objects for the domain
        """
        if not self._loaded:
            try:
                self.load_mappings()
            except FileNotFoundError:
                return []

        return [m for m in self._snomed_mappings.values() if m.domain == domain]

    def has_mapping(self, icd10_code: str) -> bool:
        """Check if a SNOMED mapping exists for an ICD-10 code.

        Args:
            icd10_code: ICD-10-CM code

        Returns:
            True if mapping exists
        """
        if not self._loaded:
            try:
                self.load_mappings()
            except FileNotFoundError:
                return False

        return icd10_code in self._snomed_mappings

    @property
    def mapping_count(self) -> int:
        """Return number of loaded mappings."""
        return len(self._snomed_mappings)


# =============================================================================
# Utility Functions
# =============================================================================


def get_code_system(name: str) -> tuple[str, str]:
    """Get code system OID and display name by name.

    Args:
        name: Code system name (e.g., "SNOMED", "LOINC", "RXNORM")

    Returns:
        Tuple of (OID, display_name)

    Raises:
        KeyError: If code system name not found
    """
    name_upper = name.upper().replace("-", "").replace("_", "")
    if name_upper in CODE_SYSTEMS:
        return CODE_SYSTEMS[name_upper]

    # Try common variations
    variations = {
        "SNOMEDCT": "SNOMED",
        "ICD10CM": "ICD10CM",
        "ICD10": "ICD10CM",
        "ICD": "ICD10CM",
    }
    if name_upper in variations:
        return CODE_SYSTEMS[variations[name_upper]]

    raise KeyError(f"Unknown code system: {name}")


def create_loinc_code(code: str, display: str) -> CodedValue:
    """Create a LOINC CodedValue.

    Args:
        code: LOINC code
        display: Display name

    Returns:
        CodedValue for LOINC
    """
    oid, name = CODE_SYSTEMS["LOINC"]
    return CodedValue(code=code, display_name=display, code_system=oid, code_system_name=name)


def create_snomed_code(code: str, display: str) -> CodedValue:
    """Create a SNOMED CT CodedValue.

    Args:
        code: SNOMED code
        display: Display name

    Returns:
        CodedValue for SNOMED CT
    """
    oid, name = CODE_SYSTEMS["SNOMED"]
    return CodedValue(code=code, display_name=display, code_system=oid, code_system_name=name)


def create_rxnorm_code(code: str, display: str) -> CodedValue:
    """Create an RxNorm CodedValue.

    Args:
        code: RxNorm code
        display: Display name

    Returns:
        CodedValue for RxNorm
    """
    oid, name = CODE_SYSTEMS["RXNORM"]
    return CodedValue(code=code, display_name=display, code_system=oid, code_system_name=name)


def create_cvx_code(code: str, display: str) -> CodedValue:
    """Create a CVX (vaccine) CodedValue.

    Args:
        code: CVX code
        display: Display name

    Returns:
        CodedValue for CVX
    """
    oid, name = CODE_SYSTEMS["CVX"]
    return CodedValue(code=code, display_name=display, code_system=oid, code_system_name=name)


def create_cpt_code(code: str, display: str) -> CodedValue:
    """Create a CPT CodedValue.

    Args:
        code: CPT code
        display: Display name

    Returns:
        CodedValue for CPT
    """
    oid, name = CODE_SYSTEMS["CPT"]
    return CodedValue(code=code, display_name=display, code_system=oid, code_system_name=name)


# =============================================================================
# LOINC Lab Panel Definitions
# =============================================================================


@dataclass
class LabPanelDefinition:
    """Definition of a laboratory panel with component tests."""

    panel_name: str
    panel_loinc: str
    tests: list[tuple[str, str, str]]  # List of (loinc_code, test_name, units)


# Common lab panels with their LOINC codes
LAB_PANELS: dict[str, LabPanelDefinition] = {
    "BMP": LabPanelDefinition(
        panel_name="Basic Metabolic Panel",
        panel_loinc="24323-8",
        tests=[
            ("2345-7", "Glucose", "mg/dL"),
            ("3094-0", "BUN", "mg/dL"),
            ("2160-0", "Creatinine", "mg/dL"),
            ("2951-2", "Sodium", "mmol/L"),
            ("2823-3", "Potassium", "mmol/L"),
            ("2075-0", "Chloride", "mmol/L"),
            ("2028-9", "CO2", "mmol/L"),
            ("17861-6", "Calcium", "mg/dL"),
        ],
    ),
    "CMP": LabPanelDefinition(
        panel_name="Comprehensive Metabolic Panel",
        panel_loinc="24322-0",
        tests=[
            ("2345-7", "Glucose", "mg/dL"),
            ("3094-0", "BUN", "mg/dL"),
            ("2160-0", "Creatinine", "mg/dL"),
            ("2951-2", "Sodium", "mmol/L"),
            ("2823-3", "Potassium", "mmol/L"),
            ("2075-0", "Chloride", "mmol/L"),
            ("2028-9", "CO2", "mmol/L"),
            ("17861-6", "Calcium", "mg/dL"),
            ("1751-7", "Albumin", "g/dL"),
            ("2885-2", "Total Protein", "g/dL"),
            ("1742-6", "ALT", "U/L"),
            ("1920-8", "AST", "U/L"),
            ("6768-6", "Alkaline Phosphatase", "U/L"),
            ("1975-2", "Total Bilirubin", "mg/dL"),
        ],
    ),
    "LIPID": LabPanelDefinition(
        panel_name="Lipid Panel",
        panel_loinc="24331-1",
        tests=[
            ("2093-3", "Total Cholesterol", "mg/dL"),
            ("2085-9", "HDL Cholesterol", "mg/dL"),
            ("13457-7", "LDL Cholesterol Calculated", "mg/dL"),
            ("2571-8", "Triglycerides", "mg/dL"),
        ],
    ),
    "CBC": LabPanelDefinition(
        panel_name="Complete Blood Count",
        panel_loinc="58410-2",
        tests=[
            ("6690-2", "WBC", "10*3/uL"),
            ("789-8", "RBC", "10*6/uL"),
            ("718-7", "Hemoglobin", "g/dL"),
            ("4544-3", "Hematocrit", "%"),
            ("777-3", "Platelets", "10*3/uL"),
            ("787-2", "MCV", "fL"),
            ("785-6", "MCH", "pg"),
            ("786-4", "MCHC", "g/dL"),
        ],
    ),
}


def get_lab_panel(panel_code: str) -> LabPanelDefinition | None:
    """Get lab panel definition by code.

    Args:
        panel_code: Panel code (e.g., "BMP", "CMP", "LIPID", "CBC")

    Returns:
        LabPanelDefinition or None if not found
    """
    return LAB_PANELS.get(panel_code.upper())


# =============================================================================
# Vital Signs LOINC Codes
# =============================================================================


VITAL_SIGNS_LOINC: dict[str, tuple[str, str, str]] = {
    "systolic_bp": ("8480-6", "Systolic blood pressure", "mm[Hg]"),
    "diastolic_bp": ("8462-4", "Diastolic blood pressure", "mm[Hg]"),
    "heart_rate": ("8867-4", "Heart rate", "/min"),
    "respiratory_rate": ("9279-1", "Respiratory rate", "/min"),
    "temperature_f": ("8310-5", "Body temperature", "[degF]"),
    "temperature_c": ("8310-5", "Body temperature", "Cel"),
    "spo2": ("2708-6", "Oxygen saturation", "%"),
    "height_in": ("8302-2", "Body height", "[in_i]"),
    "height_cm": ("8302-2", "Body height", "cm"),
    "weight_lb": ("29463-7", "Body weight", "[lb_av]"),
    "weight_kg": ("29463-7", "Body weight", "kg"),
    "bmi": ("39156-5", "Body mass index", "kg/m2"),
    "head_circumference": ("9843-4", "Head Occipital-frontal circumference", "cm"),
}


def get_vital_loinc(vital_type: str) -> tuple[str, str, str] | None:
    """Get LOINC code info for a vital sign type.

    Args:
        vital_type: Vital sign type (e.g., "systolic_bp", "heart_rate")

    Returns:
        Tuple of (loinc_code, display_name, unit) or None
    """
    return VITAL_SIGNS_LOINC.get(vital_type.lower())
