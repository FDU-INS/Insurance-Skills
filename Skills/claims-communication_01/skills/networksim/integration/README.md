---
name: integration-readme
description: Overview of NetworkSim integration skills for cross-product use
version: "1.0"
category: integration
---

# NetworkSim Integration Skills

## Overview

Integration skills bridge NetworkSim entities to other HealthSim products. They provide context-aware generation and enrichment of network-related data for realistic cross-product cohorts.

## Integration Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         HealthSim Products                          │
├─────────────┬─────────────┬─────────────┬─────────────┬────────────┤
│  PatientSim │  MemberSim  │ RxMemberSim │   TrialSim  │ PopulationSim│
└──────┬──────┴──────┬──────┴──────┬──────┴──────┬──────┴──────┬──────┘
       │             │             │             │             │
       ▼             ▼             ▼             ▼             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    NetworkSim Integration Layer                      │
├─────────────────┬─────────────────┬─────────────────┬───────────────┤
│ Provider for    │ Network for     │ Pharmacy for    │ Benefit for   │
│ Encounter       │ Member          │ Rx              │ Claim         │
├─────────────────┼─────────────────┼─────────────────┼───────────────┤
│ Formulary for   │                 │                 │               │
│ Rx              │                 │                 │               │
└─────────────────┴─────────────────┴─────────────────┴───────────────┘
       │             │             │             │
       ▼             ▼             ▼             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      NetworkSim Core Skills                          │
├─────────────────┬─────────────────┬─────────────────────────────────┤
│    Reference    │    Synthetic    │           Patterns              │
└─────────────────┴─────────────────┴─────────────────────────────────┘
```

---

## Integration Skills

| Skill | Source Product | Purpose |
|-------|---------------|---------|
| [Provider for Encounter](provider-for-encounter.md) | PatientSim, TrialSim | Generate appropriate providers for encounters |
| [Network for Member](network-for-member.md) | MemberSim | Determine network status and cost sharing |
| [Pharmacy for Rx](pharmacy-for-rx.md) | RxMemberSim | Route prescriptions to appropriate pharmacy |
| [Benefit for Claim](benefit-for-claim.md) | MemberSim, RxMemberSim | Apply benefit structure for adjudication |
| [Formulary for Rx](formulary-for-rx.md) | RxMemberSim | Determine formulary coverage and programs |

---

## Integration Patterns

### Pattern 1: Context → Entity Generation

Source product provides context, integration skill generates NetworkSim entity.

```
PatientSim Encounter Context
    │
    ▼
┌─────────────────────────┐
│ Provider for Encounter  │
│ - Analyze diagnosis     │
│ - Match specialty       │
│ - Generate provider     │
└─────────────────────────┘
    │
    ▼
NetworkSim Provider Entity
```

**Example Use Cases**:
- Generate attending physician for inpatient admission
- Create specialist for referral visit
- Assign surgeon for procedure

### Pattern 2: Entity → Status Determination

Source product provides entity, integration skill determines status/context.

```
MemberSim Claim + Provider
    │
    ▼
┌─────────────────────────┐
│ Network for Member      │
│ - Check network roster  │
│ - Determine tier        │
│ - Return cost sharing   │
└─────────────────────────┘
    │
    ▼
Network Status + Cost Sharing
```

**Example Use Cases**:
- Determine if provider is in-network
- Assign network tier for tiered products
- Calculate tier-based cost sharing

### Pattern 3: Entity → Routing Decision

Source product provides entity, integration skill determines routing.

```
RxMemberSim Prescription
    │
    ▼
┌─────────────────────────┐
│ Pharmacy for Rx         │
│ - Analyze drug          │
│ - Check specialty ind   │
│ - Route to pharmacy     │
└─────────────────────────┘
    │
    ▼
Pharmacy Assignment + Routing
```

**Example Use Cases**:
- Route specialty drug to specialty pharmacy
- Direct maintenance medication to mail order
- Select preferred retail pharmacy

### Pattern 4: Entity → Coverage Determination

Source product provides entity, integration skill determines coverage.

```
RxMemberSim Drug
    │
    ▼
┌─────────────────────────┐
│ Formulary for Rx        │
│ - Check formulary       │
│ - Get tier/cost sharing │
│ - Check clinical pgms   │
└─────────────────────────┘
    │
    ▼
Formulary Status + Programs
```

**Example Use Cases**:
- Determine if drug is on formulary
- Identify prior authorization requirements
- Apply step therapy protocols

---

## Cross-Product Data Flow

### Complete Claim Flow Example

```
1. PatientSim: Generate encounter
       │
       ▼
2. Provider for Encounter: Add provider to encounter
       │
       ▼
3. MemberSim: Create claim from encounter
       │
       ▼
4. Network for Member: Determine network status
       │
       ▼
5. Benefit for Claim: Calculate cost sharing
       │
       ▼
6. MemberSim: Complete adjudicated claim
```

### Complete Rx Flow Example

```
1. PatientSim: Generate prescription
       │
       ▼
2. RxMemberSim: Create Rx claim
       │
       ▼
3. Formulary for Rx: Check coverage/tier
       │
       ▼
4. Pharmacy for Rx: Route to pharmacy
       │
       ▼
5. RxMemberSim: Adjudicate with cost sharing
```

---

## Integration Input/Output Contracts

### Standard Input Context

All integration skills accept context objects with these common elements:

```json
{
  "member_context": {
    "member_id": "Required",
    "plan_id": "Required",
    "effective_date": "Required",
    "location": "Recommended"
  },
  "service_context": {
    "service_date": "Required",
    "service_type": "Required",
    "codes": "As applicable"
  }
}
```

### Standard Output Structure

All integration skills return structured output with:

```json
{
  "status": "Determination result",
  "entity": "Generated or enriched entity",
  "cost_sharing": "If applicable",
  "programs": "Clinical programs if applicable",
  "integration_metadata": {
    "source_product": "Originating product",
    "generated_at": "Timestamp",
    "logic_applied": "Description of matching/routing"
  }
}
```

---

## Usage Guidelines

### When to Use Integration Skills

1. **Cross-product cohorts**: When generating data that spans multiple products
2. **Realistic adjudication**: When claims need accurate cost sharing
3. **Network-aware generation**: When providers/pharmacies must match plan context
4. **Coverage determination**: When formulary/benefit context is needed

### When NOT to Use Integration Skills

1. **Standalone generation**: Use synthetic skills directly
2. **Reference lookups**: Use reference skills for concepts
3. **Pattern templates**: Use pattern skills for configurations

---

## Related Skill Categories

- [Reference Skills](../reference/) - Conceptual knowledge
- [Synthetic Skills](../synthetic/) - Entity generation
- [Pattern Skills](../patterns/) - Configuration templates

---

*Integration skills bridge NetworkSim to other HealthSim products.*
