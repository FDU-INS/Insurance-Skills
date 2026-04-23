# NetworkSim Architecture Consistency Guide

**Purpose**: Ensure NetworkSim follows established HealthSim patterns  
**Reference**: `docs/HEALTHSIM-ARCHITECTURE-GUIDE.md` (v3.0)

---

## 1. Current Repository Structure Analysis

### 1.1 Standard Directories

| Directory | Purpose | NetworkSim Needs? |
|-----------|---------|-------------------|
| `skills/{product}/` | Domain skills | ✅ Yes - already exists |
| `formats/` (root) | Output format transformations | ⚠️ Review - any new formats? |
| `references/` (root) | Shared reference data | ⚠️ Review - any new references? |
| `packages/{product}/` | Python code/MCP | ❓ TBD - likely no Python initially |
| `hello-healthsim/` | Tutorials/examples | ✅ Yes - add examples |
| `cohorts/{product}/` | Saved cohorts | ❓ Optional |

### 1.2 Observed Product Skill Structures

**PatientSim** (established pattern):
```
skills/patientsim/
├── SKILL.md                    # Master router
├── {cohort-name}.md          # Flat file per cohort
├── oncology/                   # Subcategory (allowed)
└── pediatrics/                 # Subcategory (allowed)
```

**MemberSim** (simplest pattern):
```
skills/membersim/
├── SKILL.md                    # Master router
└── {cohort-name}.md          # Flat files only
```

**PopulationSim** (richest pattern - data-heavy):
```
skills/populationsim/
├── SKILL.md
├── README.md
├── {domain-skill}.md           # Domain skills
├── data/                       # Embedded data package (148MB)
├── data-access/                # Data access skills
├── geographic/                 # Category skills
├── health-patterns/            # Category skills
├── sdoh/                       # Category skills
├── cohorts/                    # Category skills
├── models/                     # Schema definitions
├── references/                 # Product-specific references
└── integration/                # Cross-product skills
```

**TrialSim** (domain-heavy pattern):
```
skills/trialsim/
├── SKILL.md
├── README.md
├── clinical-trials-domain.md   # Domain knowledge
├── phase{n}-{name}.md          # Phase skills
├── domains/                    # CDISC domain skills
├── therapeutic-areas/          # TA-specific skills
└── rwe/                        # Real-world evidence
```

### 1.3 Architecture Guide vs. Reality

| Guideline | Architecture Guide Says | Observed Reality |
|-----------|------------------------|------------------|
| Schemas | "Schemas defined inline in skills" | PopulationSim has `models/` folder |
| References | "ALL reference data in root `references/`" | PopulationSim has `references/` in skills |
| Formats | "ALL output formats in root `formats/`" | Consistent ✅ |
| Subcategories | "Use sparingly" | PopulationSim has many |

**Resolution**: PopulationSim is the newest, most complete product. Its pattern (with data/, models/, references/ within skills) is justified for data-heavy products. For NetworkSim (public version with no embedded data), we should follow a simpler pattern.

---

## 2. NetworkSim Recommended Structure

### 2.1 Proposed Directory Structure

```
skills/networksim/
├── SKILL.md                              # Master router (REQUIRED)
├── README.md                             # Product overview (REQUIRED)
│
├── reference/                            # Product-specific reference knowledge
│   ├── network-types.md                  # HMO, PPO, EPO, etc.
│   ├── plan-structures.md                # Benefit design concepts
│   ├── pharmacy-benefit-concepts.md      # Tier structures
│   ├── pbm-operations.md                 # PBM overview
│   ├── utilization-management.md         # PA, step therapy
│   ├── specialty-pharmacy.md             # Hub models
│   └── network-adequacy.md               # Access standards
│
├── synthetic/                            # Generation skills
│   ├── synthetic-provider.md
│   ├── synthetic-facility.md
│   ├── synthetic-pharmacy.md
│   ├── synthetic-network.md
│   ├── synthetic-plan.md
│   └── synthetic-pharmacy-benefit.md
│
├── patterns/                             # Configuration templates
│   ├── hmo-network-pattern.md
│   ├── ppo-network-pattern.md
│   ├── pharmacy-benefit-patterns.md
│   ├── tiered-network-pattern.md
│   └── specialty-distribution-pattern.md
│
└── integration/                          # Cross-product integration
    ├── provider-for-encounter.md
    ├── network-for-member.md
    ├── pharmacy-for-rx.md
    ├── benefit-for-claim.md
    └── formulary-concepts-for-rx.md
```

### 2.2 What We're NOT Creating (Public Version)

| Directory | Why Not |
|-----------|---------|
| `data/` | No embedded data in public version (deferred to networksim-local) |
| `models/` | Schemas will be inline in skills (simpler for knowledge-focused product) |
| `packages/networksim/` | No Python code initially |
| `cohorts/networksim/` | Optional - add if needed later |

### 2.3 Pattern Justification

NetworkSim public version is **knowledge + patterns**, not **data-heavy** like PopulationSim. Therefore:
- Use subdirectories to organize skill categories (like TrialSim's `therapeutic-areas/`)
- Keep schemas inline in skills (per architecture guide)
- No separate data package needed

---

## 3. VS Code Workspace Updates

### 3.1 Current Configuration

NetworkSim is already in the workspace:
```json
{ "name": "skills/networksim", "path": "skills/networksim" }
```

### 3.2 Required Updates

If we add Python package later:
```json
{ "name": "packages/networksim", "path": "packages/networksim" }
```

**Action**: No workspace update needed for Phase 1.

---

## 4. Testing Strategy

### 4.1 Current Test Locations

```
packages/core/tests/           # Core library tests
packages/patientsim/tests/     # PatientSim tests
packages/membersim/tests/      # MemberSim tests
packages/rxmembersim/tests/    # RxMemberSim tests
```

### 4.2 NetworkSim Testing

**Phase 1-5 (Skills only)**: No Python tests needed
- Test by conversational generation requests
- Document test cases in hello-healthsim examples

**Future (if Python added)**:
```
packages/networksim/
├── pyproject.toml
├── src/networksim/
└── tests/
    ├── test_provider.py
    ├── test_facility.py
    └── test_pharmacy.py
```

### 4.3 Running Tests

```bash
# Run all tests
cd /Users/markoswald/Developer/projects/healthsim-workspace
pytest packages/

# Run specific product tests
pytest packages/core/tests/
pytest packages/patientsim/tests/
```

---

## 5. Git Workflow

### 5.1 Commit Message Format

Per project instructions:
```
[NetworkSim] Brief description
```

Examples:
```
[NetworkSim] Phase 1: Foundation + Reference Knowledge
[NetworkSim] Add synthetic-provider.md skill
[NetworkSim] Update cross-product integration references
```

### 5.2 Workflow Per Session

```bash
# Before starting
git status
git pull origin main

# During work - commit frequently
git add skills/networksim/
git commit -m "[NetworkSim] Add network-types.md reference skill"

# After completing phase
git push origin main
```

### 5.3 Sync Checkpoints

- After completing each skill file
- After completing each phase
- Before ending any work session

---

## 6. Cross-Product Integration Updates

### 6.1 Files Requiring Updates

When NetworkSim is complete, update these files to add cross-references:

| File | Update Needed |
|------|---------------|
| `skills/patientsim/SKILL.md` | Add NetworkSim to Related Skills |
| `skills/membersim/SKILL.md` | Add NetworkSim to Related Skills |
| `skills/rxmembersim/SKILL.md` | Add NetworkSim to Related Skills |
| `skills/trialsim/SKILL.md` | Add NetworkSim to Related Skills |
| `skills/populationsim/SKILL.md` | Add NetworkSim to Related Skills |
| `SKILL.md` (master) | Add NetworkSim routing |
| `docs/HEALTHSIM-ARCHITECTURE-GUIDE.md` | Update product table, status |
| `references/data-models.md` | Add Provider entity model |

### 6.2 Cross-Reference Pattern

In each product's SKILL.md, add to Related Skills section:
```markdown
## Related Skills

### Cross-Product Integration
- [NetworkSim](../networksim/SKILL.md) - Provider and network generation
  - Use `integration/provider-for-encounter.md` when generating encounters
```

---

## 7. Hello-HealthSim Examples

### 7.1 Required Examples

Add to `hello-healthsim/examples/`:

| Example | Purpose |
|---------|---------|
| `networksim-provider-generation.md` | Generate synthetic provider |
| `networksim-network-types.md` | Explain network types |
| `networksim-integration.md` | Cross-product example |

### 7.2 Example Template

```markdown
# NetworkSim: Generate a Synthetic Provider

## Prompt
"Generate a cardiologist in San Diego for a heart failure patient"

## Response
[Expected Claude response with provider details]

## What's Happening
- NetworkSim generates valid synthetic NPI
- Specialty assigned based on request
- Location matches geography
- Provenance marked as SYNTHETIC
```

---

## 8. Checklist: Architecture Consistency

### Pre-Implementation
- [x] Review architecture guide
- [x] Compare to existing products
- [x] Define consistent structure
- [x] Document in this guide

### Per Phase
- [ ] Follow directory structure defined above
- [ ] Use YAML frontmatter on all skills
- [ ] Include ≥2 examples per skill
- [ ] Add cross-references to related skills
- [ ] Commit with proper message format
- [ ] Push to GitHub

### Post-Implementation
- [ ] Update VS Code workspace (if needed)
- [ ] Update master SKILL.md
- [ ] Update architecture guide product table
- [ ] Add hello-healthsim examples
- [ ] Update CHANGELOG.md
- [ ] Run any applicable tests
- [ ] Final git push

---

## 9. Deferred Items (networksim-local)

These items are explicitly deferred to the private networksim-local repository:

| Item | Notes |
|------|-------|
| Embedded data package | NPPES, POS, HPSA data |
| Data processing scripts | Python ETL |
| DuckDB integration | Local database |
| Parquet extracts | Optimized data files |
| MCP server | Local file access |

---

*Document Version: 1.0 | Created: 2024-12-24*
