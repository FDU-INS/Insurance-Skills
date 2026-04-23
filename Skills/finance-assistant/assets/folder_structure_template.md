# TaxDE Folder Structure Template

Use this structure to organise your tax documents. Create it locally or in Google Drive.
**Smartphone photos of receipts are fine — JPG/PNG work alongside PDFs.**

---

## Suggested Structure

```
📁 Steuer [YEAR]/
├── 📁 00_NeedsReview/          ← Unclassified documents dropped here by document_sorter.py
│
├── 📁 01_Income/               ← Employment income documents
│   ├── Lohnsteuerbescheinigung_[Employer1].pdf
│   ├── Lohnsteuerbescheinigung_[Employer2].pdf   ← if multiple employers
│   └── Gehaltsabrechnungen/    ← Monthly payslips (optional; Lohnsteuerbesch. is enough)
│
├── 📁 02_Insurance/            ← All insurance certificates for deductions
│   ├── Krankenversicherung_Beitragsbescheinigung_[Provider].pdf  ← MANDATORY for GKV deduction
│   ├── Pflegeversicherung_Nachweis.pdf
│   ├── Riester_Bescheinigung_[Provider].pdf
│   ├── Ruerup_Bescheinigung_[Provider].pdf
│   └── Lebens_BU_[Provider].pdf                  ← if deductible portion applicable
│
├── 📁 03_Family/               ← Child-related documents
│   ├── 📁 Childcare/
│   │   ├── Kita_Jahresrechnung_[Child].pdf        ← annual invoice from Kita
│   │   ├── Kita_Zahlungsbelege.pdf                ← bank transfers showing payment
│   │   └── Tagesmutter_Rechnungen/
│   └── 📁 Kindergeld/
│       └── Kindergeldbescheid_[Year].pdf
│
├── 📁 04_Pension/              ← Pension contributions and statements
│   ├── 📁 Riester/
│   │   └── [Year]_Riester_[Provider]_Bescheinigung.pdf
│   ├── 📁 Ruerup/
│   │   └── [Year]_Ruerup_[Provider]_Bescheinigung.pdf
│   ├── 📁 bAV/
│   │   └── [Year]_bAV_[Provider]_Bescheinigung.pdf
│   └── 📁 DRV/
│       └── Renteninformation_[Year].pdf            ← annual DRV letter; useful for planning
│
├── 📁 05_Equipment/            ← Work equipment receipts (Arbeitsmittel)
│   ├── [Year]_Laptop_Dell_[Amount].pdf
│   ├── [Year]_Monitor_[Brand]_[Amount].jpg        ← photos of receipts fine
│   ├── [Year]_Fachliteratur_[Title]_[Amount].pdf
│   └── [Year]_Kurs_[Name]_[Amount].pdf            ← training/course invoices
│
├── 📁 06_Werbungskosten/       ← Other work expense documentation
│   ├── 📁 Fortbildung/
│   │   └── [Course invoices, conference receipts]
│   ├── 📁 Doppelte_Haushaltsfuehrung/
│   │   ├── Mietvertrag_Zweitwohnung.pdf
│   │   └── Heimfahrten_Belege/
│   └── 📁 Sonstiges/
│       └── [Other Werbungskosten receipts]
│
├── 📁 07_Property/             ← Property-related documents
│   ├── 📁 Eigenheim/
│   │   └── Grundsteuer_Bescheid.pdf
│   └── 📁 Vermietung/          ← If renting out property (Anlage V)
│       ├── Mietvertrag.pdf
│       ├── Nebenkostenabrechnung_[Year].pdf
│       ├── Zinsbescheinigung_[Bank].pdf           ← Mortgage interest statement
│       └── 📁 Handwerker/
│           ├── [Year]_Handwerker_[Contractor]_[Amount].pdf
│           └── [Proof of bank payment for each invoice]
│
├── 📁 08_Donations/            ← Charitable giving (Spendenquittungen)
│   ├── [Year]_Spende_UNICEF_[Amount].pdf
│   └── [Year]_Spende_[Org]_[Amount].pdf
│           Note: <€300 — Kontoauszug sufficient
│           ≥€300 — Zuwendungsbestätigung from org required
│
├── 📁 09_Investments/          ← Capital income (Anlage KAP if needed)
│   ├── Jahressteuerbescheinigung_[Bank1].pdf      ← one per bank/broker
│   ├── Jahressteuerbescheinigung_[Bank2].pdf
│   └── Freistellungsauftraege/
│       └── [Keep copies of filed Freistellungsaufträge]
│
└── 📁 10_TaxOffice/            ← Communication with Finanzamt
    ├── Steuerbescheid_[PreviousYear].pdf          ← keep previous year for reference
    ├── EStG_Vorauszahlung_Bescheid.pdf            ← if prepayments set
    └── 📁 Filed_Returns/
        └── [Copies of submitted ELSTER returns]
```

---

## Naming Convention

TaxDE's document_sorter.py uses this naming pattern:
```
{YEAR}_{Category}_{Detail}_{Amount}.{ext}
```

**Examples**:
- `2024_Lohnsteuerbescheinigung_Google_65000.pdf`
- `2024_KV_TK_1240.pdf`
- `2024_Kita_Monat06_250.pdf`
- `2024_Equipment_Laptop_950.jpg`
- `2024_Donation_UNHCR_200.pdf`
- `REVIEW_document_unknown.pdf` → goes to 00_NeedsReview/

---

## Format Notes

- **PDFs**: Preferred; all major scanners and phone apps produce them
- **JPG/PNG**: Fully accepted for receipts photographed with smartphone
- **Scan quality**: 300 DPI sufficient for OCR; ensure text is readable
- **Phone photos**: Make sure the receipt is flat, well-lit, full frame visible
- **Multiple pages**: Combine into single PDF for multi-page documents (Kita annual invoice, etc.)

**Recommended free scanner app**: Adobe Scan (iOS/Android) — produces searchable PDFs

---

## What Counts as "Filed" Documents

Keep the following indefinitely (or at least 10 years for business):
- All Steuerbescheide
- All filed returns
- Documents supporting claimed deductions

Keep for 4 years minimum (Festsetzungsverjährung):
- Receipts for claimed deductions
- Insurance certificates
- Lohnsteuerbescheinigungen

**Business documents**: 10-year retention obligation for Gewerbetreibende and self-employed.
