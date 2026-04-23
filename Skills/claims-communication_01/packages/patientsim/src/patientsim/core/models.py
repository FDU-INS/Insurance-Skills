"""Core data models for PatientSim.

This module defines the internal representation of patient data, clinical encounters,
and related healthcare information. All models use Pydantic v2 for validation and
are format-agnostic (they can be exported to HL7v2, FHIR, CDA, etc.).
"""

from datetime import date, datetime
from enum import Enum
from typing import Any

from healthsim.person import Gender, Person  # noqa: F401 - Gender re-exported
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class EncounterClass(str, Enum):
    """Type of encounter."""

    INPATIENT = "I"
    OUTPATIENT = "O"
    EMERGENCY = "E"
    URGENT_CARE = "U"
    OBSERVATION = "OBS"


class EncounterStatus(str, Enum):
    """Status of the encounter."""

    PLANNED = "planned"
    ARRIVED = "arrived"
    IN_PROGRESS = "in-progress"
    ON_HOLD = "on-hold"
    FINISHED = "finished"
    CANCELLED = "cancelled"


class DiagnosisType(str, Enum):
    """Type of diagnosis."""

    ADMITTING = "admitting"
    WORKING = "working"
    FINAL = "final"
    DIFFERENTIAL = "differential"


class MedicationStatus(str, Enum):
    """Status of medication."""

    ACTIVE = "active"
    COMPLETED = "completed"
    STOPPED = "stopped"
    ON_HOLD = "on-hold"


class Patient(Person):
    """Core patient model with demographics and identifiers.

    Extends healthsim.person.Person with healthcare-specific fields.
    This is the central model that other models reference.

    Attributes:
        mrn: Medical Record Number (primary identifier in healthcare context)
        ssn: Social Security Number (optional)
        race: Race/ethnicity
        language: Preferred language code
        created_at: When this record was created

    Example:
        >>> patient = Patient(
        ...     id="patient-001",
        ...     mrn="MRN12345",
        ...     name=PersonName(given_name="John", family_name="Doe"),
        ...     birth_date=date(1980, 1, 15),
        ...     gender=Gender.MALE
        ... )
        >>> patient.age  # Calculated property from Person
        45
    """

    # Healthcare-specific identifiers
    mrn: str = Field(..., description="Medical Record Number", min_length=1)
    ssn: str | None = Field(None, description="Social Security Number", pattern=r"^\d{9}$")

    # Clinical demographics
    race: str | None = Field(None, description="Race/ethnicity")
    language: str = Field("en", description="Preferred language code")

    # Metadata
    created_at: datetime = Field(
        default_factory=datetime.now, description="When this record was created"
    )

    model_config = ConfigDict(use_enum_values=True)


class Encounter(BaseModel):
    """Clinical encounter (visit, admission, etc.).

    Represents a single interaction between a patient and the healthcare system.
    This could be an ED visit, inpatient admission, outpatient appointment, etc.

    Example:
        >>> encounter = Encounter(
        ...     encounter_id="V12345",
        ...     patient_mrn="MRN12345",
        ...     class_code=EncounterClass.EMERGENCY,
        ...     status=EncounterStatus.FINISHED,
        ...     admission_time=datetime(2025, 1, 26, 14, 30),
        ...     discharge_time=datetime(2025, 1, 26, 18, 45)
        ... )
    """

    encounter_id: str = Field(..., description="Unique encounter identifier", min_length=1)
    patient_mrn: str = Field(..., description="Patient MRN this encounter is for", min_length=1)

    class_code: EncounterClass = Field(..., description="Type of encounter")
    status: EncounterStatus = Field(..., description="Current status")

    # Timing
    admission_time: datetime = Field(..., description="When patient was admitted/arrived")
    discharge_time: datetime | None = Field(None, description="When patient was discharged")

    # Location
    facility: str | None = Field(None, description="Facility/hospital name")
    department: str | None = Field(None, description="Department/unit")
    room: str | None = Field(None, description="Room number")
    bed: str | None = Field(None, description="Bed identifier")

    # Clinical
    chief_complaint: str | None = Field(None, description="Patient's chief complaint")
    admitting_diagnosis: str | None = Field(None, description="Diagnosis on admission")
    discharge_disposition: str | None = Field(None, description="Where patient went after")

    # Providers
    attending_physician: str | None = Field(None, description="Attending physician ID")
    admitting_physician: str | None = Field(None, description="Admitting physician ID")

    @field_validator("discharge_time")
    @classmethod
    def discharge_after_admission(cls, v: datetime | None, info: Any) -> datetime | None:
        """Validate discharge time is after admission time."""
        if v and "admission_time" in info.data and v < info.data["admission_time"]:
            raise ValueError("Discharge time cannot be before admission time")
        return v

    @property
    def length_of_stay_hours(self) -> float | None:
        """Calculate length of stay in hours."""
        if not self.discharge_time:
            return None
        delta = self.discharge_time - self.admission_time
        return delta.total_seconds() / 3600

    model_config = ConfigDict(use_enum_values=True)


class Diagnosis(BaseModel):
    """Patient diagnosis/condition.

    Represents a single diagnosis with ICD-10 coding. Can be linked to
    an encounter or be part of the patient's problem list.

    Example:
        >>> diagnosis = Diagnosis(
        ...     code="E11.9",
        ...     description="Type 2 diabetes mellitus without complications",
        ...     type=DiagnosisType.FINAL,
        ...     diagnosed_date=date(2024, 6, 15)
        ... )
    """

    code: str = Field(..., description="ICD-10 diagnosis code", min_length=1)
    description: str = Field(..., description="Diagnosis description", min_length=1)
    type: DiagnosisType = Field(DiagnosisType.FINAL, description="Type of diagnosis")

    patient_mrn: str = Field(..., description="Patient MRN", min_length=1)
    encounter_id: str | None = Field(None, description="Associated encounter if applicable")

    diagnosed_date: date = Field(..., description="When diagnosis was made")
    resolved_date: date | None = Field(None, description="When condition resolved")

    @field_validator("resolved_date")
    @classmethod
    def resolved_after_diagnosed(cls, v: date | None, info: Any) -> date | None:
        """Validate resolved date is after diagnosed date."""
        if v and "diagnosed_date" in info.data and v < info.data["diagnosed_date"]:
            raise ValueError("Resolved date cannot be before diagnosed date")
        return v

    model_config = ConfigDict(use_enum_values=True)


class Procedure(BaseModel):
    """Clinical procedure performed on patient.

    Represents a procedure with ICD-10-PCS or CPT coding.

    Example:
        >>> procedure = Procedure(
        ...     code="3E0G76Z",
        ...     description="Insertion of central venous catheter",
        ...     patient_mrn="MRN12345",
        ...     performed_date=datetime(2025, 1, 26, 15, 30)
        ... )
    """

    code: str = Field(..., description="ICD-10-PCS or CPT procedure code", min_length=1)
    description: str = Field(..., description="Procedure description", min_length=1)

    patient_mrn: str = Field(..., description="Patient MRN", min_length=1)
    encounter_id: str | None = Field(None, description="Associated encounter if applicable")

    performed_date: datetime = Field(..., description="When procedure was performed")
    performer: str | None = Field(None, description="Clinician who performed procedure")
    location: str | None = Field(None, description="Where procedure was performed")

    @field_validator("performed_date")
    @classmethod
    def performed_date_not_future(cls, v: datetime) -> datetime:
        """Validate procedure date is not in the future."""
        if v > datetime.now():
            raise ValueError("Procedure date cannot be in the future")
        return v


class Medication(BaseModel):
    """Medication order or administration.

    Represents a medication with dosage, route, and timing information.

    Example:
        >>> medication = Medication(
        ...     name="Metformin",
        ...     code="860975",  # RxNorm code
        ...     dose="500 mg",
        ...     route="PO",
        ...     frequency="BID",
        ...     patient_mrn="MRN12345",
        ...     start_date=datetime(2024, 6, 15, 8, 0)
        ... )
    """

    name: str = Field(..., description="Medication name", min_length=1)
    code: str | None = Field(None, description="RxNorm or NDC code")

    dose: str = Field(..., description="Dose (e.g., '500 mg', '10 units')", min_length=1)
    route: str = Field(..., description="Route of administration (PO, IV, IM, etc.)", min_length=1)
    frequency: str = Field(
        ..., description="Frequency (QD, BID, TID, QID, PRN, etc.)", min_length=1
    )

    patient_mrn: str = Field(..., description="Patient MRN", min_length=1)
    encounter_id: str | None = Field(None, description="Associated encounter if applicable")

    start_date: datetime = Field(..., description="When medication started")
    end_date: datetime | None = Field(None, description="When medication stopped")
    status: MedicationStatus = Field(MedicationStatus.ACTIVE, description="Current status")

    prescriber: str | None = Field(None, description="Prescribing clinician")
    indication: str | None = Field(None, description="Reason for medication")

    @field_validator("end_date")
    @classmethod
    def end_after_start(cls, v: datetime | None, info: Any) -> datetime | None:
        """Validate end date is after start date."""
        if v and "start_date" in info.data and v < info.data["start_date"]:
            raise ValueError("End date cannot be before start date")
        return v

    model_config = ConfigDict(use_enum_values=True)


class LabResult(BaseModel):
    """Laboratory test result.

    Represents a single lab test with LOINC coding and result value.

    Example:
        >>> lab = LabResult(
        ...     test_name="Glucose",
        ...     loinc_code="2345-7",
        ...     value="95",
        ...     unit="mg/dL",
        ...     reference_range="70-100",
        ...     patient_mrn="MRN12345",
        ...     collected_time=datetime(2025, 1, 26, 8, 0),
        ...     resulted_time=datetime(2025, 1, 26, 10, 30)
        ... )
    """

    test_name: str = Field(..., description="Name of the test", min_length=1)
    loinc_code: str | None = Field(None, description="LOINC code for the test")

    value: str = Field(..., description="Test result value", min_length=1)
    unit: str | None = Field(None, description="Unit of measure")
    reference_range: str | None = Field(None, description="Normal reference range")

    abnormal_flag: str | None = Field(None, description="Abnormal flag (H, L, HH, LL, A, etc.)")

    patient_mrn: str = Field(..., description="Patient MRN", min_length=1)
    encounter_id: str | None = Field(None, description="Associated encounter if applicable")

    collected_time: datetime = Field(..., description="When specimen was collected")
    resulted_time: datetime | None = Field(None, description="When result was finalized")

    performing_lab: str | None = Field(None, description="Lab that performed the test")
    ordering_provider: str | None = Field(None, description="Provider who ordered the test")

    @field_validator("resulted_time")
    @classmethod
    def resulted_after_collected(cls, v: datetime | None, info: Any) -> datetime | None:
        """Validate resulted time is after collected time."""
        if v and "collected_time" in info.data and v < info.data["collected_time"]:
            raise ValueError("Resulted time cannot be before collected time")
        return v


class VitalSign(BaseModel):
    """Vital sign observation.

    Represents a set of vital signs taken at a specific time.

    Example:
        >>> vitals = VitalSign(
        ...     patient_mrn="MRN12345",
        ...     observation_time=datetime(2025, 1, 26, 14, 0),
        ...     temperature=98.6,
        ...     heart_rate=72,
        ...     respiratory_rate=16,
        ...     systolic_bp=120,
        ...     diastolic_bp=80,
        ...     spo2=98
        ... )
    """

    patient_mrn: str = Field(..., description="Patient MRN", min_length=1)
    encounter_id: str | None = Field(None, description="Associated encounter if applicable")

    observation_time: datetime = Field(..., description="When vitals were taken")

    # Vital sign values (all optional as not all may be taken together)
    temperature: float | None = Field(None, description="Temperature in Fahrenheit", ge=90, le=110)
    heart_rate: int | None = Field(None, description="Heart rate in bpm", ge=0, le=300)
    respiratory_rate: int | None = Field(
        None, description="Respiratory rate per minute", ge=0, le=100
    )
    systolic_bp: int | None = Field(None, description="Systolic blood pressure", ge=0, le=300)
    diastolic_bp: int | None = Field(None, description="Diastolic blood pressure", ge=0, le=200)
    spo2: int | None = Field(None, description="Oxygen saturation percentage", ge=0, le=100)
    height_cm: float | None = Field(None, description="Height in centimeters", ge=0, le=300)
    weight_kg: float | None = Field(None, description="Weight in kilograms", ge=0, le=500)

    @property
    def blood_pressure(self) -> str | None:
        """Get blood pressure in standard format (120/80)."""
        if self.systolic_bp is not None and self.diastolic_bp is not None:
            return f"{self.systolic_bp}/{self.diastolic_bp}"
        return None

    @property
    def bmi(self) -> float | None:
        """Calculate BMI if height and weight are available."""
        if self.height_cm is not None and self.weight_kg is not None:
            height_m = self.height_cm / 100
            return round(self.weight_kg / (height_m**2), 1)
        return None

    @model_validator(mode="after")
    def validate_bp_pair(self) -> "VitalSign":
        """Validate that if one BP value is present, the other should be too."""
        has_systolic = self.systolic_bp is not None
        has_diastolic = self.diastolic_bp is not None

        if has_systolic != has_diastolic:
            raise ValueError("Both systolic and diastolic BP must be provided together")

        if has_systolic and has_diastolic and self.systolic_bp <= self.diastolic_bp:  # type: ignore
            raise ValueError("Systolic BP must be greater than diastolic BP")

        return self


class ClinicalNote(BaseModel):
    """Clinical note or documentation.

    Represents a text note in the patient's chart.

    Example:
        >>> note = ClinicalNote(
        ...     note_type="Progress Note",
        ...     patient_mrn="MRN12345",
        ...     encounter_id="V12345",
        ...     note_time=datetime(2025, 1, 26, 10, 0),
        ...     text="Patient reports improvement in symptoms...",
        ...     author="Dr. Jane Smith"
        ... )
    """

    note_type: str = Field(
        ...,
        description="Type of note (Progress Note, H&P, Discharge Summary, etc.)",
        min_length=1,
    )

    patient_mrn: str = Field(..., description="Patient MRN", min_length=1)
    encounter_id: str | None = Field(None, description="Associated encounter if applicable")

    note_time: datetime = Field(..., description="When note was written")
    text: str = Field(..., description="Note content", min_length=1)

    author: str | None = Field(None, description="Clinician who wrote the note")
    service: str | None = Field(None, description="Clinical service (Medicine, Surgery, etc.)")

    @field_validator("note_time")
    @classmethod
    def note_time_not_future(cls, v: datetime) -> datetime:
        """Validate note time is not in the future."""
        if v > datetime.now():
            raise ValueError("Note time cannot be in the future")
        return v
