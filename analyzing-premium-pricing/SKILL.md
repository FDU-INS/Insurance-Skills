---
name: hcls-provider-claims-data-analysis
description: Analyze healthcare claims data for real-world evidence (RWE) studies. Use when working with medical/pharmacy claims (837/835), calculating utilization metrics, building patient cohorts, or analyzing treatment patterns. Triggers include claims data, RWE, real-world evidence, 837, 835, medical claims, pharmacy claims, utilization, treatment patterns, HEDIS, healthcare analytics.
---

# Healthcare Claims Data Analysis

Analyze medical and pharmacy claims for real-world evidence (RWE) and healthcare analytics.

## When to Use This Skill

- Analyzing medical claims (837P/837I) or pharmacy claims
- Building patient cohorts from administrative data
- Calculating healthcare utilization metrics
- Conducting treatment pattern analysis
- Real-world evidence studies

## Claims Data Overview

### Medical Claims (837)

| Field | Description | Example |
|-------|-------------|---------|
| claim_id | Unique claim identifier | CLM123456 |
| member_id | Patient identifier | MBR789 |
| service_date | Date of service | 2024-01-15 |
| diagnosis_codes | ICD-10 codes (dx1-dx12) | E11.9, I10 |
| procedure_code | CPT/HCPCS code | 99213 |
| place_of_service | Service location code | 11 (Office) |
| allowed_amount | Plan allowed amount | 150.00 |
| paid_amount | Plan paid amount | 120.00 |
| provider_npi | Rendering provider | 1234567890 |

### Pharmacy Claims

| Field | Description | Example |
|-------|-------------|---------|
| claim_id | Rx claim identifier | RX456789 |
| member_id | Patient identifier | MBR789 |
| fill_date | Prescription fill date | 2024-01-15 |
| ndc | National Drug Code | 00002-3227-30 |
| drug_name | Medication name | Metformin 500mg |
| quantity | Quantity dispensed | 60 |
| days_supply | Days supply | 30 |
| ingredient_cost | Drug cost | 45.00 |
| pharmacy_npi | Dispensing pharmacy | 9876543210 |

## Quick Start

### Load Claims to Snowflake

```sql
-- Medical claims table
CREATE OR REPLACE TABLE CLAIMS.MEDICAL (
    claim_id VARCHAR,
    member_id VARCHAR,
    service_from_date DATE,
    service_to_date DATE,
    admission_date DATE,
    discharge_date DATE,
    claim_type VARCHAR,  -- P=Professional, I=Institutional
    place_of_service VARCHAR,
    dx1 VARCHAR, dx2 VARCHAR, dx3 VARCHAR, dx4 VARCHAR,
    dx5 VARCHAR, dx6 VARCHAR, dx7 VARCHAR, dx8 VARCHAR,
    proc_code VARCHAR,
    proc_modifier VARCHAR,
    revenue_code VARCHAR,
    drg_code VARCHAR,
    provider_npi VARCHAR,
    facility_npi VARCHAR,
    billed_amount FLOAT,
    allowed_amount FLOAT,
    paid_amount FLOAT,
    member_liability FLOAT,
    _loaded_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- Pharmacy claims table
CREATE OR REPLACE TABLE CLAIMS.PHARMACY (
    claim_id VARCHAR,
    member_id VARCHAR,
    fill_date DATE,
    ndc VARCHAR,
    gpi VARCHAR,
    drug_name VARCHAR,
    generic_name VARCHAR,
    brand_generic_ind VARCHAR,
    quantity FLOAT,
    days_supply INTEGER,
    refill_number INTEGER,
    prescriber_npi VARCHAR,
    pharmacy_npi VARCHAR,
    ingredient_cost FLOAT,
    dispensing_fee FLOAT,
    plan_paid FLOAT,
    member_paid FLOAT,
    _loaded_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- Member eligibility
CREATE OR REPLACE TABLE CLAIMS.ELIGIBILITY (
    member_id VARCHAR,
    eff_date DATE,
    term_date DATE,
    lob VARCHAR,  -- Line of business
    plan_type VARCHAR,
    gender VARCHAR,
    birth_date DATE,
    zip_code VARCHAR,
    state VARCHAR
);
```

## Common Analyses

### Patient Cohort Building

```sql
-- Diabetes cohort: 2+ diagnoses or 1 Rx
WITH diabetes_dx AS (
    SELECT DISTINCT member_id
    FROM CLAIMS.MEDICAL
    WHERE dx1 LIKE 'E11%' OR dx2 LIKE 'E11%' OR dx3 LIKE 'E11%'
    GROUP BY member_id
    HAVING COUNT(DISTINCT claim_id) >= 2
),
diabetes_rx AS (
    SELECT DISTINCT member_id
    FROM CLAIMS.PHARMACY
    WHERE gpi LIKE '27%'  -- Antidiabetics
),
diabetes_cohort AS (
    SELECT member_id FROM diabetes_dx
    UNION
    SELECT member_id FROM diabetes_rx
)
SELECT 
    dc.member_id,
    e.gender,
    DATEDIFF('year', e.birth_date, CURRENT_DATE) AS age,
    e.state
FROM diabetes_cohort dc
JOIN CLAIMS.ELIGIBILITY e ON dc.member_id = e.member_id
WHERE e.term_date >= CURRENT_DATE;
```

### Healthcare Utilization Metrics

```sql
-- PMPM (Per Member Per Month) cost
WITH member_months AS (
    SELECT 
        member_id,
        DATEDIFF('month', eff_date, LEAST(term_date, CURRENT_DATE)) + 1 AS months_enrolled
    FROM CLAIMS.ELIGIBILITY
    WHERE eff_date <= CURRENT_DATE
),
member_costs AS (
    SELECT 
        member_id,
        SUM(paid_amount) AS total_medical
    FROM CLAIMS.MEDICAL
    WHERE service_from_date >= '2024-01-01'
    GROUP BY member_id
)
SELECT 
    AVG(mc.total_medical / mm.months_enrolled) AS medical_pmpm,
    SUM(mc.total_medical) / SUM(mm.months_enrolled) AS aggregate_pmpm
FROM member_costs mc
JOIN member_months mm ON mc.member_id = mm.member_id;
```

### Treatment Patterns

```sql
-- First-line therapy analysis
WITH first_rx AS (
    SELECT 
        member_id,
        drug_name,
        fill_date,
        ROW_NUMBER() OVER (PARTITION BY member_id ORDER BY fill_date) AS rx_order
    FROM CLAIMS.PHARMACY
    WHERE gpi LIKE '27%'  -- Antidiabetics
)
SELECT 
    drug_name,
    COUNT(*) AS patient_count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(), 1) AS pct
FROM first_rx
WHERE rx_order = 1
GROUP BY drug_name
ORDER BY patient_count DESC;
```

### Medication Adherence (PDC)

```sql
-- Proportion of Days Covered
WITH rx_fills AS (
    SELECT 
        member_id,
        fill_date,
        days_supply,
        LEAD(fill_date) OVER (PARTITION BY member_id ORDER BY fill_date) AS next_fill
    FROM CLAIMS.PHARMACY
    WHERE gpi LIKE '2720%'  -- Metformin
      AND fill_date >= '2024-01-01'
),
covered_days AS (
    SELECT 
        member_id,
        SUM(LEAST(
            days_supply,
            COALESCE(DATEDIFF('day', fill_date, next_fill), days_supply)
        )) AS days_covered,
        DATEDIFF('day', MIN(fill_date), MAX(fill_date)) + 
            MAX(days_supply) AS observation_period
    FROM rx_fills
    GROUP BY member_id
)
SELECT 
    member_id,
    days_covered,
    observation_period,
    ROUND(days_covered * 100.0 / observation_period, 1) AS pdc,
    CASE WHEN days_covered * 100.0 / observation_period >= 80 THEN 'Adherent' 
         ELSE 'Non-Adherent' END AS adherence_status
FROM covered_days
WHERE observation_period >= 90;
```

### Episode of Care

```sql
-- Group claims into episodes (30-day gap = new episode)
WITH claims_sorted AS (
    SELECT 
        member_id,
        service_from_date,
        paid_amount,
        LAG(service_from_date) OVER (PARTITION BY member_id ORDER BY service_from_date) AS prev_date
    FROM CLAIMS.MEDICAL
    WHERE dx1 LIKE 'M54%'  -- Back pain
),
episode_flags AS (
    SELECT 
        *,
        CASE WHEN DATEDIFF('day', prev_date, service_from_date) > 30 
             OR prev_date IS NULL THEN 1 ELSE 0 END AS new_episode
    FROM claims_sorted
),
episodes AS (
    SELECT 
        *,
        SUM(new_episode) OVER (PARTITION BY member_id ORDER BY service_from_date) AS episode_num
    FROM episode_flags
)
SELECT 
    member_id,
    episode_num,
    MIN(service_from_date) AS episode_start,
    MAX(service_from_date) AS episode_end,
    COUNT(*) AS claim_count,
    SUM(paid_amount) AS episode_cost
FROM episodes
GROUP BY member_id, episode_num;
```

## Place of Service Codes

| Code | Description |
|------|-------------|
| 11 | Office |
| 21 | Inpatient Hospital |
| 22 | Outpatient Hospital |
| 23 | Emergency Room |
| 31 | Skilled Nursing Facility |
| 81 | Independent Lab |

## GPI Drug Classification

| GPI Prefix | Therapeutic Class |
|------------|-------------------|
| 27 | Antidiabetics |
| 39 | Cardiovascular |
| 40 | Antihypertensives |
| 44 | Antihyperlipidemics |
| 57 | Psychotherapeutics |
| 66 | Analgesics |

## HEDIS-Style Measures

```sql
-- Diabetes A1c Testing Rate
WITH diabetic_members AS (
    SELECT DISTINCT member_id
    FROM CLAIMS.MEDICAL
    WHERE dx1 LIKE 'E11%' OR dx2 LIKE 'E11%'
),
a1c_tests AS (
    SELECT DISTINCT member_id
    FROM CLAIMS.MEDICAL
    WHERE proc_code IN ('83036', '83037')  -- A1c CPT codes
      AND service_from_date >= DATEADD('year', -1, CURRENT_DATE)
)
SELECT 
    COUNT(DISTINCT a.member_id) AS tested,
    COUNT(DISTINCT d.member_id) AS diabetic,
    ROUND(100.0 * COUNT(DISTINCT a.member_id) / COUNT(DISTINCT d.member_id), 1) AS testing_rate
FROM diabetic_members d
LEFT JOIN a1c_tests a ON d.member_id = a.member_id;
```

## Best Practices

1. **Continuous enrollment**: Require minimum enrollment period for studies
2. **Washout periods**: Look back for prior conditions/treatments
3. **Claims lag**: Allow 60-90 days for claims runout
4. **Validate cohorts**: Cross-check Dx and Rx definitions
5. **Adjust for confounders**: Age, gender, comorbidities

## Reference Files

- `references/place_of_service.md` - POS codes
- `references/gpi_classification.md` - Drug classification
- `references/hedis_measures.md` - HEDIS specifications

## Requirements

```
pandas>=2.0.0
snowflake-connector-python>=3.0.0
```

## Evidence Grounding: Clinical Trials CKE

Invoke `$cke-clinical-trials` when trial registry evidence enhances claims analysis:

- Feasibility analysis: search for trials by condition to match against claims-based cohort characteristics
- RWE benchmarking: compare real-world treatment patterns against clinical trial protocols
- Site selection support: identify active trial sites and match with claims-based patient geographies

See `$cke-clinical-trials` for setup, query patterns, and the feasibility analysis SQL pattern.
