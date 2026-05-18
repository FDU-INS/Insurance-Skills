# Validation Rules Reference

Validation rules ensure generated data is structurally correct, temporally consistent, and clinically coherent.

## Table of Contents

- [Structural Validation](#structural-validation)
- [Temporal Validation](#temporal-validation)
- [Clinical Coherence](#clinical-coherence)
- [Claims Validation](#claims-validation)
- [Pharmacy Validation (DUR)](#pharmacy-validation-dur)
- [Cross-Entity Validation](#cross-entity-validation)

---

## Structural Validation

### Required Fields

Every entity must have all `required` fields populated per schema.

| Entity | Required Fields |
|--------|-----------------|
| Patient | mrn, name.family, name.given, birth_date, gender |
| Encounter | id, patient_id, type, status, period.start |
| Diagnosis | code, system, display |
| Claim | id, member_id, type, status, service_date, lines[] |
| ClaimLine | line_number, procedure_code, service_date, billed_amount |
| Prescription | id, patient_id, prescriber.npi, medication.ndc, written_date |
| PharmacyClaim | id, prescription_id, member_id, pharmacy.ncpdp_id, fill_date |

### Identifier Formats

| Identifier | Pattern | Example | Validation |
|------------|---------|---------|------------|
| MRN | `MRN[0-9]{8}` | MRN00001234 | Unique per facility |
| Member ID | `[A-Z0-9]{9,12}` | ABC123456789 | Unique per payer |
| Claim ID | `CLM[0-9]{12}` | CLM000000001234 | Unique, sequential |
| NPI | `[0-9]{10}` | 1234567890 | Luhn checksum valid |
| NDC | `[0-9]{11}` | 00000123456 | 5-4-2 format |
| ICD-10-CM | `[A-Z][0-9]{2}(\.[0-9A-Z]{1,4})?` | E11.9 | Valid category |
| CPT | `[0-9]{5}` | 99213 | Known procedure |
| LOINC | `[0-9]+-[0-9]` | 2345-7 | Valid code |

### NPI Validation (Luhn Algorithm)

```
Valid NPI: Last digit is checksum
1. Prefix NPI with 80840 (for health care)
2. Double every other digit from right
3. Sum all digits
4. Check digit makes sum divisible by 10
```

### Code System URIs

| System | URI | Required With |
|--------|-----|---------------|
| ICD-10-CM | `http://hl7.org/fhir/sid/icd-10-cm` | Diagnosis codes |
| ICD-10-PCS | `http://hl7.org/fhir/sid/icd-10-pcs` | Procedure codes (inpatient) |
| CPT | `http://www.ama-assn.org/go/cpt` | Procedure codes (professional) |
| LOINC | `http://loinc.org` | Lab/vital codes |
| RxNorm | `http://www.nlm.nih.gov/research/umls/rxnorm` | Medications |
| SNOMED CT | `http://snomed.info/sct` | Clinical findings |
| NDC | `http://hl7.org/fhir/sid/ndc` | Drug products |

---

## Temporal Validation

### Date Ordering Rules

| Rule | Constraint | Error |
|------|------------|-------|
| Birth before all | `birth_date < all_other_dates` | Date precedes birth |
| Death after all | `deceased_date > all_clinical_dates` | Activity after death |
| Encounter order | `period.start <= period.end` | Invalid period |
| Service order | `service_date <= service_end_date` | Invalid service period |
| Prescription sequence | `written_date <= fill_date` | Fill before written |
| Claim timing | `service_date <= received_date` | Received before service |
| Coverage required | `service_date BETWEEN coverage_start AND coverage_end` | No coverage |

### Timeline Consistency

```
Patient Timeline:
birth_date
  → first_encounter
    → diagnoses (onset_date >= encounter_date)
      → prescriptions (written_date >= diagnosis_date)
        → pharmacy_claims (fill_date >= written_date)
          → refills (fill_date > previous_fill + days_supply - 7)
            → [deceased_date] (if applicable)
```

### Encounter Duration Rules

| Encounter Type | Typical Duration | Maximum |
|----------------|------------------|---------|
| ambulatory | 15-60 minutes | 8 hours |
| emergency | 1-12 hours | 72 hours |
| observation | 8-48 hours | 48 hours |
| inpatient | 1-14 days | 365 days |
| virtual | 10-30 minutes | 2 hours |

### Prescription Timing

| Check | Rule |
|-------|------|
| Written validity | written_date within last 1 year (non-controlled) |
| Controlled validity | written_date within last 6 months (Schedule II-V) |
| Fill timing | first_fill within 10 days of written_date |
| Refill interval | next_refill >= previous_fill_date + days_supply - 7 |
| Early refill | not before 75% of days_supply elapsed |

---

## Clinical Coherence

### Age-Appropriate Conditions

| Condition Category | Valid Age Range | ICD-10 Examples |
|--------------------|-----------------|-----------------|
| Pediatric only | 0-17 | P07 (premature), Z00.12 (well child) |
| Adult onset | 18+ | E11 (Type 2 DM), I10 (HTN) |
| Geriatric common | 65+ | G30 (Alzheimer's), M81 (Osteoporosis) |
| Any age | 0-120 | J06 (URI), S00-T88 (injuries) |

### Age Validation Matrix

| Code | Min Age | Max Age | Gender | Notes |
|------|---------|---------|--------|-------|
| E11.x | 10 | - | Any | Type 2 diabetes rare <10 |
| N40.x | 40 | - | Male | Prostate conditions |
| N80.x | 12 | 55 | Female | Endometriosis |
| Z23 | 0 | - | Any | Immunization (various schedules) |
| O00-O9A | 10 | 55 | Female | Pregnancy |
| P00-P96 | 0 | 0.08 | Any | Perinatal (~28 days) |

### Gender-Appropriate Conditions

| Gender | Allowed Codes | Excluded Codes |
|--------|---------------|----------------|
| Male | N40-N51 (male genital) | N70-N98 (female genital), O00-O9A (pregnancy) |
| Female | N70-N98, O00-O9A | N40-N51 |
| Other/Unknown | All except gender-exclusive | - |

### Diagnosis-Procedure Coherence

| Diagnosis | Expected Procedures | Invalid Procedures |
|-----------|--------------------|--------------------|
| E11 (T2DM) | 82947 (glucose), 83036 (A1C) | 27447 (knee replacement) unrelated |
| I10 (HTN) | 93000 (ECG), 80061 (lipid panel) | - |
| M17 (Knee OA) | 27447 (TKR), 20610 (injection) | - |
| C50 (Breast CA) | 19301 (mastectomy), 77067 (mammogram) | Only for female/trans |

### Diagnosis-Medication Coherence

Medications must have an indication matching a diagnosis:

| Medication Class | Required Diagnosis | ICD-10 Codes |
|------------------|-------------------|--------------|
| Metformin | Diabetes | E08-E13 |
| Lisinopril | Hypertension or CHF | I10, I50 |
| Atorvastatin | Hyperlipidemia or ASCVD | E78, I25 |
| Albuterol | Asthma or COPD | J45, J44 |
| Levothyroxine | Hypothyroidism | E03 |
| Methotrexate | RA or Psoriasis | M05, M06, L40 |
| Insulin | Diabetes | E08-E13 |
| Warfarin | A-fib or DVT/PE | I48, I26, I82 |

### Lab Value Ranges

| Test (LOINC) | Normal Range | Critical Low | Critical High | Unit |
|--------------|--------------|--------------|---------------|------|
| Glucose (2345-7) | 70-100 | <40 | >500 | mg/dL |
| HbA1c (4548-4) | 4.0-5.6 | <3.0 | >15.0 | % |
| Creatinine (2160-0) | 0.7-1.3 | <0.3 | >10.0 | mg/dL |
| eGFR (33914-3) | >60 | <15 | - | mL/min/1.73m2 |
| WBC (6690-2) | 4.5-11.0 | <1.0 | >30.0 | 10*3/uL |
| Hemoglobin (718-7) | 12.0-17.5 | <7.0 | >20.0 | g/dL |
| Platelets (777-3) | 150-400 | <50 | >1000 | 10*3/uL |
| Sodium (2951-2) | 136-145 | <120 | >160 | mmol/L |
| Potassium (2823-3) | 3.5-5.0 | <2.5 | >6.5 | mmol/L |
| TSH (3016-3) | 0.4-4.0 | <0.01 | >100 | mIU/L |
| LDL (2089-1) | <100 | - | >190 | mg/dL |
| ALT (1742-6) | 7-56 | - | >1000 | U/L |

### Vital Sign Ranges

| Vital | Normal Adult | Low | High | Critical |
|-------|--------------|-----|------|----------|
| Systolic BP | 90-120 | <90 | 120-140 | >180 |
| Diastolic BP | 60-80 | <60 | 80-90 | >120 |
| Heart Rate | 60-100 | <50 | 100-120 | <40 or >150 |
| Resp Rate | 12-20 | <10 | 20-30 | <8 or >35 |
| Temperature | 36.1-37.2°C | <35.0 | 37.3-38.3 | <34 or >40 |
| O2 Sat | 95-100% | 90-95 | - | <90 |
| BMI | 18.5-24.9 | <18.5 | 25-30 | >40 |

---

## Claims Validation

### Claim Type Requirements

| Claim Type | Required Fields | Special Rules |
|------------|-----------------|---------------|
| professional | place_of_service, rendering_provider | Max 50 lines |
| institutional | facility, revenue_codes, drg (if inpatient) | Admission/discharge dates |
| pharmacy | ndc, days_supply, pharmacy | Single line per claim |

### Diagnosis Validation

| Rule | Description |
|------|-------------|
| Principal required | Institutional claims must have principal diagnosis |
| Valid ICD-10 | Code must be valid for service date |
| Specificity | Use most specific code available |
| Sequence | Principal, admitting, then secondary |
| Limit | Maximum 12 diagnosis codes per claim |

### Procedure Code Validation

| Rule | Description |
|------|-------------|
| Valid CPT/HCPCS | Code must exist and be active |
| Valid modifiers | Each modifier must be appropriate for code |
| Units reasonable | Units must be clinically reasonable |
| Unbundling | No unbundled services (check CCI edits) |

### Place of Service Validation

| POS Code | Description | Valid Claim Types |
|----------|-------------|-------------------|
| 11 | Office | Professional |
| 21 | Inpatient Hospital | Professional, Institutional |
| 22 | Outpatient Hospital | Professional, Institutional |
| 23 | Emergency Room | Professional, Institutional |
| 31 | Skilled Nursing | Professional, Institutional |
| 81 | Independent Lab | Professional |

### Payment Calculation Rules

```
allowed_amount = MIN(billed_amount, fee_schedule_amount)
plan_pay = allowed_amount - deductible - copay - coinsurance
member_responsibility = deductible + copay + coinsurance
```

| Scenario | Calculation |
|----------|-------------|
| Deductible not met | deductible = MIN(remaining_deductible, allowed_amount) |
| Copay applies | copay = plan_copay_amount |
| Coinsurance applies | coinsurance = (allowed_amount - deductible - copay) * coinsurance_rate |
| OOP max met | member_responsibility = 0 |

### Adjustment Reason Codes

| Group | Meaning | Example Codes |
|-------|---------|---------------|
| CO | Contractual Obligation | CO-45 (exceeds fee schedule) |
| PR | Patient Responsibility | PR-1 (deductible), PR-2 (coinsurance), PR-3 (copay) |
| OA | Other Adjustment | OA-23 (COB) |
| PI | Payer Initiated | PI-97 (plan limitations) |
| CR | Correction/Reversal | CR-104 (correct previous claim) |

---

## Pharmacy Validation (DUR)

### Drug Utilization Review Checks

| Check Type | Code | Description | Action |
|------------|------|-------------|--------|
| Drug-Drug | DD | Interaction between drugs | Warning/Reject |
| Drug-Age | PA | Pediatric/geriatric concern | Warning |
| Drug-Gender | SX | Gender mismatch | Warning |
| Drug-Allergy | DA | Known allergy | Reject |
| Duplicate Therapy | TD | Same drug class | Warning |
| Early Refill | ER | Before 75% days elapsed | Reject |
| Excessive Quantity | MX | Exceeds quantity limit | Reject |
| Drug-Diagnosis | DC | No indication on file | Warning |
| Drug-Pregnancy | PG | Contraindicated in pregnancy | Warning/Reject |
| High Dose | HD | Exceeds max daily dose | Warning |
| Low Dose | LD | Below therapeutic dose | Warning |
| Long Duration | LR | Exceeds max days supply | Warning |

### Common Reject Codes (NCPDP)

| Code | Field | Description |
|------|-------|-------------|
| 01 | - | Missing/Invalid BIN |
| 07 | - | Missing/Invalid Card ID |
| 19 | - | Missing/Invalid Days Supply |
| 25 | - | Missing/Invalid Prescriber ID |
| 70 | - | Product/Service not covered |
| 75 | - | Prior Authorization Required |
| 76 | - | Plan Limitations Exceeded |
| 79 | - | Refill Too Soon |
| 88 | - | DUR Reject Error |

### Step Therapy Validation

```
1. Check if drug requires step therapy
2. Verify patient has claims for step 1 drug
3. Check adequate trial period (typically 30-90 days)
4. If not met: Reject with code 76, message "Step therapy required"
```

### Prior Authorization Validation

```
1. Check if drug requires PA
2. Look up PA by member_id and NDC/GPI
3. Verify PA status = "approved"
4. Verify service_date within PA effective dates
5. If invalid: Reject with code 75
```

### Quantity Limit Validation

| Drug Category | Typical Limit | Period |
|---------------|---------------|--------|
| Controlled II-III | 30 day supply max | Per fill |
| Maintenance drugs | 90 day supply | Per fill (retail), 90 (mail) |
| Specialty drugs | 30 day supply | Per fill |
| Erectile dysfunction | 6-12 units | Per 30 days |
| Migraine triptans | 9-12 units | Per 30 days |

---

## Cross-Entity Validation

### Patient-Member Linkage

When patient is also a member:
- `patient.birth_date == member.birth_date`
- `patient.gender == member.gender`
- `patient.name ~= member.name` (fuzzy match)

### Encounter-Claim Consistency

| Encounter Field | Claim Field | Validation |
|-----------------|-------------|------------|
| period.start | service_date | Match |
| period.end | service_end_date | Match |
| type | claim.type | ambulatory→professional, inpatient→institutional |
| diagnoses | claim.diagnoses | Claim subset of encounter |
| procedures | claim.lines.procedure_code | Codes match |
| provider.npi | rendering_provider.npi | Match |
| place_of_service | place_of_service | Match |

### Prescription-PharmacyClaim Consistency

| Prescription Field | PharmacyClaim Field | Validation |
|--------------------|---------------------|------------|
| id | prescription_id | Reference matches |
| medication.ndc | ndc | Match or therapeutic equivalent |
| quantity | quantity_dispensed | <= prescribed quantity |
| days_supply | days_supply | Match |
| prescriber.npi | prescriber_npi | Match |
| daw_code | daw_code | Match |

### Accumulator Updates

After claim payment:
```
1. Get member accumulators for plan year
2. Add deductible amount to deductible accumulator
3. Add member_responsibility to OOP accumulator
4. Check if limits met
5. Update met_date if newly met
6. Save accumulator state
```

### Validation Severity Levels

| Level | Action | Examples |
|-------|--------|----------|
| ERROR | Reject/fail | Missing required field, invalid format |
| WARNING | Accept with flag | Clinical coherence issue, unusual value |
| INFO | Log only | Near boundary condition |
