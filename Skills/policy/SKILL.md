---
name: policy
description: 'Design an insurance underwriter policy'
context: fork
agent: protocol-policy
argument-hint: '[describe the risk model]'
---

# Underwriter Policy Design

**Task:** $ARGUMENTS

Read `.claude/agents/protocol-policy.md` before starting.

## Acceptance Criteria

- [ ] FHE pattern correct (allowThis + allow)
- [ ] Risk score uses 0-10000 bps scale
- [ ] Pool economics sustainable
- [ ] ERC-165 supportsInterface included

## Handoff

Return: policy specification with risk model, judge logic, and implementation path in reineira-code.
