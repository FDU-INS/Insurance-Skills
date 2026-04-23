---
name: specialty-pharmacy
description: |
  Reference knowledge about specialty pharmacy operations including what makes
  a drug "specialty", limited distribution, hub model, REMS programs, and
  specialty pharmacy services.
  
  Trigger phrases: "specialty pharmacy", "specialty drug", "limited distribution",
  "hub model", "REMS", "specialty tier", "white bagging", "brown bagging",
  "specialty services", "copay assistance"
version: "1.0"
category: reference
related_skills:
  - pharmacy-benefit-concepts
  - pbm-operations
  - synthetic-pharmacy
---

# Specialty Pharmacy

## Overview

Specialty pharmacy is a distinct segment of pharmacy focused on high-cost, complex medications that require special handling, administration, or patient support. These drugs treat serious conditions like cancer, rheumatoid arthritis, multiple sclerosis, and rare diseases.

---

## Trigger Phrases

Use this skill when you see:
- "What is specialty pharmacy?"
- "Limited distribution drugs"
- "Hub and spoke model"
- "REMS program"
- "Specialty vs retail pharmacy"
- "White bagging vs brown bagging"
- "Copay assistance programs"

---

## What Makes a Drug "Specialty"

### Defining Characteristics

A drug is typically classified as specialty if it meets several of these criteria:

| Characteristic | Description |
|----------------|-------------|
| **High Cost** | >$1,000/month (some definitions: >$600) |
| **Complex Administration** | Injection, infusion, or special handling |
| **Special Storage** | Refrigeration, cold chain, light protection |
| **Limited Distribution** | Not available at all pharmacies |
| **Patient Support Needs** | Training, monitoring, adherence support |
| **Rare Disease** | Treats orphan or rare conditions |
| **High Touch** | Requires clinical monitoring |

### Examples by Therapy Area

| Therapy Area | Example Drugs | Why Specialty |
|--------------|---------------|---------------|
| **Oncology** | Keytruda, Ibrance | High cost, infusion |
| **Rheumatology** | Humira, Enbrel | Self-injection, monitoring |
| **Multiple Sclerosis** | Ocrevus, Tysabri | Infusion, REMS |
| **Hepatitis C** | Harvoni, Mavyret | High cost, monitoring |
| **HIV** | Biktarvy, Dovato | Adherence critical |
| **Rare Disease** | Spinraza, Kalydeco | Ultra-high cost, complex |

---

## Specialty Pharmacy Services

### Clinical Services

| Service | Description |
|---------|-------------|
| **Patient Education** | Training on self-injection, administration |
| **Adherence Support** | Refill reminders, counseling calls |
| **Side Effect Management** | Proactive monitoring and intervention |
| **Care Coordination** | Communication with prescriber |
| **Clinical Monitoring** | Lab tracking, therapy assessment |

### Financial Services

| Service | Description |
|---------|-------------|
| **Benefits Investigation** | Verify coverage before dispensing |
| **Prior Authorization** | Support PA submission |
| **Copay Assistance** | Enroll in manufacturer programs |
| **Foundation Assistance** | Connect to patient foundations |
| **Appeals** | Support for coverage denials |

### Operational Services

| Service | Description |
|---------|-------------|
| **Cold Chain Shipping** | Temperature-controlled delivery |
| **Flexible Delivery** | Multiple ship locations |
| **Refill Coordination** | Timed to therapy schedule |
| **Inventory Management** | Limited distribution access |

---

## Limited Distribution

### Definition

Limited Distribution Drugs (LDDs) are medications that manufacturers restrict to a small network of specialty pharmacies. Not all pharmacies can dispense them.

### Why Manufacturers Limit Distribution

1. **Safety/REMS**: Required safety monitoring and certification
2. **Data Collection**: Track outcomes and safety
3. **Inventory Control**: Prevent waste of expensive products
4. **Patient Support**: Ensure appropriate services provided
5. **Channel Control**: Manage pricing and contracts

### Distribution Models

| Model | Description |
|-------|-------------|
| **Open** | Available at any pharmacy |
| **Preferred** | Better pricing at select pharmacies |
| **Limited** | Only available at designated pharmacies |
| **Exclusive** | Single pharmacy or small network |
| **Direct from Manufacturer** | Shipped by manufacturer |

---

## Hub Model

### What is a Hub?

A Hub is a centralized patient support center operated by or for a drug manufacturer. It coordinates services but typically doesn't dispense medication.

### Hub Services

```
┌─────────────────────────────────────────────────────────────┐
│                         HUB SERVICES                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐   │
│  │   Benefits   │    │    Prior     │    │    Copay     │   │
│  │Investigation │    │Authorization │    │  Assistance  │   │
│  └──────────────┘    └──────────────┘    └──────────────┘   │
│                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐   │
│  │   Patient    │    │    Nurse     │    │   Pharmacy   │   │
│  │   Onboarding │    │   Support    │    │  Referral    │   │
│  └──────────────┘    └──────────────┘    └──────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │ Specialty Pharmacy│
                    │    Dispenses      │
                    └──────────────────┘
```

### Hub vs Specialty Pharmacy

| Function | Hub | Specialty Pharmacy |
|----------|-----|-------------------|
| Dispenses medication | No | Yes |
| Benefits investigation | Yes | Sometimes |
| Prior authorization | Yes | Sometimes |
| Copay assistance | Yes | Sometimes |
| Clinical support | Some | Yes |
| Refills | Coordinates | Dispenses |

---

## REMS Programs

### Definition

Risk Evaluation and Mitigation Strategies (REMS) are FDA-required safety programs for medications with serious safety concerns.

### REMS Elements

| Element | Description |
|---------|-------------|
| **Medication Guide** | Patient information document |
| **Communication Plan** | Healthcare provider information |
| **ETASU** | Elements to Assure Safe Use |
| **Implementation System** | Systems to track compliance |

### ETASU Requirements (Strictest REMS)

| Requirement | Example |
|-------------|---------|
| **Prescriber Certification** | Complete training, register |
| **Pharmacy Certification** | Register, ensure processes |
| **Patient Enrollment** | Sign agreement, education |
| **Dispense Conditions** | Verify requirements before each fill |

### Example: Clozapine REMS

```
Requirements:
✓ Prescriber enrolled in REMS
✓ Pharmacy enrolled in REMS
✓ Patient enrolled in REMS
✓ ANC lab result before each dispense
✓ Maximum 30-day supply
✓ Registry tracking
```

### Example: iPLEDGE (Isotretinoin)

```
Requirements:
✓ Prescriber registered
✓ Pharmacy registered
✓ Patient registered
✓ Monthly pregnancy tests (females)
✓ Two forms of contraception
✓ 7-day prescription window
```

---

## Buy and Bill vs Specialty Pharmacy

### Buy and Bill

```
Provider purchases drug → Stores → Administers → Bills medical
```

- Provider takes inventory risk
- Billed under medical benefit
- Common for infusion drugs

### Specialty Pharmacy Dispensing

```
Specialty pharmacy ships → Provider administers → Pharmacy bills Rx
```

#### White Bagging

```
Specialty pharmacy ships TO provider site
Provider administers drug
Billed under pharmacy benefit
```

#### Brown Bagging

```
Specialty pharmacy ships TO patient
Patient brings to provider
Provider administers
```

### Comparison

| Model | Inventory Risk | Benefit | Challenge |
|-------|----------------|---------|-----------|
| Buy & Bill | Provider | Medical | Drug cost, storage |
| White Bag | Pharmacy | Rx | Coordination, waste |
| Brown Bag | Pharmacy | Rx | Patient handling |

---

## Examples

### Example 1: What is Specialty Pharmacy

**Prompt**: "What is specialty pharmacy and how is it different from retail?"

**Response**:

Specialty pharmacy is a distinct pharmacy segment focused on high-cost, complex medications that require special handling and patient support.

**Key Differences from Retail Pharmacy**:

| Factor | Retail Pharmacy | Specialty Pharmacy |
|--------|-----------------|-------------------|
| **Drug Cost** | Most <$500/month | Most >$1,000/month |
| **Complexity** | Oral medications | Injectables, infusions |
| **Storage** | Room temperature | Cold chain common |
| **Patient Support** | Minimal | Extensive (nurses, training) |
| **Refill Process** | Patient-initiated | Proactive outreach |
| **Copays** | Manageable | May need assistance |
| **Prior Auth** | Sometimes | Almost always |

**What Specialty Pharmacies Provide**:
1. **Clinical Support**: Nurses who help with injections, side effects
2. **Financial Support**: Navigate copay cards, foundations
3. **Coordination**: Work with your doctor on lab monitoring
4. **Delivery**: Ship temperature-controlled to your home
5. **Adherence**: Proactive refill calls, education

**Common Specialty Conditions**:
- Cancer (oncology)
- Rheumatoid arthritis, psoriasis (autoimmune)
- Multiple sclerosis (neurology)
- Hepatitis C, HIV (infectious disease)
- Rare/orphan diseases

**Why It Matters**:
You can't fill most specialty drugs at CVS or Walgreens. Your insurance will direct you to a designated specialty pharmacy that has the expertise and access to dispense these complex medications.

---

### Example 2: Hub and Spoke Model

**Prompt**: "Explain the specialty pharmacy hub model"

**Response**:

The Hub model is a manufacturer-operated patient support center that coordinates care for specialty medications.

**How It Works**:

```
PATIENT/PRESCRIBER
        │
        ▼
   ┌─────────┐
   │   HUB   │  ← Manufacturer-operated
   └─────────┘
        │
        ├── Benefits Investigation (Is it covered?)
        ├── Prior Authorization (Get approval)
        ├── Copay Assistance (Find financial help)
        ├── Patient Education (Initial onboarding)
        │
        ▼
   ┌───────────────────┐
   │ SPECIALTY PHARMACY │  ← Actually dispenses
   └───────────────────┘
        │
        ▼
   ┌─────────────┐
   │   PATIENT   │
   └─────────────┘
```

**Hub Services**:
1. **Benefits Investigation**: Check coverage before therapy starts
2. **Prior Authorization**: Help submit PA paperwork
3. **Copay Assistance**: Enroll in manufacturer copay card
4. **Foundation Referral**: Connect to patient assistance foundations
5. **Nurse Support**: Initial training, ongoing check-ins

**What Hub Does NOT Do**:
- Does not dispense medication (that's the specialty pharmacy)
- Does not replace your doctor
- Does not make clinical decisions

**Why Manufacturers Use Hubs**:
- Ensure patients can afford and access therapy
- Reduce abandonment (patients who never start)
- Collect outcomes data
- Provide consistent patient experience

**How You Interact**:
When your doctor prescribes a specialty drug, the hub may call you to:
- Verify your insurance information
- Explain your coverage and costs
- Enroll you in copay assistance
- Schedule delivery with the specialty pharmacy

---

## Related Skills

- [Pharmacy Benefit Concepts](pharmacy-benefit-concepts.md) - Tier structures, specialty tier
- [PBM Operations](pbm-operations.md) - Claims processing
- [Synthetic Pharmacy](../synthetic/synthetic-pharmacy.md) - Generate specialty pharmacies
- [Pharmacy for RX](../integration/pharmacy-for-rx.md) - RxMemberSim integration

---

*Specialty Pharmacy is a reference skill in the NetworkSim product.*
