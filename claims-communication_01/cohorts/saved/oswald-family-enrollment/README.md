# Oswald Family Enrollment Scenario

## Overview

Complete healthcare enrollment scenario for a 5-member family in San Francisco, CA, including initial enrollment, PCP assignments, encounters, claims, and benefit tracking.

## Family Members

| Member | Role | DOB | Age | Member ID | Current PCP |
|--------|------|-----|-----|-----------|-------------|
| Mark Oswald | Subscriber | 1975-06-15 | 49 | AET847291001 | Dr. Joshua Bamberger, MD |
| Karen Oswald | Spouse | 1977-03-22 | 47 | AET847291002 | Dr. Joshua Bamberger, MD |
| Gracie Oswald | Child | 2010-08-03 | 14 | AET847291003 | Dr. Julianne Burns, MD |
| Emmy Oswald | Child | 2014-11-18 | 10 | AET847291004 | Dr. Julianne Burns, MD |
| Miles Oswald | Child | 2020-04-12 | 4 | AET847291005 | Dr. Julianne Burns, MD |

## Health Plan

- **Payer**: Aetna (Payer ID: 60054)
- **Plan**: Aetna Platinum PPO (AET-PPO-PLAT-2025)
- **Group**: 847291
- **Coverage Type**: Family
- **Monthly Premium**: $1,875.00

### Benefits Summary

| Benefit | In-Network |
|---------|------------|
| Deductible | $250 individual / $500 family |
| Out-of-Pocket Max | $2,500 individual / $5,000 family |
| Coinsurance | 10% |
| PCP Copay | $20 |
| Specialist Copay | $40 |
| Preventive Care | 100% covered |

## Primary Care Providers

### Adult PCP (Mark & Karen)

| Field | Value |
|-------|-------|
| Name | Dr. Joshua Bamberger, MD |
| NPI | **1255468245** |
| Specialty | Family Medicine |
| Practice | UCSF Family Medicine - Tenderloin |
| Address | 234 Eddy Street, San Francisco, CA 94102 |
| Phone | 415-353-5095 |
| Effective | April 1, 2025 |

### Pediatrician (Gracie, Emmy, Miles)

| Field | Value |
|-------|-------|
| Name | Dr. Julianne Burns, MD |
| NPI | **1891038006** |
| Specialty | Pediatrics |
| Practice | Sutter Health CPMC Pediatrics |
| Address | 1100 Van Ness Ave FL 7, San Francisco, CA 94109 |
| Phone | 628-336-2220 |
| Effective | April 1, 2025 |

## Transaction History

| Date | Transaction ID | Type | Description |
|------|----------------|------|-------------|
| 2025-01-01 | ENR-2025-0001847 | Initial Enrollment | Open enrollment, family coverage effective |
| 2025-03-15 | ENR-2025-0001848 | PCP Change | All 5 members assigned to new PCPs |

## Files in This Scenario

| File | Description |
|------|-------------|
| `enrollment.json` | Complete enrollment data with current PCPs |
| `enrollment-834.edi` | Initial 834 enrollment transaction |
| `pcp-change-834.edi` | 834 PCP change transaction (March 2025) |
| `encounters.json` | Q1 2025 clinical encounters |
| `claims.json` | Q1 2025 adjudicated claims |
| `sf-health-profile.md` | San Francisco SDOH & health profile analysis |
| `edi-834-explained.md` | 834 segment-by-segment guide |
| `README.md` | This file |

## Accumulators (as of March 8, 2025)

| Member | Deductible Used | OOP Used |
|--------|-----------------|----------|
| Family Total | $0 / $500 | $121.30 / $5,000 |
| Mark | $0 / $250 | $60.30 / $2,500 |
| Karen | $0 / $250 | $0 / $2,500 |
| Gracie | $0 / $250 | $0 / $2,500 |
| Emmy | $0 / $250 | $61.00 / $2,500 |
| Miles | $0 / $250 | $0 / $2,500 |

## Location Context

**Address**: 1234 Oak Street, San Francisco, CA 94102 (Civic Center)

See `sf-health-profile.md` for:
- CDC PLACES health indicators
- Social Vulnerability Index (SVI) data
- SDOH factors
- Family demographic mapping

## Provider Data Source

PCP information sourced from **CMS NPPES NPI Registry** (real providers, real NPIs).

---

*Last Updated: March 15, 2025*
*HealthSim Scenario Version: 2.0*
