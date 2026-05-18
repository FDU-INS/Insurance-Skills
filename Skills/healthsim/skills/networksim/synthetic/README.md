# NetworkSim Synthetic Generation Skills

Skills for generating synthetic healthcare entities (providers, facilities, pharmacies, networks, plans) with realistic attributes and proper identifier formatting.

## Skills in This Directory

| Skill | Purpose | Key Triggers |
|-------|---------|--------------|
| [synthetic-provider.md](synthetic-provider.md) | Generate providers with valid NPI format | "generate provider", "create physician" |
| [synthetic-facility.md](synthetic-facility.md) | Generate hospitals, ASCs, clinics with CCN | "generate hospital", "create facility" |
| [synthetic-pharmacy.md](synthetic-pharmacy.md) | Generate pharmacies with NCPDP IDs | "generate pharmacy", "create CVS" |
| [synthetic-network.md](synthetic-network.md) | Generate complete network configurations | "generate network", "create PPO" |
| [synthetic-plan.md](synthetic-plan.md) | Generate health plan structures | "generate plan", "create benefits" |
| [synthetic-pharmacy-benefit.md](synthetic-pharmacy-benefit.md) | Generate PBM configurations | "generate formulary", "pharmacy benefit" |

## When to Use Synthetic vs Query Skills

| Cohort | Use | Reason |
|----------|-----|--------|
| Need a provider for demo | **Synthetic** | Quick, no database required |
| Find real cardiologists in Houston | **Query** | Need actual NPPES data |
| PatientSim encounter needs attending | **Synthetic** | Consistent with other synthetic data |
| Validate network adequacy | **Query** | Need real provider counts |

## Identifier Formats

### NPI (National Provider Identifier)
- 10 digits
- Luhn algorithm checksum (digit 10)
- Prefix: 1 (individual) or 2 (organization)
- Example: `1234567893`

### CCN (CMS Certification Number)
- 6 characters
- State code (2 digits) + facility type (2 digits) + sequence (2 digits)
- Example: `450123` (Texas, hospital type 01)

### NCPDP Provider ID
- 7 digits
- Used for pharmacy identification
- Example: `3456789`

## Example Outputs

### Synthetic Provider
```json
{
  "npi": "1987654321",
  "entity_type": "individual",
  "provider": {
    "last_name": "Chen",
    "first_name": "Michael",
    "credential": "MD, FACC"
  },
  "taxonomy": {
    "code": "207RC0000X",
    "display": "Cardiovascular Disease"
  },
  "practice_location": {
    "city": "Houston",
    "state": "TX",
    "county_fips": "48201"
  }
}
```

### Synthetic Facility
```json
{
  "ccn": "450358",
  "npi": "1234567890",
  "facility": {
    "name": "Memorial Hermann Hospital",
    "type": "Short Term Acute Care",
    "bed_count": 350
  },
  "services": {
    "emergency": true,
    "trauma_level": "Level I",
    "cardiac_cath": true
  }
}
```

## Generation Patterns

Synthetic skills use realistic patterns:

- **Names**: Common first/last name combinations
- **Credentials**: Appropriate for specialty (MD/DO for physicians, NP for nurse practitioners)
- **Taxonomy**: Valid NUCC codes matching specialty
- **Geography**: Real cities, states, valid county FIPS codes
- **Dates**: Reasonable enumeration dates (not future)

## Related Skills

- [Query Skills](../query/) - Search real provider data
- [Pattern Skills](../patterns/) - Network configuration templates
- [Integration Skills](../integration/) - Cross-product provider assignment
- [Reference Skills](../reference/) - Domain knowledge for realistic generation

---

*Synthetic skills generate realistic-looking entities for demos and testing. For real provider data, use Query skills.*
