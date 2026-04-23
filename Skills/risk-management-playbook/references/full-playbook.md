# Risk Management Playbook — Full Reference

## Table of Contents

1. [Risk Governance Deep Dive](#1-risk-governance-deep-dive)
2. [Enterprise Risk Assessment Details](#2-enterprise-risk-assessment-details)
3. [Business Continuity Planning Advanced](#3-business-continuity-planning-advanced)
4. [Disaster Recovery Advanced](#4-disaster-recovery-advanced)
5. [Scenario Planning Methodology](#5-scenario-planning-methodology)
6. [Fraud Prevention Advanced](#6-fraud-prevention-advanced)
7. [Fraud Governance Framework & Checklists](#7-fraud-governance-framework--checklists)
8. [Reputational Risk Advanced](#8-reputational-risk-advanced)
9. [Geopolitical Risk Advanced](#9-geopolitical-risk-advanced)
10. [Insurance & Risk Transfer Advanced](#10-insurance--risk-transfer-advanced)
11. [Crisis Communication Playbook](#11-crisis-communication-playbook)
12. [Testing & Exercises Advanced](#12-testing--exercises-advanced)
13. [Key Risk Indicators & Dashboards](#13-key-risk-indicators--dashboards)
14. [Implementation Roadmap](#14-implementation-roadmap)
15. [Multi-Jurisdictional Compliance Matrix](#15-multi-jurisdictional-compliance-matrix)
16. [Templates & Checklists](#16-templates--checklists)

---

## 1. Risk Governance Deep Dive

### Board & Risk Committee Responsibilities
- Set and review risk appetite annually (or after material events)
- Approve enterprise risk management framework
- Review enterprise risk register at least quarterly
- Ensure adequate resources allocated to risk management
- Oversee crisis preparedness and exercise programme
- Challenge management assumptions on residual risk
- Monitor regulatory developments and compliance posture

### CRO / Head of Risk Responsibilities
- Maintain the enterprise risk framework and ensure its adoption
- Facilitate risk assessments across all business units
- Escalate material risks and emerging threats to the board
- Coordinate cross-functional risk response
- Drive risk culture through training, communication, and incentives
- Own the risk reporting and dashboard infrastructure
- Ensure external audit findings are addressed on schedule

### Risk Appetite Statement Template
```
[Organisation Name] accepts [low/moderate/high] levels of [risk category] risk
in pursuit of [strategic objective]. The maximum acceptable [metric] is [threshold].
Risks exceeding this threshold require [escalation path] approval before proceeding.
```

### Risk Culture Assessment Questions
- Do employees understand how their daily actions contribute to risk?
- Can staff articulate the escalation pathway for reporting concerns?
- Are near-misses and incidents reported without fear of blame?
- Is risk discussed in regular business meetings (not just compliance forums)?
- Do performance reviews incorporate risk management behaviours?
- Is there visible executive engagement with risk management?

---

## 2. Enterprise Risk Assessment Details

### Risk Register Fields
| Field | Description |
|---|---|
| Risk ID | Unique identifier |
| Risk Description | Clear, specific description of the risk event |
| Category | Strategic / Operational / Financial / Compliance / Cyber / Reputational / Geopolitical / Climate |
| Risk Owner | Named individual accountable for managing this risk |
| Likelihood Score | 1–5 scale |
| Impact Score | 1–5 scale |
| Inherent Risk Rating | Likelihood × Impact (before controls) |
| Current Controls | Existing mitigations in place |
| Control Effectiveness | Strong / Adequate / Weak |
| Residual Risk Rating | Risk level after controls applied |
| Risk Response | Accept / Mitigate / Transfer / Avoid |
| Planned Actions | Specific actions to reduce residual risk |
| Action Owner | Named individual responsible for action |
| Target Date | Deadline for action completion |
| Status | Open / In Progress / Complete / Overdue |
| Last Reviewed | Date of most recent review |

### BIA Process Step-by-Step
1. Identify all business processes and map to departments/teams
2. Classify each process: mission-critical, important, supportive, non-essential
3. For each mission-critical process, determine:
   - Financial impact of downtime (per hour, per day, per week)
   - Customer impact (SLA breaches, churn, complaint volume)
   - Regulatory impact (reporting obligations, licence conditions)
   - Reputational impact (media attention, social media escalation)
   - Employee safety implications
4. Identify dependencies: IT systems, data, third-party services, key personnel, physical facilities
5. Define RTO, RPO, MAD, and MBCO for each critical process
6. Identify single points of failure and interdependencies
7. Validate with process owners and senior management
8. Document and maintain (review after any material change)

### Dependency Mapping
For each critical process, map:
- **Technology dependencies** — servers, applications, databases, network, cloud services
- **People dependencies** — key personnel, specialised skills, minimum staffing levels
- **Facility dependencies** — office space, data centres, warehouses, branch locations
- **Vendor dependencies** — third-party services, SaaS platforms, payment processors
- **Data dependencies** — databases, file stores, real-time feeds, regulatory data
- **Supply chain dependencies** — raw materials, logistics, distribution partners

---

## 3. Business Continuity Planning Advanced

### BCP Document Structure
1. **Plan Overview** — Purpose, scope, assumptions, activation criteria
2. **Governance** — BCP team, roles, authority levels, escalation matrix
3. **Risk Assessment Summary** — Top risks, likelihood, impact
4. **BIA Summary** — Critical processes, RTOs, RPOs, dependencies
5. **Continuity Strategies** — For each critical function:
   - Primary strategy (e.g., failover to secondary site)
   - Secondary strategy (e.g., manual workaround)
   - Resource requirements (people, technology, space, budget)
6. **Incident Response Procedures** — Detection, assessment, escalation, containment
7. **Communication Plan** — Internal, external, regulatory, media
8. **Recovery Procedures** — Step-by-step for each critical function
9. **Vendor Continuity** — Critical vendor list, SLAs, contacts, alternative providers
10. **Training & Awareness** — Programme schedule, content, attendance tracking
11. **Testing Schedule** — Exercise types, frequency, success criteria
12. **Plan Maintenance** — Review cycle, change triggers, version control

### Vendor Continuity Management
Categorise all vendors into tiers:
| Tier | Criteria | BCP Requirement |
|---|---|---|
| Critical | Business cannot operate without this vendor | Validated vendor BCP, SLA with recovery commitments, tested failover, alternative provider identified |
| Important | Significant impact if unavailable >24hrs | Vendor BCP on file, annual review, manual workaround documented |
| Supportive | Inconvenient but manageable if unavailable | Contact information current, general awareness of alternatives |
| Non-essential | No operational impact | No specific BCP action required |

### Remote Work Continuity
- Secure remote access to all critical systems (VPN, MFA, SSO)
- Hardware provisioning for off-site employees
- Cybersecurity controls adapted for remote (endpoint security, secure DNS)
- Communication tools tested under load (video, chat, document sharing)
- Employee wellbeing considerations for sustained remote operation
- Stress-test response protocols under remote/hybrid configurations

---

## 4. Disaster Recovery Advanced

### DR Runbook Template
For each system in the recovery plan:
```
SYSTEM: [System Name]
CRITICALITY: [Tier 1/2/3/4]
RTO: [Target]
RPO: [Target]
OWNER: [Name, Contact]
BACKUP DETAILS:
  - Method: [Full/Incremental/Differential]
  - Frequency: [Hourly/Daily/Weekly]
  - Location: [On-prem/Cloud/Hybrid]
  - Retention: [Days/Weeks/Months]
  - Encryption: [Yes/No, Method]
  - Last successful test restore: [Date]
FAILOVER PROCEDURE:
  1. [Step-by-step instructions]
  2. [DNS changes required]
  3. [Authentication reconfiguration]
  4. [Verification checks]
RECOVERY PROCEDURE:
  1. [Step-by-step restoration]
  2. [Data integrity validation]
  3. [Service verification]
  4. [User notification and access restoration]
DEPENDENCIES: [List of upstream/downstream systems]
ROLLBACK PROCEDURE: [Steps to revert if recovery fails]
```

### Cloud DR Considerations
- **Data residency** — Ensure backup locations comply with data sovereignty requirements (GDPR, local regulations)
- **Egress costs** — Factor in data transfer costs for large-scale recovery events
- **Multi-cloud strategy** — Avoid single-provider dependency (2025 AWS outage impacted 2,000+ companies)
- **Testing under load** — Cloud failover must be tested with realistic traffic patterns, not just connectivity
- **Configuration drift** — Ensure DR environment mirrors production; automate configuration management
- **Shared responsibility** — Cloud provider manages infrastructure; you manage data, access, and application recovery

### DR Test Success Criteria
| Criterion | Measure |
|---|---|
| RTO Met | System restored within target time |
| RPO Met | Data loss within acceptable window |
| Data Integrity | No corruption detected post-recovery |
| Application Functionality | All critical functions operational |
| User Access | All authorised users can authenticate and work |
| External Integration | APIs, payment systems, third-party feeds operational |
| Communication | Stakeholders notified per protocol |
| Documentation | All steps logged, issues captured |

---

## 5. Scenario Planning Methodology

### Seven-Step Process
1. **Set Objectives** — Test strategies? Identify blind spots? Prepare for specific disruptions?
2. **Identify Key Drivers** — Economic, technology, regulatory, geopolitical, social, environmental
3. **Determine Critical Uncertainties** — Highest impact + most unpredictable drivers form scenario axes
4. **Construct Scenarios** — 3–4 internally consistent narratives of distinct plausible futures
5. **Analyse Implications** — Impact on business model, operations, supply chain, talent, finances
6. **Formulate Strategies** — No-regret moves (good in all scenarios) + hedging strategies
7. **Implement & Monitor** — Embed in strategic planning, set early-warning indicators and triggers

### Scenario Types
| Type | Description | Use Case |
|---|---|---|
| Quantitative | Financial projections under optimistic/pessimistic/base | Budget, capital allocation, investor comms |
| Operational | What-if for specific events affecting current operations | Supply chain, outage, key-person loss |
| Normative | Preferred end state, working backward to define path | Vision setting, transformation roadmaps |
| Strategic Management | Broad external forces (PESTEL) impacting markets | Market entry, competitive strategy, M&A |

### Integrating AI into Scenario Planning
- Process large datasets to identify weak signals and emerging patterns
- Natural language processing of news, earnings calls, regulatory filings
- Monte Carlo simulations for data-driven probability distributions
- Automated scenario narrative generation from multiple data sources
- Distinguish urgent near-term risks from deeper structural shifts
- Continuously update scenarios as new data arrives

### Scenario Planning Workshop Format
**Duration:** Half-day to full day
**Participants:** Cross-functional (exec, strategy, risk, ops, finance, tech, legal)
**Agenda:**
1. Context setting — External environment scan (30 min)
2. Driver identification — Brainstorm and prioritise key forces (45 min)
3. Uncertainty mapping — Plot drivers on impact vs. uncertainty matrix (30 min)
4. Scenario construction — Small groups develop 3–4 narratives (90 min)
5. Implications analysis — What breaks? What thrives? Per scenario (60 min)
6. Strategy formulation — No-regret moves, hedges, triggers (60 min)
7. Action planning — Assign owners, timelines, monitoring (30 min)

---

## 6. Fraud Prevention Advanced

### Fraud Risk Assessment Process
1. Identify fraud risk factors specific to your industry and business model
2. Map fraud vulnerability points across the transaction lifecycle:
   - Onboarding (identity fraud, synthetic identities)
   - Transaction processing (payment fraud, authorisation bypass)
   - Account management (account takeover, social engineering)
   - Reporting and reconciliation (internal fraud, manipulation)
3. Score each vulnerability: likelihood × impact × control effectiveness
4. Define fraud risk tolerance per category
5. Design controls proportionate to risk level
6. Monitor, test, and refine continuously

### AI-Powered Fraud Detection Stack
| Layer | Technology | Purpose |
|---|---|---|
| Identity Verification | Document AI, biometric, liveness | Prevent onboarding fraud |
| Transaction Monitoring | ML anomaly detection, rules engine | Flag suspicious activity in real time |
| Behavioural Analytics | Session analysis, device fingerprint | Detect account takeover |
| Network Analysis | Graph analytics, link analysis | Identify fraud rings and mule networks |
| Case Management | Workflow automation, investigation tools | Efficient triage and resolution |

### Fraud Response Procedure
1. **Detect** — Alert triggered by monitoring system or human report
2. **Assess** — Determine severity, scope, and immediate risk
3. **Contain** — Block suspect transactions, freeze accounts if necessary
4. **Investigate** — Gather evidence, interview parties, analyse patterns
5. **Report** — File regulatory reports (SARs, STRs) within required timeframes
6. **Recover** — Attempt fund recovery, coordinate with law enforcement
7. **Remediate** — Fix control gaps, update detection rules, retrain staff
8. **Learn** — Feed insights back into risk assessment and prevention

---

## 7. Fraud Governance Framework & Checklists

### Fraud Prevention Checklist
- [ ] Anti-fraud policy approved by board and communicated to all staff
- [ ] Fraud risk register maintained and reviewed quarterly
- [ ] Segregation of duties enforced for all critical processes
- [ ] Dual approval required for all payments above threshold
- [ ] Background checks conducted on all new employees
- [ ] Fraud awareness training completed annually by all staff
- [ ] Whistleblower/anonymous reporting channel operational and promoted
- [ ] Transaction monitoring system deployed and tuned
- [ ] Real-time alerting for anomalous activity
- [ ] Vendor and third-party fraud controls assessed
- [ ] Insurance coverage (crime, fidelity, cyber) reviewed annually
- [ ] Regulatory reporting procedures documented and tested
- [ ] Incident response plan for fraud events documented and exercised
- [ ] Post-incident lessons learned fed back into controls

### Payment Security Controls
- Validate all payment instruction changes by calling a trusted, independently verified number
- Never trust contact details provided on invoices (fraudsters replace them)
- Implement Positive Pay and Payee Positive Pay for check payments
- Disable unnecessary USB/CD/DVD and cloud access on financial systems
- Keep browsers, plugins, antivirus, and firewalls current
- Social media training: employees must not share sensitive business information online
- Conduct regular phishing simulations and track click-through rates

---

## 8. Reputational Risk Advanced

### Reputational Risk Quantification
Traditional approaches treated reputational risk qualitatively. Advanced methods include:
- **NLP-based sentiment analysis** of news and social media (real-time)
- **Correlation analysis** between sentiment scores and financial indicators (revenue, share price, customer acquisition)
- **Scenario modelling** of reputational events and estimated financial impact
- **Stakeholder perception surveys** (customers, employees, investors, regulators)
- **Brand health metrics** — awareness, consideration, preference, advocacy tracked over time

### Vendor Reputational Risk Categories
| Category | Description | Monitoring |
|---|---|---|
| Cybersecurity | Vendor breach exposes your data/customers | SecurityScorecard, vendor SOC 2, penetration test results |
| Compliance | Vendor violates regulations, implicating you | Regulatory filings, sanctions screening, compliance certifications |
| Financial | Vendor financial instability disrupts service | Credit reports, financial statements, payment behaviour |
| Strategic | Vendor actions misaligned with your values | News monitoring, ESG ratings, public controversies |
| Operational | Vendor service failure reflects on your brand | SLA monitoring, incident tracking, customer feedback |

### Reputational Crisis Response Playbook
1. **First 60 minutes** — Activate crisis team, assess facts, issue holding statement
2. **Hours 2–6** — Detailed assessment, stakeholder notification, media response prepared
3. **Hours 6–24** — Public statement if warranted, customer communication, regulatory notification
4. **Days 2–7** — Root cause analysis underway, remediation plan communicated, ongoing monitoring
5. **Weeks 2–4** — Remediation progress updates, stakeholder rebuilding, lessons learned
6. **Month 2+** — Long-term recovery programme, sentiment monitoring, trust rebuilding initiatives

---

## 9. Geopolitical Risk Advanced

### Geopolitical Exposure Assessment
Map the following for every jurisdiction where you operate or have dependencies:
- Revenue generated / concentrated
- Assets and infrastructure located
- Supply chain links and alternatives
- Data stored or processed
- Intellectual property exposed
- Regulatory licensing and compliance obligations
- Key personnel and talent dependencies
- Banking and payment infrastructure dependencies

### Five Steps for Geopolitical Resilience (KPMG Framework)
1. **Treat risk as an asset** — Align geopolitical risk with strategic objectives
2. **Build holistic risk management** — From reactive to proactive
3. **Develop scenario-based strategies** — Multiple plausible geopolitical futures
4. **Diversify systematically** — Supply chains, markets, talent, data
5. **Engage with the policy environment** — Advocate for clarity, participate in shaping outcomes

### Sanctions Compliance Essentials
- Screen all customers, counterparties, and transactions against OFAC, EU, UK, and UN sanctions lists
- Implement real-time screening for payments and onboarding
- Maintain audit trail of all screening decisions
- Update screening lists within 24 hours of publication
- Escalation procedures for potential matches
- Regular training for compliance and front-line staff
- Annual independent review of sanctions programme effectiveness

### BlackRock Top 10 Geopolitical Risks (Reference Categories)
These are tracked by institutional investors and signal market-moving risk:
1. US-China strategic competition
2. Global trade fragmentation
3. Technology decoupling
4. Major cyber attack
5. Gulf conflict/disruption
6. Russia-NATO confrontation
7. Taiwan Strait escalation
8. Climate policy divergence
9. Emerging market instability
10. AI governance divergence

---

## 10. Insurance & Risk Transfer Advanced

### Insurance Programme Review Checklist
- [ ] Policy schedule and renewal dates tracked
- [ ] Coverage limits adequate for current risk profile
- [ ] Deductibles/excesses affordable in worst-case scenario
- [ ] Exclusions reviewed (especially cyber, pandemic, war, regulatory)
- [ ] Sublimits checked for adequacy (especially business interruption, cyber)
- [ ] Claims notification procedures documented and known
- [ ] Broker relationship reviewed annually
- [ ] Premium benchmarked against market
- [ ] Claims history analysed for trends and improvement opportunities
- [ ] Coverage gaps identified and addressed or accepted with documentation
- [ ] Policy wording aligned with actual business operations (not outdated descriptions)
- [ ] Key person and D&O coverage adequate for current leadership team

### Parametric Insurance
Traditional indemnity insurance pays based on assessed loss (slow, subjective). Parametric insurance pays a predetermined amount when a defined trigger is met (fast, objective). Useful for:
- Natural catastrophe (hurricane category, earthquake magnitude, rainfall level)
- Supply chain disruption (port closure days, shipping route blockage)
- Power outage (duration exceeding threshold)
- Pandemic-related business interruption

### Captive Insurance
Self-insurance vehicle owned by the parent organisation. Consider when:
- Organisation has sufficient scale to absorb frequency risk
- Commercial market pricing is unfavourable
- Risks are unique or hard to place in commercial market
- Tax and capital efficiency benefits are material

---

## 11. Crisis Communication Playbook

### Pre-Drafted Message Templates

**Holding Statement (First Hour)**
```
[Organisation] is aware of [brief description of event]. We are actively investigating
and have activated our response plan. The safety of our [customers/employees/stakeholders]
is our top priority. We will provide further updates as information becomes available.
For urgent enquiries, contact [designated contact].
```

**Data Breach Notification**
```
We are writing to inform you of a security incident affecting [scope].
On [date], we identified [nature of incident]. We immediately [actions taken].
The following data may have been affected: [categories].
We have [remediation steps] and are [ongoing actions].
If you have concerns, please contact [support details].
```

**Service Outage**
```
We are experiencing a service disruption affecting [services/regions].
Our teams are working to restore normal operations. Current estimated restoration
time is [ETA]. We will update every [frequency]. We apologise for the inconvenience
and appreciate your patience.
```

### Spokesperson Hierarchy
1. **CEO / Managing Director** — Existential crises, fatalities, major regulatory action
2. **CTO / CIO** — Technology failures, data breaches, system outages
3. **CFO** — Financial crises, fraud, audit findings
4. **Head of Communications** — Media liaison, routine updates, social media response
5. **Legal Counsel** — Regulatory enquiries, litigation, legal notices

### Social Media Crisis Protocol
1. Monitor all channels continuously during active crisis
2. Respond to misinformation within 30 minutes
3. Direct detailed enquiries to official channels
4. Never argue with individuals publicly
5. Disable scheduled posts during active crisis
6. Screenshot and document all significant interactions for legal record

---

## 12. Testing & Exercises Advanced

### Tabletop Exercise Template
**Duration:** 90–120 minutes
**Participants:** BCP team, department heads, executive sponsor

**Structure:**
1. **Scenario Injection** (10 min) — Facilitator presents crisis scenario
2. **Initial Response** (20 min) — Team discusses immediate actions, escalation, communication
3. **Escalation Inject** (10 min) — Scenario worsens (new information, media attention)
4. **Recovery Planning** (20 min) — Team discusses recovery strategies and resource allocation
5. **Communication Exercise** (15 min) — Draft stakeholder messages, media response
6. **Resolution Inject** (10 min) — Scenario evolves toward resolution; new risks emerge
7. **Debrief** (25 min) — What worked, what didn't, action items

**Key Scenarios to Test:**
- Ransomware attack with data exfiltration
- Cloud provider outage lasting 48+ hours
- Key vendor bankruptcy
- Major data breach with regulatory notification
- Natural disaster affecting primary site
- Key person loss (sudden departure or incapacitation)
- Fraud discovery (internal or external)
- Geopolitical event affecting supply chain
- Social media crisis or reputational attack

### Exercise Evaluation Criteria
| Criterion | Questions |
|---|---|
| Activation Speed | How quickly was the incident detected and the response activated? |
| Decision Making | Were decisions timely, informed, and at the right level? |
| Communication | Were stakeholders notified promptly with accurate information? |
| Role Clarity | Did everyone know their responsibilities? |
| Resource Adequacy | Were required resources available and accessible? |
| Plan Adherence | Were documented procedures followed? Where did they break down? |
| Recovery Effectiveness | Were RTOs and RPOs achieved? |
| Lessons Captured | Were issues documented and corrective actions assigned? |

---

## 13. Key Risk Indicators & Dashboards

### Business Continuity KRIs
| KRI | Target | Frequency |
|---|---|---|
| % critical processes with tested recovery plans | 100% | Quarterly |
| Average incident response activation time | <30 minutes | Per incident |
| BCP exercises conducted vs. target | 100% adherence | Quarterly |
| % employees trained on continuity roles | >95% | Annually |
| Vendor continuity coverage (critical vendors with validated BCPs) | 100% | Semi-annually |
| Plan currency (% plans reviewed within 12 months) | 100% | Quarterly |

### Disaster Recovery KRIs
| KRI | Target | Frequency |
|---|---|---|
| RTO achieved in tests vs. target | 100% within target | Per test |
| RPO achieved in tests vs. target | 100% within target | Per test |
| Backup success rate | >99.9% | Daily |
| Mean time to restore from backup | Within RPO | Per test |
| Unplanned outages (count and duration) | Trending down | Monthly |
| DR test pass rate | 100% pass | Per test |

### Fraud KRIs
| KRI | Target | Frequency |
|---|---|---|
| Fraud loss rate (% of revenue) | <0.1% (varies by industry) | Monthly |
| Fraud incidents detected / prevented | Trending up (detection improving) | Monthly |
| Mean time to detect fraud | Trending down | Monthly |
| False positive rate | <5% (balance sensitivity) | Monthly |
| Staff fraud training completion | >95% | Annually |
| Suspicious activity reports filed | Per regulatory requirement | Monthly |

### Reputational & Geopolitical KRIs
| KRI | Target | Frequency |
|---|---|---|
| Brand sentiment score | Stable or improving | Weekly |
| Net Promoter Score | Above industry benchmark | Quarterly |
| Negative media mentions | Trending down | Weekly |
| Geopolitical exposure concentration | No >30% revenue in single high-risk jurisdiction | Quarterly |
| Sanctions screening resolution time | <24 hours | Per event |

### Executive Risk Dashboard Components
1. **Risk Heat Map** — Visual matrix of top risks by likelihood × impact
2. **KRI Traffic Lights** — Red/amber/green status for each metric
3. **Open Actions Tracker** — Overdue corrective actions from audits, exercises, incidents
4. **Incident Trend** — Rolling 12-month count and severity of incidents
5. **Insurance Coverage Summary** — Coverage vs. exposure by category
6. **Regulatory Compliance Status** — Current standing across applicable frameworks
7. **Geopolitical Watch List** — Active geopolitical risks with business exposure rating

---

## 14. Implementation Roadmap

### Phase 1: Foundation (Months 1–3)
- Establish risk governance structure, appoint risk owners
- Conduct enterprise risk assessment, build risk register
- Complete BIA for all critical functions
- Define risk appetite and tolerance statements
- Insurance gap analysis
- Basic fraud controls: segregation of duties, dual approvals, access reviews

### Phase 2: Core Plans (Months 4–6)
- Develop BCPs for all critical functions
- Create DR plans with defined RTO/RPO
- Build crisis communication plan with pre-drafted templates
- Deploy fraud monitoring tools
- Establish reputational risk monitoring (social listening, media tracking)
- First tabletop exercise

### Phase 3: Advanced Capabilities (Months 7–9)
- Scenario planning workshops for top strategic risks
- Geopolitical risk monitoring and exposure mapping
- AI-powered fraud detection and transaction monitoring
- Functional DR drill and vendor continuity assessment
- Align programmes with ISO 22301 and target standards
- Organisation-wide risk awareness training launch

### Phase 4: Maturity & Optimisation (Months 10–12)
- Full-scale BCP/DR simulation
- KRI dashboard and board-level risk reporting live
- Insurance programme optimised against updated risk profile
- Lessons-learned and continuous improvement formalised
- Industry benchmarking and target certification planning
- Year 2 priorities defined from gap analysis and maturity assessment

### Maturity Model
| Level | Name | Description |
|---|---|---|
| 1 | Initial | Ad hoc risk management; no formal processes |
| 2 | Developing | Basic policies and risk register exist; limited testing |
| 3 | Defined | Formal framework, documented plans, regular exercises |
| 4 | Managed | Quantitative metrics, integrated with strategy, proactive monitoring |
| 5 | Optimising | Continuous improvement, predictive capabilities, industry-leading resilience |

---

## 15. Multi-Jurisdictional Compliance Matrix

### UK
| Requirement | Authority | Key Obligations |
|---|---|---|
| FCA Operational Resilience | FCA/PRA | Important business services, impact tolerances, self-assessment, testing |
| UK GDPR | ICO | 72-hour breach notification, DPIA, privacy by design |
| Fraud Act 2006 | CPS | Criminal liability for fraud by false representation, failing to disclose, abuse of position |
| Proceeds of Crime Act | NCA | AML obligations, suspicious activity reports |
| Companies Act 2006 | Companies House | Directors' duties including duty of care and skill |

### EU
| Requirement | Authority | Key Obligations |
|---|---|---|
| DORA | EBA/ESMA/EIOPA | ICT risk management, incident reporting, resilience testing, third-party risk |
| GDPR | DPAs | 72-hour breach notification, DPIA, privacy by design, cross-border transfers |
| AML Package 2025 | AMLA | Single rulebook, centralised supervision, enhanced due diligence |
| NIS2 Directive | National CSIRTs | Cybersecurity risk management, incident reporting for essential/important entities |

### US
| Requirement | Authority | Key Obligations |
|---|---|---|
| Bank Secrecy Act | FinCEN | AML programme, SARs, CTRs, customer due diligence |
| SOX | SEC | Internal controls over financial reporting |
| HIPAA | HHS | Healthcare data security and breach notification |
| FFIEC Guidelines | Federal regulators | Business continuity requirements for financial institutions |

### Zambia
| Requirement | Authority | Key Obligations |
|---|---|---|
| Bank of Zambia Directives | BOZ | Payment system licensing, operational requirements |
| Financial Intelligence Centre Act | FIC | AML/CFT obligations, suspicious transaction reporting |
| Data Protection Act 2021 | DPA | Data processing principles, breach notification |

### Estonia
| Requirement | Authority | Key Obligations |
|---|---|---|
| EU DORA | Finantsinspektsioon | ICT risk management for financial entities |
| EU GDPR | AKI | Data protection compliance |
| Payment Institutions Act | Finantsinspektsioon | Licensing, capital, operational requirements |
| Cybersecurity Act | RIA | Critical infrastructure protection |

---

## 16. Templates & Checklists

### Monthly Risk Review Agenda
1. Review of risk register changes (new risks, closed risks, score changes)
2. Open action items status (from audits, exercises, incidents)
3. KRI dashboard review (traffic light status, trends)
4. Incident report summary (events since last review)
5. Emerging risks discussion
6. Regulatory update (new requirements, enforcement actions)
7. Next period priorities and resource needs

### Annual Risk Programme Calendar
| Month | Activity |
|---|---|
| January | Annual risk assessment kickoff, insurance renewal review |
| February | BIA refresh, risk register annual update |
| March | Q1 tabletop exercise |
| April | Insurance programme finalisation |
| May | Fraud controls testing, vendor continuity review |
| June | Q2 tabletop exercise, mid-year risk report to board |
| July | DR functional drill |
| August | Scenario planning workshop |
| September | Q3 tabletop exercise, training programme refresh |
| October | Geopolitical risk assessment update |
| November | Full-scale BCP/DR simulation |
| December | Q4 review, annual risk report, Year+1 planning |

### Incident Report Template
```
INCIDENT ID: [Auto-generated]
DATE/TIME DETECTED: [YYYY-MM-DD HH:MM]
DETECTED BY: [Person/System]
INCIDENT TYPE: [Cyber/Fraud/Operational/Reputational/Physical/Vendor]
SEVERITY: [Critical/High/Medium/Low]
DESCRIPTION: [What happened]
IMMEDIATE IMPACT: [Systems, customers, data, operations affected]
RESPONSE ACTIONS TAKEN: [Chronological log]
ROOT CAUSE: [If known]
REGULATORY REPORTING: [Required? Filed? Reference numbers]
INSURANCE NOTIFICATION: [Required? Filed? Policy reference]
REMEDIATION ACTIONS: [What will be done to prevent recurrence]
LESSONS LEARNED: [Key takeaways]
REVIEWED BY: [Name, Date]
STATUS: [Open/Resolved/Closed]
```

---

**Remember: Resilience over recovery. Function-based, not scenario-based. Test everything.
Risk is everyone's responsibility. Anticipate, prepare, prevent — then adapt constantly.
BUILD – DOCUMENT – RESEARCH – LEARN – REPEAT.**
