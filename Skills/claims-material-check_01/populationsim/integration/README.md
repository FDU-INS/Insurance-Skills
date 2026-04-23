# PopulationSim Integration Guide

## Overview

PopulationSim serves as the demographic and SDOH foundation layer for the entire HealthSim ecosystem. This directory contains documentation for integrating PopulationSim with downstream products.

---

## Integration Documents

| Document | Description |
|----------|-------------|
| [Cross-Product Integration](cross-product-integration.md) | Architecture overview, data flow patterns, identity correlation |
| [PatientSim Integration](patientsim-integration.md) | Demographic and SDOH mapping to clinical data |
| [MemberSim Integration](membersim-integration.md) | Insurance, enrollment, and claims generation |
| [TrialSim Integration](trialsim-integration.md) | Feasibility, diversity planning, enrollment simulation |

---

## Integration Principles

### 1. PopulationSim First

Always start workflows with PopulationSim to establish:
- Geographic context
- Demographic distributions
- Health indicator prevalence
- SDOH characteristics

### 2. Identity Correlation

SSN serves as the universal correlator across all products:

```
Person (SSN: 123-45-6789)
├── PatientSim: MRN-000001
├── MemberSim: MEM-567890
├── RxMemberSim: RX-567890
└── TrialSim: SUBJ-001
```

### 3. Consistent Geography

Use the same geographic identifiers across products:
- FIPS codes for precise location
- CBSA codes for metropolitan areas
- Tract-level for fine-grained analysis

### 4. SDOH Alignment

Ensure SDOH characteristics flow consistently:
- PopulationSim → Z-code rates
- PatientSim → Encounter diagnoses
- MemberSim → Risk adjustment
- TrialSim → Retention modeling

---

## Quick Start

### Generate Cross-Product Cohort

```
User: Generate a cohort of 1,000 diabetic patients in Harris County 
      with high SDOH vulnerability. Include clinical records, 
      insurance enrollment, and pharmacy claims.

Claude: [Uses PopulationSim skills to create PopulationProfile]
        [Defines CohortSpecification with SDOH requirements]
        [Generates PatientSim patients with FHIR resources]
        [Creates MemberSim enrollments and claims]
        [Produces RxMemberSim pharmacy claims]
        [Returns correlated data bundle]
```

### Assess Trial Feasibility

```
User: Assess feasibility for a Type 2 diabetes cardiovascular outcomes 
      trial with sites in Houston, Dallas, and San Antonio. 
      Target 500 subjects with 40% minority enrollment.

Claude: [Analyzes catchment areas with PopulationSim]
        [Calculates eligible population per site]
        [Projects diversity achievement]
        [Models retention with SDOH factors]
        [Returns feasibility report]
```

---

## Related Documentation

- [PopulationSim SKILL.md](../SKILL.md) - Main PopulationSim skill
- [Model Schemas](../../../references/populationsim-models/) - Data model definitions
- [Reference Data](../../../references/) - Code systems and methodologies
