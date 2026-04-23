# HealthSim Workspace Pre-UAT Audit

**Started:** 2026-01-06
**Last Updated:** 2026-01-06
**Status:** IN PROGRESS

---

## Audit Scope

### Products
- [x] PatientSim - 486 tests passed, 10 skipped
- [x] MemberSim - 211 tests passed
- [x] RxMemberSim - 234 tests passed
- [x] TrialSim - 110 tests passed
- [ ] PopulationSim - No dedicated package (lives in core)
- [ ] NetworkSim - No dedicated package (lives in core)

### Cross-Cutting Features
- [x] Core Package (healthsim-core) - 1,708 tests passed, 2 skipped
- [x] Reference Data & DuckDB - Tests passing
- [x] State Management - Tests passing
- [x] MCP Servers - 125 tests passed
- [x] Output Formatters - Tests passing
- [ ] Skills System - Need to verify
- [ ] Cross-Product Integration - Need to verify
- [x] Generative Framework (Profiles, Journeys) - Tests passing

### Project Structure
- [x] VS Code workspace organization - Good
- [x] Git repo folder structure - Good
- [x] Package consistency - Core packages consistent

### Quality
- [x] All automated tests pass - 2,874 total tests passing
- [x] Smoke tests pass - 37/37 passed
- [ ] Code consistency across products - Need deeper review

### Documentation
- [ ] README files complete and accurate
- [ ] API documentation
- [ ] Guides and tutorials
- [ ] All links work - 171 broken found (mostly in archive)
- [ ] Navigation is clear

---

## Progress Log

### Phase 1: Project Structure Audit
Status: COMPLETE
- Verified package structure for core, patientsim, membersim, rxmembersim, trialsim
- Note: PopulationSim and NetworkSim don't have dedicated packages
- MCP server package exists separately

### Phase 2: Database/Migration Fix
Status: COMPLETE
- Found migration 1.5 bug: SELECT from `cohort_id` when column was still `scenario_id`
- Fixed migration SQL in migrations.py
- Applied migration to create cohorts, cohort_entities, cohort_tags tables
- Verified all MCP server tests now pass

### Phase 3: Test Suite Verification
Status: COMPLETE
- Core: 1,708 passed, 2 skipped
- PatientSim: 486 passed, 10 skipped
- MemberSim: 211 passed
- RxMemberSim: 234 passed
- TrialSim: 110 passed
- MCP Server: 125 passed
- **Total: 2,874 tests passing**

### Phase 4: Smoke Test Verification
Status: COMPLETE
- All 37 smoke tests passed
- Directory structure verified
- Oncology skills verified
- Reference data verified
- Cross-references verified
- Hello-HealthSim examples verified
- JSON validation passed

### Phase 5: Documentation Link Audit
Status: IN PROGRESS
- Found 171 broken links out of 2,494 total
- ~140 are in docs/archive/ (historical planning docs)
- ~31 are in active documentation

---

## Issues Found

### Critical (Must Fix Before UAT)
1. ✅ FIXED: Migration 1.5 bug - cohorts table not being created
   - Fixed: SELECT from scenario_id instead of cohort_id
   - Applied migration successfully

### Major (Should Fix)
1. **MCP README broken links** - packages/core/src/healthsim/mcp/README.md
   - Points to non-existent: api/profile-schema.md, api/journey-engine.md, guides/generative-framework.md
   
2. **Skills generation broken links** - skills/generation/README.md and SKILL.md
   - Points to non-existent: CURRENT-WORK.md

3. **Development Process doc** - docs/HEALTHSIM-DEVELOPMENT-PROCESS.md
   - Has placeholder example links that should be real examples

### Minor (Nice to Fix)
1. **Archive folder links** - ~140 broken links in docs/archive/
   - These are historical planning documents
   - Low priority but could be cleaned up

2. **Template placeholder links** - docs/skills-template.md
   - Has example placeholder links (expected for template)

### Deferred (Post-UAT)
1. PopulationSim/NetworkSim package structure
   - Currently live in core package
   - May want dedicated packages for consistency

---

## Fixes Applied

| Issue | File(s) | Commit |
|-------|---------|--------|
| Migration 1.5 SELECT bug | packages/core/src/healthsim/db/migrations.py | pending |
| Applied migration 1.5 | healthsim.duckdb | N/A (db) |

---

## Test Summary

| Package | Passed | Skipped | Failed |
|---------|--------|---------|--------|
| core | 1,708 | 2 | 0 |
| patientsim | 486 | 10 | 0 |
| membersim | 211 | 0 | 0 |
| rxmembersim | 234 | 0 | 0 |
| trialsim | 110 | 0 | 0 |
| mcp-server | 125 | 0 | 0 |
| **TOTAL** | **2,874** | **12** | **0** |

---

## Next Steps
1. Fix active documentation broken links
2. Commit migration fix
3. Review skills organization
4. Verify cross-product integration
5. Final documentation review

