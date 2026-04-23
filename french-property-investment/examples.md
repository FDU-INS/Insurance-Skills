# Usage Examples

Common scenarios and use cases for the French Property Investment Analyzer.

## Basic Analysis

Simplest case with only required parameters:

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

**Key outputs:**
- Monthly payment: €1,471.90
- Initial investment: €66,750 (€60k down + €6,750 French fees)
- 10-year ROI: ~169%
- Break-even year: 8

## Complete Analysis with All Expenses

Including property tax, HOA, maintenance, management, vacancy:

```bash
echo '{
  "propertyPrice": 300000,
  "downPayment": 60000,
  "interestRate": 3.5,
  "loanTermYears": 20,
  "monthlyRent": 1500,
  "holdingPeriodYears": 10,
  "propertyTaxAnnual": 2400,
  "hoaMonthly": 150,
  "maintenancePercent": 1.5,
  "managementFeePercent": 8,
  "vacancyRate": 5,
  "rentIncreaseAnnual": 2
}' | python3 french_mortgage.py --json-input
```

This more realistic scenario accounts for:
- €2,400/year property tax
- €150/month HOA fees
- 1.5% annual maintenance (€4,500/year)
- 8% management fee
- 5% vacancy rate
- 2% annual rent increases

## Comparing Multiple Properties

Compare Property A (300k) vs Property B (250k):

```bash
# Property A - Larger, higher rent
echo '{
  "propertyPrice": 300000,
  "downPayment": 60000,
  "interestRate": 3.5,
  "loanTermYears": 20,
  "monthlyRent": 1500,
  "holdingPeriodYears": 10
}' | python3 french_mortgage.py --json-input > property_a.json

# Property B - Smaller, lower rent
echo '{
  "propertyPrice": 250000,
  "downPayment": 50000,
  "interestRate": 3.5,
  "loanTermYears": 20,
  "monthlyRent": 1300,
  "holdingPeriodYears": 10
}' | python3 french_mortgage.py --json-input > property_b.json
```

Then analyze and compare:
- Initial investment required
- Monthly cash flow (positive or negative)
- ROI over 10 years
- Break-even year
- Total equity built

## Sensitivity Analysis

### Interest Rate Impact

Test different interest rates:

```bash
# Optimistic - 3.0%
echo '{
  "propertyPrice": 300000,
  "downPayment": 60000,
  "interestRate": 3.0,
  "loanTermYears": 20,
  "monthlyRent": 1500,
  "holdingPeriodYears": 10
}' | python3 french_mortgage.py --json-input

# Expected - 3.5%
echo '{
  "propertyPrice": 300000,
  "downPayment": 60000,
  "interestRate": 3.5,
  "loanTermYears": 20,
  "monthlyRent": 1500,
  "holdingPeriodYears": 10
}' | python3 french_mortgage.py --json-input

# Pessimistic - 4.5%
echo '{
  "propertyPrice": 300000,
  "downPayment": 60000,
  "interestRate": 4.5,
  "loanTermYears": 20,
  "monthlyRent": 1500,
  "holdingPeriodYears": 10
}' | python3 french_mortgage.py --json-input
```

Compare monthly payments and total interest paid.

### Vacancy Rate Impact

Test different vacancy scenarios:

```bash
# No vacancy
echo '{
  "propertyPrice": 300000,
  "downPayment": 60000,
  "interestRate": 3.5,
  "loanTermYears": 20,
  "monthlyRent": 1500,
  "holdingPeriodYears": 10,
  "vacancyRate": 0
}' | python3 french_mortgage.py --json-input

# Moderate vacancy - 5%
echo '{
  "propertyPrice": 300000,
  "downPayment": 60000,
  "interestRate": 3.5,
  "loanTermYears": 20,
  "monthlyRent": 1500,
  "holdingPeriodYears": 10,
  "vacancyRate": 5
}' | python3 french_mortgage.py --json-input

# High vacancy - 10%
echo '{
  "propertyPrice": 300000,
  "downPayment": 60000,
  "interestRate": 3.5,
  "loanTermYears": 20,
  "monthlyRent": 1500,
  "holdingPeriodYears": 10,
  "vacancyRate": 10
}' | python3 french_mortgage.py --json-input
```

## Different Loan Terms

Compare 15, 20, and 25-year mortgages:

```bash
# 15-year - Higher monthly payment, less total interest
echo '{
  "propertyPrice": 300000,
  "downPayment": 60000,
  "interestRate": 3.5,
  "loanTermYears": 15,
  "monthlyRent": 1500,
  "holdingPeriodYears": 15
}' | python3 french_mortgage.py --json-input

# 20-year - Balanced
echo '{
  "propertyPrice": 300000,
  "downPayment": 60000,
  "interestRate": 3.5,
  "loanTermYears": 20,
  "monthlyRent": 1500,
  "holdingPeriodYears": 20
}' | python3 french_mortgage.py --json-input

# 25-year - Lower monthly payment, more total interest
echo '{
  "propertyPrice": 300000,
  "downPayment": 60000,
  "interestRate": 3.5,
  "loanTermYears": 25,
  "monthlyRent": 1500,
  "holdingPeriodYears": 25
}' | python3 french_mortgage.py --json-input
```

## Down Payment Scenarios

Compare different down payment amounts:

```bash
# 10% down
echo '{
  "propertyPrice": 300000,
  "downPayment": 30000,
  "interestRate": 3.5,
  "loanTermYears": 20,
  "monthlyRent": 1500,
  "holdingPeriodYears": 10
}' | python3 french_mortgage.py --json-input

# 20% down
echo '{
  "propertyPrice": 300000,
  "downPayment": 60000,
  "interestRate": 3.5,
  "loanTermYears": 20,
  "monthlyRent": 1500,
  "holdingPeriodYears": 10
}' | python3 french_mortgage.py --json-input

# 30% down
echo '{
  "propertyPrice": 300000,
  "downPayment": 90000,
  "interestRate": 3.5,
  "loanTermYears": 20,
  "monthlyRent": 1500,
  "holdingPeriodYears": 10
}' | python3 french_mortgage.py --json-input
```

Higher down payment means:
- Lower monthly payments
- Less total interest
- Higher initial investment
- Potentially lower ROI %

## Rent Growth Scenarios

Compare flat rent vs growing rent:

```bash
# Flat rent - no increases
echo '{
  "propertyPrice": 300000,
  "downPayment": 60000,
  "interestRate": 3.5,
  "loanTermYears": 20,
  "monthlyRent": 1500,
  "holdingPeriodYears": 10,
  "rentIncreaseAnnual": 0
}' | python3 french_mortgage.py --json-input

# Inflation-adjusted - 2% annual
echo '{
  "propertyPrice": 300000,
  "downPayment": 60000,
  "interestRate": 3.5,
  "loanTermYears": 20,
  "monthlyRent": 1500,
  "holdingPeriodYears": 10,
  "rentIncreaseAnnual": 2
}' | python3 french_mortgage.py --json-input

# Aggressive growth - 4% annual
echo '{
  "propertyPrice": 300000,
  "downPayment": 60000,
  "interestRate": 3.5,
  "loanTermYears": 20,
  "monthlyRent": 1500,
  "holdingPeriodYears": 10,
  "rentIncreaseAnnual": 4
}' | python3 french_mortgage.py --json-input
```

## Table Output for Presentation

Generate human-readable tables:

```bash
python3 french_mortgage.py \
  --property-price 300000 \
  --down-payment 60000 \
  --interest-rate 3.5 \
  --loan-term-years 20 \
  --monthly-rent 1500 \
  --holding-period-years 10 \
  --property-tax-annual 2400 \
  --hoa-monthly 150 \
  --format table
```

Produces formatted output with:
- Investment overview
- Year-by-year table
- Summary metrics

## Conversational Usage with Claude

**User asks:**
> "I'm looking at a 280k apartment in Lyon. I can put down 50k, the bank quotes 3.8% over 20 years, and I think I can rent it for 1400/month. Is this a good investment over 10 years?"

**Claude extracts:**
- Property price: 280,000
- Down payment: 50,000
- Interest rate: 3.8
- Loan term: 20 (standard)
- Monthly rent: 1,400
- Holding period: 10

**Claude runs:**
```bash
echo '{
  "propertyPrice": 280000,
  "downPayment": 50000,
  "interestRate": 3.8,
  "loanTermYears": 20,
  "monthlyRent": 1400,
  "holdingPeriodYears": 10
}' | python3 french_mortgage.py --json-input
```

**Claude presents:**
- Monthly payment: ~€1,420
- Initial investment: ~€56,200
- 10-year net profit: ~€98,000
- ROI: ~174%
- Monthly cash flow: slightly negative at first, positive after ~7 years
- Break-even: Year 7

Then discuss whether this meets the user's investment goals.
