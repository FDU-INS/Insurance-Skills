# DuckDB Connection Architecture for HealthSim MCP

## Overview

This document describes the **close-before-write pattern** used by the HealthSim MCP server to enable concurrent database access while maintaining write capability.

## Problem Statement

DuckDB uses file-level locking with specific concurrency rules:

| First Connection | Second Connection | Result |
|-----------------|-------------------|--------|
| Read-Write | Any | ❌ Blocked (exclusive lock) |
| Read-Only | Read-Only | ✅ Allowed (shared lock) |
| Read-Only | Read-Write | ❌ Blocked |

### Critical Constraint Discovered

**DuckDB does NOT allow simultaneous connections with different `read_only` configurations to the same database file, even within the same process.**

```python
# This FAILS - even in the same process
read_conn = duckdb.connect("db.duckdb", read_only=True)
write_conn = duckdb.connect("db.duckdb", read_only=False)  # ConnectionException!
```

Error message:
```
Connection Error: Can't open a connection to same database file 
with a different configuration than existing connections
```

This is more restrictive than the standard "multiple readers OR one writer" model. The `read_only` configuration must match across all connections to the same file.

## Solution: Close-Before-Write Pattern

Since we cannot hold both connection types simultaneously, we use a **close-before-write** pattern:

1. **Read operations**: Use a persistent read-only connection (fast, reusable)
2. **Write operations**: Close the read connection, open write connection, write, close write connection
3. **Subsequent reads**: Read connection reopens lazily

```
┌─────────────────────────────────────────────────────────────────────┐
│ healthsim-mcp Server                                                │
│                                                                     │
│  NORMAL STATE (most of the time)                                    │
│  ┌─────────────────────────────────┐                                │
│  │ Read Connection (persistent)    │                                │
│  │ read_only=True                  │                                │
│  │ Shared lock                     │                                │
│  │                                 │                                │
│  │ → healthsim_query()             │                                │
│  │ → healthsim_list_cohorts()    │                                │
│  │ → healthsim_load_cohort()     │                                │
│  │ → healthsim_get_cohort_summary()       │                                │
│  │ → healthsim_query_reference()   │                                │
│  │ → healthsim_tables()            │                                │
│  └─────────────────────────────────┘                                │
│                                                                     │
│  DURING WRITE (brief transition)                                    │
│  ┌─────────────────────────────────┐                                │
│  │ 1. Close read connection        │                                │
│  │ 2. Open write connection        │  → healthsim_save_cohort()   │
│  │ 3. Perform write operation      │  → healthsim_delete_cohort() │
│  │ 4. Close write connection       │                                │
│  │ 5. (Read reopens lazily)        │                                │
│  └─────────────────────────────────┘                                │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│                        healthsim.duckdb                             │
│                        (1.7 GB)                                     │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ↓ Concurrent Read Access Possible
┌─────────────────────────────────────────────────────────────────────┐
│ External Processes (when MCP holds read connection)                 │
│                                                                     │
│ pytest (read_only=True)        ✅ Allowed                           │
│ CLI tools (read_only=True)     ✅ Allowed                           │
│ Jupyter notebooks (read_only)  ✅ Allowed                           │
└─────────────────────────────────────────────────────────────────────┘
```

## Implementation

### Connection Manager

```python
from contextlib import contextmanager
import duckdb

class ConnectionManager:
    """Manages DuckDB connections using close-before-write pattern.
    
    DuckDB Constraint: Cannot have simultaneous connections with different
    read_only configurations to the same database file, even in the same process.
    
    Solution:
    - Read operations: Use persistent read-only connection (shared lock)
    - Write operations: Close read connection first, open read-write connection,
      perform write, close write connection. Read connection reopens lazily.
    """
    
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._read_conn: Optional[duckdb.DuckDBPyConnection] = None
        self._read_manager: Optional[StateManager] = None
    
    def get_read_connection(self) -> duckdb.DuckDBPyConnection:
        """Get persistent read-only connection.
        
        Uses shared lock - allows concurrent readers from other processes.
        Connection is reused across all read operations.
        Will be automatically reopened after write operations.
        """
        if self._read_conn is None:
            self._read_conn = duckdb.connect(str(self.db_path), read_only=True)
        return self._read_conn
    
    def _close_read_connection(self):
        """Close the read connection before write operations."""
        if self._read_conn is not None:
            self._read_conn.close()
            self._read_conn = None
            self._read_manager = None
    
    @contextmanager
    def write_connection(self):
        """Context manager for write operations.
        
        IMPORTANT: Closes read connection first to avoid DuckDB's constraint
        against mixing read_only=True and read_only=False connections.
        
        The read connection will be lazily reopened on the next read operation.
        """
        # Close read connection first - DuckDB doesn't allow mixed configurations
        self._close_read_connection()
        
        conn = duckdb.connect(str(self.db_path))  # read_only=False (default)
        try:
            yield conn
        finally:
            conn.close()
            # Read connection will reopen lazily on next read
    
    def close(self):
        """Close all connections."""
        if self._read_conn:
            self._read_conn.close()
            self._read_conn = None
            self._read_manager = None
```

### Tool Classification

| Tool | Operation Type | Connection | Notes |
|------|---------------|------------|-------|
| `healthsim_list_cohorts` | Read | Persistent read | Fast, reusable |
| `healthsim_load_cohort` | Read | Persistent read | Fast, reusable |
| `healthsim_get_cohort_summary` | Read | Persistent read | Fast, reusable |
| `healthsim_query` | Read | Persistent read | Fast, reusable |
| `healthsim_query_reference` | Read | Persistent read | Fast, reusable |
| `healthsim_tables` | Read | Persistent read | Fast, reusable |
| `healthsim_save_cohort` | **Write** | Close-then-write | Closes read first |
| `healthsim_delete_cohort` | **Write** | Close-then-write | Closes read first |

## Benefits

1. **Concurrent Testing**: pytest can run against live database while MCP server is active
2. **Multi-Tool Support**: Multiple processes can query database simultaneously  
3. **Reliable Writes**: No more "different configuration" errors when saving after queries
4. **Lazy Reconnection**: Read connection reopens automatically after writes
5. **Cloud-Ready**: Pattern works with hosted databases that have similar locking semantics

## Trade-offs

1. **Write Overhead**: Each write closes read connection, adds ~50ms latency
2. **Connection Churn**: Read connection may close/reopen around write operations
3. **Brief Read Unavailability**: During write, read connection is closed (milliseconds)

These trade-offs are acceptable because:
- Writes are infrequent (save/delete cohorts are rare operations)
- Read reopening is fast (~10-20ms)
- The alternative (connection conflicts) is unacceptable

## Sequence Diagram: Read → Write → Read

```
User          MCP Server           ConnectionManager        DuckDB
  |               |                       |                    |
  |--query------->|                       |                    |
  |               |--get_read_conn()----->|                    |
  |               |                       |--connect(ro=True)->|
  |               |                       |<---read_conn-------|
  |               |<--read_conn-----------|                    |
  |               |--execute(SELECT)------|----query---------->|
  |<--results-----|                       |                    |
  |               |                       |                    |
  |--save-------->|                       |                    |
  |               |--write_connection()--->|                    |
  |               |                       |--close(read_conn)->|
  |               |                       |--connect(ro=False)->|
  |               |                       |<---write_conn------|
  |               |<--write_conn----------|                    |
  |               |--execute(INSERT)------|----insert--------->|
  |               |--close(write_conn)---->|----close--------->|
  |<--success-----|                       |                    |
  |               |                       |                    |
  |--query------->|                       |                    |
  |               |--get_read_conn()----->|                    |
  |               |                       |--connect(ro=True)->|  (lazy reopen)
  |               |                       |<---read_conn-------|
  |               |<--read_conn-----------|                    |
  |               |--execute(SELECT)------|----query---------->|
  |<--results-----|                       |                    |
```

## Testing the Pattern

```python
def test_read_then_write_then_read():
    """Verify the close-before-write pattern works correctly."""
    from healthsim_mcp import ConnectionManager
    
    manager = ConnectionManager(db_path)
    
    # Step 1: Read operation (establishes read connection)
    read_conn = manager.get_read_connection()
    result = read_conn.execute("SELECT COUNT(*) FROM cohorts").fetchone()
    
    # Step 2: Write operation (closes read, opens write, closes write)
    with manager.write_connection() as write_conn:
        write_conn.execute("INSERT INTO cohorts ...")
    
    # Step 3: Read again (read connection reopens automatically)
    read_conn = manager.get_read_connection()
    result = read_conn.execute("SELECT COUNT(*) FROM cohorts").fetchone()
    
    manager.close()


def test_mixed_config_fails():
    """Demonstrate DuckDB's constraint that requires close-before-write."""
    read_conn = duckdb.connect("db.duckdb", read_only=True)
    
    # This will raise ConnectionException
    with pytest.raises(duckdb.ConnectionException):
        write_conn = duckdb.connect("db.duckdb", read_only=False)
    
    read_conn.close()
```

## Migration Notes

- The change is backward-compatible with existing claude_desktop_config.json configurations
- The `HEALTHSIM_READ_ONLY` environment variable is deprecated
- MCP server must be restarted to pick up the new connection pattern
- All existing tests continue to pass

## Related Documentation

- [MCP Configuration](configuration.md) - Server setup
- [Data Architecture](../data-architecture.md) - Database schema overview
- [Testing Patterns](../testing-patterns.md) - Test conventions

## Changelog

- **2024-12-29**: Updated from "dual-connection pattern" to "close-before-write pattern"
  - Root cause: DuckDB prohibits simultaneous connections with different `read_only` configs
  - Fix: Close read connection before opening write connection
  - Tests: Added `test_close_before_write.py` with 11 new tests
