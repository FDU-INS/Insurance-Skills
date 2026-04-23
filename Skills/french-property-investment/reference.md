# API Reference

Complete parameter and output specification for the French Property Investment Analyzer.

## Input Parameters

### Required

| Parameter | Type | Description |
|-----------|------|-------------|
| `propertyPrice` | number | Property purchase price in EUR (must be > 0) |
| `downPayment` | number | Down payment in EUR (must be >= 0 and < propertyPrice) |
| `interestRate` | number | Annual interest rate as percentage (e.g., 3.5 for 3.5%, must be > 0) |
| `loanTermYears` | integer | Loan term in years (must be > 0) |
| `monthlyRent` | number | Monthly rental income in EUR (must be >= 0) |
| `holdingPeriodYears` | integer | Investment holding period in years (must be > 0) |

### Optional

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `propertyTaxAnnual` | number | 0 | Annual property tax (taxe foncière) in EUR |
| `hoaMonthly` | number | 0 | Monthly HOA/copropriété fees in EUR |
| `maintenancePercent` | number | 1.0 | Annual maintenance cost as % of property value |
| `managementFeePercent` | number | 0 | Property management fee as % of monthly rent |
| `vacancyRate` | number | 0 | Expected vacancy rate as percentage (0-100) |
| `rentIncreaseAnnual` | number | 0 | Annual rent increase as percentage (must be > -100) |

## Output Structure

### Root Object

```json
{
  "input": { /* echo of all input parameters */ },
  "mortgage": { /* mortgage details */ },
  "yearlyProjections": [ /* array of yearly data */ ],
  "summary": { /* investment summary */ }
}
```

### Mortgage Details

```json
{
  "monthlyPayment": 1471.90,     // Monthly payment including life insurance
  "totalInterest": 113256.80,    // Total interest over full loan term
  "totalPayments": 353256.80     // Total amount paid over full loan term
}
```

### Yearly Projection (one per year)

```json
{
  "year": 1,
  "rentalIncome": 18000.00,           // Rental income (adjusted for vacancy, rent increases)
  "expenses": {
    "mortgage": 17662.80,              // Annual mortgage payments
    "propertyTax": 0.00,               // Annual property tax
    "hoa": 0.00,                       // Annual HOA fees
    "maintenance": 3000.00,            // Annual maintenance
    "management": 0.00,                // Annual management fees
    "insurance": 960.00,               // Annual life insurance
    "total": 20662.80                  // Sum of all expenses
  },
  "netCashFlow": -2662.80,             // Rental income - total expenses
  "cumulativeCashFlow": -69412.80,     // Running total (including initial investment)
  "principalPaydown": 9412.89,         // Principal paid this year
  "totalEquity": 69412.89,             // Down payment + total principal paid
  "remainingBalance": 230587.11        // Outstanding loan balance
}
```

### Investment Summary

```json
{
  "initialInvestment": 66750.00,     // Down payment + fees
  "loanAmount": 240000.00,           // Property price - down payment
  "totalRentalIncome": 180000.00,    // Sum of all rental income
  "totalExpenses": 176628.00,        // Sum of all expenses
  "totalCashFlow": 3372.00,          // Total rental income - total expenses
  "totalPrincipalPaydown": 115886.18, // Total principal paid during holding period
  "finalEquity": 175886.18,          // Down payment + total principal paydown
  "netProfit": 112508.18,            // Cash flow + equity - initial investment
  "roi": 168.55,                     // (Net profit / initial investment) × 100
  "avgCashOnCashReturn": 0.51,       // Average annual cash-on-cash return %
  "breakEvenYear": 8                 // Year when cumulative cash flow >= 0 (null if never)
}
```

## Calculated Costs

### Initial Investment

```
Initial Investment = Down Payment + Arrangement Fee + Registration Fee + Survey Fee
```

Where:
- Arrangement Fee = Loan Amount × 0.01
- Registration Fee = Loan Amount × 0.015
- Survey Fee = 750 EUR (fixed)

### Monthly Payment

```
Base Payment = P × [r(1+r)^n] / [(1+r)^n - 1]
Life Insurance = (Loan Amount × 0.004) / 12
Monthly Payment = Base Payment + Life Insurance
```

Where:
- P = Loan amount (property price - down payment)
- r = Monthly interest rate (annual rate / 100 / 12)
- n = Number of payments (loan term years × 12)

### Yearly Metrics

**Rental Income (per year):**
```
Base Rent = Monthly Rent × (1 + Rent Increase %)^(Year - 1)
Effective Rent = Base Rent × (1 - Vacancy Rate / 100)
Annual Rental Income = Effective Rent × 12
```

**Expenses (per year):**
```
Mortgage = Monthly Payment × 12
Property Tax = Property Tax Annual
HOA = HOA Monthly × 12
Maintenance = Property Price × (Maintenance % / 100)
Management = Base Rent × 12 × (Management Fee % / 100)
Insurance = Loan Amount × 0.004
```

**Net Cash Flow:**
```
Net Cash Flow = Rental Income - Total Expenses
```

**Cumulative Cash Flow:**
```
Year 1: -Initial Investment + Net Cash Flow
Year N: Previous Cumulative + Net Cash Flow
```

**Principal Paydown:**
Calculated month-by-month using amortization:
```
For each month:
  Interest Payment = Remaining Balance × Monthly Rate
  Principal Payment = Monthly Payment - Interest Payment
  Remaining Balance -= Principal Payment
```

### Summary Metrics

**ROI (Return on Investment):**
```
Net Profit = Total Cash Flow + Final Equity - Initial Investment
ROI = (Net Profit / Initial Investment) × 100
```

**Average Cash-on-Cash Return:**
```
Avg CoC = (Total Cash Flow / Holding Period Years / Initial Investment) × 100
```

**Break-Even Year:**
First year where `Cumulative Cash Flow >= 0`, or `null` if never reached.

## CLI Usage

### JSON Input (Recommended)

```bash
echo '{"propertyPrice": 300000, "downPayment": 60000, ...}' | python3 french_mortgage.py --json-input
```

### Command-Line Arguments

```bash
python3 french_mortgage.py \
  --property-price 300000 \
  --down-payment 60000 \
  --interest-rate 3.5 \
  --loan-term-years 20 \
  --monthly-rent 1500 \
  --holding-period-years 10
```

### Output Formats

- `--format json` (default): Structured JSON output
- `--format table`: Human-readable table format

## Input Validation

The script validates:
- Property price must be positive
- Down payment must be non-negative and less than property price
- Interest rate must be positive
- Loan term must be positive
- Holding period must be positive
- Vacancy rate must be between 0-100%
- Rent increase must be greater than -100%

Invalid inputs return error messages with specific constraint violations.

## Requirements

- Python 3.8 or later
- No external dependencies (uses standard library only)
