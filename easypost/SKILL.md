---
name: easypost
description: "EasyPost — shipping labels, rate comparison, package tracking, address verification, and insurance."
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "🚚", "requires": {"env": ["EASYPOST_API_KEY"]}, "primaryEnv": "EASYPOST_API_KEY", "homepage": "https://www.agxntsix.ai"}}
---

# 🚚 EasyPost

EasyPost — shipping labels, rate comparison, package tracking, address verification, and insurance.

## Requirements

| Variable | Required | Description |
|----------|----------|-------------|
| `EASYPOST_API_KEY` | ✅ | EasyPost API key |


## Quick Start

```bash
# Create shipment & get rates
python3 {{baseDir}}/scripts/easypost.py create-shipment --from "JSON address" --to "JSON address" --parcel "JSON"

# Get shipment details
python3 {{baseDir}}/scripts/easypost.py get-shipment <id>

# List shipments
python3 {{baseDir}}/scripts/easypost.py list-shipments --page-size "20"

# Buy label for shipment
python3 {{baseDir}}/scripts/easypost.py buy-shipment <id> --rate-id <value>

# Create a tracker
python3 {{baseDir}}/scripts/easypost.py create-tracker --tracking-code <value> --carrier <value>

# Get tracker details
python3 {{baseDir}}/scripts/easypost.py get-tracker <id>

# List trackers
python3 {{baseDir}}/scripts/easypost.py list-trackers --page-size "20"

# Verify/create address
python3 {{baseDir}}/scripts/easypost.py verify-address --street1 <value> --city <value> --state <value> --zip <value> --country "US"

# Insure a shipment
python3 {{baseDir}}/scripts/easypost.py create-insurance --shipment-id <value> --amount <value>

# Refund a label
python3 {{baseDir}}/scripts/easypost.py create-refund --carrier <value> --tracking-codes "comma-separated"

# List rates for shipment
python3 {{baseDir}}/scripts/easypost.py list-rates <id>

# Create return shipment
python3 {{baseDir}}/scripts/easypost.py create-return --from "JSON" --to "JSON" --parcel "JSON" --is-return "true"
```

## Output Format

All commands output JSON by default.

## Script Reference

| Script | Description |
|--------|-------------|
| `{baseDir}/scripts/easypost.py` | Main CLI — all commands in one tool |

## Credits
Built by [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) | [agxntsix.ai](https://www.agxntsix.ai)
[YouTube](https://youtube.com/@aiwithabidi) | [GitHub](https://github.com/aiwithabidi)
Part of the **AgxntSix Skill Suite** for OpenClaw agents.

📅 **Need help setting up OpenClaw for your business?** [Book a free consultation](https://cal.com/agxntsix/abidi-openclaw)
