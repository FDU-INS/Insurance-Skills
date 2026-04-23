# HealthSim Migration Plan: Skills-First Architecture

## Overview

This document outlines the phased migration from the current Python-library HealthSim architecture to a conversation-first Skills architecture. The migration follows a hybrid approach: **Knowledge Extraction + Fresh Build**.

---

## Migration Principles

1. **Extract knowledge, don't migrate code** - Domain expertise is the valuable asset
2. **PatientSim is the reference implementation** - Build once correctly, replicate pattern
3. **Templates enable consistency** - Standardize skill and script structures
4. **GitHub-first documentation** - README, getting started, examples are first-class
5. **Review checkpoints** - Validate before building

---

## Session Plan Overview

| Session | Focus | Duration | Deliverables | Review Point |
|---------|-------|----------|--------------|--------------|
| **Session 1** | Knowledge Extraction | 2-3 hours | Knowledge base document | ✅ Review before Session 2 |
| **Session 2** | Templates & Architecture | 1-2 hours | Skill/script templates, repo structure | ✅ Review before Session 3 |
| **Session 3** | PatientSim Reference Build | 3-4 hours | Complete PatientSim skill | ✅ Review before Session 4 |
| **Session 4** | MemberSim Build | 2-3 hours | Complete MemberSim skill | Optional review |
| **Session 5** | RxMemberSim Build | 2-3 hours | Complete RxMemberSim skill | Optional review |
| **Session 6** | MCP Server & Integration | 2-3 hours | Batch tools, CLI integrations | ✅ Review before Session 7 |
| **Session 7** | Documentation & Examples | 2-3 hours | README, getting started, examples | ✅ Final review |
| **Session 8** | Git Migration & Launch | 1-2 hours | Archive old, publish new | Launch |

**Total estimated time: 16-23 hours across 8 sessions**

---

## Session 1: Knowledge Extraction

### Objective
Extract all domain knowledge from existing Python codebases into a structured document that serves as the authoritative reference for building new skills.

### Inputs (What I'll Read)
```
Existing Repositories:
├── healthsim-common/
│   ├── src/healthsim/person/       → Demographics, identifiers
│   ├── src/healthsim/temporal/     → Timeline, date utilities
│   ├── src/healthsim/generation/   → Distributions, seeds
│   ├── src/healthsim/validation/   → Validation framework
│   └── src/healthsim/formats/      → Base transformer patterns
│
├── patientsim/
│   ├── src/patientsim/models/      → Patient, Encounter, etc.
│   ├── src/patientsim/validation/  → Clinical validators
│   ├── src/patientsim/formats/     → FHIR, HL7v2, MIMIC
│   ├── src/patientsim/skills/      → Original Python skills
│   └── skills/                     → Any markdown skills
│
├── membersim/
│   ├── src/membersim/models/       → Member, Claim, etc.
│   ├── src/membersim/adjudication/ → Claims processing
│   ├── src/membersim/formats/      → X12 transformers
│   └── skills/
│
├── rxmembersim/
│   ├── src/rxmembersim/models/     → Prescription, Formulary
│   ├── src/rxmembersim/ncpdp/      → NCPDP logic
│   ├── src/rxmembersim/dur/        → Drug utilization review
│   └── skills/
│
└── Recently Created Skills (15 files)
    ├── diabetes-management-skill.md
    ├── heart-failure-skill.md
    ├── membersim-professional-claims-skill.md
    └── [etc.]
```

### Output: Knowledge Base Document

```markdown
# HealthSim Domain Knowledge Base
# Version 1.0 - Extracted [date]

## Table of Contents
1. Data Models & Schemas
2. Validation Rules
3. Format Specifications
4. Reference Data Catalog
5. Cohort Patterns
6. Generation Logic
7. Code System Mappings

---

## 1. Data Models & Schemas

### 1.1 PatientSim Entities

#### Patient
[Fields, types, constraints, relationships extracted from Pydantic model]

#### Encounter
[...]

### 1.2 MemberSim Entities

#### Member
[...]

#### Claim
[...]

### 1.3 RxMemberSim Entities

#### Prescription
[...]

---

## 2. Validation Rules

### 2.1 Clinical Plausibility (PatientSim)

#### Age-Condition Rules
| Condition Category | Age Range | Notes |
|-------------------|-----------|-------|
| Pediatric conditions | 0-17 | [specific codes] |
| [etc.] | | |

#### Medication-Diagnosis Coherence
[Rules extracted from clinical validators]

#### Lab Value Ranges
| Lab Test | Normal Range | Units | Condition Variations |
|----------|--------------|-------|---------------------|
| A1C | 4.0-5.6% | % | Diabetes: 6.5-14% |
| [etc.] | | | |

### 2.2 Claims Validation (MemberSim)
[...]

### 2.3 Pharmacy Validation (RxMemberSim)
[...]

---

## 3. Format Specifications

### 3.1 FHIR R4 Mappings

#### Patient → FHIR Patient
| Internal Field | FHIR Path | Transform |
|---------------|-----------|-----------|
| patient_id | Patient.id | Direct |
| name.family | Patient.name[0].family | Direct |
| [etc.] | | |

#### Encounter → FHIR Encounter
[...]

### 3.2 HL7v2 Segment Structures

#### ADT^A01 Message Structure
[Segment definitions, field mappings]

### 3.3 X12 837 Professional
[...]

### 3.4 NCPDP D.0
[...]

---

## 4. Reference Data Catalog

### 4.1 Code Systems Used

| System | Source | Records | Usage |
|--------|--------|---------|-------|
| ICD-10-CM | CMS | ~500 common | Diagnoses |
| CPT | AMA | ~200 common | Procedures |
| NDC | FDA | ~1000 common | Medications |
| LOINC | Regenstrief | ~100 common | Lab tests |
| RxNorm | NLM | ~500 common | Drug concepts |

### 4.2 Reference Data Files

| File | Content | Records | Source |
|------|---------|---------|--------|
| icd10-common.csv | Common diagnosis codes | ~500 | Extracted from validators |
| [etc.] | | | |

---

## 5. Cohort Patterns

### 5.1 Clinical Cohorts (PatientSim)

#### Diabetes Management
- **Variations**: New diagnosis, well-controlled, uncontrolled, with complications
- **Event sequence**: [from existing skills]
- **Key data points**: A1C, medications, encounters
- **Quality measures**: Diabetes care measures

#### Heart Failure
[...]

### 5.2 Claims Cohorts (MemberSim)
[...]

### 5.3 Pharmacy Cohorts (RxMemberSim)
[...]

---

## 6. Generation Logic

### 6.1 Distribution Patterns

#### Age Distribution (Default)
| Age Band | Weight | Notes |
|----------|--------|-------|
| 0-17 | 0.15 | Pediatric |
| 18-44 | 0.30 | Young adult |
| 45-64 | 0.30 | Middle age |
| 65+ | 0.25 | Senior |

#### Gender Distribution
[...]

### 6.2 Identifier Patterns

| Identifier | Format | Example |
|------------|--------|---------|
| MRN | 8 digits | 12345678 |
| SSN | XXX-XX-XXXX | 123-45-6789 |
| NPI | 10 digits | 1234567890 |
| [etc.] | | |

---

## 7. Code System Mappings

### 7.1 Condition → Medication Mappings
| Condition (ICD-10) | Typical Medications (RxNorm) |
|--------------------|------------------------------|
| E11.9 (T2DM) | Metformin (860975), ... |
| [etc.] | |

### 7.2 Diagnosis → Lab Test Mappings
[...]

---

## Appendix A: Original Source File Index
[List of all files read during extraction with line counts]

## Appendix B: Decisions & Assumptions
[Any interpretation decisions made during extraction]
```

### Review Checkpoint

**Before proceeding to Session 2, you should review:**
1. Completeness - Is any domain knowledge missing?
2. Accuracy - Are the rules/mappings correct?
3. Priority - Which cohorts are most important to implement first?

---

## Session 2: Templates & Architecture

### Objective
Create standardized templates for skills, scripts, and repository structure. These templates ensure consistency across all three products.

### Deliverables

#### 2.1 Repository Structure Template

```
healthsim/
├── .github/
│   ├── workflows/
│   │   ├── test.yml              # Run script tests
│   │   └── validate-skills.yml   # Validate skill format
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   ├── feature_request.md
│   │   └── new_cohort.md
│   └── PULL_REQUEST_TEMPLATE.md
│
├── skills/
│   ├── patientsim/
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   ├── references/
│   │   └── skills/
│   ├── membersim/
│   │   └── [same structure]
│   ├── rxmembersim/
│   │   └── [same structure]
│   └── shared/
│       ├── references/
│       └── scripts/
│
├── mcp-server/
│   ├── src/healthsim_mcp/
│   │   ├── __init__.py
│   │   ├── server.py
│   │   └── tools/
│   ├── tests/
│   ├── pyproject.toml
│   └── README.md
│
├── docs/
│   ├── getting-started.md
│   ├── user-guide/
│   │   ├── patientsim.md
│   │   ├── membersim.md
│   │   └── rxmembersim.md
│   ├── developer-guide/
│   │   ├── adding-cohorts.md
│   │   ├── adding-formats.md
│   │   └── architecture.md
│   └── api/
│       └── mcp-tools.md
│
├── examples/
│   ├── conversations/
│   │   ├── simple-patient.md
│   │   ├── diabetes-cohort.md
│   │   └── claims-testing.md
│   ├── outputs/
│   │   ├── sample-patient.json
│   │   ├── sample-fhir-bundle.json
│   │   └── sample-hl7v2.txt
│   └── notebooks/
│       └── analytics-examples.sql
│
├── tests/
│   ├── test_validation_scripts.py
│   ├── test_export_scripts.py
│   └── test_mcp_tools.py
│
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── CHANGELOG.md
└── pyproject.toml              # For MCP server only
```

#### 2.2 Skill Template (SKILL.md)

```markdown
---
name: [product]-sim
description: |
  [One paragraph description of what this skill does and when Claude should use it.
  Include trigger phrases that should activate this skill.]
version: 1.0.0
author: HealthSim Team
---

# [Product]Sim

[One paragraph overview of the product's purpose]

## Quick Start

```
User: [Simple example request]
Claude: [Brief response description]
```

## Workflow

When generating [entities], follow this workflow:

1. **Understand the request** - Identify cohort, count, variations
2. **Load cohort** - Read appropriate `skills/*.md` file
3. **Generate data** - Create canonical JSON per `references/canonical-model.md`
4. **Validate** - Run `scripts/validate_[entity].py`
5. **Export** - Transform to requested format via `scripts/export_*.py`

## Available Cohorts

| Cohort | File | Description | Triggers |
|----------|------|-------------|----------|
| [Name] | `skills/[name].md` | [Description] | "[trigger phrases]" |

## Output Formats

| Format | Script | Description |
|--------|--------|-------------|
| JSON (canonical) | Native | Internal representation |
| FHIR R4 | `scripts/export_fhir.py` | FHIR Bundle |
| HL7v2 | `scripts/export_hl7v2.py` | Pipe-delimited messages |
| CSV | `scripts/export_csv.py` | Flat file export |
| Parquet | `scripts/export_parquet.py` | Columnar format |

## Batch Generation

For generating multiple [entities]:

- **Conversation-first**: Claude generates SQL directly for any count
- **File export**: `healthsim.write_parquet` - Write to Parquet files
- **Databricks**: Claude uses `databricks sql -e` CLI (no MCP needed)

## Validation

All generated data is validated for:
- Structural integrity (required fields, types)
- [Domain-specific validation rules]
- Temporal consistency
- Code validity (ICD-10, CPT, etc.)

## Reference Files

| File | Purpose |
|------|---------|
| `references/canonical-model.md` | JSON schema for [entity] |
| `references/[codes].csv` | [Description] |

## Extension

To add new cohorts, see `skills/_template.md`.
```

#### 2.3 Cohort Template (skills/_template.md)

```markdown
# [Cohort Name]

## Overview

**Purpose:** [What this cohort represents]
**Complexity:** [Simple | Moderate | Complex]
**Typical Use:** [When users would request this]

## Trigger Phrases

Users might request this cohort with phrases like:
- "[phrase 1]"
- "[phrase 2]"
- "[phrase 3]"

## Patient/Member/Prescription Profile

### Demographics
- **Age range:** [range]
- **Gender:** [any | specific]
- **Other criteria:** [if applicable]

### Clinical/Claims Characteristics
[Key attributes that define this cohort]

## Variations

### Variation 1: [Name]
**Trigger:** "[specific phrase]"
**Characteristics:**
- [Key difference 1]
- [Key difference 2]

### Variation 2: [Name]
[...]

## Event Sequence

```yaml
timeline:
  - event: [event_type]
    timing: [when]
    details:
      [key]: [value]
  
  - event: [event_type]
    timing: [relative to previous]
    details:
      [key]: [value]
```

## Key Data Points

| Element | Value/Range | Notes |
|---------|-------------|-------|
| [Field] | [Value] | [Why this value] |

## Diagnosis/Procedure Codes

| Code | System | Display | When Used |
|------|--------|---------|-----------|
| [code] | [ICD-10/CPT/etc] | [description] | [condition] |

## Medications (if applicable)

| Medication | Code | Dosing | Duration |
|------------|------|--------|----------|
| [name] | [RxNorm] | [dose] | [duration] |

## Example Output

```json
{
  // Minimal example showing key fields for this cohort
}
```

## Quality Measures (if applicable)

This cohort supports testing:
- [Measure 1]
- [Measure 2]

## Related Cohorts

- `[related-cohort.md]` - [relationship]
```

#### 2.4 Validation Script Template

```python
#!/usr/bin/env python3
"""
Validate [Entity] data for structural integrity and domain rules.

Usage:
    python validate_[entity].py input.json
    python validate_[entity].py --stdin < input.json

Exit codes:
    0 - Validation passed
    1 - Validation failed (errors in output)
    2 - Script error (invalid input, etc.)
"""
import json
import sys
import argparse
from datetime import datetime
from typing import Any
from pathlib import Path

# Validation result structure
class ValidationResult:
    def __init__(self):
        self.errors: list[dict] = []
        self.warnings: list[dict] = []
    
    def add_error(self, field: str, message: str, value: Any = None):
        self.errors.append({"field": field, "message": message, "value": value})
    
    def add_warning(self, field: str, message: str, value: Any = None):
        self.warnings.append({"field": field, "message": message, "value": value})
    
    @property
    def is_valid(self) -> bool:
        return len(self.errors) == 0
    
    def to_dict(self) -> dict:
        return {
            "valid": self.is_valid,
            "error_count": len(self.errors),
            "warning_count": len(self.warnings),
            "errors": self.errors,
            "warnings": self.warnings
        }


def validate_required_fields(data: dict, result: ValidationResult) -> None:
    """Check that all required fields are present."""
    required = ["[field1]", "[field2]"]  # Update per entity
    
    for field in required:
        if field not in data or data[field] is None:
            result.add_error(field, f"Required field '{field}' is missing")


def validate_field_types(data: dict, result: ValidationResult) -> None:
    """Check that fields have correct types."""
    # Add type checks per entity schema
    pass


def validate_domain_rules(data: dict, result: ValidationResult) -> None:
    """Check domain-specific business rules."""
    # Add domain validation logic
    pass


def validate_temporal_consistency(data: dict, result: ValidationResult) -> None:
    """Check that dates/times are logically consistent."""
    # Add temporal validation logic
    pass


def validate_code_values(data: dict, result: ValidationResult) -> None:
    """Validate code values against reference data."""
    # Load reference CSVs and check codes
    pass


def validate(data: dict) -> ValidationResult:
    """Run all validations on the input data."""
    result = ValidationResult()
    
    validate_required_fields(data, result)
    validate_field_types(data, result)
    validate_domain_rules(data, result)
    validate_temporal_consistency(data, result)
    validate_code_values(data, result)
    
    return result


def main():
    parser = argparse.ArgumentParser(description="Validate [Entity] data")
    parser.add_argument("input", nargs="?", help="Input JSON file (or use --stdin)")
    parser.add_argument("--stdin", action="store_true", help="Read from stdin")
    parser.add_argument("--quiet", action="store_true", help="Only output on failure")
    args = parser.parse_args()
    
    try:
        if args.stdin:
            data = json.load(sys.stdin)
        elif args.input:
            with open(args.input) as f:
                data = json.load(f)
        else:
            parser.error("Provide input file or use --stdin")
            return 2
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"Invalid JSON: {e}"}))
        return 2
    except FileNotFoundError:
        print(json.dumps({"error": f"File not found: {args.input}"}))
        return 2
    
    result = validate(data)
    
    if not args.quiet or not result.is_valid:
        print(json.dumps(result.to_dict(), indent=2))
    
    return 0 if result.is_valid else 1


if __name__ == "__main__":
    sys.exit(main())
```

#### 2.5 Export Script Template

```python
#!/usr/bin/env python3
"""
Export [Entity] data to [Format] format.

Usage:
    python export_[format].py input.json output.[ext]
    python export_[format].py --stdin < input.json > output.[ext]

Supports single entity or array of entities.
"""
import json
import sys
import argparse
from typing import Any
from pathlib import Path

def transform_single(data: dict) -> Any:
    """Transform a single entity to [Format]."""
    # Implement transformation logic
    result = {
        # Map fields according to format spec
    }
    return result


def transform_batch(data: list[dict]) -> Any:
    """Transform multiple entities to [Format]."""
    return [transform_single(item) for item in data]


def transform(data: dict | list) -> Any:
    """Transform input data to [Format]."""
    if isinstance(data, list):
        return transform_batch(data)
    else:
        return transform_single(data)


def format_output(result: Any) -> str:
    """Format the result for output."""
    # JSON output example - adjust per format
    return json.dumps(result, indent=2)


def main():
    parser = argparse.ArgumentParser(description="Export to [Format]")
    parser.add_argument("input", nargs="?", help="Input JSON file")
    parser.add_argument("output", nargs="?", help="Output file")
    parser.add_argument("--stdin", action="store_true", help="Read from stdin")
    parser.add_argument("--stdout", action="store_true", help="Write to stdout")
    args = parser.parse_args()
    
    try:
        if args.stdin:
            data = json.load(sys.stdin)
        elif args.input:
            with open(args.input) as f:
                data = json.load(f)
        else:
            parser.error("Provide input file or use --stdin")
            return 2
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON - {e}", file=sys.stderr)
        return 2
    
    result = transform(data)
    output = format_output(result)
    
    if args.stdout or not args.output:
        print(output)
    else:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"Exported to {args.output}", file=sys.stderr)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

### Review Checkpoint

**Before proceeding to Session 3, you should review:**
1. Repository structure - Does this organization make sense?
2. Templates - Are they complete and clear?
3. Any additions needed for your use cases?

---

## Session 3: PatientSim Reference Build

### Objective
Build the complete PatientSim skill as the reference implementation that other products will follow.

### Deliverables

```
skills/patientsim/
├── SKILL.md                          # Main skill file (YAML frontmatter)
├── scripts/
│   ├── validate_patient.py           # Structural + clinical validation
│   ├── export_fhir.py               # FHIR R4 Bundle export
│   ├── export_hl7v2.py              # HL7v2 ADT messages
│   ├── export_csv.py                # Flat file export
│   ├── export_json.py               # Pretty JSON (passthrough with formatting)
│   └── export_parquet.py            # Columnar format
├── references/
│   ├── canonical-model.md           # JSON schema documentation
│   ├── canonical-schema.json        # Formal JSON Schema (optional)
│   ├── icd10-common.csv             # Common diagnosis codes
│   ├── medications.csv              # Common medications with RxNorm
│   ├── lab-tests.csv                # Lab tests with LOINC + normal ranges
│   ├── vital-signs.csv              # Vital sign definitions
│   └── fhir-mappings.md             # Field mapping documentation
└── skills/
    ├── _template.md                 # Template for new cohorts
    ├── diabetes.md                  # Diabetes management (enhanced)
    ├── heart-failure.md             # Heart failure (enhanced)
    ├── ckd.md                       # Chronic kidney disease (enhanced)
    ├── healthy-adult.md             # Baseline healthy patient
    └── multi-chronic.md             # Multiple chronic conditions
```

### Build Sequence

1. **Canonical Model** (references/canonical-model.md)
   - Extract from Pydantic models
   - Document as JSON schema in markdown
   - Include examples for each entity

2. **Reference Data** (references/*.csv)
   - Extract from existing reference_data.py
   - Format as CSV with headers
   - Include common codes only (not exhaustive)

3. **Validation Script** (scripts/validate_patient.py)
   - Extract rules from clinical validators
   - Implement as standalone script
   - Test with valid and invalid samples

4. **Export Scripts** (scripts/export_*.py)
   - Port transformer logic from existing code
   - FHIR: Full R4 Bundle with Patient, Encounter, Condition, Observation
   - HL7v2: ADT^A01, ADT^A03 messages
   - CSV: Flattened patient records
   - Parquet: Using pyarrow

5. **Cohorts** (skills/*.md)
   - Merge existing skills with new format
   - Add event sequences
   - Include variation triggers

6. **Main Skill** (SKILL.md)
   - Proper YAML frontmatter
   - Comprehensive workflow documentation
   - Link all components

### Validation

Test the complete skill with sample conversations:
- Simple patient generation
- Cohort-specific generation (diabetes)
- Batch generation request
- Export to each format

### Review Checkpoint

**Before proceeding to Session 4, you should:**
1. Test PatientSim skill in Claude Project
2. Verify export scripts produce valid output
3. Confirm validation catches expected errors
4. Approve pattern for replication

---

## Session 4: MemberSim Build

### Objective
Build MemberSim following the PatientSim pattern.

### Deliverables

```
skills/membersim/
├── SKILL.md
├── scripts/
│   ├── validate_member.py
│   ├── validate_claim.py
│   ├── adjudicate_claim.py          # Claims adjudication logic
│   ├── export_x12_837p.py           # Professional claim
│   ├── export_x12_837i.py           # Institutional claim
│   ├── export_x12_835.py            # Remittance advice
│   ├── export_x12_834.py            # Enrollment
│   ├── export_csv.py
│   ├── export_json.py
│   └── export_parquet.py
├── references/
│   ├── canonical-model.md
│   ├── member-schema.json
│   ├── claim-schema.json
│   ├── cpt-common.csv
│   ├── drg-weights.csv
│   ├── place-of-service.csv
│   ├── plan-types.csv
│   └── x12-mappings.md
└── skills/
    ├── _template.md
    ├── professional-claims.md       # From existing skill
    ├── facility-claims.md           # From existing skill
    ├── prior-auth.md                # From existing skill
    ├── enrollment-eligibility.md    # From existing skill
    ├── value-based-care.md          # From existing skill
    └── accumulator-tracking.md      # From existing skill
```

### Key Differences from PatientSim

- **Adjudication script**: New - processes claims through benefit rules
- **X12 exports**: Multiple transaction types
- **Dual validation**: Both member and claim validation

---

## Session 5: RxMemberSim Build

### Objective
Build RxMemberSim following the PatientSim pattern.

### Deliverables

```
skills/rxmembersim/
├── SKILL.md
├── scripts/
│   ├── validate_prescription.py
│   ├── validate_pharmacy_claim.py
│   ├── adjudicate_rx_claim.py
│   ├── check_formulary.py           # Formulary lookup
│   ├── run_dur.py                   # Drug utilization review
│   ├── export_ncpdp_b1b2.py         # Billing request/response
│   ├── export_ncpdp_script.py       # NCPDP SCRIPT (eRx)
│   ├── export_csv.py
│   ├── export_json.py
│   └── export_parquet.py
├── references/
│   ├── canonical-model.md
│   ├── prescription-schema.json
│   ├── ndc-common.csv
│   ├── pharmacy-types.csv
│   ├── formulary-tiers.csv
│   ├── dur-codes.csv
│   └── ncpdp-mappings.md
└── skills/
    ├── _template.md
    ├── retail-pharmacy.md           # From existing skill
    ├── specialty-pharmacy.md        # From existing skill
    ├── prior-auth.md                # From existing skill
    ├── formulary-management.md      # From existing skill
    ├── manufacturer-programs.md     # From existing skill
    └── drug-utilization-review.md   # From existing skill
```

### Key Differences from PatientSim

- **Formulary script**: New - checks drug coverage
- **DUR script**: New - drug interaction checking
- **NCPDP exports**: Pharmacy-specific formats

---

## Session 6: MCP Server & Integration

### Objective
Build the MCP server for batch operations and external integrations.

### Deliverables

```
mcp-server/
├── src/healthsim_mcp/
│   ├── __init__.py
│   ├── server.py                    # Main MCP server
│   └── tools/
│       ├── __init__.py
│       ├── batch_generate.py        # Generate cohorts
│       ├── write_parquet.py         # Write to Parquet
│       ├── write_csv.py             # Write to CSV
│       ├── run_cohort.py          # Execute multi-event cohort
│       └── validate_batch.py        # Validate multiple entities
├── tests/
│   ├── test_batch_generate.py
│   ├── test_write_tools.py
│   └── conftest.py
├── pyproject.toml
├── README.md
└── .env.example
```

**Note**: Databricks integration uses conversation-first approach (no MCP tool needed).
Claude generates SQL and executes via `databricks sql -e` CLI, trusting existing CLI auth.

### MCP Tool Specifications

```python
@app.tool()
async def batch_generate(
    product: str,           # "patientsim" | "membersim" | "rxmembersim"
    cohort: str,          # cohort name from cohorts/
    count: int,             # number to generate
    seed: int | None,       # optional seed for reproducibility
    parameters: dict        # cohort-specific parameters
) -> list[dict]:
    """Generate multiple entities based on cohort."""

@app.tool()
async def write_parquet(
    data: list[dict],
    output_path: str,
    partition_by: list[str] | None = None
) -> dict:
    """Write entities to Parquet file(s)."""

@app.tool()
async def run_cohort(
    product: str,
    cohort: str,
    entity_context: dict,   # existing entity to build upon
    duration: str,          # "30_days", "6_months", etc.
    output_format: str      # "json" | "fhir" | "hl7v2" | etc.
) -> dict:
    """Execute multi-event cohort over time period."""
```

### Review Checkpoint

**Before proceeding to Session 7:**
1. Test MCP server locally
2. Verify Databricks CLI auth works (`databricks auth profiles`)
3. Test batch generation at scale (100+ entities)

---

## Session 7: Documentation & Examples

### Objective
Create comprehensive documentation for the GitHub repository.

### Deliverables

#### README.md (Root)

```markdown
# HealthSim

**Synthetic healthcare data through conversation**

Generate realistic patients, claims, and prescriptions for testing
healthcare systems—without risking real patient information.

## Products

| Product | Description | Status |
|---------|-------------|--------|
| **PatientSim** | Clinical/EMR patient data | ✅ Ready |
| **MemberSim** | Health plan member & claims data | ✅ Ready |
| **RxMemberSim** | Pharmacy benefits data | ✅ Ready |

## Quick Start

### 1. Add Skills to Claude Project

[Instructions for adding skills to Claude Project]

### 2. Start a Conversation

```
You: Generate a diabetic patient with 6 months of encounter history

Claude: I'll create a Type 2 diabetes patient with quarterly visits...
        [Generates patient with encounters, labs, medications]
```

### 3. Export Your Data

```
You: Export that patient as a FHIR Bundle

Claude: [Runs export script, provides FHIR R4 Bundle]
```

## Documentation

- [Getting Started Guide](docs/getting-started.md)
- [PatientSim User Guide](docs/user-guide/patientsim.md)
- [MemberSim User Guide](docs/user-guide/membersim.md)
- [RxMemberSim User Guide](docs/user-guide/rxmembersim.md)
- [Adding New Cohorts](docs/developer-guide/adding-cohorts.md)

## Examples

- [Conversation Examples](examples/conversations/)
- [Sample Outputs](examples/outputs/)
- [Analytics Examples](examples/notebooks/analytics-examples.sql)

## Installation (MCP Server)

For batch operations and database integration:

```bash
# Clone repository
git clone https://github.com/[org]/healthsim.git
cd healthsim/mcp-server

# Install
pip install -e .

# Configure Claude Desktop
# Add to claude_desktop_config.json
```

## License

Apache 2.0

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)
```

#### docs/getting-started.md

```markdown
# Getting Started with HealthSim

This guide will have you generating synthetic healthcare data in minutes.

## Prerequisites

- Claude Pro or Team account (for Claude Projects)
- OR Claude API access
- Python 3.10+ (for export scripts and MCP server)

## Setup Options

### Option 1: Claude Project (Recommended)

1. Create a new Claude Project
2. Add HealthSim skills to project knowledge
3. Start conversing

[Detailed steps with screenshots]

### Option 2: Claude Desktop with MCP

1. Install MCP server
2. Configure Claude Desktop
3. Skills automatically available

[Detailed steps]

### Option 3: API Integration

[For programmatic access]

## Your First Patient

[Step-by-step conversation example]

## Your First Claim

[Step-by-step conversation example]

## Exporting Data

[How to get data out in various formats]

## Next Steps

- Explore [clinical cohorts](../skills/patientsim/)
- Try [batch generation](user-guide/batch-generation.md)
- Load data to [analytics databases](user-guide/analytics-integration.md) (DuckDB, Databricks)
```

#### Example Conversations

```markdown
# Example: Diabetes Testing Cohort

## Goal
Generate 50 diabetic patients with varying A1C levels for testing
a diabetes management dashboard.

## Conversation

**You:**
> I need to test our diabetes dashboard. Can you generate 50 Type 2 
> diabetes patients with a mix of well-controlled and uncontrolled A1C?

**Claude:**
> I'll create a diabetes testing cohort with varied glycemic control.
>
> **Cohort Distribution:**
> - 20 patients: Well-controlled (A1C 6.5-7.0%)
> - 15 patients: Moderately controlled (A1C 7.0-8.0%)
> - 10 patients: Poorly controlled (A1C 8.0-10.0%)
> - 5 patients: Severely uncontrolled (A1C > 10.0%)
>
> Each patient will have:
> - 6-12 months of encounter history
> - Appropriate medications (metformin, SGLT2i, GLP-1, insulin as needed)
> - Quarterly A1C labs
> - Related conditions (hypertension, hyperlipidemia as appropriate)
>
> [Calls batch_generate tool]
>
> ✓ Generated 50 patients
>
> Would you like me to:
> 1. Export as FHIR Bundles for your dashboard?
> 2. Load directly to your Databricks test environment?
> 3. Show sample patients from each control category?

[Conversation continues...]
```

### Review Checkpoint

**Before proceeding to Session 8:**
1. Review all documentation for clarity
2. Test getting started guide end-to-end
3. Verify examples work as documented

---

## Session 8: Git Migration & Launch

### Objective
Archive old repositories and publish new HealthSim repository.

### Git Operations

#### Step 1: Archive Old Repositories

```bash
# For each old repo (healthsim-common, patientsim, membersim, rxmembersim)

# Option A: Archive on GitHub (recommended)
# Go to Settings > Archive this repository

# Option B: Rename with -archived suffix
gh repo rename healthsim-common healthsim-common-archived
```

#### Step 2: Create New Repository

```bash
# Create new repo
gh repo create healthsim --public --description "Synthetic healthcare data through conversation"

# Clone locally
git clone https://github.com/[org]/healthsim.git
cd healthsim
```

#### Step 3: Initialize Structure

```bash
# Create directory structure
mkdir -p skills/{patientsim,membersim,rxmembersim}/{scripts,references,cohorts}
mkdir -p skills/shared/{references,scripts}
mkdir -p mcp-server/src/healthsim_mcp/tools
mkdir -p mcp-server/tests
mkdir -p docs/{user-guide,developer-guide,api}
mkdir -p examples/{conversations,outputs,notebooks}
mkdir -p tests
mkdir -p .github/{workflows,ISSUE_TEMPLATE}

# Create placeholder files
touch skills/patientsim/SKILL.md
touch skills/membersim/SKILL.md
touch skills/rxmembersim/SKILL.md
# ... etc
```

#### Step 4: Copy Built Assets

```bash
# Copy all built skills, scripts, docs from working directory
# (Details depend on where Session 3-7 outputs are stored)
```

#### Step 5: Initial Commit

```bash
git add -A
git commit -m "Initial HealthSim Skills-First Architecture

- PatientSim: Clinical patient generation
- MemberSim: Health plan claims generation
- RxMemberSim: Pharmacy benefits generation
- MCP Server: Batch operations and integrations
- Documentation: Getting started, user guides, examples

Architecture: Conversation-first design using Claude Skills
with Python scripts for validation and format export."
```

#### Step 6: Create Release

```bash
git tag -a v1.0.0 -m "HealthSim 1.0.0 - Skills-First Architecture"
git push origin main --tags

# Create GitHub release with notes
gh release create v1.0.0 --title "HealthSim 1.0.0" --notes "Initial release..."
```

#### Step 7: Update Old Repo READMEs

For each archived repo, update README to point to new location:

```markdown
# ⚠️ This Repository Has Been Archived

This repository has been superseded by the new HealthSim Skills-First Architecture.

**New Repository:** https://github.com/[org]/healthsim

The new architecture provides:
- Conversation-first design (no Python required for basic use)
- Unified repository for all products
- Simpler setup and extension

Please use the new repository for all future work.
```

### Launch Checklist

- [ ] All skills tested in Claude Project
- [ ] All export scripts produce valid output
- [ ] MCP server functional
- [ ] Documentation complete and accurate
- [ ] Getting started guide tested end-to-end
- [ ] Old repositories archived with redirect
- [ ] New repository public
- [ ] v1.0.0 release created
- [ ] Announcement ready (if applicable)

---

## Appendix: Session Prompts

### Session 1 Kickoff Prompt

```
I'm ready to begin HealthSim knowledge extraction.

Please read the following repositories and extract domain knowledge 
into the structured format we discussed:

1. healthsim-common at [path]
2. patientsim at [path]
3. membersim at [path]
4. rxmembersim at [path]
5. Recent skills at [path]

Create the Knowledge Base Document covering:
- Data models & schemas
- Validation rules
- Format specifications
- Reference data catalog
- Cohort patterns
- Generation logic
- Code system mappings

Output as a single comprehensive markdown document.
```

### Session 3 Kickoff Prompt

```
I'm ready to build the PatientSim reference implementation.

Using:
- The approved Knowledge Base Document
- The approved templates from Session 2
- The repository structure we defined

Build the complete PatientSim skill:
1. SKILL.md with proper YAML frontmatter
2. Canonical model in references/
3. Reference data CSVs
4. Validation script
5. Export scripts (FHIR, HL7v2, CSV, JSON, Parquet)
6. Enhanced cohorts (diabetes, heart-failure, ckd, healthy-adult)

Follow the templates exactly. Test each component.
```

[Similar prompts for Sessions 4-8...]

---

## Questions Before We Begin?

1. **Repository location**: Where are your current repos? (Local path or GitHub URLs)
2. **GitHub organization**: Personal account or organization?
3. **Databricks testing**: Do you have a test environment available?
4. **Timeline**: Any deadline considerations?
5. **Session scheduling**: Preferred session length/frequency?
