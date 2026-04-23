---
name: pharmacy-search
description: Search for retail and specialty pharmacies using NPPES provider data with pharmacy taxonomy codes

Trigger phrases:
- "Find pharmacies in [location]"
- "Search for retail pharmacies near [ZIP]"
- "Locate pharmacies in [county]"
- "Show me specialty pharmacies in [state]"
- "Find mail-order pharmacies"
---

# Pharmacy Search Skill

## Overview

Searches for retail, specialty, and mail-order pharmacies using NPPES provider data. Pharmacies are identified by taxonomy codes starting with '332' (Pharmacy Service Providers). Supports geographic filtering and pharmacy type classification.

**Data Source**: `network.providers` table (subset with pharmacy taxonomy codes)  
**Pharmacy Taxonomies**: 332* (all pharmacy types)

---

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| pharmacy_type | string | No | Type of pharmacy (retail, specialty, mail-order) |
| location | object | No | Geographic search criteria |
| location.state | string | No | Two-letter state code |
| location.county_fips | string | No | 5-digit county FIPS code |
| location.zip_code | string | No | ZIP code (5 or 9 digits) |
| location.city | string | No | City name |
| specialty | string | No | Pharmacy specialty (oncology, compounding, etc.) |
| limit | integer | No | Max results (default: 50, max: 1000) |

---

## Pharmacy Taxonomy Codes

| Code | Description |
|------|-------------|
| 3336C0003X | Community/Retail Pharmacy |
| 3336C0004X | Clinic Pharmacy |
| 333600000X | Pharmacy (general) |
| 3336I0012X | Institutional Pharmacy |
| 3336L0003X | Long Term Care Pharmacy |
| 3336M0002X | Mail Order Pharmacy |
| 3336N0007X | Nuclear Pharmacy |
| 3336S0011X | Specialty Pharmacy |
| 3336C0002X | Compounding Pharmacy |

**Full Reference**: [NUCC Taxonomy - Pharmacy Service Providers](https://www.nucc.org/index.php/code-sets-mainmenu-41/provider-taxonomy-mainmenu-40)

---

## Query Patterns

### Pattern 1: Basic Pharmacy Search by Location

Find all pharmacies in a specific state or county.

```sql
-- Find all pharmacies in Harris County, Texas
SELECT 
    p.npi,
    p.organization_name AS pharmacy_name,
    p.practice_address_1 AS address,
    p.practice_city AS city,
    p.practice_state AS state,
    p.practice_zip AS zip,
    p.taxonomy_1 AS pharmacy_type_code,
    p.phone
FROM network.providers p
WHERE p.county_fips = '48201'  -- Harris County, TX
  AND p.taxonomy_1 LIKE '332%'  -- Pharmacy taxonomy prefix
  AND p.entity_type_code = '2'  -- Organizations
ORDER BY p.practice_city, p.organization_name
LIMIT 100;
```

### Pattern 2: Search by Pharmacy Type

Search for specific pharmacy types (retail, specialty, mail-order).

```sql
-- Find specialty pharmacies in California
SELECT 
    p.npi,
    p.organization_name,
    p.taxonomy_1,
    p.practice_city,
    p.practice_state,
    p.practice_zip,
    p.phone
FROM network.providers p
WHERE p.practice_state = 'CA'
  AND p.taxonomy_1 = '3336S0011X'  -- Specialty Pharmacy
  AND p.entity_type_code = '2'
ORDER BY p.practice_city, p.organization_name
LIMIT 50;
```

### Pattern 3: Multi-Taxonomy Search

Search across multiple pharmacy types.

```sql
-- Find retail and community pharmacies in New York City
SELECT 
    p.npi,
    p.organization_name,
    p.practice_address_1,
    p.practice_city,
    p.practice_zip,
    CASE 
        WHEN p.taxonomy_1 = '3336C0003X' THEN 'Community/Retail'
        WHEN p.taxonomy_1 = '3336C0004X' THEN 'Clinic'
        ELSE 'Other Pharmacy'
    END AS pharmacy_type,
    p.phone
FROM network.providers p
WHERE p.practice_city IN ('New York', 'Brooklyn', 'Queens', 'Bronx', 'Staten Island')
  AND p.practice_state = 'NY'
  AND p.taxonomy_1 IN ('3336C0003X', '3336C0004X')  -- Community or Clinic pharmacy
ORDER BY p.practice_city, p.organization_name
LIMIT 100;
```

### Pattern 4: Pharmacy Density Analysis

Analyze pharmacy coverage by geography.

```sql
-- Calculate pharmacy density per 100K population by county
SELECT 
    sv.county,
    sv.state,
    sv.e_totpop AS population,
    COUNT(p.npi) AS pharmacy_count,
    ROUND(100000.0 * COUNT(p.npi) / NULLIF(sv.e_totpop, 0), 2) AS pharmacies_per_100k
FROM population.svi_county sv
LEFT JOIN network.providers p ON sv.stcnty = p.county_fips
WHERE p.taxonomy_1 LIKE '332%'
  AND sv.e_totpop > 10000  -- Exclude very small counties
GROUP BY sv.county, sv.state, sv.e_totpop
HAVING COUNT(p.npi) > 0
ORDER BY pharmacies_per_100k DESC
LIMIT 50;
```

### Pattern 5: Pharmacy Deserts

Identify areas with limited pharmacy access.

```sql
-- Find high-population counties with few pharmacies
SELECT 
    sv.county,
    sv.state,
    sv.e_totpop AS population,
    COUNT(p.npi) AS pharmacy_count,
    ROUND(100000.0 * COUNT(p.npi) / NULLIF(sv.e_totpop, 0), 2) AS pharmacies_per_100k,
    sv.rpl_themes AS vulnerability_index
FROM population.svi_county sv
LEFT JOIN network.providers p ON sv.stcnty = p.county_fips 
    AND p.taxonomy_1 LIKE '332%'
WHERE sv.e_totpop > 50000  -- Significant population
GROUP BY sv.county, sv.state, sv.e_totpop, sv.rpl_themes
HAVING ROUND(100000.0 * COUNT(p.npi) / NULLIF(sv.e_totpop, 0), 2) < 10  -- Low pharmacy density
ORDER BY population DESC, pharmacies_per_100k ASC
LIMIT 20;
```

---

## Examples

### Example 1: Find Retail Pharmacies Near ZIP Code 60601

**Request**: "Find retail pharmacies near downtown Chicago (60601)"

**Parameters**:
- ZIP Code: 60601
- Pharmacy Type: Community/Retail (3336C0003X)
- Radius: Same county

**Query**:
```sql
-- Get pharmacies in the same county as ZIP 60601
WITH zip_county AS (
    SELECT DISTINCT county_fips 
    FROM network.providers 
    WHERE practice_zip LIKE '60601%'
    LIMIT 1
)
SELECT 
    p.npi,
    p.organization_name AS pharmacy_name,
    p.practice_address_1,
    p.practice_city,
    p.practice_zip,
    p.phone
FROM network.providers p
WHERE p.county_fips = (SELECT county_fips FROM zip_county)
  AND p.taxonomy_1 = '3336C0003X'  -- Community/Retail Pharmacy
  AND p.entity_type_code = '2'
ORDER BY p.practice_zip, p.organization_name
LIMIT 25;
```

**Expected Output**: Retail pharmacies in Cook County, IL near downtown

**Sample Result**:
```
npi        | pharmacy_name           | practice_address_1  | city    | zip   | phone
-----------|-------------------------|---------------------|---------|-------|---------------
1234567890 | Walgreens #12345        | 123 Michigan Ave    | Chicago | 60601 | 312-555-0100
2345678901 | CVS Pharmacy #5678      | 456 State St        | Chicago | 60602 | 312-555-0200
```

### Example 2: Find Specialty Pharmacies in Los Angeles County

**Request**: "Find specialty pharmacies that handle oncology medications in LA County"

**Parameters**:
- Location: Los Angeles County (FIPS: 06037)
- Pharmacy Type: Specialty (3336S0011X)

**Query**:
```sql
SELECT 
    p.npi,
    p.organization_name,
    p.practice_address_1,
    p.practice_city,
    p.practice_zip,
    p.phone,
    p.taxonomy_1,
    p.taxonomy_2,
    p.taxonomy_3
FROM network.providers p
WHERE p.county_fips = '06037'  -- Los Angeles County
  AND (p.taxonomy_1 = '3336S0011X'  -- Specialty Pharmacy
       OR p.taxonomy_2 = '3336S0011X'
       OR p.taxonomy_3 = '3336S0011X')
  AND p.entity_type_code = '2'
ORDER BY p.practice_city, p.organization_name
LIMIT 50;
```

**Expected Output**: Specialty pharmacies in Los Angeles County

### Example 3: Mail-Order Pharmacy Analysis

**Request**: "How many mail-order pharmacies are there per state?"

**Query**:
```sql
SELECT 
    p.practice_state AS state,
    COUNT(p.npi) AS mail_order_pharmacies,
    STRING_AGG(DISTINCT p.organization_name, '; ' ORDER BY p.organization_name) AS pharmacy_names
FROM network.providers p
WHERE p.taxonomy_1 = '3336M0002X'  -- Mail Order Pharmacy
  OR p.taxonomy_2 = '3336M0002X'
  OR p.taxonomy_3 = '3336M0002X'
GROUP BY p.practice_state
ORDER BY mail_order_pharmacies DESC, state
LIMIT 50;
```

**Expected Output**: State-level distribution of mail-order pharmacies

---

## Integration with RxMemberSim

Pharmacy search integrates with RxMemberSim for prescription fill analysis:

```sql
-- Cross-product: Match prescription fills to nearest pharmacy
-- (Conceptual example - requires RxMemberSim data)
SELECT 
    rx.member_id,
    rx.fill_date,
    rx.ndc,
    rx.fill_zip AS member_zip,
    p.npi AS pharmacy_npi,
    p.organization_name AS pharmacy_name,
    p.practice_zip AS pharmacy_zip
FROM rxmembersim.prescriptions rx
JOIN network.providers p 
    ON SUBSTRING(rx.fill_zip, 1, 3) = SUBSTRING(p.practice_zip, 1, 3)
    AND p.taxonomy_1 LIKE '332%'
WHERE rx.fill_date >= '2024-01-01'
LIMIT 100;
```

---

## Validation Rules

### Input Validation
- NPIs must be exactly 10 digits
- State codes must be valid 2-letter abbreviations
- County FIPS must be 5 digits
- Taxonomy codes must start with '332'
- Entity type should be '2' (organizations) for pharmacies
- Limit must be between 1 and 1000

### Output Validation
- All pharmacies should have organization_name (not individual names)
- Taxonomy codes should be valid NUCC pharmacy codes
- Geographic coordinates should be valid

---

## Performance Notes

- **Pharmacy count queries**: <100ms
- **Geographic + type searches**: 200-400ms
- **Density analysis**: 500ms-1s
- **Indexes**: Same as providers table (`npi`, `practice_state`, `county_fips`, `taxonomy_1`)

**Optimization Tips**:
- Always filter by `taxonomy_1 LIKE '332%'` first
- Use exact match on taxonomy codes when searching specific types
- Filter by entity_type_code = '2' early (pharmacies are organizations)
- Consider searching taxonomy_2 and taxonomy_3 for comprehensive results

---

## Data Quality Notes

**Pharmacy Count**: Estimated 60,000-80,000 pharmacies in NPPES database
- **Community/Retail**: ~55,000 (largest category)
- **Long-Term Care**: ~5,000
- **Specialty**: ~3,000
- **Mail-Order**: ~500
- **Other types**: Varies

**Entity Type**: 99%+ of pharmacies are Type 2 (Organizations)
- Some individual pharmacists may have pharmacy taxonomy as secondary
- Filter by entity_type_code = '2' for facility-based pharmacies

**Taxonomy Distribution**:
- `taxonomy_1`: Primary classification (best for searching)
- `taxonomy_2-4`: Additional specializations (e.g., retail + compounding)

**Geographic Coverage**:
- 97.77% have county FIPS (same as overall provider coverage)
- Missing FIPS primarily affect mail-order and specialty pharmacies with PO Box addresses

---

## Related Skills

- **provider-search**: Find other healthcare providers
- **rxmembersim-integration**: Link pharmacies to prescription fill data
- **pharmacy-network**: Build pharmacy networks for PBM contracts
- **access-analysis**: Analyze pharmacy access and coverage gaps

---

## Future Enhancements

1. **Pharmacy chains identification** (CVS, Walgreens, Walmart, etc.) via name parsing
2. **24-hour pharmacy flag** from supplementary data sources
3. **Specialty services** (compounding, immunizations, MTM) from taxonomy codes
4. **Network adequacy** calculations with time/distance standards
5. **NCPDP ID linkage** for prescription routing
6. **DEA registration** data for controlled substances
