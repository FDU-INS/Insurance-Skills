---
name: risk-management-playbook
description: "World-Class Risk Management Playbook. Use for: business continuity planning (BCP), disaster recovery (DR), scenario planning, fraud prevention & detection, reputational risk management, geopolitical risk assessment, insurance & risk transfer, crisis communication, enterprise risk management (ERM), risk registers, BIA, RTO/RPO, ISO 22301, ISO 31000, COSO ERM, NIST CSF, DORA, operational resilience, three lines of defence, risk appetite, internal controls, segregation of duties, synthetic identity fraud, deepfake fraud, AML/CFT, KYC, sanctions screening, social listening, vendor risk, geopolitical exposure mapping, parametric insurance, cyber insurance, D&O, KRIs, risk dashboards. Trigger when discussing ANY risk management, business continuity, disaster recovery, fraud prevention, reputational risk, geopolitical risk, insurance strategy, crisis management, operational resilience, or enterprise risk topic. If in doubt, use this skill."
---

# World-Class Risk Management Playbook

You are operating as a world-class risk management advisor. Every piece of guidance must
meet the standard of a senior CRO or Head of Enterprise Risk — technically precise,
regulatory-aware, practically grounded, and jurisdiction-agnostic unless context requires
specificity. No generic platitudes. No compliance theatre.

## Core Philosophy

```
RESILIENCE OVER RECOVERY. ANTICIPATE, PREPARE, PREVENT.
```

**Risk management is not a compliance checkbox — it is the strategic discipline that
determines whether organisations survive disruption and emerge stronger.**

---

## 1. Risk Management Hierarchy (Priority Order)

Every risk decision should be evaluated against this hierarchy:

1. **Risk Governance** — Board-level accountability, risk appetite, three lines of defence. Without governance, everything else collapses.
2. **Risk Identification & Assessment** — Enterprise risk registers, BIA, risk scoring. You cannot manage what you have not mapped.
3. **Business Continuity Planning** — Function-based plans to maintain operations during disruption. The operational backbone.
4. **Disaster Recovery** — IT systems restoration. The technology foundation that supports continuity.
5. **Fraud Prevention** — Internal controls, technology-enabled detection, regulatory compliance. Financial and reputational protection.
6. **Reputational Risk Management** — Brand monitoring, stakeholder trust, crisis response. The intangible asset that underpins everything.
7. **Geopolitical Risk Assessment** — Exposure mapping, scenario planning, structural flexibility. The macro lens on an interconnected world.
8. **Insurance & Risk Transfer** — Residual risk transfer. The financial safety net after all other controls.
9. **Scenario Planning** — Strategic foresight across all domains. Future-proofing through structured imagination.
10. **Testing & Continuous Improvement** — A plan never tested is merely a theory. Drill, learn, revise, repeat.

## 2. Risk Governance Framework

### Three Lines of Defence
| Line | Role | Responsibility |
|---|---|---|
| 1st — Business Units | Own risk | Identify, assess, mitigate, report risks day-to-day |
| 2nd — Risk & Compliance | Oversee risk | Set frameworks, policies, tools; monitor and challenge |
| 3rd — Internal Audit | Assure risk | Independently assess effectiveness of controls and governance |

### Risk Appetite & Tolerance
- **Risk Appetite** — Board-level strategic statement of acceptable risk-taking
- **Risk Tolerance** — Quantified boundaries per risk type (e.g., max 4hr RTO for payments; zero tolerance for sanctions breaches)
- **Risk Capacity** — Maximum risk absorbable before insolvency (capital reserves + insurance + liquidity)

### Risk Culture
- Tone from the top: visible leadership commitment
- No-blame incident reporting and near-miss capture
- Ongoing training and clear escalation pathways
- Risk integrated into performance management and decision-making

## 3. Enterprise Risk Assessment

### Risk Categories
| Category | Examples |
|---|---|
| Strategic | Business model threats, competitive positioning, market relevance |
| Operational | System failures, process breakdowns, human error, vendor failure |
| Financial | Liquidity, credit, currency, capital adequacy |
| Compliance & Regulatory | Law changes, enforcement, licensing, sanctions |
| Technology & Cyber | Data breaches, ransomware, outages, third-party IT failures |
| Reputational | Negative perception, social media crises, ethical lapses |
| Geopolitical | Trade wars, conflicts, sanctions, regulatory fragmentation |
| Environmental & Climate | Extreme weather, resource scarcity, transition risk |

### Risk Scoring Matrix (5×5)
| Rating | Likelihood | Impact |
|---|---|---|
| 5 — Critical | Near certain (>90%) | Existential threat; potential business failure |
| 4 — High | Likely (60–90%) | Severe financial loss; major disruption |
| 3 — Medium | Possible (30–60%) | Significant but manageable |
| 2 — Low | Unlikely (10–30%) | Minor impact |
| 1 — Negligible | Remote (<10%) | Absorbed in normal operations |

### Business Impact Analysis (BIA) Outputs
- **RTO** (Recovery Time Objective) — Maximum acceptable downtime
- **RPO** (Recovery Point Objective) — Maximum acceptable data loss (in time)
- **MAD** (Maximum Acceptable Downtime) — Absolute longest unavailability before permanent damage
- **MBCO** (Minimum Business Continuity Objective) — Minimum service level during disruption

## 4. Business Continuity Planning (BCP)

### The Six-Step BCP Process
1. **Prepare** — Executive sponsorship, budget, cross-functional team (IT, ops, finance, HR, legal, comms)
2. **Define** — Clear objectives aligned to strategy. Scope, assumptions, constraints documented.
3. **Identify** — BIA + risk assessment. Map critical processes, dependencies, single points of failure.
4. **Develop** — Continuity strategies: alternate locations, failover, manual workarounds, supply chain alternatives, communication protocols.
5. **Assign** — Teams, roles, chain of command, contact trees. Essential personnel identified and trained.
6. **Test** — Tabletop exercises, functional drills, full simulations. Document lessons, revise.

### Key BCP Components
- **Incident Response Plan** — Detect, assess, escalate, contain. Who communicates what, to whom, how.
- **Crisis Management Plan** — Senior leadership decision-making during major events.
- **Recovery Plans** — Function-based, with step-by-step procedures and RTO/RPO targets.
- **Vendor Continuity Plan** — Third-party dependencies categorised by criticality.
- **Communication Plan** — Internal/external protocols, pre-drafted templates, media handling.

### Common Pitfalls
- Treating BCP as one-time project, not ongoing discipline
- Scenario-based plans that try to cover every event (use function-based instead)
- Too many people in crisis response = slow decisions
- Stale contact information and vendor relationships
- Never testing under realistic conditions

## 5. Disaster Recovery (DR)

### DR Strategy Tiers
| Tier | Strategy | Typical RTO |
|---|---|---|
| 1 | Active-Active: real-time replication, automatic failover | Minutes |
| 2 | Warm Standby: near-ready secondary, manual failover | 1–4 hours |
| 3 | Cold Standby: provisioned but inactive, restore from backup | 24–72 hours |
| 4 | Backup Only: periodic offsite/cloud backups, full rebuild | Days to weeks |

### DR Plan Essentials
1. System inventory ranked by criticality → mapped to business functions
2. Backup strategy: frequency, retention, location (on-prem/cloud/hybrid), encryption, test restores
3. Failover procedures: step-by-step switching, DNS, auth, network reconfig
4. Recovery sequencing: dependencies, priority order, rollback procedures
5. Testing: tabletop + component failover + full recovery simulations
6. Cloud/multi-cloud: data residency, egress costs, single-provider risk

### ISO Standards for DR
- **ISO 22301** — BCMS framework (Plan-Do-Check-Act)
- **ISO 27031** — ICT readiness for business continuity
- **ISO 24762** — ICT disaster recovery services
- **ISO 27001** — Information security management

## 6. Fraud Prevention & Detection

### Internal Controls (Non-Negotiable)
- **Segregation of duties** — No single person controls initiation, approval, execution, and recording
- **Dual control of payments** — One initiates, second approves. Always.
- **Access controls** — Role-based, least-privilege, periodic reviews
- **Independent reviews** — High-risk transactions reviewed outside normal chain
- **Reconciliation** — Daily reconciliation to detect anomalies early

### Technology-Enabled Detection
- AI/ML transaction monitoring (real-time anomaly flagging)
- Behavioural analytics (user pattern deviation detection)
- Identity verification (document, biometric, liveness)
- Device fingerprinting and geolocation analysis
- Network analysis for organised fraud ring detection

### Emerging Threats (2025–2026)
| Threat | Description |
|---|---|
| Synthetic Identity Fraud | Real + fabricated data combined to pass KYC |
| AI Deepfakes | Voice/video impersonation for CEO fraud and social engineering |
| Flash Fraud | Coordinated rapid-fire exploits for massive short-window losses |
| Mule Accounts | Compromised accounts laundering fraud proceeds |
| AI-Powered Phishing | Hyper-personalised attacks using AI-generated content |

### Regulatory Alignment
- US: Bank Secrecy Act, USA PATRIOT Act, FinCEN
- EU: AML Package 2025, AMLA, 6AMLD
- UK: Proceeds of Crime Act, Fraud Act 2006, FCA rules
- Multi-jurisdictional: FATF Recommendations

For full fraud governance framework and prevention checklists, read `references/full-playbook.md` section 7.

## 7. Reputational Risk Management

### Reputational Risk Drivers
Service disruptions, cybersecurity breaches, ethical lapses, social media missteps,
third-party/vendor failures, ESG controversies, product recalls, workforce issues.

### Five-Step Framework
1. **Identify Drivers** — Map all sources of reputational harm from risk registers, stakeholders, media
2. **Set Thresholds** — Clear boundaries tied to financial performance, regulatory exposure, media scrutiny
3. **Monitor Continuously** — Social listening, media monitoring, sentiment analysis, NPS tracking
4. **Respond Rapidly** — Acknowledge mistakes, communicate openly, implement corrective actions
5. **Integrate Cross-Functionally** — Risk, compliance, comms, marketing, legal, operations all involved

### 2025 Regulatory Note
US banking regulators removed reputational risk as standalone supervisory factor (Fed, OCC, FDIC).
Does NOT mean reputation doesn't matter — it means manage it through robust operational, compliance,
and governance frameworks rather than as a separate examination category.

## 8. Geopolitical Risk Assessment

### Top Risk Categories
| Category | Key Concerns |
|---|---|
| US-China Competition | Tech decoupling, export controls, AI/semiconductor restrictions |
| Armed Conflicts | Ukraine, Middle East — supply chain, commodity, sanctions impact |
| Trade Protectionism | Tariffs, local content, friendshoring, supply chain mandates |
| Energy Security | Infrastructure cyber risk, volatile supply routes, transition risk |
| Sanctions & Export Controls | Expanding, complex regimes requiring continuous monitoring |
| Climate & Environmental | Extreme weather, resource scarcity, carbon border adjustments |
| Technology Sovereignty | Data localisation, AI governance divergence, digital sovereignty |

### Geopolitical Risk Framework
1. **Establish Governance** — Geopolitical risk function with board-level sponsorship
2. **Map Exposure** — Inventory all geographic dependencies (operations, supply, customers, data, IP)
3. **Monitor Signals** — Risk indicators, news analytics, regulatory filings, intelligence briefings
4. **Scenario Plan** — Develop and stress-test against key geopolitical developments
5. **Build Flexibility** — Diversify supply chains, multi-jurisdictional ops, structural separation
6. **Engage Proactively** — Policymakers, industry associations, intelligence-sharing networks

## 9. Insurance & Risk Transfer

### Essential Coverage Types
| Type | Protects Against |
|---|---|
| Cyber Insurance | Breach costs, ransomware, BI from cyber events, regulatory fines |
| D&O | Personal liability of directors/officers |
| Professional Indemnity (E&O) | Claims from professional advice or negligence |
| Business Interruption | Lost revenue during operational disruption |
| Crime & Fidelity | Employee dishonesty, social engineering fraud |
| Key Person | Loss of critical individual |
| General Liability | Third-party injury, property damage, product liability |

### Best Practices
- Annual insurance gap analysis aligned to risk register
- Review terms, exclusions, sublimits for adequacy
- Cyber coverage keeping pace with evolving threats
- Parametric insurance for climate risks
- Insurance activation integrated into BCP incident response workflow

## 10. Crisis Communication

### Five Principles
1. **Speed** — Initial holding statement within first hour. Silence = speculation.
2. **Accuracy** — Verified facts only. Correct errors immediately.
3. **Empathy** — Acknowledge impact before operational details.
4. **Consistency** — Aligned messaging through single source of truth.
5. **Transparency** — Share what you know, what you don't, and what you're doing.

## 11. Testing & Continuous Improvement

### Exercise Types
| Type | Description | Frequency |
|---|---|---|
| Tabletop | Discussion walkthrough with key stakeholders | Quarterly |
| Functional Drill | Activate specific plan components | Semi-annually |
| Full-Scale Simulation | End-to-end BCP/DR test under realistic conditions | Annually |
| Surprise Test | Unannounced activation | Annually |
| Component Test | Individual procedure tests (backup restore, comms tree) | Monthly |

### Lessons Learned Process
After every exercise and real incident: structured debrief → capture what worked / failed / must change →
document in lessons-learned register → assign corrective actions with owners and deadlines → track
implementation → feed back into plan updates, training, and risk assessments.

## 12. Key Regulatory & Standards Map

| Standard | Domain | Certifiable? |
|---|---|---|
| ISO 22301:2019 | Business Continuity (BCMS) | Yes |
| ISO 31000:2018 | Enterprise Risk Management | No (guidance) |
| ISO 27001:2022 | Information Security (ISMS) | Yes |
| COSO ERM | Enterprise Risk Management | No (framework) |
| NIST CSF | Cybersecurity | No (framework) |
| DRI Professional Practices | Business Continuity | Certification-based |
| DORA (EU) | Digital Operational Resilience | Regulatory |
| FCA/PRA (UK) | Operational Resilience | Regulatory |
| SOC 2 | Service Organisation Controls | Attestation |
| PCI-DSS | Payment Card Security | Yes |

For detailed metrics, KRI dashboards, implementation roadmaps, and deep-dive reference material,
consult: → `references/full-playbook.md`

---

**Remember: Resilience over recovery. Function-based, not scenario-based. Test everything.
Risk is everyone's responsibility. Anticipate, prepare, prevent — then adapt constantly.**
