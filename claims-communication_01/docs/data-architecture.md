# HealthSim Data Architecture

## Overview

HealthSim uses **DuckDB** as its unified data store, organized into three schemas:

| Schema | Purpose | Tables |
|--------|---------|--------|
| **main** | Generated entities + state management | patients, encounters, claims, cohorts, etc. |
| **network** | Real provider reference data (NPPES) | providers (8.9M), facilities, quality metrics |
| **population** | Real demographic reference data (CDC/Census) | places_county, svi_tract, adi_blockgroup, etc. |

**Database Location**: `healthsim-workspace/healthsim.duckdb` (~1.7 GB)

The database is distributed via Git LFS and downloaded automatically when you clone the repository.

---

## Canonical Data Model

### Entity Extension Pattern

HealthSim uses an inheritance-based entity model where Person is the base entity that extends to domain-specific types:

```
                    Person (Base)
                       │
        ┌──────────────┼──────────────┐
        │              │              │
     Patient        Member       RxMember
   (PatientSim)   (MemberSim)  (RxMemberSim)
        │
     Subject
    (TrialSim)
```

**Identity Correlation**: SSN serves as the universal correlator across products, enabling seamless entity linking between clinical, claims, and pharmacy domains.

### Entity Relationships

| Entity | Primary Key | Foreign Keys | Product |
|--------|-------------|--------------|---------|
| patients | patient_id | - | PatientSim |
| encounters | encounter_id | patient_id | PatientSim |
| diagnoses | diagnosis_id | encounter_id, patient_id | PatientSim |
| medications | medication_id | patient_id | PatientSim |
| lab_results | lab_result_id | encounter_id, patient_id | PatientSim |
| vital_signs | vital_sign_id | encounter_id, patient_id | PatientSim |
| clinical_notes | note_id | encounter_id, patient_id | PatientSim |
| members | member_id | - | MemberSim |
| claims | claim_id | member_id | MemberSim |
| claim_lines | claim_line_id | claim_id | MemberSim |
| prescriptions | prescription_id | patient_id | RxMemberSim |
| pharmacy_claims | pharmacy_claim_id | prescription_id | RxMemberSim |
| subjects | subject_id | patient_id | TrialSim |
| trial_visits | visit_id | subject_id | TrialSim |
| adverse_events | ae_id | subject_id | TrialSim |
| exposures | exposure_id | subject_id | TrialSim |

---

## Schema Details

### Main Schema (Entity + State Management)

Source of truth for all generated entities and cohort management.

**Entity Tables** (generated data):

| Table | Description | Source Product |
|-------|-------------|----------------|
| patients | Patient demographics and identifiers | PatientSim |
| encounters | Visits, admissions, discharges | PatientSim |
| diagnoses | ICD-10-CM coded diagnoses | PatientSim |
| medications | Active and historical medications | PatientSim |
| lab_results | Laboratory values with LOINC codes | PatientSim |
| vital_signs | Vitals (BP, HR, temp, etc.) | PatientSim |
| clinical_notes | Clinical documentation | PatientSim |
| orders | Clinical orders | PatientSim |
| members | Health plan member demographics | MemberSim |
| claims | Claim headers (837P/837I) | MemberSim |
| claim_lines | Claim line items with CPT/HCPCS | MemberSim |
| prescriptions | Prescription orders | RxMemberSim |
| pharmacy_claims | NCPDP pharmacy claims | RxMemberSim |
| subjects | Clinical trial subjects | TrialSim |
| trial_visits | Protocol visit data | TrialSim |
| adverse_events | AEs with MedDRA coding | TrialSim |
| exposures | Drug exposure records | TrialSim |

**State Management Tables**:

| Table | Description |
|-------|-------------|
| cohorts | Cohort metadata (name, description, timestamps, tags) |
| cohort_entities | Links entities to cohorts (stores entity JSON) |
| cohort_tags | Tag-based organization for filtering |
| schema_migrations | Schema version tracking |

### Network Schema (Provider Reference Data)

Real-world provider data from CMS/NPPES. Read-only reference tables.

| Table | Source | Records | Description |
|-------|--------|---------|-------------|
| providers | NPPES | 8,925,672 | All US healthcare providers with NPIs |
| facilities | CMS POS | ~35,000 | Medicare-certified facilities |
| hospital_quality | CMS Hospital Compare | ~4,500 | Hospital quality metrics |
| physician_quality | CMS Physician Compare | ~1.2M | Physician quality data |
| ahrf_county | HRSA AHRF | ~3,200 | County-level healthcare resources |

### Population Schema (Demographic Reference Data)

Real-world demographic and health indicator data from CDC/Census. Read-only reference tables.

| Table | Source | Records | Description |
|-------|--------|---------|-------------|
| places_county | CDC PLACES 2024 | ~3,200 | County-level health indicators |
| places_tract | CDC PLACES 2024 | ~85,000 | Census tract health indicators |
| svi_county | CDC SVI 2022 | ~3,200 | Social Vulnerability Index by county |
| svi_tract | CDC SVI 2022 | ~85,000 | Social Vulnerability Index by tract |
| adi_blockgroup | HRSAn ADI 2021 | ~242,000 | Area Deprivation Index by block group |

---

## State Management

### Overview

State management enables saving, loading, and querying generated data across sessions. All entity data is persisted to DuckDB with full provenance tracking.

### Two Retrieval Patterns

When working with saved cohorts, you have two options for retrieving data:

| Pattern | Use Case | Token Cost | Tool |
|---------|----------|------------|------|
| **Full Load** | Small cohorts (<50 entities), need all data immediately | High (1K-50K tokens) | `healthsim_load_cohort` |
| **Summary + Query** | Large cohorts (50+ entities), token efficiency | Low (~500 tokens) | `healthsim_get_cohort_summary` + `healthsim_query` |

**Why two patterns?**

- **Full Load** returns all entities in the response, making them immediately available in the conversation context. Great for small cohorts where you want to work with all the data at once.

- **Summary + Query** returns only metadata and statistics (~500 tokens), keeping the context window lean. You then query for specific data as needed. Essential for large cohorts that would overwhelm the context.

### State Management Operations

| Operation | Tool | Description |
|-----------|------|-------------|
| Save cohort | `healthsim_save_cohort` | Persist entities with name, description, tags |
| Load full data | `healthsim_load_cohort` | Retrieve all entities (high token cost) |
| Load summary | `healthsim_get_cohort_summary` | Retrieve metadata + samples (~500 tokens) |
| Query data | `healthsim_query` | SQL query against saved entities |
| List cohorts | `healthsim_list_cohorts` | Browse saved cohorts with filtering |
| Delete cohort | `healthsim_delete_cohort` | Remove cohort (requires confirmation) |

### Workflow Examples

**Small Cohort (Full Load)**:
```
User: "Save these 10 patients as 'test-cohort'"
→ healthsim_save_cohort(name='test-cohort', entities={...})

User: "Load my test cohort"
→ healthsim_load_cohort('test-cohort')
→ Returns all 10 patients with full details
```

**Large Cohort (Summary + Query)**:
```
User: "Generate 200 diabetic patients and save them"
→ healthsim_save_cohort(name='diabetes-200', entities={...})

User: "What's in my diabetes cohort?"
→ healthsim_get_cohort_summary('diabetes-200')
→ Returns: 200 patients, age range 35-78, 52% female, 3 samples

User: "Show me female patients over 65"
→ healthsim_query("SELECT * FROM patients WHERE gender='F' AND age > 65")
→ Returns matching subset only
```

### Provenance Tracking

All entity tables include provenance columns for traceability:

```sql
created_at          TIMESTAMP   -- When the entity was created
source_type         VARCHAR     -- 'generated', 'loaded', 'derived'
source_system       VARCHAR     -- 'patientsim', 'membersim', etc.
skill_used          VARCHAR     -- Skill that generated the entity
generation_seed     INTEGER     -- For reproducibility
```

---

## Reference Data Philosophy

HealthSim uses two approaches for reference data, chosen based on data characteristics:

### Text Files (Skills-Based Reference Data)

**Location**: `references/` and `formats/` directories

**Examples**: Code systems (ICD-10, CPT, LOINC), format specifications, validation rules

**Why text files?**
- Version controlled in git
- Human-readable and editable
- Part of the conversation (Claude reads during generation)
- Small and focused (~KB each)

### DuckDB (External Reference Data)

**Location**: `healthsim.duckdb` (network.* and population.* schemas)

**Examples**: NPPES providers (8.9M records), CDC PLACES health indicators, SVI vulnerability scores

**Why DuckDB?**
- Large datasets (millions of records)
- Real statistical data from authoritative sources
- SQL queryable for complex analysis
- Compressed storage (5-7x smaller than CSV)

### Decision Guide

| Characteristic | Use Text Files | Use DuckDB |
|----------------|----------------|------------|
| Size | < 1MB | > 1MB |
| Source | HealthSim-created | External agency (CDC, CMS) |
| Updates | Version controlled | Periodic refresh |
| Access pattern | Read during generation | Query for analysis |

---

## Querying the Database

### Via HealthSim MCP Server (Recommended)

The `healthsim-mcp` server is the recommended way to query:

```
# List all tables
healthsim_tables

# Query population reference data
healthsim_query_reference(table="places_county", state="CA")

# Custom SQL query
healthsim_query(sql="SELECT * FROM network.providers WHERE state = 'TX' LIMIT 10")

# Get cohort summary
healthsim_get_cohort_summary(cohort_id_or_name="my-cohort")
```

### SQL Query Examples

**Find providers by specialty and location**:
```sql
SELECT npi, first_name, last_name, primary_taxonomy_code, city
FROM network.providers 
WHERE state = 'CA' 
  AND primary_taxonomy_code LIKE '207R%'  -- Internal Medicine
LIMIT 20;
```

**Get health indicators for a county**:
```sql
SELECT county_name, diabetes_crude_prev, obesity_crude_prev, 
       smoking_crude_prev, binge_drinking_crude_prev
FROM population.places_county 
WHERE state_abbr = 'TX'
ORDER BY diabetes_crude_prev DESC
LIMIT 10;
```

**Cross-reference patient location with SDOH**:
```sql
SELECT p.patient_id, p.given_name, p.family_name,
       svi.rpl_themes as vulnerability_score
FROM main.patients p
JOIN population.svi_tract svi ON p.census_tract = svi.fips
WHERE svi.rpl_themes > 0.75;
```

**Query saved cohort data**:
```sql
SELECT se.entity_type, COUNT(*) as count
FROM main.cohort_entities se
JOIN main.cohorts s ON se.cohort_id = s.cohort_id
WHERE s.name = 'diabetes-cohort'
GROUP BY se.entity_type;
```

---

## Performance Characteristics

| Operation | Typical Performance |
|-----------|---------------------|
| Save cohort (100 entities) | < 100ms |
| Load cohort (100 entities) | < 50ms |
| Get cohort summary | < 50ms |
| List cohorts | < 10ms |
| Provider search (indexed) | < 50ms |
| Full table scan (250K rows) | < 500ms |

DuckDB's columnar storage provides excellent compression:
- Reference data: 5-7x compression vs CSV
- Cohort data: 3-5x compression vs JSON

---

## Related Documentation

- [State Management Skill](../skills/common/state-management.md) - Conversational interface for cohorts
- [NetworkSim README](../skills/networksim/README.md) - Provider reference data usage
- [PopulationSim README](../skills/populationsim/README.md) - Demographic reference data usage
- [Architecture Guide](./HEALTHSIM-ARCHITECTURE-GUIDE.md) - Overall system architecture
