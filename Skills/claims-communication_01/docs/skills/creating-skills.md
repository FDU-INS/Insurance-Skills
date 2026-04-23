# Creating Skills

Guide to authoring clinical cohort skills for Claude.

## Skill Overview

Skills are markdown files that give Claude domain expertise. They define:
- Clinical cohorts (diabetes, cardiac, surgical)
- Generation guidelines and parameters
- Example patient profiles
- Clinical reasoning and evidence base

## Skill Format v2.0

HealthSim products use Skills Format v2.0 with dedicated sections.

### Basic Structure

```markdown
# Skill Name

**Version:** 2.0
**Category:** cohorts | healthcare | formats
**Last Updated:** 2025-01-26

## For Claude

[Natural language description of what this skill enables Claude to do]

## When to Use This Skill

[Explain when Claude should use this skill vs. others]

## Domain Knowledge

### Section 1: Clinical Concepts

[Medical terminology, guidelines, pathophysiology]

### Section 2: Parameters & Ranges

[Lab values, medication doses, severity criteria]

## Generation Guidelines

### Patient Demographics

[Age ranges, gender considerations, epidemiology]

### Clinical Presentation

[Symptoms, signs, typical presentations]

### Medications

[Evidence-based regimens, dosing, contraindications]

### Labs & Vitals

[Expected values, ranges, coherence rules]

### Complications

[Common complications, timelines, risk factors]

## Example Requests and Interpretations

**Request:** "[user request]"

**Interpretation:** [How Claude should interpret this]

**Example Output:** [Sample generated patient]
```

## Example: Sepsis Cohort

Create `skills/sepsis.md`:

```markdown
# Sepsis Management Cohort

**Version:** 2.0
**Category:** cohorts
**Last Updated:** 2025-01-26

## For Claude

This skill enables you to generate realistic sepsis patients presenting to the Emergency Department or ICU, with appropriate clinical timelines, SIRS criteria, organ dysfunction, and treatment protocols following Surviving Sepsis Campaign guidelines.

## When to Use This Skill

Use this skill when requests involve:
- Sepsis, severe sepsis, or septic shock patients
- ED presentations with infection and SIRS
- ICU patients requiring vasopressor support
- Testing sepsis early warning systems (SEWS, qSOFA)
- Antimicrobial stewardship cohorts

## Domain Knowledge

### Clinical Definitions

**SIRS (Systemic Inflammatory Response Syndrome):**
≥2 of the following:
- Temperature >38°C or <36°C
- Heart rate >90 bpm
- Respiratory rate >20 or PaCO2 <32 mmHg
- WBC >12,000 or <4,000 or >10% bands

**Sepsis:** SIRS + documented or suspected infection

**Severe Sepsis:** Sepsis + organ dysfunction
- Hypotension (SBP <90 or MAP <65)
- Lactate >2 mmol/L
- Creatinine >2.0 mg/dL or UOP <0.5 mL/kg/hr
- Bilirubin >2 mg/dL
- Platelets <100,000
- INR >1.5

**Septic Shock:** Severe sepsis + persistent hypotension despite fluid resuscitation

### Common Sources

- Pneumonia (35%)
- Urinary tract infection (25%)
- Intra-abdominal infection (20%)
- Skin/soft tissue (10%)
- Other/unknown (10%)

### Microbiology

**Gram-positive:**
- Staphylococcus aureus (MRSA/MSSA)
- Streptococcus pneumoniae
- Enterococcus

**Gram-negative:**
- Escherichia coli
- Klebsiella pneumoniae
- Pseudomonas aeruginosa

## Generation Guidelines

### Patient Demographics

- Age: Typically 60-85 (higher risk)
- Risk factors: Diabetes, immunosuppression, chronic illness
- Recent hospitalization or nursing home residence

### ED Presentation Timeline

```
T=0: Symptom onset (fever, chills, confusion)
T=6-24h: Presents to ED
T=0 (ED): Triage vitals show SIRS criteria
T=30min: Labs drawn (lactate, WBC, blood cultures)
T=1h: Antibiotics initiated (door-to-antibiotic <1h goal)
T=1-3h: Fluid resuscitation (30 mL/kg crystalloid)
T=3h: Reassess, may need ICU/vasopressors
```

### Vital Signs (Septic Patient)

- Temperature: 102-104°F (38.9-40°C) or <96°F (35.6°C)
- Heart Rate: 110-140 bpm (tachycardic)
- Respiratory Rate: 24-32 (tachypneic)
- Blood Pressure: 85/50 - 100/60 (hypotensive)
- SpO2: 88-94% on room air

### Laboratory Values

**Sepsis Panel:**
- WBC: 18,000-25,000 (leukocytosis) or <4,000 (leukopenia)
- Bands: 15-25% (left shift)
- Lactate: 3.5-6.0 mmol/L (elevated)
- Creatinine: 1.8-3.5 mg/dL (AKI)
- Bilirubin: 2.5-4.0 mg/dL (hepatic dysfunction)
- Platelets: 80,000-120,000 (thrombocytopenia)
- Procalcitonin: 5-20 ng/mL (bacterial infection)

**Blood Cultures:** 2 sets drawn before antibiotics

### Antibiotics (Empiric)

**Source Unknown:**
- Vancomycin 15-20 mg/kg IV + Piperacillin-tazobactam 4.5g IV Q6H

**Pneumonia:**
- Vancomycin + Ceftriaxone 2g IV daily + Azithromycin 500mg IV daily

**Urinary Source:**
- Ceftriaxone 1-2g IV daily

**Intra-abdominal:**
- Piperacillin-tazobactam or Meropenem 1g IV Q8H

### Fluid Resuscitation

- Initial: 30 mL/kg crystalloid (LR or NS) within 3 hours
- Reassess: CVP, ScvO2, lactate clearance
- If still hypotensive: Start vasopressors (norepinephrine)

### ICU Management

**Vasopressor Support:**
- Norepinephrine 0.05-0.5 mcg/kg/min (first-line)
- Vasopressin 0.03 units/min (adjunct)
- Target MAP ≥65 mmHg

**Mechanical Ventilation:**
- If respiratory failure develops
- Low tidal volume (6 mL/kg IBW)
- PEEP 5-10 cmH2O

## Example Requests and Interpretations

**Request:** "Generate a septic patient for ED testing"

**Interpretation:** Create patient with sepsis from pneumonia, showing SIRS criteria, elevated lactate, and appropriate ED management timeline

**Example Output:**
```
Michael Anderson, 72M, MRN-837492
- PMH: COPD, diabetes
- Presentation: Fever (103.2°F), cough, confusion × 2 days
- Vitals: T 103.2, HR 125, RR 28, BP 88/52, SpO2 91% RA
- SIRS: 4/4 criteria met ✓
- Labs: WBC 22.5k, lactate 4.2, Cr 2.1
- CXR: Right lower lobe infiltrate
- Diagnosis: Severe sepsis (pneumonia source)
- Treatment:
  - Blood cultures × 2
  - Vancomycin 1.5g IV + Ceftriaxone 2g IV + Azithromycin 500mg IV
  - 2L NS bolus → BP improved to 102/65
  - Admitted to ICU
```

**Request:** "Generate septic shock patient requiring vasopressors"

**Interpretation:** Create patient with persistent hypotension despite 30 mL/kg fluids, needing ICU admission and norepinephrine

**Example Output:**
```
Dorothy Williams, 68F, MRN-648291
- PMH: Diabetes, CKD Stage 3
- Presentation: Urosepsis (E. coli UTI)
- Vitals: T 101.8, HR 132, RR 30, BP 78/45
- Labs: WBC 28k, lactate 5.8, Cr 3.2
- Fluid resuscitation: 2.5L NS → BP only to 85/50
- Septic shock confirmed
- ICU admission:
  - Norepinephrine started at 0.1 mcg/kg/min
  - Titrated to MAP >65
  - Vancomycin + Ceftriaxone
  - Requiring mechanical ventilation
```

## Clinical Pearls

- Door-to-antibiotic time <1 hour improves mortality
- Lactate clearance >10% at 6h predicts better outcomes
- Early goal-directed therapy no longer standard (PROCESS trial)
- Source control essential (drain abscess, remove infected device)
- De-escalate antibiotics based on cultures (antimicrobial stewardship)

## Validation Rules

- SIRS criteria: Must have ≥2 of 4 criteria
- Sepsis: SIRS + infection source documented
- Severe sepsis: Must have organ dysfunction
- Antibiotics: Broad-spectrum initially, then targeted
- Timeline: Antibiotics within 1h, fluids within 3h

## References

- Surviving Sepsis Campaign Guidelines 2021
- SCCM/ESICM Sepsis-3 Definitions 2016
```

## Skill Development Workflow

1. **Research clinical guidelines**
   - ADA, AHA/ACC, NICE, UpToDate

2. **Define scope**
   - What cohorts does this cover?
   - What does it NOT cover?

3. **Write skill sections**
   - For Claude (conversational)
   - Domain Knowledge (clinical depth)
   - Generation Guidelines (parameters)
   - Examples (show, don't just tell)

4. **Test with Claude**
   - Add to Claude Project
   - Generate test patients
   - Refine based on results

5. **Add validation rules**
   - Clinical plausibility checks
   - Format compliance

6. **Document**
   - Update README
   - Add to skill index

## See Also

- [Skills Format v1.0](format-specification.md) - Original specification
- [Skills Format v2.0](format-specification-v2.md) - Claude-optimized format
- [Migration Guide](migration-guide.md) - Migrating v1.0 to v2.0
- [Existing Skills](../../skills/) - Reference implementations
