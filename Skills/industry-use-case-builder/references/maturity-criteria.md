# Use Case Maturity Assessment Criteria

## Maturity Levels

### Foundational

**Badge:** `[!BADGE Foundational]{type=Neutral}`

A use case is **Foundational** when it:

- Maps to a single-step or event-triggered pattern (Event-Triggered Messaging, Batch Outbound Message Activation)
- Has straightforward data requirements (single event type, standard profile attributes)
- Requires minimal or no AI/ML capabilities
- Uses standard channel delivery (email, SMS, push) without complex orchestration
- Has well-established implementation patterns with clear best practices
- Requires fewer system integrations (typically 1-2 data sources)

**Typical patterns:** Event-Triggered Messaging, Batch Outbound Message Activation

**Examples:** Abandoned cart recovery, appointment reminders, service notifications, price drop alerts, bill payment reminders

### Emerging

**Badge:** `[!BADGE Emerging]{type=Informative}`

A use case is **Emerging** when it:

- Maps to a multi-step or personalization pattern (Multi-Step Orchestrated Journey, Known-Visitor Personalization, Behavioral Recommendation, Anonymous Visitor Personalization)
- Requires behavioral data collection and analysis
- Uses recommendation models or known-visitor profile resolution
- Involves multi-touch nurture sequences with branching logic
- Has moderate integration complexity (2-4 data sources)
- May require audience activation or segment-based targeting

**Typical patterns:** Multi-Step Orchestrated Journey, Known-Visitor Web/App Personalization, Behavioral Recommendation, Anonymous Visitor Web Personalization, B2B Audience Activation

**Examples:** Welcome series, medication adherence campaigns, personalized account dashboards, lead scoring, content recommendations

### Advanced

**Badge:** `[!BADGE Advanced]{type=Caution}`

A use case is **Advanced** when it:

- Maps to a decisioning or cross-channel orchestration pattern (Cross-Channel Journey with Decisioning, Offer Decisioning)
- Requires AI-powered prediction or propensity scoring
- Uses centralized decision logic across multiple channels simultaneously
- Involves complex orchestration with real-time decisioning at multiple journey points
- Has high integration complexity (4+ data sources, real-time data feeds)
- Requires sophisticated business rules, priority management, and frequency governance

**Typical patterns:** Cross-Channel Journey with Decisioning, Offer Decisioning

**Examples:** Churn prevention with AI scoring, life-stage product recommendations, cross-sell optimization, loyalty program personalization, VIP exclusive offers

## Assessment Workflow

1. Identify which use case pattern the use case maps to
2. Check the "Typical patterns" list above for a quick match
3. If the pattern doesn't clearly indicate maturity, evaluate the data complexity, AI/ML requirements, and integration scope
4. Present the assessment to the user with reasoning: "Based on the pattern mapping ({pattern}) and {key factors}, I'd classify this as {level} because {reasoning}."
5. Let the user confirm or override before proceeding
