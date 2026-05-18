# Generation Patterns Reference

Standard patterns for generating realistic synthetic healthcare data with reproducibility.

## Table of Contents

- [Identifier Generation](#identifier-generation)
- [Demographic Distributions](#demographic-distributions)
- [Temporal Patterns](#temporal-patterns)
- [Seed Management](#seed-management)
- [Batch Generation](#batch-generation)
- [Realistic Variance](#realistic-variance)

---

## Identifier Generation

### Pattern Formats

| Identifier | Format | Example | Algorithm |
|------------|--------|---------|-----------|
| MRN | `MRN` + 8 digits | MRN00001234 | Sequential with zero-pad |
| Member ID | 9-12 alphanumeric | ABC123456789 | Random + check digit |
| Claim ID | `CLM` + 12 digits | CLM000000001234 | Sequential |
| Prescription ID | `RX` + 10 digits | RX0000001234 | Sequential |
| Encounter ID | `ENC` + 10 digits | ENC0000001234 | Sequential |
| NPI | 10 digits | 1234567893 | Random + Luhn checksum |
| DEA | 2 letters + 7 digits | AB1234563 | Prefix + random + check |
| NCPDP ID | 7 digits | 1234567 | Random |
| SSN | XXX-XX-XXXX | 123-45-6789 | Random (900-999 for synthetic) |
| Tax ID | XX-XXXXXXX | 12-3456789 | Random |

### NPI Generation Algorithm

```
1. Generate 9 random digits
2. Prefix with "80840" (healthcare identifier)
3. Calculate Luhn checksum:
   a. Double every other digit from right
   b. If doubled digit > 9, subtract 9
   c. Sum all digits
   d. Check digit = (10 - (sum mod 10)) mod 10
4. Append check digit to 9 digits
5. Return 10-digit NPI
```

### Member ID Generation

```
1. Generate prefix based on payer (3 chars)
2. Generate 6-9 random alphanumeric
3. Calculate mod-10 check digit
4. Format: {PREFIX}{RANDOM}{CHECK}
```

### Unique ID Guarantees

- **Sequential IDs**: Use atomic counter, thread-safe
- **Random IDs**: Check uniqueness against generated set
- **Scoped uniqueness**: MRNs unique per facility, member IDs per payer

---

## Demographic Distributions

### Age Distributions

**Default (General Population)**

| Age Range | Weight | Notes |
|-----------|--------|-------|
| 0-4 | 6% | Infants/toddlers |
| 5-17 | 16% | Pediatric |
| 18-29 | 16% | Young adult |
| 30-44 | 20% | Adult |
| 45-64 | 26% | Middle age |
| 65-74 | 10% | Young elderly |
| 75+ | 6% | Elderly |

**Pediatric Focus**

| Age Range | Weight |
|-----------|--------|
| 0-1 | 15% |
| 1-4 | 25% |
| 5-12 | 35% |
| 13-17 | 25% |

**Geriatric Focus**

| Age Range | Weight |
|-----------|--------|
| 65-69 | 25% |
| 70-74 | 25% |
| 75-79 | 20% |
| 80-84 | 15% |
| 85+ | 15% |

**Working Age (Commercial Insurance)**

| Age Range | Weight |
|-----------|--------|
| 18-25 | 15% |
| 26-35 | 25% |
| 36-45 | 25% |
| 46-55 | 20% |
| 56-64 | 15% |

### Gender Distribution

| Gender | Default | Notes |
|--------|---------|-------|
| male | 49% | Biological male |
| female | 50% | Biological female |
| other | 0.5% | Non-binary/other |
| unknown | 0.5% | Not recorded |

### Geographic Distribution (US States)

| Region | States | Weight |
|--------|--------|--------|
| Northeast | NY, PA, NJ, MA, CT, etc. | 17% |
| Southeast | FL, GA, NC, VA, TN, etc. | 25% |
| Midwest | IL, OH, MI, IN, WI, etc. | 21% |
| Southwest | TX, AZ, NM, OK | 14% |
| West | CA, WA, OR, CO, etc. | 23% |

### Race/Ethnicity Distribution

| Race | Weight |
|------|--------|
| white | 60% |
| black | 13% |
| asian | 6% |
| native | 1% |
| pacific | 0.5% |
| other | 7% |
| unknown | 12.5% |

| Ethnicity | Weight |
|-----------|--------|
| non-hispanic | 81% |
| hispanic | 19% |

### Insurance Plan Distribution

| Plan Type | Commercial | Medicare | Medicaid |
|-----------|------------|----------|----------|
| HMO | 25% | 35% | 60% |
| PPO | 55% | 40% | 20% |
| EPO | 10% | - | - |
| POS | 5% | - | - |
| HDHP | 5% | - | - |
| Traditional | - | 25% | 20% |

---

## Temporal Patterns

### Date Generation

**Historical Range**

```
For clinical data: generate within last 3 years
For claims: generate within last 2 years
For prescriptions: generate within last 1 year
```

**Date Sequence Generation**

```
1. Generate anchor date (enrollment, first encounter)
2. Generate subsequent dates relative to anchor
3. Apply minimum intervals (e.g., 1 day between visits)
4. Apply maximum gaps (e.g., no more than 6 months without visit for chronic conditions)
```

### Encounter Frequency Patterns

**Well Patients**

| Age Group | Visits/Year | Pattern |
|-----------|-------------|---------|
| 0-2 | 8-12 | Well child checks |
| 2-18 | 1-2 | Annual + sick |
| 18-64 | 1-3 | Annual + sick |
| 65+ | 3-6 | Quarterly + sick |

**Chronic Conditions**

| Condition | Visits/Year | Lab Frequency |
|-----------|-------------|---------------|
| Diabetes | 4-6 | A1C quarterly |
| Hypertension | 2-4 | Labs annually |
| CHF | 4-8 | Labs quarterly |
| COPD | 3-6 | Spirometry annually |
| CKD Stage 3+ | 4-6 | Labs quarterly |

### Prescription Refill Patterns

| Medication Type | Days Supply | Refills | Adherence |
|-----------------|-------------|---------|-----------|
| Acute | 7-14 days | 0-1 | Single fill |
| Maintenance | 30 days retail | 3-11 | Monthly |
| Maintenance | 90 days mail | 1-3 | Quarterly |
| Controlled | 30 days max | 0 (II), 5 (III-V) | Monthly |

### Claim Processing Timelines

| Stage | Days from Service |
|-------|-------------------|
| Claim submission | 0-30 days |
| Claim received | 1-45 days |
| Adjudication | 1-14 days |
| Payment | 14-45 days |
| EOB to member | 14-60 days |

---

## Seed Management

### Reproducibility

Use explicit seeds for deterministic generation:

```
seed = hash(base_seed + entity_type + sequence_number)
```

### Seed Usage

| Component | Seed Application |
|-----------|------------------|
| Names | seed determines first/last name selection |
| DOB | seed determines year, month, day |
| Gender | seed determines male/female/other |
| Address | seed determines state, city, ZIP |
| Conditions | seed determines which diagnoses |
| Encounters | seed determines timing, types |
| Labs | seed determines values within ranges |

### Seed Chaining

```
Patient Seed → Demographics Seed → Encounter Seeds → Lab Seeds
                                → Prescription Seeds → Fill Seeds
                                → Claim Seeds
```

### Cross-Entity Consistency

Same seed should produce:
- Same patient demographics
- Consistent clinical narrative
- Matching claim data

---

## Batch Generation

### Batch Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| count | Number of entities | 1 |
| seed | Base seed for batch | Random |
| start_id | Starting sequence number | 1 |
| include_related | Generate related entities | true |
| date_range | Temporal bounds | Last 2 years |

### Batch Structure

```
Batch Generation:
├── Generate N patients
│   ├── For each patient:
│   │   ├── Demographics (seeded)
│   │   ├── Conditions (based on age/demographics)
│   │   ├── Encounters (frequency per conditions)
│   │   │   ├── Diagnoses
│   │   │   ├── Procedures
│   │   │   ├── Labs
│   │   │   └── Vitals
│   │   ├── Prescriptions (per diagnoses)
│   │   └── Insurance claims (per encounters)
└── Return batch with relationships
```

### Parallelization

- Patients can be generated in parallel with different seeds
- Related entities within a patient are sequential
- Unique IDs require synchronization

---

## Realistic Variance

### Value Distributions

**Numeric Values (Normal Distribution)**

```
value = mean + (random_normal() * std_dev)
clamp(value, min, max)
```

**Lab Values with Clinical Context**

| Scenario | A1c Mean | A1c StdDev |
|----------|----------|------------|
| Well-controlled DM | 6.5 | 0.5 |
| Uncontrolled DM | 9.0 | 1.5 |
| Non-diabetic | 5.2 | 0.3 |

**Charges (Log-Normal Distribution)**

```
charge = exp(log_mean + random_normal() * log_std_dev)
round_to_cents(charge)
```

### Clinical Progression

**Improving Patient (e.g., new diabetes treatment)**

```
A1c Timeline:
  Month 0: 9.5 (baseline)
  Month 3: 8.5 (-1.0)
  Month 6: 7.5 (-0.5)
  Month 9: 7.0 (-0.5)
  Month 12: 6.8 (stable)
```

**Deteriorating Patient (e.g., progressing CKD)**

```
eGFR Timeline:
  Year 0: 55 (Stage 3a)
  Year 1: 48 (Stage 3b)
  Year 2: 38 (Stage 3b)
  Year 3: 28 (Stage 4)
```

### Name Generation

Use weighted lists by ethnicity:

| Ethnicity | First Names Pool | Last Names Pool |
|-----------|------------------|-----------------|
| White | John, James, Michael... | Smith, Johnson, Williams... |
| Hispanic | José, Maria, Carlos... | Garcia, Rodriguez, Martinez... |
| Black | Jamal, Aaliyah, Deshawn... | Jackson, Washington, Jefferson... |
| Asian | Wei, Yuki, Raj... | Chen, Kim, Patel... |

### Address Generation

```
1. Select state (weighted by population)
2. Select city within state (weighted by population)
3. Generate street number (1-9999)
4. Select street name from pool
5. Select street type (St, Ave, Blvd, Dr)
6. Generate ZIP code (valid for city)
```

### Provider Generation

```
NPI Pool by Specialty:
- Primary Care: 500 NPIs
- Cardiology: 200 NPIs
- Endocrinology: 100 NPIs
- Emergency: 300 NPIs

Assign based on encounter type and patient conditions.
```

---

## Error Injection (Optional)

For testing error handling, optionally inject:

| Error Type | Rate | Example |
|------------|------|---------|
| Missing required field | 1% | No member_id |
| Invalid code | 0.5% | Invalid ICD-10 |
| Date out of range | 0.5% | Future service date |
| Duplicate claim | 0.1% | Same claim twice |
| Clinical mismatch | 1% | Male with pregnancy |

Enable with `include_errors: true` parameter.
