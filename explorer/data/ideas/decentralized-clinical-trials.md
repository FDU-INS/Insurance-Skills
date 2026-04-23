---
title: "Tamper-evident data integrity for decentralized clinical trials"
domains: health, science
---

## Problem

Decentralized clinical trials (DCTs) — where patients participate from home using wearables, ePRO apps, and telemedicine — are growing rapidly but face a data integrity challenge that traditional site-based trials don't: when data is collected on patient devices across hundreds of locations rather than at monitored investigator sites, sponsors and regulators have weaker assurance that electronic source data hasn't been altered, that consent was properly obtained, or that the chain of custody from device to database is intact. FDA's 2023 DCT guidance specifically calls out electronic source data integrity as a key concern.

## Solution

Cryptographic attestation of clinical trial data at the point of collection — patient-reported outcomes, wearable sensor readings, and eConsent signatures are hashed and timestamped on an immutable ledger at the moment of capture, creating an audit trail that satisfies 21 CFR Part 11 requirements and gives monitors, sponsors, and regulators confidence in source data integrity without requiring physical site visits.

## Why Ethereum

Verifiability: trial data is cryptographically committed at the point of collection — monitors and regulators can verify source data integrity without physical site visits, satisfying the data provenance requirements that make regulators hesitant to approve decentralized trial designs.

## Resources

- [Molecule](https://molecule.xyz/) - Crowdfunded biopharma protocol with milestone-based governance
- [Genomes](https://www.genomes.io/) - Platform for safe, private & auditable monetization of genomic data
- [OriginTrail](https://origintrail.io/) - Decentralized Knowledge Graph for medical data, counterfeit prevention, and medicine traceability
- [AminoChain](https://aminochain.io/) - Community-owned and decentralized biobank that streamlines biosample procurement
- [Recerts](https://www.recerts.org/) - Tokenized impact certificates for retroactive recognition of research contributions
- [OpenSci](https://www.opensci.io/) - Empowers scientists to own ideas from inception, permanently track contributions, and automatically receive returns
- [Blockchain and Healthcare: A Critical Analysis of Progress and Challenges in the Last Five Years](https://www.mdpi.com/2813-5288/1/2/6)
- [Verifiable Badging System for Scientific Data Reproducibility](https://www.sciencedirect.com/science/article/pii/S2096720921000105) - Layered approach to data sharing and proofs of research quality
- [The case of Hyperledger Fabric as a blockchain solution for healthcare applications](https://www.sciencedirect.com/science/article/pii/S2096720921000075) - Evaluates private blockchains for health data privacy, security, and compliance
- [Privacy-preserving pathological data sharing](https://www.sciencedirect.com/science/article/pii/S2096720924000174) - Uses re-encryption techniques for secure multi-party pathology data exchange
- [Blockchain-based Healthcare Information Exchange System](https://www.sciencedirect.com/science/article/pii/S2096720924000617) - Hybrid blockchain + ontology system enabling secure, cross-institutional patient data exchange
- [Exploring the decentralized science ecosystem](https://www.frontiersin.org/journals/blockchain/articles/10.3389/fbloc.2025.1524222/full) - Insights on organizational structures, technologies, and funding in DeSci
