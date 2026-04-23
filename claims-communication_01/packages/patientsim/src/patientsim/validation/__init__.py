"""Validation framework for patient data.

This module provides validators to ensure patient data is structurally sound
and clinically plausible. Validators check temporal consistency, referential
integrity, and medical appropriateness.

Example:
    >>> from patientsim.validation import validate_patient_record, ValidationSeverity
    >>> from patientsim.core import PatientGenerator
    >>>
    >>> gen = PatientGenerator(seed=42)
    >>> patient = gen.generate_patient()
    >>> encounter = gen.generate_encounter(patient)
    >>> diagnosis = gen.generate_diagnosis(patient, encounter)
    >>>
    >>> result = validate_patient_record(
    ...     patient=patient,
    ...     encounters=[encounter],
    ...     diagnoses=[diagnosis]
    ... )
    >>>
    >>> if result.valid:
    ...     print("Patient record is valid!")
    >>> else:
    ...     for error in result.errors:
    ...         print(f"Error: {error}")
"""

from patientsim.core.models import (
    Diagnosis,
    Encounter,
    LabResult,
    Medication,
    Patient,
    Procedure,
    VitalSign,
)
from patientsim.validation.base import (
    BaseValidator,
    CompositeValidator,
    StructuralValidator,
    ValidationIssue,
    ValidationMessage,
    ValidationResult,
    ValidationSeverity,
    Validator,
)
from patientsim.validation.clinical import (
    AgeAppropriatenessValidator,
    ClinicalCoherenceValidator,
    GenderAppropriatenessValidator,
    VitalSignPlausibilityValidator,
)
from patientsim.validation.structural import (
    ReferentialIntegrityValidator,
    TemporalValidator,
)

__all__ = [
    # Base classes (from healthsim-core)
    "BaseValidator",
    "Validator",  # Alias for BaseValidator
    "ValidationIssue",
    "ValidationMessage",  # Alias for ValidationIssue
    "ValidationResult",
    "ValidationSeverity",
    # New validators from healthsim-core v0.2.0
    "CompositeValidator",
    "StructuralValidator",
    # Structural validators (PatientSim-specific)
    "TemporalValidator",
    "ReferentialIntegrityValidator",
    # Clinical validators
    "AgeAppropriatenessValidator",
    "GenderAppropriatenessValidator",
    "ClinicalCoherenceValidator",
    "VitalSignPlausibilityValidator",
    # Convenience function
    "validate_patient_record",
]


def validate_patient_record(
    patient: Patient,
    encounters: list[Encounter] | None = None,
    diagnoses: list[Diagnosis] | None = None,
    medications: list[Medication] | None = None,
    labs: list[LabResult] | None = None,
    procedures: list[Procedure] | None = None,
    vitals: list[VitalSign] | None = None,
) -> ValidationResult:
    """Validate a complete patient record.

    This convenience function runs all validators on a patient record
    and returns a combined result.

    Args:
        patient: The patient to validate (required)
        encounters: List of encounters to validate
        diagnoses: List of diagnoses to validate
        medications: List of medications to validate
        labs: List of lab results to validate
        procedures: List of procedures to validate
        vitals: List of vital signs to validate

    Returns:
        ValidationResult with all issues found across all validators

    Example:
        >>> from patientsim.validation import validate_patient_record
        >>> from patientsim.core import PatientGenerator
        >>>
        >>> gen = PatientGenerator(seed=42)
        >>> patient = gen.generate_patient()
        >>> result = validate_patient_record(patient)
        >>> print(result.valid)
        True
    """
    result = ValidationResult(valid=True)

    # Initialize validators
    temporal = TemporalValidator()
    ref_integrity = ReferentialIntegrityValidator()
    age_appropriate = AgeAppropriatenessValidator()
    gender_appropriate = GenderAppropriatenessValidator()
    clinical_coherence = ClinicalCoherenceValidator()
    vitals_plausibility = VitalSignPlausibilityValidator()

    # Validate patient
    result.merge(temporal.validate_patient(patient))

    # Validate encounters
    if encounters:
        for encounter in encounters:
            result.merge(temporal.validate_encounter(encounter))
            result.merge(ref_integrity.validate_encounter_patient(encounter, patient))

    # Validate diagnoses
    if diagnoses:
        for diagnosis in diagnoses:
            result.merge(ref_integrity.validate_diagnosis(diagnosis, patient))
            result.merge(age_appropriate.validate(diagnosis=diagnosis, patient=patient))
            result.merge(gender_appropriate.validate(diagnosis=diagnosis, patient=patient))

            # Check labs for this diagnosis
            if labs:
                result.merge(clinical_coherence.validate_labs_for_condition(diagnosis, labs))

    # Validate medications
    if medications and diagnoses:
        for medication in medications:
            result.merge(ref_integrity.validate(patient=patient, medication=medication))
            result.merge(clinical_coherence.validate_medication_indication(medication, diagnoses))

    # Validate labs
    if labs:
        for lab in labs:
            # Find matching encounter if any
            matching_encounter = None
            if encounters and lab.encounter_id:
                matching_encounter = next(
                    (e for e in encounters if e.encounter_id == lab.encounter_id), None
                )

            result.merge(ref_integrity.validate_lab_references(lab, patient, matching_encounter))

            if matching_encounter:
                result.merge(temporal.validate_lab_in_encounter(lab, matching_encounter))

    # Validate procedures
    if procedures:
        for procedure in procedures:
            result.merge(ref_integrity.validate(patient=patient, procedure=procedure))

    # Validate vitals
    if vitals:
        for vital in vitals:
            result.merge(ref_integrity.validate(patient=patient, vitals=vital))
            result.merge(vitals_plausibility.validate(vital, patient))

    return result
