---
name: healthcare-deserts
description: Identify healthcare deserts by combining provider density, health needs, social vulnerability, and access barriers to prioritize underserved communities

Trigger phrases:
- "Identify healthcare deserts in [geography]"
- "Find underserved communities"
- "Analyze provider access gaps"
- "Where are the areas with poor healthcare access?"
- "Show me communities with high need and low access"
---

# Healthcare Deserts Skill

## Overview

Healthcare deserts are geographic areas with inadequate access to healthcare providers combined with high health needs. This skill identifies underserved communities by integrating multiple data dimensions: provider supply (NetworkSim), disease burden (PopulationSim CDC PLACES), and social vulnerability (PopulationSim SVI).

**What Makes a Healthcare Desert:**
- **Low Provider Access**: Few or no providers relative to population
- **High Health Needs**: Elevated disease prevalence, poor health outcomes
- **Social Vulnerability**: Barriers to care (poverty, transportation, language)
- **Geographic Isolation**: Distance from care facilities
- **Quality Gaps**: Limited access to high-quality providers

**Analysis Dimensions:**
1. **Provider Access**: Density, specialty availability, facility access
2. **Health Burden**: Chronic disease prevalence, preventable mortality
3. **Social Determinants**: Poverty, insurance status, transportation
4. **Quality Metrics**: Hospital ratings, provider credentials
5. **Equity Considerations**: Racial/ethnic disparities, vulnerable populations

**Data Sources**:
- `network.providers` (8.9M providers)
- `network.facilities` (hospitals, clinics)
- `network.hospital_quality` (CMS star ratings)
- `population.svi_county` (Social Vulnerability Index, 3,144 counties)
- `population.places_county` (CDC health indicators, 3,143 counties)

---

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| geography | string/array | Yes | State, county, or region to analyze |
| desert_type | string | No | Focus area ('primary_care', 'mental_health', 'maternity', 'all') |
| severity_threshold | string | No | Minimum severity ('critical', 'severe', 'moderate') |
| population_min | integer | No | Minimum population to consider (default: 10,000) |
| include_svi | boolean | No | Include social vulnerability factors (default: true) |
| include_health | boolean | No | Include health outcome data (default: true) |

---

## Healthcare Desert Classifications

### Primary Care Deserts
**Criteria:**
- <20 PCPs per 100K population (vs HRSA standard 60-80)
- No PCP within county boundaries
- High rates of preventable hospitalizations

**Health Impact:**
- Delayed diagnosis and treatment
- Higher ER utilization for primary care needs
- Worse management of chronic conditions

### Mental Health Deserts
**Criteria:**
- <5 psychiatrists per 100K population
- Limited behavioral health provider access
- High suicide rates, depression prevalence

**Health Impact:**
- Untreated mental illness
- Substance abuse complications
- Suicide risk

### Maternity Care Deserts
**Criteria:**
- No OB/GYN providers
- No hospital with obstetric services
- >30 miles to nearest birthing facility

**Health Impact:**
- Higher maternal mortality
- Limited prenatal care
- Emergency deliveries

### Specialty Deserts
**Criteria:**
- Missing essential NCQA specialties
- Limited access to specialists
- Long wait times for specialty care

**Health Impact:**
- Disease progression
- Treatment delays
- Complications from delayed care

---

## Desert Severity Scoring

### Composite Desert Score (0-100)

**Formula:**
```
Desert Score = (Access Gap × 0.35) + 
               (Health Burden × 0.30) + 
               (Social Vulnerability × 0.25) + 
               (Quality Gap × 0.10)
```

**Components:**

1. **Access Gap (0-100)**:
   - Provider-to-population ratio vs HRSA benchmarks
   - Distance to nearest facility
   - Specialty availability

2. **Health Burden (0-100)**:
   - Chronic disease prevalence
   - Preventable mortality rates
   - Poor/fair health self-rating

3. **Social Vulnerability (0-100)**:
   - SVI overall percentile
   - Poverty rate, uninsured rate
   - Transportation barriers

4. **Quality Gap (0-100)**:
   - Access to 4-5 star hospitals
   - MD/DO vs NP/PA ratio
   - Provider credential quality

**Severity Tiers:**
- **Critical** (80-100): Immediate intervention needed
- **Severe** (60-79): High priority for resources
- **Moderate** (40-59): Targeted improvements needed
- **Mild** (20-39): Monitor for changes
- **Minimal** (<20): Not a desert

---

## Query Patterns

### Pattern 1: Basic Healthcare Desert Identification

Find counties with low provider access and high health needs.

```sql
-- Primary care deserts with health burden
WITH provider_access AS (
    SELECT 
        p.county_fips,
        COUNT(DISTINCT CASE 
            WHEN p.taxonomy_1 LIKE '207Q%' OR p.taxonomy_1 LIKE '207R%' 
            THEN p.npi END) as pcp_count,
        COUNT(DISTINCT p.npi) as total_providers
    FROM network.providers p
    WHERE p.entity_type_code = '1'
    GROUP BY p.county_fips
),
demographics AS (
    SELECT 
        sv.state,
        sv.county,
        sv.stcnty as county_fips,
        sv.e_totpop as population,
        sv.rpl_themes as svi_overall_percentile
    FROM population.svi_county sv
    WHERE sv.e_totpop >= 10000  -- Min population threshold
),
health_indicators AS (
    SELECT 
        p.locationid as county_fips,
        MAX(CASE WHEN p.measure = 'DIABETES' THEN CAST(p.data_value AS FLOAT) END) as diabetes_prev,
        MAX(CASE WHEN p.measure = 'CHD' THEN CAST(p.data_value AS FLOAT) END) as heart_disease_prev,
        MAX(CASE WHEN p.measure = 'COPD' THEN CAST(p.data_value AS FLOAT) END) as copd_prev
    FROM population.places_county p
    WHERE p.data_value_type = 'Age-adjusted prevalence'
    GROUP BY p.locationid
)
SELECT 
    d.state,
    d.county,
    d.population,
    COALESCE(pa.pcp_count, 0) as pcps,
    ROUND(COALESCE(pa.pcp_count, 0) * 100000.0 / d.population, 1) as pcps_per_100k,
    d.svi_overall_percentile,
    ROUND(hi.diabetes_prev, 1) as diabetes_prev,
    ROUND(hi.heart_disease_prev, 1) as heart_disease_prev,
    CASE 
        WHEN COALESCE(pa.pcp_count, 0) * 100000.0 / d.population < 20 
             AND d.svi_overall_percentile > 0.75 THEN 'Critical Desert'
        WHEN COALESCE(pa.pcp_count, 0) * 100000.0 / d.population < 40 
             AND d.svi_overall_percentile > 0.60 THEN 'Severe Desert'
        WHEN COALESCE(pa.pcp_count, 0) * 100000.0 / d.population < 60 THEN 'Moderate Desert'
        ELSE 'Adequate Access'
    END as desert_status
FROM demographics d
LEFT JOIN provider_access pa ON d.county_fips = pa.county_fips
LEFT JOIN health_indicators hi ON d.county_fips = hi.county_fips
WHERE COALESCE(pa.pcp_count, 0) * 100000.0 / d.population < 60  -- Below HRSA minimum
ORDER BY 
    COALESCE(pa.pcp_count, 0) * 100000.0 / d.population ASC,
    d.svi_overall_percentile DESC
LIMIT 30;
```

### Pattern 2: Mental Health Desert Analysis

Identify areas with mental health provider shortages and high need.

```sql
-- Mental health deserts with depression/suicide data
WITH mental_health_providers AS (
    SELECT 
        p.county_fips,
        COUNT(DISTINCT CASE WHEN p.taxonomy_1 LIKE '208000%' THEN p.npi END) as psychiatrists,
        COUNT(DISTINCT CASE WHEN p.taxonomy_1 LIKE '103T%' THEN p.npi END) as psychologists,
        COUNT(DISTINCT CASE WHEN p.taxonomy_1 LIKE '106H%' THEN p.npi END) as counselors
    FROM network.providers p
    WHERE p.entity_type_code = '1'
    GROUP BY p.county_fips
),
demographics AS (
    SELECT 
        sv.state,
        sv.county,
        sv.stcnty as county_fips,
        sv.e_totpop as population,
        sv.rpl_themes as svi_percentile
    FROM population.svi_county sv
    WHERE sv.e_totpop >= 20000
),
mental_health_indicators AS (
    SELECT 
        p.locationid as county_fips,
        MAX(CASE WHEN p.measure = 'DEPRESSION' THEN CAST(p.data_value AS FLOAT) END) as depression_prev,
        MAX(CASE WHEN p.measure = 'MHLTH' THEN CAST(p.data_value AS FLOAT) END) as poor_mental_health_days
    FROM population.places_county p
    WHERE p.data_value_type = 'Age-adjusted prevalence'
    GROUP BY p.locationid
)
SELECT 
    d.state,
    d.county,
    d.population,
    COALESCE(mh.psychiatrists, 0) as psychiatrists,
    COALESCE(mh.psychologists, 0) as psychologists,
    ROUND(COALESCE(mh.psychiatrists, 0) * 100000.0 / d.population, 1) as psychiatrists_per_100k,
    ROUND(mhi.depression_prev, 1) as depression_prev,
    ROUND(mhi.poor_mental_health_days, 1) as poor_mh_days,
    d.svi_percentile,
    CASE 
        WHEN COALESCE(mh.psychiatrists, 0) = 0 
             AND mhi.depression_prev > 20 THEN 'Critical Mental Health Desert'
        WHEN COALESCE(mh.psychiatrists, 0) * 100000.0 / d.population < 5 
             AND mhi.depression_prev > 18 THEN 'Severe Mental Health Desert'
        WHEN COALESCE(mh.psychiatrists, 0) * 100000.0 / d.population < 10 THEN 'Moderate Gap'
        ELSE 'Adequate'
    END as mental_health_desert_status,
    ROUND((COALESCE(mh.psychiatrists, 0) + COALESCE(mh.psychologists, 0) + COALESCE(mh.counselors, 0)) 
          * 100000.0 / d.population, 1) as total_mh_providers_per_100k
FROM demographics d
LEFT JOIN mental_health_providers mh ON d.county_fips = mh.county_fips
LEFT JOIN mental_health_indicators mhi ON d.county_fips = mhi.county_fips
WHERE COALESCE(mh.psychiatrists, 0) * 100000.0 / d.population < 15  -- Well below standard
ORDER BY 
    COALESCE(mh.psychiatrists, 0) * 100000.0 / d.population ASC,
    depression_prev DESC
LIMIT 25;
```

### Pattern 3: Maternity Care Desert Identification

Counties without OB/GYN access.

```sql
-- Maternity care deserts
WITH maternity_providers AS (
    SELECT 
        p.county_fips,
        COUNT(DISTINCT CASE WHEN p.taxonomy_1 LIKE '207V%' THEN p.npi END) as obgyn_count
    FROM network.providers p
    WHERE p.entity_type_code = '1'
    GROUP BY p.county_fips
),
maternity_facilities AS (
    SELECT 
        f.county_fips,
        COUNT(DISTINCT CASE WHEN f.type = '01' THEN f.ccn END) as hospitals_with_maternity
    FROM network.facilities f
    -- Note: Actual maternity capability would need additional data
    WHERE f.type = '01'
    GROUP BY f.county_fips
),
demographics AS (
    SELECT 
        sv.state,
        sv.county,
        sv.stcnty as county_fips,
        sv.e_totpop as population,
        sv.rpl_themes as svi_percentile
    FROM population.svi_county sv
    WHERE sv.e_totpop >= 15000
)
SELECT 
    d.state,
    d.county,
    d.population,
    COALESCE(mp.obgyn_count, 0) as obgyn_providers,
    COALESCE(mf.hospitals_with_maternity, 0) as maternity_hospitals,
    d.svi_percentile,
    CASE 
        WHEN COALESCE(mp.obgyn_count, 0) = 0 
             AND COALESCE(mf.hospitals_with_maternity, 0) = 0 THEN 'Complete Maternity Desert'
        WHEN COALESCE(mp.obgyn_count, 0) = 0 THEN 'No OB/GYN Providers'
        WHEN COALESCE(mf.hospitals_with_maternity, 0) = 0 THEN 'No Maternity Facilities'
        WHEN COALESCE(mp.obgyn_count, 0) * 100000.0 / d.population < 10 THEN 'Limited Access'
        ELSE 'Adequate'
    END as maternity_desert_status,
    CASE 
        WHEN COALESCE(mp.obgyn_count, 0) = 0 
             AND COALESCE(mf.hospitals_with_maternity, 0) = 0 
             AND d.svi_percentile > 0.75 THEN 'Critical Priority'
        WHEN COALESCE(mp.obgyn_count, 0) = 0 THEN 'High Priority'
        ELSE 'Medium Priority'
    END as recruitment_priority
FROM demographics d
LEFT JOIN maternity_providers mp ON d.county_fips = mp.county_fips
LEFT JOIN maternity_facilities mf ON d.county_fips = mf.county_fips
WHERE COALESCE(mp.obgyn_count, 0) = 0 
   OR COALESCE(mf.hospitals_with_maternity, 0) = 0
ORDER BY 
    CASE 
        WHEN COALESCE(mp.obgyn_count, 0) = 0 AND COALESCE(mf.hospitals_with_maternity, 0) = 0 THEN 1
        WHEN COALESCE(mp.obgyn_count, 0) = 0 THEN 2
        ELSE 3
    END,
    d.svi_percentile DESC
LIMIT 25;
```

### Pattern 4: Multi-Dimensional Desert Composite Score

Calculate comprehensive desert score across all dimensions.

```sql
-- Composite healthcare desert score
WITH provider_metrics AS (
    SELECT 
        p.county_fips,
        COUNT(DISTINCT CASE WHEN p.taxonomy_1 LIKE '207Q%' OR p.taxonomy_1 LIKE '207R%' THEN p.npi END) as pcps,
        COUNT(DISTINCT CASE WHEN p.taxonomy_1 LIKE '208000%' THEN p.npi END) as psychiatrists,
        COUNT(DISTINCT p.npi) as total_providers
    FROM network.providers p
    WHERE p.entity_type_code = '1'
    GROUP BY p.county_fips
),
facility_metrics AS (
    SELECT 
        f.county_fips,
        COUNT(DISTINCT CASE WHEN f.type = '01' THEN f.ccn END) as hospitals,
        COUNT(DISTINCT CASE WHEN hq.hospital_overall_rating IN ('4', '5') THEN f.ccn END) as quality_hospitals
    FROM network.facilities f
    LEFT JOIN network.hospital_quality hq ON f.ccn = hq.facility_id
    GROUP BY f.county_fips
),
demographics AS (
    SELECT 
        sv.state,
        sv.county,
        sv.stcnty as county_fips,
        sv.e_totpop as population,
        sv.rpl_themes as svi_overall,
        sv.ep_pov as poverty_rate,
        sv.ep_uninsur as uninsured_rate
    FROM population.svi_county sv
    WHERE sv.e_totpop >= 10000
),
health_burden AS (
    SELECT 
        p.locationid as county_fips,
        AVG(CASE WHEN p.measure IN ('DIABETES', 'CHD', 'COPD', 'CANCER', 'STROKE') 
            THEN CAST(p.data_value AS FLOAT) END) as avg_chronic_disease_prev,
        MAX(CASE WHEN p.measure = 'DEPRESSION' THEN CAST(p.data_value AS FLOAT) END) as depression_prev
    FROM population.places_county p
    WHERE p.data_value_type = 'Age-adjusted prevalence'
    GROUP BY p.locationid
)
SELECT 
    d.state,
    d.county,
    d.population,
    
    -- Provider Access Metrics
    COALESCE(pm.pcps, 0) as pcps,
    ROUND(COALESCE(pm.pcps, 0) * 100000.0 / d.population, 1) as pcps_per_100k,
    COALESCE(fm.hospitals, 0) as hospitals,
    COALESCE(fm.quality_hospitals, 0) as quality_hospitals,
    
    -- Social Vulnerability
    ROUND(d.svi_overall * 100, 1) as svi_percentile,
    ROUND(d.poverty_rate, 1) as poverty_rate,
    ROUND(d.uninsured_rate, 1) as uninsured_rate,
    
    -- Health Burden
    ROUND(hb.avg_chronic_disease_prev, 1) as avg_chronic_disease,
    ROUND(hb.depression_prev, 1) as depression_prev,
    
    -- Desert Scores (0-100 scale, higher = worse)
    ROUND(100 * (1 - LEAST(COALESCE(pm.pcps, 0) * 100000.0 / d.population / 80.0, 1)), 1) as access_gap_score,
    ROUND(d.svi_overall * 100, 1) as vulnerability_score,
    ROUND(COALESCE(hb.avg_chronic_disease_prev, 0) * 5, 1) as health_burden_score,
    ROUND(100 * (1 - COALESCE(fm.quality_hospitals, 0) / GREATEST(COALESCE(fm.hospitals, 1), 1)), 1) as quality_gap_score,
    
    -- Composite Desert Score
    ROUND(
        (100 * (1 - LEAST(COALESCE(pm.pcps, 0) * 100000.0 / d.population / 80.0, 1)) * 0.35) +
        (d.svi_overall * 100 * 0.25) +
        (COALESCE(hb.avg_chronic_disease_prev, 0) * 5 * 0.30) +
        (100 * (1 - COALESCE(fm.quality_hospitals, 0) / GREATEST(COALESCE(fm.hospitals, 1), 1)) * 0.10)
    , 1) as composite_desert_score,
    
    -- Desert Classification
    CASE 
        WHEN (
            (100 * (1 - LEAST(COALESCE(pm.pcps, 0) * 100000.0 / d.population / 80.0, 1)) * 0.35) +
            (d.svi_overall * 100 * 0.25) +
            (COALESCE(hb.avg_chronic_disease_prev, 0) * 5 * 0.30) +
            (100 * (1 - COALESCE(fm.quality_hospitals, 0) / GREATEST(COALESCE(fm.hospitals, 1), 1)) * 0.10)
        ) >= 80 THEN 'Critical Desert'
        WHEN (
            (100 * (1 - LEAST(COALESCE(pm.pcps, 0) * 100000.0 / d.population / 80.0, 1)) * 0.35) +
            (d.svi_overall * 100 * 0.25) +
            (COALESCE(hb.avg_chronic_disease_prev, 0) * 5 * 0.30) +
            (100 * (1 - COALESCE(fm.quality_hospitals, 0) / GREATEST(COALESCE(fm.hospitals, 1), 1)) * 0.10)
        ) >= 60 THEN 'Severe Desert'
        WHEN (
            (100 * (1 - LEAST(COALESCE(pm.pcps, 0) * 100000.0 / d.population / 80.0, 1)) * 0.35) +
            (d.svi_overall * 100 * 0.25) +
            (COALESCE(hb.avg_chronic_disease_prev, 0) * 5 * 0.30) +
            (100 * (1 - COALESCE(fm.quality_hospitals, 0) / GREATEST(COALESCE(fm.hospitals, 1), 1)) * 0.10)
        ) >= 40 THEN 'Moderate Desert'
        ELSE 'Adequate Access'
    END as desert_tier
    
FROM demographics d
LEFT JOIN provider_metrics pm ON d.county_fips = pm.county_fips
LEFT JOIN facility_metrics fm ON d.county_fips = fm.county_fips
LEFT JOIN health_burden hb ON d.county_fips = hb.county_fips
WHERE (
    (100 * (1 - LEAST(COALESCE(pm.pcps, 0) * 100000.0 / d.population / 80.0, 1)) * 0.35) +
    (d.svi_overall * 100 * 0.25) +
    (COALESCE(hb.avg_chronic_disease_prev, 0) * 5 * 0.30) +
    (100 * (1 - COALESCE(fm.quality_hospitals, 0) / GREATEST(COALESCE(fm.hospitals, 1), 1)) * 0.10)
) >= 40  -- Only show deserts
ORDER BY composite_desert_score DESC
LIMIT 30;
```

### Pattern 5: Equity-Focused Desert Analysis

Identify deserts disproportionately affecting vulnerable populations.

```sql
-- Healthcare deserts with equity lens
WITH provider_access AS (
    SELECT 
        p.county_fips,
        COUNT(DISTINCT CASE WHEN p.taxonomy_1 LIKE '207Q%' OR p.taxonomy_1 LIKE '207R%' THEN p.npi END) as pcp_count
    FROM network.providers p
    WHERE p.entity_type_code = '1'
    GROUP BY p.county_fips
),
demographics AS (
    SELECT 
        sv.state,
        sv.county,
        sv.stcnty as county_fips,
        sv.e_totpop as population,
        sv.rpl_themes as svi_overall,
        sv.ep_minrty as minority_pct,
        sv.ep_pov as poverty_rate,
        sv.ep_age65 as elderly_pct,
        sv.ep_age17 as children_pct,
        sv.ep_nohsdp as no_hs_diploma_pct,
        sv.ep_uninsur as uninsured_rate
    FROM population.svi_county sv
    WHERE sv.e_totpop >= 15000
),
health_indicators AS (
    SELECT 
        p.locationid as county_fips,
        MAX(CASE WHEN p.measure = 'DIABETES' THEN CAST(p.data_value AS FLOAT) END) as diabetes,
        MAX(CASE WHEN p.measure = 'BPHIGH' THEN CAST(p.data_value AS FLOAT) END) as hypertension,
        MAX(CASE WHEN p.measure = 'OBESITY' THEN CAST(p.data_value AS FLOAT) END) as obesity
    FROM population.places_county p
    WHERE p.data_value_type = 'Age-adjusted prevalence'
    GROUP BY p.locationid
)
SELECT 
    d.state,
    d.county,
    d.population,
    ROUND(d.minority_pct, 1) as minority_pct,
    ROUND(d.poverty_rate, 1) as poverty_rate,
    ROUND(d.uninsured_rate, 1) as uninsured_rate,
    COALESCE(pa.pcp_count, 0) as pcps,
    ROUND(COALESCE(pa.pcp_count, 0) * 100000.0 / d.population, 1) as pcps_per_100k,
    ROUND(hi.diabetes, 1) as diabetes_prev,
    ROUND(hi.obesity, 1) as obesity_prev,
    ROUND(d.svi_overall * 100, 1) as svi_percentile,
    CASE 
        WHEN d.minority_pct > 50 AND COALESCE(pa.pcp_count, 0) * 100000.0 / d.population < 40 
            THEN 'Minority Health Desert'
        WHEN d.poverty_rate > 20 AND COALESCE(pa.pcp_count, 0) * 100000.0 / d.population < 40 
            THEN 'Poverty Health Desert'
        WHEN d.elderly_pct > 15 AND COALESCE(pa.pcp_count, 0) * 100000.0 / d.population < 50 
            THEN 'Senior Health Desert'
        WHEN d.uninsured_rate > 15 AND COALESCE(pa.pcp_count, 0) * 100000.0 / d.population < 45 
            THEN 'Uninsured Health Desert'
        ELSE 'General Desert'
    END as equity_desert_type,
    CASE 
        WHEN d.svi_overall > 0.9 AND COALESCE(pa.pcp_count, 0) * 100000.0 / d.population < 30 
            THEN 'Extreme Inequity - Critical'
        WHEN d.svi_overall > 0.75 AND COALESCE(pa.pcp_count, 0) * 100000.0 / d.population < 40 
            THEN 'High Inequity - Severe'
        WHEN d.svi_overall > 0.60 AND COALESCE(pa.pcp_count, 0) * 100000.0 / d.population < 50 
            THEN 'Moderate Inequity'
        ELSE 'Lower Inequity'
    END as equity_impact_tier
FROM demographics d
LEFT JOIN provider_access pa ON d.county_fips = pa.county_fips
LEFT JOIN health_indicators hi ON d.county_fips = hi.county_fips
WHERE d.svi_overall > 0.60  -- Focus on vulnerable communities
  AND COALESCE(pa.pcp_count, 0) * 100000.0 / d.population < 60  -- Below HRSA minimum
ORDER BY d.svi_overall DESC, pcps_per_100k ASC
LIMIT 30;
```

---

## Examples

### Example 1: Identify Critical Healthcare Deserts in Texas

**Request**: "Show me the most critical healthcare deserts in Texas"

*Uses Pattern 1 query with state filter*

**Expected Output**:
```
state | county      | population | pcps | pcps_per_100k | svi_percentile | desert_status
------|-------------|------------|------|---------------|----------------|---------------
Texas | ZAVALA      | 11,677     | 2    | 17.1          | 92.3           | Critical Desert
Texas | DIMMIT      | 10,663     | 2    | 18.8          | 88.7           | Critical Desert
Texas | KENEDY      | 404        | 0    | 0.0           | 85.4           | Critical Desert
```

### Example 2: Mental Health Deserts Analysis

**Request**: "Find counties with mental health provider shortages and high depression rates"

*Uses Pattern 2 query*

**Expected Output**:
```
county          | population | psychiatrists | depression_prev | mental_health_desert_status
----------------|------------|---------------|-----------------|----------------------------
HIDALGO (TX)    | 860,661    | 0             | 21.3            | Critical Mental Health Desert
WEBB (TX)       | 276,652    | 1             | 20.8            | Severe Mental Health Desert
CAMERON (TX)    | 421,017    | 2             | 20.5            | Severe Mental Health Desert
```

### Example 3: Maternity Care Deserts

**Request**: "Identify counties without OB/GYN providers or maternity facilities"

*Uses Pattern 3 query*

**Expected Output**:
```
county        | population | obgyn_providers | maternity_hospitals | maternity_desert_status
--------------|------------|-----------------|---------------------|-------------------------
ZAVALA (TX)   | 11,677     | 0               | 0                   | Complete Maternity Desert
KENEDY (TX)   | 404        | 0               | 0                   | Complete Maternity Desert
LOVING (TX)   | 102        | 0               | 0                   | Complete Maternity Desert
```

---

## Desert Intervention Priorities

### Recruitment Priority Matrix

| Desert Severity | SVI Percentile | Population | Priority Level |
|-----------------|----------------|------------|----------------|
| Critical | >75 | >50K | **Immediate** |
| Critical | >75 | 25-50K | **Urgent** |
| Critical | 50-75 | >50K | **High** |
| Severe | >75 | >25K | **High** |
| Severe | 50-75 | >50K | **Medium** |
| Moderate | >75 | Any | **Medium** |

### Intervention Strategies by Desert Type

**Primary Care Deserts:**
- Residency programs in underserved areas
- Loan forgiveness for providers
- Telehealth infrastructure
- Community Health Centers (CHC)

**Mental Health Deserts:**
- Integrated behavioral health models
- Telepsychiatry expansion
- Community mental health centers
- School-based mental health services

**Maternity Deserts:**
- Regional birthing centers
- Midwifery programs
- Prenatal telehealth
- Emergency transport protocols

**Specialty Deserts:**
- Telemedicine specialist networks
- Visiting specialist clinics
- Hub-and-spoke models
- Academic medical center partnerships

---

## Integration with Other Skills

### With Network Adequacy
```sql
-- Combine desert identification with adequacy assessment
SELECT hd.county, hd.desert_tier, na.adequacy_pct, na.adequacy_status
FROM healthcare_deserts hd
JOIN network_adequacy na ON hd.county_fips = na.county_fips
WHERE hd.desert_tier IN ('Critical Desert', 'Severe Desert');
```

### With Provider Density
```sql
-- Desert analysis with density benchmarks
SELECT 
    hd.county,
    hd.composite_desert_score,
    pd.providers_per_100k,
    pd.density_tier
FROM healthcare_deserts hd
JOIN provider_density pd ON hd.county_fips = pd.county_fips
ORDER BY hd.composite_desert_score DESC;
```

### With Quality Analysis
```sql
-- Desert areas lacking quality providers
SELECT 
    hd.county,
    hd.desert_tier,
    hq.quality_hospital_count,
    hq.quality_adequacy_pct
FROM healthcare_deserts hd
LEFT JOIN hospital_quality_analysis hq ON hd.county_fips = hq.county_fips
WHERE hd.desert_tier = 'Critical Desert';
```

---

## Validation Rules

### Desert Classification Criteria
- Must have population >= 10,000 (configurable)
- Provider density < 60 per 100K (HRSA minimum)
- SVI data available for vulnerability scoring
- Health outcome data available for burden scoring

### Severity Thresholds
- **Critical**: Score >= 80 AND (no PCPs OR SVI > 90th percentile)
- **Severe**: Score >= 60 AND provider density < 40 per 100K
- **Moderate**: Score >= 40 AND provider density < 60 per 100K

### Data Quality Checks
- Verify county FIPS matching across datasets
- Validate population totals against Census
- Check for missing SVI or PLACES data
- Confirm provider location accuracy

---

## Performance Notes

- **Basic desert identification**: 100-200ms (state-level)
- **Mental health analysis**: 150-300ms (specialty filtering)
- **Composite scoring**: 300-600ms (multi-table aggregation)
- **Equity analysis**: 200-400ms (complex demographic JOINs)

**Optimization Tips**:
- Filter by population threshold early
- Index county_fips in all tables
- Pre-calculate SVI percentiles
- Cache specialty mappings
- Use CTEs for complex scoring

---

## Future Enhancements

1. **True Distance Calculations**
   - Drive time to nearest provider
   - Public transportation accessibility
   - Geographic barriers (mountains, water)

2. **Temporal Analysis**
   - Desert trend analysis over time
   - Provider retirement impact
   - Population growth projections

3. **Intervention Impact Modeling**
   - ROI of provider recruitment
   - Telehealth desert mitigation
   - CHC expansion effectiveness

4. **Advanced Health Indicators**
   - Preventable hospitalizations
   - ER utilization for primary care
   - Delayed diagnosis rates

5. **Demographic Granularity**
   - Census tract-level analysis
   - ZIP code-level deserts
   - Neighborhood-level equity

---

## Related Skills

- **[network-adequacy-analysis](network-adequacy-analysis.md)**: Regulatory compliance assessment
- **[provider-density](../query/provider-density.md)**: Provider per population calculations
- **[coverage-analysis](../query/coverage-analysis.md)**: Network coverage gaps
- **[hospital-quality-search](../query/hospital-quality-search.md)**: Quality-adjusted networks
- **[physician-quality-search](../query/physician-quality-search.md)**: Provider credential analysis

---

*Last Updated: December 27, 2025*  
*Version: 1.0.0*  
*Data Sources: NetworkSim, PopulationSim (SVI, PLACES)*
