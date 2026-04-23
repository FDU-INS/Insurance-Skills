---
name: zocdoc-doctor-finder
description: Use when a user needs to find a doctor, dentist, specialist, therapist, or healthcare provider — especially when they mention insurance, in-network, availability, location, appointments, or booking. Also use for browsing provider reviews, comparing doctors by specialty, or checking if a provider takes their insurance.
compatibility: Requires browser access (e.g., computer use or browser automation tool)
---

# Zocdoc Doctor Finder

## Overview

Find in-network healthcare providers with real-time availability on Zocdoc.com using browser automation. Extract data from Zocdoc's Redux store and GraphQL API — no authentication required.

## Browser Requirements

This skill requires the user's **real browser session** — not a headless browser, fresh profile, or isolated automation context. Use the browser the user already has open, with their existing cookies, history, and login state. A clean profile with no browsing history is more likely to trigger bot detection.

**Pacing:** Wait for each page to fully load before taking the next action. Do not rapid-fire navigate between pages. A 2-3 second pause between actions mimics normal browsing and reduces bot detection risk.

**Two interaction modes exist:**

| Mode | Can run console JS? | How to extract data |
|------|-------------------|-------------------|
| **Programmatic** (Playwright, Puppeteer) | Yes | Redux state extraction (preferred) |
| **Computer use** (screen-based agent) | No | Read data directly from the visible page |

Both modes follow the same workflow — the only difference is *how* you extract data at each step. Instructions for both are included below.

## When to Use

- User asks to find a doctor, dentist, or specialist
- User mentions insurance and wants to know who's in-network
- User wants to check appointment availability or book a visit
- User wants to compare providers by rating, distance, or reviews
- User asks about a specific provider on Zocdoc

**When NOT to use:**
- User wants to interact with Zocdoc's programmatic/partner API
- User needs providers outside the US (Zocdoc is US-only)
- User wants to complete the booking transaction (requires auth + PHI)

## Workflow

### 1. Gather Requirements

Collect from the user (ask only what's missing — infer from context when possible):

- **What they need**: specialty, condition, or procedure (e.g., "dermatologist", "back pain", "annual physical")
- **Location**: city/state, zip code, or address
- **Insurance** (optional but high-value): carrier + plan name
- **Preferences** (optional): time of day, virtual vs in-person, language, gender, urgency ("soon as possible")

If the user is vague ("I need a doctor"), ask one focused question: "What kind of doctor, and where are you located?"

**Agent tips:**
- Always ask about insurance if not provided — it's the #1 factor that determines which doctors appear
- If the user names a condition ("my knee hurts") rather than a specialty, do not guess the specialty — use the homepage search autocomplete in step 2
- Infer location from prior conversation context before asking (e.g., user previously mentioned "I live in Brooklyn")
- Don't ask for all fields upfront — specialty + location is enough to start; refine with filters after showing initial results

### 2. Construct Search URL

Build a Zocdoc search URL. See [references/url-patterns.md](references/url-patterns.md) for full parameter documentation.

**Quick reference — search URL structure:**

```
https://www.zocdoc.com/search?
  address=<City,+State+or+Zip>
  &dr_specialty=<specialty_id>
  &insurance_carrier=<carrier_name>
  &insurance_plan=<plan_id>
  &day_filter=<AnyDay|Today|Tomorrow|NextWeek>
  &sort_type=Default
  &visitType=<inPersonAndVirtualVisits|virtualVisits|inPersonVisits>
  &after_5pm=<true|false>
  &before_10am=<true|false>
  &gender=<-1|1|2>
  &language=<language_id|-1>
  &offset=<page_number>
```

Common specialty IDs: Primary Care = `153`, Dentist = `98`, Dermatologist = `105`, OB-GYN = `133`, Psychiatrist = `319`, Eye Doctor = `113`, Urgent Care = `702`.

For a complete specialty list, see [references/url-patterns.md](references/url-patterns.md).

If the specialty ID is unknown, use the homepage search: navigate to `zocdoc.com`, type the specialty/condition in the search combobox, and select from autocomplete suggestions.

### 3. Navigate and Parse Results

1. Open the search URL in the browser.
2. If a **visit reason picker** appears ("What type of care are you looking for?"), click the "Skip to search results" button to bypass it.
3. **Extract structured data from Redux** (preferred over DOM scraping). Run this in the browser console:

```javascript
(() => {
  const sr = window.__REDUX_STATE__?.searchResults?.search?.searchResponse;
  if (!sr) return JSON.stringify({error: 'no results'});
  return JSON.stringify(sr.providerLocations.map(pl => ({
    name: pl.provider.approvedFullName,
    rating: pl.provider.averageRating,
    reviewCount: pl.provider.reviewCount,
    specialty: pl.provider.relevantSpecialty?.name,
    profileUrl: 'https://www.zocdoc.com' + pl.provider.profileUrl,
    address: [pl.location.address, pl.location.cityName, pl.location.stateName, pl.location.zip].filter(Boolean).join(', '),
    distance: pl.location.distanceMiles,
    isVirtual: pl.location.isVirtual,
    isSponsored: !!pl.spoData?.adDecisionId,
    badges: pl.provider.badges?.map(b => b.displayText) || []
  })), null, 2);
})()
```

This returns clean JSON from the Redux store — much more reliable than parsing the DOM.

4. **Computer-use alternative**: If you cannot run JavaScript (screen-based agent), read the search results directly from the visible page. Each result card shows:
   - Provider name and credentials (header of each card)
   - Star rating and review count (below the name)
   - Address and distance (below rating)
   - Badges like "Highly Recommended" (if present)
   - Availability preview (date/time slots on the right side of the card)
   - "Sponsored" label (top-right corner, if applicable)

   Read each card carefully and extract these fields from what is visible. **Do not infer or fabricate any field you cannot see on the page.**

5. **Fallback**: If Redux state is unavailable and you are in programmatic mode, read search results from the DOM snapshot. Each article/result card contains provider name, rating, reviews, address, badges, and availability grid.

6. Present results to the user in a clean summary. Format each provider like:

   ```
   1. **Dr. Name, MD** — ⭐ 4.96 (312 reviews) · Highly Recommended
      📍 1.2 mi — 680 N Lake Shore Dr, Chicago, IL 60611
      🗓 Next available: Tomorrow, Mar 4
      🔗 https://www.zocdoc.com/doctor/name-slug-123456

      ℹ️ Sponsored result (if applicable)
   ```

   Include for each: name + credentials, rating + review count, address + distance, notable badges, next available date, direct profile link, and whether it's a sponsored result.

**Agent tips:**
- Show 3-5 top results initially — don't dump the full list of 20. Offer "Want to see more?" if they want to browse
- Present results in the same order Zocdoc returns them, but label sponsored results so the user knows which are ads
- Highlight badges like "Highly Recommended" or "Patient Choice" — these carry weight with users
- If all results are far away (>10 miles), proactively suggest broadening the search or trying virtual visits
- Always include the review count alongside the rating — "4.9 with 200 reviews" gives users more confidence than a score alone

See [references/api-patterns.md](references/api-patterns.md) for full Redux state structure and GraphQL API details.

### 4. Drill Into a Provider (on request)

When the user wants details on a specific doctor, navigate to their profile URL and extract:

- **About**: bio, education, board certifications, languages, gender, NPI
- **Insurance**: full list of accepted plans (click "View All" to expand)
- **Availability grid**: shows dates with appointment count, navigable by week
- **Reviews**: rating breakdown (overall, wait time, bedside manner), searchable/filterable
- **Areas of expertise**: conditions/procedures they treat most

Summarize relevant sections based on what the user cares about.

**Agent tips:**
- If the user asked about insurance, lead with the insurance section — confirm their plan is accepted before anything else
- For reviews, mention the rating breakdown (wait time vs bedside manner) — not just the overall score
- If the user is comparing two doctors, present a side-by-side comparison rather than sequential descriptions

### 5. Check Specific Availability

**Option A — GQL API** (best for bulk/extended availability): Call `POST https://api.zocdoc.com/directory/v3/gql` with the `providerLocationsAvailability` operation to get exact timeslots per date. See [references/api-patterns.md](references/api-patterns.md) for the full query and response structure. Get `searchRequestId` and `providerLocationIds` from the Redux state extracted in step 3.

**Option B — DOM / visual interaction**: On the provider profile page:
- The availability grid shows dates with appointment counts
- Click a date cell to see specific time slots
- Use "Show more availability" buttons to navigate earlier/later dates
- The visit reason dropdown affects which slots appear

Report available dates/times clearly: "Dr. X has 15 appointments available on Thu Feb 19, and 19 on Thu Feb 26."

**Agent tips:**
- When reporting availability, group by week and highlight the soonest opening: "Next available: tomorrow at 9am. Also has 12 slots next week."
- If the user said "soon as possible," sort by earliest first availability, not by rating
- If a doctor has no availability in the next 2 weeks, say so and offer to check the next provider on the list

### 6. Guide to Booking

When the user is ready to book:
1. Provide the direct Zocdoc profile link
2. Tell them to click the desired time slot and follow Zocdoc's booking flow
3. Note: completing the booking requires a Zocdoc account (free signup)

**Do not attempt to complete the booking flow** — it requires authentication and personal health information.

**Agent tips:**
- Provide the direct booking start URL with pre-filled insurance and visit reason when possible (see url-patterns.md Profile URL Query Parameters)
- Remind the user: "Zocdoc signup is free and takes about 1 minute"
- If the user compared multiple doctors, briefly restate why this one stood out: "Dr. X had the highest rating and earliest availability"

## Filters

Apply these filters via the search page filter buttons:

| Filter | Options |
|--------|---------|
| Time of day | Morning, Afternoon, Evening |
| I'm flexible | Date flexibility |
| Illness | Condition-based filtering |
| Specialty | Refine specialty |
| Distance | Radius from location |
| In-person/video | Visit type |
| More filters | Gender, language, sees children, etc. |

## Data Integrity

**Only report data you actually extracted from Zocdoc.** Never present a provider name, address, phone number, rating, review count, or availability that you did not read from Zocdoc's page, Redux state, or API response. If a field is not visible or not returned, omit it — do not guess or fill in from another source.

If you used a different source (e.g., a web search), you must explicitly tell the user: "I couldn't load Zocdoc results, so these come from a general web search and may not reflect current Zocdoc availability or insurance acceptance."

## Failure Protocol

**If you cannot load Zocdoc search results — for any reason — tell the user immediately.** Do not silently switch to a web search or another data source.

Specifically:
- If the page shows a CAPTCHA, access denied, or error page: tell the user what you see and ask them to try loading the page manually
- If the page loads but results are empty or the Redux state returns no data: retry once after waiting for full page load, then report the failure
- If you are blocked or rate-limited: tell the user and suggest they try the search directly at the URL you constructed

**Never fabricate results to fill a gap.** An honest "I couldn't load results" is always better than plausible-looking data the user can't verify.

## Common Mistakes

- **Not bypassing the visit reason picker.** After navigating to a search URL, a "What type of care are you looking for?" modal often appears. You must click "Skip to search results" or results won't load and Redux state will be empty.
- **Extracting Redux state too early.** `window.__REDUX_STATE__` may not be populated on initial page load. If the extraction returns `{error: 'no results'}`, wait for the page to fully render and retry.
- **Not disclosing sponsored results.** Sponsored providers appear first and look like organic results. Always check the `isSponsored` field and tell the user which results are ads.
- **Forgetting insurance.** Insurance is the #1 filter that determines which doctors appear. Always ask if not provided.
- **Using specialty ID when condition is given.** If the user describes a condition ("back pain") rather than a specialty, use the homepage search autocomplete — Zocdoc maps conditions to the right specialties internally. Don't guess the specialty ID.
- **Navigating too fast.** Rapid page transitions trigger bot detection. Wait for each page to fully render (2-3 seconds) before taking the next action.
- **Using a fresh browser profile.** A browser with no cookies or history is more likely to be flagged. Always use the user's existing browser session.
- **Silently falling back to web search.** If Zocdoc doesn't load, tell the user. Never quietly switch data sources and present the results as if they came from Zocdoc.

## Handling Common Situations

- **User doesn't know their insurance:** Search without insurance first, then say: "I found X doctors near you. If you share your insurance, I can filter to in-network providers — this can significantly reduce your cost."
- **No results for their search:** Try these in order: (1) remove the insurance filter, (2) expand to a nearby city or broader zip, (3) try a related specialty, (4) suggest virtual visits. Tell the user what you changed.
- **User names a condition, not a specialty:** Do not guess a specialty ID. Navigate to zocdoc.com and use the search combobox autocomplete — Zocdoc maps conditions to the right provider types internally.
- **User wants to compare two doctors:** Pull both profiles and present a side-by-side comparison: rating, review count, distance, next availability, insurance acceptance, and notable badges.
- **User asks about a doctor not on Zocdoc:** Say "I couldn't find Dr. X on Zocdoc. They may not be listed. Want me to search for similar providers in the same specialty and area?"
- **User wants "the soonest available":** Sort by `firstAvailability` from the GQL response or look at the availability grid dates, not by default ranking. Tell the user: "The soonest available is Dr. X with an appointment today at 3pm."
- **Too many results, user seems overwhelmed:** Narrow by asking one targeted question: "Do you prefer someone closer to you, or with the highest rating?" Then re-filter.
- **User wants evening or weekend appointments:** Apply `after_5pm=true` or `day_filter=NextWeek` and note that weekend availability is limited for most specialties.

## Example Conversations

### Finding a specialist with insurance

```
User: I need a dermatologist in Chicago that takes Aetna.

Agent: Searching Zocdoc for dermatologists in Chicago accepting Aetna...

Here are the top results:

1. **Dr. Sarah Kim, MD** — ⭐ 4.96 (312 reviews) · Highly Recommended
   📍 1.2 mi — 680 N Lake Shore Dr, Chicago, IL 60611
   🗓 Next available: Tomorrow, Mar 4
   🔗 https://www.zocdoc.com/doctor/sarah-kim-md-234567

2. **Dr. James Chen, DO** — ⭐ 4.89 (187 reviews)
   📍 2.4 mi — 1253 N Milwaukee Ave, Chicago, IL 60622
   🗓 Next available: Thu, Mar 6
   🔗 https://www.zocdoc.com/doctor/james-chen-do-345678

3. **Dr. Maria Lopez, MD** — ⭐ 4.85 (95 reviews) · Patient Choice
   📍 3.1 mi — 150 E Huron St, Chicago, IL 60611
   🗓 Next available: Mon, Mar 9
   🔗 https://www.zocdoc.com/doctor/maria-lopez-md-456789

   ℹ️ Sponsored result

Dr. Kim has the highest rating and earliest availability. Want details on any of these, or should I check specific appointment times?

User: Tell me more about Dr. Kim. Does she have anything Thursday afternoon?

Agent: Here's Dr. Kim's profile:

**Dr. Sarah Kim, MD — Dermatologist**
⭐ 4.96 overall · 4.98 bedside manner · 4.94 wait time (312 reviews)
🎓 Northwestern Feinberg School of Medicine · Board Certified
💼 Specializes in: acne, eczema, skin cancer screening, cosmetic dermatology
✅ Accepts Aetna (confirmed)

**Thursday Mar 6 availability:**
- 1:00 PM, 1:30 PM, 2:15 PM, 3:00 PM, 3:45 PM

5 afternoon slots available. Want to book one? I'll send you the direct link.

User: The 2:15 slot.

Agent: Here's your booking link:

🔗 https://www.zocdoc.com/doctor/sarah-kim-md-234567?insuranceCarrier=Aetna&insurancePlan=-1&reason_visit=75

Click the 2:15 PM slot on Thursday Mar 6 and follow the booking flow. You'll need a Zocdoc account (free signup, takes about 1 minute). Dr. Kim was the top-rated dermatologist in your area with the earliest availability — great pick.
```

### Searching by condition (not specialty)

```
User: My back has been killing me. Who should I see near 10001?

Agent: Back pain could be treated by several specialties — let me search Zocdoc to find the right match.

Searching zocdoc.com for "back pain" near 10001...

Zocdoc suggests these provider types for back pain:
- **Orthopedic Surgeon** — for structural/joint issues
- **Pain Management Specialist** — for chronic pain treatment
- **Physical Therapist** — for rehab and exercises
- **Chiropractor** — for spinal alignment

Here are the top-rated providers for back pain near 10001:

1. **Dr. Robert Patel, MD** — Pain Management · ⭐ 4.91 (245 reviews) · Highly Recommended
   📍 0.8 mi — 317 E 34th St, New York, NY 10016
   🗓 Next available: Today, 4:30 PM
   🔗 https://www.zocdoc.com/doctor/robert-patel-md-567890

2. **Dr. Lisa Wong, MD** — Orthopedic Surgeon · ⭐ 4.87 (178 reviews)
   📍 1.1 mi — 535 E 70th St, New York, NY 10021
   🗓 Next available: Wed, Mar 5
   🔗 https://www.zocdoc.com/doctor/lisa-wong-md-678901

Do you have insurance you'd like me to filter by? That will narrow results to in-network providers.
```

### Checking availability for a known doctor

```
User: What appointments does Dr. Laurence Gordon have available next week?

Agent: Looking up Dr. Laurence Gordon on Zocdoc...

**Dr. Laurence Gordon, DO**
📍 258 Broadway, New York, NY 10007

Next week's availability:
- **Mon Mar 9:** 9:00 AM, 10:30 AM, 2:00 PM (3 slots)
- **Tue Mar 10:** 9:00 AM, 11:00 AM, 1:00 PM, 3:30 PM (4 slots)
- **Wed Mar 11:** 10:00 AM, 2:30 PM (2 slots)
- **Thu Mar 12:** No availability
- **Fri Mar 13:** 9:00 AM, 11:30 AM, 4:00 PM (3 slots)

12 total appointments next week. Tuesday has the most options. Want to book one?
```

## Quick Reference

### URLs

```
Search:    https://www.zocdoc.com/search?address={loc}&dr_specialty={id}&insurance_carrier={carrier}
Profile:   https://www.zocdoc.com/doctor/{name-slug}-{id}
GQL API:   POST https://api.zocdoc.com/directory/v3/gql
```

### Top Specialty IDs

```
153  Primary Care       98  Dentist         105  Dermatologist
133  OB-GYN            319  Psychiatrist    113  Eye Doctor
702  Urgent Care       141  Orthopedic      149  Pediatrician
 47  Cardiologist        7  ENT             117  Gastroenterologist
```

### Key URL Params

```
address          City, State or zip (URL-encoded)
dr_specialty     Specialty ID
insurance_carrier  Carrier name
insurance_plan   Plan ID (-1 = any)
day_filter       AnyDay | Today | Tomorrow | NextWeek
visitType        inPersonAndVirtualVisits | virtualVisits | inPersonVisits
sort_type        Default | Distance
offset           Page number (0-indexed)
```

### Redux Extraction

```javascript
window.__REDUX_STATE__?.searchResults?.search?.searchResponse?.providerLocations
```

### Data Flow

```
Build search URL → Navigate → Bypass visit picker → Extract Redux state → Present results
                                                   → Call GQL for availability → Report timeslots
                                                   → Navigate to profile → Extract details
```
