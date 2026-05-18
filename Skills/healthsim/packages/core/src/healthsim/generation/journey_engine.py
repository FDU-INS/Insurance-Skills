"""Shared journey engine for cross-product event orchestration.

This module provides the core journey execution engine that can be used
across all HealthSim products (PatientSim, MemberSim, RxMemberSim, etc.).

The journey engine follows a timeline-based approach:
1. JourneySpecification defines the event sequence
2. JourneyEngine creates timelines with scheduled events
3. Product-specific handlers execute events
4. Cross-product triggers coordinate related events
"""

from __future__ import annotations

import hashlib
import random
from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from enum import Enum
from typing import Any, Protocol

from pydantic import BaseModel, Field

# Import for skill-aware parameter resolution (lazy to avoid circular imports)
_parameter_resolver = None

def _get_parameter_resolver():
    """Lazy load the parameter resolver to avoid circular imports."""
    global _parameter_resolver
    if _parameter_resolver is None:
        from healthsim.generation.skill_reference import ParameterResolver
        _parameter_resolver = ParameterResolver()
    return _parameter_resolver


_skill_registry = None

def _get_skill_registry():
    """Lazy load the skill registry to avoid circular imports."""
    global _skill_registry
    if _skill_registry is None:
        from healthsim.generation.skill_registry import SkillRegistry
        _skill_registry = SkillRegistry()
    return _skill_registry


# =============================================================================
# Event Type System
# =============================================================================

class BaseEventType(str, Enum):
    """Base event types common across products."""
    
    # Lifecycle events
    ENTITY_CREATED = "entity_created"
    ENTITY_UPDATED = "entity_updated"
    ENTITY_TERMINATED = "entity_terminated"
    
    # Temporal markers
    JOURNEY_START = "journey_start"
    JOURNEY_END = "journey_end"
    MILESTONE = "milestone"
    
    # Cross-product triggers
    TRIGGER_OUTBOUND = "trigger_outbound"
    TRIGGER_RECEIVED = "trigger_received"


class PatientEventType(str, Enum):
    """PatientSim-specific event types."""
    
    # ADT events
    ADMISSION = "admission"
    DISCHARGE = "discharge"
    TRANSFER = "transfer"
    
    # Clinical events
    ENCOUNTER = "encounter"
    OBSERVATION = "observation"
    PROCEDURE = "procedure"
    MEDICATION_ORDER = "medication_order"
    LAB_ORDER = "lab_order"
    LAB_RESULT = "lab_result"
    DIAGNOSIS = "diagnosis"
    
    # Care coordination
    REFERRAL = "referral"
    CARE_PLAN_UPDATE = "care_plan_update"


class MemberEventType(str, Enum):
    """MemberSim-specific event types."""
    
    # Enrollment
    NEW_ENROLLMENT = "new_enrollment"
    TERMINATION = "termination"
    PLAN_CHANGE = "plan_change"
    
    # Claims
    CLAIM_PROFESSIONAL = "claim_professional"
    CLAIM_INSTITUTIONAL = "claim_institutional"
    CLAIM_PHARMACY = "claim_pharmacy"
    
    # Quality
    GAP_IDENTIFIED = "gap_identified"
    GAP_CLOSED = "gap_closed"


class RxEventType(str, Enum):
    """RxMemberSim-specific event types."""
    
    # Prescription lifecycle
    NEW_RX = "new_rx"
    REFILL = "refill"
    FILL = "fill"
    REVERSAL = "reversal"
    
    # Therapy management
    THERAPY_START = "therapy_start"
    THERAPY_CHANGE = "therapy_change"
    THERAPY_DISCONTINUE = "therapy_discontinue"
    
    # Adherence
    ADHERENCE_GAP = "adherence_gap"
    MPR_THRESHOLD = "mpr_threshold"


class TrialEventType(str, Enum):
    """TrialSim-specific event types."""
    
    # Enrollment
    SCREENING = "screening"
    RANDOMIZATION = "randomization"
    WITHDRAWAL = "withdrawal"
    
    # Visits
    SCHEDULED_VISIT = "scheduled_visit"
    UNSCHEDULED_VISIT = "unscheduled_visit"
    
    # Safety
    ADVERSE_EVENT = "adverse_event"
    SERIOUS_ADVERSE_EVENT = "serious_adverse_event"
    
    # Protocol
    PROTOCOL_DEVIATION = "protocol_deviation"
    DOSE_MODIFICATION = "dose_modification"



# =============================================================================
# Delay and Timing Specifications
# =============================================================================

class DelaySpec(BaseModel):
    """Specification for event delay/timing."""
    
    days: int = 0
    days_min: int | None = None
    days_max: int | None = None
    distribution: str = "fixed"  # fixed, uniform, normal
    
    def to_timedelta(self, seed: int | None = None) -> timedelta:
        """Convert to actual timedelta, applying randomization if needed."""
        rng = random.Random(seed) if seed else random.Random()
        
        if self.distribution == "fixed":
            return timedelta(days=self.days)
        
        elif self.distribution == "uniform":
            min_days = self.days_min if self.days_min is not None else self.days
            max_days = self.days_max if self.days_max is not None else self.days
            actual_days = rng.randint(min_days, max_days)
            return timedelta(days=actual_days)
        
        elif self.distribution == "normal":
            # Use days as mean, (max-min)/4 as std_dev
            mean = self.days
            std_dev = (self.days_max - self.days_min) / 4 if self.days_min and self.days_max else 2
            actual_days = max(0, int(rng.gauss(mean, std_dev)))
            return timedelta(days=actual_days)
        
        return timedelta(days=self.days)


# =============================================================================
# Condition System
# =============================================================================

class EventCondition(BaseModel):
    """Condition that must be met for an event to occur."""
    
    field: str  # Path to context field (e.g., "demographics.age")
    operator: str  # eq, ne, gt, gte, lt, lte, in, not_in, contains
    value: Any
    
    def evaluate(self, context: dict[str, Any]) -> bool:
        """Evaluate condition against context."""
        # Navigate to field value
        actual = self._get_field_value(context, self.field)
        if actual is None:
            return False
        
        # Apply operator
        if self.operator == "eq":
            return actual == self.value
        elif self.operator == "ne":
            return actual != self.value
        elif self.operator == "gt":
            return actual > self.value
        elif self.operator == "gte":
            return actual >= self.value
        elif self.operator == "lt":
            return actual < self.value
        elif self.operator == "lte":
            return actual <= self.value
        elif self.operator == "in":
            return actual in self.value
        elif self.operator == "not_in":
            return actual not in self.value
        elif self.operator == "contains":
            return self.value in actual
        
        return False
    
    def _get_field_value(self, context: dict, path: str) -> Any:
        """Navigate to nested field value."""
        parts = path.split(".")
        current = context
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return None
        return current


# =============================================================================
# Event Definitions
# =============================================================================

class SkillRef(BaseModel):
    """Reference to a skill for parameter resolution.
    
    When present in parameters, the ParameterResolver will load the
    referenced skill and extract values based on the lookup key.
    
    Example:
        skill_ref = SkillRef(
            skill="diabetes-management",
            lookup="diagnosis_code",
            context={"control_status": "${entity.control_status}"}
        )
    """
    skill: str = Field(..., description="Skill name to reference")
    lookup: str = Field(..., description="What to look up in the skill")
    context: dict[str, Any] = Field(default_factory=dict, description="Context for resolution")
    fallback: Any = Field(default=None, description="Fallback if lookup fails")


class EventDefinition(BaseModel):
    """Definition of an event within a journey.
    
    Events can specify parameters in three ways:
    1. Direct values: {"icd10": "E11.9", "description": "..."}
    2. Skill references: {"skill_ref": {"skill": "diabetes-management", "lookup": "diagnosis_code"}}
    3. Auto-resolution: Set `condition` field and parameters are resolved automatically
    
    When skill_ref is present, the ParameterResolver will resolve it
    to concrete values at execution time.
    
    When condition is set (e.g., "diabetes"), the SkillRegistry automatically
    finds the appropriate skill and resolves parameters based on event_type.
    """
    
    event_id: str
    name: str
    event_type: str  # String to support any event type enum
    product: str = "core"  # Which product owns this event
    
    # Timing
    delay: DelaySpec = Field(default_factory=DelaySpec)
    depends_on: str | None = None  # event_id of dependency
    
    # Conditions
    conditions: list[EventCondition] = Field(default_factory=list)
    
    # Probability (for optional events)
    probability: float = 1.0
    
    # Auto-resolution: specify condition to auto-resolve from skill
    condition: str | None = None  # e.g., "diabetes", "ckd", "heart_failure"
    
    # Event-specific parameters (can include skill_ref for dynamic resolution)
    parameters: dict[str, Any] = Field(default_factory=dict)
    
    # Cross-product triggers
    triggers: list["TriggerSpec"] = Field(default_factory=list)
    
    def has_skill_ref(self) -> bool:
        """Check if parameters contain a skill reference."""
        return "skill_ref" in self.parameters
    
    def uses_auto_resolution(self) -> bool:
        """Check if this event uses auto-resolution via condition."""
        return self.condition is not None


class TriggerSpec(BaseModel):
    """Specification for a cross-product trigger."""
    
    target_product: str  # e.g., "membersim", "patientsim"
    event_type: str
    delay: DelaySpec = Field(default_factory=DelaySpec)
    parameters: dict[str, Any] = Field(default_factory=dict)
    condition: EventCondition | None = None



# =============================================================================
# Journey Specification
# =============================================================================

class JourneySpecification(BaseModel):
    """Complete specification for a journey (temporal event sequence)."""
    
    journey_id: str
    name: str
    description: str = ""
    version: str = "1.0"
    
    # Target products
    products: list[str] = Field(default_factory=lambda: ["patientsim"])
    
    # Duration
    duration_days: int | None = None
    
    # Events in the journey
    events: list[EventDefinition] = Field(default_factory=list)
    
    # Journey-level parameters
    parameters: dict[str, Any] = Field(default_factory=dict)
    
    @classmethod
    def from_dict(cls, data: dict) -> "JourneySpecification":
        """Create from dictionary."""
        return cls(**data)


# =============================================================================
# Timeline Classes
# =============================================================================

@dataclass
class TimelineEvent:
    """A scheduled event on a timeline."""
    
    timeline_event_id: str
    journey_id: str
    event_definition_id: str
    scheduled_date: date
    event_type: str
    event_name: str
    product: str = "core"
    
    # Auto-resolution condition (e.g., "diabetes", "ckd")
    condition: str | None = None
    
    # Event parameters (may contain skill_ref for lazy resolution)
    parameters: dict[str, Any] = field(default_factory=dict)
    
    # Execution state
    status: str = "pending"  # pending, executed, skipped, failed
    executed_at: datetime | None = None
    result: dict[str, Any] = field(default_factory=dict)
    
    # Resolved parameters (after skill_ref resolution)
    resolved_parameters: dict[str, Any] = field(default_factory=dict)
    
    # Cross-product tracking
    triggered_events: list[str] = field(default_factory=list)


@dataclass 
class Timeline:
    """Timeline of events for an entity."""
    
    entity_id: str
    entity_type: str  # "patient", "member", "rx_member", etc.
    journey_ids: list[str] = field(default_factory=list)
    start_date: date = field(default_factory=date.today)
    end_date: date | None = None
    
    events: list[TimelineEvent] = field(default_factory=list)
    
    # Cross-product correlation
    linked_timelines: dict[str, str] = field(default_factory=dict)  # product -> timeline_id
    
    def add_event(self, event: TimelineEvent) -> None:
        """Add event to timeline, maintaining chronological order."""
        self.events.append(event)
        self.events.sort(key=lambda e: e.scheduled_date)
    
    def get_pending_events(self) -> list[TimelineEvent]:
        """Get all pending events in chronological order."""
        return [e for e in self.events if e.status == "pending"]
    
    def get_events_by_date(self, target_date: date) -> list[TimelineEvent]:
        """Get events scheduled for a specific date."""
        return [e for e in self.events if e.scheduled_date == target_date]
    
    def get_events_up_to(self, target_date: date) -> list[TimelineEvent]:
        """Get pending events up to and including target date."""
        return [
            e for e in self.events 
            if e.status == "pending" and e.scheduled_date <= target_date
        ]
    
    def mark_executed(self, event_id: str, result: dict[str, Any]) -> None:
        """Mark an event as executed with result."""
        for event in self.events:
            if event.timeline_event_id == event_id:
                event.status = "executed"
                event.executed_at = datetime.utcnow()
                event.result = result
                break


# =============================================================================
# Event Handler Protocol
# =============================================================================

class EventHandler(Protocol):
    """Protocol for event handlers."""
    
    def __call__(
        self,
        entity: Any,
        event: TimelineEvent,
        context: dict[str, Any]
    ) -> dict[str, Any]:
        """Execute the event and return results."""
        ...



# =============================================================================
# Journey Engine
# =============================================================================

class JourneyEngine:
    """Engine for executing journeys and generating timelines.
    
    The journey engine is the orchestrator for temporal event sequences.
    It creates timelines from journey specifications and coordinates
    event execution across products.
    
    Example:
        >>> engine = JourneyEngine(seed=42)
        >>> engine.register_handler("patientsim", "encounter", encounter_handler)
        >>> 
        >>> journey = JourneySpecification(...)
        >>> timeline = engine.create_timeline(patient, journey, start_date)
        >>> 
        >>> # Execute events up to today
        >>> results = engine.execute_timeline(timeline, patient, up_to_date=date.today())
    """
    
    def __init__(self, seed: int | None = None):
        """Initialize the journey engine.
        
        Args:
            seed: Random seed for reproducibility
        """
        self.seed = seed
        self._rng = random.Random(seed)
        
        # Handlers by product and event type
        self._handlers: dict[str, dict[str, EventHandler]] = {}
        
        # Cross-product trigger handlers
        self._trigger_handlers: dict[str, Callable] = {}
        
        # Active timelines for cross-product coordination
        self._active_timelines: dict[str, Timeline] = {}
    
    def register_handler(
        self,
        product: str,
        event_type: str,
        handler: EventHandler
    ) -> None:
        """Register an event handler for a product/event type combination.
        
        Args:
            product: Product identifier (e.g., "patientsim", "membersim")
            event_type: Event type string
            handler: Callable that handles the event
        """
        if product not in self._handlers:
            self._handlers[product] = {}
        self._handlers[product][event_type] = handler
    
    def register_trigger_handler(
        self,
        target_product: str,
        handler: Callable[[str, TriggerSpec, dict], None]
    ) -> None:
        """Register handler for cross-product triggers.
        
        Args:
            target_product: Product that receives triggers
            handler: Function to handle trigger dispatch
        """
        self._trigger_handlers[target_product] = handler
    
    def create_timeline(
        self,
        entity: Any,
        entity_type: str,
        journey: JourneySpecification,
        start_date: date | None = None,
        parameters: dict[str, Any] | None = None,
    ) -> Timeline:
        """Create a timeline for an entity from a journey specification.
        
        Args:
            entity: The entity (patient, member, etc.)
            entity_type: Type identifier for the entity
            journey: Journey specification to use
            start_date: When to start the timeline
            parameters: Override journey parameters
            
        Returns:
            Timeline with scheduled events
        """
        # Determine entity ID
        entity_id = self._get_entity_id(entity)
        
        # Create timeline
        timeline_start = start_date or date.today()
        timeline = Timeline(
            entity_id=entity_id,
            entity_type=entity_type,
            journey_ids=[journey.journey_id],
            start_date=timeline_start,
        )
        
        # Build context for condition evaluation
        context = self._build_context(entity, entity_type, parameters or {})
        
        # Schedule events
        scheduled_events: dict[str, date] = {}
        current_date = timeline_start
        
        for event_def in journey.events:
            # Check probability
            if event_def.probability < 1.0:
                if self._rng.random() > event_def.probability:
                    continue
            
            # Check conditions
            if not self._evaluate_conditions(event_def.conditions, context):
                continue
            
            # Calculate scheduled date
            if event_def.depends_on and event_def.depends_on in scheduled_events:
                base_date = scheduled_events[event_def.depends_on]
            else:
                base_date = current_date
            
            # Apply delay with seed for reproducibility
            event_seed = self._derive_seed(entity_id, event_def.event_id)
            delay = event_def.delay.to_timedelta(event_seed)
            event_date = base_date + delay
            
            # Create timeline event
            timeline_event_id = self._generate_event_id(entity_id, event_def.event_id)
            timeline_event = TimelineEvent(
                timeline_event_id=timeline_event_id,
                journey_id=journey.journey_id,
                event_definition_id=event_def.event_id,
                scheduled_date=event_date,
                event_type=event_def.event_type,
                event_name=event_def.name,
                product=event_def.product,
                condition=event_def.condition,  # For auto-resolution
                parameters=event_def.parameters.copy(),  # Store original params
            )
            
            timeline.add_event(timeline_event)
            scheduled_events[event_def.event_id] = event_date
            
            # Update current_date for non-dependent events
            if not event_def.depends_on:
                current_date = event_date
        
        # Set end date
        if timeline.events:
            timeline.end_date = max(e.scheduled_date for e in timeline.events)
        
        # Register as active timeline
        self._active_timelines[timeline.entity_id] = timeline
        
        return timeline

    
    def execute_event(
        self,
        timeline: Timeline,
        event: TimelineEvent,
        entity: Any,
        context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Execute a single event from a timeline.
        
        Args:
            timeline: The entity's timeline
            event: The event to execute
            entity: The entity
            context: Additional context
            
        Returns:
            Execution result dict
        """
        product = event.product
        event_type = event.event_type
        
        # Find handler
        if product not in self._handlers or event_type not in self._handlers[product]:
            return {"status": "skipped", "reason": f"No handler for {product}/{event_type}"}
        
        handler = self._handlers[product][event_type]
        
        try:
            # Resolve skill references in parameters
            entity_dict = self._entity_to_dict(entity)
            resolved_params = self._resolve_event_parameters(
                event.parameters, 
                entity_dict,
                event_type=event.event_type,
                condition=event.condition,
            )
            event.resolved_parameters = resolved_params
            
            # Merge resolved parameters into context
            exec_context = dict(context or {})
            exec_context["event_parameters"] = resolved_params
            
            result = handler(entity, event, exec_context)
            timeline.mark_executed(event.timeline_event_id, result)
            
            # Process triggers
            self._process_triggers(event, result, exec_context)
            
            return {"status": "executed", "outputs": result, "parameters": resolved_params}
        except Exception as e:
            event.status = "failed"
            return {"status": "failed", "error": str(e)}
    
    def _entity_to_dict(self, entity: Any) -> dict[str, Any]:
        """Convert entity to dictionary for parameter resolution."""
        if isinstance(entity, dict):
            return entity
        if hasattr(entity, "model_dump"):
            return entity.model_dump()
        if hasattr(entity, "dict"):
            return entity.dict()
        if hasattr(entity, "__dict__"):
            return entity.__dict__
        return {}
    
    def _resolve_event_parameters(
        self,
        parameters: dict[str, Any],
        entity_dict: dict[str, Any],
        event_type: str | None = None,
        condition: str | None = None,
    ) -> dict[str, Any]:
        """Resolve skill references and entity variables in parameters.
        
        Supports three resolution modes:
        1. Direct values: Used as-is
        2. skill_ref: Explicit skill reference resolved via ParameterResolver
        3. Auto-resolution: When condition is set, finds skill automatically
        
        Args:
            parameters: Original event parameters
            entity_dict: Entity attributes for ${entity.x} substitution
            event_type: Event type (for auto-resolution)
            condition: Condition keyword (for auto-resolution)
            
        Returns:
            Resolved parameters with concrete values
        """
        # Auto-resolution: condition is set, no skill_ref
        if condition and "skill_ref" not in parameters and event_type:
            return self._auto_resolve_parameters(
                event_type, condition, parameters, entity_dict
            )
        
        # Explicit skill_ref
        if "skill_ref" in parameters:
            resolver = _get_parameter_resolver()
            return resolver.resolve_event_parameters(parameters, entity_dict)
        
        # Direct values - just resolve entity variables
        if not parameters:
            return {}
        
        resolved = {}
        for key, value in parameters.items():
            if isinstance(value, str) and "${entity." in value:
                resolved[key] = self._resolve_entity_var(value, entity_dict)
            else:
                resolved[key] = value
        
        return resolved
    
    def _auto_resolve_parameters(
        self,
        event_type: str,
        condition: str,
        parameters: dict[str, Any],
        entity_dict: dict[str, Any],
    ) -> dict[str, Any]:
        """Auto-resolve parameters using SkillRegistry.
        
        Args:
            event_type: Type of event (diagnosis, medication_order, etc.)
            condition: Condition keyword (diabetes, ckd, etc.)
            parameters: Additional parameters to merge
            entity_dict: Entity attributes
            
        Returns:
            Resolved parameters
        """
        registry = _get_skill_registry()
        
        resolved = registry.resolve_for_event(
            event_type=event_type,
            condition=condition,
            context=entity_dict,
        )
        
        # Merge with any additional provided parameters
        for key, value in parameters.items():
            if key not in resolved:
                if isinstance(value, str) and "${entity." in value:
                    resolved[key] = self._resolve_entity_var(value, entity_dict)
                else:
                    resolved[key] = value
        
        return resolved
    
    def _resolve_entity_var(self, value: str, entity: dict[str, Any]) -> Any:
        """Resolve ${entity.x} variables in a string."""
        import re
        pattern = r"\$\{entity\.(\w+)\}"
        
        def replacer(match):
            attr = match.group(1)
            return str(entity.get(attr, match.group(0)))
        
        result = re.sub(pattern, replacer, value)
        
        # If entire string was a variable, return the actual value
        if value.startswith("${entity.") and value.endswith("}"):
            attr = value[9:-1]
            return entity.get(attr, value)
        
        return result
    
    def execute_timeline(
        self,
        timeline: Timeline,
        entity: Any,
        up_to_date: date | None = None,
        context: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """Execute all pending events on a timeline up to a date.
        
        Args:
            timeline: Timeline to execute
            entity: The entity
            up_to_date: Execute events up to this date
            context: Additional context
            
        Returns:
            List of execution results
        """
        results = []
        target_date = up_to_date or date.max
        
        for event in timeline.get_events_up_to(target_date):
            result = self.execute_event(timeline, event, entity, context)
            results.append({
                "event_id": event.timeline_event_id,
                "event_type": event.event_type,
                "scheduled_date": event.scheduled_date.isoformat(),
                **result,
            })
        
        return results
    
    def _process_triggers(
        self,
        event: TimelineEvent,
        result: dict[str, Any],
        context: dict[str, Any]
    ) -> None:
        """Process cross-product triggers from an executed event."""
        # This would dispatch to trigger handlers for cross-product coordination
        # Implementation depends on product-specific trigger definitions
        pass
    
    def _build_context(
        self,
        entity: Any,
        entity_type: str,
        parameters: dict[str, Any]
    ) -> dict[str, Any]:
        """Build context dict for condition evaluation."""
        context = {
            "entity_type": entity_type,
            "params": parameters,
        }
        
        # Extract entity attributes if available
        if hasattr(entity, "__dict__"):
            context["entity"] = entity.__dict__
        elif hasattr(entity, "dict"):
            context["entity"] = entity.dict()
        elif isinstance(entity, dict):
            context["entity"] = entity
        
        return context
    
    def _evaluate_conditions(
        self,
        conditions: list[EventCondition],
        context: dict[str, Any]
    ) -> bool:
        """Evaluate all conditions (AND logic)."""
        return all(cond.evaluate(context) for cond in conditions)
    
    def _get_entity_id(self, entity: Any) -> str:
        """Extract entity ID from entity."""
        # Try common ID field names
        for field in ["entity_id", "patient_id", "member_id", "id"]:
            if hasattr(entity, field):
                return str(getattr(entity, field))
            if isinstance(entity, dict) and field in entity:
                return str(entity[field])
        
        # Fallback to hash
        return hashlib.md5(str(entity).encode()).hexdigest()[:12]
    
    def _derive_seed(self, entity_id: str, event_id: str) -> int:
        """Derive a deterministic seed from entity and event IDs."""
        combined = f"{self.seed or 0}:{entity_id}:{event_id}"
        return int(hashlib.md5(combined.encode()).hexdigest()[:8], 16)
    
    def _generate_event_id(self, entity_id: str, event_def_id: str) -> str:
        """Generate unique timeline event ID."""
        return f"{entity_id}_{event_def_id}_{self._derive_seed(entity_id, event_def_id)}"



# =============================================================================
# Convenience Functions
# =============================================================================

def create_journey_engine(seed: int | None = None) -> JourneyEngine:
    """Create a journey engine with default configuration.
    
    Args:
        seed: Random seed for reproducibility
        
    Returns:
        Configured JourneyEngine instance
    """
    return JourneyEngine(seed=seed)


def create_simple_journey(
    journey_id: str,
    name: str,
    events: list[dict[str, Any]],
    products: list[str] | None = None,
) -> JourneySpecification:
    """Create a simple journey from a list of event dicts.
    
    Args:
        journey_id: Unique identifier
        name: Human-readable name
        events: List of event definitions
        products: Target products
        
    Returns:
        JourneySpecification
        
    Example:
        >>> journey = create_simple_journey(
        ...     "diabetic-first-year",
        ...     "First Year of Diabetic Care",
        ...     events=[
        ...         {"event_id": "e1", "name": "Initial Diagnosis", 
        ...          "event_type": "diagnosis", "delay": {"days": 0}},
        ...         {"event_id": "e2", "name": "A1C Test", 
        ...          "event_type": "lab_order", "delay": {"days": 7}, "depends_on": "e1"},
        ...     ]
        ... )
    """
    event_defs = []
    for event_dict in events:
        # Convert delay dict to DelaySpec if needed
        if "delay" in event_dict and isinstance(event_dict["delay"], dict):
            event_dict["delay"] = DelaySpec(**event_dict["delay"])
        
        # Convert conditions
        if "conditions" in event_dict:
            event_dict["conditions"] = [
                EventCondition(**c) if isinstance(c, dict) else c
                for c in event_dict["conditions"]
            ]
        
        event_defs.append(EventDefinition(**event_dict))
    
    return JourneySpecification(
        journey_id=journey_id,
        name=name,
        products=products or ["patientsim"],
        events=event_defs,
    )


# =============================================================================
# Built-in Journey Templates
# =============================================================================

JOURNEY_TEMPLATES = {
    "diabetic-first-year": {
        "journey_id": "diabetic-first-year",
        "name": "First Year of Diabetic Care",
        "description": "Standard care journey for newly diagnosed Type 2 diabetes",
        "products": ["patientsim", "membersim"],
        "duration_days": 365,
        "events": [
            {
                "event_id": "initial_dx",
                "name": "Initial Diabetes Diagnosis",
                "event_type": "diagnosis",
                "product": "patientsim",
                "delay": {"days": 0},
                "parameters": {"icd10": "E11.9", "description": "Type 2 diabetes mellitus without complications"},
            },
            {
                "event_id": "initial_a1c",
                "name": "Initial A1C Test",
                "event_type": "lab_order",
                "product": "patientsim",
                "delay": {"days": 0, "days_min": 0, "days_max": 7, "distribution": "uniform"},
                "depends_on": "initial_dx",
                "parameters": {"loinc": "4548-4", "test_name": "Hemoglobin A1c"},
            },
            {
                "event_id": "metformin_start",
                "name": "Start Metformin",
                "event_type": "medication_order",
                "product": "patientsim",
                "delay": {"days": 3, "days_min": 1, "days_max": 7, "distribution": "uniform"},
                "depends_on": "initial_dx",
                "parameters": {"rxnorm": "860975", "drug_name": "Metformin 500 MG"},
            },
            {
                "event_id": "followup_1",
                "name": "3-Month Follow-up",
                "event_type": "encounter",
                "product": "patientsim",
                "delay": {"days": 90, "days_min": 80, "days_max": 100, "distribution": "uniform"},
                "depends_on": "initial_dx",
            },
            {
                "event_id": "followup_a1c",
                "name": "3-Month A1C",
                "event_type": "lab_order",
                "product": "patientsim",
                "delay": {"days": 0},
                "depends_on": "followup_1",
            },
            {
                "event_id": "quality_gap",
                "name": "A1C Gap Identified",
                "event_type": "gap_identified",
                "product": "membersim",
                "delay": {"days": 30},
                "depends_on": "initial_dx",
                "probability": 0.3,
                "parameters": {"measure": "CDC", "description": "A1C not completed within 90 days"},
            },
        ],
    },
    
    "new-member-onboarding": {
        "journey_id": "new-member-onboarding",
        "name": "New Member Onboarding",
        "description": "Standard journey for new health plan enrollment",
        "products": ["membersim"],
        "duration_days": 90,
        "events": [
            {
                "event_id": "enrollment",
                "name": "New Enrollment",
                "event_type": "new_enrollment",
                "product": "membersim",
                "delay": {"days": 0},
            },
            {
                "event_id": "id_card",
                "name": "ID Card Generated",
                "event_type": "milestone",
                "product": "membersim",
                "delay": {"days": 3, "days_min": 2, "days_max": 5, "distribution": "uniform"},
                "depends_on": "enrollment",
            },
            {
                "event_id": "welcome_call",
                "name": "Welcome Call",
                "event_type": "milestone",
                "product": "membersim",
                "delay": {"days": 14, "days_min": 7, "days_max": 21, "distribution": "uniform"},
                "depends_on": "enrollment",
                "probability": 0.6,
            },
            {
                "event_id": "hra",
                "name": "Health Risk Assessment",
                "event_type": "milestone",
                "product": "membersim",
                "delay": {"days": 30, "days_min": 14, "days_max": 60, "distribution": "uniform"},
                "depends_on": "enrollment",
                "probability": 0.4,
            },
        ],
    },
    
    # =========================================================================
    # TrialSim Journey Templates
    # =========================================================================
    
    "phase3-pivotal-subject": {
        "journey_id": "phase3-pivotal-subject",
        "name": "Phase 3 Pivotal Trial Subject Journey",
        "description": "Standard subject journey through a Phase 3 pivotal trial",
        "products": ["trialsim"],
        "duration_days": 365,
        "events": [
            {
                "event_id": "screening",
                "name": "Screening Visit",
                "event_type": "screening",
                "product": "trialsim",
                "delay": {"days": 0},
                "parameters": {"pass_rate": 0.75},
            },
            {
                "event_id": "randomization",
                "name": "Randomization",
                "event_type": "randomization",
                "product": "trialsim",
                "delay": {"days": 14, "days_min": 7, "days_max": 28, "distribution": "uniform"},
                "depends_on": "screening",
                "parameters": {"arm_weights": {"Treatment": 0.5, "Placebo": 0.5}},
            },
            {
                "event_id": "baseline_visit",
                "name": "Baseline Visit (Day 1)",
                "event_type": "scheduled_visit",
                "product": "trialsim",
                "delay": {"days": 0},
                "depends_on": "randomization",
                "parameters": {"visit_number": 1, "visit_name": "Baseline"},
            },
            {
                "event_id": "visit_2",
                "name": "Week 4 Visit",
                "event_type": "scheduled_visit",
                "product": "trialsim",
                "delay": {"days": 28, "days_min": 25, "days_max": 35, "distribution": "uniform"},
                "depends_on": "baseline_visit",
                "parameters": {"visit_number": 2, "visit_name": "Week 4"},
            },
            {
                "event_id": "visit_3",
                "name": "Week 12 Visit",
                "event_type": "scheduled_visit",
                "product": "trialsim",
                "delay": {"days": 56, "days_min": 50, "days_max": 63, "distribution": "uniform"},
                "depends_on": "visit_2",
                "parameters": {"visit_number": 3, "visit_name": "Week 12"},
            },
            {
                "event_id": "visit_4",
                "name": "Week 24 Visit",
                "event_type": "scheduled_visit",
                "product": "trialsim",
                "delay": {"days": 84, "days_min": 77, "days_max": 91, "distribution": "uniform"},
                "depends_on": "visit_3",
                "parameters": {"visit_number": 4, "visit_name": "Week 24"},
            },
            {
                "event_id": "end_of_treatment",
                "name": "End of Treatment Visit",
                "event_type": "scheduled_visit",
                "product": "trialsim",
                "delay": {"days": 168, "days_min": 161, "days_max": 182, "distribution": "uniform"},
                "depends_on": "visit_4",
                "parameters": {"visit_number": 5, "visit_name": "End of Treatment"},
            },
        ],
    },
    
    "trial-safety-monitoring": {
        "journey_id": "trial-safety-monitoring",
        "name": "Trial Safety Monitoring Journey",
        "description": "Safety event monitoring and reporting journey",
        "products": ["trialsim"],
        "duration_days": 180,
        "events": [
            {
                "event_id": "baseline_labs",
                "name": "Baseline Safety Labs",
                "event_type": "scheduled_visit",
                "product": "trialsim",
                "delay": {"days": 0},
                "parameters": {"visit_name": "Safety Baseline", "procedures": ["CBC", "CMP", "LFTs"]},
            },
            {
                "event_id": "ae_mild",
                "name": "Mild Adverse Event",
                "event_type": "adverse_event",
                "product": "trialsim",
                "delay": {"days": 21, "days_min": 7, "days_max": 60, "distribution": "uniform"},
                "depends_on": "baseline_labs",
                "probability": 0.4,
                "parameters": {"severity": "Mild", "term": "Headache"},
            },
            {
                "event_id": "safety_labs_4wk",
                "name": "4-Week Safety Labs",
                "event_type": "scheduled_visit",
                "product": "trialsim",
                "delay": {"days": 28, "days_min": 25, "days_max": 35, "distribution": "uniform"},
                "depends_on": "baseline_labs",
                "parameters": {"visit_name": "Week 4 Safety", "procedures": ["LFTs", "CBC"]},
            },
            {
                "event_id": "ae_moderate",
                "name": "Moderate Adverse Event",
                "event_type": "adverse_event",
                "product": "trialsim",
                "delay": {"days": 45, "days_min": 30, "days_max": 90, "distribution": "uniform"},
                "depends_on": "baseline_labs",
                "probability": 0.15,
                "parameters": {"severity": "Moderate", "term": "Nausea"},
            },
            {
                "event_id": "sae",
                "name": "Serious Adverse Event",
                "event_type": "serious_adverse_event",
                "product": "trialsim",
                "delay": {"days": 60, "days_min": 14, "days_max": 120, "distribution": "uniform"},
                "depends_on": "baseline_labs",
                "probability": 0.05,
                "parameters": {"severity": "Severe", "criteria": ["hospitalization"]},
            },
        ],
    },
    
    "phase1-dose-escalation": {
        "journey_id": "phase1-dose-escalation",
        "name": "Phase 1 Dose Escalation Journey",
        "description": "First-in-human dose escalation trial journey",
        "products": ["trialsim"],
        "duration_days": 56,
        "events": [
            {
                "event_id": "screening",
                "name": "Screening Visit",
                "event_type": "screening",
                "product": "trialsim",
                "delay": {"days": 0},
                "parameters": {"pass_rate": 0.6},
            },
            {
                "event_id": "dose_1",
                "name": "First Dose Administration",
                "event_type": "scheduled_visit",
                "product": "trialsim",
                "delay": {"days": 7, "days_min": 5, "days_max": 14, "distribution": "uniform"},
                "depends_on": "screening",
                "parameters": {"visit_name": "Dose 1", "dose_level": 1},
            },
            {
                "event_id": "pk_sampling",
                "name": "PK Sampling Visit",
                "event_type": "scheduled_visit",
                "product": "trialsim",
                "delay": {"days": 1},
                "depends_on": "dose_1",
                "parameters": {"visit_name": "PK Day 2", "procedures": ["PK sampling"]},
            },
            {
                "event_id": "safety_review",
                "name": "Safety Review",
                "event_type": "scheduled_visit",
                "product": "trialsim",
                "delay": {"days": 7},
                "depends_on": "dose_1",
                "parameters": {"visit_name": "Safety Review"},
            },
            {
                "event_id": "dlt_assessment",
                "name": "DLT Assessment",
                "event_type": "adverse_event",
                "product": "trialsim",
                "delay": {"days": 21, "days_min": 14, "days_max": 28, "distribution": "uniform"},
                "depends_on": "dose_1",
                "probability": 0.15,
                "parameters": {"term": "Dose-limiting toxicity", "severity": "Severe"},
            },
        ],
    },
    
    "trial-subject-withdrawal": {
        "journey_id": "trial-subject-withdrawal",
        "name": "Trial Subject Withdrawal Journey",
        "description": "Journey for subject early termination from trial",
        "products": ["trialsim"],
        "duration_days": 30,
        "events": [
            {
                "event_id": "withdrawal_decision",
                "name": "Withdrawal Decision",
                "event_type": "withdrawal",
                "product": "trialsim",
                "delay": {"days": 0},
                "parameters": {"reason": "Subject decision", "type": "consent_withdrawn"},
            },
            {
                "event_id": "early_term_visit",
                "name": "Early Termination Visit",
                "event_type": "scheduled_visit",
                "product": "trialsim",
                "delay": {"days": 7, "days_min": 3, "days_max": 14, "distribution": "uniform"},
                "depends_on": "withdrawal_decision",
                "parameters": {"visit_name": "Early Termination"},
            },
            {
                "event_id": "final_safety_labs",
                "name": "Final Safety Labs",
                "event_type": "scheduled_visit",
                "product": "trialsim",
                "delay": {"days": 0},
                "depends_on": "early_term_visit",
                "parameters": {"visit_name": "Safety Labs", "procedures": ["CBC", "CMP", "LFTs"]},
            },
            {
                "event_id": "follow_up_call",
                "name": "30-Day Follow-up Call",
                "event_type": "scheduled_visit",
                "product": "trialsim",
                "delay": {"days": 30},
                "depends_on": "early_term_visit",
                "parameters": {"visit_name": "Safety Follow-up", "visit_type": "phone"},
            },
        ],
    },
    
    "protocol-deviation-journey": {
        "journey_id": "protocol-deviation-journey",
        "name": "Protocol Deviation Management Journey",
        "description": "Handling of protocol deviations and corrective actions",
        "products": ["trialsim"],
        "duration_days": 14,
        "events": [
            {
                "event_id": "deviation_identified",
                "name": "Protocol Deviation Identified",
                "event_type": "protocol_deviation",
                "product": "trialsim",
                "delay": {"days": 0},
                "parameters": {"category": "Visit window", "severity": "Minor"},
            },
            {
                "event_id": "deviation_documented",
                "name": "Deviation Documentation",
                "event_type": "scheduled_visit",
                "product": "trialsim",
                "delay": {"days": 1, "days_min": 0, "days_max": 3, "distribution": "uniform"},
                "depends_on": "deviation_identified",
                "parameters": {"visit_name": "Documentation"},
            },
            {
                "event_id": "corrective_action",
                "name": "Corrective Action Implemented",
                "event_type": "scheduled_visit",
                "product": "trialsim",
                "delay": {"days": 7, "days_min": 3, "days_max": 14, "distribution": "uniform"},
                "depends_on": "deviation_documented",
                "parameters": {"visit_name": "CAPA Implementation"},
            },
        ],
    },
    
    "trial-dose-modification": {
        "journey_id": "trial-dose-modification",
        "name": "Trial Dose Modification Journey",
        "description": "Journey for dose reduction or interruption due to toxicity",
        "products": ["trialsim"],
        "duration_days": 42,
        "events": [
            {
                "event_id": "toxicity_event",
                "name": "Toxicity Event Reported",
                "event_type": "adverse_event",
                "product": "trialsim",
                "delay": {"days": 0},
                "parameters": {"term": "Drug-related toxicity", "severity": "Moderate"},
            },
            {
                "event_id": "dose_hold",
                "name": "Dose Hold Decision",
                "event_type": "dose_modification",
                "product": "trialsim",
                "delay": {"days": 1, "days_min": 0, "days_max": 2, "distribution": "uniform"},
                "depends_on": "toxicity_event",
                "parameters": {"type": "dose_hold", "reason": "Toxicity"},
            },
            {
                "event_id": "recovery_assessment",
                "name": "Recovery Assessment",
                "event_type": "scheduled_visit",
                "product": "trialsim",
                "delay": {"days": 14, "days_min": 7, "days_max": 21, "distribution": "uniform"},
                "depends_on": "dose_hold",
                "parameters": {"visit_name": "Recovery Check"},
            },
            {
                "event_id": "dose_reduction",
                "name": "Dose Reduction",
                "event_type": "dose_modification",
                "product": "trialsim",
                "delay": {"days": 1, "days_min": 0, "days_max": 3, "distribution": "uniform"},
                "depends_on": "recovery_assessment",
                "parameters": {"type": "dose_reduction", "reduction_level": 1},
            },
            {
                "event_id": "resumed_treatment",
                "name": "Treatment Resumed at Reduced Dose",
                "event_type": "scheduled_visit",
                "product": "trialsim",
                "delay": {"days": 0},
                "depends_on": "dose_reduction",
                "parameters": {"visit_name": "Treatment Restart"},
            },
        ],
    },
}


def get_journey_template(template_name: str) -> JourneySpecification:
    """Get a built-in journey template.
    
    Args:
        template_name: Name of the template
        
    Returns:
        JourneySpecification
        
    Raises:
        ValueError: If template not found
    """
    if template_name not in JOURNEY_TEMPLATES:
        available = ", ".join(JOURNEY_TEMPLATES.keys())
        raise ValueError(f"Template '{template_name}' not found. Available: {available}")
    
    template = JOURNEY_TEMPLATES[template_name]
    return create_simple_journey(
        journey_id=template["journey_id"],
        name=template["name"],
        events=template["events"],
        products=template.get("products"),
    )
