---
name: afrexai-insurance-automation
description: "Insurance Operations Automation"
---

# Insurance Operations Automation

Comprehensive insurance operations framework for AI agents. Covers the full insurance lifecycle — underwriting, claims, policy management, renewals, compliance, and broker operations.

## What This Skill Does

Guides your AI agent through insurance-specific workflows with industry benchmarks, regulatory requirements, and automation priorities.

## Capabilities

### 1. Underwriting Assessment
- Risk scoring framework (12 factors, weighted by line of business)
- Data enrichment checklist (credit, claims history, property data, telematics)
- Referral triggers and authority limits by tier
- Combined ratio targets by line: Auto (95-98%), Home (85-92%), Commercial (88-95%), Life (varies by mortality table)

### 2. Claims Processing Pipeline
- FNOL intake automation (voice + digital, structured extraction)
- Severity triage: Green (auto-approve <$2K) → Yellow (adjuster review $2K-$25K) → Red (SIU referral >$25K or fraud indicators)
- Subrogation identification triggers
- Reserve estimation formulas by claim type
- Settlement authority matrix

### 3. Policy Administration
- Quote-to-bind workflow (target: <15 min for personal lines)
- Mid-term adjustment processing
- Renewal scoring: retention probability model (7 factors)
- Cancellation/non-renewal compliance by state/jurisdiction

### 4. Broker Operations (Jointly AI Model)
- 5-agent pipeline architecture: Intake → Research → Quoting → Analysis → Delivery
- Market panel management and placement optimization
- Quote comparison normalization across carriers
- FCA/state regulatory compliance verification
- Parallel execution: up to 4 simultaneous carrier interactions

### 5. Compliance & Regulatory
- **US:** State DOI requirements, NAIC model laws, Solvency II (reinsurers)
- **UK:** FCA handbook (ICOBS, SYSC), Consumer Duty, IDD compliance
- **EU:** Solvency II, IDD, GDPR for policyholder data
- Anti-fraud indicators (SIU trigger list — 15 red flags)
- SAR/suspicious activity reporting thresholds

### 6. Insurance Metrics Dashboard
| Metric | Personal Lines Target | Commercial Target |
|--------|----------------------|-------------------|
| Combined Ratio | 95-98% | 88-95% |
| Loss Ratio | 60-70% | 55-65% |
| Expense Ratio | 25-32% | 28-35% |
| Claims Settlement Time | <48h (auto) | <14 days |
| Policy Issuance Time | <15 min | <24h |
| Renewal Rate | >85% | >80% |
| Quote-to-Bind Ratio | >25% | >15% |
| NPS | >40 | >35 |

### 7. Automation Priority Matrix
| Process | Hours/Month (50-person broker) | Agent-Ready? | Expected Savings |
|---------|-------------------------------|--------------|-----------------|
| Quote comparison | 160h | Yes — now | $140K-$280K/yr |
| FNOL intake | 120h | Yes — now | $105K-$210K/yr |
| Policy document generation | 80h | Yes — now | $70K-$140K/yr |
| Renewal processing | 100h | Yes — now | $87K-$175K/yr |
| Compliance checks | 60h | Yes — now | $52K-$105K/yr |
| Subrogation identification | 40h | Partial | $35K-$70K/yr |
| Complex claims adjustment | 200h | Human-in-loop | $50K-$100K/yr |

### 8. Insurance-Specific Agent Prompts

**Underwriting Agent:**
```
You are an underwriting assessment agent. For each submission:
1. Extract all risk factors from the application
2. Score each factor against the risk matrix (1-10 scale)
3. Calculate composite risk score (weighted by line of business)
4. Flag any referral triggers (prior losses >3 in 5yr, credit <600, high-hazard occupation)
5. Recommend: Auto-approve / Refer to senior / Decline with reason
6. Generate underwriting memo with supporting data
```

**Claims Triage Agent:**
```
You are a claims triage agent. For each FNOL:
1. Extract: date of loss, type, description, estimated amount, policyholder details
2. Verify active coverage and applicable endorsements
3. Assign severity: Green (<$2K auto-process) / Yellow ($2K-$25K adjuster) / Red (>$25K or fraud flags)
4. Check fraud indicators against the 15-point SIU trigger list
5. Set initial reserve based on claim type benchmarks
6. Route to appropriate handler with priority score
```

## 90-Day Deployment Roadmap

**Month 1:** Deploy intake + quote comparison agents. Target: 70% of personal lines quotes handled autonomously.

**Month 2:** Add claims triage + policy document generation. Target: FNOL processing <5 minutes, auto-approval for Green claims.

**Month 3:** Compliance monitoring + renewal automation. Target: 85%+ renewal rate, zero compliance gaps.

## Cost Framework
- **Solo broker/MGA:** $2K-$5K/month (2-3 agents)
- **Mid-size broker (20-50 staff):** $5K-$15K/month (5-8 agents)
- **Carrier/large broker (100+ staff):** $15K-$50K/month (10-20 agents)

## Resources
- **Calculate your insurance automation ROI →** [AI Revenue Leak Calculator](https://afrexai-cto.github.io/ai-revenue-calculator/)
- **Full Insurance & Fintech Context Pack →** [AfrexAI Context Packs](https://afrexai-cto.github.io/context-packs/) — $47, includes fintech agent configurations, compliance frameworks, and industry benchmarks
- **Configure your insurance agent stack →** [Agent Setup Wizard](https://afrexai-cto.github.io/agent-setup/)
- **Bundle:** Pick 3 packs for $97 | All 10 for $197 | Everything $247
