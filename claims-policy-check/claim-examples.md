# MemberSim — Claim Examples

Extended examples for claim generation. See [SKILL.md](SKILL.md) for the core skill.

## Example: Partial Payment (Deductible Applied)

**Request:** "Generate a claim where deductible applies"

```json
{
  "accumulator_before": {
    "deductible_applied": 200.00,
    "deductible_limit": 500.00,
    "oop_applied": 200.00,
    "oop_limit": 3000.00
  },
  "claim": {
    "claim_id": "CLM20250115000003",
    "procedure_code": "99214",
    "charge_amount": 175.00
  },
  "adjudication": {
    "status": "paid",
    "allowed_amount": 125.00,
    "deductible": 125.00,
    "copay": 0.00,
    "paid_amount": 0.00,
    "patient_responsibility": 125.00
  },
  "accumulator_after": {
    "deductible_applied": 325.00,
    "deductible_limit": 500.00,
    "oop_applied": 325.00,
    "oop_limit": 3000.00
  }
}
```

Key accumulator elements:
- Shows before/after accumulator state
- Remaining deductible absorbs the full allowed amount
- paid_amount is $0 because deductible was not yet met
- OOP tracks alongside deductible

## Example: Oncology Infusion Claim

**Request:** "Generate a facility claim for chemotherapy infusion"

```json
{
  "claim": {
    "claim_id": "CLM20250115000004",
    "claim_type": "INSTITUTIONAL",
    "member_id": "MEM005678",
    "provider_npi": "1234567890",
    "facility_type": "outpatient_hospital",
    "service_date": "2025-01-15",
    "principal_diagnosis": "C50.911",
    "diagnosis_description": "Malignant neoplasm of right female breast",
    "claim_lines": [
      {
        "line_number": 1,
        "revenue_code": "0335",
        "procedure_code": "96413",
        "hcpcs_code": "J9267",
        "description": "Paclitaxel injection, 1mg",
        "units": 175,
        "charge_amount": 3500.00
      },
      {
        "line_number": 2,
        "revenue_code": "0335",
        "procedure_code": "96415",
        "description": "Chemotherapy infusion, additional hour",
        "units": 2,
        "charge_amount": 400.00
      },
      {
        "line_number": 3,
        "revenue_code": "0250",
        "procedure_code": "96360",
        "hcpcs_code": "J2405",
        "description": "Ondansetron injection (antiemetic)",
        "units": 8,
        "charge_amount": 120.00
      }
    ]
  },
  "prior_auth": {
    "auth_number": "PA20250101-12345",
    "status": "approved",
    "approved_units": 6,
    "approved_through": "2025-06-30"
  },
  "adjudication": {
    "status": "paid",
    "allowed_amount": 3200.00,
    "deductible": 0.00,
    "coinsurance": 640.00,
    "paid_amount": 2560.00,
    "patient_responsibility": 640.00
  }
}
```

Key oncology claim elements:
- J-codes for injectable drugs (J9267 = paclitaxel)
- Revenue code 0335 (chemotherapy)
- Prior authorization reference
- Multi-line claim (drug + administration + supportive care)

## Example: Out-of-Network Emergency

**Request:** "Generate an OON emergency department claim"

Key elements for OON ED:
- Balance billing protections apply (No Surprises Act)
- Qualifying Payment Amount (QPA) determines allowed
- Member cost share = in-network rate (surprise billing rules)
- Claim adjudicates at in-network benefit level

## Example: Telehealth Office Visit

**Request:** "Generate a telehealth professional claim"

Key elements:
- Place of service: 10 (telehealth in patient home) or 02 (telehealth other)
- Modifier 95 (synchronous telehealth)
- CPT codes: 99213-99215 with modifier
- Audio-only: append modifier 93
