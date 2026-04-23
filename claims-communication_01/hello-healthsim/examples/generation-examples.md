# Generation Framework Examples

This document provides hands-on examples for using the HealthSim Generative Framework to create realistic healthcare data through conversation.

## Overview

The Generative Framework uses a two-phase approach:
1. **Specification Phase** - Build a profile or journey through conversation
2. **Execution Phase** - Generate data deterministically from the specification

## Quick Start Examples

### Example 1: Quick Generate - Single Patient

The fastest way to generate data. No specification needed.

```
User: "Generate a diabetic patient"

Claude: "Generated 1 patient:

Patient: Sarah Mitchell
- MRN: MRN00000001
- Age: 58, Female
- Conditions: Type 2 diabetes (E11.9), Hypertension (I10)
- A1c: 7.4%
- Medications: Metformin 1000mg BID, Lisinopril 10mg daily

Output format: FHIR R4
Save to DuckDB? (y/n)"
```

### Example 2: Quick Generate with Details

```
User: "Generate a Medicare patient with CHF who had a recent hospitalization"

Claude: "Generated 1 patient:

Patient: Robert Chen
- MRN: MRN00000002
- Age: 74, Male
- Medicare Advantage plan
- Conditions: 
  - Heart failure with reduced EF (I50.22)
  - Type 2 diabetes (E11.9)
  - CKD Stage 3 (N18.3)
- Recent hospitalization: 12/15/2024 - 12/19/2024
  - Admission: CHF exacerbation
  - DRG: 291 (Heart Failure with CC)
  - Discharge: Home with home health

Labs:
- BNP: 850 pg/mL
- Creatinine: 1.8 mg/dL
- EF: 35%

Medications:
- Carvedilol 12.5mg BID
- Lisinopril 20mg daily
- Furosemide 40mg daily
- Empagliflozin 10mg daily

Output includes: PatientSim (FHIR), MemberSim (claims)
Save to scenario?"
```

---

## Profile Builder Examples

### Example 3: Build a Simple Profile

```
User: "Build a profile for 50 Medicare diabetics"

Claude: "I'll help you build a profile for Medicare diabetics.

**Starting Profile:**
- Count: 50 patients
- Coverage: Medicare
- Primary condition: Type 2 diabetes (E11)

Let me ask a few questions to refine this:

1. **Age range**: Standard Medicare (65+) or include ESRD/disability?
2. **Geography**: National distribution or specific region?
3. **Diabetes severity**: Mix of controlled/uncontrolled, or specific distribution?

Or say 'use defaults' to proceed with standard Medicare diabetic profile."
```

```
User: "Use defaults but focus on Texas"

Claude: "Updated profile:

**Medicare Diabetic Texas Profile**
```json
{
  "profile": {
    "id": "medicare-diabetic-texas-001",
    "generation": {
      "count": 50,
      "products": ["patientsim", "membersim"]
    },
    "demographics": {
      "age": {"type": "normal", "mean": 72, "std_dev": 8, "min": 65},
      "gender": {"M": 0.48, "F": 0.52},
      "geography": {"state": "TX", "distribution": "population_weighted"}
    },
    "clinical": {
      "primary_condition": {"code": "E11", "prevalence": 1.0},
      "comorbidities": [
        {"code": "I10", "prevalence": 0.78},
        {"code": "E78.5", "prevalence": 0.72}
      ]
    },
    "coverage": {
      "type": "Medicare",
      "plan_mix": {"MA": 0.55, "Original": 0.45}
    }
  }
}
```

Ready to execute this profile? Or would you like to customize further?"
```

```
User: "Execute it"

Claude: "Executing profile 'medicare-diabetic-texas-001'...

Progress:
- Generating 50 patients... ████████████ 100%
- Creating conditions... ████████████ 100%  
- Generating encounters... ████████████ 100%
- Creating claims... ████████████ 100%

✓ Generated successfully!

Summary:
- 50 patients (24M/26F)
- Age range: 65-89, mean 71.4
- 205 encounters, 410 claims
- Texas counties: Harris (18), Dallas (12), Bexar (8), Travis (6), other (6)

Validation:
✓ Age distribution within tolerance
✓ Gender ratio within tolerance
✓ All patients have diabetes diagnosis
✓ Comorbidity rates within tolerance

Saved as scenario: 'medicare-diabetic-texas-001'
View in DuckDB: SELECT * FROM main.patients WHERE scenario_id = 'medicare-diabetic-texas-001'"
```

### Example 4: Profile with Journey Attached

```
User: "Create 100 newly diagnosed diabetics with their first year journey"

Claude: "I'll create a profile with the diabetic first year journey attached.

**Profile + Journey Specification:**
```json
{
  "profile": {
    "id": "new-diabetic-first-year-001",
    "generation": {
      "count": 100,
      "products": ["patientsim", "membersim", "rxmembersim"]
    },
    "demographics": {
      "age": {"type": "normal", "mean": 55, "std_dev": 12, "min": 30, "max": 75}
    },
    "clinical": {
      "primary_condition": {
        "code": "E11.9",
        "status": "new_diagnosis",
        "diagnosis_date": "2025-01-01"
      }
    }
  },
  "journey": {
    "template": "diabetic_first_year",
    "start_trigger": "diagnosis_date"
  }
}
```

This will generate:
- 100 patients with new T2DM diagnosis
- 12 months of care events per patient
- ~1,200 encounters, ~2,400 claims, ~1,200 Rx fills

Execute now?"
```

---

## Journey Examples

### Example 5: Surgical Episode Journey

```
User: "Create a knee replacement surgical journey for 25 patients"

Claude: "Building surgical episode journey for total knee arthroplasty.

**Journey Configuration:**
- Procedure: Total Knee Arthroplasty (CPT 27447)
- Duration: 3 months (pre-op through recovery)
- Patients: 25

**Timeline Preview:**
| Phase | Timing | Events |
|-------|--------|--------|
| Pre-op | Week -4 to -1 | Consult, clearance, labs, imaging |
| Surgery | Day 0 | Admission, procedure, 2-3 day stay |
| Acute Recovery | Week 1-2 | Discharge, home health or SNF |
| Rehab | Week 3-10 | Outpatient PT 3x/week |
| Final | Week 12 | Final follow-up |

**Branching Outcomes:**
- 70% discharge to home
- 25% discharge to SNF
- 5% complications (2% infection, 1% DVT, 2% other)

Execute this journey?"
```

```
User: "Yes, execute"

Claude: "Executing surgical episode journey...

Generating 25 patient journeys:
- Pre-operative phase... ████████████ 100%
- Surgical phase... ████████████ 100%
- Recovery phase... ████████████ 100%
- Rehabilitation phase... ████████████ 100%

**Results:**

Discharge Disposition:
- Home: 18 patients (72%)
- SNF: 6 patients (24%)  
- Home with HH: 1 patient (4%)

Complications:
- Surgical site infection: 1 patient
- DVT: 0 patients
- 30-day readmission: 1 patient

Events Generated:
- Encounters: 625 (25 avg per patient)
- Professional claims: 625
- Facility claims: 25
- PT sessions: 450

Timeline span: 2025-01-01 to 2025-04-01

Saved as scenario: 'tka-surgical-episode-001'"
```

### Example 6: New Member Onboarding Journey

```
User: "Generate 200 new Medicare Advantage members with onboarding journey"

Claude: "Creating MA new member onboarding cohort.

**Profile + Journey:**
```json
{
  "profile": {
    "id": "ma-new-members-jan2025",
    "count": 200,
    "demographics": {
      "age": {"mean": 72, "std_dev": 7, "min": 65}
    },
    "coverage": {
      "type": "Medicare Advantage",
      "effective_date": "2025-01-01",
      "enrollment_reason": {
        "AEP": 0.85,
        "SEP": 0.10,
        "aging_in": 0.05
      }
    }
  },
  "journey": {
    "template": "new_member_onboarding",
    "duration": "90 days"
  }
}
```

**Expected Outcomes (based on typical rates):**
- Welcome calls completed: ~90 (45%)
- Portal activations: ~110 (55%)
- HRA completions: ~70 (35%)
- First PCP visits: ~60 (30%)
- Care gap closures: ~40 (20%)

Execute?"
```

---

## Cross-Product Examples

### Example 7: Full Ecosystem Generation

```
User: "Generate a complete healthcare ecosystem for a small town"

Claude: "Creating a small-town healthcare ecosystem using multiple products.

**Ecosystem Specification:**

**1. Population (PopulationSim reference)**
- Town: Smallville, TX (fictional)
- Population: 15,000
- Demographics from similar real Texas towns

**2. Network (NetworkSim)**
- Hospital: 1 (50 beds)
- PCPs: 12
- Specialists: 8
- Pharmacies: 4
- Urgent Care: 2

**3. Patients (PatientSim + MemberSim + RxMemberSim)**

| Segment | Count | Coverage | Profile |
|---------|-------|----------|---------|
| Medicare | 2,500 | MA/Original | Older, chronic |
| Commercial | 5,000 | Employer | Working age |
| Medicaid | 1,500 | Managed | Lower income |
| Uninsured | 1,000 | None | Gap population |

**4. Utilization Patterns**
- Annual visits per capita: 4.2
- ER visits per 1000: 380
- Admissions per 1000: 95

This is a complex generation. Shall I:
A) Generate full ecosystem (may take several minutes)
B) Generate a representative sample (500 patients)
C) Generate one segment at a time"
```

---

## Template Usage Examples

### Example 8: Using a Pre-built Template

```
User: "Use the Medicare diabetic template"

Claude: "Loading template: medicare-diabetic

**Template Defaults:**
- Count: 100 patients
- Age: 65-95 (mean 72)
- Coverage: Medicare (55% MA, 45% Original)
- Diabetes: 100% with standard severity distribution
- Comorbidities: HTN 78%, Hyperlipidemia 72%, CKD 28%

**Customization Options:**
1. Change count
2. Change geography
3. Adjust severity distribution
4. Add journey
5. Use as-is

What would you like to do?"
```

```
User: "Use as-is but only 25 patients"

Claude: "Adjusted template:
- Count: 25 (changed from 100)
- All other settings: default

Executing... ✓

Generated 25 Medicare diabetic patients.
Saved as: 'medicare-diabetic-20250103-001'"
```

---

## Output Format Examples

### Example 9: Specify Output Formats

```
User: "Generate 10 patients in FHIR R4 and X12 837 formats"

Claude: "Generated 10 patients with dual format output:

**FHIR R4 Bundle:**
- 10 Patient resources
- 45 Condition resources
- 82 Encounter resources
- 120 Observation resources

**X12 837P Claims:**
- 82 professional claims
- Payer: Generic Commercial
- Submission date: 2025-01-03

Files saved:
- /outputs/patients-fhir-bundle.json
- /outputs/claims-837p.x12

View FHIR: `SELECT * FROM main.fhir_patients`
View Claims: `SELECT * FROM main.claims_837`"
```

---

## Tips and Best Practices

### When to Use Each Approach

| Need | Approach |
|------|----------|
| Quick demo data | Quick Generate |
| Specific population study | Profile Builder |
| Longitudinal analysis | Profile + Journey |
| Claims testing | MemberSim focus |
| Clinical scenarios | PatientSim focus |
| Pharmacy testing | RxMemberSim focus |

### Conversation Shortcuts

- "Use defaults" - Accept standard settings
- "Same as last time" - Reuse previous profile
- "Add journey" - Attach journey to profile
- "Execute" - Run the current specification
- "Save as template" - Save for reuse
- "Show me the JSON" - View specification

---

## Next Steps

- [Profile Builder Skill](../../skills/generation/builders/profile-builder.md)
- [Journey Builder Skill](../../skills/generation/builders/journey-builder.md)
- [Template Library](../../skills/generation/templates/)
- [Distribution Types](../../skills/generation/distributions/distribution-types.md)

---

*Part of Hello-HealthSim - Your guide to getting started with HealthSim*
