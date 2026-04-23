# Treasury Circular 570 Verification Reference

## Data Source

- **URL:** https://www.fiscal.treasury.gov/surety-bonds/list-certified-companies.html
- **Format:** Downloadable Excel (current listing) or PDF (annual publication)
- **Fields in Excel:** Company name, NAIC code, business address, phone, states licensed, underwriting limit per bond, aggregate limit
- **Updated:** Continuously; annual publication August 1
- **Contact:** Surety.Bonds@fiscal.treasury.gov / 304-480-6635

## Verification Steps

### Step 1: Is the surety on Circular 570?
- Download the current Excel from the URL above
- Search for the surety name (exact match or fuzzy)
- If found: PASS. If not found: FAIL — surety is not federally approved.

### Step 2: Is the surety licensed in the project state?
- The Excel includes a "States Licensed" column
- Check that the project's state (e.g., MI for Michigan) appears
- If yes: PASS. If not: FAIL — surety cannot write bonds in that state.

### Step 3: Is the penal sum within the underwriting limit?
- The Excel includes "Underwriting Limit" per bond
- Compare the bond's penal sum against this limit
- If penal sum ≤ limit: PASS. If exceeds: FAIL or WARNING (may require reinsurance).

### Step 4: AM Best rating (optional but recommended)
- AM Best requires free registration: ambest.com
- Look up the surety by name or NAIC code
- A- or better is the industry standard for construction bonds
- Below A-: WARNING — surety may have financial concerns

## Surety Verification Portals (Direct Confirmation)

| Surety | Method | URL |
|--------|--------|-----|
| Merchants Bonding | Online form | https://www.merchantsbonding.com/surety-bonds/verify-a-bond |
| Intact Insurance | Online form | https://www.intactspecialty.com/en/surety/bond-verification-form.page |
| Frankenmuth | Online form | https://www.frankenmuthsurety.com/credentials/verify-your-bond/ |
| All others | Phone/email with bond number | Contact info in Circular 570 Excel |

## CBP Surety Codes

For cross-referencing: https://www.cbp.gov/sites/default/files/2024-08/Active%20Sureties%202024_0.pdf
Each surety has a 3-digit CBP code that can be used as a secondary verification.
