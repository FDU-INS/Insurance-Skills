# Profile Builder Specification

*This document is stored in the Claude Project files. See /mnt/project/HEALTHSIM-PROFILE-BUILDER-SPECIFICATION.md for full content.*

**Status**: Archived from design phase  
**Full Document**: 700 lines covering the 4-phase conversation flow

## Overview

The Profile Builder is a conversational tool for constructing population specifications.

## Four-Phase Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│  Phase 1: Intent Recognition                                        │
│  - Detect scope (entity, cohort, population)                       │
│  - Identify domain (clinical, payer, pharmacy, trial)              │
│  - Extract key parameters from natural language                    │
└────────────────────────┬────────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────────┐
│  Phase 2: Profile Selection/Customization                           │
│  - Match to templates if applicable                                │
│  - Query PopulationSim for reference data                          │
│  - Build initial specification                                      │
└────────────────────────┬────────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────────┐
│  Phase 3: Refinement Loop                                           │
│  - Present specification for review                                │
│  - Accept adjustments                                              │
│  - Re-validate after changes                                       │
└────────────────────────┬────────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────────┐
│  Phase 4: Specification Confirmation                                │
│  - Final specification output                                      │
│  - Ready for execution                                             │
└─────────────────────────────────────────────────────────────────────┘
```

## Output Format

The Profile Builder produces a JSON specification that the Profile Executor consumes.

For complete schema and examples, reference the Claude Project file.
