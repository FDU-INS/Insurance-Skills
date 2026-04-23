# Mark Oswald - Colorectal Cancer Screening & Treatment

## Scenario Overview

| Element | Value |
|---------|-------|
| **Patient** | Mark Oswald |
| **Age** | 58 years |
| **DOB** | September 15, 1966 |
| **MRN** | MRN00000058 |
| **Episode** | Colorectal cancer screening → diagnosis → surgical treatment |
| **Date Range** | October 15, 2024 - November 20, 2024 |

## Clinical Journey

This scenario follows a 58-year-old male through routine colorectal cancer screening that leads to discovery of adenomatous polyps, subsequent diagnosis of early-stage colon cancer, and surgical treatment with excellent prognosis.

### Timeline

| Date | Event | Encounter |
|------|-------|-----------|
| Oct 15, 2024 | Screening colonoscopy | ENC20241015000001 |
| Oct 18, 2024 | Pathology results received | — |
| Oct 25, 2024 | Surgical consultation | ENC20241025000001 |
| Oct 28, 2024 | Pre-op CT scan & labs | — |
| Nov 5-8, 2024 | Laparoscopic right hemicolectomy (3-day stay) | ENC20241105000001 |
| Nov 8, 2024 | Surgical pathology: Stage I adenocarcinoma | — |
| Nov 20, 2024 | Oncology follow-up | ENC20241120000001 |

### Clinical Progression

1. **Screening**: Routine colonoscopy for average-risk screening with positive family history (father with colon cancer at 62)
2. **Findings**: Two polyps removed - 8mm tubulovillous adenoma with high-grade dysplasia (ascending colon) and 4mm tubular adenoma (sigmoid)
3. **Escalation**: High-grade dysplasia with unclear margins → surgical referral
4. **Pre-op workup**: CT negative for metastatic disease, CEA normal (2.1)
5. **Surgery**: Laparoscopic right hemicolectomy, uncomplicated
6. **Final pathology**: pT1N0M0 adenocarcinoma, Stage I, MSS, KRAS/BRAF wild-type
7. **Prognosis**: >95% 5-year survival, surveillance only (no adjuvant chemo)

## Diagnosis Codes

| ICD-10 | Description | Context |
|--------|-------------|---------|
| Z12.11 | Encounter for screening for malignant neoplasm of colon | Initial screening |
| Z80.42 | Family history of malignant neoplasm of colon | Risk factor |
| D12.2 | Benign neoplasm of ascending colon | Post-colonoscopy |
| D12.5 | Benign neoplasm of sigmoid colon | Post-colonoscopy |
| C18.2 | Malignant neoplasm of ascending colon | Final surgical pathology |
| Z85.038 | Personal history of malignant neoplasm of ascending colon | Surveillance |

## Procedure Codes

| Code | System | Description |
|------|--------|-------------|
| 45385 | CPT | Colonoscopy with snare polypectomy |
| 45380 | CPT | Colonoscopy with biopsy |
| 44204 | CPT | Laparoscopic right hemicolectomy |
| 0DBK4ZZ | ICD-10-PCS | Excision of ascending colon, percutaneous endoscopic |

## Insurance & Financial

| Field | Value |
|-------|-------|
| **Payer** | Blue Cross Blue Shield of Illinois |
| **Member ID** | XYZ123456789 |
| **Group** | GRP00987 |
| **Plan Type** | PPO |
| **Individual Deductible** | $1,500 (fully met) |
| **Individual OOP Max** | $6,000 |

### Episode Financial Summary

| Claim | Service | Charges | Allowed | Patient | Plan Paid |
|-------|---------|---------|---------|---------|-----------|
| Colonoscopy | Oct 15 | $1,850 | $1,425 | $625 | $800 |
| Surgical Consult | Oct 25 | $350 | $275 | $275 | $0 |
| Inpatient Surgery | Nov 5-8 | $52,300 | $38,500 | $8,340 | $30,160 |
| **Total** | | **$54,500** | **$40,200** | **$9,240** | **$30,960** |

### Accumulator Status (as of Nov 8)

| Accumulator | Limit | Applied | Remaining |
|-------------|-------|---------|-----------|
| Individual Deductible | $1,500 | $1,500 | $0 |
| Individual OOP Max | $6,000 | $4,250 | $1,750 |

## Files in This Scenario

| File | Format | Description |
|------|--------|-------------|
| `patient.json` | JSON | Complete patient, clinical, and encounter data |
| `adt-a01-admission.hl7` | HL7v2.5 | Surgical admission message |
| `adt-a03-discharge.hl7` | HL7v2.5 | Discharge with final diagnoses |
| `claim-837p-colonoscopy.edi` | X12 837P | Professional claim - colonoscopy |
| `claim-837i-surgery.edi` | X12 837I | Institutional claim - surgery |
| `claims.json` | JSON | All claims with adjudication details |

## Key Clinical Points

- **Screening interval**: With family history, colonoscopy recommended at age 50 or 10 years before youngest affected relative
- **Treatment decision**: High-grade dysplasia + incomplete margins = surgical resection recommended
- **Staging**: pT1N0M0 = tumor confined to submucosa, no lymph node involvement
- **MSS status**: Microsatellite stable tumors don't respond to immunotherapy
- **Surveillance**: Per NCCN guidelines - CEA q3-6mo, CT annually, colonoscopy at 1 year

## Data Relationships

```
Patient (Mark Oswald, MRN00000058)
    │
    ├── Screening Encounter (Oct 15)
    │       ├── Colonoscopy procedure
    │       ├── Pathology specimens
    │       └── 837P Claim
    │
    ├── Surgical Consult (Oct 25)
    │       └── Professional claim
    │
    ├── Pre-op Workup (Oct 28)
    │       ├── CT scan
    │       └── Labs (CEA, CBC, CMP)
    │
    ├── Surgical Admission (Nov 5-8)
    │       ├── ADT A01 → Admission
    │       ├── OR Procedure
    │       ├── Surgical pathology
    │       ├── ADT A03 → Discharge
    │       └── 837I Claim (DRG 329)
    │
    └── Oncology Follow-up (Nov 20)
            └── Surveillance plan established
```

## Generated
- **Date**: December 18, 2024
- **Generator**: HealthSim
- **Scenario Type**: Oncology Episode
