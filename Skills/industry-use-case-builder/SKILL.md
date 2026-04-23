---
name: industry-use-case-builder
description: "Guide creation of new industry use cases for the Adobe Experience Platform blueprints repository. Use this skill when adding a new use case to an industry vertical (retail, automotive, healthcare, financial services, insurance, media & entertainment, telecommunications, travel & hospitality, B2B), when the user wants to add business scenarios to industry pages, or when updating the use case catalog. Handles the full workflow: gathering use case details, assessing maturity level, generating content, updating the industry overview page and use case catalog, and invoking the use-case-icon-generator skill for icon creation."
---

# Industry Use Case Builder

This skill guides the creation of new industry use cases for the Adobe Experience Platform blueprints repository. Follow each phase sequentially. Read the reference files before beginning:

- `references/use-case-template.md` — exact template for use case sections
- `references/catalog-row-template.md` — exact format for catalog table rows
- `references/maturity-criteria.md` — detailed rubric for maturity assessment

## Phase 1: Information Gathering

Interview the user to collect all required details before generating any content.

### Required fields

1. **Industry vertical** — Must be one of:
   - automotive
   - b2b
   - financial-services
   - healthcare
   - insurance
   - media-entertainment
   - retail
   - telecommunications
   - travel-hospitality

2. **Use case name** — A clear, descriptive title (e.g., "Abandoned Cart Email Recovery", "Medication Adherence Campaigns").

3. **Description** — 1-2 sentences describing the business scenario and why it matters.

4. **Business impact** — Quantified outcomes with specific metrics (e.g., "20-30% increase in click-through rates", "15-25% improvement in refill rates").

5. **Use case pattern** — Must map to exactly one of these existing patterns:
   - Audience Activation to Destinations
   - Audience Collaboration with Segment Match
   - Event Forwarding
   - B2B Audience Activation
   - Anonymous Visitor Web Personalization
   - Known-Visitor Web/App Personalization
   - Offer Decisioning
   - Behavioral Recommendation
   - Batch Outbound Message Activation
   - Event-Triggered Messaging
   - Multi-Step Orchestrated Journey
   - Cross-Channel Journey with Decisioning
   - Buying Group-Based Marketing & Journey Management
   - Customer Analytics & Insight Generation
   - B2B Analytics
   - Brand Concierge Conversational Experience

6. **Technical considerations** — 4-8 bullet points covering data requirements, integrations, regulatory/compliance needs, performance considerations, and architectural notes.

Ask for any missing fields before proceeding. Do not assume or fabricate details.

## Phase 2: Maturity Assessment

Read `references/maturity-criteria.md` for the full rubric. Assign one of three maturity levels:

- **Foundational** `[!BADGE Foundational]{type=Neutral}` — Single-step or event-triggered patterns (Event-Triggered Messaging, Batch Outbound), straightforward data requirements, minimal AI/ML, standard integrations.
- **Emerging** `[!BADGE Emerging]{type=Informative}` — Multi-step journeys, behavioral data, recommendation models, known-visitor personalization, moderate integration complexity.
- **Advanced** `[!BADGE Advanced]{type=Caution}` — Cross-channel decisioning, AI-powered prediction, offer decisioning, complex orchestration, multiple system integrations.

### Assessment workflow

1. Identify which use case pattern the use case maps to.
2. Check the "Typical patterns" list in the maturity criteria for a quick match.
3. If the pattern does not clearly indicate maturity, evaluate data complexity, AI/ML requirements, and integration scope.
4. Present the assessment to the user with reasoning: "Based on the pattern mapping ({pattern}) and {key factors}, I'd classify this as {level} because {reasoning}."
5. Wait for the user to confirm or override before proceeding to content generation.

## Phase 3: Content Generation

Generate or update content in two files.

### A. Industry overview file

**File path:** `/help/blueprints/industry-use-cases/{industry}/{industry}-overview.md`

Read the existing file first to understand current structure and content. Then add a new section following the exact template from `references/use-case-template.md`:

```markdown
## {Use Case Title}

{1-2 sentence description of the business scenario and why it matters}

### Business impact

{Quantified business outcomes, e.g., "Retailers typically see a 20-30% increase in click-through rates..."}

### How to implement

Use the [{Pattern Name}](/help/blueprints/use-case-patterns/{category}/{pattern-file}.md) pattern. {1-2 sentence explanation of why this pattern applies}

### Technical considerations

- {4-8 bullet points covering data integration, regulatory, performance, or architectural considerations}
```

Place the new section after existing use case sections, maintaining consistent formatting.

### B. Use case catalog

**File path:** `/help/blueprints/industry-use-cases/use-case-catalog.md`

Read the existing catalog file first. Add a new row to the correct industry tab. The catalog uses a tabbed structure with `>[!TAB {Industry}]` markers. Each tab contains a table with these columns:

| Column | Content |
| --- | --- |
| Icon | `<img src="assets/use-case-icons/{industry}/icon-{kebab-name}.png" alt="{Alt Text}" width="40">` (leave empty if no icon yet) |
| Use Case | `[{Use Case Title}]({industry}/{industry}-overview.md#{anchor})` where anchor is the heading in kebab-case |
| Description | One-sentence summary |
| Maturity | Badge syntax for the assigned level |
| Pattern | `[{Pattern Name}](/help/blueprints/use-case-patterns/{category}/{pattern-file}.md)` |

**Placement rule:** Within each industry tab, rows are grouped by maturity in this order: Foundational first, then Emerging, then Advanced. Place the new row at the end of the correct maturity group.

The pattern file paths are:
- `audience-building-activation/audience-activation-to-destinations.md`
- `audience-building-activation/audience-collaboration-segment-match.md`
- `audience-building-activation/event-forwarding.md`
- `audience-building-activation/b2b-audience-activation.md`
- `personalization/anonymous-visitor-web-personalization.md`
- `personalization/known-visitor-web-app-personalization.md`
- `personalization/offer-decisioning.md`
- `personalization/behavioral-recommendation.md`
- `campaign-management-orchestration/batch-outbound-message-activation.md`
- `campaign-management-orchestration/event-triggered-messaging.md`
- `campaign-management-orchestration/multi-step-orchestrated-journey.md`
- `campaign-management-orchestration/cross-channel-journey-with-decisioning.md`
- `campaign-management-orchestration/buying-group-based-marketing.md`
- `analysis/customer-analytics-insight-generation.md`
- `analysis/b2b-analytics.md`
- `conversational-experience/brand-concierge-conversational-experience.md`

## Phase 4: Icon Generation

After content is created, invoke the `use-case-icon-generator` skill to generate an icon specification for the new use case. Provide the skill with:
- The use case name
- The industry vertical
- A brief description of the use case

Once the user has the generated icon file, update the catalog row to include the icon reference:
```
<img src="assets/use-case-icons/{industry}/icon-{kebab-name}.png" alt="{Alt Text}" width="40">
```

## Phase 5: Validation

Before finishing, verify all of the following:

1. **Template compliance** — The industry overview section follows the template exactly (## heading, description, ### Business impact, ### How to implement, ### Technical considerations).
2. **Catalog placement** — The catalog row is in the correct industry tab and in the correct maturity group (Foundational, then Emerging, then Advanced).
3. **Pattern link validity** — The pattern link in both the overview and catalog uses a valid pattern file path from the list above.
4. **Anchor consistency** — The anchor in the catalog link (e.g., `#abandoned-cart-email-recovery`) matches the `##` heading in the overview file converted to kebab-case.
5. **Icon path conventions** — The icon path follows `assets/use-case-icons/{industry}/icon-{kebab-name}.png`.

Report any issues found during validation and fix them before completing.
