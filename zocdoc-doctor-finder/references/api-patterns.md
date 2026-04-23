# Zocdoc API Patterns

Extract provider data using two approaches — Redux state (preferred for search results) and GraphQL API (for availability). No authentication required.

## Approach 1: Redux State Extraction (Recommended for Search Results)

After navigating to a search results page, extract structured data from `window.__REDUX_STATE__`:

```javascript
// Full search results with provider details
window.__REDUX_STATE__.searchResults.search.searchResponse.providerLocations

// Search parameters
window.__REDUX_STATE__.search.parameters

// Availability data (after GQL loads)
window.__REDUX_STATE__.timesgrid
```

### Provider Location Object Structure

Each item in `providerLocations` contains:

```json
{
  "id": "pr_xxx|lo_xxx",           // providerLocation composite ID
  "provider": {
    "id": "pr_xxx",
    "monolithId": "651573",         // Numeric ID used in profile URLs
    "approvedFullName": "Dr. Nithin Charlly, MD",
    "averageRating": 4.93,
    "averageBedsideRating": 4.97,
    "averageWaitTimeRating": 4.91,
    "firstName": "Nithin",
    "lastName": "Charlly",
    "postnominal": "MD",
    "prenominal": "Dr.",
    "profileUrl": "/doctor/nithin-charlly-md-651573",
    "relevantSpecialty": { "id": "153", "name": "Primary Care Doctor" },
    "reviewCount": 95,
    "procedures": [{ "id": "75" }, ...],
    "badges": [...],                // Highly recommended, Patient Choice, etc.
    "frontEndCirclePictureUrl": "//d2uur722ua7fvv.cloudfront.net/photos/...",
    "canHaveAppointments": true
  },
  "location": {
    "id": "lo_xxx",
    "monolithId": "274383",
    "address": "1253 N Milwaukee Ave",
    "cityName": "Chicago",
    "stateName": "IL",
    "zip": "60622",
    "phone": "...",
    "isVirtual": false,
    "distanceMiles": 2.4
  },
  "spoData": { ... }               // Sponsored ad data (if sponsored result)
}
```

### JavaScript to Extract Clean Results

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

## Approach 2: GraphQL API (For Availability Data)

Call `https://api.zocdoc.com/directory/v3/gql` for real-time availability. No auth required — uses the browser's session.

### Availability Query

**Endpoint:** `POST https://api.zocdoc.com/directory/v3/gql`

**Operation:** `providerLocationsAvailability`

```json
{
  "operationName": "providerLocationsAvailability",
  "variables": {
    "directoryId": "-1",
    "insurancePlanId": "-1",
    "isNewPatient": true,
    "numDays": 13,
    "procedureId": "75",
    "searchRequestId": "<from search response>",
    "startDate": "2026-03-02",
    "timeFilter": "AnyTime",
    "providerLocationIds": ["pr_xxx|lo_xxx", ...]
  },
  "query": "query providerLocationsAvailability($directoryId: String, $insurancePlanId: String, $isNewPatient: Boolean, $isReschedule: Boolean, $jumpAhead: Boolean, $firstAvailabilityMaxDays: Int, $numDays: Int, $procedureId: String, $providerLocationIds: [String], $searchRequestId: String, $startDate: String, $timeFilter: TimeFilter, $widget: Boolean) { providerLocations(ids: $providerLocationIds) { id ...availability __typename } } fragment availability on ProviderLocation { id provider { id monolithId __typename } location { id monolithId state phone isVirtual __typename } availability(directoryId: $directoryId, insurancePlanId: $insurancePlanId, isNewPatient: $isNewPatient, isReschedule: $isReschedule, jumpAhead: $jumpAhead, firstAvailabilityMaxDays: $firstAvailabilityMaxDays, numDays: $numDays, procedureId: $procedureId, searchRequestId: $searchRequestId, startDate: $startDate, timeFilter: $timeFilter, widget: $widget) { times { date timeslots { isResource isResourceFullProfile performingProviderId startTime __typename } __typename } firstAvailability { startTime __typename } timesgridId today __typename } __typename }"
}
```

### Response Structure

```json
{
  "data": {
    "providerLocations": [
      {
        "id": "pr_xxx|lo_xxx",
        "availability": {
          "times": [
            {
              "date": "2026-02-18",
              "timeslots": [
                { "startTime": "2026-02-18T09:00:00", "isResource": false },
                { "startTime": "2026-02-18T09:30:00", "isResource": false }
              ]
            }
          ],
          "firstAvailability": { "startTime": "2026-02-18T09:00:00" },
          "today": "2026-02-17"
        }
      }
    ]
  }
}
```

### TimeFilter Enum Values

- `AnyTime`
- `Morning` (before 12pm)
- `Afternoon` (12pm-5pm)
- `Evening` (after 5pm)

### GQL Endpoints

| Endpoint | Purpose |
|----------|---------|
| `api.zocdoc.com/directory/v3/gql` | Search results, provider data, availability — use this one |
| `api2.zocdoc.com/user/v1/gql` | User session/auth — requires login, do not use |

## Extracting Availability via JavaScript (Simpler)

Instead of calling GQL directly, extract availability from the Redux timesgrid state after the page renders:

```javascript
(() => {
  const tg = window.__REDUX_STATE__?.timesgrid;
  if (!tg) return JSON.stringify({error: 'no timesgrid'});
  return JSON.stringify(tg).substring(0, 5000);
})()
```

Alternatively, read the availability grid directly from the DOM — dates and appointment counts are visible per provider.

## Notes

- No auth tokens needed — all data is publicly accessible from the rendered page
- Get `searchRequestId` from the initial search response in Redux state
- Provider location IDs are composite: `provider_id|location_id`
- The GQL endpoint uses the browser's cookies/session — do not add separate auth headers
- Avoid rapid successive calls — rate limiting may apply
