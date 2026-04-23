# Session 01: Database Foundation

**Initiative**: DuckDB Unified Data Architecture  
**Phase**: 1 - Foundation  
**Estimated Duration**: 60-90 minutes  
**Prerequisites**: None (first session)

---

## Objective

Create the core database module with schema definitions, connection management, and migration support. This establishes the foundation for all subsequent DuckDB work.

---

## Context

HealthSim is migrating from JSON-based state management to DuckDB. This session creates:
1. The database module structure
2. Schema definitions for canonical and state management tables
3. Connection management with automatic database creation
4. Migration framework for schema versioning

### Reference Documents

Before starting, read these files to understand current architecture:

```
docs/initiatives/duckdb-architecture/MASTER-PLAN.md     # This initiative's plan
docs/state-management/specification.md                   # Current MCP tool specs  
skills/common/state-management.md                        # Current state skill
references/data-models.md                                # Canonical model schemas
```

### Design Decisions (Already Made)

- Database location: `~/.healthsim/healthsim.duckdb`
- All canonical tables include provenance columns
- Schema versioning handled at load time via migrations
- Conflict resolution: Latest entity wins (by UUID)

---

## Pre-Flight Checklist

- [ ] Read MASTER-PLAN.md and understand the initiative
- [ ] Verify git status is clean: `git status`
- [ ] Verify tests pass: `cd packages/core && source .venv/bin/activate && pytest tests/ -v`
- [ ] Read current state-management.md skill
- [ ] Read data-models.md for canonical schemas

---

## Deliverables

### 1. Database Module Structure

```
packages/core/healthsim/db/
├── __init__.py              # Module exports
├── connection.py            # Connection management, auto-create
├── schema.py                # DDL definitions (all layers)
├── migrations.py            # Schema versioning
└── queries.py               # Common query helpers
```

### 2. Schema Definitions

**Canonical Tables** (from data-models.md):
- `patients` - Core patient demographics
- `encounters` - Visits, admissions
- `diagnoses` - ICD-10 codes
- `procedures` - CPT/ICD-PCS codes
- `medications` - Active/historical meds
- `lab_results` - Laboratory results
- `vital_signs` - Vitals
- `clinical_notes` - Notes/documents
- `members` - Health plan members (MemberSim)
- `claims` - Claims headers
- `claim_lines` - Claim line items
- `prescriptions` - Rx fills (RxMemberSim)
- `subjects` - Trial subjects (TrialSim)
- `trial_visits` - Trial visit data

**State Management Tables**:
- `cohorts` - Cohort metadata
- `cohort_entities` - Entity-cohort junction
- `cohort_tags` - Tag organization

**System Tables**:
- `schema_migrations` - Applied migrations tracking

### 3. Tests

```
packages/core/tests/db/
├── __init__.py
├── test_connection.py       # Connection, auto-create tests
├── test_schema.py           # DDL application tests
└── test_migrations.py       # Migration framework tests
```

---

## Implementation Steps

### Step 1: Create Database Module Structure

```bash
# Create directories
mkdir -p packages/core/healthsim/db
mkdir -p packages/core/tests/db
touch packages/core/healthsim/db/__init__.py
touch packages/core/tests/db/__init__.py
```

### Step 2: Implement connection.py

```python
"""
Database connection management for HealthSim.

Provides:
- Automatic database creation on first access
- Connection pooling (via DuckDB's built-in)
- Path configuration (local vs cloud future)
"""

import os
from pathlib import Path
from typing import Optional
import duckdb

# Default database location
DEFAULT_DB_PATH = Path.home() / ".healthsim" / "healthsim.duckdb"


class DatabaseConnection:
    """Manages DuckDB connections for HealthSim."""
    
    _instance: Optional['DatabaseConnection'] = None
    _connection: Optional[duckdb.DuckDBPyConnection] = None
    
    def __init__(self, db_path: Optional[Path] = None):
        """
        Initialize database connection.
        
        Args:
            db_path: Path to database file. Uses DEFAULT_DB_PATH if not specified.
        """
        self.db_path = db_path or DEFAULT_DB_PATH
        self._ensure_directory()
    
    def _ensure_directory(self) -> None:
        """Create database directory if it doesn't exist."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
    
    def connect(self) -> duckdb.DuckDBPyConnection:
        """
        Get or create database connection.
        
        Returns:
            Active DuckDB connection.
        """
        if self._connection is None:
            self._connection = duckdb.connect(str(self.db_path))
            self._initialize_if_needed()
        return self._connection
    
    def _initialize_if_needed(self) -> None:
        """Apply schema if this is a new database."""
        from .schema import apply_schema
        from .migrations import run_migrations
        
        # Check if schema_migrations table exists
        result = self._connection.execute("""
            SELECT count(*) FROM information_schema.tables 
            WHERE table_name = 'schema_migrations'
        """).fetchone()
        
        if result[0] == 0:
            # New database - apply full schema
            apply_schema(self._connection)
        else:
            # Existing database - run any pending migrations
            run_migrations(self._connection)
    
    def close(self) -> None:
        """Close the database connection."""
        if self._connection:
            self._connection.close()
            self._connection = None
    
    @classmethod
    def get_instance(cls, db_path: Optional[Path] = None) -> 'DatabaseConnection':
        """
        Get singleton database connection instance.
        
        Args:
            db_path: Override default path (only used on first call).
            
        Returns:
            DatabaseConnection singleton.
        """
        if cls._instance is None:
            cls._instance = cls(db_path)
        return cls._instance
    
    @classmethod
    def reset(cls) -> None:
        """Reset singleton (for testing)."""
        if cls._instance:
            cls._instance.close()
        cls._instance = None


def get_connection() -> duckdb.DuckDBPyConnection:
    """
    Convenience function to get database connection.
    
    Returns:
        Active DuckDB connection.
    """
    return DatabaseConnection.get_instance().connect()
```

### Step 3: Implement schema.py

Create comprehensive DDL for all canonical and state management tables. Include:

1. **Standard provenance columns** for all canonical tables:
   ```sql
   created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   source_type         VARCHAR,  -- 'generated', 'loaded', 'derived'
   source_system       VARCHAR,  -- 'patientsim', 'membersim', etc.
   skill_used          VARCHAR,  -- 'diabetes-management', etc.
   generation_seed     INTEGER
   ```

2. **All canonical entity tables** matching the JSON schemas in data-models.md

3. **State management tables**: cohorts, cohort_entities, cohort_tags

4. **Schema migrations table** for version tracking

5. **Appropriate indexes** for common query patterns

### Step 4: Implement migrations.py

```python
"""
Schema migration framework for HealthSim.

Migrations are applied at connection time, ensuring the database
schema is always up-to-date.
"""

from typing import List, Tuple
import duckdb

# Migration definitions: (version, description, sql)
MIGRATIONS: List[Tuple[str, str, str]] = [
    # Initial schema is applied via schema.py, not migrations
    # Future migrations go here:
    # ("1.1", "Add index on patients.ssn", "CREATE INDEX idx_patients_ssn ON patients(ssn)"),
]


def get_current_version(conn: duckdb.DuckDBPyConnection) -> str:
    """Get the current schema version from the database."""
    result = conn.execute("""
        SELECT version FROM schema_migrations 
        ORDER BY applied_at DESC LIMIT 1
    """).fetchone()
    return result[0] if result else "1.0"


def run_migrations(conn: duckdb.DuckDBPyConnection) -> List[str]:
    """
    Run any pending migrations.
    
    Returns:
        List of applied migration versions.
    """
    current = get_current_version(conn)
    applied = []
    
    for version, description, sql in MIGRATIONS:
        if version > current:
            conn.execute(sql)
            conn.execute("""
                INSERT INTO schema_migrations (version, description)
                VALUES (?, ?)
            """, [version, description])
            applied.append(version)
    
    return applied
```

### Step 5: Implement queries.py

Common query helpers for typical operations:
- `get_patient_by_id()`
- `get_patients_in_cohort()`
- `count_entities_by_type()`
- `get_cohort_summary()`

### Step 6: Write Tests

Create comprehensive tests in `packages/core/tests/db/`:

**test_connection.py**:
- Test database auto-creation
- Test connection singleton
- Test path configuration
- Test reset/reconnect

**test_schema.py**:
- Test schema application on new database
- Test all tables created
- Test indexes created
- Test provenance columns present

**test_migrations.py**:
- Test migration tracking
- Test version detection
- Test migration application order

### Step 7: Update __init__.py exports

```python
"""HealthSim Database Module."""

from .connection import (
    DatabaseConnection,
    get_connection,
    DEFAULT_DB_PATH,
)
from .schema import (
    apply_schema,
    SCHEMA_VERSION,
)
from .migrations import (
    run_migrations,
    get_current_version,
)

__all__ = [
    'DatabaseConnection',
    'get_connection',
    'DEFAULT_DB_PATH',
    'apply_schema',
    'SCHEMA_VERSION',
    'run_migrations',
    'get_current_version',
]
```

### Step 8: Verify and Test

```bash
# Run the new tests
cd packages/core
source .venv/bin/activate
pytest tests/db/ -v

# Run all tests to ensure no regressions
pytest tests/ -v
```

---

## Post-Flight Checklist

- [ ] All new tests pass
- [ ] All existing tests still pass (476+)
- [ ] Database auto-creates at `~/.healthsim/healthsim.duckdb`
- [ ] All canonical tables created with correct columns
- [ ] Provenance columns present on all canonical tables
- [ ] State management tables created
- [ ] Schema version tracking works
- [ ] No linting errors

---

## Commit

```bash
git add -A
git commit -m "[Database] Add DuckDB database module with schema and migrations

- Create packages/core/healthsim/db/ module
- Add connection management with auto-creation
- Define canonical table schemas (patients, encounters, etc.)
- Define state management schemas (cohorts, cohort_entities)
- Add migration framework for schema versioning
- Add comprehensive tests for db module

Part of: DuckDB Unified Data Architecture initiative"

git push
```

---

## Update MASTER-PLAN.md

Mark SESSION-01 as complete with commit hash.

---

## Update CURRENT-WORK.md

```markdown
## Active Initiative

**DuckDB Unified Data Architecture** - Phase 1
- Session 01: Database Foundation ✅ Complete (commit: XXXXXX)
- Session 02: PopulationSim Migration - Next

## Next Session Should
1. Start SESSION-02 from docs/initiatives/duckdb-architecture/SESSION-02-populationsim-migration.md
```

---

## Success Criteria

✅ Session complete when:
1. `packages/core/healthsim/db/` module exists and is importable
2. `from healthsim.db import get_connection` works
3. Database auto-creates on first connection
4. All schema tables exist with correct structure
5. New tests pass
6. All existing tests pass
7. Committed and pushed

---

## Troubleshooting

**DuckDB import fails:**
```bash
pip install duckdb --break-system-packages
```

**Tests can't find module:**
```bash
pip install -e . --break-system-packages
```

**Schema application fails:**
- Check SQL syntax in schema.py
- Ensure all referenced tables exist before foreign keys

---

## Next Session

Proceed to [SESSION-02: PopulationSim Migration](SESSION-02-populationsim-migration.md)
