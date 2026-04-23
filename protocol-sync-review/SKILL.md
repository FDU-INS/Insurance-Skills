---
name: protocol-sync-review
description: Review this monorepo for cross-package consistency, interface compatibility, event stability, and configuration alignment. Use when validating that oracle, insurance consumer, policy engine, vault, workflows, and frontend remain synchronized.
---

# Protocol Sync Review

Use this workflow to catch integration drift before runtime failures.

## Primary objective

Detect mismatches between:

1. Solidity interfaces and implementations
2. Event names, field order, and indexed fields
3. Decimal and unit assumptions (`priceUsdE8`, USDC e6, wei)
4. Feed key hashing conventions
5. Workflow/frontend expectations versus on-chain APIs

## Review targets

1. `requirements.md`
2. `README.md`
3. `policy-engine/contracts/src`
4. `vault/contracts/src`
5. `chainlink-cre-car-price-oracle/contracts/src`
6. `chainlink-cre-car-value-insurance/contracts/src`
7. `chainlink-cre-car-price-oracle/car-price-oracle-workflow`
8. `chainlink-cre-car-value-insurance/insurance-workflow`
9. `frontend`

## Locked protocol assumptions

Treat these as stable until the team intentionally revises the spec:

1. `feedKeyHash = keccak256(bytes(feedKeyString))`
2. Oracle struct shape:
3. `priceUsdE8 uint128`
4. `sampleSize uint32`
5. `confidenceBps uint32`
6. `updatedAt uint64`
7. `sourceHash bytes32`
8. `PolicyPurchased` and `PolicyClaimed` event names and argument order.
9. Policy identifier rule: `tokenId == policyId`.
10. Policy manager API shape:
11. `buyPolicy(bytes32,uint128,uint256,uint64)`
12. `triggerPayout(uint256)`
13. `getPolicy(uint256)`
14. `isActive(uint256)`

## Drift checks

1. Flag interface signature mismatches between contracts and interfaces.
2. Flag payout semantic mismatches across docs/contracts/tests.
3. Flag ETH-versus-USDC assumption mismatches.
4. Flag event type or ordering drift from locked spec.
5. Flag stale addresses, wrong chain targets, or missing config linkage.

## Output contract

Return:

1. `Critical integration breaks` (causes failed tx or invalid runtime behavior).
2. `Spec drift` (not yet broken but no longer aligned).
3. `Decision-needed items` requiring team alignment.
4. `Patch plan` with exact files to change.
