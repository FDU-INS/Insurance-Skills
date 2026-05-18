---
name: policy-conditioned-routing-demo
description: "Interactive demo: Build a policy-conditioned support ticket routing AI function using hand-curated gold-labeled data, then evaluate and optimize cheaper models via GEPA optimization."
parent_skill: demos
---
<!-- Copyright (c) 2026 Snowflake Inc. All rights reserved.
     Licensed under the Snowflake Skills License. See LICENSE file. -->

# Policy-Conditioned Support Ticket Routing Demo

Build an AI function that routes support tickets using company-specific policy context, then optimize cheaper models via GEPA optimization to match or beat a strong baseline.

## Overview

This demo walks you through:
1. Loading a labeled dataset with company routing policies
2. Creating a policy-aware routing AI function
3. Evaluating baseline accuracy across multiple models
4. Optimizing cheap models via GEPA optimization to close the accuracy gap
5. Comparing before/after results

Correct routing requires interpreting company-specific policy language written in internal vocabulary — models must generalize policy semantics rather than rely on keyword matching.

**Estimated time:** 20-40 minutes

## Workflow

### Step 1: Introduction

Explain to user:
```
Welcome to the Policy-Conditioned Routing Demo!

This demo uses a hard benchmark where correct routing depends on reading
company-specific policy text written in unfamiliar internal vocabulary.

Route labels:
- billing
- account_access
- bug_or_outage
- feature_request
- refund_or_cancel
- security_or_abuse

The dataset includes 4 companies, each with unique routing policies.
Most tickets have a "default" label that gets overridden by company
policy — a model that ignores policy context will score poorly.

Objects created: all prefixed with DEMO_ for easy cleanup.
```

### Step 2: Setup - Choose Location

Ask user:
```
Where would you like to create the demo objects?

Database: [e.g., TEMP]
Schema: [e.g., PUBLIC]

All objects will be prefixed with DEMO_ for easy cleanup.
```

Store the database and schema for use throughout the demo.

### Step 3: Load Seed Data

Explain to user:
```
I'll load the hand-curated gold-labeled dataset. This creates:

1. A company routing policy table (4 companies with unique policies)
2. A 24-row holdout set for evaluation (21 override rows)
3. A 96-row training set for optimization (84 override rows)

The data is pre-split — no train/test splitting needed.
```

**⚠️ STOP**: Wait for user confirmation before loading data.

**Load** `create_support_ticket_v6_dataset.sql.j2` and render it as a Jinja2 template with `database` and `schema` set to the user's chosen values, then execute the resulting SQL. This creates and populates the policy, holdout, and training tables.

Verify creation:
```sql
SELECT 'policy' AS TBL, COUNT(*) AS ROWS
FROM {database}.{schema}.DEMO_COMPANY_ROUTING_POLICY_V6
UNION ALL
SELECT 'holdout', COUNT(*)
FROM {database}.{schema}.DEMO_TICKETS_HARD_GOLD_V6_SMALL
UNION ALL
SELECT 'train', COUNT(*)
FROM {database}.{schema}.DEMO_TICKETS_POLICY_TRAIN_V6_LARGE;
```

Expected: policy=4, holdout=24, train=96.

Also verify zero subject overlap between train and holdout:
```sql
SELECT COUNT(*) AS EXACT_SUBJECT_OVERLAP_COUNT
FROM {database}.{schema}.DEMO_TICKETS_POLICY_TRAIN_V6_LARGE t
JOIN {database}.{schema}.DEMO_TICKETS_HARD_GOLD_V6_SMALL h
    ON t.SUBJECT = h.SUBJECT;
```

Expected: 0.

### Step 4: Create the Routing AI Function

Present the function configuration:
```
Now I'll create a policy-aware routing function.

Function name: DEMO_ROUTE_TICKET
Default model: gemini-2.5-flash-lite

Inputs:
  SUBJECT, BODY, CUSTOMER_TIER, COMPANY_NAME,
  POLICY_PROFILE, POLICY_TEXT, ENTITLEMENT_TEXT

Output: route (string)
```

**⚠️ STOP**: Wait for user confirmation or modifications before creating the function.

**Load** `create/SKILL.md` and follow it from **Step 7 onward**, passing:
- `database`, `schema`
- `function_name`: `DEMO_ROUTE_TICKET`
- `function_intention`: `Route policy-aware support tickets using company context.`
- `model`: `gemini-2.5-flash-lite`
- `inputs`: `[{"name": "SUBJECT", "sql_type": "VARCHAR"}, {"name": "BODY", "sql_type": "VARCHAR"}, {"name": "CUSTOMER_TIER", "sql_type": "VARCHAR"}, {"name": "COMPANY_NAME", "sql_type": "VARCHAR"}, {"name": "POLICY_PROFILE", "sql_type": "VARCHAR"}, {"name": "POLICY_TEXT", "sql_type": "VARCHAR"}, {"name": "ENTITLEMENT_TEXT", "sql_type": "VARCHAR"}]`
- `outputs`: `[{"name": "route", "json_type": "string", "description": "Support ticket route"}]`
- `system_prompt`: `You are a support ticket router. Given a ticket subject, body, customer tier, company name, policy profile, company policy text, and entitlement notes, classify it into exactly one category: billing, account_access, bug_or_outage, feature_request, refund_or_cancel, or security_or_abuse. The company policy is written in internal handling language rather than the route labels themselves. Infer the best route from the ticket and company policy, and only use company context when it changes the default interpretation. Return only the label in the route field.`
- `user_prompt_template`: `Subject: {SUBJECT}\nBody: {BODY}\nCustomer tier: {CUSTOMER_TIER}\nCompany name: {COMPANY_NAME}\nPolicy profile: {POLICY_PROFILE}\nCompany policy: {POLICY_TEXT}\nEntitlement notes: {ENTITLEMENT_TEXT}`

Return here after the smoke test succeeds.

### Step 5: Prepare Evaluation Table

Create the eval table from the holdout set, renaming the gold label column to `EXPECTED_OUTPUT`:
```sql
CREATE OR REPLACE TABLE {database}.{schema}.DEMO_TICKETS_EVAL AS
SELECT
    CASE_ID, CASE_GROUP, SUBJECT, BODY, CUSTOMER_TIER,
    COMPANY_NAME, POLICY_PROFILE, POLICY_TEXT, ENTITLEMENT_TEXT,
    DEFAULT_LABEL,
    GOLD_LABEL_V6_SMALL AS EXPECTED_OUTPUT,
    RULE_FAMILY, POLICY_EFFECT, REQUIRES_POLICY_CONTEXT,
    CURATION_NOTE, CURATED_AT
FROM {database}.{schema}.DEMO_TICKETS_HARD_GOLD_V6_SMALL
ORDER BY CASE_ID;
```

Verify:
```sql
SELECT COUNT(*) AS ROWS, COUNT_IF(REQUIRES_POLICY_CONTEXT) AS OVERRIDE_ROWS
FROM {database}.{schema}.DEMO_TICKETS_EVAL;
```

Expected: 24 rows, 21 overrides.

### Step 6: Evaluate Baselines

Present to user:
```
We'll evaluate the routing function across multiple models on the
24-row holdout set. This establishes baselines before optimization.

Default comparison models:
- claude-sonnet-4-5 (strong reference)
- claude-haiku-4-5
- gemini-2.5-flash
- gemini-2.5-flash-lite
- llama3.1-8b
- mistral-7b
```

**⚠️ STOP**: Confirm the model list with the user before running.

If one of these models is unavailable, remove it from the list or **load** `references/model_selection.md` to choose substitutes.

Create the results table:
```sql
CREATE OR REPLACE TABLE {database}.{schema}.DEMO_ROUTE_TICKET_BASELINE_RESULTS (
    MODEL_NAME VARCHAR, ROW_COUNT NUMBER, CORRECT NUMBER, ACCURACY NUMBER(10, 4)
);
```

**Create a per-model UDF for each model**, then run evaluation. The model and system prompt are baked into each function body — we create a separate function per model using `create_udf.py`, reusing the same configuration from Step 4 but with a different `model` and `function_name`.

**Do not confirm with the user before creating each UDF** — the user already confirmed the model list above.

For each model, derive a function suffix from the model name (replace `-` and `.` with `_`, uppercase). For example, `claude-sonnet-4-5` → `DEMO_ROUTE_TICKET__CLAUDE_SONNET_4_5`.

For **each model**, create the function:
```bash
PYTHONPATH=<SKILL_DIRECTORY>/src uv run --project <SKILL_DIRECTORY> python <SKILL_DIRECTORY>/src/create_udf.py \
    --execute --connection <CONNECTION_NAME> \
    --database {database} \
    --schema {schema} \
    --function-name "DEMO_ROUTE_TICKET__{model_suffix}" \
    --function-intention 'Route policy-aware support tickets using company context.' \
    --model {model_name} \
    --system-prompt '<same system_prompt from Step 4>' \
    --user-prompt-template 'Subject: {SUBJECT}\nBody: {BODY}\nCustomer tier: {CUSTOMER_TIER}\nCompany name: {COMPANY_NAME}\nPolicy profile: {POLICY_PROFILE}\nCompany policy: {POLICY_TEXT}\nEntitlement notes: {ENTITLEMENT_TEXT}' \
    --inputs '[{"name": "SUBJECT", "sql_type": "VARCHAR"}, {"name": "BODY", "sql_type": "VARCHAR"}, {"name": "CUSTOMER_TIER", "sql_type": "VARCHAR"}, {"name": "COMPANY_NAME", "sql_type": "VARCHAR"}, {"name": "POLICY_PROFILE", "sql_type": "VARCHAR"}, {"name": "POLICY_TEXT", "sql_type": "VARCHAR"}, {"name": "ENTITLEMENT_TEXT", "sql_type": "VARCHAR"}]' \
    --outputs '[{"name": "route", "json_type": "string", "description": "Support ticket route"}]'
```

After all UDFs are created, run eval queries **in parallel** — one per model:
```sql
INSERT INTO {database}.{schema}.DEMO_ROUTE_TICKET_BASELINE_RESULTS
WITH preds AS (
    SELECT
        EXPECTED_OUTPUT,
        {database}.{schema}.DEMO_ROUTE_TICKET__{model_suffix}(
            SUBJECT, BODY, CUSTOMER_TIER, COMPANY_NAME,
            POLICY_PROFILE, POLICY_TEXT, ENTITLEMENT_TEXT
        ) AS PREDICTED
    FROM {database}.{schema}.DEMO_TICKETS_EVAL
)
SELECT
    '{model_name}', COUNT(*), COUNT_IF(PREDICTED = EXPECTED_OUTPUT),
    ROUND(COUNT_IF(PREDICTED = EXPECTED_OUTPUT) / COUNT(*), 4)
FROM preds;
```

After all results are collected, **drop the per-model UDFs**:
```sql
DROP FUNCTION IF EXISTS {database}.{schema}.DEMO_ROUTE_TICKET__{model_suffix}(VARCHAR, VARCHAR, VARCHAR, VARCHAR, VARCHAR, VARCHAR, VARCHAR);
```

Show the baseline leaderboard:
```sql
SELECT MODEL_NAME, ROUND(ACCURACY * 100, 1) AS ACCURACY_PCT
FROM {database}.{schema}.DEMO_ROUTE_TICKET_BASELINE_RESULTS
ORDER BY ACCURACY DESC;
```

Highlight that cheap models typically score well below the strong reference on this hard benchmark because the policy vocabulary is unfamiliar.

### Step 7: Optimize Functions

Present the optimization configuration:
```
Now we'll optimize the cheap models using GEPA optimization.
The optimizer evolves the function body through multiple generations,
testing variations against the 96-row training set.

Default cheap models:
- llama3.1-8b
- mistral-7b
- gemini-2.5-flash
- gemini-2.5-flash-lite
- claude-haiku-4-5

Auto budget: demo (~5 minutes)
Experiment: DEMO_ROUTE_TICKET_OPT_EXP
```

**⚠️ STOP**: Wait for user confirmation or modifications before starting optimization.

**Load** `optimize/SKILL.md` and follow it from **Step 6 onward**, passing:
- `function_name`: `{database}.{schema}.DEMO_ROUTE_TICKET`
- `training_table`: `{database}.{schema}.DEMO_TICKETS_POLICY_TRAIN_V6_LARGE`
- `test_table`: `{database}.{schema}.DEMO_TICKETS_EVAL`
- `input_columns`: `['SUBJECT', 'BODY', 'CUSTOMER_TIER', 'COMPANY_NAME', 'POLICY_PROFILE', 'POLICY_TEXT', 'ENTITLEMENT_TEXT']`
- `label_column`: `EXPECTED_OUTPUT`
- `metric`: `exact_match`
- `models`: the confirmed cheap-model list
- `reflection_model`: `claude-sonnet-4-5`
- `auto_budget`: `demo`
- `experiment_name`: `{database}.{schema}.DEMO_ROUTE_TICKET_OPT_EXP`

Return here after optimization results are presented.

### Step 8: Summarize Results

**8.1.** Join baseline results from `DEMO_ROUTE_TICKET_BASELINE_RESULTS` with the best optimized score per model from `DEMO_ROUTE_TICKET_OPT_EXP`. Show each model's baseline accuracy, optimized accuracy, gain, and whether it meets or exceeds the strong reference (`claude-sonnet-4-5`) baseline. The strong reference itself was not optimized — include it as the reference row.

**8.2.** Calculate relative cost using the Pareto filter script (`src/filter_pareto.py`). Include all models: optimized cheap models at their best optimized score and `claude-sonnet-4-5` at its baseline score. Use the system prompt character length for `--prompt-chars` and average expected output length from the eval table for `--avg-output-chars`. Use the strong reference baseline as `--seed-score`. Present the Pareto-optimal table to the user.

**8.3.** Summarize key findings:
- Which model gained the most accuracy from GEPA optimization.
- If any optimized cheap model beats or matches the strong reference, call it out along with its relative cost — better quality at lower cost.
- If `claude-sonnet-4-5` is dominated on the Pareto frontier (a cheaper model has equal or higher score), note that the strong model is no longer the best option at any price point.
- If no cheap model beats the strong reference, note the remaining gap and suggest heavier optimization budgets or different models.

### Step 9: Cleanup

Ask user:
```
The Policy-Conditioned Routing demo is complete!

Would you like to clean up the demo objects?

This will drop:
- {database}.{schema}.DEMO_COMPANY_ROUTING_POLICY_V6
- {database}.{schema}.DEMO_TICKETS_HARD_GOLD_V6_SMALL
- {database}.{schema}.DEMO_TICKETS_POLICY_TRAIN_V6_LARGE
- {database}.{schema}.DEMO_TICKETS_EVAL
- {database}.{schema}.DEMO_ROUTE_TICKET
- {database}.{schema}.DEMO_ROUTE_TICKET_BASELINE_RESULTS
- {database}.{schema}.DEMO_ROUTE_TICKET_OPT_EXP
```

**⚠️ STOP**: Wait for user confirmation before cleanup.

If yes, execute:
```sql
DROP TABLE IF EXISTS {database}.{schema}.DEMO_COMPANY_ROUTING_POLICY_V6;
DROP TABLE IF EXISTS {database}.{schema}.DEMO_TICKETS_HARD_GOLD_V6_SMALL;
DROP TABLE IF EXISTS {database}.{schema}.DEMO_TICKETS_POLICY_TRAIN_V6_LARGE;
DROP TABLE IF EXISTS {database}.{schema}.DEMO_TICKETS_EVAL;
DROP FUNCTION IF EXISTS {database}.{schema}.DEMO_ROUTE_TICKET(VARCHAR, VARCHAR, VARCHAR, VARCHAR, VARCHAR, VARCHAR, VARCHAR);
DROP TABLE IF EXISTS {database}.{schema}.DEMO_ROUTE_TICKET_BASELINE_RESULTS;
DROP EXPERIMENT IF EXISTS {database}.{schema}.DEMO_ROUTE_TICKET_OPT_EXP;
```

### Step 10: Next Steps

Explain to user:
```
You completed a policy-conditioned routing workflow:

1. Loaded labeled data with unfamiliar company routing policies
2. Built a policy-aware routing function
3. Measured baselines — cheap models scored well below the strong
   reference because the policy vocabulary is intentionally unfamiliar
4. Optimized cheap models via GEPA optimization
5. Compared cost and quality side-by-side

Key takeaways:

  Accuracy: GEPA optimization recovered large accuracy gains on
  cheap models. On hard tasks where baselines are low, the room for
  improvement is biggest.

  Cost: The Pareto frontier shows which models offer the best
  quality-per-dollar. When an optimized cheap model matches or beats
  the strong reference, switching to it saves cost with no quality
  penalty.

  When to use GEPA optimization: Whenever baseline accuracy on
  your task is disappointing, especially with cheaper models.
  Optimization can close the gap without changing models or data.
```

## Key Cautions

- Gold labels are authored for this specific policy vocabulary. They represent ground truth, not pseudo-labels.
- The v6 policy vocabulary is intentionally unfamiliar. Models that memorize standard routing keywords will underperform.
- The holdout set is small (24 rows). Each row counts for ~4.2% of accuracy.

## Stopping Points

- ✋ Step 1: After introduction
- ✋ Step 2: After choosing database and schema
- ✋ Step 3: Before loading seed data
- ✋ Step 4: Before creating the routing function
- ✋ Step 6: Before running baseline evaluations
- ✋ Step 7: Before optimization
- ✋ Step 9: Before cleanup
