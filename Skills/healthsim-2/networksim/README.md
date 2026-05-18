# NetworkSim

> Query 8.9 million real US healthcare providers and generate synthetic provider entities when needed.

## What NetworkSim Does

NetworkSim is the **provider network** component of HealthSim. Its primary function is providing access to **real reference data**—8.9 million US healthcare providers from the NPPES registry stored in DuckDB. This real data grounds HealthSim cohorts in actual provider information.

When real data isn't appropriate (demos, tutorials, testing), NetworkSim can also generate synthetic providers with valid-format NPIs.

## Capabilities

| Capability | Description | Primary Use |
|------------|-------------|-------------|
| **Real Provider Queries** | Search 8.9M providers by specialty, location, credentials | Production cohorts, validation |
| **Geographic Analysis** | Provider distribution by county, state, metro area | Network adequacy, planning |
| **Facility Lookup** | Find hospitals, ASCs, clinics with quality metrics | Care coordination, referrals |
| **Synthetic Generation** | Create test providers when real data isn't needed | Demos, tutorials, testing |

## Quick Start: Query Real Providers

NetworkSim's primary value is access to real NPPES data. Here are common queries:

### Find Providers by Specialty and Location

```
Find cardiologists in Houston, TX
```

Claude queries `network.providers` and returns real providers:

| NPI | Name | Credentials | City | Taxonomy |
|-----|------|-------------|------|----------|
| 1234567890 | Dr. Sarah Chen | MD, FACC | Houston | Cardiovascular Disease |
| 1987654321 | Dr. Michael Patel | MD, FSCAI | Houston | Interventional Cardiology |
| ... | ... | ... | ... | ... |

### Count Providers by Region

```
How many primary care physicians are in San Diego County?
```

Claude returns aggregate statistics from real data:
- Total PCPs: 2,847
- Internal Medicine: 1,245
- Family Medicine: 1,602

### Find Hospitals with Quality Data

```
Show me hospitals in Phoenix with 4+ star ratings
```

Claude joins provider and quality tables to return real facilities with their CMS quality scores.

### Verify a Provider Exists

```
Is NPI 1234567890 a valid cardiologist?
```

Claude looks up the exact NPI in the database and confirms the provider's specialty, location, and credentials.

## Data Architecture

All reference data is in the unified HealthSim DuckDB database (`network` schema):

| Table | Records | Description |
|-------|---------|-------------|
| `network.providers` | 8,925,672 | All US healthcare providers from NPPES |
| `network.facilities` | ~35,000 | Medicare-certified facilities from CMS POS |
| `network.hospital_quality` | ~4,500 | Hospital quality metrics from CMS |
| `network.physician_quality` | ~1.2M | Physician quality data from CMS |
| `network.ahrf_county` | ~3,200 | County healthcare resources from HRSA |

**Data Source**: CMS NPPES (National Plan and Provider Enumeration System) - public domain, updated monthly.

### Provider Table Structure

Key columns in `network.providers`:

| Column | Description |
|--------|-------------|
| `npi` | 10-digit National Provider Identifier |
| `entity_type_code` | 1=Individual, 2=Organization |
| `first_name`, `last_name` | Provider name (individuals) |
| `organization_name` | Organization name (type 2) |
| `primary_taxonomy_code` | Healthcare Provider Taxonomy Code |
| `city`, `state`, `zip_code` | Practice location |
| `credential_text` | Credentials (MD, DO, NP, etc.) |

### Example SQL Queries

**Find specialists by taxonomy:**
```sql
SELECT npi, first_name, last_name, credential_text, city
FROM network.providers
WHERE state = 'CA'
  AND primary_taxonomy_code = '207RC0000X'  -- Cardiovascular Disease
  AND city = 'SAN FRANCISCO'
LIMIT 10;
```

**Count providers by state:**
```sql
SELECT state, COUNT(*) as provider_count
FROM network.providers
WHERE entity_type_code = '1'  -- Individuals only
GROUP BY state
ORDER BY provider_count DESC;
```

**Join with quality data:**
```sql
SELECT p.organization_name, p.city, h.overall_rating
FROM network.providers p
JOIN network.hospital_quality h ON p.npi = h.facility_id
WHERE p.state = 'TX' AND h.overall_rating >= 4;
```

## When to Use Real vs. Synthetic Data

### Use Real Data (Primary Use Case)

- **Production cohorts** - Ground synthetic patients in real provider networks
- **Validation** - Verify NPIs exist and have correct specialties
- **Analysis** - Understand provider distribution, network adequacy
- **Integration testing** - Use real NPIs for realistic claim and encounter data
- **Research** - Analyze provider characteristics by geography

### Use Synthetic Generation (When Real Data Doesn't Fit)

- **Tutorials and demos** - When you don't want to reference real providers
- **Training materials** - Avoid any connection to actual practitioners
- **Reproducible cohorts** - Same synthetic provider every time
- **Specialized testing** - Need exact credentials or characteristics

## Synthetic Generation

When you need synthetic providers (rather than querying real ones):

```
Generate a synthetic cardiologist for this patient's encounter
Generate a 200-bed community hospital
Generate a specialty pharmacy for oncology
```

Claude creates entities with valid-format NPIs and appropriate characteristics. The generated data follows real-world patterns but doesn't reference actual providers.

## Integration with Other Products

| Product | NetworkSim Provides | Example |
|---------|---------------------|---------|
| **PatientSim** | Attending, referring, PCP NPIs | Real cardiologist NPI for heart failure encounter |
| **MemberSim** | Billing provider, network status | In-network verification for claim adjudication |
| **RxMemberSim** | Dispensing pharmacy | Real pharmacy NPI for prescription fill |
| **TrialSim** | Site, investigator | PI credentials for trial site |

When generating encounters, claims, or prescriptions, other products can reference real providers from NetworkSim data or request synthetic ones.

## Domain Knowledge

NetworkSim also provides reference knowledge about provider networks:

| Topic | Description |
|-------|-------------|
| Network Types | HMO, PPO, EPO, POS structures |
| Adequacy Standards | Access requirements, provider ratios |
| Taxonomy Codes | Healthcare Provider Taxonomy Code System |
| Credentialing | Provider verification and enrollment |

## Skills Reference

- **[SKILL.md](SKILL.md)** - Complete skill reference with all query and generation parameters
- **[Examples](../../hello-healthsim/examples/networksim-examples.md)** - Detailed examples

## Related Documentation

- [Data Architecture](../../docs/data-architecture.md) - Database schema details
- [Architecture Guide](../../docs/HEALTHSIM-ARCHITECTURE-GUIDE.md) - System overview
- [Code Systems](../../references/code-systems.md) - Taxonomy codes reference

---

*NetworkSim provides access to 8.9 million real US healthcare providers for queries and validation, plus synthetic generation when real data isn't appropriate.*
