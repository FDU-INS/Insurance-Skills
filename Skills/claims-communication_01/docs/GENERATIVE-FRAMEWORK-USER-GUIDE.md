# HealthSim Generative Framework User Guide

**Version**: 1.0  
**Last Updated**: January 2026  
**Status**: Reference Documentation

---

## Executive Summary

The **Generative Framework** is HealthSim's core engine for producing realistic synthetic healthcare data at scale. It transforms conversational requests into structured specifications, then executes those specifications deterministically to generate data across all HealthSim products.

**Key Insight**: The framework separates *creative specification* (conversational, flexible) from *mechanical execution* (deterministic, reproducible). This allows users to describe what they need in natural language while ensuring the same specification always produces the same data.

---

## Part 1: Conceptual Foundation

### 1.1 The "Why" - Design Philosophy

Healthcare data generation presents a unique challenge: users need data that is simultaneously **realistic** (statistically valid, clinically coherent) and **reproducible** (same inputs yield same outputs). The Generative Framework solves this by implementing a two-phase architecture:

```
┌─────────────────────────────────────────────────────────────────┐
│                      USER CONVERSATION                          │
│  "Generate 200 Medicare diabetic patients with first year      │
│   of care in Texas, including claims and prescriptions"        │
└─────────────────────────────────┬───────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│              PHASE 1: SPECIFICATION BUILDING                    │
│                                                                 │
│  • Profile Builder interprets demographics, conditions         │
│  • Journey Builder structures temporal events                  │
│  • Claude asks clarifying questions                            │
│  • Output: Validated JSON specification                        │
│                                                                 │
│  Character: Creative, conversational, AI-assisted              │
└─────────────────────────────────┬───────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│              PHASE 2: DETERMINISTIC EXECUTION                   │
│                                                                 │
│  • Profile Executor generates entities from spec               │
│  • Journey Engine creates timelines                            │
│  • Handlers produce product-specific events                    │
│  • Triggers coordinate cross-product generation                │
│                                                                 │
│  Character: Mechanical, deterministic, Python-based            │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Core Concepts

#### Profile

A **Profile** defines *who* you're generating—the population characteristics that entities should have. Profiles specify:

- **Demographics**: Age distribution, gender mix, geographic location
- **Clinical**: Conditions, severity, comorbidity patterns
- **Coverage**: Insurance type, plan mix, benefit structure

Think of a profile as answering: "What does this population look like?"

#### Journey

A **Journey** defines *what happens over time*—the sequence of events that entities experience. Journeys specify:

- **Events**: Encounters, labs, prescriptions, claims
- **Timing**: When events occur, delays between events
- **Conditions**: Branching logic based on outcomes
- **Triggers**: Cross-product event coordination

Think of a journey as answering: "What happens to this person?"

#### Cohort

A **Cohort** is the result of applying a Profile (and optionally a Journey) to generate a group of entities. The term "cohort" replaced the earlier term "scenario" to better align with healthcare terminology where cohorts are groups of individuals sharing common characteristics.

**Terminology Evolution**:
```
Scenario (legacy) → Cohort (current)

A cohort encapsulates:
  - Profile specification (population characteristics)
  - Journey specification (event sequences)  
  - Generated entities (patients, members, etc.)
  - State for persistence/resumption
```

### 1.3 The Generation Hierarchy

```
Cohort
├── Profile Specification
│   ├── Demographics Spec
│   │   ├── Age Distribution
│   │   ├── Gender Distribution
│   │   └── Geography Reference
│   ├── Clinical Spec
│   │   ├── Primary Condition
│   │   ├── Comorbidities
│   │   └── Severity Distribution
│   └── Coverage Spec
│       ├── Plan Type Distribution
│       └── Benefit Structure
│
├── Journey Specification
│   ├── Phases
│   │   ├── Event Definitions
│   │   ├── Timing (Delays)
│   │   └── Conditions (Branching)
│   └── Cross-Domain Triggers
│
└── Generated Entities
    ├── PatientSim: Patients, Encounters, Labs
    ├── MemberSim: Members, Claims, Eligibility
    ├── RxMemberSim: Prescriptions, Fills, Adherence
    └── TrialSim: Subjects, Visits, Assessments
```

---

## Part 2: Framework Components

### 2.1 Distributions

Distributions are the building blocks for generating realistic attribute values. Each distribution type models a different statistical pattern:

| Distribution | Use Case | Example |
|-------------|----------|---------|
| **Categorical** | Discrete choices with weights | Gender: {M: 48%, F: 52%} |
| **Normal** | Bell curve around a mean | Age: mean=72, std=8 |
| **Log-Normal** | Right-skewed positive values | Claim amount: median=$250 |
| **Uniform** | Equal probability across range | Day of month: 1-28 |
| **Age Band** | Healthcare age groupings | {18-34: 20%, 35-54: 35%, 55+: 45%} |
| **Truncated Normal** | Normal with hard bounds | BP: mean=120, bounds=[80,200] |
| **Explicit** | Exact list of values | States: ["TX", "CA", "FL"] |
| **Conditional** | Value depends on other attributes | If age≥65: Medicare eligible |

**Implementation**: `healthsim.generation.distributions`

```python
from healthsim.generation import NormalDistribution, CategoricalDistribution

# Age distribution
age_dist = NormalDistribution(mean=72, std_dev=8, min_value=65, max_value=95)

# Gender distribution  
gender_dist = CategoricalDistribution(weights={"M": 0.48, "F": 0.52})
```

### 2.2 Profile Schema

The Profile Schema defines the structure for population specifications. Key components:

```python
ProfileSpecification
├── id: str                    # Unique identifier
├── name: str                  # Human-readable name
├── version: str               # Schema version
├── generation: GenerationSpec
│   ├── count: int            # Number to generate (1-10,000)
│   ├── products: list        # Target products
│   ├── seed: int | None      # For reproducibility
│   └── validation: str       # "strict" | "warn" | "none"
├── demographics: DemographicsSpec
│   ├── age: DistributionSpec
│   ├── gender: DistributionSpec
│   └── geography: GeographyReference | None
├── clinical: ClinicalSpec | None
│   ├── primary_condition: ConditionSpec
│   ├── comorbidities: list[ConditionSpec]
│   └── severity: DistributionSpec
├── coverage: CoverageSpec | None
│   ├── type: str             # Medicare, Commercial, etc.
│   └── plan_distribution: DistributionSpec
└── outputs: OutputSpec
```

**Implementation**: `healthsim.generation.profile_schema`

### 2.3 Profile Executor

The Profile Executor transforms a ProfileSpecification into generated entities:

```python
from healthsim.generation import ProfileExecutor, execute_profile

# Create executor with seed for reproducibility
executor = ProfileExecutor(seed=42)

# Execute profile
result = executor.execute(profile_spec)

# Result contains:
# - entities: list of GeneratedEntity
# - validation: ValidationReport
# - metadata: execution statistics
```

**Key Features**:
- **Hierarchical Seeding**: Each entity gets a deterministic child seed, so adding/removing entities doesn't affect others
- **Validation**: Checks generated data against profile constraints
- **Progress Tracking**: Callbacks for monitoring batch generation

**Implementation**: `healthsim.generation.profile_executor`

### 2.4 Journey Engine

The Journey Engine orchestrates temporal event sequences. It consists of:

#### Timeline

A timeline is an instantiated journey for a specific entity:

```python
Timeline
├── entity_id: str           # The patient/member this timeline belongs to
├── start_date: date         # When the journey begins
├── events: list[TimelineEvent]
│   ├── event_type: EventType
│   ├── timestamp: datetime
│   ├── status: EventStatus
│   ├── data: dict          # Event-specific payload
│   └── triggered_by: str | None  # Source event if triggered
└── metadata: dict
```

#### Event Types

Events are categorized by product domain:

| Domain | Event Types |
|--------|------------|
| **PatientSim** | ADT_A01 (Admit), ADT_A03 (Discharge), ORU_R01 (Lab Result), RDE_O11 (Rx Order) |
| **MemberSim** | Enrollment, Termination, PlanChange, Claim837P, Claim837I |
| **RxMemberSim** | NewRx, Fill, Refill, Reversal, PARequest, TherapyStart |
| **TrialSim** | Screening, Randomization, ProtocolVisit, AdverseEvent, SAE |

#### Event Conditions

Events can have conditions that determine if they execute:

```python
EventCondition
├── condition_type: ConditionType  # "attribute", "random", "prior_event"
├── attribute: str | None          # For attribute checks
├── operator: str | None           # "eq", "gt", "lt", "in", etc.
├── value: any                     # Comparison value
└── probability: float | None      # For random conditions
```

**Implementation**: `healthsim.generation.journey_engine`

### 2.5 Product Handlers

Handlers translate generic events into product-specific data. Each product has its own handler class:

| Handler | Responsibilities |
|---------|-----------------|
| **PatientSimHandlers** | Generate ADT events, encounters, labs, diagnoses, procedures |
| **MemberSimHandlers** | Generate claims, enrollment transactions, quality events |
| **RxMemberSimHandlers** | Generate prescriptions, fills, adherence events, DUR alerts |
| **TrialSimHandlers** | Generate protocol visits, assessments, safety events |

**Example Handler Registration**:

```python
from healthsim.generation import JourneyEngine, PatientSimHandlers

# Create engine and handlers
engine = JourneyEngine(seed=42)
handlers = PatientSimHandlers(seed=42)

# Register handlers
handlers.register_with_engine(engine)

# Now engine can process PatientSim events
```

**Implementation**: `healthsim.generation.handlers`

### 2.6 Cross-Product Triggers

Triggers coordinate events across products. When an event in one domain fires, it can trigger events in other domains:

```
PatientSim Event                    MemberSim Event
┌──────────────┐    Trigger        ┌──────────────────┐
│ ADT_A03      │ ─────────────────>│ Claim837I        │
│ (Discharge)  │    2-7 day delay  │ (Facility Claim) │
└──────────────┘                   └──────────────────┘

PatientSim Event                    RxMemberSim Event
┌──────────────┐    Trigger        ┌──────────────────┐
│ RDE_O11      │ ─────────────────>│ NewRx + Fill     │
│ (Rx Order)   │    0-2 day delay  │ (Pharmacy)       │
└──────────────┘                   └──────────────────┘
```

**Implementation**: `healthsim.generation.triggers`

```python
from healthsim.generation import CrossProductCoordinator, create_coordinator

# Create coordinator with default triggers
coordinator = create_coordinator(seed=42)

# Register product engines
coordinator.register_product_engine("patientsim", patient_engine)
coordinator.register_product_engine("membersim", member_engine)

# Execute coordinated generation
result = coordinator.execute_coordinated(linked_entity)
```

### 2.7 Cross-Domain Synchronization

The Cross-Domain Sync module handles identity correlation and event coordination:

```python
CrossDomainSync
├── IdentityRegistry
│   ├── PersonIdentity        # Core person identity
│   ├── patient_id           # PatientSim ID
│   ├── member_id            # MemberSim ID  
│   ├── rx_member_id         # RxMemberSim ID
│   └── subject_id           # TrialSim ID
├── TriggerSpecs              # Cross-product trigger definitions
└── SyncReport                # Coordination results
```

**Key Insight**: The same real-world person may have different IDs in different systems. The IdentityRegistry maintains the correlation so that patient John Smith (MRN: PAT-12345) is correctly linked to member John Smith (Member ID: MEM-67890) when generating cross-product data.

**Implementation**: `healthsim.generation.cross_domain_sync`

---

## Part 3: Integration Architecture

### 3.1 Integration with Canonical Data Model

The Generative Framework produces entities that conform to HealthSim's canonical data model:

```
Generation Framework          Canonical Model            Format Serializers
┌──────────────────┐         ┌──────────────────┐       ┌──────────────────┐
│ ProfileExecutor  │────────>│ Person           │──────>│ FHIR R4          │
│ JourneyEngine    │         │ ├── PersonName   │       │ HL7v2 ADT        │
│ ProductHandlers  │         │ ├── Address      │       │ X12 834/837      │
└──────────────────┘         │ └── ContactInfo  │       │ NCPDP D.0        │
                             │                  │       │ CDISC SDTM       │
                             │ Encounter        │       └──────────────────┘
                             │ ├── Diagnoses    │
                             │ ├── Procedures   │
                             │ └── Observations │
                             │                  │
                             │ Claim            │
                             │ ├── Lines        │
                             │ └── Amounts      │
                             └──────────────────┘
```

**Entity Location**: `healthsim.person.demographics`

### 3.2 State Management and Persistence

Generated cohorts can be persisted and resumed using the State Manager:

```python
from healthsim.state import StateManager, EntityWithProvenance

# Save generated entities
state_manager = StateManager()
for entity in generated_entities:
    wrapped = EntityWithProvenance.from_model(
        model=entity,
        entity_id=entity.id,
        entity_type="patients",
        provenance=Provenance.generated(
            generator="ProfileExecutor",
            seed=42,
            profile_id="medicare-diabetic-001"
        )
    )
    state_manager.save(wrapped)

# Later: Load and resume
loaded = state_manager.load_by_type("patients")
```

**State Components**:

| Component | Purpose |
|-----------|---------|
| **EntityWithProvenance** | Wraps any entity with lineage metadata |
| **Provenance** | Tracks generation source, seed, timestamp |
| **Serializers** | Format-specific serialization (JSON, CSV, etc.) |
| **Session** | Manages conversation-scoped state |
| **Workspace** | Manages persistent cohort storage |

**Implementation**: `healthsim.state`

### 3.3 Reference Data Integration

The framework integrates with PopulationSim reference data for realistic demographics:

```python
from healthsim.generation import ReferenceProfileResolver, resolve_geography

# Get actual Harris County demographics
resolver = ReferenceProfileResolver()
profile = resolver.resolve(
    geography={"type": "county", "fips": "48201"},
    datasets=["acs_demographics", "cdc_places", "svi"]
)

# Returns actual values:
# - Age distribution from ACS census
# - Health indicators from CDC PLACES
# - Social vulnerability from SVI
```

**Data Sources**:
- **ACS** (American Community Survey): Demographics, income, housing
- **CDC PLACES**: Health outcome prevalence by geography
- **SVI** (Social Vulnerability Index): Community risk factors
- **NPPES**: Real provider data (for NetworkSim)

---

## Part 4: Tooling Ecosystem

### 4.1 Skills Architecture

Skills are markdown documents that teach Claude how to assist with specific tasks. The Generative Framework uses a hierarchical skill structure:

```
skills/
├── generation/
│   ├── SKILL.md                    # Framework overview
│   ├── builders/
│   │   ├── profile-builder.md      # Build population specs
│   │   ├── journey-builder.md      # Build event sequences
│   │   └── quick-generate.md       # Simple generation
│   ├── executors/
│   │   ├── profile-executor.md     # Execute profiles
│   │   ├── journey-executor.md     # Execute journeys
│   │   └── cross-domain-sync.md    # Coordinate products
│   ├── distributions/
│   │   └── distribution-types.md   # Statistical distributions
│   ├── journeys/
│   │   └── journey-patterns.md     # Common journey patterns
│   └── templates/
│       ├── profiles/               # Pre-built profile templates
│       └── journeys/               # Pre-built journey templates
```

**How Skills Work**:

1. User makes a request ("Build a profile for Medicare diabetics")
2. Claude searches skills for relevant knowledge
3. Skills provide patterns, examples, and constraints
4. Claude guides user through building a specification
5. Result: Validated JSON ready for execution

### 4.2 Builders

Builders are conversational tools for creating specifications:

| Builder | Input | Output | Skill |
|---------|-------|--------|-------|
| **Profile Builder** | Natural language demographics | ProfileSpecification JSON | `profile-builder.md` |
| **Journey Builder** | Natural language care pathway | JourneySpecification JSON | `journey-builder.md` |
| **Quick Generate** | Simple request | Generated entities | `quick-generate.md` |

**Example Profile Builder Session**:

```
User: "Build a profile for 200 Medicare diabetic patients"

Claude: "I'll help you build this profile. Quick questions:
- Standard Medicare age (65+, mean ~72)? [Y/n]
- Geographic focus? [National/State/County]
- Include standard comorbidities (HTN, hyperlipidemia)? [Y/n]"

User: "Yes to defaults, Texas only"

Claude: [Generates ProfileSpecification JSON]
"Ready to generate or make adjustments?"
```

### 4.3 Templates

Templates are pre-built profiles and journeys for common use cases:

**Profile Templates**:
- `medicare-diabetic` - Medicare population with Type 2 diabetes
- `commercial-healthy` - Commercial working-age healthy adults
- `medicaid-pediatric` - Medicaid pediatric population

**Journey Templates**:
- `diabetic-first-year` - New T2DM diagnosis through year one
- `surgical-episode` - Pre-op through post-op recovery
- `new-member-onboarding` - First 90 days of coverage

**Using Templates**:

```
User: "Use the Medicare diabetic template for 100 patients"

Claude: [Loads template, applies count=100]
"Using medicare-diabetic template with 100 patients. Execute now?"
```

### 4.4 MCP Servers

MCP (Model Context Protocol) servers provide tool interfaces for programmatic access:

| Server | Purpose | Key Tools |
|--------|---------|-----------|
| **healthsim-mcp** | Core HealthSim operations | Query reference data, generate entities |
| **profile-server** | Profile operations | Build profile, execute profile |

**MCP Tool Example**:

```python
# healthsim-mcp tool call
{
    "tool": "healthsim_query_reference",
    "params": {
        "table": "places_county",
        "state": "TX",
        "county": "Harris"
    }
}
```

### 4.5 Python Tools

The Python implementation provides programmatic access to all framework components:

```python
from healthsim.generation import (
    # Specifications
    ProfileSpecification,
    JourneySpecification,
    
    # Execution
    ProfileExecutor,
    JourneyEngine,
    execute_profile,
    
    # Distributions
    NormalDistribution,
    CategoricalDistribution,
    create_distribution,
    
    # Cross-product
    CrossProductCoordinator,
    create_coordinator,
    
    # Handlers
    PatientSimHandlers,
    MemberSimHandlers,
    register_all_handlers,
)

# Complete generation workflow
spec = ProfileSpecification(
    id="my-cohort",
    name="My Cohort",
    generation=GenerationSpec(count=100, products=["patientsim"]),
    demographics=DemographicsSpec(
        age=DistributionSpec(type="normal", mean=55, std_dev=10),
        gender=DistributionSpec(type="categorical", weights={"M": 0.48, "F": 0.52})
    )
)

executor = ProfileExecutor(seed=42)
result = executor.execute(spec)
```

---

## Part 5: Usage Patterns

### 5.1 Simple Generation (No Journey)

Generate static entities without temporal events:

```
User: "Generate 50 diabetic patients"

Result:
- 50 Patient entities with demographics
- Each has Type 2 diabetes diagnosis
- Standard comorbidity patterns applied
- No encounters, claims, or events
```

### 5.2 Profile + Journey Generation

Generate entities with temporal event sequences:

```
User: "Generate 50 diabetic patients with first year of care"

Result:
- 50 Patient entities
- Each has a Timeline with:
  - Initial diagnosis encounter
  - Labs (A1c, CMP)
  - Medication orders (metformin)
  - Quarterly follow-ups
  - Cross-product triggers fire:
    - Encounter → Claim
    - Rx Order → Fill
```

### 5.3 Cross-Product Generation

Generate coordinated data across multiple products:

```
User: "Generate a patient-member pair with hospital stay and claims"

Result:
- PatientSim: Patient + ADT events + Labs
- MemberSim: Member + 837I (facility claim) + 837P (professional claims)
- Identity correlation maintained
- Events temporally coordinated
```

### 5.4 Reference-Based Generation

Generate entities matching real population characteristics:

```
User: "Generate 100 patients matching Harris County TX demographics"

Result:
- Age/gender distributions from ACS census data
- Condition prevalence from CDC PLACES
- Geographic coordinates within Harris County
- Realistic population representation
```

---

## Part 6: Architecture Summary

### 6.1 Component Interaction Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           USER INTERFACE                                │
│                                                                         │
│   Conversation ─────> Skills ─────> Builders ─────> Specifications     │
└─────────────────────────────────────┬───────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        SPECIFICATION LAYER                              │
│                                                                         │
│   ProfileSpecification          JourneySpecification                   │
│   ├── Demographics              ├── Phases                             │
│   ├── Clinical                  ├── Events                             │
│   ├── Coverage                  ├── Conditions                         │
│   └── Outputs                   └── Triggers                           │
└─────────────────────────────────────┬───────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         EXECUTION LAYER                                 │
│                                                                         │
│   ProfileExecutor               JourneyEngine                          │
│   ├── Distributions             ├── Timeline Creation                  │
│   ├── Seed Management           ├── Event Scheduling                   │
│   └── Entity Generation         └── Condition Evaluation               │
│                                                                         │
│   ProductHandlers               CrossProductCoordinator                │
│   ├── PatientSimHandlers        ├── Identity Registry                  │
│   ├── MemberSimHandlers         ├── Trigger Registry                   │
│   ├── RxMemberSimHandlers       └── Event Coordination                 │
│   └── TrialSimHandlers                                                 │
└─────────────────────────────────────┬───────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      CANONICAL DATA MODEL                               │
│                                                                         │
│   Person              Encounter           Claim                        │
│   ├── PersonName      ├── Diagnoses       ├── Lines                    │
│   ├── Address         ├── Procedures      └── Amounts                  │
│   └── ContactInfo     └── Observations                                 │
└─────────────────────────────────────┬───────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         PERSISTENCE LAYER                               │
│                                                                         │
│   StateManager                  Serializers                            │
│   ├── EntityWithProvenance      ├── FHIR R4                            │
│   ├── Session                   ├── HL7v2                              │
│   └── Workspace                 ├── X12 834/837                        │
│                                 └── CDISC SDTM                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 6.2 Key Design Principles

1. **Separation of Specification and Execution**: Creative work (specification) is conversational; mechanical work (execution) is deterministic.

2. **Hierarchical Seeding**: Every entity gets a deterministic child seed, enabling reproducibility even when entity count changes.

3. **Cross-Product Coordination**: A single person flows through multiple products with different IDs but correlated identity.

4. **Distribution-Driven Generation**: All random values come from explicit distribution specifications, not ad-hoc randomness.

5. **Progressive Enhancement**: Simple requests use defaults; complex requests enable full customization.

---

## Appendix A: Glossary

| Term | Definition |
|------|------------|
| **Cohort** | A group of generated entities sharing common characteristics (formerly "scenario") |
| **Distribution** | A statistical specification for generating values |
| **Event** | A discrete occurrence at a point in time |
| **Handler** | Product-specific logic for processing events |
| **Journey** | A specification of temporal event sequences |
| **Profile** | A specification of population characteristics |
| **Seed** | A number that initializes random generation for reproducibility |
| **Timeline** | An instantiated journey for a specific entity |
| **Trigger** | An event that causes another event (often cross-product) |

## Appendix B: Related Documentation

- [Generative Framework Concepts](initiatives/generative-framework/CONCEPTS.md) - Original conceptual design
- [Generative Framework Decisions](initiatives/generative-framework/DECISIONS.md) - Design decisions
- [Generation Skills Overview](../skills/generation/SKILL.md) - Skills overview
- [Profile Builder Skill](../skills/generation/builders/profile-builder.md) - Profile building guide
- [Journey Builder Skill](../skills/generation/builders/journey-builder.md) - Journey building guide

---

*End of Document*
