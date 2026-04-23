---
name: state-management
description: "Save, load, and manage workspace cohorts to preserve synthetic data across sessions. Auto-persist for token-efficient batch operations. Query saved data with SQL. Tag, clone, merge, and export cohorts. Triggers: save, load, cohort, persist, resume, continue, list cohorts, delete cohort, export cohort, query cohort, get summary, tag cohort, clone cohort, merge cohorts"
---

# State Management

_Save, load, and manage workspace cohorts to preserve your synthetic healthcare data across sessions._

## For Claude

Use this skill when the user wants to persist their work or resume from a previous session. Cohorts are named snapshots containing all generated entities (patients, encounters, claims, etc.).

**Two Approaches**:

1. **Full Data** - Load everything into conversation. Best for small cohorts (<50 entities) where the user needs to see or reference all data immediately.

2. **Auto-Persist** - Save data, return only a summary. Best for large batches (50+ entities) to avoid context overflow. Query for specific data as needed.

Apply this knowledge when:
- User asks to save work ("save this", "let's save my progress")
- User wants to resume ("load my cohort", "continue from yesterday")
- User wants to see saved cohorts ("what cohorts do I have?")
- User generates large batches (auto-persist to avoid context overflow)
- User wants specific data from a saved cohort (query rather than load all)

## Purpose

State Management captures your workspace as a named cohort that can be restored later:

- **Session continuity** - Save at end of session, resume tomorrow
- **Cohort libraries** - Build reusable cohorts for demos and testing
- **Context efficiency** - Generate thousands of entities without overflow
- **Targeted queries** - Find exactly what you need without loading everything

## Trigger Phrases

**Saving**:
- "Save this as..."
- "Save my patients as..."
- "Persist these entities"

**Loading**:
- "Load my cohort"
- "Open the diabetes cohort"
- "What's in my cohort?"
- "Get a summary of..."

**Querying**:
- "Show me patients where..."
- "Query for female members over 65"
- "Find encounters with diagnosis..."

**Managing**:
- "List my cohorts"
- "Delete the test cohort"
- "Tag this with 'validated'"
- "Clone my cohort"
- "Merge these two cohorts"
- "Export to CSV"

## Conversation Examples

### Example 1: Save a Small Cohort

```
User: Save these 10 patients as "demo-cohort"

Claude: Saved "demo-cohort":
- 10 patients
- 32 encounters
- 89 lab results
- Tags: (none)

Load anytime with "load demo-cohort".
```

### Example 2: Load with Full Data (Small Cohort)

```
User: Load my demo cohort

Claude: Loaded "demo-cohort" with 10 patients:

1. Maria Santos (58F) - Type 2 DM, A1C 7.8%
   - 4 encounters, latest: 2024-02-15
   - Medications: Metformin 1000mg BID

2. James Wilson (67M) - Type 2 DM with CKD Stage 3
   - 3 encounters, latest: 2024-01-28
   - Medications: Metformin 500mg BID, Lisinopril 10mg

[...full details for all 10 patients...]

What would you like to do with this cohort?
```

### Example 3: Generate Large Batch (Auto-Persist)

```
User: Generate 200 Medicare members over 65

Claude: Generated and saved "medicare-members-20241228":

| Metric | Value |
|--------|-------|
| Members | 200 |
| Age Range | 65-89 |
| Gender | 96 male, 104 female |
| Top States | CA (42), TX (38), FL (31) |

Data is persisted. Query for specific subsets:
- "Show me members from California"
- "Find members with diabetes"
- "Show 3 sample members"
```

### Example 4: Query Saved Data

```
User: Show me female members from California over 75

Claude: Found 18 matching members:

| Name | Age | City | Risk Score |
|------|-----|------|------------|
| Margaret Chen | 78 | Los Angeles | 1.85 |
| Dorothy Williams | 82 | San Francisco | 2.12 |
| Patricia Lee | 76 | San Diego | 1.45 |
| Betty Martinez | 79 | Sacramento | 1.92 |
| Ruth Anderson | 81 | Fresno | 2.34 |
...

Showing 5 of 18. Say "show more" for next page.
```

### Example 5: Get Summary Without Loading All Data

```
User: What's in my diabetes cohort?

Claude: "diabetes-cohort-20241227" summary:

| Entity Type | Count |
|-------------|-------|
| Patients | 150 |
| Encounters | 425 |
| Lab Results | 890 |
| Medications | 320 |

**Demographics**:
- Age range: 35-78 years
- Gender: 72 male, 78 female

**Clinical**:
- Average A1C: 7.8%
- With complications: 67 (45%)
- On insulin: 43 (29%)

Need specific data? I can query for particular patients or conditions.
```

### Example 6: Resume Work on Large Cohort

```
User: Continue working on my Medicare cohort from yesterday

Claude: Loaded summary for "medicare-members-20241227":
- 500 members
- Last updated: yesterday at 3:45 PM
- Tags: training, california

What would you like to do?
- Generate more members
- Query specific subsets  
- Add claims or encounters
- Export for analysis
```

### Example 7: List Available Cohorts

```
User: What cohorts do I have?

Claude: You have 5 saved cohorts:

| Name | Entities | Last Updated | Tags |
|------|----------|--------------|------|
| diabetes-cohort-20241227 | 1,785 | 2 days ago | training, validated |
| medicare-members-20241227 | 500 | yesterday | training |
| heart-failure-demo | 45 | 1 week ago | demo |
| test-patients | 10 | 3 weeks ago | - |
| oncology-trial-2024 | 2,340 | 1 month ago | trialsim |

Load any with "load [name]" or get summary with "summarize [name]".
```

### Example 8: Delete a Cohort

```
User: Delete test-patients

Claude: Delete "test-patients"? This contained 10 patients and cannot be undone.

User: Yes

Claude: Deleted "test-patients". You have 4 remaining cohorts.
```

### Example 9: Tag Management

```
User: Tag my diabetes cohort as "validated" and "production"

Claude: Tagged "diabetes-cohort-20241227":
- validated ✓
- production ✓

Now has 4 tags: [training, validated, production, diabetes]
```

```
User: What cohorts are tagged "validated"?

Claude: 2 cohorts tagged "validated":
- diabetes-cohort-20241227 (1,785 entities)
- heart-failure-validated (890 entities)
```

### Example 10: Clone a Cohort

```
User: Clone my diabetes cohort for testing variations

Claude: Cloned "diabetes-cohort-20241227" → "diabetes-cohort-20241227-copy":
- 150 patients copied
- 425 encounters copied
- All entities have new IDs

The clone is independent—changes won't affect the original.
Would you like to rename it?
```

### Example 11: Merge Cohorts

```
User: Merge my diabetes and heart-failure cohorts into combined-training

Claude: Created "combined-training" from 2 sources:

| Source | Patients | Encounters |
|--------|----------|------------|
| diabetes-cohort | 150 | 425 |
| heart-failure-cohort | 120 | 380 |
| **Total** | **270** | **805** |

- Conflicts resolved: 0 (no duplicate IDs)
- Tags inherited: training, validated

Both source cohorts preserved unchanged.
```

### Example 12: Export to CSV

```
User: Export my diabetes cohort to CSV

Claude: Exported "diabetes-cohort-20241227" to CSV:

| File | Rows | Size |
|------|------|------|
| patients.csv | 150 | 145 KB |
| encounters.csv | 425 | 312 KB |
| lab_results.csv | 890 | 548 KB |
| medications.csv | 320 | 98 KB |

Location: ~/Downloads/diabetes-cohort-20241227/
Total: 1.1 MB

Load in Python:
```python
import pandas as pd
patients = pd.read_csv('~/Downloads/diabetes-cohort-20241227/patients.csv')
```
```

## Generation Guidelines

### When to Use Full Data vs Auto-Persist

| Situation | Approach | Reason |
|-----------|----------|--------|
| User asks to "save" small cohort | Full save, confirm | User expects confirmation |
| User generates 50+ entities | Auto-persist, show summary | Avoid context overflow |
| User asks "what's in my cohort" | Get summary first | Don't assume they want all data |
| User asks to "load" and cohort is small | Load full data | User wants to see it |
| User asks to "load" and cohort is large | Get summary, offer to query | Context efficiency |
| User asks specific question about saved data | Query for just that data | Targeted response |

### Proactive Auto-Persist

When generating large batches:
1. Generate entities
2. Auto-persist immediately
3. Show summary with counts and key stats
4. Offer query options

```
User: Generate 100 heart failure patients

Claude: [Generates patients]
[Auto-persists]

Saved "heart-failure-20241228":
- 100 patients persisted
- NYHA Class: I (15), II (40), III (35), IV (10)
- EF range: 15-55%
- On GDMT: 82 (82%)

Query for specific subsets or generate encounters for these patients.
```

### Confirming Destructive Actions

Always confirm before:
- Deleting cohorts
- Overwriting existing cohorts
- Merging (which creates new cohort)

```
User: Save this as diabetes-cohort

Claude: "diabetes-cohort" already exists with 150 patients. 
Overwrite it, or save as "diabetes-cohort-2"?
```

## Parameters Reference

### save_cohort
| Parameter | Description | Required |
|-----------|-------------|----------|
| name | Cohort identifier | Yes |
| entities | Dict of entity type → list | Yes |
| description | Notes about contents | No |
| tags | Organization keywords | No |
| overwrite | Replace existing | No (default: false) |

### get_summary
| Parameter | Description | Required |
|-----------|-------------|----------|
| cohort_id_or_name | Cohort identifier | Yes |
| include_samples | Include sample entities | No (default: true) |
| samples_per_type | Samples per entity type | No (default: 3) |

### query_cohort
| Parameter | Description | Required |
|-----------|-------------|----------|
| cohort_id_or_name | Cohort identifier | Yes |
| sql | SELECT query | Yes |
| limit | Max results | No (default: 20) |

### clone_cohort
| Parameter | Description | Required |
|-----------|-------------|----------|
| source_cohort_id | Source cohort | Yes |
| new_name | Name for clone | No (auto-generated) |
| tags | Tags for clone | No (copies source) |

### merge_cohorts
| Parameter | Description | Required |
|-----------|-------------|----------|
| source_cohort_ids | List of sources (min 2) | Yes |
| target_name | Name for merged | No (auto-generated) |
| conflict_strategy | skip/overwrite/rename | No (default: skip) |

### export_cohort
| Parameter | Description | Required |
|-----------|-------------|----------|
| cohort_id | Cohort to export | Yes |
| format | json/csv/parquet | Yes |
| output_path | Destination | No (default: ~/Downloads) |

## Related Skills

- [PatientSim](../patientsim/SKILL.md) - Generate patient data
- [MemberSim](../membersim/SKILL.md) - Generate member/claims data
- [TrialSim](../trialsim/SKILL.md) - Generate clinical trial data
- [DuckDB Skill](./duckdb-skill.md) - Advanced database queries

## Metadata

- **Version**: 5.0
- **Updated**: 2024-12-28
- **Tags**: state-management, persistence, cohorts, query, export
