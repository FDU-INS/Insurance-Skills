---
name: vehicle-appraiser
description: >
  Insurance valuation with comparable evidence. Triggers: "appraise this vehicle",
  "what's it worth", "insurance valuation", "comparable analysis",
  "fair market value", "pre-loss value", "appraisal report",
  "settlement valuation", "vehicle valuation", "claims appraisal",
  building a defensible, comparable-backed vehicle valuation
  for insurance claims, total-loss determinations, or
  settlement pricing decisions.
version: 0.1.0
---

# Insurance Valuation — Comparable-Backed Valuations With Transaction Evidence

> **`get_sold_summary` parameter safety:**
> - **Always set `inventory_type`** explicitly (`New` or `Used`) — omitting it defaults to `New`, returning zero results for used-vehicle queries
> - **Always set `limit: 5000`** — the default (1000) silently truncates when (months × states × ranking combos) exceeds 1000 rows
> - **For volume totals**, use `ranking_dimensions: dealership_group_name` (or the single relevant dimension) — never use the default `make,model,body_type` which creates ~150K rows for national 3-month queries
> - **Use separate calls** for totals vs breakdowns — don't combine in one call

## Insurer Profile (Load First)

Load the `marketcheck-profile.md` project memory file if exists. Extract: zip, state, radius, total_loss_threshold_pct, default_comp_radius. If missing, ask for ZIP and radius. US-only (all tools: decode, predict, search, history); UK not supported. Confirm profile.

## CPO Detection & Valuation

When appraising a vehicle, determine if it is Certified Pre-Owned (CPO):

1. **From user input:** If the user states the vehicle is certified/CPO.
2. **From listing data:** If the vehicle's listing has `is_certified=true`.
3. **From VIN history:** If `get_car_history` shows the vehicle currently listed as certified.

When the vehicle IS CPO, the Full Comparable Appraisal workflow adds these steps:

- **CPO predicted value:** Call `predict_price_with_comparables` with `is_certified=true` to get the certified market value.
- **Non-CPO predicted value:** Call `predict_price_with_comparables` WITHOUT `is_certified` to get the standard market value.
- **CPO retail comps:** Call `search_active_cars` with the YMMT filters PLUS `is_certified=true` to find certified-only comparables.
- **CPO premium calculation:** CPO Premium = CPO Predicted Value - Non-CPO Predicted Value

In the Valuation Summary output, add:

| Measure | Value |
|---------|-------|
| CPO Predicted Retail Value | $XX,XXX |
| Non-CPO Predicted Retail Value | $XX,XXX |
| CPO Premium | +$X,XXX (+X.X%) |
| Active CPO Comps | N within radius |
| Active Non-CPO Comps | N within radius |

## User Context

User is an insurance adjuster, claims analyst, or total-loss specialist needing a defensible, comparable-backed valuation for settlement offers and dispute resolution.

| Required | Field | Source |
|----------|-------|--------|
| Yes | VIN or YMMT | Ask |
| Yes | Odometer reading | Ask |
| Auto/Ask | ZIP, radius | Profile or ask |
| Recommended | Pre-loss condition (Clean/Average/Rough), purpose | Ask |
| Optional | CPO status | Ask |

VIN provided → decode first. Assumed trims lose credibility in disputes.

## Workflow: Full Comparable Appraisal

Use this for formal insurance valuations, total-loss claims, or any situation where the valuation must be supported by cited comparables for dispute resolution.

1. **Decode VIN** — Call `mcp__marketcheck__decode_vin_neovin` with `vin`.
   → **Extract only**: year, make, model, trim, body_type, drivetrain, engine, transmission. Discard full response.

2. **Predict price** — Call `mcp__marketcheck__predict_price_with_comparables` with `vin`, `miles`, `zip`, `dealer_type=franchise`, `is_certified` if applicable.
   → **Extract only**: predicted_price, comparable VINs with prices and miles. Discard full response.

3. **Pull active comps** — Call `mcp__marketcheck__search_active_cars` with YMMT from step 1, `zip`, `radius=100` (wider for defensible claims), `miles_range=<odo-15k>-<odo+15k>`, `car_type=used`, `sort_by=price`, `sort_order=asc`, `rows=20`.
   → **Extract only**: per listing — VIN, price, miles, dealer_name, distance, dom. Discard full response.

4. **Pull sold transactions** — Call `mcp__marketcheck__search_past_90_days` with same YMMT + location filters, `sold=true`.
   → **Extract only**: per listing — VIN, sold_price, miles, dealer_name, sale_date. Discard full response.

5. **Synthesize the valuation** — Combine all three data sources:
   - **Algorithmic predicted price** from step 2 (central estimate)
   - **Active comparable range** from step 3 (current retail context)
   - **Sold transaction range** from step 4 (transaction evidence)
   - Calculate a **recommended value range** (low / mid / high) using the overlap of all three.
   - Adjust for condition if the user provided it (rough = low end of range, clean = high end).

6. **Total-loss threshold calculation** — Using the condition-adjusted FMV:
   - **Repair cost threshold** = FMV x total_loss_threshold_pct (default 75%)
   - Present: "This vehicle is a total loss if repair costs exceed $XX,XXX (XX% of FMV)"
   - If estimated repair cost was provided, render the determination: TOTAL LOSS or NOT TOTAL LOSS

7. **Present the insurance valuation report** — Deliver a structured report with the valuation, every cited comparable (VIN, price, miles, dealer, distance), total-loss threshold, methodology notes, and confidence assessment.

## Workflow: Regional Price Variance

Use this when the user needs to understand how values differ across geographies, important for understanding settlement variation by region and ensuring fair market value reflects the claimant's local market.

1. **Primary market stats** — Call `mcp__marketcheck__search_active_cars` with `year`, `make`, `model`, `zip`, `radius=100`, `stats=price,miles`, `rows=0`, `car_type=used`.
   → **Extract only**: mean, median, min, max, count for price and miles. Discard full response.

2. **Comparison market stats** — Repeat step 1 for each additional ZIP.
   → **Extract only**: mean, median, count per market. Discard full response.

3. **Sold summary by state** — Call `mcp__marketcheck__get_sold_summary` with `make`, `model`, `inventory_type=Used`, `summary_by=state`, `ranking_measure=average_sale_price`, `ranking_order=desc`, `top_n=10`, `limit=5000`.
   → **Extract only**: per state — average_sale_price, sold_count. Discard full response.

4. **Calculate regional variance** — Build a comparison table: market, median price, mean price, sample size, and delta from the lowest market. Regional price variance directly impacts settlement values — the same vehicle may warrant a higher settlement in a premium market.

5. **Present the regional map** — Show the price variance table and highlight any market where the price delta exceeds 5%. Note: "Settlement offers should reflect the claimant's local market. Regional variance of X% supports adjusting the FMV for geographic factors."

## Workflow: Wholesale vs Retail Spread

Use this when understanding the gap between wholesale and retail values, critical for determining fair settlement amounts and salvage value estimates.

1. **Predict franchise (retail) price** — Call `mcp__marketcheck__predict_price_with_comparables` with `vin`, `miles`, `zip`, `dealer_type=franchise`.
   → **Extract only**: predicted_price. Discard full response.

2. **Predict independent (wholesale-proxy) price** — Call `mcp__marketcheck__predict_price_with_comparables` with `vin`, `miles`, `zip`, `dealer_type=independent`.
   → **Extract only**: predicted_price. Discard full response.

3. **Pull franchise listings** — Call `mcp__marketcheck__search_active_cars` with YMMT, `zip`, `radius=100`, `dealer_type=franchise`, `car_type=used`, `sort_by=price`, `sort_order=asc`, `rows=10`.
   → **Extract only**: per listing — price, miles, dealer_name; plus median. Discard full response.

4. **Pull independent listings** — Call `mcp__marketcheck__search_active_cars` with same filters, `dealer_type=independent`, `rows=10`.
   → **Extract only**: per listing — price, miles, dealer_name; plus median. Discard full response.

5. **Calculate the spread** — Present:
   - Franchise median price vs Independent median price
   - Spread in dollars and percentage
   - Predicted retail value vs predicted wholesale-proxy value
   - Note: "The franchise retail value represents the replacement cost a claimant would face. Settlement offers should be anchored to the retail replacement cost, not wholesale."

## Workflow: Historical Value Trajectory

Use this when the user asks "what has this VIN been listed at over time" or needs to understand the pricing history of a specific unit for claims documentation.

1. **Pull listing history** — Call `mcp__marketcheck__get_car_history` with `vin`, `sort_order=asc`.
   → **Extract only**: per event — date, dealer_name, price, dom. Discard full response.

2. **Decode VIN** — Call `mcp__marketcheck__decode_vin_neovin` with `vin`.
   → **Extract only**: year, make, model, trim, MSRP. Discard full response.

3. **Build the trajectory** — From the history, extract each listing event: date, dealer, asking price, and DOM at that dealer. Calculate:
   - Total days on market across all listings
   - Total price depreciation from first listing to most recent
   - Average price drop per listing hop
   - Number of unique dealers

4. **Current market context** — Call `mcp__marketcheck__predict_price_with_comparables` with `vin`, `miles`, `zip`.
   → **Extract only**: predicted_price. Discard full response.

5. **Present the timeline** — Show a chronological table of all listings with price, dealer, and DOM. Note any pre-loss listing history that establishes the vehicle's market value trajectory — useful for supporting or challenging settlement offers.

## Output

Present: vehicle ID summary, valuation table (franchise/independent/condition-adjusted FMV/comp ranges/confidence), total-loss threshold and determination, settlement range (low/mid/high), comparable data tables (active retail + sold transactions with VIN/price/miles/dealer), and methodology notes with condition adjustments, threshold source, and caveats.
