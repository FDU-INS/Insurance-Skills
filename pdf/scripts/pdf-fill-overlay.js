#!/usr/bin/env node
// Directly write text onto a PDF using pdf-lib (no HTML/Chrome intermediary)
// Uses the same coordinate system as the PDF itself — no alignment drift
// Usage: node pdf-fill-overlay.js <source.pdf> <config.json> <output.pdf>
//
// PDF coordinate system: origin is BOTTOM-LEFT, Y increases upward
// Use pdf-coords.js to find reference positions (note: it outputs top-left Y, so convert)

const fs = require('fs');
const { PDFDocument, rgb, StandardFonts } = require('pdf-lib');

async function fillPdf(sourcePath, configPath, outputPath) {
  const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
  const pdfBytes = fs.readFileSync(sourcePath);
  const pdfDoc = await PDFDocument.load(pdfBytes);
  const font = await pdfDoc.embedFont(StandardFonts.Helvetica);

  const pages = pdfDoc.getPages();

  for (const pageConfig of (config.pages || [])) {
    const pageIndex = pageConfig.page - 1;
    if (pageIndex < 0 || pageIndex >= pages.length) continue;
    const page = pages[pageIndex];
    const { height } = page.getSize();

    for (const field of (pageConfig.fields || [])) {
      const fontSize = field.fontSize || 10;
      const color = field.color ? parseColor(field.color) : rgb(0, 0, 0);
      
      // Config uses top-left origin (like pdf-coords.js output)
      // Convert to PDF bottom-left origin
      const x = field.x;
      const y = height - field.y;

      page.drawText(field.text, {
        x,
        y,
        size: fontSize,
        font,
        color,
      });
    }
  }

  const outputBytes = await pdfDoc.save();
  fs.writeFileSync(outputPath, outputBytes);
  console.log(`Written to ${outputPath}`);
}

function parseColor(c) {
  if (c === 'red') return rgb(1, 0, 0);
  if (c === 'blue') return rgb(0, 0, 1);
  if (c === 'green') return rgb(0, 0.5, 0);
  return rgb(0, 0, 0);
}

const [source, config, output] = process.argv.slice(2);
if (!source || !config || !output) {
  console.error('Usage: node pdf-fill-overlay.js <source.pdf> <config.json> <output.pdf>');
  process.exit(1);
}
fillPdf(source, config, output).catch(e => { console.error(e.message); process.exit(1); });
