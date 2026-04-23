"""Tests for database connection management."""

import os
import tempfile
from pathlib import Path
import pytest
import duckdb

from healthsim.db.connection import (
    DatabaseConnection,
    get_connection,
    DEFAULT_DB_PATH,
)


class TestDatabaseConnection:
    """Tests for DatabaseConnection class."""
    
    def setup_method(self):
        """Reset singleton before each test."""
        DatabaseConnection.reset()
    
    def teardown_method(self):
        """Clean up after each test."""
        DatabaseConnection.reset()
    
    def test_default_path(self):
        """Test that default path is set correctly."""
        conn = DatabaseConnection()
        assert conn.db_path == DEFAULT_DB_PATH
    
    def test_custom_path(self):
        """Test that custom path can be specified."""
        custom_path = Path("/tmp/test_healthsim.duckdb")
        conn = DatabaseConnection(custom_path)
        assert conn.db_path == custom_path
    
    def test_directory_creation(self, tmp_path):
        """Test that directory is created if it doesn't exist."""
        db_path = tmp_path / "subdir" / "test.duckdb"
        conn = DatabaseConnection(db_path)
        assert db_path.parent.exists()
    
    def test_connect_returns_connection(self, tmp_path):
        """Test that connect() returns a DuckDB connection."""
        db_path = tmp_path / "test.duckdb"
        conn = DatabaseConnection(db_path)
        db_conn = conn.connect()
        assert isinstance(db_conn, duckdb.DuckDBPyConnection)
    
    def test_connect_is_idempotent(self, tmp_path):
        """Test that multiple connect() calls return same connection."""
        db_path = tmp_path / "test.duckdb"
        conn = DatabaseConnection(db_path)
        conn1 = conn.connect()
        conn2 = conn.connect()
        assert conn1 is conn2
    
    def test_close_closes_connection(self, tmp_path):
        """Test that close() closes the connection."""
        db_path = tmp_path / "test.duckdb"
        conn = DatabaseConnection(db_path)
        conn.connect()
        conn.close()
        assert conn._connection is None
    
    def test_reconnect_after_close(self, tmp_path):
        """Test that we can reconnect after closing."""
        db_path = tmp_path / "test.duckdb"
        conn = DatabaseConnection(db_path)
        conn.connect()
        conn.close()
        new_conn = conn.connect()
        assert isinstance(new_conn, duckdb.DuckDBPyConnection)


class TestSingleton:
    """Tests for singleton pattern."""
    
    def setup_method(self):
        """Reset singleton before each test."""
        DatabaseConnection.reset()
    
    def teardown_method(self):
        """Clean up after each test."""
        DatabaseConnection.reset()
    
    def test_get_instance_returns_same_instance(self, tmp_path):
        """Test that get_instance returns singleton."""
        db_path = tmp_path / "test.duckdb"
        instance1 = DatabaseConnection.get_instance(db_path)
        instance2 = DatabaseConnection.get_instance()
        assert instance1 is instance2
    
    def test_reset_clears_instance(self, tmp_path):
        """Test that reset clears the singleton."""
        db_path = tmp_path / "test.duckdb"
        instance1 = DatabaseConnection.get_instance(db_path)
        DatabaseConnection.reset()
        instance2 = DatabaseConnection.get_instance(db_path)
        assert instance1 is not instance2


class TestGetConnection:
    """Tests for get_connection convenience function."""
    
    def setup_method(self):
        """Reset singleton before each test."""
        DatabaseConnection.reset()
    
    def teardown_method(self):
        """Clean up after each test."""
        DatabaseConnection.reset()
    
    def test_get_connection_returns_connection(self, tmp_path):
        """Test that get_connection returns a DuckDB connection."""
        db_path = tmp_path / "test.duckdb"
        conn = get_connection(db_path)
        assert isinstance(conn, duckdb.DuckDBPyConnection)
    
    def test_get_connection_creates_database(self, tmp_path):
        """Test that get_connection creates database file."""
        db_path = tmp_path / "test.duckdb"
        get_connection(db_path)
        assert db_path.exists()
