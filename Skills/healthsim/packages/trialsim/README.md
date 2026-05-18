# TrialSim

Synthetic clinical trial data generation for CDISC/SDTM formats.

## Overview

TrialSim generates realistic clinical trial data including:
- **Subjects**: Trial participants with demographics and eligibility
- **Protocol Visits**: Scheduled and unscheduled visit events
- **Adverse Events**: AE/SAE with severity, causality, and outcomes
- **Exposures**: Drug exposure records with dosing information
- **Lab Results**: Central and local laboratory data
- **Efficacy Data**: Response assessments and endpoints

## Installation

```bash
cd packages/trialsim
pip install -e ".[dev]"
```

## Quick Start

```python
from trialsim import TrialSubjectGenerator, VisitGenerator

# Generate trial subjects
subject_gen = TrialSubjectGenerator(seed=42)
subjects = subject_gen.generate_many(100, protocol_id="PROTO-001")

# Generate visits for a subject
visit_gen = VisitGenerator()
visits = visit_gen.generate_schedule(
    subject=subjects[0],
    duration_weeks=52
)

# Generate adverse events
from trialsim import AdverseEventGenerator
ae_gen = AdverseEventGenerator()
aes = ae_gen.generate_for_subject(subjects[0], visit_count=len(visits))
```

## Profile-Based Generation

TrialSim supports the unified generation framework:

```python
from trialsim.generation import generate, quick_sample

# Generate from template
result = generate("phase3-oncology-trial", count=200, seed=42)
print(f"Generated {result.count} subjects")

# Quick sample
subjects = quick_sample(count=10)

# Via unified healthsim API
import healthsim
result = healthsim.generate("trials", template="phase2-diabetes-trial", count=100)
```

### Available Templates

| Template | Description |
|----------|-------------|
| `phase3-oncology-trial` | Phase 3 oncology RCT |
| `phase2-diabetes-trial` | Phase 2 diabetes study |
| `phase1-healthy-volunteers` | Phase 1 PK/PD study |
| `observational-registry` | Non-interventional registry |
| `rare-disease-trial` | Small rare disease study |

## Architecture

```
trialsim/
├── core/           # Core models (Subject, Visit, AE)
├── protocol/       # Protocol definitions and schedules
├── subjects/       # Subject generation and enrollment
├── visits/         # Visit scheduling and events
├── adverse_events/ # AE/SAE generation
├── exposures/      # Drug exposure records
├── formats/        # CDISC/SDTM export
├── journeys/       # Journey integration with core
└── mcp/            # MCP server for AI integration
```

## MCP Server Integration

TrialSim provides MCP (Model Context Protocol) servers for AI-assisted trial data generation.

### Generation Server

Tools for generating trial data:

| Tool | Description |
|------|-------------|
| `generate_subject` | Generate a single trial subject with demographics |
| `generate_subject_cohort` | Generate multiple subjects for a protocol |
| `generate_visit_schedule` | Create visit schedule for a subject |
| `generate_adverse_events` | Generate adverse events for a subject |
| `generate_exposures` | Generate drug exposure records |
| `list_skills` | List available generation skills |
| `get_skill_details` | Get details about a specific skill |

### State Server

Tools for managing cohorts:

| Tool | Description |
|------|-------------|
| `save_cohort` | Save workspace as a named cohort |
| `load_cohort` | Load a previously saved cohort |
| `list_saved_cohorts` | List saved cohorts with filtering |
| `delete_cohort` | Delete a saved cohort |
| `workspace_summary` | Get current workspace state |

### Running MCP Servers

```bash
# Generation server
python -m trialsim.mcp.generation_server

# State server
python -m trialsim.mcp.state_server
```

### Claude Desktop Configuration

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "trialsim-generation": {
      "command": "python",
      "args": ["-m", "trialsim.mcp.generation_server"],
      "cwd": "/path/to/healthsim-workspace/packages/trialsim"
    },
    "trialsim-state": {
      "command": "python",
      "args": ["-m", "trialsim.mcp.state_server"],
      "cwd": "/path/to/healthsim-workspace/packages/trialsim"
    }
  }
}
```

### Example MCP Interactions

```
User: Generate 50 subjects for protocol ABC-123

Claude: [calls generate_subject_cohort with count=50, protocol_id="ABC-123"]

**Generated 50 Subjects**

**Demographics:**
- Average age: 54.3 years
- Age range: 28-72 years
- Sex: 26 male, 24 female

**Status Distribution:**
- enrolled: 50

**Sample Subjects (3 of 50):**
- SUBJ-A1B2C3D4: 45y M, enrolled
- SUBJ-E5F6G7H8: 62y F, enrolled
- SUBJ-I9J0K1L2: 38y M, enrolled
```

## Integration with Core

TrialSim uses the unified journey engine from `healthsim-core`:

```python
from healthsim.generation import JourneyEngine, get_journey_template

engine = JourneyEngine(seed=42)
journey = get_journey_template("phase3-pivotal-subject")

timeline = engine.create_timeline(
    entity=subject,
    entity_type="subject",
    journey=journey,
    start_date=date(2025, 1, 15),
)
```

## CDISC/SDTM Export

```python
from trialsim.formats import SDTMExporter

exporter = SDTMExporter()
datasets = exporter.export(
    subjects=subjects,
    visits=visits,
    adverse_events=aes,
    format="xpt"  # or "csv", "json"
)
```

## Related

- [HealthSim Core](../core/README.md) - Shared models and journey engine
- [PatientSim](../patientsim/README.md) - Clinical data generation
- [TrialSim Skills](../../skills/trialsim/README.md) - AI conversation skills

## License

Apache 2.0
