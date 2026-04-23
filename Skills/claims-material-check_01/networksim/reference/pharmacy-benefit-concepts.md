---
name: pharmacy-benefit-concepts
description: |
  Reference knowledge about pharmacy benefit structures including tier structures,
  formulary types, pharmacy networks, and cost sharing. Explains concepts without
  drug-specific coverage (that's RxMemberSim's domain).
  
  Trigger phrases: "pharmacy benefit", "tier structure", "formulary", 
  "preferred pharmacy", "specialty tier", "copay vs coinsurance", "generic",
  "brand", "pharmacy network", "mail order", "90-day supply"
version: "1.0"
category: reference
related_skills:
  - pbm-operations
  - specialty-pharmacy
  - pharmacy-for-rx
  - synthetic-pharmacy-benefit
boundary_note: |
  This skill explains pharmacy benefit CONCEPTS. RxMemberSim owns drug-specific
  coverage decisions, formulary placement, and PA criteria.
---

# Pharmacy Benefit Concepts

## Overview

Pharmacy benefits define how prescription drug costs are shared between health plans and members. This skill covers the structural concepts of pharmacy benefits, not specific drug coverage (which is RxMemberSim's domain).

Topics covered:
- Tier Structures
- Formulary Types
- Pharmacy Networks
- Cost Sharing Models
- Accumulator Integration
- Specialty Pharmacy Requirements

---

## Trigger Phrases

Use this skill when you see:
- "Explain pharmacy tiers"
- "What is a formulary?"
- "Preferred vs non-preferred pharmacy"
- "How do specialty tiers work?"
- "Mail order pharmacy benefits"
- "Generic vs brand copay"
- "Pharmacy benefit design"

---

## Tier Structures

### Overview

Pharmacy benefits use tiers to encourage use of lower-cost medications. Each tier has different cost sharing.

### Common Tier Structures

**3-Tier Structure** (Traditional):
| Tier | Contents | Typical Copay |
|------|----------|---------------|
| Tier 1 | Generic drugs | $10 - $15 |
| Tier 2 | Preferred brand | $30 - $50 |
| Tier 3 | Non-preferred brand | $60 - $100 |

**4-Tier Structure** (Common):
| Tier | Contents | Typical Copay |
|------|----------|---------------|
| Tier 1 | Generic | $10 - $15 |
| Tier 2 | Preferred brand | $30 - $50 |
| Tier 3 | Non-preferred brand | $60 - $100 |
| Tier 4 | Specialty | 20-30% coinsurance |

**5-Tier Structure** (Comprehensive):
| Tier | Contents | Typical Cost Share |
|------|----------|-------------------|
| Tier 1 | Preferred generic | $5 - $10 |
| Tier 2 | Non-preferred generic | $15 - $25 |
| Tier 3 | Preferred brand | $40 - $60 |
| Tier 4 | Non-preferred brand | $75 - $150 |
| Tier 5 | Specialty | 25-33% coinsurance |

### Specialty Tier Characteristics

Specialty tiers typically have:
- **Coinsurance** instead of copay (20-33%)
- **Cost maximums** (e.g., $250-$500/Rx)
- **Quantity limits** (30-day supply common)
- **Specialty pharmacy requirement**
- **Prior authorization** requirements

---

## Formulary Types

### Definition

A formulary is the list of prescription drugs covered by a health plan, organized by tier with coverage rules.

### Formulary Categories

**Open Formulary**:
- Covers most FDA-approved drugs
- Non-formulary drugs covered at higher cost
- Maximum flexibility for members
- Higher overall drug costs for plan

**Closed Formulary**:
- Only formulary drugs are covered
- Non-formulary drugs not covered at all
- Lower costs for plan
- More restrictive for members

**Incentive Formulary** (Most Common):
- All drugs potentially covered
- Tiered cost sharing encourages formulary use
- Balance of flexibility and cost control
- Non-formulary = highest tier

### Formulary Management

| Element | Description |
|---------|-------------|
| **P&T Committee** | Pharmacy & Therapeutics committee reviews drugs |
| **Clinical Criteria** | Evidence-based guidelines for coverage |
| **Tier Placement** | Based on efficacy, safety, and cost |
| **Utilization Management** | PA, step therapy, quantity limits |
| **Updates** | Quarterly or as needed |

---

## Pharmacy Networks

### Network Types

**Open Network**:
- Members can use any pharmacy
- Lower cost share at preferred pharmacies
- Higher cost share at non-preferred
- Maximum member convenience

**Preferred Network**:
- Incentivizes specific pharmacy chains
- Lower copays at preferred pharmacies
- Higher copays at non-preferred
- Cost savings through volume contracts

**Limited/Narrow Network**:
- Coverage only at select pharmacies
- Specialty drugs at specific pharmacies
- Lowest costs for plan
- Less convenience for members

### Pharmacy Types

| Type | Description | Typical Use |
|------|-------------|-------------|
| **Retail** | Neighborhood pharmacies | Acute medications |
| **Preferred Retail** | Contract pharmacies | Cost savings |
| **Mail Order** | Home delivery | Maintenance meds |
| **Specialty** | High-touch service | Complex therapies |
| **90-Day Retail** | Extended supply at retail | Maintenance alternative |

### Preferred vs Non-Preferred

| Factor | Preferred Pharmacy | Non-Preferred |
|--------|-------------------|---------------|
| Copay | Lower | Higher |
| Network | Contract | Non-contract |
| Examples | CVS, Walgreens (varies) | Independent |
| Savings | Plan negotiated rates | Standard pricing |

---

## Cost Sharing Models

### Copay Model

Fixed dollar amount per prescription:

| Tier | 30-Day Supply | 90-Day Supply |
|------|---------------|---------------|
| Generic | $10 | $25 |
| Preferred Brand | $40 | $100 |
| Non-Preferred | $80 | $200 |
| Specialty | $150 | N/A |

**Advantages**: Predictable costs for members
**Disadvantages**: Doesn't scale with drug cost

### Coinsurance Model

Percentage of drug cost:

| Tier | Coinsurance | Maximum |
|------|-------------|---------|
| Generic | 10% | None |
| Brand | 25% | $150 |
| Specialty | 30% | $300 |

**Advantages**: Aligns member/plan incentives
**Disadvantages**: Less predictable for members

### Hybrid Model

Combination of copay and coinsurance:

| Tier | Cost Share |
|------|------------|
| Generic | $10 copay |
| Brand | $40 copay or 25%, whichever greater |
| Specialty | 25% up to $500 max |

---

## Supply and Channel Rules

### Days Supply Limits

| Channel | Typical Limit | Use Case |
|---------|---------------|----------|
| Retail | 30 days | Acute medications |
| Mail Order | 90 days | Maintenance |
| 90-Day Retail | 90 days | Maintenance alternative |
| Specialty | 30 days | High-cost specialty |

### Maintenance Medication Rules

Many plans require maintenance medications to be filled through mail order or 90-day retail after initial fills:

```
Fill 1-2: Retail 30-day allowed
Fill 3+: Must use mail order or 90-day retail
Penalty: Higher copay or not covered at retail
```

### Specialty Pharmacy Requirements

Specialty drugs often must be filled at:
- Plan-designated specialty pharmacy
- Limited distribution specialty pharmacies
- Cannot use retail or mail order

---

## Accumulator Integration

### Medical vs Pharmacy Accumulators

| Structure | Description |
|-----------|-------------|
| **Combined** | Pharmacy and medical share deductible/OOP |
| **Separate** | Pharmacy has own deductible/OOP |
| **Pharmacy Exempt** | Pharmacy costs don't require deductible |

### Deductible Application

| Tier | Deductible Applies? |
|------|---------------------|
| Tier 1 (Generic) | Often exempt |
| Tier 2 (Preferred) | Sometimes exempt |
| Tier 3+ | Usually applies |
| Specialty | Always applies (HDHP) |

### Copay Accumulator Programs

**Traditional**:
- Manufacturer copay assistance counts toward deductible/OOP
- Member reaches OOP max faster

**Accumulator Adjustment (Controversial)**:
- Manufacturer assistance does NOT count toward accumulators
- Member pays full cost share after assistance ends
- Reduces plan cost, increases member exposure

---

## Examples

### Example 1: Understanding Tier Structures

**Prompt**: "Explain pharmacy benefit tier structures"

**Response**:

Pharmacy benefits organize drugs into tiers, with each tier having different cost sharing to encourage use of lower-cost medications.

**Common 4-Tier Structure**:

| Tier | What's Included | Typical Copay | Why |
|------|-----------------|---------------|-----|
| **Tier 1** | Generic drugs | $10 | Lowest cost, clinically equivalent |
| **Tier 2** | Preferred brands | $40 | Plan has negotiated discount |
| **Tier 3** | Non-preferred brands | $80 | Alternative available, higher cost |
| **Tier 4** | Specialty drugs | 25% coinsurance | High-cost, complex therapies |

**How Tier Placement Works**:
1. **Clinical Review**: P&T committee evaluates efficacy and safety
2. **Cost Analysis**: Plan considers acquisition cost and rebates
3. **Therapeutic Class**: Drugs compete within same class
4. **Preferred Status**: Manufacturer offers better rebate

**Member Impact**:
- Same drug can be different tiers on different plans
- Tier changes during the year possible
- Non-formulary drugs may not be covered at all

**Example**:
Lisinopril (generic ACE inhibitor): Tier 1, $10 copay
Diovan (brand ARB): Tier 3, $80 copay
Both treat hypertension, but generic ACE inhibitor is preferred first-line

---

### Example 2: Preferred Pharmacy Networks

**Prompt**: "How do preferred pharmacy networks work?"

**Response**:

Preferred pharmacy networks give members lower copays when they use specific pharmacy chains that have contracts with the plan.

**How It Works**:

| Pharmacy Type | Contract | Copay Impact |
|---------------|----------|--------------|
| **Preferred** | Has contract with plan | Lower copay |
| **Non-Preferred** | No contract | Higher copay |

**Example Cost Difference**:

| Drug Tier | Preferred Pharmacy | Non-Preferred |
|-----------|-------------------|---------------|
| Generic | $10 | $20 |
| Brand | $40 | $65 |
| Specialty | 25% | 40% |

**Common Preferred Networks**:
- CVS Caremark plans → CVS preferred
- Express Scripts → Walgreens often preferred
- OptumRx → Varies by region

**Why Plans Use Preferred Networks**:
1. **Volume discounts**: Guaranteed volume = lower prices
2. **Rebate sharing**: Pharmacy shares manufacturer rebates
3. **Data integration**: Better claims management
4. **Cost control**: Steers to lower-cost channels

**Member Considerations**:
- Check which pharmacies are preferred before filling
- Savings can be significant ($10-30 per prescription)
- Mail order is usually even cheaper than preferred retail
- Specialty drugs often require specific specialty pharmacies

---

## Boundary Note

This skill covers pharmacy benefit **concepts and structures**. For drug-specific information:

| Need | Use Instead |
|------|-------------|
| Is Drug X covered? | RxMemberSim |
| What tier is Drug Y? | RxMemberSim |
| PA criteria for Drug Z | RxMemberSim |
| Step therapy requirements | RxMemberSim |
| Drug alternatives | RxMemberSim |

---

## Related Skills

- [PBM Operations](pbm-operations.md) - How PBMs process claims
- [Specialty Pharmacy](specialty-pharmacy.md) - Specialty distribution
- [Synthetic Pharmacy Benefit](../synthetic/synthetic-pharmacy-benefit.md) - Generate benefit designs
- [Pharmacy for RX](../integration/pharmacy-for-rx.md) - RxMemberSim integration

---

*Pharmacy Benefit Concepts is a reference skill in the NetworkSim product.*
