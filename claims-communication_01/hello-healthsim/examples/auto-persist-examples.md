# Auto-Persist Examples

_Token-efficient scenario management for large batch operations._

## Overview

When generating large datasets (50+ entities), auto-persist saves data to DuckDB and returns a compact summary instead of flooding the conversation with hundreds of JSON objects. Query for specific data as needed.

**When to Use Auto-Persist**:
- Generating 50+ entities at once
- Building large cohorts for training or testing
- Batch generation workflows
- Long sessions where context efficiency matters

**Traditional vs Auto-Persist**:

| Approach | Use Case | What You See |
|----------|----------|--------------|
| Traditional | Small scenarios (<50 entities) | Full data in conversation |
| Auto-Persist | Large batches (50+ entities) | Summary + query on demand |

---

## Example 1: Generate Large Member Cohort

### Prompt
```
Generate 100 Medicare Advantage members over 65 in California
```

### Response
```
Generated and saved "medicare-ca-20241228":

| Metric | Value |
|--------|-------|
| Members | 100 |
| Age Range | 65-89 |
| Gender | 48 male, 52 female |
| Plan Types | HMO (40), PPO (35), PFFS (25) |

Top counties: Los Angeles (28), San Diego (18), Orange (15)

The data is saved. Would you like to:
- Query specific subsets ("show members in San Diego")
- See sample members ("show me 3 examples")
- Generate claims for these members
```

---

## Example 2: Query Saved Data

### Prompt
```
From my Medicare scenario, show female members over 75 with diabetes
```

### Response
```
Found 12 matching members:

| Name | Age | City | Plan | Risk Score |
|------|-----|------|------|------------|
| Margaret Wilson | 78 | San Diego | HMO | 1.85 |
| Dorothy Chen | 82 | Los Angeles | PPO | 2.12 |
| Patricia Johnson | 76 | San Francisco | HMO | 1.45 |
| Betty Martinez | 79 | Sacramento | PFFS | 1.92 |
| Ruth Anderson | 81 | Fresno | PPO | 2.34 |

Showing 5 of 12. Say "show more" for the rest.

These high-risk members may benefit from care management programs.
```

---

## Example 3: Resume Work with Summary

### Prompt
```
Load my diabetes cohort from yesterday
```

### Response
```
"diabetes-cohort-20241227" summary:

| Entity Type | Count |
|-------------|-------|
| Patients | 150 |
| Encounters | 425 |
| Lab Results | 890 |
| Medications | 320 |

**Demographics**:
- Age range: 35-78 years
- Gender: 72 male, 78 female

**Clinical Characteristics**:
- Average A1C: 7.8% (range: 6.1-12.4%)
- With complications: 67 (45%)
- On insulin: 43 (29%)

What would you like to do?
- Query specific patients
- Generate additional encounters
- Export for analysis
```

---

## Example 4: Get Sample Entities

### Prompt
```
Show me a few example patients from that cohort
```

### Response
```
Here are 3 representative patients:

---

**1. Maria Gonzalez** (Female, 58)
- MRN: P-2024-00847
- Diagnosis: Type 2 DM with hyperglycemia
- Latest A1C: 8.2% (2024-02-15)
- Medications: Metformin 1000mg BID, Jardiance 10mg daily
- Comorbidities: Hypertension, Obesity
- Last Visit: 2024-02-15 (routine follow-up)

---

**2. James Thompson** (Male, 67)
- MRN: P-2024-01234
- Diagnosis: Type 2 DM without complications
- Latest A1C: 6.8% (2024-01-20) - well controlled
- Medications: Metformin 500mg BID
- Comorbidities: None
- Last Visit: 2024-01-20 (annual wellness)

---

**3. Patricia Lee** (Female, 72)
- MRN: P-2024-00623
- Diagnosis: Type 2 DM with nephropathy
- Latest A1C: 10.1% (2024-03-01) - poor control
- Medications: Insulin glargine 30u qHS, Humalog sliding scale
- Comorbidities: CKD Stage 3, Retinopathy
- Last Visit: 2024-03-01 (post-hospitalization)

---

Want to see more samples or query for specific criteria?
```

---

## Example 5: Generate Clinical Trial Scenario

### Prompt
```
Generate a Phase 3 oncology trial with 200 subjects
```

### Response
```
Generated and saved "oncology-phase3-20241228":

**Study**: ONCO-2024-001 (Phase 3 NSCLC)

| Attribute | Value |
|-----------|-------|
| Sites | 8 |
| Subjects | 200 |
| Treatment Arms | Active (100), Control (100) |

**Visit Statistics**:
- Scheduled visits: 2,400 (12 per subject)
- Completed visits: 1,847 (77%)
- Adverse events: 89 (32 subjects affected)

**Data Generated**:
| Entity | Count |
|--------|-------|
| Subjects | 200 |
| Visits | 1,847 |
| Adverse Events | 89 |
| Lab Results | 3,200 |

Would you like to:
- Query subjects by arm or site
- View adverse event details
- Export to CDISC SDTM format
```

---

## Example 6: Cross-Product Query

### Prompt
```
For my diabetes cohort, show patients who also have claims over $10,000
```

### Response
```
Found 23 patients with diabetes AND claims over $10,000:

| Patient | Total Claims | Highest Single Claim | Payer |
|---------|-------------|---------------------|-------|
| Robert Wilson | $45,230 | $28,500 (inpatient) | Medicare |
| Linda Martinez | $32,100 | $15,200 (surgery) | BCBS PPO |
| Michael Chen | $28,750 | $12,400 (ED visit) | Aetna HMO |
| Barbara Johnson | $24,300 | $11,800 (inpatient) | UHC |
| Thomas Brown | $19,450 | $10,500 (procedure) | Medicare |

Showing 5 of 23.

**Insights**:
- Average total claims: $18,420
- Most common high-cost service: Inpatient hospitalization
- Average age of high-cost patients: 68 years

See claim details for any specific patient?
```

---

## Example 7: Tag and Organize Scenarios

### Prompt
```
Tag my Medicare scenario as "training" and "california"
```

### Response
```
Tagged "medicare-ca-20241228":
- training ✓
- california ✓

Find it later with "show scenarios tagged training".
```

### Prompt
```
What tags do I have across my scenarios?
```

### Response
```
Your scenario tags:

| Tag | Scenarios |
|-----|-----------|
| training | 5 |
| production | 3 |
| california | 3 |
| diabetes | 2 |
| validated | 2 |
| testing | 1 |

To find scenarios: "show scenarios tagged [tag]"
To add a tag: "tag [scenario] with [tag]"
```

---

## Example 8: Clone for Testing

### Prompt
```
Clone my diabetes cohort so I can test different analysis approaches
```

### Response
```
Cloned "diabetes-cohort-20241227" → "diabetes-cohort-20241227-copy":

| Entity Type | Copied |
|-------------|--------|
| Patients | 150 |
| Encounters | 425 |
| Lab Results | 890 |
| Medications | 320 |

All entities have new unique IDs. The clone is independent—changes won't affect the original.

Would you like to rename it to something more descriptive?
```

---

## Example 9: Merge Multiple Cohorts

### Prompt
```
Merge my diabetes, heart-failure, and copd scenarios into a combined training set
```

### Response
```
Created "combined-training-20241228" from 3 sources:

| Source | Patients | Encounters | Labs |
|--------|----------|------------|------|
| diabetes-cohort | 150 | 425 | 890 |
| heart-failure-cohort | 120 | 380 | 720 |
| copd-training | 75 | 210 | 450 |
| **Total** | **345** | **1,015** | **2,060** |

- Conflicts resolved: 0 (no duplicate IDs)
- Tags inherited: training, chronic-disease

All source scenarios preserved. Would you like to:
- Query the combined set
- Export for analysis
- Add more scenarios
```

---

## Example 10: Export for Analysis

### Prompt
```
Export my training dataset to CSV for Python analysis
```

### Response
```
Exported "combined-training-20241228" to CSV:

| File | Rows | Size |
|------|------|------|
| patients.csv | 345 | 312 KB |
| encounters.csv | 1,015 | 548 KB |
| lab_results.csv | 2,060 | 1.2 MB |
| diagnoses.csv | 892 | 124 KB |
| medications.csv | 1,240 | 186 KB |

**Location**: ~/Downloads/combined-training-20241228/
**Total**: 2.3 MB

Load in Python:
```python
import pandas as pd

patients = pd.read_csv('~/Downloads/combined-training-20241228/patients.csv')
encounters = pd.read_csv('~/Downloads/combined-training-20241228/encounters.csv')

print(f"Loaded {len(patients)} patients with {len(encounters)} encounters")
```
```

---

## Example 11: Paginated Query Results

### Prompt
```
Show all encounters from January 2024
```

### Response
```
Found 234 encounters in January 2024:

| Date | Patient | Type | Provider | Diagnosis |
|------|---------|------|----------|-----------|
| 2024-01-03 | Maria Gonzalez | Office Visit | Dr. Chen | E11.9 |
| 2024-01-05 | James Thompson | Lab Only | - | E11.65 |
| 2024-01-08 | Robert Wilson | ED Visit | Dr. Patel | I50.9 |
| 2024-01-10 | Patricia Lee | Inpatient | Dr. Kim | E11.22 |
| 2024-01-12 | Linda Martinez | Office Visit | Dr. Chen | I10 |
...

Showing 5 of 234. 

- "show more" - next page
- "show encounters from week of Jan 15" - narrow down
- "count by type" - see breakdown
```

---

## Example 12: Scenario Statistics

### Prompt
```
Give me statistics on my heart failure cohort
```

### Response
```
"heart-failure-cohort" statistics:

**Demographics**:
- Total patients: 120
- Age: mean 68.4, range 45-89
- Gender: 58% male, 42% female
- Race: White (52%), Black (28%), Hispanic (15%), Other (5%)

**Clinical**:
- NYHA Class: I (12%), II (35%), III (38%), IV (15%)
- EF: mean 35%, range 15-55%
- On GDMT: 94 (78%)

**Encounters**:
- Total: 380
- Per patient: mean 3.2, range 1-12
- Types: Office (45%), Inpatient (30%), ED (25%)

**Top Diagnoses**:
1. I50.9 Heart failure, unspecified (120)
2. I10 Essential hypertension (98)
3. E11.9 Type 2 DM (67)
4. N18.3 CKD Stage 3 (45)
5. I25.10 CAD (42)

Would you like to drill into any of these areas?
```

---

## Related Examples

- [Cross-Domain Examples](cross-domain-examples.md) - Multi-product workflows
- [PatientSim Examples](patientsim-examples.md) - Clinical data generation
- [MemberSim Examples](membersim-examples.md) - Claims and payer data
- [TrialSim Examples](trialsim-examples.md) - Clinical trial data

---

*Auto-Persist Examples v3.0 | December 2024*
