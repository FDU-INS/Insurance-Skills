# Bond Field Definitions

## AIA A312-2010 Payment Bond Fields

The standard construction payment bond form. Two bonds (performance + payment) use identical header fields but are executed separately.

| Field | Location in Document | Description |
|-------|---------------------|-------------|
| Bond Number | Top right, after "No." | Surety's unique identifier for this bond |
| Surety | "SURETY:" line | Full legal name of the surety company |
| Principal | "CONTRACTOR:" or "PRINCIPAL:" | The contractor who is bonded |
| Obligee | "OWNER:" | The project owner who the bond protects |
| Construction Contract | "CONSTRUCTION CONTRACT:" | Date and description of the underlying contract |
| Contract Amount | Dollar amount | The value of the construction contract |
| Penal Sum | "PENAL SUM:" or "AMOUNT:" | Maximum the surety will pay (usually = contract amount) |
| Effective Date | "Date:" | When the bond takes effect |
| Surety Agent | Signature block | The agent who executed the bond on behalf of the surety |
| Power of Attorney | Attached exhibit | Proof the agent is authorized to bind the surety |

## ConsensusDocs 260 Payment Bond Fields

Similar structure to AIA A312 with minor terminology differences:
- "Constructor" instead of "Contractor"
- "Surety" same
- "Owner" same
- Bond amount and project description same locations

## Common Variations

- Some bonds use NAIC code after the surety name
- Federal bonds include the contracting agency and solicitation number
- State bonds may reference the state statute (e.g., "pursuant to MCL 129.201")
- The Power of Attorney is sometimes a separate attached page, sometimes printed on the bond

## Michigan Little Miller Act Bonds (MCL 129.201)

Required on Michigan public projects ≥$50,000. Must name:
- The public body (MDOT, county, city) as obligee
- The prime contractor as principal
- Bond amount = contract price
