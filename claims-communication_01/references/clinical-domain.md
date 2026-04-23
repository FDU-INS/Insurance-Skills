# Clinical Domain Knowledge

_Foundational healthcare knowledge for generating realistic, clinically coherent patient data._

## For Claude

Use this skill as your core medical knowledge base when generating any patient data. This teaches you:

- How diseases present across their severity spectrum
- Which medications are appropriate for which conditions
- What laboratory abnormalities accompany specific diagnoses
- How to ensure clinical coherence between all patient elements
- How conditions commonly coexist (comorbidity patterns)
- What vital sign patterns match different conditions

You should apply this knowledge to **every patient you generate** to ensure:
- Diagnoses match laboratory findings
- Medications are appropriate for the conditions
- Vital signs reflect disease severity
- Comorbidities are clinically plausible combinations
- Age/gender patterns are realistic

This skill provides patterns for chronic conditions (diabetes, hypertension, heart failure, COPD, CKD), acute conditions (pneumonia, sepsis, MI), medication classes, laboratory interpretation, and clinical workflows.

## Metadata
- **Type**: domain-knowledge
- **Version**: 2.0
- **Format**: Claude-Optimized (v2.0)
- **Author**: PatientSim Clinical Team
- **Tags**: healthcare, clinical, medical-knowledge, baseline, chronic-disease, acute-care
- **Created**: 2025-11-26
- **Updated**: 2025-11-26

## Purpose

This skill provides essential clinical knowledge that enables realistic patient data generation. It serves as the foundation for understanding:

- How diseases present and progress over time
- Which medications are appropriate for which conditions
- What laboratory abnormalities accompany specific diagnoses
- Typical clinical workflows and admission patterns
- How to create clinically coherent patients where all elements align

Use this skill when generating patients to ensure clinical coherence between diagnoses, medications, vital signs, and laboratory results. This is a foundational skill that should inform nearly all patient generation tasks.

## When to Use This Skill

Apply this skill **proactively** for all patient generation. Specific triggers:

**Direct Keywords**:
- Any disease name: "diabetes", "hypertension", "heart failure", "COPD", "sepsis", "pneumonia", "MI"
- Medication names: "metformin", "lisinopril", "insulin", "antibiotics"
- Clinical settings: "ICU", "emergency department", "clinic", "hospital admission"
- Lab abnormalities: "elevated glucose", "high WBC", "abnormal creatinine"

**Clinical Scenarios**:
- "Generate a diabetic patient"
- "Create a patient with heart failure"
- "I need a septic patient in the ED"
- "Make an elderly patient with multiple comorbidities"
- "Generate realistic ICU patients"

**Implicit Indicators**:
- Any request for "realistic" or "clinically accurate" patients
- Requests mentioning age groups (elderly = more comorbidities)
- Requests for specific clinical settings
- When coherence between vitals/labs/meds is needed

**Co-occurring Mentions**:
- Often paired with: scenario templates, FHIR export, training data generation
- Frequently includes: vital signs, laboratory results, medication lists
- May mention: ICD-10 codes, clinical workflows, EHR data

## Domain Knowledge

### Chronic Condition Patterns

#### Type 2 Diabetes Mellitus

Diabetes is a metabolic disorder characterized by chronic hyperglycemia. It's extremely common (prevalence ~10-15% in adults, higher over age 65) and frequently coexists with other conditions.

**Age/Gender Pattern**:
- Onset typically 45-75 years
- Slightly more common in males (55%)
- Prevalence increases with age

**Clinical Presentation Spectrum**:
- **Early/Mild**: Asymptomatic, found on screening, fasting glucose 126-160 mg/dL, HbA1c 6.5-7.5%
- **Moderate**: Some polyuria/polydipsia, glucose 160-250 mg/dL, HbA1c 7.5-9.0%
- **Poorly Controlled**: Clear symptoms, glucose 250-400+ mg/dL, HbA1c 9.0-12%+

**Why this matters for generation**: Don't give a patient with HbA1c 6.8% (well-controlled) symptoms like severe polyuria or a glucose of 350. Match the lab severity to the clinical presentation.

**Laboratory Pattern**:
```
Well-controlled:
  - Fasting glucose: 90-140 mg/dL
  - HbA1c: 6.5-7.5%
  - Usually no ketones

Poorly controlled:
  - Fasting glucose: 200-400 mg/dL
  - HbA1c: 9.0-12%
  - May have ketonuria
  - Often elevated triglycerides
```

**Medication Progression** (choose based on disease severity):
```
Early Stage:
  - Metformin 500-1000mg PO BID (first-line)
  - Diet and exercise counseling

Moderate Stage:
  - Metformin 1000mg PO BID
  - + SGLT2 inhibitor (empagliflozin 10-25mg QD)
  - OR + DPP-4 inhibitor (sitagliptin 100mg QD)

Advanced Stage:
  - Metformin + multiple agents
  - Insulin glargine 20-50 units SubQ QD (basal)
  - Insulin lispro with meals (bolus)
```

**Comorbidity Clustering** (these commonly coexist):
- **Hypertension (I10)**: 60-80% of diabetics have HTN
- **Hyperlipidemia (E78.5)**: Very common, often requires statin
- **Obesity (E66.9)**: Strong association, BMI typically >30
- **Chronic Kidney Disease (N18.3)**: Develops over 10-20 years
- **Coronary Artery Disease (I25.10)**: Increased risk

**Why this matters for generation**: A 68-year-old diabetic patient should probably have hypertension too. If they've had diabetes for 15+ years, consider adding early CKD.

#### Essential Hypertension

Hypertension is sustained elevated blood pressure ≥140/90 mmHg. Extremely common (~30-40% of adults), often asymptomatic, frequently requires multiple medications.

**Age/Gender Pattern**:
- Can occur at any adult age
- More common with increasing age
- Equal gender distribution overall

**Vital Sign Patterns**:
```
Stage 1 HTN:
  - BP: 140-159/90-99 mmHg
  - Usually asymptomatic

Stage 2 HTN:
  - BP: ≥160/100 mmHg
  - May have headaches if severe

Hypertensive Urgency:
  - BP: ≥180/110 mmHg
  - No organ damage (yet)

Hypertensive Emergency:
  - BP: ≥180/120 mmHg
  - With organ damage (encephalopathy, MI, stroke)
```

**Medication Selection Logic**:
```python
# Start with 1-2 agents based on BP elevation
if bp_systolic >= 160 or bp_diastolic >= 100:
    # Stage 2: Start with 2 agents
    agents = [
        "Lisinopril 10mg PO QD",  # ACE inhibitor
        "Amlodipine 5mg PO QD"    # Calcium channel blocker
    ]
elif bp_systolic >= 140 or bp_diastolic >= 90:
    # Stage 1: Start with 1 agent
    agents = ["Lisinopril 10mg PO QD"]

# Additional considerations
if patient_has_diabetes or patient_has_ckd:
    # Prefer ACE inhibitor or ARB (renoprotective)
    use_ace_or_arb = True

if patient_has_heart_failure:
    # Add beta-blocker and diuretic
    agents.append("Carvedilol 6.25mg PO BID")
    agents.append("Furosemide 20mg PO QD")
```

**Common Comorbidities**:
- **Type 2 Diabetes**: Very common pairing
- **Hyperlipidemia**: Often requires statin therapy
- **Coronary Artery Disease**: HTN is major risk factor
- **Chronic Kidney Disease**: Both cause and consequence

**Why this matters for generation**: A patient with BP 165/95 should be on at least 2 antihypertensives, not just one. If they also have diabetes, make sure one is an ACE inhibitor or ARB.

#### Coronary Artery Disease

CAD is atherosclerotic narrowing of coronary arteries. Common in adults >55, especially with risk factors (smoking, diabetes, hypertension, hyperlipidemia).

**Presentation Spectrum**:
- **Stable Angina**: Exertional chest pain, predictable, relieved by rest/nitro
- **Unstable Angina**: Rest pain, changing pattern (ACS)
- **Silent Ischemia**: No symptoms despite CAD (common in diabetics)

**Laboratory/Diagnostic Patterns**:
```
Stable CAD (not acute):
  - Troponin: Normal (<0.04 ng/mL)
  - Total cholesterol: Often elevated (200-300 mg/dL)
  - LDL: Often high (>130 mg/dL)
  - HDL: Often low (<40 mg/dL in men)

Acute MI (contrast):
  - Troponin: Elevated and rising (>0.04, peaks 12-24hr)
  - CK-MB: Elevated
```

**Standard Medical Regimen**:
```
"DAPT + Statin + BB + ACE":
  - Aspirin 81mg PO QD (antiplatelet)
  - Atorvastatin 40-80mg PO QHS (high-intensity statin)
  - Metoprolol 50mg PO BID (beta-blocker)
  - Lisinopril 10mg PO QD (ACE inhibitor)
  - Nitroglycerin 0.4mg SL PRN chest pain
```

**Why this matters for generation**: A patient with CAD diagnosis should be on most/all of these medications unless there's a contraindication. Don't forget the aspirin and statin - these are core therapy.

#### Heart Failure

Heart failure is impaired cardiac output leading to fluid overload and poor perfusion. Increasing prevalence with aging population.

**Clinical Presentation by NYHA Class**:
```
Class I (Asymptomatic):
  - No symptoms, but EF reduced on echo
  - BNP: 100-300 pg/mL
  - On standard meds

Class II (Mild):
  - Symptoms with moderate exertion (walking 2 blocks)
  - Mild peripheral edema
  - BNP: 300-500 pg/mL

Class III (Moderate):
  - Symptoms with minimal exertion (walking one block)
  - Dyspnea on exertion, orthopnea
  - Moderate edema
  - BNP: 500-1000 pg/mL

Class IV (Severe):
  - Symptoms at rest
  - Severe dyspnea, significant edema
  - BNP: >1000 pg/mL
  - May need hospital admission
```

**Vital Sign Patterns**:
```
Compensated (stable):
  - HR: 70-85 bpm (well-controlled)
  - BP: Normal or slightly low
  - SpO2: 94-98%

Decompensated (exacerbation):
  - HR: 90-110 bpm (tachycardia)
  - BP: Variable (may drop if severe)
  - SpO2: 88-93% (hypoxia)
  - RR: 22-28 (tachypnea)
```

**Guideline-Directed Medical Therapy**:
```
Core 4 medications:
  1. ACE inhibitor: Lisinopril 10-40mg PO QD
  2. Beta-blocker: Carvedilol 6.25-25mg PO BID
  3. Diuretic: Furosemide 20-80mg PO QD-BID
  4. Aldosterone antagonist: Spironolactone 25mg PO QD

Additional:
  - ARB if ACE-intolerant: Losartan 50-100mg QD
  - Digoxin: If AFib present
  - SGLT2i: Empagliflozin (newer, improves outcomes)
```

**Why this matters for generation**: Match the medication intensity and BNP level to the NYHA class. A Class IV patient should have higher doses and possibly all 4 core meds.

#### Chronic Obstructive Pulmonary Disease

COPD is progressive airflow limitation, typically from smoking. Common in adults >60 with smoking history.

**Severity Staging (GOLD criteria)**:
```
Mild (GOLD 1):
  - FEV1 ≥80% predicted
  - Minimal symptoms
  - Short-acting bronchodilator PRN

Moderate (GOLD 2):
  - FEV1 50-79% predicted
  - Exertional dyspnea
  - Long-acting bronchodilator + PRN

Severe (GOLD 3):
  - FEV1 30-49% predicted
  - Dyspnea with minimal exertion
  - Multiple inhalers + possible oxygen

Very Severe (GOLD 4):
  - FEV1 <30% predicted
  - Severe dyspnea, frequent exacerbations
  - Oxygen-dependent
```

**Vital Sign Patterns**:
```
Stable COPD:
  - SpO2: 88-92% (chronic hypoxia, this is normal for them!)
  - RR: 16-22 /min
  - May have pursed-lip breathing

COPD Exacerbation:
  - SpO2: <88% (worse than baseline)
  - RR: 24-30 /min (tachypnea)
  - Increased work of breathing
  - Productive cough, wheezing
```

**Medication Regimen by Severity**:
```
Mild:
  - Albuterol inhaler PRN

Moderate:
  - Tiotropium 18mcg inhaled QD (LAMA)
  - Albuterol PRN

Severe:
  - Tiotropium + Fluticasone/Salmeterol inhaled BID (ICS/LABA)
  - Albuterol PRN
  - Oxygen 2L NC continuous if SpO2 <88%

Exacerbation:
  - Add: Prednisone 40mg PO QD x 5 days
  - Add: Azithromycin 500mg PO QD x 5 days (if bacterial)
```

**Why this matters for generation**: Don't give a stable COPD patient SpO2 of 98% - they chronically run 88-92%. If SpO2 is <88%, they should be on oxygen.

#### Chronic Kidney Disease

CKD is progressive kidney dysfunction, commonly from diabetes or hypertension. Staged by eGFR.

**CKD Staging**:
```
Stage 3a (N18.3):
  - eGFR: 45-59 mL/min
  - Creatinine: ~1.5-2.0 mg/dL
  - Usually asymptomatic
  - Early intervention critical

Stage 3b (N18.3):
  - eGFR: 30-44 mL/min
  - Creatinine: ~2.0-3.0 mg/dL
  - May have fatigue, mild anemia

Stage 4 (N18.4):
  - eGFR: 15-29 mL/min
  - Creatinine: ~3.0-5.0 mg/dL
  - Anemia, hyperkalemia, acidosis
  - Pre-dialysis planning

Stage 5 (N18.5):
  - eGFR: <15 mL/min
  - Creatinine: >5.0 mg/dL
  - Uremia, volume overload
  - Needs dialysis
```

**Laboratory Evolution**:
```
Early CKD (Stage 3):
  - Creatinine: 1.5-2.5 mg/dL (stable)
  - BUN: 25-40 mg/dL
  - Potassium: Normal to high-normal
  - Hemoglobin: Normal to slightly low

Advanced CKD (Stage 4-5):
  - Creatinine: >3.0 mg/dL
  - BUN: 50-100 mg/dL
  - Potassium: 5.0-6.0 mEq/L (hyperkalemia)
  - Hemoglobin: 9-11 g/dL (anemia from low EPO)
  - Phosphorus: Elevated
  - Calcium: Low
```

**Medication Management**:
```
Renoprotective:
  - ACE inhibitor: Lisinopril 10-20mg QD (slows progression)
  - OR ARB if ACE-intolerant

Complications:
  - Anemia: Epoetin alfa (EPO) if Hgb <10
  - Hyperkalemia: Low-potassium diet, patiromer
  - High phosphate: Calcium carbonate 500mg with meals

AVOID:
  - NSAIDs (nephrotoxic)
  - Metformin if eGFR <30
  - Gadolinium contrast
```

**Why this matters for generation**: If a patient has CKD Stage 4, they should have anemia and possibly high potassium. Adjust medication doses for renal function.

### Acute Condition Patterns

#### Community-Acquired Pneumonia

Pneumonia is lower respiratory tract infection, common cause of hospitalization.

**Severity Assessment (CURB-65)**:
```
Low Risk (0-1 points):
  - Outpatient treatment
  - Oral antibiotics

Moderate Risk (2 points):
  - Consider hospitalization
  - IV antibiotics if admitted

High Risk (3-5 points):
  - Hospitalize, possibly ICU
  - IV antibiotics, oxygen

Points for:
  - Confusion
  - Uremia (BUN >20)
  - Respiratory rate ≥30
  - Blood pressure <90/60
  - Age ≥65
```

**Clinical Presentation**:
```
Typical Presentation:
  - Fever: 101-104°F
  - Productive cough (purulent sputum)
  - Pleuritic chest pain
  - Tachypnea: RR 24-30
  - Hypoxia: SpO2 85-92%

Elderly/Atypical:
  - May have low-grade fever or no fever
  - Confusion is prominent
  - Tachypnea out of proportion
```

**Laboratory Pattern**:
```
Bacterial Pneumonia:
  - WBC: 15-25 x10^3/uL (leukocytosis)
  - Neutrophil predominance
  - CRP: 100-300 mg/L
  - Procalcitonin: >0.5 (suggests bacterial)

Viral Pneumonia:
  - WBC: Normal to mildly elevated
  - Lymphocyte predominance
  - Procalcitonin: Usually <0.25
```

**Antibiotic Selection**:
```
Outpatient (mild):
  - Amoxicillin-clavulanate 875mg PO BID
  - + Azithromycin 500mg PO QD x 5 days
  - OR Doxycycline 100mg PO BID

Inpatient (moderate-severe):
  - Ceftriaxone 1-2g IV Q24H
  - + Azithromycin 500mg IV/PO QD
  - Duration: 5-7 days typical
```

**Why this matters for generation**: Match antibiotic route to severity. Outpatient = oral, inpatient = IV. High WBC and high CRP suggest bacterial (needs antibiotics).

#### Sepsis and Septic Shock

Sepsis is dysregulated host response to infection causing organ dysfunction. Life-threatening, requires rapid intervention.

**Sepsis Spectrum**:
```
Infection (not sepsis yet):
  - Localized infection
  - Mild vital sign changes
  - WBC elevated
  - Lactate normal

Sepsis:
  - Infection + organ dysfunction
  - qSOFA ≥2 (altered mental status, SBP ≤100, RR ≥22)
  - Lactate: 2-4 mmol/L
  - Creatinine rising (AKI)

Septic Shock:
  - Sepsis + persistent hypotension
  - SBP <90 despite fluids
  - Lactate: >4 mmol/L
  - Requires vasopressors
  - High mortality (30-40%)
```

**Vital Sign Evolution**:
```
Early Sepsis:
  - Temp: 101-104°F (or <96°F)
  - HR: 110-130 bpm
  - RR: 24-28 /min
  - BP: 95-110/55-65 mmHg
  - SpO2: 90-94%

Septic Shock:
  - Temp: May be normal/low
  - HR: 120-140 bpm (or low if severe)
  - RR: 28-35 /min
  - BP: 70-90/40-55 mmHg
  - SpO2: 85-90%
```

**Laboratory Cascade**:
```
Hour 0 (Initial):
  - WBC: 15-30 x10^3/uL (or <4 if severe)
  - Lactate: 2-6 mmol/L
  - Creatinine: Elevated above baseline
  - Platelets: May be dropping

Hour 3-6 (Worsening):
  - Lactate: Rising or not clearing
  - Creatinine: Continues to rise
  - Bilirubin: Rising (liver dysfunction)
  - Coagulopathy developing

Hour 12-24 (Improving if treated):
  - Lactate: Trending down
  - Organ function stabilizing
```

**Sepsis Bundle (Hour-1)**:
```
Must complete within 1 hour:
  1. Measure lactate
  2. Obtain blood cultures BEFORE antibiotics
  3. Administer broad-spectrum antibiotics
  4. Begin rapid IV fluid resuscitation (30 mL/kg)

Antibiotic Regimen:
  - Ceftriaxone 2g IV Q24H + Vancomycin 1.5g IV Q12H
  - OR Piperacillin-tazobactam 4.5g IV Q6H
  - Adjust based on source:
    - Abdominal: Add metronidazole
    - Urosepsis: May use single agent

Vasopressors (if shock):
  - Norepinephrine 0.1-0.5 mcg/kg/min
  - Target MAP ≥65 mmHg
```

**Why this matters for generation**: Sepsis requires time-critical actions. If generating septic patient, include timeline showing when antibiotics started, lactate measurements, etc. Don't give septic shock patient a lactate of 1.5 mmol/L - should be >4.

#### Acute Myocardial Infarction

MI is myocardial necrosis from coronary occlusion. Medical emergency requiring rapid reperfusion.

**MI Types**:
```
STEMI (ST-Elevation MI):
  - Complete coronary occlusion
  - ST elevation on ECG
  - High troponin
  - Needs immediate cath lab (PCI)

NSTEMI (Non-ST-Elevation MI):
  - Partial occlusion or demand ischemia
  - No ST elevation (but may have other changes)
  - Elevated troponin
  - Urgent cath (within 24-72hr)
```

**Clinical Presentation**:
```
Typical:
  - Substernal chest pressure/pain
  - Radiates to left arm, jaw, back
  - Diaphoresis, nausea
  - Dyspnea
  - Anxiety ("sense of doom")

Atypical (elderly, diabetics, women):
  - Dyspnea without chest pain
  - Epigastric discomfort
  - Fatigue, weakness
  - May be painless
```

**Cardiac Biomarker Pattern**:
```
Acute MI:
  - Troponin I:
    - Initial: May be normal if very early
    - 3-6hr: Rising above 0.04 ng/mL
    - 12-24hr: Peak (can be 5-50+ ng/mL)
    - 48-72hr: Still elevated, declining

  - CK-MB: Similar pattern but less sensitive
  - Myoglobin: Rises early but not specific

Not MI (other causes of troponin elevation):
  - Heart failure, myocarditis, sepsis
  - Usually troponin <1 ng/mL
  - Doesn't have rising-falling pattern
```

**STEMI Treatment Timeline**:
```
Time 0 (Presentation):
  - 12-lead ECG within 10 minutes
  - Aspirin 325mg chewed immediately
  - Oxygen if SpO2 <90%

Time 0-10min:
  - Clopidogrel 600mg or ticagrelor 180mg loading dose
  - Nitroglycerin 0.4mg SL (if BP adequate)
  - Morphine 2-4mg IV for pain
  - Heparin or enoxaparin

Time <90min (Goal):
  - Door-to-balloon time
  - Cardiac catheterization with PCI
  - OR thrombolytics if PCI not available

Medications to Continue:
  - Aspirin 81mg PO QD (lifelong)
  - Clopidogrel 75mg PO QD (1 year minimum)
  - High-intensity statin: Atorvastatin 80mg PO QD
  - Beta-blocker: Metoprolol 50mg PO BID
  - ACE inhibitor: Lisinopril 10mg PO QD
```

**Why this matters for generation**: If generating MI patient, include the timeline showing when aspirin/cath occurred. Troponin should show the characteristic rise-and-fall pattern over hours.

### Medication Class Patterns

#### Antihypertensive Medication Selection

**Drug Class Recognition Patterns**:
```
ACE Inhibitors (end in -pril):
  - Lisinopril, enalapril, ramipril
  - Mechanism: Block angiotensin II formation
  - Side effects: Dry cough (10-15%), hyperkalemia
  - Contraindications: Pregnancy, bilateral renal artery stenosis
  - Dose ranges: Lisinopril 5-40mg QD

ARBs (end in -sartan):
  - Losartan, valsartan, irbesartan
  - Mechanism: Block angiotensin II receptor
  - No cough (alternative to ACE-I)
  - Dose ranges: Losartan 25-100mg QD

Calcium Channel Blockers (end in -dipine for dihydropyridines):
  - Amlodipine, nifedipine
  - Mechanism: Vasodilation
  - Side effects: Peripheral edema, flushing
  - Dose ranges: Amlodipine 2.5-10mg QD

Beta-Blockers (end in -olol):
  - Metoprolol, carvedilol, atenolol
  - Mechanism: Decrease HR and contractility
  - Contraindications: Asthma, severe bradycardia
  - Dose ranges: Metoprolol 25-200mg BID

Diuretics:
  - Thiazide: Hydrochlorothiazide 12.5-25mg QD
  - Loop: Furosemide 20-80mg QD-BID
  - Potassium-sparing: Spironolactone 25-50mg QD
```

**Selection Algorithm**:
```python
# Choose based on comorbidities
if patient_has_diabetes or patient_has_ckd:
    first_line = "ACE inhibitor or ARB"  # Renoprotective

if patient_has_heart_failure:
    required = ["ACE inhibitor", "Beta-blocker", "Diuretic"]

if patient_has_cad:
    required = ["Beta-blocker", "ACE inhibitor"]

if patient_is_black and no_diabetes_or_ckd:
    first_line = "Calcium channel blocker or thiazide"

if bp_very_high (stage 2):
    use_combination = True  # Start with 2 agents
```

**Why this matters for generation**: Don't randomly pick antihypertensives. If patient has diabetes + HTN, they should be on an ACE inhibitor or ARB, not just any BP med.

#### Antidiabetic Medication Patterns

**Treatment Intensification Ladder**:
```
Step 1 (HbA1c 6.5-7.5%):
  - Metformin 500-1000mg PO BID
  - Lifestyle modifications

Step 2 (HbA1c 7.5-9.0%):
  - Metformin (continued)
  + SGLT2 inhibitor: Empagliflozin 10-25mg QD
  OR + GLP-1 agonist: Semaglutide (if weight loss goal)
  OR + DPP-4 inhibitor: Sitagliptin 100mg QD

Step 3 (HbA1c >9.0% or symptomatic):
  - Metformin + oral agent
  + Basal insulin: Glargine 10-20 units SubQ QHS
  - Titrate based on fasting glucose

Step 4 (Very poor control):
  - Basal-bolus insulin regimen
  - Glargine 30-50 units QD
  + Lispro 8-15 units with each meal
  - May continue metformin
```

**Drug Class Characteristics**:
```
Metformin:
  - First-line for all (unless contraindicated)
  - Contraindicated if eGFR <30
  - Side effects: GI upset, rare lactic acidosis

SGLT2 Inhibitors (-gliflozin):
  - Cardiovascular benefits
  - Weight loss effect
  - Side effects: UTI, genital infections
  - Contraindicated if eGFR <30-45 (varies by drug)

Sulfonylureas (glipizide, glyburide):
  - Older agents, less used now
  - Risk: Hypoglycemia, weight gain
  - Cheap (may use if cost is concern)

Insulin:
  - Required for Type 1, often needed in Type 2
  - Basal (glargine, detemir): Once daily, smooth coverage
  - Bolus (lispro, aspart): With meals, rapid
```

**Why this matters for generation**: A patient with HbA1c 11% shouldn't be on metformin monotherapy - they need insulin. Match medication intensity to HbA1c level.

#### Antibiotic Selection Patterns

**Common Infection-Antibiotic Pairings**:
```
Community-Acquired Pneumonia:
  - Outpatient: Amoxicillin-clavulanate + azithromycin
  - Inpatient: Ceftriaxone 1-2g IV Q24H + azithromycin
  - Duration: 5-7 days

Urinary Tract Infection:
  - Uncomplicated: Nitrofurantoin 100mg PO BID x 5 days
  - Complicated: Ciprofloxacin 500mg PO BID x 7 days
  - Pyelonephritis: Ceftriaxone IV x 7-14 days

Skin/Soft Tissue:
  - Cellulitis: Cephalexin 500mg PO QID x 7 days
  - MRSA suspected: Doxycycline or TMP-SMX
  - Abscess: Incision/drainage + antibiotics

Sepsis (unknown source):
  - Broad-spectrum:
    - Ceftriaxone 2g IV Q24H + Vancomycin 1.5g IV Q12H
    - OR Piperacillin-tazobactam 4.5g IV Q6H
  - Adjust when cultures/sensitivities available
  - Duration: 7-14 days typically

Intra-Abdominal:
  - Add anaerobic coverage: Metronidazole
  - OR use combination with anaerobic coverage
```

**Antibiotic Naming Patterns**:
```
Cephalosporins (generation):
  - 1st gen: Cephalexin (oral), cefazolin (IV) - Gram+ focus
  - 3rd gen: Ceftriaxone, cefotaxime - Broad, including Gram-
  - 4th gen: Cefepime - Anti-pseudomonal

Fluoroquinolones (end in -floxacin):
  - Ciprofloxacin, levofloxacin
  - Broad spectrum, good for UTI, pneumonia
  - Side effects: Tendon rupture, QT prolongation

Macrolides (end in -thromycin):
  - Azithromycin, erythromycin
  - Atypical coverage (Mycoplasma, Legionella)
  - Good for respiratory infections
```

**Why this matters for generation**: Match antibiotic route to severity. Oral = outpatient/mild, IV = inpatient/severe. Use appropriate duration (don't give 20 days for simple UTI).

### Laboratory Interpretation Patterns

#### Complete Blood Count (CBC)

**Normal Values and Interpretation**:
```
White Blood Cell Count (WBC):
  - Normal: 4-11 x10^3/uL
  - Leukocytosis (elevated): >11, suggests infection/inflammation
    - Mild: 11-15 (minor infection, stress)
    - Moderate: 15-25 (bacterial infection, pneumonia)
    - Severe: >25 (sepsis, leukemia)
  - Leukopenia (low): <4, suggests viral infection, immunosuppression

Hemoglobin (Hgb):
  - Normal: Men 13.5-17.5 g/dL, Women 12-16 g/dL
  - Anemia: Below normal
    - Mild: 10-12 (asymptomatic often)
    - Moderate: 8-10 (fatigue, pallor)
    - Severe: <8 (dyspnea, tachycardia, may need transfusion)

Platelets:
  - Normal: 150-400 x10^3/uL
  - Thrombocytopenia: <150
    - Mild: 100-150 (no symptoms)
    - Moderate: 50-100 (bruising risk)
    - Severe: <50 (spontaneous bleeding risk)
```

**Disease-Specific CBC Patterns**:
```
Bacterial Infection:
  - WBC: 15-25 (leukocytosis)
  - Neutrophil predominance (left shift)

Viral Infection:
  - WBC: Normal to mildly elevated
  - Lymphocyte predominance

Anemia of Chronic Disease (CKD, cancer):
  - Hgb: 9-11 g/dL
  - MCV: Normal (normocytic)

Iron Deficiency Anemia:
  - Hgb: <12 (women), <13 (men)
  - MCV: <80 (microcytic)
  - Seen in: GI bleeding, menorrhagia

Chronic Kidney Disease:
  - Hgb: 9-11 g/dL (from low EPO)
  - Normocytic anemia
```

**Why this matters for generation**: A patient with pneumonia should have WBC 15-25 with neutrophil predominance, not a normal WBC of 7.

#### Basic Metabolic Panel (BMP)

**Renal Function Assessment**:
```
Creatinine:
  - Normal: 0.7-1.3 mg/dL
  - Elevated: Suggests kidney dysfunction
    - Mild elevation: 1.3-2.0 (early CKD or mild AKI)
    - Moderate: 2.0-4.0 (CKD Stage 3-4)
    - Severe: >4.0 (CKD Stage 4-5 or severe AKI)

BUN (Blood Urea Nitrogen):
  - Normal: 7-20 mg/dL
  - Elevated: >20
    - BUN/Creatinine ratio:
      - >20: Prerenal (dehydration, heart failure)
      - 10-20: Intrinsic renal disease
      - <10: Liver disease

eGFR (calculated):
  - Normal: >60 mL/min
  - CKD Stage 3a: 45-59
  - CKD Stage 3b: 30-44
  - CKD Stage 4: 15-29
  - CKD Stage 5: <15 (dialysis needed)
```

**Electrolyte Patterns**:
```
Sodium:
  - Normal: 136-145 mEq/L
  - Hyponatremia: <136 (heart failure, SIADH)
  - Hypernatremia: >145 (dehydration)

Potassium:
  - Normal: 3.5-5.0 mEq/L
  - Hypokalemia: <3.5 (diuretics, GI losses)
  - Hyperkalemia: >5.0 (CKD, ACE inhibitors)
    - Mild: 5.0-6.0
    - Severe: >6.0 (cardiac risk)

Glucose:
  - Fasting normal: 70-100 mg/dL
  - Prediabetes: 100-125
  - Diabetes: ≥126
```

**Clinical Patterns**:
```
Acute Kidney Injury (AKI):
  - Creatinine: Rising (>0.3 above baseline)
  - BUN: Rising
  - Potassium: May be elevated
  - Seen in: Sepsis, dehydration, nephrotoxic drugs

Heart Failure Decompensation:
  - BUN: Elevated (prerenal)
  - Creatinine: May be mildly elevated
  - Sodium: Low (dilutional hyponatremia)

Diabetic Ketoacidosis (DKA):
  - Glucose: >250 mg/dL
  - Sodium: Low (artifact)
  - Potassium: Variable (total body depleted)
  - Bicarbonate: <18 (metabolic acidosis)
```

**Why this matters for generation**: A septic patient should have rising creatinine (AKI), not normal creatinine. Heart failure patients often have mild hyponatremia.

#### Cardiac and Inflammatory Markers

**Troponin (Cardiac Injury)**:
```
Normal: <0.04 ng/mL

Acute MI:
  - 0-3hr: May still be normal
  - 3-6hr: Rising above 0.04
  - 12-24hr: Peak (can be 5-50+)
  - Days: Slowly declining

Elevated but not MI:
  - <1.0: Heart failure, myocarditis, sepsis
  - Doesn't show rising-falling pattern
```

**BNP (Heart Failure Marker)**:
```
Normal: <100 pg/mL

Heart Failure:
  - 100-300: Mild (NYHA I-II)
  - 300-500: Moderate (NYHA II-III)
  - 500-1000: Severe (NYHA III)
  - >1000: Very severe (NYHA IV), poor prognosis

Not heart failure:
  - Slightly elevated: Renal dysfunction, PE, COPD
```

**Inflammatory Markers**:
```
C-Reactive Protein (CRP):
  - Normal: <10 mg/L
  - Mild inflammation: 10-50 (viral illness)
  - Moderate-severe infection: 100-300 (bacterial pneumonia, sepsis)

Procalcitonin (PCT):
  - Normal: <0.1 ng/mL
  - Viral: Typically <0.25
  - Bacterial: >0.5 (suggests bacterial infection)
  - Sepsis: >2.0

Lactate:
  - Normal: 0.5-2.0 mmol/L
  - Sepsis: 2-4 (elevated, concerning)
  - Septic shock: >4 (severe, high mortality)
```

**Why this matters for generation**: Don't give a heart failure patient BNP of 50 - should be >100. Bacterial pneumonia should have CRP >100, viral might be 30-50.

### Clinical Workflow Patterns

#### Emergency Department Admission Process

**ED Sepsis Timeline** (use for septic patient generation):
```
Hour 0 (Triage):
  - Vitals: T 103°F, HR 125, BP 92/55, RR 28, SpO2 90%
  - ESI Level 2 (high acuity)
  - Rapid triage to treatment area

Hour 0-1 (Initial Management):
  - Place 2 large-bore IVs
  - Draw: Blood cultures x2, lactate, CBC, BMP, CRP
  - Start IV fluids: 30 mL/kg crystalloid (NS 1-2L bolus)
  - Administer antibiotics: Ceftriaxone 2g IV + Vancomycin 1.5g IV
  - Oxygen: 4L NC for SpO2 <94%
  - Initial lactate: 4.2 mmol/L

Hour 1-3 (Monitoring):
  - Repeat vitals q30min
  - Monitor urine output
  - Repeat lactate at hour 3: 3.1 mmol/L (improving)

Hour 3-6 (Disposition Decision):
  - Improving: BP 102/62, HR 110, RR 24
  - Lactate trending down
  - Decision: Admit to medical floor
  - Continue IV antibiotics, fluids
  - Source control if needed
```

**ED Chest Pain Workup** (for MI patient):
```
Hour 0 (Arrival):
  - 12-lead ECG within 10 minutes
  - Vitals, IV access
  - Aspirin 325mg chewed

Hour 0-1 (If STEMI on ECG):
  - Activate cath lab
  - Antiplatelet: Ticagrelor 180mg
  - Anticoagulation: Heparin bolus
  - Pain control: Morphine if needed
  - Door-to-balloon goal: <90min

Hour 0-3 (If NSTEMI or UA):
  - Serial troponins: Initial, 3hr, 6hr
  - Troponin I: 0.08 → 0.52 → 1.21 (rising = MI)
  - Risk stratification (HEART score)
  - Admit for urgent cath within 24-72hr
```

#### Inpatient Hospital Admission

**Day-by-Day Pneumonia Admission**:
```
Day 1 (Admission):
  - ED transfer to medical floor
  - Admission vitals: T 101.8°F, HR 105, RR 26, SpO2 91% on 2L
  - Orders:
    - Ceftriaxone 2g IV Q24H
    - Azithromycin 500mg IV QD
    - Oxygen to keep SpO2 >92%
    - NS 100 mL/hr maintenance
    - Blood cultures, sputum culture
    - Chest X-ray: Right lower lobe infiltrate
  - Labs: WBC 18.2, CRP 185

Day 2:
  - Vitals improving: T 100.2°F, HR 95, RR 22, SpO2 93% on 2L
  - Culture results: Streptococcus pneumoniae (sensitive)
  - Continue antibiotics
  - Diet advanced to regular

Day 3:
  - Afebrile: T 98.6°F
  - Oxygen weaned to room air, SpO2 95%
  - Transition antibiotics to oral:
    - Amoxicillin-clavulanate 875mg PO BID
    - Azithromycin 500mg PO QD
  - Discharge planning

Day 4 (Discharge):
  - Off oxygen, vitals stable
  - Complete antibiotics at home (total 7 days)
  - Discharge instructions
  - Follow-up in 1-2 weeks
```

**ICU Admission for Septic Shock**:
```
Day 1:
  - Transfer from ED, septic shock
  - Vitals: BP 82/48 on norepi 0.3 mcg/kg/min, HR 128
  - Mechanical ventilation
  - Central line, arterial line
  - Fluids ongoing, vasopressor titration
  - Lactate 6.8 → 4.2 (improving)

Day 2-3:
  - Vasopressor weaning
  - Lactate normalizing
  - Cultures growing E. coli (tailor antibiotics)

Day 4-5:
  - Off vasopressors
  - Extubated
  - Transfer to floor when stable
```

**Why this matters for generation**: Use realistic timelines. Pneumonia typically 3-5 day stay. Septic shock might be ICU for 5-7 days before floor transfer.

### Clinical Coherence Patterns

**Diagnosis-Lab Coherence Rules**:
```python
# Before finalizing patient, check coherence:

if diagnosis == "Diabetes (E11.9)":
    assert glucose > 126 or HbA1c >= 6.5
    # Can't have diabetes without hyperglycemia

if diagnosis == "Pneumonia (J18.9)":
    assert WBC > 11 or CRP > 50
    assert SpO2 < 95 or chest_xray_has_infiltrate
    # Pneumonia should have infection markers

if diagnosis == "Heart Failure (I50.9)":
    assert BNP > 100
    assert has_dyspnea_or_edema
    # HF requires elevated BNP and symptoms

if diagnosis == "Acute MI (I21.x)":
    assert troponin > 0.04
    assert ECG_changes or clinical_symptoms
    # MI requires biomarker elevation

if diagnosis == "Sepsis (A41.9)":
    assert lactate >= 2.0
    assert has_infection_source
    assert qSOFA >= 2  # organ dysfunction
```

**Medication-Diagnosis Coherence**:
```python
# Medications should match diagnoses

if patient.has_diagnosis("Diabetes"):
    assert patient.has_medication("metformin" or "insulin")

if patient.has_diagnosis("Hypertension"):
    assert len(patient.antihypertensives) >= 1
    if patient.bp_systolic > 160:
        assert len(patient.antihypertensives) >= 2

if patient.has_diagnosis("CAD"):
    assert patient.has_medication("aspirin")
    assert patient.has_medication("statin")
    # Core CAD meds are non-optional

if patient.has_diagnosis("Heart Failure"):
    assert patient.has_medication("ACE-I or ARB")
    assert patient.has_medication("beta-blocker")
    assert patient.has_medication("diuretic")
    # GDMT is standard of care
```

**Vital Sign-Disease Coherence**:
```python
# Vitals should match disease severity

if diagnosis == "Pneumonia":
    if severity == "mild":
        assert temp in [100-102], SpO2 in [92-95]
    elif severity == "severe":
        assert temp in [102-104], SpO2 in [85-91]
        assert RR >= 24

if diagnosis == "Sepsis":
    assert temp > 100.4 or temp < 96
    assert HR > 90
    assert RR > 22 or SpO2 < 94

if diagnosis == "COPD Exacerbation":
    # Stable COPD patients chronically have low SpO2
    if exacerbation:
        assert SpO2 < baseline_SpO2  # Worse than usual
```

**Age-Disease Appropriateness**:
```python
# Certain diseases more common at certain ages

if patient.age < 40:
    # Unlikely to have multiple chronic conditions
    avoid_diagnoses = ["CAD", "Heart Failure", "COPD", "advanced CKD"]

if patient.age in [45, 75]:
    # Typical diabetic age range
    diabetes_probability = 0.15
    hypertension_probability = 0.35

if patient.age > 75:
    # Expect multiple comorbidities
    average_diagnoses = 3-5
    common = ["HTN", "Diabetes", "CKD", "CAD"]
```

## Generation Guidelines

### How to Apply This Knowledge

**When the user says**: "Generate a diabetic patient"

**Claude should**:
1. Choose appropriate age (typically 45-75, peak 60-70)
2. Determine control level (default to moderate control, HbA1c ~7.5-8.5%)
3. Generate matching lab values:
   - Glucose: 150-220 mg/dL
   - HbA1c: 7.5-8.5%
4. Select appropriate medications based on control level:
   - Moderate: Metformin + one additional agent
5. Add likely comorbidities (60-80% should have hypertension)
6. Ensure vital signs are appropriate (may have slightly elevated BP if HTN comorbid)

**When the user says**: "Generate a patient with heart failure"

**Claude should**:
1. Assign NYHA class (default to Class II-III)
2. Generate BNP matching class (Class II = 300-500 pg/mL)
3. Include all guideline-directed medical therapy:
   - ACE inhibitor or ARB
   - Beta-blocker
   - Diuretic
   - Spironolactone
4. Match vital signs to class (Class II-III: mild tachycardia, possible mild hypoxia)
5. Add likely causes (CAD, HTN, diabetes as comorbidities)

**When the user says**: "Generate a septic patient in the ED"

**Claude should**:
1. Choose infection source (default: pneumonia 60%, UTI 20%, abdominal 15%, other 5%)
2. Determine severity (sepsis vs. septic shock)
3. Generate appropriate vital signs:
   - Sepsis: BP 95-110/55-65, HR 110-130, temp 101-104
   - Septic shock: BP 70-90/40-55, HR 120-140, temp variable
4. Include time-sensitive bundles in timeline:
   - Hour 0-1: Blood cultures, antibiotics, fluids
   - Hour 3: Repeat lactate
5. Match labs to severity:
   - Sepsis: Lactate 2-4, WBC 15-25
   - Septic shock: Lactate >4, WBC >25 or <4
6. Choose appropriate antibiotics (broad-spectrum: ceftriaxone + vancomycin)

### Clinical Feature Coherence

**Glucose-HbA1c Relationship**:
- HbA1c reflects 3-month average glucose
- Rough formula: Average glucose ≈ (HbA1c × 28.7) - 46.7
- HbA1c 7.0% → average glucose ~154 mg/dL
- Don't give HbA1c 11% with glucose consistently 140 mg/dL (incoherent)

**Creatinine-eGFR Relationship**:
- Inversely related: Higher creatinine = lower eGFR
- Creatinine 1.5 → eGFR ~50 (CKD Stage 3)
- Creatinine 3.0 → eGFR ~25 (CKD Stage 4)
- Don't give creatinine 4.0 with eGFR 85 (impossible)

**Troponin-ECG-Symptoms Triangle**:
- All three should align for MI diagnosis
- Elevated troponin + chest pain + ECG changes = MI
- Elevated troponin alone (no symptoms, normal ECG) = other cause (HF, sepsis)

**Vital Signs Internal Coherence**:
```python
# Fever should cause compensatory tachycardia
if temp > 100.4:
    expected_HR = baseline_HR + (10 * (temp - 98.6))
    # Each 1°F → ~10 bpm increase

# Hypoxia should cause compensatory tachypnea
if SpO2 < 90:
    assert RR > 20  # Body trying to compensate

# Hypotension should cause compensatory tachycardia
if SBP < 90:
    assert HR > 100  # Unless shock is severe (then may be low)
```

### Medication Selection Logic

```python
# Antihypertensive selection pseudocode
def select_antihypertensives(patient):
    agents = []

    # First-line choice based on comorbidities
    if patient.has_diabetes or patient.has_ckd:
        agents.append("ACE-I or ARB")  # Renoprotective
    elif patient.is_black and not patient.has_diabetes:
        agents.append("CCB or thiazide")  # Per guidelines
    else:
        agents.append("ACE-I or thiazide")

    # Add second agent if BP very high
    if patient.bp_systolic >= 160:
        if "ACE-I" in agents:
            agents.append("CCB or thiazide")
        else:
            agents.append("ACE-I")

    # Add third agent if needed
    if patient.bp_systolic >= 170:
        # Typically need 3 agents for very high BP
        remaining_classes = ["beta-blocker", "alpha-blocker", "vasodilator"]
        agents.append(random.choice(remaining_classes))

    # Special additions
    if patient.has_heart_failure:
        agents.append("beta-blocker")
        agents.append("loop diuretic")

    return agents
```

### Clinical Coherence Checks

Before finalizing a patient, verify:

- [ ] **Diagnosis-Lab Alignment**: Every diagnosis has supporting lab findings
- [ ] **Medication-Diagnosis Match**: Medications are appropriate for listed diagnoses
- [ ] **Vital Signs-Disease Severity**: Vital sign abnormalities match stated severity
- [ ] **Comorbidity Plausibility**: Comorbidities commonly coexist (diabetes + HTN yes, multiple rare diseases no)
- [ ] **Age-Disease Appropriateness**: Diseases fit patient age (no advanced CAD in 25-year-old)
- [ ] **Temporal Consistency**: Timelines make sense (don't start antibiotics before blood cultures)
- [ ] **Medication Dosing**: Doses are within normal ranges and appropriate for indication
- [ ] **Lab Value Relationships**: Related labs are coherent (high HbA1c matches high glucose, etc.)

## Example Requests and Interpretations

### Example 1: Simple Chronic Disease Request

**User says**: "Generate a patient with diabetes"

**Claude interprets**:
- Type: Type 2 diabetes (most common, ~95% of cases)
- Age: 62 years (typical age for T2DM)
- Control level: Moderate (HbA1c ~8.0%, common scenario)
- Duration: Assume 8-10 years (time to develop early complications)

**Key features Claude generates**:
- Demographics: Age 62, male (slightly more common), BMI 32 (obesity common)
- Vital signs: BP 142/88 (hypertension comorbidity), otherwise normal
- Labs:
  - Glucose: 182 mg/dL (fasting, matches HbA1c)
  - HbA1c: 8.1% (moderate control)
  - Creatinine: 1.3 mg/dL (early CKD developing)
  - LDL: 145 mg/dL (dyslipidemia common)
- Diagnosis:
  - E11.9 (Type 2 diabetes mellitus)
  - I10 (Essential hypertension) - 70% comorbid
  - N18.3 (CKD Stage 3) - common complication
- Medications:
  - Metformin 1000mg PO BID
  - Empagliflozin 10mg PO QD (SGLT2i for CV benefit)
  - Lisinopril 20mg PO QD (for HTN and renal protection)
  - Atorvastatin 40mg PO QD (statin for CV risk)

### Example 2: Acute Care Request

**User says**: "Generate a septic patient presenting to the ED"

**Claude interprets**:
- Severity: Sepsis (not septic shock) - default to moderate severity
- Source: Pneumonia (most common source, ~40-50%)
- Age: 72 years (sepsis more common in elderly)
- Setting: Emergency department presentation

**Key features Claude generates**:
- Demographics: Age 72, female
- Vital signs (hour 0):
  - Temperature: 102.8°F (fever)
  - HR: 118 bpm (tachycardia)
  - BP: 96/58 mmHg (hypotension)
  - RR: 26 /min (tachypnea)
  - SpO2: 89% on room air (hypoxia)
- Labs:
  - WBC: 21.5 x10^3/uL (leukocytosis)
  - Lactate: 3.2 mmol/L (elevated, indicates sepsis)
  - Creatinine: 1.8 mg/dL (AKI from sepsis)
  - CRP: 215 mg/L (highly elevated)
- Diagnosis:
  - A41.9 (Sepsis, unspecified organism)
  - J18.9 (Pneumonia, unspecified organism)
  - N17.9 (Acute kidney injury)
- Medications (timeline):
  - Hour 0: Blood cultures drawn
  - Hour 0: Ceftriaxone 2g IV + Vancomycin 1.5g IV (broad-spectrum)
  - Hour 0: Normal saline 2L IV bolus
  - Hour 1: Oxygen 4L NC
  - Hour 3: Repeat lactate 2.4 mmol/L (improving)
- Timeline:
  - Hour 0-1: Sepsis bundle completed
  - Hour 3: Reassessment, improving
  - Hour 6: Admit to medical floor (not ICU - improving)

### Example 3: Severity-Specific Request

**User says**: "Generate a patient with severe heart failure"

**Claude interprets**:
- Severity: NYHA Class III-IV (based on "severe")
- Type: Systolic heart failure (HFrEF, EF <40%)
- Acuity: Decompensated (since described as "severe")
- Setting: Likely hospital admission

**Key features Claude generates**:
- Demographics: Age 68, male
- Vital signs:
  - HR: 102 bpm (tachycardia from poor cardiac output)
  - BP: 108/68 mmHg (lower than normal)
  - RR: 24 /min (dyspnea)
  - SpO2: 90% on 2L NC (hypoxia from pulmonary edema)
  - Weight: 5 kg above dry weight (fluid overload)
- Labs:
  - BNP: 1250 pg/mL (very elevated for NYHA III-IV)
  - Creatinine: 2.1 mg/dL (cardiorenal syndrome)
  - Sodium: 132 mEq/L (dilutional hyponatremia)
  - Hemoglobin: 10.2 g/dL (anemia of chronic disease)
- Diagnosis:
  - I50.23 (Acute on chronic systolic heart failure)
  - I25.10 (CAD - likely cause)
  - N18.3 (CKD Stage 3 - complication)
- Medications:
  - Lisinopril 40mg PO QD (max dose ACE-I)
  - Carvedilol 25mg PO BID (max dose beta-blocker)
  - Furosemide 80mg IV BID (high dose diuretic for decompensation)
  - Spironolactone 25mg PO QD
  - Digoxin 0.125mg PO QD (if also has AFib)

### Example 4: Multiple Comorbidities Request

**User says**: "Generate an elderly patient with multiple chronic conditions"

**Claude interprets**:
- Age: 78 years (elderly)
- Number of conditions: 4-5 (typical for elderly)
- Type: Chronic diseases that commonly coexist
- Setting: Outpatient/clinic visit or hospital admission

**Key features Claude generates**:
- Demographics: Age 78, female
- Vital signs:
  - BP: 148/82 mmHg (Stage 1 HTN, common in elderly)
  - HR: 76 bpm (normal)
  - SpO2: 91% on room air (chronic low from COPD)
- Labs:
  - Glucose: 156 mg/dL, HbA1c: 7.8% (diabetes)
  - Creatinine: 1.6 mg/dL, eGFR: 38 (CKD Stage 3b)
  - Hemoglobin: 10.8 g/dL (anemia from CKD)
  - LDL: 138 mg/dL (dyslipidemia)
- Diagnoses (clustering of common geriatric conditions):
  - E11.9 (Type 2 diabetes mellitus)
  - I10 (Essential hypertension)
  - N18.3 (CKD Stage 3b)
  - J44.1 (COPD with acute exacerbation - has history)
  - I50.9 (Heart failure) - developing
  - E78.5 (Hyperlipidemia)
- Medications (polypharmacy typical in elderly):
  - Metformin 500mg PO BID (reduced dose for CKD)
  - Lisinopril 20mg PO QD (HTN + renal protection)
  - Furosemide 40mg PO QD (HTN + early HF)
  - Tiotropium inhaler QD (COPD)
  - Atorvastatin 40mg PO QD (dyslipidemia)
  - Aspirin 81mg PO QD (CV prevention)
  - Erythropoietin SubQ weekly (anemia from CKD)

**Why this clustering makes sense**: Diabetes → CKD + HTN. Smoking history → COPD. Multiple CV risk factors → heart failure developing. All are highly prevalent in this age group and frequently coexist.

### Example 5: Laboratory-Driven Request

**User says**: "Generate a patient with an elevated troponin"

**Claude interprets**:
- Elevated troponin can mean MI or other causes
- Need to determine: Is this acute MI or alternative diagnosis?
- Default to acute MI (most common teaching scenario)
- Type: NSTEMI (more common than STEMI)

**Key features Claude generates**:
- Demographics: Age 66, male
- Presentation: Chest pain starting 4 hours ago
- Vital signs:
  - BP: 156/92 mmHg (elevated from pain/stress)
  - HR: 95 bpm (slightly elevated)
  - Otherwise normal
- Labs (with temporal pattern):
  - Troponin I initial: 0.08 ng/mL (elevated)
  - Troponin I at 3hr: 0.52 ng/mL (rising)
  - Troponin I at 6hr: 1.18 ng/mL (peak)
  - CK-MB: Elevated
  - BNP: 145 pg/mL (slightly elevated)
- ECG: ST depression in V3-V6 (NSTEMI pattern)
- Diagnosis:
  - I21.4 (NSTEMI)
  - I25.10 (Background CAD)
  - I10 (Hypertension)
  - E78.5 (Hyperlipidemia - risk factor)
- Medications:
  - Aspirin 325mg chewed stat
  - Ticagrelor 180mg loading dose
  - Heparin drip
  - Atorvastatin 80mg PO QD
  - Metoprolol 50mg PO BID
  - Lisinopril 10mg PO QD
- Timeline:
  - Hour 0: Presentation, ECG, aspirin, labs
  - Hour 3: Repeat troponin rising → NSTEMI confirmed
  - Hour 6: Admit to cardiac care unit
  - Day 1-2: Cardiac catheterization scheduled

**Alternative interpretation if user meant non-MI troponin elevation**:
- Diagnosis: I50.9 (Heart failure exacerbation)
- Troponin: 0.28 ng/mL (elevated but not rising pattern)
- BNP: 850 pg/mL (very high, points to HF)
- No chest pain, instead dyspnea and edema

## Related Skills

Complementary skills:
- **skills/patientsim/sepsis-acute-care.md** - Detailed sepsis scenario template using this knowledge
- **skills/patientsim/diabetes-management.md** - Diabetes-specific scenario patterns
- **skills/patientsim/ed-chest-pain.md** - Chest pain evaluation workflow
- **formats/fhir-r4.md** - How to export this data to FHIR
- **formats/hl7v2-adt.md** - How to format ADT messages

## Metadata

- **Type**: domain-knowledge
- **Version**: 2.0
- **Format**: Claude-Optimized (v2.0)
- **Author**: PatientSim Clinical Team
- **Tags**: healthcare, clinical, medical-knowledge, baseline, chronic-disease, acute-care
- **Created**: 2025-11-26
- **Updated**: 2025-11-26

## References

**Clinical Guidelines**:
- American Diabetes Association Standards of Care (2024)
- ACC/AHA Hypertension Guidelines (2017)
- Surviving Sepsis Campaign Guidelines (2021)
- GOLD COPD Guidelines (2024)
- AHA/ACC Heart Failure Guidelines (2022)
- ACCF/AHA STEMI Guidelines (2013)
- Kidney Disease: Improving Global Outcomes (KDIGO) CKD Guidelines (2024)

**Clinical Calculators**:
- CURB-65 (pneumonia severity)
- qSOFA (sepsis screening)
- CHA2DS2-VASc (stroke risk)
- HEART Score (chest pain risk)
- Framingham Risk Score (CV risk)

**Laboratory Reference Ranges**:
- Standard adult reference ranges
- Age and gender adjustments applied
- Critical values noted where applicable

## Dependencies

None - this is a foundational domain knowledge skill that other skills may reference.
