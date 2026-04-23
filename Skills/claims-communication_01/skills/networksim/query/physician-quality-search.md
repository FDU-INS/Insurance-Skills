---
name: physician-quality-search
description: Search and filter physicians by quality metrics, credentials, board certification, and experience (framework for future metric integration)

Trigger phrases:
- "Find high-quality physicians in [specialty]"
- "Search for board-certified [specialty] providers"
- "Show physicians with [credential] in [location]"
- "Find experienced physicians for [condition]"
- "List top-performing physicians"
---

# Physician Quality Search Skill

## Overview

Framework for physician quality-based search and filtering. Current implementation focuses on credential validation and specialty expertise as quality proxies. Designed for expansion when CMS MIPS scores, patient satisfaction ratings, and clinical outcome metrics become available.

**Current Quality Indicators**:
- **Credentials**: MD, DO, NP, PA certification levels
- **Specialty Taxonomy**: Board certification specialties
- **Practice Affiliation**: Association with high-quality facilities
- **Geographic Presence**: Established practice locations

**Future Quality Metrics** (when available):
- **MIPS Composite Scores**: Merit-based Incentive Payment System
- **Patient Satisfaction**: CAHPS scores, online ratings
- **Clinical Outcomes**: Disease-specific performance measures
- **Cost Efficiency**: Resource utilization metrics

**Data Sources**: 
- `network.providers` (8.9M providers with credentials/taxonomy)
- `network.physician_quality` (1.5M NPIs, framework for metrics)
- `network.hospital_quality` (facility affiliation inference)

---

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| credential | string/array | No | Required credentials (MD, DO, NP, PA, etc.) |
| specialty | string/array | No | Taxonomy codes or specialty names |
| min_mips_score | number | No | Minimum MIPS score (future - when available) |
| board_certified | boolean | No | Board certification required (inferred from taxonomy) |
| hospital_affiliation | string | No | Associated hospital CCN or name |
| experience_years | integer | No | Minimum years in practice (future) |
| patient_rating | number | No | Minimum patient rating (future - when available) |

---

## Credential Hierarchy

### Physician Credentials (Independent Practice)
```
MD (Doctor of Medicine)           - Medical degree, 4 years med school + residency
DO (Doctor of Osteopathic Med)    - Medical degree, holistic approach
```

### Advanced Practice Providers
```
NP (Nurse Practitioner)           - Advanced nursing degree, independent in some states
PA (Physician Assistant)          - Medical training, supervised practice
```

### Specialty Credentials
```
FACP (Fellow, American College of Physicians) - Internal medicine expertise
FACS (Fellow, American College of Surgeons)   - Surgical expertise
FACOG (Fellow, American College of OB/GYN)    - OB/GYN expertise
```

---

## Query Patterns

### Pattern 1: Credential-Based Filtering

Filter providers by credential level and type.

```sql
-- Find board-certified physicians (MD/DO with specialty credentials)
SELECT 
    p.npi,
    p.first_name || ' ' || p.last_name as provider_name,
    p.credential,
    p.taxonomy_1 as primary_specialty,
    p.practice_city,
    p.practice_state
FROM network.providers p
WHERE p.credential IN ('M.D.', 'MD', 'D.O.', 'DO')
  AND p.taxonomy_1 LIKE '207%'  -- Physician specialties
  AND p.practice_state = 'CA'
  AND p.entity_type_code = '1'
ORDER BY p.last_name, p.first_name
LIMIT 100;
```

### Pattern 2: Specialty Expertise Filter

Focus on specific specialty board certifications.

```sql
-- Find cardiologists with MD/DO credentials
SELECT 
    p.npi,
    p.first_name || ' ' || p.last_name as provider_name,
    p.credential,
    p.taxonomy_1,
    p.practice_address_1 as address,
    p.practice_city || ', ' || p.practice_state as location,
    p.phone
FROM network.providers p
WHERE p.taxonomy_1 LIKE '207RC%'  -- Cardiology
  AND p.credential ~ 'M\\.?D\\.?|D\\.?O\\.?'  -- MD or DO variations
  AND p.practice_state IN ('TX', 'CA')
  AND p.entity_type_code = '1'
ORDER BY p.practice_state, p.practice_city, p.last_name
LIMIT 200;
```

### Pattern 3: Hospital Affiliation Quality (Conceptual)

Infer quality through association with high-rated hospitals.

```sql
-- Physicians practicing in same city as 5-star hospitals
SELECT 
    p.npi,
    p.first_name || ' ' || p.last_name as provider_name,
    p.credential,
    p.taxonomy_1,
    p.practice_city,
    p.practice_state,
    COUNT(DISTINCT hq.facility_id) as nearby_5star_hospitals
FROM network.providers p
INNER JOIN network.hospital_quality hq
    ON p.practice_city = hq.city_town
    AND p.practice_state = hq.state
    AND hq.hospital_overall_rating = '5'
WHERE p.entity_type_code = '1'
  AND p.credential ~ 'M\\.?D\\.?|D\\.?O\\.?'
  AND p.practice_state = 'CA'
GROUP BY p.npi, p.first_name, p.last_name, p.credential, 
         p.taxonomy_1, p.practice_city, p.practice_state
HAVING COUNT(DISTINCT hq.facility_id) > 0
ORDER BY nearby_5star_hospitals DESC, p.last_name
LIMIT 100;
```

### Pattern 4: Multi-Specialty Quality Roster

Build roster emphasizing credentials and specialization.

```sql
-- Quality-focused primary care roster (MD/DO with PCP specialties)
WITH pcp_credentials AS (
    SELECT 
        p.npi,
        p.first_name || ' ' || p.last_name as provider_name,
        p.credential,
        CASE 
            WHEN p.taxonomy_1 LIKE '207Q%' THEN 'Family Medicine'
            WHEN p.taxonomy_1 LIKE '207R%' THEN 'Internal Medicine'
            WHEN p.taxonomy_1 LIKE '208D%' THEN 'General Practice'
            ELSE 'Other Primary Care'
        END as specialty,
        p.practice_city,
        p.practice_state,
        p.phone
    FROM network.providers p
    WHERE (p.taxonomy_1 LIKE '207Q%' OR p.taxonomy_1 LIKE '207R%' OR p.taxonomy_1 LIKE '208D%')
      AND p.credential ~ 'M\\.?D\\.?|D\\.?O\\.?'
      AND p.practice_state = 'FL'
      AND p.entity_type_code = '1'
)
SELECT 
    specialty,
    COUNT(*) as provider_count,
    STRING_AGG(DISTINCT practice_state, ', ') as states,
    COUNT(DISTINCT practice_city) as cities_covered
FROM pcp_credentials
GROUP BY specialty
ORDER BY provider_count DESC;
```

### Pattern 5: Experience Proxy (NPI Distribution)

Use NPI number as rough proxy for experience (lower = earlier enrollment).

```sql
-- Find potentially experienced providers (earlier NPI enrollment)
-- NOTE: NPI number correlates loosely with enumeration date
SELECT 
    p.npi,
    p.first_name || ' ' || p.last_name as provider_name,
    p.credential,
    p.taxonomy_1,
    p.practice_city,
    p.practice_state,
    CAST(p.npi AS BIGINT) as npi_numeric
FROM network.providers p
WHERE p.taxonomy_1 LIKE '207RC%'  -- Cardiology
  AND p.credential ~ 'M\\.?D\\.?'
  AND p.practice_state = 'NY'
  AND p.entity_type_code = '1'
  AND CAST(p.npi AS BIGINT) < 1300000000  -- Earlier enrollees (pre-2007)
ORDER BY npi_numeric ASC
LIMIT 50;
```

---

## Examples

### Example 1: Find Board-Certified Cardiologists in Texas

**Request**: "Find board-certified cardiologists in Houston, Texas"

**Query**:
```sql
SELECT 
    p.npi,
    p.first_name || ' ' || p.last_name || ', ' || p.credential as provider,
    p.taxonomy_1 as taxonomy_code,
    p.practice_address_1 as address,
    p.practice_city,
    p.practice_zip,
    p.phone
FROM network.providers p
WHERE p.practice_city = 'HOUSTON'
  AND p.practice_state = 'TX'
  AND p.taxonomy_1 LIKE '207RC%'  -- Cardiology taxonomy
  AND p.credential ~ 'M\\.?D\\.?|D\\.?O\\.?'  -- Physician credentials
  AND p.entity_type_code = '1'
ORDER BY p.last_name, p.first_name
LIMIT 50;
```

**Expected Output**: Houston cardiologists with MD/DO credentials

**Sample**:
```
npi        | provider                | taxonomy_code | address         | city    | zip   | phone
-----------|-------------------------|---------------|-----------------|---------|-------|-------------
1234567890 | JOHN SMITH, M.D.        | 207RC0000X    | 123 Medical Dr  | HOUSTON | 77001 | (713)555-0100
1234567891 | JANE DOE, D.O.          | 207RC0000X    | 456 Heart Ave   | HOUSTON | 77002 | (713)555-0200
```

### Example 2: Quality-Focused PCP Network

**Request**: "Build primary care network with physician-level providers (exclude mid-levels)"

**Query**:
```sql
WITH physician_pcps AS (
    SELECT 
        p.npi,
        p.first_name || ' ' || p.last_name as provider_name,
        p.credential,
        CASE 
            WHEN p.taxonomy_1 LIKE '207Q%' THEN 'Family Medicine'
            WHEN p.taxonomy_1 LIKE '207R%' THEN 'Internal Medicine'
            WHEN p.taxonomy_1 LIKE '208D%' THEN 'General Practice'
        END as specialty,
        p.county_fips,
        p.practice_state
    FROM network.providers p
    WHERE (p.taxonomy_1 LIKE '207Q%' OR p.taxonomy_1 LIKE '207R%' OR p.taxonomy_1 LIKE '208D%')
      AND p.credential ~ 'M\\.?D\\.?|D\\.?O\\.?'  -- Physicians only
      AND p.practice_state IN ('CA', 'TX', 'NY')
      AND p.entity_type_code = '1'
)
SELECT 
    practice_state,
    specialty,
    COUNT(*) as physician_count,
    COUNT(DISTINCT county_fips) as counties_covered
FROM physician_pcps
GROUP BY practice_state, specialty
ORDER BY practice_state, specialty;
```

**Expected Output**: Physician-level PCP counts by state/specialty

### Example 3: Physicians Near High-Quality Hospitals

**Request**: "Find physicians practicing near 5-star hospitals in California"

**Query**:
```sql
SELECT 
    p.npi,
    p.first_name || ' ' || p.last_name as physician,
    p.credential,
    p.taxonomy_1,
    p.practice_city,
    hq.facility_name as nearby_5star_hospital,
    hq.hospital_overall_rating as hospital_rating
FROM network.providers p
INNER JOIN network.hospital_quality hq
    ON p.practice_city = hq.city_town
    AND p.practice_state = hq.state
WHERE hq.state = 'CA'
  AND hq.hospital_overall_rating = '5'
  AND p.credential ~ 'M\\.?D\\.?|D\\.?O\\.?'
  AND p.entity_type_code = '1'
ORDER BY p.practice_city, hq.facility_name, p.last_name
LIMIT 100;
```

**Expected Output**: Physicians in cities with 5-star hospitals

---

## MIPS Integration Framework (Future)

### Merit-Based Incentive Payment System

When MIPS data becomes available, extend queries with quality scoring:

```sql
-- FUTURE: Filter by MIPS composite score
SELECT 
    p.npi,
    p.first_name || ' ' || p.last_name as provider_name,
    p.credential,
    p.taxonomy_1,
    pq.mips_composite_score,  -- FUTURE FIELD
    pq.quality_score,          -- FUTURE FIELD
    pq.improvement_score,      -- FUTURE FIELD
    pq.cost_score             -- FUTURE FIELD
FROM network.providers p
INNER JOIN network.physician_quality pq ON p.npi = pq.npi
WHERE pq.mips_composite_score >= 75  -- High performers
  AND p.taxonomy_1 LIKE '207%'
  AND p.practice_state = 'CA'
ORDER BY pq.mips_composite_score DESC
LIMIT 100;
```

### Patient Satisfaction Integration

```sql
-- FUTURE: Filter by patient satisfaction ratings
SELECT 
    p.npi,
    p.first_name || ' ' || p.last_name as provider_name,
    pq.patient_satisfaction_score,  -- FUTURE FIELD
    pq.care_coordination_score,     -- FUTURE FIELD
    pq.communication_score          -- FUTURE FIELD
FROM network.providers p
INNER JOIN network.physician_quality pq ON p.npi = pq.npi
WHERE pq.patient_satisfaction_score >= 4.5  -- 5-point scale
  AND p.practice_state = 'TX'
ORDER BY pq.patient_satisfaction_score DESC;
```

---

## Quality Tiers (Conceptual Framework)

### Tier 1: Premium Physicians
- MD/DO credentials required
- Board certification in specialty
- MIPS score ≥75 (when available)
- Patient satisfaction ≥4.5/5 (when available)
- Association with 4-5 star hospitals

### Tier 2: High-Quality Physicians
- MD/DO or experienced NP/PA
- Specialty certification
- MIPS score ≥60 (when available)
- Patient satisfaction ≥4.0/5 (when available)
- Established practice (>5 years)

### Tier 3: Standard Physicians
- Appropriate credentials for role
- Specialty training
- MIPS score ≥40 (when available)
- No significant quality concerns

---

## Credential Validation Patterns

### Physician Validation
```sql
-- Strict physician filter
WHERE p.credential ~ 'M\\.?D\\.?|D\\.?O\\.?'
```

### Advanced Practice Provider Validation
```sql
-- Include APPs (NP, PA)
WHERE p.credential ~ 'M\\.?D\\.?|D\\.?O\\.?|N\\.?P\\.?|P\\.?A\\.?'
```

### Fellowship Credentials
```sql
-- Subspecialty fellowship training
WHERE p.credential LIKE '%FAC%'  -- FACP, FACS, FACOG, etc.
```

---

## Integration with Other Skills

### With Hospital Quality
```sql
-- Physicians affiliated with high-quality facilities
SELECT p.npi, p.first_name || ' ' || p.last_name as name,
       hq.facility_name, hq.hospital_overall_rating
FROM network.providers p
INNER JOIN network.hospital_quality hq 
    ON p.practice_city = hq.city_town AND p.practice_state = hq.state
WHERE hq.hospital_overall_rating IN ('4', '5')
  AND p.credential ~ 'M\\.?D\\.?';
```

### With Network Roster
```sql
-- Quality-filtered provider roster
SELECT npi, provider_name, credential, specialty
FROM (SELECT ...) WHERE credential ~ 'M\\.?D\\.?|D\\.?O\\.?';
```

---

## Validation Rules

### Credential Format
- Variations accepted: MD, M.D., MD., M.D, etc.
- Case-insensitive matching
- Regex patterns for flexibility

### Taxonomy Validation
- Must be valid NUCC taxonomy code
- Primary taxonomy (taxonomy_1) required
- Specialty alignment with credentials

### Data Quality
- NPI must be valid 10-digit
- Entity type '1' for individuals
- Practice location required

---

## Performance Notes

- **Credential filter**: <10ms
- **Specialty + credential**: 20-30ms
- **Hospital affiliation JOIN**: 50-100ms
- **Complex multi-filter**: 100-200ms

**Optimization Tips**:
- Use regex efficiently (pre-compile patterns)
- Filter by state before credentials
- Index on credential field
- Limit results appropriately

---

## Related Skills

- **[provider-search](provider-search.md)**: Basic provider search
- **[hospital-quality-search](hospital-quality-search.md)**: Facility quality
- **[network-roster](network-roster.md)**: Quality-tier rosters
- **[coverage-analysis](coverage-analysis.md)**: Quality-adjusted adequacy

---

## Future Enhancements

1. **MIPS Score Integration** (CMS physician quality payment program)
2. **Patient Satisfaction Data** (CAHPS, online ratings)
3. **Clinical Outcome Metrics** (disease-specific performance)
4. **Board Certification Verification** (ABMS integration)
5. **Malpractice History** (NPDB integration)
6. **Years in Practice** (calculated from NPI enumeration date)
7. **Practice Volume Metrics** (claims-based utilization)
8. **Peer Comparisons** (regional/national benchmarks)

---

*Last Updated: December 27, 2025*  
*Version: 1.0.0*  
*Status: Framework Ready for Metric Integration*
