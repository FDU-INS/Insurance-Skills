---
name: gcc-crossborder-overlay
version: 1.0
description: >
  Apply for multi-jurisdiction GCC engagements where entities span multiple
  GCC countries with different accounting frameworks (e.g., Bahrain parent
  with UAE/Saudi/Kuwait subsidiaries).
author: Panaversity — The AI Agent Factory
---

## GOVERNING FRAMEWORK FOR GCC CROSS-BORDER ENGAGEMENTS

When an engagement spans multiple GCC jurisdictions:

1. Identify the PRIMARY jurisdiction (usually the parent company's domicile).
2. Load the primary jurisdiction overlay first.
3. For each subsidiary, load its own jurisdiction overlay.
4. Apply consolidation rules per IFRS 10 (or AAOIFI equivalent).

## KEY FRAMEWORK CONFLICTS IN GCC CONSOLIDATION

| Parent | Subsidiary | Conflict |
|---|---|---|
| Bahrain (AAOIFI) | UAE (IFRS) | IAH funds: separate category vs. financial liability |
| Bahrain (AAOIFI) | Saudi (IFRS) | Income labels, balance sheet classification |
| Qatar (AAOIFI) | Kuwait (IFRS) | Same as Bahrain vs. UAE |

## CONSOLIDATION POLICY DECISION

For GCC groups with mixed AAOIFI/IFRS subsidiaries, the group must choose one framework
for the consolidated financial statements. Common industry practice:
- IFRS primary for consolidated group (satisfies international investor requirements)
- AAOIFI supplementary disclosures in notes (satisfies Bahrain/Qatar regulatory requirements)

## KEY CONSOLIDATION ADJUSTMENTS

1. IAH reclassification: Convert AAOIFI "Equity of IAH" to IFRS financial liability for consolidation.
2. Income relabelling: Standardise income labels across all entities to IFRS-consistent labels.
3. Ijarah assets: AAOIFI subsidiaries keep ijarah assets on-balance-sheet; IFRS subsidiaries
   (finance lease assessment) may have derecognised. Align to group policy.

## RESPONSE HEADER
```
GOVERNING FRAMEWORK: Multi-jurisdiction GCC — [Primary: X] / [Subsidiaries: Y, Z]
Consolidation basis: [IFRS / AAOIFI — specify which governs the group consolidated statements]
```
