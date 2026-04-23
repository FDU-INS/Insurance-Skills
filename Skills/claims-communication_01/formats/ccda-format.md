---
name: ccda-format
description: "C-CDA clinical document generation for care transitions, health information exchange, and clinical documentation. Use this skill when asked to generate C-CDA, CCD, Continuity of Care Document, Discharge Summary, Referral Note, Transfer Summary, or clinical XML documents from PatientSim data."
---

# C-CDA Format Transformation

## Trigger Phrases

- C-CDA, CDA, CCD, Continuity of Care Document
- Discharge Summary, Hospital Discharge
- Referral Note, Specialist Referral
- Transfer Summary, Care Transition Document
- Clinical Document Architecture, HL7 CDA
- Health Information Exchange, HIE document
- Patient summary XML, Clinical XML

## Overview

C-CDA (Consolidated Clinical Document Architecture) is the US standard for clinical document exchange, built on HL7 CDA R2. It defines structured XML documents for sharing patient information during care transitions.

### Key Characteristics

- **XML-based**: Documents are structured XML with both human-readable narrative and machine-processable entries
- **Template-driven**: Each document type, section, and entry has a unique template OID (Object Identifier)
- **US Realm Header**: All documents require the US Realm Header template (2.16.840.1.113883.10.20.22.1.1)
- **Vocabulary bindings**: Standard code systems (SNOMED CT, RxNorm, LOINC, ICD-10-CM) are required

### Supported Document Types

| Document Type | LOINC Code | Template OID | Primary Use Cases |
|---------------|------------|--------------|-------------------|
| CCD (Continuity of Care Document) | 34133-9 | 2.16.840.1.113883.10.20.22.1.2 | Care transitions, patient portal, payer requests |
| Discharge Summary | 18842-5 | 2.16.840.1.113883.10.20.22.1.8 | Hospital to ambulatory handoff, SNF transfers |
| Referral Note | 57133-1 | 2.16.840.1.113883.10.20.22.1.14 | PCP to specialist referral, oncology consult |
| Transfer Summary | 18761-7 | 2.16.840.1.113883.10.20.22.1.13 | Hospital to SNF, ED to inpatient, ICU transfer |

## Section Templates

Each C-CDA document contains sections that map to PatientSim entities:

| Section | Template OID | LOINC | Maps From Entity |
|---------|--------------|-------|------------------|
| Problems | 2.16.840.1.113883.10.20.22.2.5.1 | 11450-4 | Diagnosis |
| Medications | 2.16.840.1.113883.10.20.22.2.1.1 | 10160-0 | MedicationRequest |
| Allergies | 2.16.840.1.113883.10.20.22.2.6.1 | 48765-2 | AllergyIntolerance |
| Results | 2.16.840.1.113883.10.20.22.2.3.1 | 30954-2 | LabResult |
| Vital Signs | 2.16.840.1.113883.10.20.22.2.4.1 | 8716-3 | VitalSign |
| Procedures | 2.16.840.1.113883.10.20.22.2.7.1 | 47519-4 | Procedure |
| Immunizations | 2.16.840.1.113883.10.20.22.2.2.1 | 11369-6 | Immunization |
| Plan of Treatment | 2.16.840.1.113883.10.20.22.2.10 | 18776-5 | CarePlan |
| Encounters | 2.16.840.1.113883.10.20.22.2.22.1 | 46240-8 | Encounter |
| Social History | 2.16.840.1.113883.10.20.22.2.17 | 29762-2 | Patient |
| Hospital Course | 2.16.840.1.113883.10.20.22.2.16 | 8648-8 | Encounter (narrative) |
| Discharge Instructions | 2.16.840.1.113883.10.20.22.2.41 | 8653-8 | CarePlan (instructions) |
| Reason for Referral | 1.3.6.1.4.1.19376.1.5.3.1.3.1 | 42349-1 | Encounter (reason) |

## Vocabulary Bindings

| Code System | OID | Usage |
|-------------|-----|-------|
| SNOMED CT | 2.16.840.1.113883.6.96 | Problems, procedures, clinical findings |
| RxNorm | 2.16.840.1.113883.6.88 | Medications |
| LOINC | 2.16.840.1.113883.6.1 | Labs, vitals, section codes, document types |
| ICD-10-CM | 2.16.840.1.113883.6.90 | Diagnosis codes (supplemental to SNOMED) |
| CPT | 2.16.840.1.113883.6.12 | Procedure codes |
| NDC | 2.16.840.1.113883.6.69 | Drug product identifiers |
| CVX | 2.16.840.1.113883.12.292 | Vaccine codes |

## Entity to CDA Mappings

### Patient → recordTarget/patientRole

```yaml
patient_mapping:
  recordTarget:
    patientRole:
      id:
        - root: "2.16.840.1.113883.4.1"           # SSN OID (if SSN available)
          extension: patient.ssn
        - root: "{{facility_oid}}"                 # Facility MRN
          extension: patient.mrn
      addr:
        streetAddressLine: patient.address.street
        city: patient.address.city
        state: patient.address.state
        postalCode: patient.address.postal_code
        country: "US"
      telecom:
        value: "tel:{{patient.phone}}"
        use: "HP"                                  # Home phone
      patient:
        name:
          given: patient.given_name
          family: patient.family_name
        administrativeGenderCode:
          code: patient.gender                     # M, F, UN
          codeSystem: "2.16.840.1.113883.5.1"
          displayName:
            M: "Male"
            F: "Female"
            UN: "Undifferentiated"
        birthTime:
          value: patient.birth_date                # YYYYMMDD format
        raceCode:                                   # If available
          code: patient.race_code
          codeSystem: "2.16.840.1.113883.6.238"
        languageCommunication:
          languageCode:
            code: patient.language                 # en-US default
```

### Encounter → encompassingEncounter

```yaml
encounter_mapping:
  componentOf:
    encompassingEncounter:
      id:
        root: "{{facility_oid}}"
        extension: encounter.encounter_id
      code:
        code: encounter.type_code                  # AMB, EMER, IMP, etc.
        codeSystem: "2.16.840.1.113883.5.4"
        displayName: encounter.type_display
      effectiveTime:
        low:
          value: encounter.start_date              # YYYYMMDDHHMMSS
        high:
          value: encounter.end_date                # YYYYMMDDHHMMSS (if completed)
      location:
        healthCareFacility:
          id:
            root: "{{facility_oid}}"
          code:
            code: encounter.facility_type
            codeSystem: "2.16.840.1.113883.1.11.17660"
          location:
            name: encounter.facility_name
            addr:
              streetAddressLine: facility.address.street
              city: facility.address.city
              state: facility.address.state
              postalCode: facility.address.postal_code
```

### Diagnosis → Problem Concern Act + Problem Observation

```yaml
diagnosis_mapping:
  # Problem Section entry
  entry:
    act:
      classCode: "ACT"
      moodCode: "EVN"
      templateId:
        root: "2.16.840.1.113883.10.20.22.4.3"     # Problem Concern Act
        extension: "2015-08-01"
      id:
        root: "{{uuid}}"
      code:
        code: "CONC"
        codeSystem: "2.16.840.1.113883.5.6"
      statusCode:
        code: diagnosis.status                      # active, completed, aborted
      effectiveTime:
        low:
          value: diagnosis.onset_date              # YYYYMMDD
        high:
          value: diagnosis.resolution_date         # YYYYMMDD (if resolved)
      entryRelationship:
        typeCode: "SUBJ"
        observation:
          classCode: "OBS"
          moodCode: "EVN"
          templateId:
            root: "2.16.840.1.113883.10.20.22.4.4"  # Problem Observation
            extension: "2015-08-01"
          id:
            root: "{{uuid}}"
          code:
            code: "55607006"                        # Problem
            codeSystem: "2.16.840.1.113883.6.96"
            displayName: "Problem"
          statusCode:
            code: "completed"
          effectiveTime:
            low:
              value: diagnosis.onset_date
          value:
            xsi_type: "CD"
            code: diagnosis.snomed_code             # Primary: SNOMED CT
            codeSystem: "2.16.840.1.113883.6.96"
            displayName: diagnosis.display
            translation:                            # Secondary: ICD-10-CM
              code: diagnosis.icd10_code
              codeSystem: "2.16.840.1.113883.6.90"
              displayName: diagnosis.icd10_display
```

### MedicationRequest → Medication Activity

```yaml
medication_mapping:
  # Medications Section entry
  entry:
    substanceAdministration:
      classCode: "SBADM"
      moodCode: "EVN"                               # EVN for administered, INT for ordered
      templateId:
        root: "2.16.840.1.113883.10.20.22.4.16"    # Medication Activity
        extension: "2014-06-09"
      id:
        root: "{{uuid}}"
      statusCode:
        code: medication.status                     # active, completed, on-hold
      effectiveTime:
        - xsi_type: "IVL_TS"                       # Duration
          low:
            value: medication.start_date
          high:
            value: medication.end_date              # nullFlavor="UNK" if ongoing
        - xsi_type: "PIVL_TS"                      # Frequency
          institutionSpecified: "true"
          period:
            value: medication.frequency_value       # e.g., 12
            unit: medication.frequency_unit         # e.g., "h" for every 12 hours
      routeCode:
        code: medication.route_code                 # C38288 (oral), C38276 (IV), etc.
        codeSystem: "2.16.840.1.113883.3.26.1.1"
        displayName: medication.route_display
      doseQuantity:
        value: medication.dose_value
        unit: medication.dose_unit                  # mg, mL, etc.
      consumable:
        manufacturedProduct:
          classCode: "MANU"
          templateId:
            root: "2.16.840.1.113883.10.20.22.4.23"
            extension: "2014-06-09"
          manufacturedMaterial:
            code:
              code: medication.rxnorm_code
              codeSystem: "2.16.840.1.113883.6.88"  # RxNorm
              displayName: medication.drug_name
```

### LabResult → Result Organizer + Result Observation

```yaml
lab_result_mapping:
  # Results Section entry
  entry:
    organizer:
      classCode: "BATTERY"
      moodCode: "EVN"
      templateId:
        root: "2.16.840.1.113883.10.20.22.4.1"     # Result Organizer
        extension: "2015-08-01"
      id:
        root: "{{uuid}}"
      code:
        code: lab.panel_loinc                       # Panel LOINC code
        codeSystem: "2.16.840.1.113883.6.1"
        displayName: lab.panel_name
      statusCode:
        code: "completed"
      effectiveTime:
        value: lab.collection_time                  # YYYYMMDDHHMMSS
      component:
        observation:
          classCode: "OBS"
          moodCode: "EVN"
          templateId:
            root: "2.16.840.1.113883.10.20.22.4.2"  # Result Observation
            extension: "2015-08-01"
          id:
            root: "{{uuid}}"
          code:
            code: lab.test_loinc
            codeSystem: "2.16.840.1.113883.6.1"
            displayName: lab.test_name
          statusCode:
            code: "completed"
          effectiveTime:
            value: lab.result_time
          value:
            xsi_type: "PQ"                          # Physical Quantity
            value: lab.value
            unit: lab.unit                          # UCUM units
          interpretationCode:
            code: lab.abnormal_flag                 # N, H, L, HH, LL
            codeSystem: "2.16.840.1.113883.5.83"
          referenceRange:
            observationRange:
              text: "{{lab.reference_range_low}} - {{lab.reference_range_high}} {{lab.unit}}"
              value:
                xsi_type: "IVL_PQ"
                low:
                  value: lab.reference_range_low
                  unit: lab.unit
                high:
                  value: lab.reference_range_high
                  unit: lab.unit
```

### AllergyIntolerance → Allergy Concern Act + Allergy Observation

```yaml
allergy_mapping:
  # Allergies Section entry
  entry:
    act:
      classCode: "ACT"
      moodCode: "EVN"
      templateId:
        root: "2.16.840.1.113883.10.20.22.4.30"    # Allergy Concern Act
        extension: "2015-08-01"
      id:
        root: "{{uuid}}"
      code:
        code: "CONC"
        codeSystem: "2.16.840.1.113883.5.6"
      statusCode:
        code: allergy.status                        # active, inactive
      effectiveTime:
        low:
          value: allergy.onset_date
      entryRelationship:
        typeCode: "SUBJ"
        observation:
          classCode: "OBS"
          moodCode: "EVN"
          templateId:
            root: "2.16.840.1.113883.10.20.22.4.7"  # Allergy Observation
            extension: "2014-06-09"
          id:
            root: "{{uuid}}"
          code:
            code: "ASSERTION"
            codeSystem: "2.16.840.1.113883.5.4"
          statusCode:
            code: "completed"
          effectiveTime:
            low:
              value: allergy.onset_date
          value:
            xsi_type: "CD"
            code: allergy.type_code                 # 419511003 (drug), 418038007 (food)
            codeSystem: "2.16.840.1.113883.6.96"
            displayName: allergy.type_display
          participant:
            typeCode: "CSM"
            participantRole:
              classCode: "MANU"
              playingEntity:
                classCode: "MMAT"
                code:
                  code: allergy.substance_code      # RxNorm for drugs
                  codeSystem: "2.16.840.1.113883.6.88"
                  displayName: allergy.substance_name
          entryRelationship:
            typeCode: "MFST"                        # Reaction manifestation
            observation:
              value:
                code: allergy.reaction_code         # SNOMED reaction code
                codeSystem: "2.16.840.1.113883.6.96"
                displayName: allergy.reaction_display
```

### Procedure → Procedure Activity Procedure

```yaml
procedure_mapping:
  # Procedures Section entry
  entry:
    procedure:
      classCode: "PROC"
      moodCode: "EVN"
      templateId:
        root: "2.16.840.1.113883.10.20.22.4.14"    # Procedure Activity Procedure
        extension: "2014-06-09"
      id:
        root: "{{uuid}}"
      code:
        code: procedure.cpt_code                    # Primary: CPT
        codeSystem: "2.16.840.1.113883.6.12"
        displayName: procedure.procedure_name
        translation:
          code: procedure.snomed_code               # Secondary: SNOMED CT
          codeSystem: "2.16.840.1.113883.6.96"
          displayName: procedure.snomed_display
      statusCode:
        code: "completed"
      effectiveTime:
        value: procedure.procedure_date             # YYYYMMDDHHMMSS
      performer:
        assignedEntity:
          id:
            root: "2.16.840.1.113883.4.6"           # NPI OID
            extension: procedure.provider_npi
          assignedPerson:
            name:
              given: procedure.provider_first_name
              family: procedure.provider_last_name
```

### Immunization → Immunization Activity

```yaml
immunization_mapping:
  # Immunizations Section entry
  entry:
    substanceAdministration:
      classCode: "SBADM"
      moodCode: "EVN"
      templateId:
        root: "2.16.840.1.113883.10.20.22.4.52"    # Immunization Activity
        extension: "2015-08-01"
      id:
        root: "{{uuid}}"
      statusCode:
        code: "completed"
      effectiveTime:
        value: immunization.administration_date     # YYYYMMDD
      routeCode:
        code: immunization.route_code
        codeSystem: "2.16.840.1.113883.3.26.1.1"
        displayName: immunization.route_display
      consumable:
        manufacturedProduct:
          classCode: "MANU"
          templateId:
            root: "2.16.840.1.113883.10.20.22.4.54"
            extension: "2014-06-09"
          manufacturedMaterial:
            code:
              code: immunization.cvx_code
              codeSystem: "2.16.840.1.113883.12.292"  # CVX
              displayName: immunization.vaccine_name
            lotNumberText: immunization.lot_number
```

### CarePlan → Plan of Treatment Section

```yaml
care_plan_mapping:
  # Plan of Treatment Section entry
  entry:
    act:
      classCode: "ACT"
      moodCode: "INT"                               # Intent
      templateId:
        root: "2.16.840.1.113883.10.20.22.4.20"    # Planned Act
        extension: "2014-06-09"
      id:
        root: "{{uuid}}"
      code:
        code: care_plan.activity_code
        codeSystem: "2.16.840.1.113883.6.96"        # SNOMED CT
        displayName: care_plan.activity_name
      statusCode:
        code: "active"
      effectiveTime:
        low:
          value: care_plan.planned_date
```

## Domain-Specific Considerations

### Diabetes

When generating C-CDA documents for diabetic patients:

**Problems Section:**
- Primary diagnosis: Use SNOMED code 44054006 (Type 2 diabetes mellitus)
- Include translation with ICD-10-CM code (E11.x)
- Add diabetic complications as separate problem observations (retinopathy, nephropathy, neuropathy)

**Results Section:**
- A1C results: LOINC 4548-4, target < 7.0%
- Fasting glucose: LOINC 1558-6
- eGFR for nephropathy monitoring: LOINC 48642-3 or 88293-6
- Urine albumin/creatinine ratio: LOINC 9318-7

**Medications Section:**
- First-line: Metformin (RxNorm 860975)
- SGLT2 inhibitors: Empagliflozin (RxNorm 1545653), Dapagliflozin (RxNorm 1488574)
- GLP-1 agonists: Semaglutide (RxNorm 1991302)
- Insulin: Glargine (RxNorm 274783)

### Heart Failure

When generating C-CDA documents for heart failure patients:

**Problems Section:**
- Primary diagnosis: Use SNOMED code 84114007 (Heart failure)
- Specify type: Systolic (417996009), Diastolic (418304008)
- Include ICD-10-CM translation (I50.x)
- Include NYHA class as observation

**Results Section:**
- BNP: LOINC 30934-4 (elevated indicates decompensation)
- NT-proBNP: LOINC 33762-6
- Sodium: LOINC 2951-2 (hyponatremia monitoring)
- Potassium: LOINC 2823-3 (MRA monitoring)
- Creatinine/eGFR: Cardiorenal syndrome monitoring

**Medications Section (GDMT - Guideline Directed Medical Therapy):**
- ARNI: Sacubitril/Valsartan (RxNorm 1656340)
- Beta-blocker: Carvedilol (RxNorm 20352), Metoprolol Succinate (RxNorm 866514)
- SGLT2i: Dapagliflozin (RxNorm 1488574)
- MRA: Spironolactone (RxNorm 9997)
- Diuretics: Furosemide (RxNorm 4603)

**Vital Signs Section:**
- Blood pressure trends
- Weight (fluid status indicator)
- Heart rate (beta-blocker effect)
- SpO2 (decompensation indicator)

### Chronic Kidney Disease

When generating C-CDA documents for CKD patients:

**Problems Section:**
- Stage-specific diagnosis: Use SNOMED codes for CKD stages
- Include ICD-10-CM staging codes (N18.1-N18.6)
- Add etiology as linked problem (diabetic, hypertensive)
- Include complications: Anemia (D63.1), Hyperparathyroidism (E21.1)

**Results Section:**
- Creatinine: LOINC 2160-0
- eGFR: LOINC 48642-3 (stage determines value range)
- BUN: LOINC 3094-0
- Potassium: LOINC 2823-3 (hyperkalemia risk)
- Phosphorus: LOINC 2777-1 (mineral bone disease)
- Calcium: LOINC 17861-6
- PTH: LOINC 2731-8 (secondary hyperparathyroidism)
- Hemoglobin: LOINC 718-7 (anemia of CKD)
- Bicarbonate: LOINC 1963-8 (metabolic acidosis)

**Medications Section:**
- ACE inhibitors: Lisinopril (RxNorm 104376) - nephroprotection
- Phosphate binders: Sevelamer (RxNorm 273279)
- ESAs: Epoetin alfa (RxNorm 9374)
- Vitamin D: Calcitriol (RxNorm 1534)
- Potassium binders: Patiromer (RxNorm 1876449)

### Oncology

When generating C-CDA documents for oncology patients:

**Problems Section:**
- Primary malignancy: Use ICD-10-CM C codes with SNOMED translation
- Include staging as linked observation
- Document metastatic sites separately (C78.x, C79.x)
- Include history codes for survivors (Z85.x)
- Document adverse effects (D70.1 neutropenia, G62.0 neuropathy)

**Results Section:**
- CBC with differential: Myelosuppression monitoring
- Tumor markers by cancer type:
  - Breast: CA 15-3 (LOINC 6875-9)
  - Colorectal: CEA (LOINC 2039-6)
  - Ovarian: CA-125 (LOINC 10334-1)
  - Prostate: PSA (LOINC 2857-1)
  - Pancreatic: CA 19-9 (LOINC 24108-3)
- CMP for organ function monitoring
- LDH for lymphoma (LOINC 2532-0)

**Procedures Section:**
- Surgical procedures with CPT/SNOMED codes
- Chemotherapy administration (Z51.11)
- Radiation therapy (Z51.0)

**Medications Section:**
- Chemotherapy agents by RxNorm code
- Supportive care: G-CSF, antiemetics, pain management
- Targeted therapy and immunotherapy agents

## XML Structure Patterns

### Document Header Template

```xml
<?xml version="1.0" encoding="UTF-8"?>
<ClinicalDocument xmlns="urn:hl7-org:v3" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <realmCode code="US"/>
  <typeId root="2.16.840.1.113883.1.3" extension="POCD_HD000040"/>
  <!-- US Realm Header -->
  <templateId root="2.16.840.1.113883.10.20.22.1.1" extension="2015-08-01"/>
  <!-- Document-specific template (e.g., CCD) -->
  <templateId root="{{document_template_oid}}" extension="2015-08-01"/>
  <id root="{{uuid}}"/>
  <code code="{{document_loinc}}" codeSystem="2.16.840.1.113883.6.1"
        codeSystemName="LOINC" displayName="{{document_display_name}}"/>
  <title>{{document_title}}</title>
  <effectiveTime value="{{generation_timestamp}}"/>
  <confidentialityCode code="N" codeSystem="2.16.840.1.113883.5.25" displayName="Normal"/>
  <languageCode code="en-US"/>

  <!-- recordTarget (Patient) -->
  <recordTarget>
    <patientRole>
      <!-- Patient identifiers, demographics -->
    </patientRole>
  </recordTarget>

  <!-- author (Document creator) -->
  <author>
    <time value="{{generation_timestamp}}"/>
    <assignedAuthor>
      <!-- Author details -->
    </assignedAuthor>
  </author>

  <!-- custodian (Organization responsible) -->
  <custodian>
    <assignedCustodian>
      <representedCustodianOrganization>
        <!-- Organization details -->
      </representedCustodianOrganization>
    </assignedCustodian>
  </custodian>

  <!-- componentOf (Encounter context) -->
  <componentOf>
    <encompassingEncounter>
      <!-- Encounter details -->
    </encompassingEncounter>
  </componentOf>

  <!-- Document body with sections -->
  <component>
    <structuredBody>
      <!-- Sections -->
    </structuredBody>
  </component>
</ClinicalDocument>
```

### Section Template

```xml
<component>
  <section>
    <templateId root="{{section_template_oid}}" extension="2015-08-01"/>
    <code code="{{section_loinc}}" codeSystem="2.16.840.1.113883.6.1"
          codeSystemName="LOINC" displayName="{{section_display_name}}"/>
    <title>{{section_title}}</title>

    <!-- Human-readable narrative (required) -->
    <text>
      <table border="1" width="100%">
        <thead>
          <tr>
            <th>{{column_headers}}</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>{{row_data}}</td>
          </tr>
        </tbody>
      </table>
    </text>

    <!-- Machine-processable entries -->
    <entry>
      {{entry_content}}
    </entry>
  </section>
</component>
```

## Generation Examples

### Example: CCD for Diabetic Patient with Heart Failure

**Request:**
> Generate a CCD for a 65-year-old male diabetic patient with heart failure.

**Claude generates a CCD containing:**

**Problems Section:**
- E11.9 / 44054006 - Type 2 diabetes mellitus (active)
- I50.22 / 441530006 - Chronic systolic heart failure (active)
- I10 / 59621000 - Essential hypertension (active)

**Medications Section:**
- Metformin 1000 mg PO BID (RxNorm 860975)
- Empagliflozin 10 mg PO daily (RxNorm 1545653) - dual diabetes/HF benefit
- Sacubitril/Valsartan 49/51 mg PO BID (RxNorm 1656340)
- Carvedilol 25 mg PO BID (RxNorm 20352)
- Spironolactone 25 mg PO daily (RxNorm 9997)

**Results Section:**
- A1C: 7.2% (LOINC 4548-4)
- BNP: 450 pg/mL (LOINC 30934-4)
- Creatinine: 1.3 mg/dL (LOINC 2160-0)
- eGFR: 58 mL/min/1.73m2 (LOINC 48642-3)
- Sodium: 138 mmol/L (LOINC 2951-2)
- Potassium: 4.5 mmol/L (LOINC 2823-3)

**Vital Signs Section:**
- BP: 124/76 mmHg
- HR: 68 bpm
- Weight: 185 lb

### Example: Discharge Summary for Breast Cancer Patient

**Request:**
> Create a discharge summary for a breast cancer patient after chemotherapy hospitalization.

**Claude generates a Discharge Summary containing:**

**Hospital Course Section:**
- Narrative describing admission for cycle 4 of AC-T chemotherapy
- Development of febrile neutropenia, treated with IV antibiotics
- Resolution of fever, ANC recovery to 1500

**Problems Section:**
- C50.912 / 254837009 - Malignant neoplasm of left female breast (active)
- D70.1 / 417181009 - Drug-induced neutropenia (resolved)
- Z51.11 - Encounter for antineoplastic chemotherapy

**Procedures Section:**
- Chemotherapy administration
- Central line care

**Medications Section (Discharge):**
- Pegfilgrastim 6 mg SC once (RxNorm 358545) - G-CSF prophylaxis
- Ondansetron 8 mg PO TID PRN (RxNorm 283737) - nausea
- Levofloxacin 500 mg PO daily x 7 days (RxNorm 199885) - prophylaxis

**Results Section:**
- WBC: 5.2 x10^3/uL (LOINC 6690-2)
- ANC: 2800 (calculated)
- Hemoglobin: 10.5 g/dL (LOINC 718-7)
- Platelets: 145 x10^3/uL (LOINC 777-3)

**Discharge Instructions Section:**
- Return precautions: fever > 100.4°F, bleeding
- Follow-up: Oncology in 1 week for cycle 5
- Activity: Resume normal activities as tolerated

## Related Skills

- [patientsim/SKILL.md](../skills/patientsim/SKILL.md) - PatientSim foundational model and entities
- [data-models.md](../references/data-models.md) - Entity schemas and relationships
- [code-systems.md](../references/code-systems.md) - Healthcare code system references
- [fhir-r4.md](fhir-r4.md) - FHIR R4 format for comparison
- [hl7v2-adt.md](hl7v2-adt.md) - HL7v2 format for legacy systems
- [diabetes-management.md](../skills/patientsim/diabetes-management.md) - Diabetes clinical patterns
- [heart-failure.md](../skills/patientsim/heart-failure.md) - Heart failure clinical patterns
- [chronic-kidney-disease.md](../skills/patientsim/chronic-kidney-disease.md) - CKD clinical patterns
- [oncology-domain.md](../references/oncology-domain.md) - Oncology clinical patterns

## Reference Data

- [ccda-template-oids.csv](../references/ccda/ccda-template-oids.csv) - Template identifiers
- [ccda-section-requirements.csv](../references/ccda/ccda-section-requirements.csv) - Section requirements by document type
- [ccda-code-systems.csv](../references/ccda/ccda-code-systems.csv) - Vocabulary OIDs
- [ccda-snomed-problem-mappings.csv](../references/ccda/ccda-snomed-problem-mappings.csv) - ICD-10 to SNOMED mappings
- [ccda-loinc-lab-panels.csv](../references/ccda/ccda-loinc-lab-panels.csv) - Lab LOINC codes
- [ccda-vital-signs-loinc.csv](../references/ccda/ccda-vital-signs-loinc.csv) - Vital sign LOINC codes
