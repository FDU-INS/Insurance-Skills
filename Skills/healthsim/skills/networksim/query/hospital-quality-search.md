---
name: hospital-quality-search
description: Search and filter hospitals by CMS star ratings, quality domains, and performance metrics

Trigger phrases:
- "Find hospitals with [X] star rating in [location]"
- "Search for high-quality hospitals"
- "Show hospitals rated [rating] or higher"
- "List hospitals by star rating in [state]"
- "Which hospitals have 5-star ratings?"
---

# Hospital Quality Search Skill

## Overview

Searches and filters hospitals based on CMS Hospital Compare star ratings and quality metrics. Enables quality-tier network development, value-based contracting, and patient access to high-performing facilities. CMS star ratings range from 1 (lowest) to 5 (highest quality), with approximately 47% of hospitals lacking ratings.

**CMS Star Rating System**:
- **5 stars**: Much above average
- **4 stars**: Above average
- **3 stars**: Average
- **2 stars**: Below average  
- **1 star**: Much below average
- **Not Available**: Insufficient data or not rated

**Data Source**: `network.hospital_quality` (5,421 hospitals, 53% with ratings)

---

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| min_rating | integer | No | Minimum star rating (1-5) |
| rating | string | No | Exact rating ('1', '2', '3', '4', '5') |
| include_unrated | boolean | No | Include 'Not Available' hospitals (default: false) |
| state | string | No | Filter by state |
| city | string | No | Filter by city |
| facility_name | string | No | Search facility name (partial match) |

---

## Rating Distribution (CMS Hospital Compare)

```
Rating Distribution (5,421 total hospitals):

5 stars: ★★★★★        289 (  5.3%)  ← Excellence tier
4 stars: ★★★★         765 ( 14.1%)  ← High quality tier
3 stars: ★★★          937 ( 17.3%)  ← Average tier
2 stars: ★★           649 ( 12.0%)  ← Below average
1 stars: ★            229 (  4.2%)  ← Lowest performing
Not Available      2,552 ( 47.1%)  ← Unrated/insufficient data
```

**Quality Tiers for Network Design**:
- **Premium Network**: 5-star only (289 hospitals, 5.3%)
- **High-Quality Network**: 4-5 stars (1,054 hospitals, 19.4%)
- **Standard Network**: 3-5 stars (1,991 hospitals, 36.7%)
- **Broad Network**: 1-5 stars (2,869 hospitals, 52.9%)

---

## Query Patterns

### Pattern 1: Basic Star Rating Filter

Find hospitals meeting minimum quality threshold.

```sql
-- Find 4 and 5-star hospitals in California
SELECT 
    hq.facility_id,
    hq.facility_name,
    hq.city_town as city,
    hq.state,
    hq.hospital_overall_rating as star_rating
FROM network.hospital_quality hq
WHERE hq.state = 'CA'
  AND hq.hospital_overall_rating IN ('4', '5')
ORDER BY 
    CAST(hq.hospital_overall_rating AS INTEGER) DESC,
    hq.facility_name
LIMIT 100;
```

### Pattern 2: Quality-Tier Network Selection

Build tiered networks based on quality levels.

```sql
-- Multi-tier network: Premium (5★), Preferred (4★), Standard (3★)
SELECT 
    CASE 
        WHEN hq.hospital_overall_rating = '5' THEN 'Premium'
        WHEN hq.hospital_overall_rating = '4' THEN 'Preferred'
        WHEN hq.hospital_overall_rating = '3' THEN 'Standard'
        ELSE 'Not Included'
    END as network_tier,
    COUNT(*) as hospital_count,
    STRING_AGG(DISTINCT hq.state, ', ' ORDER BY hq.state) as states_covered
FROM network.hospital_quality hq
WHERE hq.hospital_overall_rating IN ('3', '4', '5')
  AND hq.state IN ('CA', 'TX', 'FL', 'NY')
GROUP BY network_tier
ORDER BY 
    CASE network_tier
        WHEN 'Premium' THEN 1
        WHEN 'Preferred' THEN 2
        WHEN 'Standard' THEN 3
        ELSE 4
    END;
```

### Pattern 3: Geographic Quality Distribution

Analyze quality distribution by location.

```sql
-- Quality distribution by state
SELECT 
    hq.state,
    COUNT(*) as total_hospitals,
    COUNT(CASE WHEN hq.hospital_overall_rating = '5' THEN 1 END) as five_star,
    COUNT(CASE WHEN hq.hospital_overall_rating = '4' THEN 1 END) as four_star,
    COUNT(CASE WHEN hq.hospital_overall_rating = '3' THEN 1 END) as three_star,
    COUNT(CASE WHEN hq.hospital_overall_rating IN ('1', '2') THEN 1 END) as below_avg,
    COUNT(CASE WHEN hq.hospital_overall_rating = 'Not Available' THEN 1 END) as unrated,
    ROUND(100.0 * COUNT(CASE WHEN hq.hospital_overall_rating IN ('4', '5') THEN 1 END) / 
          COUNT(*), 1) as pct_high_quality
FROM network.hospital_quality hq
WHERE hq.state IN ('CA', 'TX', 'FL', 'NY', 'PA')
GROUP BY hq.state
ORDER BY pct_high_quality DESC;
```

### Pattern 4: Quality-Based Facility Roster

Generate hospital roster filtered by quality.

```sql
-- Premium hospital roster (5-star only) with facility details
SELECT 
    hq.facility_id,
    hq.facility_name,
    hq.city_town,
    hq.state,
    hq.hospital_overall_rating as rating,
    f.type as facility_type,
    f.bed_count,
    f.name as official_name
FROM network.hospital_quality hq
INNER JOIN network.facilities f ON hq.facility_id = f.ccn
WHERE hq.hospital_overall_rating = '5'
  AND hq.state = 'CA'
ORDER BY hq.city_town, hq.facility_name
LIMIT 100;
```

### Pattern 5: Quality Gap Analysis

Identify areas with limited high-quality hospital access.

```sql
-- Counties with zero high-quality hospitals
WITH county_quality AS (
    SELECT 
        f.state,
        f.county as county_name,
        COUNT(*) as total_hospitals,
        COUNT(CASE WHEN hq.hospital_overall_rating IN ('4', '5') THEN 1 END) as high_quality_count,
        MAX(CASE 
            WHEN hq.hospital_overall_rating = '5' THEN 5
            WHEN hq.hospital_overall_rating = '4' THEN 4
            WHEN hq.hospital_overall_rating = '3' THEN 3
            WHEN hq.hospital_overall_rating = '2' THEN 2
            WHEN hq.hospital_overall_rating = '1' THEN 1
            ELSE 0
        END) as best_rating
    FROM network.facilities f
    LEFT JOIN network.hospital_quality hq ON f.ccn = hq.facility_id
    WHERE f.type = '01'  -- Hospitals only
      AND f.state IN ('TX', 'CA', 'FL')
    GROUP BY f.state, f.county
)
SELECT 
    state,
    county_name,
    total_hospitals,
    high_quality_count,
    best_rating,
    CASE 
        WHEN high_quality_count = 0 AND total_hospitals > 0 THEN 'Quality Desert'
        WHEN best_rating <= 2 THEN 'Low Quality Area'
        WHEN high_quality_count < 2 THEN 'Limited Choice'
        ELSE 'Adequate'
    END as access_status
FROM county_quality
WHERE high_quality_count = 0 OR best_rating <= 2
ORDER BY state, county_name
LIMIT 50;
```

---

## Examples

### Example 1: Find 5-Star Hospitals in California

**Request**: "Show me all 5-star hospitals in California"

**Query**:
```sql
SELECT 
    hq.facility_id,
    hq.facility_name,
    hq.city_town as city,
    hq.hospital_overall_rating as rating,
    f.bed_count
FROM network.hospital_quality hq
LEFT JOIN network.facilities f ON hq.facility_id = f.ccn
WHERE hq.state = 'CA'
  AND hq.hospital_overall_rating = '5'
ORDER BY hq.city_town, hq.facility_name;
```

**Expected Output**: List of California's highest-rated hospitals (5.3% of total)

**Sample**:
```
facility_id | facility_name                    | city          | rating | bed_count
------------|----------------------------------|---------------|--------|----------
050308      | STANFORD HEALTH CARE             | STANFORD      | 5      | 613
050673      | HOAG MEMORIAL HOSPITAL PRESBYTER | NEWPORT BEACH | 5      | 498
```

### Example 2: Build Quality-Tiered Network

**Request**: "Create a tiered network for Texas: Premium (5★), Preferred (4★), Standard (3★)"

**Query**:
```sql
WITH texas_hospitals AS (
    SELECT 
        hq.facility_id,
        hq.facility_name,
        hq.city_town,
        hq.hospital_overall_rating,
        CASE 
            WHEN hq.hospital_overall_rating = '5' THEN 'Premium'
            WHEN hq.hospital_overall_rating = '4' THEN 'Preferred'
            WHEN hq.hospital_overall_rating = '3' THEN 'Standard'
            ELSE NULL
        END as tier
    FROM network.hospital_quality hq
    WHERE hq.state = 'TX'
      AND hq.hospital_overall_rating IN ('3', '4', '5')
)
SELECT 
    tier,
    COUNT(*) as hospital_count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) as pct_of_network,
    STRING_AGG(facility_name, ', ' ORDER BY facility_name) 
        FILTER (WHERE tier = 'Premium') as sample_premium_hospitals
FROM texas_hospitals
GROUP BY tier
ORDER BY 
    CASE tier
        WHEN 'Premium' THEN 1
        WHEN 'Preferred' THEN 2
        WHEN 'Standard' THEN 3
    END;
```

**Expected Output**: Tiered hospital counts with distribution

### Example 3: Quality Analysis by Metro Area

**Request**: "Compare hospital quality across major cities"

**Query**:
```sql
WITH city_quality AS (
    SELECT 
        hq.city_town,
        hq.state,
        COUNT(*) as total,
        ROUND(AVG(
            CASE 
                WHEN hq.hospital_overall_rating = '5' THEN 5
                WHEN hq.hospital_overall_rating = '4' THEN 4
                WHEN hq.hospital_overall_rating = '3' THEN 3
                WHEN hq.hospital_overall_rating = '2' THEN 2
                WHEN hq.hospital_overall_rating = '1' THEN 1
                ELSE NULL
            END
        ), 2) as avg_rating,
        COUNT(CASE WHEN hq.hospital_overall_rating IN ('4', '5') THEN 1 END) as high_quality
    FROM network.hospital_quality hq
    WHERE hq.city_town IN ('HOUSTON', 'LOS ANGELES', 'CHICAGO', 'PHOENIX', 'PHILADELPHIA')
    GROUP BY hq.city_town, hq.state
)
SELECT 
    city_town,
    state,
    total as hospitals,
    avg_rating,
    high_quality,
    ROUND(100.0 * high_quality / total, 1) as pct_high_quality,
    CASE 
        WHEN avg_rating >= 4.0 THEN 'Excellent Market'
        WHEN avg_rating >= 3.5 THEN 'Good Market'
        WHEN avg_rating >= 3.0 THEN 'Average Market'
        ELSE 'Below Average Market'
    END as market_quality
FROM city_quality
ORDER BY avg_rating DESC;
```

**Expected Output**: City comparison with quality metrics

---

## Quality-Based Network Strategies

### Premium Network (5-Star Only)
**Profile**: Highest quality, limited network
- **Hospitals**: 289 (5.3% of rated)
- **Use Case**: Medicare Advantage premium plans, COEs
- **Trade-Off**: Limited geographic access, premium pricing

### High-Quality Network (4-5 Stars)
**Profile**: Above-average quality, moderate network
- **Hospitals**: 1,054 (19.4% of rated)
- **Use Case**: Standard MA plans, quality-focused commercial
- **Trade-Off**: Balanced access and quality

### Standard Network (3+ Stars)
**Profile**: Average or better, broad network
- **Hospitals**: 1,991 (36.7% of rated)
- **Use Case**: Broad commercial networks, Medicaid
- **Trade-Off**: Wide access, mixed quality

### Selective Exclusion (Exclude 1-2 Stars)
**Profile**: Avoid lowest performers
- **Excluded**: 878 hospitals (16.2% of rated)
- **Use Case**: Quality improvement focus
- **Trade-Off**: May limit access in some areas

---

## Integration with Other Skills

### With Coverage Analysis
```sql
-- Network adequacy + quality requirements
SELECT 
    sv.county,
    sv.state,
    COUNT(DISTINCT hq.facility_id) as high_quality_hospitals,
    sv.e_totpop as population,
    ROUND(100000.0 * COUNT(DISTINCT hq.facility_id) / sv.e_totpop, 2) as per_100k
FROM population.svi_county sv
LEFT JOIN network.facilities f ON sv.stcnty = f.county_fips
LEFT JOIN network.hospital_quality hq 
    ON f.ccn = hq.facility_id 
    AND hq.hospital_overall_rating IN ('4', '5')
WHERE sv.state = 'California'
GROUP BY sv.county, sv.state, sv.e_totpop
HAVING COUNT(DISTINCT hq.facility_id) = 0  -- Counties with zero high-quality hospitals
ORDER BY population DESC
LIMIT 20;
```

### With Provider Search
```sql
-- Physicians affiliated with high-quality hospitals (conceptual)
SELECT 
    p.npi,
    p.first_name || ' ' || p.last_name as provider_name,
    p.taxonomy_1,
    hq.facility_name,
    hq.hospital_overall_rating
FROM network.providers p
INNER JOIN network.hospital_quality hq 
    ON p.practice_city = hq.city_town
    AND p.practice_state = hq.state
WHERE hq.hospital_overall_rating IN ('4', '5')
  AND p.entity_type_code = '1'
  AND p.practice_state = 'CA'
ORDER BY hq.hospital_overall_rating DESC, p.last_name
LIMIT 100;
```

---

## Validation Rules

### Rating Values
- Must be '1', '2', '3', '4', '5', or 'Not Available'
- Null values treated as 'Not Available'
- Case-insensitive matching ('5' = '5')

### Data Quality
- All hospitals have facility_id (CCN)
- 100% have ratings (may be 'Not Available')
- State abbreviations standardized (2 letters)
- City names uppercase

### Business Rules
- Minimum quality tier must be defensible
- Geographic access maintained with quality requirements
- Unrated hospitals handled consistently
- Quality metrics updated annually

---

## Performance Notes

- **Single rating filter**: <5ms
- **State-level aggregation**: 10-20ms
- **Quality distribution**: 20-30ms
- **Complex JOIN with facilities**: 30-50ms

**Optimization Tips**:
- Use IN clause for multiple ratings
- Index on hospital_overall_rating
- Filter by state early
- Cache rating distributions

---

## CMS Rating Methodology

**Hospital Overall Rating** is composite of 7 quality domains:
1. Mortality
2. Safety of Care
3. Readmission
4. Patient Experience
5. Effectiveness of Care
6. Timeliness of Care
7. Efficient Use of Medical Imaging

**Note**: Current dataset has overall rating only. Domain-specific metrics can be added when available.

---

## Related Skills

- **[facility-search](facility-search.md)**: Basic hospital search
- **[coverage-analysis](coverage-analysis.md)**: Network adequacy with quality
- **[network-roster](network-roster.md)**: Quality-filtered rosters
- **[physician-quality-search](physician-quality-search.md)**: Provider quality metrics

---

## Future Enhancements

1. **Domain-specific ratings** (mortality, readmission, patient experience)
2. **Trend analysis** (year-over-year rating changes)
3. **Peer comparisons** (vs regional or national benchmarks)
4. **Value scores** (quality × cost efficiency)
5. **Patient preference weighting** (emphasize specific domains)
6. **Leapfrog ratings** integration
7. **Safety scores** (HAI, PSI indicators)

---

*Last Updated: December 27, 2025*  
*Version: 1.0.0*  
*CMS Data: Hospital Compare Overall Rating*
