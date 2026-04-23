---
name: provider-search
description: Search for healthcare providers by specialty, location, and credentials using real NPPES data

Trigger phrases:
- "Find providers in [location]"
- "Search for [specialty] providers"
- "Locate providers near [ZIP code]"
- "Find NPIs for [specialty]"
- "Show me doctors in [county]"
- "List healthcare providers in [state]"
---

# Provider Search Skill

## Overview

Searches the NPPES provider database for individual practitioners and organizational providers based on specialty, geography, and other criteria. Uses real CMS National Provider Identifier (NPI) Registry data with 8.9M active US providers.

**Data Source**: `network.providers` table (97.77% with county FIPS codes)

---

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| specialty | string | No | Provider specialty or taxonomy code |
| location | object | No | Geographic search criteria |
| location.state | string | No | Two-letter state code (e.g., 'CA', 'TX') |
| location.county_fips | string | No | 5-digit county FIPS code |
| location.zip_code | string | No | ZIP code (5 or 9 digits) |
| location.city | string | No | City name |
| entity_type | string | No | '1'=Individual, '2'=Organization |
| credential | string | No | Provider credential (MD, DO, RN, etc.) |
| gender | string | No | Gender code (M, F) |
| limit | integer | No | Max results (default: 50, max: 1000) |

---

## Query Patterns

### Pattern 1: Basic Specialty Search

Search for providers by taxonomy code (specialty).

```sql
-- Find all family medicine physicians (207Q00000X)
SELECT 
    p.npi,
    p.first_name || ' ' || p.last_name AS provider_name,
    p.credential,
    p.taxonomy_1 AS primary_specialty,
    p.practice_city || ', ' || p.practice_state AS location,
    p.phone
FROM network.providers p
WHERE p.taxonomy_1 = '207Q00000X'  -- Family Medicine
  AND p.entity_type_code = '1'     -- Individual providers
LIMIT 50;
```

### Pattern 2: Geographic + Specialty Search

Combine location and specialty criteria.

```sql
-- Find cardiologists in Los Angeles County
SELECT 
    p.npi,
    CASE 
        WHEN p.entity_type_code = '1' 
        THEN p.first_name || ' ' || p.last_name || 
             COALESCE(', ' || p.credential, '')
        ELSE p.organization_name
    END AS provider_name,
    p.taxonomy_1 AS primary_specialty,
    p.practice_address_1,
    p.practice_city || ', ' || p.practice_state || ' ' || p.practice_zip AS address,
    p.phone
FROM network.providers p
WHERE p.county_fips = '06037'  -- Los Angeles County
  AND p.taxonomy_1 LIKE '207R%'  -- Cardiology taxonomy prefix
ORDER BY p.last_name, p.first_name
LIMIT 100;
```

### Pattern 3: Multi-Criteria Search

Search by state, credential, and gender.

```sql
-- Find female physicians with MD credential in California
SELECT 
    p.npi,
    p.first_name || ' ' || p.last_name AS provider_name,
    p.credential,
    p.practice_city,
    p.practice_zip,
    p.taxonomy_1
FROM network.providers p
WHERE p.practice_state = 'CA'
  AND p.credential = 'M.D.'
  AND p.gender = 'F'
  AND p.entity_type_code = '1'
ORDER BY p.practice_city, p.last_name
LIMIT 200;
```

### Pattern 4: Cross-Product - Providers in High-Need Areas

Identify providers in counties with high disease prevalence and social vulnerability.

```sql
-- Find providers in high-diabetes, high-vulnerability counties
SELECT 
    pc.countyname,
    pc.stateabbr,
    pc.diabetes_crudeprev AS diabetes_rate,
    sv.rpl_themes AS vulnerability_index,
    COUNT(DISTINCT p.npi) AS provider_count,
    COUNT(DISTINCT CASE WHEN p.taxonomy_1 LIKE '207%' THEN p.npi END) AS physicians,
    COUNT(DISTINCT CASE WHEN p.taxonomy_1 LIKE '163W%' THEN p.npi END) AS nurses
FROM population.places_county pc
JOIN population.svi_county sv ON pc.countyfips = sv.stcnty
LEFT JOIN network.providers p ON pc.countyfips = p.county_fips
WHERE pc.diabetes_crudeprev > 12.0  -- High diabetes prevalence (>12%)
  AND sv.rpl_themes > 0.75          -- Top quartile social vulnerability
  AND p.entity_type_code = '1'
GROUP BY pc.countyname, pc.stateabbr, pc.diabetes_crudeprev, sv.rpl_themes
HAVING COUNT(DISTINCT p.npi) < 100  -- Provider shortage
ORDER BY provider_count ASC, diabetes_rate DESC
LIMIT 20;
```

### Pattern 5: Organization Search

Search for healthcare organizations instead of individuals.

```sql
-- Find hospitals and medical centers in Texas
SELECT 
    p.npi,
    p.organization_name,
    p.practice_city,
    p.practice_state,
    p.practice_zip,
    p.taxonomy_1,
    p.phone
FROM network.providers p
WHERE p.entity_type_code = '2'  -- Organizations
  AND p.practice_state = 'TX'
  AND (p.organization_name ILIKE '%hospital%' 
       OR p.organization_name ILIKE '%medical center%')
ORDER BY p.practice_city, p.organization_name
LIMIT 100;
```

---

## Examples

### Example 1: Find Primary Care Physicians in Harris County, TX

**Request**: "Find primary care physicians in Harris County, Texas"

**Parameters**:
- Location: Harris County, TX (FIPS: 48201)
- Specialty: Primary Care (taxonomy codes 207Q*, 208D*, 207R*)
- Entity Type: Individual

**Query**:
```sql
SELECT 
    p.npi,
    p.first_name || ' ' || p.last_name || 
    COALESCE(', ' || p.credential, '') AS provider_name,
    p.practice_address_1 AS address,
    p.practice_city,
    p.practice_zip,
    p.taxonomy_1 AS specialty_code,
    p.phone
FROM network.providers p
WHERE p.county_fips = '48201'  -- Harris County, TX
  AND (p.taxonomy_1 LIKE '207Q%'  -- Family Medicine
       OR p.taxonomy_1 LIKE '208D%'  -- General Practice
       OR p.taxonomy_1 LIKE '207R%')  -- Internal Medicine
  AND p.entity_type_code = '1'
ORDER BY p.last_name, p.first_name
LIMIT 50;
```

**Expected Output**: ~50 PCPs with name, location, specialty code

**Sample Result**:
```
npi         | provider_name           | address              | city    | zip   | specialty_code | phone
------------|-------------------------|----------------------|---------|-------|----------------|---------------
1234567890  | John Smith, MD          | 123 Main St          | Houston | 77001 | 207Q00000X     | 713-555-0100
2345678901  | Maria Garcia, DO        | 456 Oak Ave          | Houston | 77002 | 208D00000X     | 713-555-0200
```

### Example 2: Find Cardiologists Near ZIP Code 90210

**Request**: "Find cardiologists near Beverly Hills (90210)"

**Parameters**:
- Location: ZIP 90210
- Specialty: Cardiology (207RC*)
- Radius: Same county

**Query**:
```sql
-- First, get county FIPS for ZIP 90210
WITH zip_county AS (
    SELECT DISTINCT county_fips 
    FROM network.providers 
    WHERE practice_zip LIKE '90210%'
    LIMIT 1
)
SELECT 
    p.npi,
    p.first_name || ' ' || p.last_name || ', ' || p.credential AS provider_name,
    p.practice_address_1,
    p.practice_city,
    p.practice_zip,
    p.phone
FROM network.providers p
WHERE p.county_fips = (SELECT county_fips FROM zip_county)
  AND p.taxonomy_1 LIKE '207RC%'  -- Cardiovascular Disease
  AND p.entity_type_code = '1'
ORDER BY p.practice_zip, p.last_name
LIMIT 25;
```

**Expected Output**: Cardiologists in Los Angeles County near 90210

### Example 3: Healthcare Desert Analysis

**Request**: "Find counties with high diabetes but few providers"

**Parameters**:
- Diabetes rate: >12%
- Provider density: <50 per 100K population
- Cross-reference with PopulationSim

**Query**:
```sql
SELECT 
    pc.countyname AS county,
    pc.stateabbr AS state,
    pc.diabetes_crudeprev AS diabetes_pct,
    sv.e_totpop AS population,
    COUNT(p.npi) AS total_providers,
    ROUND(100000.0 * COUNT(p.npi) / NULLIF(sv.e_totpop, 0), 1) AS providers_per_100k
FROM population.places_county pc
JOIN population.svi_county sv ON pc.countyfips = sv.stcnty
LEFT JOIN network.providers p ON pc.countyfips = p.county_fips
WHERE pc.diabetes_crudeprev > 12.0
  AND sv.e_totpop > 10000  -- Exclude very small counties
GROUP BY pc.countyname, pc.stateabbr, pc.diabetes_crudeprev, sv.e_totpop
HAVING ROUND(100000.0 * COUNT(p.npi) / NULLIF(sv.e_totpop, 0), 1) < 50
ORDER BY diabetes_pct DESC, providers_per_100k ASC
LIMIT 20;
```

**Expected Output**: Counties with provider shortages and high diabetes burden

---

## Common Taxonomy Codes

| Code | Specialty |
|------|-----------|
| 207Q00000X | Family Medicine |
| 207R00000X | Internal Medicine |
| 208D00000X | General Practice |
| 207RC0000X | Cardiovascular Disease (Cardiology) |
| 207RE0101X | Endocrinology, Diabetes & Metabolism |
| 207RG0100X | Gastroenterology |
| 207RN0300X | Nephrology |
| 163W00000X | Registered Nurse |
| 364S00000X | Clinical Nurse Specialist |
| 367500000X | Nurse Anesthetist |

**Note**: Full taxonomy reference available at [NUCC Website](https://www.nucc.org/index.php/code-sets-mainmenu-41/provider-taxonomy-mainmenu-40)

---

## Validation Rules

### Input Validation
- NPIs must be exactly 10 digits
- State codes must be valid 2-letter abbreviations (use `practice_state`)
- County FIPS must be 5 digits
- Entity type must be '1' or '2'
- Limit must be between 1 and 1000
- ZIP codes must be 5 or 9 digits

### Output Validation
- All returned NPIs should exist in NPPES registry
- Geographic coordinates should be within valid ranges
- Phone numbers should be in valid format

---

## Performance Notes

- **Provider count queries**: <100ms
- **Geographic + specialty searches**: 200-500ms
- **Cross-product analytics**: 500ms-1s
- **Indexes available**: `npi` (PRIMARY KEY), `practice_state`, `county_fips`, `taxonomy_1`

**Optimization Tips**:
- Use county_fips instead of city names for better performance
- Filter by entity_type_code early in WHERE clause
- Use taxonomy_1 for primary specialty (most providers have this populated)
- LIMIT results appropriately for large datasets

---

## Related Skills

- **facility-search**: Find facilities instead of individual providers
- **pharmacy-search**: Search for retail pharmacies specifically
- **npi-validation**: Validate NPI format and existence
- **provider-density**: Analyze provider distribution by geography
- **network-roster**: Generate provider rosters from search results

---

## Data Quality Notes

**County FIPS Coverage**: 97.77% of providers have county FIPS assigned
- **Missing FIPS**: Primarily military addresses (APO, FPO) and PO Box-only addresses
- **Workaround**: Use `practice_state` and `practice_city` for providers without county_fips

**Taxonomy Codes**:
- `taxonomy_1`: Primary specialty (99%+ populated)
- `taxonomy_2-4`: Additional specialties (varies by provider)
- No taxonomy description table yet - use external reference or add lookup table

**Entity Types**:
- Type 1 (Individual): 85% of providers
- Type 2 (Organization): 15% of providers

---

## Future Enhancements

1. **Add taxonomy_codes reference table** for human-readable specialty names
2. **Geospatial queries** using PostGIS or DuckDB spatial extensions
3. **Distance calculations** for radius-based searches
4. **Provider quality scores** integration with physician_quality table
5. **Network adequacy** calculations with time/distance standards
