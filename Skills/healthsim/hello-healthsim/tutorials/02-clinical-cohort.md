# Tutorial 2: Clinical Cohort

**Time:** 15 minutes  
**Level:** Beginner  
**Products:** PatientSim

## What You'll Learn

- Add conditions (diagnoses) to a patient
- Add medications with realistic prescriptions
- Generate lab results with clinical values
- Create a complete clinical picture

## Step 1: Patient with a Condition

Start by generating a patient with a specific condition:

```
You: "Generate a diabetic patient"

Claude: "Here's a Type 2 diabetic patient:

Patient: Robert Chen, 58M
MRN: MRN00000003
DOB: 1966-11-08

Conditions:
• E11.9 - Type 2 diabetes mellitus without complications
  Onset: 2019-03-15
  Status: Active

Would you like to add medications, labs, or comorbidities?"
```

## Step 2: Add Realistic Comorbidities

Diabetic patients often have related conditions:

```
You: "Add typical diabetic comorbidities"

Claude: "Added comorbidities based on clinical patterns:

Conditions:
• E11.9 - Type 2 diabetes mellitus (primary)
• I10 - Essential hypertension
• E78.5 - Hyperlipidemia, unspecified
• E66.9 - Obesity, unspecified

All conditions set with clinically appropriate onset dates relative to diabetes diagnosis."
```

## Step 3: Add Medications

```
You: "Add medications for these conditions"

Claude: "Added appropriate medications:

Medications:
┌─────────────────────┬──────────┬───────────┬─────────────┐
│ Medication          │ Dose     │ Frequency │ Start Date  │
├─────────────────────┼──────────┼───────────┼─────────────┤
│ Metformin           │ 1000mg   │ BID       │ 2019-04-01  │
│ Lisinopril          │ 20mg     │ Daily     │ 2019-06-15  │
│ Atorvastatin        │ 40mg     │ Daily     │ 2020-01-10  │
│ Aspirin             │ 81mg     │ Daily     │ 2019-06-15  │
└─────────────────────┴──────────┴───────────┴─────────────┘

All prescriptions include realistic days supply and refill patterns."
```

## Step 4: Generate Lab Results

```
You: "Add recent lab results"

Claude: "Generated lab results consistent with controlled diabetes:

Recent Labs (as of 2024-12-15):

HbA1c Panel:
• HbA1c: 7.2% (target <7.0)

Basic Metabolic Panel:
• Glucose (fasting): 128 mg/dL (H)
• BUN: 18 mg/dL
• Creatinine: 1.1 mg/dL
• eGFR: 72 mL/min/1.73m²

Lipid Panel:
• Total Cholesterol: 185 mg/dL
• LDL: 95 mg/dL
• HDL: 48 mg/dL
• Triglycerides: 165 mg/dL

All values generated with clinically realistic ranges based on patient's conditions."
```

## Step 5: Complete Clinical Picture

```
You: "Show me the complete patient summary"

Claude: "Complete Clinical Summary for Robert Chen (MRN00000003):

DEMOGRAPHICS
• 58-year-old Male
• DOB: 1966-11-08

ACTIVE CONDITIONS
1. E11.9 - Type 2 diabetes mellitus (since 2019)
2. I10 - Essential hypertension (since 2019)
3. E78.5 - Hyperlipidemia (since 2020)
4. E66.9 - Obesity (since 2018)

CURRENT MEDICATIONS
1. Metformin 1000mg BID
2. Lisinopril 20mg daily
3. Atorvastatin 40mg daily
4. Aspirin 81mg daily

RECENT LABS (2024-12-15)
• HbA1c: 7.2%
• eGFR: 72

CLINICAL ASSESSMENT
Moderately controlled Type 2 DM with common comorbidities.
On appropriate guideline-directed therapy."
```

## Try It Yourself

Practice creating clinical cohorts:

1. "Generate a patient with COPD and add inhalers"
2. "Create a heart failure patient with recent echo results"
3. "Generate a hypertensive patient not at goal"

## Key Concepts

| Concept | Description |
|---------|-------------|
| **Conditions** | Diagnoses with ICD-10 codes, onset dates, status |
| **Medications** | Prescriptions with dose, frequency, days supply |
| **Observations** | Lab results with values, units, reference ranges |
| **Clinical Realism** | Values correlated with conditions and each other |

## What's Next?

In [Tutorial 3: Claims Journey](03-claims-journey.md), you'll learn to generate claims that correspond to your patient's clinical encounters.

---

**← Previous:** [Tutorial 1: First Patient](01-first-patient.md)  
**→ Next:** [Tutorial 3: Claims Journey](03-claims-journey.md)
