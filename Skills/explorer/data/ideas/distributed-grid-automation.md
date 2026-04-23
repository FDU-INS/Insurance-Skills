---
title: "Grid-edge device coordination and tamper-evident event logging"
domains: utilities
---

## Problem

Distribution utilities adding thousands of DERs, smart inverters, and storage systems to the grid edge have no unified view of device state or energy flows below the substation level — SCADA systems designed for centralized generation don't extend to the grid edge, and the growing attack surface of connected devices makes it critical to maintain tamper-evident records of device commands and state changes for NERC CIP compliance and incident forensics.

## Solution

An append-only event log for grid-edge device actions — recording commands, state changes, and energy flow measurements with cryptographic attestation — giving distribution operators and regulators a tamper-evident audit trail at the grid edge where SCADA visibility currently ends.

## Why Ethereum

Verifiability: device actions and energy flow data are cryptographically logged — giving distribution operators an audit trail below the substation level that SCADA systems don't provide, and making unauthorized device commands forensically detectable.

## Resources

- [Glow](https://glow.org/) - A decentralized protocol designed to subsidize the production of carbon-neutral solar energy by replacing traditional carbon credits with a system of economic incentives for solar farms
- [Daylight](https://godaylight.com/) - A decentralized energy marketplace that allows individuals and businesses to buy and sell renewable energy directly from each other
- [Resilient design of distribution grid automation system against cyber-physical attacks using blockchain and smart contract](https://www.sciencedirect.com/science/article/pii/S2096720921000051) - Proposes a solution to keep grid automation functions operational even if central controllers are compromised
- [What blockchain can do for power grids?](https://www.sciencedirect.com/science/article/pii/S2096720921000038) - Review and classification of blockchain applications across energy and power grid domains
- [Integrating big data and blockchain to manage energy smart grids—TOTEM framework](https://www.sciencedirect.com/science/article/pii/S2096720922000227) - Privacy-preserving data hub combining blockchain and machine learning for prosumer energy trading and smart grid management
- [Blockchain-enhanced hydrogen fuel production and distribution for sustainable energy management](https://www.sciencedirect.com/science/article/pii/S2096720924000423) - Presents a tokenized system using ERC-1155 to track, trade, and govern renewable hydrogen fuel production and distribution
