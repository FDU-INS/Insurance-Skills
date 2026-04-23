# Domain Review Matrix

Use this matrix when the session's domain pack drives real risk more than generic software checks.
For each domain, verify the listed items. Use `ck_validate` for automated pattern checks, then
manually verify items that require business-logic or process judgment.

## HR

- **Protected classes in scoring**: Scan job descriptions, screening logic, and ranking algorithms for protected attributes (race, gender, age, religion, disability, national origin). Use `ck_validate` on scoring code. Verify no training data features encode proxies for protected attributes.
- **Candidate data segregation**: Confirm candidate PII (name, email, address, phone) is stored separately from evaluation data. Verify interviewer notes reference candidate IDs, not names, in analytics. Check that rejected candidate data retention respects local regulations (typically 1-2 years, then purge).
- **Compensation visibility**: Verify salary bands are visible only to HR ops and authorized managers. Confirm individual compensation data requires explicit role-scoped access. Check that compensation reports aggregate to levels where individual identification is not possible.
- **Employment verification**: Confirm I-9 document data is stored separately from performance records. Verify work-authorization status is checked at hire and on expiration, but not used in performance or promotion logic.

## Legal

- **Privileged materials isolation**: Verify privileged documents are tagged at creation time. Confirm privilege tags propagate through search, export, and AI-summarization pipelines. Check that privilege review logs record who accessed what and when.
- **Retention and eDiscovery**: Confirm retention schedules are configured per document type and jurisdiction. Verify automated retention enforcement skips documents on legal hold. Check that expired document purge produces a destruction certificate.
- **Conflict checking**: Verify new matter intake runs conflict-of-interest checks against existing clients. Confirm conflict check results are logged and require affirmative clearance before work begins.

## Marketing

- **Opt-in and unsubscribe controls**: Verify email and messaging consent is captured with timestamp, source, and scope. Confirm consent records are immutable once created. Check that opt-out requests propagate to all downstream systems within 72 hours.
- **Analytics PII**: Verify analytics pipelines do not store raw email addresses, phone numbers, or device IDs in user-facing dashboards. Confirm PII used for attribution is hashed or tokenized before storage. Check that audience segment exports exclude individual-level PII unless the consumer has explicit consent scope.
- **Advertising targeting**: Verify ad targeting does not use sensitive categories (health condition, financial status, sexual orientation, religion). Confirm lookalike audiences exclude protected-attribute proxies.

## Sales

- **CRM contact handling**: Verify CRM export endpoints mask or strip PII for non-authorized scopes. Confirm contact deletion requests propagate to all integrated systems within 30 days. Check that lead enrichment data sources comply with data-minimization principles.
- **Revenue and quota auditability**: Verify pipeline and forecast data is accessible only to roles with explicit need. Confirm individual deal values are not exposed in team-level dashboards without aggregation. Check that commission calculations are auditable and traceable to signed terms.
- **Contract handling**: Verify contract documents are encrypted at rest with access restricted to deal team and legal. Confirm contract metadata is stored separately from contract text in analytics. Check that expired contracts are archived per retention policy.

## Real Estate

- **Fair-housing violations blocked**: Verify property listing algorithms do not filter or sort by neighborhood demographic composition. Confirm advertising copy does not contain discriminatory language. Check that recommendation engines do not use protected-class data.
- **Tenant data protection**: Verify tenant application data (SSN, income, criminal history) is encrypted at rest and purged after the decision period. Confirm screening results are shared only with authorized leasing agents. Check that tenant payment history is accessible only to property management roles.
- **Retention controls**: Verify lease documents are retained per state-specific requirements (typically 7 years after lease termination). Confirm tenant dispute records are retained for the statute of limitations period.

## Government / Public Sector

- **Records retention and holds**: Verify all official records follow the jurisdiction's retention schedule. Confirm record deletion requires documented authorization. Check that records requests (FOIA, public records) are processable within statutory deadlines.
- **Benefits and licensing fairness**: Verify benefits eligibility logic does not use citizenship-adjacent shortcuts as proxies for protected attributes. Confirm licensing decisions follow published criteria and are auditable. Check that automated scoring in case management is explainable and reviewable.
- **Approval chains**: Verify procurement and policy decisions follow required approval chains. Confirm approval delegation is documented and auditable.

## Insurance / Claims

- **Claims fairness**: Verify claim adjudication logic does not use protected attributes as rating or denial factors. Confirm model-based pricing or underwriting decisions are explainable. Check that denial letters include specific reason codes and appeal instructions.
- **Medical-adjacent privacy**: Verify health-related claims data is treated with HIPAA-equivalent protections even when not technically PHI. Confirm medical records access is limited to claims adjusters with active case assignment.
- **Denial review**: Verify denied claims undergo secondary review before finalization. Confirm appeal timelines are tracked and enforced. Check that appeal outcomes are logged with reason and reviewer identity.

## E-commerce / Retail

- **Card and checkout data**: Verify cardholder data environment is segmented from general application infrastructure. Confirm no raw PANs are stored in logs, databases, or error tracking. Check that PCI-DSS self-assessment is completed annually.
- **Refund and chargeback controls**: Verify refund authorization requires role-appropriate approval for amounts exceeding defined thresholds. Confirm refund processing produces immutable audit entries. Check that refund fraud detection is active and calibrated.
- **Fraud scoring**: Verify order fraud scoring runs before payment capture. Confirm fraud review queues are staffed to meet response-time SLAs. Check that false-positive rates are monitored.

## Logistics / Supply Chain

- **Chain-of-custody integrity**: Verify chain-of-custody records are immutable once created. Confirm custody transfers produce signed, timestamped audit entries. Check that custody gaps trigger alerts for investigation.
- **Dispatch and hazmat safety**: Verify dispatch routing does not assign drivers to routes exceeding hours-of-service limits. Confirm hazardous-material routing follows DOT restrictions. Check that safety interlock bypasses require explicit review and are logged.
- **Carrier data**: Verify carrier insurance and safety ratings are current before load assignment. Confirm carrier PII is not exposed in shipper-facing dashboards.

## Manufacturing / Quality

- **QA holds and recall traces**: Verify quality-hold decisions are immutable and require documented justification. Confirm held inventory is physically and logically segregated from shippable stock. Check that hold releases require authorized sign-off with documented corrective action. Verify lot and serial traceability from raw material through finished goods shipment.
- **Safety interlocks**: Verify safety-critical system changes go through management-of-change review. Confirm incident reports are retained per OSHA requirements (5 years for records, 30 years for exposure records). Check that safety interlock bypasses cannot occur silently in automation.

## Nonprofit / Grants

- **Donor payment isolation**: Verify donor records are not sold or shared outside the organization's stated privacy policy. Confirm anonymous donation options preserve donor identity from all internal reporting except compliance-required access. Check that donor communication preferences are respected across all channels.
- **Grant restrictions**: Verify restricted funds are tracked separately from general operating funds. Confirm grant spending reports match restricted-purpose documentation. Check that restricted fund balances are visible to finance and grant management roles only.
- **Beneficiary data**: Verify beneficiary data exports strip or mask PII unless the consumer has explicit authorization. Confirm bulk beneficiary data transfers use encrypted channels. Check that beneficiary consent for data sharing is documented and current.
