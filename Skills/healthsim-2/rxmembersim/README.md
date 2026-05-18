# RxMemberSim

> Generate realistic pharmacy data including prescription fills, DUR alerts, formulary management, and manufacturer copay programs.

## What RxMemberSim Does

RxMemberSim is the **pharmacy and PBM data** engine of HealthSim. It creates synthetic pharmacy claims that flow through realistic adjudication—checking formulary coverage, applying tier copays, generating DUR alerts for drug interactions, and modeling manufacturer assistance programs.

Whether you need a simple generic fill, a rejected specialty drug requiring PA, or a complex drug-drug interaction alert, RxMemberSim generates data that matches real PBM processing.

## Quick Start

**Simple:**
```
Generate a pharmacy claim for atorvastatin
Generate an RxMember with pharmacy coverage
```

**With alerts/rejections:**
```
Generate a drug-drug interaction alert for warfarin and aspirin
Generate a rejected claim for Eliquis requiring prior auth
```

**With manufacturer programs:**
```
Generate a specialty pharmacy claim with manufacturer copay card
```

See [hello-healthsim examples](../../hello-healthsim/examples/rxmembersim-examples.md) for detailed examples with expected outputs.

## Key Capabilities

| Capability | Description | Skill Reference |
|------------|-------------|-----------------|
| **Retail Pharmacy** | Standard fills with copays, refills | [retail-pharmacy.md](retail-pharmacy.md) |
| **Specialty Pharmacy** | Biologics, limited distribution, hub model | [specialty-pharmacy.md](specialty-pharmacy.md) |
| **DUR Alerts** | Drug interactions, early refills, therapeutic dup | [dur-alerts.md](dur-alerts.md) |
| **Formulary** | Tiers, coverage status, PA requirements | [formulary-management.md](formulary-management.md) |
| **Rx Prior Auth** | Step therapy, formulary exceptions | [rx-prior-auth.md](rx-prior-auth.md) |
| **Accumulators** | Rx deductible, TrOOP, Part D phases | [rx-accumulator.md](rx-accumulator.md) |
| **Manufacturer Programs** | Copay cards, PAPs, hub programs | [manufacturer-programs.md](manufacturer-programs.md) |

## Pharmacy Cohorts

| Cohort | Key Elements | Skill |
|----------|--------------|-------|
| Retail Fills | Generic/brand, copays, refills | [retail-pharmacy.md](retail-pharmacy.md) |
| Specialty Drugs | Limited distribution, prior auth, hub enrollment | [specialty-pharmacy.md](specialty-pharmacy.md) |
| Drug Interactions | DDI severity, override codes | [dur-alerts.md](dur-alerts.md) |
| Early Refill | Percent supply used, vacation override | [dur-alerts.md](dur-alerts.md) |
| Step Therapy | Required drugs tried first | [rx-prior-auth.md](rx-prior-auth.md) |
| Copay Assistance | Manufacturer cards, annual maximums | [manufacturer-programs.md](manufacturer-programs.md) |

## Output Formats

| Format | Request | Use Case |
|--------|---------|----------|
| JSON | (default) | API testing, internal use |
| NCPDP D.0 | "as NCPDP", "pharmacy claim format" | Real-time pharmacy claims |
| CSV | "as CSV" | Analytics, spreadsheets |

## Integration with Other Products

| Product | Integration | Example |
|---------|-------------|---------|
| **PatientSim** | Medication orders → Fills | Metformin order → NCPDP claim |
| **MemberSim** | Coordinated benefits | Combined deductible/OOP tracking |
| **NetworkSim** | Pharmacy entities | Dispensing pharmacy with NCPDP ID |
| **PopulationSim** | Geography → Adherence patterns | SVI vulnerability → adherence modeling |

## Data-Driven Generation (PopulationSim v2.0)

When you specify a geography, RxMemberSim uses **real population data** for realistic pharmacy utilization:

```
Generate pharmacy claims for a diabetic population in Pike County, KY
```

This grounds the claims in:
- Actual medication utilization rates (62% on BP meds in Pike County)
- SDOH-adjusted adherence (lower MPR with high SVI)
- Channel preferences (more mail-order with transportation barriers)
- Generic utilization patterns based on poverty rates

See [SKILL.md](SKILL.md#cross-product-populationsim-integration) for full integration details.

## DUR Alert Types

| Code | Type | Description |
|------|------|-------------|
| DD | Drug-Drug | Interaction between medications |
| TD | Therapeutic Duplication | Same drug class prescribed twice |
| ER | Early Refill | Before 80% of supply used |
| HD | High Dose | Exceeds recommended dosing |
| DA | Drug-Age | Age-based precaution |
| DC | Drug-Disease | Contraindication with condition |

## Skills Reference

For complete generation parameters, examples, and validation rules, see:

- **[SKILL.md](SKILL.md)** - Full skill reference with all cohorts
- **[../../SKILL.md](../../SKILL.md)** - Master skill file (cross-product routing)

## Related Documentation

- [hello-healthsim RxMemberSim Examples](../../hello-healthsim/examples/rxmembersim-examples.md)
- [Cross-Product Integration Guide](../../docs/HEALTHSIM-ARCHITECTURE-GUIDE.md#93-cross-product-integration)
- [NCPDP Format Specification](../../formats/ncpdp-d0.md)
- [Code Systems Reference](../../references/code-systems.md)

---

*RxMemberSim generates synthetic pharmacy data only. Never use for actual prescription processing.*
