---
name: unemployment-statistics
description: Query Estonian Unemployment Insurance Fund statistics and studies for labor-market, unemployment, and employment-service indicators.
---

# Unemployment Statistics (Töötukassa)

## Use when
- You need unemployment and labor-market indicators from Töötukassa.
- You need employment-service trend context.

## Avoid when
- You only need macro labor indicators already in Stats Estonia tables.

## Inputs
- Period, region, demographic scope, and indicator set.

## Outputs
- Unemployment/labor dataset and trend summaries.

## Primary endpoints
- Statistics and studies: https://www.tootukassa.ee/et/statistika-ja-uuringud

## Workflow
1. Locate target indicator publication/table.
2. Extract period and regional dimensions.
3. Normalize metric definitions and units.
4. Return analysis-ready table with metadata notes.

## Human setup (when needed)
- If data must be downloaded manually from portal widgets, guide user through exact selections and continue from exported files.

## Quality checks
- Preserve indicator definitions per publication.
- Distinguish stock vs flow metrics.

## Access reality
- Public access type: Public webpage/document extraction.
- Verification run: 2026-02-24.
- https://www.tootukassa.ee/et/statistika-ja-uuringud (HTTP 200, text/html, file links detected: 0)

## Request contract
- Use the listed primary endpoints as authoritative entry points.
- If API/query parameters are only visible in-browser, preserve exact request URL, params, and headers in output metadata.
- If endpoint is UI-only, document click path and extraction method used.

## Output schema expectations
- Keep at least: source URL, retrieval timestamp, publication/update date (if available), title/record label, and extracted governance-relevant fields.
- Preserve original field names when present in downloadable/API output.

## Limits and caveats
- Confirm whether data is open-download, UI-only, or authenticated before claiming full access.
- Separate narrative/guidance text from measurable records.

## Verification hooks
- Validate endpoint reachability and content type before extraction.
- Validate that each extracted claim is linked to a concrete source URL.
