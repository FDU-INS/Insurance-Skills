---
name: freight-compliance-docs
description: Generate freight documents (Bill of Lading, Rate Confirmation) and check carrier/broker compliance via FMCSA. Track insurance expiries and authority status. Use when a broker needs to generate a BOL or Rate Con, wants to verify carrier compliance, needs to check upcoming document expiries, or when booking a load. Triggered by phrases like "generate BOL", "generate rate con", "compliance check MC#", "upcoming expiries", or "document for load".
---

# Freight Compliance & Documents

Generates BOLs and Rate Confirmations as PDFs. Checks carrier compliance via FMCSA and tracks insurance expiries.

## Usage

### Generate BOL
```bash
cd skills/freight-compliance-docs/scripts
python3 bol_generator.py --shipper "ABC Corp" --consignee "XYZ Inc" --origin "Dallas, TX" --dest "Chicago, IL"
```

### Generate Rate Con
```bash
python3 rate_con_generator.py --carrier "XYZ Trucking" --mc 123456 --origin "Dallas, TX" --dest "Chicago, IL" --rate 3200
```

### Check compliance
```bash
python3 compliance_checker.py --mc 123456
python3 compliance_checker.py --scan-all
python3 compliance_checker.py --expiry-alerts
```

## Broker Text Commands

| Command | Action |
|---------|--------|
| `generate BOL [load ID]` | Create BOL PDF |
| `generate rate con [load ID]` | Create Rate Con PDF |
| `compliance check MC#[number]` | Check carrier compliance |
| `upcoming expiries` | List expiring insurance |

## Example SMS Outputs

### Doc generated:
```
📄 DOCS GENERATED - Load #12345
✅ BOL attached
✅ Rate Con attached
Carrier: XYZ Trucking (MC#123456) ✅ Compliant

Reply 'send carrier' to email docs
```

### Compliance alert:
```
⚠️ COMPLIANCE ALERT
XYZ Logistics (MC#789012)
Insurance expires in 14 days

Do not book new loads until renewed
```

## Integrations

This skill uses the following external services. See [INTEGRATIONS.md](../../INTEGRATIONS.md) for detailed setup instructions, API documentation links, and implementation guidance.

| Service | Purpose | Section in INTEGRATIONS.md |
|---------|---------|---------------------------|
| FMCSA SAFER API | Carrier insurance verification | Skill 6: FMCSA SAFER |
| DocuSign/HelloSign | E-signatures (future) | Skill 6: DocuSign/HelloSign |
| Twilio | SMS compliance alerts | Shared Infrastructure: Twilio |

## Document Storage

- PDFs: `~/.freight-broker/documents/`
- Naming: BOL-{timestamp}.pdf, RC-{timestamp}.pdf
- See [INTEGRATIONS.md](../../INTEGRATIONS.md) for complete integration architecture
