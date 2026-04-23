"""
Database schema definitions for HealthSim.

Defines DDL for all canonical tables, state management tables,
and system tables. Schema follows the data models in references/data-models.md.
"""

from typing import List
import duckdb

# Current schema version
SCHEMA_VERSION = "1.7"

# Standard provenance columns included in all canonical tables
PROVENANCE_COLUMNS = """
    cohort_id           VARCHAR,   -- Links to cohorts table for auto-persist
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source_type         VARCHAR,   -- 'generated', 'loaded', 'derived'
    source_system       VARCHAR,   -- 'patientsim', 'membersim', etc.
    skill_used          VARCHAR,   -- 'diabetes-management', etc.
    generation_seed     INTEGER
"""

# ============================================================================
# SYSTEM TABLES
# ============================================================================

SCHEMA_MIGRATIONS_DDL = """
CREATE TABLE IF NOT EXISTS schema_migrations (
    version         VARCHAR PRIMARY KEY,
    description     VARCHAR,
    applied_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

# ============================================================================
# STATE MANAGEMENT TABLES  
# ============================================================================

# Sequences for auto-increment IDs
COHORT_ENTITIES_SEQ_DDL = """
CREATE SEQUENCE IF NOT EXISTS cohort_entities_seq START 1;
"""

COHORT_TAGS_SEQ_DDL = """
CREATE SEQUENCE IF NOT EXISTS cohort_tags_seq START 1;
"""

COHORTS_DDL = """
CREATE TABLE IF NOT EXISTS cohorts (
    id              VARCHAR PRIMARY KEY,
    name            VARCHAR NOT NULL UNIQUE,
    description     VARCHAR,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata        JSON
);
"""

COHORT_ENTITIES_DDL = """
CREATE TABLE IF NOT EXISTS cohort_entities (
    id              INTEGER PRIMARY KEY DEFAULT nextval('cohort_entities_seq'),
    cohort_id       VARCHAR NOT NULL REFERENCES cohorts(id),
    entity_type     VARCHAR NOT NULL,  -- 'patient', 'encounter', 'claim', etc.
    entity_id       VARCHAR NOT NULL,
    entity_data     JSON,              -- Full entity JSON for export
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(cohort_id, entity_type, entity_id)
);
"""

COHORT_TAGS_DDL = """
CREATE TABLE IF NOT EXISTS cohort_tags (
    id              INTEGER PRIMARY KEY DEFAULT nextval('cohort_tags_seq'),
    cohort_id       VARCHAR NOT NULL REFERENCES cohorts(id),
    tag             VARCHAR NOT NULL,
    UNIQUE(cohort_id, tag)
);
"""

# ============================================================================
# PROFILE MANAGEMENT TABLES
# ============================================================================

PROFILES_SEQ_DDL = """
CREATE SEQUENCE IF NOT EXISTS profiles_seq START 1;
"""

PROFILES_DDL = """
CREATE TABLE IF NOT EXISTS profiles (
    id              VARCHAR PRIMARY KEY,
    name            VARCHAR NOT NULL UNIQUE,
    description     VARCHAR,
    version         INTEGER DEFAULT 1,
    profile_spec    JSON NOT NULL,          -- Full ProfileSpecification as JSON
    product         VARCHAR,                -- 'patientsim', 'membersim', etc.
    tags            JSON,                   -- Array of tags for filtering
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata        JSON                    -- Additional metadata
);
"""

PROFILE_EXECUTIONS_DDL = """
CREATE TABLE IF NOT EXISTS profile_executions (
    id              INTEGER PRIMARY KEY DEFAULT nextval('profiles_seq'),
    profile_id      VARCHAR NOT NULL REFERENCES profiles(id),
    cohort_id       VARCHAR REFERENCES cohorts(id),
    executed_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    seed            INTEGER,                -- Random seed used
    count           INTEGER,                -- Number of entities generated
    duration_ms     INTEGER,                -- Execution time in milliseconds
    status          VARCHAR DEFAULT 'completed',  -- 'completed', 'failed', 'partial'
    error_message   VARCHAR,                -- Error details if failed
    metadata        JSON                    -- Execution metadata (timings, etc.)
);
"""

# ============================================================================
# JOURNEY MANAGEMENT TABLES
# ============================================================================

JOURNEYS_SEQ_DDL = """
CREATE SEQUENCE IF NOT EXISTS journeys_seq START 1;
"""

JOURNEYS_DDL = """
CREATE TABLE IF NOT EXISTS journeys (
    id              VARCHAR PRIMARY KEY,
    name            VARCHAR NOT NULL UNIQUE,
    description     VARCHAR,
    version         INTEGER DEFAULT 1,
    journey_spec    JSON NOT NULL,          -- Full JourneySpecification as JSON
    products        JSON,                   -- Array of products this applies to
    tags            JSON,                   -- Array of tags for filtering
    duration_days   INTEGER,                -- Journey duration
    event_count     INTEGER,                -- Number of events in journey
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata        JSON                    -- Additional metadata
);
"""

JOURNEY_EXECUTIONS_DDL = """
CREATE TABLE IF NOT EXISTS journey_executions (
    id              INTEGER PRIMARY KEY DEFAULT nextval('journeys_seq'),
    journey_id      VARCHAR NOT NULL REFERENCES journeys(id),
    profile_id      VARCHAR REFERENCES profiles(id),
    cohort_id       VARCHAR REFERENCES cohorts(id),
    entity_id       VARCHAR,                -- The entity (patient, member) this was executed for
    executed_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    start_date      DATE,                   -- Journey start date
    end_date        DATE,                   -- Journey end date
    events_generated INTEGER,               -- Number of events generated
    duration_ms     INTEGER,                -- Execution time in milliseconds
    status          VARCHAR DEFAULT 'completed',
    error_message   VARCHAR,
    metadata        JSON
);
"""

# ============================================================================
# CANONICAL TABLES - PatientSim
# ============================================================================

PATIENTS_DDL = f"""
CREATE TABLE IF NOT EXISTS patients (
    id              VARCHAR PRIMARY KEY,
    mrn             VARCHAR NOT NULL,
    ssn             VARCHAR,
    given_name      VARCHAR NOT NULL,
    middle_name     VARCHAR,
    family_name     VARCHAR NOT NULL,
    suffix          VARCHAR,
    prefix          VARCHAR,
    birth_date      DATE NOT NULL,
    gender          VARCHAR NOT NULL,
    race            VARCHAR,
    ethnicity       VARCHAR,
    language        VARCHAR DEFAULT 'en',
    street_address  VARCHAR,
    street_address_2 VARCHAR,
    city            VARCHAR,
    state           VARCHAR,
    postal_code     VARCHAR,
    country         VARCHAR DEFAULT 'US',
    phone           VARCHAR,
    phone_mobile    VARCHAR,
    email           VARCHAR,
    deceased        BOOLEAN DEFAULT FALSE,
    death_date      DATE,
    {PROVENANCE_COLUMNS}
);
"""

ENCOUNTERS_DDL = f"""
CREATE TABLE IF NOT EXISTS encounters (
    encounter_id    VARCHAR PRIMARY KEY,
    patient_mrn     VARCHAR NOT NULL,
    class_code      VARCHAR NOT NULL,  -- I, O, E, U, OBS
    status          VARCHAR NOT NULL,
    admission_time  TIMESTAMP NOT NULL,
    discharge_time  TIMESTAMP,
    facility        VARCHAR,
    department      VARCHAR,
    room            VARCHAR,
    bed             VARCHAR,
    chief_complaint VARCHAR,
    admitting_diagnosis VARCHAR,
    discharge_disposition VARCHAR,
    attending_physician VARCHAR,
    admitting_physician VARCHAR,
    {PROVENANCE_COLUMNS}
);
"""

DIAGNOSES_DDL = f"""
CREATE TABLE IF NOT EXISTS diagnoses (
    id              VARCHAR PRIMARY KEY,
    code            VARCHAR NOT NULL,
    description     VARCHAR,
    type            VARCHAR DEFAULT 'final',  -- admitting, working, final, differential
    patient_mrn     VARCHAR NOT NULL,
    encounter_id    VARCHAR,
    diagnosed_date  DATE NOT NULL,
    resolved_date   DATE,
    {PROVENANCE_COLUMNS}
);
"""

MEDICATIONS_DDL = f"""
CREATE TABLE IF NOT EXISTS medications (
    id              VARCHAR PRIMARY KEY,
    name            VARCHAR NOT NULL,
    code            VARCHAR,           -- RxNorm or NDC
    dose            VARCHAR NOT NULL,
    route           VARCHAR NOT NULL,
    frequency       VARCHAR NOT NULL,
    patient_mrn     VARCHAR NOT NULL,
    encounter_id    VARCHAR,
    start_date      TIMESTAMP NOT NULL,
    end_date        TIMESTAMP,
    status          VARCHAR DEFAULT 'active',
    prescriber      VARCHAR,
    indication      VARCHAR,
    {PROVENANCE_COLUMNS}
);
"""

LAB_RESULTS_DDL = f"""
CREATE TABLE IF NOT EXISTS lab_results (
    id              VARCHAR PRIMARY KEY,
    test_name       VARCHAR NOT NULL,
    loinc_code      VARCHAR,
    value           VARCHAR NOT NULL,
    unit            VARCHAR,
    reference_range VARCHAR,
    abnormal_flag   VARCHAR,  -- H, L, HH, LL, A, N
    patient_mrn     VARCHAR NOT NULL,
    encounter_id    VARCHAR,
    collected_time  TIMESTAMP NOT NULL,
    resulted_time   TIMESTAMP,
    performing_lab  VARCHAR,
    ordering_provider VARCHAR,
    {PROVENANCE_COLUMNS}
);
"""

VITAL_SIGNS_DDL = f"""
CREATE TABLE IF NOT EXISTS vital_signs (
    id              VARCHAR PRIMARY KEY,
    patient_mrn     VARCHAR NOT NULL,
    encounter_id    VARCHAR,
    observation_time TIMESTAMP NOT NULL,
    temperature     DECIMAL(5,2),
    heart_rate      INTEGER,
    respiratory_rate INTEGER,
    systolic_bp     INTEGER,
    diastolic_bp    INTEGER,
    spo2            INTEGER,
    height_cm       DECIMAL(5,2),
    weight_kg       DECIMAL(6,2),
    {PROVENANCE_COLUMNS}
);
"""

ORDERS_DDL = f"""
CREATE TABLE IF NOT EXISTS orders (
    order_id        VARCHAR PRIMARY KEY,
    patient_mrn     VARCHAR NOT NULL,
    encounter_id    VARCHAR,
    order_type      VARCHAR NOT NULL,  -- LAB, RAD, MEDICATION, PROCEDURE
    code            VARCHAR NOT NULL,
    code_system     VARCHAR DEFAULT 'CPT',
    description     VARCHAR,
    priority        VARCHAR DEFAULT 'routine',
    status          VARCHAR DEFAULT 'new',
    ordered_datetime TIMESTAMP NOT NULL,
    scheduled_datetime TIMESTAMP,
    collected_datetime TIMESTAMP,
    resulted_datetime TIMESTAMP,
    ordering_provider_npi VARCHAR,
    ordering_provider_name VARCHAR,
    clinical_indication VARCHAR,
    specimen_type   VARCHAR,
    {PROVENANCE_COLUMNS}
);
"""

CLINICAL_NOTES_DDL = f"""
CREATE TABLE IF NOT EXISTS clinical_notes (
    id              VARCHAR PRIMARY KEY,
    patient_mrn     VARCHAR NOT NULL,
    encounter_id    VARCHAR,
    note_type       VARCHAR NOT NULL,
    note_datetime   TIMESTAMP NOT NULL,
    author          VARCHAR,
    content         TEXT,
    {PROVENANCE_COLUMNS}
);
"""

# ============================================================================
# CANONICAL TABLES - MemberSim
# ============================================================================

MEMBERS_DDL = f"""
CREATE TABLE IF NOT EXISTS members (
    id              VARCHAR PRIMARY KEY,
    member_id       VARCHAR NOT NULL,
    subscriber_id   VARCHAR,
    relationship_code VARCHAR DEFAULT '18',  -- 18=Self, 01=Spouse, 19=Child
    ssn             VARCHAR,
    given_name      VARCHAR NOT NULL,
    middle_name     VARCHAR,
    family_name     VARCHAR NOT NULL,
    birth_date      DATE NOT NULL,
    gender          VARCHAR NOT NULL,
    street_address  VARCHAR,
    city            VARCHAR,
    state           VARCHAR,
    postal_code     VARCHAR,
    phone           VARCHAR,
    email           VARCHAR,
    group_id        VARCHAR NOT NULL,
    plan_code       VARCHAR NOT NULL,
    coverage_start  DATE NOT NULL,
    coverage_end    DATE,
    pcp_npi         VARCHAR,
    {PROVENANCE_COLUMNS}
);
"""

CLAIMS_DDL = f"""
CREATE TABLE IF NOT EXISTS claims (
    claim_id        VARCHAR PRIMARY KEY,
    claim_type      VARCHAR NOT NULL,  -- PROFESSIONAL, INSTITUTIONAL, DENTAL, RX
    member_id       VARCHAR NOT NULL,
    subscriber_id   VARCHAR,
    provider_npi    VARCHAR NOT NULL,
    facility_npi    VARCHAR,
    service_date    DATE NOT NULL,
    admission_date  DATE,
    discharge_date  DATE,
    place_of_service VARCHAR DEFAULT '11',
    principal_diagnosis VARCHAR NOT NULL,
    other_diagnoses JSON,
    authorization_number VARCHAR,
    total_charge    DECIMAL(12,2),
    total_allowed   DECIMAL(12,2),
    total_paid      DECIMAL(12,2),
    member_responsibility DECIMAL(12,2),
    {PROVENANCE_COLUMNS}
);
"""

CLAIM_LINES_DDL = f"""
CREATE TABLE IF NOT EXISTS claim_lines (
    id              VARCHAR PRIMARY KEY,
    claim_id        VARCHAR NOT NULL,
    line_number     INTEGER NOT NULL,
    procedure_code  VARCHAR NOT NULL,
    procedure_modifiers JSON,
    service_date    DATE NOT NULL,
    units           DECIMAL(6,2) DEFAULT 1,
    charge_amount   DECIMAL(12,2) NOT NULL,
    allowed_amount  DECIMAL(12,2),
    paid_amount     DECIMAL(12,2),
    diagnosis_pointers JSON,
    revenue_code    VARCHAR,
    ndc_code        VARCHAR,
    place_of_service VARCHAR DEFAULT '11',
    {PROVENANCE_COLUMNS}
);
"""

# ============================================================================
# CANONICAL TABLES - RxMemberSim
# ============================================================================

PRESCRIPTIONS_DDL = f"""
CREATE TABLE IF NOT EXISTS prescriptions (
    prescription_number VARCHAR PRIMARY KEY,
    patient_mrn     VARCHAR,           -- Link to PatientSim if available
    member_id       VARCHAR,           -- Link to RxMember
    ndc             VARCHAR NOT NULL,
    drug_name       VARCHAR NOT NULL,
    quantity_prescribed DECIMAL(10,2) NOT NULL,
    days_supply     INTEGER NOT NULL,
    refills_authorized INTEGER DEFAULT 0,
    refills_remaining INTEGER DEFAULT 0,
    prescriber_npi  VARCHAR NOT NULL,
    prescriber_name VARCHAR,
    prescriber_dea  VARCHAR,
    written_date    DATE NOT NULL,
    expiration_date DATE NOT NULL,
    daw_code        VARCHAR DEFAULT '0',
    directions      TEXT,
    {PROVENANCE_COLUMNS}
);
"""

PHARMACY_CLAIMS_DDL = f"""
CREATE TABLE IF NOT EXISTS pharmacy_claims (
    claim_id        VARCHAR PRIMARY KEY,
    transaction_code VARCHAR NOT NULL,  -- B1=Billing, B2=Reversal, B3=Rebill
    service_date    DATE NOT NULL,
    pharmacy_npi    VARCHAR NOT NULL,
    pharmacy_ncpdp  VARCHAR,
    member_id       VARCHAR NOT NULL,
    cardholder_id   VARCHAR NOT NULL,
    person_code     VARCHAR,
    bin             VARCHAR NOT NULL,
    pcn             VARCHAR NOT NULL,
    group_number    VARCHAR NOT NULL,
    prescription_number VARCHAR NOT NULL,
    fill_number     INTEGER DEFAULT 0,
    ndc             VARCHAR NOT NULL,
    quantity_dispensed DECIMAL(10,2) NOT NULL,
    days_supply     INTEGER NOT NULL,
    daw_code        VARCHAR,
    prescriber_npi  VARCHAR NOT NULL,
    ingredient_cost_submitted DECIMAL(12,2),
    dispensing_fee_submitted DECIMAL(12,2),
    usual_customary_charge DECIMAL(12,2),
    gross_amount_due DECIMAL(12,2),
    patient_pay_amount DECIMAL(12,2),
    {PROVENANCE_COLUMNS}
);
"""

# ============================================================================
# CANONICAL TABLES - TrialSim
# ============================================================================

SUBJECTS_DDL = f"""
CREATE TABLE IF NOT EXISTS subjects (
    id              VARCHAR PRIMARY KEY,
    subject_id      VARCHAR NOT NULL,
    usubjid         VARCHAR NOT NULL,  -- STUDYID-SITEID-SUBJID
    study_id        VARCHAR NOT NULL,
    site_id         VARCHAR NOT NULL,
    patient_ref     VARCHAR,           -- Reference to PatientSim MRN
    ssn             VARCHAR,
    given_name      VARCHAR NOT NULL,
    family_name     VARCHAR NOT NULL,
    birth_date      DATE NOT NULL,
    gender          VARCHAR NOT NULL,
    race            VARCHAR,
    ethnicity       VARCHAR,
    screening_id    VARCHAR,
    screening_date  DATE,
    informed_consent_date DATE NOT NULL,
    randomization_date DATE,
    treatment_arm   VARCHAR,
    status          VARCHAR NOT NULL,
    {PROVENANCE_COLUMNS}
);
"""

TRIAL_VISITS_DDL = f"""
CREATE TABLE IF NOT EXISTS trial_visits (
    id              VARCHAR PRIMARY KEY,
    usubjid         VARCHAR NOT NULL,
    visit_num       DECIMAL(5,1) NOT NULL,
    visit_name      VARCHAR,
    visit_date      DATE NOT NULL,
    study_day       INTEGER,
    visit_status    VARCHAR,
    window_deviation_days INTEGER DEFAULT 0,
    {PROVENANCE_COLUMNS}
);
"""

ADVERSE_EVENTS_DDL = f"""
CREATE TABLE IF NOT EXISTS adverse_events (
    id              VARCHAR PRIMARY KEY,
    usubjid         VARCHAR NOT NULL,
    aeseq           INTEGER,
    aeterm          VARCHAR NOT NULL,
    aedecod         VARCHAR,           -- MedDRA Preferred Term
    aebodsys        VARCHAR,           -- MedDRA System Organ Class
    aestdtc         DATE NOT NULL,
    aeendtc         DATE,
    aesev           VARCHAR,           -- Mild, Moderate, Severe
    aetoxgr         VARCHAR,           -- CTCAE grade 1-5
    aeser           VARCHAR,           -- Y/N
    aerel           VARCHAR,           -- Relationship to treatment
    aeacn           VARCHAR,           -- Action taken
    aeout           VARCHAR,           -- Outcome
    {PROVENANCE_COLUMNS}
);
"""

EXPOSURES_DDL = f"""
CREATE TABLE IF NOT EXISTS exposures (
    id              VARCHAR PRIMARY KEY,
    usubjid         VARCHAR NOT NULL,
    exseq           INTEGER,
    extrt           VARCHAR NOT NULL,
    exdose          DECIMAL(12,4),
    exdosu          VARCHAR,
    exdosfrq        VARCHAR,
    exroute         VARCHAR,
    exstdtc         DATE NOT NULL,
    exendtc         DATE,
    exadj           VARCHAR,
    dose_modification VARCHAR,
    {PROVENANCE_COLUMNS}
);
"""

# ============================================================================
# INDEXES
# ============================================================================

INDEXES_DDL = """
-- Patient lookups
CREATE INDEX IF NOT EXISTS idx_patients_ssn ON patients(ssn);
CREATE INDEX IF NOT EXISTS idx_patients_mrn ON patients(mrn);
CREATE INDEX IF NOT EXISTS idx_patients_cohort ON patients(cohort_id);

-- Encounter lookups
CREATE INDEX IF NOT EXISTS idx_encounters_patient ON encounters(patient_mrn);
CREATE INDEX IF NOT EXISTS idx_encounters_admission ON encounters(admission_time);
CREATE INDEX IF NOT EXISTS idx_encounters_cohort ON encounters(cohort_id);

-- Diagnosis lookups
CREATE INDEX IF NOT EXISTS idx_diagnoses_patient ON diagnoses(patient_mrn);
CREATE INDEX IF NOT EXISTS idx_diagnoses_code ON diagnoses(code);
CREATE INDEX IF NOT EXISTS idx_diagnoses_cohort ON diagnoses(cohort_id);

-- Medication lookups
CREATE INDEX IF NOT EXISTS idx_medications_patient ON medications(patient_mrn);
CREATE INDEX IF NOT EXISTS idx_medications_cohort ON medications(cohort_id);

-- Lab results lookups
CREATE INDEX IF NOT EXISTS idx_lab_results_patient ON lab_results(patient_mrn);
CREATE INDEX IF NOT EXISTS idx_lab_results_loinc ON lab_results(loinc_code);
CREATE INDEX IF NOT EXISTS idx_lab_results_cohort ON lab_results(cohort_id);

-- Member lookups
CREATE INDEX IF NOT EXISTS idx_members_ssn ON members(ssn);
CREATE INDEX IF NOT EXISTS idx_members_subscriber ON members(subscriber_id);
CREATE INDEX IF NOT EXISTS idx_members_cohort ON members(cohort_id);

-- Claim lookups
CREATE INDEX IF NOT EXISTS idx_claims_member ON claims(member_id);
CREATE INDEX IF NOT EXISTS idx_claims_service_date ON claims(service_date);
CREATE INDEX IF NOT EXISTS idx_claims_cohort ON claims(cohort_id);
CREATE INDEX IF NOT EXISTS idx_claim_lines_claim ON claim_lines(claim_id);
CREATE INDEX IF NOT EXISTS idx_claim_lines_cohort ON claim_lines(cohort_id);

-- Pharmacy claim lookups
CREATE INDEX IF NOT EXISTS idx_pharmacy_claims_member ON pharmacy_claims(member_id);
CREATE INDEX IF NOT EXISTS idx_pharmacy_claims_ndc ON pharmacy_claims(ndc);
CREATE INDEX IF NOT EXISTS idx_pharmacy_claims_cohort ON pharmacy_claims(cohort_id);

-- Prescription lookups
CREATE INDEX IF NOT EXISTS idx_prescriptions_patient ON prescriptions(patient_mrn);
CREATE INDEX IF NOT EXISTS idx_prescriptions_member ON prescriptions(member_id);
CREATE INDEX IF NOT EXISTS idx_prescriptions_cohort ON prescriptions(cohort_id);

-- Subject lookups
CREATE INDEX IF NOT EXISTS idx_subjects_study ON subjects(study_id);
CREATE INDEX IF NOT EXISTS idx_subjects_site ON subjects(site_id);
CREATE INDEX IF NOT EXISTS idx_subjects_ssn ON subjects(ssn);
CREATE INDEX IF NOT EXISTS idx_subjects_cohort ON subjects(cohort_id);

-- Trial visit lookups
CREATE INDEX IF NOT EXISTS idx_trial_visits_subject ON trial_visits(usubjid);
CREATE INDEX IF NOT EXISTS idx_trial_visits_cohort ON trial_visits(cohort_id);

-- Adverse event lookups
CREATE INDEX IF NOT EXISTS idx_adverse_events_subject ON adverse_events(usubjid);
CREATE INDEX IF NOT EXISTS idx_adverse_events_cohort ON adverse_events(cohort_id);

-- Exposure lookups
CREATE INDEX IF NOT EXISTS idx_exposures_cohort ON exposures(cohort_id);

-- Cohort entity lookups
CREATE INDEX IF NOT EXISTS idx_cohort_entities_cohort ON cohort_entities(cohort_id);
CREATE INDEX IF NOT EXISTS idx_cohort_entities_type ON cohort_entities(entity_type);
CREATE INDEX IF NOT EXISTS idx_cohort_tags_cohort ON cohort_tags(cohort_id);
CREATE INDEX IF NOT EXISTS idx_cohort_tags_tag ON cohort_tags(tag);
"""

# ============================================================================
# SCHEMA APPLICATION
# ============================================================================

# All DDL statements in order of execution
ALL_DDL = [
    # System tables
    SCHEMA_MIGRATIONS_DDL,
    
    # Sequences (must be created before tables that reference them)
    COHORT_ENTITIES_SEQ_DDL,
    COHORT_TAGS_SEQ_DDL,
    
    # State management tables
    COHORTS_DDL,
    COHORT_ENTITIES_DDL,
    COHORT_TAGS_DDL,
    
    # Profile management tables
    PROFILES_SEQ_DDL,
    PROFILES_DDL,
    PROFILE_EXECUTIONS_DDL,
    
    # Journey management tables
    JOURNEYS_SEQ_DDL,
    JOURNEYS_DDL,
    JOURNEY_EXECUTIONS_DDL,
    
    # PatientSim canonical tables
    PATIENTS_DDL,
    ENCOUNTERS_DDL,
    DIAGNOSES_DDL,
    MEDICATIONS_DDL,
    LAB_RESULTS_DDL,
    VITAL_SIGNS_DDL,
    ORDERS_DDL,
    CLINICAL_NOTES_DDL,
    
    # MemberSim canonical tables
    MEMBERS_DDL,
    CLAIMS_DDL,
    CLAIM_LINES_DDL,
    
    # RxMemberSim canonical tables
    PRESCRIPTIONS_DDL,
    PHARMACY_CLAIMS_DDL,
    
    # TrialSim canonical tables
    SUBJECTS_DDL,
    TRIAL_VISITS_DDL,
    ADVERSE_EVENTS_DDL,
    EXPOSURES_DDL,
    
    # Indexes
    INDEXES_DDL,
]


def apply_schema(conn: duckdb.DuckDBPyConnection) -> None:
    """
    Apply the full schema to a database connection.
    
    Args:
        conn: DuckDB connection to apply schema to.
    """
    for ddl in ALL_DDL:
        conn.execute(ddl)
    
    # Record initial schema version
    conn.execute("""
        INSERT INTO schema_migrations (version, description)
        VALUES (?, 'Initial schema with auto-persist support')
    """, [SCHEMA_VERSION])


def get_canonical_tables() -> List[str]:
    """Get list of canonical table names."""
    return [
        'patients', 'encounters', 'diagnoses', 'medications',
        'lab_results', 'vital_signs', 'orders', 'clinical_notes',
        'members', 'claims', 'claim_lines',
        'prescriptions', 'pharmacy_claims',
        'subjects', 'trial_visits', 'adverse_events', 'exposures'
    ]


def get_state_tables() -> List[str]:
    """Get list of state management table names."""
    return ['cohorts', 'cohort_entities', 'cohort_tags']


def get_system_tables() -> List[str]:
    """Get list of system table names."""
    return ['schema_migrations']
