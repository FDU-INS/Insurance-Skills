"""Tests for JSON to DuckDB migration."""

import pytest
import json
from pathlib import Path
import tempfile
import shutil

from healthsim.db import DatabaseConnection
from healthsim.db.migrate.json_cohorts import (
    MigrationResult,
    discover_json_cohorts,
    migrate_cohort,
    migrate_all_cohorts,
    backup_json_cohorts,
    verify_migration,
    get_migration_status,
)
from healthsim.state.manager import StateManager, reset_manager


@pytest.fixture
def temp_dirs(tmp_path):
    """Create temporary directories for testing."""
    legacy_dir = tmp_path / "cohorts"
    backup_dir = tmp_path / "backup"
    db_dir = tmp_path / "db"
    
    legacy_dir.mkdir()
    db_dir.mkdir()
    
    return {
        'legacy': legacy_dir,
        'backup': backup_dir,
        'db': db_dir,
    }


@pytest.fixture
def sample_json_cohorts(temp_dirs):
    """Create sample JSON cohort files."""
    legacy_dir = temp_dirs['legacy']
    
    # Cohort 1: Simple patient
    cohort1 = {
        'name': 'test-cohort-1',
        'description': 'First test cohort',
        'entities': {
            'patients': [{'patient_id': 'p1', 'given_name': 'Alice', 'family_name': 'Smith'}]
        },
        'tags': ['test']
    }
    
    # Cohort 2: Multiple entities
    cohort2 = {
        'name': 'test-cohort-2',
        'description': 'Second test cohort',
        'entities': {
            'patients': [
                {'patient_id': 'p2', 'given_name': 'Bob', 'family_name': 'Jones'},
                {'patient_id': 'p3', 'given_name': 'Carol', 'family_name': 'Davis'}
            ],
            'encounters': [
                {'encounter_id': 'e1', 'patient_id': 'p2', 'encounter_type': 'outpatient'}
            ]
        },
        'tags': ['test', 'multi']
    }
    
    # Cohort 3: Legacy format (entities at top level)
    cohort3 = {
        'name': 'legacy-format',
        'patients': [{'patient_id': 'p4', 'given_name': 'Dave'}],
        'encounters': []
    }
    
    (legacy_dir / "test-cohort-1.json").write_text(json.dumps(cohort1))
    (legacy_dir / "test-cohort-2.json").write_text(json.dumps(cohort2))
    (legacy_dir / "legacy-format.json").write_text(json.dumps(cohort3))
    
    return legacy_dir


@pytest.fixture
def test_db(temp_dirs):
    """Create test database."""
    db_path = temp_dirs['db'] / "test_migration.duckdb"
    db_conn = DatabaseConnection(db_path)
    conn = db_conn.connect()
    yield conn
    db_conn.close()


@pytest.fixture
def state_manager(test_db):
    """Create state manager with test database."""
    manager = StateManager(connection=test_db)
    yield manager
    reset_manager()


class TestMigrationResult:
    """Tests for MigrationResult dataclass."""
    
    def test_success_repr(self):
        """Success result shows entity count."""
        result = MigrationResult(name='test', success=True, entity_count=5)
        repr_str = repr(result)
        assert '✓' in repr_str
        assert 'test' in repr_str
        assert '5 entities' in repr_str
    
    def test_failure_repr(self):
        """Failure result shows error."""
        result = MigrationResult(name='test', success=False, error='File not found')
        repr_str = repr(result)
        assert '✗' in repr_str
        assert 'test' in repr_str
        assert 'File not found' in repr_str
    
    def test_dry_run_repr(self):
        """Dry run shows special indicator."""
        result = MigrationResult(name='test', success=True, entity_count=-1)
        repr_str = repr(result)
        assert '✓' in repr_str
        assert 'dry run' in repr_str


class TestDiscoverCohorts:
    """Tests for cohort discovery."""
    
    def test_discover_empty_directory(self, temp_dirs):
        """Empty directory returns empty list."""
        cohorts = discover_json_cohorts(temp_dirs['legacy'])
        assert cohorts == []
    
    def test_discover_finds_cohorts(self, sample_json_cohorts):
        """Discovers all JSON files."""
        cohorts = discover_json_cohorts(sample_json_cohorts)
        
        assert len(cohorts) == 3
        names = [s['name'] for s in cohorts]
        assert 'test-cohort-1' in names
        assert 'test-cohort-2' in names
        assert 'legacy-format' in names
    
    def test_discover_includes_metadata(self, sample_json_cohorts):
        """Discovered cohorts include metadata."""
        cohorts = discover_json_cohorts(sample_json_cohorts)
        
        for s in cohorts:
            assert 'name' in s
            assert 'path' in s
            assert 'size_bytes' in s
            assert 'modified_at' in s
            assert s['size_bytes'] > 0
    
    def test_discover_nonexistent_directory(self, temp_dirs):
        """Nonexistent directory returns empty list."""
        cohorts = discover_json_cohorts(temp_dirs['backup'])  # Doesn't exist
        assert cohorts == []


class TestMigrateCohort:
    """Tests for single cohort migration."""
    
    def test_migrate_simple_cohort(self, sample_json_cohorts, state_manager):
        """Migrates a simple cohort."""
        json_path = sample_json_cohorts / "test-cohort-1.json"
        
        result = migrate_cohort(json_path, state_manager)
        
        assert result.success
        assert result.name == "test-cohort-1"
        assert result.entity_count == 1
        assert result.error is None
    
    def test_migrate_multi_entity_cohort(self, sample_json_cohorts, state_manager):
        """Migrates cohort with multiple entities."""
        json_path = sample_json_cohorts / "test-cohort-2.json"
        
        result = migrate_cohort(json_path, state_manager)
        
        assert result.success
        assert result.name == "test-cohort-2"
        assert result.entity_count == 3  # 2 patients + 1 encounter
    
    def test_migrate_legacy_format(self, sample_json_cohorts, state_manager):
        """Migrates legacy format cohort."""
        json_path = sample_json_cohorts / "legacy-format.json"
        
        result = migrate_cohort(json_path, state_manager)
        
        assert result.success
        assert result.name == "legacy-format"
        assert result.entity_count == 1
    
    def test_migrate_preserves_data(self, sample_json_cohorts, state_manager):
        """Migration preserves entity data."""
        json_path = sample_json_cohorts / "test-cohort-1.json"
        
        migrate_cohort(json_path, state_manager)
        
        loaded = state_manager.load_cohort("test-cohort-1")
        assert len(loaded['entities']['patients']) == 1
        assert loaded['entities']['patients'][0]['given_name'] == 'Alice'
    
    def test_migrate_invalid_json(self, temp_dirs, state_manager):
        """Handles invalid JSON gracefully."""
        invalid_path = temp_dirs['legacy'] / "invalid.json"
        invalid_path.write_text("not valid json {")
        
        result = migrate_cohort(invalid_path, state_manager)
        
        assert not result.success
        assert result.error is not None
    
    def test_migrate_duplicate_without_overwrite(self, sample_json_cohorts, state_manager):
        """Duplicate name fails without overwrite."""
        json_path = sample_json_cohorts / "test-cohort-1.json"
        
        # First migration
        result1 = migrate_cohort(json_path, state_manager)
        assert result1.success
        
        # Second migration should fail
        result2 = migrate_cohort(json_path, state_manager, overwrite=False)
        assert not result2.success
    
    def test_migrate_duplicate_with_overwrite(self, sample_json_cohorts, state_manager):
        """Duplicate name succeeds with overwrite."""
        json_path = sample_json_cohorts / "test-cohort-1.json"
        
        # First migration
        result1 = migrate_cohort(json_path, state_manager)
        assert result1.success
        
        # Second migration with overwrite
        result2 = migrate_cohort(json_path, state_manager, overwrite=True)
        assert result2.success


class TestMigrateAll:
    """Tests for batch migration."""
    
    def test_migrate_all_empty(self, temp_dirs):
        """Empty directory returns empty results."""
        results, backup = migrate_all_cohorts(
            legacy_path=temp_dirs['legacy'],
            backup_path=temp_dirs['backup']
        )
        
        assert results == []
        assert backup is None
    
    def test_migrate_all_dry_run(self, sample_json_cohorts, temp_dirs):
        """Dry run reports but doesn't migrate."""
        results, backup = migrate_all_cohorts(
            dry_run=True,
            legacy_path=sample_json_cohorts,
            backup_path=temp_dirs['backup']
        )
        
        assert len(results) == 3
        for r in results:
            assert r.success
            assert r.entity_count == -1  # Dry run indicator
        
        # Original files should still exist
        assert (sample_json_cohorts / "test-cohort-1.json").exists()


class TestBackup:
    """Tests for backup functionality."""
    
    def test_backup_creates_directory(self, sample_json_cohorts, temp_dirs):
        """Backup moves files to backup location."""
        backup_path = backup_json_cohorts(
            source_path=sample_json_cohorts,
            backup_path=temp_dirs['backup']
        )
        
        assert backup_path is not None
        assert backup_path.exists()
        assert not sample_json_cohorts.exists()
    
    def test_backup_preserves_files(self, sample_json_cohorts, temp_dirs):
        """Backup preserves all files."""
        original_files = list(sample_json_cohorts.glob("*.json"))
        
        backup_path = backup_json_cohorts(
            source_path=sample_json_cohorts,
            backup_path=temp_dirs['backup']
        )
        
        backup_files = list(backup_path.glob("*.json"))
        assert len(backup_files) == len(original_files)
    
    def test_backup_nonexistent_source(self, temp_dirs):
        """Nonexistent source returns None."""
        result = backup_json_cohorts(
            source_path=temp_dirs['backup'],  # Doesn't exist
            backup_path=temp_dirs['backup']
        )
        
        assert result is None
    
    def test_backup_existing_backup_adds_timestamp(self, sample_json_cohorts, temp_dirs):
        """Existing backup gets timestamped name."""
        # Create initial backup
        temp_dirs['backup'].mkdir()
        (temp_dirs['backup'] / "existing.json").write_text("{}")
        
        backup_path = backup_json_cohorts(
            source_path=sample_json_cohorts,
            backup_path=temp_dirs['backup']
        )
        
        # Should create timestamped directory
        assert backup_path is not None
        assert 'cohorts_backup_' in backup_path.name


class TestVerification:
    """Tests for migration verification."""
    
    def test_verify_success(self, sample_json_cohorts, state_manager, temp_dirs):
        """Verification passes when all migrated."""
        # Migrate cohorts
        for json_path in sample_json_cohorts.glob("*.json"):
            migrate_cohort(json_path, state_manager)
        
        # Verify using the same manager (proper dependency injection)
        verification = verify_migration(
            expected_count=3,
            expected_names=['test-cohort-1', 'test-cohort-2', 'legacy-format'],
            manager=state_manager
        )
        
        assert verification['success']
        assert verification['count_match']
        assert len(verification['missing']) == 0
    
    def test_verify_missing_cohorts(self, sample_json_cohorts, state_manager):
        """Verification reports missing cohorts."""
        # Only migrate one
        migrate_cohort(sample_json_cohorts / "test-cohort-1.json", state_manager)
        
        verification = verify_migration(
            expected_count=3,
            expected_names=['test-cohort-1', 'test-cohort-2', 'missing'],
            manager=state_manager
        )
        
        assert not verification['success']
        assert 'test-cohort-2' in verification['missing']
        assert 'missing' in verification['missing']
