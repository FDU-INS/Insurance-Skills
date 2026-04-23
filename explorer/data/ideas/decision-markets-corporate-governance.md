---
title: "Decision markets for corporate governance"
domains: business-operations
---

## Problem

Corporate decisions — which strategy to pursue, whether to hire or fire an executive, which product to prioritize — are made through a combination of politics, hierarchy, and intuition rather than mechanisms that aggregate genuine beliefs of those closest to the work. Board votes and management sign-off concentrate decision-making power in ways that reward confidence and seniority over accuracy, with no feedback loop that punishes bad predictions or rewards good ones. Organizations systematically act on what's good for those in power rather than what's good for the organization.

## Solution

Conditional prediction markets tied to company-specific metrics — share price, TVL, revenue, retention — where any proposal generates two parallel markets: expected metric outcome if it passes, and if it fails. The proposal executes if markets predict a positive impact. Participants with genuine information have financial incentive to trade accurately. Early implementations include Butter Markets (used in Optimism's grant allocation experiments) and MetaDAO, which has run 96+ proposals for 14 organizations using this mechanism.

## Why Ethereum

Enforcement: conditional markets execute and settle via smart contract, making the link between market signal and organizational decision a protocol property rather than management discretion. Composability: the same decision market infrastructure can be referenced by any organization's governance without rebuilding from scratch.

## Resources

- [Butter](https://butter.markets/) - Decision markets for onchain governance

## Examples

- [Aragon](https://aragon.org/) - Organizational governance and operations toolkit
