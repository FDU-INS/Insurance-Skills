---
name: business-formation
description: Guide founders through operational fundamentals — entity setup, co-founder agreements, IP assignment, banking, bookkeeping, taxes, insurance, and contractor agreements. Phase-based interactive guided process.
trigger_phrases:
  - "business formation"
  - "set up my company"
  - "LLC or C-Corp"
  - "legal structure"
  - "operations setup"
  - "stage 5"
benefits-from:
  - founder-profile
  - runway-calculator
feeds-into:
  - runway-calculator
version: 2.0
---

# Business Formation & Legal Structure (Guided Interactive)

You've been building for weeks or months. Code is shipping. But here's the uncomfortable question: **Who actually owns this company?** Who owns the code? If something goes wrong, what are you personally liable for?

Most technical founders skip this section entirely. Then at funding time — or worse, during a co-founder conflict — they discover they've built everything under a structure that was never set up. This skill ensures you've asked the right questions and have a documented plan.

**DISCLAIMER:** This is NOT legal or tax advice. Consult a lawyer and accountant for your specific situation. This skill ensures you've asked the right questions.

## Phase Overview

This skill works in phases:
- **Phase 0:** Understanding current status
- **Phase 1:** Entity structure (LLC vs. C-Corp)
- **Phase 2:** Co-founder agreements (equity, vesting, IP)
- **Phase 3:** Banking setup
- **Phase 4:** Bookkeeping & financial tracking
- **Phase 5:** Tax planning
- **Phase 6:** Insurance
- **Phase 7:** Contractor agreements
- **Phase 8:** Output & checklist
- **Phase 9:** Completion

Each phase uses AskUserQuestion guided interactions.

---

## Phase 0: Current Status Assessment

**Goal:** Understand what you've already done (if anything).

I will ask:
- Have you formed any legal entity yet?
- Do you have co-founders?
- Have you opened a business bank account?
- Are you tracking expenses?
- Have you thought about fundraising?

**Exit criteria:** I understand your starting point. Move to Phase 1 (Entity Structure).

---

## Phase 1: Entity Structure

**Goal:** Decide between LLC (simple, bootstrap) or C-Corp (fundraising-ready).

**Re-ground:** "We're deciding entity structure. This determines liability protection, tax treatment, and ability to raise funding."

Use AskUserQuestion tool:

**SIMPLIFY:** "LLC = simpler, cheaper setup ($100-500), but VCs won't fund it. C-Corp = more complex, pricier ($500-2K+), but required if you ever want institutional investment. If you think you might raise money in 2-5 years, pick C-Corp. If you're bootstrapping forever, LLC is fine."

**RECOMMEND:** "RECOMMENDATION: If you might raise funding, C-Corp now (you'll need it). If purely bootstrapped and solo, LLC is simpler.
- Completeness: 5/10 (no structure yet)
- Completeness: 7/10 (structure chosen, state not)
- Completeness: 10/10 (entity formed, state selected, paperwork filed)"

**OPTIONS:**
- **(A)** "I'm planning to raise funding. C-Corp (Delaware or home state)."
- **(B)** "I'm bootstrapping, solo founder. LLC is simpler."
- **(C)** "I have co-founders. We need C-Corp with proper equity structure."
- **(D)** "I'm not sure. What would you recommend?"

**For C-Corp, ask:**
- Delaware (best for funded startups) or home state (simpler)?
- Delaware has better legal precedent but you'll pay home state taxes anyway.

**For LLC, ask:**
- Will you ever want to raise institutional funding? If yes, you'll regret LLC.
- Are you solo or co-founders? (Co-founders should use C-Corp for equity clarity)

**Red flags:**
- "We'll form LLC now and convert to C-Corp later" (conversion is expensive/painful)
- "We'll figure out legal structure later" (do it now, easier)
- "We don't need liability protection" (you do)

**Exit criteria for Phase 1:** Entity type chosen (LLC or C-Corp) and state selected. Move to Phase 2 (Co-founder Agreements).

---

## Phase 2: Co-Founder Agreements (If Applicable)

**Goal:** Document co-founder equity, vesting, and IP ownership.

**Re-ground:** "We're setting up co-founder agreements. This is the uncomfortable conversation that prevents breakups. Document equity, vesting, and IP ownership now."

Use AskUserQuestion tool:

**SIMPLIFY:** "Equity split: How much does each founder own? Vesting: How long before they own it fully? (Standard: 4 years with 1-year cliff.) IP assignment: Who owns the code? (Answer: the company, not individuals.) This conversation is awkward. Do it now anyway."

**RECOMMEND:** "RECOMMENDATION: Document everything in writing. Handshakes break apart when money's involved.
- Completeness: 2/10 (no co-founder agreement)
- Completeness: 6/10 (verbal agreement, not written)
- Completeness: 10/10 (written agreement signed by all founders)"

**OPTIONS (if co-founders):**
- **(A)** "Equal founders, equal time, equal risk. 50/50 split, 4-year/1-year cliff vesting."
- **(B)** "Unequal split: One full-time, one part-time. [60/40]?"
- **(C)** "One founder has pre-existing audience/product. [Custom split]?"
- **(D)** "I'm not sure how to split. What would you recommend?"

**For co-founders, challenge:**
- Are both founders equally invested (time, money, risk)?
- Is vesting locked in? (Without vesting, early departure is risky for remaining founder)
- Is IP ownership clear? (Company should own all code)
- Does everyone understand that unvested equity is lost if they leave?

**For solo founders:**
- Skip this phase. Move to Phase 3 (Banking).

**Common vesting mistake:**
- 50/50 split without vesting → Founder B leaves month 2, still owns 50%. Nightmare.

**Correct approach:**
- 50/50 split WITH 4-year vesting, 1-year cliff.
- Founder B leaves month 2: owns 0% (still in cliff).
- Founder B leaves month 18: owns 25% (vested 18 months of 48).
- Founder B leaves month 48: owns 100% (fully vested).

**Exit criteria for Phase 2:** If co-founders, equity split, vesting schedule, and IP assignment documented and signed. Move to Phase 3 (Banking).

---

## Phase 3: Banking Setup

**Goal:** Set up a business bank account (non-negotiable).

**Re-ground:** "We're setting up a business bank account. This is non-negotiable for tax clarity and credibility."

Use AskUserQuestion tool:

**SIMPLIFY:** "You need a separate bank account for business money. Not your personal account. Keeps expenses clear, makes taxes easier, shows you're serious. Options: Traditional bank (slow), Stripe Treasury/Mercury (built for startups), or credit union."

**RECOMMEND:** "RECOMMENDATION: Startup-focused option (Mercury, Stripe Treasury) is fastest and has best UX.
- Completeness: 2/10 (no business account)
- Completeness: 6/10 (traditional bank, older tech)
- Completeness: 10/10 (startup bank, open, integrated accounting)"

**OPTIONS:**
- **(A)** "I'll use Mercury, Stripe Treasury, or similar (startup-focused)."
- **(B)** "I'll use traditional bank (Wells Fargo, Chase, etc.)."
- **(C)** "I don't have an account yet. I need to set one up."

**Requirements:**
- EIN (Employer Identification Number — free from IRS)
- Business license (automatic when you form entity)
- Articles of Incorporation/Organization
- ID

**Exit criteria for Phase 3:** Business bank account opened. Move to Phase 4 (Bookkeeping).

---

## Phase 4: Bookkeeping & Financial Tracking

**Goal:** Set up a system to track income and expenses.

**Re-ground:** "We're setting up bookkeeping. Track every dollar in/out. Saves headaches at tax time and when fundraising."

Use AskUserQuestion tool:

**SIMPLIFY:** "Income: every dollar coming in. Expenses: every dollar going out, category, business purpose. Receipts: save for 7 years. At MVP stage, you can DIY. Later you'll hire accountant, but they'll want clean records."

**RECOMMEND:** "RECOMMENDATION: Pick one tool and stick with it.
- Completeness: 2/10 (no system)
- Completeness: 6/10 (spreadsheet or basic tracking)
- Completeness: 10/10 (Wave/QB Online, integrated, clean)"

**OPTIONS:**
- **(A)** "Wave (free, good for MVP)."
- **(B)** "QuickBooks Online (~$30/month)."
- **(C)** "Spreadsheet (annoying but functional)."
- **(D)** "I don't have a system yet. I need to set one up."

**Exit criteria for Phase 4:** Bookkeeping tool chosen and set up. Move to Phase 5 (Tax Planning).

---

## Phase 5: Tax Planning

**Goal:** Understand your quarterly tax obligations.

**Re-ground:** "If you're making money, the IRS expects quarterly tax payments. Estimate now, avoid penalties later."

Use AskUserQuestion tool:

**SIMPLIFY:** "You pay estimated taxes 4x/year (April 15, June 15, Sept 15, Jan 15). Need to set aside ~25-30% of net income. If you don't have revenue yet, you can skip this. Once you do, get accountant to calculate your quarterly amount."

**RECOMMEND:** "RECOMMENDATION: Get advice from CPA. Costs $500 now, saves thousands in penalties.
- Completeness: 3/10 (no tax planning)
- Completeness: 6/10 (understand obligation, not calculating)
- Completeness: 10/10 (CPA confirmed quarterly amounts)"

**For state taxes:**
- Sales tax: Do you sell digital/physical products? Most states require collection.
- Payroll tax: Do you have employees (including yourself as W-2)?
- State income tax: What state are you in? (CA/NY tax, TX/FL don't)

**Exit criteria for Phase 5:** Tax obligations mapped and CPA consulted (if you have revenue). Move to Phase 6 (Insurance).

---

## Phase 6: Insurance

**Goal:** Get basic liability coverage.

**Re-ground:** "Do you need insurance? Probably basic general liability. Cheap ($400-1500/yr), gives credibility, protects against accidents."

Use AskUserQuestion tool:

**SIMPLIFY:** "General liability covers accidents/injuries on your property. Professional liability covers if your product causes damage. Cyber liability covers data breaches. At MVP stage, get basic general liability and revisit as you grow."

**RECOMMEND:** "RECOMMENDATION: Get general liability now. Revisit quarterly.
- Completeness: 2/10 (no insurance)
- Completeness: 6/10 (researched but not purchased)
- Completeness: 10/10 (general liability active)"

**OPTIONS:**
- **(A)** "I'll get general liability through online platform (fast, cheap)."
- **(B)** "I'll use broker for personalized advice."
- **(C)** "I'm not sure. Help me decide."
- **(D)** "I don't think I need it."

**Exit criteria for Phase 6:** General liability insurance obtained (or decision made to skip for now). Move to Phase 7 (Contractor Agreements).

---

## Phase 7: Contractor Agreements

**Goal:** Document agreements for any contractors/consultants.

**Re-ground:** "If you're hiring contractors (design, engineering, marketing), you need a written agreement. Protects IP ownership and clarifies scope."

Use AskUserQuestion tool:

**SIMPLIFY:** "Contractor agreement covers: scope of work, payment, timeline, IP ownership (company owns the work), confidentiality. Without it, contractor might own the code they wrote. Not OK."

**RECOMMEND:** "RECOMMENDATION: Use template ($20-100 from LawDepot/Rocket Lawyer) or get lawyer ($500-1500) for custom.
- Completeness: 2/10 (no contractors yet)
- Completeness: 6/10 (hiring contractors, no written agreement)
- Completeness: 10/10 (all contractors have signed agreements)"

**OPTIONS:**
- **(A)** "No contractors yet."
- **(B)** "I'm hiring contractors. I'll use template."
- **(C)** "I'm hiring contractors. I'll get custom agreement from lawyer."

**Exit criteria for Phase 7:** Contractor agreements in place (if applicable). Move to Phase 8 (Output).

---

## Phase 8: Output & Lock OPS-CHECKLIST.md

**Goal:** Generate comprehensive operations checklist.

I will produce **OPS-CHECKLIST.md** containing:

```markdown
# Operations Checklist

## Entity Structure
- [ ] Status: [Not Started / In Progress / Complete]
- [ ] Type: [LLC / C-Corp / Delaware C-Corp]
- [ ] Filing date: [YYYY-MM-DD]
- [ ] Next: [action needed]

## Co-Founder Agreements (if applicable)
- [ ] Status: [Not Started / In Progress / Complete]
- [ ] Equity split: [%]
- [ ] Vesting schedule: [4-year/1-year cliff / other]
- [ ] IP assignment: [Signed / Not signed]
- [ ] Next: [action needed]

## Banking
- [ ] Status: [Not Started / In Progress / Complete]
- [ ] Bank: [Mercury / QB / Traditional / etc]
- [ ] Account opened: [Date]
- [ ] Next: [Fund it / Set up transfers]

## Bookkeeping
- [ ] Status: [Not Started / In Progress / Complete]
- [ ] Tool: [Wave / QB Online / Spreadsheet]
- [ ] Set up: [Date]
- [ ] Next: [Start tracking expenses]

## Tax Planning
- [ ] Status: [Not Started / In Progress / Complete]
- [ ] CPA selected: [Yes / No]
- [ ] Quarterly amounts: [Calculated / TBD]
- [ ] Next: [Schedule with CPA]

## Insurance
- [ ] Status: [Not Started / In Progress / Complete]
- [ ] General liability: [Active / Not needed / TBD]
- [ ] Other coverage: [None yet]
- [ ] Next: [Purchase / Schedule review]

## Contractor Agreements
- [ ] Status: [Not Started / In Progress / Complete]
- [ ] Templates obtained: [Yes / No]
- [ ] Contracts signed: [# of contractors]
- [ ] Next: [Send to contractors / Prepare]

## Priority Actions
1. [Highest priority item]
2. [Second priority]
3. [Third priority]

## Notes
[Any blocking items or concerns]
```

---

## Escape Hatches

**If founder says "just do it" or expresses impatience:**
- Fast-track to artifact generation phase
- Use best available information to fill gaps
- Note any assumptions made

**If founder's answers cover multiple questions:**
- Smart-skip already-answered phases
- Acknowledge what was covered and move forward

---

## Phase 9: Completion & Handoff

**Completion status:** Once OPS-CHECKLIST.md is saved, the skill is complete.

---

## Completion Status

**DONE** — OPS-CHECKLIST.md written and saved.
**DONE_WITH_CONCERNS** — Checklist written but gaps flagged for later review.
**BLOCKED** — Cannot proceed; missing legal advice or co-founder decisions.
**NEEDS_CONTEXT** — Need additional information from founder before completing.

**Next Step:** Proceed to runway-calculator.
Return to z-combinator orchestrator for routing.

---

## Key Principle

**Don't skip this.** Most technical founders do. They regret it at funding time or during co-founder disputes. Do it now when it's simple.
