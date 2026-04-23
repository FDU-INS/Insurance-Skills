# PopulationSim Embedded Data Package

## Executive Summary

PopulationSim v2.0 introduces an **Embedded Data Package**—a curated collection of authoritative public health and demographic datasets covering 100% of US geography. This transforms PopulationSim from a synthesis-first system to a **real-data-first** platform, with transparent synthesis only for data that cannot be directly observed.

### The Fundamental Shift

| Aspect | v1.0 (Current) | v2.0 (With Data Package) |
|--------|----------------|--------------------------|
| **Data source** | Claude's domain knowledge | Real embedded datasets |
| **Accuracy** | Plausible (~70-80%) | Exact (100%) for embedded data |
| **Coverage** | Unlimited but approximate | 100% US, precise values |
| **Transparency** | Implicit synthesis | Explicit data provenance |
| **Confidence** | "This area likely has..." | "CDC reports 12.1% (PLACES 2024)" |

---

## Data Package Contents

### Complete Inventory

| Dataset | Source | Level | Records | Size | Update Cycle |
|---------|--------|-------|---------|------|--------------|
| ACS Demographics | Census Bureau | County | 3,143 | ~1.5 MB | Annual |
| ACS Demographics | Census Bureau | Tract | 85,000 | ~40 MB | Annual |
| PLACES Health Indicators | CDC | County | 3,143 | ~500 KB | Annual |
| PLACES Health Indicators | CDC | Tract | 85,000 | ~12 MB | Annual |
| Social Vulnerability Index | CDC/ATSDR | County | 3,143 | ~2 MB | Biennial |
| Social Vulnerability Index | CDC/ATSDR | Tract | 85,000 | ~50 MB | Biennial |
| Area Deprivation Index | UW-Madison | Block Group | 240,000 | ~25 MB | Annual |
| Geography Crosswalks | Census Bureau | Various | ~90,000 | ~2 MB | Decennial+ |
| **TOTAL** | | | **~508,000** | **~133 MB** | |

### Data Vintages (Initial Release)

| Dataset | Data Year | Release Year | Notes |
|---------|-----------|--------------|-------|
| ACS 5-Year | 2019-2023 | Dec 2024 | Most reliable for small areas |
| CDC PLACES | 2022 BRFSS | Aug 2024 | 40 health measures |
| CDC SVI | 2022 ACS | May 2024 | 16 vulnerability indicators |
| ADI | 2023 ACS | 2024 | Block group rankings |

---

## Dataset Details

### 1. American Community Survey (ACS) Demographics

**Source**: U.S. Census Bureau  
**License**: Public Domain

#### Variables Included (~50 per geography)

| Category | Key Variables | PopulationSim Use |
|----------|---------------|-------------------|
| **Population** | Total count, density | Base population sizing |
| **Age** | 18 brackets by sex | Age-appropriate condition modeling |
| **Sex** | Male/female distribution | Gender-specific health patterns |
| **Race** | 7 OMB categories | Diversity planning, health disparities |
| **Ethnicity** | Hispanic/Latino | Cultural health patterns |
| **Income** | Median household, per capita | Economic SDOH, plan eligibility |
| **Poverty** | % below 100%, 150%, 200% FPL | Medicaid eligibility, vulnerability |
| **Insurance** | Employer, Medicare, Medicaid, Uninsured | Coverage modeling |
| **Education** | Attainment levels | SDOH factor, health literacy proxy |
| **Employment** | Labor force participation, unemployment | Economic stability |
| **Housing** | Tenure, value, rent burden | Housing security SDOH |
| **Transportation** | Vehicle access, commute patterns | Healthcare access proxy |
| **Language** | English proficiency, languages spoken | Care delivery considerations |
| **Disability** | Functional limitation types | Special population identification |

### 2. CDC PLACES Health Indicators

**Source**: Centers for Disease Control and Prevention  
**License**: Public Domain

#### All 40 Measures

**Health Outcomes (12)**
| Measure | Definition | National Rate |
|---------|------------|---------------|
| ARTHRITIS | Adults with arthritis | 24.2% |
| BPHIGH | Adults with high blood pressure | 32.4% |
| CANCER | Adults ever told they had cancer | 6.9% |
| CASTHMA | Adults with current asthma | 9.8% |
| CHD | Coronary heart disease | 5.8% |
| COPD | Chronic obstructive pulmonary disease | 6.6% |
| DEPRESSION | Adults with depression | 18.6% |
| DIABETES | Adults with diabetes | 10.1% |
| HIGHCHOL | Adults with high cholesterol | 29.8% |
| KIDNEY | Chronic kidney disease | 3.2% |
| OBESITY | Adults with BMI ≥30 | 32.1% |
| STROKE | Adults who had a stroke | 3.4% |

**Prevention (7)**
| Measure | Definition | National Rate |
|---------|------------|---------------|
| BPMED | Taking BP medication | 78.4% |
| CERVICAL | Cervical cancer screening | 83.2% |
| CHECKUP | Annual checkup | 77.8% |
| CHOLSCREEN | Cholesterol screening | 88.4% |
| COLON_SCREEN | Colorectal cancer screening | 72.8% |
| DENTAL | Dental visit past year | 66.8% |
| MAMMOUSE | Mammography | 78.2% |

**Health Risk Behaviors (4)**
| Measure | Definition | National Rate |
|---------|------------|---------------|
| BINGE | Binge drinking | 16.8% |
| CSMOKING | Current smoking | 13.4% |
| LPA | Physical inactivity | 25.2% |
| SLEEP | Short sleep (<7 hours) | 34.8% |

**Disabilities (7)**
- Hearing, Vision, Cognitive, Mobility, Self-care, Independent living, Any disability

**Health Status (3)**
- General health (fair/poor), Mental health days, Physical health days

**Health-Related Social Needs (7)**
- Food insecurity, Housing insecurity, Utility needs, Transportation needs, etc.

### 3. CDC/ATSDR Social Vulnerability Index (SVI)

**Source**: CDC Agency for Toxic Substances and Disease Registry  
**License**: Public Domain

#### Four Themes, 16 Variables

| Theme | Variables | Weight |
|-------|-----------|--------|
| **Socioeconomic Status** | Below 150% poverty, Unemployed, Housing cost burden, No HS diploma, No health insurance | 25% |
| **Household Characteristics** | Age 65+, Age 17 and under, Civilian with disability, Single-parent households, English proficiency | 25% |
| **Racial & Ethnic Minority Status** | Hispanic/Latino, Black, Asian, AIAN, NHPI, Other race, Multiple races | 25% |
| **Housing Type & Transportation** | Multi-unit structures, Mobile homes, Crowding, No vehicle, Group quarters | 25% |

#### Output Fields
- Overall SVI percentile (0-1)
- Theme-specific percentiles (4)
- Raw estimates for each variable
- Margins of error

### 4. Area Deprivation Index (ADI)

**Source**: University of Wisconsin-Madison, Center for Health Disparities Research  
**License**: Free for research/non-commercial (registration required)

#### What's Included

| Field | Range | Description |
|-------|-------|-------------|
| National Percentile | 1-100 | Ranking vs. all US block groups |
| State Decile | 1-10 | Ranking vs. block groups in same state |

#### The 17 Underlying Variables (methodology reference)

| Domain | Variables |
|--------|-----------|
| **Income** | Median family income, Income disparity, % below poverty, % below 150% poverty |
| **Education** | % <9 years education, % <12 years education |
| **Employment** | % white-collar occupation |
| **Housing** | Median home value, Median rent, Median mortgage, % owner-occupied, % no plumbing, % no telephone, % crowded, % single-parent with children |

### 5. Geography Crosswalks

| File | Purpose | Records |
|------|---------|---------|
| fips_state.csv | State codes and names | 56 |
| fips_county.csv | County codes, names, states | 3,143 |
| tract_to_county.csv | Tract → County mapping | 85,000 |
| block_group_to_tract.csv | Block group → Tract mapping | 240,000 |
| cbsa_definitions.csv | Metro/micro area composition | ~1,900 |
| cbsa_to_county.csv | County → CBSA mapping | ~1,400 |

---

## How This Enables PopulationSim

### Current State (v1.0): Knowledge-Based Synthesis

```
User: "What's the diabetes prevalence in Harris County, TX?"

Claude: "Based on my knowledge of urban Texas counties and national 
        diabetes patterns, Harris County likely has diabetes prevalence 
        around 11-13%, somewhat higher than the national average due to 
        demographic factors and regional health patterns."
```

**Limitations**:
- No exact values
- Confidence is implicit
- Can't distinguish tracts within county
- No audit trail for compliance

### Future State (v2.0): Data-First with Transparent Synthesis

```
User: "What's the diabetes prevalence in Harris County, TX?"

Claude: "Harris County, TX has adult diabetes prevalence of 12.1% 
        (CDC PLACES 2024, based on 2022 BRFSS data). This is higher 
        than the national rate of 10.1%.
        
        Within the county, prevalence varies significantly by tract:
        - Lowest: 6.8% (tract 48201421502, River Oaks area)
        - Highest: 21.3% (tract 48201311500, Third Ward)
        - Median across 786 tracts: 11.4%
        
        The high-prevalence areas correlate strongly with SVI scores 
        above 0.75 and ADI national percentiles above 80."
```

**Capabilities Gained**:
- Exact values with source citation
- Within-county variation visible
- SDOH correlation analysis
- Audit-ready data provenance

### New Skill Capabilities

| Skill | v1.0 Capability | v2.0 Enhancement |
|-------|-----------------|------------------|
| **county-profile** | Synthesized demographics | Real ACS + PLACES + SVI data |
| **tract-analysis** | Limited | Full tract-level queries with real data |
| **sdoh-profile** | Approximated indices | Real SVI + ADI rankings |
| **cohort-specification** | Synthetic distributions | Distributions matching real population |
| **health-equity-analysis** | Directional only | Quantitative disparities from real data |

### The Transparency Principle in Action

| Data Availability | Response Pattern |
|-------------------|------------------|
| **Direct from embedded data** | "Harris County diabetes: 12.1% (CDC PLACES 2024)" |
| **Aggregated from embedded** | "Houston MSA diabetes: 11.8% (computed from 9 county PLACES values)" |
| **Derived from embedded** | "Tract ADI estimate: ~75th percentile (averaged from 3 component block groups)" |
| **Synthesized** | "2030 projected prevalence: ~14% (modeled from aging demographics and trend data). Note: This is a projection, not observed data." |

---

## Cross-Product Impact

### PatientSim Integration

**Current State**: PatientSim generates patients with demographics and conditions, but distributions are based on Claude's general knowledge.

**With Embedded Data**:

| Capability | How Data Package Enables It |
|------------|----------------------------|
| **Realistic demographics** | Generate patients matching actual tract-level age/sex/race distributions |
| **Accurate prevalence** | Assign conditions at rates matching CDC PLACES for the specified geography |
| **SDOH-aware patients** | Include SVI/ADI-derived social factors that correlate with health outcomes |
| **Health equity cohorts** | Create patient panels reflecting real disparities between neighborhoods |

**Example Enhancement**:
```
User: "Generate 100 patients for a diabetes clinic in Houston's Third Ward"

PatientSim (v2.0):
- Pulls tract 48201311500 demographics: 73% Black, median age 34, 28% poverty
- Applies PLACES diabetes rate: 21.3% (vs 12.1% county average)
- Incorporates SVI 0.89: Higher rates of uninsured, transportation barriers
- Generates patients with realistic comorbidity patterns for high-deprivation area
- Each patient has SDOH flags derived from real neighborhood characteristics
```

### MemberSim Integration

**Current State**: MemberSim generates health plan members with coverage and claims, but member panels don't reflect real market demographics.

**With Embedded Data**:

| Capability | How Data Package Enables It |
|------------|----------------------------|
| **Actuarially sound panels** | Member demographics match real service area populations |
| **Realistic plan mix** | Insurance coverage types from ACS (employer, Medicare, Medicaid, individual) |
| **Risk adjustment accuracy** | SDOH factors (ADI) now used in CMS models can be incorporated |
| **Network adequacy analysis** | Understand where members live relative to social vulnerability |

**Example Enhancement**:
```
User: "Generate a 10,000 member Medicare Advantage panel for Maricopa County, AZ"

MemberSim (v2.0):
- Pulls Maricopa 65+ demographics: Age distribution, income, racial composition
- Applies PLACES chronic condition rates for 65+ population
- Stratifies by ADI: 15% of members in high-deprivation block groups (ADI 80+)
- Generates realistic HCC risk score distribution based on actual prevalence
- Members in high-ADI areas have higher utilization patterns (per literature)
```

### RxMemberSim Integration

**Current State**: RxMemberSim generates pharmacy claims, but prescribing patterns are generalized.

**With Embedded Data**:

| Capability | How Data Package Enables It |
|------------|----------------------------|
| **Geographic prescribing variation** | Rx patterns reflecting regional disease burden |
| **Adherence modeling** | ADI correlates with medication adherence (validated) |
| **Specialty drug access** | SVI transportation barriers affect specialty pharmacy access |
| **Generic vs brand patterns** | Income/poverty data informs generic substitution rates |

**Example Enhancement**:
```
User: "Generate pharmacy claims for diabetes patients in rural Appalachian county"

RxMemberSim (v2.0):
- Pulls county PLACES: Diabetes 16.2%, Obesity 42%, COPD 14%
- Notes high ADI (85th percentile): Expect adherence challenges
- Applies regional prescribing: Higher sulfonylurea use, lower GLP-1 (cost/access)
- Models 90-day fills for stable patients (mail-order more common in rural)
- Generates realistic gaps in therapy based on SDOH barriers
```

### TrialSim Integration

**Current State**: TrialSim generates clinical trial data, but site selection and diversity planning are approximated.

**With Embedded Data**:

| Capability | How Data Package Enables It |
|------------|----------------------------|
| **Site feasibility** | Match protocol criteria to real population prevalence by tract |
| **Diversity planning** | Identify tracts with target demographic compositions |
| **FDA diversity requirements** | Quantify enrollment pools by race/ethnicity from real ACS data |
| **Underserved population access** | Use SVI to identify high-vulnerability areas for targeted enrollment |

**Example Enhancement**:
```
User: "Identify optimal sites for Phase 3 NASH trial requiring 30% Hispanic enrollment"

TrialSim (v2.0):
- Queries PLACES for NAFLD/obesity prevalence by tract
- Filters for tracts with >30% Hispanic population (ACS)
- Ranks by disease burden × target demographic concentration
- Identifies Houston, Phoenix, LA tracts meeting criteria
- Notes SVI scores to flag potential retention challenges
```

---

## NetworkSim Synergy (Future)

When NetworkSim is developed, the embedded data package creates powerful integration opportunities:

### Planned NetworkSim Data Sources

| Source | Content | Integration with Population Data |
|--------|---------|----------------------------------|
| **NPPES NPI Registry** | All US providers/facilities | Provider density by tract/county |
| **CMS Provider of Services** | Hospital characteristics | Facility access analysis |
| **CMS Physician Compare** | Physician specialties, quality | Specialist availability |
| **HRSA Health Center Data** | FQHCs, rural health clinics | Safety net coverage |

### Integration Cohorts

**Cohort 1: Healthcare Desert Identification**
```
Combine:
- High SVI tracts (vulnerability)
- Low provider density (NetworkSim)
- High chronic disease prevalence (PLACES)
= Identify underserved areas needing intervention
```

**Cohort 2: Network Adequacy Assessment**
```
Combine:
- Member home locations by tract (MemberSim)
- Provider locations and specialties (NetworkSim)  
- Transportation access (SVI Theme 4)
= Calculate true access considering SDOH barriers
```

**Cohort 3: Value-Based Care Targeting**
```
Combine:
- High-ADI block groups (population deprivation)
- Attributed members in those areas (MemberSim)
- Available community health resources (NetworkSim)
= Design care management programs for highest-need populations
```

**Cohort 4: Clinical Trial Site Optimization**
```
Combine:
- Disease prevalence by tract (PLACES)
- Demographic targets (ACS)
- Investigator locations (NetworkSim NPI)
- Patient accessibility (SVI transportation)
= Optimal site selection balancing feasibility and diversity
```

### Data Flow Vision

```
┌─────────────────────────────────────────────────────────────────────┐
│                     HEALTHSIM DATA FOUNDATION                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐          │
│  │   Census     │    │     CDC      │    │   UW-Madison │          │
│  │     ACS      │    │   PLACES     │    │     ADI      │          │
│  │ Demographics │    │   Health     │    │    SDOH      │          │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘          │
│         │                   │                   │                   │
│         └─────────┬─────────┴─────────┬─────────┘                   │
│                   │                   │                             │
│                   ▼                   ▼                             │
│         ┌─────────────────────────────────────┐                     │
│         │         POPULATIONSIM v2.0          │                     │
│         │    Embedded Data + Smart Synthesis   │                     │
│         └─────────────────┬───────────────────┘                     │
│                           │                                         │
│         ┌─────────────────┼─────────────────┐                       │
│         │                 │                 │                       │
│         ▼                 ▼                 ▼                       │
│  ┌────────────┐   ┌────────────┐   ┌────────────┐                  │
│  │ PatientSim │   │ MemberSim  │   │TrialSim   │                  │
│  │            │   │ RxMemberSim│   │            │                  │
│  │ Realistic  │   │ Actuarial  │   │ Feasible   │                  │
│  │ Patients   │   │ Accuracy   │   │ Trials     │                  │
│  └────────────┘   └────────────┘   └────────────┘                  │
│         │                 │                 │                       │
│         └─────────────────┼─────────────────┘                       │
│                           │                                         │
│                           ▼                                         │
│         ┌─────────────────────────────────────┐                     │
│         │          NETWORKSIM (Future)         │                     │
│         │     Provider + Facility + Access     │                     │
│         └─────────────────────────────────────┘                     │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Architecture Changes

### Current PopulationSim Architecture (v1.0)

```
skills/populationsim/
├── SKILL.md                    # Master routing skill
├── skills/
│   ├── county-profile.md       # Synthesis-based county data
│   ├── tract-analysis.md       # Limited tract capability
│   ├── cohort-specification.md # Synthetic cohort generation
│   ├── sdoh-profile.md         # Approximated SDOH
│   └── health-equity.md        # Directional analysis
├── models/
│   └── populationsim-canonical.md
└── references/
    ├── geography-codes.md      # Code systems only
    ├── census-variables.md     # Variable definitions only
    └── ...                     # Methodology docs only
```

**Limitation**: No actual data—skills synthesize everything from domain knowledge.

### New PopulationSim Architecture (v2.0)

```
skills/populationsim/
├── SKILL.md                    # Master routing skill (updated)
├── skills/
│   ├── county-profile.md       # Enhanced: reads real data
│   ├── tract-analysis.md       # Enhanced: full tract queries
│   ├── block-group-adi.md      # NEW: ADI lookups
│   ├── cohort-specification.md # Enhanced: real distributions
│   ├── sdoh-profile.md         # Enhanced: real SVI + ADI
│   ├── health-equity.md        # Enhanced: quantitative analysis
│   └── data-query.md           # NEW: direct data access skill
├── models/
│   └── populationsim-canonical.md  # Updated with data fields
├── data/                       # NEW: Embedded data directory
│   ├── README.md               # Data dictionary and provenance
│   ├── county/
│   │   ├── acs_county_2023.csv
│   │   ├── places_county_2024.csv
│   │   └── svi_county_2022.csv
│   ├── tract/
│   │   ├── acs_tract_2023.csv
│   │   ├── places_tract_2024.csv
│   │   └── svi_tract_2022.csv
│   ├── block_group/
│   │   └── adi_block_group_2023.csv
│   └── crosswalks/
│       ├── fips_state.csv
│       ├── fips_county.csv
│       ├── tract_to_county.csv
│       ├── block_group_to_tract.csv
│       └── cbsa_definitions.csv
└── references/
    ├── geography-codes.md
    ├── census-variables.md
    ├── data-sources.md         # Enhanced: provenance details
    └── data-dictionary.md      # NEW: field-level documentation
```

### Key Architecture Principles

#### 1. Data Loading Strategy

Skills will include instructions for Claude to read embedded data files when available:

```markdown
## Data Access Pattern

When user requests data for a specific geography:

1. **Identify geography type** (county, tract, block group)
2. **Look up in embedded data**:
   - County: Read from `data/county/{dataset}.csv`
   - Tract: Read from `data/tract/{dataset}.csv`
   - Block group: Read from `data/block_group/adi_block_group_2023.csv`
3. **If found**: Return exact values with source citation
4. **If not found**: Synthesize with explicit disclaimer
```

#### 2. Data Provenance in Responses

Every data point should be traceable:

```json
{
  "geography": {
    "type": "tract",
    "geoid": "48201311500",
    "name": "Census Tract 3115, Harris County, TX"
  },
  "metrics": {
    "diabetes_prevalence": {
      "value": 21.3,
      "unit": "percent",
      "source": "CDC PLACES 2024",
      "data_year": 2022,
      "methodology": "Model-based estimate from BRFSS"
    },
    "svi_overall": {
      "value": 0.89,
      "source": "CDC/ATSDR SVI 2022",
      "interpretation": "Higher vulnerability than 89% of US tracts"
    }
  }
}
```

#### 3. Graceful Degradation

When exact data isn't available:

| Cohort | Response Strategy |
|----------|-------------------|
| Data exists | Return exact value with citation |
| Data exists at different level | Aggregate/disaggregate with explanation |
| Data doesn't exist | Synthesize with clear disclaimer |
| Data is outdated | Return with vintage note, offer to synthesize current estimate |

#### 4. File Size Management

For the ~133 MB data package:

| Approach | Pros | Cons |
|----------|------|------|
| **Direct embed in repo** | Simple, always available | Large repo size |
| **Git LFS** | Repo stays small, data versioned | Requires LFS setup |
| **External hosting** | Smallest repo | Dependency on external availability |
| **Lazy loading** | Best of both | Implementation complexity |

**Recommendation**: Use **Git LFS** for the data directory. This keeps the repo manageable while maintaining version control over the data files.

---

## Implementation Approach

### Phase 1: Data Acquisition & Validation (1-2 sessions)

**Objectives**:
- Download all source datasets
- Validate completeness and quality
- Standardize formats (consistent FIPS, column names)
- Create data dictionary

**Deliverables**:
- [ ] Raw data files downloaded
- [ ] Validation scripts/checks run
- [ ] Standardized CSV files created
- [ ] `data/README.md` with provenance documentation
- [ ] `references/data-dictionary.md` with field definitions

### Phase 2: Skill Updates (2-3 sessions)

**Objectives**:
- Update existing skills to read embedded data
- Add new data-query skill
- Update canonical model with data fields
- Add data provenance to response patterns

**Deliverables**:
- [ ] `county-profile.md` updated
- [ ] `tract-analysis.md` enhanced
- [ ] `block-group-adi.md` created
- [ ] `sdoh-profile.md` updated with real SVI/ADI
- [ ] `data-query.md` created for direct data access
- [ ] `populationsim-canonical.md` updated

### Phase 3: Cross-Product Integration (1-2 sessions)

**Objectives**:
- Update PatientSim, MemberSim, RxMemberSim integration patterns
- Add examples using real data
- Document data-driven generation patterns

**Deliverables**:
- [ ] Cross-product SKILL.md sections updated
- [ ] Integration examples using real data
- [ ] Hello-HealthSim examples updated

### Phase 4: Testing & Documentation (1 session)

**Objectives**:
- Test all skills with real data queries
- Verify cross-product integration
- Complete documentation
- Update CHANGELOG

**Deliverables**:
- [ ] Test queries documented with expected results
- [ ] Architecture guide updated
- [ ] CHANGELOG updated
- [ ] Git LFS configured and data committed

---

## Success Criteria

### Functional Requirements

| Requirement | Validation |
|-------------|------------|
| Query any US county and get real data | Test 10 diverse counties |
| Query any US tract and get real data | Test 20 tracts across different states |
| Query any block group for ADI | Test 10 block groups |
| Aggregate tract data to county | Computed values match embedded county data |
| Cross-product integration works | PatientSim generates patients matching real tract demographics |

### Quality Requirements

| Requirement | Validation |
|-------------|------------|
| Data provenance in all responses | Every metric includes source and year |
| Graceful degradation | Queries for unavailable data return appropriate synthesis |
| Performance acceptable | Data lookups complete within conversation flow |
| Documentation complete | All fields documented in data dictionary |

### Technical Requirements

| Requirement | Validation |
|-------------|------------|
| Git LFS configured | Data files tracked in LFS |
| Repository size manageable | Main repo < 50 MB (excluding LFS) |
| Data files validated | No missing required fields, valid FIPS codes |

---

## Appendix: Data File Schemas

### County ACS Schema (acs_county_2023.csv)

```
fips              STRING    County FIPS code (5 digits)
state_fips        STRING    State FIPS code (2 digits)
county_name       STRING    County name
state_abbr        STRING    State abbreviation
state_name        STRING    State full name
total_population  INTEGER   Total population count
population_density FLOAT    Population per square mile
median_age        FLOAT     Median age in years
pct_male          FLOAT     Percent male
pct_female        FLOAT     Percent female
pct_white         FLOAT     Percent White alone
pct_black         FLOAT     Percent Black alone
pct_asian         FLOAT     Percent Asian alone
pct_aian          FLOAT     Percent American Indian/Alaska Native
pct_nhpi          FLOAT     Percent Native Hawaiian/Pacific Islander
pct_other         FLOAT     Percent other race
pct_two_or_more   FLOAT     Percent two or more races
pct_hispanic      FLOAT     Percent Hispanic/Latino (any race)
median_household_income INTEGER Median household income (dollars)
per_capita_income INTEGER   Per capita income (dollars)
pct_below_poverty FLOAT     Percent below poverty level
pct_below_150_poverty FLOAT Percent below 150% poverty level
pct_uninsured     FLOAT     Percent without health insurance
pct_employer_ins  FLOAT     Percent with employer-sponsored insurance
pct_medicare      FLOAT     Percent with Medicare
pct_medicaid      FLOAT     Percent with Medicaid
pct_hs_or_higher  FLOAT     Percent with high school diploma or higher
pct_bachelors_plus FLOAT    Percent with bachelor's degree or higher
pct_employed      FLOAT     Employment rate (civilian labor force)
unemployment_rate FLOAT     Unemployment rate
```

### County PLACES Schema (places_county_2024.csv)

```
fips              STRING    County FIPS code
state_abbr        STRING    State abbreviation
county_name       STRING    County name
measure_id        STRING    PLACES measure identifier
measure_name      STRING    Full measure name
data_value        FLOAT     Crude prevalence (percent)
low_confidence    FLOAT     Lower 95% confidence bound
high_confidence   FLOAT     Upper 95% confidence bound
data_value_type   STRING    "Crude prevalence" or "Age-adjusted"
category          STRING    Health outcomes/Prevention/etc.
```

### ADI Block Group Schema (adi_block_group_2023.csv)

```
geoid             STRING    Block group GEOID (12 digits)
state_fips        STRING    State FIPS code
county_fips       STRING    County FIPS code (5 digits)
tract_fips        STRING    Tract FIPS code (11 digits)
state_abbr        STRING    State abbreviation
county_name       STRING    County name
adi_natl_rank     INTEGER   National percentile ranking (1-100)
adi_state_decile  INTEGER   State decile ranking (1-10)
```

---

## Next Steps

1. **Approve this architecture** ✓
2. **Begin Phase 1**: Download and validate source data
3. **Configure Git LFS** for data directory
4. **Implement Phase 2-4** per schedule above

Estimated total effort: **5-8 sessions**

---

*Document Version: 1.0*  
*Created: December 2024*  
*Status: Planning*
