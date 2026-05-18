---
name: ratchet-reduce
description: Extract structured claims from source documents into graph concepts. Adapted from JP's 6R REDUCE phase.
skill_type: graph-extraction
related_skills: [ratchet-reflect, ratchet-reweave, ratchet-verify]
---

# Ratchet REDUCE — Exhaustive Claim Extraction

Extract every distinct claim from a source document and add to the A2 graph.

## Invocation

```
/ratchet-reduce [file_path]          # extract from specific file
/ratchet-reduce inbox                # process all unprocessed source docs
/ratchet-reduce --entropy-first      # process lowest-entropy docs first
```

## EXECUTE NOW Steps

1. **Read source fully.** If >2500 lines, chunk into 350-1200 line segments.
2. **Source entropy check:** Score 1-5 (1=formal spec, 5=raw braindump). If ≥4, quarantine — do NOT extract yet.
3. **Hunt for extractable claims** by category:
   - DEFINITION: "X is Y" / "X means Y"
   - CONSTRAINT: "X must/shall/cannot Y" 
   - RELATIONSHIP: "X depends on/enables/contradicts Y"
   - ASSERTION: "X causes/implies/requires Y"
   - PATTERN: "When X, do Y" / "The pattern is..."
4. **Duplicate check:** For each candidate, check if already in A2 graph:
   - MATCHED → skip
   - PARTIAL → flag for enrichment
   - MISSING → extract as new concept
   - CONTRADICTS → add CONTRADICTS edge
5. **Classify each claim:** OPEN (needs investigation) or CLOSED (standalone, ready)
6. **Present findings** — report by category with counts
7. **Extract** — create concept nodes with:
   - `name`: IS the claim (test: "this concept argues that [name]")
   - `description`: 1-2 sentences, adds info beyond name
   - `tags`: [source_type, domain_area]
   - `trust_zone`: A2_3_INTAKE initially
   - `source_doc`: path to origin
8. **Create SOURCE_MAP edges** from concept to source document

## Quality Gates

**INVALID skip reasons (these are BUGS):**
- "validates existing approach"
- "already captured"  
- "obvious"
- "near-duplicate" (without checking for enrichment)

**Expected yields:**
| Source Size | Expected Outputs |
|-------------|-----------------|
| ~100 lines  | 5-10 claims     |
| ~350 lines  | 15-30 claims    |
| ~1000+ lines| 40-70 claims    |

**Zero extraction from a domain-relevant source is a BUG.**

## Entropy Scoring Reference

| Score | Source Type | Action |
|-------|-----------|--------|
| 1 | Formal spec, schema, contract | Extract first (highest priority) |
| 2 | Structured doc with definitions | Extract second |
| 3 | Mixed structure + prose | Extract with moderate selectivity |
| 4 | Chat log, informal notes | QUARANTINE — process after 1-3 complete |
| 5 | Raw braindump, stream of consciousness | QUARANTINE — last priority |

## Pipeline Chaining

After REDUCE → `/ratchet-reflect [created concepts]` to weave into graph.
