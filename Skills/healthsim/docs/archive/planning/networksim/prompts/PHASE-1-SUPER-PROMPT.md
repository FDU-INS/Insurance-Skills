# NetworkSim Phase 1 Super-Prompt

**Purpose**: Foundation + Reference Knowledge + Core Documentation  
**Target Environment**: Claude Code  
**Estimated Duration**: 1-2 sessions  
**Version**: 1.0  
**Created**: 2024-12-24

---

## Instructions for Claude Code

This is a self-contained implementation prompt. Execute each section in order, completing all checkpoints before proceeding.

---

## PRE-FLIGHT CHECKLIST

Before implementing anything, read these files to establish context:

### Required Reading (Execute These First)

```
1. Read: docs/networksim/NETWORKSIM-PROJECT-PLAN.md
   Focus: Sections 1-5 (Executive Summary through Implementation Phases)
   
2. Read: docs/networksim/NETWORKSIM-ARCHITECTURE-CONSISTENCY.md
   Focus: Directory structure, what NOT to create
   
3. Read: docs/networksim/NETWORKSIM-DOCUMENTATION-PLAN.md
   Focus: Section 2 (Documentation Deliverables)
   
4. Read: skills/populationsim/developer-guide.md
   Focus: Structure and quality as template to match
   
5. Read: skills/populationsim/prompt-guide.md
   Focus: Structure and example organization
   
6. Read: skills/trialsim/SKILL.md
   Focus: Master router pattern
   
7. Check: docs/networksim/NETWORKSIM-IMPLEMENTATION-STATUS.md
   Purpose: Verify current progress, don't repeat completed work
```

### Pre-Flight Verification

After reading, confirm understanding:
- [ ] NetworkSim = knowledge + entity generation (NOT claim processing)
- [ ] Directory structure: skills/networksim/{reference,synthetic,patterns,integration}/
- [ ] No embedded data (that's for networksim-local)
- [ ] Documentation target: README 400+ lines, dev-guide shell, prompt-guide shell

---

## PHASE 1 DELIVERABLES

### Files to Create

| File | Type | Priority | Lines |
|------|------|----------|-------|
| skills/networksim/reference/ | Directory | Must | - |
| skills/networksim/synthetic/ | Directory | Must | - |
| skills/networksim/patterns/ | Directory | Must | - |
| skills/networksim/integration/ | Directory | Must | - |
| skills/networksim/SKILL.md | Master Router | Must | 200-300 |
| skills/networksim/README.md | Product Overview | Must | 400-500 |
| skills/networksim/developer-guide.md | Dev Guide Shell | Must | 150-200 |
| skills/networksim/prompt-guide.md | Prompt Guide Shell | Must | 150-200 |
| skills/networksim/reference/network-types.md | Reference | Must | 300-400 |
| skills/networksim/reference/plan-structures.md | Reference | Must | 250-350 |
| skills/networksim/reference/pharmacy-benefit-concepts.md | Reference | Must | 250-350 |
| skills/networksim/reference/pbm-operations.md | Reference | Should | 200-300 |
| skills/networksim/reference/utilization-management.md | Reference | Should | 200-300 |
| skills/networksim/reference/specialty-pharmacy.md | Reference | Should | 200-300 |
| skills/networksim/reference/network-adequacy.md | Reference | Could | 200-300 |

---

## IMPLEMENTATION STEPS

### Step 1: Create Directory Structure

```bash
mkdir -p skills/networksim/reference
mkdir -p skills/networksim/synthetic
mkdir -p skills/networksim/patterns
mkdir -p skills/networksim/integration
```

**Checkpoint 1**: Verify directories exist with `ls -la skills/networksim/`

---

### Step 2: Create SKILL.md (Master Router)

**File**: `skills/networksim/SKILL.md`

**Template to Follow**: `skills/trialsim/SKILL.md`

**Required Content**:

```markdown
---
name: networksim
description: |
  Healthcare network knowledge and entity generation. Reference information about 
  network types, plan structures, pharmacy benefits, and PBM operations. Synthetic 
  generation of providers, facilities, pharmacies, and network configurations.
  Cross-product integration for realistic healthcare data generation.
version: "1.0"
status: "Active"
---

# NetworkSim

## Overview

NetworkSim provides healthcare network knowledge and synthetic entity generation 
for the HealthSim ecosystem. Unlike other products that generate transaction data, 
NetworkSim focuses on:

1. **Reference Knowledge** - Network types, plan structures, pharmacy benefits, PBM operations
2. **Synthetic Generation** - Providers, facilities, pharmacies, network configurations
3. **Integration Patterns** - Cross-product enhancement for realistic data

## When to Use NetworkSim

| Need | Skill Category | Example |
|------|---------------|---------|
| Understand network types | reference/ | "Explain the difference between HMO and PPO" |
| Generate a provider | synthetic/ | "Generate a cardiologist in Houston" |
| Generate a facility | synthetic/ | "Generate a 200-bed community hospital" |
| Generate a pharmacy | synthetic/ | "Generate a specialty pharmacy" |
| Use a network template | patterns/ | "Create an HMO network configuration" |
| Enhance other products | integration/ | "Generate a provider for this encounter" |

## Skill Categories

### Reference Knowledge (reference/)
Educational content about healthcare networks and benefits.

- [Network Types](reference/network-types.md) - HMO, PPO, EPO, POS, HDHP definitions
- [Plan Structures](reference/plan-structures.md) - Benefit design concepts
- [Pharmacy Benefit Concepts](reference/pharmacy-benefit-concepts.md) - Tier structures, formulary concepts
- [PBM Operations](reference/pbm-operations.md) - PBM function overview
- [Utilization Management](reference/utilization-management.md) - PA, step therapy, quantity limits
- [Specialty Pharmacy](reference/specialty-pharmacy.md) - Hub model, specialty distribution
- [Network Adequacy](reference/network-adequacy.md) - Access standards, time/distance

### Synthetic Generation (synthetic/)
Generate realistic synthetic healthcare entities.

- [Synthetic Provider](synthetic/synthetic-provider.md) - Generate provider entities
- [Synthetic Facility](synthetic/synthetic-facility.md) - Generate facility entities
- [Synthetic Pharmacy](synthetic/synthetic-pharmacy.md) - Generate pharmacy entities
- [Synthetic Network](synthetic/synthetic-network.md) - Generate network configurations
- [Synthetic Plan](synthetic/synthetic-plan.md) - Generate plan benefit structures
- [Synthetic Pharmacy Benefit](synthetic/synthetic-pharmacy-benefit.md) - Generate pharmacy benefit designs

### Patterns & Templates (patterns/)
Reusable configuration patterns.

- [HMO Network Pattern](patterns/hmo-network-pattern.md) - Typical HMO structure
- [PPO Network Pattern](patterns/ppo-network-pattern.md) - Typical PPO structure
- [Tiered Network Pattern](patterns/tiered-network-pattern.md) - Narrow/tiered networks
- [Pharmacy Benefit Patterns](patterns/pharmacy-benefit-patterns.md) - Common PBM configurations
- [Specialty Distribution Pattern](patterns/specialty-distribution-pattern.md) - Hub vs retail routing

### Cross-Product Integration (integration/)
Enhance other HealthSim products with network context.

- [Provider for Encounter](integration/provider-for-encounter.md) - PatientSim integration
- [Network for Member](integration/network-for-member.md) - MemberSim integration
- [Pharmacy for RX](integration/pharmacy-for-rx.md) - RxMemberSim integration
- [Benefit for Claim](integration/benefit-for-claim.md) - MemberSim claims context
- [Formulary Concepts for RX](integration/formulary-concepts-for-rx.md) - RxMemberSim formulary context

## Quick Start Examples

### Example 1: Network Type Reference
```
User: What's the difference between an HMO and a PPO?

Claude: [Routes to reference/network-types.md]
[Provides comprehensive comparison with cost/flexibility tradeoffs]
```

### Example 2: Generate a Provider
```
User: Generate a cardiologist in San Diego

Claude: [Routes to synthetic/synthetic-provider.md]
[Generates provider with NPI, credentials, taxonomy, address]
```

### Example 3: Cross-Product Integration
```
User: Generate a provider for this heart failure patient's cardiology referral

Claude: [Routes to integration/provider-for-encounter.md]
[Generates appropriate specialist with context from PatientSim encounter]
```

## Related Products

| Product | NetworkSim Provides | Integration Skill |
|---------|--------------------|--------------------|
| PatientSim | Providers for encounters | provider-for-encounter.md |
| MemberSim | Network context for claims | network-for-member.md |
| RxMemberSim | Pharmacies for prescriptions | pharmacy-for-rx.md |
| TrialSim | Sites and investigators | provider-for-encounter.md |
| PopulationSim | Provider access patterns | network-adequacy.md |

## Boundary Rules

**NetworkSim Owns**:
- Network type knowledge and definitions
- Provider/facility/pharmacy entity generation
- Network configuration patterns
- Benefit design concepts

**Other Products Own**:
- Claim processing logic (MemberSim)
- Formulary drug coverage (RxMemberSim)
- Encounter generation (PatientSim)
- Geographic data (PopulationSim)

## Documentation

- [README](README.md) - Product overview and quick start
- [Developer Guide](developer-guide.md) - Technical reference
- [Prompt Guide](prompt-guide.md) - Example prompts by category
```

**Checkpoint 2**: 
- File created at `skills/networksim/SKILL.md`
- Contains all 4 skill category sections
- Links to skills that will be created later (OK if broken for now)

---

### Step 3: Create README.md (Comprehensive)

**File**: `skills/networksim/README.md`

**Template to Follow**: `skills/populationsim/README.md`

**Target Length**: 400-500 lines

**Required Sections**:

1. **Product Overview** (what NetworkSim provides)
2. **Key Capabilities** (reference, generation, integration)
3. **Quick Start** (3 example prompts with expected outputs)
4. **Skill Organization** (categories with descriptions)
5. **Use Cases by Audience** (developers, analysts, educators)
6. **Integration Points** (how NetworkSim enhances other products)
7. **Core Concepts** (network types, provider taxonomy, facility types, pharmacy classification)
8. **Output Formats** (canonical JSON schemas)
9. **What NetworkSim Does NOT Do** (boundary clarification)
10. **Version History / Roadmap**
11. **Related Documentation** (links)

**Content Guidelines**:
- Include full JSON examples in Quick Start (not truncated)
- Show comparison tables where appropriate
- Progressive complexity (simple → advanced)
- Cross-reference related skills and docs

**Checkpoint 3**:
- File created at `skills/networksim/README.md`
- Contains all 11 required sections
- At least 400 lines
- At least 2 full JSON examples

---

### Step 4: Create Developer Guide Shell

**File**: `skills/networksim/developer-guide.md`

**Purpose**: Shell structure to be completed in Phase 5

**Required Content** (shell with placeholders):

```markdown
---
name: networksim-developer-guide
description: |
  Developer guide for NetworkSim covering quick start, core concepts,
  skill reference, workflows, output formats, integration points, and
  best practices for working with healthcare network data.
---

# NetworkSim Developer Guide

## Overview

NetworkSim provides healthcare network knowledge and synthetic entity generation
for the HealthSim ecosystem. This guide covers technical details for developers
integrating NetworkSim into their workflows.

---

## Quick Start

### 1. Network Type Reference

```
User: Explain the difference between HMO and PPO networks

Claude: [Comprehensive explanation with comparison table]
```

### 2. Synthetic Provider Generation

```
User: Generate a cardiologist in Houston, Texas

Claude: [Full provider entity with NPI, credentials, taxonomy, address]
```

### 3. Cross-Product Integration

```
User: Generate a provider for this heart failure patient's cardiology referral

Claude: [Provider matched to encounter context]
```

---

## Core Concepts

### Network Types
[To be completed in Phase 5 - see reference/network-types.md]

### Provider Taxonomy
[To be completed in Phase 5 - NUCC taxonomy codes, specialty distribution]

### Facility Types
[To be completed in Phase 5 - Hospital, ambulatory, post-acute categories]

### Pharmacy Classification
[To be completed in Phase 5 - Retail, mail order, specialty]

---

## Skill Reference

| Skill | Purpose | Trigger Phrases |
|-------|---------|-----------------|
| network-types | Network type definitions | "explain HMO", "difference between PPO and EPO" |
| plan-structures | Benefit design concepts | "plan structure", "deductible vs copay" |
| pharmacy-benefit-concepts | Pharmacy benefit design | "tier structure", "formulary" |
| synthetic-provider | Generate providers | "generate provider", "create physician" |
| synthetic-facility | Generate facilities | "generate hospital", "create ASC" |
| synthetic-pharmacy | Generate pharmacies | "generate pharmacy", "create specialty pharmacy" |

---

## Common Workflows

### Workflow 1: Provider for Clinical Encounter
[To be completed in Phase 5]

### Workflow 2: Network for Member Plan
[To be completed in Phase 5]

### Workflow 3: Pharmacy for Prescription
[To be completed in Phase 5]

### Workflow 4: Site for Clinical Trial
[To be completed in Phase 5]

---

## Output Formats

### Provider Entity (Canonical JSON)
[To be completed in Phase 5 - full schema]

### Facility Entity (Canonical JSON)
[To be completed in Phase 5 - full schema]

### Pharmacy Entity (Canonical JSON)
[To be completed in Phase 5 - full schema]

---

## Integration Points

### To PatientSim
[To be completed in Phase 5]

### To MemberSim
[To be completed in Phase 5]

### To RxMemberSim
[To be completed in Phase 5]

### To TrialSim
[To be completed in Phase 5]

### From PopulationSim
[To be completed in Phase 5]

---

## Best Practices

1. **Be Specific About Geography** - Include city, county, or state for provider generation
2. **Specify Specialty When Relevant** - Use specific specialty names, not generic terms
3. **Include Context for Integration** - Provide encounter/claim context for cross-product use
4. **Request Specific Output When Needed** - Ask for taxonomy codes, credentials if required
5. [Additional best practices to be added in Phase 5]

---

## Troubleshooting

[To be completed in Phase 5]

---

## Related Documentation

- [SKILL.md](SKILL.md) - Main skill reference
- [Prompt Guide](prompt-guide.md) - Example prompts
- [README](README.md) - Product overview
```

**Checkpoint 4**:
- File created at `skills/networksim/developer-guide.md`
- Contains all section headers
- Quick Start section is complete
- Placeholders clearly marked "[To be completed in Phase 5]"

---

### Step 5: Create Prompt Guide Shell

**File**: `skills/networksim/prompt-guide.md`

**Purpose**: Shell with Reference section complete, other sections as placeholders

**Required Content**:

```markdown
---
name: networksim-prompt-guide
description: |
  Example prompts for using NetworkSim skills effectively. Templates for
  network reference, provider generation, facility generation, pharmacy
  generation, and cross-product integration cohorts.
---

# NetworkSim Prompt Guide

## Overview

This guide provides example prompts for using NetworkSim skills effectively.
Use these templates as starting points for network reference queries and
synthetic entity generation.

---

## Reference Knowledge Prompts

### Network Type Explanations

```
Explain the difference between HMO and PPO networks
```
**Expected**: Comprehensive comparison with cost/flexibility tradeoffs

```
What are the key characteristics of an EPO plan?
```
**Expected**: EPO definition, how it differs from HMO and PPO

```
When would a patient choose a POS plan over HMO?
```
**Expected**: POS advantages, point-of-service decision explanation

```
Explain HDHP plans and HSA eligibility requirements
```
**Expected**: HDHP thresholds, HSA rules, triple tax advantage

---

### Plan Structure Concepts

```
What components make up a typical health plan benefit structure?
```
**Expected**: Deductibles, copays, coinsurance, OOP max explanation

```
Explain the difference between in-network and out-of-network benefits
```
**Expected**: Cost sharing differences, balance billing, UCR

```
How do tiered networks work?
```
**Expected**: Tier structure, cost incentives, narrow network concept

---

### Pharmacy Benefit Concepts

```
Explain pharmacy benefit tier structures
```
**Expected**: 4-5 tier explanation, cost sharing by tier

```
What's the difference between open and closed formularies?
```
**Expected**: Formulary types, coverage implications

```
How do preferred pharmacy networks work?
```
**Expected**: Preferred vs non-preferred, cost incentives

```
Explain specialty pharmacy vs retail pharmacy
```
**Expected**: Specialty characteristics, limited distribution, hub model

---

### PBM Operations

```
How does a PBM process pharmacy claims?
```
**Expected**: Claim flow, BIN/PCN routing, adjudication steps

```
What's the relationship between a health plan and PBM?
```
**Expected**: Carve-out vs carve-in, PBM services

```
Explain the formulary management process
```
**Expected**: P&T committee, tier placement, clinical criteria

---

### Utilization Management

```
What is prior authorization and when is it required?
```
**Expected**: PA process, common PA drugs, approval criteria

```
Explain step therapy requirements
```
**Expected**: Step therapy concept, first-line/second-line, exceptions

```
How do quantity limits work?
```
**Expected**: QL types, safety vs cost, override process

---

## Synthetic Generation Prompts

### Provider Generation
[To be completed in Phase 5 - 10+ example prompts]

### Facility Generation
[To be completed in Phase 5 - 10+ example prompts]

### Pharmacy Generation
[To be completed in Phase 5 - 10+ example prompts]

### Network Configuration
[To be completed in Phase 5 - 5+ example prompts]

---

## Cross-Product Integration Prompts

### PatientSim Integration
[To be completed in Phase 5]

### MemberSim Integration
[To be completed in Phase 5]

### RxMemberSim Integration
[To be completed in Phase 5]

### TrialSim Integration
[To be completed in Phase 5]

### PopulationSim Integration
[To be completed in Phase 5]

---

## Advanced Prompts

[To be completed in Phase 5]

---

## Tips for Effective Prompts

### Be Specific About Geography
✅ "Generate a cardiologist in Harris County, Texas"
❌ "Generate a doctor in Texas"

### Specify Specialty When Relevant
✅ "Generate an interventional cardiologist"
❌ "Generate a heart doctor"

### Include Context for Integration
✅ "Generate a provider for this heart failure patient's cardiology referral"
❌ "Generate a provider"

### Request Specific Output When Needed
✅ "Generate a provider with full taxonomy codes and credentials"
❌ "Generate a provider"

---

## Related Documentation

- [Developer Guide](developer-guide.md)
- [SKILL.md](SKILL.md)
- [Integration Skills](integration/)
```

**Checkpoint 5**:
- File created at `skills/networksim/prompt-guide.md`
- Reference Knowledge section is COMPLETE (all prompts filled in)
- Other sections have placeholders
- Tips section is complete

---

### Step 6: Create Reference Skills (Must Priority)

Create these three reference skills with full content:

#### 6A: network-types.md

**File**: `skills/networksim/reference/network-types.md`

**Required Sections**:
- YAML frontmatter with name, description (include trigger phrases)
- Overview
- Trigger Phrases list
- HMO section (definition, characteristics, pros/cons, when to use)
- PPO section (same structure)
- EPO section (same structure)
- POS section (same structure)
- HDHP section (same structure, include HSA eligibility)
- Comparison Table (all 5 types across key dimensions)
- When to Use Each Type (generation guidance)
- Examples (at least 2 complete examples with full responses)
- Related Skills

**Target Length**: 300-400 lines

---

#### 6B: plan-structures.md

**File**: `skills/networksim/reference/plan-structures.md`

**Required Sections**:
- YAML frontmatter
- Overview
- Trigger Phrases
- Benefit Components (deductible, copay, coinsurance, OOP max)
- Cost Sharing Mechanics (how each component works)
- In-Network vs Out-of-Network (cost differences, balance billing)
- Accumulator Types (deductible, OOP, family vs individual)
- Common Plan Designs (Bronze/Silver/Gold/Platinum, employer typical)
- Examples (at least 2)
- Related Skills

**Target Length**: 250-350 lines

---

#### 6C: pharmacy-benefit-concepts.md

**File**: `skills/networksim/reference/pharmacy-benefit-concepts.md`

**Required Sections**:
- YAML frontmatter
- Overview
- Trigger Phrases
- Tier Structures (4-tier, 5-tier, specialty tier)
- Formulary Types (open, closed, incentive)
- Pharmacy Networks (preferred, non-preferred, mail, specialty)
- Cost Sharing (copay vs coinsurance by tier)
- Accumulator Integration (medical vs pharmacy deductible)
- Specialty Pharmacy Requirements (when specialty required)
- Examples (at least 2)
- Related Skills

**Boundary Note**: This skill explains CONCEPTS. RxMemberSim owns drug-specific coverage.

**Target Length**: 250-350 lines

**Checkpoint 6**:
- All three Must-priority reference skills created
- Each has YAML frontmatter
- Each has at least 2 complete examples
- Each is 250+ lines

---

### Step 7: Create Reference Skills (Should Priority)

Create these three reference skills:

#### 7A: pbm-operations.md

**File**: `skills/networksim/reference/pbm-operations.md`

**Content Focus**:
- What is a PBM (high-level)
- PBM Services (claims processing, formulary management, rebates, mail order)
- Claim Flow (pharmacy → PBM → response)
- BIN/PCN/Group routing
- Relationship to Health Plans (carve-in vs carve-out)
- Major PBM models (traditional, pass-through, transparent)

**Target Length**: 200-300 lines

---

#### 7B: utilization-management.md

**File**: `skills/networksim/reference/utilization-management.md`

**Content Focus**:
- Prior Authorization (what, when, process)
- Step Therapy (concept, common cohorts)
- Quantity Limits (safety, cost, days supply)
- Exception Processes (how to override)
- Clinical Criteria (P&T, evidence-based)

**Target Length**: 200-300 lines

---

#### 7C: specialty-pharmacy.md

**File**: `skills/networksim/reference/specialty-pharmacy.md`

**Content Focus**:
- What makes a drug "specialty"
- Limited Distribution model
- Hub/Spoke model
- REMS programs (high-level)
- Specialty pharmacy services (care coordination, adherence)
- Cost (specialty tier, copay assistance)
- Retail vs specialty routing

**Target Length**: 200-300 lines

**Checkpoint 7**:
- All three Should-priority reference skills created
- Each has YAML frontmatter
- Each has at least 2 examples

---

### Step 8: Create Reference Skill (Could Priority)

#### network-adequacy.md

**File**: `skills/networksim/reference/network-adequacy.md`

**Content Focus**:
- What is network adequacy
- Time/Distance standards (urban, suburban, rural)
- Provider-to-member ratios
- Essential community providers
- State and federal requirements
- HPSA/MUA concepts (link to PopulationSim)
- Access disparity patterns

**Target Length**: 200-300 lines

**Checkpoint 8**:
- File created
- Links to PopulationSim for geographic data

---

### Step 9: Git Commit Checkpoint

```bash
cd /Users/markoswald/Developer/projects/healthsim-workspace

# Stage all new files
git add skills/networksim/

# Commit with descriptive message
git commit -m "[NetworkSim] Phase 1: Foundation + Reference Knowledge

- Created directory structure (reference/, synthetic/, patterns/, integration/)
- Created SKILL.md master router with all skill categories
- Created comprehensive README.md (400+ lines)
- Created developer-guide.md shell with Quick Start
- Created prompt-guide.md shell with Reference section complete
- Created 7 reference skills:
  - network-types.md (Must)
  - plan-structures.md (Must)
  - pharmacy-benefit-concepts.md (Must)
  - pbm-operations.md (Should)
  - utilization-management.md (Should)
  - specialty-pharmacy.md (Should)
  - network-adequacy.md (Could)"

# Push to remote
git push origin main
```

**Checkpoint 9**: Git commit successful, pushed to main

---

## POST-FLIGHT CHECKLIST

### Update Implementation Status

Update `docs/networksim/NETWORKSIM-IMPLEMENTATION-STATUS.md`:

```markdown
## Session Log

### Session: [DATE]
**Phase**: 1 - Foundation + Reference Knowledge
**Duration**: [X hours]
**Status**: Complete

**Completed Tasks**:
- [x] 1.1 Create directory structure
- [x] 1.2 Update SKILL.md (master router)
- [x] 1.3 Update README.md (comprehensive)
- [x] 1.4 Write network-types.md
- [x] 1.5 Write plan-structures.md
- [x] 1.6 Write pharmacy-benefit-concepts.md
- [x] 1.7 Write pbm-operations.md
- [x] 1.8 Write utilization-management.md
- [x] 1.9 Write specialty-pharmacy.md
- [x] 1.10 Write network-adequacy.md
- [x] 1.11 Create developer-guide.md (shell)
- [x] 1.12 Create prompt-guide.md (shell)

**Files Created**:
- skills/networksim/SKILL.md
- skills/networksim/README.md
- skills/networksim/developer-guide.md
- skills/networksim/prompt-guide.md
- skills/networksim/reference/network-types.md
- skills/networksim/reference/plan-structures.md
- skills/networksim/reference/pharmacy-benefit-concepts.md
- skills/networksim/reference/pbm-operations.md
- skills/networksim/reference/utilization-management.md
- skills/networksim/reference/specialty-pharmacy.md
- skills/networksim/reference/network-adequacy.md

**Line Counts**:
- SKILL.md: [X] lines
- README.md: [X] lines
- developer-guide.md: [X] lines
- prompt-guide.md: [X] lines
- Reference skills total: [X] lines

**Next Phase**: Phase 2 - Synthetic Generation
```

### Commit Status Update

```bash
git add docs/networksim/NETWORKSIM-IMPLEMENTATION-STATUS.md
git commit -m "[NetworkSim] Update implementation status - Phase 1 complete"
git push origin main
```

---

## SUCCESS CRITERIA

Phase 1 is complete when:

- [ ] All 4 directories created (reference/, synthetic/, patterns/, integration/)
- [ ] SKILL.md routes to all skill categories (200+ lines)
- [ ] README.md is comprehensive (400+ lines)
- [ ] developer-guide.md shell exists with Quick Start complete
- [ ] prompt-guide.md shell exists with Reference section complete
- [ ] 7 reference skills created with YAML frontmatter
- [ ] Each reference skill has ≥2 complete examples
- [ ] All files committed and pushed to GitHub
- [ ] Implementation status updated

---

## TROUBLESHOOTING

### If context window fills up
- Complete current checkpoint
- Commit progress
- Update status document
- Continue in new session from next checkpoint

### If unsure about content
- Reference existing skills in populationsim/ and trialsim/
- Check NETWORKSIM-PROJECT-PLAN.md Section 6 for specifications
- Follow patterns from similar existing skills

### If boundary confusion
- NetworkSim = knowledge + entity generation
- MemberSim = claim processing
- RxMemberSim = pharmacy claim processing + formulary rules
- When in doubt, explain concepts, don't implement logic

---

## NEXT PHASE PREVIEW

**Phase 2: Synthetic Generation** will create:
- synthetic-provider.md
- synthetic-facility.md
- synthetic-pharmacy.md
- synthetic-network.md
- synthetic-plan.md
- synthetic-pharmacy-benefit.md

Super-prompt will be created after Phase 1 review in Claude Desktop.

---

*End of Phase 1 Super-Prompt*
