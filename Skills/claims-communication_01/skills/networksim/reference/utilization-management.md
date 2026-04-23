---
name: utilization-management
description: |
  Reference knowledge about pharmacy utilization management programs including
  prior authorization, step therapy, quantity limits, and exception processes.
  
  Trigger phrases: "prior authorization", "PA", "step therapy", "quantity limits",
  "QL", "utilization management", "UM", "formulary exception", "fail first"
version: "1.0"
category: reference
related_skills:
  - pbm-operations
  - pharmacy-benefit-concepts
  - specialty-pharmacy
---

# Utilization Management

## Overview

Utilization Management (UM) programs ensure prescription drugs are used appropriately, safely, and cost-effectively. The three main UM programs are prior authorization, step therapy, and quantity limits.

---

## Trigger Phrases

Use this skill when you see:
- "What is prior authorization?"
- "How does step therapy work?"
- "Quantity limits"
- "Fail first requirement"
- "Formulary exception"
- "PA criteria"
- "Override process"

---

## Prior Authorization (PA)

### Definition

Prior Authorization is a requirement that the prescriber obtain approval from the health plan before a medication will be covered.

### Why PA is Required

| Reason | Example |
|--------|---------|
| **High Cost** | Specialty medications ($10,000+/month) |
| **Safety** | Drugs with serious side effects |
| **Appropriate Use** | Off-label use concerns |
| **Alternatives Available** | Lower-cost options exist |
| **Clinical Criteria** | Diagnosis verification needed |

### PA Process

```
1. Prescription Submitted
   └── Pharmacy claim rejected: "PA Required"
   
2. PA Request Initiated
   └── Prescriber submits PA form with clinical info
   
3. Clinical Review
   └── PBM pharmacist/MD reviews against criteria
   
4. Decision
   ├── Approved → Claim will process
   ├── Denied → Appeal option available
   └── More Info Needed → Prescriber contacted
   
5. Notification
   └── Prescriber and member notified of decision
```

### PA Timeline Requirements

| Request Type | Decision Timeline |
|--------------|-------------------|
| Standard | 72 hours |
| Urgent/Expedited | 24 hours |
| Appeal | 72 hours |
| External Review | Varies by state |

### Common PA Criteria

**For Specialty Drugs**:
- Confirmed diagnosis (ICD-10 codes)
- Lab values (if applicable)
- Failed first-line therapy
- Prescriber specialty requirements
- Treatment facility requirements

**Example: Humira (adalimumab)**:
```
Required for approval:
✓ Diagnosis of rheumatoid arthritis, psoriasis, or Crohn's
✓ Failed trial of methotrexate (for RA) 
✓ Labs within last 90 days
✓ No active infections
✓ Prescribed by rheumatology/GI/dermatology
```

---

## Step Therapy

### Definition

Step Therapy (also called "fail first") requires patients to try one or more preferred medications before a non-preferred medication is covered.

### How It Works

```
Step 1: Try generic/preferred drug first
        ↓
        Fails (side effects, ineffective, contraindicated)
        ↓
Step 2: Second-line option approved
        ↓
        Fails
        ↓
Step 3: Non-preferred option approved
```

### Common Step Therapy Examples

**Cholesterol (Statins)**:
```
Step 1: Generic simvastatin, atorvastatin
Step 2: Generic rosuvastatin
Step 3: Brand Livalo, Crestor (if brand needed)
```

**Depression (SSRIs)**:
```
Step 1: Generic fluoxetine, sertraline, escitalopram
Step 2: Generic duloxetine, venlafaxine
Step 3: Brand medications
```

**Diabetes (GLP-1s)**:
```
Step 1: Metformin (if appropriate)
Step 2: Generic sulfonylurea or DPP-4
Step 3: GLP-1 agonist
```

### Step Therapy Exceptions

Exceptions may be granted when:
- Contraindication to step drug
- Previous trial and failure documented
- Clinical reason step drug is inappropriate
- Continuation of current therapy (grandfather)

---

## Quantity Limits (QL)

### Definition

Quantity Limits restrict the amount of medication that can be dispensed in a given time period.

### Types of Quantity Limits

| Type | Description | Example |
|------|-------------|---------|
| **Units per Fill** | Max tablets/doses per fill | 30 tablets per fill |
| **Units per Day** | Max daily dose | 2 tablets per day |
| **Fills per Period** | Max fills in timeframe | 12 fills per year |
| **Days Supply** | Max days per fill | 30 days (specialty) |

### Reasons for Quantity Limits

**Safety-Based QL**:
- Prevent overdose risk
- Limit abuse potential
- Control medications (opioids)
- High-risk drugs

**Cost-Based QL**:
- Prevent waste
- Limit high-cost drug usage
- Encourage appropriate dosing

### Examples

**Opioids** (Safety):
```
Limit: 90 MME (morphine milligram equivalents) per day
Example: Oxycodone 30mg max 3 tablets/day
Override: Pain specialist attestation
```

**Specialty Drugs** (Cost):
```
Limit: 30-day supply per fill
Reason: High cost, adherence monitoring
```

**Migraine Triptans** (Clinical):
```
Limit: 9 tablets per month
Reason: Medication overuse headache risk
Override: Neurologist attestation
```

---

## Exception Processes

### Formulary Exception Request

When a non-formulary or higher-tier drug is needed:

```
1. Prescriber documents clinical rationale
2. Shows why formulary alternatives won't work
3. Submits exception request
4. PBM reviews against exception criteria
5. If approved, drug covered at lower tier
```

### Quantity Limit Override

```
1. Prescriber documents medical necessity
2. Explains why higher quantity needed
3. Submits override request
4. PBM reviews
5. If approved, higher quantity covered
```

### Step Therapy Override

```
1. Document contraindication or prior failure
2. Provide clinical evidence
3. Submit override request
4. PBM reviews
5. If approved, step requirement waived
```

### Appeal Process

If initial request denied:

```
Level 1: Internal Appeal
├── Submit to PBM within 60 days
├── Additional clinical info may help
└── Decision within 72 hours

Level 2: External Review
├── Independent review organization
├── Required by state/federal law
└── Decision binding on plan

Level 3: State Insurance Commissioner
└── Complaint if process not followed
```

---

## Examples

### Example 1: Prior Authorization Process

**Prompt**: "What is prior authorization and when is it required?"

**Response**:

Prior Authorization (PA) is a requirement that your doctor get approval from the health plan before a medication is covered.

**When PA is Required**:
- **High-cost drugs**: Specialty medications costing $1,000+/month
- **Safety concerns**: Drugs with significant side effects
- **Alternative availability**: When cheaper options exist
- **Appropriate use**: To verify diagnosis and appropriateness

**The Process**:
1. **You fill prescription** → Pharmacy claim rejects with "PA Required"
2. **Doctor submits PA request** → Includes diagnosis, clinical info
3. **Plan reviews** → Usually within 24-72 hours
4. **Decision made**:
   - ✅ Approved: Medication covered, pharmacy can fill
   - ❌ Denied: Doctor can appeal with more information

**What Your Doctor Provides**:
- Diagnosis codes (ICD-10)
- Lab results (if applicable)
- Previous medications tried
- Clinical rationale

**Timeline**:
- Standard requests: 72 hours
- Urgent requests: 24 hours

**Tip**: Your doctor's office often handles PA. Ask them about status if it's taking too long.

---

### Example 2: Step Therapy Requirements

**Prompt**: "Explain step therapy requirements"

**Response**:

Step Therapy (also called "fail first") requires trying preferred medications before a more expensive option is covered.

**How It Works**:

```
Your doctor prescribes: Brand Drug X ($500/month)
Plan says: "Try Drug A first" (generic, $20/month)
                    ↓
         Drug A doesn't work
                    ↓
Plan says: "Try Drug B" (preferred brand, $100/month)
                    ↓
         Drug B doesn't work
                    ↓
      Brand Drug X now approved
```

**Why Plans Use Step Therapy**:
1. **Cost**: Generic/preferred drugs are significantly cheaper
2. **Clinical**: Many conditions respond well to first-line drugs
3. **Appropriate**: Ensures systematic treatment approach

**Getting an Exception**:
You can skip steps if:
- Medical reason you can't take the step drug (allergy, interaction)
- You already tried and failed the step drug
- You're currently stable on the requested drug (continuation)
- Clinical circumstances make step drug inappropriate

**What to Provide for Exception**:
- Documentation of previous trial
- Dates, doses, and reason for discontinuation
- Why preferred alternatives won't work
- Clinical rationale from specialist

**Common Step Therapy Categories**:
- Cholesterol medications (try generic statin first)
- Antidepressants (try generic SSRI first)
- Pain medications (try NSAIDs before specialty)
- Diabetes medications (try metformin first)

---

## Related Skills

- [PBM Operations](pbm-operations.md) - Claims processing
- [Pharmacy Benefit Concepts](pharmacy-benefit-concepts.md) - Tier structures
- [Specialty Pharmacy](specialty-pharmacy.md) - High-touch specialty
- [Formulary for RX](../integration/formulary-for-rx.md) - RxMemberSim

---

*Utilization Management is a reference skill in the NetworkSim product.*
