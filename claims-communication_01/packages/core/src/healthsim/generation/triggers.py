"""Cross-product trigger system for event coordination.

This module handles the dispatch and coordination of events across
different HealthSim products (PatientSim, MemberSim, RxMemberSim, etc.).

The trigger system enables scenarios like:
- Patient diagnosis (PatientSim) triggers a claim (MemberSim)
- Medication order (PatientSim) triggers a fill (RxMemberSim)
- Quality gap (MemberSim) triggers an outreach event (PatientSim)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Any, Callable, Protocol
from enum import Enum
import logging

from healthsim.generation.journey_engine import (
    DelaySpec,
    EventCondition,
    Timeline,
    TimelineEvent,
    TriggerSpec,
)

logger = logging.getLogger(__name__)


# =============================================================================
# Trigger Registry
# =============================================================================

class TriggerPriority(Enum):
    """Priority levels for trigger execution."""
    IMMEDIATE = 0  # Execute same day
    HIGH = 1       # Execute within 1-3 days
    NORMAL = 2     # Execute per delay spec
    LOW = 3        # Execute when convenient


@dataclass
class RegisteredTrigger:
    """A registered cross-product trigger."""
    
    source_product: str
    source_event_type: str
    target_product: str
    target_event_type: str
    
    # Trigger behavior
    delay: DelaySpec = field(default_factory=DelaySpec)
    priority: TriggerPriority = TriggerPriority.NORMAL
    condition: EventCondition | None = None
    
    # Parameter mapping
    parameter_map: dict[str, str] = field(default_factory=dict)
    
    # Handler for custom logic
    handler: Callable | None = None


class TriggerRegistry:
    """Registry of cross-product triggers.
    
    The registry maintains mappings between source events and
    the triggers they activate in other products.
    
    Example:
        >>> registry = TriggerRegistry()
        >>> registry.register(
        ...     source_product="patientsim",
        ...     source_event_type="diagnosis",
        ...     target_product="membersim",
        ...     target_event_type="claim_professional",
        ...     delay=DelaySpec(days=3),
        ... )
    """
    
    def __init__(self):
        # Triggers indexed by source: {(product, event_type): [triggers]}
        self._triggers: dict[tuple[str, str], list[RegisteredTrigger]] = {}
        
        # Target handlers by product
        self._target_handlers: dict[str, Callable] = {}
    
    def register(
        self,
        source_product: str,
        source_event_type: str,
        target_product: str,
        target_event_type: str,
        delay: DelaySpec | None = None,
        priority: TriggerPriority = TriggerPriority.NORMAL,
        condition: EventCondition | None = None,
        parameter_map: dict[str, str] | None = None,
        handler: Callable | None = None,
    ) -> None:
        """Register a cross-product trigger.
        
        Args:
            source_product: Product that fires the trigger
            source_event_type: Event type that fires the trigger
            target_product: Product that receives the trigger
            target_event_type: Event type to create in target
            delay: Delay before trigger fires
            priority: Execution priority
            condition: Optional condition for trigger
            parameter_map: Map source params to target params
            handler: Custom handler function
        """
        key = (source_product, source_event_type)
        
        trigger = RegisteredTrigger(
            source_product=source_product,
            source_event_type=source_event_type,
            target_product=target_product,
            target_event_type=target_event_type,
            delay=delay or DelaySpec(),
            priority=priority,
            condition=condition,
            parameter_map=parameter_map or {},
            handler=handler,
        )
        
        if key not in self._triggers:
            self._triggers[key] = []
        self._triggers[key].append(trigger)
    
    def register_target_handler(
        self,
        product: str,
        handler: Callable[[str, TimelineEvent, dict], None]
    ) -> None:
        """Register a handler for receiving triggers in a product.
        
        Args:
            product: Target product
            handler: Function to handle incoming triggers
        """
        self._target_handlers[product] = handler
    
    def get_triggers(
        self,
        source_product: str,
        source_event_type: str
    ) -> list[RegisteredTrigger]:
        """Get triggers for a source event."""
        return self._triggers.get((source_product, source_event_type), [])
    
    def fire_triggers(
        self,
        source_event: TimelineEvent,
        source_result: dict[str, Any],
        context: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """Fire all triggers for a source event.
        
        Args:
            source_event: The event that fired
            source_result: Result from source event execution
            context: Execution context
            
        Returns:
            List of triggered event info dicts
        """
        triggered = []
        triggers = self.get_triggers(source_event.product, source_event.event_type)
        
        for trigger in triggers:
            # Check condition if present
            if trigger.condition and not trigger.condition.evaluate(context):
                continue
            
            # Calculate target date
            target_date = source_event.scheduled_date + trigger.delay.to_timedelta()
            
            # Build target parameters
            target_params = {}
            for target_key, source_key in trigger.parameter_map.items():
                if source_key in source_result:
                    target_params[target_key] = source_result[source_key]
                elif source_key in context:
                    target_params[target_key] = context[source_key]
            
            # Dispatch to target handler if registered
            if trigger.target_product in self._target_handlers:
                handler = self._target_handlers[trigger.target_product]
                try:
                    handler(trigger.target_event_type, source_event, {
                        "target_date": target_date,
                        "parameters": target_params,
                        "source_event_id": source_event.timeline_event_id,
                    })
                except Exception as e:
                    logger.error(f"Trigger handler failed: {e}")
            
            triggered.append({
                "source_event_id": source_event.timeline_event_id,
                "target_product": trigger.target_product,
                "target_event_type": trigger.target_event_type,
                "target_date": target_date.isoformat(),
                "priority": trigger.priority.name,
            })
        
        return triggered



# =============================================================================
# Cross-Product Coordinator
# =============================================================================

@dataclass
class LinkedEntity:
    """An entity with cross-product linkage."""
    
    core_id: str  # Shared identifier across products
    
    # Product-specific IDs
    patient_id: str | None = None
    member_id: str | None = None
    rx_member_id: str | None = None
    trial_subject_id: str | None = None
    
    # Timelines by product
    timelines: dict[str, Timeline] = field(default_factory=dict)


class CrossProductCoordinator:
    """Coordinates events across multiple HealthSim products.
    
    The coordinator manages linked entities and their timelines,
    ensuring consistency across products.
    
    Example:
        >>> coordinator = CrossProductCoordinator()
        >>> 
        >>> # Create linked entity
        >>> linked = coordinator.create_linked_entity("E001", {
        ...     "patient_id": "P001",
        ...     "member_id": "M001"
        ... })
        >>> 
        >>> # Register products
        >>> coordinator.register_product_engine("patientsim", patient_engine)
        >>> coordinator.register_product_engine("membersim", member_engine)
        >>> 
        >>> # Execute coordinated journey
        >>> results = coordinator.execute_journey(
        ...     linked,
        ...     journey_spec,
        ...     start_date
        ... )
    """
    
    def __init__(self):
        self._linked_entities: dict[str, LinkedEntity] = {}
        self._product_engines: dict[str, Any] = {}  # JourneyEngine instances
        self._trigger_registry = TriggerRegistry()
        
        # Register standard healthcare triggers
        self._register_default_triggers()
    
    def create_linked_entity(
        self,
        core_id: str,
        product_ids: dict[str, str] | None = None,
    ) -> LinkedEntity:
        """Create a new linked entity.
        
        Args:
            core_id: Shared identifier
            product_ids: Dict of product -> entity_id mappings
            
        Returns:
            LinkedEntity instance
        """
        linked = LinkedEntity(core_id=core_id)
        
        if product_ids:
            if "patient_id" in product_ids:
                linked.patient_id = product_ids["patient_id"]
            if "member_id" in product_ids:
                linked.member_id = product_ids["member_id"]
            if "rx_member_id" in product_ids:
                linked.rx_member_id = product_ids["rx_member_id"]
            if "trial_subject_id" in product_ids:
                linked.trial_subject_id = product_ids["trial_subject_id"]
        
        self._linked_entities[core_id] = linked
        return linked
    
    def register_product_engine(self, product: str, engine: Any) -> None:
        """Register a product's journey engine.
        
        Args:
            product: Product identifier
            engine: JourneyEngine instance for that product
        """
        self._product_engines[product] = engine
    
    def get_linked_entity(self, core_id: str) -> LinkedEntity | None:
        """Get a linked entity by core ID."""
        return self._linked_entities.get(core_id)
    
    def add_timeline(
        self,
        linked: LinkedEntity,
        product: str,
        timeline: Timeline
    ) -> None:
        """Add a timeline to a linked entity.
        
        Args:
            linked: The linked entity
            product: Product the timeline belongs to
            timeline: The timeline to add
        """
        linked.timelines[product] = timeline
        
        # Link back to other timelines
        for other_product, other_timeline in linked.timelines.items():
            if other_product != product:
                timeline.linked_timelines[other_product] = other_timeline.entity_id
                other_timeline.linked_timelines[product] = timeline.entity_id
    
    def execute_coordinated(
        self,
        linked: LinkedEntity,
        up_to_date: date,
    ) -> dict[str, list[dict]]:
        """Execute all pending events across products.
        
        Events are executed in chronological order across all products,
        with triggers firing as events complete.
        
        Args:
            linked: The linked entity
            up_to_date: Execute events up to this date
            
        Returns:
            Dict of product -> list of execution results
        """
        results: dict[str, list[dict]] = {}
        
        # Collect all pending events across products
        all_events: list[tuple[str, Timeline, TimelineEvent]] = []
        
        for product, timeline in linked.timelines.items():
            for event in timeline.get_events_up_to(up_to_date):
                all_events.append((product, timeline, event))
        
        # Sort by scheduled date
        all_events.sort(key=lambda x: x[2].scheduled_date)
        
        # Execute in order
        for product, timeline, event in all_events:
            if product not in results:
                results[product] = []
            
            engine = self._product_engines.get(product)
            if not engine:
                results[product].append({
                    "event_id": event.timeline_event_id,
                    "status": "skipped",
                    "reason": f"No engine registered for {product}"
                })
                continue
            
            # Get entity for this product
            entity = self._get_product_entity(linked, product)
            
            # Execute event
            result = engine.execute_event(timeline, event, entity)
            results[product].append({
                "event_id": event.timeline_event_id,
                "event_type": event.event_type,
                "scheduled_date": event.scheduled_date.isoformat(),
                **result
            })
            
            # Fire cross-product triggers
            if result.get("status") == "executed":
                triggered = self._trigger_registry.fire_triggers(
                    event, 
                    result.get("outputs", {}),
                    {"linked_entity": linked}
                )
                if triggered:
                    results[product][-1]["triggered"] = triggered
        
        return results
    
    def _get_product_entity(self, linked: LinkedEntity, product: str) -> dict:
        """Get entity dict for a specific product."""
        if product == "patientsim":
            return {"patient_id": linked.patient_id, "core_id": linked.core_id}
        elif product == "membersim":
            return {"member_id": linked.member_id, "core_id": linked.core_id}
        elif product == "rxmembersim":
            return {"rx_member_id": linked.rx_member_id, "core_id": linked.core_id}
        elif product == "trialsim":
            return {"subject_id": linked.trial_subject_id, "core_id": linked.core_id}
        return {"core_id": linked.core_id}
    
    def _register_default_triggers(self) -> None:
        """Register standard healthcare cross-product triggers."""
        
        # Patient diagnosis → Member claim
        self._trigger_registry.register(
            source_product="patientsim",
            source_event_type="diagnosis",
            target_product="membersim",
            target_event_type="claim_professional",
            delay=DelaySpec(days=3, days_min=1, days_max=7, distribution="uniform"),
            parameter_map={"diagnosis_code": "icd10"},
        )
        
        # Medication order → Pharmacy claim
        self._trigger_registry.register(
            source_product="patientsim",
            source_event_type="medication_order",
            target_product="membersim",
            target_event_type="claim_pharmacy",
            delay=DelaySpec(days=1, days_min=0, days_max=3, distribution="uniform"),
            parameter_map={"ndc": "rxnorm"},
        )
        
        # Medication order → Rx fill
        self._trigger_registry.register(
            source_product="patientsim",
            source_event_type="medication_order",
            target_product="rxmembersim",
            target_event_type="fill",
            delay=DelaySpec(days=1, days_min=0, days_max=3, distribution="uniform"),
            parameter_map={"ndc": "rxnorm", "quantity": "quantity"},
        )
        
        # Lab order → Lab result
        self._trigger_registry.register(
            source_product="patientsim",
            source_event_type="lab_order",
            target_product="patientsim",
            target_event_type="lab_result",
            delay=DelaySpec(days=2, days_min=1, days_max=5, distribution="uniform"),
            parameter_map={"loinc": "loinc", "order_id": "order_id"},
        )
        
        # Quality gap → Outreach
        self._trigger_registry.register(
            source_product="membersim",
            source_event_type="gap_identified",
            target_product="patientsim",
            target_event_type="care_plan_update",
            delay=DelaySpec(days=7, days_min=3, days_max=14, distribution="uniform"),
            parameter_map={"measure": "measure", "gap_id": "gap_id"},
        )


# =============================================================================
# Convenience Functions
# =============================================================================

def create_coordinator() -> CrossProductCoordinator:
    """Create a cross-product coordinator with default configuration."""
    return CrossProductCoordinator()
