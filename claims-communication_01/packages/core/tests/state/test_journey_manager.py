"""Tests for JourneyManager.

Comprehensive tests for journey persistence including:
- CRUD operations (save, load, update, delete)
- Listing and filtering
- Execution history tracking
- Entity journey tracking
"""

import pytest
from datetime import date, datetime
from unittest.mock import patch
import duckdb

from healthsim.state.journey_manager import (
    JourneyManager,
    JourneyRecord,
    JourneySummary,
    JourneyExecutionRecord,
    get_journey_manager,
)


@pytest.fixture
def conn():
    """Create in-memory DuckDB connection."""
    return duckdb.connect(":memory:")


@pytest.fixture
def manager(conn):
    """Create JourneyManager with test connection."""
    return JourneyManager(conn)


@pytest.fixture
def sample_journey_spec():
    """Sample journey specification."""
    return {
        "journey_id": "diabetic-first-year",
        "name": "First Year Diabetes Management",
        "description": "Quarterly visits with labs for new diabetics",
        "duration_days": 365,
        "products": ["patientsim"],
        "events": [
            {
                "event_id": "quarterly-visit",
                "name": "Quarterly PCP Visit",
                "event_type": "encounter",
                "delay": {"min_days": 90, "max_days": 90}
            },
            {
                "event_id": "hba1c-lab",
                "name": "HbA1c Lab Order",
                "event_type": "lab_order",
                "delay": {"min_days": 90, "max_days": 90}
            },
            {
                "event_id": "annual-eye-exam",
                "name": "Annual Ophthalmology Visit",
                "event_type": "encounter",
                "delay": {"min_days": 60, "max_days": 60}
            },
            {
                "event_id": "annual-foot-exam",
                "name": "Annual Podiatry Visit",
                "event_type": "encounter",
                "delay": {"min_days": 180, "max_days": 180}
            }
        ]
    }


# =============================================================================
# Save Journey Tests
# =============================================================================

class TestSaveJourney:
    """Tests for save_journey method."""
    
    def test_save_journey_basic(self, manager, sample_journey_spec):
        """Save a journey and verify ID returned."""
        journey_id = manager.save_journey(
            name="diabetic-first-year",
            journey_spec=sample_journey_spec
        )
        
        assert journey_id.startswith("journey-")
        assert len(journey_id) == 16  # "journey-" + 8 hex chars
    
    def test_save_journey_with_description(self, manager, sample_journey_spec):
        """Save journey with explicit description."""
        journey_id = manager.save_journey(
            name="dm-journey",
            journey_spec=sample_journey_spec,
            description="Custom description override"
        )
        
        journey = manager.load_journey(journey_id)
        assert journey.description == "Custom description override"
    
    def test_save_journey_with_tags(self, manager, sample_journey_spec):
        """Save journey with tags."""
        journey_id = manager.save_journey(
            name="tagged-journey",
            journey_spec=sample_journey_spec,
            tags=["diabetes", "chronic-care", "primary-care"]
        )
        
        journey = manager.load_journey(journey_id)
        assert "diabetes" in journey.tags
        assert "chronic-care" in journey.tags
        assert len(journey.tags) == 3
    
    def test_save_journey_with_products(self, manager, sample_journey_spec):
        """Save journey with explicit products list."""
        journey_id = manager.save_journey(
            name="multi-product-journey",
            journey_spec=sample_journey_spec,
            products=["patientsim", "membersim"]
        )
        
        journey = manager.load_journey(journey_id)
        assert "patientsim" in journey.products
        assert "membersim" in journey.products
    
    def test_save_journey_duplicate_name_raises(self, manager, sample_journey_spec):
        """Saving duplicate name raises ValueError."""
        manager.save_journey(name="unique-journey", journey_spec=sample_journey_spec)
        
        with pytest.raises(ValueError, match="already exists"):
            manager.save_journey(name="unique-journey", journey_spec=sample_journey_spec)
    
    def test_save_journey_extracts_event_count(self, manager, sample_journey_spec):
        """Event count is extracted from spec."""
        journey_id = manager.save_journey(
            name="counted-journey",
            journey_spec=sample_journey_spec
        )
        
        journey = manager.load_journey(journey_id)
        assert journey.event_count == 4  # 4 events in sample
    
    def test_save_journey_extracts_duration(self, manager, sample_journey_spec):
        """Duration is extracted from spec."""
        journey_id = manager.save_journey(
            name="timed-journey",
            journey_spec=sample_journey_spec
        )
        
        journey = manager.load_journey(journey_id)
        assert journey.duration_days == 365
    
    def test_save_journey_with_metadata(self, manager, sample_journey_spec):
        """Save journey with metadata."""
        journey_id = manager.save_journey(
            name="metadata-journey",
            journey_spec=sample_journey_spec,
            metadata={"author": "claude", "version": "1.0"}
        )
        
        journey = manager.load_journey(journey_id)
        assert journey.metadata["author"] == "claude"


# =============================================================================
# Load Journey Tests
# =============================================================================

class TestLoadJourney:
    """Tests for load_journey method."""
    
    def test_load_by_name(self, manager, sample_journey_spec):
        """Load journey by name."""
        manager.save_journey(name="loadable-journey", journey_spec=sample_journey_spec)
        
        journey = manager.load_journey("loadable-journey")
        assert journey.name == "loadable-journey"
    
    def test_load_by_id(self, manager, sample_journey_spec):
        """Load journey by ID."""
        journey_id = manager.save_journey(
            name="id-loadable",
            journey_spec=sample_journey_spec
        )
        
        journey = manager.load_journey(journey_id)
        assert journey.id == journey_id
    
    def test_load_nonexistent_raises(self, manager):
        """Loading nonexistent journey raises ValueError."""
        with pytest.raises(ValueError, match="not found"):
            manager.load_journey("nonexistent-journey")
    
    def test_load_returns_journey_record(self, manager, sample_journey_spec):
        """Loaded journey is JourneyRecord with all fields."""
        manager.save_journey(name="full-record", journey_spec=sample_journey_spec)
        
        journey = manager.load_journey("full-record")
        
        assert isinstance(journey, JourneyRecord)
        assert journey.name == "full-record"
        assert journey.version == 1
        assert journey.journey_spec is not None
        assert journey.created_at is not None
        assert journey.updated_at is not None
    
    def test_load_preserves_spec(self, manager, sample_journey_spec):
        """Loaded journey preserves full specification."""
        manager.save_journey(name="spec-preserved", journey_spec=sample_journey_spec)
        
        journey = manager.load_journey("spec-preserved")
        
        assert journey.journey_spec["journey_id"] == "diabetic-first-year"
        assert len(journey.journey_spec["events"]) == 4


# =============================================================================
# Update Journey Tests
# =============================================================================

class TestUpdateJourney:
    """Tests for update_journey method."""
    
    def test_update_journey_spec(self, manager, sample_journey_spec):
        """Updating spec bumps version."""
        manager.save_journey(name="updatable", journey_spec=sample_journey_spec)
        
        new_spec = sample_journey_spec.copy()
        new_spec["duration_days"] = 180
        
        updated = manager.update_journey("updatable", journey_spec=new_spec)
        
        assert updated.version == 2
        assert updated.duration_days == 180
    
    def test_update_description(self, manager, sample_journey_spec):
        """Update description only."""
        manager.save_journey(name="desc-update", journey_spec=sample_journey_spec)
        
        updated = manager.update_journey("desc-update", description="New description")
        
        assert updated.description == "New description"
        assert updated.version == 2
    
    def test_update_tags(self, manager, sample_journey_spec):
        """Update tags."""
        manager.save_journey(
            name="tag-update",
            journey_spec=sample_journey_spec,
            tags=["old-tag"]
        )
        
        updated = manager.update_journey("tag-update", tags=["new-tag", "another-tag"])
        
        assert "new-tag" in updated.tags
        assert "old-tag" not in updated.tags
    
    def test_update_without_version_bump(self, manager, sample_journey_spec):
        """Update without bumping version."""
        manager.save_journey(name="no-bump", journey_spec=sample_journey_spec)
        
        updated = manager.update_journey(
            "no-bump",
            description="Minor fix",
            bump_version=False
        )
        
        assert updated.version == 1
    
    def test_update_recalculates_event_count(self, manager, sample_journey_spec):
        """Updating spec recalculates event count."""
        manager.save_journey(name="event-recount", journey_spec=sample_journey_spec)
        
        new_spec = sample_journey_spec.copy()
        new_spec["events"] = new_spec["events"][:2]  # Keep only 2 events
        
        updated = manager.update_journey("event-recount", journey_spec=new_spec)
        
        assert updated.event_count == 2


# =============================================================================
# Delete Journey Tests
# =============================================================================

class TestDeleteJourney:
    """Tests for delete_journey method."""
    
    def test_delete_journey(self, manager, sample_journey_spec):
        """Delete a journey."""
        manager.save_journey(name="deletable", journey_spec=sample_journey_spec)
        
        result = manager.delete_journey("deletable")
        
        assert result is True
        assert not manager.journey_exists("deletable")
    
    def test_delete_nonexistent_returns_false(self, manager):
        """Deleting nonexistent journey returns False."""
        result = manager.delete_journey("nonexistent")
        assert result is False
    
    def test_delete_with_executions(self, manager, sample_journey_spec):
        """Delete journey with execution history."""
        journey_id = manager.save_journey(
            name="has-executions",
            journey_spec=sample_journey_spec
        )
        
        manager.record_execution(
            journey_id=journey_id,
            entity_id="patient-001",
            events_generated=10
        )
        
        result = manager.delete_journey("has-executions", delete_executions=True)
        
        assert result is True
        assert not manager.journey_exists("has-executions")


# =============================================================================
# List Journeys Tests
# =============================================================================

class TestListJourneys:
    """Tests for list_journeys method."""
    
    def test_list_all_journeys(self, manager, sample_journey_spec):
        """List all journeys."""
        manager.save_journey(name="journey-1", journey_spec=sample_journey_spec)
        manager.save_journey(name="journey-2", journey_spec=sample_journey_spec)
        manager.save_journey(name="journey-3", journey_spec=sample_journey_spec)
        
        journeys = manager.list_journeys()
        
        assert len(journeys) == 3
        assert all(isinstance(j, JourneySummary) for j in journeys)
    
    def test_list_by_product(self, manager, sample_journey_spec):
        """List journeys filtered by product."""
        manager.save_journey(
            name="patient-journey",
            journey_spec=sample_journey_spec,
            products=["patientsim"]
        )
        manager.save_journey(
            name="member-journey",
            journey_spec=sample_journey_spec,
            products=["membersim"]
        )
        
        journeys = manager.list_journeys(products=["patientsim"])
        
        assert len(journeys) == 1
        assert journeys[0].name == "patient-journey"
    
    def test_list_by_tags(self, manager, sample_journey_spec):
        """List journeys filtered by tags."""
        manager.save_journey(
            name="diabetes-journey",
            journey_spec=sample_journey_spec,
            tags=["diabetes", "chronic"]
        )
        manager.save_journey(
            name="cardiac-journey",
            journey_spec=sample_journey_spec,
            tags=["cardiac", "acute"]
        )
        
        journeys = manager.list_journeys(tags=["diabetes"])
        
        assert len(journeys) == 1
        assert journeys[0].name == "diabetes-journey"
    
    def test_list_with_search(self, manager, sample_journey_spec):
        """List journeys with search."""
        manager.save_journey(
            name="diabetes-management",
            journey_spec=sample_journey_spec,
            description="For diabetic patients"
        )
        manager.save_journey(
            name="cardiac-rehab",
            journey_spec=sample_journey_spec,
            description="Post-MI rehabilitation"
        )
        
        journeys = manager.list_journeys(search="diabetes")
        
        assert len(journeys) == 1
        assert journeys[0].name == "diabetes-management"
    
    def test_list_includes_execution_count(self, manager, sample_journey_spec):
        """List includes execution count."""
        journey_id = manager.save_journey(
            name="executed-journey",
            journey_spec=sample_journey_spec
        )
        
        manager.record_execution(journey_id=journey_id, events_generated=5)
        manager.record_execution(journey_id=journey_id, events_generated=10)
        
        journeys = manager.list_journeys()
        
        assert journeys[0].execution_count == 2


# =============================================================================
# Record Execution Tests
# =============================================================================

class TestRecordExecution:
    """Tests for record_execution method."""
    
    def test_record_basic_execution(self, manager, sample_journey_spec):
        """Record a basic journey execution."""
        journey_id = manager.save_journey(
            name="exec-journey",
            journey_spec=sample_journey_spec
        )
        
        exec_id = manager.record_execution(
            journey_id=journey_id,
            events_generated=12,
            duration_ms=500
        )
        
        assert exec_id > 0
    
    def test_record_execution_with_entity(self, manager, sample_journey_spec):
        """Record execution for specific entity."""
        journey_id = manager.save_journey(
            name="entity-exec",
            journey_spec=sample_journey_spec
        )
        
        exec_id = manager.record_execution(
            journey_id=journey_id,
            entity_id="patient-123",
            events_generated=8
        )
        
        executions = manager.get_executions(journey_id)
        assert executions[0].entity_id == "patient-123"
    
    def test_record_execution_with_dates(self, manager, sample_journey_spec):
        """Record execution with date range."""
        journey_id = manager.save_journey(
            name="dated-exec",
            journey_spec=sample_journey_spec
        )
        
        manager.record_execution(
            journey_id=journey_id,
            start_date=date(2024, 1, 1),
            end_date=date(2024, 12, 31),
            events_generated=20
        )
        
        executions = manager.get_executions(journey_id)
        assert executions[0].start_date == date(2024, 1, 1)
        assert executions[0].end_date == date(2024, 12, 31)
    
    def test_record_execution_with_profile_link(self, manager, sample_journey_spec):
        """Record execution linked to profile."""
        journey_id = manager.save_journey(
            name="profile-linked",
            journey_spec=sample_journey_spec
        )
        
        manager.record_execution(
            journey_id=journey_id,
            profile_id="profile-abc123",
            cohort_id="cohort-xyz789",
            events_generated=15
        )
        
        executions = manager.get_executions(journey_id)
        assert executions[0].profile_id == "profile-abc123"
        assert executions[0].cohort_id == "cohort-xyz789"
    
    def test_record_failed_execution(self, manager, sample_journey_spec):
        """Record failed journey execution."""
        journey_id = manager.save_journey(
            name="failed-exec",
            journey_spec=sample_journey_spec
        )
        
        manager.record_execution(
            journey_id=journey_id,
            events_generated=0,
            status="failed",
            error_message="Timeline generation failed"
        )
        
        executions = manager.get_executions(journey_id)
        assert executions[0].status == "failed"
        assert "failed" in executions[0].error_message


# =============================================================================
# Get Executions Tests
# =============================================================================

class TestGetExecutions:
    """Tests for get_executions method."""
    
    def test_get_executions_ordered_by_time(self, manager, sample_journey_spec):
        """Executions ordered newest first."""
        journey_id = manager.save_journey(
            name="ordered-exec",
            journey_spec=sample_journey_spec
        )
        
        manager.record_execution(journey_id=journey_id, events_generated=5)
        manager.record_execution(journey_id=journey_id, events_generated=10)
        manager.record_execution(journey_id=journey_id, events_generated=15)
        
        executions = manager.get_executions(journey_id)
        
        assert len(executions) == 3
        assert executions[0].events_generated == 15  # Most recent
        assert executions[2].events_generated == 5   # Oldest
    
    def test_get_executions_with_limit(self, manager, sample_journey_spec):
        """Limit number of executions returned."""
        journey_id = manager.save_journey(
            name="limited-exec",
            journey_spec=sample_journey_spec
        )
        
        for i in range(10):
            manager.record_execution(journey_id=journey_id, events_generated=i)
        
        executions = manager.get_executions(journey_id, limit=5)
        
        assert len(executions) == 5
    
    def test_get_executions_returns_records(self, manager, sample_journey_spec):
        """Returns JourneyExecutionRecord objects."""
        journey_id = manager.save_journey(
            name="record-exec",
            journey_spec=sample_journey_spec
        )
        
        manager.record_execution(
            journey_id=journey_id,
            entity_id="patient-999",
            events_generated=20,
            duration_ms=1000
        )
        
        executions = manager.get_executions(journey_id)
        
        assert isinstance(executions[0], JourneyExecutionRecord)
        assert executions[0].entity_id == "patient-999"
        assert executions[0].events_generated == 20
        assert executions[0].duration_ms == 1000


# =============================================================================
# Entity Journeys Tests
# =============================================================================

class TestGetEntityJourneys:
    """Tests for get_entity_journeys method."""
    
    def test_get_journeys_for_entity(self, manager, sample_journey_spec):
        """Get all journey executions for an entity."""
        journey1_id = manager.save_journey(
            name="entity-journey-1",
            journey_spec=sample_journey_spec
        )
        journey2_id = manager.save_journey(
            name="entity-journey-2",
            journey_spec=sample_journey_spec
        )
        
        # Same entity in multiple journeys
        manager.record_execution(
            journey_id=journey1_id,
            entity_id="patient-multi",
            events_generated=10
        )
        manager.record_execution(
            journey_id=journey2_id,
            entity_id="patient-multi",
            events_generated=5
        )
        # Different entity
        manager.record_execution(
            journey_id=journey1_id,
            entity_id="patient-other",
            events_generated=8
        )
        
        executions = manager.get_entity_journeys("patient-multi")
        
        assert len(executions) == 2
        assert all(e.entity_id == "patient-multi" for e in executions)
    
    def test_get_entity_journeys_empty(self, manager):
        """Returns empty list for entity with no journeys."""
        executions = manager.get_entity_journeys("nonexistent-patient")
        assert executions == []


# =============================================================================
# Journey Exists Tests
# =============================================================================

class TestJourneyExists:
    """Tests for journey_exists method."""
    
    def test_journey_exists_by_name(self, manager, sample_journey_spec):
        """Check existence by name."""
        manager.save_journey(name="existing-journey", journey_spec=sample_journey_spec)
        
        assert manager.journey_exists("existing-journey") is True
        assert manager.journey_exists("nonexistent") is False
    
    def test_journey_exists_by_id(self, manager, sample_journey_spec):
        """Check existence by ID."""
        journey_id = manager.save_journey(
            name="id-check",
            journey_spec=sample_journey_spec
        )
        
        assert manager.journey_exists(journey_id) is True


# =============================================================================
# Convenience Function Tests
# =============================================================================

class TestConvenienceFunctions:
    """Tests for module-level convenience functions."""
    
    def test_get_journey_manager_with_connection(self, conn):
        """Get manager with provided connection."""
        manager = get_journey_manager(conn)
        
        assert isinstance(manager, JourneyManager)
        assert manager.conn is conn
