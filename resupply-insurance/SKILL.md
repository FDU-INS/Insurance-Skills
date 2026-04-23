---
name: resupply-insurance
description: This skill should be used when the user asks about "insurance pool", "reIP", "InsurancePool", "protocol insurance", "bad debt coverage", "exit delay", "insurance vault", or needs to understand Resupply's insurance mechanism.
---

# Resupply Insurance Pool

The Insurance Pool (reIP) is an ERC4626 vault that provides coverage against protocol insolvency and bad debt. Located in `/src/protocol/InsurancePool.sol`.

## Overview

The Insurance Pool:
- Accepts reUSD deposits from users
- Issues reIP shares representing ownership
- Covers bad debt from liquidations
- Earns rewards from protocol fees
- Has a 7-day exit delay for withdrawals

## InsurancePool Contract

```solidity
contract InsurancePool is ERC4626, RewardDistributorMultiEpoch {
    // Exit delay configuration
    uint256 public constant EXIT_DELAY = 7 days;

    // Pending withdrawal tracking
    struct PendingWithdrawal {
        uint256 shares;
        uint256 unlockTime;
    }
    mapping(address => PendingWithdrawal) public pendingWithdrawals;

    // Bad debt tracking
    uint256 public totalBadDebt;
    uint256 public coveredBadDebt;
}
```

## Depositing to Insurance Pool

Deposit reUSD to receive reIP shares:

```solidity
// Standard ERC4626 deposit
function deposit(uint256 assets, address receiver) public returns (uint256 shares) {
    shares = previewDeposit(assets);

    // Transfer reUSD from depositor
    IERC20(asset()).safeTransferFrom(msg.sender, address(this), assets);

    // Mint reIP shares
    _mint(receiver, shares);

    emit Deposit(msg.sender, receiver, assets, shares);
}

// Share calculation
function previewDeposit(uint256 assets) public view returns (uint256) {
    uint256 supply = totalSupply();
    uint256 totalAssets = totalAssets();

    if (supply == 0) return assets;
    return (assets * supply) / totalAssets;
}
```

## Withdrawal Process

Withdrawals require a two-step process with a 7-day delay:

### Step 1: Request Withdrawal

```solidity
function requestWithdrawal(uint256 shares) external {
    require(balanceOf(msg.sender) >= shares, "Insufficient shares");

    // Lock shares
    _transfer(msg.sender, address(this), shares);

    // Set unlock time
    pendingWithdrawals[msg.sender] = PendingWithdrawal({
        shares: shares,
        unlockTime: block.timestamp + EXIT_DELAY
    });

    emit WithdrawalRequested(msg.sender, shares, block.timestamp + EXIT_DELAY);
}
```

### Step 2: Complete Withdrawal

```solidity
function completeWithdrawal() external returns (uint256 assets) {
    PendingWithdrawal memory pending = pendingWithdrawals[msg.sender];

    require(pending.shares > 0, "No pending withdrawal");
    require(block.timestamp >= pending.unlockTime, "Still locked");

    // Calculate assets
    assets = previewRedeem(pending.shares);

    // Clear pending
    delete pendingWithdrawals[msg.sender];

    // Burn shares and transfer assets
    _burn(address(this), pending.shares);
    IERC20(asset()).safeTransfer(msg.sender, assets);

    emit Withdraw(msg.sender, msg.sender, msg.sender, assets, pending.shares);
}
```

### Cancel Withdrawal

```solidity
function cancelWithdrawal() external {
    PendingWithdrawal memory pending = pendingWithdrawals[msg.sender];
    require(pending.shares > 0, "No pending withdrawal");

    // Return shares
    _transfer(address(this), msg.sender, pending.shares);

    delete pendingWithdrawals[msg.sender];

    emit WithdrawalCancelled(msg.sender, pending.shares);
}
```

## Bad Debt Coverage

The insurance pool covers bad debt from undercollateralized liquidations:

```solidity
function coverBadDebt(uint256 amount) external onlyLiquidationHandler {
    uint256 available = totalAssets();

    if (available >= amount) {
        // Full coverage - burn reUSD
        IStablecoin(asset()).burn(address(this), amount);
        coveredBadDebt += amount;
    } else {
        // Partial coverage
        if (available > 0) {
            IStablecoin(asset()).burn(address(this), available);
            coveredBadDebt += available;
        }
        // Remaining is protocol loss
        totalBadDebt += (amount - available);
    }

    emit BadDebtCovered(amount, available);
}
```

### Impact on Share Value

Bad debt coverage reduces total assets, affecting share value:

```solidity
// Before bad debt: 1000 reUSD, 1000 shares → 1 reUSD/share
// After 100 reUSD bad debt: 900 reUSD, 1000 shares → 0.9 reUSD/share
function totalAssets() public view returns (uint256) {
    return IERC20(asset()).balanceOf(address(this));
}
```

## Reward Distribution

Insurance pool participants earn rewards:

### Reward Sources

1. **Protocol fees**: Share of interest and redemption fees
2. **Liquidation fees**: Portion of liquidation proceeds
3. **RSUP emissions**: Governance token rewards

### Claiming Rewards

```solidity
function getReward(address _account) external {
    _checkpoint(_account);

    for (uint256 i = 0; i < rewardTokens.length; i++) {
        address token = rewardTokens[i];
        uint256 reward = earned(_account, token);

        if (reward > 0) {
            rewards[_account][token] = 0;
            IERC20(token).safeTransfer(_account, reward);
        }
    }
}
```

### Reward Tracking

```solidity
// Per-epoch reward accumulation
mapping(address token => mapping(uint256 epoch => uint256 amount)) public epochRewards;

// User reward integral
mapping(address user => mapping(address token => uint256 integral)) public userRewardIntegral;

function earned(address _account, address _token) public view returns (uint256) {
    uint256 balance = balanceOf(_account);
    uint256 rewardPerToken = rewardIntegral[_token] - userRewardIntegral[_account][_token];
    return (balance * rewardPerToken / 1e18) + rewards[_account][_token];
}
```

## Share Value Mechanics

The reIP share value fluctuates based on:

**Value increases from:**
- Interest fee distribution
- Redemption fee distribution
- RSUP reward accumulation

**Value decreases from:**
- Bad debt coverage
- Protocol losses

```solidity
// Share price calculation
function sharePrice() public view returns (uint256) {
    uint256 supply = totalSupply();
    if (supply == 0) return 1e18;
    return (totalAssets() * 1e18) / supply;
}
```

## Exit Delay Rationale

The 7-day exit delay:
- Prevents bank runs during stress
- Ensures capital availability for bad debt coverage
- Aligns incentives with protocol health
- Provides time for market stabilization

## Events

```solidity
event WithdrawalRequested(
    address indexed user,
    uint256 shares,
    uint256 unlockTime
);

event WithdrawalCancelled(
    address indexed user,
    uint256 shares
);

event BadDebtCovered(
    uint256 totalBadDebt,
    uint256 amountCovered
);

event RewardDistributed(
    address indexed token,
    uint256 amount,
    uint256 epoch
);
```

