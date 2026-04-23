---
name: metlife-pets
description: This skill should be used when the user asks to query MetLife Pet Insurance, check pet insurance claims, list claims, get claim details, download EOBs, download policy documents, or interact with the mypets.metlife.com API.
argument-hint: "<action> [policy <policyId>] [pet <petId>] [claim <claimId>]"
---

# MetLife Pet Insurance API

You are a helper for interacting with the MetLife Pet Insurance API.

## Authentication

Authentication is handled by `metlife.sh` in the repo root. It supports:
- **Programmatic login** with username/password (2-step: login + profileDevice, with MFA support)
- **MFA handling** via email OTP (deliverOtpToDevice + VerifyOtp)
- **Automatic token refresh** using the refresh token (~15 min access token TTL)
- **Token persistence** across shell sessions via `.metlife-cache/.token`
- **Proactive refresh** before token expiry (120s buffer)

### First-time setup / expired session

If `ensure_auth` returns `AUTH_NEEDED`, ask the user for their MetLife login credentials:

> "I need to log into your MetLife account. What's your email and password for mypets.metlife.com?"

Then call:
```bash
source metlife.sh
LOGIN_RESULT=$(metlife_login "user@email.com" "their_password")
```

**If login returns `MFA_OTP_SENT` (exit code 2):** MetLife requires email verification. Ask the user to check their email for a verification code, then call:
```bash
source metlife.sh
metlife_verify_otp "123456"
```

**If login completes without MFA:** Tokens are saved automatically.

**Important (zsh compatibility):** Always run metlife.sh with `bash` or ensure the calling shell is bash. The script uses bash-specific features and avoids zsh reserved variable names.

### Every Bash call

**Always source `metlife.sh` and call `ensure_auth`** at the top of every Bash tool invocation:
```bash
cd /path/to/claude-metlife
source metlife.sh
AUTH_RESULT=$(ensure_auth)
if [ "$AUTH_RESULT" = "AUTH_NEEDED" ]; then
  echo "AUTH_NEEDED"
  exit 0
fi
```

If `AUTH_NEEDED` is returned, stop and ask the user for credentials. Do not proceed with API calls.

## Two API Gateways

MetLife uses two separate API gateways. The helper script handles headers for each automatically.

### Azure APIM (`apis.metlife.com`) — pets, policies, rewards
Use `metlife_apim` for these endpoints:

| Endpoint | Description |
|----------|-------------|
| `GET $APIM_BASE/pets` | List all pets |
| `GET $APIM_BASE/pets/{petId}/profile` | Pet profile details |
| `GET $APIM_BASE/pets/{petId}/profileImage` | Pet profile image (base64 JPEG) |
| `GET $APIM_BASE/policies` | List all policies |
| `GET $APIM_BASE/policies/{policyId}` | Policy details |
| `GET $APIM_BASE/rewards/active` | Active rewards |
| `GET $APIM_BASE/rewards/isAvailable` | Rewards availability |

### IBM API Connect (`api.metlife.com`) — claims, customer, payments
Use `metlife_ibm` for these endpoints:

| Endpoint | Description |
|----------|-------------|
| `GET $IBM_BASE/cl/v1/claim/all?petId={petId}&policyId={policyId}` | List all claims (pass `policyId=` empty for all policies) |
| `GET $IBM_BASE/cl/v1/incident/{claimSourceId}/{claimId}/incidents` | Claim incidents (line-item groups per pet/condition; `claimSourceId` is typically `1`) |
| `GET $IBM_BASE/cl/v1/incident/{incidentId}/lineItems` | Incident line items (individual charges, denial reasons, exception messages) |
| `GET $IBM_BASE/cl/v1/document-details?policyId={policyId}&claimSourceId=1&claimId={claimId}` | List claim documents (EOBs and submitted docs) |
| `GET $IBM_BASE/cl/v1/document-details?..&isBlobRequest=true&filePath={filePath}&claimDocumentType=2` | Download submitted docs (invoices, SOAP notes) |
| `GET $IBM_BASE/cl/v1/document-details?..&isBlobRequest=true&filePath={filePath}&claimDocumentType=1` | Download EOB |
| `GET $IBM_BASE/p/v1/policy/{policyId}/policyPacket` | Policy packet PDF (binary response, save directly) |
| `GET $IBM_BASE/cu/v1/customer/details` | Customer profile |

You can also use `metlife_api` which auto-routes to the correct gateway based on the URL.

## Document Downloads

### Submitted documents (invoices, SOAP notes)
The `filePath` comes from the `docDetails` array in the document list response. Use `claimDocumentType=1` (not 2). The response may return the document in either `docDetails[].document` or `eobDetails[].eobDocument` -- check both fields.

**If a download returns null**, try the other `claimDocumentType` and try both petIds on the policy. The API is inconsistent -- some documents only download with a specific petId even if tagged for multiple pets. URL-encode filePaths with spaces.
```bash
RESPONSE=$(metlife_ibm "$IBM_BASE/cl/v1/document-details?policyId=$POLICY&claimId=$CLAIM&petId=$PET&isBlobRequest=true&filePath=$FILE_PATH&claimDocumentType=1")
echo "$RESPONSE" | python3 -c "
import sys,json,base64
d=json.load(sys.stdin)
m=d.get('model',{})
for e in (m.get('eobDetails') or []):
    if e.get('eobDocument'):
        open('output.pdf','wb').write(base64.b64decode(e['eobDocument'])); break
else:
    for doc in (m.get('docDetails') or []):
        if doc.get('document'):
            open('output.pdf','wb').write(base64.b64decode(doc['document'])); break
"
```

### EOBs (Explanation of Benefits)
The `filePath` comes from the `eobDetails` array (`eobFilePath` field). Use `claimDocumentType=1`:
```bash
RESPONSE=$(metlife_ibm "$IBM_BASE/cl/v1/document-details?policyId=$POLICY&claimId=$CLAIM&petId=$PET&isBlobRequest=true&filePath=$EOB_PATH&claimDocumentType=1")
echo "$RESPONSE" | python3 -c "import sys,json,base64; data=json.load(sys.stdin); eob=data.get('model',{}).get('eobDetails',None); [open('eob.pdf','wb').write(base64.b64decode(e['eobDocument'])) for e in (eob or []) if e.get('eobDocument')]"
```

## Local Cache

All API responses and downloaded documents are cached in `.metlife-cache/`.

### Cache structure
```
.metlife-cache/
├── .token                                  # Auth tokens (4 lines: bearer, refresh, expiry, session_id)
├── claims/
│   ├── {policyId}_{petId}_all.json         # All claims list
│   └── {claimSourceId}_{claimId}.json      # Individual claim details
├── documents/
│   ├── {policyId}_{claimId}_{petId}_list.json  # Document list
│   └── {policyId}_{claimId}_{petId}/           # Downloaded files
│       └── {filename}.pdf
└── policies/
    └── {policyId}_packet.pdf               # Policy packet
```

### Cache rules
1. **Before any API call**, check if the cached file exists. If it does, read from cache.
2. **After any successful API call**, validate the response with `is_cacheable` before writing to cache. **Never cache error responses.**
3. For JSON responses, save the raw JSON. For PDFs, save the decoded file.
4. To force a refresh, the user says "refresh" or "re-fetch" — bypass cache and overwrite.
5. Create directories as needed with `mkdir -p`.

**Caching pattern:**
```bash
CACHE_FILE=".metlife-cache/claims/${POLICY}_${PET}_all.json"
if [ -f "$CACHE_FILE" ]; then
  RESPONSE=$(cat "$CACHE_FILE")
else
  RESPONSE=$(metlife_ibm "$IBM_BASE/cl/v1/claim/all?petId=$PET&policyId=$POLICY")
  if is_cacheable "$RESPONSE"; then
    mkdir -p "$(dirname "$CACHE_FILE")"
    echo "$RESPONSE" > "$CACHE_FILE"
  else
    echo "ERROR: API call failed. Response: $RESPONSE" >&2
  fi
fi
```

## Instructions

1. **Source `metlife.sh` and call `ensure_auth`** at the top of every Bash tool call. If `AUTH_NEEDED`, ask for credentials and call `metlife_login`.
2. **Proactively call `ensure_auth`** before multi-step operations to avoid mid-operation failures.
3. **Check cache first** before making any API call.
4. **Validate before caching** — use `is_cacheable` to avoid writing error responses to cache.
5. **Use `metlife_ibm`** for claims/documents/policy endpoints, **`metlife_apim`** for pets/policies list/rewards, or just **`metlife_api`** (auto-routes).
6. **Parse JSON responses** and present data in readable format (tables, summaries).
7. **For document/PDF downloads**, save to the cache directory and tell the user the path.
8. **If login fails**, it may be due to ThreatMetrix device profiling. Tell the user: "Automated login didn't work — MetLife's fraud detection may have blocked it. You can try again, or paste a Bearer token from DevTools as a fallback." To set a manual token: write the bearer token as line 1 and refresh token as line 2 to `.metlife-cache/.token`.

## First-Run Sync

When the user first provides their credentials (or says "sync" or "fetch everything"):

1. **Log in** if not already authenticated.
2. **Fetch all pets** via `metlife_apim "$APIM_BASE/pets"` — get pet IDs and names.
3. **Fetch all policies** via `metlife_apim "$APIM_BASE/policies"` — get policy IDs.
4. **Fetch all claims** for each pet/policy combo. Cache the response.
5. **For each claim**, fetch claim details and document list. Cache each one.
6. **Download every document** (EOBs, invoices, SOAP notes) from every claim. Cache them.
7. **Download the policy packet**. Cache it.
8. Run independent fetches in parallel where possible.
9. Tell the user what was fetched and cached when done.

After sync, all reads come from cache unless the user asks to refresh.

$ARGUMENTS
