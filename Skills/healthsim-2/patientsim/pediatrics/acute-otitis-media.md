---
name: acute-otitis-media
description: "Pediatric ear infections including acute otitis media (AOM) and recurrent ear infections. Triggers: ear infection, otitis media, AOM, amoxicillin child, pediatric ENT, ear tubes, myringotomy, ear pain, pediatric fever"
---

# Acute Otitis Media Cohort

A cohort template for generating pediatric patients with ear infections, including acute otitis media (AOM), otitis media with effusion (OME), and recurrent ear infections.

## For Claude

Use this skill when the user requests pediatric ear infection patients. This teaches you how to generate **realistic acute otitis media presentations** with appropriate age-based treatment protocols per AAP guidelines.

**When to apply this skill:**
- User mentions ear infection, otitis media, or AOM
- User requests amoxicillin for a child
- User asks for pediatric ENT cohorts
- User needs ear tube (myringotomy) candidates
- User specifies young children with ear pain or fever

**Key capabilities this skill provides:**
- How to classify AOM severity (mild, moderate, severe)
- How to apply AAP watchful waiting vs. antibiotic criteria
- How to match age-appropriate antibiotic dosing
- How to model recurrent AOM and referral criteria
- How to handle treatment failures and resistant organisms

## Metadata
- **Type**: cohort-template
- **Version**: 1.0
- **Author**: PatientSim
- **Tags**: pediatrics, ENT, infectious-disease, primary-care
- **Updated**: 2025-01-15

## Purpose

This cohort generates realistic pediatric ear infection patients from ages 6 months to 12 years, modeling severity, treatment decisions per AAP guidelines, recurrence patterns, and ENT referral criteria.

## When to Use This Skill

Apply this skill when the user's request involves:

**Direct Keywords**:
- "ear infection", "otitis media", "AOM"
- "ear pain" (in children)
- "amoxicillin" (pediatric context)
- "ear tubes", "myringotomy", "PE tubes"
- "middle ear", "tympanic membrane"

**Clinical Cohorts**:
- "Generate a child with an ear infection"
- "Create a pediatric patient with recurrent AOM"
- "Generate a toddler with fever and ear pain"

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| age_range | range | 1-5 | Patient age range (6mo-12yr) |
| severity | enum | moderate | mild, moderate, severe |
| laterality | enum | unilateral | unilateral, bilateral |
| recurrent | boolean | false | History of recurrent AOM |
| treatment_failure | boolean | false | Failed initial antibiotic |
| geography | string | null | County/tract FIPS for local patterns |

## Data Sources (PopulationSim v2.0)

When geography is specified, AOM cohorts reflect local demographic and healthcare access patterns:

### Embedded Data Lookup

```
File: skills/populationsim/data/county/svi_county_2022.csv
Key columns for pediatric patterns:
  - EP_AGE17: Percentage under 18 (pediatric population)
  - EP_UNINSUR: Uninsured rate (access to care)
  - RPL_THEMES: Overall vulnerability
  - EP_POV150: Poverty rate (daycare exposure proxy)
```

### Data-Driven Patterns

| Factor | Generic Default | Data-Driven Adjustment |
|--------|-----------------|------------------------|
| Daycare exposure | 50% | Higher if EP_POV150 < 30% (working families) |
| Antibiotic access delay | Low | Higher if EP_UNINSUR > 15% |
| Recurrence rate | 20% | Higher in high-vulnerability areas |
| ENT referral timing | Prompt | Delayed if SVI > 0.7 |

### Example: Jefferson County, AL (FIPS 01073)
```
From svi_county_2022.csv:
  EP_AGE17: 21.8%
  EP_UNINSUR: 11.2%
  RPL_THEMES: 0.58
  EP_POV150: 24.6%

Apply to generation:
  - Moderate pediatric population
  - Some delay in antibiotic initiation patterns
  - Standard recurrence rates
```

## Generation Rules

### Demographics
- Peak age: 6-24 months
- Male predominance (slight)
- Risk factors: daycare, smoke exposure, bottle feeding, no breastfeeding
- Season: Fall/Winter (viral URI season)

### Diagnosis Codes

| Code | Description | Use |
|------|-------------|-----|
| H66.001 | AOM with spontaneous rupture, right ear | Ruptured TM, right |
| H66.002 | AOM with spontaneous rupture, left ear | Ruptured TM, left |
| H66.003 | AOM with spontaneous rupture, bilateral | Ruptured TM, bilateral |
| H66.011 | AOM, recurrent, right ear | Recurrent, right |
| H66.012 | AOM, recurrent, left ear | Recurrent, left |
| H66.013 | AOM, recurrent, bilateral | Recurrent, bilateral |
| H66.91 | Otitis media, unspecified, right ear | Unspecified, right |
| H66.92 | Otitis media, unspecified, left ear | Unspecified, left |
| H66.93 | Otitis media, unspecified, bilateral | Unspecified, bilateral |
| H65.191 | Other acute nonsuppurative OM, right ear | OME, right |
| H65.192 | Other acute nonsuppurative OM, left ear | OME, left |
| H65.193 | Other acute nonsuppurative OM, bilateral | OME, bilateral |

### Severity Classification (AAP Guidelines)

#### Mild AOM
- Mild otalgia <48 hours
- Temperature <39°C (102.2°F)
- Unilateral
- Age ≥2 years
- **Treatment**: Watchful waiting option (48-72h observation)

#### Moderate AOM
- Moderate otalgia
- Temperature <39°C
- May be unilateral or bilateral
- **Treatment**: Antibiotics indicated

#### Severe AOM
- Moderate to severe otalgia ≥48 hours OR
- Temperature ≥39°C
- **Treatment**: Antibiotics required

### Treatment Decision Algorithm (AAP 2013)

| Age | Otorrhea | Bilateral AOM | Severe Symptoms | Unilateral, Non-severe |
|-----|----------|---------------|-----------------|------------------------|
| 6-23 mo | Antibiotics | Antibiotics | Antibiotics | Antibiotics OR Observe |
| ≥2 yr | Antibiotics | Antibiotics OR Observe | Antibiotics | Observe |

### First-Line Antibiotics

| Antibiotic | Dose | Frequency | Duration | Use |
|------------|------|-----------|----------|-----|
| Amoxicillin | 80-90 mg/kg/day | Divided BID or TID | 10 days (<2yr), 5-7 days (≥2yr) | First-line |
| Amoxicillin-clavulanate | 90 mg/kg/day amox component | Divided BID | 10 days | Penicillin allergy (non-severe), treatment failure |

### Second-Line Antibiotics (Treatment Failure)

| Antibiotic | Dose | Frequency | Duration | Use |
|------------|------|-----------|----------|-----|
| Amoxicillin-clavulanate | 90 mg/kg/day | Divided BID | 10 days | First-line failure |
| Ceftriaxone IM | 50 mg/kg | Daily x 3 days | 3 days | Vomiting, non-compliance |
| Cefdinir | 14 mg/kg/day | Once daily | 5-10 days | Mild penicillin allergy |
| Cefuroxime | 30 mg/kg/day | Divided BID | 10 days | Alternative |
| Azithromycin | 10 mg/kg day 1, then 5 mg/kg | Once daily | 5 days | Type I penicillin allergy |

### Pain Management

| Medication | Dose | Frequency | Notes |
|------------|------|-----------|-------|
| Acetaminophen | 15 mg/kg | q4-6h PRN | Max 75 mg/kg/day |
| Ibuprofen | 10 mg/kg | q6-8h PRN | Age ≥6 mo, max 40 mg/kg/day |
| Benzocaine otic drops | 4 drops | q1-2h PRN | Age ≥2 yr, intact TM only |

### Physical Exam Findings

| Finding | Description | Significance |
|---------|-------------|--------------|
| TM bulging | Outward displacement | Strong indicator of AOM |
| TM erythema | Redness | Supports AOM (less specific) |
| TM mobility | Decreased or absent | Effusion present |
| Air-fluid level | Visible behind TM | Middle ear effusion |
| Perforation | Hole in TM | AOM with rupture |
| Otorrhea | Drainage from ear | Ruptured TM or tubes |

### Recurrent AOM Criteria
- ≥3 episodes in 6 months OR
- ≥4 episodes in 12 months with ≥1 in past 6 months
- Consider ENT referral for tympanostomy tubes

### ENT Referral Indications
- Recurrent AOM meeting criteria
- Persistent OME >3 months
- Hearing loss concerns
- Suspected cholesteatoma
- Treatment failures
- Structural abnormalities

### Complications (Rare but Important)
| Complication | Code | Description |
|--------------|------|-------------|
| Mastoiditis | H70.001 | Infection of mastoid bone |
| TM perforation | H72.01 | Persistent perforation |
| Hearing loss | H90.0 | Conductive hearing loss |
| Cholesteatoma | H71.01 | Epithelial growth |

## Variations

### Typical First Episode AOM
- Age: 18 months
- Unilateral, moderate severity
- Temperature 38.5°C
- Treatment: Amoxicillin 80 mg/kg/day x 10 days

### Bilateral AOM in Infant
- Age: 10 months
- Bilateral, moderate severity
- Temperature 39°C
- Treatment: Amoxicillin 90 mg/kg/day x 10 days

### Treatment Failure
- Age: 2 years
- Failed amoxicillin after 48-72 hours
- Persistent fever, otalgia
- Treatment: Amoxicillin-clavulanate or Ceftriaxone IM

### Recurrent AOM - Tube Candidate
- Age: 3 years
- 5 episodes in past 12 months
- ENT referral for myringotomy with PE tubes
- Hearing evaluation ordered

### AOM with Perforation
- Age: 4 years
- Sudden pain relief followed by drainage
- TM perforation noted
- Treatment: Oral antibiotics + topical ofloxacin drops

## Examples

### Example 1: Typical AOM
```json
{
  "patient": {
    "mrn": "MRN00000001",
    "name": { "given_name": "Sophia", "family_name": "Rodriguez" },
    "birth_date": "2023-03-15",
    "gender": "F",
    "age_months": 22
  },
  "encounter": {
    "type": "sick visit",
    "chief_complaint": "Ear pain and fever x1 day"
  },
  "diagnoses": [
    { "code": "H66.91", "description": "Otitis media, unspecified, right ear" }
  ],
  "vitals": {
    "temperature": 38.8,
    "heart_rate": 130,
    "respiratory_rate": 28,
    "weight_kg": 11.5
  },
  "physical_exam": {
    "right_ear": "TM bulging, erythematous, decreased mobility",
    "left_ear": "TM clear, mobile, normal landmarks"
  },
  "medications": [
    {
      "name": "Amoxicillin",
      "dose": "460 mg",
      "frequency": "BID",
      "duration": "10 days",
      "calculated_dose": "80 mg/kg/day"
    },
    {
      "name": "Acetaminophen",
      "dose": "175 mg",
      "frequency": "q4-6h PRN",
      "calculated_dose": "15 mg/kg"
    }
  ]
}
```

### Example 2: Recurrent AOM
```json
{
  "patient": {
    "mrn": "MRN00000002",
    "name": { "given_name": "Ethan", "family_name": "Johnson" },
    "birth_date": "2021-07-10",
    "gender": "M",
    "age": 3
  },
  "diagnoses": [
    { "code": "H66.013", "description": "Acute otitis media, recurrent, bilateral" }
  ],
  "history": {
    "aom_episodes": [
      { "date": "2024-08-15", "treatment": "Amoxicillin" },
      { "date": "2024-10-02", "treatment": "Amoxicillin" },
      { "date": "2024-11-20", "treatment": "Augmentin" },
      { "date": "2025-01-05", "treatment": "Augmentin" }
    ],
    "risk_factors": ["Daycare attendance", "Secondhand smoke exposure"]
  },
  "plan": {
    "referral": "ENT for evaluation of tympanostomy tubes",
    "audiology": "Hearing evaluation ordered",
    "treatment": "Amoxicillin-clavulanate pending ENT"
  }
}
```

## Trigger Phrases

- ear infection
- otitis media
- AOM
- ear pain child
- amoxicillin pediatric
- ear tubes
- myringotomy
- recurrent ear infections
- middle ear infection
- otalgia

## Validation Rules

| Rule | Requirement | Example |
|------|-------------|---------|
| Age | Typically 6mo-6yr | 2 years |
| Temperature | May be elevated | 101.5°F |
| Ear affected | left, right, bilateral | "right" |
| TM appearance | bulging, erythematous, etc. | "bulging with effusion" |
| Antibiotic | Weight-based dosing | Amoxicillin 90mg/kg/day |
| Duration | Days of symptoms | 3 days |
| Severity | mild, moderate, severe | "moderate" |
| Recurrence | Episodes in past 6-12 mo | 3 episodes in 6 months |

### Business Rules

- **Observation Option**: Age ≥2, unilateral, non-severe → can observe 48-72h
- **Immediate Antibiotics**: Age <2, bilateral, severe symptoms, high fever
- **First-line Antibiotic**: High-dose amoxicillin (80-90 mg/kg/day)
- **Penicillin Allergy**: Cephalosporin or macrolide
- **Treatment Failure**: No improvement at 48-72h → switch antibiotic
- **Recurrent AOM**: ≥3 episodes in 6 mo or ≥4 in 12 mo → consider ENT referral
- **Tympanostomy Tubes**: For recurrent AOM or chronic OME
- **Pain Management**: Acetaminophen or ibuprofen for otalgia

## Dependencies

- [../../../references/code-systems.md](../../../references/code-systems.md) - ICD-10 ENT codes
- [../../../formats/fhir-r4.md](../../../formats/fhir-r4.md) - FHIR resources

## Related Skills

- [childhood-asthma.md](childhood-asthma.md) - Often triggered by same viruses
- [../diabetes-management.md](../diabetes-management.md) - For weight-based dosing reference
- [../../membersim/professional-claims.md](../../membersim/professional-claims.md) - Claims for pediatric visits
