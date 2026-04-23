---
name: close-management
description: "Manage month-end and year-end close (Monats-/Jahresabschluss) with checklists, task sequencing, and status tracking. Adapted for Swiss OR requirements including MWST and social insurance."
---

# Close Management (Abschlussverwaltung)

**Important:** This skill assists with close management workflows but does not provide financial advice. All close activities should be reviewed by qualified financial professionals. Based on Swiss Obligationenrecht (OR Art. 957–963b).

Month-end close checklist, task sequencing and dependencies, status tracking, and common close activities — including Swiss-specific tasks (MWST, Sozialversicherungen, Verrechnungssteuer).

## Month-End Close Checklist (Monatsabschluss-Checkliste)

### Pre-Close (Vorabschluss — Last 2–3 Business Days)

- [ ] Close calendar and deadline reminders sent to all contributors
- [ ] Cut-off procedures confirmed with Kreditoren, Debitoren, Payroll, Treasury
- [ ] All sub-systems processing normally (ERP, Lohnbuchhaltung, Banking)
- [ ] Preliminary bank reconciliation (Bankabstimmung) completed
- [ ] Open purchase orders reviewed for accrual needs
- [ ] Payroll processing schedule confirmed
- [ ] Known unusual transactions documented

### Close Day 1 (T+1)

- [ ] All subledger modules completed period-end processing
- [ ] Kreditorenabgrenzungen (AP accruals) posted
- [ ] Lohnbuchungen (Payroll entries) posted, including accrual for split pay periods
- [ ] Cash receipts and disbursements recorded through month-end
- [ ] Intercompany transactions posted and confirmed with counterparties
- [ ] Bankabstimmung completed with final Bankauszug
- [ ] Abschreibungen (Depreciation) run per Anlagenspiegel
- [ ] Auflösung aktive Rechnungsabgrenzungen (Prepaid amortization) posted

### Close Day 2 (T+2)

- [ ] Revenue recognition entries (Ertragsabgrenzungen) posted
- [ ] All remaining accrual journal entries posted
- [ ] Debitorenbuchhaltung reconciled to GL
- [ ] Kreditorenbuchhaltung reconciled to GL
- [ ] Inventory adjustments (Vorratsbewertung) recorded if applicable
- [ ] FX revaluation entries (Währungsumrechnung) posted
- [ ] Balance sheet reconciliations (Bilanzabstimmungen) started
- [ ] **MWST-Abstimmung:** Vorsteuer vs Umsatzsteuer reconciled for the period

### Close Day 3 (T+3)

- [ ] All Bilanzabstimmungen completed
- [ ] Adjusting journal entries (Korrekturbuchungen) from reconciliation posted
- [ ] Intercompany reconciliation and Eliminierungsbuchungen completed
- [ ] Preliminary Probebilanz (trial balance) and Erfolgsrechnung run
- [ ] Preliminary flux analysis (Abweichungsanalyse) on Erfolgsrechnung
- [ ] Material variances investigated and resolved
- [ ] **Sozialversicherungs-Abstimmung:** AHV/IV/EO/ALV contributions reconciled

### Close Day 4 (T+4)

- [ ] Steuerrückstellungen (Tax provisions) posted — direkte Bundessteuer, Kantonssteuern
- [ ] Eigenkapital-Übertrag (Equity roll-forward) completed
- [ ] All journal entries finalized — Soft Close
- [ ] Draft Jahresrechnung (Financial statements: Erfolgsrechnung, Bilanz, Geldflussrechnung)
- [ ] Detailed Abweichungsanalyse and variance explanations prepared
- [ ] Management review of financial statements and key metrics

### Close Day 5 (T+5)

- [ ] Final adjustments from management review posted
- [ ] Financial statements finalized — Hard Close
- [ ] Period locked in ERP/GL system
- [ ] Financial reporting package distributed to stakeholders
- [ ] Forecasts/projections updated based on actual results
- [ ] Close retrospective — process improvements identified

## Swiss-Specific Close Tasks (Schweiz-spezifische Aufgaben)

### MWST-Abrechnung (VAT Settlement — Quarterly)

- [ ] MWST-Journal für das Quartal abgestimmt
- [ ] Vorsteuer (Input VAT) and Umsatzsteuer (Output VAT) reconciled
- [ ] MWST-Abrechnung an ESTV (Federal Tax Administration) prepared
- [ ] MWST-Zahlung veranlasst (due: 60 days after quarter end)
- [ ] Rates verified: Normalsatz 8.1%, Reduzierter Satz 2.6%, Beherbergung 3.8%

### Sozialversicherungen (Social Insurance — Monthly/Quarterly)

- [ ] AHV/IV/EO contributions reconciled (employer + employee: 10.6% total)
- [ ] ALV contributions reconciled (employer + employee: 2.2% up to CHF 148'200)
- [ ] BVG/Pensionskasse contributions reconciled (per plan)
- [ ] UVG/UVGZ (accident insurance) reconciled
- [ ] FAK/FLG (family allowances) reconciled
- [ ] Quellensteuer (withholding tax for foreign employees) settled with cantonal authority

### Verrechnungssteuer (Withholding Tax — Event-driven)

- [ ] 35% Verrechnungssteuer on dividends declared — reported to ESTV
- [ ] Verrechnungssteuer on interest from bonds/deposits — reported
- [ ] Refund claims (Rückerstattungsanträge) filed if applicable

### Direkte Steuern (Direct Taxes — Annual)

- [ ] Steuerrückstellung for direkte Bundessteuer (federal income tax, 8.5%)
- [ ] Steuerrückstellung for Kantons- und Gemeindesteuern (varies by canton)
- [ ] Kapitalsteuer (capital tax, cantonal) accrued
- [ ] Tax provision reconciled to prior year assessment

## Task Sequencing and Dependencies (Ablauf und Abhängigkeiten)

### Dependency Map

```
LEVEL 1 (No dependencies — start immediately at T+1):
├── Cash entries (Zahlungseingänge/-ausgänge)
├── Bankauszug retrieval
├── Lohnbuchungen (Payroll)
├── Abschreibungen (Depreciation)
├── Auflösung Abgrenzungen (Prepaid amortization)
├── Kreditorenabgrenzungen (AP accruals)
└── Intercompany posting

LEVEL 2 (Depends on Level 1):
├── Bankabstimmung (needs: cash entries + Bankauszug)
├── Ertragsabgrenzungen (needs: billing data finalized)
├── Debitorenabstimmung (needs: all revenue/cash entries)
├── Kreditorenabstimmung (needs: all AP entries/accruals)
├── Währungsumrechnung (needs: all FX entries posted)
├── MWST-Abstimmung (needs: all Vorsteuer/Umsatzsteuer entries)
└── Remaining accruals

LEVEL 3 (Depends on Level 2):
├── All Bilanzabstimmungen (needs: all JEs posted)
├── IC-Abstimmung (needs: both sides posted)
├── Korrekturbuchungen from reconciliations
├── Sozialversicherungs-Abstimmung
└── Preliminary Probebilanz

LEVEL 4 (Depends on Level 3):
├── Steuerrückstellungen (needs: pre-tax income finalized)
├── Eigenkapital-Übertrag
├── Konsolidierung and Eliminierungen
├── Draft Jahresrechnung
└── Preliminary Abweichungsanalyse

LEVEL 5 (Depends on Level 4):
├── Management review
├── Final adjustments
├── Hard Close / Period lock
├── Reporting package
└── Forecast updates
```

### Critical Path

```
Cash/AP/AR entries → Nebenbuch-Abstimmungen → Bilanzabstimmungen →
  Steuerrückstellungen → Draft Jahresrechnung → Management review → Hard Close
```

## Status Tracking (Statusverfolgung)

### Close Status Dashboard

| Aufgabe | Verantwortlich | Frist | Status | Blocker | Bemerkungen |
|---------|---------------|-------|--------|---------|-------------|
| [Task]  | [Person/Role] | T+N   | Offen/In Bearbeitung/Erledigt/Blockiert | [If blocked] | [Notes] |

### Status Definitions

- **Offen (Not Started):** Task not yet begun
- **In Bearbeitung (In Progress):** Actively being worked on
- **Erledigt (Complete):** Finished and reviewed/approved
- **Blockiert (Blocked):** Cannot proceed due to dependency or issue
- **Gefährdet (At Risk):** May not meet deadline

### Close Metrics

| Kennzahl | Definition | Ziel |
|---------|-----------|------|
| Close-Dauer (days) | Business days from period end to hard close | Reduce over time |
| Nachträgliche Buchungen | Entries after soft close | Minimize |
| Verspätete Aufgaben | Tasks completed after deadline | Zero |
| Abstimmungsdifferenzen | Items requiring investigation | Reduce over time |
| Korrekturen | Errors found after close | Zero |

## Typical 5-Day Close Calendar

| Tag | Hauptaktivitäten | Verantwortlich |
|-----|-----------------|---------------|
| **T+1** | Cash, Payroll, AP-Abgrenzungen, Abschreibungen, Prepaid-Auflösung, IC-Buchungen | Buchhalter, Payroll |
| **T+2** | Ertragsabgrenzung, übrige Abgrenzungen, Debitoren-/Kreditorenabstimmung, FX, MWST-Abstimmung | Revenue Accountant, AP/AR, Treasury |
| **T+3** | Bilanzabstimmungen, IC-Abstimmung, Eliminierungen, Probebilanz, Voranalyse, Sozialversicherungen | Buchhaltungsteam, Konsolidierung |
| **T+4** | Steuerrückstellungen, Eigenkapital, Draft Jahresrechnung, Abweichungsanalyse, Management Review | Steuern, Controller, FP&A |
| **T+5** | Finalkorrekturen, Hard Close, Periodensperre, Reporting, Forecast-Update, Retrospektive | Controller, FP&A, Finanzleitung |

## Close Process Improvement (Verbesserung)

### Common Bottlenecks

| Engpass | Ursache | Lösung |
|---------|---------|--------|
| Late AP accruals | Waiting for department confirmation | Implement continuous accrual estimation; set cut-off deadlines |
| Manual journal entries | Recurring entries prepared manually | Automate standard recurring entries in ERP |
| Slow reconciliations | Starting from scratch each month | Implement continuous/rolling reconciliation |
| IC delays | Waiting for counterparty | Automate IC matching; set stricter deadlines |
| MWST reconciliation | Manual matching of Vorsteuer/Umsatzsteuer | Automate MWST-Abstimmung in ERP |
| Missing Belege | Scrambling for documentation at close | Maintain documentation throughout the month (OR Art. 957a) |

### Close Retrospective Questions

1. Was lief gut in diesem Abschluss?
2. Was dauerte länger als erwartet und warum?
3. Welche Blocker traten auf und wie können wir sie vermeiden?
4. Gab es Überraschungen in den Finanzergebnissen?
5. Was können wir für den nächsten Monat automatisieren oder vereinfachen?
