"""
Tests for HealthSim MCP Server connection management.

Tests the dual-connection pattern:
- Persistent read-only connection for queries
- On-demand write connection for modifications
- Concurrent access from multiple processes

See docs/mcp/duckdb-connection-architecture.md for design details.

IMPORTANT: DuckDB connections are NOT thread-safe within the same process.
Each thread/process needs its own connection. The dual-connection pattern
works because:
1. MCP server handles requests serially (single-threaded)
2. External processes (pytest, CLI) use separate connections

These tests validate the architecture without violating DuckDB's threading model.
"""

import json
import os
import sys
import tempfile
import time
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from unittest.mock import patch
import multiprocessing

import pytest
import duckdb

# Add packages to path for imports
WORKSPACE_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(WORKSPACE_ROOT / "packages" / "core" / "src"))
sys.path.insert(0, str(WORKSPACE_ROOT / "packages" / "mcp-server"))

from healthsim.db import DEFAULT_DB_PATH


class TestDuckDBConcurrency:
    """
    Test DuckDB's concurrency behavior.
    
    These tests verify DuckDB's locking semantics that our dual-connection
    pattern relies on.
    """
    
    def test_multiple_read_only_connections_same_db(self, tmp_path):
        """Multiple read-only connections can access same database."""
        db_path = tmp_path / "test.duckdb"
        
        # Create database with some data
        setup_conn = duckdb.connect(str(db_path))
        setup_conn.execute("CREATE TABLE test (id INTEGER, value TEXT)")
        setup_conn.execute("INSERT INTO test VALUES (1, 'one'), (2, 'two')")
        setup_conn.close()
        
        # Open multiple read-only connections
        conn1 = duckdb.connect(str(db_path), read_only=True)
        conn2 = duckdb.connect(str(db_path), read_only=True)
        conn3 = duckdb.connect(str(db_path), read_only=True)
        
        # All should work simultaneously
        result1 = conn1.execute("SELECT COUNT(*) FROM test").fetchone()[0]
        result2 = conn2.execute("SELECT SUM(id) FROM test").fetchone()[0]
        result3 = conn3.execute("SELECT value FROM test WHERE id = 1").fetchone()[0]
        
        assert result1 == 2
        assert result2 == 3
        assert result3 == "one"
        
        conn1.close()
        conn2.close()
        conn3.close()
    
    def test_read_only_connection_blocks_write(self, tmp_path):
        """A read-only connection cannot write."""
        db_path = tmp_path / "test.duckdb"
        
        # Create database
        setup_conn = duckdb.connect(str(db_path))
        setup_conn.execute("CREATE TABLE test (id INTEGER)")
        setup_conn.close()
        
        # Open read-only connection
        read_conn = duckdb.connect(str(db_path), read_only=True)
        
        # Attempt to write should fail
        with pytest.raises(duckdb.InvalidInputException):
            read_conn.execute("INSERT INTO test VALUES (1)")
        
        read_conn.close()
    
    def test_sequential_write_then_read(self, tmp_path):
        """
        Verify writes are visible to subsequent reads.
        
        This simulates the pattern where MCP write operation completes,
        then a read operation sees the updated data.
        """
        db_path = tmp_path / "test.duckdb"
        
        # Create database
        setup_conn = duckdb.connect(str(db_path))
        setup_conn.execute("CREATE TABLE test (id INTEGER, value TEXT)")
        setup_conn.execute("INSERT INTO test VALUES (1, 'initial')")
        setup_conn.close()
        
        # Simulate write operation (brief exclusive lock)
        write_conn = duckdb.connect(str(db_path))
        write_conn.execute("UPDATE test SET value = 'updated' WHERE id = 1")
        write_conn.close()  # Release lock
        
        # Read operation should see the update
        read_conn = duckdb.connect(str(db_path), read_only=True)
        value = read_conn.execute("SELECT value FROM test WHERE id = 1").fetchone()[0]
        assert value == "updated"
        read_conn.close()
    
    def test_read_only_connections_see_same_data(self, tmp_path):
        """Multiple read-only connections see consistent data."""
        db_path = tmp_path / "test.duckdb"
        
        # Create database with data
        setup_conn = duckdb.connect(str(db_path))
        setup_conn.execute("CREATE TABLE test (id INTEGER)")
        setup_conn.execute("INSERT INTO test SELECT * FROM range(100)")
        setup_conn.close()
        
        # Multiple read connections
        conn1 = duckdb.connect(str(db_path), read_only=True)
        conn2 = duckdb.connect(str(db_path), read_only=True)
        
        # Both should see same count
        count1 = conn1.execute("SELECT COUNT(*) FROM test").fetchone()[0]
        count2 = conn2.execute("SELECT COUNT(*) FROM test").fetchone()[0]
        
        assert count1 == count2 == 100
        
        conn1.close()
        conn2.close()


class TestConnectionManager:
    """Tests for the MCP server's ConnectionManager class."""
    
    @pytest.fixture
    def temp_db(self, tmp_path):
        """Create a temporary database for testing."""
        db_path = tmp_path / "test_healthsim.duckdb"
        
        # Initialize with schema
        conn = duckdb.connect(str(db_path))
        conn.execute("""
            CREATE TABLE cohorts (
                cohort_id VARCHAR PRIMARY KEY,
                name VARCHAR UNIQUE NOT NULL,
                description VARCHAR,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE TABLE cohort_entities (
                id INTEGER PRIMARY KEY,
                cohort_id VARCHAR NOT NULL,
                entity_type VARCHAR NOT NULL,
                entity_id VARCHAR NOT NULL,
                entity_data JSON NOT NULL
            )
        """)
        conn.execute("""
            INSERT INTO cohorts (cohort_id, name, description)
            VALUES ('test-123', 'Test Cohort', 'A test cohort')
        """)
        conn.close()
        
        return db_path
    
    def test_connection_manager_import(self):
        """ConnectionManager can be imported from the MCP server."""
        from healthsim_mcp import ConnectionManager
        assert ConnectionManager is not None
    
    def test_read_connection_is_persistent(self, temp_db):
        """Read connection should be reused across calls."""
        from healthsim_mcp import ConnectionManager
        
        manager = ConnectionManager(temp_db)
        
        conn1 = manager.get_read_connection()
        conn2 = manager.get_read_connection()
        
        assert conn1 is conn2
        
        manager.close()
    
    def test_read_connection_is_read_only(self, temp_db):
        """Read connection should not allow writes."""
        from healthsim_mcp import ConnectionManager
        
        manager = ConnectionManager(temp_db)
        conn = manager.get_read_connection()
        
        with pytest.raises(duckdb.InvalidInputException):
            conn.execute("INSERT INTO cohorts (cohort_id, name) VALUES ('x', 'x')")
        
        manager.close()
    
    def test_write_connection_context_manager(self, temp_db):
        """Write connection should be acquired and released via context manager."""
        from healthsim_mcp import ConnectionManager
        
        manager = ConnectionManager(temp_db)
        
        # Write using context manager
        with manager.write_connection() as conn:
            conn.execute("""
                INSERT INTO cohorts (cohort_id, name, description)
                VALUES ('new-123', 'New Scenario', 'Created via write_connection')
            """)
        
        # Connection should be closed after context exits
        # Verify by reading with read connection
        read_conn = manager.get_read_connection()
        result = read_conn.execute(
            "SELECT name FROM cohorts WHERE cohort_id = 'new-123'"
        ).fetchone()
        
        assert result[0] == "New Scenario"
        
        manager.close()
    
    def test_write_connection_releases_lock(self, temp_db):
        """Write connection should release lock after context exits."""
        from healthsim_mcp import ConnectionManager
        
        manager = ConnectionManager(temp_db)
        
        # First write
        with manager.write_connection() as conn:
            conn.execute("""
                INSERT INTO cohorts (cohort_id, name)
                VALUES ('cohort-1', 'First')
            """)
        
        # Second write should work (lock was released)
        with manager.write_connection() as conn:
            conn.execute("""
                INSERT INTO cohorts (cohort_id, name)
                VALUES ('cohort-2', 'Second')
            """)
        
        # Verify both exist
        read_conn = manager.get_read_connection()
        count = read_conn.execute("SELECT COUNT(*) FROM cohorts").fetchone()[0]
        assert count == 3  # original + 2 new
        
        manager.close()
    
    def test_sequential_reads_work(self, temp_db):
        """Sequential read operations work correctly."""
        from healthsim_mcp import ConnectionManager
        
        manager = ConnectionManager(temp_db)
        conn = manager.get_read_connection()
        
        # Multiple sequential reads
        for i in range(10):
            result = conn.execute("SELECT COUNT(*) FROM cohorts").fetchone()[0]
            assert result == 1
        
        manager.close()
    
    def test_write_then_read_in_sequence(self, temp_db):
        """Write operation followed by read sees the changes.
        
        Note: DuckDB doesn't allow mixing read-only and read-write connections
        to the same file within the same process. So we use separate managers
        for write and read operations.
        """
        from healthsim_mcp import ConnectionManager
        
        # First: Write operation (needs exclusive connection)
        write_manager = ConnectionManager(temp_db)
        with write_manager.write_connection() as write_conn:
            write_conn.execute("""
                INSERT INTO cohorts (cohort_id, name)
                VALUES ('new-1', 'New One')
            """)
        write_manager.close()  # Release all connections
        
        # Second: Read operation (separate manager)
        read_manager = ConnectionManager(temp_db)
        read_conn = read_manager.get_read_connection()
        count = read_conn.execute("SELECT COUNT(*) FROM cohorts").fetchone()[0]
        assert count == 2  # original + new
        read_manager.close()


class TestMCPToolsWithDualConnection:
    """
    Integration tests for MCP tools using the dual-connection pattern.
    
    These tests verify that the actual MCP tool functions work correctly
    with the new connection management.
    """
    
    @pytest.fixture
    def mock_db_path(self, tmp_path):
        """Create a mock database and patch the MCP server to use it."""
        db_path = tmp_path / "test_healthsim.duckdb"
        
        # Initialize full schema (simplified version for testing)
        conn = duckdb.connect(str(db_path))
        conn.execute("""
            CREATE TABLE cohorts (
                cohort_id VARCHAR PRIMARY KEY,
                name VARCHAR UNIQUE NOT NULL,
                description VARCHAR,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
                entity_data JSON NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE schema_migrations (
                version VARCHAR PRIMARY KEY,
                description VARCHAR,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # Add PopulationSim reference tables (minimal)
        conn.execute("""
            CREATE TABLE ref_places_county (
                stateabbr VARCHAR,
                countyname VARCHAR,
                countycode VARCHAR
            )
        """)
        conn.execute("""
            INSERT INTO ref_places_county VALUES 
            ('CA', 'Los Angeles', '06037'),
            ('CA', 'San Diego', '06073'),
            ('NY', 'New York', '36061')
        """)
        conn.close()
        
        return db_path
    
    def test_list_tables_uses_read_connection(self, mock_db_path):
        """list_tables should work with read-only connection."""
        import healthsim_mcp as mcp_module
        
        # Patch the DB_PATH
        with patch.object(mcp_module, 'DB_PATH', mock_db_path):
            # Reset the manager to use new path
            mcp_module._manager = None
            
            result = mcp_module.list_tables()
            data = json.loads(result)
            
            assert "reference_tables" in data
            assert "ref_places_county" in data["reference_tables"]
            assert "entity_tables" in data or data["entity_tables"] == []
            
            # Clean up
            if mcp_module._manager:
                mcp_module._manager.close()
            mcp_module._manager = None
    
    def test_query_uses_read_connection(self, mock_db_path):
        """query tool should work with read-only connection."""
        import healthsim_mcp as mcp_module
        from healthsim_mcp import QueryInput
        
        with patch.object(mcp_module, 'DB_PATH', mock_db_path):
            mcp_module._manager = None
            
            params = QueryInput(sql="SELECT COUNT(*) as cnt FROM ref_places_county")
            result = mcp_module.query(params)
            data = json.loads(result)
            
            assert "rows" in data
            assert data["rows"][0]["cnt"] == 3
            
            if mcp_module._manager:
                mcp_module._manager.close()
            mcp_module._manager = None


class TestConcurrentAccessWithProduction:
    """
    Tests that verify concurrent access works with the production database.
    
    These tests use read-only connections and should work even if the
    MCP server is running WITH THE NEW DUAL-CONNECTION PATTERN.
    
    If the old MCP server (with exclusive lock) is running, these tests
    will be skipped with a message to restart the server.
    """
    
    @pytest.fixture
    def production_db(self):
        """Get path to production database if it exists."""
        if not DEFAULT_DB_PATH.exists():
            pytest.skip("Production database not found")
        return DEFAULT_DB_PATH
    
    def _check_can_connect(self, db_path):
        """Check if we can connect to the database."""
        try:
            conn = duckdb.connect(str(db_path), read_only=True)
            conn.close()
            return True
        except duckdb.IOException as e:
            if "Conflicting lock" in str(e):
                pytest.skip(
                    "MCP server holding exclusive lock. "
                    "Restart the MCP server to use the new dual-connection pattern. "
                    f"Error: {e}"
                )
            raise
    
    def test_read_only_access_to_production(self, production_db):
        """Can open read-only connection to production database."""
        self._check_can_connect(production_db)
        
        conn = duckdb.connect(str(production_db), read_only=True)
        
        # Should be able to query
        result = conn.execute("SHOW TABLES").fetchall()
        tables = [row[0] for row in result]
        
        assert len(tables) > 0
        # Tables are in main schema (scenarios, patients) or population schema
        assert "scenarios" in tables or "patients" in tables
        
        conn.close()
    
    def test_multiple_read_connections_to_production(self, production_db):
        """Multiple read-only connections can access production simultaneously."""
        self._check_can_connect(production_db)
        
        conn1 = duckdb.connect(str(production_db), read_only=True)
        conn2 = duckdb.connect(str(production_db), read_only=True)
        
        # Both should work
        result1 = conn1.execute("SELECT 1 as test").fetchone()[0]
        result2 = conn2.execute("SELECT 2 as test").fetchone()[0]
        
        assert result1 == 1
        assert result2 == 2
        
        conn1.close()
        conn2.close()
    
    def test_query_cohorts_read_only(self, production_db):
        """Can query scenarios table with read-only connection."""
        self._check_can_connect(production_db)
        
        conn = duckdb.connect(str(production_db), read_only=True)
        
        result = conn.execute("SELECT COUNT(*) FROM scenarios").fetchone()[0]
        
        # Just verify we can query - count may be 0 or more
        assert result >= 0
        
        conn.close()
    
    def test_query_reference_data_read_only(self, production_db):
        """Can query reference data with read-only connection."""
        self._check_can_connect(production_db)
        
        conn = duckdb.connect(str(production_db), read_only=True)
        
        # Check if reference tables exist
        tables = conn.execute("SHOW TABLES").fetchall()
        table_names = [t[0] for t in tables]
        
        if "ref_places_county" in table_names:
            result = conn.execute(
                "SELECT COUNT(*) FROM ref_places_county"
            ).fetchone()[0]
            assert result > 0  # Should have CDC PLACES data
        
        conn.close()


class TestNetworkSimConcurrentAccess:
    """Tests for NetworkSim-specific concurrent access patterns."""
    
    @pytest.fixture
    def production_db(self):
        """Get production database path."""
        if not DEFAULT_DB_PATH.exists():
            pytest.skip("Production database not found")
        return DEFAULT_DB_PATH
    
    def _check_can_connect(self, db_path):
        """Check if we can connect to the database."""
        try:
            conn = duckdb.connect(str(db_path), read_only=True)
            conn.close()
            return True
        except duckdb.IOException as e:
            if "Conflicting lock" in str(e):
                pytest.skip(
                    "MCP server holding exclusive lock. Restart server to test."
                )
            raise
    
    def test_network_provider_query_read_only(self, production_db):
        """Can query network.providers with read-only connection."""
        self._check_can_connect(production_db)
        
        conn = duckdb.connect(str(production_db), read_only=True)
        
        # Check for network schema
        try:
            result = conn.execute(
                "SELECT COUNT(*) FROM network.providers LIMIT 1"
            ).fetchone()[0]
            assert result > 0
        except duckdb.CatalogException:
            pytest.skip("network.providers table not found")
        finally:
            conn.close()
    
    def test_cross_schema_join_read_only(self, production_db):
        """Can perform cross-schema joins with read-only connection."""
        self._check_can_connect(production_db)
        
        conn = duckdb.connect(str(production_db), read_only=True)
        
        try:
            # Test join between network and population schemas
            # Join on state (practice_state in providers, st_abbr in svi_county)
            result = conn.execute("""
                SELECT COUNT(*)
                FROM network.providers p
                JOIN population.svi_county s ON p.practice_state = s.st_abbr
                LIMIT 1
            """).fetchone()[0]
            assert result >= 0
        except duckdb.CatalogException:
            pytest.skip("Required tables not found")
        finally:
            conn.close()


class TestPopulationSimConcurrentAccess:
    """Tests for PopulationSim-specific concurrent access patterns."""
    
    @pytest.fixture
    def production_db(self):
        """Get production database path."""
        if not DEFAULT_DB_PATH.exists():
            pytest.skip("Production database not found")
        return DEFAULT_DB_PATH
    
    def _check_can_connect(self, db_path):
        """Check if we can connect to the database."""
        try:
            conn = duckdb.connect(str(db_path), read_only=True)
            conn.close()
            return True
        except duckdb.IOException as e:
            if "Conflicting lock" in str(e):
                pytest.skip(
                    "MCP server holding exclusive lock. Restart server to test."
                )
            raise
    
    def test_places_county_query_read_only(self, production_db):
        """Can query population.places_county with read-only connection."""
        self._check_can_connect(production_db)
        
        conn = duckdb.connect(str(production_db), read_only=True)
        try:
            result = conn.execute(
                "SELECT COUNT(*) FROM population.places_county"
            ).fetchone()[0]
            # Should have ~3,143 counties
            assert result > 3000
        except duckdb.CatalogException:
            pytest.skip("population.places_county table not found")
        finally:
            conn.close()
    
    def test_svi_county_query_read_only(self, production_db):
        """Can query population.svi_county with read-only connection."""
        self._check_can_connect(production_db)
        
        conn = duckdb.connect(str(production_db), read_only=True)
        try:
            result = conn.execute(
                "SELECT COUNT(*) FROM population.svi_county"
            ).fetchone()[0]
            # Should have ~3,144 counties
            assert result > 3000
        except duckdb.CatalogException:
            pytest.skip("population.svi_county table not found")
        finally:
            conn.close()
    
    def test_adi_blockgroup_query_read_only(self, production_db):
        """Can query population.adi_blockgroup with read-only connection."""
        self._check_can_connect(production_db)
        
        conn = duckdb.connect(str(production_db), read_only=True)
        try:
            result = conn.execute(
                "SELECT COUNT(*) FROM population.adi_blockgroup"
            ).fetchone()[0]
            # Should have ~242,336 block groups
            assert result > 200000
        except duckdb.CatalogException:
            pytest.skip("population.adi_blockgroup table not found")
        finally:
            conn.close()


# Helper function for process-based concurrency tests
def _query_table_in_process(args):
    """Query a table in a separate process."""
    db_path, table_name = args
    try:
        conn = duckdb.connect(str(db_path), read_only=True)
        count = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
        conn.close()
        return (table_name, count, None)
    except Exception as e:
        return (table_name, None, str(e))


class TestMultiProcessConcurrency:
    """
    Test concurrent access from multiple processes.
    
    This is the actual use case for the dual-connection pattern:
    MCP server in one process, pytest/CLI in another.
    """
    
    @pytest.fixture
    def production_db(self):
        """Get production database path."""
        if not DEFAULT_DB_PATH.exists():
            pytest.skip("Production database not found")
        return DEFAULT_DB_PATH
    
    def _check_can_connect(self, db_path):
        """Check if we can connect to the database."""
        try:
            conn = duckdb.connect(str(db_path), read_only=True)
            conn.close()
            return True
        except duckdb.IOException as e:
            if "Conflicting lock" in str(e):
                pytest.skip(
                    "MCP server holding exclusive lock. Restart server to test."
                )
            raise
    
    def test_concurrent_process_reads(self, production_db):
        """Multiple processes can read simultaneously."""
        self._check_can_connect(production_db)
        
        # Use tables that actually exist in the healthsim database
        tables = [
            "patients",
            "members",
            "encounters",
        ]
        
        args = [(production_db, t) for t in tables]
        
        # Use ProcessPoolExecutor for true multi-process
        with ProcessPoolExecutor(max_workers=3) as executor:
            results = list(executor.map(_query_table_in_process, args))
        
        # At least one should succeed
        successful = [r for r in results if r[2] is None]
        assert len(successful) > 0, f"All queries failed: {results}"
