---
name: pdf-form-filler
description: Use this skill whenever the user wants to fill out a PDF form, analyze PDF form fields, troubleshoot form field mapping, verify field identification accuracy, or export a filled PDF. This includes tax forms (IRS 1040, W-2, W-4, W-9, 1099), government applications, contracts, legal documents, insurance forms, medical forms, and any PDF — with or without AcroForm fields. Also triggers when the user reports wrong field mapping ("it put 1f into 1d"), vision analysis failures, wants to improve field extraction accuracy, or needs to fill a flat/non-fillable PDF via annotations. If the user mentions a fillable PDF, asks to populate form fields, or wants to write text onto a flat PDF form, use this skill.
---

# PDF Form Filler Skill

You are an expert PDF form filling system. You fill any PDF with perfect field accuracy using two distinct modes:

1. **AcroForm mode** — PDFs with fillable fields: radial spatial identity, scanline context, Gemini vision, server-side validation
2. **Flat PDF mode** — PDFs with NO fillable fields: content stream geometry scanning, floor/ceiling detection, FreeText annotations with appearance streams

## Quick Reference

**CRITICAL FILES** (read these first when debugging):
- `src/hooks/usePdfFormFields.js` — Field extraction + spatial labels
- `src/utils/scanlineAccumulator.js` — Radial identity + bbox scoring
- `src/utils/formFieldsCsv.js` — CSV generation (13 columns)
- `server/src/routes/ai.ts` — Server: analyze-form, fill validation, prompt builder
- `src/validator.ts` — Server-side validation engine (5 rules)
- `src/form-state.ts` — Form state simulator (buildFormState, applyFields)
- `src/eval-runner.ts` — Eval assertion runner + intent parser

**SCRIPTS** (run from `PDF-Filler-Skill/scripts/`):
- `verify-field-map.ts` — Validate field mapping against ground truth
- `diagnose-field.ts` — Debug why a specific field maps wrong
- `dump-field-context.ts` — Dump all spatial context for every field
- `eval-fill-accuracy.ts` — Run automated fill accuracy eval
- `live-fill.ts` — End-to-end pipeline: prompt → intent → validate → fill JSON
- `flat-pdf-fill.py` — Flat PDF scanner + annotation filler (no AcroForm required)

**TESTS** (115 tests, 686 assertions):
- `__tests__/ground-truth.test.ts` — 27 tests: field map integrity
- `__tests__/validator.test.ts` — 25 tests: all 5 validation rules
- `__tests__/form-state.test.ts` — 17 tests: state management
- `__tests__/e2e-scenarios.test.ts` — 46 tests: all 6 eval scenarios + filing status matrix

For detailed architecture, see `architecture.md`.
For field extraction internals, see `field-extraction-guide.md`.
For validation rules, see `validation-rules.md`.
For system prompt construction, see `system-prompt-reference.md`.
For flat PDF filling technique, see `docs/flat-pdf-filling-guide.md`.

## How Form Filling Works

### Pipeline Overview

```
PDF opened in StickyApp
  |
  v
[1. EXTRACT] pdfjs-dist: getFieldObjects() + getTextContent()
  |           -> AcroForm fields (name, type, rect, options, maxLen, tooltip)
  |           -> Text layout (every character with x,y coordinates)
  |
  v
[2. ENRICH]  Three-layer spatial label matching:
  |           Layer 1: Heuristic directional (findLabelLeft/Above/Below/Right)
  |           Layer 2: Radial identity (ray cast + fragment clustering + line joining)
  |           Layer 3: Scanline accumulator (reading-order context + section detection)
  |           Cross-validation: bboxAdjacencyScore() confirms or overrides matches
  |
  v
[3. ANALYZE] Gemini vision (optional, auto-triggers if no cached template):
  |           -> Inject FIELD_IDs into PDF via pdf-lib
  |           -> Send modified PDF to Gemini page-by-page
  |           -> Parse: description, section, lineNumber, semanticType, format,
  |              calculation, dependencies, confidence
  |           -> Multi-pass: follow-up for missed fields
  |           -> Cache results as template in IndexedDB
  |
  v
[4. PROMPT]  Build AI system prompt:
  |           IF vision template: 13-column CSV (compact, semantic)
  |           ELSE: XML + Field Lookup Index + Text Search Index
  |
  v
[5. FILL]    AI calls fill_form_fields({ fields: {name: value}, reason })
  |           -> Server validates: unknown names, read-only, checkbox bool,
  |              dropdown options
  |           -> Valid fields emitted via SSE to client
  |           -> Validation errors returned to AI for retry
  |
  v
[6. EXPORT]  pdf-lib: write values -> flatten form -> overlay annotations -> download
```

### Mode 2: Flat PDF Pipeline (No AcroForm Fields)

For PDFs like the IRS W-9 that have NO fillable fields — just static drawings:

```
PDF with no AcroForm fields
  |
  v
[1. SCAN]    Parse content stream for geometric primitives:
  |           -> `re` operator: rectangles (checkboxes, digit boxes, borders)
  |           -> `q 1 0 0 1 TX TY cm ... S Q`: line segments with transforms
  |
  v
[2. CLASSIFY] Rectangle size → element type:
  |           -> 8×8 pt = checkbox
  |           -> 14.4×24 pt = digit input box
  |           -> Gaps between digit boxes = dash separators
  |           -> Pattern 3-2-4 = SSN (XXX-XX-XXXX)
  |           -> Pattern 2-7 = EIN (XX-XXXXXXX)
  |
  v
[3. DETECT]  Floor/ceiling detection:
  |           -> Extract text label positions via visitor pattern
  |           -> For each label, scan DOWN through h_lines to find floor (underline)
  |           -> For each label, scan UP to find ceiling (line above)
  |           -> Text sits ON the floor line, not below it
  |
  v
[4. PLACE]   FreeText annotations with appearance streams:
  |           -> Build /AP dictionary with PDF content stream (BT/Tf/Td/Tj/ET)
  |           -> Register /Helv font in /Resources
  |           -> Set /F=4 (print flag), /BS /W=0 (no border)
  |           -> Without /AP, annotations are INVISIBLE in most viewers
  |
  v
[5. WRITE]   pypdf writes annotations to output PDF
```

#### Content Stream Scanning

PDF pages are sequences of drawing commands. The `re` operator draws rectangles:
```
417.6 396.0 14.4 24.0 re    → digit box at (417.6, 396.0), 14.4w × 24h
73.0 603.7 8.0 8.0 re       → checkbox at (73.0, 603.7), 8w × 8h
```

Line segments use transformation matrices inside save/restore pairs:
```
q 1 0 0 1 543.35 587.97 cm   → translate to (543.35, 587.97)
0 0 m                         → moveto (0,0) in local coords
32.9 0 l                      → lineto (32.9, 0) — horizontal line
S                             → stroke
Q                             → restore state
```
Real position: horizontal line at y=587.97 from x=543.35 to x=576.25.

#### Floor Detection Algorithm

From a label position, scan outward then down to find the underline:

1. **Start** at label (x, y) — e.g., "Exempt payee code (if any)" at (457.6, 592.5)
2. **Scan down** through all horizontal lines where:
   - `line.y < label.y` (below the label)
   - `line.y > label.y - 40` (within 40pt)
   - Line overlaps horizontally with the label's x ± tolerance
3. **Pick nearest** (highest y = closest floor below)
4. **Place text** with annotation rect bottom AT the floor y-coordinate

Result: text sits precisely on the underline, exactly where a human would write.

#### Appearance Streams (Critical)

pypdf's `FreeText()` helper creates annotations WITHOUT `/AP` (appearance dictionary). Most PDF viewers ignore annotations that lack `/AP`. You MUST build it manually:

```python
# The appearance stream is a mini PDF content stream
ap_content = "BT\n/Helv 10 Tf\n0 g\n2 1.0 Td\n(5) Tj\nET"

ap_stream["/Type"] = "/XObject"
ap_stream["/Subtype"] = "/Form"
ap_stream["/BBox"] = [0, 0, width, height]
ap_stream["/Resources"] = {"/Font": {"/Helv": <Helvetica font dict>}}

annot["/AP"] = {"/N": ap_stream}   # /N = Normal appearance
annot["/DA"] = "/Helv 10 Tf 0 g"  # Default appearance fallback
annot["/F"] = 4                     # Print flag
annot["/BS"] = {"/W": 0}           # No border
```

### The Three Enrichment Layers

**Layer 1 — Heuristic Directional** (`usePdfFormFields.js`):
- For each field, search LEFT/ABOVE/BELOW/RIGHT for nearest text
- Scoring: `distance * bandOverlapBonus` (bbox Y-band overlap breaks ties)
- Fast but fails on dense forms where widget Y-offset (0.008) exceeds half the row spacing

**Layer 2 — Radial Identity** (`scanlineAccumulator.js`):
- Each field independently casts rays in 4 cardinal directions
- Collects ALL text fragments within ray band, clusters by Y (tolerance: 0.004)
- Joins fragments into full lines: "Your " + "first " + "name" -> "Your first name"
- LEFT ray: Y band = 0.025, picks line with Y >= field center (accounts for widget offset)
- Cross-validated with `bboxAdjacencyScore(field, text, direction)`:
  - Score = bandOverlapRatio * proximityScore (exponential decay)
  - If bbox finds different label with score > 0.5, bbox wins
- **Why radial works**: Each field finds its OWN labels, immune to global sort corruption

**Layer 3 — Scanline Accumulator** (`scanlineAccumulator.js`):
- Walk all elements (text + fields) in reading order (top-to-bottom, left-to-right)
- Maintain sliding window of last 10 text items -> `accumulatedContext`
- Detect section headers via regex (`/^(step|part|section|income|deductions|...)/i`)
- Detect grid regions: 3+ fields per Y-band, 2+ bands -> grid with column headers
- Detect dense-math regions: right column (x > 0.55), clustered calculation fields
- Output: currentSection, regionType, columnHeader, accumulatedContext

**Override Priority**: scanline lineNumber ALWAYS overrides heuristic lineNumber.
Radial identity is immune to the widget Y-offset bug that corrupts heuristic matching on dense forms.

## Reading the Form Field Map

### Vision-Analyzed Forms (CSV)

When Gemini has analyzed the form, the AI sees a 13-column CSV:

```
field_name,type,page,line,description,section,semantic_type,format,calculation,dependencies,value,options,status
```

- `field_name` — AcroForm name. Use EXACTLY this in fill_form_fields.
- `line` — Form line label ("1a", "25d"). Reference in conversation.
- `description` — What the field is for. AI-verified by Gemini vision.
- `semantic_type` — Data category: currency, ssn, ein, date, name, address, city, state, zip, phone, email, percent, integer, decimal, boolean, enum, text
- `format` — Value pattern: "$#,###.##", "###-##-####", "9 digits no dashes", "MM/DD/YYYY"
- `calculation` — Formula: "Line 11 = Line 9 - Line 10", "Sum of Lines 1a through 1z"
- `dependencies` — Pipe-delimited field names this depends on
- `options` — Pipe-delimited values for dropdowns/radios
- `status` — filled, empty, empty-required

### Heuristic Forms (XML)

Without vision analysis, the AI sees verbose XML with navigation indices:

```xml
<field name="f1_14" type="text" status="empty" page="1" line="Your first name">
  <primary-label>Your first name and middle initial</primary-label>
  <label-left>Your first name</label-left>
  <nearby-text>Your first name [left, closest] | Last name [right, near]</nearby-text>
  <field-right>f1_15</field-right>
  <max-length>25</max-length>
</field>
```

Plus a **Text Search Index** (visible text -> nearby fields) and **Field Lookup Index** (line/label -> field_name).

**WARNING**: On dense forms (IRS 1040 income section), heuristic `line` attributes may be offset by 1-2 positions. ALWAYS verify with:
1. `<primary-label>` and `<label-left>` text
2. Text Search Index (source of truth)
3. Neighbor tags (`<field-above>`, `<field-below>`)

## Filling Strategy

### Step 1: Read the Field Map
- Scan ALL fields before filling anything
- Identify: required fields, calculated fields, checkbox groups, dependencies
- Note format constraints (maxLen, semantic_type, format column)

### Step 2: Gather User Information
- Ask upfront for all needed data when possible
- Reference fields by **line number** + **description** (not cryptic field_name)
- For calculated fields, note which inputs must be filled first

### Step 3: Fill Fields
```
fill_form_fields({
  fields: {
    "f1_14": "John",
    "f1_15": "Doe",
    "f1_16": "123456789",    // SSN: 9 digits, no dashes (maxLen=9)
    "c1_1": true,            // Checkbox: boolean only
  },
  reason: "Filling identification section with user-provided data"
})
```

Rules:
- Fill ALL determinable fields in ONE tool call for efficiency
- Checkboxes: `true` or `false` (never "Yes", "On", "X")
- Dropdowns: exact value from options column
- SSN: check maxLen — if 9, use "123456789" not "123-45-6789"
- Currency: "$1,234.00" unless maxLen forces shorter
- Calculated fields: compute from inputs, don't leave blank

### Step 4: Handle Validation Errors
- Valid fields ARE applied even when some fail
- Parse error messages:
  - "Unknown field name" -> check field_name column for exact spelling
  - "Checkbox - use true or false" -> send boolean, not string
  - "Not in allowed options" -> check options column for exact values
  - "Read-only" -> skip this field
- Retry ONLY failed fields (don't re-send successful ones)

## Debugging Field Mapping Issues

When a field maps to the wrong location (e.g., "1f content appears in 1d"):

### Diagnosis Steps

1. **Check the template**: Is `visionAnalyzed: true`? If not, the AI is using heuristic labels which are unreliable on dense forms.

2. **Run the diagnostic script**:
   ```bash
   bun run PDF-Filler-Skill/scripts/diagnose-field.ts --field="f1_XX" --pdf=path/to/form.pdf
   ```
   This shows: heuristic label, radial label, scanline context, bbox scores, and what Gemini thinks.

3. **Check scanline override**: In `usePdfFormFields.js`, scanline lineNumber should ALWAYS override heuristic:
   ```javascript
   const scanLineNum = extractScanlineLineNumber(scanCtx);
   if (scanLineNum) {
     pf.scanlineLineNumber = scanLineNum;
     pf.lineNumber = scanLineNum; // Always override
   }
   ```

4. **Check radial identity**: The LEFT ray should find the correct label. If not:
   - Widget Y-offset may exceed RADIAL_Y_BAND (0.025)
   - Row spacing may be < 0.015 (extremely dense)
   - Text fragments may not cluster properly

5. **Force re-analysis**: Delete the cached template to trigger fresh Gemini analysis.

### Common Failure Modes

| Symptom | Root Cause | Fix |
|---------|-----------|-----|
| Line number off by 1-2 | Widget Y-offset on dense forms | Radial identity overrides heuristic |
| Wrong section label | Section header regex missed | Add pattern to section detection |
| Missing field in vision | Gemini truncated response | Multi-pass follow-up catches it |
| Checkbox in wrong group | Spatial proximity ambiguity | identifyCheckboxGroups() adds hints |
| Stale template descriptions | Old vision analysis cached | Auto-invalidation clears bad templates |
| Empty labels on scanned PDF | No text layer in PDF | OCR needed (out of scope) |

## Known Form Patterns

### IRS 1040 (199 fields, 3 pages)
- Page 1: Filing Status (checkboxes), Name/SSN, Address, Standard Deduction, Dependents
- Page 2: Income (Lines 1-9), Adjustments (10-11), Deductions (12-15)
- Page 3: Tax/Credits (16-24), Payments (25-37), Signature

Field naming: `f1_XX` (page 1 text), `f2_XX` (page 2 text), `c1_XX` (page 1 checkboxes), `c2_XX` (page 2 checkboxes)

SSN fields: maxLen=9, no dashes. Address fields: standard US format.

### IRS W-2, W-4, W-9, 1099
See `FORM_PAGE_DESCRIPTIONS` in `server/src/routes/ai.ts` for page-level priors.

## Eval Framework

### Running Evals

```bash
# Verify field map against ground truth
bun run PDF-Filler-Skill/scripts/verify-field-map.ts --form=1040

# Test fill accuracy (fills form, checks results)
bun run PDF-Filler-Skill/scripts/eval-fill-accuracy.ts --form=1040 --scenario=basic

# Dump all field context for debugging
bun run PDF-Filler-Skill/scripts/dump-field-context.ts --pdf=path/to/form.pdf
```

### Adding New Form Support

1. Create ground truth file: `evals/ground-truth-{form-name}.json`
2. Add page descriptions to `FORM_PAGE_DESCRIPTIONS` in `ai.ts`
3. Run `verify-field-map.ts` to check extraction accuracy
4. Run `eval-fill-accuracy.ts` to verify fill correctness
5. If accuracy < 95%, tune radial constants or add form-specific heuristics
