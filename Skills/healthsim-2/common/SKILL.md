# Common Skills - Master Reference

Cross-product infrastructure skills that enable persistence, identity correlation, and database operations across all HealthSim products.

## Quick Start

```
# Save your current work
Save this cohort as "demo-patients"

# Load previous work
Load the cohort named "demo-patients"

# Find related entities
Find the member record for patient MRN-12345

# Query the database
Show me all cohorts created in the last week
```

## Core Capabilities

### State Management
Persist generated data across sessions with cohort save/load operations. Supports auto-persist for token-efficient batch generation.

**Triggers**: save, load, persist, resume, snapshot, restore
**Details**: [state-management.md](state-management.md)

### Identity Correlation
Link entities across products using SSN as the universal correlator. Track the same person as patient, member, rx member, and trial subject.

**Triggers**: find member, link patient, correlate, same person, cross-reference
**Details**: [identity-correlation.md](identity-correlation.md)

### DuckDB Operations
Direct database access for advanced queries, schema exploration, and reference data access.

**Triggers**: query, SQL, schema, database, show tables
**Details**: [duckdb-skill.md](duckdb-skill.md)

## Cross-Product Architecture

Common skills enable data flow between products:

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  PatientSim │    │  MemberSim  │    │ RxMemberSim │
│   (MRN)     │    │   (MBI)     │    │  (RxID)     │
└──────┬──────┘    └──────┬──────┘    └──────┬──────┘
       │                  │                  │
       └────────┬─────────┴─────────┬────────┘
                │                   │
         ┌──────▼───────┐   ┌───────▼──────┐
         │  Identity    │   │    State     │
         │ Correlation  │   │  Management  │
         │   (SSN)      │   │  (Cohorts)   │
         └──────────────┘   └──────────────┘
                │                   │
                └─────────┬─────────┘
                          │
                   ┌──────▼──────┐
                   │   DuckDB    │
                   │  Database   │
                   └─────────────┘
```

## Database Schema

Common skills work with these core tables:

| Table | Purpose | Key Columns |
|-------|---------|-------------|
| cohorts | Saved cohort metadata | cohort_id, name, created_at |
| persons | Core person identity | person_id, ssn, demographics |
| patients | PatientSim entities | patient_id, mrn, person_id |
| members | MemberSim entities | member_id, mbi, person_id |
| rx_members | RxMemberSim entities | rx_member_id, rx_id, person_id |

## Related Skills

- [Generation Skills](../generation/SKILL.md) - Profile and journey building
- [PopulationSim](../populationsim/SKILL.md) - Reference data and population targeting
- [NetworkSim](../networksim/SKILL.md) - Provider network modeling

---

*Part of HealthSim Workspace Infrastructure*
