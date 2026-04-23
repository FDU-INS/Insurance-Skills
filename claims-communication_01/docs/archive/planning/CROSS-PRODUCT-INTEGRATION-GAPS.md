# Cross-Product Integration Gap Analysis

**Date**: 2025-12-21  
**Updated**: 2025-12-21  
**Purpose**: Identify structural gaps that would make cross-product integration difficult

---

## Executive Summary

HealthSim is designed as a unified ecosystem where products share foundational data and cross-reference each other. Analysis reveals **7 structural gaps** that would make this difficult without intervention. The most critical are the missing foundation layers (PopulationSim, NetworkSim) and the lack of cross-product identity mapping patterns.

### Status Summary

| Gap | Description | Severity | Status |
|-----|-------------|----------|--------|
| #1 | Missing Foundation Products | MEDIUM | ⚡ Partial - PopulationSim Active, NetworkSim Planned |
| #2 | No Cross-Product Identity Mapping | HIGH | ✅ **RESOLVED** - Added to data-models.md |
| #3 | Incomplete Cross-References | MEDIUM | ✅ **RESOLVED** - All products linked |
| #4 | Missing Shared Domain References | MEDIUM | ✅ **RESOLVED** - Cross-refs added; shared refs deferred |
| #5 | No Provider/Facility Reference | MEDIUM | 🔜 Planned (NetworkSim) |
| #6 | No Event Correlation Pattern | MEDIUM | ⏸️ Deferred (user-triggered for now) |
| #7 | Architecture Guide Incomplete | LOW | 🔜 Planned |

---

## Gap 1: Missing Foundation Products

**Severity**: HIGH  
**Impact**: All products generate demographics and providers ad-hoc, leading to inconsistency

### Current State
- **PopulationSim**: ✅ Active - demographics, SDOH, cohort specifications available
- **NetworkSim**: Planned but not implemented - providers/facilities generated ad-hoc per product

### Problem
Each product independently generates:
- Demographics (age, gender, address, race)
- Providers (NPI, name, specialty)
- Facilities (NPI, name, type)

This leads to:
- Inconsistent geographic distribution
- Non-realistic provider specialties for given cohorts
- No shared provider pool across cohorts

### Recommendation
**Priority**: Implement PopulationSim and NetworkSim as foundation layers BEFORE adding new cohort skills.

**Interim Workaround**: Create shared reference files:
- `references/demographics-patterns.md` - Realistic age/gender distributions by cohort
- `references/provider-patterns.md` - Common provider types by specialty area
- `references/facility-types.md` - Facility codes and characteristics

---

## Gap 2: No Cross-Product Identity Mapping Pattern

**Severity**: HIGH  
**Status**: ✅ **RESOLVED** (2025-12-21)  
**Resolution**: Added "Cross-Product Identity Correlation" section to `references/data-models.md`  
**Impact**: Cannot generate the SAME person across multiple products

### Current State
Data models define inheritance:
```
Person → Patient (+ mrn)
Person → Member (+ member_id, subscriber_id)
Person → RxMember (+ cardholder_id, bin, pcn)
Person → Subject (+ subject_id) [implied for TrialSim]
```

But NO guidance exists for:
- How to link identities across products
- How to generate consistent person data
- How to correlate events across products

### Example Problem
Generate a patient journey: Hospital admission → Claim submission → Prescription fill

Currently no pattern for:
- Patient MRN `12345` = Member ID `ABC123` = Cardholder ID `XYZ789`
- Encounter ID `ENC-001` correlates to Claim ID `CLM-001`
- Inpatient medication → Discharge prescription → Pharmacy fill

### Recommendation
Create `references/identity-mapping.md` with:

```markdown
## Cross-Product Identity Mapping

### Person Identity Correlation
When generating the same person across products:

| Product | Primary ID | Secondary IDs |
|---------|------------|---------------|
| PatientSim | MRN | SSN (optional) |
| MemberSim | member_id | subscriber_id, SSN |
| RxMemberSim | cardholder_id | member_id, person_code |
| TrialSim | subject_id | screening_id, mrn (if EMR-linked) |

### Linkage Pattern
```json
{
  "person_correlation": {
    "master_id": "PERSON-001",
    "identities": {
      "patientsim": { "mrn": "12345" },
      "membersim": { "member_id": "ABC123", "subscriber_id": "ABC123" },
      "rxmembersim": { "cardholder_id": "XYZ789", "person_code": "01" },
      "trialsim": { "subject_id": "TRL-001" }
    }
  }
}
```

### Event Correlation Pattern
When an event in one product should generate related events in others:

| Source Event | Correlated Events |
|--------------|-------------------|
| PatientSim Encounter | MemberSim Claim(s), RxMemberSim Prescription(s) |
| PatientSim Medication Order | RxMemberSim Prescription → PharmacyClaim |
| MemberSim Prior Auth | PatientSim scheduled procedure |
| TrialSim Subject Enrollment | PatientSim encounters (study visits) |
```

---

## Gap 3: Incomplete Cross-Product References Between Products

**Severity**: MEDIUM  
**Status**: ✅ **RESOLVED** (2025-12-21)  
**Resolution**: Added cross-product "Related Skills" sections with integration patterns to all skills  
**Impact**: Users and Claude don't discover related skills across products

### Current State

| Product A | Product B | Cross-Refs Exist? |
|-----------|-----------|-------------------|
| PatientSim | TrialSim | ✅ Yes (oncology, CV, CNS) |
| PatientSim | MemberSim | ⚠️ Partial (behavioral-health only) |
| PatientSim | RxMemberSim | ❌ Missing |
| MemberSim | RxMemberSim | ❌ Missing |
| TrialSim | MemberSim | ❌ Missing |
| TrialSim | RxMemberSim | ❌ Missing |

### Missing Cross-References

**PatientSim → MemberSim** (cohorts that should link):
- `heart-failure.md` → facility-claims.md, prior-authorization.md
- `diabetes-management.md` → professional-claims.md
- `chronic-kidney-disease.md` → facility-claims.md
- `elective-joint.md` → prior-authorization.md, facility-claims.md
- `ed-chest-pain.md` → facility-claims.md
- `oncology/*.md` → facility-claims.md, prior-authorization.md

**PatientSim → RxMemberSim**:
- `diabetes-management.md` → retail-pharmacy.md, rx-prior-auth.md
- `heart-failure.md` → retail-pharmacy.md
- `behavioral-health.md` → retail-pharmacy.md (already partial via MemberSim)
- `chronic-kidney-disease.md` → specialty-pharmacy.md
- `oncology/*.md` → specialty-pharmacy.md

**MemberSim → RxMemberSim**:
- `plan-benefits.md` → formulary-management.md
- `accumulator-tracking.md` → rx-accumulator.md
- `prior-authorization.md` → rx-prior-auth.md
- `enrollment-eligibility.md` → rx-enrollment.md

### Recommendation
Systematic cross-reference addition project (see implementation plan below).

---

## Gap 4: Missing Shared Domain References

**Severity**: MEDIUM  
**Status**: ✅ **RESOLVED** (2025-12-21)  
**Resolution**: Cross-product references now link to existing domain knowledge in each product. Standalone shared references (cardiovascular-domain.md, etc.) deferred - can be created when needed.  
**Impact**: Domain knowledge duplicated or inconsistent across products

### Current State

| Domain | Shared Reference | Products Using |
|--------|------------------|----------------|
| Oncology | ✅ `references/oncology-domain.md` | PatientSim, TrialSim |
| Behavioral Health | ✅ `references/mental-health-reference.md` | PatientSim, MemberSim |
| Cardiovascular | ❌ Missing | PatientSim, TrialSim |
| CNS/Neurology | ❌ Missing | PatientSim, TrialSim |
| Diabetes | ❌ Missing | PatientSim, (RxMemberSim) |
| Chronic Kidney Disease | ❌ Missing | PatientSim |
| Pediatrics | ⚠️ Partial (`pediatric-dosing.md`) | PatientSim |

### Recommendation
Create shared domain references for active therapeutic areas:
- `references/cardiovascular-domain.md`
- `references/cns-domain.md`
- `references/diabetes-domain.md`

---

## Gap 5: No Provider/Facility Reference

**Severity**: MEDIUM  
**Impact**: Provider data inconsistent, no realistic specialty distribution

### Current State
No shared provider reference exists. Each product generates:
- Provider NPI (random 10-digit)
- Provider name (random)
- Specialty (cohort-appropriate but not validated)
- Facility (ad-hoc)

### Problem Examples
- PatientSim oncology generates "Dr. Smith, Oncologist" with NPI 1234567890
- MemberSim claim for same cohort uses completely different provider
- No realistic specialty taxonomy codes used

### Recommendation
Create `references/provider-reference.md`:

```markdown
## Provider Taxonomy Codes

### Common Specialties
| Taxonomy Code | Specialty | Typical Cohorts |
|--------------|-----------|-------------------|
| 207RH0003X | Hematology/Oncology | Oncology cohorts |
| 207RC0000X | Cardiovascular Disease | Heart failure, chest pain |
| 2084P0800X | Psychiatry | Behavioral health |
| 207RE0101X | Endocrinology | Diabetes |
| 207RN0300X | Nephrology | CKD |

### Provider Generation Pattern
For consistency, generate provider with:
- Valid NPI format (Luhn check digit)
- Appropriate taxonomy code
- Realistic name patterns
- Geographic alignment with cohort
```

NetworkSim will eventually own this, but interim reference needed.

---

## Gap 6: No Cross-Product Event Correlation Pattern

**Severity**: MEDIUM  
**Impact**: Cannot generate realistic multi-product journeys

### Current State
No documented pattern for generating events that span products:
- Patient admitted → Claim submitted → Rx filled
- Prior auth approved → Procedure scheduled → Claim filed
- Trial subject enrolled → Study visits → Pharmacy dispensing

### Recommendation
Add section to `references/generation-patterns.md`:

```markdown
## Cross-Product Event Correlation

### Clinical-to-Claims Flow
1. PatientSim: Generate encounter with diagnoses, procedures, medications
2. MemberSim: Generate claim(s) with matching:
   - Service date = encounter date
   - Diagnosis codes from encounter
   - Procedure codes from orders
   - Provider NPI consistent
3. RxMemberSim: Generate pharmacy claims with:
   - Fill date shortly after discharge
   - NDC matching prescribed medication
   - Prescriber NPI from encounter

### Timeline Correlation
| PatientSim Event | MemberSim Timing | RxMemberSim Timing |
|------------------|------------------|-------------------|
| Outpatient visit | Same day or +1 day | Same day (in-office) |
| ED visit | Same day | N/A or +1 day |
| Inpatient stay | +2 to +14 days | Discharge +0-3 days |
| Surgery | +7 to +30 days | +0-7 days (pain meds) |
```

---

## Gap 7: Architecture Guide Cross-Product Mapping Incomplete

**Severity**: LOW  
**Impact**: Documentation doesn't reflect full integration picture

### Current State
Section 8.3 only shows PatientSim ↔ TrialSim mapping.

### Missing from Mapping Table
- PatientSim ↔ MemberSim integration
- PatientSim ↔ RxMemberSim integration
- MemberSim ↔ RxMemberSim integration
- Future PopulationSim/NetworkSim integration points

### Recommendation
Expand cross-product mapping table to show all product relationships.

---

## Implementation Priority

### Phase 1: Foundation (Before New Skills)
1. ✅ Document cross-product integration as standard practice (DONE)
2. ✅ Add cross-product identity mapping to `references/data-models.md` (DONE)
3. Create `references/provider-reference.md` (deferred to NetworkSim)
4. Expand Architecture Guide cross-product table

### Phase 2: Cross-Reference Completion
5. ✅ Add PatientSim ↔ MemberSim cross-references (DONE)
6. ✅ Add PatientSim ↔ RxMemberSim cross-references (DONE)
7. ✅ Add MemberSim ↔ RxMemberSim cross-references (DONE)

### Phase 3: Shared Domain References
8. Create `references/cardiovascular-domain.md`
9. Create `references/cns-domain.md`
10. Create `references/diabetes-domain.md`

### Phase 4: Foundation Products
11. Implement PopulationSim foundation layer
12. Implement NetworkSim foundation layer
13. Retrofit existing products to use foundations

---

## Cross-Product Integration Vision

```
                    ┌─────────────────┐
                    │  PopulationSim  │ ← Demographics Foundation
                    │  (Geographic,   │
                    │   SDOH, Census) │
                    └────────┬────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
         ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│   PatientSim    │ │   MemberSim     │ │   RxMemberSim   │
│   (Clinical)    │◄─►│   (Claims)     │◄─►│   (Pharmacy)   │
└────────┬────────┘ └────────┬────────┘ └────────┬────────┘
         │                   │                   │
         └───────────────────┼───────────────────┘
                             │
                    ┌────────┴────────┐
                    │   NetworkSim    │ ← Provider/Facility Foundation
                    │  (Providers,    │
                    │   Facilities)   │
                    └─────────────────┘
                             │
                    ┌────────┴────────┐
                    │    TrialSim     │ ← Uses all foundations
                    │ (Sites, PIs,    │
                    │  Subjects)      │
                    └─────────────────┘
```

When fully implemented:
- PopulationSim provides realistic demographics for all products
- NetworkSim provides consistent providers/facilities for all products
- Cross-references enable discovery of related capabilities
- Event correlation enables multi-product journey generation

---

*End of Gap Analysis*
