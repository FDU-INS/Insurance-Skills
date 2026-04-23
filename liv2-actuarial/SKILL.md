---
name: flux-verify-claims
description: Use when about to say a fix works, tests are green, a bug is resolved, a task is done, or a branch is ready for review or submit.
user-invocable: false
---

# Verify Claims

Do not claim success from inference. Run the command that proves the claim, read the output, then state the result.

## Gate

Before any completion claim:
1. Identify the command that proves it
2. Run it now
3. Read the full result and exit status
4. State the real outcome

If you did not run the command in the current turn, you do not have evidence.

## Common Claims

| Claim | Required Evidence |
|---|---|
| Tests pass | Fresh test command with 0 failures |
| Build succeeds | Fresh build command exits 0 |
| Bug fixed | Reproduction or regression check now passes |
| Task done | Verification commands pass and task state is updated |
| Ready for review | Relevant checks are green on current diff |
| Ready to submit | Final verification on the branch is green |

## Flux Fit

Apply this before:
- `fluxctl done`
- invoking `flux:impl-review`
- saying SHIP or done in review loops
- PR creation
- submit, gate, and release claims

## Reporting Pattern

Good:
- `Ran \`pytest tests/auth -q\`: 24 passed, 0 failed.`
- `Ran \`npm run build\`: exit 0.`

Bad:
- `Should be fixed now`
- `Looks good`
- `Probably green`

## Gotchas

- Partial checks do not justify broad claims
- Prior runs do not count if code changed afterward
- Agent or reviewer reports do not replace your own verification
- Confidence is not evidence
