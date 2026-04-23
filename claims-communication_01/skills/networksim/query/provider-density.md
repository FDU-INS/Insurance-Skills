---
name: provider-density
description: Calculate provider-to-population ratios and identify underserved areas using PopulationSim demographic data

Trigger phrases:
- "Calculate provider density in [location]"
- "Show provider-to-population ratio for [specialty]"
- "Find underserved areas for [specialty]"
- "Analyze provider coverage in [region]"
- "What's the PCP density in [county]?"
---

# Provider Density Skill

## Overview

Calculates provider-to-population ratios using NetworkSim provider data and PopulationSim demographic data. Identifies underserved areas, analyzes specialty distribution, and supports network adequacy assessments for regulatory compliance and strategic planning.

**Key Metrics**:
- **Providers per 100K population**: Industry standard metric
- **PCPs per 100K**: HRSA standard (>60 = adequate)
- **Specialty ratios**: Compare to national benchmarks
- **Geographic coverage**: Counties, metros, rural vs urban

**Data Sources**: 
- `network.providers` (8.9M providers)
- `population.svi_county` (3,144 counties with population)
- `population.places_county` (3,143 counties with health indicators)

---

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| specialty | string/array | No | Taxonomy code(s) or specialty name |
| geography | object | Yes | State, county_fips, or metro area |
| population_source | string | No | 'svi' or 'places' (default: 'svi') |
| min_population | integer | No | Exclude areas below threshold (default: 10000) |
| benchmark | number | No | Compare to standard (e.g., 60 PCPs/100K) |
| include_trend | boolean | No | Show year-over-year changes (future) |

---

## Standard Benchmarks

### National Standards (per 100,000 population)

| Specialty | Standard | Source |
|-----------|----------|--------|
| Primary Care Physicians | 60-80 | HRSA |
| All Physicians | 200-250 | AMA |
| Registered Nurses | 800-900 | BLS |
| Dentists | 60-65 | ADA |
| Psychiatrists | 10-15 | SAMHSA |
| Pharmacies | 25-30 | NACDS |

### Urban vs Rural Thresholds

| Area Type | PCP Ratio | Designation |
|-----------|-----------|-------------|
| Urban | <60/100K | Underserved |
| Rural | <45/100K | Underserved |
| Frontier | <30/100K | Critical Shortage |

---

## Query Patterns

### Pattern 1: Basic Provider Density by County

Calculate providers per 100K for all counties.

```sql
-- Provider density by county with population
SELECT 
    sv.county,
    sv.state,
    sv.e_totpop as population,
    COUNT(DISTINCT p.npi) as provider_count,
    ROUND(100000.0 * COUNT(DISTINCT p.npi) / NULLIF(sv.e_totpop, 0), 2) as providers_per_100k
FROM population.svi_county sv
LEFT JOIN network.providers p ON sv.stcnty = p.county_fips
WHERE sv.e_totpop >= 10000
  AND p.entity_type_code = '1'
GROUP BY sv.county, sv.state, sv.e_totpop
ORDER BY providers_per_100k DESC
LIMIT 50;
```

### Pattern 2: Primary Care Density with Adequacy Assessment

Calculate PCP density and compare to HRSA standard.

```sql
-- PCP density with adequacy assessment
WITH pcp_density AS (
    SELECT 
        sv.stcnty as county_fips,
        sv.county,
        sv.state,
        sv.e_totpop as population,
        COUNT(DISTINCT CASE 
            WHEN p.taxonomy_1 LIKE '207Q%' 
                OR p.taxonomy_1 LIKE '208D%' 
                OR p.taxonomy_1 LIKE '207R%'
            THEN p.npi 
        END) as pcp_count,
        ROUND(100000.0 * COUNT(DISTINCT CASE 
            WHEN p.taxonomy_1 LIKE '207Q%' 
                OR p.taxonomy_1 LIKE '208D%' 
                OR p.taxonomy_1 LIKE '207R%'
            THEN p.npi 
        END) / NULLIF(sv.e_totpop, 0), 2) as pcps_per_100k
    FROM population.svi_county sv
    LEFT JOIN network.providers p ON sv.stcnty = p.county_fips
    WHERE sv.e_totpop >= 10000
      AND (p.entity_type_code = '1' OR p.entity_type_code IS NULL)
    GROUP BY sv.stcnty, sv.county, sv.state, sv.e_totpop
)
SELECT 
    county,
    state,
    population,
    pcp_count,
    pcps_per_100k,
    CASE 
        WHEN pcps_per_100k >= 60 THEN 'Adequate'
        WHEN pcps_per_100k >= 45 THEN 'Below Standard'
        WHEN pcps_per_100k >= 30 THEN 'Underserved'
        ELSE 'Critical Shortage'
    END as adequacy_status,
    60 - pcps_per_100k as gap_from_standard
FROM pcp_density
ORDER BY pcps_per_100k ASC, population DESC
LIMIT 100;
```

### Pattern 3: Specialty Distribution Analysis

Compare density across multiple specialties.

```sql
-- Multi-specialty density comparison
SELECT 
    sv.state,
    sv.e_totpop as total_population,
    COUNT(DISTINCT CASE WHEN p.taxonomy_1 LIKE '207Q%' THEN p.npi END) as family_med,
    COUNT(DISTINCT CASE WHEN p.taxonomy_1 LIKE '207RC%' THEN p.npi END) as cardiology,
    COUNT(DISTINCT CASE WHEN p.taxonomy_1 LIKE '2080P%' THEN p.npi END) as pediatrics,
    COUNT(DISTINCT CASE WHEN p.taxonomy_1 LIKE '207T%' THEN p.npi END) as psychiatry,
    ROUND(100000.0 * COUNT(DISTINCT CASE WHEN p.taxonomy_1 LIKE '207Q%' THEN p.npi END) / NULLIF(sv.e_totpop, 0), 2) as fm_per_100k,
    ROUND(100000.0 * COUNT(DISTINCT CASE WHEN p.taxonomy_1 LIKE '207RC%' THEN p.npi END) / NULLIF(sv.e_totpop, 0), 2) as cardio_per_100k,
    ROUND(100000.0 * COUNT(DISTINCT CASE WHEN p.taxonomy_1 LIKE '2080P%' THEN p.npi END) / NULLIF(sv.e_totpop, 0), 2) as peds_per_100k,
    ROUND(100000.0 * COUNT(DISTINCT CASE WHEN p.taxonomy_1 LIKE '207T%' THEN p.npi END) / NULLIF(sv.e_totpop, 0), 2) as psych_per_100k
FROM (
    SELECT state, SUM(e_totpop) as e_totpop
    FROM population.svi_county
    GROUP BY state
) sv
LEFT JOIN network.providers p ON sv.state = p.practice_state
WHERE p.entity_type_code = '1' OR p.entity_type_code IS NULL
GROUP BY sv.state, sv.e_totpop
ORDER BY sv.state;
```

### Pattern 4: Healthcare Deserts Identification

Find areas with critically low provider density and high health needs.

```sql
-- Healthcare deserts: Low density + high disease burden
WITH county_metrics AS (
    SELECT 
        pc.countyfips,
        pc.countyname,
        pc.stateabbr,
        pc.totalpopulation,
        pc.diabetes_crudeprev,
        pc.obesity_crudeprev,
        COUNT(DISTINCT p.npi) as provider_count,
        ROUND(100000.0 * COUNT(DISTINCT p.npi) / NULLIF(pc.totalpopulation, 0), 2) as providers_per_100k
    FROM population.places_county pc
    LEFT JOIN network.providers p ON pc.countyfips = p.county_fips
    WHERE pc.totalpopulation >= 20000
      AND (p.entity_type_code = '1' OR p.entity_type_code IS NULL)
    GROUP BY pc.countyfips, pc.countyname, pc.stateabbr, pc.totalpopulation, 
             pc.diabetes_crudeprev, pc.obesity_crudeprev
)
SELECT 
    countyname,
    stateabbr,
    totalpopulation,
    provider_count,
    providers_per_100k,
    diabetes_crudeprev as diabetes_rate,
    obesity_crudeprev as obesity_rate,
    CASE 
        WHEN providers_per_100k < 50 AND diabetes_crudeprev > 12 THEN 'Critical'
        WHEN providers_per_100k < 70 AND diabetes_crudeprev > 10 THEN 'High Priority'
        WHEN providers_per_100k < 100 THEN 'Monitor'
        ELSE 'Adequate'
    END as desert_status
FROM county_metrics
WHERE providers_per_100k < 100  -- Below national average
  AND diabetes_crudeprev > 9    -- Above average diabetes
ORDER BY 
    CASE 
        WHEN providers_per_100k < 50 AND diabetes_crudeprev > 12 THEN 1
        WHEN providers_per_100k < 70 AND diabetes_crudeprev > 10 THEN 2
        ELSE 3
    END,
    providers_per_100k ASC
LIMIT 50;
```

### Pattern 5: Pharmacy Density Analysis

Calculate pharmacy access metrics.

```sql
-- Pharmacy density and access metrics
SELECT 
    sv.county,
    sv.state,
    sv.e_totpop as population,
    COUNT(DISTINCT p.npi) as pharmacy_count,
    ROUND(100000.0 * COUNT(DISTINCT p.npi) / NULLIF(sv.e_totpop, 0), 2) as pharmacies_per_100k,
    CASE 
        WHEN ROUND(100000.0 * COUNT(DISTINCT p.npi) / NULLIF(sv.e_totpop, 0), 2) >= 25 
        THEN 'Adequate'
        WHEN ROUND(100000.0 * COUNT(DISTINCT p.npi) / NULLIF(sv.e_totpop, 0), 2) >= 15 
        THEN 'Below Standard'
        ELSE 'Pharmacy Desert'
    END as access_status
FROM population.svi_county sv
LEFT JOIN network.providers p 
    ON sv.stcnty = p.county_fips 
    AND p.taxonomy_1 LIKE '332%'  -- Pharmacy taxonomy
    AND p.entity_type_code = '2'
WHERE sv.e_totpop >= 10000
GROUP BY sv.county, sv.state, sv.e_totpop
ORDER BY pharmacies_per_100k ASC
LIMIT 100;
```

---

## Examples

### Example 1: Calculate PCP Density for California Counties

**Request**: "What's the primary care physician density in California counties?"

**Query**:
```sql
WITH ca_pcp_density AS (
    SELECT 
        sv.county,
        sv.state,
        sv.e_totpop as population,
        COUNT(DISTINCT p.npi) as pcp_count,
        ROUND(100000.0 * COUNT(DISTINCT p.npi) / NULLIF(sv.e_totpop, 0), 2) as pcps_per_100k
    FROM population.svi_county sv
    LEFT JOIN network.providers p ON sv.stcnty = p.county_fips
    WHERE sv.state = 'California'
      AND sv.e_totpop >= 10000
      AND (
          p.taxonomy_1 LIKE '207Q%' OR  -- Family Medicine
          p.taxonomy_1 LIKE '208D%' OR  -- General Practice
          p.taxonomy_1 LIKE '207R%'     -- Internal Medicine
      )
      AND p.entity_type_code = '1'
    GROUP BY sv.county, sv.state, sv.e_totpop
)
SELECT 
    county,
    population,
    pcp_count,
    pcps_per_100k,
    CASE 
        WHEN pcps_per_100k >= 60 THEN '✓ Adequate'
        WHEN pcps_per_100k >= 45 THEN '⚠ Below Standard'
        ELSE '✗ Underserved'
    END as status,
    GREATEST(0, 60 - pcps_per_100k) as gap_from_hrsa_standard
FROM ca_pcp_density
ORDER BY pcps_per_100k ASC
LIMIT 20;
```

**Expected Output**:
```
county              | population | pcp_count | pcps_per_100k | status          | gap
--------------------|------------|-----------|---------------|-----------------|------
Alpine County       | 1,204      | 0         | 0.00          | ✗ Underserved   | 60.00
Modoc County        | 8,661      | 2         | 23.09         | ✗ Underserved   | 36.91
Trinity County      | 16,060     | 8         | 49.81         | ⚠ Below Standard| 10.19
Los Angeles County  | 10,014,009 | 7,234     | 72.24         | ✓ Adequate      | 0.00
San Francisco County| 873,965    | 985       | 112.70        | ✓ Adequate      | 0.00
```

### Example 2: Identify Healthcare Deserts in High-Diabetes Areas

**Request**: "Find counties with low provider density and high diabetes rates"

**Query**:
```sql
WITH desert_analysis AS (
    SELECT 
        pc.countyname,
        pc.stateabbr,
        pc.totalpopulation,
        pc.diabetes_crudeprev,
        sv.rpl_themes as social_vulnerability,
        COUNT(DISTINCT p.npi) as provider_count,
        ROUND(100000.0 * COUNT(DISTINCT p.npi) / NULLIF(pc.totalpopulation, 0), 2) as providers_per_100k
    FROM population.places_county pc
    LEFT JOIN population.svi_county sv ON pc.countyfips = sv.stcnty
    LEFT JOIN network.providers p ON pc.countyfips = p.county_fips
    WHERE pc.totalpopulation >= 25000
      AND (p.entity_type_code = '1' OR p.entity_type_code IS NULL)
    GROUP BY pc.countyname, pc.stateabbr, pc.totalpopulation, 
             pc.diabetes_crudeprev, sv.rpl_themes
)
SELECT 
    countyname,
    stateabbr,
    totalpopulation,
    provider_count,
    providers_per_100k,
    diabetes_crudeprev as diabetes_rate,
    social_vulnerability,
    CASE 
        WHEN providers_per_100k < 50 AND diabetes_crudeprev > 13 THEN 'CRITICAL DESERT'
        WHEN providers_per_100k < 70 AND diabetes_crudeprev > 11 THEN 'High Priority'
        ELSE 'Monitor'
    END as priority_level
FROM desert_analysis
WHERE providers_per_100k < 100 
  AND diabetes_crudeprev > 9
ORDER BY 
    CASE priority_level
        WHEN 'CRITICAL DESERT' THEN 1
        WHEN 'High Priority' THEN 2
        ELSE 3
    END,
    diabetes_crudeprev DESC,
    providers_per_100k ASC
LIMIT 30;
```

**Expected Output**: List of underserved counties with high health needs

### Example 3: State-Level Specialty Distribution

**Request**: "Compare specialty provider density across states"

**Query**:
```sql
WITH state_specialty_density AS (
    SELECT 
        sv.state,
        SUM(sv.e_totpop) as total_population,
        COUNT(DISTINCT CASE WHEN p.taxonomy_1 LIKE '207Q%' OR p.taxonomy_1 LIKE '207R%' THEN p.npi END) as pcps,
        COUNT(DISTINCT CASE WHEN p.taxonomy_1 LIKE '207RC%' THEN p.npi END) as cardiologists,
        COUNT(DISTINCT CASE WHEN p.taxonomy_1 LIKE '2080P%' THEN p.npi END) as pediatricians,
        COUNT(DISTINCT CASE WHEN p.taxonomy_1 LIKE '207T%' THEN p.npi END) as psychiatrists,
        COUNT(DISTINCT CASE WHEN p.taxonomy_1 LIKE '163W%' THEN p.npi END) as nurses
    FROM (
        SELECT state, SUM(e_totpop) as e_totpop
        FROM population.svi_county
        GROUP BY state
    ) sv
    LEFT JOIN network.providers p ON sv.state = p.practice_state AND p.entity_type_code = '1'
    GROUP BY sv.state, sv.e_totpop
)
SELECT 
    state,
    total_population,
    pcps,
    ROUND(100000.0 * pcps / total_population, 1) as pcp_per_100k,
    ROUND(100000.0 * cardiologists / total_population, 1) as cardio_per_100k,
    ROUND(100000.0 * pediatricians / total_population, 1) as peds_per_100k,
    ROUND(100000.0 * psychiatrists / total_population, 1) as psych_per_100k,
    ROUND(100000.0 * nurses / total_population, 1) as nurse_per_100k
FROM state_specialty_density
WHERE total_population > 0
ORDER BY pcp_per_100k DESC
LIMIT 25;
```

**Expected Output**: State comparison table with specialty ratios

---

## Visualization Support

### Summary Statistics for Dashboards

```sql
-- Summary metrics for visualization
SELECT 
    'National' as geography,
    COUNT(DISTINCT sv.stcnty) as counties_analyzed,
    SUM(sv.e_totpop) as total_population,
    COUNT(DISTINCT p.npi) as total_providers,
    ROUND(100000.0 * COUNT(DISTINCT p.npi) / NULLIF(SUM(sv.e_totpop), 0), 2) as avg_density,
    COUNT(DISTINCT CASE WHEN density_calc.providers_per_100k < 60 THEN sv.stcnty END) as underserved_counties,
    ROUND(100.0 * COUNT(DISTINCT CASE WHEN density_calc.providers_per_100k < 60 THEN sv.stcnty END) / 
          COUNT(DISTINCT sv.stcnty), 1) as pct_underserved
FROM population.svi_county sv
LEFT JOIN network.providers p ON sv.stcnty = p.county_fips AND p.entity_type_code = '1'
LEFT JOIN (
    SELECT 
        sv2.stcnty,
        ROUND(100000.0 * COUNT(DISTINCT p2.npi) / NULLIF(sv2.e_totpop, 0), 2) as providers_per_100k
    FROM population.svi_county sv2
    LEFT JOIN network.providers p2 ON sv2.stcnty = p2.county_fips
    GROUP BY sv2.stcnty, sv2.e_totpop
) density_calc ON sv.stcnty = density_calc.stcnty
WHERE sv.e_totpop >= 10000;
```

### Distribution Buckets for Histograms

```sql
-- Provider density distribution for charts
SELECT 
    CASE 
        WHEN providers_per_100k < 20 THEN '0-20'
        WHEN providers_per_100k < 40 THEN '20-40'
        WHEN providers_per_100k < 60 THEN '40-60'
        WHEN providers_per_100k < 80 THEN '60-80'
        WHEN providers_per_100k < 100 THEN '80-100'
        ELSE '100+'
    END as density_bucket,
    COUNT(*) as county_count,
    ROUND(AVG(providers_per_100k), 1) as avg_density,
    SUM(population) as total_population
FROM (
    SELECT 
        sv.stcnty,
        sv.county,
        sv.state,
        sv.e_totpop as population,
        ROUND(100000.0 * COUNT(DISTINCT p.npi) / NULLIF(sv.e_totpop, 0), 2) as providers_per_100k
    FROM population.svi_county sv
    LEFT JOIN network.providers p ON sv.stcnty = p.county_fips
    WHERE sv.e_totpop >= 10000
      AND (p.entity_type_code = '1' OR p.entity_type_code IS NULL)
    GROUP BY sv.stcnty, sv.county, sv.state, sv.e_totpop
) density_data
GROUP BY density_bucket
ORDER BY density_bucket;
```

---

## Validation Rules

### Data Quality Checks
- Population data must be current (within 5 years)
- Exclude counties with population <10K (unreliable ratios)
- Provider counts must include only active NPIs
- Entity type filter required (individual vs organization)

### Calculation Validation
- Denominators never zero (use NULLIF)
- Ratios rounded to 2 decimal places
- Negative values impossible (COUNT always ≥0)
- Sanity check: Density <500/100K (flag outliers)

---

## Performance Notes

- **State-level aggregation**: <50ms
- **County-level (3K counties)**: 200-500ms
- **Healthcare deserts query**: 500ms-1s (complex JOINs)
- **Specialty distribution**: 300-600ms

**Optimization Tips**:
- Pre-aggregate at state level when possible
- Use CTEs for complex calculations
- Filter by minimum population early
- Index on county_fips for JOIN performance

---

## Related Skills

- **[coverage-analysis](coverage-analysis.md)**: Network adequacy assessment
- **[provider-search](provider-search.md)**: Find providers in underserved areas
- **[network-roster](network-roster.md)**: Build networks for low-density areas

---

## Future Enhancements

1. **Trend analysis** using multi-year NPPES data
2. **Drive-time accessibility** using geospatial calculations
3. **Specialty-specific benchmarks** by disease prevalence
4. **Rural vs urban classification** using RUCA codes
5. **Provider FTE adjustment** (part-time vs full-time)
6. **Telehealth impact modeling** on effective density

---

*Last Updated: December 27, 2025*  
*Version: 1.0.0*
