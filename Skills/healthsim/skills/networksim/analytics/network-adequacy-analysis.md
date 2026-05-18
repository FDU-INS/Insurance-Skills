---
name: network-adequacy-analysis
description: Advanced network adequacy assessment combining time/distance access, provider-to-member ratios, and specialty coverage requirements for regulatory compliance

Trigger phrases:
- "Assess network adequacy for [geography]"
- "Calculate time and distance access standards"
- "Check NCQA adequacy requirements"
- "Generate network adequacy report"
- "Analyze access to care in [region]"
---

# Network Adequacy Analysis Skill

## Overview

Comprehensive network adequacy assessment for regulatory compliance and strategic planning. Combines multiple adequacy dimensions including time/distance access, provider-to-enrollee ratios, specialty coverage, and quality metrics to provide a complete picture of network performance.

**Adequacy Dimensions:**
- **Time/Distance Access**: Geographic proximity standards (CMS, NCQA, state requirements)
- **Provider Ratios**: Enrollee-to-provider counts (CMS MA, Medicaid MCO)
- **Specialty Coverage**: Essential specialty availability (NCQA 13 categories)
- **Quality Standards**: Minimum quality thresholds (star ratings, credentials)
- **Appointment Access**: Availability and wait times (when data available)

**Regulatory Frameworks:**
- CMS Medicare Advantage (MA) network adequacy standards
- NCQA Health Plan Accreditation requirements
- State Medicaid MCO network standards (varies by state)
- ACA Qualified Health Plan (QHP) network adequacy

**Data Sources**: 
- `network.providers` (8.9M providers with locations)
- `network.facilities` (60K+ facilities)
- `network.hospital_quality` (CMS star ratings)
- `population.svi_county` (demographics, 3,144 counties)
- `population.places_county` (health indicators)

---

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| geography | string/array | Yes | State, county, or ZIP codes to analyze |
| standard | string | No | Adequacy standard ('cms_ma', 'ncqa', 'state_medicaid') |
| specialty | string/array | No | Specific specialties to assess |
| min_quality | string | No | Minimum quality threshold ('3', '4', '5' stars) |
| enrollee_count | integer | No | Projected enrollment for ratio calculations |
| urban_rural | string | No | Geographic classification ('urban', 'suburban', 'rural') |

---

## CMS Medicare Advantage Time/Distance Standards

### Standard Access Requirements

**Urban Areas** (>50,000 population):
```
Primary Care:         10 miles
Specialists:          15 miles
Hospitals:            15 miles
Pharmacies:           2 miles
```

**Suburban Areas** (10,000-50,000 population):
```
Primary Care:         20 miles
Specialists:          30 miles
Hospitals:            30 miles
Pharmacies:           5 miles
```

**Rural Areas** (<10,000 population):
```
Primary Care:         30 miles
Specialists:          60 miles
Hospitals:            60 miles
Pharmacies:           15 miles
```

**Note**: Current implementation uses county-level aggregation as proxy for time/distance. True geospatial calculations require lat/long coordinates and routing algorithms (future enhancement).

---

## CMS Provider-to-Enrollee Ratios

### Required Minimums

| Specialty | Ratio | Example (1,000 Enrollees) |
|-----------|-------|---------------------------|
| Primary Care | 1:1,200 | 0.83 PCPs minimum |
| OB/GYN | 1:2,000 | 0.50 providers |
| Mental Health | 1:3,000 | 0.33 providers |
| General Surgery | 1:5,000 | 0.20 providers |

**Calculation Formula:**
```
Required Providers = Enrollees / Ratio
Network Adequacy % = (Actual Providers / Required Providers) × 100
```

---

## NCQA Essential Specialty Requirements

### 13 Required Specialties

Must have at least one contracted provider in each:

1. **Primary Care** (Family Medicine, Internal Medicine, Pediatrics)
2. **Cardiology** (heart disease specialists)
3. **Dermatology** (skin conditions)
4. **Endocrinology** (diabetes, thyroid disorders)
5. **Gastroenterology** (digestive system)
6. **General Surgery** (surgical procedures)
7. **Neurology** (brain, nervous system)
8. **OB/GYN** (women's health)
9. **Ophthalmology** (eye care)
10. **Orthopedic Surgery** (bones, joints, muscles)
11. **Otolaryngology (ENT)** (ear, nose, throat)
12. **Psychiatry** (mental health)
13. **Urology** (urinary tract, male reproductive)

---

## Query Patterns

### Pattern 1: Basic Adequacy Assessment

Assess provider availability against enrollment.

```sql
-- Network adequacy for Texas counties (PCP focus)
WITH county_demographics AS (
    SELECT 
        sv.county,
        sv.state,
        sv.e_totpop as population,
        sv.stcnty as county_fips
    FROM population.svi_county sv
    WHERE sv.state = 'Texas'
),
county_providers AS (
    SELECT 
        p.county_fips,
        COUNT(DISTINCT CASE 
            WHEN p.taxonomy_1 LIKE '207Q%' OR p.taxonomy_1 LIKE '207R%' 
            THEN p.npi END) as pcp_count
    FROM network.providers p
    WHERE p.entity_type_code = '1'
      AND p.practice_state = 'TX'
    GROUP BY p.county_fips
)
SELECT 
    cd.county,
    cd.population,
    COALESCE(cp.pcp_count, 0) as actual_pcps,
    ROUND(cd.population / 1200.0, 1) as required_pcps_cms,
    ROUND(100.0 * COALESCE(cp.pcp_count, 0) / (cd.population / 1200.0), 1) as adequacy_pct,
    CASE 
        WHEN COALESCE(cp.pcp_count, 0) / (cd.population / 1200.0) >= 1.0 THEN 'Adequate'
        WHEN COALESCE(cp.pcp_count, 0) / (cd.population / 1200.0) >= 0.75 THEN 'Approaching'
        WHEN COALESCE(cp.pcp_count, 0) / (cd.population / 1200.0) >= 0.5 THEN 'Inadequate'
        ELSE 'Critical Shortage'
    END as adequacy_status
FROM county_demographics cd
LEFT JOIN county_providers cp ON cd.county_fips = cp.county_fips
ORDER BY adequacy_pct ASC
LIMIT 20;
```

### Pattern 2: NCQA Specialty Coverage Assessment

Check if all 13 essential specialties are represented.

```sql
-- NCQA essential specialty coverage for California
WITH specialty_mapping AS (
    SELECT 'Primary Care' as specialty_name, '207Q%' as taxonomy_pattern
    UNION ALL SELECT 'Primary Care', '207R%'
    UNION ALL SELECT 'Cardiology', '207RC%'
    UNION ALL SELECT 'Dermatology', '207N%'
    UNION ALL SELECT 'Endocrinology', '207RE%'
    UNION ALL SELECT 'Gastroenterology', '207RG%'
    UNION ALL SELECT 'General Surgery', '208600%'
    UNION ALL SELECT 'Neurology', '207RN%'
    UNION ALL SELECT 'OB/GYN', '207V%'
    UNION ALL SELECT 'Ophthalmology', '207W%'
    UNION ALL SELECT 'Orthopedic Surgery', '207X%'
    UNION ALL SELECT 'Otolaryngology (ENT)', '207YX%'
    UNION ALL SELECT 'Psychiatry', '208000%'
    UNION ALL SELECT 'Urology', '208800%'
),
specialty_counts AS (
    SELECT 
        sm.specialty_name,
        COUNT(DISTINCT p.npi) as provider_count
    FROM specialty_mapping sm
    LEFT JOIN network.providers p 
        ON p.taxonomy_1 LIKE sm.taxonomy_pattern
        AND p.practice_state = 'CA'
        AND p.entity_type_code = '1'
    GROUP BY sm.specialty_name
)
SELECT 
    specialty_name,
    provider_count,
    CASE 
        WHEN provider_count >= 10 THEN 'Well Covered'
        WHEN provider_count >= 5 THEN 'Adequate'
        WHEN provider_count >= 1 THEN 'Minimally Adequate'
        ELSE 'Not Covered'
    END as coverage_status,
    CASE WHEN provider_count >= 1 THEN 'Yes' ELSE 'No' END as ncqa_compliant
FROM specialty_counts
ORDER BY provider_count ASC;
```

### Pattern 3: Quality-Adjusted Adequacy

Include quality metrics in adequacy assessment.

```sql
-- High-quality network adequacy (4-5 star hospitals + MD/DO PCPs)
WITH quality_providers AS (
    SELECT 
        p.practice_state,
        p.county_fips,
        COUNT(DISTINCT p.npi) as quality_pcp_count
    FROM network.providers p
    WHERE (p.taxonomy_1 LIKE '207Q%' OR p.taxonomy_1 LIKE '207R%')
      AND p.credential ~ 'M\\.?D\\.?|D\\.?O\\.?'
      AND p.entity_type_code = '1'
      AND p.practice_state IN ('CA', 'TX', 'FL')
    GROUP BY p.practice_state, p.county_fips
),
quality_hospitals AS (
    SELECT 
        f.state,
        f.county_fips,
        COUNT(DISTINCT hq.facility_id) as quality_hospital_count
    FROM network.facilities f
    INNER JOIN network.hospital_quality hq 
        ON f.ccn = hq.facility_id
        AND hq.hospital_overall_rating IN ('4', '5')
    WHERE f.type = '01'  -- Hospitals
      AND f.state IN ('CA', 'TX', 'FL')
    GROUP BY f.state, f.county_fips
),
demographics AS (
    SELECT 
        sv.state,
        sv.stcnty as county_fips,
        sv.county,
        sv.e_totpop as population
    FROM population.svi_county sv
    WHERE sv.state IN ('California', 'Texas', 'Florida')
)
SELECT 
    d.state,
    d.county,
    d.population,
    COALESCE(qp.quality_pcp_count, 0) as quality_pcps,
    COALESCE(qh.quality_hospital_count, 0) as quality_hospitals,
    ROUND(d.population / 1200.0, 1) as required_pcps,
    ROUND(100.0 * COALESCE(qp.quality_pcp_count, 0) / (d.population / 1200.0), 1) as quality_adequacy_pct,
    CASE 
        WHEN COALESCE(qp.quality_pcp_count, 0) >= d.population / 1200.0 
             AND COALESCE(qh.quality_hospital_count, 0) >= 1 THEN 'High Quality Network'
        WHEN COALESCE(qp.quality_pcp_count, 0) >= d.population / 1800.0 THEN 'Adequate Quality'
        ELSE 'Quality Gaps'
    END as quality_status
FROM demographics d
LEFT JOIN quality_providers qp ON d.county_fips = qp.county_fips
LEFT JOIN quality_hospitals qh ON d.county_fips = qh.county_fips
WHERE d.population > 50000  -- Focus on larger counties
ORDER BY quality_adequacy_pct ASC
LIMIT 25;
```

### Pattern 4: Multi-Specialty Adequacy Scorecard

Comprehensive adequacy across multiple dimensions.

```sql
-- Network adequacy scorecard for a state
WITH pcp_adequacy AS (
    SELECT 
        p.practice_state,
        COUNT(DISTINCT p.npi) as pcp_count,
        SUM(sv.e_totpop) as total_population,
        ROUND(100.0 * COUNT(DISTINCT p.npi) / (SUM(sv.e_totpop) / 1200.0), 1) as pcp_adequacy_pct
    FROM network.providers p
    INNER JOIN population.svi_county sv 
        ON p.county_fips = sv.stcnty
    WHERE (p.taxonomy_1 LIKE '207Q%' OR p.taxonomy_1 LIKE '207R%')
      AND p.entity_type_code = '1'
      AND p.practice_state = 'CA'
    GROUP BY p.practice_state
),
specialist_adequacy AS (
    SELECT 
        p.practice_state,
        COUNT(DISTINCT CASE WHEN p.taxonomy_1 LIKE '207V%' THEN p.npi END) as obgyn_count,
        COUNT(DISTINCT CASE WHEN p.taxonomy_1 LIKE '208000%' THEN p.npi END) as psych_count,
        COUNT(DISTINCT CASE WHEN p.taxonomy_1 LIKE '208600%' THEN p.npi END) as surgery_count
    FROM network.providers p
    WHERE p.entity_type_code = '1'
      AND p.practice_state = 'CA'
    GROUP BY p.practice_state
),
hospital_adequacy AS (
    SELECT 
        f.state,
        COUNT(DISTINCT f.ccn) as total_hospitals,
        COUNT(DISTINCT CASE WHEN hq.hospital_overall_rating IN ('4', '5') THEN f.ccn END) as quality_hospitals
    FROM network.facilities f
    LEFT JOIN network.hospital_quality hq ON f.ccn = hq.facility_id
    WHERE f.type = '01'
      AND f.state = 'CA'
    GROUP BY f.state
)
SELECT 
    pcp.practice_state as state,
    pcp.total_population,
    pcp.pcp_count,
    pcp.pcp_adequacy_pct,
    spec.obgyn_count,
    spec.psych_count,
    spec.surgery_count,
    hosp.total_hospitals,
    hosp.quality_hospitals,
    CASE 
        WHEN pcp.pcp_adequacy_pct >= 100 
             AND spec.obgyn_count >= pcp.total_population / 2000
             AND spec.psych_count >= pcp.total_population / 3000
             AND hosp.quality_hospitals >= 10 THEN 'Exceeds Standards'
        WHEN pcp.pcp_adequacy_pct >= 75 THEN 'Meets Standards'
        WHEN pcp.pcp_adequacy_pct >= 50 THEN 'Approaching Standards'
        ELSE 'Below Standards'
    END as overall_adequacy_status
FROM pcp_adequacy pcp
LEFT JOIN specialist_adequacy spec ON pcp.practice_state = spec.practice_state
LEFT JOIN hospital_adequacy hosp ON pcp.practice_state = hosp.state;
```

### Pattern 5: Geographic Access Proxy Analysis

County-level access as proxy for time/distance (conceptual).

```sql
-- Geographic access proxy: counties without providers
WITH provider_coverage AS (
    SELECT 
        sv.state,
        sv.county,
        sv.stcnty as county_fips,
        sv.e_totpop as population,
        COUNT(DISTINCT p.npi) as provider_count,
        COUNT(DISTINCT CASE WHEN p.taxonomy_1 LIKE '207Q%' OR p.taxonomy_1 LIKE '207R%' 
              THEN p.npi END) as pcp_count,
        COUNT(DISTINCT f.ccn) as hospital_count
    FROM population.svi_county sv
    LEFT JOIN network.providers p 
        ON sv.stcnty = p.county_fips
        AND p.entity_type_code = '1'
    LEFT JOIN network.facilities f 
        ON sv.stcnty = f.county_fips
        AND f.type = '01'
    WHERE sv.state IN ('Texas', 'California', 'Florida')
    GROUP BY sv.state, sv.county, sv.stcnty, sv.e_totpop
)
SELECT 
    state,
    county,
    population,
    provider_count,
    pcp_count,
    hospital_count,
    CASE 
        WHEN provider_count = 0 THEN 'No Providers (Access Desert)'
        WHEN pcp_count = 0 THEN 'No Primary Care'
        WHEN hospital_count = 0 THEN 'No Hospital Access'
        WHEN provider_count < population / 10000 THEN 'Severely Limited'
        ELSE 'Has Coverage'
    END as access_status,
    CASE 
        WHEN provider_count = 0 OR pcp_count = 0 THEN 'Critical'
        WHEN provider_count < population / 5000 THEN 'High Priority'
        WHEN provider_count < population / 2500 THEN 'Medium Priority'
        ELSE 'Low Priority'
    END as recruitment_priority
FROM provider_coverage
WHERE population > 10000  -- Focus on counties with significant population
  AND (provider_count = 0 OR pcp_count = 0 OR provider_count < population / 5000)
ORDER BY 
    CASE 
        WHEN provider_count = 0 THEN 1
        WHEN pcp_count = 0 THEN 2
        ELSE 3
    END,
    population DESC
LIMIT 30;
```

---

## Examples

### Example 1: State-Level PCP Adequacy Assessment

**Request**: "Assess primary care network adequacy for Texas"

**Query**:
```sql
WITH texas_demographics AS (
    SELECT 
        SUM(e_totpop) as total_population,
        COUNT(DISTINCT stcnty) as county_count
    FROM population.svi_county
    WHERE state = 'Texas'
),
texas_pcps AS (
    SELECT 
        COUNT(DISTINCT npi) as pcp_count
    FROM network.providers
    WHERE (taxonomy_1 LIKE '207Q%' OR taxonomy_1 LIKE '207R%')
      AND practice_state = 'TX'
      AND entity_type_code = '1'
)
SELECT 
    td.total_population,
    td.county_count,
    tp.pcp_count,
    ROUND(td.total_population / 1200.0, 0) as required_pcps_cms,
    ROUND(100.0 * tp.pcp_count / (td.total_population / 1200.0), 1) as adequacy_pct,
    CASE 
        WHEN tp.pcp_count / (td.total_population / 1200.0) >= 1.2 THEN 'Exceeds CMS Standard'
        WHEN tp.pcp_count / (td.total_population / 1200.0) >= 1.0 THEN 'Meets CMS Standard'
        WHEN tp.pcp_count / (td.total_population / 1200.0) >= 0.75 THEN 'Approaching Standard'
        ELSE 'Below Standard'
    END as adequacy_status
FROM texas_demographics td, texas_pcps tp;
```

**Expected Output**:
```
total_population | county_count | pcp_count | required_pcps_cms | adequacy_pct | adequacy_status
-----------------|--------------|-----------|-------------------|--------------|------------------
28,191,816       | 120          | 27,730    | 23,493            | 118.0%       | Exceeds CMS Standard
```

### Example 2: NCQA Specialty Coverage Check

**Request**: "Check if California network meets NCQA 13 essential specialties"

*Uses Pattern 2 query from above*

**Expected Output**:
```
specialty_name          | provider_count | coverage_status | ncqa_compliant
------------------------|----------------|-----------------|---------------
Primary Care            | 45,234         | Well Covered    | Yes
Cardiology              | 3,456          | Well Covered    | Yes
Dermatology             | 2,123          | Well Covered    | Yes
...
Psychiatry              | 1,234          | Well Covered    | Yes
Urology                 | 987            | Well Covered    | Yes
```

### Example 3: Quality-Adjusted Adequacy

**Request**: "Assess network adequacy using only high-quality providers (4-5 star hospitals, MD/DO physicians)"

*Uses Pattern 3 query from above*

**Expected Output**:
```
state  | county         | population | quality_pcps | quality_hospitals | quality_adequacy_pct | quality_status
-------|----------------|------------|--------------|-------------------|---------------------|------------------
CA     | LOS ANGELES    | 10,014,009 | 8,456        | 12                | 101.3%              | High Quality Network
CA     | SAN DIEGO      | 3,298,634  | 2,789        | 5                 | 101.5%              | High Quality Network
TX     | HARRIS         | 4,713,325  | 3,234        | 8                 | 82.2%               | Adequate Quality
```

---

## Adequacy Scoring Methodology

### Composite Adequacy Score (0-100)

**Components** (each 0-100):
1. **Provider Ratio Score** (40 points)
   - PCPs: Actual / Required (CMS 1:1,200)
   - Specialists: Average across NCQA 13 categories
   
2. **Geographic Access Score** (30 points)
   - County coverage: % counties with providers
   - Urban/Suburban/Rural standards met
   
3. **Specialty Coverage Score** (20 points)
   - NCQA 13 essential specialties present
   - Specialty depth (multiple providers per specialty)
   
4. **Quality Score** (10 points)
   - % providers meeting quality thresholds
   - % facilities with 4-5 star ratings

**Formula**:
```
Composite Score = (Provider Ratio × 0.40) + 
                  (Geographic Access × 0.30) + 
                  (Specialty Coverage × 0.20) + 
                  (Quality × 0.10)
```

**Interpretation**:
- **90-100**: Excellent - Exceeds all standards
- **75-89**: Good - Meets standards with margin
- **60-74**: Adequate - Meets minimum standards
- **50-59**: Approaching - Near standards, gaps exist
- **<50**: Inadequate - Falls short of standards

---

## Integration with Other Skills

### With Provider Density
```sql
-- Adequacy + density analysis
SELECT 
    pd.county,
    pd.providers_per_100k,
    na.adequacy_pct,
    CASE 
        WHEN pd.providers_per_100k >= 60 AND na.adequacy_pct >= 100 THEN 'Optimal'
        WHEN na.adequacy_pct >= 75 THEN 'Adequate'
        ELSE 'Gaps Exist'
    END as combined_status
FROM provider_density pd
JOIN network_adequacy na ON pd.county_fips = na.county_fips;
```

### With Coverage Analysis
```sql
-- Expand on coverage-analysis with adequacy scoring
SELECT 
    ca.county,
    ca.current_providers,
    ca.target_providers_cms,
    ca.adequacy_pct,
    na.composite_adequacy_score,
    na.adequacy_tier
FROM coverage_analysis ca
JOIN network_adequacy_scores na ON ca.county_fips = na.county_fips;
```

### With Healthcare Deserts
```sql
-- Adequacy in underserved areas
SELECT hd.county, hd.desert_type, na.adequacy_pct
FROM healthcare_deserts hd
JOIN network_adequacy na ON hd.county_fips = na.county_fips
WHERE hd.desert_severity = 'Critical';
```

---

## Validation Rules

### CMS Standards
- Provider ratios must meet minimums (1:1,200 PCPs, etc.)
- Time/distance standards apply by geography type
- All specialties must be available within distance thresholds

### NCQA Requirements
- All 13 essential specialties must be represented
- Minimum provider counts per specialty
- Geographic distribution requirements

### State Variations
- Some states have stricter standards
- Medicaid MCO requirements vary by state
- Rural vs urban thresholds differ

---

## Performance Notes

- **State-level adequacy**: 50-100ms
- **County-level adequacy**: 100-300ms (120 counties)
- **NCQA specialty check**: 50-100ms
- **Quality-adjusted adequacy**: 200-400ms (complex JOINs)
- **Composite scoring**: 300-600ms (multi-table aggregation)

**Optimization Tips**:
- Filter by state early in query
- Use materialized views for demographic data
- Cache specialty mapping tables
- Index on county_fips for JOINs

---

## Future Enhancements

1. **True Time/Distance Calculations**
   - Geospatial queries with lat/long coordinates
   - Road network routing algorithms
   - Drive time isochrones (15, 30, 60 min)

2. **Appointment Availability**
   - Provider capacity metrics
   - Average wait times for appointments
   - New patient acceptance rates

3. **Telehealth Integration**
   - Virtual care provider counts
   - Telehealth-adjusted adequacy standards
   - Hybrid network models

4. **Provider Panel Status**
   - Open vs closed panels
   - Patient attribution data
   - Provider capacity utilization

5. **Predictive Adequacy**
   - Retirement projections
   - New provider additions
   - Population growth forecasts

6. **State-Specific Standards**
   - Medicaid MCO requirements by state
   - Commercial plan regulations
   - CON (Certificate of Need) considerations

---

## Related Skills

- **[coverage-analysis](../query/coverage-analysis.md)**: Foundational adequacy assessment
- **[provider-density](../query/provider-density.md)**: Providers per 100K population
- **[healthcare-deserts](healthcare-deserts.md)**: Underserved area identification
- **[specialty-distribution-pattern](../patterns/specialty-distribution-pattern.md)**: Specialty mix analysis
- **[hospital-quality-search](../query/hospital-quality-search.md)**: Quality-adjusted networks

---

*Last Updated: December 27, 2025*  
*Version: 1.0.0*  
*Standards: CMS MA, NCQA, State Medicaid MCO*
