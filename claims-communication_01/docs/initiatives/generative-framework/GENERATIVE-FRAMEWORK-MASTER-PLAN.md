# HealthSim Generative Framework - Master Implementation Plan

**Version:** 1.0  
**Created:** January 3, 2026  
**Status:** READY FOR IMPLEMENTATION

---

## Executive Summary

This plan implements the Generative Framework for HealthSim - a two-phase architecture separating **Specification Building** (creative, conversational) from **Execution** (mechanical, deterministic). The framework enables data-driven generation of synthetic healthcare populations and their journeys over time.

### Key Principles

1. **Skills-First**: All knowledge in Skills, not Python code
2. **Conversation-Driven**: Configuration via natural language
3. **Consistent Architecture**: Uniform patterns across all products
4. **Test-Driven**: Automated validation at every stage
5. **Documentation Excellence**: Every file documented, linked, navigable

### Deliverables Overview

| Phase | Focus | Skills | Tests | Docs |
|-------|-------|--------|-------|------|
| 0 | Foundation & Cleanup | 0 | Audit | Links |
| 1 | Profile Builder | 8 | 20+ | 4 |
| 2 | Journey Builder | 10 | 25+ | 4 |
| 3 | Executors | 6 | 30+ | 4 |
| 4 | Integration & Polish | 4 | 50+ | 6 |
| **Total** | | **28** | **125+** | **18** |

**Timeline:** 4-6 weeks (8-12 focused sessions)

---

## Architecture Standards

### Directory Structure (ENFORCED)

```
healthsim-workspace/
├── SKILL.md                          # Master router (update with generation section)
├── README.md                         # Main README (update with generation overview)
│
├── skills/
│   ├── common/                       # Shared skills
│   │   ├── state-management.md       # (existing)
│   │   ├── duckdb-skill.md           # (existing)
│   │   └── cross-product.md          # NEW: Cross-product correlation patterns
│   │
│   ├── generation/                   # NEW: Generative Framework skills
│   │   ├── README.md                 # Category overview
│   │   ├── SKILL.md                  # Generation master router
│   │   │
│   │   ├── builders/                 # Phase 1: Specification Building
│   │   │   ├── README.md
│   │   │   ├── profile-builder.md    # 4-phase conversation flow
│   │   │   ├── journey-builder.md    # Journey specification
│   │   │   └── quick-generate.md     # Single-entity fast path
│   │   │
│   │   ├── executors/                # Phase 2: Execution
│   │   │   ├── README.md
│   │   │   ├── profile-executor.md   # Execute profile specifications
│   │   │   ├── journey-executor.md   # Execute journey timelines
│   │   │   └── cross-domain-sync.md  # Cross-product event triggers
│   │   │
│   │   ├── distributions/            # Statistical tools
│   │   │   ├── README.md
│   │   │   ├── distribution-types.md # Categorical, Normal, LogNormal, Explicit
│   │   │   ├── age-distributions.md  # Age distribution patterns
│   │   │   └── cost-distributions.md # Cost/utilization distributions
│   │   │
│   │   ├── journeys/                 # Journey patterns
│   │   │   ├── README.md
│   │   │   ├── linear-journey.md     # Sequential events
│   │   │   ├── branching-journey.md  # Decision-based paths
│   │   │   ├── protocol-journey.md   # Trial protocol visits
│   │   │   └── lifecycle-journey.md  # Multi-year patient journeys
│   │   │
│   │   └── templates/                # Pre-built specifications
│   │       ├── README.md
│   │       ├── profiles/
│   │       │   ├── medicare-diabetic.md
│   │       │   ├── commercial-healthy.md
│   │       │   └── medicaid-pediatric.md
│   │       └── journeys/
│   │           ├── diabetic-first-year.md
│   │           ├── surgical-episode.md
│   │           └── new-member-onboarding.md
│   │
│   ├── patientsim/                   # (existing - no structural changes)
│   ├── membersim/                    # (existing - no structural changes)
│   ├── rxmembersim/                  # (existing - no structural changes)
│   ├── trialsim/                     # (existing - no structural changes)
│   ├── populationsim/                # (existing - add integration refs)
│   └── networksim/                   # (existing - add integration refs)
│
├── schemas/                          # NEW: JSON Schemas (supplementary)
│   ├── README.md
│   ├── profile-spec-v1.json
│   ├── journey-spec-v1.json
│   └── distribution-types.json
│
├── docs/
│   ├── initiatives/
│   │   └── generative-framework/     # NEW: Initiative documentation
│   │       ├── GENERATIVE-FRAMEWORK-MASTER-PLAN.md  # This file
│   │       ├── ARCHITECTURE.md       # Conceptual model document
│   │       ├── DECISIONS.md          # Design decisions
│   │       └── sessions/             # Session logs
│   │           ├── SESSION-01.md
│   │           └── ...
│   │
│   └── architecture/                 # (update existing)
│       └── generative-framework.md   # Architecture reference
│
├── hello-healthsim/
│   └── examples/
│       ├── generation-examples.md    # NEW: Generation examples
│       └── (existing files)
│
└── packages/
    └── mcp-server/                   # (enhance for execution)
        └── healthsim_mcp.py          # Add generation execution tools
```

### Skill File Standards (MANDATORY)

Every skill file MUST have:

```markdown
---
name: skill-name
description: "Brief description with trigger phrases in quotes"
version: "1.0"
status: active
product: generation  # or patientsim, membersim, etc.
category: builders   # or executors, distributions, journeys, templates
---

# Skill Title

## Overview
Brief description (2-3 sentences)

## Trigger Phrases
- "phrase one"
- "phrase two"

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| param1    | string | Yes | - | What it does |

## Generation Patterns
(Domain-specific content)

## Examples

### Example 1: [Descriptive Title]
**Request:** "User request in quotes"
**Output:**
```json
{
  "complete": "example"
}
```

### Example 2: [Descriptive Title]
(At least 2 examples required)

## Validation Rules

| Rule | Description | Example |
|------|-------------|---------|
| RULE-001 | Rule description | Valid: x, Invalid: y |

## Related Skills
- [skill-name](path/to/skill.md) - Brief description
- [skill-name](path/to/skill.md) - Brief description

## For Claude
(Hidden section with Claude-specific guidance)
```

### README Standards (MANDATORY)

Every directory with skills MUST have a README.md:

```markdown
# [Category Name]

## Overview
Brief description of this category.

## Skills in This Category

| Skill | Purpose | When to Use |
|-------|---------|-------------|
| [skill.md](skill.md) | Description | Trigger conditions |

## Quick Start
1. Step one
2. Step two

## Related Categories
- [Category](../category/) - Brief description
```

---

## Phase 0: Foundation & Cleanup (Session 1)

### Objective
Establish a clean foundation with consistent structure and working links.

### Pre-Flight Checklist
- [ ] Read CURRENT-WORK.md
- [ ] Pull latest from GitHub
- [ ] Run full test suite (baseline)
- [ ] Review existing README link structure

### Deliverables

#### 0.1 Link Audit & Repair

**Scope:**
1. Scan all markdown files for broken links
2. Fix or remove broken links
3. Add missing cross-references
4. Verify all README files exist

**Script:** Create `scripts/audit_links.py`

```python
# Audit all markdown links in the workspace
# Output: report of broken links with suggested fixes
```

#### 0.2 Create Initiative Directory Structure

```bash
mkdir -p docs/initiatives/generative-framework/sessions
mkdir -p skills/generation/{builders,executors,distributions,journeys,templates/profiles,templates/journeys}
mkdir -p schemas
```

#### 0.3 Move Design Documents

Move existing design documents to initiative folder:
- `HEALTHSIM-GENERATIVE-FRAMEWORK-CONCEPTS.md` → `docs/initiatives/generative-framework/CONCEPTS.md`
- `HEALTHSIM-GENERATIVE-FRAMEWORK-DECISIONS.md` → `docs/initiatives/generative-framework/DECISIONS.md`
- `HEALTHSIM-PROFILE-BUILDER-SPECIFICATION.md` → `docs/initiatives/generative-framework/PROFILE-BUILDER-SPEC.md`
- `HEALTHSIM-GENERATIVE-TAXONOMY.md` → `docs/initiatives/generative-framework/TAXONOMY.md`
- `healthsim-conceptual-model.html` → `docs/initiatives/generative-framework/ARCHITECTURE.html`

#### 0.4 Baseline Tests

Run and document baseline test status:

```bash
# From workspace root
cd packages/core && pytest -v --tb=short > ../../test-results/core-baseline.txt
cd ../mcp-server && pytest -v --tb=short > ../../test-results/mcp-baseline.txt
```

### Post-Flight Checklist
- [ ] All links verified working
- [ ] Directory structure created
- [ ] Design docs moved and renamed
- [ ] Baseline test results documented
- [ ] Git commit: `[Generation] Phase 0: Foundation and cleanup`
- [ ] Git push

### Success Criteria
- Zero broken links in repository
- All README files present in skill directories
- Clean baseline test results documented

---

## Phase 1: Profile Builder (Sessions 2-3)

### Objective
Implement the Profile Builder - the conversational specification tool for defining population characteristics.

### Pre-Flight Checklist
- [ ] Phase 0 complete and verified
- [ ] Read CONCEPTS.md and PROFILE-BUILDER-SPEC.md
- [ ] Understand 4-phase conversation flow

### Deliverables

#### 1.1 Core Builder Skills (Session 2)

**File:** `skills/generation/builders/README.md`
- Category overview
- Builder workflow diagram
- Links to all builder skills

**File:** `skills/generation/builders/profile-builder.md`
- 4-phase conversation flow:
  1. Intent Recognition
  2. Profile Selection/Customization
  3. Refinement Loop
  4. Specification Confirmation
- Scope handling (entity, cohort, population)
- Domain detection (clinical, payer, pharmacy, trial)
- PopulationSim integration for real demographics
- Complete JSON specification output

**File:** `skills/generation/builders/quick-generate.md`
- Fast path for simple requests
- Single entity generation without full builder flow
- When to route to full builder

#### 1.2 Distribution Skills (Session 2)

**File:** `skills/generation/distributions/README.md`
- Overview of statistical distribution types
- When to use each type

**File:** `skills/generation/distributions/distribution-types.md`
- Categorical distributions (weighted selection)
- Normal/Gaussian distributions (continuous values)
- Log-normal distributions (cost, utilization)
- Explicit value lists
- JSON schema for each type

**File:** `skills/generation/distributions/age-distributions.md`
- Pre-built age distributions by population type
- Medicare, Commercial, Medicaid, Pediatric patterns

**File:** `skills/generation/distributions/cost-distributions.md`
- Utilization and cost distribution patterns
- By product and cohort type

#### 1.3 Profile Templates (Session 3)

**File:** `skills/generation/templates/README.md`
- How templates work
- When to use vs. custom profiles

**File:** `skills/generation/templates/profiles/README.md`
- Profile template index

**File:** `skills/generation/templates/profiles/medicare-diabetic.md`
- Complete Medicare diabetic profile
- Demographics, clinical, coverage attributes
- Pre-configured for common use case

**File:** `skills/generation/templates/profiles/commercial-healthy.md`
- Commercial employer population
- Low-risk, healthy demographics

**File:** `skills/generation/templates/profiles/medicaid-pediatric.md`
- Medicaid pediatric population
- Age-appropriate conditions and patterns

### Testing (Session 3)

**Manual Smoke Tests:**
1. "Generate 100 Medicare diabetics" → Profile Builder activates
2. "Quick, give me a diabetic patient" → Quick Generate activates
3. "Use the medicare-diabetic template" → Template loads

**Automated Tests:**
Create `tests/test_profile_builder.py`:
- Test profile JSON schema validation
- Test distribution calculations
- Test template loading

### Documentation

**File:** `hello-healthsim/examples/generation-examples.md`
- Section 1: Profile Building Examples
- 4+ complete examples with outputs

### Post-Flight Checklist
- [ ] All 8 skill files created with full content
- [ ] README files in all directories
- [ ] Manual smoke tests pass
- [ ] Automated tests pass
- [ ] Examples documented
- [ ] Links verified
- [ ] Git commit: `[Generation] Phase 1: Profile Builder complete`
- [ ] Git push

### Success Criteria
- Profile Builder conversation flow works end-to-end
- Distribution types generate statistically correct values
- Templates load and customize correctly
- All documentation complete and linked

---

## Phase 2: Journey Builder (Sessions 4-5)

### Objective
Implement the Journey Builder - the specification tool for defining event sequences over time.

### Pre-Flight Checklist
- [ ] Phase 1 complete and verified
- [ ] Read CONCEPTS.md journey section
- [ ] Understand journey complexity levels

### Deliverables

#### 2.1 Journey Skills (Session 4)

**File:** `skills/generation/builders/journey-builder.md`
- Journey specification creation
- Timeline definition (days, weeks, months, years)
- Event types by product
- Branching logic definition
- Cross-domain trigger configuration

**File:** `skills/generation/journeys/README.md`
- Journey pattern overview
- Complexity levels
- Pattern selection guide

**File:** `skills/generation/journeys/linear-journey.md`
- Sequential event pattern
- Fixed timeline with variations
- Example: Annual wellness visits

**File:** `skills/generation/journeys/branching-journey.md`
- Decision-based event paths
- Probability-driven branching
- Example: Diabetes complication cascade

**File:** `skills/generation/journeys/protocol-journey.md`
- Clinical trial protocol visits
- Required vs. optional windows
- Deviation handling

**File:** `skills/generation/journeys/lifecycle-journey.md`
- Multi-year patient journeys
- Condition progression
- Life event triggers

#### 2.2 Journey Templates (Session 5)

**File:** `skills/generation/templates/journeys/README.md`
- Journey template index

**File:** `skills/generation/templates/journeys/diabetic-first-year.md`
- Complete first year diabetes journey
- PCP visits, A1C labs, medication fills
- Specialist referrals, complications

**File:** `skills/generation/templates/journeys/surgical-episode.md`
- Pre-op, surgery, recovery journey
- Claims timing patterns

**File:** `skills/generation/templates/journeys/new-member-onboarding.md`
- New member enrollment journey
- Initial visits, plan setup

### Testing (Session 5)

**Manual Smoke Tests:**
1. "Add a journey to this profile" → Journey Builder activates
2. "Use the diabetic-first-year journey" → Template loads
3. "Create a branching journey for HF patients" → Branching pattern

**Automated Tests:**
Create `tests/test_journey_builder.py`:
- Test journey JSON schema validation
- Test timeline calculations
- Test branching probability validation

### Documentation

Update `hello-healthsim/examples/generation-examples.md`:
- Section 2: Journey Building Examples
- 4+ complete examples with outputs

### Post-Flight Checklist
- [ ] All 10 journey-related skill files created
- [ ] README files in all directories
- [ ] Manual smoke tests pass
- [ ] Automated tests pass
- [ ] Examples documented
- [ ] Links verified
- [ ] Git commit: `[Generation] Phase 2: Journey Builder complete`
- [ ] Git push

### Success Criteria
- Journey Builder creates valid specifications
- All journey patterns generate correct event sequences
- Timing calculations are accurate
- Templates customize correctly

---

## Phase 3: Executors (Sessions 6-7)

### Objective
Implement the execution layer that transforms specifications into actual entities.

### Pre-Flight Checklist
- [ ] Phase 2 complete and verified
- [ ] Review MCP server current tools
- [ ] Understand entity generation patterns

### Deliverables

#### 3.1 Executor Skills (Session 6)

**File:** `skills/generation/executors/README.md`
- Executor architecture overview
- Specification → Entity flow
- MCP tool mapping

**File:** `skills/generation/executors/profile-executor.md`
- Execute profile specifications
- Entity count handling (batching for >50)
- Distribution sampling
- PopulationSim data lookup
- NetworkSim provider lookup
- Output to canonical format

**File:** `skills/generation/executors/journey-executor.md`
- Execute journey timelines
- Event generation by product
- Timing calculations
- Cross-domain trigger firing

**File:** `skills/generation/executors/cross-domain-sync.md`
- Cross-product event triggers
- Encounter → Claim mapping
- Prescription → Fill mapping
- Identity correlation maintenance

#### 3.2 MCP Server Enhancements (Session 7)

**File:** `packages/mcp-server/healthsim_mcp.py`
Enhance with new tools:

```python
# New tools for generation execution
healthsim_execute_profile   # Execute a profile specification
healthsim_execute_journey   # Execute a journey specification
healthsim_preview_entities  # Preview generation without saving
```

**Tests:** `packages/mcp-server/tests/test_generation_execution.py`
- Test profile execution
- Test journey execution
- Test cross-domain triggers
- Test batching behavior

### Testing (Session 7)

**Manual Smoke Tests:**
1. Complete flow: Profile → Execute → Save
2. Journey execution with cross-domain events
3. Large batch handling (100+ entities)

**Automated Tests:**
- Executor skill validation
- MCP tool response schemas
- Entity count verification

### Documentation

Update `hello-healthsim/examples/generation-examples.md`:
- Section 3: Execution Examples
- Complete end-to-end workflows

### Post-Flight Checklist
- [ ] All 4 executor skill files created
- [ ] MCP server tools implemented
- [ ] MCP tests pass
- [ ] Manual end-to-end tests pass
- [ ] Examples documented
- [ ] Git commit: `[Generation] Phase 3: Executors complete`
- [ ] Git push

### Success Criteria
- Specifications execute to correct entity counts
- Cross-domain triggers fire correctly
- Batching works for large generations
- MCP tools return proper responses

---

## Phase 4: Integration & Polish (Sessions 8-10)

### Objective
Complete integration, comprehensive testing, documentation excellence.

### Pre-Flight Checklist
- [ ] Phases 1-3 complete and verified
- [ ] Full test suite passing
- [ ] Review all documentation for consistency

### Deliverables

#### 4.1 Master SKILL.md Updates (Session 8)

**File:** `SKILL.md`
Add new section:

```markdown
## Generation Framework

### Profile Building
| Skill | Purpose | When to Use |
|-------|---------|-------------|
| [profile-builder](../../../skills/generation/builders/profile-builder.md) | Build population profiles | "Generate N members...", "Create a cohort..." |
| [quick-generate](../../../skills/generation/builders/quick-generate.md) | Single entity fast path | "Give me a patient...", "Quick, generate..." |

### Journey Building
| Skill | Purpose | When to Use |
|-------|---------|-------------|
| [journey-builder](../../../skills/generation/builders/journey-builder.md) | Define event sequences | "Add a journey...", "With monthly visits..." |

### Execution
| Skill | Purpose | When to Use |
|-------|---------|-------------|
| [profile-executor](../../../skills/generation/executors/profile-executor.md) | Execute specifications | After profile approval |
| [journey-executor](../../../skills/generation/executors/journey-executor.md) | Execute journeys | After journey approval |
```

**File:** `skills/generation/SKILL.md`
- Master router for generation category
- Quick reference table
- Usage patterns
- Integration with other products

#### 4.2 README Updates (Session 8)

**File:** `README.md`
Add Generation Framework section:
- Overview of profile/journey building
- Link to examples
- Integration diagram

**File:** `skills/generation/README.md`
- Complete category overview
- Workflow diagram
- All skill links

#### 4.3 Cross-Product Integration (Session 9)

**File:** `skills/common/cross-product.md`
- Identity correlation patterns
- Event synchronization rules
- Product-specific entity mapping

Update all product SKILL.md files:
- PatientSim: Add generation integration section
- MemberSim: Add generation integration section
- RxMemberSim: Add generation integration section
- TrialSim: Add generation integration section
- PopulationSim: Add generation integration section
- NetworkSim: Add generation integration section

#### 4.4 JSON Schemas (Session 9)

**File:** `schemas/README.md`
- Schema usage guide
- When schemas are needed vs. Skills

**File:** `schemas/profile-spec-v1.json`
- Complete profile specification schema

**File:** `schemas/journey-spec-v1.json`
- Complete journey specification schema

**File:** `schemas/distribution-types.json`
- All distribution type schemas

#### 4.5 Comprehensive Testing (Session 10)

**Create:** `tests/test_generation_integration.py`
- End-to-end generation tests
- Cross-product event tests
- Large scale generation tests (500+ entities)

**Create:** `scripts/smoke_test_generation.py`
- Quick validation script for CI/CD
- Tests core generation paths

**Run:** Full test suite
```bash
pytest packages/core/tests -v
pytest packages/mcp-server/tests -v
python scripts/smoke_test_generation.py
```

#### 4.6 Documentation Excellence (Session 10)

**Complete:**
- All hello-healthsim examples
- All skill cross-references
- All README files
- CHANGELOG.md update

**Create:** `docs/initiatives/generative-framework/IMPLEMENTATION-SUMMARY.md`
- What was built
- Key decisions made
- Future enhancements

### Post-Flight Checklist
- [ ] SKILL.md updated with generation section
- [ ] README.md updated
- [ ] All product SKILL.md files updated
- [ ] JSON schemas created
- [ ] Full test suite passes (1700+ tests)
- [ ] Smoke test script works
- [ ] All documentation complete
- [ ] All links verified
- [ ] CHANGELOG.md updated
- [ ] Git commit: `[Generation] Phase 4: Integration and polish complete`
- [ ] Git tag: `v2.0.0-generation`
- [ ] Git push with tags

### Success Criteria
- All generation features work end-to-end
- Documentation is complete and navigable
- Test coverage is comprehensive
- No broken links
- Clean test results

---

## Testing Strategy

### Automated Tests

| Test File | Tests | Coverage |
|-----------|-------|----------|
| `test_profile_builder.py` | ~20 | Profile schema, distributions |
| `test_journey_builder.py` | ~25 | Journey schema, timeline |
| `test_generation_execution.py` | ~30 | Execution, batching, triggers |
| `test_generation_integration.py` | ~50 | End-to-end, cross-product |

### Smoke Tests

Quick validation after each session:

```bash
# Run after every session
python scripts/smoke_test_generation.py

# Should output:
# ✅ Profile Builder: OK
# ✅ Journey Builder: OK
# ✅ Profile Executor: OK
# ✅ Journey Executor: OK
# ✅ Cross-Domain Sync: OK
# ✅ All 5 smoke tests passed
```

### Manual Validation

After each phase, manually test:
1. Natural language prompt → correct skill activation
2. Specification output → valid JSON
3. Execution → correct entity counts
4. Cross-product → events correlate properly

---

## Documentation Checklist

### Skill Files (28 total)

| Directory | Files | Status |
|-----------|-------|--------|
| builders/ | 3 + README | ⬜ |
| executors/ | 3 + README | ⬜ |
| distributions/ | 3 + README | ⬜ |
| journeys/ | 4 + README | ⬜ |
| templates/profiles/ | 3 + README | ⬜ |
| templates/journeys/ | 3 + README | ⬜ |
| generation/ (root) | 1 + README | ⬜ |

### README Files (12 total)

| Directory | Status |
|-----------|--------|
| skills/generation/ | ⬜ |
| skills/generation/builders/ | ⬜ |
| skills/generation/executors/ | ⬜ |
| skills/generation/distributions/ | ⬜ |
| skills/generation/journeys/ | ⬜ |
| skills/generation/templates/ | ⬜ |
| skills/generation/templates/profiles/ | ⬜ |
| skills/generation/templates/journeys/ | ⬜ |
| schemas/ | ⬜ |
| docs/initiatives/generative-framework/ | ⬜ |

### Updates to Existing Files (10 total)

| File | Update | Status |
|------|--------|--------|
| SKILL.md | Add generation section | ⬜ |
| README.md | Add generation overview | ⬜ |
| skills/patientsim/SKILL.md | Add integration | ⬜ |
| skills/membersim/SKILL.md | Add integration | ⬜ |
| skills/rxmembersim/SKILL.md | Add integration | ⬜ |
| skills/trialsim/SKILL.md | Add integration | ⬜ |
| skills/populationsim/SKILL.md | Add integration | ⬜ |
| skills/networksim/SKILL.md | Add integration | ⬜ |
| CHANGELOG.md | Add generation entries | ⬜ |
| hello-healthsim/examples/ | Add generation-examples.md | ⬜ |

---

## Git Workflow

### Commit Message Format

```
[Generation] Phase N: Brief description

- Bullet point of what was done
- Another item
- Test results: X passing
```

### Branch Strategy

Work on `main` branch with frequent commits:

```bash
# After each session
git add -A
git status  # Review changes
git commit -m "[Generation] Phase N: Session description"
git push origin main
```

### Tags

| Tag | When | Description |
|-----|------|-------------|
| `v2.0.0-gen-phase1` | After Phase 1 | Profile Builder complete |
| `v2.0.0-gen-phase2` | After Phase 2 | Journey Builder complete |
| `v2.0.0-gen-phase3` | After Phase 3 | Executors complete |
| `v2.0.0` | After Phase 4 | Full release |

---

## Risk Mitigation

### Risk 1: Scope Creep
**Mitigation:** Strict adherence to deliverables list. New ideas go to FUTURE-ENHANCEMENTS.md.

### Risk 2: Breaking Existing Functionality
**Mitigation:** Run full test suite after every session. No PR without all tests passing.

### Risk 3: Documentation Drift
**Mitigation:** Update docs in same session as code changes. Link verification before commit.

### Risk 4: Inconsistent Patterns
**Mitigation:** Use skill template for all files. Code review checklist before commit.

---

## Session Execution Template

Each session follows this template:

### Pre-Flight (5 minutes)
1. Pull latest from GitHub
2. Run test suite (verify baseline)
3. Read relevant design docs
4. Review session deliverables

### Implementation (Main work)
1. Create directory structure if needed
2. Create/update skill files
3. Create/update README files
4. Write tests
5. Run tests
6. Fix issues
7. Update CHANGELOG.md

### Post-Flight (10 minutes)
1. Run full test suite
2. Run smoke tests
3. Verify all links
4. Git add, commit, push
5. Update CURRENT-WORK.md
6. Log session in sessions/ folder

---

## Appendix: File Templates

### Skill File Template

See Architecture Standards section above.

### README Template

```markdown
# [Category Name]

## Overview
[1-2 sentence description]

## Skills in This Category

| Skill | Purpose | When to Use |
|-------|---------|-------------|
| [name.md](name.md) | Description | Trigger phrases |

## Quick Start

```
Example prompt
```

## Directory Structure
```
category/
├── README.md
├── skill1.md
└── skill2.md
```

## Related Categories
- [Other](../other/) - Brief description
```

### Test File Template

```python
"""Tests for [component name]."""

import pytest
from healthsim.generation import ...

class TestComponentName:
    """Test suite for ComponentName."""
    
    def test_basic_functionality(self):
        """Test basic operation."""
        result = component.do_something()
        assert result is not None
        
    def test_edge_case(self):
        """Test edge case handling."""
        with pytest.raises(ValueError):
            component.do_something_invalid()
```

---

## Sign-Off

**Plan Author:** Claude (Claude Opus 4.5)  
**Plan Version:** 1.0  
**Created:** January 3, 2026  
**Status:** Ready for Implementation

---

*This plan enforces architectural consistency, comprehensive testing, and documentation excellence across the HealthSim Generative Framework implementation.*
