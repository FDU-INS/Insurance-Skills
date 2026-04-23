# Hello HealthSim!

**Get up and running with synthetic healthcare data generation in 5 minutes.**

HealthSim is a skill-based framework that enables Claude to generate realistic synthetic healthcare data through natural conversation. No coding required - just describe what you need.

> **⚠️ Important Notice**
>
> HealthSim generates **synthetic test data only**. It is not a clinical decision support system and does not provide medical advice, diagnosis recommendations, or treatment guidance. The clinical patterns, medication regimens, and lab values produced are for software testing, development, training, and demonstration purposes. They reflect general healthcare conventions but should never be used for actual patient care decisions.

## What You'll Build

By the end of this guide, you'll be able to generate:

- **Clinical Data** - Patients with realistic diagnoses, medications, and lab results
- **Claims Data** - Professional and facility claims with proper adjudication
- **Pharmacy Data** - Prescriptions, pharmacy claims, and drug utilization alerts
- **Saved Scenarios** - Persistent workspaces you can resume, branch, and share

All through simple natural language requests like:
> "Generate a 65-year-old diabetic patient with hypertension and their recent office visit claim"

---

## Access Methods

HealthSim can be accessed in four ways:

| Method | Best For | Setup |
|--------|----------|-------|
| **Claude Code** (local) | Development, testing, skill editing | [Setup below](#prerequisites) |
| **Console UI** (cloud) | Quick testing, ad-hoc queries | [Managed Agent Guide](../docs/MANAGED-AGENT-GUIDE.md) |
| **CLI** (cloud) | Scripted access, terminal-based chat | [Deploy README](../deploy/README.md) |
| **Web App** (cloud) | End users, team access | Coming soon via Rewire |

This guide focuses on **Claude Code** (local development). For cloud deployment and access, see the [Managed Agent Guide](../docs/MANAGED-AGENT-GUIDE.md).

---

## Prerequisites

Before starting, ensure you have:

| Requirement | Version | Check Command |
|-------------|---------|---------------|
| Git | 2.0+ | `git --version` |
| Python | 3.10+ | `python3 --version` |
| Claude Desktop **or** Claude Code | Latest | See installation links below |
| Anthropic API Key (for Claude Code) | - | [Get API Key](https://console.anthropic.com/) |

### Python Environment

HealthSim uses DuckDB for state management and reference data. The `healthsim-core` package includes DuckDB as a dependency - no separate installation required.

```bash
# Create and activate a virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install healthsim-core (includes DuckDB)
cd packages/core
pip install -e .
```

The DuckDB database is created automatically at `~/.healthsim/healthsim.duckdb` on first use.

### Install Claude (Choose One)

**Option A: Claude Desktop** (Recommended for beginners)
- Download from [claude.ai/download](https://claude.ai/download)
- Requires Claude Pro subscription for extended usage

**Option B: Claude Code** (For developers)
```bash
# Install via npm
npm install -g @anthropic-ai/claude-code

# Or via Homebrew (macOS)
brew install claude-code
```

---

## Quick Start

### Step 1: Clone the Repository

```bash
# Clone HealthSim skills
git clone https://github.com/mark64oswald/healthsim-common.git

# Navigate to the project
cd healthsim-common
```

### Step 2: Configure Claude

Choose your Claude environment and follow the appropriate guide:

| Environment | Guide | Best For |
|-------------|-------|----------|
| Claude Desktop | [CLAUDE-DESKTOP.md](CLAUDE-DESKTOP.md) | Interactive exploration, non-developers |
| Claude Code | [CLAUDE-CODE.md](CLAUDE-CODE.md) | Developers, automation, CI/CD |

### Step 3: Verify Installation

Once configured, test with this simple prompt:

```
Generate a patient with Type 2 diabetes
```

You should see output like:
```json
{
  "patient": {
    "mrn": "MRN00000001",
    "name": { "given_name": "Maria", "family_name": "Garcia" },
    "birth_date": "1962-05-14",
    "gender": "F"
  },
  "diagnoses": [
    { "code": "E11.9", "description": "Type 2 diabetes mellitus without complications" }
  ],
  "medications": [
    { "name": "Metformin", "dose": "1000 mg", "frequency": "BID" }
  ]
}
```

**Congratulations!** You're ready to generate healthcare data!

---

## Your First 5 Minutes

Try these examples to explore HealthSim's capabilities:

### Example 1: Generate a Patient (PatientSim)

```
Generate a 72-year-old male with heart failure and COPD, including recent labs
```

### Example 2: Generate a Claim (MemberSim)

```
Generate a paid professional claim for a cardiology office visit
```

### Example 3: Generate a Pharmacy Claim (RxMemberSim)

```
Generate a pharmacy claim for lisinopril with a drug interaction alert
```

### Example 4: Generate a Clinical Trial (TrialSim)

```
Generate a Phase 3 oncology trial with 50 subjects
```

### Example 5: Population Intelligence (PopulationSim)

```
Generate a population profile for Maricopa County, Arizona including demographics and SDOH
```

### Example 6: Cross-Domain Generation

```
Generate a diabetic patient with their recent office visit claim and pharmacy claims for their medications
```

### Example 7: Format Transformation

```
Generate an HL7 ADT^A01 admission message for a patient with pneumonia
```

See [examples/](examples/) for more detailed examples with expected outputs.

---

## Hello, Diabetes!

Let's explore a common chronic disease scenario with output format variations.

### Basic Diabetic Patient

```
Generate a 58-year-old female with Type 2 diabetes
```

This generates a patient with:

- Diagnosis (E11.9 Type 2 diabetes)
- Common comorbidities (hypertension, hyperlipidemia)
- Appropriate medications (metformin, lisinopril, atorvastatin)
- Relevant labs (A1C, glucose, creatinine)

### With Complications

```
Generate a diabetic patient with nephropathy and retinopathy
```

This adds diabetic complications with appropriate staging and specialist referrals.

### As FHIR Bundle

```
Generate a diabetic patient as a FHIR Bundle
```

Same clinical content, but formatted as FHIR R4 resources - perfect for testing FHIR APIs.

### As CSV for Analytics

```
Generate 10 diabetic patients as CSV
```

Generates tabular data suitable for spreadsheets and analytics tools.

---

## Hello, Claims!

Now let's generate claims data with different payment scenarios.

### Paid Claim (Basic)

```
Generate a paid professional claim for a primary care office visit
```

This generates:

- Member information
- Claim with CPT 99213/99214 (E&M code)
- Adjudication with copay applied
- CARC/RARC adjustment codes

### Denied Claim

```
Generate a denied professional claim for an MRI requiring prior authorization
```

This generates a claim with denial reason CO-15 (prior auth required) and appeal information.

### Facility Claim with DRG

```
Generate an inpatient admission claim for heart failure with DRG
```

This generates an 837I institutional claim with DRG assignment and length-of-stay based payment.

### As X12 837P Format

```
Generate a professional claim as X12 837P
```

Same claim data, but in EDI X12 format - perfect for testing claims processing systems.

---

## Hello, Pharmacy!

Generate pharmacy claims with clinical interventions.

### Simple Prescription Fill

```
Generate a pharmacy claim for atorvastatin 20mg
```

This generates:

- Prescription details (NDC, quantity, days supply)
- Pharmacy claim (BIN, PCN, cardholder ID)
- Pricing (ingredient cost, dispensing fee, copay)
- Tier information (generic = Tier 1)

### Drug Interaction Alert

```
Generate a pharmacy claim for warfarin that triggers a drug interaction alert with aspirin
```

This generates a DUR (Drug Utilization Review) alert with:

- Interaction severity (DD - Drug-Drug)
- Clinical significance
- Pharmacist recommendation

### Prior Authorization Required

```
Generate a specialty pharmacy claim for Humira requiring prior authorization
```

This generates the PA workflow for high-cost biologics with clinical criteria.

### As NCPDP Format

```
Generate a pharmacy claim as NCPDP D.0
```

Same pharmacy data in NCPDP telecommunications standard format.

---

## Hello, Oncology!

PatientSim includes comprehensive oncology scenario skills for generating realistic cancer patient journeys with accurate staging, biomarkers, and treatment protocols.

### Breast Cancer Patient

```
Generate a 55-year-old female with Stage IIA ER-positive, HER2-negative breast cancer
```

This generates a complete breast cancer patient with:

- TNM staging (T2 N0 M0)
- Biomarkers (ER 95%, PR 80%, HER2 1+, Ki-67 15%)
- Molecular subtype (Luminal A)
- Oncotype DX score and chemotherapy benefit assessment
- Surgical details (lumpectomy, sentinel node biopsy)
- Treatment plan (surgery → radiation → hormonal therapy)

### Lung Cancer with Targeted Therapy

```
Generate a 68-year-old male with Stage IV NSCLC, EGFR exon 19 deletion positive, with brain metastases
```

This generates biomarker-driven lung cancer treatment:

- Comprehensive molecular testing (EGFR, ALK, ROS1, PD-L1)
- Brain metastases management (SRS)
- Targeted therapy selection (osimertinib for EGFR mutation)
- Surveillance imaging schedule

### Colorectal Cancer with Biomarkers

```
Generate a 58-year-old with Stage III colon cancer, MSI-high status
```

This generates colorectal cancer with genomic context:

- MSI/MMR testing results
- RAS/BRAF mutation status
- Genetic counseling referral (Lynch syndrome evaluation)
- Adjuvant chemotherapy (CAPOX) with duration

### Cancer Patient with Comorbidities

```
Generate a 70-year-old with Stage IIIB colon cancer who has CKD Stage 3b and Type 2 diabetes requiring chemotherapy dose adjustments
```

This generates multi-morbid oncology patients:

- Chemotherapy dose modifications for renal function
- Multi-specialty care coordination
- Enhanced monitoring protocols

See [examples/oncology-examples.md](examples/oncology-examples.md) for detailed oncology examples with complete outputs.

---

## Hello, Clinical Trials!

TrialSim generates realistic synthetic clinical trial data for testing CDISC-compliant systems, regulatory submission pipelines, and clinical data management tools.

> **Note:** TrialSim generates synthetic clinical trial data only. This is test data for software development - the trial designs, adverse event patterns, and efficacy results are simulated.

### Phase 3 Pivotal Trial

```
Generate a Phase 3 oncology trial with 200 subjects randomized 2:1 to treatment vs placebo
```

This generates a complete Phase 3 trial with:

- Study design (randomization ratio, masking, endpoints)
- 20 sites across multiple countries
- 200 subjects with demographics and baseline characteristics
- Treatment arm assignments
- Subject disposition (completers, discontinuations)

### Adverse Events with MedDRA Coding

```
Generate adverse events for a Phase III immunotherapy trial with 150 subjects
```

This generates safety data with:

- Treatment-emergent adverse events (TEAEs)
- Serious adverse events (SAEs)
- MedDRA hierarchy (SOC → HLGT → HLT → PT → LLT)
- CTCAE grades and causality assessments

### SDTM Domain Output

```
Generate DM and AE domains for 50 subjects as SDTM
```

This generates CDISC-compliant datasets:

- Demographics (DM) with USUBJID, ARM, RFSTDTC
- Adverse Events (AE) with MedDRA coding
- Ready for regulatory submission testing

### Phase 1 Dose Escalation

```
Generate a Phase 1 dose escalation study using 3+3 design with 5 dose levels
```

This generates first-in-human trial data:

- Cohort-by-cohort dose escalation
- Dose-limiting toxicities (DLTs)
- Maximum tolerated dose (MTD) determination
- Pharmacokinetic sampling schedule

### Efficacy with RECIST

```
Generate tumor response data for an oncology trial with RECIST 1.1 assessments
```

This generates efficacy endpoints:

- Target lesion measurements
- Response categories (CR, PR, SD, PD)
- Best overall response
- Change from baseline calculations

### Star Schema for Trial Analytics

```
Generate Phase III trial with 100 subjects as star schema for DuckDB
```

This creates dimensional analytics tables:

- **Dimensions**: dim_study, dim_site, dim_subject, dim_treatment_arm, dim_meddra
- **Facts**: fact_enrollment, fact_adverse_event, fact_efficacy, fact_visit
- Ready for enrollment dashboards, safety surveillance, site performance

See [examples/trialsim-examples.md](examples/trialsim-examples.md) for comprehensive clinical trial examples.

---

## Hello, Population Intelligence!

PopulationSim provides access to **real population health data** from CDC PLACES, Social Vulnerability Index, and Area Deprivation Index. Unlike other HealthSim products that generate synthetic data, PopulationSim queries embedded real-world statistics to ground your data generation in evidence.

### County Health Profile

```
Profile Maricopa County, Arizona for health indicators and SDOH
```

This returns real data including:

- Demographics (population, age distribution, race/ethnicity)
- Chronic disease prevalence (diabetes 10.2%, obesity 31.5%, etc.)
- Health behaviors (smoking, binge drinking, physical inactivity)
- Social vulnerability themes (economic, housing, minority status)

### Census Tract Analysis

```
Show health disparities across census tracts in Los Angeles County
```

This provides neighborhood-level granularity:

- Tract-by-tract health measures from CDC PLACES
- SVI vulnerability scores for each tract
- ADI deprivation rankings at block group level

### Cohort Specification

```
Build a cohort specification for a Phase III diabetes trial targeting the Midwest
```

This creates an evidence-based CohortSpecification:

- Target demographics grounded in actual county distributions
- Expected disease prevalence from CDC data
- SDOH factors affecting enrollment feasibility
- Ready to use with PatientSim for realistic patient generation

### Trial Site Selection

```
Identify top 5 counties for a NASH trial based on patient availability and site access
```

This provides trial planning intelligence:

- Disease prevalence rankings from CDC PLACES
- Population size and demographic fit
- Healthcare access indicators from SVI
- Site selection recommendations

### Data-Driven Generation

When you specify a geography, PopulationSim's embedded data grounds generation across all products:

```
Generate 20 diabetic patients for Harris County, TX with real prevalence data
```

This produces patients reflecting actual Harris County statistics:

- 12.1% diabetes prevalence (not generic 10%)
- Real comorbidity correlations (33% obesity, 32% hypertension)
- Demographics matching county distributions
- Data provenance tracking in output

See [examples/populationsim-examples.md](examples/populationsim-examples.md) for detailed examples.

---

## Hello, Provider Networks!

NetworkSim provides access to **8.9 million real US healthcare providers** from the NPPES registry stored in DuckDB. Query real providers for validation and analysis, or generate synthetic providers when real data isn't appropriate for your use case.

### Query Real Providers (Primary Use Case)

```
Find cardiologists in Houston, Texas
```

This queries the real NPPES registry and returns:

- Actual NPIs from the national provider database
- Real taxonomy codes and specialties
- Actual practice addresses
- Provider credentials (MD, DO, NP, etc.)

### Analyze Provider Distribution

```
How many primary care physicians are in San Diego County?
```

NetworkSim analyzes real provider data:

- Provider counts by specialty and geography
- Network adequacy analysis
- Provider-to-population ratios

### Verify Provider Information

```
Is NPI 1234567890 a valid cardiologist?
```

Look up any NPI to verify:

- Provider exists in NPPES
- Specialty and taxonomy codes
- Practice location and credentials

### Generate Synthetic Providers (When Needed)

When real data isn't appropriate (tutorials, demos, testing):

```
Generate a synthetic cardiologist for this patient's encounter
```

This creates a synthetic provider with:

- Valid-format NPI (synthetic, not from registry)
- Appropriate specialty taxonomy code
- Practice address in the specified location

### Generate Facilities and Pharmacies

```
Generate a 350-bed acute care hospital in Phoenix
```

```
Generate a specialty pharmacy for oncology medications
```

### Understanding Network Types

```
Explain the differences between HMO, PPO, and EPO network structures
```

NetworkSim provides reference knowledge about:

- Network design patterns and access rules
- Cost sharing differences
- Referral and authorization requirements

### Integration with Other Products

NetworkSim provides provider data for other HealthSim products:

- **PatientSim encounters**: Real or synthetic provider for the visit
- **MemberSim claims**: Billing provider with NPI
- **RxMemberSim fills**: Dispensing pharmacy identifiers

See [examples/networksim-examples.md](examples/networksim-examples.md) for detailed examples.

---

## Hello, Analytics!

HealthSim data can be loaded directly into DuckDB for local analytics. Star schema format enables BI dashboards and SQL-based analysis.

### Local Analytics with DuckDB

Perfect for local development, testing, and demos. No additional setup required - DuckDB is bundled with healthsim-core.

**Simple tables:**

```
Generate 10 diabetic patients and load them into DuckDB
```

**Star schema for BI dashboards:**

```
Generate 10 patients in dimensional format for DuckDB with fact and dimension tables
```

This creates properly normalized analytics tables with:

- Dimension tables (dim_patient, dim_diagnosis, dim_medication, dim_date)
- Fact tables (fact_encounters, fact_lab_results)
- Pre-calculated metrics (age bands, LOS, readmission flags)

### Claims and Pharmacy Analytics

Same flexibility works for claims and pharmacy data:

```
Generate 20 members with claims in star schema format for DuckDB
```

```
Generate pharmacy data with prescription fills as a fact table for DuckDB
```

### Enterprise Analytics (Future)

Support for enterprise platforms (Databricks, Snowflake, MotherDuck) is planned for Phase 3. For now, export dimensional data from DuckDB and load to your enterprise platform using standard ETL tools.

See [../formats/dimensional-analytics.md](../formats/dimensional-analytics.md) for complete star schema definitions and sample queries.

---

## Hello, State Management!

Save your work, pick up where you left off, and explore "what-if" scenarios.

### Save Your Work

After generating data you want to keep:

```text
Save this as my-diabetes-cohort
```

HealthSim saves your entire workspace - all patients, clinical data, claims, and provenance information - to the DuckDB database at `~/.healthsim/healthsim.duckdb`.

### Load Later

Come back tomorrow (or next month) and restore exactly where you left off:

```text
Load my-diabetes-cohort
```

### See What You've Saved

```text
What scenarios do I have?
```

### Share Scenarios

Export a scenario as JSON to share with colleagues:

```text
Export my-diabetes-cohort for sharing
```

This creates `~/Downloads/my-diabetes-cohort.json` that others can import.

### Why Save Scenarios?

- **Session continuity** - Work on complex cohorts across multiple sessions
- **Reproducibility** - Save test baselines for regression testing
- **Sharing** - Export scenarios as portable JSON files to share with colleagues
- **Version control** - Save before making changes, compare versions

### "What-If" Branching

Build a patient, save a baseline, then explore different paths:

```text
Save this as patient-baseline
```

Now explore an acute complication:

```text
Generate a DKA hospitalization for this patient
Save this as patient-dka-path
```

Or go back and try a different trajectory:

```text
Load patient-baseline
Instead, add gradual progression over 6 months
Save this as patient-progression-path
```

Now you have three scenarios you can compare - perfect for testing how different clinical trajectories affect your systems.

---

## What's Included

```
healthsim-common/
├── SKILL.md                    # Master skill file (start here)
├── skills/
│   ├── patientsim/            # Clinical/EMR data generation
│   │   ├── diabetes-management.md
│   │   ├── heart-failure.md
│   │   └── ...
│   ├── membersim/             # Claims/payer data generation
│   │   ├── professional-claims.md
│   │   ├── facility-claims.md
│   │   └── ...
│   ├── rxmembersim/           # Pharmacy/PBM data generation
│   │   ├── retail-pharmacy.md
│   │   ├── dur-alerts.md
│   │   └── ...
│   └── trialsim/              # Clinical trials data generation
│       ├── phase1-dose-escalation.md
│       ├── phase3-pivotal.md
│       ├── domains/           # SDTM domains (DM, AE, LB, etc.)
│       └── therapeutic-areas/ # Oncology, CV, CNS, CGT
├── formats/                    # Output format transformations
│   ├── fhir-r4.md
│   ├── hl7v2-adt.md
│   ├── x12-837.md
│   ├── cdisc-sdtm.md          # CDISC SDTM for trials
│   ├── cdisc-adam.md          # CDISC ADaM for trials
│   ├── dimensional-analytics.md  # DuckDB star schemas (enterprise exports planned)
│   └── ...
├── references/                 # Code systems and rules
│   ├── data-models.md
│   ├── code-systems.md
│   └── ...
└── hello-healthsim/           # You are here!
```

---

## Next Steps

Once you're comfortable with basic generation:

### Learn More
- [SKILL.md](../SKILL.md) - Complete feature reference
- [examples/](examples/) - Detailed examples with outputs
- [docs/integration-guide.md](../docs/integration-guide.md) - Cross-skill data flows

### Extend HealthSim
- [EXTENDING.md](EXTENDING.md) - Add new scenarios, formats, and code systems

### Get Help
- [Troubleshooting](TROUBLESHOOTING.md) - Common issues and solutions
- [GitHub Issues](https://github.com/mark64oswald/healthsim-common/issues) - Report bugs or request features

---

## Quick Reference Card

### PatientSim (Clinical Data)

| Request | What You Get |
|---------|--------------|
| "diabetic patient" | Patient + diabetes diagnoses + meds + labs |
| "heart failure patient" | Patient + CHF + GDMT medications + BNP |
| "admission for pneumonia" | ADT event + encounter + orders |

### MemberSim (Claims Data)

| Request | What You Get |
|---------|--------------|
| "office visit claim" | 837P professional claim + adjudication |
| "inpatient claim" | 837I facility claim + DRG + payment |
| "denied claim" | Claim + denial reason + appeal info |

### RxMemberSim (Pharmacy Data)

| Request | What You Get |
|---------|--------------|
| "pharmacy claim for metformin" | NCPDP claim + pricing + copay |
| "drug interaction alert" | Claim + DUR response + clinical info |
| "specialty drug claim" | High-cost drug + prior auth + copay assistance |

### TrialSim (Clinical Trials)

| Request | What You Get |
|---------|--------------|
| "Phase 3 oncology trial" | Trial + sites + subjects + SDTM domains |
| "trial with 200 subjects" | Complete study with demographics + AEs |
| "breast cancer trial" | TA-specific protocol + efficacy endpoints |
| "SDTM for my trial" | CDISC-compliant domain datasets |

### Oncology (PatientSim)

| Request | What You Get |
|---------|--------------|
| "breast cancer patient" | Patient + staging + biomarkers + treatment plan |
| "lung cancer EGFR positive" | Patient + molecular testing + targeted therapy |
| "colon cancer MSI-high" | Patient + genomic testing + adjuvant chemo |
| "cancer with comorbidities" | Multi-morbid patient + dose adjustments |

### PopulationSim (Demographics & SDOH)

| Request | What You Get |
|---------|--------------|
| "county profile for Maricopa" | Demographics + health indicators + SDOH |
| "SVI analysis for rural Texas" | Social vulnerability by census tract |
| "define cohort for diabetes study" | CohortSpecification for generation |
| "trial feasibility for NASH" | Site recommendations + enrollment projection |

### NetworkSim (Provider Networks)

| Request | What You Get |
|---------|--------------|
| "find cardiologists in Houston" | Real NPIs from NPPES registry |
| "how many PCPs in San Diego County" | Provider distribution analysis |
| "generate a cardiologist" | Synthetic provider + NPI + credentials |
| "generate a hospital" | Facility + NPI + beds + services |
| "explain HMO vs PPO networks" | Network type comparison + trade-offs |

### Format Requests

| Add This | Output Format |
|----------|---------------|
| "as FHIR" | FHIR R4 Bundle |
| "as HL7" | HL7v2 message |
| "as 837" | X12 837 EDI |
| "as CSV" | CSV file format |
| "for DuckDB" | SQL for local analytics |
| "in star schema" | Dimensional fact/dimension tables |

### State Management

| Request | What You Get |
|---------|--------------|
| "save as my-cohort" | Scenario saved with all patients/data |
| "load my-cohort" | Restore previous workspace |
| "what scenarios do I have" | List saved scenarios |
| "delete old-scenario" | Remove a saved scenario |

---

## Success! What Now?

You've just unlocked the ability to generate realistic healthcare test data through conversation. Here are some ideas:

1. **Test Your APIs** - Generate FHIR resources to test your healthcare APIs
2. **Train ML Models** - Create diverse patient populations for training data
3. **Demo Your Product** - Generate realistic scenarios for product demos
4. **Load Test Systems** - Generate bulk data for performance testing
5. **Validate Workflows** - Test claims adjudication and pharmacy workflows

**Happy generating!**

---

## Disclaimer

HealthSim is a synthetic data generation framework designed exclusively for:

- Software development and testing
- System integration validation
- Training and educational demonstrations
- Performance and load testing
- Product demos and prototypes

**HealthSim is NOT intended for:**

- Clinical decision support
- Medical advice or diagnosis
- Treatment recommendations
- Actual patient care
- Processing or generating real PHI

The clinical patterns, medication regimens, diagnostic criteria, and lab values generated by HealthSim reflect general healthcare conventions and published guidelines. They are simplified representations suitable for test data and do not account for individual patient circumstances, contraindications, or the full complexity of clinical practice.

*Always consult qualified healthcare professionals for actual medical decisions.*
