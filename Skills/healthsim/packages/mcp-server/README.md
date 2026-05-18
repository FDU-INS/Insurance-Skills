# HealthSim MCP Server

MCP (Model Context Protocol) server for the HealthSim healthcare data simulation platform.

## Purpose

This server provides a **single connection holder** to the HealthSim DuckDB database, solving the file locking issue that prevents multiple processes from accessing the database simultaneously.

## Installation

```bash
cd /Users/markoswald/Developer/projects/healthsim-workspace/packages/mcp-server
pip install -e .
```

Or install dependencies directly:

```bash
pip install mcp pydantic duckdb
```

## Configuration

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "healthsim-mcp": {
      "command": "/Users/markoswald/anaconda3/bin/python",
      "args": [
        "/Users/markoswald/Developer/projects/healthsim-workspace/packages/mcp-server/healthsim_mcp.py"
      ],
      "env": {
        "PYTHONPATH": "/Users/markoswald/Developer/projects/healthsim-workspace/packages/core/src:/Users/markoswald/Developer/projects/healthsim-workspace/packages/mcp-server"
      }
    }
  }
}
```

**Important**: 
1. Remove the old `healthsim-duckdb` entry to avoid conflicts
2. Adjust the Python path to match your environment (`which python3`)

## Available Tools

### Cohort Management

| Tool | Description |
|------|-------------|
| `healthsim_list_cohorts` | List all saved cohorts |
| `healthsim_load_cohort` | Load a cohort by name/ID |
| `healthsim_save_cohort` | Save entities as a cohort (full replacement) |
| `healthsim_add_entities` | Add entities incrementally (recommended for large datasets) |
| `healthsim_delete_cohort` | Delete a cohort (requires confirm=True) |
| `healthsim_get_cohort_summary` | Get token-efficient cohort summary |

### Database Queries

| Tool | Description |
|------|-------------|
| `healthsim_query` | Execute read-only SQL queries |
| `healthsim_query_reference` | Query PopulationSim reference data |
| `healthsim_search_providers` | Search REAL NPPES provider data (8.9M records) |
| `healthsim_tables` | List all database tables |

## Real vs Synthetic Data Decision

HealthSim uses a "real data first" approach. **Always query real reference data before generating synthetic data**:

| Entity Type | Data Source | Why |
|-------------|-------------|-----|
| **Providers/Facilities** | Use `healthsim_search_providers` (NPPES) | 8.9M real registered providers |
| **Demographics/Health** | Use `healthsim_query_reference` (CDC/SVI) | Real population health data |
| **Patients/Members/Claims** | Generate SYNTHETIC | PHI - must be synthetic |

### When to Use Real vs Synthetic

```
User: "Add PCPs to the Rewire Health cohort"

✅ CORRECT: Query real NPPES data first
   healthsim_search_providers(state="CA", city="San Diego", specialty="Family Medicine")
   Then add real providers to cohort

❌ WRONG: Generate synthetic providers immediately
   healthsim_add_entities(entities={"providers": [generated_fake_npis...]})
```

**Only generate synthetic providers if:**
- Real data is unavailable for the geography
- User explicitly requests synthetic data
- Testing requires controlled/predictable NPIs

## Entity Type Taxonomy

HealthSim enforces a clear separation between **cohort data**, **relationship data**, and **reference data**:

### Cohort Data (Stored per-cohort)

These are synthetic PHI entities that are generated for each cohort:

| Entity Type | Description | Example Fields |
|-------------|-------------|----------------|
| `patients` | Synthetic patient demographics | patient_id, name, dob, address |
| `members` | Synthetic insurance enrollment | member_id, patient_id, plan_id |
| `claims` | Synthetic claims/utilization | claim_id, member_id, service_date |
| `claim_lines` | Synthetic claim line items | claim_line_id, procedure_code |
| `encounters` | Synthetic clinical encounters | encounter_id, diagnosis_codes |
| `prescriptions` | Synthetic medication records | rx_id, ndc, quantity |
| `subjects` | Clinical trial subjects | subject_id, enrollment_date |

### Relationship Data (Stored per-cohort)

These link cohort data to reference data via IDs/NPIs:

| Entity Type | Description | Key Fields |
|-------------|-------------|------------|
| `pcp_assignments` | Member → Provider relationships | member_id, provider_npi, effective_date |
| `network_contracts` | Plan → Provider contracts | plan_id, provider_npi, contract_type |
| `authorizations` | Service authorizations | member_id, service_code, provider_npi |
| `referrals` | Provider → Provider referrals | member_id, from_npi, to_npi |
| `facility_assignments` | Member → Facility assignments | member_id, facility_npi |

### Reference Data (Query directly, never copy)

These exist in shared tables and should **NEVER** be added to cohorts:

| Entity Type | Query Tool | Table |
|-------------|-----------|-------|
| `providers` | `healthsim_search_providers` | `network.providers` (8.9M records) |
| `facilities` | `healthsim_search_providers` | `network.providers` (entity_type=2) |
| `pharmacies` | `healthsim_query` | `network.providers` (taxonomy LIKE '333600%') |
| `hospitals` | `healthsim_search_providers` | `network.providers` (taxonomy LIKE '282N%') |

### Validation Enforcement

The `healthsim_add_entities` and `healthsim_save_cohort` tools will **suggest using real data** when you try to store reference types, but allow override when synthetic data is explicitly needed:

```
⚠️ 'providers' is typically REFERENCE DATA that exists in shared tables.

RECOMMENDED: Use real data from network.providers (8.9M+ records):
  → healthsim_search_providers(state='CA', specialty='Family Medicine')
  → Then store relationships via 'pcp_assignments' or 'network_contracts'

TO OVERRIDE: If you intentionally need synthetic providers for testing/demos,
set allow_reference_entities=True in your request.
```

### Correct Pattern Example

```python
# ⚠️ SUGGESTS REAL DATA (default behavior)
healthsim_add_entities(entities={
    "providers": [{"npi": "123", "name": "Dr. Smith", ...}]
})
# → Returns suggestion to use healthsim_search_providers

# ✅ OVERRIDE: Intentionally use synthetic providers
healthsim_add_entities(
    entities={"providers": [{"npi": "123", "name": "Dr. Smith"}]},
    allow_reference_entities=True  # Explicit override
)

# ✅ RECOMMENDED: Store relationship, query reference data
healthsim_add_entities(entities={
    "pcp_assignments": [{"member_id": "M001", "provider_npi": "1234567890"}]
})

# For analytics, JOIN to reference table:
# SELECT m.*, p.name as pcp_name 
# FROM cohort_members m
# JOIN network.providers p ON m.provider_npi = p.npi
```

## save_cohort vs add_entities

The two write tools have different behaviors. **Claude automatically selects the right tool** based on entity count:

| Feature | `save_cohort` | `add_entities` |
|---------|-----------------|----------------|
| **When to use** | ≤50 entities total | >50 entities OR incremental |
| Behavior | Replace all entities | Upsert (add/update only) |
| Safe for batching | ❌ No (overwrites) | ✅ Yes |
| Creates cohort | Yes | Yes (if not exists) |
| Token efficient | ❌ Echoes all data | ✅ Returns summary only |

### Automatic Tool Selection

The tool descriptions guide Claude to automatically choose:

- **≤50 entities**: `save_cohort` (simple, atomic)
- **>50 entities**: `add_entities` in batches of ~50 (avoids truncation)
- **Adding to existing**: Always `add_entities` (upsert, non-destructive)

You don't need to specify which tool to use - just describe what you want and Claude will pick appropriately.

### When to use `add_entities`

Use `healthsim_add_entities` when:
- Creating cohorts with 100+ entities
- Streaming data in batches to avoid token limits
- Adding new entity types to existing cohorts
- Updating specific entities without affecting others

**Example: Building a cohort in batches**

```python
# Batch 1: Create cohort with first 50 patients
healthsim_add_entities(
    cohort_name="My Large Cohort",
    entities={"patients": first_50_patients},
    batch_number=1,
    total_batches=4
)
# Returns: {"cohort_id": "abc-123", ...}

# Batch 2-4: Add remaining patients using cohort_id
healthsim_add_entities(
    cohort_id="abc-123",
    entities={"patients": next_50_patients},
    batch_number=2,
    total_batches=4
)

# Add different entity types
healthsim_add_entities(
    cohort_id="abc-123",
    entities={"members": member_list}
)
```

## Reference Data Tables

| Table | Rows | Description |
|-------|------|-------------|
| `population.places_county` | 3,143 | CDC PLACES county-level health indicators |
| `population.places_tract` | 83,522 | CDC PLACES tract-level health indicators |
| `population.svi_county` | 3,144 | Social Vulnerability Index by county |
| `population.svi_tract` | 84,120 | Social Vulnerability Index by tract |
| `population.adi_blockgroup` | 242,336 | Area Deprivation Index by block group |

## Usage Examples

### List cohorts
```
Use healthsim_list_cohorts to see what's saved
```

### Query reference data
```
Use healthsim_query_reference with table="places_county" and state="CA"
```

### Save a cohort (small dataset)
```
Use healthsim_save_cohort with:
- name: "my-cohort"
- entities: {"patients": [...], "encounters": [...]}
- description: "Test cohort"
- tags: ["test", "demo"]
```

### Add entities incrementally (large dataset)
```
Use healthsim_add_entities with:
- cohort_name: "my-large-cohort"  # Creates if not exists
- entities: {"patients": [...]}
- batch_number: 1
- total_batches: 4

Then for subsequent batches:
- cohort_id: "uuid-from-first-call"
- entities: {"patients": [...]}
- batch_number: 2
- total_batches: 4
```

### Search for real providers
```
Use healthsim_search_providers with:
- state: "CA"
- city: "San Diego"
- specialty: "Family Medicine"
- entity_type: "individual"
- limit: 50
```

Or search by taxonomy code:
```
Use healthsim_search_providers with:
- state: "CA"
- taxonomy_code: "207Q00000X"  # Family Medicine
- limit: 20
```

### Run custom SQL
```
Use healthsim_query with:
- sql: "SELECT countyname, obesity_crudeprev FROM ref_places_county WHERE stateabbr = 'TX' ORDER BY obesity_crudeprev DESC LIMIT 10"
```

## Database Location

The HealthSim database is stored at: `~/.healthsim/healthsim.duckdb`

## Troubleshooting

### Lock conflict error
If you see "Could not set lock on file", ensure:
1. The old `healthsim-duckdb` MCP server is removed from config
2. No Python processes are holding the database connection
3. Restart Claude Desktop after config changes

### Module not found
Ensure the healthsim core package is importable:
```bash
cd /Users/markoswald/Developer/projects/healthsim-workspace
source .venv/bin/activate
python -c "from healthsim.state import StateManager; print('OK')"
```

### Batch truncation issues
If large entity lists are being truncated when using `save_cohort`:
- Switch to `healthsim_add_entities` for batched operations
- Keep batches to ≤50 entities per call
- Use batch_number/total_batches for progress tracking
