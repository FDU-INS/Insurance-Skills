"""
Test add_entities canonical table insertion end-to-end.

Uses a temporary test database to avoid locking issues.
"""

import sys
from pathlib import Path
import json
import uuid
import tempfile
import shutil

# Add paths
WORKSPACE_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(WORKSPACE_ROOT / "packages" / "core" / "src"))
sys.path.insert(0, str(WORKSPACE_ROOT / "packages" / "mcp-server"))

import duckdb

# Schema for test tables
PATIENTS_SCHEMA = """
CREATE TABLE IF NOT EXISTS patients (
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
);
"""

MEMBERS_SCHEMA = """
CREATE TABLE IF NOT EXISTS members (
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
);
"""


def test_canonical_insert_end_to_end():
    """Test that insert_into_canonical_table works correctly."""
    
    # Create a temp directory for test DB
    temp_dir = tempfile.mkdtemp()
    test_db_path = Path(temp_dir) / "test.duckdb"
    
    test_cohort_id = f"test-canonical-{uuid.uuid4().hex[:8]}"
    test_patient_id = f"PAT-TEST-{uuid.uuid4().hex[:8]}"
    test_member_id = f"MBR-TEST-{uuid.uuid4().hex[:8]}"
    
    print(f"Test DB: {test_db_path}")
    print(f"Test cohort ID: {test_cohort_id}")
    
    conn = duckdb.connect(str(test_db_path), read_only=False)
    
    try:
        # Create test tables
        conn.execute(PATIENTS_SCHEMA)
        conn.execute(MEMBERS_SCHEMA)
        
        # Create test entities
        test_patient = {
            "patient_id": test_patient_id,
            "mrn": "MRN-TEST-001",
            "given_name": "Test",
            "family_name": "Patient",
            "birth_date": "1985-06-15",
            "gender": "female",
            "address": {
                "line1": "123 Test St",
                "city": "San Diego",
                "state": "CA",
                "postalCode": "92101"
            }
        }
        
        test_member = {
            "member_id": test_member_id,
            "subscriber_id": "SUB-TEST-001",
            "given_name": "Test",
            "family_name": "Member",
            "birth_date": "1985-06-15",
            "gender": "F",
            "plan_code": "TEST-PLAN",
            "coverage_start": "2024-01-01",
            "relationship_code": "18"
        }
        
        # Import and call the insert function directly
        from healthsim_mcp import insert_into_canonical_table
        
        print("\n=== Testing Patient Canonical Insert ===")
        patient_result = insert_into_canonical_table(conn, test_cohort_id, 'patients', test_patient)
        print(f"Patient insert result: {patient_result}")
        
        print("\n=== Testing Member Canonical Insert ===")
        member_result = insert_into_canonical_table(conn, test_cohort_id, 'members', test_member)
        print(f"Member insert result: {member_result}")
        
        # Verify data in canonical tables
        print("\n=== Verifying Canonical Tables ===")

        patient_check = conn.execute(
            "SELECT id, given_name, family_name, city, cohort_id FROM patients WHERE cohort_id = ?",
            [test_cohort_id]
        ).fetchall()
        print(f"Patients in canonical table: {patient_check}")

        member_check = conn.execute(
            "SELECT id, member_id, given_name, family_name, plan_code, cohort_id FROM members WHERE cohort_id = ?",
            [test_cohort_id]
        ).fetchall()
        print(f"Members in canonical table: {member_check}")
        
        # Assertions
        assert len(patient_check) == 1, f"Expected 1 patient, got {len(patient_check)}"
        assert patient_check[0][1] == "Test", f"Expected given_name 'Test', got {patient_check[0][1]}"
        assert patient_check[0][3] == "San Diego", f"Expected city 'San Diego', got {patient_check[0][3]}"
        
        assert len(member_check) == 1, f"Expected 1 member, got {len(member_check)}"
        assert member_check[0][2] == "Test", f"Expected given_name 'Test', got {member_check[0][2]}"
        assert member_check[0][4] == "TEST-PLAN", f"Expected plan_code 'TEST-PLAN', got {member_check[0][4]}"
        
        print("\n✅ All assertions passed!")

    finally:
        conn.close()
        shutil.rmtree(temp_dir)


if __name__ == "__main__":
    test_canonical_insert_end_to_end()
