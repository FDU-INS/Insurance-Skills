# HealthSim Product Architecture

Visual guide to how HealthSim products work together.

---

## Product Relationships

```
                           ┌─────────────────────────────────────────────────────────┐
                           │                    HealthSim Ecosystem                   │
                           └─────────────────────────────────────────────────────────┘
                                                      │
              ┌──────────────────────────────────────┼──────────────────────────────────────┐
              │                                      │                                      │
              ▼                                      ▼                                      ▼
    ┌──────────────────┐                  ┌──────────────────┐                  ┌──────────────────┐
    │   Data Layer     │                  │  Generation      │                  │  Network Layer   │
    │                  │                  │  Products        │                  │                  │
    │  PopulationSim   │─────────────────▶│                  │◀────────────────│   NetworkSim     │
    │                  │  Demographics,   │  PatientSim      │  Providers,     │                  │
    │  • CDC PLACES    │  SDOH, rates     │  MemberSim       │  facilities,    │  • Providers     │
    │  • SVI           │                  │  RxMemberSim     │  pharmacies     │  • Facilities    │
    │  • ADI           │                  │  TrialSim        │                 │  • Pharmacies    │
    │                  │                  │                  │                  │  • Networks      │
    └──────────────────┘                  └──────────────────┘                  └──────────────────┘
```

---

## Data Flow Between Products

### Clinical → Claims → Pharmacy Flow

```
┌───────────────┐      ┌───────────────┐      ┌───────────────┐
│   PatientSim  │─────▶│   MemberSim   │─────▶│  RxMemberSim  │
│               │      │               │      │               │
│  • Encounter  │      │  • Claim      │      │  • Rx Claim   │
│  • Diagnosis  │      │  • Adjudicate │      │  • DUR Check  │
│  • Medication │      │  • Payment    │      │  • Fill       │
└───────────────┘      └───────────────┘      └───────────────┘
       │                      │                      │
       └──────────────────────┴──────────────────────┘
                              │
                    ┌─────────▼─────────┐
                    │    NetworkSim     │
                    │   (Provider NPI)  │
                    └───────────────────┘
```

### Trial Enrollment Flow

```
┌───────────────┐      ┌───────────────┐
│   PatientSim  │─────▶│   TrialSim    │
│               │      │               │
│  • Patient    │      │  • Subject    │
│  • History    │      │  • Consent    │
│  • Baseline   │      │  • Randomize  │
│               │      │  • SDTM       │
└───────────────┘      └───────────────┘
       ▲                      ▲
       │                      │
┌──────┴──────┐      ┌────────┴────────┐
│PopulationSim│      │   NetworkSim    │
│ (Diversity) │      │ (Investigator)  │
└─────────────┘      └─────────────────┘
```

---

## Identity Correlation

```
                    ┌─────────────────────────────────────┐
                    │               Person                │
                    │  (SSN as universal correlator)      │
                    └─────────────────────────────────────┘
                                     │
         ┌───────────────┬───────────┼───────────┬───────────────┐
         │               │           │           │               │
         ▼               ▼           ▼           ▼               ▼
    ┌─────────┐    ┌─────────┐ ┌─────────┐ ┌─────────┐    ┌─────────┐
    │ Patient │    │ Member  │ │RxMember │ │ Subject │    │ Patient │
    │  (MRN)  │    │(Member  │ │(Cardholder│ │(Subject │    │ (MRN)   │
    │         │    │   ID)   │ │   ID)   │ │   ID)   │    │         │
    └─────────┘    └─────────┘ └─────────┘ └─────────┘    └─────────┘
         │               │           │           │               │
    PatientSim     MemberSim   RxMemberSim   TrialSim      PatientSim
```

---

## Product Capabilities Matrix

| Need | Primary Product | Supporting Products |
|------|----------------|---------------------|
| Patient demographics | PatientSim | PopulationSim (real data) |
| Clinical encounters | PatientSim | NetworkSim (providers) |
| Lab results | PatientSim | - |
| Medication orders | PatientSim | RxMemberSim (fills) |
| Professional claims | MemberSim | PatientSim (encounter), NetworkSim (provider) |
| Facility claims | MemberSim | PatientSim (admission), NetworkSim (facility) |
| Pharmacy claims | RxMemberSim | PatientSim (medication), NetworkSim (pharmacy) |
| Trial subjects | TrialSim | PatientSim (baseline), PopulationSim (diversity) |
| SDTM domains | TrialSim | - |
| Provider entities | NetworkSim | - |
| Population statistics | PopulationSim | - |

---

## Common Workflows

### 1. Simple Patient Generation
```
User Request → PatientSim → JSON/FHIR output
```

### 2. Patient with Claims
```
User Request → PatientSim → MemberSim → X12/JSON output
                   ↓
              NetworkSim (provider)
```

### 3. Complete Care Episode
```
User Request → PatientSim (admission)
                   ↓
              MemberSim (facility claim)
                   ↓
              PatientSim (discharge)
                   ↓
              RxMemberSim (Rx fills)
                   ↓
              MemberSim (follow-up claim)
```

### 4. Data-Driven Population
```
User Request (with geography)
     ↓
PopulationSim (lookup real data)
     ↓
PatientSim/MemberSim/RxMemberSim (apply rates)
     ↓
Output with provenance
```

### 5. Clinical Trial Data
```
User Request
     ↓
TrialSim (study definition)
     ↓
PatientSim → TrialSim (subjects with baseline)
     ↓
TrialSim (visits, AEs, efficacy)
     ↓
SDTM/ADaM output
```

---

## Output Format by Product

| Product | Native Output | Healthcare Standards |
|---------|--------------|---------------------|
| PatientSim | JSON | FHIR R4, HL7v2, C-CDA |
| MemberSim | JSON | X12 837/835/834/270/271 |
| RxMemberSim | JSON | NCPDP D.0 |
| TrialSim | JSON | CDISC SDTM, CDISC ADaM |
| PopulationSim | JSON | CohortSpecification |
| NetworkSim | JSON | - |

---

## See Also

- [Main README](../README.md) - "I Want To..." navigation
- [Architecture Guide](HEALTHSIM-ARCHITECTURE-GUIDE.md) - Detailed architecture
- [Cross-Product Integration](HEALTHSIM-ARCHITECTURE-GUIDE.md#83-cross-product-integration) - Integration patterns
- [Examples](../hello-healthsim/examples/) - Working examples by product
