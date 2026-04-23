"""RxMemberSim-specific event handlers for the journey engine.

This module provides handlers for RxMemberSim events that can be registered
with the core JourneyEngine. Handlers generate the appropriate outputs
(claims, prescriptions, PA records, etc.) when events are executed.
"""

from datetime import date
from typing import Any

from healthsim.generation.journey_engine import (
    JourneyEngine,
    RxEventType,
    Timeline,
    TimelineEvent,
    create_journey_engine,
)


def prescription_handler(
    entity: Any,
    event: TimelineEvent,
    context: dict[str, Any],
) -> dict[str, Any]:
    """Handle prescription lifecycle events.
    
    Generates prescription records for new Rx, refills, transfers.
    """
    event_type = event.event_type
    member_id = getattr(entity, 'member_id', str(entity))
    
    if event_type == RxEventType.NEW_RX.value:
        return {
            "type": "prescription",
            "action": "new",
            "member_id": member_id,
            "rx_date": event.scheduled_date.isoformat(),
            "ndc": context.get("ndc"),
            "drug_name": context.get("drug_name"),
            "quantity": context.get("quantity", 30),
            "days_supply": context.get("days_supply", 30),
            "prescriber_npi": context.get("prescriber_npi"),
        }
    
    elif event_type == RxEventType.REFILL.value:
        return {
            "type": "prescription",
            "action": "refill",
            "member_id": member_id,
            "rx_date": event.scheduled_date.isoformat(),
            "original_rx_number": context.get("original_rx_number"),
            "refill_number": context.get("refill_number", 1),
        }
    
    return {"type": "prescription", "status": "unknown_event"}


def fill_handler(
    entity: Any,
    event: TimelineEvent,
    context: dict[str, Any],
) -> dict[str, Any]:
    """Handle pharmacy fill events.
    
    Generates fill records and NCPDP claim data.
    """
    event_type = event.event_type
    member_id = getattr(entity, 'member_id', str(entity))
    
    if event_type == RxEventType.FILL.value:
        return {
            "type": "fill",
            "action": "dispense",
            "member_id": member_id,
            "fill_date": event.scheduled_date.isoformat(),
            "rx_number": context.get("rx_number"),
            "ndc": context.get("ndc"),
            "quantity_dispensed": context.get("quantity", 30),
            "days_supply": context.get("days_supply", 30),
            "pharmacy_npi": context.get("pharmacy_npi"),
            "ingredient_cost": context.get("ingredient_cost"),
            "dispensing_fee": context.get("dispensing_fee"),
            "copay": context.get("copay"),
        }
    
    elif event_type == RxEventType.REVERSAL.value:
        return {
            "type": "fill",
            "action": "reversal",
            "member_id": member_id,
            "reversal_date": event.scheduled_date.isoformat(),
            "original_claim_id": context.get("original_claim_id"),
            "reason": context.get("reason", "return_to_stock"),
        }
    
    return {"type": "fill", "status": "unknown_event"}


def therapy_handler(
    entity: Any,
    event: TimelineEvent,
    context: dict[str, Any],
) -> dict[str, Any]:
    """Handle therapy management events.
    
    Generates therapy records for starts, changes, discontinuations.
    """
    event_type = event.event_type
    member_id = getattr(entity, 'member_id', str(entity))
    
    if event_type == RxEventType.THERAPY_START.value:
        return {
            "type": "therapy",
            "action": "start",
            "member_id": member_id,
            "start_date": event.scheduled_date.isoformat(),
            "therapy_class": context.get("therapy_class"),
            "drug_name": context.get("drug_name"),
            "ndc": context.get("ndc"),
            "indication": context.get("indication"),
        }
    
    elif event_type == RxEventType.THERAPY_CHANGE.value:
        return {
            "type": "therapy",
            "action": "change",
            "member_id": member_id,
            "change_date": event.scheduled_date.isoformat(),
            "from_drug": context.get("from_drug"),
            "to_drug": context.get("to_drug"),
            "reason": context.get("reason"),
        }
    
    elif event_type == RxEventType.THERAPY_DISCONTINUE.value:
        return {
            "type": "therapy",
            "action": "discontinue",
            "member_id": member_id,
            "discontinue_date": event.scheduled_date.isoformat(),
            "drug_name": context.get("drug_name"),
            "reason": context.get("reason", "therapy_complete"),
        }
    
    return {"type": "therapy", "status": "unknown_event"}


def adherence_handler(
    entity: Any,
    event: TimelineEvent,
    context: dict[str, Any],
) -> dict[str, Any]:
    """Handle adherence-related events.
    
    Generates adherence gap and MPR threshold records.
    """
    event_type = event.event_type
    member_id = getattr(entity, 'member_id', str(entity))
    
    if event_type == RxEventType.ADHERENCE_GAP.value:
        return {
            "type": "adherence",
            "status": "gap",
            "member_id": member_id,
            "gap_date": event.scheduled_date.isoformat(),
            "drug_class": context.get("drug_class"),
            "days_without_fill": context.get("days_without_fill"),
            "last_fill_date": context.get("last_fill_date"),
        }
    
    elif event_type == RxEventType.MPR_THRESHOLD.value:
        return {
            "type": "adherence",
            "status": "threshold_reached",
            "member_id": member_id,
            "measure_date": event.scheduled_date.isoformat(),
            "drug_class": context.get("drug_class"),
            "mpr_value": context.get("mpr_value"),
            "threshold": context.get("threshold", 0.8),
        }
    
    return {"type": "adherence", "status": "unknown_event"}


def milestone_handler(
    entity: Any,
    event: TimelineEvent,
    context: dict[str, Any],
) -> dict[str, Any]:
    """Handle milestone events.
    
    Milestones are non-transactional markers in a pharmacy journey.
    """
    member_id = getattr(entity, 'member_id', str(entity))
    
    return {
        "type": "milestone",
        "member_id": member_id,
        "milestone_name": event.event_name,
        "milestone_date": event.scheduled_date.isoformat(),
        "parameters": event.result.get("parameters", {}),
    }


def register_rx_handlers(engine: JourneyEngine) -> None:
    """Register all RxMemberSim event handlers with a journey engine.
    
    Args:
        engine: JourneyEngine instance to register handlers with
    """
    product = "rxmembersim"
    
    # Prescription handlers
    engine.register_handler(product, RxEventType.NEW_RX.value, prescription_handler)
    engine.register_handler(product, RxEventType.REFILL.value, prescription_handler)
    
    # Fill handlers
    engine.register_handler(product, RxEventType.FILL.value, fill_handler)
    engine.register_handler(product, RxEventType.REVERSAL.value, fill_handler)
    
    # Therapy handlers
    engine.register_handler(product, RxEventType.THERAPY_START.value, therapy_handler)
    engine.register_handler(product, RxEventType.THERAPY_CHANGE.value, therapy_handler)
    engine.register_handler(product, RxEventType.THERAPY_DISCONTINUE.value, therapy_handler)
    
    # Adherence handlers
    engine.register_handler(product, RxEventType.ADHERENCE_GAP.value, adherence_handler)
    engine.register_handler(product, RxEventType.MPR_THRESHOLD.value, adherence_handler)
    
    # Milestone handler
    engine.register_handler(product, "milestone", milestone_handler)


def create_rx_journey_engine(seed: int | None = None) -> JourneyEngine:
    """Create a JourneyEngine pre-configured with RxMemberSim handlers.
    
    Args:
        seed: Random seed for reproducibility
        
    Returns:
        JourneyEngine with all RxMemberSim handlers registered
        
    Example:
        >>> engine = create_rx_journey_engine(seed=42)
        >>> timeline = engine.create_timeline(rx_member, "rx_member", journey_spec)
        >>> results = engine.execute_timeline(timeline, rx_member)
    """
    engine = create_journey_engine(seed)
    register_rx_handlers(engine)
    return engine
