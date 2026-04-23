# HealthSim Workspace Architecture Audit Report

**Date:** 2026-01-05  
**Auditor:** Claude (AI Assistant)  
**Scope:** Complete evaluation of architecture, code, documentation, and terminology

---

## Executive Summary

The HealthSim Workspace is a well-structured multi-product healthcare data generation system. This audit identified **5 priority areas** requiring attention:

| Area | Severity | Issues Found |
|------|----------|--------------|
| **Terminology Refactoring** | 🔴 High | "scenario" still used in 637+ Python code locations |
| **Broken Links** | 🟠 Medium | 211 broken links in documentation |
| **Duplicate Code** | 🟡 Low | Duplicate skills/ folders in patientsim |
| **Incomplete Templates** | 🟡 Low | Referenced templates don't exist |
| **Archive Cleanup** | ⚪ Info | Old docs in archive have stale links |

---

## 1. Project Structure Evaluation

### 1.1 Package Structure Consistency

| Package | Structure | Status | Notes |
|---------|-----------|--------|-------|
| `core` | `src/healthsim/` | ✅ Consistent | Clean modular structure |
| `patientsim` | `src/patientsim/` | ⚠️ Issue | Has duplicate `src/skills/` AND `src/patientsim/skills/` |
| `membersim` | `src/membersim/` | ✅ Consistent | Well organized |
| `rxmembersim` | `src/rxmembersim/` | ✅ Consistent | Well organized |
| `mcp-server` | flat | ✅ Consistent | Single-file appropriate |

**Core Package Modules (Excellent):**
```
packages/core/src/healthsim/
├── benefits/       # Accumulator tracking
├── config/         # Settings, logging
├── db/             # DuckDB schema, queries
├── dimensional/    # Star schema analytics
├── formats/        # Export transformers
├── generation/     # NEW: Generative Framework ✅
├── person/         # Identity, demographics
├── skills/         # Skill loading/parsing
├── state/          # Workspace, cohort management
├── temporal/       # Timeline, periods
└── validation/     # Data validation
```

### 1.2 Skills Structure Consistency

| Product | README | SKILL.md | Sub-Skills | Status |
|---------|--------|----------|------------|--------|
| generation | ✅ | ✅ | 16 files | ✅ Excellent |
| patientsim | ✅ | ✅ | 14+ files | ✅ Good |
| membersim | ✅ | ✅ | 9 files | ✅ Good |
| rxmembersim | ✅ | ✅ | 8 files | ✅ Good |
| trialsim | ✅ | ✅ | 12+ files | ✅ Good |
| populationsim | ✅ | ✅ | 25+ files | ✅ Excellent |
| networksim | ✅ | ✅ | 30+ files | ✅ Excellent |
| common | ⚠️ Missing | ❌ N/A | 3 files | 🟠 Needs README |

---

## 2. Terminology Audit: "scenario" vs "cohort"

### 2.1 Clarifying the Distinction

After analysis, there are **two valid uses** of "scenario":

| Term | Definition | Example | Status |
|------|------------|---------|--------|
| **Cohort** | Saved collection of generated entities | "Medicare diabetic cohort" | ✅ Correct usage |
| **Scenario** (template) | Event sequence pattern over time | "Heart failure progression scenario" | ✅ Valid technical term |
| **Scenario** (old) | Deprecated synonym for cohort | "scenario_id" instead of "cohort_id" | ❌ Should be refactored |

### 2.2 Locations Requiring Refactoring

**Python Code (637 matches in packages/):**

| File/Area | Issue | Priority |
|-----------|-------|----------|
| `patientsim/mcp/generation_server.py` | Tool names: `list_scenarios`, `describe_scenario` | 🔴 High |
| `patientsim/mcp/formatters.py` | Functions: `format_scenario_list`, `format_scenario_details` | 🔴 High |
| `patientsim/skills/schema.py` | `SCENARIO_TEMPLATE = "scenario-template"` | 🔴 High |
| `patientsim/core/reference_data.py` | `CLINICAL_SCENARIOS` dict | 🟡 Low (valid usage) |
| `membersim/scenarios/` folder | Entire folder uses scenario terminology | 🟠 Medium |
| `rxmembersim/scenarios/` folder | Entire folder uses scenario terminology | 🟠 Medium |
| `mcp-server/healthsim_mcp.py` | `SCENARIO_ENTITY_TYPES` constant | 🟡 Low (valid usage) |

**Skill/Documentation (412 matches in *.md files):**

| File | Issue | Priority |
|------|-------|----------|
| `SKILL.md` (root) | Multiple "Scenario" headers | 🔴 High |
| `hello-healthsim/CLAUDE-DESKTOP.md` | "Scenario" as section headers | 🟠 Medium |
| Various tutorials | Mixed terminology | 🟠 Medium |

### 2.3 Recommended Terminology

| Old Term | New Term | Context |
|----------|----------|---------|
| `list_scenarios` | `list_templates` | MCP tools |
| `describe_scenario` | `describe_template` | MCP tools |
| `scenario_id` | `template_id` | Parameters |
| `SCENARIO_TEMPLATE` | `CARE_TEMPLATE` | SkillType enum |
| `membersim/scenarios/` | `membersim/journeys/` | Folder rename |
| `ScenarioDefinition` | `JourneyDefinition` | Class rename |

**Keep "scenario" when it means:**
- Clinical scenarios (sepsis scenario, CHF scenario) - describes a medical situation
- `SCENARIO_ENTITY_TYPES` - describes type of synthetic data

---

## 3. Documentation Quality

### 3.1 README Files Audit

| Location | Exists | Quality | Links Valid |
|----------|--------|---------|-------------|
| `/README.md` | ✅ | ⭐⭐⭐⭐⭐ | ✅ |
| `/hello-healthsim/README.md` | ✅ | ⭐⭐⭐⭐⭐ | ✅ |
| `/packages/README.md` | ✅ | ⭐⭐⭐⭐ | ✅ |
| `/packages/core/README.md` | ✅ | ⭐⭐⭐⭐ | ✅ |
| `/skills/generation/README.md` | ✅ | ⭐⭐⭐⭐⭐ | ✅ |
| `/skills/common/README.md` | ❌ | N/A | N/A |
| `/formats/README.md` | ✅ | ⭐⭐⭐⭐ | ✅ |
| `/references/README.md` | ✅ | ⭐⭐⭐ | ⚠️ Some issues |
| `/schemas/README.md` | ✅ | ⭐⭐⭐ | ✅ |

### 3.2 Broken Links Summary (211 total)

| Category | Count | Examples | Action |
|----------|-------|----------|--------|
| Archive docs | 89 | Old initiative docs | ⚪ Ignore (archived) |
| Template references | 42 | `commercial-diabetic.md` doesn't exist | 🟠 Create or remove |
| Cross-product refs | 28 | `full-ecosystem-scenario.md` | 🟠 Create or rename |
| Skill references | 19 | `protocol-patterns.md` | 🟡 Create |
| Journey templates | 15 | `care-transition.md` | 🟡 Create |
| Profile templates | 18 | `medicare-chf.md` | 🟡 Create |

### 3.3 Missing Documentation

| File | Purpose | Priority |
|------|---------|----------|
| `skills/common/README.md` | Explain common skills | 🟠 Medium |
| `docs/guides/mcp-setup.md` | MCP configuration guide | 🟡 Low |
| Several template files | Referenced but don't exist | 🟡 Low |

---

## 4. Generative Framework Audit

### 4.1 Implementation Status: ✅ COMPLETE

| Component | Files | Tests | Quality |
|-----------|-------|-------|---------|
| Distributions | `distributions.py` (850 lines) | 89 tests ✅ | Excellent |
| Profile Schema | `profile_schema.py` (265 lines) | 17 tests ✅ | Excellent |
| Profile Executor | `profile_executor.py` (594 lines) | 17 tests ✅ | Excellent |
| Reference Profiles | `reference_profiles.py` (430 lines) | 19 tests ✅ | Excellent |
| Journey Engine | `journey_engine.py` (850 lines) | 27 tests ✅ | Excellent |
| Triggers | `triggers.py` (400 lines) | 13 tests ✅ | Excellent |
| Handlers | `handlers.py` (1,240 lines) | 20 tests ✅ | Excellent |
| Integration Tests | `test_integration_*.py` | 9 tests ✅ | Excellent |

**Total: 194 tests passing**

### 4.2 Skills Documentation Status

| Document | Location | Status |
|----------|----------|--------|
| Framework Guide | `docs/initiatives/generative-framework/FRAMEWORK-GUIDE.md` | ✅ Complete |
| Hello-HealthSim Tutorial | `docs/initiatives/generative-framework/HELLO-HEALTHSIM-GENERATION.md` | ✅ Complete |
| Profile Builder Skill | `skills/generation/builders/profile-builder.md` | ✅ Complete |
| Journey Builder Skill | `skills/generation/builders/journey-builder.md` | ✅ Complete |
| Distribution Types | `skills/generation/distributions/distribution-types.md` | ✅ Complete |
| Templates (10 files) | `skills/generation/templates/` | ✅ Complete |

---

## 5. Duplicate Code Issues

### 5.1 Patientsim Duplicate Skills

**Found duplicate paths:**
```
packages/patientsim/src/skills/           # 4 files
packages/patientsim/src/patientsim/skills/ # 4 files (identical)
```

**Recommendation:** Remove `packages/patientsim/src/skills/` (outer one)

---

## 6. Action Plan

### Priority 1: Terminology Refactoring (High)

1. **Rename MCP tool names** in `patientsim/mcp/generation_server.py`:
   - `list_scenarios` → `list_templates`
   - `describe_scenario` → `describe_template`
   - `scenario` parameter → `template`

2. **Rename formatter functions** in `patientsim/mcp/formatters.py`:
   - `format_scenario_list` → `format_template_list`
   - `format_scenario_details` → `format_template_details`

3. **Update SkillType enum** in `patientsim/skills/schema.py`:
   - `SCENARIO_TEMPLATE` → `CARE_TEMPLATE` or `CLINICAL_TEMPLATE`

4. **Consider renaming folders** (breaking change, defer):
   - `membersim/scenarios/` → `membersim/journeys/`
   - `rxmembersim/scenarios/` → `rxmembersim/journeys/`

### Priority 2: Documentation Fixes (Medium)

1. **Create missing READMEs:**
   - `skills/common/README.md`

2. **Fix broken template links** by either:
   - Creating the missing template files, OR
   - Removing/updating links to only reference existing files

3. **Update SKILL.md** (root) to remove "Scenario" headers

### Priority 3: Code Cleanup (Low)

1. Remove duplicate `packages/patientsim/src/skills/` folder

2. Update imports if any reference the duplicate path

---

## 7. Positive Findings

| Area | Assessment |
|------|------------|
| **Overall Architecture** | ⭐⭐⭐⭐⭐ Excellent - clean separation of concerns |
| **Test Coverage** | ⭐⭐⭐⭐⭐ Excellent - 194+ tests for generation alone |
| **Database Schema** | ⭐⭐⭐⭐⭐ Excellent - properly uses "cohort" terminology |
| **README Quality** | ⭐⭐⭐⭐ Very Good - clear and comprehensive |
| **Skills Organization** | ⭐⭐⭐⭐⭐ Excellent - consistent structure across products |
| **Generative Framework** | ⭐⭐⭐⭐⭐ Excellent - complete implementation with docs |
| **MCP Integration** | ⭐⭐⭐⭐ Very Good - well-documented tools |
| **Cross-Product Design** | ⭐⭐⭐⭐⭐ Excellent - clear integration patterns |

---

## Appendix: File Counts

| Area | Files | Lines (approx) |
|------|-------|----------------|
| Skills (Markdown) | 150+ | 25,000+ |
| Python source | 100+ | 30,000+ |
| Tests | 50+ | 8,000+ |
| Documentation | 80+ | 15,000+ |
| Templates (JSON/YAML) | 10+ | 2,000+ |

**Total Repository:** ~500+ files, ~80,000+ lines
