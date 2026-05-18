# X12 834 Benefit Enrollment Transaction - Explained

This document explains the 834 EDI transaction for the Oswald Family enrollment, segment by segment.

## Overview

The **X12 834** is the HIPAA-mandated format for transmitting benefit enrollment and maintenance information between employers, health plans, and third-party administrators.

**Transaction Set**: 834 (Benefit Enrollment and Maintenance)  
**Version**: 005010X220A1  
**Purpose**: Initial enrollment for a family of 5 in Aetna Platinum PPO

---

## Transaction Structure

```
┌─────────────────────────────────────────────────────────────┐
│  ENVELOPE (ISA/IEA)                                         │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  FUNCTIONAL GROUP (GS/GE)                             │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │  TRANSACTION SET (ST/SE)                        │  │  │
│  │  │  ┌───────────────────────────────────────────┐  │  │  │
│  │  │  │  Header (BGN, REF, DTP, N1)               │  │  │  │
│  │  │  ├───────────────────────────────────────────┤  │  │  │
│  │  │  │  Member Loop 1 (Subscriber - Mark)        │  │  │  │
│  │  │  │    INS, REF, DTP, NM1, PER, N3, N4, DMG   │  │  │  │
│  │  │  │    HD, DTP, LX, NM1 (PCP)                 │  │  │  │
│  │  │  ├───────────────────────────────────────────┤  │  │  │
│  │  │  │  Member Loop 2 (Spouse - Karen)           │  │  │  │
│  │  │  ├───────────────────────────────────────────┤  │  │  │
│  │  │  │  Member Loop 3 (Child - Gracie)           │  │  │  │
│  │  │  ├───────────────────────────────────────────┤  │  │  │
│  │  │  │  Member Loop 4 (Child - Emmy)             │  │  │  │
│  │  │  ├───────────────────────────────────────────┤  │  │  │
│  │  │  │  Member Loop 5 (Child - Miles)            │  │  │  │
│  │  │  └───────────────────────────────────────────┘  │  │  │
│  │  └─────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## Segment-by-Segment Explanation

### Interchange Envelope

```
ISA*00*          *00*          *ZZ*SENDER         *ZZ*60054          *250101*1200*^*00501*000001847*0*P*:~
```

| Element | Value | Meaning |
|---------|-------|---------|
| ISA01 | 00 | No authorization info |
| ISA02 | (blank) | Authorization info (not used) |
| ISA03 | 00 | No security info |
| ISA04 | (blank) | Security info (not used) |
| ISA05 | ZZ | Sender ID qualifier (mutually defined) |
| ISA06 | SENDER | Sender ID |
| ISA07 | ZZ | Receiver ID qualifier |
| ISA08 | 60054 | Receiver ID (Aetna payer ID) |
| ISA09 | 250101 | Date (YYMMDD) |
| ISA10 | 1200 | Time (HHMM) |
| ISA11 | ^ | Repetition separator |
| ISA12 | 00501 | Interchange version |
| ISA13 | 000001847 | Interchange control number |
| ISA14 | 0 | No acknowledgment requested |
| ISA15 | P | Production data |
| ISA16 | : | Sub-element separator |

### Functional Group Header

```
GS*BE*SENDER*60054*20250101*1200*1847*X*005010X220A1~
```

| Element | Value | Meaning |
|---------|-------|---------|
| GS01 | BE | Benefit Enrollment |
| GS02 | SENDER | Sender application code |
| GS03 | 60054 | Receiver application code |
| GS04 | 20250101 | Date (CCYYMMDD) |
| GS05 | 1200 | Time |
| GS06 | 1847 | Group control number |
| GS07 | X | Version identifier |
| GS08 | 005010X220A1 | Implementation guide version |

### Transaction Set Header

```
ST*834*0001*005010X220A1~
```

| Element | Value | Meaning |
|---------|-------|---------|
| ST01 | 834 | Transaction set identifier |
| ST02 | 0001 | Transaction set control number |
| ST03 | 005010X220A1 | Implementation version |

### Beginning Segment

```
BGN*00*ENR20250001847*20250101*1200****2~
```

| Element | Value | Meaning |
|---------|-------|---------|
| BGN01 | 00 | Original transaction |
| BGN02 | ENR20250001847 | Reference ID |
| BGN03 | 20250101 | Transaction date |
| BGN04 | 1200 | Transaction time |
| BGN08 | 2 | Action code: Change (initial enrollment is a "change" from no coverage) |

### Reference Information

```
REF*38*847291~
```

| Element | Value | Meaning |
|---------|-------|---------|
| REF01 | 38 | Master policy number |
| REF02 | 847291 | Group number |

### Date/Time Reference

```
DTP*007*D8*20250101~
```

| Element | Value | Meaning |
|---------|-------|---------|
| DTP01 | 007 | Effective date |
| DTP02 | D8 | Date format (CCYYMMDD) |
| DTP03 | 20250101 | January 1, 2025 |

### Sponsor/Payer Names

```
N1*P5*AETNA*FI*60054~
N1*IN*OSWALD FAMILY*94*AET847291001~
```

| Segment | N101 | Meaning |
|---------|------|---------|
| First N1 | P5 | Plan sponsor (Aetna) |
| Second N1 | IN | Insured (family unit) |

---

## Member Loop: Subscriber (Mark Oswald)

### Insurance Segment

```
INS*Y*18*021*28*A***FT~
```

| Element | Value | Meaning |
|---------|-------|---------|
| INS01 | Y | Yes, subscriber |
| INS02 | 18 | Self (subscriber relationship) |
| INS03 | 021 | Active coverage |
| INS04 | 28 | Initial enrollment |
| INS05 | A | Active status |
| INS08 | FT | Full-time employment |

### Member References

```
REF*0F*AET847291001~    (Member ID)
REF*1L*847291~          (Group number)
REF*23*AET-PPO-PLAT-2025~  (Plan ID)
```

### Coverage Dates

```
DTP*336*D8*20250101~    (Employment start)
DTP*348*D8*20250101~    (Benefit begin date)
```

### Member Name

```
NM1*IL*1*OSWALD*MARK****34*XXX-XX-4521~
```

| Element | Value | Meaning |
|---------|-------|---------|
| NM101 | IL | Insured/Subscriber |
| NM102 | 1 | Person (not organization) |
| NM103 | OSWALD | Last name |
| NM104 | MARK | First name |
| NM108 | 34 | SSN qualifier |
| NM109 | XXX-XX-4521 | SSN (masked) |

### Contact Information

```
PER*IP**TE*4155550147*EM*mark.oswald@email.com~
```

| Element | Value | Meaning |
|---------|-------|---------|
| PER01 | IP | Insured party |
| PER03 | TE | Telephone |
| PER04 | (number) | Phone number |
| PER05 | EM | Email |
| PER06 | (email) | Email address |

### Address

```
N3*1234 OAK STREET~
N4*SAN FRANCISCO*CA*94102~
```

### Demographics

```
DMG*D8*19750615*M~
```

| Element | Value | Meaning |
|---------|-------|---------|
| DMG01 | D8 | Date format |
| DMG02 | 19750615 | DOB: June 15, 1975 |
| DMG03 | M | Male |

### Health Coverage

```
HD*021**HLT*AET-PPO-PLAT-2025*FAM~
```

| Element | Value | Meaning |
|---------|-------|---------|
| HD01 | 021 | Health coverage |
| HD03 | HLT | Health |
| HD04 | AET-PPO-PLAT-2025 | Plan code |
| HD05 | FAM | Family coverage level |

### Primary Care Provider

```
LX*1~
NM1*P3*1*ARBABI*NASRIN****XX*1234567890~
N3*500 MEDICAL CENTER DRIVE*SUITE 210~
N4*SAN FRANCISCO*CA*94103~
PER*IC**TE*4155550200~
```

| Element | Value | Meaning |
|---------|-------|---------|
| LX01 | 1 | Provider loop sequence |
| NM101 | P3 | Primary care provider |
| NM108 | XX | NPI qualifier |
| NM109 | 1234567890 | NPI |

---

## Member Loop: Dependent (Example - Karen)

```
INS*N*01*021*28*A~
```

| Element | Value | Meaning |
|---------|-------|---------|
| INS01 | N | No, not subscriber (dependent) |
| INS02 | 01 | Spouse relationship |

The rest follows the same pattern as the subscriber.

---

## Member Loop: Child (Example - Gracie)

```
INS*N*19*021*28*A~
```

| Element | Value | Meaning |
|---------|-------|---------|
| INS02 | 19 | Child relationship |

Children are assigned a pediatric PCP (Dr. Torres) instead of the family medicine provider.

---

## Trailer Segments

### Transaction Set Trailer

```
SE*76*0001~
```

| Element | Value | Meaning |
|---------|-------|---------|
| SE01 | 76 | Segment count |
| SE02 | 0001 | Transaction set control number (matches ST02) |

### Functional Group Trailer

```
GE*1*1847~
```

| Element | Value | Meaning |
|---------|-------|---------|
| GE01 | 1 | Number of transaction sets |
| GE02 | 1847 | Group control number (matches GS06) |

### Interchange Trailer

```
IEA*1*000001847~
```

| Element | Value | Meaning |
|---------|-------|---------|
| IEA01 | 1 | Number of functional groups |
| IEA02 | 000001847 | Interchange control number (matches ISA13) |

---

## Key Code Values Reference

### Relationship Codes (INS02)

| Code | Relationship |
|------|--------------|
| 18 | Self (subscriber) |
| 01 | Spouse |
| 19 | Child |
| 17 | Stepchild |
| 23 | Domestic partner |
| 53 | Life partner |

### Maintenance Type Codes (INS03)

| Code | Meaning |
|------|---------|
| 001 | Change |
| 021 | Addition |
| 024 | Cancel |
| 025 | Reinstatement |
| 030 | Audit/compare |

### Maintenance Reason Codes (INS04)

| Code | Reason |
|------|--------|
| 28 | Initial enrollment |
| 01 | Divorce |
| 02 | Birth |
| 03 | Marriage |
| 07 | Termination of employment |
| 33 | Open enrollment |

---

## Data Flow Visualization

```
Employer/TPA                         Health Plan
    │                                    │
    │  ┌──────────────────────────┐      │
    │  │  834 Transaction         │      │
    │  │  - Family enrollment     │      │
    │  │  - 5 members             │      │
    │  │  - Plan: Platinum PPO    │      │
    │  │  - Effective: 2025-01-01 │      │
    │  └──────────────────────────┘      │
    │              │                     │
    ├──────────────┼─────────────────────┤
    │              ▼                     │
    │       EDI Translator               │
    │              │                     │
    │              ▼                     │
    │    Enrollment Database             │
    │              │                     │
    │              ▼                     │
    │    ┌─────────────────────┐         │
    │    │ Member Records      │         │
    │    │ - AET847291001 Mark │         │
    │    │ - AET847291002 Karen│         │
    │    │ - AET847291003 Gracie         │
    │    │ - AET847291004 Emmy │         │
    │    │ - AET847291005 Miles│         │
    │    └─────────────────────┘         │
    │              │                     │
    │              ▼                     │
    │    ID Cards Generated              │
    │    Eligibility Active              │
    │                                    │
```

---

*Reference: ASC X12 005010X220A1 Implementation Guide*
