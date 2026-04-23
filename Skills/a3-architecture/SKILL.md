---
name: a3-architecture
description: Complete architecture reference for the A3 insurance platform — file locations, data flow, conventions, microservice map, and fullstack patterns
version: 0.1.0
---

# A3 Platform Architecture Reference

## Overview

A3 is a full-featured SaaS platform for insurance agent management built by Trusted American Insurance Agency. It provides CRM, enrollment management, commission tracking, compliance tools, and agent support.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Ember.js 6.9 (Octane) with TypeScript, Glimmer GTS components |
| Build | Vite + Embroider |
| Styling | Tailwind CSS 4 + Bootstrap 5 |
| State | WarpDrive (next-gen Ember Data) |
| Database | Cloud Firestore (NoSQL) |
| Realtime DB | Firebase Realtime Database (status tracking) |
| File Storage | Google Cloud Storage |
| Auth | Firebase Authentication + ember-simple-auth |
| Backend | Google Cloud Functions (Node.js 22, TypeScript) |
| Search | Algolia |
| Payments | Stripe |
| Email | Mailgun |
| Documents | PandaDoc |
| CRM Sync | HubSpot, Salesforce |
| Error Tracking | Sentry |
| Customer Support | Intercom |
| State Machines | XState 5 |
| Charts | Highcharts 12 |
| Maps | Google Maps |
| Deployment | Netlify (frontend), GCP (backend) |
| IaC | Terraform |

## Directory Structure

```
A3/
├── app/                          # Ember.js frontend application
│   ├── abilities/     (101)      # ember-can permission definitions
│   ├── adapters/      (11)       # Data source adapters
│   ├── builders/      (2)        # API call builders
│   ├── components/    (436)      # Glimmer GTS components
│   ├── config/        (5)        # App configuration
│   ├── controllers/   (varies)   # Controllers (only for query params)
│   ├── handlers/      (2)        # Request handlers
│   ├── helpers/       (2)        # Template helpers
│   ├── models/        (136)      # Ember Data models
│   ├── modifiers/     (1)        # DOM modifiers
│   ├── routes/        (333)      # Route definitions
│   ├── serializers/   (16)       # Data serializers
│   ├── services/      (12)       # Application services
│   ├── session-stores/(1)        # Auth session storage
│   ├── styles/        (1)        # Tailwind CSS entry point
│   ├── templates/     (158)      # GTS route templates
│   ├── transforms/    (5)        # Attribute transforms
│   └── utils/         (19)       # Utility functions
├── functions/                    # Google Cloud Functions backend
│   ├── src/
│   │   ├── auth/                 # Auth triggers
│   │   ├── database/             # Realtime DB triggers
│   │   ├── firestore/            # Firestore document triggers
│   │   ├── https/                # HTTPS endpoints
│   │   ├── pubsub/               # Pub/Sub triggers
│   │   ├── storage/              # Cloud Storage triggers
│   │   ├── models/               # TypeScript interfaces
│   │   ├── types/                # Type definitions
│   │   └── utils/                # Shared utilities
│   └── lib/                      # Compiled output
├── tests/                        # Test suites (807 files)
│   ├── acceptance/               # User flow tests
│   ├── integration/              # Component tests
│   └── unit/                     # Logic tests
├── translations/                 # i18n files
├── types/                        # Global TypeScript types
├── algolia/                      # Algolia search config
├── terraform/                    # Infrastructure as Code
├── emulator-data/                # Firebase emulator snapshots
├── config/                       # Ember.js config
├── docs/                         # Documentation
└── public/                       # Static assets
```

## Data Flow Architecture

### Read Flow (Frontend → Firestore)
```
User visits route
  → Route.model() calls store.query() or store.findRecord()
    → WarpDrive Store dispatches to adapter
      → CloudFirestoreAdapter reads from Firestore
        → CloudFirestoreSerializer normalizes response
          → Store caches record
            → GTS template renders via @model
              → Glimmer component displays data
```

### Write Flow (Frontend → Firestore → Triggers)
```
User submits form
  → Component @action or ember-concurrency task
    → model.save() via WarpDrive Store
      → CloudFirestoreAdapter writes to Firestore
        → Firestore document created/updated
          → Cloud Function trigger fires
            → Side effects: email, Algolia sync, audit trail, webhooks
              → Real-time listener updates frontend Store
                → Component re-renders with updated data
```

### Third-Party Integration Flow
```
Frontend component → REST adapter (adapter/firebase.ts)
  → Cloud Function HTTPS endpoint
    → Third-party API (Stripe, Mailgun, PandaDoc, etc.)
      → Response → Firestore document update
        → Real-time listener → Frontend update
```

## Domain Model Map

### Core Entities
- **Agency** — Insurance agency (primary organizational unit)
- **User** — Platform user (agent, admin, super admin)
- **Client** — Contact/person being insured
- **Carrier** — Insurance carrier company

### Business Entities
- **Enrollment** — Insurance enrollment record
- **Contract** — Agent-carrier contract
- **Group** — Group insurance plan
- **Quote** — Insurance quote
- **Membership** — Client membership

### Financial
- **Statement** — Commission statement
- **Transaction** — Financial transaction

### Communication
- **Activity** — Audit trail / activity log
- **Message** — Internal messaging
- **Ticket** — Support ticket
- **Inquiry** — Lead inquiry

### Associations
- **Affiliation** — Agent-agency relationship
- **License** — Agent license record
- **Event** — Calendar/marketing event

### Attachment Patterns
Most entities have associated:
- `*-file` — File attachments (stored in Cloud Storage)
- `*-note` — Text notes
- `activity` — Audit trail entries

## Route Map

### Public Routes
| Route | Purpose |
|-------|---------|
| `/login` | User authentication |
| `/register` | New user registration |
| `/reset` | Password reset |
| `/onboarding` | Post-registration setup |
| `/client/:id` | Public client profile |
| `/client-form/:id` | Public client form |
| `/order/:id` | Order page |
| `/session` | Session management |

### Authenticated Routes (`/a3/...`)
| Route | Purpose |
|-------|---------|
| `/a3` | Dashboard |
| `/a3/clients` | Client (contact) management |
| `/a3/enrollments` | Enrollment management |
| `/a3/groups` | Group management |
| `/a3/agencies` | Agency management |
| `/a3/carriers` | Carrier information |
| `/a3/contracting` | Contract management |
| `/a3/statements` | Commission statements |
| `/a3/settings` | User settings |
| `/a3/tools` | Quote tools |
| `/a3/calendar` | Calendar |
| `/a3/leads` | Lead management |
| `/a3/notifications` | Notifications |
| `/a3/search` | Global search |
| `/a3/support` | Support tickets |
| `/a3/resources` | Resources |
| `/a3/knowledge-hub` | Knowledge base |
| `/a3/marketing-events` | Marketing events |
| `/a3/readiness-report` | Readiness report |
| `/a3/services` | Services (websites) |

### Admin Routes (`/admin/...`)
| Route | Purpose |
|-------|---------|
| `/admin/accounting` | Financial management |
| `/admin/agencies` | Agency administration |
| `/admin/carriers` | Carrier management |
| `/admin/clients` | Client administration |
| `/admin/contracting` | Contract admin |
| `/admin/enrollments` | Enrollment admin |
| `/admin/enrollment-issues` | Issue tracking |
| `/admin/events` | Event management |
| `/admin/groups` | Group admin |
| `/admin/inquiries` | Lead/inquiry management |
| `/admin/marketing` | Marketing tools |
| `/admin/messages` | Messaging |
| `/admin/notifications` | Notification management |
| `/admin/products` | Product management |
| `/admin/reporting` | Reports |
| `/admin/search` | Admin search |
| `/admin/settings` | System settings |
| `/admin/tickets` | Support ticket admin |
| `/admin/users` | User management |

## Service Map

| Service | File | Purpose |
|---------|------|---------|
| `store` | `app/services/store.ts` | WarpDrive data store with custom aggregation methods |
| `session` | `app/services/session.ts` | Firebase Auth + MFA + ember-simple-auth |
| `current-user` | `app/services/current-user.ts` | Loaded user data and permissions |
| `search` | `app/services/search.ts` | Algolia search integration |
| `pdf` | `app/services/pdf.ts` | PDF generation/manipulation |
| `csv` | `app/services/csv.ts` | CSV export |
| `xlsx` | `app/services/xlsx.ts` | Excel export |
| `analytics` | `app/services/analytics.ts` | Event tracking |
| `tour` | `app/services/tour.ts` | Shepherd.js onboarding tour |
| `recent-records` | `app/services/recent-records.ts` | Recently viewed record tracking |

## Key Configuration Files

| File | Purpose |
|------|---------|
| `app/config/environment.js` | Firebase config, API endpoints, feature flags |
| `firebase.json` | Firebase project config, emulator settings |
| `firestore.rules` | Firestore security rules (~101KB) |
| `firestore.indexes.json` | Composite indexes (~235KB) |
| `storage.rules` | Cloud Storage security rules |
| `database.rules.json` | Realtime Database rules |
| `ember-cli-build.js` | Build config (Embroider, split routes) |
| `vite.config.mjs` | Vite build config (Tailwind, PWA) |
| `app/router.ts` | Route definitions |
| `tsconfig.json` | TypeScript configuration |
| `netlify.toml` | Netlify deployment config |

## Development Environment

- **Frontend dev**: `ember serve` or `vite dev`
- **Backend dev**: Firebase Emulator Suite (auth, firestore, functions, storage, pubsub)
- **Emulator data**: `emulator-data/` contains snapshots for seeding
- **Tests**: `ember test` (runs in browser via testem)
- **Linting**: ESLint, Prettier, Stylelint, ember-template-lint

## Further Investigation Links

When you need deeper knowledge about specific areas:

- **Ember.js**: https://guides.emberjs.com/release/
- **Glimmer Components**: https://guides.emberjs.com/release/components/
- **WarpDrive/Ember Data**: https://api.emberjs.com/ember-data/release
- **Firestore**: https://firebase.google.com/docs/firestore
- **Cloud Functions**: https://firebase.google.com/docs/functions
- **Tailwind CSS**: https://tailwindcss.com/docs
- **ember-cloud-firestore-adapter**: https://github.com/nickersk/ember-cloud-firestore-adapter
- **ember-simple-auth**: https://ember-simple-auth.com/
- **ember-can**: https://github.com/minutebase/ember-can
- **ember-concurrency**: https://ember-concurrency.com/
- **XState**: https://stately.ai/docs
