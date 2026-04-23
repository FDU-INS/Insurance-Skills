---
name: populationsim-prompt-guide
description: |
  Example prompts for using PopulationSim skills effectively. Templates for 
  population analysis, SDOH assessment, cohort definition, trial support, 
  and cross-product integration cohorts.
---

# PopulationSim Prompt Guide

## Overview

This guide provides example prompts for using PopulationSim skills effectively. Use these templates as starting points for your population analysis and synthetic data generation needs.

---

## Foundation Prompts

### Basic Population Profile

```
Create a population profile for [County Name], [State]

Example:
Create a population profile for Harris County, Texas
```

**Expected Output**: Complete PopulationProfile with demographics, health indicators, and SDOH

---

### State-Level Overview

```
Generate a state-level demographic overview for [State]

Example:
Generate a state-level demographic overview for California
```

---

### Metropolitan Area Analysis

```
Analyze the population characteristics of the [MSA Name] metropolitan area

Example:
Analyze the population characteristics of the Houston-The Woodlands-Sugar Land metropolitan area
```

---

## Geographic Intelligence Prompts

### Tract-Level Analysis

```
Provide a census tract analysis for tracts in [County] with [criteria]

Example:
Provide a census tract analysis for tracts in Harris County with SVI above 0.70
```

---

### Urban/Rural Comparison

```
Compare urban and rural population characteristics in [County/State]

Example:
Compare urban and rural population characteristics in Texas
```

---

### Multi-County Region

```
Create a combined population profile for [County List]

Example:
Create a combined population profile for Harris, Fort Bend, and Montgomery counties in Texas
```

---

## Health Pattern Prompts

### Chronic Disease Prevalence

```
What are the chronic disease prevalence rates in [Geography]?

Example:
What are the chronic disease prevalence rates in Harris County, Texas?
```

---

### Health Behavior Analysis

```
Analyze health behaviors including smoking, physical activity, and sleep patterns in [Geography]

Example:
Analyze health behaviors including smoking, physical activity, and sleep patterns in Dallas County
```

---

### Prevention Metrics

```
What are the preventive care screening rates in [Geography]?

Example:
What are the preventive care screening rates in Travis County, Texas?
```

---

### Diabetes Deep Dive

```
Provide a detailed diabetes profile for [Geography] including prevalence, comorbidities, and demographic breakdown

Example:
Provide a detailed diabetes profile for Harris County including prevalence, comorbidities, and demographic breakdown
```

---

## SDOH Analysis Prompts

### Social Vulnerability Assessment

```
Analyze social vulnerability (SVI) for [Geography] with theme breakdown

Example:
Analyze social vulnerability for Harris County census tracts with theme breakdown
```

---

### Area Deprivation Analysis

```
What is the Area Deprivation Index distribution in [Geography]?

Example:
What is the Area Deprivation Index distribution in census tracts around downtown Houston?
```

---

### Economic Factors

```
Analyze economic factors including income, poverty, and employment in [Geography]

Example:
Analyze economic factors including income, poverty, and employment in Bexar County, Texas
```

---

### Healthcare Access

```
Assess healthcare access including insurance coverage, provider availability, and HPSA status in [Geography]

Example:
Assess healthcare access including insurance coverage, provider availability, and HPSA status in rural East Texas counties
```

---

### Z-Code Prevalence

```
Estimate SDOH Z-code prevalence rates for [Geography]

Example:
Estimate SDOH Z-code prevalence rates for high-vulnerability tracts in Harris County
```

---

## Cohort Definition Prompts

### Basic Clinical Cohort

```
Define a cohort of [condition] patients aged [age range] in [Geography]

Example:
Define a cohort of diabetic patients aged 40-70 in Harris County
```

---

### SDOH-Focused Cohort

```
Define a cohort from high-vulnerability areas with [conditions] in [Geography]

Example:
Define a cohort from high-vulnerability areas (SVI ≥ 0.70) with diabetes and hypertension in Harris County
```

---

### Diversity Requirements Cohort

```
Define a cohort with specific diversity requirements: [requirements]

Example:
Define a cohort of 1,000 patients with:
- Diabetes diagnosis
- Age 35-65
- At least 40% minority representation
- At least 25% from high-SDOH areas (SVI ≥ 0.60)
- Geographic scope: Houston metropolitan area
```

---

### Multi-Condition Cohort

```
Define a cohort with multiple conditions and comorbidity requirements

Example:
Define a cohort of patients with:
- Type 2 diabetes (required)
- Hypertension (at least 50% prevalence)
- Obesity (at least 40% prevalence)
- Exclude: ESRD, active cancer, pregnancy
- Size: 2,000 patients
```

---

### Insurance-Specific Cohort

```
Define a cohort with specific insurance coverage requirements

Example:
Define a cohort of Medicare beneficiaries with:
- Age 65+
- Diabetes diagnosis
- From Medicaid expansion counties
- Include dual-eligible at 15% rate
```

---

## Trial Support Prompts

### Site Feasibility

```
Assess clinical trial feasibility for a [condition] trial at [site locations]

Example:
Assess clinical trial feasibility for a Type 2 diabetes cardiovascular outcomes trial at sites in Houston, Dallas, and San Antonio
```

---

### Catchment Analysis

```
Analyze the catchment area for a trial site at [location] with [radius] mile radius

Example:
Analyze the catchment area for a trial site at Houston Medical Center with 30 mile radius
```

---

### Diversity Planning

```
Create a diversity enrollment plan for a [condition] trial with [target] subjects

Example:
Create a diversity enrollment plan for a diabetes trial with 500 subjects meeting FDA diversity guidance
```

---

### Enrollment Projection

```
Project enrollment timeline for a [condition] trial with [parameters]

Example:
Project enrollment timeline for a Phase 3 diabetes trial with:
- Target enrollment: 500 subjects
- 3 sites (Houston, Dallas, San Antonio)
- 18-month enrollment window
- Diversity targets: 40% minority, 50% female
```

---

### Retention Modeling

```
Model retention rates for a trial population with high SDOH burden

Example:
Model 12-month retention rates for a diabetes trial population with:
- 30% high-vulnerability (SVI ≥ 0.75)
- 15% transportation insecure
- 12% food insecure
Include recommended accommodations
```

---

## Cross-Product Integration Prompts

### PatientSim Integration

```
Generate a population-matched patient cohort for [use case]

Example:
Generate a population-matched patient cohort of 500 diabetic patients from Harris County for EMR testing, including:
- FHIR Patient resources
- Condition resources with SDOH Z-codes
- 2 years of encounter history
```

---

### MemberSim Integration

```
Generate members with claims data based on [population profile]

Example:
Generate 1,000 health plan members from the Harris County population profile with:
- Population-based insurance distribution
- 12 months of professional and institutional claims
- Pharmacy claims included
- X12 834/837 output format
```

---

### Full Ecosystem Generation

```
Generate a complete synthetic healthcare dataset for [cohort]

Example:
Generate a complete synthetic healthcare dataset for a diabetes quality improvement study:
- 2,000 patients from high-SDOH areas of Houston
- Clinical records (PatientSim/FHIR)
- Insurance enrollment (MemberSim/X12 834)
- Medical claims (MemberSim/X12 837)
- Pharmacy claims (RxMemberSim/NCPDP)
- Correlated by SSN
```

---

## Advanced Analysis Prompts

### Comparative Analysis

```
Compare [metric] across [geographies]

Example:
Compare diabetes prevalence and SDOH factors across the 10 largest Texas counties
```

---

### Trend Analysis

```
Analyze how [metric] varies by [dimension] in [Geography]

Example:
Analyze how chronic disease prevalence varies by SVI quartile in Harris County census tracts
```

---

### Disparity Analysis

```
Identify health disparities by [demographic factor] in [Geography]

Example:
Identify health disparities by race/ethnicity in cardiovascular disease outcomes in Harris County
```

---

### Custom Geographic Selection

```
Select census tracts meeting [criteria] for [purpose]

Example:
Select census tracts meeting these criteria for a community health intervention:
- SVI Theme 1 (socioeconomic) ≥ 0.70
- Diabetes prevalence > 12%
- At least 5,000 population
- Within Houston city limits
```

---

## Tips for Effective Prompts

### Be Specific About Geography

✅ "Harris County, Texas (FIPS 48201)"  
❌ "Houston area"

### Specify Output Needs

✅ "Include Z-code prevalence estimates"  
❌ "Include SDOH data"

### Set Clear Thresholds

✅ "SVI ≥ 0.70, ADI national percentile ≥ 70"  
❌ "High vulnerability areas"

### Define Cohort Size

✅ "Target 1,000 patients with ±5% tolerance"  
❌ "A reasonably sized cohort"

### Clarify Integration Needs

✅ "Enable PatientSim integration with FHIR R4 output"  
❌ "Make it work with other tools"

---

## Related Documentation

- [Developer Guide](developer-guide.md)
- [SKILL.md](SKILL.md)
- [Integration Guide](integration/README.md)
