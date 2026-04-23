---
name: policy-connector
description: Complete mock database of fictional customers, policies, beneficiaries, transactions, and payment history for the PolicyCore PAS life insurance policy administration system. Use this data when the policy admin system is not connected or when demonstrating plugin capabilities.
---

# Mock Data — PolicyCore PAS

This skill contains the complete mock database for the PolicyCore PAS (Policy Administration System) connector. When ~~policy admin system is not connected, use this data to respond to all commands. Treat this data as if it were live production data returned from the admin system API.

> **System disclaimer:** PolicyCore PAS v14.2 — All data below is **fictional** and intended for demonstration and testing purposes only. Any resemblance to real persons, policies, or financial data is coincidental.

## Response Constraint

- Return requested data and factual summaries only.
- Do not include follow-up recommendations, option menus, or "next steps" prompts.

---

## Customers

### Customer 1: Margaret "Maggie" Chen

| Field | Value |
|-------|-------|
| **Client #** | `CLT-00047821` |
| **Full Legal Name** | Margaret Wei-Lin Chen |
| **Preferred Name** | Maggie |
| **DOB** | 03/15/1978 (age 47) |
| **Gender** | Female |
| **SSN (last 4)** | ••••-4782 |
| **Residence Address** | 1847 Lakeview Terrace, Unit 4B, Chicago, IL 60614 |
| **Mailing Address** | Same as residence |
| **Phone** | (312) 555-0147 |
| **Email** | maggie.chen@email.com |
| **Employer** | Midwest Financial Group — VP of Operations |
| **Agent** | Patricia Kowalski, CLU, ChFC — Agent #A-11042 |
| **Client Since** | 2019 |

**Policies:**
- `WL-2019-004782` — Whole Life
- `TL-2021-008341` — 20-Year Term Life

**Notes:**
- Recently called about updating her mailing address — moving to a new condo
- Annual review due in March 2026
- Referred by her financial advisor at Midwest Financial Group

---

### Customer 2: David Antonio Rodriguez

| Field | Value |
|-------|-------|
| **Client #** | `CLT-00061957` |
| **Full Legal Name** | David Antonio Rodriguez |
| **Preferred Name** | David |
| **DOB** | 07/22/1985 (age 40) |
| **Gender** | Male |
| **SSN (last 4)** | ••••-6195 |
| **Residence Address** | 520 Palmetto Drive, Tampa, FL 33606 |
| **Mailing Address** | Same as residence |
| **Phone** | (813) 555-0283 |
| **Email** | d.rodriguez@email.com |
| **Employer** | Self-employed — Rodriguez Consulting LLC |
| **Agent** | James Whitfield, CFP — Agent #A-08837 |
| **Client Since** | 2020 |

**Policies:**
- `UL-2020-006195` — Universal Life

**Notes:**
- Missed a flexible premium payment in Q3 2025 — policy still active, cash value covers COI
- Interested in adding a term rider for additional coverage
- Business owner, uses policy as part of buy-sell agreement

---

### Customer 3: Sarah & James Thompson

| Field | Value |
|-------|-------|
| **Client # (Sarah)** | `CLT-00032568` |
| **Client # (James)** | `CLT-00032569` |
| **Full Legal Name (Sarah)** | Sarah Elizabeth Thompson |
| **Full Legal Name (James)** | James Michael Thompson |
| **DOB (Sarah)** | 11/03/1970 (age 55) |
| **DOB (James)** | 06/18/1968 (age 57) |
| **Gender** | Female / Male |
| **SSN last 4 (Sarah)** | ••••-3256 |
| **SSN last 4 (James)** | ••••-3257 |
| **Residence Address** | 8902 Willowbrook Lane, Scottsdale, AZ 85260 |
| **Mailing Address** | PO Box 1122, Scottsdale, AZ 85260 |
| **Phone (Sarah)** | (480) 555-0391 |
| **Phone (James)** | (480) 555-0392 |
| **Email** | thompson.family@email.com |
| **Employer (Sarah)** | Retired — former CFO, Valley Medical Center |
| **Employer (James)** | Thompson & Associates Law Firm — Managing Partner |
| **Agent** | Maria Gonzalez-Santos, CLU, LUTCF — Agent #A-05521 |
| **Client Since** | 2018 |

**Policies:**
- `JL-2018-003256` — Joint Survivorship (Second-to-Die) Whole Life
- `TL-2022-009874` — 10-Year Term Life (Sarah only)

**Notes:**
- Joint policy is part of an estate plan — irrevocable life insurance trust (ILIT) owns the policy
- Sarah's term policy was purchased for bridge coverage during estate restructuring
- High-net-worth clients — annual review completed January 2026

---

### Customer 4: Robert "Bob" Okafor

| Field | Value |
|-------|-------|
| **Client #** | `CLT-00021038` |
| **Full Legal Name** | Robert Chukwuemeka Okafor |
| **Preferred Name** | Bob |
| **DOB** | 09/08/1972 (age 53) |
| **Gender** | Male |
| **SSN (last 4)** | ••••-2103 |
| **Residence Address** | 3345 Magnolia Street, Charlotte, NC 28205 |
| **Mailing Address** | Same as residence |
| **Phone** | (704) 555-0718 |
| **Email** | rokafor@email.com |
| **Employer** | Pinnacle Engineering Inc. — Senior Director |
| **Agent** | Patricia Kowalski, CLU, ChFC — Agent #A-11042 |
| **Client Since** | 2017 |

**Policies:**
- `VUL-2017-002103` — Variable Universal Life
- `WL-2023-011548` — Whole Life (recently issued)

**Notes:**
- VUL sub-account allocation was rebalanced in January 2026
- New whole life policy issued November 2023 — still in first-year surrender charge period
- Has expressed interest in long-term care rider options
- Same agent as Margaret Chen — Patricia Kowalski

---

### Customer 5: Linda Park-Watson

| Field | Value |
|-------|-------|
| **Client #** | `CLT-00056473` |
| **Full Legal Name** | Linda Soojin Park-Watson |
| **Preferred Name** | Linda |
| **DOB** | 01/27/1982 (age 44) |
| **Gender** | Female |
| **SSN (last 4)** | ••••-5647 |
| **Residence Address** | 1220 NE Hawthorne Blvd, Portland, OR 97214 |
| **Mailing Address** | Same as residence |
| **Phone** | (503) 555-0462 |
| **Email** | linda.pw@email.com |
| **Employer** | Pacific Northwest Health System — Director of Nursing |
| **Agent** | James Whitfield, CFP — Agent #A-08837 |
| **Client Since** | 2019 |

**Policies:**
- `IUL-2019-005647` — Indexed Universal Life

**Notes:**
- Policy allocated 60% to S&P 500 index account, 40% to fixed account
- Recently increased monthly premium from $800 to $1,000 to maximize cash accumulation
- Same agent as David Rodriguez — James Whitfield
- Has a pending address change (moving within Portland)

---

## Policies

### Policy: WL-2019-004782 — Whole Life

| Field | Value |
|-------|-------|
| **Product** | SecureLife Whole Life 100 |
| **Status** | Active — Premium Paying (`AC-PP`) |
| **Face Amount** | $500,000 |
| **Issue Date** | 04/01/2019 |
| **Issue Age** | 41 |
| **Maturity Date** | 03/15/2078 (age 100) |
| **Risk Class** | Preferred Non-Tobacco |
| **Underwriting** | Full medical exam |

**Parties:**
| Role | Name | DOB | Relationship |
|------|------|-----|-------------|
| Owner | Margaret W. Chen | 03/15/1978 | Self |
| Insured | Margaret W. Chen | 03/15/1978 | — |
| Payor | Margaret W. Chen | — | Self |

**Beneficiary Designations:**
| Tier | Beneficiary | Relationship | Share | Distribution | Type |
|------|-------------|-------------|-------|-------------|------|
| Primary | David Chen | Spouse | 100% | Per stirpes | Revocable |
| Contingent | Jennifer Chen | Daughter | 50% | Per capita | Revocable |
| Contingent | Michael Chen | Son | 50% | Per capita | Revocable |

**Riders:**
| Rider | Benefit | Status | Annual Premium |
|-------|---------|--------|----------------|
| Waiver of Premium | Waives premium on disability | Active | $187.00 |
| Accelerated Death Benefit | Up to 75% of face, terminal illness | Active | Included |
| Paid-Up Additions (Dividend) | Participating dividends purchase PUAs | Active | N/A (dividend-funded) |

**Premium Information:**
| Field | Value |
|-------|-------|
| Annual Premium | $7,845.00 |
| Payment Mode | Monthly |
| Modal Premium | $672.50 |
| Billing Method | EFT — account ending 3847 |
| Auto-Pay | Active |
| Next Due Date | 03/01/2026 |
| Last Payment | $672.50 on 02/01/2026 |

**Policy Values (as of 02/28/2026):**
| Value | Amount |
|-------|--------|
| Gross Cash Value | $48,237.15 |
| Surrender Charges | $0.00 |
| Outstanding Loan | $0.00 |
| Net Cash Surrender Value | $48,237.15 |
| Paid-Up Addition Cash Value | $5,412.80 |
| Accumulated Dividends | $3,287.44 |
| Total Death Benefit | $519,680.00 (includes PUA face) |
| Total Premiums Paid | $54,015.00 |
| Cost Basis | $54,015.00 |
| Dividend Option | Paid-Up Additions |

**Recent Transactions:**
| Date | Transaction | Amount | Status |
|------|------------|--------|--------|
| 02/01/2026 | Monthly Premium — EFT | $672.50 | Applied |
| 01/15/2026 | Annual Dividend Credited | $1,247.30 | Applied |
| 01/01/2026 | Monthly Premium — EFT | $672.50 | Applied |
| 12/01/2025 | Monthly Premium — EFT | $672.50 | Applied |
| 11/01/2025 | Monthly Premium — EFT | $672.50 | Applied |

---

### Policy: TL-2021-008341 — 20-Year Term

| Field | Value |
|-------|-------|
| **Product** | ValueTerm 20 |
| **Status** | Active — Premium Paying (`AC-PP`) |
| **Face Amount** | $1,000,000 |
| **Issue Date** | 06/15/2021 |
| **Issue Age** | 43 |
| **Expiration Date** | 06/15/2041 |
| **Risk Class** | Preferred Non-Tobacco |
| **Underwriting** | Full medical exam |

**Parties:**
| Role | Name | DOB | Relationship |
|------|------|-----|-------------|
| Owner | Margaret W. Chen | 03/15/1978 | Self |
| Insured | Margaret W. Chen | 03/15/1978 | — |
| Payor | Margaret W. Chen | — | Self |

**Beneficiary Designations:**
| Tier | Beneficiary | Relationship | Share | Distribution | Type |
|------|-------------|-------------|-------|-------------|------|
| Primary | David Chen | Spouse | 100% | Per stirpes | Revocable |
| Contingent | Chen Family Trust dtd 05/10/2021 | Trust | 100% | N/A | Revocable |

**Riders:**
| Rider | Benefit | Status | Annual Premium |
|-------|---------|--------|----------------|
| Conversion Privilege | Convert to permanent without evidence | Active | Included |
| Accelerated Death Benefit | Up to 50% of face, terminal illness | Active | Included |

**Premium Information:**
| Field | Value |
|-------|-------|
| Annual Premium | $1,124.00 |
| Payment Mode | Annual |
| Modal Premium | $1,124.00 |
| Billing Method | Direct bill |
| Auto-Pay | Inactive |
| Next Due Date | 06/15/2026 |
| Last Payment | $1,124.00 on 06/10/2025 |

**Conversion Details:**
| Field | Value |
|-------|-------|
| Convertible | Yes |
| Conversion Deadline | 06/15/2036 (or age 60, whichever is earlier) |
| Eligible Products | SecureLife Whole Life 100, FlexLife Universal Life, IndexGrowth IUL |
| Conversion Basis | Attained age at conversion |

**Recent Transactions:**
| Date | Transaction | Amount | Status |
|------|------------|--------|--------|
| 06/10/2025 | Annual Premium — Check | $1,124.00 | Applied |
| 06/12/2024 | Annual Premium — Check | $1,124.00 | Applied |
| 06/15/2023 | Annual Premium — Check | $1,124.00 | Applied |

---

### Policy: UL-2020-006195 — Universal Life

| Field | Value |
|-------|-------|
| **Product** | FlexLife Universal Life |
| **Status** | Active — Premium Paying (`AC-PP`) |
| **Face Amount** | $750,000 |
| **Death Benefit Option** | Option A — Level death benefit |
| **Issue Date** | 02/01/2020 |
| **Issue Age** | 34 |
| **Maturity Date** | 07/22/2085 (age 100) |
| **Risk Class** | Standard Non-Tobacco |
| **Underwriting** | Full medical exam |

**Parties:**
| Role | Name | DOB | Relationship |
|------|------|-----|-------------|
| Owner | David A. Rodriguez | 07/22/1985 | Self |
| Insured | David A. Rodriguez | 07/22/1985 | — |
| Payor | David A. Rodriguez | — | Self |

**Beneficiary Designations:**
| Tier | Beneficiary | Relationship | Share | Distribution | Type |
|------|-------------|-------------|-------|-------------|------|
| Primary | Maria Elena Rodriguez | Spouse | 70% | Per stirpes | Revocable |
| Primary | Sofia Rodriguez | Daughter | 15% | Per capita | Revocable |
| Primary | Lucas Rodriguez | Son | 15% | Per capita | Revocable |
| Contingent | Rosa Rodriguez | Mother | 100% | Per stirpes | Revocable |

**Riders:**
| Rider | Benefit | Status | Annual Premium |
|-------|---------|--------|----------------|
| Waiver of Premium | Waives COI on disability | Active | $214.00/yr |
| Accidental Death Benefit | Additional $750,000 for accidental death | Active | $187.50/yr |
| Children's Term Rider | $25,000 per child, to age 25 | Active | $75.00/yr |

**Premium Information:**
| Field | Value |
|-------|-------|
| Target Premium | $6,500.00/year |
| Minimum Premium (keep in force) | $4,120.00/year (current COI + charges) |
| Payment Mode | Quarterly |
| Planned Quarterly Premium | $1,625.00 |
| Billing Method | EFT — account ending 7291 |
| Auto-Pay | Active |
| Next Due Date | 04/01/2026 |
| Last Payment | $1,625.00 on 01/03/2026 |

**Note:** Q3 2025 premium ($1,625.00 due 07/01/2025) was missed. Policy remained in force — COI deducted from account value. Total account value impact: approximately $1,980 (COI + missed premium accumulation).

**Policy Values (as of 02/28/2026):**
| Value | Amount |
|-------|--------|
| Account Value | $31,847.22 |
| Surrender Charges | ($2,150.00) |
| Outstanding Loan | $0.00 |
| Net Cash Surrender Value | $29,697.22 |
| Death Benefit | $750,000.00 |
| Guaranteed Interest Rate | 2.00% |
| Current Credited Rate | 4.35% |
| Total Premiums Paid | $35,750.00 |
| Cost Basis | $35,750.00 |
| Monthly COI + Charges | $164.80 |

**Recent Transactions:**
| Date | Transaction | Amount | Status |
|------|------------|--------|--------|
| 02/01/2026 | Monthly COI Deduction | ($164.80) | Applied |
| 01/03/2026 | Quarterly Premium — EFT | $1,625.00 | Applied |
| 01/01/2026 | Monthly COI Deduction | ($164.80) | Applied |
| 01/01/2026 | Interest Credit (4.35% annual) | $112.37 | Applied |
| 12/01/2025 | Monthly COI Deduction | ($164.80) | Applied |

---

### Policy: JL-2018-003256 — Joint Survivorship Whole Life

| Field | Value |
|-------|-------|
| **Product** | LegacyGuard Survivorship Whole Life |
| **Status** | Active — Premium Paying (`AC-PP`) |
| **Face Amount** | $2,000,000 |
| **Issue Date** | 09/01/2018 |
| **Issue Ages** | Sarah: 47 / James: 50 |
| **Maturity Date** | Second death or November 2068 (younger insured age 98) |
| **Risk Class** | Joint Standard Non-Tobacco |
| **Underwriting** | Full medical exam — both insureds |
| **Death Benefit Trigger** | Second to die |

**Parties:**
| Role | Name | DOB | Relationship |
|------|------|-----|-------------|
| Owner | Thompson Family ILIT dtd 08/15/2018 | N/A | Irrevocable Trust |
| Trustee | First National Bank & Trust | N/A | Corporate Trustee |
| Insured 1 | Sarah E. Thompson | 11/03/1970 | — |
| Insured 2 | James M. Thompson | 06/18/1968 | — |
| Payor | Thompson Family ILIT | — | Trust |

**Beneficiary Designations:**
| Tier | Beneficiary | Relationship | Share | Distribution | Type |
|------|-------------|-------------|-------|-------------|------|
| Primary | Emily Thompson | Daughter | 33.34% | Per stirpes | Irrevocable |
| Primary | Andrew Thompson | Son | 33.33% | Per stirpes | Irrevocable |
| Primary | Olivia Thompson | Daughter | 33.33% | Per stirpes | Irrevocable |
| Contingent | Thompson Family Foundation | Charity | 100% | N/A | Irrevocable |

**⚠️ Note:** This policy is owned by an **Irrevocable Life Insurance Trust (ILIT)**. All changes require trustee authorization from First National Bank & Trust. Beneficiary changes require consent of all irrevocable beneficiaries and may require court approval.

**Riders:**
| Rider | Benefit | Status | Annual Premium |
|-------|---------|--------|----------------|
| Waiver of Premium | Waives on disability of either insured | Active | $847.00/yr |
| Accelerated Death Benefit | Up to 50% on terminal illness (either insured) | Active | Included |

**Premium Information:**
| Field | Value |
|-------|-------|
| Annual Premium | $28,450.00 |
| Payment Mode | Annual |
| Modal Premium | $28,450.00 |
| Billing Method | Direct bill to trustee — First National Bank & Trust |
| Auto-Pay | Inactive (trustee processes manually) |
| Next Due Date | 09/01/2026 |
| Last Payment | $28,450.00 on 08/28/2025 |

**Policy Values (as of 02/28/2026):**
| Value | Amount |
|-------|--------|
| Gross Cash Value | $187,542.80 |
| Surrender Charges | $0.00 |
| Outstanding Loan | $0.00 |
| Net Cash Surrender Value | $187,542.80 |
| Paid-Up Addition Cash Value | $22,815.40 |
| Accumulated Dividends | $11,478.22 |
| Total Death Benefit | $2,067,350.00 (includes PUA face) |
| Total Premiums Paid | $213,375.00 |
| Cost Basis | $213,375.00 |
| Dividend Option | Paid-Up Additions |

**Recent Transactions:**
| Date | Transaction | Amount | Status |
|------|------------|--------|--------|
| 01/15/2026 | Annual Dividend Credited | $6,124.50 | Applied |
| 08/28/2025 | Annual Premium — Check (trustee) | $28,450.00 | Applied |
| 01/15/2025 | Annual Dividend Credited | $5,687.20 | Applied |
| 08/30/2024 | Annual Premium — Check (trustee) | $28,450.00 | Applied |

---

### Policy: TL-2022-009874 — 10-Year Term (Sarah Thompson)

| Field | Value |
|-------|-------|
| **Product** | ValueTerm 10 |
| **Status** | Active — Premium Paying (`AC-PP`) |
| **Face Amount** | $500,000 |
| **Issue Date** | 03/01/2022 |
| **Issue Age** | 51 |
| **Expiration Date** | 03/01/2032 |
| **Risk Class** | Standard Non-Tobacco |
| **Underwriting** | Accelerated (no exam) |

**Parties:**
| Role | Name | DOB | Relationship |
|------|------|-----|-------------|
| Owner | Sarah E. Thompson | 11/03/1970 | Self |
| Insured | Sarah E. Thompson | 11/03/1970 | — |
| Payor | Sarah E. Thompson | — | Self |

**Beneficiary Designations:**
| Tier | Beneficiary | Relationship | Share | Distribution | Type |
|------|-------------|-------------|-------|-------------|------|
| Primary | James M. Thompson | Spouse | 100% | Per stirpes | Revocable |
| Contingent | Emily Thompson | Daughter | 34% | Per capita | Revocable |
| Contingent | Andrew Thompson | Son | 33% | Per capita | Revocable |
| Contingent | Olivia Thompson | Daughter | 33% | Per capita | Revocable |

**Riders:**
| Rider | Benefit | Status | Annual Premium |
|-------|---------|--------|----------------|
| Conversion Privilege | Convert without evidence to age 65 | Active | Included |
| Accelerated Death Benefit | Up to 50% on terminal illness | Active | Included |

**Premium Information:**
| Field | Value |
|-------|-------|
| Annual Premium | $2,340.00 |
| Payment Mode | Semi-Annual |
| Modal Premium | $1,193.40 |
| Billing Method | EFT — account ending 5508 |
| Auto-Pay | Active |
| Next Due Date | 03/01/2026 |
| Last Payment | $1,193.40 on 09/01/2025 |

**Conversion Details:**
| Field | Value |
|-------|-------|
| Convertible | Yes |
| Conversion Deadline | 03/01/2032 (or age 65, whichever is earlier) |
| Eligible Products | SecureLife Whole Life 100, FlexLife Universal Life |
| Conversion Basis | Attained age |

**Recent Transactions:**
| Date | Transaction | Amount | Status |
|------|------------|--------|--------|
| 09/01/2025 | Semi-Annual Premium — EFT | $1,193.40 | Applied |
| 03/01/2025 | Semi-Annual Premium — EFT | $1,193.40 | Applied |
| 09/01/2024 | Semi-Annual Premium — EFT | $1,193.40 | Applied |

---

### Policy: VUL-2017-002103 — Variable Universal Life

| Field | Value |
|-------|-------|
| **Product** | InvestLife Variable Universal Life |
| **Status** | Active — Premium Paying (`AC-PP`) |
| **Face Amount** | $1,000,000 |
| **Death Benefit Option** | Option B — Increasing (face + account value) |
| **Issue Date** | 11/01/2017 |
| **Issue Age** | 45 |
| **Maturity Date** | 09/08/2072 (age 100) |
| **Risk Class** | Preferred Non-Tobacco |
| **Underwriting** | Full medical exam |

**Parties:**
| Role | Name | DOB | Relationship |
|------|------|-----|-------------|
| Owner | Robert C. Okafor | 09/08/1972 | Self |
| Insured | Robert C. Okafor | 09/08/1972 | — |
| Payor | Robert C. Okafor | — | Self |

**Beneficiary Designations:**
| Tier | Beneficiary | Relationship | Share | Distribution | Type |
|------|-------------|-------------|-------|-------------|------|
| Primary | Grace Okafor | Spouse | 60% | Per stirpes | Revocable |
| Primary | Okafor Education Trust dtd 03/01/2020 | Trust | 40% | N/A | Revocable |
| Contingent | Chukwuma Okafor | Brother | 100% | Per stirpes | Revocable |

**Riders:**
| Rider | Benefit | Status | Annual Premium |
|-------|---------|--------|----------------|
| Waiver of Premium | Waives COI on disability (to age 65) | Active | $312.00/yr |
| Overloan Protection | Prevents lapse from excessive loans | Active | $95.00/yr |
| Accelerated Death Benefit | Up to 75% on terminal / chronic illness | Active | Included |

**Premium Information:**
| Field | Value |
|-------|-------|
| Target Premium | $12,000.00/year |
| Minimum Premium | $7,840.00/year (current COI + charges) |
| Payment Mode | Monthly |
| Planned Monthly Premium | $1,000.00 |
| Billing Method | EFT — account ending 0847 |
| Auto-Pay | Active |
| Next Due Date | 03/01/2026 |
| Last Payment | $1,000.00 on 02/01/2026 |

**Sub-Account Allocation (as of 02/28/2026):**
| Fund | Allocation | Current Value | YTD Return |
|------|-----------|---------------|------------|
| Vanguard S&P 500 Index | 40% | $47,892.18 | +4.2% |
| Fidelity Growth Company | 20% | $24,115.40 | +5.1% |
| PIMCO Total Return Bond | 20% | $22,847.60 | +1.3% |
| American Funds EuroPacific | 10% | $11,203.75 | +2.8% |
| Fixed Account (3.50% guaranteed) | 10% | $11,547.30 | +0.6% (YTD) |

**Policy Values (as of 02/28/2026):**
| Value | Amount |
|-------|--------|
| Total Account Value | $117,606.23 |
| Surrender Charges | ($1,200.00) |
| Outstanding Loan | ($15,000.00) |
| Loan Interest Accrued | ($487.50) |
| Net Cash Surrender Value | $100,918.73 |
| Death Benefit (Option B) | $1,117,606.23 |
| Loan Interest Rate | 5.00% variable |
| Loan Available | $82,324.36 |
| Total Premiums Paid | $99,600.00 |
| Cost Basis | $99,600.00 |
| Monthly COI + Charges | $287.50 |

**Loan History:**
| Date | Type | Amount | Balance After |
|------|------|--------|---------------|
| 06/15/2024 | Loan Disbursement | $15,000.00 | $15,000.00 |

**Recent Transactions:**
| Date | Transaction | Amount | Status |
|------|------------|--------|--------|
| 02/01/2026 | Monthly Premium — EFT | $1,000.00 | Applied |
| 02/01/2026 | Monthly COI Deduction | ($287.50) | Applied |
| 01/15/2026 | Sub-Account Rebalance | — | Processed |
| 01/01/2026 | Monthly Premium — EFT | $1,000.00 | Applied |
| 01/01/2026 | Monthly COI Deduction | ($287.50) | Applied |

---

### Policy: WL-2023-011548 — Whole Life (Robert Okafor)

| Field | Value |
|-------|-------|
| **Product** | SecureLife Whole Life 100 |
| **Status** | Active — Premium Paying (`AC-PP`) |
| **Face Amount** | $250,000 |
| **Issue Date** | 11/15/2023 |
| **Issue Age** | 51 |
| **Maturity Date** | 09/08/2072 (age 100) |
| **Risk Class** | Standard Non-Tobacco |
| **Underwriting** | Full medical exam |

**Parties:**
| Role | Name | DOB | Relationship |
|------|------|-----|-------------|
| Owner | Robert C. Okafor | 09/08/1972 | Self |
| Insured | Robert C. Okafor | 09/08/1972 | — |
| Payor | Robert C. Okafor | — | Self |

**Beneficiary Designations:**
| Tier | Beneficiary | Relationship | Share | Distribution | Type |
|------|-------------|-------------|-------|-------------|------|
| Primary | Grace Okafor | Spouse | 100% | Per stirpes | Revocable |
| Contingent | Okafor Education Trust dtd 03/01/2020 | Trust | 100% | N/A | Revocable |

**Riders:**
| Rider | Benefit | Status | Annual Premium |
|-------|---------|--------|----------------|
| Accelerated Death Benefit | Up to 75% on terminal illness | Active | Included |
| Paid-Up Additions (Dividend) | Dividends purchase PUAs | Active | N/A |

**Premium Information:**
| Field | Value |
|-------|-------|
| Annual Premium | $6,875.00 |
| Payment Mode | Monthly |
| Modal Premium | $589.80 |
| Billing Method | EFT — account ending 0847 |
| Auto-Pay | Active |
| Next Due Date | 03/15/2026 |
| Last Payment | $589.80 on 02/15/2026 |

**Policy Values (as of 02/28/2026):**
| Value | Amount |
|-------|--------|
| Gross Cash Value | $4,215.60 |
| Surrender Charges | ($3,150.00) |
| Outstanding Loan | $0.00 |
| Net Cash Surrender Value | $1,065.60 |
| Death Benefit | $250,000.00 |
| Total Premiums Paid | $15,937.50 |
| Cost Basis | $15,937.50 |
| Dividend Option | Paid-Up Additions |

**Note:** Policy is in first-year surrender charge period until 11/15/2026. Surrender value is significantly less than premiums paid. Advise against surrender during this period.

**Recent Transactions:**
| Date | Transaction | Amount | Status |
|------|------------|--------|--------|
| 02/15/2026 | Monthly Premium — EFT | $589.80 | Applied |
| 01/15/2026 | Monthly Premium — EFT | $589.80 | Applied |
| 01/15/2026 | Annual Dividend Credited | $187.40 | Applied |
| 12/15/2025 | Monthly Premium — EFT | $589.80 | Applied |
| 11/15/2025 | Policy Anniversary Processing | — | Applied |

---

### Policy: IUL-2019-005647 — Indexed Universal Life

| Field | Value |
|-------|-------|
| **Product** | IndexGrowth Indexed Universal Life |
| **Status** | Active — Premium Paying (`AC-PP`) |
| **Face Amount** | $600,000 |
| **Death Benefit Option** | Option A — Level death benefit |
| **Issue Date** | 08/01/2019 |
| **Issue Age** | 37 |
| **Maturity Date** | 01/27/2082 (age 100) |
| **Risk Class** | Preferred Non-Tobacco |
| **Underwriting** | Full medical exam |

**Parties:**
| Role | Name | DOB | Relationship |
|------|------|-----|-------------|
| Owner | Linda S. Park-Watson | 01/27/1982 | Self |
| Insured | Linda S. Park-Watson | 01/27/1982 | — |
| Payor | Linda S. Park-Watson | — | Self |

**Beneficiary Designations:**
| Tier | Beneficiary | Relationship | Share | Distribution | Type |
|------|-------------|-------------|-------|-------------|------|
| Primary | Thomas Watson | Spouse | 60% | Per stirpes | Revocable |
| Primary | Hana Watson | Daughter | 20% | Per capita | Revocable |
| Primary | Ethan Watson | Son | 20% | Per capita | Revocable |
| Contingent | Soonja Park | Mother | 50% | Per stirpes | Revocable |
| Contingent | Minjun Park | Father | 50% | Per stirpes | Revocable |

**Riders:**
| Rider | Benefit | Status | Annual Premium |
|-------|---------|--------|----------------|
| Waiver of Premium | Waives COI on disability | Active | $178.00/yr |
| Chronic Illness Rider | Accelerates DB for qualifying chronic illness | Active | Included |
| Index Lock | Lock in index gains mid-segment | Active | $120.00/yr |

**Premium Information:**
| Field | Value |
|-------|-------|
| Target Premium | $9,600.00/year (originally) |
| Current Planned Premium | $12,000.00/year (increased 01/2026) |
| Minimum Premium | $3,240.00/year (current COI + charges) |
| Payment Mode | Monthly |
| Planned Monthly Premium | $1,000.00 (was $800.00 until 12/2025) |
| Billing Method | EFT — account ending 6214 |
| Auto-Pay | Active |
| Next Due Date | 03/01/2026 |
| Last Payment | $1,000.00 on 02/01/2026 |

**Index Account Allocation:**
| Account | Allocation | Cap Rate | Floor | Participation Rate | Current Value |
|---------|-----------|----------|-------|-------------------|---------------|
| S&P 500 Annual Point-to-Point | 60% | 10.50% | 0% | 100% | $38,247.60 |
| Fixed Account | 40% | N/A | N/A | N/A | $25,018.40 |
| Fixed Account Credited Rate | — | — | — | — | 3.75% |

**Policy Values (as of 02/28/2026):**
| Value | Amount |
|-------|--------|
| Total Account Value | $63,266.00 |
| Surrender Charges | ($1,580.00) |
| Outstanding Loan | $0.00 |
| Net Cash Surrender Value | $61,686.00 |
| Death Benefit | $600,000.00 |
| Total Premiums Paid | $53,600.00 |
| Cost Basis | $53,600.00 |
| Monthly COI + Charges | $142.20 |

**Index Segment History (Last 3 Annual Segments):**
| Segment Start | Segment End | Index Return | Credited Rate | Status |
|--------------|------------|-------------|---------------|--------|
| 08/01/2025 | 07/31/2026 | +6.8% (projected) | TBD | Open |
| 08/01/2024 | 07/31/2025 | +12.4% | 10.50% (capped) | Settled |
| 08/01/2023 | 07/31/2024 | +8.2% | 8.20% | Settled |

**Pending Transactions:**
| Transaction | Submitted | Status | Expected Completion |
|------------|-----------|--------|-------------------|
| Address Change | 02/20/2026 | In Process | 03/01/2026 |
| New address: 4455 SE Division Street, Apt 7, Portland, OR 97206 |

**Recent Transactions:**
| Date | Transaction | Amount | Status |
|------|------------|--------|--------|
| 02/20/2026 | Address Change Submitted | — | Pending |
| 02/01/2026 | Monthly Premium — EFT | $1,000.00 | Applied |
| 02/01/2026 | Monthly COI Deduction | ($142.20) | Applied |
| 01/01/2026 | Monthly Premium — EFT | $1,000.00 | Applied |
| 01/01/2026 | Premium Increase Processed (from $800 to $1,000/mo) | — | Applied |

---

## Agent Directory

| Agent # | Name | Credentials | Phone | Email | Region |
|---------|------|-------------|-------|-------|--------|
| A-11042 | Patricia Kowalski | CLU, ChFC | (312) 555-0800 | p.kowalski@agencymail.com | Midwest |
| A-08837 | James Whitfield | CFP | (503) 555-0900 | j.whitfield@agencymail.com | West Coast |
| A-05521 | Maria Gonzalez-Santos | CLU, LUTCF | (480) 555-0700 | m.gonzalez@agencymail.com | Southwest |

---

## Product Reference

| Product Code | Product Name | Type | Min Face | Max Issue Age |
|-------------|-------------|------|----------|---------------|
| WL | SecureLife Whole Life 100 | Permanent — Whole Life | $50,000 | 80 |
| TL-10 | ValueTerm 10 | Term — 10 Year Level | $100,000 | 70 |
| TL-20 | ValueTerm 20 | Term — 20 Year Level | $100,000 | 65 |
| TL-30 | ValueTerm 30 | Term — 30 Year Level | $100,000 | 55 |
| UL | FlexLife Universal Life | Permanent — Universal Life | $100,000 | 75 |
| VUL | InvestLife Variable Universal Life | Permanent — Variable UL | $250,000 | 70 |
| IUL | IndexGrowth Indexed Universal Life | Permanent — Indexed UL | $100,000 | 70 |
| JL | LegacyGuard Survivorship Whole Life | Permanent — Joint Second-to-Die | $500,000 | 80 |

---

## Using This Skill

When ~~policy admin system is not connected, this mock data serves as the complete source of truth for all commands. Treat it as a live system response:

- Return realistic data from this skill as if querying an API
- Maintain the data's internal consistency — don't invent additional customers or policies
- For transactions that modify data (address change, beneficiary change), describe the change as successfully submitted and provide a confirmation number in the format `[TYPE]-2026-[6-digit random]`
- If a user queries something not in this dataset, respond with "No records found" just as a real system would
- Never expose full SSNs — always mask as `••••-[last 4]`
