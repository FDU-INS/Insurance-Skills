"""Tests for DuckDB-backed state manager."""

import pytest
from datetime import datetime
import tempfile
from pathlib import Path
from uuid import uuid4

from healthsim.db import DatabaseConnection
from healthsim.state.manager import StateManager, reset_manager


@pytest.fixture
def test_db():
    """Create a temporary test database with schema applied."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test_state.duckdb"
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


class TestSaveScenario:
    """Tests for save_cohort functionality."""
    
    def test_save_empty_cohort(self, state_manager):
        """Can save a cohort with no entities."""
        cohort_id = state_manager.save_cohort(
            name='empty-cohort',
            entities={},
            description='An empty test cohort'
        )
        
        assert cohort_id is not None
        assert len(cohort_id) == 36  # UUID format
    
    def test_save_cohort_with_patients(self, state_manager):
        """Can save a cohort with patient entities."""
        entities = {
            'patients': [
                {
                    'patient_id': str(uuid4()),
                    'mrn': 'MRN001',
                    'given_name': 'John',
                    'family_name': 'Doe',
                    'birth_date': '1980-01-15',
                    'gender': 'male',
                },
                {
                    'patient_id': str(uuid4()),
                    'mrn': 'MRN002',
                    'given_name': 'Jane',
                    'family_name': 'Smith',
                    'birth_date': '1985-06-20',
                    'gender': 'female',
                },
            ]
        }
        
        cohort_id = state_manager.save_cohort(
            name='patient-cohort',
            entities=entities,
            description='Test with patients'
        )
        
        assert cohort_id is not None
    
    def test_save_cohort_with_multiple_entity_types(self, state_manager):
        """Can save cohort with multiple entity types."""
        entities = {
            'patients': [
                {'patient_id': str(uuid4()), 'mrn': 'MRN001', 'given_name': 'John', 'family_name': 'Doe', 'birth_date': '1980-01-15', 'gender': 'male'}
            ],
            'encounters': [
                {'encounter_id': str(uuid4()), 'patient_mrn': 'MRN001', 'class_code': 'O', 'status': 'finished', 'admission_time': '2024-01-15T09:00:00'}
            ],
        }
        
        cohort_id = state_manager.save_cohort(
            name='multi-entity-cohort',
            entities=entities,
        )
        
        assert cohort_id is not None
    
    def test_save_cohort_with_tags(self, state_manager):
        """Can save cohort with tags."""
        cohort_id = state_manager.save_cohort(
            name='tagged-cohort',
            entities={'patients': []},
            tags=['diabetes', 'chronic', 'test'],
        )
        
        tags = state_manager.get_cohort_tags('tagged-cohort')
        assert 'diabetes' in tags
        assert 'chronic' in tags
        assert 'test' in tags
    
    def test_save_duplicate_name_fails(self, state_manager):
        """Saving with duplicate name raises error without overwrite."""
        state_manager.save_cohort(name='duplicate', entities={})
        
        with pytest.raises(ValueError, match="already exists"):
            state_manager.save_cohort(name='duplicate', entities={})
    
    def test_save_with_overwrite(self, state_manager):
        """Can overwrite existing cohort."""
        # Save original
        state_manager.save_cohort(
            name='overwrite-test',
            entities={'patients': [{'given_name': 'Original', 'family_name': 'Person', 'birth_date': '1990-01-01', 'gender': 'male'}]},
        )
        
        # Overwrite
        state_manager.save_cohort(
            name='overwrite-test',
            entities={'patients': [{'given_name': 'Updated', 'family_name': 'Person', 'birth_date': '1990-01-01', 'gender': 'male'}]},
            overwrite=True,
        )
        
        # Verify updated
        loaded = state_manager.load_cohort('overwrite-test')
        assert loaded['entities']['patients'][0]['given_name'] == 'Updated'


class TestLoadScenario:
    """Tests for load_cohort functionality."""
    
    def test_load_by_name(self, state_manager):
        """Can load cohort by name."""
        state_manager.save_cohort(name='load-by-name', entities={})
        
        loaded = state_manager.load_cohort('load-by-name')
        assert loaded['name'] == 'load-by-name'
    
    def test_load_by_id(self, state_manager):
        """Can load cohort by UUID."""
        cohort_id = state_manager.save_cohort(name='load-by-id', entities={})
        
        loaded = state_manager.load_cohort(cohort_id)
        assert loaded['cohort_id'] == cohort_id
    
    def test_load_not_found(self, state_manager):
        """Loading non-existent cohort raises error."""
        with pytest.raises(ValueError, match="not found"):
            state_manager.load_cohort('nonexistent-cohort')
    
    def test_load_preserves_entities(self, state_manager):
        """Loaded entities match saved entities."""
        original_entities = {
            'patients': [
                {
                    'patient_id': str(uuid4()),
                    'mrn': 'MRN123',
                    'given_name': 'Test',
                    'family_name': 'Patient',
                    'birth_date': '1975-03-10',
                    'gender': 'female',
                    'race': 'white',
                    'ethnicity': 'non-hispanic',
                }
            ]
        }
        
        state_manager.save_cohort(
            name='preserve-test',
            entities=original_entities,
        )
        
        loaded = state_manager.load_cohort('preserve-test')
        
        assert len(loaded['entities']['patients']) == 1
        patient = loaded['entities']['patients'][0]
        assert patient['given_name'] == 'Test'
        assert patient['family_name'] == 'Patient'
        assert patient['mrn'] == 'MRN123'
    
    def test_load_returns_metadata(self, state_manager):
        """Loaded cohort includes metadata."""
        state_manager.save_cohort(
            name='metadata-test',
            entities={},
            description='Test description',
            tags=['tag1', 'tag2'],
        )
        
        loaded = state_manager.load_cohort('metadata-test')
        
        assert loaded['name'] == 'metadata-test'
        assert loaded['description'] == 'Test description'
        assert 'tag1' in loaded['tags']
        assert 'tag2' in loaded['tags']
        assert 'created_at' in loaded
        assert 'updated_at' in loaded


class TestListScenarios:
    """Tests for list_cohorts functionality."""
    
    def test_list_empty(self, state_manager):
        """List returns empty when no cohorts."""
        cohorts = state_manager.list_cohorts()
        assert cohorts == []
    
    def test_list_all(self, state_manager):
        """List returns all cohorts."""
        state_manager.save_cohort(name='list-1', entities={})
        state_manager.save_cohort(name='list-2', entities={})
        state_manager.save_cohort(name='list-3', entities={})
        
        cohorts = state_manager.list_cohorts()
        names = [s['name'] for s in cohorts]
        
        assert 'list-1' in names
        assert 'list-2' in names
        assert 'list-3' in names
    
    def test_list_filter_by_tag(self, state_manager):
        """Can filter cohorts by tag."""
        state_manager.save_cohort(name='diabetes-1', entities={}, tags=['diabetes'])
        state_manager.save_cohort(name='diabetes-2', entities={}, tags=['diabetes', 'chronic'])
        state_manager.save_cohort(name='cardiac-1', entities={}, tags=['cardiac'])
        
        diabetes_cohorts = state_manager.list_cohorts(tag='diabetes')
        names = [s['name'] for s in diabetes_cohorts]
        
        assert 'diabetes-1' in names
        assert 'diabetes-2' in names
        assert 'cardiac-1' not in names
    
    def test_list_search(self, state_manager):
        """Can search cohorts by name/description."""
        state_manager.save_cohort(name='alpha-cohort', entities={}, description='First test')
        state_manager.save_cohort(name='beta-cohort', entities={}, description='Second alpha test')
        state_manager.save_cohort(name='gamma-cohort', entities={}, description='Third test')
        
        # Search in name
        results = state_manager.list_cohorts(search='alpha')
        names = [s['name'] for s in results]
        assert 'alpha-cohort' in names
        assert 'beta-cohort' in names  # 'alpha' in description
        assert 'gamma-cohort' not in names
    
    def test_list_with_limit(self, state_manager):
        """List respects limit parameter."""
        for i in range(10):
            state_manager.save_cohort(name=f'limited-{i}', entities={})
        
        cohorts = state_manager.list_cohorts(limit=5)
        assert len(cohorts) == 5
    
    def test_list_ordered_by_updated(self, state_manager):
        """List returns cohorts ordered by updated_at desc."""
        state_manager.save_cohort(name='old', entities={})
        state_manager.save_cohort(name='newer', entities={})
        state_manager.save_cohort(name='newest', entities={})
        
        cohorts = state_manager.list_cohorts()
        # Most recently updated should be first
        assert cohorts[0]['name'] == 'newest'


class TestDeleteScenario:
    """Tests for delete_cohort functionality."""
    
    def test_delete_by_name(self, state_manager):
        """Can delete cohort by name."""
        state_manager.save_cohort(name='to-delete', entities={})
        
        result = state_manager.delete_cohort('to-delete', confirm=True)
        assert result is True
        
        cohorts = state_manager.list_cohorts()
        names = [s['name'] for s in cohorts]
        assert 'to-delete' not in names
    
    def test_delete_by_id(self, state_manager):
        """Can delete cohort by UUID."""
        cohort_id = state_manager.save_cohort(name='delete-by-id', entities={})
        
        result = state_manager.delete_cohort(cohort_id, confirm=True)
        assert result is True
    
    def test_delete_not_found(self, state_manager):
        """Delete returns False for non-existent cohort."""
        result = state_manager.delete_cohort('nonexistent', confirm=True)
        assert result is False
    
    def test_delete_removes_tags(self, state_manager):
        """Delete also removes associated tags."""
        state_manager.save_cohort(
            name='tagged-delete',
            entities={},
            tags=['tag1', 'tag2'],
        )
        
        state_manager.delete_cohort('tagged-delete', confirm=True)
        
        # Verify tags are gone by checking the tags table directly
        result = state_manager.conn.execute(
            "SELECT COUNT(*) FROM cohort_tags WHERE cohort_id IN (SELECT id FROM cohorts WHERE name = 'tagged-delete')"
        ).fetchone()
        assert result[0] == 0


class TestScenarioExists:
    """Tests for cohort_exists functionality."""
    
    def test_exists_by_name(self, state_manager):
        """cohort_exists returns True for existing name."""
        state_manager.save_cohort(name='exists-test', entities={})
        
        assert state_manager.cohort_exists('exists-test') is True
    
    def test_exists_by_id(self, state_manager):
        """cohort_exists returns True for existing UUID."""
        cohort_id = state_manager.save_cohort(name='exists-by-id', entities={})
        
        assert state_manager.cohort_exists(cohort_id) is True
    
    def test_not_exists(self, state_manager):
        """cohort_exists returns False for non-existent cohort."""
        assert state_manager.cohort_exists('nonexistent') is False


class TestEntityRoundTrip:
    """Tests for entity data round-trip (save → load)."""
    
    def test_patient_round_trip(self, state_manager):
        """Patient data survives save/load cycle."""
        original = {
            'patient_id': str(uuid4()),
            'mrn': 'MRN999',
            'given_name': 'Alice',
            'family_name': 'Wonderland',
            'birth_date': '1990-05-15',
            'gender': 'female',
            'race': 'asian',
            'ethnicity': 'non-hispanic',
            'address': {
                'line1': '123 Main St',
                'city': 'Anytown',
                'state': 'CA',
                'postalCode': '90210',
            },
            'telecom': {
                'phone': '555-1234',
                'email': 'alice@example.com',
            },
        }
        
        state_manager.save_cohort(
            name='round-trip-test',
            entities={'patients': [original]},
        )
        
        loaded = state_manager.load_cohort('round-trip-test')
        patient = loaded['entities']['patients'][0]
        
        # Core fields
        assert patient['given_name'] == 'Alice'
        assert patient['family_name'] == 'Wonderland'
        assert patient['mrn'] == 'MRN999'
        
        # Nested fields (stored as JSON)
        assert patient.get('address', {}).get('city') == 'Anytown' or patient.get('city') == 'Anytown'
    
    def test_encounter_round_trip(self, state_manager):
        """Encounter data survives save/load cycle."""
        original = {
            'encounter_id': str(uuid4()),
            'patient_mrn': 'MRN001',
            'class_code': 'I',
            'status': 'in-progress',
            'admission_time': '2024-06-15T10:30:00',
            'facility': 'General Hospital',
            'department': 'Cardiology',
            'chief_complaint': 'Chest pain',
        }
        
        state_manager.save_cohort(
            name='encounter-round-trip',
            entities={'encounters': [original]},
        )
        
        loaded = state_manager.load_cohort('encounter-round-trip')
        encounter = loaded['entities']['encounters'][0]
        
        assert encounter['patient_mrn'] == 'MRN001'
        assert encounter['class_code'] == 'I'
        assert encounter['chief_complaint'] == 'Chest pain'
    
    def test_multiple_entity_types_round_trip(self, state_manager):
        """Multiple entity types survive save/load cycle."""
        entities = {
            'patients': [
                {'patient_id': str(uuid4()), 'mrn': 'MRN001', 'given_name': 'John', 'family_name': 'Doe', 'birth_date': '1980-01-01', 'gender': 'male'}
            ],
            'encounters': [
                {'encounter_id': str(uuid4()), 'patient_mrn': 'MRN001', 'class_code': 'O', 'status': 'finished', 'admission_time': '2024-01-15T09:00:00'}
            ],
            'members': [
                {'member_id': str(uuid4()), 'given_name': 'John', 'family_name': 'Doe', 'subscriber_id': 'SUB001'}
            ],
        }
        
        state_manager.save_cohort(
            name='multi-type-round-trip',
            entities=entities,
        )
        
        loaded = state_manager.load_cohort('multi-type-round-trip')
        
        assert len(loaded['entities']['patients']) == 1
        assert len(loaded['entities']['encounters']) == 1
        assert len(loaded['entities']['members']) == 1


class TestTagManagement:
    """Tests for tag management functionality."""
    
    def test_get_tags(self, state_manager):
        """Can get tags for a cohort."""
        state_manager.save_cohort(
            name='get-tags-test',
            entities={},
            tags=['alpha', 'beta', 'gamma'],
        )
        
        tags = state_manager.get_cohort_tags('get-tags-test')
        
        assert 'alpha' in tags
        assert 'beta' in tags
        assert 'gamma' in tags
    
    def test_add_tags(self, state_manager):
        """Can add tags to existing cohort."""
        state_manager.save_cohort(
            name='add-tags-test',
            entities={},
            tags=['original'],
        )
        
        state_manager.add_cohort_tags('add-tags-test', ['new1', 'new2'])
        
        tags = state_manager.get_cohort_tags('add-tags-test')
        assert 'original' in tags
        assert 'new1' in tags
        assert 'new2' in tags
    
    def test_add_duplicate_tag(self, state_manager):
        """Adding duplicate tag doesn't create duplicates."""
        state_manager.save_cohort(
            name='dup-tag-test',
            entities={},
            tags=['tag1'],
        )
        
        state_manager.add_cohort_tags('dup-tag-test', ['tag1', 'tag1'])
        
        tags = state_manager.get_cohort_tags('dup-tag-test')
        assert tags.count('tag1') == 1
