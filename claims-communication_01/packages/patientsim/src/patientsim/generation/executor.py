"""Patient profile executor for PatientSim.

This module provides the execution engine that transforms a PatientProfileSpecification
into actual Patient entities with clinical data.

Example:
    >>> from patientsim.generation import PatientProfileExecutor, PatientProfileSpecification
    >>> spec = PatientProfileSpecification(
    ...     id="test-patients",
    ...     demographics=PatientDemographicsSpec(count=10)
    ... )
    >>> executor = PatientProfileExecutor(spec)
    >>> result = executor.execute()
    >>> print(f"Generated {len(result.patients)} patients")
"""

from dataclasses import dataclass, field
from datetime import date, datetime
import random
from typing import Any

from healthsim.generation.profile_executor import (
    HierarchicalSeedManager,
    ProfileExecutor,
    ValidationReport,
)
from healthsim.generation.distributions import create_distribution
from healthsim.person import PersonName

from patientsim.core.models import (
    Diagnosis,
    DiagnosisType,
    Encounter,
    EncounterClass,
    EncounterStatus,
    LabResult,
    Medication,
    MedicationStatus,
    Patient,
    VitalSign,
)
from patientsim.generation.profiles import (
    PatientClinicalSpec,
    PatientDemographicsSpec,
    PatientGenerationSpec,
    PatientProfileSpecification,
)


@dataclass
class GeneratedPatient:
    """Container for a generated patient with all clinical data.
    
    Attributes:
        patient: The core Patient entity
        encounters: List of clinical encounters
        diagnoses: List of diagnoses
        medications: List of medications
        lab_results: List of lab results
        vital_signs: List of vital sign observations
    """
    
    patient: Patient
    encounters: list[Encounter] = field(default_factory=list)
    diagnoses: list[Diagnosis] = field(default_factory=list)
    medications: list[Medication] = field(default_factory=list)
    lab_results: list[LabResult] = field(default_factory=list)
    vital_signs: list[VitalSign] = field(default_factory=list)
    
    @property
    def mrn(self) -> str:
        """Get patient MRN."""
        return self.patient.mrn
    
    @property
    def first_name(self) -> str:
        """Get patient first name."""
        return self.patient.name.given_name if self.patient.name else ""
    
    @property
    def last_name(self) -> str:
        """Get patient last name."""
        return self.patient.name.family_name if self.patient.name else ""
    
    @property
    def gender(self) -> str:
        """Get patient gender."""
        return self.patient.gender or ""
    
    @property
    def date_of_birth(self) -> date | None:
        """Get patient date of birth."""
        return self.patient.birth_date
    
    @property
    def age(self) -> int | None:
        """Get patient age."""
        return self.patient.age
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "patient": self.patient.model_dump(),
            "encounters": [e.model_dump() for e in self.encounters],
            "diagnoses": [d.model_dump() for d in self.diagnoses],
            "medications": [m.model_dump() for m in self.medications],
            "lab_results": [l.model_dump() for l in self.lab_results],
            "vital_signs": [v.model_dump() for v in self.vital_signs],
        }


@dataclass
class PatientExecutionResult:
    """Result of patient profile execution.
    
    Attributes:
        patients: List of generated patients with clinical data
        spec_id: ID of the executed specification
        seed: Seed used for generation (for reproducibility)
        validation: Validation results
    """
    
    spec_id: str = ""
    seed: int = 0
    patients: list[GeneratedPatient] = field(default_factory=list)
    validation: ValidationReport = field(default_factory=ValidationReport)
    
    @property
    def count(self) -> int:
        """Number of patients generated."""
        return len(self.patients)
    
    @property
    def profile_id(self) -> str:
        """Alias for spec_id for consistency with other products."""
        return self.spec_id
    
    @property
    def entities(self) -> list[Patient]:
        """Get just the Patient entities."""
        return [p.patient for p in self.patients]
    
    def summary(self) -> dict[str, Any]:
        """Generate summary statistics."""
        if not self.patients:
            return {"count": 0}
        
        ages = [p.patient.age for p in self.patients if p.patient.age]
        
        return {
            "count": self.count,
            "spec_id": self.spec_id,
            "seed": self.seed,
            "validation_passed": self.validation.passed,
            "avg_age": sum(ages) / len(ages) if ages else None,
            "total_encounters": sum(len(p.encounters) for p in self.patients),
            "total_diagnoses": sum(len(p.diagnoses) for p in self.patients),
            "total_medications": sum(len(p.medications) for p in self.patients),
        }


class PatientProfileExecutor(ProfileExecutor):
    """Executes patient profile specifications to generate synthetic patients.
    
    This executor implements a two-phase generation approach:
    1. Generate base demographics from spec distributions
    2. Apply clinical attributes, conditions, and related data
    
    Example:
        >>> spec = PatientProfileSpecification(
        ...     id="diabetic-cohort",
        ...     demographics=PatientDemographicsSpec(count=100),
        ...     clinical=PatientClinicalSpec(
        ...         primary_condition={"code": "E11.9", "name": "Type 2 Diabetes"}
        ...     )
        ... )
        >>> executor = PatientProfileExecutor(spec)
        >>> result = executor.execute()
        >>> assert result.validation.passed
    """
    
    def __init__(
        self,
        spec: PatientProfileSpecification,
        seed: int | None = None,
    ):
        """Initialize the executor.
        
        Args:
            spec: Patient profile specification
            seed: Optional seed for reproducibility
        """
        super().__init__(spec, seed)
        self.patient_spec = spec
        self.demographics = spec.demographics
        self.clinical = spec.clinical
        self.generation = spec.generation
    
    def execute(
        self,
        dry_run: bool = False,
        count_override: int | None = None,
    ) -> PatientExecutionResult:
        """Execute the profile specification.
        
        Args:
            dry_run: If True, generate only a small sample (max 5)
            count_override: Override the count from spec
        
        Returns:
            PatientExecutionResult containing generated patients
        """
        result = PatientExecutionResult(
            spec_id=self.patient_spec.id,
            seed=self.seed,
        )
        
        # Determine count
        count = self.generation.count
        if count_override is not None:
            count = count_override
        if dry_run:
            count = min(count, 5)
        
        for i in range(count):
            try:
                patient = self._generate_patient(i)
                result.patients.append(patient)
            except Exception as e:
                result.validation.errors.append(
                    f"Failed to generate patient {i}: {str(e)}"
                )
        
        # Validate results
        self._validate_result(result)
        
        return result
    
    def _generate_patient(self, index: int) -> GeneratedPatient:
        """Generate a single patient with clinical data.
        
        Args:
            index: Patient index (for seed derivation)
            
        Returns:
            GeneratedPatient with all clinical data
        """
        # Get RNG for this patient
        rng = self.seed_manager.get_entity_rng(index)
        
        # Generate base patient
        patient = self._generate_base_patient(index, rng)
        
        # Create container
        generated = GeneratedPatient(patient=patient)
        
        # Add clinical data if specified
        if self.clinical:
            self._add_clinical_data(generated, rng)
        
        return generated
    
    def _generate_base_patient(
        self,
        index: int,
        rng: 'random.Random',
    ) -> Patient:
        """Generate base patient demographics.
        
        Args:
            index: Patient index
            rng: Random number generator for this patient
            
        Returns:
            Patient entity with demographics
        """
        from faker import Faker
        faker = Faker()
        faker.seed_instance(rng.randint(0, 2**31 - 1))
        
        # Generate age
        if self.demographics.age:
            age_dist = create_distribution(self.demographics.age.model_dump())
            age = int(age_dist.sample(rng=rng))
        else:
            age = rng.randint(18, 85)
        
        # Calculate birth date from age
        today = date.today()
        birth_year = today.year - age
        birth_date = date(birth_year, rng.randint(1, 12), rng.randint(1, 28))
        
        # Generate gender
        if self.demographics.gender:
            gender_dist = create_distribution(self.demographics.gender.model_dump())
            gender = gender_dist.sample(rng=rng)
        else:
            gender = rng.choice(["M", "F"])
        
        # Generate name based on gender
        if gender == "M":
            first_name = faker.first_name_male()
        else:
            first_name = faker.first_name_female()
        last_name = faker.last_name()
        
        # Generate MRN
        mrn_num = str(rng.randint(10**(self.demographics.mrn_length-1), 10**self.demographics.mrn_length - 1))
        mrn = f"{self.demographics.mrn_prefix}{mrn_num}"
        
        # Generate patient ID
        patient_id = f"patient-{self.patient_spec.id}-{index:06d}"
        
        return Patient(
            id=patient_id,
            mrn=mrn,
            name=PersonName(given_name=first_name, family_name=last_name),
            birth_date=birth_date,
            gender=gender,
            ssn=faker.ssn().replace("-", "") if rng.random() < 0.8 else None,
            race=rng.choice(["White", "Black", "Asian", "Hispanic", "Other"]),
            language="en",
        )
    
    def _add_clinical_data(
        self,
        generated: GeneratedPatient,
        rng: 'random.Random',
    ) -> None:
        """Add clinical data to generated patient.
        
        Args:
            generated: GeneratedPatient to populate
            rng: Random number generator for this patient
        """
        if not self.clinical:
            return
        
        patient = generated.patient
        
        # Add primary condition as diagnosis
        if self.clinical.primary_condition:
            cond = self.clinical.primary_condition
            diagnosis = Diagnosis(
                code=cond.code,
                description=cond.description or cond.code,
                type=DiagnosisType.FINAL,
                patient_mrn=patient.mrn,
                diagnosed_date=date.today().replace(
                    year=date.today().year - rng.randint(1, 5)
                ),
            )
            generated.diagnoses.append(diagnosis)
        
        # Add comorbidities based on prevalence
        if self.clinical.comorbidities:
            for comorbidity in self.clinical.comorbidities:
                prevalence = comorbidity.prevalence or 0.5
                if rng.random() < prevalence:
                    diagnosis = Diagnosis(
                        code=comorbidity.code,
                        description=comorbidity.description or comorbidity.code,
                        type=DiagnosisType.FINAL,
                        patient_mrn=patient.mrn,
                        diagnosed_date=date.today().replace(
                            year=date.today().year - rng.randint(1, 3)
                        ),
                    )
                    generated.diagnoses.append(diagnosis)
    
    def _validate_result(self, result: PatientExecutionResult) -> None:
        """Validate execution results against spec tolerances.
        
        Args:
            result: Result to validate
        """
        expected = self.generation.count
        actual = result.count
        tolerance = getattr(self.generation, 'tolerance', 0.1)  # Default 10%
        
        if actual > 0 and abs(actual - expected) / expected > tolerance:
            result.validation.warnings.append(
                f"Count {actual} differs from expected {expected} by more than {tolerance*100}%"
            )
        
        # Note: validation.passed is a computed property based on errors


__all__ = [
    "PatientProfileExecutor",
    "PatientExecutionResult",
    "GeneratedPatient",
]
