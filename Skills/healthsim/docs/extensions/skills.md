# Adding Skills

Guide to creating skills that teach Claude new domain knowledge.

## When to Add a Skill

Add a skill when **Claude needs to KNOW something** about a clinical domain, cohort, or format.

### Good Reasons to Add Skill

**New clinical domain**
```
User: "Generate a stroke patient eligible for tPA"
→ Need stroke skill with tPA criteria, NIHSS scoring, timing windows
```

**New cohort pattern**
```
User: "Generate a postpartum patient with hemorrhage"
→ Need obstetrics skill with delivery cohorts, complications
```

**Clinical guidelines**
```
User: "Generate diabetic patients following ADA guidelines"
→ Need updated diabetes skill with current treatment standards
```

**New healthcare format**
```
User: "Export to CDA format"
→ Need CDA format skill explaining structure, use cases
```

### Bad Reasons to Add Skill

**Claude needs to calculate something**
```
User: "Calculate SOFA score for this patient"
→ Don't need skill, need MCP tool to perform calculation
```

**Just parameter variations**
```
User: "Generate patient aged 70-80"
→ Don't need skill, existing generation handles age ranges
```

**One-time specific request**
```
User: "Generate patient named John Smith"
→ Don't need skill, one-off parameter
```

## Skill vs MCP Tool Decision

Use this matrix to decide between skill and MCP tool:

| Question | Skill | MCP Tool |
|----------|-------|----------|
| Does it require code execution? | No | **Yes** |
| Does it involve calculations? | No | **Yes** |
| Is it primarily knowledge? | **Yes** | No |
| Does it teach Claude "how to think"? | **Yes** | No |
| Does it require data transformation? | No | **Yes** |
| Does it enable interpretation? | **Yes** | No |
| Does it need session state? | No | **Yes** |

### Decision Examples

**Cohort: Sepsis Management**
- Question: Does it require code execution? **No**
- Question: Is it primarily knowledge? **Yes**
- Decision: **Skill**

**Cohort: SOFA Score Calculation**
- Question: Does it require calculations? **Yes**
- Question: Is it primarily knowledge? **No**
- Decision: **MCP Tool**

**Cohort: CDA Export**
- Question: Does it require data transformation? **Yes**
- Question: Does it need session state? **Yes**
- Decision: **MCP Tool** + **Skill** (to explain format)

## Skill Types

HealthSim uses three types of skills:

### 1. Domain Skills

**What:** Teach Claude about clinical specialties, conditions, or systems

**Examples:**
- Cardiology (heart disease, interventions, medications)
- Nephrology (kidney disease, dialysis, transplant)
- Obstetrics (pregnancy, delivery, postpartum)

**File location:** `skills/healthcare/[domain]-domain.md`

**When to use:** Adding a new medical specialty or organ system

### 2. Cohort Skills

**What:** Teach Claude how to generate specific patient types

**Examples:**
- Sepsis (SIRS criteria, antibiotics, timelines)
- Diabetes (HbA1c control levels, complications, regimens)
- Joint replacement (pre-op, post-op, rehab)

**File location:** `skills/[cohort].md`

**When to use:** Adding a new patient generation pattern

### 3. Format Skills

**What:** Teach Claude about healthcare data standards

**Examples:**
- FHIR R4 (resources, references, extensions)
- HL7v2 (segments, messages, delimiters)
- MIMIC-III (tables, relationships, codes)

**File location:** `skills/formats/[format]-format.md`

**When to use:** Adding export format or data standard knowledge

## Claude-First Skill Structure

Skills use a Claude-first structure optimized for conversational AI:

```markdown
# Skill Name

**Version:** 2.0
**Category:** cohorts | healthcare | formats
**Last Updated:** YYYY-MM-DD

## For Claude

[Write directly to Claude in natural language]

This skill enables you to [what Claude can now do].

When users request [cohorts], you should [approach].

## When to Use This Skill

Use this skill when requests involve:
- [Specific trigger 1]
- [Specific trigger 2]
- [Specific trigger 3]

Don't use this skill for:
- [Anti-pattern 1]
- [Anti-pattern 2]

## Domain Knowledge

### Section 1: Clinical Concepts

[Medical terminology, pathophysiology, definitions]

### Section 2: Parameters & Ranges

[Lab values, vital signs, medication doses with ranges]

### Section 3: Guidelines & Evidence

[Clinical guidelines, treatment protocols, standards of care]

## Generation Guidelines

### Patient Demographics

[Who typically gets this condition? Age ranges, risk factors]

### Clinical Presentation

[How do patients present? Symptoms, signs, history]

### Medications

[Evidence-based regimens, dosing, contraindications]

### Labs & Vitals

[Expected values, ranges, coherence relationships]

### Complications

[Common complications, timelines, risk factors]

## Example Requests and Interpretations

**Request:** "[user request]"

**Interpretation:** [How Claude should interpret this]

**Example Output:** [Sample generated patient or response]

---

[Repeat for 3-5 common request patterns]

## Clinical Pearls

- [Important clinical insight 1]
- [Important clinical insight 2]
- [Important clinical insight 3]

## Validation Rules

- [Rule 1]: [What makes it valid]
- [Rule 2]: [Plausibility check]
- [Rule 3]: [Coherence requirement]

## References

- [Guideline or source 1]
- [Guideline or source 2]
```

### Section Guidelines

**"For Claude" section:**
- Write conversationally to Claude
- Explain what this enables
- Set expectations clearly

**"When to Use" section:**
- List specific triggers (keywords, cohorts)
- Include anti-patterns (when NOT to use)
- Help Claude make good decisions

**"Domain Knowledge" section:**
- Clinical depth and accuracy
- Include ranges and thresholds
- Cite evidence when available

**"Generation Guidelines" section:**
- Practical instructions for creating patients
- Realistic parameter ranges
- Temporal relationships

**"Example Requests" section:**
- Show, don't just tell
- Cover common variations
- Include complete example outputs

## Adding a Domain Skill - Quick Prompt

Use this prompt to add a domain skill:

```
Create [DOMAIN] domain skill for HealthSim:

**Conversation Goal:**
Enable: "Generate [domain] patients with [characteristics]"

**Domain Knowledge:**
- Key conditions: [list main conditions]
- Common treatments: [typical interventions]
- Lab/vital ranges: [relevant values]
- Guidelines: [cite relevant standards]

**Typical Patients:**
1. [Patient type 1]: [characteristics]
2. [Patient type 2]: [characteristics]
3. [Patient type 3]: [characteristics]

**File Location:** skills/healthcare/[domain]-domain.md

**Follow:** skills/SKILL_TEMPLATE_V2.md structure

**Examples to include:**
- Simple: "Generate [domain] patient"
- Moderate: "Generate [domain] patient with [complication]"
- Complex: "Generate [domain] patient for [specific use case]"
```

## Adding a Cohort Skill - Quick Prompt

Use this prompt to add a cohort skill:

```
Create [SCENARIO] cohort skill for HealthSim:

**Conversation Goal:**
Enable: "Generate [cohort] patient with [characteristics]"

**Clinical Pattern:**
[Describe the clinical presentation, typical timeline, key features]

**Required Elements:**
- Presentation: [how patient presents]
- Timeline: [symptom onset → ED/admission → treatment progression]
- Key findings: [vital signs, labs, imaging]
- Treatment: [evidence-based management]
- Complications: [common complications to consider]

**Parameters Users Control:**
- Severity: [mild/moderate/severe definitions]
- Timing: [early vs late presentation]
- Complications: [which complications present]

**File Location:** skills/[cohort].md

**Follow:** skills/SKILL_TEMPLATE_V2.md structure

**Examples to include:**
- Basic: "Generate [cohort] patient"
- Specific: "Generate [cohort] patient with [severity/timing]"
- Complex: "Generate [cohort] patient with [multiple complications]"

**References:**
[List clinical guidelines to consult]
```

## Skill Composition

Skills can reference other skills to avoid duplication:

### Referencing Patterns

**In a cohort skill referencing domain knowledge:**

```markdown
## Domain Knowledge

### Cardiac Medications

For detailed clinical rules, see the [Clinical Rules](../../references/clinical-rules.md#required-medications-by-condition).

**Quick reference for this cohort:**
- Aspirin 325mg loading, then 81mg daily
- Clopidogrel 600mg loading, then 75mg daily
- Atorvastatin 80mg daily (high-intensity statin)
```

**In a domain skill referencing cohorts:**

```markdown
## Common Cohorts

This domain knowledge supports several cohort skills:

- **[Heart Failure](../../skills/patientsim/heart-failure.md)** - HFrEF/HFpEF management
- **[Diabetes Management](../../skills/patientsim/diabetes-management.md)** - Type 1/2 diabetes
- **[ED Chest Pain](../../skills/patientsim/ed-chest-pain.md)** - ACS workup and management

Refer to those skills for specific generation patterns.
```

### Composition Benefits

- Avoid duplicating medication lists
- Single source of truth for lab ranges
- Easy to update (change once, affects all)
- Claude sees connections between skills

## Testing Skills

### Step 1: Add to Claude Project

```bash
# In Claude Desktop or Claude.ai
1. Open HealthSim project
2. Add skill file to Project Knowledge
3. Refresh project context
```

### Step 2: Test Basic Request

```
User: "Generate [cohort] patient"

Expected: Claude generates patient matching skill guidelines
Verify:
- Correct demographics
- Appropriate conditions
- Realistic medications
- Valid lab values
- Proper timeline
```

### Step 3: Test Variations

```
User: "Generate [cohort] patient with [complication]"

Expected: Claude adds complication appropriately
Verify:
- Complication matches clinical pattern
- Labs/vitals adjusted appropriately
- Treatment reflects complication
```

### Step 4: Test Edge Cases

```
User: "Generate severe [cohort] patient"
User: "Generate [cohort] patient presenting late"
User: "Generate [cohort] patient with multiple complications"

Expected: Claude handles severity/timing/complexity correctly
```

### Step 5: Verify Skill Usage

Ask Claude:

```
User: "What skills did you use to generate that patient?"

Expected: Claude should mention your new skill
```

### Step 6: Test Knowledge Retention

```
User: "Why did you choose those medications?"
User: "What's the normal range for that lab value?"
User: "What complications should I watch for?"

Expected: Claude answers from skill knowledge
```

## Checklist

When adding a new skill, complete this checklist:

### Design Phase
- [ ] Identified conversation goal (what users should be able to say)
- [ ] Confirmed skill is appropriate (not MCP tool or just parameters)
- [ ] Identified skill type (domain/cohort/format)
- [ ] Researched clinical guidelines and evidence
- [ ] Identified what Claude needs to KNOW vs DO

### Content Phase
- [ ] Created skill file in correct location
- [ ] Wrote "For Claude" section (conversational)
- [ ] Wrote "When to Use" section (triggers and anti-patterns)
- [ ] Wrote "Domain Knowledge" section (clinical depth)
- [ ] Wrote "Generation Guidelines" section (practical instructions)
- [ ] Wrote "Example Requests" section (3-5 examples)
- [ ] Added clinical pearls
- [ ] Added validation rules
- [ ] Added references

### Quality Phase
- [ ] Clinical accuracy verified (checked against guidelines)
- [ ] Parameter ranges realistic (compared to MIMIC/literature)
- [ ] Examples complete and detailed
- [ ] Skill references other skills where appropriate
- [ ] No duplication with existing skills
- [ ] Writing is clear and conversational

### Testing Phase
- [ ] Skill added to Claude Project
- [ ] Basic request tested
- [ ] Variations tested
- [ ] Edge cases tested
- [ ] Claude correctly uses skill
- [ ] Claude retains knowledge when asked

### Documentation Phase
- [ ] Skill listed in skills/README.md
- [ ] Example conversation added to examples/conversations/
- [ ] User guide updated (if major capability)
- [ ] Skill announced in CHANGELOG.md

### Integration Phase
- [ ] Skill works with existing cohorts
- [ ] Skill complements (not duplicates) other skills
- [ ] Validation rules don't conflict with existing rules
- [ ] Export formats handle new data (if applicable)

---

**Remember:** Skills teach Claude to think like a clinician. Write them conversationally, provide clinical context, and show realistic examples. If Claude can't generate appropriate patients after reading your skill, refine the skill content.

## Common Patterns

### Pattern 1: Severity Spectrum

Many cohorts have mild/moderate/severe variants:

```markdown
## Generation Guidelines

### Severity Levels

**Mild [Condition]:**
- Presentation: [mild symptoms]
- Labs: [mildly abnormal ranges]
- Treatment: [conservative management]

**Moderate [Condition]:**
- Presentation: [moderate symptoms]
- Labs: [more abnormal ranges]
- Treatment: [standard therapy]

**Severe [Condition]:**
- Presentation: [severe symptoms, complications]
- Labs: [severely abnormal ranges]
- Treatment: [intensive management, ICU]

**Example Requests:**
"Generate mild [condition] patient" → Use mild guidelines
"Generate severe [condition] patient" → Use severe guidelines
```

### Pattern 2: Temporal Progression

Some conditions have early/late or acute/chronic phases:

```markdown
## Generation Guidelines

### Timeline Variations

**Early Presentation (< [timeframe]):**
- [Early phase characteristics]
- [Treatment options available]
- [Prognosis considerations]

**Late Presentation (> [timeframe]):**
- [Late phase characteristics]
- [Limited treatment options]
- [Complications more likely]

**Example Requests:**
"Generate [condition] patient presenting within [window]" → Early
"Generate [condition] patient presenting [late]" → Late
```

### Pattern 3: Complication Patterns

Structure complications systematically:

```markdown
## Generation Guidelines

### Complications

**Common Complications (30-50%):**
- [Complication 1]: [description, management]
- [Complication 2]: [description, management]

**Serious Complications (5-10%):**
- [Complication 3]: [description, management]
- [Complication 4]: [description, management]

**Rare Complications (<5%):**
- [Complication 5]: [description, management]

**Example Requests:**
"Generate [condition] with [common complication]" → Apply complication pattern
"Generate [condition] with [rare complication]" → Ensure clinical plausibility
```

## See Also

- [Skills Format v1.0](../skills/format-specification.md) - Original specification
- [Skills Format v2.0](../skills/format-specification-v2.md) - Claude-optimized format
- [Creating Skills](../skills/creating-skills.md) - Detailed authoring guide
- [Extension Philosophy](philosophy.md) - Conversation-first approach
- [MCP Tools](mcp-tools.md) - When skills aren't enough
