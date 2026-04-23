---
name: therapeutic-cgt
description: |
  Generate cell and gene therapy clinical trial data with long-term follow-up, 
  gene expression monitoring, and CGT-specific safety patterns. Triggers: 
  "gene therapy", "CAR-T", "cell therapy", "CGT", "ATMP", "viral vector".
---

# Cell & Gene Therapy Trials

Generate realistic cell and gene therapy (CGT) clinical trial data with unique patterns including single-dose administration, long-term follow-up (5-15 years), and CGT-specific safety events.

---

## For Claude

This is a **therapeutic area skill** for generating CGT trial data. CGT trials differ significantly from traditional pharma trials.

**Always apply this skill when you see:**
- References to gene therapy, CAR-T, or cell therapy
- Viral vectors (AAV, lentivirus)
- CRISPR or gene editing
- Long-term follow-up (LTFU) requirements
- CRS, ICANS, or immune-related toxicities

---

## Key Differences from Traditional Pharma

| Aspect | Traditional Pharma | Cell & Gene Therapy |
|--------|-------------------|---------------------|
| **Dosing** | Multiple doses | Often single dose (curative intent) |
| **Follow-up** | 6-24 months | 5-15 years (FDA mandated) |
| **Manufacturing** | Batch production | Patient-specific (autologous) |
| **Safety Focus** | Standard AE monitoring | Gene expression, insertional mutagenesis |

---

## CAR-T Therapy

### Treatment Journey

```
Leukapheresis (Day -14) → Manufacturing (2-4 weeks) → 
Lymphodepletion (Day -5 to -3) → CAR-T Infusion (Day 0) → 
CRS/ICANS Monitoring (Day 1-28) → Response Assessment (Day 28+) →
Long-Term Follow-Up (15 years)
```

### CRS Grading

| Grade | Symptoms | Intervention |
|-------|----------|--------------|
| **1** | Fever only (≥38°C) | Supportive care |
| **2** | Fever + hypotension (responds to fluids) | Tocilizumab ± steroids |
| **3** | Fever + hypotension (requires vasopressor) | ICU, tocilizumab + steroids |
| **4** | Life-threatening | ICU, aggressive intervention |

### ICANS Grading

| Grade | ICE Score | Clinical Features |
|-------|-----------|-------------------|
| **1** | 7-9 | Mild confusion |
| **2** | 3-6 | Moderate confusion |
| **3** | 0-2 | Severe confusion, seizures |
| **4** | 0 | Coma, cerebral edema |


---

## Long-Term Follow-Up (LTFU)

### FDA Requirements

| Vector Type | LTFU Duration |
|-------------|---------------|
| Integrating (lenti/retro) | 15 years |
| Non-integrating (AAV) | 5 years minimum |
| Gene-edited products | 15 years |

### LTFU Visit Schedule

| Period | Frequency | Assessments |
|--------|-----------|-------------|
| Year 1 | Monthly → Quarterly | Clinical, labs, expression, safety |
| Year 2 | Quarterly | Clinical, labs, expression |
| Years 3-5 | Every 6 months | Clinical, safety, basic labs |
| Years 6-15 | Annually | Questionnaire, malignancy screening |

---

## Generation Patterns

### CAR-T Response Data

```json
{
  "response_assessment": {
    "subject_id": "CAR-001-0015",
    "indication": "RELAPSED_DLBCL",
    "infusion_date": "2024-06-05",
    "assessment_timepoint": "DAY28",
    "response": {
      "overall_response": "COMPLETE_RESPONSE",
      "pet_ct_result": "DEAUVILLE_2"
    },
    "car_t_persistence": {
      "car_positive_cells_per_ul": 125,
      "peak_expansion_date": "2024-06-15",
      "peak_car_cells_per_ul": 2450
    }
  }
}
```

### CRS Event

```json
{
  "crs_event": {
    "subject_id": "CAR-001-0015",
    "onset_day": 2,
    "max_grade": 2,
    "duration_days": 5,
    "symptoms": {
      "fever_max_c": 39.8,
      "hypotension": true,
      "hypoxia": false
    },
    "interventions": [
      {"medication": "TOCILIZUMAB", "dose": "8 mg/kg"}
    ],
    "biomarkers": {
      "peak_crp": 285,
      "peak_ferritin": 12500,
      "peak_il6": 890
    },
    "outcome": "RESOLVED"
  }
}
```

---

## Validation Checklist

- [ ] Leukapheresis data complete (for autologous)
- [ ] Manufacturing lot documentation
- [ ] CRS grading per ASTCT consensus
- [ ] ICANS grading per ASTCT consensus
- [ ] LTFU visits scheduled per FDA guidance
- [ ] Gene expression assays at required timepoints

---

## Related Skills

**TrialSim:**
- [Clinical Trials Domain](../clinical-trials-domain.md) - Core trial concepts
- [Oncology](oncology.md) - CAR-T for hematologic malignancies, solid tumor patterns

**Cross-Product (PatientSim):**
- [PatientSim Oncology](../../patientsim/oncology/) - Cancer clinical care pathways (CAR-T often follows failed chemotherapy)

> **Integration Pattern:** CGT trials have unique patterns (single-dose, long-term follow-up, CRS/ICANS monitoring). Use PatientSim oncology for the pre-CGT clinical journey, then apply this skill for CGT-specific trial endpoints.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-12 | Initial Cell & Gene Therapy skill |
