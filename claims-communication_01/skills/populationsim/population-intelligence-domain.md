---
name: population-intelligence-domain
description: >
  Core domain knowledge for population health intelligence. Covers geographic
  hierarchies, census data fundamentals, health indicator methodology, SDOH 
  frameworks, and cohort definition principles. Reference this for understanding
  PopulationSim concepts, data sources, and methodology.
---

# Population Intelligence Domain Knowledge

## Overview

Population intelligence combines demographic data, health indicators, and social determinants to create comprehensive profiles of geographic areas and population segments. This knowledge enables:

1. **Geographic Profiling**: Understanding the characteristics of counties, metro areas, or custom regions
2. **Health Pattern Analysis**: Identifying disease prevalence, risk factors, and disparities
3. **SDOH Assessment**: Measuring social vulnerability and community barriers
4. **Cohort Definition**: Creating specifications for synthetic data generation

**Key Principle**: PopulationSim uses real population data from public sources to inform synthetic data generation, ensuring realistic distributions and correlations.

---

## Geographic Hierarchy

### Census Geography Levels

The US Census Bureau defines a hierarchical geography system:

```
Nation
  └── Region (4: Northeast, Midwest, South, West)
      └── Division (9)
          └── State (50 + DC + territories)
              └── County (3,143)
                  └── Census Tract (~85,000)
                      └── Block Group (~240,000)
                          └── Block (~11 million)
```

### Geographic Level Characteristics

| Level | Typical Population | Primary Use | Data Availability |
|-------|-------------------|-------------|-------------------|
| **Nation** | 330+ million | National benchmarks | All sources |
| **State** | 500K - 40M | Policy analysis, state comparisons | All sources |
| **County** | 1K - 10M | Health department planning, regional analysis | All sources |
| **Census Tract** | 1,200 - 8,000 | Neighborhood-level analysis, SVI | ACS 5-year, CDC PLACES |
| **Block Group** | 600 - 3,000 | Granular SDOH, ADI | ACS 5-year, ADI |
| **Block** | 0 - 1,000 | Decennial census only | Decennial only |

### Geographic Identifiers

| Identifier | Format | Example | Description |
|------------|--------|---------|-------------|
| **State FIPS** | 2 digits | `06` | California |
| **County FIPS** | 5 digits | `06073` | San Diego County, CA |
| **Tract FIPS** | 11 digits | `06073008346` | Specific tract in San Diego |
| **Block Group** | 12 digits | `060730083461` | Block group within tract |
| **CBSA Code** | 5 digits | `41740` | San Diego-Chula Vista-Carlsbad MSA |

### Metropolitan Statistical Areas (MSAs)

MSAs are defined by the Office of Management and Budget (OMB):

- **Metropolitan Statistical Area**: Core urban area ≥50,000 population
- **Micropolitan Statistical Area**: Core urban area 10,000-49,999
- **Combined Statistical Area**: Adjacent metro/micro areas with commuting ties

**CBSA Structure**:
```
CBSA (Core Based Statistical Area)
├── Central County/Counties (contain core urban area)
└── Outlying Counties (25%+ commuting to central)
```

---

## Census Data Fundamentals

### American Community Survey (ACS)

The ACS is the primary source for demographic and socioeconomic data between decennial censuses.

#### Estimate Types

| Type | Geography Coverage | Sample Size | Best For |
|------|-------------------|-------------|----------|
| **1-Year** | Pop ≥ 65,000 only | ~3.5M households/year | Current estimates, large areas |
| **5-Year** | All geographies | ~15M households pooled | Small area analysis, tracts |

**Decision Guide**:
- Need tract-level data? → Use 5-year
- Need most current data for large area? → Use 1-year
- Analyzing trends over time? → Use consistent estimate type

#### Key ACS Subject Tables

| Table | Content | Key Variables |
|-------|---------|---------------|
| **S0101** | Age and Sex | Age distribution, median age, dependency ratio |
| **S0201** | Selected Population Profile | Comprehensive demographic summary |
| **S1501** | Educational Attainment | % with HS diploma, bachelor's, graduate degree |
| **S1701** | Poverty Status | Poverty rate, % below 150% FPL |
| **S1901** | Income | Median household income, income distribution |
| **S2301** | Employment Status | Labor force participation, unemployment |
| **S2701** | Health Insurance Coverage | Uninsured rate by age, coverage type |

#### Key ACS Data Tables (B-Tables)

| Table | Content | Use |
|-------|---------|-----|
| **B01001** | Sex by Age | Detailed age distribution |
| **B02001** | Race | Race alone categories |
| **B03002** | Hispanic Origin by Race | Race/ethnicity combination |
| **B19013** | Median Household Income | Income analysis |
| **B25001** | Housing Units | Housing stock |

### Margin of Error (MOE)

All ACS estimates include sampling error expressed as MOE at 90% confidence.

#### MOE Calculations

**For sums**:
```
MOE_sum = √(MOE₁² + MOE₂² + ... + MOEₙ²)
```

**For proportions** (ratio of estimate to base):
```
MOE_proportion = √(MOE_numerator² + (proportion² × MOE_denominator²)) / denominator
```

**Coefficient of Variation (CV)**:
```
CV = (MOE / 1.645) / Estimate × 100
```

#### Reliability Thresholds

| CV | Reliability | Recommendation |
|----|-------------|----------------|
| < 15% | High | Use with confidence |
| 15-30% | Moderate | Use with caution, note uncertainty |
| > 30% | Low | Consider aggregating geographies |

---

## Health Indicator Methodology

### CDC PLACES

CDC PLACES (Population Level Analysis and Community Estimates) provides model-based small area estimates for health measures.

#### Measure Categories (27 Total)

**Health Outcomes (13)**:
| Measure | Variable | Definition |
|---------|----------|------------|
| Arthritis | ARTHRITIS | Arthritis among adults ≥18 |
| Asthma | CASTHMA | Current asthma among adults |
| Cancer | CANCER | Cancer (excluding skin) among adults |
| CHD | CHD | Coronary heart disease among adults |
| COPD | COPD | COPD among adults |
| Depression | DEPRESSION | Depression among adults |
| Diabetes | DIABETES | Diagnosed diabetes among adults |
| High Blood Pressure | BPHIGH | High blood pressure among adults |
| High Cholesterol | HIGHCHOL | High cholesterol among adults |
| Chronic Kidney Disease | KIDNEY | CKD among adults |
| Obesity | OBESITY | Obesity among adults |
| Stroke | STROKE | Stroke among adults |
| Poor Mental Health | MHLTH | ≥14 days poor mental health |
| Poor Physical Health | PHLTH | ≥14 days poor physical health |

**Prevention (9)**:
| Measure | Variable | Definition |
|---------|----------|------------|
| Annual Checkup | CHECKUP | Annual checkup among adults |
| Dental Visit | DENTAL | Dental visit in past year |
| Cholesterol Screening | CHOLSCREEN | Cholesterol screening |
| Colorectal Screening | COLON_SCREEN | Up-to-date colorectal cancer screening |
| Mammography | MAMMOUSE | Mammography among women 50-74 |
| Pap Smear | PAPTEST | Pap test among women 21-65 |
| Core Preventive Services (Men) | COREM | Core preventive services, men |
| Core Preventive Services (Women) | COREW | Core preventive services, women |

**Health Risk Behaviors (4)**:
| Measure | Variable | Definition |
|---------|----------|------------|
| Binge Drinking | BINGE | Binge drinking among adults |
| Current Smoking | CSMOKING | Current smoking among adults |
| Physical Inactivity | LPA | No leisure-time physical activity |
| Short Sleep | SLEEP | Sleep < 7 hours among adults |

**Health Status (1)**:
| Measure | Variable | Definition |
|---------|----------|------------|
| Fair/Poor Health | GHLTH | Fair or poor self-rated health |

#### Age Adjustment

CDC PLACES uses **direct age adjustment** to the 2000 US standard population:

```
Age-Adjusted Rate = Σ(Age-specific rate × Standard population weight)
```

**Standard Population Weights (2000)**:
| Age Group | Weight |
|-----------|--------|
| 18-24 | 0.1283 |
| 25-34 | 0.1810 |
| 35-44 | 0.1994 |
| 45-54 | 0.1721 |
| 55-64 | 0.1272 |
| 65+ | 0.1920 |

**Why Age Adjustment Matters**:
- Florida has older population than Utah
- Without adjustment, Florida appears less healthy
- Age adjustment enables fair comparison

#### PLACES Methodology

1. **Data Source**: Behavioral Risk Factor Surveillance System (BRFSS)
2. **Model**: Multilevel regression with poststratification (MRP)
3. **Covariates**: Age, race/ethnicity, sex, education, income, county-level factors
4. **Output**: Prevalence estimates for counties and census tracts

---

## SDOH Frameworks

### Social Vulnerability Index (SVI)

CDC/ATSDR Social Vulnerability Index ranks census tracts on social factors affecting disaster resilience and health.

#### SVI Structure: 4 Themes, 16 Variables

**Theme 1: Socioeconomic Status**
| Variable | ACS Table | Definition |
|----------|-----------|------------|
| Below 150% Poverty | S1701 | % persons below 150% FPL |
| Unemployed | S2301 | % civilian unemployed |
| Housing Cost Burden | DP04 | % paying >30% income for housing |
| No High School Diploma | S1501 | % age 25+ without HS diploma |
| No Health Insurance | S2701 | % without health insurance |

**Theme 2: Household Characteristics**
| Variable | ACS Table | Definition |
|----------|-----------|------------|
| Aged 65+ | S0101 | % population age 65+ |
| Aged 17 or Younger | S0101 | % population age 17 or younger |
| Civilian with Disability | S1810 | % with disability |
| Single-Parent Households | S1101 | % single-parent with children |
| English Proficiency | S1601 | % speaking English less than well |

**Theme 3: Racial & Ethnic Minority Status**
| Variable | ACS Table | Definition |
|----------|-----------|------------|
| Minority Status | B03002 | % minority (all except White non-Hispanic) |

**Theme 4: Housing Type & Transportation**
| Variable | ACS Table | Definition |
|----------|-----------|------------|
| Multi-Unit Structures | DP04 | % in structures with 10+ units |
| Mobile Homes | DP04 | % living in mobile homes |
| Crowding | DP04 | % with >1 person per room |
| No Vehicle | DP04 | % households with no vehicle |
| Group Quarters | S2601A | % in group quarters (non-institutional) |

#### SVI Scoring

1. **Percentile Ranking**: Each variable ranked 0-1 within state or US
2. **Theme Score**: Sum of variable percentiles / number of variables
3. **Overall SVI**: Sum of all theme scores (0-4 scale, often normalized to 0-1)

**Interpretation**:
| SVI Range | Vulnerability Level |
|-----------|---------------------|
| 0.00-0.25 | Low |
| 0.25-0.50 | Low-Moderate |
| 0.50-0.75 | Moderate-High |
| 0.75-1.00 | High |

### Area Deprivation Index (ADI)

Health Resources and Services Administration (HRSA) ADI measures neighborhood socioeconomic disadvantage.

#### ADI Factor Structure (17 Measures)

**Income Domain**:
- Median family income
- Income disparity (ratio of households <$10K to >$50K)
- % families below poverty

**Education Domain**:
- % age 25+ with < 9 years education
- % age 25+ with at least high school diploma

**Employment Domain**:
- % civilian labor force unemployed

**Housing Quality Domain**:
- Median home value
- Median gross rent
- Median monthly mortgage
- % owner-occupied housing
- % occupied units without complete plumbing
- % occupied units without telephone
- % crowding (>1 person/room)

#### ADI Rankings

| Ranking | Scale | Interpretation |
|---------|-------|----------------|
| **National Percentile** | 1-100 | 100 = most disadvantaged nationally |
| **State Decile** | 1-10 | 10 = most disadvantaged in state |

**Usage**:
- National percentile: Cross-state comparisons
- State decile: Within-state targeting

---

## Cohort Definition Principles

### CohortSpecification Structure

A cohort specification defines a population segment for synthetic data generation:

```
CohortSpecification
├── Identification
│   ├── cohort_id (unique identifier)
│   ├── name (human-readable name)
│   └── description
│
├── Geographic Filter
│   ├── base (state, county, MSA, tract list)
│   ├── constraint (SVI, ADI, urban/rural)
│   └── resolved_units (tract count, geography type)
│
├── Population Filter
│   ├── age_range
│   ├── sex
│   ├── conditions (ICD-10 codes)
│   └── sdoh_risk
│
├── Estimated Real Population
│
├── Demographic Profile (distributions)
│   ├── race_ethnicity
│   ├── age_distribution
│   └── sex_distribution
│
├── Clinical Profile (rates)
│   ├── primary_condition
│   ├── comorbidities
│   └── clinical_markers
│
├── SDOH Profile (barrier frequencies)
│   ├── economic_barriers
│   ├── access_barriers
│   └── social_barriers
│
├── Target Product (PatientSim, MemberSim, TrialSim)
│
└── Generation Options
    ├── count
    ├── include_options
    └── format_options
```

### Profile Estimation Methods

| Component | Data Source | Method |
|-----------|-------------|--------|
| Age distribution | ACS S0101 | Direct from census |
| Race/ethnicity | ACS B03002 | Direct from census |
| Condition prevalence | CDC PLACES | Age-adjusted rates |
| Comorbidity rates | Literature + MEPS | Published comorbidity matrices |
| SDOH barriers | SVI components | Theme-specific variables |

### Demographic Distribution Matching

When generating synthetic data from a cohort spec:

1. **Marginal Distributions**: Match overall percentages
   - Example: 58% Hispanic, 42% other

2. **Joint Distributions**: Respect correlations
   - Age-condition correlation (older → more diabetes)
   - Race-SDOH correlation (minority → higher SVI areas)
   - Income-insurance correlation (lower income → more Medicaid)

3. **Geographic Clustering**: Maintain spatial patterns
   - Patients from same tract share SDOH factors
   - Nearby tracts have similar characteristics

### SDOH to Z-Code Mapping

PopulationSim SDOH profiles translate to ICD-10 Z-codes in PatientSim:

| SDOH Factor | Z-Code | Description |
|-------------|--------|-------------|
| Food insecurity | Z59.41 | Food insecurity |
| Housing instability | Z59.00 | Homelessness, unspecified |
| Low income | Z59.6 | Low income |
| Transportation barrier | Z59.82 | Transportation insecurity |
| Social isolation | Z60.2 | Problems related to living alone |
| Limited English | Z60.3 | Acculturation difficulty |
| Unemployment | Z56.0 | Unemployment, unspecified |
| Inadequate housing | Z59.1 | Inadequate housing |

---

## Integration with HealthSim Products

### PopulationSim → PatientSim

```
CohortSpecification
├── demographic_profile → Patient demographics
│   ├── race_ethnicity → Patient.race, Patient.ethnicity
│   ├── age_distribution → Patient.birth_date
│   └── sex_distribution → Patient.gender
│
├── clinical_profile → Diagnosis assignment
│   ├── primary_condition → Principal diagnosis
│   └── comorbidities → Secondary diagnoses (with rates)
│
└── sdoh_profile → SDOH Z-codes
    ├── food_insecurity → Z59.41
    ├── housing → Z59.xx
    └── transportation → Z59.82
```

### PopulationSim → MemberSim

```
PopulationProfile
├── healthcare_access.insurance_mix → Plan type distribution
│   ├── employer → Commercial (Group)
│   ├── individual → Commercial (Individual)
│   ├── medicare → Medicare
│   ├── medicaid → Medicaid
│   └── uninsured → (exclude or COBRA)
│
├── demographics → Member demographics
│
└── sdoh_indices → Utilization adjustments
    ├── high_svi → Higher ED utilization
    └── low_access → Lower preventive care
```

### PopulationSim → TrialSim

```
CohortSpecification (diversity-focused)
├── demographic_profile → Subject diversity targets
│   └── race_ethnicity → Enrollment goals by group
│
├── geography_filter → Site selection input
│   └── high_prevalence_areas → Recommended sites
│
└── clinical_profile → I/E criteria alignment
    └── comorbidities → Exclusion risk assessment
```

---

## Terminology Glossary

| Term | Definition |
|------|------------|
| **ACS** | American Community Survey - Census Bureau annual survey providing demographic, social, economic, and housing data |
| **ADI** | Area Deprivation Index - HRSA measure of neighborhood socioeconomic disadvantage |
| **Age-adjusted rate** | Prevalence rate standardized to eliminate age distribution effects, enabling fair geographic comparison |
| **BRFSS** | Behavioral Risk Factor Surveillance System - CDC telephone health survey |
| **CBSA** | Core Based Statistical Area - OMB-defined metro or micro area based on commuting patterns |
| **CDC PLACES** | Population Level Analysis and Community Estimates - model-based small area health estimates |
| **Cohort** | Defined population segment with shared characteristics for analysis or generation |
| **CV** | Coefficient of Variation - ratio of standard error to estimate, measures reliability |
| **FIPS** | Federal Information Processing Standards - numeric codes for geographic entities |
| **FPL** | Federal Poverty Level - income threshold used for program eligibility |
| **MOE** | Margin of Error - uncertainty measure for survey estimates at 90% confidence |
| **MRP** | Multilevel Regression with Poststratification - statistical method for small area estimation |
| **MSA** | Metropolitan Statistical Area - CBSA with urban core ≥50,000 population |
| **SDOH** | Social Determinants of Health - non-medical factors affecting health outcomes |
| **SVI** | Social Vulnerability Index - CDC/ATSDR composite measure of social factors |
| **Tract** | Census tract - statistical subdivision averaging 4,000 people designed to be stable over time |

---

## Examples

### Example 1: Interpreting SVI

**Request**: "Explain what an SVI of 0.85 means for a census tract"

**Response**:

An SVI of 0.85 indicates this census tract ranks in the 85th percentile for social vulnerability—meaning 85% of US tracts are less vulnerable, and only 15% are more vulnerable.

**Theme Breakdown** (hypothetical):

| Theme | Score | Interpretation |
|-------|-------|----------------|
| Socioeconomic (0.92) | Very High | High poverty, low education, high uninsured |
| Household Composition (0.78) | High | Significant elderly/disabled population |
| Minority Status (0.88) | Very High | Predominantly minority population |
| Housing/Transportation (0.82) | High | Housing quality issues, limited vehicle access |

**Implications for HealthSim Products**:

| Product | Impact |
|---------|--------|
| **PatientSim** | Higher rates of SDOH Z-codes (Z59.41 food insecurity, Z59.6 low income, Z59.82 transportation) |
| **MemberSim** | Higher Medicaid enrollment, lower commercial; higher ED utilization |
| **RxMemberSim** | Higher medication non-adherence due to cost barriers; more generic substitution |
| **TrialSim** | Important for diversity enrollment; may need transportation support for retention |

---

### Example 2: Census Data for Cohort Definition

**Request**: "What ACS data do I need to define a diabetic cohort in Texas border counties?"

**Response**:

**Step 1: Identify Border Counties**

Texas counties on Mexican border (14 total):
```
Cameron (48061), Hidalgo (48215), Starr (48427), 
Webb (48479), Zapata (48505), Maverick (48323), 
Kinney (48271), Val Verde (48465), Terrell (48443), 
Brewster (48043), Presidio (48377), Jeff Davis (48243), 
Hudspeth (48229), El Paso (48141)
```

**Step 2: Pull ACS 5-Year Estimates**

| Table | Variables | Purpose |
|-------|-----------|---------|
| S0101 | Age by sex | Age distribution for cohort |
| B03002 | Hispanic origin by race | Race/ethnicity profile |
| S1701 | Poverty status | Economic vulnerability |
| S2701 | Insurance coverage | Access assessment |
| S1901 | Income | Economic profile |

**Step 3: Pull CDC PLACES**

| Measure | Variable | Border Avg | Texas Avg |
|---------|----------|------------|-----------|
| Diabetes | DIABETES_CrudePrev | 14.2% | 11.8% |
| Obesity | OBESITY_CrudePrev | 36.1% | 33.2% |
| No Insurance | ACCESS2_CrudePrev | 24.3% | 17.5% |

**Step 4: Pull SVI**

| County | SVI Overall | Interpretation |
|--------|-------------|----------------|
| Starr | 0.98 | Highest vulnerability |
| Hidalgo | 0.94 | Very high |
| Cameron | 0.89 | Very high |
| Webb | 0.85 | High |
| El Paso | 0.72 | Moderate-high |

**Resulting Cohort Profile**:

```json
{
  "cohort_id": "TX-BORDER-DM-001",
  "name": "Texas Border County Diabetics",
  "geography_filter": {
    "counties": ["48061", "48215", "48427", "48479", "48141"],
    "constraint": "svi_overall >= 0.70"
  },
  "demographic_profile": {
    "race_ethnicity": {
      "hispanic": 0.88,
      "white_nh": 0.08,
      "other": 0.04
    },
    "median_age": 32.1
  },
  "clinical_profile": {
    "diabetes_prevalence": 0.142,
    "obesity_prevalence": 0.361,
    "comorbidities": {
      "hypertension": 0.68,
      "hyperlipidemia": 0.54
    }
  },
  "sdoh_profile": {
    "uninsured_rate": 0.243,
    "poverty_rate": 0.31,
    "limited_english": 0.28
  }
}
```

---

### Example 3: Age Adjustment Importance

**Request**: "Why do I need age-adjusted rates to compare Florida and Utah diabetes?"

**Response**:

**The Problem with Crude Rates**:

| State | Crude Diabetes Rate | Median Age |
|-------|---------------------|------------|
| Florida | 11.8% | 42.2 |
| Utah | 7.9% | 31.1 |

At first glance, Florida appears much unhealthier. But Florida has an older population, and diabetes increases with age.

**Age-Specific Rates** (both states similar within age groups):

| Age Group | Florida | Utah |
|-----------|---------|------|
| 18-44 | 3.2% | 3.1% |
| 45-64 | 12.8% | 12.5% |
| 65+ | 22.1% | 21.8% |

**Age-Adjusted Rates** (using 2000 standard population):

| State | Age-Adjusted Rate | Difference from Crude |
|-------|-------------------|----------------------|
| Florida | 10.2% | -1.6% |
| Utah | 9.8% | +1.9% |

**Conclusion**: After age adjustment, Florida and Utah have nearly identical diabetes rates. The apparent difference was due to age structure, not actual health differences.

**PopulationSim Practice**: All CDC PLACES measures are age-adjusted. When comparing geographies, always use age-adjusted rates for fair comparison.

---

## Related Skills

- [Geographic Skills](geographic/README.md) - County, tract, metro analysis
- [Health Pattern Skills](health-patterns/README.md) - Disease prevalence, disparities
- [SDOH Skills](sdoh/README.md) - SVI, ADI, community factors
- [Cohort Skills](cohorts/README.md) - Cohort specification
- [Trial Support Skills](trial-support/README.md) - Diversity planning, site selection

## Data Source References

| Source | URL | Update Frequency |
|--------|-----|------------------|
| Census ACS | data.census.gov | Annual |
| CDC PLACES | cdc.gov/places | Annual |
| CDC/ATSDR SVI | atsdr.cdc.gov/placeandhealth/svi | Biennial |
| HRSA ADI | neighborhoodatlas.medicine.wisc.edu | Annual |
