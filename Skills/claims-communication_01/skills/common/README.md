# Common Skills

Cross-product infrastructure skills that apply to all HealthSim products.

## Skills Overview

| Skill | Purpose | Triggers |
|-------|---------|----------|
| [State Management](state-management.md) | Save, load, and query cohorts | save, load, persist, resume |
| [Identity Correlation](identity-correlation.md) | Link entities across products | find member, link patient, correlate |
| [DuckDB Skill](duckdb-skill.md) | Direct database operations | query, SQL, schema |

## State Management

Enables persistence of generated data across sessions:

- **Save cohorts** - Snapshot your workspace as a named cohort
- **Load cohorts** - Restore previous work
- **Auto-persist** - Token-efficient batch generation
- **Query data** - SQL access to saved entities

**Example:**
```
Save these patients as "cardiac-rehab-cohort"
```

See [state-management.md](state-management.md) for details.

## Identity Correlation

Links entities across products using SSN as the universal correlator:

```
Person (SSN: 123-45-6789)
├── Patient (MRN: P001) - PatientSim
├── Member (MBI: M001) - MemberSim  
├── RxMember (ID: RX001) - RxMemberSim
└── Subject (ID: S001) - TrialSim
```

**Example:**
```
Find the member record for patient MRN P001
```

See [identity-correlation.md](identity-correlation.md) for details.

## DuckDB Skill

Direct database access for advanced queries:

- Schema exploration
- Custom SQL queries
- Reference data access
- Aggregations and analysis

**Example:**
```sql
SELECT * FROM cohorts WHERE name LIKE '%diabetic%'
```

See [duckdb-skill.md](duckdb-skill.md) for details.

## Related Documentation

- [Data Architecture](../../docs/data-architecture.md) - Database schema details
- [Cross-Product Integration](../../docs/HEALTHSIM-ARCHITECTURE-GUIDE.md#3-product-relationships) - How products work together
