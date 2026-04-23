# Cohort → Cohort Refactoring Plan

**Status:** 🔵 IN PROGRESS  
**Started:** 2026-01-04  
**Target:** Rename "Cohort" to "Cohort" throughout the codebase

---

## Executive Summary

| Category | Files | Status |
|----------|-------|--------|
| Phase 1: Database Schema | 3 files | ⬜ Not Started |
| Phase 2: Core Python | 15 files | ⬜ Not Started |
| Phase 3: MCP Server | 8 files | ⬜ Not Started |
| Phase 4: Skills | 12 files | ⬜ Not Started |
| Phase 5: Documentation | ~80 files | ⬜ Not Started |
| Phase 6: Directory Structure | 2 directories | ⬜ Not Started |
| Phase 7: Tests | 25 files | ⬜ Not Started |
| Phase 8: Final Validation | - | ⬜ Not Started |

---

## Terminology Changes

| Old Term | New Term | Context |
|----------|----------|---------|
| `cohort` | `cohort` | General usage |
| `cohorts` | `cohorts` | Table name, plural |
| `cohort_id` | `cohort_id` | Column/field name |
| `cohort_entities` | `cohort_entities` | Table name |
| `cohort_tags` | `cohort_tags` | Table name |
| `healthsim_list_cohorts` | `healthsim_list_cohorts` | MCP tool |
| `healthsim_load_cohort` | `healthsim_load_cohort` | MCP tool |
| `healthsim_save_cohort` | `healthsim_save_cohort` | MCP tool |
| `healthsim_delete_cohort` | `healthsim_delete_cohort` | MCP tool |
| `healthsim_get_cohort_summary` | `healthsim_get_cohort_summary` | MCP tool |
| `CohortManager` | `CohortManager` | Class name |
| `save_cohort` | `save_cohort` | Method name |
| `load_cohort` | `load_cohort` | Method name |
| `delete_cohort` | `delete_cohort` | Method name |
| `list_cohorts` | `list_cohorts` | Method name |
| `cohorts/saved/` | `cohorts/saved/` | Directory path |

---

## Phase 1: Database Schema

**Critical - Must be done first and carefully**

### 1.1 Schema Definition File
**File:** `packages/core/src/healthsim/db/schema.py`

| Change | Status |
|--------|--------|
| Rename `SCENARIO_ENTITIES_SEQ_DDL` → `COHORT_ENTITIES_SEQ_DDL` | ⬜ |
| Rename `SCENARIO_TAGS_SEQ_DDL` → `COHORT_TAGS_SEQ_DDL` | ⬜ |
| Rename `SCENARIOS_DDL` → `COHORTS_DDL` | ⬜ |
| Rename `SCENARIO_ENTITIES_DDL` → `COHORT_ENTITIES_DDL` | ⬜ |
| Rename `SCENARIO_TAGS_DDL` → `COHORT_TAGS_DDL` | ⬜ |
| Change table name `cohorts` → `cohorts` | ⬜ |
| Change table name `cohort_entities` → `cohort_entities` | ⬜ |
| Change table name `cohort_tags` → `cohort_tags` | ⬜ |
| Change column `cohort_id` → `cohort_id` in all tables | ⬜ |
| Update all index names from `cohort` → `cohort` | ⬜ |
| Update `get_state_tables()` return values | ⬜ |
| Increment `SCHEMA_VERSION` to "1.5" | ⬜ |

### 1.2 Migration Script
**File:** `packages/core/src/healthsim/db/migrations.py`

| Change | Status |
|--------|--------|
| Create migration v1.5 for cohort→cohort rename | ⬜ |
| Rename tables: cohorts→cohorts, cohort_entities→cohort_entities, cohort_tags→cohort_tags | ⬜ |
| Rename columns: cohort_id→cohort_id in all tables | ⬜ |
| Rename sequences | ⬜ |
| Rename indexes | ⬜ |

### 1.3 Query Files
**File:** `packages/core/src/healthsim/db/queries.py`

| Change | Status |
|--------|--------|
| Update all SQL queries to use `cohorts` table | ⬜ |
| Update all SQL queries to use `cohort_entities` table | ⬜ |
| Update all SQL queries to use `cohort_tags` table | ⬜ |
| Update all references to `cohort_id` → `cohort_id` | ⬜ |

### 1.4 Tests
**Files:** `packages/core/tests/db/test_schema.py`, `test_migration.py`

| Change | Status |
|--------|--------|
| Update table name assertions | ⬜ |
| Add migration v1.5 test | ⬜ |

---

## Phase 2: Core Python (State Management)

### 2.1 Manager Class
**File:** `packages/core/src/healthsim/state/manager.py`

| Change | Status |
|--------|--------|
| Rename class `CohortManager` → `CohortManager` | ⬜ |
| Rename method `save_cohort` → `save_cohort` | ⬜ |
| Rename method `load_cohort` → `load_cohort` | ⬜ |
| Rename method `delete_cohort` → `delete_cohort` | ⬜ |
| Rename method `list_cohorts` → `list_cohorts` | ⬜ |
| Rename method `get_cohort` → `get_cohort` | ⬜ |
| Rename method `tag_cohort` → `tag_cohort` | ⬜ |
| Update all SQL queries | ⬜ |
| Update all variable names | ⬜ |
| Update all docstrings | ⬜ |

### 2.2 Auto-Persist
**File:** `packages/core/src/healthsim/state/auto_persist.py`

| Change | Status |
|--------|--------|
| Update `cohort_id` references → `cohort_id` | ⬜ |
| Update docstrings | ⬜ |

### 2.3 Auto-Naming
**File:** `packages/core/src/healthsim/state/auto_naming.py`

| Change | Status |
|--------|--------|
| Update naming logic for cohorts | ⬜ |
| Update docstrings | ⬜ |

### 2.4 Summary
**File:** `packages/core/src/healthsim/state/summary.py`

| Change | Status |
|--------|--------|
| Update all cohort references | ⬜ |

### 2.5 Serializers
**File:** `packages/core/src/healthsim/state/serializers.py`

| Change | Status |
|--------|--------|
| Update cohort references | ⬜ |

### 2.6 Workspace
**File:** `packages/core/src/healthsim/state/workspace.py`

| Change | Status |
|--------|--------|
| Update cohort references | ⬜ |

### 2.7 Init File
**File:** `packages/core/src/healthsim/state/__init__.py`

| Change | Status |
|--------|--------|
| Update exports (`CohortManager` → `CohortManager`) | ⬜ |
| Add backwards-compat alias if needed | ⬜ |

### 2.8 Legacy File
**File:** `packages/core/src/healthsim/state/legacy.py`

| Change | Status |
|--------|--------|
| Update cohort references | ⬜ |

### 2.9 JSON Migration
**File:** `packages/core/src/healthsim/db/migrate/json_cohorts.py`

| Change | Status |
|--------|--------|
| Rename file to `json_cohorts.py` | ⬜ |
| Update function names and docstrings | ⬜ |

---

## Phase 3: MCP Server

### 3.1 Main MCP File
**File:** `packages/mcp-server/healthsim_mcp.py`

| Change | Status |
|--------|--------|
| Rename tool `healthsim_list_cohorts` → `healthsim_list_cohorts` | ⬜ |
| Rename tool `healthsim_load_cohort` → `healthsim_load_cohort` | ⬜ |
| Rename tool `healthsim_save_cohort` → `healthsim_save_cohort` | ⬜ |
| Rename tool `healthsim_delete_cohort` → `healthsim_delete_cohort` | ⬜ |
| Rename tool `healthsim_get_cohort_summary` → `healthsim_get_cohort_summary` | ⬜ |
| Update all docstrings | ⬜ |
| Update all example code in docstrings | ⬜ |
| Update header comments | ⬜ |

### 3.2 MCP Tests
**Files:** All files in `packages/mcp-server/tests/`

| Change | Status |
|--------|--------|
| `test_add_entities.py` - Update cohort references | ⬜ |
| `test_canonical_e2e.py` - Update cohort references | ⬜ |
| `test_canonical_insert.py` - Update cohort references | ⬜ |
| `test_close_before_write.py` - Update cohort references | ⬜ |
| `test_connection_concurrency.py` - Update cohort references | ⬜ |
| `test_dual_connection.py` - Update cohort references | ⬜ |
| `test_entity_type_validation.py` - Update cohort references | ⬜ |

---

## Phase 4: Skills

### 4.1 State Management Skill (Critical)
**File:** `skills/common/state-management.md`

| Change | Status |
|--------|--------|
| Rename entire skill focus from Cohort to Cohort | ⬜ |
| Update frontmatter description | ⬜ |
| Update all trigger phrases | ⬜ |
| Update all conversation examples | ⬜ |
| Update all commands | ⬜ |

### 4.2 DuckDB Skill
**File:** `skills/common/duckdb-skill.md`

| Change | Status |
|--------|--------|
| Update cohort table references | ⬜ |

### 4.3 Identity Correlation
**File:** `skills/common/identity-correlation.md`

| Change | Status |
|--------|--------|
| Update cohort references | ⬜ |

### 4.4 Generation Skills
**Files:** All files in `skills/generation/`

| Change | Status |
|--------|--------|
| SKILL.md - Update cohort references | ⬜ |
| executors/profile-executor.md | ⬜ |
| executors/journey-executor.md | ⬜ |
| builders/quick-generate.md | ⬜ |

### 4.5 Product Skills
**Files:** All product SKILL.md files

| Change | Status |
|--------|--------|
| `skills/patientsim/SKILL.md` | ⬜ |
| `skills/membersim/SKILL.md` | ⬜ |
| `skills/rxmembersim/SKILL.md` | ⬜ |
| `skills/trialsim/SKILL.md` | ⬜ |

---

## Phase 5: Documentation

### 5.1 Root-Level Files
| File | Status |
|------|--------|
| `README.md` | ⬜ |
| `SKILL.md` | ⬜ |
| `CHANGELOG.md` | ⬜ |

### 5.2 Architecture Docs
| File | Status |
|------|--------|
| `docs/HEALTHSIM-ARCHITECTURE-GUIDE.md` | ⬜ |
| `docs/HEALTHSIM-DEVELOPMENT-PROCESS.md` | ⬜ |
| `docs/data-architecture.md` | ⬜ |
| `docs/healthsim-duckdb-schema.md` | ⬜ |
| `docs/integration-guide.md` | ⬜ |

### 5.3 MCP Docs
| File | Status |
|------|--------|
| `docs/mcp/configuration.md` | ⬜ |
| `docs/mcp/development-guide.md` | ⬜ |
| `docs/mcp/duckdb-connection-architecture.md` | ⬜ |
| `docs/mcp/integration-guide.md` | ⬜ |

### 5.4 Hello HealthSim
| File | Status |
|------|--------|
| `hello-healthsim/README.md` | ⬜ |
| `hello-healthsim/CLAUDE-CODE.md` | ⬜ |
| `hello-healthsim/CLAUDE-DESKTOP.md` | ⬜ |
| `hello-healthsim/EXTENDING.md` | ⬜ |
| `hello-healthsim/TROUBLESHOOTING.md` | ⬜ |

### 5.5 Examples
| File | Status |
|------|--------|
| `hello-healthsim/examples/README.md` | ⬜ |
| `hello-healthsim/examples/auto-persist-examples.md` | ⬜ |
| `hello-healthsim/examples/cross-domain-examples.md` | ⬜ |
| `hello-healthsim/examples/generation-examples.md` | ⬜ |
| All other example files | ⬜ |

### 5.6 Tutorials
| File | Status |
|------|--------|
| All files in `hello-healthsim/tutorials/` | ⬜ |

### 5.7 Package READMEs
| File | Status |
|------|--------|
| `packages/README.md` | ⬜ |
| `packages/core/README.md` | ⬜ |
| `packages/mcp-server/README.md` | ⬜ |
| `packages/patientsim/README.md` | ⬜ |
| `packages/membersim/README.md` | ⬜ |
| `packages/rxmembersim/README.md` | ⬜ |

### 5.8 Initiative Docs
| File | Status |
|------|--------|
| `docs/initiatives/generative-framework/CONCEPTUAL-ARCHITECTURE.md` | ⬜ |
| `docs/initiatives/generative-framework/IMPLEMENTATION-SUMMARY.md` | ⬜ |
| `docs/initiatives/generative-framework/GENERATIVE-FRAMEWORK-MASTER-PLAN.md` | ⬜ |

### 5.9 Archive Docs (Lower Priority)
| Category | Status |
|----------|--------|
| `docs/archive/` - All files (update if breaking links) | ⬜ |

---

## Phase 6: Directory Structure

### 6.1 Rename Directories
| Change | Status |
|--------|--------|
| `cohorts/saved/` → `cohorts/saved/` | ⬜ |
| Update all path references in code | ⬜ |
| Update all path references in docs | ⬜ |

### 6.2 Tools
| File | Status |
|------|--------|
| `tools/cohort_loader.py` → `tools/cohort_loader.py` | ⬜ |
| `tools/cohort_saver.py` → `tools/cohort_saver.py` | ⬜ |

---

## Phase 7: Tests

### 7.1 Core Tests
| File | Status |
|------|--------|
| `packages/core/tests/state/test_manager.py` | ⬜ |
| `packages/core/tests/state/test_auto_persist.py` | ⬜ |
| `packages/core/tests/state/test_auto_persist_integration.py` | ⬜ |
| `packages/core/tests/state/test_auto_persist_phase2.py` | ⬜ |
| `packages/core/tests/state/test_auto_naming.py` | ⬜ |
| `packages/core/tests/state/test_json_compat.py` | ⬜ |
| `packages/core/tests/state/test_provenance.py` | ⬜ |
| `packages/core/tests/state/test_summary.py` | ⬜ |

### 7.2 Package Tests
| File | Status |
|------|--------|
| `packages/patientsim/tests/core/test_state.py` | ⬜ |
| `packages/patientsim/tests/skills/test_cohorts.py` → rename | ⬜ |
| `packages/membersim/tests/test_cohorts.py` → rename | ⬜ |
| `packages/rxmembersim/tests/test_cohorts.py` → rename | ⬜ |

---

## Phase 8: Final Validation

| Task | Status |
|------|--------|
| Run all smoke tests | ⬜ |
| Run all unit tests | ⬜ |
| Run all integration tests | ⬜ |
| Verify database migration works on existing data | ⬜ |
| Manual testing of MCP tools | ⬜ |
| Search for any remaining "cohort" references | ⬜ |
| Update CHANGELOG.md with v2.1.0-cohort entry | ⬜ |
| Git commit and tag v2.1.0-cohort | ⬜ |
| Git push | ⬜ |

---

## Execution Order

```
Phase 1: Database Schema
    ↓
Phase 2: Core Python
    ↓
Phase 3: MCP Server
    ↓
    [RUN TESTS - Must pass before continuing]
    ↓
Phase 4: Skills
    ↓
Phase 5: Documentation
    ↓
Phase 6: Directory Structure
    ↓
Phase 7: Tests (file renames)
    ↓
Phase 8: Final Validation
```

---

## Rollback Plan

If issues are found during migration:

1. **Database**: Keep old table names as aliases initially
   ```sql
   CREATE VIEW cohorts AS SELECT * FROM cohorts;
   ```

2. **MCP Tools**: Consider deprecation period with aliases
   ```python
   # Alias old names to new
   healthsim_list_cohorts = healthsim_list_cohorts
   ```

3. **Git**: Tag before starting (`pre-cohort-refactor`)

---

## Progress Log

| Date | Phase | Action | Result |
|------|-------|--------|--------|
| 2026-01-04 | Plan | Created refactoring plan | ✅ |
| | | | |

---

*Last Updated: 2026-01-04*
