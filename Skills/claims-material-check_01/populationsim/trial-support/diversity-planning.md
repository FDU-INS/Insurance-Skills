---
name: diversity-planning
description: >
  Plan for diverse clinical trial enrollment meeting FDA requirements and
  reflecting disease epidemiology. Uses PopulationSim v2.0 embedded CDC SVI data
  for minority population % by geography. Triggers: "diversity requirements",
  "minority enrollment", "representative sample", "diversity action plan".
version: "2.0"
---

# Diversity Planning Skill

## Overview

The diversity-planning skill supports development of FDA-compliant diversity action plans by analyzing disease epidemiology, identifying high-potential sites for minority enrollment, and setting realistic diversity targets based on population data.

**Primary Use Cases**:
- FDA Diversity Action Plan development
- Site selection for diversity
- Enrollment target setting by demographic
- Geographic strategy for representation

---

## Trigger Phrases

- "Diversity plan for [condition] trial"
- "How to enroll more minorities for [trial]?"
- "Diversity requirements for [condition]"
- "Representative enrollment targets"
- "Sites with high minority populations"

---

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `condition` | string | Yes | - | Target condition |
| `target_enrollment` | int | No | 500 | Total enrollment |
| `geography` | string | No | "national" | Geographic scope |
| `phase` | string | No | "Phase 3" | Trial phase |

---

## Data Sources (Embedded v2.0)

Diversity planning uses SVI and PLACES data for evidence-based demographic targeting:

| Data Source | File | Application |
|-------------|------|-------------|
| CDC SVI (County) | `data/county/svi_county_2022.csv` | EP_MINRTY (minority %), demographic breakdown |
| CDC SVI (Tract) | `data/tract/svi_tract_2022.csv` | Granular minority population for site catchment |
| CDC PLACES (County) | `data/county/places_county_2024.csv` | Disease prevalence by geography |
| Geography Crosswalks | `data/crosswalks/*.csv` | FIPS to metro area mapping |

### Data-Driven Diversity Targeting

```python
# Find high-diversity metros for trial sites:
for county in us_counties:
    minority_pct = lookup(svi_county, county.fips, 'EP_MINRTY')
    disease_prev = lookup(places_county, county.fips, 'DIABETES_CrudePrev')
    
    # Calculate minority disease population
    minority_eligible = county.population * minority_pct * disease_prev
    
    if minority_pct > 0.50 and minority_eligible > 10000:
        high_diversity_sites.append(county)

# Result: Evidence-based list for FDA Diversity Action Plan
```

### Provenance for FDA Submission

```json
{
  "diversity_plan": {
    "target_minority_enrollment": 0.45,
    "data_provenance": {
      "demographic_source": "CDC_SVI_2022",
      "prevalence_source": "CDC_PLACES_2024",
      "methodology": "Population-weighted minority disease burden",
      "file_references": [
        "populationsim/data/county/svi_county_2022.csv",
        "populationsim/data/county/places_county_2024.csv"
      ]
    }
  }
}
```

---

## FDA Diversity Requirements (2024)

### Diversity Action Plan Components

1. **Enrollment Goals**
   - Demographic-specific targets
   - Based on disease epidemiology
   - Justified deviations documented

2. **Enrollment Strategies**
   - Site selection rationale
   - Community engagement plans
   - Barrier mitigation approaches

3. **Enrollment Tracking**
   - Real-time demographic monitoring
   - Adjustment triggers
   - Contingency plans

### Required Demographics

| Category | Subgroups |
|----------|-----------|
| **Sex** | Male, Female |
| **Age** | Pediatric (<18), Adult (18-64), Older Adult (65+) |
| **Race** | American Indian/Alaska Native, Asian, Black, Native Hawaiian/Pacific Islander, White, Multiple |
| **Ethnicity** | Hispanic/Latino, Not Hispanic/Latino |

---

## Disease-Specific Diversity Targets

### Type 2 Diabetes
| Group | US Prevalence | Recommended Target |
|-------|---------------|-------------------|
| White NH | 7.4% | 45-50% |
| Black | 12.1% | 18-22% |
| Hispanic | 12.1% | 22-26% |
| Asian | 9.5% | 6-10% |
| AIAN | 14.5% | 2-4% |

### Heart Failure
| Group | US Prevalence | Recommended Target |
|-------|---------------|-------------------|
| White NH | 5.8% | 55-60% |
| Black | 9.0% | 22-28% |
| Hispanic | 4.2% | 10-14% |
| Asian | 3.8% | 4-6% |

### Alzheimer's Disease
| Group | Prevalence (65+) | Recommended Target |
|-------|-----------------|-------------------|
| White NH | 10% | 50-55% |
| Black | 19% | 20-25% |
| Hispanic | 14% | 15-20% |
| Asian | 8% | 5-8% |

### Lupus (SLE)
| Group | Prevalence | Recommended Target |
|-------|------------|-------------------|
| White NH Female | 0.05% | 25-30% |
| Black Female | 0.20% | 40-45% |
| Hispanic Female | 0.10% | 15-20% |
| Asian Female | 0.08% | 8-12% |

---

## Output Schema

```json
{
  "diversity_plan": {
    "trial_context": {
      "condition": "E11",
      "condition_name": "Type 2 Diabetes",
      "phase": "Phase 3",
      "target_enrollment": 600,
      "geography": "United States"
    },
    
    "epidemiology_basis": {
      "source": "CDC_NHANES_2022",
      "overall_prevalence": 0.115,
      "prevalence_by_group": {
        "white_nh": { "prevalence": 0.074, "population": 16500000 },
        "black": { "prevalence": 0.121, "population": 4200000 },
        "hispanic": { "prevalence": 0.121, "population": 5800000 },
        "asian": { "prevalence": 0.095, "population": 1200000 },
        "aian": { "prevalence": 0.145, "population": 180000 }
      }
    },
    
    "enrollment_targets": {
      "by_race_ethnicity": {
        "white_nh": { "target_pct": 0.48, "target_n": 288, "range": [270, 306] },
        "black": { "target_pct": 0.20, "target_n": 120, "range": [108, 132] },
        "hispanic": { "target_pct": 0.24, "target_n": 144, "range": [132, 156] },
        "asian": { "target_pct": 0.06, "target_n": 36, "range": [30, 42] },
        "other": { "target_pct": 0.02, "target_n": 12, "range": [6, 18] }
      },
      "by_sex": {
        "male": { "target_pct": 0.48, "target_n": 288 },
        "female": { "target_pct": 0.52, "target_n": 312 }
      },
      "by_age": {
        "18_44": { "target_pct": 0.15, "target_n": 90 },
        "45_64": { "target_pct": 0.45, "target_n": 270 },
        "65_plus": { "target_pct": 0.40, "target_n": 240 }
      }
    },
    
    "site_strategy": {
      "total_sites": 30,
      "distribution": {
        "high_minority_sites": {
          "count": 12,
          "pct_enrollment": 0.45,
          "target_minority_pct": 0.65
        },
        "moderate_diversity_sites": {
          "count": 12,
          "pct_enrollment": 0.40,
          "target_minority_pct": 0.35
        },
        "academic_centers": {
          "count": 6,
          "pct_enrollment": 0.15,
          "target_minority_pct": 0.40
        }
      }
    },
    
    "high_potential_sites": {
      "for_black_enrollment": [
        {
          "metro": "Atlanta, GA",
          "black_diabetic_pop": 185000,
          "recommended_sites": 2,
          "expected_contribution": 25
        },
        {
          "metro": "Detroit, MI",
          "black_diabetic_pop": 142000,
          "recommended_sites": 2,
          "expected_contribution": 20
        },
        {
          "metro": "Chicago, IL (South Side)",
          "black_diabetic_pop": 98000,
          "recommended_sites": 1,
          "expected_contribution": 12
        }
      ],
      "for_hispanic_enrollment": [
        {
          "metro": "Houston, TX",
          "hispanic_diabetic_pop": 248000,
          "recommended_sites": 3,
          "expected_contribution": 35
        },
        {
          "metro": "Los Angeles, CA",
          "hispanic_diabetic_pop": 312000,
          "recommended_sites": 2,
          "expected_contribution": 28
        },
        {
          "metro": "Miami, FL",
          "hispanic_diabetic_pop": 186000,
          "recommended_sites": 2,
          "expected_contribution": 22
        }
      ],
      "for_asian_enrollment": [
        {
          "metro": "San Francisco Bay Area",
          "asian_diabetic_pop": 82000,
          "recommended_sites": 2,
          "expected_contribution": 15
        },
        {
          "metro": "New York City",
          "asian_diabetic_pop": 68000,
          "recommended_sites": 1,
          "expected_contribution": 8
        }
      ]
    },
    
    "barrier_mitigation": {
      "transportation": {
        "strategy": "Rideshare reimbursement + NEMT partnership",
        "budget": 75000,
        "impact": "+15% retention diverse sites"
      },
      "language": {
        "strategy": "Spanish and Mandarin translations, bilingual coordinators",
        "budget": 50000,
        "sites_affected": 8
      },
      "trust": {
        "strategy": "Community advisory board, partnership with FQHCs",
        "budget": 40000,
        "community_partners": 5
      },
      "schedule": {
        "strategy": "Evening and weekend visits, home health options",
        "budget": 60000,
        "impact": "+20% enrollment working adults"
      }
    },
    
    "monitoring_plan": {
      "frequency": "Bi-weekly",
      "metrics": [
        "Screened by race/ethnicity",
        "Enrolled by race/ethnicity",
        "Screen failure rate by group",
        "Site-level diversity index"
      ],
      "triggers": {
        "yellow": "Any group >15% below target at 50% enrollment",
        "red": "Any group >25% below target at 50% enrollment"
      },
      "contingency_actions": [
        "Activate backup diverse sites",
        "Increase outreach budget",
        "Extend enrollment period"
      ]
    }
  },
  
  "metadata": {
    "fda_guidance_version": "2024",
    "generated_at": "2024-12-23T10:00:00Z"
  }
}
```

---

## Examples

### Example 1: Comprehensive Diversity Plan

**Request**: "Diversity plan for a 400-subject heart failure trial"

**Response**:

**Heart Failure Trial Diversity Action Plan**

**Epidemiologic Basis**:
| Group | HF Prevalence | % of HF Pop | Target (n=400) |
|-------|---------------|-------------|----------------|
| White NH | 5.8% | 58% | 232 (58%) |
| Black | 9.0% | 26% | **104 (26%)** |
| Hispanic | 4.2% | 10% | 40 (10%) |
| Asian | 3.8% | 4% | 16 (4%) |
| Other | - | 2% | 8 (2%) |

**Key Target**: 26% Black enrollment (vs historical 8%)

**Site Strategy** (25 sites):

| Region | Sites | Focus | Expected Contribution |
|--------|-------|-------|----------------------|
| Southeast | 8 | High Black | 35% of Black enrollment |
| Texas | 5 | Hispanic | 40% of Hispanic enrollment |
| Midwest | 6 | Mixed | General population |
| Northeast | 4 | Urban diversity | 25% of Black, Asian |
| West | 2 | Hispanic, Asian | 30% of each |

**High-Priority Sites for Black Enrollment**:
1. Emory (Atlanta) - 30,000 Black HF patients in catchment
2. Johns Hopkins (Baltimore) - 25,000 Black HF patients
3. Duke (Durham) - 18,000 Black HF patients
4. Morehouse (Atlanta) - HBCU partnership

**Barrier Mitigation**:
- $100K transportation budget
- CHW program at 6 sites
- Church/community partnerships

---

### Example 2: Hispanic Enrollment Strategy

**Request**: "How to improve Hispanic enrollment for our NAFLD trial?"

**Response**:

**Hispanic Enrollment Enhancement Strategy**

**Challenge**: NAFLD/NASH prevalence highest in Hispanic populations (24% vs 15% White NH) but historically under-enrolled.

**Target**: 35% Hispanic (reflecting epidemiology)

**Geographic Hotspots**:
| Metro | Hispanic NAFLD Est. | Recommended Sites |
|-------|---------------------|-------------------|
| Los Angeles | 580,000 | 3 sites |
| Houston | 420,000 | 2 sites |
| San Antonio | 280,000 | 2 sites |
| Phoenix | 240,000 | 1 site |
| Miami | 320,000 | 2 sites |

**Barrier Analysis**:
| Barrier | % Affected | Mitigation |
|---------|------------|------------|
| Language | 32% | Spanish materials, bilingual staff |
| Transportation | 28% | Rideshare, site in community |
| Work schedule | 42% | Evening/weekend visits |
| Trust/cultural | 25% | CHW outreach, FQHC partnership |
| Insurance fear | 18% | Clear messaging, undocumented-friendly |

**Site Recommendations**:
1. **Community health centers**: 4 FQHCs with high Hispanic populations
2. **Academic with Spanish programs**: UT Health SA, UCLA, U Miami
3. **Hybrid model**: Academic hub + community satellite clinics

**Budget Impact**: +$180K for comprehensive program

---

### Example 3: Multi-Condition Analysis

**Request**: "Compare diversity needs across DM, HTN, and CKD trials"

**Response**:

**Diversity Target Comparison**

| Group | Diabetes | HTN | CKD | Rationale |
|-------|----------|-----|-----|-----------|
| White NH | 48% | 52% | 50% | Lower relative burden |
| Black | 20% | **28%** | **26%** | Highest HTN, CKD disparity |
| Hispanic | 24% | 15% | 18% | High DM, moderate others |
| Asian | 6% | 4% | 5% | Moderate prevalence |
| Other | 2% | 1% | 1% | Small populations |

**Key Insights**:

**Hypertension**:
- Black adults have highest HTN prevalence (56% vs 48% White)
- Target 28% Black enrollment (often under 10% historically)
- Southeast sites critical

**CKD**:
- Black patients 3x more likely to progress to ESRD
- 26% Black target reflects burden
- Nephrology specialty sites needed

**Diabetes**:
- Most equitable distribution needed
- Hispanic/Black together should be ~44%
- Community health centers effective

**Shared Strategies**:
- 8 sites can serve all three conditions
- Southeast/Southwest regional priority
- CHW programs scale across trials

---

## Best Practices

### Site Selection
1. ✅ Select sites in high-minority geographies
2. ✅ Include FQHCs and community health centers
3. ✅ Partner with minority-serving institutions
4. ❌ Don't rely solely on large academic centers

### Protocol Design
1. ✅ Minimize exclusions that disproportionately affect minorities
2. ✅ Flexible visit schedules
3. ✅ Allow home visits and telehealth
4. ❌ Don't require excessive office visits

### Operational
1. ✅ Bilingual materials and staff
2. ✅ Transportation support
3. ✅ Community advisory boards
4. ❌ Don't start enrollment without diversity infrastructure

---

## Validation Rules

### Input Validation
- Condition must have epidemiologic data
- Target enrollment > 0
- Geography valid

### Output Validation
- [ ] Targets sum to 100%
- [ ] Targets reflect epidemiology
- [ ] Site strategy supports targets
- [ ] Barriers addressed

---

## Related Skills

- [site-selection-support.md](site-selection-support.md) - Site-level demographics
- [enrollment-projection.md](enrollment-projection.md) - Timeline impact
- [health-outcome-disparities.md](../health-patterns/health-outcome-disparities.md) - Disparity data
- [county-profile.md](../geographic/county-profile.md) - Geographic demographics
