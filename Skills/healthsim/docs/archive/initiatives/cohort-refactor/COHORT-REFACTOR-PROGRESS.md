# Cohort Refactoring Progress

**Started:** 2026-01-04
**Goal:** Rename database tables/columns from scenario→cohort

## Scope (STRICT)
- ✅ Database table names: scenarios→cohorts, scenario_entities→cohort_entities, scenario_tags→cohort_tags
- ✅ Database column names: scenario_id→cohort_id
- ✅ SQL strings in Python code
- ❌ NOT Python method names (keep save_scenario, load_scenario, etc.)
- ❌ NOT Python variable names
- ❌ NOT dataclass field names
- ❌ NOT class names

## Phase 1: Database Schema

| File | Status | Tests |
|------|--------|-------|
| schema.py | ⬜ | - |
| migrations.py | ⬜ | - |
| queries.py | ⬜ | - |

## Phase 2: SQL Strings in State Management

| File | Status | Tests |
|------|--------|-------|
| state/manager.py | ⬜ | - |
| state/auto_persist.py | ⬜ | - |
| state/summary.py | ⬜ | - |
| state/auto_naming.py | ⬜ | - |

## Phase 3: Test Files (SQL strings only)

| File | Status | Tests |
|------|--------|-------|
| tests/db/test_schema.py | ⬜ | - |
| tests/state/test_manager.py | ⬜ | - |
| tests/state/test_summary.py | ⬜ | - |

## Commits
| Phase | Commit | Tests |
|-------|--------|-------|
| - | - | - |

---
*Last updated: Starting*
