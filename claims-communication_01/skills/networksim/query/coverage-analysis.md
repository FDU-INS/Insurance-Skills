---
name: coverage-analysis
description: Analyze network adequacy, identify specialty gaps, and generate compliance reports for regulatory requirements

Trigger phrases:
- "Analyze network coverage for [specialty] in [location]"
- "Check network adequacy in [state]"
- "Find coverage gaps for [specialty]"
- "Generate adequacy report for [network]"
- "Is my network adequate for [region]?"
---

# Coverage Analysis Skill

## Overview

Analyzes provider network adequacy and identifies coverage gaps using regulatory standards, industry benchmarks, and population health needs. Supports compliance with state and federal network adequacy requirements including time/distance standards, provider-to-enrollee ratios, and specialty availability.

**Key Analyses**:
- **Time/Distance Standards**: Geographic access requirements
- **Provider-to-Enrollee Ratios**: Minimum provider counts
- **Specialty Availability**: Required specialty types
- **Appointment Wait Times**: Access to care metrics (conceptual)
- **After-Hours Coverage**: Weekend/evening availability

**Regulatory Context**:
- CMS Medicare Advantage network adequacy standards
- State-specific Medicaid/Commercial requirements
- NCQA accreditation standards
- ACA essential community provider (ECP) requirements

---

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| network_id | string | No | Network roster to analyze |
| geography | object | Yes | State, county, or service area |
| enrollment | integer | No | Expected member enrollment |
| standard | string | No | 'cMS', 'ncqa', 'state' (default: 'cms') |
| specialty_requirements | array | No | Required specialty types |
| generate_report | boolean | No | Create compliance report (default: false) |

---

## Regulatory Standards

### CMS Medicare Advantage Time/Distance Standards

| Area Type | Primary Care | Specialists | Hospitals |
|-----------|--------------|-------------|-----------|
| Urban | 10 miles | 15 miles | 15 miles |
| Suburban | 20 miles | 30 miles | 30 miles |
| Rural | 30 miles | 60 miles | 60 miles |

### CMS Provider-to-Enrollee Ratios

| Specialty | Minimum Ratio |
|-----------|---------------|
| Primary Care | 1 PCP : 1,200 enrollees |
| OB/GYN | 1 : 2,000 enrollees |
| Mental Health | 1 : 3,000 enrollees |
| General Surgery | 1 : 5,000 enrollees |

### NCQA Essential Specialty Categories

1. Primary Care (Family Medicine, Internal Medicine, Pediatrics)
2. Cardiology
3. Dermatology
4. Endocrinology
5. Gastroenterology
6. General Surgery
7. Neurology
8. OB/GYN
9. Ophthalmology
10. Orthopedic Surgery
11. Otolaryngology (ENT)
12. Psychiatry
13. Urology

---

## Query Patterns

### Pattern 1: Basic Coverage Assessment by County

Identify counties with adequate vs inadequate coverage.

```sql
-- County-level coverage assessment
WITH county_coverage AS (
    SELECT 
        sv.stcnty as county_fips,
        sv.county,
        sv.state,
        sv.e_totpop as population,
        COUNT(DISTINCT CASE 
            WHEN p.taxonomy_1 LIKE '207Q%' OR p.taxonomy_1 LIKE '207R%' 
            THEN p.npi 
        END) as pcp_count,
        COUNT(DISTINCT CASE WHEN p.taxonomy_1 LIKE '207RC%' THEN p.npi END) as cardio_count,
        COUNT(DISTINCT CASE WHEN p.taxonomy_1 LIKE '207T%' THEN p.npi END) as psych_count,
        ROUND(100000.0 * COUNT(DISTINCT CASE 
            WHEN p.taxonomy_1 LIKE '207Q%' OR p.taxonomy_1 LIKE '207R%' 
            THEN p.npi 
        END) / NULLIF(sv.e_totpop, 0), 2) as pcp_per_100k
    FROM population.svi_county sv
    LEFT JOIN network.providers p ON sv.stcnty = p.county_fips
    WHERE sv.state = 'Texas'
      AND sv.e_totpop >= 10000
      AND (p.entity_type_code = '1' OR p.entity_type_code IS NULL)
    GROUP BY sv.stcnty, sv.county, sv.state, sv.e_totpop
)
SELECT 
    county,
    state,
    population,
    pcp_count,
    cardio_count,
    psych_count,
    pcp_per_100k,
    CASE 
        WHEN pcp_count >= CEILING(population / 1200.0) THEN '✓ Adequate'
        WHEN pcp_count >= CEILING(population / 2000.0) THEN '⚠ Below Target'
        ELSE '✗ Inadequate'
    END as pcp_coverage_status,
    CEILING(population / 1200.0) - pcp_count as pcp_gap
FROM county_coverage
ORDER BY pcp_coverage_status DESC, pcp_gap DESC
LIMIT 50;
```

### Pattern 2: Specialty Gap Analysis

Identify missing or underrepresented specialties.

```sql
-- NCQA specialty coverage gap analysis
WITH required_specialties AS (
    SELECT specialty_name, taxonomy_pattern, min_per_100k
    FROM (VALUES
        ('Primary Care', '207Q%|207R%|208D%', 60),
        ('Cardiology', '207RC%', 5),
        ('Dermatology', '207N%', 3),
        ('Endocrinology', '207RE%', 2),
        ('Gastroenterology', '207RG%', 3),
        ('General Surgery', '208600%', 4),
        ('OB/GYN', '207V%', 10),
        ('Orthopedic Surgery', '207X%', 5),
        ('Psychiatry', '207T%', 10)
    ) AS specs(specialty_name, taxonomy_pattern, min_per_100k)
),
state_specialty_counts AS (
    SELECT 
        p.practice_state,
        SUM(CASE WHEN sv.e_totpop IS NOT NULL THEN sv.e_totpop ELSE 0 END) as total_population,
        COUNT(DISTINCT CASE WHEN p.taxonomy_1 ~ '207Q|207R|208D' THEN p.npi END) as primary_care,
        COUNT(DISTINCT CASE WHEN p.taxonomy_1 LIKE '207RC%' THEN p.npi END) as cardiology,
        COUNT(DISTINCT CASE WHEN p.taxonomy_1 LIKE '207N%' THEN p.npi END) as dermatology,
        COUNT(DISTINCT CASE WHEN p.taxonomy_1 LIKE '207RE%' THEN p.npi END) as endocrinology,
        COUNT(DISTINCT CASE WHEN p.taxonomy_1 LIKE '207RG%' THEN p.npi END) as gastroenterology,
        COUNT(DISTINCT CASE WHEN p.taxonomy_1 LIKE '208600%' THEN p.npi END) as general_surgery,
        COUNT(DISTINCT CASE WHEN p.taxonomy_1 LIKE '207V%' THEN p.npi END) as obgyn,
        COUNT(DISTINCT CASE WHEN p.taxonomy_1 LIKE '207X%' THEN p.npi END) as orthopedic,
        COUNT(DISTINCT CASE WHEN p.taxonomy_1 LIKE '207T%' THEN p.npi END) as psychiatry
    FROM network.providers p
    LEFT JOIN population.svi_county sv ON p.county_fips = sv.stcnty
    WHERE p.practice_state = 'CA'
      AND p.entity_type_code = '1'
    GROUP BY p.practice_state
)
SELECT 
    'California' as state,
    'Primary Care' as specialty,
    primary_care as provider_count,
    ROUND(100000.0 * primary_care / NULLIF(total_population, 0), 2) as per_100k,
    60 as benchmark,
    CASE 
        WHEN ROUND(100000.0 * primary_care / NULLIF(total_population, 0), 2) >= 60 THEN '✓ Adequate'
        ELSE '✗ Gap: ' || (60 - ROUND(100000.0 * primary_care / NULLIF(total_population, 0), 2))::text
    END as status
FROM state_specialty_counts

UNION ALL

SELECT 
    'California', 'Cardiology', cardiology,
    ROUND(100000.0 * cardiology / NULLIF(total_population, 0), 2), 5,
    CASE WHEN ROUND(100000.0 * cardiology / NULLIF(total_population, 0), 2) >= 5 THEN '✓ Adequate'
         ELSE '✗ Gap: ' || (5 - ROUND(100000.0 * cardiology / NULLIF(total_population, 0), 2))::text
    END
FROM state_specialty_counts

-- Repeat for other specialties...
ORDER BY status DESC, specialty;
```

### Pattern 3: Network Adequacy Score

Calculate overall network adequacy score.

```sql
-- Comprehensive network adequacy scoring
WITH network_metrics AS (
    SELECT 
        COUNT(DISTINCT p.county_fips) as counties_covered,
        (SELECT COUNT(DISTINCT stcnty) FROM population.svi_county WHERE state = 'California') as total_counties,
        COUNT(DISTINCT p.npi) as total_providers,
        COUNT(DISTINCT CASE WHEN p.taxonomy_1 ~ '207Q|207R|208D' THEN p.npi END) as pcp_count,
        COUNT(DISTINCT CASE WHEN p.taxonomy_1 LIKE '207RC%' THEN p.npi END) as cardio_count,
        COUNT(DISTINCT CASE WHEN p.taxonomy_1 LIKE '207V%' THEN p.npi END) as obgyn_count,
        COUNT(DISTINCT CASE WHEN p.taxonomy_1 LIKE '207T%' THEN p.npi END) as psych_count,
        SUM(sv.e_totpop) as network_population
    FROM network.providers p
    LEFT JOIN population.svi_county sv ON p.county_fips = sv.stcnty
    WHERE p.practice_state = 'California'
      AND p.entity_type_code = '1'
)
SELECT 
    -- Geographic Coverage Score (40%)
    ROUND(40.0 * counties_covered / NULLIF(total_counties, 0), 1) as geographic_score,
    
    -- Provider Availability Score (30%)
    ROUND(30.0 * LEAST(1.0, pcp_count / NULLIF(CEILING(network_population / 1200.0), 0)), 1) as availability_score,
    
    -- Specialty Diversity Score (30%)
    ROUND(30.0 * (
        CASE WHEN pcp_count > 0 THEN 0.4 ELSE 0 END +
        CASE WHEN cardio_count > 0 THEN 0.2 ELSE 0 END +
        CASE WHEN obgyn_count > 0 THEN 0.2 ELSE 0 END +
        CASE WHEN psych_count > 0 THEN 0.2 ELSE 0 END
    ), 1) as specialty_score,
    
    -- Overall Adequacy Score
    ROUND(
        40.0 * counties_covered / NULLIF(total_counties, 0) +
        30.0 * LEAST(1.0, pcp_count / NULLIF(CEILING(network_population / 1200.0), 0)) +
        30.0 * (
            CASE WHEN pcp_count > 0 THEN 0.4 ELSE 0 END +
            CASE WHEN cardio_count > 0 THEN 0.2 ELSE 0 END +
            CASE WHEN obgyn_count > 0 THEN 0.2 ELSE 0 END +
            CASE WHEN psych_count > 0 THEN 0.2 ELSE 0 END
        )
    , 1) as overall_score,
    
    counties_covered,
    total_counties,
    total_providers,
    network_population
FROM network_metrics;
```

### Pattern 4: Essential Community Provider (ECP) Coverage

Assess availability of safety-net providers.

```sql
-- ECP coverage analysis (FQHCs, Rural Health Clinics)
SELECT 
    f.state,
    COUNT(DISTINCT CASE WHEN f.type = '50' THEN f.ccn END) as fqhc_count,
    COUNT(DISTINCT CASE WHEN f.type = '09' THEN f.ccn END) as rhc_count,
    COUNT(DISTINCT CASE WHEN f.type = '01' AND f.name LIKE '%CRITICAL ACCESS%' THEN f.ccn END) as cah_count,
    sv.total_population,
    ROUND(100000.0 * COUNT(DISTINCT CASE WHEN f.type = '50' THEN f.ccn END) / 
          NULLIF(sv.total_population, 0), 2) as fqhc_per_100k
FROM network.facilities f
LEFT JOIN (
    SELECT state, SUM(e_totpop) as total_population
    FROM population.svi_county
    WHERE state = 'Texas'
    GROUP BY state
) sv ON f.state = (SELECT stateabbr FROM population.places_county WHERE stateabbr = 'TX' LIMIT 1)
WHERE f.state = 'TX'
GROUP BY f.state, sv.total_population;
```

### Pattern 5: Cross-Product Gap Analysis

Identify coverage gaps correlated with health needs.

```sql
-- Coverage gaps in high-need areas
WITH coverage_needs AS (
    SELECT 
        pc.countyfips,
        pc.countyname,
        pc.stateabbr,
        pc.totalpopulation,
        pc.diabetes_crudeprev,
        pc.obesity_crudeprev,
        pc.access2_crudeprev as no_doctor_visit_rate,
        COUNT(DISTINCT p.npi) as provider_count,
        ROUND(100000.0 * COUNT(DISTINCT p.npi) / NULLIF(pc.totalpopulation, 0), 2) as providers_per_100k,
        sv.rpl_themes as social_vulnerability
    FROM population.places_county pc
    LEFT JOIN population.svi_county sv ON pc.countyfips = sv.stcnty
    LEFT JOIN network.providers p ON pc.countyfips = p.county_fips
    WHERE pc.stateabbr = 'MS'  -- Mississippi example
      AND pc.totalpopulation >= 15000
      AND (p.entity_type_code = '1' OR p.entity_type_code IS NULL)
    GROUP BY pc.countyfips, pc.countyname, pc.stateabbr, pc.totalpopulation,
             pc.diabetes_crudeprev, pc.obesity_crudeprev, pc.access2_crudeprev,
             sv.rpl_themes
)
SELECT 
    countyname,
    stateabbr,
    totalpopulation,
    provider_count,
    providers_per_100k,
    diabetes_crudeprev as diabetes_rate,
    no_doctor_visit_rate,
    social_vulnerability,
    CASE 
        WHEN providers_per_100k < 50 AND diabetes_crudeprev > 13 AND social_vulnerability > 0.75 
        THEN 'CRITICAL - High Need, Low Access'
        WHEN providers_per_100k < 70 AND diabetes_crudeprev > 11 
        THEN 'HIGH PRIORITY'
        WHEN providers_per_100k < 90 
        THEN 'MONITOR'
        ELSE 'ADEQUATE'
    END as priority_classification,
    GREATEST(0, 80 - providers_per_100k) as provider_gap_per_100k
FROM coverage_needs
ORDER BY 
    CASE priority_classification
        WHEN 'CRITICAL - High Need, Low Access' THEN 1
        WHEN 'HIGH PRIORITY' THEN 2
        WHEN 'MONITOR' THEN 3
        ELSE 4
    END,
    providers_per_100k ASC;
```

---

## Examples

### Example 1: Network Adequacy Report for Texas

**Request**: "Generate network adequacy report for Texas focusing on primary care"

**Query**:
```sql
WITH tx_coverage AS (
    SELECT 
        sv.county,
        sv.state,
        sv.e_totpop as population,
        COUNT(DISTINCT p.npi) as pcp_count,
        ROUND(100000.0 * COUNT(DISTINCT p.npi) / NULLIF(sv.e_totpop, 0), 2) as pcp_per_100k,
        CEILING(sv.e_totpop / 1200.0) as target_pcps,
        CEILING(sv.e_totpop / 1200.0) - COUNT(DISTINCT p.npi) as pcp_gap
    FROM population.svi_county sv
    LEFT JOIN network.providers p ON sv.stcnty = p.county_fips
    WHERE sv.state = 'Texas'
      AND sv.e_totpop >= 10000
      AND (p.taxonomy_1 LIKE '207Q%' OR p.taxonomy_1 LIKE '207R%' OR p.taxonomy_1 LIKE '208D%')
      AND (p.entity_type_code = '1' OR p.entity_type_code IS NULL)
    GROUP BY sv.county, sv.state, sv.e_totpop
)
SELECT 
    -- Summary Statistics
    COUNT(*) as counties_analyzed,
    SUM(population) as total_population,
    SUM(pcp_count) as total_pcps,
    SUM(target_pcps) as target_pcps,
    SUM(pcp_gap) as total_gap,
    ROUND(AVG(pcp_per_100k), 2) as avg_density,
    COUNT(CASE WHEN pcp_gap > 0 THEN 1 END) as counties_with_gaps,
    ROUND(100.0 * COUNT(CASE WHEN pcp_gap > 0 THEN 1 END) / COUNT(*), 1) as pct_inadequate
FROM tx_coverage

UNION ALL

-- Top 10 Counties with Largest Gaps
SELECT 
    county,
    population,
    pcp_count,
    target_pcps,
    pcp_gap,
    pcp_per_100k,
    NULL,
    NULL
FROM tx_coverage
WHERE pcp_gap > 0
ORDER BY pcp_gap DESC
LIMIT 10;
```

**Expected Output**: Summary statistics + list of counties needing additional PCPs

### Example 2: Multi-Specialty Compliance Check

**Request**: "Check if California network meets NCQA specialty requirements"

**Query**:
```sql
WITH ca_population AS (
    SELECT SUM(e_totpop) as total_pop
    FROM population.svi_county
    WHERE state = 'California'
),
specialty_counts AS (
    SELECT 
        COUNT(DISTINCT CASE WHEN taxonomy_1 ~ '207Q|207R|208D' THEN npi END) as primary_care,
        COUNT(DISTINCT CASE WHEN taxonomy_1 LIKE '207RC%' THEN npi END) as cardiology,
        COUNT(DISTINCT CASE WHEN taxonomy_1 LIKE '207N%' THEN npi END) as dermatology,
        COUNT(DISTINCT CASE WHEN taxonomy_1 LIKE '207V%' THEN npi END) as obgyn,
        COUNT(DISTINCT CASE WHEN taxonomy_1 LIKE '207X%' THEN npi END) as orthopedic,
        COUNT(DISTINCT CASE WHEN taxonomy_1 LIKE '207T%' THEN npi END) as psychiatry
    FROM network.providers
    WHERE practice_state = 'CA' AND entity_type_code = '1'
)
SELECT 
    'Primary Care' as specialty,
    primary_care as provider_count,
    ROUND(100000.0 * primary_care / total_pop, 2) as per_100k,
    60.0 as benchmark,
    ROUND(100000.0 * primary_care / total_pop, 2) >= 60 as meets_standard
FROM specialty_counts, ca_population

UNION ALL

SELECT 'Cardiology', cardiology,
    ROUND(100000.0 * cardiology / total_pop, 2), 5.0,
    ROUND(100000.0 * cardiology / total_pop, 2) >= 5
FROM specialty_counts, ca_population

-- Continue for all NCQA-required specialties...
;
```

### Example 3: Gap-Focused Recruitment Strategy

**Request**: "Where should we recruit providers to improve network adequacy?"

**Query**:
```sql
WITH recruitment_priorities AS (
    SELECT 
        sv.county,
        sv.state,
        sv.stcnty as county_fips,
        sv.e_totpop as population,
        pc.diabetes_crudeprev,
        COUNT(DISTINCT p.npi) as current_providers,
        CEILING(sv.e_totpop / 1200.0) as target_pcps,
        CEILING(sv.e_totpop / 1200.0) - COUNT(DISTINCT p.npi) as recruitment_need,
        ROUND(100000.0 * COUNT(DISTINCT p.npi) / NULLIF(sv.e_totpop, 0), 2) as current_density
    FROM population.svi_county sv
    LEFT JOIN population.places_county pc ON sv.stcnty = pc.countyfips
    LEFT JOIN network.providers p ON sv.stcnty = p.county_fips 
        AND (p.taxonomy_1 LIKE '207Q%' OR p.taxonomy_1 LIKE '207R%')
        AND p.entity_type_code = '1'
    WHERE sv.state = 'Florida'
      AND sv.e_totpop >= 20000
    GROUP BY sv.county, sv.state, sv.stcnty, sv.e_totpop, pc.diabetes_crudeprev
)
SELECT 
    county,
    state,
    population,
    current_providers,
    target_pcps,
    recruitment_need,
    current_density,
    diabetes_crudeprev,
    CASE 
        WHEN recruitment_need >= 10 AND diabetes_crudeprev > 11 THEN '🔴 Urgent - High Need'
        WHEN recruitment_need >= 5 THEN '🟡 Priority'
        WHEN recruitment_need > 0 THEN '🟢 Monitor'
        ELSE '✓ Adequate'
    END as priority_level
FROM recruitment_priorities
WHERE recruitment_need > 0
ORDER BY 
    CASE 
        WHEN recruitment_need >= 10 AND diabetes_crudeprev > 11 THEN 1
        WHEN recruitment_need >= 5 THEN 2
        ELSE 3
    END,
    recruitment_need DESC
LIMIT 30;
```

**Expected Output**: Prioritized list of counties for provider recruitment

---

## Compliance Reporting

### Network Adequacy Certification Template

```markdown
# Network Adequacy Certification
**Plan**: [Plan Name]
**Service Area**: [State/Counties]
**Effective Date**: [Date]

## Executive Summary
- Total Providers: X,XXX
- Counties Covered: XX of XX (XX%)
- Primary Care Ratio: XX.X per 100K (Target: 60)
- Overall Adequacy Score: XX%

## Specialty Coverage
| Specialty | Count | Per 100K | Standard | Status |
|-----------|-------|----------|----------|--------|
| Primary Care | XXX | XX.X | 60 | ✓/✗ |
| Cardiology | XXX | XX.X | 5 | ✓/✗ |
...

## Geographic Access
- Urban Areas: XX% within 10 miles of PCP
- Suburban Areas: XX% within 20 miles of PCP
- Rural Areas: XX% within 30 miles of PCP

## Identified Gaps
1. [County]: Needs X additional PCPs
2. [County]: Missing cardiology coverage
...

## Remediation Plan
- Recruit X providers in [locations]
- Contract with [facilities] for specialty coverage
- Timeline: [dates]
```

---

## Validation Rules

### Data Requirements
- Minimum 12 months of provider data
- Population data must be current
- All counties in service area must be analyzed
- Provider counts verified against NPPES

### Adequacy Thresholds
- PCP ratio: ≥60 per 100K (or state-specific)
- Geographic access: 90% within time/distance standards
- Specialty availability: All NCQA categories represented
- ECP participation: ≥30% of network

---

## Performance Notes

- **State-level analysis**: 100-200ms
- **County-level (full state)**: 300-600ms
- **Comprehensive adequacy score**: 500ms-1s
- **Gap analysis with PopulationSim**: 800ms-1.5s

---

## Related Skills

- **[provider-density](provider-density.md)**: Calculate density metrics
- **[network-roster](network-roster.md)**: Generate compliant rosters
- **[provider-search](provider-search.md)**: Find providers for gaps

---

## Future Enhancements

1. **Geospatial distance calculations** for time/distance standards
2. **Appointment availability** integration
3. **Cultural/linguistic competency** assessment
4. **Telehealth** impact on access calculations
5. **Provider capacity modeling** (patient panel sizes)
6. **Multi-year trend analysis**

---

*Last Updated: December 27, 2025*  
*Version: 1.0.0*
