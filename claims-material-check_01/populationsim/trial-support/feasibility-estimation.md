---
name: feasibility-estimation
description: >
  Estimate eligible patient populations for clinical trial protocols based on
  inclusion/exclusion criteria. Uses disease prevalence, demographics, and
  clinical characteristics to model the eligibility funnel. Supports PopulationSim
  v2.0 embedded data for real CDC PLACES prevalence rates. Triggers: "feasibility",
  "eligible population", "how many patients qualify", "protocol feasibility".
version: "2.0"
---

# Feasibility Estimation Skill

## Overview

The feasibility-estimation skill calculates eligible patient populations for clinical trial protocols by applying inclusion/exclusion criteria to population-level epidemiologic data. It models the eligibility funnel from disease prevalence through final eligible population.

**Primary Use Cases**:
- Protocol feasibility assessment
- Sample size planning support
- Geographic targeting for site selection
- Competitive landscape analysis
- Diversity target setting

---

## Trigger Phrases

- "Estimate feasibility for [protocol/indication]"
- "How many patients are eligible for [trial]?"
- "Feasibility analysis for [criteria]"
- "Eligible population for diabetes trial"
- "Calculate screening pool for [protocol]"

---

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `indication` | string | Yes | - | Primary condition (ICD-10 or name) |
| `inclusion` | object | Yes | - | Inclusion criteria |
| `exclusion` | object | No | {} | Exclusion criteria |
| `geography` | string/array | No | "national" | Geographic scope |
| `diversity_requirements` | object | No | - | Enrollment targets by demographic |

---

## Data Sources (Embedded v2.0)

When geography is specified, feasibility estimation uses real CDC PLACES and SVI data:

| Data Source | File | Key Measures |
|-------------|------|-------------|
| CDC PLACES (County) | `data/county/places_county_2024.csv` | DIABETES_CrudePrev, OBESITY_CrudePrev, BPHIGH_CrudePrev |
| CDC PLACES (Tract) | `data/tract/places_tract_2024.csv` | All 36 health measures at tract level |
| CDC SVI (County) | `data/county/svi_county_2022.csv` | RPL_THEMES, EP_MINRTY, EP_UNINSUR |
| CDC SVI (Tract) | `data/tract/svi_tract_2022.csv` | All SVI themes for retention modeling |

### Data-Driven Feasibility Pattern

```python
# Instead of generic national prevalence:
diabetes_national = 0.102  # Generic

# Look up actual county-level prevalence:
from data/county/places_county_2024.csv where CountyFIPS = '48201':
  DIABETES_CrudePrev = 12.1%  # Harris County actual rate
  OBESITY_CrudePrev = 32.8%
  BPHIGH_CrudePrev = 32.4%

# Apply to site catchment population for accurate eligible counts
```

### Provenance Tracking

Feasibility outputs include data source attribution:

```json
{
  "data_provenance": {
    "prevalence_source": "CDC_PLACES_2024",
    "prevalence_year": 2022,
    "svi_source": "CDC_SVI_2022",
    "geography_level": "county",
    "file_reference": "populationsim/data/county/places_county_2024.csv"
  }
}
```

---

## Eligibility Funnel Model

### Standard Funnel Stages

```
Stage 1: Disease Prevalence
    ↓ (apply age filter)
Stage 2: Age-Eligible
    ↓ (apply clinical criteria)
Stage 3: Clinically Eligible
    ↓ (apply exclusions)
Stage 4: Protocol Eligible
    ↓ (apply geographic constraints)
Stage 5: Geographically Accessible
    ↓ (estimate reachable)
Stage 6: Likely Screenable
```

### Typical Conversion Rates

| Transition | Typical Rate | Varies By |
|------------|--------------|-----------|
| Prevalent → Age-Eligible | 70-95% | Protocol age range |
| Age → Clinical Criteria | 30-60% | Specificity of criteria |
| Clinical → After Exclusions | 60-85% | Exclusion stringency |
| Eligible → Accessible | 40-70% | Site network |
| Accessible → Screenable | 3-8%/year | Awareness, motivation |

---

## Output Schema

```json
{
  "feasibility_analysis": {
    "protocol_id": "DIABETES-001",
    "analysis_date": "2024-12-23",
    
    "indication": {
      "code": "E11",
      "name": "Type 2 Diabetes Mellitus",
      "national_prevalence": 0.102,
      "prevalent_population": 34200000
    },
    
    "criteria_applied": {
      "inclusion": {
        "age_range": [18, 75],
        "confirmed_diagnosis": "E11",
        "hba1c_range": [7.5, 10.5],
        "on_metformin": true,
        "willing_to_consent": true
      },
      "exclusion": {
        "ckd_stage_4_5": ["N18.4", "N18.5", "N18.6"],
        "recent_cv_event": "I21 within 6 months",
        "current_insulin": true,
        "pregnancy": "O09, Z33",
        "active_malignancy": "C00-C96"
      }
    },
    
    "funnel": {
      "stage_1_prevalent": {
        "population": 34200000,
        "pct_of_us": 0.102,
        "notes": "CDC 2022 diabetes prevalence"
      },
      "stage_2_age_eligible": {
        "population": 28400000,
        "conversion": 0.83,
        "notes": "Age 18-75 restriction"
      },
      "stage_3_hba1c_eligible": {
        "population": 12800000,
        "conversion": 0.45,
        "notes": "HbA1c 7.5-10.5% (~45% of diabetics)"
      },
      "stage_4_on_metformin": {
        "population": 9200000,
        "conversion": 0.72,
        "notes": "72% of T2DM on metformin"
      },
      "stage_5_after_exclusions": {
        "population": 6800000,
        "conversion": 0.74,
        "breakdown": {
          "ckd_4_5_excluded": 820000,
          "recent_cv_excluded": 460000,
          "on_insulin_excluded": 920000,
          "other_excluded": 200000
        }
      },
      "stage_6_final_eligible": {
        "population": 6800000,
        "pct_of_prevalent": 0.199,
        "notes": "National eligible pool"
      }
    },
    
    "geographic_distribution": {
      "by_region": {
        "south": { "population": 2584000, "pct": 0.38 },
        "west": { "population": 1632000, "pct": 0.24 },
        "midwest": { "population": 1360000, "pct": 0.20 },
        "northeast": { "population": 1224000, "pct": 0.18 }
      },
      "top_states": [
        { "state": "TX", "eligible": 748000, "pct": 0.11 },
        { "state": "FL", "eligible": 680000, "pct": 0.10 },
        { "state": "CA", "eligible": 612000, "pct": 0.09 },
        { "state": "NY", "eligible": 476000, "pct": 0.07 },
        { "state": "PA", "eligible": 340000, "pct": 0.05 }
      ],
      "top_metros": [
        { "metro": "Houston", "eligible": 185000 },
        { "metro": "Miami", "eligible": 168000 },
        { "metro": "Los Angeles", "eligible": 156000 },
        { "metro": "Dallas", "eligible": 142000 },
        { "metro": "Phoenix", "eligible": 128000 }
      ]
    },
    
    "demographic_profile": {
      "age": {
        "18-44": 0.18,
        "45-54": 0.24,
        "55-64": 0.32,
        "65-75": 0.26
      },
      "sex": {
        "male": 0.52,
        "female": 0.48
      },
      "race_ethnicity": {
        "white_nh": 0.52,
        "black": 0.18,
        "hispanic": 0.22,
        "asian": 0.06,
        "other": 0.02
      }
    },
    
    "diversity_analysis": {
      "disease_burden_by_race": {
        "white_nh": { "prevalence": 0.088, "representation": 0.52 },
        "black": { "prevalence": 0.128, "representation": 0.18 },
        "hispanic": { "prevalence": 0.122, "representation": 0.22 },
        "asian": { "prevalence": 0.094, "representation": 0.06 }
      },
      "recommended_targets": {
        "minority_total": 0.40,
        "black": 0.15,
        "hispanic": 0.20
      }
    },
    
    "screening_projections": {
      "assumptions": {
        "awareness_rate": 0.05,
        "willingness_rate": 0.60,
        "screen_to_enroll": 0.35
      },
      "annual_screen_pool": {
        "national": 204000,
        "per_site_40_sites": 5100
      },
      "enrollment_potential": {
        "annual_national": 71400,
        "per_site_40_sites": 1785
      }
    },
    
    "competitive_landscape": {
      "active_trials_same_indication": 42,
      "recruiting_trials": 28,
      "estimated_competition_sites": 850,
      "competition_intensity": "moderate"
    },
    
    "confidence": {
      "overall": "high",
      "prevalence_data": "CDC_2022",
      "clinical_criteria_estimates": "literature_derived",
      "notes": "Large indication with robust epidemiologic data"
    }
  }
}
```

---

## Examples

### Example 1: Diabetes Trial Feasibility

**Request**: "Feasibility for T2DM trial: age 40-70, HbA1c 8-11%, on oral agents only"

**Response**:

**T2DM Trial Feasibility Analysis**

**Eligibility Funnel**:
| Stage | Population | Conversion |
|-------|------------|------------|
| T2DM Prevalent | 34.2M | - |
| Age 40-70 | 24.8M | 72.5% |
| HbA1c 8-11% | 7.4M | 29.8% |
| Oral agents only | 5.0M | 67.6% |
| After exclusions | 4.2M | 84.0% |

**Final Eligible**: 4.2 million nationally

**Top Metros by Eligible Population**:
| Metro | Eligible | Diversity Score |
|-------|----------|-----------------|
| Houston | 128,000 | 0.84 |
| Miami | 115,000 | 0.78 |
| Los Angeles | 108,000 | 0.82 |
| Dallas | 98,000 | 0.76 |
| Chicago | 92,000 | 0.72 |

**Demographic Profile**:
- Mean Age: 56.4 years
- Male: 54%
- White NH: 48%, Black: 20%, Hispanic: 24%, Asian: 6%

**Enrollment Projection** (40 sites):
- Eligible per site catchment: ~3,000
- Annual screen potential: ~150/site
- Expected enrollment: ~52/site/year
- Time to 2,000 subjects: ~10 months

---

### Example 2: Rare Disease Feasibility

**Request**: "Feasibility for NASH with fibrosis F2-F3, age 18-70"

**Response**:

**NASH F2-F3 Feasibility Analysis**

**Eligibility Funnel**:
| Stage | Population | Conversion |
|-------|------------|------------|
| NAFLD Prevalent | 80-100M | - |
| NASH (subset) | 16-20M | 20% |
| Age 18-70 | 14.4M | 80% |
| Fibrosis F2-F3 | 2.9M | 20% |
| Diagnosed/aware | 580,000 | 20% ⚠️ |
| After exclusions | 490,000 | 85% |

**Challenge**: Low diagnosis rate

**Final Eligible**: ~490,000 (diagnosed)
**True Eligible** (if diagnosed): 2.5M

**Geographic Concentration**:
- South: 42% (higher obesity/metabolic syndrome)
- Texas, Florida, California: Top 3 states

**Site Strategy Recommendation**:
- Target hepatology centers
- Partner with bariatric programs
- Screen metabolic syndrome patients
- Consider imaging-based screening

---

### Example 3: Pediatric Feasibility

**Request**: "Feasibility for pediatric asthma trial, age 6-17, moderate-severe"

**Response**:

**Pediatric Asthma Feasibility**

**Eligibility Funnel**:
| Stage | Population | Conversion |
|-------|------------|------------|
| Pediatric asthma | 5.1M | - |
| Age 6-17 | 4.2M | 82% |
| Moderate-Severe | 1.05M | 25% |
| Uncontrolled | 420,000 | 40% |
| After exclusions | 360,000 | 86% |

**Final Eligible**: 360,000 nationally

**Geographic Distribution**:
| Region | Eligible | Key Metros |
|--------|----------|------------|
| Northeast | 82,000 | NYC, Boston, Philadelphia |
| South | 115,000 | Houston, Atlanta, Miami |
| Midwest | 72,000 | Chicago, Detroit |
| West | 91,000 | LA, Phoenix, Seattle |

**Special Considerations**:
- Parent/guardian consent required
- School schedule impacts
- Higher minority prevalence (Black, Hispanic)
- Urban vs rural access

**Diversity Opportunity**:
- Black children: 16% of asthma (vs 13% general pediatric)
- Hispanic children: 22%
- Target urban pediatric centers

---

## Validation Rules

### Input Validation
- [ ] Indication is valid ICD-10 or recognized name
- [ ] Age range valid (min < max)
- [ ] Criteria are assessable

### Output Validation
- [ ] Funnel populations decrease monotonically
- [ ] Conversion rates between 0 and 1
- [ ] Geographic distribution sums to ~1.0
- [ ] Demographics sum to ~1.0

### Plausibility Checks
- [ ] Final eligible is reasonable fraction of prevalent
- [ ] Exclusion impact clinically plausible
- [ ] Geographic distribution matches disease epidemiology

---

## Related Skills

- [site-selection-support.md](site-selection-support.md) - Site recommendations
- [enrollment-projection.md](enrollment-projection.md) - Timeline projections
- [chronic-disease-prevalence.md](../health-patterns/chronic-disease-prevalence.md) - Prevalence source
- [cohort-specification.md](../cohorts/cohort-specification.md) - Trial cohort definition
