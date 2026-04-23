# NetworkSim Query Skills

Query skills for searching, validating, and analyzing provider network data from the NPPES registry and CMS facility files.

## Skills in This Directory

| Skill | Purpose | Key Triggers |
|-------|---------|--------------|
| [provider-search.md](provider-search.md) | Search 8.9M providers by specialty, location, credentials | "find cardiologists", "providers in" |
| [facility-search.md](facility-search.md) | Search hospitals, nursing homes, clinics | "hospitals in", "find facilities" |
| [pharmacy-search.md](pharmacy-search.md) | Search retail, specialty, mail pharmacies | "pharmacies in", "CVS near" |
| [npi-validation.md](npi-validation.md) | Validate NPIs with Luhn checksums | "is NPI valid", "check NPI" |
| [network-roster.md](network-roster.md) | Generate provider rosters (CSV/JSON/Excel) | "create roster", "export providers" |
| [provider-density.md](provider-density.md) | Calculate providers per 100K vs HRSA benchmarks | "density analysis", "per 100K" |
| [coverage-analysis.md](coverage-analysis.md) | Assess geographic/specialty coverage | "network coverage", "specialty gaps" |
| [hospital-quality-search.md](hospital-quality-search.md) | Filter hospitals by CMS star ratings | "4-star hospitals", "quality filter" |
| [physician-quality-search.md](physician-quality-search.md) | Filter by credentials (MD/DO/NP/PA) | "MD only", "credentials" |

## Data Sources

- **network.providers**: 8,925,672 NPPES provider records
- **network.facilities**: 77,302 CMS-certified facilities
- **network.hospital_quality**: 5,421 hospitals with star ratings
- **network.physician_quality**: 1,478,309 physicians with quality metrics

## Common Query Patterns

### Provider by Specialty
```sql
SELECT npi, first_name, last_name, credential, practice_city
FROM network.providers
WHERE taxonomy_1 LIKE '207R%'  -- Internal Medicine
  AND practice_state = 'CA'
LIMIT 10;
```

### High-Quality Hospitals
```sql
SELECT f.facility_name, f.city, hq.hospital_overall_rating
FROM network.facilities f
JOIN network.hospital_quality hq ON f.ccn = hq.facility_id
WHERE hq.hospital_overall_rating IN ('4', '5')
  AND f.state_code = 'TX';
```

### Provider Density
```sql
SELECT 
    p.practice_state,
    COUNT(DISTINCT p.npi) * 100000.0 / sv.e_totpop as per_100k
FROM network.providers p
JOIN population.svi_county sv ON p.county_fips = sv.stcnty
GROUP BY p.practice_state, sv.e_totpop;
```

## Related Skills

- [Analytics Skills](../analytics/) - Advanced adequacy and desert analysis
- [Integration Skills](../integration/) - Cross-product provider assignment
- [PopulationSim](../../populationsim/) - Demographics for equity analysis

---

*Query skills use real NPPES data - every NPI returned is a registered provider.*
