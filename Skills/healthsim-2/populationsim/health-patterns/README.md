---
name: populationsim-health-patterns
description: >
  Health pattern analysis skills for PopulationSim. Use for chronic disease
  prevalence, health behaviors, healthcare access assessment, and health
  disparities analysis. Primary data source is CDC PLACES.
---

# Health Pattern Analysis Skills

## Overview

Health pattern analysis skills provide detailed analysis of disease prevalence, health behaviors, healthcare access, and outcome disparities across geographic areas. These skills primarily leverage CDC PLACES data, which provides model-based estimates for 27 health measures at both county and census tract levels.

**Key Capability**: Transform geographic areas into detailed health profiles that inform cohort definition and synthetic data generation.

---

## Skills in This Category

| Skill | Purpose | Key Triggers |
|-------|---------|--------------|
| [chronic-disease-prevalence.md](chronic-disease-prevalence.md) | Disease prevalence analysis | "diabetes rate", "prevalence", "disease burden" |
| [health-behavior-patterns.md](health-behavior-patterns.md) | Risk behavior analysis | "smoking", "obesity", "physical activity" |
| [healthcare-access-analysis.md](healthcare-access-analysis.md) | Access and coverage assessment | "uninsured", "provider ratio", "access barriers" |
| [health-outcome-disparities.md](health-outcome-disparities.md) | Disparity and equity analysis | "disparities", "by race", "health equity" |

---

## CDC PLACES Measures

All 27 measures available in CDC PLACES:

### Health Outcomes (13)
| Measure | Variable | Age Group |
|---------|----------|-----------|
| Arthritis | ARTHRITIS | 18+ |
| Current Asthma | CASTHMA | 18+ |
| High Blood Pressure | BPHIGH | 18+ |
| Cancer (excl. skin) | CANCER | 18+ |
| High Cholesterol | HIGHCHOL | 18+ |
| Chronic Kidney Disease | KIDNEY | 18+ |
| COPD | COPD | 18+ |
| Coronary Heart Disease | CHD | 18+ |
| Depression | DEPRESSION | 18+ |
| Diabetes | DIABETES | 18+ |
| Obesity | OBESITY | 18+ |
| Stroke | STROKE | 18+ |
| Poor Mental Health 14+ days | MHLTH | 18+ |
| Poor Physical Health 14+ days | PHLTH | 18+ |

### Prevention (9)
| Measure | Variable | Age Group |
|---------|----------|-----------|
| Annual Checkup | CHECKUP | 18+ |
| Dental Visit | DENTAL | 18+ |
| Cholesterol Screening | CHOLSCREEN | 18+ |
| Colorectal Cancer Screening | COLON_SCREEN | 45-75 |
| Core Preventive Services (Men) | COREM | 65+ |
| Core Preventive Services (Women) | COREW | 65+ |
| Mammography | MAMMOUSE | 50-74 (women) |
| Cervical Cancer Screening | PAPTEST | 21-65 (women) |

### Health Risk Behaviors (4)
| Measure | Variable | Age Group |
|---------|----------|-----------|
| Binge Drinking | BINGE | 18+ |
| Current Smoking | CSMOKING | 18+ |
| Physical Inactivity | LPA | 18+ |
| Sleep Less Than 7 Hours | SLEEP | 18+ |

### Health Status (1)
| Measure | Variable | Age Group |
|---------|----------|-----------|
| Fair/Poor Self-Rated Health | GHLTH | 18+ |

---

## Age Adjustment

All CDC PLACES measures are **age-adjusted** using direct standardization to the 2000 US standard population. This enables fair comparisons across geographies with different age structures.

**Why This Matters**:
- Florida (median age 42) vs Utah (median age 31)
- Without adjustment, Florida appears less healthy
- Age-adjusted rates reveal true health differences

**Standard Population Weights**:
| Age Group | Weight |
|-----------|--------|
| 18-24 | 0.1283 |
| 25-34 | 0.1810 |
| 35-44 | 0.1994 |
| 45-54 | 0.1721 |
| 55-64 | 0.1272 |
| 65+ | 0.1920 |

---

## Integration Points

### → Cohort Definition

Health patterns inform clinical profiles in CohortSpecification:

```json
{
  "clinical_profile": {
    "primary_condition": "E11",
    "comorbidities": {
      "hypertension": 0.71,
      "obesity": 0.62,
      "depression": 0.28
    }
  }
}
```

### → PatientSim

Health prevalence rates drive diagnosis assignment:
- County diabetes rate 12% → 12% of patients assigned E11.x
- Comorbidity rates from CDC PLACES inform multi-diagnosis patients

### → TrialSim

Disease prevalence informs recruitment feasibility:
- High diabetes prevalence → Better recruitment for diabetes trials
- Prevalence × population = Estimated disease population

---

## Data Quality Notes

### Methodology
- CDC PLACES uses multilevel regression with poststratification (MRP)
- Model inputs: BRFSS survey data + ACS demographics
- Output: Small area estimates for counties and tracts

### Reliability
| Geography | Population | Reliability |
|-----------|------------|-------------|
| County | > 100,000 | High |
| County | 20,000-100,000 | Moderate |
| County | < 20,000 | Use with caution |
| Tract | > 2,000 | Moderate |
| Tract | < 2,000 | Use with caution |

### Limitations
- Model-based estimates, not direct measurement
- May not capture recent trends
- Limited by BRFSS question set
- Some measures (e.g., cancer) have wider confidence intervals

---

## Skill Selection Guide

### Use chronic-disease-prevalence.md when:
- Analyzing specific conditions (diabetes, heart disease, etc.)
- Comparing disease burden across geographies
- Assessing comorbidity patterns
- Informing clinical trial feasibility

### Use health-behavior-patterns.md when:
- Analyzing risk factors (smoking, obesity)
- Understanding modifiable health determinants
- Assessing prevention opportunities
- Correlating behaviors with outcomes

### Use healthcare-access-analysis.md when:
- Assessing insurance coverage gaps
- Analyzing provider availability
- Identifying access barriers
- Evaluating preventive care utilization

### Use health-outcome-disparities.md when:
- Analyzing health equity
- Comparing outcomes by demographic group
- Identifying disparity hotspots
- Supporting diversity planning

---

## Quick Examples

### Disease Analysis
```
"What's the diabetes prevalence in Harris County?"
→ 12.4% (vs 10.1% national), with obesity 33.8%, HTN 32.1%
```

### Behavior Analysis
```
"Compare smoking rates: Kentucky vs California"
→ KY: 22.4%, CA: 9.8%, explaining lung disease disparity
```

### Access Analysis
```
"Show uninsured rates in Texas border counties"
→ Range 18-32%, all above national 8.8%
```

### Disparity Analysis
```
"Diabetes disparities by race in Atlanta metro"
→ Black: 14.2%, Hispanic: 11.8%, White NH: 8.4%
```

---

## Related Skills

- [Geographic Intelligence](../geographic/README.md) - Geographic profiling
- [SDOH Analysis](../sdoh/README.md) - Social determinants
- [Cohort Definition](../cohorts/README.md) - Clinical profiles
- [Trial Support](../trial-support/README.md) - Feasibility analysis

---

## Data Sources

| Source | Content | Geography | Update |
|--------|---------|-----------|--------|
| CDC PLACES | 27 health measures | County, Tract | Annual |
| BRFSS | Survey data | State, some metro | Annual |
| Census ACS | Demographics | All levels | Annual |
| HRSA AHRF | Provider data | County | Annual |
