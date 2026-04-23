# NetworkSim Data Package

**Version**: 2.0  
**Last Updated**: December 28, 2025  
**Location**: `healthsim.duckdb` (network schema)

---

## Overview

NetworkSim v2.0 is a data-driven network analytics product built on real healthcare provider data. Unlike v1.0's synthetic generation, v2.0 queries actual NPPES, CMS, and HRSA datasets for authentic provider lookups, network analysis, and cross-product analytics.

**Key Feature**: Geographic enrichment enables cross-schema JOINs with PopulationSim demographic data for healthcare access analysis.

---

## Database Schema: `network`

### Tables Summary

| Table | Records | Description |
|-------|---------|-------------|
| **providers** | 8.9M | Active US healthcare providers (NPPES) |
| **facilities** | 77K | Hospitals and healthcare facilities (CMS POS) |
| **hospital_quality** | 5.4K | Hospital quality ratings (CMS Hospital Compare) |
| **physician_quality** | 1.5M | Physician performance metrics (CMS Physician Compare) |
| **ahrf_county** | 3.2K | County-level workforce data (HRSA AHRF) |

**Total Size**: ~1.2 GB  
**Geographic Coverage**: 97.77% of providers have county FIPS codes  
**Counties Covered**: 3,213 (exceeds PopulationSim's 3,143)

---

## Table Schemas

### `network.providers` (8,925,672 records)

Primary table containing all active US healthcare providers from NPPES.

| Column | Type | Description |
|--------|------|-------------|
| npi | VARCHAR | 10-digit National Provider Identifier (PRIMARY KEY) |
| entity_type_code | VARCHAR | '1' = Individual, '2' = Organization |
| first_name, last_name | VARCHAR | Individual provider names |
| organization_name | VARCHAR | Organization legal name |
| credential | VARCHAR | Credentials (MD, DO, RN, etc.) |
| gender | VARCHAR | Gender code |
| practice_address_1 | VARCHAR | Street address |
| practice_city | VARCHAR | City |
| practice_state | VARCHAR | State (2-letter) |
| practice_zip | VARCHAR | ZIP code |
| taxonomy_1 - taxonomy_4 | VARCHAR | Healthcare provider taxonomy codes |
| county_fips | VARCHAR | **5-digit county FIPS** (enables PopulationSim JOINs) |
| phone | VARCHAR | Practice phone number |
| enumeration_date | DATE | NPI assignment date |
| last_update_date | DATE | Last NPPES update |
| created_at | TIMESTAMP | Import timestamp |

**Geographic Enrichment**: 97.77% of providers have county FIPS codes assigned via ZIP→County crosswalk.

**Indexes**: PRIMARY KEY on `npi`, INDEX on `practice_state`, `county_fips`, `taxonomy_1`

---

### `network.facilities` (77,302 records)

Healthcare facilities from CMS Provider of Services file.

| Column | Type | Description |
|--------|------|-------------|
| ccn | VARCHAR | CMS Certification Number (PRIMARY KEY) |
| facility_name | VARCHAR | Facility name |
| city | VARCHAR | City |
| state | VARCHAR | State |
| zip | VARCHAR | ZIP code |
| county_fips | VARCHAR | County FIPS code |
| type | VARCHAR | Facility type (Hospital, SNF, etc.) |
| subtype | VARCHAR | Facility subtype |
| beds | INTEGER | Licensed bed count |
| phone | VARCHAR | Contact phone |
| created_at | TIMESTAMP | Import timestamp |

---

### `network.hospital_quality` (5,421 records)

Hospital quality ratings from CMS Hospital Compare.

| Column | Type | Description |
|--------|------|-------------|
| facility_id | VARCHAR | CMS facility identifier (PRIMARY KEY) |
| facility_name | VARCHAR | Hospital name |
| city_town | VARCHAR | City |
| state | VARCHAR | State |
| hospital_overall_rating | VARCHAR | 1-5 star rating |
| hospital_overall_rating_footnote | VARCHAR | Rating notes |
| mortality_national_comparison | VARCHAR | Mortality vs national |
| readmission_national_comparison | VARCHAR | Readmission vs national |
| created_at | TIMESTAMP | Import timestamp |

---

### `network.physician_quality` (1,478,309 records)

Physician performance metrics from CMS Physician Compare.

| Column | Type | Description |
|--------|------|-------------|
| npi | VARCHAR | National Provider Identifier (PRIMARY KEY) |
| last_name | VARCHAR | Last name |
| first_name | VARCHAR | First name |
| credential | VARCHAR | Credentials |
| medical_school | VARCHAR | Medical school name |
| graduation_year | INTEGER | Graduation year |
| primary_specialty | VARCHAR | Primary specialty |
| hospital_affiliations | INTEGER | Number of hospital affiliations |
| created_at | TIMESTAMP | Import timestamp |

**Foreign Key**: `npi` → `network.providers.npi`

---

### `network.ahrf_county` (3,235 records)

Area Health Resources File county-level workforce data from HRSA.

| Column | Type | Description |
|--------|------|-------------|
| county_fips | VARCHAR | 5-digit county FIPS (PRIMARY KEY) |
| county_name | VARCHAR | County name |
| state | VARCHAR | State abbreviation |
| total_population | INTEGER | Total population |
| primary_care_phys | INTEGER | Number of primary care physicians |
| pcp_per_100k | DECIMAL | PCPs per 100K population |
| specialists | INTEGER | Number of specialists |
| hospital_beds | INTEGER | Hospital beds |
| hpsa_primary_care | BOOLEAN | Health Professional Shortage Area status |
| created_at | TIMESTAMP | Import timestamp |

---

## Cross-Schema Integration

### Join Keys with PopulationSim

| NetworkSim Column | PopulationSim Table | Join Column |
|-------------------|---------------------|-------------|
| county_fips | population.svi_county | stcnty |
| county_fips | population.places_county | locationid |
| county_fips | population.svi_tract | (first 5 digits of FIPS) |

### Example Cross-Product Queries

**Healthcare Access + Social Vulnerability**:
```sql
SELECT 
    s.county,
    s.state,
    s.rpl_themes as svi_percentile,
    COUNT(DISTINCT p.npi) as provider_count,
    s.e_totpop as population,
    ROUND(COUNT(DISTINCT p.npi) * 100000.0 / s.e_totpop, 1) as per_100k
FROM population.svi_county s
LEFT JOIN network.providers p ON s.stcnty = p.county_fips
WHERE s.rpl_themes >= 0.75  -- Top quartile vulnerability
GROUP BY s.county, s.state, s.rpl_themes, s.e_totpop
ORDER BY per_100k ASC;
```

**Healthcare Deserts + Disease Burden**:
```sql
SELECT 
    s.county,
    COUNT(p.npi) * 100000.0 / s.e_totpop as providers_per_100k,
    pl.diabetes_crudeprev as diabetes_rate,
    s.rpl_themes as vulnerability
FROM population.svi_county s
LEFT JOIN network.providers p ON s.stcnty = p.county_fips
LEFT JOIN population.places_county pl ON s.stcnty = pl.locationid
GROUP BY s.county, s.e_totpop, pl.diabetes_crudeprev, s.rpl_themes
HAVING COUNT(p.npi) * 100000.0 / s.e_totpop < 40
ORDER BY diabetes_rate DESC;
```

---

## Data Sources

| Data | Source | Update Frequency | URL |
|------|--------|------------------|-----|
| NPPES Provider Registry | CMS | Monthly | [npiregistry.cms.hhs.gov](https://npiregistry.cms.hhs.gov/) |
| Provider of Services | CMS | Quarterly | [data.cms.gov](https://data.cms.gov/) |
| Hospital Compare | CMS | Quarterly | [data.cms.gov](https://data.cms.gov/) |
| Physician Compare | CMS | Quarterly | [data.cms.gov](https://data.cms.gov/) |
| AHRF County Data | HRSA | Annual | [data.hrsa.gov](https://data.hrsa.gov/) |
| ZIP→County Crosswalk | HUD | Quarterly | [huduser.gov](https://www.huduser.gov/portal/datasets/usps_crosswalk.html) |

---

## Data Quality

### Validation Tests

| Test | Result | Notes |
|------|--------|-------|
| Provider count | 8,925,672 | All active US providers |
| NPI format | 100% valid | 10 digits, Luhn checksum |
| Duplicate NPIs | 0 | Unique constraint enforced |
| County FIPS coverage | 97.77% | Exceeds 95% target |
| County FIPS format | 100% valid | 5 digits |
| Facility count | 77,302 | CMS-certified only |
| Hospital quality | 5,421 | With star ratings |

### Test Suite

```bash
cd /path/to/healthsim-workspace
pytest cohorts/networksim/tests/test_data_quality.py -v
```

---

## Refresh Procedures

### Monthly NPPES Refresh

1. Download from CMS (first Sunday of month)
2. Run `scripts/filter_nppes.py` to filter US active providers
3. Run `scripts/enrich_geography.py` for county FIPS assignment
4. Run test suite for validation
5. Import to `network.providers`

### Quarterly CMS Updates

1. Download updated POS, Hospital Compare, Physician Compare
2. Process with dedicated import scripts
3. Validate data quality
4. Import to respective tables

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0 | Dec 2025 | Real NPPES data, geographic enrichment, cross-product integration |
| 1.0 | 2024 | Synthetic generation only (archived) |

---

## Related Documentation

- [DuckDB Schema](../../../docs/healthsim-duckdb-schema.md) - Full database schema
- [DuckDB Architecture](../../../docs/healthsim-duckdb-architecture.html) - Database design
- [Query Skills](../query/README.md) - Provider search skills
- [Analytics Skills](../analytics/README.md) - Adequacy and desert analysis
- [PopulationSim Data](../../populationsim/data-access/README.md) - Demographics data

---

*NetworkSim uses real NPPES registry data - every NPI is an actual registered provider.*
