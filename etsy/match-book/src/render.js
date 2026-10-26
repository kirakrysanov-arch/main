// Renders a journal theme to its PDF and page previews.
// Run: [THEME=retro] [NOPDF=1] [SRC=guide-retro.html OUT=listings/...pdf] node render.js <page ids...>
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const theme = process.env.THEME || 'club';
const html = process.env.SRC || (theme === 'club' ? 'journal.html' : `journal-${theme}.html`);
const pdf = process.env.OUT || path.join('listings', theme, 'upload', theme === 'club' ? 'The-Match-Book-Tennis-Journal.pdf' : `The-Match-Book-Tennis-Journal-${theme[0].toUpperCase() + theme.slice(1)}.pdf`);
const previews = path.join('previews', theme);
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 720, height: 960 }, deviceScaleFactor: 3 });
  await page.goto('file://' + path.join(__dirname, html), { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  if (!process.env.NOPDF) await page.pdf({ path: path.join(__dirname, '..', pdf), width: '7.5in', height: '10in', printBackground: true, preferCSSPageSize: true });
  fs.mkdirSync(path.join(__dirname, previews), { recursive: true });
  const ids = process.argv.slice(2);
  for (const id of ids) {
    await page.locator('#' + id).screenshot({ path: path.join(__dirname, previews, id + '.png') });
  }
  await browser.close();
})();
