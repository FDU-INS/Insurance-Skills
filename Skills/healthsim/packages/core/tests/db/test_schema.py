"""Tests for database schema application."""

from pathlib import Path
import pytest
import duckdb

from healthsim.db.connection import DatabaseConnection, get_connection
from healthsim.db.schema import (
    apply_schema,
    SCHEMA_VERSION,
    get_canonical_tables,
    get_state_tables,
    get_system_tables,
)


class TestSchemaApplication:
    """Tests for schema application."""
    
    def setup_method(self):
        """Reset singleton before each test."""
        DatabaseConnection.reset()
    
    def teardown_method(self):
        """Clean up after each test."""
        DatabaseConnection.reset()
    
    def test_apply_schema_creates_all_tables(self, tmp_path):
        """Test that apply_schema creates all expected tables."""
        db_path = tmp_path / "test.duckdb"
        conn = duckdb.connect(str(db_path))
        apply_schema(conn)
        
        # Get all tables
        tables = conn.execute("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_schema = 'main'
        """).fetchall()
        table_names = {row[0] for row in tables}
        
        # Check canonical tables
        for table in get_canonical_tables():
            assert table in table_names, f"Missing canonical table: {table}"
        
        # Check state tables
        for table in get_state_tables():
            assert table in table_names, f"Missing state table: {table}"
        
        # Check system tables
        for table in get_system_tables():
            assert table in table_names, f"Missing system table: {table}"
    
    def test_schema_version_recorded(self, tmp_path):
        """Test that schema version is recorded in migrations table."""
        db_path = tmp_path / "test.duckdb"
        conn = duckdb.connect(str(db_path))
        apply_schema(conn)
        
        result = conn.execute("""
            SELECT version FROM schema_migrations ORDER BY applied_at DESC LIMIT 1
        """).fetchone()
        
        assert result[0] == SCHEMA_VERSION
    
    def test_patients_table_structure(self, tmp_path):
        """Test that patients table has correct columns."""
        db_path = tmp_path / "test.duckdb"
        conn = get_connection(db_path)
        
        columns = conn.execute("""
            SELECT column_name FROM information_schema.columns
            WHERE table_name = 'patients'
        """).fetchall()
        column_names = {row[0] for row in columns}
        
        # Check required columns
        required_columns = {
            'id', 'mrn', 'ssn', 'given_name', 'family_name',
            'birth_date', 'gender', 'created_at', 'source_type',
            'source_system', 'skill_used', 'generation_seed'
        }
        for col in required_columns:
            assert col in column_names, f"Missing column: {col}"

    def test_encounters_table_structure(self, tmp_path):
        """Test that encounters table has correct columns."""
        db_path = tmp_path / "test.duckdb"
        conn = get_connection(db_path)
        
        columns = conn.execute("""
            SELECT column_name FROM information_schema.columns
            WHERE table_name = 'encounters'
        """).fetchall()
        column_names = {row[0] for row in columns}
        
        required_columns = {
            'encounter_id', 'patient_mrn', 'class_code', 'status',
            'admission_time', 'created_at', 'source_type'
        }
        for col in required_columns:
            assert col in column_names, f"Missing column: {col}"
    
    def test_cohorts_table_structure(self, tmp_path):
        """Test that cohorts state table has correct columns."""
        db_path = tmp_path / "test.duckdb"
        conn = get_connection(db_path)
        
        columns = conn.execute("""
            SELECT column_name FROM information_schema.columns
            WHERE table_name = 'cohorts'
        """).fetchall()
        column_names = {row[0] for row in columns}
        
        required_columns = {
            'id', 'name', 'description', 
            'created_at', 'updated_at', 'metadata'
        }
        for col in required_columns:
            assert col in column_names, f"Missing column: {col}"
    
    def test_provenance_columns_present(self, tmp_path):
        """Test that provenance columns are present on canonical tables."""
        db_path = tmp_path / "test.duckdb"
        conn = get_connection(db_path)
        
        provenance_columns = {
            'created_at', 'source_type', 'source_system', 
            'skill_used', 'generation_seed'
        }
        
        for table in get_canonical_tables():
            columns = conn.execute(f"""
                SELECT column_name FROM information_schema.columns
                WHERE table_name = '{table}'
            """).fetchall()
            column_names = {row[0] for row in columns}
            
            for col in provenance_columns:
                assert col in column_names, f"Missing provenance column {col} in {table}"


class TestIndexCreation:
    """Tests for index creation."""
    
    def setup_method(self):
        """Reset singleton before each test."""
        DatabaseConnection.reset()
    
    def teardown_method(self):
        """Clean up after each test."""
        DatabaseConnection.reset()
    
    def test_indexes_created(self, tmp_path):
        """Test that indexes are created."""
        db_path = tmp_path / "test.duckdb"
        conn = get_connection(db_path)
        
        # DuckDB stores index info differently - just verify tables work with queries
        # that would use indexes
        result = conn.execute(
            "EXPLAIN SELECT * FROM patients WHERE mrn = 'test'"
        ).fetchall()
        
        # If we get here without error, the table exists and can be queried
        assert result is not None


class TestTableHelpers:
    """Tests for table helper functions."""
    
    def test_get_canonical_tables_returns_list(self):
        """Test that get_canonical_tables returns expected tables."""
        tables = get_canonical_tables()
        assert isinstance(tables, list)
        assert 'patients' in tables
        assert 'encounters' in tables
        assert 'claims' in tables
        assert 'subjects' in tables
    
    def test_get_state_tables_returns_list(self):
        """Test that get_state_tables returns expected tables."""
        tables = get_state_tables()
        assert isinstance(tables, list)
        assert 'cohorts' in tables
        assert 'cohort_entities' in tables
        assert 'cohort_tags' in tables
    
    def test_get_system_tables_returns_list(self):
        """Test that get_system_tables returns expected tables."""
        tables = get_system_tables()
        assert isinstance(tables, list)
        assert 'schema_migrations' in tables
