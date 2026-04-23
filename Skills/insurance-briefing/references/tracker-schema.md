# Story Tracker Schema

The story tracker (`briefings/tracker.json`) provides cross-session memory for the insurance briefing pipeline. It is read before each briefing run and updated after.

## Schema

```json
{
  "meta": {
    "last_updated": "YYYY-MM-DD",
    "briefings_generated": <number>
  },
  "stories": [
    {
      "id": "<kebab-case-identifier>",
      "headline": "<story headline as it appeared in the briefing>",
      "domain": "<primary domain: regulatory|market|industry|reinsurance|cross-domain>",
      "first_covered": "YYYY-MM-DD",
      "last_covered": "YYYY-MM-DD",
      "times_covered": <number>,
      "status": "<new|developing|covered|resolved|archived>",
      "key_facts": ["<fact 1>", "<fact 2>", "..."],
      "last_known_state": "<1-2 sentence summary of where things stand>"
    }
  ]
}
```

## Story Domains (Insurance-Specific)

| Domain | Definition | Examples |
|--------|-----------|----------|
| `regulatory` | SEDDK decisions, law changes, compliance requirements, solvency standards | New capital rule, enforcement action, license suspension, DASK update |
| `market` | Premium trends, underwriting results, investment performance, market share shifts, M&A | Earnings report, premium growth data, investment yield trends, company acquisition |
| `industry` | Competitive moves, company strategy, distribution innovation, product launches | Product launch, digital strategy, distribution partnership, executive change |
| `reinsurance` | Global reinsurance pricing, international CAT events, reinsurance market moves with Turkish relevance | Reinsurance treaty renewal trends, international disaster, reinsurer strategy shift |
| `cross-domain` | Macroeconomic data, interest rates, inflation, geopolitical events, CAT risks with Turkish implications | Inflation release, TCMB rate decision, earthquake, economic downturn signal |

## Story Statuses

| Status | Meaning | Behavior |
|--------|---------|----------|
| `new` | Just added this run | Will be checked for updates next run; expect continuation |
| `developing` | Ongoing story with expected future developments | Scouts actively check for updates each run; will likely resurface |
| `covered` | Story was covered; no further developments expected in next 24-48 hours | Scouts skip unless they find something unexpected |
| `resolved` | Story reached a conclusion or outcome is clear | Scouts skip. Kept in tracker for reference. |
| `archived` | Older than 7 days with status `covered` | Ignored by scouts. Removed from continuity brief. |

## Lifecycle

1. **New story appears in briefing** → added with status `new` (first mention) or `developing` (ongoing saga expected)
2. **Story is covered again with updates** → `times_covered` incremented, `last_covered` updated, `key_facts` appended with new details, `last_known_state` updated
3. **Story has no updates for 2+ days** → status may shift from `developing` to `covered`
4. **Story reaches conclusion or decision point** → status set to `resolved`
5. **Story is older than 7 days and status is `covered`** → status set to `archived`

## Continuity Brief Generation

Before each run, the briefing command reads the tracker and generates a continuity brief:

- **Developing stories:** All stories with status `developing` — scouts actively check for updates and new information
- **Recently covered:** All stories covered in the last 3 days — scouts avoid redundant coverage, but flag genuinely new angles
- **Previous deep dive:** The deep dive topic from the most recent briefing — not to be reused as deep dive, but may surface if new developments emerge

The continuity brief is kept under 800 words to fit within scout context windows.

## Update Rules (post-briefing)

After each briefing is published, the command updates the tracker:

### Stories Covered in Today's Briefing

- **Existing story:** increment `times_covered`, update `last_covered` to today's date
- **New facts discovered:** append to `key_facts` array (avoid exact duplication; be precise)
- **Status update:** update `last_known_state` with 1-2 sentence summary of current situation
- **Status transition:** if story reached conclusion, set status to `resolved`; if new developments are expected, keep as `developing`

### New Stories in Today's Briefing

- **Add new entry** to stories array with:
  - `first_covered` = today's date
  - `last_covered` = today's date
  - `times_covered` = 1
  - `status` = `new` (if single event) or `developing` (if expected to have updates)
  - `key_facts` = initial facts from briefing
  - `last_known_state` = summary of story as covered

### Untouched Stories (Not Covered Today)

- **Older than 7 days AND status `covered`:** set status to `archived`
- **Status `developing` AND not updated in 5+ days:** consider shifting to `covered` (editorial judgment; use if no new information emerged despite checking)

### Pruning

- **Archived stories:** Keep in tracker for reference, but exclude from continuity brief
- **Stories reaching `resolved`:** Keep in tracker indefinitely for context, but don't check for updates

## Example Tracker Entry Lifecycle

**Day 1 (March 1):** SEDDK issues new underwriting standard

```json
{
  "id": "seddk-new-underwriting-standard-mar-2026",
  "headline": "SEDDK Issues Mandatory New Underwriting Standards for Motor Insurance",
  "domain": "regulatory",
  "first_covered": "2026-03-01",
  "last_covered": "2026-03-01",
  "times_covered": 1,
  "status": "developing",
  "key_facts": ["SEDDK issued Circular No. 123/2026", "Effective April 1, 2026", "Applies to motor insurance underwriting process"],
  "last_known_state": "SEDDK has mandated new underwriting documentation requirements for motor policies effective April 1. Implementation details to be clarified."
}
```

**Day 3 (March 3):** Companies issue guidance on implementation

```json
{
  "id": "seddk-new-underwriting-standard-mar-2026",
  "headline": "SEDDK Issues Mandatory New Underwriting Standards for Motor Insurance",
  "domain": "regulatory",
  "first_covered": "2026-03-01",
  "last_covered": "2026-03-03",
  "times_covered": 2,
  "status": "developing",
  "key_facts": ["SEDDK issued Circular No. 123/2026", "Effective April 1, 2026", "Applies to motor insurance underwriting process", "DASK and three major insurers published implementation guidance"],
  "last_known_state": "Major insurers have published guidance for April 1 implementation. Key requirement: new risk assessment form for age and claims history factors."
}
```

**Day 6 (March 6):** No new developments, status shifts

```json
{
  "id": "seddk-new-underwriting-standard-mar-2026",
  "headline": "SEDDK Issues Mandatory New Underwriting Standards for Motor Insurance",
  "domain": "regulatory",
  "first_covered": "2026-03-01",
  "last_covered": "2026-03-03",
  "times_covered": 2,
  "status": "covered",
  "key_facts": ["SEDDK issued Circular No. 123/2026", "Effective April 1, 2026", "Applies to motor insurance underwriting process", "DASK and three major insurers published implementation guidance"],
  "last_known_state": "Regulation effective April 1. Major insurers have published implementation guidance."
}
```

**Day 10+ (March 10+):** Story archived

```json
{
  "id": "seddk-new-underwriting-standard-mar-2026",
  "status": "archived",
  ...
}
```

## Quality Guidelines for Tracker Entries

### Headline
- Capture the story as it appeared in the briefing (exact quote or close paraphrase)
- Not a summary; the actual headline

### Key Facts
- Add new facts only when they represent genuine new information, not repetition
- Be specific: "April 1 effective date" not just "implementation details"
- Remove duplicate facts when updating

### Last Known State
- Always update this when you cover the story again
- Capture progression: "Previously X. Now Y. Next step is Z."
- Keep to 1-2 sentences max

### Status Transitions
- `new` → `developing` (if story is expected to have follow-ups)
- `developing` → `covered` (if no updates in 5+ days and no further action expected)
- Any status → `resolved` (when story reaches conclusion or decision point)
- `covered` + older than 7 days → `archived`
