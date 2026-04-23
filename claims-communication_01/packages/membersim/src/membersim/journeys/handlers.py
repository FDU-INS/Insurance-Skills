"""MemberSim-specific event handlers for the journey engine.

This module provides handlers for MemberSim events that can be registered
with the core JourneyEngine. Handlers generate the appropriate outputs
(claims, enrollment records, etc.) when events are executed.
"""

from datetime import date
from typing import Any

from healthsim.generation.journey_engine import (
    JourneyEngine,
    MemberEventType,
    Timeline,
    TimelineEvent,
    create_journey_engine,
)

from membersim.core.member import Member


def enrollment_handler(
    member: Member,
    event: TimelineEvent,
    context: dict[str, Any],
) -> dict[str, Any]:
    """Handle enrollment-related events.
    
    Generates enrollment records for new enrollment, termination, plan changes.
    """
    event_type = event.event_type
    
    if event_type == MemberEventType.NEW_ENROLLMENT.value:
        return {
            "type": "enrollment",
            "action": "add",
            "member_id": member.member_id,
            "effective_date": event.scheduled_date.isoformat(),
            "plan_code": member.plan_code,
            "group_id": member.group_id,
        }
    
    elif event_type == MemberEventType.TERMINATION.value:
        return {
            "type": "enrollment",
            "action": "terminate",
            "member_id": member.member_id,
            "termination_date": event.scheduled_date.isoformat(),
            "reason": context.get("termination_reason", "voluntary"),
        }
    
    elif event_type == MemberEventType.PLAN_CHANGE.value:
        return {
            "type": "enrollment",
            "action": "change",
            "member_id": member.member_id,
            "effective_date": event.scheduled_date.isoformat(),
            "old_plan": context.get("old_plan"),
            "new_plan": context.get("new_plan"),
        }
    
    return {"type": "enrollment", "status": "unknown_event"}


def claim_handler(
    member: Member,
    event: TimelineEvent,
    context: dict[str, Any],
) -> dict[str, Any]:
    """Handle claims-related events.
    
    Generates claim records for professional, institutional, and pharmacy claims.
    """
    event_type = event.event_type
    base_claim = {
        "member_id": member.member_id,
        "service_date": event.scheduled_date.isoformat(),
        "subscriber_id": member.subscriber_id,
    }
    
    if event_type == MemberEventType.CLAIM_PROFESSIONAL.value:
        return {
            **base_claim,
            "type": "claim",
            "claim_type": "professional",
            "place_of_service": context.get("place_of_service", "11"),  # Office
            "procedure_codes": context.get("procedure_codes", ["99213"]),
            "diagnosis_codes": context.get("diagnosis_codes", ["Z00.00"]),
        }
    
    elif event_type == MemberEventType.CLAIM_INSTITUTIONAL.value:
        return {
            **base_claim,
            "type": "claim",
            "claim_type": "institutional",
            "facility_type": context.get("facility_type", "hospital"),
            "admission_date": context.get("admission_date", event.scheduled_date.isoformat()),
            "discharge_date": context.get("discharge_date"),
            "drg": context.get("drg"),
            "revenue_codes": context.get("revenue_codes", ["0120"]),
        }
    
    elif event_type == MemberEventType.CLAIM_PHARMACY.value:
        return {
            **base_claim,
            "type": "claim",
            "claim_type": "pharmacy",
            "ndc": context.get("ndc"),
            "quantity": context.get("quantity", 30),
            "days_supply": context.get("days_supply", 30),
            "pharmacy_npi": context.get("pharmacy_npi"),
        }
    
    return {"type": "claim", "status": "unknown_event"}


def quality_handler(
    member: Member,
    event: TimelineEvent,
    context: dict[str, Any],
) -> dict[str, Any]:
    """Handle quality/HEDIS-related events.
    
    Generates gap records for identified and closed quality gaps.
    """
    event_type = event.event_type
    
    if event_type == MemberEventType.GAP_IDENTIFIED.value:
        return {
            "type": "quality_gap",
            "status": "open",
            "member_id": member.member_id,
            "measure_id": context.get("measure_id", "CDC"),
            "measure_name": context.get("measure_name", "Comprehensive Diabetes Care"),
            "identified_date": event.scheduled_date.isoformat(),
            "due_date": context.get("due_date"),
        }
    
    elif event_type == MemberEventType.GAP_CLOSED.value:
        return {
            "type": "quality_gap",
            "status": "closed",
            "member_id": member.member_id,
            "measure_id": context.get("measure_id"),
            "closed_date": event.scheduled_date.isoformat(),
            "closed_by": context.get("closed_by", "claim"),
        }
    
    return {"type": "quality", "status": "unknown_event"}


def milestone_handler(
    member: Member,
    event: TimelineEvent,
    context: dict[str, Any],
) -> dict[str, Any]:
    """Handle milestone events.
    
    Milestones are non-transactional markers in a member's journey.
    """
    return {
        "type": "milestone",
        "member_id": member.member_id,
        "milestone_name": event.event_name,
        "milestone_date": event.scheduled_date.isoformat(),
        "parameters": event.result.get("parameters", {}),
    }


def register_member_handlers(engine: JourneyEngine) -> None:
    """Register all MemberSim event handlers with a journey engine.
    
    Args:
        engine: JourneyEngine instance to register handlers with
    """
    product = "membersim"
    
    # Enrollment handlers
    engine.register_handler(product, MemberEventType.NEW_ENROLLMENT.value, enrollment_handler)
    engine.register_handler(product, MemberEventType.TERMINATION.value, enrollment_handler)
    engine.register_handler(product, MemberEventType.PLAN_CHANGE.value, enrollment_handler)
    
    # Claims handlers
    engine.register_handler(product, MemberEventType.CLAIM_PROFESSIONAL.value, claim_handler)
    engine.register_handler(product, MemberEventType.CLAIM_INSTITUTIONAL.value, claim_handler)
    engine.register_handler(product, MemberEventType.CLAIM_PHARMACY.value, claim_handler)
    
    # Quality handlers
    engine.register_handler(product, MemberEventType.GAP_IDENTIFIED.value, quality_handler)
    engine.register_handler(product, MemberEventType.GAP_CLOSED.value, quality_handler)
    
    # Milestone handler (from base types)
    engine.register_handler(product, "milestone", milestone_handler)


def create_member_journey_engine(seed: int | None = None) -> JourneyEngine:
    """Create a JourneyEngine pre-configured with MemberSim handlers.
    
    Args:
        seed: Random seed for reproducibility
        
    Returns:
        JourneyEngine with all MemberSim handlers registered
        
    Example:
        >>> engine = create_member_journey_engine(seed=42)
        >>> timeline = engine.create_timeline(member, "member", journey_spec)
        >>> results = engine.execute_timeline(timeline, member)
    """
    engine = create_journey_engine(seed)
    register_member_handlers(engine)
    return engine
