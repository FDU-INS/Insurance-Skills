# HealthSim Core Specification

This document outlines the shared infrastructure foundation (`healthsim-common`) that enables PatientSim, MemberSim, and RxMemberSim to share common functionality.

**Document Version**: 1.0

---

## 1. Module Classification

### Legend
- **CORE** — Generic infrastructure, shared across all products
- **PRODUCT** — Product-specific, stays in respective repository
- **HYBRID** — Contains both; needs to be split

---

### 1.1 Core Module Classification

| File | Classification | Classes/Functions | Notes |
|------|---------------|-------------------|-------|
| `models.py` | **HYBRID** | `Gender`, `Person`, `PersonName`, `Address`, `ContactInfo` | Split into: generic `Person` model (CORE) + product-specific extensions |
| `generator.py` | **HYBRID** | `BaseGenerator` | Extract base class with seed management, random utilities |
| `reference_data.py` | **PRODUCT** | Codes and reference data | Product-specific codes (ICD-10, NDC, etc.) stay in products |

---

### 1.2 Validation Module

| File | Classification | Classes/Functions | Notes |
|------|---------------|-------------------|-------|
| `base.py` | **CORE** | `ValidationSeverity`, `ValidationIssue`, `ValidationResult`, `BaseValidator` | Generic validation framework |
| `structural.py` | **HYBRID** | `TemporalValidator`, `ReferentialIntegrityValidator` | `TemporalValidator` is mostly generic (date logic) |
| `clinical.py` | **PRODUCT** | Domain-specific validators | Product-specific validation rules |

---

### 1.3 Formats Module

| File | Classification | Classes/Functions | Notes |
|------|---------------|-------------------|-------|
| `base.py` | **CORE** | `BaseTransformer` | Abstract base class for format transformers |
| `json.py` | **CORE** | `JSONExporter` | Generic JSON export |
| `csv.py` | **CORE** | `CSVExporter` | Generic CSV export |
| Product formats | **PRODUCT** | FHIR, HL7v2, X12, NCPDP, etc. | Product-specific format implementations |

---

### 1.4 Skills Module

| File | Classification | Classes/Functions | Notes |
|------|---------------|-------------------|-------|
| `schema.py` | **CORE** | `SkillType`, `ParameterType`, `SkillMetadata`, `SkillParameter`, `Skill` | Generic skill schema |
| `loader.py` | **CORE** | `SkillLoader`, `SkillParseError` | Generic markdown parsing |
| `composer.py` | **CORE** | `SkillComposer`, `SkillCompositionError` | Generic skill composition |

---

### 1.5 MCP Module

| File | Classification | Classes/Functions | Notes |
|------|---------------|-------------------|-------|
| `session.py` | **HYBRID** | `Session[T]`, `SessionManager` | Session management is generic pattern |
| `formatters.py` | **HYBRID** | `format_error()`, `format_success()` | Generic formatters extract, product-specific stay |
| Servers | **PRODUCT** | `generation_server`, `export_server`, `validation_server` | Product-specific MCP servers |

---

## 2. Core API Specification

### 2.1 `healthsim.person` — Demographics & Identifiers

```python
# healthsim/person/models.py

class Gender(str, Enum):
    """Generic gender representation."""
    MALE = "M"
    FEMALE = "F"
    OTHER = "O"
    UNKNOWN = "U"

class PersonName(BaseModel):
    """Name components."""
    given_name: str
    middle_name: str | None = None
    family_name: str
    suffix: str | None = None

    @property
    def full_name(self) -> str: ...

class Address(BaseModel):
    """Physical address."""
    street_address: str | None = None
    city: str | None = None
    state: str | None = None
    postal_code: str | None = None
    country: str = "US"

class ContactInfo(BaseModel):
    """Contact information."""
    phone: str | None = None
    email: str | None = None

class Person(BaseModel):
    """Base person model - generic demographics."""
    id: str  # Generic ID field
    name: PersonName
    birth_date: date
    gender: Gender
    address: Address | None = None
    contact: ContactInfo | None = None
    deceased: bool = False
    death_date: date | None = None

    @property
    def age(self) -> int: ...

    @field_validator("birth_date")
    def birth_date_not_future(cls, v): ...

    @model_validator(mode="after")
    def validate_death_date(self): ...
```

---

### 2.2 `healthsim.temporal` — Timeline & Date Utilities

```python
# healthsim/temporal/models.py

class TimePeriod(BaseModel):
    """A period of time with start and optional end."""
    start: datetime
    end: datetime | None = None

    @property
    def duration_hours(self) -> float | None: ...

    @field_validator("end")
    def end_after_start(cls, v, info): ...

class TimelineEvent(BaseModel):
    """A single event on a timeline."""
    event_id: str
    event_type: str
    timestamp: datetime
    metadata: dict[str, Any] = Field(default_factory=dict)

class Timeline(BaseModel):
    """Ordered sequence of events."""
    entity_id: str  # ID of the entity this timeline belongs to
    events: list[TimelineEvent] = Field(default_factory=list)

    def add_event(self, event: TimelineEvent) -> None: ...
    def get_events_in_range(self, start: datetime, end: datetime) -> list[TimelineEvent]: ...

# healthsim/temporal/utils.py

def format_datetime_iso(dt: datetime) -> str: ...
def format_date_iso(d: date) -> str: ...
def parse_datetime(s: str) -> datetime: ...
def calculate_age(birth_date: date, as_of: date | None = None) -> int: ...
```

---

### 2.3 `healthsim.generation` — Base Generator Framework

```python
# healthsim/generation/base.py

class BaseGenerator:
    """Base class for data generators with reproducibility support."""

    def __init__(self, seed: int | None = None, locale: str = "en_US") -> None:
        self.seed = seed
        self.faker = Faker(locale)
        self._setup_seed(seed)

    def _setup_seed(self, seed: int | None) -> None:
        """Setup random seeds for reproducibility."""
        if seed is not None:
            Faker.seed(seed)
            self.faker.seed_instance(seed)
            random.seed(seed)

    def random_choice(self, options: list[T]) -> T: ...
    def random_int(self, min_val: int, max_val: int) -> int: ...
    def random_float(self, min_val: float, max_val: float) -> float: ...
    def random_date_in_range(self, start: date, end: date) -> date: ...
    def random_datetime_in_range(self, start: datetime, end: datetime) -> datetime: ...
    def weighted_choice(self, options: list[T], weights: list[float]) -> T: ...

# healthsim/generation/person.py

class PersonGenerator(BaseGenerator):
    """Generator for Person demographics."""

    def generate_person(
        self,
        age_range: tuple[int, int] | None = None,
        gender: Gender | None = None,
    ) -> Person: ...

    def generate_name(self, gender: Gender | None = None) -> PersonName: ...
    def generate_address(self) -> Address: ...
    def generate_contact(self) -> ContactInfo: ...
```

---

### 2.4 `healthsim.validation` — Validation Framework

```python
# healthsim/validation/base.py

class ValidationSeverity(str, Enum):
    """Severity level of a validation issue."""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"

@dataclass
class ValidationIssue:
    """A single validation issue."""
    code: str
    message: str
    severity: ValidationSeverity
    field_path: str | None = None
    context: dict[str, Any] = field(default_factory=dict)

@dataclass
class ValidationResult:
    """Result of validation."""
    valid: bool
    issues: list[ValidationIssue] = field(default_factory=list)

    @property
    def errors(self) -> list[ValidationIssue]: ...
    @property
    def warnings(self) -> list[ValidationIssue]: ...
    @property
    def infos(self) -> list[ValidationIssue]: ...

    def add_issue(self, code: str, message: str, severity: ValidationSeverity, ...) -> None: ...
    def merge(self, other: "ValidationResult") -> None: ...

class BaseValidator(ABC):
    """Abstract base validator."""

    @abstractmethod
    def validate(self, *args, **kwargs) -> ValidationResult: ...

# healthsim/validation/temporal.py

class TemporalValidator(BaseValidator):
    """Validates temporal consistency."""

    def validate_date_not_future(self, d: date, field_name: str) -> ValidationResult: ...
    def validate_date_order(self, earlier: date, later: date, ...) -> ValidationResult: ...
    def validate_period(self, period: TimePeriod) -> ValidationResult: ...
```

---

### 2.5 `healthsim.formats` — Base Transformer Interface

```python
# healthsim/formats/base.py

from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar("T")  # Input type
R = TypeVar("R")  # Output type

class BaseTransformer(ABC, Generic[T, R]):
    """Abstract base class for format transformers."""

    @abstractmethod
    def transform(self, source: T) -> R:
        """Transform source object to target format."""
        ...

    def transform_batch(self, sources: list[T]) -> list[R]:
        """Transform multiple objects."""
        return [self.transform(s) for s in sources]

# healthsim/formats/json.py

class JSONExporter:
    """Export objects to JSON."""

    def export(self, obj: BaseModel, **kwargs) -> str: ...
    def export_to_file(self, obj: BaseModel, path: Path, **kwargs) -> None: ...

# healthsim/formats/csv.py

class CSVExporter:
    """Export tabular data to CSV."""

    def export(self, data: list[dict], columns: list[str] | None = None) -> str: ...
    def export_to_file(self, data: list[dict], path: Path, ...) -> None: ...
```

---

### 2.6 `healthsim.skills` — Skill Framework

```python
# healthsim/skills/schema.py

class SkillType(str, Enum):
    """Type of skill."""
    DOMAIN_KNOWLEDGE = "domain-knowledge"
    SCENARIO_TEMPLATE = "cohort-template"
    FORMAT_SPEC = "format-spec"
    VALIDATION_RULES = "validation-rules"

class ParameterType(str, Enum):
    """Type of skill parameter."""
    RANGE = "range"
    ENUM = "enum"
    BOOLEAN = "boolean"
    INTEGER = "integer"
    STRING = "string"

class SkillMetadata(BaseModel):
    """Metadata for a skill."""
    type: SkillType
    version: str
    author: str | None = None
    tags: list[str] = Field(default_factory=list)

class SkillParameter(BaseModel):
    """A configurable parameter for a skill."""
    name: str
    type: ParameterType
    default: Any
    description: str

    def validate_value(self, value: Any) -> bool: ...

class Skill(BaseModel):
    """A complete skill definition."""
    name: str
    description: str
    metadata: SkillMetadata
    purpose: str
    parameters: list[SkillParameter] = Field(default_factory=list)
    knowledge: dict[str, str] = Field(default_factory=dict)
    examples: list[str] = Field(default_factory=list)
    references: list[str] = Field(default_factory=list)
    dependencies: list[str] = Field(default_factory=list)
    raw_text: str
    # v2.0 format fields
    for_claude: str | None = None
    when_to_use: str | None = None

# healthsim/skills/loader.py

class SkillParseError(Exception): ...

class SkillLoader:
    """Loads and parses skill files from Markdown."""

    def load_file(self, path: Path) -> Skill: ...
    def load_string(self, content: str) -> Skill: ...

# healthsim/skills/composer.py

class SkillCompositionError(Exception): ...

class SkillComposer:
    """Composes multiple skills together."""

    def __init__(self, skills_dir: Path | None = None) -> None: ...
    def compose(self, skill_paths: list[Path], resolve_dependencies: bool = True) -> Skill: ...
```

---

### 2.7 `healthsim.config` — Settings & Logging

```python
# healthsim/config/settings.py

from pydantic_settings import BaseSettings

class HealthSimSettings(BaseSettings):
    """Base settings for HealthSim applications."""

    app_name: str = "healthsim"
    debug: bool = False
    log_level: str = "INFO"
    random_seed: int | None = None
    locale: str = "en_US"

    class Config:
        env_prefix = "HEALTHSIM_"

# healthsim/config/logging.py

def setup_logging(level: str = "INFO", app_name: str = "healthsim") -> logging.Logger: ...
```

---

## 3. Extraction Sequence

Extract in this order (least dependencies first):

### Phase 2A: Foundation (No Internal Dependencies)

1. **`healthsim.config`** — Settings, logging utilities
2. **`healthsim.validation.base`** — ValidationSeverity, ValidationIssue, ValidationResult, BaseValidator
3. **`healthsim.temporal`** — TimePeriod, Timeline, date utilities
4. **`healthsim.formats.base`** — BaseTransformer interface

### Phase 2B: Person & Generation (Depends on Foundation)

5. **`healthsim.person`** — Gender, PersonName, Address, ContactInfo, Person
6. **`healthsim.generation.base`** — BaseGenerator with seed management
7. **`healthsim.generation.person`** — PersonGenerator (depends on person, generation.base)
8. **`healthsim.validation.temporal`** — TemporalValidator (depends on validation.base, temporal)

### Phase 2C: Skills Framework (Depends on Foundation)

9. **`healthsim.skills.schema`** — Skill, SkillType, SkillParameter, etc.
10. **`healthsim.skills.loader`** — SkillLoader (depends on schema)
11. **`healthsim.skills.composer`** — SkillComposer (depends on loader, schema)

### Phase 2D: Utilities

12. **`healthsim.formats.json`** — JSONExporter
13. **`healthsim.formats.csv`** — CSVExporter

---

## 4. Dependency Map

```
healthsim-common
├── config/
│   ├── settings.py      (pydantic-settings)
│   └── logging.py       (stdlib logging)
│
├── validation/
│   ├── base.py          (dataclasses, enum)
│   └── temporal.py      → validation.base, temporal
│
├── temporal/
│   ├── models.py        (pydantic, datetime)
│   └── utils.py         (datetime)
│
├── person/
│   └── models.py        (pydantic) → temporal
│
├── generation/
│   ├── base.py          (faker, random)
│   └── person.py        → generation.base, person
│
├── formats/
│   ├── base.py          (abc, typing)
│   ├── json.py          (pydantic, json)
│   └── csv.py           (csv)
│
└── skills/
    ├── schema.py        (pydantic, enum)
    ├── loader.py        → skills.schema
    └── composer.py      → skills.loader, skills.schema
```

**External Dependencies for healthsim-common:**
- `pydantic >= 2.0`
- `pydantic-settings >= 2.0`
- `faker >= 18.0`
- `python-dateutil >= 2.8`
- `PyYAML >= 6.0`

---

## 5. Risk Areas

### 5.1 Model Inheritance Complexity

**Risk**: Product models may become monolithic. Splitting into `Person` (core) + product-specific extension requires careful inheritance design.

**Mitigation**:
- Product models inherit from `Person` and add product-specific fields
- Use composition where inheritance creates coupling issues
- Provide migration utilities for existing data

### 5.2 Validation Model References

**Risk**: Validators may reference product-specific models directly.

**Mitigation**:
- Extract generic temporal validation (date ordering, future date checks)
- Product-specific validators remain in product repos
- Use Protocol/ABC for generic "entity with dates" validation

### 5.3 Skills GenerationRules

**Risk**: `GenerationRules` may have product-specific fields.

**Mitigation**:
- Make `GenerationRules` extensible with generic base
- Products extend with their specific fields
- Alternatively, use `raw_sections` dict approach

### 5.4 Session Manager Coupling

**Risk**: Sessions may be tightly coupled to product models.

**Mitigation**:
- Extract generic `Session[T]` pattern
- Product sessions become `Session[ProductData]`
- SessionManager becomes generic

### 5.5 Circular Import Prevention

**Risk**: Current code may have validation importing from models; models might need validation.

**Mitigation**:
- Strict layering: `config` → `validation.base` → `temporal` → `person` → `generation`
- No upward imports within healthsim-common
- Use TYPE_CHECKING imports where necessary

---

## 6. Product Post-Extraction Structure

After extraction, each product will have this structure:

```
product/
├── __init__.py
├── core/
│   ├── __init__.py
│   ├── models.py           # ProductModel extends healthsim.person.Person
│   ├── generator.py        # ProductGenerator extends healthsim.generation.BaseGenerator
│   └── reference_data.py   # Product-specific codes (unchanged)
│
├── validation/
│   ├── __init__.py
│   ├── product.py          # Product-specific validators (unchanged)
│   └── structural.py       # Uses healthsim.validation.base
│
├── formats/
│   ├── format1/            # Product-specific format implementations
│   ├── format2/
│   └── ...
│
├── skills/
│   └── product_rules.py    # Product-specific skill extensions
│
└── mcp/
    ├── __init__.py
    ├── session.py          # ProductSession (uses healthsim session pattern)
    ├── generation_server.py
    ├── validation_server.py
    ├── export_server.py
    └── formatters.py
```

**Product Dependencies:**
```toml
[project]
dependencies = [
    "healthsim-common >= 1.0.0",
    # ... product-specific deps
]
```

---

## 7. Testing Strategy

### 7.1 healthsim-common Tests

- Unit tests for all extracted modules
- No product-specific test data
- Use generic person/entity test cases

### 7.2 Product Tests

- Existing tests continue to work (after import updates)
- Integration tests verify healthsim-common integration
- Product-specific validation tests remain

### 7.3 Migration Testing

- Create test script that validates:
  1. Old product code still runs (import aliases)
  2. New code using healthsim-common works
  3. Generated data is identical (seed reproducibility)

---

## 8. Next Steps

1. **Create healthsim-common repository**
   - Initialize with pyproject.toml
   - Setup CI/CD

2. **Extract Foundation** (Phase 2A)
   - config, validation.base, temporal, formats.base

3. **Extract Person & Generation** (Phase 2B)
   - person, generation.base, generation.person

4. **Extract Skills** (Phase 2C)
   - skills.schema, loader, composer

5. **Refactor Products**
   - Update imports to use healthsim-common
   - Product models extend Person
   - Product generators extend BaseGenerator

6. **Release healthsim-common v1.0.0**

7. **Release Updated Products**
   - Depend on healthsim-common

---

## Appendix A: File-by-File Classification Summary

| Module | File | Classification |
|--------|------|----------------|
| core | models.py | HYBRID |
| core | generator.py | HYBRID |
| core | reference_data.py | PRODUCT |
| validation | base.py | **CORE** |
| validation | structural.py | HYBRID |
| validation | product.py | PRODUCT |
| formats/* | transformers | PRODUCT |
| skills | schema.py | **CORE** |
| skills | loader.py | **CORE** |
| skills | composer.py | **CORE** |
| mcp | session.py | HYBRID |
| mcp | servers | PRODUCT |
| mcp | formatters.py | HYBRID |

**Summary:**
- **CORE (extract to healthsim-common)**: 4 files
- **HYBRID (split required)**: 6 files
- **PRODUCT (stays in product repos)**: Multiple files

---

## Appendix B: Import Migration Examples

### Before (current products)

```python
from product.validation.base import ValidationResult, ValidationSeverity
from product.core.models import ProductModel, Gender
from product.skills.loader import SkillLoader
```

### After (with healthsim-common)

```python
# Generic imports from healthsim-common
from healthsim.validation import ValidationResult, ValidationSeverity
from healthsim.person import Person, Gender
from healthsim.skills import SkillLoader

# Product imports from product package
from product.core.models import ProductModel  # ProductModel extends Person
from product.validation.product import ProductValidator
```

---

## See Also

- [Layered Architecture](layered-pattern.md) - Architecture overview
- [Extension Philosophy](../extensions/philosophy.md) - Adding capabilities
- [MCP Integration](../mcp/integration-guide.md) - MCP integration

---

*End of HealthSim Core Specification*
