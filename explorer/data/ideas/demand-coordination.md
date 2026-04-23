---
title: "DER aggregation and behind-the-meter market participation"
domains: utilities
---

## Problem

FERC Order 2222 requires ISOs/RTOs to let distributed energy resources — residential batteries, smart thermostats, EV chargers, water heaters — participate in wholesale energy markets through aggregators. But the settlement infrastructure doesn't exist: aggregators have no scalable way to meter, verify, and compensate individual behind-the-meter assets for the load flexibility they provide, because each device is on a different protocol and the minimum transaction size in wholesale markets makes sub-kWh contributions uneconomic to settle individually.

## Solution

A settlement layer for DER aggregation that meters individual device contributions, verifies demand reductions against smart meter baselines, and distributes compensation to device owners automatically — making it economically viable for aggregators to orchestrate millions of small assets into wholesale market participation.

## Why Ethereum

Enforcement: compensation for individual device contributions executes automatically when metered demand reductions are confirmed — enabling aggregators to settle millions of micro-transactions that would be uneconomic through traditional payment infrastructure.

## Resources

- [Glow](https://glow.org/) - A decentralized protocol designed to subsidize the production of carbon-neutral solar energy by replacing traditional carbon credits with a system of economic incentives for solar farms
- [Daylight](https://godaylight.com/) - A decentralized energy marketplace that allows individuals and businesses to buy and sell renewable energy directly from each other
- [Blockchain-based prosumer incentivization for peak mitigation through temporal aggregation and contextual clustering](https://www.sciencedirect.com/science/article/pii/S2096720921000117) - Incentivizing prosumers to shift energy use and flatten peak demand
- [Resilient design of distribution grid automation system against cyber-physical attacks using blockchain and smart contract](https://www.sciencedirect.com/science/article/pii/S2096720921000051) - Proposes a solution to keep grid automation functions operational even if central controllers are compromised
- [Blockchain-enhanced hydrogen fuel production and distribution for sustainable energy management](https://www.sciencedirect.com/science/article/pii/S2096720924000423) - Presents a tokenized system using ERC-1155 to track, trade, and govern renewable hydrogen fuel production and distribution
