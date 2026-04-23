---
name: insurance-claim-routing-demo
description: "Interactive demo: Generate pseudo-labels from a strong teacher model, build a cheap student function, and evaluate accuracy. Showcases pseudo-labeling and teacher-student distillation."
parent_skill: demos
---
<!-- Copyright (c) 2026 Snowflake Inc. All rights reserved.
     Licensed under the Snowflake Skills License. See LICENSE file. -->

# Insurance Claim Routing Demo

Build an AI function that routes insurance claims using pseudo-labeled training data.

## Overview

Seed input-only data → pseudo-label with a strong teacher → build a cheap student function → evaluate. **Estimated time:** ~10 minutes.

## Workflow

### Step 1: Introduction

Explain to user:
```
Welcome to the Pseudo-Labeling & Teacher-Student Distillation Demo!

At the end of this demo, you will witness the Cortex AI Function Studio's ability to:
- Generate pseudo-labels using a strong teacher model (no labeled data needed!)
- Build a cheap student model that reproduces teacher-quality decisions
- Evaluate how closely the student matches the teacher using the exact_match metric

This demo starts with unlabeled claim intake records. We will use a strong
teacher model to create routing labels, then build a cheaper student model
and measure how closely it reproduces those decisions.

Claim routes:
- fast_track_auto
- property_damage
- injury_review
- fraud_review
- documentation_needed
- manual_specialist_review

Objects created: all prefixed with DEMO_ for easy cleanup.
```

### Step 2: Setup - Choose Location

If `{database}` and `{schema}` are already known from the prerequisite flow, accept them silently and skip the prompt.

Otherwise, ask user:
```
Where would you like to create the demo objects?

Database: [e.g., TEMP]
Schema: [e.g., PUBLIC]
```

Store the database and schema for use throughout the demo.

### Step 3: Create Input-Only Sample Data

Explain to user:
```
I'll load 80 realistic insurance claim intake records from a pre-generated set:
auto collisions, property damage, theft, injury, fraud, and documentation cases.

Columns:
- CLAIM_SUMMARY  (pre-generated, unique per row)
- INCIDENT_CHANNEL
- CUSTOMER_SEGMENT

I'll create:
- {database}.{schema}.DEMO_CLAIMS_UNLABELED
```

Run the data generation script:
```bash
PYTHONPATH=<SKILL_DIRECTORY>/src uv run --project <SKILL_DIRECTORY> python <SKILL_DIRECTORY>/src/generate_claims_data.py load \
  --connection <CONNECTION_NAME> \
  --database {database} \
  --schema {schema}
```

**Note:** Replace `<SKILL_DIRECTORY>` with the absolute path to the cortex-ai-function-studio skill directory, and `<CONNECTION_NAME>` with the active Snowflake connection.

Verify creation and confirm summaries are diverse:
```sql
SELECT COUNT(*) FROM {database}.{schema}.DEMO_CLAIMS_UNLABELED;

SELECT LEFT(CLAIM_SUMMARY, 150) AS SUMMARY_PREVIEW, INCIDENT_CHANNEL, CUSTOMER_SEGMENT
FROM {database}.{schema}.DEMO_CLAIMS_UNLABELED
LIMIT 5;
```

### Step 4: Pseudo-Label with Teacher Model

Present the pseudo-label configuration:
```
Now we'll use a strong teacher model to label each claim intake row.

Default teacher model: claude-opus-4-6 (or the strongest available Claude Opus variant)
Fallback: use the strongest available Claude-family model in the account

Source table: {database}.{schema}.DEMO_CLAIMS_UNLABELED
Input columns: CLAIM_SUMMARY, INCIDENT_CHANNEL, CUSTOMER_SEGMENT
Output fields:
  - claim_route (string) — routing category
Destination table: {database}.{schema}.DEMO_CLAIMS_DATA
```

If the default teacher model is unavailable, **load** `references/model_selection.md` and choose the strongest Claude-family option.

**MANDATORY:** Do not synthesize labels ad hoc in this demo. **Load** `synthetic-data/SKILL.md` and follow the **Pseudo-Label Input-Only Tables** workflow.

Pass this context into that workflow:
- `source_table`: `{database}.{schema}.DEMO_CLAIMS_UNLABELED`
- `input_columns`: `['CLAIM_SUMMARY', 'INCIDENT_CHANNEL', 'CUSTOMER_SEGMENT']`
- `output_table`: `{database}.{schema}.DEMO_CLAIMS_DATA`
- `model`: `{teacher_model}`
- `task_description`: `Classify each claim intake row into exactly one routing category: fast_track_auto, property_damage, injury_review, fraud_review, documentation_needed, or manual_specialist_review.`
- `output_schema`: `{"properties": {"claim_route": {"type": "string", "description": "One of: fast_track_auto, property_damage, injury_review, fraud_review, documentation_needed, manual_specialist_review"}}}`
- `preview_rows`: `0`

The label-synthesis workflow must:
- skip the preview step and label all rows in one pass
- continue with `EXPECTED` as the default label column

Show the label distribution after labeling completes:
```sql
SELECT EXPECTED:claim_route::STRING AS CLAIM_ROUTE, COUNT(*) AS ROWS
FROM {database}.{schema}.DEMO_CLAIMS_DATA
GROUP BY 1
ORDER BY ROWS DESC;
```

The pseudo-label workflow stores labels as a VARIANT column (`EXPECTED`). Since our output has a single field, convert it to a plain string column for evaluation:
```sql
ALTER TABLE {database}.{schema}.DEMO_CLAIMS_DATA ADD COLUMN EXPECTED_OUTPUT VARCHAR;
UPDATE {database}.{schema}.DEMO_CLAIMS_DATA SET EXPECTED_OUTPUT = EXPECTED:claim_route::STRING;
ALTER TABLE {database}.{schema}.DEMO_CLAIMS_DATA DROP COLUMN EXPECTED;
```

### Step 5: Create the Student AI Function

Present the function configuration:
```
Now we'll create a cheaper student model for claim routing.

Default student model: llama3.1-8b

Function name: DEMO_ROUTE_CLAIM
Inputs: CLAIM_SUMMARY, INCIDENT_CHANNEL, CUSTOMER_SEGMENT
Outputs:
  - claim_route (string) — routing category
System prompt:
"You are an insurance claim routing system. Given a claim summary, incident
channel, and customer segment, classify the claim into exactly one route:
fast_track_auto, property_damage, injury_review, fraud_review,
documentation_needed, or manual_specialist_review."

User prompt template:
"Claim summary: {CLAIM_SUMMARY}\nIncident channel: {INCIDENT_CHANNEL}\nCustomer segment: {CUSTOMER_SEGMENT}"
```

**⚠️ STOP**: Wait for user confirmation before creating the function.

**Load** `create/SKILL.md` and follow it from **Step 7 onward**, passing:
- `database`, `schema`
- `function_name`: `DEMO_ROUTE_CLAIM`
- `function_intention`: `Route insurance claims to the correct processing track.`
- `model`: chosen student model
- `inputs`: `[{"name": "CLAIM_SUMMARY", "sql_type": "VARCHAR"}, {"name": "INCIDENT_CHANNEL", "sql_type": "VARCHAR"}, {"name": "CUSTOMER_SEGMENT", "sql_type": "VARCHAR"}]`
- `outputs`: `[{"name": "claim_route", "json_type": "string", "description": "One of: fast_track_auto, property_damage, injury_review, fraud_review, documentation_needed, manual_specialist_review"}]`
- `system_prompt`: confirmed prompt
- `user_prompt_template`: `Claim summary: {CLAIM_SUMMARY}\nIncident channel: {INCIDENT_CHANNEL}\nCustomer segment: {CUSTOMER_SEGMENT}`

Return here after the smoke test succeeds.

### Step 6: Evaluate the Student AI Function

Present the evaluation configuration:
```
Let's evaluate how well the student model routes claims.

Since the function returns a single claim_route string, the built-in
exact_match metric works perfectly — it compares the predicted route
directly against the teacher-labeled EXPECTED_OUTPUT.

Default metric: exact_match
Results table: DEMO_ROUTE_CLAIM_EVAL_RESULTS
```

**⚠️ STOP**: Wait for user confirmation before running evaluation.

**Load** `evaluate/SKILL.md` and follow it from **Step 5 onward**, passing:
- `function_name`: `{database}.{schema}.DEMO_ROUTE_CLAIM`
- `function_model`: chosen student model
- `test_table`: `{database}.{schema}.DEMO_CLAIMS_DATA`
- `input_columns`: `['CLAIM_SUMMARY', 'INCIDENT_CHANNEL', 'CUSTOMER_SEGMENT']`
- `label_column`: `EXPECTED_OUTPUT`
- `metric`: `exact_match`
- `results_table`: `{database}.{schema}.DEMO_ROUTE_CLAIM_EVAL_RESULTS`

**Async by default:** When the evaluate workflow reaches the execution mode selection, choose **async** (`EVALUATE_AI_FUNCTION_ASYNC`) without asking the user. If the async SPROC returns an error string (e.g., warehouse permission issue), inform the user and fall back to sync execution (`EVALUATE_AI_FUNCTION`) instead. After kicking off the async job, poll `TASK_HISTORY()` for completion within this session rather than asking the user to return later — this is a guided demo. **Load** `references/async_status.md` for polling patterns.

**Skip Step 6 (next steps)** in the evaluate workflow — return here after results are presented.

Once evaluation is done, review the results. Show the scores to the user. Offer to see what cases did not match:
```
Would you like to see which claims the function routed incorrectly?
```

If yes, query the results table:
```sql
SELECT
    LEFT(INPUT_TEXT, 150) AS SUMMARY_PREVIEW,
    EXPECTED AS EXPECTED_ROUTE,
    PREDICTED AS PREDICTED_ROUTE,
    SCORE,
    FEEDBACK
FROM {database}.{schema}.DEMO_ROUTE_CLAIM_EVAL_RESULTS
WHERE SCORE < 1.0
ORDER BY SCORE
LIMIT 20;
```

Discuss common failure patterns. Explain that labels are teacher-generated (pseudo-labels), not human ground truth.

After reviewing results, continue to Step 7.

### Step 7: Cleanup

Ask user:
```
The Insurance Claim Routing demo is complete!

Would you like to clean up the demo objects?

This will drop:
- {database}.{schema}.DEMO_CLAIMS_UNLABELED
- {database}.{schema}.DEMO_CLAIMS_DATA
- {database}.{schema}.DEMO_ROUTE_CLAIM
- {database}.{schema}.DEMO_ROUTE_CLAIM_EVAL_RESULTS
```

**⚠️ STOP**: Wait for user confirmation before cleanup.

If yes, execute:
```sql
DROP TABLE IF EXISTS {database}.{schema}.DEMO_CLAIMS_UNLABELED;
DROP TABLE IF EXISTS {database}.{schema}.DEMO_CLAIMS_DATA;
DROP FUNCTION IF EXISTS {database}.{schema}.DEMO_ROUTE_CLAIM(VARCHAR, VARCHAR, VARCHAR);
DROP TABLE IF EXISTS {database}.{schema}.DEMO_ROUTE_CLAIM_EVAL_RESULTS;
```

### Step 8: Next Steps

Summarize the workflow: unlabeled data → teacher pseudo-labels → cheap student function → evaluation.

Explain to user:
```
You completed the pseudo-labeling and teacher-student distillation workflow:

1. Loaded unlabeled insurance claim intake records
2. Used a strong teacher model (Claude Opus) to generate routing labels
3. Built a cheaper student model to reproduce teacher routing decisions
4. Evaluated the student against teacher labels using exact_match

Key takeaways:

  Pseudo-labeling: When you don't have labeled data, a strong teacher model
  can generate high-quality training labels from your unlabeled data. This
  is dramatically faster than manual annotation.

  Teacher-student distillation: Once you have labels, you can train a cheap
  student model that approaches teacher quality at a fraction of the cost.

Want to build richer evaluation metrics? Try the "Custom Evaluation Metrics" demo.
Want to optimize the student's prompt? Try the "Prompt Optimization" demo.
```

## Key Cautions

- Pseudo-labels are teacher-generated, not human ground truth
- Insurance routing is regulated — keep human review for high-stakes decisions (fraud_review, injury_review)
- Some model names may not be available in every account or region

## Stopping Points

- ✋ Step 1: After introduction
- ✋ Step 2: After choosing database and schema
- ✋ Step 4: Before pseudo-labeling
- ✋ Step 5: Before creating the student function
- ✋ Step 6: Before evaluation
- ✋ Step 7: Before cleanup
