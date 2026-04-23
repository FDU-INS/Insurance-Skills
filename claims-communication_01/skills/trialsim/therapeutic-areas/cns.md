---
name: therapeutic-cns
description: |
  Generate CNS/neurology clinical trial data with cognitive assessments, 
  neuroimaging endpoints, and neurological disease patterns. Triggers: "CNS", 
  "neurology", "Alzheimer's", "Parkinson's", "MS", "cognitive", "dementia".
---

# CNS/Neurology Trials

Generate realistic CNS and neurology clinical trial data with cognitive assessments, neuroimaging endpoints, and disease-specific patterns.

---

## For Claude

This is a **therapeutic area skill** for generating CNS/neurology trial data. Apply this when users request neurological or psychiatric trials.

**Always apply this skill when you see:**
- References to CNS, neurology, or brain-related trials
- Cognitive assessments or dementia endpoints
- Neuroimaging (MRI, PET) as endpoints
- Specific conditions (Alzheimer's, Parkinson's, MS, epilepsy)
- Neurological rating scales (ADAS-Cog, UPDRS, EDSS)

---

## Alzheimer's Disease

### Disease Staging

| Stage | Clinical Description | MMSE Range |
|-------|---------------------|------------|
| Preclinical | Biomarker positive, no symptoms | 26-30 |
| MCI due to AD | Mild cognitive impairment | 20-26 |
| Mild AD | Early dementia | 18-23 |
| Moderate AD | Clear functional decline | 10-18 |
| Severe AD | Significant dependence | <10 |

### Key Endpoints

| Endpoint | Instrument | Range | MCID |
|----------|------------|-------|------|
| **Primary** | ADAS-Cog 13 | 0-85 (higher=worse) | 2-3 points |
| **Co-primary** | CDR-SB | 0-18 (higher=worse) | 1-2 points |
| **Secondary** | MMSE | 0-30 (higher=better) | 2-3 points |

### Biomarkers

| Biomarker | AD Pattern | Measurement |
|-----------|------------|-------------|
| CSF Aβ42 | Decreased | <600 pg/mL |
| CSF p-tau | Increased | >60 pg/mL |
| Amyloid PET | Positive | SUVr >1.1 |

---

## Parkinson's Disease

### Hoehn & Yahr Staging

| Stage | Description |
|-------|-------------|
| 1 | Unilateral involvement only |
| 2 | Bilateral involvement without balance impairment |
| 3 | Mild to moderate bilateral disease; postural instability |
| 4 | Severe disability; still able to walk/stand unassisted |
| 5 | Wheelchair bound or bedridden |

### Key Endpoints

| Endpoint | Instrument | Range | MCID |
|----------|------------|-------|------|
| **Motor** | MDS-UPDRS Part III | 0-132 | 3-5 points |
| **Total** | MDS-UPDRS Total | 0-260 | 5-8 points |
| **ON time** | Patient diary | Hours | 1 hour |


---

## Multiple Sclerosis

### Disease Types

| Type | Abbreviation | Description |
|------|--------------|-------------|
| Relapsing-Remitting | RRMS | Discrete attacks with recovery |
| Secondary Progressive | SPMS | Progressive after initial RRMS |
| Primary Progressive | PPMS | Progressive from onset |

### Key Endpoints

| Endpoint | Instrument | Range | MCID |
|----------|------------|-------|------|
| **Disability** | EDSS | 0-10 (0.5 steps) | 0.5-1.0 points |
| **Relapses** | ARR | Annual rate | 30% reduction |
| **MRI lesions** | T2 lesion count | Count | - |
| **Brain atrophy** | BPF change | % change | 0.4%/year |

---

## Generation Patterns

### ADAS-Cog Assessment

```json
{
  "cognitive_assessment": {
    "subject_id": "AD301-025-0112",
    "visit": "WEEK52",
    "instrument": "ADAS-COG-13",
    "total_score": 28.5,
    "change_from_baseline": 4.2,
    "subscales": {
      "word_recall": 6.5,
      "orientation": 2.0,
      "word_recognition": 4.5,
      "delayed_word_recall": 5.0
    }
  }
}
```

### MRI Volumetrics

```json
{
  "neuroimaging": {
    "subject_id": "AD301-025-0112",
    "modality": "MRI",
    "volumes": {
      "whole_brain_ml": 1142.5,
      "whole_brain_pct_change": -1.8,
      "hippocampus_total_mm3": 5230,
      "hippocampus_pct_change": -3.2
    },
    "aria_assessment": {
      "aria_e_present": false,
      "aria_h_present": false
    }
  }
}
```

---

## Validation Checklist

- [ ] Cognitive scale scores within valid ranges
- [ ] EDSS scores in 0.5-point increments
- [ ] Rater certification documented
- [ ] ARIA monitoring per protocol
- [ ] ON/OFF medication state documented for PD

---

## Related Skills

**TrialSim:**
- [Clinical Trials Domain](../clinical-trials-domain.md) - Core trial concepts
- [Cardiovascular](cardiovascular.md) - Stroke endpoints

**Cross-Product (PatientSim):**
- [Behavioral Health](../../patientsim/behavioral-health.md) - Psychiatric conditions (depression, anxiety, bipolar), PHQ-9/GAD-7 assessments

> **Integration Pattern:** TrialSim CNS focuses on neurological diseases (Alzheimer's, Parkinson's, MS) with cognitive/motor endpoints. PatientSim behavioral-health covers psychiatric conditions with mood/anxiety assessments. For CNS trials involving psychiatric endpoints (e.g., depression scales), reference both skills.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-12 | Initial CNS/neurology therapeutic area skill |
