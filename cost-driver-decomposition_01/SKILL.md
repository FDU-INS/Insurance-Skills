---
name: upload-case
description: Use when uploading PDF documents as new cases to Stream Claims, when user says "upload", "create a case", "submit this PDF", or references files to upload to the platform
---

# Upload Case

Upload one or more PDFs as a new case to Stream Claims.

## Parameters

Gather these from the user before starting. Ask for anything missing.

| Parameter | Required | Default | Notes |
|-----------|----------|---------|-------|
| PDF path(s) | Yes | - | Absolute path(s) on local filesystem or S3 URI |
| Case ID | Yes | - | Identifier for the new case |
| LOB | No | WC | `WC` (Workers' Comp) or `BI` (Bodily Injury) |
| First Name | No | "John" | Auto-extracted from real PDFs when using browser flow |
| Last Name | No | "Doe" | Auto-extracted from real PDFs when using browser flow |
| Environment | No | eilamdev | URL prefix: `{env}.dev.stream.claims` |
| AWS Profile | No | default | AWS CLI profile for S3 operations |

## Approach Selection

Two approaches exist. Choose based on file size and source:

| Scenario | Approach |
|----------|----------|
| **PDF on local disk or S3 (any size)** | **Hybrid API** (recommended) |
| **Small PDF (<500KB) on local disk, need AI extraction** | Browser automation (fallback) |

The **hybrid API approach** is strongly recommended. It bypasses browser limitations with large files and Tailscale routing issues that block cross-origin requests.

## Prerequisites: Browser Authentication

This skill requires **chrome-in-chrome** (the Claude browser extension) for authenticated API calls. Before starting:

1. Load the extension: `ToolSearch: select:mcp__claude-in-chrome__tabs_context_mcp`
2. Call `tabs_context_mcp(createIfEmpty: true)`

**If chrome-in-chrome returns "Browser extension is not connected":**
- **STOP. Do NOT attempt workarounds** (no Cognito admin auth, no password changes, no modifying auth flows).
- **Flag to the user:** "Chrome-in-chrome extension isn't connected. Please make sure the Claude browser extension is running in Chrome and you're logged into claude.ai, then try again."
- The S3 download/upload steps can proceed independently, but the API calls (presigned URL + case creation) require the authenticated browser session.

**Do NOT use chrome-devtools as a fallback** — it opens a separate browser without the user's session cookies.

---

## Approach 1: Hybrid API (Recommended)

Uses browser JS for authenticated same-origin API calls + AWS CLI for S3 upload. This works reliably for files of any size.

### 1. Determine the S3 bucket for the target environment

The masterbucket follows the naming convention: `{stackname}-masterbucket{suffix}-{hash}` (the suffix varies per environment)

```bash
# For eilamdev (default profile):
aws s3 ls --profile default | grep masterbucket
# Example: eilamdevstack-masterbucket7c03eada-chzxxwprmgbe

# For other environments, use the appropriate profile
```

### 2. Get PDF page count

```bash
# If the file is local:
python3 -c "
import subprocess
result = subprocess.run(['mdls', '-name', 'kMDItemNumberOfPages', '/path/to/file.pdf'], capture_output=True, text=True)
print(result.stdout)
"

# Or with PyPDF2/pikepdf if available:
python3 -c "
from pypdf import PdfReader
r = PdfReader('/path/to/file.pdf')
print(len(r.pages))
"

# If the file is on S3, download it first to /tmp
```

### 3. Get browser context

**IMPORTANT:** You MUST load chrome tools via ToolSearch before using them.

```
ToolSearch: select:mcp__claude-in-chrome__tabs_context_mcp
tabs_context_mcp(createIfEmpty: true)
ToolSearch: select:mcp__claude-in-chrome__tabs_create_mcp
tabs_create_mcp()  // always create a fresh tab
```

Navigate via JavaScript (regular navigate fails for internal domains):
```
ToolSearch: select:mcp__claude-in-chrome__javascript_tool
javascript_tool(action: "javascript_exec", tabId: TAB_ID,
  text: "window.location.href = 'https://{env}.dev.stream.claims'")
```

Wait 5s for page load, then screenshot to confirm the Cases dashboard loaded.

### 4. Get presigned S3 URL via browser JS

The browser has an authenticated session (via chrome-in-chrome). Use it to call the same-origin API:

```javascript
const caseId = 'YOUR_CASE_ID';
const fileName = 'your-file.pdf';

const response = await fetch(`/case/${encodeURIComponent(caseId)}/presigned_url_case`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ file_names: [fileName] })
});
const data = await response.json();
// Returns: { presignedUrls: [{ fileName, url, fields: { key, ... } }] }
JSON.stringify(data);
```

Extract the `fields.key` value from the first entry — this is the S3 key where the file should be uploaded.

### 5. Upload file to S3 via AWS CLI

Use the S3 key from step 4 to upload directly to the environment's masterbucket:

```bash
# From local file:
aws s3 cp /path/to/file.pdf "s3://MASTERBUCKET/upload/CASE_ID/FILENAME.pdf" --profile PROFILE

# From another S3 bucket (cross-account copy):
aws s3 cp "s3://SOURCE_BUCKET/path/to/file.pdf" /tmp/temp-file.pdf --profile source_profile
aws s3 cp /tmp/temp-file.pdf "s3://DEST_BUCKET/upload/CASE_ID/FILENAME.pdf" --profile dest_profile
```

### 6. Create case via browser JS

```javascript
const response = await fetch('/case', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    caseId: 'YOUR_CASE_ID',
    fileMetadata: [{
      fileName: 'your-file.pdf',
      pageCount: PAGE_COUNT
    }],
    specialties: [{ specialty: 'general' }],
    patientInfo: {
      name: {
        firstName: 'John',   // or user-provided
        lastName: 'Doe',     // or user-provided
        middleName: ''
      },
      dateOfBirth: ''
    },
    lineOfBusiness: 'WC',   // or 'BI'
    uploadedBy: ''           // overridden server-side with session email
  })
});
const result = await response.json();
JSON.stringify({ status: response.status, body: result });
```

### 7. Verify

Refresh the page and screenshot to confirm the case appears in the list:
```javascript
window.location.reload();
```

---

## Approach 2: Browser Automation (Small Files Only)

For small PDFs (<500KB) where you want the UI's AI extraction for patient info.

**WARNING:** This approach fails for large files. The dev environment's Tailscale exit node blocks ALL cross-origin requests from the browser, so base64-in-JS is the only file transfer method, and it's limited by tool output size.

### 1. Get browser context and navigate

Same as Hybrid steps 3 above.

### 2. Open upload modal

Click the **"Upload"** button in the left sidebar (~coordinates `[75, 619]`).
Wait 2s, screenshot to confirm "Upload Document" modal appeared.

### 3. Attach files via DataTransfer API

The file input is `#smart-dropzone` (type="file"). Never click it directly — it triggers a native file picker.

```bash
# First, base64-encode the file (must be small enough for tool output)
base64 -i /path/to/file.pdf | tr -d '\n'
```

Then in browser JS:
```javascript
const b64 = 'BASE64_STRING_HERE';
const binary = atob(b64);
const bytes = new Uint8Array(binary.length);
for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);
const blob = new Blob([bytes], { type: 'application/pdf' });
const file = new File([blob], 'filename.pdf', { type: 'application/pdf' });
const dt = new DataTransfer();
dt.items.add(file);
document.getElementById('smart-dropzone').files = dt.files;
document.getElementById('smart-dropzone').dispatchEvent(new Event('change', { bubbles: true }));
```

Screenshot to confirm "Selected Files" section shows the file(s).

### 4. Click Upload button

Click the **"Upload"** button (purple, bottom-right of modal ~`[1303, 642]`). Wait 3s.
Screenshot to confirm the Patient Information form appeared.

### 5. Fill the form

Use `read_page` with `filter: "interactive"` on the dialog to get current refs.

Form fields:
- **First Name** (textbox) - required, may auto-populate from AI extraction
- **Middle Name** (textbox) - optional
- **Last Name** (textbox) - required, may auto-populate
- **Date of Birth** (date input) - optional
- **Line of Business** (combobox) - required, options: "WC", "BI"
- **Additional Emails** (email input) - optional
- **Case ID** (textbox, placeholder "Enter new case ID") - required

Check if fields are already filled (green "AI Extracted" badge) before overwriting.

Defaults when empty: First Name = "John", Last Name = "Doe", LOB = "WC".

### 6. Submit

Click **"Add New Case"** button (purple, bottom-right). Wait for response.
Screenshot to confirm success.

---

## Copying Cases Between Environments

To copy a case from one environment (e.g., production) to another (e.g., eilamdev):

```bash
# 1. Find the source bucket
aws s3 ls --profile production | grep masterbucket

# 2. Find the merged PDF
aws s3 ls "s3://SOURCE_BUCKET/merged/CASE_ID/" --profile production

# 3. Download to /tmp
aws s3 cp "s3://SOURCE_BUCKET/merged/CASE_ID/merged.pdf" /tmp/CASE_ID-merged.pdf --profile production

# 4. Get page count
python3 -c "from pypdf import PdfReader; print(len(PdfReader('/tmp/CASE_ID-merged.pdf').pages))"

# 5. Then follow Hybrid API steps 3-7 above, but add skipAutoSegmentation: true
#    to the case creation body (step 6) to prevent auto-segmentation from
#    creating duplicate segments over the copied data.
```

## Multiple Files

For the hybrid approach, repeat steps 4-5 for each file, adding all to `fileMetadata`:

```javascript
fileMetadata: [
  { fileName: 'file1.pdf', totalPages: 30 },
  { fileName: 'file2.pdf', totalPages: 48 }
]
```

Upload each file to S3 separately using the respective keys from the presigned URL response.

## Common Issues

| Issue | Solution |
|-------|----------|
| `navigate` tool doesn't work | Use `window.location.href` via JS instead |
| Page requires Tailscale | Ensure exit node is set to dev before starting |
| Browser can't fetch external URLs | Tailscale blocks cross-origin requests; use AWS CLI for S3 |
| Large PDF can't be base64'd into browser | Use Hybrid API approach instead |
| File input triggers native picker | Use DataTransfer API, never click dropzone directly |
| Form fields have wrong refs | Call `read_page` with `filter: "interactive"` before filling |
| Cross-account S3 copy denied | Download to /tmp first, then upload from /tmp |
| Chrome extension popup blocks interaction | Create a new tab and retry |

## API Reference

These are the SvelteKit server routes that proxy to the backend:

| Route | Method | Purpose |
|-------|--------|---------|
| `/case/[slug]/presigned_url_case` | POST | Get presigned S3 upload URLs |
| `/case` | POST | Create case with metadata |

The `/case` POST body shape (backend Pydantic model: `CreateCaseDto`):
```typescript
{
  // Required fields
  caseId: string;
  fileMetadata: Array<{ fileName: string; pageCount: number }>;
  specialties: Array<{ specialty: string }>;  // e.g. "general", "ortho", "neuro", "pain", etc.

  // Optional fields
  patientInfo?: {
    name: { firstName: string; lastName: string; middleName?: string };
    dateOfBirth?: string;  // MM/DD/YYYY
  };
  lineOfBusiness?: 'WC' | 'BI';
  uploadedBy?: string;     // overridden server-side with session email
  bccEmails?: string[];
  dueDate?: string;        // MM/DD/YYYY
  comments?: string;
  reviewType?: string;
}
```

Valid `specialty` values: `general`, `ortho`, `neuro`, `pain`, `psych`, `pmr`, `chiro`, `internalMed`, `occupationalMed`.

**Source of truth:** `/Stream/backend/packages/dto/case/case_dto.py` — `CreateCaseDto` class.
