# French Property Investment Analyzer - Claude Code Skill

A Claude Code skill for analyzing French rental property investments with comprehensive financial modeling.

## Features

- **French-Specific Costs**: Includes arrangement fees (1%), registration fees (1.5%), survey fees (€750), and mandatory life insurance (0.4% annually)
- **Comprehensive Analysis**: Year-by-year cash flow projections, ROI calculations, and break-even analysis
- **Flexible Inputs**: Supports all major investment parameters including vacancy rates, rent increases, and various expenses
- **No External Dependencies**: Uses Python standard library only

## Installation

### Quick Install

Copy the skill files to your Claude Code skills directory:

```bash
# Create skills directory if it doesn't exist
mkdir -p ~/.claude/skills/french-property-investment

# Copy skill files
cp french_mortgage.py ~/.claude/skills/french-property-investment/
cp SKILL.md ~/.claude/skills/french-property-investment/

# Make script executable (if needed)
chmod +x ~/.claude/skills/french-property-investment/french_mortgage.py
```

### Verify Installation

Test that the skill works:

```bash
cd ~/.claude/skills/french-property-investment
echo '{
  "propertyPrice": 300000,
  "downPayment": 60000,
  "interestRate": 3.5,
  "loanTermYears": 20,
  "monthlyRent": 1500,
  "holdingPeriodYears": 10
}' | python3 french_mortgage.py --json-input
```

You should see detailed JSON output with mortgage details, yearly projections, and investment summary.

## Usage with Claude

Once installed, you can ask Claude to analyze French properties naturally:

### Example Conversations

**Basic Analysis:**
> "Analyze a 300k EUR property in France with 60k down payment, 3.5% interest rate, 20-year mortgage, renting for 1500/month. I plan to hold it for 10 years."

**With Additional Parameters:**
> "Same property but with 2400 EUR annual property tax, 150 EUR monthly HOA fees, 8% management fee, 5% vacancy rate, and 2% annual rent increases."

**Comparisons:**
> "Compare this to a 250k property renting for 1300/month with a 15-year mortgage at 3% interest."

Claude will:
1. Extract the parameters from your question
2. Call the skill with appropriate JSON input
3. Parse the comprehensive output
4. Present results in a conversational format with key insights

## Input Parameters

### Required
- `propertyPrice` (number): Property purchase price in EUR
- `downPayment` (number): Down payment in EUR
- `interestRate` (number): Annual interest rate as percentage (e.g., 3.5)
- `loanTermYears` (integer): Loan term in years
- `monthlyRent` (number): Monthly rental income in EUR
- `holdingPeriodYears` (integer): Investment holding period in years

### Optional
- `propertyTaxAnnual` (number): Annual property tax in EUR (default: 0)
- `hoaMonthly` (number): Monthly HOA/copropriété fees in EUR (default: 0)
- `maintenancePercent` (number): Annual maintenance as % of property value (default: 1.0)
- `managementFeePercent` (number): Property management fee as % of rent (default: 0)
- `vacancyRate` (number): Expected vacancy rate as percentage (default: 0)
- `rentIncreaseAnnual` (number): Annual rent increase as percentage (default: 0)

## Output Structure

The skill returns comprehensive JSON with:

### Mortgage Details
- Monthly payment (including life insurance)
- Total interest over loan term
- Total payments over loan term

### Yearly Projections
For each year of the holding period:
- Rental income (adjusted for vacancy and rent increases)
- Detailed expenses breakdown (mortgage, taxes, fees, maintenance, etc.)
- Net cash flow
- Cumulative cash flow
- Principal paydown
- Total equity built
- Remaining loan balance

### Investment Summary
- Initial investment required (down payment + fees)
- Total rental income
- Total expenses
- Total cash flow
- Total principal paid down
- Final equity
- Net profit
- ROI (%)
- Average cash-on-cash return (%)
- Break-even year (if reached)

## French Mortgage Specifics

The calculator automatically includes French-specific costs:

1. **Arrangement Fee**: 1% of loan amount (frais de dossier)
2. **Registration Fee**: 1.5% of loan amount (frais de garantie)
3. **Survey Fee**: €750 fixed cost
4. **Life Insurance**: 0.4% of loan amount annually, included in monthly payment

These are added to your down payment to calculate the total initial investment.

## Troubleshooting

### Skill Not Found
Verify the skill is in the correct location:
```bash
ls -la ~/.claude/skills/french-property-investment/
```

You should see:
- `french_mortgage.py`
- `SKILL.md`
- `README.md`

### Python Not Found
Ensure Python 3 is installed:
```bash
python3 --version
```

Should show Python 3.8 or later.

### Test Manually
If Claude can't invoke the skill, test it manually:
```bash
cd ~/.claude/skills/french-property-investment
python3 french_mortgage.py --help
```

### Invalid JSON
If you get JSON parsing errors, test the input:
```bash
echo '{"propertyPrice": 300000, "downPayment": 60000, "interestRate": 3.5, "loanTermYears": 20, "monthlyRent": 1500, "holdingPeriodYears": 10}' | python3 french_mortgage.py --json-input | python3 -m json.tool
```

## Standalone Usage

You can also use the script without Claude:

### JSON Input (for programmatic use)
```bash
python3 french_mortgage.py --json-input < input.json
```

### CLI Arguments (for manual use)
```bash
python3 french_mortgage.py \
  --property-price 300000 \
  --down-payment 60000 \
  --interest-rate 3.5 \
  --loan-term-years 20 \
  --monthly-rent 1500 \
  --holding-period-years 10 \
  --format table
```

Use `--format json` or `--format table` to control output format.

## License

MIT License - See LICENSE file for details

## Version

2.0.0 - Python implementation
