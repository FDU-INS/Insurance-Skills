"""Tests for cohort summary generation."""

import pytest
from datetime import datetime
import tempfile
from pathlib import Path
from uuid import uuid4

from healthsim.db import DatabaseConnection
from healthsim.state.summary import (
    CohortSummary,
    generate_summary,
    get_cohort_by_name,
)


@pytest.fixture
def test_db():
    """Create a temporary test database with schema applied."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test_summary.duckdb"
        db_conn = DatabaseConnection(db_path)
        conn = db_conn.connect()
        yield conn
        db_conn.close()


@pytest.fixture
def cohort_with_data(test_db):
    """Create a cohort with sample data."""
    cohort_id = str(uuid4())
    now = datetime.utcnow()
    
    # Create cohort
    test_db.execute("""
        INSERT INTO cohorts (id, name, description, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?)
    """, [cohort_id, 'test-cohort', 'A test cohort', now, now])
    
    # Add tags
    test_db.execute("""
        INSERT INTO cohort_tags (id, cohort_id, tag) VALUES (nextval('cohort_tags_seq'), ?, ?)
    """, [cohort_id, 'diabetes'])
    test_db.execute("""
        INSERT INTO cohort_tags (id, cohort_id, tag) VALUES (nextval('cohort_tags_seq'), ?, ?)
    """, [cohort_id, 'test'])
    
    # Add patients (using correct column names from schema)
    for i in range(5):
        test_db.execute("""
            INSERT INTO patients (id, cohort_id, mrn, given_name, family_name, 
                                  birth_date, gender, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, [
            str(uuid4()), cohort_id, f'MRN{i:03d}', f'Patient{i}', 'Test',
            f'19{50 + i * 5}-01-01', 'male' if i % 2 == 0 else 'female', now
        ])
    
    return cohort_id


class TestCohortSummary:
    """Tests for CohortSummary dataclass."""
    
    def test_to_dict(self):
        """Can convert summary to dict."""
        summary = CohortSummary(
            cohort_id='abc123',
            name='test-cohort',
            entity_counts={'patients': 10, 'encounters': 25},
            tags=['diabetes'],
        )
        
        d = summary.to_dict()
        
        assert d['cohort_id'] == 'abc123'
        assert d['name'] == 'test-cohort'
        assert d['entity_counts']['patients'] == 10
        assert 'diabetes' in d['tags']
    
    def test_to_json(self):
        """Can convert summary to JSON string."""
        summary = CohortSummary(
            cohort_id='abc123',
            name='test-cohort',
        )
        
        json_str = summary.to_json()
        
        assert 'abc123' in json_str
        assert 'test-cohort' in json_str
    
    def test_from_dict(self):
        """Can create summary from dict."""
        data = {
            'cohort_id': 'abc123',
            'name': 'test-cohort',
            'entity_counts': {'patients': 5},
            'tags': ['test'],
        }
        
        summary = CohortSummary.from_dict(data)
        
        assert summary.cohort_id == 'abc123'
        assert summary.name == 'test-cohort'
        assert summary.entity_counts['patients'] == 5
    
    def test_total_entities(self):
        """Can calculate total entity count."""
        summary = CohortSummary(
            cohort_id='abc123',
            name='test',
            entity_counts={'patients': 10, 'encounters': 20, 'claims': 15},
        )
        
        assert summary.total_entities() == 45
    
    def test_token_estimate(self):
        """Can estimate token count."""
        summary = CohortSummary(
            cohort_id='abc123',
            name='test-cohort',
            entity_counts={'patients': 10},
        )
        
        tokens = summary.token_estimate()
        
        # Should be a reasonable positive number
        assert tokens > 0
        assert tokens < 1000  # Simple summary should be small


class TestGenerateSummary:
    """Tests for generate_summary function."""
    
    def test_generate_basic_summary(self, test_db, cohort_with_data):
        """Can generate summary for cohort with data."""
        summary = generate_summary(
            cohort_id=cohort_with_data,
            include_samples=False,
            connection=test_db
        )
        
        assert summary.cohort_id == cohort_with_data
        assert summary.name == 'test-cohort'
        assert summary.entity_counts.get('patients', 0) == 5
    
    def test_generate_with_samples(self, test_db, cohort_with_data):
        """Summary includes samples when requested."""
        summary = generate_summary(
            cohort_id=cohort_with_data,
            include_samples=True,
            samples_per_type=3,
            connection=test_db
        )
        
        assert 'patients' in summary.samples
        assert len(summary.samples['patients']) <= 3
    
    def test_generate_includes_tags(self, test_db, cohort_with_data):
        """Summary includes cohort tags."""
        summary = generate_summary(
            cohort_id=cohort_with_data,
            connection=test_db
        )
        
        assert 'diabetes' in summary.tags
        assert 'test' in summary.tags
    
    def test_generate_not_found(self, test_db):
        """Raises error for non-existent cohort."""
        with pytest.raises(ValueError, match="not found"):
            generate_summary(
                cohort_id=str(uuid4()),
                connection=test_db
            )


class TestGetCohortByName:
    """Tests for get_cohort_by_name function."""
    
    def test_exact_match(self, test_db, cohort_with_data):
        """Can find cohort by exact name."""
        result = get_cohort_by_name('test-cohort', test_db)
        
        assert result == cohort_with_data
    
    def test_case_insensitive(self, test_db, cohort_with_data):
        """Can find cohort with case-insensitive match."""
        result = get_cohort_by_name('TEST-COHORT', test_db)
        
        assert result == cohort_with_data
    
    def test_partial_match(self, test_db, cohort_with_data):
        """Can find cohort by partial name."""
        result = get_cohort_by_name('test', test_db)
        
        assert result == cohort_with_data
    
    def test_not_found(self, test_db):
        """Returns None for non-existent cohort."""
        result = get_cohort_by_name('nonexistent', test_db)
        
        assert result is None
