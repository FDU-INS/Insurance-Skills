# Clinical Business Rules Reference

## Overview

This reference defines clinical business rules and guidelines for generating realistic, coherent healthcare data. These rules ensure generated data reflects real-world clinical patterns and constraints.

## Age-Appropriate Conditions

### Pediatric (0-17 years)

**Common Conditions:**
- Acute otitis media (H66.x)
- Upper respiratory infections (J06.x)
- Asthma (J45.x)
- ADHD (F90.x)
- Allergic rhinitis (J30.x)
- Streptococcal pharyngitis (J02.0)
- Viral gastroenteritis (A08.x)

**Rare/Unlikely:**
- Type 2 diabetes (under age 10)
- Osteoarthritis
- COPD
- Coronary artery disease
- Atrial fibrillation

**Age-Specific Considerations:**
| Age Range | Clinical Considerations |
|-----------|------------------------|
| 0-2 years | Well-child visits, immunizations, developmental milestones |
| 3-5 years | Preschool physicals, speech/language development |
| 6-12 years | School physicals, vision/hearing screening |
| 13-17 years | Adolescent wellness, sports physicals, mental health screening |

### Adult (18-64 years)

**Common Conditions by Decade:**

| Age Range | Common Conditions |
|-----------|------------------|
| 18-29 | Anxiety, depression, injuries, STIs, pregnancy |
| 30-39 | Hypertension onset, obesity, back pain, migraines |
| 40-49 | Hyperlipidemia, pre-diabetes, perimenopause |
| 50-64 | Type 2 diabetes, CAD risk, cancer screening age |

### Geriatric (65+ years)

**Common Conditions:**
- Hypertension (I10)
- Type 2 diabetes (E11.x)
- Hyperlipidemia (E78.x)
- Osteoarthritis (M15-M19)
- Osteoporosis (M80-M81)
- Atrial fibrillation (I48.x)
- Heart failure (I50.x)
- COPD (J44.x)
- Chronic kidney disease (N18.x)
- Dementia (F01-F03, G30)

**Polypharmacy Expectations:**
| Age | Expected Medications |
|-----|---------------------|
| 65-74 | 4-6 chronic medications |
| 75-84 | 6-8 chronic medications |
| 85+ | 8-10 chronic medications |

## Gender-Specific Conditions

### Female-Only Conditions
- Pregnancy-related (O00-O9A)
- Menstrual disorders (N91-N95)
- Breast conditions (N60-N65)
- Ovarian conditions (N83)
- Uterine conditions (N80-N85)
- Cervical conditions (N86-N88)
- Menopause (N95.1)

### Male-Only Conditions
- Prostate conditions (N40-N42)
- Testicular conditions (N43-N45)
- Erectile dysfunction (N52)
- Male pattern baldness (L64.0)

### Gender-Predominant Conditions

| Condition | Predominant Gender | Ratio |
|-----------|-------------------|-------|
| Osteoporosis | Female | 4:1 |
| Autoimmune thyroid | Female | 7:1 |
| Rheumatoid arthritis | Female | 3:1 |
| Lupus (SLE) | Female | 9:1 |
| Gout | Male | 4:1 |
| Hemophilia | Male | Nearly 100% |
| Abdominal aortic aneurysm | Male | 4:1 |

## Disease Progression Rules

### Diabetes Progression

```
Stage 1: Pre-diabetes (R73.03)
  ↓ (2-5 years untreated)
Stage 2: Type 2 Diabetes (E11.9)
  ↓ (5-10 years)
Stage 3: Diabetes with complications
  - Neuropathy (E11.40-E11.49)
  - Nephropathy (E11.21-E11.29)
  - Retinopathy (E11.31-E11.39)
  - Peripheral vascular (E11.51-E11.59)
```

**A1C Progression:**
| Stage | A1C Range | Typical Medications |
|-------|-----------|---------------------|
| Pre-diabetes | 5.7-6.4% | Lifestyle, possibly metformin |
| Well-controlled T2DM | 6.5-7.0% | Metformin |
| Moderate T2DM | 7.0-8.5% | Metformin + second agent |
| Poorly controlled T2DM | 8.5-10% | Multiple agents or insulin |
| Uncontrolled T2DM | >10% | Insulin required |

### Chronic Kidney Disease Progression

```
Stage 1: GFR ≥ 90, kidney damage present (N18.1)
  ↓
Stage 2: GFR 60-89, mild decrease (N18.2)
  ↓
Stage 3a: GFR 45-59, mild-moderate (N18.31)
  ↓
Stage 3b: GFR 30-44, moderate-severe (N18.32)
  ↓
Stage 4: GFR 15-29, severe (N18.4)
  ↓
Stage 5: GFR < 15 or dialysis (N18.5, N18.6)
```

**CKD Lab Expectations:**
| CKD Stage | Creatinine (mg/dL) | BUN (mg/dL) | Hemoglobin |
|-----------|-------------------|-------------|------------|
| 1-2 | 0.7-1.5 | 10-25 | Normal |
| 3a | 1.5-2.0 | 25-35 | Normal to low |
| 3b | 2.0-3.0 | 35-50 | 10-12 g/dL |
| 4 | 3.0-5.0 | 50-80 | 9-11 g/dL |
| 5 | >5.0 | >80 | 8-10 g/dL |

### Heart Failure Progression

**NYHA Classification:**
| Class | Symptoms | Typical BNP | EF (HFrEF) |
|-------|----------|-------------|------------|
| I | None with ordinary activity | <100 | 40-50% |
| II | Slight limitation | 100-300 | 30-40% |
| III | Marked limitation | 300-900 | 20-30% |
| IV | Symptoms at rest | >900 | <20% |

**Medication Escalation:**
```
NYHA I-II: ACEi/ARB + beta-blocker
  ↓
NYHA II-III: Add MRA (spironolactone)
  ↓
NYHA II-III: Add SGLT2i, consider ARNI
  ↓
NYHA III-IV: Add digoxin, diuretic adjustment
  ↓
NYHA IV: Consider advanced therapies (VAD, transplant)
```

### Hypertension Progression

**BP Categories:**
| Category | Systolic | Diastolic |
|----------|----------|-----------|
| Normal | <120 | <80 |
| Elevated | 120-129 | <80 |
| Stage 1 HTN | 130-139 | 80-89 |
| Stage 2 HTN | ≥140 | ≥90 |
| Crisis | >180 | >120 |

**Treatment Escalation:**
| Stage | Treatment Approach |
|-------|-------------------|
| Elevated | Lifestyle modification |
| Stage 1, low risk | Lifestyle 3-6 months, then medication |
| Stage 1, high risk | Medication + lifestyle |
| Stage 2 | Two medications, different classes |
| Resistant | 3+ medications including diuretic |

## Common Comorbidity Clusters

### Metabolic Syndrome Cluster
- Obesity (E66.x)
- Type 2 diabetes (E11.x)
- Hypertension (I10)
- Hyperlipidemia (E78.x)
- Fatty liver (K76.0)
- Obstructive sleep apnea (G47.33)

**Rule:** If patient has 2+ of these, consider adding related conditions.

### Cardiovascular Cluster
- Hypertension (I10)
- Coronary artery disease (I25.x)
- Heart failure (I50.x)
- Atrial fibrillation (I48.x)
- Peripheral vascular disease (I73.9)
- Chronic kidney disease (N18.x)

### Autoimmune Cluster
Patients with one autoimmune condition have higher risk of others:
- Rheumatoid arthritis (M05-M06)
- Hashimoto's thyroiditis (E06.3)
- Type 1 diabetes (E10.x)
- Celiac disease (K90.0)
- Psoriasis (L40.x)
- Inflammatory bowel disease (K50-K51)

### Mental Health Cluster
- Depression (F32-F33)
- Anxiety (F41.x)
- Insomnia (G47.0)
- Chronic pain (G89.x)
- Substance use (F10-F19)

## Medication-Condition Rules

### Required Medications by Condition

| Condition | Expected Medications |
|-----------|---------------------|
| Type 2 Diabetes | Metformin (first-line), possibly additional agents |
| Hypertension | ACEi/ARB, thiazide, CCB, or beta-blocker |
| Heart Failure (HFrEF) | ACEi/ARB/ARNI + beta-blocker + MRA |
| Atrial Fibrillation | Rate control + anticoagulation (if CHA2DS2-VASc ≥2) |
| Post-MI | Aspirin + statin + beta-blocker + ACEi |
| COPD | Inhaled bronchodilators, possibly ICS |
| Hypothyroidism | Levothyroxine |
| Osteoporosis | Bisphosphonate + calcium/vitamin D |
| GERD | PPI or H2 blocker |
| Depression | SSRI/SNRI or other antidepressant |

### Contraindicated Combinations

| Condition | Contraindicated Drug Classes |
|-----------|------------------------------|
| Asthma | Non-selective beta-blockers |
| Severe CKD (Stage 4-5) | NSAIDs, metformin, certain ACEi doses |
| Hyperkalemia | K-sparing diuretics, high-dose ACEi/ARB |
| Bradycardia | Beta-blockers, non-DHP CCBs |
| Pregnancy | ACEi, ARB, statins, warfarin |
| Gout | Thiazide diuretics, aspirin |
| Liver cirrhosis | Acetaminophen (high dose), NSAIDs |

### Drug-Drug Interactions (High Severity)

| Drug 1 | Drug 2 | Risk |
|--------|--------|------|
| Warfarin | NSAIDs | Bleeding |
| Warfarin | Antibiotics (fluoroquinolones) | INR elevation |
| ACEi | K-sparing diuretic | Hyperkalemia |
| Metformin | IV contrast | Lactic acidosis |
| MAOIs | SSRIs | Serotonin syndrome |
| Digoxin | Amiodarone | Digoxin toxicity |
| Simvastatin | Amiodarone | Myopathy |
| Clopidogrel | Omeprazole | Reduced efficacy |

## Laboratory Value Coherence

### Diabetes Labs
| A1C | Expected Fasting Glucose | Interpretation |
|-----|-------------------------|----------------|
| 5.0-5.6% | 70-99 mg/dL | Normal |
| 5.7-6.4% | 100-125 mg/dL | Pre-diabetes |
| 6.5-7.5% | 120-160 mg/dL | Well-controlled DM |
| 7.5-9.0% | 160-220 mg/dL | Moderately controlled |
| >9.0% | >220 mg/dL | Poorly controlled |

### Anemia Labs
| Hemoglobin | MCV | Iron | TIBC | Ferritin | Interpretation |
|------------|-----|------|------|----------|----------------|
| Low | Low | Low | High | Low | Iron deficiency |
| Low | High | Normal | Normal | Normal | B12/folate deficiency |
| Low | Normal | Normal | Normal | Normal/High | Anemia of chronic disease |
| Low | Normal | Low | Low | High | Anemia of chronic disease |

### Thyroid Labs
| TSH | Free T4 | Interpretation |
|-----|---------|----------------|
| Normal | Normal | Euthyroid |
| High | Low | Primary hypothyroidism |
| Low | High | Primary hyperthyroidism |
| High | Normal | Subclinical hypothyroidism |
| Low | Normal | Subclinical hyperthyroidism |

### Liver Panel Patterns
| Pattern | ALT | AST | ALP | Bilirubin | Interpretation |
|---------|-----|-----|-----|-----------|----------------|
| Hepatocellular | ↑↑↑ | ↑↑ | ↑ | ↑ | Hepatitis, drug injury |
| Cholestatic | ↑ | ↑ | ↑↑↑ | ↑↑ | Biliary obstruction |
| Mixed | ↑↑ | ↑↑ | ↑↑ | ↑ | Various liver diseases |

## Temporal Rules

### Visit Frequency by Condition

| Condition | Typical Visit Frequency |
|-----------|------------------------|
| Well-controlled chronic disease | Every 3-6 months |
| New diagnosis | Monthly until stable |
| Poorly controlled diabetes | Every 1-3 months |
| Heart failure exacerbation | Weekly until stable |
| Post-hospitalization | Within 7-14 days |
| Anticoagulation management | Monthly INR checks |
| Cancer treatment | Per protocol (often weekly-biweekly) |

### Lab Monitoring Frequency

| Test | Condition | Frequency |
|------|-----------|-----------|
| A1C | Diabetes | Every 3 months (poorly controlled) to 6 months (stable) |
| Lipid panel | Hyperlipidemia | Annually when stable, 6-12 weeks after med change |
| TSH | Hypothyroidism | Every 6-12 months when stable |
| INR | Warfarin therapy | Weekly to monthly |
| BMP | CKD or diuretic use | Every 3-6 months |
| CBC | Anemia or chemotherapy | Per clinical need |
| LFTs | Statin therapy | Baseline, then if symptoms |

### Medication Duration Rules

| Medication Type | Expected Duration |
|-----------------|-------------------|
| Antibiotics | 5-14 days typically |
| Chronic disease meds | Ongoing/indefinite |
| Post-MI therapy | Minimum 1 year, often indefinite |
| Anticoagulation for DVT | 3-6 months minimum |
| Bisphosphonates | 3-5 years, then reassess |
| Antidepressants | 6-12 months minimum, often longer |

## Claims Rules

### Medical Necessity

**Documentation Requirements:**
| Service | Required Documentation |
|---------|----------------------|
| High-level E&M (99215) | Complex medical decision making |
| Advanced imaging | Diagnosis supporting need, prior conservative tx |
| DME | Medical necessity letter, diagnosis |
| Physical therapy | Functional limitations, goals |
| Home health | Homebound status, skilled need |

### Bundling Rules

**Services typically bundled:**
- E&M and minor procedures same day
- Lab handling fees into lab tests
- Supplies into procedures
- Pre-op and post-op visits into surgical global period

### Frequency Limitations

| Service | Typical Limit |
|---------|--------------|
| Annual wellness visit | Once per calendar year |
| Colonoscopy (screening) | Every 10 years |
| Mammogram (screening) | Annual or biennial |
| Bone density (DEXA) | Every 2 years |
| Diabetic eye exam | Annual |
| Flu vaccine | Once per season |

## Related References

- [Code Systems](code-systems.md) - ICD-10, CPT, LOINC codes
- [Terminology](terminology.md) - Abbreviations and terms
- [Validation Rules](validation-rules.md) - Data validation
- [Data Models](data-models.md) - Entity schemas
