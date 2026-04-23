const fs = require('fs');
const pdfjsLib = require('pdfjs-dist/legacy/build/pdf.mjs');

async function extractText(file) {
  const data = new Uint8Array(fs.readFileSync(file));
  const doc = await pdfjsLib.getDocument({data}).promise;
  let text = '';
  for (let i = 1; i <= doc.numPages; i++) {
    const page = await doc.getPage(i);
    const content = await page.getTextContent();
    text += content.items.map(item => item.str).join(' ') + '\n---PAGE ' + i + '---\n';
  }
  return text;
}

const file = process.argv[2];
if (!file) { console.error('Usage: node pdf-extract.js <file.pdf>'); process.exit(1); }
extractText(file).then(t => console.log(t)).catch(e => { console.error(e.message); process.exit(1); });
