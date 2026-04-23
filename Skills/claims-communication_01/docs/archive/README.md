# Development Archive

Historical documentation from HealthSim development. These documents are preserved for reference but are not part of active product documentation.

> ⚠️ **Note on Links**: Documents in this archive may contain broken links to files that have been moved, renamed, or removed during development. These links are preserved as historical artifacts and are not maintained. For current documentation, see the links at the bottom of this page.

---

## Contents

| Folder | Description |
|--------|-------------|
| **planning/** | Project plans, roadmaps, architecture decisions, product development plans |
| **prompts/** | Super-prompts and session prompts used during development |
| **audits/** | Quality audits, assessments, and roadmap reviews |
| **migration/** | Migration guides and superseded documents |
| **drafts/** | Work-in-progress documents |
| **session/** | Session context and work tracking files |
| **architecture/** | Historical architecture documents |
| **initiatives/** | Completed development initiatives |

---

## Recently Archived (December 2024)

### DuckDB Architecture Initiative (Completed)
**Location**: `initiatives/duckdb-architecture-completed/`

The DuckDB Unified Data Architecture initiative is complete. All 7 sessions were executed successfully:
- 41-table canonical schema across 6 products
- State management with DuckDB backend
- JSON compatibility layer
- Migration tools
- 605 tests passing

These planning documents are preserved for historical reference.

### State Management v1 Documentation (Superseded)
**Location**: `migration/state-management-*-v1.md`

The original state management specification and user guide have been superseded by:
- **Authoritative Skill**: `skills/common/state-management.md` (v4.0)
- **Examples**: `hello-healthsim/examples/auto-persist-examples.md` (v2.0)

The Skill now includes Phase 2 features (tags, cloning, merging, multi-format export) that were not in the original v1 docs.

### Auto-Persist Architecture v1 (Superseded)
**Location**: `architecture/healthsim-auto-persist-architecture-v1.html`

The original auto-persist design document. Implementation is complete and documented in the state-management skill.

---

## Folder Details

### planning/
- Project-level planning (remediation, migration, instructions)
- Product development plans (TrialSim, PopulationSim, NetworkSim)
- Architecture decisions and workspace structure

### prompts/
- Super-prompts for Claude Code sessions
- Prompt guides for product development
- Session-specific prompts

### audits/
- PopulationSim v2.0 comprehensive audits
- Roadmap audits and honest assessments
- Gap analyses

### migration/
- Legacy SKILL.md files (superseded by root SKILL.md)
- Feature comparisons
- Domain knowledge base (now embedded in skills)
- State management v1 docs (superseded by skill v4.0)

### drafts/
- TrialSim canonical models draft
- TrialSim dimensional analytics draft

### session/
- Claude Code context files
- Current work tracking

### architecture/
- Historical architecture documents
- Superseded design specs

### initiatives/
- Completed development initiatives with planning docs

---

## Current Documentation

For up-to-date documentation, see:

| Topic | Location |
|-------|----------|
| State Management | `skills/common/state-management.md` |
| Auto-Persist Examples | `hello-healthsim/examples/auto-persist-examples.md` |
| DuckDB Schema | `docs/healthsim-duckdb-schema.md` |
| Product Skills | `skills/{product}/SKILL.md` |
| Getting Started | `hello-healthsim/README.md` |

