# Reference Data Integration Guide

HealthSim integrates real-world reference data from PopulationSim (CDC demographics) and NetworkSim (NPPES providers/facilities) to create realistic synthetic healthcare data.

## Overview

Reference data provides:
- **PopulationSim**: Real demographic distributions from CDC PLACES and SVI datasets
- **NetworkSim**: Real provider/facility data from NPPES, CMS, and HRSA

This enables generating synthetic patients that match real-world population health characteristics and can be assigned to real providers and facilities.

## Database Architecture

All reference data is stored in `healthsim.duckdb` with schema organization:

| Schema | Tables | Source |
|--------|--------|--------|
| `population` | places_county, places_tract, svi_county, svi_tract, adi_blockgroup | CDC, Census |
| `network` | providers, facilities, hospital_quality, physician_quality, ahrf_county | NPPES, CMS |
| `main` | Generated entities (patients, members, etc.) | HealthSim |

## Quick Start

### Basic Demographics Lookup

```python
import duckdb
from healthsim.generation.reference_profiles import ReferenceProfileResolver

conn = duckdb.connect("healthsim.duckdb", read_only=True)
resolver = ReferenceProfileResolver(conn)

# Get Harris County, TX demographics
profile = resolver.resolve_county("48201")
print(f"Population: {profile.population:,}")
print(f"Diabetes rate: {profile.pct_diabetes:.1f}%")
print(f"Obesity rate: {profile.pct_obesity:.1f}%")
print(f"65+ population: {profile.pct_age_65_plus:.1f}%")
```

### Provider Lookup

```python
from healthsim.generation.networksim_reference import NetworkSimResolver

resolver = NetworkSimResolver(conn)

# Find Texas cardiologists
cardiologists = resolver.find_providers(
    state="TX",
    taxonomy="207RC0000X",  # Cardiology
    limit=10
)
for p in cardiologists:
    print(f"{p.display_name} - {p.practice_city}, {p.practice_state}")
```

### Facility Lookup

```python
# Find large Texas hospitals
hospitals = resolver.find_facilities(
    state="TX",
    facility_type="hospital",
    min_beds=200,
    limit=10
)
for f in hospitals:
    print(f"{f.name} - {f.beds} beds")
```

## Hybrid Profiles

Hybrid profiles combine user specifications with reference data:

### Demographics from PopulationSim

```python
from healthsim.generation.reference_profiles import create_hybrid_profile

spec = {
    "profile": {
        "id": "harris-diabetic",
        "generation": {"count": 200},
        "demographics": {
            "source": "populationsim",
            "reference": {"type": "county", "fips": "48201"},
            # Override age for elderly focus
            "age": {"type": "normal", "mean": 72, "std_dev": 8, "min": 65}
        },
        "clinical": {
            "primary_condition": {"code": "E11", "prevalence": 1.0}
        }
    }
}

hybrid = create_hybrid_profile(spec, conn)
# Gender, race, SES from Harris County; age overridden; clinical from user
```

### Full Integration with NetworkSim

```python
from healthsim.generation.reference_profiles import create_hybrid_profile_with_network

spec = {
    "profile": {
        "id": "comprehensive-diabetic",
        "demographics": {
            "source": "populationsim",
            "reference": {"type": "county", "fips": "48201"}
        },
        "providers": {
            "source": "networksim",
            "reference": {"state": "TX", "specialty": "endocrinology"},
            "assignment": "pcp"
        },
        "facilities": {
            "source": "networksim",
            "reference": {"state": "TX", "type": "hospital", "min_beds": 200},
            "assignment": "primary"
        }
    }
}

hybrid = create_hybrid_profile_with_network(spec, conn)

# Access resolved data
print(f"Provider pool: {hybrid['profile']['_providers']['count']} endocrinologists")
print(f"Facility pool: {hybrid['profile']['_facilities']['count']} hospitals")
```

## Available Reference Data

### PopulationSim Demographics

| Metric | Field | Source |
|--------|-------|--------|
| Population | `population` | SVI |
| Age 65+ | `pct_age_65_plus` | SVI |
| Age <17 | `pct_age_under_17` | SVI |
| Minority | `pct_minority` | SVI |
| Hispanic | `pct_hispanic` | SVI |
| Poverty | `pct_poverty` | SVI |
| Uninsured | `pct_uninsured` | SVI |
| Diabetes | `pct_diabetes` | PLACES |
| Obesity | `pct_obesity` | PLACES |
| Hypertension | `pct_hypertension` | PLACES |
| Heart Disease | `pct_heart_disease` | PLACES |
| COPD | `pct_copd` | PLACES |
| Asthma | `pct_asthma` | PLACES |
| Depression | `pct_depression` | PLACES |
| Cancer | `pct_cancer` | PLACES |

### NetworkSim Providers

| Field | Description |
|-------|-------------|
| `npi` | 10-digit National Provider Identifier |
| `entity_type` | "1" (individual) or "2" (organization) |
| `display_name` | Formatted provider name |
| `practice_state` | 2-letter state code |
| `practice_city` | City name |
| `practice_zip` | 5 or 9 digit ZIP |
| `primary_taxonomy` | Healthcare Provider Taxonomy Code |

### Common Specialty Codes

| Specialty | Taxonomy Code |
|-----------|---------------|
| Internal Medicine | 207R00000X |
| Family Medicine | 207Q00000X |
| Cardiology | 207RC0000X |
| Endocrinology | 207RE0101X |
| Nephrology | 207RN0300X |
| Pulmonology | 207RP1001X |
| Pediatrics | 208000000X |
| Nurse Practitioner | 363L00000X |
| Physician Assistant | 363A00000X |

### NetworkSim Facilities

| Field | Description |
|-------|-------------|
| `ccn` | 6-character CMS Certification Number |
| `name` | Facility name |
| `facility_type` | hospital, snf, hha, hospice, fqhc, rhc, asc |
| `state` | 2-letter state code |
| `city` | City name |
| `beds` | Number of beds (hospitals) |

## Best Practices

1. **Always use schema-qualified table names** when querying directly:
   ```sql
   SELECT * FROM population.places_county WHERE stateabbr = 'TX'
   SELECT * FROM network.providers WHERE provider_state = 'TX'
   ```

2. **Use read-only connections** for reference data:
   ```python
   conn = duckdb.connect("healthsim.duckdb", read_only=True)
   ```

3. **Sample from provider pools** rather than using all results:
   ```python
   import random
   providers = resolver.find_providers(state="TX", limit=100)
   assigned = random.choice(providers)
   ```

4. **Cache resolver instances** for multiple lookups:
   ```python
   resolver = ReferenceProfileResolver(conn)
   # Reuse for multiple resolve_* calls
   ```

## See Also

- [Data Architecture](../data-architecture.md) - Full database schema documentation
- [Skill Integration Guide](skill-integration.md) - Using skills with generation
- [Profile Schema](../api/profile-schema.md) - Profile specification format
