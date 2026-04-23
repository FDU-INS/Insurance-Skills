# RxMemberSim - Claude Code Configuration

## Project Overview
RxMemberSim generates synthetic pharmacy benefit data for testing PBM systems.

## Domain: Pharmacy Benefits Management

### Key Concepts
- **NCPDP Telecommunication**: Real-time pharmacy claim transactions (B1/B2)
- **NCPDP SCRIPT**: E-prescribing standard (NewRx, RxChange, RxRenewal)
- **NCPDP ePA**: Electronic prior authorization transactions
- **Formulary**: Drug coverage tiers, step therapy, quantity limits
- **DUR**: Drug Utilization Review - safety checks at point of sale
- **NDC**: National Drug Code - 11-digit drug identifier
- **GPI**: Generic Product Identifier - therapeutic classification

### Transaction Types
| Type | Standard | Purpose |
|------|----------|---------|
| B1/B2 | NCPDP Telecom | Pharmacy claims |
| NewRx | NCPDP SCRIPT | New prescription |
| RxChange | NCPDP SCRIPT | Prescription change |
| RxRenewal | NCPDP SCRIPT | Refill request |
| PAInitiation | NCPDP ePA | Start prior auth |
| PARequest | NCPDP ePA | PA with clinical info |

## Skills Location
Domain knowledge is in `/https://github.com/mark64oswald/healthsim-common/blob/main/skills/rxmembersim/`:
- `pharmacy-domain.md` - Core pharmacy concepts
- `ncpdp-transactions.md` - NCPDP formats
- `formulary.md` - Formulary management
- `dur-rules.md` - DUR alert types
- `prior-auth.md` - PA workflows
- `epa.md` - Electronic PA transactions
- `specialty-pharmacy.md` - Specialty workflows
- `pricing.md` - Rebates, spread, copay assist

## Code Conventions
- Models: Pydantic BaseModel with validation
- IDs: Use healthsim-core generators
- Dates: datetime objects, ISO format for export
- Money: Decimal for all financial amounts
- Codes: Enums for NDC, GPI, reject codes

## Testing Requirements
- Unit tests for all models
- Integration tests for adjudication
- NCPDP format validation tests
- Scenario execution tests

## Dependencies
- healthsim-core: Shared foundation
- pydantic: Data validation
- faker: Test data generation