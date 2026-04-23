# TrialSim

> Generate realistic clinical trial data including study definitions, subjects, visits, adverse events, efficacy assessments, and CDISC-compliant output.

## What TrialSim Does

TrialSim is the **clinical trial data** engine of HealthSim. It creates synthetic trial data that follows regulatory standards—proper SDTM domains, MedDRA-coded adverse events, LOINC-coded labs, and realistic enrollment patterns across multi-site, multi-country trials.

Whether you need a small Phase 1 dose-escalation study or a large Phase 3 pivotal trial with SDTM/ADaM output, TrialSim generates data suitable for testing EDC systems, statistical programming, and regulatory submission workflows.

## Quick Start

**Simple:**
```
Generate a Phase 3 oncology trial with 200 subjects
Generate adverse events for an immunotherapy trial
```

**SDTM domains:**
```
Generate DM domain for 50 subjects as SDTM
Generate AE domain with MedDRA coding
```

**With output format:**
```
Generate a Phase II trial as SDTM datasets
Generate analysis-ready data as ADaM
```

See [hello-healthsim examples](../../hello-healthsim/examples/trialsim-examples.md) for detailed examples with expected outputs.

## Key Capabilities

| Capability | Description | Skill Reference |
|------------|-------------|-----------------|
| **Study Definition** | Protocol, arms, visit schedules | [SKILL.md](SKILL.md#core-entities) |
| **Phase 1** | Dose escalation, MTD, 3+3, BOIN, CRM | [phase1-dose-escalation.md](phase1-dose-escalation.md) |
| **Phase 2** | Proof of concept, Simon's two-stage | [phase2-proof-of-concept.md](phase2-proof-of-concept.md) |
| **Phase 3** | Pivotal registration trials | [phase3-pivotal.md](phase3-pivotal.md) |
| **SDTM Domains** | DM, AE, VS, LB, CM, EX, DS, MH | [domains/](domains/) |
| **Therapeutic Areas** | Oncology, CV, CNS, CGT | [therapeutic-areas/](therapeutic-areas/) |
| **Real World Evidence** | Synthetic controls, external comparators | [rwe/](rwe/) |

## Trial Phase Cohorts

| Phase | Key Elements | Skill |
|-------|--------------|-------|
| Phase 1 | First-in-human, dose escalation, MTD, DLTs | [phase1-dose-escalation.md](phase1-dose-escalation.md) |
| Phase 2 | Proof of concept, dose-ranging, futility | [phase2-proof-of-concept.md](phase2-proof-of-concept.md) |
| Phase 3 | Pivotal, registration, NDA/BLA enabling | [phase3-pivotal.md](phase3-pivotal.md) |

## SDTM Domains

| Domain | Purpose | Skill |
|--------|---------|-------|
| DM | Subject demographics, treatment arms | [domains/demographics-dm.md](domains/demographics-dm.md) |
| AE | Adverse events with MedDRA | [domains/adverse-events-ae.md](domains/adverse-events-ae.md) |
| VS | Vital sign measurements | [domains/vital-signs-vs.md](domains/vital-signs-vs.md) |
| LB | Laboratory results with LOINC | [domains/laboratory-lb.md](domains/laboratory-lb.md) |
| CM | Concomitant medications with ATC | [domains/concomitant-meds-cm.md](domains/concomitant-meds-cm.md) |
| EX | Study drug exposure | [domains/exposure-ex.md](domains/exposure-ex.md) |
| DS | Subject disposition | [domains/disposition-ds.md](domains/disposition-ds.md) |
| MH | Medical history | [domains/medical-history-mh.md](domains/medical-history-mh.md) |

## Output Formats

| Format | Request | Use Case |
|--------|---------|----------|
| JSON | (default) | API testing, EDC integration |
| CDISC SDTM | "as SDTM" | Regulatory submission |
| CDISC ADaM | "as ADaM" | Statistical analysis |
| Star Schema | "as star schema" | BI dashboards, DuckDB |
| CSV | "as CSV" | Spreadsheet analysis |

## Integration with Other Products

| Product | Integration | Example |
|---------|-------------|---------|
| **PatientSim** | Patient → Subject | Cancer patient enrolls in trial |
| **PopulationSim** | Geography → Feasibility | County data → Site selection, diversity |
| **NetworkSim** | Provider → Investigator | Site PI with credentials |
| **MemberSim** | Standard of care claims | SOC claims during trial |

## Data-Driven Planning (PopulationSim v2.0)

When planning trials, TrialSim uses **real population data** for evidence-based feasibility:

```
Identify top 5 US counties for a Phase III NASH trial based on patient availability
```

This provides:
- Disease prevalence from CDC PLACES for feasibility estimates
- Demographic distributions for diversity planning (FDA guidance compliance)
- SVI data for site access and enrollment projections
- Data provenance for audit trails

See [SKILL.md](SKILL.md#cross-product-populationsim-integration) for full integration details.

## Skills Reference

For complete generation parameters, examples, and validation rules, see:

- **[SKILL.md](SKILL.md)** - Full skill reference with all cohorts
- **[../../SKILL.md](../../SKILL.md)** - Master skill file (cross-product routing)
- **[domains/README.md](domains/README.md)** - SDTM domain overview

## Related Documentation

- [hello-healthsim TrialSim Examples](../../hello-healthsim/examples/trialsim-examples.md)
- [CDISC SDTM Format](../../formats/cdisc-sdtm.md)
- [CDISC ADaM Format](../../formats/cdisc-adam.md)
- [Clinical Trials Domain Knowledge](clinical-trials-domain.md)

---

*TrialSim generates synthetic trial data only. Never use for actual regulatory submissions.*
