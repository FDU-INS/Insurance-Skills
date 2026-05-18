---
name: healthcare-access-analysis
description: >
  Analyze healthcare access including insurance coverage, provider availability,
  preventive care utilization, and access barriers. Triggers: "uninsured rate",
  "provider ratio", "healthcare access", "coverage", "PCP per capita",
  "access barriers", "insurance coverage".
---

# Healthcare Access Analysis Skill

## Overview

The healthcare-access-analysis skill evaluates healthcare access across geographic areas, including insurance coverage rates, provider availability, preventive care utilization, and identification of access barriers. This enables understanding of healthcare infrastructure and access challenges.

**Primary Use Cases**:
- Insurance coverage gap analysis
- Provider shortage identification
- Preventive care assessment
- Access barrier mapping
- Healthcare infrastructure planning
- Member population profiling

---

## Trigger Phrases

- "What's the uninsured rate in [geography]?"
- "How many PCPs per capita in [area]?"
- "Compare healthcare access: [A] vs [B]"
- "Insurance coverage breakdown for [geography]"
- "Access barriers in [region]"
- "Provider shortage areas"
- "Preventive care utilization in [area]"

---

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `geography` | string | Yes | - | County, tract, metro, or state |
| `focus` | string | No | "all" | "coverage", "providers", "prevention", "barriers" |
| `compare_to` | string | No | - | Geography for comparison |
| `benchmark` | string | No | "national" | Comparison benchmark |

---

## Data Sources (Embedded v2.0)

Healthcare access data comes from multiple embedded sources:

| Metric | File | Key Columns |
|--------|------|-------------|
| Uninsured Rate | `data/county/svi_county_2022.csv` | EP_UNINSUR |
| Uninsured Rate (tract) | `data/tract/svi_tract_2022.csv` | EP_UNINSUR, E_UNINSUR |
| Annual Checkup | `data/county/places_county_2024.csv` | CHECKUP_CrudePrev |
| Dental Visit | `data/county/places_county_2024.csv` | DENTAL_CrudePrev |
| Cholesterol Screening | `data/county/places_county_2024.csv` | CHOLSCREEN_CrudePrev |
| Colorectal Screening | `data/county/places_county_2024.csv` | COLON_SCREEN_CrudePrev |
| Mammography | `data/county/places_county_2024.csv` | MAMMOUSE_CrudePrev |

### Data Lookup Pattern

```
1. Identify geography type and FIPS code
2. Read SVI file for insurance coverage (EP_UNINSUR)
3. Read PLACES file for preventive care utilization
4. Compare to national/state benchmarks
5. Return with source citations
```

**Note**: Provider ratios require external data (AHRF, NPPES) not included in embedded package.

---

## Access Dimensions

### Insurance Coverage (ACS)

| Measure | Definition | National Rate |
|---------|------------|---------------|
| Uninsured | No health insurance coverage | 8.8% |
| Employer | Employer-sponsored coverage | 54.4% |
| Medicare | Medicare coverage | 14.2% |
| Medicaid | Medicaid coverage | 17.8% |
| Individual | Non-group coverage | 5.8% |
| Military | VA/TRICARE | 2.4% |

### Provider Availability (HRSA)

| Measure | Definition | Adequate Level |
|---------|------------|----------------|
| PCP per 100K | Primary care physicians | > 60 |
| Specialist per 100K | Specialists | > 100 |
| Dentist per 100K | Dentists | > 50 |
| Mental Health per 100K | MH providers | > 200 |
| Hospital Beds per 1K | Inpatient beds | > 2.0 |

### Preventive Care (CDC PLACES)

| Measure | Definition | Target |
|---------|------------|--------|
| Annual Checkup | Routine checkup past year | > 75% |
| Dental Visit | Dental visit past year | > 65% |
| Cholesterol Screen | Screening past 5 years | > 85% |
| Colorectal Screen | Up-to-date screening | > 70% |
| Mammography | Mammogram past 2 years | > 75% |

---

## Output Schema

```json
{
  "analysis_type": "healthcare_access",
  "geography": {
    "type": "county",
    "fips": "48141",
    "name": "El Paso County",
    "state": "TX"
  },
  "insurance_coverage": {
    "uninsured_rate": 0.182,
    "vs_state": 0.175,
    "vs_national": 0.088,
    "status": "significantly_above",
    "coverage_breakdown": {
      "employer": 0.428,
      "medicare": 0.118,
      "medicaid": 0.212,
      "individual": 0.042,
      "military": 0.058,
      "uninsured": 0.182
    },
    "uninsured_by_age": {
      "under_19": 0.092,
      "19_25": 0.242,
      "26_34": 0.228,
      "35_44": 0.198,
      "45_54": 0.168,
      "55_64": 0.142,
      "65_plus": 0.008
    },
    "uninsured_population": 152000
  },
  "provider_availability": {
    "pcp_per_100k": 52.4,
    "adequacy": "shortage",
    "shortage_designation": "HPSA",
    "specialist_per_100k": 98.2,
    "dentist_per_100k": 42.8,
    "mental_health_per_100k": 148.2,
    "hospital_beds_per_1k": 1.8,
    "fqhc_count": 18,
    "vs_benchmarks": {
      "pcp": { "value": 52.4, "benchmark": 76.4, "gap": -24.0 },
      "dentist": { "value": 42.8, "benchmark": 61.2, "gap": -18.4 }
    }
  },
  "preventive_care": {
    "annual_checkup": 0.722,
    "dental_visit": 0.542,
    "cholesterol_screening": 0.812,
    "colorectal_screening": 0.622,
    "mammography": 0.742,
    "vs_targets": {
      "annual_checkup": { "value": 0.722, "target": 0.75, "gap": -0.028 },
      "dental_visit": { "value": 0.542, "target": 0.65, "gap": -0.108 }
    }
  },
  "access_barriers": {
    "identified_barriers": [
      {
        "barrier": "Insurance coverage gap",
        "severity": "high",
        "affected_pct": 0.182,
        "description": "18.2% uninsured, 2x national rate"
      },
      {
        "barrier": "PCP shortage",
        "severity": "moderate",
        "affected_pct": 0.35,
        "description": "HPSA designated, 52 PCPs per 100K"
      },
      {
        "barrier": "Dental provider shortage",
        "severity": "moderate",
        "affected_pct": 0.40,
        "description": "43 dentists per 100K, below threshold"
      }
    ],
    "sdoh_barriers": {
      "transportation": 0.12,
      "language": 0.28,
      "cost": 0.24
    }
  },
  "implications": {
    "for_membersim": {
      "medicaid_pct": 0.212,
      "uninsured_pct": 0.182,
      "commercial_pct": 0.47
    },
    "for_patientsim": {
      "delayed_care_likelihood": "high",
      "ed_primary_care_rate": "elevated",
      "prevention_gap_diagnoses": ["E11.65", "I10", "Z23"]
    }
  }
}
```

---

## Examples

### Example 1: Coverage Analysis

**Request**: "Insurance coverage analysis for Texas border counties"

**Response**:

**Texas Border County Insurance Analysis**

**Summary**: Border counties have uninsured rates 2-3x national average

| County | Population | Uninsured | vs National |
|--------|------------|-----------|-------------|
| Hidalgo | 870,781 | 24.8% | +16.0% ⚠️ |
| Cameron | 423,725 | 22.4% | +13.6% ⚠️ |
| Webb | 276,652 | 21.8% | +13.0% ⚠️ |
| El Paso | 865,657 | 18.2% | +9.4% ⚠️ |
| Starr | 67,141 | 28.4% | +19.6% ⚠️ |

**Coverage Mix** (border region avg):
- Employer: 38% (vs 54% national)
- Medicaid: 28% (vs 18% national)
- Medicare: 12% (vs 14% national)
- Uninsured: 22% (vs 9% national)

**Uninsured by Age**:
- 19-25: 32% (highest)
- 26-34: 28%
- 35-44: 24%
- Children: 11%

**Key Factors**:
- Non-expansion state (Texas)
- High poverty rates (25-35%)
- Large undocumented population
- Limited employer coverage

---

### Example 2: Provider Analysis

**Request**: "Provider availability in rural Appalachia"

**Response**:

**Appalachian Rural County Provider Analysis**

**Sample Counties** (rural, population < 50K):

| Metric | Appalachian Rural | National | Gap |
|--------|-------------------|----------|-----|
| PCP per 100K | 38.2 | 76.4 | -50% |
| Specialists per 100K | 42.1 | 134.2 | -69% |
| Dentists per 100K | 28.4 | 61.2 | -54% |
| MH Providers per 100K | 82.4 | 284.0 | -71% |

**HPSA Designation**: 92% of rural Appalachian counties

**County Examples**:
| County, State | Pop | PCPs | Specialists | Dentists |
|---------------|-----|------|-------------|----------|
| McDowell, WV | 18,800 | 18 | 8 | 12 |
| Owsley, KY | 4,200 | 8 | 4 | 4 |
| Mingo, WV | 22,400 | 24 | 12 | 16 |

**Access Implications**:
- Average drive to specialist: 45-90 minutes
- Telehealth critical for access
- FQHCs serve as primary care backbone
- ED used for primary care (28% higher rate)

---

### Example 3: Preventive Care Gap

**Request**: "Preventive care utilization in Memphis metro"

**Response**:

**Memphis Metro Preventive Care Analysis**

| Measure | Memphis Metro | National | Gap |
|---------|---------------|----------|-----|
| Annual Checkup | 72.4% | 77.8% | -5.4% |
| Dental Visit | 54.2% | 66.8% | -12.6% ⚠️ |
| Cholesterol Screen | 78.4% | 86.2% | -7.8% |
| Colorectal Screen | 62.4% | 70.2% | -7.8% |
| Mammography | 71.8% | 78.4% | -6.6% |

**Variation by County**:
| County | Annual Checkup | Dental | SVI |
|--------|----------------|--------|-----|
| Shelby, TN | 71.2% | 52.4% | 0.72 |
| DeSoto, MS | 74.8% | 58.2% | 0.48 |
| Fayette, TN | 76.2% | 62.4% | 0.32 |

**Correlation with SDOH**:
- Higher SVI → Lower preventive care (r = -0.68)
- Higher uninsured → Lower checkups (r = -0.72)
- Lower income → Lower dental visits (r = 0.58)

**Intervention Priorities**:
1. Dental access (largest gap)
2. Colorectal screening (mortality impact)
3. Target high-SVI census tracts

---

## Validation Rules

### Input Validation
- Geography must be valid identifier
- Focus area must be valid option

### Output Validation
- [ ] Percentages between 0 and 1
- [ ] Provider ratios positive
- [ ] Coverage types sum to ~100%

---

## Related Skills

- [county-profile.md](../geographic/county-profile.md) - Full profiles
- [svi-analysis.md](../sdoh/svi-analysis.md) - SDOH context
- [health-outcome-disparities.md](health-outcome-disparities.md) - Access disparities
- [cohort-specification.md](../cohorts/cohort-specification.md) - Coverage mix
