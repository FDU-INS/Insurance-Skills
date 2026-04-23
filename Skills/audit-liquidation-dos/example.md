# Liquidation DoS Vulnerability Examples

## Pattern #1: Many Small Positions DoS

### VULNERABLE
```solidity
contract VulnerableUnboundedLoop {
    struct Position {
        uint256 collateral;
        uint256 debt;
    }

    mapping(address => Position[]) public userPositions;

    // ISSUE: Unbounded loop over user positions
    function liquidate(address user) external {
        Position[] storage positions = userPositions[user];

        // Attacker creates 10,000 small positions
        // Loop consumes 30M+ gas, exceeds block limit
        for (uint i = 0; i < positions.length; i++) {
            if (isLiquidatable(positions[i])) {
                // Liquidate position
                seizeCollateral(user, i);
            }
        }
    }
}
```

### FIXED
```solidity
contract FixedBoundedLoop {
    uint256 public constant MAX_POSITIONS = 50;

    struct Position {
        uint256 collateral;
        uint256 debt;
    }

    mapping(address => Position[]) public userPositions;

    function liquidate(address user, uint256 positionId) external {
        // Liquidate single position by ID - O(1)
        require(positionId < userPositions[user].length, "Invalid position");
        Position storage pos = userPositions[user][positionId];

        require(isLiquidatable(pos), "Not liquidatable");
        seizeCollateral(user, positionId);
    }

    function createPosition(uint256 collateral, uint256 debt) external {
        require(
            userPositions[msg.sender].length < MAX_POSITIONS,
            "Max positions reached"
        );
        userPositions[msg.sender].push(Position(collateral, debt));
    }
}
```

## Pattern #2: Multiple Positions Corruption

### VULNERABLE
```solidity
contract VulnerableEnumerableSet {
    using EnumerableSet for EnumerableSet.UintSet;

    mapping(address => EnumerableSet.UintSet) private userPositionIds;
    mapping(uint256 => Position) public positions;

    // ISSUE: Removing from EnumerableSet during iteration corrupts ordering
    function liquidateAll(address user) external {
        EnumerableSet.UintSet storage posIds = userPositionIds[user];

        for (uint i = 0; i < posIds.length(); i++) {
            uint256 posId = posIds.at(i);

            if (isLiquidatable(positions[posId])) {
                // Remove corrupts iteration - skips positions
                posIds.remove(posId);
                delete positions[posId];
            }
        }
    }
}
```

### FIXED
```solidity
contract FixedEnumerableSet {
    using EnumerableSet for EnumerableSet.UintSet;

    mapping(address => EnumerableSet.UintSet) private userPositionIds;
    mapping(uint256 => Position) public positions;

    function liquidate(address user, uint256 posId) external {
        require(userPositionIds[user].contains(posId), "Invalid position");
        require(isLiquidatable(positions[posId]), "Not liquidatable");

        // Single position removal - no iteration corruption
        userPositionIds[user].remove(posId);
        delete positions[posId];
    }

    // Alternative: iterate backwards for batch operations
    function liquidateAllSafe(address user) external {
        EnumerableSet.UintSet storage posIds = userPositionIds[user];
        uint256 length = posIds.length();

        // Iterate backwards to avoid index shift issues
        for (uint i = length; i > 0; i--) {
            uint256 posId = posIds.at(i - 1);
            if (isLiquidatable(positions[posId])) {
                posIds.remove(posId);
                delete positions[posId];
            }
        }
    }
}
```

## Pattern #3: Front-Run Prevention

### VULNERABLE
```solidity
contract VulnerableFrontRun {
    mapping(address => uint256) public nonces;
    mapping(address => Position) public positions;

    // ISSUE: Liquidation depends on nonce user can change
    function liquidate(address user, uint256 nonce) external {
        require(nonces[user] == nonce, "Invalid nonce");

        // User sees liquidation in mempool
        // Front-runs with any transaction to increment nonce
        // Liquidation reverts with "Invalid nonce"

        nonces[user]++;
        seizeCollateral(user);
    }
}
```

### FIXED
```solidity
contract FixedNoNonceDependency {
    mapping(address => Position) public positions;

    function liquidate(address user) external {
        // No nonce dependency - cannot be front-run
        Position memory pos = positions[user];
        require(isLiquidatable(pos), "Not liquidatable");

        seizeCollateral(user);
        delete positions[user];
    }
}
```

## Pattern #4: Pending Action Prevention

### VULNERABLE
```solidity
contract VulnerablePendingWithdrawal {
    mapping(address => uint256) public collateral;
    mapping(address => uint256) public pendingWithdrawals;

    function liquidate(address user) external {
        uint256 userCollateral = collateral[user];

        // ISSUE: Transfer fails when pendingWithdrawals == collateral
        // User queues withdrawal equal to collateral
        // Available: collateral - pendingWithdrawals = 0
        require(
            userCollateral - pendingWithdrawals[user] > 0,
            "Insufficient available collateral"
        );

        // Revert - user has pending withdrawal
    }
}
```

### FIXED
```solidity
contract FixedPendingWithdrawal {
    mapping(address => uint256) public collateral;
    mapping(address => uint256) public pendingWithdrawals;

    function liquidate(address user) external {
        uint256 userCollateral = collateral[user];

        // Liquidation cancels pending withdrawals
        delete pendingWithdrawals[user];

        // Seize full collateral regardless of pending actions
        token.transfer(msg.sender, userCollateral);
        delete collateral[user];
    }
}
```

## Pattern #5: Malicious Callback Prevention

### VULNERABLE
```solidity
contract VulnerableMaliciousCallback {
    function liquidate(address user) external {
        Position memory pos = positions[user];

        // ISSUE: Transfer triggers onERC721Received on user contract
        // Malicious borrower reverts in callback
        collateralNFT.safeTransferFrom(address(this), msg.sender, pos.tokenId);

        // Never reaches here - revert in callback prevents liquidation
        delete positions[user];
    }
}
```

### FIXED
```solidity
contract FixedCallbackIsolation {
    function liquidate(address user) external {
        Position memory pos = positions[user];

        // Use transferFrom instead of safeTransferFrom - no callbacks
        collateralNFT.transferFrom(address(this), msg.sender, pos.tokenId);

        delete positions[user];
    }

    // Alternative: low-level call with ignore revert
    function liquidateWithTryCatch(address user) external {
        Position memory pos = positions[user];

        try collateralNFT.safeTransferFrom(
            address(this),
            msg.sender,
            pos.tokenId
        ) {
            // Success path
        } catch {
            // Callback reverted, use transferFrom
            collateralNFT.transferFrom(address(this), msg.sender, pos.tokenId);
        }

        delete positions[user];
    }
}
```

## Pattern #6: Yield Vault Collateral Hiding

### VULNERABLE
```solidity
contract VulnerableVaultCollateral {
    mapping(address => uint256) public collateralInProtocol;
    IVault public vault;

    function liquidate(address user) external {
        // ISSUE: Only checks collateral in protocol
        uint256 seizable = collateralInProtocol[user];

        // User has 100 ETH in vault.balanceOf(user)
        // Protocol only seizes collateralInProtocol[user] = 0
        // Actual collateral not seized

        token.transfer(msg.sender, seizable);
    }
}
```

### FIXED
```solidity
contract FixedVaultCollateral {
    mapping(address => uint256) public collateralInProtocol;
    IVault public vault;

    function liquidate(address user) external {
        // Check all collateral locations
        uint256 protocolCollateral = collateralInProtocol[user];
        uint256 vaultCollateral = vault.balanceOf(user);
        uint256 totalCollateral = protocolCollateral + vaultCollateral;

        // Seize from both locations
        if (protocolCollateral > 0) {
            token.transfer(msg.sender, protocolCollateral);
        }

        if (vaultCollateral > 0) {
            vault.seizeCollateral(user, msg.sender, vaultCollateral);
        }

        delete collateralInProtocol[user];
    }
}
```

## Pattern #7: Insurance Fund Insufficient

### VULNERABLE
```solidity
contract VulnerableInsuranceFund {
    uint256 public insuranceFund;

    function liquidate(address user) external {
        Position memory pos = positions[user];
        uint256 badDebt = pos.debt > pos.collateral ? pos.debt - pos.collateral : 0;

        // ISSUE: Revert when bad debt exceeds fund
        require(insuranceFund >= badDebt, "Insufficient insurance fund");

        // Position cannot be liquidated until fund replenished
        // Bad debt accumulates
    }
}
```

### FIXED
```solidity
contract FixedInsuranceFund {
    uint256 public insuranceFund;
    uint256 public unrecoverableBadDebt;

    function liquidate(address user) external {
        Position memory pos = positions[user];

        if (pos.debt > pos.collateral) {
            uint256 badDebt = pos.debt - pos.collateral;

            if (insuranceFund >= badDebt) {
                // Cover from insurance fund
                insuranceFund -= badDebt;
            } else {
                // Track uncovered bad debt
                unrecoverableBadDebt += (badDebt - insuranceFund);
                insuranceFund = 0;
            }

            // Liquidation proceeds regardless
            seizeCollateral(user, pos.collateral);
        } else {
            // Normal liquidation
            seizeCollateral(user, pos.collateral);
        }

        delete positions[user];
    }
}
```

## Pattern #8: Fixed Bonus Insufficient Collateral

### VULNERABLE
```solidity
contract VulnerableFixedBonus {
    uint256 public constant LIQUIDATION_BONUS = 1100; // 110%

    function liquidate(address user) external {
        Position memory pos = positions[user];

        // ISSUE: 110% bonus fails when collateral ratio < 110%
        // Position: 100 debt, 105 collateral (105% ratio)
        // Bonus: 100 * 1.1 = 110 collateral required
        // Available: 105 collateral
        // Revert: arithmetic underflow or insufficient collateral

        uint256 bonusAmount = (pos.debt * LIQUIDATION_BONUS) / 1000;
        require(pos.collateral >= bonusAmount, "Insufficient collateral");

        // Cannot liquidate underwater positions
    }
}
```

### FIXED
```solidity
contract FixedDynamicBonus {
    uint256 public constant MAX_LIQUIDATION_BONUS = 1100; // 110% max

    function liquidate(address user) external {
        Position memory pos = positions[user];

        // Dynamic bonus capped at available collateral
        uint256 idealBonus = (pos.debt * MAX_LIQUIDATION_BONUS) / 1000;
        uint256 actualBonus = idealBonus <= pos.collateral
            ? idealBonus
            : pos.collateral;

        token.transferFrom(msg.sender, address(this), pos.debt);
        token.transfer(msg.sender, actualBonus);

        // Works even with low collateral ratios
        delete positions[user];
    }
}
```

## Pattern #9: Non-18 Decimal Reverts

### VULNERABLE
```solidity
contract VulnerableDecimals {
    function liquidate(address user) external {
        Position memory pos = positions[user];

        // ISSUE: Assumes 18 decimals
        // USDC has 6 decimals, WBTC has 8
        uint256 bonus = (pos.debt * 1e18 * 110) / 100 / 1e18;

        // For USDC (6 decimals):
        // debt = 1000 USDC = 1000 * 10^6
        // calculation: (1000 * 10^6 * 10^18 * 110) / 100 / 10^18
        // result wrong by 10^12 factor
    }
}
```

### FIXED
```solidity
contract FixedDecimals {
    mapping(address => uint8) public tokenDecimals;

    function liquidate(address user) external {
        Position memory pos = positions[user];

        // Get actual token decimals
        uint8 decimals = tokenDecimals[pos.token];
        uint256 decimalFactor = 10 ** decimals;

        // Correct calculation for any decimal precision
        uint256 bonus = (pos.debt * 110) / 100;

        token.transferFrom(msg.sender, address(this), pos.debt);
        token.transfer(msg.sender, bonus);

        delete positions[user];
    }
}
```

## Pattern #10: Multiple nonReentrant Modifiers

### VULNERABLE
```solidity
contract VulnerableReentrancy {
    bool private locked;

    modifier nonReentrant() {
        require(!locked, "ReentrancyGuard: reentrant call");
        locked = true;
        _;
        locked = false;
    }

    // ISSUE: Both functions have nonReentrant
    function liquidate(address user) external nonReentrant {
        Position memory pos = positions[user];

        // Calls internal liquidation
        _liquidateInternal(user, pos);
    }

    function _liquidateInternal(address user, Position memory pos)
        internal
        nonReentrant  // Second nonReentrant - causes revert!
    {
        seizeCollateral(user, pos);
    }
}
```

### FIXED
```solidity
contract FixedReentrancy {
    bool private locked;

    modifier nonReentrant() {
        require(!locked, "ReentrancyGuard: reentrant call");
        locked = true;
        _;
        locked = false;
    }

    // Only external entry point has nonReentrant
    function liquidate(address user) external nonReentrant {
        Position memory pos = positions[user];
        _liquidateInternal(user, pos);
    }

    // Internal function - no nonReentrant
    function _liquidateInternal(address user, Position memory pos) internal {
        seizeCollateral(user, pos);
    }
}
```

## Pattern #11: Zero Value Transfer Reverts

### VULNERABLE
```solidity
contract VulnerableZeroTransfer {
    function liquidate(address user) external {
        Position memory pos = positions[user];

        // ISSUE: Some tokens revert on zero transfer
        // Edge case: pos.collateral = 0 (bad debt position)
        token.transfer(msg.sender, pos.collateral); // Reverts!

        delete positions[user];
    }
}
```

### FIXED
```solidity
contract FixedZeroTransfer {
    function liquidate(address user) external {
        Position memory pos = positions[user];

        // Skip zero transfers
        if (pos.collateral > 0) {
            token.transfer(msg.sender, pos.collateral);
        }

        delete positions[user];
    }
}
```

## Pattern #12: Token Deny List Reverts

### VULNERABLE
```solidity
contract VulnerableDenyList {
    function liquidate(address user) external {
        Position memory pos = positions[user];

        // ISSUE: Transfer to blacklisted user reverts
        // User gets blacklisted by USDC
        // Cannot transfer to user address
        debtToken.transfer(user, repaymentRefund);

        // Liquidation reverts, position unliquidatable
    }
}
```

### FIXED
```solidity
contract FixedDenyList {
    mapping(address => uint256) public claimableRefunds;

    function liquidate(address user) external {
        Position memory pos = positions[user];

        // Don't transfer directly to user - let them claim
        claimableRefunds[user] += repaymentRefund;

        // Liquidation succeeds regardless of blacklist status
        seizeCollateral(msg.sender, pos.collateral);
        delete positions[user];
    }

    function claimRefund() external {
        uint256 amount = claimableRefunds[msg.sender];
        claimableRefunds[msg.sender] = 0;

        // User claims when not blacklisted
        debtToken.transfer(msg.sender, amount);
    }
}
```

## Pattern #13: Single Borrower Edge Case

### VULNERABLE
```solidity
contract VulnerableSingleBorrower {
    uint256 public totalBorrowers;
    uint256 public totalDebt;

    function liquidate(address user) external {
        Position memory pos = positions[user];

        // ISSUE: Division by zero when only 1 borrower
        uint256 shareOfBadDebt = pos.debt / (totalBorrowers - 1);

        // Revert when totalBorrowers == 1
    }
}
```

### FIXED
```solidity
contract FixedSingleBorrower {
    uint256 public totalBorrowers;
    uint256 public totalDebt;

    function liquidate(address user) external {
        Position memory pos = positions[user];

        // Handle single borrower case
        uint256 shareOfBadDebt;
        if (totalBorrowers > 1) {
            shareOfBadDebt = pos.debt / (totalBorrowers - 1);
        } else {
            // Last borrower - no sharing needed
            shareOfBadDebt = pos.debt;
        }

        // Liquidation works with any number of borrowers
    }
}
```

## Summary: Key Protections

1. **Bounded iteration:** Liquidate by position ID, enforce max positions
2. **Safe data structures:** Don't modify EnumerableSet during iteration
3. **No nonce dependency:** Liquidation independent of user state
4. **Cancel pending actions:** Clear withdrawals during liquidation
5. **Callback isolation:** Use transferFrom or try/catch for callbacks
6. **Check all collateral:** Include external vaults
7. **Graceful bad debt:** Track uncovered losses, don't revert
8. **Dynamic bonus:** Cap at available collateral
9. **Decimal handling:** Use actual token decimals
10. **Single reentrancy guard:** Only on external entry point
11. **Zero checks:** Skip transfers when amount == 0
12. **No direct transfers:** Use claimable pattern for deny lists
13. **Edge case validation:** Handle n=1 borrower, n=0 positions
