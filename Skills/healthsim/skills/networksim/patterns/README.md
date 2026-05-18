---
name: patterns-readme
description: Overview of NetworkSim pattern/template skills
version: "1.0"
category: patterns
---

# NetworkSim Patterns

## Overview

This directory contains reusable configuration patterns and templates for healthcare networks and pharmacy benefits. These patterns represent common industry approaches that can be used as starting points for generating synthetic network configurations.

## Pattern Categories

### Network Patterns

Templates for provider network configurations:

| Pattern | Description | Key Use Cases |
|---------|-------------|---------------|
| [HMO Network Pattern](hmo-network-pattern.md) | Gatekeeper model with closed network | Medicare Advantage, Medicaid MCO, Cost-focused commercial |
| [PPO Network Pattern](ppo-network-pattern.md) | Open access with in/out-of-network tiers | Standard commercial, National employers |
| [Tiered Network Pattern](tiered-network-pattern.md) | Quality/cost-based provider tiers | Value-based designs, ACA exchange, Large employers |

### Pharmacy Benefit Patterns

Templates for pharmacy benefit configurations:

| Pattern | Description | Key Use Cases |
|---------|-------------|---------------|
| [Pharmacy Benefit Patterns](pharmacy-benefit-patterns.md) | Tier structures, formularies, clinical programs | All pharmacy benefit designs |
| [Specialty Distribution Pattern](specialty-distribution-pattern.md) | Hub models, site-of-care, limited distribution | Specialty drug programs |

---

## How to Use Patterns

### 1. Select Appropriate Pattern

Based on your use case:

- **HMO Pattern**: When generating closed networks with PCP gatekeepers
- **PPO Pattern**: When generating open access networks
- **Tiered Pattern**: When generating value-based or narrow networks
- **Pharmacy Patterns**: When designing drug benefit structures
- **Specialty Distribution**: When configuring specialty pharmacy programs

### 2. Apply Pattern Template

Each pattern provides:
- Base configuration template with placeholders
- Multiple variants for common sub-types
- Example complete configurations
- Validation checklists

### 3. Customize for Cohort

Modify pattern parameters for your specific:
- Geographic market
- Line of business (Commercial, Medicare, Medicaid)
- Employer size and preferences
- Regulatory requirements

---

## Pattern Components

Each pattern skill includes:

| Component | Purpose |
|-----------|---------|
| Pattern Variants | Sub-types within the pattern category |
| Template Configuration | JSON template with placeholders |
| Cost Sharing Templates | Typical cost sharing structures |
| Complete Examples | Fully specified configurations |
| Validation Checklist | Requirements to verify |

---

## Integration with Synthetic Skills

Patterns are designed to feed into synthetic generation skills:

```
[Pattern Skill] → [Synthetic Skill] → [Generated Entity]

hmo-network-pattern → synthetic-network → HMO network configuration
ppo-network-pattern → synthetic-network → PPO network configuration
pharmacy-benefit-patterns → synthetic-pharmacy-benefit → Rx benefit design
specialty-distribution-pattern → synthetic-pharmacy → Specialty pharmacy entity
```

---

## Cross-Product Usage

Patterns support cross-product integration:

| Pattern | Used By |
|---------|---------|
| HMO/PPO Network | MemberSim (network context for claims) |
| Tiered Network | MemberSim (cost sharing calculations) |
| Pharmacy Benefit | RxMemberSim (adjudication logic) |
| Specialty Distribution | RxMemberSim (pharmacy routing) |

---

## Related Skills

- [Reference Skills](../reference/) - Conceptual knowledge behind patterns
- [Synthetic Skills](../synthetic/) - Generate entities from patterns
- [Integration Skills](../integration/) - Apply to other products

---

*Patterns are template skills in the NetworkSim product.*
