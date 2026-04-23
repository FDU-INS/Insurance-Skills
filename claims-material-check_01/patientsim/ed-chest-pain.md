---
name: ed-chest-pain
description: "Emergency Department chest pain presentations with complete event sequences from symptom onset through disposition. Triggers: chest pain, cardiac, ED, MI, STEMI, NSTEMI, ACS, acute coronary syndrome, troponin, ECG, rule out MI, emergency department"
---

# Emergency Department Chest Pain Cohort - Complete Event Timelines

A cohort template for generating patients presenting to the Emergency Department with chest pain **with complete event sequences from symptom onset through disposition**, covering the spectrum from benign musculoskeletal pain to acute myocardial infarction.

## For Claude

Use this skill when the user requests ED chest pain patients or cardiac workup cohorts. This teaches you how to generate **realistic clinical event sequences** for chest pain presentations across the risk spectrum - from low-risk rule-outs to STEMI requiring emergent intervention.

**When to apply this skill:**
- User mentions chest pain, cardiac presentation, or ED cohorts
- User requests MI, STEMI, NSTEMI, or acute coronary syndrome patients
- User specifies troponin levels, ECG changes, or cardiac workup
- User asks for emergency department or acute care cohorts with event timelines
- User mentions "rule out MI" or cardiac risk stratification
- User needs event sequences for testing clinical decision support or workflow protocols

**Key capabilities this skill provides:**
- How to generate complete event timelines (symptom onset → EMS → ED arrival → diagnostic workup → treatment → disposition)
- How to match ECG findings with troponin levels at specific time points (STEMI vs NSTEMI vs rule-out)
- How to apply HEART score risk stratification throughout the ED course
- How to create time-critical sequences (door-to-balloon <90 min for STEMI, serial troponins 3h apart)
- How to sequence lab orders → results → clinical decisions → treatment interventions
- When to activate cath lab emergently vs admit to cardiology vs discharge
- How to create alert-triggering events (troponin rising, ST elevations appearing)

**Important**: STEMI requires **immediate** cath lab activation (ST elevations ≥1mm in 2 contiguous leads). NSTEMI has elevated troponin but NO ST elevations. Rule-out has negative troponins and normal/non-diagnostic ECG. All cohorts should include **temporal sequences** showing progression of events.

## Metadata
- **Type**: cohort-template
- **Version**: 2.0
- **Author**: PatientSim
- **Tags**: emergency, chest-pain, cardiac, acute-care
- **Updated**: 2025-11-26

## Purpose

This cohort generates realistic ED chest pain presentations, one of the most common and critical emergency department chief complaints. It simulates the diagnostic workup, risk stratification, and disposition decisions for chest pain patients.

The cohort is designed to:
- Model realistic chest pain presentations across the severity spectrum
- Generate appropriate diagnostic workups (ECG, troponin, imaging)
- Simulate risk stratification using clinical decision tools
- Support different outcomes: rule-out, NSTEMI, STEMI, non-cardiac diagnoses
- Include realistic timeline from presentation through disposition

## When to Use This Skill

Apply this skill when the user's request involves:

**Direct Keywords**:
- "chest pain", "chest discomfort", "angina"
- "MI", "myocardial infarction", "heart attack"
- "STEMI", "NSTEMI", "unstable angina"
- "ACS", "acute coronary syndrome"
- "troponin", "cardiac enzymes", "cardiac markers"
- "rule out MI", "cardiac workup", "chest pain workup"
- "ECG", "ST elevation", "ST depression"

**Clinical Cohorts**:
- "Generate an ED chest pain patient"
- "I need a STEMI patient for cath lab"
- "Create a patient with elevated troponin"
- "Generate a low-risk chest pain rule-out"
- "Make a patient with unstable angina"
- "I need an NSTEMI for cardiology admission"

**Implicit Indicators**:
- User mentions emergency department or ED setting
- User specifies cardiac catheterization or PCI
- User mentions "door-to-balloon time" or cath lab activation
- User asks for "time-critical" or "emergency" cardiac cohorts
- User specifies acute chest pain with radiation to arm/jaw

**Co-occurring Mentions**:
- When user mentions chest pain AND ECG changes
- When user mentions chest pain AND cardiac risk factors (smoking, diabetes, HTN)
- When user mentions chest pain AND hypotension (cardiogenic shock)
- When user mentions chest pain AND dyspnea (possible heart failure or PE)

## Trigger Phrases

- chest pain
- myocardial infarction
- MI
- STEMI
- NSTEMI
- acute coronary syndrome
- ACS
- troponin
- ED chest pain
- rule out MI
- cardiac workup

## Dependencies
- healthcare/clinical-domain.md

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| age_range | range | 45-75 | Patient age range (cardiac risk increases with age) |
| cardiac_risk | enum | intermediate | Cardiac risk level: low, intermediate, high |
| final_diagnosis | enum | rule-out | Outcome: rule-out, unstable-angina, nstemi, stemi, non-cardiac |
| has_risk_factors | boolean | true | Whether patient has cardiac risk factors |
| presentation_severity | enum | moderate | Initial severity: mild, moderate, severe |
| geography | string | null | County/tract FIPS for data-driven rates |

## Data Sources (PopulationSim v2.0)

When geography is specified, ED chest pain cohorts use real population data:

### Embedded Data Lookup

```
File: skills/populationsim/data/county/places_county_2024.csv
Relevant columns for cardiac:
  - CHD_CrudePrev: Coronary heart disease prevalence
  - STROKE_CrudePrev: Stroke prevalence
  - BPHIGH_CrudePrev: Hypertension (CAD risk factor)
  - DIABETES_CrudePrev: Diabetes (CAD risk factor)
  - CSMOKING_CrudePrev: Smoking (major CAD risk)
  - HIGHCHOL_CrudePrev: High cholesterol
```

### Data-Driven Risk Stratification

| Risk Factor | PLACES Column | Impact |
|-------------|---------------|--------|
| Baseline CAD | CHD_CrudePrev | Higher → more true ACS |
| Hypertension | BPHIGH_CrudePrev | Comorbidity weighting |
| Diabetes | DIABETES_CrudePrev | Atypical presentations |
| Smoking | CSMOKING_CrudePrev | Risk factor presence |

### Geographic Variation in Outcomes

Areas with higher CHD prevalence have:
- Higher proportion of true-positive chest pain workups
- More STEMI/NSTEMI diagnoses relative to rule-outs
- Higher comorbidity burden in presentations

## Domain Knowledge

### Chest Pain Diagnostic Spectrum

Chest pain exists on a spectrum from benign (musculoskeletal) to immediately life-threatening (STEMI). The critical skill is recognizing where on this spectrum the patient falls.

**Why this matters for generation**: The final diagnosis determines ECG findings, troponin levels, symptoms severity, vital signs, and the entire clinical timeline. These elements must be coherent.

**Rule-Out / Low Risk**:
- ECG: Normal sinus rhythm, no ST changes
- Troponin: Negative at 0h and 3h (<0.04 ng/mL)
- Symptoms: Atypical (sharp, positional, reproducible with palpation)
- Vitals: Normal
- Disposition: Discharge with outpatient follow-up

**Unstable Angina**:
- ECG: May show ST depressions or T wave changes
- Troponin: NEGATIVE (by definition)
- Symptoms: Typical anginal (substernal pressure, radiation)
- Risk: High risk for MI despite negative troponin
- Disposition: Admit to cardiology, early cath

**NSTEMI** (Non-ST Elevation MI):
- ECG: ST depressions, T wave inversions, or non-specific changes
- Troponin: ELEVATED and RISING (diagnostic)
- Symptoms: Typical anginal, ongoing or recent
- Disposition: Admit to CCU, cath within 24-72h

**STEMI** (ST Elevation MI):
- ECG: ST elevations ≥1mm in 2 contiguous limb leads OR ≥2mm in 2 contiguous precordial leads
- Troponin: Elevated (but don't wait for results)
- Symptoms: Severe, crushing chest pain
- **TIME-CRITICAL**: Activate cath lab immediately, door-to-balloon <90 min
- Disposition: Emergent PCI, then CCU

### ECG-Troponin Coherence

The ECG and troponin must tell the same story.

**Coherence Rules**:
```python
if ECG_shows_ST_elevations_meeting_criteria:
    diagnosis = "STEMI"
    troponin_will_be_elevated = True
    action = "IMMEDIATE cath lab activation"
    do_not_wait_for_troponin_results()

elif troponin_elevated and ECG_normal_or_nonspecific:
    diagnosis = "NSTEMI"
    expect_ST_depressions_or_T_wave_inversions = possible
    action = "Admit to cardiology, cath within 24-72h"

elif ECG_shows_ST_depressions and troponin_negative:
    diagnosis = "Unstable angina"
    action = "Admit, high-risk, early invasive strategy"

elif troponin_negative_x2 and ECG_normal:
    diagnosis = "Low risk, likely rule-out"
    check_HEART_score()
    if HEART_score <= 3:
        disposition = "Discharge with outpatient follow-up"
```

**Why this matters for generation**: Never generate a patient with ST elevations who has negative troponin and gets discharged. Never generate NSTEMI without elevated troponin. The ECG and labs must match the diagnosis.

### STEMI Recognition and Response

STEMI is a medical emergency requiring immediate action.

**STEMI Criteria** (any one meets criteria):
- ST elevation ≥1mm in 2 contiguous limb leads (e.g., II, III, aVF for inferior MI)
- ST elevation ≥2mm in 2 contiguous precordial leads (e.g., V1-V4 for anterior MI)
- New left bundle branch block (Sgarbossa criteria)
- ST depressions V1-V3 with tall R waves (posterior MI)

**STEMI Territories**:
- **Inferior STEMI**: ST elevations in II, III, aVF → Right coronary artery
- **Anterior STEMI**: ST elevations in V1-V4 → Left anterior descending artery
- **Lateral STEMI**: ST elevations in I, aVL, V5-V6 → Left circumflex artery
- **Posterior STEMI**: ST depressions V1-V3, tall R waves → Posterior descending artery

**STEMI Timeline** (time-critical):
```python
arrival = 0_min
ECG_obtained = 5_min  # Within 10 min of arrival
STEMI_recognized = 5_min
code_STEMI_activated = 7_min  # Immediately
cath_lab_team_paged = 7_min
aspirin_ticagrelor_heparin_given = 10_min
patient_to_cath_lab = 25_min
balloon_inflation = 60_min  # GOAL: Door-to-balloon <90 min

# If STEMI patient doesn't follow this timeline, something is wrong
```

**Why this matters for generation**: STEMI is defined by ECG, not troponin. The moment you see ST elevations, CODE STEMI is activated. Don't generate STEMI patients with delayed recognition or treatment.

### Risk Stratification: HEART Score

The HEART score stratifies chest pain patients into low, intermediate, and high risk.

**HEART Score Components**:
1. **History**: Highly suspicious (2), Moderately suspicious (1), Slightly suspicious (0)
2. **ECG**: ST depression (2), Non-specific repolarization (1), Normal (0)
3. **Age**: ≥65 (2), 45-65 (1), <45 (0)
4. **Risk Factors**: ≥3 factors (2), 1-2 factors (1), None (0)
5. **Troponin**: ≥3x normal (2), 1-3x normal (1), Normal (0)

**Interpretation**:
- **Score 0-3**: Low risk (2% MACE) → consider discharge with outpatient stress test
- **Score 4-6**: Intermediate risk (12% MACE) → admit for observation
- **Score 7-10**: High risk (65% MACE) → admit, early invasive strategy

**Example Application**:
```python
patient = {
    "history": "substernal pressure, radiation to arm, diaphoresis",  # Highly suspicious = 2
    "ECG": "ST depressions 1mm in V4-V6",  # ST depression = 2
    "age": 67,  # ≥65 = 2
    "risk_factors": ["HTN", "diabetes", "smoking"],  # ≥3 = 2
    "troponin": 4.5,  # ≥3x normal = 2
}
HEART_score = 2 + 2 + 2 + 2 + 2 = 10  # High risk - admit, cath lab
```

**Why this matters for generation**: Use HEART score to justify disposition. Low HEART score → discharge. High HEART score → admit and cath.

### Troponin Kinetics

Troponin rises and falls in a predictable pattern after MI.

**Timeline**:
- **Hour 0**: May be normal or mildly elevated
- **Hour 3-6**: Peak troponin (highest levels)
- **Hour 12-24**: Starts declining
- **Day 3-10**: Returns to normal

**Serial Troponins**:
- Initial troponin at presentation (hour 0)
- Repeat troponin at hour 3 (standard for rule-out)
- If rising (e.g., 0.5 → 3.2 → 8.5), confirms ongoing MI

**Magnitude**:
- <0.04 ng/mL: Normal (negative)
- 0.04-0.5 ng/mL: Mildly elevated (demand ischemia, small MI)
- 0.5-15 ng/mL: Elevated (NSTEMI range)
- >15 ng/mL: Markedly elevated (large STEMI)

**Why this matters for generation**: Troponin must rise over time in MI. Generate serial troponins that are coherent (e.g., 0.8 → 3.5 → 9.2, not 5.0 → 2.0 → 8.0).

### Cardiac Risk Factors

Cardiac risk factors increase probability of ACS and influence HEART score.

**Major Risk Factors**:
- Hypertension (60% of chest pain patients)
- Hyperlipidemia (50%)
- Diabetes mellitus (30%)
- Smoking (current 30%, former 40%)
- Family history of early CAD (35%)
- Known CAD or prior MI

**Risk Factor Clustering**:
```python
if age > 60:
    probability_has_HTN = 0.65
    probability_has_hyperlipidemia = 0.55
    probability_has_diabetes = 0.30

if has_diabetes:
    # Diabetics often have multiple risk factors
    also_has_HTN = 0.75
    also_has_hyperlipidemia = 0.70
```

**Why this matters for generation**: High-risk patients (multiple risk factors, older) should have higher probability of actual MI. Low-risk patients (young, no risk factors) more likely to be rule-outs.

### Medications and Timing

Cardiac medications must be given in correct sequence and timing.

**ED Treatment for STEMI** (time-critical):
```python
arrival_time = 0
aspirin_325mg_chewed = 5_min  # Immediately
ticagrelor_180mg_or_clopidogrel_600mg = 10_min  # Dual antiplatelet
heparin_bolus_60_units_per_kg = 10_min
nitroglycerin_SL_if_pain_ongoing = 12_min
morphine_IV_if_severe_pain = 15_min  # Caution: may mask symptoms
metoprolol_5mg_IV_if_not_contraindicated = 20_min
to_cath_lab = 25_min
```

**ED Treatment for NSTEMI/Unstable Angina**:
- Aspirin 325mg PO
- Ticagrelor 180mg PO (or clopidogrel 600mg)
- Heparin drip or enoxaparin 1mg/kg SQ Q12H
- Nitroglycerin drip for ongoing chest pain
- Metoprolol 25-50mg PO Q6H
- Atorvastatin 80mg PO (high-intensity statin)
- Admit to cardiology service

**Why this matters for generation**: Don't give beta-blockers to STEMI patients with bradycardia or hypotension. Don't give morphine before aspirin. Timing matters.

## Generation Guidelines

### How to Apply This Knowledge

**When the user says**: "Generate an ED chest pain patient"

**Claude should**:
1. **Determine risk level**: Default to intermediate risk (HEART score 4-6)
2. **Select outcome**: Rule-out (40%), NSTEMI (30%), unstable angina (20%), STEMI (10%)
3. **Generate coherent findings**:
   ```python
   if outcome == "rule-out":
       ECG = "normal sinus rhythm, no ST changes"
       troponin_0h = "<0.04 ng/mL"
       troponin_3h = "<0.04 ng/mL"
       symptoms = "atypical - sharp, positional"
       HEART_score = 2-3  # Low risk
       disposition = "discharge with cardiology follow-up"
   ```
4. **Add appropriate risk factors**: Age 55, HTN, hyperlipidemia
5. **Create realistic timeline**: Arrival → ECG (10 min) → Labs sent (20 min) → Results (90 min)

**When the user says**: "Generate a STEMI patient"

**Claude should**:
1. **Select MI territory**: Inferior (most common) or anterior
2. **Generate diagnostic ECG**:
   ```python
   if territory == "inferior":
       ECG = "ST elevations 3-4mm in II, III, aVF"
       reciprocal_changes = "ST depressions in I, aVL"
       culprit_artery = "Right coronary artery"
   elif territory == "anterior":
       ECG = "ST elevations 4-6mm in V1-V4"
       culprit_artery = "Left anterior descending"
   ```
3. **Make troponin coherent**: Will be elevated, but DON'T WAIT for results
4. **Create time-critical timeline**:
   - Arrival → 0 min
   - ECG obtained → 5 min
   - CODE STEMI activated → 7 min
   - Door-to-balloon → <90 min (ideally 60 min)
5. **Severe symptoms**: "Crushing" chest pain, diaphoresis, nausea, dyspnea
6. **Disposition**: Emergent PCI → CCU

**When the user says**: "Generate an NSTEMI patient"

**Claude should**:
1. **ECG findings**: ST depressions or T wave inversions (NOT ST elevations)
2. **Troponin**: Elevated and rising
   ```python
   troponin_0h = 3.8  # Elevated
   troponin_3h = 9.2  # Rising (confirms ongoing MI)
   ```
3. **Symptoms**: Typical anginal (substernal pressure, radiation, diaphoresis)
4. **Timeline**: Not as time-critical as STEMI, but admit to cardiology
5. **Disposition**: CCU admission, cardiac cath within 24-72h

### Coherence Checks

Before finalizing a chest pain patient, verify:

```python
# 1. STEMI criteria
if has_ST_elevations_meeting_criteria:
    assert diagnosis == "STEMI"
    assert code_STEMI_activated == True
    assert door_to_balloon_time < 90_min
    assert NOT_sent_to_floor  # Must go to cath lab

# 2. Troponin-diagnosis coherence
if diagnosis == "NSTEMI":
    assert troponin > 0.04  # Must be elevated
    assert troponin_rising  # Serial troponins should increase
    assert NO_ST_elevations  # NSTEMI by definition

if diagnosis == "rule-out":
    assert troponin_0h < 0.04 and troponin_3h < 0.04
    assert ECG_normal_or_nonspecific

# 3. HEART score and disposition alignment
if HEART_score <= 3:
    disposition_should_be_discharge_with_follow_up()
if HEART_score >= 7:
    disposition_should_be_admit_early_cath()

# 4. Symptom-severity coherence
if diagnosis == "STEMI":
    assert pain_severity >= 8  # Severe
    assert has_diaphoresis  # Common
if diagnosis == "rule-out" and pain_severity >= 9:
    reconsider_diagnosis()  # Severe pain unusual for rule-out
```

## Example Requests and Interpretations

### Example 1: Simple Request - "ED chest pain patient"

**User says**: "Generate an ED chest pain patient"

**Claude interprets**:
- Risk: Intermediate (most common)
- Outcome: Rule-out (most common ED outcome)
- Age: 55 years
- Setting: Emergency department

**Key features Claude generates**:

**Demographics**: Age 55, male, smoker

**Chief Complaint**: "Chest pain for 2 hours"

**HPI**: Dull, aching chest pain started 2 hours ago while watching TV. 5/10 intensity, center of chest, no radiation. Worsens with deep breath. Denies SOB, nausea, diaphoresis. No recent trauma.

**PMH**: Hypertension, hyperlipidemia

**Vital Signs**: BP 135/82, HR 78, RR 16, O2 99% RA

**ECG** (5 min): Normal sinus rhythm, rate 76, no ST changes

**Labs**:
- Troponin I (0h): <0.04 ng/mL (negative)
- Troponin I (3h): <0.04 ng/mL (negative)

**HEART Score**: 3 (low risk)
- History: Slightly suspicious (0)
- ECG: Normal (0)
- Age: 45-65 (1)
- Risk factors: 2 (HTN, smoking) = 1
- Troponin: Normal (0)

**Diagnosis**: Chest pain, likely musculoskeletal, rule out ACS

**Disposition**: Discharged with ibuprofen, outpatient stress test in 1 week

---

### Example 2: Severity-Specific - "STEMI patient"

**User says**: "Generate a STEMI patient"

**Claude interprets**:
- Diagnosis: ST-elevation myocardial infarction
- Territory: Inferior (most common)
- Severity: Severe, time-critical
- Action: Emergent cath lab activation

**Key features Claude generates**:

**Demographics**: Age 58, male, smoker (40 pack-years)

**Chief Complaint**: "Crushing chest pain"

**HPI**: Sudden-onset severe substernal chest pain 30 minutes ago while shoveling snow. 10/10, pressure-like, radiating to left arm and neck. Severe dyspnea, nausea, vomiting, profuse diaphoresis. Called 911.

**PMH**: Hypertension, hyperlipidemia, family history (father MI at 52)

**EMS Report**: BP 145/90, HR 110, O2 92% on 4L NC, gave aspirin 324mg en route

**ED Vital Signs** (arrival): BP 138/85, HR 105, RR 24, O2 93% on 4L NC

**ECG** (5 min from arrival):
- **ST elevations 4mm in II, III, aVF** (INFERIOR STEMI)
- Reciprocal ST depressions in I, aVL
- **STEMI CRITERIA MET**

**Immediate Actions**:
- **CODE STEMI activated** at 7 minutes
- Cath lab team paged emergently
- Aspirin 325mg (already given by EMS)
- Ticagrelor 180mg PO
- Heparin 4000 unit bolus IV
- Morphine 4mg IV for pain
- Nitroglycerin 0.4mg SL x2

**Troponin** (drawn but NOT waiting): 8.5 ng/mL (elevated as expected)

**Door-to-Balloon**: 58 minutes

**Cath Findings**:
- Right coronary artery 100% acute occlusion
- Drug-eluting stent placed
- TIMI 3 flow restored

**Disposition**: CCU, hemodynamically stable

---

### Example 3: Diagnosis-Specific - "NSTEMI patient"

**User says**: "Generate an NSTEMI patient"

**Claude interprets**:
- Diagnosis: Non-ST elevation MI
- ECG: ST depressions or T wave inversions (NO ST elevations)
- Troponin: Elevated and rising
- Urgency: Admit to cardiology, cath within 24-72h (not emergent)

**Key features Claude generates**:

**Demographics**: Age 67, female, diabetic

**Chief Complaint**: "Squeezing chest pain and nausea"

**HPI**: Awoke at 3 AM with severe substernal chest pressure, 8/10, radiating to left arm and jaw. Nausea, diaphoresis, mild dyspnea. Took nitroglycerin x2 at home with minimal relief. Pain ongoing on arrival.

**PMH**: Type 2 diabetes (10 years), hypertension, hyperlipidemia, 30 pack-year smoking

**Vital Signs**: BP 155/92, HR 98, RR 22, O2 94% RA

**ECG** (8 min):
- Sinus tachycardia 98 bpm
- **ST depressions 2mm in V4-V6**
- **T wave inversions in I, aVL**
- NO ST ELEVATIONS

**Troponin**:
- 0h: 3.8 ng/mL (ELEVATED - diagnostic for MI)
- 3h: 9.2 ng/mL (RISING - confirms ongoing MI)

**Diagnosis**: Non-ST elevation myocardial infarction (NSTEMI)

**Treatment**:
- Aspirin 325mg PO
- Ticagrelor 180mg PO
- Heparin drip
- Nitroglycerin drip (pain improved)
- Metoprolol 25mg PO
- Atorvastatin 80mg PO

**Disposition**: Admitted to CCU, cardiac catheterization scheduled for next morning

**Hospital Course**:
- Cath Day 2: 85% LAD stenosis, drug-eluting stent placed
- Discharged Day 4

---

### Example 4: Risk-Level Specific - "Low-risk chest pain"

**User says**: "Generate a low-risk chest pain patient for discharge"

**Claude interprets**:
- Risk: Low (HEART score ≤3)
- Outcome: Rule-out, safe for discharge
- Age: <65 years
- Minimal risk factors

**Key features Claude generates**:

**Demographics**: Age 48, male, non-smoker

**Chief Complaint**: "Chest pain for 2 hours"

**HPI**: Dull aching chest pain, 5/10, started while watching TV. Located center of chest, worsens with deep breath. No radiation. Denies SOB, nausea, diaphoresis. Pain improved with position change.

**PMH**: Hypertension

**Vital Signs**: BP 135/82, HR 78, RR 16, O2 99% RA

**Physical Exam**:
- Chest wall tenderness with palpation over left chest
- Otherwise normal

**ECG**: Normal sinus rhythm, no ST changes

**Troponin**: 0h <0.04, 3h <0.04 (both negative)

**HEART Score**: 3 (LOW RISK)
- History: Slightly suspicious (0)
- ECG: Normal (0)
- Age: 45-65 (1)
- Risk factors: 1 (HTN) = 1
- Troponin: Normal (0)

**Diagnosis**: Chest pain, likely musculoskeletal

**Disposition**: Discharged with ibuprofen 600mg TID, outpatient stress test in 1 week, return precautions given

---

### Example 5: Complication-Specific - "STEMI with cardiogenic shock"

**User says**: "Generate a STEMI patient with cardiogenic shock"

**Claude interprets**:
- Diagnosis: Massive MI with shock
- Severity: Critical, life-threatening
- Complications: Cardiogenic shock, pulmonary edema
- Treatment: Pressors, possible mechanical support

**Key features Claude generates**:

**Demographics**: Age 72, male

**Chief Complaint**: "Crushing chest pain, can't breathe"

**Vital Signs**: BP 80/50 (hypotensive), HR 115, RR 28, O2 88% RA

**Exam**: Cool, clammy, altered mental status, pulmonary edema (rales throughout)

**ECG**:
- **ST elevations 6mm in V1-V6** (ANTERIOR STEMI - extensive)
- Poor R wave progression

**Treatment**:
- CODE STEMI activated
- Intubated for respiratory failure
- Norepinephrine drip started (for shock)
- Aspirin, ticagrelor, heparin given
- Emergent cath with intra-aortic balloon pump placement

**Cath Findings**:
- LAD 100% proximal occlusion (large territory)
- Stent placed
- IABP placed for hemodynamic support

**Troponin**: >50 ng/mL (markedly elevated)

**Complications**: Cardiogenic shock, acute heart failure

**Disposition**: CCU, on pressors and IABP, guarded prognosis

## Variations

### Variation: Young Low-Risk Chest Pain
Younger patient with atypical features, very low cardiac risk.
- age_range: 25-40 years
- cardiac_risk: low
- has_risk_factors: false
- final_diagnosis: non-cardiac
- **Presentation**: Sharp, positional chest pain, worse with deep breath
- **Exam**: Chest wall tenderness, pain reproduced with palpation
- **ECG**: Normal sinus rhythm, early repolarization (normal variant)
- **Troponin**: Negative x 2
- **Diagnosis**: Costochondritis or musculoskeletal pain
- **Disposition**: Discharge with NSAIDs, reassurance, PCP follow-up

### Variation: STEMI with Cardiogenic Shock
Massive MI complicated by cardiogenic shock, critical presentation.
- cardiac_risk: high
- final_diagnosis: stemi
- presentation_severity: severe
- **Vital Signs**: BP 80/50 (hypotensive), HR 115 (tachycardic), RR 28, O2 88%
- **Exam**: Cool, clammy, altered mental status, pulmonary edema
- **ECG**: Extensive ST elevations V1-V6 (anterior STEMI)
- **Treatment**: Pressors (norepinephrine), intubation, emergent cath with IABP
- **Troponin**: Markedly elevated (>50 ng/mL)
- **Complications**: Cardiogenic shock, acute heart failure
- **Disposition**: CCU, possible mechanical circulatory support

### Variation: Atypical Presentation in Diabetic
Diabetic patient with minimal or no chest pain (silent MI).
- has_risk_factors: true
- cardiac_risk: high
- final_diagnosis: nstemi
- **Presentation**: "Just not feeling right," vague fatigue, mild dyspnea
- **Pain**: Minimal or absent (diabetic neuropathy)
- **ECG**: Subtle ST depressions, may be overlooked initially
- **Troponin**: Elevated (2.5 ng/mL)
- **Key**: High index of suspicion in diabetics with vague symptoms
- **Outcome**: NSTEMI diagnosed, cardiac cath, stent placement

### Variation: Cocaine-Induced Chest Pain
Young patient with cocaine use presenting with chest pain.
- age_range: 25-45 years
- cardiac_risk: low (young) but elevated (cocaine)
- final_diagnosis: unstable-angina or nstemi
- **History**: Cocaine use in past 24 hours
- **Mechanism**: Coronary vasospasm, increased cardiac demand
- **ECG**: May show ST elevations or depressions
- **Troponin**: May be elevated if true MI
- **Treatment**: Benzodiazepines, nitroglycerin, aspirin
- **AVOID**: Beta-blockers (unopposed alpha stimulation)
- **Disposition**: Admit for observation, serial troponins, substance abuse counseling

### Variation: Aortic Dissection (Rare but Critical)
Patient with sudden-onset tearing chest pain radiating to back.
- age_range: 55-75 years
- presentation_severity: severe
- final_diagnosis: non-cardiac (but critical)
- **Presentation**: "Worst pain of my life," tearing/ripping quality, back pain
- **Risk Factors**: Hypertension, connective tissue disorder
- **Vital Signs**: BP differential between arms (>20 mmHg), often hypertensive
- **ECG**: May be normal or show LVH from chronic hypertension
- **Troponin**: Normal (unless dissection extends to coronary ostia)
- **CXR**: Widened mediastinum (classic but not always present)
- **Diagnosis**: CT angiography chest - Type A dissection
- **Treatment**: Blood pressure control, emergent cardiothoracic surgery
- **Critical**: Do NOT give thrombolytics

## Generation Rules

### Demographics
- **Age**: 45-75 years (higher cardiac risk with age)
- **Gender**: Male patients at higher risk <65, equal risk >65
- **Smoking Status**: Current smoker (30%), former smoker (40%), never (30%)

### Conditions

**Cardiac Risk Factors** (if has_risk_factors=true, select 2-4):
- Hypertension (I10) - 60% prevalence
- Hyperlipidemia (E78.5) - 50% prevalence
- Type 2 Diabetes (E11.9) - 30% prevalence
- Obesity (E66.9) - 40% prevalence
- Family history of CAD - 35% prevalence

**Final Diagnosis Options**:

If final_diagnosis=rule-out:
- Chest pain, unspecified (R07.9)
- Possible musculoskeletal chest pain (M79.1)
- Anxiety-related chest pain (F41.9)

If final_diagnosis=unstable-angina:
- Unstable angina (I20.0)
- Coronary artery disease (I25.10)

If final_diagnosis=nstemi:
- Non-ST elevation myocardial infarction (I21.4)
- Acute coronary syndrome (I24.9)

If final_diagnosis=stemi:
- ST elevation myocardial infarction - anterior (I21.09) or inferior (I21.19)
- Acute myocardial infarction (I21.9)

If final_diagnosis=non-cardiac:
- Gastroesophageal reflux disease (K21.9)
- Costochondritis (M94.0)
- Pulmonary embolism (I26.99) - rare but critical
- Aortic dissection (I71.00) - rare but critical

### Vital Signs

**Low Cardiac Risk / Rule-Out**:
- **Blood Pressure**: 120-140/70-85 mmHg (normal)
- **Heart Rate**: 70-90 bpm (normal)
- **Temperature**: 98.0-98.6 F (afebrile)
- **Respiratory Rate**: 14-18 breaths/min (normal)
- **Oxygen Saturation**: 97-100% on room air

**Intermediate Risk / Unstable Angina**:
- **Blood Pressure**: 140-160/85-95 mmHg (mildly elevated)
- **Heart Rate**: 85-105 bpm (mildly elevated)
- **Temperature**: 98.0-99.0 F
- **Respiratory Rate**: 16-22 breaths/min
- **Oxygen Saturation**: 95-98% on room air

**High Risk / NSTEMI**:
- **Blood Pressure**: 100-150/60-90 mmHg (variable, may be low)
- **Heart Rate**: 90-115 bpm (tachycardic)
- **Temperature**: 98.6-99.5 F (may have low-grade fever)
- **Respiratory Rate**: 18-24 breaths/min (tachypneic)
- **Oxygen Saturation**: 92-96% on room air (may be hypoxic)

**STEMI** (critical):
- **Blood Pressure**: 90-140/50-80 mmHg (often hypotensive)
- **Heart Rate**: 50-65 bpm (bradycardic if inferior MI) OR 100-130 bpm (tachycardic)
- **Temperature**: 98.6-100.0 F
- **Respiratory Rate**: 20-28 breaths/min (tachypneic, possible pulmonary edema)
- **Oxygen Saturation**: 88-94% on room air (hypoxic)

### Laboratory

**Cardiac Biomarkers**:

Rule-Out:
- **Troponin I**: <0.04 ng/mL (normal) at 0h and 3h
- **CK-MB**: <5 ng/mL (normal)
- **BNP**: <100 pg/mL (normal)

Unstable Angina:
- **Troponin I**: <0.04 ng/mL (negative, but high risk features)
- **CK-MB**: <5 ng/mL
- May have dynamic ECG changes

NSTEMI:
- **Troponin I**: 0.5-15 ng/mL (elevated, diagnostic)
- **CK-MB**: 8-50 ng/mL (elevated)
- **Peak Troponin**: 3-6 hours after presentation, may require serial troponins

STEMI:
- **Troponin I**: 2.0-50+ ng/mL (markedly elevated)
- **CK-MB**: 25-200+ ng/mL (markedly elevated)
- **Myoglobin**: Elevated early (2-4 hours)

### Medications

**ED Treatment - Rule-Out / Low Risk**:
- Aspirin 325mg PO x 1 (unless contraindicated)
- Nitroglycerin 0.4mg SL PRN chest pain x 3 (if pain persists)
- GI cocktail (antacid + viscous lidocaine) if suspected GI cause
- Discharge with outpatient cardiology follow-up

**ED Treatment - Unstable Angina / NSTEMI**:
- Aspirin 325mg PO x 1 (loading dose)
- Ticagrelor 180mg PO x 1 OR Clopidogrel 600mg PO x 1 (P2Y12 inhibitor loading)
- Heparin drip OR Enoxaparin 1mg/kg SQ Q12H (anticoagulation)
- Nitroglycerin drip 10-200 mcg/min (for active chest pain)
- Metoprolol 25-50mg PO/IV Q6H (beta blockade)
- Atorvastatin 80mg PO QHS (high-intensity statin)
- Admit to cardiology service

**ED Treatment - STEMI** (time-critical):
- Aspirin 325mg PO x 1 (chewed)
- Ticagrelor 180mg PO x 1 (loading dose)
- Heparin 60 units/kg IV bolus, then 12 units/kg/hr drip
- Morphine 2-4mg IV PRN pain (caution: may mask symptoms)
- Nitroglycerin 0.4mg SL x 3 OR nitroglycerin drip
- Metoprolol 5mg IV Q5min x 3 doses (if not contraindicated)
- **IMMEDIATE**: Activate cath lab for primary PCI OR
- **If PCI unavailable**: Thrombolytic therapy (tPA, tenecteplase)
- Goal door-to-balloon time: <90 minutes

### Timeline

**Rule-Out Chest Pain** (low risk):
- 0 min: Arrival to ED, triage, chief complaint "chest pain"
- 5 min: Placed on cardiac monitor, IV access, O2 if needed
- 10 min: ECG obtained (normal sinus rhythm, no ST changes)
- 15 min: Provider evaluation, history and physical
- 20 min: Labs sent: troponin, BMP, CBC
- 30 min: Aspirin 325mg given, nitroglycerin trial if pain ongoing
- 90 min: First troponin results negative (<0.04)
- 180 min: Second troponin results negative
- 240 min: HEART score calculated: low risk
- 270 min: Discharge with cardiology follow-up in 1 week
- Disposition: Home with outpatient stress test

**STEMI** (critical, time-sensitive):
- 0 min: Arrival to ED, "crushing chest pain radiating to left arm"
- 3 min: Cardiac monitor shows ST elevations
- 5 min: STAT 12-lead ECG: 3mm ST elevations in II, III, aVF (inferior STEMI)
- 7 min: **CODE STEMI ACTIVATED**
- 8 min: Cardiology and cath lab team paged emergently
- 10 min: Aspirin 325mg chewed, ticagrelor 180mg, heparin bolus given
- 12 min: Two large-bore IVs, labs sent (troponin, type & screen, coags)
- 15 min: Nitroglycerin 0.4mg SL x 2 doses (pain improved)
- 20 min: Metoprolol 5mg IV x 1
- 25 min: Patient to cath lab
- 45 min: Right coronary artery 100% occlusion identified
- 60 min: **Door-to-balloon 60 minutes** - stent deployed, TIMI 3 flow restored
- 90 min: Patient to CCU, hemodynamically stable
- 24-48h: Echo shows EF 45%, inferior wall hypokinesis
- 3-5 days: Cardiac rehabilitation referral, discharge planning

## Validation Rules

| Rule | Requirement | Example |
|------|-------------|---------|
| Troponin | Positive numeric or "negative" | 0.45 ng/mL (elevated) |
| HEART score | 0-10 | 6 (high risk) |
| TIMI score | 0-7 for UA/NSTEMI | 4 (intermediate) |
| Door-to-ECG | ≤10 minutes per guidelines | 8 minutes |
| Door-to-balloon | ≤90 minutes for STEMI | 55 minutes |
| ECG findings | Documented interpretation | ST elevation V2-V4 |
| Chest pain character | Typical, atypical, non-cardiac | "typical" |
| Risk stratification | low, intermediate, high | "high risk" |

### Business Rules

- **STEMI Protocol**: Door-to-balloon <90 min; activate cath lab immediately
- **NSTEMI/UA**: Risk stratify with HEART/TIMI; high risk → early invasive strategy
- **Serial Troponins**: At presentation and 3-6 hours later; high-sensitivity troponin preferred
- **ECG Timing**: Obtain within 10 minutes of arrival; repeat if symptoms change
- **Aspirin**: Give immediately unless contraindicated
- **Anticoagulation**: Heparin for ACS; choice depends on planned strategy
- **Risk Scores**: HEART score validated for ED chest pain disposition decisions
- **Stress Testing**: Low-risk patients may undergo stress testing before discharge

## References

- 2021 AHA/ACC/ASE/CHEST/SAEM/SCCT/SCMR Guideline for the Evaluation and Diagnosis of Chest Pain
- 2023 ACC/AHA/ACCP/ASPC/NLA/PCNA Guideline for the Management of Patients With Chronic Coronary Disease
- Fourth Universal Definition of Myocardial Infarction (2018)
- HEART Score validation studies (Six AJ, et al. 2008)

## Related Skills

### PatientSim Cohorts

- [SKILL.md](SKILL.md) - PatientSim overview
- [heart-failure.md](heart-failure.md) - Cardiac comorbidity
- [adt-workflow.md](adt-workflow.md) - Admission workflows
- [orders-results.md](orders-results.md) - Lab ordering and results

### Cross-Product: MemberSim

- [../membersim/professional-claims.md](../membersim/professional-claims.md) - ED physician billing, cardiology consult
- [../membersim/facility-claims.md](../membersim/facility-claims.md) - ED facility claims, cardiac cath facility billing

> **Integration Pattern:** Use PatientSim for ED workup, disposition decisions, and admission if needed. Use MemberSim for ED facility claims (revenue code 045x) and professional claims. STEMI → cath lab generates high-cost facility claims.

### Cross-Product: RxMemberSim

- [../rxmembersim/retail-pharmacy.md](../rxmembersim/retail-pharmacy.md) - Cardiac medication fills (statins, antiplatelets, beta-blockers)
- [../rxmembersim/specialty-pharmacy.md](../rxmembersim/specialty-pharmacy.md) - PCSK9 inhibitors for high-risk patients

> **Integration Pattern:** Use PatientSim for acute medication orders. Use RxMemberSim for discharge medication fills - ACS patients typically start DAPT (aspirin + P2Y12 inhibitor), high-intensity statin.

### Reference Files

- [../../references/data-models.md](../../references/data-models.md) - Entity schemas
- [../../references/code-systems.md](../../references/code-systems.md) - ICD-10, CPT, LOINC codes
