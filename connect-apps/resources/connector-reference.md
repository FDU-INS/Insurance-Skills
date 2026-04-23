# Connector Quick Reference

## Categories & Auth Types

| Category | Connectors | Typical Data Synced |
|----------|-----------|---------------------|
| **pms** | Guesty, Hostaway, Lodgify, Beds24, Hostfully | Properties, reservations, guests, calendars |
| **ota** | Airbnb, VRBO, Booking.com | Listings, bookings, availability, pricing |
| **payment** | Stripe, PayPal | Payouts, transactions, refunds |
| **smart-lock** | August, Schlage, Yale | Lock status, access codes, entry logs |
| **accounting** | QuickBooks, Xero | Revenue, expenses, invoices |
| **insurance** | Superhog | Guest verification, damage claims |

## Sync Types

| Type | Description | Typical Use |
|------|-------------|-------------|
| `full` | All data categories | Initial setup, recovery |
| `listings` | Property/listing data | After adding new properties |
| `bookings` | Reservations and guests | Hourly/daily sync |
| `availability` | Calendar and block data | High-frequency (every 15min) |
| `pricing` | Rates and pricing rules | After pricing changes |
| `payouts` | Financial transactions | Daily reconciliation |

## Status Lifecycle

```
disconnected → configured → connected → error
     ↑                          ↑         │
     └──────────────────────────┴─────────┘
                 (re-auth / disconnect)
```

- **disconnected**: No credentials, never connected
- **configured**: Env vars present, not yet activated
- **connected**: Active and syncing
- **error**: Was connected, encountered a failure (expired token, API error)

## OAuth Flow (for oauth-type connectors)

1. Redirect user to provider's authorization URL
2. User grants access → provider redirects back with `code` parameter
3. Call `connect_app` with `oauthCode` set to the received code
4. Plugin exchanges code for access/refresh tokens (stored securely)
5. Status changes to `connected`

## API Key Flow (for apiKey-type connectors)

1. User generates API key from provider's dashboard
2. Set the key in the appropriate env var (see SKILL.md registry table)
3. Call `connect_app` with `apiKey` parameter
4. Status changes to `connected`
