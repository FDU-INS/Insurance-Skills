# MemberSim

Synthetic insurance member data generation for payer and claims simulations.

## Overview

MemberSim is part of the HealthSim workspace, providing realistic synthetic member data generation for healthcare insurance simulation cohorts. It generates members, subscribers, claims, and supports X12 EDI transaction formats.

## Features

- **Member Enrollment**: Generate member demographics, eligibility periods, and coverage
- **Claims Generation**: Professional (837P) and facility (837I) claims with realistic coding
- **Payment Processing**: Remittance advice (835) with adjudication details
- **Eligibility Management**: 834 enrollment transactions and 270/271 eligibility inquiries
- **Prior Authorization**: 278 authorization request/response generation
- **Value-Based Care**: Capitation, attribution, and quality measure cohorts
- **Network Contracts**: Fee schedules and provider network management

## Installation

```bash
cd packages/membersim
pip install -e ".[dev]"
```

## Quick Start

```python
from membersim.core import MemberGenerator, ClaimGenerator

# Generate members
gen = MemberGenerator(seed=42)
members = gen.generate_many(count=10, plan_type="commercial")

# Generate claims for a member
claim_gen = ClaimGenerator()
claims = claim_gen.generate_for_member(members[0], claim_count=5)
```

## Profile-Based Generation

MemberSim supports the unified generation framework for creating members from profile specifications:

```python
from membersim.generation import generate, list_templates, quick_sample

# List available templates
templates = list_templates()
# ['commercial-ppo-healthy', 'medicare-advantage-diabetic', ...]

# Generate from template
result = generate("commercial-ppo-healthy", count=100, seed=42)
print(f"Generated {result.count} members")

# Quick sample for testing
members = quick_sample(count=10)

# Or use the unified healthsim API
import healthsim
result = healthsim.generate("members", template="medicare-advantage-diabetic", count=50)
```

### Available Templates

| Template | Description |
|----------|-------------|
| `commercial-ppo-healthy` | Working-age adults with PPO coverage |
| `commercial-hdhp-young` | Young adults with high-deductible plans |
| `commercial-family-mix` | Diverse commercial population with families |
| `medicare-advantage-diabetic` | MA members with Type 2 diabetes |
| `medicare-original-healthy` | Traditional Medicare in good health |
| `medicaid-pediatric` | Children covered under Medicaid/CHIP |
| `medicaid-adult-expansion` | Adults covered under Medicaid expansion |
| `exchange-silver-plan` | ACA marketplace Silver plan members |

## Architecture

```
membersim/
├── core/           # Member, subscriber, plan models
├── claims/         # Claim generation and payment
├── authorization/  # Prior authorization
├── formats/        # X12 EDI export (834, 835, 837, 270/271, 278)
├── network/        # Provider contracts and fee schedules
├── quality/        # HEDIS measures and care gaps
├── vbc/            # Value-based care arrangements
├── dimensional/    # Star schema transforms
├── journeys/       # Journey templates and handlers
├── mcp/            # MCP server for AI integration
└── validation/     # Claims validation
```

## Integration with Core

MemberSim uses the unified state management from `healthsim-core`:

```python
from healthsim.state import save_cohort, load_cohort

# Save generated members
save_cohort(
    name="commercial-members-q1",
    entities={"members": members, "claims": claims},
    tags=["commercial", "2025-q1"]
)
```

## X12 Export

```python
from membersim.formats.x12 import EDI837Generator

# Generate 837P claim file
generator = EDI837Generator()
edi_content = generator.generate(claims, claim_type="professional")
```

## Testing

```bash
cd packages/membersim
pytest tests/ -v
```

## Related

- [HealthSim Core](../core/README.md) - Shared models and state management
- [MemberSim Skills](../../skills/membersim/README.md) - AI conversation skills
- [PatientSim](../patientsim/README.md) - Clinical data generation

## License

Apache 2.0
