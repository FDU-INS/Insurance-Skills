# MemberSim - Claude Code Guide

## Project Overview

MemberSim generates synthetic health plan member data for testing payer systems without PHI exposure. It's part of the HealthSim product family alongside PatientSim.

### Core Philosophy
- **Configuration as Conversation**: Users describe scenarios in natural language
- **Payer Domain Focus**: Enrollment, claims, payments, quality, authorization
- **Industry Standards**: X12 EDI transactions, HEDIS measures, FHIR

### Relationship to Other Projects
- **healthsim-core**: Shared foundation (demographics, temporal, generation, validation)
- **PatientSim**: Sibling product for clinical/EMR data (HL7v2, FHIR clinical)
- MemberSim uses healthsim-core but NOT PatientSim code directly

## Architecture

### Package Structure
```
membersim/
├── core/         # Member, Subscriber, Plan, Provider, Accumulator
├── claims/       # Claim, ClaimLine, Payment, generation
├── quality/      # HEDIS measures, care gaps, Star Ratings
├── authorization/# Prior auth, concurrent review
├── network/      # Provider contracts, fee schedules
├── vbc/          # Value-based care, attribution, capitation
├── formats/      # X12 (834/837/835/278/270), FHIR, CSV/JSON
├── mcp/          # MCP server for Claude Code tools
└── validation/   # Claim validators, consistency checks
```

### Key Design Principles
1. **Extend healthsim-core**: Use Person → Member, Timeline → Coverage periods
2. **Pydantic Models**: All entities are Pydantic BaseModel subclasses
3. **Immutable Where Possible**: Prefer frozen models for data integrity
4. **Deterministic Generation**: Seed support for reproducible output

## Payer Domain Knowledge

### X12 EDI Transactions
- **834**: Benefit enrollment (employer ↔ payer)
- **837P/I**: Professional/Institutional claims (provider → payer)
- **835**: Remittance advice (payer → provider)
- **278**: Prior authorization request/response
- **270/271**: Eligibility inquiry/response

### Key Entities
- **Member**: Person enrolled in health plan
- **Subscriber**: Primary policy holder (member with dependents)
- **Claim**: Request for payment (professional, institutional, dental, rx)
- **Authorization**: Pre-service approval for care
- **Provider**: Healthcare professional or facility in network
- **Accumulator**: Tracks deductible and OOP max progress

### HEDIS Quality Measures
- Breast Cancer Screening (BCS), Colorectal (COL), Cervical (CCS)
- Diabetes Care (CDC): A1C testing, eye exams, nephropathy
- Medication Adherence: PDC calculations
- Care gaps: Open vs. closed measure status

## Coding Standards

### Style
- **Formatter**: Ruff (line length 100)
- **Type Hints**: Required on all public functions
- **Docstrings**: Google style, required on public API

### Imports
```python
# Standard library
from datetime import date, datetime
from decimal import Decimal
from typing import Optional

# Third party
from pydantic import BaseModel, Field

# healthsim-core
from healthsim.person import Demographics
from healthsim.generation import BaseGenerator

# Local
from membersim.core.member import Member
```

### Testing
- pytest with conftest.py fixtures
- Test file naming: test_<module>.py
- Aim for 80%+ coverage on core modules
- Test reproducibility with fixed seeds

### Git Commits
```
type: Short description

- Detail 1
- Detail 2

Implements: REQ-XXX (if applicable)
```
Types: feat, fix, docs, test, refactor, chore

## Common Tasks

### Adding a New Model
1. Create model in appropriate package (core/, claims/, etc.)
2. Extend healthsim base if applicable
3. Add __all__ export in __init__.py
4. Write tests in tests/test_<module>.py
5. Update CLAUDE.md if significant

### Adding X12 Transaction Support
1. Create generator in formats/x12/edi_<type>.py
2. Define segment generators
3. Handle control numbers (ISA, GS, ST)
4. Test with valid X12 structure
5. Add to MCP tools if needed

### Adding HEDIS Measure
1. Define measure in quality/hedis.py
2. Specify denominator/numerator criteria
3. Create care gap detection logic
4. Test with sample member data

## Reference Data

### Place of Service Codes
- 11: Office
- 21: Inpatient Hospital
- 22: Outpatient Hospital
- 23: Emergency Room
- 31: Skilled Nursing Facility

### Claim Adjustment Reason Codes (CARC)
- 1: Deductible amount
- 2: Coinsurance amount
- 3: Copay amount
- 45: Exceeds fee schedule/maximum allowable
- 50: Non-covered service

### Relationship Codes (X12 834)
- 18: Self
- 01: Spouse
- 19: Child

## Do NOT Do

- Import PatientSim code directly (use healthsim-core instead)
- Include real PHI or realistic-looking SSNs
- Generate claims with invalid code combinations
- Create circular dependencies between packages
