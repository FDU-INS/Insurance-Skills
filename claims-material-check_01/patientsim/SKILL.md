---
name: healthsim-patientsim
description: "Generate realistic clinical patient data including demographics, encounters, diagnoses, medications, labs, and vitals. Use when user requests: (1) patient records or clinical data, (2) EMR test data, (3) specific clinical cohorts like diabetes or heart failure, (4) HL7v2 or FHIR patient resources."
---

# PatientSim - Clinical Patient Data Generation

## For Claude

Use this skill when the user requests clinical patient data, EMR/EHR test data, or medical records. This is the primary skill for generating realistic synthetic patients with complete clinical histories.

**When to apply this skill:**

- User mentions patients, clinical data, or medical records
- User requests EMR or EHR test data
- User specifies clinical cohorts (diabetes, heart failure, oncology, etc.)
- User asks for HL7v2 messages, FHIR resources, or C-CDA documents
- User needs encounters, diagnoses, medications, labs, or vitals

**Key capabilities:**

- Generate patients with realistic demographics and identifiers
- Create encounters across care settings (inpatient, outpatient, ED, observation)
- Apply clinical cohorts from specialized skills (diabetes, oncology, etc.)
- Produce appropriately coded data (ICD-10, CPT, HCPCS, LOINC, RxNorm, SNOMED)
- Transform output to FHIR R4 (Bundle, Patient, Condition, Encounter), HL7v2, C-CDA

For specific clinical cohorts, load the appropriate cohort skill from the table below.

## Overview

PatientSim generates realistic synthetic clinical data for EMR/EHR testing, including:
- Patient demographics
- Encounters (inpatient, outpatient, emergency, observation)
- Diagnoses (ICD-10-CM)
- Procedures (CPT, ICD-10-PCS)
- Medications (with RxNorm codes)
- Lab results (with LOINC codes)
- Vital signs

## Quick Start

### Simple Patient

**Request:** "Generate a patient"

```json
{
  "mrn": "MRN00000001",
  "name": { "given_name": "John", "family_name": "Smith" },
  "birth_date": "1975-03-15",
  "gender": "M",
  "address": {
    "street_address": "123 Main Street",
    "city": "Springfield",
    "state": "IL",
    "postal_code": "62701"
  }
}
```

### Clinical Cohort

**Request:** "Generate a diabetic patient with complications"

Claude loads [diabetes-management.md](diabetes-management.md) and produces a complete clinical picture.

## Cohort Skills

Load the appropriate cohort based on user request:

| Cohort | Trigger Phrases | File |
|----------|-----------------|------|
| **ADT Workflow** | admission, discharge, transfer, ADT, patient movement | [adt-workflow.md](adt-workflow.md) |
| **Behavioral Health** | depression, anxiety, bipolar, PTSD, mental health, psychiatric, substance use, PHQ-9, GAD-7 | [behavioral-health.md](behavioral-health.md) |
| **Diabetes Management** | diabetes, A1C, glucose, metformin, insulin | [diabetes-management.md](diabetes-management.md) |
| **Heart Failure** | CHF, HFrEF, HFpEF, BNP, ejection fraction, I50 | [heart-failure.md](heart-failure.md) |
| **Chronic Kidney Disease** | CKD, eGFR, dialysis, nephropathy | [chronic-kidney-disease.md](chronic-kidney-disease.md) |
| **Sepsis/Acute Care** | sepsis, infection, ICU, critical care | [sepsis-acute-care.md](sepsis-acute-care.md) |
| **Orders & Results** | lab order, radiology, ORM, ORU, results | [orders-results.md](orders-results.md) |
| **Maternal Health** | pregnancy, prenatal, obstetric, labor, delivery, postpartum, GDM, preeclampsia | [maternal-health.md](maternal-health.md) |
| **Pediatrics** | | |
| ↳ Childhood Asthma | asthma, pediatric, inhaler, albuterol, nebulizer, wheeze | [pediatrics/childhood-asthma.md](pediatrics/childhood-asthma.md) |
| ↳ Acute Otitis Media | ear infection, otitis media, AOM, ear pain, amoxicillin pediatric | [pediatrics/acute-otitis-media.md](pediatrics/acute-otitis-media.md) |
| **Oncology** | | |
| ↳ Breast Cancer | breast cancer, mastectomy, ER positive, HER2, tamoxifen | [oncology/breast-cancer.md](oncology/breast-cancer.md) |
| ↳ Lung Cancer | lung cancer, NSCLC, EGFR, ALK, immunotherapy | [oncology/lung-cancer.md](oncology/lung-cancer.md) |
| ↳ Colorectal Cancer | colon cancer, rectal cancer, FOLFOX, colonoscopy | [oncology/colorectal-cancer.md](oncology/colorectal-cancer.md) |

## Generation Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| age | int or range | 18-90 | Patient age or range |
| gender | M/F/O/U | weighted | M=49%, F=51% |
| conditions | list | none | Specific diagnoses to include |
| severity | string | moderate | mild, moderate, severe |
| encounters | int | 1 | Number of encounters to generate |
| timeline | string | 1 year | How far back to generate history |

## Output Entities

### Patient
Demographics extending the Person model with MRN.

### Encounter
Clinical visit with class (I/O/E/U/OBS), timing, location, providers.

### Diagnosis
ICD-10-CM code with type (admitting, working, final), dates.

### Medication
Drug with RxNorm code, dose, route, frequency, status.

### LabResult
Test with LOINC code, value, units, reference range, abnormal flag.

### VitalSign
Observation with temperature, HR, RR, BP, SpO2, height, weight.

See [data-models.md](../../references/data-models.md) for complete schemas.

## Clinical Coherence Rules

PatientSim ensures generated data is clinically realistic:

1. **Age-appropriate conditions**: No pediatric conditions in adults, geriatric conditions require appropriate age
2. **Gender-appropriate conditions**: Prostate conditions for males only, pregnancy for females only
3. **Medication indications**: Drugs match diagnoses (metformin requires diabetes)
4. **Lab coherence**: Values align with conditions (elevated A1C with diabetes, BMP reflects renal status)
5. **Temporal consistency**: Diagnoses before treatments, labs after orders
6. **Comorbidity patterns**: Realistic comorbid conditions cluster together (e.g., diabetes + hypertension + CKD)

See [validation-rules.md](../../references/validation-rules.md) for complete rules.

## Safety Guardrails

All PatientSim data is **100% synthetic** (fictional and simulated). Enforce these rules at all times:

1. **No real patient data.** Never copy real medical records, real MRNs, or real SSNs into output. All identifiers must be generated.
2. **No clinical advice.** Output is test data, not medical guidance. Never phrase output as a recommendation for actual patient care.
3. **No real provider NPIs in patient context.** Use synthetic NPIs (prefix with `9999`) unless explicitly pulling from NetworkSim reference data.
4. **Validate code systems.** Only emit ICD-10-CM codes from the current valid set (e.g., `E11.65` not `E11.999`). Same for CPT, LOINC, and RxNorm -- use real codes, not invented ones.
5. **PHI boundary.** If a user supplies real patient details, refuse and explain that PatientSim generates synthetic data only.

## Negative Examples (What NOT to Generate)

| Mistake | Why It Fails | Correct Approach |
|---------|-------------|------------------|
| Assigning pregnancy to a male patient | Gender-inappropriate | Check gender before obstetric conditions |
| Metformin without a diabetes diagnosis | Medication without indication | Always pair drugs with supporting Dx |
| A1C of 14.2% on a healthy patient | Lab contradicts condition list | Abnormal values require matching diagnosis |
| ICD-10 code `E11.999` | Invalid code -- does not exist | Use valid codes like `E11.65` (with complications) |
| Discharge date before admission date | Temporal inversion | Ensure chronological ordering of all events |
| Using a real SSN (e.g., `078-05-1120`) | PHI leak risk | Generate synthetic SSNs in `900-xx-xxxx` range |

## Edge Case Handling

| Scenario | Behavior |
|----------|----------|
| **Partial data request** ("just demographics") | Omit clinical entities (encounters, labs, meds); return only requested subset |
| **Age-cohort conflict** ("5-year-old with COPD") | Flag the clinical implausibility, suggest an age-appropriate alternative, and ask before proceeding |
| **Invalid ICD-10 code from user** (e.g., `E11.999`) | Reject the code, suggest the nearest valid code, explain why |
| **Missing required fields** (no age or gender given) | Apply defaults from Generation Parameters table; note assumptions in output |
| **Contradictory instructions** ("healthy patient with A1C of 12%") | Prioritize clinical coherence; ask user to clarify intent |
| **Unsupported output format** ("as X12 837") | Redirect to MemberSim which owns claims formats; explain the boundary |

## Output Formats

| Format | Request | Use Case |
|--------|---------|----------|
| JSON | default | API testing |
| FHIR R4 | "as FHIR", "FHIR bundle" | Interoperability |
| HL7v2 ADT | "as HL7", "ADT message" | Legacy EMR |
| CSV | "as CSV" | Analytics |

## Data Integration (PopulationSim)

Add `geography` (5-digit county FIPS or 11-digit tract FIPS) to ground generation in real CDC PLACES, SVI, and ADI data. See [data-integration.md](data-integration.md) for full patterns, data sources, and provenance tracking.

## Examples

### Example 1: Basic Patient with Encounter

**Request:** "Generate a 45-year-old male with an office visit for hypertension"

**Output:**
```json
{
  "patient": {
    "mrn": "MRN00000001",
    "name": { "given_name": "Michael", "family_name": "Johnson" },
    "birth_date": "1980-06-22",
    "gender": "M"
  },
  "encounter": {
    "encounter_id": "ENC0000000001",
    "patient_mrn": "MRN00000001",
    "class_code": "O",
    "status": "finished",
    "admission_time": "2025-01-15T09:30:00",
    "discharge_time": "2025-01-15T10:00:00",
    "chief_complaint": "Blood pressure follow-up"
  },
  "diagnoses": [
    {
      "code": "I10",
      "description": "Essential hypertension",
      "type": "final",
      "diagnosed_date": "2024-06-15"
    }
  ],
  "medications": [
    {
      "name": "Lisinopril",
      "code": "104376",
      "dose": "10 mg",
      "route": "PO",
      "frequency": "QD",
      "status": "active"
    }
  ],
  "vitals": {
    "observation_time": "2025-01-15T09:35:00",
    "systolic_bp": 138,
    "diastolic_bp": 88,
    "heart_rate": 72,
    "temperature": 98.4,
    "spo2": 98
  }
}
```

### Example 2: Acute Inpatient Encounter

**Request:** "Create an inpatient admission for pneumonia"

Generates a hospital encounter with:
- Encounter class `I` (inpatient), admission and discharge dates
- Diagnosis: J18.9 (Pneumonia, unspecified organism) plus respiratory symptoms
- Procedures: chest X-ray (CPT 71046), blood cultures, CBC
- Labs: WBC, procalcitonin, BMP, blood gas
- Medications: antibiotics (ceftriaxone + azithromycin)
- Imaging results documenting chest infiltrates

### Example 3: Complex Multi-Condition Patient

**Request:** "Generate a 68-year-old female with diabetes, hypertension, and CKD stage 3"

Claude combines patterns from multiple cohort skills to generate a coherent patient with:
- Multiple chronic diagnoses with appropriate onset dates
- Medications for each condition (metformin, lisinopril, etc.)
- Quarterly encounters over 2 years
- Labs showing disease progression (A1C, eGFR trends)
- Comorbidity interactions (CKD affecting medication choices)

## Related Skills

All cohort sub-skills are listed in the [Cohort Skills](#cohort-skills) table above. Additional references:

- [oncology-domain.md](../../references/oncology-domain.md) - Foundational oncology knowledge

### Cross-Product: MemberSim (Claims)

PatientSim clinical encounters generate corresponding claims in MemberSim:

| PatientSim Cohort | MemberSim Skill | Typical Timing |
|---------------------|-----------------|----------------|
| Office visits | [professional-claims.md](../membersim/professional-claims.md) | Same day |
| Inpatient stays | [facility-claims.md](../membersim/facility-claims.md) | +2-14 days |
| Surgeries | [prior-authorization.md](../membersim/prior-authorization.md), [facility-claims.md](../membersim/facility-claims.md) | PA before, claim after |
| Behavioral health | [behavioral-health.md](../membersim/behavioral-health.md) | Same day |

> **Integration Pattern:** Generate clinical encounter in PatientSim first, then use MemberSim to create corresponding claims with matching dates, diagnoses, and procedures.

### Cross-Product: RxMemberSim (Pharmacy)

PatientSim medication orders generate prescription fills in RxMemberSim:

| PatientSim Cohort | RxMemberSim Skill | Typical Timing |
|---------------------|-------------------|----------------|
| Chronic disease meds | [retail-pharmacy.md](../rxmembersim/retail-pharmacy.md) | Same day or +1-3 days |
| Discharge meds | [retail-pharmacy.md](../rxmembersim/retail-pharmacy.md) | +0-3 days post-discharge |
| Specialty drugs | [specialty-pharmacy.md](../rxmembersim/specialty-pharmacy.md) | +1-7 days |
| High-cost drugs | [rx-prior-auth.md](../rxmembersim/rx-prior-auth.md) | PA required first |

> **Integration Pattern:** Generate medication orders in PatientSim, then use RxMemberSim to model pharmacy fills with matching NDCs and appropriate fill timing.

### Cross-Product: PopulationSim (Demographics & SDOH)

When geography is specified, PatientSim grounds generation in real CDC PLACES, SVI, and ADI data via PopulationSim. See [data-integration.md](data-integration.md) for the full data-driven generation pattern, data files, and provenance tracking.

### Cross-Product: NetworkSim (Provider Networks)

NetworkSim provides realistic provider and facility entities for clinical encounters:

| PatientSim Need | NetworkSim Skill | Generated Entity |
|-----------------|------------------|------------------|
| Attending physician | [provider-for-encounter.md](../networksim/integration/provider-for-encounter.md) | Provider with NPI, credentials |
| Hospital/facility | [synthetic-facility.md](../networksim/synthetic/synthetic-facility.md) | Facility with CCN |
| Specialty referral | [synthetic-provider.md](../networksim/synthetic/synthetic-provider.md) | Specialist with taxonomy |

> **Integration Pattern:** Generate encounters in PatientSim first, then use NetworkSim to add realistic provider entities with proper NPIs, credentials, and hospital affiliations.

### Cross-Product: TrialSim (Clinical Trials)

For patients enrolled in clinical trials:

- [../trialsim/therapeutic-areas/oncology.md](../trialsim/therapeutic-areas/oncology.md) - Oncology trial endpoints
- [../trialsim/therapeutic-areas/cardiovascular.md](../trialsim/therapeutic-areas/cardiovascular.md) - CV outcomes trials
- [../trialsim/therapeutic-areas/cns.md](../trialsim/therapeutic-areas/cns.md) - CNS trial assessments

> **Integration Pattern:** Use PatientSim for clinical care journeys. When a patient enrolls in a trial, apply TrialSim skills for trial-specific data (RECIST, SDTM format, randomization).

### Output Formats
- [../../formats/fhir-r4.md](../../formats/fhir-r4.md) - FHIR transformation
- [../../formats/hl7v2-adt.md](../../formats/hl7v2-adt.md) - HL7v2 ADT messages
- [../../formats/hl7v2-orm.md](../../formats/hl7v2-orm.md) - HL7v2 Order messages
- [../../formats/hl7v2-oru.md](../../formats/hl7v2-oru.md) - HL7v2 Results messages

### Reference Data
- [../../references/oncology/](../../references/oncology/) - Oncology codes, medications, regimens

---

## Generative Framework Integration

PatientSim integrates with the [Generative Framework](../generation/SKILL.md) for specification-driven generation at scale.

- **Profile-Driven:** `"Use the Medicare diabetic profile to generate 100 patients"` — samples demographics, generates clinical attributes, links to NetworkSim providers.
- **Journey-Driven:** `"Add the diabetic first-year journey to each patient"` — generates encounters over time, labs, medication changes, and complication branching.
- **Cross-Domain Sync:** Patient → MemberSim Member (via SSN), Encounter → Claim, Prescription → RxMemberSim Fill, Trial Subject → TrialSim Subject. See [cross-domain-sync.md](../generation/executors/cross-domain-sync.md).
