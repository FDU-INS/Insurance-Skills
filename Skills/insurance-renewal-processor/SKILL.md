---
name: insurance-renewal-processor
description: |
  Processes insurance renewal documentation for brokers and underwriters. Extracts policy details, compares renewal terms against expiring policies, identifies coverage gaps, and generates renewal summaries with premium comparisons and recommendation narratives.
version: "1.0.0"
author: "agentops"
license: "MIT"
x-agent:
  industries: [financial-services, insurance]
  risk_level: standard
  requires_approval: false
  memory_blocks: []
  mcp_dependencies: []
  tools: [file-read]
  trigger_keywords: [insurance, renewal, policy, premium, coverage, underwriting, broker]
  run_after: []
  compatibility: "Agent Platform >= 1.0"
---

# Insurance Renewal Processor

## Purpose

This skill processes insurance renewal documentation for brokers, underwriters, and risk managers. It extracts key policy details from expiring and renewal terms, performs side-by-side comparisons of coverage, conditions, and premiums, identifies material coverage gaps or restriction changes, and produces structured renewal summaries with recommendation narratives suitable for client presentation.

## When to Use

- When processing renewal invitations from insurers and comparing them against the expiring policy terms
- When preparing a renewal report for a commercial client covering multiple lines of business (property, liability, motor fleet, D&O, PI)
- When reviewing premium movements across renewal cycles to identify trends and negotiate with underwriters
- When onboarding a new client mid-term and needing to document their existing insurance programme for gap analysis
- When comparing quotations from multiple insurers to produce a market comparison for the client
- When identifying coverage gaps that may expose the client to uninsured losses, particularly in professional indemnity and public liability policies
- When preparing renewal documentation for submission to Lloyd's syndicates or London Market insurers via placing slips

## Instructions

1. **Ingest the renewal documentation.** Read the expiring policy schedule, renewal invitation or quotation, and any supplementary documents such as endorsements, claims experience summaries, or risk survey reports. Identify the policy class (e.g., commercial combined, professional indemnity, employers' liability, cyber, directors' and officers') and the policy period.

2. **Extract key policy details from both expiring and renewal terms.** For each policy, capture: insurer name, policy number, inception and expiry dates, the insured entity and any subsidiaries or named insureds, the limit of indemnity or sum insured, the excess or deductible, the premium (net, IPT, and gross), and any notable conditions, warranties, or exclusions.

3. **Perform a side-by-side comparison.** Align the expiring and renewal terms in a structured comparison. For each material field, highlight whether the renewal represents an improvement, deterioration, or no change. Pay particular attention to changes in excess levels, sub-limits, aggregate limits, territorial scope, retroactive dates (for claims-made policies), and any newly introduced exclusions or conditions precedent.

4. **Analyse premium movements.** Calculate the percentage change in premium from the expiring terms. Break down the premium movement into rate change and exposure change where the information is available. Compare against market benchmarks if prior renewal cycle data or market indices are available. Note whether Insurance Premium Tax (IPT) has been applied at the standard rate (12%) or the higher rate (20% for travel and certain other classes).

5. **Identify coverage gaps and risk exposures.** Review the renewal terms for any coverage gaps relative to the client's known risk profile. Check for common gap areas: cyber exclusions in property or liability policies, professional indemnity retroactive date restrictions, pollution exclusions, communicable disease exclusions, and adequacy of business interruption indemnity periods. Flag any warranties or conditions precedent that the client may struggle to comply with.

6. **Draft the recommendation narrative.** Write a clear recommendation for each policy line stating whether to accept the renewal terms, negotiate specific points, or seek alternative quotations. Where terms have deteriorated, provide context on market conditions (hard or soft market, capacity constraints, loss experience) to help the client understand the position. Quantify the financial impact of material changes where possible.

7. **Compile the renewal summary report.** Assemble all findings into a structured renewal report with an executive summary, individual policy comparisons, premium summary table across all lines, identified gaps and recommendations, and a timeline of renewal actions required with deadlines.

## Output Format

The output is a structured renewal report in markdown containing:

- **Executive Summary**: Total programme premium (expiring vs. renewal), overall percentage movement, number of policies reviewed, count of material coverage changes, and top-priority actions
- **Programme Overview Table**: A summary table listing each policy class, insurer, expiring premium, renewal premium, percentage change, and renewal status (accepted, pending, to market)
- **Individual Policy Comparisons**: For each policy, a two-column comparison table (expiring vs. renewal) covering all key fields, followed by a commentary section explaining material changes
- **Premium Analysis**: A breakdown of premium movements by policy class with charts or tables showing rate versus exposure components where available
- **Coverage Gap Analysis**: A list of identified gaps, each with a severity rating (critical, significant, advisory), a description of the exposure, and a recommended action
- **Recommendation Narrative**: A per-policy recommendation with supporting rationale
- **Action Timeline**: A list of actions, responsible parties, and deadlines aligned to renewal and inception dates
- **Appendices**: Claims experience summaries, market quotation comparisons, and any supporting documentation references

## Quality Checks

- All premium figures must reconcate across the individual policy tables and the programme summary, including correct application of IPT at the appropriate rate
- Percentage movements must be calculated consistently (renewal minus expiring, divided by expiring, multiplied by 100)
- Coverage comparisons must flag every change in excess, sub-limit, exclusion, or condition between expiring and renewal terms, not just premium changes
- For claims-made policies (PI, D&O, cyber), the retroactive date must be explicitly confirmed and any change flagged as a critical finding
- The recommendation narrative must not provide regulated financial advice; it must present factual analysis and options rather than directive instructions
- Policy periods must be verified to ensure continuous cover with no gap between expiry and inception dates
- All insurer names and policy numbers must match the source documents exactly, with no transposition errors

## Limitations

- The skill processes documents provided as input and cannot access insurer portals, broker management systems, or placing platforms directly
- It does not perform actuarial analysis or loss modelling; premium benchmarking is limited to the data available in the input files and prior renewal records
- Complex reinsurance arrangements, facultative placements, or treaty structures are outside the scope of this skill
- The skill does not provide regulated insurance advice under the Insurance Distribution Directive (IDD) or FCA ICOBS rules; output must be reviewed by an appropriately authorised person before client distribution
- Lloyd's market-specific documentation (Market Reform Contract, Placing Information and Broker Remuneration) may require manual formatting adjustments to meet LMA standards
- Multi-currency programmes require exchange rate inputs to be provided; the skill does not source live exchange rates
- Long-tail liability classes (employers' liability, clinical negligence) may require specialist actuarial input for adequate limit assessment that this skill cannot provide
