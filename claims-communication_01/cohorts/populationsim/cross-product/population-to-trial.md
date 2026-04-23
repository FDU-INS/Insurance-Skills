# Population to Trial Integration

## Overview

This scenario demonstrates how PopulationSim data informs clinical trial feasibility, site selection, enrollment planning, and diversity compliance through integration with TrialSim.

---

## Integration Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                      PopulationSim                               │
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │Demographics │  │   Health    │  │      Geography          │  │
│  │             │  │ Indicators  │  │                         │  │
│  │ • Diversity │  │ • Condition │  │ • Site catchment        │  │
│  │ • Age dist  │  │   rates     │  │ • Distance analysis     │  │
│  │ • Race/eth  │  │ • Comorbid  │  │ • Urban/rural           │  │
│  └──────┬──────┘  └──────┬──────┘  └───────────┬─────────────┘  │
│         │                │                      │                │
└─────────┼────────────────┼──────────────────────┼────────────────┘
          │                │                      │
          ▼                ▼                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                        TrialSim                                  │
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │ Feasibility │  │  Diversity  │  │      Enrollment         │  │
│  │             │  │  Planning   │  │                         │  │
│  │ • Eligible  │  │ • Race/eth  │  │ • Screening             │  │
│  │   pool      │  │   targets   │  │ • Enrollment rates      │  │
│  │ • Barriers  │  │ • Compliance│  │ • SDOH considerations   │  │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Step-by-Step Workflow

### Step 1: Define Trial Protocol Requirements

**Protocol**: DM-CARDIO-2024-001 (Type 2 Diabetes Cardiovascular Outcomes)

```json
{
  "protocol_id": "DM-CARDIO-2024-001",
  "indication": "Type 2 Diabetes with CV Risk",
  
  "eligibility": {
    "inclusion": [
      {"criterion": "age", "min": 40, "max": 75},
      {"criterion": "diagnosis", "code": "E11", "duration_months": 12},
      {"criterion": "hba1c", "min": 7.0, "max": 10.5},
      {"criterion": "cv_risk", "type": "established_or_high_risk"}
    ],
    "exclusion": [
      {"criterion": "diagnosis", "code": "N18.5", "reason": "ESRD"},
      {"criterion": "diagnosis", "code": "C*", "reason": "Active cancer"},
      {"criterion": "pregnancy", "status": "current_or_planned"}
    ]
  },
  
  "enrollment": {
    "target": 500,
    "sites": 5,
    "per_site_target": 100,
    "duration_months": 18
  },
  
  "diversity_requirements": {
    "fda_guidance": true,
    "race_ethnicity_targets": {
      "minority_minimum": 0.35,
      "hispanic_minimum": 0.15,
      "black_minimum": 0.12
    },
    "sex_balance": {"female_minimum": 0.45}
  }
}
```

### Step 2: Site Catchment Analysis

**PopulationSim Skill**: `analyze-trial-catchment`

```
User: Analyze the catchment area for Houston Methodist Hospital 
(Harris County) for the DM-CARDIO-2024-001 trial.
```

**Catchment Analysis Output**:
```json
{
  "site": {
    "name": "Houston Methodist Hospital",
    "location": {"lat": 29.7107, "lng": -95.3998},
    "catchment_radius_miles": 30
  },
  
  "catchment_population": {
    "total": 4200000,
    "tracts_included": 842,
    "counties": ["Harris", "Fort Bend", "Montgomery"]
  },
  
  "eligible_pool_estimate": {
    "diabetes_prevalence": 0.118,
    "adults_40_75": 1680000,
    "diabetes_in_age_range": 198240,
    "cv_risk_factor": 0.55,
    "estimated_eligible": 109032,
    "eligibility_rate": 0.026
  },
  
  "diversity_profile": {
    "race_ethnicity": {
      "white_nh": 0.288,
      "black_nh": 0.198,
      "hispanic": 0.438,
      "asian_nh": 0.078
    },
    "diversity_index": 0.72,
    "meets_fda_targets": true
  },
  
  "sdoh_considerations": {
    "mean_svi": 0.52,
    "high_vulnerability_tracts": 0.38,
    "transportation_barriers": 0.12,
    "uninsured_rate": 0.148
  }
}
```

### Step 3: Feasibility Assessment

**TrialSim Skill**: `assess-trial-feasibility`

```json
{
  "feasibility": {
    "eligible_pool": 109032,
    "projected_awareness": 0.15,
    "projected_interest": 0.30,
    "screening_conversion": 0.45,
    "randomization_rate": 0.72,
    
    "enrollment_funnel": {
      "aware_of_trial": 16355,
      "express_interest": 4906,
      "screened": 2208,
      "screen_pass": 1590,
      "randomized": 1145
    },
    
    "enrollment_projection": {
      "target": 100,
      "projected_18_months": 145,
      "feasibility_score": "high",
      "confidence": 0.85
    }
  },
  
  "diversity_compliance": {
    "hispanic_projected": 0.42,
    "black_projected": 0.19,
    "female_projected": 0.48,
    "all_targets_met": true
  },
  
  "barriers": {
    "transportation": {
      "impact": "moderate",
      "affected_population": 0.12,
      "mitigation": "rideshare_stipend"
    },
    "work_schedule": {
      "impact": "moderate",
      "affected_population": 0.35,
      "mitigation": "evening_weekend_visits"
    },
    "food_insecurity": {
      "impact": "low",
      "affected_population": 0.14,
      "mitigation": "meal_provision_at_visits"
    }
  }
}
```

### Step 4: Generate Trial Subjects

**TrialSim Skill**: `generate-trial-cohort`

```
User: Generate 100 eligible subjects for the DM-CARDIO trial 
at the Houston Methodist site, ensuring diversity compliance.
```

---

## Data Mapping

### Demographics to Eligibility

| PopulationSim Field | TrialSim Mapping | Usage |
|---------------------|------------------|-------|
| `age_distribution` | Subject age sampling | Eligibility (40-75) |
| `race_ethnicity` | Diversity stratification | FDA compliance |
| `sex_distribution` | Sex balance | 45% female minimum |
| `geography` | Site catchment | Distance calculation |

### Health Indicators to Eligibility

| PopulationSim Field | TrialSim Mapping | Usage |
|---------------------|------------------|-------|
| `health_indicators.diabetes` | Base eligible pool | Inclusion criterion |
| `health_indicators.chd` | CV risk factor | Inclusion criterion |
| `health_indicators.ckd` | Exclusion screen | Stage 5 excluded |

### SDOH to Enrollment Barriers

| SDOH Factor | Enrollment Impact | Mitigation |
|-------------|-------------------|------------|
| No vehicle (Z59.82) | Visit attendance | Transportation stipend |
| Low income (Z59.6) | Participation cost | Enhanced stipend |
| Food insecurity (Z59.41) | Fasting requirements | Meal provision |
| Limited English (Z60.3) | Consent/compliance | Bilingual staff |

---

## Example Generated Subject

```json
{
  "subject": {
    "subject_id": "SUBJ-DM-CARDIO-001",
    "screening_id": "SCR-2024-0042",
    
    "person": {
      "ssn": "123-45-6789",
      "first_name": "Maria",
      "last_name": "Garcia"
    },
    
    "demographics": {
      "age": 58,
      "sex": "female",
      "race": "white",
      "ethnicity": "hispanic",
      "primary_language": "spanish"
    },
    
    "address": {
      "city": "Houston",
      "state": "TX",
      "zip": "77023",
      "distance_to_site_miles": 8.2
    }
  },
  
  "eligibility": {
    "inclusion_met": [
      {"criterion": "age", "value": 58, "status": "pass"},
      {"criterion": "diabetes_diagnosis", "duration_months": 36, "status": "pass"},
      {"criterion": "hba1c", "value": 8.2, "status": "pass"},
      {"criterion": "cv_risk", "type": "hypertension_dyslipidemia", "status": "pass"}
    ],
    "exclusion_cleared": [
      {"criterion": "esrd", "status": "not_present"},
      {"criterion": "active_cancer", "status": "not_present"},
      {"criterion": "pregnancy", "status": "not_applicable"}
    ],
    "overall_eligible": true
  },
  
  "medical_history": {
    "conditions": [
      {"code": "E11.9", "onset": "2021-03-15", "status": "active"},
      {"code": "I10", "onset": "2018-06-22", "status": "active"},
      {"code": "E78.5", "onset": "2019-11-08", "status": "active"}
    ],
    "labs": {
      "hba1c": {"value": 8.2, "date": "2024-09-01"},
      "egfr": {"value": 72, "date": "2024-09-01"},
      "ldl": {"value": 142, "date": "2024-09-01"}
    }
  },
  
  "sdoh_context": {
    "svi_score": 0.68,
    "z_codes": ["Z59.6", "Z59.41"],
    "barriers_identified": {
      "transportation": {
        "has_vehicle": true,
        "distance_concern": false
      },
      "work_schedule": {
        "employed": true,
        "flexible": false,
        "prefers_evening": true
      },
      "language": {
        "primary": "spanish",
        "english_proficiency": "moderate",
        "interpreter_needed": true
      }
    },
    "accommodations_recommended": [
      "bilingual_consent_form",
      "spanish_speaking_coordinator",
      "evening_visit_slots"
    ]
  },
  
  "enrollment_status": {
    "screened_date": "2024-10-15",
    "consent_date": "2024-10-15",
    "randomization_date": "2024-10-22",
    "arm": "treatment",
    "site": "Houston Methodist"
  }
}
```

---

## Diversity Planning

### Population-Based Diversity Targets

Based on PopulationSim catchment analysis:

| Group | Catchment % | FDA Minimum | Trial Target | Projected |
|-------|-------------|-------------|--------------|-----------|
| Hispanic | 43.8% | 15% | 40% | 42% |
| Black NH | 19.8% | 12% | 18% | 19% |
| White NH | 28.8% | - | 30% | 29% |
| Asian NH | 7.8% | - | 8% | 8% |
| Female | 50.2% | 45% | 48% | 48% |

### Stratified Enrollment Algorithm

```
function enrollSubject(eligiblePool, currentEnrollment, targets):
    # Calculate current diversity metrics
    currentDiversity = calculateDiversity(currentEnrollment)
    
    # Identify underrepresented groups
    underrepresented = findUnderrepresented(currentDiversity, targets)
    
    # Weight selection toward underrepresented
    if underrepresented:
        candidatePool = prioritizeUnderrepresented(eligiblePool, underrepresented)
    else:
        candidatePool = eligiblePool
    
    # Select next subject
    subject = selectWithSDOHConsiderations(candidatePool)
    
    return subject
```

---

## SDOH-Informed Enrollment

### Barrier Mitigation Strategies

| Barrier | Population % | Strategy | Cost/Subject |
|---------|--------------|----------|--------------|
| No vehicle | 8.8% | Rideshare vouchers | $150/visit |
| Work conflicts | 35% | Evening/weekend visits | Staff overtime |
| Food insecurity | 14.2% | Meals at visits | $25/visit |
| Limited English | 16.8% | Bilingual staff | Included |
| Low income | 18.2% | Enhanced stipend | +$100/visit |

### Retention Risk Scoring

```json
{
  "subject_id": "SUBJ-DM-CARDIO-001",
  "retention_risk": {
    "score": 0.35,
    "level": "moderate",
    "factors": {
      "transportation": 0.10,
      "work_schedule": 0.15,
      "language_barrier": 0.05,
      "socioeconomic": 0.05
    },
    "mitigation_plan": [
      "flexible_scheduling",
      "reminder_calls_spanish",
      "transportation_assistance_available"
    ]
  }
}
```

---

## Multi-Site Comparison

### Site Feasibility Summary

| Site | Catchment Pop | Eligible Pool | Diversity Index | SVI Mean | Feasibility |
|------|---------------|---------------|-----------------|----------|-------------|
| Houston Methodist | 4.2M | 109K | 0.72 | 0.52 | High |
| MD Anderson | 4.2M | 109K | 0.72 | 0.52 | High |
| Memorial Hermann | 3.8M | 98K | 0.68 | 0.58 | High |
| Ben Taub (Harris Health) | 2.1M | 62K | 0.78 | 0.74 | Moderate |
| Kelsey-Seybold | 1.8M | 48K | 0.58 | 0.42 | Moderate |

---

## Validation Checklist

- [ ] Eligible pool estimate based on population prevalence
- [ ] Diversity projections match catchment demographics
- [ ] SDOH barriers identified from population profile
- [ ] Accommodation recommendations address barriers
- [ ] Generated subjects reflect population distribution
- [ ] SSN correlates to PatientSim/MemberSim records

---

## Related Scenarios

- [Population to Patient](population-to-patient.md) - Clinical history
- [Population to Member](population-to-member.md) - Insurance status
- [Full Ecosystem](full-ecosystem-cohort.md) - Complete integration
