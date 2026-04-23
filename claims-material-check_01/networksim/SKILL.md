---
name: healthsim-networksim
description: >
  NetworkSim provides provider network intelligence using real NPPES data (8.9M providers).
  Use this skill for ANY request involving: (1) provider search by specialty or location,
  (2) facility search (hospitals, nursing homes, clinics), (3) NPI validation,
  (4) network adequacy assessment against CMS/NCQA standards, (5) healthcare desert
  identification, (6) provider density analysis, (7) network roster generation,
  (8) hospital or physician quality metrics, (9) cross-product provider assignment,
  (10) pharmacy network analysis.
---

# NetworkSim - Provider Network Intelligence & Analytics

## Overview

NetworkSim queries **real NPPES provider data** (8.9M records), CMS facility data (60K+ facilities), and quality metrics. Unlike synthetic generation, it uses **actual registered providers** to enable:

1. **Provider Discovery**: Search by specialty, location, credentials, quality
2. **Network Analysis**: Assess adequacy against CMS MA, NCQA, Medicaid standards
3. **Healthcare Access**: Identify deserts via access gaps, health needs, vulnerability
4. **Cross-Product Integration**: Provide real providers for PatientSim, MemberSim, TrialSim

## Quick Reference

| I want to... | Use This Skill | Key Triggers |
|--------------|----------------|--------------|
| **Provider Search** | | |
| Find providers by specialty | `query/provider-search.md` | "find cardiologists", "search for PCPs", "providers in" |
| Search hospitals/facilities | `query/facility-search.md` | "hospitals in", "find nursing homes", "clinics near" |
| Find pharmacies | `query/pharmacy-search.md` | "pharmacies in", "retail pharmacy", "specialty pharmacy" |
| **Validation & Roster** | | |
| Validate an NPI | `query/npi-validation.md` | "is NPI valid", "validate NPI", "check NPI" |
| Generate network roster | `query/network-roster.md` | "create roster", "export providers", "network list" |
| **Density & Coverage** | | |
| Calculate provider density | `query/provider-density.md` | "providers per 100K", "density analysis", "HRSA benchmark" |
| Assess network coverage | `query/coverage-analysis.md` | "network coverage", "geographic coverage", "specialty gaps" |
| **Quality Metrics** | | |
| Filter by hospital quality | `query/hospital-quality-search.md` | "4-star hospitals", "high quality", "CMS ratings" |
| Filter by physician credentials | `query/physician-quality-search.md` | "MD only", "board certified", "credentials" |
| **Advanced Analytics** | | |
| Assess network adequacy | `analytics/network-adequacy-analysis.md` | "adequacy assessment", "CMS standards", "NCQA requirements" |
| Identify healthcare deserts | `analytics/healthcare-deserts.md` | "healthcare deserts", "underserved areas", "access gaps" |
| **Synthetic Generation** | | |
| Generate synthetic provider | `synthetic/synthetic-provider.md` | "generate a provider", "create physician" |
| Generate synthetic facility | `synthetic/synthetic-facility.md` | "generate hospital", "create facility" |
| Generate synthetic pharmacy | `synthetic/synthetic-pharmacy.md` | "generate pharmacy", "create pharmacy" |
| Generate synthetic network | `synthetic/synthetic-network.md` | "generate network", "create provider network" |
| Generate synthetic plan | `synthetic/synthetic-plan.md` | "generate plan", "create health plan" |
| **Integration** | | |
| Assign provider to encounter | `integration/provider-for-encounter.md` | "provider for patient", "attending physician" |
| Determine network status | `integration/network-for-member.md` | "in-network check", "network status" |
| Route prescription | `integration/pharmacy-for-rx.md` | "pharmacy for prescription", "dispense at" |

## Trigger Phrases

- **Provider/Facility**: "find [specialty] in [location]", "hospitals in [state]", "nursing homes near", "pharmacies in"
- **Validation/Roster**: "validate NPI", "is NPI valid", "create roster", "export providers"
- **Density/Coverage**: "providers per 100K", "density in [county]", "HRSA benchmark"
- **Quality**: "4-star hospitals", "MD/DO only", "board certified"
- **Adequacy**: "CMS adequacy standards", "NCQA coverage", "provider ratio", "time/distance"
- **Deserts/Access**: "healthcare deserts", "underserved counties", "access gaps", "shortage areas"

## Skill Inventory

### Query Skills (9 skills)

| Skill | File | Lines | Purpose |
|-------|------|-------|---------|
| Provider Search | `query/provider-search.md` | 450 | Search 8.9M providers by specialty, location |
| Facility Search | `query/facility-search.md` | 380 | Search hospitals, nursing homes, clinics |
| Pharmacy Search | `query/pharmacy-search.md` | 320 | Search retail, specialty, mail pharmacies |
| NPI Validation | `query/npi-validation.md` | 280 | Validate NPIs with Luhn checksums |
| Network Roster | `query/network-roster.md` | 350 | Generate rosters in CSV/JSON/Excel |
| Provider Density | `query/provider-density.md` | 400 | Calculate density vs HRSA benchmarks |
| Coverage Analysis | `query/coverage-analysis.md` | 380 | Assess geographic/specialty coverage |
| Hospital Quality | `query/hospital-quality-search.md` | 320 | Filter by CMS star ratings |
| Physician Quality | `query/physician-quality-search.md` | 290 | Filter by credentials (MD/DO/NP/PA) |

### Analytics Skills (2 skills)

| Skill | File | Lines | Purpose |
|-------|------|-------|---------|
| Network Adequacy | `analytics/network-adequacy-analysis.md` | 653 | CMS/NCQA regulatory compliance |
| Healthcare Deserts | `analytics/healthcare-deserts.md` | 757 | Access + health needs + vulnerability |

### Synthetic Skills (6 skills)

| Skill | File | Lines | Purpose |
|-------|------|-------|---------|
| Synthetic Provider | `synthetic/synthetic-provider.md` | 400 | Generate providers with valid NPI format |
| Synthetic Facility | `synthetic/synthetic-facility.md` | 350 | Generate hospitals, ASCs, clinics |
| Synthetic Pharmacy | `synthetic/synthetic-pharmacy.md` | 320 | Generate pharmacies with NCPDP IDs |
| Synthetic Network | `synthetic/synthetic-network.md` | 450 | Generate complete network configurations |
| Synthetic Plan | `synthetic/synthetic-plan.md` | 380 | Generate health plan structures |
| Synthetic Pharmacy Benefit | `synthetic/synthetic-pharmacy-benefit.md` | 350 | Generate PBM configurations |

### Integration Skills (5 skills)

| Skill | File | Lines | Purpose |
|-------|------|-------|---------|
| Provider for Encounter | `integration/provider-for-encounter.md` | 280 | Assign providers to PatientSim |
| Network for Member | `integration/network-for-member.md` | 300 | Network status for MemberSim |
| Pharmacy for Rx | `integration/pharmacy-for-rx.md` | 260 | Pharmacy routing for RxMemberSim |
| Formulary for Rx | `integration/formulary-for-rx.md` | 290 | Formulary checks for RxMemberSim |
| Benefit for Claim | `integration/benefit-for-claim.md` | 270 | Benefit lookup for MemberSim |

### Reference Skills (7 skills)

| Skill | File | Purpose |
|-------|------|---------|
| Network Types | `reference/network-types.md` | HMO, PPO, EPO, POS structures |
| Plan Structures | `reference/plan-structures.md` | Cost sharing, benefit design |
| Pharmacy Benefits | `reference/pharmacy-benefit-concepts.md` | PBM, formulary, tiers |
| Network Adequacy | `reference/network-adequacy.md` | CMS/NCQA standards |
| PBM Operations | `reference/pbm-operations.md` | Claims processing, rebates |
| Specialty Pharmacy | `reference/specialty-pharmacy.md` | Limited distribution, hubs |
| Utilization Management | `reference/utilization-management.md` | PA, step therapy, QL |

### Pattern Skills (5 skills)

| Skill | File | Purpose |
|-------|------|---------|
| HMO Network | `patterns/hmo-network-pattern.md` | Closed network, gatekeeper model |
| PPO Network | `patterns/ppo-network-pattern.md` | Open access, tiered cost sharing |
| Tiered Network | `patterns/tiered-network-pattern.md` | Quality-based tier assignment |
| Specialty Distribution | `patterns/specialty-distribution-pattern.md` | Specialty mix by geography |
| Pharmacy Benefit | `patterns/pharmacy-benefit-patterns.md` | PBM network configurations |

---

## Output Types

### ProviderSearchResult

Provider records from NPPES database:

```json
{
  "npi": "1234567890",
  "entity_type": "individual",
  "name": {
    "last": "Johnson",
    "first": "Sarah",
    "credential": "MD, FACC"
  },
  "taxonomy": {
    "code": "207RC0000X",
    "classification": "Internal Medicine",
    "specialization": "Cardiovascular Disease"
  },
  "practice_location": {
    "address": "123 Medical Center Dr",
    "city": "Houston",
    "state": "TX",
    "zip": "77030",
    "county_fips": "48201"
  },
  "enumeration_date": "2015-03-15",
  "last_update": "2024-11-01"
}
```

### AdequacyAssessment

Key fields: `geography` (type, code, name), `standard` (CMS_MA/NCQA), `metrics.pcp_ratio` (actual, required, status), `metrics.specialist_coverage` (13 specialties), `overall_status` (COMPLIANT/NON_COMPLIANT).

### HealthcareDesert

Key fields: `geography` (fips, county, state), `desert_type`, `severity` (critical/high/moderate), `scores` (access_gap, health_burden, social_vulnerability, composite 0-1), `intervention_priority` (1=highest).

### NetworkRoster

Key fields: `roster_id`, `criteria` (specialty, geography, quality_filter), `summary` (total_providers, by_taxonomy), `export_formats` (csv, json, xlsx).

---

## Data Sources

### Provider Data (network.providers)

| Attribute | Value |
|-----------|-------|
| Source | NPPES (National Plan and Provider Enumeration System) |
| Records | 8,925,672 |
| Update Frequency | Monthly CMS releases |
| Coverage | All active US healthcare providers with NPIs |
| County FIPS | 97.77% coverage (3,213 of 3,286 counties) |

**Key Columns**: npi, entity_type_code, last_name, first_name, credential, taxonomy_1-4, practice_state, practice_city, practice_zip, county_fips

### Additional Tables

| Table | Source | Records | Key Content |
|-------|--------|---------|-------------|
| `network.facilities` | CMS POS file | 77,302 | Hospitals (01), SNFs (05), HHAs (07), Hospice (13) |
| `network.hospital_quality` | CMS Hospital Compare | 5,421 | Star ratings (1-5), mortality, readmission, safety |
| `network.physician_quality` | CMS Physician Compare | 1,478,309 | Quality measures, Medicare participation |
| `network.ahrf_county` | HRSA AHRF | 3,235 | Provider counts, hospital beds, health workforce |

---

## Regulatory Standards

See `reference/network-adequacy.md` for full CMS MA ratios, time/distance tables, NCQA 13 essential specialties, ECP requirements, and HPSA/MUA definitions.

**Quick reference**:
- CMS MA PCP ratio: 1:1,200 enrollees
- HRSA HPSA threshold: <60 PCPs per 100K
- NCQA requires coverage across 13 specialties
- Time/distance varies by urban/suburban/rural designation

**Database**: healthsim.duckdb (1.7 GB), indexed on county_fips, taxonomy_1, practice_state

---

## Cross-Product Integration

### NetworkSim → PatientSim

Assign providers to clinical encounters:

```sql
-- Find cardiologist for heart failure patient
SELECT npi, first_name, last_name, credential
FROM network.providers
WHERE taxonomy_1 LIKE '207RC%'  -- Cardiovascular
  AND practice_state = 'TX'
  AND county_fips = '48201'     -- Harris County
LIMIT 1;
```

### NetworkSim → MemberSim

Determine network status for claims:

```sql
-- Check if provider is in network
SELECT 
  CASE WHEN p.npi IS NOT NULL THEN 'IN_NETWORK' 
       ELSE 'OUT_OF_NETWORK' END as network_status
FROM network.providers p
WHERE p.npi = '1234567890';
```

### NetworkSim + PopulationSim

Equity analysis combining provider access with vulnerability:

```sql
-- Provider access in vulnerable communities
SELECT 
    sv.county,
    sv.rpl_themes as svi_percentile,
    COUNT(DISTINCT p.npi) as provider_count,
    sv.e_totpop as population,
    ROUND(COUNT(DISTINCT p.npi) * 100000.0 / sv.e_totpop, 1) as per_100k
FROM population.svi_county sv
LEFT JOIN network.providers p ON sv.stcnty = p.county_fips
WHERE sv.rpl_themes > 0.75  -- Most vulnerable quartile
GROUP BY sv.county, sv.rpl_themes, sv.e_totpop
ORDER BY per_100k ASC;
```

---

## Safety Guardrails

### Real Data Disclaimer
NetworkSim queries **real NPPES registry data** (public CMS data, non-PHI). Every NPI is a real registered provider. Results reflect registry status only -- not accepting-patients, insurance participation, or clinical competence.

### What NetworkSim Does NOT Do
- **No clinical advice**: Never suggest a provider is "best" for a condition
- **No insurance verification**: Network status is simulated, not real-time eligibility
- **No appointment scheduling**: Registry data is not a booking system
- **No synthetic NPIs in real queries**: Use `synthetic/` skills only for test data

### Code System References
| System | Used For | Example |
|--------|----------|---------|
| NUCC Taxonomy | Provider specialty classification | `207RC0000X` = Cardiovascular Disease |
| NPI | Provider identification (Luhn-validated) | `1234567890` |
| County FIPS | Geographic scoping | `48201` = Harris County, TX |
| CMS Certification Number | Facility identification | POS file facility IDs |
| CBSA | Urban/rural classification | Metro, micro, rural designations |
| HCPCS | Provider service codes | Level I (CPT) and Level II codes |

**Cross-product code systems** (via PatientSim/MemberSim/RxMemberSim integration): ICD-10 (diagnoses), CPT (procedures), LOINC (labs), SNOMED (clinical terms), RxNorm/NDC (medications). These are real standard codes -- linked patient data is synthetic/fictional.

### Edge Cases
- **Missing county_fips**: ~2.2% of records lack county FIPS; filter with `WHERE county_fips IS NOT NULL` for geographic queries
- **Deactivated NPIs**: Check `npi_deactivation_date IS NULL` for active providers
- **Multi-taxonomy providers**: Up to 15 taxonomies; `taxonomy_1` is primary but check `taxonomy_2`-`taxonomy_4` for dual-specialty searches
- **Organization vs Individual**: `entity_type_code = 1` (individual) vs `2` (organization); filter appropriately

### Negative Examples (What NOT to Do)

**Never give clinical advice based on provider data:**
- WRONG: "I recommend Dr. Smith for your heart condition" or "The patient needs a cardiologist"
- RIGHT: "Here are cardiologists registered in Harris County per NPPES data. This is simulated test data for analytics, not a referral."

**Always distinguish real reference data from synthetic/fictional entities:**
- WRONG: "Here is the patient's real provider" (implies real clinical relationship)
- RIGHT: "NPI data is from the real NPPES registry (public CMS data). Patient/encounter data is synthetic/fictional -- not real patient information."

**Never mix synthetic and real data without labeling:**
- WRONG: Return synthetic NPIs alongside real NPPES query results
- RIGHT: Label synthetic providers (from `synthetic/` skills) vs real providers (from `network.providers`)

## Validation Rules

### NPI: 10 digits, Luhn checksum, prefix 1 (individual) or 2 (organization), active in NPPES
### Taxonomy: Valid NUCC codes, primary taxonomy switch indicator
### Geography: 2-letter state, 5-digit county FIPS, 5- or 9-digit ZIP

---

## Related Documentation

- **Examples**: [hello-healthsim/examples/networksim-examples.md](../../hello-healthsim/examples/networksim-examples.md)
- **Developer Guide**: [developer-guide.md](developer-guide.md)
- **Prompt Guide**: [prompt-guide.md](prompt-guide.md)
- **Data Architecture**: [docs/healthsim-duckdb-schema.md](../../docs/healthsim-duckdb-schema.md)
- **Master SKILL.md**: [SKILL.md](../../SKILL.md)

---

*Last Updated: December 28, 2025*
*Version: 2.0.0*
*Status: Active (Phase 3)*
