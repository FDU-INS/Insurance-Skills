---
name: networksim-developer-guide
description: |
  Developer guide for NetworkSim covering quick start, core concepts,
  skill reference, workflows, output formats, integration points, and
  best practices for working with healthcare network data.
---

# NetworkSim Developer Guide

## Overview

NetworkSim provides healthcare network knowledge and synthetic entity generation for the HealthSim ecosystem. This guide covers technical details for developers integrating NetworkSim into their workflows.

**Key Principle**: NetworkSim generates the *structural entities* (providers, facilities, pharmacies, networks) that other HealthSim products use for realistic data generation.

---

## Quick Start

### 1. Network Type Reference

```
User: Explain the difference between HMO and PPO networks

Claude: 
HMO (Health Maintenance Organization) and PPO (Preferred Provider Organization) 
differ primarily in flexibility and cost:

| Aspect | HMO | PPO |
|--------|-----|-----|
| Network | Must use in-network | Can use any provider |
| Referrals | Required for specialists | Not required |
| PCP Required | Yes | No |
| Out-of-Network | Not covered (except emergency) | Covered at higher cost |
| Premiums | Lower | Higher |

HMOs emphasize coordinated care through a gatekeeper model.
PPOs prioritize member flexibility with broader access.
```

### 2. Synthetic Provider Generation

```
User: Generate a cardiologist in Houston, Texas

Claude:
{
  "npi": "1234567890",
  "entity_type": "individual",
  "provider": {
    "last_name": "Nguyen",
    "first_name": "David",
    "credential": "MD, FACC"
  },
  "taxonomy": {
    "code": "207RC0000X",
    "classification": "Internal Medicine",
    "specialization": "Cardiovascular Disease"
  },
  "practice_location": {
    "city": "Houston",
    "state": "TX",
    "county_fips": "48201"
  }
}
```

### 3. Cross-Product Integration

```
User: Generate a provider for this heart failure patient's cardiology referral

Claude:
Based on the patient's diagnosis (I50.9) and location, generating 
an appropriate heart failure specialist:

{
  "npi": "1987654321",
  "provider": {
    "last_name": "Patel",
    "first_name": "Vikram",
    "credential": "MD, FACC, FHFSA"
  },
  "taxonomy": {
    "code": "207RC0001X",
    "specialization": "Advanced Heart Failure and Transplant Cardiology"
  },
  "integration_context": {
    "source_product": "patientsim",
    "matched_on": ["diagnosis_category", "geography"]
  }
}
```

---

## Core Concepts

### Network Types

NetworkSim supports five major network types, each with distinct access and cost characteristics:

| Network Type | Network Access | Referral Required | Out-of-Network Coverage | Cost Level |
|--------------|----------------|-------------------|------------------------|------------|
| **HMO** | Closed - in-network only | Yes, PCP gatekeeper | Emergency only | Lowest |
| **EPO** | Closed - in-network only | No | Emergency only | Low |
| **POS** | Hybrid - choose at service | For OON coverage | Yes, at higher cost | Medium |
| **PPO** | Open - any provider | No | Yes, at higher cost | Higher |
| **HDHP** | Varies (often PPO) | Varies | Plan-dependent | Varies |

**HMO Variants**:
- Staff Model: Physicians employed by HMO
- Group Model: Contracted physician groups
- IPA Model: Independent Practice Association
- Network Model: Multiple provider groups

**HDHP Requirements (2024)**:
- Minimum deductible: $1,600 individual / $3,200 family
- Maximum OOP: $8,050 individual / $16,100 family
- HSA contribution limits: $4,150 individual / $8,300 family

### Provider Taxonomy

The NUCC (National Uniform Claim Committee) Healthcare Provider Taxonomy defines provider classifications. NetworkSim uses these standard codes:

**Key Taxonomy Code Patterns**:

| Code Prefix | Classification | Common Specialties |
|-------------|---------------|-------------------|
| `207R%` | Internal Medicine | Cardiology (207RC), Gastro (207RG), Pulm (207RP) |
| `207X%` | Orthopedic Surgery | Adult Reconstructive, Hand, Spine |
| `207Q%` | Family Medicine | General, Adolescent, Geriatric |
| `207P%` | Emergency Medicine | General, Pediatric, Sports |
| `207N%` | Dermatology | General, MOHS, Dermatopathology |
| `207L%` | Anesthesiology | General, Pain Medicine, Critical Care |
| `207K%` | Allergy/Immunology | General, Clinical & Lab Immunology |
| `208D%` | General Practice | Non-board certified physicians |
| `363L%` | Nurse Practitioner | Family, Adult, Pediatric, Psych |
| `363A%` | Physician Assistant | Medical, Surgical |

**Credential Abbreviations**:

| Credential | Meaning |
|------------|---------|
| MD | Doctor of Medicine |
| DO | Doctor of Osteopathic Medicine |
| FACC | Fellow, American College of Cardiology |
| FACS | Fellow, American College of Surgeons |
| NP | Nurse Practitioner |
| PA-C | Physician Assistant, Certified |
| DNP | Doctor of Nursing Practice |

### Facility Types

Healthcare facilities are classified by service type and regulatory category:

**Acute Care Facilities**:

| Type | CCN Prefix | Characteristics |
|------|-----------|-----------------|
| Short-Term Acute | XX0001-0879 | General hospitals, <25 day average LOS |
| Long-Term Acute (LTACH) | XX2000-2299 | >25 day average LOS, complex patients |
| Critical Access (CAH) | XX1300-1399 | Rural, <25 beds, <96 hr average stay |
| Rehabilitation | XX3025-3099 | Inpatient rehab, 60% rule |
| Psychiatric | XX4000-4499 | Inpatient mental health |
| Children's | XX3300-3399 | Pediatric specialty |

**Post-Acute Facilities**:

| Type | CCN Prefix | Characteristics |
|------|-----------|-----------------|
| Skilled Nursing (SNF) | XX5000-6499 | Medicare-certified, 24/7 nursing |
| Home Health Agency | XX7000-7999 | Intermittent skilled services |
| Hospice | XX1500-1799 | End-of-life care |

**Ambulatory Facilities**:

| Type | CCN Prefix | Characteristics |
|------|-----------|-----------------|
| Ambulatory Surgical Center | XX5500-5549 | Outpatient surgery |
| Federally Qualified Health Center | XX1861-1869 | Community health, sliding scale |
| Rural Health Clinic | XX1880-1889 | Non-urban primary care |
| Dialysis Center | XX2300-2499 | ESRD treatment |

### Pharmacy Classification

Pharmacies are classified by dispensing model and specialty focus:

**Pharmacy Types**:

| Type | NCPDP Type | Characteristics |
|------|-----------|-----------------|
| Community/Retail | 01 | Walk-in, chain or independent |
| Mail Order | 02 | High volume, 90-day supply |
| Long-Term Care | 04 | Nursing home, assisted living |
| Specialty | 07 | High-cost, limited distribution |
| Clinic/Hospital | 05 | Outpatient dispensing |
| Nuclear | 06 | Radiopharmaceuticals |
| Home Infusion | 03 | IV therapy at home |

**Specialty Pharmacy Characteristics**:
- AWP typically >$1,000/month
- Requires special handling (cold chain, REMS)
- Complex patient management needs
- Limited distribution in many cases
- Clinical support services (adherence, side effects)

---

## Skill Reference

### Reference Skills (Conceptual Knowledge)

| Skill | Purpose | Example Trigger |
|-------|---------|-----------------|
| [network-types](reference/network-types.md) | Network type definitions | "explain HMO vs PPO" |
| [plan-structures](reference/plan-structures.md) | Benefit design concepts | "what is a deductible" |
| [pharmacy-benefit-concepts](reference/pharmacy-benefit-concepts.md) | Pharmacy benefit design | "explain tier structure" |
| [pbm-operations](reference/pbm-operations.md) | PBM functions | "what is BIN PCN" |
| [utilization-management](reference/utilization-management.md) | UM programs | "prior authorization process" |
| [specialty-pharmacy](reference/specialty-pharmacy.md) | Specialty distribution | "hub model for specialty" |
| [network-adequacy](reference/network-adequacy.md) | Access standards | "time distance standards" |

### Synthetic Skills (Entity Generation)

| Skill | Purpose | Example Trigger |
|-------|---------|-----------------|
| [synthetic-provider](synthetic/synthetic-provider.md) | Generate providers | "generate cardiologist in Houston" |
| [synthetic-facility](synthetic/synthetic-facility.md) | Generate facilities | "generate 200-bed hospital" |
| [synthetic-pharmacy](synthetic/synthetic-pharmacy.md) | Generate pharmacies | "generate specialty pharmacy" |
| [synthetic-network](synthetic/synthetic-network.md) | Generate networks | "generate HMO network" |
| [synthetic-plan](synthetic/synthetic-plan.md) | Generate plans | "generate silver tier plan" |
| [synthetic-pharmacy-benefit](synthetic/synthetic-pharmacy-benefit.md) | Generate Rx benefits | "generate 4-tier formulary" |

### Pattern Skills (Configuration Templates)

| Skill | Purpose | Example Trigger |
|-------|---------|-----------------|
| [hmo-network-pattern](patterns/hmo-network-pattern.md) | HMO templates | "IPA model HMO" |
| [ppo-network-pattern](patterns/ppo-network-pattern.md) | PPO templates | "national PPO network" |
| [tiered-network-pattern](patterns/tiered-network-pattern.md) | Tiered networks | "quality-based tier" |
| [pharmacy-benefit-patterns](patterns/pharmacy-benefit-patterns.md) | Rx benefit templates | "5-tier formulary" |
| [specialty-distribution-pattern](patterns/specialty-distribution-pattern.md) | Specialty models | "white bagging program" |

### Integration Skills (Cross-Product)

| Skill | Source Product | Purpose |
|-------|---------------|---------|
| [provider-for-encounter](integration/provider-for-encounter.md) | PatientSim, TrialSim | Generate provider for encounter |
| [network-for-member](integration/network-for-member.md) | MemberSim | Determine network status |
| [pharmacy-for-rx](integration/pharmacy-for-rx.md) | RxMemberSim | Route prescription |
| [benefit-for-claim](integration/benefit-for-claim.md) | MemberSim | Calculate cost sharing |
| [formulary-for-rx](integration/formulary-for-rx.md) | RxMemberSim | Determine coverage |

---

## Common Workflows

### Workflow 1: Provider for Clinical Encounter

Generate appropriate providers for PatientSim encounters based on diagnosis and procedures.

```
┌─────────────────┐     ┌──────────────────────┐     ┌─────────────────┐
│   PatientSim    │     │   Provider for       │     │   Provider      │
│   Encounter     │────▶│   Encounter Skill    │────▶│   Entity        │
│   - Diagnosis   │     │   - Match specialty  │     │   - NPI         │
│   - Procedures  │     │   - Assign role      │     │   - Taxonomy    │
│   - Location    │     │   - Generate entity  │     │   - Credentials │
└─────────────────┘     └──────────────────────┘     └─────────────────┘
```

**Example**:
```
Input: Heart failure admission (I50.9) in Houston
Output: Attending cardiologist (207RC0000X) with FACC credentials
```

**Specialty Matching Logic**:
- I20-I25 (Ischemic Heart Disease) → Cardiology
- C00-C97 (Malignant Neoplasms) → Oncology
- M00-M99 (Musculoskeletal) → Orthopedics
- N18 (Chronic Kidney Disease) → Nephrology

### Workflow 2: Network Status for Member Claims

Determine network status and apply tier-based cost sharing for MemberSim claims.

```
┌─────────────────┐     ┌──────────────────────┐     ┌─────────────────┐
│   MemberSim     │     │   Network for        │     │   Network       │
│   Claim         │────▶│   Member Skill       │────▶│   Status +      │
│   - Provider    │     │   - Check roster     │     │   Cost Sharing  │
│   - Plan        │     │   - Determine tier   │     │   - Tier        │
│   - Service     │     │   - Get cost share   │     │   - Copay/Coins │
└─────────────────┘     └──────────────────────┘     └─────────────────┘
```

**Status Outcomes**:
- IN_NETWORK: Apply in-network cost sharing
- OUT_OF_NETWORK (PPO): Apply OON cost sharing, balance billing
- OUT_OF_NETWORK (HMO): Deny (except emergency)
- TIERED: Apply tier-specific cost sharing

### Workflow 3: Pharmacy Routing for Prescriptions

Route RxMemberSim prescriptions to appropriate pharmacy type.

```
┌─────────────────┐     ┌──────────────────────┐     ┌─────────────────┐
│   RxMemberSim   │     │   Pharmacy for       │     │   Pharmacy      │
│   Prescription  │────▶│   Rx Skill           │────▶│   Assignment    │
│   - Drug/NDC    │     │   - Check specialty  │     │   - NCPDP ID    │
│   - Days supply │     │   - Route by rules   │     │   - Type        │
│   - Member prefs│     │   - Apply network    │     │   - Services    │
└─────────────────┘     └──────────────────────┘     └─────────────────┘
```

**Routing Rules**:
- Specialty indicator = true → Specialty pharmacy
- Days supply ≥ 90 + maintenance → Mail order
- REMS required → Certified pharmacy only
- Default → Preferred retail network

### Workflow 4: Site and Investigator for Clinical Trials

Generate trial site facilities and investigators for TrialSim studies.

```
┌─────────────────┐     ┌──────────────────────┐     ┌─────────────────┐
│   TrialSim      │     │   Provider for       │     │   Site +        │
│   Protocol      │────▶│   Encounter          │────▶│   Investigator  │
│   - Indication  │     │   (Trial context)    │     │   - Facility    │
│   - Phase       │     │   - Match expertise  │     │   - PI NPI      │
│   - Requirements│     │   - Academic/community│    │   - Credentials │
└─────────────────┘     └──────────────────────┘     └─────────────────┘
```

**Site Selection Logic**:
- Phase 1: Academic medical center, experienced PI
- Phase 2-3: Mix of academic and community sites
- Rare disease: Centers of Excellence
- Geographic distribution based on population

---

## Output Formats

### Provider Entity (Canonical JSON)

```json
{
  "npi": "1234567890",
  "entity_type": "individual",
  "enumeration_date": "2010-05-15",
  
  "provider": {
    "last_name": "Chen",
    "first_name": "Michael",
    "middle_name": "Wei",
    "name_prefix": "Dr.",
    "name_suffix": null,
    "credential": "MD, FACC",
    "gender": "M"
  },
  
  "taxonomy": {
    "primary": {
      "code": "207RC0000X",
      "classification": "Internal Medicine",
      "specialization": "Cardiovascular Disease",
      "license_state": "TX",
      "license_number": "TX12345"
    },
    "secondary": [
      {
        "code": "207RI0011X",
        "classification": "Internal Medicine",
        "specialization": "Interventional Cardiology"
      }
    ]
  },
  
  "practice_location": {
    "address_line_1": "6550 Fannin Street",
    "address_line_2": "Suite 1800",
    "city": "Houston",
    "state": "TX",
    "zip": "77030",
    "zip_plus_4": "2717",
    "county_fips": "48201",
    "phone": "713-555-0123",
    "fax": "713-555-0124"
  },
  
  "organization_affiliation": {
    "organization_npi": "1987654320",
    "organization_name": "Houston Heart Associates",
    "role": "Partner"
  },
  
  "hospital_privileges": [
    {
      "facility_name": "Houston Methodist Hospital",
      "ccn": "450358"
    }
  ],
  
  "board_certifications": [
    {
      "board": "American Board of Internal Medicine",
      "specialty": "Cardiovascular Disease",
      "initial_certification": "2008",
      "expiration": "2028"
    }
  ]
}
```

### Facility Entity (Canonical JSON)

```json
{
  "ccn": "450358",
  "npi": "1234567890",
  
  "facility": {
    "name": "Houston Methodist Hospital",
    "doing_business_as": "Houston Methodist",
    "type": "Short Term Acute Care Hospital",
    "type_code": "STAC",
    "subtype": "General Medical and Surgical",
    "ownership": "Voluntary Nonprofit - Church",
    "ownership_code": "02"
  },
  
  "characteristics": {
    "bed_count": 907,
    "staffed_beds": 850,
    "icu_beds": 120,
    "emergency_department": true,
    "trauma_level": "Level I",
    "teaching_hospital": true,
    "medical_school_affiliation": "Weill Cornell Medicine"
  },
  
  "services": {
    "cardiac_surgery": true,
    "cardiac_cath_lab": true,
    "transplant_center": ["Heart", "Kidney", "Liver"],
    "stroke_certification": "Comprehensive Stroke Center",
    "oncology_certification": "NCI Comprehensive Cancer Center"
  },
  
  "location": {
    "address_line_1": "6565 Fannin Street",
    "city": "Houston",
    "state": "TX",
    "zip": "77030",
    "county_fips": "48201",
    "phone": "713-790-3311"
  },
  
  "accreditation": [
    {"body": "The Joint Commission", "status": "Accredited"},
    {"body": "Magnet Recognition", "status": "Designated"}
  ]
}
```

### Pharmacy Entity (Canonical JSON)

```json
{
  "ncpdp_id": "3456789",
  "npi": "1876543210",
  
  "pharmacy": {
    "name": "CVS Pharmacy #4521",
    "doing_business_as": "CVS Pharmacy",
    "type": "Community/Retail Pharmacy",
    "type_code": "01",
    "chain_code": "CVS",
    "dispensing_class": "Retail"
  },
  
  "specialty": {
    "specialty_pharmacy": false,
    "mail_order": false,
    "compounding": true,
    "compounding_sterile": false,
    "long_term_care": false,
    "home_infusion": false
  },
  
  "services": {
    "immunizations": true,
    "mtm": true,
    "point_of_care_testing": true,
    "drive_through": true,
    "24_hour": false
  },
  
  "hours": {
    "monday": "08:00-21:00",
    "tuesday": "08:00-21:00",
    "wednesday": "08:00-21:00",
    "thursday": "08:00-21:00",
    "friday": "08:00-21:00",
    "saturday": "09:00-18:00",
    "sunday": "10:00-17:00"
  },
  
  "location": {
    "address_line_1": "123 Main Street",
    "city": "Chicago",
    "state": "IL",
    "zip": "60601",
    "county_fips": "17031",
    "phone": "312-555-0123",
    "fax": "312-555-0124"
  },
  
  "network_participation": [
    {"network_id": "ESI-PREFERRED-2024", "tier": "Preferred"},
    {"network_id": "CVS-CAREMARK-STD", "tier": "Standard"}
  ]
}
```

### Network Entity (Canonical JSON)

```json
{
  "network_id": "NET-TX-PPO-2024",
  
  "network": {
    "name": "Blue Cross Blue Shield of Texas PPO",
    "type": "PPO",
    "geography": {
      "states": ["TX"],
      "metro_areas": ["Houston", "Dallas", "Austin", "San Antonio"]
    }
  },
  
  "configuration": {
    "tiered": false,
    "tier_count": 2,
    "tiers": [
      {"tier_id": "IN-NETWORK", "tier_level": 1},
      {"tier_id": "OUT-OF-NETWORK", "tier_level": 2}
    ],
    "out_of_network_coverage": true,
    "balance_billing_allowed": true
  },
  
  "adequacy": {
    "pcp_count": 4500,
    "specialist_count": 8200,
    "hospital_count": 185,
    "pharmacy_count": 3200,
    "meets_state_requirements": true
  },
  
  "cost_sharing": {
    "in_network": {
      "deductible_individual": 1500,
      "deductible_family": 3000,
      "coinsurance": 0.20,
      "oop_max_individual": 6000,
      "oop_max_family": 12000
    },
    "out_of_network": {
      "deductible_individual": 3000,
      "deductible_family": 6000,
      "coinsurance": 0.40,
      "oop_max_individual": 12000,
      "oop_max_family": 24000
    }
  }
}
```

---

## Integration Points

### To PatientSim

NetworkSim provides structural entities for clinical encounters:

**Provider for Encounter**:
```json
{
  "encounter": {
    "attending_provider": {
      "npi": "1234567890",
      "name": "Dr. Michael Chen, MD",
      "specialty": "Cardiovascular Disease"
    }
  }
}
```

**FHIR Mapping**:
```json
{
  "Encounter": {
    "participant": [
      {
        "type": [{"coding": [{"code": "ATND", "display": "attender"}]}],
        "individual": {"reference": "Practitioner/1234567890"}
      }
    ]
  }
}
```

### To MemberSim

NetworkSim provides network context for claims adjudication:

**Network Status for Claim**:
```json
{
  "claim": {
    "network_context": {
      "provider_status": "IN_NETWORK",
      "tier": "Tier 1",
      "contracted_rate": 150.00,
      "network_discount": 50.00
    }
  }
}
```

**X12 835 Mapping**:
```json
{
  "835": {
    "CLP": {"claim_status": "1"},
    "CAS": [
      {"group": "CO", "reason": "45", "amount": 50.00}
    ]
  }
}
```

### To RxMemberSim

NetworkSim provides pharmacy and formulary context:

**Pharmacy for Prescription**:
```json
{
  "prescription": {
    "dispensing_pharmacy": {
      "ncpdp_id": "3456789",
      "pharmacy_type": "Retail",
      "network_tier": "Preferred"
    }
  }
}
```

**Formulary Context**:
```json
{
  "claim": {
    "formulary": {
      "tier": 2,
      "tier_name": "Preferred Brand",
      "copay": 35.00,
      "prior_auth_required": false,
      "step_therapy_required": false
    }
  }
}
```

### To TrialSim

NetworkSim provides site and investigator entities:

**Trial Site**:
```json
{
  "site": {
    "facility": {
      "ccn": "450358",
      "name": "Houston Methodist Hospital",
      "type": "Academic Medical Center"
    },
    "principal_investigator": {
      "npi": "1234567890",
      "name": "Dr. Katherine Sullivan, MD, PhD",
      "specialty": "Medical Oncology"
    }
  }
}
```

### From PopulationSim

PopulationSim provides geographic context for network generation:

**Geographic Context**:
```json
{
  "geography": {
    "county_fips": "48201",
    "county_name": "Harris County",
    "population": 4731145,
    "urban_rural": "Urban",
    "hpsa_designation": null,
    "provider_ratio": {
      "pcp_per_100k": 72.5,
      "specialist_per_100k": 145.2
    }
  }
}
```

**Use for Network Adequacy**:
- Population density determines provider counts
- HPSA status indicates underserved areas
- Urban/rural affects time-distance standards
- Demographics influence specialty mix

---

## Best Practices

### 1. Be Specific About Geography

Include city, county, or state for realistic provider generation.

✅ **Good**:
```
Generate a cardiologist in Harris County, Texas
```

❌ **Avoid**:
```
Generate a cardiologist in Texas
```

**Why**: Specific geography produces realistic addresses, phone numbers, hospital affiliations, and county FIPS codes.

### 2. Specify Specialty When Relevant

Use specific specialty names that map to NUCC taxonomy codes.

✅ **Good**:
```
Generate an interventional cardiologist
```

❌ **Avoid**:
```
Generate a heart doctor
```

**Why**: Specific specialties map to correct taxonomy codes (207RC0001X vs 207RC0000X) and appropriate credentials (FSCAI).

### 3. Include Context for Integration

Provide encounter/claim context when generating for other products.

✅ **Good**:
```
Generate a provider for this heart failure patient's cardiology referral
[Include patient diagnosis, location]
```

❌ **Avoid**:
```
Generate a provider
```

**Why**: Context enables matching specialty to diagnosis, geography to patient, and appropriate credentials.

### 4. Request Specific Output When Needed

Ask for specific fields if you need them.

✅ **Good**:
```
Generate a provider with full taxonomy codes and board certifications
```

❌ **Avoid**:
```
Generate a provider
```

**Why**: Default output may omit optional fields like secondary taxonomies or hospital privileges.

### 5. Use Reference Skills First

Understand concepts before generating data.

✅ **Good**:
```
1. "Explain specialty pharmacy concepts"
2. "Generate a specialty pharmacy for oncology"
```

❌ **Avoid**:
```
Jump straight to "generate specialty pharmacy"
```

**Why**: Understanding concepts produces better prompts and more realistic output.

### 6. Validate Generated Data

Check key fields for format correctness.

**Validation Checklist**:
- NPI: 10 digits, passes Luhn check
- Taxonomy: Valid NUCC code
- CCN: 6 characters, correct prefix for state/type
- NCPDP: 7 digits
- FIPS: 5 digits (2 state + 3 county)

### 7. Use Consistent Entity References

When generating related entities, maintain consistency.

✅ **Good**:
```
Generate 3 cardiologists affiliated with Houston Methodist Hospital
[Reference the same CCN across all]
```

**Why**: Maintains referential integrity across entities.

### 8. Consider Network Constraints

Generate entities appropriate for the network type.

✅ **Good**:
```
Generate an HMO network with capitated PCPs
[Include panel size, referral requirements]
```

**Why**: Network type affects provider relationships and compensation models.

---

## Troubleshooting

### Common Issues

| Issue | Cause | Resolution |
|-------|-------|------------|
| Missing taxonomy code | Specialty not recognized | Use NUCC taxonomy lookup, check spelling |
| Invalid NPI format | Not 10 digits or fails Luhn | NPIs are always 10 digits with checksum |
| County not found | Misspelled or wrong state | Use 5-digit FIPS code instead of name |
| Unrealistic address | Generic city name | Specify county or ZIP for better results |
| Wrong facility type | Ambiguous request | Use specific type (STAC, CAH, LTACH) |
| Network mismatch | Provider not in network | Check network roster effective dates |

### Validation Errors

| Error | Resolution |
|-------|------------|
| "NPI check digit invalid" | Regenerate NPI with correct Luhn checksum |
| "Taxonomy code not found" | Verify code in NUCC taxonomy codeset |
| "CCN format invalid" | Check state prefix and facility type range |
| "FIPS code not found" | Verify against Census Bureau FIPS list |

### Integration Issues

| Issue | Resolution |
|-------|------------|
| Specialty doesn't match diagnosis | Use diagnosis-to-specialty mapping from provider-for-encounter |
| Network status incorrect | Verify effective dates on network roster |
| Cost sharing wrong | Check service type and tier for correct cost sharing |
| Pharmacy type mismatch | Verify specialty indicator and routing rules |

---

## Related Documentation

- [SKILL.md](SKILL.md) - Main skill reference with routing
- [Prompt Guide](prompt-guide.md) - Example prompts by category
- [README](README.md) - Product overview
- [Reference Skills](reference/) - Concept explanations
- [Synthetic Skills](synthetic/) - Entity generation
- [Integration Skills](integration/) - Cross-product workflows
- [HealthSim Architecture](../../docs/HEALTHSIM-ARCHITECTURE-GUIDE.md) - Overall architecture

---

*NetworkSim Developer Guide v1.0 - December 2024*
