// Exports every sticker in stickers.html as a transparent PNG. Run: node render_stickers.js <out_dir>
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const out = process.argv[2];
const list = JSON.parse(fs.readFileSync(path.join(__dirname, 'stickers.json')));
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1560, height: 900 }, deviceScaleFactor: 4 });
  await page.goto('file://' + path.join(__dirname, 'stickers.html'), { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  for (const { id, cat } of list) {
    fs.mkdirSync(path.join(out, cat), { recursive: true });
    await page.locator('#' + id).screenshot({ path: path.join(out, cat, id + '.png'), omitBackground: true });
  }
  await browser.close();
})();
