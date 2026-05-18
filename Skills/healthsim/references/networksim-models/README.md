# NetworkSim Reference Data Models

Canonical data models for NetworkSim entities. These models define the standard structure for provider network data across all HealthSim products.

## Entity Hierarchy

```
Network
├── Provider (individual or organization)
│   ├── Physician
│   ├── NursePractitioner
│   └── Specialist
├── Facility
│   ├── Hospital
│   ├── Clinic
│   └── AmbulatorySurgeryCenter
├── Pharmacy
│   ├── RetailPharmacy
│   └── SpecialtyPharmacy
└── Plan
    └── Benefits
```

## Models in This Directory

| Model | File | Purpose |
|-------|------|---------|
| Provider | [provider-model.md](provider-model.md) | Individual/organization healthcare providers |
| Facility | [facility-model.md](facility-model.md) | Hospitals, clinics, and healthcare facilities |
| Pharmacy | [pharmacy-model.md](pharmacy-model.md) | Retail and specialty pharmacies |
| Network | [network-model.md](network-model.md) | Network configuration and roster |
| Plan | [plan-model.md](plan-model.md) | Health plan benefit structures |

## Key Identifiers

| Entity | Primary ID | Format | Source |
|--------|-----------|--------|--------|
| Provider | NPI | 10 digits, Luhn checksum | NPPES |
| Facility | CCN | 6 alphanumeric | CMS |
| Pharmacy | NCPDP ID | 7 digits | NCPDP |
| Network | Custom | NETWORK-{type}-{seq} | Internal |
| Plan | Custom | PLAN-{type}-{seq} | Internal |

## Cross-Product Integration

### Person → Provider Linkage

When a Person in PatientSim has an encounter, they're linked to a Provider:

```json
{
  "encounter": {
    "patient_id": "PAT-001",
    "attending_provider": {
      "npi": "1234567890",
      "name": "Sarah Johnson, MD"
    }
  }
}
```

### Member → Network Status

When a Member in MemberSim has a claim, network status is determined:

```json
{
  "claim": {
    "member_id": "MEM-001",
    "provider_npi": "1234567890",
    "network_status": "IN_NETWORK",
    "tier": "preferred"
  }
}
```

### Prescription → Pharmacy Routing

When an RxMemberSim prescription is filled:

```json
{
  "fill": {
    "rx_number": "RX-001",
    "pharmacy_ncpdp": "3456789",
    "network_status": "IN_NETWORK"
  }
}
```

## Validation Rules

All NetworkSim entities must pass:

1. **Identifier Format**: Valid NPI/CCN/NCPDP format
2. **Geographic Data**: Valid state, ZIP, county FIPS
3. **Taxonomy Codes**: Valid NUCC taxonomy codes
4. **Date Ranges**: Logical date sequences

## Related Documentation

- [NetworkSim SKILL.md](../../skills/networksim/SKILL.md) - Master skill catalog
- [DuckDB Schema](../../docs/healthsim-duckdb-schema.md) - Database structure
- [PopulationSim Models](../populationsim-models/) - Demographic models for integration
