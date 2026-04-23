---
name: insurance-product-review
description: Review the insurance product design, payout terms, and pricing assumptions for viability and profitability. Use when critiquing thesis, economics, risk controls, underwriting assumptions, premium strategy, and solvency posture of this vehicle insurance protocol.
---

# Insurance Product Review

Use this workflow to critique the protocol as an insurance product, not only as code.

## Review lens

Evaluate:

1. Profitability (expected premium vs expected losses)
2. Solvency and liquidity stress risk
3. Adverse selection and moral hazard exposure
4. Trigger design and basis risk
5. Operability (claims fairness, disputes, reserve policy)

## Repository context

Start from:

1. `requirements.md`
2. `README.md`
3. `policy-engine/README.md`
4. `policy-engine/contracts/src/PolicyManager.sol`
5. `vault/contracts/src/InsuranceVault.sol`

Current assumptions to challenge:

1. Flat payout equals `coverageUSDC`.
2. Tier-based premium bps model.
3. Coverage caps at absolute max and percent of entry value.
4. Trigger based on a single oracle condition around floor price.

## Required analysis steps

1. Build a simple unit-economics table for each floor tier.
2. Estimate loss ratio sensitivity under mild, base, and stressed price-drop scenarios.
3. Check whether premium schedule compensates for jump-risk and correlation risk.
4. Check reserve adequacy and liquidity timing under clustered claims.
5. Highlight where product terms can be gamed by informed buyers.
6. Propose contract-level guardrails that improve risk control.

## Practical critique checklist

1. Does premium scale with volatility and policy duration, or stay static?
2. Is there a waiting period or anti-gaming mechanism before claims can trigger?
3. Are confidence and sample-size signals used to gate low-quality oracle reports?
4. Are max payout and total exposure caps enforced per feed and globally?
5. Is there a reserve ratio target and underfunded-vault handling path?
6. Is there reinsurance-like logic or a circuit breaker for extreme events?

## Output contract

Return:

1. `Economic risks` with quantified directionality where possible.
2. `Top 5 product changes` ranked by impact and implementation effort.
3. `Contract implications` mapping each recommendation to Solidity/workflow updates.
4. `Go or no-go` for demo, pilot, and production-readiness stages.
