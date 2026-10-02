// Renders src/*.html to A4 PDFs: node render.js
const { chromium } = require('playwright');
const path = require('path');
const files = process.argv.slice(2).length ? process.argv.slice(2) : ['cv', 'cover-letter', 'libero-nordics-concept'];
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  for (const f of files) {
    await page.goto('file://' + path.join(__dirname, 'src', f + '.html'), { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    await page.pdf({ path: path.join(__dirname, `Kira-Krysanov-${f}.pdf`), format: 'A4', printBackground: true, preferCSSPageSize: true });
    console.log('rendered', f);
  }
  await browser.close();
})();
