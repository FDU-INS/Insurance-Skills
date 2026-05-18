# Extending HealthSim

Learn how to customize and extend HealthSim with new scenarios, formats, and code systems.

---

## Architecture Overview

```
healthsim-common/
├── SKILL.md                    # Master skill (entry point)
├── skills/                  # Domain-specific generation rules
│   ├── patientsim/            # Clinical data
│   ├── membersim/             # Claims data
│   └── rxmembersim/           # Pharmacy data
├── formats/                    # Output transformations
├── references/                 # Shared data (codes, models, rules)
└── hello-healthsim/           # Getting started guide
```

### How It Works

1. **User request** → Claude reads relevant skill files
2. **Skill files** → Define what to generate and how
3. **References** → Provide codes, schemas, validation rules
4. **Formats** → Transform output to standards (FHIR, HL7v2, X12)

---

## Adding a New Scenario

### Step 1: Choose the Product

| Product | Directory | Use For |
|---------|-----------|---------|
| PatientSim | `skills/patientsim/` | Clinical/EMR scenarios |
| MemberSim | `skills/membersim/` | Claims/payer scenarios |
| RxMemberSim | `skills/rxmembersim/` | Pharmacy/PBM scenarios |

### Step 2: Create the Scenario File

```bash
# Example: Adding a maternal health scenario
touch skills/patientsim/maternal-health.md
```

### Step 3: Follow the Template

```markdown
# Maternal Health Scenario

## Trigger Phrases

- pregnancy
- prenatal
- OB visit
- postpartum
- maternal

## Parameters

| Parameter | Type | Default | Options |
|-----------|------|---------|---------|
| trimester | string | first | first, second, third, postpartum |
| risk_level | string | low | low, moderate, high |
| complications | list | none | gestational_diabetes, preeclampsia, etc. |

## Clinical Context

### Normal Pregnancy Timeline
- First trimester: Weeks 1-12
- Second trimester: Weeks 13-26
- Third trimester: Weeks 27-40

### Common Diagnoses

| Condition | ICD-10 | Trimester |
|-----------|--------|-----------|
| Normal pregnancy | Z34.00 | Any |
| Gestational diabetes | O24.4x | 2nd-3rd |
| Preeclampsia | O14.x | 2nd-3rd |

### Typical Visit Schedule

| Week | Visit Type | CPT |
|------|------------|-----|
| 8-10 | Initial OB | 99205 |
| 12 | First trimester screen | 99214 + labs |
| 16-20 | Anatomy scan | 76805 |

## Example Output

```json
{
  "patient": {
    "mrn": "MRN00000001",
    "name": { "given_name": "Sarah", "family_name": "Johnson" },
    "birth_date": "1992-04-15",
    "gender": "F"
  },
  "pregnancy": {
    "gestational_age_weeks": 28,
    "trimester": "third",
    "edd": "2025-04-20",
    "gravida": 2,
    "para": 1
  },
  "diagnoses": [
    { "code": "Z34.03", "description": "Supervision of normal third trimester pregnancy" }
  ]
}
```

## Related Skills

- [SKILL.md](../skills/patientsim/SKILL.md) - PatientSim overview
- [code-systems.md](../references/code-systems.md) - OB-related codes
```

### Step 4: Update the SKILL.md

Add your scenario to the product's SKILL.md:

```markdown
## Scenario Skills

| Scenario | Trigger Phrases | File |
|----------|-----------------|------|
| ... existing ... |
| **Maternal Health** | pregnancy, prenatal, OB visit | [maternal-health.md](../skills/patientsim/maternal-health.md) |
```

### Step 5: Update the Main SKILL.md

Add to the master skill file's scenario list.

---

## Adding a New Format

### Step 1: Create the Format File

```bash
touch formats/ccd-r2.md
```

### Step 2: Define Transformation Rules

```markdown
# CCD R2 Format

## Overview

Consolidated Clinical Document Architecture (C-CDA) Release 2.1 format.

## Trigger Phrases

- as CCD
- as C-CDA
- as CCDA
- continuity of care document

## Transformation Rules

### Patient → recordTarget

```xml
<recordTarget>
  <patientRole>
    <id root="2.16.840.1.113883.4.1" extension="{mrn}"/>
    <addr>
      <streetAddressLine>{address.street}</streetAddressLine>
      <city>{address.city}</city>
      <state>{address.state}</state>
      <postalCode>{address.postal_code}</postalCode>
    </addr>
    <patient>
      <name>
        <given>{name.given_name}</given>
        <family>{name.family_name}</family>
      </name>
      <administrativeGenderCode code="{gender}" codeSystem="2.16.840.1.113883.5.1"/>
      <birthTime value="{birth_date:YYYYMMDD}"/>
    </patient>
  </patientRole>
</recordTarget>
```

### Diagnosis → Problem Section

Map ICD-10 codes to SNOMED CT where possible.

## Example Output

[Include full CCD example]

## Related Formats

- [fhir-r4.md](../formats/fhir-r4.md) - Alternative modern format
```

### Step 3: Update Main SKILL.md

Add the new format to the formats table.

---

## Adding Code Systems

### Step 1: Update references/code-systems.md

Add new codes to the appropriate section:

```markdown
## Obstetric Codes

### ICD-10-CM Pregnancy Codes

| Code | Description |
|------|-------------|
| Z34.00 | Supervision of normal first pregnancy, unspecified trimester |
| Z34.01 | Supervision of normal first pregnancy, first trimester |
| O24.410 | Gestational diabetes mellitus in pregnancy, diet controlled |
| O14.00 | Mild to moderate pre-eclampsia, unspecified trimester |
```

### Step 2: Add Lookup Tables

For frequently used codes, add JSON lookup tables:

```json
{
  "pregnancy_supervision": {
    "first_pregnancy": {
      "unspecified": "Z34.00",
      "first_trimester": "Z34.01",
      "second_trimester": "Z34.02",
      "third_trimester": "Z34.03"
    },
    "other_normal": {
      "unspecified": "Z34.80",
      "first_trimester": "Z34.81"
    }
  }
}
```

---

## Modifying Data Models

### Step 1: Update references/data-models.md

Add or modify entity schemas:

```markdown
### PregnancyRecord

Tracks pregnancy-specific information.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| patient_mrn | string | yes | Link to patient |
| edd | date | yes | Estimated due date |
| lmp | date | no | Last menstrual period |
| gestational_age_weeks | int | no | Current gestational age |
| gravida | int | yes | Number of pregnancies |
| para | int | yes | Number of deliveries |
| risk_level | string | no | low, moderate, high |

```json
{
  "pregnancy": {
    "patient_mrn": "MRN00000001",
    "edd": "2025-04-20",
    "lmp": "2024-07-14",
    "gestational_age_weeks": 28,
    "gravida": 2,
    "para": 1,
    "risk_level": "low"
  }
}
```
```

---

## Adding Validation Rules

### Step 1: Update references/validation-rules.md

```markdown
### Pregnancy Validation Rules

| Rule | Description | Severity |
|------|-------------|----------|
| PREG-001 | EDD must be 280 days after LMP | error |
| PREG-002 | Gestational age must match EDD | warning |
| PREG-003 | Pregnancy diagnosis requires female gender | error |
| PREG-004 | Postpartum codes require delivery date | error |
```

---

## Best Practices

### 1. Be Specific with Trigger Phrases

Choose phrases that:
- Are commonly used in requests
- Don't overlap with other scenarios
- Include abbreviations and full terms

### 2. Include Realistic Examples

Every scenario should have:
- At least one complete example output
- Key points explaining important fields
- Variations showing different parameters

### 3. Cross-Reference Properly

Link to:
- Parent SKILL.md files
- Related scenarios
- Relevant reference files
- Format transformations

### 4. Maintain Code Accuracy

- Use real ICD-10, CPT, LOINC, NDC codes
- Include code descriptions
- Verify codes are current (check annual updates)

### 5. Test Your Extensions

Before committing:
1. Try generating with your new scenario
2. Verify output matches expected format
3. Check cross-references work
4. Test format transformations

---

## Example: Complete Extension

Here's a checklist for adding a new "Wound Care" scenario:

- [ ] Create `skills/patientsim/wound-care.md`
  - [ ] Add trigger phrases (wound, ulcer, debridement)
  - [ ] Define parameters (wound_type, location, severity)
  - [ ] Add wound-related ICD-10 codes
  - [ ] Add wound care CPT codes
  - [ ] Include example output
- [ ] Update `skills/patientsim/SKILL.md`
  - [ ] Add to scenario table
  - [ ] Add to related skills
- [ ] Update `references/code-systems.md`
  - [ ] Add wound ICD-10 codes section
  - [ ] Add wound care CPT codes
- [ ] Update `references/data-models.md`
  - [ ] Add WoundAssessment entity if needed
- [ ] Test the scenario
  - [ ] "Generate a patient with a diabetic foot ulcer"
  - [ ] "Generate a wound care claim"

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes following this guide
4. Test thoroughly
5. Submit a pull request

Include in your PR:
- Description of what you added
- Example prompts that use the new content
- Any new dependencies or requirements
