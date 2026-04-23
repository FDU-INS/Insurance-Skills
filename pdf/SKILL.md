---
name: pdf
description: Read, extract text, fill forms, and overlay text on PDF files using pdftk and pdfjs-dist. Use when working with PDFs — extracting content, filling fillable form fields, or adding text to non-fillable PDFs via coordinate-based overlays. Handles insurance forms, applications, contracts, and any PDF document processing.
---

# PDF Skill

## Dependencies

- `pdftk` — PDF toolkit for form operations, stamping, merging, splitting
- `pdfjs-dist` — Mozilla's PDF.js for text extraction (npm, already installed)
- `google-chrome` — Available at `/usr/bin/google-chrome` for generating overlay PDFs from HTML

> **Note:** `pdfjs-dist` text extraction returns empty for scanned/image-based PDFs. For those, burst into individual pages with `pdftk` and view in the browser to read content visually.

## Quick Reference

### Extract text from a PDF
```bash
node /home/jenn/clawd/skills/pdf/scripts/pdf-extract.js <file.pdf>
```

### List fillable form fields
```bash
pdftk <file.pdf> dump_data_fields
```

### Fill a fillable PDF form
Create an FDF file with field values, then:
```bash
pdftk <form.pdf> fill_form <data.fdf> output <filled.pdf> flatten
```

To generate a blank FDF template from a form:
```bash
pdftk <form.pdf> generate_fdf output <template.fdf>
```

Edit the FDF template, setting `/V` values for each field. For text fields use `/V (value)`. For buttons/checkboxes use `/V /OptionName`. For Choice/dropdown fields use `/V (OptionText)` matching one of the `FieldStateOption` values.

> **Important:** Always use `generate_fdf` first to get the template, then edit the copy. Hand-crafted FDF files may fail to parse — pdftk is picky about the format (needs the binary header bytes from the template).

### Overlay text on non-fillable PDFs
For PDFs without form fields, generate an HTML overlay and stamp it:

1. Create an HTML file with absolutely positioned text matching PDF coordinates
2. Convert to PDF using Chrome: `google-chrome --headless --disable-gpu --print-to-pdf=overlay.pdf --no-margins overlay.html`
3. Stamp onto original: `pdftk original.pdf multistamp overlay.pdf output filled.pdf`

Use `scripts/pdf-overlay.js` to generate the overlay HTML:
```bash
node /home/jenn/clawd/skills/pdf/scripts/pdf-overlay.js <config.json> <output.html>
```

The config.json format (`totalPages` must match the source PDF page count for `multistamp` to work correctly):
```json
{
  "pageWidth": 612,
  "pageHeight": 792,
  "totalPages": 7,
  "pages": [
    {
      "page": 1,
      "fields": [
        {"x": 200, "y": 150, "text": "Boardwise", "fontSize": 10},
        {"x": 200, "y": 175, "text": "123 Main St", "fontSize": 10}
      ]
    }
  ]
}
```

Coordinates are in PDF points (72 points = 1 inch). Origin is top-left.

To find the right coordinates, screenshot the PDF page and estimate positions based on the layout, or use `scripts/pdf-coords.js` to get text positions from the existing PDF as reference points.

### Reading scanned/image PDFs
When `pdf-extract.js` returns empty pages, the PDF contains scanned images, not text. To read:

1. Burst into individual pages: `pdftk input.pdf burst output page_%02d.pdf`
2. Open each page in the browser (openclaw profile) and screenshot to read visually
3. Zoom out with `document.body.style.zoom = '0.35'` to see full page in Chrome PDF viewer

### Fillable form workflow (end-to-end)

```bash
# 1. Check if form has fields
pdftk form.pdf dump_data_fields

# 2. Generate FDF template
pdftk form.pdf generate_fdf output template.fdf

# 3. Copy and edit the template with values
cp template.fdf filled.fdf
# Edit filled.fdf — replace /V () with /V (Your Value) for text fields
# Replace /V /Off with /V /OptionName for buttons/checkboxes

# 4. Fill the form
pdftk form.pdf fill_form filled.fdf output filled.pdf

# 5. Optionally flatten (makes fields non-editable)
pdftk form.pdf fill_form filled.fdf output filled.pdf flatten
```

### Other pdftk operations
```bash
# Merge PDFs
pdftk a.pdf b.pdf cat output merged.pdf

# Split pages
pdftk input.pdf cat 1-3 output pages1-3.pdf

# Rotate pages
pdftk input.pdf cat 1-endeast output rotated.pdf

# Get PDF info
pdftk input.pdf dump_data

# Add password
pdftk input.pdf output protected.pdf owner_pw secret

# Remove password
pdftk protected.pdf input_pw secret output unlocked.pdf

# Stamp (overlay on every page)
pdftk input.pdf stamp overlay.pdf output stamped.pdf

# Multistamp (page-matched overlay)
pdftk input.pdf multistamp overlay.pdf output stamped.pdf

# Burst into individual pages
pdftk input.pdf burst output page_%02d.pdf
```
