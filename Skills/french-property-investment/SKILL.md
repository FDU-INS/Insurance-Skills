---
name: french-property-investment
description: Analyze French rental property investments with comprehensive financial modeling. Use when analyzing French properties, calculating mortgage payments, ROI, cash flow projections, or break-even analysis. Includes French-specific costs like arrangement fees (1%), registration fees (1.5%), survey fees (€750), and mandatory life insurance (0.4% annually).
allowed-tools: Bash(python:*)
---

# French Property Investment Analyzer

Analyze French rental property investments with detailed cash flow projections, ROI calculations, and break-even analysis.

## Quick Start

The calculator runs via Python script with JSON input/output:

```bash
echo '{
  "propertyPrice": 300000,
  "downPayment": 60000,
  "interestRate": 3.5,
  "loanTermYears": 20,
  "monthlyRent": 1500,
  "holdingPeriodYears": 10
}' | python3 french_mortgage.py --json-input
```

Returns comprehensive JSON with mortgage details, yearly projections, and investment summary.

## Required Parameters

| Parameter | Description |
|-----------|-------------|
| `propertyPrice` | Property purchase price in EUR |
| `downPayment` | Down payment in EUR |
| `interestRate` | Annual interest rate (%) |
| `loanTermYears` | Loan term in years |
| `monthlyRent` | Monthly rental income in EUR |
| `holdingPeriodYears` | Investment holding period in years |

## Optional Parameters

See [reference.md](reference.md) for complete parameter list including property tax, HOA fees, maintenance, management fees, vacancy rate, and rent increases.

## French-Specific Costs

The calculator automatically includes:
- **Arrangement Fee**: 1% of loan amount
- **Registration Fee**: 1.5% of loan amount
- **Survey Fee**: €750 fixed
- **Life Insurance**: 0.4% annually (in monthly payment)

## Common Use Cases

For detailed examples of comparing properties, sensitivity analysis, and handling complex scenarios, see [examples.md](examples.md).

## Key Output Metrics

- **Monthly Payment**: Mortgage + life insurance
- **ROI**: (Net profit / Initial investment) × 100
- **Cash-on-Cash Return**: Annual cash flow / initial investment
- **Break-Even Year**: When cumulative cash flow becomes positive
- **Equity Build-Up**: Down payment + principal paid

## How to Use with Claude

When the user mentions French property analysis, extract parameters from natural language and run the analysis.

**Example user request:**
> "What's the ROI on a 300k property with 20% down, 3.5% interest, renting for 1500/month?"

**Extract and run:**
```bash
echo '{
  "propertyPrice": 300000,
  "downPayment": 60000,
  "interestRate": 3.5,
  "loanTermYears": 20,
  "monthlyRent": 1500,
  "holdingPeriodYears": 10
}' | python3 french_mortgage.py --json-input
```

Present the ROI, monthly payment, cash flow, and break-even year from the results.

## Additional Resources

- [reference.md](reference.md) - Complete API documentation
- [examples.md](examples.md) - Usage examples and common scenarios
