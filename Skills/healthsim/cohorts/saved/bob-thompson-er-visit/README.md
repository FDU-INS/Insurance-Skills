# Bob Thompson - ER Visit (Wrist Fracture)

## Scenario Overview

| Element | Value |
|---------|-------|
| **Patient** | Bob Thompson |
| **Age** | 46 years |
| **DOB** | April 22, 1978 |
| **Person ID** | PER-20251226-001 |
| **Member ID** | MBR-WI-78042201 |
| **MRN** | MRN-MAD-20251226 |
| **Episode** | ER visit for wrist fracture after fall on ice |
| **Date** | December 26, 2024 |

## Cross-Product Journey

This scenario demonstrates cross-product integration:

1. **MemberSim**: Bob is enrolled in Anthem Blue Cross Wisconsin (Gold PPO)
2. **PatientSim**: Bob visits the ER with a wrist injury
3. **MemberSim**: Professional claim generated and adjudicated

### Identity Correlation

| Product | Entity | ID | Correlator |
|---------|--------|-----|------------|
| Core | Person | PER-20251226-001 | SSN: 555-12-3456 |
| MemberSim | Member | MBR-WI-78042201 | person_id |
| PatientSim | Patient | PAT-20251226-001 | person_id |

## Clinical Summary

**Chief Complaint**: Left wrist pain after fall on ice

**Diagnoses**:
- S62.102A - Fracture of unspecified carpal bone, left wrist
- W00.0XXA - Fall on same level due to ice and snow

**Procedures**:
- 73110 - X-ray wrist, complete (3 views)
- 29125 - Application of short arm splint

**Disposition**: Discharged to home with orthopedic follow-up

## Financial Summary

| Field | Amount |
|-------|--------|
| Total Billed | $860.00 |
| Total Allowed | $715.00 |
| Plan Paid | $372.00 |
| Patient Responsibility | $343.00 |

### Patient Responsibility Breakdown
- Deductible applied: $175.00
- ER Copay: $250.00 (included in line 1)
- Coinsurance: $108.00

## Files

| File | Content |
|------|---------|
| `person.json` | Base person demographics |
| `member.json` | Health plan enrollment |
| `patient.json` | Clinical patient record |
| `encounter.json` | ER visit, diagnoses, procedures |
| `claim.json` | Professional claim with adjudication |

## Generated

- **Date**: December 26, 2024
- **Generator**: HealthSim
- **Scenario Type**: Cross-Product (MemberSim + PatientSim)
- **Storage**: JSON + DuckDB
