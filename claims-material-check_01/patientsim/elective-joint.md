---
name: elective-joint
description: "Elective total joint arthroplasty (hip/knee replacement) with complete perioperative event sequences. Triggers: joint replacement, hip replacement, knee replacement, arthroplasty, orthopedic surgery, perioperative, POD, post-operative, DVT, surgical"
---

# Elective Joint Replacement Cohort - Complete Surgical Event Timelines

A cohort template for generating patients undergoing elective total joint arthroplasty (hip or knee replacement) **with complete perioperative event sequences** from pre-operative evaluation through surgery, daily post-operative progression (POD 0-3), complications, and discharge planning.

## For Claude

Use this skill when the user requests orthopedic surgery patients, specifically total joint replacement cohorts. This teaches you how to generate **realistic surgical event timelines** for perioperative patients across all phases - pre-operative optimization, day of surgery, post-operative recovery with daily progression, rehabilitation milestones, and potential complications.

**When to apply this skill:**
- User mentions joint replacement, hip/knee replacement, or arthroplasty
- User requests orthopedic surgery or perioperative cohorts with event timelines
- User asks for elective surgery admissions with complete surgical course
- User specifies POD (post-operative day) patients with progression over time
- User mentions orthopedic complications (DVT, infection, delirium) and their development
- User needs surgical workflow testing or post-op protocol validation

**Key capabilities this skill provides:**
- How to generate complete surgical event timelines (pre-op workup → surgery → POD 0 → POD 1 → POD 2 → POD 3 → discharge)
- How to structure day-by-day progression with vital signs, pain scores, lab trends, PT milestones
- How to sequence pain management events (IV opioids → transition to PO → multimodal analgesia)
- How to create complication event sequences (DVT developing on POD 2, workup, treatment)
- How to select appropriate DVT prophylaxis and show timing (enoxaparin daily dosing)
- How to track PT progression events (POD 1: bedside → POD 2: 100 feet → POD 3: stairs)
- When to send patients home vs skilled nursing facility based on functional milestones
- How to create alert-triggering events (sudden hypotension, tachycardia suggesting bleeding/PE)

**Important**: Joint replacement patients are **high risk for DVT** (10-40% without prophylaxis). Always include DVT prophylaxis (enoxaparin, rivaroxaban, or aspirin). Post-operative infections are devastating - include pre-op antibiotics and proper wound care.

**Clinical coherence**: Match pain levels to post-op day (POD 0: 6-8/10 → POD 3: 3-5/10), ensure Hgb drop is realistic (typically 2-4 g/dL from blood loss), and include appropriate PT milestones (POD 1: bedside → POD 2: 100 feet → POD 3: stairs). Show **temporal progression** with events occurring in realistic sequence.

## Metadata
- **Type**: cohort-template
- **Version**: 2.0
- **Author**: PatientSim
- **Tags**: orthopedics, surgery, perioperative, rehabilitation

## Purpose

This cohort generates realistic patients undergoing elective total joint replacement surgery. It models the complete perioperative journey including pre-operative optimization, surgical procedure, post-operative care, rehabilitation, and potential complications.

The cohort is designed to:
- Simulate realistic elective surgery admissions
- Model pre-operative medical optimization and clearance
- Generate appropriate perioperative medication management
- Support common complications (DVT, infection, delirium)
- Include realistic recovery timeline and disposition planning
- Demonstrate interdisciplinary care (surgery, anesthesia, PT, case management)

## When to Use This Skill

Apply this skill when the user's request involves:

**Direct Keywords**:
- "joint replacement", "total joint arthroplasty", "arthroplasty"
- "hip replacement", "total hip arthroplasty", "THA"
- "knee replacement", "total knee arthroplasty", "TKA"
- "orthopedic surgery", "orthopedic patient", "ortho"
- "post-op patient", "POD 1", "POD 2" (post-operative day)
- "elective surgery", "planned surgery"

**Clinical Cohorts**:
- "Generate a patient for hip replacement"
- "I need a post-op orthopedic patient"
- "Create a knee replacement patient on POD 2"
- "Generate a patient with post-op DVT"
- "Make an elderly patient after joint surgery"
- "I need a patient going to SNF after surgery"

**Implicit Indicators**:
- User mentions DVT prophylaxis or enoxaparin (common in joint replacement)
- User requests perioperative care or surgical timeline
- User mentions PT/OT (physical/occupational therapy) in hospital setting
- User specifies "walker", "assistive device", "mobility" in post-op context
- User mentions orthopedic complications (infection, DVT, delirium)
- User asks for discharge planning or SNF placement

**Co-occurring Mentions**:
- When user mentions joint replacement AND DVT (10-40% risk without prophylaxis)
- When user mentions surgery AND pain control (multimodal analgesia key)
- When user mentions elderly AND delirium (common post-op complication)
- When user mentions orthopedic AND rehabilitation/PT
- When user mentions obesity AND osteoarthritis (strong association)

## Trigger Phrases

- joint replacement
- hip replacement
- knee replacement
- THA
- TKA
- arthroplasty
- orthopedic surgery
- post-op orthopedic
- POD
- DVT prophylaxis
- elective surgery

## Dependencies
- healthcare/clinical-domain.md

## Domain Knowledge

### Joint Replacement Overview

Total joint arthroplasty (hip or knee replacement) is one of the most successful elective surgeries, providing dramatic pain relief and functional improvement for end-stage osteoarthritis. Over 1 million joint replacements are performed annually in the US.

**Typical Patient Profile**:
- Age 60-80 years (peak age range)
- BMI 25-35 (obesity is both a risk factor for OA and surgical risk)
- Years of progressive joint pain limiting function
- Failed conservative management (PT, NSAIDs, injections)
- Comorbidities: HTN (65%), diabetes (25%), hyperlipidemia (50%)

**Why this matters for generation**: Joint replacement patients are generally medically complex with multiple comorbidities requiring pre-operative optimization. They're not young/healthy - they're elderly with chronic conditions.

### Hip vs Knee Replacement - Key Differences

**Total Knee Arthroplasty (TKA)**:
- More common than hip (700k/year vs 400k/year)
- More painful post-operatively (knee has more nerve endings)
- ROM more critical (need 90° flexion for stairs, transfers)
- Rehab more intensive
- Female > Male (55% female)

**Total Hip Arthroplasty (THA)**:
- Less painful post-operatively
- Faster recovery, earlier discharge
- Dislocation precautions critical (no flexion >90°, no crossing legs, no internal rotation)
- Gender equal distribution
- Extended DVT prophylaxis (35 days vs 10-14 for knee)

**Why this matters for generation**: When generating TKA patients, expect more pain (6-8/10 POD 0), slower mobility, and more intensive PT. For THA, expect hip precautions education and extended anticoagulation.

### Perioperative Timeline Phases

Joint replacement follows a predictable timeline from decision to surgery through recovery:

**Pre-Operative Phase (4-6 weeks before)**:
- Orthopedic consultation → surgery scheduled
- PCP medical clearance (cardiac risk, diabetes control, infection screening)
- Pre-admission testing (PAT) - labs, EKG, anesthesia evaluation
- Medication adjustments (stop NSAIDs/aspirin 7 days before)
- Education (expectations, home preparation, PT goals)

**Day of Surgery (POD 0)**:
- NPO after midnight → Arrive 2h early → Pre-op area
- Prophylactic antibiotics 30-60 min before incision (cefazolin 2g)
- Spinal anesthesia most common (vs general)
- Surgery 2-3 hours → PACU recovery → Floor by afternoon
- Pain control initiated, PT evaluates bedside
- Hemovac drain monitoring (200-300mL expected)

**Post-Operative Days 1-3**:
- POD 1: Drain removed, catheter out, ambulate with PT, transition to oral pain meds
- POD 2: Increase ambulation distance, stairs practice, case management for discharge planning
- POD 3: Final PT clearance, discharge teaching, home/SNF decision

**Why this matters for generation**: When user says "POD 2 patient", you should generate someone who's already had drain/catheter removed (POD 1), is ambulating 50-100 feet with walker, pain 4-5/10, and case management is planning discharge. Don't generate POD 2 with drain still in or patient bed-bound.

### DVT Prophylaxis (Critical Concept)

Joint replacement is **HIGH RISK for venous thromboembolism (VTE)**. Without prophylaxis, 10-40% develop DVT, 1-2% develop PE.

**Prophylaxis Options**:
1. **LMWH** (Low Molecular Weight Heparin): Enoxaparin 40mg SQ daily x 10-14 days (knee) or 35 days (hip)
   - Most common choice, proven efficacy
   - Requires daily injections (patient/family education needed)

2. **DOACs** (Direct Oral Anticoagulants): Rivaroxaban 10mg PO daily x 12-14 days
   - Oral convenience (better compliance)
   - No monitoring required
   - More expensive

3. **Aspirin**: 325mg PO BID x 6 weeks
   - For low-risk patients only
   - Easier to take, lower bleeding risk
   - Less effective than anticoagulants

4. **Mechanical**: SCDs (sequential compression devices) while in hospital
   - Adjunct to pharmacologic, not replacement

**Why this matters for generation**: NEVER generate a joint replacement patient without DVT prophylaxis. This is a critical safety issue. If generating DVT complication, show patient WAS on prophylaxis (it's not 100% effective). Typical cohort: patient on enoxaparin 40mg daily, develops DVT POD 5-7 at home.

### Multimodal Analgesia (Opioid-Sparing Strategy)

Modern pain management uses **multiple medication classes** to minimize opioid use and side effects.

**The Multimodal Approach**:
```python
pain_control_regimen = {
    "acetaminophen": "1000mg PO Q8H scheduled",  # Baseline, non-opioid
    "NSAID": "celecoxib 200mg PO Q12H",  # Anti-inflammatory (if no contraindication)
    "gabapentinoid": "gabapentin 300mg PO TID",  # Neuropathic component
    "local_anesthetic": "periarticular injection in OR (bupivacaine)",  # Lasts 24-48h
    "opioid_breakthrough": "oxycodone 5-10mg PO Q4H PRN",  # Only for breakthrough pain
}

# POD 0: May use PCA (patient-controlled analgesia) hydromorphone
# POD 1-2: Transition to oral opioids PRN
# Goal: Pain <4/10 at rest, <6/10 with PT
```

**Why this matters for generation**: Don't generate patients on opioids alone (outdated practice). Include the full multimodal regimen. Expect pain to improve over time: POD 0 = 6-8/10, POD 1 = 5-6/10, POD 2 = 4-5/10, POD 3 = 3-4/10.

### Pre-Operative Medical Clearance

Elective surgery requires optimization of medical conditions to minimize perioperative risk.

**Medical Clearance Checklist**:
```python
clearance_requirements = {
    "cardiac_risk": "Revised Cardiac Risk Index → stress test if high risk",
    "diabetes": "HbA1c <8% (ideally <7%), optimize glucose control",
    "hypertension": "BP <160/100, continue meds except ACE-I morning of surgery",
    "anticoagulation": "Bridge warfarin if needed (AFib, mechanical valve)",
    "anemia": "Treat if Hgb <12 (iron, EPO)",
    "infection_screening": "UA negative (UTI must be treated before joint replacement)",
    "smoking": "Cessation counseling (increases infection, delayed healing)",
}

medications_to_stop_before_surgery = {
    "NSAIDs": "STOP 7 days before (bleeding risk)",
    "aspirin": "STOP 7 days before (unless cardiac indication)",
    "ACE_inhibitors": "HOLD morning of surgery (hypotension risk)",
    "metformin": "HOLD morning of surgery (lactic acidosis risk)",
}
```

**Why this matters for generation**: If generating pre-op patient, show they've had medical clearance - labs within 30 days, HbA1c <8% if diabetic, UA negative. If generating complications, you can show inadequate pre-op optimization (e.g., poorly controlled diabetes → increased infection risk).

### Post-Operative Complications

**Deep Vein Thrombosis (DVT)** - Most Common:
- Incidence: 10-40% without prophylaxis, 1-5% with prophylaxis
- Timing: Usually POD 5-14, often after discharge
- Presentation: Calf pain, swelling, warmth, positive Homan's sign
- Diagnosis: Doppler ultrasound (positive thrombus in popliteal/femoral vein)
- Treatment: Therapeutic anticoagulation (apixaban 10mg BID x 7d → 5mg BID x 3mo)

**Prosthetic Joint Infection (PJI)** - Most Devastating:
- Incidence: 1-2%
- Timing: Early (POD 3-30) or late (months-years)
- Presentation: Increasing pain, fever, wound drainage, erythema
- Diagnosis: Joint aspiration (WBC >10,000, positive culture - S. aureus common)
- Treatment: Irrigation & debridement (I&D), 6 weeks IV antibiotics, may require prosthesis removal

**Post-Operative Delirium** - Common in Elderly:
- Incidence: 10-30% (higher in elderly, cognitive impairment)
- Timing: POD 1-3 (peak POD 2)
- Risk Factors: Age >75, polypharmacy, opioids, sleep deprivation
- Presentation: Waxing/waning confusion, disorientation, agitation
- Management: Non-pharmacologic (reorientation, family), minimize opioids, low-dose haloperidol PRN severe agitation

**Why this matters for generation**: Complications should be realistic. DVT presents POD 5-14 at home (not POD 1 in hospital). PJI presents with systemic signs (fever, elevated WBC/ESR/CRP). Delirium happens POD 2-3 in elderly patients on opioids.

## Data Sources (PopulationSim v2.0)

When geography is specified, joint replacement cohorts use real population data:

### Embedded Data Lookup

```
File: skills/populationsim/data/county/places_county_2024.csv
Key columns for orthopedics:
  - OBESITY_CrudePrev: Obesity rate (complication risk factor)
  - DIABETES_CrudePrev: Diabetes (wound healing, infection risk)
  - ARTHRITIS_CrudePrev: Arthritis prevalence (joint replacement candidates)

File: skills/populationsim/data/county/svi_county_2022.csv
Key columns:
  - EP_AGE65: Age 65+ percentage (joint replacement population)
  - RPL_THEMES: Vulnerability (affects discharge disposition)
```

### Data-Driven Comorbidity and Disposition Rates

| Factor | Generic Default | Data-Driven Adjustment |
|--------|-----------------|------------------------|
| Obesity | 60% | OBESITY_CrudePrev × 1.5 (ortho population higher) |
| Diabetes | 25% | DIABETES_CrudePrev × 2 |
| Discharge to SNF | 25% | Higher if SVI > 0.6 and age > 75 |
| DVT risk | 2% (with prophylaxis) | Higher if BMI > 35 and OBESITY > 35% |

### Example: Miami-Dade County, FL (FIPS 12086)
```
From places_county_2024.csv:
  ARTHRITIS_CrudePrev: 24.8%
  OBESITY_CrudePrev: 28.1%
  DIABETES_CrudePrev: 12.3%

From svi_county_2022.csv:
  EP_AGE65: 17.2%
  RPL_THEMES: 0.72

Apply to generation:
  - High arthritis prevalence → reasonable joint replacement demand
  - Obesity comorbidity: ~42% (28.1% × 1.5)
  - Higher SNF discharge rate (high SVI, older population)
```

## Generation Guidelines

### How to Apply This Knowledge

**When the user says**: "Generate a knee replacement patient"

**Claude should**:
1. **Set demographics**:
   ```python
   age = random(60, 80)  # Peak age
   gender = "Female" if random() < 0.55 else "Male"  # Slight female predominance for knee
   BMI = random(28, 34)  # Obesity common
   ```

2. **Add primary diagnosis**:
   - Primary osteoarthritis of right knee (M17.11) [or left M17.12]
   - Duration: 3-5 years of progressive pain
   - Failed conservative management (PT, NSAIDs, injections)

3. **Add realistic comorbidities** (select 2-4):
   - Hypertension (65% probability) → add if yes
   - Type 2 diabetes (25% probability) → add if yes
   - Hyperlipidemia (50% probability) → add if yes
   - Obesity (60% probability) → BMI >30
   - Chronic pain syndrome (very common)
   - GERD (30% probability)

4. **Structure timeline based on context**:
   - If no POD specified: Default to POD 2 (typical teaching case)
   - If "day of surgery": Generate POD 0 timeline
   - If "ready for discharge": Generate POD 3

5. **Include critical safety elements**:
   ```python
   DVT_prophylaxis = "Enoxaparin 40mg SQ daily x 10 days"  # REQUIRED

   multimodal_analgesia = {
       "acetaminophen": "1000mg Q8H scheduled",
       "celecoxib": "200mg Q12H",
       "gabapentin": "300mg TID",
       "oxycodone": "5-10mg Q4H PRN",
   }

   prophylactic_antibiotics = "Cefazolin 2g IV 30 min before incision"  # REQUIRED
   ```

6. **Set appropriate vitals/labs by POD**:
   ```python
   if POD == 0:
       pain = random(6, 8)
       Hgb = baseline_Hgb - random(1, 2)  # Some blood loss
       drain_output = "200-300 mL"

   elif POD == 1:
       pain = random(5, 6)
       Hgb = baseline_Hgb - random(2, 3)  # Peak drop
       drain_removed = True
       catheter_removed = True
       PT_milestone = "Ambulated 30 feet with walker"

   elif POD == 2:
       pain = random(4, 5)
       Hgb = "stable at " + str(baseline_Hgb - 3)
       PT_milestone = "Ambulated 100 feet, stairs x 4 steps"
       case_management = "Planning discharge for POD 3"

   elif POD == 3:
       pain = random(3, 4)
       PT_milestone = "Independent with walker, stairs cleared"
       discharge = True
   ```

7. **Determine disposition**:
   ```python
   if age < 70 and has_home_support and independent_baseline:
       disposition = "Discharge home with home PT 3x/week"
   elif age >= 75 or limited_home_support or complications:
       disposition = "Discharge to SNF for 2-3 weeks rehab"
   ```

**When the user says**: "Generate a patient with post-op DVT"

**Claude should**:
1. **Start with uncomplicated joint replacement** (follow steps above)
2. **Set timeline to POD 5-10** (DVT timing after discharge)
3. **Show patient WAS on prophylaxis**: "Prescribed enoxaparin 40mg SQ daily, reports compliance"
4. **Generate DVT presentation**:
   ```python
   chief_complaint = "Calf pain and swelling"
   HPI = "POD 7 after left THA, discharged POD 3. Reports 2 days progressive left calf pain,
          swelling, warmth. Different from surgical pain. Mild SOB with walking.
          Concerned about blood clot. Compliant with enoxaparin injections."

   vitals = {
       "HR": random(95, 105),  # Mild tachycardia
       "RR": random(18, 22),  # Mild tachypnea
       "O2": random(92, 95),  # Mild hypoxia possible
       "Temp": 98.6,  # Afebrile
   }

   exam = {
       "surgical_site": "Healing well, no signs of infection",
       "affected_calf": "Swollen, warm, tender to palpation, positive Homan's sign",
   }

   diagnostic = {
       "D-dimer": "3500 ng/mL (elevated, but expected post-op)",
       "Doppler_ultrasound": "Positive for thrombus in popliteal vein",
       "CTA_chest": "No PE (if dyspnea present)",
   }

   treatment = {
       "STOP": "Enoxaparin 40mg (prophylactic)",
       "START": "Apixaban 10mg PO BID x 7 days, then 5mg BID x 3 months",
       "education": "Bleeding precautions, leg elevation, continue ambulation",
   }
   ```

**When the user says**: "Elderly patient with post-op delirium"

**Claude should**:
1. **Set age 75-85 years** (major risk factor)
2. **Add risk factors**:
   - Pre-existing mild cognitive impairment
   - Polypharmacy (5+ home meds)
   - Poor vision/hearing
   - Lives alone (less stimulation)

3. **Set timeline to POD 2** (peak delirium timing)
4. **Generate delirium presentation**:
   ```python
   presentation = {
       "onset": "POD 2 morning, nursing reports patient confused",
       "mental_status": "Waxing/waning confusion, disoriented to place/time, agitated",
       "sleep": "Reversed sleep-wake cycle, up all night",
       "vitals": "Normal (delirium is clinical diagnosis)",
   }

   workup_to_rule_out_other_causes = {
       "UA": "Negative (no UTI)",
       "CXR": "Clear (no pneumonia)",
       "BMP": "Normal (no metabolic derangement)",
       "O2_sat": "97% RA (no hypoxia)",
   }

   contributing_factors = [
       "Moderate pain (7/10) → increased opioid use",
       "Sleep deprivation (vital signs Q4H, unfamiliar environment)",
       "Polypharmacy (opioids, gabapentin, multiple home meds)",
       "Age >75",
   ]

   management = {
       "non_pharmacologic": [
           "Reorientation (clock, calendar, glasses, hearing aids)",
           "Family presence during day",
           "Sleep hygiene (reduce nighttime interruptions)",
           "Early mobilization with PT",
       ],
       "pharmacologic": [
           "REDUCE opioids (switch to acetaminophen/celecoxib)",
           "AVOID benzodiazepines (paradoxical agitation)",
           "Haloperidol 0.5mg PO Q6H PRN severe agitation (last resort)",
       ],
       "disposition": "Extended hospital stay (5-7 days), likely SNF placement",
   }
   ```

### Coherence Checks

**When generating joint replacement patients, ensure**:

1. **Hemoglobin drop is realistic**:
   ```python
   # Expected blood loss in joint replacement: 500-1000mL
   # Hgb typically drops 2-4 g/dL

   if pre_op_Hgb == 13.5:
       POD_1_Hgb = random(9.5, 11.5)  # 2-4 point drop

       if POD_1_Hgb < 8.0:
           transfusion_indicated = True  # Symptomatic or <8

   # DON'T generate: Pre-op Hgb 13 → POD 1 Hgb 12.5 (too little drop)
   # DON'T generate: Pre-op Hgb 13 → POD 1 Hgb 6 (too much, would need transfusion)
   ```

2. **Pain trajectory makes sense**:
   ```python
   # Pain should IMPROVE over time with PT and meds

   pain_by_POD = {
       0: random(6, 8),  # Highest pain, immediate post-op
       1: random(5, 6),  # Improving
       2: random(4, 5),  # Continuing to improve
       3: random(3, 4),  # Ready for discharge
   }

   # DON'T generate: POD 3 with pain 8/10 (should be improving, or suspect complication)
   ```

3. **PT milestones match POD**:
   ```python
   PT_progression = {
       "POD 0": "Bedside evaluation, dangling legs, may sit in chair",
       "POD 1": "Stand at bedside, transfer practice, ambulate 20-30 feet with walker",
       "POD 2": "Ambulate 50-100 feet, stairs practice (4 steps with rail)",
       "POD 3": "Independent with walker, stairs cleared (8-12 steps), ready for discharge",
   }

   # DON'T generate: POD 1 patient walking 200 feet (too fast)
   # DON'T generate: POD 3 patient bed-bound (should be ambulating by now)
   ```

4. **DVT prophylaxis is ALWAYS included**:
   ```python
   # Every joint replacement patient needs DVT prophylaxis

   if cohort == "joint_replacement":
       assert "enoxaparin" in medications or "rivaroxaban" in medications or "aspirin 325mg" in medications

       # If NO prophylaxis listed, this is an error - joint replacement is HIGH RISK
   ```

5. **Disposition matches patient factors**:
   ```python
   def determine_disposition(age, home_support, baseline_function, complications):
       if complications:
           return "SNF for extended rehab"
       elif age >= 75 and home_support == "limited":
           return "SNF for 2-3 weeks"
       elif baseline_function == "independent" and home_support == "good":
           return "Home with home PT 3x/week"
       else:
           return "SNF for short-term rehab"

   # 82-year-old living alone → SNF likely
   # 65-year-old with spouse, independent baseline → Home likely
   ```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| age_range | range | 60-80 | Patient age range (joint replacement common in elderly) |
| joint_type | enum | knee | Joint being replaced: knee, hip |
| joint_side | enum | right | Laterality: right, left, bilateral |
| bmi_range | range | 25-35 | BMI range (obesity common indication) |
| has_complications | boolean | false | Whether patient develops post-op complications |
| complication_type | enum | none | Complication if any: none, dvt, infection, delirium, bleeding |
| functional_status | enum | independent | Pre-op status: independent, walker, limited |

## Generation Rules

### Demographics
- **Age**: 60-80 years (peak age for joint replacement)
- **Gender**: Female slightly more common (55% for knee, equal for hip)
- **BMI**: 25-35 (obesity major risk factor for osteoarthritis)
- **Occupation**: Often retired or sedentary work

### Conditions

**Primary Indication**:
If joint_type=knee:
- Primary osteoarthritis of knee, unilateral (M17.11 right, M17.12 left)
- OR Bilateral knee osteoarthritis (M17.0) if bilateral

If joint_type=hip:
- Primary osteoarthritis of hip, unilateral (M16.11 right, M16.12 left)
- OR Bilateral hip osteoarthritis (M16.0) if bilateral

**Common Comorbidities** (select 2-4):
- Hypertension (I10) - 65% prevalence
- Type 2 Diabetes (E11.9) - 25% prevalence
- Hyperlipidemia (E78.5) - 50% prevalence
- Obesity (E66.9) - 60% prevalence
- Chronic pain syndrome (G89.29) - very common
- Gastroesophageal reflux (K21.9) - 30% prevalence
- Obstructive sleep apnea (G47.33) - 20% prevalence (if obese)

**Post-Operative Complications** (if has_complications=true):

If complication_type=dvt:
- Deep vein thrombosis, lower extremity (I82.4Y1)
- Possible pulmonary embolism (I26.99)

If complication_type=infection:
- Acute post-procedural infection (T84.50XA)
- Cellulitis of surgical site (L03.115)

If complication_type=delirium:
- Post-operative delirium (F05)
- Common in elderly, multifactorial

If complication_type=bleeding:
- Post-operative hematoma (T81.0XXA)
- Acute blood loss anemia (D62)

### Vital Signs

**Pre-Operative** (baseline):
- **Blood Pressure**: 120-145/70-88 mmHg (may hold BP meds morning of surgery)
- **Heart Rate**: 65-85 bpm (resting)
- **Temperature**: 97.8-98.6 F (afebrile)
- **Respiratory Rate**: 14-18 breaths/min
- **Oxygen Saturation**: 96-100% on room air
- **Pain Score**: 6-8/10 in affected joint (chronic baseline pain)

**Post-Operative Day 0-1** (immediate):
- **Blood Pressure**: 110-140/65-85 mmHg (fluid shifts)
- **Heart Rate**: 75-100 bpm (post-surgical tachycardia normal)
- **Temperature**: 99.0-100.5 F (low-grade fever common POD 1-2)
- **Respiratory Rate**: 16-22 breaths/min
- **Oxygen Saturation**: 93-97% on 2-3L NC (anesthesia effects)
- **Pain Score**: 4-7/10 (controlled with PCA or multimodal analgesia)

**Post-Operative Day 2-3** (improving):
- **Blood Pressure**: 118-138/70-85 mmHg
- **Heart Rate**: 70-90 bpm
- **Temperature**: 98.0-99.5 F (resolving)
- **Oxygen Saturation**: 95-99% on room air
- **Pain Score**: 3-5/10 (improving with PT)

**If Complications**:

DVT/PE:
- Tachycardia (HR 100-120), tachypnea (RR 22-28), hypoxia (O2 88-93%)

Infection:
- Fever (Temp 101-103 F), tachycardia (HR 95-115), surgical site erythema/warmth

Delirium:
- Vital signs may be normal, waxing/waning confusion, agitation

### Laboratory

**Pre-Operative Labs** (within 30 days of surgery):
- **CBC**: WBC 5-10 K/uL, Hgb 12-15 g/dL (may defer if <11), Plt 180-350 K/uL
- **BMP**: All within normal limits, Cr 0.8-1.3 mg/dL (renal clearance for anesthesia)
- **Coagulation**: PT/INR normal (if on warfarin, bridge to LMWH)
- **HbA1c**: <8.0% (if diabetic, optimize pre-op)
- **Urinalysis**: Negative (UTI must be treated before joint replacement)
- **Type & Screen**: In case transfusion needed

**Post-Operative Day 1**:
- **CBC**: WBC 10-15 K/uL (normal post-op elevation), Hgb 9-11 g/dL (blood loss), Plt normal
- **BMP**: May show mild hypokalemia (3.2-3.5), Cr stable or mildly elevated
- **Transfusion Threshold**: Hgb <8 g/dL OR symptomatic (chest pain, tachycardia, hypotension)

**Post-Operative Day 2-3**:
- **CBC**: WBC 8-12 K/uL (trending down), Hgb stable 9-11 g/dL
- **BMP**: Normalizing

**If DVT Suspected**:
- **D-dimer**: Elevated (but not specific post-op)
- **Doppler Ultrasound**: Positive for thrombus in popliteal/femoral vein

**If Infection Suspected**:
- **CBC**: WBC 15-25 K/uL with left shift
- **ESR**: >100 mm/hr (markedly elevated)
- **CRP**: >150 mg/L (markedly elevated)
- **Blood Cultures**: May be positive if bacteremia
- **Wound Culture**: Positive for organism (S. aureus common)

### Medications

**Pre-Operative Home Medications**:
- Ibuprofen 600mg PO TID (for chronic pain) - **HOLD 7 days before surgery**
- Acetaminophen 1000mg PO Q8H PRN pain
- Lisinopril 20mg PO QD (for hypertension) - **HOLD morning of surgery**
- Atorvastatin 40mg PO QHS (continue)
- Metformin 1000mg PO BID (if diabetic) - **HOLD morning of surgery**
- Aspirin 81mg PO QD - **HOLD 7 days before surgery** (per surgeon preference)
- Omeprazole 20mg PO QD (for GERD)

**Pre-Operative Day** (day of surgery):
- Acetaminophen 1000mg PO (pre-emptive analgesia)
- Celecoxib 200mg PO (if no NSAID contraindication)
- Gabapentin 300mg PO (multimodal pain control)
- Scopolamine patch (PONV prophylaxis)
- Antibiotics 30-60 min before incision: Cefazolin 2g IV (or vancomycin if MRSA risk)

**Post-Operative Orders** (standard):

**Multimodal Analgesia**:
- Acetaminophen 1000mg PO Q8H scheduled
- Celecoxib 200mg PO Q12H (if no contraindication)
- Gabapentin 300mg PO TID
- Oxycodone 5-10mg PO Q4H PRN breakthrough pain
- **OR** Hydromorphone PCA: 0.2mg Q10min lockout, no basal rate (POD 0-1)
- Transition to oral opioids POD 1-2

**DVT Prophylaxis** (critical for joint replacement):
- Enoxaparin 40mg SQ Q24H x 10-14 days post-op
- **OR** Rivaroxaban 10mg PO QD x 12-14 days (if oral preferred)
- **OR** Aspirin 325mg PO BID x 6 weeks (if low-risk patient)
- **PLUS** Sequential compression devices (SCDs) while in bed
- Early mobilization (most important)

**GI Prophylaxis**:
- Omeprazole 40mg PO QD (stress ulcer prophylaxis while on NSAID/opioids)

**Other**:
- Ondansetron 4mg IV Q6H PRN nausea
- Docusate 100mg PO BID (stool softener for opioid-induced constipation)
- Resume home meds POD 1 (metformin once eating, lisinopril once stable)

**If Complication - DVT**:
- **STOP** prophylactic anticoagulation
- **START** therapeutic anticoagulation:
  - Enoxaparin 1mg/kg SQ Q12H
  - OR Apixaban 10mg PO BID x 7 days, then 5mg BID x 3-6 months
- Monitor for bleeding

**If Complication - Infection**:
- Vancomycin 15mg/kg IV Q12H (for MRSA coverage)
- PLUS Ceftriaxone 2g IV Q24H (gram-negative coverage)
- Adjust based on culture results
- May require surgical washout/debridement

### Timeline

**Pre-Operative Phase**:
- 4-6 weeks before: Orthopedic surgery consultation, joint X-rays, surgery scheduled
- 3-4 weeks before: Pre-operative appointment with PCP for medical clearance
- 3-4 weeks before: Labs drawn (CBC, BMP, HbA1c if diabetic)
- 2 weeks before: Pre-admission testing (PAT) appointment
- 2 weeks before: Anesthesia evaluation, review risks
- 1 week before: STOP NSAIDs, aspirin (if instructed)
- 1 day before: Pre-op instructions, NPO after midnight
- Day of surgery: Arrive 2 hours before scheduled procedure

**Day of Surgery (POD 0)**:
- 0600: Patient arrives, check-in, IV placed
- 0630: Pre-op area, vitals, nursing assessment
- 0700: Anesthesia pre-op evaluation
- 0730: Surgical site marked, consent confirmed
- 0745: Prophylactic antibiotics (cefazolin 2g IV)
- 0800: To OR, spinal anesthesia placed
- 0830: Incision made
- 0830-1030: Total knee arthroplasty performed (2 hours)
- 1030: Closure, dressing applied
- 1045: To PACU (post-anesthesia care unit)
- 1200: Alert, stable, pain controlled, to orthopedic floor
- 1400: PT evaluation at bedside, assess mobility
- 1600: OOB to chair with PT assistance
- 1800: Hemovac drain output 200mL, ice to knee
- 2200: Pain 6/10, PCA utilized, sleep

**Post-Operative Day 1**:
- 0600: Vitals stable, pain 5/10
- 0800: Labs drawn (CBC shows Hgb 9.8, down from 13.2 pre-op)
- 0900: PT session - stand at bedside, transfer practice
- 0900: Drain removed (output <30mL/8h)
- 1200: Urinary catheter removed (placed intra-op)
- 1400: PT session - ambulate 20 feet with walker
- 1600: Transition from PCA to oral opioids
- 1800: Tolerating regular diet
- 2000: Pain 4/10 with oral medications

**Post-Operative Day 2**:
- 0800: PT session - ambulate 50 feet, stairs practice
- 0900: Case management evaluation for discharge planning
- 1000: Surgical dressing changed, incision clean/dry/intact
- 1200: OT evaluation - ADL training
- 1400: PT session - ambulate 100 feet, independent with walker
- 1600: Discharge planning meeting - home with home PT vs SNF
- 1800: Patient meets discharge criteria

**Post-Operative Day 3** (typical discharge):
- 0800: Final PT evaluation - independent with walker, stairs cleared
- 0900: Discharge teaching - wound care, activity restrictions, medications
- 1000: Prescriptions given:
  - Oxycodone 5mg PO Q6H PRN pain x 2 weeks
  - Acetaminophen 1000mg Q8H x 4 weeks
  - Celecoxib 200mg Q12H x 2 weeks
  - Enoxaparin 40mg SQ daily x 10 days (home injections)
  - Docusate 100mg BID PRN constipation
- 1030: Follow-up appointments scheduled:
  - Orthopedic surgeon in 2 weeks (suture removal)
  - Home PT 3x/week x 6 weeks
  - OR discharge to skilled nursing facility (SNF) for 2-3 weeks
- 1100: Discharge home with walker and elevated toilet seat

**Outpatient Follow-Up**:
- 2 weeks: Post-op visit, suture/staple removal, wound check
- 6 weeks: X-ray, assess early healing, advance weight-bearing
- 3 months: Progress check, may discharge from orthopedics
- 6-12 months: Final assessment, range of motion, return to activities

**If Complication - DVT on POD 5**:
- POD 5: Patient at home, calls with left calf pain, swelling
- Same day: Return to ED
- ED: Doppler ultrasound positive for popliteal DVT
- ED: Start apixaban 10mg PO BID, D/C enoxaparin
- ED: Discharge home, follow up with PCP in 2 days
- Ongoing: Anticoagulation x 3 months minimum

## Variations

### Variation: Bilateral Knee Replacement
Patient undergoing simultaneous bilateral total knee arthroplasty.
- joint_side: bilateral
- **Surgery Time**: 3-4 hours (longer than unilateral)
- **Blood Loss**: Greater (Hgb may drop to 8-9 g/dL, transfusion more common)
- **Pain**: More severe initially (7-9/10)
- **Rehabilitation**: Slower, more challenging
- **Hospital Stay**: Typically 4-5 days (longer than unilateral)
- **Disposition**: More likely to require SNF for rehab
- **Complications**: Higher risk of DVT, delirium, blood loss

### Variation: Revision Joint Replacement
Patient with failed prior joint replacement requiring revision surgery.
- **Indication**: Prosthetic loosening (T84.039A) or infection (T84.50XA)
- **Surgery Complexity**: Higher, longer operative time (3-5 hours)
- **Blood Loss**: Greater, transfusion common
- **Infection Risk**: Higher, may require 2-stage revision if infected
- **Hospital Stay**: 5-7 days
- **Complications**: More frequent (infection, instability, dislocation)
- **Prognosis**: Less predictable than primary arthroplasty

### Variation: Post-Op Delirium in Elderly Patient
Elderly patient develops post-operative delirium.
- age_range: 75-85 years
- complication_type: delirium
- **Risk Factors**: Age >75, pre-existing cognitive impairment, poor vision/hearing, polypharmacy
- **POD 2 Presentation**: Waxing/waning confusion, disorientation, agitation, sleep-wake disturbance
- **Workup**: Rule out infection (UA, CXR), metabolic (BMP), hypoxia (ABG)
- **Contributing Factors**: Pain, opioids, sleep deprivation, unfamiliar environment
- **Management**:
  - Non-pharmacologic: Reorientation, family presence, sleep hygiene, minimize interruptions
  - Minimize opioids/benzodiazepines
  - Treat underlying causes
  - Low-dose haloperidol 0.5-1mg PO/IV Q6H PRN severe agitation (last resort)
- **Disposition**: Extended hospital stay (5-7 days), likely SNF placement

### Variation: Post-Op Surgical Site Infection
Patient develops early post-operative joint infection.
- complication_type: infection
- **POD 7-10 Presentation**: Increasing pain, fever, wound drainage, erythema
- **At home**: Calls surgeon's office with concerns
- **Return to hospital**: Admitted for workup
- **Labs**: WBC 18, ESR 120, CRP 200
- **Imaging**: X-ray may show soft tissue swelling, effusion
- **Arthrocentesis**: Joint aspiration shows 50,000 WBCs, culture grows S. aureus
- **Management**:
  - Admit for IV antibiotics (vancomycin + ceftriaxone)
  - Orthopedic surgery: Irrigation and debridement (I&D) in OR
  - Possible removal of prosthesis if deep infection
  - 6 weeks IV antibiotics
  - May require 2-stage revision (remove prosthesis, antibiotics, re-implant later)
- **Outcome**: Prolonged recovery, higher morbidity

### Variation: Outpatient Joint Replacement (Same-Day Discharge)
Low-risk patient selected for outpatient arthroplasty program.
- age_range: 55-70 years
- bmi_range: 20-30 (not obese)
- functional_status: independent
- has_complications: false
- **Selection Criteria**: ASA class 1-2, good home support, lives <30 min from hospital
- **Pre-op Optimization**: Extensive education, home preparation (bathroom rails, etc.)
- **Anesthesia**: Spinal with long-acting local anesthetic (bupivacaine)
- **Surgery**: Morning case, starts 0730
- **PACU**: Extended recovery, PT evaluation before discharge
- **Discharge Criteria Met by 1600**: Pain <4/10, ambulating with walker, voiding, tolerating PO, stable vitals
- **Discharge Same Day**: Home with home PT starting next day, close phone follow-up
- **Advantages**: Lower cost, patient preference, lower infection risk
- **Risks**: Must have good support, 24h nurse hotline access

## Example Requests and Interpretations

### Example 1: Simple Request - "Generate a knee replacement patient"

**User says**: "Generate a knee replacement patient"

**Claude interprets**:
- Joint type: knee (specified)
- POD: Not specified → default to POD 2 (typical teaching case, shows progression)
- Age: 60-80 range (typical for joint replacement)
- Complications: None (uncomplicated case)
- Disposition: To be determined based on age/support

**Claude generates**:

**Patient**: 72-year-old female with right total knee arthroplasty, POD 2

**History**: 4-year history of progressive right knee pain from osteoarthritis, failed conservative management (PT, NSAIDs, intra-articular injections). Right TKA performed 2 days ago.

**PMH**: Hypertension, hyperlipidemia, obesity, chronic pain syndrome, GERD

**Pre-Op**: Cleared for surgery, HbA1c N/A (non-diabetic), UA negative, Hgb 13.2 g/dL

**Surgery (POD 0)**: Right TKA performed under spinal anesthesia, uncomplicated, 2h operative time. Cefazolin 2g IV given pre-incision. Hemovac drain placed.

**POD 1**: Drain removed (output <30mL/8h), Foley removed, ambulated 25 feet with walker, transitioned from PCA to oral pain meds. Hgb 10.1 g/dL (down from 13.2, no transfusion needed).

**POD 2 (Current)**:
- **Vitals**: BP 128/76, HR 78, Temp 98.6 F, RR 16, O2 97% RA
- **Pain**: 4/10 with oral medications (acetaminophen 1000mg Q8H, celecoxib 200mg Q12H, gabapentin 300mg TID, oxycodone 5mg PRN)
- **PT Session This Morning**: Ambulated 100 feet with walker, practiced stairs x 4 steps with rail, independent with transfers
- **Incision**: Clean, dry, intact - no erythema, drainage, or warmth
- **Labs**: Hgb stable at 10.0 g/dL, WBC 9.5 K/uL (trending down from 12 on POD 1)
- **Case Management**: Evaluated for discharge planning - patient lives with husband, has good home support, home PT arranged 3x/week starting POD 4
- **Plan**: Discharge POD 3 to home with home PT, follow-up with surgeon in 2 weeks

**Medications**:
- Enoxaparin 40mg SQ Q24H x 10 days (DVT prophylaxis) - teaching patient/husband injection technique
- Acetaminophen 1000mg PO Q8H scheduled
- Celecoxib 200mg PO Q12H
- Gabapentin 300mg PO TID
- Oxycodone 5mg PO Q4H PRN pain
- Docusate 100mg PO BID (stool softener)
- Omeprazole 40mg PO QD
- Home meds resumed: Lisinopril 20mg QD, atorvastatin 40mg QHS

---

### Example 2: Severity-Specific - "Generate a patient with post-op DVT"

**User says**: "Generate a patient with post-op DVT"

**Claude interprets**:
- Complication type: DVT (specified)
- Timeline: POD 5-10 (DVT typically occurs after discharge)
- Setting: Patient at home, returns to ED
- Initial surgery: Was uncomplicated, patient WAS on DVT prophylaxis (DVT can still occur despite prophylaxis - it's not 100% effective)

**Claude generates**:

**Patient**: 68-year-old male, POD 7 after left total hip arthroplasty, presenting to ED with left calf pain and swelling

**Chief Complaint**: "Left calf pain and swelling for 2 days"

**HPI**: Patient underwent uncomplicated left THA 7 days ago for severe hip osteoarthritis. Discharged POD 3 to home with home PT. Was doing well until 2 days ago (POD 5) when he developed progressive left calf pain - different character from surgical pain. Calf is swollen and warm. Also notes mild shortness of breath with walking. Concerned about blood clot. **Reports compliance with enoxaparin 40mg SQ daily injections** (due to continue x 10 more days).

**PMH**: Hypertension, Type 2 diabetes (well-controlled), obesity, chronic back pain

**Surgical History**: Left THA POD 7 (for primary hip OA)

**Initial Post-Op Course**: Uncomplicated - discharged POD 3 ambulating with walker, pain controlled, incision healing well.

**ED Presentation**:

**Vitals**: BP 142/88, HR 98, Temp 98.6 F, RR 20, O2 94% on room air

**Physical Exam**:
- **General**: Mildly uncomfortable, mildly tachypneic
- **Surgical site**: Left hip incision healing well, no erythema/drainage, no warmth
- **Left hip ROM**: Mild pain with movement (expected post-op), no instability
- **Left calf**: Swollen (3cm larger circumference than right), warm to touch, tender to palpation, positive Homan's sign
- **Lungs**: Clear bilaterally, no wheezing/rales
- **Cardiac**: Regular rate, mildly tachycardic

**Labs**:
- **D-dimer**: 3800 ng/mL (markedly elevated, but non-specific post-op)
- **CBC**: WBC 8.2 K/uL, Hgb 11.5 g/dL (stable from discharge), Plt 285 K/uL
- **BMP**: Within normal limits
- **Troponin**: <0.01 (negative)

**Imaging**:
- **Doppler Ultrasound Left Lower Extremity**: **Positive for non-occlusive thrombus in left popliteal vein and posterior tibial vein**
- **CTA Chest**: **No pulmonary embolism** (ordered due to mild dyspnea/hypoxia - reassuring)

**Diagnosis**: Acute deep vein thrombosis (DVT) of left lower extremity, post-operative (I82.4Y1)

**Risk Factors**: Recent major orthopedic surgery (high risk), age 68, obesity, immobility post-op

**Treatment Plan**:
1. **STOP prophylactic anticoagulation**: Discontinue enoxaparin 40mg daily
2. **START therapeutic anticoagulation**:
   - Apixaban 10mg PO BID x 7 days, then 5mg PO BID
   - Duration: Minimum 3 months (provoked DVT from surgery)
3. **Supportive care**:
   - Leg elevation when sitting/lying
   - Compression stockings (knee-high, 20-30 mmHg)
   - **Continue ambulation** (walking helps, bed rest is harmful)
4. **Education**:
   - Bleeding precautions (avoid falls, monitor for blood in stool/urine)
   - Signs of PE to watch for (chest pain, severe SOB, syncope → call 911)
   - Medication adherence critical

**Disposition**: Discharge home from ED (no PE, hemodynamically stable)

**Follow-Up**:
- PCP in 2 days: Monitor for PE symptoms, assess bleeding risk
- Repeat Doppler ultrasound in 1 week: Assess clot progression/stability
- Continue home PT, advance activities as tolerated
- Orthopedic surgeon follow-up in 1 week (originally scheduled for 2 weeks, moved up)

**Prognosis**: Good - most post-surgical DVTs resolve with anticoagulation, low recurrence risk after completing treatment

---

### Example 3: Timeline-Specific - "POD 0 knee replacement patient"

**User says**: "Generate a POD 0 knee replacement patient, just arrived on the floor from PACU"

**Claude interprets**:
- POD: 0 (day of surgery, specified)
- Status: Just out of PACU (post-anesthesia care unit), recently arrived on orthopedic floor
- Timing: Afternoon/early evening (surgery typically AM, PACU 2-3h)
- Pain: Higher (6-8/10), may still have PCA running
- Mobility: Limited - bedside evaluation only

**Claude generates**:

**Patient**: 65-year-old female, POD 0 after right total knee arthroplasty, just transferred to orthopedic floor from PACU

**Time**: 1400 (2:00 PM) - patient arrived on floor 30 minutes ago

**Surgical Procedure** (This Morning):
- **Surgery**: Right total knee arthroplasty
- **Indication**: Severe right knee osteoarthritis, bone-on-bone medial compartment
- **Anesthesia**: Spinal anesthesia with sedation
- **Operative Time**: 0800-1000 (2 hours)
- **Intra-op Course**: Uncomplicated, EBL 400mL, cemented prosthesis placed
- **Prophylactic Antibiotics**: Cefazolin 2g IV given at 0730 (30 min before incision)
- **PACU**: 1000-1330, pain controlled, stable vitals, alert and oriented

**Current Status (1430)**:

**Vitals**: BP 118/72, HR 88, Temp 99.2 F (low-grade fever normal POD 0), RR 18, O2 96% on 2L NC

**Pain**: 7/10 in right knee at rest, 8/10 with movement

**Mental Status**: Alert, oriented x3, conversing appropriately, slightly drowsy from anesthesia

**Right Knee**:
- **Dressing**: Bulky compression dressing in place, clean and dry, no visible drainage
- **Hemovac Drain**: In place, draining serosanguinous fluid - **output 180mL since surgery** (expected)
- **Ice**: Applied to knee for pain/swelling
- **Elevation**: Knee elevated on pillows
- **Neurovascular Check**: Distal pulses 2+ (dorsalis pedis, posterior tibial), cap refill <2 sec, toes warm/pink, able to wiggle toes, sensation intact

**Lines/Tubes**:
- **IV**: Left forearm 18g, infusing LR at 100mL/h
- **PCA**: Hydromorphone PCA connected - 0.2mg Q10min lockout, no basal, patient using appropriately
- **Foley Catheter**: In place (placed intra-op), draining clear yellow urine
- **SCDs**: Sequential compression devices on both calves (DVT prophylaxis)

**Activity**:
- Bed rest currently
- PT consulted - will evaluate at bedside this afternoon (around 1600)
- Goal: Dangle legs at bedside, assess ability to sit in chair

**Diet**: Clear liquids, advancing to regular diet as tolerated (nausea assessment)

**Post-Op Orders**:

**Pain Management** (Multimodal):
- Hydromorphone PCA 0.2mg Q10min lockout (current)
- Acetaminophen 1000mg PO Q8H scheduled (first dose at 1400)
- Celecoxib 200mg PO Q12H (first dose at 1800)
- Gabapentin 300mg PO TID (first dose at 1800)
- Ice to knee Q2H

**DVT Prophylaxis**:
- SCDs to bilateral lower extremities (in place)
- Enoxaparin 40mg SQ Q24H - **first dose at 1800** (6h post-op per protocol)
- Early mobilization with PT

**GI Prophylaxis**:
- Omeprazole 40mg PO QD (first dose tomorrow AM)
- Docusate 100mg PO BID starting tonight

**Antiemetics**:
- Ondansetron 4mg IV Q6H PRN nausea

**Antibiotics**:
- Post-op antibiotics not continued (single pre-op dose sufficient per protocol)

**Labs**: CBC, BMP in AM (POD 1)

**Plan**:
- **1600**: PT bedside evaluation - assess leg dangling, transfers
- **1800**: First enoxaparin dose, evening meds (celecoxib, gabapentin)
- **2200**: Night vitals, pain reassessment
- **POD 1 Goals**: Remove drain if output <30mL/8h, remove Foley, transition from PCA to oral opioids, ambulate with PT

**Current Nursing Interventions**:
- Vital signs Q4H
- Neurovascular checks Q2H x 24h
- Pain assessment Q2H
- I&O monitoring (Foley output)
- Drain output Q4H
- Incentive spirometry Q2H while awake (prevent atelectasis)
- Fall precautions (post-anesthesia, on PCA)

---

### Example 4: Complication-Specific - "Elderly patient with post-op delirium"

**User says**: "Generate an elderly patient with post-op delirium after hip replacement"

**Claude interprets**:
- Age: 75-85 (elderly, major delirium risk factor)
- Joint: Hip replacement (specified)
- Complication: Delirium (specified)
- POD: 2 (peak delirium timing, specified by typical onset)
- Risk factors: Should include age, polypharmacy, cognitive impairment, opioids

**Claude generates**:

**Patient**: 82-year-old male, POD 2 after left total hip arthroplasty, developed acute confusion overnight

**Chief Concern** (Nursing Report): "Patient very confused this morning, doesn't know where he is, agitated, trying to get out of bed"

**Background**:

**Surgery**: Left THA performed 2 days ago for severe hip osteoarthritis

**PMH**:
- Hypertension
- Mild cognitive impairment (baseline MMSE 24/30, lives independently with wife's help)
- Hard of hearing (wears hearing aids, but didn't bring to hospital)
- Cataracts (decreased vision)
- BPH (benign prostatic hyperplasia)
- GERD

**Pre-Op Baseline**: Independent with ADLs, walks with cane, drives, manages medications with wife's assistance. Oriented x3, occasionally forgets names/words.

**Post-Op Course**:

**POD 0-1**: Unremarkable - pain controlled with PCA, ambulated 20 feet with PT on POD 1, appropriate/oriented

**POD 2 (Current) - Delirium Onset**:

**Timeline**:
- **0200** (overnight): Nurse found patient trying to climb out of bed, disoriented, said "I need to go to work" (retired 20 years ago)
- **0400**: Agitated, pulling at IV, yelling for wife
- **0600**: Waxing/waning - periods of calm, then agitation
- **0800** (current): Disoriented to place/time, doesn't recognize daughter at bedside

**Current Mental Status**:
- **Alertness**: Awake, hypervigilant
- **Orientation**: Disoriented to place and time (thinks he's at home, thinks it's 1995), oriented to person (knows his name)
- **Attention**: Extremely poor - cannot focus on questions
- **Speech**: Rambling, tangential, perseverating on "need to go to work"
- **Mood**: Anxious, agitated
- **Behavior**: Restless, attempting to get out of bed, pulling at lines/wires
- **Hallucinations**: Reports seeing "bugs on the wall" (visual hallucinations common in delirium)
- **Sleep**: Nurse reports sleep-wake reversal - up most of night, sleeping during day

**Vitals**: BP 152/88 (elevated from baseline 130s), HR 92, Temp 98.8 F, RR 18, O2 96% RA

**Physical Exam**:
- **General**: Elderly male, agitated, not following commands consistently
- **HEENT**: Not wearing hearing aids (can't find them), decreased vision without glasses
- **Neurologic**: Waxing/waning alertness, disoriented, otherwise non-focal
- **Surgical site**: Left hip incision clean/dry/intact, no erythema
- **Lungs**: Clear (no pneumonia)
- **Abdomen**: Soft, non-tender (bowel sounds present)

**Delirium Workup** (Rule Out Underlying Causes):

**Labs**:
- **CBC**: WBC 10.2 K/uL (normal post-op), Hgb 10.5 g/dL (stable)
- **BMP**: Na 138, K 3.8, Cl 102, CO2 24, BUN 22, Cr 1.1 (baseline), Glucose 118
- **Urinalysis**: Negative (no UTI)
- **ABG**: Not indicated (O2 sat normal, no respiratory symptoms)

**Imaging**:
- **CXR**: Clear, no infiltrate/effusion (no pneumonia)

**Conclusion**: **No acute medical cause identified** - delirium is multifactorial

**Contributing Risk Factors**:
1. **Age 82** (major risk factor)
2. **Baseline mild cognitive impairment** (predisposes to delirium)
3. **Sensory impairment**: No hearing aids, no glasses (disoriented without cues)
4. **Opioid use**: Oxycodone 10mg Q4H (total 60mg in last 24h - high for elderly)
5. **Sleep deprivation**: Vitals Q4H, unfamiliar environment, hospital noise
6. **Polypharmacy**: Opioids + gabapentin + home meds (8 total medications)
7. **Pain**: 6/10 (undertreated pain can worsen delirium)
8. **Immobility**: Limited mobility post-op

**Management Plan**:

**Non-Pharmacologic (First-Line)**:
1. **Re-orientation**:
   - Find hearing aids, glasses → improve sensory input
   - Clock, calendar visible at bedside
   - Frequent re-orientation by staff ("Mr. Smith, you're in the hospital, you had hip surgery")
   - Family presence (daughter to stay during day)

2. **Sleep Hygiene**:
   - Reduce nighttime interruptions (cluster vital signs, labs in AM only)
   - Lights off at night, open blinds during day
   - Quiet environment

3. **Early Mobilization**:
   - PT twice daily (walking helps cognitive function)
   - Out of bed to chair for meals

4. **Avoid Physical Restraints** (worsens agitation)
   - 1:1 sitter if needed for safety
   - Move to room closer to nurses' station

**Pharmacologic Adjustments**:
1. **Reduce Opioids** (major contributor):
   - STOP scheduled oxycodone
   - Increase acetaminophen to 1000mg Q6H (around the clock)
   - Add ice, elevation
   - Oxycodone 5mg Q6H PRN only (half previous dose)

2. **Avoid Benzodiazepines** (paradoxical agitation in elderly)

3. **If Severe Agitation** (safety risk):
   - Haloperidol 0.5mg PO/IV Q6H PRN severe agitation (lowest dose, last resort)
   - Monitor QTc on EKG

**Disposition**:
- Extended hospital stay likely (5-7 days vs typical 3)
- Discharge to **skilled nursing facility (SNF)** for rehabilitation (cannot go home with delirium)
- Delirium may take days-weeks to fully resolve

**Family Discussion**:
- Explain delirium is common post-op, usually resolves
- Reassure this is not permanent dementia (though may unmask underlying cognitive decline)
- Importance of non-pharmacologic interventions
- SNF placement temporary - goal is to return home once delirium clears and PT goals met

---

### Example 5: Disposition-Specific - "Patient being discharged to SNF after joint replacement"

**User says**: "Generate a patient being discharged to SNF after knee replacement"

**Claude interprets**:
- Joint: Knee replacement (specified)
- POD: 3-4 (typical discharge timing)
- Disposition: SNF (specified) - need to identify why (age, limited support, complications, or functional status)
- Status: Medically stable, meets discharge criteria from hospital, but needs extended rehab

**Claude generates**:

**Patient**: 78-year-old female, POD 4 after bilateral total knee arthroplasty, being discharged to skilled nursing facility (SNF) for rehabilitation

**Background**:

**Surgery**: Bilateral TKA performed 4 days ago for severe bilateral knee osteoarthritis

**PMH**: Hypertension, Type 2 diabetes (well-controlled), obesity (BMI 33), osteoporosis, chronic pain

**Social History**:
- **Lives**: Alone in 2-story home (bedrooms upstairs)
- **Functional Baseline**: Independent with ADLs, ambulates with cane, grocery shopping with assistance
- **Support**: Daughter lives 45 minutes away, works full-time (cannot provide daily care)

**Why SNF vs Home**:
1. **Bilateral surgery** (more challenging rehab than unilateral)
2. **Age 78** (slower recovery)
3. **Limited home support** (lives alone, daughter not nearby)
4. **Home not accessible** (stairs to bedroom, bathroom)
5. **Need for intensive PT** (bilateral = more intensive rehab needs)

**Hospital Course**:

**POD 0-1**: Bilateral TKA performed, spinal anesthesia, uncomplicated. Significant pain initially (8/10), managed with PCA. Blood loss greater than unilateral (Hgb dropped from 12.8 to 9.2). Drains removed POD 1, Foley removed POD 1.

**POD 2-3**: Transitioned to oral pain meds. PT challenging due to bilateral pain - ambulated 40 feet with walker and significant assist on POD 2, 75 feet with walker and minimal assist POD 3. Pain 6/10 with movement.

**POD 4 (Discharge Day)**:

**Current Status**:
- **Pain**: 5/10 at rest, 7/10 with PT (still significant due to bilateral surgery)
- **Mobility**: Ambulates 100 feet with walker, requires standby assist for safety, bilateral pain limits endurance
- **Stairs**: Not yet cleared (too painful, would need to do both legs)
- **ADLs**: Needs assist with bathing (cannot reach feet), dressing lower body
- **Vitals**: Stable - BP 138/82, HR 76, Temp 98.4 F, O2 97% RA

**Physical Exam**:
- **Bilateral Knees**: Incisions clean/dry/intact, no erythema/drainage/warmth, ROM limited by pain (flexion 80° bilaterally - needs improvement)
- **General**: Ambulatory with walker, slow gait, guarding both knees

**Labs (POD 3)**:
- **CBC**: WBC 9.8 K/uL, Hgb 9.5 g/dL (stable, no transfusion needed), Plt 298 K/uL
- **BMP**: Within normal limits

**Discharge Planning Meeting** (POD 3):
- **Case Manager**, **Patient**, **Daughter**, **PT**, **Surgeon** present
- **Options Discussed**:
  - Home with 24/7 caregiver (patient declined, too expensive)
  - Home with daughter moving in (daughter cannot take leave from work)
  - **SNF for short-term rehab** (recommended, patient agreed)

**SNF Selection**:
- Patient/daughter chose "Oakwood Rehabilitation Center" (3 miles from daughter's work, good reputation)
- **Anticipated Length of Stay**: 2-3 weeks
- **Goals**: Independent ambulation with walker, stairs clearance, independent ADLs, pain control

**Discharge Medications** (Going to SNF):

**Pain Management**:
- Acetaminophen 1000mg PO Q8H scheduled
- Celecoxib 200mg PO Q12H
- Gabapentin 300mg PO TID
- Oxycodone 10mg PO Q6H PRN pain (higher dose due to bilateral surgery)

**DVT Prophylaxis**:
- Enoxaparin 40mg SQ Q24H x 10 more days (total 14 days)

**Home Medications Resumed**:
- Lisinopril 20mg PO QD
- Metformin 1000mg PO BID
- Atorvastatin 40mg PO QHS
- Alendronate 70mg PO Q weekly (osteoporosis)

**Other**:
- Omeprazole 40mg PO QD
- Docusate 100mg PO BID PRN constipation

**Discharge Instructions**:

**Activity**:
- Weight-bearing as tolerated with walker
- PT at SNF daily
- NO driving until cleared by surgeon (6 weeks)
- Use walker at all times

**Wound Care**:
- Dressings will be changed by SNF nursing
- Keep incisions clean and dry, no soaking
- Watch for signs of infection (increased pain, redness, drainage, fever)

**Medications**:
- All medications will be managed by SNF
- Enoxaparin injections by SNF nursing staff

**Follow-Up Appointments**:
- **Orthopedic Surgeon**: 2 weeks (at surgeon's office - daughter will transport from SNF)
  - Suture/staple removal
  - X-rays to assess hardware position
  - Wound check
- **PCP**: 4 weeks (after discharge from SNF to home)

**SNF Orders**:

**Therapy Orders**:
- **PT**: Daily (5-7 days/week)
  - Gait training, strengthening, ROM exercises
  - Stairs training (critical for home discharge)
  - Goal: Independent with walker, stairs x 12 steps
- **OT**: 3x/week
  - ADL training (bathing, dressing, toileting)
  - Adaptive equipment training

**Nursing Orders**:
- Vital signs daily
- Wound assessment daily
- Enoxaparin 40mg SQ daily (nursing to administer)
- Pain assessment Q4H, goal <5/10

**Labs**: None needed (stable)

**Discharge Criteria from SNF** (Goals for Home):
1. Independent ambulation with walker (no assist needed)
2. Able to navigate stairs safely (minimum 8 steps for home)
3. Independent with ADLs or minimal assist
4. Pain controlled on oral meds (<4/10)
5. Safe home environment prepared (bathroom rails installed, bedroom moved to first floor temporarily)

**SNF Discharge Plan** (Anticipated):
- **Week 2-3**: Re-assess home readiness
- If ready: Discharge home with home PT 2-3x/week x 4 weeks
- If not ready: Extended SNF stay (up to 4 weeks)

**Prognosis**: Good - bilateral TKA has excellent long-term outcomes, but recovery is slower and more challenging than unilateral. With intensive PT at SNF, expect patient to achieve home discharge goals in 2-3 weeks.

## Clinical Reasoning Patterns

### Pre-Operative Optimization

**Medical Clearance Checklist**:
- Cardiac risk assessment (Revised Cardiac Risk Index)
- If high-risk cardiac: Consider stress test, cardiology clearance
- Diabetes: HbA1c <8% (ideally <7%), optimize glucose control
- Hypertension: BP <160/100 (hold ACE-I morning of surgery)
- Anticoagulation: Bridge if on warfarin for AFib (stop 5 days prior, start LMWH)
- Nutrition: Optimize if malnourished (albumin >3.0)
- Anemia: Treat if Hgb <12 (consider iron, EPO)
- Smoking: Cessation counseling (increases infection, delayed healing)

**Medication Management**:
- **STOP 7 days before**: NSAIDs, aspirin (bleeding risk)
- **STOP morning of**: ACE-I/ARB (hypotension risk), metformin (lactic acidosis risk)
- **CONTINUE**: Beta-blockers, statins, antihypertensives (except ACE-I)
- **BRIDGE if needed**: Warfarin (for mechanical valves, high-risk AFib)

### DVT Prophylaxis Strategy

**Risk Assessment**:
- Joint replacement = **HIGH RISK** for VTE (10-40% without prophylaxis)
- Additional risk factors: Age >60, obesity, prolonged immobility, cancer, prior VTE

**Prophylaxis Options** (AAOS guidelines):
1. **Pharmacologic**:
   - LMWH (enoxaparin 40mg SQ daily) x 10-14 days - most common
   - DOACs (rivaroxaban 10mg daily, apixaban 2.5mg BID) x 12-14 days - oral convenience
   - Warfarin (INR 2-3) - less common, requires monitoring
   - Aspirin 325mg BID x 6 weeks - option for low-risk patients

2. **Mechanical**:
   - Sequential compression devices (SCDs) - use in hospital
   - TED stockings - limited evidence

3. **Early Mobilization** - MOST IMPORTANT

**Duration**: Minimum 10-14 days, extended to 35 days for hip replacement

### Post-Operative Pain Management

**Multimodal Analgesia** (opioid-sparing):
1. **Acetaminophen** 1000mg Q8H scheduled (baseline)
2. **NSAIDs** Celecoxib 200mg Q12H (if no contraindication)
3. **Gabapentinoids** Gabapentin 300mg TID (neuropathic component)
4. **Local Anesthesia** Periarticular injection in OR (bupivacaine, ropivacaine)
5. **Opioids** Short-acting PRN for breakthrough (oxycodone, hydromorphone)

**Avoid**:
- Long-acting opioids (unnecessary for acute pain)
- Excessive opioids (delirium, constipation, falls, respiratory depression)

**Goal**: Pain <4/10 at rest, <6/10 with PT

### Infection Prevention

**Strategies**:
- Pre-op antibiotics 30-60 min before incision (cefazolin 2g)
- Re-dose if surgery >4 hours
- Nasal decontamination if MRSA carrier (mupirocin)
- Chlorhexidine shower night before and morning of surgery
- Strict sterile technique in OR
- Minimize OR traffic
- Tight glucose control perioperatively (<180 mg/dL)
- Normothermia (warming blankets)
- Wound closed in layers, waterproof dressing

**If Infection Suspected**:
- High clinical suspicion: Pain out of proportion, fever, wound drainage
- Labs: WBC, ESR (>100 suspicious), CRP (>100 suspicious)
- Arthrocentesis: Synovial fluid cell count, culture
- Criteria for PJI: WBC >10,000 in joint fluid, positive culture

### Discharge Planning

**Discharge Criteria**:
- Pain controlled on oral medications (<5/10)
- Ambulating safely with assistive device
- Adequate ROM for function (90° knee flexion for transfers)
- Voiding without catheter
- Tolerating PO intake
- Incision stable
- Vitals stable
- Safe discharge plan

**Disposition Options**:
1. **Home** - preferred if able
   - Requires: Safe home environment, support person, able to perform ADLs
   - Arrange: Home PT 3x/week, DME (walker, toilet riser)
2. **Skilled Nursing Facility (SNF)** - short-term rehab
   - Indications: Limited home support, need for intensive PT, medical complexity
   - Duration: 2-3 weeks typically
3. **Acute Rehab** - rare
   - For patients with major complications, prolonged recovery needs

**Post-Discharge Monitoring**:
- Wound check at 2 weeks (suture/staple removal)
- X-ray at 6 weeks (assess component position, early healing)
- Final assessment 3-6 months (ROM, return to activities)

## References

- American Academy of Orthopaedic Surgeons (AAOS) Clinical Practice Guidelines on VTE Prophylaxis, 2021
- American Society of Anesthesiologists (ASA) Perioperative Management Guidelines, 2023
- CDC Guideline for Prevention of Surgical Site Infection, 2017
- Journal of Arthroplasty - Prosthetic Joint Infection Management, 2023

## Validation Rules

| Rule | Requirement | Example |
|------|-------------|---------|
| Procedure code | Valid CPT | 27447 (TKA), 27130 (THA) |
| DRG | Valid MS-DRG | 469 (major joint w/ MCC), 470 (w/o MCC) |
| ASA class | I-VI | ASA II |
| BMI | Typically <40 for elective | 32.5 |
| Hemoglobin | Pre-op baseline | 13.5 g/dL |
| INR | <1.5 for surgery | 1.1 |
| LOS | Days, typically 1-3 | 2 days |
| Discharge disposition | home, SNF, rehab | "home with PT" |

### Business Rules

- **Pre-op Optimization**: BMI <40, A1C <8%, smoking cessation, dental clearance
- **DVT Prophylaxis**: Required post-op; aspirin, LMWH, or direct oral anticoagulant
- **Antibiotic Prophylaxis**: Pre-incision cefazolin (or vancomycin if MRSA)
- **Blood Management**: Tranexamic acid; consider autologous blood donation
- **Pain Management**: Multimodal approach; regional blocks preferred
- **Early Mobilization**: Physical therapy POD 0-1
- **Discharge Criteria**: Pain controlled, mobilizing safely, wound intact
- **Bundled Payment**: 90-day episode includes surgery, hospital, and post-acute care

## Related Skills

### PatientSim Cohorts

- [SKILL.md](SKILL.md) - PatientSim overview
- [adt-workflow.md](adt-workflow.md) - Admission/transfer workflows
- [orders-results.md](orders-results.md) - Lab ordering and results
- [sepsis-acute-care.md](sepsis-acute-care.md) - Surgical site infection complications

### Cross-Product: MemberSim

- [../membersim/professional-claims.md](../membersim/professional-claims.md) - Orthopedic surgeon billing
- [../membersim/facility-claims.md](../membersim/facility-claims.md) - Inpatient surgical DRG claims (469/470), SNF billing
- [../membersim/prior-authorization.md](../membersim/prior-authorization.md) - Elective surgery authorization

> **Integration Pattern:** Use PatientSim for surgical episode from pre-op through discharge. Use MemberSim for prior auth workflow, facility claims (bundled payment model), and post-acute SNF claims.

### Cross-Product: RxMemberSim

- [../rxmembersim/retail-pharmacy.md](../rxmembersim/retail-pharmacy.md) - Post-op medications (pain management, anticoagulants)
- [../rxmembersim/dur-alerts.md](../rxmembersim/dur-alerts.md) - Opioid therapy monitoring

> **Integration Pattern:** Use PatientSim for medication orders during episode. Use RxMemberSim for discharge prescription fills - opioid prescriptions trigger DUR alerts and may have quantity limits.

### Reference Files

- [../../references/data-models.md](../../references/data-models.md) - Entity schemas
- [../../references/code-systems.md](../../references/code-systems.md) - ICD-10, CPT codes
