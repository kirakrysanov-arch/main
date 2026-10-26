// Renders journal.html to the PDF and page previews. Run: node render.js
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 720, height: 960 }, deviceScaleFactor: 3 });
  await page.goto('file://' + path.join(__dirname, 'journal.html'), { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({ path: path.join(__dirname, '..', 'The-Match-Book-Tennis-Journal.pdf'), width: '7.5in', height: '10in', printBackground: true, preferCSSPageSize: true });
  const ids = process.argv.slice(2);
  for (const id of ids) {
    await page.locator('#' + id).screenshot({ path: path.join(__dirname, 'previews', id + '.png') });
  }
  await browser.close();
})();
