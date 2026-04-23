---
name: member_exp_cli
description: Explain member coverage and benefits in plain language.
metadata:
  moltbot:
    bins: ["member_exp_cli.py"]
    env: ["ELEVANCE_API_BASE_URL", "ELEVANCE_API_TOKEN", "ELEVANCE_CLIENT_ID", "ELEVANCE_CLIENT_SECRET", "ELEVANCE_REFRESH_TOKEN"]
---

Use this skill when members need clear coverage summaries or benefits Q&A support.

## Commands

- `coverage-summary --member-id <id> --service <service>`
- `benefits-faq --member-id <id> --question <text>`

## Example

```bash
export ELEVANCE_DEMO_MODE=1
python3 member_exp_cli.py --json coverage-summary --member-id M-100 --service pcp_visit
```
