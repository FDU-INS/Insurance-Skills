---
name: lung-cancer
description: "Lung cancer patient journeys for NSCLC and SCLC with biomarker-driven treatment selection. Triggers: lung cancer, lung mass, pulmonary nodule, NSCLC, SCLC, adenocarcinoma, squamous cell, EGFR, ALK, ROS1, KRAS, PD-L1, osimertinib, immunotherapy, pembrolizumab"
---

# Lung Cancer Management

Comprehensive cohort skill for generating realistic lung cancer patient journeys, covering both Non-Small Cell Lung Cancer (NSCLC) and Small Cell Lung Cancer (SCLC), from diagnosis through biomarker-driven treatment selection, progression, and palliative care.

## For Claude

Use this skill when generating lung cancer patients across the care continuum. This teaches you how to generate **realistic clinical event sequences** for lung cancer patients - from incidental nodule detection or symptomatic presentation through staging, molecular testing, treatment selection, and disease monitoring.

**When to apply this skill:**
- User mentions lung cancer, lung mass, pulmonary nodule
- User requests thoracic oncology or lung cancer treatment cohorts
- User specifies NSCLC, SCLC, adenocarcinoma, or squamous cell lung cancer
- User asks about EGFR, ALK, ROS1, KRAS, or PD-L1 testing
- User mentions targeted therapy agents (osimertinib, alectinib, sotorasib)
- User mentions immunotherapy in lung cancer (pembrolizumab, durvalumab)
- User needs brain metastases cohorts (common in lung cancer)
- User requests smoking-related cancer cohorts

**Key capabilities this skill provides:**
- How to generate complete treatment timelines based on histology and biomarkers
- How to match molecular profile with appropriate targeted therapy
- How to distinguish NSCLC treatment from SCLC treatment
- How to create realistic biomarker testing workflows (NGS, PD-L1)
- How to model brain metastases presentation and management
- How to sequence therapies upon progression
- How to structure surveillance for each stage and treatment

**Important**: Lung cancer treatment is highly dependent on histology (NSCLC vs SCLC) and molecular markers. NEVER give targeted therapy without confirming the mutation. ALWAYS test for actionable mutations in non-squamous NSCLC before starting treatment.

## Metadata
- **Type**: cohort-template
- **Version**: 1.0
- **Author**: Claude (AI-generated, requires clinical validation)
- **Tags**: oncology, lung-cancer, nsclc, sclc, immunotherapy, targeted-therapy, egfr, alk, pdl1
- **Dependencies**:
  - skills/healthcare/oncology-domain.md
  - skills/references/oncology/
- **Updated**: 2025-12-11

## Purpose

This cohort generates realistic lung cancer patients across the disease spectrum, from screen-detected early-stage cancers through metastatic disease. It simulates the biomarker-driven approach to lung cancer care, which has transformed outcomes for patients with actionable mutations.

The cohort is designed to:
- Model realistic lung cancer presentations (incidental finding vs symptomatic)
- Generate appropriate staging workups including PET-CT and brain MRI
- Simulate molecular testing workflows and result interpretation
- Support treatment selection based on histology and biomarkers
- Include brain metastases (common in lung cancer)
- Cover SCLC-specific staging and treatment
- Address treatment toxicities including pneumonitis

## When to Use This Skill

Apply this skill when the user's request involves:

**Direct Keywords**:
- "lung cancer", "lung mass", "lung nodule", "pulmonary mass"
- "NSCLC", "non-small cell", "adenocarcinoma of lung", "squamous cell lung"
- "SCLC", "small cell lung cancer", "oat cell"
- "EGFR", "ALK", "ROS1", "KRAS G12C", "BRAF", "MET", "RET", "NTRK"
- "PD-L1", "tumor proportion score", "TPS"
- "osimertinib", "Tagrisso", "alectinib", "Alecensa", "sotorasib", "Lumakras"
- "pembrolizumab", "Keytruda", "durvalumab", "Imfinzi"
- "carboplatin", "cisplatin", "pemetrexed", "etoposide"
- "lobectomy", "pneumonectomy", "VATS", "thoracotomy"

**Clinical Cohorts**:
- "Generate a lung cancer patient"
- "I need an EGFR-positive lung cancer patient"
- "Create a patient with ALK-rearranged NSCLC"
- "Generate a small cell lung cancer patient"
- "Make a patient with lung cancer brain metastases"
- "I need a patient on immunotherapy for lung cancer"
- "Create a patient who progressed on osimertinib"

**Implicit Indicators**:
- User mentions thoracic oncology or pulmonary oncology
- User specifies smoking history or pack-years
- User asks about molecular testing or NGS panels
- User mentions checkpoint inhibitors in solid tumors
- User specifies stereotactic body radiation (SBRT)

**Co-occurring Mentions**:
- When user mentions lung cancer AND brain metastases
- When user mentions lung cancer AND COPD
- When user mentions lung cancer AND smoking cessation
- When user mentions lung cancer AND driver mutation

## Trigger Phrases

- lung cancer
- lung mass
- NSCLC
- SCLC
- EGFR
- ALK
- PD-L1
- osimertinib
- immunotherapy lung
- brain metastases

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| age_range | range | 55-75 | Patient age range |
| gender | enum | any | male, female, any |
| histology | enum | nsclc_adenocarcinoma | nsclc_adenocarcinoma, nsclc_squamous, nsclc_large_cell, sclc |
| stage | enum | IV | I, II, IIIA, IIIB, IIIC, IVA, IVB (NSCLC) or limited, extensive (SCLC) |
| driver_mutation | enum | none | none, egfr_common, egfr_exon20, alk, ros1, braf, kras_g12c, met_exon14, ret, ntrk |
| pdl1_status | enum | any | negative, low, high, any |
| smoking_status | enum | former | current, former, never |
| treatment_phase | enum | active | newly_diagnosed, active_treatment, surveillance, progression, palliative |
| has_brain_mets | boolean | false | Whether patient has CNS metastases |

## Domain Knowledge

### Histologic Classification

Lung cancer is divided into two major categories with fundamentally different biology and treatment.

**Non-Small Cell Lung Cancer (NSCLC) - 85%**:
```
Adenocarcinoma (40%):
  - Most common type overall
  - More common in never-smokers
  - Higher rate of actionable mutations (EGFR, ALK, ROS1)
  - Peripheral location common
  - Test ALL adenocarcinomas for molecular markers

Squamous Cell Carcinoma (25-30%):
  - Strongly associated with smoking
  - Central location (near major bronchi)
  - Lower rate of actionable mutations
  - PD-L1 often high
  - Pemetrexed contraindicated (use taxane instead)

Large Cell Carcinoma (10-15%):
  - Poorly differentiated
  - Can occur anywhere in lung
  - Treat similar to adenocarcinoma
```

**Small Cell Lung Cancer (SCLC) - 15%**:
```
Characteristics:
  - Aggressive, rapidly growing
  - Almost exclusively in smokers
  - Often metastatic at diagnosis
  - High initial response to chemo/radiation
  - High rate of relapse
  - Brain metastases very common

Staging:
  - Limited Stage: Confined to one hemithorax + regional nodes
    - Can be encompassed in tolerable radiation field
    - ~30% of SCLC at diagnosis
  - Extensive Stage: Beyond limited stage
    - Distant metastases or too extensive for radiation
    - ~70% of SCLC at diagnosis
```

**Why this matters for generation**: NSCLC and SCLC are treated completely differently. SCLC does NOT use targeted therapies. Never give osimertinib to SCLC. Always verify histology before selecting treatment.

### Actionable Biomarkers (NSCLC)

**Testing Requirements**:
```python
if histology in ["adenocarcinoma", "nsclc_nos", "large_cell"]:
    must_test = ["EGFR", "ALK", "ROS1", "BRAF", "KRAS", "MET", "RET", "NTRK", "PD-L1"]
    # Broad NGS panel preferred

if histology == "squamous":
    test_if_never_smoker = ["EGFR", "ALK", "ROS1"]  # Lower yield but still test
    always_test = ["PD-L1"]
```

**EGFR Mutations (10-15% of NSCLC, 40-50% in Asians)**:
```
Common Sensitizing Mutations:
  - Exon 19 deletion (45%): Best prognosis
  - L858R (exon 21) (40%): Good response to TKIs

Resistance Mutations:
  - T790M: Develops during 1st/2nd gen TKI therapy
  - C797S: Develops during osimertinib therapy

Exon 20 Insertions:
  - ~10% of EGFR mutations
  - Resistant to standard EGFR TKIs
  - Amivantamab or mobocertinib

Treatment Sequence:
  1st line: Osimertinib (3rd gen TKI, CNS penetrant)
  Progression: Rebiopsy for resistance mechanism
  2nd line: Based on resistance (platinum-chemo if C797S)
```

**ALK Rearrangements (3-5% of NSCLC)**:
```
Patient Profile:
  - Younger patients (median 50s)
  - Light or never smokers
  - Adenocarcinoma histology

Treatment Sequence:
  1st line: Alectinib (preferred) or lorlatinib
  2nd line: Lorlatinib (especially if CNS progression)
  Later lines: Chemotherapy

Key Points:
  - Long survival possible (median 5+ years)
  - High rate of brain mets (use CNS-penetrant TKI)
  - Sequential ALK TKIs can control disease for years
```

**ROS1 Rearrangements (1-2%)**:
```
Treatment:
  1st line: Crizotinib or entrectinib (CNS penetrant)
  2nd line: Lorlatinib

Similar to ALK in many ways:
  - Younger, never smokers
  - Adenocarcinoma
  - Favorable prognosis
```

**BRAF V600E (2-3%)**:
```
Treatment:
  Dabrafenib + trametinib (BRAF + MEK inhibitor combination)

Key Points:
  - Can occur in smokers or never smokers
  - Good responses to targeted therapy
```

**KRAS G12C (13% of NSCLC)**:
```
Treatment:
  - Sotorasib 960mg daily
  - Adagrasib 600mg BID

Key Points:
  - Most common driver mutation
  - Historically "undruggable"
  - Typically used after immunotherapy/chemo
  - Associated with smoking history
```

**MET Exon 14 Skipping (3-4%)**:
```
Treatment:
  Capmatinib or tepotinib

Key Points:
  - Often in older patients
  - Associated with smoking
  - Can occur with high PD-L1
```

**RET Fusions (1-2%)**:
```
Treatment:
  Selpercatinib or pralsetinib

Key Points:
  - Often in younger, never smokers
  - Highly active targeted agents
```

**NTRK Fusions (<1%)**:
```
Treatment:
  Larotrectinib or entrectinib

Key Points:
  - Rare but highly actionable
  - Tumor-agnostic indication
```

**PD-L1 Expression**:
```
Testing: IHC using 22C3 (pembrolizumab) or SP263 (other agents)
Reporting: Tumor Proportion Score (TPS)
  - <1%: Low/negative
  - 1-49%: Low positive
  - ≥50%: High positive

Treatment Implications:
  - TPS ≥50%: Pembrolizumab monotherapy option (no chemo)
  - TPS 1-49%: Pembrolizumab + chemotherapy
  - TPS <1%: Chemotherapy ± ipilimumab + nivolumab
```

### Staging and Workup

**Initial Workup**:
```
1. Imaging:
   - CT chest with contrast (or CT C/A/P)
   - PET-CT (staging, nodal involvement)
   - Brain MRI (required for Stage III-IV, recommended for all)

2. Tissue diagnosis:
   - CT-guided biopsy (peripheral lesions)
   - Bronchoscopy with biopsy (central lesions)
   - EBUS (mediastinal lymph nodes)
   - Thoracentesis (if pleural effusion)

3. Molecular testing (NSCLC):
   - NGS panel (comprehensive, preferred)
   - OR individual tests: EGFR, ALK (FISH/IHC), ROS1, BRAF, KRAS
   - PD-L1 IHC
   - Turnaround time: 1-2 weeks

4. Pulmonary function:
   - PFTs if surgery considered
   - FEV1 and DLCO predict surgical risk

5. Mediastinal staging (if surgery planned):
   - EBUS-TBNA (endobronchial ultrasound)
   - Mediastinoscopy if EBUS inconclusive
```

**NSCLC TNM Staging (AJCC 8th Edition)**:

| Stage | TNM | Description | 5-Year Survival |
|-------|-----|-------------|-----------------|
| IA1 | T1a N0 M0 | ≤1 cm, no nodes | 92% |
| IA2 | T1b N0 M0 | >1-2 cm, no nodes | 83% |
| IA3 | T1c N0 M0 | >2-3 cm, no nodes | 77% |
| IB | T2a N0 M0 | >3-4 cm, no nodes | 68% |
| IIA | T2b N0 M0 | >4-5 cm, no nodes | 60% |
| IIB | T1-2 N1 M0 | Any T1-2 with hilar nodes | 53% |
| IIB | T3 N0 M0 | >5-7 cm or local invasion | 53% |
| IIIA | Various | Locally advanced, resectable | 36% |
| IIIB | Various | Locally advanced, often unresectable | 26% |
| IIIC | T3-4 N3 M0 | Contralateral/scalene nodes | 13% |
| IVA | Any T, N, M1a-b | Contralateral lung, pleural, single distant met | 10% |
| IVB | Any T, N, M1c | Multiple distant mets | <1% (w/o driver) |

**SCLC Staging**:
```
Limited Stage:
  - Disease confined to one hemithorax
  - May include ipsilateral supraclavicular nodes
  - Can be encompassed in one radiation field
  - ~30% at diagnosis

Extensive Stage:
  - Anything beyond limited stage
  - Contralateral lung involvement
  - Distant metastases
  - Malignant pleural effusion
  - ~70% at diagnosis
```

### Treatment Pathways by Stage (NSCLC)

**Stage I-II (Resectable)**:
```
Standard Approach:
  1. Surgical resection (lobectomy preferred, VATS if possible)
  2. Mediastinal lymph node sampling/dissection
  3. Adjuvant therapy based on stage:
     - Stage IA: Observation only
     - Stage IB: Consider adjuvant chemo if high risk
     - Stage II: Adjuvant chemotherapy (cisplatin-based × 4 cycles)
     - EGFR+: Adjuvant osimertinib × 3 years

Non-surgical candidates:
  - SBRT (stereotactic body radiation) for Stage I
  - Excellent local control (>90%)
  - Option for medically inoperable patients
```

**Stage III (Locally Advanced)**:
```
Stage IIIA (Potentially Resectable):
  Option 1: Neoadjuvant chemoradiation → Surgery
  Option 2: Definitive chemoradiation → Durvalumab
  - Decision based on tumor board, patient factors

Stage IIIB-IIIC (Unresectable):
  1. Concurrent chemoradiation (6-7 weeks)
     - Cisplatin + etoposide OR carboplatin + paclitaxel
     - 60-66 Gy radiation
  2. Durvalumab consolidation × 1 year
     - If PD-L1 ≥1% (per FDA label) OR any PD-L1 (per NCCN)
     - Start within 1-42 days after chemoradiation
     - Monitor for pneumonitis

Key Toxicities:
  - Esophagitis (during radiation)
  - Pneumonitis (radiation and/or durvalumab)
  - Myelosuppression
```

**Stage IV (Metastatic) - Without Driver Mutation**:
```
PD-L1 ≥50% (no contraindication to immunotherapy):
  Option 1: Pembrolizumab monotherapy
  Option 2: Pembrolizumab + carboplatin + pemetrexed (non-squamous)
  Option 2: Pembrolizumab + carboplatin + paclitaxel (squamous)

PD-L1 1-49%:
  Pembrolizumab + platinum-doublet chemotherapy × 4 cycles
  Then pembrolizumab maintenance

PD-L1 <1%:
  Option 1: Platinum-doublet + pembrolizumab
  Option 2: Nivolumab + ipilimumab + chemo (CheckMate 9LA)

Non-squamous specific:
  - Pemetrexed-based (carboplatin + pemetrexed + pembrolizumab)
  - Pemetrexed maintenance

Squamous specific:
  - Taxane-based (carboplatin + paclitaxel + pembrolizumab)
  - NO pemetrexed (poor efficacy in squamous)
```

**Stage IV - With Driver Mutation**:
```
EGFR mutated:
  1st line: Osimertinib 80mg daily
  Progression: Rebiopsy → based on resistance mechanism

ALK rearranged:
  1st line: Alectinib 600mg BID or Lorlatinib 100mg daily
  Progression: Next-generation ALK TKI or chemotherapy

ROS1 rearranged:
  1st line: Entrectinib 600mg daily or crizotinib 250mg BID

BRAF V600E:
  1st line: Dabrafenib 150mg BID + trametinib 2mg daily

KRAS G12C:
  After progression on immunotherapy/chemo:
  Sotorasib 960mg daily or adagrasib 600mg BID

MET exon 14:
  1st line: Capmatinib 400mg BID or tepotinib 450mg daily

RET fusion:
  1st line: Selpercatinib 120mg BID or pralsetinib 400mg daily

NTRK fusion:
  1st line: Larotrectinib 100mg BID or entrectinib 600mg daily
```

### Treatment Pathways (SCLC)

**Limited Stage SCLC**:
```
Treatment Intent: Potentially curative

Standard Treatment:
  1. Concurrent chemoradiation
     - Cisplatin 60mg/m² D1 + Etoposide 120mg/m² D1-3 q3w × 4 cycles
     - OR Carboplatin AUC 5 + Etoposide (if cisplatin not tolerated)
     - Thoracic radiation 45Gy BID or 60-70Gy daily
     - Start radiation with cycle 1-2

  2. Prophylactic Cranial Irradiation (PCI)
     - If complete or partial response
     - Reduces brain mets from 40% to 15%
     - 25 Gy in 10 fractions
     - Cognitive effects possible

Response:
  - CR/PR in 80-90% of patients
  - Median survival: 17-23 months
  - 2-year survival: 20-40%
  - High relapse rate
```

**Extensive Stage SCLC**:
```
Treatment Intent: Palliative (not curative)

First-Line:
  Carboplatin AUC 5 D1 + Etoposide 100mg/m² D1-3 q3w × 4 cycles
  PLUS Atezolizumab 1200mg D1 q3w (or durvalumab 1500mg q3w)

  Then: Atezolizumab (or durvalumab) maintenance until progression

Second-Line (platinum-sensitive, ≥3 months):
  Rechallenge with platinum-etoposide ± immunotherapy

Second-Line (platinum-resistant, <3 months):
  - Topotecan 1.5mg/m² D1-5 q3w
  - OR Lurbinectedin 3.2mg/m² q3w

Prognosis:
  - Median survival: 12-14 months (with immunotherapy)
  - High initial response but rapid progression common
```

### Brain Metastases in Lung Cancer

Lung cancer has the highest rate of brain metastases of any solid tumor.

**Incidence**:
```
At diagnosis:
  - NSCLC: 10-20%
  - SCLC: 10-15% (limited), 15-25% (extensive)
  - EGFR/ALK positive: Higher rates

During disease course:
  - NSCLC: 30-50%
  - SCLC: 50-80%
```

**Presentation**:
- Headache, worse in morning
- Focal neurologic deficits
- Seizures
- Cognitive changes
- Often asymptomatic (found on staging MRI)

**Management**:
```
Symptomatic:
  - Dexamethasone 4-8mg q6h (edema reduction)
  - Antiepileptics if seizures (levetiracetam preferred)

Limited brain mets (1-4 lesions, good performance status):
  - Stereotactic radiosurgery (SRS): 15-24 Gy single fraction
  - High local control (80-90%)
  - Preserve cognition

Multiple brain mets or poor performance status:
  - Whole brain radiation therapy (WBRT): 30 Gy in 10 fractions
  - More cognitive impact than SRS
  - Consider hippocampal-sparing WBRT

With targetable driver:
  - CNS-penetrant TKIs first:
    - Osimertinib (EGFR) - excellent CNS activity
    - Alectinib, lorlatinib (ALK) - excellent CNS activity
    - Entrectinib (ROS1, NTRK) - good CNS activity
  - May defer radiation if CNS controlled on TKI
```

### Common Chemotherapy Regimens

**NSCLC Regimens**:

| Regimen | Components | Setting | Notes |
|---------|------------|---------|-------|
| Carboplatin-Pemetrexed-Pembrolizumab | Carbo AUC 5 + Pem 500mg/m² + Pembro 200mg q3w | 1st line non-squamous | Most common |
| Carboplatin-Paclitaxel-Pembrolizumab | Carbo AUC 6 + Pac 200mg/m² + Pembro 200mg q3w | 1st line squamous | |
| Cisplatin-Pemetrexed | Cis 75mg/m² + Pem 500mg/m² q3w | Adjuvant non-squamous | |
| Cisplatin-Vinorelbine | Cis 80mg/m² D1 + Vin 25mg/m² D1,8 q3w | Adjuvant | Alternative |
| Docetaxel | Doc 75mg/m² q3w | 2nd line | Single agent |

**SCLC Regimens**:

| Regimen | Components | Setting |
|---------|------------|---------|
| Carboplatin-Etoposide-Atezolizumab | Carbo AUC 5 D1 + Etop 100mg/m² D1-3 + Atezo 1200mg D1 q3w | ES-SCLC 1st line |
| Cisplatin-Etoposide | Cis 60mg/m² D1 + Etop 120mg/m² D1-3 q3w | LS-SCLC with RT |
| Topotecan | Topo 1.5mg/m² D1-5 q3w | 2nd line |
| Lurbinectedin | Lurbi 3.2mg/m² q3w | 2nd line |

### Treatment Toxicities

**Immunotherapy-Related Adverse Events**:
```
Pneumonitis (most important in lung cancer):
  - Incidence: 5-10% (higher with prior radiation)
  - Symptoms: Dyspnea, cough, hypoxia
  - Imaging: Ground-glass opacities, consolidation
  - Management:
    - Grade 1: Monitor, may continue treatment
    - Grade 2: Hold immunotherapy, prednisone 1mg/kg
    - Grade 3-4: Discontinue, high-dose steroids, consider infliximab

Other irAEs:
  - Colitis, hepatitis, thyroiditis
  - Adrenal insufficiency
  - Hypophysitis
  - Myocarditis (rare but serious)
```

**Targeted Therapy Toxicities**:
```
EGFR TKIs (osimertinib):
  - Rash (acneiform)
  - Diarrhea
  - Paronychia
  - Interstitial lung disease (rare, serious)
  - QT prolongation

ALK TKIs (alectinib):
  - Edema
  - Myalgias
  - Constipation
  - Hepatotoxicity
  - Bradycardia
```

**Chemotherapy Toxicities**:
```
Pemetrexed:
  - Myelosuppression
  - Requires B12 and folate supplementation
  - Skin rash

Platinum (carboplatin/cisplatin):
  - Myelosuppression (especially thrombocytopenia)
  - Nausea (cisplatin > carboplatin)
  - Nephrotoxicity (cisplatin)
  - Ototoxicity (cisplatin)
  - Neuropathy
```

## Generation Guidelines

### How to Apply This Knowledge

**When the user says**: "Generate a lung cancer patient"

**Claude should**:
1. **Select histology**: Adenocarcinoma (most common)
2. **Choose stage**: Stage IV (most common at diagnosis)
3. **Determine smoking history**: Former smoker (60 pack-years)
4. **Select driver mutation**: None (most common) or EGFR (if never-smoker)
5. **Set PD-L1**: Variable based on cohort
6. **Generate appropriate treatment pathway**

**When the user says**: "Generate an EGFR-positive lung cancer patient"

**Claude should**:
1. **Set histology**: Adenocarcinoma (required for EGFR)
2. **Set EGFR status**: Positive (exon 19 del or L858R)
3. **Patient profile**:
   - More likely female
   - More likely never/light smoker
   - More likely Asian ethnicity
4. **Treatment**: Osimertinib first-line
5. **Include CNS surveillance**: Brain MRI, CNS penetrant therapy

**When the user says**: "Generate a small cell lung cancer patient"

**Claude should**:
1. **Set histology**: SCLC
2. **Set stage**: Limited or Extensive (70% extensive)
3. **Patient profile**:
   - Heavy smoking history (virtually always)
   - Often symptomatic at presentation
4. **Treatment**:
   - Limited: Concurrent chemoradiation + PCI
   - Extensive: Platinum-etoposide + immunotherapy
5. **Emphasize**: Rapid progression, frequent brain mets

### Coherence Checks

Before finalizing a lung cancer patient, verify:

```python
# 1. Histology-treatment coherence
if histology == "sclc":
    assert no_targeted_therapy, "SCLC does not use TKIs"
    assert staging in ["limited", "extensive"], "Use SCLC staging"
    assert has_heavy_smoking_history, "SCLC nearly always in smokers"

if histology == "squamous":
    assert no_pemetrexed, "Pemetrexed not effective in squamous"
    assert low_probability_driver_mutation, "Drivers rare in squamous"

# 2. Driver mutation-treatment coherence
if egfr_mutated:
    assert treatment_includes_egfr_tki, "EGFR+ must have TKI"
    assert histology != "sclc", "SCLC doesn't have EGFR mutations"

if alk_rearranged:
    assert treatment_includes_alk_tki, "ALK+ must have TKI"
    assert likely_never_smoker, "ALK common in never smokers"

# 3. PD-L1-treatment coherence
if pdl1_high and no_driver_mutation:
    pembrolizumab_monotherapy_is_option = True

if immunotherapy_given:
    assert no_autoimmune_disease_contraindication
    monitor_for_pneumonitis = True

# 4. Brain metastases coherence
if has_brain_mets:
    assert brain_mri_performed, "Must have brain MRI"
    assert treatment_addresses_cns, "Need SRS/WBRT or CNS-penetrant agent"

# 5. Stage-treatment intent coherence
if stage in ["I", "II"]:
    assert treatment_intent in ["curative", "adjuvant"]
    consider_surgery = True

if stage == "IV" or sclc_extensive:
    assert treatment_intent == "palliative"
```

## Example Requests and Interpretations

### Example 1: Metastatic NSCLC Without Driver

**User says**: "Generate a lung cancer patient on immunotherapy"

**Claude interprets**:
- Histology: Adenocarcinoma
- Stage: IV (immunotherapy for metastatic)
- Driver mutation: Negative (all tested)
- PD-L1: High (≥50%) - immunotherapy monotherapy option

**Key features Claude generates**:

**Demographics**: Age 67, male, former smoker (40 pack-years, quit 5 years ago)

**Presentation**: 3-month history of cough, 15-lb weight loss, incidental pulmonary nodule on CT

**Pathology** (CT-guided biopsy):
- Adenocarcinoma, moderately differentiated
- TTF-1 positive, Napsin A positive
- PD-L1: 70% (TPS)

**Molecular Testing** (NGS panel):
- EGFR: Wild-type
- ALK: No rearrangement
- ROS1: No rearrangement
- BRAF: Wild-type
- KRAS: G12V (not G12C, not targetable)
- MET: No exon 14 skipping
- RET: No fusion
- NTRK: No fusion

**Staging**:
- Primary: 4.2 cm right upper lobe mass
- PET-CT: Right hilar and mediastinal nodes, adrenal met
- Brain MRI: No metastases
- Stage IVA (T2a N2 M1b - single adrenal met)

**Treatment Plan**:
- Pembrolizumab 200mg IV q3w monotherapy (PD-L1 ≥50%)
- Cycle 1 of planned 35 cycles (2 years)

**Current Status** (Cycle 6):
- CT shows partial response (35% decrease)
- Tolerating well
- Grade 1 fatigue, Grade 1 hypothyroidism (on levothyroxine)
- No pneumonitis

**Labs**:
- WBC: 6.2
- Hemoglobin: 12.5
- TSH: 8.5 (elevated, on replacement)
- LFTs: Normal

**ICD-10 Codes**:
- C34.11 (Malignant neoplasm upper lobe, right lung)
- C79.70 (Secondary malignant neoplasm of adrenal gland)
- Z51.12 (Encounter for antineoplastic immunotherapy)

---

### Example 2: EGFR-Positive with CNS Progression

**User says**: "Generate an EGFR-positive lung cancer patient with brain metastases"

**Claude interprets**:
- Histology: Adenocarcinoma
- Driver: EGFR mutation
- Stage: IV with CNS involvement
- Treatment: Osimertinib (CNS-penetrant)

**Key features Claude generates**:

**Demographics**: Age 58, female, never smoker, Asian

**Cancer History**:
- Diagnosed 18 months ago with Stage IVB adenocarcinoma
- EGFR exon 19 deletion positive
- PD-L1: 5%
- Initial sites: Bilateral lung nodules, bone (T10, L2)

**Initial Treatment**:
- Osimertinib 80mg daily
- Excellent response at 3 months (60% decrease)
- Continued stable disease for 15 months

**Current Presentation**:
- New headaches, word-finding difficulty
- Brain MRI: 3 new enhancing lesions (right frontal, left parietal, cerebellar)
- Extracranial disease stable

**Current Molecular Status**:
- Liquid biopsy (circulating tumor DNA):
  - EGFR exon 19 del: Detected
  - EGFR C797S: Detected (osimertinib resistance mutation)
  - No MET amplification

**Treatment Plan**:
1. Stereotactic radiosurgery (SRS) to brain lesions
2. Continue osimertinib (may have some ongoing activity)
3. Plan for tissue biopsy if accessible for full resistance profiling
4. Consider clinical trial or platinum-based chemotherapy

**Performance Status**: ECOG 1

**Medications**:
- Osimertinib 80mg PO daily (continuing)
- Dexamethasone 4mg PO BID (for cerebral edema)
- Levetiracetam 500mg PO BID (seizure prophylaxis)
- Zoledronic acid 4mg IV monthly (bone mets)

**Labs**:
- WBC: 5.8
- Hemoglobin: 11.2
- Creatinine: 0.9
- LFTs: AST 42, ALT 38 (slightly elevated, osimertinib)

**ICD-10 Codes**:
- C34.92 (Malignant neoplasm left lung)
- C79.31 (Secondary malignant neoplasm of brain)
- C79.51 (Secondary malignant neoplasm of bone)

---

### Example 3: ALK-Positive NSCLC

**User says**: "Generate an ALK-positive lung cancer patient"

**Claude interprets**:
- Histology: Adenocarcinoma
- Driver: ALK rearrangement
- Patient profile: Younger, never/light smoker
- Treatment: ALK TKI (alectinib or lorlatinib)

**Key features Claude generates**:

**Demographics**: Age 45, male, never smoker

**Presentation**: Cough and dyspnea for 2 months, found to have large right-sided pleural effusion

**Pathology** (Thoracentesis cytology + cell block):
- Adenocarcinoma, TTF-1 positive
- ALK: Positive by IHC (confirmed by FISH)
- EGFR, ROS1, BRAF: Wild-type/negative
- PD-L1: 25%

**Staging**:
- Primary: 3.5 cm right lower lobe mass
- Large malignant right pleural effusion
- Brain MRI: 8mm left parietal lesion (asymptomatic)
- Stage IVA (T2a N0 M1a, malignant effusion + brain met)

**Treatment Plan**:
- Alectinib 600mg PO BID (CNS-penetrant ALK TKI)
- PleurX catheter for pleural effusion drainage

**Current Status** (Month 8):
- Excellent response
- CT: Primary decreased to 1.2 cm, minimal pleural fluid
- Brain MRI: Complete response of brain lesion
- PleurX removed (no more drainage)

**Tolerating Treatment**:
- Grade 1 edema (ankles)
- Grade 1 constipation
- No hepatotoxicity

**Labs**:
- CBC: Normal
- LFTs: AST 28, ALT 32 (normal)
- CPK: 180 (slightly elevated, monitor)

**Expected Course**:
- Long-term disease control possible (median PFS ~35 months)
- Will monitor for CNS progression
- Lorlatinib available at progression

---

### Example 4: Limited Stage SCLC

**User says**: "Generate a limited stage small cell lung cancer patient"

**Claude interprets**:
- Histology: SCLC
- Stage: Limited
- Treatment: Concurrent chemoradiation + PCI
- Prognosis: Potentially curable but high relapse risk

**Key features Claude generates**:

**Demographics**: Age 62, female, current smoker (45 pack-years)

**Presentation**: 6-week cough, hemoptysis, 20-lb weight loss

**Imaging**:
- CT: 5.2 cm right hilar mass with right paratracheal adenopathy
- PET-CT: FDG-avid right hilar mass (SUV 18) and mediastinal nodes
  - No extrathoracic uptake
- Brain MRI: No metastases

**Pathology** (EBUS biopsy):
- Small cell carcinoma
- TTF-1 positive
- Chromogranin and synaptophysin positive
- Ki-67: 90%

**Staging**: Limited stage SCLC

**Treatment Plan**:
1. Concurrent chemoradiation:
   - Cisplatin 60mg/m² D1 + Etoposide 120mg/m² D1-3 q3w × 4 cycles
   - Twice-daily thoracic radiation (45 Gy) starting Cycle 1
2. If response: Prophylactic cranial irradiation (PCI)

**Current Status** (After Cycle 4):
- CT: Near-complete response (residual 1.1 cm nodule)
- PET: No FDG-avid disease
- Completed radiation
- Plan for PCI (25 Gy in 10 fractions)

**Toxicities During Treatment**:
- Grade 3 esophagitis (required PEG tube weeks 3-5)
- Grade 2 neutropenia (delayed Cycle 4 by 1 week)
- Grade 2 fatigue

**Labs**:
- WBC: 4.2 (recovered)
- Hemoglobin: 10.8 (treatment-related anemia)
- Platelets: 145

**Prognosis Discussion**:
- Good response to treatment
- Median survival 17-23 months with LS-SCLC
- PCI reduces brain mets but has cognitive effects
- Close surveillance required (high relapse rate)

---

### Example 5: Extensive Stage SCLC

**User says**: "Generate an extensive stage small cell lung cancer patient"

**Claude interprets**:
- Histology: SCLC
- Stage: Extensive
- Treatment: Platinum-etoposide + immunotherapy
- Prognosis: Poor, palliative intent

**Key features Claude generates**:

**Demographics**: Age 68, male, current smoker (60 pack-years)

**Presentation**: Severe dyspnea, facial swelling (SVC syndrome)

**Imaging**:
- CT: Large right hilar mass encasing SVC, multiple bilateral lung nodules
- Liver: Multiple hepatic metastases (largest 4.2 cm)
- Brain MRI: 2 small asymptomatic brain mets
- Bone scan: T8, L3, right femur

**Pathology** (Liver biopsy):
- Small cell carcinoma
- TTF-1 positive, synaptophysin positive

**Staging**: Extensive stage SCLC

**Treatment Plan**:
- Carboplatin AUC 5 D1 + Etoposide 100mg/m² D1-3 q3w × 4 cycles
- Atezolizumab 1200mg D1 q3w (with chemo, then maintenance)
- SVC stent placed urgently
- Dexamethasone for brain mets
- Whole brain radiation after chemotherapy

**Current Status** (Cycle 2, Day 1):
- SVC syndrome resolved after stent
- Symptomatically improved
- CT (interim): Partial response (40% decrease)

**Performance Status**: ECOG 2 (improved from ECOG 3)

**Medications**:
- Atezolizumab + carboplatin + etoposide (Cycle 2 today)
- Dexamethasone 4mg BID
- Ondansetron 8mg PRN
- Enoxaparin 40mg SQ daily (VTE prophylaxis)

**Prognosis**:
- Median survival ~12-14 months with immunotherapy
- High likelihood of progression within 6-12 months
- Goals of care discussion documented

## Variations

### Variation: Early Stage Resectable NSCLC
Incidental or screen-detected Stage I-II proceeding to surgery.
- histology: nsclc_adenocarcinoma or nsclc_squamous
- stage: I or II
- **Includes**:
  - Low-dose CT screening detection (if applicable)
  - PET-CT staging
  - PFTs to assess surgical candidacy
  - Lobectomy (preferred) or sublobar resection
  - Mediastinal lymph node sampling
  - Adjuvant chemotherapy (Stage II+)
  - Adjuvant osimertinib if EGFR+ (Stage IB-IIIA)
- **Surveillance**: CT q6mo × 2 years, then annually

### Variation: Locally Advanced Unresectable IIIB
Stage IIIB/IIIC treated with definitive chemoradiation.
- stage: IIIB or IIIC
- treatment_phase: active_treatment
- **Includes**:
  - Concurrent chemoradiation (6-7 weeks)
  - Cisplatin-etoposide or carboplatin-paclitaxel with RT
  - Durvalumab consolidation × 1 year
  - Pneumonitis monitoring (radiation + immunotherapy)
- **Key Toxicities**: Esophagitis, pneumonitis, fatigue

### Variation: Metastatic EGFR-Positive
Stage IV adenocarcinoma with actionable EGFR mutation.
- stage: IV
- driver_mutation: egfr_common
- smoking_status: never or light
- **Includes**:
  - Osimertinib 80mg daily first-line
  - Brain MRI surveillance (even if asymptomatic at baseline)
  - Liquid biopsy at progression for resistance mechanism
  - T790M testing (if on 1st/2nd gen TKI)
  - Sequential therapies based on resistance
- **Expected PFS**: ~18-22 months on osimertinib

### Variation: Metastatic ALK-Positive
Stage IV adenocarcinoma with ALK rearrangement.
- stage: IV
- driver_mutation: alk
- smoking_status: never
- **Includes**:
  - Younger patient (median age 50s)
  - Alectinib or lorlatinib first-line
  - Excellent CNS penetration
  - Long survival possible (5+ years)
  - Sequential ALK TKIs at progression
- **Brain Mets**: High rate, use CNS-penetrant TKI

### Variation: Metastatic High PD-L1
Stage IV NSCLC without driver, PD-L1 ≥50%.
- stage: IV
- driver_mutation: none
- pdl1_status: high
- **Includes**:
  - Pembrolizumab monotherapy option (no chemo)
  - OR chemo-immunotherapy combination
  - irAE monitoring (pneumonitis critical)
  - Response assessment q9 weeks
- **Durable Responses**: 15-20% long-term survivors

### Variation: Metastatic KRAS G12C
Stage IV with KRAS G12C mutation.
- stage: IV
- driver_mutation: kras_g12c
- smoking_status: current or former
- **Includes**:
  - First-line: Immunotherapy + chemotherapy (KRAS inhibitor not 1st line approved)
  - Second-line: Sotorasib 960mg daily or adagrasib 600mg BID
  - GI toxicity monitoring (diarrhea, nausea)
- **Note**: Most common driver mutation but targeted therapy typically 2nd line+

### Variation: Limited Stage SCLC
SCLC confined to one hemithorax with curative intent treatment.
- histology: sclc
- stage: limited
- **Includes**:
  - Concurrent chemoradiation
  - Cisplatin-etoposide × 4 cycles
  - Twice-daily or once-daily thoracic RT
  - PCI if response achieved
  - High initial response rate (80-90%)
  - Frequent relapse despite good response

### Variation: Extensive Stage SCLC
Metastatic SCLC with poor prognosis.
- histology: sclc
- stage: extensive
- **Includes**:
  - Carboplatin-etoposide + atezolizumab (or durvalumab)
  - 4 cycles chemo, then immunotherapy maintenance
  - Consider WBRT if brain mets
  - Second-line: topotecan or lurbinectedin
  - Early palliative care integration
- **Median Survival**: 12-14 months

### Variation: Lung Cancer with Brain Metastases
NSCLC with CNS involvement at diagnosis or progression.
- has_brain_mets: true
- **Includes**:
  - Brain MRI findings (number, location, size)
  - Neurologic symptoms if symptomatic
  - Treatment: SRS vs WBRT based on number/size
  - Steroids for edema
  - CNS-penetrant systemic therapy if driver positive
  - Neurocognitive monitoring post-WBRT
- **Common in**: EGFR+, ALK+, SCLC

### Variation: Never-Smoker Lung Cancer
Adenocarcinoma in patient without smoking history.
- smoking_status: never
- histology: nsclc_adenocarcinoma
- **Includes**:
  - Higher probability of driver mutation (60-70%)
  - Test comprehensively for all drivers
  - Often female, younger
  - EGFR (50%), ALK (15%), ROS1 (5%), RET (3%)
  - Better prognosis than smoking-related NSCLC
- **Always obtain NGS** in never-smokers

## Composite Patterns

### Lung Cancer with COPD
```yaml
description: Lung cancer in patient with underlying COPD
combines: [lung-cancer.md, respiratory physiology]
shared_considerations:
  - Pulmonary function testing essential before surgery
  - FEV1 ≥1.5L (or ≥60% predicted) for lobectomy
  - DLCO assessment (fibrosis/emphysema)
  - Higher radiation pneumonitis risk
  - Oxygen requirements may increase during treatment
  - Smoking cessation critical
  - Concurrent COPD medications (inhalers)
typical_patient:
  - Heavy smoking history (60+ pack-years)
  - Baseline O2 requirement
  - FEV1 50-60% predicted
  - May be deemed inoperable → SBRT or definitive RT
```

### Lung Cancer with Brain Metastases
```yaml
description: Management of CNS involvement
includes:
  - Brain MRI protocol (thin cuts, contrast)
  - Symptoms: headache, neuro deficits, seizures
  - SRS for oligometastatic (1-4 lesions)
  - WBRT for multiple mets or poor performance status
  - Hippocampal-sparing WBRT to preserve cognition
  - Dexamethasone for edema
  - CNS-penetrant systemic therapy:
    - Osimertinib (EGFR)
    - Alectinib, lorlatinib (ALK)
    - Entrectinib (ROS1, NTRK)
  - Pembrolizumab has CNS activity
treatment_sequence:
  - Asymptomatic, driver+: Start TKI, defer radiation
  - Symptomatic: SRS/WBRT + systemic therapy
  - Progression on TKI: Local therapy (SRS) + continue/change systemic
```

### Lung Cancer with VTE
```yaml
description: Venous thromboembolism in lung cancer
includes:
  - High VTE incidence in lung cancer (10-15%)
  - PE symptoms vs tumor-related dyspnea
  - Anticoagulation with LMWH or DOAC
  - Contraindications: brain mets (relative), bleeding
  - Catheter-related thrombosis (port-associated)
  - Duration: Continue while cancer active
  - IVC filter if anticoagulation contraindicated
medications:
  - Enoxaparin 1mg/kg BID (preferred in cancer)
  - OR Rivaroxaban 15mg BID × 21d, then 20mg daily
  - OR Apixaban 10mg BID × 7d, then 5mg BID
```

### Lung Cancer with Immunotherapy Pneumonitis
```yaml
description: Development of checkpoint inhibitor pneumonitis
includes:
  - Symptoms: New/worsening dyspnea, cough, hypoxia
  - Imaging: New ground-glass, consolidation (CT)
  - Rule out: Infection, progression, PE, radiation pneumonitis
  - Grading and management:
    - Grade 1: Monitor, may continue
    - Grade 2: Hold immunotherapy, prednisone 1-2mg/kg
    - Grade 3+: Discontinue permanently, high-dose steroids
    - Refractory: Infliximab or mycophenolate
  - Taper steroids over 4-6 weeks
  - May or may not rechallenge (shared decision)
risk_factors:
  - Prior thoracic radiation
  - Underlying lung disease
  - Combination immunotherapy
```

### Lung Cancer with Paraneoplastic Syndrome
```yaml
description: Paraneoplastic manifestations (especially SCLC)
includes:
  - SIADH (hyponatremia): Most common in SCLC
  - Lambert-Eaton syndrome (weakness)
  - Cushing syndrome (ectopic ACTH)
  - Hypercalcemia (squamous cell)
  - Limbic encephalitis (anti-Hu antibodies)
management:
  - Treat underlying cancer
  - Specific therapy for syndrome:
    - SIADH: Fluid restriction, tolvaptan
    - Hypercalcemia: IV fluids, zoledronic acid
  - Paraneoplastic often improves with cancer treatment
```

## Generation Rules

### Demographics
- **Age**: 55-75 years (median ~70)
- **Gender**: Male slightly more common (historically), female increasing
- **Smoking**: Current (30%), former (50%), never (20% of adenocarcinoma)

### Conditions

**Primary Diagnosis**:
- Adenocarcinoma (C34.x) - 40%
- Squamous cell carcinoma (C34.x) - 25%
- Small cell carcinoma (C34.x) - 15%
- Large cell carcinoma (C34.x) - 10%
- NSCLC NOS (C34.x) - 10%

**Common Comorbidities**:
- COPD (J44.x) - 40-50%
- Coronary artery disease (I25.x) - 25%
- Hypertension (I10) - 50%
- Type 2 diabetes (E11.x) - 20%
- Prior malignancy - 15%

**Treatment-Related Conditions**:
- Pneumonitis (J84.89) - immunotherapy or radiation
- Anemia (D64.9) - chemotherapy
- Neuropathy (G62.0) - platinum, taxane
- Hypothyroidism (E03.9) - immunotherapy
- VTE (I82.x) - cancer-associated

### Vital Signs

**At Diagnosis (symptomatic patient)**:
- SpO2: 90-95% on room air (may be hypoxic)
- Heart Rate: 80-100 bpm
- Respiratory Rate: 18-24 (tachypnea common)
- Blood Pressure: Variable
- Weight: Often recent loss (>5%)

**During Treatment**:
- Monitor SpO2 closely (pneumonitis, progression)
- Weight trends (response indicator)

### Laboratory

**At Diagnosis**:
- CBC: Often normal or mild anemia
- CMP: LFTs, creatinine (baseline before treatment)
- LDH: May be elevated (tumor burden marker)

**SCLC-Specific**:
- Sodium: May be low (SIADH in 15-20%)
- LDH: Often elevated

**During Treatment**:
```
Immunotherapy monitoring:
  - TSH q6 weeks (thyroiditis)
  - LFTs (hepatitis)
  - Glucose (diabetes from steroids if pneumonitis)

Chemotherapy monitoring:
  - CBC before each cycle
  - CMP (renal function for platinum)
```

### Medications

**NSCLC Systemic Therapy**:
```
First-line (no driver, high PD-L1):
  - Pembrolizumab 200mg IV q3w

First-line (no driver, with chemo):
  - Carboplatin AUC 5 + Pemetrexed 500mg/m² + Pembrolizumab 200mg q3w × 4
  - Then pemetrexed + pembrolizumab maintenance

EGFR+:
  - Osimertinib 80mg PO daily

ALK+:
  - Alectinib 600mg PO BID
```

**SCLC Systemic Therapy**:
```
Extensive stage:
  - Carboplatin AUC 5 D1 + Etoposide 100mg/m² D1-3 + Atezolizumab 1200mg D1 q3w
  - × 4 cycles, then atezolizumab maintenance

Limited stage:
  - Cisplatin 60mg/m² D1 + Etoposide 120mg/m² D1-3 q3w × 4
  - With concurrent thoracic radiation
```

**Supportive Care**:
- Ondansetron 8mg (antiemetic)
- Dexamethasone (antiemetic, brain mets, pneumonitis)
- B12 1000mcg IM + Folic acid 1mg PO (for pemetrexed)
- Pegfilgrastim (if indicated)
- Zoledronic acid (bone mets)

### Timeline

**Stage I NSCLC (Screen-detected)**:
- Week 0: Abnormal LDCT screening
- Week 1-2: Diagnostic CT, PET-CT
- Week 2-3: Biopsy, molecular testing sent
- Week 3-4: Molecular results, tumor board
- Week 4-6: PFTs, surgical evaluation
- Week 6-8: Lobectomy
- Week 10: Final pathology, adjuvant decision
- Week 12+: Surveillance or adjuvant therapy

**Stage IV NSCLC with Driver**:
- Week 0: Symptomatic presentation
- Week 1: CT, brain MRI, biopsy
- Week 2: Pathology, molecular testing sent
- Week 2-3: Start empiric treatment if symptomatic
- Week 3: Molecular results available
- Week 3: Start targeted therapy (e.g., osimertinib)
- Week 9: First restaging CT
- Ongoing: CT q9-12 weeks

**Extensive SCLC**:
- Week 0: Presentation (often symptomatic)
- Week 1: Staging, liver biopsy
- Week 1-2: Start carboplatin-etoposide-atezolizumab C1
- Week 4, 7, 10: Cycles 2-4
- Week 12: Restaging CT
- Ongoing: Atezolizumab maintenance q3w

## References

**Clinical Guidelines**:
- NCCN Guidelines for Non-Small Cell Lung Cancer (Version 1.2024)
- NCCN Guidelines for Small Cell Lung Cancer (Version 1.2024)
- ASCO Guidelines for Systemic Therapy for Stage IV NSCLC
- ESMO Clinical Practice Guidelines for Lung Cancer

**Key Clinical Trials**:
- FLAURA (osimertinib 1st line EGFR): Soria et al, NEJM 2018
- ALEX (alectinib 1st line ALK): Peters et al, NEJM 2017
- KEYNOTE-024 (pembrolizumab monotherapy high PD-L1): Reck et al, NEJM 2016
- KEYNOTE-189 (pembrolizumab + chemo): Gandhi et al, NEJM 2018
- PACIFIC (durvalumab post-chemoRT): Antonia et al, NEJM 2017
- IMpower133 (atezolizumab ES-SCLC): Horn et al, NEJM 2018
- CodeBreaK 100 (sotorasib KRAS G12C): Skoulidis et al, NEJM 2021

**Molecular Testing**:
- CAP/IASLC/AMP Molecular Testing Guidelines
- ASCO Provisional Clinical Opinion: Liquid Biopsy

## Clinical Validation Notice

This cohort skill was AI-generated and requires clinical validation before use in any production or clinical decision-support context. The information provided is intended for synthetic data generation for testing and training purposes only.

Key areas requiring validation:
- Molecular testing algorithms and current actionable mutations
- Treatment regimen accuracy and sequencing
- Staging criteria per current AJCC/VA guidelines
- Drug dosing and current approvals
- SCLC staging and treatment protocols

Last validation review: Pending

## Validation Rules

| Rule | Requirement | Example |
|------|-------------|---------|
| Stage | I, II, III, IV (or IA-IVB) | Stage IIIA |
| Histology | NSCLC, SCLC, adenocarcinoma, etc. | "adenocarcinoma" |
| EGFR status | mutated, wild-type, specific mutation | "L858R mutation" |
| ALK status | positive, negative | "negative" |
| PD-L1 TPS | 0-100% | 80% |
| Tumor size | cm | 3.5 cm |
| Node status | N0, N1, N2, N3 | N2 |
| Performance status | ECOG 0-4 | ECOG 1 |

### Business Rules

- **NSCLC vs SCLC**: Different staging, treatment, and prognosis
- **Biomarker Testing**: EGFR, ALK, ROS1, BRAF, PD-L1 required for NSCLC
- **EGFR+**: Osimertinib first-line for exon 19 del or L858R
- **ALK+**: Alectinib or brigatinib first-line
- **PD-L1 High (≥50%)**: Pembrolizumab monotherapy option
- **Stage I-II**: Surgery +/- adjuvant therapy
- **Stage III**: Chemoradiation +/- immunotherapy consolidation
- **Stage IV**: Systemic therapy; targeted if actionable mutation

## Related Skills

### PatientSim Cohorts

- [../SKILL.md](../SKILL.md) - PatientSim overview
- [breast-cancer.md](breast-cancer.md) - Similar oncology cohort structure
- [colorectal-cancer.md](colorectal-cancer.md) - Similar oncology cohort structure
- [../sepsis-acute-care.md](../sepsis-acute-care.md) - Oncology patients with neutropenic fever

### Cross-Product: MemberSim

- [../../membersim/professional-claims.md](../../membersim/professional-claims.md) - Oncology office visit billing
- [../../membersim/facility-claims.md](../../membersim/facility-claims.md) - Chemotherapy infusion, surgery, radiation claims
- [../../membersim/prior-authorization.md](../../membersim/prior-authorization.md) - Oncology drug authorization

### Cross-Product: RxMemberSim

- [../../rxmembersim/specialty-pharmacy.md](../../rxmembersim/specialty-pharmacy.md) - Targeted therapies (osimertinib, alectinib), immunotherapy
- [../../rxmembersim/rx-prior-auth.md](../../rxmembersim/rx-prior-auth.md) - Specialty drug authorization

### Reference Files

- [../../../references/data-models.md](../../../references/data-models.md) - Entity schemas
- [../../../references/code-systems.md](../../../references/code-systems.md) - ICD-10, CPT, HCPCS codes
