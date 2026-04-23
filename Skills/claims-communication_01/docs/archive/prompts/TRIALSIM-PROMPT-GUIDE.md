# TrialSim Prompt Guide

**Purpose**: Guide for crafting effective prompts to generate clinical trial synthetic data  
**Audience**: Users of TrialSim within HealthSim  
**Last Updated**: December 2024

---

## Prompt Structure

### Basic Pattern

```
Generate [what] for [trial type] with [specifications]
```

### Components

| Component | Examples |
|-----------|----------|
| **What** | subjects, adverse events, lab results, SDTM domains |
| **Trial Type** | Phase 1 oncology, Phase 3 cardiovascular, CNS trial |
| **Specifications** | sample size, time period, format, therapeutic area |

---

## Example Prompts by Use Case

### 1. Complete Trial Dataset

**Simple:**
```
Generate a complete Phase 3 oncology trial with 200 subjects
```

**Detailed:**
```
Generate a Phase 3 double-blind RCT for advanced NSCLC:
- 200 subjects (2:1 randomization)
- 24-month treatment period
- SDTM domains: DM, AE, LB, VS, EX
- Include RECIST 1.1 tumor assessments
```

### 2. Specific SDTM Domains

**Demographics:**
```
Generate DM domain for 50 subjects across 5 sites
```

**Adverse Events:**
```
Generate adverse events for an immunotherapy trial:
- 30 subjects
- 12-month follow-up
- Include immune-related AEs (colitis, pneumonitis, hepatitis)
- MedDRA coded with severity grades
```

**Laboratory:**
```
Generate LB domain with:
- Chemistry panel (liver, renal function)
- Hematology (CBC with differential)
- LOINC codes included
- Visits at screening, baseline, weeks 4, 8, 12
```

### 3. Trial Phases

**Phase 1:**
```
Generate a Phase 1 dose-escalation study:
- 3+3 design
- 4 dose levels (100mg, 200mg, 400mg, 800mg)
- Identify MTD based on DLT patterns
```

**Phase 2:**
```
Generate Phase 2 proof-of-concept data:
- Simon's optimal two-stage design
- Target response rate: 30%
- 25 subjects in stage 1, expand to 50 if threshold met
```

**Phase 3:**
```
Generate Phase 3 pivotal trial:
- Parallel group, 1:1 randomization
- Double-blind, placebo-controlled
- Primary endpoint: PFS
- 400 subjects, 36-month follow-up
```

### 4. Therapeutic Areas

**Oncology:**
```
Generate oncology trial data with:
- Solid tumor (NSCLC)
- RECIST 1.1 response assessments
- Include progression events and deaths
- Time-to-event data for PFS and OS
```

**CNS:**
```
Generate Alzheimer's trial data:
- Mild-to-moderate AD population
- MMSE 14-26 at baseline
- ADAS-Cog assessments at baseline, months 6, 12, 18
- Include cognitive decline patterns
```

**Cardiovascular:**
```
Generate CV outcomes trial:
- Heart failure population (NYHA II-III)
- Primary endpoint: MACE
- Include hospitalization events
- 24-month follow-up
```

**Cell & Gene Therapy:**
```
Generate CAR-T trial data:
- r/r DLBCL population
- Include manufacturing data
- Track CRS and neurotoxicity
- Long-term follow-up (5 years)
```

### 5. Screening and Enrollment

```
Generate screening data for oncology trial:
- 500 patients screened
- 30% screen failure rate
- Common failures: ECOG status, prior therapy, organ function
- Track time from screening to randomization
```

### 6. Real World Evidence

```
Generate synthetic control arm:
- Match to trial population demographics
- Use claims-based outcomes
- Include propensity score weights
```

---

## Output Format Requests

| Format | How to Request | Use Case |
|--------|----------------|----------|
| JSON | (default) | Internal processing |
| SDTM | "as SDTM", "SDTM format" | FDA/EMA submission |
| ADaM | "as ADaM", "analysis dataset" | Statistical analysis |
| CSV | "as CSV" | Quick review |

### Examples

```
Generate DM domain for 20 subjects as JSON
```

```
Generate adverse events in SDTM format with all required variables
```

```
Generate analysis-ready ADAE dataset
```

---

## Combining Skills

### Pattern 1: Therapeutic Area + Phase + Domains

```
Using oncology therapeutic patterns, generate a Phase 3 trial
with DM, AE, and LB domains for 100 subjects
```

### Pattern 2: Cross-Product Integration

```
Start with a PatientSim oncology patient with Stage IIIB NSCLC,
then enroll them in a TrialSim immunotherapy trial and
generate their complete trial record including AEs and tumor assessments
```

### Pattern 3: Screening to Completion

```
Generate the full patient journey:
1. Screening with I/E criteria evaluation
2. Randomization to treatment arm
3. On-treatment assessments (visits, labs, AEs)
4. End of study disposition
```

---

## Specification Parameters

### Sample Size
```
- 50 subjects
- Sample size: 200
- N=100 per arm
```

### Time Period
```
- 12-month treatment period
- 24-week follow-up
- 5-year long-term monitoring
```

### Sites
```
- 5 sites
- Multi-center (10 sites across 3 countries)
- Site IDs: 001-010
```

### Randomization
```
- 1:1 randomization
- 2:1 active:placebo
- Stratified by ECOG status
```

### Blinding
```
- Double-blind
- Open-label
- Single-blind (subject blinded)
```

---

## Common Patterns

### Realistic Data Requests

**Include temporal patterns:**
```
Generate AEs with realistic timing - more events early in treatment,
tapering after week 8
```

**Include dropouts:**
```
Include 15% dropout rate with realistic disposition reasons
(AE, lack of efficacy, withdrawal of consent)
```

**Include missing data:**
```
Include realistic missing data patterns - 5-10% missing lab values,
higher missingness after discontinuation
```

### Quality Variations

**Minimum viable:**
```
Generate basic trial data - just demographics and disposition
```

**Production quality:**
```
Generate complete, submission-ready SDTM data package:
- All required domains with full variables
- Controlled terminology
- Valid MedDRA/LOINC codes
- Proper date formatting
```

---

## Validation Prompts

### Check Generated Data

```
Validate the generated AE domain:
- Confirm USUBJID format
- Verify MedDRA coding accuracy
- Check date sequencing
- Ensure required variables present
```

### Compare to Standards

```
Compare this DM domain against CDISC SDTM IG 3.3 requirements
and identify any discrepancies
```

---

## Troubleshooting

### If results are too generic

Add specificity:
```
Instead of: "Generate trial data"
Use: "Generate Phase 2 oncology dose-ranging study with 4 arms 
     (placebo, low, medium, high dose), 25 subjects per arm, 
     16-week treatment"
```

### If missing required elements

Be explicit about what you need:
```
"Include all required SDTM variables for AE domain:
STUDYID, DOMAIN, USUBJID, AESEQ, AETERM, AEDECOD,
AEBODSYS, AESTDTC, AEENDTC, AESER, AEREL, AEOUT"
```

### If format is wrong

Specify output format:
```
"Output as SDTM-compliant JSON with domain metadata header"
```

---

## Quick Reference Card

| To Generate | Start Your Prompt With |
|-------------|------------------------|
| Full trial | "Generate a Phase [X] [therapeutic] trial..." |
| SDTM domain | "Generate [DOMAIN] domain for..." |
| Specific population | "Generate [N] subjects with [characteristics]..." |
| Time-to-event | "Generate survival data with..." |
| Safety data | "Generate adverse events for..." |
| Screening | "Generate screening data with [X]% failure rate..." |

---

## Advanced Patterns

### Conditional Generation

```
Generate 100 subjects where:
- 60% are responders (CR or PR by RECIST)
- 25% have stable disease
- 15% have progressive disease
Then generate matching AE profiles (responders have more immune-related AEs)
```

### Longitudinal Consistency

```
Generate a subject's complete trial record ensuring:
- Lab values trend realistically over time
- AE start dates are after treatment start
- Disposition date is after last assessment
- All dates are chronologically consistent
```

### Regulatory Cohorts

```
Generate data for FDA submission including:
- Define.xml metadata
- Reviewer's guide comments
- Common data quality issues to test validation rules
```

---

## Related Documentation

| Document | Location |
|----------|----------|
| TrialSim Skills | `skills/trialsim/SKILL.md` |
| Developer Guide | `docs/TRIALSIM-DEVELOPER-GUIDE.md` |
| CDISC SDTM Format | `formats/cdisc-sdtm.md` |
| CDISC ADaM Format | `formats/cdisc-adam.md` |

---

*For technical details on skill structure, see the TrialSim Developer Guide.*
