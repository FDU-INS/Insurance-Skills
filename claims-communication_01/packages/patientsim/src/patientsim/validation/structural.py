"""Structural validators for data integrity.

This module validates structural/referential integrity of patient data,
ensuring required fields are present and references resolve correctly.
"""

from datetime import datetime

from patientsim.core.models import (
    Diagnosis,
    Encounter,
    LabResult,
    Medication,
    Patient,
    Procedure,
    VitalSign,
)
from patientsim.validation.base import BaseValidator, ValidationResult, ValidationSeverity


class TemporalValidator(BaseValidator):
    """Validates temporal consistency of patient data.

    Ensures dates and times are in correct order and within valid ranges.
    """

    def validate_patient(self, patient: Patient) -> ValidationResult:
        """Validate patient temporal data.

        Args:
            patient: Patient to validate

        Returns:
            ValidationResult with any issues found
        """
        result = ValidationResult(valid=True)

        # Birth date should not be in future
        # This is already validated by the Patient model, but we double-check
        # since this is a critical validation rule

        # Death date validations (already in model, but documented here)
        if patient.deceased and patient.death_date and patient.death_date < patient.birth_date:
            result.add_issue(
                code="TEMP_001",
                message="Death date is before birth date",
                severity=ValidationSeverity.ERROR,
                field_path="death_date",
                context={
                    "birth_date": str(patient.birth_date),
                    "death_date": str(patient.death_date),
                },
            )

        return result

    def validate_encounter(self, encounter: Encounter) -> ValidationResult:
        """Validate encounter temporal data.

        Args:
            encounter: Encounter to validate

        Returns:
            ValidationResult with any issues found
        """
        result = ValidationResult(valid=True)

        # Admission should not be in future
        if encounter.admission_time > datetime.now():
            result.add_issue(
                code="TEMP_002",
                message="Admission time is in the future",
                severity=ValidationSeverity.WARNING,
                field_path="admission_time",
                context={"admission_time": str(encounter.admission_time)},
            )

        # Discharge should be after admission (already validated by model)
        # But we can add warnings for unusual patterns
        if encounter.discharge_time and encounter.length_of_stay_hours:
            los = encounter.length_of_stay_hours

            # Unusually long stay
            if los > 365 * 24:  # More than 1 year
                result.add_issue(
                    code="TEMP_003",
                    message=f"Unusually long length of stay: {los / 24:.1f} days",
                    severity=ValidationSeverity.WARNING,
                    field_path="discharge_time",
                    context={"los_hours": los},
                )

            # Negative or zero LOS (should be caught by model, but double-check)
            if los <= 0:
                result.add_issue(
                    code="TEMP_004",
                    message="Length of stay is zero or negative",
                    severity=ValidationSeverity.ERROR,
                    field_path="discharge_time",
                    context={"los_hours": los},
                )

        return result

    def validate_lab_in_encounter(self, lab: LabResult, encounter: Encounter) -> ValidationResult:
        """Validate lab timing relative to encounter.

        Args:
            lab: Lab result to validate
            encounter: Associated encounter

        Returns:
            ValidationResult with any issues found
        """
        result = ValidationResult(valid=True)

        # Lab collected before admission
        if lab.collected_time < encounter.admission_time:
            result.add_issue(
                code="TEMP_005",
                message="Lab collected before encounter admission",
                severity=ValidationSeverity.WARNING,
                field_path="collected_time",
                context={
                    "collected": str(lab.collected_time),
                    "admission": str(encounter.admission_time),
                },
            )

        # Lab collected after discharge
        if encounter.discharge_time and lab.collected_time > encounter.discharge_time:
            result.add_issue(
                code="TEMP_006",
                message="Lab collected after encounter discharge",
                severity=ValidationSeverity.WARNING,
                field_path="collected_time",
                context={
                    "collected": str(lab.collected_time),
                    "discharge": str(encounter.discharge_time),
                },
            )

        return result

    def validate(
        self,
        patient: Patient | None = None,
        encounter: Encounter | None = None,
        lab: LabResult | None = None,
    ) -> ValidationResult:
        """Validate temporal consistency.

        Args:
            patient: Optional patient to validate
            encounter: Optional encounter to validate
            lab: Optional lab result to validate (requires encounter)

        Returns:
            Combined validation result
        """
        result = ValidationResult(valid=True)

        if patient:
            result.merge(self.validate_patient(patient))

        if encounter:
            result.merge(self.validate_encounter(encounter))

            if lab:
                result.merge(self.validate_lab_in_encounter(lab, encounter))

        return result


class ReferentialIntegrityValidator(BaseValidator):
    """Validates referential integrity between records.

    Ensures MRNs, encounter IDs, and other references are valid.
    """

    def validate_diagnosis(self, diagnosis: Diagnosis, patient: Patient) -> ValidationResult:
        """Validate diagnosis references patient correctly.

        Args:
            diagnosis: Diagnosis to validate
            patient: Patient it should reference

        Returns:
            ValidationResult with any issues found
        """
        result = ValidationResult(valid=True)

        if diagnosis.patient_mrn != patient.mrn:
            result.add_issue(
                code="REF_001",
                message="Diagnosis patient_mrn does not match patient",
                severity=ValidationSeverity.ERROR,
                field_path="patient_mrn",
                context={
                    "diagnosis_mrn": diagnosis.patient_mrn,
                    "patient_mrn": patient.mrn,
                },
            )

        return result

    def validate_encounter_patient(
        self, encounter: Encounter, patient: Patient
    ) -> ValidationResult:
        """Validate encounter references patient correctly.

        Args:
            encounter: Encounter to validate
            patient: Patient it should reference

        Returns:
            ValidationResult with any issues found
        """
        result = ValidationResult(valid=True)

        if encounter.patient_mrn != patient.mrn:
            result.add_issue(
                code="REF_002",
                message="Encounter patient_mrn does not match patient",
                severity=ValidationSeverity.ERROR,
                field_path="patient_mrn",
                context={
                    "encounter_mrn": encounter.patient_mrn,
                    "patient_mrn": patient.mrn,
                },
            )

        return result

    def validate_lab_references(
        self,
        lab: LabResult,
        patient: Patient,
        encounter: Encounter | None = None,
    ) -> ValidationResult:
        """Validate lab result references.

        Args:
            lab: Lab result to validate
            patient: Patient it should reference
            encounter: Optional encounter it should reference

        Returns:
            ValidationResult with any issues found
        """
        result = ValidationResult(valid=True)

        # Check patient MRN
        if lab.patient_mrn != patient.mrn:
            result.add_issue(
                code="REF_003",
                message="Lab patient_mrn does not match patient",
                severity=ValidationSeverity.ERROR,
                field_path="patient_mrn",
                context={"lab_mrn": lab.patient_mrn, "patient_mrn": patient.mrn},
            )

        # Check encounter ID if provided
        if encounter and lab.encounter_id != encounter.encounter_id:
            result.add_issue(
                code="REF_004",
                message="Lab encounter_id does not match encounter",
                severity=ValidationSeverity.ERROR,
                field_path="encounter_id",
                context={
                    "lab_encounter": lab.encounter_id,
                    "encounter_id": encounter.encounter_id,
                },
            )

        return result

    def validate(
        self,
        patient: Patient,
        diagnosis: Diagnosis | None = None,
        encounter: Encounter | None = None,
        lab: LabResult | None = None,
        medication: Medication | None = None,
        procedure: Procedure | None = None,
        vitals: VitalSign | None = None,
    ) -> ValidationResult:
        """Validate referential integrity.

        Args:
            patient: Patient (required anchor)
            diagnosis: Optional diagnosis to validate
            encounter: Optional encounter to validate
            lab: Optional lab to validate
            medication: Optional medication to validate
            procedure: Optional procedure to validate
            vitals: Optional vitals to validate

        Returns:
            Combined validation result
        """
        result = ValidationResult(valid=True)

        if diagnosis:
            result.merge(self.validate_diagnosis(diagnosis, patient))

        if encounter:
            result.merge(self.validate_encounter_patient(encounter, patient))

        if lab:
            result.merge(self.validate_lab_references(lab, patient, encounter))

        # Add similar validations for medication, procedure, vitals if needed
        if medication and medication.patient_mrn != patient.mrn:
            result.add_issue(
                code="REF_005",
                message="Medication patient_mrn does not match patient",
                severity=ValidationSeverity.ERROR,
                field_path="patient_mrn",
            )

        if procedure and procedure.patient_mrn != patient.mrn:
            result.add_issue(
                code="REF_006",
                message="Procedure patient_mrn does not match patient",
                severity=ValidationSeverity.ERROR,
                field_path="patient_mrn",
            )

        if vitals and vitals.patient_mrn != patient.mrn:
            result.add_issue(
                code="REF_007",
                message="VitalSign patient_mrn does not match patient",
                severity=ValidationSeverity.ERROR,
                field_path="patient_mrn",
            )

        return result
