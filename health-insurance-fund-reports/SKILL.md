---
name: health-insurance-fund-reports
description: Use Estonian Health Insurance Fund annual reports for financing, service volumes, and system performance indicators.
---

# Health Insurance Fund Reports

## Use when
- You need annual financial and service indicators from Tervisekassa.
- You need official health insurance system performance context.

## Avoid when
- You need disease-incidence surveillance data.

## Inputs
- Reporting year and metric scope.

## Outputs
- Structured annual report indicators and metadata.

## Primary endpoints
- Annual reports: https://www.tervisekassa.ee/en/organisation/annual-reports

## Workflow
1. Retrieve selected annual reports.
2. Extract financing, service, and utilization metrics.
3. Normalize indicators across years.
4. Return analysis-ready dataset with definitions.

## Human setup (when needed)
- If reports require manual download, guide the user through download and continue from files.

## Quality checks
- Distinguish budgeted vs realized values.
- Keep indicator units and accounting basis.

## Access reality
- Public access type: UI page with direct downloadable files.
- Verification run: 2026-02-24.
- https://www.tervisekassa.ee/en/organisation/annual-reports (HTTP 200, text/html;, file links detected: 24)

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
