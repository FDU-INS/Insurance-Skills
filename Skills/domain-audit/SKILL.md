---
name: domain-audit
description: "Audit a session against its domain pack, especially the regulated and operations-heavy packs such as HR, legal, marketing, sales, real-estate, government, insurance, logistics, manufacturing, e-commerce, and nonprofit. Use this when domain-specific policy needs a manual pass."
when_to_use: "Activate before handling data in regulated or sensitive domains, or when the user asks about HR policy, legal compliance, GDPR, healthcare, finance, or any industry-specific governance requirements."
argument-hint: "[domain or data type to audit]"
license: Apache-2.0
compatibility:
  - codex
  - claude-standalone
  - claude-plugin
  - copilot-plugin
  - github-repo
  - open-standard
metadata:
  author: controlkeel
  version: "2.0"
  category: domain
  ck_mcp_tools:
    - ck_context
    - ck_finding
---

# Domain Audit Skill

Use this skill when the session’s domain pack drives the real risk more than generic software checks.

## Focus areas

- HR: bias, candidate data, compensation visibility
- Legal: privilege, retention, document handling
- Marketing: consent, unsubscribe, analytics PII
- Sales: CRM data, contact deletion, revenue visibility
- Real estate: fair-housing logic, tenant PII, retention
- Government: records retention, constituent data, approval chains
- Insurance: claims fairness, medical-adjacent privacy, denial review
- E-commerce: card scope, refunds, fraud controls
- Logistics: shipment custody, dispatch safety, carrier data
- Manufacturing: QA holds, traceability, plant safety
- Nonprofit: donor privacy, grant restrictions, beneficiary exports

## Additional resources

- [Domain review matrix](references/domain-review-matrix.md)
