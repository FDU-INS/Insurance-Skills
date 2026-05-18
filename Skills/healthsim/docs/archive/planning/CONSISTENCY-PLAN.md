# HealthSim Product Consistency Plan

## Completed ✅

### Phase 1: PatientSim State Server Terminology
- [x] Renamed user-facing messages from "Scenario" to "Cohort"
- [x] Updated formatters.py: "Scenario" → "Skill" in output

### Phase 2: Remove PatientSim Legacy Structure
- [x] Removed `packages/patientsim/src/core/` (duplicate)
- [x] Removed `packages/patientsim/src/dimensional/`
- [x] Removed `packages/patientsim/src/formats/`
- [x] Removed `packages/patientsim/src/mcp/`
- [x] Removed `packages/patientsim/src/validation/`
- [x] Canonical structure: `packages/patientsim/src/patientsim/`

### Phase 3: Implement TrialSim Package
- [x] Created complete package structure
- [x] Implemented core models (Subject, Site, Protocol, Visit, AdverseEvent, Exposure)
- [x] Implemented generators (TrialSubjectGenerator, VisitGenerator, AdverseEventGenerator, ExposureGenerator)
- [x] Created test suite (16 tests passing)
- [x] Added CLAUDE.md and README.md

### Phase 4: Documentation Consistency
- [x] Standardized README.md format across MemberSim, RxMemberSim, PatientSim
- [x] Added consistent sections: Overview, Features, Installation, Quick Start, Architecture, Integration, Testing, Related
- [x] Added missing profile templates (9 files)
- [x] Added missing journey templates (4 files)

---

## Test Summary

| Package | Tests | Status |
|---------|-------|--------|
| Core | 902 | ✅ Passing |
| MemberSim | 183 | ✅ Passing |
| RxMemberSim | 213 | ✅ Passing |
| PatientSim | 446 | ✅ Passing |
| TrialSim | 16 | ✅ Passing |
| **Total** | **1,760** | ✅ All Passing |

---

## Outstanding Items (Lower Priority)

### Database Index Names
- [ ] Update index names from `idx_*_scenario` to `idx_*_cohort` in migrations.py
- Note: This is cosmetic and doesn't affect functionality

### MCP Server Consistency
- [ ] Audit MemberSim MCP tools for terminology consistency
- [ ] Audit RxMemberSim MCP tools for terminology consistency
- [ ] Consider adding MCP server to TrialSim

---

## Product Structure Reference

All products now follow this canonical structure:

```
packages/{product}/
├── CLAUDE.md           # AI development guide
├── README.md           # Product documentation
├── pyproject.toml      # Package configuration
├── src/{product}/      # Source code (single canonical location)
│   ├── __init__.py
│   ├── core/           # Core models and generators
│   ├── dimensional/    # Star schema transforms
│   ├── formats/        # Export formats
│   ├── journeys/       # Journey templates and handlers
│   ├── mcp/            # MCP server integration
│   └── validation/     # Validation logic
└── tests/              # Test suite
    ├── conftest.py
    └── test_*.py
```

---

## Commits

1. `53417fd` - refactor(patientsim): rename scenario terminology to skill/cohort in MCP layer
2. `5ba716a` - feat: implement TrialSim package and standardize product structure
3. `cfeedac` - docs: add profile and journey templates, consistency plan
