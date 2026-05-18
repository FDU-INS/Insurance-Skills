"""PatientSim - Healthcare patient simulation and synthetic data generation platform.

This package provides tools for generating realistic synthetic patient data
for healthcare applications, testing, and research.

Key Features:
- Patient model extending healthsim.person.Person
- Clinical encounter, diagnosis, medication, and lab generation
- ClinicalTimeline for managing patient care events
- Validation framework for ensuring data quality
- Format transformers for HL7v2, FHIR, etc.
- Dimensional output for analytics and BI tools

Example:
    >>> from patientsim.core import PatientGenerator, Patient, Gender
    >>> from patientsim.core import ClinicalTimeline
    >>>
    >>> # Generate a patient
    >>> gen = PatientGenerator(seed=42)
    >>> patient = gen.generate_patient(age_range=(50, 70), gender=Gender.MALE)
    >>> print(f"{patient.full_name}, {patient.age} years old")
    >>>
    >>> # Create a clinical timeline
    >>> timeline = ClinicalTimeline(patient_mrn=patient.mrn)
    >>> timeline.add_admission(datetime.now(), facility="General Hospital")
    >>>
    >>> # Transform to dimensional format for analytics
    >>> from patientsim.dimensional import PatientDimensionalTransformer
    >>> transformer = PatientDimensionalTransformer(patients=[patient])
    >>> dimensions, facts = transformer.transform()
"""

__version__ = "2.1.0"

# Expose dimensional transformer at package level
from patientsim.dimensional import PatientDimensionalTransformer

# Expose journeys module for convenience
from patientsim.journeys import (
    create_patient_journey_engine,
    PATIENT_JOURNEY_TEMPLATES,
    get_patient_journey_template,
    list_patient_journey_templates,
)

__all__ = [
    "PatientDimensionalTransformer",
    # Journey exports
    "create_patient_journey_engine",
    "PATIENT_JOURNEY_TEMPLATES",
    "get_patient_journey_template",
    "list_patient_journey_templates",
]
