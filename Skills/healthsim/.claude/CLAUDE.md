# HealthSim Workspace Instructions

## Skills-First Approach

**IMPORTANT**: This workspace uses skill files to guide responses. Before attempting web searches, writing code, or improvising:

1. **Read `SKILL.md`** at workspace root for routing guidance
2. **Route to the appropriate product skill** based on the request
3. **Follow the skill's documented patterns** for data access and response format

## Skill Routing

| Request Type | Route To |
|--------------|----------|
| Demographics, SDOH, SVI, ADI, county/tract profiles | `skills/populationsim/SKILL.md` |
| Patients, clinical data, diagnoses, labs, EMR | `skills/patientsim/SKILL.md` |
| Claims, members, enrollment, benefits | `skills/membersim/SKILL.md` |
| Pharmacy, prescriptions, formulary, DUR | `skills/rxmembersim/SKILL.md` |
| Clinical trials, subjects, CDISC | `skills/trialsim/SKILL.md` |
| Provider networks, facilities | `skills/networksim/SKILL.md` |

## PopulationSim Data Access

PopulationSim has **embedded data files** in `skills/populationsim/data/`. For lookups:

1. **Don't write Python code** for simple lookups
2. Use `grep` to find rows by FIPS code or name
3. Use `Read` to get column headers
4. The skill files document exact column names and data sources

Example for county lookup:
```bash
grep "06073" skills/populationsim/data/county/places_county_2024.csv
grep "06073" skills/populationsim/data/county/svi_county_2022.csv
```

## Data Sources Reference

| Dataset | File Location | Key Column |
|---------|---------------|------------|
| CDC PLACES (County) | `data/county/places_county_2024.csv` | CountyFIPS |
| SVI (County) | `data/county/svi_county_2022.csv` | STCNTY |
| CDC PLACES (Tract) | `data/tract/places_tract_2024.csv` | TractFIPS |
| SVI (Tract) | `data/tract/svi_tract_2022.csv` | FIPS |
| FIPS Crosswalk | `data/crosswalks/fips_county.csv` | county_fips |

## Key Principles

1. **Skills contain the instructions** - read them before improvising
2. **Data is embedded** - no web searches needed for demographics/SDOH
3. **Simple tools first** - grep/read before Python
4. **Follow documented patterns** - skills show exact column names and formats
