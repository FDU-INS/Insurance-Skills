#!/usr/bin/env python3
"""
Test that add_entities correctly writes to BOTH:
1. cohort_entities (JSON storage)
2. canonical tables (typed columns)

This is an integration test that directly tests the MCP server's
insert_into_canonical_table function.
"""

import sys
from pathlib import Path
import pytest
import json

# Setup paths
WORKSPACE_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(WORKSPACE_ROOT / "packages" / "core" / "src"))
sys.path.insert(0, str(WORKSPACE_ROOT / "packages" / "mcp-server"))

import duckdb
from healthsim.state.serializers import get_serializer, get_table_info


@pytest.fixture
def test_db(tmp_path):
    """Create a test database with proper schema matching production."""
    db_path = tmp_path / "test.duckdb"
    conn = duckdb.connect(str(db_path))
    
    # Create schema matching production healthsim.duckdb
    conn.execute("""
        CREATE TABLE patients (
            id VARCHAR PRIMARY KEY,
            mrn VARCHAR,
            ssn VARCHAR,
            given_name VARCHAR,
            middle_name VARCHAR,
            family_name VARCHAR,
            suffix VARCHAR,
            prefix VARCHAR,
            birth_date DATE,
            gender VARCHAR,
            race VARCHAR,
            ethnicity VARCHAR,
            language VARCHAR,
            street_address VARCHAR,
            street_address_2 VARCHAR,
            city VARCHAR,
            state VARCHAR,
            postal_code VARCHAR,
            country VARCHAR,
            phone VARCHAR,
            phone_mobile VARCHAR,
            email VARCHAR,
            deceased BOOLEAN,
            death_date DATE,
            created_at TIMESTAMP,
            source_type VARCHAR,
            source_system VARCHAR,
            skill_used VARCHAR,
            generation_seed INTEGER,
            cohort_id VARCHAR
        )
    """)
    
    # Members table - matches production schema
    conn.execute("""
        CREATE TABLE members (
            id VARCHAR PRIMARY KEY,
            member_id VARCHAR,
            subscriber_id VARCHAR,
            relationship_code VARCHAR,
            ssn VARCHAR,
            given_name VARCHAR,
            middle_name VARCHAR,
            family_name VARCHAR,
            birth_date DATE,
            gender VARCHAR,
            street_address VARCHAR,
            city VARCHAR,
            state VARCHAR,
            postal_code VARCHAR,
            phone VARCHAR,
            email VARCHAR,
            group_id VARCHAR,
            plan_code VARCHAR,
            coverage_start DATE,
            coverage_end DATE,
            pcp_npi VARCHAR,
            created_at TIMESTAMP,
            source_type VARCHAR,
            source_system VARCHAR,
            skill_used VARCHAR,
            generation_seed INTEGER,
            cohort_id VARCHAR
        )
    """)
    
    yield conn
    conn.close()


# Import the function we're testing
from healthsim_mcp import insert_into_canonical_table


class TestCanonicalInsert:
    """Test the insert_into_canonical_table function."""
    
    def test_patient_insert(self, test_db):
        """Test that patient entities insert correctly into canonical table."""
        cohort_id = "test-cohort-001"
        patient = {
            "patient_id": "PT-001",
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": "1985-06-15",
            "gender": "M",
            "city": "San Diego",
            "state": "CA",
            "zip_code": "92101"
        }
        
        result = insert_into_canonical_table(
            test_db,
            cohort_id,
            "patients",
            patient
        )
        
        success, error = result
        assert success is True, f"Insert failed: {error}"
        
        # Verify the data
        row = test_db.execute(
            "SELECT id, given_name, family_name, city, cohort_id FROM patients WHERE id = ?",
            ["PT-001"]
        ).fetchone()
        
        assert row is not None
        assert row[0] == "PT-001"
        assert row[1] == "John"
        assert row[2] == "Doe"
        assert row[3] == "San Diego"
        assert row[4] == cohort_id
    
    def test_member_insert(self, test_db):
        """Test that member entities insert correctly into canonical table."""
        cohort_id = "test-cohort-001"
        member = {
            "member_id": "MBR-001",
            "patient_id": "PT-001",
            "plan_code": "BSC-PPO",
            "group_id": "GRP-001",
            "coverage_start": "2024-01-01",
        }
        
        result = insert_into_canonical_table(
            test_db,
            cohort_id,
            "members",
            member
        )
        
        success, error = result
        assert success is True, f"Insert failed: {error}"
        
        # Verify the data - use columns that match the serializer output
        row = test_db.execute(
            "SELECT member_id, plan_code, group_id, cohort_id FROM members WHERE member_id = ?",
            ["MBR-001"]
        ).fetchone()
        
        assert row is not None
        assert row[0] == "MBR-001"
        assert row[1] == "BSC-PPO"
        assert row[2] == "GRP-001"
        assert row[3] == cohort_id
    
    def test_upsert_updates_existing(self, test_db):
        """Test that re-inserting same ID updates the record."""
        cohort_id = "test-cohort-001"
        
        # First insert
        patient1 = {
            "patient_id": "PT-002",
            "first_name": "Jane",
            "last_name": "Smith",
            "city": "Los Angeles"
        }
        insert_into_canonical_table(test_db, cohort_id, "patients", patient1)
        
        # Update via upsert
        patient2 = {
            "patient_id": "PT-002",
            "first_name": "Jane",
            "last_name": "Smith-Jones",  # Changed
            "city": "San Francisco"       # Changed
        }
        insert_into_canonical_table(test_db, cohort_id, "patients", patient2)
        
        # Should only be one record
        count = test_db.execute("SELECT COUNT(*) FROM patients WHERE id = ?", ["PT-002"]).fetchone()[0]
        assert count == 1
        
        # Should have updated values
        row = test_db.execute(
            "SELECT family_name, city FROM patients WHERE id = ?",
            ["PT-002"]
        ).fetchone()
        assert row[0] == "Smith-Jones"
        assert row[1] == "San Francisco"
    
    def test_no_serializer_returns_false(self, test_db):
        """Test that unknown entity types return (False, error_msg) gracefully."""
        success, error = insert_into_canonical_table(
            test_db,
            "test-cohort",
            "unknown_type",
            {"id": "123"}
        )
        assert success is False
        assert "No serializer" in error


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
