---
name: network-adequacy
description: |
  Reference knowledge about network adequacy standards including time/distance
  requirements, provider-to-member ratios, essential community providers, and
  access disparity patterns. Links to PopulationSim for geographic context.
  
  Trigger phrases: "network adequacy", "access standards", "time distance",
  "provider ratio", "essential community provider", "HPSA", "MUA", "access",
  "network access", "adequacy requirements"
version: "1.0"
category: reference
related_skills:
  - network-types
  - synthetic-network
  - network-for-member
cross_product:
  - populationsim: Geographic and HPSA/MUA data
---

# Network Adequacy

## Overview

Network adequacy ensures health plan members have reasonable access to healthcare providers. Regulators set standards for time/distance to providers, provider-to-member ratios, and inclusion of essential community providers.

---

## Trigger Phrases

Use this skill when you see:
- "What is network adequacy?"
- "Time and distance standards"
- "Provider ratio requirements"
- "Essential community providers"
- "Access standards"
- "Network access requirements"
- "HPSA/MUA areas"

---

## What is Network Adequacy?

### Definition

Network adequacy is the requirement that health plan provider networks include sufficient numbers and types of providers to ensure members can access covered services without unreasonable delay.

### Regulatory Context

| Regulator | Applies To | Key Requirements |
|-----------|------------|------------------|
| **CMS** | Medicare Advantage, ACA plans | Time/distance, appointments |
| **State DOI** | Commercial plans | Varies by state |
| **NCQA** | Accredited plans | Credentialing, access |
| **URAC** | Accredited plans | Network standards |

### Why It Matters

Without adequacy standards:
- Members in rural areas might have no nearby providers
- Wait times for appointments could be excessive
- Certain specialties might be unavailable
- Essential services could be inaccessible

---

## Time and Distance Standards

### Federal Standards (CMS)

Medicare Advantage and ACA Marketplace plans must meet these standards:

**Primary Care**:
| Area Type | Max Time | Max Distance |
|-----------|----------|--------------|
| Large Metro | 10 min | 5 miles |
| Metro | 10 min | 10 miles |
| Micro | 20 min | 20 miles |
| Rural | 30 min | 30 miles |
| CEAC | 40 min | 40 miles |

**Specialty Care** (varies by specialty):
| Specialty | Large Metro | Metro | Micro | Rural |
|-----------|-------------|-------|-------|-------|
| Cardiology | 15 min/10 mi | 30 min/30 mi | 45 min/45 mi | 60 min/60 mi |
| Oncology | 15 min/10 mi | 30 min/30 mi | 60 min/60 mi | 75 min/75 mi |
| Dermatology | 15 min/10 mi | 30 min/30 mi | 45 min/45 mi | 60 min/60 mi |
| Mental Health | 10 min/5 mi | 20 min/20 mi | 45 min/45 mi | 60 min/60 mi |

### State Variations

States may have stricter requirements:

| State | Notable Requirement |
|-------|---------------------|
| California | Strict mental health parity standards |
| New York | Specialty-specific access times |
| Texas | Network sufficiency reporting |
| Florida | Provider ratio requirements |

---

## Provider-to-Member Ratios

### Definition

Provider ratios measure the number of providers available relative to plan membership, ensuring sufficient provider capacity.

### Common Ratio Standards

| Provider Type | Typical Ratio | Meaning |
|---------------|---------------|---------|
| **PCP** | 1:2,000 | 1 PCP per 2,000 members |
| **OB/GYN** | 1:2,000 | 1 OB per 2,000 female members |
| **Mental Health** | 1:5,000 | 1 MH provider per 5,000 members |
| **Hospital Beds** | 1:1,000 | 1 bed per 1,000 members |

### Calculating Adequacy

```
Network has:
- 500 PCPs
- 250,000 members

PCP Ratio: 500/250,000 = 1:500
Standard: 1:2,000

Result: Network exceeds adequacy standard
```

---

## Essential Community Providers (ECPs)

### Definition

Essential Community Providers are providers that serve predominantly low-income and medically underserved populations. ACA requires QHP networks to include ECPs.

### ECP Categories

| Category | Examples |
|----------|----------|
| **FQHC** | Federally Qualified Health Centers |
| **RHC** | Rural Health Clinics |
| **Indian Health** | IHS, Tribal, Urban Indian |
| **Ryan White** | HIV/AIDS providers |
| **Family Planning** | Title X clinics |
| **STD Clinics** | Public health STD services |
| **TB Clinics** | Public health TB services |
| **Hemophilia** | Hemophilia treatment centers |
| **Substance Abuse** | SAMHSA-listed providers |
| **Mental Health** | Community mental health centers |

### ACA Requirements

- QHPs must include 30% of available ECPs in service area
- Must include at least one ECP in each category available
- Must offer contracts to ECPs at no worse than standard terms

---

## Health Professional Shortage Areas (HPSAs)

### Definition

HPSAs are designated areas with a shortage of primary care, dental, or mental health providers. Designated by HRSA.

### HPSA Types

| Type | Shortage Of |
|------|-------------|
| **Primary Care** | PCPs (physicians, NPs, PAs) |
| **Dental** | Dentists |
| **Mental Health** | Psychiatrists, psychologists, etc. |

### HPSA Designation Types

| Designation | Description |
|-------------|-------------|
| **Geographic** | Entire county or area |
| **Population** | Specific underserved population |
| **Facility** | Specific facility designation |

### Integration with PopulationSim

PopulationSim provides HPSA designations that can inform NetworkSim adequacy analysis:

```
Query PopulationSim:
- Which counties are primary care HPSAs?
- What is the HPSA score for this county?
- Which ZCTAs are mental health HPSAs?
```

---

## Medically Underserved Areas (MUAs)

### Definition

MUAs are areas with a shortage of primary care services based on a composite of factors beyond just provider counts.

### MUA Scoring Factors

| Factor | Weight |
|--------|--------|
| Provider-to-population ratio | Significant |
| Infant mortality rate | Significant |
| Poverty rate | Significant |
| Percent elderly (65+) | Significant |

### MUA vs HPSA

| Aspect | HPSA | MUA |
|--------|------|-----|
| Focus | Provider shortage | Service shortage |
| Factors | Primarily ratio | Multiple factors |
| Use | Loan repayment, bonus | FQHC designation |

---

## Access Disparity Patterns

### Common Disparity Types

| Disparity | Description |
|-----------|-------------|
| **Geographic** | Rural vs urban access |
| **Specialty** | Limited specialty availability |
| **Language** | Non-English speaking access |
| **Cultural** | Culturally competent care |
| **Economic** | Low-income area access |

### Rural Access Challenges

```
Rural areas often have:
- Fewer specialists (must travel for specialty care)
- Limited hospital options (CAH may be only option)
- Provider shortages (HPSA designation common)
- Transportation barriers (no public transit)
- Telehealth potential (if broadband available)
```

### Urban Access Challenges

```
Urban areas may have:
- Provider concentration (not distribution)
- Safety net provider reliance
- Language/cultural barriers
- Insurance acceptance issues
- Transportation to specific facilities
```

---

## Measuring Network Adequacy

### Access Analysis Process

```
1. Map member locations (ZIP centroids)
2. Map provider locations
3. Calculate time/distance for each member
4. Identify gaps (members exceeding standards)
5. Report by specialty, area type
```

### Adequacy Report Elements

| Element | Measure |
|---------|---------|
| **Coverage** | % members within standards |
| **Gaps** | Areas/members without access |
| **Ratios** | Provider-to-member calculations |
| **ECPs** | % ECP inclusion |
| **Wait Times** | Appointment availability |

---

## Examples

### Example 1: Understanding Network Adequacy

**Prompt**: "What is network adequacy and why does it matter?"

**Response**:

Network adequacy ensures that health plan members have reasonable access to healthcare providers. It's about having enough providers, in the right locations, accepting new patients.

**Key Components**:

1. **Time/Distance Standards**
   - Can members reach providers within reasonable time?
   - Example: PCP within 10 minutes in urban areas
   
2. **Provider Ratios**
   - Are there enough providers for the member population?
   - Example: 1 PCP per 2,000 members
   
3. **Essential Community Providers**
   - Are safety-net providers included?
   - Example: FQHCs serving low-income populations
   
4. **Appointment Availability**
   - Can members get appointments within reasonable time?
   - Example: Urgent care within 24 hours

**Why It Matters**:

Without adequacy requirements:
- Rural members might drive 2+ hours for care
- Specialists might be completely unavailable
- Low-income populations might have no options
- Wait times could be weeks or months

**Who Enforces It**:
- CMS (Medicare Advantage, Marketplace)
- State insurance departments (commercial plans)
- Accreditation organizations (NCQA, URAC)

Plans must demonstrate adequacy when filing rates and may be denied or sanctioned for inadequate networks.

---

### Example 2: Geographic Access Standards

**Prompt**: "Explain time and distance standards for network adequacy"

**Response**:

Time and distance standards define the maximum travel time and distance members should have to reach in-network providers.

**How Standards Vary by Area**:

| Area Type | PCP | Specialist | Hospital |
|-----------|-----|------------|----------|
| **Large Metro** (>1M pop) | 10 min/5 mi | 15 min/10 mi | 10 min/10 mi |
| **Metro** (50K-1M) | 10 min/10 mi | 30 min/30 mi | 15 min/15 mi |
| **Micro** (10-50K) | 20 min/20 mi | 45 min/45 mi | 30 min/30 mi |
| **Rural** (<10K) | 30 min/30 mi | 60 min/60 mi | 40 min/40 mi |

**Specialty-Specific Examples**:

| Specialty | Urban | Rural |
|-----------|-------|-------|
| Cardiology | 15 min | 60 min |
| Oncology | 15 min | 75 min |
| Mental Health | 10 min | 60 min |
| Pediatrics | 10 min | 45 min |

**How It's Measured**:
1. Plot member addresses (usually by ZIP centroid)
2. Plot in-network provider addresses
3. Calculate driving time/distance to nearest provider
4. Identify members exceeding standards
5. Report compliance percentage

**What Happens If Not Met**:
- Network exception required (explain gap, mitigation)
- Enhanced telehealth may partially satisfy
- Out-of-network coverage at in-network rates
- Potential denial of plan certification

---

## PopulationSim Integration

NetworkSim works with PopulationSim for geographic adequacy analysis:

| Need | PopulationSim Provides |
|------|------------------------|
| Member distribution | Population by geography |
| Underserved areas | HPSA/MUA designations |
| Demographics | Age, income distribution |
| Rural/Urban | CBSA classifications |

**Example Query**:
```
Use PopulationSim to identify primary care HPSA counties in Texas,
then use NetworkSim to analyze provider coverage in those counties.
```

---

## Related Skills

- [Network Types](network-types.md) - Network type definitions
- [Synthetic Network](../synthetic/synthetic-network.md) - Generate networks
- [Network for Member](../integration/network-for-member.md) - MemberSim integration
- PopulationSim - Geographic and HPSA data

---

*Network Adequacy is a reference skill in the NetworkSim product.*
