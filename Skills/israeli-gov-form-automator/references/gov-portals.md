# Israeli Government Portals Reference

## Main Government Portals

| Portal | URL | Description | Authentication |
|--------|-----|-------------|----------------|
| gov.il (Central) | https://www.gov.il | Unified government services portal | gov.il account |
| Rashut HaMisim (Tax Authority) | https://www.misim.gov.il | Income tax, VAT, purchase tax | Personal area login |
| Bituach Leumi (National Insurance) | https://www.btl.gov.il | Social security benefits and claims | Personal area login |
| Rasham HaChevarot (Companies Registrar) | https://www.ica.justice.gov.il | Company registration and filings | Digital certificate |
| Misrad HaPnim (Interior Ministry) | https://www.gov.il/he/departments/ministry_of_interior | Population registry, ID services | gov.il account |
| Rashut HaTaagidim (Corporations Authority) | https://www.gov.il/he/departments/corporations_authority | Non-profit organizations | gov.il account |

## Common Government Forms

### Tax Authority (Rashut HaMisim) Forms

| Form | Hebrew Name | Purpose | Filing Method |
|------|-------------|---------|---------------|
| Tofes 101 | טופס 101 | Employee tax coordination | PDF / Online |
| Tofes 106 | טופס 106 | Annual salary report (employer) | Online |
| Tofes 135 | טופס 135 | Self-employed annual report | Online |
| Tofes 1301 | טופס 1301 | Individual annual tax return | Online |
| Tofes 857 | טופס 857 | Pension fund annual report | PDF |
| Tofes 119 | טופס 119 | Tax credit request | Online |
| Tofes 161 | טופס 161 | Severance pay tax approval | PDF / Online |

### Bituach Leumi (National Insurance) Forms

| Form | Hebrew Name | Purpose | Filing Method |
|------|-------------|---------|---------------|
| Dmei Leida | דמי לידה | Maternity benefit claim | Online |
| Nechut | נכות | Disability claim | Online |
| Avtala | אבטלה | Unemployment benefit claim | Online |
| Pgia BaAvoda | פגיעה בעבודה | Work injury claim | Online |
| Kitzba LZikna | קצבת זקנה | Old age pension claim | Online |
| Dmei Makhala | דמי מחלה | Sick pay claim | Online |

### Companies Registrar Forms

| Form | Hebrew Name | Purpose | Filing Method |
|------|-------------|---------|---------------|
| Rishum Chevra | רישום חברה | New company registration | Online |
| Doch Shnati LaRasham | דוח שנתי לרשם | Annual company report | Online |
| Shinui Direktorim | שינוי דירקטורים | Director change notification | Online |
| Shinui Baalei Mniayot | שינוי בעלי מניות | Shareholder change | Online |
| Piruq Chevra | פירוק חברה | Company dissolution | Online / PDF |

## Authentication Methods

### gov.il Account
- Registration: https://www.gov.il/he/service/register-to-digital-services
- Methods: SMS OTP, biometric ID, digital certificate
- Session duration: ~20 minutes inactive timeout

### Tax Authority Personal Area
- URL: https://www.misim.gov.il/shaamweb
- Known as SHAAM (sheirut atsmi me'ukav)
- Requires: Teudat Zehut + password or digital certificate

### Bituach Leumi Personal Area
- URL: https://www.btl.gov.il/benefits/Pages/default.aspx
- Requires: Teudat Zehut + password or gov.il SSO

## Date and Number Formats

| Field | Format | Example |
|-------|--------|---------|
| Date | DD/MM/YYYY | 15/03/2024 |
| Teudat Zehut | 9 digits (with leading zeros) | 012345678 |
| Phone (mobile) | 05X-XXXXXXX | 052-1234567 |
| Phone (landline) | 0X-XXXXXXX | 03-1234567 |
| Mikud (postal code) | 7 digits | 6100000 |
| Company number | 9 digits | 514567890 |
| Amuta (non-profit) number | 9 digits starting with 58 | 580123456 |

## Browser Automation Notes

### General Tips
- Government sites use Hebrew (RTL) -- set locale to `he-IL`
- Many forms are React/Angular SPAs -- wait for dynamic content
- File uploads often require specific formats (PDF, JPG) and size limits
- Digital signatures may be required for some submissions

### Common Selectors
- gov.il forms typically use `data-testid` attributes
- Tax Authority uses custom form components
- Bituach Leumi uses standard HTML forms with Hebrew labels

### Rate Limiting
- No official rate limits published
- Recommended: add 1-2 second delays between page navigations
- Peak hours (tax filing season March-May): expect slower responses
