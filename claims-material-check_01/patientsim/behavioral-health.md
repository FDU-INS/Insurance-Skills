---
name: behavioral-health
description: "Mental health and substance use disorders - depression, anxiety, bipolar, PTSD, SUD. Triggers: depression, anxiety, bipolar, PTSD, mental health, psychiatric, antidepressants, mood stabilizers, substance use, addiction, therapy, PHQ-9, GAD-7"
---

# Behavioral Health Clinical Cohort

A cohort template for generating patients with mental health and substance use disorders, including depression, anxiety, bipolar disorder, PTSD, and substance use disorders.

## For Claude

Use this skill when the user requests behavioral health patients or mental health clinical cohorts. This teaches you how to generate **realistic clinical presentations** for psychiatric conditions across the spectrum from mild anxiety to complex multi-diagnosis patients.

**When to apply this skill:**
- User mentions depression, anxiety, bipolar, PTSD, or mental health
- User requests psychiatric patient data or behavioral health cohorts
- User specifies antidepressants, mood stabilizers, or psychiatric medications
- User asks for substance use disorder or addiction cohorts
- User needs therapy or counseling visit documentation
- User mentions PHQ-9, GAD-7, or other psychiatric screening tools

**Key capabilities this skill provides:**
- How to generate clinically accurate psychiatric diagnoses with appropriate severity levels
- How to match symptoms to diagnostic criteria (DSM-5 aligned)
- How to apply appropriate medication regimens for each condition
- How to create realistic psychiatric assessment scores (PHQ-9, GAD-7, Columbia)
- How to model treatment progression and response
- How to handle comorbid psychiatric conditions

## Metadata
- **Type**: cohort-template
- **Version**: 1.0
- **Author**: PatientSim
- **Tags**: behavioral-health, psychiatry, mental-health, substance-use, primary-care
- **Updated**: 2025-01-15

## Purpose

This cohort generates realistic behavioral health patients across the spectrum of psychiatric conditions. It models clinical presentations, symptom severity, treatment response, and comorbidity patterns for depression, anxiety, bipolar disorder, PTSD, and substance use disorders.

## When to Use This Skill

Apply this skill when the user's request involves:

**Direct Keywords**:
- "depression", "depressed", "MDD", "major depression"
- "anxiety", "anxious", "GAD", "panic"
- "bipolar", "manic", "mood disorder"
- "PTSD", "trauma", "post-traumatic"
- "substance abuse", "SUD", "addiction", "alcohol use"
- "mental health", "psychiatric", "behavioral health"

**Clinical Cohorts**:
- "Generate a patient with depression"
- "Create a patient with anxiety and insomnia"
- "Generate a patient in recovery from opioid use"
- "Model treatment response over 6 months"

## Generation Guidelines

When generating behavioral health patients:
1. **Match severity to diagnosis code**: Mild (F32.0), Moderate (F32.1), Severe (F32.2)
2. **Include screening scores**: PHQ-9 for depression, GAD-7 for anxiety
3. **Apply comorbidities**: Anxiety + Depression (60%), SUD + Depression (40%)
4. **Progress treatment appropriately**: SSRI start → titration → switch if needed
5. **Include relevant vitals/labs**: Weight (for medication monitoring), metabolic panel (for antipsychotics)

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| age_range | range | 18-65 | Patient age range |
| condition_type | enum | depression | depression, anxiety, bipolar, ptsd, sud, schizophrenia |
| severity | enum | moderate | mild, moderate, severe |
| has_comorbidity | boolean | false | Include psychiatric comorbidities |
| treatment_phase | enum | active | new-diagnosis, active, maintenance, remission |
| substance_type | enum | none | none, alcohol, opioid, cannabis, stimulant |
| geography | string | null | County/tract FIPS for data-driven rates |

## Data Sources (PopulationSim v2.0)

When geography is specified, behavioral health cohorts use real CDC PLACES data:

### Embedded Data Lookup

```
File: skills/populationsim/data/county/places_county_2024.csv
Behavioral health columns:
  - DEPRESSION_CrudePrev: Depression prevalence (%)
  - BINGE_CrudePrev: Binge drinking (proxy for alcohol use)
  - SLEEP_CrudePrev: Short sleep (<7 hrs, correlates with MH)
  - GHLTH_CrudePrev: Fair/poor general health
```

### Data-Driven Rates

| Measure | PLACES Column | National Avg |
|---------|---------------|--------------|
| Depression | DEPRESSION_CrudePrev | 18.6% |
| Binge drinking | BINGE_CrudePrev | 16.8% |
| Poor mental health days | (not in PLACES) | Use SVI proxy |

### SDOH Context for Behavioral Health

SVI factors significantly affect behavioral health outcomes:

```
File: skills/populationsim/data/county/svi_county_2022.csv
Relevant columns:
  - RPL_THEMES: Overall vulnerability
  - EP_POV150: Poverty (access barriers)
  - EP_UNINSUR: Uninsured (treatment access)
  - EP_SNGPNT: Single-parent households (support systems)
```

**Higher SVI correlates with:**
- Lower treatment engagement
- Higher severity at presentation
- More ED utilization for MH crises
- Lower medication adherence

## Generation Rules

### Demographics
- Age range: 18-65 years (varies by condition)
- Depression/anxiety: peak 25-44
- Schizophrenia onset: 18-25
- Substance use: 18-35 peak

### Common Diagnosis Codes

#### Depressive Disorders
| Code | Description | Typical PHQ-9 |
|------|-------------|---------------|
| F32.0 | MDD, single episode, mild | 5-9 |
| F32.1 | MDD, single episode, moderate | 10-14 |
| F32.2 | MDD, single episode, severe | 15-19 |
| F32.3 | MDD, single episode, severe with psychotic features | 20-27 |
| F33.0 | MDD, recurrent, mild | 5-9 |
| F33.1 | MDD, recurrent, moderate | 10-14 |
| F33.2 | MDD, recurrent, severe | 15-19 |
| F34.1 | Persistent depressive disorder (dysthymia) | 5-10 |

#### Anxiety Disorders
| Code | Description | Typical GAD-7 |
|------|-------------|---------------|
| F41.1 | Generalized anxiety disorder | 10-21 |
| F41.0 | Panic disorder | Varies |
| F40.10 | Social anxiety disorder | Varies |
| F43.10 | Post-traumatic stress disorder | PCL-5 score |
| F42.2 | Obsessive-compulsive disorder | Y-BOCS score |

#### Bipolar Disorders
| Code | Description | Phase |
|------|-------------|-------|
| F31.0 | Bipolar I, current hypomanic | Elevated |
| F31.11 | Bipolar I, current manic, mild | Manic |
| F31.12 | Bipolar I, current manic, moderate | Manic |
| F31.31 | Bipolar I, current depressed, mild | Depressed |
| F31.32 | Bipolar I, current depressed, moderate | Depressed |
| F31.81 | Bipolar II disorder | Variable |

#### Substance Use Disorders
| Code | Description | Severity |
|------|-------------|----------|
| F10.10 | Alcohol use disorder, mild | 2-3 criteria |
| F10.20 | Alcohol use disorder, moderate | 4-5 criteria |
| F10.21 | Alcohol use disorder, moderate, in remission | In remission |
| F11.10 | Opioid use disorder, mild | 2-3 criteria |
| F11.20 | Opioid use disorder, moderate | 4-5 criteria |
| F11.21 | Opioid use disorder, moderate, in remission | On MAT |

### Psychiatric Medications

#### Antidepressants (SSRIs/SNRIs)
| Medication | Starting Dose | Target Dose | Use |
|------------|---------------|-------------|-----|
| Sertraline | 25-50 mg | 100-200 mg | Depression, anxiety, PTSD |
| Escitalopram | 5-10 mg | 10-20 mg | Depression, anxiety |
| Fluoxetine | 10-20 mg | 20-60 mg | Depression, OCD |
| Venlafaxine XR | 37.5-75 mg | 150-225 mg | Depression, anxiety |
| Duloxetine | 30 mg | 60-120 mg | Depression, anxiety, pain |
| Bupropion XL | 150 mg | 300-450 mg | Depression (no sexual SE) |

#### Mood Stabilizers
| Medication | Starting Dose | Target Dose | Use |
|------------|---------------|-------------|-----|
| Lithium | 300 mg BID | 900-1200 mg | Bipolar I |
| Lamotrigine | 25 mg | 200-400 mg | Bipolar depression |
| Valproate | 250 mg BID | 1000-2000 mg | Bipolar mania |

#### Antipsychotics
| Medication | Starting Dose | Target Dose | Use |
|------------|---------------|-------------|-----|
| Quetiapine | 25-50 mg | 150-800 mg | Bipolar, adjunct depression |
| Aripiprazole | 2-5 mg | 10-30 mg | Bipolar, adjunct depression |
| Risperidone | 0.5-1 mg | 2-6 mg | Schizophrenia |
| Olanzapine | 5 mg | 10-20 mg | Bipolar, schizophrenia |

#### Medications for SUD
| Medication | Dose | Use |
|------------|------|-----|
| Buprenorphine/naloxone | 8-24 mg | Opioid use disorder |
| Naltrexone | 50 mg daily or 380 mg monthly | Alcohol/opioid use |
| Acamprosate | 666 mg TID | Alcohol use disorder |
| Disulfiram | 250-500 mg | Alcohol deterrent |

### Screening Instruments

#### PHQ-9 (Depression)
| Score | Severity | Interpretation |
|-------|----------|----------------|
| 0-4 | None/minimal | No treatment indicated |
| 5-9 | Mild | Watchful waiting, consider therapy |
| 10-14 | Moderate | Treatment plan indicated |
| 15-19 | Moderately severe | Active treatment, medication |
| 20-27 | Severe | Immediate intervention, medication |

#### GAD-7 (Anxiety)
| Score | Severity | Interpretation |
|-------|----------|----------------|
| 0-4 | Minimal | No treatment indicated |
| 5-9 | Mild | Consider therapy |
| 10-14 | Moderate | Treatment indicated |
| 15-21 | Severe | Active treatment needed |

#### Columbia Suicide Severity Rating (C-SSRS)
- Ideation intensity: 1-5 scale
- Suicidal behavior: Yes/No with type
- Always document safety planning

### Vital Signs & Labs

#### Monitoring for Antipsychotics
- Weight (baseline, 4 weeks, 8 weeks, 12 weeks, then quarterly)
- Fasting glucose and lipid panel (baseline, 12 weeks, annually)
- A1C if glucose elevated

#### Monitoring for Lithium
- Lithium level (5-7 days after dose change, then every 3-6 months)
- Creatinine, TSH (baseline, then every 6 months)
- Target level: 0.6-1.0 mEq/L (acute: 0.8-1.2)

#### Monitoring for Valproate
- Valproic acid level (target: 50-100 mcg/mL)
- CBC, LFTs (baseline, then periodically)

## Variations

### Mild Depression, New Diagnosis
- PHQ-9: 8-10
- Diagnosis: F32.0
- Medications: Sertraline 50 mg started
- Treatment: Therapy referral + medication

### Moderate Depression with Anxiety Comorbidity
- PHQ-9: 14, GAD-7: 12
- Diagnoses: F33.1, F41.1
- Medications: Escitalopram 10 mg, PRN hydroxyzine
- Treatment: Weekly therapy, medication follow-up

### Bipolar I, Current Manic Episode
- Diagnosis: F31.12
- Medications: Lithium 900 mg, Quetiapine 400 mg
- Labs: Lithium level 0.9, TSH normal
- Recent hospitalization history

### Opioid Use Disorder in Treatment
- Diagnosis: F11.21
- Medications: Buprenorphine/naloxone 16 mg
- Treatment: MAT program, weekly counseling
- Urine drug screen: Positive buprenorphine only

### PTSD with Trauma History
- Diagnosis: F43.12
- PCL-5 Score: 48
- Medications: Sertraline 150 mg, Prazosin 3 mg HS
- Treatment: Trauma-focused therapy (CPT or EMDR)

## Examples

### Example 1: Major Depression
```json
{
  "patient": {
    "mrn": "MRN00000001",
    "name": { "given_name": "Jennifer", "family_name": "Martinez" },
    "birth_date": "1988-03-15",
    "gender": "F"
  },
  "diagnoses": [
    { "code": "F33.1", "description": "Major depressive disorder, recurrent, moderate" }
  ],
  "screening_scores": {
    "phq9": { "score": 14, "date": "2025-01-15" },
    "gad7": { "score": 8, "date": "2025-01-15" }
  },
  "medications": [
    { "name": "Sertraline", "dose": "100 mg", "frequency": "QD", "status": "active" }
  ],
  "encounters": [
    {
      "date": "2025-01-15",
      "type": "psychiatry follow-up",
      "note": "PHQ-9 improved from 18 to 14. Tolerating sertraline well. Continue current dose."
    }
  ]
}
```

### Example 2: Anxiety with Panic
```json
{
  "patient": {
    "mrn": "MRN00000002",
    "name": { "given_name": "David", "family_name": "Thompson" },
    "birth_date": "1995-08-22",
    "gender": "M"
  },
  "diagnoses": [
    { "code": "F41.1", "description": "Generalized anxiety disorder" },
    { "code": "F41.0", "description": "Panic disorder" }
  ],
  "screening_scores": {
    "gad7": { "score": 16, "date": "2025-01-10" },
    "panic_frequency": "2-3 episodes per week"
  },
  "medications": [
    { "name": "Escitalopram", "dose": "10 mg", "frequency": "QD", "status": "active" },
    { "name": "Hydroxyzine", "dose": "25 mg", "frequency": "PRN", "status": "active" }
  ]
}
```

### Example 3: Opioid Use Disorder on MAT
```json
{
  "patient": {
    "mrn": "MRN00000003",
    "name": { "given_name": "Michael", "family_name": "Roberts" },
    "birth_date": "1990-11-03",
    "gender": "M"
  },
  "diagnoses": [
    { "code": "F11.21", "description": "Opioid use disorder, moderate, in early remission" },
    { "code": "F32.1", "description": "Major depressive disorder, single episode, moderate" }
  ],
  "medications": [
    { "name": "Buprenorphine/naloxone", "dose": "16 mg", "frequency": "QD", "status": "active" },
    { "name": "Sertraline", "dose": "50 mg", "frequency": "QD", "status": "active" }
  ],
  "labs": [
    { "test": "Urine drug screen", "result": "Positive: Buprenorphine. Negative: Opioids, Cocaine, Amphetamines", "date": "2025-01-12" }
  ],
  "treatment_program": {
    "type": "MAT",
    "counseling_frequency": "weekly",
    "sobriety_date": "2024-06-15"
  }
}
```

## Trigger Phrases

- depression
- depressed patient
- anxiety
- mental health
- psychiatric
- behavioral health
- bipolar
- PTSD
- substance abuse
- addiction
- opioid use disorder
- alcohol use disorder
- PHQ-9
- GAD-7
- antidepressant
- mood disorder
- therapy patient

## Dependencies

- [../../references/code-systems.md](../../references/code-systems.md) - ICD-10 psychiatric codes
- [../../formats/fhir-r4.md](../../formats/fhir-r4.md) - FHIR Condition and MedicationRequest

## Validation Rules

| Rule | Requirement | Example |
|------|-------------|---------|
| PHQ-9 score | 0-27 | 15 (moderately severe) |
| GAD-7 score | 0-21 | 12 (moderate anxiety) |
| MDQ score | 0-13 for screening | 8 (positive screen) |
| AUDIT-C score | 0-12 | 5 (hazardous drinking) |
| Diagnosis code | Valid ICD-10 F-codes | F32.1 (MDD, moderate) |
| Medication class | Appropriate for diagnosis | SSRI for MDD |
| Suicide risk | low, moderate, high | "moderate" |
| Admission type | voluntary, involuntary | "voluntary" |

### Business Rules

- **Depression Severity**: PHQ-9 <5 (minimal), 5-9 (mild), 10-14 (moderate), 15-19 (mod severe), ≥20 (severe)
- **Anxiety Severity**: GAD-7 <5 (minimal), 5-9 (mild), 10-14 (moderate), ≥15 (severe)
- **Medication Trials**: Adequate trial = 4-6 weeks at therapeutic dose before switching
- **Treatment Resistance**: ≥2 failed adequate trials defines treatment-resistant depression
- **Metabolic Monitoring**: Antipsychotics require baseline/periodic metabolic panels
- **Safety Assessment**: Document suicide risk assessment at each visit
- **Level of Care**: Outpatient, IOP, PHP, inpatient based on acuity
- **Involuntary Admission**: Danger to self/others or gravely disabled

## Related Skills

### PatientSim
- [diabetes-management.md](diabetes-management.md) - For metabolic monitoring with antipsychotics

### Cross-Product: MemberSim
- [../membersim/behavioral-health.md](../membersim/behavioral-health.md) - Behavioral health claims
- [../membersim/professional-claims.md](../membersim/professional-claims.md) - Psychiatry/therapy E&M claims

> **Integration Pattern:** Use PatientSim for clinical encounters, assessments (PHQ-9, GAD-7), and medication management. Use MemberSim for behavioral health claims - parity requirements mean mental health benefits must equal medical benefits.

### Cross-Product: RxMemberSim
- [../rxmembersim/retail-pharmacy.md](../rxmembersim/retail-pharmacy.md) - Psychotropic medication fills
- [../rxmembersim/rx-prior-auth.md](../rxmembersim/rx-prior-auth.md) - PA for specialty psych meds

> **Integration Pattern:** Use PatientSim for medication orders. Use RxMemberSim for fills - antidepressants, antipsychotics, mood stabilizers. Adherence tracking is critical for psychiatric medications.

### Cross-Product: TrialSim
- [../trialsim/therapeutic-areas/cns.md](../trialsim/therapeutic-areas/cns.md) - CNS/neurology clinical trials, cognitive assessments

> **Integration Pattern:** This PatientSim skill covers psychiatric clinical care. For CNS drug trials involving psychiatric endpoints (e.g., depression scales in dementia trials), reference TrialSim CNS skill for trial-specific patterns.

### References
- [../../references/code-systems.md](../../references/code-systems.md) - ICD-10 psychiatric codes
- [../../references/mental-health-reference.md](../../references/mental-health-reference.md) - Behavioral health domain knowledge
- [../../formats/fhir-r4.md](../../formats/fhir-r4.md) - FHIR Condition and MedicationRequest
- [../../formats/hl7v2-adt.md](../../formats/hl7v2-adt.md) - Psychiatric admission messages
