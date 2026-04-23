# TaxDE Law Change Monitoring

Instructions for checking, verifying, and communicating German tax law changes.

---

## 1. Primary Sources (in order of authority)

### Tier 1 — Binding legal sources
1. **bundesfinanzministerium.de**
   - BMF-Schreiben (binding on Finanzämter immediately upon publication)
   - Gesetzentwürfe and final Gesetze
   - Annual Änderungen overview (January publication)
   - URL: bundesfinanzministerium.de → Themen → Steuern

2. **bundesgesetze.de / gesetze-im-internet.de**
   - Official consolidated version of EStG, UStG, ErbStG, AO, etc.
   - Always check current version, not cached copies

3. **bundesrat.de**
   - Status of legislation requiring Bundesrat approval
   - Einspruchs- und Zustimmungsgesetze

4. **bfh.de**
   - Bundesfinanzhof rulings — binding on lower courts, and Finanzämter must follow
   - BFH decisions sometimes retroactively change years of practice

### Tier 2 — Reliable secondary sources
5. **steuerliches.de / haufe.de**
   - Professional tax commentary
   - Good for practical interpretation of BMF-Schreiben

6. **bundestag.de**
   - Legislation status tracker
   - Committee reports and plenary transcripts

### Tier 3 — For awareness, not citation
7. News media (Spiegel, Zeit, Handelsblatt)
   - Often report before final passage
   - Do NOT cite these as law — always verify at primary source

---

## 2. Search Strategies

### For specific rule changes
```
web_search: "[Deduction name] [year] Änderung aktuell"
Examples:
  "Homeoffice Pauschale 2025 Änderung aktuell"
  "Grundfreibetrag 2025 aktuell Erhöhung"
  "Riester Zulage 2025 aktuell"
  "Kinderfreibetrag 2025 Änderung"
```

### For annual omnibus changes
```
web_search: "Jahressteuergesetz [year] Änderungen Übersicht"
web_search: "Steuerrecht Änderungen [year] Zusammenfassung"
web_search: "Steuerliche Neuregelungen [year] BMF"
```

### For specific BMF guidance
```
web_search: "§[X] EStG BMF-Schreiben [year]"
web_search: "BMF-Schreiben [topic] [year]"
```

### For court rulings
```
web_search: "BFH Urteil [topic] [year] aktuell"
web_search: "BFH [AZ: e.g., VI R 12/22] Urteil"
```

---

## 3. Credibility Assessment Framework

| Source | Status | Action |
|--------|--------|--------|
| BMF-Schreiben published | Binding | Cite with publication date |
| BFH Urteil | Binding on courts | Cite; note if BMF has accepted or non-acceptance letter exists |
| Gesetz passed Bundestag + Bundesrat | Law | Cite with BGBl reference |
| Gesetz passed Bundestag, Bundesrat pending | Not yet law | Flag as "pending final passage" |
| Koalitionsvertrag item | Planned | "Planned, not yet legislated" |
| Draft Referentenentwurf | Early draft | "In drafting phase, not yet law" |
| Media report | Unverified | Verify at primary source before citing |

**Rule**: Never give an answer based on media reports alone. Always trace to primary source.

---

## 4. Communication Format (Mandatory for Every Law Change)

Use this format every time a law change is surfaced, whether proactively or in response to a question:

```
📋 [Rule name] — updated for [year]

Was:  [previous value] ([previous year])
Now:  [new value] ([current year])

Why:  [Plain language explanation — one of:
      - Annual inflation adjustment (e.g., Grundfreibetrag)
      - New legislation: [law name] vom [date]
      - Court ruling: BFH [AZ] vom [date]
      - Coalition agreement implementation
      - EU law requirement]

Impact on you:  [specific € effect on user's situation]
Action needed: [Yes/No — if yes: what to do and by when]
```

**Example**:
```
📋 Grundfreibetrag — updated for 2025

Was:  €11,604 (2024)
Now:  €12,096 (2025)

Why:  Annual inflation-based adjustment under §32a EStG; part of the
      Jahressteuergesetz 2024 (BGBl. 2024 I Nr. [X]).

Impact on you:  The first €492 of your income that was previously taxed
                is now tax-free. At your marginal rate of 32%, this saves
                approximately €157/year.

Action needed: No — applied automatically by Finanzamt. No filing change.
```

---

## 5. Proactive Alert Criteria

Alert the user without being asked if:

### Mandatory alerts (always)
- Any change affecting a deduction they currently claim (per profile)
- New deadline created that they could miss
- Retroactive change creating a refund opportunity for prior years
- Significant court ruling that opens new deduction territory

### Conditional alerts (when relevant)
- Change affects their Steuerklasse or family situation
- Change creates a NEW deduction they qualify for
- Rate change for their income bracket (Grundfreibetrag, Spitzensteuersatz threshold)
- BBG change affecting their social contributions

### Alert format for user notification
```
⚠️ Tax law update that affects you directly

[Use the communication format above]

This affects your [current year] return. [Specific instruction on what to do.]
```

---

## 6. Key Annual Change Calendar

These items change almost every year — monitor each January:

| Item | When published | Source |
|------|---------------|--------|
| Grundfreibetrag | Jahressteuergesetz (usually Dec/Jan) | BGBl |
| BBG RV/GKV | §4 SGB IV — published November | bundesgesundheitsministerium.de |
| Vorabpauschale Basiszins | BMF-Schreiben, January | BMF website |
| Beitragssatz GKV Zusatzbeitrag (avg) | GKV-Spitzenverband, November | gkv-spitzenverband.de |
| Rürup maximum | Depends on BBG RV West | Calculated |
| Verpflegungsmehraufwand | BMF-Schreiben | BMF website |
| Pendlerpauschale | Only if legislated change | BGBl |
| Dienstwagenbesteuerung thresholds | Occasionally | BMF-Schreiben |

---

## 7. Recent Major Changes to Track

### 2023 changes (for reference)
- Homeoffice Pauschale increased to €6/day (from €5) and days to 210 (from 120)
- Rürup deductibility reached 100% (was 96% in 2022)
- Arbeitnehmer-Pauschbetrag increased to €1,230 (from €1,000)
- Sparer-Pauschbetrag doubled to €1,000/€2,000 (from €801/€1,602)

### 2024 changes
- Grundfreibetrag: €11,784 (from €10,908)
- Progressionsstufen adjusted upward
- Kindergeld: €250/month per child
- Kinderfreibetrag: €9,540 per child
- Arbeitnehmer-Pauschbetrag remains €1,230

### 2025 legislated changes
- Grundfreibetrag: €12,096
- Kleinunternehmergrenze: €25,000 / €100,000
- BBG RV: €96,600
- Kindergeld: €255/month per child
- Kinderbetreuungskosten: 80% / max €4,800 per child

### 2026 legislated changes
- Grundfreibetrag: €12,348
- Kindergeld: €259/month per child
- Kinderfreibetrag: €9,756 per child
- Soli-Freigrenze: ~€20,350 single / ~€40,700 together

---

## 8. Einspruch Opportunities from BFH Rulings

When a BFH ruling creates a retroactive opportunity:

1. Check whether the Finanzamt accepted or rejected the ruling (check BMF non-acceptance letters)
2. If accepted: amend returns for open years (within 4-year assessment window)
3. If rejected: the BMF will issue a BMF-Schreiben — file Einspruch and request "Ruhen des Verfahrens" (suspension pending outcome)
4. If litigation ongoing: claim the deduction with a note referring to pending case; request vorläufige Steuerfestsetzung

### Open years for amendment
- Tax years still within Festsetzungsverjährung (4 years from end of assessment year)
- Example in 2025: can still amend 2021, 2022, 2023, 2024
- For evasion: 10 years; for willful evasion: 10 years

### Filing Einspruch template (basic)
```
An das Finanzamt [Name]
Steuernummer: [XXXXXXXX]
Betreff: Einspruch gegen Einkommensteuerbescheid [year] vom [date]

Ich lege hiermit Einspruch ein gegen den Einkommensteuerbescheid für das Jahr [year].

Begründung:
[Specific reason — cite BFH ruling with Az. or legal basis]

Antrag:
Den Bescheid unter Berücksichtigung von [X] zu ändern und die Steuer
auf €[X] herabzusetzen.

Bitte bestätigen Sie den Eingang dieses Einspruchs.

Mit freundlichen Grüßen,
[Name]
[Date]
[Signature]
```
