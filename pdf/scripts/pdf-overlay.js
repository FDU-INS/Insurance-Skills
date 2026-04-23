#!/usr/bin/env node
// Generates an HTML file with absolutely positioned text for PDF overlay
// Usage: node pdf-overlay.js <config.json> <output.html>

const fs = require('fs');

const configFile = process.argv[2];
const outputFile = process.argv[3];

if (!configFile || !outputFile) {
  console.error('Usage: node pdf-overlay.js <config.json> <output.html>');
  process.exit(1);
}

const config = JSON.parse(fs.readFileSync(configFile, 'utf8'));
const pageWidth = config.pageWidth || 612;
const pageHeight = config.pageHeight || 792;

let html = `<!DOCTYPE html>
<html>
<head>
<style>
  @page { size: ${pageWidth}pt ${pageHeight}pt; margin: 0; }
  body { margin: 0; padding: 0; }
  .page {
    width: ${pageWidth}pt;
    height: ${pageHeight}pt;
    position: relative;
    page-break-after: always;
    overflow: hidden;
  }
  .page:last-child { page-break-after: auto; }
  .field {
    position: absolute;
    font-family: Arial, Helvetica, sans-serif;
    color: black;
    white-space: nowrap;
  }
</style>
</head>
<body>
`;

// Sort pages by page number
const pages = (config.pages || []).sort((a, b) => a.page - b.page);

// totalPages can be specified in config to match the source PDF exactly
// This is critical for multistamp — it must have the same page count as the original
const maxPage = config.totalPages || (pages.length > 0 ? Math.max(...pages.map(p => p.page)) : 0);

for (let i = 1; i <= maxPage; i++) {
  const pageConfig = pages.find(p => p.page === i);
  html += `<div class="page">\n`;
  if (pageConfig && pageConfig.fields) {
    for (const field of pageConfig.fields) {
      const fontSize = field.fontSize || 10;
      const fontWeight = field.bold ? 'bold' : 'normal';
      const fontStyle = field.italic ? 'italic' : 'normal';
      const color = field.color || 'black';
      // Check/X mark support
      const text = field.text === '✓' || field.text === '✗' ? field.text : 
                   field.text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
      html += `  <div class="field" style="left:${field.x}pt; top:${field.y}pt; font-size:${fontSize}pt; font-weight:${fontWeight}; font-style:${fontStyle}; color:${color};">${text}</div>\n`;
    }
  }
  html += `</div>\n`;
}

html += `</body>\n</html>`;

fs.writeFileSync(outputFile, html);
console.log(`Overlay HTML written to ${outputFile} (${maxPage} pages)`);
