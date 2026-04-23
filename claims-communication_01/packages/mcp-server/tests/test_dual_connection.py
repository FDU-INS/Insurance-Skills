"""
Tests for DuckDB dual-connection pattern and concurrent access.

Verifies that:
1. Multiple read-only connections can access database simultaneously
2. Read operations work while MCP server pattern is active
3. Write operations acquire/release locks properly
4. External processes (like pytest) can query while MCP holds read connection

IMPORTANT: These tests require the NEW MCP server with dual-connection pattern.
If the old MCP server is running, tests will skip with instructions to restart.
"""

import os
import sys
import tempfile
import threading
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

import pytest
import duckdb

# Add healthsim to path
WORKSPACE_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(WORKSPACE_ROOT / "packages" / "core" / "src"))
sys.path.insert(0, str(WORKSPACE_ROOT / "packages" / "mcp-server"))

from healthsim.db import DEFAULT_DB_PATH


def check_db_accessible(db_path=DEFAULT_DB_PATH):
    """Check if database is accessible. Skip test if old MCP server holds exclusive lock."""
    if not db_path.exists():
        pytest.skip(f"Database not found: {db_path}")
    
    try:
        conn = duckdb.connect(str(db_path), read_only=True)
        conn.close()
        return True
    except duckdb.IOException as e:
        if "Conflicting lock" in str(e):
            pytest.skip(
                "Old MCP server holding exclusive lock. "
                "Please restart Claude Desktop to activate the new dual-connection MCP server. "
                "After restart, run tests again to verify concurrent access works."
            )
        raise


class TestReadOnlyConcurrency:
    """Test that multiple read-only connections work simultaneously."""
    
    def test_multiple_read_connections_same_process(self):
        """Multiple read-only connections in same process should work."""
        check_db_accessible()
        
        conn1 = duckdb.connect(str(DEFAULT_DB_PATH), read_only=True)
        conn2 = duckdb.connect(str(DEFAULT_DB_PATH), read_only=True)
        conn3 = duckdb.connect(str(DEFAULT_DB_PATH), read_only=True)
        
        try:
            # All should be able to query
            result1 = conn1.execute("SELECT COUNT(*) FROM cohorts").fetchone()
            result2 = conn2.execute("SELECT COUNT(*) FROM cohorts").fetchone()
            result3 = conn3.execute("SELECT COUNT(*) FROM cohorts").fetchone()
            
            # All should return same count
            assert result1 == result2 == result3
        finally:
            conn1.close()
            conn2.close()
            conn3.close()
    
    def test_concurrent_read_queries(self):
        """Concurrent read queries should not block each other."""
        check_db_accessible()
        
        results = []
        errors = []
        
        def run_query(query_id: int):
            try:
                conn = duckdb.connect(str(DEFAULT_DB_PATH), read_only=True)
                # Simulate some work
                result = conn.execute("""
                    SELECT COUNT(*) as cnt FROM network.providers 
                    WHERE practice_state = 'CA'
                """).fetchone()
                conn.close()
                return (query_id, result[0])
            except Exception as e:
                return (query_id, f"ERROR: {e}")
        
        # Run 5 concurrent queries
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(run_query, i) for i in range(5)]
            for future in as_completed(futures):
                results.append(future.result())
        
        # All should succeed with same result
        assert len(results) == 5
        counts = [r[1] for r in results]
        assert all(isinstance(c, int) for c in counts), f"Some queries failed: {results}"
        assert len(set(counts)) == 1, "All queries should return same count"
    
    def test_read_connection_does_not_block_other_reads(self):
        """A held read connection should not block other read connections."""
        check_db_accessible()
        
        # Simulate MCP server holding a read connection
        mcp_conn = duckdb.connect(str(DEFAULT_DB_PATH), read_only=True)
        
        try:
            # Keep MCP connection active with a query
            mcp_conn.execute("SELECT 1")
            
            # External process (pytest) should also work
            external_conn = duckdb.connect(str(DEFAULT_DB_PATH), read_only=True)
            result = external_conn.execute("SELECT COUNT(*) FROM cohorts").fetchone()
            external_conn.close()
            
            assert result is not None
            assert isinstance(result[0], int)
        finally:
            mcp_conn.close()


class TestConnectionManagerPattern:
    """Test the ConnectionManager dual-connection pattern."""
    
    def test_connection_manager_with_temp_db(self, tmp_path):
        """ConnectionManager should reuse read connection with temp database."""
        from healthsim_mcp import ConnectionManager
        
        # Create temp database
        db_path = tmp_path / "test.duckdb"
        setup = duckdb.connect(str(db_path))
        setup.execute("CREATE TABLE test (id INT)")
        setup.close()
        
        manager = ConnectionManager(db_path)
        
        try:
            conn1 = manager.get_read_connection()
            conn2 = manager.get_read_connection()
            
            # Should be same connection object
            assert conn1 is conn2
            
            # Should work
            result = conn1.execute("SELECT 1").fetchone()
            assert result[0] == 1
        finally:
            manager.close()
    
    def test_write_context_with_temp_db(self, tmp_path):
        """Write context manager should acquire and release connection."""
        from healthsim_mcp import ConnectionManager
        
        # Create temp database
        db_path = tmp_path / "test.duckdb"
        setup = duckdb.connect(str(db_path))
        setup.execute("CREATE TABLE test (id INT, value TEXT)")
        setup.close()
        
        manager = ConnectionManager(db_path)
        
        try:
            # Write connection should work
            with manager.write_connection() as conn:
                conn.execute("INSERT INTO test VALUES (1, 'test')")
            
            # After context exits, verify data was written
            read_conn = manager.get_read_connection()
            result = read_conn.execute("SELECT value FROM test WHERE id = 1").fetchone()
            assert result[0] == "test"
        finally:
            manager.close()
    
    def test_production_connection_manager(self):
        """ConnectionManager works with production database."""
        check_db_accessible()
        
        from healthsim_mcp import ConnectionManager
        
        manager = ConnectionManager(DEFAULT_DB_PATH)
        
        try:
            conn1 = manager.get_read_connection()
            conn2 = manager.get_read_connection()
            
            # Should be same connection object
            assert conn1 is conn2
            
            # Should work
            result = conn1.execute("SELECT COUNT(*) FROM cohorts").fetchone()
            assert result[0] >= 0
        finally:
            manager.close()


class TestMCPToolsWithDualConnection:
    """Test that MCP tools work correctly with dual connection pattern."""
    
    def test_read_tools_use_shared_connection(self):
        """Read-only tools should use the shared read connection."""
        check_db_accessible()
        
        from healthsim_mcp import _get_manager, list_tables, ListCohortsInput, list_cohorts
        
        # Reset manager to ensure fresh state
        import healthsim_mcp
        healthsim_mcp._manager = None
        
        try:
            # Get the manager
            manager = _get_manager()
            
            # Call read-only tools
            tables_result = list_tables()
            assert "reference_tables" in tables_result
            
            cohorts_result = list_cohorts(ListCohortsInput())
            assert isinstance(cohorts_result, str)
            
            # Verify read connection is still active
            conn = manager.get_read_connection()
            result = conn.execute("SELECT 1").fetchone()
            assert result[0] == 1
        finally:
            if healthsim_mcp._manager:
                healthsim_mcp._manager.close()
            healthsim_mcp._manager = None
    
    def test_query_tool_read_only(self):
        """Query tool should work with read-only connection."""
        check_db_accessible()
        
        import healthsim_mcp
        from healthsim_mcp import query, QueryInput
        
        healthsim_mcp._manager = None
        
        try:
            # Valid read query
            result = query(QueryInput(sql="SELECT COUNT(*) as cnt FROM cohorts"))
            assert "row_count" in result
            
            # Should reject write attempts
            result = query(QueryInput(sql="INSERT INTO cohorts VALUES (1,2,3)"))
            assert "error" in result.lower()
        finally:
            if healthsim_mcp._manager:
                healthsim_mcp._manager.close()
            healthsim_mcp._manager = None
    
    def test_external_access_while_mcp_active(self):
        """External connections should work while MCP tools are active."""
        check_db_accessible()
        
        import healthsim_mcp
        from healthsim_mcp import _get_manager, list_tables
        
        healthsim_mcp._manager = None
        
        try:
            # Initialize MCP manager (simulates server startup)
            manager = _get_manager()
            _ = manager.get_read_connection()
            
            # Call a tool to ensure connection is active
            list_tables()
            
            # External read connection should work
            external = duckdb.connect(str(DEFAULT_DB_PATH), read_only=True)
            result = external.execute("SELECT COUNT(*) FROM network.providers").fetchone()
            external.close()
            
            assert result[0] > 0
        finally:
            if healthsim_mcp._manager:
                healthsim_mcp._manager.close()
            healthsim_mcp._manager = None


class TestConcurrentReadWrite:
    """Test concurrent read and write operations."""
    
    def test_write_does_not_permanently_block_reads(self, tmp_path):
        """After a write operation, reads should work immediately."""
        from healthsim_mcp import ConnectionManager
        
        # Create temp database
        db_path = tmp_path / "test.duckdb"
        setup = duckdb.connect(str(db_path))
        setup.execute("CREATE TABLE test (id INT)")
        setup.close()
        
        manager = ConnectionManager(db_path)
        
        try:
            # Do a "write" operation
            with manager.write_connection() as write_conn:
                write_conn.execute("INSERT INTO test VALUES (1)")
            
            # Immediately after, read should work
            read_conn = manager.get_read_connection()
            result = read_conn.execute("SELECT COUNT(*) FROM test").fetchone()
            assert result[0] == 1
        finally:
            manager.close()
    
    def test_read_operations_during_simulated_load(self):
        """Read operations should remain responsive during concurrent activity."""
        check_db_accessible()
        
        from healthsim_mcp import ConnectionManager
        
        manager = ConnectionManager(DEFAULT_DB_PATH)
        read_times = []
        
        try:
            def do_reads():
                for _ in range(10):
                    start = time.time()
                    conn = manager.get_read_connection()
                    conn.execute("SELECT COUNT(*) FROM network.providers LIMIT 1").fetchone()
                    read_times.append(time.time() - start)
                    time.sleep(0.01)
            
            # Run reads in background
            read_thread = threading.Thread(target=do_reads)
            read_thread.start()
            read_thread.join(timeout=5)
            
            # All reads should complete quickly (< 1 second each)
            assert len(read_times) == 10
            assert all(t < 1.0 for t in read_times), f"Slow reads detected: {read_times}"
        finally:
            manager.close()


class TestDatabaseIntegrity:
    """Verify database integrity with dual connection pattern."""
    
    def test_network_schema_accessible(self):
        """Network schema should be accessible via read connection."""
        check_db_accessible()
        
        conn = duckdb.connect(str(DEFAULT_DB_PATH), read_only=True)
        
        try:
            # Check providers table
            result = conn.execute("""
                SELECT COUNT(*) FROM network.providers
            """).fetchone()
            assert result[0] > 1000000, "Expected millions of providers"
            
            # Check facilities table
            result = conn.execute("""
                SELECT COUNT(*) FROM network.facilities
            """).fetchone()
            assert result[0] > 10000, "Expected thousands of facilities"
        finally:
            conn.close()
    
    def test_population_schema_accessible(self):
        """Population schema should be accessible via read connection."""
        check_db_accessible()
        
        conn = duckdb.connect(str(DEFAULT_DB_PATH), read_only=True)
        
        try:
            # Check reference tables exist (in population schema)
            result = conn.execute("""
                SELECT COUNT(*) FROM population.places_county
            """).fetchone()
            assert result[0] > 3000, "Expected ~3143 counties"
            
            # Check SVI table if it exists
            try:
                result = conn.execute("""
                    SELECT COUNT(*) FROM population.svi_county
                """).fetchone()
                assert result[0] > 3000, "Expected ~3144 counties"
            except duckdb.CatalogException:
                pass  # SVI table may not exist in all configurations
        finally:
            conn.close()
    
    def test_cross_schema_join(self):
        """Cross-schema joins should work with read connection."""
        check_db_accessible()
        
        conn = duckdb.connect(str(DEFAULT_DB_PATH), read_only=True)
        
        try:
            result = conn.execute("""
                SELECT 
                    p.stateabbr,
                    p.countyname,
                    COUNT(DISTINCT n.npi) as provider_count
                FROM population.places_county p
                LEFT JOIN network.providers n 
                    ON p.stateabbr = n.practice_state
                WHERE p.stateabbr = 'CA'
                GROUP BY p.stateabbr, p.countyname
                LIMIT 5
            """).fetchall()
            
            assert len(result) > 0, "Should return California counties"
        finally:
            conn.close()
