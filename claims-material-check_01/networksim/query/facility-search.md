---
name: facility-search
description: Search for healthcare facilities including hospitals, nursing homes, and outpatient centers using CMS Provider of Services data

Trigger phrases:
- "Find hospitals in [location]"
- "Search for nursing homes in [state]"
- "Locate facilities near [city]"
- "Show me hospitals with [beds] beds"
- "Find [facility type] in [county]"
---

# Facility Search Skill

## Overview

Searches the CMS Provider of Services (POS) database for healthcare facilities including hospitals, skilled nursing facilities, home health agencies, and outpatient centers. Data includes bed counts, ownership types, and facility characteristics.

**Data Source**: `network.facilities` table (77,302 facilities)  
**Quality Data**: `network.hospital_quality` table (5,421 hospitals with CMS ratings)

---

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| facility_type | string | No | Type of facility (Hospital, Nursing Home, etc.) |
| location | object | No | Geographic search criteria |
| location.state | string | No | Two-letter state code |
| location.city | string | No | City name |
| location.zip | string | No | ZIP code |
| beds | object | No | Bed count criteria |
| beds.min | integer | No | Minimum bed count |
| beds.max | integer | No | Maximum bed count |
| ownership | string | No | Ownership type filter |
| quality_rating | integer | No | Minimum CMS star rating (1-5) |
| limit | integer | No | Max results (default: 50) |

---

## Query Patterns

### Pattern 1: Basic Facility Type Search

Search for facilities by type and location.

```sql
-- Find all short-term hospitals in California
SELECT 
    f.ccn,
    f.name AS facility_name,
    f.type,
    f.subtype,
    f.city,
    f.state,
    f.zip,
    f.beds,
    f.phone
FROM network.facilities f
WHERE f.state = 'CA'
  AND f.type = '01'  -- Short-term hospital
ORDER BY f.city, f.name
LIMIT 100;
```

### Pattern 2: Bed Count Filter

Search for facilities within a specific size range.

```sql
-- Find large hospitals (500+ beds) in major metros
SELECT 
    f.ccn,
    f.name,
    f.city,
    f.state,
    f.beds,
    f.type,
    f.subtype
FROM network.facilities f
WHERE f.type IN ('01', '17')  -- Short-term hospitals and Critical Access Hospitals
  AND f.beds >= 500
  AND f.state IN ('CA', 'NY', 'TX', 'FL', 'IL')
ORDER BY f.beds DESC, f.state, f.name
LIMIT 50;
```

### Pattern 3: Quality-Based Search

Search for highly-rated hospitals using CMS Hospital Compare data.

```sql
-- Find 5-star hospitals with full contact info
SELECT 
    f.ccn,
    f.name AS facility_name,
    f.city,
    f.state,
    f.beds,
    hq.hospital_overall_rating AS star_rating,
    hq.hospital_overall_rating_footnote AS rating_notes,
    f.phone
FROM network.facilities f
INNER JOIN network.hospital_quality hq ON f.ccn = hq.facility_id
WHERE hq.hospital_overall_rating = '5'
ORDER BY f.state, f.city, f.name
LIMIT 100;
```

### Pattern 4: Facility Type Distribution

Analyze facility types across states or regions.

```sql
-- Count facilities by type and state
SELECT 
    f.state,
    f.type,
    COUNT(*) AS facility_count,
    SUM(f.beds) AS total_beds,
    ROUND(AVG(f.beds), 1) AS avg_beds
FROM network.facilities f
WHERE f.state IN ('CA', 'TX', 'FL', 'NY')
  AND f.beds IS NOT NULL
GROUP BY f.state, f.type
ORDER BY f.state, facility_count DESC;
```

### Pattern 5: Cross-Product - Facilities in Underserved Areas

Find facilities in high-vulnerability counties with provider shortages.

```sql
-- Identify facilities in high-need counties
SELECT 
    sv.county AS county_name,
    sv.state AS state_abbr,
    sv.rpl_themes AS vulnerability_index,
    COUNT(DISTINCT f.ccn) AS facilities,
    SUM(f.beds) AS total_beds,
    COUNT(DISTINCT p.npi) AS providers
FROM population.svi_county sv
LEFT JOIN network.facilities f ON sv.stcnty = f.ccn  -- Note: needs county_fips on facilities
LEFT JOIN network.providers p ON sv.stcnty = p.county_fips
WHERE sv.rpl_themes > 0.75  -- High vulnerability
  AND sv.e_totpop > 50000   -- Significant population
GROUP BY sv.county, sv.state, sv.rpl_themes
HAVING COUNT(DISTINCT f.ccn) < 5  -- Few facilities
ORDER BY vulnerability_index DESC, sv.e_totpop DESC
LIMIT 20;
```

---

## Examples

### Example 1: Find Teaching Hospitals in Massachusetts

**Request**: "Find teaching hospitals in Massachusetts"

**Parameters**:
- State: MA
- Type: 01 (Short-term hospital)
- Filter: Teaching hospitals (by name)

**Query**:
```sql
SELECT 
    f.ccn,
    f.name,
    f.city,
    f.beds,
    f.subtype,
    hq.hospital_overall_rating AS rating,
    f.phone
FROM network.facilities f
LEFT JOIN network.hospital_quality hq ON f.ccn = hq.facility_id
WHERE f.state = 'MA'
  AND f.type = '01'  -- Short-term hospital
  AND (f.name ILIKE '%university%'
       OR f.name ILIKE '%medical center%'
       OR f.name ILIKE '%teaching%')
ORDER BY f.beds DESC, f.name
LIMIT 25;
```

**Expected Output**: Major academic medical centers in Massachusetts

**Sample Result**:
```
ccn     | name                              | city      | beds | subtype  | rating | phone
--------|-----------------------------------|-----------|------|----------|--------|---------------
220071  | Massachusetts General Hospital    | Boston    | 999  | Teaching | 5      | 617-726-2000
220140  | Brigham and Women's Hospital      | Boston    | 793  | Teaching | 5      | 617-732-5500
```

### Example 2: Find Skilled Nursing Facilities in Miami-Dade County

**Request**: "Find nursing homes in Miami with 100+ beds"

**Parameters**:
- City: Miami
- Type: 11 (Skilled Nursing Facility)
- Beds: ≥100

**Query**:
```sql
SELECT 
    f.ccn,
    f.name,
    f.city,
    f.zip,
    f.beds,
    f.phone
FROM network.facilities f
WHERE f.state = 'FL'
  AND (f.city ILIKE '%miami%' OR f.city = 'Miami')
  AND f.type = '11'  -- Skilled Nursing Facility
  AND f.beds >= 100
ORDER BY f.beds DESC, f.name
LIMIT 30;
```

**Expected Output**: Large nursing homes in Miami area

### Example 3: Quality Rating Distribution Analysis

**Request**: "Show me the distribution of hospital quality ratings in Texas"

**Query**:
```sql
SELECT 
    hq.hospital_overall_rating AS star_rating,
    COUNT(*) AS hospital_count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS percentage
FROM network.hospital_quality hq
JOIN network.facilities f ON hq.facility_id = f.ccn
WHERE f.state = 'TX'
  AND hq.hospital_overall_rating IS NOT NULL
GROUP BY hq.hospital_overall_rating
ORDER BY star_rating DESC;
```

**Expected Output**:
```
star_rating | hospital_count | percentage
------------|----------------|------------
5           | 45             | 12.50
4           | 98             | 27.22
3           | 135            | 37.50
2           | 61             | 16.94
1           | 21             | 5.83
```

---

## Facility Type Codes Reference

CMS Provider of Services (POS) type codes:

| Code | Description | Typical Bed Range | Count |
|------|-------------|-------------------|-------|
| 01 | Short-Term Hospital (General Acute Care) | 25-1000+ | 13,501 |
| 06 | Psychiatric Hospital | 20-500 | 713 |
| 07 | Physical Rehabilitation Hospital | N/A | 1,726 |
| 08 | Hospice | Varies | 7,580 |
| 09 | Home Health Agency | N/A | 10,867 |
| 11 | Skilled Nursing Facility | 50-300 | 11,500 |
| 12 | End-Stage Renal Disease (ESRD/Dialysis) | N/A | 12,714 |
| 14 | Partial Hospitalization Program | N/A | 1,619 |
| 17 | Critical Access Hospital | 10-25 | 75 |
| 19 | Ambulatory Surgical Center | N/A | 1,979 |
| 21 | Religious Non-Medical Health Institution | Varies | 15,028 |

**Note**: Type field contains numeric codes, not text descriptions

---

## Validation Rules

### Input Validation
- CCN (CMS Certification Number) must be 6 characters
- State codes must be valid 2-letter abbreviations
- Bed counts must be non-negative integers
- Star ratings must be 1-5 (where available)
- Limit must be between 1 and 1000

### Output Validation
- All CCNs should be valid CMS identifiers
- Bed counts should be reasonable for facility type
- Quality ratings should match CMS data

---

## Performance Notes

- **Facility count queries**: <50ms
- **Type + location searches**: 100-200ms
- **Quality rating joins**: 200-400ms
- **Primary key**: `ccn`

**Optimization Tips**:
- Filter by state first for better performance
- Use exact match on type field when possible
- Join with hospital_quality only when needed (only ~7% of facilities have ratings)

---

## Data Quality Notes

**Facility Coverage**: 77,302 facilities across all types
- **Hospitals**: ~6,000 acute care hospitals
- **Nursing Homes**: ~15,000 skilled nursing facilities
- **Other**: Home health, hospice, clinics, dialysis centers

**Quality Ratings**: 5,421 hospitals with CMS star ratings (~7% of total facilities)
- Ratings only available for Medicare-participating hospitals
- Scale: 1 (lowest) to 5 (highest)

**Geographic Coverage**:
- All 50 states + DC + territories
- **Missing county_fips**: Facilities table doesn't have county FIPS yet
  - Workaround: Use city/state or join with providers table on geography

**Bed Counts**:
- Available for hospitals and nursing homes
- NULL for outpatient facilities and agencies

---

## Related Skills

- **provider-search**: Find individual providers at facilities
- **hospital-quality-search**: Advanced quality-based hospital searches
- **network-roster**: Generate facility rosters for networks
- **coverage-analysis**: Analyze facility adequacy by geography

---

## Future Enhancements

1. **Add county_fips to facilities table** for better geographic joins
2. **Facility-provider linkage** via NPI to show which providers practice at which facilities
3. **Quality score trends** over time using historical CMS data
4. **Service line analysis** (trauma centers, NICUs, cardiac cath labs, etc.)
5. **Accreditation data** (Joint Commission, DNV, etc.)
6. **Distance calculations** for radius-based facility searches
