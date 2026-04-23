# Tutorial 1: Your First Patient

**Time:** 10 minutes  
**Level:** Beginner  
**Products:** PatientSim

## What You'll Learn

- Generate a single patient with basic demographics
- Understand the quick-generate capability
- See patient output in different formats

## Step 1: Simple Generation

The simplest way to generate a patient is to just ask:

```
You: "Generate a patient"

Claude: "Here's a patient I've generated:

Patient ID: PAT-00001
Name: Maria Santos
DOB: 1978-03-15 (46 years old)
Gender: Female
MRN: MRN00000001

Would you like to add clinical details, save this patient, or generate more?"
```

## Step 2: Add Some Specifics

You can be more specific about what you want:

```
You: "Generate a 65-year-old male patient from Texas"

Claude: "Here's your patient:

Patient ID: PAT-00002
Name: James Mitchell
DOB: 1959-07-22 (65 years old)
Gender: Male
MRN: MRN00000002
Address: 4521 Oak Lane, Houston, TX 77002

Would you like to add conditions, medications, or other clinical details?"
```

## Step 3: Choose Your Format

You can request different output formats:

```
You: "Show me that patient in FHIR format"

Claude: "Here's the patient in FHIR R4:

{
  "resourceType": "Patient",
  "id": "PAT-00002",
  "identifier": [{
    "system": "urn:oid:2.16.840.1.113883.19.5",
    "value": "MRN00000002"
  }],
  "name": [{
    "family": "Mitchell",
    "given": ["James"]
  }],
  "gender": "male",
  "birthDate": "1959-07-22",
  "address": [{
    "city": "Houston",
    "state": "TX",
    "postalCode": "77002"
  }]
}
```

## Step 4: Save Your Patient

If you want to keep this patient for later use:

```
You: "Save this patient"

Claude: "Patient saved to scenario 'ad-hoc-patients'.

Summary:
- Patient PAT-00002 (James Mitchell) saved
- Available in main.patients table
- Can be retrieved with: SELECT * FROM main.patients WHERE patient_id = 'PAT-00002'

Would you like to generate more patients or add clinical data?"
```

## Try It Yourself

Practice generating patients with different characteristics:

1. "Generate a pediatric patient under 5 years old"
2. "Create an elderly female patient from Florida"
3. "Give me a patient with a Spanish name"

## What's Next?

In [Tutorial 2: Clinical Scenario](02-clinical-cohort.md), you'll learn to add conditions, medications, and lab values to make your patients clinically realistic.

---

**← Previous:** [Tutorials Home](README.md)  
**→ Next:** [Tutorial 2: Clinical Scenario](02-clinical-cohort.md)
