# HealthSim Claude Project Instructions

*Condensed guardrails for consistent development. Full details in docs/HEALTHSIM-ARCHITECTURE-GUIDE.md and docs/HEALTHSIM-DEVELOPMENT-PROCESS.md*

---

## Core Philosophy

**Conversation-First**: HealthSim generates synthetic healthcare data via natural language + Skills. No Python libraries or APIs - Skills contain domain knowledge, Claude generates data dynamically.

**Design → Super-Prompt → Implement**: Design thoroughly in Claude Desktop, create comprehensive super-prompts, execute systematically in Claude Code.

---

## Session Protocol (MANDATORY)

### Starting Every Session

1. **Read `CURRENT-WORK.md` FIRST** - This file tracks live state across sessions
2. **Verify git state** matches documented state:
   ```bash
   cd /Users/markoswald/Developer/projects/healthsim-workspace
   git log --oneline -3
   ```
3. **Confirm which phase/task is next** from the "Next Session Should" section
4. **If recovering from interruption**: Run tests first to verify clean state

### During a Session

- **Commit frequently** - After each major file group, not at the very end
- **If context feels heavy** - Commit current work, update CURRENT-WORK.md, suggest continuing in new session
- **Verify as you go** - Don't batch all verification to the end

### Ending Every Session

1. **Run tests**: `cd packages/core && pytest tests/ -v`
2. **Commit all changes** with descriptive message
3. **Update `CURRENT-WORK.md`** with:
   - What was completed (with commit hash)
   - What's next
   - Any important notes for next session
4. **Push to remote**: `git push`

### Multi-Session Initiatives

For large initiatives (like NetworkSim), create atomic session prompts:

```
docs/initiatives/{initiative-name}/
  MASTER-PLAN.md              # High-level roadmap (stable)
  SESSION-01-description.md   # One session's work
  SESSION-02-description.md   # One session's work
  ...
```

Each session prompt should:
- Fit comfortably in context (avoid 2000+ line monoliths)
- Have ONE clear deliverable
- End with verification steps and "update CURRENT-WORK.md"

---

## Repository Structure

**Single Repository**: `healthsim-workspace` (https://github.com/mark64oswald/healthsim-workspace)

```
healthsim-workspace/
├── SKILL.md                    # Master routing skill
├── docs/                       # Architecture, process docs
├── references/                 # Code systems, validation rules (shared)
├── formats/                    # Output formats: FHIR, X12, CDISC, etc. (shared)
├── skills/                     # Domain-specific cohort skills
│   ├── common/                 # Shared skills
│   ├── patientsim/             # Clinical/EMR cohorts
│   ├── membersim/              # Payer/claims cohorts
│   ├── rxmembersim/            # Pharmacy/PBM cohorts
│   ├── trialsim/               # Clinical trials cohorts
│   ├── populationsim/          # Demographics/SDOH
│   └── networksim/             # Provider networks (planned)
├── hello-healthsim/            # Tutorials and examples
├── packages/                   # Python packages (infrastructure)
│   ├── core/                   # Shared library
│   ├── patientsim/             # PatientSim MCP/utilities
│   ├── membersim/              # MemberSim MCP/utilities
│   └── rxmembersim/            # RxMemberSim MCP/utilities
├── demos/                      # Interactive demos
└── scripts/                    # Utility scripts
```

---

## Architecture Rules

### Skills Organization

| Location | Content |
|----------|---------|
| `skills/{product}/` | Cohort and domain skills (flat structure) |
| `skills/{product}/{subcategory}/` | Allowed for logical groupings (oncology/, pediatrics/) |
| `formats/` | ALL output formats (shared, not product-specific) |
| `references/` | ALL reference data (shared, not product-specific) |

### DO NOT Create These Subdirectories

- `skills/{product}/cohorts/` - Put cohorts directly in product folder
- `skills/{product}/domain/` - Put domain files directly in product folder
- `skills/{product}/formats/` - Use root `formats/` instead
- `skills/{product}/models/` - Schemas defined inline in skills

### Skills Must Have

- YAML frontmatter with `name` and `description` (include trigger phrases)
- Sections: Overview, Trigger Phrases, Parameters table, Generation Patterns, Examples (≥2), Validation Rules, Related Skills

### Data Models

- Generate canonical JSON first, then transform to output format
- Extend common entities (Person → Patient → Member → Subject)
- Use standard code systems: ICD-10, CPT, LOINC, NDC, NPI, CDISC

### MCP = I/O Only

File system, database, GitHub operations. Generation happens in conversation.

---

## Products

| Product | Domain | Standards | Skills Location | Package Location |
|---------|--------|-----------|-----------------|------------------|
| PatientSim | Clinical/EMR | FHIR, HL7v2, C-CDA | `skills/patientsim/` | `packages/patientsim/` |
| MemberSim | Payer/Claims | X12 837/835/834 | `skills/membersim/` | `packages/membersim/` |
| RxMemberSim | Pharmacy/PBM | NCPDP D.0 | `skills/rxmembersim/` | `packages/rxmembersim/` |
| TrialSim | Clinical Trials | CDISC SDTM/ADaM | `skills/trialsim/` | - |
| PopulationSim | Demographics/SDOH | Census, ACS | `skills/populationsim/` | - |
| NetworkSim | Provider Networks | NPPES, NPI | `skills/networksim/` | - |

---

## Development Workflow

### Every Super-Prompt Must Include

1. Context + reference documents to read
2. Pre-flight checklist
3. Specific deliverables (files to create/modify)
4. Step-by-step implementation with verification
5. Post-flight checklist
6. Success criteria

### After Every Implementation Session

- [ ] Test with sample generation request
- [ ] Update CHANGELOG.md
- [ ] Verify documentation links
- [ ] Git add → commit (descriptive message) → push

### Commit Message Format

```
[Product] Brief description

Examples:
[TrialSim] Add Phase 3 pivotal trial skill
[MemberSim] Fix accumulator calculation example
[Docs] Clarify directory structure
```

---

## Quality Gates

### New Skill Checklist

- [ ] YAML frontmatter with `name` and `description` (triggers included)
- [ ] At least 2 complete examples with JSON output
- [ ] Linked from product SKILL.md routing table
- [ ] Cross-product check: Related skills identified, bidirectional links added
- [ ] hello-healthsim example added
- [ ] CHANGELOG.md updated

### New Product Checklist

- [ ] Directory: `skills/{product}/`
- [ ] Product SKILL.md created
- [ ] Master SKILL.md updated with routing
- [ ] Cross-product review: All existing products checked for integration
- [ ] VS Code workspace updated
- [ ] Architecture guide updated (including cross-product mapping)
- [ ] hello-healthsim quickstart added

---

## Test Failure Policy

When tests fail during implementation:

1. **STOP and diagnose** - Before making any changes, explain:
   - What the test is trying to verify
   - Why it's failing
   - Whether the problem is in the TEST or the IMPLEMENTATION

2. **Never modify test assertions to make them pass** - If a test's expectations need to change, explain why the original expectation was wrong, not just inconvenient.

3. **Ask if uncertain** - If there's any ambiguity about whether the test or implementation is at fault, ask before proceeding.

4. **Red flags that require discussion**:
   - Changing test assertions or expected values
   - Commenting out test code
   - Skipping tests with `@pytest.skip`
   - "Simplifying" tests that were testing real functionality

**Core Principle**: Tests are a specification of how code should behave. Changing a test to pass is like changing the requirements to match a bug. The only valid reasons to modify a test are:
- The requirement itself was wrong
- The test doesn't accurately represent the requirement

---

## Link Patterns

From within `skills/{product}/`:

| Target | Pattern |
|--------|---------|
| Same folder | `[file.md](file.md)` |
| Subcategory | `[category/file.md](category/file.md)` |
| Root formats | `[../../formats/fhir-r4.md](../../formats/fhir-r4.md)` |
| Root references | `[../../references/code-systems.md](../../references/code-systems.md)` |
| Hello examples | `[../../hello-healthsim/examples/quickstart.md](../../hello-healthsim/examples/quickstart.md)` |

---

## Key Reminders

- **FIRST: Read CURRENT-WORK.md** - Always check state before starting work
- **LAST: Update CURRENT-WORK.md** - Always update state before ending session
- **Single repo**: Clone `healthsim-workspace` to get everything
- **Follow existing patterns**: Review similar files before creating new ones
- **Cross-product integration**: Check for related skills in other products, add bidirectional references
- **Skills are flat**: Cohorts go directly in product folder, not nested
- **Formats are shared**: All formats in root `formats/`, never in product folders
- **Packages for Python**: Python infrastructure in `packages/`, not in `skills/`
- **Progressive disclosure**: Master skill routes to detailed skills
- **Extend, don't duplicate**: Reference canonical models
- **Commit frequently**: Don't batch all commits to session end
- **Test frequently**: Verify after each change
- **Document as you go**: CHANGELOG.md every session

---

*GitHub: https://github.com/mark64oswald/healthsim-workspace*
