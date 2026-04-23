# PatientSim - Claude Code Guide

This document provides comprehensive context for Claude Code to effectively contribute to PatientSim. Read this first when starting work on the project.

## Project Overview

### What is PatientSim?

PatientSim is a healthcare patient simulation and synthetic data generation platform that enables:
- Creation of realistic patient data for testing and development
- Generation of healthcare interoperability messages (HL7v2, FHIR, CDA)
- Building clinical scenarios through natural language (Configuration as Conversation)
- Integration testing of healthcare systems
- Healthcare education and training

### Key Concepts

**Digital Patient Twin**: A comprehensive digital representation of a patient including demographics, conditions, medications, vitals, and clinical history. The twin maintains temporal consistency and clinical plausibility.

**Configuration as Conversation**: Rather than writing YAML or JSON configs, users describe what they want in natural language to Claude, which generates appropriate patient data and scenarios.

**Skills Library**: Reusable prompt templates for common healthcare tasks (generating HL7v2 messages, creating FHIR bundles, simulating ED visits, etc.).

### Target Users

- **Healthcare developers** testing EHR integrations
- **QA engineers** validating healthcare systems
- **Data scientists** needing realistic test datasets
- **Educators** creating training scenarios
- **Claude users** working with healthcare data

## Architecture

### Layered Architecture (v2.0)

PatientSim v2.0 uses [healthsim-core](../core) as its foundation:

```
┌─────────────────────────────────────────┐
│  PatientSim (This Repository)           │
├─────────────────────────────────────────┤
│  Skills & MCP Servers (Claude Interface)│
│  Clinical Validation Rules              │
│  Format Handlers (HL7v2, FHIR, MIMIC)   │
│  PatientGenerator (extends BaseGenerator)│
│  Clinical Models (Patient, Encounter...)│
├─────────────────────────────────────────┤
│  healthsim-core (Shared Library)        │
├─────────────────────────────────────────┤
│  BaseGenerator, SeedManager             │
│  ValidationFramework, BaseValidator     │
│  Person, Address, ContactInfo           │
│  Timeline, TimePeriod utilities         │
│  SkillLoader, SkillComposer             │
└─────────────────────────────────────────┘
```

**Key Inheritance:**
- `PatientGenerator` extends `healthsim.generation.BaseGenerator`
- Validation re-exports from `healthsim.validation`
- Skills module extends healthsim-core schema with clinical fields

### Core Components

**Core Module** (`src/patientsim/core/`)
- `Patient` - Primary patient model with demographics, identifiers
- `Encounter` - Clinical encounters (ED visits, admissions, etc.)
- `Condition` - Diagnoses and problems
- `Medication` - Medication orders and administrations
- `Observation` - Vitals, labs, and other observations
- `Generator` - Patient and scenario generation engine

**Formats Module** (`src/patientsim/formats/`)
- `hl7v2/` - HL7v2 message builders (ADT, ORM, ORU, etc.)
- `fhir/` - FHIR resource generators
- `cda/` - CDA document generators (future)
- `json/` - JSON export formats

**Validation Module** (`src/patientsim/validation/`)
- Format validators (HL7v2, FHIR conformance)
- Clinical plausibility checks
- Data quality rules

**MCP Module** (`src/patientsim/mcp/`)
- MCP server implementations
- Skill loading and execution
- Resource providers for Claude

### Technology Stack

- **Python 3.11+** - Match expressions, improved type hints, performance
- **healthsim-core** - Shared foundation library (v2.0+)
- **Pydantic v2** - Data validation, serialization, settings management
- **Pandas** - Tabular data manipulation, MIMIC-III integration
- **Faker** - Realistic fake data (via healthsim-core)
- **python-dateutil** - Date/time handling
- **PyYAML** - Configuration files

## Coding Standards

### Python Style

**Formatting**: Black with 100 character line length
```python
# Good - fits in 100 chars, clear and readable
def create_patient(
    name: str, age: int, gender: str, mrn: str | None = None
) -> Patient:
    """Create a new patient with the given attributes."""
    return Patient(name=name, age=age, gender=gender, mrn=mrn or generate_mrn())
```

**Linting**: Ruff with these key rules enabled:
- Pyflakes (F) - detect errors
- Pycodestyle (E, W) - PEP 8
- isort (I) - import sorting
- flake8-bugbear (B) - common bugs
- pyupgrade (UP) - modern Python syntax

**Type Hints**: Required everywhere
```python
# Good - complete type hints
def generate_hl7_message(patient: Patient, event_type: str) -> str:
    """Generate HL7v2 message for the patient."""
    ...

# Bad - missing type hints
def generate_hl7_message(patient, event_type):
    ...
```

Use `| None` instead of `Optional`, `list[str]` instead of `List[str]` (Python 3.11+ style).

### Documentation Standards

**Docstrings**: Google style, present tense
```python
def admit_patient(patient: Patient, facility: str, room: str) -> Encounter:
    """Admit a patient to the specified facility and room.

    Args:
        patient: The patient to admit.
        facility: Facility identifier (e.g., "MAIN HOSPITAL").
        room: Room assignment (e.g., "ICU-101").

    Returns:
        The created encounter representing the admission.

    Raises:
        ValueError: If the patient is already admitted.
    """
    ...
```

**Inline Comments**: Explain "why", not "what"
```python
# Good - explains rationale
# Use MSH-9 format: message_type^trigger_event
message_type = f"{msg_type}^{trigger}"

# Bad - states the obvious
# Set message_type to concatenation
message_type = f"{msg_type}^{trigger}"
```

**Module Docstrings**: First line of every module
```python
"""HL7v2 ADT message generation and parsing."""
```

### Testing Requirements

**Coverage Target**: 90%+ for new code

**Test Structure**: Follow AAA pattern (Arrange, Act, Assert)
```python
def test_patient_age_calculation() -> None:
    """Test that patient age is calculated correctly from birth date."""
    # Arrange
    birth_date = datetime(1980, 1, 1)
    patient = Patient(name="Test", birth_date=birth_date)

    # Act
    age = patient.calculate_age()

    # Assert
    assert age == 45  # assuming current year 2025
```

**Test Files**: Mirror source structure
- `src/patientsim/core/patient.py` → `tests/core/test_patient.py`
- Use `test_*.py` naming
- Group related tests in classes: `class TestPatientValidation`

**Fixtures**: Use pytest fixtures for common setup
```python
@pytest.fixture
def sample_patient() -> Patient:
    """Create a sample patient for testing."""
    return Patient(name="John Doe", age=45, gender="M", mrn="MRN001")
```

### Git Commit Messages

Format: `<type>: <subject>`

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Test additions/changes
- `refactor`: Code refactoring
- `chore`: Build/tooling changes

Examples:
```
feat: add HL7v2 ADT^A01 message generator
fix: correct patient age calculation for leap years
docs: add FHIR resource generation examples
test: add tests for encounter creation
refactor: extract common HL7 segment builders
```

## Domain Knowledge

### Healthcare Data Fundamentals

**Patient Identifiers**:
- **MRN** (Medical Record Number) - Internal patient ID
- **SSN** - Social Security Number (9 digits)
- **Driver's License** - State-issued ID

**Demographics**:
- Name (Given, Family, Middle, Suffix)
- Date of Birth (for age calculation)
- Gender (M/F/O/U)
- Address (street, city, state, zip)
- Phone, email

**Clinical Data**:
- **Conditions** - Diagnoses, problems (use ICD-10 codes)
- **Medications** - Prescriptions, administrations (use RxNorm codes)
- **Vitals** - BP, HR, temp, SpO2, height, weight
- **Labs** - Blood work, cultures (use LOINC codes)

### HL7v2 Message Structure

HL7v2 messages are pipe-delimited with this structure:
```
MSH|^~\&|SENDING_APP|FACILITY|RECEIVING_APP|DEST|20250126160000||ADT^A01|MSG001|P|2.5
EVN|A01|20250126160000
PID|1||MRN12345^^^MRN||DOE^JOHN^Q||19800101|M|||123 MAIN ST^^BOSTON^MA^02101
PV1|1|I|ICU^101^01||||DOC001^SMITH^JANE|||MED||||A|||DOC001|IP|V001
```

**Key Segments**:
- **MSH** - Message Header (required, first segment)
- **EVN** - Event Type (when/what happened)
- **PID** - Patient Identification
- **PV1** - Patient Visit
- **OBX** - Observation/Result
- **ORC/OBR** - Order Control/Order Detail

**Field Separators**:
- `|` - Field separator
- `^` - Component separator
- `~` - Repetition separator
- `\` - Escape character
- `&` - Sub-component separator

### FHIR Resource Concepts

FHIR uses JSON/XML resources with REST APIs:

**Key Resources**:
- **Patient** - Demographics, identifiers
- **Encounter** - Hospital visits, ED visits
- **Condition** - Diagnoses
- **MedicationRequest** - Prescriptions
- **Observation** - Vitals, labs

**Resource Structure**:
```json
{
  "resourceType": "Patient",
  "id": "example",
  "identifier": [{"system": "http://hospital.org/mrn", "value": "MRN12345"}],
  "name": [{"given": ["John"], "family": "Doe"}],
  "gender": "male",
  "birthDate": "1980-01-01"
}
```

### MIMIC-III Schema Overview

MIMIC-III is a real ICU database we reference for realistic patterns:

**Key Tables**:
- `PATIENTS` - Demographics, DOB, DOD
- `ADMISSIONS` - Hospital admissions
- `ICUSTAYS` - ICU stays
- `CHARTEVENTS` - Vitals, monitoring data
- `LABEVENTS` - Lab results
- `PRESCRIPTIONS` - Medications

We don't store MIMIC data, but use it to understand realistic distributions and relationships.

## Project-Specific Patterns

### Adding New Output Formats

1. Create module in `src/patientsim/formats/<format_name>/`
2. Implement `BaseFormatter` interface:
   ```python
   class MyFormatter(BaseFormatter):
       def format_patient(self, patient: Patient) -> str:
           """Convert patient to format."""
           ...
   ```
3. Add validator in `src/patientsim/validation/<format_name>.py`
4. Add tests in `tests/formats/test_<format_name>.py`
5. Document in `docs/formats/<format_name>.md`

### Creating New Skills

Skills live in `skills/` directory:

1. Create skill file: `skills/<category>/<skill_name>.md`
2. Use frontmatter for metadata:
   ```markdown
   ---
   name: Generate HL7 ADT Message
   description: Create an HL7v2 ADT^A01 admission message
   category: hl7v2
   ---

   Generate an HL7v2 ADT^A01 message for patient admission with...
   ```
3. Register in MCP server if needed
4. Add example usage in `examples/skills/`

### Implementing MCP Servers

MCP servers provide Claude with context:

1. Create server in `src/patientsim/mcp/<server_name>.py`
2. Implement resource providers:
   ```python
   @mcp.resource("patient://{mrn}")
   def get_patient(mrn: str) -> dict:
       """Provide patient data to Claude."""
       ...
   ```
3. Register in `pyproject.toml` entry points
4. Document in `docs/mcp/<server_name>.md`

### Validation Patterns

All validators follow this pattern:

```python
class PatientValidator:
    """Validate patient data."""

    def validate(self, patient: Patient) -> list[ValidationError]:
        """Validate patient and return errors."""
        errors = []
        if not patient.name:
            errors.append(ValidationError("Patient name is required"))
        if patient.age < 0:
            errors.append(ValidationError("Patient age cannot be negative"))
        return errors
```

Return list of errors (empty = valid), don't raise exceptions.

## File Organization

### Directory Structure

```
src/patientsim/
├── __init__.py          # Package exports
├── core/                # Core models
│   ├── __init__.py
│   ├── patient.py       # Patient model
│   ├── encounter.py     # Encounter model
│   └── generator.py     # Generation logic
├── formats/             # Format handlers
│   ├── __init__.py
│   ├── hl7v2/          # HL7v2 messages
│   ├── fhir/           # FHIR resources
│   └── json/           # JSON export
├── validation/          # Validators
│   ├── __init__.py
│   ├── clinical.py     # Clinical rules
│   └── format.py       # Format validation
└── mcp/                # MCP integration
    ├── __init__.py
    ├── server.py       # MCP server
    └── skills.py       # Skill loader
```

### Naming Conventions

**Files**: lowercase with underscores (`patient_generator.py`)
**Classes**: PascalCase (`PatientGenerator`)
**Functions**: snake_case (`generate_patient`)
**Constants**: UPPER_SNAKE_CASE (`DEFAULT_FACILITY`)
**Private**: prefix with underscore (`_internal_helper`)

### Import Organization

Use isort/Ruff ordering:
```python
# Standard library
import os
from datetime import datetime

# Third-party
import pandas as pd
from pydantic import BaseModel

# Local
from patientsim.core import Patient
from patientsim.validation import validate_patient
```

Prefer explicit imports over wildcards:
```python
# Good
from patientsim.core import Patient, Encounter

# Bad
from patientsim.core import *
```

## Common Tasks

### Running Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=patientsim --cov-report=html

# Specific file
pytest tests/core/test_patient.py

# Specific test
pytest tests/core/test_patient.py::test_patient_age_calculation

# Watch mode (requires pytest-watch)
ptw
```

### Code Quality Checks

```bash
# Format code
black src/ tests/

# Lint
ruff check src/ tests/ --fix

# Type check
mypy src/

# All quality checks
pre-commit run --all-files
```

### Building & Packaging

```bash
# Install in editable mode
pip install -e ".[dev]"

# Build distribution
python -m build

# Run from source
python -m patientsim
```

### Generating Documentation

```bash
# (Future) Build Sphinx docs
cd docs
make html
```

## Key Reminders

1. **Type hints everywhere** - No exceptions
2. **Test first** - Write tests before/with implementation
3. **Validate early** - Use Pydantic models for data validation
4. **Document public APIs** - All public functions/classes need docstrings
5. **Keep it modular** - Small, focused modules
6. **Think in layers** - Core → Formats → Validation → MCP
7. **Real-world patterns** - Reference MIMIC-III for realistic data
8. **Configuration as Conversation** - Users describe, Claude generates

## Questions?

When uncertain about:
- **Architecture** - Ask which layer is appropriate
- **Naming** - Follow existing patterns in similar modules
- **Testing** - Reference existing test files
- **Standards** - Check this document first

PatientSim is designed to be extended. When adding new capabilities, follow existing patterns and maintain the layered architecture.
