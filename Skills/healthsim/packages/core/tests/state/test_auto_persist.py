"""Tests for auto-persist service."""

import pytest
from datetime import datetime
import tempfile
from pathlib import Path
from uuid import uuid4

from healthsim.db import DatabaseConnection
from healthsim.state.auto_persist import (
    AutoPersistService,
    PersistResult,
    QueryResult,
    CohortBrief,
    get_auto_persist_service,
    reset_service,
)


@pytest.fixture
def test_db():
    """Create a temporary test database with schema applied."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test_auto_persist.duckdb"
        db_conn = DatabaseConnection(db_path)
        conn = db_conn.connect()
        yield conn
        db_conn.close()


@pytest.fixture
def service(test_db):
    """Create auto-persist service with test database."""
    svc = AutoPersistService(connection=test_db)
    yield svc
    reset_service()


class TestPersistEntities:
    """Tests for persist_entities functionality."""
    
    def test_persist_creates_cohort(self, service):
        """Persisting entities creates a new cohort."""
        entities = [
            {'patient_id': str(uuid4()), 'mrn': 'MRN001', 'given_name': 'John', 
             'family_name': 'Doe', 'birth_date': '1980-01-15', 'gender': 'male'}
        ]
        
        result = service.persist_entities(
            entities=entities,
            entity_type='patient',
        )
        
        assert result.is_new_cohort is True
        assert result.entities_persisted == 1
        assert result.cohort_id is not None
    
    def test_persist_uses_context_keywords(self, service):
        """Cohort name uses context keywords."""
        entities = [
            {'patient_id': str(uuid4()), 'mrn': 'MRN001', 'given_name': 'Jane',
             'family_name': 'Doe', 'birth_date': '1990-06-15', 'gender': 'female'}
        ]
        
        result = service.persist_entities(
            entities=entities,
            entity_type='patient',
            context_keywords=['diabetes', 'elderly'],
        )
        
        assert 'diabetes' in result.cohort_name or 'elderly' in result.cohort_name
    
    def test_persist_uses_existing_cohort(self, service):
        """Can add entities to existing cohort."""
        # Create first batch
        result1 = service.persist_entities(
            entities=[{'patient_id': str(uuid4()), 'mrn': 'MRN001', 'given_name': 'First',
                      'family_name': 'Patient', 'birth_date': '1980-01-01', 'gender': 'male'}],
            entity_type='patient',
        )
        
        # Add more to same cohort
        result2 = service.persist_entities(
            entities=[{'patient_id': str(uuid4()), 'mrn': 'MRN002', 'given_name': 'Second',
                      'family_name': 'Patient', 'birth_date': '1985-06-15', 'gender': 'female'}],
            entity_type='patient',
            cohort_id=result1.cohort_id,
        )
        
        assert result2.is_new_cohort is False
        assert result2.cohort_id == result1.cohort_id
        assert result2.summary.entity_counts['patients'] == 2
    
    def test_persist_returns_summary_not_data(self, service):
        """Result contains summary, not full entity data."""
        entities = [
            {'patient_id': str(uuid4()), 'mrn': f'MRN{i:03d}', 'given_name': f'Patient{i}',
             'family_name': 'Test', 'birth_date': '1980-01-01', 'gender': 'male'}
            for i in range(10)
        ]
        
        result = service.persist_entities(
            entities=entities,
            entity_type='patient',
        )
        
        # Summary should have counts
        assert result.summary.entity_counts['patients'] == 10
        
        # Samples should be limited (not all entities)
        assert len(result.summary.samples.get('patients', [])) <= 3
    
    def test_persist_empty_raises_error(self, service):
        """Persisting empty list raises error."""
        with pytest.raises(ValueError, match="No entities"):
            service.persist_entities(entities=[], entity_type='patient')


class TestGetCohortSummary:
    """Tests for get_cohort_summary functionality."""
    
    def test_get_summary_by_id(self, service):
        """Can get summary by cohort ID."""
        # Create cohort
        result = service.persist_entities(
            entities=[{'patient_id': str(uuid4()), 'mrn': 'MRN001', 'given_name': 'Test',
                      'family_name': 'Patient', 'birth_date': '1980-01-01', 'gender': 'male'}],
            entity_type='patient',
        )
        
        summary = service.get_cohort_summary(cohort_id=result.cohort_id)
        
        assert summary.cohort_id == result.cohort_id
        assert summary.entity_counts['patients'] == 1
    
    def test_get_summary_by_name(self, service):
        """Can get summary by cohort name."""
        result = service.persist_entities(
            entities=[{'patient_id': str(uuid4()), 'mrn': 'MRN001', 'given_name': 'Test',
                      'family_name': 'Patient', 'birth_date': '1980-01-01', 'gender': 'male'}],
            entity_type='patient',
            cohort_name='my-test-cohort',
        )
        
        summary = service.get_cohort_summary(cohort_name='my-test-cohort')
        
        assert summary.name == 'my-test-cohort'
    
    def test_get_summary_without_samples(self, service):
        """Can get summary without samples."""
        result = service.persist_entities(
            entities=[{'patient_id': str(uuid4()), 'mrn': 'MRN001', 'given_name': 'Test',
                      'family_name': 'Patient', 'birth_date': '1980-01-01', 'gender': 'male'}],
            entity_type='patient',
        )
        
        summary = service.get_cohort_summary(
            cohort_id=result.cohort_id,
            include_samples=False
        )
        
        assert summary.samples == {}
    
    def test_get_summary_not_found(self, service):
        """Getting non-existent cohort raises error."""
        with pytest.raises(ValueError, match="not found"):
            service.get_cohort_summary(cohort_name='nonexistent')


class TestQueryCohort:
    """Tests for query_cohort functionality."""
    
    def test_basic_query(self, service):
        """Can execute basic SELECT query."""
        # Create cohort with data
        entities = [
            {'patient_id': str(uuid4()), 'mrn': f'MRN{i:03d}', 'given_name': f'Patient{i}',
             'family_name': 'Test', 'birth_date': '1980-01-01', 'gender': 'male' if i % 2 == 0 else 'female'}
            for i in range(10)
        ]
        result = service.persist_entities(entities=entities, entity_type='patient')
        
        query_result = service.query_cohort(
            cohort_id=result.cohort_id,
            query="SELECT * FROM patients",
        )
        
        assert query_result.total_count == 10
        assert len(query_result.results) <= 20  # Default page size
    
    def test_query_with_filter(self, service):
        """Can execute filtered query."""
        entities = [
            {'patient_id': str(uuid4()), 'mrn': f'MRN{i:03d}', 'given_name': f'Patient{i}',
             'family_name': 'Test', 'birth_date': '1980-01-01', 'gender': 'male' if i % 2 == 0 else 'female'}
            for i in range(10)
        ]
        result = service.persist_entities(entities=entities, entity_type='patient')
        
        query_result = service.query_cohort(
            cohort_id=result.cohort_id,
            query="SELECT * FROM patients WHERE gender = 'male'",
        )
        
        assert query_result.total_count == 5
    
    def test_query_pagination(self, service):
        """Query respects pagination."""
        entities = [
            {'patient_id': str(uuid4()), 'mrn': f'MRN{i:03d}', 'given_name': f'Patient{i}',
             'family_name': 'Test', 'birth_date': '1980-01-01', 'gender': 'male'}
            for i in range(50)
        ]
        result = service.persist_entities(entities=entities, entity_type='patient')
        
        # First page
        page1 = service.query_cohort(
            cohort_id=result.cohort_id,
            query="SELECT * FROM patients",
            limit=10,
            offset=0,
        )
        
        assert len(page1.results) == 10
        assert page1.has_more is True
        assert page1.page == 0
        
        # Second page
        page2 = service.query_cohort(
            cohort_id=result.cohort_id,
            query="SELECT * FROM patients",
            limit=10,
            offset=10,
        )
        
        assert len(page2.results) == 10
        assert page2.page == 1
    
    def test_query_rejects_non_select(self, service):
        """Non-SELECT queries are rejected."""
        result = service.persist_entities(
            entities=[{'patient_id': str(uuid4()), 'mrn': 'MRN001', 'given_name': 'Test',
                      'family_name': 'Patient', 'birth_date': '1980-01-01', 'gender': 'male'}],
            entity_type='patient',
        )
        
        with pytest.raises(ValueError, match="SELECT"):
            service.query_cohort(
                cohort_id=result.cohort_id,
                query="DELETE FROM patients",
            )
    
    def test_query_rejects_dangerous_patterns(self, service):
        """Dangerous SQL patterns are rejected."""
        result = service.persist_entities(
            entities=[{'patient_id': str(uuid4()), 'mrn': 'MRN001', 'given_name': 'Test',
                      'family_name': 'Patient', 'birth_date': '1980-01-01', 'gender': 'male'}],
            entity_type='patient',
        )
        
        with pytest.raises(ValueError):
            service.query_cohort(
                cohort_id=result.cohort_id,
                query="SELECT * FROM patients; DROP TABLE patients;",
            )


class TestListCohorts:
    """Tests for list_cohorts functionality."""
    
    def test_list_empty(self, service):
        """List returns empty when no cohorts."""
        cohorts = service.list_cohorts()
        assert cohorts == []
    
    def test_list_all(self, service):
        """List returns all cohorts."""
        # Create multiple cohorts
        for i in range(3):
            service.persist_entities(
                entities=[{'patient_id': str(uuid4()), 'mrn': f'MRN{i:03d}', 'given_name': f'Patient{i}',
                          'family_name': 'Test', 'birth_date': '1980-01-01', 'gender': 'male'}],
                entity_type='patient',
                cohort_name=f'cohort-{i}',
            )
        
        cohorts = service.list_cohorts()
        
        assert len(cohorts) == 3
    
    def test_list_filter_by_pattern(self, service):
        """Can filter cohorts by name pattern."""
        service.persist_entities(
            entities=[{'patient_id': str(uuid4()), 'mrn': 'MRN001', 'given_name': 'P1',
                      'family_name': 'Test', 'birth_date': '1980-01-01', 'gender': 'male'}],
            entity_type='patient',
            cohort_name='diabetes-test',
        )
        service.persist_entities(
            entities=[{'patient_id': str(uuid4()), 'mrn': 'MRN002', 'given_name': 'P2',
                      'family_name': 'Test', 'birth_date': '1980-01-01', 'gender': 'male'}],
            entity_type='patient',
            cohort_name='cardiac-test',
        )
        
        cohorts = service.list_cohorts(filter_pattern='diabetes')
        
        assert len(cohorts) == 1
        assert cohorts[0].name == 'diabetes-test'


class TestRenameCohort:
    """Tests for rename_cohort functionality."""
    
    def test_rename_cohort(self, service):
        """Can rename a cohort."""
        result = service.persist_entities(
            entities=[{'patient_id': str(uuid4()), 'mrn': 'MRN001', 'given_name': 'Test',
                      'family_name': 'Patient', 'birth_date': '1980-01-01', 'gender': 'male'}],
            entity_type='patient',
            cohort_name='original-name',
        )
        
        old_name, new_name = service.rename_cohort(
            cohort_id=result.cohort_id,
            new_name='new-name',
        )
        
        assert old_name == 'original-name'
        assert new_name == 'new-name'
    
    def test_rename_not_found(self, service):
        """Renaming non-existent cohort raises error."""
        with pytest.raises(ValueError, match="not found"):
            service.rename_cohort(
                cohort_id=str(uuid4()),
                new_name='new-name',
            )


class TestDeleteCohort:
    """Tests for delete_cohort functionality."""
    
    def test_delete_requires_confirm(self, service):
        """Delete requires confirm=True."""
        result = service.persist_entities(
            entities=[{'patient_id': str(uuid4()), 'mrn': 'MRN001', 'given_name': 'Test',
                      'family_name': 'Patient', 'birth_date': '1980-01-01', 'gender': 'male'}],
            entity_type='patient',
        )
        
        with pytest.raises(ValueError, match="confirm"):
            service.delete_cohort(
                cohort_id=result.cohort_id,
                confirm=False,
            )
    
    def test_delete_removes_cohort(self, service):
        """Delete removes cohort and entities."""
        result = service.persist_entities(
            entities=[{'patient_id': str(uuid4()), 'mrn': 'MRN001', 'given_name': 'Test',
                      'family_name': 'Patient', 'birth_date': '1980-01-01', 'gender': 'male'}],
            entity_type='patient',
            cohort_name='to-delete',
        )
        
        delete_result = service.delete_cohort(
            cohort_id=result.cohort_id,
            confirm=True,
        )
        
        assert delete_result['name'] == 'to-delete'
        
        # Verify it's gone
        cohorts = service.list_cohorts(filter_pattern='to-delete')
        assert len(cohorts) == 0
    
    def test_delete_not_found(self, service):
        """Deleting non-existent cohort raises error."""
        with pytest.raises(ValueError, match="not found"):
            service.delete_cohort(
                cohort_id=str(uuid4()),
                confirm=True,
            )


class TestGetEntitySamples:
    """Tests for get_entity_samples functionality."""
    
    def test_get_samples(self, service):
        """Can get sample entities."""
        entities = [
            {'patient_id': str(uuid4()), 'mrn': f'MRN{i:03d}', 'given_name': f'Patient{i}',
             'family_name': 'Test', 'birth_date': '1980-01-01', 'gender': 'male'}
            for i in range(20)
        ]
        result = service.persist_entities(entities=entities, entity_type='patient')
        
        samples = service.get_entity_samples(
            cohort_id=result.cohort_id,
            entity_type='patient',
            count=5,
        )
        
        assert len(samples) == 5
    
    def test_samples_exclude_internal_fields(self, service):
        """Samples exclude internal fields like cohort_id."""
        entities = [
            {'patient_id': str(uuid4()), 'mrn': 'MRN001', 'given_name': 'Test',
             'family_name': 'Patient', 'birth_date': '1980-01-01', 'gender': 'male'}
        ]
        result = service.persist_entities(entities=entities, entity_type='patient')
        
        samples = service.get_entity_samples(
            cohort_id=result.cohort_id,
            entity_type='patient',
            count=1,
        )
        
        assert 'cohort_id' not in samples[0]
    
    def test_samples_diverse_strategy(self, service):
        """Diverse strategy returns evenly spaced samples."""
        entities = [
            {'patient_id': str(uuid4()), 'mrn': f'MRN{i:03d}', 'given_name': f'Patient{i}',
             'family_name': 'Test', 'birth_date': '1980-01-01', 'gender': 'male'}
            for i in range(100)
        ]
        result = service.persist_entities(entities=entities, entity_type='patient')
        
        samples = service.get_entity_samples(
            cohort_id=result.cohort_id,
            entity_type='patient',
            count=3,
            strategy='diverse',
        )
        
        assert len(samples) == 3
