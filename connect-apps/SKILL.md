---
name: connect-apps
description: "Manage CompliCore external app integrations: PMS providers (Guesty, Hostaway, Lodgify, Beds24, Hostfully), OTA channels (Airbnb, VRBO, Booking.com), payment processors (Stripe, PayPal), smart locks (August, Schlage, Yale), accounting (QuickBooks, Xero), and insurance (Superhog). Actions: list, connect, disconnect, sync, check env vars, diagnose errors. Uses the connect-apps-plugin MCP server."
---

# Connect Apps — CompliCore Integration Skill

Manage external application integrations for the CompliCore rental platform. This skill provides context and instructions for working with the **connect-apps-plugin** MCP server located at `connect-apps-plugin/`.

## When to Apply

Use this skill when the user asks about:
- Connecting, disconnecting, or configuring external apps
- Syncing data with PMS, OTA, payment, smart-lock, or accounting systems
- Checking environment variables or credentials for integrations
- Diagnosing sync errors or connection issues
- Listing available connectors and their status

## Architecture

```
connect-apps-plugin/
├── mcp.json           # MCP server manifest
├── package.json       # Dependencies (@modelcontextprotocol/sdk, zod)
├── tsconfig.json      # TypeScript config (ES2022, ESNext modules)
├── src/
│   └── index.ts       # MCP server with 7 tools (864 lines)
└── dist/              # Compiled output (after npm run build)
```

**Runtime:** Node.js ≥ 20, TypeScript, MCP stdio transport
**Launch:** `claude --plugin-dir ./connect-apps-plugin`

## Connector Registry

| ID | Name | Category | Auth | Required Env Vars |
|----|------|----------|------|-------------------|
| `guesty` | Guesty | pms | OAuth | `GUESTY_CLIENT_ID`, `GUESTY_CLIENT_SECRET` |
| `hostaway` | Hostaway | pms | API Key | `HOSTAWAY_API_KEY`, `HOSTAWAY_ACCOUNT_ID` |
| `lodgify` | Lodgify | pms | API Key | `LODGIFY_API_KEY` |
| `beds24` | Beds24 | pms | API Key | `BEDS24_PROP_KEY`, `BEDS24_API_KEY` |
| `hostfully` | Hostfully | pms | OAuth | `HOSTFULLY_CLIENT_ID`, `HOSTFULLY_CLIENT_SECRET` |
| `airbnb` | Airbnb | ota | OAuth | `AIRBNB_CLIENT_ID`, `AIRBNB_CLIENT_SECRET` |
| `vrbo` | VRBO | ota | API Key | `VRBO_API_KEY`, `VRBO_ADVERTISER_ID` |
| `booking-com` | Booking.com | ota | API Key | `BOOKINGCOM_API_KEY`, `BOOKINGCOM_HOTEL_ID` |
| `stripe` | Stripe | payment | API Key | `STRIPE_SECRET_KEY`, `STRIPE_PUBLISHABLE_KEY`, `STRIPE_WEBHOOK_SECRET` |
| `paypal` | PayPal | payment | OAuth | `PAYPAL_CLIENT_ID`, `PAYPAL_CLIENT_SECRET` |
| `august` | August Smart Lock | smart-lock | OAuth | `AUGUST_CLIENT_ID`, `AUGUST_CLIENT_SECRET` |
| `schlage` | Schlage Encode | smart-lock | API Key | `SCHLAGE_API_KEY` |
| `yale` | Yale Access | smart-lock | OAuth | `YALE_CLIENT_ID`, `YALE_CLIENT_SECRET` |
| `quickbooks` | QuickBooks Online | accounting | OAuth | `QUICKBOOKS_CLIENT_ID`, `QUICKBOOKS_CLIENT_SECRET` |
| `xero` | Xero | accounting | OAuth | `XERO_CLIENT_ID`, `XERO_CLIENT_SECRET` |
| `superhog` | Superhog | insurance | API Key | `SUPERHOG_API_KEY`, `SUPERHOG_HOST_ID` |

## MCP Tools Reference

### `list_connectors`
List all connectors, optionally filtered by category or status.
- **category** (optional): `pms` | `ota` | `payment` | `smart-lock` | `accounting` | `insurance`
- **status** (optional): `connected` | `disconnected` | `error` | `configured`

### `get_connector`
Get details for a specific connector including env vars and sync history.
- **connectorId** (required): Connector ID string (e.g. `guesty`, `stripe`)

### `connect_app`
Activate a connection with credentials.
- **connectorId** (required): Connector ID
- **apiKey** (optional): For API-key connectors
- **oauthCode** (optional): For OAuth connectors
- **webhookUrl** (optional): Webhook endpoint to register

### `disconnect_app`
Disconnect and revoke credentials.
- **connectorId** (required): Connector ID

### `trigger_sync`
Trigger a data sync with a connected app.
- **connectorId** (required): Connector ID
- **syncType** (optional, default `full`): `full` | `listings` | `bookings` | `availability` | `pricing` | `payouts`

### `get_sync_history`
View recent sync history.
- **connectorId** (optional): Filter by connector
- **limit** (optional, default 20): Max records (1–100)

### `check_env_vars`
Check which required env vars are set vs missing for a connector. Does not expose secret values.
- **connectorId** (required): Connector ID

## Workflow Patterns

### First-Time Setup
1. `list_connectors` — see what's available
2. `check_env_vars` with target connector — verify credentials are configured
3. `connect_app` with credentials — activate the connection
4. `trigger_sync` with `syncType: "full"` — pull initial data
5. `get_sync_history` — verify the sync completed

### Diagnose a Failing Connector
1. `get_connector` — check status and recent sync errors
2. `check_env_vars` — look for missing credentials
3. If status is `error`, `disconnect_app` then `connect_app` to re-auth
4. `trigger_sync` — test with a fresh sync

### Daily Operations
- `list_connectors` with `status: "error"` — find broken connections
- `get_sync_history` with `limit: 5` — check recent activity
- `trigger_sync` with `syncType: "availability"` — quick calendar sync

## Development

```bash
cd connect-apps-plugin
npm install          # Install deps
npm run build        # Compile TypeScript → dist/
npm run dev          # Run with tsx (hot-reload)
npm start            # Run compiled output
```

### Adding a New Connector
1. Add entry to the `connectors` array in `src/index.ts`
2. Define: `id`, `name`, `category`, `authType`, `status`, `docsUrl`, `description`, `requiredEnvVars`
3. Rebuild: `npm run build`

### Key Types
```typescript
type ConnectorCategory = "pms" | "ota" | "payment" | "smart-lock" | "accounting" | "insurance";
type ConnectorStatus = "connected" | "disconnected" | "error" | "configured";
interface AppConnector {
  id: string; name: string; category: ConnectorCategory;
  authType: "oauth" | "apiKey" | "webhook";
  status: ConnectorStatus; docsUrl: string;
  description: string; requiredEnvVars: string[];
}
```

## Related Files
- `connect-apps-plugin/src/index.ts` — Full MCP server implementation
- `connect-apps-plugin/mcp.json` — Server manifest
- `AGENTS.md` — LodgingOrchestrator agent manifesto (references settlement contracts)
- `contracts/ComplicoreInstantSettlement.sol` — Settlement smart contract
- `backend/src/routes/` — Backend API routes that consume synced data
