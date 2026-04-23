---
name: therapeutic-oncology
description: |
  Generate oncology clinical trial data with RECIST 1.1 tumor assessments, 
  survival endpoints, and cancer-specific patterns. Triggers: "oncology", 
  "cancer", "tumor", "RECIST", "ORR", "PFS", "OS", "solid tumor".
---

# Oncology Trials

Generate realistic oncology clinical trial data with RECIST 1.1 tumor response assessments, survival endpoints, and cancer-specific adverse event patterns.

---

## For Claude

This is a **therapeutic area skill** for generating oncology trial data. Apply this when users request cancer clinical trials. Combine with phase cohort skills for complete trial generation.

**Always apply this skill when you see:**
- References to oncology, cancer, or tumor trials
- RECIST, tumor response, or imaging assessments
- Survival endpoints (OS, PFS, DFS)
- Cancer drug classes (chemotherapy, immunotherapy, targeted therapy)
- Specific cancer types (NSCLC, breast, colorectal, melanoma)

---

## RECIST 1.1 Response Criteria

### Target Lesion Assessment

| Response | Definition |
|----------|------------|
| **Complete Response (CR)** | Disappearance of all target lesions |
| **Partial Response (PR)** | ≥30% decrease in sum of diameters |
| **Progressive Disease (PD)** | ≥20% increase AND ≥5mm absolute increase, or new lesion |
| **Stable Disease (SD)** | Neither PR nor PD criteria met |

### Overall Response

| Target | Non-Target | New Lesions | Overall Response |
|--------|------------|-------------|------------------|
| CR | CR | No | CR |
| CR | Non-CR/Non-PD | No | PR |
| PR | Any | No | PR |
| SD | Any | No | SD |
| Any | PD | Any | PD |
| Any | Any | Yes | PD |

---

## Common Oncology Endpoints

### Primary Endpoints by Setting

| Setting | Common Primary Endpoints |
|---------|-------------------------|
| Metastatic (1L) | Overall Survival (OS), PFS |
| Metastatic (2L+) | PFS, ORR |
| Adjuvant | Disease-Free Survival (DFS) |
| Neoadjuvant | Pathological Complete Response (pCR) |

### Secondary Endpoints

- **Duration of Response (DOR)** - Time from response to progression
- **Disease Control Rate (DCR)** - CR + PR + SD
- **Clinical Benefit Rate (CBR)** - CR + PR + SD ≥6 months
- **Time to Response (TTR)** - Time from randomization to first response


---

## Cancer-Specific Patterns

### Non-Small Cell Lung Cancer (NSCLC)

**Biomarkers:**
- EGFR mutations (exon 19 del, L858R, T790M)
- ALK rearrangement
- ROS1 rearrangement
- KRAS G12C
- PD-L1 expression (TPS %, CPS)
- BRAF V600E

**Typical Response Rates:**
| Treatment | ORR | Median PFS | Median OS |
|-----------|-----|------------|-----------|
| Chemotherapy (1L) | 25-35% | 5-6 months | 10-12 months |
| IO monotherapy (PD-L1 ≥50%) | 40-50% | 7-10 months | 20-26 months |
| IO + Chemo | 45-60% | 8-9 months | 18-22 months |
| EGFR TKI (EGFR+) | 70-80% | 10-18 months | 24-38 months |

### Breast Cancer

**Biomarkers:**
- ER/PR status
- HER2 status (IHC, FISH)
- Ki-67
- BRCA1/2 mutations

**Subtypes:**
| Subtype | ER | PR | HER2 | Treatment Approach |
|---------|----|----|------|-------------------|
| Luminal A | + | + | - | Endocrine ± chemo |
| Luminal B | + | ± | - | Endocrine + chemo |
| HER2+ | ± | ± | + | Anti-HER2 + chemo |
| Triple Negative | - | - | - | Chemo ± IO |

### Melanoma

**Biomarkers:**
- BRAF V600E/K
- NRAS
- PD-L1

**Typical Response Rates:**
| Treatment | ORR | Median PFS |
|-----------|-----|------------|
| Anti-PD-1 monotherapy | 40-45% | 6-8 months |
| Anti-PD-1 + Anti-CTLA-4 | 55-60% | 11-12 months |
| BRAF + MEK (BRAF+) | 65-70% | 11-14 months |

---

## Adverse Events by Drug Class

### Chemotherapy

| AE Category | Common Events | Grade 3-4 Rate |
|-------------|---------------|----------------|
| Hematologic | Neutropenia, anemia, thrombocytopenia | 30-50% |
| GI | Nausea, vomiting, diarrhea | 5-15% |
| Constitutional | Fatigue, alopecia | 5-10% |
| Neurologic | Peripheral neuropathy | 5-20% |

### Checkpoint Inhibitors

| AE Category | Common Events | Grade 3-4 Rate |
|-------------|---------------|----------------|
| Endocrine | Hypothyroidism, hyperthyroidism | 1-2% |
| GI | Diarrhea, colitis | 2-5% |
| Hepatic | Hepatitis, elevated LFTs | 2-5% |
| Pulmonary | Pneumonitis | 2-5% |
| Skin | Rash, pruritus | 1-3% |


---

## Generation Patterns

### Tumor Response Data

```json
{
  "tumor_assessment": {
    "subject_id": "ONCO-001-0042",
    "assessment_date": "2024-09-15",
    "visit": "WEEK18",
    "target_lesions": [
      {
        "lesion_id": "TL01",
        "location": "RIGHT LUNG",
        "baseline_diameter_mm": 45,
        "current_diameter_mm": 28,
        "change_pct": -37.8
      }
    ],
    "sum_of_diameters": {
      "baseline_mm": 77,
      "current_mm": 50,
      "change_from_baseline_pct": -35.1
    },
    "overall_response": "PARTIAL RESPONSE"
  }
}
```

### Survival Data

```json
{
  "survival_data": {
    "subject_id": "ONCO-001-0042",
    "randomization_date": "2024-03-15",
    "treatment_arm": "EXPERIMENTAL",
    "progression_free_survival": {
      "event_type": "PROGRESSION",
      "event_date": "2024-12-20",
      "pfs_months": 9.2,
      "censored": false
    },
    "overall_survival": {
      "status": "ALIVE",
      "last_known_alive_date": "2025-02-15",
      "os_months": 11.1,
      "censored": true
    }
  }
}
```

---

## SDTM Mapping

### Tumor Results (TR) Domain

| Variable | Label | Example |
|----------|-------|---------|
| USUBJID | Subject ID | ONCO-001-0042 |
| TRTESTCD | Test Code | LDIAM |
| TRTEST | Test Name | Longest Diameter |
| TRORRES | Result | 28 |
| TRORRESU | Unit | mm |
| TRLOC | Location | RIGHT LUNG |
| VISITNUM | Visit Number | 6 |

### Response (RS) Domain

| Variable | Label | Example |
|----------|-------|---------|
| USUBJID | Subject ID | ONCO-001-0042 |
| RSTESTCD | Test Code | OVRLRESP |
| RSTEST | Test Name | Overall Response |
| RSORRES | Result | PR |
| RSSTRESC | Char Result | PARTIAL RESPONSE |

---

## Validation Checklist

- [ ] Target lesions ≤5 total, ≤2 per organ
- [ ] Lesion measurements in millimeters
- [ ] Response assessment per RECIST 1.1 rules
- [ ] Confirmation of response at next assessment
- [ ] Survival data consistent with response trajectory
- [ ] MedDRA coding for adverse events

---

## Related Skills

**TrialSim:**
- [Clinical Trials Domain](../clinical-trials-domain.md) - Core trial concepts
- [Phase 3 Pivotal](../phase3-pivotal.md) - Pivotal trial cohorts
- [CGT](cgt.md) - CAR-T and gene therapy oncology

**Shared Domain Knowledge:**
- [Oncology Domain](../../../references/oncology-domain.md) - Foundational oncology concepts, staging, treatment modalities
- [Oncology Reference Data](../../../references/oncology/) - ICD-10 codes, medications, regimens, tumor markers

**Cross-Product (PatientSim):**
- [PatientSim Oncology](../../patientsim/oncology/) - Clinical care pathways, treatment decision trees
- [Lung Cancer](../../patientsim/oncology/lung-cancer.md) - NSCLC/SCLC clinical journeys, biomarker-driven therapy
- [Breast Cancer](../../patientsim/oncology/breast-cancer.md) - Molecular subtypes, hormonal/targeted therapy
- [Colorectal Cancer](../../patientsim/oncology/colorectal-cancer.md) - MSI status, hereditary syndromes

> **Integration Pattern:** Use PatientSim oncology skills for detailed clinical care patterns (diagnosis, treatment selection, toxicity management). Use this TrialSim skill for trial-specific endpoints (RECIST, survival analysis, SDTM mapping).

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-12 | Initial oncology therapeutic area skill |
