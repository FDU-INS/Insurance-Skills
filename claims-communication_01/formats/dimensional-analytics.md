# Dimensional Analytics Format

## Trigger Phrases

- dimensional
- star schema
- analytics
- data warehouse
- fact table
- dimension table
- DuckDB
- BI export
- reporting database

## Overview

This skill transforms HealthSim entities into dimensional (star schema) format optimized for analytics and business intelligence. The dimensional model separates data into:

- **Dimension Tables**: Descriptive attributes (who, what, where, when)
- **Fact Tables**: Measurable events and metrics (how much, how many)

## When to Use

Use dimensional output when:
- Building BI dashboards (Tableau, Power BI, Looker)
- Running SQL-based population health analytics
- Computing quality measures and KPIs
- Creating data warehouses for reporting
- Loading to analytics databases

## Target Databases

### DuckDB (Primary - Local Analytics)

**Status**: ✅ Fully Supported  
**Use case**: Local development, testing, demos, personal analytics

DuckDB is the default target for dimensional analytics. It's bundled with healthsim-core - no additional setup required.

**Example conversation:**
```
Generate 10 diabetic patients in star schema format for DuckDB
```

### Enterprise Cloud Platforms (Future)

**Status**: 🔮 Planned for Phase 3

Support for enterprise analytics platforms is planned for a future release:

| Platform | Status | Notes |
|----------|--------|-------|
| Databricks | Planned | Unity Catalog integration, Delta tables |
| Snowflake | Planned | Snowpark integration |
| MotherDuck | Planned | Cloud-hosted DuckDB |

When implemented, these will enable:
- Team collaboration on shared datasets
- Large-scale data generation (millions of records)
- Integration with enterprise BI tools
- Data governance and access control

For now, you can export dimensional data from DuckDB and load it to your enterprise platform using standard ETL tools.

## Conversation-First Approach

Generate dimensional data through natural conversation. Claude generates SQL directly - no scripts, no code generation.

### Quick Start Example

```
Generate 10 diabetic patients in star schema format for DuckDB
```

## Products and Their Star Schemas

### PatientSim (Clinical Analytics)

**Dimensions:**
| Table | Description | Key Columns |
|-------|-------------|-------------|
| `dim_patient` | Patient demographics | patient_key, mrn, age, age_band, gender |
| `dim_facility` | Healthcare facilities | facility_key, facility_code, facility_name |
| `dim_provider` | Healthcare providers | provider_key, npi, provider_name, specialty |
| `dim_diagnosis` | ICD-10 codes | diagnosis_key, icd10_code, description, category |
| `dim_procedure` | Procedure codes | procedure_key, cpt_code, description |
| `dim_medication` | Medications | medication_key, rxnorm_code, drug_name, therapeutic_class |
| `dim_lab_test` | Lab definitions | lab_test_key, loinc_code, test_name, unit |
| `dim_date` | Calendar | date_key, full_date, year, quarter, month, day_name, is_holiday |

**Facts:**
| Table | Grain | Key Metrics |
|-------|-------|-------------|
| `fact_encounters` | One row per encounter | length_of_stay_hours, length_of_stay_days, is_readmission_7_day, is_readmission_30_day |
| `fact_diagnoses` | One row per diagnosis | is_primary, is_admitting, onset_date_key |
| `fact_procedures` | One row per procedure | performed_date_key, procedure_count |
| `fact_medications` | One row per medication | start_date_key, end_date_key, is_active |
| `fact_lab_results` | One row per result | result_numeric, is_abnormal, is_critical |
| `fact_vitals` | One row per vital set | is_febrile, is_tachycardic, is_hypotensive, is_hypertensive |

### MemberSim (Payer Analytics)

**Dimensions:**
| Table | Description | Key Columns |
|-------|-------------|-------------|
| `dim_member` | Member demographics | member_key, member_id, age_band, relationship |
| `dim_plan` | Plan details | plan_key, plan_code, plan_type, network_type |
| `dim_provider` | Billing/rendering | provider_key, npi, provider_type |
| `dim_facility` | Place of service | facility_key, pos_code, facility_type |
| `dim_diagnosis` | ICD-10 codes | diagnosis_key, icd10_code, category |
| `dim_procedure` | CPT/HCPCS | procedure_key, cpt_code, description |
| `dim_service_category` | Service groupings | service_category_key, category_name |

**Facts:**
| Table | Grain | Key Metrics |
|-------|-------|-------------|
| `fact_claims` | One row per claim line | charge_amount, allowed_amount, paid_amount, member_responsibility, deductible, copay, coinsurance |
| `fact_eligibility_spans` | One row per coverage period | start_date_key, end_date_key, coverage_days |

### RxMemberSim (Pharmacy Analytics)

**Dimensions:**
| Table | Description | Key Columns |
|-------|-------------|-------------|
| `dim_rx_member` | Pharmacy member | rx_member_key, member_id, age_band, plan_phase |
| `dim_medication` | NDC/drug details | medication_key, ndc, gpi, therapeutic_class, is_brand, is_specialty |
| `dim_pharmacy` | Pharmacy info | pharmacy_key, ncpdp_id, pharmacy_type, in_network |
| `dim_prescriber` | Prescriber info | prescriber_key, npi, specialty, dea_number |
| `dim_formulary` | Tier assignments | formulary_key, tier, requires_pa, step_therapy |

**Facts:**
| Table | Grain | Key Metrics |
|-------|-------|-------------|
| `fact_prescription_fills` | One row per fill | quantity_dispensed, days_supply, ingredient_cost, dispensing_fee, total_paid, patient_pay |
| `fact_prior_auth` | One row per PA | request_date_key, decision_date_key, status, approved_quantity |
| `fact_rx_eligibility_spans` | One row per coverage | deductible_remaining, oop_remaining, part_d_phase |

## Shared Date Dimension

All products share a common date dimension:

```sql
CREATE TABLE dim_date (
    date_key INT PRIMARY KEY,           -- YYYYMMDD format
    full_date DATE NOT NULL,
    year INT,
    quarter INT,
    quarter_name VARCHAR(2),            -- Q1, Q2, Q3, Q4
    month INT,
    month_name VARCHAR(20),
    week_of_year INT,
    day_of_month INT,
    day_of_week INT,
    day_name VARCHAR(20),
    is_weekend BOOLEAN,
    is_us_federal_holiday BOOLEAN,
    holiday_name VARCHAR(50)
);
```

US Federal Holidays included:
- New Year's Day, MLK Day, Presidents Day, Memorial Day
- Juneteenth, Independence Day, Labor Day, Columbus Day
- Veterans Day, Thanksgiving, Christmas

## Common Analytics Queries

### PatientSim: 30-Day Readmission Rate

```sql
SELECT
    d.category as diagnosis_category,
    COUNT(*) as encounters,
    SUM(CASE WHEN f.is_readmission_30_day THEN 1 ELSE 0 END) as readmissions,
    ROUND(100.0 * SUM(CASE WHEN f.is_readmission_30_day THEN 1 ELSE 0 END) / COUNT(*), 2) as readmit_rate
FROM fact_encounters f
JOIN fact_diagnoses fd ON f.encounter_key = fd.encounter_key
JOIN dim_diagnosis d ON fd.icd10_code = d.icd10_code
WHERE fd.is_primary = true
GROUP BY d.category
ORDER BY readmit_rate DESC;
```

### MemberSim: Cost by Service Category

```sql
SELECT
    sc.category_name as service_category,
    COUNT(*) as claim_lines,
    SUM(f.charge_amount) as total_charged,
    SUM(f.allowed_amount) as total_allowed,
    SUM(f.paid_amount) as plan_paid,
    SUM(f.member_responsibility) as member_paid
FROM fact_claims f
JOIN dim_service_category sc ON f.service_category_key = sc.service_category_key
GROUP BY sc.category_name
ORDER BY plan_paid DESC;
```

### RxMemberSim: Generic Dispensing Rate

```sql
SELECT
    m.therapeutic_class,
    COUNT(*) as total_fills,
    SUM(CASE WHEN NOT m.is_brand THEN 1 ELSE 0 END) as generic_fills,
    ROUND(100.0 * SUM(CASE WHEN NOT m.is_brand THEN 1 ELSE 0 END) / COUNT(*), 2) as gdr
FROM fact_prescription_fills f
JOIN dim_medication m ON f.medication_key = m.medication_key
GROUP BY m.therapeutic_class
ORDER BY gdr;
```

### Cross-Product: Total Member Spend

```sql
-- Requires both MemberSim and RxMemberSim data
SELECT
    m.age_band,
    COUNT(DISTINCT m.member_key) as members,
    COALESCE(SUM(mc.paid_amount), 0) as medical_spend,
    COALESCE(SUM(rx.total_paid), 0) as pharmacy_spend,
    COALESCE(SUM(mc.paid_amount), 0) + COALESCE(SUM(rx.total_paid), 0) as total_spend
FROM dim_member m
LEFT JOIN fact_claims mc ON m.member_key = mc.member_key
LEFT JOIN dim_rx_member rm ON m.person_id = rm.person_id
LEFT JOIN fact_prescription_fills rx ON rm.rx_member_key = rx.rx_member_key
GROUP BY m.age_band
ORDER BY total_spend DESC;
```

## Derived Metrics

The dimensional model pre-calculates useful derived metrics:

### Patient Dimensions
- `age_band`: 0-17, 18-34, 35-44, 45-54, 55-64, 65-74, 75-84, 85+
- `gender_description`: Male, Female, Other, Unknown

### Encounter Facts
- `length_of_stay_hours`: Calculated from admission/discharge
- `length_of_stay_days`: Rounded LOS in days
- `is_readmission_7_day`: True if readmitted within 7 days
- `is_readmission_30_day`: True if readmitted within 30 days

### Lab Result Facts
- `is_abnormal`: Outside reference range
- `is_critical`: Significantly outside range (panic value)

### Vital Sign Facts
- `is_febrile`: Temperature > 100.4F
- `is_tachycardic`: Heart rate > 100
- `is_hypotensive`: Systolic BP < 90
- `is_hypertensive`: Systolic BP > 140

### Claim Facts
- `member_responsibility`: deductible + copay + coinsurance
- Service category derived from CPT code ranges

## Example: Complete Workflow

### DuckDB Local Workflow

**User request:**
```
Generate 5 patients with encounters in star schema format for DuckDB analytics
```

**Claude generates:**
1. CREATE TABLE statements for dimensions and facts
2. INSERT statements with realistic healthcare data
3. Sample analytics queries to verify the data

```sql
-- Dimension: dim_patient
CREATE TABLE IF NOT EXISTS analytics.dim_patient (
    patient_key INT PRIMARY KEY,
    mrn VARCHAR(20),
    given_name VARCHAR(50),
    family_name VARCHAR(50),
    birth_date DATE,
    age INT,
    age_band VARCHAR(10),
    gender CHAR(1),
    gender_description VARCHAR(10),
    city VARCHAR(50),
    state CHAR(2)
);

-- Insert patients
INSERT INTO analytics.dim_patient VALUES
(1, 'MRN100001', 'John', 'Smith', '1960-03-15', 65, '65-74', 'M', 'Male', 'Springfield', 'IL'),
(2, 'MRN100002', 'Maria', 'Garcia', '1955-08-22', 69, '65-74', 'F', 'Female', 'Chicago', 'IL'),
-- ... more rows
```

## Reproducibility

For consistent results across sessions:

**Request:** "Generate 10 patients using seed 42"

Claude will:
1. Use seed 42 for all random selections
2. Generate identical output if same parameters used
3. Note the seed in output for reference

---

## TrialSim (Clinical Trial Analytics)

Dimensional model for clinical trial operational analytics, site performance, and safety surveillance.

### Use Cases

| Analytics Domain | Questions Answered |
|------------------|-------------------|
| **Enrollment Operations** | Enrollment velocity by site? Screen failure rate by reason? Days from screening to randomization? |
| **Safety Surveillance** | AE rates by arm over time? SAE clustering? Time-to-first-AE curves? |
| **Site Performance** | Protocol deviation rates by site? Visit compliance? Query resolution time? |
| **Efficacy Analysis** | Response rates by arm? Disease control rate? Progression-free survival? |
| **Dose-Response** | Dose intensity? Dose modifications by reason? Exposure-response correlation? |

### Dimensions

| Table | Description | Key Columns |
|-------|-------------|-------------|
| `dim_study` | Study/protocol attributes | study_key, study_id, phase, therapeutic_area, indication |
| `dim_site` | Site/geography attributes | site_key, site_id, country, region, pi_name |
| `dim_subject` | Subject demographics | subject_key, usubjid, age_band, sex, race, ethnicity |
| `dim_treatment_arm` | Treatment arm definitions | arm_key, arm_code, arm_type, dose, schedule |
| `dim_visit_schedule` | Protocol visit schedule | visit_schedule_key, visit_num, visit_name, target_day |
| `dim_meddra` | MedDRA hierarchy for AEs | meddra_key, pt_term, hlt_term, hlgt_term, soc_term |
| `dim_lab_test` | Lab test definitions | lab_test_key, lbtestcd, lbtest, lbcat, loinc_code |

### Facts

| Table | Grain | Key Metrics |
|-------|-------|-------------|
| `fact_enrollment` | One row per subject milestone | days_screen_to_consent, days_consent_to_randomization, screen_failure_flag |
| `fact_visit` | One row per actual visit | window_deviation_days, is_within_window, assessments_completed |
| `fact_adverse_event` | One row per AE occurrence | severity, ctcae_grade, is_serious, is_related, duration_days |
| `fact_exposure` | One row per dosing record | dose_administered, dose_percent, is_dose_reduction, cumulative_dose |
| `fact_efficacy` | One row per efficacy assessment | response_category, is_responder, change_from_baseline_pct |
| `fact_lab_result` | One row per lab result | result_numeric, is_abnormal, ctcae_grade, change_from_baseline |

### TrialSim Star Schema Diagram

```
                           ┌─────────────────┐
                           │    dim_study    │
                           │  (study attrs)  │
                           └────────┬────────┘
                                    │
           ┌────────────────────────┼────────────────────────┐
           │                        │                        │
           ▼                        ▼                        ▼
    ┌─────────────┐         ┌──────────────┐         ┌──────────────┐
    │  dim_site   │         │dim_treatment_│         │dim_visit_    │
    │(geography)  │         │    arm       │         │  schedule    │
    └──────┬──────┘         └──────┬───────┘         └──────┬───────┘
           │                       │                        │
           └───────────┬───────────┴────────────┬───────────┘
                       │                        │
                       ▼                        │
                ┌─────────────┐                 │
                │ dim_subject │◄────────────────┘
                │(demographics│
                └──────┬──────┘
                       │
    ┌──────────────────┼──────────────────┬──────────────────┐
    │                  │                  │                  │
    ▼                  ▼                  ▼                  ▼
┌────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│    fact_   │  │    fact_    │  │    fact_    │  │    fact_    │
│ enrollment │  │    visit    │  │adverse_event│  │  exposure   │
│(milestones)│  │ (compliance)│  │  (safety)   │  │  (dosing)   │
└────────────┘  └──────┬──────┘  └──────┬──────┘  └─────────────┘
                       │                │
                       │                ▼
                       │         ┌─────────────┐
                       │         │ dim_meddra  │
                       │         │(AE hierarch)│
                       │         └─────────────┘
                       │
            ┌──────────┴──────────┐
            │                     │
            ▼                     ▼
     ┌─────────────┐       ┌─────────────┐
     │fact_efficacy│       │fact_lab_    │
     │ (response)  │       │  result     │
     └─────────────┘       └──────┬──────┘
                                  │
                                  ▼
                           ┌─────────────┐
                           │dim_lab_test │
                           └─────────────┘

Shared:
┌─────────────┐
│  dim_date   │ ◄── All fact tables link here (shared with other products)
│ (calendar)  │
└─────────────┘
```

### TrialSim Dimension DDL

```sql
-- dim_study
CREATE TABLE dim_study (
    study_key INT PRIMARY KEY,
    study_id VARCHAR(50) NOT NULL,
    protocol_title VARCHAR(500),
    phase VARCHAR(20),
    therapeutic_area VARCHAR(100),
    indication VARCHAR(200),
    sponsor VARCHAR(200),
    design_allocation VARCHAR(50),
    design_masking VARCHAR(50),
    enrollment_target INT,
    status VARCHAR(50),
    start_date DATE,
    primary_completion_date DATE
);

-- dim_site
CREATE TABLE dim_site (
    site_key INT PRIMARY KEY,
    site_id VARCHAR(10) NOT NULL,
    study_key INT REFERENCES dim_study(study_key),
    site_name VARCHAR(200),
    country VARCHAR(3),
    region VARCHAR(50),
    pi_name VARCHAR(100),
    status VARCHAR(50),
    activation_date DATE,
    enrollment_target INT
);

-- dim_subject
CREATE TABLE dim_subject (
    subject_key INT PRIMARY KEY,
    usubjid VARCHAR(50) NOT NULL UNIQUE,
    study_key INT REFERENCES dim_study(study_key),
    site_key INT REFERENCES dim_site(site_key),
    arm_key INT REFERENCES dim_treatment_arm(arm_key),
    age INT,
    age_band VARCHAR(20),
    sex VARCHAR(10),
    race VARCHAR(100),
    ethnicity VARCHAR(50),
    screening_date DATE,
    consent_date DATE,
    randomization_date DATE,
    status VARCHAR(50),
    patient_mrn VARCHAR(50)  -- Link to PatientSim
);

-- dim_treatment_arm
CREATE TABLE dim_treatment_arm (
    arm_key INT PRIMARY KEY,
    arm_code VARCHAR(20) NOT NULL,
    arm_name VARCHAR(200),
    arm_type VARCHAR(50),
    study_key INT REFERENCES dim_study(study_key),
    dose VARCHAR(50),
    schedule VARCHAR(50),
    randomization_ratio DECIMAL(3,1)
);

-- dim_visit_schedule
CREATE TABLE dim_visit_schedule (
    visit_schedule_key INT PRIMARY KEY,
    study_key INT REFERENCES dim_study(study_key),
    visit_num DECIMAL(5,1) NOT NULL,
    visit_name VARCHAR(100),
    visit_type VARCHAR(50),
    target_day INT,
    window_before INT,
    window_after INT,
    is_required BOOLEAN
);

-- dim_meddra (separate hierarchy for rollup analytics)
CREATE TABLE dim_meddra (
    meddra_key INT PRIMARY KEY,
    pt_code VARCHAR(10) NOT NULL,
    pt_term VARCHAR(200),
    hlt_code VARCHAR(10),
    hlt_term VARCHAR(200),
    hlgt_code VARCHAR(10),
    hlgt_term VARCHAR(200),
    soc_code VARCHAR(10),
    soc_term VARCHAR(200)
);

-- dim_lab_test
CREATE TABLE dim_lab_test (
    lab_test_key INT PRIMARY KEY,
    lbtestcd VARCHAR(20) NOT NULL,
    lbtest VARCHAR(100),
    lbcat VARCHAR(50),
    loinc_code VARCHAR(20),
    unit_standard VARCHAR(20),
    normal_lo DECIMAL(10,3),
    normal_hi DECIMAL(10,3)
);
```

### TrialSim Fact DDL

```sql
-- fact_enrollment (grain: 1 row per subject)
CREATE TABLE fact_enrollment (
    enrollment_key INT PRIMARY KEY,
    subject_key INT REFERENCES dim_subject(subject_key),
    study_key INT REFERENCES dim_study(study_key),
    site_key INT REFERENCES dim_site(site_key),
    arm_key INT REFERENCES dim_treatment_arm(arm_key),
    screening_date_key INT REFERENCES dim_date(date_key),
    consent_date_key INT REFERENCES dim_date(date_key),
    randomization_date_key INT REFERENCES dim_date(date_key),
    days_screen_to_consent INT,
    days_consent_to_randomization INT,
    screen_failure_flag BOOLEAN,
    screen_failure_reason VARCHAR(200),
    is_randomized BOOLEAN,
    is_completed BOOLEAN,
    is_discontinued BOOLEAN,
    discontinuation_reason VARCHAR(200)
);

-- fact_visit (grain: 1 row per actual visit)
CREATE TABLE fact_visit (
    visit_key INT PRIMARY KEY,
    subject_key INT REFERENCES dim_subject(subject_key),
    study_key INT REFERENCES dim_study(study_key),
    site_key INT REFERENCES dim_site(site_key),
    visit_schedule_key INT REFERENCES dim_visit_schedule(visit_schedule_key),
    visit_date_key INT REFERENCES dim_date(date_key),
    visit_num DECIMAL(5,1),
    study_day INT,
    window_deviation_days INT,
    is_within_window BOOLEAN,
    visit_status VARCHAR(50),
    assessments_planned INT,
    assessments_completed INT
);

-- fact_adverse_event (grain: 1 row per AE)
CREATE TABLE fact_adverse_event (
    ae_key INT PRIMARY KEY,
    subject_key INT REFERENCES dim_subject(subject_key),
    study_key INT REFERENCES dim_study(study_key),
    site_key INT REFERENCES dim_site(site_key),
    arm_key INT REFERENCES dim_treatment_arm(arm_key),
    meddra_key INT REFERENCES dim_meddra(meddra_key),
    onset_date_key INT REFERENCES dim_date(date_key),
    resolution_date_key INT REFERENCES dim_date(date_key),
    aeseq INT,
    aeterm VARCHAR(200),
    severity VARCHAR(20),
    ctcae_grade INT,
    is_serious BOOLEAN,
    is_related BOOLEAN,
    is_treatment_emergent BOOLEAN,
    duration_days INT,
    action_taken VARCHAR(50),
    outcome VARCHAR(50)
);

-- fact_exposure (grain: 1 row per dosing record)
CREATE TABLE fact_exposure (
    exposure_key INT PRIMARY KEY,
    subject_key INT REFERENCES dim_subject(subject_key),
    study_key INT REFERENCES dim_study(study_key),
    arm_key INT REFERENCES dim_treatment_arm(arm_key),
    start_date_key INT REFERENCES dim_date(date_key),
    end_date_key INT REFERENCES dim_date(date_key),
    exseq INT,
    treatment_name VARCHAR(100),
    dose_administered DECIMAL(10,3),
    dose_unit VARCHAR(20),
    dose_planned DECIMAL(10,3),
    dose_percent DECIMAL(5,2),
    is_dose_reduction BOOLEAN,
    is_dose_delay BOOLEAN,
    is_dose_interruption BOOLEAN,
    duration_days INT,
    cumulative_dose DECIMAL(10,3)
);

-- fact_efficacy (grain: 1 row per assessment)
CREATE TABLE fact_efficacy (
    efficacy_key INT PRIMARY KEY,
    subject_key INT REFERENCES dim_subject(subject_key),
    study_key INT REFERENCES dim_study(study_key),
    arm_key INT REFERENCES dim_treatment_arm(arm_key),
    visit_key INT REFERENCES fact_visit(visit_key),
    assessment_date_key INT REFERENCES dim_date(date_key),
    assessment_type VARCHAR(50),
    visitnum DECIMAL(5,1),
    response_category VARCHAR(20),
    is_responder BOOLEAN,
    target_lesion_sum DECIMAL(10,2),
    change_from_baseline_pct DECIMAL(5,2),
    is_confirmed_response BOOLEAN,
    new_lesions_flag BOOLEAN,
    score_value DECIMAL(10,2),
    score_change DECIMAL(10,2)
);

-- fact_lab_result (grain: 1 row per result)
CREATE TABLE fact_lab_result (
    lab_result_key INT PRIMARY KEY,
    subject_key INT REFERENCES dim_subject(subject_key),
    study_key INT REFERENCES dim_study(study_key),
    lab_test_key INT REFERENCES dim_lab_test(lab_test_key),
    visit_key INT REFERENCES fact_visit(visit_key),
    collection_date_key INT REFERENCES dim_date(date_key),
    lbseq INT,
    result_numeric DECIMAL(15,5),
    result_character VARCHAR(50),
    result_unit VARCHAR(20),
    is_baseline BOOLEAN,
    baseline_value DECIMAL(15,5),
    change_from_baseline DECIMAL(15,5),
    pct_change_from_baseline DECIMAL(10,2),
    is_abnormal BOOLEAN,
    is_low BOOLEAN,
    is_high BOOLEAN,
    ctcae_grade INT,
    is_clinically_significant BOOLEAN
);
```

### TrialSim Analytics Queries

**Enrollment Velocity by Site:**
```sql
SELECT 
    s.site_name,
    s.country,
    COUNT(*) as subjects_screened,
    SUM(CASE WHEN f.is_randomized THEN 1 ELSE 0 END) as subjects_randomized,
    AVG(f.days_consent_to_randomization) as avg_days_to_randomize,
    ROUND(100.0 * SUM(CASE WHEN f.screen_failure_flag THEN 1 ELSE 0 END) / COUNT(*), 1) as screen_failure_rate_pct
FROM fact_enrollment f
JOIN dim_site s ON f.site_key = s.site_key
GROUP BY s.site_name, s.country
ORDER BY subjects_randomized DESC;
```

**Safety: AE Rates by Treatment Arm and SOC:**
```sql
SELECT
    a.arm_name,
    m.soc_term as system_organ_class,
    COUNT(DISTINCT f.ae_key) as ae_count,
    COUNT(DISTINCT f.subject_key) as subjects_with_ae,
    SUM(CASE WHEN f.is_serious THEN 1 ELSE 0 END) as serious_ae_count,
    SUM(CASE WHEN f.ctcae_grade >= 3 THEN 1 ELSE 0 END) as grade_3_plus_count
FROM fact_adverse_event f
JOIN dim_treatment_arm a ON f.arm_key = a.arm_key
JOIN dim_meddra m ON f.meddra_key = m.meddra_key
WHERE f.is_treatment_emergent = true
GROUP BY a.arm_name, m.soc_term
ORDER BY a.arm_name, ae_count DESC;
```

**Efficacy: Response Rate (ORR) by Treatment Arm:**
```sql
SELECT
    a.arm_name,
    a.arm_type,
    COUNT(DISTINCT f.subject_key) as evaluable_subjects,
    SUM(CASE WHEN f.response_category = 'CR' THEN 1 ELSE 0 END) as complete_response,
    SUM(CASE WHEN f.response_category = 'PR' THEN 1 ELSE 0 END) as partial_response,
    SUM(CASE WHEN f.is_responder THEN 1 ELSE 0 END) as total_responders,
    ROUND(100.0 * SUM(CASE WHEN f.is_responder THEN 1 ELSE 0 END) / 
        COUNT(DISTINCT f.subject_key), 1) as orr_pct
FROM fact_efficacy f
JOIN dim_treatment_arm a ON f.arm_key = a.arm_key
WHERE f.assessment_type = 'RECIST'
  AND f.is_confirmed_response = true
GROUP BY a.arm_name, a.arm_type
ORDER BY orr_pct DESC;
```

**Visit Compliance by Site:**
```sql
SELECT
    s.site_name,
    COUNT(*) as total_visits,
    SUM(CASE WHEN f.is_within_window THEN 1 ELSE 0 END) as on_schedule,
    ROUND(100.0 * SUM(CASE WHEN f.is_within_window THEN 1 ELSE 0 END) / COUNT(*), 1) as compliance_rate_pct,
    AVG(ABS(f.window_deviation_days)) as avg_deviation_days
FROM fact_visit f
JOIN dim_site s ON f.site_key = s.site_key
GROUP BY s.site_name
ORDER BY compliance_rate_pct DESC;
```

### TrialSim Cross-Product Analytics

The `dim_subject.patient_mrn` field enables joining trial analytics with PatientSim clinical data:

**Example: Baseline Characteristics vs Response**
```sql
-- Join TrialSim subjects with PatientSim patient data
SELECT
    CASE 
        WHEN p.baseline_tumor_size < 50 THEN 'Low Burden (<50mm)'
        WHEN p.baseline_tumor_size < 100 THEN 'Medium Burden (50-100mm)'
        ELSE 'High Burden (>100mm)'
    END as baseline_tumor_category,
    COUNT(DISTINCT ts.subject_key) as subjects,
    SUM(CASE WHEN fe.is_responder THEN 1 ELSE 0 END) as responders,
    ROUND(100.0 * SUM(CASE WHEN fe.is_responder THEN 1 ELSE 0 END) / 
        COUNT(DISTINCT ts.subject_key), 1) as response_rate_pct
FROM trialsim.dim_subject ts
JOIN patientsim.dim_patient p ON ts.patient_mrn = p.mrn
JOIN trialsim.fact_efficacy fe ON ts.subject_key = fe.subject_key
WHERE fe.assessment_type = 'RECIST'
GROUP BY 1
ORDER BY response_rate_pct DESC;
```

### TrialSim Platform Notes

**DuckDB (Primary):**
```sql
CREATE SCHEMA IF NOT EXISTS trialsim;
-- Use trialsim.dim_study, trialsim.fact_enrollment, etc.
```

**Enterprise Platforms (Future):**
Enterprise export to Databricks, Snowflake, and MotherDuck is planned for Phase 3. See "Enterprise Cloud Platforms" section above.

---

## Related Skills

- [../skills/patientsim/SKILL.md](../skills/patientsim/SKILL.md) - Clinical data generation
- [../skills/membersim/SKILL.md](../skills/membersim/SKILL.md) - Claims data generation
- [../skills/rxmembersim/SKILL.md](../skills/rxmembersim/SKILL.md) - Pharmacy data generation
- [sql.md](sql.md) - SQL INSERT format (transactional, not dimensional)
- [csv.md](csv.md) - CSV export format
