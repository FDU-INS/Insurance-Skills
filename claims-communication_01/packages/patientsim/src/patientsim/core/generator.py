"""Patient data generation utilities.

This module provides the PatientGenerator class for creating synthetic patient data
with medically plausible relationships between diagnoses, labs, vitals, and medications.
"""

from datetime import date, datetime, timedelta
from typing import Any

from healthsim.generation import AgeDistribution, BaseGenerator
from healthsim.person import Address, ContactInfo, PersonName

from patientsim.core.models import (
    Diagnosis,
    DiagnosisType,
    Encounter,
    EncounterClass,
    EncounterStatus,
    Gender,
    LabResult,
    Medication,
    MedicationStatus,
    Patient,
    VitalSign,
)
from patientsim.core.reference_data import (
    COMMON_DIAGNOSES,
    LAB_TESTS,
    MEDICATIONS,
    VITAL_RANGES,
    ICD10Code,
    get_lab_test,
    get_medication,
)


class PatientGenerator(BaseGenerator):
    """Generate synthetic patient data with medically plausible relationships.

    This generator creates complete patient records including demographics, encounters,
    diagnoses, labs, vitals, and medications. The generated data is internally consistent
    and follows medical logic (e.g., diabetic patients have abnormal glucose levels).

    Extends healthsim.generation.BaseGenerator for reproducibility support.

    Example:
        >>> gen = PatientGenerator(seed=42)
        >>> patient = gen.generate_patient()
        >>> print(f"{patient.full_name}, {patient.age} years old")
        >>> patient = gen.generate_patient(age_range=(65, 85), gender=Gender.FEMALE)
    """

    def __init__(self, seed: int | None = None, locale: str = "en_US") -> None:
        """Initialize the patient generator.

        Args:
            seed: Random seed for reproducible generation. Same seed produces same data.
            locale: Faker locale for demographic data (default: en_US).
        """
        super().__init__(seed=seed, locale=locale)
        # Store seed for compatibility with existing code
        self.seed = seed

    def generate_patient(
        self,
        age_range: tuple[int, int] | None = None,
        gender: Gender | None = None,
        age_distribution: AgeDistribution | None = None,
    ) -> Patient:
        """Generate a single patient with demographics.

        Args:
            age_range: Tuple of (min_age, max_age). If None, uses (18, 85).
            gender: Specific gender to use. If None, random.
            age_distribution: Optional AgeDistribution for weighted age sampling.
                             If provided, overrides age_range.

        Returns:
            Patient instance with complete demographics.

        Example:
            >>> gen = PatientGenerator()
            >>> patient = gen.generate_patient(age_range=(50, 70), gender=Gender.MALE)
            >>> # Using age distribution
            >>> dist = AgeDistribution.adult()
            >>> patient = gen.generate_patient(age_distribution=dist)
        """
        # Determine age
        if age_distribution is not None:
            age = age_distribution.sample()
        else:
            age_min, age_max = age_range if age_range else (18, 85)
            age = self.random_int(age_min, age_max)

        birth_date = date.today() - timedelta(days=age * 365 + self.random_int(0, 364))

        # Gender
        if gender is None:
            gender = self.random_choice(list(Gender))

        # Name based on gender
        if gender == Gender.MALE:
            given_name = self.faker.first_name_male()
        elif gender == Gender.FEMALE:
            given_name = self.faker.first_name_female()
        else:
            given_name = self.faker.first_name()

        family_name = self.faker.last_name()
        middle_name = self.faker.first_name()[0] if self.random_bool(0.5) else None

        # Build PersonName
        name = PersonName(
            given_name=given_name,
            middle_name=middle_name,
            family_name=family_name,
        )

        # Identifiers
        patient_id = f"patient-{self.random_int(100000, 999999)}"
        mrn = f"MRN{self.random_int(100000, 999999)}"
        ssn = f"{self.random_int(100, 999)}{self.random_int(10, 99)}{self.random_int(1000, 9999)}"

        # Build Address
        address = Address(
            street_address=self.faker.street_address(),
            city=self.faker.city(),
            state=self.faker.state_abbr(),
            postal_code=self.faker.postcode(),
            country="US",
        )

        # Build ContactInfo
        contact = ContactInfo(
            phone=self.faker.phone_number(),
            email=self.faker.email(),
        )

        # Race/ethnicity
        races = ["White", "Black or African American", "Asian", "Hispanic or Latino", "Other"]
        race = self.random_choice(races)

        return Patient(
            id=patient_id,
            mrn=mrn,
            ssn=ssn,
            name=name,
            birth_date=birth_date,
            gender=gender,
            address=address,
            contact=contact,
            race=race,
        )

    def generate_encounter(
        self,
        patient: Patient,
        encounter_class: EncounterClass | None = None,
        admission_date: datetime | None = None,
        length_of_stay_days: int | None = None,
    ) -> Encounter:
        """Generate a clinical encounter for a patient.

        Args:
            patient: The patient this encounter is for.
            encounter_class: Type of encounter. If None, random.
            admission_date: Specific admission time. If None, recent past.
            length_of_stay_days: How many days. If None, varies by encounter type.

        Returns:
            Encounter instance with logical admission/discharge times.

        Example:
            >>> gen = PatientGenerator()
            >>> patient = gen.generate_patient()
            >>> encounter = gen.generate_encounter(patient, EncounterClass.INPATIENT)
        """
        # Encounter type
        if encounter_class is None:
            encounter_class = self.random_choice(list(EncounterClass))

        # Admission time (within past 30 days if not specified)
        if admission_date is None:
            days_ago = self.random_int(0, 30)
            admission_time = datetime.now() - timedelta(days=days_ago, hours=self.random_int(0, 23))
        else:
            admission_time = admission_date

        # Length of stay based on encounter type
        if length_of_stay_days is None:
            if encounter_class == EncounterClass.INPATIENT:
                length_of_stay_days = self.random_int(2, 10)
            elif encounter_class == EncounterClass.EMERGENCY:
                length_of_stay_days = 0  # Same day
            elif encounter_class == EncounterClass.OBSERVATION:
                length_of_stay_days = self.random_int(1, 2)
            else:
                length_of_stay_days = 0  # Outpatient

        # Discharge time
        if length_of_stay_days > 0:
            discharge_time = admission_time + timedelta(
                days=length_of_stay_days, hours=self.random_int(8, 18)
            )
        else:
            discharge_time = admission_time + timedelta(hours=self.random_int(2, 8))

        # Status based on timing
        if discharge_time < datetime.now():
            status = EncounterStatus.FINISHED
        else:
            status = self.random_choice([EncounterStatus.IN_PROGRESS, EncounterStatus.ARRIVED])

        # Generate encounter ID
        encounter_id = f"V{self.random_int(100000, 999999)}"

        # Random facility and location
        facilities = ["General Hospital", "Memorial Medical Center", "University Hospital"]
        departments = ["Emergency", "ICU", "Medical Floor", "Surgical Floor", "Observation"]
        facility = self.random_choice(facilities)
        department = (
            self.random_choice(departments) if encounter_class == EncounterClass.INPATIENT else None
        )

        return Encounter(
            encounter_id=encounter_id,
            patient_mrn=patient.mrn,
            class_code=encounter_class,
            status=status,
            admission_time=admission_time,
            discharge_time=discharge_time if status == EncounterStatus.FINISHED else None,
            facility=facility,
            department=department,
            room=f"{self.random_int(100, 999)}" if department else None,
            bed=f"{self.random_choice(['A', 'B', 'C', 'D'])}" if department else None,
        )

    def generate_diagnosis(
        self,
        patient: Patient,
        encounter: Encounter | None = None,
        category: str | None = None,
        diagnosis_code: ICD10Code | None = None,
    ) -> Diagnosis:
        """Generate a diagnosis for a patient.

        Args:
            patient: The patient this diagnosis is for.
            encounter: Optional encounter to link to.
            category: Diagnosis category (diabetes, cardiac, etc.). If None, random.
            diagnosis_code: Specific ICD10Code to use. If None, random from category.

        Returns:
            Diagnosis instance with ICD-10 coding.

        Example:
            >>> gen = PatientGenerator()
            >>> patient = gen.generate_patient()
            >>> diagnosis = gen.generate_diagnosis(patient, category="diabetes")
        """
        # Select diagnosis
        selected_code: ICD10Code
        if diagnosis_code is None:
            if category:
                available = [d for d in COMMON_DIAGNOSES if d.category == category]
                if not available:
                    raise ValueError(f"No diagnoses found for category: {category}")
                selected_code = self.random_choice(available)
            else:
                selected_code = self.random_choice(COMMON_DIAGNOSES)
        else:
            selected_code = diagnosis_code

        # Diagnosis date (within past year)
        days_ago = self.random_int(1, 365)
        diagnosed_date = date.today() - timedelta(days=days_ago)

        # Type
        diag_type = self.random_choice(list(DiagnosisType))

        return Diagnosis(
            code=selected_code.code,
            description=selected_code.description,
            type=diag_type,
            patient_mrn=patient.mrn,
            encounter_id=encounter.encounter_id if encounter else None,
            diagnosed_date=diagnosed_date,
        )

    def generate_lab_result(
        self,
        patient: Patient,
        encounter: Encounter | None = None,
        test_name: str | None = None,
        make_abnormal: bool = False,
    ) -> LabResult:
        """Generate a lab result for a patient.

        Args:
            patient: The patient this lab is for.
            encounter: Optional encounter to link to.
            test_name: Specific test name. If None, random.
            make_abnormal: If True, generate abnormal value.

        Returns:
            LabResult instance with realistic values.

        Example:
            >>> gen = PatientGenerator()
            >>> patient = gen.generate_patient()
            >>> lab = gen.generate_lab_result(patient, test_name="Glucose", make_abnormal=True)
        """
        # Select test
        if test_name:
            test = get_lab_test(test_name)
            if not test:
                raise ValueError(f"Unknown lab test: {test_name}")
        else:
            test = self.random_choice(LAB_TESTS)

        # Generate value
        if make_abnormal:
            # 50/50 high vs low
            if self.random_bool(0.5):
                # High
                value = round(self.random_float(test.normal_max * 1.1, test.normal_max * 1.5), 1)
                abnormal_flag = "H" if value < test.normal_max * 1.3 else "HH"
            else:
                # Low
                value = round(self.random_float(test.normal_min * 0.5, test.normal_min * 0.9), 1)
                abnormal_flag = "L" if value > test.normal_min * 0.7 else "LL"
        else:
            # Normal range
            value = round(self.random_float(test.normal_min, test.normal_max), 1)
            abnormal_flag = None

        # Timing
        if encounter:
            collected_time = encounter.admission_time + timedelta(hours=self.random_int(1, 4))
            resulted_time = collected_time + timedelta(hours=self.random_int(2, 6))
        else:
            collected_time = datetime.now() - timedelta(days=self.random_int(0, 7))
            resulted_time = collected_time + timedelta(hours=self.random_int(2, 6))

        return LabResult(
            test_name=test.name,
            loinc_code=test.loinc_code,
            value=str(value),
            unit=test.unit,
            reference_range=f"{test.normal_min}-{test.normal_max}",
            abnormal_flag=abnormal_flag,
            patient_mrn=patient.mrn,
            encounter_id=encounter.encounter_id if encounter else None,
            collected_time=collected_time,
            resulted_time=resulted_time,
        )

    def generate_vital_signs(
        self,
        patient: Patient,
        encounter: Encounter | None = None,
        abnormal_parameters: list[str] | None = None,
    ) -> VitalSign:
        """Generate vital signs for a patient.

        Args:
            patient: The patient these vitals are for.
            encounter: Optional encounter to link to.
            abnormal_parameters: List of parameters to make abnormal
                                (temperature, heart_rate, etc.).

        Returns:
            VitalSign instance with realistic values.

        Example:
            >>> gen = PatientGenerator()
            >>> patient = gen.generate_patient()
            >>> vitals = gen.generate_vital_signs(patient, abnormal_parameters=["temperature"])
        """
        # Age-appropriate ranges
        age_group = "adult" if patient.age >= 18 else "pediatric"
        ranges = VITAL_RANGES[age_group]

        # Observation time
        if encounter:
            observation_time = encounter.admission_time + timedelta(minutes=self.random_int(15, 60))
        else:
            observation_time = datetime.now() - timedelta(days=self.random_int(0, 7))

        # Generate vitals
        abnormal = abnormal_parameters or []

        # Temperature
        if "temperature" in abnormal:
            temperature = round(self.random_float(100.5, 103.0), 1)  # Fever
        else:
            temperature = round(self.random_float(*ranges["temperature"]), 1)

        # Heart rate
        if "heart_rate" in abnormal:
            heart_rate = self.random_int(110, 140)  # Tachycardia
        else:
            hr_range = ranges["heart_rate"]
            heart_rate = self.random_int(int(hr_range[0]), int(hr_range[1]))

        # Respiratory rate
        if "respiratory_rate" in abnormal:
            respiratory_rate = self.random_int(24, 32)  # Tachypnea
        else:
            rr_range = ranges["respiratory_rate"]
            respiratory_rate = self.random_int(int(rr_range[0]), int(rr_range[1]))

        # Blood pressure
        if "blood_pressure" in abnormal:
            systolic_bp = self.random_int(160, 190)  # Hypertension
            diastolic_bp = self.random_int(95, 110)
        else:
            sbp_range = ranges["systolic_bp"]
            dbp_range = ranges["diastolic_bp"]
            systolic_bp = self.random_int(int(sbp_range[0]), int(sbp_range[1]))
            diastolic_bp = self.random_int(int(dbp_range[0]), int(dbp_range[1]))

        # SpO2
        if "spo2" in abnormal:
            spo2 = self.random_int(85, 92)
        else:
            spo2_range = ranges["spo2"]
            spo2 = self.random_int(int(spo2_range[0]), int(spo2_range[1]))

        # Height/weight (reasonable ranges)
        height_cm = self.random_int(150, 190)
        weight_kg = self.random_int(50, 120)

        return VitalSign(
            patient_mrn=patient.mrn,
            encounter_id=encounter.encounter_id if encounter else None,
            observation_time=observation_time,
            temperature=temperature,
            heart_rate=heart_rate,
            respiratory_rate=respiratory_rate,
            systolic_bp=systolic_bp,
            diastolic_bp=diastolic_bp,
            spo2=spo2,
            height_cm=height_cm,
            weight_kg=weight_kg,
        )

    def generate_medication(
        self,
        patient: Patient,
        encounter: Encounter | None = None,
        medication_name: str | None = None,
    ) -> Medication:
        """Generate a medication order for a patient.

        Args:
            patient: The patient this medication is for.
            encounter: Optional encounter to link to.
            medication_name: Specific medication name. If None, random.

        Returns:
            Medication instance with realistic dosing.

        Example:
            >>> gen = PatientGenerator()
            >>> patient = gen.generate_patient()
            >>> med = gen.generate_medication(patient, medication_name="Metformin")
        """
        # Select medication
        if medication_name:
            med_info = get_medication(medication_name)
            if not med_info:
                raise ValueError(f"Unknown medication: {medication_name}")
        else:
            med_info = self.random_choice(MEDICATIONS)

        # Random dose, route, frequency from options
        dose = self.random_choice(med_info.common_doses)
        route = self.random_choice(med_info.routes)
        frequency = self.random_choice(med_info.frequencies)

        # Start date
        if encounter:
            start_date = encounter.admission_time
        else:
            start_date = datetime.now() - timedelta(days=self.random_int(1, 365))

        # Status (most are active)
        status = self.weighted_choice(
            [
                (MedicationStatus.ACTIVE, 0.7),
                (MedicationStatus.COMPLETED, 0.2),
                (MedicationStatus.STOPPED, 0.1),
            ]
        )

        # End date for non-active
        end_date = None
        if status != MedicationStatus.ACTIVE:
            end_date = start_date + timedelta(days=self.random_int(1, 90))

        return Medication(
            name=med_info.name,
            code=med_info.rxnorm_code,
            dose=dose,
            route=route,
            frequency=frequency,
            patient_mrn=patient.mrn,
            encounter_id=encounter.encounter_id if encounter else None,
            start_date=start_date,
            end_date=end_date,
            status=status,
            indication=med_info.indication,
        )


def generate_patient(seed: int | None = None, **kwargs: Any) -> Patient:
    """Convenience function to generate a single patient.

    Args:
        seed: Random seed for reproducible generation.
        **kwargs: Additional arguments passed to PatientGenerator.generate_patient().

    Returns:
        Patient instance.

    Example:
        >>> patient = generate_patient(seed=42, age_range=(50, 70))
    """
    gen = PatientGenerator(seed=seed)
    return gen.generate_patient(**kwargs)
