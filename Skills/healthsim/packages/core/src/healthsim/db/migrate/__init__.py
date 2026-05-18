"""
Migration tools for HealthSim database.

Provides utilities to migrate from previous storage formats
(JSON files) to the unified DuckDB database.
"""

from .json_cohorts import (
    MigrationResult,
    discover_json_cohorts,
    migrate_cohort,
    migrate_all_cohorts,
    backup_json_cohorts,
    verify_migration,
    LEGACY_PATH,
    BACKUP_PATH,
)

__all__ = [
    "MigrationResult",
    "discover_json_cohorts",
    "migrate_cohort",
    "migrate_all_cohorts",
    "backup_json_cohorts",
    "verify_migration",
    "LEGACY_PATH",
    "BACKUP_PATH",
]
