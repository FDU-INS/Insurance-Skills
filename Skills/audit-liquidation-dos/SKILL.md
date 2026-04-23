---
name: audit-liquidation-dos
description: Audits Solidity liquidation mechanisms for denial of service vulnerabilities including unbounded loops over positions causing out-of-gas reverts, data structure corruption preventing liquidation, front-running to block liquidation via nonce changes or self-liquidation, pending withdrawals forcing reverts, malicious ERC721/ERC20 callback reverts, collateral in external vaults not seized, insufficient insurance fund blocking liquidation, fixed bonus exceeding available collateral, incorrect decimal handling, conflicting nonReentrant modifiers, zero value transfer reverts, token deny list issues, and single borrower edge cases
allowed-tools: Read, Grep, Glob
license: MIT
compatibility: Designed for Claude Code (or similar products)
metadata:
  author: Tomasz Kowalczyk (tom@auditmos.com)
  version: "1.0"
---

# Liquidation DoS Auditor

## When to Use
- Auditing liquidation mechanisms for DoS vectors
- User mentions: liquidation DoS, unbounded loops, gas limits, front-run liquidation, callback attacks, reentrancy, token compatibility
- Analyzing liquidation griefing attacks, gas exhaustion, revert conditions
- Reviewing position enumeration, collateral seizure, token integrations

## Audit Workflow

**IMPORTANT: Announce skill usage at the start of analysis**

Begin with: "I'm using the **audit-liquidation-dos** skill to analyze this contract for liquidation denial of service vulnerabilities..."

1. **Scan for liquidation operations**
   - Search: `liquidate`, `seizeCollateral`, `for`, `while`, `onERC721Received`, `transfer`, `nonReentrant`, `positions`, `EnumerableSet`
   - Focus: loops, callbacks, reentrancy guards, token transfers, balance checks

2. **Check against vulnerability patterns**
   - Reference `reference.md` for complete checklist
   - Compare code against `example.md`

3. **Validate exploitability**
   - **Check access control first** - grep for `onlyOwner|onlyAdmin|onlyGovernance` modifiers
   - Can non-privileged actors trigger liquidation DoS?
   - Can liquidation be blocked via gas exhaustion?
   - Can users front-run to prevent liquidation?
   - Can callbacks or hooks revert liquidation?
   - Can token incompatibilities block liquidation?
   - Verify no compensating protections exist
   - Downgrade severity if admin-only unless prevents all liquidations

4. **Generate report**
   - Use deliverable template below
   - Include PoC showing DoS condition
   - Rank by severity

## Core Vulnerability Patterns

See `reference.md` for full checklist. Key patterns:

1. Unbounded loops over positions → OOG revert during liquidation
2. Data structure corruption → liquidation reverts on corrupted state
3. Front-run prevention → nonce change or self-liquidation blocks liquidator
4. Pending withdrawals → equal to balance causes revert
5. Malicious callbacks → ERC721/ERC20 hooks revert to prevent liquidation
6. External vault collateral → not seized during liquidation
7. Insufficient insurance fund → bad debt blocks liquidation
8. Fixed bonus exceeds collateral → 110% bonus fails when ratio < 110%
9. Non-18 decimal handling → precision errors cause reverts
10. Multiple nonReentrant → conflicting guards block execution
11. Zero transfer reverts → missing checks with strict tokens
12. Token deny lists → USDC blocklists prevent transfers
13. Single borrower edge case → assumes > 1 borrower

**Code examples:** See `example.md`

## Severity Criteria

**Critical:** Liquidation permanently blocked causing protocol insolvency, all positions unliquidatable, **MUST be exploitable by non-privileged actors**
**High:** Specific positions unliquidatable via griefing, protocol accumulates bad debt from DoS, **MUST be exploitable by non-privileged actors**
**Medium:** Liquidation delayed or requires special conditions, increases bad debt risk, **admin-only liquidation function DoS issues with cascading impact**
**Low:** Edge case DoS with limited impact, easily mitigated, **admin-only function issues without immediate liquidation impact**

**IMPORTANT:** Admin-only liquidation functions (onlyOwner, onlyAdmin, onlyGovernance) with DoS vectors are **MEDIUM or LOW severity** unless:
- Admin function failure prevents all liquidations protocol-wide
- DoS in admin function enables bad debt accumulation affecting all users
- Admin liquidation path is the only liquidation mechanism (no trustless alternative)

## False Positives - Do NOT Flag

- Bounded loops with documented max limits
- Trusted token integrations (if explicitly documented)
- Admin-controlled liquidation paths with known restrictions
- Intentional liquidation delays with explicit design docs
- Protocols using liquidation queues or alternative mechanisms
- **Admin-only liquidation helper functions** (onlyOwner, onlyAdmin) where public liquidation path exists
- Governance-controlled collateral seizure functions with documented emergency-only usage
- Admin batch liquidation functions with gas limits where single liquidation still works

## Deliverable Format

**MANDATORY:** Before deliverable, verify each `checklist.md` item against codebase. Flag violations as findings.

Use template: `templates/report-template.md`

Each finding includes: severity, pattern #, file/lines, description, vulnerable code, DoS impact analysis, PoC showing griefing attack, remediation, gas impact.

## Key Principles

- **Bounded iteration** - never loop over unbounded user-controlled arrays
- **Graceful degradation** - liquidation should work even with bad debt/edge cases
- **Front-run resistance** - liquidation cannot be blocked by borrower actions
- **Callback isolation** - external calls cannot revert liquidation
- **Token compatibility** - handle zero transfers, deny lists, non-standard decimals

## Output Guidelines

**DO:**
- Reference specific lines and functions
- Provide executable PoCs showing DoS
- Quantify gas limits and iteration costs
- Show token compatibility issues

**DON'T:**
- Report intentional design choices with documentation
- Flag bounded loops with max limits
- Use vague terms ("could cause DoS")
- Ignore compensating mechanisms (liquidation queues, etc.)
