---
name: social-insurance-statistics
description: Query Social Insurance Board statistical publications for benefits, social protection services, and caseload trends.
---

# Social Insurance Statistics

## Use when
- You need Social Insurance Board caseload/benefit statistics.
- You need social-protection service trend context.

## Avoid when
- You only need unemployment service data.

## Inputs
- Benefit/service type, period, and region/group.

## Outputs
- Social-insurance statistics dataset with period metadata.

## Primary endpoints
- Statistics page: https://www.sotsiaalkindlustusamet.ee/asutus-uudised-ja-kontakt/praktiline-teave/statistika

## Workflow
1. Locate relevant publication/table on statistics page.
2. Extract indicators by period/group.
3. Normalize metric definitions and units.
4. Return analysis-ready dataset with caveats.

## Human setup (when needed)
- If data is offered in document downloads only, walk user through downloads and continue from supplied files.

## Quality checks
- Preserve source terminology for benefits/services.
- Separate counts, rates, and monetary values.

## Access reality
- Public access type: UI page with direct downloadable files.
- Verification run: 2026-02-24.
- https://www.sotsiaalkindlustusamet.ee/asutus-uudised-ja-kontakt/praktiline-teave/statistika (HTTP 200, text/html;, file links detected: 56)

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
