---
name: network-roster
description: Generate provider network rosters from search criteria with export to standard formats (CSV, JSON, Excel)

Trigger phrases:
- "Generate network roster for [criteria]"
- "Create provider list for [specialty] in [location]"
- "Build network of [providers]"
- "Export provider roster to [format]"
- "Generate provider panel for [network]"
---

# Network Roster Skill

## Overview

Generates comprehensive provider network rosters based on search criteria including specialty, geography, quality metrics, and provider characteristics. Supports multiple output formats (CSV, JSON, Excel) for integration with claims systems, credentialing platforms, and provider directories.

**Use Cases**:
- Health plan network development
- Provider directory generation
- Credentialing roster creation
- Network adequacy reporting
- Provider panel management

**Data Source**: `network.providers`, `network.facilities`, `network.hospital_quality`

---

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| criteria | object | Yes | Selection criteria for roster |
| criteria.specialties | array | No | Taxonomy codes or specialty names |
| criteria.locations | array | No | States, counties, or ZIP codes |
| criteria.entity_type | string | No | '1'=Individual, '2'=Organization |
| criteria.min_quality | integer | No | Minimum quality rating (if available) |
| output_format | string | No | 'json', 'csv', 'excel' (default: 'json') |
| include_fields | array | No | Fields to include in output |
| group_by | string | No | Group results by specialty, location, etc. |
| limit | integer | No | Max providers (default: 1000) |

---

## Query Patterns

### Pattern 1: Basic Specialty Roster

Generate roster for specific specialties in target geography.

```sql
-- Primary care roster for Texas counties
SELECT 
    p.npi,
    p.first_name || ' ' || p.last_name || 
    COALESCE(', ' || p.credential, '') as provider_name,
    p.taxonomy_1 as specialty_code,
    p.practice_address_1 as address,
    p.practice_city as city,
    p.practice_state as state,
    p.practice_zip as zip,
    p.county_fips,
    p.phone,
    p.entity_type_code as type
FROM network.providers p
WHERE p.practice_state = 'TX'
  AND (p.taxonomy_1 LIKE '207Q%'  -- Family Medicine
       OR p.taxonomy_1 LIKE '208D%'  -- General Practice  
       OR p.taxonomy_1 LIKE '207R%')  -- Internal Medicine
  AND p.entity_type_code = '1'
ORDER BY p.county_fips, p.last_name, p.first_name
LIMIT 1000;
```

### Pattern 2: Multi-Specialty Network Roster

Build comprehensive network across multiple specialties.

```sql
-- Multi-specialty network roster with specialty grouping
SELECT 
    CASE 
        WHEN p.taxonomy_1 LIKE '207Q%' THEN 'Family Medicine'
        WHEN p.taxonomy_1 LIKE '207R%' THEN 'Internal Medicine'
        WHEN p.taxonomy_1 LIKE '207RC%' THEN 'Cardiology'
        WHEN p.taxonomy_1 LIKE '207RE%' THEN 'Endocrinology'
        ELSE 'Other'
    END as specialty_group,
    COUNT(DISTINCT p.npi) as provider_count,
    COUNT(DISTINCT p.county_fips) as counties_covered,
    STRING_AGG(DISTINCT p.practice_state, ', ') as states
FROM network.providers p
WHERE p.taxonomy_1 IN (
    '207Q00000X',  -- Family Medicine
    '207R00000X',  -- Internal Medicine
    '207RC0000X',  -- Cardiology
    '207RE0101X'   -- Endocrinology
)
  AND p.practice_state IN ('CA', 'TX', 'FL', 'NY')
  AND p.entity_type_code = '1'
GROUP BY specialty_group
ORDER BY provider_count DESC;
```

### Pattern 3: Quality-Based Roster

Select providers meeting quality thresholds.

```sql
-- High-quality physician roster (with quality metrics when available)
SELECT 
    p.npi,
    p.first_name || ' ' || p.last_name as provider_name,
    p.credential,
    p.taxonomy_1,
    p.practice_city,
    p.practice_state,
    pq.composite_score as quality_score,
    pq.patient_satisfaction_score
FROM network.providers p
LEFT JOIN network.physician_quality pq ON p.npi = pq.npi
WHERE p.practice_state IN ('CA', 'NY')
  AND p.entity_type_code = '1'
  AND (pq.composite_score >= 75 OR pq.composite_score IS NULL)  -- High quality or no data
ORDER BY pq.composite_score DESC NULLS LAST, p.last_name
LIMIT 500;
```

### Pattern 4: Facility-Based Roster

Generate roster of providers affiliated with specific facilities.

```sql
-- Providers practicing at 5-star hospitals (conceptual linkage)
SELECT DISTINCT
    p.npi,
    p.first_name || ' ' || p.last_name as provider_name,
    p.taxonomy_1,
    f.name as facility_name,
    hq.hospital_overall_rating as hospital_rating,
    p.practice_city,
    p.practice_state
FROM network.facilities f
INNER JOIN network.hospital_quality hq ON f.ccn = hq.facility_id
INNER JOIN network.providers p 
    ON f.city = p.practice_city 
    AND f.state = p.practice_state
WHERE hq.hospital_overall_rating = '5'
  AND p.entity_type_code = '1'
  AND f.type = '01'  -- Hospitals
ORDER BY f.name, p.last_name
LIMIT 1000;
```

### Pattern 5: Network Adequacy Roster with Population

Generate roster with provider-to-population ratios.

```sql
-- Network roster with adequacy metrics by county
WITH county_roster AS (
    SELECT 
        p.county_fips,
        p.practice_state as state,
        COUNT(DISTINCT p.npi) as provider_count,
        COUNT(DISTINCT CASE WHEN p.taxonomy_1 LIKE '207Q%' THEN p.npi END) as pcp_count,
        COUNT(DISTINCT CASE WHEN p.taxonomy_1 LIKE '207RC%' THEN p.npi END) as cardio_count,
        STRING_AGG(DISTINCT p.npi, ', ') as npi_list
    FROM network.providers p
    WHERE p.entity_type_code = '1'
      AND p.county_fips IS NOT NULL
    GROUP BY p.county_fips, p.practice_state
)
SELECT 
    sv.county,
    cr.state,
    sv.e_totpop as population,
    cr.provider_count,
    cr.pcp_count,
    cr.cardio_count,
    ROUND(100000.0 * cr.provider_count / NULLIF(sv.e_totpop, 0), 2) as providers_per_100k,
    ROUND(100000.0 * cr.pcp_count / NULLIF(sv.e_totpop, 0), 2) as pcps_per_100k,
    CASE 
        WHEN ROUND(100000.0 * cr.pcp_count / NULLIF(sv.e_totpop, 0), 2) < 60 
        THEN 'Below Standard'
        ELSE 'Adequate'
    END as adequacy_status
FROM county_roster cr
JOIN population.svi_county sv ON cr.county_fips = sv.stcnty
WHERE sv.e_totpop > 10000
ORDER BY adequacy_status, providers_per_100k ASC
LIMIT 100;
```

---

## Examples

### Example 1: Generate Primary Care Roster for Harris County, TX

**Request**: "Generate a primary care provider roster for Harris County, Texas"

**Criteria**:
```json
{
  "specialties": ["207Q00000X", "208D00000X", "207R00000X"],
  "locations": {"county_fips": "48201"},
  "entity_type": "1",
  "output_format": "csv"
}
```

**Query**:
```sql
SELECT 
    p.npi,
    p.first_name,
    p.last_name,
    p.credential,
    p.taxonomy_1 as specialty_code,
    CASE 
        WHEN p.taxonomy_1 LIKE '207Q%' THEN 'Family Medicine'
        WHEN p.taxonomy_1 LIKE '208D%' THEN 'General Practice'
        WHEN p.taxonomy_1 LIKE '207R%' THEN 'Internal Medicine'
    END as specialty_name,
    p.practice_address_1 as address,
    p.practice_city as city,
    p.practice_state as state,
    p.practice_zip as zip,
    p.phone,
    p.county_fips
FROM network.providers p
WHERE p.county_fips = '48201'
  AND (p.taxonomy_1 LIKE '207Q%' 
       OR p.taxonomy_1 LIKE '208D%' 
       OR p.taxonomy_1 LIKE '207R%')
  AND p.entity_type_code = '1'
ORDER BY specialty_name, p.last_name, p.first_name;
```

**Expected Output**: CSV file with ~500-1000 PCPs

**Sample CSV**:
```csv
npi,first_name,last_name,credential,specialty_code,specialty_name,address,city,state,zip,phone,county_fips
1821267477,SYED,ABBAS,M.D.,207Q00000X,Family Medicine,123 Main St,HOUSTON,TX,77083,(713)555-0100,48201
1235219593,NAGEEB,ABDALLA,MD,207Q00000X,Family Medicine,456 Oak Ave,HOUSTON,TX,77018,(713)555-0200,48201
```

### Example 2: Multi-State Cardiology Network

**Request**: "Build a cardiology network for CA, TX, and FL with minimum 200 providers per state"

**Query**:
```sql
WITH state_counts AS (
    SELECT 
        p.practice_state,
        COUNT(*) as provider_count
    FROM network.providers p
    WHERE p.taxonomy_1 LIKE '207RC%'  -- Cardiology
      AND p.practice_state IN ('CA', 'TX', 'FL')
      AND p.entity_type_code = '1'
    GROUP BY p.practice_state
)
SELECT 
    p.npi,
    p.first_name || ' ' || p.last_name || ', ' || p.credential as provider_name,
    p.taxonomy_1,
    p.practice_address_1,
    p.practice_city,
    p.practice_state,
    p.practice_zip,
    p.phone,
    sc.provider_count as total_in_state
FROM network.providers p
JOIN state_counts sc ON p.practice_state = sc.practice_state
WHERE p.taxonomy_1 LIKE '207RC%'
  AND p.practice_state IN ('CA', 'TX', 'FL')
  AND p.entity_type_code = '1'
  AND sc.provider_count >= 200  -- Only include states meeting minimum
ORDER BY p.practice_state, p.practice_city, p.last_name
LIMIT 2000;
```

**Expected Output**: JSON roster with provider details grouped by state

### Example 3: Hospital-Affiliated Provider Roster

**Request**: "Generate roster of providers affiliated with 5-star hospitals in Massachusetts"

**Query**:
```sql
SELECT 
    p.npi,
    p.first_name || ' ' || p.last_name as provider_name,
    p.credential,
    p.taxonomy_1,
    p.practice_city,
    f.name as affiliated_hospital,
    hq.hospital_overall_rating as hospital_rating,
    p.phone
FROM network.providers p
INNER JOIN network.facilities f 
    ON p.practice_city = f.city 
    AND p.practice_state = f.state
INNER JOIN network.hospital_quality hq ON f.ccn = hq.facility_id
WHERE p.practice_state = 'MA'
  AND f.state = 'MA'
  AND f.type = '01'  -- Hospitals
  AND hq.hospital_overall_rating = '5'
  AND p.entity_type_code = '1'
ORDER BY f.name, p.taxonomy_1, p.last_name
LIMIT 500;
```

**Expected Output**: Provider roster with hospital affiliations

---

## Output Formats

### CSV Format

Standard comma-separated format for Excel, claims systems:

```csv
npi,provider_name,specialty,address,city,state,zip,phone
1234567890,"John Smith, MD",Family Medicine,123 Main St,Houston,TX,77001,(713)555-0100
```

### JSON Format

Structured format for APIs and integrations:

```json
{
  "roster_metadata": {
    "generated_date": "2025-12-27",
    "criteria": {
      "specialties": ["Family Medicine"],
      "locations": ["TX"]
    },
    "provider_count": 1250
  },
  "providers": [
    {
      "npi": "1234567890",
      "name": {
        "first": "John",
        "last": "Smith",
        "credential": "MD"
      },
      "specialty": {
        "code": "207Q00000X",
        "description": "Family Medicine"
      },
      "practice_location": {
        "address": "123 Main St",
        "city": "Houston",
        "state": "TX",
        "zip": "77001"
      },
      "phone": "(713) 555-0100"
    }
  ]
}
```

### Excel Format

Multi-sheet workbook with summary and details:

**Sheet 1: Summary**
- Provider counts by specialty
- Geographic distribution
- Network adequacy metrics

**Sheet 2: Provider Roster**
- Complete provider listing
- All contact information
- Taxonomy codes

---

## Export Implementation

### Python Export Functions

```python
import duckdb
import pandas as pd
import json

def export_roster_csv(query: str, output_path: str, conn):
    """Export roster to CSV file."""
    df = conn.execute(query).df()
    df.to_csv(output_path, index=False)
    return len(df)

def export_roster_json(query: str, output_path: str, conn):
    """Export roster to JSON file with metadata."""
    df = conn.execute(query).df()
    
    roster = {
        "roster_metadata": {
            "generated_date": pd.Timestamp.now().strftime('%Y-%m-%d'),
            "provider_count": len(df)
        },
        "providers": df.to_dict('records')
    }
    
    with open(output_path, 'w') as f:
        json.dump(roster, f, indent=2)
    
    return len(df)

def export_roster_excel(query: str, output_path: str, conn):
    """Export roster to Excel with summary sheet."""
    df = conn.execute(query).df()
    
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        # Summary sheet
        summary = pd.DataFrame({
            'Metric': ['Total Providers', 'Unique Specialties', 'States Covered'],
            'Value': [
                len(df),
                df['specialty_code'].nunique() if 'specialty_code' in df.columns else 0,
                df['state'].nunique() if 'state' in df.columns else 0
            ]
        })
        summary.to_excel(writer, sheet_name='Summary', index=False)
        
        # Full roster
        df.to_excel(writer, sheet_name='Provider Roster', index=False)
    
    return len(df)
```

---

## Validation Rules

### Roster Quality Checks
- All NPIs must be 10 digits and valid
- Each provider must have minimum required fields (name, NPI, location)
- No duplicate NPIs in roster
- Taxonomy codes must be valid NUCC codes

### Network Adequacy Checks
- Minimum provider counts per specialty met
- Geographic coverage requirements satisfied
- Provider-to-population ratios within standards

### Data Completeness
- Practice address complete (street, city, state, ZIP)
- Phone numbers in valid format
- Taxonomy codes populated

---

## Performance Notes

- **Small roster (<100 providers)**: <10ms
- **Medium roster (100-1000 providers)**: 50-100ms
- **Large roster (1000-10000 providers)**: 200-500ms
- **CSV export (1000 providers)**: ~100ms
- **JSON export (1000 providers)**: ~150ms
- **Excel export (1000 providers)**: ~300ms

**Optimization Tips**:
- Use LIMIT for large rosters
- Create roster in stages (by county or specialty)
- Index on frequently filtered fields
- Use batch exports for very large networks

---

## Related Skills

- **[provider-search](provider-search.md)**: Find providers for roster
- **[coverage-analysis](coverage-analysis.md)**: Validate network adequacy
- **[provider-density](provider-density.md)**: Calculate coverage metrics
- **[npi-validation](npi-validation.md)**: Validate roster NPIs

---

## Future Enhancements

1. **Automated roster updates** based on provider changes
2. **Tiering/stratification** by quality, cost, or utilization
3. **Provider attribution** to facilities or medical groups
4. **Network comparison** tools (before/after analysis)
5. **Export to EDI formats** (834 enrollment, 270/271)
6. **Integration with credentialing systems**

---

*Last Updated: December 27, 2025*  
*Version: 1.0.0*
