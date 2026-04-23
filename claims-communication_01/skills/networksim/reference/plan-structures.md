---
name: plan-structures
description: |
  Reference knowledge about health plan benefit structures including deductibles,
  copays, coinsurance, out-of-pocket maximums, and accumulators. Explains how
  cost sharing works between members and plans.
  
  Trigger phrases: "plan structure", "deductible", "copay", "coinsurance",
  "out-of-pocket maximum", "OOP max", "cost sharing", "in-network vs out-of-network",
  "accumulator", "benefit design", "metal tier"
version: "1.0"
category: reference
related_skills:
  - network-types
  - synthetic-plan
  - benefit-for-claim
---

# Plan Structures

## Overview

Health plan benefit structures define how costs are shared between the health plan and the member. Understanding these components is essential for generating realistic benefit designs and claims.

This skill covers:
- Deductibles
- Copays and Coinsurance
- Out-of-Pocket Maximums
- In-Network vs Out-of-Network Benefits
- Accumulators
- Common Plan Designs

---

## Trigger Phrases

Use this skill when you see:
- "What is a deductible?"
- "Difference between copay and coinsurance"
- "How does out-of-pocket max work?"
- "In-network vs out-of-network"
- "Plan benefit structure"
- "How do accumulators work?"
- "Bronze vs Gold plan"

---

## Core Benefit Components

### Deductible

**Definition**: The amount a member must pay out-of-pocket before the health plan begins to pay for covered services.

**Key Concepts**:
- **Individual Deductible**: Amount one person must meet
- **Family Deductible**: Combined amount for all family members
- **Embedded vs Aggregate**: How family deductibles work

| Deductible Type | How It Works |
|-----------------|--------------|
| **Embedded** | Each individual has own deductible capped at individual amount; family deductible met when individuals' combined = family amount |
| **Aggregate** | No individual deductible; entire family deductible must be met before plan pays for anyone |

**Typical Ranges**:
| Plan Type | Individual | Family |
|-----------|------------|--------|
| HMO | $0 - $500 | $0 - $1,000 |
| PPO | $500 - $2,000 | $1,000 - $4,000 |
| HDHP | $1,600 - $5,000 | $3,200 - $10,000 |

**Services Often Exempt from Deductible**:
- Preventive care (ACA requirement)
- Primary care copay visits (some plans)
- Generic drugs (some plans)

---

### Copay (Copayment)

**Definition**: A fixed dollar amount the member pays for a covered service at the time of service.

**Common Copay Amounts**:
| Service | Typical Copay |
|---------|---------------|
| Primary Care Visit | $20 - $40 |
| Specialist Visit | $40 - $75 |
| Urgent Care | $50 - $100 |
| Emergency Room | $150 - $500 |
| Generic Drug | $5 - $15 |
| Brand Drug | $30 - $60 |
| Specialty Drug | $100 - $500 |

**Copay Characteristics**:
- Fixed, predictable amount
- Paid at time of service
- May or may not apply to deductible
- Common in HMO plans
- Usually only for in-network

---

### Coinsurance

**Definition**: A percentage of the allowed amount that the member pays for a covered service after the deductible is met.

**How It Works**:
```
Allowed Amount: $1,000
Deductible: Already met
Coinsurance: 20%

Plan Pays: $800 (80%)
Member Pays: $200 (20%)
```

**Common Coinsurance Rates**:
| Network Status | Member Pays | Plan Pays |
|----------------|-------------|-----------|
| In-Network | 10-20% | 80-90% |
| Out-of-Network | 30-50% | 50-70% |

**Coinsurance vs Copay**:
| Factor | Copay | Coinsurance |
|--------|-------|-------------|
| Amount | Fixed dollar | Percentage |
| Predictability | High | Lower |
| Varies by cost | No | Yes |
| Common in | HMO | PPO, HDHP |

---

### Out-of-Pocket Maximum (OOP Max)

**Definition**: The maximum amount a member will pay for covered services in a plan year. After reaching this limit, the plan pays 100%.

**What Counts Toward OOP Max**:
- Deductibles
- Copays
- Coinsurance

**What Typically Does NOT Count**:
- Premiums
- Out-of-network costs (separate OOP max)
- Non-covered services
- Balance billing

**2024 ACA Limits**:
| Coverage | Maximum OOP |
|----------|-------------|
| Individual | $9,450 |
| Family | $18,900 |

**Typical OOP Max Ranges**:
| Plan Type | Individual | Family |
|-----------|------------|--------|
| HMO | $3,000 - $6,000 | $6,000 - $12,000 |
| PPO In-Network | $5,000 - $8,000 | $10,000 - $16,000 |
| PPO Out-of-Network | $10,000 - $20,000 | $20,000 - $40,000 |
| HDHP | $4,000 - $8,050 | $8,000 - $16,100 |

---

## In-Network vs Out-of-Network

### Definitions

**In-Network Provider**: A provider who has a contract with the health plan to provide services at negotiated rates.

**Out-of-Network Provider**: A provider without a plan contract who can charge their standard rates.

### Cost Differences

| Component | In-Network | Out-of-Network |
|-----------|------------|----------------|
| Deductible | Lower | Higher |
| Coinsurance | 10-20% | 30-50% |
| OOP Maximum | Lower | Higher or unlimited |
| Balance Billing | No | Yes |
| Coverage | Full | Reduced or none |

### Balance Billing

When using out-of-network providers:

```
Provider Charge: $1,500
Plan Allowed Amount: $1,000
Plan Pays (70%): $700
Member Coinsurance (30%): $300
Balance Bill: $500 (provider charge - allowed amount)

Total Member Cost: $800 ($300 + $500)
```

**Note**: Some states have balance billing protections for emergency and surprise bills.

### UCR (Usual, Customary, and Reasonable)

Plans use UCR to determine allowed amounts for out-of-network claims:
- Based on what providers in the area typically charge
- Member responsible for amounts above UCR
- Different methodologies (percentile-based, Medicare-based)

---

## Accumulators

### Definition

Accumulators track member spending toward deductibles and out-of-pocket maximums throughout the plan year.

### Types of Accumulators

| Accumulator | Tracks Progress Toward |
|-------------|------------------------|
| Deductible Accumulator | Annual deductible |
| OOP Maximum Accumulator | Out-of-pocket limit |
| Visit Accumulator | Visit limits (e.g., 20 PT visits) |

### Family Accumulator Strategies

**Embedded Deductible**:
```
Family Deductible: $3,000
Individual Embedded Max: $1,500

- Member A spends $1,500 → A's deductible met
- Member B spends $500 → B still has $1,000 to go
- Family total: $2,000 → Family not yet met
```

**Aggregate Deductible**:
```
Family Deductible: $3,000
No individual deductible

- Member A spends $2,500
- Member B spends $500
- Family total: $3,000 → Deductible met for ALL members
```

### Pharmacy vs Medical Accumulators

Some plans have separate accumulators:
| Accumulator Type | Applies To |
|------------------|------------|
| Medical Deductible | Doctor visits, hospital, labs |
| Pharmacy Deductible | Prescription drugs |
| Combined | Both medical and pharmacy |

---

## Common Plan Designs

### ACA Metal Tiers

The Affordable Care Act defines plan tiers by actuarial value (average % of costs plan pays):

| Tier | Actuarial Value | Member Pays | Best For |
|------|-----------------|-------------|----------|
| **Bronze** | 60% | 40% | Healthy, low utilization |
| **Silver** | 70% | 30% | Moderate utilization |
| **Gold** | 80% | 20% | Higher utilization |
| **Platinum** | 90% | 10% | High utilization, chronic conditions |

### Typical Bronze Plan

```
Premium: Low
Deductible: $6,000 individual / $12,000 family
Coinsurance: 40% after deductible
OOP Max: $8,700 individual / $17,400 family
PCP Copay: $40 (before deductible)
Specialist Copay: After deductible
Generic Rx: $20 (before deductible)
```

### Typical Silver Plan

```
Premium: Moderate
Deductible: $3,000 individual / $6,000 family
Coinsurance: 30% after deductible
OOP Max: $8,700 individual / $17,400 family
PCP Copay: $35 (before deductible)
Specialist Copay: $70 (before deductible)
Generic Rx: $15 (before deductible)
```

### Typical Gold Plan

```
Premium: Higher
Deductible: $1,000 individual / $2,000 family
Coinsurance: 20% after deductible
OOP Max: $6,000 individual / $12,000 family
PCP Copay: $25 (before deductible)
Specialist Copay: $50 (before deductible)
Generic Rx: $10 (before deductible)
```

### Typical Employer PPO

```
Premium: Employer-subsidized
Deductible: $500 in-network / $1,000 out-of-network
Coinsurance: 20% in-network / 40% out-of-network
OOP Max: $4,000 in-network / $8,000 out-of-network
PCP Copay: $25
Specialist Copay: $50
Emergency: $250 copay
```

---

## Examples

### Example 1: Understanding Cost Sharing

**Prompt**: "What's the difference between a copay and coinsurance?"

**Response**:

Copays and coinsurance are both forms of cost sharing, but they work differently:

**Copay (Copayment)**:
- Fixed dollar amount you pay at time of service
- Amount stays the same regardless of total cost
- Example: $30 copay for a specialist visit
- You pay $30 whether the visit costs $150 or $300

**Coinsurance**:
- Percentage of the allowed cost you pay
- Amount varies based on total service cost
- Usually applies after deductible is met
- Example: 20% coinsurance for hospital services

**Cost Comparison Example**:

For a $500 specialist visit:
| Cost Sharing | You Pay | Plan Pays |
|--------------|---------|-----------|
| $50 Copay | $50 | $450 |
| 20% Coinsurance | $100 | $400 |

**When Each Is Used**:
- **Copays**: Common for predictable services (office visits, Rx)
- **Coinsurance**: Common for variable-cost services (hospital, surgery)

Many plans use both: copays for routine care, coinsurance for major services.

---

### Example 2: How Deductibles and OOP Max Work Together

**Prompt**: "Explain how deductibles and out-of-pocket maximums work together"

**Response**:

Deductibles and out-of-pocket maximums (OOP max) work together to limit your total healthcare costs:

**The Relationship**:
```
$0 ──────────────────► Deductible ──────────────► OOP Max ───►
   You pay 100%          You pay copay/         Plan pays 
   (except preventive)   coinsurance            100%
```

**Example: $1,500 deductible, 20% coinsurance, $5,000 OOP max**

| Total Costs | Your Spending | Running Total | Status |
|-------------|---------------|---------------|--------|
| First $1,500 | $1,500 | $1,500 | Deductible met |
| Next $17,500 | $3,500 (20%) | $5,000 | OOP max met |
| Beyond $19,000 | $0 | $5,000 | Plan pays 100% |

**What Counts Toward OOP Max**:
✅ Deductible payments
✅ Copays
✅ Coinsurance

**What Does NOT Count**:
❌ Monthly premiums
❌ Out-of-network costs (usually separate OOP max)
❌ Non-covered services

**Family Considerations**:
- Individual deductible may be embedded in family deductible
- Once any individual hits individual OOP max, plan pays 100% for them
- Family OOP max protects against multiple family members with high costs

---

## Generation Guidance

When generating plan benefit structures:

| Plan Type | Typical Structure |
|-----------|-------------------|
| Low-cost HMO | Low deductible, copays, low OOP max |
| Standard PPO | Moderate deductible, coinsurance, separate OON benefits |
| HDHP | High deductible, coinsurance, HSA-compatible limits |
| Rich Employer | Low deductible, low copays, employer-funded HRA |

---

## Related Skills

- [Network Types](network-types.md) - Network configurations
- [Synthetic Plan](../synthetic/synthetic-plan.md) - Generate plan designs
- [Benefit for Claim](../integration/benefit-for-claim.md) - Apply benefits to claims
- [Pharmacy Benefit Concepts](pharmacy-benefit-concepts.md) - Rx cost sharing

---

*Plan Structures is a reference skill in the NetworkSim product.*
