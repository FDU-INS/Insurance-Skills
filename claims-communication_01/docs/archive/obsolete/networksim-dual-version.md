# NetworkSim Data Architecture

**Purpose**: Explains the two data source options for NetworkSim provider/facility/pharmacy data

---

## Overview

NetworkSim supports two data modes, allowing users to choose between lightweight synthetic generation or comprehensive real provider data:

| Mode | Skill Trigger | Data Source | Use Case |
|------|---------------|-------------|----------|
| **Generated** | NetworkSim-Gen | Synthetic on-demand | Quick demos, tutorials, testing |
| **Database** | NetworkSim-DB | Real NPPES via DuckDB | Research, validation, analytics |

Users choose their mode based on whether they download the optional NPPES database.

---

## NetworkSim-Gen (Default)

The default mode uses Claude to generate synthetic provider entities on-demand. No additional downloads required.

### Characteristics

- **Synthetic NPIs**: Valid format, but not real registrations
- **On-demand generation**: Claude creates entities during conversation
- **Lightweight**: No large data files needed
- **Consistent with tutorials**: All hello-healthsim examples use this mode
- **Fully integrated**: Works seamlessly with PatientSim, MemberSim, TrialSim

### Example

```
User: Generate a cardiologist in San Francisco

Claude: [Uses NetworkSim-Gen]

{
  "npi": "1234567890",          // Valid format, synthetic
  "entity_type": "individual",
  "name": {
    "first": "Sarah",
    "last": "Chen",
    "credential": "MD"
  },
  "specialty": "Internal Medicine",
  "taxonomy_code": "207RC0000X",
  "address": {
    "city": "San Francisco",
    "state": "CA",
    "zip": "94102"
  }
}
```

---

## NetworkSim-DB (Optional)

For users who need real provider data, NetworkSim-DB queries the NPPES registry stored in DuckDB.

### Characteristics

- **Real NPIs**: Actual registered provider identifiers
- **9M+ providers**: Complete US provider registry
- **Geographic analysis**: Real provider distribution by specialty and location
- **SQL queryable**: Complex filtering and aggregation
- **Larger footprint**: ~1.7GB DuckDB database

### Setup Required

To use NetworkSim-DB, users must download and build the NPPES database:

```bash
# Clone the NetworkSim-DB repository (public)
git clone https://github.com/mark64oswald/networksim-db.git

# Run setup (downloads NPPES, builds DuckDB)
cd networksim-db
python setup/setup-all.py
```

The database is stored at `~/.healthsim/networksim.duckdb` and is separate from the main HealthSim database.

### Example

```
User: Find real cardiologists in San Francisco

Claude: [Uses NetworkSim-DB, queries DuckDB]

Found 342 cardiologists in San Francisco County:

| NPI | Name | Specialty | Address |
|-----|------|-----------|---------|
| 1679576722 | John Smith, MD | Cardiovascular Disease | 450 Sutter St |
| 1234567893 | Maria Garcia, MD | Interventional Cardiology | 2100 Webster St |
| ... | ... | ... | ... |
```

---

## When to Use Each Mode

### Use NetworkSim-Gen (Default) When:

- Running demos or tutorials
- Generating test data for development
- Creating reproducible synthetic cohorts
- Building public-facing content
- Quick prototyping without setup

### Use NetworkSim-DB When:

- Validating against real provider distributions
- Research requiring actual NPI lookups
- Geographic analysis of real provider networks
- Enriching synthetic data with real attributes
- Building features that will use real data in production

---

## Automatic Mode Selection

Claude selects the appropriate mode based on:

1. **Explicit request**: "Find real cardiologists" → NetworkSim-DB
2. **Database availability**: If DuckDB database exists → NetworkSim-DB available
3. **Generation request**: "Generate a cardiologist" → NetworkSim-Gen
4. **Fallback**: If database not available but real data requested → Inform user

### Example Routing

```
"Generate a provider in Texas"
→ NetworkSim-Gen (generation request)

"Find real pediatricians in Austin"  
→ NetworkSim-DB (real data request)

"How many cardiologists are in California?"
→ NetworkSim-DB (analysis request)

"Create a specialty pharmacy network"
→ NetworkSim-Gen (generation request)
```

---

## Implementation Status

| Component | Status | Location |
|-----------|--------|----------|
| NetworkSim-Gen skills | ✅ Complete | `skills/networksim/synthetic/` |
| NetworkSim-Gen integration | ✅ Complete | `skills/networksim/integration/` |
| NetworkSim-DB repository | 🔮 Planned | `github.com/mark64oswald/networksim-db` |
| NetworkSim-DB skills | 🔮 Planned | `skills/networksim/database/` |
| Automatic mode selection | 🔮 Planned | Future enhancement |

**Current State**: NetworkSim-Gen is fully functional. NetworkSim-DB repository is public and available at [github.com/mark64oswald/networksim-db](https://github.com/mark64oswald/networksim-db). The NetworkSim-DB skills (database query skills) are planned for a future session.

---

## Data Comparison

### NetworkSim-Gen Output

```json
{
  "npi": "1234567890",          // Valid format, synthetic
  "entity_type": "individual",
  "provider": {
    "last_name": "Chen",
    "first_name": "Sarah",
    "credential": "MD, FACC"
  },
  "taxonomy_code": "207RC0000X",
  "practice_location": {
    "city": "San Francisco",
    "state": "CA"
  }
}
```

### NetworkSim-DB Output

```json
{
  "npi": "1679576722",          // Real registered NPI
  "entity_type_code": "1",
  "provider_last_name_legal_name": "SMITH",
  "provider_first_name": "JOHN",
  "provider_credential_text": "MD",
  "healthcare_provider_taxonomy_code_1": "207RC0000X",
  "provider_business_practice_location_address_city_name": "SAN FRANCISCO",
  "provider_business_practice_location_address_state_name": "CA"
}
```

---

## Repository Structure (Future)

### NetworkSim-DB Repository

```
networksim-db/
├── README.md                  # Overview and setup
├── SKILL.md                   # Skill reference  
├── networksim-db.code-workspace
│
├── setup/                     # Setup scripts
│   ├── setup-all.py          # Full setup workflow
│   ├── download-nppes.py     # Download NPPES data
│   ├── build-database.py     # Build DuckDB
│   └── validate-db.py        # Validation checks
│
├── skills/                    # Query skills
│   ├── provider-lookup.md    # Find providers by NPI
│   ├── geographic-search.md  # Search by location
│   ├── specialty-analysis.md # Specialty distribution
│   └── network-builder.md    # Build real networks
│
└── data/                      # LOCAL ONLY - gitignored
    ├── README.md              # Data documentation
    ├── nppes/                 # Raw NPPES CSVs
    └── networksim.duckdb      # Built database
```

---

## Reference Data Philosophy

NetworkSim-DB follows the same data architecture principles as PopulationSim:

| Aspect | Skills Files | DuckDB |
|--------|--------------|--------|
| **Source** | HealthSim-created | External (CMS/NPPES) |
| **Size** | < 1MB | > 1GB |
| **Updates** | Version controlled | Monthly NPPES refresh |
| **Access** | Read during generation | SQL queries |
| **Required** | Yes (core function) | Optional (enhanced function) |

See [Data Architecture](./data-architecture.md) for the full reference data philosophy.

---

## Related Documentation

- [NetworkSim SKILL.md](../skills/networksim/SKILL.md) - Current skill reference
- [Data Architecture](./data-architecture.md) - Reference data philosophy
- [PopulationSim](../skills/populationsim/SKILL.md) - Similar DuckDB pattern

---

*Last Updated: December 2024*
