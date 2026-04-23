# Oncology Domain Knowledge

_Foundational oncology knowledge for generating realistic cancer patient data across the disease spectrum._

## Metadata

- **Type**: Domain Knowledge
- **Domain**: Oncology
- **Version**: 1.0
- **Author**: Claude (AI-generated, requires clinical validation)
- **Tags**: oncology, cancer, chemotherapy, radiation, immunotherapy, staging
- **Dependencies**: None (foundational skill)

## For Claude

Use this skill as your core oncology knowledge base when generating any cancer patient data. This teaches you:

- How cancers are classified and staged
- Which treatment modalities apply to which cancer types and stages
- What laboratory and biomarker patterns accompany specific malignancies
- How to ensure clinical coherence between diagnosis, staging, treatment, and outcomes
- How treatment toxicities present and are managed
- How performance status guides treatment decisions

You should apply this knowledge to **every oncology patient you generate** to ensure:
- Cancer diagnoses include appropriate staging information
- Treatment regimens match cancer type, stage, and patient performance status
- Laboratory values reflect disease burden and treatment effects
- Toxicity patterns are realistic for the treatments administered
- Temporal progression follows realistic oncology timelines

This is a **domain knowledge skill** that provides foundational concepts. Cancer-specific scenario skills (breast cancer, lung cancer, etc.) will build upon this foundation.

## Purpose

This skill provides essential oncology knowledge that enables realistic cancer patient data generation. It serves as the foundation for understanding:

- How cancers are classified, staged, and coded
- Which treatments are appropriate for different cancer types and stages
- What laboratory and imaging patterns accompany malignancies
- How treatment toxicities present and require supportive care
- How oncology care is delivered across different settings

**Cross-Product Relevance:**
- **PatientSim**: Clinical encounters, treatment timelines, laboratory progressions, adverse events
- **MemberSim**: Oncology claims patterns, prior authorizations for cancer drugs, episode-of-care groupings
- **RxMemberSim**: Specialty pharmacy for oral oncolytics, supportive care medications (antiemetics, growth factors)

Use this skill when generating oncology patients to ensure clinical coherence across all elements. This is a foundational skill that cancer-specific scenario skills will reference.

## When to Use This Skill

Apply this skill **proactively** for all oncology-related patient generation. Specific triggers:

**Direct Keywords**:
- Any cancer type: "breast cancer", "lung cancer", "colon cancer", "lymphoma", "leukemia"
- Oncology terms: "malignancy", "tumor", "metastatic", "carcinoma", "sarcoma"
- Treatment terms: "chemotherapy", "radiation", "immunotherapy", "targeted therapy"
- Staging terms: "Stage IV", "TNM staging", "metastasis"
- Oncology settings: "infusion center", "oncology clinic", "tumor board"

**Clinical Scenarios**:
- "Generate a cancer patient"
- "Create a patient receiving chemotherapy"
- "I need a metastatic breast cancer patient"
- "Generate a patient with treatment-related neutropenia"
- "Make a patient transitioning to hospice care"

**Implicit Indicators**:
- Any request for patients with malignant neoplasms
- Requests mentioning tumor markers (CEA, CA-125, PSA)
- Requests for specialty pharmacy scenarios involving oncology drugs
- When coherence between staging, treatment, and prognosis is needed

**Co-occurring Mentions**:
- Often paired with: specialty pharmacy skills, prior authorization workflows
- Frequently includes: performance status, treatment intent, response assessment
- May mention: clinical trials, tumor boards, multidisciplinary care

## Domain Knowledge

### Cancer Classification

#### Solid Tumors vs Hematologic Malignancies

Cancers are fundamentally classified into two major categories:

**Solid Tumors**:
- Arise from epithelial, mesenchymal, or neural tissues
- Form discrete masses that can be imaged and measured
- Staged primarily by TNM system
- Examples: breast, lung, colon, prostate, pancreatic cancers

**Hematologic Malignancies**:
- Arise from blood-forming tissues (bone marrow, lymphoid tissue)
- Often disseminated at diagnosis
- Staged by disease-specific systems (Ann Arbor, Rai, Binet)
- Examples: leukemias, lymphomas, multiple myeloma

**Why this matters for generation**: Don't apply TNM staging to lymphomas (use Ann Arbor). Don't describe a "tumor mass" for leukemia (it's in the blood/marrow).

#### Primary Site and Histology

Every cancer has:
- **Primary Site**: Where the cancer originated (breast, lung, colon)
- **Histology**: The cell type (adenocarcinoma, squamous cell, small cell)
- **Behavior**: Malignant (invasive), in-situ (pre-invasive), benign

**Common Histologic Types by Site**:
```
Lung:
  - Non-small cell (85%):
    - Adenocarcinoma (40%)
    - Squamous cell (25-30%)
    - Large cell (10-15%)
  - Small cell (15%)

Breast:
  - Invasive ductal carcinoma (70-80%)
  - Invasive lobular carcinoma (10-15%)
  - Ductal carcinoma in-situ (DCIS) - pre-invasive

Colon:
  - Adenocarcinoma (95%+)
  - Neuroendocrine tumors (rare)

Prostate:
  - Adenocarcinoma (95%+)
  - Gleason grading (3+3 to 5+5)
```

#### ICD-10 Oncology Coding Structure

**Primary Malignancy Codes (C00-C96)**:
```
C00-C14: Lip, oral cavity, pharynx
C15-C26: Digestive organs
C30-C39: Respiratory and intrathoracic
C40-C41: Bone and articular cartilage
C43-C44: Skin
C45-C49: Mesothelial and soft tissue
C50: Breast
C51-C58: Female genital organs
C60-C63: Male genital organs
C64-C68: Urinary tract
C69-C72: Eye, brain, CNS
C73-C75: Thyroid and other endocrine
C76-C80: Ill-defined, secondary, unspecified
C81-C96: Lymphoid, hematopoietic (lymphomas, leukemias)
```

**Secondary (Metastatic) Codes (C77-C79)**:
```
C77.x: Secondary to lymph nodes
C78.0x: Secondary to lung
C78.7: Secondary to liver
C79.31: Secondary to brain
C79.51: Secondary to bone
```

**Why this matters for generation**: A patient with metastatic breast cancer to bone should have BOTH C50.x (primary breast) AND C79.51 (secondary to bone).

### Staging Systems

#### TNM Staging (AJCC 8th Edition)

The TNM system applies to most solid tumors and describes anatomic extent of disease.

**T - Primary Tumor**:
```
Tx: Primary tumor cannot be assessed
T0: No evidence of primary tumor
Tis: Carcinoma in situ (pre-invasive)
T1: Small, localized tumor (size varies by cancer type)
T2: Larger tumor or minimal local extension
T3: Large tumor or more local extension
T4: Tumor invading adjacent structures
```

**N - Regional Lymph Nodes**:
```
Nx: Regional nodes cannot be assessed
N0: No regional node metastasis
N1: Limited regional node involvement (1-3 nodes typically)
N2: Moderate regional node involvement (4-9 nodes typically)
N3: Extensive regional node involvement (10+ nodes typically)
```

**M - Distant Metastasis**:
```
M0: No distant metastasis
M1: Distant metastasis present
  - M1a, M1b, M1c: Site-specific substaging for some cancers
```

**Stage Groupings**:
```
Stage 0: Tis, N0, M0 (carcinoma in situ)
Stage I: Small tumor, no nodes, no mets (T1-T2, N0, M0)
Stage II: Larger tumor OR limited node involvement (varies)
Stage III: Locally advanced, extensive nodes (T3-T4 and/or N2-N3, M0)
Stage IV: Any T, any N, M1 (distant metastasis present)
```

**Substages (A, B, C)**:
- Most stages have substages based on specific TNM combinations
- Stage IIIA vs IIIB vs IIIC have different prognosis and treatment implications
- Always check cancer-specific staging criteria

**Why this matters for generation**: Stage determines treatment intent (curative vs palliative). Stage I-II are often curable with surgery. Stage IV is typically incurable (with exceptions like testicular cancer, some lymphomas).

#### Ann Arbor Staging for Lymphomas

Used for Hodgkin and Non-Hodgkin lymphomas:

```
Stage I: Single lymph node region OR single extralymphatic site
Stage II: Two or more node regions on SAME side of diaphragm
Stage III: Node regions on BOTH sides of diaphragm
Stage IV: Diffuse extralymphatic involvement (liver, bone marrow, lungs)

Modifiers:
  A: No B symptoms
  B: B symptoms present (fever, night sweats, >10% weight loss)
  E: Extranodal extension
  S: Splenic involvement
  X: Bulky disease (>10 cm mass)
```

**Why this matters for generation**: A lymphoma patient with "Stage IIIB" has disease above and below the diaphragm WITH constitutional symptoms. This affects prognosis and treatment intensity.

#### FIGO Staging for Gynecologic Cancers

Used for ovarian, uterine, cervical, and other gynecologic malignancies:

```
Stage I: Confined to organ of origin
Stage II: Local extension (within pelvis)
Stage III: Spread beyond pelvis but within abdomen
Stage IV: Distant metastases
```

**Note**: FIGO staging has cancer-specific substaging criteria. Reference FIGO guidelines for specific cancer types.

### Performance Status

Performance status is CRITICAL in oncology - it determines treatment eligibility and prognosis.

#### ECOG Performance Status (Most Commonly Used)

```
ECOG 0: Fully active, able to carry on all pre-disease activities
        - Working full-time, no restrictions
        - Eligible for most aggressive treatments

ECOG 1: Restricted in strenuous activity but ambulatory
        - Can do light work, normal daily activities
        - Eligible for most standard treatments

ECOG 2: Ambulatory and capable of all self-care
        - Unable to work, up and about >50% of waking hours
        - Eligible for many treatments, may need dose modifications

ECOG 3: Limited self-care, confined to bed/chair >50% of waking hours
        - May still receive some treatments
        - Often focus shifts toward symptom management

ECOG 4: Completely disabled, cannot carry on any self-care
        - Totally confined to bed or chair
        - Generally NOT a candidate for systemic therapy
        - Focus on comfort care

ECOG 5: Dead
```

#### Karnofsky Performance Scale (KPS)

```
100: Normal, no complaints, no evidence of disease
90:  Able to carry on normal activity; minor symptoms
80:  Normal activity with effort; some symptoms

70:  Cares for self; unable to carry on normal activity or work
60:  Requires occasional assistance; cares for most needs
50:  Requires considerable assistance and frequent medical care

40:  Disabled; requires special care and assistance
30:  Severely disabled; hospitalization indicated
20:  Very sick; hospitalization necessary; active supportive treatment
10:  Moribund; fatal processes progressing rapidly
0:   Dead
```

**ECOG to KPS Mapping**:
```
ECOG 0 = KPS 90-100
ECOG 1 = KPS 70-80
ECOG 2 = KPS 50-60
ECOG 3 = KPS 30-40
ECOG 4 = KPS 10-20
```

**Why this matters for generation**: NEVER give a patient with ECOG 4 aggressive chemotherapy - they cannot tolerate it. A patient receiving curative-intent treatment should typically be ECOG 0-1.

### Treatment Modalities

#### Surgery

**Curative Surgery**:
- Goal: Remove all cancer with clear margins
- Examples: Mastectomy, colectomy, lobectomy, prostatectomy
- Typically for Stage I-III without distant metastasis

**Debulking (Cytoreductive) Surgery**:
- Goal: Remove as much tumor as possible
- Common in ovarian cancer
- Improves response to subsequent chemotherapy

**Palliative Surgery**:
- Goal: Relieve symptoms, not cure
- Examples: Bowel obstruction relief, tumor debulking for pain

#### Radiation Therapy

**External Beam Radiation Therapy (EBRT)**:
- Most common type
- Delivered over multiple fractions (typically 5 days/week for weeks)
- Measured in Gray (Gy), typical total doses 45-70 Gy

```
Common Fractionation Schemes:
- Definitive: 60-70 Gy in 30-35 fractions (6-7 weeks)
- Adjuvant breast: 50 Gy in 25 fractions (5 weeks)
- Palliative bone mets: 30 Gy in 10 fractions OR 8 Gy in 1 fraction
- Brain mets: 30 Gy in 10 fractions (whole brain)
```

**Stereotactic Radiosurgery/Body Radiation (SRS/SBRT)**:
- High-dose, precisely targeted radiation
- Fewer fractions (1-5 treatments)
- Used for limited metastatic disease, small primary tumors
- Examples: Brain mets, early lung cancer, liver mets

**Brachytherapy**:
- Radioactive source placed inside or near tumor
- Used in prostate, cervical, breast cancer
- Examples: Prostate seed implants, intracavitary cervical treatment

#### Systemic Therapy

**Cytotoxic Chemotherapy**:
Traditional chemotherapy that kills rapidly dividing cells.

```
Common Regimens by Cancer:

Breast Cancer:
  - AC (Doxorubicin + Cyclophosphamide)
  - TC (Docetaxel + Cyclophosphamide)
  - AC-T (AC followed by Paclitaxel)

Non-Small Cell Lung:
  - Carboplatin + Pemetrexed
  - Carboplatin + Paclitaxel
  - Cisplatin + Etoposide

Colon Cancer:
  - FOLFOX (5-FU + Leucovorin + Oxaliplatin)
  - FOLFIRI (5-FU + Leucovorin + Irinotecan)
  - CAPOX (Capecitabine + Oxaliplatin)

Lymphoma:
  - R-CHOP (Rituximab + Cyclophosphamide + Doxorubicin +
           Vincristine + Prednisone)
  - ABVD (Doxorubicin + Bleomycin + Vinblastine + Dacarbazine)
```

**Targeted Therapy**:
Drugs targeting specific molecular pathways in cancer cells.

```
Small Molecule Inhibitors (oral, end in -ib):
  - Imatinib: BCR-ABL (CML), KIT (GIST)
  - Erlotinib, Osimertinib: EGFR mutations (lung)
  - Vemurafenib, Dabrafenib: BRAF V600E (melanoma)
  - Palbociclib, Ribociclib: CDK4/6 (breast)
  - Olaparib: PARP (BRCA+ breast/ovarian)

Monoclonal Antibodies (IV, end in -mab):
  - Trastuzumab (Herceptin): HER2 (breast, gastric)
  - Bevacizumab (Avastin): VEGF (colon, lung, ovarian)
  - Cetuximab: EGFR (colon, head/neck)
  - Rituximab: CD20 (lymphomas)
```

**Immunotherapy**:
Drugs that enhance immune response against cancer.

```
Checkpoint Inhibitors:
  - PD-1 inhibitors: Pembrolizumab (Keytruda), Nivolumab (Opdivo)
  - PD-L1 inhibitors: Atezolizumab, Durvalumab
  - CTLA-4 inhibitors: Ipilimumab (Yervoy)

Indications:
  - Melanoma
  - Non-small cell lung cancer
  - Renal cell carcinoma
  - Bladder cancer
  - Hodgkin lymphoma
  - MSI-high/MMR-deficient cancers (any site)

CAR-T Cell Therapy:
  - Axicabtagene ciloleucel (Yescarta)
  - Tisagenlecleucel (Kymriah)
  - For relapsed/refractory large B-cell lymphoma, ALL
```

**Hormonal Therapy**:
For hormone-receptor positive cancers.

```
Breast Cancer (ER/PR positive):
  - Tamoxifen: Selective estrogen receptor modulator
  - Aromatase inhibitors: Letrozole, Anastrozole, Exemestane
  - Fulvestrant: ER degrader
  - Duration: 5-10 years for adjuvant therapy

Prostate Cancer:
  - GnRH agonists: Leuprolide, Goserelin (androgen deprivation)
  - GnRH antagonists: Degarelix
  - Antiandrogens: Bicalutamide, Enzalutamide, Abiraterone
```

#### Multimodal Approaches

**Neoadjuvant Therapy**:
- Systemic therapy BEFORE surgery
- Goals: Shrink tumor, assess response, treat micrometastases
- Common in breast cancer, rectal cancer, esophageal cancer

**Adjuvant Therapy**:
- Systemic therapy AFTER surgery
- Goal: Eliminate microscopic residual disease
- Common in breast, colon, lung (based on stage and features)

**Concurrent Chemoradiation**:
- Chemotherapy given with radiation (radiosensitizer)
- Used in locally advanced head/neck, cervical, anal, esophageal, lung

**Why this matters for generation**: A Stage III rectal cancer patient typically gets neoadjuvant chemoradiation FIRST, then surgery, then adjuvant chemotherapy. Don't skip steps in the sequence.

### Biomarkers and Molecular Testing

#### Common Actionable Mutations by Cancer Type

```
Lung Cancer (NSCLC):
  - EGFR mutations: Predict response to EGFR TKIs (osimertinib)
  - ALK rearrangements: Predict response to ALK inhibitors (alectinib)
  - ROS1 rearrangements: Predict response to crizotinib
  - BRAF V600E: Predict response to dabrafenib/trametinib
  - KRAS G12C: Predict response to sotorasib
  - PD-L1 expression: Predict response to immunotherapy

Breast Cancer:
  - ER (estrogen receptor): Positive = hormonal therapy indicated
  - PR (progesterone receptor): Positive = hormonal therapy indicated
  - HER2: Positive = trastuzumab + pertuzumab indicated
  - BRCA1/2 mutations: PARP inhibitors (olaparib) indicated

Colorectal Cancer:
  - KRAS/NRAS: Wild-type = anti-EGFR therapy (cetuximab) may work
  - BRAF V600E: Poor prognosis, specific targeted therapy
  - MSI-H/dMMR: Immunotherapy highly effective

Melanoma:
  - BRAF V600E/K: Targeted therapy (dabrafenib + trametinib)
  - PD-L1: Checkpoint inhibitors effective

Ovarian Cancer:
  - BRCA1/2: PARP inhibitors indicated
  - HRD (homologous recombination deficiency): PARP inhibitors
```

#### Immunohistochemistry (IHC) Markers

```
ER (Estrogen Receptor):
  - Reported as: Positive/Negative or % of cells staining
  - ER+ means hormonal therapy indicated

PR (Progesterone Receptor):
  - Often positive when ER is positive
  - PR+ reinforces hormonal therapy indication

HER2 (Human Epidermal Growth Factor Receptor 2):
  - IHC: 0, 1+, 2+, 3+
  - 3+ = HER2 positive
  - 2+ = Equivocal, need FISH testing
  - HER2+ = Trastuzumab indicated

PD-L1 (Programmed Death-Ligand 1):
  - Reported as: TPS (tumor proportion score) or CPS (combined positive score)
  - High PD-L1 = May respond better to immunotherapy
  - Different cutoffs for different cancers (1%, 50%, etc.)

Ki-67:
  - Proliferation marker
  - High Ki-67 (>20%) = More aggressive tumor
  - Used in breast cancer for treatment decisions
```

#### Genomic Testing

**Next-Generation Sequencing (NGS) Panels**:
- Test multiple genes simultaneously
- Foundation One, Tempus, Caris, Guardant Health
- Identifies actionable mutations for targeted therapy

**Liquid Biopsy**:
- Blood-based test for circulating tumor DNA (ctDNA)
- Can identify mutations when tissue biopsy not feasible
- Monitor for resistance mutations during treatment

**MSI/MMR Status**:
```
MSI-H (Microsatellite Instability-High) / dMMR (deficient Mismatch Repair):
  - ~15% of colorectal cancers
  - ~3-5% of all solid tumors
  - HIGHLY responsive to immunotherapy
  - Test all colorectal, endometrial, and consider in other cancers

MSS (Microsatellite Stable) / pMMR (proficient Mismatch Repair):
  - Most common
  - Less responsive to single-agent immunotherapy
```

### Response Assessment

#### RECIST 1.1 Criteria

Used to assess response to treatment on imaging:

```
Complete Response (CR):
  - Disappearance of all target lesions
  - Any pathological lymph nodes <10mm short axis

Partial Response (PR):
  - >=30% decrease in sum of target lesion diameters
  - Compared to baseline

Stable Disease (SD):
  - Neither PR nor PD criteria met
  - Some shrinkage but <30%, or some growth but <20%

Progressive Disease (PD):
  - >=20% increase in sum of target lesion diameters
  - AND absolute increase of >=5mm
  - OR appearance of new lesions
```

**Imaging Schedule**:
- Typically every 2-3 cycles of chemotherapy (6-9 weeks)
- CT chest/abdomen/pelvis most common
- PET/CT for lymphomas and metabolically active tumors

#### Tumor Markers for Monitoring

```
CEA (Carcinoembryonic Antigen):
  - Colorectal cancer (most useful)
  - Normal: <3-5 ng/mL
  - Monitor every 3-6 months in CRC

CA-125:
  - Ovarian cancer
  - Normal: <35 U/mL
  - Monitor with each treatment cycle

PSA (Prostate Specific Antigen):
  - Prostate cancer
  - Normal: <4 ng/mL (age-dependent)
  - Monitor every 3-6 months on treatment

CA 19-9:
  - Pancreatic cancer, biliary cancers
  - Normal: <37 U/mL
  - Monitor response to treatment

AFP (Alpha-Fetoprotein):
  - Hepatocellular carcinoma
  - Testicular cancer (non-seminoma)
  - Normal: <10-20 ng/mL

LDH (Lactate Dehydrogenase):
  - Non-specific tumor marker
  - Elevated in many aggressive cancers
  - Prognostic in lymphoma, melanoma, testicular

HCG (Human Chorionic Gonadotropin):
  - Testicular cancer
  - Gestational trophoblastic disease
```

**Why this matters for generation**: A patient responding to colon cancer treatment should show decreasing CEA. A patient with progressive ovarian cancer should have rising CA-125.

## Treatment Intent Categories

### Curative Intent

Goal is to eliminate all cancer and cure the patient.

**Characteristics**:
- Typically Stage I-III (varies by cancer type)
- Aggressive, maximal therapy
- Accept higher toxicity for cure
- Definitive local therapy (surgery and/or radiation)
- Systemic therapy to address micrometastatic disease

**Examples**:
- Stage II colon cancer: Surgery + adjuvant FOLFOX
- Stage IIIA NSCLC: Concurrent chemoradiation + durvalumab consolidation
- Localized Hodgkin lymphoma: ABVD chemotherapy

### Adjuvant Therapy

Systemic therapy given AFTER definitive local treatment (surgery/radiation).

**Purpose**:
- Treat micrometastatic disease not detectable on imaging
- Reduce recurrence risk
- Improve survival

**Examples**:
- Stage II-III breast cancer: Chemotherapy after surgery
- Stage III colon cancer: FOLFOX after colectomy
- High-risk melanoma: Immunotherapy after resection

### Neoadjuvant Therapy

Systemic therapy given BEFORE definitive local treatment.

**Purpose**:
- Shrink tumor to improve resectability
- Assess chemosensitivity
- Treat micrometastatic disease early
- May allow less extensive surgery

**Examples**:
- Locally advanced breast cancer: Chemotherapy before mastectomy
- Locally advanced rectal cancer: Chemoradiation before surgery
- Resectable pancreatic cancer: Chemotherapy before surgery

### Palliative Intent

Goal is to control disease and symptoms, not cure.

**Characteristics**:
- Typically Stage IV / metastatic disease
- Balance efficacy with quality of life
- May use less intensive regimens
- Focus on symptom management
- May continue indefinitely or until progression

**Examples**:
- Metastatic colon cancer: FOLFOX + bevacizumab
- Metastatic NSCLC: Pembrolizumab + chemotherapy
- Hormone-refractory prostate cancer: Docetaxel or cabazitaxel

### Maintenance Therapy

Continued therapy after initial response to prolong remission.

**Examples**:
- Ovarian cancer: PARP inhibitor maintenance after platinum response
- NSCLC: Pemetrexed maintenance after platinum-pemetrexed induction
- Multiple myeloma: Lenalidomide maintenance after transplant

**Why this matters for generation**: Always specify treatment intent. A "Stage IV" patient typically has palliative intent, NOT curative (with exceptions like germ cell tumors, some lymphomas).

## Common Toxicities and Supportive Care

### Myelosuppression

The most common dose-limiting toxicity of chemotherapy.

**Neutropenia**:
```
Grading:
  Grade 1: ANC 1500-2000/uL
  Grade 2: ANC 1000-1500/uL
  Grade 3: ANC 500-1000/uL
  Grade 4: ANC <500/uL (severe, high infection risk)

Febrile Neutropenia:
  - ANC <500/uL (or <1000 with predicted decline) + fever >=38.3C
  - ONCOLOGIC EMERGENCY
  - Requires immediate broad-spectrum antibiotics
  - Hospitalization often required

Nadir:
  - Typical nadir: 7-14 days after chemotherapy
  - Recovery by day 21-28 (next cycle timing)
```

**Management**:
```
G-CSF (Granulocyte Colony-Stimulating Factor):
  - Filgrastim (Neupogen): 5 mcg/kg/day SC starting day after chemo
  - Pegfilgrastim (Neulasta): 6 mg SC once per cycle (day after chemo)

Primary Prophylaxis:
  - Given when regimen has >20% risk of febrile neutropenia
  - All dose-dense regimens require G-CSF

Secondary Prophylaxis:
  - Given after episode of febrile neutropenia
  - Prevents recurrence in subsequent cycles
```

**Anemia**:
```
Chemotherapy-Induced Anemia:
  - Hemoglobin <10 g/dL common
  - Causes fatigue, dyspnea

Management:
  - Transfusion if Hgb <7-8 g/dL or symptomatic
  - ESAs (Erythropoietin-Stimulating Agents): Less commonly used now
  - Iron supplementation if iron-deficient
```

**Thrombocytopenia**:
```
Grading:
  Grade 1: Platelets 100-150K/uL
  Grade 2: Platelets 50-100K/uL
  Grade 3: Platelets 25-50K/uL
  Grade 4: Platelets <25K/uL (bleeding risk)

Management:
  - Hold anticoagulation if <50K
  - Platelet transfusion if <10K or <20K with bleeding/fever
  - Dose reduce or delay chemotherapy
```

### Chemotherapy-Induced Nausea and Vomiting (CINV)

**Emetogenic Potential Categories**:
```
High Emetogenic (>90% risk without antiemetics):
  - Cisplatin
  - Cyclophosphamide >1500 mg/m2
  - AC regimen (anthracycline + cyclophosphamide)
  - Carmustine

Moderate Emetogenic (30-90% risk):
  - Carboplatin
  - Oxaliplatin
  - Irinotecan
  - Cyclophosphamide <1500 mg/m2
  - Doxorubicin

Low Emetogenic (10-30% risk):
  - Docetaxel
  - Paclitaxel
  - Etoposide
  - 5-Fluorouracil
  - Gemcitabine
```

**Antiemetic Regimens**:
```
High Emetogenic Risk:
  Pre-chemo:
    - NK1 antagonist: Aprepitant 125mg PO or fosaprepitant 150mg IV
    - 5-HT3 antagonist: Ondansetron 8-16mg IV or palonosetron 0.25mg IV
    - Dexamethasone 12mg PO/IV
  Post-chemo:
    - Aprepitant 80mg PO days 2-3
    - Dexamethasone 8mg PO daily days 2-4
    - PRN: Prochlorperazine, lorazepam

Moderate Emetogenic Risk:
  Pre-chemo:
    - 5-HT3 antagonist: Ondansetron 8mg IV
    - Dexamethasone 12mg PO/IV
  Post-chemo:
    - Ondansetron 8mg PO BID days 2-3
    - Dexamethasone 8mg PO day 2-3
```

### Peripheral Neuropathy

**Causative Agents**:
```
Taxanes:
  - Paclitaxel, docetaxel
  - Sensory > motor
  - Often dose-limiting

Platinum Compounds:
  - Oxaliplatin: Acute (cold sensitivity) and chronic
  - Cisplatin: Cumulative, may be irreversible

Vinca Alkaloids:
  - Vincristine: Motor and sensory
  - Often dose-limiting

Proteasome Inhibitors:
  - Bortezomib (myeloma)
  - Can be severe
```

**Management**:
- Dose reduction or discontinuation
- Gabapentin 300-600mg TID or pregabalin
- Duloxetine 60mg daily (some evidence)
- Physical therapy

### Cardiotoxicity

**Anthracycline Cardiomyopathy**:
```
Agents: Doxorubicin, epirubicin, daunorubicin

Mechanism: Direct myocardial damage, dose-dependent

Cumulative Dose Limits:
  - Doxorubicin: 450-550 mg/m2 lifetime maximum
  - Epirubicin: 900 mg/m2 lifetime maximum

Monitoring:
  - Baseline ECHO or MUGA before starting
  - Repeat every 3 months or after 300 mg/m2 cumulative
  - Hold if LVEF drops >10% or <50%

Prevention:
  - Dexrazoxane (Zinecard): Cardioprotectant
  - Liposomal formulations (less cardiotoxic)
```

**HER2-Targeted Agent Cardiotoxicity**:
```
Agents: Trastuzumab, pertuzumab

Mechanism: Myocardial dysfunction (usually reversible)

Monitoring:
  - ECHO every 3 months while on therapy
  - Hold if LVEF <50% or drops >16% from baseline

Management:
  - Usually reversible with holding therapy
  - May rechallenge when LVEF recovers
```

### Nephrotoxicity

**Cisplatin Nephrotoxicity**:
```
Mechanism: Direct tubular damage, dose-dependent, cumulative

Prevention:
  - Aggressive IV hydration (1-2L before and after)
  - Avoid concurrent nephrotoxins (NSAIDs, aminoglycosides)
  - Magnesium supplementation

Monitoring:
  - Creatinine before each cycle
  - Dose reduce or switch to carboplatin if creatinine rises

Why it matters: Cisplatin is one of the most effective agents for many cancers.
Dose modifications and switches to carboplatin are common.
```

### Growth Factor and Supportive Care Summary

```
G-CSF (Neutropenia Prevention):
  - Filgrastim (Neupogen): 5 mcg/kg SC daily days 2-7 or until recovery
  - Pegfilgrastim (Neulasta): 6 mg SC once, 24hr after chemo

ESAs (Anemia - less commonly used):
  - Epoetin alfa: 40,000 units SC weekly
  - Darbepoetin: 200 mcg SC every 2 weeks

Antiemetics:
  - Ondansetron, granisetron (5-HT3 antagonists)
  - Aprepitant, fosaprepitant (NK1 antagonists)
  - Dexamethasone (steroid)
  - Prochlorperazine, metoclopramide (dopamine antagonists)
  - Olanzapine (for refractory CINV)

Pain Management:
  - WHO Pain Ladder: Non-opioid → Weak opioid → Strong opioid
  - Long-acting opioids for baseline pain (MS Contin, fentanyl patch)
  - Short-acting for breakthrough (morphine IR, oxycodone IR)
  - Adjuvants: Gabapentin (neuropathic), NSAIDs (bone pain)
```

## Oncology Care Settings

### Outpatient Infusion Center

**Most chemotherapy is administered here**:
- Typical visit: 2-6 hours depending on regimen
- Pre-medications given first (antiemetics, steroids)
- IV chemotherapy infusions
- Post-treatment observation

**Typical Visit Flow**:
```
1. Check-in and vital signs
2. Phlebotomy (labs before treatment)
3. Provider assessment (if scheduled)
4. Pharmacy reviews/prepares drugs
5. Pre-medications infused
6. Chemotherapy infused
7. Post-treatment monitoring
8. Discharge with home medications and instructions
```

### Inpatient Oncology

**Indications for Hospitalization**:
- Febrile neutropenia
- Severe treatment toxicity
- Intensive chemotherapy regimens (leukemia induction)
- Stem cell transplant
- Acute complications (bowel obstruction, cord compression)

**Oncologic Emergencies**:
```
Febrile Neutropenia:
  - ANC <500 + fever
  - Immediate broad-spectrum antibiotics
  - Risk stratification (MASCC score)

Tumor Lysis Syndrome:
  - Massive cell death releasing contents
  - Hyperuricemia, hyperkalemia, hyperphosphatemia, hypocalcemia
  - Prevention: Hydration, allopurinol/rasburicase

Spinal Cord Compression:
  - Back pain + neurologic symptoms
  - MRI urgently, high-dose steroids, radiation/surgery

Hypercalcemia of Malignancy:
  - Calcium >12 mg/dL with symptoms
  - IV fluids, bisphosphonates (zoledronic acid)

Superior Vena Cava Syndrome:
  - Face/arm swelling, dyspnea
  - Urgent radiation or stent
```

### Radiation Oncology Department

**Typical Treatment Course**:
- Simulation (CT planning session)
- Treatment planning (dosimetry, physician review)
- Daily treatments (Monday-Friday, typically)
- Weekly on-treatment visits with physician

**Treatment Duration**:
```
Definitive (curative): 6-7 weeks (30-35 fractions)
Adjuvant breast: 3-5 weeks (15-25 fractions)
Palliative: 1-2 weeks (5-10 fractions) or single fraction
SBRT: 1-5 treatments over 1-2 weeks
```

### Palliative Care and Hospice

**Palliative Care**:
- Symptom management alongside cancer treatment
- Can be concurrent with curative-intent therapy
- Focus: Pain, nausea, dyspnea, depression, goals of care

**Hospice**:
- End-of-life care when curative treatment stopped
- Prognosis typically <6 months
- Focus on comfort, not life prolongation
- Can be home-based or inpatient

**Transition Triggers**:
```
Consider hospice referral when:
  - Disease progressing despite multiple lines of therapy
  - ECOG 3-4 (poor functional status)
  - Declining to tolerate further treatment
  - Patient goals shift to comfort-focused care
  - Estimated prognosis <6 months
```

## Oncology-Specific Coding Patterns

### Primary Malignancy Codes

```
C50.x: Breast
  C50.911: Right breast, female
  C50.912: Left breast, female

C34.x: Lung
  C34.11: Upper lobe, right
  C34.12: Middle lobe, right
  C34.31: Lower lobe, right
  C34.90: Unspecified

C18.x: Colon
  C18.0: Cecum
  C18.2: Ascending colon
  C18.4: Transverse colon
  C18.6: Descending colon
  C18.7: Sigmoid colon

C61: Prostate (no laterality)

C20: Rectum

C56.x: Ovary
  C56.1: Right ovary
  C56.2: Left ovary

C81-C85: Lymphomas
  C81: Hodgkin lymphoma
  C83: Non-Hodgkin lymphoma (diffuse)
  C85.9: NHL, unspecified

C90.0x: Multiple myeloma

C91-C95: Leukemias
  C91.0x: Acute lymphoblastic leukemia (ALL)
  C91.1x: Chronic lymphocytic leukemia (CLL)
  C92.0x: Acute myeloid leukemia (AML)
  C92.1x: Chronic myeloid leukemia (CML)
```

### Secondary (Metastatic) Codes

```
C77.x: Secondary to lymph nodes
  C77.0: Head, face, neck nodes
  C77.3: Axillary and upper limb nodes
  C77.4: Inguinal and lower limb nodes

C78.0x: Secondary malignant neoplasm of lung
C78.7: Secondary malignant neoplasm of liver
C78.6: Secondary to retroperitoneum and peritoneum

C79.31: Secondary to brain
C79.51: Secondary to bone
C79.81: Secondary to breast
```

### History and Encounter Codes

```
Personal History of Malignancy (Z85.x):
  Z85.3: Personal history of breast cancer
  Z85.118: Personal history of lung cancer
  Z85.038: Personal history of colon cancer
  Z85.46: Personal history of prostate cancer

Encounter for Treatment:
  Z51.11: Encounter for antineoplastic chemotherapy
  Z51.12: Encounter for antineoplastic immunotherapy
  Z51.0: Encounter for antineoplastic radiation therapy

Surveillance:
  Z08: Encounter for follow-up after completed treatment
  Z09: Encounter for follow-up after completed treatment (different conditions)
```

### Adverse Effect Codes

```
Myelosuppression:
  D70.1: Drug-induced neutropenia
  D61.1: Drug-induced aplastic anemia
  D69.59: Other secondary thrombocytopenia

Nausea/Vomiting:
  R11.0: Nausea
  R11.10: Vomiting, unspecified
  T45.1X5A: Adverse effect of antineoplastic drugs, initial encounter

Neuropathy:
  G62.0: Drug-induced polyneuropathy
  T45.1X5A: Adverse effect code

Cardiotoxicity:
  I42.7: Cardiomyopathy due to drug and external agent
  T45.1X5A: Adverse effect code
```

**Why this matters for generation**: Always pair primary cancer codes with metastatic site codes for Stage IV disease. Use Z51.11 as secondary code for chemotherapy encounters. Include adverse effect codes when generating toxicity scenarios.

## Cross-Domain Connections

### Oncology + Chronic Kidney Disease

**Cisplatin Nephrotoxicity**:
- Cisplatin causes dose-dependent nephrotoxicity
- Monitor creatinine before each cycle
- Dose reduce or switch to carboplatin if creatinine rises
- May need to avoid cisplatin entirely in pre-existing CKD

**Medication Adjustments**:
```
Adjust for Renal Function (eGFR):
  - Carboplatin: Dose by Calvert formula using GFR
  - Methotrexate: Reduce dose and monitor levels
  - Lenalidomide: Reduce dose if CrCl <60

Avoid in Severe CKD:
  - Cisplatin (switch to carboplatin)
  - High-dose methotrexate
```

**Contrast Concerns**:
- CT scans with contrast needed for staging
- Assess renal function before contrast
- Hydration protocols, avoid nephrotoxins

### Oncology + Heart Failure

**Anthracycline Cardiomyopathy**:
- Doxorubicin, epirubicin cause cumulative cardiomyopathy
- Lifetime dose limits (doxorubicin 450-550 mg/m2)
- Monitor LVEF, hold if drops significantly
- Consider liposomal doxorubicin or alternative regimens

**HER2 Agent Cardiotoxicity**:
- Trastuzumab, pertuzumab can cause reversible LVEF decline
- Monitor ECHO every 3 months
- Often can rechallenge after recovery

**Management in Pre-existing HF**:
```
Cautions:
  - Avoid or reduce anthracyclines
  - Careful fluid management (high-volume hydration for cisplatin)
  - Close cardiology involvement
  - Consider cardio-oncology consultation
```

### Oncology + Diabetes

**Steroid-Induced Hyperglycemia**:
- Dexamethasone used in antiemetic regimens (common)
- Prednisone in lymphoma regimens (R-CHOP)
- High-dose steroids for brain mets, cord compression

**Management**:
```
Pre-existing Diabetes:
  - Increase monitoring during steroid days
  - May need insulin dose increase 30-50% on steroid days
  - Sliding scale coverage for inpatients
  - Return to baseline after steroids stopped

New Hyperglycemia:
  - Common during treatment
  - Usually transient
  - May need short-term insulin coverage
```

### Oncology + Specialty Pharmacy

**Oral Oncolytics**:
```
Common Oral Cancer Drugs (Specialty Pharmacy):
  - Ibrutinib (CLL, lymphoma)
  - Osimertinib (EGFR+ lung cancer)
  - Palbociclib, ribociclib (breast cancer)
  - Capecitabine (colon, breast cancer)
  - Enzalutamide, abiraterone (prostate cancer)
  - Olaparib (BRCA+ breast/ovarian)
  - Lenalidomide (multiple myeloma)

Characteristics:
  - High cost ($10,000-$20,000+/month)
  - Often require specialty pharmacy distribution
  - REMS programs for some (lenalidomide, thalidomide)
  - Adherence monitoring critical
```

**Supportive Care Medications**:
```
Antiemetics:
  - Aprepitant, fosaprepitant (NK1 antagonists)
  - Ondansetron, palonosetron (5-HT3 antagonists)

Growth Factors:
  - Pegfilgrastim (Neulasta): ~$6,000/dose
  - Filgrastim (Neupogen)
  - On-body injector options

Bone-Modifying Agents:
  - Denosumab (Xgeva): For bone mets
  - Zoledronic acid (Zometa)
```

**Why this matters for generation**: Specialty pharmacy scenarios for oncology should include appropriate oral oncolytics with realistic costs, prior authorization requirements, and REMS compliance when applicable.

## Generation Guidelines

### How to Apply This Knowledge

**When the user says**: "Generate a cancer patient"

**Claude should**:
1. **Choose cancer type**: Select common cancer appropriate for demographics
2. **Determine stage**: Default to Stage III-IV unless specified (common scenario)
3. **Assign performance status**: ECOG 0-1 for patients on treatment
4. **Select treatment**: Match to cancer type, stage, and treatment intent
5. **Include staging details**: TNM for solid tumors, Ann Arbor for lymphomas
6. **Generate appropriate labs**: Tumor markers, CBC with potential cytopenias
7. **Add supportive care**: Antiemetics, growth factors as appropriate

**When the user says**: "Generate a patient receiving chemotherapy"

**Claude should**:
1. **Identify cancer type and regimen**: Choose realistic combination
2. **Set cycle number**: Usually cycles 1-6 for adjuvant, ongoing for palliative
3. **Include toxicity potential**: Nadir neutropenia, nausea grading
4. **Add supportive medications**: Antiemetics, G-CSF if indicated
5. **Generate timeline**: Day of cycle, expected nadir, recovery

**When the user says**: "Generate a patient with metastatic breast cancer"

**Claude should**:
1. **Set stage**: Stage IV (metastatic)
2. **Choose metastatic sites**: Bone, liver, lung, brain most common
3. **Include biomarkers**: ER/PR/HER2 status determines treatment
4. **Select treatment**: Based on biomarker status (hormonal, HER2-targeted, or chemo)
5. **Set treatment intent**: Palliative (not curative)
6. **Include both primary and metastatic codes**: C50.x + C79.x codes

### Coherence Checks

Before finalizing an oncology patient, verify:

```python
# 1. Stage-Treatment Intent Coherence
if stage == "IV" and not exception_cancer:
    assert treatment_intent == "palliative"  # Not curative

# 2. Performance Status-Treatment Coherence
if ECOG >= 3:
    assert not aggressive_chemotherapy  # Too frail for aggressive treatment

# 3. Staging System Coherence
if cancer_type == "lymphoma":
    assert staging_system == "Ann Arbor"  # Not TNM
if cancer_type in solid_tumors:
    assert staging_system == "TNM"  # Not Ann Arbor

# 4. Biomarker-Treatment Coherence
if breast_cancer and HER2_positive:
    assert has_trastuzumab_in_regimen()
if breast_cancer and ER_positive:
    assert has_hormonal_therapy()

# 5. Tumor Marker-Disease Status Coherence
if progressive_disease:
    assert tumor_markers_rising()  # CEA, CA-125 should trend up
if responding_to_treatment:
    assert tumor_markers_declining()

# 6. Toxicity-Treatment Coherence
if on_cisplatin:
    monitor_for_nephrotoxicity()
if on_anthracycline:
    monitor_cardiac_function()
    check_cumulative_dose()

# 7. ICD-10 Code Coherence
if metastatic:
    assert has_primary_code AND has_secondary_code
    # Both C50.x (primary) AND C79.x (metastatic site)
```

### Example Request: "Generate a lung cancer patient on chemotherapy"

**Claude should interpret**:
- Cancer type: Non-small cell lung cancer (most common)
- Stage: Stage IIIB or IV (chemotherapy indicated)
- Histology: Adenocarcinoma (most common NSCLC subtype)
- Performance status: ECOG 1 (on treatment, functional)

**Key features Claude generates**:

**Demographics**:
- Age 66, male, former smoker (35 pack-years)

**Diagnosis**:
- C34.90 (Lung cancer, unspecified)
- C79.51 (Secondary to bone) - if Stage IV
- C79.31 (Secondary to brain) - if applicable

**Staging**:
- Stage IIIB: T3N2M0 or T4N2M0
- Or Stage IV: Any T, Any N, M1

**Biomarkers**:
- EGFR: Wild-type
- ALK: Negative
- PD-L1: 60% (high, immunotherapy benefit)
- KRAS G12C: Positive (sotorasib option)

**Treatment**:
- Cycle 3 of 4: Carboplatin AUC 5 + Pemetrexed 500 mg/m2 + Pembrolizumab 200 mg
- Given every 21 days
- Pembrolizumab maintenance planned after 4 cycles

**Performance Status**: ECOG 1

**Supportive Care**:
- Ondansetron 8 mg IV pre-chemo
- Dexamethasone 8 mg IV pre-chemo
- Ondansetron 8 mg PO BID x 3 days home
- Vitamin B12 + folic acid supplementation (for pemetrexed)

**Labs**:
- WBC 5.2, ANC 3800 (recovered from last cycle)
- Hemoglobin 11.2 (mild anemia of chronic disease)
- Platelets 165
- Creatinine 1.0 (normal, carboplatin okay)
- LDH 280 (slightly elevated, tumor burden marker)

**Imaging**: CT chest/abdomen/pelvis after cycle 4 for response assessment

## Related Skills

**Cancer-Specific Scenario Skills** (to be developed):
- skills/breast-cancer.md
- skills/lung-cancer.md
- skills/colorectal-cancer.md
- skills/lymphoma.md
- skills/prostate-cancer.md

**Complementary Domain Skills**:
- skills/healthcare/clinical-domain.md - General clinical knowledge
- skills/healthcare/specialty-pharmacy-oncology.md - Oral oncolytics detail

**Format Skills**:
- skills/formats/fhir-r4.md - FHIR export for oncology resources
- skills/formats/hl7v2-adt.md - Oncology admission messages
- skills/formats/x12-837.md - Oncology claims formatting

## References

**Clinical Guidelines**:
- NCCN Clinical Practice Guidelines in Oncology (by tumor type)
- ASCO Clinical Practice Guidelines
- AJCC Cancer Staging Manual, 8th Edition
- Surviving Sepsis Campaign (for febrile neutropenia)
- MASCC/ESMO Antiemetic Guidelines

**Staging Systems**:
- American Joint Committee on Cancer (AJCC) TNM Staging
- Ann Arbor Staging for Lymphomas
- FIGO Staging for Gynecologic Cancers

**Response Criteria**:
- RECIST 1.1 (Response Evaluation Criteria in Solid Tumors)
- Lugano Classification (lymphoma response)
- IMWG Criteria (multiple myeloma response)

**Performance Scales**:
- ECOG Performance Status (Oken et al., 1982)
- Karnofsky Performance Scale

## Clinical Validation Notice

This domain knowledge skill was AI-generated and requires clinical validation before use in any production or clinical decision-support context. The information provided is intended for synthetic data generation for testing and training purposes only.

Key areas requiring validation:
- Treatment regimen accuracy and currency
- Staging criteria alignment with current AJCC edition
- Biomarker-treatment matching per current guidelines
- Supportive care protocols per institutional standards
- ICD-10 code accuracy and specificity

Last validation review: Pending
