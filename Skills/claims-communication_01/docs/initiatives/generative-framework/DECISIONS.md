# HealthSim Generative Framework: Design Decisions

*This document is stored in the Claude Project files. See /mnt/project/HEALTHSIM-GENERATIVE-FRAMEWORK-DECISIONS.md for full content.*

**Status**: Archived from design phase  
**Full Document**: 853 lines covering 7 major design decision points

## Key Decisions Made

| # | Decision Point | Options Considered | Decision |
|---|----------------|-------------------|----------|
| 1 | Specification Storage | JSON files, Skills, Python objects | **Skills-based** |
| 2 | Profile Resolution | Templates only, Data-driven only | **Hybrid approach** |
| 3 | Journey Complexity | Simple linear, Full branching | **Medium (linear + optional branching)** |
| 4 | Cross-Domain Sync | Loose coupling, Tight coupling | **Hybrid (configurable)** |
| 5 | Execution Model | Single-pass, Two-phase | **Two-phase (build then execute)** |
| 6 | Seed Management | Per-entity, Per-generation, Global | **Per-generation with override** |
| 7 | Output Batching | All at once, Streaming | **Batched (50 per batch)** |

For full rationale and alternatives analysis, reference the Claude Project file.
