# Architecture

HealthSim's layered architecture enables clean separation of concerns and easy extensibility.

## System Overview

```text
┌──────────────────────────────────────────────┐
│         Claude Interface Layer                │
│  (Skills + MCP Servers + Project Knowledge)  │
└──────────────────────────────────────────────┘
                      ↓
┌──────────────────────────────────────────────┐
│        State Management Layer                 │
│   (Session + Cohorts + Provenance)          │
└──────────────────────────────────────────────┘
                      ↓
┌──────────────────────────────────────────────┐
│          Validation Layer                     │
│     (Clinical Rules + Format Compliance)      │
└──────────────────────────────────────────────┘
                      ↓
┌──────────────────────────────────────────────┐
│         Format Handler Layer                  │
│   (FHIR Transformer + HL7v2 + MIMIC)         │
└──────────────────────────────────────────────┘
                      ↓
┌──────────────────────────────────────────────┐
│          Core Model Layer                     │
│    (Patient + Encounter + Diagnosis, etc.)    │
└──────────────────────────────────────────────┘
                      ↓
┌──────────────────────────────────────────────┐
│         Generator Layer                       │
│  (PatientGenerator + Clinical Logic)          │
└──────────────────────────────────────────────┘
                      ↓
┌──────────────────────────────────────────────┐
│         Data Source Layer                     │
│      (Faker + MIMIC Patterns + Seed Data)    │
└──────────────────────────────────────────────┘
```

## Component Details

### 1. Claude Interface Layer

**Purpose:** Enable natural language and tool-based interaction

**Components:**
- **Skills** (`skills/`) - Markdown files with clinical knowledge
- **MCP Servers** (`src/*/mcp/`) - Tool servers for Claude
- **Project Instructions** (`.claude/project-instructions.md`) - Claude's role

**Data Flow:**
```text
User Request → Claude (with skills context) → MCP Tool Call → Generator → Response
```

### 2. State Management Layer

**Purpose:** Persist and restore workspace state across sessions

**Components:**

- **Session Manager** (`src/*/mcp/session.py`) - In-memory entity collection
- **Cohort Storage** (`~/.healthsim/cohorts/`) - Persistent JSON cohort files
- **Provenance Tracking** - Records how each entity was created (generated/loaded/derived)

**Key Concepts:**

- **Cohort** - A named snapshot of the entire workspace (patients + clinical data)
- **Provenance** - Metadata tracking source_type, source_system, skill_used, created_at
- **Branching** - Save baseline, explore variations, compare outcomes

**Tools (spec: [state-management/specification.md](../state-management/specification.md)):**

- `healthsim.save_cohort` - Save workspace to named cohort
- `healthsim.load_cohort` - Restore workspace from cohort
- `healthsim.list_cohorts` - List saved cohorts with filtering
- `healthsim.delete_cohort` - Remove a saved cohort

**Example:**
```text
User: "Save this as my-baseline before we add the complication"
Claude: [calls save_cohort] → Saved "my-baseline" with 15 patients

User: "Load my-baseline and try a different approach"
Claude: [calls load_cohort] → Restored to pre-complication state
```

### 3. Validation Layer

**Purpose:** Ensure clinical plausibility and format compliance

**Components:**
- **Clinical Validators** (`src/*/validation/clinical.py`)
  - HbA1c-glucose coherence
  - Medication appropriateness
  - Age-appropriate conditions
  - Temporal consistency

- **Format Validators** (`src/*/validation/format.py`)
  - FHIR R4 compliance
  - HL7v2 structure validation
  - MIMIC-III schema validation

**Example:**
```python
from patientsim.validation import validate_patient

results = validate_patient(patient)
if not results.is_valid:
    for issue in results.issues:
        print(f"{issue.severity}: {issue.message}")
```

### 4. Format Handler Layer

**Purpose:** Transform core models to healthcare standards

**Components:**
- **FHIR Transformer** (`src/*/formats/fhir/`)
  - Patient → FHIR Patient resource
  - Diagnosis → FHIR Condition resource
  - Medication → FHIR MedicationRequest
  - Labs → FHIR Observation

- **HL7v2 Generator** (`src/*/formats/hl7v2/`)
  - ADT^A01, ADT^A03, ADT^A08 messages
  - ORU^R01 lab result messages
  - Segment generators (PID, PV1, DG1, OBX)

- **MIMIC Transformer** (`src/*/formats/mimic/`)
  - PATIENTS table
  - ADMISSIONS table
  - DIAGNOSES_ICD, LABEVENTS, CHARTEVENTS

**Example:**
```python
from patientsim.formats.fhir import FHIRTransformer

transformer = FHIRTransformer()
fhir_bundle = transformer.create_bundle(
    patients=[patient],
    encounters=[encounter],
    diagnoses=diagnoses
)
```

### 5. Core Model Layer

**Purpose:** Define data structures with Pydantic

**Key Models:**

```python
class Patient(BaseModel):
    mrn: str
    given_name: str
    family_name: str
    birth_date: date
    gender: Gender
    # ... additional fields

class Encounter(BaseModel):
    encounter_id: str
    patient_mrn: str
    class_code: EncounterClass
    admission_time: datetime
    # ...

class Diagnosis(BaseModel):
    code: str  # ICD-10
    description: str
    patient_mrn: str
    # ...
```

**Benefits:**
- Type safety
- Automatic validation
- JSON serialization
- IDE autocomplete

### 6. Generator Layer

**Purpose:** Create realistic synthetic data

**Components:**

```python
class PatientGenerator:
    def generate_patient(
        self,
        age_range: tuple[int, int] = (18, 85),
        gender: Optional[Gender] = None,
        seed: Optional[int] = None
    ) -> Patient:
        """Generate patient with demographics."""

    def generate_encounter(
        self,
        patient: Patient,
        encounter_class: EncounterClass = EncounterClass.INPATIENT
    ) -> Encounter:
        """Generate encounter for patient."""

    def generate_diagnosis(
        self,
        patient: Patient,
        encounter: Encounter
    ) -> Diagnosis:
        """Generate diagnosis."""
```

**Generation Logic:**
- Uses Faker for demographics
- Applies clinical guidelines
- Ensures temporal coherence
- Maintains statistical distributions

### 7. Data Source Layer

**Purpose:** Provide realistic base data

**Components:**
- **Faker** - Names, addresses, phone numbers
- **MIMIC-III Patterns** - Lab value distributions, vital sign ranges
- **Seed Data** - Medication lists, ICD-10 codes, LOINC codes

## Data Flow

### Generation Flow

```text
1. User Request
   ↓
2. Claude (with Skills context)
   ↓
3. MCP Tool Call (generate_patient)
   ↓
4. PatientGenerator.generate_patient()
   ↓
5. Demographics from Faker
   ↓
6. Clinical data from guidelines
   ↓
7. Validation checks
   ↓
8. Return Patient object
   ↓
9. Claude formats response
```

### Export Flow

```text
1. User Request ("export to FHIR")
   ↓
2. Claude calls export_fhir tool
   ↓
3. FHIRTransformer.transform_patient()
   ↓
4. Create FHIR resources
   ↓
5. Validate FHIR bundle
   ↓
6. Return JSON
   ↓
7. Save to file (optional)
```

## Design Patterns

### Pattern 1: Transformer Pattern

Each format has a transformer that converts core models:

```python
class BaseTransformer(ABC):
    @abstractmethod
    def transform_patient(self, patient: Patient) -> Any:
        """Transform patient to target format."""

class FHIRTransformer(BaseTransformer):
    def transform_patient(self, patient: Patient) -> FHIRPatient:
        # FHIR-specific transformation
```

### Pattern 2: Builder Pattern

Complex objects built incrementally:

```python
generator = PatientGenerator()
patient = generator.generate_patient(age=65)
encounter = generator.generate_encounter(patient)
diagnosis = generator.generate_diagnosis(patient, encounter)
```

### Pattern 3: Strategy Pattern

Different validation strategies:

```python
class ValidationStrategy(ABC):
    @abstractmethod
    def validate(self, patient: Patient) -> ValidationResult:
        pass

class HbA1cGlucoseValidator(ValidationStrategy):
    def validate(self, patient: Patient) -> ValidationResult:
        # Check HbA1c-glucose coherence
```

## Extensibility Points

### Adding New Export Format

1. Create `src/*/formats/your_format/transformer.py`
2. Implement `BaseTransformer` interface
3. Add tests
4. Register in MCP export server

### Adding New Validation Rule

1. Create validator in `src/*/validation/rules/`
2. Implement `ValidationRule` interface
3. Add to validation pipeline
4. Add tests

### Adding New Clinical Cohort

1. Create skill file in healthsim-common/skills/
2. Define clinical logic and parameters
3. Add example patients
4. Test with Claude

## Technology Stack

- **Python 3.11+** - Modern Python features
- **Pydantic 2.x** - Data validation and serialization
- **Faker** - Synthetic demographics
- **Black** - Code formatting
- **Ruff** - Linting
- **Mypy** - Type checking
- **Pytest** - Testing

## Performance Considerations

### Optimization Strategies

**1. Seed-based generation:**
```python
generator = PatientGenerator(seed=42)  # Reproducible
```

**2. Batch generation:**
```python
patients = [generator.generate_patient() for _ in range(1000)]
```

**3. Lazy validation:**
```python
# Validate only when needed
if needs_validation:
    validate_patient(patient)
```

**4. Efficient export:**
```python
# Batch export
transformer.create_bundle(patients=patients)  # Single bundle
```

## Security & Privacy

**Synthetic Data Only:**
- All data generated using Faker and statistical distributions
- No real patient data
- HIPAA-safe for development/testing

**No PII Storage:**
- No persistent storage of generated data
- Data exists only in memory during session
- Export to user-controlled locations

## See Also

- [HealthSim Core Extraction Spec](healthsim-common-spec.md) - Shared library architecture
- [Extension Framework](../extensions/philosophy.md) - Adding new capabilities
- [State Management](../state-management/specification.md) - Save/load cohorts
