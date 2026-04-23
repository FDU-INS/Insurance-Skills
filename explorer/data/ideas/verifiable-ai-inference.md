---
title: "Verifiable AI inference"
domains: ai
---

## Problem

Users receiving AI-generated outputs have no way to independently verify which model, version, or weights produced a given result, making it impossible to hold providers accountable for hallucinations or manipulation.

## Solution

Onchain proofs that a specific model produced a specific output, enabling accountability and auditability

## Why Ethereum

Verifiability: cryptographic proofs allow anyone to confirm which model version produced a given output, creating an auditable trail that holds providers accountable for hallucinations or manipulation.

## Resources

- [Giza](https://www.gizatech.xyz/) - Lets smart contracts use ML models (like price predictors or risk engines) with cryptographic proof that the model actually ran correctly, so DeFi apps can trust AI outputs without trusting the operator
- [EZKL](https://ezkl.xyz/) - Enables you to prove you ran a specific model on specific data
- [x402](https://www.x402.org/) - Uses the HTTP 402 status code to let servers charge for API calls or content via on-chain stablecoin payments, so AI agents and humans can pay per request without accounts or API keys
- [The Rise of Onchain AI: Agents, Apps, and Commerce](https://paragraph.com/@cbventures/the-rise-of-onchain-ai-agents-apps-and-commerce)
