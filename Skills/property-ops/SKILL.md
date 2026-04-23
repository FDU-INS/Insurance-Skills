---
name: property-ops
description: >
  Real Estate & Property Management for the Owens household. Tracks the rental
  property ($120K equity, $1K/mo income) and primary residence ($245K mortgage).
  Tenant management, maintenance schedules, property tax payments, insurance
  renewals, market values, and depreciation tracking. Triggers on: "Rental check",
  "Property update", "Tenant", "Maintenance", "Property tax", "Home value",
  "Rental income", "Property management", "Lease", "Landlord", "Property ops",
  "Real estate", "House check", "Mortgage check". Real estate is a business —
  run it like one.
---

# Property Operations — S4 Financial (Real Estate Division)

**Mission:** Manage the Owens real estate portfolio as a business. Two properties (primary residence + rental) with combined equity of $365K+ and rental income of $12K/year. Maintenance deferred is equity destroyed. Tenants unmanaged is income at risk.

---

## Property Portfolio

### Primary Residence
| Field | Value |
|-------|-------|
| Type | Single Family Home |
| Location | Indianapolis, IN area |
| Mortgage Balance | $245,000 |
| Interest Rate | [data gap — verify] |
| Monthly Payment | [data gap — verify PITI] |
| Estimated Value | [data gap — verify] |
| Equity | [value - mortgage] |
| Insurance | [carrier, premium — verify] |
| Property Tax | [annual amount — verify] |

### Rental Property
| Field | Value |
|-------|-------|
| Type | [verify — SFH, duplex, condo?] |
| Location | [verify] |
| Equity | $120,000 (from financial plan) |
| Monthly Rent | $1,000 |
| Mortgage | [is there a mortgage? — verify] |
| Tenant | [current tenant status — verify] |
| Lease Expiration | [data gap] |
| Property Manager | [self-managed or PM company? — verify] |
| Insurance | [landlord policy — verify] |
| Property Tax | [annual amount — verify] |

---

## Procedure

### When Invoked — Property Check

1. **Read financial data:**
   - Financial Plan for property details
   - COP for any property-related flags

2. **Deliver Property Operations Brief:**

```
━━ PROPERTY OPS — [DATE] ━━

── PRIMARY RESIDENCE ──
  Mortgage: $245,000 remaining
  Payment: $X,XXX/mo (PITI)
  Equity: ~$XXX,XXX
  Maintenance: [any upcoming/overdue]
  Insurance: [renewal date, premium]
  Property Tax: [next due date]

── RENTAL PROPERTY ──
  Tenant Status: [occupied/vacant, lease term]
  Rent: $1,000/mo [current/past due]
  Cash Flow: $1,000 - expenses = $XXX net
  Maintenance: [any requests/upcoming]
  Insurance: [renewal date]
  Property Tax: [next due date]
  Depreciation: Year X of 27.5 ($X,XXX annual deduction)

FINANCIAL SUMMARY:
  Gross rental income (annual): $12,000
  Expenses: -$X,XXX
  Net rental income: $X,XXX
  Tax benefit (depreciation): $X,XXX
  Effective return on equity: X%

ACTION ITEMS:
  [Any pending property tasks]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Rental Property Management

### Tenant Management
- Lease tracking: start date, end date, renewal terms
- Rent collection: on-time record, payment method
- Communication log: maintenance requests, issues
- Tenant screening (for new tenants): credit, background, income verification

### Maintenance Calendar
| Frequency | Task |
|-----------|------|
| Monthly | HVAC filter change |
| Quarterly | Inspect exterior, gutters, landscaping |
| Semi-Annual | HVAC service (spring/fall) |
| Annual | Roof inspection, water heater flush |
| Annual | Smoke/CO detector battery replacement |
| As needed | Plumbing, electrical, appliance repair |
| Every 3-5 years | Interior paint, carpet replacement |
| Every 10-15 years | Roof replacement, HVAC replacement |

### Financial Tracking
```
Monthly Cash Flow:
  Rent collected:        $1,000
  Mortgage (if any):     -$XXX
  Insurance:             -$XXX
  Property tax (monthly): -$XXX
  Maintenance reserve:   -$100 (10% rule)
  Property management:   -$XXX (if applicable)
  ──────────
  Net cash flow:         $XXX
```

---

## Primary Residence Maintenance

### Seasonal Calendar
| Season | Tasks |
|--------|-------|
| Spring | HVAC service, gutter cleaning, exterior inspection, lawn startup |
| Summer | Deck/patio maintenance, check irrigation, pest inspection |
| Fall | Furnace service, gutter cleaning, winterize exterior, check roof |
| Winter | Check insulation, monitor ice dams, check pipes in cold snaps |

### Capital Improvement Tracking
Track improvements for tax basis purposes:
- Date, description, cost, category
- Improvements increase basis → reduce capital gains at sale
- Keep receipts (scan to iCloud)

---

## Tax Integration

- **Rental depreciation:** 27.5-year straight-line on building value (not land)
- **Deductible expenses:** mortgage interest, insurance, repairs, property tax, travel to property
- **Passive activity rules:** Net rental loss may offset other income (AGI-dependent)
- **1031 exchange:** If selling rental, defer capital gains by exchanging into new property
- **Primary residence:** $500K capital gains exclusion for MFJ (2 of 5 years occupancy)
- **Cross-reference:** tax-intel handles the tax optimization; property-ops provides the data

---

## Insurance Review

| Property | Coverage Type | Carrier | Premium | Renewal |
|----------|-------------|---------|---------|---------|
| Primary | Homeowner's | [?] | [?] | [?] |
| Rental | Landlord | [?] | [?] | [?] |
| Either | Umbrella | [?] | [?] | [?] |

**Action:** Ensure umbrella policy covers both properties. Landlord policy should include liability + loss of rent coverage.

---

## Integration

- **financial-intelligence:** Rental is an asset class in the portfolio
- **tax-intel:** Depreciation, rental income/loss, capital improvements
- **estate-guard:** Property titles, beneficiary/trust ownership
- **spend-intel:** Maintenance expenses flow through spending tracking
- **life-admin:** Insurance renewals, property tax deadlines

---

## The Standard

A rental property is a small business. It generates income, incurs expenses, requires maintenance, involves legal obligations, and has tax implications. Treating it like a passive asset is how landlords end up with deferred maintenance, unhappy tenants, and surprise expenses. This skill treats it like what it is: an investment that requires active management.
