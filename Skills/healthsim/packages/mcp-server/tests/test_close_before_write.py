"""
Tests for the Close-Before-Write connection pattern.

This pattern solves a specific DuckDB constraint:
- DuckDB does NOT allow simultaneous connections with different read_only
  configurations to the same database file, even within the same process.

The close-before-write pattern:
1. Hold a persistent read-only connection for fast repeated reads
2. Before any write operation, close the read connection
3. Open a read-write connection, perform write, close it
4. Let the read connection reopen lazily on next read

This test file specifically validates this pattern works correctly.
"""

import json
import sys
from pathlib import Path

import pytest
import duckdb

# Add packages to path
WORKSPACE_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(WORKSPACE_ROOT / "packages" / "core" / "src"))
sys.path.insert(0, str(WORKSPACE_ROOT / "packages" / "mcp-server"))


class TestCloseBeforeWritePattern:
    """Tests that validate the close-before-write pattern works correctly."""
    
    @pytest.fixture
    def temp_db(self, tmp_path):
        """Create a temporary database for testing."""
        db_path = tmp_path / "test.duckdb"
        
        conn = duckdb.connect(str(db_path))
        conn.execute("CREATE TABLE test (id INTEGER, value TEXT)")
        conn.execute("INSERT INTO test VALUES (1, 'initial')")
        conn.close()
        
        return db_path
    
    def test_mixed_config_connections_fail(self, temp_db):
        """
        Verify that DuckDB rejects mixed read_only configurations.
        
        This is the constraint that the close-before-write pattern solves.
        """
        # Open read-only connection
        read_conn = duckdb.connect(str(temp_db), read_only=True)
        
        # Attempt to open read-write connection while read-only is open
        # DuckDB raises ConnectionException (subclass of Error)
        with pytest.raises((duckdb.IOException, duckdb.ConnectionException)) as exc_info:
            write_conn = duckdb.connect(str(temp_db), read_only=False)
        
        assert "different configuration" in str(exc_info.value).lower()
        
        read_conn.close()
    
    def test_close_before_write_succeeds(self, temp_db):
        """
        Verify that closing read connection before write allows the write.
        """
        # Open read-only connection
        read_conn = duckdb.connect(str(temp_db), read_only=True)
        result = read_conn.execute("SELECT value FROM test WHERE id = 1").fetchone()
        assert result[0] == "initial"
        
        # Close read connection BEFORE opening write connection
        read_conn.close()
        
        # Now write connection should work
        write_conn = duckdb.connect(str(temp_db), read_only=False)
        write_conn.execute("UPDATE test SET value = 'updated' WHERE id = 1")
        write_conn.close()
        
        # Reopen read connection to verify
        read_conn = duckdb.connect(str(temp_db), read_only=True)
        result = read_conn.execute("SELECT value FROM test WHERE id = 1").fetchone()
        assert result[0] == "updated"
        read_conn.close()
    
    def test_connection_manager_close_before_write(self, temp_db):
        """
        Verify ConnectionManager implements close-before-write correctly.
        """
        from healthsim_mcp import ConnectionManager
        
        manager = ConnectionManager(temp_db)
        
        # Step 1: Read operation (establishes read connection)
        read_conn = manager.get_read_connection()
        result = read_conn.execute("SELECT value FROM test WHERE id = 1").fetchone()
        assert result[0] == "initial"
        
        # Verify read connection is cached
        assert manager._read_conn is not None
        
        # Step 2: Write operation (should close read first)
        with manager.write_connection() as write_conn:
            write_conn.execute("UPDATE test SET value = 'updated' WHERE id = 1")
        
        # Step 3: Read again (should reopen read connection)
        read_conn = manager.get_read_connection()
        result = read_conn.execute("SELECT value FROM test WHERE id = 1").fetchone()
        assert result[0] == "updated"
        
        manager.close()
    
    def test_read_connection_closed_during_write(self, temp_db):
        """
        Verify that read connection is None during write operation.
        """
        from healthsim_mcp import ConnectionManager
        
        manager = ConnectionManager(temp_db)
        
        # Establish read connection
        _ = manager.get_read_connection()
        assert manager._read_conn is not None
        
        # During write, read connection should be closed
        with manager.write_connection() as write_conn:
            # Inside write context, read connection should be None
            assert manager._read_conn is None
            write_conn.execute("INSERT INTO test VALUES (2, 'new')")
        
        # After write, read connection is still None (lazy reopen)
        assert manager._read_conn is None
        
        # Next read reopens it
        _ = manager.get_read_connection()
        assert manager._read_conn is not None
        
        manager.close()
    
    def test_multiple_write_operations(self, temp_db):
        """
        Verify multiple sequential write operations work correctly.
        """
        from healthsim_mcp import ConnectionManager
        
        manager = ConnectionManager(temp_db)
        
        # Read -> Write -> Read -> Write -> Read
        
        # Read 1
        conn = manager.get_read_connection()
        count = conn.execute("SELECT COUNT(*) FROM test").fetchone()[0]
        assert count == 1
        
        # Write 1
        with manager.write_connection() as write_conn:
            write_conn.execute("INSERT INTO test VALUES (2, 'second')")
        
        # Read 2
        conn = manager.get_read_connection()
        count = conn.execute("SELECT COUNT(*) FROM test").fetchone()[0]
        assert count == 2
        
        # Write 2
        with manager.write_connection() as write_conn:
            write_conn.execute("INSERT INTO test VALUES (3, 'third')")
        
        # Read 3
        conn = manager.get_read_connection()
        count = conn.execute("SELECT COUNT(*) FROM test").fetchone()[0]
        assert count == 3
        
        manager.close()
    
    def test_read_manager_invalidated_on_write(self, temp_db):
        """
        Verify that StateManager (read_manager) is invalidated during write.
        """
        from healthsim_mcp import ConnectionManager
        
        manager = ConnectionManager(temp_db)
        
        # Get read manager (triggers read connection)
        read_mgr = manager.get_read_manager()
        assert manager._read_manager is not None
        
        # Write operation should invalidate read manager
        with manager.write_connection() as write_conn:
            assert manager._read_manager is None
            write_conn.execute("SELECT 1")  # Just to use the connection
        
        # After write, read manager is None
        assert manager._read_manager is None
        
        # Next call creates new read manager
        new_read_mgr = manager.get_read_manager()
        assert manager._read_manager is not None
        # It should be a different object (fresh connection)
        # (Can't compare directly since old one is invalid)
        
        manager.close()


class TestMCPToolsReadThenWrite:
    """
    Test MCP tool functions with the read-then-write pattern.
    
    This simulates the actual failure case: query reference data,
    then try to save a cohort.
    """
    
    @pytest.fixture
    def mock_db(self, tmp_path):
        """Create a mock database with full schema."""
        db_path = tmp_path / "test_healthsim.duckdb"
        
        conn = duckdb.connect(str(db_path))
        
        # Main schema - must match what StateManager expects
        conn.execute("""
            CREATE TABLE cohorts (
                id VARCHAR PRIMARY KEY,
                name VARCHAR UNIQUE NOT NULL,
                description VARCHAR,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                metadata JSON
            )
        """)
        conn.execute("""
            CREATE TABLE cohort_tags (
                cohort_id VARCHAR NOT NULL,
                tag VARCHAR NOT NULL,
                PRIMARY KEY (cohort_id, tag)
            )
        """)
        conn.execute("""
            CREATE TABLE cohort_entities (
                id INTEGER PRIMARY KEY,
                cohort_id VARCHAR NOT NULL,
                entity_type VARCHAR NOT NULL,
                entity_id VARCHAR NOT NULL,
                entity_data JSON NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Population schema (simplified)
        conn.execute("CREATE SCHEMA IF NOT EXISTS population")
        conn.execute("""
            CREATE TABLE population.places_county (
                stateabbr VARCHAR,
                countyname VARCHAR,
                countycode VARCHAR,
                diabetes_prevalence DOUBLE
            )
        """)
        conn.execute("""
            INSERT INTO population.places_county VALUES 
            ('CA', 'San Diego', '06073', 10.0),
            ('CA', 'Los Angeles', '06037', 11.5)
        """)
        
        conn.close()
        return db_path
    
    def test_query_then_save_cohort(self, mock_db):
        """
        Test the exact failure case: query reference data, then save.
        
        This is the bug that was reported - querying places_county followed
        by save_cohort caused a connection configuration conflict.
        
        Note: We test with empty entities to avoid schema complexity.
        The key validation is that the connection pattern allows read → write → read.
        """
        import healthsim_mcp as mcp_module
        from healthsim_mcp import QueryInput, SaveCohortInput
        from unittest.mock import patch
        
        with patch.object(mcp_module, 'DB_PATH', mock_db):
            mcp_module._manager = None
            
            try:
                # Step 1: Query reference data (uses read connection)
                query_result = mcp_module.query(QueryInput(
                    sql="SELECT * FROM population.places_county WHERE stateabbr = 'CA'"
                ))
                data = json.loads(query_result)
                assert data["row_count"] == 2
                
                # Step 2: Save cohort with empty entities (focus on connection pattern)
                # The important thing is that this doesn't fail with connection conflict
                save_result = mcp_module.save_cohort(SaveCohortInput(
                    name="Test Cohort",
                    entities={},  # Empty - we're testing connection pattern, not full save
                    description="Created after query"
                ))
                save_data = json.loads(save_result)
                
                # Verify save succeeded
                assert save_data.get("status") == "saved", f"Save failed: {save_data}"
                assert "cohort_id" in save_data
                
                # Step 3: Query again to verify (read connection should reopen)
                query_result2 = mcp_module.query(QueryInput(
                    sql="SELECT COUNT(*) as cnt FROM cohorts"
                ))
                data2 = json.loads(query_result2)
                assert data2["rows"][0]["cnt"] == 1
                
            finally:
                if mcp_module._manager:
                    mcp_module._manager.close()
                mcp_module._manager = None
    
    def test_multiple_queries_then_save(self, mock_db):
        """
        Test multiple queries followed by save.
        """
        import healthsim_mcp as mcp_module
        from healthsim_mcp import QueryInput, SaveCohortInput
        from unittest.mock import patch
        
        with patch.object(mcp_module, 'DB_PATH', mock_db):
            mcp_module._manager = None
            
            try:
                # Multiple read operations
                for i in range(5):
                    result = mcp_module.query(QueryInput(
                        sql=f"SELECT '{i}' as iteration, * FROM population.places_county LIMIT 1"
                    ))
                    assert "rows" in result
                
                # Then save
                save_result = mcp_module.save_cohort(SaveCohortInput(
                    name="After Multiple Queries",
                    entities={"patients": []},
                ))
                save_data = json.loads(save_result)
                assert save_data.get("status") == "saved"
                
            finally:
                if mcp_module._manager:
                    mcp_module._manager.close()
                mcp_module._manager = None
    
    def test_interleaved_read_write_operations(self, mock_db):
        """
        Test interleaved read and write operations.
        """
        import healthsim_mcp as mcp_module
        from healthsim_mcp import (
            QueryInput, SaveCohortInput, ListCohortsInput,
            DeleteCohortInput
        )
        from unittest.mock import patch
        
        with patch.object(mcp_module, 'DB_PATH', mock_db):
            mcp_module._manager = None
            
            try:
                # Read
                mcp_module.query(QueryInput(sql="SELECT 1"))
                
                # Write 1
                mcp_module.save_cohort(SaveCohortInput(
                    name="Scenario 1",
                    entities={"patients": [{"id": "P1"}]},
                ))
                
                # Read
                result = mcp_module.list_cohorts(ListCohortsInput())
                assert "Scenario 1" in result
                
                # Write 2
                mcp_module.save_cohort(SaveCohortInput(
                    name="Scenario 2",
                    entities={"patients": [{"id": "P2"}]},
                ))
                
                # Read
                result = mcp_module.list_cohorts(ListCohortsInput())
                assert "Scenario 1" in result
                assert "Scenario 2" in result
                
                # Write 3 (delete)
                mcp_module.delete_cohort(DeleteCohortInput(
                    name_or_id="Scenario 1",
                    confirm=True
                ))
                
                # Read
                result = mcp_module.list_cohorts(ListCohortsInput())
                assert "Scenario 1" not in result
                assert "Scenario 2" in result
                
            finally:
                if mcp_module._manager:
                    mcp_module._manager.close()
                mcp_module._manager = None


class TestErrorHandling:
    """Test error handling in the close-before-write pattern."""
    
    @pytest.fixture
    def temp_db(self, tmp_path):
        """Create a temporary database."""
        db_path = tmp_path / "test.duckdb"
        conn = duckdb.connect(str(db_path))
        conn.execute("CREATE TABLE test (id INTEGER PRIMARY KEY)")
        conn.close()
        return db_path
    
    def test_write_error_allows_subsequent_reads(self, temp_db):
        """
        If a write operation fails, subsequent reads should still work.
        """
        from healthsim_mcp import ConnectionManager
        
        manager = ConnectionManager(temp_db)
        
        # Establish read connection
        conn = manager.get_read_connection()
        initial_count = conn.execute("SELECT COUNT(*) FROM test").fetchone()[0]
        
        # Attempt write that fails (duplicate key)
        manager.get_read_connection()  # Ensure read conn is open
        with manager.write_connection() as write_conn:
            write_conn.execute("INSERT INTO test VALUES (1)")
        
        # Try to insert duplicate (will fail)
        try:
            with manager.write_connection() as write_conn:
                write_conn.execute("INSERT INTO test VALUES (1)")  # Duplicate!
        except duckdb.ConstraintException:
            pass  # Expected
        
        # Read should still work
        conn = manager.get_read_connection()
        count = conn.execute("SELECT COUNT(*) FROM test").fetchone()[0]
        assert count == initial_count + 1  # First insert succeeded
        
        manager.close()
    
    def test_write_context_manager_cleanup_on_exception(self, temp_db):
        """
        Write context manager should clean up even if exception occurs.
        """
        from healthsim_mcp import ConnectionManager
        
        manager = ConnectionManager(temp_db)
        
        # Establish read connection
        _ = manager.get_read_connection()
        
        # Write that raises exception
        try:
            with manager.write_connection() as write_conn:
                write_conn.execute("INSERT INTO test VALUES (1)")
                raise ValueError("Simulated error")
        except ValueError:
            pass
        
        # Connection should still be properly closed
        # Next read should work
        conn = manager.get_read_connection()
        count = conn.execute("SELECT COUNT(*) FROM test").fetchone()[0]
        assert count == 1  # Insert happened before exception
        
        manager.close()
