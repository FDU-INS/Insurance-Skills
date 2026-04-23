# Miles Oswald - Pediatric ER Visit: Acute Otitis Media

## Scenario Overview

| Element | Value |
|---------|-------|
| **Patient** | Miles Oswald |
| **Age** | 4 years, 8 months |
| **DOB** | April 12, 2020 |
| **MRN** | MRN00000003 |
| **Encounter** | ENC20241218000001 |
| **Encounter Type** | Emergency Department |
| **Date** | December 18, 2024 |

## Clinical Summary

4-year-old male presenting to the ED with **acute otitis media (AOM)** of the right ear. Classic presentation with 2-day history of ear pain following URI, associated fever (101.4°F), and characteristic otoscopic findings (bulging, erythematous TM with purulent effusion).

### Chief Complaint
- Right ear pain × 2 days
- Fever

### Diagnoses
| ICD-10 | Description | Type |
|--------|-------------|------|
| H66.91 | Otitis media, unspecified, right ear | Principal |
| R50.9 | Fever, unspecified | Secondary |
| H92.01 | Otalgia, right ear | Secondary |

### Treatment
- **Amoxicillin** 400mg (5mL) PO BID × 10 days
- **Acetaminophen** 240mg (7.5mL) PO q4-6h PRN pain/fever

## Insurance Information

| Field | Value |
|-------|-------|
| **Payer** | Blue Cross Blue Shield of Illinois |
| **Member ID** | XYZ123456789 |
| **Group** | GRP00987 |
| **Plan Type** | PPO |
| **Subscriber** | Mark Oswald (Father) |

## Files in This Scenario

| File | Format | Description |
|------|--------|-------------|
| `patient.json` | JSON | Complete patient, encounter, clinical data |
| `adt-a04-registration.hl7` | HL7v2.5 | ED registration message |
| `adt-a03-discharge.hl7` | HL7v2.5 | Discharge message with final diagnoses |
| `claim-837p.edi` | X12 5010 | Professional claim for ED visit |
| `pharmacy-claim-ncpdp.json` | NCPDP D.0 | Pharmacy claim for amoxicillin |

## Professional Claim Details (837P)

| Service | CPT | Description | Charge |
|---------|-----|-------------|--------|
| Line 1 | 99283-25 | ED Visit Level 3, Moderate Severity | $175.00 |
| Line 2 | 92587 | Evoked otoacoustic emissions, limited | $85.00 |
| Line 3 | 96372 | Therapeutic injection (antipyretic) | $25.00 |
| | | **Total Charges** | **$285.00** |

## Pharmacy Claim Details (NCPDP)

| Field | Value |
|-------|-------|
| **NDC** | 00093-4157-01 |
| **Drug** | Amoxicillin 400mg/5mL Suspension |
| **Quantity** | 150 mL |
| **Days Supply** | 10 |
| **Ingredient Cost** | $12.50 |
| **Dispensing Fee** | $2.00 |
| **Patient Copay** | $10.00 |
| **Plan Paid** | $3.25 |

## Clinical Notes

### Physical Exam Findings
- **Right Ear**: TM erythematous and bulging, decreased mobility on pneumatic otoscopy, purulent effusion visible
- **Left Ear**: Normal TM, pearly gray, good mobility
- **General**: Alert, mildly fussy but consolable, no acute distress

### AAP Treatment Guidelines Applied
Per AAP guidelines for AOM:
- Age ≥2 years with unilateral AOM → antibiotic treatment appropriate
- High-dose amoxicillin (80-90 mg/kg/day) is first-line therapy
- 10-day course for children <2 years or with severe symptoms

## Data Relationships

```
Patient (Miles Oswald)
    │
    ├── Encounter (ENC20241218000001)
    │       │
    │       ├── ADT A04 → Registration
    │       ├── ADT A03 → Discharge
    │       └── 837P Claim → Professional billing
    │
    └── Prescription (RX20241218001)
            │
            └── NCPDP Claim → Pharmacy billing
```

## Generated
- **Date**: December 18, 2024
- **Generator**: HealthSim
- **Scenario Type**: Pediatric Emergency
