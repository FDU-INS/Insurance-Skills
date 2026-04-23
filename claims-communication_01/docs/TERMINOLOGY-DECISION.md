# HealthSim Terminology Decision Guide

## The Problem

We have terminology inconsistency:
- **Core framework** uses "journey" (e.g., `JourneyEngine`, `JourneySpecification`)  
- **MemberSim/RxMemberSim** use "scenario" (e.g., `ScenarioEngine`, `ScenarioDefinition`)
- **Documentation** uses both terms interchangeably

These concepts are **functionally identical**:
- Both define event sequences over time
- Both have an engine that creates timelines
- Both execute events through registered handlers

## Decision: Converge on "Journey"

| Old Term | New Term | Rationale |
|----------|----------|-----------|
| `ScenarioDefinition` | `JourneyDefinition` | "Journey" better conveys temporal progression |
| `ScenarioEngine` | `JourneyEngine` | Aligns with core framework |
| `ScenarioMetadata` | `JourneyMetadata` | Consistency |
| `scenarios/` folder | `journeys/` folder | Consistency |
| `scenario_id` | `journey_id` | Consistency |

## Terminology Glossary (Final)

| Term | Definition | Example |
|------|------------|---------|
| **Cohort** | Saved collection of generated entities | "Medicare diabetic cohort with 500 members" |
| **Journey** | Event sequence pattern over time | "Heart failure first-year journey" |
| **Profile** | Population characteristics specification | "Commercial healthy adults age 25-45" |
| **Template** | Pre-built profile or journey | "Medicare Diabetic Profile Template" |
| **Handler** | Function that executes a specific event type | `admission_handler()` |
| **Trigger** | Cross-product event coordination | "Claim triggers encounter creation" |

## Keep "Scenario" When...

"Scenario" remains valid in these contexts:
- **Clinical scenario**: Describes a medical situation (e.g., "sepsis scenario", "heart failure scenario")
- **Test scenario**: QA test case description
- **User-facing prompts**: Natural language ("Generate a diabetes scenario")

These are NOT being renamed because they describe situations, not event sequences.

## Refactoring Scope

### Phase 1: MemberSim Folder Rename (Low Risk)
```
membersim/src/membersim/scenarios/ → membersim/src/membersim/journeys/
```

### Phase 2: Class Renames (Medium Risk)
```python
# Before
class ScenarioDefinition: ...
class ScenarioEngine: ...
class ScenarioMetadata: ...

# After  
class JourneyDefinition: ...
class JourneyEngine: ...
class JourneyMetadata: ...
```

### Phase 3: PatientSim MCP Tools (Low Risk)
```python
# Before
"list_scenarios" → "list_templates"
"describe_scenario" → "describe_template"
format_scenario_list() → format_template_list()
```

### Phase 4: Skills/Documentation (Low Risk)
- Update SKILL.md section headers
- Update any docs using "scenario" for event sequences

## Files to Modify

### MemberSim
- `membersim/src/membersim/scenarios/` → `journeys/`
- `membersim/src/membersim/scenarios/__init__.py`
- `membersim/src/membersim/scenarios/definition.py`
- `membersim/src/membersim/scenarios/engine.py`
- `membersim/src/membersim/scenarios/events.py`
- `membersim/src/membersim/scenarios/timeline.py`
- `membersim/tests/test_*.py` (imports)

### RxMemberSim
- `rxmembersim/src/rxmembersim/scenarios/` → `journeys/`
- Same files as MemberSim

### PatientSim
- `patientsim/src/patientsim/mcp/generation_server.py`
- `patientsim/src/patientsim/mcp/formatters.py`
- `patientsim/src/patientsim/skills/schema.py` (SkillType enum)

### Documentation
- `SKILL.md` (section headers)
- `hello-healthsim/*.md` (various)
- `skills/*/SKILL.md` (if applicable)

## Verification Checklist

After refactoring:
- [ ] All tests pass
- [ ] No Python import errors
- [ ] `grep -r "scenario" packages/` shows only valid uses
- [ ] MCP tools work correctly
- [ ] Documentation is consistent
