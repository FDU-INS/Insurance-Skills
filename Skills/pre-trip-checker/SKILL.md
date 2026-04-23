---
name: pre-trip-checker
description: Comprehensive pre-trip verification: visa requirements, transit rules, passport validity, vaccination/insurance requirements, travel advisories, neighborhood safety, strikes/protests, and health requirements. Combines Agent 7 (Visa & Documents) and Safety & Alerts into one pre-departure checklist. Use 2-4 weeks before travel.
---

# Pre-Trip Checker (Agent 7)

Everything you need to verify before you go — in one checklist.

## Two Parts

### 7A: Visa & Documents
- ✅ Visa requirements by nationality
- ✅ Transit visa rules (layovers)
- ✅ Passport validity (6-month rule)
- ✅ Vaccination requirements
- ✅ Travel insurance requirements
- ✅ Document checklist (printouts, photos, etc.)

### 7B: Safety & Alerts
- ✅ Government travel advisories
- ✅ Neighborhood safety ratings
- ✅ Current strikes/protests
- ✅ Health requirements & vaccinations
- ✅ Emergency contacts
- ✅ Scam alerts

## Quick Usage

```bash
python3 scripts/pre_trip_check.py \
  --passport SG \
  --destination TH \
  --transit MY \
  --depart 2025-05-15 \
  --nationality Singaporean
```

## Parameters

| Flag | Description | Example |
|------|-------------|---------|
| `--passport` | Passport country code | `SG`, `US`, `MY` |
| `--destination` | Destination country | `TH`, `JP`, `ID` |
| `--transit` | Transit countries | `MY`, `SG` |
| `--depart` | Departure date | `2025-05-15` |
| `--nationality` | Nationality | `Singaporean`, `American` |
| `--purpose` | Travel purpose | `tourism`, `business`, `transit` |
| `--duration` | Trip length | `7` (days) |

## Output: Pre-Departure Checklist

```
🛂 VISA & DOCUMENTS (7A)
═══════════════════════════════════════════

✅ VISA: Not required for Singaporean passport
   • Tourism: 30 days visa-free
   • Business: 30 days visa-free
   • Valid until: Entry date + 30 days

✅ PASSPORT: Valid
   • Expires: 2028-03-15
   • Rule: Must be valid 6 months beyond entry
   • Status: ✅ OK (valid for 2+ years)

⚠️  TRANSIT (Malaysia): Check requirements
   • If leaving airport: Transit visa required
   • If staying airside: No visa needed
   • Recommendation: Confirm with airline

✅ VACCINATIONS: None required
   • Routine: Up to date (recommended)
   • Yellow fever: Not required (unless from endemic area)
   • COVID-19: No restrictions

✅ INSURANCE: Recommended
   • Required: No
   • Recommended: Yes (medical coverage $50k+)
   • Provider suggestion: World Nomads, AXA

📋 DOCUMENT CHECKLIST
□ Passport (original + 2 photocopies)
□ Flight tickets (printed)
□ Hotel reservations (printed)
□ Travel insurance policy
□ Emergency contacts
□ Passport photos (2, for visa runs)

🚨 SAFETY & ALERTS (7B)
═══════════════════════════════════════════

✅ ADVISORY LEVEL: Exercise Normal Precautions
   • Source: US State Department, Level 1
   • UK FCO: No warnings
   • Singapore MFA: No advisories

⚠️  CURRENT SITUATION
   • Political: Stable
   • Protests: None significant
   • Strikes: BTS occasional (check before travel)
   • Crime: Low (watch for pickpockets in tourist areas)

🏥 HEALTH & SAFETY
   • Hospitals: Bumrungrad, Bangkok Hospital (international)
   • Emergency: 191 (police), 1669 (ambulance)
   • Water: Bottled only
   • Food: Street food generally safe

🚫 SCAM ALERTS
   • "Grand Palace closed" → FALSE (common scam)
   • "Special shopping deals" → Tourist traps
   • Tuk-tuk 20 baht tours → Shopping stops included

💡 RECOMMENDATIONS
   • Register with Singapore MFA (TravelReg)
   • Save emergency numbers
   • Download offline maps
   • Get local SIM on arrival
```

## Risk Levels

| Level | Meaning | Action |
|-------|---------|--------|
| ✅ **Go** | No issues | Normal prep |
| ⚠️ **Caution** | Minor concerns | Extra preparation |
| ❌ **Reconsider** | Significant risk | Consider alternatives |
| 🚫 **Do Not Travel** | Extreme risk | Postpone/cancel |

## Integration

Called by Coordinator before booking:

```python
# Pre-booking check
visa_check = PreTripChecker.verify(
    passport="SG",
    destination="TH",
    depart="2025-05-15"
)

if visa_check['visa_required'] and not has_visa:
    alert("Visa required - apply before booking")
```

## Data Sources

- **Visa**: IATA Timatic, government immigration sites
- **Advisories**: US State Dept, UK FCO, Singapore MFA
- **Health**: WHO, CDC, local health ministries
- **Safety**: OSAC, local news, expat forums

## See Also

- `references/visa_free_countries.md` — Visa-free access by passport
- `references/vaccination_requirements.md` — Health requirements by country
- `references/emergency_contacts.md` — Embassy numbers worldwide
