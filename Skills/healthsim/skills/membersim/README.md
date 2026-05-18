# MemberSim

> Generate realistic healthcare claims and payer data including enrollment, professional and facility claims, adjudication, and accumulator tracking.

## What MemberSim Does

MemberSim is the **claims and payer data** engine of HealthSim. It creates synthetic health plan members with realistic coverage, and generates claims that flow through proper adjudication logic—applying deductibles, copays, coinsurance, and tracking accumulators exactly like a real payer system.

Whether you need a single paid claim, a denied prior auth, or a year of claims for a member panel, MemberSim generates data that matches how real claims processing works.

## Quick Start

**Simple:**
```
Generate a professional claim for an office visit
Generate a member with PPO coverage
```

**With adjudication:**
```
Generate a denied claim for MRI without prior authorization
Generate a claim where deductible applies
```

**With output format:**
```
Generate a professional claim as X12 837P
Generate a remittance as X12 835
```

See [hello-healthsim examples](../../hello-healthsim/examples/membersim-examples.md) for detailed examples with expected outputs.

## Key Capabilities

| Capability | Description | Skill Reference |
|------------|-------------|-----------------|
| **Enrollment** | Members with plans, coverage dates, group info | [enrollment-eligibility.md](enrollment-eligibility.md) |
| **Professional Claims** | 837P claims with CPT, modifiers, place of service | [professional-claims.md](professional-claims.md) |
| **Facility Claims** | 837I claims with DRGs, revenue codes, UB-04 | [facility-claims.md](facility-claims.md) |
| **Adjudication** | Payment calculation with CARC/RARC codes | [SKILL.md](SKILL.md#adjudication-logic) |
| **Prior Auth** | PA requests, approvals, denials | [prior-authorization.md](prior-authorization.md) |
| **Accumulators** | Deductible, OOP tracking | [accumulator-tracking.md](accumulator-tracking.md) |
| **Value-Based Care** | HEDIS, risk adjustment, HCC | [value-based-care.md](value-based-care.md) |

## Claim Cohorts

| Cohort | Key Elements | Skill |
|----------|--------------|-------|
| Plan & Benefits | HMO/PPO/HDHP design, cost sharing | [plan-benefits.md](plan-benefits.md) |
| Professional Claims | Office visits, consults, E&M coding | [professional-claims.md](professional-claims.md) |
| Facility Claims | Inpatient, outpatient, ED, DRG assignment | [facility-claims.md](facility-claims.md) |
| Prior Authorization | PA requests, medical necessity, approvals/denials | [prior-authorization.md](prior-authorization.md) |
| Accumulator Tracking | Deductible, OOP, family vs individual | [accumulator-tracking.md](accumulator-tracking.md) |
| Behavioral Health | Mental health parity, SUD claims | [behavioral-health.md](behavioral-health.md) |

## Output Formats

| Format | Request | Use Case |
|--------|---------|----------|
| JSON | (default) | API testing, internal use |
| X12 834 | "as 834", "enrollment file" | Enrollment transactions |
| X12 837P | "as 837P", "professional claim" | Professional claims |
| X12 837I | "as 837I", "institutional claim" | Facility claims |
| X12 835 | "as 835", "remittance" | Payment posting |
| X12 270/271 | "as 270", "eligibility" | Eligibility inquiry/response |
| CSV | "as CSV" | Analytics, spreadsheets |

## Integration with Other Products

| Product | Integration | Example |
|---------|-------------|---------|
| **PatientSim** | Clinical encounters → Claims | Heart failure admission → 837I with DRG 291 |
| **RxMemberSim** | Coordinated benefits | Combined deductible/OOP tracking |
| **NetworkSim** | Network status → Adjudication | In-network vs OON cost sharing |
| **PopulationSim** | Geography → Utilization patterns | County health rates → Expected claims |

## Data-Driven Generation (PopulationSim v2.0)

When you specify a geography, MemberSim uses **real population data** for actuarially realistic member panels:

```
Generate 1,000 members for a Medicare Advantage plan in Maricopa County, AZ
```

This grounds the members in:
- Real age distributions (17% 65+ in Maricopa)
- Actual chronic disease prevalence for risk adjustment
- Expected utilization based on CDC PLACES data
- SDOH factors affecting plan selection and adherence

See [SKILL.md](SKILL.md) for full integration details.

## Skills Reference

For complete generation parameters, examples, and validation rules, see:

- **[SKILL.md](SKILL.md)** - Full skill reference with all cohorts
- **[../../SKILL.md](../../SKILL.md)** - Master skill file (cross-product routing)

## Related Documentation

- [hello-healthsim MemberSim Examples](../../hello-healthsim/examples/membersim-examples.md)
- [Cross-Product Integration Guide](../../docs/HEALTHSIM-ARCHITECTURE-GUIDE.md#93-cross-product-integration)
- [X12 Format Specifications](../../formats/)
- [Code Systems Reference](../../references/code-systems.md)

---

*MemberSim generates synthetic claims data only. Never use for actual claims submission.*
