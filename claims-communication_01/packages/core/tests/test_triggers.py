"""Tests for the cross-product trigger system."""

import pytest
from datetime import date

from healthsim.generation.journey_engine import (
    DelaySpec,
    EventCondition,
    TimelineEvent,
)
from healthsim.generation.triggers import (
    CrossProductCoordinator,
    LinkedEntity,
    RegisteredTrigger,
    TriggerPriority,
    TriggerRegistry,
    create_coordinator,
)


class TestTriggerRegistry:
    """Tests for TriggerRegistry."""
    
    def test_creation(self):
        """Test creating registry."""
        registry = TriggerRegistry()
        assert registry is not None
    
    def test_register_trigger(self):
        """Test registering a trigger."""
        registry = TriggerRegistry()
        registry.register(
            source_product="patientsim",
            source_event_type="diagnosis",
            target_product="membersim",
            target_event_type="claim_professional",
            delay=DelaySpec(days=3),
        )
        
        triggers = registry.get_triggers("patientsim", "diagnosis")
        assert len(triggers) == 1
        assert triggers[0].target_product == "membersim"
    
    def test_multiple_triggers(self):
        """Test multiple triggers for same source."""
        registry = TriggerRegistry()
        registry.register(
            source_product="patientsim",
            source_event_type="medication_order",
            target_product="membersim",
            target_event_type="claim_pharmacy",
        )
        registry.register(
            source_product="patientsim",
            source_event_type="medication_order",
            target_product="rxmembersim",
            target_event_type="fill",
        )
        
        triggers = registry.get_triggers("patientsim", "medication_order")
        assert len(triggers) == 2
    
    def test_no_triggers(self):
        """Test getting triggers for unregistered event."""
        registry = TriggerRegistry()
        triggers = registry.get_triggers("unknown", "unknown")
        assert len(triggers) == 0
    
    def test_fire_triggers(self):
        """Test firing triggers."""
        registry = TriggerRegistry()
        registry.register(
            source_product="patientsim",
            source_event_type="diagnosis",
            target_product="membersim",
            target_event_type="claim_professional",
            delay=DelaySpec(days=3),
            parameter_map={"dx_code": "icd10"},
        )
        
        source_event = TimelineEvent(
            timeline_event_id="e1",
            journey_id="j1",
            event_definition_id="ed1",
            scheduled_date=date(2025, 1, 1),
            event_type="diagnosis",
            event_name="Test",
            product="patientsim",
        )
        
        triggered = registry.fire_triggers(
            source_event,
            source_result={"icd10": "E11.9"},
            context={}
        )
        
        assert len(triggered) == 1
        assert triggered[0]["target_product"] == "membersim"
        assert triggered[0]["target_date"] == "2025-01-04"
    
    def test_conditional_trigger(self):
        """Test trigger with condition."""
        registry = TriggerRegistry()
        registry.register(
            source_product="patientsim",
            source_event_type="diagnosis",
            target_product="membersim",
            target_event_type="claim",
            condition=EventCondition(field="entity.age", operator="gte", value=65),
        )
        
        source_event = TimelineEvent(
            timeline_event_id="e1", journey_id="j1", event_definition_id="ed1",
            scheduled_date=date(2025, 1, 1), event_type="diagnosis",
            event_name="Test", product="patientsim",
        )
        
        # Young patient - trigger should not fire
        triggered = registry.fire_triggers(
            source_event, {},
            context={"entity": {"age": 30}}
        )
        assert len(triggered) == 0
        
        # Senior patient - trigger should fire
        triggered = registry.fire_triggers(
            source_event, {},
            context={"entity": {"age": 70}}
        )
        assert len(triggered) == 1


class TestLinkedEntity:
    """Tests for LinkedEntity."""
    
    def test_creation(self):
        """Test creating linked entity."""
        linked = LinkedEntity(core_id="E001")
        assert linked.core_id == "E001"
        assert linked.patient_id is None
    
    def test_with_product_ids(self):
        """Test linked entity with product IDs."""
        linked = LinkedEntity(
            core_id="E001",
            patient_id="P001",
            member_id="M001"
        )
        assert linked.patient_id == "P001"
        assert linked.member_id == "M001"


class TestCrossProductCoordinator:
    """Tests for CrossProductCoordinator."""
    
    def test_creation(self):
        """Test creating coordinator."""
        coordinator = CrossProductCoordinator()
        assert coordinator is not None
    
    def test_create_linked_entity(self):
        """Test creating linked entity through coordinator."""
        coordinator = CrossProductCoordinator()
        linked = coordinator.create_linked_entity("E001", {
            "patient_id": "P001",
            "member_id": "M001"
        })
        
        assert linked.core_id == "E001"
        assert linked.patient_id == "P001"
        assert linked.member_id == "M001"
    
    def test_get_linked_entity(self):
        """Test retrieving linked entity."""
        coordinator = CrossProductCoordinator()
        coordinator.create_linked_entity("E001")
        
        linked = coordinator.get_linked_entity("E001")
        assert linked is not None
        assert linked.core_id == "E001"
        
        missing = coordinator.get_linked_entity("E999")
        assert missing is None
    
    def test_default_triggers_registered(self):
        """Test that default healthcare triggers are registered."""
        coordinator = CrossProductCoordinator()
        
        # Check diagnosis → claim trigger
        triggers = coordinator._trigger_registry.get_triggers("patientsim", "diagnosis")
        assert len(triggers) > 0
        
        # Check medication → fill trigger
        triggers = coordinator._trigger_registry.get_triggers("patientsim", "medication_order")
        assert len(triggers) > 0


class TestConvenienceFunctions:
    """Tests for convenience functions."""
    
    def test_create_coordinator(self):
        """Test create_coordinator function."""
        coordinator = create_coordinator()
        assert isinstance(coordinator, CrossProductCoordinator)
