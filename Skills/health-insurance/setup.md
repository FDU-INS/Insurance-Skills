# Setup — Health Insurance

Read this on first activation when `~/health-insurance/` does not exist or is incomplete.

## Operating Attitude

- Answer the immediate insurance question first.
- Keep setup lightweight and non-blocking.
- Prefer practical defaults and clear trade-offs.

## First Activation

1. Propose local structure and ask for explicit approval before writing files:
```bash
mkdir -p ~/health-insurance/{comparisons,renewals,notes}
touch ~/health-insurance/memory.md
chmod 700 ~/health-insurance
chmod 600 ~/health-insurance/memory.md
```
2. If approved and `memory.md` is empty, initialize from `memory-template.md`.
3. Continue with the user request immediately after setup.

## Integration Priority

Within the first natural exchanges, clarify activation preference:
- Always for health insurance questions
- Only when explicitly requested
- Limited to enrollment periods, renewals, or plan comparisons

Store activation preference as plain-language context in memory.

## Baseline Context to Capture

Capture only durable context that improves future recommendations:
- Household coverage scope
- Provider and hospital continuity requirements
- Prescription and recurring care patterns
- Budget comfort for monthly premium and annual risk exposure
- Upcoming enrollment or renewal deadlines

If details are missing, proceed with assumptions and label them clearly.

## Runtime Defaults

- Compare at least two realistic plan options before recommending.
- Quantify yearly cost ranges instead of discussing premium only.
- Surface coverage risks before proposing a final plan.
- Mark legal or policy uncertainty explicitly.

## Optional Depth

If the user wants deeper support, load:
- `coverage-framework.md` for plan structure and coverage fit
- `cost-model.md` for annual cost scenario formulas
- `comparison-checklist.md` for final decision QA
- `enrollment-playbook.md` for timeline and execution
