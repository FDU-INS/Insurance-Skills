# RxMemberSim

Synthetic pharmacy and PBM data generation for prescription benefit simulations.

## Overview

RxMemberSim is part of the HealthSim workspace, providing realistic synthetic prescription data generation for pharmacy benefit management (PBM) simulation cohorts. It generates prescriptions, pharmacy claims, and supports NCPDP transaction formats.

## Features

- **Prescription Generation**: Realistic prescriptions with drug details and dosing
- **Pharmacy Claims**: NCPDP Telecommunication Standard claims
- **Drug Utilization Review**: DUR alerts and intervention tracking
- **Formulary Management**: Tier structures, step therapy, and quantity limits
- **Prior Authorization**: Electronic prior authorization (ePA) workflows
- **Specialty Pharmacy**: Hub services and specialty drug programs
- **Pricing Models**: AWP, MAC, rebates, and copay assistance

## Installation

```bash
cd packages/rxmembersim
pip install -e ".[dev]"
```

## Quick Start

```python
from rxmembersim.core import RxMemberGenerator, PrescriptionGenerator

# Generate pharmacy members
gen = RxMemberGenerator(seed=42)
members = gen.generate_many(count=10)

# Generate prescriptions
rx_gen = PrescriptionGenerator()
prescriptions = rx_gen.generate_for_member(members[0], rx_count=5)
```

## Profile-Based Generation

RxMemberSim supports the unified generation framework:

```python
from rxmembersim.generation import generate, quick_sample

# Generate from template
result = generate("medicare-partd-polypharmacy", count=100, seed=42)

# Quick sample
rx_members = quick_sample(count=10)

# Via unified healthsim API
import healthsim
result = healthsim.generate("rx", template="specialty-oncology", count=50)
```

### Available Templates

| Template | Description |
|----------|-------------|
| `commercial-healthy` | Minimal medication use |
| `commercial-chronic` | Multiple chronic conditions |
| `medicare-partd-standard` | Standard Part D beneficiary |
| `medicare-partd-polypharmacy` | 5+ medications |
| `medicare-partd-lis` | Low-income subsidy eligible |
| `specialty-oncology` | Oncology specialty drugs |
| `specialty-autoimmune` | Autoimmune specialty drugs |
| `ltc-nursing-home` | Long-term care residents |

## Architecture

```
rxmembersim/
├── core/           # Member, prescription, drug models
├── claims/         # Pharmacy claim adjudication
├── authorization/  # Prior auth and ePA
├── formulary/      # Formulary, tiers, step therapy
├── dur/            # Drug utilization review
├── specialty/      # Specialty pharmacy programs
├── pricing/        # Drug pricing and rebates
├── formats/        # NCPDP export (Telecom, SCRIPT, ePA)
├── dimensional/    # Star schema transforms
├── journeys/       # Journey templates and handlers
├── mcp/            # MCP server for AI integration
└── validation/     # Pharmacy validation
```

## Integration with Core

RxMemberSim uses the unified state management from `healthsim-core`:

```python
from healthsim.state import save_cohort, load_cohort

# Save generated prescriptions
save_cohort(
    name="specialty-rx-cohort",
    entities={"members": members, "prescriptions": prescriptions},
    tags=["specialty", "oncology"]
)
```

## NCPDP Export

```python
from rxmembersim.formats.ncpdp import NCPDPTelecomGenerator

# Generate NCPDP claim
generator = NCPDPTelecomGenerator()
ncpdp_claim = generator.generate(claim)
```

## Testing

```bash
cd packages/rxmembersim
pytest tests/ -v
```

## Related

- [HealthSim Core](../core/README.md) - Shared models and state management
- [RxMemberSim Skills](../../skills/rxmembersim/README.md) - AI conversation skills
- [MemberSim](../membersim/README.md) - Medical claims generation

## License

Apache 2.0
