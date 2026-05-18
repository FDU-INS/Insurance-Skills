# Population to Member Integration

## Overview

This scenario demonstrates how PopulationSim data flows into MemberSim to generate health plan member records with realistic plan selection, enrollment patterns, and SDOH-influenced utilization.

---

## Integration Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                      PopulationSim                               │
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │ Healthcare  │  │  Economic   │  │      SDOH Profile       │  │
│  │   Access    │  │  Factors    │  │                         │  │
│  │             │  │             │  │                         │  │
│  │ • Ins mix   │  │ • Income    │  │ • SVI: 0.72             │  │
│  │ • Uninsured │  │ • Poverty   │  │ • ADI: 72               │  │
│  │ • Medicaid  │  │ • Employ    │  │ • Z-codes               │  │
│  └──────┬──────┘  └──────┬──────┘  └───────────┬─────────────┘  │
│         │                │                      │                │
└─────────┼────────────────┼──────────────────────┼────────────────┘
          │                │                      │
          ▼                ▼                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                        MemberSim                                 │
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │  Enrollment │  │    Plan     │  │       Claims            │  │
│  │             │  │  Selection  │  │                         │  │
│  │ • Member ID │  │ • HMO/PPO   │  │ • Professional          │  │
│  │ • Coverage  │  │ • Metal     │  │ • Facility              │  │
│  │ • Effective │  │ • Deduct    │  │ • SDOH adjustments      │  │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Step-by-Step Workflow

### Step 1: Analyze Insurance Coverage Mix

**PopulationSim Output**:
```json
{
  "healthcare_access": {
    "insurance_coverage": {
      "commercial": 0.482,
      "medicare": 0.148,
      "medicaid": 0.228,
      "dual_eligible": 0.032,
      "uninsured": 0.142
    }
  },
  "economic_factors": {
    "median_household_income": 48200,
    "poverty_rate": 0.218,
    "income_distribution": {
      "below_poverty": 0.218,
      "100_200_fpl": 0.182,
      "200_400_fpl": 0.324,
      "above_400_fpl": 0.276
    }
  },
  "sdoh_profile": {
    "svi_overall": 0.72,
    "adi_national_percentile": 72
  }
}
```

### Step 2: Define Member Cohort

**MemberSim Skill**: `define-member-cohort`

```
User: Generate 1000 health plan members reflecting this 
population's insurance mix and economic profile.
```

**Cohort Specification**:
```json
{
  "cohort_id": "member-cohort-houston-sdoh-001",
  "size": 1000,
  "insurance_distribution": {
    "commercial": 0.55,
    "medicare": 0.17,
    "medicaid": 0.26,
    "dual": 0.02
  },
  "plan_selection_rules": {
    "commercial": {
      "income_based": true,
      "high_income": {"preferred": "PPO", "metal": "gold"},
      "moderate_income": {"preferred": "HMO", "metal": "silver"},
      "low_income": {"preferred": "HDHP", "metal": "bronze"}
    },
    "medicaid": {
      "managed_care": 0.85,
      "fee_for_service": 0.15
    }
  },
  "sdoh_considerations": {
    "apply_utilization_adjustments": true,
    "flag_high_risk_members": true
  }
}
```

### Step 3: Generate Member Records

**Plan Selection Logic by Income/SDOH**:

| Income Level | Commercial Plan | Medicare | Medicaid |
|--------------|-----------------|----------|----------|
| <138% FPL | - | - | Managed Care |
| 138-200% FPL | Exchange Bronze | Medicare Advantage | - |
| 200-400% FPL | Employer HMO/Silver | Medicare Advantage | - |
| >400% FPL | Employer PPO/Gold | Traditional + Supp | - |

---

## Data Mapping

### Insurance Coverage Mapping

| PopulationSim Field | MemberSim Field | Transformation |
|---------------------|-----------------|----------------|
| `insurance_coverage.commercial` | `enrollment.plan_type = "commercial"` | Direct assignment |
| `insurance_coverage.medicare` | `enrollment.plan_type = "medicare"` | Age-based selection |
| `insurance_coverage.medicaid` | `enrollment.plan_type = "medicaid"` | Income-based selection |
| `economic_factors.income_distribution` | `enrollment.plan_selection` | Income → plan type |

### SDOH to Utilization Mapping

| SDOH Factor | MemberSim Impact | Adjustment |
|-------------|------------------|------------|
| SVI ≥ 0.75 | ED claims | +20% |
| SVI ≥ 0.75 | Preventive claims | -18% |
| ADI ≥ 75 | Pharmacy adherence | -15% |
| Z59.6 present | Cost sharing burden | Flag for assistance |
| Z59.82 present | Missed appointments | +25% |

---

## Example Generated Member

### Commercial Member

```json
{
  "member": {
    "member_id": "MEM-456789",
    "subscriber_id": "SUB-123456",
    "person": {
      "ssn": "123-45-6789",
      "first_name": "Maria",
      "last_name": "Garcia",
      "date_of_birth": "1975-03-15",
      "gender": "F"
    },
    "relationship": "subscriber",
    "coverage_tier": "employee_plus_spouse"
  },
  
  "enrollment": {
    "plan": {
      "plan_id": "COMM-HMO-SILVER-2024",
      "plan_name": "Aetna HMO Silver",
      "plan_type": "HMO",
      "metal_tier": "silver",
      "carrier": "Aetna"
    },
    "effective_date": "2024-01-01",
    "term_date": null,
    "enrollment_reason": "open_enrollment",
    "premium_monthly": 485.00,
    "employer_contribution": 380.00,
    "employee_contribution": 105.00
  },
  
  "benefits": {
    "deductible_individual": 2500,
    "deductible_family": 5000,
    "oop_max_individual": 7500,
    "oop_max_family": 15000,
    "copay_pcp": 30,
    "copay_specialist": 50,
    "copay_er": 250,
    "coinsurance": 0.20
  },
  
  "accumulators": {
    "deductible_met": 1250.00,
    "oop_met": 2340.00,
    "as_of_date": "2024-09-30"
  },
  
  "sdoh_context": {
    "svi_score": 0.72,
    "adi_percentile": 72,
    "risk_flags": ["transportation_barrier", "food_insecurity"],
    "care_management_eligible": true,
    "utilization_adjustments": {
      "ed_multiplier": 1.18,
      "preventive_multiplier": 0.88
    }
  }
}
```

### Medicaid Member

```json
{
  "member": {
    "member_id": "MED-987654",
    "person": {
      "ssn": "234-56-7890",
      "first_name": "Carlos",
      "last_name": "Rodriguez",
      "date_of_birth": "1988-07-22",
      "gender": "M"
    },
    "relationship": "subscriber"
  },
  
  "enrollment": {
    "plan": {
      "plan_id": "MCAID-MCO-SUPERIOR-2024",
      "plan_name": "Superior HealthPlan",
      "plan_type": "medicaid_managed_care",
      "mco_name": "Superior"
    },
    "effective_date": "2024-02-01",
    "eligibility_category": "adult_expansion",
    "aid_code": "AX",
    "income_pct_fpl": 125
  },
  
  "benefits": {
    "cost_sharing": "minimal",
    "copay_pcp": 0,
    "copay_specialist": 0,
    "copay_er": 4,
    "pharmacy_copay": 1
  },
  
  "sdoh_context": {
    "svi_score": 0.82,
    "adi_percentile": 78,
    "z_codes_documented": ["Z59.6", "Z56.0"],
    "care_management": {
      "enrolled": true,
      "program": "chronic_care_management",
      "community_health_worker": true
    }
  }
}
```

---

## Claims Generation with SDOH Adjustments

### Utilization Rates by SDOH Level

| Service | Low SVI (<0.25) | Moderate (0.25-0.50) | High (0.50-0.75) | Very High (>0.75) |
|---------|-----------------|----------------------|------------------|-------------------|
| PCP visits/year | 4.2 | 3.8 | 3.2 | 2.8 |
| ED visits/year | 0.18 | 0.25 | 0.38 | 0.52 |
| Inpatient/1000 | 68 | 78 | 92 | 118 |
| Preventive | 78% | 72% | 62% | 54% |
| Rx adherence | 85% | 80% | 72% | 65% |

### Example Claim with SDOH Context

```json
{
  "claim": {
    "claim_id": "CLM-2024-789012",
    "member_id": "MEM-456789",
    "claim_type": "professional",
    "service_date": "2024-09-15",
    "provider": {
      "npi": "1234567890",
      "name": "Dr. Sarah Chen",
      "specialty": "Internal Medicine"
    },
    "diagnoses": [
      {"code": "E11.9", "type": "principal"},
      {"code": "I10", "type": "secondary"},
      {"code": "Z59.41", "type": "sdoh"}
    ],
    "procedures": [
      {"code": "99214", "units": 1, "charge": 185.00}
    ],
    "allowed_amount": 142.00,
    "paid_amount": 112.00,
    "member_responsibility": 30.00,
    
    "sdoh_flags": {
      "food_insecurity_documented": true,
      "referral_to_resources": true,
      "community_health_worker_notified": true
    }
  }
}
```

---

## Plan Selection Algorithm

### Income-Based Selection

```
function selectPlan(member, populationProfile):
    income = member.householdIncome
    fpl = calculateFPL(member.householdSize)
    incomePctFPL = income / fpl * 100
    
    if incomePctFPL <= 138:
        return selectMedicaidPlan(member, populationProfile)
    elif incomePctFPL <= 250:
        return selectExchangePlan(member, populationProfile, "silver")
    elif incomePctFPL <= 400:
        return selectExchangePlan(member, populationProfile, "gold")
    else:
        return selectEmployerPlan(member, populationProfile)
```

### SDOH Adjustment

```
function adjustUtilization(baseRate, sdohProfile):
    svi = sdohProfile.svi_overall
    
    if svi >= 0.75:
        edMultiplier = 1.22
        preventiveMultiplier = 0.82
    elif svi >= 0.50:
        edMultiplier = 1.08
        preventiveMultiplier = 0.92
    else:
        edMultiplier = 0.90
        preventiveMultiplier = 1.05
    
    return adjustedRates
```

---

## Validation Checklist

- [ ] Insurance mix matches population profile (±3%)
- [ ] Medicaid enrollment correlates with poverty rate
- [ ] Plan selection reflects income distribution
- [ ] ED utilization elevated for high-SVI members
- [ ] Preventive services reduced for high-vulnerability
- [ ] Z-codes appear on claims when appropriate
- [ ] Member IDs correlate to PatientSim MRNs via SSN

---

## Related Scenarios

- [Population to Patient](population-to-patient.md) - Clinical data
- [Population to Trial](population-to-trial.md) - Trial enrollment
