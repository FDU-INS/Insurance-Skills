"""FHIR R4 resource models.

Pydantic models for FHIR R4 resources following the specification:
https://www.hl7.org/fhir/R4/
"""

from typing import Any

from pydantic import BaseModel, Field


# Base FHIR types
class CodeableConcept(BaseModel):
    """FHIR CodeableConcept - concept defined by one or more codes."""

    coding: list[dict[str, Any]] = Field(default_factory=list)
    text: str | None = None


class Identifier(BaseModel):
    """FHIR Identifier - unique identifier for resources."""

    system: str | None = None
    value: str
    use: str | None = None


class Reference(BaseModel):
    """FHIR Reference - reference to another resource."""

    reference: str
    display: str | None = None


class HumanName(BaseModel):
    """FHIR HumanName - name of a person."""

    use: str | None = None
    family: str | None = None
    given: list[str] = Field(default_factory=list)
    text: str | None = None


class Period(BaseModel):
    """FHIR Period - time period defined by start and end."""

    start: str | None = None  # ISO 8601 datetime
    end: str | None = None  # ISO 8601 datetime


class Quantity(BaseModel):
    """FHIR Quantity - measured or measurable amount."""

    value: float | None = None
    unit: str | None = None
    system: str | None = None
    code: str | None = None


# FHIR Resources
class PatientResource(BaseModel):
    """FHIR Patient resource.

    https://www.hl7.org/fhir/R4/patient.html
    """

    resourceType: str = "Patient"
    id: str
    identifier: list[Identifier] = Field(default_factory=list)
    name: list[HumanName] = Field(default_factory=list)
    gender: str | None = None  # male | female | other | unknown
    birthDate: str | None = None  # YYYY-MM-DD
    deceasedBoolean: bool | None = None
    deceasedDateTime: str | None = None

    class Config:
        """Pydantic config."""

        populate_by_name = True


class EncounterResource(BaseModel):
    """FHIR Encounter resource.

    https://www.hl7.org/fhir/R4/encounter.html
    """

    resourceType: str = "Encounter"
    id: str
    identifier: list[Identifier] = Field(default_factory=list)
    status: str  # planned | in-progress | finished | cancelled
    class_: CodeableConcept = Field(alias="class")
    type: list[CodeableConcept] = Field(default_factory=list)
    subject: Reference
    period: Period | None = None
    reasonCode: list[CodeableConcept] = Field(default_factory=list)
    hospitalization: dict[str, Any] | None = None

    class Config:
        """Pydantic config."""

        populate_by_name = True


class ConditionResource(BaseModel):
    """FHIR Condition resource.

    https://www.hl7.org/fhir/R4/condition.html
    """

    resourceType: str = "Condition"
    id: str
    identifier: list[Identifier] = Field(default_factory=list)
    clinicalStatus: CodeableConcept | None = None
    verificationStatus: CodeableConcept | None = None
    category: list[CodeableConcept] = Field(default_factory=list)
    code: CodeableConcept
    subject: Reference
    encounter: Reference | None = None
    onsetDateTime: str | None = None
    recordedDate: str | None = None

    class Config:
        """Pydantic config."""

        populate_by_name = True


class ObservationResource(BaseModel):
    """FHIR Observation resource.

    https://www.hl7.org/fhir/R4/observation.html
    """

    resourceType: str = "Observation"
    id: str
    identifier: list[Identifier] = Field(default_factory=list)
    status: str  # registered | preliminary | final | amended
    category: list[CodeableConcept] = Field(default_factory=list)
    code: CodeableConcept
    subject: Reference
    encounter: Reference | None = None
    effectiveDateTime: str | None = None
    issued: str | None = None
    valueQuantity: Quantity | None = None
    valueString: str | None = None

    class Config:
        """Pydantic config."""

        populate_by_name = True


class BundleEntry(BaseModel):
    """FHIR Bundle entry."""

    fullUrl: str | None = None
    resource: dict[str, Any]


class Bundle(BaseModel):
    """FHIR Bundle resource.

    https://www.hl7.org/fhir/R4/bundle.html
    """

    resourceType: str = "Bundle"
    id: str | None = None
    type: str  # document | message | transaction | collection | etc.
    timestamp: str | None = None
    entry: list[BundleEntry] = Field(default_factory=list)

    class Config:
        """Pydantic config."""

        populate_by_name = True


# Code system URIs
class CodeSystems:
    """Standard FHIR and terminology code systems."""

    # Identity systems
    PATIENT_MRN = "http://hospital.example.org/patient-mrn"
    ENCOUNTER_ID = "http://hospital.example.org/encounter-id"

    # Terminology systems
    SNOMED_CT = "http://snomed.info/sct"
    LOINC = "http://loinc.org"
    ICD10 = "http://hl7.org/fhir/sid/icd-10"
    UCUM = "http://unitsofmeasure.org"

    # FHIR code systems
    OBSERVATION_CATEGORY = "http://terminology.hl7.org/CodeSystem/observation-category"
    CONDITION_CLINICAL = "http://terminology.hl7.org/CodeSystem/condition-clinical"
    CONDITION_VERIFICATION = "http://terminology.hl7.org/CodeSystem/condition-ver-status"
    ENCOUNTER_CLASS = "http://terminology.hl7.org/CodeSystem/v3-ActCode"


# Common code system helpers
def create_coding(system: str, code: str, display: str | None = None) -> dict[str, Any]:
    """Create a FHIR coding dict."""
    coding = {"system": system, "code": code}
    if display:
        coding["display"] = display
    return coding


def create_codeable_concept(
    system: str, code: str, display: str | None = None, text: str | None = None
) -> CodeableConcept:
    """Create a FHIR CodeableConcept."""
    return CodeableConcept(
        coding=[create_coding(system, code, display)],
        text=text or display,
    )


# LOINC code mappings for common lab tests
LOINC_MAPPINGS = {
    "hemoglobin": ("718-7", "Hemoglobin [Mass/volume] in Blood"),
    "hematocrit": ("4544-3", "Hematocrit [Volume Fraction] of Blood"),
    "wbc": ("6690-2", "Leukocytes [#/volume] in Blood"),
    "platelets": ("777-3", "Platelets [#/volume] in Blood"),
    "sodium": ("2951-2", "Sodium [Moles/volume] in Serum or Plasma"),
    "potassium": ("2823-3", "Potassium [Moles/volume] in Serum or Plasma"),
    "chloride": ("2075-0", "Chloride [Moles/volume] in Serum or Plasma"),
    "bicarbonate": ("1963-8", "Bicarbonate [Moles/volume] in Serum or Plasma"),
    "bun": ("3094-0", "Urea nitrogen [Mass/volume] in Serum or Plasma"),
    "creatinine": ("2160-0", "Creatinine [Mass/volume] in Serum or Plasma"),
    "glucose": ("2345-7", "Glucose [Mass/volume] in Serum or Plasma"),
    "calcium": ("17861-6", "Calcium [Mass/volume] in Serum or Plasma"),
    "lactate": ("2524-7", "Lactate [Moles/volume] in Blood"),
}

# LOINC codes for vital signs
VITAL_SIGN_LOINC = {
    "heart_rate": ("8867-4", "Heart rate"),
    "respiratory_rate": ("9279-1", "Respiratory rate"),
    "temperature": ("8310-5", "Body temperature"),
    "systolic_bp": ("8480-6", "Systolic blood pressure"),
    "diastolic_bp": ("8462-4", "Diastolic blood pressure"),
    "spo2": ("2708-6", "Oxygen saturation in Arterial blood"),
    "height": ("8302-2", "Body height"),
    "weight": ("29463-7", "Body weight"),
    "bmi": ("39156-5", "Body mass index (BMI)"),
}


def get_loinc_code(test_name: str) -> tuple[str, str] | None:
    """Get LOINC code and display for a lab test.

    Args:
        test_name: Name of the test (normalized)

    Returns:
        Tuple of (code, display) or None if not found
    """
    normalized = test_name.lower().replace(" ", "_").replace("-", "_")

    # Direct lookup
    if normalized in LOINC_MAPPINGS:
        return LOINC_MAPPINGS[normalized]

    # Common aliases
    aliases = {
        "hgb": "hemoglobin",
        "hct": "hematocrit",
        "wbc_count": "wbc",
        "white_blood_cell": "wbc",
        "plt": "platelets",
        "na": "sodium",
        "k": "potassium",
        "cl": "chloride",
        "co2": "bicarbonate",
        "blood_urea_nitrogen": "bun",
        "cr": "creatinine",
        "glu": "glucose",
        "ca": "calcium",
    }

    if normalized in aliases:
        return LOINC_MAPPINGS.get(aliases[normalized])

    return None


def get_vital_loinc(vital_type: str) -> tuple[str, str] | None:
    """Get LOINC code and display for a vital sign.

    Args:
        vital_type: Type of vital sign

    Returns:
        Tuple of (code, display) or None if not found
    """
    normalized = vital_type.lower().replace(" ", "_").replace("-", "_")

    if normalized in VITAL_SIGN_LOINC:
        return VITAL_SIGN_LOINC[normalized]

    # Aliases
    aliases = {
        "hr": "heart_rate",
        "pulse": "heart_rate",
        "rr": "respiratory_rate",
        "temp": "temperature",
        "sbp": "systolic_bp",
        "dbp": "diastolic_bp",
        "o2_sat": "spo2",
        "oxygen_saturation": "spo2",
        "ht": "height",
        "wt": "weight",
    }

    if normalized in aliases:
        return VITAL_SIGN_LOINC.get(aliases[normalized])

    return None
