# HealthSim Generative Framework: Taxonomy

*This document is stored in the Claude Project files. See /mnt/project/HEALTHSIM-GENERATIVE-TAXONOMY.md for full content.*

**Status**: Archived from design phase  
**Full Document**: Complete mental model and terminology reference

## Core Concepts

| Concept | Definition | Example |
|---------|------------|---------|
| **Profile** | "What are they?" - Population characteristics | Demographics, conditions, coverage |
| **Distribution** | "How do I pick values?" - Statistical tools | 60% HMO, 40% PPO |
| **Journey** | "What happens to them?" - Event sequences | Annual wellness visits |
| **Event** | "What's this moment?" - Discrete occurrence | Office visit, lab result |
| **Timing** | "When does it happen?" - Scheduling | Day 0, Day 30, Day 90 |
| **Trigger** | "This causes that" - Cross-domain connections | Encounter → Claim |

## Conceptual Model Dimensions

### Scope
- **Entity**: Single person
- **Cohort**: Group (10-1000)
- **Population**: Large scale (1000+)

### Temporality
- **Snapshot**: Point-in-time
- **Episode**: Single event sequence
- **Journey**: Weeks to months
- **Lifecycle**: Years

### Correlation
- **Isolated**: Single product
- **Linked**: Shared identifiers
- **Integrated**: Full cross-domain triggers

For complete diagrams and detailed explanations, reference the Claude Project file.
