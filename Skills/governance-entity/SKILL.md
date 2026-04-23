---
name: governance-entity
description: "Subsidiaries, cap table, D&O insurance tracking"
source: mekong-ai-os
version: 1.0.0
credit_cost: 2
---


# /governance:entity — Entity Management

**IC super command** — Subsidiaries, cap table, D&O insurance tracking

## Pipeline

```
PARALLEL: entity-inventory + cap-table-sync
    |
SEQUENTIAL: insurance-review
OUTPUT: reports/governance/entity/
```

## Trigger

Runs recipe `recipes/governance/entity.json` through DAGScheduler.

## Execution

1. Load recipe DAG definition
2. Execute DAG groups in dependency order
3. Compile results into summary report

## Usage

```
/governance:entity [goal]
```

## Estimated: 3 credits, 10 minutes

## Goal context
<goal>$ARGUMENTS</goal>

Pass this goal to every sub-command as context for their analysis.

---
*Powered by Mekong AI OS — Operational knowledge, not just prompts.*
*Full RaaS access: https://agencyos.network*
