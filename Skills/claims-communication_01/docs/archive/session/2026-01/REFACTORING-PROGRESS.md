# Terminology & Cleanup Refactoring Progress

## Status: IN PROGRESS
**Started:** 2026-01-05

---

## Quick Wins

### 1. Remove Duplicate Folder
- [ ] Delete `packages/patientsim/src/skills/` (duplicate of `packages/patientsim/src/patientsim/skills/`)
- [ ] Verify no imports reference the deleted path
- [ ] Run tests

### 2. Create Missing README
- [ ] Create `skills/common/README.md`

---

## Terminology Refactoring

### 3. PatientSim MCP Tools (Low Risk)
- [ ] Rename `list_scenarios` → `list_templates` in generation_server.py
- [ ] Rename `describe_scenario` → `describe_template` in generation_server.py
- [ ] Update `format_scenario_list` → `format_template_list` in formatters.py
- [ ] Update `format_scenario_details` → `format_template_details` in formatters.py
- [ ] Update SkillType.SCENARIO_TEMPLATE → CLINICAL_TEMPLATE in schema.py
- [ ] Run PatientSim tests

### 4. MemberSim Scenarios → Journeys (Medium Risk)
- [ ] Rename folder: `scenarios/` → `journeys/`
- [ ] Rename classes: Scenario* → Journey*
- [ ] Update all imports in membersim
- [ ] Update tests
- [ ] Run MemberSim tests

### 5. RxMemberSim Scenarios → Journeys (Medium Risk)
- [ ] Rename folder: `scenarios/` → `journeys/`
- [ ] Rename classes: Scenario* → Journey*
- [ ] Update all imports in rxmembersim
- [ ] Update tests
- [ ] Run RxMemberSim tests

---

## Documentation Fixes

### 6. Fix Broken Links (Non-Archive)
- [ ] Count non-archive broken links
- [ ] Fix or remove template references
- [ ] Fix cross-product references
- [ ] Re-run link validator

### 7. Update Documentation Terminology
- [ ] Update SKILL.md headers
- [ ] Update hello-healthsim docs
- [ ] Update skill files as needed

---

## Verification

- [ ] Full test suite passes
- [ ] Link validator shows minimal issues
- [ ] `grep -r "scenario" packages/` shows only valid clinical scenario uses
- [ ] Commit and push

---

## Progress Log

| Time | Action | Result |
|------|--------|--------|
| | | |
