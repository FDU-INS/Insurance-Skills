---
title: "Privacy-preserving KYC and sanctions screening proofs"
domains: business-operations, government
---

## Problem

Every financial institution that onboards the same customer independently collects and stores the same identity documents, running redundant KYC checks that cost $50–500 per customer — while creating dozens of copies of sensitive identity data across institutions that each become breach targets. Cross-border transactions compound the problem: a European bank processing a payment to a US correspondent must demonstrate OFAC and EU sanctions compliance, which currently requires sharing enough customer data for the counterparty to independently screen — forcing a choice between privacy and compliance.

## Solution

Zero-knowledge proofs that let institutions demonstrate a customer passed KYC and sanctions screening — proving the fact of compliance without sharing the underlying identity documents, so counterparties can satisfy their regulatory obligations without receiving (and storing) sensitive data they didn't need.

## Why Ethereum

Verifiability: ZK proofs confirm compliance status cryptographically — counterparties verify that screening was performed without receiving the underlying identity data, reducing breach surface while satisfying correspondent banking compliance requirements.
