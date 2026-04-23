---
name: sales
description: >
  Master orchestrator for the sales intelligence engine. Routes /sales commands
  to the correct subagent or skill. Trigger: any message starting with "/sales".
  Flagship command: /sales prospect <url> launches 5 parallel subagents for
  comprehensive prospect analysis. All engines are industry-agnostic — the same
  orchestrator works for SaaS, insurance, real estate, or any vertical by loading
  the appropriate runtime config.
---

## Tier 0 Doctrine

This is a routing hub. It receives a `/sales` command, identifies the target skill,
and dispatches execution. It does not perform analysis itself — subagents and skills
do the work. The orchestrator's job is classification, routing, and aggregation.

**Governed by: Hub-and-Spoke**
- Hub: This orchestrator — receives all `/sales` commands
- Spokes: 13 skills + 5 agents that do the actual work
- Rim: The user — invokes commands, receives outputs

---

## IMO

**Ingress:** User invokes `/sales <command> [arguments]`. Schema validation:
command must match a registered route. Arguments must match the target skill's
expected input type (URL, prospect name, description, or none).

**Middle:** Route to the correct skill. For `/sales prospect`, launch 5 parallel
subagents, collect results, compute composite score, assemble final output. For
all other commands, dispatch to the matching `skills/sales-<command>/SKILL.md`.

**Egress:** Markdown file output (or terminal output for `/sales quick`). Read-only
view of the analysis. No logic in the output — it is a report.

---

## Constants

### Command Registry (Fixed)

| Command | Skill | Output File |
|---------|-------|-------------|
| `/sales prospect <url>` | sales-prospect | PROSPECT-ANALYSIS.md |
| `/sales quick <url>` | (inline) | Terminal output |
| `/sales research <url>` | sales-research | COMPANY-RESEARCH.md |
| `/sales qualify <url>` | sales-qualify | LEAD-QUALIFICATION.md |
| `/sales contacts <url>` | sales-contacts | DECISION-MAKERS.md |
| `/sales outreach <prospect>` | sales-outreach | OUTREACH-SEQUENCE.md |
| `/sales followup <prospect>` | sales-followup | FOLLOWUP-SEQUENCE.md |
| `/sales prep <url>` | sales-prep | MEETING-PREP.md |
| `/sales proposal <client>` | sales-proposal | CLIENT-PROPOSAL.md |
| `/sales objections <topic>` | sales-objections | OBJECTION-PLAYBOOK.md |
| `/sales icp <description>` | sales-icp | IDEAL-CUSTOMER-PROFILE.md |
| `/sales competitors <url>` | sales-competitors | COMPETITIVE-INTEL.md |
| `/sales report` | sales-report | SALES-REPORT.md |
| `/sales report-pdf` | sales-report-pdf | SALES-REPORT-*.pdf |

### Prospect Score Framework (Fixed)

| Category | Weight | Subagent |
|----------|--------|----------|
| Company Fit | 25% | sales-company |
| Contact Access | 20% | sales-contacts |
| Opportunity Quality | 20% | sales-opportunity |
| Competitive Position | 15% | sales-competitive |
| Outreach Readiness | 20% | sales-strategy |

**Composite Score** = Weighted average of all 5 categories (0-100).

### Grade Scale (Fixed)

| Score | Grade | Action |
|-------|-------|--------|
| 90-100 | A+ | Hot Lead — prioritize immediately |
| 75-89 | A | Strong Prospect — significant investment |
| 60-74 | B | Qualified Lead — standard approach |
| 40-59 | C | Lukewarm — nurture, don't hard sell |
| 0-39 | D | Poor Fit — deprioritize or disqualify |

### Output Standards (Fixed)

1. Actionable over theoretical — every recommendation is executable
2. Personalized — tailored to the specific prospect, not generic
3. Revenue-focused — every insight connects to deal probability
4. Evidence-based — cite specific sources and data points
5. Ready to use — outreach emails are copy-paste ready

---

## Variables

| Variable | Source | Changes When |
|----------|--------|-------------|
| Target URL | User input | Every invocation |
| Prospect name | User input or extracted | Every invocation |
| Industry vertical | Runtime config | Config swap |
| Industry-specific signals | Runtime config | Config swap |
| Company type detection rules | Runtime config | Config swap |
| Qualification weight overrides | Runtime config (optional) | Config swap |

---

## Workflow

### BLOCK 1: Command Classification
**Governed by: C&V**

**Constants:**
- Every `/sales` command maps to exactly one skill.
- Unknown commands produce an error with the command registry table.
- `/sales prospect` is the only command that launches parallel subagents.

**Variables:**
- The specific command entered by the user.
- The specific arguments provided.

**IMO:**
- Ingress: Raw user input — `/sales <command> [args]`.
- Middle: Parse command. Match against command registry. If no match, return
  the registry table as help output. If match, identify the target skill path.
- Egress: Classified command + target skill path + parsed arguments.

**Go/No-Go:** Command matches a registered route. Arguments are present if required.

---

### BLOCK 2: Skill Dispatch
**Governed by: Hub-and-Spoke**

**Constants:**
- Each skill lives at `skills/sales-<command>/SKILL.md`.
- The orchestrator reads the skill, then executes it — never modifies it.
- For `/sales prospect`, dispatch 5 subagents in parallel (not sequential).

**Variables:**
- The specific skill being dispatched.
- The specific arguments passed to the skill.

**IMO:**
- Ingress: Classified command from Block 1.
- Middle: If `/sales prospect` → launch 5 parallel subagent calls:
  1. `agents/sales-company.md` → Company research
  2. `agents/sales-contacts.md` → Contact intelligence
  3. `agents/sales-opportunity.md` → Opportunity assessment
  4. `agents/sales-competitive.md` → Competitive analysis
  5. `agents/sales-strategy.md` → Outreach strategy
  For all other commands → read and execute the target skill.
- Egress: Skill execution results (raw outputs from subagents or skill).

**Go/No-Go:** Skill file exists and is readable. Arguments match skill's expected input.

---

### BLOCK 3: Score Aggregation (Prospect Only)
**Governed by: IMO**

**Constants:**
- Aggregation applies ONLY to `/sales prospect` output.
- Weights are fixed: Company 25%, Contacts 20%, Opportunity 20%, Competitive 15%, Strategy 20%.
- Each subagent returns a 0-100 score for its category.
- Composite = weighted sum of all 5 scores.
- Grade assignment uses the fixed grade scale (A+ through D).

**Variables:**
- The 5 individual category scores.
- The resulting composite score and grade.

**IMO:**
- Ingress: Raw outputs from all 5 parallel subagents.
- Middle: Extract category score from each subagent output. Apply weights.
  Calculate composite. Assign grade. If any subagent failed, mark that
  category as "incomplete" and note it in the executive summary.
- Egress: Composite score, grade, and per-category breakdown.

**Go/No-Go:** At least 3 of 5 subagents returned valid scores. If fewer than 3,
flag as incomplete analysis — do not assign a grade.

---

### BLOCK 4: Output Assembly
**Governed by: CTB**

**Constants:**
- Output file includes: prospect URL, date, overall score, executive summary.
- Output is structured with clear headers and tables.
- Output follows the target skill's specified file format.

**Variables:**
- The specific content assembled from skill/subagent outputs.
- The output filename.

**IMO:**
- Ingress: Skill output (Block 2) + score aggregation (Block 3 if prospect).
- Middle: Assemble the final output file:
  - Trunk: The output file itself.
  - Branches: Major sections (summary, detailed findings, recommendations, next steps).
  - Leaves: Specific data points, scores, action items.
  Save to the current directory with the filename from the command registry.
- Egress: Written markdown file (or terminal output for `/sales quick`).

**Go/No-Go:** Output file written successfully. Contains all required sections.

---

## Rules

1. **Never** hardcode industry-specific content into the orchestrator. Industry detection
   rules, vertical-specific signals, and company type heuristics live in runtime config.
2. **Never** execute analysis in the orchestrator. The orchestrator routes — skills analyze.
3. **Never** modify a skill file during execution. Read and execute, never write.
4. **Never** run subagents sequentially when they can run in parallel.
5. **Never** assign a grade when fewer than 3 subagents returned valid scores.
6. **Never** produce output without citing data sources. "Based on our analysis" is not a source.
7. **Never** skip the command classification step. Unknown commands get the help table, not a guess.

---

## Cross-Skill Integration

| Skill | Benefits From | Feeds Into |
|-------|--------------|------------|
| prospect | all 5 subagents | report, report-pdf |
| outreach | research, contacts | followup |
| prep | research, contacts, qualify | proposal |
| proposal | qualify, competitors | (terminal) |
| report | all prospect analyses | report-pdf |
| objections | competitors | prep, outreach |

---

## Quick Snapshot (`/sales quick <url>`)

This is the only command handled inline (no external skill file):

1. Fetch homepage via WebFetch.
2. Evaluate: company size signals, industry fit, tech indicators, growth signals,
   decision maker visibility.
3. Output: scorecard with top 3 opportunities + top 3 concerns.
4. Max 30 lines of terminal output. No file saved.

---

## Reference Pointers

| File | Contains | Load When |
|------|----------|-----------|
| `factory/agents/skill-creator/SKILL.md` | Block format spec | Creating new skills |
| `factory/agents/CAR_SKILL_TEMPLATE.md` | Car-specific skill template | Creating repo-specific skills |
| `agents/*.md` | 5 subagent definitions | `/sales prospect` dispatch |
| `skills/sales-*/SKILL.md` | 13 skill packages | Any `/sales` command |
| `templates/*.md` | Output templates | Skills that generate docs |
