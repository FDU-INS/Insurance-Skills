---
name: depreciation-tracker
description: >
  Claim value trending and replacement cost tracking. Triggers: "claim value trending",
  "replacement cost tracking", "vehicle depreciation for claims",
  "residual value for insurance", "how fast is the insured vehicle losing value",
  "pre-loss value trajectory", "depreciation rate for settlement",
  "value retention for claims", "depreciation curve for total loss",
  "diminished value over time", "claim reserve adjustment",
  "portfolio depreciation exposure", "fleet depreciation risk",
  tracking vehicle depreciation for insurance claims valuation,
  replacement cost estimation, settlement trending, or reserve adequacy assessment.
version: 0.1.0
---

> **Date anchor:** Today's date comes from the `# currentDate` system context. Compute ALL relative dates from it. Example: if today = 2026-03-14, then "prior month" = 2026-02-01 to 2026-02-28, "current month" (most recent complete) = February 2026, "three months ago" = December 2025. Never use training-data dates.

> **`get_sold_summary` parameter safety:**
> - **Always set `inventory_type`** explicitly (`New` or `Used`) — omitting it defaults to `New`, returning zero results for used-vehicle queries
> - **Always set `limit: 5000`** — the default (1000) silently truncates when (months × states × ranking combos) exceeds 1000 rows
> - **For volume totals**, use `ranking_dimensions: dealership_group_name` (or the single relevant dimension) — never use the default `make,model,body_type` which creates ~150K rows for national 3-month queries
> - **Use separate calls** for totals vs breakdowns — don't combine in one call

# Depreciation Tracker — Claim Value Trending & Replacement Cost Tracking

## Insurer Profile (Load First)

Load the `marketcheck-profile.md` project memory file if exists. Extract: zip, state, role, claim_types, total_loss_threshold_pct, default_comp_radius. If missing, ask for ZIP. US-only (`get_sold_summary`, `search_active_cars`); UK not supported. Confirm profile.

## User Context

User is an insurance professional (adjuster, underwriter, claims manager) needing depreciation trends for accurate claim reserves, settlement offers, and total-loss determinations.

| Required | Field | Source |
|----------|-------|--------|
| Yes | Make/Model or segment | Ask |
| Recommended | Model year(s) | Ask |
| Auto/Ask | Geography (state/zip) | Profile or ask |
| Optional | Inventory type, comparison dimension, time horizon | Ask |

Clarify: used vehicle depreciation (total-loss claims) vs new vehicle MSRP parity (replacement cost) — different workflows.

## Workflow: Make/Model Depreciation Curve (Claims Context)

Use this when an adjuster asks "how fast is the RAV4 losing value" or "what's the depreciation trend for 2022 Civics" to inform settlement offers and reserve adjustments.

1. **Get current period sold data** — Call `get_sold_summary` with `make`, `model`, `inventory_type=Used`, `date_from` (first of prior month), `date_to` (end of prior month), `limit=5000`. Include `state` if specified.
   → **Extract only**: average_sale_price, sold_count. Discard full response.

2. **Get historical sold data at multiple intervals** — Make separate calls to `get_sold_summary` for each lookback period (all with `inventory_type=Used`, `limit=5000`):
   - **60 days ago**
   - **90 days ago**
   - **6 months ago**
   - **1 year ago**
   Record `average_sale_price` at each point. Adjust dates based on today's date.
   → **Extract only**: average_sale_price, sold_count per interval. Discard full response.

3. **Get current active market asking price** — Call `search_active_cars` with `year`, `make`, `model`, `car_type=used`, `stats=price`, `rows=0`. Include `zip`/`state` if available.
   → **Extract only**: mean, median, min, max price stats. Discard full response.

4. **Get original MSRP baseline** — Call `search_active_cars` with same YMMT, `rows=1`, `sort_by=price`, `sort_order=desc`. Decode the VIN for MSRP. Fallback: highest 1-year-ago sold price.
   → **Extract only**: msrp from decode. Discard full response.

5. **Build the depreciation curve with claims impact** — Calculate at each time interval:
   - **Retention %** = (average_sale_price at interval / original MSRP) x 100
   - **Monthly depreciation rate** = (price change between consecutive intervals) / (months between intervals)
   - **Annualized depreciation rate** = monthly rate x 12
   - **Settlement impact** = dollar change in FMV over the period (affects claim reserve accuracy)
   Present as a table and describe the curve shape (linear, accelerating, stabilizing).

## Workflow: Segment Value Trends (Portfolio Risk Context)

Use this when an underwriter asks "are SUVs holding value better than sedans in our claims portfolio" or "how is EV depreciation affecting our total-loss exposure."

1. **Get current period segment data** — Call `get_sold_summary` with `ranking_dimensions=body_type`, `ranking_measure=average_sale_price`, `date_from` (first of prior month), `date_to` (end of prior month), `inventory_type=Used`, `top_n=10`, `limit=5000`.
   → **Extract only**: per body_type — average_sale_price, sold_count. Discard full response.

2. **Get prior period segment data** — Same call with dates shifted back 3 months (or user's chosen comparison window), `limit=5000`.
   → **Extract only**: per body_type — average_sale_price, sold_count. Discard full response.

3. **Get fuel type comparison** — Call `get_sold_summary` with `fuel_type_category=EV`, current period dates, `inventory_type=Used`, `limit=5000`. Repeat with `fuel_type_category=ICE`. Repeat both for prior period.
   → **Extract only**: average_sale_price, sold_count per fuel_type per period. Discard full response.

4. **Calculate segment trends with insurance impact** — For each body type and fuel type:
   - **Period-over-period price change** = (current avg price - prior avg price) / prior avg price x 100
   - **Volume change** = (current sold_count - prior sold_count) / prior sold_count x 100
   - **Claims impact assessment:**
     - Segments with price declined more than 3%: "Accelerating depreciation — total-loss claims in this segment are becoming less expensive, but existing reserves may be overstated"
     - Segments held within +/- 1%: "Stable — current settlement benchmarks remain reliable"
     - Segments where price increased: "Appreciating — replacement costs are rising, reserves may be understated"

5. **Deliver the segment comparison** — Present a ranked table from strongest retention to weakest. Highlight the EV vs ICE gap specifically (EV depreciation directly impacts claims exposure for insured EV portfolios). Include volume context — a segment with strong prices but falling volume may signal softening ahead, requiring proactive reserve adjustment.

## Workflow: Brand Residual Ranking (Underwriting Context)

Use this when an underwriter asks "which brands hold value best" or "rank automakers by residual value for our risk models."

1. **Get current period brand prices** — Call `get_sold_summary` with `ranking_dimensions=make`, `ranking_measure=average_sale_price`, `ranking_order=desc`, `date_from` (first of prior month), `date_to` (end of prior month), `inventory_type=Used`, `top_n=25`, `limit=5000`.
   → **Extract only**: per make — average_sale_price. Discard full response.

2. **Get prior period brand prices** — Same call with dates shifted back 6 months (or user's preferred comparison window), `limit=5000`.
   → **Extract only**: per make — average_sale_price. Discard full response.

3. **Get volume context** — Call `get_sold_summary` with `ranking_dimensions=make`, `ranking_measure=sold_count`, `ranking_order=desc`, current period dates, `inventory_type=Used`, `top_n=25`, `limit=5000`.
   → **Extract only**: per make — sold_count. Discard full response.

4. **Calculate brand retention scores with risk tiers** — For each make:
   - **Retention %** = current average_sale_price / prior average_sale_price x 100
   - **Volume trend** = current sold_count vs prior sold_count (indicates demand strength)
   - Rank brands by retention % descending
   - Classify into **insurance risk tiers**:
     - Tier 1 — Low Risk (>98% retention): Strong value retention, lower total-loss claim severity
     - Tier 2 — Moderate Risk (95-98%): Normal depreciation, standard reserves adequate
     - Tier 3 — Elevated Risk (90-95%): Faster depreciation, consider adjusting reserves upward
     - Tier 4 — High Risk (<90%): Rapid depreciation, total-loss claims increasingly likely; may warrant premium adjustments

5. **Present the brand ranking** — Show a ranked table with: Rank, Make, Current Avg Price, Prior Avg Price, Retention %, Volume, Risk Tier. Note: "Brands in Tier 4 have the highest total-loss claim frequency due to rapid depreciation. Underwriters should factor retention tier into premium calculations for comprehensive and collision coverage."

## Workflow: Geographic Depreciation Variance (Settlement Calibration)

Use this when an adjuster asks "where do Tacomas hold value best" or "which states have the highest replacement costs" to calibrate settlement offers by region.

1. **Get state-level transaction data** — Call `get_sold_summary` with `make`, `model`, `summary_by=state`, `date_from` (first of prior month), `date_to` (end of prior month), `inventory_type=Used`, `limit=5000`.
   → **Extract only**: per state — average_sale_price, sold_count. Discard full response.

2. **Get national baseline** — Same call without `summary_by` for national average.
   → **Extract only**: average_sale_price, sold_count. Discard full response.

3. **Calculate geographic variance for settlement calibration** — For each state:
   - **Price index** = state average_sale_price / national average_sale_price x 100 (100 = national average)
   - **Premium/discount** = state price - national price in dollars
   - Sort by price index descending to show where vehicles command the highest premiums

4. **Identify settlement calibration patterns** — Group states into:
   - **Premium markets** (index > 105): Higher replacement costs — settlements should reflect the claimant's local market, not national averages
   - **At-national-average** (index 95-105): Standard settlement benchmarks apply
   - **Discount markets** (index < 95): Lower replacement costs — but settlements must still reflect what the claimant would actually pay to replace the vehicle in their local market
   Note: "Settlement offers must reflect the claimant's local market. Using a national average in a premium market understates replacement cost and invites disputes."

5. **Deliver the geographic map** — Present as a ranked table: State, Avg Transaction Price, National Avg, Price Index, Premium/Discount $, Sold Count. Highlight the top 5 and bottom 5 states for the specific vehicle. Note the settlement implications for each region.

## Workflow: MSRP Parity Tracker (Replacement Cost for New Vehicles)

Use this when a claims manager asks "which new cars are selling over sticker" or "what's the actual replacement cost for a new [Model]" — critical for claims on vehicles less than 1 year old where replacement cost may exceed MSRP.

1. **Get current MSRP parity data** — Call `get_sold_summary` with `inventory_type=New`, `ranking_dimensions=make,model`, `ranking_measure=price_over_msrp_percentage`, `ranking_order=desc`, `date_from` (first of prior month), `date_to` (end of prior month), `top_n=30`, `limit=5000`.
   → **Extract only**: per make/model — price_over_msrp_percentage. Discard full response.

2. **Get prior period parity data** — Same call with dates shifted back 3 months, `limit=5000`.
   → **Extract only**: per make/model — price_over_msrp_percentage. Discard full response.

3. **Get volume context** — Call `get_sold_summary` with `inventory_type=New`, `ranking_dimensions=make,model`, `ranking_measure=sold_count`, `ranking_order=desc`, current period dates, `top_n=30`, `limit=5000`.
   → **Extract only**: per make/model — sold_count. Discard full response.

4. **Classify parity status with claims implications** — For each make/model:
   - **Above MSRP** (price_over_msrp_percentage > 0): "Replacement cost exceeds MSRP — total-loss settlements on these vehicles may need to reflect actual market replacement cost, not sticker price"
   - **At MSRP** (price_over_msrp_percentage between -1% and 0%): "Replacement at MSRP — standard settlement"
   - **Below MSRP** (price_over_msrp_percentage < -1%): "Replacement below MSRP — settlement can reflect actual transaction prices"
   - **Trend direction**: compare current vs prior period to show if replacement costs are rising or falling

5. **Present the parity report** — Show a table: Make/Model, Current % Over/Under MSRP, Prior Period %, Change Direction, Sold Volume. Highlight:
   - Models that flipped from above-MSRP to below (replacement costs normalizing)
   - Models still commanding premiums (claims on these vehicles may face dispute if settled at MSRP)
   - Models with deepening discounts (favorable for claims resolution)

## Output

Present: claims-impact headline with depreciation rate and settlement range, trend data table (period/price/retention/rate/volume/settlement impact), key claims and underwriting signals (reserve adequacy, total-loss threshold shifts, EV exposure), and role-specific actionable recommendation with quantified business impact.
