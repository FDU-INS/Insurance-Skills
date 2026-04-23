---
name: populationsim-references
description: >
  Reference data for PopulationSim including data source documentation,
  code systems, and lookup tables. Use these references when generating
  accurate population intelligence data.
---

# PopulationSim Reference Data

## Overview

This directory contains reference documentation for the data sources and code systems used by PopulationSim. These references ensure accurate and consistent data generation across all skills.

---

## Reference Files

| File | Content | Primary Use |
|------|---------|-------------|
| [cdc-places-measures.md](cdc-places-measures.md) | 27 CDC PLACES health measures | Health pattern skills |
| [svi-variables.md](svi-variables.md) | 16 SVI variables across 4 themes | SDOH analysis skills |
| [acs-tables.md](acs-tables.md) | Key ACS table references | Demographic skills |
| [fips-codes.md](fips-codes.md) | Geographic identifier structure | All geographic skills |
| [icd10-sdoh-codes.md](icd10-sdoh-codes.md) | SDOH Z-codes | SDOH profile skills |

---

## Data Source Summary

### Primary Sources

| Source | Agency | Content | Geography | Update |
|--------|--------|---------|-----------|--------|
| **CDC PLACES** | CDC | 27 health measures | County, Tract | Annual |
| **CDC SVI** | ATSDR | 16 vulnerability variables | County, Tract | Biennial |
| **Census ACS** | Census | Demographics, economics | All levels | Annual |
| **USDA Food Atlas** | USDA | Food access | Tract | Periodic |
| **ADI** | HRSA/UW | Area deprivation | Block Group | Periodic |

### Supporting Sources

| Source | Content | Use |
|--------|---------|-----|
| NPPES NPI | Provider registry | NetworkSim integration |
| CMS POS | Provider of Services | Facility data |
| HCAHPS | Patient experience | Quality metrics |
| HEDIS | Quality measures | Plan performance |

---

## Geographic Hierarchy

```
Nation
├── Region (4)
│   └── Division (9)
│       └── State (50 + DC + territories)
│           ├── County (3,143)
│           │   ├── Census Tract (~74,000)
│           │   │   └── Block Group (~240,000)
│           │   └── ZIP Code Tabulation Area
│           └── Metro/Micro Area (CBSA)
```

---

## Code System Quick Reference

### Geographic Codes (FIPS)

| Level | Format | Example |
|-------|--------|---------|
| State | 2 digits | 06 (California) |
| County | 5 digits | 06037 (Los Angeles) |
| Tract | 11 digits | 06037201001 |
| Block Group | 12 digits | 060372010011 |
| CBSA | 5 digits | 31080 (Los Angeles MSA) |

### Health Codes

| System | Use | Example |
|--------|-----|---------|
| ICD-10-CM | Diagnoses | E11.9 (Type 2 DM) |
| ICD-10-CM Z | SDOH | Z59.41 (Food insecurity) |
| CPT | Procedures | 99213 (Office visit) |
| LOINC | Labs | 4548-4 (HbA1c) |
| NDC | Medications | 11-digit code |
| NPI | Providers | 10-digit code |

---

## Data Reliability

### CDC PLACES Reliability

| Population | Reliability | Note |
|------------|-------------|------|
| > 50,000 | High | Stable estimates |
| 10,000-50,000 | Moderate | Check confidence intervals |
| < 10,000 | Low | Use county-level data |

### SVI Considerations

| Factor | Impact |
|--------|--------|
| Small population tracts | Higher variance |
| Recent population change | May not reflect current |
| Suppressed variables | Missing components |

---

## Related Skills

All PopulationSim skills reference these data sources:
- [Geographic Skills](../geographic/README.md)
- [Health Pattern Skills](../health-patterns/README.md)
- [SDOH Skills](../sdoh/README.md)
- [Cohort Skills](../cohorts/README.md)
