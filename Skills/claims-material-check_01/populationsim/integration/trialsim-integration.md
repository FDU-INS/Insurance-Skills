---
name: trialsim-integration
description: |
  Integration guide for PopulationSim to TrialSim data flow. Describes how 
  geographic, demographic, and health data supports trial feasibility assessment, 
  site selection, and diverse subject enrollment simulation.
---

# PopulationSim → TrialSim Integration

## Overview

This document describes how PopulationSim geographic, demographic, and health data flows into TrialSim to support clinical trial feasibility assessment, site selection, and diverse subject enrollment simulation.

---

## Integration Flow

```
PopulationProfile                    TrialSim
      │                                   │
      ├─ geography ─────────────────────► Site selection
      │   └─ catchment_area              │  └─ Site feasibility
      │                                   │
      ├─ demographics ──────────────────► Diversity planning
      │   └─ race_ethnicity              │  └─ Enrollment targets
      │                                   │
      ├─ health_indicators ─────────────► Eligibility assessment
      │   └─ condition_prevalence        │  └─ Eligible pool size
      │                                   │
      └─ sdoh_profile ──────────────────► Retention modeling
          ├─ transportation              │  ├─ Visit compliance
          └─ economic_factors            │  └─ Drop-out risk
```

---

## Site Selection Support

### Catchment Area Analysis

PopulationSim provides demographic profiles for potential trial sites:

```json
// Site analysis request
{
  "sites": [
    {
      "site_id": "SITE-001",
      "name": "Houston Medical Center",
      "location": {
        "fips": "48201",
        "coordinates": {"lat": 29.7108, "lng": -95.3973}
      },
      "catchment_radius_miles": 30
    }
  ],
  "protocol": {
    "condition": "type_2_diabetes",
    "age_range": {"min": 40, "max": 75}
  }
}

// PopulationSim catchment analysis output
{
  "site_id": "SITE-001",
  "catchment_profile": {
    "total_population": 4731145,
    "age_eligible_population": 1842000,
    "condition_prevalent": 198800,
    "demographics": {
      "white_nh": 0.288,
      "black_nh": 0.198,
      "hispanic": 0.438,
      "asian_nh": 0.078
    },
    "sdoh_summary": {
      "svi_mean": 0.58,
      "high_vulnerability_pct": 0.32
    }
  }
}
```

### Site Comparison Matrix

```json
{
  "comparison": [
    {
      "site": "Houston Medical Center",
      "eligible_pool": 198800,
      "diversity_score": 0.85,
      "accessibility_score": 0.72,
      "feasibility_rank": 1
    },
    {
      "site": "Dallas University Medical",
      "eligible_pool": 156200,
      "diversity_score": 0.78,
      "accessibility_score": 0.68,
      "feasibility_rank": 2
    }
  ]
}
```

---

## Diversity Planning

### FDA Diversity Requirements

Map PopulationSim demographics to trial diversity targets:

```json
// PopulationProfile demographics
{
  "demographics": {
    "race_ethnicity": {
      "white_nh": 0.288,
      "black_nh": 0.198,
      "hispanic": 0.438,
      "asian_nh": 0.078
    }
  }
}

// TrialSim diversity planning output
{
  "diversity_plan": {
    "target_enrollment": 500,
    "demographic_targets": {
      "white_nh": {"min": 100, "max": 200, "target_pct": 0.30},
      "black_nh": {"min": 75, "max": 125, "target_pct": 0.20},
      "hispanic": {"min": 150, "max": 250, "target_pct": 0.40},
      "asian_nh": {"min": 25, "max": 75, "target_pct": 0.10}
    },
    "age_distribution": {
      "40_49": {"target_pct": 0.25},
      "50_59": {"target_pct": 0.35},
      "60_69": {"target_pct": 0.30},
      "70_75": {"target_pct": 0.10}
    },
    "sex_distribution": {
      "male": {"target_pct": 0.50},
      "female": {"target_pct": 0.50}
    }
  }
}
```

### SDOH Diversity Considerations

Include SDOH-based diversity for health equity:

```json
{
  "sdoh_diversity_targets": {
    "high_vulnerability": {
      "description": "SVI ≥ 0.70",
      "target_pct": 0.25,
      "min_subjects": 125
    },
    "transportation_insecure": {
      "description": "No vehicle household",
      "target_pct": 0.08,
      "min_subjects": 40,
      "accommodation": "transport_stipend"
    },
    "food_insecure": {
      "description": "Food insecurity documented",
      "target_pct": 0.12,
      "min_subjects": 60,
      "accommodation": "meal_vouchers"
    }
  }
}
```

---

## Eligibility Pool Estimation

### Condition Prevalence to Eligible Population

```json
// PopulationProfile health indicators
{
  "health_indicators": {
    "chronic_conditions": {
      "diabetes": 0.108,
      "hypertension": 0.348,
      "chf": 0.068,
      "ckd": 0.038
    }
  }
}

// TrialSim eligibility calculation
{
  "protocol_criteria": {
    "inclusion": {
      "age": {"min": 40, "max": 75},
      "conditions": ["diabetes"],
      "hba1c": {"min": 7.0, "max": 10.0}
    },
    "exclusion": {
      "conditions": ["esrd", "active_cancer", "pregnancy"],
      "egfr_below": 30
    }
  },
  
  "eligibility_funnel": {
    "catchment_population": 4731145,
    "age_eligible": 1842000,
    "has_diabetes": 198936,
    "hba1c_in_range": 119362,
    "no_exclusions": 107426,
    "estimated_eligible": 107426,
    "conversion_assumptions": {
      "aware_of_trial": 0.10,
      "interested": 0.40,
      "screen_pass": 0.75,
      "consent": 0.85
    },
    "projected_enrollable": 2742
  }
}
```

### Comorbidity Impact on Eligibility

```json
{
  "comorbidity_impact": {
    "diabetes_only": {
      "pool_size": 82500,
      "exclusion_rate": 0.08
    },
    "diabetes_hypertension": {
      "pool_size": 85200,
      "exclusion_rate": 0.12
    },
    "diabetes_ckd_stage3": {
      "pool_size": 18200,
      "exclusion_rate": 0.25
    },
    "diabetes_chf": {
      "pool_size": 12400,
      "exclusion_rate": 0.35
    }
  }
}
```

---

## Retention Risk Modeling

### SDOH Factors and Visit Compliance

PopulationSim SDOH profiles predict retention challenges:

```json
// SDOH retention risk factors
{
  "sdoh_retention_impact": {
    "transportation_insecurity": {
      "prevalence": 0.088,
      "missed_visit_multiplier": 2.1,
      "drop_out_multiplier": 1.8,
      "mitigation": "transport_reimbursement"
    },
    "employment_constraints": {
      "prevalence": 0.42,
      "missed_visit_multiplier": 1.4,
      "mitigation": "flexible_scheduling"
    },
    "food_insecurity": {
      "prevalence": 0.148,
      "drop_out_multiplier": 1.5,
      "mitigation": "meal_provision"
    },
    "low_health_literacy": {
      "prevalence": 0.044,
      "protocol_deviation_multiplier": 1.6,
      "mitigation": "enhanced_education"
    }
  }
}
```

### Retention Rate Projection

```json
{
  "retention_projection": {
    "baseline_retention_12mo": 0.85,
    
    "sdoh_adjusted_retention": {
      "low_vulnerability": 0.90,
      "moderate_vulnerability": 0.82,
      "high_vulnerability": 0.72,
      "very_high_vulnerability": 0.65
    },
    
    "overall_expected_retention": 0.78,
    
    "recommended_over_enrollment": 1.28
  }
}
```

---

## Subject Simulation

### SDTM Demographics (DM) Integration

```json
// PopulationSim-driven DM domain
{
  "domain": "DM",
  "records": [
    {
      "STUDYID": "DM-CARDIO-001",
      "USUBJID": "DM-CARDIO-001-001-001",
      "SUBJID": "001-001",
      "SITEID": "001",
      "AGE": 58,
      "AGEU": "YEARS",
      "SEX": "F",
      "RACE": "BLACK OR AFRICAN AMERICAN",
      "ETHNIC": "NOT HISPANIC OR LATINO",
      "COUNTRY": "USA",
      "DMDTC": "2024-03-15",
      "DMDY": 1
    }
  ]
}
```

### Supplemental SDOH Qualifiers (SUPPDM)

```json
{
  "domain": "SUPPDM",
  "records": [
    {
      "STUDYID": "DM-CARDIO-001",
      "RDOMAIN": "DM",
      "USUBJID": "DM-CARDIO-001-001-001",
      "QNAM": "SVITOT",
      "QLABEL": "Social Vulnerability Index Total",
      "QVAL": "0.72",
      "QORIG": "DERIVED"
    },
    {
      "QNAM": "TRANINS",
      "QLABEL": "Transportation Insecurity",
      "QVAL": "Y",
      "QORIG": "CRF"
    },
    {
      "QNAM": "FOODINS",
      "QLABEL": "Food Insecurity",
      "QVAL": "N",
      "QORIG": "CRF"
    }
  ]
}
```

---

## Enrollment Simulation

### Screening and Enrollment Flow

```json
{
  "enrollment_simulation": {
    "protocol_id": "DM-CARDIO-001",
    "simulation_period": {"start": "2024-01-01", "months": 18},
    "target_enrollment": 500,
    
    "screening_projections": {
      "month_1": {"screened": 45, "enrolled": 28, "screen_fail_rate": 0.38},
      "month_6": {"screened": 62, "enrolled": 42, "screen_fail_rate": 0.32},
      "month_12": {"screened": 48, "enrolled": 35, "screen_fail_rate": 0.27}
    },
    
    "cumulative": {
      "total_screened": 842,
      "total_enrolled": 512,
      "overall_screen_fail": 0.39,
      "target_met_month": 14
    },
    
    "diversity_achieved": {
      "white_nh": 0.29,
      "black_nh": 0.21,
      "hispanic": 0.38,
      "asian_nh": 0.12,
      "diversity_target_met": true
    }
  }
}
```

---

## Example: Complete Feasibility Assessment

### Input: Protocol Definition

```json
{
  "protocol": {
    "protocol_id": "DM-CARDIO-001",
    "title": "Cardiovascular Outcomes in Type 2 Diabetes",
    "phase": "3",
    "target_enrollment": 500,
    "duration_months": 24,
    
    "eligibility": {
      "age": {"min": 40, "max": 75},
      "conditions": {
        "required": ["type_2_diabetes"],
        "hba1c": {"min": 7.0, "max": 10.5}
      },
      "exclusions": ["esrd", "nyha_class_iv", "active_malignancy"]
    },
    
    "diversity_requirements": {
      "minority_enrollment": 0.40,
      "elderly_65_plus": 0.25,
      "female": 0.50
    },
    
    "sites": ["48201", "48113", "48029"]
  }
}
```

### Output: Feasibility Report

```json
{
  "feasibility_report": {
    "protocol_id": "DM-CARDIO-001",
    "assessment_date": "2024-12-23",
    
    "overall_feasibility": "HIGH",
    "confidence_score": 0.85,
    
    "site_assessments": [
      {
        "site": "Houston (48201)",
        "eligible_pool": 107426,
        "feasibility": "HIGH",
        "projected_enrollment": 220,
        "diversity_alignment": 0.92
      },
      {
        "site": "Dallas (48113)",
        "eligible_pool": 84200,
        "feasibility": "HIGH",
        "projected_enrollment": 180,
        "diversity_alignment": 0.88
      },
      {
        "site": "San Antonio (48029)",
        "eligible_pool": 62400,
        "feasibility": "MODERATE",
        "projected_enrollment": 120,
        "diversity_alignment": 0.95
      }
    ],
    
    "aggregate_projections": {
      "total_eligible_pool": 254026,
      "projected_total_enrollment": 520,
      "enrollment_timeline_months": 14,
      "diversity_targets_achievable": true,
      "sdoh_considerations": {
        "high_vulnerability_pct": 0.28,
        "recommended_accommodations": [
          "transportation_stipend",
          "flexible_scheduling",
          "bilingual_coordinators"
        ]
      }
    },
    
    "recommendations": [
      "Proceed with all three sites",
      "Implement enhanced retention program for high-SDOH subjects",
      "Consider mobile/home visit option for 10% of visits",
      "Budget for transportation reimbursement"
    ]
  }
}
```

---

## Related Skills

- [Geographic Intelligence](../geographic/county-profile.md)
- [Health Patterns](../health-patterns/chronic-disease-prevalence.md)
- [Feasibility Estimation](../trial-support/feasibility-estimation.md)
- [Site Selection Support](../trial-support/site-selection-support.md)
- [TrialSim SKILL](../../trialsim/SKILL.md)
