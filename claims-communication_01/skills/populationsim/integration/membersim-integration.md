---
name: membersim-integration
description: |
  Integration guide for PopulationSim to MemberSim data flow. Describes how 
  demographic, SDOH, and healthcare access data maps to health plan enrollment, 
  claims patterns, and risk adjustment.
---

# PopulationSim → MemberSim Integration

## Overview

This document describes how PopulationSim demographic, SDOH, and healthcare access data flows into MemberSim to generate realistic health plan enrollment and claims data.

---

## Integration Flow

```
PopulationProfile                    MemberSim
      │                                   │
      ├─ demographics ──────────────────► Member demographics
      │   └─ household_composition       │  └─ Coverage tier selection
      │                                   │
      ├─ healthcare_access ─────────────► Plan enrollment
      │   ├─ insurance_coverage          │  ├─ Plan type distribution
      │   └─ provider_access             │  └─ Network assignment
      │                                   │
      ├─ sdoh_profile ──────────────────► Risk & utilization
      │   ├─ economic_factors            │  ├─ Premium tier selection
      │   └─ z_code_mapping              │  └─ HCC risk adjustment
      │                                   │
      └─ utilization_patterns ──────────► Claims generation
          ├─ ed_visits_per_1k            │  ├─ Institutional claims
          └─ ambulatory_visits           │  └─ Professional claims
```

---

## Plan Distribution Mapping

### Insurance Coverage to Plan Type

PopulationSim insurance distribution drives MemberSim enrollment:

```json
// PopulationProfile input
{
  "healthcare_access": {
    "insurance_coverage": {
      "commercial": 0.482,
      "medicare": 0.148,
      "medicaid": 0.198,
      "dual_eligible": 0.032,
      "uninsured": 0.148
    }
  }
}

// MemberSim enrollment distribution
// 48.2% → Commercial plans (HMO, PPO, EPO, HDHP)
// 14.8% → Medicare Advantage or Traditional Medicare
// 19.8% → Medicaid Managed Care
// 3.2%  → Dual-eligible SNP plans
// 14.8% → No enrollment (self-pay/uninsured)
```

### Commercial Plan Type Distribution

Within commercial coverage, distribute by plan type based on geography:

| Area Type | HMO | PPO | EPO | HDHP |
|-----------|-----|-----|-----|------|
| Urban | 30% | 40% | 15% | 15% |
| Suburban | 25% | 45% | 10% | 20% |
| Rural | 15% | 55% | 5% | 25% |

```json
// MemberSim Member output
{
  "member_id": "MEM-000000001",
  "ssn": "123-45-6789",
  "enrollment": {
    "plan_type": "PPO",
    "plan_name": "Blue Choice PPO Gold",
    "metal_tier": "gold",
    "effective_date": "2024-01-01",
    "coverage_tier": "employee_spouse"
  }
}
```

---

## Coverage Tier Mapping

### Household Composition to Coverage Tier

```json
// PopulationProfile input
{
  "demographics": {
    "household_composition": {
      "average_household_size": 2.78,
      "family_households": 0.682,
      "single_person": 0.248,
      "single_parent": 0.142
    }
  }
}

// MemberSim coverage tier distribution
// EMP (Employee only): 24.8% (single_person)
// ESP (Employee + Spouse): 20% (estimated couples)
// ECH (Employee + Children): 14.2% (single_parent)
// FAM (Family): 40% (family_households - single_parent)
```

### Coverage Tier Codes

| Code | Description | Typical Distribution |
|------|-------------|---------------------|
| EMP | Employee only | 25-35% |
| ESP | Employee + spouse | 15-25% |
| ECH | Employee + child(ren) | 10-18% |
| FAM | Employee + family | 30-45% |

---

## SDOH-Driven Plan Selection

### Economic Factors to Premium Tier

```json
// PopulationProfile SDOH input
{
  "sdoh_profile": {
    "economic": {
      "median_household_income": 52400,
      "poverty_rate": 0.182
    }
  }
}

// MemberSim plan selection logic
// Median income < $40,000 → Bronze/Silver ACA or Medicaid
// Median income $40,000-$80,000 → Silver/Gold mix
// Median income > $80,000 → Gold/Platinum or employer-sponsored
```

### Metal Tier Distribution by Income

| Income Level | Bronze | Silver | Gold | Platinum |
|--------------|--------|--------|------|----------|
| Low (<150% FPL) | 30% | 50% | 15% | 5% |
| Moderate (150-300% FPL) | 20% | 45% | 30% | 5% |
| High (>300% FPL) | 10% | 25% | 45% | 20% |

---

## Utilization Pattern Integration

### Claims Frequency Calculation

```json
// PopulationProfile utilization input
{
  "utilization_patterns": {
    "ed_visits_per_1k": 428,
    "inpatient_admits_per_1k": 98,
    "ambulatory_visits_per_capita": 4.8,
    "avg_los_days": 4.2,
    "sdoh_adjustments": {
      "ed_multiplier": 1.18,
      "preventive_reduction": 0.88
    }
  }
}

// MemberSim claims generation rates (per member per year)
// ED visits: 0.428 (high-SDOH: 0.505)
// Inpatient: 0.098 (high-SDOH: 0.116)
// Office visits: 4.8 (high-SDOH: 4.2 preventive, 5.2 acute)
```

### SDOH-Adjusted Utilization

For high-vulnerability populations (SVI ≥ 0.75):

| Service Type | Base Rate | SDOH Multiplier | Adjusted Rate |
|--------------|-----------|-----------------|---------------|
| ED visits | 0.428 | 1.18 | 0.505 |
| Preventive | 0.62 | 0.88 | 0.546 |
| Acute ambulatory | 2.4 | 1.10 | 2.64 |
| Inpatient | 0.098 | 1.15 | 0.113 |

---

## Risk Adjustment Integration

### Z-Codes to HCC Mapping

PopulationSim SDOH Z-codes influence risk scores:

```json
// PopulationProfile Z-code rates
{
  "sdoh_profile": {
    "z_code_mapping": {
      "prevalence_rates": {
        "Z59.6": {"rate": 0.146},   // Low income
        "Z59.41": {"rate": 0.118},  // Food insecurity
        "Z59.82": {"rate": 0.070}   // Transportation insecurity
      }
    }
  }
}

// MemberSim risk impact
// Note: Z-codes don't directly map to HCCs but indicate:
// - Higher expected utilization
// - Lower medication adherence
// - Increased readmission risk
```

### Clinical Conditions to HCC

Map PopulationSim conditions to CMS-HCC risk factors:

| Condition | HCC | Risk Weight |
|-----------|-----|-------------|
| Diabetes w/o complications | HCC 19 | 0.105 |
| Diabetes with complications | HCC 18 | 0.302 |
| CHF | HCC 85 | 0.323 |
| COPD | HCC 111 | 0.335 |
| CKD Stage 4 | HCC 137 | 0.289 |

---

## Claims Generation

### Professional Claims (837P)

```json
// MemberSim 837P Claim
{
  "claim_id": "CLM-2024-000001",
  "member_id": "MEM-000000001",
  "claim_type": "professional",
  "service_date": "2024-03-15",
  "provider": {
    "npi": "1234567890",
    "name": "Dr. Smith",
    "specialty": "Internal Medicine"
  },
  "place_of_service": "11",
  "diagnosis_codes": ["E11.9", "I10", "Z59.6"],
  "procedure_codes": [
    {"cpt": "99214", "modifier": [], "units": 1, "charge": 175.00}
  ],
  "total_charge": 175.00,
  "allowed_amount": 125.00,
  "member_responsibility": 25.00,
  "plan_paid": 100.00
}
```

### Institutional Claims (837I)

```json
// MemberSim 837I Claim
{
  "claim_id": "CLM-2024-000002",
  "member_id": "MEM-000000001",
  "claim_type": "institutional",
  "admission_date": "2024-06-10",
  "discharge_date": "2024-06-14",
  "admission_type": "1",
  "admission_source": "7",
  "discharge_status": "01",
  "facility": {
    "npi": "9876543210",
    "name": "Houston General Hospital"
  },
  "drg": "291",
  "diagnosis_codes": {
    "principal": "J18.9",
    "secondary": ["E11.9", "I10", "Z59.6"]
  },
  "revenue_codes": [
    {"code": "0120", "units": 4, "charge": 4800.00},
    {"code": "0250", "units": 1, "charge": 350.00},
    {"code": "0300", "units": 1, "charge": 450.00}
  ],
  "total_charge": 28500.00,
  "allowed_amount": 18200.00,
  "member_responsibility": 2500.00,
  "plan_paid": 15700.00
}
```

---

## X12 834 Enrollment

### Member Enrollment Transaction

```
ST*834*0001*005010X220A1~
BGN*00*12456*20240101*0800****2~
N1*P5*Blue Cross Blue Shield*FI*123456789~
N1*IN*GARCIA, MARIA~
INS*Y*18*021*28*A***FT~
REF*0F*MEM-000000001~
REF*1L*123-45-6789~
DTP*336*D8*20240101~
NM1*IL*1*GARCIA*MARIA****34*123456789~
N3*1234 OAK ST~
N4*HOUSTON*TX*77004~
DMG*D8*19680722*F~
HD*021**HLT*PPO-GOLD-500~
DTP*348*D8*20240101~
SE*15*0001~
```

---

## Example: Complete Member Generation

### Input: Population-Based Cohort

```json
{
  "cohort_id": "cohort-commercial-harris-001",
  "geography": {"fips": "48201"},
  "integration": {
    "membersim": {
      "enabled": true,
      "plan_distribution": "population_based",
      "generate_claims": true,
      "timeframe": {
        "start": "2024-01-01",
        "end": "2024-12-31"
      }
    }
  },
  "size": {"target": 1000}
}
```

### Output: MemberSim Bundle

```json
{
  "bundle_id": "membersim-bundle-001",
  "generated_at": "2024-12-23T10:30:00Z",
  "summary": {
    "total_members": 1000,
    "plan_distribution": {
      "commercial": 482,
      "medicare": 148,
      "medicaid": 198,
      "uninsured": 172
    },
    "total_claims": 4250,
    "total_charges": 8500000.00,
    "total_paid": 5100000.00
  },
  "files": {
    "enrollment": "enrollment-834.x12",
    "professional_claims": "claims-837p.x12",
    "institutional_claims": "claims-837i.x12",
    "remittance": "remittance-835.x12"
  }
}
```

---

## Cost Calculation Patterns

### SDOH Impact on Costs

High-SDOH populations show different cost patterns:

| Cost Category | Baseline | High-SDOH Multiplier |
|---------------|----------|---------------------|
| ED costs | $2,400 PMPY | 1.25x |
| Inpatient costs | $4,200 PMPY | 1.18x |
| Pharmacy costs | $3,100 PMPY | 0.92x (lower adherence) |
| Preventive costs | $800 PMPY | 0.85x |
| Total medical | $10,500 PMPY | 1.12x |

---

## Related Skills

- [Geographic Intelligence](../geographic/county-profile.md)
- [Cohort Definition](../cohorts/cohort-specification.md)
- [MemberSim SKILL](../../membersim/SKILL.md)
- [Cross-Product Integration](cross-product-integration.md)
