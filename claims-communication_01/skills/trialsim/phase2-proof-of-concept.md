---
name: phase2-proof-of-concept
description: |
  Generate Phase 2 clinical trial data including proof-of-concept (Phase 2a), 
  dose-ranging (Phase 2b), futility analysis, and efficacy signal detection. 
  Supports Simon's two-stage, Bryant & Day, and MCP-Mod designs. 
  Triggers: "phase 2", "proof of concept", "dose ranging", "futility", 
  "Simon two-stage", "MCP-Mod", "Phase 2a", "Phase 2b".
---

# Phase 2 Proof-of-Concept Trials

Generate realistic Phase 2 clinical trial data for proof-of-concept studies (Phase 2a), dose-ranging trials (Phase 2b), and adaptive designs with futility analysis.

---

## For Claude

This is a **trial phase skill** for generating Phase 2 clinical trial data. Apply when users request proof-of-concept studies, dose-finding trials, or efficacy signal detection studies.

**Always apply this skill when you see:**
- Phase 2, Phase II, or proof-of-concept (POC) requests
- Dose-ranging or dose-response modeling
- Futility analysis or interim analysis
- Simon's two-stage design references
- MCP-Mod or dose-response curve fitting
- Efficacy signal or go/no-go decision discussions

**Combine with:**
- Therapeutic area skills for disease-specific endpoints
- SDTM domain skills for regulatory-compliant data structures
- Phase 1 skill for seamless Phase 1/2 designs

---

## Phase 2 Trial Characteristics

| Aspect | Phase 2a | Phase 2b |
|--------|----------|----------|
| **Primary Objective** | Proof-of-concept, efficacy signal | Dose-response, dose selection |
| **Sample Size** | 20-100 subjects | 100-500 subjects |
| **Duration** | 3-12 months | 6-24 months |
| **Design** | Single-arm or randomized | Randomized, multiple doses |
| **Key Decision** | Go/no-go for Phase 2b | RP3D selection for Phase 3 |
| **Control** | Often none or historical | Active or placebo control |

### Phase 2 Subtypes

| Subtype | Purpose | Typical Design |
|---------|---------|----------------|
| **Phase 2a** | Establish biological activity, initial efficacy signal | Single-arm, Simon's two-stage |
| **Phase 2b** | Characterize dose-response, select Phase 3 dose | Randomized, multiple arms, MCP-Mod |
| **Phase 2/3 (Seamless)** | Combine POC with confirmatory | Adaptive, sample size re-estimation |

---

## Phase 2a: Proof-of-Concept Designs

### Simon's Two-Stage Design

The most widely used Phase 2a design, allowing early stopping for futility.

**Design Parameters:**
- p₀: Unacceptable response rate (null hypothesis)
- p₁: Target response rate (alternative hypothesis)  
- α: Type I error rate (typically 0.05 or 0.10)
- β: Type II error rate (typically 0.10 or 0.20)

**Design Types:**

| Type | Optimization Criterion |
|------|----------------------|
| **Optimal** | Minimizes expected sample size under H₀ |
| **Minimax** | Minimizes maximum sample size |

**Common Simon's Designs (α=0.05, β=0.20):**

| p₀ | p₁ | Design | Stage 1 | Total N | Early Stop If |
|----|----|----|---------|---------|---------------|
| 0.05 | 0.20 | Optimal | 9 | 24 | ≤0/9 |
| 0.05 | 0.20 | Minimax | 13 | 21 | ≤1/13 |
| 0.10 | 0.25 | Optimal | 18 | 43 | ≤2/18 |
| 0.10 | 0.25 | Minimax | 21 | 41 | ≤3/21 |
| 0.20 | 0.40 | Optimal | 13 | 43 | ≤3/13 |
| 0.20 | 0.40 | Minimax | 19 | 39 | ≤5/19 |
| 0.30 | 0.50 | Optimal | 19 | 54 | ≤7/19 |
| 0.30 | 0.50 | Minimax | 25 | 52 | ≤9/25 |

**Decision Rules:**
```
Stage 1: Enroll n₁ subjects
├── If responses ≤ r₁ → STOP for futility (reject drug)
└── If responses > r₁ → Continue to Stage 2

Stage 2: Enroll additional (n - n₁) subjects  
├── If total responses ≤ r → Reject drug (insufficient activity)
└── If total responses > r → Accept drug (proceed to Phase 2b/3)
```

### Bryant & Day Design

Extension of Simon's design allowing stopping for both futility (efficacy) AND excessive toxicity.

**Parameters:**
- Response rate: p₀, p₁ (as in Simon's)
- Toxicity rate: q₀ (unacceptable), q₁ (acceptable)

**Decision Matrix:**
| Efficacy Outcome | Toxicity Outcome | Decision |
|-----------------|------------------|----------|
| Responses ≤ r₁ | Any | Stop - Futility |
| Responses > r₁ | Toxicities > t₁ | Stop - Toxicity |
| Responses > r₁ | Toxicities ≤ t₁ | Continue |

### Gehan Two-Stage Design

Conservative design focused on early futility assessment.

```
Stage 1: Enroll 14 subjects
├── 0 responses → STOP (95% confidence drug has <20% response rate)
└── ≥1 response → Continue to Stage 2

Stage 2: Enroll additional subjects for precision
└── Calculate response rate confidence interval
```

---

## Phase 2b: Dose-Ranging Designs

### MCP-Mod (Multiple Comparison Procedures - Modeling)

FDA/EMA-endorsed method combining hypothesis testing with dose-response modeling.

**Step 1: MCP (Testing)**
```
Test for dose-response signal using contrast tests:
- Linear contrast
- Emax contrast  
- Exponential contrast
- Sigmoidal Emax contrast
- Quadratic contrast

Multiple testing adjustment via Dunnett or similar
```

**Step 2: Mod (Modeling)**
```
If MCP confirms dose-response:
├── Fit candidate dose-response models
├── Model averaging or selection
└── Estimate target dose (ED50, ED90, etc.)
```

**Common Dose-Response Models:**

| Model | Formula | Use Case |
|-------|---------|----------|
| Linear | E = E₀ + δ × d | Simple linear relationship |
| Emax | E = E₀ + (Emax × d)/(ED50 + d) | Saturable response |
| Sigmoidal Emax | E = E₀ + (Emax × d^h)/(ED50^h + d^h) | Steep dose-response |
| Exponential | E = E₀ + E₁ × (1 - exp(-d/δ)) | Plateau response |
| Quadratic | E = E₀ + β₁d + β₂d² | Non-monotonic possible |
| Log-linear | E = E₀ + δ × log(d + 1) | Compressed high doses |

### Parallel Dose-Ranging Design

Traditional randomized design with multiple dose arms.

```
Typical Structure:
┌──────────────┬────────────┬─────────────┐
│ Arm          │ Dose       │ N per Arm   │
├──────────────┼────────────┼─────────────┤
│ Placebo      │ 0          │ 40          │
│ Low Dose     │ 25mg       │ 40          │
│ Medium Dose  │ 50mg       │ 40          │
│ High Dose    │ 100mg      │ 40          │
│ Active Ctrl  │ Standard   │ 40 (opt.)   │
└──────────────┴────────────┴─────────────┘
Total N: 160-200
```

### Adaptive Dose-Finding

Bayesian adaptive designs that update dose allocation based on accumulating data.

**Features:**
- Response-adaptive randomization
- Interim analyses for futility/superiority
- Drop losing arms, add winning doses
- Sample size re-estimation

---

## Interim Analysis & Futility

### Futility Stopping Rules

| Rule Type | Description | Use Case |
|-----------|-------------|----------|
| **Non-binding** | Can stop but not required | Flexibility for sponsors |
| **Binding** | Must stop if criteria met | Regulatory requirement |
| **Conditional Power** | Stop if CP < threshold (e.g., 20%) | Efficiency |
| **Predictive Probability** | Stop if P(success) < threshold | Bayesian |

### O'Brien-Fleming Boundaries

Conservative spending function for group sequential designs.

**α-spending at Information Fraction (t):**

| Analysis | Info Fraction | Z Boundary | Nominal α |
|----------|---------------|------------|-----------|
| Interim 1 | 0.33 | 3.47 | 0.0001 |
| Interim 2 | 0.67 | 2.45 | 0.007 |
| Final | 1.00 | 2.00 | 0.022 |

### Lan-DeMets α-Spending

More flexible spending function.

```
α*(t) = 2 - 2Φ(Z_{α/2} / √t)  [O'Brien-Fleming-like]
α*(t) = α × log(1 + (e-1)×t)   [Pocock-like]
```

---

## Endpoints by Therapeutic Area

### Oncology Phase 2 Endpoints

| Endpoint | Measurement | Typical Target |
|----------|-------------|----------------|
| **ORR** | RECIST 1.1 (CR+PR) | 15-40% improvement over SOC |
| **DCR** | CR+PR+SD ≥6 weeks | 50-70% |
| **PFS** | Time to progression/death | HR 0.60-0.75 |
| **DOR** | Time from response to PD | >6 months |

### CNS/Psychiatric Phase 2 Endpoints

| Endpoint | Scale | Typical Effect Size |
|----------|-------|---------------------|
| **Depression** | MADRS, HAM-D | 2-3 point separation |
| **Anxiety** | HAM-A | 2-3 point separation |
| **Schizophrenia** | PANSS | 5-8 point separation |
| **Cognition** | Various batteries | 0.3-0.5 SD |

### Cardiovascular Phase 2 Endpoints

| Endpoint | Measurement | Typical Target |
|----------|-------------|----------------|
| **Blood Pressure** | mmHg change | 5-10 mmHg reduction |
| **LDL Cholesterol** | % change | 20-50% reduction |
| **HbA1c** | % change | 0.5-1.0% reduction |
| **Heart Failure** | NT-proBNP | 20-30% reduction |

---

## Generation Patterns

### Pattern 1: Simon's Two-Stage Success

```json
{
  "study_type": "phase2a_poc",
  "design": "simon_two_stage",
  "indication": "non_small_cell_lung_cancer",
  "parameters": {
    "p0": 0.20,
    "p1": 0.40,
    "alpha": 0.05,
    "beta": 0.20,
    "design_type": "optimal",
    "n1": 13,
    "n_total": 43,
    "r1": 3,
    "r": 12
  },
  "stage1": {
    "enrolled": 13,
    "evaluable": 13,
    "responses": 5,
    "decision": "continue",
    "threshold": ">3 responses needed"
  },
  "stage2": {
    "enrolled": 30,
    "evaluable": 28,
    "responses": 10,
    "total_enrolled": 43,
    "total_responses": 15
  },
  "outcome": {
    "observed_rr": 0.366,
    "ci_95": [0.23, 0.52],
    "decision": "positive",
    "threshold": ">12 responses needed",
    "conclusion": "proceed_to_phase_2b"
  }
}
```

### Pattern 2: Simon's Two-Stage Futility Stop

```json
{
  "study_type": "phase2a_poc", 
  "design": "simon_two_stage",
  "indication": "metastatic_colorectal_cancer",
  "parameters": {
    "p0": 0.10,
    "p1": 0.25,
    "alpha": 0.10,
    "beta": 0.10,
    "design_type": "optimal",
    "n1": 18,
    "n_total": 43,
    "r1": 2,
    "r": 7
  },
  "stage1": {
    "enrolled": 18,
    "evaluable": 17,
    "responses": 2,
    "decision": "stop_futility",
    "threshold": ">2 responses needed"
  },
  "outcome": {
    "observed_rr": 0.118,
    "decision": "negative",
    "conclusion": "terminate_development",
    "rationale": "Insufficient efficacy signal to justify further development"
  }
}
```

### Pattern 3: MCP-Mod Dose-Ranging

```json
{
  "study_type": "phase2b_dose_ranging",
  "design": "mcp_mod",
  "indication": "type_2_diabetes",
  "endpoint": {
    "name": "HbA1c_change",
    "type": "continuous",
    "direction": "reduction_better"
  },
  "dose_arms": [
    {"arm": "placebo", "dose_mg": 0, "n": 45, "mean_change": -0.15, "sd": 0.9},
    {"arm": "low", "dose_mg": 10, "n": 44, "mean_change": -0.52, "sd": 0.85},
    {"arm": "medium", "dose_mg": 25, "n": 46, "mean_change": -0.78, "sd": 0.88},
    {"arm": "high", "dose_mg": 50, "n": 45, "mean_change": -0.95, "sd": 0.92},
    {"arm": "max", "dose_mg": 100, "n": 43, "mean_change": -1.02, "sd": 0.90}
  ],
  "mcp_step": {
    "candidate_models": ["linear", "emax", "sigEmax", "exponential"],
    "contrast_tests": {
      "linear": {"z_stat": 4.82, "p_value": 0.000001},
      "emax": {"z_stat": 5.21, "p_value": 0.0000002},
      "sigEmax": {"z_stat": 5.15, "p_value": 0.0000003},
      "exponential": {"z_stat": 4.95, "p_value": 0.0000007}
    },
    "dose_response_detected": true,
    "adjusted_p_value": 0.0000008
  },
  "mod_step": {
    "selected_model": "emax",
    "model_fit": {
      "E0": -0.15,
      "Emax": -0.92,
      "ED50": 12.5
    },
    "model_aic": 512.3,
    "dose_estimates": {
      "ED50": 12.5,
      "ED80": 50.0,
      "ED90": 112.5
    }
  },
  "rp3d_recommendation": {
    "dose": "50mg",
    "rationale": "Near-maximal efficacy (~90% of Emax) with acceptable safety",
    "predicted_effect": -0.88
  }
}
```

---

## Examples

### Example 1: Complete Simon's Two-Stage Trial

**Request:** "Generate Phase 2a Simon's two-stage trial for a novel checkpoint inhibitor in melanoma"

```json
{
  "study": {
    "study_id": "MEL-201",
    "title": "Phase 2 Study of XYZ-001 in Unresectable Stage III/IV Melanoma",
    "phase": "2a",
    "design": "simon_optimal_two_stage",
    "population": "advanced_melanoma_anti_pd1_naive"
  },
  "design_rationale": {
    "historical_rr": 0.15,
    "target_rr": 0.35,
    "clinically_meaningful_improvement": 0.20,
    "selected_design": {
      "p0": 0.15,
      "p1": 0.35,
      "alpha": 0.05,
      "power": 0.80,
      "type": "optimal"
    },
    "design_parameters": {
      "n1": 17,
      "r1": 3,
      "n": 37,
      "r": 9,
      "PET": 0.55,
      "EN_H0": 24.0
    }
  },
  "stage1_results": {
    "enrollment_period": "2024-01-15 to 2024-06-30",
    "subjects": [
      {"usubjid": "MEL201-001", "bor": "PR", "response": true},
      {"usubjid": "MEL201-002", "bor": "SD", "response": false},
      {"usubjid": "MEL201-003", "bor": "PD", "response": false},
      {"usubjid": "MEL201-004", "bor": "PR", "response": true},
      {"usubjid": "MEL201-005", "bor": "SD", "response": false},
      {"usubjid": "MEL201-006", "bor": "CR", "response": true},
      {"usubjid": "MEL201-007", "bor": "SD", "response": false},
      {"usubjid": "MEL201-008", "bor": "PD", "response": false},
      {"usubjid": "MEL201-009", "bor": "PR", "response": true},
      {"usubjid": "MEL201-010", "bor": "SD", "response": false},
      {"usubjid": "MEL201-011", "bor": "PD", "response": false},
      {"usubjid": "MEL201-012", "bor": "SD", "response": false},
      {"usubjid": "MEL201-013", "bor": "PR", "response": true},
      {"usubjid": "MEL201-014", "bor": "PD", "response": false},
      {"usubjid": "MEL201-015", "bor": "NE", "response": false},
      {"usubjid": "MEL201-016", "bor": "SD", "response": false},
      {"usubjid": "MEL201-017", "bor": "PR", "response": true}
    ],
    "summary": {
      "enrolled": 17,
      "evaluable": 16,
      "responses": 6,
      "response_rate": 0.375,
      "threshold_met": true
    },
    "interim_decision": {
      "rule": "Continue if >3 responses in first 17",
      "observed": 6,
      "decision": "CONTINUE_TO_STAGE_2"
    }
  },
  "stage2_results": {
    "enrollment_period": "2024-07-01 to 2024-12-15",
    "additional_enrolled": 20,
    "additional_responses": 7,
    "cumulative": {
      "enrolled": 37,
      "evaluable": 35,
      "responses": 13,
      "response_rate": 0.371,
      "ci_95": [0.22, 0.54]
    }
  },
  "final_analysis": {
    "primary_endpoint": {
      "orr": 0.371,
      "cr": 2,
      "pr": 11,
      "sd": 14,
      "pd": 8,
      "ne": 2
    },
    "secondary_endpoints": {
      "dcr": 0.771,
      "median_dor_months": 8.2,
      "median_pfs_months": 5.8,
      "6mo_pfs_rate": 0.48
    },
    "decision": {
      "threshold": ">9 responses in 37 subjects",
      "observed": 13,
      "result": "POSITIVE",
      "conclusion": "Drug demonstrates sufficient activity to warrant Phase 2b/3 development"
    }
  },
  "safety_summary": {
    "total_subjects": 37,
    "any_trae": 32,
    "grade_3_4_trae": 8,
    "serious_aes": 4,
    "discontinuation_due_to_ae": 2,
    "immune_related_aes": {
      "hypothyroidism": 5,
      "rash": 8,
      "colitis": 2,
      "pneumonitis": 1,
      "hepatitis": 1
    }
  }
}
```



### Example 2: Phase 2b Dose-Ranging with Futility

**Request:** "Generate a Phase 2b dose-ranging study for a novel antidepressant using MCP-Mod"

```json
{
  "study": {
    "study_id": "DEP-202",
    "title": "Randomized, Double-Blind, Placebo-Controlled Dose-Ranging Study of ABC-002 in Major Depressive Disorder",
    "phase": "2b",
    "design": "parallel_mcp_mod",
    "population": "moderate_to_severe_mdd"
  },
  "study_design": {
    "randomization": "1:1:1:1:1",
    "blinding": "double_blind",
    "treatment_duration_weeks": 8,
    "primary_endpoint": "MADRS_change_week8",
    "key_secondary": ["HAM-D17_change", "CGI-S_response", "remission_rate"]
  },
  "arms": [
    {
      "arm_code": "PBO",
      "treatment": "Placebo",
      "dose_mg": 0,
      "planned_n": 50,
      "actual_n": 52,
      "completers": 45
    },
    {
      "arm_code": "LOW",
      "treatment": "ABC-002 5mg",
      "dose_mg": 5,
      "planned_n": 50,
      "actual_n": 51,
      "completers": 44
    },
    {
      "arm_code": "MED1",
      "treatment": "ABC-002 15mg",
      "dose_mg": 15,
      "planned_n": 50,
      "actual_n": 49,
      "completers": 42
    },
    {
      "arm_code": "MED2",
      "treatment": "ABC-002 30mg",
      "dose_mg": 30,
      "planned_n": 50,
      "actual_n": 50,
      "completers": 43
    },
    {
      "arm_code": "HIGH",
      "treatment": "ABC-002 60mg",
      "dose_mg": 60,
      "planned_n": 50,
      "actual_n": 51,
      "completers": 41
    }
  ],
  "interim_analysis": {
    "timing": "50%_enrollment",
    "n_analyzed": 126,
    "purpose": "futility",
    "conditional_power": 0.72,
    "decision": "continue"
  },
  "primary_results": {
    "analysis_set": "mITT",
    "n_analyzed": 253,
    "baseline_madrs": {
      "overall_mean": 32.5,
      "sd": 4.2
    },
    "madrs_change_week8": {
      "placebo": {"n": 52, "mean": -8.2, "se": 1.1},
      "5mg": {"n": 51, "mean": -10.5, "se": 1.2},
      "15mg": {"n": 49, "mean": -13.8, "se": 1.1},
      "30mg": {"n": 50, "mean": -15.2, "se": 1.2},
      "60mg": {"n": 51, "mean": -15.8, "se": 1.2}
    },
    "ls_mean_difference_vs_placebo": {
      "5mg": {"diff": -2.3, "se": 1.6, "p": 0.152},
      "15mg": {"diff": -5.6, "se": 1.5, "p": 0.0003},
      "30mg": {"diff": -7.0, "se": 1.6, "p": 0.00002},
      "60mg": {"diff": -7.6, "se": 1.6, "p": 0.000006}
    }
  },
  "mcp_mod_analysis": {
    "step1_mcp": {
      "candidate_contrasts": ["linear", "emax", "sigEmax", "quadratic"],
      "test_results": {
        "linear": {"t_stat": 4.52, "p_adj": 0.00002},
        "emax": {"t_stat": 4.88, "p_adj": 0.000004},
        "sigEmax": {"t_stat": 4.91, "p_adj": 0.000003},
        "quadratic": {"t_stat": 3.89, "p_adj": 0.0002}
      },
      "dose_response_confirmed": true,
      "min_adjusted_p": 0.000003
    },
    "step2_mod": {
      "model_selection": "emax",
      "model_parameters": {
        "E0": -8.2,
        "Emax": -8.1,
        "ED50": 8.5
      },
      "model_fit_statistics": {
        "aic": 1823.5,
        "bic": 1835.2,
        "r_squared": 0.89
      },
      "dose_estimates": {
        "ED50": {"dose_mg": 8.5, "ci_90": [5.2, 14.8]},
        "ED80": {"dose_mg": 34.0, "ci_90": [22.1, 52.3]},
        "ED90": {"dose_mg": 76.5, "ci_90": [48.5, 120.8]}
      }
    }
  },
  "secondary_endpoints": {
    "hamd17_change": {
      "placebo": -5.8,
      "5mg": -7.2,
      "15mg": -9.8,
      "30mg": -11.2,
      "60mg": -11.5
    },
    "response_rate_50pct_reduction": {
      "placebo": 0.25,
      "5mg": 0.31,
      "15mg": 0.45,
      "30mg": 0.52,
      "60mg": 0.55
    },
    "remission_rate_madrs_leq_10": {
      "placebo": 0.12,
      "5mg": 0.18,
      "15mg": 0.29,
      "30mg": 0.36,
      "60mg": 0.37
    }
  },
  "safety_summary": {
    "any_teae": {"placebo": 0.54, "5mg": 0.57, "15mg": 0.61, "30mg": 0.66, "60mg": 0.73},
    "discontinuation_ae": {"placebo": 0.04, "5mg": 0.04, "15mg": 0.06, "30mg": 0.08, "60mg": 0.14},
    "common_aes": [
      {"term": "Nausea", "placebo": 0.08, "5mg": 0.12, "15mg": 0.18, "30mg": 0.22, "60mg": 0.31},
      {"term": "Headache", "placebo": 0.12, "5mg": 0.14, "15mg": 0.16, "30mg": 0.18, "60mg": 0.20},
      {"term": "Insomnia", "placebo": 0.06, "5mg": 0.08, "15mg": 0.12, "30mg": 0.16, "60mg": 0.18},
      {"term": "Dizziness", "placebo": 0.04, "5mg": 0.06, "15mg": 0.10, "30mg": 0.14, "60mg": 0.18}
    ]
  },
  "dose_selection": {
    "rp3d": "30mg",
    "rationale": [
      "Achieves ~86% of maximum effect (ED80)",
      "Statistically significant vs placebo (p<0.00002)",
      "Clinically meaningful effect (-7.0 MADRS points)",
      "Acceptable tolerability profile",
      "60mg provides minimal additional efficacy with increased AEs"
    ],
    "phase3_recommendation": "Proceed to Phase 3 with 30mg QD"
  }
}
```

### Example 3: Randomized Phase 2 with Group Sequential Design

**Request:** "Generate a randomized Phase 2 trial with interim futility analysis for a cardiovascular drug"

```json
{
  "study": {
    "study_id": "CV-203",
    "title": "Randomized, Double-Blind, Placebo-Controlled Phase 2 Study of XYZ-003 in Patients with Heart Failure with Reduced Ejection Fraction",
    "phase": "2",
    "design": "parallel_group_sequential",
    "population": "hfref_nyha_ii_iii"
  },
  "study_design": {
    "randomization": "1:1",
    "stratification": ["NYHA_class", "baseline_NT_proBNP"],
    "treatment_duration_weeks": 24,
    "primary_endpoint": "NT_proBNP_percent_change_week24",
    "interim_analyses": 1,
    "alpha_spending": "obrien_fleming"
  },
  "sample_size": {
    "planned_total": 200,
    "per_arm": 100,
    "assumptions": {
      "placebo_change": -5,
      "treatment_change": -25,
      "common_sd": 40,
      "alpha": 0.05,
      "power": 0.80,
      "dropout_rate": 0.15
    }
  },
  "interim_analysis": {
    "timing": "50%_information",
    "date": "2024-09-15",
    "n_analyzed": 100,
    "results": {
      "treatment": {"n": 48, "mean_change": -22.5, "sd": 38.2},
      "placebo": {"n": 52, "mean_change": -8.2, "sd": 41.5}
    },
    "test_statistic": {
      "z_observed": 1.82,
      "z_boundary_efficacy": 2.96,
      "z_boundary_futility": 0.50
    },
    "conditional_power": 0.68,
    "decision": "continue",
    "rationale": "Z-statistic (1.82) between futility (0.50) and efficacy (2.96) boundaries"
  },
  "final_analysis": {
    "date": "2025-03-01",
    "analysis_set": "mITT",
    "primary_endpoint": {
      "treatment": {"n": 92, "mean_change": -24.8, "sd": 36.5, "median_change": -28.2},
      "placebo": {"n": 95, "mean_change": -6.5, "sd": 39.8, "median_change": -8.5},
      "difference": {
        "ls_mean_diff": -18.3,
        "se": 5.6,
        "ci_95": [-29.3, -7.3],
        "p_value": 0.0012
      }
    },
    "responder_analysis": {
      "definition": "≥30% NT-proBNP reduction",
      "treatment": {"n": 92, "responders": 48, "rate": 0.522},
      "placebo": {"n": 95, "responders": 25, "rate": 0.263},
      "odds_ratio": 3.07,
      "ci_95": [1.68, 5.62],
      "p_value": 0.0002
    },
    "secondary_endpoints": {
      "6mwd_change_m": {
        "treatment": {"mean": 32.5, "se": 8.2},
        "placebo": {"mean": 8.2, "se": 7.8},
        "p_value": 0.032
      },
      "kccq_total_change": {
        "treatment": {"mean": 8.5, "se": 2.1},
        "placebo": {"mean": 2.2, "se": 2.0},
        "p_value": 0.028
      },
      "composite_hf_hospitalization_cv_death": {
        "treatment": {"events": 8, "rate": 0.087},
        "placebo": {"events": 15, "rate": 0.158},
        "hr": 0.52,
        "ci_95": [0.22, 1.22],
        "p_value": 0.13
      }
    }
  },
  "safety_summary": {
    "treatment": {
      "any_ae": 68,
      "serious_ae": 12,
      "death": 2,
      "discontinuation_ae": 6
    },
    "placebo": {
      "any_ae": 72,
      "serious_ae": 18,
      "death": 4,
      "discontinuation_ae": 8
    },
    "aesi": {
      "hypotension": {"treatment": 8, "placebo": 3},
      "renal_impairment": {"treatment": 5, "placebo": 4},
      "hyperkalemia": {"treatment": 6, "placebo": 5}
    }
  },
  "conclusions": {
    "primary_met": true,
    "effect_size": "clinically_meaningful",
    "safety": "acceptable",
    "recommendation": "proceed_to_phase3",
    "phase3_design_considerations": [
      "Consider composite CV death/HF hospitalization as primary",
      "Longer duration (12-24 months) for outcomes study",
      "Stratify by baseline NT-proBNP quartile"
    ]
  }
}
```

---

## Validation Rules

| Field | Rule | Error Handling |
|-------|------|----------------|
| `p0` | 0 < p0 < p1 < 1 | Error if violated |
| `alpha` | Typically 0.05-0.10 | Warn if outside range |
| `power` | 1 - beta, typically 0.80-0.90 | Warn if < 0.80 |
| `n1` | < n_total | Error if n1 >= n |
| `r1` | < r | Error if r1 >= r |
| `responses` | ≤ enrolled | Error if exceeded |
| `dose_levels` | Monotonically increasing | Warn if not |
| `response_rate` | Consistent with design | Flag if extreme |

### Design-Specific Validation

**Simon's Two-Stage:**
- Stage 1 decision must match threshold comparison
- Total responses must match sum of stages
- Final decision must match r threshold

**MCP-Mod:**
- At least 4 dose levels recommended
- Placebo/control arm required
- Model parameters must be biologically plausible

---

## Business Rules

### Phase 2a Rules

1. **Single primary endpoint** - Focus on one efficacy measure
2. **Historical control acceptable** - But reduces confidence
3. **Early termination binding** - If futility met, must stop
4. **Sample size fixed** - No re-estimation in classic designs

### Phase 2b Rules

1. **Multiple doses required** - At least 3-4 active doses
2. **Control arm essential** - Placebo or active comparator
3. **Dose-response must be demonstrated** - Before Phase 3 dose selection
4. **Safety at selected dose** - Adequate exposure at RP3D

### Endpoint Rules

1. **Clinically meaningful threshold** - Pre-specify MCID
2. **Appropriate analysis method** - MMRM for longitudinal, logistic for binary
3. **Missing data handling** - Pre-specify imputation strategy
4. **Multiplicity control** - If multiple endpoints or doses

---

## Cross-Product Integration

### From Phase 1 to Phase 2

```
Phase 1 Completion → Phase 2 Initiation:
├── RP2D from Phase 1 → Phase 2a dose
├── Safety profile → Monitoring plan
├── PK parameters → Dosing schedule
├── Preliminary signals → Endpoint selection
└── Expansion cohort data → Enrichment strategy
```

### To Phase 3

```
Phase 2 Completion → Phase 3 Planning:
├── Effect size → Sample size calculation
├── Selected dose → Phase 3 dose
├── Endpoint performance → Primary endpoint selection
├── Subgroup signals → Stratification factors
└── Safety profile → Exclusion criteria
```

---

## Related Skills

| Skill | Integration |
|-------|-------------|
| [Phase 1 Dose Escalation](phase1-dose-escalation.md) | Seamless Phase 1/2 designs |
| [Phase 3 Pivotal](phase3-pivotal.md) | Transition to confirmatory trials |
| [SDTM Demographics (DM)](domains/demographics-dm.md) | Subject baseline data |
| [SDTM Adverse Events (AE)](domains/adverse-events-ae.md) | Safety endpoint data |
| [SDTM Disposition (DS)](domains/disposition-ds.md) | Discontinuation tracking |
| [Oncology Trials](therapeutic-areas/oncology.md) | Cancer-specific Phase 2 patterns |
| [CNS Trials](therapeutic-areas/cns.md) | Psychiatric scale endpoints |
| [Cardiovascular Trials](therapeutic-areas/cardiovascular.md) | CV biomarker endpoints |
| [Recruitment & Enrollment](recruitment-enrollment.md) | Screen failure patterns |

---

## References

- Simon R. Optimal two-stage designs for phase II clinical trials. Control Clin Trials. 1989;10(1):1-10.
- Bryant J, Day R. Incorporating toxicity considerations into the design of two-stage phase II clinical trials. Biometrics. 1995;51(4):1372-1383.
- Bretz F, et al. Combining multiple comparisons and modeling techniques in dose-response studies. Biometrics. 2005;61(3):738-748.
- FDA Guidance: Adaptive Designs for Clinical Trials of Drugs and Biologics. 2019.
- EMA Qualification Opinion on MCP-Mod. 2014.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-12-20 | Initial comprehensive Phase 2 skill |

