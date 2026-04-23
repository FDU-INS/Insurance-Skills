---
authority_level: secondary
effective_from: evergreen
last_verified: 2026-03-18
jurisdiction: federal
---

# M&A Financial Due Diligence — C-Corporation Transactions

**Purpose:** Due diligence framework for financial, tax, and operational analysis in C-corporation acquisitions and dispositions.

**Tier:** 3 (evergreen — M&A diligence process is stable across regulatory cycles)

**Skills that reference this:** `fp-strategic-advisory`, `fp-valuation-support`, `tx-entity-restructuring`, `tx-officer-compensation`

---

## Due Diligence Phases

### Phase 1: Preliminary

- Execute mutual NDA before any information exchange
- Review the teaser (anonymous one-pager) and Confidential Information Memorandum (CIM)
- Perform initial financial screening: revenue trend, EBITDA margin, customer concentration, capital intensity
- Issue a preliminary indication of interest (IOI) with valuation range and deal structure preference
- Engage outside counsel and tax counsel early — structure drives economics

### Phase 2: Detailed

- Access the virtual data room (VDR) — organize review by functional area (financial, tax, legal, operational, HR, IT, environmental)
- Attend management presentations — probe beyond the CIM narrative (ask about customer churn, pipeline quality, key person dependencies)
- Conduct site visits for businesses with physical assets, inventory, or manufacturing operations
- Prepare a detailed financial model incorporating diligence findings
- Draft quality of earnings (QoE) report — the centerpiece deliverable

### Phase 3: Confirmatory

- Verify key assumptions from Phase 2 with third-party confirmations (bank balances, AR confirmations, insurance coverage letters)
- Finalize purchase price and working capital peg
- Complete the bring-down diligence — confirm no material adverse changes between signing and closing
- Deliver final diligence report to buyer's board or investment committee

---

## Financial Due Diligence Checklist

### Core Financial Records (3-5 Years)

- Audited/reviewed/compiled financial statements and interim financials (YTD + prior year comparative)
- Federal and state tax returns (Form 1120 and all state filings), trial balances, general ledger detail for material accounts

### Working Capital and Balance Sheet

- AR aging (concentrations, past-due, write-off history), AP aging (stretched payables = cash flow stress signal)
- Inventory schedule (method, obsolescence reserve, physical count reconciliation), fixed asset schedule, debt schedule (including covenant compliance), prepaids and accrued liabilities

### Tax-Specific Items

- Tax provision workpapers (ASC 740), NOL carryforward schedule with expirations, R&D credit studies
- Open IRS/state examination history, transfer pricing documentation, state nexus analysis

### Legal and Operational

- Material contracts (top 10 customers/vendors, leases, employment agreements), litigation summary (5 years)
- Insurance policies (coverage, limits, claims history), employee census, benefit plans, IP schedule

---

## Quality of Earnings (QoE) Analysis

The QoE bridges reported earnings to sustainable, recurring EBITDA. Start with reported EBITDA, then adjust:

### Non-Recurring Items

- One-time gains or losses (asset sales, insurance recoveries, lawsuit settlements)
- Restructuring charges (severance, facility closure costs)
- Transaction costs (legal, advisory, VDR fees related to the current deal)
- Natural disaster or pandemic-related impacts (PPP forgiveness, ERTC, business interruption)

### Owner-Related Adjustments

- Above-market officer compensation — benchmark using the methodology in `fp/compensation-benchmarking.md` and replace with market-rate equivalent
- Personal expenses run through the business (vehicles, travel, meals, family-member payroll for minimal services)
- Related-party rent — compare to fair market value; adjust if the owner leases property to the company at an inflated or deflated rate
- Related-party revenue or expenses — eliminate or adjust to arm's-length pricing

### Accounting Policy and Pro Forma Adjustments

- Revenue recognition differences (percentage of completion vs. completed contract, bill-and-hold), inventory method conversions (LIFO to FIFO), depreciation assumptions vs. economic reality, accrual vs. cash basis conversion
- Full-year run rate of mid-year changes, annualized cost savings from completed actions, normalization for cyclicality or seasonality

---

## Working Capital Normalization

- **Define working capital** — typically: current assets (excluding cash and cash equivalents) minus current liabilities (excluding current portion of long-term debt and income tax payable)
- **Compute the peg** — trailing 12-month average of monthly normalized working capital. Some deals use a 24-month average to smooth seasonality
- **Purchase agreement mechanism** — set a target working capital peg at signing. At close, deliver estimated working capital. Post-close (60-90 days), perform a true-up to adjust purchase price for the difference between delivered and target working capital
- **Dispute resolution** — specify an independent accounting firm to resolve true-up disagreements, with costs shared equally

---

## Transaction Structure: Asset vs. Stock Purchase

### Asset Purchase

- Buyer selects specific assets to acquire and liabilities to assume
- Buyer receives a **stepped-up tax basis** in acquired assets — higher depreciation and amortization deductions going forward
- Seller recognizes gain or loss on each asset disposed (ordinary income on depreciation recapture, capital gain on goodwill post-TCJA)
- Contracts, licenses, and permits may require counterparty consent for assignment
- Buyer generally does NOT assume unknown or contingent liabilities (subject to successor liability doctrines)

### Stock Purchase

- Buyer acquires the entity with all assets and all liabilities (known and unknown)
- Existing tax basis in assets carries over — no step-up
- Contracts, licenses, and permits remain in place (no assignment needed)
- Simpler execution for entities with numerous contracts or hard-to-transfer licenses
- Buyer inherits tax attributes (NOLs, credit carryforwards) — subject to Section 382 limitations

### Section 338(h)(10) Election

- Treats a stock purchase as if it were an asset purchase **for tax purposes only**
- Both buyer and seller must jointly elect on Form 8023 (due by the 15th day of the 9th month after the acquisition date)
- Buyer gets stepped-up basis in assets (as in an asset purchase)
- Seller recognizes gain as if the corporation sold all assets on the acquisition date — the gain is reported on the corporation's final return
- Advantageous when the target has NOLs or losses that can offset the deemed asset sale gain
- Commonly used for S-corp acquisitions but also available for C-corp subsidiaries of a consolidated group

---

## Section 368 Tax-Free Reorganizations

- **Type A** — Statutory merger or consolidation under state law. Most flexible; can use mixed consideration (stock + cash) with boot recognized as gain
- **Type B** — Stock-for-stock exchange. Acquiring corporation must use solely voting stock. No cash or other property permitted
- **Type C** — Stock-for-assets. Acquiring corporation acquires substantially all assets of target using solely voting stock (limited boot exception)
- **Type D** — Acquisitive or divisive. Acquisitive: transfer of substantially all assets to a controlled corporation. Divisive: spin-offs, split-offs, split-ups under Section 355
- **Continuity requirements** — Continuity of interest (target shareholders must receive a meaningful equity stake in the acquirer) and continuity of business enterprise (acquirer must continue the target's historic business or use a significant portion of its assets)

---

## Earnout Structures

- Contingent purchase price tied to post-close performance metrics (revenue, EBITDA, customer retention)
- **Tax treatment for sellers** — installment sale reporting under Section 453 for deferred payments; imputed interest under Section 1274/7872 on below-market-rate deferred payments
- **Open vs. closed transaction doctrine** — if the maximum earnout is determinable, closed transaction treatment applies (gain calculated on total potential consideration). If not ascertainable, open transaction treatment may be available (gain recognized as payments are received)
- **Accounting treatment** — ASC 805 requires the buyer to record the earnout at fair value on the acquisition date as part of purchase price; subsequent changes to the earnout liability flow through earnings (not goodwill)

---

## Purchase Price Allocation (ASC 805)

- Allocate total consideration (cash + stock + earnout fair value + assumed liabilities) to identifiable assets and liabilities at fair value
- **Tangible assets** — inventory, equipment, real property, receivables (at collectible value)
- **Intangible assets** — customer relationships, trade names/trademarks, developed technology, non-compete agreements, favorable leases, backlog. Each requires a separate fair value determination
- **Goodwill** — excess of total consideration over net identifiable assets at fair value. Not amortizable for book (ASC 350 impairment testing); amortizable over 15 years for tax (Section 197)
- **Tax vs. book differences** — stepped-up tax basis creates a deferred tax asset/liability that affects the allocation
- Engage a qualified valuation firm (ASC 820 compliant) for material transactions — CPA firms typically do not perform the valuation but review and rely on the specialist's work

---

## Integration Planning

### Day-One Readiness

- New bank accounts (or account signer changes) in place before close
- Payroll transition — either add to buyer's payroll system or maintain target's system through a transition period
- Insurance — binder for new policies effective on close date (general liability, D&O, workers' comp, cyber)
- Regulatory filings — UCC amendments, state entity filings, business license transfers

### Accounting Integration

- Chart of accounts harmonization — map target's COA to buyer's COA, resolve naming and structure differences
- Cutoff procedures — define the exact moment of cut (typically 11:59 PM on close date) for revenue, expenses, cash receipts, and disbursements
- Opening balance sheet — record acquired assets and liabilities at fair value per the purchase price allocation
- Intercompany elimination entries — establish intercompany accounts and elimination procedures from day one

---

## Decision Points for the CPA

- **When to recommend a valuation firm** — any transaction exceeding $5M in enterprise value, any transaction involving significant intangible assets, any Section 338(h)(10) election (allocation is critical), any deal requiring ASC 805 purchase price allocation for GAAP reporting
- **When to recommend environmental diligence** — manufacturing, real estate, chemical/petroleum, or any business with potential CERCLA liability
- **When to recommend IP counsel** — technology companies, pharmaceutical/biotech, companies with material patent portfolios or trade secret dependencies
- **Red flags in diligence** — declining gross margins without clear explanation, customer concentration (>25% of revenue from one customer), heavy related-party transactions with unclear business purpose, off-balance-sheet obligations (operating leases pre-ASC 842, guarantees, pending litigation), deferred revenue inconsistencies, sudden acceleration of revenue recognition near the transaction date

---

## Accounting System Integration Notes

- For the acquiring entity: create a journal entry recording acquired assets (debits), assumed liabilities (credits), goodwill (debit for excess), and cash/consideration paid (credit)
- Map acquired entity's COA to the buyer's COA. Invoke `qbo-integration:qbo-coa` for platform-specific account mapping methodology
- Record purchase price allocation entries separately from operating entries — use a memo class or tag for "Acquisition" to enable easy filtering
- Goodwill: create an Other Asset account ("Goodwill — [Target Name]") — no book amortization but track tax amortization (15 years) separately
- Track earnout liability in Other Current Liabilities; adjust quarterly as performance data becomes available

---

## Authoritative References

- IRC Section 338 — Certain stock purchases treated as asset acquisitions
- IRC Section 368 — Definitions relating to corporate reorganizations
- IRC Section 382 — Limitation on NOL carryforward after ownership change
- IRC Section 197 — Amortization of goodwill and certain other intangibles
- IRC Section 453 — Installment method for deferred payments
- IRC Section 1060 — Special allocation rules for asset acquisitions
- ASC 805 — Business Combinations (FASB)
- ASC 350 — Intangibles — Goodwill and Other (FASB)
- ASC 820 — Fair Value Measurement (FASB)
- Treas. Reg. 1.338-1 through 1.338-10 — Section 338 election mechanics
- Form 8023 — Elections Under Section 338 for Corporations Making Qualified Stock Purchases
- Form 8594 — Asset Acquisition Statement Under Section 1060
- AICPA Due Diligence Working Group — Practice guide for financial due diligence engagements
