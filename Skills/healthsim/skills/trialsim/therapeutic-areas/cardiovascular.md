---
name: therapeutic-cardiovascular
description: |
  Generate cardiovascular clinical trial data with MACE endpoints, heart failure 
  outcomes, and CV-specific patterns. Triggers: "cardiovascular", "cardiac", 
  "heart failure", "MACE", "CV outcomes", "HFrEF", "HFpEF".
---

# Cardiovascular Trials

Generate realistic cardiovascular clinical trial data with MACE endpoints, heart failure outcomes, and CV-specific safety patterns.

---

## For Claude

This is a **therapeutic area skill** for generating CV trial data. Apply this when users request cardiac or CV outcomes trials.

**Always apply this skill when you see:**
- References to cardiovascular, cardiac, or heart trials
- MACE or CV outcomes endpoints
- Heart failure (HFrEF, HFpEF)
- CV drug classes (SGLT2i, ARNi, beta-blockers)

---

## MACE Endpoints

### Standard MACE Definitions

| Endpoint | Components |
|----------|------------|
| **3-point MACE** | CV death, non-fatal MI, non-fatal stroke |
| **4-point MACE** | 3-point + hospitalization for unstable angina |
| **Expanded MACE** | 3-point + HF hospitalization |

### Component Definitions

| Event | Definition |
|-------|------------|
| **CV Death** | Death from MI, stroke, HF, sudden cardiac death |
| **Non-fatal MI** | Type 1 MI with biomarker rise + symptoms or ECG changes |
| **Non-fatal Stroke** | Focal neurological deficit >24h or imaging evidence |
| **HF Hospitalization** | Admission with primary diagnosis of HF, requiring IV therapy |

---

## Heart Failure Classifications

### Ejection Fraction Categories

| Category | EF Range | Abbreviation |
|----------|----------|--------------|
| Reduced | ≤40% | HFrEF |
| Mildly Reduced | 41-49% | HFmrEF |
| Preserved | ≥50% | HFpEF |

### NYHA Functional Class

| Class | Description |
|-------|-------------|
| I | No limitation; ordinary activity does not cause symptoms |
| II | Slight limitation; ordinary activity causes symptoms |
| III | Marked limitation; less than ordinary activity causes symptoms |
| IV | Unable to carry on any activity without discomfort; symptoms at rest |

---

## Cardiac Biomarkers

| Biomarker | Use | Thresholds |
|-----------|-----|------------|
| **Troponin I/T** | MI diagnosis | >99th percentile URL |
| **NT-proBNP** | HF diagnosis | >300 pg/mL (acute) |
| **BNP** | HF diagnosis | >100 pg/mL |
| **hs-CRP** | CV risk | >2 mg/L high risk |


---

## CV Drug Classes (GDMT for HFrEF)

| Drug Class | Examples | Target Dose |
|------------|----------|-------------|
| ACEi/ARB | Lisinopril, Losartan | Max tolerated |
| ARNi | Sacubitril/valsartan | 97/103 mg BID |
| Beta-blocker | Carvedilol, Metoprolol XL | Max tolerated |
| MRA | Spironolactone, Eplerenone | 25-50 mg daily |
| SGLT2i | Dapagliflozin, Empagliflozin | 10 mg daily |

---

## Generation Patterns

### MACE Event

```json
{
  "mace_event": {
    "subject_id": "CV301-015-0089",
    "event_type": "NON_FATAL_MI",
    "event_date": "2024-09-20",
    "event_details": {
      "mi_type": "TYPE_1",
      "presentation": "NSTEMI",
      "peak_troponin": 2.45,
      "intervention": "PCI"
    },
    "adjudication": {
      "cec_confirmed": true,
      "adjudication_date": "2024-10-15"
    }
  }
}
```

### Echo Assessment

```json
{
  "echocardiogram": {
    "subject_id": "CV301-015-0089",
    "assessment_date": "2024-08-15",
    "lv_function": {
      "lvef_pct": 32,
      "lvef_method": "SIMPSON_BIPLANE",
      "lvedd_mm": 62
    },
    "diastolic_function": {
      "e_e_prime_ratio": 15,
      "grade": "GRADE_II"
    }
  }
}
```

---

## Validation Checklist

- [ ] MACE components properly adjudicated
- [ ] EF measurements within physiologic range
- [ ] NYHA class appropriate for EF
- [ ] Biomarker values clinically plausible
- [ ] ECG parameters in valid ranges (HR, QTc)

---

## Related Skills

**TrialSim:**
- [Clinical Trials Domain](../clinical-trials-domain.md) - Core trial concepts
- [CNS](cns.md) - Stroke and neurological endpoints

**Cross-Product (PatientSim):**
- [Heart Failure](../../patientsim/heart-failure.md) - HF clinical care pathways, GDMT optimization, hospitalization patterns

> **Integration Pattern:** Use PatientSim heart-failure.md for clinical care journeys and treatment optimization. Use this TrialSim skill for CV outcomes trials (MACE endpoints, adjudicated events, SDTM mapping).

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-12 | Initial cardiovascular therapeutic area skill |
