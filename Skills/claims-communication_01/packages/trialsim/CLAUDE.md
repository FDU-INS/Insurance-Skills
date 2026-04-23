# TrialSim - Claude Development Guide

## Package Purpose
Generate synthetic clinical trial data for testing, demos, and AI training.

## Key Concepts

### Trial Entities
- **Subject**: Trial participant (links to PatientSim patient)
- **Site**: Clinical trial site
- **Protocol**: Trial protocol definition
- **Visit**: Scheduled/unscheduled visit event
- **Adverse Event**: AE/SAE with CTCAE grading
- **Exposure**: Drug/treatment exposure record

### Event Types (from core)
```python
from healthsim.generation.journey_engine import TrialEventType

# Available: screening, randomization, withdrawal, scheduled_visit,
#           unscheduled_visit, adverse_event, serious_adverse_event,
#           protocol_deviation, dose_modification
```

### Journey Templates
Pre-built templates in `healthsim-core`:
- `phase3-pivotal-subject` - Complete Phase 3 subject journey
- `trial-safety-monitoring` - Safety event monitoring
- `phase1-dose-escalation` - First-in-human dose escalation
- `trial-subject-withdrawal` - Early termination
- `protocol-deviation-journey` - Protocol deviation handling
- `trial-dose-modification` - Dose modification events

## Common Operations

### Generate Trial Subjects
```python
from trialsim import TrialSubjectGenerator

gen = TrialSubjectGenerator(seed=42)
subjects = gen.generate_many(
    count=100,
    protocol_id="PROTO-001",
    sites=["SITE-001", "SITE-002"],
    arms=["treatment", "placebo"]
)
```

### Generate Visit Schedule
```python
from healthsim.generation import JourneyEngine, get_journey_template

engine = JourneyEngine(seed=42)
journey = get_journey_template("phase3-pivotal-subject")

timeline = engine.create_timeline(
    entity=subject,
    entity_type="subject",
    journey=journey,
    start_date=screening_date
)
```

### Export to SDTM
```python
from trialsim.formats import SDTMExporter

exporter = SDTMExporter(study_id="STUDY-001")
exporter.export_dm(subjects)  # Demographics
exporter.export_sv(visits)    # Subject Visits
exporter.export_ae(aes)       # Adverse Events
exporter.export_ex(exposures) # Exposures
```

## Testing
```bash
cd packages/trialsim
pytest tests/ -v
```

## Integration Points
- Uses `healthsim-core` for journey engine and base models
- Links to `patientsim` for clinical data
- Skills in `skills/trialsim/` for AI conversations
