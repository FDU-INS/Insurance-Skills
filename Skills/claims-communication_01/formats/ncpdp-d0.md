# NCPDP Telecommunication Standard (D.0) Format

## Trigger Phrases

- NCPDP
- NCPDP D.0
- pharmacy claim format
- pharmacy transaction
- B1 claim
- B2 reversal
- pharmacy EDI

## Overview

NCPDP Telecommunication Standard (D.0) is the standard for real-time pharmacy claim transactions. This skill transforms HealthSim pharmacy entities into compliant NCPDP transactions.

## Transaction Codes

| Code | Name | Description |
|------|------|-------------|
| B1 | Billing | New claim submission |
| B2 | Reversal | Cancel previous claim |
| B3 | Rebill | Correct and resubmit |
| E1 | Eligibility Verification | Check coverage |
| P1 | Prior Authorization Request | Submit PA |
| P2 | Prior Authorization Inquiry | Check PA status |
| P4 | Prior Authorization Cancel | Cancel PA |

## Message Structure

### Request Structure
```
Header
  Transmission Header Segment
  Patient Segment
  Insurance Segment
  Claim Segment
  Prescriber Segment
  COB Segment (if applicable)
  Pricing Segment
  DUR/PPS Segment (if applicable)
  Prior Authorization Segment (if applicable)
```

### Response Structure
```
Header
  Response Header Segment
  Response Message Segment
  Response Status Segment
  Response Claim Segment
  Response Pricing Segment
  Response DUR/PPS Segment
```

## Segment Definitions

### Transmission Header Segment
| Field ID | Field Name | Length | Example |
|----------|------------|--------|---------|
| 101-A1 | BIN Number | 6 | `610014` |
| 102-A2 | Version/Release | 2 | `D0` |
| 103-A3 | Transaction Code | 2 | `B1` |
| 104-A4 | Processor Control Number | 10 | `RXGROUP` |
| 109-A9 | Transaction Count | 1 | `1` |
| 110-AK | Software Vendor/Certification ID | 10 | `HEALTHSIM` |

### Patient Segment (Segment ID: 01)
| Field ID | Field Name | Format | Example |
|----------|------------|--------|---------|
| 1Ø1-C1 | Patient ID Qualifier | 2 | `01` |
| 332-CY | Patient ID | AN | `MEM001234` |
| 304-C4 | Date of Birth | D8 | `19780315` |
| 305-C5 | Patient Gender Code | 1 | `1` (Male), `2` (Female) |
| 310-CA | Patient First Name | AN | `JOHN` |
| 311-CB | Patient Last Name | AN | `SMITH` |
| 322-CM | Patient Street Address | AN | `123 MAIN ST` |
| 323-CN | Patient City | AN | `SPRINGFIELD` |
| 324-CO | Patient State | 2 | `IL` |
| 325-CP | Patient Zip Code | 15 | `627010000` |

### Insurance Segment (Segment ID: 04)
| Field ID | Field Name | Format | Example |
|----------|------------|--------|---------|
| 302-C2 | Cardholder ID | AN | `001234001` |
| 301-C1 | Group ID | AN | `CORP001` |
| 303-C3 | Person Code | 3 | `001` |
| 306-C6 | Patient Relationship Code | 1 | `1` |
| 312-CC | Cardholder First Name | AN | `JOHN` |
| 313-CD | Cardholder Last Name | AN | `SMITH` |

### Claim Segment (Segment ID: 07)
| Field ID | Field Name | Format | Example |
|----------|------------|--------|---------|
| 455-EM | Prescription/Service Ref # Qualifier | 1 | `1` |
| 402-D2 | Prescription/Service Reference # | AN | `RX78901234` |
| 436-E1 | Product/Service ID Qualifier | 2 | `03` (NDC) |
| 407-D7 | Product/Service ID | 19 | `00093505601` |
| 442-E7 | Quantity Dispensed | 10 | `30.000` |
| 405-D5 | Days Supply | 3 | `030` |
| 406-D6 | Compound Code | 1 | `1` (Not compound) |
| 408-D8 | Dispense as Written (DAW) Code | 1 | `0` |
| 414-DE | Date Prescription Written | D8 | `20250110` |
| 415-DF | Number of Refills Authorized | 2 | `05` |
| 419-DJ | Prescription Origin Code | 1 | `1` (Written) |
| 403-D3 | Fill Number | 2 | `00` |

### Prescriber Segment (Segment ID: 03)
| Field ID | Field Name | Format | Example |
|----------|------------|--------|---------|
| 466-EZ | Prescriber ID Qualifier | 2 | `01` (NPI) |
| 411-DB | Prescriber ID | 15 | `1234567890` |
| 427-DR | Prescriber Last Name | AN | `SMITH` |
| 364-2J | Prescriber First Name | AN | `JOHN` |
| 465-EY | Prescriber Phone Number | 10 | `5551234567` |

### Pricing Segment (Segment ID: 11)
| Field ID | Field Name | Format | Example |
|----------|------------|--------|---------|
| 409-D9 | Ingredient Cost Submitted | $$$$$$$cc | `0000850` |
| 412-DC | Dispensing Fee Submitted | $$$$$cc | `000200` |
| 426-DQ | Usual and Customary Charge | $$$$$$$cc | `0001500` |
| 430-DU | Gross Amount Due | $$$$$$$cc | `0001050` |
| 423-DN | Basis of Cost Determination | 2 | `01` (AWP) |

### DUR/PPS Segment (Segment ID: 08)
| Field ID | Field Name | Format | Example |
|----------|------------|--------|---------|
| 473-7E | DUR/PPS Code Counter | 2 | `01` |
| 439-E4 | Reason for Service Code | 2 | `ER` |
| 440-E5 | Professional Service Code | 2 | `M0` |
| 441-E6 | Result of Service Code | 2 | `1A` |
| 474-8E | DUR/PPS Level of Effort | 2 | `11` |

### DUR Reason for Service Codes (439-E4)
| Code | Description |
|------|-------------|
| AD | Additional Drug Needed |
| AR | Adverse Drug Reaction |
| DD | Drug-Drug Interaction |
| ER | Early Refill |
| HD | High Dose |
| LD | Low Dose |
| MC | Drug-Disease Contraindication |
| MN | Insufficient Duration |
| MX | Excessive Duration |
| PA | Drug-Age Precaution |
| PG | Drug-Pregnancy Precaution |
| TD | Therapeutic Duplication |

## Response Segments

### Response Status Segment (Segment ID: 21)
| Field ID | Field Name | Format | Example |
|----------|------------|--------|---------|
| 501-F1 | Transaction Response Status | 1 | `A` (Accepted) |
| 112-AN | Authorization Number | AN | `AUTH001234` |

### Response Status Codes (501-F1)
| Code | Description |
|------|-------------|
| A | Accepted |
| C | Captured (Deferred) |
| D | Duplicate of Paid |
| P | Paid |
| R | Rejected |

### Response Reject Segment (Segment ID: 24)
| Field ID | Field Name | Format | Example |
|----------|------------|--------|---------|
| 510-FA | Reject Count | 2 | `01` |
| 511-FB | Reject Code | 3 | `075` |
| 546-4F | Reject Field Occurrence Indicator | AN | |

### Response Pricing Segment (Segment ID: 23)
| Field ID | Field Name | Format | Example |
|----------|------------|--------|---------|
| 505-F5 | Patient Pay Amount | $$$$$$$cc | `0001000` |
| 506-F6 | Ingredient Cost Paid | $$$$$$$cc | `0000850` |
| 507-F7 | Dispensing Fee Paid | $$$$$$$cc | `000175` |
| 509-F9 | Total Amount Paid | $$$$$$$cc | `0000025` |
| 518-FI | Copay Amount | $$$$$cc | `001000` |
| 577-G3 | Coinsurance Amount | $$$$$cc | |
| 575-G1 | Deductible Amount | $$$$$cc | |

### Response DUR/PPS Segment (Segment ID: 28)
| Field ID | Field Name | Format | Example |
|----------|------------|--------|---------|
| 567-FY | DUR Response Code Counter | 2 | `01` |
| 439-E4 | Reason for Service Code | 2 | `ER` |
| 528-FS | Clinical Significance Code | 1 | `2` |
| 529-FT | Other Pharmacy Indicator | 1 | `N` |
| 530-FU | Previous Date of Fill | D8 | `20241227` |
| 531-FV | Quantity of Previous Fill | 10 | `30.000` |
| 532-FW | Database Indicator | 1 | `1` |
| 533-FX | Other Prescriber Indicator | 1 | `N` |
| 544-FE | DUR Free Text Message | AN | `REFILL 8 DAYS EARLY` |

## Example Transactions

### B1 Billing Request (Formatted)
```
Header:
  BIN: 610014
  Version: D0
  Transaction Code: B1
  PCN: RXGROUP

Patient:
  Patient ID: MEM001234
  DOB: 19780315
  Gender: 1 (Male)
  Name: JOHN SMITH

Insurance:
  Cardholder ID: 001234001
  Group ID: CORP001
  Person Code: 001
  Relationship: 1 (Cardholder)

Claim:
  Rx Number: RX78901234
  NDC: 00093505601
  Quantity: 30.000
  Days Supply: 30
  DAW: 0
  Fill Number: 0
  Written Date: 20250110
  Refills Authorized: 5

Prescriber:
  NPI: 1234567890
  Name: DR JOHN SMITH

Pricing:
  Ingredient Cost: $8.50
  Dispensing Fee: $2.00
  U&C Charge: $15.00
  Gross Amount Due: $10.50
```

### Paid Response
```
Response Status:
  Status: P (Paid)
  Authorization: AUTH20250115001

Pricing:
  Patient Pay: $10.00
  Ingredient Cost Paid: $8.50
  Dispensing Fee Paid: $1.75
  Total Amount Paid: $0.25
  Copay: $10.00

Message:
  Message: CLAIM ACCEPTED
```

### Rejected Response (PA Required)
```
Response Status:
  Status: R (Rejected)

Reject:
  Reject Count: 1
  Reject Code: 75
  Reject Message: PRIOR AUTHORIZATION REQUIRED

Additional Message:
  Submit PA request with diagnosis documentation
  PA Phone: 1-800-555-0123
```

### Response with DUR Alert
```
Response Status:
  Status: P (Paid)
  Authorization: AUTH20250115002

DUR Response:
  Alert Count: 1
  Reason Code: ER (Early Refill)
  Significance: 2 (Moderate)
  Previous Fill: 20241227
  Previous Qty: 30.000
  Message: REFILL 8 DAYS EARLY - 73% SUPPLY USED

Pricing:
  Patient Pay: $10.00
  Total Paid: $0.25
```

## Common Reject Codes

| Code | Description |
|------|-------------|
| 01 | Missing/Invalid BIN Number |
| 06 | Missing/Invalid Group ID |
| 07 | Missing/Invalid Cardholder ID |
| 19 | Missing/Invalid Days Supply |
| 25 | Missing/Invalid Prescriber ID |
| 70 | Product/Service Not Covered |
| 75 | Prior Authorization Required |
| 76 | Plan Limitations Exceeded |
| 79 | Refill Too Soon |
| 80 | Prescriber Not Found |
| 83 | Duplicate Paid/Captured Claim |
| 88 | DUR Reject Error |

## Transformation from JSON

### Input (HealthSim Pharmacy Claim)
```json
{
  "claim": {
    "claim_id": "RX20250115000001",
    "transaction_code": "B1",
    "bin": "610014",
    "pcn": "RXGROUP",
    "member_id": "MEM001234",
    "cardholder_id": "001234001",
    "group_number": "CORP001",
    "ndc": "00093505601",
    "quantity_dispensed": 30,
    "days_supply": 30,
    "prescriber_npi": "1234567890",
    "ingredient_cost_submitted": 8.50,
    "dispensing_fee_submitted": 2.00
  }
}
```

### Output (NCPDP Fields)
```
101-A1: 610014
102-A2: D0
103-A3: B1
104-A4: RXGROUP
332-CY: MEM001234
302-C2: 001234001
301-C1: CORP001
407-D7: 00093505601
442-E7: 30.000
405-D5: 030
411-DB: 1234567890
409-D9: 0000850
412-DC: 000200
```

## Validation Rules

1. **BIN**: Must be 6 numeric digits
2. **NDC**: Must be 11 digits (5-4-2 format)
3. **NPI**: Must be 10 digits with valid check digit
4. **Quantity**: Must be positive decimal
5. **Days Supply**: Must be 1-999
6. **Date Format**: CCYYMMDD
7. **DAW Code**: Must be 0-9

## Related Skills

- [../skills/rxmembersim/retail-pharmacy.md](../skills/rxmembersim/retail-pharmacy.md) - Pharmacy claims
- [../skills/rxmembersim/dur-alerts.md](../skills/rxmembersim/dur-alerts.md) - DUR processing
- [../skills/rxmembersim/formulary-management.md](../skills/rxmembersim/formulary-management.md) - Coverage
- [../references/code-systems.md](../references/code-systems.md) - NDC codes
