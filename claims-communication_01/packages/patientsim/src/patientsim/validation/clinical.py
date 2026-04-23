"""Clinical validators for medical plausibility.

This module validates clinical coherence and medical plausibility of patient data,
ensuring diagnoses, medications, labs, and procedures make clinical sense together.
"""

from patientsim.core.models import Diagnosis, Gender, LabResult, Medication, Patient, VitalSign
from patientsim.validation.base import BaseValidator, ValidationResult, ValidationSeverity


class AgeAppropriatenessValidator(BaseValidator):
    """Validates age appropriateness of diagnoses and conditions."""

    # Age ranges for conditions that are typically age-specific
    PEDIATRIC_CONDITIONS = {
        "J45.909",  # Asthma (can occur at any age, but onset often pediatric)
    }

    GERIATRIC_CONDITIONS = {
        "I25.10",  # CAD
        "I50.9",  # Heart failure
        "N18.3",  # CKD stage 3
        "N18.4",  # CKD stage 4
    }

    def validate_diagnosis_age(self, diagnosis: Diagnosis, patient: Patient) -> ValidationResult:
        """Validate diagnosis is age-appropriate.

        Args:
            diagnosis: Diagnosis to validate
            patient: Patient with the diagnosis

        Returns:
            ValidationResult with any issues found
        """
        result = ValidationResult(valid=True)
        age = patient.age

        # Geriatric conditions in young patients
        if diagnosis.code in self.GERIATRIC_CONDITIONS and age < 40:
            result.add_issue(
                code="CLIN_001",
                message=f"Geriatric condition '{diagnosis.description}' in young patient (age {age})",
                severity=ValidationSeverity.WARNING,
                field_path="code",
                context={"age": age, "diagnosis_code": diagnosis.code},
            )

        return result

    def validate(
        self, diagnosis: Diagnosis | None = None, patient: Patient | None = None
    ) -> ValidationResult:
        """Validate age appropriateness.

        Args:
            diagnosis: Optional diagnosis to validate
            patient: Optional patient (required if diagnosis provided)

        Returns:
            ValidationResult with any issues found
        """
        result = ValidationResult(valid=True)

        if diagnosis and patient:
            result.merge(self.validate_diagnosis_age(diagnosis, patient))

        return result


class GenderAppropriatenessValidator(BaseValidator):
    """Validates gender appropriateness of diagnoses and procedures."""

    # Conditions that are gender-specific
    # Pregnancy, gynecological conditions would go here
    # Not in our current reference data, but framework is ready
    FEMALE_ONLY_CONDITIONS: set[str] = set()

    # Prostate conditions would go here
    # Not in our current reference data, but framework is ready
    MALE_ONLY_CONDITIONS: set[str] = set()

    def validate_diagnosis_gender(self, diagnosis: Diagnosis, patient: Patient) -> ValidationResult:
        """Validate diagnosis is gender-appropriate.

        Args:
            diagnosis: Diagnosis to validate
            patient: Patient with the diagnosis

        Returns:
            ValidationResult with any issues found
        """
        result = ValidationResult(valid=True)

        # Check female-only conditions
        if diagnosis.code in self.FEMALE_ONLY_CONDITIONS and patient.gender != Gender.FEMALE:
            result.add_issue(
                code="CLIN_002",
                message=f"Female-only condition '{diagnosis.description}' in non-female patient",
                severity=ValidationSeverity.ERROR,
                field_path="code",
                context={"gender": patient.gender, "diagnosis_code": diagnosis.code},
            )

        # Check male-only conditions
        if diagnosis.code in self.MALE_ONLY_CONDITIONS and patient.gender != Gender.MALE:
            result.add_issue(
                code="CLIN_003",
                message=f"Male-only condition '{diagnosis.description}' in non-male patient",
                severity=ValidationSeverity.ERROR,
                field_path="code",
                context={"gender": patient.gender, "diagnosis_code": diagnosis.code},
            )

        return result

    def validate(
        self, diagnosis: Diagnosis | None = None, patient: Patient | None = None
    ) -> ValidationResult:
        """Validate gender appropriateness.

        Args:
            diagnosis: Optional diagnosis to validate
            patient: Optional patient (required if diagnosis provided)

        Returns:
            ValidationResult with any issues found
        """
        result = ValidationResult(valid=True)

        if diagnosis and patient:
            result.merge(self.validate_diagnosis_gender(diagnosis, patient))

        return result


class ClinicalCoherenceValidator(BaseValidator):
    """Validates clinical coherence between diagnoses, meds, and labs."""

    # Medication to diagnosis mappings
    MEDICATION_INDICATIONS = {
        "Metformin": ["E11.9", "E11.65"],  # Diabetes medications
        "Insulin Glargine": ["E10.9", "E11.9", "E11.65"],
        "Lisinopril": ["I10", "I11.9", "I50.9"],  # Hypertension/heart failure
        "Amlodipine": ["I10", "I11.9"],
        "Hydrochlorothiazide": ["I10", "I11.9"],
        "Metoprolol": ["I10", "I11.9", "I25.10", "I48.91"],  # HTN, CAD, AFib
        "Azithromycin": ["J18.9", "A49.9"],  # Infections
        "Ceftriaxone": ["J18.9", "A41.9", "A49.9"],
        "Vancomycin": ["A41.9", "A49.9"],
    }

    # Lab tests relevant to conditions
    CONDITION_LABS = {
        "E11.9": ["Glucose", "HbA1c"],  # Diabetes
        "E11.65": ["Glucose", "HbA1c"],
        "E10.9": ["Glucose", "HbA1c"],
        "I50.9": ["BNP"],  # Heart failure
        "N18.3": ["Creatinine", "BUN"],  # CKD
        "N18.4": ["Creatinine", "BUN"],
        "J18.9": ["WBC", "CRP"],  # Pneumonia
        "A41.9": ["WBC", "CRP"],  # Sepsis
    }

    def validate_medication_indication(
        self, medication: Medication, diagnoses: list[Diagnosis]
    ) -> ValidationResult:
        """Validate medication has appropriate indication.

        Args:
            medication: Medication to validate
            diagnoses: List of patient's diagnoses

        Returns:
            ValidationResult with any issues found
        """
        result = ValidationResult(valid=True)

        # Check if medication has known indications
        if medication.name in self.MEDICATION_INDICATIONS:
            expected_codes = self.MEDICATION_INDICATIONS[medication.name]
            diagnosis_codes = [d.code for d in diagnoses]

            # Check if patient has any of the expected diagnoses
            has_indication = any(code in diagnosis_codes for code in expected_codes)

            if not has_indication:
                result.add_issue(
                    code="CLIN_004",
                    message=f"Medication '{medication.name}' prescribed without typical indication",
                    severity=ValidationSeverity.INFO,
                    field_path="name",
                    context={
                        "medication": medication.name,
                        "expected_diagnoses": expected_codes,
                        "actual_diagnoses": diagnosis_codes,
                    },
                )

        return result

    def validate_labs_for_condition(
        self, diagnosis: Diagnosis, labs: list[LabResult]
    ) -> ValidationResult:
        """Validate appropriate labs are ordered for condition.

        Args:
            diagnosis: Diagnosis to check
            labs: List of lab results

        Returns:
            ValidationResult with any issues found
        """
        result = ValidationResult(valid=True)

        # Check if condition has expected labs
        if diagnosis.code in self.CONDITION_LABS:
            expected_labs = self.CONDITION_LABS[diagnosis.code]
            lab_names = [lab.test_name for lab in labs]

            # Info message if typical labs are missing (not an error, just informational)
            missing_labs = [lab for lab in expected_labs if lab not in lab_names]

            if missing_labs:
                result.add_issue(
                    code="CLIN_005",
                    message=f"Diagnosis '{diagnosis.description}' without typical labs: {', '.join(missing_labs)}",
                    severity=ValidationSeverity.INFO,
                    field_path="code",
                    context={
                        "diagnosis": diagnosis.code,
                        "missing_labs": missing_labs,
                        "available_labs": lab_names,
                    },
                )

        return result

    def validate(
        self,
        medication: Medication | None = None,
        diagnosis: Diagnosis | None = None,
        diagnoses: list[Diagnosis] | None = None,
        labs: list[LabResult] | None = None,
    ) -> ValidationResult:
        """Validate clinical coherence.

        Args:
            medication: Optional medication to validate (requires diagnoses)
            diagnosis: Optional diagnosis to validate (requires labs)
            diagnoses: Optional list of diagnoses
            labs: Optional list of labs

        Returns:
            ValidationResult with any issues found
        """
        result = ValidationResult(valid=True)

        if medication and diagnoses:
            result.merge(self.validate_medication_indication(medication, diagnoses))

        if diagnosis and labs:
            result.merge(self.validate_labs_for_condition(diagnosis, labs))

        return result


class VitalSignPlausibilityValidator(BaseValidator):
    """Validates vital signs are medically plausible."""

    def validate_vitals(self, vitals: VitalSign, _patient: Patient) -> ValidationResult:
        """Validate vital signs are plausible.

        Args:
            vitals: Vital signs to validate
            _patient: Patient the vitals belong to (reserved for future use)

        Returns:
            ValidationResult with any issues found
        """
        result = ValidationResult(valid=True)

        # Critically abnormal values that would be life-threatening
        if vitals.temperature and vitals.temperature > 106.0:
            result.add_issue(
                code="CLIN_006",
                message=f"Critically high temperature: {vitals.temperature}°F",
                severity=ValidationSeverity.WARNING,
                field_path="temperature",
                context={"temperature": vitals.temperature},
            )

        if vitals.temperature and vitals.temperature < 92.0:
            result.add_issue(
                code="CLIN_007",
                message=f"Critically low temperature: {vitals.temperature}°F",
                severity=ValidationSeverity.WARNING,
                field_path="temperature",
                context={"temperature": vitals.temperature},
            )

        if vitals.heart_rate and vitals.heart_rate > 180:
            result.add_issue(
                code="CLIN_008",
                message=f"Critically high heart rate: {vitals.heart_rate} bpm",
                severity=ValidationSeverity.WARNING,
                field_path="heart_rate",
                context={"heart_rate": vitals.heart_rate},
            )

        if vitals.heart_rate and vitals.heart_rate < 40:
            result.add_issue(
                code="CLIN_009",
                message=f"Critically low heart rate: {vitals.heart_rate} bpm",
                severity=ValidationSeverity.WARNING,
                field_path="heart_rate",
                context={"heart_rate": vitals.heart_rate},
            )

        if vitals.spo2 and vitals.spo2 < 85:
            result.add_issue(
                code="CLIN_010",
                message=f"Critically low oxygen saturation: {vitals.spo2}%",
                severity=ValidationSeverity.WARNING,
                field_path="spo2",
                context={"spo2": vitals.spo2},
            )

        # Check for impossible combinations
        if vitals.systolic_bp and vitals.diastolic_bp:
            pulse_pressure = vitals.systolic_bp - vitals.diastolic_bp

            if pulse_pressure < 20:
                result.add_issue(
                    code="CLIN_011",
                    message=f"Unusually narrow pulse pressure: {pulse_pressure} mmHg",
                    severity=ValidationSeverity.WARNING,
                    field_path="blood_pressure",
                    context={
                        "systolic": vitals.systolic_bp,
                        "diastolic": vitals.diastolic_bp,
                        "pulse_pressure": pulse_pressure,
                    },
                )

            if pulse_pressure > 100:
                result.add_issue(
                    code="CLIN_012",
                    message=f"Unusually wide pulse pressure: {pulse_pressure} mmHg",
                    severity=ValidationSeverity.INFO,
                    field_path="blood_pressure",
                    context={
                        "systolic": vitals.systolic_bp,
                        "diastolic": vitals.diastolic_bp,
                        "pulse_pressure": pulse_pressure,
                    },
                )

        # BMI warnings
        if vitals.bmi:
            if vitals.bmi < 16:
                result.add_issue(
                    code="CLIN_013",
                    message=f"Severely underweight BMI: {vitals.bmi}",
                    severity=ValidationSeverity.WARNING,
                    field_path="bmi",
                    context={"bmi": vitals.bmi},
                )

            if vitals.bmi > 40:
                result.add_issue(
                    code="CLIN_014",
                    message=f"Severely obese BMI: {vitals.bmi}",
                    severity=ValidationSeverity.INFO,
                    field_path="bmi",
                    context={"bmi": vitals.bmi},
                )

        return result

    def validate(self, vitals: VitalSign, patient: Patient) -> ValidationResult:
        """Validate vital sign plausibility.

        Args:
            vitals: Vital signs to validate
            patient: Patient the vitals belong to

        Returns:
            ValidationResult with any issues found
        """
        return self.validate_vitals(vitals, patient)
