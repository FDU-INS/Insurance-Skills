---
name: israeli-bituach-leumi
description: Navigate Israeli National Insurance (Bituach Leumi) benefits, eligibility, and contributions. Use when user asks about "bituach leumi", national insurance, retirement pension (kiztavat zikna), unemployment (dmei avtala), maternity leave (dmei leida), child allowance (kiztavat yeladim), disability benefits, work injury, reserve duty compensation, or NI contributions. Covers all 15+ Bituach Leumi programs. Do NOT use for private insurance or health fund (kupat cholim) questions.
license: MIT
allowed-tools: Bash(python:*)
compatibility: No network required. Works with Claude Code, Claude.ai, Cursor.
---

# Israeli Bituach Leumi (National Insurance)

## Critical Note
Bituach Leumi rules are complex and change frequently. Always recommend users verify
specific eligibility at btl.gov.il or call *6050 for definitive answers. This skill
provides general guidance based on published rules.

## Instructions

### Step 1: Identify the Benefit Program
Ask what the user needs help with and map to the correct program.

### Step 2: Check Eligibility
Each program has specific conditions. Key factors:
- Residency status
- Age
- Employment history (qualifying period)
- Income level
- Medical condition (for disability)
- Marital/family status

### Step 3: Estimate Benefit Amount
Provide calculation methodology per program. Note that amounts update periodically.

### Step 4: Guide Claims Process
For each benefit:
1. Required documents
2. Submission method (online/mail/in-person)
3. Processing time
4. Appeal process if denied

## Key Programs Detail

### Old Age Pension (Kiztavat Zikna)
- **Eligibility age:** Men 67, Women 65 (the gradual increase from 62 to 65 was completed in 2017)
- **Qualifying period:** 60-144 months of contributions (varies by age at immigration)
- **Basic amount (as of 2026):** ~1,810 NIS/month (single), ~2,730 NIS/month (couple). These are approximate figures; check btl.gov.il for current rates.
- **Income supplement:** Additional if below income threshold
- **Deferral bonus:** +5% per year of deferred claiming after eligibility age

### Unemployment (Dmei Avtala)
- **Eligibility:** Employed 12+ months in last 18 months, terminated (not resigned)
- **Waiting period:** 5 days
- **Duration:** 50-175 days depending on age and dependents
- **Amount:** Based on average of last 6 months salary, capped at ~70% of average wage

### Maternity (Dmei Leida)
- **Eligibility:** 10-15 months of employment in last 14-22 months
- **Duration:** 15 weeks (employed 10+ months) or 8 weeks (6+ months)
- **Amount:** Full salary replacement up to maximum insurable income
- **Father:** 1 week minimum, option to split remaining weeks

### Child Allowance (Kiztavat Yeladim)
- **Eligibility:** All Israeli residents with children under 18
- **Amounts (as of 2026):** ~170 NIS/child/month (varies by number of children, child's birth year)
- **Payment:** Monthly, automatic to registered parent

## Examples

### Example 1: Maternity Leave
User says: "I'm pregnant and want to know about maternity leave benefits"
Result: Explain eligibility based on employment duration, 15-week leave, salary replacement, partner's leave rights, how to file claim.

### Example 2: Retirement Planning
User says: "When can I start getting pension from Bituach Leumi?"
Result: Explain eligibility age, qualifying period, basic amount, supplements, deferral bonus.

### Example 3: Reserve Duty Compensation
User says: "I did 30 days of miluim, how much will Bituach Leumi pay me?"
Actions:
1. Determine eligibility for reserve duty compensation (tashlumeimimluim)
2. Calculate based on salary history and qualifying days
3. Explain employer vs. Bituach Leumi payment split
Result: Estimated compensation amount with explanation of the payment process and timeline.

## Bundled Resources

### Scripts
- `scripts/calculate_benefits.py` — Estimate Bituach Leumi benefit amounts for old age pension (kiztavat zikna), unemployment (dmei avtala), maternity leave (dmei leida), and child allowance (kiztavat yeladim) based on user-provided parameters like age, salary, and employment history. Supports subcommands: `pension`, `unemployment`, `maternity`, `child-allowance`. Run: `python scripts/calculate_benefits.py --help`

### References
- `references/benefit-programs.md` — Quick-reference table of all 13+ Bituach Leumi programs with Hebrew names, eligibility summaries, contact information (*6050, btl.gov.il), and key dates for rate updates and payment schedules. Consult when identifying which benefit program applies to a user's situation.

## Gotchas
- Bituach Leumi (National Insurance) contribution rates have two tiers: a reduced rate on income up to 60% of the average wage, and a normal rate above it. Agents almost always apply a single flat rate.
- Self-employed individuals pay both the employee and a portion of the employer Bituach Leumi contributions. Agents may calculate only the employee share, underestimating the total obligation.
- Bituach Leumi benefits (disability, old-age, maternity) have waiting periods and eligibility requirements. Agents may tell users they are immediately eligible when there are qualification periods.
- The average wage (sachir memutza) used for Bituach Leumi calculations is updated twice a year by the CBS. Agents may use an outdated figure. Check the current value at btl.gov.il.

## Troubleshooting

### Error: "Not enough qualifying months"
Cause: Insufficient contribution history
Solution: Check if any periods (military service, maternity leave) count as qualifying months. New immigrants have special rules.

### Error: "Benefit amounts don't match expected values"
Cause: Bituach Leumi updates benefit amounts periodically, often tied to the national average wage
Solution: Verify current amounts at btl.gov.il or call *6050. Amounts in this skill reflect published rates as of 2026 -- check for annual updates each January.

### Error: "Eligibility period not met"
Cause: Most benefits require a qualifying period of NI contributions (e.g., 10 months for maternity, 12 months for unemployment)
Solution: Check the specific qualifying period for each benefit. Partial periods may qualify for reduced benefits. New immigrants (olim) may have special eligibility rules.