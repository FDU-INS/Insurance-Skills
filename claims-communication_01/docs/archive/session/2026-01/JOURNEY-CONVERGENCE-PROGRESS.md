# Journey Convergence Progress Tracker

## Overview
Refactoring HealthSim products to use the unified JourneyEngine from 
`packages/core/src/healthsim/generation/journey_engine.py` with consistent
journey templates across all products.

**Status**: ✅ COMPLETE
**Started**: 2025-01-04
**Completed**: 2025-01-05

---

## Summary of Changes

### Phase 1: MemberSim Migration ✅ COMPLETE
- Created `journeys/` module with handlers, templates, and backward compat
- Migrated 6 journey templates from scenarios
- Updated package exports
- Removed old `scenarios/` folder
- Tests: 182/183 passing (1 unrelated failure)

### Phase 2: RxMemberSim Migration ✅ COMPLETE
- Created `journeys/` module with handlers, templates, and backward compat
- Migrated 6 journey templates from scenarios
- Updated MCP server to use journey API
- Removed old `scenarios/` folder
- Tests: 213/213 passing

### Phase 3: TrialSim Journey Templates ✅ COMPLETE
- Added 6 journey templates to core `JOURNEY_TEMPLATES`
- TrialSim handlers were already in core
- Tests: 902/902 passing

### Phase 4: PatientSim Assessment ✅ NO CHANGES NEEDED
- PatientSim uses "scenario-template" as a Skill type (clinical scenario descriptions)
- This is a different concept from journey engine event sequences
- PatientSim handlers exist in core

---

## Journey Templates Summary

### Core Templates (journey_engine.py)
| Template | Product | Duration | Description |
|----------|---------|----------|-------------|
| `diabetic-first-year` | cross-product | 365 days | First year of diabetic care |
| `new-member-onboarding` | membersim | 90 days | New health plan enrollment |

### TrialSim Templates (journey_engine.py)
| Template | Duration | Description |
|----------|----------|-------------|
| `phase3-pivotal-subject` | 365 days | Phase 3 pivotal trial subject journey |
| `trial-safety-monitoring` | 180 days | Safety event monitoring journey |
| `phase1-dose-escalation` | 56 days | First-in-human dose escalation |
| `trial-subject-withdrawal` | 30 days | Subject early termination |
| `protocol-deviation-journey` | 14 days | Protocol deviation management |
| `trial-dose-modification` | 42 days | Dose reduction due to toxicity |

### MemberSim Templates (membersim/journeys/templates.py)
| Template | Duration | Description |
|----------|----------|-------------|
| `new-member-onboarding` | 90 days | ID card → welcome call → HRA → PCP |
| `annual-wellness` | 365 days | Wellness visit → preventive labs |
| `chronic-care-management` | 365 days | CCM enrollment → monthly touchpoints |
| `surgical-episode` | 120 days | Consult → auth → surgery → follow-ups |
| `quality-gap-closure` | 90 days | Gap ID → outreach → visit → closure |
| `member-termination` | 90 days | Term notice → COBRA → final claims |

### RxMemberSim Templates (rxmembersim/journeys/templates.py)
| Template | Duration | Description |
|----------|----------|-------------|
| `new-therapy-start` | 180 days | Rx → first fill → refills |
| `chronic-therapy-maintenance` | 365 days | 90-day fill cycles |
| `specialty-onboarding` | 90 days | PA → hub → copay assist → fill |
| `step-therapy` | 120 days | First-line → failure → second-line |
| `adherence-intervention` | 60 days | Gap → outreach → refill → MPR |
| `therapy-discontinuation` | 30 days | Final fill → discontinue → follow-up |

---

## Architecture

### Unified Journey Engine (core)
```
packages/core/src/healthsim/generation/
├── journey_engine.py      # JourneyEngine, specs, all templates
│   ├── BaseEventType      # Common events
│   ├── PatientEventType   # Clinical events
│   ├── MemberEventType    # Enrollment/claims events
│   ├── RxEventType        # Prescription/fill events
│   ├── TrialEventType     # Clinical trial events
│   └── JOURNEY_TEMPLATES  # All built-in templates
│
└── handlers.py            # Product-specific handlers
    ├── PatientSimHandlers
    ├── MemberSimHandlers
    ├── RxMemberSimHandlers
    └── TrialSimHandlers
```

### Product Packages (with journey modules)
```
packages/membersim/src/membersim/journeys/
├── __init__.py       # Re-exports core + product templates
├── handlers.py       # Additional MemberSim handlers
├── templates.py      # 6 MemberSim-specific templates
└── compat.py         # Backward compatibility aliases

packages/rxmembersim/src/rxmembersim/journeys/
├── __init__.py       # Re-exports core + product templates
├── handlers.py       # Additional RxMemberSim handlers
├── templates.py      # 6 RxMemberSim-specific templates
└── compat.py         # Backward compatibility aliases
```

---

## Test Results

| Package | Tests | Passed | Status |
|---------|-------|--------|--------|
| Core | 902 | 902 | ✅ |
| MemberSim | 183 | 182 | ✅ (1 unrelated) |
| RxMemberSim | 213 | 213 | ✅ |
| PatientSim | 403 | 392 | ⚠️ (11 pre-existing) |

---

## Git Commits

1. `2d4a5d9` - refactor: Migrate MemberSim and RxMemberSim from scenarios to journeys
2. `c1d5f51` - docs: Update journey convergence progress tracker
3. `[pending]` - feat: Add TrialSim journey templates to core

---

## Usage

### Get Journey Templates
```python
# Core templates
from healthsim.generation import get_journey_template, JOURNEY_TEMPLATES
journey = get_journey_template("phase3-pivotal-subject")

# MemberSim templates
from membersim.journeys import get_member_journey_template, MEMBER_JOURNEY_TEMPLATES
journey = get_member_journey_template("chronic-care-management")

# RxMemberSim templates
from rxmembersim.journeys import get_rx_journey_template, RX_JOURNEY_TEMPLATES
journey = get_rx_journey_template("specialty-onboarding")
```

### Create Timeline
```python
from healthsim.generation import create_journey_engine
from datetime import date

engine = create_journey_engine(seed=42)
journey = get_journey_template("phase3-pivotal-subject")
subject = {"subject_id": "SUBJ-001", "site_id": "SITE-001"}

timeline = engine.create_timeline(
    entity=subject,
    entity_type="subject",
    journey=journey,
    start_date=date(2025, 1, 15),
)

for event in timeline.events:
    print(f"{event.scheduled_date}: {event.event_name}")
```

---

## Next Steps

### Completed ✅
1. ~~Update SKILL.md documentation for generation/journeys~~
2. ~~Fix broken markdown links across documentation~~ (reduced from 211 to 30, with 17 real broken links remaining)
3. Added new journey templates and distribution skills

### Remaining
1. Create remaining profile templates (14 files) or remove broken links
2. Update hello-healthsim examples with journey patterns
3. Consider creating dedicated `packages/trialsim` package for parity
4. Clean up archive directory broken links (low priority)
