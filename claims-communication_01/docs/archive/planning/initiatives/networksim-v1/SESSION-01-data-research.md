# NetworkSim Session 01: Data Source Research

**Phase**: 1 - Data Package  
**Goal**: Evaluate data sources and define filtering strategy  
**Estimated Duration**: 1 session  
**Prerequisites**: None

---

## Pre-Flight Checklist

- [ ] Read `CURRENT-WORK.md` - verify clean state
- [ ] Confirm git status is clean
- [ ] Review this session prompt completely before starting

---

## Context

Before downloading large data files, we need to:
1. Understand what's available in NPPES and CMS data
2. Define which fields we actually need
3. Plan filtering strategy to reduce 8GB → ~500MB
4. Identify any licensing/usage restrictions

---

## Deliverables

### 1. Data Source Analysis Document
**File**: `docs/initiatives/networksim-v1/DATA-SOURCE-ANALYSIS.md`

Research and document:
- NPPES NPI file structure (columns, data types)
- CMS Provider of Services file structure
- Which fields are essential vs. nice-to-have
- Data quality observations
- Licensing/usage notes

### 2. Filtering Strategy Document
**File**: `docs/initiatives/networksim-v1/FILTERING-STRATEGY.md`

Define:
- Which provider types to include (individual, organization)
- Which entity types to include (NPI-1, NPI-2)
- Geographic scope (all US, or subset)
- Active vs. deactivated providers
- Fields to retain vs. drop
- Estimated final dataset size

### 3. Download Scripts (Draft)
**File**: `scripts/networksim/download-nppes.sh` (draft, not executed yet)

Prepare download commands for next session.

---

## Steps

### Step 1: Research NPPES Structure
1. Visit https://download.cms.gov/nppes/NPI_Files.html
2. Download the data dictionary (PDF or readme)
3. Document key columns in DATA-SOURCE-ANALYSIS.md

### Step 2: Research CMS Provider Files
1. Visit https://data.cms.gov/provider-data/
2. Identify relevant datasets (Hospital General Info, etc.)
3. Document structure in DATA-SOURCE-ANALYSIS.md

### Step 3: Define Filtering Strategy
1. List must-have fields (NPI, name, taxonomy, address, status)
2. List optional fields (phone, credentials, etc.)
3. Define inclusion criteria (active, US-based, etc.)
4. Estimate filtered size
5. Document in FILTERING-STRATEGY.md

### Step 4: Verify & Commit
1. Review both documents for completeness
2. Commit: `[NetworkSim] Session 01 - Data source analysis and filtering strategy`
3. Update CURRENT-WORK.md

---

## Post-Flight Checklist

- [ ] DATA-SOURCE-ANALYSIS.md created with NPPES and CMS structures
- [ ] FILTERING-STRATEGY.md created with field list and inclusion criteria
- [ ] Download script drafted (not executed)
- [ ] Committed with descriptive message
- [ ] CURRENT-WORK.md updated with:
  - Session 01 marked complete
  - Session 02 as next
  - Any notes/decisions made
- [ ] Pushed to remote

---

## Success Criteria

- [ ] Clear understanding of NPPES data structure
- [ ] Filtering strategy will reduce data to manageable size (~500MB)
- [ ] No licensing issues identified (or issues documented with mitigation)
- [ ] Ready to proceed with data download in Session 02

---

## Next Session

Session 02 will execute the download and filtering strategy defined here.
