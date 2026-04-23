# Session 06: Documentation Update

**Initiative**: DuckDB Unified Data Architecture  
**Phase**: 1 - Foundation  
**Estimated Duration**: 60-90 minutes  
**Prerequisites**: SESSION-01 through SESSION-05 complete

---

## Objective

Update all documentation to reflect the new DuckDB-based architecture. Ensure consistency, fix broken links, update tutorials, and deprecate outdated content.

---

## Context

With the migration to DuckDB complete, documentation throughout the project needs updates:
- State management docs need to reflect DuckDB backend
- PopulationSim docs need to reference DuckDB tables
- Skills need updates for new capabilities
- Tutorials need to use current APIs
- README needs architecture updates

### Documentation Audit Checklist

| Document | Status | Action Needed |
|----------|--------|---------------|
| docs/state-management/specification.md | Outdated | Update for DuckDB |
| docs/state-management/user-guide.md | Outdated | Update examples |
| skills/common/state-management.md | Outdated | Add new tools, update behavior |
| skills/populationsim/SKILL.md | Outdated | Reference DuckDB tables |
| skills/populationsim/data-sources.md | Outdated | Update storage info |
| README.md | May need updates | Check architecture section |
| docs/HEALTHSIM-ARCHITECTURE-GUIDE.md | Outdated | Add data architecture |
| hello-healthsim/ examples | May need updates | Verify still work |
| CHANGELOG.md | Needs entry | Document changes |

---

## Pre-Flight Checklist

- [ ] SESSION-05 complete (all code changes done)
- [ ] All tests passing
- [ ] Git status clean
- [ ] Review each document listed above

---

## Deliverables

### 1. Updated Core Documentation

- State management specification
- State management user guide
- Architecture guide update
- New data-architecture.md

### 2. Updated Skills

- state-management.md skill
- PopulationSim skill

### 3. Updated Examples

- hello-healthsim cohorts

### 4. Updated Project Files

- README.md
- CHANGELOG.md

---

## Implementation Steps

### Step 1: Create New Data Architecture Document

```markdown
# docs/data-architecture.md

# HealthSim Data Architecture

## Overview

HealthSim uses DuckDB as its unified data store for:
- **State Management**: Cohort persistence and retrieval
- **Reference Data**: PopulationSim demographic datasets
- **Analytics** (Phase 2): Star schema for OHDSI-style analysis

## Database Location

```
~/.healthsim/healthsim.duckdb
```

## Schema Layers

### Layer 1: Canonical Data Model

Source of truth for all generated entities. Tables mirror the JSON canonical model.

| Table | Description |
|-------|-------------|
| patients | Patient demographics |
| encounters | Visits, admissions |
| diagnoses | ICD-10 codes |
| procedures | CPT/ICD-PCS codes |
| medications | Active/historical meds |
| lab_results | Lab values |
| vital_signs | Vitals |
| clinical_notes | Notes/documents |
| members | Health plan members |
| claims | Claim headers |
| claim_lines | Claim line items |
| prescriptions | Rx fills |
| subjects | Trial subjects |
| trial_visits | Trial visit data |

### Layer 2: State Management

Organizes entities into named cohorts.

| Table | Description |
|-------|-------------|
| cohorts | Cohort metadata |
| cohort_entities | Entity-cohort links |
| cohort_tags | Tag organization |

### Layer 3: Reference Data

Read-only datasets for generation support.

| Table | Source | Records |
|-------|--------|---------|
| ref_cdc_places_tract | CDC PLACES 2024 | ~85,000 |
| ref_cdc_places_county | CDC PLACES 2024 | ~3,200 |
| ref_svi_tract | SVI 2022 | ~85,000 |
| ref_svi_county | SVI 2022 | ~3,200 |
| ref_adi_blockgroup | ADI 2021 | ~242,000 |

## Provenance Tracking

All canonical tables include provenance columns:

```sql
created_at          TIMESTAMP
source_type         VARCHAR   -- 'generated', 'loaded', 'derived'
source_system       VARCHAR   -- 'patientsim', 'membersim', etc.
skill_used          VARCHAR   -- Skill that generated the entity
generation_seed     INTEGER   -- For reproducibility
```

## Querying

Direct SQL queries are supported:

```sql
-- Find all diabetic patients
SELECT * FROM patients p
JOIN cohort_entities se ON p.patient_id = se.entity_id
JOIN cohorts s ON se.cohort_id = s.cohort_id
WHERE s.name = 'diabetes-cohort';

-- Query reference data
SELECT AVG(diabetes_crude_prev) 
FROM ref_cdc_places_tract 
WHERE state_abbr = 'CA';
```

## Migration from JSON

If you have existing JSON cohorts, run:

```bash
python scripts/migrate_json_to_duckdb.py
```

See [Migration Guide](./state-management/migration.md) for details.
```

### Step 2: Update State Management Specification

Update `docs/state-management/specification.md`:

```markdown
# State Management Specification

## Overview

HealthSim state management persists generated entities in a DuckDB database,
enabling cohorts to be saved, loaded, shared, and queried.

## Storage

- **Location**: `~/.healthsim/healthsim.duckdb`
- **Format**: DuckDB embedded database
- **Schema**: See [Data Architecture](../data-architecture.md)

## MCP Tools

### save_cohort

Saves entities to the database as a named cohort.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| name | string | Yes | Unique cohort name |
| entities | object | Yes | Dict of entity type → entity list |
| description | string | No | Cohort description |
| tags | array | No | List of tags for organization |
| overwrite | boolean | No | Replace existing (default: false) |

**Returns:**
```json
{
  "cohort_id": "uuid-string",
  "name": "cohort-name",
  "entity_count": 42
}
```

### load_cohort

Loads a cohort from the database.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| name | string | Yes | Cohort name or UUID |

**Returns:**
```json
{
  "cohort_id": "uuid-string",
  "name": "cohort-name",
  "description": "...",
  "entities": {
    "patient": [...],
    "encounter": [...]
  },
  "tags": ["tag1", "tag2"]
}
```

### list_cohorts

Lists available cohorts.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| tag | string | No | Filter by tag |
| search | string | No | Search in name/description |
| limit | integer | No | Max results (default: 100) |

### delete_cohort

Deletes a cohort (metadata and links, not entity data).

### export_cohort_json

Exports a cohort to JSON file for sharing.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| name | string | Yes | Cohort name or UUID |
| output_path | string | No | Where to save (default: ~/Downloads) |

### import_cohort_json

Imports a JSON cohort file.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| file_path | string | Yes | Path to JSON file |
| name | string | No | Override cohort name |
| overwrite | boolean | No | Replace existing (default: false) |
```

### Step 3: Update State Management Skill

Update `skills/common/state-management.md`:

```markdown
---
name: state-management
description: |
  Save, load, and manage HealthSim cohorts. Cohorts persist generated
  entities (patients, encounters, claims, etc.) for later use. Use phrases
  like "save this cohort", "load my diabetic patients", "list cohorts",
  "export for sharing", "import from file".
---

# State Management Skill

## Overview

State management allows you to persist generated healthcare data cohorts
for future use, sharing, and analysis. Cohorts are stored in a local
DuckDB database.

## Trigger Phrases

- "Save this cohort as..."
- "Save these patients as..."
- "Load cohort..."
- "Open the [name] cohort"
- "List my cohorts"
- "Show available cohorts"
- "Delete cohort..."
- "Export [cohort] as JSON"
- "Import cohort from [path]"
- "Tag this cohort with..."
- "Find cohorts tagged..."

## Capabilities

### Saving Cohorts

```
User: "Save this as my-diabetes-cohort"
Claude: [Saves all generated entities to database]
        "Saved cohort 'my-diabetes-cohort' with 15 patients, 47 encounters."
```

### Loading Cohorts

```
User: "Load my-diabetes-cohort"
Claude: [Retrieves entities from database]
        "Loaded 'my-diabetes-cohort': 15 patients, 47 encounters, 23 diagnoses."
```

### Listing Cohorts

```
User: "What cohorts do I have?"
Claude: [Lists available cohorts]
        "You have 5 saved cohorts:
         - diabetes-cohort (15 patients)
         - ed-simulation (50 patients)
         - claims-test (100 members)
         ..."
```

### Sharing Cohorts

```
User: "Export diabetes-cohort as JSON"
Claude: [Exports to ~/Downloads/diabetes-cohort.json]
        "Exported to ~/Downloads/diabetes-cohort.json (150 entities)"

User: "Import cohort from ~/Downloads/shared-cohort.json"
Claude: [Imports to database]
        "Imported 'shared-cohort' with 25 patients."
```

### Querying (Advanced)

```
User: "How many encounters across all cohorts?"
Claude: [Queries database directly]
        "Found 1,247 encounters across 12 cohorts."
```

## Examples

### Example 1: Complete Save/Load Cycle

```
User: "Generate 5 patients with Type 2 Diabetes"
Claude: [Generates patients with encounters, diagnoses, medications]

User: "Save this as diabetes-test-cohort with tags diabetes, testing"
Claude: "Saved 'diabetes-test-cohort' (5 patients, 15 encounters, 5 A1C labs)
         Tagged: diabetes, testing"

[Later session]

User: "Load my diabetes testing cohort"
Claude: [Loads diabetes-test-cohort]
        "Loaded 'diabetes-test-cohort': 5 patients ready for use."
```

### Example 2: Sharing Between Users

```
User: "Export my trial simulation for the research team"
Claude: [Exports to JSON]
        "Exported 'trial-simulation' to ~/Downloads/trial-simulation.json
         Share this file with your team."

[Teammate's session]

User: "Import the trial cohort from ~/Downloads/trial-simulation.json"
Claude: "Imported 'trial-simulation': 200 subjects, 1,500 visits."
```

## Validation Rules

- Cohort names must be unique
- Entity references must be valid UUIDs
- Dates must be in ISO format
- Tags are case-insensitive

## Related Skills

- [PatientSim](../patientsim/SKILL.md) - Generate patient data
- [MemberSim](../membersim/SKILL.md) - Generate member/claims data
- [TrialSim](../trialsim/SKILL.md) - Generate clinical trial data

## Storage Details

Cohorts are stored in `~/.healthsim/healthsim.duckdb`. For technical
details, see the [Data Architecture Guide](../../docs/data-architecture.md).
```

### Step 4: Update PopulationSim Skill

Update `skills/populationsim/SKILL.md` to reference DuckDB tables.

### Step 5: Update README.md

Add data architecture section to the main README.

### Step 6: Update CHANGELOG.md

```markdown
## [Unreleased]

### Added
- DuckDB-based state management replacing JSON files
- PopulationSim reference data now in DuckDB (5-7x compression)
- JSON export/import for cohort sharing
- SQL query capability for cohorts and reference data
- Migration tool for existing JSON cohorts
- New `export_cohort_json` and `import_cohort_json` MCP tools

### Changed
- State management backend from JSON files to DuckDB
- PopulationSim data location from CSV to embedded DuckDB
- State management documentation updated

### Deprecated
- JSON file storage (migrated, backup preserved)

### Migration
- Run `python scripts/migrate_json_to_duckdb.py` to migrate existing cohorts
```

### Step 7: Verify All Links

```bash
# Check for broken links in markdown files
# You can use a tool like markdown-link-check or manually verify

find docs -name "*.md" -exec grep -l "\[.*\](.*\.md)" {} \;
```

### Step 8: Update hello-healthsim Examples

Review and update any examples that reference state management:

```bash
ls hello-healthsim/
# Check each example for state management references
```

### Step 9: Run Documentation Build (if applicable)

If there's a documentation build process, run it to verify everything works.

---

## Post-Flight Checklist

- [ ] New data-architecture.md created
- [ ] State management specification updated
- [ ] State management user guide updated
- [ ] State management skill updated
- [ ] PopulationSim skill updated
- [ ] README.md updated
- [ ] CHANGELOG.md updated
- [ ] HEALTHSIM-ARCHITECTURE-GUIDE.md updated
- [ ] All internal links verified working
- [ ] hello-healthsim examples still work
- [ ] No orphaned or outdated documentation

---

## Commit

```bash
git add -A
git commit -m "[Docs] Update documentation for DuckDB architecture

- Add data-architecture.md with full schema documentation
- Update state management specification and user guide
- Update state-management skill with new capabilities
- Update PopulationSim skill for DuckDB reference data
- Update CHANGELOG with all changes
- Update README architecture section
- Verify all internal documentation links

Part of: DuckDB Unified Data Architecture initiative"

git push
```

---

## Update MASTER-PLAN.md

Mark SESSION-06 as complete with commit hash.

---

## Success Criteria

✅ Session complete when:
1. All documentation reflects DuckDB architecture
2. No broken internal links
3. Skills have updated trigger phrases and examples
4. CHANGELOG documents all changes
5. README accurately describes current architecture
6. Examples in hello-healthsim still work
7. Committed and pushed

---

## Next Session

Proceed to [SESSION-07: Testing & Polish](SESSION-07-testing-polish.md)
