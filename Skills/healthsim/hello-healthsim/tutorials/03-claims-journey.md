# Tutorial 3: Claims Journey

**Time:** 20 minutes  
**Level:** Intermediate  
**Products:** PatientSim, MemberSim

## What You'll Learn

- Generate encounters that create claims
- Understand the patient-to-member relationship
- See cross-product synchronization in action
- Work with both clinical and administrative data

## Step 1: Generate a Member (Not Just a Patient)

When you need claims, generate across products:

```
You: "Generate a Medicare member with diabetes"

Claude: "Created linked patient/member:

PATIENT (PatientSim)
• MRN: MRN00000004
• Name: Dorothy Williams
• DOB: 1955-08-22 (69 years old)
• Conditions: E11.65 (T2DM with hyperglycemia)

MEMBER (MemberSim)
• Member ID: MEM00000004
• Plan: Medicare Advantage HMO
• Effective: 2023-01-01
• PCP: Dr. Sarah Johnson (NPI: 1234567890)

Both records linked via SSN for cross-product correlation."
```

## Step 2: Generate an Encounter

```
You: "Generate an office visit for her diabetes"

Claude: "Created encounter with corresponding claim:

ENCOUNTER (PatientSim)
• Encounter ID: ENC-2024-00001
• Date: 2024-11-15
• Type: Office Visit
• Provider: Dr. Sarah Johnson
• Diagnoses: E11.65, I10
• CPT: 99214 (Est patient, moderate complexity)
• Labs ordered: HbA1c, CMP

CLAIM (MemberSim)
• Claim ID: CLM-2024-00001
• Service Date: 2024-11-15
• Claim Type: Professional (837P)
• Billed: $175.00
• Lines:
  - 99214: $150.00
  - 36415 (Venipuncture): $25.00
• Status: Paid
• Allowed: $142.00
• Member Responsibility: $28.40 (20% coinsurance)

Cross-product sync: Encounter → Claim created automatically."
```

## Step 3: Add Lab Results with Claims

```
You: "Add the lab results from that visit"

Claude: "Generated lab results with claim:

LAB OBSERVATIONS (PatientSim)
• HbA1c: 7.8% (resulted 2024-11-16)
• Glucose: 145 mg/dL
• Creatinine: 1.2 mg/dL
• eGFR: 58 mL/min

LAB CLAIM (MemberSim)
• Claim ID: CLM-2024-00002
• Service Date: 2024-11-15
• Place of Service: 81 (Lab)
• Lines:
  - 83036 (HbA1c): $42.00
  - 80053 (CMP): $85.00
• Status: Paid
• Allowed: $98.00"
```

## Step 4: View the Complete Journey

```
You: "Show me all claims for this member in November"

Claude: "Claims summary for Dorothy Williams (MEM00000004), November 2024:

┌────────────────┬────────────┬─────────────┬──────────┬──────────┐
│ Claim ID       │ Date       │ Type        │ Billed   │ Paid     │
├────────────────┼────────────┼─────────────┼──────────┼──────────┤
│ CLM-2024-00001 │ 2024-11-15 │ Office Visit│ $175.00  │ $142.00  │
│ CLM-2024-00002 │ 2024-11-15 │ Lab         │ $127.00  │ $98.00   │
├────────────────┼────────────┼─────────────┼──────────┼──────────┤
│ TOTAL          │            │             │ $302.00  │ $240.00  │
└────────────────┴────────────┴─────────────┴──────────┴──────────┘

Member paid: $48.00 (coinsurance)
Claims link to encounters: ENC-2024-00001"
```

## Step 5: Generate a Pharmacy Claim

```
You: "She filled a prescription for metformin at CVS"

Claude: "Generated pharmacy fill with claim:

PRESCRIPTION (PatientSim)
• Rx Number: RX-2024-00001
• Medication: Metformin 1000mg
• Quantity: 60
• Days Supply: 30
• Prescriber: Dr. Sarah Johnson

FILL (RxMemberSim)
• Fill ID: FILL-2024-00001
• Fill Date: 2024-11-15
• Pharmacy: CVS #4521 (NPI: 9876543210)
• NDC: 00093-7214-01

PHARMACY CLAIM (MemberSim)
• Claim ID: CLM-2024-00003
• Type: Pharmacy
• Ingredient Cost: $12.50
• Dispensing Fee: $2.00
• Plan Paid: $10.50
• Member Copay: $4.00"
```

## Cross-Product Sync Explained

```
                   ┌─────────────┐
                   │   Person    │
                   │  (SSN link) │
                   └──────┬──────┘
                          │
         ┌────────────────┼────────────────┐
         │                │                │
         ▼                ▼                ▼
   ┌──────────┐    ┌──────────┐    ┌──────────┐
   │ Patient  │    │  Member  │    │RxMember  │
   │(PatSim)  │    │(MemSim)  │    │(RxMemSim)│
   └────┬─────┘    └────┬─────┘    └────┬─────┘
        │               │               │
        ▼               ▼               ▼
   Encounters      Claims          Fills
   Conditions      Eligibility     DUR Alerts
   Observations    EOBs           Formulary
```

## Try It Yourself

1. "Generate a member with a recent ER visit and see the facility claim"
2. "Create an inpatient stay with daily charges"
3. "Generate a specialist referral with both visits and claims"

## What's Next?

In [Tutorial 4: Population Cohort](04-population-cohort.md), you'll learn to use the Profile Builder to generate groups of patients/members at scale.

---

**← Previous:** [Tutorial 2: Clinical Scenario](02-clinical-cohort.md)  
**→ Next:** [Tutorial 4: Population Cohort](04-population-cohort.md)
