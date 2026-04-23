"""Core patient simulation models and data structures."""

from healthsim.person import Address, ContactInfo, PersonName
from healthsim.temporal import EventDelay, EventStatus, Timeline, TimelineEvent

from patientsim.core.generator import PatientGenerator, generate_patient
from patientsim.core.models import (
    ClinicalNote,
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
    Procedure,
    VitalSign,
)
from patientsim.core.state import (
    EntityWithProvenance,
    Provenance,
    ProvenanceSummary,
    Scenario,
    ScenarioMetadata,
    SourceType,
)
from patientsim.core.timeline import (
    ClinicalEvent,
    ClinicalEventType,
    ClinicalTimeline,
)

# Backward compatibility alias - use PatientGenerator for new code
PatientFactory = PatientGenerator

__all__ = [
    # Person components (from healthsim-core)
    "PersonName",
    "Address",
    "ContactInfo",
    # Timeline components (from healthsim-core)
    "Timeline",
    "TimelineEvent",
    "EventStatus",
    "EventDelay",
    # Clinical timeline (PatientSim-specific)
    "ClinicalTimeline",
    "ClinicalEvent",
    "ClinicalEventType",
    # Models
    "Patient",
    "Encounter",
    "Diagnosis",
    "Procedure",
    "Medication",
    "LabResult",
    "VitalSign",
    "ClinicalNote",
    # Enums
    "Gender",
    "EncounterClass",
    "EncounterStatus",
    "DiagnosisType",
    "MedicationStatus",
    # Generator
    "PatientGenerator",
    "PatientFactory",  # Backward compatibility alias
    "generate_patient",
    # State Management
    "Provenance",
    "SourceType",
    "ProvenanceSummary",
    "EntityWithProvenance",
    "Scenario",
    "ScenarioMetadata",
]
