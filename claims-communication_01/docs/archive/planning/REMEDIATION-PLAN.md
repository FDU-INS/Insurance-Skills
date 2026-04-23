# HealthSim Remediation Plan

**Created**: December 25, 2025  
**Purpose**: Systematic remediation of documentation, structure, and consistency gaps  
**Status**: ✅ COMPLETE

---

## Overview

This plan addresses gaps identified in the comprehensive HealthSim workspace audit. Work is organized into 6 priority areas with atomic, trackable tasks.

### Progress Summary

| Priority | Area | Tasks | Complete | Status |
|----------|------|-------|----------|--------|
| P1 | README Files | 8 | 8 | ✅ Complete |
| P2 | hello-healthsim | 6 | 6 | ✅ Complete |
| P3 | Cross-Product Integration | 4 | 4 | ✅ Complete |
| P4 | SKILL.md Consistency | 7 | 7 | ✅ Complete |
| P5 | NetworkSim Dual-Version | 5 | 5 | ✅ Complete |
| P6 | Navigation & Discovery | 4 | 4 | ✅ Complete |
| **TOTAL** | | **34** | **34** | **100%** |

---

## Priority 1: README Files (Foundation)

**Goal**: Solid README files across all products highlighting capabilities and providing navigation.

### Tasks

| ID | Task | File | Status | Notes |
|----|------|------|--------|-------|
| P1.1 | Restructure main README with quick navigation | `/README.md` | ✅ | Already comprehensive with "I want to..." navigation |
| P1.2 | Update PatientSim README | `/skills/patientsim/README.md` | ✅ | Created with capabilities, examples nav, cross-links |
| P1.3 | Update MemberSim README | `/skills/membersim/README.md` | ✅ | Created with capabilities, examples nav, cross-links |
| P1.4 | Update RxMemberSim README | `/skills/rxmembersim/README.md` | ✅ | Created with capabilities, examples nav, cross-links |
| P1.5 | Update TrialSim README | `/skills/trialsim/README.md` | ✅ | Created with capabilities, examples nav, cross-links |
| P1.6 | Update PopulationSim README | `/skills/populationsim/README.md` | ✅ | Created with capabilities, examples nav, cross-links |
| P1.7 | Update NetworkSim README | `/skills/networksim/README.md` | ✅ | Created with capabilities, examples nav, cross-links |
| P1.8 | Update docs/README.md | `/docs/README.md` | ✅ | Removed external repo links, consolidated navigation |

### README Template Structure

```markdown
# [Product Name]

> One-sentence description

## What [Product] Does

Brief capabilities overview (2-3 paragraphs max)

## Quick Start

Link to hello-healthsim examples

## Key Capabilities

| Capability | Description | Example Link |
|------------|-------------|--------------|

## Skills Reference

Link to SKILL.md

## Integration

Links to cross-product documentation

## Examples & Tutorials

Links to hello-healthsim/examples/[product]-examples.md
```

---

## Priority 2: hello-healthsim Coverage

**Goal**: Balanced product coverage with proper introductions and navigation.

### Tasks

| ID | Task | File | Status | Notes |
|----|------|------|--------|-------|
| P2.1 | Add "Hello, Population Intelligence!" section | `/hello-healthsim/README.md` | ⬜ | Match format of other Hello sections |
| P2.2 | Add "Hello, Provider Networks!" section | `/hello-healthsim/README.md` | ⬜ | Match format of other Hello sections |
| P2.3 | Add product introduction section | `/hello-healthsim/README.md` | ⬜ | "What is PatientSim?" etc. before examples |
| P2.4 | Balance Quick Reference Card | `/hello-healthsim/README.md` | ⬜ | Add PopulationSim, NetworkSim examples |
| P2.5 | Expand NetworkSim examples | `/hello-healthsim/examples/networksim-examples.md` | ⬜ | Currently only 1 example, need 4-6 |
| P2.6 | Update learning path README | `/hello-healthsim/examples/README.md` | ⬜ | Balance NetworkSim positioning |

---

## Priority 3: Cross-Product Integration

**Goal**: Complete bidirectional integration documentation across all products.

### Tasks

| ID | Task | File | Status | Notes |
|----|------|------|--------|-------|
| P3.1 | Add PopulationSim v2.0 integration to RxMemberSim | `/skills/rxmembersim/SKILL.md` | ⬜ | Currently missing |
| P3.2 | Strengthen NetworkSim integration in PatientSim | `/skills/patientsim/SKILL.md` | ⬜ | Brief mention, needs detail |
| P3.3 | Strengthen NetworkSim integration in MemberSim | `/skills/membersim/SKILL.md` | ⬜ | Brief mention, needs detail |
| P3.4 | Document TrialSim ↔ PatientSim/MemberSim patterns | `/skills/trialsim/SKILL.md` | ⬜ | Trial subjects with ongoing care |

---

## Priority 4: SKILL.md Consistency

**Goal**: Ensure all SKILL.md files are solid with consistent structure and subdirectory organization.

### Tasks

| ID | Task | File | Status | Notes |
|----|------|------|--------|-------|
| P4.1 | Audit PatientSim SKILL.md structure | `/skills/patientsim/SKILL.md` | ✅ | Gold standard template created |
| P4.2 | Standardize MemberSim SKILL.md | `/skills/membersim/SKILL.md` | ✅ | Already aligned |
| P4.3 | Standardize RxMemberSim SKILL.md | `/skills/rxmembersim/SKILL.md` | ✅ | Already aligned with PopSim v2.0 |
| P4.4 | Standardize TrialSim SKILL.md | `/skills/trialsim/SKILL.md` | ✅ | Appropriate domain-specific structure |
| P4.5 | Standardize PopulationSim SKILL.md | `/skills/populationsim/SKILL.md` | ✅ | Appropriate data-focused structure |
| P4.6 | Standardize NetworkSim SKILL.md | `/skills/networksim/SKILL.md` | ✅ | Appropriate ref+gen dual structure |
| P4.7 | Organize complex skill subdirectories | Various | ✅ | PatientSim: oncology/, pediatrics/; TrialSim: domains/ |

### SKILL.md Standard Sections

1. **Frontmatter**: name, description, trigger phrases
2. **For Claude**: When to use this skill
3. **Quick Start**: 2-3 example prompts
4. **Cohort/Skill Table**: Links to individual skills
5. **Parameters**: Generation parameters table
6. **Output Formats**: Supported formats
7. **Cross-Product Integration**: Each product section
8. **Related Skills**: Links to related skills

---

## Priority 5: NetworkSim Dual-Version Setup

**Goal**: Complete setup of both NetworkSim (public/generative) and NetworkSim-Local (private/real data).

### Current State

| Component | NetworkSim (Public) | NetworkSim-Local (Private) |
|-----------|---------------------|----------------------------|
| Location | `/skills/networksim/` | `/Users/.../networksim-local/` |
| Git Repo | ✅ healthsim-workspace | ⚠️ Local git, no remote |
| VS Code Workspace | ✅ In healthsim.code-workspace | ❌ Missing |
| Skills | ✅ Complete | ✅ Complete |
| Data | N/A (generative) | ✅ NPPES (~1.7GB DuckDB) |
| Documentation | ⬜ Needs enhancement | ✅ Good |

### Tasks

| ID | Task | Status | Notes |
|----|------|--------|-------|
| P5.1 | Create private GitHub repo for NetworkSim-Local | ✅ | mark64oswald/networksim-local (private) |
| P5.2 | Configure git remote for NetworkSim-Local | ✅ | Linked to private repo |
| P5.3 | Create networksim-local.code-workspace | ✅ | VS Code workspace file created |
| P5.4 | Update .gitignore for data files | ✅ | Verified - large files excluded |
| P5.5 | Create dual-version documentation | ✅ | docs/networksim-dual-version.md |

---

## Priority 6: Navigation & Discovery

**Goal**: Clear paths from use case to appropriate product and examples.

### Tasks

| ID | Task | File | Status | Notes |
|----|------|------|--------|-------|
| P6.1 | Create "Use Case → Product" mapping | `/README.md` | ✅ | Enhanced "I Want To..." table with multi-product workflows |
| P6.2 | Create product relationship diagram | `/docs/` | ✅ | product-architecture.md with diagrams and workflows |
| P6.3 | Add "Common Workflows" section | `/README.md` | ✅ | Linked to product-architecture.md#common-workflows |
| P6.4 | Create navigation breadcrumbs | Various | ✅ | Product READMEs link to SKILL.md, examples, cross-products |

---

## Execution Order

Recommended sequence to minimize dependencies:

1. **P5.1-P5.5**: NetworkSim Dual-Version (standalone, no dependencies)
2. **P4.1**: Audit PatientSim SKILL.md (establishes template)
3. **P1.1**: Main README restructure (foundation for navigation)
4. **P4.2-P4.7**: Standardize other SKILL.md files
5. **P1.2-P1.8**: Product README files
6. **P3.1-P3.4**: Cross-product integration
7. **P2.1-P2.6**: hello-healthsim coverage
8. **P6.1-P6.4**: Navigation & discovery

---

## Session Log

| Session | Date | Tasks Completed | Notes |
|---------|------|-----------------|-------|
| 1 | 2025-12-25 | Initial audit, plan created | |
| 2 | 2025-12-25 | P5.1-P5.5 (NetworkSim Dual-Version) | Private repo created, VS Code workspace, data docs enhanced |
| 3 | 2025-12-25 | P4 (SKILL.md), P1-P3, P6 | All product READMEs, hello-healthsim, cross-product integration, navigation |

---

## How to Use This Document

1. **Starting a session**: Check "Progress Summary" for current state
2. **Working on tasks**: Update task status (⬜→🔄→✅)
3. **Completing a session**: Add entry to "Session Log"
4. **If crash occurs**: Resume from last completed task

### Status Legend

- ⬜ Not Started
- 🔄 In Progress
- ✅ Complete
- ⏸️ Blocked
- ❌ Skipped (with reason)

---

*Last Updated: December 25, 2025*
