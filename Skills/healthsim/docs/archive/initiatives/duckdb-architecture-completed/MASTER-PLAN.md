# DuckDB Unified Data Architecture - Master Plan

**Initiative**: Migrate HealthSim to DuckDB-based state management, analytics, and reference data  
**Status**: ✅ PHASE 1 COMPLETE  
**Started**: 2024-12-26  
**Phase 1 Completed**: 2024-12-26

---

## Executive Summary

This initiative consolidates HealthSim's storage architecture into a unified DuckDB database:
- **State Management**: Replace JSON files with DuckDB tables
- **Analytics**: Add optional star schema layer for OHDSI-style analysis
- **Reference Data**: Migrate PopulationSim CSVs to DuckDB

### Key Decisions (Locked)

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Database Engine | DuckDB | Analytics focus, MotherDuck path, already used |
| Schema Versioning | Migrations at load time | Handled in data loading process |
| Partial Analytics | Materialize all cohort entities | More data > less data for analytics users |
| MotherDuck | Deferred | Architect for it, implement later |
| Conflict Resolution | Latest wins (by UUID) | Simple approach, not building distributed DB |

---

## Phase 1: Foundation ✅ COMPLETE

**Goal**: Replace JSON state management with DuckDB, migrate PopulationSim data

| Session | Description | Status | Commit |
|---------|-------------|--------|--------|
| [SESSION-01](SESSION-01-foundation.md) | Database module, schema, connection management | ✅ Complete | 3349ad4 |
| [SESSION-02](SESSION-02-populationsim-migration.md) | Migrate PopulationSim CSVs to DuckDB | ✅ Complete | e41bfe0 |
| [SESSION-03](SESSION-03-state-management.md) | Update state management MCP tools | ✅ Complete | 7d984f3 |
| [SESSION-04](SESSION-04-json-compatibility.md) | JSON export/import for sharing | ✅ Complete | 4cf28ce |
| [SESSION-05](SESSION-05-migration-tool.md) | Migrate existing JSON cohorts | ✅ Complete | 8a184e0 |
| [SESSION-06](SESSION-06-documentation.md) | Update all docs, skills, tutorials | ✅ Complete | aeb3314 |
| SESSION-06.5 | Doc cleanup: prerequisites, reference data, enterprise exports | ✅ Complete | 693d204 |
| [SESSION-07](SESSION-07-testing-polish.md) | Integration testing, cleanup | ✅ Complete | (this commit) |

### Phase 1 Success Criteria

- [x] `~/.healthsim/healthsim.duckdb` created on first use
- [x] All existing MCP state tools work with DuckDB backend
- [x] PopulationSim queries work against DuckDB tables
- [x] JSON export produces identical output to current format
- [x] Existing JSON cohorts migrated successfully
- [x] All 605 tests still passing
- [x] Documentation updated, no broken links
- [x] Skills updated with new capabilities

### Phase 1 Summary

| Metric | Value |
|--------|-------|
| Tests | 605 passed |
| Database Size | 86 MB (vs 142 MB CSV = 1.7x compression) |
| Reference Tables | 5 tables, 416K rows |
| Performance | All targets met (save/load/list) |

---

## Phase 2: Analytics Layer (After Phase 1)

**Goal**: Add star schema transformation for OHDSI-style analytics

| Session | Description | Status | Commit |
|---------|-------------|--------|--------|
| SESSION-08 | Star schema design, DDL | ⬜ Not Started | - |
| SESSION-09 | Canonical → Star transformation | ⬜ Not Started | - |
| SESSION-10 | Batch generation mode | ⬜ Not Started | - |
| SESSION-11 | Analytics MCP tools | ⬜ Not Started | - |
| SESSION-12 | Analytics skills integration | ⬜ Not Started | - |

---

## Phase 3: Scale & Cloud (Future)

**Goal**: MotherDuck integration, Databricks export, team sharing

*Sessions to be defined after Phase 2 completion*

---

## Architecture Reference

```
~/.healthsim/
  healthsim.duckdb                 # Unified database
    ├── Canonical Tables           # patients, encounters, claims, etc.
    ├── State Management Tables    # cohorts, cohort_entities, cohort_tags
    ├── Analytics Tables           # dim_*, fact_* (Phase 2)
    └── Reference Tables           # cdc_places, svi, adi, nppes (optional)
```

### Layer Summary

| Layer | Purpose | When Populated |
|-------|---------|----------------|
| Canonical | Source of truth, mirrors JSON models | On generation/save |
| State Management | Cohort organization | On save/load |
| Analytics | Star schema for OHDSI analysis | On explicit request (Phase 2) |
| Reference | External data (CDC, NPPES) | On init/import |

---

## Files Changed/Created

### New Files
- `packages/core/healthsim/db/` - Database module
  - `__init__.py`
  - `schema.py` - DDL definitions
  - `connection.py` - Connection management
  - `migrations.py` - Schema versioning
- `packages/core/healthsim/db/reference/` - Reference data loaders
  - `populationsim.py`
  - `networksim.py` (optional)
- `scripts/migrate_json_to_duckdb.py`
- `scripts/import_reference_data.py`
- `docs/data-architecture.md` - New architecture guide

### Modified Files
- `packages/core/healthsim/state/manager.py` - DuckDB backend
- `skills/common/state-management.md` - Updated capabilities
- `docs/state-management/specification.md` - Updated for DuckDB
- `docs/state-management/user-guide.md` - Updated for DuckDB
- `CHANGELOG.md`
- `README.md`

### Deprecated/Removed
- `~/.healthsim/cohorts/*.json` - Migrated to DuckDB, kept as backup

---

## Session Recovery

If starting fresh or after interruption:

```bash
# 1. Check current state
cd /Users/markoswald/Developer/projects/healthsim-workspace
git status
git log --oneline -5

# 2. Read this file for current session status

# 3. Read CURRENT-WORK.md for overall project state
cat docs/CURRENT-WORK.md

# 4. Resume from the next incomplete session above
```

---

## Related Documents

- [Design Document](../../healthsim-duckdb-architecture.html) - Full architecture specification
- [State Management Skill](../../../skills/common/state-management.md) - Current implementation
- [State Management Spec](../state-management/specification.md) - MCP tool specs
- [CURRENT-WORK.md](../../CURRENT-WORK.md) - Live project state

---

## Status Legend

- ⬜ Not Started
- 🟡 In Progress
- ✅ Complete
- ❌ Blocked
- ⏸️ Paused

---

*Last Updated: 2024-12-26 (Phase 1 Complete)*
