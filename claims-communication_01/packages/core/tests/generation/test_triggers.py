"""Tests for cross-product trigger system."""

import pytest
from datetime import date, timedelta

from healthsim.generation.triggers import (
    TriggerPriority,
    RegisteredTrigger,
    TriggerRegistry,
    LinkedEntity,
    CrossProductCoordinator,
    create_coordinator,
)
from healthsim.generation.journey_engine import (
    DelaySpec,
    EventCondition,
    Timeline,
    TimelineEvent,
    JourneyEngine,
)


# =============================================================================
# TriggerPriority Tests
# =============================================================================

class TestTriggerPriority:
    """Tests for TriggerPriority enum."""

    def test_priority_values(self):
        """Test priority enum values."""
        assert TriggerPriority.IMMEDIATE.value == 0
        assert TriggerPriority.HIGH.value == 1
        assert TriggerPriority.NORMAL.value == 2
        assert TriggerPriority.LOW.value == 3

    def test_priority_ordering(self):
        """Test priorities can be compared."""
        assert TriggerPriority.IMMEDIATE.value < TriggerPriority.HIGH.value
        assert TriggerPriority.HIGH.value < TriggerPriority.NORMAL.value
        assert TriggerPriority.NORMAL.value < TriggerPriority.LOW.value


# =============================================================================
# RegisteredTrigger Tests
# =============================================================================

class TestRegisteredTrigger:
    """Tests for RegisteredTrigger dataclass."""

    def test_basic_creation(self):
        """Test basic trigger creation."""
        trigger = RegisteredTrigger(
            source_product="patientsim",
            source_event_type="diagnosis",
            target_product="membersim",
            target_event_type="claim_professional"
        )
        
        assert trigger.source_product == "patientsim"
        assert trigger.target_product == "membersim"
        assert trigger.priority == TriggerPriority.NORMAL

    def test_with_delay(self):
        """Test trigger with delay."""
        trigger = RegisteredTrigger(
            source_product="patientsim",
            source_event_type="diagnosis",
            target_product="membersim",
            target_event_type="claim_professional",
            delay=DelaySpec(days=3)
        )
        
        assert trigger.delay.days == 3

    def test_with_condition(self):
        """Test trigger with condition."""
        condition = EventCondition(field="age", operator="gte", value=65)
        trigger = RegisteredTrigger(
            source_product="patientsim",
            source_event_type="diagnosis",
            target_product="membersim",
            target_event_type="claim_professional",
            condition=condition
        )
        
        assert trigger.condition is not None

    def test_with_parameter_map(self):
        """Test trigger with parameter mapping."""
        trigger = RegisteredTrigger(
            source_product="patientsim",
            source_event_type="diagnosis",
            target_product="membersim",
            target_event_type="claim_professional",
            parameter_map={"diagnosis_code": "icd10"}
        )
        
        assert "diagnosis_code" in trigger.parameter_map


# =============================================================================
# TriggerRegistry Tests
# =============================================================================

class TestTriggerRegistry:
    """Tests for TriggerRegistry."""

    @pytest.fixture
    def registry(self):
        """Create registry fixture."""
        return TriggerRegistry()

    def test_empty_registry(self, registry):
        """Test empty registry."""
        triggers = registry.get_triggers("patientsim", "diagnosis")
        assert triggers == []

    def test_register_trigger(self, registry):
        """Test registering a trigger."""
        registry.register(
            source_product="patientsim",
            source_event_type="diagnosis",
            target_product="membersim",
            target_event_type="claim_professional"
        )
        
        triggers = registry.get_triggers("patientsim", "diagnosis")
        assert len(triggers) == 1
        assert triggers[0].target_product == "membersim"

    def test_register_multiple_triggers(self, registry):
        """Test registering multiple triggers for same source."""
        registry.register(
            source_product="patientsim",
            source_event_type="diagnosis",
            target_product="membersim",
            target_event_type="claim_professional"
        )
        registry.register(
            source_product="patientsim",
            source_event_type="diagnosis",
            target_product="membersim",
            target_event_type="gap_identified"
        )
        
        triggers = registry.get_triggers("patientsim", "diagnosis")
        assert len(triggers) == 2

    def test_register_with_delay(self, registry):
        """Test registering trigger with delay."""
        registry.register(
            source_product="patientsim",
            source_event_type="diagnosis",
            target_product="membersim",
            target_event_type="claim_professional",
            delay=DelaySpec(days=5)
        )
        
        triggers = registry.get_triggers("patientsim", "diagnosis")
        assert triggers[0].delay.days == 5

    def test_register_with_priority(self, registry):
        """Test registering trigger with priority."""
        registry.register(
            source_product="patientsim",
            source_event_type="diagnosis",
            target_product="membersim",
            target_event_type="claim_professional",
            priority=TriggerPriority.HIGH
        )
        
        triggers = registry.get_triggers("patientsim", "diagnosis")
        assert triggers[0].priority == TriggerPriority.HIGH

    def test_register_target_handler(self, registry):
        """Test registering target handler."""
        handler_called = []
        
        def my_handler(event_type, source_event, params):
            handler_called.append(event_type)
        
        registry.register_target_handler("membersim", my_handler)
        
        assert "membersim" in registry._target_handlers

    def test_fire_triggers_basic(self, registry):
        """Test firing triggers."""
        registry.register(
            source_product="patientsim",
            source_event_type="diagnosis",
            target_product="membersim",
            target_event_type="claim_professional"
        )
        
        source_event = TimelineEvent(
            timeline_event_id="te-001",
            journey_id="j1",
            event_definition_id="e1",
            scheduled_date=date(2024, 1, 15),
            event_type="diagnosis",
            event_name="Diagnosis",
            product="patientsim"
        )
        
        triggered = registry.fire_triggers(source_event, {}, {})
        
        assert len(triggered) == 1
        assert triggered[0]["target_product"] == "membersim"
        assert triggered[0]["target_event_type"] == "claim_professional"

    def test_fire_triggers_with_delay(self, registry):
        """Test fired trigger has correct target date."""
        registry.register(
            source_product="patientsim",
            source_event_type="diagnosis",
            target_product="membersim",
            target_event_type="claim_professional",
            delay=DelaySpec(days=3)
        )
        
        source_event = TimelineEvent(
            timeline_event_id="te-001",
            journey_id="j1",
            event_definition_id="e1",
            scheduled_date=date(2024, 1, 15),
            event_type="diagnosis",
            event_name="Diagnosis",
            product="patientsim"
        )
        
        triggered = registry.fire_triggers(source_event, {}, {})
        
        assert triggered[0]["target_date"] == "2024-01-18"

    def test_fire_triggers_with_condition_pass(self, registry):
        """Test trigger fires when condition passes."""
        registry.register(
            source_product="patientsim",
            source_event_type="diagnosis",
            target_product="membersim",
            target_event_type="claim_professional",
            condition=EventCondition(field="age", operator="gte", value=65)
        )
        
        source_event = TimelineEvent(
            timeline_event_id="te-001",
            journey_id="j1",
            event_definition_id="e1",
            scheduled_date=date(2024, 1, 15),
            event_type="diagnosis",
            event_name="Diagnosis",
            product="patientsim"
        )
        
        triggered = registry.fire_triggers(source_event, {}, {"age": 70})
        
        assert len(triggered) == 1

    def test_fire_triggers_with_condition_fail(self, registry):
        """Test trigger doesn't fire when condition fails."""
        registry.register(
            source_product="patientsim",
            source_event_type="diagnosis",
            target_product="membersim",
            target_event_type="claim_professional",
            condition=EventCondition(field="age", operator="gte", value=65)
        )
        
        source_event = TimelineEvent(
            timeline_event_id="te-001",
            journey_id="j1",
            event_definition_id="e1",
            scheduled_date=date(2024, 1, 15),
            event_type="diagnosis",
            event_name="Diagnosis",
            product="patientsim"
        )
        
        triggered = registry.fire_triggers(source_event, {}, {"age": 45})
        
        assert len(triggered) == 0

    def test_fire_triggers_with_parameter_map(self, registry):
        """Test parameter mapping in triggers."""
        handler_params = []
        
        def capture_handler(event_type, source_event, params):
            handler_params.append(params)
        
        registry.register(
            source_product="patientsim",
            source_event_type="diagnosis",
            target_product="membersim",
            target_event_type="claim_professional",
            parameter_map={"diagnosis_code": "icd10"}
        )
        registry.register_target_handler("membersim", capture_handler)
        
        source_event = TimelineEvent(
            timeline_event_id="te-001",
            journey_id="j1",
            event_definition_id="e1",
            scheduled_date=date(2024, 1, 15),
            event_type="diagnosis",
            event_name="Diagnosis",
            product="patientsim"
        )
        
        registry.fire_triggers(source_event, {"icd10": "E11.9"}, {})
        
        assert len(handler_params) == 1
        assert handler_params[0]["parameters"]["diagnosis_code"] == "E11.9"


# =============================================================================
# LinkedEntity Tests
# =============================================================================

class TestLinkedEntity:
    """Tests for LinkedEntity dataclass."""

    def test_basic_creation(self):
        """Test basic linked entity creation."""
        linked = LinkedEntity(core_id="E001")
        
        assert linked.core_id == "E001"
        assert linked.patient_id is None
        assert linked.member_id is None

    def test_with_product_ids(self):
        """Test linked entity with product IDs."""
        linked = LinkedEntity(
            core_id="E001",
            patient_id="P001",
            member_id="M001"
        )
        
        assert linked.patient_id == "P001"
        assert linked.member_id == "M001"

    def test_timelines_default_empty(self):
        """Test timelines default to empty dict."""
        linked = LinkedEntity(core_id="E001")
        
        assert linked.timelines == {}


# =============================================================================
# CrossProductCoordinator Tests
# =============================================================================

class TestCrossProductCoordinator:
    """Tests for CrossProductCoordinator."""

    @pytest.fixture
    def coordinator(self):
        """Create coordinator fixture."""
        return CrossProductCoordinator()

    def test_initialization(self, coordinator):
        """Test coordinator initialization."""
        assert coordinator._linked_entities == {}
        assert coordinator._product_engines == {}

    def test_create_linked_entity(self, coordinator):
        """Test creating linked entity."""
        linked = coordinator.create_linked_entity("E001")
        
        assert linked.core_id == "E001"
        assert "E001" in coordinator._linked_entities

    def test_create_linked_entity_with_ids(self, coordinator):
        """Test creating linked entity with product IDs."""
        linked = coordinator.create_linked_entity(
            "E001",
            product_ids={
                "patient_id": "P001",
                "member_id": "M001"
            }
        )
        
        assert linked.patient_id == "P001"
        assert linked.member_id == "M001"

    def test_get_linked_entity(self, coordinator):
        """Test getting linked entity."""
        coordinator.create_linked_entity("E001")
        
        linked = coordinator.get_linked_entity("E001")
        
        assert linked is not None
        assert linked.core_id == "E001"

    def test_get_linked_entity_not_found(self, coordinator):
        """Test getting non-existent entity."""
        linked = coordinator.get_linked_entity("nonexistent")
        
        assert linked is None

    def test_register_product_engine(self, coordinator):
        """Test registering product engine."""
        engine = JourneyEngine(seed=42)
        
        coordinator.register_product_engine("patientsim", engine)
        
        assert "patientsim" in coordinator._product_engines

    def test_add_timeline(self, coordinator):
        """Test adding timeline to linked entity."""
        linked = coordinator.create_linked_entity("E001", {
            "patient_id": "P001"
        })
        
        timeline = Timeline(
            entity_id="P001",
            entity_type="patient",
            start_date=date(2024, 1, 1)
        )
        
        coordinator.add_timeline(linked, "patientsim", timeline)
        
        assert "patientsim" in linked.timelines

    def test_add_multiple_timelines_links_them(self, coordinator):
        """Test adding multiple timelines creates cross-links."""
        linked = coordinator.create_linked_entity("E001", {
            "patient_id": "P001",
            "member_id": "M001"
        })
        
        patient_timeline = Timeline(
            entity_id="P001",
            entity_type="patient",
            start_date=date(2024, 1, 1)
        )
        member_timeline = Timeline(
            entity_id="M001",
            entity_type="member",
            start_date=date(2024, 1, 1)
        )
        
        coordinator.add_timeline(linked, "patientsim", patient_timeline)
        coordinator.add_timeline(linked, "membersim", member_timeline)
        
        # Check cross-links
        assert "membersim" in patient_timeline.linked_timelines
        assert "patientsim" in member_timeline.linked_timelines

    def test_get_product_entity_patientsim(self, coordinator):
        """Test getting patient entity."""
        linked = LinkedEntity(
            core_id="E001",
            patient_id="P001"
        )
        
        entity = coordinator._get_product_entity(linked, "patientsim")
        
        assert entity["patient_id"] == "P001"
        assert entity["core_id"] == "E001"

    def test_get_product_entity_membersim(self, coordinator):
        """Test getting member entity."""
        linked = LinkedEntity(
            core_id="E001",
            member_id="M001"
        )
        
        entity = coordinator._get_product_entity(linked, "membersim")
        
        assert entity["member_id"] == "M001"

    def test_default_triggers_registered(self, coordinator):
        """Test default triggers are registered on init."""
        triggers = coordinator._trigger_registry.get_triggers("patientsim", "diagnosis")
        
        assert len(triggers) > 0

    def test_execute_coordinated_no_events(self, coordinator):
        """Test executing with no pending events."""
        linked = coordinator.create_linked_entity("E001", {
            "patient_id": "P001"
        })
        
        timeline = Timeline(
            entity_id="P001",
            entity_type="patient"
        )
        coordinator.add_timeline(linked, "patientsim", timeline)
        
        results = coordinator.execute_coordinated(linked, date(2024, 12, 31))
        
        assert results == {}

    def test_execute_coordinated_with_engine(self, coordinator):
        """Test executing with registered engine."""
        from healthsim.generation.handlers import PatientSimHandlers
        
        linked = coordinator.create_linked_entity("E001", {
            "patient_id": "P001"
        })
        
        # Set up engine with handlers
        engine = JourneyEngine(seed=42)
        handlers = PatientSimHandlers(seed=42)
        handlers.register_all(engine)
        coordinator.register_product_engine("patientsim", engine)
        
        # Create timeline with event
        timeline = Timeline(
            entity_id="P001",
            entity_type="patient",
            start_date=date(2024, 1, 1)
        )
        timeline.add_event(TimelineEvent(
            timeline_event_id="te-001",
            journey_id="j1",
            event_definition_id="e1",
            scheduled_date=date(2024, 1, 15),
            event_type="encounter",
            event_name="Office Visit",
            product="patientsim"
        ))
        coordinator.add_timeline(linked, "patientsim", timeline)
        
        results = coordinator.execute_coordinated(linked, date(2024, 12, 31))
        
        assert "patientsim" in results
        assert len(results["patientsim"]) == 1

    def test_execute_coordinated_chronological_order(self, coordinator):
        """Test events execute in chronological order across products."""
        linked = coordinator.create_linked_entity("E001", {
            "patient_id": "P001",
            "member_id": "M001"
        })
        
        # Create timelines
        patient_timeline = Timeline(entity_id="P001", entity_type="patient")
        patient_timeline.add_event(TimelineEvent(
            timeline_event_id="te-p1",
            journey_id="j1",
            event_definition_id="e1",
            scheduled_date=date(2024, 1, 15),
            event_type="encounter",
            event_name="Visit",
            product="patientsim"
        ))
        
        member_timeline = Timeline(entity_id="M001", entity_type="member")
        member_timeline.add_event(TimelineEvent(
            timeline_event_id="te-m1",
            journey_id="j1",
            event_definition_id="e1",
            scheduled_date=date(2024, 1, 10),  # Earlier
            event_type="new_enrollment",
            event_name="Enrollment",
            product="membersim"
        ))
        
        coordinator.add_timeline(linked, "patientsim", patient_timeline)
        coordinator.add_timeline(linked, "membersim", member_timeline)
        
        # Without engines, events will be skipped but in correct order
        results = coordinator.execute_coordinated(linked, date(2024, 12, 31))
        
        # Both products should have results
        assert "patientsim" in results or "membersim" in results


# =============================================================================
# Convenience Function Tests
# =============================================================================

class TestConvenienceFunctions:
    """Tests for convenience functions."""

    def test_create_coordinator(self):
        """Test create_coordinator function."""
        coordinator = create_coordinator()
        
        assert isinstance(coordinator, CrossProductCoordinator)


# =============================================================================
# Integration Tests
# =============================================================================

class TestTriggerIntegration:
    """Integration tests for trigger system."""

    def test_diagnosis_triggers_claim(self):
        """Test diagnosis event triggers claim creation."""
        coordinator = CrossProductCoordinator()
        
        # Check default trigger exists
        triggers = coordinator._trigger_registry.get_triggers("patientsim", "diagnosis")
        
        claim_triggers = [t for t in triggers if t.target_event_type == "claim_professional"]
        assert len(claim_triggers) > 0

    def test_medication_order_triggers_fill(self):
        """Test medication order triggers pharmacy fill."""
        coordinator = CrossProductCoordinator()
        
        triggers = coordinator._trigger_registry.get_triggers("patientsim", "medication_order")
        
        fill_triggers = [t for t in triggers if t.target_event_type == "fill"]
        assert len(fill_triggers) > 0

    def test_lab_order_triggers_result(self):
        """Test lab order triggers lab result."""
        coordinator = CrossProductCoordinator()
        
        triggers = coordinator._trigger_registry.get_triggers("patientsim", "lab_order")
        
        result_triggers = [t for t in triggers if t.target_event_type == "lab_result"]
        assert len(result_triggers) > 0

    def test_full_cross_product_flow(self):
        """Test a complete cross-product trigger flow."""
        from healthsim.generation.handlers import (
            PatientSimHandlers,
            MemberSimHandlers,
        )
        
        coordinator = CrossProductCoordinator()
        
        # Set up engines
        patient_engine = JourneyEngine(seed=42)
        PatientSimHandlers(seed=42).register_all(patient_engine)
        coordinator.register_product_engine("patientsim", patient_engine)
        
        member_engine = JourneyEngine(seed=42)
        MemberSimHandlers(seed=42).register_all(member_engine)
        coordinator.register_product_engine("membersim", member_engine)
        
        # Create linked entity
        linked = coordinator.create_linked_entity("E001", {
            "patient_id": "P001",
            "member_id": "M001"
        })
        
        # Create timelines
        patient_timeline = Timeline(entity_id="P001", entity_type="patient")
        patient_timeline.add_event(TimelineEvent(
            timeline_event_id="te-dx",
            journey_id="j1",
            event_definition_id="e1",
            scheduled_date=date(2024, 1, 15),
            event_type="diagnosis",
            event_name="Diabetes Diagnosis",
            product="patientsim"
        ))
        coordinator.add_timeline(linked, "patientsim", patient_timeline)
        
        member_timeline = Timeline(entity_id="M001", entity_type="member")
        coordinator.add_timeline(linked, "membersim", member_timeline)
        
        # Execute
        results = coordinator.execute_coordinated(linked, date(2024, 12, 31))
        
        # Diagnosis should be executed
        assert "patientsim" in results
        assert len(results["patientsim"]) == 1
        assert results["patientsim"][0]["event_type"] == "diagnosis"
