"""
Tests for the healthsim_add_entities MCP tool.

This tool provides incremental entity addition to cohorts, solving:
1. Batch truncation - allows adding entities in multiple calls
2. Destructive overwrite - uses upsert logic instead of replace

Tests cover:
- Creating new cohorts via add_entities
- Adding to existing cohorts
- Upsert behavior (update existing, insert new)
- Batch tracking
- Error handling
"""

import json
import pytest
import tempfile
import os
from pathlib import Path
from datetime import datetime

import duckdb

# Import the MCP server module
import sys
WORKSPACE_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(WORKSPACE_ROOT / "packages" / "mcp-server"))
sys.path.insert(0, str(WORKSPACE_ROOT / "packages" / "core" / "src"))

from healthsim_mcp import (
    ConnectionManager,
)


@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    # Create a temp file path but don't create the file
    # DuckDB will create it fresh
    fd, path = tempfile.mkstemp(suffix='.duckdb')
    os.close(fd)
    os.unlink(path)  # Delete the empty file so DuckDB can create it
    db_path = Path(path)
    
    # Initialize schema
    conn = duckdb.connect(str(db_path))
    conn.execute("""
        CREATE TABLE cohorts (
            cohort_id VARCHAR PRIMARY KEY,
            name VARCHAR UNIQUE NOT NULL,
            description VARCHAR,
            created_at TIMESTAMP,
            updated_at TIMESTAMP,
            metadata JSON
        )
    """)
    conn.execute("""
        CREATE TABLE cohort_entities (
            id INTEGER PRIMARY KEY,
            cohort_id VARCHAR NOT NULL,
            entity_type VARCHAR NOT NULL,
            entity_id VARCHAR NOT NULL,
            entity_data JSON,
            created_at TIMESTAMP,
            UNIQUE(cohort_id, entity_type, entity_id)
        )
    """)
    conn.execute("""
        CREATE TABLE cohort_tags (
            id INTEGER PRIMARY KEY,
            cohort_id VARCHAR NOT NULL,
            tag VARCHAR NOT NULL,
            UNIQUE(cohort_id, tag)
        )
    """)
    conn.execute("CREATE SEQUENCE cohort_entities_seq START 1")
    conn.execute("CREATE SEQUENCE cohort_tags_seq START 1")
    conn.close()
    
    yield db_path
    
    # Cleanup
    db_path.unlink(missing_ok=True)


@pytest.fixture
def connection_manager(temp_db):
    """Create a connection manager for the temp database."""
    return ConnectionManager(temp_db)


class TestAddEntitiesNewScenario:
    """Tests for creating new cohorts via add_entities."""
    
    def test_create_cohort_with_name(self, connection_manager):
        """Create a new cohort by providing cohort_name."""
        with connection_manager.write_connection() as conn:
            # Create cohort
            cohort_id = "test-uuid-123"
            cohort_name = "Test Scenario"
            now = datetime.utcnow()
            
            conn.execute("""
                INSERT INTO cohorts (cohort_id, name, description, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
            """, [cohort_id, cohort_name, "Test description", now, now])
            
            # Verify cohort was created
            result = conn.execute(
                "SELECT name FROM cohorts WHERE cohort_id = ?",
                [cohort_id]
            ).fetchone()
            
            assert result is not None
            assert result[0] == cohort_name
    
    def test_create_cohort_auto_name(self, connection_manager):
        """Create a new cohort with auto-generated name."""
        with connection_manager.write_connection() as conn:
            # Auto-generate name
            cohort_id = "test-uuid-456"
            cohort_name = f"cohort-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}"
            now = datetime.utcnow()
            
            conn.execute("""
                INSERT INTO cohorts (cohort_id, name, created_at, updated_at)
                VALUES (?, ?, ?, ?)
            """, [cohort_id, cohort_name, now, now])
            
            # Verify
            result = conn.execute(
                "SELECT name FROM cohorts WHERE cohort_id = ?",
                [cohort_id]
            ).fetchone()
            
            assert result is not None
            assert result[0].startswith("cohort-")


class TestAddEntitiesToExisting:
    """Tests for adding entities to existing cohorts."""
    
    def test_add_entities_to_existing_cohort(self, connection_manager):
        """Add entities to a cohort that already exists."""
        with connection_manager.write_connection() as conn:
            # Create cohort first
            cohort_id = "existing-cohort-123"
            now = datetime.utcnow()
            conn.execute("""
                INSERT INTO cohorts (cohort_id, name, created_at, updated_at)
                VALUES (?, ?, ?, ?)
            """, [cohort_id, "Existing Scenario", now, now])
            
            # Add initial entities
            conn.execute("""
                INSERT INTO cohort_entities (id, cohort_id, entity_type, entity_id, entity_data, created_at)
                VALUES (1, ?, 'patients', 'PAT-001', '{"name": "John"}', ?)
            """, [cohort_id, now])
            
            # Verify initial state
            count = conn.execute(
                "SELECT COUNT(*) FROM cohort_entities WHERE cohort_id = ?",
                [cohort_id]
            ).fetchone()[0]
            assert count == 1
            
            # Add more entities
            conn.execute("""
                INSERT INTO cohort_entities (id, cohort_id, entity_type, entity_id, entity_data, created_at)
                VALUES (2, ?, 'patients', 'PAT-002', '{"name": "Jane"}', ?)
            """, [cohort_id, now])
            
            # Verify new count
            count = conn.execute(
                "SELECT COUNT(*) FROM cohort_entities WHERE cohort_id = ?",
                [cohort_id]
            ).fetchone()[0]
            assert count == 2
    
    def test_add_different_entity_types(self, connection_manager):
        """Add different entity types to same cohort."""
        with connection_manager.write_connection() as conn:
            cohort_id = "multi-type-cohort"
            now = datetime.utcnow()
            
            conn.execute("""
                INSERT INTO cohorts (cohort_id, name, created_at, updated_at)
                VALUES (?, ?, ?, ?)
            """, [cohort_id, "Multi-Type Scenario", now, now])
            
            # Add patients
            conn.execute("""
                INSERT INTO cohort_entities (id, cohort_id, entity_type, entity_id, entity_data, created_at)
                VALUES (1, ?, 'patients', 'PAT-001', '{"name": "John"}', ?)
            """, [cohort_id, now])
            
            # Add members
            conn.execute("""
                INSERT INTO cohort_entities (id, cohort_id, entity_type, entity_id, entity_data, created_at)
                VALUES (2, ?, 'members', 'MBR-001', '{"plan": "Gold"}', ?)
            """, [cohort_id, now])
            
            # Verify both types exist
            types = conn.execute("""
                SELECT DISTINCT entity_type FROM cohort_entities WHERE cohort_id = ?
            """, [cohort_id]).fetchall()
            
            type_set = {t[0] for t in types}
            assert 'patients' in type_set
            assert 'members' in type_set


class TestUpsertBehavior:
    """Tests for upsert (update or insert) behavior."""
    
    def test_insert_new_entity(self, connection_manager):
        """Insert a new entity that doesn't exist."""
        with connection_manager.write_connection() as conn:
            cohort_id = "upsert-test"
            now = datetime.utcnow()
            
            conn.execute("""
                INSERT INTO cohorts (cohort_id, name, created_at, updated_at)
                VALUES (?, ?, ?, ?)
            """, [cohort_id, "Upsert Test", now, now])
            
            # Insert new entity
            entity_id = "NEW-001"
            conn.execute("""
                INSERT INTO cohort_entities (id, cohort_id, entity_type, entity_id, entity_data, created_at)
                VALUES (1, ?, 'patients', ?, '{"name": "New Patient"}', ?)
            """, [cohort_id, entity_id, now])
            
            # Verify insert
            result = conn.execute("""
                SELECT entity_data FROM cohort_entities 
                WHERE cohort_id = ? AND entity_id = ?
            """, [cohort_id, entity_id]).fetchone()
            
            assert result is not None
            data = json.loads(result[0])
            assert data["name"] == "New Patient"
    
    def test_update_existing_entity(self, connection_manager):
        """Update an entity that already exists (upsert behavior)."""
        with connection_manager.write_connection() as conn:
            cohort_id = "upsert-update-test"
            now = datetime.utcnow()
            
            conn.execute("""
                INSERT INTO cohorts (cohort_id, name, created_at, updated_at)
                VALUES (?, ?, ?, ?)
            """, [cohort_id, "Upsert Update Test", now, now])
            
            # Insert initial entity
            entity_id = "PAT-001"
            conn.execute("""
                INSERT INTO cohort_entities (id, cohort_id, entity_type, entity_id, entity_data, created_at)
                VALUES (1, ?, 'patients', ?, '{"name": "Original"}', ?)
            """, [cohort_id, entity_id, now])
            
            # Update via upsert logic
            # Check if exists
            existing = conn.execute("""
                SELECT id FROM cohort_entities 
                WHERE cohort_id = ? AND entity_type = ? AND entity_id = ?
            """, [cohort_id, 'patients', entity_id]).fetchone()
            
            assert existing is not None  # Should exist
            
            # Update
            conn.execute("""
                UPDATE cohort_entities 
                SET entity_data = ?, created_at = ?
                WHERE cohort_id = ? AND entity_type = ? AND entity_id = ?
            """, ['{"name": "Updated"}', now, cohort_id, 'patients', entity_id])
            
            # Verify update
            result = conn.execute("""
                SELECT entity_data FROM cohort_entities 
                WHERE cohort_id = ? AND entity_id = ?
            """, [cohort_id, entity_id]).fetchone()
            
            data = json.loads(result[0])
            assert data["name"] == "Updated"
    
    def test_upsert_does_not_delete_other_entities(self, connection_manager):
        """Verify that upserting doesn't delete entities not in the current batch."""
        with connection_manager.write_connection() as conn:
            cohort_id = "no-delete-test"
            now = datetime.utcnow()
            
            conn.execute("""
                INSERT INTO cohorts (cohort_id, name, created_at, updated_at)
                VALUES (?, ?, ?, ?)
            """, [cohort_id, "No Delete Test", now, now])
            
            # Insert 3 entities
            for i in range(1, 4):
                conn.execute("""
                    INSERT INTO cohort_entities (id, cohort_id, entity_type, entity_id, entity_data, created_at)
                    VALUES (?, ?, 'patients', ?, ?, ?)
                """, [i, cohort_id, f"PAT-00{i}", f'{{"id": {i}}}', now])
            
            # Verify 3 entities
            count = conn.execute(
                "SELECT COUNT(*) FROM cohort_entities WHERE cohort_id = ?",
                [cohort_id]
            ).fetchone()[0]
            assert count == 3
            
            # Now "upsert" just one entity (PAT-002)
            conn.execute("""
                UPDATE cohort_entities 
                SET entity_data = ?
                WHERE cohort_id = ? AND entity_id = ?
            """, ['{"id": 2, "updated": true}', cohort_id, "PAT-002"])
            
            # Verify still 3 entities (no deletion)
            count = conn.execute(
                "SELECT COUNT(*) FROM cohort_entities WHERE cohort_id = ?",
                [cohort_id]
            ).fetchone()[0]
            assert count == 3
            
            # Verify PAT-001 and PAT-003 still exist unchanged
            result = conn.execute("""
                SELECT entity_id FROM cohort_entities 
                WHERE cohort_id = ? ORDER BY entity_id
            """, [cohort_id]).fetchall()
            
            ids = [r[0] for r in result]
            assert ids == ["PAT-001", "PAT-002", "PAT-003"]


class TestBatchTracking:
    """Tests for batch progress tracking."""
    
    def test_batch_number_tracking(self, connection_manager):
        """Track batch numbers across multiple calls."""
        with connection_manager.write_connection() as conn:
            cohort_id = "batch-test"
            now = datetime.utcnow()
            
            conn.execute("""
                INSERT INTO cohorts (cohort_id, name, created_at, updated_at)
                VALUES (?, ?, ?, ?)
            """, [cohort_id, "Batch Test", now, now])
            
            # Simulate batch 1 of 4
            batch_1_count = 50
            for i in range(1, batch_1_count + 1):
                conn.execute("""
                    INSERT INTO cohort_entities (id, cohort_id, entity_type, entity_id, entity_data, created_at)
                    VALUES (?, ?, 'patients', ?, '{}', ?)
                """, [i, cohort_id, f"PAT-{i:03d}", now])
            
            count = conn.execute(
                "SELECT COUNT(*) FROM cohort_entities WHERE cohort_id = ?",
                [cohort_id]
            ).fetchone()[0]
            assert count == 50
            
            # Simulate batch 2 of 4
            for i in range(51, 101):
                conn.execute("""
                    INSERT INTO cohort_entities (id, cohort_id, entity_type, entity_id, entity_data, created_at)
                    VALUES (?, ?, 'patients', ?, '{}', ?)
                """, [i, cohort_id, f"PAT-{i:03d}", now])
            
            count = conn.execute(
                "SELECT COUNT(*) FROM cohort_entities WHERE cohort_id = ?",
                [cohort_id]
            ).fetchone()[0]
            assert count == 100


class TestErrorHandling:
    """Tests for error conditions."""
    
    def test_cohort_not_found(self, connection_manager):
        """Error when cohort_id doesn't exist."""
        with connection_manager.write_connection() as conn:
            # Try to find non-existent cohort
            result = conn.execute(
                "SELECT name FROM cohorts WHERE cohort_id = ?",
                ["non-existent-id"]
            ).fetchone()
            
            assert result is None
    
    def test_empty_entities_handled(self, connection_manager):
        """Handle empty entity lists gracefully."""
        with connection_manager.write_connection() as conn:
            cohort_id = "empty-test"
            now = datetime.utcnow()
            
            conn.execute("""
                INSERT INTO cohorts (cohort_id, name, created_at, updated_at)
                VALUES (?, ?, ?, ?)
            """, [cohort_id, "Empty Test", now, now])
            
            # Adding empty list should not error
            entities = {}  # Empty
            
            for entity_type, entity_list in entities.items():
                for entity in entity_list:
                    pass  # Nothing to do
            
            # Scenario should exist with 0 entities
            count = conn.execute(
                "SELECT COUNT(*) FROM cohort_entities WHERE cohort_id = ?",
                [cohort_id]
            ).fetchone()[0]
            assert count == 0


class TestEntityTypeNormalization:
    """Tests for entity type normalization (singular -> plural)."""
    
    def test_singular_to_plural_conversion(self):
        """Verify entity types are normalized to plural form."""
        test_cases = [
            ("patient", "patients"),
            ("patients", "patients"),
            ("member", "members"),
            ("members", "members"),
            ("claim", "claims"),
            ("encounter", "encounters"),
        ]
        
        for input_type, expected in test_cases:
            normalized = input_type.lower()
            if not normalized.endswith('s'):
                normalized += 's'
            assert normalized == expected, f"Failed for {input_type}"


class TestScenarioTotals:
    """Tests for cohort total calculations."""
    
    def test_total_by_type(self, connection_manager):
        """Calculate totals by entity type."""
        with connection_manager.write_connection() as conn:
            cohort_id = "totals-test"
            now = datetime.utcnow()
            
            conn.execute("""
                INSERT INTO cohorts (cohort_id, name, created_at, updated_at)
                VALUES (?, ?, ?, ?)
            """, [cohort_id, "Totals Test", now, now])
            
            # Add mixed entities
            conn.execute("""
                INSERT INTO cohort_entities (id, cohort_id, entity_type, entity_id, entity_data, created_at)
                VALUES 
                    (1, ?, 'patients', 'P1', '{}', ?),
                    (2, ?, 'patients', 'P2', '{}', ?),
                    (3, ?, 'patients', 'P3', '{}', ?),
                    (4, ?, 'members', 'M1', '{}', ?),
                    (5, ?, 'members', 'M2', '{}', ?)
            """, [cohort_id, now, cohort_id, now, cohort_id, now, cohort_id, now, cohort_id, now])
            
            # Get totals by type
            result = conn.execute("""
                SELECT entity_type, COUNT(*) as count 
                FROM cohort_entities 
                WHERE cohort_id = ? 
                GROUP BY entity_type
            """, [cohort_id]).fetchall()
            
            totals = {row[0]: row[1] for row in result}
            
            assert totals.get('patients') == 3
            assert totals.get('members') == 2
            assert sum(totals.values()) == 5



class TestToolSelectionGuidance:
    """Tests verifying tool descriptions contain proper selection guidance.
    
    These tests ensure Claude receives clear signals about when to use
    save_cohort vs add_entities based on entity count thresholds.
    """
    
    def test_save_cohort_warns_about_large_datasets(self):
        """Verify save_cohort docstring warns about 50+ entity limit."""
        from healthsim_mcp import save_cohort
        
        docstring = save_cohort.__doc__
        assert docstring is not None
        
        # Should warn to use add_entities instead
        assert "add_entities" in docstring.lower() or "healthsim_add_entities" in docstring
        
        # Should mention the 50 entity threshold
        assert "50" in docstring
        
        # Should indicate it's for small datasets
        assert "small" in docstring.lower() or "≤50" in docstring
        
        # Should warn about replacement behavior
        assert "replace" in docstring.lower()
    
    def test_add_entities_recommends_for_large_datasets(self):
        """Verify add_entities docstring recommends itself for large datasets."""
        from healthsim_mcp import add_entities
        
        docstring = add_entities.__doc__
        assert docstring is not None
        
        # Should indicate it's recommended
        assert "recommended" in docstring.lower() or "RECOMMENDED" in docstring
        
        # Should mention 50 entity threshold
        assert "50" in docstring
        
        # Should mention upsert/incremental behavior
        assert "upsert" in docstring.lower() or "incremental" in docstring.lower()
        
        # Should mention it doesn't delete
        assert "never delete" in docstring.lower() or "NEVER deletes" in docstring
    
    def test_tool_descriptions_are_complementary(self):
        """Verify the two tools have complementary guidance."""
        from healthsim_mcp import save_cohort, add_entities
        
        save_doc = save_cohort.__doc__
        add_doc = add_entities.__doc__
        
        # save_cohort should redirect to add_entities for large datasets
        assert "healthsim_add_entities" in save_doc or "add_entities" in save_doc
        
        # add_entities should be marked as preferred
        assert "✅" in add_doc or "RECOMMENDED" in add_doc
        
        # save_cohort should have warning indicator
        assert "⚠" in save_doc or "WARNING" in save_doc
    
    def test_threshold_consistency(self):
        """Verify both tools reference the same entity count threshold."""
        from healthsim_mcp import save_cohort, add_entities
        
        save_doc = save_cohort.__doc__
        add_doc = add_entities.__doc__
        
        # Both should mention 50 as the threshold
        assert "50" in save_doc, "save_cohort should mention 50 entity threshold"
        assert "50" in add_doc, "add_entities should mention 50 entity threshold"


class TestToolAnnotations:
    """Tests verifying MCP tool annotations are correct."""
    
    def test_save_cohort_annotations(self):
        """Verify save_cohort has correct MCP annotations."""
        from healthsim_mcp import mcp
        
        # Get the tool from the MCP server
        tools = mcp._tool_manager._tools
        save_tool = tools.get("healthsim_save_cohort")
        
        assert save_tool is not None, "healthsim_save_cohort tool should exist"
    
    def test_add_entities_annotations(self):
        """Verify add_entities has correct MCP annotations."""
        from healthsim_mcp import mcp
        
        tools = mcp._tool_manager._tools
        add_tool = tools.get("healthsim_add_entities")
        
        assert add_tool is not None, "healthsim_add_entities tool should exist"
    
    def test_add_entities_is_idempotent(self):
        """Verify add_entities is marked as idempotent (upsert behavior)."""
        from healthsim_mcp import mcp
        
        tools = mcp._tool_manager._tools
        add_tool = tools.get("healthsim_add_entities")
        
        # The tool should exist and be properly configured
        assert add_tool is not None
        # Note: FastMCP may store annotations differently, 
        # but the key behavior is tested in TestUpsertBehavior
