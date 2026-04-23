"""
HealthSim Database Module.

Provides DuckDB-based storage for canonical entities, state management,
and future analytics capabilities.

Usage:
    from healthsim.db import get_connection, SCHEMA_VERSION
    
    conn = get_connection()
    conn.execute("SELECT * FROM patients")
"""

from .connection import (
    DatabaseConnection,
    get_connection,
    get_read_only_connection,
    DEFAULT_DB_PATH,
)
from .schema import (
    apply_schema,
    SCHEMA_VERSION,
    get_canonical_tables,
    get_state_tables,
    get_system_tables,
)
from .migrations import (
    run_migrations,
    get_current_version,
    get_applied_migrations,
    get_pending_migrations,
)
from .queries import (
    get_patient_by_id,
    get_patient_by_mrn,
    get_patients_in_cohort,
    count_entities_by_type,
    get_cohort_summary,
    list_cohorts,
    cohort_exists,
    get_schema_version,
)
from .reference import (
    import_all_reference_data,
    get_reference_status,
    is_reference_data_loaded,
    REFERENCE_TABLES,
)
from .lfs_check import (
    is_lfs_pointer,
    check_duckdb_file,
    require_duckdb,
    get_db_connection,
    LFSError,
)

__all__ = [
    # Connection management
    'DatabaseConnection',
    'get_connection',
    'get_read_only_connection',
    'DEFAULT_DB_PATH',
    
    # Schema
    'apply_schema',
    'SCHEMA_VERSION',
    'get_canonical_tables',
    'get_state_tables',
    'get_system_tables',
    
    # Migrations
    'run_migrations',
    'get_current_version',
    'get_applied_migrations',
    'get_pending_migrations',
    
    # Queries
    'get_patient_by_id',
    'get_patient_by_mrn',
    'get_patients_in_cohort',
    'count_entities_by_type',
    'get_cohort_summary',
    'list_cohorts',
    'cohort_exists',
    'get_schema_version',
    
    # Reference Data
    'import_all_reference_data',
    'get_reference_status',
    'is_reference_data_loaded',
    'REFERENCE_TABLES',
    
    # LFS Check
    'is_lfs_pointer',
    'check_duckdb_file',
    'require_duckdb',
    'get_db_connection',
    'LFSError',
]
