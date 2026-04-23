---
title: "Cross-network EV charging roaming settlement"
domains: utilities
---

## Problem

When an EV driver charges on a network other than their home provider, the roaming transaction passes through bilateral settlement agreements between the charge point operator (CPO) and the eMobility service provider (eMSP) — each pair requiring a custom integration. In Europe alone there are 500+ CPOs and dozens of eMSPs, and the bilateral model means most roaming pairs simply don't exist, leaving drivers unable to charge on large portions of the network without creating new accounts.

## Solution

A shared settlement layer where any CPO and any eMSP can clear roaming transactions without bilateral agreements — using standardized session records (kWh delivered, time, location, tariff) that both parties confirm onchain, with payment executing automatically at session close.

## Why Ethereum

Composability: a shared settlement layer means any CPO-eMSP pair can transact without a pre-negotiated bilateral integration — roaming coverage expands from bilateral partnerships to the entire network by default.

## Resources

- [DIMO](https://dimo.co/) - Vehicle data sharing network enabling fleet telemetry and provenance
- [Blockchain-enabled secure and authentic Nash equilibrium strategies for heterogeneous networked hub of electric vehicle charging stations](https://www.sciencedirect.com/science/article/pii/S2096720924000368) - Cross-chain EV-charging market hub research
- [Blockchain-enabled decentralized identity management: The case of self-sovereign identity in public transportation](https://www.sciencedirect.com/science/article/pii/S2096720921000099) - Proposes SSI-based interoperable transit credentials across operators
