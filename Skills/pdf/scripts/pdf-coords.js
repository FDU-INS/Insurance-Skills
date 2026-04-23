#!/usr/bin/env node
// Extract text positions from a PDF to help with overlay coordinate mapping
// Usage: node pdf-coords.js <file.pdf> [page_number]

const fs = require('fs');
const pdfjsLib = require('pdfjs-dist/legacy/build/pdf.mjs');

async function getCoords(file, targetPage) {
  const data = new Uint8Array(fs.readFileSync(file));
  const doc = await pdfjsLib.getDocument({data}).promise;
  
  const startPage = targetPage || 1;
  const endPage = targetPage || doc.numPages;
  
  for (let i = startPage; i <= endPage; i++) {
    const page = await doc.getPage(i);
    const viewport = page.getViewport({scale: 1.0});
    const content = await page.getTextContent();
    
    console.log(`\n=== Page ${i} (${viewport.width}x${viewport.height}pt) ===`);
    
    for (const item of content.items) {
      if (!item.str.trim()) continue;
      // Transform coordinates: PDF uses bottom-left origin, we convert to top-left
      const tx = item.transform;
      const x = tx[4];
      const y = viewport.height - tx[5]; // flip Y axis
      const text = item.str.substring(0, 60);
      console.log(`  x:${Math.round(x)} y:${Math.round(y)} h:${Math.round(item.height)} "${text}"`);
    }
  }
}

const file = process.argv[2];
const page = process.argv[3] ? parseInt(process.argv[3]) : null;
if (!file) { console.error('Usage: node pdf-coords.js <file.pdf> [page]'); process.exit(1); }
getCoords(file, page).catch(e => { console.error(e.message); process.exit(1); });
