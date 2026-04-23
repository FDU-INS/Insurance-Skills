# PatientSim

> Generate realistic clinical patient data including demographics, encounters, diagnoses, medications, labs, and vitals.

## What PatientSim Does

PatientSim is the **clinical data generation** engine of HealthSim. It creates synthetic patients with complete medical histories that are clinically coherent—medications match diagnoses, labs correlate with conditions, and temporal relationships make sense.

Whether you need a single patient record, a complex multi-condition case, or thousands of patients for load testing, PatientSim generates data that looks like it came from a real EMR.

## Quick Start

**Simple:**
```
Generate a patient
Generate a 45-year-old female with hypertension
```

**With clinical cohort:**
```
Generate a diabetic patient with A1C of 8.5
Generate a heart failure patient admitted for acute exacerbation
```

**With output format:**
```
Generate a diabetic patient as FHIR Bundle
Generate an inpatient admission as ADT A01 HL7v2
```

See [hello-healthsim examples](../../hello-healthsim/examples/patientsim-examples.md) for detailed examples with expected outputs.

## Key Capabilities

| Capability | Description | Skill Reference |
|------------|-------------|-----------------|
| **Demographics** | Patients with realistic names, addresses, MRNs | [SKILL.md](SKILL.md#patient) |
| **Encounters** | Inpatient, outpatient, ED, observation visits | [adt-workflow.md](adt-workflow.md) |
| **Chronic Disease** | Diabetes, heart failure, CKD with progression | Multiple cohort skills |
| **Oncology** | Breast, lung, colorectal cancer journeys | [oncology/](oncology/) |
| **Maternal Health** | Prenatal through postpartum | [maternal-health.md](maternal-health.md) |
| **Behavioral Health** | Depression, anxiety, bipolar, SUD | [behavioral-health.md](behavioral-health.md) |
| **Pediatrics** | Asthma, ear infections | [pediatrics/](pediatrics/) |
| **Acute Care** | Sepsis, ICU cohorts | [sepsis-acute-care.md](sepsis-acute-care.md) |
| **Labs & Vitals** | LOINC-coded results with reference ranges | [orders-results.md](orders-results.md) |

## Clinical Cohorts

| Cohort | Key Elements | Skill |
|----------|--------------|-------|
| Diabetes Management | Type 1/2, A1C, glucose, insulin, complications | [diabetes-management.md](diabetes-management.md) |
| Heart Failure | HFrEF/HFpEF, NYHA class, BNP, GDMT | [heart-failure.md](heart-failure.md) |
| Chronic Kidney Disease | Stages 1-5, eGFR, dialysis | [chronic-kidney-disease.md](chronic-kidney-disease.md) |
| Breast Cancer | Staging, ER/PR/HER2, surgery, chemo, hormonal | [oncology/breast-cancer.md](oncology/breast-cancer.md) |
| Lung Cancer | NSCLC/SCLC, EGFR/ALK, immunotherapy | [oncology/lung-cancer.md](oncology/lung-cancer.md) |
| Maternal Health | Prenatal, GDM, preeclampsia, delivery | [maternal-health.md](maternal-health.md) |
| Behavioral Health | Depression, anxiety, bipolar, PTSD, SUD | [behavioral-health.md](behavioral-health.md) |
| Pediatric Asthma | Severity classification, rescue/controller meds | [pediatrics/childhood-asthma.md](pediatrics/childhood-asthma.md) |

## Output Formats

| Format | Request | Use Case |
|--------|---------|----------|
| JSON | (default) | API testing, internal use |
| FHIR R4 | "as FHIR", "FHIR Bundle" | Interoperability testing |
| HL7v2 ADT | "as HL7", "as ADT" | Legacy EMR integration |
| HL7v2 ORM/ORU | "as ORM", "as ORU" | Orders and results |
| C-CDA | "as C-CDA", "as CCD" | Clinical document exchange |
| CSV | "as CSV" | Analytics, spreadsheets |

## Integration with Other Products

| Product | Integration | Example |
|---------|-------------|---------|
| **MemberSim** | Clinical encounters → Claims | Office visit → 837P professional claim |
| **RxMemberSim** | Medication orders → Pharmacy fills | Metformin order → NCPDP claim |
| **TrialSim** | Patient → Trial subject | Cancer patient → Oncology trial enrollment |
| **NetworkSim** | Encounter needs → Provider entity | Cardiology referral → Cardiologist NPI |
| **PopulationSim** | Geography → Demographics | County FIPS → Real prevalence rates |

## Data-Driven Generation (PopulationSim v2.0)

When you specify a geography, PatientSim uses **real population data** from CDC PLACES and SVI:

```
Generate a diabetic patient in Harris County, TX (FIPS 48201)
```

This grounds the patient in:
- Actual 12.1% diabetes prevalence (not generic 10%)
- Real comorbidity rates (obesity 33%, hypertension 32%)
- Demographic distributions matching the county
- SDOH factors from SVI vulnerability scores

See [data-integration.md](data-integration.md) for full integration details.

## Skills Reference

For complete generation parameters, examples, and validation rules, see:

- **[SKILL.md](SKILL.md)** - Full skill reference with all cohorts
- **[../../SKILL.md](../../SKILL.md)** - Master skill file (cross-product routing)

## Related Documentation

- [hello-healthsim PatientSim Examples](../../hello-healthsim/examples/patientsim-examples.md)
- [Cross-Product Integration Guide](../../docs/HEALTHSIM-ARCHITECTURE-GUIDE.md#93-cross-product-integration)
- [Output Formats](../../formats/)
- [Code Systems Reference](../../references/code-systems.md)

---

*PatientSim generates synthetic clinical data only. Never use for actual patient care.*
