---
name: insurance-domain
description: "Use when modifying domain/models/, domain/services/, adaptor/llm/, or any business logic involving insurance terms, coverages, or risk rules. Also use when adding new fields, endorsements, or coverage types."
---

# Insurance Domain Knowledge (ACORD-Based)

ACORD (Association for Cooperation in Operations Research and Development) defines the insurance industry's data standards. This project covers Personal Lines — Auto (ACORD 90) and Homeowners (ACORD 80).

## Core Terminology

| Term | Definition | ACORD Context |
|------|-----------|---------------|
| **Renewal** | Policy renewal. Comparing Prior vs Renewal is the core workflow | ACORD 80/90 Status: `Renew` |
| **Endorsement** | Mid-term policy change or rider. Expands/restricts coverage scope | ACORD 70 (HO), 71 (Auto): change type A/C/D |
| **Premium** | Insurance premium. Rate of change at renewal is the primary risk indicator | ACORD `WrittenAmt` |
| **Deductible** | Amount the insured pays first before a claim is covered | ACORD `DeductibleAmt` |
| **Liability Limit** | Liability cap. A protected field that must never be auto-reduced | ACORD `BI`, `PD`, Coverage E |
| **Coverage Dropped** | Coverage item removed. Flagged when True→False or amount decreases | DiffFlag.COVERAGE_DROPPED |
| **Material Change** | A change with substantial impact on coverage scope | LLM endorsement_comparison target |
| **Risk Signal** | Risk factors extracted from renewal notes (claims history, property condition, etc.) | LLM risk_signal_extractor output |
| **Bundle** | Auto + Home package for the same customer. Discount eligible; risk when unbundled | Core concept in Portfolio analysis |
| **SR-22** | High-risk driver certificate. Minimum insurance proof required by the state | ACORD Driver field |

## Coverage Types (ACORD Code Mapping)

### Auto Coverages

| ACORD Code | Name | Current Model Field | Notes |
|-----------|------|---------------------|-------|
| `BI` | Bodily Injury | `bodily_injury_limit` | split limit "100/300" |
| `PD` | Property Damage | `property_damage_limit` | |
| `COLL` | Collision | `collision_deductible` | |
| `COMP` | Comprehensive | `comprehensive_deductible` | |
| `UM` | Uninsured Motorist | `uninsured_motorist` | |
| `MEDPM` | Medical Payments | `medical_payments` | |
| `TL` | Towing/Roadside | `roadside_assistance` | bool only — ACORD uses amount |
| `RENTAL` | Rental Reimbursement | `rental_reimbursement` | bool only — ACORD uses daily/max limit |
| `UNDUM` | Underinsured Motorist | **not implemented** | separate from UM, required in many states |
| `PIP` | Personal Injury Protection | **not implemented** | required in no-fault states |
| `UMPD` | UM Property Damage | **not implemented** | separate coverage in some states |

### Home Coverages

| ACORD Code | Name | Current Model Field | Notes |
|-----------|------|---------------------|-------|
| `DWELL` | Coverage A (Dwelling) | `coverage_a_dwelling` | protected field |
| `OTSTR` | Coverage B (Other Structures) | `coverage_b_other_structures` | typically 10% of A |
| `PP` | Coverage C (Personal Property) | `coverage_c_personal_property` | |
| `ALE` | Coverage D (Loss of Use) | `coverage_d_loss_of_use` | |
| `PL` | Coverage E (Liability) | `coverage_e_liability` | protected field |
| `MEDPM` | Coverage F (Medical) | `coverage_f_medical` | |
| `WIND` | Wind/Hail | `wind_hail_deductible` | deductible only |
| — | Water Backup | `water_backup` | bool only — ACORD uses limit amount |
| `EQ` | Earthquake | **not implemented** | near-mandatory in CA/WA/OR |
| `FLOOD` | Flood | **not implemented** | separate NFIP policy |

## ACORD Gap Analysis — Known Limitations of Current Models

### High Priority (Directly impacts renewal review)

1. **UIM/PIP/UMPD not implemented** — Cannot compare state-required coverages
2. **No amounts on boolean coverages** — Cannot compare limits for rental($30/day), roadside($75/occ), water_backup($5K), etc.
3. **No Loss History** — ACORD 80/90 Prior Loss section. Key factor in renewal premium determination
4. **No HO Form Type** — HO-3(broad), HO-5(open), HO-6(condo), etc. Fundamentally different coverage scopes
5. **No Territory Code** — Basic variable in premium calculation

### Medium Priority (Improves analysis precision)

6. **Driver DOB** — ACORD standard uses DOB instead of age. Enables exact age calculation
7. **Vehicle annual mileage** — `EstimatedAnnualDistance`. Major premium factor
8. **Driver relationship/marital status** — `RelationshipToInsured`, `MaritalStatus`. Discount factors
9. **Endorsement limit/deductible** — Cannot compare endorsement coverage limits
10. **Prior Carrier** — ACORD 80 Prior Coverage section. Renewal context

## Protected Fields — Never auto-modify

Per ACORD standards, reducing these fields carries legal/contractual risk:

- `bodily_injury_limit` — Bodily injury liability limit
- `property_damage_limit` — Property damage liability limit
- `uninsured_motorist` — Uninsured motorist coverage
- `coverage_a_dwelling` — Dwelling reconstruction cost
- `coverage_e_liability` — Personal liability

## Endorsement Form System

ACORD uses a Form Number system rather than a single code list:

- **Auto**: PP series (PP 03 06, PP 03 22, PP 03 23, etc.)
- **Home**: HO series (HO 04 10, HO 04 61, HO 04 90, HO 04 95, etc.)
- **Change Request**: ACORD 70 (HO), ACORD 71 (Auto) — type A(Add)/C(Change)/D(Delete)

Currently `Endorsement.code` is free text. Validation can be added when ISO/AAIS form number mapping is implemented.

## Application Rules

1. **When adding new coverage fields**: Reference the ACORD code mapping tables above for naming
2. **When adding DiffFlags**: Consider the industry importance of the coverage (liability types → URGENT)
3. **When modifying LLM prompts**: Verify the exact meaning of insurance terms before use
4. **When adding Quote strategies**: Re-verify the protected fields list. Protected fields cannot be changed in any strategy
