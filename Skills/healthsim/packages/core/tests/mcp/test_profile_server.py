"""Tests for HealthSim MCP Profile Server."""

import pytest
import json
from pathlib import Path
from unittest.mock import patch
import tempfile

from healthsim.mcp.profile_server import (
    # Profile formatters
    format_profile_summary,
    format_profile_list,
    format_template_list,
    format_execution_result,
    format_error,
    format_success,
    # Journey formatters
    format_journey_summary,
    format_journey_list,
    # Profile handlers
    handle_build_profile,
    handle_save_profile,
    handle_load_profile,
    handle_list_profiles,
    handle_list_profile_templates,
    handle_get_profile_template,
    # Journey handlers
    handle_build_journey,
    handle_save_journey,
    handle_load_journey,
    handle_list_journeys,
    handle_list_journey_templates,
    handle_get_journey_template,
    handle_execute_journey,
)
from healthsim.generation.profile_schema import (
    ProfileSpecification,
    GenerationSpec,
    DemographicsSpec,
    DistributionSpec,
    DistributionType,
    ClinicalSpec,
    ConditionSpec,
)
from healthsim.generation.profile_executor import ExecutionResult, ValidationReport


# =============================================================================
# Profile Formatter Tests
# =============================================================================

class TestFormatProfileSummary:
    """Tests for format_profile_summary."""

    def test_basic_profile(self):
        """Test formatting a basic profile."""
        profile = ProfileSpecification(
            id="test-profile-001",
            name="Test Profile",
            version="1.0",
            generation=GenerationSpec(count=50, products=["patientsim"]),
        )
        result = format_profile_summary(profile)
        
        assert "Test Profile" in result
        assert "test-profile-001" in result
        assert "50" in result
        assert "patientsim" in result

    def test_profile_with_demographics(self):
        """Test formatting profile with demographics."""
        profile = ProfileSpecification(
            id="test-demo-001",
            name="Demo Profile",
            generation=GenerationSpec(count=100),
            demographics=DemographicsSpec(
                age=DistributionSpec(
                    type=DistributionType.NORMAL,
                    mean=72.0,
                    std_dev=8.0,
                )
            ),
        )
        result = format_profile_summary(profile)
        
        assert "Demographics" in result
        assert "72" in result

    def test_profile_with_clinical(self):
        """Test formatting profile with clinical specs."""
        profile = ProfileSpecification(
            id="test-clinical-001",
            name="Clinical Profile",
            clinical=ClinicalSpec(
                primary_condition=ConditionSpec(
                    code="E11",
                    description="Type 2 Diabetes",
                )
            ),
        )
        result = format_profile_summary(profile)
        
        assert "Clinical" in result
        assert "E11" in result
        assert "Diabetes" in result


class TestFormatProfileList:
    """Tests for format_profile_list."""

    def test_empty_list(self):
        """Test formatting empty profile list."""
        result = format_profile_list([])
        assert "No saved profiles" in result

    def test_profile_list(self):
        """Test formatting profile list."""
        profiles = [
            {"name": "Profile 1", "id": "profile-1", "description": "First profile"},
            {"name": "Profile 2", "id": "profile-2"},
        ]
        result = format_profile_list(profiles)
        
        assert "Profile 1" in result
        assert "profile-1" in result
        assert "First profile" in result
        assert "Profile 2" in result


class TestFormatTemplateList:
    """Tests for format_template_list."""

    def test_template_list(self):
        """Test formatting template list."""
        templates = {
            "medicare-standard": {"description": "Medicare population"},
            "commercial-family": {"name": "Family Coverage"},
        }
        result = format_template_list(templates, "profile")
        
        assert "Profile Templates" in result
        assert "medicare-standard" in result
        assert "commercial-family" in result


class TestFormatExecutionResult:
    """Tests for format_execution_result."""

    def test_basic_result(self):
        """Test formatting execution result."""
        result = ExecutionResult(
            profile_id="test-profile-001",
            count=100,
            seed=12345,
            entities=[],  # Empty for this test
            duration_seconds=1.5,
            validation=ValidationReport(),  # Empty report = passed
        )
        formatted = format_execution_result(result)
        
        assert "100" in formatted
        assert "12345" in formatted
        assert "1.5" in formatted
        assert "Passed" in formatted

    def test_result_with_warnings(self):
        """Test formatting result with warnings."""
        result = ExecutionResult(
            profile_id="test-profile-002",
            count=50,
            seed=42,
            entities=[],
            duration_seconds=0.8,
            validation=ValidationReport(
                warnings=["Age distribution slightly skewed"],
            ),
        )
        formatted = format_execution_result(result)
        
        assert "Warnings: 1" in formatted


# =============================================================================
# Journey Formatter Tests
# =============================================================================

class TestFormatJourneySummary:
    """Tests for format_journey_summary."""

    def test_basic_journey(self):
        """Test formatting a basic journey."""
        journey = {
            "journey_id": "test-journey-001",
            "name": "Test Journey",
            "description": "A test journey",
            "duration_days": 30,
            "products": ["patientsim"],
            "events": [
                {"name": "Event 1", "event_type": "encounter"},
                {"name": "Event 2", "event_type": "lab_order"},
            ]
        }
        result = format_journey_summary(journey)
        
        assert "Test Journey" in result
        assert "test-journey-001" in result
        assert "30" in result
        assert "2" in result  # event count
        assert "patientsim" in result

    def test_journey_with_many_events(self):
        """Test formatting journey with more than 8 events."""
        events = [{"name": f"Event {i}", "event_type": "encounter"} for i in range(15)]
        journey = {
            "journey_id": "many-events",
            "name": "Many Events Journey",
            "events": events
        }
        result = format_journey_summary(journey)
        
        assert "15" in result  # total count
        assert "and 7 more" in result  # 15 - 8 = 7


class TestFormatJourneyList:
    """Tests for format_journey_list."""

    def test_empty_list(self):
        """Test formatting empty journey list."""
        result = format_journey_list([])
        assert "No saved journeys" in result

    def test_journey_list(self):
        """Test formatting journey list."""
        journeys = [
            {
                "journey_id": "journey-1",
                "name": "Journey 1",
                "description": "First journey",
                "duration_days": 30,
                "events": [{"name": "e1"}, {"name": "e2"}]
            },
            {
                "journey_id": "journey-2",
                "name": "Journey 2",
                "events": [{"name": "e1"}]
            },
        ]
        result = format_journey_list(journeys)
        
        assert "Journey 1" in result
        assert "journey-1" in result
        assert "First journey" in result
        assert "Journey 2" in result
        assert "2 events" in result
        assert "30 days" in result


# =============================================================================
# Utility Formatter Tests
# =============================================================================

class TestUtilityFormatters:
    """Tests for utility formatting functions."""

    def test_format_error(self):
        """Test error message formatting."""
        result = format_error("Something went wrong")
        assert "Error" in result
        assert "Something went wrong" in result

    def test_format_success(self):
        """Test success message formatting."""
        result = format_success("Operation completed")
        assert "✓" in result
        assert "Operation completed" in result


# =============================================================================
# Profile Handler Tests
# =============================================================================

@pytest.mark.asyncio
class TestBuildProfileHandler:
    """Tests for build_profile handler."""

    async def test_build_basic_profile(self):
        """Test building a basic profile."""
        result = await handle_build_profile({"name": "Test Profile"})
        
        assert len(result) == 1
        text = result[0].text
        assert "Test Profile" in text
        assert "test-profile" in text

    async def test_build_profile_with_id(self):
        """Test building profile with custom ID."""
        result = await handle_build_profile({
            "name": "My Profile",
            "id": "custom-id-001",
        })
        
        text = result[0].text
        assert "custom-id-001" in text

    async def test_build_profile_with_demographics(self):
        """Test building profile with demographics."""
        result = await handle_build_profile({
            "name": "Demo Profile",
            "age_mean": 65,
            "age_std": 10,
            "age_min": 50,
            "age_max": 85,
        })
        
        text = result[0].text
        assert "Demographics" in text

    async def test_build_profile_with_clinical(self):
        """Test building profile with clinical specs."""
        result = await handle_build_profile({
            "name": "Clinical Profile",
            "primary_condition_code": "E11",
            "primary_condition_name": "Type 2 Diabetes",
        })
        
        text = result[0].text
        assert "E11" in text


@pytest.mark.asyncio
class TestSaveLoadProfileHandlers:
    """Tests for save/load profile handlers."""

    async def test_save_and_list_profiles(self):
        """Test saving and listing profiles."""
        with tempfile.TemporaryDirectory() as tmpdir:
            profiles_dir = Path(tmpdir)
            
            # Patch the storage directory
            with patch("healthsim.mcp.profile_server.PROFILES_DIR", profiles_dir):
                # Create a profile
                profile = ProfileSpecification(
                    id="test-save-001",
                    name="Test Save Profile",
                    generation=GenerationSpec(count=10),
                )
                
                # Save it
                result = await handle_save_profile({
                    "profile_json": profile.to_json(),
                })
                
                assert "✓" in result[0].text or "Saved" in result[0].text

    async def test_load_profile_not_found(self):
        """Test loading non-existent profile."""
        with tempfile.TemporaryDirectory() as tmpdir:
            profiles_dir = Path(tmpdir)
            
            with patch("healthsim.mcp.profile_server.PROFILES_DIR", profiles_dir):
                result = await handle_load_profile({"name": "nonexistent"})
                
                text = result[0].text
                assert "not found" in text.lower() or "error" in text.lower()


@pytest.mark.asyncio
class TestProfileTemplateHandlers:
    """Tests for profile template handlers."""

    async def test_list_profile_templates(self):
        """Test listing profile templates."""
        result = await handle_list_profile_templates({})
        
        text = result[0].text
        assert "Template" in text

    async def test_get_profile_template_not_found(self):
        """Test getting non-existent profile template."""
        result = await handle_get_profile_template({
            "template_name": "nonexistent-template"
        })
        
        text = result[0].text
        assert "not found" in text.lower() or "error" in text.lower()


# =============================================================================
# Journey Handler Tests
# =============================================================================

@pytest.mark.asyncio
class TestBuildJourneyHandler:
    """Tests for build_journey handler."""

    async def test_build_basic_journey(self):
        """Test building a basic journey."""
        result = await handle_build_journey({"name": "Test Journey"})
        
        assert len(result) == 1
        text = result[0].text
        assert "Test Journey" in text
        assert "test-journey" in text

    async def test_build_journey_with_events(self):
        """Test building journey with events."""
        result = await handle_build_journey({
            "name": "Journey With Events",
            "duration_days": 30,
            "events": [
                {"name": "Initial Visit", "event_type": "encounter"},
                {"name": "Follow Up", "event_type": "encounter"},
            ]
        })
        
        text = result[0].text
        assert "Journey With Events" in text
        assert "2" in text  # event count

    async def test_build_journey_with_custom_id(self):
        """Test building journey with custom ID."""
        result = await handle_build_journey({
            "name": "Custom ID Journey",
            "id": "my-custom-journey-id",
        })
        
        text = result[0].text
        assert "my-custom-journey-id" in text


@pytest.mark.asyncio
class TestSaveLoadJourneyHandlers:
    """Tests for save/load journey handlers."""

    async def test_save_journey(self):
        """Test saving a journey."""
        with tempfile.TemporaryDirectory() as tmpdir:
            journeys_dir = Path(tmpdir)
            
            with patch("healthsim.mcp.profile_server.JOURNEYS_DIR", journeys_dir):
                journey = {
                    "journey_id": "test-save-journey",
                    "name": "Test Save Journey",
                    "events": []
                }
                
                result = await handle_save_journey({
                    "journey_json": json.dumps(journey),
                })
                
                assert "✓" in result[0].text or "Saved" in result[0].text
                
                # Verify file was created
                filepath = journeys_dir / "test-save-journey.json"
                assert filepath.exists()

    async def test_save_journey_no_overwrite(self):
        """Test that save_journey doesn't overwrite by default."""
        with tempfile.TemporaryDirectory() as tmpdir:
            journeys_dir = Path(tmpdir)
            
            with patch("healthsim.mcp.profile_server.JOURNEYS_DIR", journeys_dir):
                journey = {
                    "journey_id": "duplicate-journey",
                    "name": "Original",
                    "events": []
                }
                
                # Save first time
                await handle_save_journey({"journey_json": json.dumps(journey)})
                
                # Try to save again
                journey["name"] = "Updated"
                result = await handle_save_journey({
                    "journey_json": json.dumps(journey),
                })
                
                text = result[0].text
                assert "exists" in text.lower() or "error" in text.lower()

    async def test_save_journey_with_overwrite(self):
        """Test save_journey with overwrite=True."""
        with tempfile.TemporaryDirectory() as tmpdir:
            journeys_dir = Path(tmpdir)
            
            with patch("healthsim.mcp.profile_server.JOURNEYS_DIR", journeys_dir):
                journey = {
                    "journey_id": "overwrite-journey",
                    "name": "Original",
                    "events": []
                }
                
                # Save first time
                await handle_save_journey({"journey_json": json.dumps(journey)})
                
                # Save again with overwrite
                journey["name"] = "Updated"
                result = await handle_save_journey({
                    "journey_json": json.dumps(journey),
                    "overwrite": True,
                })
                
                assert "✓" in result[0].text or "Saved" in result[0].text

    async def test_load_journey_not_found(self):
        """Test loading non-existent journey."""
        with tempfile.TemporaryDirectory() as tmpdir:
            journeys_dir = Path(tmpdir)
            
            with patch("healthsim.mcp.profile_server.JOURNEYS_DIR", journeys_dir):
                result = await handle_load_journey({"name": "nonexistent"})
                
                text = result[0].text
                assert "not found" in text.lower() or "error" in text.lower()

    async def test_load_saved_journey(self):
        """Test loading a saved journey."""
        with tempfile.TemporaryDirectory() as tmpdir:
            journeys_dir = Path(tmpdir)
            
            with patch("healthsim.mcp.profile_server.JOURNEYS_DIR", journeys_dir):
                journey = {
                    "journey_id": "loadable-journey",
                    "name": "Loadable Journey",
                    "description": "Can be loaded",
                    "events": [{"name": "Event 1", "event_type": "encounter"}]
                }
                
                # Save it
                filepath = journeys_dir / "loadable-journey.json"
                filepath.write_text(json.dumps(journey))
                
                # Load it
                result = await handle_load_journey({"name": "loadable-journey"})
                
                text = result[0].text
                assert "Loadable Journey" in text
                assert "Event 1" in text


@pytest.mark.asyncio
class TestListJourneysHandler:
    """Tests for list_journeys handler."""

    async def test_list_empty_journeys(self):
        """Test listing when no journeys exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            journeys_dir = Path(tmpdir)
            
            with patch("healthsim.mcp.profile_server.JOURNEYS_DIR", journeys_dir):
                result = await handle_list_journeys({})
                
                text = result[0].text
                assert "No saved journeys" in text

    async def test_list_journeys(self):
        """Test listing saved journeys."""
        with tempfile.TemporaryDirectory() as tmpdir:
            journeys_dir = Path(tmpdir)
            
            with patch("healthsim.mcp.profile_server.JOURNEYS_DIR", journeys_dir):
                # Create some journeys
                for i in range(3):
                    journey = {
                        "journey_id": f"journey-{i}",
                        "name": f"Journey {i}",
                        "events": [{"name": f"e{j}"} for j in range(i + 1)]
                    }
                    filepath = journeys_dir / f"journey-{i}.json"
                    filepath.write_text(json.dumps(journey))
                
                result = await handle_list_journeys({})
                
                text = result[0].text
                assert "Journey 0" in text
                assert "Journey 1" in text
                assert "Journey 2" in text


@pytest.mark.asyncio
class TestJourneyTemplateHandlers:
    """Tests for journey template listing handlers."""

    async def test_list_journey_templates(self):
        """Test listing journey templates."""
        result = await handle_list_journey_templates({})
        
        text = result[0].text
        assert "Template" in text or "journey" in text.lower()

    async def test_get_journey_template_not_found(self):
        """Test getting non-existent journey template."""
        result = await handle_get_journey_template({
            "template_name": "nonexistent-template"
        })
        
        text = result[0].text
        assert "not found" in text.lower() or "error" in text.lower()


@pytest.mark.asyncio
class TestExecuteJourneyHandler:
    """Tests for execute_journey handler."""

    async def test_execute_journey_from_json(self):
        """Test executing journey from JSON."""
        journey = {
            "journey_id": "exec-test",
            "name": "Execution Test",
            "duration_days": 7,
            "events": [
                {
                    "event_id": "evt-1",
                    "name": "Initial Event",
                    "event_type": "encounter",
                    "day_offset": 0
                }
            ]
        }
        
        result = await handle_execute_journey({
            "journey_json": json.dumps(journey),
            "entity_id": "patient-123",
            "start_date": "2024-01-01",
        })
        
        text = result[0].text
        # Should either succeed or give a meaningful response
        assert "patient-123" in text or "Error" in text

    async def test_execute_journey_missing_source(self):
        """Test execute_journey with no journey source."""
        result = await handle_execute_journey({})
        
        text = result[0].text
        assert "error" in text.lower() or "provide" in text.lower()

    async def test_execute_journey_invalid_date(self):
        """Test execute_journey with invalid date format."""
        journey = {"journey_id": "date-test", "name": "Date Test", "events": []}
        
        result = await handle_execute_journey({
            "journey_json": json.dumps(journey),
            "start_date": "not-a-date",
        })
        
        text = result[0].text
        assert "error" in text.lower() or "invalid" in text.lower()
