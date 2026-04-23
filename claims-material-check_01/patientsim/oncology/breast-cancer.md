---
name: breast-cancer
description: "Breast cancer patient journeys from screening through treatment and survivorship. Triggers: breast cancer, breast mass, mammogram, ER/PR/HER2, mastectomy, lumpectomy, tamoxifen, aromatase inhibitors, Herceptin, oncology, chemotherapy"
---

# Breast Cancer Management

Comprehensive cohort skill for generating realistic breast cancer patient journeys, from screening detection through treatment, surveillance, and survivorship or metastatic management.

## For Claude

Use this skill when generating breast cancer patients across the care continuum. This teaches you how to generate **realistic clinical event sequences** for breast cancer patients - from abnormal mammogram through biopsy, staging, treatment, and long-term follow-up.

**When to apply this skill:**
- User mentions breast cancer, breast mass, or abnormal mammogram
- User requests oncology patients requiring chemotherapy, radiation, or hormonal therapy
- User specifies ER/PR/HER2 status or molecular subtypes
- User asks for mastectomy, lumpectomy, or breast surgery cohorts
- User mentions tamoxifen, aromatase inhibitors, or Herceptin
- User needs survivorship or metastatic breast cancer cohorts
- User requests multi-disciplinary oncology care workflows

**Key capabilities this skill provides:**
- How to generate complete treatment timelines (diagnosis → staging → surgery → systemic therapy → surveillance)
- How to match molecular subtype with appropriate treatment regimen
- How to create realistic biomarker profiles (ER, PR, HER2, Ki-67)
- How to sequence multi-modality treatment (neoadjuvant vs adjuvant approach)
- How to model treatment toxicity and supportive care needs
- How to structure surveillance schedules by treatment phase
- How to generate metastatic progression with appropriate sites and treatment lines

**Important**: Molecular subtype determines treatment. ER+ patients need hormonal therapy. HER2+ patients need trastuzumab. Triple-negative patients need chemotherapy. Always ensure treatment matches the biomarker profile.

## Metadata
- **Type**: cohort-template
- **Version**: 1.0
- **Author**: Claude (AI-generated, requires clinical validation)
- **Tags**: oncology, breast-cancer, chemotherapy, hormonal-therapy, her2, survivorship, mastectomy
- **Dependencies**:
  - skills/healthcare/oncology-domain.md
  - skills/references/oncology/
- **Updated**: 2025-12-11

## Purpose

This cohort generates realistic breast cancer patients across the disease spectrum, from screen-detected early-stage cancers through metastatic disease. It simulates the multi-disciplinary approach to breast cancer care including surgery, radiation, chemotherapy, targeted therapy, and hormonal therapy.

The cohort is designed to:
- Model realistic breast cancer presentations and detection pathways
- Generate appropriate staging workups and biomarker testing
- Simulate treatment planning based on molecular subtype
- Support different disease phases (newly diagnosed, active treatment, surveillance, recurrence, metastatic)
- Include realistic treatment toxicity patterns and supportive care
- Cover survivorship care planning and long-term follow-up

## When to Use This Skill

Apply this skill when the user's request involves:

**Direct Keywords**:
- "breast cancer", "breast mass", "breast lump"
- "mammogram", "breast biopsy", "breast MRI"
- "lumpectomy", "mastectomy", "breast reconstruction"
- "ER positive", "HER2 positive", "triple negative", "TNBC"
- "tamoxifen", "letrozole", "anastrozole", "aromatase inhibitor"
- "Herceptin", "trastuzumab", "pertuzumab"
- "AC-T", "TCH", "TCHP", "dose-dense"
- "Oncotype DX", "MammaPrint", "genomic assay"
- "BRCA", "genetic testing", "hereditary breast cancer"
- "breast cancer survivor", "surveillance mammogram"

**Clinical Cohorts**:
- "Generate a breast cancer patient"
- "I need a HER2-positive patient on targeted therapy"
- "Create a patient with triple-negative breast cancer"
- "Generate a metastatic breast cancer patient"
- "Make a patient in breast cancer surveillance"
- "I need a patient undergoing neoadjuvant chemotherapy"
- "Create a breast cancer survivor with long-term follow-up"

**Implicit Indicators**:
- User mentions oncology infusion center or chemotherapy
- User specifies ECOG performance status
- User mentions tumor board or multi-disciplinary care
- User asks for hormone receptor status
- User specifies breast surgery or radiation oncology

**Co-occurring Mentions**:
- When user mentions breast cancer AND cardiotoxicity monitoring
- When user mentions breast cancer AND bone metastases
- When user mentions breast cancer AND lymphedema
- When user mentions breast cancer AND genetic counseling

## Trigger Phrases

- breast cancer
- breast mass
- mammogram
- mastectomy
- lumpectomy
- HER2
- ER positive
- triple negative
- tamoxifen
- Herceptin
- BRCA

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| age_range | range | 45-75 | Patient age range |
| gender | enum | female | female, male (rare, ~1% of breast cancers) |
| stage | enum | II | 0, I, IIA, IIB, IIIA, IIIB, IIIC, IV |
| molecular_subtype | enum | luminal_a | luminal_a, luminal_b, her2_enriched, triple_negative |
| laterality | enum | any | left, right, bilateral, any |
| treatment_phase | enum | active | newly_diagnosed, active_treatment, surveillance, recurrence, metastatic |
| surgical_approach | enum | any | lumpectomy, mastectomy, bilateral_mastectomy, none |
| has_reconstruction | boolean | false | Whether breast reconstruction is performed |
| geography | string | null | County/tract FIPS for data-driven context |

## Data Sources (PopulationSim v2.0)

When geography is specified, breast cancer cohorts can reference population context:

### Embedded Data Lookup

```
File: skills/populationsim/data/county/places_county_2024.csv
Cancer-related columns:
  - CANCER_CrudePrev: Any cancer prevalence (%)
  - MAMMOUSE_CrudePrev: Mammography utilization (screening context)
```

### Screening Context by Geography

Mammography rates vary significantly by geography and affect stage at diagnosis:

| Mammography Rate | Typical Stage Distribution |
|------------------|---------------------------|
| > 80% | More Stage 0-I at diagnosis |
| 70-80% | National average distribution |
| < 70% | More Stage II-III at diagnosis |

### SDOH Impact on Oncology

SVI affects breast cancer outcomes:
- **Higher SVI**: Later stage at diagnosis, treatment delays, lower clinical trial enrollment
- **Uninsured**: More locally advanced disease, less access to targeted therapies

## Domain Knowledge

### Molecular Subtype Profiles

Breast cancer is classified by receptor status, which determines treatment and prognosis.

**Why this matters for generation**: The molecular subtype drives the entire treatment plan. Never give trastuzumab to a HER2-negative patient. Never skip hormonal therapy in an ER+ patient.

**Luminal A (ER+/PR+/HER2-/Ki-67 low)**:
- Most common subtype (~40% of breast cancers)
- Best prognosis
- Hormone-responsive
- Treatment: Surgery → Radiation (if lumpectomy) → Hormonal therapy 5-10 years
- Chemotherapy: Often NOT needed (use Oncotype DX to guide)
- Typical Oncotype DX score: Low (0-25)

**Luminal B (ER+/PR+/-/HER2-/Ki-67 high or ER+/HER2+)**:
- ~20% of breast cancers
- Intermediate prognosis
- More aggressive than Luminal A
- Treatment: Surgery → Chemotherapy → Radiation → Hormonal therapy
- If HER2+: Add trastuzumab ± pertuzumab
- Typical Oncotype DX score: Intermediate to High (16-100)

**HER2-Enriched (ER-/PR-/HER2+)**:
- ~10-15% of breast cancers
- Aggressive but highly targetable
- Requires HER2-directed therapy
- Treatment: Neoadjuvant chemotherapy + HER2 therapy → Surgery → Continue HER2 therapy
- Regimens: TCHP (neoadjuvant), TCH (adjuvant)
- 1 year of trastuzumab standard

**Triple-Negative (ER-/PR-/HER2-)**:
- ~15-20% of breast cancers
- Most aggressive subtype
- No targeted therapy (no hormonal, no HER2)
- Treatment: Neoadjuvant chemotherapy → Surgery → Radiation
- May benefit from immunotherapy if PD-L1+
- BRCA testing important (PARP inhibitors if positive)
- Higher recurrence risk in first 3 years

### Biomarker-Treatment Coherence

Treatment must match biomarker status.

**Coherence Rules**:
```python
if ER_positive or PR_positive:
    must_have_hormonal_therapy = True
    # Tamoxifen (premenopausal) or Aromatase inhibitor (postmenopausal)
    duration = "5-10 years"

if HER2_positive:
    must_have_HER2_directed_therapy = True
    # Trastuzumab ± pertuzumab
    duration = "1 year"
    monitor_cardiac_function = True  # ECHO every 3 months

if triple_negative:
    no_targeted_therapy = True
    chemotherapy_is_mainstay = True
    consider_immunotherapy_if_PD_L1_positive = True
    test_BRCA_for_PARP_inhibitor_eligibility = True

if ER_positive and stage_I_or_II:
    consider_Oncotype_DX = True
    if Oncotype_score <= 25:
        may_omit_chemotherapy = True
```

### Staging and Workup

**Initial Diagnostic Workup**:
```
1. Imaging mammogram/ultrasound → suspicious finding
2. Core needle biopsy → confirms invasive carcinoma
3. Pathology:
   - Histologic type (ductal, lobular)
   - Grade (1-3)
   - ER/PR by IHC (% positive cells)
   - HER2 by IHC (0, 1+, 2+, 3+)
   - HER2 FISH if IHC 2+ (equivocal)
   - Ki-67 (proliferation index)
4. Staging imaging (if locally advanced or symptomatic):
   - CT chest/abdomen/pelvis
   - Bone scan or PET/CT
5. Genetic counseling/testing if indicated:
   - Age <50
   - Triple-negative
   - Family history
   - Ashkenazi Jewish heritage
```

**TNM Staging for Breast Cancer (AJCC 8th Edition)**:

| Stage | T | N | M | Description |
|-------|---|---|---|-------------|
| 0 | Tis | N0 | M0 | DCIS (carcinoma in situ) |
| IA | T1 | N0 | M0 | ≤2cm, no nodes |
| IB | T0-1 | N1mi | M0 | Micrometastases only |
| IIA | T0-1 | N1 | M0 | ≤2cm with 1-3 nodes |
| IIA | T2 | N0 | M0 | 2-5cm, no nodes |
| IIB | T2 | N1 | M0 | 2-5cm with 1-3 nodes |
| IIB | T3 | N0 | M0 | >5cm, no nodes |
| IIIA | T0-2 | N2 | M0 | 4-9 nodes involved |
| IIIA | T3 | N1-2 | M0 | >5cm with nodes |
| IIIB | T4 | N0-2 | M0 | Chest wall or skin involvement |
| IIIC | Any T | N3 | M0 | ≥10 nodes or infra/supraclavicular |
| IV | Any T | Any N | M1 | Distant metastases |

### Treatment Pathways by Stage

**Stage 0 (DCIS)**:
- Surgery: Lumpectomy with radiation OR mastectomy
- Hormonal therapy: Tamoxifen 5 years (if ER+) - optional
- No chemotherapy needed

**Stage I-II (Early Stage)**:
```
ER+/HER2- (Luminal A/B):
  1. Surgery (lumpectomy or mastectomy)
  2. Oncotype DX if node-negative (to guide chemo decision)
  3. Chemotherapy if high Oncotype score or node-positive
  4. Radiation if lumpectomy
  5. Hormonal therapy 5-10 years

HER2+ (Any ER status):
  1. Neoadjuvant TCHP (6 cycles) - preferred for Stage II+
  2. Surgery
  3. Adjuvant trastuzumab ± pertuzumab (complete 1 year total)
  4. Radiation if lumpectomy
  5. Hormonal therapy if ER+ (5-10 years)

Triple-Negative:
  1. Neoadjuvant chemotherapy (AC-T or carboplatin-containing)
  2. Surgery
  3. If residual disease: capecitabine 6-8 cycles
  4. Radiation if lumpectomy
  5. Consider pembrolizumab if PD-L1+
```

**Stage III (Locally Advanced)**:
```
All subtypes typically receive neoadjuvant chemotherapy:
  1. Neoadjuvant systemic therapy (allows tumor response assessment)
  2. Surgery (mastectomy more common)
  3. Radiation to chest wall and regional nodes
  4. Complete systemic therapy per subtype
  5. Assess pathologic complete response (pCR)
```

**Stage IV (Metastatic)**:
```
Treatment intent: Palliative (not curative)
Goals: Prolong survival, maintain quality of life, control symptoms

ER+/HER2-:
  1. First-line: CDK4/6 inhibitor + AI (palbociclib + letrozole)
  2. Second-line: Fulvestrant + CDK4/6 inhibitor
  3. Later lines: Chemotherapy (capecitabine, eribulin)

HER2+:
  1. First-line: Taxane + trastuzumab + pertuzumab
  2. Second-line: T-DM1 (ado-trastuzumab emtansine)
  3. Third-line: T-DXd (trastuzumab deruxtecan)

Triple-Negative:
  1. First-line: Chemotherapy ± pembrolizumab (if PD-L1+)
  2. Second-line: Different chemotherapy agent
  3. If BRCA+: PARP inhibitor (olaparib)
```

### Chemotherapy Regimens

**Adjuvant/Neoadjuvant Regimens**:

| Regimen | Components | Cycles | Indications |
|---------|------------|--------|-------------|
| AC | Doxorubicin + Cyclophosphamide | 4 | ER+, no taxane needed |
| AC-T | AC × 4 → Paclitaxel × 4 | 4+4 | Standard adjuvant |
| ddAC-T | Dose-dense AC × 4 → Paclitaxel × 4 (q14d) | 4+4 | Higher risk, requires G-CSF |
| TC | Docetaxel + Cyclophosphamide | 4 | ER+, older patients |
| TCH | Docetaxel + Carboplatin + Trastuzumab | 6 | HER2+ adjuvant |
| TCHP | Docetaxel + Carboplatin + Trastuzumab + Pertuzumab | 6 | HER2+ neoadjuvant |

**Dosing Example - AC-T**:
```
Cycles 1-4: AC (q21 days)
  - Doxorubicin 60 mg/m² IV day 1
  - Cyclophosphamide 600 mg/m² IV day 1

Cycles 5-8: Paclitaxel (q21 days or weekly)
  - Paclitaxel 175 mg/m² IV day 1 (q21d)
  - OR Paclitaxel 80 mg/m² IV weekly × 12

Pre-medications:
  - Ondansetron 8mg IV
  - Dexamethasone 12mg IV
  - Diphenhydramine 25mg IV (for paclitaxel)
```

### Hormonal Therapy

**Premenopausal**:
- Tamoxifen 20mg PO daily × 5-10 years
- May add ovarian suppression (goserelin) for high risk
- Side effects: Hot flashes, DVT risk, endometrial cancer risk

**Postmenopausal**:
- Aromatase inhibitors (preferred):
  - Letrozole 2.5mg PO daily
  - Anastrozole 1mg PO daily
  - Exemestane 25mg PO daily
- Duration: 5-10 years (extended therapy for high risk)
- Side effects: Arthralgias, bone loss, hot flashes

**Sequencing Options**:
```
Option 1: AI × 5 years
Option 2: Tamoxifen × 2-3 years → AI × 2-3 years
Option 3: AI × 2-3 years → Tamoxifen × 2-3 years
Option 4: AI × 5 years + 5 years extended therapy (high risk)
```

### HER2-Directed Therapy

**Trastuzumab (Herceptin)**:
- Dose: 8 mg/kg IV loading → 6 mg/kg IV q3 weeks
- OR: 600mg SC q3 weeks (subcutaneous formulation)
- Duration: Complete 1 year (17 cycles)
- Cardiac monitoring: ECHO or MUGA every 3 months
- Hold if LVEF drops >10% or below 50%

**Pertuzumab (Perjeta)**:
- Dose: 840mg IV loading → 420mg IV q3 weeks
- Given with trastuzumab in neoadjuvant/metastatic settings
- Enhances HER2 blockade

**T-DM1 (Kadcyla)**:
- Antibody-drug conjugate
- Dose: 3.6 mg/kg IV q3 weeks
- Used after trastuzumab-based therapy or for residual disease

**T-DXd (Enhertu)**:
- Next-generation ADC
- Dose: 5.4 mg/kg IV q3 weeks
- Highly active, even in HER2-low tumors
- Monitor for interstitial lung disease

### Surveillance Schedule

**First 5 Years (Active Surveillance)**:
```
Year 1-2:
  - Clinical exam: every 3-6 months
  - Mammogram: 6 months post-radiation, then annually
  - Labs: As needed for symptoms

Year 3-5:
  - Clinical exam: every 6-12 months
  - Mammogram: annually
  - DEXA scan: baseline, then every 2 years (if on AI)
```

**After 5 Years (Extended Surveillance)**:
```
Year 5+:
  - Clinical exam: annually
  - Mammogram: annually
  - Continue hormonal therapy monitoring if applicable
```

**Routine surveillance does NOT include**:
- Tumor markers (not recommended for asymptomatic)
- CT scans (only if symptomatic)
- PET scans (not for routine surveillance)
- Blood tests beyond standard health maintenance

### Treatment Toxicity Patterns

**Anthracycline (Doxorubicin) Toxicities**:
- Myelosuppression: Nadir day 10-14
- Nausea/vomiting: High emetogenic (use 3-drug antiemetic)
- Alopecia: Nearly universal
- Cardiotoxicity: Cumulative (limit 450-550 mg/m² lifetime)

**Taxane (Paclitaxel/Docetaxel) Toxicities**:
- Peripheral neuropathy: Dose-limiting, may be permanent
- Myelosuppression
- Hypersensitivity reactions (premedicate)
- Nail changes, edema (docetaxel)

**Hormonal Therapy Toxicities**:
```
Tamoxifen:
  - Hot flashes (common)
  - DVT/PE risk (rare but serious)
  - Endometrial cancer (rare)
  - Cataracts

Aromatase Inhibitors:
  - Arthralgias/myalgias (30-50%)
  - Bone loss/osteoporosis
  - Hot flashes
  - Vaginal dryness
```

**Trastuzumab Cardiotoxicity**:
- LVEF decline (usually reversible)
- Monitor ECHO every 3 months
- Hold if LVEF <50% or drops >16% from baseline
- Can often resume when LVEF recovers

### Common Metastatic Sites

Breast cancer commonly metastasizes to:

| Site | Frequency | Symptoms | Workup |
|------|-----------|----------|--------|
| Bone | 70% | Pain, fracture | Bone scan, CT |
| Liver | 40% | RUQ pain, LFT elevation | CT, MRI |
| Lung | 30% | Dyspnea, cough | CT chest |
| Brain | 15% | Headache, neuro deficits | MRI brain |
| Pleura | 10% | Dyspnea, effusion | CT, thoracentesis |

**HER2+ and Triple-Negative have higher rates of brain metastases**

## Generation Guidelines

### How to Apply This Knowledge

**When the user says**: "Generate a breast cancer patient"

**Claude should**:
1. **Select subtype**: Luminal A (most common) unless specified
2. **Choose stage**: Stage II (typical at diagnosis)
3. **Generate biomarkers**:
   ```python
   if subtype == "luminal_a":
       ER = "positive (95%)"
       PR = "positive (80%)"
       HER2 = "negative (IHC 1+)"
       Ki67 = "10% (low)"
       grade = 2
   ```
4. **Select treatment pathway**:
   - Surgery (lumpectomy or mastectomy)
   - Radiation if lumpectomy
   - Oncotype DX to guide chemotherapy decision
   - Hormonal therapy 5-10 years
5. **Generate realistic timeline**

**When the user says**: "Generate a HER2-positive breast cancer patient"

**Claude should**:
1. **Set biomarkers**:
   ```python
   HER2 = "positive (IHC 3+)"
   ER = randomly_select(["positive (70%)", "negative"])
   PR = randomly_select(["positive", "negative"])
   ```
2. **Select treatment**:
   - Neoadjuvant TCHP × 6 cycles (preferred approach)
   - Surgery
   - Continue trastuzumab ± pertuzumab to complete 1 year
   - Radiation if lumpectomy
   - Hormonal therapy if ER+
3. **Include cardiac monitoring**: ECHO at baseline, q3mo during HER2 therapy
4. **Document pathologic response**: pCR vs residual disease

**When the user says**: "Generate a metastatic breast cancer patient"

**Claude should**:
1. **Set stage**: IV
2. **Choose metastatic sites**: Bone (most common), liver, lung, brain
3. **Include both primary and metastatic codes**:
   ```python
   primary_code = "C50.911"  # Right breast
   metastatic_codes = ["C79.51"]  # Bone mets
   ```
4. **Select treatment based on subtype**:
   - ER+: CDK4/6 inhibitor + AI first-line
   - HER2+: Taxane + trastuzumab + pertuzumab
   - TNBC: Chemotherapy ± immunotherapy
5. **Set treatment intent**: Palliative
6. **Include line of therapy** (1st, 2nd, 3rd)

### Coherence Checks

Before finalizing a breast cancer patient, verify:

```python
# 1. Biomarker-treatment coherence
if ER_positive:
    assert has_hormonal_therapy, "ER+ must have hormonal therapy"
if HER2_positive:
    assert has_trastuzumab, "HER2+ must have HER2-directed therapy"
    assert has_cardiac_monitoring, "HER2 therapy requires ECHO monitoring"
if triple_negative:
    assert not has_hormonal_therapy, "TNBC cannot have hormonal therapy"
    assert not has_HER2_therapy, "TNBC cannot have HER2 therapy"

# 2. Stage-treatment intent coherence
if stage == "IV":
    assert treatment_intent == "palliative"
    assert has_metastatic_site_codes
if stage in ["I", "II", "III"]:
    assert treatment_intent in ["curative", "adjuvant", "neoadjuvant"]

# 3. Surgical approach coherence
if had_lumpectomy:
    assert has_radiation_therapy, "Lumpectomy requires radiation"
if stage == "IV":
    assert surgical_approach in ["none", "palliative"], "Stage IV rarely surgical"

# 4. Chemotherapy regimen coherence
if regimen == "TCHP":
    assert HER2_positive, "TCHP only for HER2+"
if regimen == "AC-T":
    assert suitable_for_anthracycline, "Check cardiac history"

# 5. Timeline coherence
if neoadjuvant_chemotherapy:
    assert chemotherapy_before_surgery
if adjuvant_chemotherapy:
    assert chemotherapy_after_surgery
```

## Example Requests and Interpretations

### Example 1: Early-Stage ER+ Patient

**User says**: "Generate an early-stage breast cancer patient"

**Claude interprets**:
- Stage: IIA (T2N0M0, most common early stage)
- Subtype: Luminal A (most common)
- Phase: Newly diagnosed proceeding to treatment

**Key features Claude generates**:

**Demographics**: Age 58, female, postmenopausal

**Presentation**: Palpable right breast mass found on self-exam, confirmed on screening mammogram

**Pathology** (core biopsy):
- Invasive ductal carcinoma, Grade 2
- ER: Positive (95%)
- PR: Positive (75%)
- HER2: Negative (IHC 1+)
- Ki-67: 12% (low)

**Staging**:
- T2 (2.3 cm tumor)
- N0 (sentinel node negative)
- M0 (no distant metastases)
- Stage IIA

**Oncotype DX**: Recurrence Score 18 (low-intermediate, chemotherapy benefit uncertain)

**Treatment Plan**:
1. Lumpectomy with sentinel lymph node biopsy - completed
2. Radiation therapy to breast - 4 weeks (hypofractionated)
3. Hormonal therapy: Anastrozole 1mg daily × 5 years

**ICD-10 Codes**:
- C50.911 (Malignant neoplasm right breast)
- Z51.0 (Encounter for radiation therapy)
- Z79.818 (Long-term hormonal therapy)

**Current Status**: Completing radiation, tolerating anastrozole with mild arthralgias

---

### Example 2: HER2+ Neoadjuvant Therapy

**User says**: "Generate a HER2-positive breast cancer patient on neoadjuvant chemotherapy"

**Claude interprets**:
- Stage: IIB-IIIA (neoadjuvant typically for larger tumors)
- Subtype: HER2-enriched
- Phase: Active treatment, mid-regimen

**Key features Claude generates**:

**Demographics**: Age 52, female, premenopausal

**Presentation**: 4.5 cm left breast mass with palpable axillary node

**Pathology**:
- Invasive ductal carcinoma, Grade 3
- ER: Negative
- PR: Negative
- HER2: Positive (IHC 3+)
- Ki-67: 65% (high)

**Staging**:
- T2 (4.5 cm)
- N1 (positive axillary node on biopsy)
- M0
- Stage IIB

**Biomarkers**: PD-L1 negative

**Treatment Plan - TCHP**:
- Docetaxel 75 mg/m² IV day 1
- Carboplatin AUC 6 IV day 1
- Trastuzumab 8 mg/kg loading → 6 mg/kg IV q3w
- Pertuzumab 840mg loading → 420mg IV q3w
- Cycle length: 21 days × 6 cycles

**Current Status**: Cycle 4 of 6
- Clinical exam: Tumor decreased from 4.5 cm to 1.5 cm (partial response)
- Tolerating treatment with:
  - Grade 2 neutropenia (nadir ANC 800)
  - Grade 1 neuropathy (numbness fingertips)
  - Mild diarrhea
- LVEF: 58% (baseline 62%) - acceptable, continuing therapy
- Next ECHO scheduled after cycle 6

**Labs (Day 1, Cycle 4)**:
- WBC: 4.2 (recovered)
- ANC: 2,800
- Hgb: 11.2 (mild anemia)
- Platelets: 185
- Creatinine: 0.9

**Supportive Care**:
- Ondansetron 8mg IV pre-chemo + days 2-3
- Dexamethasone 12mg IV pre-chemo
- Pegfilgrastim 6mg SC day 2

**Next Steps**:
- Complete cycles 5-6 of TCHP
- Repeat breast MRI for response assessment
- Surgery (likely lumpectomy given response)
- Continue trastuzumab ± pertuzumab to complete 1 year

---

### Example 3: Triple-Negative with Complete Response

**User says**: "Generate a triple-negative breast cancer patient who completed neoadjuvant therapy"

**Claude interprets**:
- Subtype: Triple-negative
- Phase: Post-neoadjuvant, assessing pathologic response
- Key outcome: Evaluating for pCR

**Key features Claude generates**:

**Demographics**: Age 45, female, premenopausal, African American

**Initial Presentation**: 3.2 cm right breast mass, Grade 3

**Pathology (Pre-treatment)**:
- Invasive ductal carcinoma, Grade 3
- ER: Negative (<1%)
- PR: Negative (<1%)
- HER2: Negative (IHC 0)
- Ki-67: 80% (high)
- PD-L1: Positive (CPS 15)

**Genetic Testing**: BRCA1 positive

**Initial Staging**: T2N1M0, Stage IIB

**Neoadjuvant Treatment**:
- Pembrolizumab 200mg IV q3w × 8 cycles
- Carboplatin AUC 5 IV q3w × 4 cycles
- Paclitaxel 80 mg/m² IV weekly × 12 weeks
- Then AC × 4 cycles

**Surgery**: Right lumpectomy with axillary dissection

**Pathology (Post-treatment)**:
- **Pathologic Complete Response (pCR)**
- ypT0 ypN0 - No residual invasive carcinoma
- Treatment effect in breast and nodes

**Adjuvant Treatment**:
- Radiation therapy to breast - completed
- Pembrolizumab × 9 additional cycles (complete 1 year)
- BRCA+ → discussed risk-reducing bilateral salpingo-oophorectomy

**Current Status**: Surveillance phase
- 6 months post-treatment
- No evidence of disease
- Tolerating pembrolizumab with Grade 1 fatigue

**Surveillance Plan**:
- Clinical exam q3-4 months × 2 years
- Mammogram annually
- High-risk screening with breast MRI annually
- Genetic counseling for family members

---

### Example 4: Metastatic Disease - Multiple Lines of Therapy

**User says**: "Generate a metastatic breast cancer patient on third-line treatment"

**Claude interprets**:
- Stage: IV (de novo or recurrence)
- Multiple prior treatments
- Disease progression cohort

**Key features Claude generates**:

**Demographics**: Age 62, female, postmenopausal

**Cancer History**:
- Original diagnosis: Stage IIA ER+/HER2- breast cancer, 8 years ago
- Treatment: Lumpectomy, radiation, AC-T, anastrozole × 5 years
- Recurrence: Bone metastases diagnosed 3 years ago

**Current Biomarkers** (re-biopsy of met):
- ER: Positive (85%)
- PR: Positive (40%)
- HER2: Negative (IHC 1+)
- ESR1 mutation: Detected (Y537S) - resistance to aromatase inhibitors

**Treatment History**:
```
First-line (3 years ago):
  - Palbociclib 125mg days 1-21 q28d + Letrozole 2.5mg daily
  - Duration: 18 months
  - Best response: Stable disease
  - Reason for discontinuation: Progressive disease (new liver mets)

Second-line (18 months ago):
  - Fulvestrant 500mg IM q2w × 3, then monthly + Abemaciclib 150mg BID
  - Duration: 12 months
  - Best response: Partial response
  - Reason for discontinuation: Progressive disease (liver mets enlarging)

Third-line (current):
  - Capecitabine 1000 mg/m² BID days 1-14 q21d
  - Started 2 months ago
  - Response: Pending imaging
```

**Current Metastatic Sites**:
- Bone: L2, L4 vertebrae; right femur (all stable on denosumab)
- Liver: 3 lesions, largest 3.2 cm

**Performance Status**: ECOG 1

**Current Symptoms**:
- Mild fatigue
- Occasional right upper quadrant discomfort
- Hand-foot syndrome (Grade 1) from capecitabine

**Labs**:
- WBC: 5.8
- Hgb: 10.8 (chronic anemia of malignancy)
- Platelets: 180
- AST: 52 (mildly elevated)
- ALT: 48
- Alk Phos: 145 (elevated from bone mets)
- CA 15-3: 85 (elevated, trending)

**Supportive Medications**:
- Denosumab 120mg SC monthly (bone-directed therapy)
- Ondansetron 8mg PRN nausea
- Vitamin B6 100mg BID (for hand-foot syndrome)
- Urea 10% cream to hands/feet

**ICD-10 Codes**:
- C50.911 (Primary breast cancer)
- C79.51 (Secondary malignant neoplasm of bone)
- C78.7 (Secondary malignant neoplasm of liver)
- Z85.3 (Personal history of breast cancer)
- Z51.11 (Encounter for antineoplastic chemotherapy)

**Prognosis Discussion**: Goals of care addressed; patient wishes to continue treatment. Palliative care involved for symptom management.

## Variations

### Variation: Newly Diagnosed Early Stage
Screen-detected Stage I-II breast cancer proceeding to initial treatment.
- stage: I or IIA
- treatment_phase: newly_diagnosed
- **Includes**:
  - Diagnostic mammogram and biopsy
  - Staging workup
  - Surgical planning (lumpectomy vs mastectomy discussion)
  - Oncotype DX or MammaPrint if ER+/HER2-/node-negative
  - Sentinel lymph node biopsy planning
- **Timeline**: Diagnosis → Surgery within 4-6 weeks

### Variation: Adjuvant Chemotherapy
Post-surgery patient receiving adjuvant chemotherapy.
- stage: II or III
- treatment_phase: active_treatment
- **Includes**:
  - Port placement for IV access
  - Chemotherapy cycles (AC-T, TC, or TCH)
  - Treatment toxicity monitoring (CBC, symptoms)
  - Growth factor support if dose-dense
  - Antiemetic regimen
- **Timeline**: Chemotherapy starts 4-6 weeks post-surgery

### Variation: HER2-Positive Treatment
HER2+ patient on targeted therapy regimen.
- molecular_subtype: her2_enriched or luminal_b_her2_positive
- **Includes**:
  - Trastuzumab ± pertuzumab dosing
  - Cardiac monitoring (ECHO every 3 months)
  - LVEF documentation
  - 1-year HER2 therapy completion
- **Cardiac Monitoring Example**:
  - Baseline LVEF: 62%
  - Cycle 6: LVEF 58% (acceptable decline)
  - Cycle 12: LVEF 55% (continue monitoring)
  - Post-treatment: LVEF 60% (recovered)

### Variation: Hormonal Therapy Surveillance
ER+ patient on long-term hormonal therapy in surveillance.
- molecular_subtype: luminal_a
- treatment_phase: surveillance
- **Includes**:
  - Tamoxifen or aromatase inhibitor
  - Annual mammogram
  - Bone density monitoring (DEXA every 2 years)
  - Side effect management (arthralgias, hot flashes)
  - 5-10 year treatment duration
- **Surveillance Schedule**: Clinical exam q6mo years 1-5, then annually

### Variation: Triple-Negative Breast Cancer
TNBC with aggressive treatment approach.
- molecular_subtype: triple_negative
- **Includes**:
  - Neoadjuvant chemotherapy (common approach)
  - Pathologic complete response assessment
  - Capecitabine if residual disease after neoadjuvant
  - BRCA testing for all TNBC patients
  - Consider pembrolizumab if PD-L1+
- **Higher recurrence risk**: Close surveillance first 3 years

### Variation: Metastatic Disease
Stage IV or recurrent metastatic breast cancer.
- stage: IV
- treatment_phase: metastatic
- **Includes**:
  - Metastatic sites (bone, liver, lung, brain)
  - Line of therapy documentation (1st, 2nd, 3rd+)
  - Treatment intent: Palliative
  - Goals of care discussions
  - Palliative care integration
  - Bone-directed therapy if bone mets
- **Sites by ER status**:
  - ER+: More bone metastases
  - HER2+/TNBC: More visceral and brain metastases

### Variation: Survivorship
Completed active treatment, in long-term surveillance.
- treatment_phase: surveillance
- **Includes**:
  - Surveillance mammogram schedule
  - Long-term side effect monitoring
  - Survivorship care plan documentation
  - Z85.3 (personal history) code
  - Screening for secondary cancers
  - Lymphedema monitoring if axillary surgery
- **Timeline**: 5+ years from diagnosis

### Variation: BRCA-Positive Hereditary
Patient with BRCA1/2 mutation and enhanced risk.
- **Includes**:
  - Genetic counseling documentation
  - BRCA test result
  - Risk-reducing surgery discussion (bilateral mastectomy, BSO)
  - Enhanced screening protocol (MRI + mammogram alternating q6mo)
  - Family member testing recommendation
  - PARP inhibitor eligibility if metastatic

### Variation: Male Breast Cancer
Rare male patient with breast cancer.
- gender: male
- **Includes**:
  - Usually ER+ (>90%)
  - Often presents at later stage (less awareness)
  - Mastectomy standard (no lumpectomy option typically)
  - Tamoxifen preferred (not aromatase inhibitors)
  - BRCA2 testing recommended for all male breast cancer

## Composite Patterns

### Breast Cancer with Anthracycline Cardiotoxicity
```yaml
description: Patient developing cardiomyopathy from doxorubicin
combines:
  - breast-cancer.md
  - oncology-domain.md (cardiotoxicity section)
shared_considerations:
  - Baseline ECHO before anthracycline
  - Cumulative doxorubicin dose tracking (limit 450-550 mg/m²)
  - LVEF decline triggers:
    - <50%: Hold chemotherapy
    - >10% drop from baseline: Cardiology consultation
  - Switch to non-anthracycline regimen (TC instead of AC)
  - Cardio-oncology referral
example_cohort:
  - Baseline LVEF 60%
  - After AC cycle 3: LVEF 48%
  - Action: Hold doxorubicin, switch to taxane-only
  - Cardiology referral, consider ACE inhibitor
```

### Breast Cancer with HER2 Therapy Cardiotoxicity
```yaml
description: Trastuzumab-induced LVEF decline
shared_considerations:
  - ECHO every 3 months during trastuzumab
  - Hold criteria: LVEF <50% or >16% drop
  - Usually reversible (unlike anthracycline)
  - Can often rechallenge when LVEF recovers
  - Consider liposomal doxorubicin if both needed
example_cohort:
  - On TCHP cycle 4
  - LVEF drops 62% → 45%
  - Hold trastuzumab/pertuzumab
  - Start lisinopril 5mg, carvedilol 6.25mg BID
  - Recheck ECHO in 4 weeks
  - LVEF recovers to 52% → resume HER2 therapy
```

### Breast Cancer with Bone Metastases
```yaml
description: Metastatic to bone requiring bone-directed therapy
includes:
  - Bisphosphonate (zoledronic acid) or denosumab monthly
  - SRE (skeletal-related event) prevention
  - Hypercalcemia monitoring
  - Dental evaluation before starting (ONJ risk)
  - Radiation for painful bone mets
  - Orthopedic evaluation for weight-bearing bones
typical_presentation:
  - Back pain, pathologic fracture risk
  - Elevated alkaline phosphatase
  - Bone scan showing multiple lesions
medications:
  - Denosumab 120mg SC monthly
  - OR Zoledronic acid 4mg IV monthly
  - Calcium 500mg + Vitamin D 400IU daily
```

### Breast Cancer Hereditary Syndrome
```yaml
description: BRCA1/2 positive with enhanced surveillance and risk reduction
includes:
  - Genetic counseling visit documentation
  - BRCA result: Pathogenic variant in BRCA1 or BRCA2
  - Enhanced screening: Breast MRI alternating with mammogram q6 months
  - Risk-reducing surgery discussion:
    - Bilateral mastectomy (reduces risk 90%+)
    - Bilateral salpingo-oophorectomy (reduces ovarian and breast cancer risk)
  - Family cascade testing recommendation
  - PARP inhibitor eligibility if metastatic
typical_patient:
  - Younger age (<50)
  - Triple-negative subtype (especially BRCA1)
  - Strong family history
  - Ashkenazi Jewish heritage
```

### Breast Cancer with Lymphedema
```yaml
description: Post-axillary surgery lymphedema development
includes:
  - Axillary lymph node dissection history
  - Arm circumference measurements
  - Lymphedema staging (mild/moderate/severe)
  - Compression sleeve fitting
  - Physical therapy referral
  - Lymphedema precautions education
risk_factors:
  - Axillary dissection (>sentinel only)
  - Regional lymph node radiation
  - Obesity
  - Infection of affected arm
management:
  - Compression garments
  - Manual lymphatic drainage
  - Complete decongestive therapy
  - Avoid blood draws/BP on affected arm
```

## Generation Rules

### Demographics
- **Age**: 45-75 years (peak incidence 55-64)
- **Gender**: Female (99%), Male (1%)
- **Race/Ethnicity**: All groups; TNBC more common in African American and young patients

### Conditions

**Primary Diagnosis**:
- Invasive ductal carcinoma (C50.x) - 70-80%
- Invasive lobular carcinoma (C50.x) - 10-15%
- DCIS (D05.x) - if Stage 0

**Common Comorbidities**:
- Hypertension (I10) - 40%
- Obesity (E66.x) - 35%
- Type 2 diabetes (E11.x) - 20%
- Osteoporosis (M81.x) - especially if on aromatase inhibitor
- Anxiety/depression (F41.x, F32.x) - 25%

**Treatment-Related Conditions**:
- Lymphedema (I89.0) - if axillary surgery
- Chemotherapy-induced neuropathy (G62.0)
- Cardiomyopathy (I42.7) - if anthracycline/trastuzumab
- Osteopenia/osteoporosis (M81.x) - if aromatase inhibitor
- Hot flashes/menopausal symptoms (N95.1) - hormonal therapy

### Vital Signs

**During Active Treatment**:
- Blood Pressure: 110-140/70-85 mmHg
- Heart Rate: 70-90 bpm
- Temperature: 98.0-99.0°F (monitor for neutropenic fever)
- Weight: May decrease during chemotherapy

**During Surveillance**:
- Generally normal vital signs
- Monitor for weight changes on hormonal therapy

### Laboratory

**Pre-Chemotherapy Labs**:
- CBC with differential (check ANC for treatment)
- Comprehensive metabolic panel
- LFTs if metastatic liver involvement suspected

**During Chemotherapy** (each cycle):
```
CBC:
  - WBC: May drop to 2-3 during nadir (day 10-14)
  - ANC: >1,500 to treat (>1,000 acceptable with G-CSF)
  - Hemoglobin: 10-12 g/dL (mild anemia common)
  - Platelets: >100,000 to treat

CMP:
  - Monitor renal function if on carboplatin
  - LFTs if on taxane
```

**Tumor Markers** (metastatic only):
- CA 15-3: Elevated in metastatic, monitor trend
- CA 27-29: Alternative marker
- NOT recommended for early-stage surveillance

### Medications

**Chemotherapy by Regimen** (see Chemotherapy Regimens section)

**Hormonal Therapy** (ER+ patients):
- Tamoxifen 20mg PO daily (premenopausal)
- Letrozole 2.5mg PO daily (postmenopausal)
- Anastrozole 1mg PO daily (postmenopausal)
- Exemestane 25mg PO daily (postmenopausal)

**HER2-Directed** (HER2+ patients):
- Trastuzumab 6mg/kg IV q3w (after loading)
- Pertuzumab 420mg IV q3w (after loading)
- T-DM1 3.6mg/kg IV q3w (metastatic)
- T-DXd 5.4mg/kg IV q3w (metastatic)

**Supportive Care**:
- Ondansetron 8mg IV/PO (antiemetic)
- Dexamethasone 12mg IV/PO (antiemetic, premedication)
- Pegfilgrastim 6mg SC (G-CSF for dose-dense)
- Diphenhydramine 25mg IV (taxane premedication)
- Denosumab 120mg SC monthly (bone mets)

### Timeline

**Newly Diagnosed → Surgery** (typical 4-6 weeks):
- Week 0: Abnormal mammogram
- Week 1: Diagnostic mammogram, ultrasound
- Week 2: Core needle biopsy, pathology results
- Week 3: Staging workup, breast MRI
- Week 4: Tumor board, surgical consultation
- Week 5-6: Surgery (lumpectomy or mastectomy)

**Surgery → Adjuvant Treatment** (4-6 weeks post-surgery):
- Week 6-8: Port placement if chemotherapy planned
- Week 8: Start chemotherapy
- Week 8-24: Chemotherapy (16 weeks typical for AC-T)
- Week 24-28: Start radiation (4-6 weeks)
- Week 28+: Start hormonal therapy (continue 5-10 years)

**Neoadjuvant Approach** (HER2+ or TNBC):
- Week 0: Diagnosis, biomarkers
- Week 2: Start neoadjuvant chemotherapy
- Week 2-20: Complete neoadjuvant (typically 6 cycles = 18 weeks)
- Week 22: Surgery
- Week 26-30: Radiation
- Continue targeted therapy to complete 1 year total

## References

**Clinical Guidelines**:
- NCCN Guidelines for Breast Cancer (Version 1.2024)
- ASCO/CAP Guidelines for HER2 Testing
- ASCO Guidelines for Adjuvant Endocrine Therapy
- American Society of Breast Surgeons Guidelines

**Genomic Assays**:
- Oncotype DX (21-gene assay)
- MammaPrint (70-gene assay)
- TAILORx Trial (Oncotype DX validation)
- RxPONDER Trial (node-positive, ER+)

**Key Clinical Trials**:
- TAILORx (Oncotype DX in node-negative ER+)
- RxPONDER (Oncotype DX in node-positive ER+)
- APHINITY (Pertuzumab adjuvant)
- KATHERINE (T-DM1 for residual disease)
- KEYNOTE-522 (Pembrolizumab in TNBC)
- CREATE-X (Capecitabine for residual TNBC)
- OlympiA (Olaparib for BRCA+ early breast cancer)

## Clinical Validation Notice

This cohort skill was AI-generated and requires clinical validation before use in any production or clinical decision-support context. The information provided is intended for synthetic data generation for testing and training purposes only.

Key areas requiring validation:
- Treatment regimen accuracy and current standard of care
- Biomarker thresholds and testing algorithms
- Staging criteria per current AJCC guidelines
- Drug dosing and administration schedules
- Surveillance protocols per current guidelines

Last validation review: Pending

## Validation Rules

| Rule | Requirement | Example |
|------|-------------|---------|
| Stage | 0, I, II, III, IV | Stage IIA |
| ER status | positive, negative | "positive" |
| PR status | positive, negative | "positive" |
| HER2 status | positive, negative, equivocal | "negative" |
| Ki-67 | 0-100% | 25% |
| Tumor size | cm | 2.3 cm |
| Node status | pN0, pN1, pN2, pN3 | pN1 (1-3 nodes) |
| Grade | 1, 2, 3 | Grade 2 |

### Business Rules

- **Molecular Subtype**: ER/PR/HER2 status determines treatment approach
- **Luminal A**: ER+/PR+/HER2-/low Ki-67 → Endocrine therapy often sufficient
- **Luminal B**: ER+/PR+/HER2±/high Ki-67 → May need chemo + endocrine
- **HER2-enriched**: HER2+ → Trastuzumab-based therapy
- **Triple Negative**: ER-/PR-/HER2- → Chemotherapy primary treatment
- **Oncotype DX**: Recurrence score guides chemo decision in ER+/HER2-/node-negative
- **Neoadjuvant**: Pre-operative chemo for locally advanced or to enable BCT
- **Adjuvant Endocrine**: 5-10 years for ER+ disease

## Related Skills

### PatientSim Cohorts

- [../SKILL.md](../SKILL.md) - PatientSim overview
- [lung-cancer.md](lung-cancer.md) - Similar oncology cohort structure
- [colorectal-cancer.md](colorectal-cancer.md) - Similar oncology cohort structure
- [../maternal-health.md](../maternal-health.md) - Pregnancy and breast cancer considerations

### Cross-Product: MemberSim

- [../../membersim/professional-claims.md](../../membersim/professional-claims.md) - Oncology office visit billing
- [../../membersim/facility-claims.md](../../membersim/facility-claims.md) - Chemotherapy infusion, surgery, radiation claims
- [../../membersim/prior-authorization.md](../../membersim/prior-authorization.md) - Oncology drug authorization

### Cross-Product: RxMemberSim

- [../../rxmembersim/specialty-pharmacy.md](../../rxmembersim/specialty-pharmacy.md) - Oncology drugs (trastuzumab, pertuzumab, CDK4/6 inhibitors)
- [../../rxmembersim/rx-prior-auth.md](../../rxmembersim/rx-prior-auth.md) - Specialty drug authorization

### Reference Files

- [../../../references/data-models.md](../../../references/data-models.md) - Entity schemas
- [../../../references/code-systems.md](../../../references/code-systems.md) - ICD-10, CPT, HCPCS codes
