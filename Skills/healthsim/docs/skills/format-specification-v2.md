# HealthSim Skills File Format Specification v2.0

**Version**: 2.0 (Claude-Optimized)
**Last Updated**: 2025-11-26
**Replaces**: v1.0 (schema-focused format)

## Overview

Skills files are HealthSim's way of teaching Claude how to generate clinically appropriate data. Unlike v1.0 which focused on data schemas, v2.0 treats skills as **domain knowledge transfer** - teaching Claude medical concepts, clinical patterns, and generation strategies.

## Design Philosophy

**Claude-First Design**: Skills are written as if explaining medical concepts to a knowledgeable clinical AI:
- **Intent-Focused**: Help Claude recognize when to use this knowledge
- **Knowledge Transfer**: Teach clinical patterns, not data structures
- **Example-Driven**: Show interpretations of user requests
- **Conversational**: Natural language over rigid schemas

**Key Shift from v1.0**:
- v1.0: "Here's the schema for vital signs" →
- v2.0: "When a patient has sepsis, their vitals typically show..."

## Required Sections

### 1. Title (H1)
Skill name - descriptive and unique.

```markdown
# Emergency Department Sepsis Management
```

### 2. For Claude Section (NEW in v2.0)
**Purpose**: Direct instruction to Claude about this skill's purpose.
**Format**: Second-person ("you"), imperative tone.
**Content**: When to use this skill, what it enables.

```markdown
## For Claude

Use this skill when the user requests septic patients or mentions systemic infection, sepsis, or septic shock. This skill teaches you how sepsis presents clinically, how it progresses, and what realistic septic patient data looks like.

You should apply this knowledge when:
- Generating patients with infection-related diagnoses
- Creating ICU or emergency department cohorts
- The user mentions "sepsis," "systemic infection," or "septic shock"
- Building patients who need antibiotics and hemodynamic support

This skill provides the clinical context to make sepsis presentations realistic, including appropriate vital sign abnormalities, laboratory patterns, medication regimens, and temporal progression.
```

**Guidelines**:
- Start with "Use this skill when..."
- Be specific about keywords and cohorts
- Explain what the skill teaches (not just what it documents)
- Mention related use cases

### 3. Purpose Section
**Purpose**: Explain what clinical cohorts this enables.
**Audience**: Both Claude and human developers.

```markdown
## Purpose

This skill enables generation of realistic septic patient presentations across the severity spectrum, from uncomplicated bacteremia to septic shock with multiple organ dysfunction.

It models the clinical progression of sepsis, including:
- Typical infectious sources (pneumonia, UTI, abdominal, skin/soft tissue)
- Hemodynamic deterioration patterns
- Laboratory abnormalities and biomarker evolution
- Time-critical treatment bundles
- ICU management and complications

Designed for emergency medicine, critical care, and infectious disease training cohorts.
```

### 4. When to Use This Skill (NEW in v2.0)
**Purpose**: Help Claude recognize user intent.
**Format**: Bullet list of triggers - keywords, phrases, cohorts.

```markdown
## When to Use This Skill

Apply this skill when the user mentions:

**Direct Keywords**:
- "sepsis," "septic," "septic shock"
- "systemic infection," "bacteremia"
- "SIRS" (Systemic Inflammatory Response Syndrome)
- "sepsis bundles," "sepsis protocol"

**Clinical Cohorts**:
- ICU admission with infection
- Emergency department with fever and hypotension
- Post-operative infection complications
- "Patient is crashing from infection"

**Implicit Indicators**:
- Requests for critically ill patients
- Multi-organ dysfunction cohorts
- Antibiotic stewardship examples
- Time-critical treatment cohorts

**Co-occurring Mentions**:
- Often paired with: pneumonia, UTI, wound infection
- Frequently includes: ICU, emergency department, critical care
- May mention: vasopressors, broad-spectrum antibiotics, lactate
```

**Guidelines**:
- Be comprehensive - include synonyms and related terms
- Distinguish direct vs implicit signals
- Note common co-occurring concepts
- Think about how users actually phrase requests

### 5. Domain Knowledge Section
**Purpose**: Teach Claude the medical concepts (not schemas).
**Format**: Narrative explanations with clinical context.
**Focus**: "What does Claude need to know?" not "What fields exist?"

```markdown
## Domain Knowledge

### Sepsis Pathophysiology
Sepsis is a dysregulated host response to infection resulting in life-threatening organ dysfunction. It progresses from localized infection → systemic inflammatory response → organ dysfunction → septic shock.

**Key Concept**: The "sepsis cascade" - infection triggers widespread inflammation, causing vasodilation, capillary leak, and impaired oxygen delivery to tissues. This manifests as hypotension, tachycardia, altered mental status, and elevated lactate.

### Clinical Presentation Patterns

#### Early Sepsis (Compensated)
Patients may appear stable initially but show subtle warning signs:
- Temperature dysregulation: fever (>101°F) or hypothermia (<96°F)
- Tachycardia out of proportion to fever (HR 100-120)
- Subtle tachypnea (RR 20-24) as body tries to compensate
- Blood pressure may be normal or slightly low (SBP 90-100)
- Mental status changes: confusion, irritability (especially in elderly)

**Why this matters for generation**: Early sepsis patients shouldn't have dramatic vital sign abnormalities. The key is *trending* - vitals getting worse over time, not immediately critical.

#### Established Sepsis (Decompensating)
As sepsis progresses, compensation fails:
- Persistent hypotension despite fluid resuscitation
- Worsening tachycardia (HR 120-140)
- Increased respiratory distress (RR 28-32)
- Hypoxia developing (SpO2 88-93%)
- Oliguria (urine output <0.5 mL/kg/hr)

**Laboratory evolution**: Lactate rises (2.0 → 4.0 → 6.0), WBC may paradoxically drop if overwhelming, creatinine rises as kidneys fail.

#### Septic Shock (Decompensated)
Profound circulatory failure requiring vasopressors:
- Hypotension refractory to fluids (MAP <65 despite 30mL/kg)
- Severe lactic acidosis (lactate >4.0, often 6-10)
- Multi-organ dysfunction: AKI, liver dysfunction, coagulopathy
- Altered mental status progressing to obtundation
- Cool, mottled extremities (poor perfusion)

**Why this matters for generation**: Septic shock patients need vasopressors (norepinephrine), mechanical ventilation, and ICU care. Don't generate septic shock patients without these interventions.
```

## Generation Guidelines

### How to Apply This Knowledge

**When the user says**: "Generate a septic patient"

**Claude should**:
1. Choose infection source (default: pneumonia, 60% probability)
2. Set severity level (default: "established sepsis" - not compensated, not shock)
3. Generate appropriate vital sign pattern for severity
4. Generate labs showing infection + organ dysfunction
5. Include appropriate antibiotic regimen
6. Consider timeline (ED admission → treatment → disposition)

**Key Generation Rules**:

#### Demographics Considerations
- Sepsis can occur at any age, but higher risk in:
  - Elderly (>65) - decreased immune response
  - Immunocompromised (cancer, diabetes, chronic steroids)
  - Post-operative patients
- No strong gender bias
- Consider including risk factors: diabetes, COPD, immunosuppression

#### Vital Sign Coherence
**Temperature-HR Relationship**: Every 1°F increase in temperature typically raises HR by 10 bpm
- Temp 103°F → expect HR ~110-120
- If temp 103°F but HR 70 → clinically implausible (unless on beta-blockers)

**BP-Lactate Relationship**: Hypotension correlates with tissue hypoperfusion
- BP 95/60 → lactate 2-4 mmol/L (mild hypoperfusion)
- BP 80/50 → lactate 6-10 mmol/L (severe hypoperfusion)

**SpO2-RR Relationship**: Hypoxia drives tachypnea
- SpO2 90% → RR 24-28
- SpO2 85% → RR 30-35

#### Clinical Coherence Checks
Before finalizing a septic patient, verify:
- [ ] Infection source identified and labs match (e.g., pneumonia → high WBC, infiltrate)
- [ ] Vital signs match severity (shock → hypotension, high lactate, pressors)
- [ ] Antibiotics appropriate for source
- [ ] Timeline makes sense (door-to-antibiotics <1 hour)
- [ ] If ICU admission, include ICU-level interventions (central line, pressors, etc.)

## Parameters

Parameters allow users to customize generation without creating new skills. Frame parameters as **conversations with the user**, not schema fields.

### Recommended Parameters

| Parameter | Natural Language Description | Type | Default | Claude's Interpretation |
|-----------|------------------------------|------|---------|------------------------|
| severity | How severe should the sepsis be? | enum: mild, moderate, severe, shock | moderate | Controls vital sign abnormality degree, lactate level, need for ICU/pressors |
| infection_source | Where is the infection coming from? | enum: pneumonia, uti, abdominal, skin, catheter, unknown | pneumonia | Determines associated symptoms, imaging, and antibiotic choices |
| complications | Should the patient have complications? | enum: none, minor, major | none | Adds DIC, ARDS, multi-organ failure |
| age_bias | What age range is typical? | range | 60-80 | Sepsis more common in elderly; affects comorbidities |
| response_to_treatment | How does the patient respond? | enum: good, slow, poor | good | Affects timeline - quick improvement vs prolonged ICU |

**How Claude Uses Parameters**:
- `severity=shock` → BP <90, lactate >6, norepinephrine drip, ICU
- `infection_source=pneumonia` → cough, infiltrate on CXR, ceftriaxone+azithromycin
- `complications=major` → add ARDS (intubated), DIC (low platelets, high INR), AKI (Cr >3)

## Example Requests and Interpretations

### Example 1: Basic Request
**User says**: "Generate a septic patient"

**Claude interprets**:
- Severity: moderate (default)
- Source: pneumonia (most common)
- Age: 65-75 (typical)
- Setting: Emergency department

**Key features Claude generates**:
- Vital signs: Temp 102°F, HR 110, BP 95/60, RR 26, SpO2 90%
- Labs: WBC 20, Lactate 3.5, CRP 180, Creatinine 1.8
- Diagnosis: Sepsis due to pneumonia (J18.9, A41.9)
- Antibiotics: Ceftriaxone + Azithromycin
- Timeline: ED arrival → antibiotics hour 1 → ICU admission hour 4

### Example 2: Specific Severity Request
**User says**: "I need a patient in septic shock for ICU simulation"

**Claude interprets**:
- Severity: shock (explicitly requested)
- Requires: vasopressors, ICU admission, critical presentation
- Setting: ICU (mentioned by user)

**Key features Claude generates**:
- Vital signs: Temp 104°F, HR 135, BP 75/45, RR 32, SpO2 86%
- Labs: Lactate 8.5, WBC 28, Cr 2.5, Plt 95 (DIC developing)
- Interventions: Norepinephrine drip, intubated/ventilated, central line
- Location: ICU
- Prognosis: Guarded, high mortality risk

### Example 3: Source-Specific Request
**User says**: "Generate a patient with urosepsis"

**Claude interprets**:
- Source: UTI (urosepsis = sepsis from urinary source)
- Likely demographics: Elderly or catheterized
- Specific features: urinary symptoms, positive UA

**Key features Claude generates**:
- Demographics: 78-year-old with indwelling catheter
- Symptoms: Fever, confusion, no urinary complaints (often asymptomatic in elderly)
- Labs: WBC 18, lactate 3.0, UA: WBC 100+, bacteria, nitrites positive
- Diagnosis: Sepsis due to UTI (N39.0, A41.9)
- Antibiotics: Ceftriaxone (UTI coverage)

## Related Skills

List complementary skills Claude might need:

```markdown
## Related Skills

- **healthcare/clinical-domain.md** - Foundation for all medical knowledge
- **skills/patientsim/sepsis-acute-care.md** - For pneumonia-source sepsis details
- **skills/patientsim/sepsis-acute-care.md** - For urosepsis details
- **fhir/observation-vitals.md** - For encoding vital signs to FHIR
- **validation/clinical-plausibility.md** - Ensures generated sepsis patients are realistic
```

## Backward Compatibility with v1.0

The v2.0 format is **additive** - all v1.0 sections remain valid. Tools can:
1. Parse both formats
2. Migrate v1.0 → v2.0 by inferring Claude-focused sections
3. Prefer v2.0 sections when present, fall back to v1.0

**Migration path**:
- Old "Parameters" table → Still used
- Old "Generation Rules" → Incorporated into "Domain Knowledge" + "Generation Guidelines"
- New "For Claude" + "When to Use" → Added to enhance discoverability

## Validation Rules

### Required for v2.0
- Must have H1 title
- Must have "For Claude" section (distinguishes v2.0 from v1.0)
- Must have "When to Use This Skill" section
- Must have "Domain Knowledge" OR "Generation Guidelines" section

### Recommended
- Include "Example Requests and Interpretations" (helps Claude learn patterns)
- Use narrative style in Domain Knowledge (not bullet points or tables)
- Provide clinical context for all numeric ranges ("why this matters")

### Format Checking
```python
def is_v2_skill(markdown_content):
    """Check if skill file uses v2.0 format."""
    has_for_claude = "## For Claude" in markdown_content
    has_when_to_use = "## When to Use" in markdown_content
    return has_for_claude and has_when_to_use
```

## Best Practices

### Writing "Domain Knowledge" Sections

**Good** (Teaches clinical patterns):
```markdown
### Sepsis Vital Sign Patterns
When sepsis progresses to shock, blood pressure drops because widespread vasodilation
reduces vascular resistance. This triggers compensatory tachycardia as the heart tries
to maintain cardiac output. Meanwhile, respiratory rate increases to blow off CO2 and
compensate for metabolic acidosis from lactic acid accumulation.

This means septic shock patients typically show:
- BP: 70-85/40-50 mmHg (vasodilation)
- HR: 120-140 bpm (compensatory)
- RR: 30-40 /min (acidosis compensation)
- Lactate: 6-12 mmol/L (tissue hypoperfusion)

Together, these create a clinical picture of "warm shock" - patient is warm/flushed
from vasodilation but hemodynamically unstable.
```

**Bad** (Just lists schemas):
```markdown
### Vital Signs
- Blood Pressure: 70-85/40-50 mmHg
- Heart Rate: 120-140 bpm
- Respiratory Rate: 30-40 /min
```

### Writing "When to Use This Skill"

**Good** (Comprehensive triggers):
```markdown
## When to Use This Skill

Direct mentions:
- "sepsis", "septic shock", "septic", "SIRS"
- "systemic infection", "overwhelming infection"

Cohort descriptions:
- "ICU patient with infection"
- "patient crashing from pneumonia"
- "needs pressors and broad antibiotics"

Implicit signals:
- Mentions of specific biomarkers: lactate, procalcitonin
- Time-critical language: "sepsis bundles", "door-to-antibiotics"
- Multi-organ mentions: "AKI from sepsis", "ARDS in sepsis"
```

**Bad** (Too narrow):
```markdown
## When to Use This Skill
Use when user says "sepsis"
```

### Writing "Example Requests and Interpretations"

**Good** (Shows reasoning):
```markdown
### Example: Implicit Severity Cues
**User says**: "Generate a septic patient on three pressors"

**Claude interprets**:
- Three pressors → extremely severe (septic shock, refractory)
- Typical progression: Norepinephrine → add vasopressin → add epinephrine
- Implies: ICU, very high lactate (>10), multi-organ failure
- Prognosis: Grave, high mortality

**Key features**:
- BP: 65/35 despite maximal pressors
- Lactate: 15 mmol/L
- Intubated, dialysis likely needed
- Multiple organ dysfunction
```

**Bad** (No interpretation shown):
```markdown
### Example
User: "Generate septic patient"
Result: Patient with sepsis
```

## See Also

- [Skills Format v1.0](format-specification.md) - Original specification
- [Migration Guide](migration-guide.md) - Migrating v1.0 → v2.0
- [Creating Skills](creating-skills.md) - Guide to authoring skills
