# PopulationSim Data Architecture: Option C Scoping

## Executive Summary

This document analyzes what public health and demographic data could be embedded in PopulationSim vs. what requires API access or synthesis. The analysis reveals a clear tiering:

| Tier | Geographic Level | Record Count | File Size | Recommendation |
|------|------------------|--------------|-----------|----------------|
| **Tier 1** | County | ~3,143 | ~2-5 MB | ✅ Embed all |
| **Tier 2** | Census Tract | ~85,000 | ~15-30 MB | ⚠️ Selective embed |
| **Tier 3** | Block Group | ~240,000 | ~50-100 MB | ❌ API or synthesis |

---

## Data Source Inventory

### 1. Census Bureau - American Community Survey (ACS)

**Availability**: Complete bulk download via FTP or API  
**Update Frequency**: Annual (5-year estimates most reliable for small areas)  
**License**: Public domain

#### Key Variables for PopulationSim

| Category | Variables | ACS Table | Use Case |
|----------|-----------|-----------|----------|
| Total Population | Count, density | B01003 | Base population sizing |
| Age Distribution | 18 age brackets by sex | B01001 | Age-appropriate conditions |
| Race | 7 categories | B02001 | Diversity planning |
| Ethnicity | Hispanic/Latino | B03003 | Diversity planning |
| Median Income | Household income | B19013 | SDOH, plan selection |
| Poverty Rate | Below poverty % | B17001 | SDOH, Medicaid eligibility |
| Insurance Coverage | By type (employer, Medicaid, Medicare, uninsured) | B27001-B27010 | MemberSim integration |
| Education | Attainment levels | B15003 | SDOH factor |
| Employment | Labor force status | B23025 | SDOH factor |
| Housing | Tenure, value | B25003, B25077 | ADI components |

#### File Size Estimates

| Level | Records | Columns | Est. CSV Size |
|-------|---------|---------|---------------|
| County | 3,143 | ~50 | ~1.5 MB |
| Tract | 85,000 | ~50 | ~40 MB |
| Block Group | 240,000 | ~50 | ~120 MB |

**Recommendation**: Embed county-level ACS. Tract-level could be embedded but adds significant size.

---

### 2. CDC PLACES (Health Indicators)

**Availability**: Complete download as CSV from data.cdc.gov  
**Update Frequency**: Annual (2024 release uses 2022 BRFSS data)  
**License**: Public domain

#### Measures Available (40 total in 2024 release)

| Category | Count | Key Measures |
|----------|-------|--------------|
| Health Outcomes | 12 | Diabetes, Obesity, CHD, COPD, Depression, Cancer, Stroke, CKD |
| Prevention | 7 | Checkup, Mammography, Colorectal screening, Dental visit |
| Health Risk Behaviors | 4 | Smoking, Binge drinking, Physical inactivity, Short sleep |
| Disabilities | 7 | Hearing, Vision, Cognitive, Mobility, Self-care, Independent living |
| Health Status | 3 | General health, Mental health days, Physical health days |
| Social Needs | 7 | Food insecurity, Housing insecurity, Utility needs, etc. |

#### File Size Estimates

| Level | Records | Measures | Est. CSV Size |
|-------|---------|----------|---------------|
| County | 3,143 | 40 | ~500 KB |
| Place/City | ~28,000 | 40 | ~4 MB |
| Tract | 85,000 | 40 | ~12 MB |
| ZCTA | 33,000 | 40 | ~5 MB |

**Recommendation**: Embed county-level PLACES. Tract-level is manageable if needed.

---

### 3. CDC/ATSDR Social Vulnerability Index (SVI)

**Availability**: Complete download as CSV or geodatabase  
**Update Frequency**: Biennial (2022 is current)  
**License**: Public domain

#### Variables (16 indicators across 4 themes)

| Theme | Variables |
|-------|-----------|
| Socioeconomic Status | Below 150% poverty, Unemployed, Housing cost burden, No HS diploma, No health insurance |
| Household Characteristics | Age 65+, Age 17 and younger, Civilian with disability, Single-parent households, English proficiency |
| Racial & Ethnic Minority Status | Hispanic/Latino, Black, Asian, AIAN, NHPI, Other race, Multiple races |
| Housing Type & Transportation | Multi-unit structures, Mobile homes, Crowding, No vehicle, Group quarters |

#### Output Fields

- Raw estimates and percentages for each variable
- Theme-specific percentile rankings (0-1)
- Overall SVI percentile ranking (0-1)
- Margin of error for each estimate

#### File Size Estimates

| Level | Records | Fields | Est. CSV Size |
|-------|---------|--------|---------------|
| County | 3,143 | ~125 | ~2 MB |
| Tract | 85,000 | ~125 | ~50 MB |
| ZCTA | 33,000 | ~125 | ~20 MB |

**Recommendation**: Embed county-level SVI. Tract-level is large but feasible.

---

### 4. Area Deprivation Index (ADI)

**Availability**: Download from Neighborhood Atlas (requires free registration)  
**Update Frequency**: Annual (2023 current)  
**License**: Free for research/non-commercial use

#### Variables (17 indicators across 4 domains)

| Domain | Indicators |
|--------|------------|
| Income | Median family income, Income disparity, % families below poverty, % population below 150% poverty |
| Education | % with less than 9 years education, % with less than 12 years education |
| Employment | % employed in white-collar occupation |
| Housing Quality | Median home value, Median gross rent, Median monthly mortgage, % owner-occupied housing, % housing units without complete plumbing, % housing units without telephone, % crowded housing, % single-parent households with children |

#### Output Fields

- National percentile ranking (1-100)
- State decile ranking (1-10)
- Raw scores are NOT publicly available (by design)

#### File Size Estimates

| Level | Records | Fields | Est. CSV Size |
|-------|---------|--------|---------------|
| Block Group | 240,000 | ~20 | ~25 MB |
| County (aggregated) | 3,143 | ~5 | ~200 KB |

**Caveat**: ADI is only validated at block group level. County aggregation requires population-weighted averaging.

**Recommendation**: ADI at block group level is too granular for embedding. Consider:
- Embedding county-level population-weighted summary (if we compute it)
- API access for block group lookup
- Synthesis using SVI as proxy (SVI and ADI are correlated ~0.7-0.8)

---

## Proposed Embedded Data Architecture

### Tier 1: Always Embedded (County Level) - ~5 MB Total

```
data/
├── census/
│   └── acs_county_2023.csv         # ~1.5 MB - Demographics, income, insurance
├── health/
│   └── cdc_places_county_2024.csv  # ~500 KB - 40 health indicators
├── sdoh/
│   └── svi_county_2022.csv         # ~2 MB - Social vulnerability
│   └── adi_county_summary.csv      # ~200 KB - Population-weighted ADI
└── geography/
    └── fips_cbsa_crosswalk.csv     # ~150 KB - County to metro area mapping
```

**Coverage**: 100% of US counties (3,143)  
**Use Cases**: All county-level queries, metro area profiles, state comparisons

### Tier 2: Optional Embedded (Tract Level) - ~100 MB Additional

```
data/
├── census/
│   └── acs_tract_2023.csv          # ~40 MB - Demographics by tract
├── health/
│   └── cdc_places_tract_2024.csv   # ~12 MB - Health indicators by tract
└── sdoh/
    └── svi_tract_2022.csv          # ~50 MB - SVI by tract
```

**Coverage**: 100% of US census tracts (~85,000)  
**Use Cases**: Neighborhood-level analysis, health equity, clinical trial site selection
**Trade-off**: Significant repo size increase, but enables much richer analysis

### Tier 3: API or Synthesis (Block Group Level)

Not embedded. Options:
1. **API MCP Server**: Query Census Bureau API, ADI API at runtime
2. **Synthesis**: Use tract-level data + statistical interpolation
3. **On-Demand Download**: User downloads block group files to local cache

---

## What Gets Synthesized vs. Real Data

### With Embedded Data (Tier 1 + 2)

| Query Type | Data Source | Accuracy |
|------------|-------------|----------|
| "Harris County demographics" | Real ACS data | ✅ Exact |
| "Diabetes rate in Cook County" | Real CDC PLACES | ✅ Exact |
| "SVI for Maricopa County" | Real CDC SVI | ✅ Exact |
| "Houston MSA population" | Real ACS, aggregated | ✅ Computed from real |
| "Census tract 48201311500 profile" | Real tract data | ✅ Exact (if Tier 2) |
| "Block group 060372071001 ADI" | ❌ Not embedded | 🔄 API or synthesize |

### Without Embedded Data (Current State)

| Query Type | Data Source | Accuracy |
|------------|-------------|----------|
| "Harris County demographics" | Claude synthesis | ⚠️ Plausible (~70-80%) |
| "Diabetes rate in Cook County" | Claude synthesis | ⚠️ Within national range |
| "SVI for Maricopa County" | Claude synthesis | ⚠️ Estimated from knowledge |

---

## Implementation Recommendations

### Phase 1: County-Level Embedding (Immediate Value)

1. **Download and curate** county-level files:
   - ACS 5-year (2019-2023) - ~50 key variables
   - CDC PLACES 2024 - all 40 measures
   - SVI 2022 - all themes + overall score
   - FIPS/CBSA crosswalk

2. **Create data loader skill**:
   - Claude reads CSV when user specifies a county
   - Falls back to synthesis if county not found (shouldn't happen)
   - Provides exact values with confidence

3. **Update skills** to indicate data source:
   ```
   "Based on 2023 ACS 5-year estimates, Harris County has..."
   vs.
   "Based on statistical modeling, this rural county likely has..."
   ```

**Estimated Effort**: 2-3 sessions  
**Repository Impact**: +5 MB

### Phase 2: Tract-Level Embedding (Optional)

1. **Add tract-level files** (large but manageable)
2. **Enable neighborhood-level queries**
3. **Support trial site feasibility** at catchment area level

**Estimated Effort**: 1-2 sessions  
**Repository Impact**: +100 MB (consider git LFS)

### Phase 3: API Integration (Future)

1. **Build Census API MCP server**
2. **Enable block-group queries** via runtime lookup
3. **Cache frequently accessed areas**

**Estimated Effort**: 3-5 sessions  
**Repository Impact**: Minimal (code only)

---

## Data Gaps Requiring Synthesis

Even with embedded data, some queries will require synthesis:

| Gap | Reason | Synthesis Approach |
|-----|--------|-------------------|
| **Sub-county health indicators** | PLACES is model-based, has uncertainty | Use tract estimates with confidence intervals |
| **Future projections** | Data is historical | Apply growth rates, aging models |
| **Condition co-occurrence** | Aggregate data, not individual | Use epidemiological correlation matrices |
| **Insurance plan mix** | ACS has coverage type, not specific plans | Use market share data + regional patterns |
| **Provider density** | Not in these datasets | Requires NPPES/CMS data (NetworkSim scope) |
| **Specific ethnic subgroups** | ACS has broad categories | Synthesize based on geography patterns |

---

## File Format Recommendations

### CSV Structure (for embedding)

```csv
fips,state_fips,county_name,state_abbr,population,median_age,pct_male,pct_female,pct_white,pct_black,pct_hispanic,median_income,pct_poverty,pct_uninsured,diabetes_crude_prev,obesity_crude_prev,svi_overall,svi_theme1,svi_theme2,svi_theme3,svi_theme4
48201,48,Harris County,TX,4731145,33.8,49.7,50.3,30.2,19.7,43.1,62100,15.2,18.3,12.1,32.4,0.72,0.68,0.71,0.82,0.65
```

### JSON Structure (alternative for richer metadata)

```json
{
  "fips": "48201",
  "name": "Harris County",
  "state": "TX",
  "demographics": {
    "population": 4731145,
    "median_age": 33.8,
    "sex": {"male": 49.7, "female": 50.3},
    "race": {"white": 30.2, "black": 19.7, "hispanic": 43.1}
  },
  "economics": {
    "median_income": 62100,
    "poverty_rate": 15.2
  },
  "health": {
    "source": "CDC PLACES 2024",
    "diabetes_prevalence": 12.1,
    "obesity_prevalence": 32.4
  },
  "sdoh": {
    "svi_overall": 0.72,
    "svi_themes": [0.68, 0.71, 0.82, 0.65]
  },
  "data_vintage": {
    "acs": "2019-2023",
    "places": "2024",
    "svi": "2022"
  }
}
```

---

## Summary: The Data Availability Spectrum

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    POPULATIONSIM DATA SPECTRUM                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  EMBEDDED (EXACT)              API (EXACT)           SYNTHESIZED        │
│  ─────────────────            ──────────────        ──────────────      │
│  • County demographics        • Block group ADI     • Future projections│
│  • County health indicators   • Real-time ACS       • Individual-level  │
│  • County SVI                 • Historical trends   • Co-occurrence     │
│  • Metro area profiles        • ZCTA lookup         • Provider density  │
│  • Tract data (if Tier 2)                           • Plan market share │
│                                                                         │
│  ◄────────── ACCURACY ──────────►                                       │
│  HIGH                         HIGH                  MODERATE            │
│                                                                         │
│  ◄────────── LATENCY ──────────►                                        │
│  INSTANT                      SECONDS               INSTANT             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Next Steps

1. **Decision Point**: Approve Tier 1 embedding (~5 MB, county-level)
2. **Data Acquisition**: Download and validate source files
3. **Schema Design**: Finalize CSV/JSON structure
4. **Loader Skill**: Create skill for Claude to read embedded data
5. **Documentation**: Update skills to indicate data provenance

Would you like to proceed with Phase 1 (county-level embedding)?
