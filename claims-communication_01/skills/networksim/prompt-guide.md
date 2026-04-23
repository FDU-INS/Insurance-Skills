---
name: networksim-prompt-guide
description: |
  Example prompts for using NetworkSim skills effectively. Templates for
  network reference, provider generation, facility generation, pharmacy
  generation, and cross-product integration cohorts.
---

# NetworkSim Prompt Guide

## Overview

This guide provides example prompts for using NetworkSim skills effectively. Use these templates as starting points for network reference queries and synthetic entity generation.

**Organization**:
1. Reference Knowledge Prompts - Learn concepts
2. Synthetic Generation Prompts - Create entities
3. Cross-Product Integration Prompts - Enhance other products
4. Advanced Prompts - Complex cohorts

---

## Reference Knowledge Prompts

### Network Type Explanations

```
Explain the difference between HMO and PPO networks
```
**Expected**: Comprehensive comparison table with cost/flexibility tradeoffs

```
What are the key characteristics of an EPO plan?
```
**Expected**: EPO definition, how it differs from HMO and PPO, when to use

```
When would a patient choose a POS plan over an HMO?
```
**Expected**: POS advantages, point-of-service decision explanation, cost implications

```
Explain HDHP plans and HSA eligibility requirements
```
**Expected**: HDHP thresholds, HSA rules, triple tax advantage, contribution limits

```
Compare all five major network types in a table
```
**Expected**: HMO, PPO, EPO, POS, HDHP comparison across key dimensions

```
What is a narrow network and why do they exist?
```
**Expected**: Narrow/tiered network concept, cost savings, access tradeoffs

---

### Plan Structure Concepts

```
What components make up a typical health plan benefit structure?
```
**Expected**: Deductibles, copays, coinsurance, OOP max explanation with examples

```
Explain the difference between in-network and out-of-network benefits
```
**Expected**: Cost sharing differences, balance billing, UCR, member responsibility

```
How do tiered networks work?
```
**Expected**: Tier structure, cost incentives, high-performance network concept

```
What's the difference between a copay and coinsurance?
```
**Expected**: Fixed vs percentage cost sharing, when each applies, examples

```
Explain how deductibles and out-of-pocket maximums work together
```
**Expected**: Accumulator relationship, family vs individual, embedded vs aggregate

```
What are the ACA metal tiers (Bronze, Silver, Gold, Platinum)?
```
**Expected**: Actuarial value explanation, cost sharing patterns by tier

---

### Pharmacy Benefit Concepts

```
Explain pharmacy benefit tier structures
```
**Expected**: 4-5 tier explanation, cost sharing by tier, typical drugs in each

```
What's the difference between open and closed formularies?
```
**Expected**: Formulary types, coverage implications, exception processes

```
How do preferred pharmacy networks work?
```
**Expected**: Preferred vs non-preferred, cost incentives, 90-day retail

```
Explain specialty pharmacy vs retail pharmacy
```
**Expected**: Specialty characteristics, limited distribution, hub model, services

```
What is a formulary and how is it developed?
```
**Expected**: P&T committee, clinical criteria, tier placement, rebate considerations

```
Explain pharmacy accumulators vs copay assistance
```
**Expected**: Manufacturer copay cards, accumulator programs, affordability

---

### PBM Operations

```
How does a PBM process pharmacy claims?
```
**Expected**: Claim flow, BIN/PCN routing, real-time adjudication steps

```
What's the relationship between a health plan and PBM?
```
**Expected**: Carve-out vs carve-in, PBM services, contract types

```
Explain the formulary management process
```
**Expected**: P&T committee, clinical review, tier placement, rebate negotiation

```
What is BIN and PCN in pharmacy claims?
```
**Expected**: Bank Identification Number, Processor Control Number, routing

```
How do pharmacy rebates work?
```
**Expected**: Manufacturer rebates, PBM role, pass-through vs spread

```
Explain mail order pharmacy benefits
```
**Expected**: 90-day supply, cost savings, mandatory vs optional mail

---

### Utilization Management

```
What is prior authorization and when is it required?
```
**Expected**: PA process, common PA drugs, approval criteria, turnaround times

```
Explain step therapy requirements
```
**Expected**: Step therapy concept, first-line/second-line, fail-first, exceptions

```
How do quantity limits work?
```
**Expected**: QL types (safety, cost), days supply, dose limits, override process

```
What is a formulary exception and how does it work?
```
**Expected**: Exception types, medical necessity, appeal process

```
Explain prior authorization for specialty drugs
```
**Expected**: Clinical criteria, diagnosis requirements, lab requirements

---

### Specialty Pharmacy Concepts

```
What makes a drug a specialty medication?
```
**Expected**: Cost threshold, complexity, distribution, patient support needs

```
Explain the specialty pharmacy hub model
```
**Expected**: Hub services, patient coordination, benefits investigation

```
What are REMS programs and how do they affect pharmacy?
```
**Expected**: Risk Evaluation and Mitigation Strategies, certification, dispensing

```
How does limited distribution work for specialty drugs?
```
**Expected**: Manufacturer control, exclusive networks, access implications

```
What services do specialty pharmacies provide beyond dispensing?
```
**Expected**: Care coordination, adherence programs, side effect management

---

### Network Adequacy

```
What is network adequacy and why does it matter?
```
**Expected**: Access standards, regulatory requirements, member impact

```
Explain time and distance standards for network adequacy
```
**Expected**: Urban/suburban/rural standards, specialty-specific, state variations

```
What are provider-to-member ratios?
```
**Expected**: PCP ratio, specialist ratio, calculation, adequacy thresholds

```
What are essential community providers?
```
**Expected**: FQHC, safety net, ACA requirements, network inclusion

---

## Synthetic Generation Prompts

### Provider Generation

**Basic Generation**:
```
Generate a primary care physician in Chicago
```
**Expected**: Individual provider with Internal Medicine or Family Medicine taxonomy, Chicago address

```
Generate a family medicine doctor in suburban Atlanta
```
**Expected**: Family Medicine (207Q00000X), Fulton/Cobb/DeKalb county address

```
Generate a pediatrician in Miami-Dade County, Florida
```
**Expected**: Pediatrics (208000000X), Florida license, Miami area address

**Specialty Specific**:
```
Generate an interventional cardiologist in Houston, Texas
```
**Expected**: Interventional Cardiology (207RC0001X), FSCAI credential, Houston Methodist affiliation

```
Generate a board-certified orthopedic surgeon specializing in sports medicine
```
**Expected**: Sports Medicine (207XS0117X), FAOASM credential

```
Generate a pediatric hematologist-oncologist in Boston
```
**Expected**: Pediatric Hematology/Oncology (207RP0230X), children's hospital affiliation

```
Generate a maternal-fetal medicine specialist in Los Angeles
```
**Expected**: Maternal-Fetal Medicine (207VX0201X), MFM fellowship credentials

```
Generate a geriatric psychiatrist in Phoenix, Arizona
```
**Expected**: Geriatric Psychiatry (2084P0005X), geriatric certification

**With Full Credentials**:
```
Generate a board-certified endocrinologist with full credentials and hospital privileges
```
**Expected**: Complete provider with FACE credential, ABIM certification, hospital affiliations

```
Generate a nurse practitioner with prescriptive authority in Texas
```
**Expected**: NP (363L00000X), Texas license, collaborative agreement, DEA number

```
Generate a physician assistant in orthopedic surgery
```
**Expected**: PA-C (363A00000X), orthopedic specialty, supervising physician

**Organization Provider**:
```
Generate a multi-specialty physician group practice in Phoenix
```
**Expected**: Organization NPI, multiple taxonomy codes, group practice structure

```
Generate a cardiology practice with 5 physicians in Dallas
```
**Expected**: Group practice with 5 individual providers, shared address, call coverage

```
Generate a hospitalist group for a 400-bed hospital
```
**Expected**: Hospitalist group (207RH0002X), appropriate staffing ratio

**Advanced Provider Cohorts**:
```
Generate a telemedicine provider licensed in multiple states
```
**Expected**: Multiple state licenses, telehealth taxonomy modifier

```
Generate a locum tenens physician for emergency medicine
```
**Expected**: EM physician with temporary practice indication

```
Generate a rural health clinic physician with loan repayment
```
**Expected**: PCP in HPSA area, NHSC eligible

---

### Facility Generation

**Basic Hospital**:
```
Generate a 200-bed community hospital in suburban Dallas
```
**Expected**: Short-term acute care, 200 beds, Dallas suburb location, basic services

```
Generate a critical access hospital in rural Montana
```
**Expected**: CAH designation (XX1300s CCN), 25 beds max, rural location

```
Generate a children's hospital in Philadelphia
```
**Expected**: Children's hospital CCN (XX3300s), pediatric services, CHOP-like

**Specialty Facility**:
```
Generate an ambulatory surgery center specializing in orthopedics
```
**Expected**: ASC (XX5500s CCN), orthopedic procedures, outpatient only

```
Generate a cardiac specialty hospital in Houston
```
**Expected**: Specialty hospital, cardiac surgery, cath lab, no general services

```
Generate a long-term acute care hospital in Chicago
```
**Expected**: LTACH (XX2000s CCN), >25 day average LOS, complex patients

```
Generate an inpatient rehabilitation facility specializing in stroke
```
**Expected**: IRF (XX3025s CCN), stroke rehab, 60% rule compliance

**Academic Medical Center**:
```
Generate a Level 1 trauma center affiliated with a medical school
```
**Expected**: Teaching hospital, residency programs, Level 1 trauma, research

```
Generate an NCI-designated comprehensive cancer center
```
**Expected**: Academic medical center, NCI designation, clinical trials

**Post-Acute Facilities**:
```
Generate a 120-bed skilled nursing facility in suburban Chicago
```
**Expected**: SNF (XX5000s CCN), Medicare-certified, rehab services

```
Generate a home health agency serving rural Texas counties
```
**Expected**: HHA (XX7000s CCN), rural service area, skilled nursing

```
Generate a hospice serving the Denver metropolitan area
```
**Expected**: Hospice (XX1500s CCN), home and inpatient services

**Specialty Care Facilities**:
```
Generate a freestanding dialysis center
```
**Expected**: ESRD facility (XX2300s CCN), hemodialysis stations

```
Generate a federally qualified health center in an underserved area
```
**Expected**: FQHC, sliding scale, HRSA designation

```
Generate a psychiatric hospital for adolescents
```
**Expected**: Psychiatric hospital (XX4000s CCN), adolescent unit

---

### Pharmacy Generation

**Retail Pharmacy**:
```
Generate a CVS pharmacy in San Diego
```
**Expected**: Chain retail, CVS branding, San Diego address, standard services

```
Generate an independent community pharmacy in a small town
```
**Expected**: Independent, non-chain, personalized services, compounding

```
Generate a Walgreens pharmacy with 24-hour service
```
**Expected**: Walgreens chain, 24-hour operation, drive-through

**Specialty Pharmacy**:
```
Generate a specialty pharmacy for oncology medications
```
**Expected**: Specialty pharmacy type, oncology focus, clinical services, cold chain

```
Generate a specialty pharmacy certified for REMS drugs
```
**Expected**: REMS certification, enhanced distribution, patient registry

```
Generate a specialty pharmacy for transplant medications
```
**Expected**: Transplant focus, immunosuppressant expertise, adherence programs

```
Generate a specialty pharmacy with home infusion capabilities
```
**Expected**: Home infusion services, IV therapy, nursing coordination

**Mail Order**:
```
Generate a mail order pharmacy operation
```
**Expected**: Mail order type, high volume, automated dispensing

```
Generate a 90-day supply mail pharmacy with specialty capabilities
```
**Expected**: Combined mail/specialty, maintenance and specialty drugs

**Specialty Services**:
```
Generate a compounding pharmacy for hormone therapy
```
**Expected**: Compounding capability, BHRT focus, PCAB accreditation

```
Generate a nuclear pharmacy serving a metropolitan area
```
**Expected**: Nuclear pharmacy type (06), radiopharmaceuticals, expedited delivery

```
Generate a long-term care pharmacy serving nursing facilities
```
**Expected**: LTC pharmacy (04), unit-dose, consultant pharmacist

---

### Network Configuration

**HMO Network**:
```
Generate an HMO network configuration for a regional health plan in California
```
**Expected**: Closed network, PCP gatekeeper, capitation structure, CA geography

```
Generate a staff model HMO network like Kaiser
```
**Expected**: Employed physicians, owned facilities, integrated delivery

```
Generate an IPA-model HMO for South Florida
```
**Expected**: IPA contracting, delegated credentialing, risk sharing

**PPO Network**:
```
Generate a broad PPO network covering the Texas Triangle
```
**Expected**: Houston/Dallas/Austin/San Antonio coverage, broad access

```
Generate a national PPO network with BlueCard access
```
**Expected**: Multi-state network, BlueCard reciprocity

**Tiered Network**:
```
Generate a quality-based tiered network with 3 tiers
```
**Expected**: Blue/White/Gray tiers, quality metrics, cost differential

```
Generate a narrow network for an ACA exchange plan
```
**Expected**: Essential community providers, adequacy compliance, lower cost

---

## Cross-Product Integration Prompts

### PatientSim Integration

**Provider for Encounter**:
```
Generate a provider for this heart failure patient's cardiology referral
[Include: Patient with I50.9 in Houston, TX]
```
**Expected**: Cardiologist matched to diagnosis, Houston location, referral context

```
Generate an attending physician for this emergency department encounter
[Include: Patient with chest pain, R07.9, arrived by ambulance]
```
**Expected**: ED physician (207PE0004X), emergency medicine credentials

```
Generate a surgeon for this patient's scheduled knee replacement
[Include: Patient with M17.11, scheduled for CPT 27447]
```
**Expected**: Orthopedic surgeon specializing in adult reconstruction

```
Generate consulting physicians for this complex ICU patient
[Include: Patient with sepsis, ARDS, AKI requiring multi-specialty care]
```
**Expected**: Pulmonology, nephrology, infectious disease consultants

**Facility for Encounter**:
```
Generate a hospital for this patient's elective surgery
[Include: Patient in Phoenix needing total hip replacement]
```
**Expected**: Phoenix area hospital with orthopedic surgery capability

```
Generate an appropriate facility for this psychiatric admission
[Include: Adolescent patient with acute psychosis]
```
**Expected**: Psychiatric facility with adolescent unit

---

### MemberSim Integration

**Network Status**:
```
Is this provider in-network for this member's PPO plan?
[Include: Provider NPI, Member plan ID, Service date]
```
**Expected**: Network status, tier if applicable, contracted rate

```
Determine the network tier for this specialist visit
[Include: Tiered network plan, Specialist NPI, Service]
```
**Expected**: Tier assignment, tier-based cost sharing

```
What is the cost sharing for this out-of-network service?
[Include: PPO member, OON provider, Service code]
```
**Expected**: OON deductible, coinsurance, UCR calculation, balance billing

**Benefit Application**:
```
Calculate the member cost sharing for this ER visit
[Include: Member accumulators, Facility copay, Service details]
```
**Expected**: Copay, deductible applied, coinsurance, new accumulator values

```
Apply the plan benefits to this inpatient admission claim
[Include: Member plan, Allowed amount, LOS, Accumulators]
```
**Expected**: Complete adjudication with facility copay, coinsurance, OOP cap

---

### RxMemberSim Integration

**Pharmacy Routing**:
```
What pharmacy type should dispense this Humira prescription?
[Include: Humira 40mg, Member benefit, Days supply]
```
**Expected**: Specialty pharmacy routing, clinical services, cost sharing

```
Route this maintenance statin to the appropriate pharmacy
[Include: Atorvastatin 90-day, Member enrolled in mail]
```
**Expected**: Mail order routing, 90-day supply, mail copay

```
Generate a dispensing pharmacy for this oncology injectable
[Include: Keytruda, Oncology patient, Specialty benefit]
```
**Expected**: Specialty pharmacy with oncology expertise, white bagging option

**Formulary Coverage**:
```
Is this drug covered on the member's formulary?
[Include: Drug NDC, Formulary ID, Member plan]
```
**Expected**: Formulary status, tier, cost sharing, any restrictions

```
What prior authorization is required for this biologic?
[Include: Enbrel, RA diagnosis, Member plan]
```
**Expected**: PA criteria, required documentation, approval timeline

```
Apply step therapy to this SSRI prescription
[Include: Lexapro, Depression diagnosis, Claims history]
```
**Expected**: Step therapy status, required first-line trials, override criteria

---

### TrialSim Integration

**Site Generation**:
```
Generate a trial site facility for this Phase 3 oncology study
[Include: NSCLC study, 50 patients needed, Southwest region]
```
**Expected**: Academic cancer center, oncology expertise, research infrastructure

```
Generate 5 diverse trial sites for this cardiovascular outcomes trial
[Include: Phase 3, 10,000 patients, nationwide]
```
**Expected**: Mix of academic/community, geographic diversity, cardiology expertise

**Investigator Generation**:
```
Generate a principal investigator for this cardiology trial
[Include: Phase 2 heart failure study, Academic site]
```
**Expected**: Heart failure specialist, research credentials, academic affiliation

```
Generate sub-investigators for this multi-site oncology trial
[Include: Community oncology site, Phase 3]
```
**Expected**: Medical oncologists, GCP certified, site staff

---

### PopulationSim Integration

**Geographic Distribution**:
```
Generate providers distributed across Harris County proportional to population
[Include: PCP and specialist needs, Population data]
```
**Expected**: Provider distribution matching population density, specialty mix

```
Identify network adequacy gaps in this rural county
[Include: County FIPS, Network roster, Adequacy standards]
```
**Expected**: Gap analysis by specialty, travel time issues, solutions

**SDOH Context**:
```
Generate a network appropriate for this high-SVI community
[Include: SVI data, Community demographics]
```
**Expected**: FQHCs, safety net providers, language access

---

## Advanced Prompts

### Multi-Entity Generation

```
Generate a complete cardiology practice with 5 physicians and affiliated hospital
```
**Expected**: 5 cardiologists with varied subspecialties, group NPI, hospital affiliation, shared resources

```
Generate an integrated delivery system with hospital, physician groups, and post-acute
```
**Expected**: Health system with hospital, employed physicians, SNF, home health, shared branding

```
Generate a PBM network with mail pharmacy, specialty pharmacy, and preferred retail
```
**Expected**: Complete pharmacy network with routing rules, tier assignments, clinical programs

### Network Adequacy Analysis

```
Analyze this network for adequacy in Maricopa County, Arizona
[Include: Provider roster, Member distribution]
```
**Expected**: Time/distance analysis, ratio calculations, gap identification, remediation

```
Identify essential community provider gaps in this network
[Include: Network roster, FQHC locations, ACA requirements]
```
**Expected**: ECP percentage, missing providers, compliance status

### Complex Cohorts

```
Generate a specialty pharmacy network for a PBM covering all 50 states
```
**Expected**: National specialty network, geographic coverage, therapeutic expertise distribution

```
Design a tiered network with Centers of Excellence for transplant
```
**Expected**: Quality tiers plus COE designation, transplant centers, routing rules

```
Generate a Medicare Advantage network meeting CMS adequacy requirements
```
**Expected**: MA-compliant network, time/distance by specialty, H&P requirements

---

## Tips for Effective Prompts

### Be Specific About Geography

✅ Good:
```
Generate a cardiologist in Harris County, Texas
```

❌ Avoid:
```
Generate a doctor in Texas
```

**Why**: Specific geography produces realistic addresses, phone numbers, hospital affiliations, and correct county FIPS codes.

---

### Specify Specialty When Relevant

✅ Good:
```
Generate an interventional cardiologist
```

❌ Avoid:
```
Generate a heart doctor
```

**Why**: Specific specialties map to correct taxonomy codes (207RC0001X vs 207RC0000X) and realistic credentials (FSCAI).

---

### Include Context for Integration

✅ Good:
```
Generate a provider for this heart failure patient's cardiology referral
[Include patient context: diagnosis, location]
```

❌ Avoid:
```
Generate a provider
```

**Why**: Context enables matching specialty to diagnosis, geography to patient location, and appropriate credentials for the care setting.

---

### Request Specific Output When Needed

✅ Good:
```
Generate a provider with full taxonomy codes and board certifications
```

❌ Avoid:
```
Generate a provider
```

**Why**: Default output may omit optional fields like secondary taxonomies, hospital privileges, or board certification details.

---

### Use Multiple Prompts for Complex Needs

✅ Good:
```
1. "Explain specialty pharmacy concepts"
2. "Generate a specialty pharmacy for oncology"
3. "Add this pharmacy to the member's network"
```

❌ Avoid:
```
Do everything related to specialty pharmacy
```

**Why**: Breaking into steps produces more accurate, complete results and allows for verification at each stage.

---

### Reference Existing Entities

✅ Good:
```
Generate 3 more cardiologists affiliated with the same hospital
[Reference: CCN 450358 - Houston Methodist]
```

❌ Avoid:
```
Generate more doctors
```

**Why**: Maintaining entity references ensures consistency across related providers.

---

### Specify Network Context

✅ Good:
```
Generate a provider for this HMO member's referral
[Include: HMO network constraints, PCP referral]
```

❌ Avoid:
```
Generate a specialist
```

**Why**: Network type affects which providers are valid, referral requirements, and cost sharing.

---

## Related Documentation

- [Developer Guide](developer-guide.md) - Technical reference
- [SKILL.md](SKILL.md) - Skill routing
- [README](README.md) - Product overview
- [Reference Skills](reference/) - Concept explanations
- [Synthetic Skills](synthetic/) - Entity generation
- [Integration Skills](integration/) - Cross-product workflows

---

*NetworkSim Prompt Guide v1.0 - December 2024*
