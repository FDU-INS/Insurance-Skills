---
name: value-based-care
description: "Value-based care arrangements including quality measures, HEDIS, risk adjustment, and alternative payment models. Triggers: value-based care, VBC, HEDIS, quality measures, risk adjustment, HCC, ACO, capitation, quality bonus, Stars rating"
---

# Value-Based Care Cohort

A cohort template for generating value-based care arrangements including quality measures, HEDIS, risk adjustment, and alternative payment models.

## For Claude

Use this skill when the user requests value-based care or quality measurement cohorts. This teaches you how to generate **realistic VBC arrangements** with quality metrics, risk adjustment, and payment models.

**When to apply this skill:**

- User mentions value-based care, VBC, or quality measures
- User requests HEDIS, STARS, or quality reporting
- User specifies risk adjustment, HCC, or attribution
- User asks for ACO or alternative payment model examples
- User needs pay-for-performance cohorts

**Key capabilities this skill provides:**

- How to structure quality measure reporting (HEDIS/STARS)
- How to model risk adjustment and HCC coding
- How to configure shared savings arrangements
- How to track member attribution to providers
- How to calculate quality bonuses and penalties

## Metadata

- **Type**: cohort-template
- **Version**: 1.0
- **Author**: MemberSim
- **Tags**: value-based-care, quality, HEDIS, risk-adjustment, payer
- **Updated**: 2025-01-15

## Purpose

This cohort generates realistic value-based care arrangements. It models quality measurement, risk adjustment, provider attribution, and alternative payment models used in population health management.

## When to Use This Skill

Apply this skill when the user's request involves:

**Direct Keywords**:

- "value-based care", "VBC", "quality measures"
- "HEDIS", "STARS", "quality payment"
- "risk adjustment", "HCC", "attribution"
- "ACO", "APM", "pay for performance"

**VBC Cohorts**:

- "Generate a quality bonus program"
- "Create a shared savings model"
- "Generate HEDIS measure compliance data"

## Trigger Phrases

- value-based care
- VBC
- quality measures
- HEDIS
- STARS
- quality payment
- pay for performance
- P4P
- risk adjustment
- HCC
- attribution
- quality bonus
- ACO
- alternative payment model
- APM

## Parameters

| Parameter | Type | Default | Options |
|-----------|------|---------|---------|
| program_type | string | quality_bonus | quality_bonus, shared_savings, bundled_payment, capitation |
| measure_domain | string | all | preventive, chronic, behavioral, pharmacy, patient_experience |
| performance_level | string | meets | below, meets, exceeds |
| attribution_model | string | pcp | pcp, specialist, facility, episode |

## Value-Based Care Overview

### Program Types

| Program | Description | Risk Level | Payment Model |
|---------|-------------|------------|---------------|
| **Quality Bonus** | Bonus for meeting quality metrics | None | FFS + bonus |
| **Shared Savings** | Share cost savings if quality met | Upside only | FFS + % savings |
| **Shared Risk** | Share savings/losses | Two-sided | FFS +/- % |
| **Bundled Payment** | Fixed payment for episode | Episode | Bundled rate |
| **Capitation** | Per-member-per-month payment | Full | PMPM |

### Quality Measure Domains

| Domain | Examples | Typical Weight |
|--------|----------|----------------|
| Preventive Care | Mammograms, colonoscopies, immunizations | 20% |
| Chronic Care | Diabetes control, BP control, statin therapy | 35% |
| Behavioral Health | Depression screening, SUD treatment | 15% |
| Pharmacy | Medication adherence, appropriate use | 15% |
| Patient Experience | CAHPS scores, access, communication | 15% |

## HEDIS Quality Measures

### Diabetes Care

| Measure ID | Measure Name | Numerator | Denominator |
|------------|--------------|-----------|-------------|
| CDC-HBD | HbA1c Control (<8%) | Members with A1C < 8% | Diabetics 18-75 |
| CDC-HBP | BP Control (<140/90) | Members with BP < 140/90 | Diabetics 18-75 |
| CDC-EYE | Eye Exam | Members with retinal exam | Diabetics 18-75 |
| CDC-KED | Kidney Health Evaluation | Members with eGFR and uACR | Diabetics 18-75 |
| SPD | Statin Therapy for Diabetes | Members on statin | Diabetics 40-75 with ASCVD risk |

### Cardiovascular

| Measure ID | Measure Name | Numerator | Denominator |
|------------|--------------|-----------|-------------|
| CBP | Controlling High Blood Pressure | BP < 140/90 | Hypertensives 18-85 |
| SPC | Statin Therapy for CVD | Members on statin | ASCVD patients |
| COA-BPR | Care for Older Adults - BP Review | BP reviewed | Members 66+ |

### Preventive Care

| Measure ID | Measure Name | Numerator | Denominator |
|------------|--------------|-----------|-------------|
| BCS | Breast Cancer Screening | Mammogram in 27 months | Women 50-74 |
| COL | Colorectal Cancer Screening | Screening per guidelines | Members 45-75 |
| CIS | Childhood Immunization Status | All required vaccines | Children turning 2 |
| IMA | Immunizations for Adolescents | Tdap, HPV, Meningococcal | Adolescents 13 |
| FLU | Flu Vaccinations for Adults | Flu shot | Adults 18+ |

### Behavioral Health

| Measure ID | Measure Name | Numerator | Denominator |
|------------|--------------|-----------|-------------|
| DSF | Depression Screening and Follow-up | Screened + follow-up if positive | Members 12+ |
| AMM | Antidepressant Medication Management | Adherent to antidepressant | Members with MDD |
| FUH | Follow-Up After Hospitalization for Mental Illness | 7-day follow-up | Discharged from inpatient psych |
| IET | Initiation and Engagement of SUD Treatment | Initiated and engaged | New SUD diagnosis |

### Medication Adherence

| Measure ID | Measure Name | Target | Population |
|------------|--------------|--------|------------|
| PDC-RASA | ACE/ARB Adherence | PDC >= 80% | Members on RASA |
| PDC-STA | Statin Adherence | PDC >= 80% | Members on statin |
| PDC-DM | Diabetes Medication Adherence | PDC >= 80% | Members on diabetes meds |

## Risk Adjustment / HCC

### Hierarchical Condition Categories

```json
{
  "hcc_model": "CMS-HCC V28",
  "purpose": "Adjust payment based on member health status",
  "process": [
    "1. Capture diagnosis codes from encounters and claims",
    "2. Map ICD-10 codes to HCC categories",
    "3. Calculate risk score based on demographics + HCCs",
    "4. Adjust capitation/quality benchmarks by risk"
  ]
}
```

### Common HCC Categories

| HCC | Category | Example ICD-10 | RAF Weight |
|-----|----------|----------------|------------|
| 19 | Diabetes with Complications | E11.22, E11.65 | 0.302 |
| 85 | CHF | I50.22, I50.32 | 0.323 |
| 111 | COPD | J44.1 | 0.335 |
| 18 | Diabetes without Complications | E11.9 | 0.105 |
| 96 | Specified Heart Arrhythmias | I48.91 | 0.288 |

### Risk Adjustment Data Elements

```json
{
  "member_risk_profile": {
    "member_id": "MEM001234",
    "demographics": {
      "age": 68,
      "gender": "F",
      "medicaid_eligible": false,
      "originally_disabled": false
    },
    "hcc_categories": [
      { "hcc": 19, "description": "Diabetes with Renal Manifestation", "source_icd10": "E11.22" },
      { "hcc": 85, "description": "CHF", "source_icd10": "I50.22" }
    ],
    "demographic_risk_score": 0.452,
    "disease_risk_score": 0.625,
    "total_risk_score": 1.077,
    "expected_cost": 12924.00
  }
}
```

## Attribution Models

### PCP Attribution

```json
{
  "attribution_model": "pcp",
  "rules": [
    {
      "priority": 1,
      "rule": "Member-selected PCP",
      "description": "Use PCP designated on enrollment"
    },
    {
      "priority": 2,
      "rule": "Plurality of E&M visits",
      "description": "PCP with most office visits in prior 12 months"
    },
    {
      "priority": 3,
      "rule": "Most recent E&M visit",
      "description": "PCP from most recent primary care visit"
    }
  ]
}
```

### Episode Attribution

```json
{
  "attribution_model": "episode",
  "episode_types": [
    {
      "episode": "Total Knee Replacement",
      "trigger": "CPT 27447",
      "duration": "90 days post-discharge",
      "attributed_to": "Operating surgeon",
      "included_costs": ["Surgery", "Inpatient", "SNF", "PT", "Readmissions"]
    },
    {
      "episode": "Pregnancy/Delivery",
      "trigger": "Delivery CPT codes",
      "duration": "Antepartum through 60 days postpartum",
      "attributed_to": "Delivering provider",
      "included_costs": ["Prenatal", "Delivery", "Postpartum", "Newborn"]
    }
  ]
}
```

## Quality Performance Calculation

### Measure Performance

```json
{
  "measure_performance": {
    "measure_id": "CDC-HBD",
    "measure_name": "HbA1c Control (<8%)",
    "measurement_period": "2024-01-01 to 2024-12-31",
    "denominator": {
      "criteria": "Diabetic members 18-75 with 2+ visits",
      "count": 1250
    },
    "numerator": {
      "criteria": "A1C < 8% during measurement period",
      "count": 1000
    },
    "exclusions": {
      "hospice": 15,
      "esrd": 8,
      "count": 23
    },
    "rate": 0.8163,
    "benchmark": {
      "25th_percentile": 0.68,
      "50th_percentile": 0.78,
      "75th_percentile": 0.85,
      "90th_percentile": 0.90
    },
    "percentile_rank": 72,
    "performance_level": "meets"
  }
}
```

### Overall Performance Score

```json
{
  "vbc_performance_summary": {
    "provider_tin": "12-3456789",
    "provider_name": "Springfield Medical Group",
    "measurement_year": 2024,
    "attributed_members": 2500,
    "total_quality_score": 82.5,
    "domain_scores": {
      "preventive_care": { "weight": 0.20, "score": 85.0, "weighted": 17.0 },
      "chronic_care": { "weight": 0.35, "score": 80.0, "weighted": 28.0 },
      "behavioral_health": { "weight": 0.15, "score": 78.0, "weighted": 11.7 },
      "pharmacy": { "weight": 0.15, "score": 88.0, "weighted": 13.2 },
      "patient_experience": { "weight": 0.15, "score": 84.0, "weighted": 12.6 }
    },
    "performance_tier": "Silver",
    "quality_bonus_earned": 125000.00
  }
}
```

## Incentive Calculations

### Quality Bonus Program

```json
{
  "quality_bonus_calculation": {
    "provider_tin": "12-3456789",
    "quality_pool": 500000.00,
    "calculation": {
      "base_pmpm": 15.00,
      "attributed_member_months": 30000,
      "maximum_bonus": 450000.00,
      "quality_score": 82.5,
      "score_threshold_for_bonus": 75.0,
      "bonus_percentage": 0.75,
      "earned_bonus": 337500.00
    },
    "tier_structure": [
      { "tier": "Bronze", "min_score": 60, "max_score": 69.99, "bonus_pct": 0.25 },
      { "tier": "Silver", "min_score": 70, "max_score": 79.99, "bonus_pct": 0.50 },
      { "tier": "Gold", "min_score": 80, "max_score": 89.99, "bonus_pct": 0.75 },
      { "tier": "Platinum", "min_score": 90, "max_score": 100, "bonus_pct": 1.00 }
    ]
  }
}
```

### Shared Savings

```json
{
  "shared_savings_calculation": {
    "provider_tin": "12-3456789",
    "performance_year": 2024,
    "financial_performance": {
      "benchmark_total_cost": 25000000.00,
      "actual_total_cost": 23500000.00,
      "gross_savings": 1500000.00,
      "minimum_savings_rate": 0.02,
      "savings_rate": 0.06
    },
    "quality_gate": {
      "passed": true,
      "minimum_score": 75.0,
      "actual_score": 82.5
    },
    "sharing_arrangement": {
      "savings_share_rate": 0.50,
      "savings_cap": 0.10,
      "earned_savings": 750000.00,
      "capped_savings": 750000.00
    },
    "final_payment": 750000.00
  }
}
```

## Care Gap Identification

### Member Care Gaps

```json
{
  "member_care_gaps": {
    "member_id": "MEM001234",
    "as_of_date": "2025-01-15",
    "open_gaps": [
      {
        "measure_id": "BCS",
        "measure_name": "Breast Cancer Screening",
        "gap_type": "missing_service",
        "due_date": "2025-12-31",
        "last_screening": "2022-03-15",
        "action_required": "Mammogram",
        "priority": "high"
      },
      {
        "measure_id": "PDC-STA",
        "measure_name": "Statin Adherence",
        "gap_type": "non_adherent",
        "current_pdc": 0.72,
        "target_pdc": 0.80,
        "days_gap": 28,
        "action_required": "Refill statin medication",
        "priority": "medium"
      }
    ],
    "closed_gaps_ytd": [
      {
        "measure_id": "FLU",
        "measure_name": "Flu Vaccination",
        "closed_date": "2024-10-15",
        "closing_claim": "CLM20241015000123"
      }
    ],
    "total_open_gaps": 2,
    "total_closed_gaps": 5
  }
}
```

### Provider Care Gap Report

```json
{
  "provider_care_gap_report": {
    "provider_npi": "1234567890",
    "as_of_date": "2025-01-15",
    "attributed_members": 450,
    "gap_summary": {
      "total_open_gaps": 312,
      "gaps_per_member": 0.69,
      "high_priority": 45,
      "medium_priority": 187,
      "low_priority": 80
    },
    "by_measure": [
      { "measure_id": "BCS", "open_gaps": 28, "denominator": 95, "gap_rate": 0.29 },
      { "measure_id": "COL", "open_gaps": 42, "denominator": 180, "gap_rate": 0.23 },
      { "measure_id": "CDC-HBD", "open_gaps": 18, "denominator": 85, "gap_rate": 0.21 },
      { "measure_id": "CBP", "open_gaps": 35, "denominator": 210, "gap_rate": 0.17 }
    ],
    "outreach_recommendations": [
      "Schedule mammogram outreach calls for 28 members",
      "Send colonoscopy reminder letters to 42 members",
      "Order A1C labs for 18 diabetic members"
    ]
  }
}
```

## Examples

### Example 1: VBC Performance Report

```json
{
  "vbc_performance_report": {
    "report_type": "quarterly_performance",
    "provider": {
      "tin": "12-3456789",
      "name": "Springfield Family Medicine",
      "npi": "1234567890"
    },
    "period": {
      "measurement_year": 2024,
      "quarter": "Q4",
      "as_of_date": "2024-12-31"
    },
    "attribution": {
      "total_attributed": 850,
      "new_this_quarter": 45,
      "termed_this_quarter": 32
    },
    "quality_measures": [
      {
        "measure_id": "CDC-HBD",
        "measure_name": "Diabetes A1C Control",
        "numerator": 142,
        "denominator": 175,
        "rate": 0.811,
        "target": 0.780,
        "status": "exceeds",
        "trend": "improving"
      },
      {
        "measure_id": "CBP",
        "measure_name": "Controlling Blood Pressure",
        "numerator": 285,
        "denominator": 350,
        "rate": 0.814,
        "target": 0.800,
        "status": "meets",
        "trend": "stable"
      },
      {
        "measure_id": "BCS",
        "measure_name": "Breast Cancer Screening",
        "numerator": 145,
        "denominator": 195,
        "rate": 0.744,
        "target": 0.780,
        "status": "below",
        "trend": "declining"
      }
    ],
    "financial_summary": {
      "ytd_claims_cost": 4250000.00,
      "benchmark_cost": 4500000.00,
      "variance": -250000.00,
      "variance_pct": -0.056,
      "projected_shared_savings": 125000.00
    },
    "action_items": [
      "Focus outreach on 50 members needing mammograms",
      "Schedule diabetes visits for 33 members with A1C > 9%",
      "Review statin therapy for 28 ASCVD patients"
    ]
  }
}
```

### Example 2: Member Quality Summary

```json
{
  "member_quality_summary": {
    "member_id": "MEM001234",
    "name": { "given_name": "Margaret", "family_name": "Thompson" },
    "age": 62,
    "conditions": ["E11.9", "I10", "E78.5"],
    "attributed_provider": {
      "npi": "1234567890",
      "name": "Dr. Sarah Williams"
    },
    "risk_score": 1.24,
    "quality_measures_applicable": [
      {
        "measure_id": "CDC-HBD",
        "status": "met",
        "last_a1c": { "value": 6.8, "date": "2024-11-15" }
      },
      {
        "measure_id": "CBP",
        "status": "met",
        "last_bp": { "systolic": 128, "diastolic": 78, "date": "2024-12-01" }
      },
      {
        "measure_id": "SPD",
        "status": "met",
        "statin_pdc": 0.92
      },
      {
        "measure_id": "BCS",
        "status": "gap",
        "last_mammogram": "2022-08-20",
        "due_by": "2025-08-20"
      }
    ],
    "care_gaps": 1,
    "next_recommended_actions": [
      "Schedule mammogram - overdue",
      "Annual wellness visit due in 3 months"
    ]
  }
}
```

### Example 3: Quality Incentive Payment

```json
{
  "quality_incentive_payment": {
    "provider_tin": "12-3456789",
    "provider_name": "Springfield Medical Group",
    "payment_period": "2024 Annual Settlement",
    "payment_date": "2025-03-15",
    "quality_performance": {
      "overall_score": 84.2,
      "performance_tier": "Gold",
      "measures_meeting_target": 12,
      "measures_below_target": 3
    },
    "incentive_calculation": {
      "base_incentive_pool": 200000.00,
      "quality_multiplier": 0.842,
      "gross_incentive": 168400.00,
      "adjustments": [
        { "description": "Improvement bonus (5+ point gain)", "amount": 10000.00 }
      ],
      "total_incentive": 178400.00
    },
    "breakdown_by_domain": [
      { "domain": "Preventive", "earned": 35000.00 },
      { "domain": "Chronic Care", "earned": 62000.00 },
      { "domain": "Behavioral", "earned": 25000.00 },
      { "domain": "Pharmacy", "earned": 28400.00 },
      { "domain": "Experience", "earned": 18000.00 },
      { "domain": "Improvement Bonus", "earned": 10000.00 }
    ],
    "payment_method": "EFT",
    "payment_reference": "VBC-2024-Q4-123456"
  }
}
```

## Validation Rules

| Rule | Requirement | Example |
|------|-------------|---------|
| Measure ID | Valid HEDIS/CMS measure | BCS (Breast Cancer Screening) |
| Measure rate | 0.0 to 1.0 or percentage | 0.85 (85%) |
| HCC code | Valid CMS-HCC | HCC 19 (Diabetes with complications) |
| RAF score | Positive decimal | 1.25 |
| Quality score | Within measure range | 4.5 Stars (1-5 scale) |
| Attribution | Member attributed to provider | Attributed via plurality |
| Measurement period | Valid date range | 2024-01-01 to 2024-12-31 |
| Payment model | Valid VBC type | Shared savings, capitation, bundled |

### Business Rules

- **HEDIS Measures**: Standardized quality measures with specific numerator/denominator definitions
- **Risk Adjustment**: HCC coding captures member acuity; drives capitation rates
- **Attribution**: Members attributed to PCPs based on plurality of visits
- **Quality Thresholds**: Bonus payments tied to meeting specific rate targets
- **Measurement Year**: Typically calendar year; lookback for continuous enrollment
- **Gap Closure**: Claims/encounters that close quality gaps within measurement period
- **Stars Ratings**: Medicare Advantage quality ratings (1-5 stars) affect rebates
- **Shared Savings**: Savings vs. benchmark shared between payer and provider

## Related Skills

- [SKILL.md](SKILL.md) - MemberSim overview
- [professional-claims.md](professional-claims.md) - Claims that close quality gaps
- [accumulator-tracking.md](accumulator-tracking.md) - Cost tracking for VBC
- [../../references/data-models.md](../../references/data-models.md) - Entity schemas
- [../../references/code-systems.md](../../references/code-systems.md) - HEDIS measure codes
