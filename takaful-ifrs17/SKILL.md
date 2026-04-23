---
name: takaful-ifrs17
description: >
  Activate for: takaful, Islamic insurance, wakala model, mudaraba takaful,
  participants fund, qard hasan takaful, takaful deficit, family takaful,
  general takaful, IFRS 17 takaful, MFRS 17 takaful, retakaful,
  wakala fee, takaful surplus, takaful operator, participants risk fund.
metadata:
  version: "1.0"
  author: "Panaversity — The AI Agent Factory"
  standard: "IFRS 17 Insurance Contracts, AAOIFI FAS 12 (General Presentation)"
---

## THE TAKAFUL STRUCTURE

Takaful is Islamic mutual insurance:
- **Participants** contribute to a common fund (Participants' Risk Fund / Takaful Pool).
- **Participants collectively** bear the insurance risk (not the operator).
- **The takaful operator** manages the fund for a fee (wakala model) or profit share (mudaraba model).

This distinguishes takaful from conventional insurance:
In conventional insurance: insurer takes premium, bears risk, keeps underwriting profit.
In takaful: operator manages the fund, earns fee only, does not bear insurance risk.

## THE THREE OPERATING MODELS

**Wakala model:**
Operator earns a FIXED PERCENTAGE of contributions as a wakala fee (e.g., 25-35%).
Operator does NOT share in underwriting surplus or bear underwriting risk.
All surplus/deficit belongs to participants (and may be distributed to them or retained in fund).

**Mudaraba model:**
Operator manages investments of the Participants' Fund as a mudarib.
Operator shares in INVESTMENT INCOME (profit-sharing ratio, e.g., 30% to operator, 70% to fund).
Operator may also share in underwriting surplus in some models.

**Hybrid model (most common in Malaysia, GCC):**
Wakala fee for underwriting management + mudaraba for investment management.

---

## THE FUNDAMENTAL IFRS 17 QUESTION

**Who is the "insurer" under IFRS 17?**

IFRS 17 applies to an entity that has issued insurance contracts — contracts under
which the entity accepts significant insurance risk.

**Wakala operator analysis:**
The operator charges a fee and DOES NOT bear insurance risk.
The PARTICIPANTS collectively bear insurance risk.
→ Potentially, IFRS 17 does not apply to the OPERATOR's own financial statements.
→ IFRS 17 may apply to the PARTICIPANTS' FUND (as the entity that accepts risk).
→ But the Participants' Fund is not a separate legal entity in most structures.

**Regulator positions:**
- Malaysia (BNM/SAC ruling): IFRS 17 DOES apply to takaful operators. The operator
  is viewed as taking on insurance risk through its management role and qard obligation.
  BNM's Financial Reporting for Takaful Operators Policy Document provides specific guidance.
- UAE, UK: No equivalent regulatory ruling as of 2025. Operators must determine
  applicability based on the specific facts of their model.

**DEFAULT INSTRUCTION:** Apply IFRS 17 to the takaful operator unless:
(a) The jurisdiction overlay specifies otherwise, or
(b) The operator has obtained a specific SSB/regulatory determination.

---

## TWO FINANCIAL STATEMENTS TO MAINTAIN

**1. Operator's Financial Statements:**
Records the operator's own revenues, expenses, assets, and liabilities.
Revenue: Wakala fee (% of contributions)
Expenses: Staff, overheads, management costs
Assets: Investments of the operator's own funds, qard receivable from Participants' Fund (if any)
Liabilities: Qard payable to participants (if operator is indebted)

**2. Participants' Fund (Takaful Pool) Statement:**
A separate fund maintained within (but separate from) the operator's books.
Revenue: Contributions received − Wakala fee paid to operator + Investment income
Expenses: Claims paid + Retakaful ceded + Management expenses
Balance: Fund surplus (distributed to participants or retained) or deficit (→ triggers qard)

---

## JOURNAL ENTRIES — WAKALA MODEL

**Contributions received (gross):**
Dr: Cash [Total contributions]
Cr: Participants' Fund — Contributions [Total contributions]

**Wakala fee deduction:**
Dr: Participants' Fund — Wakala Fee Paid [Fee amount]
Cr: Takaful Operator Income — Wakala Fee [Fee amount]

**Claims paid from Participants' Fund:**
Dr: Participants' Fund — Claims Expense [Claim amount]
Cr: Cash [Claim amount]

**Investment income on Participants' Fund assets:**
Dr: Participants' Fund Investments — Accrued Income
Cr: Participants' Fund — Investment Income

**Period-end surplus/deficit calculation:**
Surplus = Contributions − Wakala fee − Claims − Expenses + Investment Income
If SURPLUS: may be distributed to participants or transferred to reserves.
If DEFICIT: → triggers qard obligation (see below).

---

## QARD HASAN (INTEREST-FREE LOAN) FOR FUND DEFICIT

When the Participants' Fund is in DEFICIT (cannot meet claims from contributions):
The takaful operator MUST provide a qard hasan (interest-free loan) to restore solvency.
This is a Shariah obligation, not a commercial decision.

**In Operator's Books — Qard provided:**
Dr: Qard Receivable from Participants' Fund [Loan amount]
Cr: Cash [Loan amount]

Note: The qard receivable is at risk if the fund never recovers.
Impairment assessment under IFRS 9 is required for the qard receivable.
If recovery is unlikely: impair the receivable → loss in operator's P&L.

**IAS 37 Contingent Qard Obligation:**
Before a deficit materialises, the operator has a contingent obligation to provide qard.
IAS 37 analysis: Is there a present obligation from a past event (the wakala contract)?
If the operator has unconditionally committed to providing qard whenever needed → provision.
If contingent only → disclose as a contingent liability (IAS 37.86).

**In Participants' Fund books:**
Dr: Cash [Qard received]
Cr: Qard Payable to Operator [Same]
Repayment from future surpluses of the fund.

---

## IFRS 17 MEASUREMENT MODELS

**Premium Allocation Approach (PAA):** Simplification for contracts with coverage ≤ 12 months.
Most general takaful (motor, property, medical) → PAA eligible.
Family takaful (life / long-term): usually requires General Measurement Model (GMM).

**GMM (General Measurement Model / Building Block Approach):**
Used for long-term family takaful and when PAA is not eligible.
Three blocks:
1. Present value of fulfilment cash flows
2. Risk adjustment for non-financial risk
3. Contractual Service Margin (CSM)

---

## MANDATORY DISCLOSURES

**IFRS 17:**
1. Which measurement model applied (GMM, PAA, or VFA) and why
2. Reconciliation of insurance contract liabilities / assets
3. Insurance revenue recognised
4. Insurance service expenses
5. Net financial results from insurance contracts
6. Sensitivity analysis (for GMM contracts)

**AAOIFI / Shariah supplementary:**
1. Wakala fee rate and basis for determination
2. Participants' Fund statement (separate from operator accounts)
3. Surplus/deficit for the period and disposition of surplus
4. Qard balance: amount, terms, repayment schedule
5. SSB report confirming Shariah compliance of the operating model
