# Liquidation Denial of Service Vulnerability Patterns

## Pattern #1: Many Small Positions DoS
**Risk:** Iterating over unbounded user positions array causes out-of-gas revert, preventing liquidation
**Detection:** Look for loops over user-controlled arrays without bounds: `for (uint i = 0; i < positions.length; i++)`
**Impact:** Attacker creates many small positions, liquidation runs out of gas, positions remain underwater

## Pattern #2: Multiple Positions Corruption
**Risk:** EnumerableSet ordering corruption when positions removed during iteration prevents liquidation
**Detection:** Check if EnumerableSet.remove() called during iteration or if ordering matters
**Impact:** Data structure corruption causes reverts, specific positions become unliquidatable

## Pattern #3: Front-Run Prevention
**Risk:** Users change nonce or perform small self-liquidation to invalidate liquidator's transaction
**Detection:** Check if liquidation depends on exact state that user can modify (nonces, amounts)
**Impact:** Borrowers front-run liquidators to avoid full liquidation, extend underwater positions

## Pattern #4: Pending Action Prevention
**Risk:** Pending withdrawals equal to balance force liquidation reverts on transfer
**Detection:** Look for: `require(balance >= amount)` where pending withdrawals reduce available balance
**Impact:** Users can queue withdrawals to make liquidation revert, remain unliquidatable

## Pattern #5: Malicious Callback Prevention
**Risk:** onERC721Received or ERC20 hooks revert during collateral seizure, blocking liquidation
**Detection:** Check if liquidation transfers tokens to user-controlled contracts with callbacks
**Impact:** Malicious borrowers prevent liquidation via reverting callbacks

## Pattern #6: Yield Vault Collateral Hiding
**Risk:** Collateral deposited in external vaults not seized during liquidation
**Detection:** Verify liquidation checks all collateral locations (protocol + external vaults)
**Impact:** Borrowers hide collateral in vaults, appear liquidatable but collateral not seized

## Pattern #7: Insurance Fund Insufficient
**Risk:** Bad debt exceeding insurance fund causes liquidation revert instead of graceful handling
**Detection:** Look for: `require(insuranceFund >= badDebt)` without fallback
**Impact:** Insolvent positions cannot be liquidated, bad debt accumulates

## Pattern #8: Fixed Bonus Insufficient Collateral
**Risk:** Fixed 110% liquidation bonus fails when collateral ratio < 110%, causing revert
**Detection:** Check if bonus calculation can exceed available collateral: `bonus = debt * 1.1`
**Impact:** Underwater positions with low collateral ratios become unliquidatable

## Pattern #9: Non-18 Decimal Reverts
**Risk:** Incorrect decimal handling causes underflow/overflow during liquidation with non-standard tokens
**Detection:** Look for hardcoded 1e18 assumptions or missing decimal conversions
**Impact:** Liquidation reverts for tokens with != 18 decimals (USDC 6, WBTC 8)

## Pattern #10: Multiple nonReentrant Modifiers
**Risk:** Complex liquidation paths hit multiple nonReentrant guards, causing "ReentrancyGuard: reentrant call" revert
**Detection:** Trace liquidation path for multiple functions with nonReentrant modifier
**Impact:** Legitimate liquidation reverts due to reentrancy guard conflicts

## Pattern #11: Zero Value Transfer Reverts
**Risk:** Missing zero checks with tokens that revert on zero transfer (some ERC20s)
**Detection:** Look for transfers without: `if (amount > 0)` check
**Impact:** Edge cases with zero amounts cause liquidation to revert

## Pattern #12: Token Deny List Reverts
**Risk:** USDC-style blocklists prevent liquidation token transfers when borrower blacklisted
**Detection:** Check if liquidation transfers tokens to/from borrower address
**Impact:** Blacklisted borrowers cannot be liquidated, positions remain underwater

## Pattern #13: Single Borrower Edge Case
**Risk:** Protocol incorrectly assumes > 1 borrower, liquidation fails with single borrower
**Detection:** Look for calculations like: `share = debt / (totalBorrowers - 1)`
**Impact:** Division by zero or incorrect calculations when only one borrower exists
