---
name: retail-pharmacy
description: "Retail pharmacy prescription fills and claims including new prescriptions, refills, and mail order. Triggers: retail pharmacy, prescription fill, refill, CVS, Walgreens, mail order, days supply, copay, pharmacy claim, NCPDP"
---

# Retail Pharmacy Cohort

A cohort template for generating retail pharmacy prescription fills and claims including new prescriptions, refills, and mail order.

## For Claude

Use this skill when the user requests retail pharmacy or prescription fill cohorts. This teaches you how to generate **realistic pharmacy claims** with NCPDP transactions, copays, and fill workflows.

**When to apply this skill:**

- User mentions retail pharmacy or prescription fill
- User requests pharmacy claim or refill cohorts
- User specifies copay, days supply, or fill type
- User asks for CVS, Walgreens, or mail order examples
- User needs pharmacy billing cohorts

**Key capabilities this skill provides:**

- How to structure NCPDP claim transactions
- How to model retail vs mail order channel differences
- How to apply formulary copay tiers
- How to handle new fills vs refills
- How to generate rejection and override cohorts

## Metadata

- **Type**: cohort-template
- **Version**: 1.0
- **Author**: RxMemberSim
- **Tags**: pharmacy, retail, prescription, NCPDP, PBM
- **Updated**: 2025-01-15

## Purpose

This cohort generates realistic retail pharmacy transactions. It models the complete prescription lifecycle from new fill through refill, including claim submission, adjudication, and patient cost-sharing.

## When to Use This Skill

Apply this skill when the user's request involves:

**Direct Keywords**:

- "retail pharmacy", "prescription fill"
- "refill", "pharmacy claim"
- "copay", "CVS", "Walgreens"
- "30-day supply", "90-day supply", "mail order"

**Pharmacy Cohorts**:

- "Generate a retail pharmacy claim"
- "Create a prescription refill"
- "Generate a mail order fill"

## Trigger Phrases

- retail pharmacy
- prescription fill
- refill
- pharmacy claim
- copay
- CVS
- Walgreens
- pickup
- 30-day supply
- 90-day supply
- mail order

## Parameters

| Parameter | Type | Default | Options |
|-----------|------|---------|---------|
| fill_type | string | new | new, refill |
| days_supply | int | 30 | 30, 60, 90 |
| pharmacy_channel | string | retail | retail, mail_order |
| drug_category | string | generic | generic, preferred_brand, non_preferred_brand |
| claim_status | string | paid | paid, rejected |

## Pharmacy Channels

### Retail Pharmacy
- **Days Supply**: Typically 30 days
- **Copay**: Standard formulary copay
- **Examples**: CVS, Walgreens, Rite Aid, grocery store pharmacies

### Mail Order Pharmacy
- **Days Supply**: Typically 90 days
- **Copay**: Often 2.5x 30-day copay (discount)
- **Use Case**: Maintenance medications

### Preferred Pharmacy Network
- **Copay**: Reduced copay at network pharmacies
- **Non-Preferred**: Higher copay at non-network

## Prescription Lifecycle

```
1. Prescriber writes prescription
   ↓
2. Prescription transmitted to pharmacy (e-prescribe or paper)
   ↓
3. Pharmacist receives and enters prescription
   ↓
4. Pharmacy submits claim to PBM (B1 transaction)
   ↓
5. PBM adjudicates (eligibility, formulary, DUR)
   ↓
6. Response returned (paid, rejected, or warning)
   ↓
7. If paid: Pharmacist dispenses, patient picks up
   ↓
8. Refills available when 75-80% of supply used
```

## Prescription Data Elements

### New Prescription
```json
{
  "prescription_number": "RX{pharmacy_id}{sequence:06d}",
  "ndc": "11-digit NDC",
  "drug_name": "Drug Name Strength Form",
  "quantity_prescribed": 30,
  "days_supply": 30,
  "refills_authorized": 5,
  "daw_code": "0",
  "directions": "Take 1 tablet by mouth daily",
  "prescriber_npi": "10-digit NPI",
  "prescriber_dea": "DEA number (if controlled)",
  "written_date": "YYYY-MM-DD",
  "expiration_date": "YYYY-MM-DD"
}
```

### DAW (Dispense As Written) Codes
| Code | Description | Use Case |
|------|-------------|----------|
| 0 | No product selection indicated | Generic substitution allowed |
| 1 | Substitution not allowed by prescriber | Brand medically necessary |
| 2 | Substitution allowed, patient requested brand | Patient preference |
| 3 | Substitution allowed, pharmacist selected | Pharmacist choice |
| 4 | Substitution allowed, generic not in stock | Supply issue |
| 5 | Brand dispensed as generic | MAC pricing |
| 7 | Substitution not allowed, brand mandated by law | State law |
| 8 | Substitution allowed, generic not available | Market availability |

## Common Drug Categories

### Generic Maintenance Medications
```json
{
  "cardiovascular": [
    { "drug": "Lisinopril 10mg", "ndc": "00093505601", "awp": 8.50, "tier": 1 },
    { "drug": "Atorvastatin 20mg", "ndc": "00071015523", "awp": 12.00, "tier": 1 },
    { "drug": "Metoprolol Succinate 50mg", "ndc": "00378003501", "awp": 15.00, "tier": 1 },
    { "drug": "Amlodipine 5mg", "ndc": "00093231401", "awp": 6.50, "tier": 1 }
  ],
  "diabetes": [
    { "drug": "Metformin 1000mg", "ndc": "00093101901", "awp": 10.00, "tier": 1 },
    { "drug": "Glipizide 10mg", "ndc": "00093108401", "awp": 8.00, "tier": 1 }
  ],
  "mental_health": [
    { "drug": "Sertraline 50mg", "ndc": "00093041801", "awp": 9.00, "tier": 1 },
    { "drug": "Escitalopram 10mg", "ndc": "00093514101", "awp": 11.00, "tier": 1 }
  ]
}
```

### Preferred Brand Medications
```json
{
  "examples": [
    { "drug": "Eliquis 5mg", "ndc": "00003089421", "awp": 520.00, "tier": 3 },
    { "drug": "Jardiance 10mg", "ndc": "00597014130", "awp": 580.00, "tier": 3 },
    { "drug": "Ozempic 1mg/dose", "ndc": "00169410012", "awp": 950.00, "tier": 3 }
  ]
}
```

## Claim Pricing

### Pricing Benchmarks

**AWP (Average Wholesale Price)**
- Published benchmark price (often inflated)
- "Sticker price" - rarely reflects actual cost
- Used for reimbursement calculations
- AWP discounts common: AWP - 15% to AWP - 20%

**WAC (Wholesale Acquisition Cost)**
- Manufacturer's list price to wholesalers
- More accurate than AWP
- Does not include rebates or discounts
- Typically 16-20% below AWP

**MAC (Maximum Allowable Cost)**
- PBM-set ceiling price for generics
- Updated frequently (weekly/monthly)
- Based on market prices for multi-source drugs
- Pharmacies reimbursed at MAC regardless of acquisition cost

**NADAC (National Average Drug Acquisition Cost)**
- CMS survey-based actual acquisition cost
- Used for Medicaid reimbursement
- Updated weekly
- Most accurate cost benchmark

### Reimbursement Formulas

**Brand Drugs:**
```
Reimbursement = AWP - Discount% + Dispensing Fee

Example:
AWP: $500.00, Discount: 15%, Dispensing Fee: $2.00
Reimbursement = $500 - $75 + $2 = $427.00
```

**Generic Drugs:**
```
Reimbursement = Lower of:
  - MAC + Dispensing Fee
  - AWP - Discount% + Dispensing Fee
  - U&C Price

Example:
MAC: $15.00, AWP: $100.00 (15% discount = $85.00), U&C: $25.00
Dispensing Fee: $2.00
Reimbursement = $15 + $2 = $17.00 (MAC wins)
```

### Spread Pricing vs Pass-Through

**Traditional Spread Model:**
```
Plan Pays PBM:     AWP - 15% + $2.00 = $87.00
PBM Pays Pharmacy: AWP - 17% + $1.50 = $84.50
PBM Spread:        $2.50 per claim
```

**Pass-Through Model:**
```
Plan Pays PBM:     Actual pharmacy payment + admin fee
PBM Pays Pharmacy: AWP - 17% + $1.50 = $84.50
PBM Fee:          $3.00 per claim
Plan Cost:        $87.50 (transparent)
```

### Manufacturer Rebates

**Rebate Types:**
- **Base Rebate**: Guaranteed % of WAC
- **Market Share Rebate**: Bonus for formulary position
- **Price Protection**: Protection against price increases
- **Admin Fees**: PBM administrative fees

**Example Rebate Calculation:**
```
Drug WAC: $1,000
Base Rebate: 25% = $250
Market Share Bonus: 5% = $50
Total Rebate: $300 per Rx
```

**Rebate Flow:**
1. Manufacturer → PBM (quarterly)
2. PBM retains admin fee (3-5%)
3. PBM → Plan Sponsor (pass-through or retained)
4. Rebates may reduce net plan cost

### Copay by Tier (Commercial Plan)

| Tier | Description | 30-Day Copay | 90-Day Mail |
|------|-------------|--------------|-------------|
| 1 | Preferred Generic | $10 | $25 |
| 2 | Non-Preferred Generic | $25 | $62.50 |
| 3 | Preferred Brand | $50 | $125 |
| 4 | Non-Preferred Brand | $80 | $200 |
| 5 | Specialty | 25% coinsurance | N/A |

### Copay Assistance and Accumulators

**Manufacturer Copay Cards:**
```
Brand Drug Cost: $500
Plan Copay: $75
Copay Card Covers: $65
Patient Pays: $10

Note: $65 may not count toward deductible/OOPM
```

**Copay Accumulator Programs:**
Plan design to prevent copay card from counting toward accumulators:
```
Drug Cost: $500
Copay Card Pays: $75 → Does NOT apply to deductible
Patient True Spend: $0
Deductible Credit: $0
```

## Claim Structure

### NCPDP Claim Request
```json
{
  "header": {
    "bin": "610014",
    "version": "D0",
    "transaction_code": "B1",
    "pcn": "RXGROUP",
    "transaction_count": 1
  },
  "insurance": {
    "cardholder_id": "001234001",
    "group_number": "CORP001",
    "person_code": "01",
    "relationship_code": "1",
    "patient_id": "MEM001234"
  },
  "patient": {
    "date_of_birth": "19780315",
    "patient_gender": "1",
    "patient_first_name": "JOHN",
    "patient_last_name": "SMITH"
  },
  "claim": {
    "prescription_reference_number": "RX78901234",
    "product_service_id": "00093505601",
    "quantity_dispensed": 30.000,
    "days_supply": 30,
    "compound_code": "1",
    "daw_code": "0",
    "date_prescription_written": "20250110",
    "number_of_refills_authorized": 5,
    "prescription_origin_code": "1",
    "fill_number": 0
  },
  "prescriber": {
    "prescriber_id_qualifier": "01",
    "prescriber_id": "1234567890"
  },
  "pharmacy": {
    "service_provider_id_qualifier": "01",
    "service_provider_id": "9876543210"
  },
  "pricing": {
    "ingredient_cost_submitted": 8.50,
    "dispensing_fee_submitted": 2.00,
    "usual_and_customary_charge": 15.00,
    "gross_amount_due": 10.50
  }
}
```

### Claim Response (Paid)
```json
{
  "header": {
    "transaction_response_status": "A",
    "authorization_number": "AUTH20250115001234"
  },
  "pricing": {
    "ingredient_cost_paid": 8.50,
    "dispensing_fee_paid": 1.75,
    "total_amount_paid": 0.25,
    "patient_pay_amount": 10.00,
    "basis_of_reimbursement": "MAC"
  },
  "message": {
    "message": "CLAIM ACCEPTED"
  }
}
```

## Refill Cohorts

### Standard Refill
```json
{
  "original_fill": {
    "prescription_number": "RX78901234",
    "fill_number": 0,
    "service_date": "2024-12-15",
    "days_supply": 30,
    "refills_remaining": 5
  },
  "refill_request": {
    "prescription_number": "RX78901234",
    "fill_number": 1,
    "service_date": "2025-01-12",
    "days_elapsed": 28,
    "percent_used": 93,
    "refills_remaining": 4,
    "status": "eligible"
  }
}
```

### Too Early Refill
```json
{
  "original_fill": {
    "service_date": "2025-01-01",
    "days_supply": 30
  },
  "refill_request": {
    "service_date": "2025-01-15",
    "days_elapsed": 14,
    "percent_used": 47,
    "status": "too_early",
    "earliest_fill_date": "2025-01-25",
    "reject_code": "79"
  }
}
```

## Examples

### Example 1: New Generic Fill

```json
{
  "member": {
    "member_id": "MEM001234",
    "cardholder_id": "001234001",
    "name": { "given_name": "Michael", "family_name": "Brown" },
    "plan_code": "RX-STANDARD"
  },
  "pharmacy": {
    "npi": "9876543210",
    "ncpdp": "1234567",
    "name": "Springfield Pharmacy",
    "address": { "city": "Springfield", "state": "IL" }
  },
  "prescription": {
    "prescription_number": "RX78901234",
    "ndc": "00093505601",
    "drug_name": "Lisinopril 10mg Tablet",
    "quantity_prescribed": 30,
    "days_supply": 30,
    "refills_authorized": 5,
    "directions": "Take 1 tablet by mouth once daily",
    "prescriber_npi": "1234567890",
    "written_date": "2025-01-10"
  },
  "claim": {
    "claim_id": "RX20250115000001",
    "transaction_code": "B1",
    "service_date": "2025-01-15",
    "fill_number": 0,
    "daw_code": "0",
    "ndc": "00093505601",
    "quantity_dispensed": 30,
    "days_supply": 30,
    "ingredient_cost_submitted": 8.50,
    "dispensing_fee_submitted": 2.00
  },
  "response": {
    "status": "paid",
    "authorization_number": "AUTH20250115001234",
    "ingredient_cost_paid": 8.50,
    "dispensing_fee_paid": 1.75,
    "patient_pay_amount": 10.00,
    "copay_amount": 10.00,
    "basis_of_reimbursement": "MAC",
    "formulary_tier": 1,
    "message": "CLAIM ACCEPTED"
  }
}
```

### Example 2: Mail Order 90-Day Supply

```json
{
  "claim": {
    "claim_id": "RX20250115000002",
    "transaction_code": "B1",
    "service_date": "2025-01-15",
    "pharmacy_type": "mail_order",
    "ndc": "00071015523",
    "drug_name": "Atorvastatin 20mg Tablet",
    "quantity_dispensed": 90,
    "days_supply": 90,
    "fill_number": 2,
    "ingredient_cost_submitted": 36.00,
    "dispensing_fee_submitted": 0.00
  },
  "response": {
    "status": "paid",
    "ingredient_cost_paid": 36.00,
    "dispensing_fee_paid": 0.00,
    "patient_pay_amount": 25.00,
    "copay_amount": 25.00,
    "savings_message": "You saved $5.00 using mail order!",
    "formulary_tier": 1
  }
}
```

### Example 3: Brand Drug with Higher Copay

```json
{
  "claim": {
    "claim_id": "RX20250115000003",
    "ndc": "00003089421",
    "drug_name": "Eliquis 5mg Tablet",
    "quantity_dispensed": 60,
    "days_supply": 30,
    "daw_code": "0",
    "ingredient_cost_submitted": 520.00
  },
  "response": {
    "status": "paid",
    "ingredient_cost_paid": 480.00,
    "patient_pay_amount": 50.00,
    "copay_amount": 50.00,
    "formulary_tier": 3,
    "message": "Brand name drug - consider generic alternative if available"
  }
}
```

### Example 4: Rejected - Not Covered

```json
{
  "claim": {
    "claim_id": "RX20250115000004",
    "ndc": "12345678901",
    "drug_name": "Non-Formulary Drug",
    "quantity_dispensed": 30,
    "days_supply": 30
  },
  "response": {
    "status": "rejected",
    "reject_code": "70",
    "reject_message": "Product/Service Not Covered",
    "additional_message": "This drug is not on formulary. Covered alternatives: Drug A, Drug B",
    "formulary_alternatives": [
      { "ndc": "00093505601", "drug_name": "Lisinopril 10mg", "tier": 1, "copay": 10.00 },
      { "ndc": "00378003501", "drug_name": "Metoprolol 50mg", "tier": 1, "copay": 10.00 }
    ]
  }
}
```

## Validation Rules

| Rule | Requirement | Example |
|------|-------------|---------|
| NDC format | 11-digit numeric (5-4-2 format) | 00093505601 |
| Days supply | 1-90 for retail, 1-100 for mail | 30 (standard), 90 (mail order) |
| Quantity | Must be positive, match package size | 30, 60, 90 tablets |
| Fill date | Cannot be future, must be after Rx written date | 2025-01-15 |
| Refill number | 0 for new, 1-11 for refills | Refill 3 of 5 |
| Copay | Non-negative, appropriate for tier | $10 (Tier 1), $35 (Tier 2) |
| BIN/PCN | Valid processor identifiers | BIN: 003858, PCN: A4 |
| Pharmacy NPI | 10-digit valid NPI | 1234567890 |
| Prescriber NPI | 10-digit valid NPI | 0987654321 |
| DAW code | 0-9 per NCPDP standard | 0 (no selection), 1 (substitution not allowed) |

### Business Rules

- **New vs Refill**: New fills have refill_number = 0; refills have refill_number > 0
- **Mail Order**: Typically 90-day supply, lower cost per day than retail
- **Early Refill**: Most plans allow refill at 75-80% of days supply consumed
- **Controlled Substances**: Schedule II cannot have refills; must be new Rx each time
- **Generic Substitution**: DAW 0 allows generic; DAW 1 requires brand
- **Quantity Limits**: Some drugs have max quantity per fill (e.g., opioids)

## Related Skills

### RxMemberSim
- [SKILL.md](SKILL.md) - RxMemberSim overview
- [specialty-pharmacy.md](specialty-pharmacy.md) - Specialty drug fills
- [dur-alerts.md](dur-alerts.md) - Drug interaction checks
- [formulary-management.md](formulary-management.md) - Tier and coverage

### Cross-Product: PatientSim
- [../patientsim/diabetes-management.md](../patientsim/diabetes-management.md) - Oral diabetes medications (metformin, SGLT2i)
- [../patientsim/heart-failure.md](../patientsim/heart-failure.md) - GDMT medications (carvedilol, lisinopril)
- [../patientsim/chronic-kidney-disease.md](../patientsim/chronic-kidney-disease.md) - Renal medications
- [../patientsim/behavioral-health.md](../patientsim/behavioral-health.md) - Psychiatric medications

> **Integration Pattern:** Use PatientSim for medication orders. Use RxMemberSim retail-pharmacy for fills at community pharmacies. Match NDCs, correlate fill dates to prescription written dates, and apply appropriate refill patterns.

### Cross-Product: MemberSim
- [../membersim/accumulator-tracking.md](../membersim/accumulator-tracking.md) - Pharmacy costs count toward OOP

> **Integration Pattern:** For integrated medical+Rx benefits, pharmacy costs contribute to combined deductible/OOP. Coordinate accumulator tracking between MemberSim and RxMemberSim.

### References
- [../../references/code-systems.md](../../references/code-systems.md) - NDC codes
