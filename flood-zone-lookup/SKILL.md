---
name: flood-zone-lookup
description: Use when the user mentions flood zone, flood risk, FEMA, SFHA, floodplain, property due diligence, natural hazard disclosure, flood insurance, base flood elevation, or asks whether a property is in a flood zone.
version: 1.0.0
---

# Flood Zone Lookup

Query FEMA's National Flood Hazard Layer to determine the flood zone designation for any US street address.

## When to Use

- User asks about flood risk for a property
- User is doing property due diligence and needs hazard info
- User mentions FEMA, SFHA, flood insurance, or floodplain
- User wants to know if a property needs flood insurance

## How to Use

1. Get the street address from the user (ask if not provided)
2. Call the `query_flood_zone` tool with the full address (include city, state, zip)
3. Interpret results using the guide below

## Interpreting Results

| Field | Meaning |
|-------|---------|
| `zone` | FEMA flood zone code (e.g. AE, X, VE) |
| `zoneName` | Plain English description of the zone |
| `sfha` | `true` = Special Flood Hazard Area (federally regulated) |
| `riskLevel` | `high`, `moderate`, or `minimal` |
| `bfe` | Base Flood Elevation in feet (only for zones with BFE data) |

### Risk Level Guidance

- **High (SFHA zones: A, AE, AH, AO, AR, A99, V, VE):** Mandatory flood insurance if federally-backed mortgage. Located in the 100-year floodplain (1% annual chance of flooding). Coastal V/VE zones have additional wave action hazard.
- **Moderate (X Shaded, B, D):** 500-year floodplain or undetermined. Insurance not required but recommended. Preferred Risk policies are typically cheaper.
- **Minimal (X, C):** Outside mapped flood areas. Lowest risk. Insurance optional but available.

### Key Talking Points

- SFHA = mandatory flood insurance for federally-backed mortgages (FHA, VA, conventional with Fannie/Freddie)
- Zone AE is the most common high-risk zone — it means FEMA has mapped the base flood elevation
- Zone X is the most common minimal-risk zone
- FEMA maps are updated periodically — check the map effective date for currency
- Even minimal-risk zones can flood (25% of flood claims come from low-risk areas)
