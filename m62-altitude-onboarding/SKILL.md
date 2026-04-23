---
name: m62-altitude-onboarding
description: "Extract entity data from household document folders (PDFs, Word docs, images, spreadsheets) and update the Altitude (Altcore) platform via API. Queries Altitude first to find existing households and their universe of entities (Individuals, LegalEntities, AccountFinancials, Contacts, TangibleAssets, Households), extracts data from documents, matches and merges against existing records (filling empty fields, flagging conflicts), creates relationships, and uploads documents to the correct entity. Use this skill whenever the user mentions Altitude, Altcore, onboarding families, extracting entity data from documents, updating households, processing client folders, or uploading documents. Also trigger when the user has a folder of family documents (trusts, LLCs, tax returns, IDs, insurance, estate plans, bank statements) and wants to populate a wealth management platform."
---

# Altitude Document Extraction & Entity Update

> **⛔ CRITICAL RULE: You MUST read EVERY SINGLE FILE in the household folder. Not most files.
> Not the important-looking files. ALL files. Write a file tracker (`altitude_review/file_tracker.md`)
> listing every file. Mark each READ as you go. Do NOT proceed to Phase 4 until the tracker
> shows 100% READ. If you read 22 out of 60 files, you have failed. This is the #1 cause of
> extraction failure — see "Zero-Skip Rule" in Phase 3.**

This skill extracts entity data from household document folders and updates the Altitude
platform. It follows a query-first, match-and-merge approach — never blindly creating
entities. Every change is reviewed before pushing.

## Prerequisites

### Required Tools

This skill runs cross-platform (macOS, Linux, Windows). The following tools must be installed
and on the user's `PATH` **before** running. Verify each at the start of Step 0 with
`shutil.which(...)` and fail fast with a clear message if anything is missing — do NOT
attempt to install tooling automatically.

| Tool | Why | macOS | Linux | Windows |
|---|---|---|---|---|
| **Python 3.9+** | Script runtime for .docx/.xlsx/.eml/large PDFs | `brew install python` | `apt install python3` | `winget install Python.Python.3.12` (avoid the Microsoft Store stub — it silently redirects to a non-functional alias) |
| **pip packages** | Document parsing | `pip install pypdf python-docx openpyxl requests` | same | same |
| **qpdf** | Decrypt password-protected PDFs | `brew install qpdf` | `apt install qpdf` or `dnf install qpdf` | `winget install qpdf.qpdf` or `choco install qpdf` or `scoop install qpdf` |
| **poppler** (pdftotext) | **Text-first PDF extraction (REQUIRED, not optional)** — the default PDF read strategy uses `pdftotext -layout` before falling back to Claude's Read tool. Avoids the 2000px image-dimension limit that scanned-PDF pages can hit. | `brew install poppler` | `apt install poppler-utils` | `winget install oschwartz10612.Poppler` or `choco install poppler` |
| **tesseract** (OCR) | Fallback for scanned PDFs where `pdftotext` returns empty (i.e., pure image PDFs — trust documents, deeds, handwritten notes). Pipe `pdftoppm -r 150` → `tesseract` to get text. | `brew install tesseract` | `apt install tesseract-ocr` | `winget install UB-Mannheim.TesseractOCR` or `choco install tesseract` |
| **pandoc** (optional) | Cross-platform .docx → text | `brew install pandoc` | `apt install pandoc` | `winget install JohnMacFarlane.Pandoc` |
| **curl** | Occasional API examples (all scripted work uses `requests`) | built-in | built-in | built-in on Windows 10 1803+ (`C:\Windows\System32\curl.exe`) |

**Verify with this snippet** (use `PYTHON` from Cross-Platform Setup below):

```python
# check_prereqs.py
import shutil, socket, sys
missing = []
# Required tools
for tool in ("qpdf", "pdftotext"):        # pandoc + tesseract are optional-but-recommended
    if not shutil.which(tool):
        missing.append(tool)
# Python packages
try:
    import pypdf, docx, openpyxl, requests  # noqa: F401
except ImportError as e:
    missing.append(f"python package: {e.name}")
# DNS reachability check (fail fast if the user is on a restricted network)
try:
    socket.gethostbyname("api.m62.live")
except socket.gaierror:
    missing.append("DNS: cannot resolve api.m62.live (check network or set up hosts override — see Step 0.c)")
if missing:
    sys.exit(f"Missing prerequisites: {', '.join(missing)}")
print("All prerequisites OK")
```

### Windows-Specific Notes

1. **Python alias trap**: Windows 10+ ships a `python.exe` stub that opens the Microsoft
   Store instead of running Python. Verify with `python --version`. If it opens the Store,
   disable the alias under *Settings → Apps → Advanced app settings → App execution aliases*
   and install real Python from [python.org](https://www.python.org/downloads/windows/) or winget.
2. **Long paths (MAX_PATH 260)**: household folders with deep nesting can exceed Windows'
   legacy 260-character path limit. Either enable long paths (`reg add HKLM\SYSTEM\CurrentControlSet\Control\FileSystem /v LongPathsEnabled /t REG_DWORD /d 1 /f` as admin, then reboot)
   or place household folders at a short root like `C:\cl\` instead of the default Documents tree.
3. **File paths in prompts**: when passing file paths to sub-agents, use **forward slashes or
   raw strings** in Python (`r"C:\cl\Smith"` or `"C:/cl/Smith"`). Mixing backslashes with
   regular strings causes `\n`, `\t`, `\r` escapes to fire unexpectedly.
4. **PowerShell execution policy**: running `.ps1` scripts may be blocked by the default
   `Restricted` policy. For the refresh scripts, either run with `powershell -ExecutionPolicy Bypass -File tools\refresh-api-spec.ps1` or set the policy once with
   `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.
5. **No bash-isms**: Do not write `&&`, `||`, `$(...)` command substitution, `${VAR}`
   expansion, single-quote heredocs, or `python -c "..."` with embedded newlines.
   Always write scripts to a `.py` file and run them with `python script.py`.
6. **Line endings**: Python handles CRLF/LF transparently. If you write a `.py` helper
   script on Windows, don't worry about line endings.

### Step 0: Load Saved Configuration + Authenticate

**Do this FIRST before anything else.**

Altitude implements a full **OAuth 2.1 + PKCE + Dynamic Client Registration** authorization
server — the exact same protocol Claude uses for its MCP/connector integrations
(RFC 8414 / RFC 7591 / RFC 9728 / RFC 7636). This is the preferred interactive auth mode
for the skill: the user signs in on Altitude's own hosted login page in a browser, approves
the client, and the skill receives a JWT access token via a local loopback callback.

The access token returned by OAuth is a standard Altitude JWT — it works for **every**
REST endpoint (`/api/v1/individual`, `/api/v1/household`, `/api/v1/document`, etc.), not
just MCP endpoints, despite the `mcp:read`/`mcp:write` scope names.

**Auth modes supported:**

| Mode | Header used on every request | When to use |
|---|---|---|
| **OAuth (browser)** | `Authorization: Bearer <access_token>` | **Default for interactive use.** Altitude-hosted login, optional MFA, refresh tokens. |
| **API Key** | `X-API-Key: ak_live_...` | Automation, CI, long-lived server integrations. No browser needed. |
| **JWT (direct)** | `Authorization: Bearer <id_token>` | Fallback: user pastes a JWT obtained out-of-band (e.g., from the Altitude UI session). |

#### 0.a — Config file schema

`{HOME_DIR}/.altitude/config.json` (where `HOME_DIR` is `$HOME` on macOS/Linux or
`%USERPROFILE%` on Windows). The config supports all three modes via an `authMode`
discriminator:

```json
{
  "authMode": "oauth" | "api_key" | "jwt",
  "baseUrl": "https://api.m62.live",
  "firmName": "Wellington Advisors",

  "apiKey": "ak_live_xxxxxxxx",                    // if authMode=api_key
  "jwt": "eyJhbGciOiJIUzUxMi...",                  // if authMode=jwt (manual paste)

  // if authMode=oauth — populated by the OAuth flow below:
  "oauth": {
    "clientId": "550e8400-e29b-...",
    "accessToken": "eyJhbGciOiJIUzUxMi...",
    "refreshToken": "k8f3...",
    "tokenType": "Bearer",
    "expiresAt": "2026-04-18T18:00:00Z",
    "scope": "mcp:read mcp:write",
    "email": "advisor@firm.com"                    // cached only for display
  }
}
```

**Security rules** (enforce strictly):
1. **NEVER write the password to disk.** OAuth is specifically designed so the skill never
   sees the password — the browser handles that directly with Altitude.
2. Keep the config file `chmod 600` on Unix; on Windows, NTFS per-user ACLs under
   `%USERPROFILE%` provide equivalent protection.
3. When the `accessToken` is within 5 minutes of expiry, silently refresh via
   `POST /oauth/token` with `grant_type=refresh_token`. If the refresh fails (revoked,
   expired), fall back to the full browser auth flow.

#### 0.b — If config exists and credentials are current

- `authMode=api_key` + `apiKey` set → smoke-test with `GET /api/v1/authenticate` → use
- `authMode=oauth` + `accessToken` not expired → use immediately
- `authMode=oauth` + `accessToken` expired but `refreshToken` valid → refresh silently
- Any other state → run the appropriate auth flow below

#### 0.c — Auth Mode 1: OAuth (browser, recommended for interactive use)

**This is the Claude-connector flow.** The skill acts as a public OAuth client:

1. **Discover endpoints** — GET `{baseUrl}/.well-known/oauth-authorization-server` returns:
   ```json
   {
     "issuer": "https://api.m62.live",
     "authorization_endpoint": "https://api.m62.live/oauth/authorize",
     "token_endpoint": "https://api.m62.live/oauth/token",
     "registration_endpoint": "https://api.m62.live/oauth/register",
     "scopes_supported": ["mcp:read", "mcp:write"],
     "grant_types_supported": ["authorization_code", "refresh_token"],
     "response_types_supported": ["code"],
     "code_challenge_methods_supported": ["S256"],
     "token_endpoint_auth_methods_supported": ["none"]
   }
   ```
   Cache these endpoints.

2. **Dynamically register the skill as an OAuth client** (RFC 7591). This is a one-time
   operation — after the first successful registration, reuse the `clientId` from config.
   POST `{registration_endpoint}` with JSON:
   ```json
   {
     "client_name": "M62 Altitude Onboarding Skill",
     "redirect_uris": ["http://127.0.0.1:<random-free-port>/callback"],
     "grant_types": ["authorization_code", "refresh_token"],
     "token_endpoint_auth_method": "none",
     "response_types": ["code"]
   }
   ```
   Allowed redirect URIs are `http://localhost`, `http://127.0.0.1`, or `https://`. The
   response contains `client_id` — save it to `config.oauth.clientId` for reuse.

3. **Start a local loopback HTTP server** on `127.0.0.1:<port>` to receive the OAuth
   redirect. Bind port **0** to let the OS pick a free port, then read the assigned port.

4. **Generate PKCE values** (RFC 7636, S256 only):
   ```python
   import secrets, hashlib, base64
   code_verifier = base64.urlsafe_b64encode(secrets.token_bytes(64)).rstrip(b"=").decode()
   code_challenge = base64.urlsafe_b64encode(
       hashlib.sha256(code_verifier.encode()).digest()
   ).rstrip(b"=").decode()
   state = secrets.token_urlsafe(32)  # CSRF protection
   ```

5. **Open the browser** to the authorization endpoint with query parameters:
   ```
   {authorization_endpoint}
     ?response_type=code
     &client_id={clientId}
     &redirect_uri=http://127.0.0.1:{port}/callback
     &scope=mcp:read%20mcp:write
     &state={state}
     &code_challenge={code_challenge}
     &code_challenge_method=S256
   ```
   The user sees **Altitude's own login page** (not the skill's UI) in their browser,
   enters their email + password, and Altitude authenticates them. On success, Altitude
   redirects to `http://127.0.0.1:{port}/callback?code=XXX&state=YYY`.

6. **Local server catches the redirect**, validates `state`, captures `code`, shows the
   user a "Signed in — you can close this tab" page, then shuts down.

7. **Exchange code for tokens** — POST `{token_endpoint}` as
   `application/x-www-form-urlencoded`:
   ```
   grant_type=authorization_code
   &code={captured_code}
   &code_verifier={code_verifier}
   &redirect_uri=http://127.0.0.1:{port}/callback
   &client_id={clientId}
   ```
   Response (200):
   ```json
   {
     "access_token": "eyJhbGciOiJIUzUxMi...",
     "token_type": "Bearer",
     "expires_in": 3600,
     "refresh_token": "k8f3...",
     "scope": "mcp:read mcp:write"
   }
   ```
   Save `accessToken`, `refreshToken`, `expiresAt = now + expires_in - 30s` (30s buffer),
   and `tokenType` to `config.oauth.*`.

**Complete script** — write this to a temp file and run it. It handles the whole flow
including the loopback server:

```python
# altitude_oauth_login.py
import base64, hashlib, http.server, json, os, pathlib, secrets, socketserver
import sys, threading, urllib.parse, urllib.request, webbrowser

BASE = sys.argv[1]  # e.g., https://api.m62.live

# 1. Discover endpoints
meta_url = f"{BASE}/.well-known/oauth-authorization-server"
meta = json.loads(urllib.request.urlopen(meta_url, timeout=10).read())

# 2. Load or register client
home = pathlib.Path(os.environ.get("USERPROFILE") or os.environ["HOME"])
cfg_path = home / ".altitude" / "config.json"
cfg_path.parent.mkdir(exist_ok=True)
cfg = json.loads(cfg_path.read_text()) if cfg_path.exists() else {}
client_id = cfg.get("oauth", {}).get("clientId")

# 3. Pick a free loopback port
with socketserver.TCPServer(("127.0.0.1", 0), None) as s:
    port = s.server_address[1]
redirect_uri = f"http://127.0.0.1:{port}/callback"

if not client_id:
    reg_body = json.dumps({
        "client_name": "M62 Altitude Onboarding Skill",
        "redirect_uris": [redirect_uri],
        "grant_types": ["authorization_code", "refresh_token"],
        "token_endpoint_auth_method": "none",
        "response_types": ["code"],
    }).encode()
    req = urllib.request.Request(meta["registration_endpoint"], data=reg_body,
                                 headers={"Content-Type": "application/json"})
    reg = json.loads(urllib.request.urlopen(req, timeout=10).read())
    client_id = reg["client_id"]
    print(f"Registered OAuth client: {client_id}")

# 4. PKCE
cv = base64.urlsafe_b64encode(secrets.token_bytes(64)).rstrip(b"=").decode()
cc = base64.urlsafe_b64encode(hashlib.sha256(cv.encode()).digest()).rstrip(b"=").decode()
state = secrets.token_urlsafe(32)

# 5. Loopback server to catch the redirect
result = {}
class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass  # silence
    def do_GET(self):
        qs = urllib.parse.urlparse(self.path).query
        params = dict(urllib.parse.parse_qsl(qs))
        result.update(params)
        body = b"<html><body><h2>Signed in. You can close this tab.</h2></body></html>"
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
        threading.Thread(target=self.server.shutdown, daemon=True).start()

server = http.server.HTTPServer(("127.0.0.1", port), Handler)
threading.Thread(target=server.serve_forever, daemon=True).start()

# 6. Open the browser
auth_url = meta["authorization_endpoint"] + "?" + urllib.parse.urlencode({
    "response_type": "code", "client_id": client_id, "redirect_uri": redirect_uri,
    "scope": "mcp:read mcp:write", "state": state,
    "code_challenge": cc, "code_challenge_method": "S256",
})
print(f"Opening browser to: {auth_url}")
try: webbrowser.open(auth_url)
except Exception: print("Could not open browser automatically — open the URL manually.")

# Wait for callback (with 5 min timeout)
import time
deadline = time.time() + 300
while not result and time.time() < deadline:
    time.sleep(0.5)
server.shutdown()

if "error" in result:
    sys.exit(f"OAuth error: {result.get('error')} — {result.get('error_description','')}")
if result.get("state") != state:
    sys.exit("OAuth state mismatch — possible CSRF. Aborting.")
if "code" not in result:
    sys.exit("Timed out waiting for OAuth redirect.")

# 7. Exchange code for tokens
token_body = urllib.parse.urlencode({
    "grant_type": "authorization_code",
    "code": result["code"], "code_verifier": cv,
    "redirect_uri": redirect_uri, "client_id": client_id,
}).encode()
req = urllib.request.Request(meta["token_endpoint"], data=token_body,
    headers={"Content-Type": "application/x-www-form-urlencoded"})
tok = json.loads(urllib.request.urlopen(req, timeout=10).read())

# 8. Save config
import datetime
expires_at = datetime.datetime.utcnow() + datetime.timedelta(seconds=tok["expires_in"] - 30)
cfg["authMode"] = "oauth"
cfg["baseUrl"] = BASE
cfg.setdefault("oauth", {}).update({
    "clientId": client_id,
    "accessToken": tok["access_token"],
    "refreshToken": tok.get("refresh_token"),
    "tokenType": tok.get("token_type", "Bearer"),
    "expiresAt": expires_at.isoformat() + "Z",
    "scope": tok.get("scope"),
})
cfg_path.write_text(json.dumps(cfg, indent=2))
if os.name == "posix":
    os.chmod(cfg_path, 0o600)
print("OAuth login complete. Config saved.")
```

#### 0.d — OAuth token refresh (automatic)

When the access token is close to expiry, refresh silently:

```python
# altitude_oauth_refresh.py
import json, os, pathlib, urllib.parse, urllib.request, datetime, sys
home = pathlib.Path(os.environ.get("USERPROFILE") or os.environ["HOME"])
cfg = json.loads((home / ".altitude" / "config.json").read_text())
base = cfg["baseUrl"]
oa = cfg["oauth"]
body = urllib.parse.urlencode({
    "grant_type": "refresh_token",
    "refresh_token": oa["refreshToken"],
    "client_id": oa["clientId"],
}).encode()
req = urllib.request.Request(f"{base}/oauth/token", data=body,
    headers={"Content-Type": "application/x-www-form-urlencoded"})
try:
    tok = json.loads(urllib.request.urlopen(req, timeout=10).read())
except urllib.error.HTTPError as e:
    # Refresh failed (token revoked, expired) — caller should re-run full OAuth flow
    sys.exit(f"REFRESH_FAILED:{e.code}")
expires_at = datetime.datetime.utcnow() + datetime.timedelta(seconds=tok["expires_in"] - 30)
oa["accessToken"] = tok["access_token"]
if tok.get("refresh_token"):  # refresh rotation
    oa["refreshToken"] = tok["refresh_token"]
oa["expiresAt"] = expires_at.isoformat() + "Z"
(home / ".altitude" / "config.json").write_text(json.dumps(cfg, indent=2))
```

#### 0.e — Auth Mode 2: API Key (automation)

User pastes the key (it starts with `ak_live_` for production or `ak_test_` for dev).
Smoke-test with `GET {baseUrl}/api/v1/authenticate` — 200 means the key is valid. Save
with `authMode="api_key"`.

#### 0.f — Auth Mode 3: Direct JWT paste (fallback)

If the user already has a JWT (from the Altitude UI's browser session, for example), they
can paste it directly. Save with `authMode="jwt"` and `jwt=<token>`. This mode has no
refresh capability — when the JWT expires, prompt for a new paste or switch to OAuth.

#### 0.f.5 — DNS reachability test + loopback fallback

**Run this test at Step 0 before any API calls.** On some networks (corporate DNS,
split-horizon, DNS rebinding filters) `api.m62.live` fails to resolve via the system
resolver even though the service is reachable by IP. This has caused 100% of API calls
in the skill to fail with connection timeouts in prior runs.

```python
# altitude_dns_probe.py — run first, cache result
import socket, subprocess, json, os, pathlib, sys
def try_system_dns():
    try:
        ip = socket.gethostbyname("api.m62.live")
        return ("system", ip)
    except socket.gaierror:
        return None
def try_public_dns():
    for server in ("1.1.1.1", "8.8.8.8", "9.9.9.9"):
        try:
            out = subprocess.check_output(
                ["dig", f"@{server}", "api.m62.live", "+short", "+time=3"],
                text=True, timeout=5
            ).strip().splitlines()
            ips = [x for x in out if x and not x.startswith(";")]
            if ips: return ("public", ips[0])
        except Exception: pass
    return None

result = try_system_dns() or try_public_dns()
if not result:
    sys.exit("DNS: cannot resolve api.m62.live via any method. Check network/VPN/firewall.")

method, ip = result
home = pathlib.Path(os.environ.get("USERPROFILE") or os.environ["HOME"])
probe_file = home / ".altitude" / "dns_probe.json"
probe_file.parent.mkdir(exist_ok=True)
probe_file.write_text(json.dumps({"method": method, "ip": ip, "target": "api.m62.live"}))
print(f"DNS OK via {method}: {ip}")
```

**If `method == "system"`** → system DNS works, use normal Python `requests` or `curl`.

**If `method == "public"`** → system DNS is broken but public DNS has the IP. Every
subsequent API call must override. Two patterns:

1. **`curl` with `--resolve`** (simplest, reliable):
   ```bash
   curl --resolve "api.m62.live:443:<IP>" -H "X-API-Key: $KEY" "https://api.m62.live/api/v1/..."
   ```

2. **Python `requests` with connection patching** (cleaner for scripts):
   ```python
   # altitude_http.py
   import json, os, pathlib, requests
   from urllib3.util import connection
   home = pathlib.Path(os.environ.get("USERPROFILE") or os.environ["HOME"])
   probe = json.loads((home / ".altitude" / "dns_probe.json").read_text())
   if probe["method"] == "public":
       _orig = connection.create_connection
       def _patched(addr, *args, **kwargs):
           host, port = addr
           if host == "api.m62.live":
               addr = (probe["ip"], port)
           return _orig(addr, *args, **kwargs)
       connection.create_connection = _patched
   # Now use requests normally — DNS patching is transparent
   ```

On Windows with `curl.exe`, the same `--resolve` flag works. PowerShell's `Invoke-WebRequest`
does not support `--resolve`; use `curl.exe` or a Python script via PowerShell instead.

**Re-probe every hour** (IP can change). Cache the IP in `dns_probe.json` with a TTL check.

#### 0.g — Pick the right header per request

The skill's helper emits the correct header automatically based on `authMode`:

```python
# altitude_auth.py — load once, reuse everywhere
import json, os, pathlib, datetime
home = pathlib.Path(os.environ.get("USERPROFILE") or os.environ["HOME"])
cfg = json.loads((home / ".altitude" / "config.json").read_text())

def ensure_fresh():
    """Refresh OAuth token if within 5 minutes of expiry."""
    if cfg.get("authMode") != "oauth": return
    exp = datetime.datetime.fromisoformat(cfg["oauth"]["expiresAt"].rstrip("Z"))
    if exp - datetime.datetime.utcnow() < datetime.timedelta(minutes=5):
        import subprocess, sys
        subprocess.check_call([sys.executable, "altitude_oauth_refresh.py"])
        # reload
        global cfg
        cfg = json.loads((home / ".altitude" / "config.json").read_text())

def headers():
    ensure_fresh()
    mode = cfg.get("authMode", "api_key")
    if mode == "api_key":
        return {"X-API-Key": cfg["apiKey"]}
    if mode == "oauth":
        return {"Authorization": f"Bearer {cfg['oauth']['accessToken']}"}
    if mode == "jwt":
        return {"Authorization": f"Bearer {cfg['jwt']}"}
    raise RuntimeError(f"Unknown authMode: {mode}")

def base_url(): return cfg["baseUrl"]
def firm_name(): return cfg.get("firmName", "")
```

#### 0.h — Prompt the user to choose

If no usable config exists, ask:

> How should I authenticate to Altitude?
> 1. **OAuth (browser, recommended)** — I'll open Altitude's login page in your browser. You sign in there; I never see your password. I'll cache a short-lived access token + refresh token.
> 2. **API Key** (automation) — you paste an `ak_live_...` key. Good for CI or long-running integrations where no human is present.
> 3. **JWT paste** (fallback) — paste a JWT obtained from your existing Altitude browser session.

And: "Which environment? Production (`https://api.m62.live`) or Development (`http://localhost:8080`)?"

Then run the script for the chosen mode, save config, and proceed.

#### 0.i — Backwards compatibility

Config files without `authMode` but with `apiKey` set should be treated as `authMode=api_key`
for transparent upgrade. Write out an updated config with `authMode` set on the next run.

### Cross-Platform Setup

Detect the operating system and set platform-appropriate defaults. Do this ONCE at the start
and reuse throughout:

```python
import platform, shutil, os, tempfile

OS = platform.system()  # "Windows", "Darwin", "Linux"

# Python command
PYTHON = "python" if OS == "Windows" else "python3"

# Temp directory (NEVER hardcode /tmp/)
TMPDIR = tempfile.gettempdir()  # e.g., C:\Users\X\AppData\Local\Temp on Windows, /tmp on Unix

# Word doc converter
if shutil.which("textutil"):
    DOCX_CMD = "textutil -convert txt"          # macOS
elif shutil.which("pandoc"):
    DOCX_CMD = "pandoc -t plain -o"             # Cross-platform
else:
    DOCX_CMD = None  # Fall back to python-docx (see below)

# PDF decryptor
QPDF = shutil.which("qpdf")
# Install if missing:
#   macOS:   brew install qpdf
#   Windows: choco install qpdf  OR  winget install qpdf  OR  scoop install qpdf
#   Linux:   apt install qpdf    OR  dnf install qpdf
```

Save these values and use them for all subsequent commands. When this skill says `python3`,
use `PYTHON`. When it says `/tmp/`, use `TMPDIR`. When it says `textutil`, use `DOCX_CMD`.

### Full OpenAPI Spec

The full Altitude OpenAPI specification is available at `api-docs/api.json` relative to this
skill's directory. If you encounter an endpoint or schema not covered in the reference files,
search the full spec: `Glob pattern "**/m62-altitude-onboarding/**/api.json"` then use Grep
to find specific endpoints or schema definitions.

### Additional Requirements

- **firmId** (UUID) for the target firm — typically discovered during Phase 1 when querying Altitude

---

## Workflow Overview

```
Phase 1:   Query Altitude       → Find existing household + its full entity universe
Phase 2:   Scan Documents       → Classify ALL files, create read-tracking checklist
Phase 3:   Extract Entities     → PARALLEL agents read files, write extraction caches
Phase 3M:  Merge Extractions    → Combine all agent caches into unified extraction
Phase 3.5: Cross-Doc Validation → Name enrichment, relationship inference, absence tracking
Phase 3.7: Self-Audit           → Adversarial review: any unread files? any unnamed people? any missing entities?
Phase 4:   Match & Merge        → Match extracted entities to existing ones, diff fields
Phase 5:   Review               → Show user what will change (fills + conflicts)
Phase 6:   Push Updates         → PATCH existing entities, POST new ones (with approval)
Phase 7:   Upload Documents     → Associate each document with its correct entity
```

### Parallel Extraction Strategy

**Phase 3 uses parallel sub-agents to avoid context exhaustion.** The orchestrator (you)
NEVER reads document contents directly. Instead, you spawn extraction agents that each
handle a subset of files and write their results to disk.

**Batching rules — split by subdirectory, then by count. Hard cap: 25 files per batch.**

1. **Group files by subdirectory** first. Each top-level folder in the household directory
   becomes a candidate batch (e.g., `Identification/`, `LLC/`, `Tax Documents/`,
   `Financial Statements/`, `Insurance/`, `Estate Planning/`).

2. **Cap every batch at 25 files.** Any group exceeding 25 gets split:
   - 26-50 files → 2 batches of ~18-25
   - 51-75 files → 3 batches of ~17-25
   - 76+ → more splits, 25-file cap
   Never let a single batch exceed 30 files — sub-agent context pressure becomes severe
   beyond that, and image-heavy PDFs compound the load.

3. **If a subdirectory has < 4 files**, merge it with another small directory into one batch.

4. **Target batch size**: 15-20 files is the sweet spot. Very small families (< 10 files
   total) use 1 batch; larger families get 5-10 batches running in parallel.

5. **Parallelism budget**: 5-8 concurrent agents is the default target. 10+ concurrent
   agents has hit output-size limits in practice; split into waves if needed.

6. **Imbalance is OK** — don't force-balance batches. A batch of 16 mixed files + a batch
   of 22 all-statements is fine. Grouping by document type (all statements together, all
   trust docs together) is more valuable than perfect file-count parity, because agents
   can apply type-specific heuristics (statement period parsing, trust role extraction).

**Historical precedent**:
- Glickman (85 files) → 5 batches of 10-21 files, completed in ~9 minutes
- Boro-Hamilton (215 files) → 8 batches of 16-37 files; the 37-file batch strained context and retried once. Cap of 25 would have prevented the retry.

**Example batching for a 40-file household:**
```
Batch 1 (Agent A): Identification/ (3 files) + Onboarding/ (1 file) = 4 files
Batch 2 (Agent B): LLC/ (8 files) + Estate Planning/ (4 files) = 12 files
Batch 3 (Agent C): Tax Documents/ files 1-10 = 10 files
Batch 4 (Agent D): Tax Documents/ files 11-14 + Financial Statements/ (5 files) + Insurance/ (3 files) = 12 files
```

**Each extraction agent receives:**
- Its file list (absolute paths)
- The household name and folder path
- The extraction field definitions (from this skill's Phase 3 entity fields section)
- The document type patterns (from `references/document_type_patterns.md`)
- Instructions to write output to `altitude_review/extraction_cache_batch_{N}.jsonl`

**Each extraction agent produces:**
- One JSONL file: `altitude_review/extraction_cache_batch_{N}.jsonl`
- One tracker section: `altitude_review/file_tracker_batch_{N}.md`

**After ALL agents complete**, the orchestrator:
1. Reads all `extraction_cache_batch_*.jsonl` files
2. Reads all `file_tracker_batch_*.md` files
3. Merges into unified `extraction_cache.jsonl` and `file_tracker.md`
4. Verifies 100% file coverage before proceeding to Phase 3.5

**Spawn agents using the Agent tool:**
```
Agent(
  prompt="[extraction agent prompt with file list and instructions]",
  description="Extract batch N ({directory_name})",
  mode="bypassPermissions"
)
```

Launch ALL extraction agents in a **single message** so they run in parallel.
Do NOT launch them sequentially — that defeats the purpose.

---

## Phase 1: Query Altitude — Get Existing Household Universe

Before touching any documents, query Altitude to understand what already exists.

### Step 1.1: Search for the household

```
GET /api/v1/household/search?searchFor={household_name}&size=50
X-API-Key: {api_key}
```

or with JWT:

```
GET /api/v1/household/search?searchFor={household_name}&size=50
Authorization: Bearer {token}
```

If a matching household is found, record its `id`. If multiple matches, ask the user
which one. If no match, note that this is a new household (will need POST later).

### Step 1.2: Get the household's full relationship graph

Query outgoing relationships (household → members) and incoming relationships:

```
GET /api/v1/household/{householdId}/relationships/from
X-API-Key: {api_key}
```

Or via the standalone entity relationship endpoint:

```
GET /api/v1/entity-relationship/from/HOUSEHOLD/{householdId}
X-API-Key: {api_key}
```

This returns all `EntityRelationshipDto` entries — every individual, legal entity, account,
contact, and their relationship types (MEMBER, OWNERSHIP, TRUSTEE, BENEFICIARY, ADVISOR, etc.).
Record:
- All individual IDs + basic info
- All legal entity IDs + entity types
- All account (AccountFinancial) IDs + account types
- All contact IDs + job titles
- Relationship metadata (type, role, percentage, effectiveFrom, effectiveTo)

### Step 1.3: Fetch full details for each entity

**Account graph traversal — DO NOT trust `household.totalAccountCount`.** In practice the
household count often exceeds the number of accounts reachable via direct
`HOUSEHOLD → ACCOUNT_FINANCIAL` relationships, because most accounts hang off trusts and
LLCs, not the household itself. In a $1.22B household with 48 accounts, fewer than a
dozen were directly owned by the household — the rest were inside trust/LLC sub-graphs.

**Traversal algorithm** (implement this before moving past Phase 1):

```python
# altitude_account_graph.py — recursively discover all accounts reachable from household
visited_entities = set()   # (entity_type, entity_id) pairs we've already expanded
all_accounts = {}          # account_id -> basic info

def expand(entity_type, entity_id):
    key = (entity_type, entity_id)
    if key in visited_entities: return
    visited_entities.add(key)
    rels = api_get(f"/api/v1/entity-relationship/from/{entity_type}/{entity_id}")
    for r in rels:
        if r["targetEntityType"] == "ACCOUNT_FINANCIAL":
            all_accounts[r["targetEntityId"]] = {
                "id": r["targetEntityId"],
                "name": r["targetEntityName"],
                "ownerType": entity_type,
                "ownerId": entity_id,
                "ownerName": "<look up from existing cache>",
            }
        elif r["targetEntityType"] in ("LEGAL_ENTITY", "INDIVIDUAL"):
            expand(r["targetEntityType"], r["targetEntityId"])  # recurse

expand("HOUSEHOLD", household_id)
```

This expands Household → its individuals and legal entities → each of their
outgoing relationships → any sub-LEs they hold → all the way down to every leaf
ACCOUNT_FINANCIAL. The number of accounts discovered should match or exceed
`household.totalAccountCount`. If the discovered count is LOWER, flag as open question
(the household counter may include hard-deleted or orphan accounts).

**Account search fallback** — some accounts may not be wired into the relationship graph
(orphan accounts created directly). Also search by household name tokens AFTER graph
traversal to catch these:

```
GET /api/v1/account-financial/search?searchFor={householdNameToken}&size=100
```

For each individual in the household:
```
GET /api/v1/individual/{id}
```

For each legal entity in the household:
```
GET /api/v1/legal-entity/{id}
```

For each account discovered via the traversal above:
```
GET /api/v1/account-financial/{id}
```

For each contact in the household:
```
GET /api/v1/contact/{id}
```

For tangible assets, query by owner:
```
GET /api/v1/tangible-asset/by-owner/INDIVIDUAL/{individualId}
GET /api/v1/tangible-asset/by-owner/LEGAL_ENTITY/{legalEntityId}
```

For liabilities (query by individual/household):
```
GET /api/v1/liability/by-individual/{individualId}
GET /api/v1/liability/by-household/{householdId}
```

For insurance policies (query by individual/household/legal entity):
```
GET /api/v1/insurance-policy/by-individual/{individualId}
GET /api/v1/insurance-policy/by-household/{householdId}
GET /api/v1/insurance-policy/by-legal-entity/{legalEntityId}
```

Store all of this as the **"Altitude Universe"** — the complete current state of the
household in Altitude. This is the baseline for comparison.

### Step 1.4: Search for accounts and contacts by name

Additionally, search for any accounts and contacts by name pattern:

```
GET /api/v1/account-financial/search?searchFor={account_name_pattern}&size=50
GET /api/v1/contact/search?searchFor={contact_name_pattern}&size=50
```

### Step 1.5: Build the Altitude Universe index

Create an in-memory index for matching:

```json
{
  "household": { "id": "...", "name": "...", "firmId": "..." },
  "individuals": [
    {
      "id": "...", "firstName": "...", "lastName": "...", "ssn": "...",
      "dateOfBirth": "...", "email": "...", "phone": "...", "addressLegal": "..."
    }
  ],
  "legal_entities": [
    {
      "id": "...", "legalName": "...", "entityType": "...", "taxId": "...",
      "jurisdiction": "...", "formationDate": "...", "incorporationState": "...", "incorporationCountry": "..."
    }
  ],
  "accounts": [
    {
      "id": "...", "name": "...", "accountNumber": "...", "accountCategory": "...",
      "subCategory": "...", "custodianId": "..."
    }
  ],
  "contacts": [
    {
      "id": "...", "firstName": "...", "lastName": "...", "email": "...",
      "phone": "...", "jobTitle": "..."
    }
  ],
  "tangible_assets": [
    {
      "id": "...", "name": "...", "category": "...", "assetType": "...",
      "serialOrIdentifier": "...", "currentValue": "..."
    }
  ],
  "liabilities": [
    {
      "id": "...", "name": "...", "liabilityType": "...", "liabilityStatus": "...",
      "lenderName": "...", "accountNumber": "...", "currentBalance": "...",
      "interestRate": "...", "monthlyPayment": "..."
    }
  ],
  "insurance_policies": [
    {
      "id": "...", "name": "...", "policyCategory": "...", "policyNumber": "...",
      "carrierName": "...", "policyStatus": "...", "coverageAmount": "...",
      "annualPremium": "..."
    }
  ],
  "relationships": [ ... ]
}
```

Save as `{household_folder}/altitude_review/altitude_universe.json` for reference.

---

## Phase 2: Scan & Classify Documents

### Step 2.0: OneDrive / cloud-sync hydration pre-scan (REQUIRED before spawning agents)

OneDrive, Dropbox, iCloud and Box store files as "dataless placeholders" until accessed —
reading one triggers a download. In extraction sub-agents, a cloud-stub read times out
after tens of seconds (default socket timeout), wasting compute. Detect unhydrated files
**before** spawning agents and report them to the user for bulk hydration in Finder/Explorer
before the expensive extraction runs.

```python
# altitude_hydration_scan.py
import os, subprocess, sys
from pathlib import Path

HOUSEHOLD = sys.argv[1]  # absolute path to household folder
STUB_THRESHOLD_SECS = 3  # a 1-byte read taking > 3s is almost certainly a cloud stub

def is_cloud_stub(path: str) -> bool:
    try:
        subprocess.check_output(
            ["dd", f"if={path}", "bs=1", "count=1", "of=/dev/null"],
            stderr=subprocess.DEVNULL, timeout=STUB_THRESHOLD_SECS,
        )
        return False
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
        return True

stubs = []
for root, _, files in os.walk(HOUSEHOLD):
    if "altitude_review" in root: continue
    for f in files:
        if f.startswith(".DS_Store"): continue
        p = os.path.join(root, f)
        if is_cloud_stub(p): stubs.append(p)

if stubs:
    print(f"❌ {len(stubs)} cloud-stub files detected (read times out):")
    for s in stubs: print(f"  {s}")
    print()
    print("TO HYDRATE (macOS Finder):")
    print("  Right-click the folder(s) containing these files → 'Always Keep on This Device'")
    print("TO HYDRATE (Windows Explorer):")
    print("  Right-click → 'Always keep on this device'")
    print("After hydration (green circle icons), re-run the scan.")
    sys.exit(2)
else:
    print(f"✅ All files hydrated. Safe to proceed with extraction.")
```

**If stubs are found**: present the list to the user in a compact form (grouped by
parent directory, counts), ask them to hydrate, then **re-run this scan** before
proceeding. Do NOT launch extraction agents if any unhydrated files remain — they
will consume hundreds of seconds of agent time timing out on reads.

**If all files are hydrated**: proceed to document classification below.

### Step 2.1: Classify Documents

List all files recursively in the household folder. Classify each document using the
patterns in `references/document_type_patterns.md`. Key classification rules:

**Extraction priority:**
- **Tier 1** (extract first): Onboarding sheets, IDs (DLs, passports), trust agreements,
  LLC operating agreements, articles of organization/incorporation, EIN letters,
  account applications
- **Tier 1.5** (NEVER SKIP — compact, data-dense IRS forms): Form 1098 (mortgage → creates
  liability + tangible asset), Schedule K-1 (ownership percentages — authoritative), Form
  1099-DIV/INT/B/R (account + custodian validation), Form W-2 (employer + income), Form 5498
  (IRA details). A single 1098 produces 1 liability, 1 tangible asset, and 2+ relationships.
  A single K-1 produces an entity + ownership relationship with exact percentage.
- **Tier 2**: Personal tax returns (1040), entity tax returns (1065/1120/1120S/1041),
  account statements, insurance policy declarations, property tax bills, beneficiary designations
- **Tier 3**: Financial statements, meeting notes, presentations, valuations, estate planning flowcharts
- **Tier 4** (skip): Duplicates ("Copy of", "zDupes"), receipts, .msg files, spreadsheets
  with personal notes

**Document-to-entity association** — each document maps to an entity type for upload:
Read `references/document_entity_association.md` for the complete mapping of which
document types associate with which Altitude entity type and what `documentSubType`
to use.

---

## Phase 3: Extract Entities from Documents

### PDF Reading — TEXT-FIRST by default

**⚠ CRITICAL: Do NOT start with Claude's Read tool on PDFs.** Claude's Read tool rejects
images with any dimension >2000px, and many scanned PDFs (trust documents, deeds,
handwritten notes, high-res scans) include pages that trip this limit. The result is
`"image exceeds 2000px dimension limit"` errors that abort whole extraction batches.

**Required reading order for every PDF**:

1. **Text-first via `pdftotext`** (poppler) — works on any PDF with embedded text:
   ```bash
   pdftotext -layout -nopgbrk "file.pdf" - | head -c 200000 > /tmp/extracted.txt
   ```
   Then Read `/tmp/extracted.txt`. This is fast, safe, and avoids the image limit entirely.

2. **If `pdftotext` returns mostly blank or gibberish** → the PDF is a scan. Render and OCR:
   ```bash
   # Render pages 1-5 at 150 dpi (cap pages for large scans)
   pdftoppm -r 150 -f 1 -l 5 "file.pdf" /tmp/scan_page
   # Each page becomes /tmp/scan_page-1.png, scan_page-2.png, etc.
   for png in /tmp/scan_page-*.png; do
     tesseract "$png" "${png%.png}" -l eng
   done
   cat /tmp/scan_page-*.txt > /tmp/extracted.txt
   ```
   Then Read `/tmp/extracted.txt`.

3. **Only fall back to Claude's Read tool on the raw PDF** as a last resort — and only if
   the file is **< 5 MB** (to avoid loading many high-res pages). If Read fails with the
   2000px error, mark the file `status=FAILED_IMAGE_TOO_LARGE` in the tracker and move on.
   Do not loop.

**Use `pypdf` for page-index scanning** — this is still the best way to find the data-rich
pages in a 200-page tax return without loading every page's content:

### Large PDF Strategy (20+ pages)

Tax returns and combined statements are often 50-200+ pages. Reading only the first few pages
will miss K-1 summaries, W-2s, 1099s, Schedule H, and passthrough entity details buried deep
in the document. Use this two-pass strategy, **built on the text-first foundation above**:

**Pass 1 — Page Index Scan** (fast, text-only):

Use `PYTHON` from the Cross-Platform Setup section for all Python invocations.
On Windows, write multi-line scripts to a temp `.py` file instead of using `-c` to
avoid shell quoting issues.

```python
# page_scan.py — write this to a temp file, then run: python page_scan.py
import sys
from pypdf import PdfReader
reader = PdfReader(sys.argv[1])
print(f'Total pages: {len(reader.pages)}')
for i, page in enumerate(reader.pages):
    text = (page.extract_text() or '')[:150].replace('\n', ' | ')
    print(f'  Page {i+1}: {text}')
```

Run: `{PYTHON} page_scan.py "file.pdf"` (where `{PYTHON}` is `python` on Windows and `python3` on macOS/Linux, per Cross-Platform Setup above).

This produces a one-line summary per page. Scan the output for keywords that signal data-rich
pages:

| Keyword | What It Signals | Action |
|---------|----------------|--------|
| `K-1`, `Schedule K-1` | Partnership/LLC ownership + income | Read full page — TAX_K1 checklist |
| `W-2`, `Wage and Tax` | Employer name, wages, SSN | Read full page — TAX_W2 checklist |
| `1099`, `1099-DIV`, `1099-INT`, `1099-B`, `1099-R` | Account/custodian validation, income | Read full page — TAX_1099 checklist |
| `1098`, `Mortgage Interest` | Mortgage lender, balance, property | Read full page — TAX_1098 checklist |
| `Schedule E`, `Passthrough` | Entity names, EINs, income types | Read full page |
| `Schedule H`, `Household Employ` | Domestic staff, household employer EIN | Read full page |
| `Schedule A`, `Itemized` | Mortgage interest, charitable, taxes | Skim for amounts |
| `Schedule C`, `Profit or Loss` | Sole proprietorship business | Read full page |
| `Sign Here`, `Occupation`, `Preparer` | Occupations, CPA name/phone | Read full page (usually page 2 of 1040) |
| `8879`, `e-file` | SSNs, AGI confirmation, preparer | Read full page |
| Entity names (trust names, LLC names) | Entity K-1 details | Read full page |
| `LESSER`, `TRUST`, or any family surname | Related trust/entity income | Read full page |

**Pass 2 — Targeted Deep Read**:
For each flagged page, extract text with `pdftotext -f N -l N "file.pdf"` (where N is the
page number) to a temp file and Read that. Only use Claude's Read tool on the original PDF
for the flagged pages if `pdftotext` returns empty for that specific page (indicating a
scanned page). For a typical 200-page return, you'll usually need to read 15-25 key pages.

**Minimum pages to ALWAYS read from a personal 1040 return:**
1. Cover letter (page 1) — preparer firm, client address
2. Form 8879 — SSNs, AGI, preparer name
3. Form 1040 pages 1-2 — income summary, dependents, occupations, preparer, filing status
4. Schedule E page 2 — ALL passthrough entity names + EINs
5. Passthrough income detail pages — entity-by-entity breakdown
6. Schedule H (if present) — household employment
7. Any pages with K-1, W-2, 1098, or 1099 keywords

**Password-protected PDFs:**
Tax returns are often password-protected. The password is frequently in the filename
(e.g., "pass 701431"). Decrypt before reading:
```bash
qpdf --password=PASSWORD --decrypt input.pdf decrypted.pdf
```
Write the decrypted file to the same directory as the input, or to a temp directory
(use Python `tempfile.mkdtemp()` if needed — do NOT hardcode `/tmp/`).

If `qpdf` is not installed:
- **macOS**: `brew install qpdf`
- **Windows**: `choco install qpdf` or `winget install qpdf` or `scoop install qpdf`
- **Linux**: `apt install qpdf` or `dnf install qpdf`

### ⛔ CRITICAL: Zero-Skip Rule — THE #1 CAUSE OF EXTRACTION FAILURE

**EVERY file in the household folder MUST be opened and read. NO EXCEPTIONS.**

This is the single most important rule in this skill. In testing, 100% of extraction failures
trace back to files that were not read. Not "low quality" files. Not "redundant" files. Files
that were simply never opened. An Operating Agreement that contains ownership percentages. A
1099 that reveals an account number. A DocuSign certificate that identifies the employer. An
email signature with an attorney's contact info.

**You WILL be tempted to skip files.** You will think "I already have the EIN from the onboarding
sheet, I don't need to read the EIN letter." You will think "The amendments just change the
address, I already know the address." You will think "The Sunbiz is just a state filing." Every
one of these thoughts leads to missed data. Every document contains something — a name, an
address, a date, a registered agent, a formation date — that cannot be found anywhere else.

**Do not classify files as low priority and skip them.** Do not read 22 out of 60 files and call
it done. Read ALL 60. If the context window gets full, save your extraction progress to disk
and continue in a follow-up pass.

For each file, at minimum:
- **PDFs**: Read at least page 1. If it's a multi-page form (tax return, statement), use the
  Large PDF Strategy above to find all data-rich pages.
- **Images (.jpg, .png)**: Read with Claude's vision. Even a property photo confirms a real
  asset exists.
- **Word docs (.docx)**: Convert using the platform's `DOCX_CMD` (see Cross-Platform Setup).
  Fallback chain: `textutil` (macOS) → `pandoc` (cross-platform) → `python-docx` (write a
  `docx_read.py` script — see Standard Document Extraction below for the exact script).
  If all fail, flag for user — don't silently skip.
- **Emails (.eml)**: Parse headers + body. Extract attachments and process them too.

**Enforce with a tracking file**: After Phase 2 classification, write a file checklist to
`altitude_review/file_tracker.md` with every file path. As you read each file, update the
tracker with status (READ/SKIPPED) and a one-line summary of what was extracted. Before
Phase 4, parse the tracker and verify ZERO files have status other than READ. If any files
remain unread, you MUST read them before proceeding. This is not optional.

Example tracker format:
```
| # | File | Status | Extracted |
|---|------|--------|-----------|
| 1 | Identification/DL.png | READ | Brett Adam, Michaela Dylan, DOBs, addresses |
| 2 | LLC/Operating Agreement.pdf | READ | Members: Brett 60%, Michaela 40% |
| 3 | Tax/1099-INT.pdf | PENDING | |
```

**For folders with 10+ files**, use the Parallel Extraction Strategy (see Workflow Overview).
Spawn one Agent per batch. Each agent handles its assigned files independently and writes
results to its own `extraction_cache_batch_{N}.jsonl` file. The orchestrator merges after all
agents complete. For folders with < 10 files, a single agent handles all files.

### Extraction Cache (REQUIRED — each agent writes its own)

**After reading EACH file**, each extraction agent appends what it learned to its own cache file:
`altitude_review/extraction_cache_batch_{N}.jsonl` (one JSON object per line, append-only).
The orchestrator later merges all batch files into `altitude_review/extraction_cache.jsonl`.

Each line captures everything extracted from a single file:

```jsonl
{"file": "Identification/DL.png", "readAt": "2026-03-19T22:00:00Z", "fileNumber": 1, "entities": {"individuals": [{"name": "Brett Adam Podolsky", "dob": "1988-02-19", "gender": "M", "dlNumber": "P342-061-88-059-0", "dlState": "FL", "dlExpiry": "2031-02-19", "address": "3985 NW 53rd St, Boca Raton, FL 33496"}]}, "relationships": [], "contacts": [], "accounts": [], "notes": "Both Brett and Michaela DLs on same image"}
{"file": "LLC/Hercules/Operating Agreement.pdf", "readAt": "2026-03-19T22:01:00Z", "fileNumber": 2, "entities": {"legalEntities": [{"name": "Hercules Lender LLC", "type": "LLC", "managementType": "MEMBER_MANAGED", "opAgreementDate": "2022-09-29"}]}, "relationships": [{"source": "Brett Podolsky", "target": "Hercules Lender LLC", "type": "OWNERSHIP", "percentage": 50, "role": "Managing Member"}], "contacts": [{"name": "Jason Evans", "role": "Registered Agent", "address": "2300 NW Corporate Blvd Suite 215, Boca Raton FL 33431"}], "accounts": [], "notes": "Principal: 20352 Hacienda Ct"}
```

**Why this matters:**
- **Resumability**: If context resets at file 150 of 292, the next session reads the cache
  and picks up at file 151 — no re-reading of the first 150 files
- **Cross-document validation**: Later files can check against earlier extractions ("is this
  the same trust?") without re-reading the source documents
- **Subagent handoff**: One agent extracts (writes cache), another matches/merges (reads cache)
- **Audit trail**: Every extracted field traces to a specific file

**Cache rules:**
- Append after EACH file, not at the end of a batch — partial progress is saved
- Include ALL extracted data, not just summaries — names, dates, numbers, addresses, percentages
- Use `fileNumber` to track progress — on resume, skip files with fileNumber ≤ max in cache
- For files with no extractable data, still append a line with empty entities and a note explaining why
- The cache is the source of truth for Phase 4 matching — read it instead of relying on context memory

**On resume**, check for existing cache (use `os.path.join` for cross-platform paths):
```python
import json, os
cache_path = os.path.join('altitude_review', 'extraction_cache.jsonl')
existing = []
try:
    with open(cache_path) as f:
        existing = [json.loads(line) for line in f if line.strip()]
    last_file = max(e['fileNumber'] for e in existing)
    print(f"Resuming from file {last_file + 1} ({len(existing)} files already cached)")
except FileNotFoundError:
    print("No cache found, starting fresh")
```

### Standard Document Extraction

For each Tier 1 and Tier 2 document, extract structured data. Use Claude's native tools:

- **PDFs**: Use Claude Read tool natively (supports text and scanned PDFs with vision)
> **Windows note**: Do NOT use `python -c "..."` with embedded newlines or nested quotes.
> Windows cmd and PowerShell mangle multi-line argv strings and single-quote escaping
> differently from bash. The cross-platform pattern is: **write the script to a temp `.py`
> file with the `Write` tool, then run it as `python script.py`**. This avoids every
> shell-quoting pitfall on every OS. All snippets below use this pattern.

- **Word docs (.docx)**: Use the platform's `DOCX_CMD` (see Cross-Platform Setup):
  - macOS: `textutil -convert txt file.docx` then read the `.txt`
  - Cross-platform: `pandoc file.docx -t plain` (pipe or redirect output)
  - Python fallback (works everywhere): write `docx_read.py` below, then `python docx_read.py "file.docx"`

```python
# docx_read.py
import sys
from docx import Document
for p in Document(sys.argv[1]).paragraphs:
    print(p.text)
```
  Install `python-docx` if needed: `pip install python-docx`
- **Images (.jpg, .png)**: Use Claude Read tool — Claude can see images natively (multimodal)
- **Spreadsheets (.xlsx)**: Write `xlsx_read.py` below, then `python xlsx_read.py "file.xlsx"`. Install if needed: `pip install openpyxl`

```python
# xlsx_read.py
import sys, openpyxl
wb = openpyxl.load_workbook(sys.argv[1], data_only=True)
for sheet in wb.sheetnames:
    ws = wb[sheet]
    print(f"=== {sheet} ({ws.max_row} rows x {ws.max_column} cols) ===")
    for row in ws.iter_rows(values_only=True):
        print(row)
```

- **Emails (.eml)**: Write `eml_read.py` below, then `python eml_read.py "file.eml"`. Extract entity data from the email body (e.g., account confirmations, policy updates, advisor correspondence). Process any saved attachments as their native file type.

```python
# eml_read.py — prints headers + body, saves attachments to temp dir
import email, os, sys, tempfile
with open(sys.argv[1], 'rb') as f:
    msg = email.message_from_binary_file(f)
for h in ('From', 'To', 'Date', 'Subject'):
    print(f"{h}: {msg[h]}")
att_dir = os.path.join(tempfile.gettempdir(), 'eml_attachments')
os.makedirs(att_dir, exist_ok=True)
for part in msg.walk():
    ctype = part.get_content_type()
    if ctype == 'text/plain':
        body = part.get_payload(decode=True)
        if body:
            print(body.decode(errors='replace'))
    fn = part.get_filename()
    if fn:
        out_path = os.path.join(att_dir, fn)
        with open(out_path, 'wb') as out:
            out.write(part.get_payload(decode=True))
        print(f"Saved attachment: {out_path}")
```

For each document, extract:

**Individuals:**
- Core: firstName, lastName, preferredName (known-by/English name — e.g., "Tina" for legal "Dong"), dateOfBirth, ssn, gender, maritalStatus, citizenship
- Contact: email, phoneNumberPrimary, phoneNumberSecondary, faxNumber
- Address: addressLine1, addressLine2, city, state, postalCode, country, addressType, addressEmployer
- Financial: netWorth, netWorthLiquid, annualIncome, sourceOfFunds, riskTolerance, timeHorizon
- Tax: taxStatus, taxIdType (SSN/ITIN/EIN/FOREIGN_TIN/FOREIGN_ENTITY_TIN/VAT/GST/BUSINESS_NUMBER), taxIdIssuingCountry
- Regulatory: accreditedInvestorStatus, isPoliticallyExposedPerson
- Beneficiary: transferOnDeath beneficiaries
- Lifecycle: dateOfDeath, lifecycleStatus
- Profession: occupation, employer

**Legal Entities:**
- Core: legalName, entityType, formationDate, jurisdiction, incorporationState, incorporationCountry
- Tax: taxId (EIN), taxClassification, fiscalYearEnd
- Governance: llcManagementType, primarySigners, nominee, eligibility
- Registered Agent: agent name and address
- Authorized Shares: corpAuthorizedShares, corpIssuedShares
- Compliance: KYC/AML tracking, regulatoryStatus, affiliations
- **Trust-specific** (if entityType=TRUST):
  - Trustees: trustee names and roles
  - Grantor: grantor name and revocable status (revocable/irrevocable)
  - Beneficiaries: primary and contingent beneficiary names
  - Settlor and Trustee names, roles
  - Situs (jurisdiction), governing law
  - Investment Advisor, Distribution Advisor, Crummey Power Holders
  - Powers of Appointment, Spendthrift Provision, GST exemption status
  - Insurance Provisions, Amendment tracking (number, date), Restatement status
  - Pour-over trust name, trust aliases

**Account Financials:**
- Core: name, accountNumber, accountCategory (INDIVIDUAL/ENTITY), subCategory
- Type: wrapper (IRA/401k if applicable), taxStatus
- Custodian: custodianId, custodian name
- Ownership: ownershipType (PERCENT_BASED default)
- Connection: providerDetails (sourceSystemName, sourceSystemAccountId)

**Contacts:**
- Core: firstName, lastName, email, phone, jobTitle
- Note: Contact DTO has NO companyName/organization field. Company info goes in biography or via ADVISOR entity relationship.
- Address: addressLine1, addressLine2, city, state, postalCode, country

**Tangible Assets:**
- Core: name, category (LUXURY/VEHICLE/REAL_PROPERTY/COLLECTIBLE/OTHER)
- Asset Type: assetType (CAR, MOTORCYCLE, BOAT, YACHT, AIRCRAFT, HELICOPTER, RV, PRIMARY_RESIDENCE, VACATION_HOME, RENTAL_PROPERTY, COMMERCIAL_PROPERTY, LAND, FARM_RANCH, TIMESHARE, WATCH, JEWELRY, HANDBAG, FASHION, LUXURY_OTHER, ART, WINE, ANTIQUE, MEMORABILIA, COINS, STAMPS, BOOKS, MUSICAL_INSTRUMENT, COLLECTIBLE_OTHER, EQUIPMENT, LIVESTOCK, FURNITURE, OTHER_TYPE)
- Identification: serialOrIdentifier, VIN, parcel number
- Valuation: currentValue, valuationDate, valuationSource, taxBasis, taxBasisDate, acquisitionType (PURCHASE/AUCTION/GIFT/INHERITANCE/COMMISSION/EXCHANGE/PRIZE), purchaseDate, purchasePrice
- Status: status (ACTIVE/SOLD/TRANSFERRED/DONATED/DISPOSED/STOLEN/LOST)
- Location: location, storageFacility, custodianName, custodianContact
- Insurance: isInsured (Boolean), primaryInsurancePolicyNumber, insuredValue, insuranceExpirationDate (Note: full insurance details are on the InsurancePolicy entity, not TangibleAsset)
- Estate: includedInEstate, estateDisposition, designatedBeneficiaryId, estateNotes
- Type-specific: vehicleDetails (make/model/year), realPropertyDetails (address/square footage),
  luxuryDetails (brand/model), collectibleDetails (artist/medium)
- Maintenance: maintenanceRecords, provenance chain, condition

**Insurance Policies:**
- Core: name, policyCategory (LIFE/UMBRELLA/LONG_TERM_CARE/DISABILITY/HEALTH/AUTO/HOMEOWNERS/FLOOD/CYBER/COLLECTIONS/WINDSTORM/OTHER), policyNumber, carrierName, policyStatus (ACTIVE/LAPSED/CANCELLED/PAID_UP/SURRENDERED/MATURED/PENDING)
- Financial: coverageAmount, annualPremium, paymentFrequency (MONTHLY/BI_WEEKLY/QUARTERLY/ANNUAL/INTEREST_ONLY), deductible
- Dates: effectiveDate, expirationDate, applicationDate, issueDate, firstPaymentDate
- Description: description (max 4000)
- Life-specific (policyCategory=LIFE): lifePolicyType (TERM/WHOLE_LIFE/UNIVERSAL/VARIABLE_UNIVERSAL/INDEXED_UNIVERSAL/SURVIVORSHIP/GROUP_TERM), deathBenefit, cashValue, cashValueAsOfDate, loanBalance, termLengthYears, termExpirationDate, isConvertible, conversionDeadline, isIlitOwned, ilitLegalEntityId, isSecondToDie, secondInsuredIndividualId, guaranteedDeathBenefit, riders, surrenderChargeSchedule, dividendOption (CASH/PREMIUM_REDUCTION/ACCUMULATE_AT_INTEREST/PAID_UP_ADDITIONS/ONE_YEAR_TERM)
- Umbrella-specific (policyCategory=UMBRELLA): excessLiabilityCoverage, underlyingAutoRequired, underlyingHomeRequired, underlyingPoliciesDescription, coversRentalProperties, coversWatercraft, uninsuredMotorist
- LTC-specific (policyCategory=LONG_TERM_CARE): dailyBenefitAmount, benefitPeriodDescription, benefitPeriodMonths, eliminationPeriodDays, inflationProtectionType (NONE/SIMPLE/COMPOUND_3_PERCENT/COMPOUND_5_PERCENT/CPI_LINKED/FUTURE_PURCHASE_OPTION), coversHomeCare, coversAssistedLiving, coversNursingFacility, coversAdultDayCare, sharedBenefitRider, isPartnershipQualified, remainingBenefitPool
- Disability-specific (policyCategory=DISABILITY): monthlyBenefitAmount, benefitPeriodDescription, eliminationPeriodDays, isOwnOccupation, ownOccupationPeriodDescription, costOfLivingAdjustment, futureIncreaseOption, residualDisabilityRider, isGroupPolicy, isTaxableBenefit

**Liabilities:**
- Core: name, liabilityType (MORTGAGE/HOME_EQUITY_LOC/STUDENT_LOAN/MARGIN_LOAN/PLEDGED_ASSET_LINE/CREDIT_LINE/CREDIT_CARD/AUTO_LOAN/PERSONAL_LOAN/BUSINESS_LOAN/OTHER), liabilityStatus (CURRENT/DELINQUENT/IN_DEFERMENT/IN_FORBEARANCE/PAID_OFF/DEFAULTED/CHARGED_OFF)
- Lender: lenderName, accountNumber
- Balance: originalBalance, currentBalance, balanceAsOfDate, creditLimit, availableCredit
- Rate: interestRate, interestRateType (FIXED/VARIABLE/HYBRID), indexRateDescription, rateCap, rateFloor
- Payment: monthlyPayment, minimumPayment, paymentFrequency (MONTHLY/BI_WEEKLY/QUARTERLY/ANNUAL/INTEREST_ONLY), nextPaymentDate
- Term: originationDate, maturityDate
- Collateral: isSecured, collateralDescription, linkedTangibleAssetId, linkedAccountFinancialId
- Tax: isInterestDeductible, interestDeductionType (MORTGAGE_INTEREST/INVESTMENT_INTEREST/STUDENT_LOAN_INTEREST/BUSINESS_INTEREST/NONE), interestPaidYtd, interestPaidPriorYear
- Description: description (max 4000)

**Estate Planning (nested on Individual via PATCH):**
- Will: hasWill, willDate, executorName, contingentExecutorName, attorneyName, jurisdiction
- Healthcare: hasHealthcareDirective, directiveDate, agentName, alternateAgentName, hasLivingWill
- Financial POA: hasFinancialPoa, type (DURABLE/SPRINGING/LIMITED/GENERAL), agentName, poaDate
- Guardianship: hasGuardianDesignation, guardianName, alternateGuardianName
- Marital: hasPrenuptialAgreement, prenuptialDate, hasPostnuptialAgreement
- Estate Review: lastReviewDate, estimatedEstateValue, estimatedEstateTaxLiability, lifetimeGiftExclusionUsed

**Charitable Profile (nested on Individual/LegalEntity via PATCH):**
- Extract philanthropic interests, giving history, donor-advised fund info from charitable documents
- Individual: nested under `philanthropicProfile` field in Individual PATCH
- LegalEntity: nested under `charitableDetails` field in LegalEntity PATCH

Tag every extracted field with its `_source` document path.

**IMPORTANT**: For each document, use the document-type-specific extraction checklist in
`references/document_type_patterns.md`. These checklists ensure you don't miss middle names,
occupations, relationship inferences, entity hierarchies, or absence-as-data signals.

### Step 3.4: Sensitive Data Detection (mandatory, first-class artifact)

**Before merging extraction caches, scan for sensitive data that must NEVER enter API
payloads or the main extraction cache.** This includes:

- Credit card numbers (PCI DSS)
- Plaintext passwords / passphrases
- Social media / banking login credentials
- Full SSNs in document body text (outside structured extraction fields)
- Passport numbers, driver's license numbers beyond the structured DL fields
- Wire/ACH routing + account number pairs for unrelated parties
- Private encryption keys or API tokens pasted into documents

**Write a separate artifact**: `altitude_review/sensitive_data.json` — lists every
finding with file, a short description, and a redaction recommendation. This artifact
is visible to the user in the review but is **NEVER merged into `create_payloads.json`,
`extraction_cache.jsonl`, or any API-facing file**.

**Schema**:
```json
[
  {
    "id": 1,
    "file": "Onboarding/Fischer Travel Participation Agreement.pdf",
    "fileNumber": 14,
    "type": "credit_card",
    "description": "Visa ending 9115, expiry 9/29, CVV visible",
    "recommendation": "Rotate card immediately. Redact before uploading document OR upload only the redacted version. Never store in any Altitude field.",
    "severity": "high"
  },
  {
    "id": 2,
    "file": "Family Office/FO Tracker/SRB SIN PW.pdf",
    "type": "credential",
    "description": "Social Insurance Number password (Canadian SIN auth)",
    "recommendation": "Move to password manager (1Password/Bitwarden). Do not upload raw file to Altitude.",
    "severity": "high"
  }
]
```

**Severity levels**:
- `critical` — PCI data (credit cards), plaintext banking passwords → warn user explicitly in Phase 5 review
- `high` — passport #s, SIN passwords, full SSN in body text → flag for redaction
- `medium` — partial credentials, personal-notes-with-secrets → flag, low action required
- `low` — reference notes, flagged for awareness

**Extraction agents must emit sensitive findings to this artifact, NOT to notes or
entity fields.** Each batch writes its own `sensitive_data_batch_{N}.json` which the
orchestrator merges.

**In Phase 5 review**, include a dedicated "Sensitive Data Found" section at the top
(above normal entity updates) so the user sees it immediately. If any `critical`
severity items exist, the review should recommend pausing Phase 6 until rotation is
confirmed.

**Document upload policy**: files containing sensitive data should either be
(a) redacted before upload, (b) excluded from upload with a note, or (c) uploaded with
a warning tag so downstream consumers know the file needs handling. Default: **do NOT
upload files with `severity=critical` unless the user explicitly overrides**.

### Step 3.5: Cross-Document Validation Pass

After extracting from ALL documents, run these mandatory checks before proceeding to Phase 4:

0. **⛔ CRITICAL: Latest-date-wins field resolution** — When the **same field** appears on the
   same entity in multiple documents with different values, the value from the **most recent
   source document wins**. This is the single most important merge rule — it supersedes the
   "most complete value" heuristic below when values actually differ.

   **Determine each document's "as-of date" using this priority** (first match wins):
   1. Explicit "As of" date printed on the document (e.g., "As of 3/31/2026")
   2. Document execution/signing/effective date (e.g., restated trust date, policy effective date)
   3. Filing or issue date (e.g., 1099 tax year = Dec 31 of that year; deed recording date)
   4. Statement period end date (e.g., "November 2025 statement" → 2025-11-30)
   5. Filename-embedded date patterns: `YYYY.MM.DD`, `YYYY-MM-DD`, `MM.DD.YY`, `YYYY_MM` (e.g.,
      `Certificate of IconTrust 2025.05.15.pdf` → 2025-05-15; `DL_2024.docx` → 2024-01-01 as
      month/day unknown fallback)
   6. File `mtime` (filesystem modification time) — only as a **last resort**, as OneDrive/
      Dropbox sync often rewrites mtime to the download time

   **Persist `asOfDate` on every cache entry**: each JSONL line in
   `extraction_cache_batch_{N}.jsonl` must include an `asOfDate` field (ISO format
   YYYY-MM-DD) so Phase 4 can resolve conflicts deterministically.

   **Apply to every scalar field** — address, email, phone, marital status, employer,
   occupation, trustee, beneficiary, policy status, account balance, valuation, etc.
   **Exceptions** (older value wins):
   - `dateOfBirth`, `ssn`, `formationDate`, `taxId` — immutable; first confirmed value wins,
     later contradictions are conflicts to flag
   - `originalBalance`, `originationDate`, `purchaseDate`, `purchasePrice` — historical
     values, don't overwrite with later docs
   - `firstName`, `lastName` at birth — flag middle/preferred name additions as enrichment
     rather than replacement

   **Apply to amendments & restatements**: a "Restated Trust" or "Second Amendment" supersedes
   the original trust agreement for ALL trustee/grantor/beneficiary fields. The original
   becomes historical (set `effectiveTo` on old relationships). Filename tokens to watch:
   `Amendment`, `Restated`, `Restatement`, `Amended`, `Second`, `Third`, `Revised`, `Updated`,
   `Final` (prefer `Final` over `draft`).

   **Apply to account statements**: a November 2025 statement's balance/valuation supersedes
   a July 2025 statement's for the same account. Older statements are read for history, not
   for the current balance.

   **In Phase 5 review**, when a field is overwritten by a later doc, show BOTH values so the
   reviewer can audit the decision:

   | Field | Winning Value | Winning Source (date) | Superseded Value | Superseded Source (date) |
   |-------|--------------|----------------------|------------------|--------------------------|
   | addressLegal | 123 Main St, Denver CO | Driver's License (2025-08-14) | 456 Oak Ave, Boulder CO | 2022 Tax Return (2023-04-15) |

1. **Name enrichment** — For each individual, find the MOST COMPLETE version of their name
   across all documents. Tax returns and account statements often reveal middle names that
   onboarding sheets omit. For actual name *conflicts* (different spellings), apply the
   latest-date-wins rule from item 0.

2. **Relationship inference** — Check for implicit relationships:
   - Joint 1040 filing → SPOUSE relationship
   - No dependents on 1040 → note absence (no PARENT/CHILD needed)
   - K-1 partner info → MEMBER/PARTNER relationships with percentages
   - "Managing member of X" → entity-to-entity MEMBER relationship
   - Joint account title (JT TEN) → both owners get OWNERSHIP at 50%

3. **Multi-hop ownership chains** — When entity A owns entity B which manages entity C,
   create ALL intermediate relationships (A→B OWNERSHIP, B→C MEMBER), not just A→C.

4. **Absence tracking** — Explicitly note when expected data is missing:
   - No estate planning docs → record `estatePlanning.will.hasWill: false`
   - No insurance policies found → flag for review
   - No trusts despite high net worth → flag as potential planning gap

5. **Contact extraction from embedded references** — Every named professional in any document
   becomes a Contact entity: tax preparer on 1040, financial advisor on account statement,
   attorney on trust agreement, CFO mentioned in onboarding sheet.

6. **Insurance ↔ Tangible Asset cross-linking** — For every insurance policy that covers a
   tangible asset, record the linkage so that during Phase 6:
   - The TangibleAsset gets `isInsured: true`, `primaryInsurancePolicyNumber`, `insuredValue`,
     and `insuranceExpirationDate` set
   - Examples: homeowners policy → primary residence, auto policy → each vehicle,
     collections/valuable articles policy → each scheduled item (watches, jewelry, art)
   - Auto insurance schedules list specific vehicles — create a TangibleAsset (VEHICLE)
     for EACH vehicle listed on the policy, not just vehicles found in separate docs

7. **Liability ↔ Tangible Asset cross-linking** — For every liability secured by a tangible
   asset, record the linkage so that during Phase 6:
   - The Liability gets `linkedTangibleAssetId` set to the tangible asset's UUID after creation
   - The Liability gets `isSecured: true` and `collateralDescription` set
   - Examples: mortgage → property, auto loan → vehicle, boat loan → boat,
     art-secured loan → art collection
   - If the loan references a vehicle/property that hasn't been created as a TangibleAsset yet,
     create the TangibleAsset FIRST, then set `linkedTangibleAssetId` on the Liability

### Step 3.7: Self-Audit Pass (Adversarial Review)

Before proceeding to Phase 4, act as your own auditor. Pretend someone else did the extraction
and you are checking their work. Go through these checks:

**Document coverage audit:**
- [ ] List every file in the folder. Is every single one marked as READ? If any file was skipped,
  read it now. Common misses: .docx files that failed to convert, 1099 cover pages dismissed as
  "just a cover letter," photos, emails.

**Entity completeness audit — for each entity type, ask:**
- [ ] **Individuals**: Are there any NAMED PEOPLE in any document who are not yet in my entity list?
  Check: estate planning docs name guardians, trustees, beneficiaries, executors. Insurance docs
  name agents. Tax docs name preparers. Emails name senders. LLC docs name attorneys and managers.
  Every named person is either an Individual or a Contact.
- [ ] **Legal Entities**: Did every entity get created? Common miss: when two spouses each have their
  OWN trust (not one shared trust), that's TWO legal entities. Check LLC operating agreements for
  managing members that are THEMSELVES entities (entity-to-entity chains).
- [ ] **Accounts**: Did every 1099 reveal an account number + custodian? Did every bank/institution
  mentioned in the onboarding sheet get an account created? Did every account statement get its
  account number extracted?
- [ ] **Insurance Policies**: Were all policies from the insurance summary captured? Are there
  additional policy documents in the folder not covered by the summary?
- [ ] **Tangible Assets from Insurance**: Did the auto policy list specific vehicles? Create a
  TangibleAsset (VEHICLE) for each. Did the homeowners policy cover a property? Ensure the
  property TangibleAsset has `isInsured`, `insuredValue`, `primaryInsurancePolicyNumber` set.
  Did a collections/valuable articles policy schedule individual items? Each is a TangibleAsset.
- [ ] **Liability ↔ Asset Links**: For every mortgage, auto loan, boat loan, or secured loan —
  is there a corresponding TangibleAsset? If yes, record `linkedTangibleAssetId`. If the asset
  doesn't exist yet, create it first.
- [ ] **Contacts**: Did EVERY professional mentioned in ANY document get a Contact entity? Check:
  attorneys (estate, corporate, LLC formation — these are often different people), CPAs, insurance
  agents, financial advisors (from 1099s and statements), CFOs, and loan counterparties.

**Relationship completeness audit:**
- [ ] Does every Individual have at least one relationship (OWNERSHIP from household, or PARENT/CHILD)?
- [ ] Does every LegalEntity have at least one relationship (OWNERSHIP, TRUSTEE, GRANTOR)?
- [ ] Does every Account have an OWNERSHIP relationship to its owner?
- [ ] Is there a SPOUSE relationship if the documents show married individuals?
- [ ] Are PARENT→CHILD relationships created for BOTH parents, not just one?
- [ ] Does every Contact have at least one professional relationship (ADVISOR/ATTORNEY/ACCOUNTANT)?

**Data quality audit:**
- [ ] Do any two entities have conflicting addresses? (Flag for user)
- [ ] Are SSNs 9 digits with no dashes?
- [ ] Are phone numbers in E.164-compatible format (digits only)?
- [ ] Are dates in ISO format (YYYY-MM-DD)?
- [ ] Is any sensitive data (passwords, credit cards) accidentally included in entity fields?

---

## Phase 4: Match & Merge — The Core Logic

This is the critical phase. Read `references/match_merge_rules.md` for detailed rules.

### Step 4.1: Deduplicate extracted entities (cross-document merge)

The same person or entity may appear in multiple documents. Merge extracted records
using these identity signals:

**Individuals** — match if ANY of:
- SSN matches exactly (definitive)
- Full name similarity ≥ 0.85 AND (DOB matches OR address matches)
- Full name similarity ≥ 0.65 AND DOB matches AND address matches

**Legal Entities** — match if ANY of:
- EIN/Tax ID matches exactly (definitive)
- Legal name similarity ≥ 0.7 AND entity type matches

**Accounts** — match if ANY of:
- Account number matches exactly (definitive)
- Account name similarity ≥ 0.8 AND custodian matches

**Contacts** — match if ANY of:
- Email matches exactly (definitive)
- Phone matches exactly (definitive)
- Full name similarity ≥ 0.85 AND job title matches

**Tangible Assets** — match if ANY of:
- Address/parcel number matches (for real property)
- VIN/serial number matches
- Name similarity ≥ 0.8 AND category matches AND owner matches

**Insurance Policies** — match if ANY of:
- Policy number matches exactly (definitive)
- Name similarity ≥ 0.8 AND carrier name matches (case-insensitive)
- Carrier + coverage amount + policy category all match (probable)

**Liabilities** — match if ANY of:
- Account number + lender name matches exactly (definitive)
- Name similarity ≥ 0.8 AND lender name matches (case-insensitive)
- Lender + liability type + current balance within 5% tolerance (probable)

When merging across documents for the **same field**:
1. **Different values** → latest-date-wins (see Phase 3.5 Step 0). Record winner, loser, and
   both `asOfDate`s for Phase 5 review.
2. **One null, one non-null** → take the non-null value (no date check needed).
3. **Different levels of specificity** (e.g., "Denver" vs "Denver, CO 80202") → prefer the
   more specific value **only if** its source is newer or equal in age; otherwise latest-date-wins.
4. **Immutable fields** (ssn, dateOfBirth, formationDate, taxId) → first confirmed value wins;
   flag any later contradiction as a hard conflict, don't overwrite silently.

Always track all source documents + their as-of dates on every field.

### Step 4.2: Match extracted entities to Altitude Universe

For each merged extracted entity, attempt to match it to an existing Altitude entity:

**Individual matching against Altitude:**
1. SSN exact match (if both have SSN) → definitive match
2. firstName + lastName exact match (case-insensitive) → strong match
3. firstName + lastName fuzzy match (≥ 0.85 similarity) + DOB match → strong match
4. lastName match + DOB match → probable match (flag for confirmation)
5. No match → candidate for new entity creation

**Legal Entity matching against Altitude:**
1. EIN/taxId exact match → definitive match
2. legalName exact match (case-insensitive) → strong match
3. legalName fuzzy match (≥ 0.8 similarity) + entityType match → strong match
4. No match → candidate for new entity creation

**Account matching against Altitude:**
1. accountNumber exact match → definitive match
2. Account name fuzzy match (≥ 0.85 similarity) + custodian match → strong match
3. No match → candidate for new entity creation

**Contact matching against Altitude:**
1. email exact match → definitive match
2. phone exact match → definitive match
3. firstName + lastName exact match (case-insensitive) + jobTitle match → strong match
4. **FIRM-WIDE contact search** (do this before creating any new Contact): Query
   `GET /api/v1/contact/search?searchFor={firstName}+{lastName}&size=50` to find existing
   Contacts across OTHER households in the same firm. A JPM banker serving Verita may
   already exist under a different household — reuse, don't duplicate. If found:
   - Add the new household as an additional client relationship on the existing Contact
     (relationship: HOUSEHOLD→CONTACT, type ADVISOR/ATTORNEY/etc.)
   - Merge any new fields (if the existing Contact has no email and you have one, PATCH)
   - Do NOT create a duplicate Contact
5. No match anywhere → candidate for new entity creation

**Firm-wide dedup applies especially to**: JPM bankers, attorneys (Kirkland & Ellis,
Venable LLP, etc.), CPAs (large firms serve multiple clients), insurance agents,
Verita's own staff (they work across every household). These should be shared Contacts,
not per-household duplicates.

**Tangible Asset matching against Altitude:**
1. serialOrIdentifier exact match → definitive match
2. Name + category + owner match → strong match
3. Address match (for real property) → strong match
4. No match → candidate for new entity creation

**Insurance Policy matching against Altitude:**
1. policyNumber exact match → definitive match
2. name + carrierName match (case-insensitive) → strong match
3. carrierName + coverageAmount + policyCategory match → probable match
4. No match → candidate for new entity creation

**Liability matching against Altitude:**
1. accountNumber + lenderName exact match → definitive match
2. name + lenderName match (case-insensitive) → strong match
3. lenderName + liabilityType + currentBalance within 5% → probable match
4. No match → candidate for new entity creation

### Step 4.3: Field-level diff against Altitude

For each matched entity, compare every field. Altitude records carry an `updatedAt` timestamp
(the last write time for that entity). Treat `updatedAt` as the Altitude value's effective
date when resolving conflicts.

```
For each field in the extracted entity:
  altitude_value     = existing_altitude_entity[field]
  altitude_asof      = existing_altitude_entity.updatedAt   # last API write
  extracted_value    = extracted_entity[field].value
  extracted_asof     = extracted_entity[field].asOfDate     # from Phase 3.5 Step 0

  IF altitude_value is null/empty AND extracted_value is not null/empty:
    → FILL: Queue this field for automatic update (safe to copy)

  ELIF altitude_value is not null/empty AND extracted_value is not null/empty:
    IF altitude_value == extracted_value:
      → MATCH: Values agree, no action needed
    ELIF field is immutable (ssn, dateOfBirth, formationDate, taxId):
      → HARD_CONFLICT: Values differ on an immutable field — flag for user, do NOT auto-resolve
    ELIF extracted_asof > altitude_asof:
      → SUPERSEDE: Documents have newer info → queue for update, show both values in review
    ELSE:  # altitude_asof >= extracted_asof
      → STALE: Altitude was updated more recently than the document — keep Altitude, show
        both in review in case the user wants to override

  ELIF altitude_value is not null/empty AND extracted_value is null/empty:
    → KEEP: Altitude has data we don't, leave it alone
```

Generate four lists for each entity:
1. **Auto-fill fields** — empty in Altitude, has value from documents
2. **Matching fields** — same value in both (no action)
3. **Supersede fields** — documents newer than Altitude, will overwrite (show diff in review)
4. **Stale fields** — Altitude newer than documents, will keep Altitude (show in review as FYI)
5. **Hard-conflict fields** — immutable fields that differ → block on user decision

### Step 4.4: Extract and validate relationships

From documents, extract all relationships between entities. Use the relationship matrix below
to validate that source→target combinations are allowed:

**Critical Onboarding Relationships:**

| Type | Where Extracted | Source→Target | Needs % | Direction |
|------|----------------|--------------|---------|-----------|
| OWNERSHIP | Operating agreements, account apps, policy declarations, loan docs | IND→LE, IND→ACCT, IND→TA, IND→INS_POL, IND→LIAB, LE→ACCT, LE→INS_POL, LE→LIAB | Yes | Unidirectional |
| INSURED | Insurance policy declarations | IND→INS_POL | No | Unidirectional |
| BENEFICIAL_OWNERSHIP | Trust docs, entity docs | IND→LE | Yes | Unidirectional |
| OWNERSHIP | Household membership | HH→IND | Yes | Unidirectional (Household owns Individuals, NOT the reverse) |
| MEMBER | LLC membership agreements | IND→LE | Yes | Unidirectional |
| PARTNER | Partnership agreements | IND→LE | Yes | Unidirectional |
| TRUSTEE | Trust agreements | IND→LE | No | Unidirectional |
| SUCCESSOR_TRUSTEE | Trust agreements | IND→LE | No | Unidirectional |
| GRANTOR | Trust agreements | IND→LE | No | Unidirectional |
| BENEFICIARY | Trust agreements, TOD forms, will | IND→LE, IND→ACCT | Optional | Unidirectional |
| SPOUSE | Marriage certificates, onboarding sheets | IND→IND | No | Symmetric |
| PARENT | Onboarding sheets | IND→IND | No | Unidirectional |
| CHILD | Onboarding sheets | IND→IND | No | Unidirectional |
| POWER_OF_ATTORNEY | POA documents | IND→IND, IND→LE, IND→ACCT | No | Unidirectional |
| GUARDIAN | Court orders | IND→IND | No | Unidirectional |
| AUTHORIZED_SIGNER | Account apps, corporate resolutions | IND→ACCT, IND→LE | No | Unidirectional |
| OFFICER | Corporate bylaws, filings | IND→LE | No | Unidirectional |
| DIRECTOR | Corporate bylaws, filings | IND→LE | No | Unidirectional |
| ADVISOR | Engagement letters, onboarding sheets | HH→CONTACT, IND→CONTACT, LE→CONTACT | No | Unidirectional (entity points TO the advisor) |
| ACCOUNTANT | Tax returns (preparer name), onboarding sheets | HH→CONTACT, IND→CONTACT, LE→CONTACT | No | Unidirectional (entity points TO the CPA) |
| ATTORNEY | Trust docs (drafting attorney), will, onboarding | HH→CONTACT, IND→CONTACT, LE→CONTACT | No | Unidirectional (entity points TO the attorney) |

**Validation rules:**
- SPOUSE: symmetric (both directions, max 1 per person)
- PARENT: max 2 on target individual
- GUARDIAN: max 1 on target individual
- Percentage REQUIRED for: OWNERSHIP (HH→IND, IND→LE, IND→ACCT), BENEFICIAL_OWNERSHIP, MEMBER (IND→LE for LLC), PARTNER
- All other types: percentage optional

For each relationship, extract:
- sourceEntityId and sourceEntityType
- targetEntityId and targetEntityType
- relationshipType (from matrix above)
- role (optional, e.g., "Managing Member", "Trustee")
- percentage (if type requires it)
- effectiveFrom (when the relationship started, if known)
- effectiveTo (when the relationship ended, if known — null means current/ongoing)
- isPrimary (if relationship has a primary designation)

### Step 4.6: Determine Relationship Currency (Current vs Historical)

**Every relationship must be classified as CURRENT or HISTORICAL before creation.**

Documents often reference people and entities in past tense or with context that indicates
the relationship has ended. Look for these signals:

**Historical relationship indicators:**
- "Former attorney", "prior advisor", "previously represented by"
- Deceased individuals referenced as past trustees, executors, or agents
- Superseded documents (e.g., an amendment that replaces the original operating agreement's
  managing member designation)
- Terminated professional engagements (e.g., "engagement ended 2024")
- Resigned officers/directors ("resigned as trustee effective 3/15/2024")
- Replaced insurance agents, CPAs, or advisors
- Expired powers of attorney or guardianship designations
- Trust amendments that change trustees or beneficiaries (old ones are historical)

**Current relationship indicators:**
- Named in the most recent version of a document (latest amendment, restated agreement)
- Active professional engagement (current CPA on latest tax return, current attorney on
  recent correspondence)
- Named on currently effective insurance policies
- Current LLC members on latest Sunbiz filing
- Active trustees, grantors, beneficiaries on current trust agreement

**How to set effectiveFrom — extract the start date from documents:**

| Relationship Type | Where to Find Start Date |
|---|---|
| OWNERSHIP (LLC) | Operating agreement execution date, or articles of organization filing date |
| OWNERSHIP (Trust) | Trust execution date (original, not restatement) |
| MEMBER/PARTNER | Operating/partnership agreement date, or amendment date that added the member |
| TRUSTEE | Trust agreement date, or amendment date that appointed the trustee |
| GRANTOR | Trust agreement date (original execution) |
| BENEFICIARY | Trust agreement date, or beneficiary designation form date |
| SPOUSE | Marriage date if in documents, otherwise null |
| PARENT/CHILD | Child's date of birth if known |
| ATTORNEY | Engagement letter date, or date of first document they authored |
| ACCOUNTANT | Earliest tax return they prepared, or engagement start date |
| ADVISOR | Advisory agreement date, or earliest account statement showing them |
| INSURED/OWNERSHIP (Insurance) | Policy effective date |
| OWNERSHIP (Tangible Asset) | Purchase date, deed date, or gift date |

**Always prefer explicit dates** from the document (execution dates, filing dates, effective
dates printed on the document). If no explicit date, use the document's creation/signing date
as a proxy. If truly unknown, leave `effectiveFrom` null rather than guessing.

**How to set effectiveTo:**
- Set ONLY for historical/ended relationships
- Use the date the relationship ended if known (resignation date, amendment date, death date)
- **Leave null for all current/active relationships**

**In the review (Phase 5), clearly mark each relationship:**
```markdown
| Source | Target | Type | Status | effectiveFrom | effectiveTo | Notes |
|--------|--------|------|--------|--------------|-------------|-------|
| Brett | Hercules LLC | OWNERSHIP | CURRENT | 2022-09-15 | | 50%, Managing Member |
| Brett | Andrew Comiter | ATTORNEY | CURRENT | 2023-05-22 | | Estate planning |
| Brett | Old CPA Firm | ACCOUNTANT | HISTORICAL | 2020-01-01 | 2023-12-31 | Replaced by Steirman |
```

**When creating relationships via API:**
```json
{
  "sourceEntityType": "INDIVIDUAL",
  "sourceEntityId": "...",
  "targetEntityType": "CONTACT",
  "targetEntityId": "...",
  "relationshipType": "ATTORNEY",
  "effectiveFrom": "2023-05-22",
  "effectiveTo": null
}
```

For historical relationships, set `effectiveTo` and they will be hidden from current
queries but visible in historical views (`/as-of?asOfDate=...`).

### Step 4.5: Handle unmatched entities

Entities extracted from documents with no Altitude match are candidates for creation.
Group them as:
- **New individuals** to be created via `POST /api/v1/individual`
- **New legal entities** to be created via `POST /api/v1/legal-entity`
- **New accounts** to be created via `POST /api/v1/account-financial`
- **New contacts** to be created via `POST /api/v1/contact`
- **New tangible assets** to be created via `POST /api/v1/tangible-asset`
- **New insurance policies** to be created via `POST /api/v1/insurance-policy`
- **New liabilities** to be created via `POST /api/v1/liability`
- **New relationships** to be created via `POST /api/v1/entity-relationship`

### Step 4.7: Role Replacements (Trustee / Advisor / Attorney / Accountant / Officer Changes)

When documents show that a role holder has been **replaced** (new trustee named in an
amendment, new CPA preparing the current tax return, new attorney on the restated trust,
resigned/removed officer), the skill must reflect the change — NOT merely add a new
relationship while leaving the old one active.

**Detect replacement signals:**

- Amendment/restatement documents name a DIFFERENT person in the same role as the original
  (e.g., original 2022 trust names John Smith as trustee; 2023 Second Amendment names
  IconTrust LLC — John Smith is replaced)
- A new document explicitly states a removal/resignation ("effective 3/15/2024, Jane Doe
  resigned as Co-Trustee")
- The **current** filing at a corporate registry lists a different officer than earlier docs
- A newer tax return is prepared by a different CPA firm than prior years

**Action on replacement — depends on whether the prior relationship EXISTS in Altitude:**

**Case A: Prior holder + relationship EXIST in Altitude** (full retire-and-replace path):

1. **Retire the old relationship** by PATCHing `effectiveTo` to the replacement date:
   ```
   PATCH /api/v1/entity-relationship/{oldRelationshipId}
   Content-Type: application/merge-patch+json
   {
     "effectiveTo": "2023-12-18",
     "notes": "Replaced by {new role holder} per {source document}. Superseded at Phase 6."
   }
   ```
   Do NOT delete the old relationship — Altitude needs the historical record (hard-delete
   also triggers the soft-delete uniqueness conflict in rule #21).

2. **Create the new relationship** with `effectiveFrom` = replacement date:
   ```
   POST /api/v1/entity-relationship
   {
     "sourceEntityType": "...", "sourceEntityId": "...",
     "targetEntityType": "...", "targetEntityId": "<new role holder>",
     "relationshipType": "TRUSTEE",
     "effectiveFrom": "2023-12-18",
     "effectiveTo": null,
     "notes": "Replaces {old holder name} retired on same date"
   }
   ```

3. **role_replacements.json** entry: `action: "retire_old_and_create_new"` with both
   old and new relationship IDs for the audit trail.

**Case B: Prior holder does NOT exist in Altitude** (create-new-only path — the common case):

Documents reference a prior trustee/grantor/advisor who was never imported into Altitude
(e.g., a 2012 trust grantor superseded by a 2020 restatement — only the current state
is in Altitude). In this case:

1. **(Optional) Create the historical holder as a Contact** — for audit-trail completeness,
   but not strictly required. Mark with `biography` noting they are historical.

2. **Create the new relationship** as above with `effectiveFrom` = replacement date.

3. **role_replacements.json** entry: `action: "create_new_only"` with `replacesPriorHolder`
   field noting the superseded name for provenance.

**Detection — how to tell which case applies**:

For each relationship marked `isReplacement: true` in the extraction cache:

```python
# Check if any existing Altitude relationship matches the role being replaced
existing = api_get(f"/api/v1/entity-relationship/from/{source_type}/{source_id}")
candidates = [r for r in existing
              if r["relationshipType"] == new_type
              and r["effectiveTo"] is None]  # only active ones
if candidates:
    # Case A: we found the relationship to retire
    action = "retire_old_and_create_new"
    old_relationship_id = candidates[0]["id"]  # or match by target if multiple
else:
    # Case B: no existing relationship to retire, just create
    action = "create_new_only"
```

**If multiple existing relationships match** (e.g., GWN Trust has 2 current TRUSTEE
relationships and the restatement replaces both with a corporate trustee) — retire ALL
matching ones with the same effectiveTo date. Do NOT silently pick one.

**Within Phase 6 execution order**: run retirement PATCHes BEFORE creating new
relationships. Altitude's uniqueness constraint rejects duplicates: you must retire the
old one first so the new POST doesn't hit 409 Conflict.

4. **In Phase 5 review**, render replacements as their own table:

   | Role | Old Holder | New Holder | Replacement Date | Source Document |
   |------|------------|------------|------------------|-----------------|
   | Trustee of DPG Trust | John Smith (CONTACT) | IconTrust LLC (CONTACT) | 2023-12-18 | Second Amendment and Restatement of the DPG Trust (signed 12.18.23) |

**Common replacement scenarios to watch for:**
- Trust restatement naming new trustee, successor trustee, or distribution advisor
- LLC operating agreement amendment naming new managing member
- Corporate board meeting minutes replacing officers
- Current tax return preparer differs from prior-year preparer → old CPA relationship retires
- New engagement letter for attorney/advisor → flag whether it supersedes a prior engagement
- Named-insured change on insurance policy → update OWNERSHIP relationships on the policy

**When unsure**: if the document does not explicitly state a replacement (could be an
additional co-trustee rather than a replacement), leave the old relationship intact and
flag in Open Questions. Never silently retire a relationship on ambiguous signals.

### Step 4.8: Addepar (or any externally-synced) Account Handling — READ-ONLY

Accounts with an active external sync (Addepar, Orion, Black Diamond, custodian direct feed)
are **authoritative from the external source**. The onboarding skill must NOT overwrite
their fields from documents — the external sync will either overwrite the manual change on
its next run (data loss) or produce conflicting records.

**Detect externally-synced accounts:**

After fetching each account in Phase 1.3 (`GET /api/v1/account-financial/{id}`), check:
- `externalIds[]` array — if any entry has `provider: "ADDEPAR"` (or `ORION`, `BLACK_DIAMOND`,
  `SCHWAB`, `FIDELITY`, etc.), the account is externally synced
- `providerDetails.sourceSystemName` — same signal via the older field

Mark each account as one of:

| Status | Meaning | Skill Action |
|--------|---------|--------------|
| `SYNCED_HEALTHY` | Has external provider + non-zero `totalMarketValue` | **Read-only** on core fields; flag discrepancies between docs and Altitude but do NOT PATCH. Still update non-synced metadata (nickname, description, tags, tax notes) if extracted from docs. |
| `SYNCED_BUT_ZERO` | Has external provider but `totalMarketValue == 0` or null `lastSyncedAt` | **Flag to user** — sync configured but not running. Don't update fields; show the user the expected values from docs so they can investigate the sync. |
| `NOT_SYNCED` | No external provider | Normal PATCH/POST behavior — treat like any other entity |

**Fields protected on SYNCED accounts (never PATCH from docs):**

`accountNumber`, `name`, `custodianId`, `accountCategory`, `subCategory`, `taxStatus`,
`wrapper`, `totalMarketValue`, `totalCashBalance`, `totalCostBasis`, `holdings`,
`positions`, `valuations`, `providerDetails.*`, `externalIds[].*`

**Fields still safe to update on SYNCED accounts (manual-only metadata):**

`description`, `tags`, `manualNotes` (if present), `ownershipType`, account-level
PATCH-compatible flags that are not part of the sync contract.

**Discrepancy flagging** — when a document value differs from a SYNCED account's Altitude
value, don't PATCH but DO include in the review under a dedicated section:

```markdown
## Addepar / External Sync Discrepancies — Needs Investigation

| Account | Field | Altitude (from Addepar) | Document Value | Source Doc | asOfDate | Likely Cause |
|---------|-------|------------------------|----------------|------------|----------|--------------|
| DPG Trust Schwab Brokerage | totalMarketValue | $0.00 | $12,450,210 | Glickman_David_portfolio_07-08-2025.xlsx | 2025-07-08 | Sync not running — lastSyncedAt is null |
| DPG Trust Schwab Brokerage | name | "DPG TR BROKERAGE" | "DPG Trust Brokerage Account" | Schwab Account App (draft) | 2024-09-01 | Addepar uses a different display name — cosmetic only |
```

**Zero-value sync alert** — if ANY account has an external provider AND
`totalMarketValue == 0` (or the expected sum from documents is materially nonzero), raise
this as a blocking item in the review:

```markdown
## ⚠ Accounts With Zero Values Despite Active Sync

The following accounts are configured to sync from Addepar but show $0 market value.
This usually means the sync has not run, the external account ID is wrong, or the custodian
connection is broken. Please investigate before proceeding.

- {Account Name} ({account UUID}) — provider: {ADDEPAR}, externalId: {...}, lastSyncedAt: null
```

Do this check **before** Phase 6. The user needs to see this immediately, not buried at the
end of a 200-line review.

---

## Phase 5: Generate Review Package

Create a clear review for the user. This is mandatory before any API calls. Save intermediate
state to allow resuming if needed.

### Summary Report Structure

```markdown
# Altitude Update Review: {Household Name}

## Household
- Status: [EXISTS / NEW]
- Altitude ID: {id or "will create"}

## Matched Entities (will update)

### Individual: {Name} (Altitude ID: {id})
**Auto-fill fields** (empty in Altitude → will populate):
| Field | Extracted Value | Source Document |
|-------|----------------|-----------------|
| dateOfBirth | 1988-02-19 | The Whole Shebang.docx |
| ssn | 126-74-6445 | Driver's License |

**Conflicting fields** (different values → YOUR DECISION):
| Field | Altitude Value | Extracted Value | Source | Action? |
|-------|---------------|-----------------|--------|---------|
| email | old@email.com | new@email.com | Onboarding Sheet | [keep/update] |

### Legal Entity: {Name} (Altitude ID: {id})
[same structure]

### Account: {Name} (Altitude ID: {id})
[same structure]

### Contact: {Name} (Altitude ID: {id})
[same structure]

### Insurance Policy: {Name} (Altitude ID: {id})
[same structure - auto-fill, conflicting, matching fields]

### Liability: {Name} (Altitude ID: {id})
[same structure - auto-fill, conflicting, matching fields]

## New Entities (will create)

### New Individual: {Name}
[key fields that will be populated]

### New Legal Entity: {Name}
[key fields]

### New Account: {Name}
[key fields]

### New Contact: {Name}
[key fields]

### New Insurance Policy: {Name}
[key fields]

### New Liability: {Name}
[key fields]

## Relationships to Create
| Source | Target | Type | Role | Percentage |
|--------|--------|------|------|-----------|
| Podolsky Family (Household) | Brett Podolsky (Individual) | OWNERSHIP | Primary | 50% |
| Podolsky Family (Household) | Michaela Podolsky (Individual) | OWNERSHIP | | 50% |
| Brett Podolsky (Individual) | Hercules Lender LLC (LegalEntity) | OWNERSHIP | Managing Member | 50% |
| Hercules Lender LLC (LegalEntity) | Andrew Comiter (Contact) | ATTORNEY | Estate Planning | - |
| Hercules Lender LLC (LegalEntity) | Jason Evans (Contact) | ATTORNEY | Corporate | - |

## Document Uploads
| Document | Will Associate With | Entity Type | Entity Name | documentSubType |
|----------|-------------------|-------------|------------|-----------------|
| Drivers License.png | Individual | Individual | Brett Podolsky | DRIVERS_LICENSE |
| Operating Agreement.pdf | Legal Entity | LegalEntity | Hercules Lender LLC | OPERATING_AGREEMENT |
| Bank Statement.pdf | Account | AccountFinancial | Chase Brokerage | ACCOUNT_STATEMENT |
| Life Insurance Policy.pdf | Insurance Policy | InsurancePolicy | NWM Whole Life | POLICY_DECLARATION |
| Mortgage Statement.pdf | Liability | Liability | Chase Mortgage | ACCOUNT_STATEMENT |
```

### Document Upload Plan

The review MUST include a complete document upload plan — every file in the folder mapped to
the entity it will be uploaded to and the `documentSubType` to use:

```markdown
## Document Upload Plan

| # | File | Upload To (Entity Type) | Entity Name | documentSubType | Notes |
|---|------|------------------------|-------------|-----------------|-------|
| 1 | DL - Brett.png | Individual | Brett Podolsky | DRIVERS_LICENSE | |
| 2 | Operating Agreement.pdf | LegalEntity | Hercules LLC | OPERATING_AGREEMENT | |
| 3 | Trust Agreement.pdf | LegalEntity | Brett's Trust | TRUST_AGREEMENT | |
| 4 | Will.pdf | Individual | Brett Podolsky | OTHER | Estate planning - Will |
| 5 | Living Will.pdf | Individual | Brett Podolsky | OTHER | Estate planning - Living Will |
| 6 | Healthcare Surrogate.pdf | Individual | Brett Podolsky | OTHER | Healthcare directive |
| 7 | Durable POA.pdf | Individual | Brett Podolsky | POWER_OF_ATTORNEY | |
| 8 | W-2.pdf | Individual | Brett Podolsky | FORM_W2 | |
| 9 | 1099-INT.pdf | Individual | Brett Podolsky | FORM_1099_INT | |
| 10 | Warranty Deed.pdf | TangibleAsset | 3985 NW 53rd St | DEED | |
| 11 | Insurance Summary.pdf | InsurancePolicy | Chubb Homeowners | POLICY_DECLARATION | |
| 12 | Payoff Statement.pdf | Liability | RCF Loan | PAYOFF_STATEMENT | |
| ... | | | | | |
```

Every file in the folder should appear in this table. If a file doesn't map to any entity
(e.g., a duplicate, a blank page, or an internal note), mark it as SKIP with a reason.

### Open Questions & TODOs

The review MUST include a section listing every piece of information that could not be
resolved from the documents alone and requires human input:

```markdown
## Open Questions — Needs Client/Advisor Input

| # | Question | Why It Matters | Blocking? |
|---|----------|---------------|-----------|
| 1 | Which trust owns the MassMutual life policies? ("Podolsky Family Trust" is ambiguous) | Determines OWNERSHIP relationship for insurance policies | Yes — can't create relationship |
| 2 | Is 401 NE Mizner Blvd PH810 owned or rented? | Determines if we create a TangibleAsset | Yes — missing asset |
| 3 | What is Michaela's business? (Michaela Podolsky Inc) | Sets occupation field | No — can leave blank |
| 4 | CFO name for mlund@quinceandcosf.com? | Contact entity is incomplete | No — has email |
| 5 | Correct address: 3895 or 3985 NW 53rd St? (warranty deed conflict) | Property address | Yes — data integrity |
```

Mark each question as **Blocking** (can't create the entity/relationship without an answer)
or **Non-blocking** (can proceed with partial data and fill later).

### Run State File (for incremental reruns)

Write a persistent state file after every Phase 6/7 action to enable incremental reruns:

**File**: `{household_folder}/altitude_review/run_state.json`

```json
{
  "householdId": "7ee864d1-...",
  "runDate": "2026-03-16T15:30:00",
  "apiUrl": "http://localhost:8080",
  "entities": {
    "household": { "id": "7ee864d1-...", "status": "CREATED" },
    "individuals": [
      { "name": "Brett Adam Podolsky", "id": "77097747-...", "status": "CREATED" },
      { "name": "Michaela Dylan Podolsky", "id": "197ce1e3-...", "status": "CREATED" }
    ],
    "legalEntities": [...],
    "contacts": [...],
    "insurancePolicies": [...],
    "liabilities": [...],
    "tangibleAssets": [...],
    "relationships": [
      { "source": "Podolsky Family", "target": "Brett Podolsky", "type": "OWNERSHIP", "id": "8309344b-...", "status": "CREATED" }
    ]
  },
  "documents": {
    "uploaded": [
      { "file": "Identification/Drivers Licenses.png", "entityId": "77097747-...", "documentId": "abc123-...", "status": "UPLOADED" },
      { "file": "LLC/Hercules/Operating Agreement.pdf", "entityId": "da72184b-...", "documentId": "def456-...", "status": "UPLOADED" }
    ],
    "failed": [
      { "file": "LLC/RCF/4th Amended Note.pdf", "error": "HTTP 500", "status": "FAILED" }
    ],
    "sessionId": "882fea65-..."
  },
  "estatePlanningPatched": ["77097747-...", "197ce1e3-..."],
  "openQuestions": [...]
}
```

**On rerun behavior:**
- Before Phase 1: Check if `run_state.json` exists. If yes, load it and ask the user:
  "Previous run found (dated {runDate}). Options: (A) Resume — skip already-created entities,
  only create missing ones + retry failed uploads. (B) Force rerun — re-extract all documents
  and recreate everything. (C) Upload only — skip entity creation, just upload remaining documents."
- **Resume mode**: For each entity in the state file with status CREATED, skip creation.
  For documents with status UPLOADED, skip upload. For FAILED documents, retry.
- **Force mode**: Delete the state file and start fresh.
- **Upload only**: Skip Phases 1-6, only run Phase 7 using entity IDs from the state file.

Update the state file after EVERY successful API call (not just at the end). This way, if the
run is interrupted mid-way, the next run can resume from where it stopped.

### Save Artifacts

All review artifacts go to `{household_folder}/altitude_review/` (the review directory is
ALWAYS created at the root of the household folder — sibling to the source document
subfolders, never buried deeper):

- `review.md` — complete human-readable review (ALL sections above)
- `file_tracker.md` — every file with READ status and extraction summary
- `altitude_universe.json` — initial state from Phase 1
- `create_payloads.json` — POST requests for new entities
- `patch_payloads.json` — PATCH requests for existing entities (if matching)
- `relationships_to_create.json` — relationship creation plan
- `role_replacements.json` — trustee/advisor/attorney/officer replacements (see Phase 4.7)
- `addepar_discrepancies.json` — doc-vs-sync mismatches for synced accounts (see Phase 4.8)
- `document_uploads.json` — document upload plan (file → entity → subType)
- `supersede_log.json` — **REQUIRED, ALWAYS WRITE** when any latest-date-wins decision was made.
  Audit trail of every field where a later document superseded an earlier one (or overrode an
  existing Altitude value). Format:
  ```json
  [
    {
      "entityType": "Individual",
      "entityName": "Seth Boro",
      "entityId": "e9f2...",
      "field": "addressLegal",
      "winningValue": "429 Elizabeth St, San Francisco CA 94114",
      "winningSource": "DPG 2022 Trust Amendment (signed 2020-04-16)",
      "winningAsOfDate": "2020-04-16",
      "losingValue": "221 Gold Mine Drive, San Francisco CA 94131",
      "losingSource": "Onboarding Sheet 2018 draft",
      "losingAsOfDate": "2018-06-01",
      "classification": "SUPERSEDE",
      "appliedToAltitude": true,
      "reviewApprovedAt": "2026-04-17T16:40:00Z"
    }
  ]
  ```
  Categories: `FILL` (empty→value), `MATCH` (no change), `SUPERSEDE` (newer wins), `STALE`
  (older, keep Altitude), `HARD_CONFLICT` (immutable fields — never auto-resolve). This file
  is the audit trail for latest-date-wins decisions — auditors and future onboarding sessions
  can inspect to understand why a field has its current value.
- `sensitive_data.json` — **REQUIRED if any sensitive data was found**, see Step 3.4.
- `open_questions.json` — **REQUIRED, ALWAYS WRITE THIS FILE** even if empty. Structured JSON
  for programmatic tracking across families. Format:
  ```json
  [
    {"id": 1, "question": "Does client have a Will?", "category": "estate_planning", "blocking": false, "entity": "Phineas Barnes", "resolved": false, "resolution": null},
    {"id": 2, "question": "Joanne DOB: 10/02 vs 10/21?", "category": "data_conflict", "blocking": false, "entity": "Joanne Shih", "resolved": false, "resolution": null}
  ]
  ```
  This file must ALSO be written — embedding questions only in review.md is insufficient.
  Categories: `estate_planning`, `data_conflict`, `missing_data`, `ownership`, `insurance`, `address`, `account`, `other`, `addepar_sync`, `family_status`, `file_access`, `asset_detail`, `entity_detail`, `liability_detail`, `advisor_relationships`, `schema`, `holdings_data`, `account_status`
- `run_state.json` — persistent state for incremental reruns (entity IDs, document upload status, failures)

### Approval Q&A Trail (REQUIRED — separate from altitude_review/)

In ADDITION to the structured `open_questions.json` inside `altitude_review/`, **write a
human-readable Q&A tracking file at the ROOT of the household folder** (sibling to
`altitude_review/`, alongside the source subfolders). This file captures every question
asked during validation/approval, the user's response, and when each was resolved.

**File name**: `altitude_questions_{YYYY-MM-DD}.md` — dated, so multiple onboarding sessions
or revisits produce separate files and the audit trail survives.

**File location**: `{household_folder}/altitude_questions_{YYYY-MM-DD}.md` — the household
root, NOT inside `altitude_review/`. Reason: the Q&A log is user-facing and survives
cleanup/rebuild of the review directory.

**Required template** (populate as the session progresses; update in place when user responds):

```markdown
# Altitude Onboarding — Approval Questions

**Household**: {name}
**Altitude Household ID**: {uuid or "new"}
**Firm**: {firm}
**Session Date**: {YYYY-MM-DD}
**Source folder**: {absolute path}
**Review artifacts**: `./altitude_review/review.md`

## Session Timeline

| When | Phase | Actor | Note |
|---|---|---|---|

## Pre-Approval Blocking Questions

### Q1 — {short title}
**Severity**: Blocking | Non-blocking
**Category**: {one of the categories above}

**Question**: {full question with context}

**Proposed answer** (skill's best guess; user can confirm with "yes" or override):
{the skill's recommended resolution, with rationale}

Example: "Use tax return SSN `614-75-8183` (authoritative) and overwrite Altitude's
invalid `140965906`. Rationale: SSA issues SSNs in ranges 001-665, 667-699, 750-772;
140-965-906 falls outside all ranges, so it's data entry error. 2022 + 2023 1040 both
confirm 614-75-8183."

**User Response**: _awaiting_ | {response text — "yes" = accept proposed answer}
**Resolved**: _pending_ | YYYY-MM-DD HH:MM
**Resolution**: _pending_ | {final decision — populated from Proposed answer if user said "yes"}

## Non-Blocking Open Questions (see open_questions.json for full list)

{summary list — full detail lives in open_questions.json}

## Post-Approval Questions (populated during Phase 6/7)

{append each mid-execution question as it arises}

## Approval Record

**Final approval granted at**: _pending_ | YYYY-MM-DD HH:MM
**Approver**: _pending_ | {user name/role}
**Scope approved**:
- [ ] {each proposed change item}

**Any excluded items**: _pending_ | {list}
```

**Update rules**:
- Write the file at Phase 5 completion (presenting the review to the user).
- **Append** additional questions as they arise during Phase 6/7 under "Post-Approval Questions".
- **Update in place** when the user responds — fill the `User Response`, `Resolved`, and
  `Resolution` fields with timestamps.
- **Do NOT overwrite** prior session's file — if running a re-onboarding for the same family,
  use today's date in the filename so both audit trails survive.

### Upload Q&A File to Household as Document

As the final step of Phase 7, upload the `altitude_questions_{YYYY-MM-DD}.md` file to the
primary individual in Altitude (Households don't support direct document upload — see Phase 7
note). Use these parameters:

```
POST /api/v1/individual/{primaryIndividualId}/document?sessionId={sessionId}&skipDuplicates=true
createRequest:
  title: "Altitude Onboarding Q&A — {Household Name} — {YYYY-MM-DD}"
  description: "Validation and approval questions from onboarding session on {YYYY-MM-DD}."
  documentSubType: "OTHER"
  contentType: "MARKDOWN"
```

After upload, create entity associations so the document appears on both the Individual AND
the Household:

```
POST /api/v1/document/{docId}/associations?entityType=INDIVIDUAL&entityId={primaryIndividualId}&associationType=OWNER&entityDisplayName={name}
POST /api/v1/document/{docId}/associations?entityType=HOUSEHOLD&entityId={householdId}&associationType=SUBJECT&entityDisplayName={householdName}
```

This way future onboarding sessions (and auditors) can reconstruct the decision trail from
within Altitude without needing access to the source document folder.

---

Present the review to the user and wait for approval + conflict resolution.

---

## Phase 6: Push Updates to Altitude (Only After Approval)

After the user approves and resolves all conflicts:

### Step 6.1: Update existing entities (PATCH)

Use PATCH for partial updates — only send the fields that need filling or updating:

```
PATCH /api/v1/individual/{id}
Content-Type: application/merge-patch+json
X-API-Key: {api_key}

{
  "dateOfBirth": "1988-02-19",
  "ssn": "126746445",
  "email": "brett@example.com",
  "addressLegal": {
    "addressLine1": "3985 NW 53rd Street",
    "addressLine2": "Suite 200",
    "city": "Boca Raton",
    "state": "FL",
    "postalCode": "33496",
    "country": "US",
    "addressType": "PRIMARY"
  }
}
```

**IMPORTANT**: Only send fields being updated. Never include READ_ONLY computed fields like
`totalMarketValue`, `fullName`, `createdAt`, `updatedAt`, `id`. PATCH ignores null values.

Address structure fields:
- `addressLine1` (required)
- `addressLine2` (optional)
- `city` (required)
- `state` (required, 2-char US state code or province)
- `postalCode` (required, 1-10 chars)
- `country` (required, CountryCode enum like "US", "CA", "GB")
- `addressType` (optional, AddressType enum: "PRIMARY" or "ADDITIONAL")

Process in order: Household → Individuals → Legal Entities → Accounts → Contacts → Tangible Assets (via subtype endpoints) → Insurance Policies → Liabilities. Then create all relationships, then PATCH estate planning.

If an API call fails, log it, save state, and ask user to retry or continue with others.

### Step 6.2: Create new entities (POST)

For entities that don't exist in Altitude yet:

```
POST /api/v1/individual
X-API-Key: {api_key}
Content-Type: application/json

{
  "firstName": "Brett",
  "lastName": "Podolsky",
  "dateOfBirth": "1988-02-19",
  "ssn": "126746445",
  "email": "brett@example.com",
  "addressLegal": { ... }
}
```

For new legal entities (trusts, LLCs, corporations):

```
POST /api/v1/legal-entity
X-API-Key: {api_key}
Content-Type: application/json

{
  "legalName": "Hercules Lender LLC",
  "entityType": "LLC",
  "formationDate": "2015-03-20",
  "jurisdiction": "FL",
  "incorporationState": "FL",
  "incorporationCountry": "UNITED_STATES",
  "taxId": "65-1234567",
  "llcManagementType": "MEMBER_MANAGED"
}
```

For new accounts:

```
POST /api/v1/account-financial
X-API-Key: {api_key}
Content-Type: application/json

{
  "name": "Chase Brokerage Account",
  "accountNumber": "123456789",
  "accountCategory": "INDIVIDUAL",
  "subCategory": "INDIVIDUAL",
  "custodianId": "{custodian_id_from_altitude_universe}"
}
```

For new contacts:

```
POST /api/v1/contact
X-API-Key: {api_key}
Content-Type: application/json

{
  "firstName": "Jane",
  "lastName": "Smith",
  "jobTitle": "Financial Advisor",
  "biography": "Smith & Associates",
  "email": "jane.smith@example.com",
  "phoneNumberPrimary": "555-1234"
}
```

For new insurance policies:

```
POST /api/v1/insurance-policy
X-API-Key: {api_key}
Content-Type: application/json

{
  "name": "Northwestern Mutual Whole Life",
  "policyCategory": "LIFE",
  "policyStatus": "ACTIVE",
  "policyNumber": "POL-2024-789456",
  "carrierName": "Northwestern Mutual",
  "coverageAmount": 2000000.00,
  "annualPremium": 12500.00,
  "effectiveDate": "2020-01-01",
  "firstPaymentDate": "2020-02-01",
  "deathBenefit": 2000000.00,
  "cashValue": 125000.00,
  "lifePolicyType": "WHOLE_LIFE"
}
```

For new liabilities:

```
POST /api/v1/liability
X-API-Key: {api_key}
Content-Type: application/json

{
  "name": "Chase Home Mortgage",
  "liabilityType": "MORTGAGE",
  "liabilityStatus": "CURRENT",
  "lenderName": "JPMorgan Chase",
  "originalBalance": 500000.00,
  "currentBalance": 425000.00,
  "balanceAsOfDate": "2026-03-01",
  "interestRate": 6.5,
  "interestRateType": "FIXED",
  "monthlyPayment": 2750.00,
  "paymentFrequency": "MONTHLY",
  "originationDate": "2022-06-15",
  "maturityDate": "2052-06-15",
  "isSecured": true,
  "isInterestDeductible": true,
  "interestDeductionType": "MORTGAGE_INTEREST"
}
```

For new tangible assets (use SUBTYPE-SPECIFIC endpoints — NOT the base `/tangible-asset`):

```
POST /api/v1/tangible-asset/real-property
X-API-Key: {api_key}
Content-Type: application/json

{
  "name": "3985 NW 53rd St, Boca Raton, FL 33496",
  "category": "REAL_PROPERTY",
  "assetType": "PRIMARY_RESIDENCE",
  "description": "6833 sq ft, concrete block, built 1996",
  "serialOrIdentifier": "06-42-47-04-02-000-0390",
  "location": "Palm Beach County, FL",
  "currentValue": 5674000,
  "isInsured": true,
  "insuredValue": 5674000
}
```

```
POST /api/v1/tangible-asset/vehicle
{
  "name": "2024 Porsche 911",
  "category": "VEHICLE",
  "assetType": "CAR",
  "serialOrIdentifier": "WP0CD2A94RS257187",
  "currentValue": 317480,
  "isInsured": true
}
```

```
POST /api/v1/tangible-asset/luxury
{
  "name": "AP Royal Oak Offshore",
  "category": "LUXURY",
  "assetType": "WATCH",
  "serialOrIdentifier": "LH0496U",
  "currentValue": 31928,
  "isInsured": true,
  "insuredValue": 31928
}
```

Available subtype endpoints: `/real-property`, `/vehicle`, `/luxury`, `/collectible`, `/other`.
After creation, add OWNERSHIP relationships (IND→TA with percentage).

**Scheduled items from insurance policies**: If an insurance summary or collections policy
schedules individual items (watches, jewelry, art, wine) with values, create EACH item as a
separate TangibleAsset via the `/luxury` or `/collectible` endpoint. Include:
- `name` — item description (e.g., "AP Royal Oak Offshore")
- `serialOrIdentifier` — serial number if listed
- `currentValue` — scheduled/appraised value
- `isInsured: true`, `insuredValue` — same as scheduled value
These are real assets with real values and should NOT be deferred or marked as optional.

### Step 6.2.1: Cross-Entity Linking (AFTER all tangible assets, insurance policies, and liabilities are created)

After creating tangible assets, insurance policies, and liabilities, apply cross-entity links:

**Insurance → Tangible Asset:** For each insurance policy that covers a tangible asset, PATCH the
tangible asset with insurance details:
```
PATCH /api/v1/tangible-asset/{assetId}
{
  "name": "<existing name — include to avoid validation error with custom 'is required' messages>",
  "isInsured": true,
  "primaryInsurancePolicyNumber": "<policy number>",
  "insuredValue": <coverage amount>,
  "insuranceExpirationDate": "<expiration date>"
}
```
Common mappings:
- Homeowners policy → primary residence
- Auto policy → each vehicle listed on the policy
- Flood policy → primary residence
- Collections/valuable articles → each scheduled item
- Boat/yacht policy → boat tangible asset

**TangibleAssetInsurance child entries:** In addition to the summary PATCH above, create
detailed insurance child records for each asset-policy linkage. This populates the
"Insurance Policies" tab on the asset detail view:
```
POST /api/v1/tangible-asset/{assetId}/insurance
{
  "policyNumber": "<policy number>",
  "carrier": "<carrier name>",
  "insuranceType": "<HOMEOWNERS|FLOOD|AUTO|JEWELRY|COLLECTIBLES|FINE_ART|MARINE|AVIATION|UMBRELLA|VALUABLE_ARTICLES>",
  "coverageAmount": <coverage amount — REQUIRED, NOT NULL>,
  "annualPremium": <annual premium if known>,
  "effectiveDate": "<YYYY-MM-DD — REQUIRED, NOT NULL>",
  "expirationDate": "<YYYY-MM-DD — REQUIRED, NOT NULL>",
  "isActive": true,
  "isAgreedValue": <true for agreed-value policies (vehicles, jewelry)>,
  "coverageNotes": "<description of coverage>"
}
```
**CRITICAL**: `effectiveDate`, `expirationDate`, and `coverageAmount` are NOT NULL in the
database — omitting them returns HTTP 409 (data integrity error), not 400. Always include
all three fields. Use policy dates from the insurance summary/declaration documents.

Create ONE entry per asset-policy combination:
- Primary residence gets 3 entries: HOMEOWNERS + FLOOD + wind (HOMEOWNERS type with notes)
- Each vehicle gets 1 entry: AUTO with agreed value as coverageAmount
- Each jewelry/watch gets 1 entry: JEWELRY with scheduled value as coverageAmount
- Golf cart gets 1 entry: AUTO

**Liability → Tangible Asset:** For each secured liability, PATCH the liability with the
tangible asset link:
```
PATCH /api/v1/liability/{liabilityId}
{
  "linkedTangibleAssetId": "<tangible asset UUID>",
  "isSecured": true,
  "collateralDescription": "<asset name or address>"
}
```
Common mappings:
- Mortgage → property tangible asset
- Auto loan → vehicle tangible asset
- Boat loan → boat tangible asset
- Art-secured loan → art/collectible tangible asset

**Order matters:** Create tangible assets BEFORE liabilities and insurance policies, so you
have the UUIDs available for linking.

**Auto policy vehicles:** When an auto insurance policy lists specific vehicles (make/model/year),
create a TangibleAsset (VEHICLE) for EACH vehicle via `/api/v1/tangible-asset/vehicle`. Then
PATCH each vehicle with `isInsured: true` and the auto policy number. Then create OWNERSHIP
relationships from the vehicle owner to each vehicle.

For estate planning (nested on Individual PATCH — NOT a standalone entity):

```
PATCH /api/v1/individual/{id}
X-API-Key: {api_key}
Content-Type: application/merge-patch+json

{
  "estatePlanning": {
    "will": {
      "hasWill": true,
      "willDate": "2024-01-15",
      "executorName": "Jane Smith",
      "jurisdiction": "New York"
    },
    "healthcare": {
      "hasHealthcareDirective": true,
      "agentName": "Jane Smith"
    },
    "financialPoa": {
      "hasFinancialPoa": true,
      "type": "DURABLE",
      "agentName": "Jane Smith"
    }
  }
}
```

Record the returned IDs for relationship creation.

**Insurance policy relationships** (create after policy is created):
- OWNERSHIP: Individual/LegalEntity → InsurancePolicy (who owns/pays for the policy)
- INSURED: Individual → InsurancePolicy (who is covered by the policy)
- BENEFICIARY: Individual → InsurancePolicy (who receives the payout)

### Step 6.2.5: Pre-baked enum mapping table

**Altitude's relationship `relationshipType` enum is smaller than what documents typically
describe.** Historical runs discovered these remappings via 400 errors — apply them
automatically before POSTing to avoid wasted round-trips. Preserve the original semantic
via the `role` field.

| Document-described type | Altitude API type | `role` field | Notes |
|---|---|---|---|
| TRUST_PROTECTOR | TRUSTEE | "Trust Protector" | Trust agreements use this term for oversight role separate from day-to-day trustee |
| SUCCESSOR_TRUST_PROTECTOR | TRUSTEE | "Successor Trust Protector #N" | Include priority |
| INVESTMENT_COMMITTEE_MEMBER | ADVISOR | "Investment Committee" | |
| POWER_OF_APPOINTMENT_COMMITTEE_MEMBER | ADVISOR | "Power of Appointment Committee" | |
| DISTRIBUTION_COMMITTEE_MEMBER | ADVISOR | "Distribution Committee" | |
| CRUMMEY_POWER_HOLDER | BENEFICIARY | "Crummey Power Holder" | |
| EMPLOYMENT | EMPLOYEE | (firm name + title) | The IND→LE direction requires EMPLOYEE |
| EMPLOYER | EMPLOYEE | (flip source/target first) | Normalize to IND→LE EMPLOYEE |
| FAMILY | SIBLING | "Brother" / "Sister" / "Cousin" | FAMILY is a category, SIBLING is the concrete enum |
| IN_LAWS | FAMILY | "In-law (parent/sibling)" | No direct enum — use FAMILY subtype |
| DONOR | MEMBER | "Donor" | For charitable/DAF contributions |
| FOUNDER | MEMBER | "Founder" | For foundation/LLC formation role |
| MANAGER | OFFICER | "Manager" | LLC managers map to OFFICER type |
| MANAGING_MEMBER | OFFICER | "Managing Member" + pct | Also create MEMBER relationship with pct |
| REGISTERED_AGENT | ATTORNEY | "Registered Agent" | Non-litigation legal role |
| NAMED_INSURED | INSURED | — | Direct mapping |
| INSURED_DRIVER | INSURED | "Driver" | Auto policies list multiple drivers |
| TREASURER | OFFICER | "Treasurer" | |
| SECRETARY | OFFICER | "Secretary" | |
| PRESIDENT | OFFICER | "President" | |
| VICE_PRESIDENT | OFFICER | "Vice President" | |
| CHAIRMAN | OFFICER | "Chairman" | |
| CEO | OFFICER | "Chief Executive Officer" | |
| CFO | OFFICER | "Chief Financial Officer" | |
| COO | OFFICER | "Chief Operating Officer" | |

**Account `subCategory` remaps** (account POSTs with document-described values that Altitude rejects):

| Document-described | Altitude API | Notes |
|---|---|---|
| "Private Investment Fund" | LIMITED_LIABILITY_COMPANY | LLC structure |
| "Statutory/Business Trust" | IRREVOCABLE_TRUST | Trust with business purpose |
| "Donor-Advised Fund" | OTHER | DAF not a first-class type; use DAF in name/description |
| "Private Foundation" | OTHER | Use charitableDetails fields |
| "Carried Interest" | OTHER | Include "Carry" in name |
| "CARRY" | OTHER | Same |

**Liability `liabilityType` remaps**:

| Document-described | Altitude API | Notes |
|---|---|---|
| INTRAFAMILY_LOAN | PRIVATE_LOAN | |
| INTERCOMPANY_LOAN | PRIVATE_LOAN | |
| REVOLVING_CREDIT | CREDIT_LINE | |
| HELOC | HOME_EQUITY_LOC | |

**LegalEntity `entityType` remaps**:

| Document-described | Altitude API | Notes |
|---|---|---|
| DONOR_ADVISED_FUND | OTHER | Use charitableDetails |
| PRIVATE_FOUNDATION | FOUNDATION | Verify enum exists; else OTHER |
| DISREGARDED_LLC | LLC | Use taxClassification=DISREGARDED_ENTITY |
| SERIES_LLC | LLC | Note series in description |

**LegalEntity `taxClassification` remaps**:

| Document-described | Altitude API |
|---|---|
| "Partnership (Form 1065)" | PARTNERSHIP |
| "Disregarded Entity" | DISREGARDED_ENTITY |
| "C Corporation" / "C-Corp" | C_CORP |
| "S Corporation" / "S-Corp" | S_CORP |

**Apply these proactively.** When building POST payloads, run the values through these
maps before sending. On any unknown enum value that the server rejects with 400, fall
back to `OTHER` (or the closest match above) and record the remap in
`run_state.enum_mappings[<original>]`.

### Step 6.3: Create relationships

```
POST /api/v1/entity-relationship
X-API-Key: {api_key}
Content-Type: application/json

{
  "relationshipType": "OWNERSHIP",
  "sourceEntityId": "{household_id}",
  "sourceEntityType": "HOUSEHOLD",
  "targetEntityId": "{individual_id}",
  "targetEntityType": "INDIVIDUAL",
  "isPrimary": true,
  "percentage": 50
}
```

**CRITICAL**: Household-to-Individual relationships use **OWNERSHIP from HOUSEHOLD → INDIVIDUAL**
(the household "owns" its members). Do NOT use MEMBER (IND→HH) — that is for LLC membership only.
Direction matters: the household is the SOURCE, the individual is the TARGET.

**Use generational roles, not "adult/child" assumptions.** Family members should be categorized
by generation (G1 = oldest generation, G2 = their children, G3 = grandchildren), not by age.
An adult child (age 25) is still G2. A minor grandchild is G3.

- **ALL members get percentage = 100**.** The household "owns" 100% of each member. This is
  what drives the valuation rollup — each member's account values roll up fully to the
  household. Do NOT use 50/50 for couples or 0 for children.
- **isPrimary**: Set to true for the first G1 member only.
- Use generational roles (G1/G2/G3) in the `role` field for display purposes only.

Examples:
```
# Couple with 3 minor children
HOUSEHOLD → Spouse1 (OWNERSHIP, isPrimary: true, percentage: 100, role: "G1")
HOUSEHOLD → Spouse2 (OWNERSHIP, percentage: 100, role: "G1")
HOUSEHOLD → Child1 (OWNERSHIP, percentage: 100, role: "G2")
HOUSEHOLD → Child2 (OWNERSHIP, percentage: 100, role: "G2")
HOUSEHOLD → Child3 (OWNERSHIP, percentage: 100, role: "G2")

# Single parent with adult children
HOUSEHOLD → Parent (OWNERSHIP, isPrimary: true, percentage: 100, role: "G1")
HOUSEHOLD → AdultChild1 (OWNERSHIP, percentage: 100, role: "G2")
HOUSEHOLD → AdultChild2 (OWNERSHIP, percentage: 100, role: "G2")

# Multi-generational
HOUSEHOLD → Grandparent1 (OWNERSHIP, isPrimary: true, percentage: 100, role: "G1")
HOUSEHOLD → Grandparent2 (OWNERSHIP, percentage: 100, role: "G1")
HOUSEHOLD → AdultChild (OWNERSHIP, percentage: 100, role: "G2")
HOUSEHOLD → Grandchild1 (OWNERSHIP, percentage: 100, role: "G3")
HOUSEHOLD → Grandchild2 (OWNERSHIP, percentage: 100, role: "G3")
```

Validate each relationship against the matrix in Phase 4.5 before posting. If validation fails,
flag for user review.

---

## Phase 7: Upload Documents

After entities are created/updated, upload source documents and associate them with
the correct entity.

### contentType enum (EXACT values accepted by API — use precisely)

Altitude's `DocumentContentType` enum accepts exactly these 18 values — nothing else:

```
CSV, DOC, DOCX, GIF, HTML, JPG, JSON, MP3, MP4,
PDF, PNG, PPT, PPTX, TXT, XLS, XLSX, XML, ZIP
```

**NOT supported** (must be converted before upload): `EML`, `MD`, `MSG`, `RTF`, `HEIC`, `TIF/TIFF`, `WEBP`.

**File-extension → contentType mapping** (use this exactly — NEVER pass `OTHER`, `EML`, or `MARKDOWN`):

| Extension | contentType | Notes |
|---|---|---|
| `.pdf` | `PDF` | |
| `.docx` | `DOCX` | |
| `.doc` | `DOC` | |
| `.xlsx` | `XLSX` | |
| `.xls` | `XLS` | |
| `.pptx` | `PPTX` | |
| `.ppt` | `PPT` | |
| `.jpg`, `.jpeg` | `JPG` | |
| `.png` | `PNG` | |
| `.gif` | `GIF` | |
| `.csv` | `CSV` | |
| `.txt` | `TXT` | |
| `.json` | `JSON` | |
| `.xml` | `XML` | |
| `.html`, `.htm` | `HTML` | |
| `.mp3` | `MP3` | |
| `.mp4`, `.mov` (convert) | `MP4` | |
| `.zip` | `ZIP` | |
| `.md` | **convert to `.txt`** then upload as `TXT` | Rename extension + upload |
| `.eml` | **convert to `.txt`** (parse headers+body with Python `email` module) then `TXT` | |
| `.msg` | **convert to `.eml`→`.txt`** or skip | Outlook proprietary; extract-msg library |
| `.rtf` | **convert to `.txt`** via `textutil -convert txt` | |
| `.heic` | **convert to `.jpg`** via `sips -s format jpeg` (macOS) or `heif-convert` | |
| `.tif`, `.tiff` | **convert to `.pdf`** via `tiff2pdf` or reject | |

**.eml conversion helper** (apply before upload):

```python
# eml_to_txt.py
import email, sys, pathlib
p = pathlib.Path(sys.argv[1])
with open(p, 'rb') as f:
    msg = email.message_from_binary_file(f)
out = [f"From: {msg['From']}", f"To: {msg['To']}", f"Date: {msg['Date']}", f"Subject: {msg['Subject']}", ""]
for part in msg.walk():
    if part.get_content_type() == 'text/plain':
        body = part.get_payload(decode=True)
        if body: out.append(body.decode(errors='replace'))
out_path = p.with_suffix('.txt')
out_path.write_text('\n'.join(out))
print(out_path)
```

Then upload with `contentType=TXT` and `documentSubType=CORRESPONDENCE` (or entity-specific equivalent).

### documentSubType — intelligent selection (NEVER default to OTHER)

Each entity type has its own `documentSubType` enum with rich taxonomies. Classify every
document by filename pattern + content, matching to the most specific valid value. Fall back
to `OTHER` ONLY when nothing fits — and log the unmatched pattern in a `documentSubType_unmatched.json`
artifact so future runs can improve the mapping.

**Per-entity enums** (full lists — discoverable via `Grep "documentSubType" api.json`):

#### IndividualDocumentCreateRequestDto.documentSubType (62 values)

Identity: `PASSPORT`, `DRIVERS_LICENSE`, `ENHANCED_DRIVERS_LICENSE`, `NATIONAL_ID`, `STATE_ID`,
`BIRTH_CERTIFICATE`, `SOCIAL_SECURITY_CARD`, `CITIZENSHIP_CERTIFICATE`, `CERTIFICATE_OF_NATURALIZATION`,
`PERMANENT_RESIDENT_CARD`, `MILITARY_ID`, `GLOBAL_ENTRY_CARD`, `TRIBAL_ID`, `CONSULAR_ID`,
`FOREIGN_VOTER_CARD`, `REFUGEE_TRAVEL_DOCUMENT`, `DIPLOMATIC_ID`

Tax: `FORM_1040`, `FORM_W2`, `FORM_W9`, `FORM_1099_DIV`, `FORM_1099_INT`, `FORM_1099_B`,
`FORM_1099_MISC`, `FORM_1099_R`, `FORM_K1_1065`, `FORM_K1_1120S`, `FORM_W8BEN`, `STATE_TAX_RETURN`,
`PROPERTY_TAX_DOCUMENTS`

Compliance: `ACCREDITED_INVESTOR_VERIFICATION`, `QUALIFIED_PURCHASER_VERIFICATION`,
`AML_QUESTIONNAIRE`, `KYC_DOCUMENTATION`, `FATCA_CERTIFICATION`, `CRS_SELF_CERTIFICATION`,
`OFAC_SCREENING`, `PEP_DISCLOSURE`

Financial: `BANK_STATEMENT`, `INVESTMENT_STATEMENT`, `NET_WORTH_STATEMENT`, `CREDIT_REPORT`,
`EMPLOYMENT_VERIFICATION`, `INCOME_VERIFICATION`, `FINANCIAL_STATEMENT`, `UTILITY_BILL`,
`LEASE_AGREEMENT`, `PROPERTY_DEED`, `MORTGAGE_STATEMENT`

Estate/Legal: `POWER_OF_ATTORNEY`, `NAME_CHANGE_DOCUMENT`, `MARRIAGE_CERTIFICATE`, `DIVORCE_DECREE`,
`COURT_ORDER`, `LIVING_WILL`, `LAST_WILL_AND_TESTAMENT`, `HEALTHCARE_SURROGATE`

Investment: `SUBSCRIPTION_AGREEMENT`, `INVESTMENT_POLICY_STATEMENT`, `INVESTMENT_QUESTIONNAIRE`,
`INVESTOR_ACCREDITATION`

Fallback: `OTHER`

#### LegalEntityDocumentCreateRequestDto.documentSubType (84 values)

Trust: `TRUST_AGREEMENT`, `TRUST_CERTIFICATION`, `TRUST_AMENDMENTS`, `REVOCABLE_TRUST_DOCUMENT`,
`IRREVOCABLE_TRUST_DOCUMENT`, `TRUSTEE_CERTIFICATION`, `BENEFICIARY_DESIGNATION`,
`TRUST_ASSET_SCHEDULE`

Corporate: `ARTICLES_OF_INCORPORATION`, `CERTIFICATE_OF_INCORPORATION`, `CORPORATE_BYLAWS`,
`CORPORATE_RESOLUTION`, `BOARD_MINUTES`, `SHAREHOLDER_MINUTES`, `STOCK_CERTIFICATE`,
`STOCK_LEDGER`, `SHAREHOLDER_AGREEMENT`, `CERTIFICATE_OF_GOOD_STANDING`, `ANNUAL_REPORT`

LLC: `ARTICLES_OF_ORGANIZATION`, `OPERATING_AGREEMENT`, `CERTIFICATE_OF_FORMATION`,
`MEMBER_RESOLUTION`, `MEMBERSHIP_SCHEDULE`, `MANAGER_AUTHORIZATION`

Partnership: `PARTNERSHIP_AGREEMENT`, `CERTIFICATE_OF_LIMITED_PARTNERSHIP`, `GENERAL_PARTNER_AUTHORIZATION`,
`LIMITED_PARTNER_AGREEMENT`, `PARTNERSHIP_INTEREST_SCHEDULE`

Foundation: `FOUNDATION_CHARTER`, `FOUNDATION_BYLAWS`, `BOARD_OF_DIRECTORS_ROSTER`, `GRANT_POLICY`,
`FORM_990`, `FORM_990_PF`, `CHARITABLE_REGISTRATION`, `SOLICITATION_LICENSE`, `TAX_EXEMPT_DETERMINATION`

Registration/Tax: `TAX_IDENTIFICATION`, `BUSINESS_LICENSE`, `BUSINESS_REGISTRATION`, `EIN_CONFIRMATION`,
`DBA_CERTIFICATE`, `PROFESSIONAL_LICENSE`

Entity tax: `FORM_1065`, `FORM_1120`, `FORM_1120S`, `FORM_1041`, `FORM_K1_1065`, `FORM_K1_1120S`,
`FORM_K1_1041`, `FORM_W9`, `FORM_W8BEN_E`, `STATE_TAX_RETURN`, `PROPERTY_TAX_DOCUMENTS`

Compliance: `AML_CERTIFICATION`, `KYC_DOCUMENTATION`, `BENEFICIAL_OWNERSHIP_CERTIFICATION`,
`FATCA_CERTIFICATION`, `CRS_ENTITY_CERTIFICATION`, `OFAC_SCREENING`, `ACCREDITED_INVESTOR_VERIFICATION`,
`QUALIFIED_PURCHASER_VERIFICATION`

Financial: `AUDITED_FINANCIALS`, `BALANCE_SHEET`, `INCOME_STATEMENT`, `CASH_FLOW_STATEMENT`,
`BANK_STATEMENT`, `INVESTMENT_STATEMENT`, `BUSINESS_CREDIT_REPORT`

Other legal: `POWER_OF_ATTORNEY`, `AUTHORIZED_SIGNER_DOCUMENTATION`, `LEGAL_OPINION`,
`INCUMBENCY_CERTIFICATE`, `CORPORATE_SEAL`, `AMENDMENT`, `PROMISSORY_NOTE`, `PERSONAL_GUARANTY`,
`SUBSCRIPTION_AGREEMENT`, `INVESTMENT_POLICY_STATEMENT`, `INVESTOR_QUESTIONNAIRE`, `PPM_ACKNOWLEDGMENT`

Fallback: `OTHER`

#### AccountFinancialDocumentCreateRequestDto.documentSubType (92 values)

Account: `ACCOUNT_AGREEMENT`, `ACCOUNT_APPLICATION`, `TRANSFER_FORM`, `BENEFICIARY_DESIGNATION`,
`CUSTODIAL_STATEMENT`, `CUSTODY_AGREEMENT`, `FEE_SCHEDULE`, `BROKERAGE_STATEMENT`, `MARGIN_AGREEMENT`,
`OPTIONS_AGREEMENT`, `TRADE_CONFIRMATION`, `BANK_STATEMENT`, `VOIDED_CHECK`, `DIRECT_DEPOSIT_FORM`,
`WIRE_INSTRUCTIONS`, `ACH_AUTHORIZATION`

Tax (same extensive list as Individual)

Retirement: `IRA_ADOPTION_AGREEMENT`, `PLAN_DOCUMENT_401K`, `RMD_NOTICE`, `ROLLOVER_CERTIFICATION`

Authorizations + identity (same as Individual) — use CUSTODIAL_STATEMENT / BROKERAGE_STATEMENT /
BANK_STATEMENT / TRADE_CONFIRMATION before OTHER.

#### TangibleAssetDocumentCreateRequestDto.documentSubType (96 values)

Ownership: `TITLE`, `DEED`, `REGISTRATION`, `BILL_OF_SALE`, `PURCHASE_RECEIPT`, `CERTIFICATE_OF_OWNERSHIP`,
`TRANSFER_DOCUMENT`, `LIEN`, `LIEN_RELEASE`

Valuation: `APPRAISAL`, `VALUATION_REPORT`, `TAX_ASSESSMENT`, `COMPARABLE_ANALYSIS`,
`BROKER_PRICE_OPINION`, `FMV_DETERMINATION`

Insurance: `INSURANCE_POLICY`, `INSURANCE_CLAIM`, `COVERAGE_CERTIFICATE`, `INSURANCE_RIDER`,
`INSURANCE_DECLARATION`, `INSURANCE_BINDER`, `PROOF_OF_INSURANCE`, `INSURANCE_RENEWAL`,
`INSURANCE_CANCELLATION`

Maintenance: `SERVICE_RECORD`, `INSPECTION_REPORT`, `WARRANTY`, `EXTENDED_WARRANTY`,
`REPAIR_INVOICE`, `REPAIR_ESTIMATE`, `MAINTENANCE_LOG`, `RESTORATION_DOCUMENT`, `CONSERVATION_REPORT`

Vehicle-specific: `VEHICLE_HISTORY_REPORT`, `EMISSIONS_CERTIFICATE`, `SAFETY_INSPECTION`,
`AIRWORTHINESS_CERTIFICATE`, `AIRCRAFT_LOGS`, `MARINE_SURVEY`, `COAST_GUARD_DOCUMENTATION`

Real-property: `SURVEY`, `TITLE_INSURANCE`, `HOME_INSPECTION`, `PEST_INSPECTION`,
`ENVIRONMENTAL_ASSESSMENT`, `HOA_DOCUMENTS`, `ZONING_DOCUMENT`, `BUILDING_PERMIT`,
`CERTIFICATE_OF_OCCUPANCY`, `FLOOR_PLANS`

Collectibles: `CERTIFICATE_OF_AUTHENTICITY`, `CERTIFICATE_OF_ORIGIN`, `AUTHENTICATION_REPORT`,
`PROVENANCE_HISTORY`, `AUCTION_DOCUMENTATION`, `CONDITION_REPORT`, `CATALOGUE_RAISONNE`,
`EXHIBITION_HISTORY`, `LITERATURE_REFERENCE`, `EXPERT_OPINION`, `GRADING_CERTIFICATE`,
`ENCAPSULATION_CERTIFICATE`, `CELLAR_INVENTORY`, `STORAGE_RECORDS`, `WINE_PROVENANCE`

Photos: `PRIMARY_PHOTO`, `DETAIL_PHOTO`, `CONDITION_PHOTO`, `RESTORATION_PHOTO`, `DAMAGE_PHOTO`, `PHOTO`

Legal/tax: `LEGAL_AGREEMENT`, `POWER_OF_ATTORNEY`, `TRUST_DOCUMENT`, `LOAN_AGREEMENT`, `MORTGAGE`,
`LEASE_AGREEMENT`, `RENTAL_AGREEMENT`, `BILL_OF_LADING`, `CUSTOMS_DECLARATION`, `IMPORT_EXPORT_DOCUMENT`,
`PROPERTY_TAX`, `DEPRECIATION_SCHEDULE`, `TAX_BASIS`, `EXCHANGE_1031`, `GIFT_TAX_DOCUMENT`,
`ESTATE_TAX_DOCUMENT`, `CHARITABLE_DONATION_RECEIPT`, `ESTATE_APPRAISAL`

Other: `BENEFICIARY_DESIGNATION`, `WILL_EXCERPT`, `DONATION_INTENT`, `RECEIPT`, `CORRESPONDENCE`,
`NOTES`, `OTHER`

#### LiabilityDocumentCreateRequestDto.documentSubType (13 values — small)

`LOAN_AGREEMENT`, `PROMISSORY_NOTE`, `MORTGAGE_DEED`, `COLLATERAL_AGREEMENT`,
`LINE_OF_CREDIT_AGREEMENT`, `REFINANCE_DOCUMENTS`, `AMORTIZATION_SCHEDULE`, `PAYOFF_STATEMENT`,
`ACCOUNT_STATEMENT`, `FORM_1098`, `INSURANCE_CERTIFICATE`, `CORRESPONDENCE`, `OTHER`

#### InsurancePolicyDocumentCreateRequestDto.documentSubType (26 values)

Policy: `POLICY_DECLARATION`, `POLICY_CONTRACT`, `POLICY_AMENDMENT`, `POLICY_RENEWAL`,
`POLICY_SCHEDULE`, `APPLICATION`, `UNDERWRITING_REPORT`

Medical: `MEDICAL_EXAM`, `MEDICAL_RECORDS`

Claims: `CLAIM_FORM`, `CLAIM_CORRESPONDENCE`, `CLAIM_SETTLEMENT`

Billing: `PREMIUM_NOTICE`, `PAYMENT_RECEIPT`, `BILLING_STATEMENT`, `ANNUAL_STATEMENT`,
`ILLUSTRATION`, `IN_FORCE_LEDGER`

Beneficiary: `BENEFICIARY_DESIGNATION`, `BENEFICIARY_CHANGE`, `POWER_OF_ATTORNEY`,
`TRUST_ASSIGNMENT`, `IRREVOCABLE_ASSIGNMENT`, `OWNERSHIP_CHANGE`

Other: `CORRESPONDENCE`, `OTHER`

### Filename → documentSubType classifier (ALWAYS apply before upload)

Use this regex-based classifier; it catches the majority of documents. When a filename
matches multiple patterns, prefer the MORE SPECIFIC one:

```python
# filename_to_subtype.py
import re
def classify(filename: str, entity_type: str) -> str:
    """Return best-guess documentSubType. Never returns OTHER unless truly no match."""
    f = filename.lower()
    # Identity
    if re.search(r'\bdl\b|driver.?s? lic|driver.?s.?license|drivers.?licen', f): return 'DRIVERS_LICENSE'
    if 'passport' in f: return 'PASSPORT'
    if re.search(r'state.?id|national.?id', f): return 'STATE_ID'
    if 'birth.?certif' in f: return 'BIRTH_CERTIFICATE'
    # Tax forms (specific first)
    if re.search(r'\bw-?2\b|\bw2\b', f): return 'FORM_W2'
    if re.search(r'\bw-?9\b|\bw9\b', f): return 'FORM_W9'
    if re.search(r'w-?8ben-?e\b', f): return 'FORM_W8BEN_E' if entity_type == 'LEGAL_ENTITY' else 'FORM_W8BEN'
    if re.search(r'w-?8ben\b', f): return 'FORM_W8BEN'
    if re.search(r'k-?1.*1065|1065.*k-?1', f): return 'FORM_K1_1065'
    if re.search(r'k-?1.*1120s|1120s.*k-?1', f): return 'FORM_K1_1120S'
    if re.search(r'k-?1.*1041|1041.*k-?1', f): return 'FORM_K1_1041'
    if re.search(r'\bk-?1\b', f): return 'FORM_K1_1065'  # default partnership
    if '1099-div' in f: return 'FORM_1099_DIV'
    if '1099-int' in f: return 'FORM_1099_INT'
    if '1099-b' in f: return 'FORM_1099_B'
    if '1099-r' in f: return 'FORM_1099_R'
    if '1099-misc' in f or '1099-nec' in f: return 'FORM_1099_MISC'
    if re.search(r'\b1098\b|mortgage.?interest', f): return 'FORM_1098'
    if re.search(r'\b5498\b', f): return 'FORM_5498'
    if re.search(r'\b1040\b|personal.?tax.?return', f): return 'FORM_1040'
    if re.search(r'\b1065\b|partnership.?return', f): return 'FORM_1065'
    if re.search(r'\b1120s\b|s-?corp.?return', f): return 'FORM_1120S'
    if re.search(r'\b1120\b', f): return 'FORM_1120'
    if re.search(r'\b1041\b|trust.?return|estate.?return', f): return 'FORM_1041'
    if re.search(r'\b990-?pf\b', f): return 'FORM_990_PF'
    if re.search(r'\b990\b', f): return 'FORM_990'
    if re.search(r'\b8949\b', f): return 'FORM_8949'
    # Trust / estate
    if re.search(r'trust.?agreement|trust.?agt\b', f): return 'TRUST_AGREEMENT'
    if re.search(r'trust.?amend|amendment.?and.?restate|restatement', f): return 'TRUST_AMENDMENTS'
    if re.search(r'trust.?certif', f): return 'TRUST_CERTIFICATION'
    if re.search(r'certificate.?of.?trust', f): return 'TRUST_CERTIFICATION'
    if re.search(r'irrevocable', f) and 'trust' in f: return 'IRREVOCABLE_TRUST_DOCUMENT'
    if re.search(r'revocable', f) and 'trust' in f: return 'REVOCABLE_TRUST_DOCUMENT'
    if re.search(r'benefic.*designation|designation.*benefic', f): return 'BENEFICIARY_DESIGNATION'
    # Corporate / LLC / LP
    if re.search(r'articles.?of.?incorp', f): return 'ARTICLES_OF_INCORPORATION'
    if re.search(r'articles.?of.?organ', f): return 'ARTICLES_OF_ORGANIZATION'
    if re.search(r'operating.?agreement', f): return 'OPERATING_AGREEMENT'
    if re.search(r'partnership.?agreement', f): return 'PARTNERSHIP_AGREEMENT'
    if re.search(r'certificate.?of.?formation', f): return 'CERTIFICATE_OF_FORMATION'
    if re.search(r'certificate.?of.?incorp', f): return 'CERTIFICATE_OF_INCORPORATION'
    if re.search(r'certificate.?of.?good.?standing', f): return 'CERTIFICATE_OF_GOOD_STANDING'
    if re.search(r'bylaws', f): return 'CORPORATE_BYLAWS' if entity_type == 'LEGAL_ENTITY' else 'BYLAWS'
    if re.search(r'\bein\b.?letter|ein.?confirm', f): return 'EIN_CONFIRMATION'
    if re.search(r'business.?license', f): return 'BUSINESS_LICENSE'
    if re.search(r'business.?reg|state.?filing|sunbiz', f): return 'BUSINESS_REGISTRATION'
    # Accounts / statements
    if re.search(r'\bstatement\b', f) and ('bank' in f or 'chequing' in f or 'checking' in f or 'savings' in f):
        return 'BANK_STATEMENT'
    if re.search(r'brokerage.?statement|broker.?stmt', f): return 'BROKERAGE_STATEMENT'
    if re.search(r'cap.?acct|capital.?account.?summary', f): return 'INVESTMENT_STATEMENT'
    if re.search(r'trade.?confirm|confirmation', f) and 'account' not in f: return 'TRADE_CONFIRMATION'
    if re.search(r'account.?agreement|acct.?agreement', f): return 'ACCOUNT_AGREEMENT'
    if re.search(r'account.?application|acct.?app|new.?account', f): return 'ACCOUNT_APPLICATION'
    if re.search(r'wire.?instr|dtc.?instr', f): return 'WIRE_INSTRUCTIONS'
    if re.search(r'fee.?schedule', f): return 'FEE_SCHEDULE'
    if re.search(r'margin.?agreement', f): return 'MARGIN_AGREEMENT'
    # Tangible asset
    if re.search(r'\bdeed\b', f): return 'DEED'
    if re.search(r'\btitle\b', f) and 'insurance' not in f: return 'TITLE'
    if re.search(r'title.?insurance', f): return 'TITLE_INSURANCE'
    if re.search(r'bill.?of.?sale', f): return 'BILL_OF_SALE'
    if re.search(r'\bregistration\b.*\b(vehicle|reg)', f) or re.search(r'\breg.?application', f):
        return 'REGISTRATION'
    if re.search(r'appraisal', f): return 'APPRAISAL'
    if re.search(r'valuation|val.?report', f): return 'VALUATION_REPORT'
    if re.search(r'authentic|authenticity|coa\b', f): return 'CERTIFICATE_OF_AUTHENTICITY'
    if re.search(r'provenance', f): return 'PROVENANCE_HISTORY'
    if re.search(r'emissions', f): return 'EMISSIONS_CERTIFICATE'
    if re.search(r'warranty', f): return 'WARRANTY'
    # Insurance
    if re.search(r'policy.?decl|declaration.*polic|declarations.?page', f): return 'POLICY_DECLARATION'
    if re.search(r'policy.?contract|insurance.?contract', f): return 'POLICY_CONTRACT'
    if re.search(r'policy.?amend', f): return 'POLICY_AMENDMENT'
    if re.search(r'policy.?renewal', f): return 'POLICY_RENEWAL'
    if re.search(r'policy.?schedule|schedule.?of.?values', f): return 'POLICY_SCHEDULE'
    if re.search(r'claim.?form', f): return 'CLAIM_FORM'
    if re.search(r'premium.?notice', f): return 'PREMIUM_NOTICE'
    # Liability
    if re.search(r'loan.?agreement', f): return 'LOAN_AGREEMENT'
    if re.search(r'promissory.?note', f): return 'PROMISSORY_NOTE'
    if re.search(r'mortgage.?deed', f): return 'MORTGAGE_DEED'
    if re.search(r'payoff.?stmt|payoff.?statement', f): return 'PAYOFF_STATEMENT'
    if re.search(r'amortization', f): return 'AMORTIZATION_SCHEDULE'
    # Estate planning docs
    if re.search(r'\bwill\b|last.?will', f): return 'LAST_WILL_AND_TESTAMENT'
    if re.search(r'living.?will', f): return 'LIVING_WILL'
    if re.search(r'healthcare.?surrogate|healthcare.?directive|advance.?directive', f): return 'HEALTHCARE_SURROGATE'
    if re.search(r'power.?of.?attorney|\bpoa\b', f): return 'POWER_OF_ATTORNEY'
    if re.search(r'marriage.?certif', f): return 'MARRIAGE_CERTIFICATE'
    if re.search(r'divorce', f): return 'DIVORCE_DECREE'
    if re.search(r'court.?order', f): return 'COURT_ORDER'
    # Compliance
    if re.search(r'\bkyc\b', f): return 'KYC_DOCUMENTATION'
    if re.search(r'\baml\b', f): return 'AML_CERTIFICATION' if entity_type == 'LEGAL_ENTITY' else 'AML_QUESTIONNAIRE'
    if re.search(r'fatca', f): return 'FATCA_CERTIFICATION'
    if re.search(r'\bcrs\b', f): return 'CRS_ENTITY_CERTIFICATION' if entity_type == 'LEGAL_ENTITY' else 'CRS_SELF_CERTIFICATION'
    if re.search(r'ofac', f): return 'OFAC_SCREENING'
    if re.search(r'accredited', f): return 'ACCREDITED_INVESTOR_VERIFICATION'
    # Financial
    if re.search(r'balance.?sheet', f): return 'BALANCE_SHEET'
    if re.search(r'income.?statement', f): return 'INCOME_STATEMENT'
    if re.search(r'cash.?flow', f): return 'CASH_FLOW_STATEMENT'
    if re.search(r'audited.?financ', f): return 'AUDITED_FINANCIALS'
    if re.search(r'financial.?stat', f): return 'FINANCIAL_STATEMENT'
    if re.search(r'net.?worth', f): return 'NET_WORTH_STATEMENT'
    if re.search(r'credit.?report', f): return 'CREDIT_REPORT'
    # Investment / subscription
    if re.search(r'subscription', f): return 'SUBSCRIPTION_AGREEMENT'
    if re.search(r'ppm|offering.?memorand', f): return 'PPM_ACKNOWLEDGMENT'
    if re.search(r'ips\b|investment.?policy', f): return 'INVESTMENT_POLICY_STATEMENT'
    if re.search(r'investor.?question', f): return 'INVESTOR_QUESTIONNAIRE'
    # Correspondence
    if re.search(r'email|correspondence|letter\b|meeting.?notes', f): return 'CORRESPONDENCE'
    # Receipt
    if re.search(r'receipt|invoice', f): return 'RECEIPT' if entity_type == 'TANGIBLE_ASSET' else 'CORRESPONDENCE'
    # Unmatched → record + return OTHER
    return 'OTHER'
```

**When `OTHER` is returned**, append the (filename, entityType) pair to
`altitude_review/documentSubType_unmatched.json` for follow-up improvements. The goal
is to drive this list to zero over time.

### Document Association Rules

Read `references/document_entity_association.md` for the complete mapping. Key rules:

**Associate with Individual:**
- Driver's licenses, passports → `documentSubType: DRIVERS_LICENSE / PASSPORT`
- Personal ID docs → `PERSONAL_ID`
- W-2s → `FORM_W2`
- Personal tax returns → `FORM_1040`
- Power of Attorney → `POWER_OF_ATTORNEY`
- Will / Testament → `WILL`
- Healthcare directives → `HEALTHCARE_DIRECTIVE`

**Associate with Legal Entity:**
- Articles of Organization → `ARTICLES_OF_ORGANIZATION`
- Operating Agreement → `OPERATING_AGREEMENT`
- Articles of Incorporation → `ARTICLES_OF_INCORPORATION`
- Trust Agreement → `TRUST_AGREEMENT`
- EIN Letter → `EIN_CONFIRMATION`
- State filings (Sunbiz) → `BUSINESS_REGISTRATION`
- K-1s → `FORM_K1_1065` or `FORM_K1_1120S`
- Entity tax returns → `FORM_1065 / FORM_1120 / FORM_1120S / FORM_1041`

**Associate with Account (AccountFinancial):**
- Bank statements → `ACCOUNT_STATEMENT`
- Brokerage statements → `ACCOUNT_STATEMENT`
- Account confirmations → `ACCOUNT_CONFIRMATION`
- IRA/401k statements → `RETIREMENT_ACCOUNT_STATEMENT`

**Associate with Tangible Asset:**
- Property deeds → `DEED`
- Property titles → `TITLE`
- Insurance policies → `INSURANCE_POLICY`
- Appraisals → `APPRAISAL`
- Property tax bills → `PROPERTY_TAX`

### Upload format (multipart/form-data)

```
POST /api/v1/individual/{individualId}/document?sessionId={uuid}&skipDuplicates=true
X-API-Key: {api_key}
Content-Type: multipart/form-data

Parts:
- createRequest (application/json, required):
  {
    "title": "Brett Podolsky - Driver's License",
    "description": "Florida driver's license, expires 2029",
    "documentSubType": "DRIVERS_LICENSE",
    "contentType": "PNG"
  }

- file (binary, required):
  [actual file bytes]
```

Entity-specific upload endpoints:
- `POST /api/v1/individual/{individualId}/document`
- `POST /api/v1/legal-entity/{legalEntityId}/document`
- `POST /api/v1/account-financial/{accountId}/document`
- `POST /api/v1/tangible-asset/{assetId}/document`
- `POST /api/v1/insurance-policy/{policyId}/document`
- `POST /api/v1/liability/{liabilityId}/document`

**Note**: Household does NOT support document upload. Associate household-level documents with
the primary individual or legal entity instead.

Use the same `sessionId` (UUID) for all uploads in a batch so they are grouped together.
Set `skipDuplicates=true` to prevent re-uploading the same file.

For large households with 50+ documents, process in batches of 10-15 uploads at a time
to avoid timeouts.

### Create Entity Associations (REQUIRED after each upload)

The upload endpoint sets the type-specific FK (`individualId`, `legalEntityId`, etc.) but does
**NOT** auto-create entity associations. The UI uses the `entityAssociations` array to display
document-entity links. Without this step, documents will appear unlinked in the UI.

After each successful document upload, immediately call:

```
POST /api/v1/document/{documentId}/associations?entityType={TYPE}&entityId={ID}&associationType=OWNER&entityDisplayName={NAME}
X-API-Key: {api_key}
```

**Parameters:**
- `documentId` — the `id` returned from the upload response
- `entityType` — matches the entity: `INDIVIDUAL`, `LEGAL_ENTITY`, `ACCOUNT`, `INSURANCE_POLICY`, `TANGIBLE_ASSET`, `LIABILITY`
- `entityId` — UUID of the parent entity
- `associationType` — `OWNER` (the entity that owns this document)
- `entityDisplayName` — human-readable name (e.g., "Brett Podolsky", "Hercules Lender LLC")

**Example (shell-agnostic — pseudo-variables in braces, not `${…}` or `%…%`):**
```
# Upload returns {"id": "abc123", ...}
# Then call the association endpoint:
POST {baseUrl}/api/v1/document/abc123/associations
     ?entityType=INDIVIDUAL
     &entityId={brettId}
     &associationType=OWNER
     &entityDisplayName=Brett%20Podolsky
Headers:
  X-API-Key: {apiKey}
  X-Firm-Id: {firmId}
```

Prefer Python `requests` or `urllib` over shell `curl` — it avoids all cross-shell quoting
issues (bash `${VAR}`, cmd `%VAR%`, PowerShell `$env:VAR`, `--data-binary` quirks) and
works identically on macOS/Linux/Windows:

```python
# post_association.py
import os, sys, requests
base, api_key, firm_id, doc_id, entity_type, entity_id, name = sys.argv[1:8]
r = requests.post(
    f"{base}/api/v1/document/{doc_id}/associations",
    params={"entityType": entity_type, "entityId": entity_id,
            "associationType": "OWNER", "entityDisplayName": name},
    headers={"X-API-Key": api_key, "X-Firm-Id": firm_id},
    timeout=30,
)
r.raise_for_status()
print(r.json())
```

This is idempotent — calling it twice for the same document+entity+type returns the existing
association. Do this for EVERY uploaded document, not just cross-entity ones.

For documents that relate to multiple entities (e.g., a trust agreement that names trustees
and beneficiaries), create additional associations with `associationType=SUBJECT`:
```
POST /api/v1/document/{trustAgreementDocId}/associations?entityType=INDIVIDUAL&entityId={trusteeId}&associationType=SUBJECT&entityDisplayName={trusteeName}
```

---

## Important Rules

1. **NEVER create entities without checking Altitude first.** Always query the household
   universe before extraction.

2. **NEVER push without user approval.** Always generate the review package first.

3. **Auto-fill is safe.** If a field is empty/null in Altitude and you have a value from
   documents, queue it for automatic update.

4. **Conflicts require human decision.** If a field has different values in Altitude vs
   documents, present both values and ask.

5. **PATCH, don't PUT.** Use PATCH for updates so you only touch the fields being changed.

6. **Validate relationship source/target types before creating.** Not all entity type
   combinations are allowed. Consult the matrix in Phase 4.5. The API will reject
   invalid combinations with a 400 error.

7. **Never include READ_ONLY fields in PATCH payloads.** Computed fields like
   `totalMarketValue`, `fullName`, `createdAt`, `updatedAt`, `id` will cause validation
   errors. Only send fields that are actually writable.

8. **Track provenance.** Every field should trace back to a source document.

9. **Handle sensitive data carefully.** SSNs, EINs, tax IDs should only appear in
   structured payloads, not logs or markdown.

10. **Auth: OAuth for humans, API key for automation.** The skill supports three auth modes
    (see Step 0). For interactive use by a human advisor, prefer OAuth — Altitude hosts its
    own login page, we never see the password, and refresh tokens give a smooth long session.
    For CI, scripts, or unattended automation, API keys are simpler (no browser, no refresh).
    Direct JWT paste is a fallback when neither option is available. The skill's helper
    (`altitude_auth.headers()`) emits the correct `Authorization: Bearer` or `X-API-Key`
    header based on `config.authMode` — examples in this skill show `X-API-Key` for brevity
    but the helper substitutes correctly.

11. **Save checkpoints after each phase.** Write intermediate results to disk
    (`altitude_review/` folder) after Phase 1 (universe), Phase 4 (matches), and
    Phase 5 (review). This allows resuming if context resets.

12. **Process one household at a time** unless batch processing is explicitly requested.
    If processing multiple households in the same session, be extremely careful not to
    cross-contaminate data between families. Every field must trace to a source document
    in THAT household's folder. Never apply data from one family's documents to another.

13. **Handle large households gracefully.** For households with 50+ documents or 20+ entities,
    use parallel processing for document extraction (Phase 3), then merge sequentially
    (Phase 4). Process uploads in batches to avoid timeouts.

14. **Read EVERY file.** The most common extraction failure is not reading a document at all.
    No file should be skipped. If a file can't be read (password-protected, corrupt, binary),
    flag it for the user — don't silently skip it.

15. **Every named person is an entity.** Estate planning documents name guardians, executors,
    successor trustees, beneficiaries, agents. LLC docs name attorneys. Tax returns name
    preparers. 1099s name advisors. Insurance summaries name agents. If a person has a name
    in a document, they become either an Individual or a Contact in Altitude.

16. **Each spouse gets their own trust.** When estate planning docs say "your respective Trusts"
    or "each of you are the Grantor and initial Trustee of your own Trust," that is TWO separate
    LegalEntity (TRUST) records — not one shared trust. This is the most common entity miss.

17. **1099s are account discovery tools.** Every 1099 cover page has an account number and a
    custodian name. Many 1099s also name the investment advisor/RIA. These are often the ONLY
    place where an account number appears. Never dismiss a 1099 as "just tax data."

18. **Emails and cover letters contain contacts.** An email forwarding LLC documents often has
    the attorney's full name, firm, phone, and email in the signature block. A tax return cover
    letter has the CPA firm's contact info. These are Tier 1 data for Contact entity creation.

19. **Sensitive data handling.** If the onboarding sheet or any document contains plaintext
    passwords, credit card numbers, or bank login credentials: (a) Do NOT store these in any
    Altitude field, (b) Flag to the user that credentials were found in plain text and recommend
    the client change all affected passwords immediately.

20. **TangibleAsset uses subtype-specific POST endpoints.** You CANNOT POST to `/api/v1/tangible-asset`
    directly — it returns 500 (abstract entity). Use the subtype endpoints:
    - `/api/v1/tangible-asset/vehicle` — for cars, boats, aircraft
    - `/api/v1/tangible-asset/real-property` — for homes, condos, land
    - `/api/v1/tangible-asset/luxury` — for watches, jewelry, handbags
    - `/api/v1/tangible-asset/collectible` — for art, wine, antiques
    - `/api/v1/tangible-asset/other` — for everything else

21. **Do NOT delete and recreate entity relationships.** Soft-deleted relationships still enforce
    uniqueness constraints. If you delete a relationship and try to recreate it with the same
    source+target+type, you will get a 409 Conflict. Either avoid deleting relationships, or
    use the hard-delete endpoint (`DELETE /{id}/hard`) for error correction.

22. **Identity documents use `OTHER` subtype.** `DRIVERS_LICENSE` and `PASSPORT` subtypes are
    for IdentificationDocument entities, NOT IndividualDocument. When uploading DLs or passports
    via `/api/v1/individual/{id}/document`, use `documentSubType: "OTHER"` with a descriptive
    title like "Brett Podolsky - Florida Driver's License".

21. **Cache JWT tokens.** Get ONE token at the start of Phase 6 and reuse it for all API calls.
    Do NOT authenticate before every request — the server has a rate limiter (~20 login attempts
    per 15 minutes per IP). If you hit rate limiting, restart the server to clear the in-memory
    cache, then get a single token and reuse it.

22. **Household → Individual uses OWNERSHIP at 100%, not MEMBER.** The relationship from a
    household to its individual members uses `relationshipType: "OWNERSHIP"` with the household
    as SOURCE and the individual as TARGET. **ALL members get percentage = 100** — the household
    owns 100% of each person, which drives valuation rollup. Do NOT use 50/50 for couples or
    0 for children. Do NOT use MEMBER (IND→HH) — that is for LLC membership only. Use
    generational roles (G1/G2/G3) in the `role` field for display, `isPrimary: true` on the
    first G1 member only.

23. **Create ALL insurance policies — no deprioritization.** Every policy in the insurance
    summary must be created, regardless of size. A $462/yr golf cart policy and a $605/yr
    cyber policy are just as important as a $10M umbrella. The skill extracts them — create them.

24. **Create ALL tangible assets from insurance schedules.** Jewelry, watches, and collectibles
    itemized on a Chubb Collections or similar schedule are individual TangibleAssets. Create
    each one via `/luxury` or `/collectible` with its scheduled value and serial number.

25. **JPEG and JPG are both valid.** When uploading images, use `contentType: "JPG"` for both
    `.jpg` and `.jpeg` files. For filenames with special characters (parentheses, commas,
    apostrophes), escape them in curl commands or use `--data-binary` with proper quoting.

26. **Investment accounts without statements.** If the onboarding sheet mentions investments
    (Loci Capital $750K, Stonetown $250K, etc.) but no account statements exist in the folder,
    still flag these in the Open Questions section. Do NOT create AccountFinancial entities
    without at minimum an account number or custodian — but DO list them as "accounts to be
    created once client provides statements."

27. **Professional relationships flow OUTWARD from the client entity.** For ADVISOR, ATTORNEY,
    ACCOUNTANT, and INSURANCE_AGENT: the client entity (Household, Individual, or LegalEntity) is
    the SOURCE, and the Contact is the TARGET. Example: `Hercules LLC → Jason Evans (ATTORNEY)`,
    NOT `Jason Evans → Hercules LLC`. The API accepts both directions, but outgoing from the
    entity is the correct data model pattern used by the demo data and the UI.

28. **Always cross-link insurance policies to tangible assets.** After creating both the
    insurance policy and the tangible asset: (a) PATCH the tangible asset with `isInsured: true`,
    `primaryInsurancePolicyNumber`, `insuredValue`, and `insuranceExpirationDate` for the summary
    fields displayed on asset cards. (b) POST to `/api/v1/tangible-asset/{id}/insurance` to create
    `TangibleAssetInsurance` child entries for the detailed "Insurance Policies" tab. Both steps
    are required — the PATCH sets summary fields, the POST populates the detail collection.
    **CRITICAL**: The POST requires `effectiveDate`, `expirationDate`, and `coverageAmount`
    (all NOT NULL in the database) — omitting them returns 409, not 400.

29. **Always cross-link liabilities to tangible assets.** After creating both the liability and
    the tangible asset it's secured by, PATCH the liability with `linkedTangibleAssetId` set to
    the tangible asset UUID. This enables the unified liability rollup to correctly attribute
    asset-secured debt and display it on the tangible asset detail view. Mortgages link to
    properties, auto loans link to vehicles, boat loans link to boats.

30. **Create vehicles from auto insurance schedules.** Auto insurance policies list specific
    vehicles (make, model, year, VIN). Each vehicle MUST be created as a TangibleAsset via
    `/api/v1/tangible-asset/vehicle` even if no separate vehicle document exists in the folder.
    The insurance schedule IS the source document. After creation, PATCH each vehicle with
    `isInsured: true` and the auto policy number, and create OWNERSHIP relationships.

31. **Entity creation order matters for cross-linking.** Always create entities in this order:
    Household → Individuals → Legal Entities → Accounts → **Tangible Assets** → **Insurance
    Policies** → **Liabilities** → Relationships → Estate Planning → Cross-Links (insurance↔asset,
    liability↔asset). Tangible assets must exist before liabilities and insurance can link to them.

32. **ALWAYS create entity associations after uploading documents.** The upload endpoint sets
    the type-specific FK (`individualId`, `legalEntityId`, etc.) but does NOT create an entity
    association. The UI uses `entityAssociations` to display document-entity links — without
    this step, documents appear unlinked in the UI. After every successful upload, call
    `POST /api/v1/document/{docId}/associations?entityType={TYPE}&entityId={ID}&associationType=OWNER&entityDisplayName={NAME}`.
    This is idempotent and REQUIRED for every document. See Phase 7 for full details.

33. **ALWAYS populate LLC detail fields.** For every LLC/LP/partnership legal entity, extract and
    PATCH these fields — they are commonly missed:
    - `registrationNumber` — state filing document number (from Articles of Organization or Sunbiz)
    - `taxClassification` — `PARTNERSHIP` for multi-member LLCs, `DISREGARDED_ENTITY` for single-member
    - `llcOperatingAgreementDate` — execution date of the operating agreement
    - `addressPrincipal` — principal place of business (usually the primary residence address)
    These fields appear in the Articles of Organization, Sunbiz filings, and Operating Agreements.

34. **ALWAYS set gender on ALL individuals.** Gender for children is often omitted because it's
    not on IDs or tax returns. Infer from first names if not explicitly stated. Do NOT leave
    gender null — it's a core demographic field.

35. **ALWAYS create successor trustee relationships.** Trust agreements name successor trustees
    (typically spouse as 1st, then parents/in-laws as 2nd/3rd). Create `SUCCESSOR_TRUSTEE`
    relationships with `priority` (1, 2, 3) and `role` ("1st Successor Trustee", etc.).
    This is a separate relationship type from `TRUSTEE` — both should exist.

36. **ALWAYS create beneficiary relationships for children to trusts.** When trust documents name
    children as primary beneficiaries, create `BENEFICIARY` relationships from each child to each
    trust with `role: "Primary Beneficiary"`. Don't assume the grantor/trustee relationships cover
    beneficiary status.

37. **Create family member contacts.** Extended family members named as guardians, successor
    trustees, POA agents, or beneficiaries in estate planning docs should be created as `Contact`
    entities (not full Individuals unless they become clients). Include phone, address, and a
    `biography` noting their relationship ("Brett's father. Named as successor trustee and
    guardian."). Create `ADVISOR` relationship from Household → Contact with role "Family Member".

38. **WINDSTORM is a valid InsurancePolicyCategory.** Use `WINDSTORM` (not `OTHER` or `HOMEOWNERS`)
    for wind/hurricane policies that are separate from base homeowners coverage. This is common
    in Florida and coastal areas where wind is carved out of the homeowners policy.

39. **Files with special characters in filenames break curl.** Filenames containing commas,
    parentheses with periods (e.g., `(Podolsky, B.).pdf`), or dollar signs cause curl error 26.
    Copy these files to the system temp directory (use Python `tempfile.gettempdir()`) with
    clean names before uploading, then delete the temp copies after upload completes.

40. **Latest-date-wins for field merging.** When the same entity field appears in multiple
    documents (or in Altitude vs documents) with different values, the value from the most
    recent source wins — determined by the document's `asOfDate` (explicit "as of" date,
    execution/signing date, statement period end, filing date, filename-embedded date, or
    file mtime as last resort). See Phase 3.5 Step 0 for the full rule. Exceptions:
    immutable fields (SSN, DOB, EIN, formationDate, taxId) must agree and are flagged as
    hard conflicts on disagreement; historical fields (originalBalance, purchasePrice) keep
    their first confirmed value. For trust restatements, LLC amendments, and policy
    endorsements, the amending document supersedes the original for all mutable fields.

41. **Role replacements retire the old relationship.** When an amendment, restatement, or
    new engagement names a DIFFERENT person in a role previously held by someone else
    (trustee, managing member, advisor, attorney, accountant, officer, named insured): PATCH
    `effectiveTo` on the old relationship to the replacement date, then POST a new
    relationship with `effectiveFrom` = replacement date. Never delete — the historical
    record must survive, and soft-deletes still enforce uniqueness (see rule #21). See
    Phase 4.7 for the full workflow and review table format. If the document is ambiguous
    (e.g., could be an additional co-trustee rather than a replacement), leave the old
    relationship intact and flag in Open Questions.

43. **Approval Q&A trail goes at the root of the household folder, not inside `altitude_review/`.**
    Create `altitude_questions_{YYYY-MM-DD}.md` at `{household_folder}/` (sibling to the
    source subfolders like `Onboarding/`, `Trust & Estate/`, etc., and sibling to
    `altitude_review/`). Populate at Phase 5 with every pre-approval question + severity +
    category. Update in place when the user responds (fill User Response, Resolved, Resolution
    fields). Append new questions under "Post-Approval Questions" as they arise during
    Phase 6/7. Never overwrite prior sessions — the date in the filename gives each session
    its own audit trail. As the final step of Phase 7, upload the Q&A file to the primary
    individual with entity associations to both the Individual and the Household, so the
    decision trail lives inside Altitude too. See Phase 5 → "Approval Q&A Trail" for the
    full template.

42. **Externally-synced accounts (Addepar, Orion, custodian) are READ-ONLY from documents.**
    When an AccountFinancial has an `externalIds[]` entry with a provider or a
    `providerDetails.sourceSystemName` set, the external sync is the source of truth for
    account fields (`accountNumber`, `name`, `custodianId`, `totalMarketValue`,
    `totalCostBasis`, holdings, positions, valuations, etc.). Do NOT PATCH these from
    documents — the next sync will either overwrite the change or produce conflicts. DO
    update non-synced metadata (description, tags, manual notes, ownershipType). When a
    document contains a materially different value for a synced field, include it in the
    "Addepar / External Sync Discrepancies" section of the review (Phase 4.8) so the user
    can investigate the sync rather than overriding it by hand. If a synced account has
    `totalMarketValue == 0` or `lastSyncedAt == null`, raise a blocking alert in the
    review — the sync is probably broken.

---

## Running the Skill

When the user invokes this skill:

1. **Collect prerequisites**: API URL (production or development), authentication (API key or JWT),
   firmId (ask if not known)

2. **Identify the target household** folder (or process all if requested)

3. **Run Phase 1 + Phase 2 in parallel**: Launch two concurrent tasks:
   - **Task A**: Query Altitude for existing data → save `altitude_universe.json`
   - **Task B**: Scan and classify all files in the folder → save `file_tracker.md`
   These are independent — Altitude queries don't depend on file scanning.

4. **Run Phase 3 — Parallel Extraction**: After Phase 2 completes, group files into batches
   (by subdirectory, max ~12 files per batch). Spawn one extraction Agent per batch, all in
   a **single message** so they run concurrently. Each agent:
   - Reads every file in its batch
   - Extracts entities, relationships, contacts using document-type checklists
   - Writes results to `altitude_review/extraction_cache_batch_{N}.jsonl`
   - Writes tracker to `altitude_review/file_tracker_batch_{N}.md`

5. **Run Phase 3M — Merge**: After ALL extraction agents complete:
   - Concatenate all `extraction_cache_batch_*.jsonl` into `extraction_cache.jsonl`
   - Merge all `file_tracker_batch_*.md` into `file_tracker.md`
   - Verify 100% file coverage (every file marked READ)

6. **Run Phases 3.5 → 4**: Read the merged `extraction_cache.jsonl`. Run cross-document
   validation, self-audit, then match and merge against Altitude Universe.

7. **Run Phase 5**: Generate review package and present to user. Save payloads and
   conflicts to `altitude_review/` folder.

8. **Wait for approval** and conflict resolution

9. **Run Phases 6-7**: Push updates (PATCH), create new entities (POST), create relationships,
   upload documents. Track progress and report any failures.

### Extraction Agent Prompt Template

When spawning each extraction agent, use this prompt structure:

```
You are a document extraction agent for the {household_name} household onboarding.

Your task: Read EVERY file in your assigned batch and extract ALL entity data.

## Your Files (Batch {N})
{numbered list of absolute file paths}

## Output
Write extracted data to: {folder}/altitude_review/extraction_cache_batch_{N}.jsonl
Write file tracker to: {folder}/altitude_review/file_tracker_batch_{N}.md

## How to Read Files
- PDFs: Use Read tool. For 20+ page PDFs, use page index scan first (pypdf), then
  targeted deep read of data-rich pages.
- Word docs (cross-platform fallback chain):
  1. `textutil -convert txt file.docx` (macOS only)
  2. `pandoc file.docx -t plain` (cross-platform)
  3. Write `docx_read.py` (see SKILL.md → Standard Document Extraction) and run `python docx_read.py "file.docx"` (Python fallback)
- Images: Read tool (Claude has vision)
- Emails: Write `eml_read.py` (see SKILL.md → Standard Document Extraction) and run it
- Spreadsheets: Write `xlsx_read.py` (see SKILL.md → Standard Document Extraction) and run it
- **NEVER use `python -c "..."` with embedded newlines or nested quotes** — it breaks on
  Windows cmd and PowerShell. Always write scripts to a `.py` file first.
- Use `{PYTHON}` from Cross-Platform Setup (`python` on Windows, `python3` elsewhere). Detect with `platform.system()`.

## What to Extract (per file)
For EACH file, append one JSONL line to your cache with:
- file: relative path
- entities.individuals: [{name, dob, ssn, gender, address, email, phone, occupation, employer}]
- entities.legalEntities: [{name, type, ein, formationDate, jurisdiction, state, managementType}]
- entities.accounts: [{name, accountNumber, custodian, accountCategory, subCategory}]
- entities.tangibleAssets: [{name, category, assetType, address, value, serialOrIdentifier}]
- entities.insurancePolicies: [{name, policyCategory, policyNumber, carrier, coverage, premium}]
- entities.liabilities: [{name, type, lender, accountNumber, balance, rate, monthlyPayment}]
- relationships: [{source, target, type, percentage, role}]
- contacts: [{name, jobTitle, firm, email, phone, role}]
- estatePlanning: [{individual, field, value}]
- notes: free text with anything notable

## Document Type Checklists
{Read references/document_type_patterns.md and include the relevant checklists}

## Rules
- Read EVERY file. No skipping.
- Extract ALL named people — they become Individuals or Contacts.
- Track every field's source document.
- For large PDFs (tax returns), use the two-pass strategy:
  Pass 1: pypdf page index scan. Pass 2: Read only data-rich pages.
- Password-protected PDFs: check filename for password, decrypt with qpdf.
- Update file_tracker_batch_{N}.md after each file (status: READ, summary of what was found).
```

---

## Reference Files

- `references/altitude_api_schema.md` — Complete Altitude API field mappings and endpoints
- `references/altitude_api_endpoints.md` — Detailed search, PATCH, document upload, and relationship endpoints
- `references/document_type_patterns.md` — How to classify documents by filename and content
- `references/document_entity_association.md` — Which documents associate with which entity type + documentSubType values
- `references/match_merge_rules.md` — Detailed entity matching and field merge logic
