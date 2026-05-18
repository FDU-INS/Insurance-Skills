---
name: phase1-dose-escalation
description: |
  Generate Phase 1 dose escalation trial data including first-in-human (FIH) studies, 
  MTD determination, DLT assessment, and PK/PD sampling. Supports 3+3, BOIN, CRM, 
  mTPI designs. Triggers: "phase 1", "dose escalation", "first-in-human", "FIH", 
  "MTD", "DLT", "SAD", "MAD", "3+3", "BOIN", "CRM".
---

# Phase 1 Dose Escalation Trials

Generate realistic Phase 1 clinical trial data for dose escalation studies, including first-in-human (FIH) trials, maximum tolerated dose (MTD) determination, and pharmacokinetic characterization.

---

## For Claude

This is a **trial phase skill** for generating Phase 1 dose escalation data. Apply when users request first-in-human studies, dose-finding trials, or early clinical development data.

**Always apply this skill when you see:**
- Phase 1, Phase I, or first-in-human (FIH) trial requests
- Dose escalation, MTD, or DLT references
- SAD (single ascending dose) or MAD (multiple ascending dose)
- Design names: 3+3, BOIN, CRM, mTPI, Keyboard
- PK sampling or pharmacokinetic study requests
- Starting dose or dose-toxicity discussions

**Combine with:**
- Therapeutic area skills (oncology.md, cns.md) for disease-specific patterns
- SDTM domain skills for regulatory-compliant data structures

---

## Phase 1 Trial Characteristics

| Aspect | Typical Values |
|--------|----------------|
| **Sample Size** | 20-80 subjects (escalation), up to 100+ with expansion |
| **Duration** | 6-18 months |
| **Sites** | 1-5 specialized centers |
| **Population** | Healthy volunteers or patients (indication-dependent) |
| **Primary Objective** | Safety, tolerability, MTD/RP2D determination |
| **Secondary Objectives** | PK characterization, preliminary PD/efficacy |

### Population Selection

| Therapeutic Area | Population | Rationale |
|-----------------|------------|-----------|
| Oncology | Patients with advanced/refractory disease | Ethical (can't expose healthy to cytotoxic) |
| CNS | Healthy volunteers → patients | Start safe, then disease population |
| Cardiovascular | Healthy volunteers | Safe initial assessment |
| Infectious Disease | Healthy volunteers | Vaccine/antimicrobial safety |
| Rare Disease | Patients | Limited population availability |

---

## Study Design Components

### Single Ascending Dose (SAD)

Sequential cohorts receive single doses of increasing strength.

```
Cohort Structure:
┌─────────┬────────────┬─────────────┬─────────────────┐
│ Cohort  │ Dose Level │ N (Active)  │ N (Placebo)     │
├─────────┼────────────┼─────────────┼─────────────────┤
│ 1       │ Starting   │ 6           │ 2               │
│ 2       │ Level 2    │ 6           │ 2               │
│ 3       │ Level 3    │ 6           │ 2               │
│ ...     │ ...        │ ...         │ ...             │
│ N       │ MTD        │ 6           │ 2               │
└─────────┴────────────┴─────────────┴─────────────────┘
```

**Key Features:**
- Sentinel dosing: First 1-2 subjects dosed, safety review before rest of cohort
- Intensive PK sampling over 24-72 hours
- Safety follow-up period (typically 7-14 days) before next cohort
- Placebo subjects for blinding (typically 6:2 or 3:1 ratio)

### Multiple Ascending Dose (MAD)

Sequential cohorts receive multiple doses over days/weeks.

```
Cohort Structure:
┌─────────┬────────────┬─────────────┬─────────────────┬─────────────┐
│ Cohort  │ Dose Level │ Frequency   │ Duration        │ N (Act:Pbo) │
├─────────┼────────────┼─────────────┼─────────────────┼─────────────┤
│ 1       │ Level 1    │ QD          │ 7 days          │ 8:2         │
│ 2       │ Level 2    │ QD          │ 7 days          │ 8:2         │
│ 3       │ Level 3    │ QD          │ 14 days         │ 8:2         │
│ 4       │ Level 4    │ BID         │ 14 days         │ 8:2         │
└─────────┴────────────┴─────────────┴─────────────────┴─────────────┘
```

**Key Features:**
- PK sampling on Day 1 and at steady state
- Safety labs at baseline, mid-treatment, end of treatment
- Trough samples for accumulation assessment

---

## Dose Escalation Designs

### 3+3 Design (Rule-Based)

The traditional algorithm-based design using fixed rules.

**Decision Rules:**
```
At current dose level:
├── 0/3 DLTs → Escalate to next dose
├── 1/3 DLTs → Enroll 3 more subjects
│   ├── 1/6 DLTs → Escalate to next dose
│   └── ≥2/6 DLTs → MTD exceeded, de-escalate
├── ≥2/3 DLTs → MTD exceeded, de-escalate
└── MTD = Highest dose with <33% DLT rate
```

**Advantages:** Simple, transparent, no statistical expertise required
**Limitations:** Conservative, many patients at subtherapeutic doses, imprecise MTD

### BOIN Design (Model-Assisted)

Bayesian Optimal Interval design using pre-calculated boundaries.

**Parameters:**
- Target DLT rate (φ): typically 0.25-0.33
- Escalation boundary (λe): typically 0.6 × φ
- De-escalation boundary (λd): typically 1.4 × φ

**Decision Rules (for φ = 0.25):**
| Observed DLT Rate | Decision |
|-------------------|----------|
| ≤ 0.157 (λe) | Escalate |
| 0.157 < rate < 0.359 | Stay |
| ≥ 0.359 (λd) | De-escalate |

**Pre-tabulated Decisions (φ = 0.25, cohort = 3):**
| DLTs/N | 0/3 | 1/3 | 2/3 | 3/3 |
|--------|-----|-----|-----|-----|
| Decision | E | S | D | D |

E = Escalate, S = Stay, D = De-escalate

**Advantages:** Easy to implement, good performance, transparent
**Limitations:** Requires pre-specification of boundaries

### Continual Reassessment Method (CRM, Model-Based)

Bayesian model-based design that updates dose-toxicity curve after each cohort.

**Key Components:**
- Dose-toxicity model: P(DLT|d) = d^exp(β)
- Prior distribution on β
- Target DLT probability (typically 0.25-0.33)
- After each cohort: Update posterior, select dose closest to target

**Advantages:** Most accurate MTD identification, uses all accumulated data
**Limitations:** Requires statistical expertise, potential for irrational decisions

### mTPI-2 / Keyboard Design (Model-Assisted)

Uses toxicity probability intervals to guide decisions.

**Intervals:**
- Underdosing: [0, φ - ε1]
- Target: [φ - ε1, φ + ε2]  
- Overdosing: [φ + ε2, 1]

**Decision:** Based on which interval has highest posterior probability

---

## Starting Dose Determination

### NOAEL-Based Approach (FDA Guidance)

```
Step 1: Identify NOAEL from most appropriate animal species
Step 2: Convert to Human Equivalent Dose (HED)
        HED = Animal Dose × (Animal Km / Human Km)
        
        Km values by species:
        ┌──────────┬────────┐
        │ Species  │ Km     │
        ├──────────┼────────┤
        │ Mouse    │ 3      │
        │ Rat      │ 6      │
        │ Rabbit   │ 12     │
        │ Monkey   │ 12     │
        │ Dog      │ 20     │
        │ Human    │ 37     │
        └──────────┴────────┘

Step 3: Apply safety factor (typically 10x)
        MRSD = HED / 10
```

### MABEL-Based Approach (EMA Guidance)

For high-risk biologics and immunomodulatory agents:

```
MABEL = Minimum Anticipated Biological Effect Level

Based on:
- Receptor occupancy (typically 10-20% occupancy)
- EC10 from in vitro potency assays
- Lowest pharmacologically active dose in animals
- PK/PD modeling predictions
```

---

## Dose-Limiting Toxicity (DLT) Definitions

### Standard DLT Criteria

| Category | DLT Definition |
|----------|----------------|
| **Hematologic** | Grade 4 neutropenia >7 days, febrile neutropenia, Grade 4 thrombocytopenia, Grade 3 thrombocytopenia with bleeding |
| **Non-Hematologic** | Grade 3-4 toxicity (except nausea/vomiting controlled with antiemetics, alopecia, fatigue <7 days) |
| **Hepatic** | Grade 3 AST/ALT elevation, Grade 2 bilirubin with transaminases |
| **Cardiac** | QTc prolongation >500ms or >60ms increase from baseline |
| **Dose Modifications** | Inability to receive ≥75% of planned doses due to toxicity |

### DLT Evaluation Window

| Study Type | DLT Window | Rationale |
|------------|------------|-----------|
| Cytotoxic chemotherapy | Cycle 1 (21-28 days) | Acute toxicity assessment |
| Targeted therapy | 28 days | May have delayed onset |
| Immunotherapy | 6-8 weeks | Immune-related AEs delayed |
| Cell therapy | 28 days (CRS), 8 weeks (neurotox) | Different toxicity kinetics |

---

## Pharmacokinetic Sampling

### Intensive PK Schedule (SAD)

| Time Point | Sample Type | Purpose |
|------------|-------------|---------|
| Pre-dose | Baseline | Confirm no drug present |
| 0.25, 0.5, 1h | Absorption | Tmax determination |
| 2, 4, 6, 8h | Distribution | Cmax, early elimination |
| 12, 24h | Elimination | Terminal phase |
| 48, 72h | Extended | Long half-life drugs |
| 96, 168h | Optional | Very long half-life |

### Sparse PK Schedule (MAD)

| Day | Time Points | Purpose |
|-----|-------------|---------|
| Day 1 | Pre, 1, 2, 4, 8, 12h | First dose characterization |
| Days 2-6 | Pre-dose (trough) | Accumulation assessment |
| Day 7 | Full profile | Steady-state characterization |
| Day 14 | Pre-dose | Extended steady-state |

### PK Parameters Generated

| Parameter | Description | Units |
|-----------|-------------|-------|
| Cmax | Maximum concentration | ng/mL |
| Tmax | Time to maximum | hours |
| AUC0-t | Area under curve (0 to last) | ng·h/mL |
| AUC0-inf | Area under curve (0 to infinity) | ng·h/mL |
| t½ | Terminal half-life | hours |
| CL/F | Apparent clearance | L/h |
| Vd/F | Apparent volume of distribution | L |
| Rac | Accumulation ratio | dimensionless |

---

## Expansion Cohorts

After MTD/RP2D determination, expansion cohorts provide additional data.

### Expansion Cohort Objectives

| Objective | Cohort Size | Design |
|-----------|-------------|--------|
| Additional safety at RP2D | 10-20 | Single-arm |
| Preliminary efficacy signal | 20-40 | Simon's two-stage |
| Biomarker development | 15-30 | Enriched population |
| Alternative schedule | 10-20 | Different dosing regimen |
| Combination therapy | 15-30 | With standard of care |
| Special populations | 10-20 | Renal/hepatic impairment |

---

## Generation Patterns

### Pattern 1: Standard 3+3 Escalation

```json
{
  "study_type": "phase1_dose_escalation",
  "design": "3+3",
  "dose_levels": [
    {"level": 1, "dose": 10, "unit": "mg", "n_enrolled": 3, "n_dlt": 0, "decision": "escalate"},
    {"level": 2, "dose": 25, "unit": "mg", "n_enrolled": 3, "n_dlt": 0, "decision": "escalate"},
    {"level": 3, "dose": 50, "unit": "mg", "n_enrolled": 3, "n_dlt": 1, "decision": "expand"},
    {"level": 3, "dose": 50, "unit": "mg", "n_enrolled": 6, "n_dlt": 1, "decision": "escalate"},
    {"level": 4, "dose": 100, "unit": "mg", "n_enrolled": 3, "n_dlt": 2, "decision": "mtd_exceeded"},
    {"level": 3, "dose": 50, "unit": "mg", "mtd": true}
  ],
  "total_enrolled": 18,
  "mtd_dose": 50,
  "mtd_unit": "mg"
}
```

### Pattern 2: BOIN Design with PK

```json
{
  "study_type": "phase1_fih",
  "design": "BOIN",
  "target_dlt_rate": 0.25,
  "boundaries": {
    "escalation": 0.157,
    "de_escalation": 0.359
  },
  "dose_levels": [
    {
      "level": 1,
      "dose": 0.1,
      "unit": "mg/kg",
      "n_enrolled": 3,
      "n_dlt": 0,
      "observed_dlt_rate": 0.0,
      "decision": "escalate",
      "pk_summary": {
        "cmax_mean": 45.2,
        "cmax_cv": 32,
        "auc_mean": 312,
        "auc_cv": 28,
        "half_life_mean": 8.5
      }
    }
  ]
}
```

### Pattern 3: Oncology FIH with Expansion

```json
{
  "study_type": "phase1_oncology",
  "design": "accelerated_titration_3+3",
  "population": "advanced_solid_tumors",
  "parts": {
    "dose_escalation": {
      "n_subjects": 24,
      "n_dose_levels": 8,
      "mtd_dose": "400mg",
      "rp2d": "400mg QD"
    },
    "dose_expansion": {
      "cohorts": [
        {"name": "NSCLC", "n": 20, "orr": 0.15},
        {"name": "Melanoma", "n": 20, "orr": 0.25},
        {"name": "CRC", "n": 20, "orr": 0.10}
      ]
    }
  }
}
```

---

## Examples

### Example 1: First-in-Human SAD/MAD Study

**Request:** "Generate a first-in-human Phase 1 study for a novel oral small molecule"

```json
{
  "study": {
    "study_id": "ABC-101",
    "title": "First-in-Human Single and Multiple Ascending Dose Study of ABC-001",
    "phase": "1",
    "design": "randomized_placebo_controlled",
    "population": "healthy_volunteers"
  },
  "part_a_sad": {
    "design": "3+3_modified",
    "cohorts": [
      {
        "cohort_id": "SAD-1",
        "dose_mg": 5,
        "subjects": [
          {"usubjid": "ABC101-001", "arm": "active", "dlt": false},
          {"usubjid": "ABC101-002", "arm": "active", "dlt": false},
          {"usubjid": "ABC101-003", "arm": "active", "dlt": false},
          {"usubjid": "ABC101-004", "arm": "active", "dlt": false},
          {"usubjid": "ABC101-005", "arm": "active", "dlt": false},
          {"usubjid": "ABC101-006", "arm": "active", "dlt": false},
          {"usubjid": "ABC101-007", "arm": "placebo", "dlt": false},
          {"usubjid": "ABC101-008", "arm": "placebo", "dlt": false}
        ],
        "pk_parameters": {
          "cmax_ng_ml": {"mean": 12.3, "sd": 3.2},
          "tmax_h": {"median": 1.5, "range": [1.0, 3.0]},
          "auc_0_inf_ng_h_ml": {"mean": 98.5, "sd": 22.1},
          "t_half_h": {"mean": 6.2, "sd": 1.1}
        },
        "decision": "escalate"
      },
      {
        "cohort_id": "SAD-2",
        "dose_mg": 15,
        "subjects": [
          {"usubjid": "ABC101-009", "arm": "active", "dlt": false},
          {"usubjid": "ABC101-010", "arm": "active", "dlt": false},
          {"usubjid": "ABC101-011", "arm": "active", "dlt": false},
          {"usubjid": "ABC101-012", "arm": "active", "dlt": false},
          {"usubjid": "ABC101-013", "arm": "active", "dlt": false},
          {"usubjid": "ABC101-014", "arm": "active", "dlt": false},
          {"usubjid": "ABC101-015", "arm": "placebo", "dlt": false},
          {"usubjid": "ABC101-016", "arm": "placebo", "dlt": false}
        ],
        "pk_parameters": {
          "cmax_ng_ml": {"mean": 35.8, "sd": 8.9},
          "tmax_h": {"median": 2.0, "range": [1.0, 4.0]},
          "auc_0_inf_ng_h_ml": {"mean": 295.2, "sd": 65.3},
          "t_half_h": {"mean": 6.5, "sd": 1.3}
        },
        "decision": "escalate"
      },
      {
        "cohort_id": "SAD-3",
        "dose_mg": 50,
        "subjects": [
          {"usubjid": "ABC101-017", "arm": "active", "dlt": false},
          {"usubjid": "ABC101-018", "arm": "active", "dlt": false},
          {"usubjid": "ABC101-019", "arm": "active", "dlt": true, "dlt_term": "Grade 3 headache"},
          {"usubjid": "ABC101-020", "arm": "active", "dlt": false},
          {"usubjid": "ABC101-021", "arm": "active", "dlt": false},
          {"usubjid": "ABC101-022", "arm": "active", "dlt": false},
          {"usubjid": "ABC101-023", "arm": "placebo", "dlt": false},
          {"usubjid": "ABC101-024", "arm": "placebo", "dlt": false}
        ],
        "pk_parameters": {
          "cmax_ng_ml": {"mean": 118.5, "sd": 28.2},
          "tmax_h": {"median": 2.0, "range": [1.5, 3.5]},
          "auc_0_inf_ng_h_ml": {"mean": 985.3, "sd": 198.6},
          "t_half_h": {"mean": 6.8, "sd": 1.5}
        },
        "decision": "escalate"
      },
      {
        "cohort_id": "SAD-4",
        "dose_mg": 100,
        "subjects": [
          {"usubjid": "ABC101-025", "arm": "active", "dlt": false},
          {"usubjid": "ABC101-026", "arm": "active", "dlt": true, "dlt_term": "Grade 3 nausea"},
          {"usubjid": "ABC101-027", "arm": "active", "dlt": true, "dlt_term": "Grade 3 vomiting"},
          {"usubjid": "ABC101-028", "arm": "placebo", "dlt": false}
        ],
        "pk_parameters": {
          "cmax_ng_ml": {"mean": 245.2, "sd": 52.1},
          "tmax_h": {"median": 2.5, "range": [2.0, 4.0]},
          "auc_0_inf_ng_h_ml": {"mean": 2012.5, "sd": 385.2}
        },
        "decision": "mtd_exceeded"
      }
    ],
    "mtd": {
      "dose_mg": 50,
      "rationale": "100mg exceeded MTD with 2/3 DLTs; 50mg had 1/6 DLTs (16.7%)"
    }
  },
  "part_b_mad": {
    "design": "sequential_cohort",
    "dosing_duration_days": 14,
    "cohorts": [
      {
        "cohort_id": "MAD-1",
        "dose_mg": 15,
        "frequency": "QD",
        "n_active": 8,
        "n_placebo": 2,
        "n_completers": 10,
        "dlts": 0,
        "steady_state_pk": {
          "cmax_ss_ng_ml": {"mean": 42.1, "sd": 10.5},
          "cmin_ss_ng_ml": {"mean": 8.2, "sd": 2.1},
          "accumulation_ratio": 1.35
        }
      },
      {
        "cohort_id": "MAD-2",
        "dose_mg": 30,
        "frequency": "QD",
        "n_active": 8,
        "n_placebo": 2,
        "n_completers": 9,
        "dlts": 1,
        "steady_state_pk": {
          "cmax_ss_ng_ml": {"mean": 85.3, "sd": 19.2},
          "cmin_ss_ng_ml": {"mean": 16.8, "sd": 4.2},
          "accumulation_ratio": 1.42
        }
      }
    ],
    "rp2d": {
      "dose": "30mg QD",
      "rationale": "Acceptable safety profile, PK supports once daily dosing"
    }
  },
  "safety_summary": {
    "total_enrolled": 42,
    "total_aes": 68,
    "treatment_related_aes": 45,
    "serious_aes": 0,
    "discontinuations_due_to_ae": 2,
    "most_common_aes": [
      {"term": "Headache", "n": 18, "percent": 42.9},
      {"term": "Nausea", "n": 12, "percent": 28.6},
      {"term": "Fatigue", "n": 8, "percent": 19.0}
    ]
  }
}
```



### Example 2: BOIN Oncology Dose Escalation

**Request:** "Generate Phase 1 oncology trial using BOIN design for a novel kinase inhibitor"

```json
{
  "study": {
    "study_id": "KI-001",
    "title": "Phase 1 Dose Escalation Study of KI-001 in Advanced Solid Tumors",
    "phase": "1",
    "design": "BOIN",
    "population": "advanced_solid_tumors_refractory"
  },
  "design_parameters": {
    "target_dlt_rate": 0.30,
    "escalation_boundary": 0.197,
    "de_escalation_boundary": 0.419,
    "cohort_size": 3,
    "max_sample_size": 36
  },
  "dose_escalation": {
    "dose_levels": [
      {
        "level": 1,
        "dose": "50mg BID",
        "cohort": 1,
        "n_treated": 3,
        "n_dlt": 0,
        "observed_rate": 0.00,
        "decision": "escalate",
        "dlt_details": []
      },
      {
        "level": 2,
        "dose": "100mg BID",
        "cohort": 2,
        "n_treated": 3,
        "n_dlt": 0,
        "observed_rate": 0.00,
        "decision": "escalate",
        "dlt_details": []
      },
      {
        "level": 3,
        "dose": "200mg BID",
        "cohort": 3,
        "n_treated": 3,
        "n_dlt": 1,
        "observed_rate": 0.33,
        "decision": "stay",
        "dlt_details": [
          {
            "usubjid": "KI001-007",
            "dlt_term": "Grade 3 diarrhea",
            "dlt_onset_day": 18,
            "resolved": true,
            "resolution_day": 25
          }
        ]
      },
      {
        "level": 3,
        "dose": "200mg BID",
        "cohort": 4,
        "n_treated": 6,
        "n_dlt": 1,
        "observed_rate": 0.167,
        "decision": "escalate",
        "cumulative_at_dose": {"n": 6, "dlt": 1, "rate": 0.167}
      },
      {
        "level": 4,
        "dose": "300mg BID",
        "cohort": 5,
        "n_treated": 3,
        "n_dlt": 2,
        "observed_rate": 0.67,
        "decision": "de_escalate",
        "dlt_details": [
          {
            "usubjid": "KI001-013",
            "dlt_term": "Grade 3 fatigue",
            "dlt_onset_day": 14
          },
          {
            "usubjid": "KI001-015",
            "dlt_term": "Grade 3 hypertension",
            "dlt_onset_day": 21
          }
        ]
      },
      {
        "level": 3,
        "dose": "200mg BID",
        "cohort": 6,
        "n_treated": 9,
        "n_dlt": 2,
        "observed_rate": 0.222,
        "decision": "mtd_declared",
        "isotonic_estimate": 0.22
      }
    ],
    "mtd_determination": {
      "mtd_dose": "200mg BID",
      "total_at_mtd": 9,
      "dlts_at_mtd": 2,
      "dlt_rate": 0.222,
      "target_rate": 0.30
    }
  },
  "pk_summary": {
    "dose_proportionality": "approximately_linear",
    "accumulation_ratio": 1.8,
    "half_life_h": 12.5,
    "steady_state_day": 5
  },
  "preliminary_efficacy": {
    "evaluable_for_response": 18,
    "best_responses": {
      "CR": 0,
      "PR": 2,
      "SD": 8,
      "PD": 8
    },
    "orr": 0.111,
    "dcr": 0.556
  }
}
```

### Example 3: Cell Therapy Phase 1 with Extended DLT Window

**Request:** "Generate Phase 1 CAR-T cell therapy dose escalation data"

```json
{
  "study": {
    "study_id": "CART-101",
    "title": "Phase 1 Study of CART-101 in Relapsed/Refractory B-cell Lymphoma",
    "phase": "1",
    "design": "3+3_modified",
    "population": "r_r_dlbcl"
  },
  "study_design": {
    "conditioning": "fludarabine_cyclophosphamide",
    "dlt_window": {
      "crs_window_days": 28,
      "neurotoxicity_window_days": 56
    },
    "dose_levels": [
      {"level": 1, "cells_per_kg": "1e6", "description": "1 × 10^6 CAR-T cells/kg"},
      {"level": 2, "cells_per_kg": "3e6", "description": "3 × 10^6 CAR-T cells/kg"},
      {"level": 3, "cells_per_kg": "1e7", "description": "1 × 10^7 CAR-T cells/kg"}
    ]
  },
  "dose_escalation": [
    {
      "level": 1,
      "dose": "1e6 cells/kg",
      "subjects": [
        {
          "usubjid": "CART101-001",
          "crs_grade": 1,
          "crs_onset_day": 3,
          "icans_grade": 0,
          "dlt": false,
          "response_d28": "CR"
        },
        {
          "usubjid": "CART101-002",
          "crs_grade": 2,
          "crs_onset_day": 5,
          "icans_grade": 1,
          "dlt": false,
          "response_d28": "PR"
        },
        {
          "usubjid": "CART101-003",
          "crs_grade": 1,
          "crs_onset_day": 4,
          "icans_grade": 0,
          "dlt": false,
          "response_d28": "CR"
        }
      ],
      "decision": "escalate"
    },
    {
      "level": 2,
      "dose": "3e6 cells/kg",
      "subjects": [
        {
          "usubjid": "CART101-004",
          "crs_grade": 2,
          "crs_onset_day": 2,
          "icans_grade": 2,
          "dlt": false,
          "response_d28": "CR"
        },
        {
          "usubjid": "CART101-005",
          "crs_grade": 3,
          "crs_onset_day": 3,
          "tocilizumab_doses": 2,
          "icans_grade": 1,
          "dlt": false,
          "response_d28": "CR"
        },
        {
          "usubjid": "CART101-006",
          "crs_grade": 2,
          "crs_onset_day": 4,
          "icans_grade": 3,
          "icans_onset_day": 8,
          "dlt": true,
          "dlt_term": "Grade 3 ICANS",
          "response_d28": "PR"
        }
      ],
      "decision": "expand"
    },
    {
      "level": 2,
      "dose": "3e6 cells/kg",
      "expansion": true,
      "total_n": 6,
      "total_dlt": 1,
      "dlt_rate": 0.167,
      "decision": "escalate"
    },
    {
      "level": 3,
      "dose": "1e7 cells/kg",
      "subjects": [
        {
          "usubjid": "CART101-010",
          "crs_grade": 3,
          "icans_grade": 3,
          "dlt": true,
          "dlt_term": "Grade 3 ICANS requiring ICU"
        },
        {
          "usubjid": "CART101-011",
          "crs_grade": 4,
          "icans_grade": 2,
          "dlt": true,
          "dlt_term": "Grade 4 CRS"
        },
        {
          "usubjid": "CART101-012",
          "crs_grade": 3,
          "icans_grade": 4,
          "dlt": true,
          "dlt_term": "Grade 4 ICANS"
        }
      ],
      "decision": "mtd_exceeded"
    }
  ],
  "mtd_determination": {
    "mtd_dose": "3e6 cells/kg",
    "rp2d": "3e6 cells/kg",
    "rationale": "Level 3 exceeded MTD (3/3 DLTs); Level 2 demonstrated acceptable safety (1/6 DLTs)"
  },
  "efficacy_summary": {
    "evaluable": 9,
    "cr_rate": 0.667,
    "orr": 0.889,
    "median_time_to_response_days": 28
  }
}
```

---

## Validation Rules

| Field | Rule | Error Handling |
|-------|------|----------------|
| `dose_level` | Sequential integer starting at 1 | Auto-assign if missing |
| `n_dlt` | ≤ `n_treated` | Error if exceeded |
| `dlt_rate` | n_dlt / n_treated | Calculate if missing |
| `decision` | Must follow design algorithm | Validate against rules |
| `mtd` | Must be declared dose level | Verify DLT rate < target |
| `pk_parameters` | All positive values | Reject negative values |
| `dlt_onset_day` | Within DLT window | Flag if outside window |

### Design-Specific Validation

**3+3 Design:**
- Cohort size must be 3 (or 6 for expansion)
- Decision follows exact algorithm
- MTD is highest dose with <33% DLT rate

**BOIN Design:**
- Boundaries correctly calculated from target
- Decision matches boundary comparison
- Isotonic regression for final MTD

---

## Business Rules

### Dose Escalation Rules

1. **No dose skipping** - Cannot skip untested dose levels
2. **Minimum observation** - DLT window must complete before escalation decision
3. **Cohort completion** - All subjects in cohort must reach decision point
4. **Safety stopping** - If starting dose exceeds MTD, trial may stop

### PK Generation Rules

1. **Dose proportionality** - AUC and Cmax scale with dose (unless saturation)
2. **Variability** - CV typically 20-50% for PK parameters
3. **Half-life consistency** - Should be similar across dose levels
4. **Accumulation** - Predicted from half-life and dosing interval

### Safety Monitoring Rules

1. **Sentinel dosing** - First 1-2 subjects observed before cohort completion
2. **Cohort review** - Safety review committee (SRC) between cohorts
3. **Stopping rules** - Pre-defined criteria for early termination
4. **Blinding** - Maintain until database lock (placebo-controlled studies)

---

## Related Skills

| Skill | Integration |
|-------|-------------|
| [SDTM Demographics (DM)](domains/demographics-dm.md) | Subject identifiers, disposition |
| [SDTM Adverse Events (AE)](domains/adverse-events-ae.md) | DLT coding, safety data |
| [SDTM Exposure (EX)](domains/exposure-ex.md) | Dose administration records |
| [SDTM Disposition (DS)](domains/disposition-ds.md) | Screen failures, discontinuations |
| [Oncology Trials](therapeutic-areas/oncology.md) | Cancer-specific Phase 1 patterns |
| [CNS Trials](therapeutic-areas/cns.md) | Neurology Phase 1 considerations |
| [Cell & Gene Therapy](therapeutic-areas/cgt.md) | CAR-T, gene therapy dose escalation |
| [Phase 2 Proof-of-Concept](phase2-proof-of-concept.md) | Transition to Phase 2 |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-12-20 | Initial comprehensive Phase 1 skill |

