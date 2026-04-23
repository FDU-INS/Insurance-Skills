"""PatientSim-specific event handlers for the journey engine.

This module provides handlers for PatientSim clinical events that can be registered
with the core JourneyEngine. Handlers generate the appropriate outputs
(encounters, observations, diagnoses, etc.) when events are executed.

The handlers wrap the core healthsim.generation.handlers.PatientSimHandlers class
and provide a consistent interface matching MemberSim and RxMemberSim patterns.
"""

from typing import Any

from healthsim.generation.journey_engine import (
    JourneyEngine,
    PatientEventType,
    TimelineEvent,
    create_journey_engine,
)
from healthsim.generation.handlers import PatientSimHandlers as CorePatientSimHandlers


# Re-export the core handlers class for direct access if needed
PatientSimHandlers = CorePatientSimHandlers


def admission_handler(
    patient: Any,
    event: TimelineEvent,
    context: dict[str, Any],
) -> dict[str, Any]:
    """Handle admission events.
    
    Generates ADT A01 admission records.
    """
    handlers = CorePatientSimHandlers(context.get("seed"))
    return handlers.handle_admission(patient, event, context)


def discharge_handler(
    patient: Any,
    event: TimelineEvent,
    context: dict[str, Any],
) -> dict[str, Any]:
    """Handle discharge events.
    
    Generates ADT A03 discharge records.
    """
    handlers = CorePatientSimHandlers(context.get("seed"))
    return handlers.handle_discharge(patient, event, context)


def encounter_handler(
    patient: Any,
    event: TimelineEvent,
    context: dict[str, Any],
) -> dict[str, Any]:
    """Handle outpatient encounter events.
    
    Generates encounter records for office visits, ED visits, etc.
    """
    handlers = CorePatientSimHandlers(context.get("seed"))
    return handlers.handle_encounter(patient, event, context)


def diagnosis_handler(
    patient: Any,
    event: TimelineEvent,
    context: dict[str, Any],
) -> dict[str, Any]:
    """Handle diagnosis events.
    
    Generates condition/diagnosis records with ICD-10 codes.
    """
    handlers = CorePatientSimHandlers(context.get("seed"))
    return handlers.handle_diagnosis(patient, event, context)


def lab_order_handler(
    patient: Any,
    event: TimelineEvent,
    context: dict[str, Any],
) -> dict[str, Any]:
    """Handle laboratory order events.
    
    Generates ORM O01 lab order messages.
    """
    handlers = CorePatientSimHandlers(context.get("seed"))
    return handlers.handle_lab_order(patient, event, context)


def lab_result_handler(
    patient: Any,
    event: TimelineEvent,
    context: dict[str, Any],
) -> dict[str, Any]:
    """Handle laboratory result events.
    
    Generates ORU R01 lab result messages.
    """
    handlers = CorePatientSimHandlers(context.get("seed"))
    return handlers.handle_lab_result(patient, event, context)


def medication_order_handler(
    patient: Any,
    event: TimelineEvent,
    context: dict[str, Any],
) -> dict[str, Any]:
    """Handle medication order events.
    
    Generates RDE O11 pharmacy/treatment order messages.
    """
    handlers = CorePatientSimHandlers(context.get("seed"))
    return handlers.handle_medication_order(patient, event, context)


def procedure_handler(
    patient: Any,
    event: TimelineEvent,
    context: dict[str, Any],
) -> dict[str, Any]:
    """Handle procedure events.
    
    Generates procedure records with CPT codes.
    """
    handlers = CorePatientSimHandlers(context.get("seed"))
    return handlers.handle_procedure(patient, event, context)


def milestone_handler(
    patient: Any,
    event: TimelineEvent,
    context: dict[str, Any],
) -> dict[str, Any]:
    """Handle milestone events.
    
    Milestones are non-transactional markers in a patient's journey.
    """
    patient_id = _get_patient_id(patient)
    return {
        "type": "milestone",
        "patient_id": patient_id,
        "milestone_name": event.event_name,
        "milestone_date": event.scheduled_date.isoformat(),
        "parameters": event.result.get("parameters", {}) if event.result else {},
    }


def _get_patient_id(patient: Any) -> str:
    """Extract patient ID from various entity formats."""
    if isinstance(patient, dict):
        return patient.get("patient_id", patient.get("id", "unknown"))
    return getattr(patient, "patient_id", getattr(patient, "id", "unknown"))


def register_patient_handlers(engine: JourneyEngine, seed: int | None = None) -> None:
    """Register all PatientSim event handlers with a journey engine.
    
    Args:
        engine: JourneyEngine instance to register handlers with
        seed: Random seed for reproducibility
    """
    # Use the core handlers class for registration
    handlers = CorePatientSimHandlers(seed)
    handlers.register_all(engine)
    
    # Also register milestone handler
    engine.register_handler("patientsim", "milestone", milestone_handler)


def create_patient_journey_engine(seed: int | None = None) -> JourneyEngine:
    """Create a JourneyEngine pre-configured with PatientSim handlers.
    
    Args:
        seed: Random seed for reproducibility
        
    Returns:
        JourneyEngine with all PatientSim handlers registered
        
    Example:
        >>> engine = create_patient_journey_engine(seed=42)
        >>> timeline = engine.create_timeline(patient, "patient", journey_spec)
        >>> results = engine.execute_timeline(timeline, patient)
    """
    engine = create_journey_engine(seed)
    register_patient_handlers(engine, seed)
    return engine
