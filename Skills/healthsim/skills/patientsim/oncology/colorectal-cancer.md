---
name: colorectal-cancer
description: "Colorectal cancer patient journeys from screening through surgery, adjuvant therapy, and surveillance. Triggers: colon cancer, rectal cancer, colorectal, GI oncology, FOLFOX, FOLFIRI, MSI, dMMR, Lynch syndrome, KRAS, NRAS, BRAF, cetuximab, colonoscopy"
---

# Colorectal Cancer Management

Comprehensive cohort skill for generating realistic colorectal cancer patient journeys, covering colon and rectal cancer from screening detection through surgery, adjuvant therapy, metastatic treatment, and surveillance.

## For Claude

Use this skill when generating colorectal cancer patients across the care continuum. This teaches you how to generate **realistic clinical event sequences** for colorectal cancer patients - from screening colonoscopy through diagnosis, staging, treatment, and long-term surveillance.

**When to apply this skill:**
- User mentions colon cancer, rectal cancer, or colorectal cancer
- User requests GI oncology or colorectal treatment cohorts
- User specifies FOLFOX, FOLFIRI, or other colorectal regimens
- User asks about MSI/dMMR status or Lynch syndrome
- User mentions KRAS, NRAS, or BRAF testing in colorectal context
- User asks about anti-EGFR therapy (cetuximab, panitumumab)
- User needs liver metastases cohorts (common in CRC)
- User requests colonoscopy screening or polyp surveillance

**Key capabilities this skill provides:**
- How to generate complete treatment timelines based on site (colon vs rectum) and stage
- How to distinguish colon cancer management (surgery first) from rectal cancer (often neoadjuvant first)
- How to apply biomarker status to treatment selection (RAS, BRAF, MSI)
- How to model liver-limited metastatic disease with curative intent
- How to incorporate sidedness (left vs right) into treatment decisions
- How to generate hereditary syndrome patterns (Lynch, FAP)
- How to structure screening and surveillance colonoscopy schedules

**Important**: Site matters in colorectal cancer. Colon cancer typically gets surgery first, then adjuvant chemotherapy. Locally advanced rectal cancer often needs neoadjuvant chemoradiation before surgery. ALWAYS confirm RAS mutation status before considering anti-EGFR therapy - mutated RAS excludes these agents.

## Metadata
- **Type**: cohort-template
- **Version**: 1.0
- **Author**: Claude (AI-generated, requires clinical validation)
- **Tags**: oncology, colorectal-cancer, colon-cancer, rectal-cancer, folfox, msi, kras, colonoscopy, lynch-syndrome
- **Dependencies**:
  - skills/healthcare/oncology-domain.md
  - skills/references/oncology/
- **Updated**: 2025-12-11

## Purpose

This cohort generates realistic colorectal cancer patients across the disease spectrum, from screen-detected polyps and early-stage cancers through metastatic disease. It simulates the multi-disciplinary approach to colorectal cancer care including surgery, radiation (primarily rectal), chemotherapy, and targeted/immunotherapy.

The cohort is designed to:
- Model realistic colorectal cancer presentations (screening vs symptomatic)
- Distinguish colon from rectal cancer management approaches
- Generate appropriate staging workups and biomarker testing
- Simulate treatment planning based on stage, site, and molecular profile
- Support potentially curative metastatic disease (liver-limited)
- Include hereditary syndromes (Lynch, FAP)
- Cover screening and surveillance patterns

## When to Use This Skill

Apply this skill when the user's request involves:

**Direct Keywords**:
- "colon cancer", "rectal cancer", "colorectal cancer", "CRC"
- "colonoscopy", "polyp", "adenoma", "polypectomy"
- "FOLFOX", "FOLFIRI", "CAPOX", "FOLFOXIRI"
- "MSI-H", "dMMR", "microsatellite instability", "mismatch repair"
- "KRAS", "NRAS", "RAS wild-type", "BRAF V600E"
- "cetuximab", "Erbitux", "panitumumab", "Vectibix"
- "Lynch syndrome", "HNPCC", "FAP", "familial adenomatous polyposis"
- "CEA", "carcinoembryonic antigen"
- "liver metastases", "hepatectomy", "colorectal liver mets"
- "TME", "total mesorectal excision", "LAR", "APR"

**Clinical Cohorts**:
- "Generate a colon cancer patient"
- "I need a patient with rectal cancer on neoadjuvant therapy"
- "Create a patient with colorectal liver metastases"
- "Generate an MSI-high colorectal cancer patient"
- "Make a patient with KRAS-mutated metastatic colon cancer"
- "I need a Lynch syndrome patient with colon cancer"
- "Create a patient undergoing colonoscopy surveillance"

**Implicit Indicators**:
- User mentions GI oncology or colorectal surgery
- User asks about 5-fluorouracil or oxaliplatin
- User specifies pelvic radiation or chemoradiation
- User mentions tumor board for liver resection
- User asks about hereditary cancer syndromes

**Co-occurring Mentions**:
- When user mentions colorectal cancer AND liver metastases
- When user mentions colorectal cancer AND immunotherapy eligibility
- When user mentions colorectal cancer AND genetic testing
- When user mentions colorectal cancer AND screening colonoscopy

## Trigger Phrases

- colon cancer
- rectal cancer
- colorectal cancer
- colonoscopy
- FOLFOX
- MSI-H
- KRAS
- liver metastases
- Lynch syndrome
- CEA

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| age_range | range | 55-75 | Patient age range |
| gender | enum | any | male, female, any |
| site | enum | colon | colon, rectum |
| colon_location | enum | any | right (cecum, ascending, hepatic flexure), transverse, left (splenic flexure, descending, sigmoid) |
| stage | enum | III | I, IIA, IIB, IIC, IIIA, IIIB, IIIC, IVA, IVB, IVC |
| msi_status | enum | mss | msi_high, mss (microsatellite stable) |
| ras_status | enum | any | wild_type, kras_mutated, nras_mutated |
| braf_status | enum | wild_type | wild_type, v600e_mutated |
| detection_method | enum | any | screening_colonoscopy, symptomatic, incidental |
| treatment_phase | enum | active | newly_diagnosed, active_treatment, surveillance, recurrence, metastatic |
| hereditary_syndrome | enum | none | none, lynch_syndrome, fap, map |

## Domain Knowledge

### Anatomic Site Classification

The location of colorectal cancer determines both surgical approach and treatment sequencing.

**Why this matters for generation**: Colon cancer and rectal cancer have fundamentally different management approaches. Colon cancer typically undergoes surgery first. Locally advanced rectal cancer often requires neoadjuvant treatment before surgery.

**Colon Cancer (70% of CRC)**:
```
Right-sided (proximal):
  - Cecum, ascending colon, hepatic flexure, proximal transverse
  - ~40% of colon cancers
  - More often MSI-high
  - More often BRAF-mutated
  - Poorer prognosis stage-for-stage
  - Less benefit from anti-EGFR therapy even if RAS wild-type
  - Surgical approach: Right hemicolectomy

Left-sided (distal):
  - Distal transverse, splenic flexure, descending, sigmoid
  - ~60% of colon cancers
  - Usually microsatellite stable (MSS)
  - Better prognosis stage-for-stage
  - Better response to anti-EGFR therapy if RAS wild-type
  - Surgical approach: Left hemicolectomy or sigmoidectomy
```

**Rectal Cancer (30% of CRC)**:
```
Location:
  - Within 15 cm of anal verge
  - Upper rectum (10-15 cm): May be treated like colon
  - Mid rectum (5-10 cm): Neoadjuvant therapy common
  - Low rectum (<5 cm): Sphincter preservation considerations

Key differences from colon:
  - Higher local recurrence risk
  - Neoadjuvant chemoRT for locally advanced (T3-4 or N+)
  - TME (total mesorectal excision) surgery
  - May achieve complete clinical response (watch-and-wait option)
  - Pelvic radiation considerations
```

### Staging System

AJCC 8th Edition TNM staging for colorectal cancer.

**T Staging (Depth of Invasion)**:
| Stage | Description | Notes |
|-------|-------------|-------|
| Tis | In situ, intramucosal | Carcinoma in situ |
| T1 | Invades submucosa | May be polypectomy candidate |
| T2 | Invades muscularis propria | Requires segmental resection |
| T3 | Invades pericolorectal tissues | Most common T stage at diagnosis |
| T4a | Penetrates visceral peritoneum | Serosal involvement |
| T4b | Invades adjacent organs/structures | Direct extension |

**N Staging (Lymph Node Involvement)**:
| Stage | Description | Notes |
|-------|-------------|-------|
| N0 | No regional node metastasis | Minimum 12 nodes examined |
| N1a | 1 positive node | Stage III |
| N1b | 2-3 positive nodes | Stage III |
| N1c | Tumor deposits without nodes | Satellite nodules |
| N2a | 4-6 positive nodes | Higher risk |
| N2b | 7+ positive nodes | Highest node burden |

**M Staging (Distant Metastases)**:
| Stage | Description | Clinical Implications |
|-------|-------------|----------------------|
| M0 | No distant metastasis | Potentially curable |
| M1a | Single organ, no peritoneal | Liver-only may be resectable |
| M1b | Two+ organs, no peritoneal | Usually palliative |
| M1c | Peritoneal metastasis | Poorest prognosis |

**Stage Grouping**:
```
Stage 0:    Tis N0 M0           (carcinoma in situ)
Stage I:    T1-2 N0 M0          (localized, excellent prognosis)
Stage IIA:  T3 N0 M0            (through wall, no nodes)
Stage IIB:  T4a N0 M0           (serosal penetration)
Stage IIC:  T4b N0 M0           (adjacent organ invasion)
Stage IIIA: T1-2 N1 M0, T1 N2a  (node positive, limited T)
Stage IIIB: T3-4a N1 M0, T2-3 N2a, T1-2 N2b (node positive, moderate T)
Stage IIIC: T4a N2a M0, T3-4a N2b, T4b N1-2 (node positive, advanced T)
Stage IVA:  Any T, Any N, M1a   (single site metastasis)
Stage IVB:  Any T, Any N, M1b   (multiple site metastasis)
Stage IVC:  Any T, Any N, M1c   (peritoneal metastasis)
```

### Biomarker Profiles

Biomarker status is critical for treatment selection in colorectal cancer.

**MSI/MMR Status (Testing Required in All CRC)**:
```
MSI-High (dMMR) - 15% of CRC:
  Clinical significance:
    - Better prognosis in early stage
    - Does NOT benefit from 5-FU adjuvant alone in Stage II
    - Excellent response to immunotherapy in metastatic
    - Associated with Lynch syndrome (germline) or sporadic (MLH1 methylation)

  Testing methods:
    - IHC for MMR proteins (MLH1, MSH2, MSH6, PMS2)
    - PCR for microsatellite markers
    - NGS panels

  Treatment implications:
    - Stage II MSI-H: Usually NO adjuvant chemotherapy
    - Stage IV MSI-H: Pembrolizumab first-line option

MSS (pMMR) - 85% of CRC:
  - Standard chemotherapy regimens
  - Limited benefit from single-agent immunotherapy
  - Anti-EGFR eligible if RAS wild-type
```

**RAS Mutations (KRAS/NRAS)**:
```
RAS Mutated - 50-55% of CRC:
  Mutations tested:
    - KRAS exon 2 (codons 12, 13) - most common
    - KRAS exon 3 (codon 61)
    - KRAS exon 4 (codons 117, 146)
    - NRAS exon 2, 3, 4

  Clinical significance:
    - CONTRAINDICATION to anti-EGFR therapy
    - No cetuximab or panitumumab
    - Use bevacizumab-based regimens instead

RAS Wild-Type - 45-50% of CRC:
  - Eligible for anti-EGFR therapy
  - Left-sided tumors: Anti-EGFR preferred
  - Right-sided tumors: Less benefit from anti-EGFR, consider bevacizumab
```

**BRAF V600E Mutation**:
```
BRAF V600E Mutated - 8-12% of CRC:
  Clinical significance:
    - Poor prognosis
    - Often right-sided, MSI-H, older females
    - Aggressive disease
    - Rapid progression on chemotherapy

  Treatment implications:
    - More intensive chemotherapy (FOLFOXIRI)
    - BRAF-targeted therapy in later lines (encorafenib + cetuximab)
    - If also MSI-H: Immunotherapy
```

**HER2 Amplification**:
```
HER2 Amplified - 2-3% of CRC:
  - Almost exclusively in RAS/BRAF wild-type
  - Anti-HER2 therapy option (trastuzumab + pertuzumab or lapatinib)
  - Testing indicated in RAS wild-type metastatic disease
```

### Biomarker-Treatment Coherence

Treatment must align with biomarker status.

**Coherence Rules**:
```python
# RAS mutation status
if ras_mutated:
    anti_egfr_eligible = False  # Absolutely contraindicated
    preferred_biologic = "bevacizumab"
else:  # RAS wild-type
    if left_sided:
        preferred_biologic = "cetuximab or panitumumab"
    else:  # Right-sided
        preferred_biologic = "bevacizumab"  # Less anti-EGFR benefit

# MSI/MMR status
if msi_high:
    if stage == "II":
        adjuvant_chemo_benefit = "minimal to none"
    if stage == "IV":
        immunotherapy_eligible = True
        pembrolizumab_first_line = True

# BRAF V600E
if braf_v600e_mutated:
    prognosis = "poor"
    consider_folfoxiri = True
    later_line_braf_targeted = True  # encorafenib + cetuximab
```

## Treatment by Stage

### Stage I (T1-2 N0 M0)

Localized disease with excellent prognosis.

**T1 Cancers (submucosal invasion)**:
```
If favorable features (all criteria met):
  - Well/moderately differentiated
  - No lymphovascular invasion
  - Clear margins (>1mm)
  - No tumor budding
  → Polypectomy/local excision may be adequate

If unfavorable features:
  → Segmental resection recommended
```

**T2 Cancers**:
```
Standard treatment:
  - Segmental resection with lymphadenectomy
  - Minimum 12 lymph nodes examined
  - No adjuvant chemotherapy needed
  - 5-year survival: >90%
```

### Stage II (T3-4 N0 M0)

Through bowel wall without lymph node involvement.

**Risk Stratification**:
```
Low-risk Stage II:
  - T3, no adverse features
  - MSI-H (actually favorable)
  → Observation (no adjuvant chemotherapy)

High-risk Stage II (any of):
  - T4 tumor
  - Fewer than 12 lymph nodes examined
  - Poorly differentiated histology
  - Lymphovascular invasion
  - Perineural invasion
  - Tumor perforation or obstruction
  - Close/indeterminate margins
  → Consider adjuvant chemotherapy (FOLFOX or CAPOX, 3-6 months)

MSI-H Stage II:
  - Good prognosis
  - Does NOT benefit from 5-FU alone
  - If other high-risk features, consider observation vs short-course oxaliplatin
```

### Stage III (Any T, N1-2, M0)

Node-positive disease requiring adjuvant chemotherapy.

**Standard Treatment (Colon)**:
```
Surgery first:
  - Segmental resection
  - Lymphadenectomy (minimum 12 nodes)

Adjuvant chemotherapy:
  - Start within 8 weeks of surgery
  - FOLFOX or CAPOX
  - Duration based on risk:
    Low-risk (T1-3, N1): 3 months CAPOX or 3-6 months FOLFOX
    High-risk (T4 or N2): 6 months FOLFOX or CAPOX
```

**Rectal Cancer Stage II-III**:
```
Total Neoadjuvant Therapy (TNT) - Preferred:
  - FOLFOX x 4 cycles (induction)
  - Followed by chemoradiation (5-FU or capecitabine + RT)
  - TME surgery
  - Complete response: Consider watch-and-wait

Traditional approach:
  - Neoadjuvant chemoRT (long-course: 5-FU/cape + 50.4 Gy)
  - TME surgery
  - Adjuvant chemotherapy (FOLFOX x 4 months)

Short-course RT option:
  - 25 Gy in 5 fractions
  - Followed by chemotherapy
  - Surgery
```

### Stage IV (Metastatic)

Systemic disease with varying treatment goals.

**Liver-Limited Metastatic Disease (Potentially Curable)**:
```
Resectable at diagnosis:
  - Hepatic resection (staged or simultaneous with primary)
  - Perioperative chemotherapy (FOLFOX or CAPOX)
  - 5-year survival: 25-40%

Initially unresectable, potentially convertible:
  - Conversion chemotherapy (intensive regimen)
  - FOLFOX/FOLFIRI + bevacizumab or anti-EGFR (if RAS WT)
  - Reassess resectability every 2 months
  - Goal: Downstage to resection
```

**Unresectable/Palliative Metastatic Disease**:
```
First-line options:

MSI-High (15%):
  - Pembrolizumab monotherapy (preferred)
  - OR chemotherapy doublet + biologic

MSS/RAS Mutated:
  - FOLFOX or FOLFIRI + bevacizumab
  - Consider FOLFOXIRI + bevacizumab if BRAF mutated

MSS/RAS Wild-Type/Left-Sided:
  - FOLFOX or FOLFIRI + cetuximab or panitumumab
  - Anti-EGFR preferred for left-sided

MSS/RAS Wild-Type/Right-Sided:
  - FOLFOX or FOLFIRI + bevacizumab (preferred)
  - Less benefit from anti-EGFR

Second-line and beyond:
  - Switch chemotherapy backbone (FOLFOX ↔ FOLFIRI)
  - May continue bevacizumab beyond progression
  - Regorafenib or TAS-102 for refractory
  - Fruquintinib for refractory
```

## Chemotherapy Regimens

### Backbone Regimens

**FOLFOX (mFOLFOX6)**:
```
Drugs:
  - Oxaliplatin 85 mg/m² IV Day 1
  - Leucovorin 400 mg/m² IV Day 1
  - 5-FU 400 mg/m² IV bolus Day 1
  - 5-FU 2400 mg/m² IV over 46 hours

Schedule: Every 14 days
Cycles: 12 cycles adjuvant (6 months) or 6 cycles (3 months for low-risk)
Setting: Outpatient infusion center + home pump

Key toxicities:
  - Peripheral neuropathy (oxaliplatin) - cumulative, dose-limiting
  - Cold sensitivity (acute oxaliplatin)
  - Diarrhea
  - Myelosuppression

Monitoring:
  - CBC before each cycle
  - Neuropathy assessment each visit
  - Consider stopping oxaliplatin at significant neuropathy
```

**CAPOX (XELOX)**:
```
Drugs:
  - Oxaliplatin 130 mg/m² IV Day 1
  - Capecitabine 1000 mg/m² PO BID Days 1-14

Schedule: Every 21 days
Cycles: 8 cycles adjuvant (6 months) or 4 cycles (3 months for low-risk)
Setting: Outpatient (single infusion day, oral at home)

Advantages:
  - No infusion pump needed
  - Fewer clinic visits

Key toxicities:
  - Hand-foot syndrome (capecitabine)
  - Diarrhea
  - Peripheral neuropathy
```

**FOLFIRI**:
```
Drugs:
  - Irinotecan 180 mg/m² IV Day 1
  - Leucovorin 400 mg/m² IV Day 1
  - 5-FU 400 mg/m² IV bolus Day 1
  - 5-FU 2400 mg/m² IV over 46 hours

Schedule: Every 14 days
Cycles: Continues until progression or toxicity
Setting: Outpatient infusion center + home pump

Key toxicities:
  - Diarrhea (early cholinergic and late)
  - Alopecia
  - Myelosuppression
  - No cumulative neuropathy (advantage over FOLFOX)
```

**FOLFOXIRI**:
```
Drugs:
  - Oxaliplatin 85 mg/m² IV Day 1
  - Irinotecan 165 mg/m² IV Day 1
  - Leucovorin 200 mg/m² IV Day 1
  - 5-FU 3200 mg/m² IV over 48 hours

Schedule: Every 14 days
Cycles: 12 cycles max, then maintenance
Setting: Outpatient infusion center + home pump

Indication:
  - Fit patients with BRAF mutation
  - Liver-limited disease seeking conversion

Key toxicities:
  - Higher toxicity than doublets
  - Diarrhea, neuropathy, myelosuppression
  - Requires good PS (ECOG 0-1)
```

### Biologic Agents

**Bevacizumab (Avastin)**:
```
Dose: 5 mg/kg IV every 2 weeks (with FOLFOX/FOLFIRI)
      7.5 mg/kg IV every 3 weeks (with CAPOX)

Mechanism: Anti-VEGF monoclonal antibody

Indications:
  - Metastatic CRC (any RAS status)
  - Can continue beyond progression

Key toxicities:
  - Hypertension
  - Proteinuria
  - Bleeding risk
  - Wound healing impairment (hold 4-6 weeks perioperatively)
  - Bowel perforation risk (especially with intact primary)
  - Arterial thromboembolism
```

**Cetuximab (Erbitux)**:
```
Dose: 400 mg/m² loading, then 250 mg/m² weekly
      OR 500 mg/m² every 2 weeks

Mechanism: Anti-EGFR monoclonal antibody

Indications:
  - RAS wild-type metastatic CRC only
  - Left-sided preferred
  - Later line: BRAF V600E with encorafenib

Contraindication:
  - RAS mutated (KRAS or NRAS) - NO BENEFIT, possible harm

Key toxicities:
  - Acneiform rash (correlates with efficacy)
  - Hypomagnesemia
  - Infusion reactions
  - Diarrhea
```

**Panitumumab (Vectibix)**:
```
Dose: 6 mg/kg IV every 2 weeks

Mechanism: Anti-EGFR monoclonal antibody (fully human)

Indications:
  - Same as cetuximab (RAS wild-type only)
  - Lower infusion reaction risk (fully human)

Contraindication:
  - RAS mutated

Key toxicities:
  - Similar to cetuximab
  - Less infusion reaction (no chimeric component)
```

**Pembrolizumab (Keytruda)**:
```
Dose: 200 mg IV every 3 weeks OR 400 mg IV every 6 weeks

Mechanism: Anti-PD-1 checkpoint inhibitor

Indications:
  - MSI-H/dMMR metastatic CRC
  - First-line monotherapy option
  - Durable responses in selected patients

Contraindication:
  - MSS tumors (minimal benefit)

Key toxicities:
  - Immune-related adverse events (colitis, hepatitis, pneumonitis, etc.)
  - Thyroid dysfunction
  - Fatigue
```

## Radiation Therapy

Radiation is primarily used for rectal cancer, not colon cancer.

**Rectal Cancer Indications**:
```
Neoadjuvant (preoperative):
  - Clinical Stage T3-4 or N+
  - Goal: Downstage tumor, reduce local recurrence
  - May achieve complete response

Adjuvant (postoperative):
  - If no neoadjuvant RT and positive margins or close margins
  - Less preferred than neoadjuvant approach
```

**Long-Course Chemoradiation**:
```
Radiation: 45-50.4 Gy in 25-28 fractions (5 weeks)
Concurrent chemo: 5-FU infusion or capecitabine

Timing: Surgery 6-10 weeks after completion
Advantages: Higher complete response rate
Disadvantages: Longer overall treatment time
```

**Short-Course Radiation**:
```
Radiation: 25 Gy in 5 fractions (1 week)
Timing: Surgery within 1 week OR delayed 6-8 weeks

Advantages: Faster, allows chemotherapy first
Modern use: Often followed by chemotherapy, then surgery
```

## Screening and Surveillance

### Screening (Average Risk)

```
Age to start: 45 years
Preferred method: Colonoscopy every 10 years

Alternatives:
  - FIT (fecal immunochemical test) annually
  - FIT-DNA (Cologuard) every 3 years
  - CT colonography every 5 years
  - Flexible sigmoidoscopy every 5 years (with FIT every 2 years)

Stop screening: Age 75-85 based on health status
```

### High-Risk Screening

**Lynch Syndrome (HNPCC)**:
```
Start: Age 20-25 or 2-5 years before youngest CRC in family
Frequency: Colonoscopy every 1-2 years
Also screen: Endometrial, ovarian, urinary tract, gastric, small bowel
```

**Familial Adenomatous Polyposis (FAP)**:
```
Start: Age 10-12
Frequency: Annual sigmoidoscopy/colonoscopy
Intervention: Prophylactic colectomy when polyps develop
Also screen: Upper GI for duodenal adenomas
```

**Personal History of CRC**:
```
Post-resection surveillance (see below)
```

**Inflammatory Bowel Disease**:
```
Start: 8 years after diagnosis (pancolitis) or 15 years (left-sided)
Frequency: Every 1-2 years with chromoendoscopy
```

### Post-Treatment Surveillance

**After Curative-Intent Treatment (Stages I-III)**:
```
History and Physical:
  - Every 3-6 months for 2 years
  - Then every 6 months for 3 years
  - Then annually

CEA:
  - If elevated preoperatively, check postop baseline
  - Every 3-6 months for 2 years (Stage II-III)
  - Then every 6 months years 3-5

CT Chest/Abdomen/Pelvis:
  - Every 6-12 months for 5 years (Stage II-III)
  - Stage I: Less intensive, based on risk factors

Colonoscopy:
  - 1 year post-resection (or within 6 months if not done preop)
  - If normal, repeat at 3 years
  - If still normal, every 5 years

PET-CT: Not routine surveillance (use for suspected recurrence)
```

## Variations

### screen_detected_early
**Parameters**: Stage I-II, detection via screening colonoscopy

**Clinical Pattern**:
```yaml
presentation:
  detection: average_risk_screening_colonoscopy
  symptoms: none (asymptomatic)
  age_range: 50-75

workup:
  - colonoscopy_with_polypectomy_or_biopsy
  - ct_chest_abdomen_pelvis
  - cea_baseline
  - no_pet_required_early_stage

biomarkers:
  - msi_mmr_status
  - ras_braf_if_stage_ii_high_risk

treatment_stage_i:
  surgery:
    - segmental_resection
    - t1_favorable: polypectomy_may_suffice
  adjuvant: none

treatment_stage_ii:
  surgery: segmental_resection
  adjuvant_decision:
    low_risk: observation
    high_risk: consider_folfox_3_months
    msi_high: usually_observation

surveillance:
  colonoscopy: 1_year_then_3_years
  cea: every_6_months_if_elevated_baseline
  imaging: minimal_stage_i, annual_ct_stage_ii
```

**Example Timeline**:
```
Day 0:     Screening colonoscopy - 2cm ascending colon mass
Day 3:     Biopsy: Moderately differentiated adenocarcinoma
Day 10:    CT C/A/P: No metastases
Day 14:    Surgical consultation
Day 28:    Right hemicolectomy
Day 35:    Path: T3N0 (0/16 nodes), MSI-H, clear margins
Day 42:    CEA baseline: 2.1 (normal)
Day 49:    Oncology: Stage IIA, MSI-H → Observation (no adjuvant)
Month 3:   Surveillance visit, CEA 2.3
Month 12:  Colonoscopy - clear
Year 2-5:  Annual visits, CEA, CT chest/abd/pelvis
```

### adjuvant_stage_iii
**Parameters**: Stage III colon cancer requiring adjuvant chemotherapy

**Clinical Pattern**:
```yaml
presentation:
  detection: symptomatic_or_screening
  symptoms: may_include_blood_per_rectum, change_in_bowel_habits, anemia

workup:
  - colonoscopy_with_biopsy
  - ct_chest_abdomen_pelvis_staging
  - cea_preoperative
  - consider_pet_if_borderline_findings

biomarkers:
  - msi_mmr_status
  - ras_braf_for_future_treatment_planning

treatment:
  surgery_first:
    - segmental_resection
    - lymphadenectomy_minimum_12_nodes

  adjuvant_chemotherapy:
    timing: within_8_weeks_of_surgery
    low_risk_stage_iii: # T1-3 N1
      option_1: capox_3_months
      option_2: folfox_3_6_months
    high_risk_stage_iii: # T4 or N2
      preferred: folfox_6_months
      alternative: capox_6_months

monitoring_during_treatment:
  - cbc_bmp_before_each_cycle
  - neuropathy_assessment
  - dose_modifications_as_needed

surveillance_after_treatment:
  - standard_post_resection_protocol
```

**Example Timeline**:
```
Day 0:     Colonoscopy: Sigmoid mass, biopsy → adenocarcinoma
Day 7:     CT staging: No metastases
Day 10:    CEA: 15.2 (elevated)
Day 21:    Sigmoid colectomy
Day 28:    Path: T3N2a (5/18 nodes positive), MSS, KRAS G12D
Day 35:    Post-op recovery, wound healing
Day 42:    Oncology consult: Stage IIIB → 6 months FOLFOX
Day 56:    FOLFOX Cycle 1 (port placed)
Day 70:    FOLFOX Cycle 2, tolerated well
...continues every 2 weeks...
Day 182:   FOLFOX Cycle 12 completed, Grade 1 neuropathy
Day 196:   Restaging CT: NED
Day 210:   CEA: 3.1 (normalized)
Day 365:   Surveillance colonoscopy: Clear anastomosis
Year 2-5:  Surveillance q6 months with CEA, imaging
```

### locally_advanced_rectal
**Parameters**: Stage II-III rectal cancer with neoadjuvant therapy

**Clinical Pattern**:
```yaml
presentation:
  site: rectum
  stage: cT3_or_cT4_or_node_positive
  symptoms: rectal_bleeding, tenesmus, change_in_stool_caliber

workup:
  - colonoscopy_with_biopsy
  - endorectal_ultrasound_or_pelvic_mri (local staging)
  - ct_chest_abdomen_pelvis
  - cea_baseline
  - biomarker_testing

treatment_total_neoadjuvant_therapy:
  induction_chemotherapy:
    regimen: folfox_4_cycles
    rationale: systemic_control_first

  chemoradiation:
    radiation: 50.4_gy_28_fractions
    concurrent: capecitabine_or_5fu_infusion
    duration: 5_weeks

  restaging:
    timing: 6_8_weeks_post_chemoRT
    modality: pelvic_mri
    assess: tumor_response_clinical_complete_response

  surgery:
    if_residual_disease: tme_low_anterior_resection_or_apr
    if_complete_response: consider_watch_and_wait

watch_and_wait_protocol:
  criteria: clinical_complete_response_on_exam_and_mri
  surveillance: every_3_months_exam_mri_for_2_years
  local_regrowth: salvage_surgery_still_curative
```

**Example Timeline**:
```
Day 0:     Rectal bleeding → Colonoscopy: 5cm rectal mass at 8cm from AV
Day 5:     Biopsy: Moderately differentiated adenocarcinoma
Day 10:    Pelvic MRI: cT3N1, no mesorectal fascia involvement
Day 12:    CT C/A/P: No metastases
Day 14:    CEA: 8.4
Day 21:    Tumor board: Total neoadjuvant therapy (TNT)
Day 28:    FOLFOX Cycle 1 (induction)
Day 42:    FOLFOX Cycle 2
Day 56:    FOLFOX Cycle 3
Day 70:    FOLFOX Cycle 4
Day 84:    Begin chemoradiation (capecitabine + 50.4 Gy)
Day 119:   Complete chemoradiation
Day 168:   Restaging MRI: Near-complete response (ycT1N0)
Day 182:   Low anterior resection (TME)
Day 189:   Path: ypT1N0 (0/14 nodes) - excellent response
Day 203:   Surveillance begins
Year 1-5:  Close surveillance with DRE, CEA, imaging
```

### metastatic_msi_high
**Parameters**: Stage IV with MSI-H/dMMR status

**Clinical Pattern**:
```yaml
presentation:
  stage: iv_metastatic
  msi_status: msi_high_or_dmmr
  common_features:
    - often_right_sided
    - may_have_multiple_primaries
    - evaluate_for_lynch_syndrome

workup:
  - biopsy_confirming_adenocarcinoma
  - msi_mmr_testing (IHC and/or PCR)
  - ct_chest_abdomen_pelvis
  - cea_baseline
  - germline_testing_if_age_under_70
  - lynch_syndrome_evaluation

treatment:
  first_line:
    preferred: pembrolizumab_monotherapy
    rationale: high_response_rate_durable_responses

  alternatives:
    - folfox_or_folfiri_plus_bevacizumab
    - nivolumab_ipilimumab_combination

response_assessment:
  timing: every_8_12_weeks
  expect: may_see_pseudoprogression
  cea: may_lag_behind_imaging_response

durability:
  - complete_responses_possible
  - median_pfs_superior_to_chemo
  - long_term_survival_achievable
```

**Example Timeline**:
```
Day 0:     Right-sided abdominal mass on imaging
Day 3:     Colonoscopy: Cecal mass + hepatic flexure mass (synchronous)
Day 5:     Biopsy: Adenocarcinoma
Day 10:    CT: Multiple liver metastases
Day 12:    MSI/MMR testing: MLH1/PMS2 loss (dMMR)
Day 14:    Extended RAS/BRAF: BRAF V600E
Day 21:    Germline testing sent (Lynch evaluation)
Day 28:    Oncology: MSI-H metastatic CRC → Pembrolizumab
Day 35:    Pembrolizumab Cycle 1
Day 56:    Pembrolizumab Cycle 2
Day 77:    Pembrolizumab Cycle 3
Day 98:    Restaging CT: Partial response (30% reduction)
Day 119:   Pembrolizumab Cycle 4
Day 180:   CT: Near-complete response
Day 365:   CT: Continued response, CEA normal
Ongoing:   Continue pembrolizumab until progression/toxicity
           Germline negative - sporadic MSI-H (MLH1 methylation)
```

### metastatic_ras_wildtype
**Parameters**: Stage IV, RAS wild-type, eligible for anti-EGFR therapy

**Clinical Pattern**:
```yaml
presentation:
  stage: iv_metastatic
  ras_status: wild_type (KRAS and NRAS)
  sidedness: important_for_treatment_selection

workup:
  - biopsy_with_molecular_testing
  - extended_ras_panel (all KRAS and NRAS codons)
  - braf_testing
  - msi_mmr_status
  - her2_if_ras_braf_wildtype
  - ct_chest_abdomen_pelvis

treatment_left_sided:
  first_line:
    preferred: folfox_or_folfiri_plus_cetuximab_or_panitumumab
    rationale: anti_egfr_superior_in_left_sided

treatment_right_sided:
  first_line:
    preferred: folfox_or_folfiri_plus_bevacizumab
    rationale: anti_egfr_less_effective_right_sided
    alternative: may_still_use_anti_egfr_if_indicated

monitoring:
  - response_assessment_every_8_weeks
  - cea_monitoring
  - watch_for_skin_toxicity_with_anti_egfr

second_line:
  - switch_chemotherapy_backbone
  - may_continue_biologic_or_switch
  - anti_egfr_rechallenge_possible_after_interval
```

**Example Timeline (Left-Sided)**:
```
Day 0:     Sigmoid mass with liver metastases on CT
Day 3:     Colonoscopy with biopsy: Adenocarcinoma
Day 7:     CT staging: 3 liver lesions (left lobe)
Day 10:    CEA: 145
Day 14:    Molecular: KRAS/NRAS wild-type, BRAF wild-type, MSS
Day 21:    Oncology: Left-sided, RAS WT → FOLFIRI + Cetuximab
Day 28:    FOLFIRI + Cetuximab Cycle 1
Day 42:    Cycle 2, Grade 2 acneiform rash (good sign)
Day 56:    Cycle 3, rash managed with doxycycline
Day 70:    Cycle 4
Day 84:    Restaging CT: 45% reduction (partial response)
Day 98:    Cycle 5, CEA: 42 (improving)
...continues...
Day 168:   CT: Continued response, liver lesions shrinking
Day 180:   Surgical evaluation: Now resectable
Day 210:   Left hepatectomy + sigmoid resection
Day 224:   Path: Viable tumor, negative margins
Day 238:   Adjuvant FOLFIRI x 4 cycles (no oxaliplatin - neuropathy)
Year 2:    Surveillance, NED
```

### liver_limited_metastatic
**Parameters**: Stage IV with liver-only metastases, potentially curative

**Clinical Pattern**:
```yaml
presentation:
  stage: iv_m1a_liver_only
  resectability: assess_at_diagnosis
  goal: cure_with_multimodality_therapy

evaluation:
  hepatobiliary_surgery_consult:
    assess:
      - number_and_size_of_lesions
      - location_bilobar_vs_unilobar
      - relationship_to_vessels
      - future_liver_remnant
  tumor_board: mandatory_for_treatment_planning

treatment_resectable_at_diagnosis:
  option_1:
    - perioperative_folfox_6_cycles_pre_and_post
    - synchronous_or_staged_resection
  option_2:
    - upfront_surgery
    - adjuvant_chemotherapy

treatment_initially_unresectable:
  conversion_chemotherapy:
    - intensive_regimen_folfox_or_folfiri_plus_biologic
    - reassess_resectability_every_2_months
    - goal: convert_to_resectable
  if_converted:
    - proceed_to_hepatectomy
    - complete_perioperative_chemotherapy

outcomes:
  5_year_survival_resected: 25_40_percent
  cure_possible: yes_in_selected_patients
```

**Example Timeline**:
```
Day 0:     Sigmoid mass + 2 liver lesions on CT
Day 3:     Colonoscopy: Sigmoid adenocarcinoma
Day 7:     Liver MRI: 2 lesions (segments 6 and 7), resectable
Day 10:    CEA: 78
Day 14:    Molecular: KRAS G12C, MSS
Day 21:    Tumor board: Resectable liver-limited → Perioperative approach
Day 28:    FOLFOX + Bevacizumab Cycle 1
Day 42:    Cycle 2
Day 56:    Cycle 3
Day 70:    Restaging CT: Primary and liver lesions stable/improved
Day 84:    Cycle 4
Day 98:    Cycle 5
Day 112:   Cycle 6 (last preoperative)
Day 140:   Hold bevacizumab 6 weeks pre-surgery
Day 154:   Synchronous sigmoid colectomy + right posterior sectionectomy
Day 161:   Path: Both liver lesions R0, sigmoid T3N1
Day 175:   Recovery
Day 189:   Postoperative FOLFOX Cycle 7 (omit bevacizumab post-liver surgery)
...FOLFOX cycles 7-12...
Day 273:   Complete adjuvant therapy
Day 287:   Restaging: NED
Year 1-5:  Intensive surveillance
Year 3:    Remains NED - potentially cured
```

### hereditary_lynch
**Parameters**: Lynch syndrome with colorectal cancer

**Clinical Pattern**:
```yaml
presentation:
  hereditary_syndrome: lynch_syndrome_hnpcc
  tumor_characteristics:
    - typically_right_sided
    - msi_high
    - often_younger_age_at_diagnosis
    - may_have_synchronous_or_metachronous_crc

diagnosis_of_lynch:
  tumor_testing:
    - msi_mmr_by_ihc (loss of MLH1, MSH2, MSH6, or PMS2)
    - if_mlh1_loss: check_braf_and_mlh1_methylation
    - germline_testing_for_mmr_genes

  amsterdam_or_bethesda_criteria: suggestive_family_history

treatment_of_crc:
  surgery:
    consider: extended_colectomy_vs_segmental
    rationale: high_risk_of_metachronous_crc
  adjuvant:
    - msi_h_stage_ii: usually_no_adjuvant
    - msi_h_stage_iii: standard_adjuvant_folfox
  metastatic:
    - pembrolizumab_first_line_preferred

surveillance_lynch_carriers:
  colonoscopy: every_1_2_years_starting_age_20_25
  gynecologic: annual_endometrial_sampling_starting_30_35
  urologic: annual_urinalysis
  gastric: egd_every_2_3_years_if_family_history

family_management:
  - genetic_counseling_for_all_first_degree_relatives
  - cascade_testing
  - prophylactic_surgery_discussions
```

**Example Timeline**:
```
Day 0:     45-year-old with rectal bleeding
Day 3:     Colonoscopy: Ascending colon mass + 2 adenomatous polyps
Day 5:     Biopsy: Adenocarcinoma
Day 10:    CT staging: No metastases
Day 12:    Family history: Mother CRC age 48, aunt endometrial cancer age 52
Day 14:    IHC: Loss of MSH2 and MSH6 → Suspect Lynch
Day 21:    Germline testing: MSH2 pathogenic variant confirmed
Day 28:    Genetic counseling
Day 35:    Subtotal colectomy (extended resection for Lynch)
Day 42:    Path: T3N0 (0/22 nodes), MSI-H - Stage IIA
Day 56:    Oncology: No adjuvant chemotherapy (MSI-H Stage II)
Day 70:    Referrals: Gynecology, urology for Lynch surveillance
Month 6:   First surveillance: Rectal exam (preserved rectum), CEA
Month 12:  Surveillance colonoscopy/sigmoidoscopy of residual rectum
           First-degree relatives begin cascade testing
Ongoing:   Annual colonoscopy of remaining colorectum
           Gynecologic surveillance for wife (affected offspring possible)
           Two siblings test positive → begin their surveillance
```

## Composite Patterns

### CRC with Cardiac Disease

Colorectal cancer in patients with significant cardiac comorbidity.

```yaml
pattern: crc_cardiac_comorbidity
considerations:
  preoperative:
    - cardiac_risk_assessment
    - optimize_heart_failure_or_cad
    - anticoagulation_management

  chemotherapy:
    - 5fu_cardiotoxicity: rare_but_serious_coronary_spasm
    - bevacizumab: hypertension_arterial_events
    - echocardiogram_baseline_if_prior_cardiac_history

  surgery:
    - higher_perioperative_risk
    - may_need_cardiac_clearance
    - bridging_anticoagulation_if_on_anticoagulants

example_cohort:
  age: 72
  cancer: stage_iii_colon
  cardiac: cad_with_stent_on_plavix_and_aspirin
  approach:
    - hold_plavix_5_days_pre_surgery (discuss with cardiology)
    - bridge_if_high_risk_stent
    - postop_resume_anticoagulation
    - adjuvant_folfox_with_cardiac_monitoring
    - avoid_bevacizumab_given_recent_stent
```

### CRC with Diabetes

Colorectal cancer in diabetic patients.

```yaml
pattern: crc_diabetes
considerations:
  perioperative:
    - glucose_management_critical
    - higher_infection_risk
    - slower_wound_healing
    - metformin_hold_pre_contrast_and_surgery

  chemotherapy:
    - steroid_premedication_affects_glucose
    - neuropathy_baseline_assessment (may already have diabetic neuropathy)
    - oxaliplatin_neuropathy_harder_to_assess

  bevacizumab:
    - proteinuria_monitoring_more_important
    - wound_healing_concerns_compounded

example_cohort:
  age: 64
  cancer: stage_iv_colon_liver_mets
  diabetes: type_2_on_metformin_and_glipizide
  approach:
    - hold_metformin_pericontrast
    - tight_glucose_control_during_chemo
    - baseline_monofilament_exam_before_oxaliplatin
    - careful_neuropathy_monitoring
    - endocrine_involvement_for_glucose_optimization
```

### CRC with Inflammatory Bowel Disease

Colorectal cancer arising in IBD patient.

```yaml
pattern: crc_in_ibd
considerations:
  unique_features:
    - different_carcinogenesis_dysplasia_carcinoma_sequence
    - often_subtle_endoscopic_appearance
    - may_be_multifocal
    - higher_risk_mucinous_or_signet_ring

  surgical:
    - may_need_total_proctocolectomy
    - consider_ibd_extent_and_activity
    - pouch_considerations_if_prior_colectomy

  surveillance:
    - history_of_ibd_means_continued_high_risk
    - remaining_bowel_at_risk

example_cohort:
  age: 55
  cancer: stage_ii_colon_arising_in_ulcerative_colitis
  ibd: 20_year_history_of_pancolitis
  approach:
    - total_proctocolectomy_with_ileal_pouch
    - avoid_leaving_at_risk_mucosa
    - msi_mmr_testing (ibd_associated_crc_can_be_either)
    - adjuvant_decision_per_staging
    - pouch_surveillance_post_surgery
```

### CRC with Renal Insufficiency

Colorectal cancer in patients with CKD.

```yaml
pattern: crc_ckd
considerations:
  chemotherapy_adjustments:
    capecitabine:
      - reduce_dose_crcl_30_50
      - avoid_crcl_below_30
    oxaliplatin:
      - no_adjustment_mild_moderate
      - use_with_caution_severe
    irinotecan:
      - no_renal_adjustment
    5fu:
      - generally_no_adjustment

  biologic_considerations:
    bevacizumab:
      - can_worsen_proteinuria
      - monitor_closely
    cetuximab:
      - hypomagnesemia_may_be_harder_to_correct

  contrast_nephropathy:
    - pre_hydration_for_staging_scans
    - consider_alternatives_to_contrast

example_cohort:
  age: 68
  cancer: stage_iii_colon
  renal: ckd_stage_3b_egfr_35
  approach:
    - adjuvant_folfox_with_capecitabine_dose_reduced
    - alternative_5fu_infusion_backbone_if_creatinine_clearance_drops
    - avoid_nsaids_for_pain_management
    - nephrology_co_management
    - hydration_protocol_for_contrast_ct
```

### CRC with Liver Cirrhosis

Colorectal cancer in patients with underlying liver disease.

```yaml
pattern: crc_liver_cirrhosis
considerations:
  liver_metastases:
    - limited_resection_options
    - future_liver_remnant_more_critical
    - portal_hypertension_affects_surgery

  chemotherapy:
    - hepatotoxicity_risk
    - altered_drug_metabolism
    - avoid_irinotecan_if_elevated_bilirubin

  bevacizumab:
    - bleeding_risk_with_varices
    - avoid_in_significant_portal_hypertension

example_cohort:
  age: 62
  cancer: stage_iv_colon_with_single_liver_met
  liver: child_pugh_a_cirrhosis_from_nash
  approach:
    - hepatology_co_management
    - limited_hepatectomy_if_feasible
    - careful_flr_assessment
    - folfox_preferable_to_folfiri
    - avoid_bevacizumab_if_varices_present
    - close_liver_function_monitoring
```

## Clinical Event Sequences

### Screening-Detected Early Stage

```
Screening colonoscopy triggers cascade:

Visit 1 (Day 0) - Gastroenterology:
  - Routine screening colonoscopy (age 50, average risk)
  - Finding: 2.5cm sessile polyp in sigmoid colon
  - Action: Attempted polypectomy, incomplete, tattoo placed
  - Pathology sent

Visit 2 (Day 5) - Gastroenterology call:
  - Path: Invasive adenocarcinoma in polyp
  - Referral to colorectal surgery
  - Staging workup ordered

Visit 3 (Day 10) - Colorectal Surgery:
  - Review pathology: T1 but unfavorable features (LVI+)
  - CT C/A/P: No metastases
  - CEA: 3.2 (normal)
  - Plan: Sigmoid colectomy recommended

Visit 4 (Day 21) - Surgery:
  - Laparoscopic sigmoid colectomy
  - Hospital stay: 3 days
  - Uncomplicated recovery

Visit 5 (Day 35) - Post-op Surgery:
  - Path: pT1N0 (0/15 nodes), margins negative
  - Stage I colon cancer
  - No adjuvant therapy needed
  - Surveillance plan discussed

Visit 6 (Month 12) - Surveillance:
  - Colonoscopy: Clear, no recurrence
  - CEA: 2.8 (stable)
  - Next colonoscopy in 3 years
```

### Stage III Adjuvant Pathway

```
Symptomatic presentation through adjuvant completion:

Visit 1 (Day 0) - Primary Care:
  - Chief complaint: Change in bowel habits, intermittent blood
  - Exam: Guaiac positive
  - Orders: CBC (Hgb 10.2, microcytic), colonoscopy referral

Visit 2 (Day 14) - Gastroenterology:
  - Colonoscopy: Near-obstructing ascending colon mass
  - Biopsy: Invasive adenocarcinoma
  - CT staging ordered

Visit 3 (Day 21) - Colorectal Surgery:
  - CT C/A/P: No metastases
  - CEA: 28
  - Plan: Right hemicolectomy

Visit 4 (Day 28) - Surgery:
  - Open right hemicolectomy (size precluded lap)
  - Hospital stay: 5 days

Visit 5 (Day 42) - Surgical Follow-up:
  - Path: pT3N2a (5/18 nodes), MSS, KRAS G12D
  - Stage IIIB
  - Medical oncology referral

Visit 6 (Day 56) - Medical Oncology:
  - Stage IIIB colon cancer discussion
  - Plan: FOLFOX x 12 cycles (6 months)
  - Port placement scheduled

Visit 7 (Day 63) - Port placement
Visit 8 (Day 70) - FOLFOX Cycle 1
Visit 9 (Day 84) - FOLFOX Cycle 2
...cycles continue every 2 weeks...

Visit 20 (Day 196) - FOLFOX Cycle 12:
  - Grade 1 neuropathy (tolerable)
  - No dose reductions needed
  - Complete adjuvant therapy

Visit 21 (Day 210) - End of Treatment:
  - CEA: 3.1 (normalized)
  - Surveillance plan initiated
  - Next CT in 3 months
```

### Metastatic with Liver Resection

```
Liver-limited metastatic to potential cure:

Visit 1 (Day 0) - Emergency Department:
  - Abdominal pain, partial obstruction
  - CT: Sigmoid mass with 2 liver lesions
  - Admitted for decompression

Visit 2 (Day 3) - Inpatient:
  - Stent placed for obstruction
  - Biopsy: Adenocarcinoma
  - CEA: 156
  - Hepatobiliary surgery consulted

Visit 3 (Day 10) - Multidisciplinary Tumor Board:
  - Liver MRI: 2 lesions in right lobe, potentially resectable
  - Molecular: RAS wild-type, BRAF wild-type, MSS
  - Plan: Neoadjuvant chemotherapy → resection assessment

Visit 4 (Day 21) - Medical Oncology:
  - Initiate FOLFIRI + Cetuximab (left-sided, RAS WT)
  - Goal: Conversion to resection

Visit 5-10 - Chemotherapy Cycles 1-6:
  - Every 2 weeks
  - Partial response at cycle 4
  - CEA decreasing (156 → 45)

Visit 11 (Day 98) - Restaging:
  - CT/MRI: Primary reduced, liver lesions 40% smaller
  - Surgical re-evaluation: Now resectable
  - Plan: Proceed to surgery

Visit 12 (Day 126) - Surgery:
  - Sigmoid colectomy + right hepatectomy (staged)
  - Actually: Synchronous resection feasible
  - Hospital stay: 7 days

Visit 13 (Day 147) - Surgical Path:
  - Sigmoid: ypT3N1 (2/12 nodes)
  - Liver: Both lesions R0, partial response histology
  - Plan: Adjuvant FOLFIRI x 6 cycles

Visit 14-19 - Adjuvant Cycles:
  - FOLFIRI (no cetuximab post-hepatectomy)
  - Completes 6 cycles

Visit 20 (Day 273) - Surveillance:
  - CT: NED
  - CEA: 4.2 (normalized)
  - Close surveillance initiated

Year 2: Remains NED - potentially cured
```

## Examples

### Example 1: Screen-Detected Stage I

```yaml
patient:
  age: 58
  gender: male
  detection: average_risk_screening_colonoscopy

diagnosis:
  site: sigmoid_colon
  histology: adenocarcinoma_moderately_differentiated
  staging:
    clinical: cT1N0M0
    pathologic: pT1N0 (0/14 nodes)
    stage: I
  biomarkers:
    msi: MSS
    note: "RAS/BRAF not routinely tested for Stage I"

treatment:
  surgery:
    procedure: laparoscopic_sigmoid_colectomy
    date: 2025-02-15
    nodes_examined: 14
    margins: negative
  adjuvant: none

surveillance_plan:
  colonoscopy:
    - year_1: 2026-02
    - then: every_3_years_if_clear
  cea: not_indicated_stage_I_unless_elevated_preop
  imaging: minimal

cea_values:
  - date: 2025-02-01
    value: 2.1
    unit: ng/mL
    status: normal

icd10_codes:
  primary:
    - code: C18.7
      description: "Malignant neoplasm of sigmoid colon"
  encounter:
    - code: Z08
      description: "Encounter for follow-up examination after completed treatment for malignant neoplasm"

prognosis:
  five_year_survival: ">90%"
  recurrence_risk: "<5%"
```

### Example 2: Stage III Rectal with TNT

```yaml
patient:
  age: 54
  gender: female
  detection: symptomatic (rectal bleeding, tenesmus)

diagnosis:
  site: rectum
  location: mid_rectum_7cm_from_anal_verge
  histology: adenocarcinoma_moderately_differentiated
  staging:
    clinical: cT3N1M0
    pathologic: ypT1N0 (0/18 nodes) - excellent response
    stage: clinical_IIIB, pathologic_I
  biomarkers:
    msi: MSS
    kras: wild_type
    nras: wild_type
    braf: wild_type

treatment:
  total_neoadjuvant_therapy:
    induction:
      regimen: FOLFOX
      cycles: 4
      dates: 2025-01-15 to 2025-03-05
    chemoradiation:
      dose: 50.4 Gy in 28 fractions
      concurrent: capecitabine
      dates: 2025-03-15 to 2025-04-25
    restaging:
      date: 2025-06-01
      finding: near_complete_clinical_response
  surgery:
    procedure: low_anterior_resection_with_tme
    date: 2025-06-15
    pathologic_response: major_response_residual_microscopic

surveillance_plan:
  physical_exam: every_3_months_year_1-2
  cea: every_3_months_year_1-2
  ct_cap: every_6_months_year_1-2
  colonoscopy: year_1

cea_values:
  - date: 2025-01-10
    value: 12.4
    status: elevated
  - date: 2025-06-01
    value: 2.8
    status: normalized
  - date: 2025-09-01
    value: 2.2
    status: normal

icd10_codes:
  primary:
    - code: C20
      description: "Malignant neoplasm of rectum"
  treatment:
    - code: Z51.11
      description: "Encounter for antineoplastic chemotherapy"
    - code: Z51.0
      description: "Encounter for antineoplastic radiation therapy"
  history:
    - code: Z85.048
      description: "Personal history of malignant neoplasm of rectum"

outcome:
  pathologic_complete_response: no_but_major_response
  function: good_sphincter_preservation
  prognosis: excellent_given_downstaging
```

### Example 3: MSI-H Metastatic on Immunotherapy

```yaml
patient:
  age: 67
  gender: male
  detection: symptomatic (abdominal_pain, weight_loss)

diagnosis:
  site: ascending_colon (right-sided)
  histology: adenocarcinoma_poorly_differentiated
  staging:
    clinical: cT4aN2bM1a (liver metastases)
    stage: IVA
  biomarkers:
    msi: MSI-High
    mmr_ihc: loss_of_MLH1_and_PMS2
    mlh1_methylation: positive (sporadic, not Lynch)
    braf: V600E
    kras: wild_type
    nras: wild_type

treatment:
  first_line:
    regimen: pembrolizumab_monotherapy
    dose: 200mg_IV_q3weeks
    start_date: 2025-02-01
    response_assessment:
      week_9: stable_disease
      week_18: partial_response
      week_36: near_complete_response
  surgery: deferred_excellent_response_on_immunotherapy

response:
  cea_trend:
    - date: 2025-01-25
      value: 234
    - date: 2025-04-01
      value: 89
    - date: 2025-07-01
      value: 12
    - date: 2025-10-01
      value: 4.2
  imaging_response:
    best_response: 80%_reduction
    liver_mets: near_resolution

adverse_events:
  - event: hypothyroidism
    grade: 2
    onset: cycle_8
    management: levothyroxine_started
  - event: fatigue
    grade: 1
    management: supportive

icd10_codes:
  primary:
    - code: C18.2
      description: "Malignant neoplasm of ascending colon"
  secondary:
    - code: C78.7
      description: "Secondary malignant neoplasm of liver"
  treatment:
    - code: Z51.12
      description: "Encounter for antineoplastic immunotherapy"

lynch_evaluation:
  mlh1_methylation: positive
  braf_v600e: positive
  interpretation: sporadic_msi_h (not Lynch syndrome)
  germline_testing: not_indicated

ongoing_plan:
  continue: pembrolizumab_until_progression_or_toxicity
  monitoring: ct_q12_weeks, tsh_q6_weeks
  surgical_resection: may_consider_if_durable_response
```

### Example 4: Liver-Limited Metastatic with Conversion

```yaml
patient:
  age: 61
  gender: female
  detection: symptomatic (fatigue, right_upper_quadrant_pain)

diagnosis:
  site: sigmoid_colon (left-sided)
  histology: adenocarcinoma_moderately_differentiated
  staging:
    initial: cT3N1M1a (4 liver metastases, bilobar)
    post_treatment: ypT2N0M0 (R0 resection)
    stage: initially IVA, surgically NED
  biomarkers:
    msi: MSS
    kras: wild_type
    nras: wild_type
    braf: wild_type
    her2: not_amplified

treatment:
  conversion_chemotherapy:
    regimen: FOLFIRI_cetuximab
    rationale: left_sided_ras_wildtype
    cycles: 8
    dates: 2025-01-15 to 2025-04-30
    response: 55%_reduction_liver_converted_to_resectable

  surgical:
    procedure: sigmoid_colectomy_plus_staged_hepatectomy
    surgery_1:
      date: 2025-05-20
      procedure: sigmoid_colectomy_plus_right_portal_vein_embolization
    surgery_2:
      date: 2025-06-15
      procedure: right_hepatectomy_plus_segment_3_metastasectomy
    pathology:
      colon: ypT2N0 (0/14 nodes)
      liver: 4_lesions_r0, partial_pathologic_response

  adjuvant:
    regimen: FOLFIRI (no cetuximab post-hepatectomy)
    cycles: 4
    dates: 2025-08-01 to 2025-09-30

cea_values:
  - date: 2025-01-10
    value: 187
  - date: 2025-04-25
    value: 28
  - date: 2025-07-01
    value: 8.2
  - date: 2025-10-15
    value: 3.4

icd10_codes:
  primary:
    - code: C18.7
      description: "Malignant neoplasm of sigmoid colon"
  secondary:
    - code: C78.7
      description: "Secondary malignant neoplasm of liver"
  procedure:
    - code: "0DBN0ZZ"
      description: "Excision of sigmoid colon, open"
    - code: "0FB10ZZ"
      description: "Excision of liver, right lobe, open"
  history:
    - code: Z85.048
      description: "Personal history of malignant neoplasm of rectum, sigmoid colon"
    - code: Z86.001
      description: "Personal history of malignant neoplasm of liver (secondary)"

outcome:
  status: no_evidence_of_disease
  potentially_cured: yes
  five_year_survival_estimate: 30-40%

surveillance_plan:
  cea: every_3_months_x_2_years
  ct_cap: every_3_months_x_2_years, then_q6_months
  colonoscopy: year_1, then_per_guidelines
```

### Example 5: Lynch Syndrome

```yaml
patient:
  age: 42
  gender: female
  detection: symptomatic_with_family_history

family_history:
  mother: colon_cancer_age_45
  maternal_aunt: endometrial_cancer_age_50
  maternal_grandfather: colon_cancer_age_52
  pattern: suggestive_of_lynch_syndrome

diagnosis:
  site: cecum (right-sided)
  histology: adenocarcinoma_with_medullary_features
  staging:
    clinical: cT3N1M0
    pathologic: pT3N1a (2/24 nodes)
    stage: IIIB
  biomarkers:
    msi: MSI-High
    mmr_ihc: loss_of_MSH2_and_MSH6
    germline: MSH2_pathogenic_variant_confirmed

treatment:
  surgery:
    procedure: subtotal_colectomy_with_ileorectal_anastomosis
    rationale: extended_resection_for_lynch_high_metachronous_risk
    date: 2025-02-10
    outcome: uncomplicated

  adjuvant:
    regimen: FOLFOX
    cycles: 8 (3 months due to MSI-H)
    dates: 2025-03-15 to 2025-05-30
    rationale: stage_iii_still_benefits_despite_msi_h

genetic_counseling:
  proband: msh2_positive
  cascade_testing:
    sister_age_40: positive_surveillance_initiated
    sister_age_38: negative_average_risk
    brother_age_45: positive_colonoscopy_clear
    daughter_age_18: defer_until_age_25

lynch_surveillance_proband:
  remaining_colorectum:
    - annual_sigmoidoscopy (rectal_remnant)
  gynecologic:
    - annual_endometrial_biopsy
    - consider_risk_reducing_hysterectomy_bso
  urologic:
    - annual_urinalysis
  upper_gi:
    - egd_every_2_years

icd10_codes:
  primary:
    - code: C18.0
      description: "Malignant neoplasm of cecum"
  genetic:
    - code: Z15.09
      description: "Genetic susceptibility to other malignant neoplasm (Lynch)"
  surveillance:
    - code: Z80.0
      description: "Family history of malignant neoplasm of digestive organs"

family_implications:
  first_degree_relatives: 50%_risk_lynch
  recommendation: genetic_counseling_and_testing_all_first_degree
  children: testing_available_at_adulthood
```

## Validation Rules

| Rule | Requirement | Example |
|------|-------------|---------|
| Stage | 0, I, II, III, IV | Stage IIIB |
| Location | colon, rectum, specific site | "sigmoid colon" |
| KRAS status | mutated, wild-type | "wild-type" |
| NRAS status | mutated, wild-type | "wild-type" |
| BRAF status | mutated (V600E), wild-type | "wild-type" |
| MSI status | MSI-H, MSS | "MSS" |
| CEA | ng/mL | 8.5 ng/mL |
| Node status | pN0, pN1, pN2 | pN1 (1-3 nodes) |

### Business Rules

- **Screening**: Colonoscopy q10y starting age 45 (average risk)
- **RAS Testing**: KRAS/NRAS wild-type required for anti-EGFR therapy
- **MSI Testing**: MSI-H/dMMR patients eligible for immunotherapy
- **Stage I**: Surgery alone usually curative
- **Stage II**: Surgery +/- adjuvant chemo based on risk factors
- **Stage III**: Surgery + adjuvant FOLFOX (3-6 months)
- **Stage IV**: Systemic therapy; consider metastasectomy if limited mets
- **CEA Monitoring**: Baseline and surveillance marker

## Related Skills

### PatientSim Cohorts

- [../SKILL.md](../SKILL.md) - PatientSim overview
- [breast-cancer.md](breast-cancer.md) - Similar oncology cohort structure
- [lung-cancer.md](lung-cancer.md) - Similar oncology cohort structure

### Cross-Product: MemberSim

- [../../membersim/professional-claims.md](../../membersim/professional-claims.md) - Oncology office visit, colonoscopy billing
- [../../membersim/facility-claims.md](../../membersim/facility-claims.md) - Chemotherapy infusion, surgery, radiation claims
- [../../membersim/prior-authorization.md](../../membersim/prior-authorization.md) - Oncology drug authorization

### Cross-Product: RxMemberSim

- [../../rxmembersim/specialty-pharmacy.md](../../rxmembersim/specialty-pharmacy.md) - Oncology drugs (FOLFOX agents, anti-EGFR therapy)
- [../../rxmembersim/rx-prior-auth.md](../../rxmembersim/rx-prior-auth.md) - Specialty drug authorization

### Reference Files

- [../../../references/data-models.md](../../../references/data-models.md) - Entity schemas
- [../../../references/code-systems.md](../../../references/code-systems.md) - ICD-10, CPT, HCPCS codes
