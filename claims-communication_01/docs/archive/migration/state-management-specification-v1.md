# State Management Technical Specification

This document defines the API interfaces and data formats for the State Management capability.

## Overview

State Management enables users to save and load workspace cohorts - complete snapshots of all generated entities (patients, encounters, claims, etc.) with full provenance tracking.

**Storage Backend**: DuckDB embedded database  
**Storage Location**: `~/.healthsim/healthsim.duckdb`  
**Export Format**: JSON (for sharing)

---

## API Reference

### save_cohort

Saves entities as a named cohort.

#### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| name | string | Yes | Unique cohort name (kebab-case recommended) |
| entities | object | Yes | Dict of entity_type → entity list |
| description | string | No | Cohort description |
| tags | array[string] | No | Tags for organization |
| overwrite | boolean | No | Replace existing (default: false) |

#### Returns

```json
{
  "cohort_id": "uuid-string",
  "name": "cohort-name",
  "entity_count": 42,
  "entities_by_type": {
    "patient": 5,
    "encounter": 15,
    "diagnosis": 22
  }
}
```

#### Python Usage

```python
from healthsim.state import save_cohort

cohort_id = save_cohort(
    name='diabetes-cohort',
    entities={
        'patients': [patient1, patient2],
        'encounters': [enc1, enc2, enc3]
    },
    description='Type 2 Diabetes test cohort',
    tags=['diabetes', 'testing']
)
```

---

### load_cohort

Loads a cohort from the database.

#### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| name | string | Yes | Cohort name or UUID |

#### Returns

```json
{
  "cohort_id": "uuid-string",
  "name": "cohort-name",
  "description": "...",
  "entities": {
    "patients": [...],
    "encounters": [...]
  },
  "tags": ["tag1", "tag2"],
  "created_at": "2024-12-26T10:30:00Z"
}
```

#### Python Usage

```python
from healthsim.state import load_cohort

cohort = load_cohort('diabetes-cohort')
patients = cohort['entities']['patients']
```

---

### list_cohorts

Lists available cohorts with optional filtering.

#### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| tag | string | No | Filter by tag |
| search | string | No | Search in name/description |
| limit | integer | No | Max results (default: 100) |

#### Returns

```json
{
  "cohorts": [
    {
      "cohort_id": "uuid-string",
      "name": "cohort-name",
      "description": "...",
      "entity_count": 42,
      "tags": ["tag1"],
      "created_at": "2024-12-26T10:30:00Z"
    }
  ],
  "total_count": 5
}
```

#### Python Usage

```python
from healthsim.state import list_cohorts

# List all
cohorts = list_cohorts()

# Filter by tag
diabetes_cohorts = list_cohorts(tag='diabetes')

# Search
matches = list_cohorts(search='cohort')
```

---

### delete_cohort

Deletes a cohort (metadata and links, not underlying entity data).

#### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| name | string | Yes | Cohort name or UUID |

#### Python Usage

```python
from healthsim.state import delete_cohort

delete_cohort('old-cohort')
```

---

### export_cohort_to_json

Exports a cohort to JSON file for sharing.

#### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| name | string | Yes | Cohort name or UUID |
| output_path | string/Path | No | Where to save (default: ~/Downloads/{name}.json) |

#### Returns

Path to the exported file.

#### Python Usage

```python
from healthsim.state import export_cohort_to_json

path = export_cohort_to_json('diabetes-cohort')
# Returns: ~/Downloads/diabetes-cohort.json

# Custom location
path = export_cohort_to_json('diabetes-cohort', output_path='/tmp/export.json')
```

---

### import_cohort_from_json

Imports a JSON cohort file.

#### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| file_path | string/Path | Yes | Path to JSON file |
| name | string | No | Override cohort name |
| overwrite | boolean | No | Replace existing (default: false) |

#### Python Usage

```python
from healthsim.state import import_cohort_from_json
from pathlib import Path

cohort_id = import_cohort_from_json(Path('shared-cohort.json'))

# With name override
cohort_id = import_cohort_from_json(
    Path('data.json'),
    name='imported-cohort',
    overwrite=True
)
```

---

## Database Schema

### cohorts

Stores cohort metadata.

```sql
CREATE TABLE cohorts (
    cohort_id   UUID PRIMARY KEY,
    name          VARCHAR UNIQUE NOT NULL,
    description   VARCHAR,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata      JSON
);
```

### cohort_entities

Links entities to cohorts with full entity data.

```sql
CREATE TABLE cohort_entities (
    id            INTEGER PRIMARY KEY,
    cohort_id   UUID NOT NULL REFERENCES cohorts(cohort_id),
    entity_type   VARCHAR NOT NULL,
    entity_id     UUID NOT NULL,
    entity_data   JSON NOT NULL,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### cohort_tags

Tag-based organization.

```sql
CREATE TABLE cohort_tags (
    id            INTEGER PRIMARY KEY,
    cohort_id   UUID NOT NULL REFERENCES cohorts(cohort_id),
    tag           VARCHAR NOT NULL,
    UNIQUE(cohort_id, tag)
);
```

---

## JSON Export Format

Exported JSON files follow this structure for interoperability:

```json
{
  "schema_version": "1.0",
  "cohort_id": "uuid-string",
  "name": "cohort-name",
  "description": "Optional description",
  "created_at": "2024-12-26T10:30:00Z",
  "tags": ["tag1", "tag2"],
  "entities": {
    "patients": [
      {
        "patient_id": "uuid",
        "mrn": "MRN001",
        "given_name": "John",
        "family_name": "Doe",
        "birth_date": "1980-01-15",
        "...": "..."
      }
    ],
    "encounters": [...],
    "diagnoses": [...],
    "medications": [...],
    "lab_results": [...],
    "vital_signs": [...],
    "procedures": [...],
    "clinical_notes": [...]
  }
}
```

### Supported Entity Types

| Type | Description |
|------|-------------|
| patients | Patient demographics |
| encounters | Visits, admissions |
| diagnoses | ICD-10 diagnoses |
| procedures | CPT/ICD-PCS procedures |
| medications | Medication records |
| lab_results | Lab values |
| vital_signs | Vitals |
| clinical_notes | Notes/documents |
| members | Health plan members |
| claims | Claim headers |
| claim_lines | Claim line items |
| prescriptions | Rx fills |
| subjects | Trial subjects |
| trial_visits | Trial visit data |

---

## Migration from Legacy JSON

If you have existing cohorts in `~/.healthsim/cohorts/`:

```bash
# Check status
python scripts/migrate_json_to_duckdb.py --status

# Preview migration
python scripts/migrate_json_to_duckdb.py --dry-run

# Execute migration
python scripts/migrate_json_to_duckdb.py
```

The migration tool automatically:
1. Discovers JSON files in `~/.healthsim/cohorts/`
2. Creates backup at `~/.healthsim/cohorts_backup/`
3. Imports each cohort to DuckDB
4. Verifies migration success

---

## See Also

- [State Management User Guide](user-guide.md)
- [Data Architecture](../data-architecture.md)
- [State Management Skill](../../skills/common/state-management.md)
