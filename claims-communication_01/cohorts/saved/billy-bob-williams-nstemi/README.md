# Billy Bob Williams - NSTEMI Cardiac Episode

## Scenario Overview

| Element | Value |
|---------|-------|
| **Patient** | Billy Bob Williams |
| **Age** | 65 years |
| **DOB** | March 22, 1959 |
| **MRN** | MRN00000072 |
| **Encounter** | ENC20241210000001 |
| **Episode** | NSTEMI → Cardiac Cath → PCI with DES |
| **Date Range** | December 10-13, 2024 |

## Clinical Summary

65-year-old male with extensive cardiac risk factors (HTN, DM2, HLD, active smoking, obesity, family history) presenting via EMS with classic NSTEMI symptoms. Emergent cardiac catheterization revealed culprit lesion in proximal LCx (95% stenosis) successfully treated with drug-eluting stent.

### Risk Profile (TIMI Score: 6/7 - High Risk)

| Risk Factor | Status |
|-------------|--------|
| Age ≥65 | ✓ |
| ≥3 CAD risk factors | ✓ (HTN, DM, HLD, smoking, family hx, obesity) |
| Prior coronary stenosis ≥50% | New diagnosis |
| ST deviation | ✓ (1.5-2mm depression V3-V6) |
| ≥2 anginal events in 24h | ✓ |
| Elevated cardiac markers | ✓ (Troponin 0.89 → 8.21 ng/mL) |
| Aspirin use in prior 7 days | ✓ |

### Timeline

| Date/Time | Event |
|-----------|-------|
| Dec 10, 00:15 | Symptom onset at home |
| Dec 10, 02:15 | EMS arrival at ED |
| Dec 10, 02:25 | Initial EKG: ST depression V3-V6 |
| Dec 10, 02:30 | Troponin I: 0.89 ng/mL (elevated) |
| Dec 10, 03:15 | Cardiology consult, cath scheduled |
| Dec 10, 04:00 | Transfer to CCU |
| Dec 10, 08:30 | Cardiac catheterization |
| Dec 10, 09:15 | PCI with DES to LCx |
| Dec 11, 14:00 | Transfer to cardiac step-down |
| Dec 13, 11:00 | Discharge home |

## Diagnoses

| ICD-10 | Description | Type |
|--------|-------------|------|
| I21.4 | Non-ST elevation myocardial infarction | Principal |
| I25.10 | Atherosclerotic heart disease of native coronary artery | Secondary |
| I50.9 | Heart failure, unspecified | Secondary |
| I10 | Essential hypertension | Comorbid |
| E11.9 | Type 2 diabetes mellitus | Comorbid |
| E78.5 | Hyperlipidemia | Comorbid |
| N18.3 | Chronic kidney disease, stage 3 | Comorbid |
| F17.210 | Nicotine dependence, cigarettes | Comorbid |
| E66.9 | Obesity | Comorbid |

## Cardiac Catheterization Findings

| Vessel | Stenosis | Intervention |
|--------|----------|--------------|
| Left Main | 20% | None |
| LAD (mid) | 70% | Medical management |
| **LCx (proximal)** | **95% (culprit)** | **DES (Xience 3.0x18mm)** |
| RCA (mid) | 40% | None |

**Post-PCI Result**: 0% residual stenosis, TIMI 3 flow

**LV Function**: EF 35-40% with lateral/anterolateral hypokinesis

## Procedures

| Code | System | Description |
|------|--------|-------------|
| 92928 | CPT | Percutaneous coronary intervention with drug-eluting stent |
| 93458 | CPT | Left heart catheterization with coronary angiography |
| 02703ZZ | ICD-10-PCS | Dilation of coronary artery with intraluminal device |

## Insurance Coverage

### Primary: Medicare Part A/B

| Field | Value |
|-------|-------|
| **Member ID** | 1EG4TE5MK72 |
| **Coverage** | Medicare FFS |
| **Part A Deductible (2024)** | $1,632 |

### Secondary: AARP Medigap Plan F

| Field | Value |
|-------|-------|
| **Member ID** | MGF98765432 |
| **Coverage** | Covers Part A deductible |

## Financial Summary

### Hospital Stay (DRG-Based Payment)

| Item | Amount |
|------|--------|
| Total Hospital Charges | $78,500.00 |
| MS-DRG 247 Weight | 2.1893 |
| Medicare DRG Payment | $15,245.00 |
| Part A Deductible | $1,632.00 |
| Medigap Payment | $1,632.00 |
| **Patient Responsibility** | **$0.00** |

### Discharge Medications (Part D)

| Medication | Days | Cost | Patient Pay |
|------------|------|------|-------------|
| Ticagrelor 90mg | 30 | $427.50 | $47.00 |
| Atorvastatin 80mg | 30 | $15.00 | $0.00 |
| Metoprolol ER 100mg | 30 | $20.50 | $0.00 |
| Pantoprazole 40mg | 30 | $11.00 | $0.00 |
| Nitroglycerin SL | 25 | $44.50 | $8.00 |
| **Total** | | **$518.50** | **$55.00** |

### Episode Total Patient Out-of-Pocket: **$55.00**

## Files in This Scenario

| File | Format | Description |
|------|--------|-------------|
| `patient.json` | JSON | Complete clinical data including cath findings |
| `adt-a01-admission.hl7` | HL7v2.5 | ED admission message |
| `adt-a02-transfer-ccu.hl7` | HL7v2.5 | Transfer to CCU |
| `adt-a03-discharge.hl7` | HL7v2.5 | Discharge with final diagnoses |
| `claim-837i.edi` | X12 837I | Institutional claim (Medicare) |
| `claims.json` | JSON | Claims with DRG adjudication |
| `pharmacy-claims.json` | JSON | Discharge medication claims |

## Key Clinical Points

- **DAPT Duration**: Ticagrelor + Aspirin for minimum 12 months post-DES
- **High-Intensity Statin**: Atorvastatin 80mg per ACC/AHA guidelines post-ACS
- **Beta-Blocker**: Metoprolol for post-MI cardioprotection and reduced EF
- **Smoking Cessation**: Critical intervention - patient counseled
- **Cardiac Rehab**: Referral placed for Phase 2 rehabilitation
- **Follow-up**: Cardiology in 2 weeks, consider repeat echo in 3 months

## Data Relationships

```
Patient (Billy Bob Williams, MRN00000072)
    │
    ├── ED Encounter (Dec 10, 02:15)
    │       ├── EKG (ST depression)
    │       ├── Labs (Troponin series)
    │       ├── Bedside echo
    │       └── ADT A01 → Admission
    │
    ├── CCU Stay (Dec 10-11)
    │       ├── ADT A02 → Transfer
    │       ├── Cath Lab (08:30)
    │       │     ├── LHC (93458)
    │       │     └── PCI with DES (92928)
    │       └── Post-procedure monitoring
    │
    ├── Step-down Stay (Dec 11-13)
    │       ├── Telemetry monitoring
    │       ├── Cardiac rehab consult
    │       └── Discharge planning
    │
    ├── Discharge (Dec 13)
    │       ├── ADT A03 → Discharge
    │       ├── 837I Claim (DRG 247)
    │       └── Discharge medications
    │
    └── Pharmacy Claims
            ├── Ticagrelor (DAPT)
            ├── Atorvastatin (Statin)
            ├── Metoprolol (Beta-blocker)
            ├── Pantoprazole (GI protection)
            └── Nitroglycerin (PRN)
```

## Generated
- **Date**: December 18, 2024
- **Generator**: HealthSim
- **Scenario Type**: Cardiac Episode - ACS/NSTEMI
