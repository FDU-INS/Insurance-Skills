---
name: healthsim-membersim
description: "MemberSim generates realistic synthetic claims and payer data for testing claims processing systems, payment integrity, and benefits administration."
---

# MemberSim - Claims and Payer Data Generation

## For Claude

Use this skill when the user requests healthcare claims, payer data, or benefits administration cohorts. This is the primary skill for generating realistic synthetic claims and member data.

**When to apply this skill:**

- User mentions claims, billing, or reimbursement
- User requests 837P (professional) or 837I (facility) claims
- User specifies payer, insurance, or benefits cohorts
- User asks for X12 formatted output (834, 835, 837, 270/271)
- User needs member enrollment, eligibility, or prior authorization data

**Key capabilities:**

- Generate members with coverage and benefit plans
- Create professional and facility claims with proper coding
- Model claim adjudication with CARC codes and payment calculations
- Track accumulators (deductible, OOP, coinsurance)
- Handle prior authorization workflows
- Transform output to X12 formats (837, 835, 834, 270/271)

For specific claims cohorts, load the appropriate cohort skill from the table below.

## Safety Guardrails

- **All data is synthetic.** MemberSim generates fictional, simulated test data. No real patient or member data is used.
- **No clinical advice.** Never recommend treatments, prescriptions, or clinical decisions based on generated data. This is test data, not real medical records.
- **Use valid medical code systems.** Always reference recognized standards: ICD-10 for diagnoses, CPT/HCPCS for procedures, NPI for providers, NDC/RxNorm for drugs, LOINC for labs, SNOMED CT for clinical terms.
- **Do NOT generate** real SSNs, real member IDs from production systems, or data that could be confused with actual PHI.

## Overview

MemberSim generates synthetic claims and payer data for testing claims processing, payment integrity, and benefits administration:

## Quick Start

### Simple Professional Claim

**Request:** "Generate a professional claim for an office visit"

```json
{
  "claim": {
    "claim_id": "CLM20250115000001",
    "claim_type": "PROFESSIONAL",
    "member_id": "MEM001234",
    "provider_npi": "1234567890",
    "service_date": "2025-01-15",
    "place_of_service": "11",
    "principal_diagnosis": "I10",
    "claim_lines": [
      {
        "line_number": 1,
        "procedure_code": "99214",
        "charge_amount": 175.00,
        "units": 1
      }
    ]
  },
  "adjudication": {
    "status": "paid",
    "allowed_amount": 125.00,
    "paid_amount": 100.00,
    "copay": 25.00
  }
}
```

### Facility Claim with DRG

**Request:** "Generate an inpatient claim for heart failure admission"

Claude loads [facility-claims.md](facility-claims.md) and produces a complete 837I-style claim:

```json
{
  "claim": {
    "claim_type": "INSTITUTIONAL",
    "principal_diagnosis": "I50.9",
    "drg": { "ms_drg": "291", "description": "Heart failure & shock w/o CC/MCC" },
    "admit_date": "2025-01-10",
    "discharge_date": "2025-01-13",
    "claim_lines": [
      { "revenue_code": "0120", "description": "Room and board - semi-private", "per_diem": 1800.00, "units": 3 },
      { "revenue_code": "0250", "description": "Pharmacy", "charge_amount": 950.00 },
      { "revenue_code": "0300", "description": "Laboratory", "charge_amount": 1200.00 }
    ]
  }
}
```

## Cohort Skills

Load the appropriate cohort based on user request:

| Cohort | Trigger Phrases | File |
|----------|-----------------|------|
| **Plan & Benefits** | plan, benefit plan, HMO, PPO, HDHP, copay, deductible structure | [plan-benefits.md](plan-benefits.md) |
| **Enrollment & Eligibility** | enrollment, eligibility, 834, 270, 271, coverage | [enrollment-eligibility.md](enrollment-eligibility.md) |
| **Professional Claims** | office visit, 837P, physician claim, E&M | [professional-claims.md](professional-claims.md) |
| **Facility Claims** | hospital, inpatient, 837I, DRG, UB-04 | [facility-claims.md](facility-claims.md) |
| **Prior Authorization** | prior auth, pre-cert, authorization, PA | [prior-authorization.md](prior-authorization.md) |
| **Accumulator Tracking** | deductible, OOP, accumulator, cost sharing | [accumulator-tracking.md](accumulator-tracking.md) |
| **Value-Based Care** | quality measures, VBC, HEDIS, risk adjustment, HCC, care gaps | [value-based-care.md](value-based-care.md) |
| **Behavioral Health** | mental health, psychiatry, psychotherapy, substance abuse, SUD | [behavioral-health.md](behavioral-health.md) |

## Generation Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| claim_type | string | PROFESSIONAL | PROFESSIONAL, INSTITUTIONAL, DENTAL |
| claim_status | string | paid | paid, denied, pending, partial |
| network_status | string | in-network | in-network, out-of-network |
| member_age | int or range | 18-65 | Member age |
| plan_type | string | PPO | HMO, PPO, EPO, POS, HDHP |

## Output Entities

| Entity | Key Fields |
|--------|-----------|
| **Member** | member_id, subscriber_id, group_id, plan_code, coverage_start/end, PCP (HMO) |
| **Claim** | claim_id, claim_type, member_id, provider_npi, service dates, diagnosis codes, claim_lines[] |
| **ClaimLine** | procedure_code (CPT/HCPCS), modifiers, units, charge_amount, revenue_code (institutional) |
| **Adjudication** | status (paid/denied/pending), allowed_amount, paid_amount, deductible, copay, coinsurance, adjustment_reason_codes |
| **Plan** | plan_type (HMO/PPO/etc.), deductibles, OOP maximums, copays, coinsurance rates, network requirements |
| **Accumulator** | deductible_accumulated vs remaining, OOP/MOOP accumulated vs remaining, family vs individual tracking |

See [../../references/data-models.md](../../references/data-models.md) for complete schemas.

## Adjudication Logic

### Payment Calculation
```
1. Verify eligibility (coverage active on service date)
2. Check network status (in-network vs OON)
3. Determine allowed amount (fee schedule or % of charges)
4. Apply cost sharing:
   a. Deductible (if not met)
   b. Copay (fixed amount)
   c. Coinsurance (% of allowed after deductible)
5. Calculate paid amount = allowed - member responsibility
6. Update accumulators (deductible accumulated/remaining, OOP/MOOP accumulated/remaining)
```

### Common Denial Reasons
| Code | Description | Cohort |
|------|-------------|----------|
| CO-4 | Procedure code inconsistent with modifier | Invalid modifier |
| CO-45 | Charge exceeds fee schedule | UCR violation |
| CO-50 | Non-covered services | Benefit exclusion |
| CO-96 | Non-covered charge(s) | Out of network, no OON benefit |
| CO-97 | Benefit included in another service | Bundling |
| PR-1 | Deductible amount | Member responsibility |
| PR-2 | Coinsurance amount | Member responsibility |
| PR-3 | Copay amount | Member responsibility |

## Output Formats

| Format | Request | Use Case |
|--------|---------|----------|
| JSON | default | API testing |
| X12 834 | "as 834", "X12 enrollment" | Enrollment file |
| X12 270 | "as 270", "eligibility inquiry" | Eligibility request |
| X12 271 | "as 271", "eligibility response" | Eligibility response |
| X12 837P | "as 837P", "X12 professional" | Claims submission |
| X12 837I | "as 837I", "X12 institutional" | Facility claims |
| X12 835 | "as 835", "remittance" | Payment posting |
| CSV | "as CSV" | Analytics |
| SQL | "as SQL" | Database loading |

See [../../formats/](../../formats/) for transformation skills.

## Examples

### Example 1: Paid Office Visit

**Request:** "Generate a paid claim for a 99214 office visit for hypertension"

```json
{
  "member": {
    "member_id": "MEM001234",
    "name": { "given_name": "Sarah", "family_name": "Johnson" },
    "birth_date": "1978-06-15",
    "gender": "F",
    "plan_code": "PPO-GOLD",
    "coverage_start": "2024-01-01"
  },
  "claim": {
    "claim_id": "CLM20250115000001",
    "claim_type": "PROFESSIONAL",
    "member_id": "MEM001234",
    "provider_npi": "1234567890",
    "service_date": "2025-01-15",
    "place_of_service": "11",
    "principal_diagnosis": "I10",
    "claim_lines": [
      {
        "line_number": 1,
        "procedure_code": "99214",
        "charge_amount": 175.00,
        "units": 1,
        "diagnosis_pointers": [1]
      }
    ]
  },
  "adjudication": {
    "status": "paid",
    "allowed_amount": 125.00,
    "deductible": 0.00,
    "copay": 25.00,
    "coinsurance": 0.00,
    "paid_amount": 100.00,
    "patient_responsibility": 25.00
  }
}
```

### Example 2: Denied Claim (Prior Auth Required)

**Request:** "Generate a denied claim for MRI without prior authorization"

```json
{
  "claim": {
    "claim_id": "CLM20250115000002",
    "claim_type": "PROFESSIONAL",
    "service_date": "2025-01-15",
    "place_of_service": "22",
    "principal_diagnosis": "M54.5",
    "claim_lines": [
      {
        "line_number": 1,
        "procedure_code": "72148",
        "charge_amount": 1500.00,
        "units": 1
      }
    ]
  },
  "adjudication": {
    "status": "denied",
    "denial_reason": "CO-15",
    "denial_message": "Prior authorization required",
    "allowed_amount": 0.00,
    "paid_amount": 0.00
  }
}
```

See [claim-examples.md](claim-examples.md) for additional examples: partial payment with deductible application, oncology infusion claims, OON emergency, and telehealth visits.

## Related Skills

### MemberSim Cohorts
- [plan-benefits.md](plan-benefits.md) - Plan configuration and benefit structure
- [enrollment-eligibility.md](enrollment-eligibility.md) - Enrollment and eligibility
- [professional-claims.md](professional-claims.md) - Professional claim details
- [facility-claims.md](facility-claims.md) - Institutional claim details
- [prior-authorization.md](prior-authorization.md) - PA workflows (includes oncology PAs)
- [accumulator-tracking.md](accumulator-tracking.md) - Cost sharing tracking
- [value-based-care.md](value-based-care.md) - VBC, HEDIS, risk adjustment

### Cross-Product: PatientSim (Clinical)

MemberSim claims correspond to PatientSim clinical encounters:

| MemberSim Skill | PatientSim Cohorts | Integration |
|-----------------|---------------------|-------------|
| [professional-claims.md](professional-claims.md) | Office visits, consults | Match E&M codes to encounter complexity |
| [facility-claims.md](facility-claims.md) | Inpatient, ED, surgery | Match DRG to admission diagnoses |
| [prior-authorization.md](prior-authorization.md) | Elective procedures | PA approved → procedure scheduled |
| [behavioral-health.md](behavioral-health.md) | Psychiatric care | Match visit types and diagnoses |

**PatientSim Cohort Links:**
- [../patientsim/heart-failure.md](../patientsim/heart-failure.md) - HF admission claims
- [../patientsim/diabetes-management.md](../patientsim/diabetes-management.md) - Diabetes office visit claims
- [../patientsim/elective-joint.md](../patientsim/elective-joint.md) - Surgical episode claims
- [../patientsim/oncology/](../patientsim/oncology/) - Oncology infusion claims
- [../patientsim/behavioral-health.md](../patientsim/behavioral-health.md) - Behavioral health claims

> **Integration Pattern:** Generate clinical encounter in PatientSim first, then use MemberSim to create corresponding claims with matching service dates, diagnosis codes, and procedures.

### Cross-Product: RxMemberSim (Pharmacy)

Medical and pharmacy benefits are often coordinated:

| MemberSim Skill | RxMemberSim Skill | Integration |
|-----------------|-------------------|-------------|
| [plan-benefits.md](plan-benefits.md) | [formulary-management.md](../rxmembersim/formulary-management.md) | Coordinated benefit design |
| [accumulator-tracking.md](accumulator-tracking.md) | [rx-accumulator.md](../rxmembersim/rx-accumulator.md) | Combined deductible/OOP |
| [prior-authorization.md](prior-authorization.md) | [rx-prior-auth.md](../rxmembersim/rx-prior-auth.md) | Medical vs. pharmacy PA |
| [enrollment-eligibility.md](enrollment-eligibility.md) | [rx-enrollment.md](../rxmembersim/rx-enrollment.md) | Synchronized coverage |

> **Integration Pattern:** For integrated medical+Rx benefits, ensure accumulators are synchronized and coverage dates match. Some specialty drugs are covered under medical benefit (infused) vs. pharmacy benefit (oral).

### Cross-Product: PopulationSim (Demographics & SDOH)

PopulationSim provides **embedded real-world data** (CDC PLACES, SVI, ADI) for actuarially realistic member generation. When geography is specified, look up actual prevalence rates and demographics to ground synthetic member panels.

**Pattern:** (1) Look up county/tract data by FIPS code, (2) apply prevalence rates to member generation, (3) include data provenance in output.

| Source | File | Use in MemberSim |
|--------|------|------------------|
| CDC PLACES County | `populationsim/data/county/places_county_2024.csv` | Utilization rates, risk adjustment |
| SVI County | `populationsim/data/county/svi_county_2022.csv` | SDOH factors, plan selection |
| ADI Block Group | `populationsim/data/block_group/adi_blockgroup_2023.csv` | Deprivation-based adherence |

| PopulationSim Skill | MemberSim Application |
|---------------------|----------------------|
| [data-lookup.md](../populationsim/data-access/data-lookup.md) | Prevalence rates for risk adjustment |
| [county-profile.md](../populationsim/geographic/county-profile.md) | Service area demographics |
| [svi-analysis.md](../populationsim/sdoh/svi-analysis.md) | Social vulnerability → plan tier, adherence |
| [adi-analysis.md](../populationsim/sdoh/adi-analysis.md) | Area deprivation → utilization patterns |

> **Key Principle:** When geography is specified, always ground member generation in real PopulationSim data for actuarially realistic synthetic panels.

### Cross-Product: NetworkSim (Provider Networks)

NetworkSim provides network context for claims processing:

| MemberSim Need | NetworkSim Skill | Integration |
|----------------|------------------|-------------|
| Provider network status | [network-for-member.md](../networksim/integration/network-for-member.md) | In-network vs OON determination |
| Benefit cost sharing | [benefit-for-claim.md](../networksim/integration/benefit-for-claim.md) | Copay, coinsurance, deductible |
| Network configuration | [synthetic-network.md](../networksim/synthetic/synthetic-network.md) | HMO/PPO/tiered structure |

> **Integration Pattern:** Use NetworkSim to determine network status before adjudicating claims. Network type (HMO/PPO) affects whether out-of-network claims are covered and at what cost share.

### Cross-Product: TrialSim (Clinical Trials)

Members may participate in clinical trials with claims integration:

| MemberSim Context | TrialSim Integration | Claims Impact |
|-------------------|---------------------|---------------|
| Specialty drug coverage | Trial drug provided free | Reduced Rx claims during trial |
| Standard of care | SOC claims continue | Normal claim adjudication |
| Trial-related AEs | May generate medical claims | AE → ED/inpatient claims |

> **Integration Pattern:** When a member enrolls in a trial, standard of care claims continue through MemberSim while trial-specific treatments are tracked in TrialSim. Trial-related adverse events may generate claims.

### Output Formats
- [../../formats/x12-834.md](../../formats/x12-834.md) - X12 enrollment format
- [../../formats/x12-270-271.md](../../formats/x12-270-271.md) - X12 eligibility format
- [../../formats/x12-837.md](../../formats/x12-837.md) - X12 claim format
- [../../formats/x12-835.md](../../formats/x12-835.md) - Remittance format
- [../../formats/csv.md](../../formats/csv.md) - CSV export
- [../../formats/sql.md](../../formats/sql.md) - SQL export

### Reference Data
- [../../references/data-models.md](../../references/data-models.md) - Entity schemas
- [../../references/oncology/](../../references/oncology/) - Oncology codes, medications, regimens

---

## Generative Framework Integration

MemberSim integrates with the [Generative Framework](../generation/SKILL.md) for specification-driven generation at scale.

### Profile-Driven Generation

Use profile specifications to generate member populations:

```
"Use the commercial healthy profile to generate 500 members"
```

The Profile Executor will:
1. Sample demographics from profile distributions
2. Generate coverage attributes (plan type, benefits)
3. Create accumulator records
4. Link to NetworkSim providers for PCP assignment

### Journey-Driven Generation

Attach journey specifications to create claims over time:

```
"Add the new member onboarding journey to each member"
```

The Journey Executor will:
1. Generate enrollment events
2. Create initial utilization claims
3. Track accumulator progression
4. Apply branching for engagement patterns

### Cross-Domain Sync

When generating across products, MemberSim entities are automatically linked:

| MemberSim Entity | Links To |
|------------------|----------|
| Member | PatientSim Patient (via SSN) |
| Claim | PatientSim Encounter |
| Authorization | PatientSim Referral |
| Rx Claim | RxMemberSim Fill |

See: [../generation/executors/cross-domain-sync.md](../generation/executors/cross-domain-sync.md)
