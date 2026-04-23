---
name: pbm-operations
description: |
  Reference knowledge about Pharmacy Benefit Manager (PBM) operations including
  claims processing, formulary management, rebates, and relationships with 
  health plans and pharmacies.
  
  Trigger phrases: "PBM", "pharmacy benefit manager", "BIN", "PCN", "claims processing",
  "rebates", "formulary management", "mail order", "carve-out", "carve-in"
version: "1.0"
category: reference
related_skills:
  - pharmacy-benefit-concepts
  - specialty-pharmacy
  - pharmacy-for-rx
---

# PBM Operations

## Overview

A Pharmacy Benefit Manager (PBM) is an intermediary that administers prescription drug programs for health plans, employers, and government programs. PBMs negotiate with drug manufacturers and pharmacies, process claims, and manage formularies.

---

## Trigger Phrases

Use this skill when you see:
- "What is a PBM?"
- "How does the PBM process claims?"
- "What is BIN and PCN?"
- "How do pharmacy rebates work?"
- "Carve-out vs carve-in pharmacy"
- "PBM relationship with health plan"

---

## What is a PBM?

### Definition

A Pharmacy Benefit Manager (PBM) is a company that:
- Processes prescription drug claims
- Negotiates drug prices and rebates
- Manages formularies
- Operates mail order pharmacies
- Provides clinical programs

### Major PBMs

| PBM | Parent Company | Market Share |
|-----|----------------|--------------|
| CVS Caremark | CVS Health | ~30% |
| Express Scripts | Cigna | ~25% |
| OptumRx | UnitedHealth | ~20% |
| Humana Pharmacy | Humana | ~8% |
| Prime Therapeutics | BCBS Consortium | ~7% |
| MedImpact | Independent | ~5% |

---

## PBM Services

### Core Services

| Service | Description |
|---------|-------------|
| **Claims Processing** | Real-time adjudication of pharmacy claims |
| **Formulary Management** | Develop and maintain drug list |
| **Rebate Negotiation** | Negotiate manufacturer discounts |
| **Network Management** | Contract with pharmacy networks |
| **Mail Order** | Home delivery pharmacy operations |
| **Specialty Pharmacy** | High-touch specialty dispensing |

### Clinical Programs

| Program | Purpose |
|---------|---------|
| **Prior Authorization** | Review for medical necessity |
| **Step Therapy** | Enforce first-line medication use |
| **Quantity Limits** | Prevent overutilization |
| **Drug Utilization Review** | Flag safety concerns |
| **Medication Therapy Management** | Improve adherence |

---

## Claims Processing

### Claim Flow

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Pharmacy   │───►│     PBM      │───►│ Response to  │
│   Submits    │    │   Processes  │    │   Pharmacy   │
│    Claim     │    │    Claim     │    │              │
└──────────────┘    └──────────────┘    └──────────────┘
      │                    │                    │
      │                    ▼                    │
      │           ┌──────────────┐              │
      │           │   Checks:    │              │
      │           │ • Eligibility│              │
      │           │ • Formulary  │              │
      │           │ • UM rules   │              │
      │           │ • Pricing    │              │
      │           └──────────────┘              │
      │                                         │
      ▼                                         ▼
Member receives         Pharmacy collects copay
medication              and dispenses
```

### Claim Elements

| Field | Description | Example |
|-------|-------------|---------|
| **BIN** | Bank Identification Number | 004336 |
| **PCN** | Processor Control Number | ADV |
| **Group** | Employer/plan group ID | RX1234 |
| **Member ID** | Individual identifier | ABC123456 |
| **NDC** | National Drug Code | 00074-3799-01 |
| **Quantity** | Units dispensed | 30 |
| **Days Supply** | Duration of therapy | 30 |

### BIN and PCN Routing

```
ID Card shows: BIN 004336, PCN ADV, Group RX1234

1. Pharmacy reads BIN → Routes to CVS Caremark
2. CVS Caremark reads PCN → Routes to correct plan
3. Group ID → Identifies specific benefit design
4. Member ID → Confirms eligibility
```

### Adjudication Response

| Response | Meaning | Action |
|----------|---------|--------|
| **Paid** | Claim approved | Dispense, collect copay |
| **Rejected** | Claim denied | See rejection code |
| **PA Required** | Needs authorization | Submit PA request |
| **Refill Too Soon** | Too early | Wait until allowed date |
| **NDC Not Covered** | Not on formulary | Try alternative |

---

## Formulary Management

### P&T Committee

The Pharmacy & Therapeutics (P&T) Committee:
- Reviews clinical evidence
- Makes formulary decisions
- Sets tier placement
- Establishes clinical criteria

### Formulary Development Process

```
1. Clinical Review
   └── Evaluate efficacy, safety, place in therapy
   
2. Economic Analysis
   └── Compare costs, consider rebates
   
3. Therapeutic Class Review
   └── Compare drugs within class
   
4. Tier Placement Decision
   └── Assign to appropriate tier
   
5. Utilization Management
   └── Set PA, step therapy, QL criteria
   
6. Ongoing Monitoring
   └── Track utilization, outcomes, costs
```

---

## Rebates

### How Rebates Work

```
Manufacturer ──► PBM ──► Health Plan
              Rebate    Share

Drug WAC: $1,000
Rebate: $300 (30%)
Net Cost: $700
```

### Rebate Types

| Type | Description |
|------|-------------|
| **Base Rebate** | Standard discount for formulary inclusion |
| **Market Share** | Additional rebate for preferred position |
| **Admin Fees** | PBM fee for managing rebate |
| **Price Protection** | Protection against price increases |

### PBM Business Models

| Model | Rebate Handling |
|-------|-----------------|
| **Traditional** | PBM keeps portion of rebate |
| **Pass-Through** | 100% of rebate goes to plan |
| **Transparent** | Full visibility into all pricing |

---

## Plan Relationships

### Carve-Out vs Carve-In

**Carve-Out**:
```
Health Plan ◄─────────────────────► Medical
     │
     └─────► PBM ◄─────────────────► Pharmacy
             (Separate contract)
```
- Pharmacy benefit separate from medical
- Plan contracts directly with PBM
- More flexibility in PBM selection
- Separate accumulators common

**Carve-In**:
```
Health Plan ◄───► Medical + Pharmacy
                  (Integrated)
```
- Pharmacy bundled with medical
- Single vendor for both
- Integrated accumulators
- Often used by integrated health systems

### PBM Contract Elements

| Element | Description |
|---------|-------------|
| **Admin Fee PMPM** | Per-member fee for services |
| **Rebate Guarantee** | Minimum rebate commitment |
| **MAC List** | Maximum allowable cost for generics |
| **AWP Discount** | Discount from Average Wholesale Price |
| **Network** | Which pharmacies included |
| **Clinical Programs** | Which UM programs included |

---

## Examples

### Example 1: How PBM Claims Work

**Prompt**: "How does a PBM process pharmacy claims?"

**Response**:

When you fill a prescription, here's what happens in real-time:

**Step 1: Claim Submission**
The pharmacy submits a claim electronically using information from your ID card:
- BIN (Bank Identification Number) → Routes to the PBM
- PCN (Processor Control Number) → Routes to your specific plan
- Group ID → Identifies your employer's benefit design
- Member ID → Confirms your eligibility

**Step 2: PBM Adjudication** (happens in seconds)
The PBM checks:
- ✓ Are you eligible today?
- ✓ Is this drug on formulary?
- ✓ Does it require prior authorization?
- ✓ Is it too soon to refill?
- ✓ Any safety alerts (drug interactions)?

**Step 3: Pricing Calculation**
```
Drug Cost: $150.00
Plan Pays: $120.00
Your Copay: $30.00
```

**Step 4: Response to Pharmacy**
- Approved: "Paid" with copay amount
- Denied: Rejection code with reason
- Pending: "PA Required"

**Step 5: Dispensing**
Pharmacy collects your copay and provides the medication.

Total time: 2-5 seconds from submission to response.

---

### Example 2: Rebates Explained

**Prompt**: "How do pharmacy rebates work?"

**Response**:

Pharmacy rebates are discounts drug manufacturers pay to PBMs and health plans in exchange for favorable formulary placement.

**The Flow**:
```
Manufacturer → PBM → Health Plan
   (pays)      (negotiates)  (receives share)
```

**Example**:
```
Brand Drug X
├── List Price (WAC): $1,000
├── Manufacturer Rebate: $300 (30%)
├── Net Cost to Plan: $700
│
└── Rebate Split:
    ├── To Health Plan: $250 (83%)
    └── To PBM (Admin Fee): $50 (17%)
```

**Why Manufacturers Pay Rebates**:
1. **Formulary Access**: Get on the drug list
2. **Preferred Status**: Lower tier = more volume
3. **Exclusivity**: Block competitor products
4. **Market Share**: Guaranteed prescription volume

**Controversy**:
- List prices rise to fund higher rebates
- Creates misaligned incentives
- Rebate savings don't always reach members
- Point-of-sale rebate reform proposed

**Transparency Trend**:
Some PBMs now offer "pass-through" contracts where 100% of rebates go to the health plan, with PBM earning only admin fees.

---

## Related Skills

- [Pharmacy Benefit Concepts](pharmacy-benefit-concepts.md) - Tier structures, formularies
- [Specialty Pharmacy](specialty-pharmacy.md) - Specialty distribution
- [Utilization Management](utilization-management.md) - PA, step therapy
- [Pharmacy for RX](../integration/pharmacy-for-rx.md) - RxMemberSim integration

---

*PBM Operations is a reference skill in the NetworkSim product.*
