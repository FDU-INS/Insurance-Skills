# Cohort Refactoring - COMPLETE ✅

**Completed:** 2026-01-04 11:15 UTC
**Final Test Result:** 295 passed, 0 failed (core tests)

## Summary

The Scenario→Cohort terminology refactoring is **COMPLETE**. All user-facing AND internal code now uses "cohort" terminology consistently.

## What Changed

### Database Schema (Phase 1)
- Tables: `scenarios`→`cohorts`, `scenario_entities`→`cohort_entities`, `scenario_tags`→`cohort_tags`
- Columns: `scenario_id`→`cohort_id` throughout
- Migration v1.5 added for existing databases

### State Management (Phase 2)
- SQL queries updated to use new table/column names
- Entity serialization uses `cohort_id` for database inserts

### MCP Server (Phase 3)
- Tool names: `healthsim_list_cohorts`, `healthsim_load_cohort`, `healthsim_save_cohort`, etc.
- SQL statements use cohorts/cohort_entities/cohort_tags tables

### Skills & Documentation (Phases 4-5)
- All skill files updated with cohort terminology
- README files, tutorials, architecture docs updated

### Directory Structure (Phase 6)
- `scenarios/` directory renamed to `cohorts/`

### Migration Module (Phase 7)
- `json_scenarios.py` → `json_cohorts.py`
- All migration function names updated

### Complete Internal Rename (Phase 8) ← NEW
- **Methods renamed**:
  - `save_scenario` → `save_cohort`
  - `load_scenario` → `load_cohort`
  - `list_scenarios` → `list_cohorts`
  - `delete_scenario` → `delete_cohort`
  - `get_scenario_summary` → `get_cohort_summary`
  - `query_scenario` → `query_cohort`
  - etc.

- **Classes renamed**:
  - `ScenarioSummary` → `CohortSummary`
  - `ScenarioBrief` → `CohortBrief`

- **Parameters renamed**:
  - `scenario_id` → `cohort_id`
  - `scenario_name` → `cohort_name`
  - `scenario_id_or_name` → `cohort_id_or_name`

- **Files updated**:
  - `packages/core/src/healthsim/state/` (all files)
  - `packages/patientsim/src/mcp/` (session, state_server, formatters)
  - `packages/mcp-server/healthsim_mcp.py`
  - Test files across packages

## What Was NOT Changed (By Design)

The `membersim/scenarios/` and `rxmembersim/scenarios/` directories were **intentionally NOT renamed**. These contain **event sequence templates** (like "diabetic_member", "new_therapy_start") - a different concept from saved data cohorts:

- **Cohort**: A saved collection of entities (patients, members, etc.)
- **Scenario**: A template describing a sequence of events over time

This distinction is correct healthcare/simulation domain terminology.

## Git Commits

| Commit | Phase | Description |
|--------|-------|-------------|
| f480fb6 | 1.1 | schema.py - Table renames |
| 1c66f99 | 1.2 | migrations.py - Add v1.5 migration |
| 21f998d | 1.3 | queries.py - Function renames |
| 84716e8 | 1.4 | db/__init__.py - Export updates |
| bf488ca | 2.1 | summary.py - SQL updates |
| db09f50 | 2.2 | manager.py - SQL updates |
| 929a019 | 2.3 | auto_persist.py - Column fixes |
| f22124b | 2.4 | auto_naming.py - Table reference |
| 1255e2d | 3 | MCP Server - Tool renames |
| 1eedfc6 | 3.1 | MCP Server tests |
| 6259b7c | 4 | Skills documentation |
| 4267da8 | 5 | Documentation updates |
| 87b5612 | 3 | MCP Server additional updates |
| 737d74f | 4 | Skills additional updates |
| db3ea12 | 5 | Documentation additional updates |
| 72c8db1 | 6 | Directory rename scenarios→cohorts |
| 8ef68e6 | 7 | Migration module and test fixes |
| 00286ae | 8 | Final validation marker |
| ab0b168 | 8+ | Complete internal rename |

## Verification

```bash
# Run core tests
cd packages/core && source .venv/bin/activate
python -m pytest tests/db/ tests/state/ --tb=no -q
# Result: 295 passed

# Search for remaining scenario references in core state module
grep -r "scenario" packages/core/src/healthsim/state/ | grep -v __pycache__
# Result: No matches (clean)
```
