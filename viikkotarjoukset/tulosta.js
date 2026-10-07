// Tulostaa HTML-päällyssivun läpinäkyvätaustaiseksi PDF:ksi.
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const [src, out] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + path.resolve(src), { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({ path: out, width: '11.02360in', height: '15.59055in', printBackground: true, omitBackground: true, preferCSSPageSize: true });
  await browser.close();
})();
