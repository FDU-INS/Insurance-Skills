"""Tests for ProfileManager - profile persistence and execution history.

Phase 5.1: Profile Persistence
Phase 5.2: Execution History
"""

import pytest
from datetime import datetime
from pathlib import Path
import tempfile
import duckdb

from healthsim.state.profile_manager import (
    ProfileManager,
    ProfileRecord,
    ProfileSummary,
    ExecutionRecord,
    get_profile_manager,
)


# =============================================================================
# Test Fixtures
# =============================================================================

@pytest.fixture
def temp_db():
    """Create a temporary in-memory database for testing."""
    conn = duckdb.connect(":memory:")
    yield conn
    conn.close()


@pytest.fixture
def profile_manager(temp_db):
    """Create a ProfileManager with in-memory database."""
    return ProfileManager(temp_db)


@pytest.fixture
def sample_profile_spec():
    """Sample profile specification for testing."""
    return {
        "profile": {
            "id": "test-profile",
            "generation": {"count": 100, "seed": 42},
            "demographics": {
                "source": "populationsim",
                "reference": {"type": "county", "fips": "48201"}
            },
            "clinical": {
                "primary_condition": {"code": "E11", "prevalence": 1.0}
            }
        }
    }


# =============================================================================
# Phase 5.1: Profile Persistence Tests
# =============================================================================

class TestSaveProfile:
    """Tests for save_profile()."""
    
    def test_save_profile_basic(self, profile_manager, sample_profile_spec):
        """Test saving a basic profile."""
        profile_id = profile_manager.save_profile(
            name="test-diabetic",
            profile_spec=sample_profile_spec,
            description="Test diabetic profile",
        )
        
        assert profile_id.startswith("profile-")
        assert len(profile_id) == 16  # "profile-" + 8 hex chars
    
    def test_save_profile_with_tags(self, profile_manager, sample_profile_spec):
        """Test saving a profile with tags."""
        profile_id = profile_manager.save_profile(
            name="tagged-profile",
            profile_spec=sample_profile_spec,
            tags=["diabetes", "harris-county", "elderly"]
        )
        
        # Load and verify tags
        profile = profile_manager.load_profile(profile_id)
        assert "diabetes" in profile.tags
        assert "elderly" in profile.tags
    
    def test_save_profile_with_product(self, profile_manager, sample_profile_spec):
        """Test saving a profile with product type."""
        profile_id = profile_manager.save_profile(
            name="patient-profile",
            profile_spec=sample_profile_spec,
            product="patientsim"
        )
        
        profile = profile_manager.load_profile(profile_id)
        assert profile.product == "patientsim"
    
    def test_save_profile_duplicate_name_raises(self, profile_manager, sample_profile_spec):
        """Test that duplicate names raise ValueError."""
        profile_manager.save_profile(
            name="unique-profile",
            profile_spec=sample_profile_spec
        )
        
        with pytest.raises(ValueError, match="already exists"):
            profile_manager.save_profile(
                name="unique-profile",
                profile_spec=sample_profile_spec
            )
    
    def test_save_profile_with_metadata(self, profile_manager, sample_profile_spec):
        """Test saving a profile with metadata."""
        metadata = {"author": "test", "version": "1.0"}
        profile_id = profile_manager.save_profile(
            name="metadata-profile",
            profile_spec=sample_profile_spec,
            metadata=metadata
        )
        
        profile = profile_manager.load_profile(profile_id)
        assert profile.metadata == metadata


class TestLoadProfile:
    """Tests for load_profile()."""
    
    def test_load_by_name(self, profile_manager, sample_profile_spec):
        """Test loading a profile by name."""
        profile_manager.save_profile(
            name="load-by-name",
            profile_spec=sample_profile_spec
        )
        
        profile = profile_manager.load_profile("load-by-name")
        assert profile.name == "load-by-name"
        assert profile.profile_spec == sample_profile_spec
    
    def test_load_by_id(self, profile_manager, sample_profile_spec):
        """Test loading a profile by ID."""
        profile_id = profile_manager.save_profile(
            name="load-by-id",
            profile_spec=sample_profile_spec
        )
        
        profile = profile_manager.load_profile(profile_id)
        assert profile.id == profile_id
    
    def test_load_nonexistent_raises(self, profile_manager):
        """Test that loading nonexistent profile raises ValueError."""
        with pytest.raises(ValueError, match="not found"):
            profile_manager.load_profile("nonexistent-profile")
    
    def test_load_returns_profile_record(self, profile_manager, sample_profile_spec):
        """Test that load returns a ProfileRecord."""
        profile_manager.save_profile(
            name="record-test",
            profile_spec=sample_profile_spec,
            description="Test description",
            tags=["test"]
        )
        
        profile = profile_manager.load_profile("record-test")
        
        assert isinstance(profile, ProfileRecord)
        assert profile.name == "record-test"
        assert profile.description == "Test description"
        assert profile.version == 1
        assert profile.tags == ["test"]
        assert isinstance(profile.created_at, datetime)


class TestUpdateProfile:
    """Tests for update_profile()."""
    
    def test_update_profile_spec(self, profile_manager, sample_profile_spec):
        """Test updating profile specification."""
        profile_id = profile_manager.save_profile(
            name="update-spec",
            profile_spec=sample_profile_spec
        )
        
        new_spec = dict(sample_profile_spec)
        new_spec["profile"]["generation"]["count"] = 200
        
        updated = profile_manager.update_profile(
            "update-spec",
            profile_spec=new_spec
        )
        
        assert updated.profile_spec["profile"]["generation"]["count"] == 200
        assert updated.version == 2  # Version bumped
    
    def test_update_description(self, profile_manager, sample_profile_spec):
        """Test updating description only."""
        profile_manager.save_profile(
            name="update-desc",
            profile_spec=sample_profile_spec,
            description="Original"
        )
        
        updated = profile_manager.update_profile(
            "update-desc",
            description="Updated description"
        )
        
        assert updated.description == "Updated description"
        assert updated.profile_spec == sample_profile_spec  # Spec unchanged
    
    def test_update_tags(self, profile_manager, sample_profile_spec):
        """Test updating tags."""
        profile_manager.save_profile(
            name="update-tags",
            profile_spec=sample_profile_spec,
            tags=["original"]
        )
        
        updated = profile_manager.update_profile(
            "update-tags",
            tags=["new", "tags"]
        )
        
        assert updated.tags == ["new", "tags"]
    
    def test_update_without_version_bump(self, profile_manager, sample_profile_spec):
        """Test updating without bumping version."""
        profile_manager.save_profile(
            name="no-bump",
            profile_spec=sample_profile_spec
        )
        
        updated = profile_manager.update_profile(
            "no-bump",
            description="Minor fix",
            bump_version=False
        )
        
        assert updated.version == 1  # Version unchanged


class TestDeleteProfile:
    """Tests for delete_profile()."""
    
    def test_delete_profile(self, profile_manager, sample_profile_spec):
        """Test deleting a profile."""
        profile_manager.save_profile(
            name="to-delete",
            profile_spec=sample_profile_spec
        )
        
        result = profile_manager.delete_profile("to-delete")
        assert result is True
        
        # Verify deleted
        with pytest.raises(ValueError, match="not found"):
            profile_manager.load_profile("to-delete")
    
    def test_delete_nonexistent_returns_false(self, profile_manager):
        """Test deleting nonexistent profile returns False."""
        result = profile_manager.delete_profile("nonexistent")
        assert result is False
    
    def test_delete_with_executions(self, profile_manager, sample_profile_spec):
        """Test deleting profile with execution history."""
        profile_id = profile_manager.save_profile(
            name="with-executions",
            profile_spec=sample_profile_spec
        )
        
        # Add execution
        profile_manager.record_execution(
            profile_id=profile_id,
            count=100,
            duration_ms=1000
        )
        
        # Delete should remove both
        result = profile_manager.delete_profile("with-executions")
        assert result is True


class TestListProfiles:
    """Tests for list_profiles()."""
    
    def test_list_all_profiles(self, profile_manager, sample_profile_spec):
        """Test listing all profiles."""
        profile_manager.save_profile(name="profile-1", profile_spec=sample_profile_spec)
        profile_manager.save_profile(name="profile-2", profile_spec=sample_profile_spec)
        profile_manager.save_profile(name="profile-3", profile_spec=sample_profile_spec)
        
        profiles = profile_manager.list_profiles()
        
        assert len(profiles) == 3
        assert all(isinstance(p, ProfileSummary) for p in profiles)
    
    def test_list_by_product(self, profile_manager, sample_profile_spec):
        """Test filtering by product."""
        profile_manager.save_profile(
            name="patient-1", profile_spec=sample_profile_spec, product="patientsim"
        )
        profile_manager.save_profile(
            name="member-1", profile_spec=sample_profile_spec, product="membersim"
        )
        
        patients = profile_manager.list_profiles(product="patientsim")
        
        assert len(patients) == 1
        assert patients[0].name == "patient-1"
    
    def test_list_by_tags(self, profile_manager, sample_profile_spec):
        """Test filtering by tags."""
        profile_manager.save_profile(
            name="diabetic", profile_spec=sample_profile_spec, tags=["diabetes"]
        )
        profile_manager.save_profile(
            name="cardiac", profile_spec=sample_profile_spec, tags=["heart"]
        )
        
        diabetic = profile_manager.list_profiles(tags=["diabetes"])
        
        assert len(diabetic) == 1
        assert diabetic[0].name == "diabetic"
    
    def test_list_with_search(self, profile_manager, sample_profile_spec):
        """Test searching profiles."""
        profile_manager.save_profile(
            name="harris-county-diabetic",
            profile_spec=sample_profile_spec,
            description="Diabetic patients in Harris County"
        )
        profile_manager.save_profile(
            name="bexar-county-cardiac",
            profile_spec=sample_profile_spec,
            description="Cardiac patients in Bexar County"
        )
        
        harris = profile_manager.list_profiles(search="harris")
        
        assert len(harris) == 1
        assert harris[0].name == "harris-county-diabetic"
    
    def test_list_includes_execution_count(self, profile_manager, sample_profile_spec):
        """Test that list includes execution count."""
        profile_id = profile_manager.save_profile(
            name="executed-profile",
            profile_spec=sample_profile_spec
        )
        
        # Record some executions
        profile_manager.record_execution(profile_id=profile_id, count=100, duration_ms=1000)
        profile_manager.record_execution(profile_id=profile_id, count=50, duration_ms=500)
        
        profiles = profile_manager.list_profiles()
        
        assert profiles[0].execution_count == 2


# =============================================================================
# Phase 5.2: Execution History Tests
# =============================================================================

class TestRecordExecution:
    """Tests for record_execution()."""
    
    def test_record_basic_execution(self, profile_manager, sample_profile_spec):
        """Test recording a basic execution."""
        profile_id = profile_manager.save_profile(
            name="exec-test",
            profile_spec=sample_profile_spec
        )
        
        exec_id = profile_manager.record_execution(
            profile_id=profile_id,
            count=100,
            duration_ms=1500
        )
        
        assert exec_id > 0
    
    def test_record_execution_with_seed(self, profile_manager, sample_profile_spec):
        """Test recording execution with seed."""
        profile_id = profile_manager.save_profile(
            name="seed-test",
            profile_spec=sample_profile_spec
        )
        
        exec_id = profile_manager.record_execution(
            profile_id=profile_id,
            seed=42,
            count=100,
            duration_ms=1500
        )
        
        # Verify seed stored
        executions = profile_manager.get_executions(profile_id)
        assert executions[0].seed == 42
    
    def test_record_execution_with_cohort(self, profile_manager, sample_profile_spec):
        """Test recording execution linked to cohort."""
        profile_id = profile_manager.save_profile(
            name="cohort-link",
            profile_spec=sample_profile_spec
        )
        
        profile_manager.record_execution(
            profile_id=profile_id,
            cohort_id="cohort-123",
            count=100,
            duration_ms=1500
        )
        
        executions = profile_manager.get_executions(profile_id)
        assert executions[0].cohort_id == "cohort-123"
    
    def test_record_failed_execution(self, profile_manager, sample_profile_spec):
        """Test recording a failed execution."""
        profile_id = profile_manager.save_profile(
            name="failed-test",
            profile_spec=sample_profile_spec
        )
        
        profile_manager.record_execution(
            profile_id=profile_id,
            status="failed",
            error_message="Test error message",
            count=0,
            duration_ms=100
        )
        
        executions = profile_manager.get_executions(profile_id)
        assert executions[0].status == "failed"
        assert executions[0].error_message == "Test error message"


class TestGetExecutions:
    """Tests for get_executions()."""
    
    def test_get_executions_ordered_by_time(self, profile_manager, sample_profile_spec):
        """Test executions are returned newest first."""
        profile_id = profile_manager.save_profile(
            name="order-test",
            profile_spec=sample_profile_spec
        )
        
        profile_manager.record_execution(profile_id=profile_id, count=1, duration_ms=100)
        profile_manager.record_execution(profile_id=profile_id, count=2, duration_ms=200)
        profile_manager.record_execution(profile_id=profile_id, count=3, duration_ms=300)
        
        executions = profile_manager.get_executions(profile_id)
        
        assert len(executions) == 3
        assert executions[0].count == 3  # Newest first
        assert executions[2].count == 1  # Oldest last
    
    def test_get_executions_with_limit(self, profile_manager, sample_profile_spec):
        """Test limiting execution results."""
        profile_id = profile_manager.save_profile(
            name="limit-test",
            profile_spec=sample_profile_spec
        )
        
        for i in range(5):
            profile_manager.record_execution(profile_id=profile_id, count=i, duration_ms=100)
        
        executions = profile_manager.get_executions(profile_id, limit=2)
        
        assert len(executions) == 2
    
    def test_get_executions_returns_records(self, profile_manager, sample_profile_spec):
        """Test that get_executions returns ExecutionRecords."""
        profile_id = profile_manager.save_profile(
            name="record-type-test",
            profile_spec=sample_profile_spec
        )
        
        profile_manager.record_execution(
            profile_id=profile_id,
            cohort_id="cohort-xyz",
            seed=123,
            count=50,
            duration_ms=750,
            status="completed"
        )
        
        executions = profile_manager.get_executions(profile_id)
        exec_record = executions[0]
        
        assert isinstance(exec_record, ExecutionRecord)
        assert exec_record.cohort_id == "cohort-xyz"
        assert exec_record.seed == 123
        assert exec_record.count == 50
        assert exec_record.duration_ms == 750
        assert exec_record.status == "completed"


class TestGetCohortProfile:
    """Tests for get_cohort_profile()."""
    
    def test_get_profile_for_cohort(self, profile_manager, sample_profile_spec):
        """Test getting profile used to generate a cohort."""
        profile_id = profile_manager.save_profile(
            name="cohort-profile",
            profile_spec=sample_profile_spec
        )
        
        profile_manager.record_execution(
            profile_id=profile_id,
            cohort_id="my-cohort-123",
            count=100,
            duration_ms=1500
        )
        
        profile = profile_manager.get_cohort_profile("my-cohort-123")
        
        assert profile is not None
        assert profile.name == "cohort-profile"
    
    def test_get_profile_for_unknown_cohort(self, profile_manager):
        """Test that unknown cohort returns None."""
        profile = profile_manager.get_cohort_profile("unknown-cohort")
        assert profile is None


class TestGetExecutionSpec:
    """Tests for get_execution_spec()."""
    
    def test_get_spec_with_seed(self, profile_manager, sample_profile_spec):
        """Test getting execution spec with seed applied."""
        profile_id = profile_manager.save_profile(
            name="spec-test",
            profile_spec=sample_profile_spec
        )
        
        exec_id = profile_manager.record_execution(
            profile_id=profile_id,
            seed=42,
            count=200,
            duration_ms=1500
        )
        
        spec = profile_manager.get_execution_spec(exec_id)
        
        assert spec["profile"]["generation"]["seed"] == 42
        assert spec["profile"]["generation"]["count"] == 200
    
    def test_get_spec_nonexistent_raises(self, profile_manager):
        """Test that nonexistent execution raises ValueError."""
        with pytest.raises(ValueError, match="not found"):
            profile_manager.get_execution_spec(99999)


# =============================================================================
# Convenience Function Tests
# =============================================================================

class TestConvenienceFunctions:
    """Tests for convenience functions."""
    
    def test_get_profile_manager_with_connection(self, temp_db):
        """Test get_profile_manager with explicit connection."""
        manager = get_profile_manager(temp_db)
        assert isinstance(manager, ProfileManager)
