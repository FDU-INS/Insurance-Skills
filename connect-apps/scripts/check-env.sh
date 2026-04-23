#!/usr/bin/env bash
# connect-apps/scripts/check-env.sh — Check env vars for a connector
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <connector-id>"
  echo "Example: $0 stripe"
  exit 1
fi

CONNECTOR_ID="$1"

declare -A CONNECTOR_VARS
CONNECTOR_VARS[guesty]="GUESTY_CLIENT_ID GUESTY_CLIENT_SECRET"
CONNECTOR_VARS[hostaway]="HOSTAWAY_API_KEY HOSTAWAY_ACCOUNT_ID"
CONNECTOR_VARS[lodgify]="LODGIFY_API_KEY"
CONNECTOR_VARS[beds24]="BEDS24_PROP_KEY BEDS24_API_KEY"
CONNECTOR_VARS[hostfully]="HOSTFULLY_CLIENT_ID HOSTFULLY_CLIENT_SECRET"
CONNECTOR_VARS[airbnb]="AIRBNB_CLIENT_ID AIRBNB_CLIENT_SECRET"
CONNECTOR_VARS[vrbo]="VRBO_API_KEY VRBO_ADVERTISER_ID"
CONNECTOR_VARS[booking-com]="BOOKINGCOM_API_KEY BOOKINGCOM_HOTEL_ID"
CONNECTOR_VARS[stripe]="STRIPE_SECRET_KEY STRIPE_PUBLISHABLE_KEY STRIPE_WEBHOOK_SECRET"
CONNECTOR_VARS[paypal]="PAYPAL_CLIENT_ID PAYPAL_CLIENT_SECRET"
CONNECTOR_VARS[august]="AUGUST_CLIENT_ID AUGUST_CLIENT_SECRET"
CONNECTOR_VARS[schlage]="SCHLAGE_API_KEY"
CONNECTOR_VARS[yale]="YALE_CLIENT_ID YALE_CLIENT_SECRET"
CONNECTOR_VARS[quickbooks]="QUICKBOOKS_CLIENT_ID QUICKBOOKS_CLIENT_SECRET"
CONNECTOR_VARS[xero]="XERO_CLIENT_ID XERO_CLIENT_SECRET"
CONNECTOR_VARS[superhog]="SUPERHOG_API_KEY SUPERHOG_HOST_ID"

if [[ -z "${CONNECTOR_VARS[$CONNECTOR_ID]+x}" ]]; then
  echo "Unknown connector: $CONNECTOR_ID"
  echo "Valid IDs: ${!CONNECTOR_VARS[*]}"
  exit 1
fi

echo "Checking env vars for: $CONNECTOR_ID"
echo "---"

MISSING=0
for VAR in ${CONNECTOR_VARS[$CONNECTOR_ID]}; do
  if [[ -n "${!VAR+x}" && -n "${!VAR}" ]]; then
    echo "  ✓ $VAR — set"
  else
    echo "  ✗ $VAR — MISSING"
    MISSING=$((MISSING + 1))
  fi
done

echo "---"
if [[ $MISSING -eq 0 ]]; then
  echo "All variables set."
else
  echo "$MISSING variable(s) missing. Add them to .env or your shell environment."
  exit 1
fi
