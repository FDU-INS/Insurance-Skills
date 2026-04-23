# TaxDE ELSTER Guide — Field-by-Field Walkthrough

> **Note**: ELSTER form layout changes slightly each year. Verify Zeile numbers against the current year's Ausfüllanleitung (PDF published by Bundeszentralamt für Steuern).

---

## Pre-Flight Checklist

Before opening ELSTER:
- [ ] Lohnsteuerbescheinigung from each employer
- [ ] Krankenversicherung Beitragsbescheinigung
- [ ] Riester/Rürup annual statement (if applicable)
- [ ] Kontonummer/IBAN for refund
- [ ] Steuernummer (or expect to apply for one)
- [ ] All receipts sorted and totalled by category
- [ ] Previous Steuerbescheid (for reference)

Recommended order: Mantelbogen → Anlage N → Anlage Vorsorge → Anlage Kind → Anlage KAP (if needed) → Anlage V (if rental) → Sonderausgaben → Haushaltsnahe Aufwendungen

---

## Mantelbogen ESt 1 A (Main Form)

### Personal Data (Lines 1–30)
| Field | Source | Common Error |
|-------|--------|--------------|
| Steuernummer | Previous Bescheid or Finanzamt letter | Using wrong year's number |
| IBAN | Your bank account | Entering joint account that doesn't match identity |
| Veranlagungszeitraum | The tax year you're filing for | Forgetting to update year |
| Religion / Kirchensteuer | Einwohnermeldeamt registration | Not updating after Kirchenaustritt |
| Identifikationsnummer | Your permanent 11-digit number (not Steuernummer) | Confusing with Steuernummer |

### Spouse / Civil Partner (Lines 13–23)
- Required for Zusammenveranlagung
- Both sign the return
- Each partner's Identifikationsnummer required

### Bank Connection
- Zeile "IBAN": Enter here for refund/payment
- If the Finanzamt owes you money, it arrives here typically 4–8 weeks after Bescheid

**Common Finanzamt check**: IBAN validation — ensure bank details are consistent with identity.

---

## Anlage N — Employment Income

### Source: Lohnsteuerbescheinigung (Zeilen on the Bescheinigung match Anlage N Zeilen)

| Anlage N Line | Lohnsteuerbescheinigung Source | What to enter |
|---------------|-------------------------------|---------------|
| Zeile 4 | Zeile 3: Bruttoarbeitslohn | Total gross employment income |
| Zeile 5 | Zeile 4: Lohnsteuer einbehalten | Lohnsteuer already paid |
| Zeile 6 | Zeile 5: Solidaritätszuschlag | Soli already paid |
| Zeile 7 | Zeile 6: Kirchensteuer | KiSt already paid (if applicable) |
| Zeile 22 | Zeile 12a: Arbeitnehmer-Anteil RV | Social contributions (auto-populated usually) |

**⚠️ Watch out**: If you had multiple employers in the year, you need a separate Anlage N for EACH employer.

### Werbungskosten Section

**Homeoffice Pauschale (Zeile 46)**
```
Value: number of homeoffice days × 6 (max 1,260)
Source: your calendar/work log
Note: cannot combine with full Arbeitszimmer deduction for same days
```

**Pendlerpauschale (Zeile 31–38)**
```
Zeile 31: one-way commute distance in km (not round trip)
Zeile 32: number of days commuted
Zeile 35: select transport type
The form calculates the deduction automatically
Note: enter the shorter route distance unless you can prove faster route
```

**Arbeitsmittel (Zeile 42)**
```
Value: sum of all work equipment purchased
Source: your receipt log
Note: items >€800 net must already be spread over useful life
      Only enter the deductible amount for this year
```

**Fortbildung (Zeile 43)**
```
Value: sum of all work-related education costs
Source: invoices
Include: course fees, travel, accommodation for multi-day training
```

**Gewerkschaft (Zeile 41)**
```
Value: annual union dues from your union statement
No documentation needed in the return itself; keep statement
```

**Internet / Telefon (Zeile 44)**
```
Value: estimated professional use portion (typically 20% of annual cost)
Conservative approach: €240 (€20/month) accepted without documentation
```

**Doppelte Haushaltsführung (Zeile 60–72)**
```
Complex multi-line section
Zeile 60: weekly rent at work location (max €1,000/month)
Zeile 67: home visits (round trip)
Zeile 71: meals deduction (only first 3 months)
```

**⚠️ Finanzamt check**: Pendlerpauschale is a common area of scrutiny. Distance claimed vs. actual address is automatically verified against maps.

---

## Anlage Vorsorgeaufwand (Insurance)

**Source: Beitragsbescheinigung from your Krankenversicherung (mandatory)**

| Field | Source | Note |
|-------|--------|------|
| Zeile 12: Beiträge GKV | Beitragsbescheinigung Zeile 21 | Employee share + Zusatzbeitrag |
| Zeile 13: Beiträge PKV | PKV annual statement | Basisabsicherung only |
| Zeile 14: Pflegeversicherung | Beitragsbescheinigung | Separate from KV |
| Zeile 40: Riester | Riester Bescheinigung | Total contributions inc. Zulage |

**⚠️ Watch out**: The GKV Beitragsbescheinigung must list the exact figure in Zeile 21 (arbeitnehmerseitiger Beitrag). This is NOT the same as what you see on your payslip — there can be small differences. Use the Bescheinigung figure.

---

## Anlage AV (Riester Detail)

Required in addition to Anlage Vorsorge for Riester.

| Field | Source |
|-------|--------|
| Zeile 4: Eigenbeiträge | Your contributions minus state Zulage |
| Zeile 5: Zertifizierungsnummer | From Riester contract |
| Zeile 7: Vertragsnummer | Your policy number |
| Zeile 8: Zulagen | Grundzulage + Kinderzulage total |

**Günstigerprüfung**: File Anlage AV every year even if you think the Zulage is better — Finanzamt does the comparison automatically. You cannot lose by filing it.

---

## Anlage Kind (Per Child)

**One Anlage Kind per child**

| Field | Source | Note |
|-------|--------|------|
| Zeile 4: Identifikationsnummer Kind | Child's tax ID | Request from Finanzamt if unknown |
| Zeile 5: Geburtsdatum | Birth certificate | |
| Zeile 18: Kinderfreibetrag Übertragung | Agreement with other parent | If one parent transfers their half |
| Zeile 31–50: Kinderbetreuungskosten | Kita invoices | 2024: 2/3, max €4,000; 2025+: 80%, max €4,800 |
| Zeile 53: Ausbildungsfreibetrag | If child in Ausbildung away from home | €1,200 |

**Kinderbetreuungskosten section (Zeilen 31–50)**:
```
Zeile 31: Total Kinderbetreuungskosten paid
The deductible amount is calculated automatically
2024 return: 2/3 of costs, maximum €4,000 per child
2025+ return: 80% of costs, maximum €4,800 per child
Condition: Child under 14, you must have a Betreuungsnachweis
```

**⚠️ Finanzamt check**: Kinderbetreuungskosten is frequently verified. Keep all invoices and Zahlungsnachweise (bank transfers). Cash payments are not accepted.

---

## Anlage Haushaltsnahe Aufwendungen

**Source: Handwerker invoices (labor portion only)**

| Field | Source | Note |
|-------|--------|------|
| Zeile 5: Haushaltsnahe Dienstleistungen | Cleaning, garden, etc. | 20% credit, max costs €20,000 |
| Zeile 6: Pflege- und Betreuungsleistungen | Elderly care at home | 20% credit |
| Zeile 9: Handwerkerleistungen | Labor on invoices | 20% credit, max labor costs €6,000 |

**Critical rule for Handwerker**:
- Invoice must separately state Lohnanteil (labor) and Materialanteil (materials)
- Only labor qualifies for the credit
- Must pay by bank transfer — keep Kontoauszug showing the payment
- Work must be in your primary or secondary residence

**⚠️ Finanzamt check**: HIGH scrutiny area. The §35a credit is claimed frequently and audited often. Finanzamt will want to see: invoice with labor split, and proof of bank payment.

---

## Anlage Sonderausgaben (Donations etc.)

| Field | Source | Note |
|-------|--------|------|
| Zeile 5: Kirchensteuer | Lohnsteuerbescheinigung Zeile 6 | Already on main Bescheinigung |
| Zeile 7: Spenden | Donation receipts / Quittungen | |
| Zeile 10: Mitgliedsbeiträge | To political parties, etc. | Different cap than Spenden |

---

## Anlage KAP (Capital Income)

**Complete only if you want Günstigerprüfung or have foreign capital income**

| Field | Source | Note |
|-------|--------|------|
| Zeile 4: Günstigerprüfung | Tick if you want individual rate applied | Beneficial if personal rate < 25% |
| Zeile 7: Kapitalerträge | Bank Jahressteuerbescheinigung | Total capital income |
| Zeile 12: KESt bereits einbehalten | Jahressteuerbescheinigung | Tax already withheld |
| Zeile 14: Verlustverrechnungstopf | From broker | Losses to carry forward/back |

**⚠️ Watch out**: Most people with only German capital income do NOT need to file Anlage KAP — Abgeltungsteuer is already withheld by the bank. Only file if: claiming Günstigerprüfung, have foreign capital income, or have unused Freistellungsauftrag to claim back.

---

## Anlage V (Rental Income)

**One Anlage V per rental property**

| Field | Source | Note |
|-------|--------|------|
| Zeile 7: Mieteinnahmen | Rental contracts + bank statements | Total rent received |
| Zeile 33: AfA (Absetzung für Abnutzung) | AfA schedule (see below) | Annual depreciation |
| Zeile 34: Schuldzinsen | Mortgage statement (Zinsbescheinigung) | Interest only, not principal |
| Zeile 35: Grundsteuer | Annual Grundsteuerbescheid | |
| Zeile 39: Verwaltungskosten | Property management fees | |
| Zeile 47: Reparaturen | Maintenance invoices | |
| Zeile 51: Nebenkostenabrechnung | Annual statement | If landlord pays utilities |

**AfA Calculation**:
```
Building value = Purchase price − Land value (Bodenrichtwert × Land area)
Annual AfA = Building value × 3% (post-2023 buildings) or 2% (older)
```

**⚠️ Common error**: Including land in the depreciable base. Land is NEVER depreciable. You must split purchase price between land and building.

---

## Anlage S (Freelance / Freiberufler)

**For self-employed income (Freiberufler use this; Gewerbetreibende use Anlage G)**

| Field | Source | Note |
|-------|--------|------|
| Zeile 4: Betriebseinnahmen | EÜR summary | Total revenue |
| Zeile 5: Betriebsausgaben | EÜR summary | Total deductible expenses |
| Zeile 6: Gewinn | Line 4 − Line 5 | |
| Anlage EÜR | Separate detailed form | Required if revenue >€600 |

**Reference**: See references/freelancer-guide.md for full EÜR detail

---

## Anlage AUS (Foreign Income)

**Required if any foreign income received**

| Field | Source | Note |
|-------|--------|------|
| Zeile 5–20: Land | Per-country section | One section per country |
| Zeile 6: Art des Einkommens | Type of income | Employment, rental, pension, etc. |
| Zeile 7: Betrag in EUR | Foreign income in EUR | Use Bundesbank annual average rate |
| Zeile 10: Im Ausland gezahlte Steuer | Tax certificate from foreign authority | |
| Zeile 13: Freistellungsmethode | Check if DBA uses exemption | |
| Zeile 14: Progressionsvorbehalt | If DBA-exempt, still affects rate | Usually pre-populated |

**Currency conversion**: Use the official Bundesbank annual average exchange rate for the tax year. Published at bundesbank.de each January.

---

## Post-Submission

### What to expect after submitting in ELSTER

1. **Immediately**: Electronic confirmation (Empfangsbestätigung) — save this PDF
2. **1–4 weeks**: ELSTER sends a Eingangsstempel (date stamp) — proof of filing
3. **4–12 weeks**: Steuerbescheid arrives by post (or ELSTER inbox if paperless)
4. **Review**: You have **1 month** from date of Steuerbescheid to file Einspruch

### Reading your Steuerbescheid

- Compare every line to what you filed
- Check: Festgesetzte Einkommensteuer vs. your calculated tax
- Check: Verarbeitete Werbungskosten — did the Finanzamt accept all deductions?
- Note: Auflagen or Vorläufigkeitsvermerke — areas flagged as provisional (common for pending court cases)

### Einspruch deadline
**1 calendar month from the date printed on the Steuerbescheid** — not from when you received it.
If the date falls on weekend/holiday, next working day counts.

Send Einspruch in writing (registered letter recommended) with: your Steuernummer, the year, what you're disputing, and why.
