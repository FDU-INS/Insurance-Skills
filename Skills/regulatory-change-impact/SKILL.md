---
name: regulatory-change-impact
description: Analyze and explain the impact of regulatory rule changes on financial institution operations, risk management, and capital requirements. Use when interpreting new regulations, final rules, NPRMs, supervisory guidance, or assessing compliance implementation requirements for banking, capital markets, or insurance entities.

metadata:
  display_name: "Regulatory Change Impact"
  short_description: "Assess regulatory rule change impact on bank operations"
  default_prompt: "Analyze my banking regulatory change impact and recommend clear next actions"
  version: "1.0.0"
  tags:
    - financial-services
  icon_path: "assets/icon.png"
---

# Regulatory Change Impact Analysis

## Overview

This skill produces structured impact assessments of regulatory changes affecting financial institutions. It covers federal and state banking regulations, prudential standards (Basel III/IV, capital, liquidity), consumer protection rules, BSA/AML requirements, and supervisory guidance from the OCC, Federal Reserve, FDIC, CFPB, SEC, and state regulators. The output maps regulatory changes to affected business lines, systems, policies, and capital requirements.

## When to Use

- Analyzing newly issued final rules, interim final rules, or proposed rules (NPRMs)
- Assessing supervisory guidance (SR letters, OCC bulletins, FDIC FILs)
- Evaluating the impact of consent orders or enforcement actions on peer institutions
- Mapping regulatory changes to internal policies, procedures, and controls
- Estimating capital, liquidity, or operational cost impacts of rule changes
- Preparing board or senior management briefings on regulatory developments
- Supporting comment letter drafting for proposed rules

## Required Inputs

| Input | Description | Format |
|-------|-------------|--------|
| Regulatory text | Final rule, NPRM, guidance, or bulletin | Full text or Federal Register citation |
| Issuing agency | OCC, Fed, FDIC, CFPB, SEC, FinCEN, state | Agency identification |
| Institution profile | Asset size, charter type, business lines, complexity | Institutional context |
| Current compliance state | Existing policies, systems, controls for affected area | Gap baseline |
| Effective/compliance dates | Implementation timeline and phase-in periods | Date schedule |
| Peer analysis (optional) | How similarly situated institutions are responding | Industry intelligence |

## Methodology

### Step 1: Parse the Regulatory Change

Deconstruct the regulatory issuance into actionable components:

1. **Identify the rule type**: Final rule, interim final rule, NPRM (proposed), guidance (non-binding), FAQ, or enforcement action
2. **Determine applicability**: Asset size thresholds, charter type, activity triggers, de minimis exemptions
3. **Extract key provisions**: New requirements, modified requirements, eliminated requirements
4. **Map effective dates**: Publication date, effective date, compliance date(s), phase-in schedule
5. **Identify related rules**: Cross-references to existing regulations that are amended or superseded

### Step 2: Assess Institutional Applicability

Determine whether and how the rule applies to the institution:

| Factor | Assessment | Impact |
|--------|-----------|--------|
| Asset size threshold | Above / below / near threshold | Full / exempt / monitor |
| Activity trigger | Engaged in covered activities? | Direct / indirect / none |
| Charter type | National bank, state member, savings, BHC | Applicability determination |
| Complexity category | Category I-IV (tailoring framework) | Requirements may vary |
| Subsidiary/affiliate | Consolidated vs. entity-level application | Scope determination |

For institutions near thresholds, assess the likelihood of crossing during the phase-in period and recommend proactive compliance.

### Step 3: Map Impacts by Domain

Systematically assess impact across eight operational domains:

**1. Capital and Liquidity**
- Risk-weighted asset (RWA) changes under standardized and advanced approaches
- Capital ratio impact (CET1, Tier 1, Total Capital, leverage)
- Liquidity coverage ratio (LCR) and net stable funding ratio (NSFR) effects
- Stress capital buffer (SCB) implications
- Output floor phase-in impact (Basel IV 72.5% floor)

**2. Risk Management**
- Model changes required (credit, market, operational risk models)
- Risk appetite statement updates
- Limit framework modifications
- New risk metrics or reporting requirements

**3. Compliance and Legal**
- Policy and procedure updates required
- Training requirements for affected staff
- Compliance monitoring and testing program changes
- Legal opinion requirements

**4. Technology and Data**
- System changes for calculation, reporting, or monitoring
- Data collection and quality requirements
- Regulatory reporting form changes (Call Report, FR Y-9C, FR Y-14)
- Vendor system updates needed

**5. Operations**
- Process changes for affected business activities
- Staffing impact (new roles, additional FTEs)
- Customer-facing process modifications
- Third-party relationship management changes

**6. Financial Reporting**
- Accounting treatment changes (GAAP/IFRS impact)
- Disclosure requirement modifications (10-K, 10-Q, proxy)
- Call Report or regulatory filing changes
- Investor communication requirements

**7. Business Strategy**
- Product or service modifications needed
- Pricing adjustments to reflect new costs
- Market exit or entry considerations
- Competitive positioning impact

**8. Governance**
- Board reporting and approval requirements
- Committee charter modifications
- Management reporting changes
- Audit committee considerations

### Step 4: Quantify the Impact

Where possible, provide quantitative estimates:
- Capital impact in basis points of CET1 and dollar terms
- Compliance cost estimate (one-time implementation + ongoing annual)
- Revenue impact from business model changes
- FTE requirements for implementation and ongoing compliance
- Technology investment estimate (build vs. buy vs. vendor upgrade)
- Timeline: months to implement with critical path milestones

### Step 5: Develop Implementation Roadmap

Create a phased implementation plan:

**Phase 1 — Assessment (0-30 days)**:
- Detailed gap analysis against current state
- Stakeholder identification and RACI assignment
- Budget and resource estimation

**Phase 2 — Design (30-90 days)**:
- Policy and procedure drafting
- System requirements specification
- Data remediation planning
- Training curriculum development

**Phase 3 — Implementation (90-270 days)**:
- System development, configuration, or procurement
- Policy approval through governance
- Staff training delivery
- Parallel testing of new processes

**Phase 4 — Validation (270-365 days)**:
- Compliance testing and gap closure
- Internal audit review
- Regulatory filing dry runs
- Board attestation preparation

### Step 6: Identify Risks and Dependencies

Document implementation risks:
- Vendor readiness for system changes
- Data availability and quality for new requirements
- Competing regulatory projects consuming same resources
- Interpretive uncertainty requiring legal or regulatory clarification
- Industry comment period outcomes that may modify final requirements

### Step 7: Prepare Stakeholder Communication

Tailor the message by audience:
- **Board**: Strategic impact, capital implications, resource commitment, timeline
- **Senior management**: Operational impact, budget request, project governance
- **Business lines**: Product and process changes, customer communication needs
- **Regulators**: Implementation plan, timeline commitment, resource allocation
- **External stakeholders**: Investor impact, public disclosure requirements

## Output Specification

```markdown
# Regulatory Change Impact Assessment

## Rule Summary
- **Regulation**: [Name and citation]
- **Issuing Agency**: [Agency]
- **Rule Type**: [Final / NPRM / Guidance]
- **Publication Date**: [Date]
- **Effective Date**: [Date]
- **Compliance Date**: [Date(s) with phase-in]

## Applicability Determination
- **Applicable**: [Yes / No / Partial]
- **Basis**: [Asset size, activity, charter type]
- **Tailoring Category**: [I-IV, if applicable]

## Impact Summary
| Domain | Impact Level | Key Changes | Estimated Cost |
|--------|-------------|-------------|----------------|
| Capital & Liquidity | [High/Med/Low/None] | [Summary] | [$X] |
| Risk Management | [High/Med/Low/None] | [Summary] | [$X] |
| Compliance & Legal | [High/Med/Low/None] | [Summary] | [$X] |
| Technology & Data | [High/Med/Low/None] | [Summary] | [$X] |
| Operations | [High/Med/Low/None] | [Summary] | [$X] |
| Financial Reporting | [High/Med/Low/None] | [Summary] | [$X] |
| Business Strategy | [High/Med/Low/None] | [Summary] | [$X] |
| Governance | [High/Med/Low/None] | [Summary] | [$X] |

## Capital Impact Analysis
- **CET1 Impact**: [+/- X bps]
- **RWA Change**: [$XM]
- **Binding Constraint Change**: [Yes/No, which ratio]

## Implementation Roadmap
| Phase | Activities | Timeline | Owner |
|-------|-----------|----------|-------|
| Assessment | [Activities] | [Dates] | [Team] |
| Design | [Activities] | [Dates] | [Team] |
| Implementation | [Activities] | [Dates] | [Team] |
| Validation | [Activities] | [Dates] | [Team] |

## Risks and Open Items
- [Risk/dependency with mitigation plan]

## Recommendation
[Executive recommendation on approach, urgency, and resource commitment]
```

## Analysis Framework

### Regulatory Change Classification

Categorize the change by urgency and complexity:

| Complexity \ Urgency | Immediate (<90 days) | Near-term (90-365 days) | Long-term (>1 year) |
|----------------------|---------------------|------------------------|---------------------|
| **Low** (policy update) | Expedite | Standard process | Monitor |
| **Medium** (system + process) | Escalate for resources | Project charter | Plan and budget |
| **High** (capital/strategic) | Executive escalation | Major program | Strategic planning |

### Cross-Rule Interaction Analysis

Assess how the new rule interacts with existing requirements:
- Does it modify or supersede existing regulations?
- Does it create conflicts with state-level requirements?
- How does it interact with other pending proposals?
- Are there cross-border implications (EU CRD VI, UK PRA)?

## Examples

**Example 1 — Basel III Endgame (Capital Rule)**:
"The Basel III Endgame final rule (effective [date]) eliminates the advanced approaches for credit risk and introduces an expanded risk-based approach (ERBA). For our institution ($85B total assets, Category III), the impact assessment shows: CET1 ratio decline of approximately 45 bps under the ERBA due to higher RWA for operational risk (standardized measurement approach) and removal of internal models benefit for credit risk. The output floor phases in at 55% (year 1) to 72.5% (year 5). Technology impact is High: the risk engine requires recalibration for standardized credit risk weights, and a new operational risk capital calculation module must be implemented. Estimated implementation cost: $4.2M one-time, $1.1M annually. Compliance date: July 2026 with 3-year transition."

**Example 2 — CRA Modernization**:
"The interagency CRA final rule modernizes Community Reinvestment Act evaluation for banks above $2B in assets. Impact: our institution must now track and report retail lending and community development activities in assessment areas defined by both branch presence and lending concentration. Technology impact is High: geocoding of all retail loans against new assessment area definitions, new data fields for community development classification. Operations impact is Medium: CRA officer staffing model requires 2 additional FTEs for expanded data collection. Timeline: data collection effective January 2027, first evaluation under new framework 2028."

## Guidelines

- Distinguish between binding rules and non-binding guidance (supervisory expectations vs. legal requirements)
- For NPRMs, note that requirements may change and assess the range of possible outcomes
- Always identify phase-in periods and transitional provisions
- Reference specific regulatory text sections to support impact statements
- Assess both direct costs and indirect strategic impacts
- Consider competitive implications (does the rule advantage or disadvantage certain business models?)
- Flag any provisions requiring legal interpretation or regulatory clarification
- Include sunset provisions or periodic review requirements
- Track related industry comment letters and agency responses for interpretive context

## Validation Checklist

- [ ] Regulatory citation is complete and accurate (CFR part, section, Federal Register page)
- [ ] Applicability determination considers all relevant thresholds and triggers
- [ ] All eight impact domains are assessed (even if impact is "None")
- [ ] Capital impact is quantified in basis points and dollar terms where applicable
- [ ] Implementation roadmap aligns with regulatory compliance dates
- [ ] Cost estimates distinguish one-time from recurring expenses
- [ ] Cross-rule interactions and dependencies are identified
- [ ] Stakeholder communications are tailored by audience
- [ ] Risks and open items have assigned owners and mitigation plans
- [ ] Assessment is reviewed by legal and compliance before distribution
