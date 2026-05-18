---
name: network-types
description: |
  Reference knowledge about healthcare network types including HMO, PPO, EPO, 
  POS, and HDHP. Explains definitions, characteristics, cost structures, 
  pros/cons, and when to use each type. Use for understanding network concepts
  before generating synthetic network data.
  
  Trigger phrases: "network type", "HMO", "PPO", "EPO", "POS", "HDHP", 
  "difference between HMO and PPO", "explain network types", "compare networks",
  "gatekeeper", "open access", "high deductible"
version: "1.0"
category: reference
related_skills:
  - plan-structures
  - synthetic-network
  - network-for-member
---

# Network Types

## Overview

Healthcare network types define how members access care and share costs with their health plan. The five major network types represent different tradeoffs between cost, flexibility, and care coordination.

This skill provides reference knowledge about:
- HMO (Health Maintenance Organization)
- PPO (Preferred Provider Organization)
- EPO (Exclusive Provider Organization)
- POS (Point of Service)
- HDHP (High Deductible Health Plan)

---

## Trigger Phrases

Use this skill when you see:
- "What is an HMO?"
- "Difference between HMO and PPO"
- "Explain network types"
- "Compare PPO and EPO"
- "What is a gatekeeper model?"
- "High deductible health plan"
- "HSA eligible plans"
- "Which network type should I choose?"

---

## HMO (Health Maintenance Organization)

### Definition

An HMO is a closed network health plan that requires members to receive care from in-network providers and obtain referrals from a primary care physician (PCP) to see specialists.

### Key Characteristics

| Characteristic | HMO Approach |
|----------------|--------------|
| **Network** | Closed - must use in-network providers |
| **PCP Required** | Yes - serves as "gatekeeper" |
| **Referrals** | Required for specialist visits |
| **Out-of-Network** | Not covered except emergencies |
| **Care Coordination** | High - PCP coordinates all care |

### Cost Structure

- **Premiums**: Lowest among network types
- **Deductibles**: Often $0 or very low
- **Copays**: Fixed amounts (e.g., $20 PCP, $40 specialist)
- **Coinsurance**: Rarely used
- **Out-of-Pocket Maximum**: Lower than PPO

### Pros and Cons

**Advantages**:
- Lowest premiums
- Predictable costs (copays)
- Coordinated care through PCP
- No claim forms for in-network care
- Emphasis on preventive care

**Disadvantages**:
- No out-of-network coverage
- Requires referrals for specialists
- Less flexibility in provider choice
- Must change PCP to change medical home
- May require authorization for services

### When to Use

HMOs work best for:
- Cost-conscious individuals and families
- People who prefer coordinated care
- Those who don't need frequent specialist access
- Members comfortable with a single medical home
- Healthy individuals focused on preventive care

---

## PPO (Preferred Provider Organization)

### Definition

A PPO is an open network health plan that allows members to see any provider, with lower costs for in-network providers and higher costs for out-of-network providers.

### Key Characteristics

| Characteristic | PPO Approach |
|----------------|--------------|
| **Network** | Open - can use any provider |
| **PCP Required** | No |
| **Referrals** | Not required |
| **Out-of-Network** | Covered at higher cost share |
| **Care Coordination** | Member-directed |

### Cost Structure

- **Premiums**: Higher than HMO
- **Deductibles**: Moderate ($500-$2,000 typical)
- **Copays**: May use copays or coinsurance
- **Coinsurance**: Common (80/20 in-network, 60/40 out-of-network)
- **Out-of-Pocket Maximum**: Higher than HMO

### In-Network vs Out-of-Network

| Cost Component | In-Network | Out-of-Network |
|----------------|------------|----------------|
| Deductible | $1,000 | $2,000 |
| Coinsurance | 20% | 40% |
| OOP Maximum | $6,000 | $12,000 |
| Balance Billing | No | Yes |

**Balance Billing**: Out-of-network providers can bill members for the difference between their charge and the plan's allowed amount.

### Pros and Cons

**Advantages**:
- Freedom to see any provider
- No referrals needed
- Out-of-network coverage available
- Direct access to specialists
- Good for people who travel

**Disadvantages**:
- Higher premiums
- Higher out-of-pocket costs
- Out-of-network costs can be significant
- Balance billing risk
- Less care coordination

### When to Use

PPOs work best for:
- Those who value flexibility
- People with existing specialist relationships
- Frequent travelers
- Those willing to pay more for choice
- Members who dislike the referral process

---

## EPO (Exclusive Provider Organization)

### Definition

An EPO is a closed network health plan like an HMO, but without the PCP gatekeeper requirement. Members must use in-network providers but can self-refer to specialists.

### Key Characteristics

| Characteristic | EPO Approach |
|----------------|--------------|
| **Network** | Closed - must use in-network |
| **PCP Required** | Usually no |
| **Referrals** | Not required |
| **Out-of-Network** | Not covered except emergencies |
| **Care Coordination** | Member-directed within network |

### Cost Structure

- **Premiums**: Between HMO and PPO
- **Deductibles**: Moderate
- **Copays/Coinsurance**: Varies by plan
- **Out-of-Pocket Maximum**: Moderate

### Comparison to HMO and PPO

| Feature | HMO | EPO | PPO |
|---------|-----|-----|-----|
| Closed Network | Yes | Yes | No |
| PCP Required | Yes | No | No |
| Referrals | Yes | No | No |
| OON Coverage | No | No | Yes |
| Premiums | Lowest | Middle | Highest |

### Pros and Cons

**Advantages**:
- Lower premiums than PPO
- No referral requirements
- Direct specialist access
- Simpler than HMO administration
- Good network typically

**Disadvantages**:
- No out-of-network coverage
- Must stay in network
- Less coordinated than HMO
- Network may be smaller than PPO

### When to Use

EPOs work best for:
- Those who want specialist access without referrals
- Cost-conscious members who can stay in-network
- People comfortable with network restrictions
- Those who don't need out-of-network coverage
- Members in areas with good EPO networks

---

## POS (Point of Service)

### Definition

A POS plan is a hybrid of HMO and PPO that allows members to choose between in-network (HMO-like) and out-of-network (PPO-like) coverage at the point of service.

### Key Characteristics

| Characteristic | POS Approach |
|----------------|--------------|
| **Network** | Hybrid - in and out-of-network options |
| **PCP Required** | Yes for in-network |
| **Referrals** | Required for in-network specialist |
| **Out-of-Network** | Covered at higher cost |
| **Care Coordination** | PCP-directed for in-network |

### How It Works

1. **In-Network Path** (HMO-like):
   - Use PCP as gatekeeper
   - Get referrals for specialists
   - Pay lower copays/coinsurance

2. **Out-of-Network Path** (PPO-like):
   - Self-refer to any provider
   - No PCP involvement
   - Pay higher deductible and coinsurance

### Cost Structure

| Component | In-Network | Out-of-Network |
|-----------|------------|----------------|
| Deductible | $500 | $1,500 |
| Copay (PCP) | $25 | N/A |
| Coinsurance | 10% | 30% |
| OOP Max | $4,000 | $8,000 |

### Pros and Cons

**Advantages**:
- Flexibility to go out-of-network
- Lower in-network costs than PPO
- Coordinated care option available
- Best of both worlds approach
- Good for uncertain healthcare needs

**Disadvantages**:
- Higher premiums than HMO
- Referrals required for in-network specialists
- Complex to understand
- Must manage two sets of benefits
- May encourage higher utilization

### When to Use

POS plans work best for:
- Those who want flexibility but usually stay in-network
- Members unsure about their provider needs
- People with some out-of-network providers
- Those who value having options
- Families with diverse healthcare needs

---

## HDHP (High Deductible Health Plan)

### Definition

An HDHP is a health plan with a higher deductible than traditional plans, often paired with a Health Savings Account (HSA) for tax-advantaged savings.

### Key Characteristics

| Characteristic | HDHP Approach |
|----------------|--------------|
| **Network** | Varies (can be HMO, PPO, or EPO) |
| **Deductible** | High ($1,600+ individual, $3,200+ family for 2024) |
| **HSA Eligible** | Yes, if meets IRS requirements |
| **Preventive Care** | Covered pre-deductible |
| **Cost Sharing** | Member pays more until deductible met |

### 2024 IRS Requirements for HSA Eligibility

| Requirement | Individual | Family |
|-------------|------------|--------|
| Minimum Deductible | $1,600 | $3,200 |
| Maximum OOP | $8,050 | $16,100 |
| HSA Contribution Limit | $4,150 | $8,300 |
| Catch-Up (55+) | +$1,000 | +$1,000 |

### HSA Triple Tax Advantage

1. **Tax-Deductible Contributions** - Reduce taxable income
2. **Tax-Free Growth** - Investments grow without tax
3. **Tax-Free Withdrawals** - For qualified medical expenses

### Cost Structure

| Component | HDHP |
|-----------|------|
| Premiums | Lowest |
| Deductible | $2,000-$5,000+ |
| Coinsurance | 20-30% after deductible |
| OOP Max | IRS limits apply |
| Preventive | $0 (pre-deductible) |

### Pros and Cons

**Advantages**:
- Lowest premiums
- HSA tax advantages
- HSA funds roll over (no "use it or lose it")
- HSA portable (stays with you)
- Good for healthy individuals
- Retirement savings vehicle

**Disadvantages**:
- High out-of-pocket exposure
- May delay needed care
- Requires financial literacy
- Not ideal for chronic conditions
- HSA requires discipline to fund

### When to Use

HDHPs work best for:
- Healthy individuals with low healthcare utilization
- Those who can afford high deductible if needed
- People who want to save for future healthcare
- Tax-advantaged savings seekers
- Financially disciplined individuals

---

## Comparison Table

| Feature | HMO | PPO | EPO | POS | HDHP |
|---------|-----|-----|-----|-----|------|
| **Premiums** | Lowest | Highest | Middle | Middle-High | Low |
| **Deductible** | Low/None | Moderate | Moderate | Varies | High |
| **OON Coverage** | No | Yes | No | Yes | Varies |
| **PCP Required** | Yes | No | No | Yes (in-net) | Varies |
| **Referrals** | Yes | No | No | Yes (in-net) | Varies |
| **Flexibility** | Low | High | Low | Medium | Varies |
| **HSA Eligible** | Rarely | Rarely | Rarely | Rarely | Yes |
| **Best For** | Cost-conscious | Flexibility | Balanced | Uncertain | Healthy/Savers |

---

## Examples

### Example 1: Comparing HMO and PPO

**Prompt**: "What's the difference between HMO and PPO?"

**Response**:

HMO and PPO represent opposite ends of the cost-flexibility spectrum:

**HMO (Health Maintenance Organization)**:
- Closed network - you must use in-network providers
- Requires a primary care physician (PCP) who coordinates your care
- Need referrals to see specialists
- Out-of-network care not covered (except emergencies)
- Lower premiums, copays, and out-of-pocket costs

**PPO (Preferred Provider Organization)**:
- Open network - you can see any provider
- No PCP requirement
- No referrals needed for specialists
- Out-of-network care covered at higher cost
- Higher premiums but more flexibility

**Key Tradeoff**: HMOs offer lower costs in exchange for less flexibility. PPOs offer more choice but at higher premiums and cost sharing.

**Example Cohort**:
- Sarah is healthy, lives near a good HMO network, and wants to minimize costs → **HMO**
- John travels frequently, has established specialists, and values flexibility → **PPO**

---

### Example 2: Understanding HDHP and HSA

**Prompt**: "Explain HDHP plans and HSA eligibility"

**Response**:

A High Deductible Health Plan (HDHP) is a health plan with a higher deductible than traditional plans, designed to be paired with a Health Savings Account (HSA).

**2024 HDHP Requirements**:
| | Individual | Family |
|--|-----------|--------|
| Minimum Deductible | $1,600 | $3,200 |
| Maximum Out-of-Pocket | $8,050 | $16,100 |

**HSA Eligibility Rules**:
1. Must be enrolled in an HSA-eligible HDHP
2. Cannot be enrolled in Medicare
3. Cannot be claimed as a dependent
4. Cannot have other non-HDHP health coverage

**2024 HSA Contribution Limits**:
| | Individual | Family |
|--|-----------|--------|
| Standard Limit | $4,150 | $8,300 |
| Age 55+ Catch-Up | +$1,000 | +$1,000 |

**Triple Tax Advantage**:
1. Contributions are tax-deductible (or pre-tax if through payroll)
2. Investment growth is tax-free
3. Withdrawals for qualified medical expenses are tax-free

**Important**: Preventive care (annual physicals, immunizations, screenings) is covered at 100% before the deductible.

**Best For**: Healthy individuals who want low premiums and tax-advantaged savings for future healthcare costs.

---

## Generation Guidance

When generating network configurations:

| Network Type | Use When |
|--------------|----------|
| HMO | Employer wants lowest cost, regional coverage |
| PPO | Employer values flexibility, national coverage |
| EPO | Balance of cost and specialist access |
| POS | Employer wants options for diverse workforce |
| HDHP | Employer wants to promote consumerism, offer HSA |

---

## Related Skills

- [Plan Structures](plan-structures.md) - Benefit component details
- [Synthetic Network](../synthetic/synthetic-network.md) - Generate network configurations
- [Network for Member](../integration/network-for-member.md) - MemberSim integration
- [Network Adequacy](network-adequacy.md) - Access standards

---

*Network Types is a reference skill in the NetworkSim product.*
