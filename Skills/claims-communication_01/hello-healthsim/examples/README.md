# HealthSim Examples

Detailed examples demonstrating HealthSim capabilities across all products and clinical domains.

---

## Learning Path: Simple to Complex

### Level 1: Getting Started (5 minutes)

Start here to verify your setup and learn the basics.

| Example | Prompt | What You Learn |
|---------|--------|----------------|
| Simple Patient | "Generate a patient" | Basic PatientSim output |
| Office Visit Claim | "Generate a professional claim for an office visit" | Basic MemberSim output |
| Prescription Fill | "Generate a pharmacy claim for lisinopril" | Basic RxMemberSim output |
| Phase 3 Trial | "Generate a Phase 3 oncology trial with 20 subjects" | Basic TrialSim output |
| Provider Generation | "Generate a cardiologist in Houston" | Basic NetworkSim output |

See: [PatientSim Example 1](patientsim-examples.md#example-1-simple-patient), [MemberSim Example 1](membersim-examples.md#example-1-simple-office-visit-claim), [RxMemberSim Example 1](rxmembersim-examples.md#example-1-simple-generic-prescription), [TrialSim Quick Start](trialsim-examples.md#quick-start-examples)

---

### Level 2: Clinical Domains (10-15 minutes)

Learn to generate data for specific clinical conditions.

| Domain | Example Prompt | Guide |
|--------|----------------|-------|
| **Diabetes** | "Generate a 62-year-old with Type 2 diabetes and A1C of 8.5" | [PatientSim Example 2](patientsim-examples.md#example-2-diabetic-patient) |
| **Heart Failure** | "Generate a patient with HFrEF and NYHA Class III" | [PatientSim Example 3](patientsim-examples.md#example-3-heart-failure-patient) |
| **CKD** | "Generate a patient with Stage 4 CKD" | [PatientSim Example 4](patientsim-examples.md#example-4-patient-with-encounter) |
| **Oncology** | "Generate a Stage IIA breast cancer patient" | [Oncology Examples](oncology-examples.md) |
| **Behavioral Health** | "Generate a psychotherapy claim for depression" | [MemberSim](membersim-examples.md) |

---

### Level 2.5: Clinical Trials (15 minutes)

Generate clinical trial data with CDISC compliance.

| Scenario | Example Prompt | Guide |
|----------|----------------|-------|
| **Phase 3 Trial** | "Generate Phase 3 oncology trial with 100 subjects" | [TrialSim Quick Start](trialsim-examples.md#quick-start-examples) |
| **Dose Escalation** | "Generate Phase 1 3+3 dose escalation study" | [Phase 1 Examples](trialsim-examples.md#phase-i-dose-escalation-examples) |
| **Adverse Events** | "Generate AEs with MedDRA coding for 50 subjects" | [TrialSim AE Example](trialsim-examples.md#example-2-generate-adverse-events) |
| **SDTM Output** | "Generate DM and AE domains as SDTM" | [SDTM Domain Examples](trialsim-examples.md#sdtm-domain-examples) |
| **Trial Analytics** | "Generate trial data as star schema for DuckDB" | [Dimensional Analytics](trialsim-examples.md#dimensional-analytics-examples) |

---

### Level 2.6: Population Intelligence (15 minutes)

Analyze population demographics, SDOH, and define cohorts for generation.

| Scenario | Example Prompt | Guide |
|----------|----------------|-------|
| **County Profile** | "Generate a population profile for Maricopa County, AZ" | [PopulationSim Example 1](populationsim-examples.md#example-1-county-population-profile) |
| **SDOH Analysis** | "Analyze social vulnerability for rural Georgia counties" | [PopulationSim Example 2](populationsim-examples.md#example-2-sdoh-vulnerability-analysis) |
| **Cohort Definition** | "Define a cohort for a diabetes prevention study in underserved areas" | [PopulationSim Example 3](populationsim-examples.md#example-3-cohort-specification) |
| **Trial Feasibility** | "Assess enrollment feasibility for a NASH trial in Texas" | [PopulationSim Example 4](populationsim-examples.md#example-4-trial-feasibility-analysis) |

---

### Level 2.7: Provider Network Data (10-15 minutes)

Generate providers, facilities, pharmacies, and network configurations.

| Scenario | Example Prompt | Guide |
|----------|----------------|-------|
| **Provider** | "Generate a cardiologist in Houston with full credentials" | [NetworkSim - Find Providers](networksim-examples.md#find-providers-by-specialty-and-location) |
| **Hospital** | "Generate a 200-bed community hospital in Dallas" | [NetworkSim - Generate Hospital](networksim-examples.md#generate-a-hospital) |
| **Specialty Pharmacy** | "Generate a specialty pharmacy for oncology" | [NetworkSim - Generate Pharmacy](networksim-examples.md#generate-a-pharmacy) |
| **Network Config** | "Generate a tiered PPO network with 3 tiers" | [NetworkSim - Network Types](networksim-examples.md#explain-network-types) |

---

### Level 3: Claims & Adjudication (15 minutes)

Understand healthcare payment workflows.

| Scenario | Example Prompt | Guide |
|----------|----------------|-------|
| **Paid Claim** | "Generate a paid claim with copay applied" | [MemberSim Example 1](membersim-examples.md#example-1-simple-office-visit-claim) |
| **Denied Claim** | "Generate a denied MRI claim requiring prior auth" | [MemberSim Example 2](membersim-examples.md#example-2-denied-claim) |
| **Facility Claim** | "Generate a hospital admission claim with DRG" | [MemberSim Example 4](membersim-examples.md#example-4-facilityinpatient-claim) |
| **Deductible Applied** | "Generate a claim where deductible applies" | [MemberSim Example 3](membersim-examples.md#example-3-claim-with-deductible) |

---

### Level 4: Pharmacy & DUR (15 minutes)

Test pharmacy benefit workflows and drug utilization review.

| Scenario | Example Prompt | Guide |
|----------|----------------|-------|
| **Drug Interaction** | "Generate a pharmacy claim with drug-drug interaction" | [RxMemberSim Example 2](rxmembersim-examples.md#example-2-drug-interaction-alert) |
| **Prior Auth Required** | "Generate a pharmacy claim rejected for prior authorization" | [RxMemberSim Example 3](rxmembersim-examples.md#example-3-prior-authorization-required) |
| **Specialty Drug** | "Generate a specialty pharmacy claim with copay card" | [RxMemberSim Example 4](rxmembersim-examples.md#example-4-specialty-drug-with-copay-assistance) |
| **Early Refill** | "Generate a pharmacy claim rejected for early refill" | [RxMemberSim Example 5](rxmembersim-examples.md#example-5-early-refill-scenario) |

---

### Level 5: Token-Efficient Batch Operations (10 minutes)

Generate and persist large batches without filling context.

| Scenario | Example Prompt | Guide |
|----------|----------------|-------|
| **Batch Generation** | "Generate 100 Medicare members over 65 in California" | [Auto-Persist Example 1](auto-persist-examples.md#example-1-generate-large-member-cohort) |
| **Query Saved Data** | "From my medicare scenario, show female members with diabetes" | [Auto-Persist Example 2](auto-persist-examples.md#example-2-query-saved-data) |
| **Resume with Summary** | "Load my diabetes cohort from yesterday" | [Auto-Persist Example 3](auto-persist-examples.md#example-3-resume-work-with-summary) |
| **Get Samples** | "Show me a few example patients from that cohort" | [Auto-Persist Example 4](auto-persist-examples.md#example-4-get-sample-entities) |
| **Batch Trial Data** | "Generate a trial with 200 subjects" | [Auto-Persist Example 5](auto-persist-examples.md#example-5-generate-clinical-trial-scenario) |

---

### Level 6: Output Formats (15 minutes)

Transform data to healthcare standards.

| Format | Example Prompt | Guide |
|--------|----------------|-------|
| **FHIR R4** | "Generate a diabetic patient as FHIR Bundle" | [Format Examples - FHIR](format-examples.md#fhir-r4-examples) |
| **C-CDA** | "Generate a discharge summary as C-CDA" | [Format Examples - C-CDA](format-examples.md#c-cda-examples) |
| **HL7v2 ADT** | "Generate an admission as ADT A01 message" | [Format Examples - HL7v2](format-examples.md#hl7v2-examples) |
| **X12 837** | "Generate a professional claim as X12 837P" | [Format Examples - X12](format-examples.md#x12-examples) |
| **CSV** | "Generate 10 patients as CSV" | [Format Examples - CSV](format-examples.md#csv-export-example) |

---

### Level 7: Cross-Domain Scenarios (20 minutes)

Create realistic end-to-end test data spanning multiple products.

| Scenario | What You Get | Guide |
|----------|--------------|-------|
| **Patient + Claims + Rx** | Diabetic patient with office visit and pharmacy claims | [Cross-Domain Example 1](cross-domain-examples.md#example-1-patient-with-medical-and-pharmacy-claims) |
| **Hospitalization Episode** | Inpatient admission, follow-up, discharge meds | [Cross-Domain Example 2](cross-domain-examples.md#example-2-hospitalization-with-follow-up) |
| **Prior Auth Flow** | Rejection → PA submission → Approval → Fill | [Cross-Domain Example 3](cross-domain-examples.md#example-3-prior-auth-flow) |
| **Value-Based Care** | Patient with quality measures and care gaps | [Cross-Domain Example 4](cross-domain-examples.md#example-4-value-based-care-report) |
| **Trial + EMR Linkage** | Trial subject linked to PatientSim medical history | [Cross-Domain Example 6](cross-domain-examples.md#example-6-clinical-trial-subject-with-emr-linkage) |
| **Trial + Provider Network** | Trial site linked to NetworkSim facilities | [Cross-Domain Example 7](cross-domain-examples.md#example-7-trial-subject-with-site-provider-linkage) |
| **Trial Analytics** | Cross-product dimensional analytics | [Cross-Domain Example 8](cross-domain-examples.md#example-8-cross-product-dimensional-analytics) |

---

### Level 8: Generative Framework (20-30 minutes) ⭐ NEW

Build structured specifications through conversation, then generate at scale.

| Scenario | Example Prompt | Guide |
|----------|----------------|-------|
| **Quick Generate** | "Generate a diabetic patient" | [Generation Example 1](generation-examples.md#example-1-quick-generate---single-patient) |
| **Profile Builder** | "Build a profile for 50 Medicare diabetics" | [Generation Example 3](generation-examples.md#example-3-build-a-simple-profile) |
| **Profile + Journey** | "Create 100 newly diagnosed diabetics with first year journey" | [Generation Example 4](generation-examples.md#example-4-profile-with-journey-attached) |
| **Surgical Episode** | "Create a knee replacement journey for 25 patients" | [Generation Example 5](generation-examples.md#example-5-surgical-episode-journey) |
| **Member Onboarding** | "Generate 200 new MA members with onboarding journey" | [Generation Example 6](generation-examples.md#example-6-new-member-onboarding-journey) |
| **Use Template** | "Use the Medicare diabetic template" | [Generation Example 8](generation-examples.md#example-8-using-a-pre-built-template) |

**Key Concepts:**
- **Profiles** define *who* (demographics, conditions, coverage)
- **Journeys** define *what happens* (events over time)
- **Templates** provide ready-to-use starting points
- **Two phases**: Specification (conversational) → Execution (deterministic)

See: [Profile Builder](../../skills/generation/builders/profile-builder.md), [Journey Builder](../../skills/generation/builders/journey-builder.md), [Templates](../../skills/generation/templates/)

---

## Example Files by Product

| Guide | Description | Examples |
|-------|-------------|----------|
| [PatientSim Examples](patientsim-examples.md) | Clinical data generation | Patients, diagnoses, medications, labs |
| [MemberSim Examples](membersim-examples.md) | Claims and payer data | Professional, facility, adjudication |
| [RxMemberSim Examples](rxmembersim-examples.md) | Pharmacy data | Prescriptions, DUR alerts, copay cards |
| [TrialSim Examples](trialsim-examples.md) | Clinical trial data | SDTM domains, AEs, efficacy, sites |
| [PopulationSim Examples](populationsim-examples.md) | Population intelligence | Profiles, SDOH, cohorts, feasibility |
| [NetworkSim Examples](networksim-examples.md) | Provider network data | Providers, facilities, pharmacies, networks |
| [Oncology Examples](oncology-examples.md) | Cancer-specific scenarios | Staging, treatment, biomarkers |
| [Cross-Domain Examples](cross-domain-examples.md) | Multi-product scenarios | End-to-end test data |
| [Format Examples](format-examples.md) | Output transformations | FHIR, HL7v2, X12, C-CDA, SDTM, CSV |
| [Auto-Persist Examples](auto-persist-examples.md) | Token-efficient batch ops | Large cohorts, queries, summaries |
| [Generation Examples](generation-examples.md) | **⭐ Generative Framework** | Profiles, journeys, templates, at-scale generation |

---

## Quick Reference: Example Prompts by Domain

### Chronic Disease

```text
Generate a 65-year-old with Type 2 diabetes, hypertension, and hyperlipidemia
Generate a patient with heart failure and reduced ejection fraction
Generate a patient with Stage 3b CKD and diabetes
```

### Oncology

```text
Generate a Stage IIB ER-positive breast cancer patient with treatment plan
Generate a non-small cell lung cancer patient with EGFR mutation
Generate a colorectal cancer patient with liver metastases
```

### Acute Care & Emergency

```text
Generate a sepsis patient with ICU admission
Generate an ED chest pain patient with HEART score workup
Generate a hip replacement patient with pre-op and post-op care
```

### Clinical Trials

```text
Generate a Phase 3 oncology trial with 200 subjects randomized 2:1
Generate adverse events with MedDRA coding for 100 subjects
Generate DM and AE domains as SDTM for a Phase 2 trial
Generate a Phase 1 dose escalation study with 3+3 design
Generate tumor response data with RECIST 1.1 assessments
Generate trial data as star schema for DuckDB analytics
```

### Maternal & Pediatric

```text
Generate a 28-week pregnant patient with gestational diabetes
Generate a postpartum patient with preeclampsia
Generate pediatric vaccination records for a 2-year-old
```

### Behavioral Health

```text
Generate a psychotherapy claim for major depressive disorder
Generate a substance abuse IOP claim
Generate a telehealth psychiatry visit claim
```

### Claims & Payment

```text
Generate a paid claim with deductible and coinsurance applied
Generate a denied claim for prior authorization required
Generate a claim with out-of-network penalties
```

### Pharmacy

```text
Generate a pharmacy claim with drug-drug interaction alert
Generate a specialty drug claim requiring prior authorization
Generate a copay card transaction for a brand medication
```

### Provider Network

```text
Generate a cardiologist in Houston, Texas with full credentials
Generate a 200-bed community hospital in suburban Dallas
Generate a specialty pharmacy for oncology medications
Generate a tiered PPO network with quality-based tiers
Explain the difference between HMO and PPO networks
```

### Batch Operations & Auto-Persist

```text
Generate 100 Medicare members over 65 in California
Generate 200 diabetic patients and save them
Query my medicare scenario for members in San Diego
Show me a summary of my diabetes cohort
Get 3 sample patients from my trial scenario
Rename my scenario to training-cohort-q4
List my scenarios tagged with training
```

### Generation Framework (Profiles & Journeys) ⭐ NEW

```text
Generate a diabetic patient
Generate a Medicare patient with CHF who had a recent hospitalization
Build a profile for 50 Medicare diabetics in Texas
Create 100 newly diagnosed diabetics with first year journey
Use the Medicare diabetic template with 25 patients
Create a knee replacement surgical journey for 25 patients
Generate 200 new MA members with onboarding journey
Use the commercial healthy template for a tech company
Show me the profile JSON
Execute this profile
```

---

## How to Use These Examples

Each example in the guides includes:

1. **The Prompt** - Exact text to send to Claude
2. **Expected Output** - Sample JSON/format response
3. **Key Points** - What to notice in the output
4. **Variations** - How to modify the request for different scenarios

## Tips for Success

1. **Start simple** - Begin with Level 1 examples to verify your setup
2. **Be specific** - "62-year-old diabetic with A1C 9.5" beats "sick patient"
3. **Request format early** - "Generate as FHIR..." not "convert to FHIR"
4. **Combine domains** - Use cross-domain prompts for realistic test data
5. **Check consistency** - Verify diagnoses, medications, and claims align
