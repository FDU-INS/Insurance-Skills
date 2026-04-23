# HealthSim Generative Framework - Conceptual Architecture

## Executive Summary

The Generative Framework introduces a **specification-driven** approach to data generation that complements (not replaces) the existing **cohort-based** persistence model.

**Key Distinction:**
- **Cohorts** = WHERE entities are saved (persistence)
- **Profiles + Journeys** = WHAT and HOW entities are generated (specification)

These are complementary layers that work together.

---

## The Two Layers

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        SPECIFICATION LAYER (NEW)                            │
│                                                                             │
│   "Define WHAT you want"                                                    │
│                                                                             │
│   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                    │
│   │   Profile   │    │   Journey   │    │  Template   │                    │
│   │    Spec     │───▶│    Spec     │◀───│   Library   │                    │
│   └─────────────┘    └─────────────┘    └─────────────┘                    │
│         │                   │                                               │
│         └─────────┬─────────┘                                               │
│                   ▼                                                         │
│            ┌─────────────┐                                                  │
│            │  Executor   │                                                  │
│            │  (Profile + │                                                  │
│            │   Journey)  │                                                  │
│            └─────────────┘                                                  │
│                   │                                                         │
└───────────────────│─────────────────────────────────────────────────────────┘
                    │ Generates entities
                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        PERSISTENCE LAYER (EXISTING)                         │
│                                                                             │
│   "Store WHERE entities live"                                               │
│                                                                             │
│   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                    │
│   │  Cohort   │    │   State     │    │   DuckDB    │                    │
│   │   Manager   │───▶│   Manager   │───▶│  Database   │                    │
│   └─────────────┘    └─────────────┘    └─────────────┘                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Component Glossary

### Specification Layer Components

| Component | What It Is | Analogy |
|-----------|------------|---------|
| **Profile** | Population characteristics (who) | A casting call - "We need 100 people, age 65-85, with diabetes" |
| **Journey** | Event sequence over time (what happens) | A script - "Day 1: diagnosis, Day 30: follow-up, Day 90: labs" |
| **Distribution** | Statistical patterns for attributes | A recipe - "68% normal weight, 25% overweight, 7% obese" |
| **Template** | Pre-built profile or journey | A form letter - fill in the blanks |
| **Builder** | Conversational specification tool | An interview - "Tell me about your population" |
| **Executor** | Specification → Entities | The factory - takes the blueprint, produces the product |

### Persistence Layer Components (Existing)

| Component | What It Is | Analogy |
|-----------|------------|---------|
| **Cohort** | Named collection of entities | A filing cabinet drawer |
| **State Manager** | Save/load/query interface | The file clerk |
| **DuckDB** | Persistent storage | The warehouse |

---

## How Components Work Together

### 1. Profile Specification

A Profile defines **who** you're generating - demographics, clinical characteristics, coverage:

```
┌─────────────────────────────────────────────────────────────────┐
│                      PROFILE SPECIFICATION                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Demographics          Clinical              Coverage            │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐     │
│  │ count: 100   │     │ primary:     │     │ plan_type:   │     │
│  │ age: Normal  │     │   E11.9 DM   │     │   MA-HMO 35% │     │
│  │   μ=72, σ=8  │     │              │     │   MA-PPO 25% │     │
│  │ gender:      │     │ comorbid:    │     │   Orig  40%  │     │
│  │   M 48%      │     │   I10 HTN 78%│     │              │     │
│  │   F 52%      │     │   E78 HLD 65%│     │              │     │
│  └──────────────┘     └──────────────┘     └──────────────┘     │
│                                                                  │
│  Uses: Distributions for sampling                                │
│  Products: PatientSim, MemberSim, RxMemberSim                   │
└─────────────────────────────────────────────────────────────────┘
```

### 2. Distribution Types

Distributions define **how** attribute values are sampled:

```
CATEGORICAL                 NORMAL                    LOG-NORMAL
"Pick from options"         "Bell curve"              "Right-skewed"
                                                      
    ████                         ▄▄█▄▄                    ████▄
    ████ ██                    ▄██████▄                 ▄██████▄▄
    ████ ████ ██             ▄████████▄▄              ████████████▄▄
    ─────────────            ──────────────            ────────────────
    M    F   Other           65  72  79               $0   $150   $1000+
    
Gender, Plan Type          Age, Lab Values           Costs, Utilization


CONDITIONAL                 EXPLICIT
"Depends on other value"    "Specific known values"

If severity='controlled':   ["48453", "48201", "48113"]
  → Normal(6.5, 0.3)        
If severity='uncontrolled': County FIPS codes
  → Normal(9.0, 1.0)        Provider NPIs
                            ZIP codes
```

### 3. Journey Specification

A Journey defines **what happens** over time:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         JOURNEY SPECIFICATION                                │
│                         "Diabetic First Year"                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Timeline: 12 months                                                         │
│  Pattern: Linear with Branching                                              │
│                                                                              │
│  ──●───────────●───────────●───────────●───────────●──────────────▶ time    │
│   Day 0      Day 30      Day 90      Day 180     Day 270                    │
│    │           │           │           │           │                         │
│    ▼           ▼           ▼           ▼           ▼                         │
│  ┌─────┐    ┌─────┐    ┌─────┐    ┌─────┐    ┌─────┐                        │
│  │Visit│    │F/U  │    │Labs │    │Visit│    │Labs │                        │
│  │Labs │    │Visit│    │     │    │Labs │    │     │                        │
│  │Start│    │     │    │     │    │     │    │     │                        │
│  │ Rx  │    │     │    │     │    │     │    │     │                        │
│  └─────┘    └─────┘    └─────┘    └──┬──┘    └─────┘                        │
│                                      │                                       │
│                              ┌───────┴───────┐                               │
│                              │ A1c > 8.0?    │ ◄── BRANCHING                 │
│                              └───────┬───────┘                               │
│                           ┌──────────┴──────────┐                            │
│                          YES (22%)            NO (78%)                       │
│                           │                     │                            │
│                           ▼                     ▼                            │
│                      Add 2nd agent        Continue current                   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 4. Journey Patterns

Different temporal complexity levels:

```
LINEAR                    BRANCHING                 CYCLIC
Simple sequence           Decision points           Repeating events

A ──▶ B ──▶ C ──▶ D      A ──▶ B ─┬─▶ C          ┌──────────────┐
                              │   │               │              │
Annual wellness           └───▶ D             A ──▶ B ──▶ C ────┘
                                              
                         ER → Admit OR           Monthly refills
                              Discharge


PROTOCOL                  LIFECYCLE
Structured visits         Multi-year progression

Cycle 1    Cycle 2       Year 1    Year 5    Year 10
├─D1       ├─D1          │         │         │
├─D8       ├─D8          ▼         ▼         ▼
└─D15      └─D15         Mild ───▶ Mod ────▶ Severe
    └──────────┘
                         Disease progression
Trial protocol
```

### 5. Events and Timing

Events are the atomic units of a Journey:

```
┌─────────────────────────────────────────────────────────────────┐
│                           EVENT                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Type: encounter | lab | prescription | claim | enrollment       │
│                                                                  │
│  Timing:                                                         │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ day: 30           ◄── Relative to journey start          │   │
│  │ variance_days: 7  ◄── ±7 days randomization              │   │
│  │ business_days: true ◄── Skip weekends                    │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  Details (varies by type):                                       │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ encounter_type: "office"                                  │   │
│  │ reason: "Diabetes follow-up"                              │   │
│  │ cpt_codes: ["99214", "83036"]                            │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  Cross-Domain Triggers:                                          │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ generates_claim: true    ◄── MemberSim 837P              │   │
│  │ generates_fill: false                                     │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 6. Cross-Domain Sync

How events propagate across products:

```
                              PATIENT (Identity Anchor)
                                       │
                    SSN: 123-45-6789   │   DOB: 1952-03-15
                                       │
         ┌─────────────────────────────┼─────────────────────────────┐
         │                             │                             │
         ▼                             ▼                             ▼
    ┌─────────┐                  ┌─────────┐                  ┌─────────┐
    │PatientSim│                 │MemberSim│                  │RxMemberSim│
    │         │                  │         │                  │           │
    │Patient  │───────────────▶  │Member   │  ◀───────────────│RxMember   │
    │Encounter│───generates──▶   │Claim    │                  │           │
    │Rx Order │───────────────────────────────generates──────▶│Fill       │
    └─────────┘                  └─────────┘                  └───────────┘
         │
         │ If trial_eligible
         ▼
    ┌─────────┐
    │TrialSim │
    │         │
    │Subject  │
    │Visit    │
    └─────────┘

SYNC RULES:
─────────────────────────────────────────────────────────────────────────
Encounter (office visit)  ──▶  Professional Claim (837P)
Encounter (inpatient)     ──▶  Facility Claim (837I)
Prescription written      ──▶  Pharmacy Fill (NCPDP)
Diagnosis assigned        ──▶  Claim diagnosis codes
Provider on encounter     ──▶  Rendering provider on claim
```

### 7. Templates

Pre-built specifications that can be customized:

```
┌─────────────────────────────────────────────────────────────────┐
│                      TEMPLATE LIBRARY                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  PROFILE TEMPLATES              JOURNEY TEMPLATES                │
│  ─────────────────              ─────────────────                │
│  ┌──────────────────┐          ┌──────────────────┐             │
│  │ medicare-diabetic│          │ diabetic-first-  │             │
│  │ Age 65+, T2DM    │          │ year             │             │
│  │ HTN 78%, HLD 65% │          │ 12 months        │             │
│  └──────────────────┘          └──────────────────┘             │
│                                                                  │
│  ┌──────────────────┐          ┌──────────────────┐             │
│  │ commercial-      │          │ surgical-episode │             │
│  │ healthy          │          │ 3 months         │             │
│  │ Age 22-64, low Rx│          │ Pre-op → Recovery│             │
│  └──────────────────┘          └──────────────────┘             │
│                                                                  │
│  ┌──────────────────┐          ┌──────────────────┐             │
│  │ medicaid-        │          │ new-member-      │             │
│  │ pediatric        │          │ onboarding       │             │
│  │ Age 0-17, SDOH   │          │ 90 days          │             │
│  └──────────────────┘          └──────────────────┘             │
│                                                                  │
│  Usage:                                                          │
│  "Use the medicare-diabetic template for 100 patients"          │
│  "Use commercial-healthy with new-member-onboarding journey"    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 8. Builders and Executors

The two-phase architecture:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           PHASE 1: BUILDING                                  │
│                           (Creative, Conversational)                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  User: "I need 200 Medicare patients with diabetes, mostly in Texas"        │
│                                                                              │
│                                    │                                         │
│                                    ▼                                         │
│                           ┌─────────────────┐                               │
│                           │ Profile Builder │                               │
│                           │                 │                               │
│                           │ 1. Intent       │                               │
│                           │ 2. Scope        │                               │
│                           │ 3. Refine       │                               │
│                           │ 4. Confirm      │                               │
│                           └────────┬────────┘                               │
│                                    │                                         │
│                                    ▼                                         │
│                           ProfileSpecification                               │
│                           (JSON document)                                    │
│                                                                              │
│  + Optional: "Add a first-year diabetes journey"                            │
│                                                                              │
│                                    │                                         │
│                                    ▼                                         │
│                           ┌─────────────────┐                               │
│                           │ Journey Builder │                               │
│                           └────────┬────────┘                               │
│                                    │                                         │
│                                    ▼                                         │
│                           JourneySpecification                               │
│                           (JSON document)                                    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘

                                    │
                                    │ "Execute the profile"
                                    ▼

┌─────────────────────────────────────────────────────────────────────────────┐
│                           PHASE 2: EXECUTION                                 │
│                           (Mechanical, Deterministic)                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────┐         ┌─────────────────┐                            │
│  │Profile Executor │         │Journey Executor │                            │
│  │                 │         │                 │                            │
│  │ 1. Validate     │         │ 1. Expand times │                            │
│  │ 2. Sample dists │         │ 2. Apply variance│                           │
│  │ 3. Generate     │────────▶│ 3. Branch logic │                            │
│  │    entities     │         │ 4. Generate     │                            │
│  │                 │         │    events       │                            │
│  └─────────────────┘         └────────┬────────┘                            │
│                                       │                                      │
│                                       ▼                                      │
│                              ┌─────────────────┐                            │
│                              │Cross-Domain Sync│                            │
│                              │                 │                            │
│                              │ Patient→Member  │                            │
│                              │ Encounter→Claim │                            │
│                              │ Rx→Fill         │                            │
│                              └────────┬────────┘                            │
│                                       │                                      │
│                                       ▼                                      │
│                              Generated Entities                              │
│                              (Patients, Members, Claims, etc.)               │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Journeys vs Cohorts: Complementary, Not Redundant

This is a critical distinction:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│   JOURNEY (Specification)              SCENARIO (Persistence)               │
│   ══════════════════════               ═══════════════════════              │
│                                                                              │
│   WHAT it is:                          WHAT it is:                          │
│   A blueprint for generating           A named collection of                │
│   events over time                     generated entities                   │
│                                                                              │
│   WHEN used:                           WHEN used:                           │
│   Before generation                    After generation                     │
│   (specification phase)                (persistence phase)                  │
│                                                                              │
│   CONTAINS:                            CONTAINS:                            │
│   - Phases                             - Patients                           │
│   - Events                             - Encounters                         │
│   - Timing rules                       - Claims                             │
│   - Branching logic                    - Lab results                        │
│   - Distributions                      - Medications                        │
│                                                                              │
│   EXAMPLE:                             EXAMPLE:                             │
│   "12-month diabetes journey           "diabetes-cohort-2026"               │
│    with quarterly visits"              containing 200 patients              │
│                                                                              │
│   PERSISTENCE:                         PERSISTENCE:                         │
│   Stored as skill/template file        Stored in DuckDB                     │
│   (markdown or JSON)                   (relational tables)                  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘

                              HOW THEY CONNECT:

    ┌───────────────┐    ┌───────────────┐    ┌───────────────┐
    │   Profile     │    │   Journey     │    │   Cohort    │
    │   Spec        │───▶│   Spec        │───▶│   (saved)     │
    └───────────────┘    └───────────────┘    └───────────────┘
          │                    │                    │
          │                    │                    │
          ▼                    ▼                    ▼
    "200 Medicare         "First-year          "medicare-dm-2026"
     diabetics"           diabetes"             in DuckDB
    
                    │                    │
                    └────────┬───────────┘
                             │
                             ▼
                      ┌─────────────┐
                      │  Executor   │
                      │  generates  │
                      │  entities   │
                      └─────────────┘
                             │
                             ▼
                      ┌─────────────┐
                      │State Manager│
                      │   saves to  │
                      │  cohort   │
                      └─────────────┘
```

### The Full Flow

```
1. USER: "I need 200 Medicare diabetics with a first-year journey"

2. PROFILE BUILDER creates:
   ProfileSpecification {
     count: 200,
     demographics: { age: Normal(72, 8), ... },
     clinical: { primary: "E11.9", ... }
   }

3. JOURNEY BUILDER creates:
   JourneySpecification {
     duration: "12 months",
     phases: [ ... ],
     events: [ ... ]
   }

4. USER: "Execute it and save as medicare-dm-cohort"

5. PROFILE EXECUTOR generates:
   - 200 Patient entities
   - 200 Member entities
   - 200 RxMember entities

6. JOURNEY EXECUTOR generates (for each entity):
   - ~4 encounters per patient
   - ~12 lab results per patient
   - ~4 medication fills per patient
   - Corresponding claims for each encounter

7. STATE MANAGER saves:
   Cohort "medicare-dm-cohort" containing:
   - 200 patients
   - 200 members
   - 800 encounters
   - 2,400 lab results
   - 800 fills
   - 800 claims

8. USER (later): "Load my medicare-dm-cohort"
   STATE MANAGER retrieves from DuckDB
```

---

## Integration Points

### How Generative Framework Uses Existing Components

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│   GENERATIVE FRAMEWORK                    EXISTING COMPONENTS               │
│   ════════════════════                    ═══════════════════               │
│                                                                              │
│   Profile Executor ──────────────────────▶ PopulationSim                    │
│   (demographic sampling)                   (real CDC/Census data)           │
│                                                                              │
│   Profile Executor ──────────────────────▶ NetworkSim                       │
│   (provider assignment)                    (real NPI/facility data)         │
│                                                                              │
│   Journey Executor ──────────────────────▶ PatientSim                       │
│   (clinical events)                        (encounter generation)           │
│                                                                              │
│   Journey Executor ──────────────────────▶ MemberSim                        │
│   (claims events)                          (claim generation)               │
│                                                                              │
│   Journey Executor ──────────────────────▶ RxMemberSim                      │
│   (pharmacy events)                        (fill generation)                │
│                                                                              │
│   Cross-Domain Sync ─────────────────────▶ Identity Correlation             │
│   (entity linking)                         (SSN-based linking)              │
│                                                                              │
│   All Executors ─────────────────────────▶ State Manager                    │
│   (saving output)                          (DuckDB persistence)             │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### What's New vs What Existed

| Concept | Before (v1.x) | After (v2.0) |
|---------|---------------|--------------|
| **How you request data** | "Generate a diabetic patient" (imperative) | "Build a profile for 200 diabetics" (declarative) |
| **Batch generation** | Loop and generate one at a time | Define once, execute for N entities |
| **Temporal events** | Manual: "add an encounter on day 30" | Automatic: Journey defines all events |
| **Cross-product** | Manual: "now create a claim for that encounter" | Automatic: Cross-domain sync triggers |
| **Reproducibility** | Random each time | Deterministic from specification |
| **Persistence** | Cohort (same) | Cohort (same - unchanged) |
| **Small requests** | Direct generation | Quick Generate (same UX) |

---

## Quick Reference: When to Use What

| You Want To... | Use This |
|----------------|----------|
| Generate 1-10 entities quickly | Quick Generate (direct) |
| Generate 50+ entities with specific characteristics | Profile Builder → Execute |
| Add temporal events (follow-ups, labs over time) | Journey Builder |
| Start from a common pattern | Templates |
| Save generated data for later | State Manager (Cohorts) |
| Query saved data | State Manager Query |
| Customize statistical patterns | Distribution Types |
| Generate across multiple products | Cross-Domain Sync |

---

## Summary

The Generative Framework adds a **specification layer** on top of the existing **persistence layer**:

1. **Profiles** define WHO (demographics, conditions, coverage)
2. **Distributions** define HOW attributes are sampled
3. **Journeys** define WHAT HAPPENS over time
4. **Events** are atomic timeline units with timing and triggers
5. **Templates** are reusable pre-built specs
6. **Builders** create specs conversationally
7. **Executors** turn specs into entities deterministically
8. **Cohorts** (existing) store the generated entities

**Journeys and Cohorts are complementary:**
- Journey = the recipe (how to generate)
- Cohort = the meal (what was generated)

The framework integrates with all existing products (PatientSim, MemberSim, RxMemberSim, TrialSim) and reference data sources (PopulationSim, NetworkSim) while using the existing State Manager for persistence.
