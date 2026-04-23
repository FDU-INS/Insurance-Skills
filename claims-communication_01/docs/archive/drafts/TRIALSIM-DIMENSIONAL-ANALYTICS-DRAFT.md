# TrialSim Dimensional Analytics - DRAFT

> **Purpose**: This content will be added to `formats/dimensional-analytics.md` after the RxMemberSim section.
> 
> **Review Status**: DRAFT - Pending approval

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

---

## Dimension Table DDL

### dim_study

```sql
CREATE TABLE dim_study (
    study_key INT PRIMARY KEY,
    study_id VARCHAR(50) NOT NULL,
    protocol_title VARCHAR(500),
    protocol_number VARCHAR(50),
    phase VARCHAR(20),
    therapeutic_area VARCHAR(100),
    indication VARCHAR(200),
    sponsor VARCHAR(200),
    study_type VARCHAR(50),
    design_allocation VARCHAR(50),
    design_masking VARCHAR(50),
    design_model VARCHAR(50),
    enrollment_target INT,
    status VARCHAR(50),
    start_date DATE,
    primary_completion_date DATE,
    study_completion_date DATE
);
```

### dim_site

```sql
CREATE TABLE dim_site (
    site_key INT PRIMARY KEY,
    site_id VARCHAR(10) NOT NULL,
    study_key INT REFERENCES dim_study(study_key),
    site_name VARCHAR(200),
    country VARCHAR(3),
    country_name VARCHAR(100),
    region VARCHAR(50),
    pi_name VARCHAR(100),
    pi_specialty VARCHAR(100),
    status VARCHAR(50),
    activation_date DATE,
    enrollment_target INT
);
```

### dim_subject

```sql
CREATE TABLE dim_subject (
    subject_key INT PRIMARY KEY,
    usubjid VARCHAR(50) NOT NULL UNIQUE,
    subject_id VARCHAR(10),
    study_key INT REFERENCES dim_study(study_key),
    site_key INT REFERENCES dim_site(site_key),
    arm_key INT REFERENCES dim_treatment_arm(arm_key),
    age INT,
    age_band VARCHAR(20),
    sex VARCHAR(10),
    race VARCHAR(100),
    ethnicity VARCHAR(50),
    country VARCHAR(3),
    screening_date DATE,
    consent_date DATE,
    randomization_date DATE,
    status VARCHAR(50),
    patient_mrn VARCHAR(50)  -- Link to PatientSim for cross-product analytics
);
```

### dim_treatment_arm

```sql
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
```

### dim_visit_schedule

```sql
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
```

### dim_meddra

MedDRA hierarchy for adverse event analysis and rollup.

```sql
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
```

**MedDRA Hierarchy Levels:**

| Level | Name | Example |
|-------|------|---------|
| SOC | System Organ Class | Gastrointestinal disorders |
| HLGT | High Level Group Term | Gastrointestinal motility and defaecation conditions |
| HLT | High Level Term | Diarrhoea (excl infective) |
| PT | Preferred Term | Diarrhoea |

### dim_lab_test

```sql
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

---

## Fact Table DDL

### fact_enrollment

Grain: One row per subject enrollment milestone.

```sql
CREATE TABLE fact_enrollment (
    enrollment_key INT PRIMARY KEY,
    subject_key INT REFERENCES dim_subject(subject_key),
    study_key INT REFERENCES dim_study(study_key),
    site_key INT REFERENCES dim_site(site_key),
    arm_key INT REFERENCES dim_treatment_arm(arm_key),
    screening_date_key INT REFERENCES dim_date(date_key),
    consent_date_key INT REFERENCES dim_date(date_key),
    randomization_date_key INT REFERENCES dim_date(date_key),
    -- Measures
    days_screen_to_consent INT,
    days_consent_to_randomization INT,
    screen_failure_flag BOOLEAN,
    screen_failure_reason VARCHAR(200),
    is_randomized BOOLEAN,
    is_completed BOOLEAN,
    is_discontinued BOOLEAN,
    discontinuation_reason VARCHAR(200)
);
```

### fact_visit

Grain: One row per actual visit.

```sql
CREATE TABLE fact_visit (
    visit_key INT PRIMARY KEY,
    subject_key INT REFERENCES dim_subject(subject_key),
    study_key INT REFERENCES dim_study(study_key),
    site_key INT REFERENCES dim_site(site_key),
    visit_schedule_key INT REFERENCES dim_visit_schedule(visit_schedule_key),
    visit_date_key INT REFERENCES dim_date(date_key),
    -- Measures
    visit_num DECIMAL(5,1),
    study_day INT,
    window_deviation_days INT,
    is_within_window BOOLEAN,
    visit_status VARCHAR(50),
    assessments_planned INT,
    assessments_completed INT
);
```

### fact_adverse_event

Grain: One row per adverse event occurrence.

```sql
CREATE TABLE fact_adverse_event (
    ae_key INT PRIMARY KEY,
    subject_key INT REFERENCES dim_subject(subject_key),
    study_key INT REFERENCES dim_study(study_key),
    site_key INT REFERENCES dim_site(site_key),
    arm_key INT REFERENCES dim_treatment_arm(arm_key),
    meddra_key INT REFERENCES dim_meddra(meddra_key),
    onset_date_key INT REFERENCES dim_date(date_key),
    resolution_date_key INT REFERENCES dim_date(date_key),
    -- Measures
    aeseq INT,
    aeterm VARCHAR(200),
    severity VARCHAR(20),
    ctcae_grade INT,
    is_serious BOOLEAN,
    is_related BOOLEAN,
    is_treatment_emergent BOOLEAN,
    duration_days INT,
    action_taken VARCHAR(50),
    outcome VARCHAR(50),
    sae_criteria VARCHAR(200)
);
```

### fact_exposure

Grain: One row per dosing record.

```sql
CREATE TABLE fact_exposure (
    exposure_key INT PRIMARY KEY,
    subject_key INT REFERENCES dim_subject(subject_key),
    study_key INT REFERENCES dim_study(study_key),
    arm_key INT REFERENCES dim_treatment_arm(arm_key),
    start_date_key INT REFERENCES dim_date(date_key),
    end_date_key INT REFERENCES dim_date(date_key),
    -- Measures
    exseq INT,
    treatment_name VARCHAR(100),
    dose_administered DECIMAL(10,3),
    dose_unit VARCHAR(20),
    dose_planned DECIMAL(10,3),
    dose_percent DECIMAL(5,2),
    is_dose_reduction BOOLEAN,
    is_dose_delay BOOLEAN,
    is_dose_interruption BOOLEAN,
    dose_modification_reason VARCHAR(100),
    duration_days INT,
    cumulative_dose DECIMAL(10,3)
);
```

### fact_efficacy

Grain: One row per efficacy assessment.

```sql
CREATE TABLE fact_efficacy (
    efficacy_key INT PRIMARY KEY,
    subject_key INT REFERENCES dim_subject(subject_key),
    study_key INT REFERENCES dim_study(study_key),
    arm_key INT REFERENCES dim_treatment_arm(arm_key),
    visit_key INT REFERENCES fact_visit(visit_key),
    assessment_date_key INT REFERENCES dim_date(date_key),
    -- Attributes
    assessment_type VARCHAR(50),
    visitnum DECIMAL(5,1),
    -- Measures
    response_category VARCHAR(20),
    is_responder BOOLEAN,
    target_lesion_sum DECIMAL(10,2),
    change_from_baseline_pct DECIMAL(5,2),
    is_confirmed_response BOOLEAN,
    new_lesions_flag BOOLEAN,
    score_value DECIMAL(10,2),
    score_change DECIMAL(10,2)
);
```

### fact_lab_result

Grain: One row per laboratory result.

```sql
CREATE TABLE fact_lab_result (
    lab_result_key INT PRIMARY KEY,
    subject_key INT REFERENCES dim_subject(subject_key),
    study_key INT REFERENCES dim_study(study_key),
    lab_test_key INT REFERENCES dim_lab_test(lab_test_key),
    visit_key INT REFERENCES fact_visit(visit_key),
    collection_date_key INT REFERENCES dim_date(date_key),
    -- Measures
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

---

## TrialSim Dimensional Model Diagram

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

---

## TrialSim Analytics Queries

### Enrollment Velocity by Site

```sql
SELECT 
    s.site_name,
    s.country,
    COUNT(*) as subjects_screened,
    SUM(CASE WHEN f.is_randomized THEN 1 ELSE 0 END) as subjects_randomized,
    AVG(f.days_consent_to_randomization) as avg_days_to_randomize,
    SUM(CASE WHEN f.screen_failure_flag THEN 1 ELSE 0 END) as screen_failures,
    ROUND(100.0 * SUM(CASE WHEN f.screen_failure_flag THEN 1 ELSE 0 END) / COUNT(*), 1) as screen_failure_rate_pct
FROM fact_enrollment f
JOIN dim_site s ON f.site_key = s.site_key
GROUP BY s.site_name, s.country
ORDER BY subjects_randomized DESC;
```

### Safety: AE Rates by Treatment Arm and SOC

```sql
SELECT
    a.arm_name,
    m.soc_term as system_organ_class,
    COUNT(DISTINCT f.ae_key) as ae_count,
    COUNT(DISTINCT f.subject_key) as subjects_with_ae,
    SUM(CASE WHEN f.is_serious THEN 1 ELSE 0 END) as serious_ae_count,
    SUM(CASE WHEN f.ctcae_grade >= 3 THEN 1 ELSE 0 END) as grade_3_plus_count,
    ROUND(100.0 * COUNT(DISTINCT f.subject_key) / 
        (SELECT COUNT(*) FROM dim_subject WHERE arm_key = a.arm_key), 1) as incidence_pct
FROM fact_adverse_event f
JOIN dim_treatment_arm a ON f.arm_key = a.arm_key
JOIN dim_meddra m ON f.meddra_key = m.meddra_key
WHERE f.is_treatment_emergent = true
GROUP BY a.arm_name, m.soc_term
ORDER BY a.arm_name, ae_count DESC;
```

### Efficacy: Response Rate (ORR) by Treatment Arm

```sql
SELECT
    a.arm_name,
    a.arm_type,
    COUNT(DISTINCT f.subject_key) as evaluable_subjects,
    SUM(CASE WHEN f.response_category = 'CR' THEN 1 ELSE 0 END) as complete_response,
    SUM(CASE WHEN f.response_category = 'PR' THEN 1 ELSE 0 END) as partial_response,
    SUM(CASE WHEN f.is_responder THEN 1 ELSE 0 END) as total_responders,
    ROUND(100.0 * SUM(CASE WHEN f.is_responder THEN 1 ELSE 0 END) / 
        COUNT(DISTINCT f.subject_key), 1) as orr_pct,
    SUM(CASE WHEN f.response_category IN ('CR', 'PR', 'SD') THEN 1 ELSE 0 END) as disease_control,
    ROUND(100.0 * SUM(CASE WHEN f.response_category IN ('CR', 'PR', 'SD') THEN 1 ELSE 0 END) / 
        COUNT(DISTINCT f.subject_key), 1) as dcr_pct
FROM fact_efficacy f
JOIN dim_treatment_arm a ON f.arm_key = a.arm_key
WHERE f.assessment_type = 'RECIST'
  AND f.is_confirmed_response = true
GROUP BY a.arm_name, a.arm_type
ORDER BY orr_pct DESC;
```

### Site Performance: Visit Compliance

```sql
SELECT
    s.site_name,
    s.country,
    COUNT(*) as total_visits,
    SUM(CASE WHEN f.is_within_window THEN 1 ELSE 0 END) as on_schedule,
    ROUND(100.0 * SUM(CASE WHEN f.is_within_window THEN 1 ELSE 0 END) / COUNT(*), 1) as compliance_rate_pct,
    AVG(ABS(f.window_deviation_days)) as avg_deviation_days,
    SUM(CASE WHEN f.visit_status = 'Missed' THEN 1 ELSE 0 END) as missed_visits
FROM fact_visit f
JOIN dim_site s ON f.site_key = s.site_key
WHERE f.visit_status IN ('Completed', 'Missed', 'Partially Completed')
GROUP BY s.site_name, s.country
ORDER BY compliance_rate_pct DESC;
```

### Dose Intensity Analysis

```sql
SELECT
    a.arm_name,
    COUNT(DISTINCT f.subject_key) as subjects,
    AVG(f.dose_percent) as avg_dose_intensity_pct,
    SUM(CASE WHEN f.is_dose_reduction THEN 1 ELSE 0 END) as dose_reductions,
    SUM(CASE WHEN f.is_dose_delay THEN 1 ELSE 0 END) as dose_delays,
    SUM(CASE WHEN f.is_dose_interruption THEN 1 ELSE 0 END) as dose_interruptions,
    ROUND(100.0 * SUM(CASE WHEN f.is_dose_reduction OR f.is_dose_delay OR f.is_dose_interruption THEN 1 ELSE 0 END) / 
        COUNT(*), 1) as any_modification_pct
FROM fact_exposure f
JOIN dim_treatment_arm a ON f.arm_key = a.arm_key
GROUP BY a.arm_name
ORDER BY avg_dose_intensity_pct DESC;
```

### Safety Labs: Grade 3+ Lab Abnormalities by Arm

```sql
SELECT
    a.arm_name,
    t.lbcat as lab_category,
    t.lbtest as lab_test,
    COUNT(*) as total_results,
    SUM(CASE WHEN f.ctcae_grade >= 3 THEN 1 ELSE 0 END) as grade_3_plus,
    ROUND(100.0 * SUM(CASE WHEN f.ctcae_grade >= 3 THEN 1 ELSE 0 END) / COUNT(*), 2) as grade_3_plus_pct
FROM fact_lab_result f
JOIN dim_treatment_arm a ON f.study_key = a.study_key
JOIN dim_subject sub ON f.subject_key = sub.subject_key AND sub.arm_key = a.arm_key
JOIN dim_lab_test t ON f.lab_test_key = t.lab_test_key
WHERE f.is_baseline = false
GROUP BY a.arm_name, t.lbcat, t.lbtest
HAVING SUM(CASE WHEN f.ctcae_grade >= 3 THEN 1 ELSE 0 END) > 0
ORDER BY a.arm_name, grade_3_plus_pct DESC;
```

---

## Cross-Product Analytics

### TrialSim + PatientSim Integration

The `dim_subject.patient_mrn` field enables joining trial analytics with PatientSim clinical data for deeper insights.

**Use Cases:**
- Correlate baseline disease characteristics with trial outcomes
- Link trial adverse events with prior medical history
- Analyze EMR source data alongside trial CRF data

### Cross-Product: Baseline Characteristics vs Response

Compare baseline disease burden (from PatientSim) against trial efficacy (from TrialSim):

```sql
-- Join TrialSim subjects with PatientSim patient data
-- Analyze whether baseline tumor burden correlates with response

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
FROM dim_subject ts
-- Cross-product join to PatientSim
JOIN healthsim.gold.dim_patient p ON ts.patient_mrn = p.mrn
JOIN fact_efficacy fe ON ts.subject_key = fe.subject_key
WHERE fe.assessment_type = 'RECIST'
  AND fe.is_confirmed_response = true
GROUP BY 1
ORDER BY response_rate_pct DESC;
```

### Cross-Product: Prior Therapy Impact on Safety

Analyze whether prior therapies (from PatientSim) correlate with adverse events in the trial:

```sql
-- Subjects with prior chemotherapy vs treatment-naive
-- Compare AE profiles

WITH subject_prior_therapy AS (
    SELECT 
        ts.subject_key,
        ts.usubjid,
        CASE WHEN COUNT(pm.medication_key) > 0 THEN 'Prior Chemo' ELSE 'Treatment Naive' END as prior_therapy_status
    FROM dim_subject ts
    JOIN healthsim.gold.dim_patient p ON ts.patient_mrn = p.mrn
    LEFT JOIN healthsim.gold.fact_medications pm ON p.patient_key = pm.patient_key
        AND pm.therapeutic_class LIKE '%antineoplastic%'
        AND pm.start_date_key < (SELECT date_key FROM dim_date WHERE full_date = ts.screening_date)
    GROUP BY ts.subject_key, ts.usubjid
)
SELECT
    spt.prior_therapy_status,
    m.soc_term,
    COUNT(*) as ae_count,
    SUM(CASE WHEN fae.is_serious THEN 1 ELSE 0 END) as serious_ae_count
FROM subject_prior_therapy spt
JOIN fact_adverse_event fae ON spt.subject_key = fae.subject_key
JOIN dim_meddra m ON fae.meddra_key = m.meddra_key
GROUP BY spt.prior_therapy_status, m.soc_term
ORDER BY spt.prior_therapy_status, ae_count DESC;
```

---

## Platform-Specific Notes

### DuckDB (Local Development)

```sql
-- Create TrialSim schema
CREATE SCHEMA IF NOT EXISTS trialsim;

-- Example: Load dimensions first, then facts
-- (DDL from above, prefixed with trialsim.)
```

**Conversation Example:**
```
User: Generate 50 subjects for a Phase 3 oncology trial and load to DuckDB for analytics

Claude: I'll generate the trial data and create the dimensional model...
[Generates canonical entities → transforms to star schema → executes SQL]
```

### Databricks (Enterprise)

```sql
-- Use Unity Catalog
CREATE CATALOG IF NOT EXISTS healthsim;
CREATE SCHEMA IF NOT EXISTS healthsim.gold;

-- Tables created as Delta tables
-- (DDL from above, prefixed with healthsim.gold.trialsim_)
```

**Conversation Example:**
```
User: Generate 200 subjects for a Phase 2 CNS trial and load to Databricks 
      catalog 'dev_catalog' schema 'analytics'

Claude: I see you're authenticated to Databricks. Let me:
1. Generate the trial data in canonical format
2. Transform to dimensional model
3. Create/update tables via SQL Statements API
[Executes via databricks api]
```

---

## Example: Complete DuckDB Workflow

```
User: Generate a Phase 3 cardiovascular outcomes trial with:
      - 300 subjects
      - 2:1 randomization (treatment:placebo)  
      - 12-month follow-up
      - MACE endpoint
      
      Load to DuckDB as star schema for safety analysis.

Claude: I'll generate the trial and create the dimensional model for analytics.

Step 1: Generating canonical entities...
- Study: CV-OUTCOMES-001, Phase 3, MACE primary endpoint
- Sites: 25 sites across NA and EU
- Subjects: 300 (200 treatment, 100 placebo)
- Adverse Events: 847 total (including 23 MACE events)
- Efficacy: MACE adjudication records

Step 2: Transforming to star schema...
- dim_study: 1 row
- dim_site: 25 rows
- dim_subject: 300 rows
- dim_treatment_arm: 2 rows
- dim_meddra: 156 unique PTs
- fact_enrollment: 300 rows
- fact_adverse_event: 847 rows
- fact_efficacy: 312 assessments

Step 3: Loading to DuckDB...
[CREATE TABLE and INSERT statements executed]

Ready for analysis. Try:
- "Show me MACE event rates by treatment arm"
- "Which sites have the highest SAE rates?"
- "What's the enrollment velocity trend?"
```

---

## Related Skills

- `skills/trialsim/SKILL.md` - TrialSim master skill
- `formats/cdisc-sdtm.md` - SDTM output format (regulatory)
- `formats/cdisc-adam.md` - ADaM output format (analysis)
- `formats/dimensional-analytics.md` - This document (analytics)
