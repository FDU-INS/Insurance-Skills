# HealthSim Workspace

**Synthetic healthcare data generation through natural language conversation.**

HealthSim generates realistic, clinically coherent healthcare data for testing, training, and development—from simple patient records to complete care journeys spanning clinical, claims, pharmacy, and clinical trial domains.

---

## Products Overview

| Product | What It Generates | Key Cohorts | Standards |
|---------|-------------------|---------------|-----------|
| **[PatientSim](skills/patientsim/README.md)** | Clinical/EMR data | Diabetes, heart failure, oncology, maternal, behavioral health | FHIR R4, HL7v2, C-CDA |
| **[MemberSim](skills/membersim/README.md)** | Claims/payer data | Professional claims, facility claims, prior auth, accumulators | X12 837/835/834 |
| **[RxMemberSim](skills/rxmembersim/README.md)** | Pharmacy/PBM data | Retail fills, specialty drugs, DUR alerts, manufacturer programs | NCPDP D.0 |
| **[TrialSim](skills/trialsim/README.md)** | Clinical trial data | Phase I-III, adverse events, efficacy endpoints, SDTM domains | CDISC SDTM/ADaM |
| **[PopulationSim](skills/populationsim/README.md)** | Demographics/SDOH | County profiles, health disparities, cohort specifications | Census, CDC PLACES |
| **[NetworkSim](skills/networksim/README.md)** | Provider networks | Providers (8.9M real NPIs), facilities, pharmacies | NPPES, NPI |

---

## Getting Started

New to HealthSim? Start here:

| Resource | Description |
|----------|-------------|
| **[Hello HealthSim](hello-healthsim/README.md)** | Quick start guide with setup instructions and first steps |
| **[Examples by Product](hello-healthsim/examples/)** | Detailed examples with expected outputs for each product |
| **[Extending HealthSim](hello-healthsim/EXTENDING.md)** | How to add new clinical cohorts, skills, and output formats |

The examples folder contains ready-to-use prompts organized by product:
- [PatientSim Examples](hello-healthsim/examples/patientsim-examples.md) - Clinical data generation
- [MemberSim Examples](hello-healthsim/examples/membersim-examples.md) - Claims and payer data
- [RxMemberSim Examples](hello-healthsim/examples/rxmembersim-examples.md) - Pharmacy data
- [TrialSim Examples](hello-healthsim/examples/trialsim-examples.md) - Clinical trial data
- [PopulationSim Examples](hello-healthsim/examples/populationsim-examples.md) - Demographics and SDOH
- [NetworkSim Examples](hello-healthsim/examples/networksim-examples.md) - Provider networks

---

## Deployment Modes

HealthSim runs in two modes from the same codebase:

| Mode | Infrastructure | Data | Best For |
|------|---------------|------|----------|
| **Local (Claude Code)** | stdio MCP, local DuckDB | Local `.duckdb` file | Development, testing, skill editing |
| **Managed Agent (Cloud)** | Railway MCP (HTTP), MotherDuck | Cloud-hosted | Hosted access via Console, CLI, or web app |

**Local mode** is the development environment. You edit skills, test MCP tools, run generation workflows, and iterate. Everything runs on your machine.

**Managed Agent mode** is the deployment target. The same skills, MCP server code, and Python modules run on Anthropic's infrastructure (agent runtime), Railway (MCP server), and MotherDuck (data). Users access it through the Anthropic Console UI, a CLI tool, or the Rewire web application.

The two modes coexist — deploying to Managed Agent does not affect your local Claude Code workflow. See the [Managed Agent Guide](docs/MANAGED-AGENT-GUIDE.md) for full deployment instructions.

---

## Generative Framework

For large-scale data generation, HealthSim provides a **specification-driven framework** that separates what you want from how it's generated:

| Component | Purpose | Example |
|-----------|---------|---------|
| **Profile Builder** | Define population characteristics | "200 Medicare diabetics age 65-85 in Texas" |
| **Journey Builder** | Define event sequences over time | "First year diabetes journey with quarterly visits" |
| **Templates** | Pre-built common cohorts | Medicare Diabetic, Surgical Episode, New Member Onboarding |
| **Executors** | Generate data from specifications | Deterministic, reproducible output |

### Quick Examples

**Profile-Driven Generation:**
```
Build a profile for 100 commercial members:
- Age 25-45
- Mix of healthy and chronic conditions
- Urban geography

Execute the profile
```

**Template + Journey:**
```
Use the Medicare diabetic template with the diabetic first-year journey for 50 patients
```

### Resources

| Resource | Description |
|----------|-------------|
| [Generation Examples](hello-healthsim/examples/generation-examples.md) | 9 comprehensive usage examples |
| [Profile Templates](skills/generation/templates/profiles/) | Pre-built population profiles |
| [Journey Templates](skills/generation/templates/journeys/) | Pre-built care pathways |
| [Generative Framework Skills](skills/generation/) | Full skill documentation |

---

## Cross-Product Integration

HealthSim products work together to generate complete healthcare data journeys:

```
Person (Base Identity - SSN as universal correlator)
   │
   ├── PatientSim → Patient → Clinical encounters, labs, meds
   │        ↓
   ├── MemberSim → Member → Claims, adjudication, accumulators  
   │        ↓
   ├── RxMemberSim → RxMember → Pharmacy claims, DUR, formulary
   │
   └── TrialSim → Subject → Protocol visits, AEs, efficacy (if enrolled)

   NetworkSim provides: Providers, facilities, pharmacies for all products
   PopulationSim provides: Demographics, health rates, SDOH for all products
```

**Example: Heart Failure Patient Journey**

| Day | Product | Event | Output |
|-----|---------|-------|--------|
| 0 | PatientSim | ED visit, HF diagnosis | Encounter, labs, meds |
| 3 | PatientSim | Inpatient discharge | Discharge summary |
| 5 | MemberSim | Facility claim | 837I (DRG 291) |
| 3 | RxMemberSim | Discharge Rx fills | NCPDP claims |
| 30 | PatientSim | Cardiology follow-up | Office encounter |
| 32 | MemberSim | Professional claim | 837P (99214) |

See [Architecture Guide - Cross-Product Integration](docs/HEALTHSIM-ARCHITECTURE-GUIDE.md#3-product-relationships) for detailed diagrams and patterns.

---

## Output Formats

| Format | Request With | Use Case | Products |
|--------|--------------|----------|----------|
| JSON | (default) | API testing | All |
| FHIR R4 | "as FHIR" | Interoperability | PatientSim |
| C-CDA | "as C-CDA" | Clinical documents | PatientSim |
| HL7v2 | "as HL7", "as ADT" | Legacy EMR | PatientSim |
| X12 837/835 | "as 837", "as X12" | Claims | MemberSim |
| X12 834 | "as 834" | Enrollment | MemberSim |
| NCPDP D.0 | "as NCPDP" | Pharmacy | RxMemberSim |
| CDISC SDTM | "as SDTM" | Trial submission | TrialSim |
| CDISC ADaM | "as ADaM" | Trial analysis | TrialSim |
| Star Schema | "as star schema" | BI analytics | All |
| CSV | "as CSV" | Spreadsheets | All |

See [formats/](formats/) for transformation specifications.

---

## State Management

HealthSim persists your generated data to DuckDB, allowing you to build cohorts over multiple sessions and query them without regenerating.

### Two Approaches: Full Data vs. Auto-Persist

**Full Data** is best when you have a small cohort (under 50 entities) and want everything loaded at once. Claude sees all the data in context and can reference it directly.

**Auto-Persist** is best when you're generating larger datasets (50+ entities). Instead of flooding the conversation with hundreds of JSON objects, HealthSim saves them quietly and gives you a compact summary. When you need specific data, you query for just what you need.

| Approach | Best For | What Happens |
|----------|----------|---------------|
| **Full Data** | Small cohorts, interactive exploration | All entities loaded into conversation |
| **Auto-Persist** | Large batches, production datasets | Summary in conversation, data in database |

### Conversation Examples

**Full Data Approach** (small cohorts):

```
You: Generate 5 diabetes patients for my demo

Claude: [Generates patients with full details]

Here are 5 diabetes patients:
1. Maria Santos, 58F, Type 2 DM, A1C 7.8%, on Metformin...
2. James Wilson, 67M, Type 2 DM with CKD...
[full details for all 5]

You: Save these as "demo-cohort"

Claude: Saved "demo-cohort" with 5 patients.

You: Load my demo cohort

Claude: [Full patient data appears in conversation]
```

**Auto-Persist Approach** (large cohorts):

```
You: Generate 200 Medicare members over 65

Claude: Generated and saved "medicare-members-20241228":
- 200 members persisted
- Age range: 65-89
- Gender: 48% male, 52% female
- Top states: CA, TX, FL

[Data is in database, not flooding the conversation]

You: Show me members from California

Claude: Found 42 California members:

| Name | Age | County | Risk Score |
|------|-----|--------|------------|
| Margaret Chen | 72 | Los Angeles | 1.85 |
| Robert Williams | 68 | San Diego | 1.12 |
...
Showing 20 of 42. Say "show more" for next page.

You: How many have diabetes?

Claude: [Queries database]
67 members (34%) have a diabetes diagnosis.
```

### Benefits

- **Session continuity** - Save work at end of day, resume tomorrow
- **Cohort library** - Build reusable cohorts for demos and testing
- **Context efficiency** - Generate thousands of entities without context overflow
- **Targeted queries** - Find exactly what you need without loading everything

### Under the Hood

State management uses the `healthsim-mcp` server which provides tools for saving, loading, querying, and managing cohorts in DuckDB. You don't need to know the tool names—just ask Claude naturally to save, load, or query your data.

See [State Management Skill](skills/common/state-management.md) | [Auto-Persist Examples](hello-healthsim/examples/auto-persist-examples.md) | [Data Architecture](docs/data-architecture.md)

---

## Clinical Cohorts

### PatientSim Cohorts

| Domain | Skill | Key Use Cases |
|--------|-------|---------------|
| Diabetes | [diabetes-management.md](skills/patientsim/diabetes-management.md) | Type 1/2, A1C, insulin, complications |
| Heart Failure | [heart-failure.md](skills/patientsim/heart-failure.md) | HFrEF/HFpEF, NYHA, GDMT |
| CKD | [chronic-kidney-disease.md](skills/patientsim/chronic-kidney-disease.md) | Stages 1-5, dialysis |
| Oncology | [oncology/](skills/patientsim/oncology/) | Breast, lung, colorectal cancer |
| Maternal | [maternal-health.md](skills/patientsim/maternal-health.md) | Prenatal, GDM, preeclampsia |
| Behavioral | [behavioral-health.md](skills/patientsim/behavioral-health.md) | Depression, anxiety, SUD |
| Acute Care | [sepsis-acute-care.md](skills/patientsim/sepsis-acute-care.md) | Sepsis, ICU |
| Pediatrics | [pediatrics/](skills/patientsim/pediatrics/) | Asthma, otitis media |

### TrialSim Cohorts

| Domain | Skill | Key Use Cases |
|--------|-------|---------------|
| Phase 1 | [phase1-dose-escalation.md](skills/trialsim/phase1-dose-escalation.md) | FIH, 3+3, BOIN, MTD |
| Phase 2 | [phase2-proof-of-concept.md](skills/trialsim/phase2-proof-of-concept.md) | Simon's, futility |
| Phase 3 | [phase3-pivotal.md](skills/trialsim/phase3-pivotal.md) | Registration trials |
| SDTM Domains | [domains/](skills/trialsim/domains/) | DM, AE, VS, LB, CM, EX, DS |
| Therapeutic | [therapeutic-areas/](skills/trialsim/therapeutic-areas/) | Oncology, CV, CNS, CGT |

---

## Repository Structure

```
healthsim-workspace/
├── SKILL.md                    # Master skill file (Claude entry point)
├── README.md                   # This file
├── agent-config.yaml           # Managed Agent deployment manifest
├── healthsim.duckdb            # Unified database (~1.7 GB via Git LFS)
├── .env                        # API keys and tokens (gitignored)
│
├── hello-healthsim/            # Getting started (tutorials, setup)
│   ├── README.md              # Quick start guide
│   └── examples/              # Detailed examples by product
│
├── skills/                     # Product skills (domain knowledge)
│   ├── patientsim/            # Clinical/EMR (12 cohorts)
│   ├── membersim/             # Claims/payer (8 cohorts)
│   ├── rxmembersim/           # Pharmacy/PBM (8 cohorts)
│   ├── trialsim/              # Clinical trials (20+ skills)
│   ├── populationsim/         # Demographics/SDOH + embedded data
│   └── networksim/            # Provider networks (8.9M real providers)
│
├── formats/                    # Output transformations (12 formats)
├── references/                 # Shared terminology, code systems
├── docs/                       # Architecture, guides, processes
│   └── MANAGED-AGENT-GUIDE.md # Managed Agent operations guide
├── packages/                   # Python infrastructure
│   ├── core/                  # Shared healthsim-core library
│   ├── mcp-server/            # FastMCP server (stdio + HTTP transport)
│   ├── patientsim/            # PatientSim package
│   ├── membersim/             # MemberSim package
│   └── rxmembersim/           # RxMemberSim package
├── deploy/                     # Managed Agent deploy scripts
│   ├── push-skills.py         # Upload skills to Anthropic Skills API
│   ├── push-agent.py          # Create/update agent definition
│   ├── push-environment.py    # Create/update container environment
│   ├── start-session.py       # Interactive CLI for Managed Agent
│   └── run.sh                 # Convenience wrapper
├── build-prompts/              # Migration execution prompts (Phases 0-3)
└── scripts/                    # Utility and migration scripts
```

---

## Setup

**📖 [Complete Installation Guide](INSTALL.md)** - Detailed instructions for Git LFS, Python, DuckDB, and Claude integration.

### Quick Setup

| Requirement | Version | Notes |
|-------------|---------|-------|
| **Git LFS** | 3.0+ | **Required** for database files |
| Git | 2.0+ | Clone repository |
| Python | 3.10+ | For healthsim-core package |
| Claude Desktop or Claude Code | Latest | AI conversation interface |

### Git LFS (Required)

HealthSim uses Git Large File Storage for the database. Install before cloning:

```bash
# macOS
brew install git-lfs && git lfs install

# Linux (Ubuntu/Debian)
sudo apt-get install git-lfs && git lfs install

# See INSTALL.md for Windows and troubleshooting
```

### Python Environment

```bash
# Clone and setup (Git LFS downloads database automatically)
git clone https://github.com/mark64oswald/healthsim-workspace.git
cd healthsim-workspace

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install healthsim-core (includes DuckDB)
cd packages/core
pip install -e .
```

**DuckDB** is bundled with healthsim-core - no separate installation required. The database (`healthsim.duckdb`, ~1.7 GB) is automatically downloaded via Git LFS and ready to use.

**Important:** If the database file is missing or tiny (~500 bytes), Git LFS didn't download it. Run `git lfs pull` to download manually. See [INSTALL.md](INSTALL.md) for details.

### Claude Desktop (Recommended)

Add to a Claude Project or configure as MCP server:

```json
{
  "mcpServers": {
    "healthsim": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/healthsim-workspace"]
    }
  }
}
```

### Claude Code

```bash
cd healthsim-workspace
claude
```

See [hello-healthsim/](hello-healthsim/) for detailed setup instructions.

### Managed Agent Deployment

To deploy HealthSim as a cloud-hosted Managed Agent (accessible via Console UI, CLI, or web app), see the [Managed Agent Guide](docs/MANAGED-AGENT-GUIDE.md). This requires accounts on Railway, MotherDuck, and Anthropic Platform.

---

## Use Cases

| Use Case | Description |
|----------|-------------|
| **API Testing** | Generate FHIR resources, X12 transactions, NCPDP claims |
| **Training Data** | Create diverse patient populations for ML models |
| **Product Demos** | Generate realistic cohorts for demonstrations |
| **Load Testing** | Bulk data generation for performance testing |
| **Workflow Validation** | Test claims processing, pharmacy adjudication |
| **Education** | Learn healthcare data structures and relationships |
| **Trial Planning** | Feasibility analysis, site selection, diversity planning |

---

## Documentation

| Topic | Location |
|-------|----------|
| Quick Start | [hello-healthsim/](hello-healthsim/README.md) |
| Master Skill Reference | [SKILL.md](SKILL.md) |
| Architecture Guide | [docs/HEALTHSIM-ARCHITECTURE-GUIDE.md](docs/HEALTHSIM-ARCHITECTURE-GUIDE.md) |
| Managed Agent Guide | [docs/MANAGED-AGENT-GUIDE.md](docs/MANAGED-AGENT-GUIDE.md) |
| Deploy Scripts | [deploy/README.md](deploy/README.md) |
| Data Architecture | [docs/data-architecture.md](docs/data-architecture.md) |
| State Management | [skills/common/state-management.md](skills/common/state-management.md) |
| Extension Guide | [hello-healthsim/EXTENDING.md](hello-healthsim/EXTENDING.md) |
| Contributing | [docs/contributing.md](docs/contributing.md) |

---

## Key Features

- **Clinical Coherence**: Age/gender-appropriate conditions, medications match diagnoses, labs correlate with disease state
- **Proper Healthcare Codes**: ICD-10, CPT, LOINC, NDC, RxNorm, MedDRA, taxonomy codes
- **Realistic Business Logic**: Claims adjudication, accumulators, prior auth, DUR alerts, formulary tiers
- **Data-Driven Generation**: Ground synthetic data in real CDC/Census population statistics (via PopulationSim)
- **Real Provider Data**: Query 8.9 million real healthcare providers from NPPES (via NetworkSim)
- **Multiple Output Formats**: FHIR, HL7v2, C-CDA, X12, NCPDP, CDISC SDTM/ADaM

---

## Links

- [Getting Started](hello-healthsim/README.md)
- [Full Reference (SKILL.md)](SKILL.md)
- [HL7 FHIR R4](https://hl7.org/fhir/R4/)
- [X12 Standards](https://x12.org/)
- [NCPDP Standards](https://www.ncpdp.org/)
- [CDISC Standards](https://www.cdisc.org/)

---

*HealthSim generates synthetic test data only. Never use for actual patient care or real PHI.*
