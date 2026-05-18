# PopulationSim

> Query real CDC/Census population data and generate evidence-based cohort specifications grounded in actual disease prevalence, demographics, and social determinants of health.

## What PopulationSim Does

PopulationSim is the **population intelligence** engine of HealthSim. Unlike other products that generate synthetic data, PopulationSim v2.0 provides **access to real embedded data**—148 MB of CDC PLACES, SVI, and ADI data covering every US county, tract, and block group.

This data grounds all HealthSim products in reality. When you generate diabetic patients in Harris County, TX, they reflect the actual 12.1% prevalence rate, not a generic national average.

## Quick Start

**Data lookup:**
```
What is the diabetes prevalence in Harris County, TX?
Show me SVI vulnerability scores for Cook County, IL
```

**Geographic profiles:**
```
Profile San Diego County health indicators
Compare chronic disease rates across California counties
```

**Cohort specification:**
```
Generate a cohort specification for 1,000 Type 2 diabetics in Phoenix metro
Define a heart failure population for Harris County with real prevalence
```

See [hello-healthsim examples](../../hello-healthsim/examples/populationsim-examples.md) for detailed examples with expected outputs.

## Key Capabilities

| Capability | Description | Skill Reference |
|------------|-------------|-----------------|
| **Data Lookup** | Query embedded CDC/Census data | [data-access/data-lookup.md](data-access/data-lookup.md) |
| **Geographic Profiles** | County, tract, metro area analysis | [geographic/](geographic/) |
| **Health Patterns** | Chronic disease prevalence, behaviors | [health-patterns/](health-patterns/) |
| **SDOH Analysis** | SVI, ADI, economic indicators | [sdoh/](sdoh/) |
| **Cohort Specification** | Evidence-based population definitions | [cohorts/](cohorts/) |
| **Trial Support** | Feasibility, site selection, diversity | [trial-support/](trial-support/) |

## Embedded Data Package (v2.0)

| Source | Coverage | Records | Key Measures |
|--------|----------|---------|--------------|
| CDC PLACES 2024 | 100% US counties + tracts | 86,665 | 40 health measures (diabetes, obesity, COPD, etc.) |
| CDC SVI 2022 | 100% US counties + tracts | 87,264 | 16 vulnerability indicators |
| HRSA ADI 2023 | 100% US block groups | 242,336 | Area deprivation index |

**Total**: 148 MB embedded data, 416,265 geographic records

## "I Want To..." Quick Reference

| Goal | Skill | Example |
|------|-------|---------|
| Look up a health rate | [data-lookup.md](data-access/data-lookup.md) | "Diabetes rate in FIPS 48201" |
| Profile a county | [county-profile.md](geographic/county-profile.md) | "Profile Harris County, TX" |
| Analyze vulnerability | [svi-analysis.md](sdoh/svi-analysis.md) | "SVI themes for Cook County" |
| Build a cohort | [cohort-specification.md](cohorts/cohort-specification.md) | "1,000 diabetics in Phoenix" |
| Estimate trial feasibility | [feasibility-estimation.md](trial-support/feasibility-estimation.md) | "NASH trial feasibility in CA" |
| Select trial sites | [site-selection-support.md](trial-support/site-selection-support.md) | "Top 5 counties for diabetes trial" |

## Cross-Product Integration

PopulationSim data flows into all other HealthSim products:

| Product | Integration | What It Enables |
|---------|-------------|-----------------|
| **PatientSim** | Demographics, prevalence | Patients with real disease rates for their geography |
| **MemberSim** | Utilization, risk | Actuarially realistic member panels |
| **RxMemberSim** | Adherence, SDOH | Medication patterns reflecting SVI vulnerability |
| **TrialSim** | Feasibility, diversity | Evidence-based site selection and enrollment |

**Example Data Flow:**
```
Request: "Generate 50 diabetic patients for Harris County, TX"

PopulationSim provides:
  - 12.1% diabetes prevalence (CDC PLACES)
  - 72% minority population (SVI demographics)
  - 0.68 vulnerability score (SVI)
  
PatientSim applies:
  - 12.1% diabetes (not generic 10%)
  - Higher comorbidity rates (obesity, HTN)
  - SDOH factors in social history
```

## Output Types

| Output | Description | Use Case |
|--------|-------------|----------|
| Data Response | Raw values with provenance | Ad-hoc queries |
| Geographic Profile | Comprehensive area summary | Research, planning |
| CohortSpecification | Structured population definition | Feeding other products |
| Comparison Report | Multi-geography analysis | Site selection, feasibility |

## Skills Reference

For complete generation parameters, examples, and validation rules, see:

- **[SKILL.md](SKILL.md)** - Full skill reference with all capabilities
- **[data/README.md](data/README.md)** - Data package documentation
- **[../../SKILL.md](../../SKILL.md)** - Master skill file (cross-product routing)

## Related Documentation

- [hello-healthsim PopulationSim Examples](../../hello-healthsim/examples/populationsim-examples.md)
- [Data Integration Guide](../patientsim/data-integration.md)
- [Cross-Product Integration Guide](../../docs/HEALTHSIM-ARCHITECTURE-GUIDE.md#93-cross-product-integration)

---

*PopulationSim provides real population statistics for synthetic data generation. Data is from public CDC/Census sources.*
