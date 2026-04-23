# Generative Framework Implementation Plan

**Created**: 2026-01-06  
**Status**: Planning  
**Goal**: Bring designed components from "documented" to "fully implemented and integrated"

---

## Executive Summary

After auditing the codebase, the situation is **better than expected**. Many core components exist in working code, but they're not connected or exposed consistently across products.

### Actual Implementation Status

| Component | Lines of Code | Status | Gap |
|-----------|--------------|--------|-----|
| **Distributions** | 716 lines | ✅ Implemented | Need product wrappers |
| **Profile Schema** | 265 lines | ✅ Implemented | Need examples, tests |
| **Profile Executor** | 594 lines | ✅ Implemented | Need product integration |
| **Reference Profiles** | 648 lines | ✅ Implemented | Need DB initialization |
| **Journey Engine** | 1,195 lines | ✅ Implemented | Need journey→profile connection |
| **Cohort Generator** | 160 lines | ⚠️ Basic | Need product subclasses |
| **State Management** | ~1,500+ lines | ✅ Implemented | Need profile persistence |
| **Journey Templates** | ~500 lines/product | ✅ Implemented | Need Skill integration |

### The Real Problem

It's not that we haven't built anything - **we've built lots**. The problem is:

1. **No unified entry point** - Users can't easily "use" the framework
2. **Products don't expose core** - Each product has wrappers but they're inconsistent  
3. **Skills aren't integrated** - Journey templates hardcode values instead of deferring to Skills
4. **No end-to-end test** - We can't prove the full flow works

---

## Cross-Product Implementation Matrix

**CRITICAL**: Every feature must be implemented across ALL products. This matrix tracks completion.

### Phase 2: Product Integration Layer

| Feature | Core | MemberSim | PatientSim | RxMemberSim | TrialSim | PopulationSim | NetworkSim |
|---------|------|-----------|------------|-------------|----------|---------------|------------|
| `generation/` module | N/A | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| `profiles.py` | N/A | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| `executor.py` | N/A | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| `templates.py` | N/A | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| `generate()` function | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| Unit tests | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| Integration tests | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |

### Phase 3: Skill Integration

| Feature | Core | MemberSim | PatientSim | RxMemberSim | TrialSim |
|---------|------|-----------|------------|-------------|----------|
| SkillReference in journeys | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| Skill-aware event resolution | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| Migrated hardcoded values | N/A | ⬜ | ⬜ | ⬜ | ⬜ |

### Phase 5: State Management

| Feature | Core | MemberSim | PatientSim | RxMemberSim | TrialSim |
|---------|------|-----------|------------|-------------|----------|
| Profile persistence | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| Execution history | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |

### Documentation Checklist (Per Product)

| Documentation | Core | MemberSim | PatientSim | RxMemberSim | TrialSim | PopulationSim | NetworkSim |
|---------------|------|-----------|------------|-------------|----------|---------------|------------|
| README updated | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| API docs (`docs/api/`) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| Usage examples | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| Skill integration guide | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | N/A | N/A |
| Links verified | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |

---

## Documentation Requirements (Integrated per Phase)

Documentation is NOT deferred to the end. Each phase includes documentation deliverables.

### Phase 2 Documentation
- [ ] Update each product's README with generation module usage
- [ ] Create `docs/api/generation.md` with full API reference
- [ ] Add docstrings to all new classes/functions (Google style)
- [ ] Create quick-start example for each product
- [ ] Verify all existing links still work after changes

### Phase 3 Documentation
- [ ] Create `docs/guides/skill-integration.md` explaining the pattern
- [ ] Update affected Skills with integration examples
- [ ] Document SkillReference schema in API docs
- [ ] Add examples of skill-aware journey templates

### Phase 4 Documentation
- [ ] Create `docs/guides/reference-data.md` for PopulationSim/NetworkSim
- [ ] Document `healthsim init` command usage
- [ ] Add geography resolution examples

### Phase 5 Documentation
- [ ] Create `docs/guides/state-management.md` user guide
- [ ] Document profile persistence API
- [ ] Add execution history query examples

### Phase 6 Documentation (Final Polish)
- [ ] Create comprehensive `docs/guides/generative-framework.md`
- [ ] Review and update ALL product READMEs
- [ ] Run link validation across all docs
- [ ] Create "Oswald Family" demo script/walkthrough
- [ ] Update root README with framework overview

---

## Architecture: How It Should Work

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         USER CONVERSATION                                │
│  "Generate 100 diabetic Medicare patients in Harris County"             │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  PHASE 1: SPECIFICATION BUILDING (Claude + Skills)                       │
│                                                                          │
│  1. Claude reads relevant Skills (diabetes-management.md, etc.)         │
│  2. Claude resolves geography reference via ReferenceProfileResolver     │
│  3. Claude builds ProfileSpecification JSON                              │
│  4. User reviews and approves                                            │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  PHASE 2: EXECUTION (Deterministic)                                      │
│                                                                          │
│  1. ProfileExecutor generates base entities with distributions          │
│  2. JourneyEngine creates timelines for each entity                     │
│  3. Product handlers execute events                                      │
│  4. State manager persists cohort                                        │
│  5. Format transformers produce output files                             │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  OUTPUT                                                                  │
│  - Generated entities (persisted)                                        │
│  - Validation report                                                     │
│  - Formatted files (FHIR, HL7v2, X12, NCPDP, SDTM)                      │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Foundation Verification (Days 1-2)

### 1.1 Verify Core Infrastructure Works

**Goal**: Prove the existing code actually functions end-to-end.

**Tasks**:
- [ ] Create integration test: `tests/integration/test_generative_framework.py`
- [ ] Test ProfileExecutor with various specifications
- [ ] Test ReferenceProfileResolver with DuckDB
- [ ] Test JourneyEngine event scheduling
- [ ] Test state persistence round-trip

**Success Criteria**:
```python
# This should work
from healthsim.generation import ProfileExecutor, ProfileSpecification
from healthsim.generation import ReferenceProfileResolver
from healthsim.generation import JourneyEngine
from healthsim.state import persist, get_summary

spec = ProfileSpecification.model_validate({...})
executor = ProfileExecutor(spec)
result = executor.execute()
assert result.validation.passed
```

### 1.2 Document Existing APIs

**Goal**: Create accurate API documentation for what exists.

**Tasks**:
- [ ] Create `docs/api/generation.md` documenting actual functions
- [ ] Create `docs/api/state.md` documenting state management
- [ ] Update README files to point to actual APIs
- [ ] Add docstring examples to key classes

---

## Phase 2: Product Integration Layer (Days 3-5)

### 2.1 Create Consistent Product Wrappers

Each product needs a `generation/` module that wraps core infrastructure.

**Structure for each product**:
```
packages/{product}/src/{product}/
├── generation/
│   ├── __init__.py           # Re-exports
│   ├── profiles.py           # Product-specific profile extensions
│   ├── executor.py           # ProductProfileExecutor subclass
│   └── templates.py          # Pre-built profile templates
├── journeys/                  # Already exists
└── handlers/                  # Product handlers
```

**Tasks**:
- [ ] **MemberSim**: Create `generation/` module with member-specific profiles
- [ ] **PatientSim**: Create `generation/` module with patient-specific profiles
- [ ] **RxMemberSim**: Create `generation/` module with pharmacy-specific profiles
- [ ] **TrialSim**: Create `generation/` module with trial-specific profiles

**Example API**:
```python
# For each product
from membersim.generation import (
    MemberProfileExecutor,
    create_member_profile,
    MEMBER_PROFILE_TEMPLATES,
)

# Pre-built templates
spec = MEMBER_PROFILE_TEMPLATES["medicare-diabetic"]

# Execute
executor = MemberProfileExecutor(spec)
result = executor.execute()
members = result.entities
```

### 2.2 Connect Profiles to Journeys

**Goal**: ProfileExecutor output feeds into JourneyEngine.

**Tasks**:
- [ ] Add `journey` field to ProfileSpecification (exists, need implementation)
- [ ] Create `ProfileJourneyOrchestrator` class that coordinates both
- [ ] Wire journey selection based on entity attributes

**Example**:
```python
orchestrator = ProfileJourneyOrchestrator(profile_spec)
results = orchestrator.execute()  # Returns entities WITH timelines
```

### 2.3 Create Unified Entry Point (Addresses Gap 3)

**Goal**: Single, consistent API for users to generate healthcare data.

**Tasks**:
- [ ] Create `healthsim.generate()` convenience function in core
- [ ] Create product-specific `{product}.generate()` functions
- [ ] Wire to state persistence automatically
- [ ] Add format output options

**Unified API**:
```python
# Option 1: Core-level generation (multi-product)
from healthsim import generate

result = generate(
    profile="medicare-diabetic",      # Template name or ProfileSpec
    journey="diabetic-first-year",    # Optional journey
    count=100,
    products=["patientsim", "membersim"],
    output_formats=["fhir_r4", "x12_837"],
    persist=True,                     # Auto-save to state
    seed=42,                          # Reproducibility
)

# Option 2: Product-specific generation
from patientsim import generate as generate_patients

patients = generate_patients(
    profile="diabetic-senior",
    journey="chronic-management",
    count=50,
)
```

**Implementation Location**: `packages/core/src/healthsim/generate.py`

---

## Phase 3: Skill Integration (Days 6-8)

### 3.1 Define Skill Reference Pattern

**Problem**: Journey templates hardcode clinical values instead of deferring to Skills.

**Solution**: Create a "skill reference" mechanism.

**Tasks**:
- [ ] Define `SkillReference` schema in journey specifications
- [ ] Create skill-aware event parameter resolution
- [ ] Migrate hardcoded values to skill references

**Before** (current journey template):
```python
{
    "event_type": "DIAGNOSIS",
    "parameters": {
        "icd10": "E11.9",  # Hardcoded!
        "description": "Type 2 diabetes"
    }
}
```

**After** (skill-aware):
```python
{
    "event_type": "DIAGNOSIS",
    "parameters": {
        "skill_ref": "diabetes-management",
        "severity": "${entity.severity}",  # From profile
        # Claude uses skill to determine appropriate ICD-10
    }
}
```

### 3.2 Create Skill Loading Infrastructure

**Tasks**:
- [ ] Extend `healthsim.skills.loader` to support runtime loading
- [ ] Create skill metadata index for quick lookup
- [ ] Add skill version tracking

---

## Phase 4: PopulationSim/NetworkSim Integration (Days 9-10)

### 4.1 Reference Data Initialization

**Goal**: Ensure DuckDB has required reference data on first use.

**Tasks**:
- [ ] Create `healthsim init` command to set up reference data
- [ ] Verify CDC PLACES and SVI data loads correctly
- [ ] Add NetworkSim provider/facility reference data
- [ ] Create data validation checks

### 4.2 Reference Data in Profiles

**Tasks**:
- [ ] Test `create_hybrid_profile()` with real geography references
- [ ] Add provider distribution from NetworkSim
- [ ] Add facility assignment from NetworkSim

---

## Phase 5: State Management Integration (Days 11-12)

### 5.1 Profile Persistence

**Goal**: Save/load profile specifications for reuse.

**Tasks**:
- [ ] Add profile storage to StateManager
- [ ] Create `save_profile()` and `load_profile()` functions
- [ ] Add profile versioning
- [ ] Create profile listing/search

### 5.2 Execution History

**Tasks**:
- [ ] Track profile executions with metadata
- [ ] Link cohorts to their source profiles
- [ ] Enable re-execution with same seed

---

## Phase 6: Testing & Documentation (Days 13-15)

### 6.1 Comprehensive Test Suite

**Tasks**:
- [ ] Unit tests for each distribution type
- [ ] Unit tests for profile executor
- [ ] Integration tests for profile→journey→output flow
- [ ] Cross-product integration tests
- [ ] Performance tests for large cohorts (1000+ entities)

### 6.2 User Documentation

**Tasks**:
- [ ] Create `docs/guides/generative-framework.md` user guide
- [ ] Add examples for each product
- [ ] Update Skills with profile integration patterns
- [ ] Create video/demo script for Oswald family journey

---

## Success Criteria

### Minimum Viable Implementation

1. **End-to-end flow works**: User can specify → execute → get output
2. **All products consistent**: Same pattern across MemberSim, PatientSim, RxMemberSim, TrialSim
3. **Reference data integrated**: Can use PopulationSim geography
4. **Persisted profiles**: Can save and reuse specifications
5. **Tests pass**: Integration tests prove the system works

### The "Oswald Family" Demo

Ultimate proof: Execute this specification end-to-end:

```json
{
  "scenario": "Oswald Family Healthcare Journey",
  "profile": {
    "source": "populationsim",
    "reference": {"type": "county", "fips": "06073"},
    "members": [
      {"role": "subscriber", "age": 42, "conditions": ["E11"]},
      {"role": "spouse", "age": 40},
      {"role": "dependent", "age": 16}
    ]
  },
  "journeys": [
    {"member": "subscriber", "template": "diabetic_management_year"},
    {"member": "spouse", "template": "pregnancy_journey"},
    {"member": "subscriber", "template": "trial_participation"}
  ],
  "outputs": ["x12_834", "x12_837", "fhir_bundle", "sdtm_datasets"]
}
```

---

## Progress Tracking

Use this section to track progress during implementation.

### Week 1: Foundation

| Task | Status | Notes |
|------|--------|-------|
| Integration test created | ⬜ | |
| ProfileExecutor verified | ⬜ | |
| ReferenceProfileResolver verified | ⬜ | |
| JourneyEngine verified | ⬜ | |
| State persistence verified | ⬜ | |

### Week 2: Product Integration

| Task | Status | Notes |
|------|--------|-------|
| MemberSim generation module | ⬜ | |
| PatientSim generation module | ⬜ | |
| RxMemberSim generation module | ⬜ | |
| TrialSim generation module | ⬜ | |
| Profile→Journey orchestrator | ⬜ | |

### Week 3: Integration & Testing

| Task | Status | Notes |
|------|--------|-------|
| Skill integration pattern | ⬜ | |
| Reference data initialization | ⬜ | |
| Profile persistence | ⬜ | |
| Test suite complete | ⬜ | |
| Documentation complete | ⬜ | |
| Oswald demo works | ⬜ | |

---

## Appendix: Existing Code Inventory

### Core Generation (`packages/core/src/healthsim/generation/`)

| File | Lines | Purpose |
|------|-------|---------|
| `distributions.py` | 716 | Statistical distributions |
| `profile_schema.py` | 265 | ProfileSpecification model |
| `profile_executor.py` | 594 | Execute profiles to entities |
| `reference_profiles.py` | 648 | PopulationSim integration |
| `journey_engine.py` | 1,195 | Event orchestration |
| `journey_validation.py` | ~200 | Journey spec validation |
| `cohort.py` | 160 | Cohort generation base |
| `reproducibility.py` | ~150 | Seed management |
| `handlers.py` | ~200 | Event handler registry |
| `triggers.py` | ~200 | Cross-domain triggers |

### State Management (`packages/core/src/healthsim/state/`)

| File | Lines | Purpose |
|------|-------|---------|
| `manager.py` | ~400 | StateManager (DuckDB) |
| `auto_persist.py` | ~300 | Token-efficient persistence |
| `summary.py` | ~200 | Cohort summaries |
| `session.py` | ~200 | Abstract session |
| `workspace.py` | ~200 | File-based workspaces |
| `provenance.py` | ~150 | Entity lineage tracking |

---

*End of Implementation Plan*
