---
name: site-selection-support
description: >
  Support clinical trial site selection with population-based analysis of
  eligible patient density, demographic diversity, and geographic accessibility.
  Uses PopulationSim v2.0 embedded CDC PLACES and SVI data for evidence-based
  site recommendations. Triggers: "site selection", "where to conduct trial",
  "best locations for trial", "site recommendations", "trial site analysis".
version: "2.0"
---

# Site Selection Support Skill

## Overview

The site-selection-support skill provides data-driven recommendations for clinical trial site selection by analyzing eligible patient populations, demographic diversity potential, and geographic accessibility. It helps optimize site networks for enrollment success and diversity goals.

**Primary Use Cases**:
- Identify high-potential geographic areas
- Optimize site network for enrollment
- Achieve diversity enrollment targets
- Balance competitive landscape
- Support site contracting decisions

---

## Trigger Phrases

- "Where should we conduct a [indication] trial?"
- "Site selection for [protocol]"
- "Best locations for diabetes trial enrollment"
- "Recommend sites for diversity in [indication]"
- "Site analysis for [geography]"

---

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `indication` | string | Yes | - | Target condition |
| `eligible_criteria` | object | No | - | Key eligibility criteria |
| `target_enrollment` | int | Yes | - | Total enrollment target |
| `num_sites` | int | No | - | Target number of sites |
| `diversity_targets` | object | No | - | Demographic enrollment goals |
| `geography_constraints` | object | No | - | Region/state restrictions |
| `site_type` | string | No | "all" | "academic", "community", "integrated" |

---

## Data Sources (Embedded v2.0)

Site selection uses real CDC PLACES and SVI data for evidence-based recommendations:

| Data Source | File | Application |
|-------------|------|-------------|
| CDC PLACES (County) | `data/county/places_county_2024.csv` | Disease prevalence by county |
| CDC PLACES (Tract) | `data/tract/places_tract_2024.csv` | Granular prevalence for site catchment |
| CDC SVI (County) | `data/county/svi_county_2022.csv` | Minority population %, access barriers |
| CDC SVI (Tract) | `data/tract/svi_tract_2022.csv` | SDOH factors for retention modeling |
| ADI (Block Group) | `data/block_group/adi_blockgroup_2023.csv` | Deprivation for recruitment challenges |

### Data-Driven Site Scoring

```python
# Score candidate site locations using real data:
for county in candidate_counties:
    # Look up actual prevalence
    prevalence = lookup(places_county, county.fips, 'DIABETES_CrudePrev')
    
    # Get diversity potential from SVI
    minority_pct = lookup(svi_county, county.fips, 'EP_MINRTY')
    
    # Calculate eligible population
    eligible = county.population * prevalence * protocol_filters
    
    # Score with real data, not estimates
    score = weighted_score(eligible, minority_pct, competition)
```

### Provenance in Output

```json
{
  "site_recommendation": {
    "metro": "Houston-The Woodlands-Sugar Land",
    "eligible_population": 128000,
    "data_provenance": {
      "source": "CDC_PLACES_2024",
      "geography": "Harris County (48201)",
      "prevalence_rate": 0.121,
      "file": "populationsim/data/county/places_county_2024.csv"
    }
  }
}
```

---

## Site Evaluation Framework

### Key Metrics

| Metric | Definition | Weight |
|--------|------------|--------|
| Eligible Population Density | Eligible patients per 100K | 25% |
| Diversity Score | Ability to meet diversity targets | 20% |
| Competition Index | Active competing trials | 15% |
| Healthcare Access | Provider availability | 15% |
| Research Infrastructure | Trial-ready sites | 15% |
| Geographic Access | Patient travel burden | 10% |

### Site Scoring Model

```
Site Score = (0.25 × Density) + (0.20 × Diversity) + 
             (0.15 × 1/Competition) + (0.15 × Access) + 
             (0.15 × Infrastructure) + (0.10 × Geography)
```

---

## Output Schema

```json
{
  "site_selection_analysis": {
    "protocol_summary": {
      "indication": "E11",
      "target_enrollment": 2000,
      "target_sites": 40,
      "per_site_target": 50,
      "diversity_targets": {
        "minority_total": 0.40,
        "black": 0.15,
        "hispanic": 0.20
      }
    },
    
    "national_eligible": 6800000,
    
    "recommended_sites": [
      {
        "rank": 1,
        "metro": "Houston-The Woodlands-Sugar Land, TX",
        "cbsa": "26420",
        "overall_score": 0.92,
        "eligible_population": 185000,
        "per_100k_density": 248,
        "metrics": {
          "density_score": 0.94,
          "diversity_score": 0.88,
          "competition_score": 0.78,
          "access_score": 0.85,
          "infrastructure_score": 0.92
        },
        "demographic_profile": {
          "white_nh": 0.28,
          "black": 0.22,
          "hispanic": 0.42,
          "asian": 0.08
        },
        "competing_trials": 8,
        "recommended_sites_in_metro": 3,
        "site_types_available": ["academic", "community", "health_system"]
      },
      {
        "rank": 2,
        "metro": "Miami-Fort Lauderdale-Pompano Beach, FL",
        "cbsa": "33100",
        "overall_score": 0.89,
        "eligible_population": 168000,
        "per_100k_density": 262,
        "metrics": {
          "density_score": 0.96,
          "diversity_score": 0.92,
          "competition_score": 0.72,
          "access_score": 0.82,
          "infrastructure_score": 0.88
        },
        "demographic_profile": {
          "white_nh": 0.32,
          "black": 0.18,
          "hispanic": 0.44,
          "asian": 0.04
        },
        "competing_trials": 12,
        "recommended_sites_in_metro": 2
      }
    ],
    
    "regional_distribution": {
      "recommended": {
        "south": { "sites": 18, "pct": 0.45 },
        "west": { "sites": 10, "pct": 0.25 },
        "midwest": { "sites": 7, "pct": 0.175 },
        "northeast": { "sites": 5, "pct": 0.125 }
      },
      "rationale": "Weighted toward South for diabetes prevalence and diversity"
    },
    
    "diversity_achievability": {
      "with_recommended_network": {
        "minority_total": 0.44,
        "black": 0.17,
        "hispanic": 0.23,
        "asian": 0.04
      },
      "vs_targets": {
        "minority_total": { "target": 0.40, "projected": 0.44, "status": "exceeds" },
        "black": { "target": 0.15, "projected": 0.17, "status": "exceeds" },
        "hispanic": { "target": 0.20, "projected": 0.23, "status": "exceeds" }
      },
      "confidence": "high"
    },
    
    "enrollment_projection": {
      "months_to_target": 8,
      "enrollment_rate_per_site": 6.25,
      "ramp_up_period_months": 2
    },
    
    "alternative_strategies": {
      "high_diversity_focus": {
        "sites": ["Houston", "Miami", "Atlanta", "Detroit", "Memphis"],
        "tradeoff": "Higher diversity, potentially slower enrollment"
      },
      "fast_enrollment_focus": {
        "sites": ["Phoenix", "Tampa", "Denver", "Dallas", "Las Vegas"],
        "tradeoff": "Faster enrollment, lower minority representation"
      }
    },
    
    "sites_to_avoid": [
      {
        "metro": "Boston",
        "reason": "High competition (24 active trials), saturated market"
      },
      {
        "metro": "San Francisco",
        "reason": "Very high competition, lower diabetes prevalence"
      }
    ]
  }
}
```

---

## Examples

### Example 1: Diabetes Trial Site Network

**Request**: "Site recommendations for T2DM trial, 2,000 subjects, 40% minority target"

**Response**:

**T2DM Trial Site Network Recommendation**

**Target**: 2,000 subjects across 40 sites, 40% minority enrollment

**Top 15 Recommended Metros**:

| Rank | Metro | Eligible | Diversity | Competition | Recommended Sites |
|------|-------|----------|-----------|-------------|-------------------|
| 1 | Houston | 185K | 0.72 | Moderate | 3 |
| 2 | Miami | 168K | 0.68 | Moderate | 2 |
| 3 | Dallas | 142K | 0.62 | Low | 2 |
| 4 | Phoenix | 128K | 0.58 | Low | 2 |
| 5 | Los Angeles | 156K | 0.68 | High | 2 |
| 6 | Atlanta | 118K | 0.58 | Moderate | 2 |
| 7 | Chicago | 92K | 0.52 | Moderate | 2 |
| 8 | San Antonio | 86K | 0.72 | Low | 2 |
| 9 | Detroit | 78K | 0.48 | Low | 2 |
| 10 | Tampa | 82K | 0.42 | Low | 2 |

**Regional Distribution**:
| Region | Sites | % of Network |
|--------|-------|--------------|
| South | 18 | 45% |
| West | 10 | 25% |
| Midwest | 7 | 17.5% |
| Northeast | 5 | 12.5% |

**Projected Diversity Achievement**:
| Group | Target | Projected | Status |
|-------|--------|-----------|--------|
| Minority Total | 40% | 44% | ✓ |
| Black | 15% | 17% | ✓ |
| Hispanic | 20% | 23% | ✓ |

---

### Example 2: Diversity-Optimized Network

**Request**: "Sites to maximize Black enrollment for heart failure trial"

**Response**:

**Heart Failure Trial - Black Enrollment Optimization**

**Strategy**: Prioritize metros with high Black HF prevalence and healthcare access

**Recommended High-Black-Enrollment Sites**:

| Rank | Metro | Black % of HF | Black Eligible | Competing Trials |
|------|-------|---------------|----------------|------------------|
| 1 | Atlanta | 48% | 42,000 | 6 |
| 2 | Detroit | 52% | 38,000 | 4 |
| 3 | Memphis | 58% | 28,000 | 2 |
| 4 | Birmingham | 54% | 22,000 | 3 |
| 5 | Baltimore | 46% | 32,000 | 8 |
| 6 | Chicago | 38% | 48,000 | 10 |
| 7 | Houston | 28% | 35,000 | 7 |
| 8 | Philadelphia | 42% | 36,000 | 12 |
| 9 | New Orleans | 52% | 18,000 | 3 |
| 10 | Jackson, MS | 62% | 12,000 | 1 |

**Projected Black Enrollment**: 28-32% (vs ~12% typical)

**Tradeoffs**:
- Enrollment may be 15% slower
- Some sites in less research-experienced areas
- Consider community engagement programs

---

### Example 3: Regional Focus

**Request**: "Best sites for NASH trial in Texas and Florida only"

**Response**:

**NASH Trial - Texas & Florida Site Analysis**

**Geography**: Texas + Florida (combined eligible: 180K)

**Texas Recommendations**:
| Metro | Eligible | NASH Specialists | Score |
|-------|----------|------------------|-------|
| Houston | 48,000 | 12 hepatology centers | 0.94 |
| Dallas | 42,000 | 8 hepatology centers | 0.88 |
| San Antonio | 28,000 | 4 hepatology centers | 0.82 |
| Austin | 18,000 | 3 hepatology centers | 0.78 |

**Florida Recommendations**:
| Metro | Eligible | NASH Specialists | Score |
|-------|----------|------------------|-------|
| Miami | 38,000 | 10 hepatology centers | 0.92 |
| Tampa | 32,000 | 6 hepatology centers | 0.86 |
| Orlando | 24,000 | 4 hepatology centers | 0.80 |
| Jacksonville | 16,000 | 3 hepatology centers | 0.74 |

**Recommended 15-Site Network**:
- Texas: 8 sites (Houston 3, Dallas 3, SA 1, Austin 1)
- Florida: 7 sites (Miami 3, Tampa 2, Orlando 1, Jax 1)

**Enrollment Projection**:
- Per-site eligible catchment: ~12,000
- Monthly enrollment: 8-10/site
- 12 months to 1,500 subjects

---

## Validation Rules

### Input Validation
- [ ] Indication valid
- [ ] Target enrollment positive
- [ ] Diversity targets sum reasonably

### Output Validation
- [ ] Sites ranked by score
- [ ] Regional distribution sums to ~1.0
- [ ] Diversity projection plausible

---

## Related Skills

- [feasibility-estimation.md](feasibility-estimation.md) - Eligible population
- [enrollment-projection.md](enrollment-projection.md) - Timeline modeling
- [county-profile.md](../geographic/county-profile.md) - Geographic data
- [health-outcome-disparities.md](../health-patterns/health-outcome-disparities.md) - Diversity data
