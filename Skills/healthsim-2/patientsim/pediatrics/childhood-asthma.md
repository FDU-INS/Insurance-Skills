---
name: childhood-asthma
description: "Pediatric asthma patients across severity levels including acute exacerbations. Triggers: childhood asthma, pediatric asthma, wheezing, albuterol, inhaled steroids, asthma action plan, pediatric respiratory, children breathing"
---

# Childhood Asthma Cohort

A cohort template for generating pediatric patients with asthma across severity levels, from intermittent to severe persistent, including acute exacerbations.

## For Claude

Use this skill when the user requests pediatric asthma patients or childhood respiratory cohorts. This teaches you how to generate **realistic pediatric asthma presentations** across all severity classifications with appropriate age-based treatment protocols.

**When to apply this skill:**
- User mentions childhood asthma, pediatric asthma, or wheezing in children
- User requests albuterol, inhaled steroids, or asthma medications for children
- User asks for asthma action plans or exacerbation cohorts
- User needs pediatric respiratory data
- User specifies ages under 18 with breathing problems

**Key capabilities this skill provides:**
- How to classify asthma severity (NHLBI guidelines)
- How to match age-appropriate medication dosing
- How to generate realistic spirometry values (age 6+)
- How to model acute exacerbations and ED visits
- How to track controller medication adherence

## Metadata
- **Type**: cohort-template
- **Version**: 1.0
- **Author**: PatientSim
- **Tags**: pediatrics, asthma, respiratory, pulmonology, primary-care
- **Updated**: 2025-01-15

## Purpose

This cohort generates realistic pediatric asthma patients from ages 2-17, modeling severity classification, treatment escalation, and acute exacerbations according to current NHLBI/GINA guidelines.

## When to Use This Skill

Apply this skill when the user's request involves:

**Direct Keywords**:
- "childhood asthma", "pediatric asthma"
- "wheezing", "wheeze" (in children)
- "albuterol", "inhaler" (pediatric context)
- "asthma exacerbation", "asthma attack"
- "child with breathing problems"

**Clinical Cohorts**:
- "Generate a child with asthma"
- "Create a pediatric patient with an asthma flare"
- "Generate an asthmatic child needing controller medication"

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| age_range | range | 5-12 | Patient age range (2-17) |
| severity | enum | mild-persistent | intermittent, mild-persistent, moderate-persistent, severe-persistent |
| cohort_type | enum | routine | routine, exacerbation, ED-visit, hospitalization |
| has_allergies | boolean | true | Include allergic triggers |
| controller_compliant | boolean | true | Good controller medication adherence |
| geography | string | null | County/tract FIPS for local asthma prevalence |

## Data Sources (PopulationSim v2.0)

When geography is specified, pediatric asthma cohorts reflect local prevalence patterns:

### Embedded Data Lookup

```
File: skills/populationsim/data/county/places_county_2024.csv
Key columns:
  - CASTHMA_CrudePrev: Current asthma prevalence (all ages)
  - CSMOKING_CrudePrev: Smoking rate (environmental trigger)

File: skills/populationsim/data/county/svi_county_2022.csv
Key columns:
  - RPL_THEMES: Vulnerability (affects control, ED utilization)
  - EP_POV150: Poverty rate (medication access)
```

### Data-Driven Patterns

| Factor | Generic Default | Data-Driven Adjustment |
|--------|-----------------|------------------------|
| Asthma prevalence | 8% | CASTHMA_CrudePrev (ranges 6-15%) |
| Poorly controlled | 40% | Higher if SVI > 0.6 |
| ED visits/year | 0.5 | Higher if EP_POV150 > 25% |
| Smoke exposure | 15% | CSMOKING_CrudePrev |

### Example: Bronx County, NY (FIPS 36005)
```
From places_county_2024.csv:
  CASTHMA_CrudePrev: 11.2% (high)
  CSMOKING_CrudePrev: 14.1%

From svi_county_2022.csv:
  RPL_THEMES: 0.94 (very high vulnerability)
  EP_POV150: 38.2%

Apply to generation:
  - Higher baseline asthma prevalence
  - More moderate-to-severe classifications
  - Higher ED utilization patterns
  - More missed controller doses (access barriers)
```

## Generation Rules

### Demographics
- Age range: 2-17 years
- Male predominance in young children (reverses in adolescence)
- Higher prevalence with family history of atopy
- Environmental factors: urban, smoke exposure

### Asthma Severity Classification (NHLBI)

#### Intermittent
- Symptoms ≤2 days/week
- Nighttime awakenings ≤2x/month
- SABA use ≤2 days/week
- No interference with activity
- FEV1 >80% predicted (if age ≥6)
- Treatment: SABA PRN only

#### Mild Persistent
- Symptoms >2 days/week (not daily)
- Nighttime awakenings 3-4x/month
- SABA use >2 days/week (not daily)
- Minor limitation of activity
- FEV1 ≥80% predicted
- Treatment: Low-dose ICS

#### Moderate Persistent
- Daily symptoms
- Nighttime awakenings >1x/week
- Daily SABA use
- Some limitation of activity
- FEV1 60-80% predicted
- Treatment: Low-dose ICS + LABA or Medium-dose ICS

#### Severe Persistent
- Symptoms throughout day
- Nighttime awakenings often 7x/week
- SABA use several times/day
- Extremely limited activity
- FEV1 <60% predicted
- Treatment: High-dose ICS + LABA, consider biologics

### Diagnosis Codes

| Code | Description | Use |
|------|-------------|-----|
| J45.20 | Mild intermittent asthma, uncomplicated | Intermittent |
| J45.30 | Mild persistent asthma, uncomplicated | Mild persistent |
| J45.40 | Moderate persistent asthma, uncomplicated | Moderate persistent |
| J45.50 | Severe persistent asthma, uncomplicated | Severe persistent |
| J45.21 | Mild intermittent asthma with acute exacerbation | Intermittent flare |
| J45.31 | Mild persistent asthma with acute exacerbation | Mild flare |
| J45.41 | Moderate persistent asthma with acute exacerbation | Moderate flare |
| J45.51 | Severe persistent asthma with acute exacerbation | Severe flare |
| J45.901 | Unspecified asthma with acute exacerbation | Exacerbation NOS |
| J45.902 | Unspecified asthma with status asthmaticus | Status asthmaticus |

### Comorbidities
| Condition | Code | Prevalence |
|-----------|------|------------|
| Allergic rhinitis | J30.9 | 75% |
| Atopic dermatitis | L20.9 | 30% |
| Food allergies | T78.1 | 20% |
| Obesity | E66.9 | 25% |
| GERD | K21.0 | 15% |

### Medications by Age and Severity

#### Rescue Medications (All Patients)
| Medication | Age | Dose |
|------------|-----|------|
| Albuterol MDI + spacer | 2+ | 2-4 puffs q4-6h PRN |
| Albuterol nebulizer | 2+ | 2.5 mg q4-6h PRN |
| Levalbuterol MDI | 4+ | 2 puffs q4-6h PRN |

#### Low-Dose ICS (Mild Persistent)
| Medication | Age | Low Dose |
|------------|-----|----------|
| Fluticasone HFA | 4+ | 88 mcg BID |
| Budesonide nebulizer | 1-8 | 0.25-0.5 mg BID |
| Beclomethasone | 5+ | 40-80 mcg BID |
| Mometasone | 4+ | 110 mcg QD |

#### Medium-Dose ICS (Moderate Persistent)
| Medication | Age | Medium Dose |
|------------|-----|-------------|
| Fluticasone HFA | 4+ | 110-220 mcg BID |
| Budesonide nebulizer | 1-8 | 0.5-1 mg BID |
| Fluticasone/Salmeterol | 4+ | 100/50 mcg BID |

#### High-Dose ICS/LABA (Severe Persistent)
| Medication | Age | High Dose |
|------------|-----|-----------|
| Fluticasone HFA | 4+ | >220 mcg BID |
| Fluticasone/Salmeterol | 4+ | 250/50 mcg BID |
| Budesonide/Formoterol | 6+ | 160/4.5 mcg BID |
| Mometasone/Formoterol | 5+ | 200/5 mcg BID |

#### Add-On Therapies (Severe)
| Medication | Age | Dose |
|------------|-----|------|
| Montelukast | 2+ | 4 mg (2-5), 5 mg (6-14), 10 mg (15+) |
| Tiotropium | 6+ | 2.5 mcg QD |
| Omalizumab | 6+ | Weight/IgE based |
| Dupilumab | 6+ | 200-300 mg q2wk |

### Spirometry Values (Age ≥6)

| Severity | FEV1 % Predicted | FEV1/FVC |
|----------|------------------|----------|
| Normal | ≥80% | ≥85% |
| Mild obstruction | 70-79% | 75-84% |
| Moderate obstruction | 60-69% | 65-74% |
| Severe obstruction | <60% | <65% |

### Acute Exacerbation Assessment

| Severity | SpO2 | Respiratory Rate | Accessory Muscles | Speech |
|----------|------|------------------|-------------------|--------|
| Mild | ≥94% | Normal to mild increase | None | Full sentences |
| Moderate | 90-94% | Increased | Some use | Phrases |
| Severe | <90% | Significantly increased | Marked use | Words only |

### Triggers
- Viral URI (most common in children)
- Allergens: dust mites, mold, pets, pollen
- Exercise
- Cold air
- Smoke exposure
- Weather changes

## Variations

### Well-Controlled Mild Persistent
- Age: 8 years
- Diagnosis: J45.30
- Medications: Fluticasone 44 mcg BID, Albuterol PRN
- Last exacerbation: >6 months ago
- Good inhaler technique

### Moderate Persistent with Recent Exacerbation
- Age: 6 years
- Diagnosis: J45.41
- Medications: Fluticasone/Salmeterol 100/50 BID, Albuterol PRN
- Recent ED visit, oral steroid burst
- Step-up therapy being considered

### Severe Persistent on Biologic
- Age: 12 years
- Diagnosis: J45.50
- Medications: High-dose ICS/LABA, Montelukast, Omalizumab monthly
- Multiple hospitalizations
- Elevated IgE, eosinophilia

### Acute Exacerbation (ED Visit)
- Age: 5 years
- Diagnosis: J45.901
- Presenting: Wheezing, SpO2 91%, RR 32
- Treatment: Albuterol nebs q20min x3, oral prednisone
- Disposition: Observation vs. discharge

## Examples

### Example 1: Well-Controlled Asthma
```json
{
  "patient": {
    "mrn": "MRN00000001",
    "name": { "given_name": "Emma", "family_name": "Chen" },
    "birth_date": "2016-04-12",
    "gender": "F",
    "age": 8
  },
  "diagnoses": [
    { "code": "J45.30", "description": "Mild persistent asthma, uncomplicated" },
    { "code": "J30.9", "description": "Allergic rhinitis, unspecified" }
  ],
  "medications": [
    { "name": "Fluticasone HFA", "dose": "44 mcg", "frequency": "2 puffs BID", "status": "active" },
    { "name": "Albuterol HFA", "dose": "90 mcg", "frequency": "2 puffs PRN", "status": "active" }
  ],
  "asthma_control": {
    "last_exacerbation": "2024-03-15",
    "nighttime_symptoms": "0/month",
    "rescue_inhaler_use": "1-2x/week",
    "activity_limitation": "none"
  }
}
```

### Example 2: Acute Exacerbation
```json
{
  "patient": {
    "mrn": "MRN00000002",
    "name": { "given_name": "Jayden", "family_name": "Williams" },
    "birth_date": "2019-08-20",
    "gender": "M",
    "age": 5
  },
  "diagnoses": [
    { "code": "J45.41", "description": "Moderate persistent asthma with acute exacerbation" }
  ],
  "encounter": {
    "type": "ED visit",
    "chief_complaint": "Wheezing and shortness of breath x2 days",
    "trigger": "Viral URI"
  },
  "vitals": {
    "respiratory_rate": 32,
    "spo2": 91,
    "heart_rate": 120,
    "temperature": 99.2
  },
  "physical_exam": {
    "lungs": "Diffuse expiratory wheezes, moderate retractions",
    "accessory_muscles": "Suprasternal and intercostal retractions"
  },
  "treatment": [
    { "medication": "Albuterol nebulizer", "dose": "2.5 mg", "frequency": "q20min x3" },
    { "medication": "Prednisolone", "dose": "30 mg", "route": "PO", "frequency": "once" }
  ]
}
```

## Trigger Phrases

- childhood asthma
- pediatric asthma
- asthma in children
- wheezing child
- inhaler for child
- asthma exacerbation
- asthma attack
- albuterol nebulizer
- controller medication
- asthma action plan

## Validation Rules

| Rule | Requirement | Example |
|------|-------------|---------|
| Age | Typically 2-18 years | 8 years |
| Severity | intermittent, mild, moderate, severe | "moderate persistent" |
| Peak flow | % predicted | 75% predicted |
| O2 saturation | 90-100% | 94% |
| Rescue inhaler use | Days per week | 3 days/week |
| Night symptoms | Nights per month | 4 nights/month |
| Controller meds | ICS dose category | Low-dose ICS |
| Exacerbations | Per year requiring steroids | 2 per year |

### Business Rules

- **Classification**: Based on symptoms, night awakenings, rescue use, FEV1
- **Intermittent**: Symptoms ≤2 days/wk, ≤2 nights/mo → SABA PRN only
- **Persistent**: Symptoms >2 days/wk → Daily controller (ICS)
- **Step Therapy**: Start at step matching severity; step up/down based on control
- **Controller Options**: ICS, ICS/LABA, leukotriene modifiers
- **Spacer Use**: Required for MDI in children; improves delivery
- **Asthma Action Plan**: Green/yellow/red zones based on symptoms and peak flow
- **Annual Assessment**: Review control, adjust step, update action plan

## Dependencies

- [../../../references/code-systems.md](../../../references/code-systems.md) - ICD-10 respiratory codes
- [../../../formats/fhir-r4.md](../../../formats/fhir-r4.md) - FHIR resources

## Related Skills

- [acute-otitis-media.md](acute-otitis-media.md) - Common pediatric infection
- [../sepsis-acute-care.md](../sepsis-acute-care.md) - For severe respiratory distress
- [../../../formats/hl7v2-adt.md](../../../formats/hl7v2-adt.md) - ED admission messages
