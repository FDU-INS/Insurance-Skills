---
name: recruitment-enrollment
description: |
  Generate realistic clinical trial recruitment and enrollment patterns including 
  screening funnels, inclusion/exclusion criteria evaluation, informed consent, 
  screen failures, and randomization. Triggers: "screening", "enrollment", 
  "recruit", "screen failure", "consent", "eligibility", "I/E criteria".
---

# Recruitment & Enrollment

Generate realistic clinical trial recruitment funnels, screening patterns, and enrollment data. This skill bridges PatientSim patients to TrialSim subjects through the screening and consent process.

---

## For Claude

This is an **operational skill** for generating recruitment and enrollment data. Apply this when users want screening funnels, screen failures, consent workflows, or enrollment patterns.

**Always apply this skill when you see:**
- References to screening, pre-screening, or enrollment
- Requests for screen failures or screen failure rates
- Mentions of informed consent or ICF
- Inclusion/exclusion criteria evaluation
- Enrollment funnel or recruitment metrics
- Randomization or treatment assignment

**Combine with:**
- Phase cohort skills for trial-specific I/E criteria
- Therapeutic area skills for indication-specific eligibility
- PatientSim for source patient demographics

---

## When to Use This Skill

Use this skill when the user:
- Wants to generate screening and enrollment data
- Needs realistic screen failure rates and reasons
- Asks about informed consent patterns
- Wants to see the journey from patient to subject
- Needs enrollment velocity patterns by site
- Requests randomization with stratification

---

## Example Requests → Responses

| User Says | Claude Interprets | Key Features to Generate |
|-----------|-------------------|--------------------------|
| "Generate screening data for 100 subjects" | Enrollment funnel | Pre-screen, consent, eligibility, screen pass/fail |
| "Show me screen failures" | Failed eligibility | Subjects who didn't meet I/E criteria with reasons |
| "30% screen failure rate" | Controlled funnel | Adjusted proportions of pass/fail |
| "Screen failures for an oncology trial" | Indication-specific | Cancer-relevant exclusion reasons |
| "Enrollment by site" | Site performance | Variable enrollment rates across sites |
| "Subjects with consent withdrawn" | Early dropout | Consent withdrawal before randomization |

---

## The Recruitment Funnel

### Funnel Stages

```
Clinical Trial Recruitment Funnel
==================================

IDENTIFIED (100%)
  Potential subjects from referrals, EMR, advertising, patient databases
       |
       | ✗ 40-60% drop: No contact, not interested, ineligible on basic criteria
       v
PRE-SCREENED (40-60%)
  Initial eligibility check (phone/chart), Basic I/E criteria review
       |
       | ✗ 10-20% drop: Declined consent, logistics, changed mind
       v
CONSENTED (30-40%)
  Signed informed consent form, Entered screening period
       |
       | ✗ 5-15% drop: Failed screening labs/imaging, disease criteria not met
       v
SCREEN PASSED (20-30%)
  Met all I/E criteria, Eligible for enrollment
       |
       | ✗ 2-5% drop: Withdrew before randomization, slot not available
       v
RANDOMIZED (15-25%)
  Assigned to treatment arm, Officially enrolled
```

### Funnel Benchmarks by Therapeutic Area

| Therapeutic Area | Screen Failure Rate | Top Failure Reasons |
|------------------|---------------------|---------------------|
| **Oncology** | 25-40% | Wrong stage/histology, prior therapy, organ function |
| **Cardiovascular** | 20-35% | Ejection fraction, comorbidities, concomitant meds |
| **CNS/Neurology** | 30-45% | Cognitive scores, disease duration, MRI findings |
| **Diabetes/Metabolic** | 15-25% | HbA1c range, renal function, cardiovascular history |
| **Rare Disease** | 35-50% | Genetic confirmation, disease severity, prior treatment |
| **Healthy Volunteers** | 10-20% | Labs, ECG, drug screen, medical history |


---

## Screen Failure Reasons

### Categorized Failure Reasons

**Category 1: Disease-Related (30-40% of failures)**

| Reason Code | Description | Example |
|-------------|-------------|---------|
| `IE01` | Wrong disease stage | Stage II when Stage III required |
| `IE02` | Wrong histology/subtype | Squamous when adenocarcinoma required |
| `IE03` | Disease duration | Diagnosed <6 months when ≥1 year required |
| `IE04` | Prior therapy conflict | Received excluded prior treatment |
| `IE05` | Disease severity | NYHA Class II when Class III required |

**Category 2: Laboratory/Clinical (20-30% of failures)**

| Reason Code | Description | Example |
|-------------|-------------|---------|
| `IE10` | Inadequate organ function | Creatinine clearance <60 mL/min |
| `IE11` | Hematologic values | ANC <1500/μL, platelets <100K |
| `IE12` | Hepatic function | AST/ALT >2.5× ULN |
| `IE13` | Cardiac function | LVEF <50%, QTc >470ms |
| `IE14` | Vital signs | Uncontrolled hypertension |

**Category 3: Medical History (15-25% of failures)**

| Reason Code | Description | Example |
|-------------|-------------|---------|
| `IE20` | Excluded comorbidity | Active autoimmune disease |
| `IE21` | Prior malignancy | Cancer within 5 years |
| `IE22` | CNS involvement | Untreated brain metastases |
| `IE23` | Infection | Active hepatitis B/C, HIV |
| `IE24` | Cardiovascular history | MI within 6 months |

**Category 4: Administrative/Consent (10-15% of failures)**

| Reason Code | Description | Example |
|-------------|-------------|---------|
| `IE30` | Consent withdrawn | Subject changed mind |
| `IE31` | Lost to follow-up | Could not contact for screening |
| `IE32` | Investigator decision | Clinical judgment |
| `IE33` | Logistics | Unable to comply with visit schedule |
| `IE34` | Competing trial | Enrolled in another study |

---

## Informed Consent

### Consent Elements

| Element | Description | Data Captured |
|---------|-------------|---------------|
| **ICF Version** | Document version number | `ICF v3.0 dated 2024-01-15` |
| **Consent Date** | Date subject signed | ISO 8601 date |
| **Consenter** | Who signed | Subject, LAR, or both |
| **Witness** | Independent witness | Name and signature date |
| **Language** | ICF language version | English, Spanish, etc. |
| **Optional Consents** | Additional permissions | Biomarker, genetics, future research |

### Consent Patterns

```json
{
  "informed_consent": {
    "icf_version": "3.0",
    "icf_date": "2024-01-15",
    "consent_date": "2024-06-20",
    "consent_time": "14:30:00",
    "consenter_type": "SUBJECT",
    "consenter_name": "Maria Garcia",
    "witness_name": "John Smith",
    "witness_date": "2024-06-20",
    "icf_language": "ENGLISH",
    "optional_consents": {
      "biomarker_research": true,
      "genetic_testing": true,
      "future_research": false,
      "photography": true
    },
    "reconsent_history": []
  }
}
```

### Re-Consent Triggers

| Trigger | Description | Action Required |
|---------|-------------|-----------------|
| Protocol amendment | Significant changes to study | New ICF version, re-consent all active subjects |
| New safety information | Updated risk disclosure | Addendum or new ICF |
| Subject turns 18 | Minor becomes adult | Adult consent form |
| LAR changes | Different legally authorized representative | New consent with new LAR |


---

## Eligibility Assessment

### Standard I/E Criteria Structure

**Inclusion Criteria (must meet ALL):**

| # | Criterion | Assessment Method |
|---|-----------|-------------------|
| I1 | Age ≥18 years | Demographics |
| I2 | Confirmed diagnosis of [disease] | Medical records, pathology |
| I3 | [Disease-specific criterion] | Labs, imaging, clinical exam |
| I4 | ECOG PS 0-1 (oncology) | Clinical assessment |
| I5 | Adequate organ function | Screening labs |
| I6 | Signed informed consent | ICF |

**Exclusion Criteria (must meet NONE):**

| # | Criterion | Assessment Method |
|---|-----------|-------------------|
| E1 | Prior treatment with [drug class] | Medical history |
| E2 | Active autoimmune disease | Medical history, labs |
| E3 | Uncontrolled concurrent illness | Clinical assessment |
| E4 | Pregnancy or lactation | Serum pregnancy test |
| E5 | Known hypersensitivity to [drug] | Medical history |
| E6 | Participation in another interventional trial | Subject interview |

### Eligibility Evaluation Output

```json
{
  "eligibility_assessment": {
    "subject_id": "SCRN-001-0042",
    "assessment_date": "2024-06-25",
    "assessed_by": "Dr. Jane Smith",
    "overall_result": "SCREEN_FAILURE",
    "inclusion_criteria": [
      {"criterion": "I1", "met": true, "value": "67 years", "notes": null},
      {"criterion": "I2", "met": true, "value": "Stage IIIB NSCLC confirmed", "notes": null},
      {"criterion": "I3", "met": true, "value": "PD-L1 TPS 65%", "notes": null},
      {"criterion": "I4", "met": true, "value": "ECOG PS 1", "notes": null},
      {"criterion": "I5", "met": false, "value": "CrCl 42 mL/min", "notes": "Requires ≥50 mL/min"}
    ],
    "exclusion_criteria": [
      {"criterion": "E1", "met": false, "value": null, "notes": "No prior IO therapy"},
      {"criterion": "E2", "met": false, "value": null, "notes": "No autoimmune disease"},
      {"criterion": "E3", "met": true, "value": "Uncontrolled diabetes", "notes": "HbA1c 9.2%"}
    ],
    "failure_reasons": [
      {"code": "IE10", "description": "Inadequate renal function", "criterion": "I5"},
      {"code": "IE20", "description": "Uncontrolled comorbidity", "criterion": "E3"}
    ]
  }
}
```

---

## Randomization

### Randomization Methods

| Method | Description | When to Use |
|--------|-------------|-------------|
| **Simple** | Pure random assignment | Small Phase I studies |
| **Block** | Balanced within blocks | Most Phase II/III trials |
| **Stratified** | Balanced within strata | When prognostic factors matter |
| **Dynamic/Minimization** | Real-time balancing | Complex stratification |

### Stratification Factors (Common)

| Factor | Levels | Typical Trials |
|--------|--------|----------------|
| Region | NA vs EU vs Asia | Global trials |
| ECOG PS | 0 vs 1 | Oncology |
| Prior therapy | Yes vs No | Most trials |
| Disease stage | Early vs Advanced | Oncology |
| Biomarker status | Positive vs Negative | Targeted therapy |
| Sex | Male vs Female | CV, rare disease |
| Age group | <65 vs ≥65 | Geriatric considerations |

### Randomization Output

```json
{
  "randomization": {
    "subject_id": "ABC-001-0001",
    "randomization_date": "2024-06-28",
    "randomization_time": "09:15:00",
    "randomization_number": "R0001",
    "treatment_arm": "A",
    "treatment_description": "Pembrolizumab 200mg IV Q3W",
    "stratification_factors": {
      "region": "NORTH_AMERICA",
      "ecog_ps": "1",
      "histology": "NON_SQUAMOUS"
    },
    "block_id": "BLK-001-003",
    "iwrs_confirmation": "IWRS-2024-0628-001234"
  }
}
```


---

## Site Enrollment Patterns

### Enrollment Velocity by Site Type

| Site Type | Subjects/Month | Characteristics |
|-----------|----------------|-----------------|
| **High Performer** | 4-8 | Academic center, dedicated staff, large patient pool |
| **Average** | 1-3 | Community practice, part-time coordinator |
| **Low/Struggling** | 0-1 | Small practice, competing priorities |
| **Non-enrolling** | 0 | Activated but no subjects (5-10% of sites) |

### Enrollment Timeline Pattern

```
Site Activation: Month 0
├── Slow start (Months 1-2): 0-1 subjects
├── Ramp-up (Months 3-4): 1-2 subjects/month
├── Steady state (Months 5+): Consistent enrollment
└── Tail (final months): Declining as slots fill
```

---

## Generation Patterns

### Pattern 1: Basic Enrollment Funnel

**Request:** "Generate screening data for 100 randomized subjects with 25% screen failure rate"

**Calculation:**
- Target randomized: 100
- Screen failure rate: 25%
- Consented needed: 100 / 0.75 = 134

**Output Distribution:**
| Stage | N | % of Consented |
|-------|---|----------------|
| Consented | 134 | 100% |
| Screen Passed | 100 | 75% |
| Screen Failed | 34 | 25% |

### Pattern 2: Detailed Screen Failures

**Request:** "Generate 50 screen failures for an oncology trial"

**Distribution by Category:**
| Category | N | % | Top Reasons |
|----------|---|---|-------------|
| Disease-related | 18 | 36% | Wrong stage (8), histology (5), prior therapy (5) |
| Laboratory | 14 | 28% | Organ function (8), hematology (6) |
| Medical history | 10 | 20% | Comorbidity (6), prior malignancy (4) |
| Administrative | 8 | 16% | Consent withdrawn (5), lost to FU (3) |

---

## Example: Complete Enrollment Funnel

**Request:** "Generate a complete screening funnel for a Phase III oncology trial targeting 300 randomized subjects"

**Output:**

```json
{
  "study_id": "ONCO-301",
  "enrollment_summary": {
    "target_enrollment": 300,
    "actual_randomized": 300,
    "total_consented": 412,
    "screen_failure_rate": 0.272,
    "enrollment_period": {
      "first_subject_consented": "2024-01-15",
      "last_subject_randomized": "2024-11-22",
      "enrollment_duration_months": 10.2
    }
  },
  "funnel_stages": [
    {"stage": "IDENTIFIED", "n": 892, "conversion_rate": null},
    {"stage": "PRE_SCREENED", "n": 534, "conversion_rate": 0.599},
    {"stage": "CONSENTED", "n": 412, "conversion_rate": 0.772},
    {"stage": "SCREEN_PASSED", "n": 308, "conversion_rate": 0.748},
    {"stage": "RANDOMIZED", "n": 300, "conversion_rate": 0.974}
  ],
  "screen_failures": {
    "total": 112,
    "by_category": {
      "disease_related": {"n": 42, "pct": 0.375},
      "laboratory": {"n": 31, "pct": 0.277},
      "medical_history": {"n": 22, "pct": 0.196},
      "administrative": {"n": 17, "pct": 0.152}
    }
  }
}
```

---

## Validation Checklist

- [ ] Screening IDs follow format: SCRN-{STUDYID}-{NNNN}
- [ ] Consent date ≤ first screening assessment date
- [ ] Screen failure has at least one documented reason
- [ ] Randomization date > consent date
- [ ] Stratification factors are valid for study design
- [ ] Screen failure rate is within realistic range (15-50%)
- [ ] Site enrollment distribution is realistic (Pareto pattern)
- [ ] All I/E criteria are evaluated for screen failures

---

## Related Skills

- [Clinical Trials Domain](clinical-trials-domain.md) - Core trial concepts
- [Phase 3 Pivotal](phase3-pivotal.md) - Pivotal trial cohorts with I/E examples
- [PatientSim](../patientsim/SKILL.md) - Source patient data for screening

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-12 | Initial complete skill with funnel patterns, I/E criteria, examples |
