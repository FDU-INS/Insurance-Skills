# NetworkSim Analytics Skills

Advanced analytics skills for network adequacy assessment and healthcare desert identification, integrating provider data with PopulationSim demographics and health indicators.

## Skills in This Directory

| Skill | Purpose | Key Triggers |
|-------|---------|--------------|
| [network-adequacy-analysis.md](network-adequacy-analysis.md) | Assess network adequacy against CMS/NCQA standards | "adequacy assessment", "CMS standards" |
| [healthcare-deserts.md](healthcare-deserts.md) | Identify underserved areas combining access + needs + vulnerability | "healthcare deserts", "underserved" |

## Regulatory Standards Supported

### CMS Medicare Advantage
- Provider-to-enrollee ratios (1:1,200 PCPs, 1:2,000 OB/GYN, etc.)
- Time/distance access standards (urban/suburban/rural)
- Essential specialty requirements

### NCQA Health Plan Accreditation
- 13 essential specialty categories
- Geographic distribution requirements
- Provider credential standards

### HRSA Benchmarks
- 60-80 PCPs per 100K population
- Health Professional Shortage Area (HPSA) criteria
- Medically Underserved Area (MUA) designation

## Healthcare Desert Framework

Deserts are identified by combining four dimensions:

| Dimension | Weight | Source |
|-----------|--------|--------|
| Access Gap | 35% | Provider density vs HRSA benchmarks |
| Health Burden | 30% | CDC PLACES disease prevalence |
| Social Vulnerability | 25% | CDC SVI percentile |
| Quality Gap | 10% | Hospital star ratings, credentials |

**Severity Tiers**:
- Critical: Score ≥ 0.80
- Severe: Score 0.60-0.79
- Moderate: Score 0.40-0.59
- Mild: Score 0.20-0.39
- Minimal: Score < 0.20

## Cross-Product Integration

Analytics skills JOIN NetworkSim provider data with PopulationSim reference tables:

```sql
-- Healthcare desert identification
SELECT 
    sv.county,
    COUNT(p.npi) * 100000.0 / sv.e_totpop as access_score,
    pl.diabetes_prevalence as health_burden,
    sv.rpl_themes as vulnerability
FROM population.svi_county sv
LEFT JOIN network.providers p ON sv.stcnty = p.county_fips
LEFT JOIN population.places_county pl ON sv.stcnty = pl.locationid
GROUP BY sv.county, sv.e_totpop, pl.diabetes_prevalence, sv.rpl_themes;
```

## Use Cases

### Health Plan Operations
- Build compliant networks meeting regulatory standards
- Geographic coverage optimization
- Provider recruitment prioritization

### Population Health & Equity
- Identify critical shortage areas
- Target telehealth expansion
- Community Health Center placement
- Vulnerable population access gaps

### Market Intelligence
- Competitive network assessment
- Specialty availability analysis
- Provider retirement impact forecasting

## Related Skills

- [Query Skills](../query/) - Provider and facility search
- [PopulationSim SDOH](../../populationsim/sdoh/) - Vulnerability analysis
- [PopulationSim Health Patterns](../../populationsim/health-patterns/) - Disease prevalence

---

*Analytics skills combine real NPPES data with CDC/Census demographics for evidence-based insights.*
