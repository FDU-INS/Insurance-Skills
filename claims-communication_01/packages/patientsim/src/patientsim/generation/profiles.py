"""Patient-specific profile specifications for PatientSim.

This module extends healthsim-core's ProfileSpecification with patient-specific
schemas for clinical data generation.

Example:
    >>> from patientsim.generation.profiles import PatientProfileSpecification
    >>> spec = PatientProfileSpecification(
    ...     id="diabetic-seniors",
    ...     name="Diabetic Senior Patients",
    ...     demographics=PatientDemographicsSpec(count=100, age={"type": "normal", "mean": 72, "std": 8}),
    ...     clinical=PatientClinicalSpec(
    ...         primary_condition={"code": "E11.9", "name": "Type 2 Diabetes"},
    ...         comorbidities=[{"code": "I10", "name": "Hypertension", "prevalence": 0.65}]
    ...     )
    ... )
"""

from datetime import date
from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator

from healthsim.generation.profile_schema import (
    ClinicalSpec,
    ConditionSpec,
    DemographicsSpec,
    DistributionSpec,
    GenerationSpec,
    ProfileSpecification,
)


class FacilitySpec(BaseModel):
    """Specification for facility/provider assignment.
    
    Attributes:
        facility_type: Type of facility (hospital, clinic, etc.)
        name: Optional specific facility name
        npi: Optional NPI for the facility
    """
    
    facility_type: str = Field(
        "hospital",
        description="Type of facility"
    )
    name: str | None = Field(None, description="Facility name")
    npi: str | None = Field(None, description="Facility NPI")


class EncounterSpec(BaseModel):
    """Specification for encounter patterns.
    
    Attributes:
        encounter_class: Type of encounters to generate
        frequency: How often encounters occur
        duration: Typical encounter duration
    """
    
    encounter_class: Literal["inpatient", "outpatient", "emergency", "observation"] = Field(
        "outpatient",
        description="Type of encounter"
    )
    frequency: DistributionSpec | None = Field(
        None,
        description="Frequency distribution (encounters per year)"
    )
    duration: DistributionSpec | None = Field(
        None,
        description="Duration distribution (hours)"
    )


class PatientClinicalSpec(ClinicalSpec):
    """Patient-specific clinical specification.
    
    Extends base ClinicalSpec with encounter and facility configuration.
    
    Attributes:
        encounter_pattern: Default encounter generation pattern
        default_facility: Default facility for encounters
        problem_list_size: Distribution for number of problems
    """
    
    encounter_pattern: EncounterSpec | None = Field(
        None,
        description="Default encounter pattern"
    )
    default_facility: FacilitySpec | None = Field(
        None,
        description="Default facility assignment"
    )
    problem_list_size: DistributionSpec | None = Field(
        None,
        description="Distribution for number of problems on problem list"
    )


class PatientDemographicsSpec(DemographicsSpec):
    """Patient-specific demographics specification.
    
    Extends base DemographicsSpec with MRN format configuration.
    
    Attributes:
        mrn_prefix: Prefix for generated MRNs
        mrn_length: Length of MRN numeric portion
    """
    
    mrn_prefix: str = Field(
        "MRN",
        description="Prefix for generated MRNs"
    )
    mrn_length: int = Field(
        8,
        description="Length of MRN numeric portion",
        ge=4,
        le=12
    )


class PatientGenerationSpec(GenerationSpec):
    """Patient-specific generation parameters.
    
    Extends base GenerationSpec with patient-specific options.
    
    Attributes:
        include_encounters: Whether to generate encounters
        include_medications: Whether to generate medications
        include_labs: Whether to generate lab results
        include_vitals: Whether to generate vital signs
        include_notes: Whether to generate clinical notes
    """
    
    include_encounters: bool = Field(True, description="Generate encounters")
    include_medications: bool = Field(True, description="Generate medications")
    include_labs: bool = Field(True, description="Generate lab results")
    include_vitals: bool = Field(True, description="Generate vital signs")
    include_notes: bool = Field(False, description="Generate clinical notes")


class PatientProfileSpecification(ProfileSpecification):
    """Complete patient profile specification.
    
    Top-level specification for generating synthetic patient data.
    Combines demographics, clinical attributes, and generation parameters.
    
    Example:
        >>> spec = PatientProfileSpecification(
        ...     id="ed-frequent-flyers",
        ...     name="ED Frequent Flyer Patients",
        ...     description="Patients with >4 ED visits per year",
        ...     demographics=PatientDemographicsSpec(count=50),
        ...     clinical=PatientClinicalSpec(
        ...         primary_condition={"code": "F10.20", "name": "Alcohol dependence"},
        ...         encounter_pattern=EncounterSpec(
        ...             encounter_class="emergency",
        ...             frequency={"type": "normal", "mean": 8, "std": 3, "min": 4}
        ...         )
        ...     )
        ... )
    """
    
    # Override types with patient-specific versions
    demographics: PatientDemographicsSpec = Field(
        default_factory=PatientDemographicsSpec,
        description="Patient demographics specification"
    )
    clinical: PatientClinicalSpec | None = Field(
        None,
        description="Patient clinical specification"
    )
    generation: PatientGenerationSpec = Field(
        default_factory=PatientGenerationSpec,
        description="Generation parameters"
    )
    
    @field_validator("id")
    @classmethod
    def validate_patient_id(cls, v: str) -> str:
        """Ensure profile ID follows naming convention."""
        return v.lower().replace(" ", "-")


# Convenience type aliases
PatientConditionSpec = ConditionSpec
PatientDistributionSpec = DistributionSpec


__all__ = [
    "PatientProfileSpecification",
    "PatientDemographicsSpec",
    "PatientClinicalSpec",
    "PatientGenerationSpec",
    "PatientConditionSpec",
    "PatientDistributionSpec",
    "EncounterSpec",
    "FacilitySpec",
]
