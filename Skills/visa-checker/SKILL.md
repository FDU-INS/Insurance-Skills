---
name: visa-checker
description: Check visa requirements, transit rules, passport validity requirements, and travel document status for any destination. Use when planning international travel, checking entry requirements, verifying passport validity, or needing vaccination/insurance reminders for specific countries.
---

# Visa & Documents Checker

Verify entry requirements and travel documents before you fly.

## Capabilities

- **Visa requirements**: Do you need a visa? Visa-free, VOA, or pre-approved?
- **Transit rules**: Airport transit without leaving? Do you need a transit visa?
- **Passport validity**: How many months validity required?
- **Blank pages**: How many empty passport pages needed?
- **Vaccinations**: Required vs recommended (yellow fever, etc.)
- **Travel insurance**: Mandatory for entry?
- **Return/onward tickets**: Proof of onward travel required?
- **Funds proof**: Minimum funds requirements

## Quick Usage

```bash
python3 scripts/check_visa.py \
  --nationality SG \
  --destination JP \
  --purpose tourism \
  --duration 14
```

## Parameters

| Flag | Description | Example |
|------|-------------|---------|
| `--nationality` | Your passport country | `SG`, `US`, `MY`, `ID` |
| `--destination` | Destination country | `JP`, `TH`, `VN`, `AU` |
| `--purpose` | Travel purpose | `tourism`, `business`, `transit` |
| `--duration` | Stay duration in days | `7`, `14`, `30` |
| `--transit` | Transit only (don't leave airport) | (flag) |
| `--layover-hours` | Hours in transit | `4`, `12` |

## Output Sections

1. **Visa Status**: Required / Not Required / On Arrival
2. **Transit Rules**: If applicable
3. **Passport Requirements**: Validity, blank pages
4. **Documents**: Insurance, funds, tickets needed
5. **Health**: Vaccinations, health declarations
6. **Reminders**: Checklist of what to prepare

## Data Sources

- Timatic (IATA database - industry standard)
- Government immigration websites
- Embassy/consulate official sources
- CDC/WHO for health requirements

## See Also

- `references/country_codes.md` - ISO country codes
- `references/visa_types.md` - Visa category definitions
