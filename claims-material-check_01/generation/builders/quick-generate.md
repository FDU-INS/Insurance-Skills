---
name: quick-generate
description: Simple single-entity or small batch generation without full profile specification
triggers:
  - generate a patient
  - create a member
  - quick generate
  - make me a
  - give me a
  - simple patient
  - one patient
---

# Quick Generate Skill

Fast path for simple entity generation without building a full profile specification.

## Overview

Quick Generate provides immediate entity generation using sensible defaults. Use this when you need data quickly and don't require the precision of a full profile specification.

## When to Use

| Use Quick Generate | Use Profile Builder |
|-------------------|---------------------|
| 1-10 entities | 10+ entities |
| Ad-hoc testing | Repeatable cohorts |
| Exploring cohorts | Production data |
| Single-entity demos | Statistical distributions |

## Trigger Phrases

- "Generate a diabetic patient"
- "Create a Medicare member with CHF"
- "Give me a commercial family with pharmacy claims"
- "Quick generate 5 trial subjects"
- "Make me a patient with these conditions: E11.9, I10, E78.5"

## Default Behaviors

When details aren't specified, Quick Generate uses sensible defaults:

| Attribute | Default | Notes |
|-----------|---------|-------|
| Age | 45-65 | Varies by coverage type |
| Gender | Random M/F | 48/52 ratio |
| Geography | US National | Random state |
| Output | JSON summary | FHIR on request |

### Coverage-Specific Defaults

| Coverage Type | Age Range | Common Conditions |
|---------------|-----------|-------------------|
| Medicare | 65-85 | HTN, hyperlipidemia |
| Commercial | 25-55 | Varies |
| Medicaid | 18-45 | Varies |
| Pediatric | 0-17 | Well-child |

## Examples

### Example 1: Simple Patient

```
User: "Generate a diabetic patient"

Claude: "Here's a Type 2 diabetic patient:

**Patient: Maria Santos**
- MRN: MRN00000001
- DOB: 1968-05-22 (age 56)
- Gender: Female

**Conditions:**
- E11.9 - Type 2 diabetes mellitus without complications
- I10 - Essential hypertension  
- E78.5 - Hyperlipidemia

**Recent Labs:**
- HbA1c: 7.4% (2025-01-15)
- Glucose: 142 mg/dL
- eGFR: 78 mL/min

**Medications:**
- Metformin 1000mg BID
- Lisinopril 20mg QD
- Atorvastatin 20mg QD

Would you like me to add claims, save to DuckDB, or generate more patients?"
```

### Example 2: Medicare Member with Claims

```
User: "Create a Medicare member with CHF and recent hospitalization"

Claude: "Here's a Medicare member with heart failure:

**Member: Robert Chen**
- Member ID: MEM001234
- Medicare ID: 1EG4-TE5-MK72
- DOB: 1952-03-18 (age 72)
- Plan: Medicare Advantage HMO

**Conditions:**
- I50.9 - Heart failure, unspecified
- I10 - Essential hypertension
- E11.65 - T2DM with hyperglycemia
- N18.3 - CKD Stage 3

**Recent Hospitalization (2025-01-08 to 2025-01-12):**
- Admit DX: I50.9 (CHF exacerbation)
- LOS: 4 days
- Facility: Memorial Hospital (NPI: 1234567890)
- Discharge: Home with services

**Facility Claim:**
- Claim ID: FC20250108001
- Charges: $24,500
- Allowed: $18,200
- Patient responsibility: $1,820

Would you like the FHIR bundle, X12 837I, or both?"
```

### Example 3: Family with Pharmacy

```
User: "Give me a commercial family of 4 with pharmacy claims"

Claude: "Here's a commercial family:

**Subscriber: James Wilson**
- Member ID: MEM-SUB-001
- DOB: 1982-06-15 (age 42)
- Plan: Commercial PPO
- Employer: Acme Corp

**Dependents:**
1. **Sarah Wilson** (Spouse, age 40)
2. **Emma Wilson** (Child, age 14)
3. **Tyler Wilson** (Child, age 11)

**Active Prescriptions:**

James:
- Lisinopril 10mg (HTN) - $12/month
- Atorvastatin 20mg - $8/month

Sarah:
- Levothyroxine 75mcg - $10/month

Emma:
- Albuterol inhaler (asthma) - $35/fill

Tyler:
- No active medications

**30-Day Pharmacy Claims:** 4 fills, total patient pay: $65

Save to cohort or generate claims detail?"
```

### Example 4: Trial Subject

```
User: "Quick generate a Phase III oncology trial subject"

Claude: "Here's a trial subject:

**Subject: ONCO-2025-001-0042**
- Site: 005 (Memorial Cancer Center)
- Study: ONCO-2025-001 (Phase III Lung Cancer)
- Arm: Treatment (TRT)

**Demographics:**
- Age: 62
- Sex: Female
- Race: White
- ECOG Status: 1

**Disease Characteristics:**
- Primary: C34.90 (Lung cancer, unspecified)
- Stage: IIIB
- Histology: Non-small cell (adenocarcinoma)
- EGFR: Wild-type
- PD-L1: 50%

**Trial Timeline:**
- Screening: 2025-01-08
- Informed Consent: 2025-01-08
- Randomization: 2025-01-15
- Status: Active

Generate linked PatientSim EMR record?"
```

## Output Options

After generation, offer format options:

```
"Output options:
1. **JSON** - Raw data structure
2. **FHIR R4** - Patient + Conditions + Observations
3. **HL7v2** - ADT message
4. **X12 837** - Claims format
5. **Save** - Persist to DuckDB cohort
6. **More** - Generate additional similar entities"
```

## Upgrading to Profile Builder

When requests become complex, suggest Profile Builder:

```
User: "Generate 50 Medicare diabetics with specific comorbidity rates"

Claude: "For 50+ entities with specific distributions, I recommend using
the Profile Builder for better control. Would you like me to:

1. **Start Profile Builder** - Full specification with distributions
2. **Quick Generate** - 50 patients with standard defaults

Profile Builder gives you:
- Exact comorbidity prevalence (e.g., 75% HTN)
- Age/gender distributions
- Reproducible specifications
- Journey definitions"
```

## Integration with State Management

Quick-generated entities can be saved:

```
User: "Save this patient"

Claude: "Saving to cohort 'ad-hoc-patients'...

✓ Saved patient MRN00000001 (Maria Santos)
  - Cohort: ad-hoc-patients
  - Entities: 1 patient, 3 conditions, 2 observations
  
To load later: 'Load cohort ad-hoc-patients'"
```

## Related Skills

- **[Profile Builder](profile-builder.md)** - Full specification building
- **[State Management](../../common/state-management.md)** - Save/load cohorts
- **[PatientSim](../../patientsim/SKILL.md)** - Clinical cohorts
- **[MemberSim](../../membersim/SKILL.md)** - Claims cohorts

---

*Part of the HealthSim Generative Framework*
