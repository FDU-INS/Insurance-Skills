---
name: afrexai-insurance-claims
description: "Insurance Claims Processor"
---

# Insurance Claims Processor

Process, analyze, and optimize insurance claims. Covers property, liability, workers' comp, auto, and professional indemnity.

## What This Does

Takes raw claim details and produces:
- Structured claim summary with policy coverage mapping
- Liability assessment with supporting/weakening factors
- Reserve estimate with confidence range
- Subrogation opportunity analysis
- Red flag detection (fraud indicators, coverage gaps)
- Settlement recommendation with negotiation range
- Regulatory compliance checklist by jurisdiction

## Usage

Provide claim details in any format — adjuster notes, policyholder statement, incident report, photos, or free text. The agent structures everything.

### Quick Claim Analysis
```
Analyze this claim: [paste details]
```

### Full Processing
```
Process claim for:
- Policy type: [commercial general liability / property / WC / auto / PI]
- Incident date: [date]
- Reported date: [date]
- Claimant: [name/entity]
- Description: [what happened]
- Claimed amount: [if known]
- Policy limits: [if known]
- Jurisdiction: [state/country]
```

## Claim Analysis Framework

### 1. Coverage Determination
- Map incident to policy provisions
- Identify applicable endorsements and exclusions
- Flag coverage disputes early
- Check occurrence vs claims-made triggers

### 2. Liability Assessment
Score 1-10 on insured liability exposure:
- **1-3**: Strong defense position, deny or minimal settlement
- **4-6**: Mixed liability, negotiate
- **7-10**: Clear insured liability, reserve and settle

Factors evaluated:
- Comparative/contributory negligence (jurisdiction-specific)
- Statutory obligations
- Contractual indemnity provisions
- Prior loss history pattern

### 3. Reserve Estimation
Three-point estimate:
- **Low**: Best case with strong defense
- **Mid**: Most likely outcome
- **High**: Worst case including litigation costs

Include:
- Indemnity reserve
- Defense costs (inside/outside limits)
- Allocated loss adjustment expense (ALAE)
- Unallocated loss adjustment expense (ULAE)

### 4. Fraud Detection
Red flags scored by severity:
- Claim timing patterns (Monday morning, policy inception proximity)
- Prior claim frequency
- Documentation inconsistencies
- Witness availability issues
- Financial stress indicators
- Description vs damage inconsistency

### 5. Subrogation Analysis
- Third-party recovery potential
- Evidence preservation requirements
- Statute of limitations by jurisdiction
- Cost-benefit of pursuit

### 6. Settlement Strategy
- Opening position and authority range
- Mediation vs litigation cost comparison
- Jurisdiction-specific verdict ranges
- Structured settlement considerations for large claims

## Industry-Specific Modules

### Property Claims
- Replacement cost vs actual cash value
- Business interruption calculations (gross earnings, extra expense)
- Ordinance or law coverage triggers
- Catastrophe event coordination

### Workers' Compensation
- Compensability determination
- Return-to-work timeline
- Medical treatment guidelines by state
- Permanent disability rating estimates

### Professional Liability
- Discovery rule and statute of repose
- Prior acts coverage analysis
- Consent to settle provisions
- Panel counsel selection criteria

### Auto/Fleet
- Comparative fault allocation
- UM/UIM stacking analysis
- Medical payment coordination
- Total loss threshold calculations

## Compliance Checklist Generator
Produces jurisdiction-specific compliance timeline:
- Acknowledgment deadlines
- Investigation completion requirements
- Payment timing obligations
- Required notices and disclosures
- Bad faith exposure triggers

## Output Format

Every analysis produces:
1. **Executive Summary** — 3-line claim snapshot
2. **Coverage Analysis** — provisions, exclusions, disputes
3. **Liability Score** — 1-10 with reasoning
4. **Reserve Recommendation** — low/mid/high with breakdown
5. **Red Flags** — fraud indicators if any
6. **Action Items** — next steps with deadlines
7. **Settlement Range** — if applicable

---

Built by [AfrexAI](https://afrexai-cto.github.io/context-packs/) — AI agent context packs for every industry.

Get the full **Insurance & Risk Management Context Pack** with claims processing, underwriting automation, policy analysis, and actuarial modeling: [AfrexAI Storefront](https://afrexai-cto.github.io/context-packs/)

Calculate what AI agents save your claims operation: [AI Revenue Calculator](https://afrexai-cto.github.io/ai-revenue-calculator/)
