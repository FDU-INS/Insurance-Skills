"""
Schema migration framework for HealthSim.

Migrations are applied at connection time, ensuring the database
schema is always up-to-date.
"""

from typing import List, Tuple
import duckdb

# Migration definitions: (version, description, sql)
# Format: Each migration is a tuple of (version, description, sql_statement)
# Versions should be comparable strings (e.g., "1.1", "1.2", "2.0")
MIGRATIONS: List[Tuple[str, str, str]] = [
    # Initial schema is applied via schema.py, not migrations
    # Add sequences for auto-increment IDs (fixes databases created before sequences added)
    ("1.1", "Add sequences for scenario_entities and scenario_tags", """
        CREATE SEQUENCE IF NOT EXISTS scenario_entities_seq START 1;
        CREATE SEQUENCE IF NOT EXISTS scenario_tags_seq START 1;
    """),
    
    # Legacy migration: Add cohort_id columns (renamed to cohort_id in 1.5)
    # For new databases, schema.py already uses cohort_id
    ("1.2", "Add cohort_id columns to canonical tables for auto-persist", """
        -- PatientSim tables
        ALTER TABLE patients ADD COLUMN IF NOT EXISTS cohort_id VARCHAR;
        ALTER TABLE encounters ADD COLUMN IF NOT EXISTS cohort_id VARCHAR;
        ALTER TABLE diagnoses ADD COLUMN IF NOT EXISTS cohort_id VARCHAR;
        ALTER TABLE medications ADD COLUMN IF NOT EXISTS cohort_id VARCHAR;
        ALTER TABLE lab_results ADD COLUMN IF NOT EXISTS cohort_id VARCHAR;
        ALTER TABLE vital_signs ADD COLUMN IF NOT EXISTS cohort_id VARCHAR;
        ALTER TABLE orders ADD COLUMN IF NOT EXISTS cohort_id VARCHAR;
        ALTER TABLE clinical_notes ADD COLUMN IF NOT EXISTS cohort_id VARCHAR;
        
        -- MemberSim tables
        ALTER TABLE members ADD COLUMN IF NOT EXISTS cohort_id VARCHAR;
        ALTER TABLE claims ADD COLUMN IF NOT EXISTS cohort_id VARCHAR;
        ALTER TABLE claim_lines ADD COLUMN IF NOT EXISTS cohort_id VARCHAR;
        
        -- RxMemberSim tables
        ALTER TABLE prescriptions ADD COLUMN IF NOT EXISTS cohort_id VARCHAR;
        ALTER TABLE pharmacy_claims ADD COLUMN IF NOT EXISTS cohort_id VARCHAR;
        
        -- TrialSim tables
        ALTER TABLE subjects ADD COLUMN IF NOT EXISTS cohort_id VARCHAR;
        ALTER TABLE trial_visits ADD COLUMN IF NOT EXISTS cohort_id VARCHAR;
        ALTER TABLE adverse_events ADD COLUMN IF NOT EXISTS cohort_id VARCHAR;
        ALTER TABLE exposures ADD COLUMN IF NOT EXISTS cohort_id VARCHAR;
        
        -- Indexes for scenario filtering
        CREATE INDEX IF NOT EXISTS idx_patients_scenario ON patients(cohort_id);
        CREATE INDEX IF NOT EXISTS idx_encounters_scenario ON encounters(cohort_id);
        CREATE INDEX IF NOT EXISTS idx_diagnoses_scenario ON diagnoses(cohort_id);
        CREATE INDEX IF NOT EXISTS idx_medications_scenario ON medications(cohort_id);
        CREATE INDEX IF NOT EXISTS idx_lab_results_scenario ON lab_results(cohort_id);
        CREATE INDEX IF NOT EXISTS idx_vital_signs_scenario ON vital_signs(cohort_id);
        CREATE INDEX IF NOT EXISTS idx_orders_scenario ON orders(cohort_id);
        CREATE INDEX IF NOT EXISTS idx_clinical_notes_scenario ON clinical_notes(cohort_id);
        CREATE INDEX IF NOT EXISTS idx_members_scenario ON members(cohort_id);
        CREATE INDEX IF NOT EXISTS idx_claims_scenario ON claims(cohort_id);
        CREATE INDEX IF NOT EXISTS idx_claim_lines_scenario ON claim_lines(cohort_id);
        CREATE INDEX IF NOT EXISTS idx_prescriptions_scenario ON prescriptions(cohort_id);
        CREATE INDEX IF NOT EXISTS idx_pharmacy_claims_scenario ON pharmacy_claims(cohort_id);
        CREATE INDEX IF NOT EXISTS idx_subjects_scenario ON subjects(cohort_id);
        CREATE INDEX IF NOT EXISTS idx_trial_visits_scenario ON trial_visits(cohort_id);
        CREATE INDEX IF NOT EXISTS idx_adverse_events_scenario ON adverse_events(cohort_id);
        CREATE INDEX IF NOT EXISTS idx_exposures_scenario ON exposures(cohort_id);
    """),
    
    # Rename cohort_id to id in scenarios table for consistency
    ("1.4", "Rename scenarios.cohort_id to scenarios.id for consistency", """
        -- DuckDB doesn't support RENAME COLUMN directly, so we recreate the table
        -- Step 1: Create new table with correct schema
        CREATE TABLE scenarios_new (
            id              VARCHAR PRIMARY KEY,
            name            VARCHAR NOT NULL UNIQUE,
            description     VARCHAR,
            created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            metadata        JSON
        );
        
        -- Step 2: Copy data from old table
        INSERT INTO scenarios_new (id, name, description, created_at, updated_at, metadata)
        SELECT cohort_id, name, description, created_at, updated_at, metadata
        FROM scenarios;
        
        -- Step 3: Drop foreign key constraints by recreating child tables
        -- Note: DuckDB doesn't enforce FK constraints strictly, but we update for correctness
        
        -- Recreate scenario_entities with updated FK reference
        CREATE TABLE scenario_entities_new (
            id              INTEGER PRIMARY KEY,
            cohort_id     VARCHAR NOT NULL,
            entity_type     VARCHAR NOT NULL,
            entity_id       VARCHAR NOT NULL,
            entity_data     JSON,
            created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(cohort_id, entity_type, entity_id)
        );
        INSERT INTO scenario_entities_new SELECT * FROM scenario_entities;
        DROP TABLE scenario_entities;
        ALTER TABLE scenario_entities_new RENAME TO scenario_entities;
        
        -- Recreate scenario_tags with updated FK reference  
        CREATE TABLE scenario_tags_new (
            id              INTEGER PRIMARY KEY,
            cohort_id     VARCHAR NOT NULL,
            tag             VARCHAR NOT NULL,
            UNIQUE(cohort_id, tag)
        );
        INSERT INTO scenario_tags_new SELECT * FROM scenario_tags;
        DROP TABLE scenario_tags;
        ALTER TABLE scenario_tags_new RENAME TO scenario_tags;
        
        -- Step 4: Drop old scenarios table and rename new one
        DROP TABLE scenarios;
        ALTER TABLE scenarios_new RENAME TO scenarios;
        
        -- Step 5: Recreate indexes
        CREATE INDEX IF NOT EXISTS idx_scenario_entities_scenario ON scenario_entities(cohort_id);
        CREATE INDEX IF NOT EXISTS idx_scenario_entities_type ON scenario_entities(entity_type);
        CREATE INDEX IF NOT EXISTS idx_scenario_tags_scenario ON scenario_tags(cohort_id);
        CREATE INDEX IF NOT EXISTS idx_scenario_tags_tag ON scenario_tags(tag);
    """),
    
    # Rename scenario to cohort throughout the schema
    ("1.5", "Rename scenario to cohort throughout schema", """
        -- Create new cohort sequences
        CREATE SEQUENCE IF NOT EXISTS cohort_entities_seq START 1;
        CREATE SEQUENCE IF NOT EXISTS cohort_tags_seq START 1;
        
        -- Create cohorts table (copy of scenarios)
        CREATE TABLE IF NOT EXISTS cohorts (
            id              VARCHAR PRIMARY KEY,
            name            VARCHAR NOT NULL UNIQUE,
            description     VARCHAR,
            created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            metadata        JSON
        );
        INSERT INTO cohorts SELECT * FROM scenarios WHERE NOT EXISTS (SELECT 1 FROM cohorts LIMIT 1);
        
        -- Create cohort_entities table (copy of scenario_entities)
        CREATE TABLE IF NOT EXISTS cohort_entities (
            id              INTEGER PRIMARY KEY,
            cohort_id       VARCHAR NOT NULL,
            entity_type     VARCHAR NOT NULL,
            entity_id       VARCHAR NOT NULL,
            entity_data     JSON,
            created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(cohort_id, entity_type, entity_id)
        );
        INSERT INTO cohort_entities (id, cohort_id, entity_type, entity_id, entity_data, created_at)
        SELECT id, scenario_id, entity_type, entity_id, entity_data, created_at 
        FROM scenario_entities WHERE NOT EXISTS (SELECT 1 FROM cohort_entities LIMIT 1);
        
        -- Create cohort_tags table (copy of scenario_tags)
        CREATE TABLE IF NOT EXISTS cohort_tags (
            id              INTEGER PRIMARY KEY,
            cohort_id       VARCHAR NOT NULL,
            tag             VARCHAR NOT NULL,
            UNIQUE(cohort_id, tag)
        );
        INSERT INTO cohort_tags (id, cohort_id, tag)
        SELECT id, scenario_id, tag FROM scenario_tags WHERE NOT EXISTS (SELECT 1 FROM cohort_tags LIMIT 1);
        
        -- Add cohort_id column to all canonical tables (alongside cohort_id for backward compat)
        ALTER TABLE patients ADD COLUMN IF NOT EXISTS cohort_id VARCHAR;
        ALTER TABLE encounters ADD COLUMN IF NOT EXISTS cohort_id VARCHAR;
        ALTER TABLE diagnoses ADD COLUMN IF NOT EXISTS cohort_id VARCHAR;
        ALTER TABLE medications ADD COLUMN IF NOT EXISTS cohort_id VARCHAR;
        ALTER TABLE lab_results ADD COLUMN IF NOT EXISTS cohort_id VARCHAR;
        ALTER TABLE vital_signs ADD COLUMN IF NOT EXISTS cohort_id VARCHAR;
        ALTER TABLE orders ADD COLUMN IF NOT EXISTS cohort_id VARCHAR;
        ALTER TABLE clinical_notes ADD COLUMN IF NOT EXISTS cohort_id VARCHAR;
        ALTER TABLE members ADD COLUMN IF NOT EXISTS cohort_id VARCHAR;
        ALTER TABLE claims ADD COLUMN IF NOT EXISTS cohort_id VARCHAR;
        ALTER TABLE claim_lines ADD COLUMN IF NOT EXISTS cohort_id VARCHAR;
        ALTER TABLE prescriptions ADD COLUMN IF NOT EXISTS cohort_id VARCHAR;
        ALTER TABLE pharmacy_claims ADD COLUMN IF NOT EXISTS cohort_id VARCHAR;
        ALTER TABLE subjects ADD COLUMN IF NOT EXISTS cohort_id VARCHAR;
        ALTER TABLE trial_visits ADD COLUMN IF NOT EXISTS cohort_id VARCHAR;
        ALTER TABLE adverse_events ADD COLUMN IF NOT EXISTS cohort_id VARCHAR;
        ALTER TABLE exposures ADD COLUMN IF NOT EXISTS cohort_id VARCHAR;
        
        -- Copy cohort_id values to cohort_id
        UPDATE patients SET cohort_id = cohort_id WHERE cohort_id IS NULL AND cohort_id IS NOT NULL;
        UPDATE encounters SET cohort_id = cohort_id WHERE cohort_id IS NULL AND cohort_id IS NOT NULL;
        UPDATE diagnoses SET cohort_id = cohort_id WHERE cohort_id IS NULL AND cohort_id IS NOT NULL;
        UPDATE medications SET cohort_id = cohort_id WHERE cohort_id IS NULL AND cohort_id IS NOT NULL;
        UPDATE lab_results SET cohort_id = cohort_id WHERE cohort_id IS NULL AND cohort_id IS NOT NULL;
        UPDATE vital_signs SET cohort_id = cohort_id WHERE cohort_id IS NULL AND cohort_id IS NOT NULL;
        UPDATE orders SET cohort_id = cohort_id WHERE cohort_id IS NULL AND cohort_id IS NOT NULL;
        UPDATE clinical_notes SET cohort_id = cohort_id WHERE cohort_id IS NULL AND cohort_id IS NOT NULL;
        UPDATE members SET cohort_id = cohort_id WHERE cohort_id IS NULL AND cohort_id IS NOT NULL;
        UPDATE claims SET cohort_id = cohort_id WHERE cohort_id IS NULL AND cohort_id IS NOT NULL;
        UPDATE claim_lines SET cohort_id = cohort_id WHERE cohort_id IS NULL AND cohort_id IS NOT NULL;
        UPDATE prescriptions SET cohort_id = cohort_id WHERE cohort_id IS NULL AND cohort_id IS NOT NULL;
        UPDATE pharmacy_claims SET cohort_id = cohort_id WHERE cohort_id IS NULL AND cohort_id IS NOT NULL;
        UPDATE subjects SET cohort_id = cohort_id WHERE cohort_id IS NULL AND cohort_id IS NOT NULL;
        UPDATE trial_visits SET cohort_id = cohort_id WHERE cohort_id IS NULL AND cohort_id IS NOT NULL;
        UPDATE adverse_events SET cohort_id = cohort_id WHERE cohort_id IS NULL AND cohort_id IS NOT NULL;
        UPDATE exposures SET cohort_id = cohort_id WHERE cohort_id IS NULL AND cohort_id IS NOT NULL;
        
        -- Create indexes on cohort_id columns
        CREATE INDEX IF NOT EXISTS idx_patients_cohort ON patients(cohort_id);
        CREATE INDEX IF NOT EXISTS idx_encounters_cohort ON encounters(cohort_id);
        CREATE INDEX IF NOT EXISTS idx_diagnoses_cohort ON diagnoses(cohort_id);
        CREATE INDEX IF NOT EXISTS idx_medications_cohort ON medications(cohort_id);
        CREATE INDEX IF NOT EXISTS idx_lab_results_cohort ON lab_results(cohort_id);
        CREATE INDEX IF NOT EXISTS idx_vital_signs_cohort ON vital_signs(cohort_id);
        CREATE INDEX IF NOT EXISTS idx_orders_cohort ON orders(cohort_id);
        CREATE INDEX IF NOT EXISTS idx_clinical_notes_cohort ON clinical_notes(cohort_id);
        CREATE INDEX IF NOT EXISTS idx_members_cohort ON members(cohort_id);
        CREATE INDEX IF NOT EXISTS idx_claims_cohort ON claims(cohort_id);
        CREATE INDEX IF NOT EXISTS idx_claim_lines_cohort ON claim_lines(cohort_id);
        CREATE INDEX IF NOT EXISTS idx_prescriptions_cohort ON prescriptions(cohort_id);
        CREATE INDEX IF NOT EXISTS idx_pharmacy_claims_cohort ON pharmacy_claims(cohort_id);
        CREATE INDEX IF NOT EXISTS idx_subjects_cohort ON subjects(cohort_id);
        CREATE INDEX IF NOT EXISTS idx_trial_visits_cohort ON trial_visits(cohort_id);
        CREATE INDEX IF NOT EXISTS idx_adverse_events_cohort ON adverse_events(cohort_id);
        CREATE INDEX IF NOT EXISTS idx_exposures_cohort ON exposures(cohort_id);
        
        -- Create indexes on cohort state tables
        CREATE INDEX IF NOT EXISTS idx_cohort_entities_cohort ON cohort_entities(cohort_id);
        CREATE INDEX IF NOT EXISTS idx_cohort_entities_type ON cohort_entities(entity_type);
        CREATE INDEX IF NOT EXISTS idx_cohort_tags_cohort ON cohort_tags(cohort_id);
        CREATE INDEX IF NOT EXISTS idx_cohort_tags_tag ON cohort_tags(tag);
    """),
    
    # Clean up legacy scenario indexes (now redundant with cohort indexes)
    ("1.6", "Drop legacy idx_*_scenario indexes (replaced by idx_*_cohort)", """
        -- Drop legacy scenario-named indexes on entity tables
        -- These are redundant with the idx_*_cohort indexes created in 1.5
        DROP INDEX IF EXISTS idx_patients_scenario;
        DROP INDEX IF EXISTS idx_encounters_scenario;
        DROP INDEX IF EXISTS idx_diagnoses_scenario;
        DROP INDEX IF EXISTS idx_medications_scenario;
        DROP INDEX IF EXISTS idx_lab_results_scenario;
        DROP INDEX IF EXISTS idx_vital_signs_scenario;
        DROP INDEX IF EXISTS idx_orders_scenario;
        DROP INDEX IF EXISTS idx_clinical_notes_scenario;
        DROP INDEX IF EXISTS idx_members_scenario;
        DROP INDEX IF EXISTS idx_claims_scenario;
        DROP INDEX IF EXISTS idx_claim_lines_scenario;
        DROP INDEX IF EXISTS idx_prescriptions_scenario;
        DROP INDEX IF EXISTS idx_pharmacy_claims_scenario;
        DROP INDEX IF EXISTS idx_subjects_scenario;
        DROP INDEX IF EXISTS idx_trial_visits_scenario;
        DROP INDEX IF EXISTS idx_adverse_events_scenario;
        DROP INDEX IF EXISTS idx_exposures_scenario;
        
        -- Drop legacy scenario-named indexes on state tables
        DROP INDEX IF EXISTS idx_scenario_entities_scenario;
        DROP INDEX IF EXISTS idx_scenario_entities_type;
        DROP INDEX IF EXISTS idx_scenario_tags_scenario;
        DROP INDEX IF EXISTS idx_scenario_tags_tag;
    """),
]


def get_current_version(conn: duckdb.DuckDBPyConnection) -> str:
    """
    Get the current schema version from the database.
    
    Args:
        conn: DuckDB connection to check.
        
    Returns:
        Current schema version string.
    """
    result = conn.execute("""
        SELECT version FROM schema_migrations 
        ORDER BY applied_at DESC LIMIT 1
    """).fetchone()
    return result[0] if result else "0.0"


def get_applied_migrations(conn: duckdb.DuckDBPyConnection) -> List[str]:
    """
    Get list of all applied migration versions.
    
    Args:
        conn: DuckDB connection to check.
        
    Returns:
        List of applied version strings.
    """
    result = conn.execute("""
        SELECT version FROM schema_migrations ORDER BY applied_at
    """).fetchall()
    return [row[0] for row in result]


def run_migrations(conn: duckdb.DuckDBPyConnection) -> List[str]:
    """
    Run any pending migrations.
    
    Args:
        conn: DuckDB connection to apply migrations to.
        
    Returns:
        List of applied migration versions.
    """
    current = get_current_version(conn)
    applied = []
    
    for version, description, sql in MIGRATIONS:
        if version > current:
            # Execute the migration
            conn.execute(sql)
            
            # Record the migration
            conn.execute("""
                INSERT INTO schema_migrations (version, description)
                VALUES (?, ?)
            """, [version, description])
            
            applied.append(version)
    
    return applied


def get_pending_migrations(conn: duckdb.DuckDBPyConnection) -> List[Tuple[str, str]]:
    """
    Get list of pending migrations (not yet applied).
    
    Args:
        conn: DuckDB connection to check.
        
    Returns:
        List of (version, description) tuples for pending migrations.
    """
    current = get_current_version(conn)
    return [(v, d) for v, d, _ in MIGRATIONS if v > current]
