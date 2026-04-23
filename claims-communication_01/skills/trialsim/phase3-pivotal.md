---
name: phase3-pivotal-trial
description: |
  Generate Phase 3 pivotal trial data with realistic multi-site enrollment, 
  randomization, visit schedules, safety monitoring, and efficacy endpoints 
  for regulatory submission. Triggers: "phase 3", "pivotal", "confirmatory", 
  "registration trial", "NDA", "BLA", "superiority", "non-inferiority".
---

# Phase 3 Pivotal Trials

Generate realistic Phase 3 clinical trial data for confirmatory studies designed to provide substantial evidence of efficacy and safety for regulatory approval (NDA/BLA/MAA).

---

## For Claude

This is a **trial phase skill** for generating Phase 3 pivotal trial data. Apply when users request confirmatory studies, registration trials, or regulatory submission data.

**Always apply this skill when you see:**
- Phase 3, Phase III, or pivotal trial requests
- Registration, confirmatory, or submission study references
- NDA, BLA, MAA, or regulatory approval discussions
- Superiority, non-inferiority, or equivalence trial designs
- Multi-center or global trial requirements
- Primary efficacy endpoint or safety database references

**Combine with:**
- Therapeutic area skills for disease-specific endpoints and patterns
- SDTM domain skills for regulatory-compliant data structures
- Phase 2 skill for seamless Phase 2/3 designs

---

## Phase 3 Trial Characteristics

| Aspect | Typical Values |
|--------|----------------|
| **Sample Size** | 300-3,000+ subjects |
| **Duration** | 2-5 years |
| **Sites** | 50-300+ globally |
| **Countries** | 10-40+ |
| **Primary Objective** | Confirm efficacy, characterize safety |
| **Regulatory Purpose** | Substantial evidence for approval |

### Phase 3 Subtypes

| Subtype | Purpose | Design |
|---------|---------|--------|
| **Phase 3a** | Primary registration study | Randomized, controlled |
| **Phase 3b** | Additional indication, formulation | Variable |
| **Pivotal** | First approval (NDA/BLA) | Usually two adequate & well-controlled |

---

## Study Design Types

### Superiority Trial

Demonstrates treatment is better than control by a clinically meaningful margin.

**Hypothesis:**
- H₀: μ_treatment - μ_control ≤ 0 (or δ for margin)
- H₁: μ_treatment - μ_control > 0

**Sample Size Factors:**
```
n = 2 × [(Z_α + Z_β)² × σ²] / δ²

Where:
- α: Type I error (typically 0.025 one-sided or 0.05 two-sided)
- β: Type II error (typically 0.10-0.20)
- σ: Standard deviation
- δ: Clinically meaningful difference
```

### Non-Inferiority Trial

Demonstrates treatment is not worse than active control by a predefined margin.

**Hypothesis:**
- H₀: μ_treatment - μ_control ≤ -Δ (treatment is inferior)
- H₁: μ_treatment - μ_control > -Δ (treatment is non-inferior)

**Non-Inferiority Margin (Δ) Selection:**
| Approach | Method |
|----------|--------|
| Historical | 50% of proven effect vs placebo |
| Clinical | Smallest clinically meaningful difference |
| Fixed | Regulatory guidance (e.g., 1.3 for NI margin on mortality) |

### Equivalence Trial

Demonstrates two treatments have similar effects.

**Hypothesis:**
- H₀: |μ₁ - μ₂| ≥ Δ
- H₁: |μ₁ - μ₂| < Δ (treatments are equivalent)

---

## Randomization Schemes

### Simple Randomization

```json
{
  "method": "simple",
  "ratio": "1:1",
  "seed": 12345
}
```

### Stratified Block Randomization

```json
{
  "method": "stratified_block",
  "ratio": "1:1",
  "block_sizes": [4, 6],
  "stratification_factors": [
    {"name": "region", "levels": ["North America", "Europe", "Asia"]},
    {"name": "disease_severity", "levels": ["Mild", "Moderate", "Severe"]}
  ]
}
```

### Dynamic/Minimization

```json
{
  "method": "minimization",
  "ratio": "1:1",
  "factors": [
    {"name": "age_group", "weight": 1},
    {"name": "sex", "weight": 1},
    {"name": "baseline_score", "weight": 2}
  ],
  "probability_best_arm": 0.8
}
```

---

## Visit Schedules

### Standard Visit Structure

```
Study Timeline:
─────────────────────────────────────────────────────────────────────
│ Screen │ Baseline │ Treatment Period        │ Follow-up │
│ -28 to │ Day 1    │ Week 4,8,12,16,20,24    │ Week 28   │
│ Day -1 │          │                          │           │
─────────────────────────────────────────────────────────────────────
```

### Visit Windows

| Visit | Target Day | Window (Days) |
|-------|-----------|---------------|
| Screening | -28 to -1 | N/A |
| Baseline/Randomization | 1 | N/A |
| Week 4 | 29 | ±7 |
| Week 8 | 57 | ±7 |
| Week 12 | 85 | ±7 |
| Week 24 (Primary) | 169 | ±7 |
| Week 28 (Follow-up) | 197 | ±14 |
| Early Termination | Any | Within 7 days |

---

## Endpoints

### Primary Efficacy Endpoints by Therapeutic Area

| Therapeutic Area | Common Primary Endpoints |
|-----------------|-------------------------|
| **Oncology** | OS, PFS, ORR |
| **Cardiology** | MACE (CV death, MI, stroke), HF hospitalization |
| **Diabetes** | HbA1c change, CV outcomes |
| **CNS/Psychiatry** | Scale change (MADRS, PANSS, ADAS-Cog) |
| **Respiratory** | FEV1 change, exacerbation rate |
| **Immunology** | ACR20/50/70, PASI75/90/100 |
| **Infectious Disease** | Viral load, clinical cure rate |

### Composite Endpoints

```json
{
  "endpoint_name": "MACE",
  "type": "composite",
  "components": [
    {"name": "cardiovascular_death", "adjudicated": true},
    {"name": "nonfatal_MI", "adjudicated": true},
    {"name": "nonfatal_stroke", "adjudicated": true}
  ],
  "analysis": "time_to_first_event"
}
```

### Hierarchical Testing

```
Testing Order (gatekeeping):
1. Primary endpoint
   ├── If significant (p < 0.05) → Continue
   └── If not → STOP (no further claims)
2. Key secondary #1
   ├── If significant → Continue
   └── If not → STOP  
3. Key secondary #2
   └── ...
```

---

## Safety Monitoring

### Data Safety Monitoring Board (DSMB)

```json
{
  "dsmb": {
    "composition": [
      {"role": "Chair", "specialty": "Biostatistics"},
      {"role": "Member", "specialty": "Cardiology"},
      {"role": "Member", "specialty": "Clinical Pharmacology"}
    ],
    "charter_version": "2.0",
    "meeting_schedule": "quarterly",
    "unblinded_access": true
  }
}
```

### Interim Analyses

| Type | Purpose | Action |
|------|---------|--------|
| **Futility** | Early stopping if unlikely to succeed | Non-binding or binding |
| **Efficacy** | Early stopping for overwhelming benefit | Binding, α-spending |
| **Safety** | Continuous safety review | Unblinded to DSMB |
| **Sample Size Re-estimation** | Adjust N based on variance | Blinded or unblinded |

---

## Statistical Analysis

### Primary Analysis Methods

| Endpoint Type | Method |
|--------------|--------|
| Continuous | ANCOVA, MMRM |
| Binary | Logistic regression, CMH |
| Time-to-event | Log-rank, Cox PH |
| Count | Negative binomial, Poisson |
| Ordinal | Proportional odds |

### Missing Data Handling

| Method | Use Case |
|--------|----------|
| MMRM (MAR) | Longitudinal continuous, primary |
| Multiple Imputation | Sensitivity analysis |
| LOCF | Historical, deprecated |
| Tipping Point | Sensitivity for MNAR |
| Jump to Reference | Conservative, treatment policy |

---

## Generation Patterns

### Pattern 1: Superiority Trial Structure

```json
{
  "study_type": "phase3_pivotal",
  "design": "superiority",
  "comparison": "treatment_vs_placebo",
  "randomization_ratio": "1:1",
  "blinding": "double_blind",
  "planned_n": 500,
  "primary_endpoint": {
    "name": "change_from_baseline_week24",
    "type": "continuous",
    "analysis": "MMRM"
  },
  "alpha": 0.05,
  "power": 0.90
}
```

### Pattern 2: Non-Inferiority Trial

```json
{
  "study_type": "phase3_pivotal",
  "design": "non_inferiority",
  "comparison": "treatment_vs_active_control",
  "ni_margin": -1.5,
  "margin_justification": "50%_of_historical_effect",
  "primary_analysis": "per_protocol",
  "sensitivity_analysis": "ITT"
}
```

### Pattern 3: Event-Driven Cardiovascular Outcomes Trial

```json
{
  "study_type": "phase3_cvot",
  "design": "event_driven",
  "primary_endpoint": "time_to_mace",
  "target_events": 450,
  "planned_subjects": 3500,
  "median_followup_years": 2.5,
  "interim_analyses": [
    {"events": 225, "purpose": "futility"},
    {"events": 338, "purpose": "efficacy_futility"}
  ]
}
```

---

## Examples

### Example 1: Phase 3 Diabetes Trial

**Request:** "Generate a Phase 3 pivotal trial for a novel diabetes drug"

```json
{
  "study": {
    "study_id": "DM-301",
    "title": "A Phase 3, Randomized, Double-Blind, Placebo-Controlled Study to Evaluate the Efficacy and Safety of XYZ-004 in Subjects with Type 2 Diabetes Mellitus Inadequately Controlled on Metformin",
    "phase": "3",
    "design": "randomized_double_blind_placebo_controlled",
    "regulatory_pathway": "NDA"
  },
  "objectives": {
    "primary": "Demonstrate superiority of XYZ-004 vs placebo in HbA1c change at Week 24",
    "key_secondary": [
      "Proportion achieving HbA1c <7%",
      "Change in fasting plasma glucose",
      "Change in body weight"
    ]
  },
  "study_design": {
    "randomization": {
      "ratio": "1:1",
      "method": "stratified_block",
      "stratification": ["baseline_HbA1c", "region"]
    },
    "arms": [
      {"name": "XYZ-004", "dose": "10mg QD", "n_planned": 250},
      {"name": "Placebo", "dose": "matching", "n_planned": 250}
    ],
    "duration": {
      "screening": "2 weeks",
      "treatment": "24 weeks",
      "follow_up": "4 weeks"
    }
  },
  "sample_size": {
    "total": 500,
    "assumptions": {
      "treatment_effect": -0.7,
      "common_sd": 1.1,
      "alpha": 0.05,
      "power": 0.90,
      "dropout_rate": 0.15
    }
  },
  "enrollment": {
    "n_sites": 85,
    "countries": ["USA", "Canada", "Germany", "UK", "France", "Spain", "Poland", "Japan"],
    "enrollment_duration_months": 12,
    "subjects": {
      "screened": 892,
      "screen_failures": 378,
      "randomized": 514,
      "completed": 456,
      "discontinued": 58
    }
  },
  "baseline_characteristics": {
    "age_years": {"mean": 56.2, "sd": 10.5},
    "female_pct": 48.2,
    "bmi_kg_m2": {"mean": 32.4, "sd": 5.8},
    "diabetes_duration_years": {"mean": 8.5, "sd": 5.2},
    "hba1c_pct": {"mean": 8.2, "sd": 0.8},
    "fpg_mg_dl": {"mean": 172, "sd": 42},
    "metformin_dose_mg": {"mean": 1850, "sd": 350}
  },
  "efficacy_results": {
    "primary_endpoint": {
      "xyz004": {"n": 245, "ls_mean_change": -1.05, "se": 0.07},
      "placebo": {"n": 248, "ls_mean_change": -0.28, "se": 0.07},
      "difference": {
        "ls_mean": -0.77,
        "se": 0.10,
        "ci_95": [-0.96, -0.58],
        "p_value": "<0.0001"
      }
    },
    "key_secondary": {
      "hba1c_target_pct": {
        "xyz004": 52.2,
        "placebo": 18.5,
        "odds_ratio": 4.72,
        "p_value": "<0.0001"
      },
      "fpg_change_mg_dl": {
        "xyz004": -38.5,
        "placebo": -5.2,
        "difference": -33.3,
        "p_value": "<0.0001"
      },
      "weight_change_kg": {
        "xyz004": -2.8,
        "placebo": -0.5,
        "difference": -2.3,
        "p_value": "<0.0001"
      }
    }
  },
  "safety_results": {
    "safety_population": 508,
    "exposure": {
      "mean_duration_weeks": 22.8,
      "total_patient_years": 223.5
    },
    "adverse_events": {
      "any_teae": {"xyz004": 68.2, "placebo": 62.1},
      "serious_ae": {"xyz004": 5.1, "placebo": 4.8},
      "discontinuation_ae": {"xyz004": 4.3, "placebo": 3.2},
      "death": {"xyz004": 0, "placebo": 1}
    },
    "common_aes": [
      {"term": "Nausea", "xyz004": 12.5, "placebo": 4.0},
      {"term": "Diarrhea", "xyz004": 8.2, "placebo": 3.6},
      {"term": "Nasopharyngitis", "xyz004": 6.7, "placebo": 7.3},
      {"term": "Headache", "xyz004": 5.5, "placebo": 4.8}
    ],
    "aesi": {
      "hypoglycemia": {"xyz004": 3.5, "placebo": 2.4},
      "genital_infection": {"xyz004": 4.7, "placebo": 0.8}
    }
  },
  "conclusions": {
    "primary_met": true,
    "key_secondary_met": ["all"],
    "safety_acceptable": true,
    "benefit_risk": "favorable",
    "regulatory_submission": "proceed_to_nda"
  }
}
```



### Example 2: Phase 3 Oncology Trial with Survival Endpoint

**Request:** "Generate a Phase 3 pivotal trial for an oncology drug with overall survival endpoint"

```json
{
  "study": {
    "study_id": "ONC-302",
    "title": "A Phase 3, Randomized, Double-Blind Study of ABC-005 Plus Standard Chemotherapy vs Placebo Plus Standard Chemotherapy in Previously Untreated Advanced Non-Small Cell Lung Cancer",
    "phase": "3",
    "design": "randomized_double_blind",
    "regulatory_pathway": "BLA"
  },
  "objectives": {
    "primary": "Overall Survival (OS)",
    "key_secondary": [
      "Progression-Free Survival (PFS)",
      "Objective Response Rate (ORR)",
      "Duration of Response (DOR)"
    ]
  },
  "study_design": {
    "randomization": "2:1",
    "arms": [
      {"name": "ABC-005 + Chemo", "n_planned": 400},
      {"name": "Placebo + Chemo", "n_planned": 200}
    ],
    "stratification": ["PD-L1_status", "ECOG_PS", "histology"],
    "crossover_allowed": false
  },
  "sample_size": {
    "design": "event_driven",
    "target_events": 320,
    "target_subjects": 600,
    "assumptions": {
      "median_os_control_months": 12,
      "hr": 0.75,
      "alpha": 0.05,
      "power": 0.80
    }
  },
  "interim_analyses": [
    {
      "analysis": "IA1",
      "timing": "160_events",
      "boundary": {
        "efficacy_z": 3.71,
        "efficacy_p": 0.0001,
        "futility_hr": 1.0
      },
      "results": {
        "events": 162,
        "hr": 0.72,
        "ci_95": [0.53, 0.98],
        "p_value": 0.018,
        "decision": "continue"
      }
    }
  ],
  "final_analysis": {
    "data_cutoff": "2024-12-01",
    "events": 324,
    "median_follow_up_months": 24.5,
    "primary_endpoint": {
      "os": {
        "abc005_chemo": {
          "n": 398,
          "events": 198,
          "median_months": 18.5,
          "ci_95": [16.2, 21.3]
        },
        "placebo_chemo": {
          "n": 199,
          "events": 126,
          "median_months": 12.8,
          "ci_95": [10.5, 14.9]
        },
        "hr": 0.72,
        "ci_95": [0.58, 0.90],
        "p_value": 0.0032
      }
    },
    "key_secondary": {
      "pfs": {
        "abc005_median": 8.2,
        "placebo_median": 5.4,
        "hr": 0.65,
        "p_value": "<0.0001"
      },
      "orr": {
        "abc005": 0.48,
        "placebo": 0.32,
        "p_value": 0.0002
      },
      "dor_months": {
        "abc005_median": 10.5,
        "placebo_median": 6.2
      }
    }
  },
  "subgroup_analyses": {
    "pd_l1_positive": {"hr": 0.62, "ci": [0.45, 0.85]},
    "pd_l1_negative": {"hr": 0.85, "ci": [0.62, 1.16]},
    "squamous": {"hr": 0.78, "ci": [0.55, 1.10]},
    "non_squamous": {"hr": 0.68, "ci": [0.52, 0.89]}
  },
  "safety_summary": {
    "grade_3_4_ae_pct": {"abc005": 58.2, "placebo": 48.5},
    "serious_ae_pct": {"abc005": 32.1, "placebo": 28.5},
    "discontinuation_ae_pct": {"abc005": 15.2, "placebo": 10.1},
    "death_treatment_related": {"abc005": 2, "placebo": 1},
    "immune_related_aes": {
      "pneumonitis": {"abc005": 5.2, "placebo": 1.0},
      "hepatitis": {"abc005": 3.8, "placebo": 0.5},
      "colitis": {"abc005": 2.5, "placebo": 0.5}
    }
  }
}
```

### Example 3: Phase 3 Non-Inferiority Trial

**Request:** "Generate a Phase 3 non-inferiority trial comparing a new antibiotic to standard of care"

```json
{
  "study": {
    "study_id": "AB-303",
    "title": "A Phase 3, Randomized, Double-Blind, Non-Inferiority Study of XYZ-006 vs Meropenem in Hospital-Acquired Bacterial Pneumonia",
    "phase": "3",
    "design": "non_inferiority",
    "regulatory_pathway": "NDA"
  },
  "non_inferiority_design": {
    "margin": -12.5,
    "margin_justification": "FDA guidance: 10-15% for HABP",
    "analysis_population": {
      "primary": "mMITT",
      "sensitivity": "CE"
    },
    "alpha": 0.025,
    "one_sided": true
  },
  "study_design": {
    "randomization": "1:1",
    "arms": [
      {"name": "XYZ-006", "dose": "2g IV q8h", "n_planned": 300},
      {"name": "Meropenem", "dose": "1g IV q8h", "n_planned": 300}
    ],
    "treatment_duration": "7-14 days",
    "primary_endpoint": "clinical_cure_test_of_cure"
  },
  "enrollment": {
    "n_sites": 95,
    "countries": 22,
    "subjects": {
      "screened": 1205,
      "randomized": 606,
      "mmitt": 584,
      "ce": 512
    }
  },
  "primary_results": {
    "mmitt_population": {
      "xyz006": {"n": 290, "cure": 201, "rate": 0.693},
      "meropenem": {"n": 294, "cure": 188, "rate": 0.639},
      "difference": {
        "point_estimate": 5.4,
        "ci_95": [-2.2, 13.0],
        "lower_bound_vs_margin": "Lower CI (-2.2) > margin (-12.5)"
      }
    },
    "ce_population": {
      "xyz006": {"n": 254, "cure": 192, "rate": 0.756},
      "meropenem": {"n": 258, "cure": 189, "rate": 0.733},
      "difference": {
        "point_estimate": 2.3,
        "ci_95": [-5.2, 9.8]
      }
    },
    "non_inferiority_met": true,
    "superiority_tested": false
  },
  "secondary_endpoints": {
    "28_day_mortality": {
      "xyz006": 0.103,
      "meropenem": 0.112,
      "hr": 0.91
    },
    "microbiological_response": {
      "xyz006": 0.72,
      "meropenem": 0.68
    },
    "time_to_defervescence_days": {
      "xyz006_median": 3.2,
      "meropenem_median": 3.5
    }
  },
  "safety_summary": {
    "any_teae": {"xyz006": 72.3, "meropenem": 69.8},
    "serious_ae": {"xyz006": 18.5, "meropenem": 20.2},
    "c_diff_infection": {"xyz006": 2.1, "meropenem": 3.4},
    "nephrotoxicity": {"xyz006": 1.7, "meropenem": 2.8}
  },
  "conclusions": {
    "ni_demonstrated": true,
    "safety_profile": "comparable_to_meropenem",
    "regulatory_pathway": "proceed_to_nda"
  }
}
```

---

## Validation Rules

| Field | Rule | Error Handling |
|-------|------|----------------|
| `sample_size` | ≥ 100 for pivotal | Warn if smaller |
| `randomization_ratio` | Common ratios (1:1, 2:1, 3:1) | Warn if unusual |
| `alpha` | 0.05 (two-sided) or 0.025 (one-sided) | Error if different |
| `power` | ≥ 0.80 | Warn if lower |
| `ni_margin` | Clinically justified | Flag if not specified |
| `primary_endpoint` | Single endpoint | Warn if multiple |
| `events` | ≥ planned for event-driven | Flag if insufficient |

### Regulatory Validation

| Requirement | Rule |
|-------------|------|
| ICH E6 GCP | All trials must comply |
| ICH E9 Statistical | Analysis plan pre-specified |
| ICH E10 Control | Appropriate comparator |
| Two Adequate Studies | Usually required for approval |

---

## Business Rules

### Trial Conduct Rules

1. **Protocol amendments** - Major changes require IRB/ethics approval
2. **Site selection** - Minimum enrollment capability per site
3. **Monitoring** - Risk-based monitoring recommended
4. **Data management** - 21 CFR Part 11 compliant systems

### Statistical Analysis Rules

1. **SAP timing** - Finalize before database lock
2. **Unblinding** - Only at planned analyses or emergencies
3. **Multiplicity** - Strict control for family-wise error rate
4. **Subgroups** - Pre-specified, hypothesis-generating only

### Regulatory Rules

1. **Safety database** - Minimum 300-600 exposed for 6+ months
2. **Long-term safety** - 100+ exposed for 12+ months (chronic use)
3. **Special populations** - Adequate representation required
4. **Labeling** - Based on ITT population typically

---

## Global Trial Considerations

### Regional Requirements

| Region | Specific Requirements |
|--------|----------------------|
| **FDA (USA)** | Two adequate & well-controlled studies typically |
| **EMA (EU)** | Scientific advice recommended |
| **PMDA (Japan)** | Japanese bridging data often required |
| **NMPA (China)** | Chinese population data required |
| **Health Canada** | Similar to FDA |

### Multi-Regional Clinical Trial (MRCT)

```json
{
  "design": "MRCT",
  "regions": [
    {"region": "North America", "sites": 45, "n": 200},
    {"region": "Western Europe", "sites": 35, "n": 150},
    {"region": "Eastern Europe", "sites": 25, "n": 100},
    {"region": "Asia-Pacific", "sites": 30, "n": 150}
  ],
  "consistency_analysis": "region_by_treatment_interaction",
  "sample_size_rationale": "ICH E17 compliant"
}
```

---

## Related Skills

| Skill | Integration |
|-------|-------------|
| [Phase 1 Dose Escalation](phase1-dose-escalation.md) | Dose selection basis |
| [Phase 2 Proof-of-Concept](phase2-proof-of-concept.md) | Effect size estimation |
| [SDTM Demographics (DM)](domains/demographics-dm.md) | Subject baseline data |
| [SDTM Adverse Events (AE)](domains/adverse-events-ae.md) | Safety database |
| [SDTM Disposition (DS)](domains/disposition-ds.md) | Subject flow |
| [SDTM Exposure (EX)](domains/exposure-ex.md) | Treatment compliance |
| [Oncology Trials](therapeutic-areas/oncology.md) | Cancer-specific patterns |
| [Cardiovascular Trials](therapeutic-areas/cardiovascular.md) | CVOT designs |
| [Recruitment & Enrollment](recruitment-enrollment.md) | Site activation |
| [Synthetic Control Arms](rwe/synthetic-control.md) | External control data |

---

## References

- ICH E6(R2) Good Clinical Practice
- ICH E8(R1) General Considerations for Clinical Studies
- ICH E9(R1) Statistical Principles for Clinical Trials (Estimands)
- ICH E10 Choice of Control Group and Related Issues
- ICH E17 Multi-Regional Clinical Trials
- FDA Guidance: Non-Inferiority Clinical Trials (2016)
- FDA Guidance: Adaptive Designs for Clinical Trials (2019)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-12-20 | Comprehensive Phase 3 skill (replaced placeholder) |

