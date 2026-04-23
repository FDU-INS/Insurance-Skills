# NetworkSim v1.0 - Master Plan

**Status**: Planning  
**Created**: 2024-12-24  
**Target Completion**: TBD

---

## Overview

NetworkSim generates realistic provider network data using public sources (NPPES NPI Registry, CMS Provider files). It enhances geographic and structural realism across all HealthSim products by replacing generic provider IDs with realistic provider distributions.

---

## Goals

1. **Provider Network Generation**: Create realistic provider networks for any geography
2. **Cross-Product Enhancement**: Enable PatientSim, MemberSim, TrialSim to reference real provider structures
3. **Geographic Realism**: Provider density, specialty mix, and facility types match actual US distributions
4. **Standards Compliance**: NPI format, taxonomy codes, CMS certification numbers

---

## Data Sources

| Source | URL | Content | Size Est. |
|--------|-----|---------|-----------|
| NPPES NPI Registry | https://download.cms.gov/nppes/NPI_Files.html | All US providers | ~8GB (filtered to ~500MB) |
| CMS Provider of Services | https://data.cms.gov/provider-data/ | Hospitals, facilities | ~100MB |
| CMS Physician Compare | https://data.cms.gov/provider-data/ | Physician details | ~200MB |
| NUCC Taxonomy Codes | https://nucc.org/index.php/code-sets-mainmenu-41 | Provider types | Reference only |

---

## Phases

### Phase 1: Data Package
**Goal**: Download, filter, and embed core provider data  
**Sessions**: 2-3  
**Deliverables**:
- `skills/networksim/data/` directory with filtered datasets
- Data documentation with column mappings
- Geography crosswalks (county → providers)

### Phase 2: Core Skills
**Goal**: Basic provider lookup and network generation  
**Sessions**: 2-3  
**Deliverables**:
- `skills/networksim/SKILL.md` - Master routing
- Provider lookup skills (by NPI, geography, specialty)
- Network generation skills (PCP, specialist, facility)

### Phase 3: Cross-Product Integration
**Goal**: Enable other products to use NetworkSim providers  
**Sessions**: 2  
**Deliverables**:
- PatientSim: Attending/referring physician references
- MemberSim: Billing/rendering provider on claims
- TrialSim: Site/investigator references
- Integration documentation

### Phase 4: Advanced Features
**Goal**: Network adequacy, credentialing simulation  
**Sessions**: 2  
**Deliverables**:
- Network adequacy analysis skills
- Provider credentialing data patterns
- Payer-specific network tiers

---

## Session Prompts

| Session | File | Focus | Est. Duration |
|---------|------|-------|---------------|
| 01 | SESSION-01-data-research.md | Evaluate data sources, define filtering strategy | 1 session |
| 02 | SESSION-02-data-download.md | Download and filter NPPES data | 1 session |
| 03 | SESSION-03-data-package.md | Create embedded data package | 1 session |
| 04 | SESSION-04-core-skills.md | Provider lookup skills | 1 session |
| 05 | SESSION-05-network-gen.md | Network generation skills | 1 session |
| 06 | SESSION-06-integration.md | Cross-product integration | 1 session |
| 07 | SESSION-07-advanced.md | Network adequacy, credentialing | 1 session |
| 08 | SESSION-08-polish.md | Documentation, examples, testing | 1 session |

---

## Success Criteria

- [ ] Provider data embedded (~500MB filtered from NPPES)
- [ ] 100% US county coverage for provider lookup
- [ ] Specialty distribution matches CMS actuals
- [ ] PatientSim can generate encounters with real NPI references
- [ ] MemberSim can generate claims with valid provider data
- [ ] All tests passing
- [ ] hello-healthsim tutorial for NetworkSim

---

## Dependencies

- PopulationSim v2.0 geography data (for FIPS crosswalks) ✅ Complete
- NPPES monthly data file (download required)
- CMS provider files (download required)

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| NPPES file too large | Storage, performance | Aggressive filtering (active providers, key fields only) |
| Data freshness | Stale provider info | Document data date, plan quarterly refresh |
| Taxonomy complexity | Inconsistent specialty mapping | Create simplified specialty crosswalk |

---

## Notes

_Planning notes and decisions_

- Consider starting with county-level provider counts before full NPI data
- May want to create "synthetic providers" for privacy rather than using real NPIs
- Check if NPPES has any usage restrictions for our use case
