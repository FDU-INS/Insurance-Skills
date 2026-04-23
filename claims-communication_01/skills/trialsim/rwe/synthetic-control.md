---
name: rwe-synthetic-control
description: |
  Generate synthetic external control arms for single-arm trials using matched 
  real world data. Triggers: "synthetic control", "external control", 
  "historical control", "matched control", "propensity score".
---

# Synthetic Control Arm

Generate synthetic external control arms by matching trial-like populations from real world data sources.

---

## For Claude

This is an **RWE skill** for generating external control arms. Apply this when users want to create matched control populations for single-arm trials.

**Always apply this skill when you see:**
- Requests for external or synthetic control arms
- Historical control population generation
- Propensity score matching for trials
- Single-arm trial comparisons

---

## Synthetic Control Methodology

### Overview

1. **Define Target Population** - From trial eligibility criteria
2. **Identify RWD Source** - PatientSim + MemberSim + RxMemberSim
3. **Estimate Propensity Scores** - Model P(Trial | X)
4. **Match or Weight** - Create comparable populations
5. **Assess Balance** - Verify covariate balance (SMD < 0.1)
6. **Generate Dataset** - Matched population with outcomes

---

## Matching Variables

### Standard Oncology Set

| Category | Variables | Priority |
|----------|-----------|----------|
| **Demographics** | Age, sex | Required |
| **Disease** | Cancer type, stage, histology | Required |
| **Biomarkers** | PD-L1, mutations | Required if applicable |
| **Performance** | ECOG PS | Required |
| **Prior therapy** | Number of prior lines | Required |
| **Labs** | LDH, albumin, hemoglobin | Important |

---

## Balance Assessment

### Standardized Mean Difference (SMD)

| SMD Value | Interpretation |
|-----------|----------------|
| < 0.1 | Excellent balance |
| 0.1 - 0.2 | Acceptable |
| > 0.2 | Imbalance concern |

---

## Generation Patterns

### External Control Population

```json
{
  "synthetic_control": {
    "study_id": "ONCO-301",
    "trial_arm": {"name": "Experimental", "n": 150},
    "external_control": {
      "name": "Synthetic Control",
      "n_source_population": 2450,
      "n_matched": 150,
      "matching_method": "PROPENSITY_SCORE_1TO1",
      "matching_caliper": 0.2
    },
    "balance_assessment": {
      "overall_smd_max": 0.08,
      "all_smd_below_threshold": true
    }
  }
}
```

### Outcome Comparison

```json
{
  "outcome_comparison": {
    "primary_endpoint": "PFS",
    "trial_arm": {
      "n": 150, "median_pfs_months": 8.5
    },
    "external_control": {
      "n": 150, "median_pfs_months": 4.2
    },
    "comparison": {
      "hazard_ratio": 0.52,
      "hr_95ci": [0.40, 0.68],
      "p_value": "<0.0001"
    }
  }
}
```

---

## Validation Checklist

- [ ] Index date defined identically for trial and control
- [ ] All key prognostic factors included in matching
- [ ] SMD < 0.1 for all matched covariates
- [ ] Propensity score overlap assessed
- [ ] Sensitivity analyses pre-specified

---

## Related Skills

- [RWE Overview](overview.md) - RWE concepts and context
- [Clinical Trials Domain](../clinical-trials-domain.md) - Trial design
- [PatientSim](../../patientsim/SKILL.md) - Clinical data source

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-12 | Initial synthetic control skill |
