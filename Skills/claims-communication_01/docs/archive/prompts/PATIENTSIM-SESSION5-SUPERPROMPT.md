# PopulationSim v2.0 Session 5: PatientSim Integration

**Purpose**: Update PatientSim skills to use real population data from PopulationSim embedded data package for data-driven patient generation.

**Date**: 2024-12-23
**Prerequisites**: Sessions 1-4 complete (PopulationSim data package + skills + canonical model)

---

## Pre-Flight Checklist

- [ ] Verify PopulationSim data package exists: `skills/populationsim/data/` (9 files, ~148 MB)
- [ ] Verify PopulationSim canonical model v2.0: `skills/populationsim/models/population-profile-schema.md`
- [ ] Review existing integration doc: `skills/populationsim/integration/patientsim-integration.md`
- [ ] Review diabetes-management.md as pattern (already has partial v2.0 integration)
- [ ] Note current PatientSim skill count: 17 skills (SKILL.md + 16 cohorts)

---

## Phase 5A: Foundation Updates

### Task 5A.1: Update PatientSim SKILL.md

Add new section "Data Integration (PopulationSim v2.0)" after "Output Formats":

```markdown
## Data Integration (PopulationSim v2.0)

PatientSim integrates with PopulationSim's embedded data package to generate patients grounded in real demographic and health data.

### Enabling Data-Driven Generation

Add a `geography` parameter to any request:

| Parameter | Type | Example | Description |
|-----------|------|---------|-------------|
| geography | string | "48201" | County FIPS code |
| geography | string | "48201002300" | Census tract FIPS code |

### What Data-Driven Generation Provides

1. **Demographics**: Age, sex, race/ethnicity distributions match real population
2. **Condition Prevalence**: Diabetes, obesity, hypertension rates from CDC PLACES
3. **SDOH Context**: SVI vulnerability scores affect adherence, outcomes
4. **Insurance Mix**: Coverage types reflect actual area coverage

### Data Sources

| Source | File | Use |
|--------|------|-----|
| CDC PLACES 2024 | `populationsim/data/county/places_county_2024.csv` | Health indicators |
| CDC SVI 2022 | `populationsim/data/county/svi_county_2022.csv` | Vulnerability indices |
| ADI 2023 | `populationsim/data/block_group/adi_blockgroup_2023.csv` | Deprivation index |

See [PopulationSim → PatientSim Integration](../populationsim/integration/patientsim-integration.md) for complete mapping.
```

### Task 5A.2: Update Integration Document with v2.0 Provenance

Update `skills/populationsim/integration/patientsim-integration.md`:

1. Add version header: "Updated for PopulationSim v2.0 Embedded Data"
2. Add "Embedded Data File References" section with exact file paths
3. Add "Provenance Tracking" section showing how provenance flows to PatientSim output
4. Add example with `data_provenance` in metadata

### Task 5A.3: Create PatientSim Data Integration Skill

Create new file `skills/patientsim/data-integration.md`:

```yaml
---
name: patientsim-data-integration
description: |
  Foundation skill for data-driven patient generation using PopulationSim v2.0 
  embedded data. Provides lookup patterns, provenance tracking, and SDOH integration.
---
```

Content should include:
- Overview of data-driven generation
- Embedded data file locations and column names
- Lookup patterns for county and tract data
- SDOH-to-outcome correlations
- Provenance output format
- Examples at county and tract level

---

## Phase 5B: Clinical Cohort Updates

Update each clinical cohort skill with "Data Sources (PopulationSim v2.0)" section following the pattern in diabetes-management.md.

### Skills to Update

| Skill | Primary PLACES Measures | SVI/ADI Impact |
|-------|------------------------|----------------|
| heart-failure.md | CHD, BPHIGH, KIDNEY | Medication adherence |
| chronic-kidney-disease.md | KIDNEY, DIABETES, BPHIGH | Progression rate |
| behavioral-health.md | DEPRESSION, MHLTH | Treatment access |
| sepsis-acute-care.md | ACCESS2 (uninsured) | ED presentation |
| maternal-health.md | DIABETES (GDM proxy), ACCESS2 | Prenatal access |
| ed-chest-pain.md | CHD, STROKE | Presentation acuity |
| elective-joint.md | ARTHRITIS, OBESITY | Surgical candidacy |
| oncology/breast-cancer.md | MAMMOGRAPHY (screening) | Stage at diagnosis |
| oncology/lung-cancer.md | CSMOKING, COPD | Risk factors |
| oncology/colorectal-cancer.md | COLON_SCREEN | Stage at diagnosis |
| pediatrics/childhood-asthma.md | CASTHMA | Environmental factors |
| pediatrics/acute-otitis-media.md | CHECKUP (access) | Treatment patterns |

### Standard Section Template

For each skill, add after Parameters table:

```markdown
## Data Sources (PopulationSim v2.0)

When a geography is specified, [CONDITION] cohorts are grounded in real CDC PLACES data:

### Embedded Data Lookup

**County-Level Data:**
```
File: skills/populationsim/data/county/places_county_2024.csv
Columns:
  - [PRIMARY_MEASURE]_CrudePrev: Crude prevalence (%)
  - [PRIMARY_MEASURE]_AdjPrev: Age-adjusted prevalence (%)
  - [COMORBIDITY]_CrudePrev: Comorbidity rate
```

### Data-Driven Rates

| Parameter | Generic Default | Data-Driven Source |
|-----------|-----------------|-------------------|
| [condition_rate] | [X]% | [MEASURE]_CrudePrev from PLACES |
| [comorbidity] | [Y]% | [COMORBID_MEASURE]_CrudePrev |

### SDOH Context

```
File: skills/populationsim/data/county/svi_county_2022.csv
Impact on [CONDITION]:
  - RPL_THEMES (vulnerability): Affects [outcome]
  - EP_UNINSUR (uninsured): Affects [outcome]
```
```

---

## Phase 5C: Audit & Testing

### Audit Checklist

After completing 5A and 5B, verify:

- [ ] PatientSim SKILL.md has "Data Integration (PopulationSim v2.0)" section
- [ ] Integration document updated with v2.0 provenance
- [ ] data-integration.md skill created
- [ ] All 12 clinical cohort skills have "Data Sources" section
- [ ] All file paths reference correct embedded data locations
- [ ] All PLACES measure names match actual column names

### Smoke Tests

Run existing smoke test:
```bash
cd /Users/markoswald/Developer/projects/healthsim-workspace
python scripts/smoke_test.py
```

Expected: All tests pass (no regressions)

### Manual Verification Tests

Test each updated skill with sample prompts:

**Test 1: County-level diabetes patient**
```
Generate a diabetic patient in Harris County, TX (FIPS 48201)
```
Verify: Output includes provenance referencing places_county_2024.csv

**Test 2: Tract-level heart failure patient**
```
Generate a heart failure patient in census tract 48201002300
```
Verify: Comorbidity rates reflect tract-level PLACES data

**Test 3: SDOH impact on behavioral health**
```
Generate a depression patient in a high-vulnerability area (SVI > 0.8)
```
Verify: Treatment barriers reflected based on SVI theme scores

**Test 4: Cross-cohort consistency**
```
Generate a patient with diabetes AND heart failure in Maricopa County, AZ
```
Verify: Both conditions use consistent geography data

**Test 5: Provenance in output**
```
Generate a patient with full provenance tracking
```
Verify: metadata.data_provenance populated with source, data_year, file_reference

---

## Phase 5D: Documentation & Commit

### Documentation Updates

1. **Update CHANGELOG.md** with Session 5 changes
2. **Update hello-healthsim** with data-driven example
3. **Update POPULATIONSIM-V2-ROADMAP-AUDIT.md** with Session 5 completion

### CHANGELOG Entry

```markdown
- **[PatientSim]** PopulationSim v2.0 Data Integration (2024-12-23)
  - Added "Data Integration (PopulationSim v2.0)" section to SKILL.md
  - Created `data-integration.md` foundation skill
  - Updated integration document with embedded data provenance
  - Added "Data Sources" sections to 12 clinical cohort skills:
    - heart-failure.md, chronic-kidney-disease.md, behavioral-health.md
    - sepsis-acute-care.md, maternal-health.md, ed-chest-pain.md
    - elective-joint.md, oncology/*.md (3), pediatrics/*.md (2)
  - All skills now support geography parameter for data-driven generation
  - Provenance tracking flows from PopulationSim to PatientSim output
```

### Git Operations

```bash
git add -A
git status  # Verify expected files
git commit -m "[PatientSim] Add PopulationSim v2.0 data integration

- Added Data Integration section to SKILL.md
- Created data-integration.md foundation skill
- Updated integration document with v2.0 provenance
- Added Data Sources sections to 12 clinical cohort skills
- All skills support geography parameter for data-driven generation"
git push origin main
```

---

## Post-Flight Checklist

- [ ] PatientSim SKILL.md updated
- [ ] data-integration.md created
- [ ] Integration document updated
- [ ] 12 clinical cohort skills updated
- [ ] Smoke tests pass
- [ ] Manual verification tests pass
- [ ] CHANGELOG.md updated
- [ ] hello-healthsim example added (optional)
- [ ] Git committed and pushed
- [ ] POPULATIONSIM-V2-ROADMAP-AUDIT.md updated

---

## Success Criteria

1. **Completeness**: All 12 clinical cohort skills have "Data Sources (PopulationSim v2.0)" section
2. **Consistency**: All skills use same pattern and reference correct file paths
3. **Testing**: Smoke tests pass, manual tests verify data-driven generation works
4. **Documentation**: CHANGELOG updated, integration doc updated
5. **No Regressions**: Existing PatientSim functionality unchanged

---

## Files Modified (Expected)

| File | Change |
|------|--------|
| skills/patientsim/SKILL.md | Add data integration section |
| skills/patientsim/data-integration.md | NEW |
| skills/populationsim/integration/patientsim-integration.md | Update for v2.0 |
| skills/patientsim/heart-failure.md | Add data sources section |
| skills/patientsim/chronic-kidney-disease.md | Add data sources section |
| skills/patientsim/behavioral-health.md | Add data sources section |
| skills/patientsim/sepsis-acute-care.md | Add data sources section |
| skills/patientsim/maternal-health.md | Add data sources section |
| skills/patientsim/ed-chest-pain.md | Add data sources section |
| skills/patientsim/elective-joint.md | Add data sources section |
| skills/patientsim/oncology/breast-cancer.md | Add data sources section |
| skills/patientsim/oncology/lung-cancer.md | Add data sources section |
| skills/patientsim/oncology/colorectal-cancer.md | Add data sources section |
| skills/patientsim/pediatrics/childhood-asthma.md | Add data sources section |
| skills/patientsim/pediatrics/acute-otitis-media.md | Add data sources section |
| CHANGELOG.md | Add Session 5 entry |
