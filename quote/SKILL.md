---
name: quote
description: Generate a client insurance quote page from a PDF. Parses policy details and creates an HTML carrier comparison page ready for tiiny.host. Handles carrier vs carrier, full coverage vs liability-only, or single carrier scenarios.
disable-model-invocation: true
argument-hint: "[path-to-pdf]"
---

# /quote — Generate Client Quote Page from PDF

## Instructions

When invoked, follow these steps exactly:

### Step 1: Parse the PDF
Read the PDF at the provided path using the `Read` tool or `mcp__PDF_Tools_-_Analyze__Extract__Fill__Compare__read_pdf_content` tool. Extract:
- **Client name** (full name of the named insured)
- **Client address** (street, city, NC ZIP)
- **Vehicles** (year, make, model for each vehicle)
- **Per-vehicle premiums** (liability premium and comp/collision premium per vehicle, per option)
- **Per-vehicle usage** (commute, pleasure, business — from "Primary use of the vehicle" field)
- **Carrier names** (e.g., Dairyland, National General, Safeco, Progressive)
- **For each carrier/option**: liability limits, comp deductible, collision deductible, rental amount, towing amount, paid-in-full price, down payment, monthly payment after down, 6-month term total
- **Driver info** (name, relationship, years licensed, DOB if available)
- **Driver history** (look for discount keywords like "Safe Driving", "Accident Free", or any accident/violation entries — determine if each driver has a clean record or has incidents)

If the PDF contains data for more than 2 carriers, ask the user which two to compare.

### Step 2: Detect the scenario
Based on the parsed data, determine which of these 3 scenarios applies:

**Scenario A — Carrier vs Carrier** (default)
Two different carriers, both with similar coverage levels. This is the standard comparison.
- Detected when: Two different carrier names with comparable coverage (both full coverage or both liability-only)

**Scenario B — Full Coverage vs Liability-Only**
Same or different carriers, one option has comp+collision and the other has liability only.
- Detected when: One quote includes comp/collision deductibles and the other does not (or shows "N/A" / $0 / "None")
- Hero intro: "{Name}, full coverage vs liability-only for your {vehicles}. See what the extra protection costs."
- Key Difference card: Explain what full coverage adds (comp+collision) and the cost difference
- Best Value label changes to "Full Protection" on the full coverage card
- Secondary card label: "Budget Option" instead of "Option A"

**Scenario C — Single Carrier Quote**
Only one carrier/option in the PDF.
- Detected when: Only one set of carrier data found in the PDF
- Hero intro: "{Name}, here's your {Carrier} quote for your {vehicles}."
- Section 2 becomes a single centered card (no side-by-side comparison)
- No savings callout, no Key Difference section (section 3 removed — page has 5 sections)
- Daily cost card still shows below the single card
- Form carrier dropdown has only the one carrier pre-selected
- Mobile sticky CTA: "{Carrier} — BIND NOW / ${down} DOWN"

If unsure which scenario, ask the user.

### Step 3: Calculate derived data

**For Scenario A (Carrier vs Carrier):**
- **Savings**: Higher 6-month total minus lower 6-month total
- **Best Value**: Carrier with lower 6-month total
- **Daily cost**: Best Value 6-month total ÷ 182, rounded to 2 decimals
- **Key Difference**: The ONE meaningful coverage difference (usually comp deductible or a coverage gap)

**For Scenario B (Full Coverage vs Liability):**
- **Cost difference**: Full coverage 6-month total minus liability-only 6-month total
- **Daily cost**: Full coverage 6-month total ÷ 182, rounded to 2 decimals
- **Key Difference**: What comp+collision covers (damage to YOUR car) and the price gap. Bold the dollar amounts.

**For Scenario C (Single Carrier):**
- **Daily cost**: 6-month total ÷ 182, rounded to 2 decimals
- No savings or comparison calculations needed

### Step 4: Confirm data with user

**Scenario A confirmation table:**
```
Client: {name}
Address: {address}
Vehicles: {vehicle1}, {vehicle2}, ...
Scenario: Carrier vs Carrier

        Carrier A           Carrier B (Best Value)
Name:   {name}              {name}
Liab:   {limits}            {limits}
Comp:   ${ded}              ${ded}
Coll:   ${ded}              ${ded}
Rental: ${amt}/day          ${amt}/day
Towing: ${amt}              ${amt}
Down:   ${amount}           ${amount}
Mo:     ${amount}/mo        ${amount}/mo
6-Mo:   ${amount}           ${amount}
Saves:  —                   ${savings} vs {other}
Daily:  —                   ${daily}/day

Per-Vehicle Premiums (Carrier A / Carrier B):
  {vehicle1}: ${liab_A} / ${liab_B} (comp ded: ${ded_A} / ${ded_B})
  {vehicle2}: ${liab_A} / ${liab_B} (comp ded: ${ded_A} / ${ded_B})

Drivers:
  {driver1} — {relationship}, {yrs} yrs licensed, {Clean Record / Has Incidents}
  {driver2} — {relationship}, {yrs} yrs licensed, {Clean Record / Has Incidents}
```

**Scenario B confirmation table:**
```
Client: {name}
Address: {address}
Vehicles: {vehicle1}, {vehicle2}, ...
Scenario: Full Coverage vs Liability-Only

        Liability-Only      Full Coverage
Carrier:{name}              {name}
Liab:   {limits}            {limits}
Comp:   None                ${ded}
Coll:   None                ${ded}
Rental: ${amt}/day          ${amt}/day
Towing: ${amt}              ${amt}
Down:   ${amount}           ${amount}
Mo:     ${amount}/mo        ${amount}/mo
6-Mo:   ${amount}           ${amount}
Extra:  —                   +${difference} for full coverage
Daily:  —                   ${daily}/day

Per-Vehicle Premiums (Liability / With Comp):
  {vehicle1} ({usage}): ${liab} / ${comp} (comp ded: ${ded})
  {vehicle2} ({usage}): ${liab} / ${comp} (comp ded: ${ded})

Drivers:
  {driver1} — {relationship}, {yrs} yrs licensed, {Clean Record / Has Incidents}
  {driver2} — {relationship}, {yrs} yrs licensed, {Clean Record / Has Incidents}
```

**Scenario C confirmation table:**
```
Client: {name}
Address: {address}
Vehicles: {vehicle1}, {vehicle2}, ...
Scenario: Single Carrier Quote

Carrier: {name}
Liab:    {limits}
Comp:    ${ded}
Coll:    ${ded}
Rental:  ${amt}/day
Towing:  ${amt}
Down:    ${amount}
Mo:      ${amount}/mo
6-Mo:    ${amount}
Daily:   ${daily}/day

Per-Vehicle Premiums:
  {vehicle1} ({usage}): ${premium} (comp ded: ${ded})
  {vehicle2} ({usage}): ${premium} (comp ded: ${ded})

Drivers:
  {driver1} — {relationship}, {yrs} yrs licensed, {Clean Record / Has Incidents}
  {driver2} — {relationship}, {yrs} yrs licensed, {Clean Record / Has Incidents}
```

Ask: "Does this data look correct? Should I generate the quote page?"

### Step 5: Generate the HTML
Build a self-contained HTML file following the **Bill Layne Quote Template v3** design exactly. The template uses:

**Tech stack**: Self-contained HTML/CSS/JS, no external JS libraries
**Fonts**: Google Fonts — Inter (prices), Outfit (body), Plus Jakarta Sans (headings)
**Icons**: Font Awesome 6.5.1 CDN
**Favicon**: https://fav.farm/🛡️

**Agency constants** (never change):
- Agent: Bill Layne
- Phone: (336) 835-1993
- Email: Save@BillLayneInsurance.com
- Elkin Office: 1283 N Bridge St, Elkin, NC 28621
- Dobson Office: 209 S Main St, Dobson, NC 27017
- Founded: 2005
- Logo: https://i.imgur.com/lxu9nfT.png
- Bill Photo: https://i.imgur.com/BalAE1Q.jpeg
- Carrier logos: Dairyland=https://i.imgur.com/1VkIvxv.png, NatGen=https://i.imgur.com/HF8oPAF.png, Safeco=https://i.imgur.com/DDGMV4c.png

**Social links** (footer):
- Facebook: https://www.facebook.com/dollarbillagency/
- Instagram: https://www.instagram.com/ncautoandhome/
- YouTube: https://www.youtube.com/@ncautoandhome
- X: https://x.com/shopsavecompare

**Color system** (CSS variables):
- --slate-950: #020617 (page bg)
- --red-600: #dc2626 (primary accent, best value border, CTA buttons)
- --emerald-400: #34d399 (money/savings text)
- --emerald-500: #10b981 (checkmarks)
- --amber-500: #f59e0b (stars, warnings)
- --blue-400: #60a5fa (info icon)
- Glass cards: rgba(255,255,255,0.03) bg, backdrop-filter blur(12px), border 1px rgba(255,255,255,0.08)

**Design rules**:
- Best Value card: red border (2px solid --red-600), red glow shadow, larger price font, red CTA button
- Secondary card: default glass card, slate CTA button
- "Call me ASAP" = default contact time
- Recommended carrier = default in carrier dropdown
- Vehicle cards: glass card with red-tinted icon (fa-truck for trucks, fa-car for sedans, fa-car-side for SUVs/wagons), vehicle name in white, usage in slate-500, premium columns with comp/collision deductible labeled (e.g., "+ COMP ($100 DED)")
- Driver cards: glass card centered, green shield icon (fa-user-shield), name in white, relationship + years licensed in slate-500, green pill badge "Clean Record" (emerald border+bg) or amber "Has Incidents" if applicable
- Mobile footer padding: `@media (max-width: 767px) { footer { padding-bottom: 7rem !important; } }` — ensures social links clear the sticky CTA bar

**Page structure by scenario:**

**Scenario A — Carrier vs Carrier (8 sections):**
1. **Hero** — Logo top-left (height:3.5rem), dark car hero image, "YOUR QUOTE" title, one-line intro
2. **Carrier Comparison** — Two side-by-side cards + daily cost card below
3. **Key Difference** — Single card, one paragraph, under 50 words
4. **Your Vehicles** — Grid of glass cards (one per vehicle). Each card shows: vehicle icon, year/make/model, usage type, and per-carrier annual premiums with comp/collision deductible noted (e.g., "+ COMP ($100 DED)"). Footnote: "Annual per-vehicle premiums shown"
5. **Your Drivers** — Two-column grid of glass cards. Each card shows: shield icon, driver name, relationship + years licensed, and a green "Clean Record" pill badge (or incidents if applicable). Footnote: discount details (e.g., "5-Year Accident Free • 3-Year Safe Driving discount applied")
6. **What Happens Next** — 3 red-numbered steps
7. **Bind Form** — Pre-filled name, carrier dropdown (best value default), contact time, mailto fallback
8. **Testimonial + Footer** — 5-star review, Bill's photo, phone, email, social links, both offices

**Scenario B — Full Coverage vs Liability (8 sections):**
1. **Hero** — Same layout, intro: "{Name}, full coverage vs liability-only for your {vehicles}."
2. **Coverage Comparison** — Two side-by-side cards: "Budget Option" (liability) vs "Full Protection" (full coverage, red border). Full coverage card gets the red CTA. Show cost difference instead of savings.
3. **Key Difference** — Explain what comp+collision covers: "Full coverage includes comprehensive and collision — if your car is damaged, stolen, or totaled, you're covered. Liability-only means you pay out of pocket. The difference is **${amount}/month**."
4. **Your Vehicles** — Same grid as Scenario A but columns show "Liability" vs "+ Comp (${ded} ded)" premiums per vehicle
5. **Your Drivers** — Same as Scenario A
6. **What Happens Next** — Same 3 steps
7. **Bind Form** — Dropdown shows both options with coverage level labels
8. **Testimonial + Footer** — Same as Scenario A

**Scenario C — Single Carrier (7 sections):**
1. **Hero** — Same layout, intro: "{Name}, here's your {Carrier} quote for your {vehicles}."
2. **Your Quote** — Single centered card (max-width:28rem, margin:auto) with carrier logo, coverage checklist, payment breakdown, red CTA button. Daily cost card below.
3. **Your Vehicles** — Same grid with single premium column per vehicle, showing comp/collision deductible
4. **Your Drivers** — Same as Scenario A
5. **What Happens Next** — Same 3 steps
6. **Bind Form** — Carrier dropdown has only the one carrier, pre-selected
7. **Testimonial + Footer** — Same as Scenario A

**Mobile sticky CTA** — Fixed red bar at bottom (<768px):
- Scenario A: "{Best Value Carrier} — BIND NOW / ${down} DOWN"
- Scenario B: "Full Coverage — BIND NOW / ${down} DOWN"
- Scenario C: "{Carrier} — BIND NOW / ${down} DOWN"

**Includes**: OG meta tags, Schema.org JSON-LD, smooth scroll, form with Google Sheets placeholder + mailto fallback

### Step 6: Save the file
Save to: `C:\Users\bill\My Drive (Bill@billlayneinsurance.com)\Client Folders\{Client Name}\Bill-Layne-Quote-{FirstName}-{LastName}-v3.html`

Create the client folder if it doesn't exist.

### Step 7: Preview and verify
Copy the file to the worktree as `preview-quote.html`, start the dev server with `preview_start`, and take a screenshot to show the user the result. Verify:
- Logo visible and properly sized
- Card(s) render with correct numbers
- Daily cost shows correct $/day
- Vehicle cards show all vehicles with per-option premiums and deductibles
- Driver cards show all drivers with clean record / incidents badges
- Form pre-fills correctly
- Mobile sticky CTA present
- Social links visible in footer (not hidden behind sticky CTA on mobile)

Tell the user: "Quote page saved to {path}. Upload to tiiny.host and text the link to {client name}."

### Reference templates
- **Scenario B (with vehicles + drivers sections):** `C:\Users\bill\My Drive (Bill@billlayneinsurance.com)\Client Folders\THOMAS DEBOYACE\Bill-Layne-Quote-Thomas-Deboyace-v3.html`
- **Scenario A (carrier vs carrier):** `C:\Users\bill\My Drive (Bill@billlayneinsurance.com)\Client Folders\Tremayne Buchanon\Bill-Layne-Quote-Tremayne-Buchanon-v3.html` (note: does not have vehicles/drivers sections — use Deboyace as primary reference)
