# Liquidation DoS Security Checklist

Verify each item before finalizing audit report:

- [ ] **No unbounded loops:** Liquidation doesn't iterate over user-controlled arrays without max bounds
- [ ] **Data structure integrity:** EnumerableSet/mapping operations safe during liquidation
- [ ] **Front-run resistance:** Liquidation doesn't depend on exact state user can modify
- [ ] **Pending actions:** Withdrawals/deposits don't block liquidation transfers
- [ ] **Callback isolation:** Token callbacks cannot revert liquidation (use low-level calls or checks)
- [ ] **All collateral seized:** Checks both protocol and external vault collateral
- [ ] **Graceful bad debt:** Liquidation works even when bad debt exceeds insurance fund
- [ ] **Dynamic bonus:** Liquidation bonus capped at available collateral, no fixed assumptions
- [ ] **Decimal handling:** Correct conversions for all token decimals (6, 8, 18)
- [ ] **No reentrancy conflicts:** Single nonReentrant in liquidation path or proper guard placement
- [ ] **Zero transfer checks:** Skip transfers when amount == 0 for strict tokens
- [ ] **Deny list handling:** Liquidation routes through protocol, not directly to blacklisted addresses
- [ ] **Edge case validation:** Works with single borrower, zero positions, etc.
