---
name: generation
description: Conversation-driven specification and execution of healthcare data generation at scale. Use when building profiles, generating cohorts, creating journeys, batch generation, specifying distributions, or any at-scale data generation task.
---

# Generative Framework Skills

Use these skills when building specifications for data generation or executing batch generation.

## Quick Reference

| Skill | Use When | Location |
|-------|----------|----------|
| **Profile Builder** | Defining population characteristics for batch generation | [builders/profile-builder.md](builders/profile-builder.md) |
| **Journey Builder** | Defining temporal event sequences | [builders/journey-builder.md](builders/journey-builder.md) |
| **Quick Generate** | Simple single-entity generation | [builders/quick-generate.md](builders/quick-generate.md) |
| **Profile Executor** | Executing a profile specification | [executors/profile-executor.md](executors/profile-executor.md) |
| **Journey Executor** | Executing a journey specification | [executors/journey-executor.md](executors/journey-executor.md) |
| **Cross-Domain Sync** | Coordinating cross-product generation | [executors/cross-domain-sync.md](executors/cross-domain-sync.md) |

## Trigger Phrases

### Building Specifications

- "Build a profile for 100 Medicare members"
- "Create a journey for diabetic patients"
- "Specify a commercial cohort with CHF"
- "Define a surgical episode journey"

### Executing Specifications

- "Generate patients from this profile"
- "Execute the diabetic journey for 50 patients"
- "Run batch generation for this cohort"

### Using Templates

- "Use the Medicare diabetic template"
- "Start with the surgical episode journey"
- "Generate using the commercial healthy profile"

## Workflow Overview

### 1. Build a Profile (Optional)

```json
{
  "profile": {
    "generation": { "count": 200, "products": ["patientsim", "membersim"] },
    "demographics": {
      "age": { "type": "normal", "mean": 74, "std": 6, "min": 65, "max": 85 },
      "gender": { "type": "categorical", "weights": { "M": 0.48, "F": 0.52 } },
      "geography": { "county_fips": "06073" }
    },
    "clinical": {
      "primary_condition": { "code": "E11.9", "prevalence": 0.40 },
      "comorbidities": [{ "code": "I50.9", "prevalence": 0.30 }]
    }
  }
}
```

### 2. Build a Journey (Optional)

```
Create a first-year diabetic journey:
- Initial diagnosis visit with labs
- Metformin prescription
- Quarterly follow-ups with A1c
- Possible titration to second agent
```

### 3. Execute Generation

```
Generate the cohort using this profile and journey
Save as cohort "ma-diabetic-cohort-2025"
```

## Distribution Types

| Type | Use Case | Example |
|------|----------|---------|
| `categorical` | Discrete choices | Gender: M/F/Other |
| `normal` | Bell curve | Age centered at 72 |
| `log_normal` | Skewed positive | Healthcare costs |
| `uniform` | Equal probability | Random day in range |
| `explicit` | Specific values | Exactly these NDCs |

See [distributions/distribution-types.md](distributions/distribution-types.md) for details.

### Statistical Fidelity — Matching Real Populations

Generated cohorts should use statistical distributions that match real-world population characteristics. The goal is realistic synthetic data, not random noise.

**How to match a target population:**

1. **Identify the source benchmark.** For Medicare Advantage, use CMS enrollment statistics (mean age ~72, 55% female, regional mix). For Commercial, use employer-census norms. For Medicaid, use state-level demographics.
2. **Select distribution types that fit the data shape.** Age in MA populations follows a roughly normal distribution centered near 72-74 with standard deviation ~7. Cost distributions are log-normal (many low-cost, few high-cost). Chronic condition prevalence uses categorical distributions with rates from CDC PLACES or CMS Chronic Conditions data.
3. **Parameterize from published statistics.** Do not guess distribution parameters. Use published prevalence rates (e.g., 27% diabetes in Medicare, 14% heart failure) and demographic breakdowns. PopulationSim data (`skills/populationsim/`) provides county- and tract-level benchmarks for prevalence and social determinants.
4. **Validate output against inputs.** After generation, confirm the cohort's statistical profile (mean, median, standard deviation, category proportions) matches the specification within an acceptable tolerance. Flag drift greater than 5% from target parameters.

## Journey Patterns

| Pattern | Use Case | Example |
|---------|----------|---------|
| `linear` | Simple sequence | Office visit → Lab → Follow-up |
| `branching` | Decision points | ER → Admit OR Discharge |
| `protocol` | Trial schedules | Cycle 1 Day 1, Day 8, Day 15 |
| `lifecycle` | Long-term patterns | New member first year |

See the [journeys/](journeys/) folder for pattern details.

## Integration with Products

The Generative Framework orchestrates all HealthSim products:

| When Generating | Products Involved | Cross-Domain Triggers |
|-----------------|-------------------|----------------------|
| Patient cohort | PatientSim, NetworkSim | Provider assignment |
| Member claims | MemberSim, PatientSim, NetworkSim | Encounter → Claim |
| Pharmacy fills | RxMemberSim, PatientSim, NetworkSim | Rx → Fill, DUR check |
| Trial subjects | TrialSim, PatientSim, NetworkSim | Subject ↔ Patient linking |

## Templates

Pre-built profiles and journeys for common use cases:

### Profile Templates

- [medicare-diabetic.md](templates/profiles/medicare-diabetic.md) - Medicare T2DM cohort
- [commercial-healthy.md](templates/profiles/commercial-healthy.md) - Commercial healthy adults
- [medicaid-pediatric.md](templates/profiles/medicaid-pediatric.md) - Medicaid children

### Journey Templates

- [diabetic-first-year.md](templates/journeys/diabetic-first-year.md) - New T2DM diagnosis year 1
- [surgical-episode.md](templates/journeys/surgical-episode.md) - Elective surgery episode
- [new-member-onboarding.md](templates/journeys/new-member-onboarding.md) - New member first 90 days

## Safety Guardrails

**All generated data is synthetic and fictional.** HealthSim produces simulated test data only. Never present generated records as real patient data.

- **No clinical advice.** Generated data must not be used to make prescribing decisions, diagnoses, or treatment recommendations. If asked, remind the user this is synthetic test data, not real clinical information.
- **Real codes, synthetic entities.** Use real, valid medical code systems for realism (see below), but all patients, members, encounters, and claims are generated/fictional.
- **No real PHI.** Never pull from or reference real patient databases. All person-level data is simulated.

### Standard Code Systems

Generated data should reference recognized healthcare code systems:

| System | Use |
|--------|-----|
| **ICD-10** | Diagnosis codes |
| **CPT / HCPCS** | Procedure codes |
| **LOINC** | Lab / observation codes |
| **RxNorm / NDC** | Medication identifiers |
| **SNOMED CT** | Clinical terminology |
| **NPI** | Provider identifiers |

Real reference data (NPI registry, CMS facility files, published code sets) is safe to use. Synthetic data is generated for all patient/member-level entities.

## Edge Cases and Error Handling

When generating data, handle incomplete or invalid inputs gracefully:

### Missing or Partial Input

| Situation | How to Handle |
|-----------|---------------|
| No age range specified | Default to plan-appropriate range (Medicare: 65-95, Commercial: 18-64, Medicaid Pediatric: 0-18) |
| No geography specified | Omit geographic constraints; generate nationally representative distribution |
| Missing condition prevalence | Use published population baselines (e.g., CDC PLACES prevalence rates) |
| Incomplete journey steps | Generate the specified steps; warn the user about gaps rather than inventing steps silently |
| Unknown or invalid ICD-10/CPT code | Reject the code and ask the user to verify; never silently substitute a different code |

### What NOT to Generate

These are common mistakes to avoid:

- **Do NOT invent code systems.** Use only recognized systems (ICD-10, CPT, HCPCS, LOINC, RxNorm, NDC, SNOMED CT, NPI). Never fabricate codes that look plausible but do not exist in the standard.
- **Do NOT generate clinically impossible combinations.** Example: a 5-year-old with Medicare Fee-for-Service, or a pregnancy diagnosis on a male patient. Cross-check age, sex, and plan type against clinical plausibility.
- **Do NOT silently drop requested attributes.** If the user asks for 10 fields and only 8 can be generated, surface the gap explicitly rather than returning incomplete records without explanation.
- **Do NOT extrapolate beyond the specification.** If the user asks for "50 patients with diabetes," generate exactly 50 with diabetes -- do not add additional unrequested conditions for "realism" unless the user has opted into realistic comorbidity modeling.
- **Do NOT generate duplicate identifiers.** Every patient ID, member ID, encounter ID, and claim ID must be unique within a cohort.

### Validation Checklist

Before returning generated data, verify:

1. All code values exist in their respective standard (ICD-10, CPT, LOINC, etc.)
2. Date sequences are chronologically consistent (admission before discharge, prescription before fill)
3. Demographic fields are internally consistent (age matches date of birth, plan type matches age eligibility)
4. Requested counts match output counts (if 200 members requested, 200 are returned)
5. No duplicate identifiers exist across the generated dataset

## Related Skills

- **[State Management](../common/state-management.md)** - Save/load generated cohorts
- **[Identity Correlation](../common/identity-correlation.md)** - Cross-product entity linking
- **[PopulationSim](../populationsim/SKILL.md)** - Real-world demographic data
- **[NetworkSim](../networksim/SKILL.md)** - Real provider assignments

---

*Implementation Status: Foundation phase. See [GENERATIVE-FRAMEWORK-PROGRESS.md](../../docs/GENERATIVE-FRAMEWORK-PROGRESS.md) for details.*
