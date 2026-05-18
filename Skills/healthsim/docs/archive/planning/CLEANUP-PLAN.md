# Development Artifacts Cleanup Plan

**Created**: December 25, 2025  
**Purpose**: Organize development/planning documents into archive folder without breaking any links

---

## Summary

After comprehensive link analysis, I've identified **27 files/folders** that are development artifacts (planning docs, prompts, audits) and are NOT referenced from any core documentation or skill files.

---

## Proposed Structure

```
docs/
├── archive/                    # NEW: Development history (not linked)
│   ├── planning/               # Project planning documents
│   ├── prompts/                # Super-prompts and session prompts
│   ├── audits/                 # Audits and assessments
│   ├── migration/              # Migration plans and guides
│   └── drafts/                 # Move existing drafts/ here
│
├── README.md                   # KEEP: Doc hub (linked)
├── HEALTHSIM-ARCHITECTURE-GUIDE.md  # KEEP: Heavily linked
├── HEALTHSIM-DEVELOPMENT-PROCESS.md # KEEP: Linked from contributing
├── product-architecture.md     # KEEP: Linked from README
├── networksim-dual-version.md  # KEEP: Linked from NetworkSim
├── skills-template.md          # KEEP: Linked from docs/README
├── contributing.md             # KEEP: Linked
├── integration-guide.md        # KEEP: Linked from hello-healthsim
├── testing-patterns.md         # KEEP: Linked from SKILL.md
├── architecture/               # KEEP: Linked from contributing
├── extensions/                 # KEEP: Linked from contributing
├── mcp/                        # KEEP: Linked from extensions
├── skills/                     # KEEP: format-specification linked
└── state-management/           # KEEP: May be linked
```

---

## Files to Move → docs/archive/

### Root Level (→ archive/)

| File | Current | Destination | Type |
|------|---------|-------------|------|
| `CLAUDE-CODE-CONTEXT.md` | root | archive/prompts/ | Session context |
| `CURRENT-WORK.md` | root | archive/ | Session tracking |

### Planning Documents (→ archive/planning/)

| File | Current | Verified Not Linked |
|------|---------|---------------------|
| `HEALTHSIM-PROJECT-INSTRUCTIONS.md` | docs/ | ✅ |
| `CROSS-PRODUCT-INTEGRATION-GAPS.md` | docs/ | ✅ |
| `REMEDIATION-PLAN.md` | docs/ | ✅ |
| `healthsim-migration-plan.md` | docs/ | ✅ |
| `healthsim-workspace-architecture.md` | docs/ | ✅ |

### Product Development Plans (→ archive/planning/)

| File | Current | Verified Not Linked |
|------|---------|---------------------|
| `TRIALSIM-DEVELOPMENT-PLAN.md` | docs/ | ✅ |
| `TRIALSIM-DATA-MODEL-DESIGN.md` | docs/ | ✅ |
| `TRIALSIM-DEVELOPER-GUIDE.md` | docs/ | ✅ |
| `POPULATIONSIM-DATA-ARCHITECTURE.md` | docs/ | ✅ |
| `POPULATIONSIM-DATA-PACKAGE-OVERVIEW.md` | docs/ | ✅ |
| `docs/networksim/` | docs/networksim/ | ✅ (entire folder) |
| `docs/initiatives/` | docs/initiatives/ | ✅ (entire folder) |

### Prompts (→ archive/prompts/)

| File | Current | Verified Not Linked |
|------|---------|---------------------|
| `PATIENTSIM-SESSION5-SUPERPROMPT.md` | docs/ | ✅ |
| `POPULATIONSIM-PHASE2-SUPERPROMPT.md` | docs/ | ✅ |
| `POPULATIONSIM-SESSIONS-5-8-SUPERPROMPT.md` | docs/ | ✅ |
| `TRIALSIM-PROMPT-GUIDE.md` | docs/ | ✅ |

### Audits/Assessments (→ archive/audits/)

| File | Current | Verified Not Linked |
|------|---------|---------------------|
| `POPULATIONSIM-V2-COMPREHENSIVE-AUDIT.md` | docs/ | ✅ |
| `POPULATIONSIM-V2-HONEST-ASSESSMENT.md` | docs/ | ✅ |
| `POPULATIONSIM-V2-ROADMAP-AUDIT.md` | docs/ | ✅ |

### Legacy/Superseded (→ archive/migration/)

| File | Current | Verified Not Linked |
|------|---------|---------------------|
| `healthsim-master-SKILL.md` | docs/ | ✅ (superseded by root SKILL.md) |
| `healthsim-feature-comparison.md` | docs/ | ✅ |
| `healthsim-domain-knowledge-base.md` | docs/ | ✅ |

### Drafts (Move existing folder)

| Folder | Current | Verified Not Linked |
|--------|---------|---------------------|
| `docs/drafts/` | docs/drafts/ | ✅ (entire folder) |

---

## Files Staying in Place (Linked from Core Docs)

| File | Linked From |
|------|-------------|
| `docs/README.md` | Navigation hub |
| `docs/HEALTHSIM-ARCHITECTURE-GUIDE.md` | README, product READMEs, SKILL.md |
| `docs/HEALTHSIM-DEVELOPMENT-PROCESS.md` | contributing.md |
| `docs/product-architecture.md` | README "I Want To..." |
| `docs/networksim-dual-version.md` | skills/networksim/README.md |
| `docs/skills-template.md` | docs/README.md |
| `docs/contributing.md` | docs/README.md |
| `docs/integration-guide.md` | hello-healthsim/README.md, SKILL.md |
| `docs/testing-patterns.md` | SKILL.md |
| `docs/architecture/` | contributing.md, extensions/ |
| `docs/extensions/` | contributing.md |
| `docs/mcp/` | extensions/ |
| `docs/skills/format-specification-v2.md` | docs/README.md |
| `docs/skills/creating-skills.md` | contributing.md |
| `docs/state-management/` | Need to verify, keeping for safety |

---

## Verification Steps Before Moving

For each file to be moved:
1. ✅ Search for filename in all .md files
2. ✅ Search for partial path matches
3. ✅ Confirm 0 results from core documentation

---

## Archive README

Create `docs/archive/README.md`:

```markdown
# Development Archive

Historical documentation from HealthSim development. These documents are preserved 
for reference but are not part of active product documentation.

## Contents

- **planning/**: Project plans, roadmaps, architecture decisions
- **prompts/**: Super-prompts and session prompts used during development
- **audits/**: Quality audits and assessments
- **migration/**: Migration guides and legacy documents
- **drafts/**: Work-in-progress documents

## Note

Files in this folder are not linked from product documentation. They document the 
development process and may be useful for understanding design decisions or 
continuing future development.

For current documentation, see [docs/README.md](../README.md).
```

---

## Execution Plan

### Phase 1: Create Structure
```bash
mkdir -p docs/archive/{planning,prompts,audits,migration}
```

### Phase 2: Move Files (in order, with verification)
1. Root level files → archive/
2. Planning documents → archive/planning/
3. Prompts → archive/prompts/
4. Audits → archive/audits/
5. Legacy → archive/migration/
6. Move existing drafts/ → archive/drafts/
7. Move networksim/ → archive/planning/networksim/
8. Move initiatives/ → archive/planning/initiatives/

### Phase 3: Verify
```bash
# Check for any broken links
grep -r "archive/" docs/ skills/ hello-healthsim/ README.md SKILL.md
# Should return 0 results (nothing should link to archive)
```

### Phase 4: Commit
```bash
git add -A
git commit -m "[Docs] Archive development artifacts to docs/archive/

Moved planning, prompts, audits, and legacy documents to archive folder.
Core documentation remains in place with all links preserved."
```

---

## Risk Mitigation

1. **Before moving**: Double-check each file with `grep -r "filename" .`
2. **Test after**: Verify no broken links in docs/README.md navigation
3. **Reversible**: If any issues found, `git restore` can undo

---

**Ready to execute?** Confirm and I'll proceed with the moves.
