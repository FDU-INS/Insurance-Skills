# PopulationSim Integration for TrialSim

PopulationSim v2.0 provides **real-world reference data** for evidence-based trial planning, site selection, and diversity compliance. When geographies are specified, TrialSim uses actual CDC PLACES, SVI, and ADI data to ground feasibility estimates and enrollment projections.

## Data-Driven Trial Planning Pattern

**Step 1: Look up real population data for potential sites**
```
# For site feasibility in Houston metro (Harris County, FIPS: 48201)
Read from: population.places_county (via healthsim_query_reference)
-> DIABETES_CrudePrev: 12.1% (for diabetes trial)
-> CHD_CrudePrev: 6.4% (for CV outcomes trial)
-> CANCER_CrudePrev: 6.2% (for oncology trial)
-> TotalPopulation: 4,731,145

Read from: population.svi_county (via healthsim_query_reference)
-> RPL_THEMES: 0.68 (moderate-high vulnerability)
-> EP_MINRTY: 72.1% (supports diversity requirements)
```

**Step 2: Apply to site feasibility estimation**
```json
{
  "site_feasibility": {
    "county_fips": "48201",
    "county_name": "Harris County, TX",
    "indication": "Type 2 Diabetes",
    "eligible_population": {
      "total_population": 4731145,
      "disease_prevalence": 0.121,
      "prevalent_patients": 572467,
      "age_eligible_18_75": 458974,
      "funnel_to_screenable": 0.05,
      "annual_screenable": 22949
    },
    "diversity_metrics": {
      "minority_percentage": 0.721,
      "meets_fda_diversity_guidance": true
    },
    "data_provenance": {
      "source": "CDC_PLACES_2024",
      "data_year": 2022
    }
  }
}
```

**Step 3: Generate realistic enrollment projections**
- Site catchment based on real prevalence (not national averages)
- Diversity enrollment reflecting actual demographics
- Screening-to-randomization rates adjusted for SVI (access barriers)

## Reference Data Sources for Trial Planning

| Source              | Table                                                      | Use in TrialSim                     |
| ------------------- | ---------------------------------------------------------- | ----------------------------------- |
| CDC PLACES County   | `population.places_county (via healthsim_query_reference)` | Disease prevalence for feasibility  |
| CDC PLACES Tract    | `population.places_tract (via healthsim_query_reference)`  | Catchment area analysis             |
| SVI County          | `population.svi_county (via healthsim_query_reference)`    | Diversity planning, access barriers |
| SVI Tract           | `population.svi_tract (via healthsim_query_reference)`     | Site-level vulnerability context    |
| Geography Crosswalk | CBSA crosswalk (via healthsim_query)                       | Metro area site clustering          |

## Trial-Specific Applications

| Application | Data Used | TrialSim Integration |
|-------------|-----------|---------------------|
| **Site Feasibility** | PLACES disease prevalence + population | Eligible patient pool sizing |
| **Diversity Planning** | SVI EP_MINRTY, demographics | FDA diversity guidance compliance |
| **Enrollment Projection** | PLACES + SVI access indicators | Screening/randomization rates |
| **Site Selection** | Multi-county PLACES comparison | Optimal site network design |
| **Catchment Analysis** | Tract-level PLACES | Drive-time eligible population |

## Example: Data-Grounded Phase III Site Selection

**Request:** "Identify top 5 US counties for a Phase III NASH trial based on patient availability"

**Data Lookup Process:**
```
Query places_county_2024.csv for:
  - High OBESITY_CrudePrev (NASH proxy)
  - High DIABETES_CrudePrev (comorbidity)
  - Large TotalPopulation (volume)

Query svi_county_2022.csv for:
  - EP_MINRTY (diversity potential)
  - EP_UNINSUR (access consideration)
```

**Output with Provenance:**
```json
{
  "recommended_sites": [
    {
      "rank": 1,
      "county_fips": "48201",
      "name": "Harris County, TX",
      "obesity_prevalence": 0.328,
      "diabetes_prevalence": 0.121,
      "population": 4731145,
      "minority_pct": 0.721,
      "estimated_eligible": 45000,
      "diversity_score": "excellent"
    }
  ],
  "data_provenance": {
    "sources": ["CDC_PLACES_2024", "CDC_SVI_2022"],
    "methodology": "prevalence_weighted_ranking"
  }
}
```

## Integration with Trial-Support Skills

| PopulationSim Skill | TrialSim Application | Data Source |
|---------------------|---------------------|-------------|
| [data-lookup.md](../populationsim/data-access/data-lookup.md) | Exact prevalence for feasibility | CDC PLACES 2024 |
| [county-profile.md](../populationsim/geographic/county-profile.md) | Site catchment demographics | PLACES + SVI |
| [svi-analysis.md](../populationsim/sdoh/svi-analysis.md) | Diversity and access analysis | CDC SVI 2022 |
| [feasibility-estimation.md](../populationsim/trial-support/feasibility-estimation.md) | Protocol feasibility funnel | All sources |
| [diversity-planning.md](../populationsim/trial-support/diversity-planning.md) | FDA diversity compliance | SVI demographics |

> **Key Principle:** When planning trials, always ground feasibility and diversity estimates in real PopulationSim data. This enables evidence-based site selection and realistic enrollment projections.
